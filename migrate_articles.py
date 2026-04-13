#!/usr/bin/env python3
"""
Grid the Grey — One-Time Article Migration Script
==================================================
Renames existing published articles to add YYYY-MM-DD- date prefix,
and injects slug: frontmatter field to preserve URLs.

Run ONCE from your repo root:
    python migrate_articles.py

Safe to run multiple times — already-prefixed files are skipped.
"""

import re
import sys
from pathlib import Path

POSTS_DIR = Path("hugo-site/content/posts")
date_prefix_re = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def extract_date(content: str) -> str:
    """Extract YYYY-MM-DD from the date: frontmatter field."""
    for line in content.splitlines():
        line = line.rstrip("\r")
        if line.startswith("date:"):
            val = line.split(":", 1)[1].strip().strip('"\'')
            m = re.match(r"(\d{4}-\d{2}-\d{2})", val)
            if m:
                return m.group(1)
    return ""


def has_slug_field(content: str) -> bool:
    for line in content.splitlines():
        if line.rstrip("\r").startswith("slug:"):
            return True
    return False


def inject_slug(content: str, slug: str) -> str:
    """Insert slug: field before the closing --- of frontmatter."""
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


def main():
    if not POSTS_DIR.exists():
        print(f"ERROR: {POSTS_DIR} not found. Run from repo root.")
        sys.exit(1)

    files = sorted(f for f in POSTS_DIR.glob("*.md") if f.name != "_index.md")
    print(f"Found {len(files)} article(s) in {POSTS_DIR}/\n")

    renamed = 0
    skipped = 0

    for f in files:
        # Already has date prefix — skip
        if date_prefix_re.match(f.name):
            print(f"SKIP (already prefixed): {f.name}")
            skipped += 1
            continue

        content = f.read_text(encoding="utf-8")
        bare_slug = f.stem
        date_prefix = extract_date(content)

        if not date_prefix:
            date_prefix = "2026-04-01"
            print(f"  WARNING: no date in {f.name} — using fallback {date_prefix}")

        new_name = f"{date_prefix}-{bare_slug}.md"
        new_path = POSTS_DIR / new_name

        # Inject slug: if missing
        if not has_slug_field(content):
            content = inject_slug(content, bare_slug)
            print(f"  + Added slug: \"{bare_slug}\"")

        # Write new file
        new_path.write_text(content, encoding="utf-8")
        # Remove old file
        f.unlink()

        print(f"RENAMED: {f.name}")
        print(f"     TO: {new_name}\n")
        renamed += 1

    print("=" * 50)
    print(f"Done. Renamed: {renamed}  |  Skipped: {skipped}")
    print()
    print("Next steps:")
    print("  git add hugo-site/content/posts/")
    print('  git commit -m "migrate: add date prefix and slug field to all articles"')
    print("  git push origin main")


if __name__ == "__main__":
    main()
