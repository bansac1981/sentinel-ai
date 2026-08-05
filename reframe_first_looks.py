#!/usr/bin/env python3
"""
Batch reframe existing First Look articles from pessimistic attack-surface framing
to constructive defender-oriented framing.

Reads each published first_look article, extracts the existing content,
sends it to Claude for reframing, and writes back the updated article.

Usage:
    python reframe_first_looks.py                    # Process all
    python reframe_first_looks.py --limit 5          # Process first 5 only
    python reframe_first_looks.py --dry-run          # Preview without writing
    python reframe_first_looks.py --verbose          # Detailed logging
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
POSTS_DIR = Path(__file__).parent / "hugo-site" / "content" / "posts"
TRACKER_FILE = Path(__file__).parent / "reframed_articles.json"

REFRAME_PROMPT = """\
You are a senior AI security analyst reframing an existing article from Grid the Grey.

The original article was written with a pessimistic "attack surface" framing — treating every new defensive capability as primarily introducing threats. Your task is to reframe it with a constructive, defender-oriented perspective while retaining all factual content.

## Original Article Front Matter (YAML)
```
{front_matter}
```

## Original Article Body (Markdown)
{body}

## Reframing Instructions

Rewrite ONLY the following fields. Return a single valid JSON object (no markdown fences):

{{
  "summary": "<Reframed 2-3 sentence summary: first sentence describes the capability neutrally, second explains what defensive gap this closes, third (optional) notes what remains unaddressed>",
  "attack_vectors_introduced": ["<Reframe each as a defensive advance or capability this introduces for defenders — what can defenders now do that they couldn't before?>", ...],
  "tldr_who_at_risk": "<Reframe: who benefits from this capability and what gap it closes for them>",
  "tldr_actions": ["<Reframe as adoption/integration actions rather than defensive posture>", "<action 2>", "<action 3>"],
  "article_body": "<Reframed markdown article body — see format below>"
}}

## Article Body Format
Rewrite the body with these sections:
- ## Defender Impact — 1-2 sentence lead: what gap this closes for defenders and why it matters.
- ## Capability Overview — what shipped, described substantively. Retain all technical detail from the original. This should be the longest section.
- ## Defensive Advances — what new capabilities this gives defenders. Reframe the original "attack vectors" as capabilities gained.
- ## Residual Gaps — what this does NOT yet address. Reframe original attack surface concerns as honest limitations: coverage gaps, adoption barriers, maturity requirements. NOT adversary-introduced attack vectors.
- ## Framework Mapping — retain the original framework mappings but reframe the explanations to show how this capability ADDRESSES these technique categories rather than enabling them.
- ## Deployment Considerations — practical adoption guidance. Reframe original "threat scenarios" as operational considerations for teams integrating this capability.
- ## Defender Checklist — reframe as adoption/integration steps rather than defensive posture items.
- ## References — retain original reference links.

## Key Rules
- Retain ALL factual information from the original (vendor names, product details, dates, technical specifics).
- Do NOT invent new facts or capabilities not mentioned in the original.
- Frame residual concerns as maturity questions, not as reasons to fear the development.
- Tone: analytical, constructive, adoption-oriented. A reader should finish thinking "how do I adopt this" not "how could this hurt me".
- Keep body between 500-800 words.
- The tldr_actions should be imperative adoption steps, not defensive warnings.
- The attack_vectors_introduced field should list 3-5 defensive advances (despite the field name — it's retained for template compatibility).
"""


def load_tracker() -> dict:
    """Load the tracker file listing already-reframed articles."""
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text(encoding="utf-8"))
    return {"reframed": []}


def save_tracker(tracker: dict) -> None:
    """Save the tracker file."""
    TRACKER_FILE.write_text(json.dumps(tracker, indent=2, ensure_ascii=False), encoding="utf-8")


def find_first_look_articles(tracker: dict) -> list[Path]:
    """Find all published first_look articles not already in the tracker."""
    already_done = set(tracker.get("reframed", []))
    articles = []
    for f in sorted(POSTS_DIR.glob("2026-*.md")):
        if "drafts" in str(f):
            continue
        if f.name in already_done:
            continue
        content = f.read_text(encoding="utf-8")
        if 'content_type: "first_look"' not in content:
            continue
        articles.append(f)
    return articles


def parse_article(filepath: Path) -> tuple[str, str]:
    """Split article into front matter and body."""
    content = filepath.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", ""
    front_matter = parts[1].strip()
    body = parts[2].strip()
    return front_matter, body


ARRAY_FIELDS = {"attack_vectors_introduced", "tldr_actions", "mitre_techniques", "owasp_categories", "categories", "tags", "threat_actors"}


def update_front_matter_field(front_matter: str, field: str, new_value: str) -> str:
    """Replace a YAML field value in front matter. Handles multi-line arrays."""
    if field in ARRAY_FIELDS:
        # Array fields may span multiple lines — find and replace the whole value
        lines = front_matter.split('\n')
        new_lines = []
        in_field = False
        for line in lines:
            if line.startswith(f'{field}:'):
                new_lines.append(f'{field}: {new_value}')
                in_field = True
                if new_value.endswith(']'):
                    in_field = False
                continue
            if in_field:
                if line.startswith((' ', '\t')) or (line.startswith('"') and not line.startswith('#')):
                    continue
                else:
                    in_field = False
                    new_lines.append(line)
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)
    else:
        # Scalar field — wrap in JSON quotes
        lines = front_matter.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith(f'{field}:'):
                new_lines.append(f'{field}: {json.dumps(new_value)}')
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)


def to_yaml_list(items: list) -> str:
    """Convert a list to YAML inline array format."""
    return json.dumps(items, ensure_ascii=False)


def reframe_article(filepath: Path, client: Anthropic, log: logging.Logger, dry_run: bool = False) -> bool:
    """Reframe a single article. Returns True on success."""
    front_matter, body = parse_article(filepath)
    if not front_matter or not body:
        log.warning(f"  Skipping {filepath.name} — could not parse")
        return False

    prompt = REFRAME_PROMPT.format(front_matter=front_matter, body=body)

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        log.error(f"  ✗ Invalid JSON for {filepath.name}: {e}")
        return False
    except Exception as e:
        log.error(f"  ✗ API error for {filepath.name}: {e}")
        return False

    if dry_run:
        log.info(f"  [DRY RUN] Would reframe {filepath.name}")
        log.info(f"    New summary: {result.get('summary', '')[:80]}...")
        return True

    # Update front matter fields
    updated_fm = front_matter
    if result.get("summary"):
        updated_fm = update_front_matter_field(updated_fm, "summary", result["summary"])
    if result.get("attack_vectors_introduced"):
        updated_fm = update_front_matter_field(updated_fm, "attack_vectors_introduced",
                                                to_yaml_list(result["attack_vectors_introduced"]))
    if result.get("tldr_who_at_risk"):
        updated_fm = update_front_matter_field(updated_fm, "tldr_who_at_risk", result["tldr_who_at_risk"])
    if result.get("tldr_actions"):
        updated_fm = update_front_matter_field(updated_fm, "tldr_actions",
                                                to_yaml_list(result["tldr_actions"]))

    # Update the comment in front matter
    updated_fm = updated_fm.replace(
        "# ── First Look: Attack Surface Assessment ──",
        "# ── First Look: Capability Assessment ──"
    )

    # Build new file
    new_body = result.get("article_body", body)
    new_content = f"---\n{updated_fm}\n---\n\n{new_body}\n"

    filepath.write_text(new_content, encoding="utf-8")
    log.info(f"  ✓ Reframed {filepath.name}")
    return True


def fix_double_serialized_arrays(log: logging.Logger, dry_run: bool = False) -> int:
    """Find and fix articles where array fields were double-JSON-serialized."""
    # Pattern: a field that looks like tldr_actions: "[\"...\", \"...\"]"
    # (the array was wrapped in json.dumps as a scalar string)
    double_ser_pattern = re.compile(r'^((?:tldr_actions|attack_vectors_introduced):\s*)"(\[.*\])"$')

    fixed = 0
    for f in sorted(POSTS_DIR.glob("2026-*.md")):
        if "drafts" in str(f):
            continue
        content = f.read_text(encoding="utf-8")
        lines = content.split('\n')
        changed = False
        new_lines = []
        for line in lines:
            m = double_ser_pattern.match(line)
            if m:
                prefix = m.group(1)
                escaped_array = m.group(2)
                try:
                    actual_array = json.loads(escaped_array)
                    if isinstance(actual_array, list):
                        new_lines.append(f"{prefix}{json.dumps(actual_array, ensure_ascii=False)}")
                        changed = True
                        continue
                except json.JSONDecodeError:
                    pass
            new_lines.append(line)

        if changed:
            if dry_run:
                log.info(f"  [DRY RUN] Would fix arrays in {f.name}")
            else:
                f.write_text('\n'.join(new_lines), encoding="utf-8")
                log.info(f"  ✓ Fixed arrays in {f.name}")
            fixed += 1

    return fixed


def main():
    parser = argparse.ArgumentParser(description="Reframe First Look articles")
    parser.add_argument("--limit", type=int, default=0, help="Max articles to process (0 = all)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--verbose", action="store_true", help="Detailed logging")
    parser.add_argument("--start-from", type=int, default=0, help="Skip first N articles (for resuming)")
    parser.add_argument("--status", action="store_true", help="Show tracker status and exit")
    parser.add_argument("--fix-arrays", action="store_true", help="Fix double-serialized array fields in already-reframed articles")
    args = parser.parse_args()

    log = logging.getLogger("reframe")
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)

    tracker = load_tracker()

    if args.status:
        done = len(tracker.get("reframed", []))
        remaining = find_first_look_articles(tracker)
        log.info(f"Reframed: {done}")
        log.info(f"Remaining: {len(remaining)}")
        if remaining:
            log.info(f"Next up: {remaining[0].name}")
        return

    if args.fix_arrays:
        log.info("Scanning for double-serialized array fields...")
        fixed = fix_double_serialized_arrays(log, dry_run=args.dry_run)
        log.info(f"Fixed: {fixed} article(s)")
        return

    articles = find_first_look_articles(tracker)

    if args.start_from:
        articles = articles[args.start_from:]
    if args.limit:
        articles = articles[:args.limit]

    log.info(f"Already reframed: {len(tracker.get('reframed', []))}")
    log.info(f"Remaining to process: {len(articles)}")
    if args.dry_run:
        log.info("[DRY RUN MODE — no files will be modified]")

    client = Anthropic()
    success = 0
    failed = 0

    for i, filepath in enumerate(articles, 1):
        log.info(f"\n[{i}/{len(articles)}] {filepath.name}")
        if reframe_article(filepath, client, log, dry_run=args.dry_run):
            success += 1
            if not args.dry_run:
                tracker["reframed"].append(filepath.name)
                tracker["last_updated"] = datetime.now(timezone.utc).isoformat()
                save_tracker(tracker)
        else:
            failed += 1

        # Rate limiting — be respectful to the API
        if i < len(articles):
            time.sleep(1)

    log.info(f"\n{'='*60}")
    log.info(f"Done. Success: {success}, Failed: {failed}")
    log.info(f"Total reframed: {len(tracker.get('reframed', []))}")
    if args.dry_run:
        log.info("(Dry run — tracker not updated)")


if __name__ == "__main__":
    main()
