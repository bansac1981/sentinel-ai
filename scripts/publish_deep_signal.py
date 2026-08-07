#!/usr/bin/env python3
"""
publish_deep_signal.py
======================
Reads a reviewed .md article from sources/pending/, rewrites it as a
Deep Signal editorial article, extracts structured metadata via the
Claude API, renders hero + card SVGs, writes everything to the Hugo
site, commits, pushes, and archives the source file.

Usage:
    python scripts/publish_deep_signal.py <path-to-article.md> [1|2]

    Article type (required — pass as argument or select interactively):
        1 — Security Gap / Event  (threat, attack, broken control)
        2 — Research / Capability (emerging technology, new approach)

    Via GitHub Actions (non-interactive): prefix the filename instead:
        gap-my-article.md  →  type 1
        cap-my-article.md  →  type 2
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

# ── Article type definitions ──────────────────────────────────────────────────
ARTICLE_TYPES = {
    "1": "Security Gap / Event",
    "2": "Research / Capability",
}

# ── Rewrite prompts (one per article type) ────────────────────────────────────
REWRITE_PROMPT_GAP = """You are a senior editorial writer for gridthegrey.com, an AI security intelligence publication for CISOs, security architects, and practitioner security teams.

Using the research input below, write a Deep Signal editorial article following the structure and rules specified here. The output must be the article body only — no frontmatter, no metadata, no title heading.

STRUCTURE (use these exact headings):

## What's Broken
2–3 paragraphs. The specific gap, threat, or incident — grounded in one concrete real-world scenario. Who is affected and what the blast radius is. No background theory. Start with the problem.

## Why Existing Defences Miss It
1–2 paragraphs. The structural reason this slips through current controls. One comparison table (old model vs new threat) only if it genuinely clarifies — omit if not.

## What Attackers Actually Do
A realistic, specific attack chain drawn from the research. Use a mermaid flowchart diagram to illustrate. This section must be concrete, not hypothetical.

## How to Respond
Three tiers of action, always in this order:
- **Immediate** — do today, no budget required
- **Short-term** — this sprint or quarter, some tooling needed
- **Strategic** — 12–24 month architectural changes
Include specific config, commands, or policy steps where the research provides them.

## Honest Assessment
2–3 paragraphs. What we don't know yet. How mature the fix actually is. What the research is uncertain about. Name limitations plainly.

Close with a single unnumbered paragraph (no heading) that states the one most important action the reader should take.

RULES:
- Target 1,400–1,800 words for the full body
- Present tense, active voice throughout
- No references to the source document, paper, report, or research — write as if the editorial team knows this
- No document-type labels, version numbers, internal classification markers, section numbers, arXiv citations, or author affiliations
- No "this paper argues", "the study found", "according to the report" — state facts directly
- One concrete scenario per major section, not multiple hypotheticals
- Tables only where a reader will genuinely consult them, not to replicate research appendices
- All mermaid diagrams must use the flowchart TD type

RESEARCH INPUT:
"""

REWRITE_PROMPT_CAPABILITY = """You are a senior editorial writer for gridthegrey.com, an AI security intelligence publication for CISOs, security architects, and practitioner security teams.

Using the research input below, write a Deep Signal editorial article following the structure and rules specified here. The output must be the article body only — no frontmatter, no metadata, no title heading.

STRUCTURE (use these exact headings):

## Why This Is Worth Your Attention
2–3 paragraphs. The shift or signal — why this capability matters to security teams specifically and why now. Anchor with one concrete data point, real deployment, or regulatory deadline.

## What It Actually Is
2–3 paragraphs. Plain-language explanation with one analogy and one concrete example. No formal specifications, no academic framing, no mathematical notation.

## Where It Fits in Your Stack
How this capability interacts with or displaces existing controls or tools. One table comparing this approach to the traditional alternative if it adds genuine clarity. Not a vendor comparison — a conceptual placement.

## The Gaps and Gotchas
2–3 paragraphs. What the technology cannot do yet. Where the market has not matured. Adversarial edge cases or failure modes. This is the credibility section — be specific about limitations.

## Where to Start
Two tiers only:
- **Worth piloting now** — specific conditions that justify early adoption
- **Watch and revisit** — what signal or milestone would trigger action
This is a readiness assessment, not a how-to guide.

Close with a single unnumbered paragraph (no heading) that answers plainly: is this a now-problem or a next-year problem?

RULES:
- Target 1,600–2,000 words for the full body
- Present tense, active voice throughout
- No references to the source document, paper, report, or research — write as if the editorial team knows this
- No document-type labels, version numbers, internal classification markers, section numbers, arXiv citations, or author affiliations
- No "this paper argues", "the study found", "according to the report" — state facts directly
- One analogy and one concrete example in the explanation section — not multiple
- Tables only where a reader will genuinely consult them, not to replicate research appendices
- All mermaid diagrams must use the flowchart TD type

RESEARCH INPUT:
"""

# ── Metadata extraction prompt ─────────────────────────────────────────────────
EXTRACT_PROMPT = """You are a technical editor preparing a security article for publication on gridthegrey.com.

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


def prompt_article_type() -> str:
    print("\nArticle type:")
    print("  [1] Security Gap / Event  — a threat, attack, or broken control")
    print("  [2] Research / Capability — an emerging technology or new approach")
    while True:
        choice = input("\nSelect [1/2]: ").strip()
        if choice in ARTICLE_TYPES:
            print(f"  → {ARTICLE_TYPES[choice]}")
            return choice
        print("  Please enter 1 or 2.")


def rewrite_article(article_text: str, article_type: str) -> str:
    client = anthropic.Anthropic()
    prompt = REWRITE_PROMPT_GAP if article_type == "1" else REWRITE_PROMPT_CAPABILITY
    message = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt + article_text}]
    )
    return message.content[0].text.strip()


def extract_metadata(article_text: str) -> dict:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": EXTRACT_PROMPT + article_text}]
    )
    raw = message.content[0].text.strip()
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
reading_time: {meta.get('reading_time', 10)}
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


def main(source_path: str, article_type: str):
    src = Path(source_path).resolve()
    if not src.exists():
        print(f"ERROR: file not found: {src}")
        sys.exit(1)

    print(f"→ Reading source: {src.name}")
    article_text = src.read_text(encoding="utf-8")
    today        = date.today().isoformat()

    print(f"→ Rewriting as '{ARTICLE_TYPES[article_type]}' article via Claude API…")
    body = rewrite_article(article_text, article_type)
    word_count = len(body.split())
    reading_time = max(1, math.ceil(word_count / 200))
    print(f"  {word_count} words — ~{reading_time} min read")

    print("→ Extracting metadata via Claude API…")
    meta = extract_metadata(body)
    # Override reading_time with the actual rewritten body count
    meta["reading_time"] = reading_time
    slug = meta.get("slug") or slugify(meta["title"])
    print(f"  slug: {slug}")
    print(f"  title: {meta['title']}")

    template_data = {
        "title":          meta["title"],
        "slug":           slug,
        "date":           today,
        "center_label":   meta.get("center_label", "Orchestrator"),
        "right_label":    meta.get("right_label",  "Outputs"),
        "terminal_title": meta.get("terminal_title", "terminal"),
        "cmd_line1":      meta.get("cmd_line1", ""),
        "cmd_line2":      meta.get("cmd_line2", ""),
        "cmd_line3":      meta.get("cmd_line3", ""),
        "capabilities":   meta.get("capabilities", []),
        "mode_label":     meta.get("mode_label", "Mode"),
        "mode_value":     meta.get("mode_value", "ACTIVE"),
        "warning":        meta.get("warning", ""),
        "inputs":         meta.get("inputs",  []),
        "outputs":        meta.get("outputs", []),
        "frameworks":     meta.get("frameworks", []),
        "stats":          meta.get("stats", []),
        "warning_stat":   meta.get("warning_stat"),
    }

    print("→ Rendering SVGs…")
    hero_svg = render_svg("hero.svg.j2", template_data)
    card_svg = render_svg("card.svg.j2", template_data)

    hero_path = IMG_DIR / f"deep-signal-{slug}.svg"
    card_path = IMG_DIR / f"deep-signal-{slug}-card.svg"
    hero_path.write_text(hero_svg, encoding="utf-8")
    card_path.write_text(card_svg, encoding="utf-8")
    print(f"  hero: {hero_path.relative_to(ROOT)}")
    print(f"  card: {card_path.relative_to(ROOT)}")

    print("→ Writing Hugo content file…")
    content_file = CONTENT_DIR / f"{today}-{slug}.md"
    content_file.write_text(build_frontmatter(meta, slug, today) + body, encoding="utf-8")
    print(f"  content: {content_file.relative_to(ROOT)}")

    print("→ Committing and pushing…")
    git_commit_push(
        [hero_path, card_path, content_file],
        f"feat(deep-signal): publish '{meta['title']}'\n\n"
        f"Type: {ARTICLE_TYPES[article_type]}\n"
        f"Source: {src.name}\n\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )

    print("→ Archiving source file…")
    PROCESSED.mkdir(parents=True, exist_ok=True)
    dest = PROCESSED / src.name
    shutil.move(str(src), str(dest))

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
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python scripts/publish_deep_signal.py <path-to-article.md> [1|2]")
        print("  1 — Security Gap / Event")
        print("  2 — Research / Capability")
        sys.exit(1)

    article_type = None
    if len(sys.argv) == 3:
        if sys.argv[2] not in ARTICLE_TYPES:
            print(f"ERROR: article type must be 1 or 2, got '{sys.argv[2]}'")
            sys.exit(1)
        article_type = sys.argv[2]
    else:
        article_type = prompt_article_type()

    main(sys.argv[1], article_type)
