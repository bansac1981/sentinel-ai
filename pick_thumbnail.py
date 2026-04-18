#!/usr/bin/env python3
"""
pick_thumbnail.py — Let you choose exact Pexels photos for article thumbnails.

HOW IT WORKS
------------
When the pipeline creates a draft post it writes two helper fields:

    thumbnail:        "https://...auto-picked image..."
    thumbnail_pexels_id: ""          ← you fill this in
    thumbnail_search: "https://www.pexels.com/search/ransomware+cyber+attack/"

Your workflow per article:
  1. Open the draft .md file in any editor.
  2. Click the thumbnail_search URL → Pexels opens with pre-filtered results.
  3. Find a photo you prefer → copy the ID from its URL:
       https://www.pexels.com/photo/dark-server-room-1181316/  →  ID = 1181316
  4. Paste the ID into thumbnail_pexels_id:  1181316
  5. Save the file.

Then run ONE command to resolve all your picks at once:

    python pick_thumbnail.py --resolve --write

The script calls the Pexels API for each filled-in ID, fetches the correct
image URL, and updates thumbnail: in the file. The two helper fields are then
cleared so the file stays tidy.

USAGE
-----
    python pick_thumbnail.py --list             # show all posts with pending picks
    python pick_thumbnail.py --resolve          # dry-run: preview what would change
    python pick_thumbnail.py --resolve --write  # apply changes
    python pick_thumbnail.py --search "dark hacker"  # search Pexels and print results
    python pick_thumbnail.py --photo 1181316    # preview a single Pexels photo by ID

REQUIREMENTS
------------
    pip install httpx python-dotenv
    PEXELS_API_KEY in your .env file
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus

import httpx
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
POSTS_DIR   = Path(__file__).parent / "hugo-site" / "content" / "posts"
DRAFTS_DIR  = POSTS_DIR / "drafts"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PEXELS_PHOTO_URL = "https://api.pexels.com/v1/photos/{id}"
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pick_thumbnail")


# ── Pexels helpers ────────────────────────────────────────────────────────────
def _headers() -> dict:
    return {"Authorization": PEXELS_API_KEY}


def fetch_photo_by_id(photo_id: str | int) -> dict | None:
    """Fetch a single Pexels photo by ID. Returns the photo dict or None."""
    try:
        resp = httpx.get(
            PEXELS_PHOTO_URL.format(id=photo_id),
            headers=_headers(),
            timeout=8.0,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log.error(f"Pexels API error fetching photo {photo_id}: {e}")
        return None


def search_pexels(query: str, per_page: int = 10) -> list:
    """Search Pexels and return list of photo dicts."""
    try:
        resp = httpx.get(
            PEXELS_SEARCH_URL,
            params={"query": query, "per_page": per_page, "orientation": "landscape"},
            headers=_headers(),
            timeout=8.0,
        )
        resp.raise_for_status()
        return resp.json().get("photos", [])
    except Exception as e:
        log.error(f"Pexels search error: {e}")
        return []


def photo_url(photo: dict) -> str:
    """Extract the large (~940px) image URL from a Pexels photo dict."""
    return photo.get("src", {}).get("large", "")


def photo_summary(photo: dict) -> str:
    """One-line summary of a Pexels photo for display."""
    pid      = photo.get("id", "?")
    alt      = photo.get("alt", "")[:60]
    photog   = photo.get("photographer", "")
    url      = photo_url(photo)
    page_url = photo.get("url", "")
    return (
        f"  ID: {pid}\n"
        f"  Alt: {alt}\n"
        f"  By: {photog}\n"
        f"  Image URL: {url}\n"
        f"  Pexels page: {page_url}"
    )


# ── Front-matter helpers ──────────────────────────────────────────────────────
_FM_THUMBNAIL_ID  = re.compile(r'^thumbnail_pexels_id:\s*"?(\d+)"?\s*$', re.MULTILINE)
_FM_THUMBNAIL     = re.compile(r'^thumbnail:.*$', re.MULTILINE)
_FM_SEARCH        = re.compile(r'^thumbnail_search:.*$', re.MULTILINE)
_FM_ID_FIELD      = re.compile(r'^thumbnail_pexels_id:.*$', re.MULTILINE)


def get_pending_id(text: str) -> tuple[str | None, str]:
    """
    Return (photo_id, source_field) for any pending Pexels ID, or (None, "").

    Checks thumbnail_pexels_id first (correct field), then falls back to
    thumbnail_search — in case the user accidentally pasted the numeric ID
    there instead of into thumbnail_pexels_id.
    """
    # Correct field
    m = _FM_THUMBNAIL_ID.search(text)
    if m:
        val = m.group(1).strip()
        if val.isdigit():
            return val, "thumbnail_pexels_id"

    # Fallback: ID accidentally placed in thumbnail_search
    search_val = get_search_url(text)
    if search_val.isdigit():
        return search_val, "thumbnail_search"

    return None, ""


def get_title(text: str) -> str:
    """Extract title from front-matter."""
    m = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else "(unknown)"


def get_search_url(text: str) -> str:
    """Extract thumbnail_search URL from front-matter."""
    m = re.search(r'^thumbnail_search:\s*"?([^"\n]*)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def apply_thumbnail(text: str, url: str) -> str:
    """
    Update thumbnail: with the new URL and clear the helper fields
    (thumbnail_pexels_id → empty, thumbnail_search → cleared).
    """
    # Update thumbnail:
    text = _FM_THUMBNAIL.sub(f'thumbnail: "{url}"', text)
    # Clear the ID field (keep the field so future edits are easy)
    text = _FM_ID_FIELD.sub('thumbnail_pexels_id: ""', text)
    # Clear the search URL (no longer needed once resolved)
    text = _FM_SEARCH.sub('thumbnail_search: ""', text)
    return text


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_list() -> None:
    """List all posts that have a thumbnail_pexels_id waiting to be resolved."""
    pending = []
    for path in sorted(list(POSTS_DIR.glob("*.md")) + list(DRAFTS_DIR.glob("*.md"))):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        pid, field = get_pending_id(text)
        if pid:
            title = get_title(text)
            search = get_search_url(text)
            pending.append((path, pid, field, title, search))

    if not pending:
        log.info("No posts have a thumbnail_pexels_id set. Nothing to resolve.")
        return

    log.info(f"Posts with pending thumbnail picks ({len(pending)}):\n")
    for path, pid, field, title, search in pending:
        print(f"  File   : {path.name}")
        print(f"  Title  : {title[:70]}")
        print(f"  ID set : {pid}  (found in: {field})")
        if field != "thumbnail_pexels_id":
            print(f"  ⚠ ID was in '{field}' — will be auto-corrected on resolve")
        if search and not search.isdigit():
            print(f"  Search : {search}")
        print()


def cmd_resolve(write: bool) -> None:
    """Resolve all thumbnail_pexels_id fields to real URLs."""
    if not PEXELS_API_KEY:
        log.error("PEXELS_API_KEY not set. Add it to your .env file.")
        sys.exit(1)

    all_posts = list(POSTS_DIR.glob("*.md")) + list(DRAFTS_DIR.glob("*.md"))
    resolved = skipped = errors = 0

    for path in sorted(all_posts):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            log.warning(f"Cannot read {path.name}: {e}")
            errors += 1
            continue

        pid, field = get_pending_id(text)
        if not pid:
            continue

        title = get_title(text)
        log.info(f"\n  {path.name}")
        log.info(f"  Title : {title[:70]}")
        log.info(f"  ID    : {pid}")
        if field != "thumbnail_pexels_id":
            log.info(f"  ⚠ ID found in '{field}' (not thumbnail_pexels_id) — auto-correcting")

        photo = fetch_photo_by_id(pid)
        if not photo:
            log.warning(f"  ✗ Could not fetch photo {pid} — skipping")
            errors += 1
            continue

        url = photo_url(photo)
        if not url:
            log.warning(f"  ✗ Photo {pid} has no large image URL — skipping")
            errors += 1
            continue

        log.info(f"  Alt   : {photo.get('alt', '')[:60]}")
        log.info(f"  By    : {photo.get('photographer', '')}")
        log.info(f"  URL   : {url[:80]}")

        if write:
            new_text = apply_thumbnail(text, url)
            path.write_text(new_text, encoding="utf-8")
            log.info(f"  ✓ Written")
        else:
            log.info(f"  (dry-run — not written)")

        resolved += 1

    print()
    log.info(f"=== Done ===")
    log.info(f"  Resolved : {resolved}")
    log.info(f"  Skipped  : {skipped}")
    log.info(f"  Errors   : {errors}")
    if not write and resolved > 0:
        log.info(f"\nRun with --write to apply changes.")


def cmd_search(query: str) -> None:
    """Search Pexels and print results so you can pick an ID."""
    if not PEXELS_API_KEY:
        log.error("PEXELS_API_KEY not set. Add it to your .env file.")
        sys.exit(1)

    log.info(f'Searching Pexels for: "{query}"\n')
    photos = search_pexels(query, per_page=10)

    if not photos:
        log.info("No results found.")
        return

    for i, photo in enumerate(photos, 1):
        print(f"[{i}]")
        print(photo_summary(photo))
        print()

    print(f"To use one: add its ID to thumbnail_pexels_id: in your post's front-matter,")
    print(f"then run:   python pick_thumbnail.py --resolve --write")


def cmd_photo(photo_id: str) -> None:
    """Preview a single Pexels photo by ID."""
    if not PEXELS_API_KEY:
        log.error("PEXELS_API_KEY not set. Add it to your .env file.")
        sys.exit(1)

    photo = fetch_photo_by_id(photo_id)
    if not photo:
        log.error(f"Photo {photo_id} not found.")
        sys.exit(1)

    print(photo_summary(photo))


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Choose specific Pexels photos for article thumbnails.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pick_thumbnail.py --list
  python pick_thumbnail.py --resolve
  python pick_thumbnail.py --resolve --write
  python pick_thumbnail.py --search "dark server room hacker"
  python pick_thumbnail.py --photo 1181316
        """,
    )
    parser.add_argument("--list",    action="store_true", help="List posts with a pending thumbnail_pexels_id")
    parser.add_argument("--resolve", action="store_true", help="Resolve all pending IDs to image URLs")
    parser.add_argument("--write",   action="store_true", help="Actually update files (used with --resolve)")
    parser.add_argument("--search",  metavar="QUERY",     help="Search Pexels and print photo IDs + previews")
    parser.add_argument("--photo",   metavar="ID",        help="Preview a single Pexels photo by ID")
    parser.add_argument("--debug",   action="store_true", help="Verbose debug logging")
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if not any([args.list, args.resolve, args.search, args.photo]):
        parser.print_help()
        sys.exit(0)

    if args.list:
        cmd_list()
    elif args.resolve:
        cmd_resolve(write=args.write)
    elif args.search:
        cmd_search(args.search)
    elif args.photo:
        cmd_photo(args.photo)


if __name__ == "__main__":
    main()
