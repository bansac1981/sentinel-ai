#!/usr/bin/env python3
"""
One-time script to backfill thumbnail (OG image) URLs for existing published articles
that have an empty thumbnail field.

Usage:
    python backfill_thumbnails.py [--dry-run]
"""
import os
import re
import sys
import time
import httpx

POSTS_DIR = "hugo-site/content/posts"
DRY_RUN = "--dry-run" in sys.argv


def fetch_og_image(url: str) -> str:
    if not url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; GridTheGrey/1.0)"}
        resp = httpx.get(url, headers=headers, timeout=8, follow_redirects=True)
        resp.raise_for_status()
        html = resp.text
        # Try og:image first
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html, re.IGNORECASE)
        if m:
            img_url = m.group(1).strip()
            if img_url.startswith("http"):
                return img_url
    except Exception as e:
        print(f"  [warn] Failed to fetch OG image from {url}: {e}")
    return ""


def backfill_file(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Only process files with empty thumbnail
    if not re.search(r'^thumbnail:\s*["\']?\s*["\']?\s*$', content, re.MULTILINE):
        return False  # Already has a thumbnail

    # Find source_url
    m = re.search(r'^source_url:\s*["\']?([^"\'\\n]+)["\']?', content, re.MULTILINE)
    if not m:
        print(f"  [skip] No source_url in {os.path.basename(filepath)}")
        return False

    source_url = m.group(1).strip()
    print(f"  Fetching OG image for: {os.path.basename(filepath)}")
    print(f"    URL: {source_url}")

    og_image = fetch_og_image(source_url)

    if not og_image:
        print(f"    [not found] No OG image")
        return False

    print(f"    [found] {og_image[:80]}...")

    if DRY_RUN:
        print(f"    [dry-run] Would update thumbnail field")
        return True

    # Replace thumbnail: "" or thumbnail: '' or thumbnail: (empty)
    new_content = re.sub(
        r'^(thumbnail:\s*)["\']?\s*["\']?$',
        f'thumbnail: "{og_image}"',
        content,
        flags=re.MULTILINE
    )

    if new_content == content:
        print(f"    [warn] Could not replace thumbnail field")
        return False

    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)

    print(f"    [updated]")
    return True


def main():
    if DRY_RUN:
        print("=== DRY RUN MODE — no files will be modified ===\n")

    posts_dir = POSTS_DIR
    if not os.path.isdir(posts_dir):
        print(f"Error: {posts_dir} not found. Run from repo root.")
        sys.exit(1)

    files = [f for f in os.listdir(posts_dir) if f.endswith(".md") and f != "_index.md"]
    print(f"Found {len(files)} published articles\n")

    updated = 0
    for filename in sorted(files):
        filepath = os.path.join(posts_dir, filename)
        if backfill_file(filepath):
            updated += 1
        time.sleep(0.5)  # Be polite to source servers

    print(f"\n{'[dry-run] Would update' if DRY_RUN else 'Updated'} {updated} of {len(files)} articles")


if __name__ == "__main__":
    main()
