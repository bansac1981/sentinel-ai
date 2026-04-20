#!/usr/bin/env python3
"""
backfill_tldr.py — Backfill TL;DR fields for existing articles
===============================================================
Scans all published and draft posts, finds any missing tldr_what /
tldr_who_at_risk / tldr_actions fields, calls Claude to generate them
from the existing article content, and updates the front matter in-place.

USAGE
-----
    python backfill_tldr.py --dry-run    # preview which files would be updated
    python backfill_tldr.py              # apply updates to all articles
    python backfill_tldr.py --force      # re-generate even if fields already exist

COST
----
    ~$0.002 per article (claude-haiku-4-5 is used — fast and cheap for this task).
    A batch of 30 articles costs roughly $0.06.
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
POSTS_DIR   = Path(__file__).parent / "hugo-site" / "content" / "posts"
DRAFTS_DIR  = POSTS_DIR / "drafts"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
# Use Haiku for backfill — fast, cheap, good enough for structured extraction
CLAUDE_MODEL      = "claude-haiku-4-5-20251001"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("backfill_tldr")

# ── Front-matter helpers ──────────────────────────────────────────────────────
FM_PATTERN = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (fm_dict_raw_lines, body_text). fm_dict_raw_lines is a dict of key→raw_line."""
    m = FM_PATTERN.match(text)
    if not m:
        return {}, text
    fm_block = m.group(1)
    body = text[m.end():]
    # Simple key extraction — just check which keys are present
    keys = {}
    for line in fm_block.splitlines():
        kv = re.match(r'^(\w+)\s*:', line)
        if kv:
            keys[kv.group(1)] = line
    return keys, body


def needs_backfill(text: str, force: bool) -> bool:
    """Return True if the article is missing any tldr field (or force=True)."""
    if force:
        return True
    fm, _ = parse_frontmatter(text)
    # Check all three fields exist AND are non-empty
    for field in ("tldr_what", "tldr_who_at_risk", "tldr_actions"):
        if field not in fm:
            return True
        # Check value isn't empty string or empty list
        line = fm[field]
        val = line.split(":", 1)[1].strip() if ":" in line else ""
        if val in ('""', "''", "[]", ""):
            return True
    return False


def get_article_content(text: str) -> tuple[str, str, str]:
    """Extract title, summary, and body text from a post file."""
    title_m = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    summary_m = re.search(r'^summary:\s*"(.*?)"\s*$', text, re.MULTILINE | re.DOTALL)
    title   = title_m.group(1).strip() if title_m else ""
    summary = summary_m.group(1).strip() if summary_m else ""
    # Body = everything after the closing ---
    body_m = re.search(r'^---\n.*?\n---\n(.*)', text, re.DOTALL)
    body   = body_m.group(1).strip() if body_m else ""
    return title, summary, body


# ── Claude call ───────────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """\
You are an AI security editor writing concise TL;DR metadata for a security article.

Article title: {title}
Existing summary: {summary}

Article body:
{body}

Generate exactly three fields as a JSON object:

{{
  "tldr_what":        "<ONE punchy sentence — the core event/finding. Max 20 words. No filler. Start with the subject, not 'This article'.>",
  "tldr_who_at_risk": "<ONE sentence — who is most directly exposed and why. Be specific about the audience.>",
  "tldr_actions":     ["<short imperative action>", "<short imperative action>", "<short imperative action>"]
}}

Rules:
- tldr_what: tightest possible one-liner. Example: "A 3-stage exploit chain in Cursor AI gives attackers full shell access on developer machines."
- tldr_who_at_risk: name the specific audience. Example: "Developers using Cursor IDE to open untrusted repos or third-party codebases."
- tldr_actions: 2–4 short imperative actions, each under 12 words, grounded in this article's specifics.
- Return ONLY valid JSON. No markdown fences, no extra text.
"""


def generate_tldr(title: str, summary: str, body: str, client: Anthropic) -> dict | None:
    """Call Claude to generate tldr fields. Returns dict or None on failure."""
    # Truncate body to avoid token waste — first 1500 chars is enough
    body_excerpt = body[:1500] + ("…" if len(body) > 1500 else "")
    prompt = PROMPT_TEMPLATE.format(
        title=title,
        summary=summary,
        body=body_excerpt,
    )
    try:
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        # Strip accidental markdown fences
        raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
        raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        log.error(f"  ✗ Claude returned invalid JSON: {e}")
        return None
    except Exception as e:
        log.error(f"  ✗ Claude API error: {e}")
        return None


# ── Front-matter injection ────────────────────────────────────────────────────
def to_yaml_list(items: list) -> str:
    if not items:
        return "[]"
    escaped = [json.dumps(str(i)) for i in items]
    return "[" + ", ".join(escaped) + "]"


def update_frontmatter(text: str, fields: dict) -> str:
    """
    Inject or replace tldr_what / tldr_who_at_risk / tldr_actions in front matter.
    Inserts a # ── TL;DR ── block after the summary: line if not present.
    """
    # Build the replacement block lines
    tldr_what        = fields.get("tldr_what", "")
    tldr_who_at_risk = fields.get("tldr_who_at_risk", "")
    tldr_actions     = to_yaml_list(fields.get("tldr_actions", []))

    tldr_block = (
        f'\n# ── TL;DR ──\n'
        f'tldr_what: {json.dumps(tldr_what)}\n'
        f'tldr_who_at_risk: {json.dumps(tldr_who_at_risk)}\n'
        f'tldr_actions: {tldr_actions}'
    )

    # If a TL;DR block already exists, replace it entirely
    existing_block = re.compile(
        r'\n# ── TL;DR ──\n'
        r'tldr_what:.*?\n'
        r'tldr_who_at_risk:.*?\n'
        r'tldr_actions:.*?(?=\n#|\n---|\Z)',
        re.DOTALL,
    )
    if existing_block.search(text):
        return existing_block.sub(tldr_block, text)

    # Also replace any scattered individual tldr fields
    text = re.sub(r'\ntldr_what:.*', '', text)
    text = re.sub(r'\ntldr_who_at_risk:.*', '', text)
    text = re.sub(r'\ntldr_actions:.*', '', text)

    # Insert after the summary: line
    text = re.sub(
        r'(^summary:.*$)',
        r'\1' + tldr_block,
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return text


# ── Main ──────────────────────────────────────────────────────────────────────
def run(dry_run: bool, force: bool) -> None:
    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY not set in .env")
        sys.exit(1)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    all_posts = sorted(
        list(POSTS_DIR.glob("*.md")) + list(DRAFTS_DIR.glob("*.md"))
    )
    log.info(f"Found {len(all_posts)} post(s) to check.")

    updated = skipped = errors = 0

    for path in all_posts:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            log.warning(f"  Cannot read {path.name}: {e}")
            errors += 1
            continue

        if not needs_backfill(text, force):
            log.info(f"  skip  {path.name}  (tldr fields already present)")
            skipped += 1
            continue

        title, summary, body = get_article_content(text)
        if not body:
            log.warning(f"  skip  {path.name}  (no body content found)")
            skipped += 1
            continue

        log.info(f"  gen   {path.name}")
        log.info(f"        {title[:70]}")

        fields = generate_tldr(title, summary, body, client)
        if not fields:
            errors += 1
            continue

        log.info(f"        what:  {fields.get('tldr_what','')[:70]}")
        log.info(f"        risk:  {fields.get('tldr_who_at_risk','')[:70]}")
        log.info(f"        acts:  {fields.get('tldr_actions', [])}")

        if not dry_run:
            new_text = update_frontmatter(text, fields)
            path.write_text(new_text, encoding="utf-8")
            log.info(f"        ✓ written")

        updated += 1

    print()
    log.info("═" * 55)
    log.info(f"  Updated : {updated}{'  (dry run — not written)' if dry_run else ''}")
    log.info(f"  Skipped : {skipped}")
    log.info(f"  Errors  : {errors}")
    if dry_run and updated > 0:
        log.info("  Re-run without --dry-run to apply changes.")
    log.info("═" * 55)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill TL;DR fields (tldr_what, tldr_who_at_risk, tldr_actions) for existing articles.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--force",   action="store_true", help="Re-generate even if fields already exist")
    args = parser.parse_args()
    run(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
