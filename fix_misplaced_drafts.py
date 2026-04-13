#!/usr/bin/env python3
"""
Grid the Grey — Fix Misplaced Drafts
=====================================
Finds draft articles sitting in posts/ (without date prefix) that should be
in posts/drafts/. Moves them with a date prefix and adds slug: frontmatter.

Run from repo root:
    python fix_misplaced_drafts.py
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

POSTS_DIR  = Path("hugo-site/content/posts")
DRAFTS_DIR = POSTS_DIR / "drafts"
date_prefix_re = re.compile(r"^\d{4}-\d{2}-\d{2}-")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def extract_fields(content: str) -> dict:
    fields = {"draft": False, "date": "", "slug": ""}
    in_fm = False
    for i, line in enumerate(content.splitlines()):
        line = line.rstrip("\r")
        if i == 0 and line.strip() == "---":
            in_fm = True
            continue
        if in_fm and line.strip() == "---":
            break
        if not in_fm:
            continue
        if line.startswith("draft:"):
            fields["draft"] = line.split(":", 1)[1].strip().lower() == "true"
        elif line.startswith("date:"):
            fields["date"] = line.split(":", 1)[1].strip().strip('"\'')
        elif line.startswith("slug:"):
            fields["slug"] = line.split(":", 1)[1].strip().strip('"\'')
    return fields


def inject_slug(content: str, slug: str) -> str:
    lines = content.splitlines(keepends=True)
    new_lines = []
    in_fm = False
    fm_closed = False
    inserted = False
    for i, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        if i == 0 and stripped == "---":
            in_fm = True
            new_lines.append(line)
            continue
        if in_fm and not fm_closed and stripped == "---":
            if not inserted:
                new_lines.append(f'slug: "{slug}"\n')
                inserted = True
            fm_closed = True
        new_lines.append(line)
    return "".join(new_lines)


def extract_date_prefix(date_str: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
    return m.group(1) if m else TODAY


def main():
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(f for f in POSTS_DIR.glob("*.md") if f.name != "_index.md")
    print(f"Scanning {len(files)} file(s) in posts/...\n")

    moved = 0
    skipped = 0

    for f in files:
        # Skip already date-prefixed (properly migrated published articles)
        if date_prefix_re.match(f.name):
            skipped += 1
            continue

        content = f.read_text(encoding="utf-8")
        fields  = extract_fields(content)

        # Only move if still a draft
        if not fields["draft"]:
            print(f"SKIP (published, no date prefix — check manually): {f.name}")
            skipped += 1
            continue

        bare_slug   = f.stem
        date_prefix = extract_date_prefix(fields["date"]) if fields["date"] else TODAY
        new_name    = f"{date_prefix}-{bare_slug}.md"
        dest        = DRAFTS_DIR / new_name

        # Add slug: frontmatter if missing
        if not fields["slug"]:
            content = inject_slug(content, bare_slug)
            print(f"  + Added slug: \"{bare_slug}\"")

        dest.write_text(content, encoding="utf-8")
        f.unlink()

        print(f"MOVED:  posts/{f.name}")
        print(f"    TO: posts/drafts/{new_name}\n")
        moved += 1

    print("=" * 50)
    print(f"Done.  Moved to drafts: {moved}  |  Skipped: {skipped}")
    if moved > 0:
        print()
        print("Next steps:")
        print("  git add hugo-site/content/posts/")
        print('  git commit -m "fix: move misplaced drafts to posts/drafts/ with date prefix"')
        print("  git push origin main")


if __name__ == "__main__":
    main()
