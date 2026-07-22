#!/usr/bin/env python3
"""
backfill_pexels.py — Populate missing thumbnails in published Hugo posts using Pexels.

Usage:
    python backfill_pexels.py                # dry-run (preview only)
    python backfill_pexels.py --write        # actually update files

For each post in hugo-site/content/posts/ whose thumbnail: front-matter field is
empty or absent, this script:
  1. Extracts the title and categories from the front-matter.
  2. Searches Pexels for a relevant copyright-free landscape photo.
  3. Rewrites the thumbnail: line in the file.

Pexels License: https://www.pexels.com/license/
  - Free for commercial and personal use. No attribution required.
  - Photos are real photographs by human creators (not AI-generated).

Requirements:
    pip install httpx python-dotenv
    PEXELS_API_KEY must be set in your .env or environment.
"""

import argparse
import logging
import os
import random
import re
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
POSTS_DIR = Path(__file__).parent / "hugo-site" / "content" / "posts"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Keyword map — same as pipeline.py
PEXELS_KEYWORD_MAP: list[tuple[list[str], list[str]]] = [
    (["ransomware", "ransom"], [
        "chains broken industrial abstract",
        "red alert warning lights abstract",
        "factory shutdown industrial abandoned",
        "wildfire forest destruction aerial",
    ]),
    (["phishing", "spear-phishing"], [
        "fishing boat ocean water aerial",
        "bait hook fishing nature",
        "impersonation theater mask stage",
        "trust handshake business meeting",
    ]),
    (["vulnerability", "cve", "patch", "zero-day", "zero day"], [
        "cracked wall concrete texture abstract",
        "bridge inspection engineer architecture",
        "magnifying glass inspection detail",
        "x-ray medical scan abstract",
    ]),
    (["llm", "large language model", "gpt", "chatgpt", "ai model"], [
        "library books knowledge rows",
        "text typography abstract letters",
        "conversation speech bubbles abstract",
        "neural pattern abstract network light",
    ]),
    (["prompt injection", "jailbreak"], [
        "maze labyrinth escape abstract",
        "puzzle pieces misfit concept",
        "broken fence gap abstract light",
        "code terminal text abstract",
    ]),
    (["supply chain", "third-party", "dependency"], [
        "cargo ship port aerial logistics",
        "assembly line factory industrial",
        "domino effect sequence abstract",
        "jigsaw puzzle pieces fitting",
    ]),
    (["malware", "trojan", "backdoor", "rootkit"], [
        "microscope biology cell abstract",
        "parasite nature close-up macro",
        "hidden passage secret door architecture",
        "contamination hazmat warning abstract",
    ]),
    (["data breach", "data leak", "exposed data", "leaked"], [
        "water leak pipe burst abstract",
        "open vault empty bank abstract",
        "envelope letter open abstract",
        "sieve colander kitchen abstract",
    ]),
    (["nation state", "apt", "state-sponsored", "espionage"], [
        "government building architecture capitol",
        "globe world map aerial abstract",
        "chess strategy game concept",
        "embassy flag architecture diplomatic",
    ]),
    (["deepfake", "synthetic media", "disinformation"], [
        "mirror reflection distorted abstract",
        "mask theater disguise concept",
        "doppelganger shadow silhouette",
        "wax sculpture face art",
    ]),
    (["critical infrastructure", "power grid", "scada", "ics"], [
        "power plant aerial industrial",
        "pipeline oil gas industrial landscape",
        "dam water infrastructure aerial",
        "wind turbine farm landscape",
    ]),
    (["cloud", "aws", "azure", "gcp", "misconfiguration"], [
        "data center aerial architecture",
        "sky clouds aerial sunlight",
        "warehouse storage containers aerial",
        "server rack abstract blue light",
    ]),
    (["social engineering", "impersonation", "pretexting"], [
        "shadow silhouette following urban",
        "theater stage performance acting",
        "mask disguise costume carnival",
        "puppet strings control abstract",
    ]),
    (["encryption", "cryptography", "key", "cipher"], [
        "key collection vintage macro",
        "envelope wax seal letter",
        "safe vault combination lock",
        "ancient code hieroglyphics abstract",
    ]),
    (["api", "authentication", "oauth", "jwt", "credential"], [
        "electrical plug socket connection abstract",
        "fingerprint biometric close-up",
        "identity card badge close-up",
        "train tracks junction intersection",
    ]),
    (["botnet", "ddos", "distributed"], [
        "traffic jam highway aerial",
        "crowd rush stampede abstract",
        "flood wave overwhelming abstract",
        "flock birds murmuration aerial",
    ]),
    (["insider threat", "insider"], [
        "empty office corridor perspective",
        "shadow person silhouette window",
        "surveillance mirror office abstract",
        "confidential folder desk abstract",
    ]),
    (["mobile", "android", "ios", "smartphone"], [
        "smartphone screen glow abstract",
        "hand holding device close-up",
        "mobile app interface modern",
        "wireless signal tower landscape",
    ]),
    (["iot", "embedded", "firmware", "hardware"], [
        "circuit board macro electronics",
        "smart home interior modern",
        "antenna radio tower landscape",
        "electronic components soldering macro",
    ]),
    (["regulation", "compliance", "gdpr", "nist", "framework"], [
        "courthouse architecture columns",
        "contract document signing abstract",
        "scales justice balance architecture",
        "blueprint technical drawing engineering",
    ]),
]


# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("backfill")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _pexels_query(title: str, categories: list) -> str:
    """Build the best Pexels search query for this article."""
    text = title.lower()
    for keywords, queries in PEXELS_KEYWORD_MAP:
        if any(kw in text for kw in keywords):
            return random.choice(queries)
    if categories:
        cat = categories[0].replace("-", " ")
        return f"{cat} cybersecurity technology"
    return "cybersecurity technology dark computer"


def fetch_pexels_image(title: str, categories: list, used_urls: set | None = None) -> str:
    """Return a Pexels landscape photo URL or '' on failure.

    used_urls: already-assigned thumbnails — candidates in this set are skipped
               to avoid showing the same image twice across the feed.
    """
    if not PEXELS_API_KEY:
        log.warning("PEXELS_API_KEY not set — skipping")
        return ""

    if used_urls is None:
        used_urls = set()

    query = _pexels_query(title, categories)
    log.debug(f"  Pexels query: '{query}'")

    try:
        resp = httpx.get(
            "https://api.pexels.com/v1/search",
            params={"query": query, "per_page": 15, "orientation": "landscape"},
            headers={"Authorization": PEXELS_API_KEY},
            timeout=8.0,
        )
        resp.raise_for_status()
        photos = resp.json().get("photos", [])
        if not photos:
            log.debug(f"  Pexels: no results for '{query}'")
            return ""
        # Walk from deterministic start position, skip already-used images
        start = abs(hash(title)) % len(photos)
        for i in range(len(photos)):
            candidate = photos[(start + i) % len(photos)]["src"]["large"]
            if candidate not in used_urls:
                return candidate
        # All candidates used — fall back to deterministic pick
        return photos[start]["src"]["large"]
    except Exception as e:
        log.debug(f"  Pexels fetch failed: {e}")
        return ""


def parse_frontmatter(text: str) -> dict:
    """Extract simple key: value pairs from YAML front-matter (between --- markers)."""
    fm: dict = {}
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return fm
    for line in match.group(1).splitlines():
        kv = re.match(r'^(\w+):\s*(.*)', line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    # Parse categories list (YAML sequence)
    cats_match = re.search(r'^categories:\s*\[(.*?)\]', match.group(1), re.MULTILINE)
    if cats_match:
        raw = cats_match.group(1)
        fm["categories_list"] = [c.strip().strip('"').strip("'") for c in raw.split(",") if c.strip()]
    else:
        # Multi-line list
        cats_block = re.search(r'^categories:\n((?:  - .+\n?)+)', match.group(1), re.MULTILINE)
        if cats_block:
            fm["categories_list"] = [
                re.sub(r'^\s*- ', '', l).strip().strip('"').strip("'")
                for l in cats_block.group(1).splitlines()
                if l.strip()
            ]
        else:
            fm["categories_list"] = []
    return fm


def needs_thumbnail(text: str) -> bool:
    """Return True if the thumbnail front-matter field is empty or missing."""
    match = re.search(r'^thumbnail:\s*(.*)$', text, re.MULTILINE)
    if not match:
        return True
    val = match.group(1).strip().strip('"').strip("'")
    return val == ""


def set_thumbnail(text: str, url: str) -> str:
    """Replace or insert the thumbnail: field in front-matter."""
    replacement = f'thumbnail: "{url}"'
    if re.search(r'^thumbnail:', text, re.MULTILINE):
        return re.sub(r'^thumbnail:.*$', replacement, text, flags=re.MULTILINE)
    # Insert after 'source:' or 'summary:' line, or just before closing ---
    for anchor in (r'(^source:.*$)', r'(^summary:.*$)'):
        m = re.search(anchor, text, re.MULTILINE)
        if m:
            pos = m.end()
            return text[:pos] + "\n" + replacement + text[pos:]
    # Fallback: insert before closing ---
    return re.sub(r'(\n---\n)', f'\n{replacement}\\1', text, count=1)


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill Pexels thumbnails for Hugo posts")
    parser.add_argument("--write", action="store_true", help="Actually update files (default: dry-run)")
    parser.add_argument("--force", action="store_true", help="Replace existing thumbnails too (not just empty ones)")
    parser.add_argument("--limit", type=int, default=0, help="Only process N posts (0 = all)")
    parser.add_argument("--debug", action="store_true", help="Verbose debug logging")
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if not PEXELS_API_KEY:
        log.error("PEXELS_API_KEY is not set. Add it to your .env file and retry.")
        sys.exit(1)

    if not POSTS_DIR.exists():
        log.error(f"Posts directory not found: {POSTS_DIR}")
        sys.exit(1)

    mode = "WRITE" if args.write else "DRY RUN"
    log.info(f"=== Pexels Backfill  [{mode}] ===")
    log.info(f"Posts dir : {POSTS_DIR}")

    posts = sorted(POSTS_DIR.glob("*.md"))
    log.info(f"Posts found: {len(posts)}")

    if args.limit:
        posts = posts[:args.limit]
        log.info(f"Limited to first {args.limit} posts")

    updated = skipped = errors = 0

    # Seed used_urls with thumbnails that already exist in posts being skipped,
    # so backfilled images don't duplicate images already on the site.
    used_urls: set = set()
    for path in posts:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'^thumbnail:\s*"?([^"\n]+)"?', text, re.MULTILINE)
            if m:
                url = m.group(1).strip()
                if url:
                    used_urls.add(url)
        except Exception:
            pass
    log.info(f"Existing thumbnails (dedup pool): {len(used_urls)}")

    for path in posts:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            log.warning(f"  Cannot read {path.name}: {e}")
            errors += 1
            continue

        if not needs_thumbnail(text) and not args.force:
            log.debug(f"  SKIP (has thumbnail): {path.name}")
            skipped += 1
            continue

        fm = parse_frontmatter(text)
        title = fm.get("title", path.stem)
        categories = fm.get("categories_list", [])

        log.info(f"  {path.name}")
        log.info(f"    title: {title[:70]}")

        url = fetch_pexels_image(title, categories, used_urls=used_urls)
        if not url:
            log.warning(f"    No image found — leaving blank")
            skipped += 1
            continue

        log.info(f"    image: {url[:80]}")
        used_urls.add(url)   # prevent this image being picked again this run

        if args.write:
            new_text = set_thumbnail(text, url)
            path.write_text(new_text, encoding="utf-8")
            log.info(f"    ✓ written")
        else:
            log.info(f"    (dry-run — not written)")

        updated += 1

    log.info(f"\n=== Done ===")
    log.info(f"  Updated : {updated}")
    log.info(f"  Skipped : {skipped}  (already had thumbnail or no result)")
    log.info(f"  Errors  : {errors}")
    if not args.write and updated > 0:
        log.info(f"\nRun with --write to apply changes.")


if __name__ == "__main__":
    main()
