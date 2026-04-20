#!/usr/bin/env python3
"""
weekly_briefing.py — Grid the Grey Weekly Security Briefing
============================================================
Generates a CISO-level audio podcast episode from the week's published articles.

WORKFLOW
--------
Step 1 — Generate script draft:
    python weekly_briefing.py --generate

    Reads published posts from the last 7 days, calls Claude to write a
    ~600-word spoken-word briefing script, and saves it to:
        briefings/draft-YYYY-WXX.md

Step 2 — Review & edit the draft:
    Open briefings/draft-YYYY-WXX.md in any editor.
    Edit the script until you're happy with it.

Step 3 — Produce audio + upload:
    python weekly_briefing.py --produce
    python weekly_briefing.py --produce --voice nova   # try a different voice

    Converts the latest draft to MP3 via OpenAI TTS, saves it locally,
    uploads it to Cloudflare R2, and prints the public URL.

OTHER COMMANDS
--------------
    python weekly_briefing.py --list            # List available drafts
    python weekly_briefing.py --voices          # Show available TTS voices
    python weekly_briefing.py --generate --days 14  # Use last 14 days of posts

VOICES (OpenAI TTS)
-------------------
    onyx    — Deep, authoritative male. Best for news-anchor tone.  [DEFAULT]
    echo    — Clean, formal male. Good for technical briefings.
    nova    — Warm, professional female. Approachable analyst tone.
    alloy   — Neutral, balanced. Works for either gender preference.
    fable   — Expressive, storytelling style.
    shimmer — Bright, energetic female.

REQUIREMENTS
------------
    pip install openai boto3
    .env must contain: OPENAI_API_KEY, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID,
                       R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, R2_PUBLIC_URL
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
POSTS_DIR       = Path(__file__).parent / "hugo-site" / "content" / "posts"
BRIEFINGS_DIR   = Path(__file__).parent / "briefings"
PODCAST_NAME    = "CISO AI Security Briefing"
DEFAULT_DAYS    = 7
DEFAULT_VOICE   = "onyx"
TARGET_WORDS    = 450          # ~3.5 minutes at speaking pace; keeps chars well under TTS 4096 limit
MAX_TTS_CHARS   = 4000         # OpenAI TTS limit is 4096; leave headroom
MAX_ARTICLES    = 10           # Cap articles fed to Claude

ANTHROPIC_API_KEY   = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL        = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY", "")
R2_ACCOUNT_ID       = os.getenv("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY_ID    = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET_NAME      = os.getenv("R2_BUCKET_NAME", "")
R2_PUBLIC_URL       = os.getenv("R2_PUBLIC_URL", "").rstrip("/")

VOICES = {
    "onyx":    "Deep, authoritative male — news-anchor tone [DEFAULT]",
    "echo":    "Clean, formal male — technical briefing style",
    "nova":    "Warm, professional female — approachable analyst tone",
    "alloy":   "Neutral, balanced — works for either preference",
    "fable":   "Expressive, storytelling style",
    "shimmer": "Bright, energetic female",
}

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("briefing")


# ── Front-matter parser ───────────────────────────────────────────────────────
def _fm_value(text: str, key: str) -> str:
    """Extract a scalar front-matter value by key."""
    m = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _fm_list(text: str, key: str) -> list:
    """Extract an inline YAML list front-matter value, e.g. ["a", "b"]."""
    m = re.search(rf'^{key}:\s*\[([^\]]*)\]', text, re.MULTILINE)
    if not m:
        return []
    raw = m.group(1)
    return [v.strip().strip('"').strip("'") for v in raw.split(",") if v.strip()]


def parse_post(path: Path) -> dict | None:
    """
    Parse a Hugo markdown post and return a dict of key fields.
    Returns None if the post is a draft or cannot be parsed.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    draft = _fm_value(text, "draft")
    if draft.lower() == "true":
        return None

    date_str = _fm_value(text, "date")
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return None

    score_str = _fm_value(text, "relevance_score")
    try:
        score = float(score_str)
    except Exception:
        score = 0.0

    # Extract body (everything after closing front-matter ---)
    body_match = re.search(r'^---\n.*?\n---\n(.*)', text, re.DOTALL)
    body = body_match.group(1).strip()[:800] if body_match else ""

    return {
        "title":            _fm_value(text, "title"),
        "summary":          _fm_value(text, "summary"),
        "source":           _fm_value(text, "source"),
        "source_url":       _fm_value(text, "source_url"),
        "threat_level":     _fm_value(text, "threat_level"),
        "relevance_score":  score,
        "categories":       _fm_list(text, "categories"),
        "mitre_techniques": _fm_list(text, "mitre_techniques"),
        "owasp_categories": _fm_list(text, "owasp_categories"),
        "date":             date,
        "body_excerpt":     body,
    }


# ── Article reader ────────────────────────────────────────────────────────────
def get_week_articles(days: int = DEFAULT_DAYS) -> list:
    """
    Return published posts from the last N days, sorted by relevance_score desc.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    articles = []

    for path in POSTS_DIR.glob("*.md"):
        post = parse_post(path)
        if post and post["date"] >= cutoff and post["title"]:
            articles.append(post)

    articles.sort(key=lambda a: a["relevance_score"], reverse=True)
    return articles[:MAX_ARTICLES]


# ── Script generation (Claude) ────────────────────────────────────────────────
def build_article_context(articles: list) -> str:
    """Format article list as context for the Claude prompt."""
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(f"ARTICLE {i}")
        lines.append(f"Title: {a['title']}")
        lines.append(f"Source: {a['source']}")
        lines.append(f"Threat Level: {a['threat_level']}  |  Relevance: {a['relevance_score']:.1f}/10")
        if a["categories"]:
            lines.append(f"Categories: {', '.join(a['categories'][:3])}")
        if a["mitre_techniques"]:
            lines.append(f"MITRE ATLAS: {', '.join(a['mitre_techniques'][:2])}")
        if a["owasp_categories"]:
            lines.append(f"OWASP LLM: {', '.join(a['owasp_categories'][:2])}")
        lines.append(f"Summary: {a['summary'][:400]}")
        lines.append("")
    return "\n".join(lines)


def generate_script(articles: list, week_label: str) -> str:
    """
    Call Claude to generate a CISO-level spoken-word briefing script.
    Returns the raw script text.
    """
    context = build_article_context(articles)
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    prompt = f"""You are the host and writer of "{PODCAST_NAME}", a weekly audio briefing for Chief Information Security Officers and senior security leaders.

Today's date: {now_str}
Week: {week_label}

This week's articles (ordered by relevance):
{context}

Write a professional spoken-word script for this week's episode. Requirements:

MANDATORY OPENING LINE — the script MUST begin with exactly:
"This week's Grid-the-Grey CISO AI Security Brief —"
Then continue directly with the week's overarching threat theme (no further preamble).

STRUCTURE (in order):
1. Opening (mandatory line above + 1–2 sentences): The week's overarching threat theme, stated crisply.
2. Top stories (bulk of the episode): Cover the 3–5 most significant stories. For each, explain: what happened, why it matters strategically to a CISO, and any MITRE ATLAS or OWASP LLM framing where relevant. Weave them together — don't treat each as an isolated item.
3. Threat landscape synthesis (2–3 sentences): Step back and identify the pattern — what does this week tell us about the direction of AI-enabled threats?
4. CISO action points (2–3 sentences): Concrete, specific actions a CISO should take or consider this week. Not generic advice — grounded in this week's stories.

STYLE RULES:
- STRICT LIMIT: {TARGET_WORDS} words maximum. Stay under this — the audio service cuts off beyond ~3,500 characters.
- Written to be SPOKEN ALOUD — short sentences, natural rhythm, no jargon dumps
- Tone: authoritative senior analyst briefing a board. Confident, precise, no filler phrases
- No bullet points, no headers, no markdown formatting
- No stage directions, no [PAUSE], no speaker notes
- Do not sign off or say goodbye — end with the last action point
- Do not write "In conclusion" or "To summarise"

Output ONLY the spoken script. Nothing else."""

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    log.info("  Calling Claude to generate briefing script...")

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    script = response.content[0].text.strip()
    log.info(f"  Script generated: {len(script.split())} words / {len(script)} chars")
    return script


# ── Draft file management ─────────────────────────────────────────────────────
def week_label() -> str:
    """Return ISO week label like '2026-W16'."""
    now = datetime.now(timezone.utc)
    return f"{now.year}-W{now.isocalendar()[1]:02d}"


def draft_path(label: str) -> Path:
    return BRIEFINGS_DIR / f"draft-{label}.md"


def save_draft(script: str, label: str, articles: list) -> Path:
    """Save the Claude-generated script as a draft markdown file."""
    BRIEFINGS_DIR.mkdir(exist_ok=True)
    path = draft_path(label)

    word_count = len(script.split())
    char_count = len(script)
    now = datetime.now(timezone.utc).isoformat()

    front = f"""---
week: "{label}"
generated_at: "{now}"
articles_used: {len(articles)}
word_count: {word_count}
char_count: {char_count}
estimated_duration_mins: {word_count / 120:.1f}
---

"""
    path.write_text(front + script + "\n", encoding="utf-8")
    log.info(f"  Draft saved: {path}")
    return path


def load_draft(path: Path) -> str:
    """Read a draft file and return only the script text (strip front-matter)."""
    text = path.read_text(encoding="utf-8")
    # Strip YAML front-matter block
    m = re.match(r'^---\n.*?\n---\n(.*)', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def latest_draft() -> Path | None:
    """Return the latest draft file by filename (YYYY-WXX sorts correctly).
    Filename-based sort is reliable in GitHub Actions where all checked-out
    files share the same mtime."""
    BRIEFINGS_DIR.mkdir(exist_ok=True)
    drafts = sorted(BRIEFINGS_DIR.glob("draft-*.md"), key=lambda p: p.name, reverse=True)
    return drafts[0] if drafts else None


# ── OpenAI TTS ────────────────────────────────────────────────────────────────
def text_to_speech(script: str, voice: str, output_path: Path) -> bytes:
    """
    Convert script to MP3 via OpenAI TTS.
    Returns audio bytes and saves to output_path.
    """
    try:
        from openai import OpenAI
    except ImportError:
        log.error("openai package not installed. Run: pip install openai")
        sys.exit(1)

    if len(script) > MAX_TTS_CHARS:
        log.warning(f"  Script is {len(script)} chars — truncating to {MAX_TTS_CHARS} (OpenAI TTS limit)")
        # Truncate at last sentence boundary before the limit
        truncated = script[:MAX_TTS_CHARS]
        last_period = truncated.rfind(". ")
        if last_period > MAX_TTS_CHARS * 0.8:
            script = truncated[:last_period + 1]
        else:
            script = truncated

    client = OpenAI(api_key=OPENAI_API_KEY)
    log.info(f"  Generating audio via OpenAI TTS  (model: tts-1-hd, voice: {voice})")
    log.info(f"  Input: {len(script.split())} words / {len(script)} chars")

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=script,
        response_format="mp3",
    )

    audio_bytes = response.content
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_bytes(audio_bytes)
    size_kb = len(audio_bytes) / 1024
    log.info(f"  Audio saved locally: {output_path}  ({size_kb:.0f} KB)")
    return audio_bytes


# ── Cloudflare R2 upload ──────────────────────────────────────────────────────
def upload_to_r2(audio_bytes: bytes, filename: str) -> str:
    """
    Upload MP3 to Cloudflare R2 and return the public URL.
    Uses the S3-compatible API.
    """
    try:
        import boto3
        from botocore.exceptions import ClientError
    except ImportError:
        log.error("boto3 not installed. Run: pip install boto3")
        sys.exit(1)

    missing = [v for v in ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY",
                            "R2_BUCKET_NAME", "R2_PUBLIC_URL"] if not os.getenv(v)]
    if missing:
        log.error(f"Missing R2 env vars: {', '.join(missing)}")
        sys.exit(1)

    endpoint = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    log.info(f"  Uploading to Cloudflare R2: {R2_BUCKET_NAME}/{filename}")

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )

    s3.put_object(
        Bucket=R2_BUCKET_NAME,
        Key=filename,
        Body=audio_bytes,
        ContentType="audio/mpeg",
        CacheControl="public, max-age=31536000",
    )

    public_url = f"{R2_PUBLIC_URL}/{filename}"
    log.info(f"  ✓ Uploaded: {public_url}")
    return public_url


# ── Episode metadata ──────────────────────────────────────────────────────────
EPISODES_JSON   = BRIEFINGS_DIR / "episodes.json"
HUGO_TOML_PATH  = Path(__file__).parent / "hugo-site" / "hugo.toml"

SHOW_DEFAULTS = {
    "title":       PODCAST_NAME,
    "description": (
        "Weekly AI security intelligence briefings for CISO-level audiences. "
        "Every episode covers the week's most significant threats — framework-mapped "
        "to MITRE ATLAS and OWASP LLM Top 10 — and closes with concrete actions "
        "for security leaders."
    ),
    "link":        "",   # populated from hugo.toml baseURL at save time
    "image_url":   "",   # set to R2_PUBLIC_URL/podcast-artwork.jpg when artwork is uploaded
    "author":      "Grid the Grey",
    "email":       "bansalachin@gmail.com",
    "language":    "en",
    "category":    "Technology",
}


def load_episodes() -> dict:
    """Load episodes.json or return a fresh structure."""
    if EPISODES_JSON.exists():
        return json.loads(EPISODES_JSON.read_text(encoding="utf-8"))
    return {"show": SHOW_DEFAULTS.copy(), "episodes": []}


def save_episodes(data: dict) -> None:
    BRIEFINGS_DIR.mkdir(exist_ok=True)
    EPISODES_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def next_episode_num(data: dict) -> int:
    if not data["episodes"]:
        return 1
    return max(e["episode_num"] for e in data["episodes"]) + 1


def save_episode_metadata(
    audio_bytes: bytes,
    script: str,
    label: str,
    voice: str,
    public_url: str,
) -> None:
    """Append this episode to briefings/episodes.json."""
    data = load_episodes()

    # Populate show link from hugo.toml if not set
    if not data["show"].get("link") and HUGO_TOML_PATH.exists():
        toml_text = HUGO_TOML_PATH.read_text(encoding="utf-8")
        m = re.search(r'^baseURL\s*=\s*"([^"]+)"', toml_text, re.MULTILINE)
        if m:
            data["show"]["link"] = m.group(1).rstrip("/") + "/"

    # Populate show image URL from R2 if not set
    if not data["show"].get("image_url") and R2_PUBLIC_URL:
        data["show"]["image_url"] = f"{R2_PUBLIC_URL}/podcast-artwork.jpg"

    word_count  = len(script.split())
    duration_s  = int(word_count / 120 * 60)   # ~120 words/min speaking pace
    size_bytes  = len(audio_bytes)

    # Parse year+week from label e.g. "2026-W17"
    m = re.match(r'(\d{4})-W(\d+)', label)
    if m:
        year, week = int(m.group(1)), int(m.group(2))
        episode_title = f"Week {week}, {year} — AI Security Briefing"
    else:
        episode_title = f"{label} — AI Security Briefing"

    # Extract first sentence of script as short description
    first_sentence = script.split(".")[0].strip() + "."

    episode = {
        "episode_num":   next_episode_num(data),
        "week":          label,
        "title":         episode_title,
        "description":   first_sentence,
        "r2_url":        public_url,
        "pub_date":      datetime.now(timezone.utc).isoformat(),
        "duration_secs": duration_s,
        "size_bytes":    size_bytes,
        "voice":         voice,
    }

    data["episodes"].insert(0, episode)   # newest first
    save_episodes(data)
    log.info(f"  Episode #{episode['episode_num']} saved to {EPISODES_JSON.name}")


def update_hugo_params(episode_url: str, episode_title: str) -> None:
    """Update hugo.toml with the latest episode URL and title."""
    if not HUGO_TOML_PATH.exists():
        log.warning("  hugo.toml not found — skipping param update")
        return

    text = HUGO_TOML_PATH.read_text(encoding="utf-8")

    def replace_param(content: str, key: str, value: str, is_bool: bool = False) -> str:
        """Replace an existing indented param inside [params] block."""
        # Match the key with optional leading whitespace (params are indented in [params])
        pattern = rf'^(\s*){re.escape(key)}\s*=.*$'
        if is_bool:
            repl = rf'\g<1>{key} = {value}'
        else:
            repl = rf'\g<1>{key} = "{value}"'
        new_content, n = re.subn(pattern, repl, content, flags=re.MULTILINE)
        if n == 0:
            log.warning(f"  hugo.toml: param '{key}' not found — skipping update")
        return new_content

    text = replace_param(text, "latestEpisodeUrl",    episode_url)
    text = replace_param(text, "latestEpisodeTitle",  episode_title)
    text = replace_param(text, "enablePodcastPlayer", "true", is_bool=True)

    HUGO_TOML_PATH.write_text(text, encoding="utf-8")
    log.info("  hugo.toml updated with latest episode")


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_generate(days: int) -> None:
    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY not set in .env")
        sys.exit(1)

    log.info(f"=== Generate Briefing Script  (last {days} days) ===")
    articles = get_week_articles(days)

    if not articles:
        log.error(f"No published articles found in the last {days} days.")
        sys.exit(1)

    log.info(f"  Articles found: {len(articles)}")
    for a in articles:
        log.info(f"    [{a['threat_level']:6s}] {a['title'][:65]}")

    label = week_label()
    script = generate_script(articles, label)
    path = save_draft(script, label, articles)

    word_count = len(script.split())
    print()
    print("=" * 60)
    print(f"  Draft saved: {path.name}")
    print(f"  Words: {word_count}  (~{word_count/120:.1f} min at speaking pace)")
    print()
    print("  Next steps:")
    print(f"  1. Open and review: {path}")
    print(f"  2. Edit the script as needed")
    print(f"  3. Run: python weekly_briefing.py --produce")
    print("=" * 60)


def cmd_produce(draft_file: str | None, voice: str) -> None:
    if not OPENAI_API_KEY:
        log.error("OPENAI_API_KEY not set in .env")
        sys.exit(1)

    # Resolve draft path
    if draft_file:
        path = Path(draft_file)
    else:
        path = latest_draft()
        if not path:
            log.error("No draft found in briefings/. Run --generate first.")
            sys.exit(1)
        log.info(f"  Using latest draft: {path.name}")

    if not path.exists():
        log.error(f"Draft not found: {path}")
        sys.exit(1)

    script = load_draft(path)
    word_count = len(script.split())
    char_count = len(script)

    log.info(f"=== Produce Audio Episode ===")
    log.info(f"  Draft    : {path.name}")
    log.info(f"  Words    : {word_count}  (~{word_count/120:.1f} min)")
    log.info(f"  Chars    : {char_count}")
    log.info(f"  Voice    : {voice}  — {VOICES.get(voice, 'custom')}")
    log.info(f"  Estimate : OpenAI TTS cost ~${word_count * 0.000015:.4f}")
    print()

    # In CI / GitHub Actions there is no TTY — auto-confirm.
    import sys
    if sys.stdin.isatty():
        confirm = input("  Proceed? [y/N] ").strip().lower()
        if confirm != "y":
            log.info("  Aborted.")
            return
    else:
        log.info("  Non-interactive mode — proceeding automatically.")

    # Derive week label from draft filename
    m = re.search(r'draft-(\d{4}-W\d{2})', path.name)
    label = m.group(1) if m else week_label()
    filename = f"grid-the-grey-briefing-{label}-{voice}.mp3"
    local_path = BRIEFINGS_DIR / filename

    # Generate audio
    audio_bytes = text_to_speech(script, voice, local_path)

    # Upload to R2
    public_url = upload_to_r2(audio_bytes, filename)

    # Save metadata + update Hugo params
    save_episode_metadata(audio_bytes, script, label, voice, public_url)
    m2 = re.match(r'(\d{4})-W(\d+)', label)
    ep_title = f"Week {int(m2.group(2))}, {m2.group(1)} — AI Security Briefing" if m2 else label
    update_hugo_params(public_url, ep_title)

    feed_url = f"{R2_PUBLIC_URL}/feed.xml"
    print()
    print("=" * 60)
    print(f"  ✓ Episode produced successfully")
    print(f"  Week     : {label}")
    print(f"  Voice    : {voice}")
    print(f"  File     : {filename}")
    print(f"  Local    : {local_path}")
    print(f"  R2 URL   : {public_url}")
    print()
    print("  Next steps:")
    print("  1. Listen to the audio at the R2 URL above")
    print(f"  2. Run: python podcast_feed.py --update")
    print(f"     → regenerates {feed_url}")
    print(f"  3. git add hugo-site/hugo.toml briefings/")
    print(f"     git commit -m 'feat: episode {ep_title}'")
    print(f"     git push origin main")
    print("=" * 60)


def cmd_list() -> None:
    BRIEFINGS_DIR.mkdir(exist_ok=True)
    drafts = sorted(BRIEFINGS_DIR.glob("draft-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not drafts:
        log.info("No drafts found. Run: python weekly_briefing.py --generate")
        return

    print(f"\nAvailable drafts ({len(drafts)}):\n")
    for path in drafts:
        text = path.read_text(encoding="utf-8", errors="ignore")
        words = _fm_value(text, "word_count") or "?"
        articles = _fm_value(text, "articles_used") or "?"
        generated = _fm_value(text, "generated_at")[:10] if _fm_value(text, "generated_at") else "?"
        mp3_name = path.name.replace("draft-", "").replace(".md", ".mp3")
        mp3_exists = any(BRIEFINGS_DIR.glob(f"*{path.stem.replace('draft-', '')}*.mp3"))
        status = "✓ produced" if mp3_exists else "  pending"
        print(f"  {status}  {path.name}  ({words} words, {articles} articles, {generated})")
    print()


def cmd_voices() -> None:
    print(f"\nAvailable TTS voices:\n")
    for name, desc in VOICES.items():
        marker = " ← default" if name == DEFAULT_VOICE else ""
        print(f"  {name:10s}  {desc}{marker}")
    print()
    print("Usage: python weekly_briefing.py --produce --voice nova")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Grid the Grey Weekly Security Briefing — script + audio generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weekly_briefing.py --generate
  python weekly_briefing.py --generate --days 14
  python weekly_briefing.py --produce
  python weekly_briefing.py --produce --voice nova
  python weekly_briefing.py --produce briefings/draft-2026-W16.md
  python weekly_briefing.py --list
  python weekly_briefing.py --voices
        """,
    )
    parser.add_argument("--generate",  action="store_true", help="Generate a new script draft from recent articles")
    parser.add_argument("--produce",   nargs="?", const="__latest__", metavar="DRAFT_FILE",
                        help="Convert draft to audio and upload to R2 (default: latest draft)")
    parser.add_argument("--list",      action="store_true", help="List available drafts")
    parser.add_argument("--voices",    action="store_true", help="Show available TTS voices")
    parser.add_argument("--days",      type=int, default=DEFAULT_DAYS,
                        help=f"Days to look back for articles (default: {DEFAULT_DAYS})")
    parser.add_argument("--voice",     default=DEFAULT_VOICE, choices=list(VOICES.keys()),
                        help=f"TTS voice to use (default: {DEFAULT_VOICE})")
    parser.add_argument("--debug",     action="store_true", help="Verbose debug logging")
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if not any([args.generate, args.produce, args.list, args.voices]):
        parser.print_help()
        sys.exit(0)

    if args.voices:
        cmd_voices()
    elif args.list:
        cmd_list()
    elif args.generate:
        cmd_generate(days=args.days)
    elif args.produce is not None:
        draft_file = None if args.produce == "__latest__" else args.produce
        cmd_produce(draft_file=draft_file, voice=args.voice)


if __name__ == "__main__":
    main()
