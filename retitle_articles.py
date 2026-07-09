#!/usr/bin/env python3
"""
Grid the Grey — SEO Title Backfill
====================================
Re-evaluates article titles against SEO rules and rewrites suboptimal ones.
Slugs and all other front matter are left untouched.

Usage:
    python retitle_articles.py              # Dry run — show proposed changes only
    python retitle_articles.py --apply      # Write changes to disk
    python retitle_articles.py --limit 10   # Process at most 10 articles
    python retitle_articles.py --verbose    # Show Claude's reasoning
"""

import argparse
import json
import logging
import os
import re
import time
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
# Haiku is fast and cheap — sufficient for title evaluation
RETITLE_MODEL = os.getenv("RETITLE_MODEL", "claude-haiku-4-5")

HUGO_POSTS_DIR = Path(os.getenv("HUGO_POSTS_DIR", "hugo-site/content/posts"))

# ── Prompt ────────────────────────────────────────────────────────────────────

RETITLE_PROMPT = """\
You are an SEO specialist reviewing article titles for gridthegrey.com, an AI security news site.

Evaluate the CURRENT TITLE against these rules, then decide whether to keep or replace it.

## SEO Rules for threat_report titles
1. Length: 50-65 characters total
2. Front-load the primary keyword: CVE ID > product/tool name > attack technique > vendor
3. If a CVE number appears in the CVE tags field, it MUST appear in the title
4. Include the affected product or vendor name if one is clearly identified
5. Use plain English — avoid jargon acronyms unless they ARE the search term (e.g. RCE, SQLi are fine)
6. Do NOT start with "How", "Why", "What", or a bare number (e.g. "1,000...")
7. Do NOT use clickbait or vague phrases ("No one is talking about", "Here's why", etc.)
8. KEEP the title if it is already 50-65 chars, starts with a keyword, has no How/Why/What, and contains the CVE if one exists — do not rewrite for minor style preferences

## SEO Rules for first_look titles
1. Do NOT use any "First Look:" prefix — the site badge and /categories/first-look/ taxonomy handle that label
2. Length: 50-65 characters total
3. MUST include the vendor name (Google, OpenAI, Anthropic, Meta, Microsoft, AWS, NVIDIA, etc.)
4. MUST include the product or model name if one is mentioned
5. Use action verbs: Ships, Launches, Releases, Adds, Brings, Opens
6. Describe what shipped — not the security risk
7. Do NOT start with "How", "Why", or "What"
8. KEEP the title if it already satisfies rules 2-7 — even if it currently has a "First Look:" prefix, that alone is not sufficient reason to replace if the rest is good (just strip the prefix in new_title)

## Invented facts rule (critical)
Do NOT add attack techniques, vulnerability types, CVE IDs, vendor names, product names, statistics, or any other claims that are NOT explicitly present in the summary or tags provided. If you cannot write a strictly better title using only the provided information, set keep=true.

## Content type prefix rule (critical)
Never add or remove meaning by changing content type framing. If content_type is threat_report, the new title must NOT describe a product launch. If content_type is first_look, the new title must NOT describe an active exploit or breach.

## Good examples
- "CVE-2025-59528: Flowise RCE Exploited Across 12,000 Instances"  (threat, 61 chars — keep)
- "Cursor IDE Prompt Injection Enables Full OS Code Execution"  (threat, 58 chars — keep)
- "SkillCloak Bypasses AI Agent Skill Scanners at 90% Rate"  (threat, 56 chars — keep)
- "Anthropic Ships Claude Code with Terminal Access"  (first_look, 48 chars — keep)
- "Google Launches Gemini 2.5 with Agentic File Access"  (first_look, 52 chars — keep)

## Article to evaluate
Content type: {content_type}
Current title: {current_title}
Summary: {summary}
Tags: {tags}
CVE tags (if any): {cve_tags}
MITRE techniques: {mitre_techniques}
OWASP categories: {owasp_categories}

## Your task
Return a single JSON object with no markdown fences:
{{
  "keep": <true if current title already satisfies the rules, false if it should be replaced>,
  "reason": "<one sentence explaining the keep/replace decision>",
  "new_title": "<the improved title — only required when keep=false, otherwise empty string>"
}}

When keep=false: new_title must be 50-65 characters, use only facts from the summary/tags above, and follow all rules. Verify your character count before returning.
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def setup_logging(verbose: bool) -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    return logging.getLogger("retitle")


def parse_front_matter(text: str) -> dict:
    """Extract key fields from YAML front matter. Returns dict of raw string values."""
    fields = {}
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return fields
    fm = fm_match.group(1)

    for key in ("title", "summary", "content_type", "tags", "mitre_techniques", "owasp_categories"):
        m = re.search(rf'^{key}:\s*(.+)$', fm, re.MULTILINE)
        if m:
            fields[key] = m.group(1).strip().strip('"').strip("'")
    return fields


def extract_cve_tags(tags_raw: str) -> list[str]:
    """Pull CVE identifiers out of a tags string like '[\"cve-2025-1234\", ...]'."""
    return re.findall(r'cve-\d{4}-\d+', tags_raw.lower())


def replace_title_in_file(path: Path, new_title: str) -> bool:
    """Overwrite only the title: line in the front matter. Returns True on success."""
    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        r'^(title:\s*)(".*?"|\'.*?\')(\s*)$',
        lambda m: f'{m.group(1)}{json.dumps(new_title)}{m.group(3)}',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def evaluate_title(fields: dict, client: Anthropic, log: logging.Logger) -> dict | None:
    """Ask Claude Haiku to evaluate and optionally replace the title."""
    tags_raw = fields.get("tags", "[]")
    cve_tags = extract_cve_tags(tags_raw)

    prompt = RETITLE_PROMPT.format(
        content_type=fields.get("content_type", "threat_report"),
        current_title=fields.get("title", ""),
        summary=fields.get("summary", "")[:300],
        tags=tags_raw[:200],
        cve_tags=", ".join(cve_tags) if cve_tags else "none",
        mitre_techniques=fields.get("mitre_techniques", "[]")[:150],
        owasp_categories=fields.get("owasp_categories", "[]")[:150],
    )

    try:
        response = client.messages.create(
            model=RETITLE_MODEL,
            max_tokens=384,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        # Extract only the first complete JSON object — Claude sometimes appends
        # extra reasoning text after the closing brace which breaks json.loads()
        match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if not match:
            log.error(f"  No JSON object found in response | raw: {raw[:200]}")
            return None
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        log.error(f"  Invalid JSON from Claude: {e} | raw: {raw[:200]}")
        return None
    except Exception as e:
        log.error(f"  Claude API error: {e}")
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace, log: logging.Logger) -> None:
    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY is not set.")
        raise SystemExit(1)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    md_files = sorted(HUGO_POSTS_DIR.glob("*.md"))
    md_files = [f for f in md_files if f.stem != "_index"]

    if args.limit:
        md_files = md_files[: args.limit]

    log.info(f"Articles to evaluate: {len(md_files)}")
    if not args.apply:
        log.info("DRY RUN — pass --apply to write changes")
    log.info("=" * 60)

    stats = {"kept": 0, "changed": 0, "skipped": 0, "errors": 0}

    for i, path in enumerate(md_files, 1):
        text = path.read_text(encoding="utf-8", errors="ignore")
        fields = parse_front_matter(text)

        if not fields.get("title"):
            log.warning(f"[{i}/{len(md_files)}] No title found — skipping: {path.name}")
            stats["skipped"] += 1
            continue

        log.info(f"[{i}/{len(md_files)}] {fields['title'][:80]}")

        result = evaluate_title(fields, client, log)
        if result is None:
            stats["errors"] += 1
            time.sleep(1.0)
            continue

        if result.get("keep"):
            log.info(f"  KEEP  — {result.get('reason', '')}")
            stats["kept"] += 1
        else:
            new_title = result.get("new_title", "").strip()
            if not new_title:
                log.warning("  Claude said replace but gave no new_title — skipping")
                stats["skipped"] += 1
            elif len(new_title) < 40:
                log.warning(f"  REJECTED — new_title is {len(new_title)} chars (<40): {new_title}")
                stats["skipped"] += 1
            elif len(new_title) > 65:
                log.warning(f"  REJECTED — new_title is {len(new_title)} chars (>65): {new_title}")
                stats["skipped"] += 1
            else:
                log.info(f"  REPLACE — {result.get('reason', '')}")
                log.info(f"    OLD: {fields['title']}")
                log.info(f"    NEW: {new_title} ({len(new_title)} chars)")
                if args.apply:
                    ok = replace_title_in_file(path, new_title)
                    if ok:
                        stats["changed"] += 1
                    else:
                        log.warning("  File write had no effect — pattern mismatch")
                        stats["errors"] += 1
                else:
                    stats["changed"] += 1  # count as would-change in dry run

        time.sleep(0.3)  # stay well under Haiku rate limits

    log.info("\n" + "=" * 60)
    log.info("RETITLE COMPLETE")
    log.info(f"  Kept as-is:     {stats['kept']}")
    log.info(f"  {'Changed' if args.apply else 'Would change'}:  {stats['changed']}")
    log.info(f"  Skipped:        {stats['skipped']}")
    log.info(f"  Errors:         {stats['errors']}")
    if not args.apply and stats["changed"] > 0:
        log.info("\nRun with --apply to write these changes to disk.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Grid the Grey — SEO Title Backfill")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to disk (default: dry run)")
    parser.add_argument("--limit", type=int, default=0, metavar="N",
                        help="Process at most N articles")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable DEBUG logging")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log = setup_logging(args.verbose)
    log.info("╔══════════════════════════════════════╗")
    log.info("║   GRID THE GREY  —  SEO Title Backfill  ║")
    log.info("╚══════════════════════════════════════╝")
    run(args, log)
