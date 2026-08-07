#!/usr/bin/env python3
"""
publish_deep_signal.py
======================
Reads a reviewed .md article from sources/pending/, extracts structured
metadata via the Claude API, renders hero + card SVGs, writes everything
to the Hugo site, commits, pushes, and archives the source file.

Usage (local):
    python scripts/publish_deep_signal.py sources/pending/my-article.md

Usage (GitHub Actions):
    Triggered automatically when a .md file is pushed to sources/pending/
"""

import os
import re
import sys
import json
import math
import shutil
import subprocess
from datetime import date
from pathlib import Path

import anthropic
from jinja2 import Environment, FileSystemLoader

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent.parent
HUGO_ROOT   = ROOT / "hugo-site"
CONTENT_DIR = HUGO_ROOT / "content" / "deep-signal"
IMG_DIR     = HUGO_ROOT / "static" / "img"
TEMPLATES   = Path(__file__).parent / "svg_templates"
PROCESSED   = ROOT / "sources" / "processed"

# ── Claude model ──────────────────────────────────────────────────────────────
MODEL = "claude-sonnet-4-5"

# ── Extraction prompt ─────────────────────────────────────────────────────────
EXTRACT_PROMPT = """You are a technical editor preparing a security research article for publication on gridthegrey.com.

Read the article below and return a single JSON object with these exact fields. No prose, no markdown — just the JSON.

{
  "title": "Exact article title, max 80 chars",
  "slug": "kebab-case-url-slug-max-6-words",
  "description": "One sentence (max 200 chars) summarising what the article covers and for whom",
  "reading_time": <integer minutes, estimated at 200 wpm>,
  "tags": ["tag1", "tag2", "tag3", "tag4"],
  "categories": ["Primary Category", "Secondary Category"],

  "tldr_what": "One sentence: what this article covers (tool, topic, approach)",
  "tldr_who": "One sentence: who this is for (role/team type)",
  "tldr_actions": ["Key takeaway 1", "Key takeaway 2", "Key takeaway 3"],

  "inputs": [
    {"title": "Short name", "subtitle": "Endpoint or file path", "detail": "Key parameters or formats"},
    {"title": "...", "subtitle": "...", "detail": "..."},
    {"title": "...", "subtitle": "...", "detail": "..."},
    {"title": "...", "subtitle": "...", "detail": "..."}
  ],
  "outputs": [
    {"title": "Short name", "subtitle": "File path or destination", "detail": "Format or framework mapped to"},
    {"title": "...", "subtitle": "...", "detail": "..."},
    {"title": "...", "subtitle": "...", "detail": "..."},
    {"title": "...", "subtitle": "...", "detail": "..."}
  ],

  "center_label": "Short label for the orchestrator/tool (e.g. 'Claude Code Orchestrator')",
  "right_label": "Short label for outputs column (e.g. 'Security Outputs')",
  "terminal_title": "Short terminal window title (e.g. 'claude-code — bash')",
  "cmd_line1": "First line of representative CLI command (max 42 chars)",
  "cmd_line2": "Second line (max 42 chars)",
  "cmd_line3": "Third line (max 42 chars)",

  "capabilities": [
    "⚡ Short Cap 1",
    "◈ Short Cap 2",
    "🔒 Short Cap 3",
    "⬡ Short Cap 4",
    "📋 Short Cap 5",
    "— Short Cap 6"
  ],

  "mode_label": "Short label for the status/mode row (e.g. 'Permission Mode')",
  "mode_value": "Value shown in green badge (e.g. 'MANUAL')",
  "warning": "One-line warning strip text (max 60 chars, no ⚠ prefix)",

  "frameworks": ["Framework 1", "Framework 2", "Framework 3", "Framework 4", "Framework 5", "Framework 6", "Framework 7"],

  "stats": [
    {"value": "2", "label_top": "Use", "label_bot": "Cases"},
    {"value": "~$13", "label_top": "avg/analyst", "label_bot": "per day"},
    {"value": "7", "label_top": "Lockdown", "label_bot": "Settings"}
  ],

  "warning_stat": {
    "line1": "Short warning heading (max 30 chars)",
    "line2": "Short warning detail (max 45 chars)"
  }
}

Rules:
- inputs and outputs must have exactly 4 items each
- capabilities must have exactly 6 items, each prefixed with an icon/symbol
- frameworks must have 5–7 items
- stats must have exactly 3 items
- All text values must fit within the character limits shown
- slug must be unique enough to identify this specific article

ARTICLE:
"""


def extract_metadata(article_text: str) -> dict:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": EXTRACT_PROMPT + article_text}]
    )
    raw = message.content[0].text.strip()
    # Strip markdown code fences if model wrapped the JSON
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


def render_svg(template_name: str, data: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=True   # SVG is XML — escape & < > in all text values
    )
    tmpl = env.get_template(template_name)
    return tmpl.render(**data)


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:60]


def estimate_reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, math.ceil(words / 200))


def build_frontmatter(meta: dict, slug: str, today: str) -> str:
    tags_yaml    = "\n".join(f'  - "{t}"' for t in meta["tags"])
    cats_yaml    = "\n".join(f'  - "{c}"' for c in meta["categories"])
    actions_yaml = "\n".join(f'  - "{a}"' for a in meta["tldr_actions"])
    return f"""---
title: "{meta['title']}"
date: {today}
draft: false
content_type: "deep_signal"
author: "Grid the Grey Editorial"
description: "{meta['description']}"
reading_time: {meta.get('reading_time', 15)}
thumbnail: "/img/deep-signal-{slug}.svg"
thumbnail_card: "/img/deep-signal-{slug}-card.svg"
tldr_what: "{meta['tldr_what']}"
tldr_who_at_risk: "{meta['tldr_who']}"
tldr_actions:
{actions_yaml}
categories:
{cats_yaml}
tags:
{tags_yaml}
---

"""


def git_commit_push(files: list[Path], message: str):
    repo = str(ROOT)
    rel  = [str(f.relative_to(ROOT)) for f in files]
    subprocess.run(["git", "add"] + rel,       cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=repo, check=True)
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=repo, check=True)
    subprocess.run(["git", "push", "origin", "main"],   cwd=repo, check=True)


def main(source_path: str):
    src = Path(source_path).resolve()
    if not src.exists():
        print(f"ERROR: file not found: {src}")
        sys.exit(1)

    print(f"→ Reading source: {src.name}")
    article_text = src.read_text(encoding="utf-8")
    today        = date.today().isoformat()

    print("→ Extracting metadata via Claude API…")
    meta = extract_metadata(article_text)
    slug = meta.get("slug") or slugify(meta["title"])
    print(f"  slug: {slug}")
    print(f"  title: {meta['title']}")

    # Merge template data
    template_data = {
        "title":        meta["title"],
        "slug":         slug,
        "date":         today,
        "center_label": meta.get("center_label", "Orchestrator"),
        "right_label":  meta.get("right_label",  "Outputs"),
        "terminal_title": meta.get("terminal_title", "terminal"),
        "cmd_line1":    meta.get("cmd_line1", ""),
        "cmd_line2":    meta.get("cmd_line2", ""),
        "cmd_line3":    meta.get("cmd_line3", ""),
        "capabilities": meta.get("capabilities", []),
        "mode_label":   meta.get("mode_label", "Mode"),
        "mode_value":   meta.get("mode_value", "MANUAL"),
        "warning":      meta.get("warning", ""),
        "inputs":       meta.get("inputs",  []),
        "outputs":      meta.get("outputs", []),
        "frameworks":   meta.get("frameworks", []),
        "stats":        meta.get("stats", []),
        "warning_stat": meta.get("warning_stat"),
    }

    print("→ Rendering SVGs…")
    hero_svg = render_svg("hero.svg.j2", template_data)
    card_svg = render_svg("card.svg.j2", template_data)

    hero_path = IMG_DIR  / f"deep-signal-{slug}.svg"
    card_path = IMG_DIR  / f"deep-signal-{slug}-card.svg"
    hero_path.write_text(hero_svg, encoding="utf-8")
    card_path.write_text(card_svg, encoding="utf-8")
    print(f"  hero: {hero_path.relative_to(ROOT)}")
    print(f"  card: {card_path.relative_to(ROOT)}")

    print("→ Writing Hugo content file…")
    frontmatter   = build_frontmatter(meta, slug, today)
    article_body  = article_text.strip()
    # Strip the original research metadata header if present (lines before first ##)
    first_heading = re.search(r'^#{1,2} ', article_body, re.MULTILINE)
    if first_heading:
        article_body = article_body[first_heading.start():]
    content_file = CONTENT_DIR / f"{today}-{slug}.md"
    content_file.write_text(frontmatter + article_body, encoding="utf-8")
    print(f"  content: {content_file.relative_to(ROOT)}")

    print("→ Committing and pushing…")
    commit_msg = (
        f"feat(deep-signal): publish '{meta['title']}'\n\n"
        f"Auto-published via publish_deep_signal.py\n"
        f"Source: {src.name}\n\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )
    git_commit_push([hero_path, card_path, content_file], commit_msg)

    print("→ Archiving source file…")
    PROCESSED.mkdir(parents=True, exist_ok=True)
    dest = PROCESSED / src.name
    shutil.move(str(src), str(dest))

    # Commit the archive move too
    subprocess.run(["git", "add",
        str(src.relative_to(ROOT)),
        str(dest.relative_to(ROOT))],
        cwd=str(ROOT), check=True)
    subprocess.run(["git", "commit", "-m",
        f"chore: archive source {src.name}\n\nCo-Authored-By: Claude <noreply@anthropic.com>"],
        cwd=str(ROOT), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(ROOT), check=True)

    print(f"\n✓ Done — live at: https://gridthegrey.com/deep-signal/{slug}/")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/publish_deep_signal.py <path-to-article.md>")
        sys.exit(1)
    main(sys.argv[1])
