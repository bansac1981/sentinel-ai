#!/usr/bin/env python3
"""
Grid the Grey — Duplicate Content Checker
==========================================
Checks if a draft article is too similar to any existing published article.
Uses difflib.SequenceMatcher on normalised title + summary text.
Threshold: 80% similarity = blocked.

Usage:
    python check_duplicate.py <path-to-draft-file>

Exit codes:
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
    """Pull title, summary, and draft status from YAML frontmatter."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except OSError:
        return {}

    title = ""
    summary = ""
    is_draft = False

    in_frontmatter = False
    lines = content.splitlines()

    for i, line in enumerate(lines):
        line = line.rstrip("\r")  # handle CRLF
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
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

    return {"title": title, "summary": summary, "is_draft": is_draft}


# ─────────────────────────────────────────────
# Main check
# ─────────────────────────────────────────────

def check_duplicate(draft_path: Path) -> None:

    # Load the draft
    draft_fields = extract_fields(draft_path)
    if not draft_fields:
        print(f"ERROR: Could not read draft file: {draft_path}")
        sys.exit(2)

    draft_title   = draft_fields.get("title", "")
    draft_summary = draft_fields.get("summary", "")
    draft_text    = normalize(f"{draft_title} {draft_summary}")

    if not draft_text.strip():
        print("WARNING: Draft has no title or summary — skipping duplicate check.")
        sys.exit(0)

    print(f"Checking: {draft_title[:80]}")
    print(f"Against all published articles in {POSTS_DIR}/")
    print("-" * 50)

    # Load all published articles (only *.md directly in posts/, not in drafts/)
    max_ratio       = 0.0
    best_match_file = None
    best_match_title = None
    checked         = 0

    for pub_file in POSTS_DIR.glob("*.md"):
        if pub_file.name == "_index.md":
            continue

        pub_fields = extract_fields(pub_file)
        if not pub_fields or pub_fields.get("is_draft"):
            continue  # skip drafts and unreadable files

        pub_text = normalize(
            f"{pub_fields.get('title', '')} {pub_fields.get('summary', '')}"
        )
        if not pub_text.strip():
            continue

        ratio = difflib.SequenceMatcher(None, draft_text, pub_text).ratio()
        checked += 1

        if ratio > max_ratio:
            max_ratio       = ratio
            best_match_file  = pub_file.name
            best_match_title = pub_fields.get("title", "Unknown")

    print(f"Compared against {checked} published article(s).")

    if checked == 0:
        print("No published articles to compare against — OK to publish.")
        sys.exit(0)

    pct = f"{max_ratio:.1%}"
    print(f"Highest similarity: {pct}  |  Threshold: {SIMILARITY_THRESHOLD:.0%}")

    if max_ratio >= SIMILARITY_THRESHOLD:
        print()
        print("=" * 50)
        print("DUPLICATE CHECK FAILED — PUBLISHING BLOCKED")
        print("=" * 50)
        print(f"  Draft:   {draft_title[:70]}")
        print(f"  Matches: {best_match_title[:70]}")
        print(f"  Score:   {pct}")
        print(f"  File:    {best_match_file}")
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
