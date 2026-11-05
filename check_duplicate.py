#!/usr/bin/env python3
"""
Grid the Grey — Duplicate Content Checker
==========================================
Checks if a draft article is too similar to any existing published article.
Uses difflib.SequenceMatcher on normalised title + summary + body text.
Threshold: 80% similarity = blocked.

Usage (CLI):
    python check_duplicate.py <path-to-draft-file>

Usage (importable):
    from check_duplicate import is_content_duplicate
    result = is_content_duplicate(title, summary, body, posts_dir)
    if result["is_duplicate"]:
        print(result["match_title"], result["similarity"])

Exit codes (CLI only):
    0 = OK to publish (no significant duplicate found)
    1 = Duplicate detected (blocked)
    2 = Usage / file error
"""

import difflib
import re
import sys
from pathlib import Path

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

SIMILARITY_THRESHOLD = 0.80
POSTS_DIR = Path("hugo-site/content/posts")

# Common words to strip before comparison (reduces noise)
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "that", "this", "these", "those", "it", "its",
    "as", "not", "no", "so", "if", "about", "into", "through", "new", "also",
}


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, strip punctuation, remove stop words, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    words = [w for w in text.split() if w not in STOP_WORDS and len(w) > 2]
    return " ".join(words)


def extract_fields(filepath: Path) -> dict:
    """Pull title, summary, body preview, and draft status from YAML frontmatter + content."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except OSError:
        return {}

    title = ""
    summary = ""
    is_draft = False
    content_hash = ""

    in_frontmatter = False
    frontmatter_end = 0
    lines = content.splitlines()

    for i, line in enumerate(lines):
        line = line.rstrip("\r")  # handle CRLF
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            frontmatter_end = i + 1
            break
        if not in_frontmatter:
            continue

        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"\'')
        elif line.startswith("summary:"):
            summary = line.split(":", 1)[1].strip().strip('"\'')
        elif line.startswith("draft:"):
            val = line.split(":", 1)[1].strip().lower()
            is_draft = val == "true"
        elif line.startswith("content_hash:"):
            content_hash = line.split(":", 1)[1].strip().strip('"\'')

    # Extract first ~500 chars of body text (after frontmatter)
    body_lines = lines[frontmatter_end:]
    body_preview = " ".join(body_lines)[:500]

    return {
        "title": title,
        "summary": summary,
        "is_draft": is_draft,
        "body_preview": body_preview,
        "content_hash": content_hash,
    }


# ─────────────────────────────────────────────
# Importable API — used by pipeline.py
# ─────────────────────────────────────────────

def is_content_duplicate(
    title: str,
    summary: str,
    body: str = "",
    posts_dir: Path | None = None,
    threshold: float = SIMILARITY_THRESHOLD,
) -> dict:
    """
    Check if an article (title + summary + body preview) is too similar to any
    existing published post. Returns a dict with the result.

    Args:
        title:     Article title
        summary:   Article summary
        body:      Article body text (first ~500 chars used)
        posts_dir: Path to published posts directory
        threshold: Similarity threshold (0.0–1.0, default 0.80)

    Returns:
        {
            "is_duplicate": bool,
            "similarity": float,       # highest match ratio
            "match_title": str | None,  # title of best match
            "match_file": str | None,   # filename of best match
            "checked": int,             # number of posts compared
        }
    """
    if posts_dir is None:
        posts_dir = POSTS_DIR

    # Build the candidate text: title + summary + body preview
    body_preview = body[:500] if body else ""
    candidate_text = normalize(f"{title} {summary} {body_preview}")

    if not candidate_text.strip():
        return {"is_duplicate": False, "similarity": 0.0, "match_title": None,
                "match_file": None, "checked": 0}

    max_ratio = 0.0
    best_match_file = None
    best_match_title = None
    checked = 0

    for pub_file in posts_dir.glob("*.md"):
        if pub_file.name == "_index.md":
            continue

        pub_fields = extract_fields(pub_file)
        if not pub_fields or pub_fields.get("is_draft"):
            continue

        pub_text = normalize(
            f"{pub_fields.get('title', '')} {pub_fields.get('summary', '')} "
            f"{pub_fields.get('body_preview', '')}"
        )
        if not pub_text.strip():
            continue

        ratio = difflib.SequenceMatcher(None, candidate_text, pub_text).ratio()
        checked += 1

        if ratio > max_ratio:
            max_ratio = ratio
            best_match_file = pub_file.name
            best_match_title = pub_fields.get("title", "Unknown")

    return {
        "is_duplicate": max_ratio >= threshold,
        "similarity": max_ratio,
        "match_title": best_match_title,
        "match_file": best_match_file,
        "checked": checked,
    }


# ─────────────────────────────────────────────
# CLI check (original behaviour preserved)
# ─────────────────────────────────────────────

def check_duplicate(draft_path: Path) -> None:

    # Load the draft
    draft_fields = extract_fields(draft_path)
    if not draft_fields:
        print(f"ERROR: Could not read draft file: {draft_path}")
        sys.exit(2)

    draft_title   = draft_fields.get("title", "")
    draft_summary = draft_fields.get("summary", "")
    draft_body    = draft_fields.get("body_preview", "")

    result = is_content_duplicate(
        title=draft_title,
        summary=draft_summary,
        body=draft_body,
        posts_dir=POSTS_DIR,
    )

    if not (draft_title or draft_summary):
        print("WARNING: Draft has no title or summary — skipping duplicate check.")
        sys.exit(0)

    print(f"Checking: {draft_title[:80]}")
    print(f"Against all published articles in {POSTS_DIR}/")
    print("-" * 50)
    print(f"Compared against {result['checked']} published article(s).")

    if result["checked"] == 0:
        print("No published articles to compare against — OK to publish.")
        sys.exit(0)

    pct = f"{result['similarity']:.1%}"
    print(f"Highest similarity: {pct}  |  Threshold: {SIMILARITY_THRESHOLD:.0%}")

    if result["is_duplicate"]:
        print()
        print("=" * 50)
        print("DUPLICATE CHECK FAILED — PUBLISHING BLOCKED")
        print("=" * 50)
        print(f"  Draft:   {draft_title[:70]}")
        print(f"  Matches: {result['match_title'][:70]}")
        print(f"  Score:   {pct}")
        print(f"  File:    {result['match_file']}")
        print()
        print("This draft is too similar to an existing published article.")
        print("The draft has NOT been published and remains in posts/drafts/.")
        print("=" * 50)
        sys.exit(1)
    else:
        print(f"OK — no significant duplicate found (best match: {pct}). Proceeding.")
        sys.exit(0)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_duplicate.py <path-to-draft-file>")
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(2)

    check_duplicate(path)
