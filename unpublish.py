#!/usr/bin/env python3
"""Unpublish an article by slug — set to draft or delete entirely."""

import argparse
import re
import shutil
import sys
from pathlib import Path

CONTENT_DIRS = [
    Path(__file__).parent / "hugo-site" / "content" / "posts",
    Path(__file__).parent / "hugo-site" / "content" / "deep-signal",
]
SIGNAL_IMG_DIR = Path(__file__).parent / "hugo-site" / "static" / "img" / "signal"


def find_article(slug: str) -> Path | None:
    """Find an article file matching the given slug (filename or front-matter slug)."""
    for content_dir in CONTENT_DIRS:
        if not content_dir.exists():
            continue
        for md_file in content_dir.glob("*.md"):
            if slug in md_file.stem:
                return md_file
            text = md_file.read_text(encoding="utf-8")
            if re.search(rf'^slug:\s*"?{re.escape(slug)}"?\s*$', text, re.MULTILINE):
                return md_file
    return None


def set_draft(article_path: Path) -> None:
    """Set draft: true in front matter."""
    text = article_path.read_text(encoding="utf-8")

    if re.search(r"^draft:\s*true\s*$", text, re.MULTILINE):
        print(f"  Already draft: {article_path.name}")
        return

    if re.search(r"^draft:\s*false\s*$", text, re.MULTILINE):
        text = re.sub(r"^draft:\s*false\s*$", "draft: true", text, count=1, flags=re.MULTILINE)
    else:
        text = re.sub(r"^(---\s*\n)", r"\1draft: true\n", text, count=1, flags=re.MULTILINE)

    article_path.write_text(text, encoding="utf-8")
    print(f"  Set to draft: {article_path.name}")


def delete_article(article_path: Path) -> None:
    """Delete the article file and any associated signal chart images."""
    # Check for associated chart images (signal reports)
    text = article_path.read_text(encoding="utf-8")
    slug_match = re.search(r'^slug:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
    if slug_match:
        slug_val = slug_match.group(1).strip()
        week_match = re.search(r"(\d{4}w\d{2})", slug_val)
        if week_match and SIGNAL_IMG_DIR.exists():
            week_tag = week_match.group(1)
            for img in SIGNAL_IMG_DIR.glob(f"*{week_tag}*"):
                print(f"  Deleting chart image: {img.name}")
                img.unlink()

    print(f"  Deleting article: {article_path.name}")
    article_path.unlink()


def main():
    parser = argparse.ArgumentParser(description="Unpublish a mistakenly published article")
    parser.add_argument("slug", help="Article slug or partial filename to match")
    parser.add_argument(
        "--mode",
        choices=["draft", "delete"],
        default="draft",
        help="'draft' sets draft: true (default); 'delete' removes the file entirely",
    )
    args = parser.parse_args()

    article = find_article(args.slug)
    if not article:
        print(f"ERROR: No article found matching '{args.slug}'")
        print(f"  Searched: {', '.join(str(d) for d in CONTENT_DIRS)}")
        sys.exit(1)

    print(f"Found: {article.relative_to(Path(__file__).parent)}")

    if args.mode == "draft":
        set_draft(article)
    else:
        delete_article(article)

    print("Done.")


if __name__ == "__main__":
    main()
