#!/usr/bin/env python3
"""Unpublish an article by URL, slug, title, or partial filename."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

CONTENT_DIRS = [
    Path(__file__).parent / "hugo-site" / "content" / "posts",
    Path(__file__).parent / "hugo-site" / "content" / "deep-signal",
]
SIGNAL_IMG_DIR = Path(__file__).parent / "hugo-site" / "static" / "img" / "signal"


def extract_slug_from_url(url: str) -> str | None:
    """Extract the slug from a gridthegrey.com URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return None
    # URL like /deep-signal/weekly-signal-report-2026w31/ or /posts/some-article/
    parts = path.split("/")
    return parts[-1] if parts else None


def normalize_input(identifier: str) -> str:
    """Detect if input is a URL and extract slug, otherwise return as-is."""
    if identifier.startswith("http://") or identifier.startswith("https://"):
        slug = extract_slug_from_url(identifier)
        if slug:
            print(f"  Extracted slug from URL: {slug}")
            return slug
    return identifier


def find_article(identifier: str) -> Path | None:
    """Find an article file matching by slug, title, partial filename, or URL."""
    slug = normalize_input(identifier)

    for content_dir in CONTENT_DIRS:
        if not content_dir.exists():
            continue
        for md_file in content_dir.glob("*.md"):
            # Match by filename
            if slug.lower() in md_file.stem.lower():
                return md_file

            text = md_file.read_text(encoding="utf-8")

            # Match by front-matter slug
            if re.search(rf'^slug:\s*"?{re.escape(slug)}"?\s*$', text, re.MULTILINE | re.IGNORECASE):
                return md_file

            # Match by title (exact or substring)
            title_match = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip().strip('"')
                if slug.lower() in title.lower() or title.lower() in slug.lower():
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
    parser.add_argument(
        "identifier",
        help="Article URL (https://gridthegrey.com/...), slug, title, or partial filename",
    )
    parser.add_argument(
        "--mode",
        choices=["draft", "delete"],
        default="draft",
        help="'draft' sets draft: true (default); 'delete' removes the file entirely",
    )
    args = parser.parse_args()

    article = find_article(args.identifier)
    if not article:
        print(f"ERROR: No article found matching '{args.identifier}'")
        print(f"  Searched: {', '.join(str(d) for d in CONTENT_DIRS)}")
        print()
        print("  Tip: Use the full URL, slug, article title, or part of the filename.")
        print("  Examples:")
        print("    python unpublish.py https://gridthegrey.com/deep-signal/weekly-signal-report-2026w31/")
        print("    python unpublish.py weekly-signal-report-2026w31")
        print('    python unpublish.py "Claude Code Security Playbook"')
        sys.exit(1)

    print(f"Found: {article.relative_to(Path(__file__).parent)}")

    if args.mode == "draft":
        set_draft(article)
    else:
        delete_article(article)

    print("Done.")


if __name__ == "__main__":
    main()
