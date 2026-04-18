#!/usr/bin/env python3
"""
podcast_feed.py — Grid the Grey Podcast RSS Feed Generator
===========================================================
Reads briefings/episodes.json and generates a valid iTunes-compatible
podcast RSS feed (feed.xml), then uploads it to Cloudflare R2.

USAGE
-----
    python podcast_feed.py --update         # Regenerate feed.xml and upload to R2
    python podcast_feed.py --list           # List episodes in the feed
    python podcast_feed.py --show           # Print current show metadata

WORKFLOW
--------
Run this every time a new episode is produced:

    python weekly_briefing.py --produce     # generates MP3, updates episodes.json
    python podcast_feed.py --update         # regenerates feed.xml on R2

FEED URL
--------
    {R2_PUBLIC_URL}/feed.xml

Submit this URL to Spotify for Podcasters:
    https://podcasters.spotify.com/

PODCAST ARTWORK
---------------
Spotify requires a square image: 1400×1400 to 3000×3000 px, JPEG or PNG.
Upload it to R2 as 'podcast-artwork.jpg' and set image_url in episodes.json.
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
BRIEFINGS_DIR   = Path(__file__).parent / "briefings"
EPISODES_JSON   = BRIEFINGS_DIR / "episodes.json"
R2_ACCOUNT_ID        = os.getenv("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY_ID     = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET_NAME       = os.getenv("R2_BUCKET_NAME", "")
R2_PUBLIC_URL        = os.getenv("R2_PUBLIC_URL", "").rstrip("/")

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("podcast_feed")


# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_duration(secs: int) -> str:
    """Format seconds as MM:SS (or HH:MM:SS for >1hr)."""
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def fmt_pubdate(iso: str) -> str:
    """Convert ISO 8601 date to RFC 2822 (required by podcast RSS)."""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return format_datetime(dt)
    except Exception:
        return format_datetime(datetime.now(timezone.utc))


def load_episodes() -> dict:
    if not EPISODES_JSON.exists():
        log.error(f"episodes.json not found at {EPISODES_JSON}")
        log.error("Run: python weekly_briefing.py --produce  first.")
        sys.exit(1)
    return json.loads(EPISODES_JSON.read_text(encoding="utf-8"))


# ── RSS XML generator ─────────────────────────────────────────────────────────
def build_feed_xml(data: dict) -> str:
    """Generate a valid iTunes podcast RSS feed from episodes.json data."""
    show    = data.get("show", {})
    episodes = data.get("episodes", [])

    title       = escape(show.get("title", "Grid the Grey Weekly Security Briefing"))
    description = escape(show.get("description", ""))
    link        = escape(show.get("link", ""))
    image_url   = escape(show.get("image_url", ""))
    author      = escape(show.get("author", "Grid the Grey"))
    email       = escape(show.get("email", ""))
    language    = show.get("language", "en")
    category    = show.get("category", "Technology")
    feed_url    = f"{R2_PUBLIC_URL}/feed.xml"
    build_date  = format_datetime(datetime.now(timezone.utc))

    items = []
    for ep in episodes:
        ep_title    = escape(ep.get("title", ""))
        ep_desc     = escape(ep.get("description", ""))
        ep_url      = ep.get("r2_url", "")
        ep_size     = ep.get("size_bytes", 0)
        ep_duration = fmt_duration(ep.get("duration_secs", 300))
        ep_pubdate  = fmt_pubdate(ep.get("pub_date", ""))
        ep_num      = ep.get("episode_num", 1)
        ep_guid     = ep_url  # URL is stable and unique — fine as GUID

        items.append(f"""
    <item>
      <title>{ep_title}</title>
      <description>{ep_desc}</description>
      <pubDate>{ep_pubdate}</pubDate>
      <enclosure url="{ep_url}" length="{ep_size}" type="audio/mpeg"/>
      <guid isPermaLink="false">{ep_guid}</guid>
      <itunes:title>{ep_title}</itunes:title>
      <itunes:duration>{ep_duration}</itunes:duration>
      <itunes:episode>{ep_num}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    items_xml = "\n".join(items)

    # Artwork block — only include if image_url is set
    artwork_xml = f'<itunes:image href="{image_url}"/>' if image_url else ""

    # Owner block — only include if email is set
    owner_xml = ""
    if email:
        owner_xml = f"""<itunes:owner>
      <itunes:name>{author}</itunes:name>
      <itunes:email>{email}</itunes:email>
    </itunes:owner>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:atom="http://www.w3.org/2005/Atom">

  <channel>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    <language>{language}</language>
    <lastBuildDate>{build_date}</lastBuildDate>
    <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>

    <itunes:author>{author}</itunes:author>
    <itunes:summary>{description}</itunes:summary>
    <itunes:category text="{category}"/>
    {artwork_xml}
    {owner_xml}
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>episodic</itunes:type>
{items_xml}

  </channel>
</rss>
"""


# ── R2 upload ─────────────────────────────────────────────────────────────────
def upload_feed(xml: str) -> str:
    """Upload feed.xml to R2 and return its public URL."""
    try:
        import boto3
    except ImportError:
        log.error("boto3 not installed. Run: pip install boto3")
        sys.exit(1)

    missing = [v for v in ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY",
                            "R2_BUCKET_NAME", "R2_PUBLIC_URL"] if not os.getenv(v)]
    if missing:
        log.error(f"Missing R2 env vars: {', '.join(missing)}")
        sys.exit(1)

    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )

    s3.put_object(
        Bucket=R2_BUCKET_NAME,
        Key="feed.xml",
        Body=xml.encode("utf-8"),
        ContentType="application/rss+xml; charset=utf-8",
        CacheControl="public, max-age=3600",   # feed refreshes hourly
    )

    url = f"{R2_PUBLIC_URL}/feed.xml"
    log.info(f"  ✓ Feed uploaded: {url}")
    return url


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_update() -> None:
    """Regenerate feed.xml from episodes.json and upload to R2."""
    log.info("=== Update Podcast Feed ===")
    data = load_episodes()
    ep_count = len(data.get("episodes", []))
    log.info(f"  Episodes in feed: {ep_count}")

    if ep_count == 0:
        log.warning("  No episodes yet — feed will be valid but empty.")
        log.warning("  Run: python weekly_briefing.py --produce  to add an episode.")

    xml = build_feed_xml(data)

    # Save a local copy for inspection
    local_path = BRIEFINGS_DIR / "feed.xml"
    local_path.write_text(xml, encoding="utf-8")
    log.info(f"  Local copy saved: {local_path}")

    feed_url = upload_feed(xml)

    print()
    print("=" * 60)
    print(f"  ✓ Podcast feed updated")
    print(f"  Episodes : {ep_count}")
    print(f"  Feed URL : {feed_url}")
    print()
    print("  Submit feed to Spotify for Podcasters:")
    print("  → https://podcasters.spotify.com/")
    print("    (one-time step — Spotify polls the feed automatically after that)")
    print("=" * 60)


def cmd_list() -> None:
    """Print all episodes in the feed."""
    data = load_episodes()
    episodes = data.get("episodes", [])

    if not episodes:
        log.info("No episodes yet.")
        return

    print(f"\nEpisodes ({len(episodes)}):\n")
    for ep in episodes:
        dur = fmt_duration(ep.get("duration_secs", 0))
        size_mb = ep.get("size_bytes", 0) / (1024 * 1024)
        pub = ep.get("pub_date", "")[:10]
        print(f"  #{ep['episode_num']:02d}  {ep['title']}")
        print(f"       {pub}  |  {dur}  |  {size_mb:.1f} MB  |  voice: {ep.get('voice','?')}")
        print(f"       {ep.get('r2_url','')}")
        print()


def cmd_show() -> None:
    """Print current show metadata."""
    data = load_episodes()
    show = data.get("show", {})
    print("\nShow metadata (briefings/episodes.json → show):\n")
    for k, v in show.items():
        print(f"  {k:15s}: {v}")
    print()
    print("Edit briefings/episodes.json to update show details,")
    print("then run: python podcast_feed.py --update")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Grid the Grey — Podcast RSS feed generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python podcast_feed.py --update     # regenerate feed.xml and upload to R2
  python podcast_feed.py --list       # list episodes
  python podcast_feed.py --show       # show metadata
        """,
    )
    parser.add_argument("--update", action="store_true", help="Regenerate feed.xml and upload to R2")
    parser.add_argument("--list",   action="store_true", help="List episodes in the feed")
    parser.add_argument("--show",   action="store_true", help="Print show metadata")
    parser.add_argument("--debug",  action="store_true", help="Verbose debug logging")
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if not any([args.update, args.list, args.show]):
        parser.print_help()
        sys.exit(0)

    if args.update:
        cmd_update()
    elif args.list:
        cmd_list()
    elif args.show:
        cmd_show()


if __name__ == "__main__":
    main()
