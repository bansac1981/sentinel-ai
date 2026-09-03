#!/usr/bin/env python3
"""
generate_monthly_review.py — Grid the Grey Monthly AI Security Intelligence Review
===================================================================================
Generates a monthly intelligence review for CISOs and board-level decision makers.
Uses Opus 5 for the main narrative (synthesis, predictions, editorial voice) and
Sonnet 5 for supporting tasks (LinkedIn post).

Usage:
    python generate_monthly_review.py --generate                  # Current month - 1
    python generate_monthly_review.py --generate --month 2026-08  # Specific month
    python generate_monthly_review.py --dry-run                   # Analytics only
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import httpx
import ssl
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Config ────────────────────────────────────────────────────────────────────
POSTS_DIR       = Path(__file__).parent / "hugo-site" / "content" / "posts"
DEEP_SIGNAL_DIR = Path(__file__).parent / "hugo-site" / "content" / "deep-signal"
REPORTS_DIR     = Path(__file__).parent / "signal-reports"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
NARRATIVE_MODEL   = os.getenv("MONTHLY_NARRATIVE_MODEL", "claude-opus-5")
SUPPORT_MODEL     = os.getenv("MONTHLY_SUPPORT_MODEL", "claude-sonnet-5")

THREAT_SEVERITY = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "NONE": 0}

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("monthly_review")


# ── Front-matter parser (reused from weekly_signal_report.py) ─────────────────
def _fm_value(text: str, key: str) -> str:
    m = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def _fm_list(text: str, key: str) -> list:
    m = re.search(rf'^{key}:\s*\[([^\]]*)\]', text, re.MULTILINE)
    if not m:
        return []
    raw = m.group(1)
    return [v.strip().strip('"').strip("'") for v in raw.split(",") if v.strip()]

def parse_post(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    if _fm_value(text, "draft").lower() == "true":
        return None
    date_str = _fm_value(text, "date")
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return None
    try:
        score = float(_fm_value(text, "relevance_score"))
    except Exception:
        score = 0.0
    body_match = re.search(r'^---\n.*?\n---\n(.*)', text, re.DOTALL)
    body = body_match.group(1).strip()[:1500] if body_match else ""
    slug = _fm_value(text, "slug")
    return {
        "title": _fm_value(text, "title"),
        "slug": slug,
        "summary": _fm_value(text, "summary"),
        "source": _fm_value(text, "source"),
        "source_url": _fm_value(text, "source_url"),
        "threat_level": _fm_value(text, "threat_level").upper(),
        "relevance_score": score,
        "categories": _fm_list(text, "categories"),
        "tags": _fm_list(text, "tags"),
        "mitre_techniques": _fm_list(text, "mitre_techniques"),
        "owasp_categories": _fm_list(text, "owasp_categories"),
        "threat_actors": _fm_list(text, "threat_actors"),
        "content_type": _fm_value(text, "content_type"),
        "date": date,
        "body_excerpt": body,
    }


# ── Article reader (monthly) ──────────────────────────────────────────────────
def get_monthly_articles(year: int, month: int) -> list:
    articles = []
    if not POSTS_DIR.exists():
        log.error(f"Posts directory not found: {POSTS_DIR}")
        return []
    prefix = f"{year}-{month:02d}"
    for path in POSTS_DIR.glob(f"{prefix}-*.md"):
        if path.name == "_index.md":
            continue
        post = parse_post(path)
        if post and post["title"]:
            articles.append(post)
    articles.sort(key=lambda a: a["relevance_score"], reverse=True)
    log.info(f"  Found {len(articles)} articles for {prefix}")
    return articles


# ── Analytics ─────────────────────────────────────────────────────────────────
def compute_analytics(articles: list) -> dict:
    mitre_counter = Counter()
    owasp_counter = Counter()
    threat_level_counter = Counter()
    threat_actor_counter = Counter()
    category_counter = Counter()
    mitre_cooccurrence = Counter()
    total_relevance = 0.0

    for article in articles:
        for tech in article["mitre_techniques"]:
            mitre_counter[tech] += 1
        for cat in article["owasp_categories"]:
            owasp_counter[cat] += 1
        if article["threat_level"]:
            threat_level_counter[article["threat_level"]] += 1
        for actor in article["threat_actors"]:
            threat_actor_counter[actor] += 1
        for cat in article["categories"]:
            category_counter[cat] += 1
        total_relevance += article["relevance_score"]
        techniques = article["mitre_techniques"]
        for i in range(len(techniques)):
            for j in range(i + 1, len(techniques)):
                pair = tuple(sorted([techniques[i], techniques[j]]))
                mitre_cooccurrence[pair] += 1

    avg_relevance = round(total_relevance / len(articles), 2) if articles else 0
    return {
        "article_count": len(articles),
        "avg_relevance": avg_relevance,
        "mitre_distribution": dict(mitre_counter.most_common()),
        "owasp_distribution": dict(owasp_counter.most_common()),
        "threat_level_distribution": dict(threat_level_counter.most_common()),
        "threat_actor_distribution": dict(threat_actor_counter.most_common()),
        "category_distribution": dict(category_counter.most_common()),
        "mitre_cooccurrence": {f"{a} + {b}": c for (a, b), c in mitre_cooccurrence.most_common(15)},
    }


# ── Build context for Claude ──────────────────────────────────────────────────
def build_monthly_context(articles: list, analytics: dict) -> str:
    lines = []
    lines.append("=== MONTHLY STATISTICS ===")
    lines.append(f"Total articles: {analytics['article_count']}")
    lines.append(f"Average relevance score: {analytics['avg_relevance']}/10")
    lines.append(f"Threat level breakdown: {json.dumps(analytics['threat_level_distribution'])}")
    lines.append("")

    lines.append("=== MITRE ATLAS TECHNIQUE DISTRIBUTION ===")
    for tech, count in sorted(analytics["mitre_distribution"].items(), key=lambda x: x[1], reverse=True)[:20]:
        lines.append(f"  {tech}: {count} occurrences")
    lines.append("")

    lines.append("=== OWASP LLM TOP 10 DISTRIBUTION ===")
    for cat, count in sorted(analytics["owasp_distribution"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {cat}: {count} occurrences")
    lines.append("")

    lines.append("=== THREAT ACTOR DISTRIBUTION ===")
    for actor, count in sorted(analytics["threat_actor_distribution"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {actor}: {count} mentions")
    lines.append("")

    lines.append("=== CATEGORY DISTRIBUTION ===")
    for cat, count in sorted(analytics["category_distribution"].items(), key=lambda x: x[1], reverse=True)[:15]:
        lines.append(f"  {cat}: {count}")
    lines.append("")

    lines.append("=== MITRE TECHNIQUE CO-OCCURRENCE (Attack Chain Patterns) ===")
    for pair, count in sorted(analytics["mitre_cooccurrence"].items(), key=lambda x: x[1], reverse=True)[:15]:
        lines.append(f"  {pair}: {count} co-occurrences")
    lines.append("")

    # All articles with full summaries (sorted by relevance)
    lines.append("=== ALL ARTICLES THIS MONTH (by relevance) ===")
    for i, article in enumerate(articles, 1):
        lines.append(f"\n--- Article {i} ---")
        lines.append(f"Title: {article['title']}")
        lines.append(f"Slug: {article['slug']}")
        lines.append(f"Date: {article['date'].strftime('%Y-%m-%d')}")
        lines.append(f"Source: {article['source']}")
        lines.append(f"Threat Level: {article['threat_level']} | Relevance: {article['relevance_score']}/10")
        if article["mitre_techniques"]:
            lines.append(f"MITRE: {', '.join(article['mitre_techniques'][:5])}")
        if article["owasp_categories"]:
            lines.append(f"OWASP: {', '.join(article['owasp_categories'][:4])}")
        if article["threat_actors"]:
            lines.append(f"Threat Actors: {', '.join(article['threat_actors'])}")
        if article["categories"]:
            lines.append(f"Categories: {', '.join(article['categories'][:5])}")
        lines.append(f"Summary: {article['summary'][:600]}")

    return "\n".join(lines)


# ── Narrative generation (Opus 5) ─────────────────────────────────────────────
def _call_claude(model: str, prompt: str, max_tokens: int = 16000, use_thinking: bool = False) -> tuple[str, dict]:
    """Call Claude API via httpx. Returns (text_response, usage_dict)."""
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    body = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }

    if use_thinking:
        body["thinking"] = {"type": "adaptive"}

    retries = [30, 60, 120]
    with httpx.Client(timeout=300.0) as client:
        for attempt in range(len(retries) + 1):
            resp = client.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
            if resp.status_code == 529 and attempt < len(retries):
                wait = retries[attempt]
                log.warning(f"  API overloaded (529), retrying in {wait}s (attempt {attempt + 1}/{len(retries)})...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            break
        data = resp.json()

    stop_reason = data.get("stop_reason", "unknown")
    if stop_reason == "max_tokens":
        log.warning(f"  Response truncated (hit max_tokens={max_tokens})")

    raw_text = ""
    for block in data.get("content", []):
        if block.get("type") == "text":
            raw_text = block["text"].strip()
            break

    usage = data.get("usage", {})
    return raw_text, usage


def _repair_truncated_json(text: str) -> dict | None:
    """Try to repair JSON truncated by max_tokens by closing open brackets."""
    open_braces = 0
    open_brackets = 0
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            escape_next = False
            continue
        if ch == '\\' and in_string:
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            open_braces += 1
        elif ch == '}':
            open_braces -= 1
        elif ch == '[':
            open_brackets += 1
        elif ch == ']':
            open_brackets -= 1

    if open_braces == 0 and open_brackets == 0:
        return None

    repaired = text.rstrip().rstrip(',')
    if repaired[-1] == ':':
        repaired += ' ""'
    repaired += ']' * open_brackets + '}' * open_braces
    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        last_comma = repaired.rfind(',')
        if last_comma > 0:
            trimmed = repaired[:last_comma]
            trimmed += ']' * trimmed.count('[') + '}' * trimmed.count('{')
            closers_needed_brackets = trimmed.count('[') - trimmed.count(']')
            closers_needed_braces = trimmed.count('{') - trimmed.count('}')
            trimmed = repaired[:last_comma]
            trimmed += ']' * max(closers_needed_brackets, 0) + '}' * max(closers_needed_braces, 0)
            try:
                return json.loads(trimmed)
            except json.JSONDecodeError:
                return None
        return None


def _parse_json_response(raw_text: str) -> dict:
    """Parse JSON from Claude response, with truncation repair as fallback."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        log.warning(f"  Direct JSON parse failed: {e}")

    json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    log.warning("  Attempting truncated JSON repair...")
    repaired = _repair_truncated_json(raw_text)
    if repaired:
        log.info("  Truncated JSON repaired successfully (some sections may be incomplete)")
        return repaired

    log.error(f"  Raw response (first 1000 chars): {raw_text[:1000]}")
    log.error("  Could not parse or repair JSON. Aborting.")
    sys.exit(1)


def generate_narrative(articles: list, analytics: dict, month_label: str) -> dict:
    context = build_monthly_context(articles, analytics)
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    prompt = f"""You are a senior AI security intelligence analyst producing the monthly "Deep Signal" intelligence review for Grid the Grey. This is a strategic briefing read by CISOs, board members, and security executives.

Today's date: {now_str}
Report period: {month_label}

Below is the complete analytics data and article summaries for this month:

{context}

Based on this data, generate a comprehensive monthly intelligence review. The audience is CISO/board-level — strategic, risk-framed, concise. No raw MITRE technique IDs in the body text (use plain English names). Every section must answer "so what does this mean for my organisation?"

Output ONLY valid JSON with these exact keys:

{{
  "title": "A polished, industry-grade title (max 8 words). Think CrowdStrike Global Threat Report or Mandiant M-Trends style. No comma-separated lists. Short, declarative, punchy. Example: 'When AI Becomes the Adversary'",
  "month_in_focus": "One paragraph (~100 words). Editorial thesis that names the month's defining character. Not a summary — a strategic narrative. Open with a bold claim about what this month meant. Example opening: 'August 2026 was the month the industry's theoretical concern about AI autonomy became an operational reality.'",
  "top_developments": [
    {{
      "rank": 1,
      "headline": "Short headline for this development",
      "what_happened": "2-3 sentences describing the event(s). Reference specific articles by their slug for linking. Be specific — name the actors, the systems, the attack chains.",
      "board_implication": "One sentence: what this means for a board-level decision maker.",
      "article_slugs": ["slug-1", "slug-2"]
    }}
  ],
  "ai_threat_landscape": {{
    "attacks_using_ai": "One paragraph (~120 words). How AI is being weaponised. Reference specific incidents from the month's articles by slug.",
    "attacks_on_ai": "One paragraph (~120 words). How AI systems themselves are being targeted. Reference specific CVEs and incidents by slug.",
    "governance_incidents": "One paragraph (~100 words). Regulatory, compliance, and governance developments. Reference specific articles by slug."
  }},
  "threat_actor_spotlight": [
    {{
      "name": "Actor name (e.g., Kimsuky / APT43)",
      "motivation": "One word: Espionage, Financial, Hacktivism",
      "target_sectors": ["sector1", "sector2"],
      "ai_adoption": "2-3 sentences on how this actor used AI this month.",
      "whats_changed": "1-2 sentences on what's new about their behaviour.",
      "article_slugs": ["slug-1"]
    }}
  ],
  "regulatory_watch": [
    {{
      "headline": "Bold headline for this development",
      "analysis": "2-3 sentences with strategic framing for CISO audience.",
      "article_slugs": ["slug-1"]
    }}
  ],
  "trends_to_watch": [
    {{
      "headline": "Short trend headline",
      "analysis": "One paragraph (~80 words). Forward-looking analyst judgment derived from the month's patterns. Explicitly framed as prediction, not reported fact. Reference specific evidence from this month.",
      "article_slugs": ["slug-1", "slug-2"]
    }}
  ],
  "attack_chain_mermaid": "A Mermaid flowchart diagram using 'flowchart LR' (left to right). Use short plain English labels (2-3 words max) with MITRE technique IDs and event counts shown via <small> tags on a second line using <br/>. Example node: PI[\"Prompt Injection<br/><small>AML.T0051 · 40 events</small>\"]. Use subgraphs for 'Initial Access', 'Persistence', and 'Impact'. Add short edge labels in quotes. Keep to 4-5 nodes maximum. Output ONLY the mermaid code, no code fences.",
  "methodology_note": "2-3 sentences describing data sources and methodology."
}}

IMPORTANT RULES:
- This is a MONTHLY review, not a weekly summary. Identify themes and patterns across the full month.
- STRATEGIC VOICE: Write for board members who need to make budget and risk decisions, not for SOC analysts.
- Every assertion must be grounded in the article data provided. Do not hallucinate.
- Reference articles by their slug field (e.g., "anthropic-mythos-5-ai-agent-launches-rogue-supply-chain-attack") so the final report can link to them.
- Top developments: Include 6-8 developments ranked by BUSINESS IMPACT, not technical severity.
- Threat actor spotlight: 1-2 actors maximum. Only include if there's substantial evidence in the articles.
- Trends to watch: 2-3 forward-looking items. This is the highest-value section.
- Regulatory watch: 3-4 items.
- Write in British English (analyse, defence, organisation).
- QUALITY over QUANTITY: every sentence must earn its place. No filler, no padding, no generic AI-safety platitudes.
- Output ONLY the JSON object. No markdown code fences, no preamble."""

    log.info(f"  Calling {NARRATIVE_MODEL} for monthly narrative generation...")
    raw_text, usage = _call_claude(NARRATIVE_MODEL, prompt, max_tokens=32000, use_thinking=True)

    if raw_text.startswith("```"):
        raw_text = re.sub(r'^```(?:json)?\s*\n?', '', raw_text)
        raw_text = re.sub(r'\n?```\s*$', '', raw_text)

    narrative = _parse_json_response(raw_text)

    log.info(f"  Narrative generated: {len(raw_text)} chars")
    log.info(f"  Usage: input={usage.get('input_tokens', '?')}, output={usage.get('output_tokens', '?')}")
    return narrative


# ── LinkedIn post (Sonnet 5) ──────────────────────────────────────────────────
def generate_linkedin_post(narrative: dict, analytics: dict, month_label: str) -> str:
    summary = json.dumps({
        "title": narrative.get("title", ""),
        "month_in_focus": narrative.get("month_in_focus", ""),
        "top_developments": [d["headline"] for d in narrative.get("top_developments", [])[:5]],
        "trends": [t["headline"] for t in narrative.get("trends_to_watch", [])[:3]],
        "stats": analytics["threat_level_distribution"],
        "article_count": analytics["article_count"],
    }, indent=2)

    prompt = f"""Generate a LinkedIn post for the Grid the Grey Monthly Intelligence Review: {month_label}.

Here is the report summary:
{summary}

Write a professional LinkedIn post (max 300 words) that:
1. Opens with the report title and month
2. States 3-4 key findings in brief bullet points
3. Names the top 3 trends to watch
4. Closes with a call to read the full report on Grid the Grey
5. Ends with relevant hashtags

Output ONLY the post text, no preamble."""

    log.info(f"  Calling {SUPPORT_MODEL} for LinkedIn post...")
    raw_text, usage = _call_claude(SUPPORT_MODEL, prompt, max_tokens=2000)
    log.info(f"  LinkedIn usage: input={usage.get('input_tokens', '?')}, output={usage.get('output_tokens', '?')}")
    return raw_text


# ── Build Hugo markdown ───────────────────────────────────────────────────────
def build_hugo_article(narrative: dict, analytics: dict, articles: list, year: int, month: int) -> str:
    month_name = datetime(year, month, 1).strftime("%B")
    month_label = f"{month_name} {year}"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    title = narrative.get("title", f"Monthly Intelligence Review: {month_label}")
    slug = f"monthly-review-{month_name.lower()}-{year}"

    # Get top developments for description
    top_devs = narrative.get("top_developments", [])
    desc_themes = ", ".join([d["headline"].lower() for d in top_devs[:3]])
    description = f"AI security intelligence review for {month_label} — {analytics['article_count']} articles analysed across {desc_themes}. A strategic briefing for CISOs and board-level decision makers."

    # Build TL;DR from narrative
    month_in_focus = narrative.get("month_in_focus", "")
    trends = narrative.get("trends_to_watch", [])
    trend_headlines = [t["headline"] for t in trends[:3]]

    # Threat level counts
    tl = analytics["threat_level_distribution"]
    critical = tl.get("CRITICAL", 0)
    high = tl.get("HIGH", 0)
    medium = tl.get("MEDIUM", 0)
    low = tl.get("LOW", 0)
    total = analytics["article_count"]
    pct_severe = round(100 * (critical + high) / total) if total else 0

    # OWASP top categories
    owasp = analytics["owasp_distribution"]
    owasp_sorted = sorted(owasp.items(), key=lambda x: x[1], reverse=True)

    # MITRE top techniques
    mitre = analytics["mitre_distribution"]
    mitre_sorted = sorted(mitre.items(), key=lambda x: x[1], reverse=True)

    # Threat actors
    actors = analytics["threat_actor_distribution"]

    # CVE articles
    cve_articles = [a for a in articles if "cve-" in a["slug"].lower()]
    cve_articles.sort(key=lambda a: a["relevance_score"], reverse=True)

    # ── Frontmatter ──
    lines = []
    lines.append("---")
    lines.append(f'title: "{title}"')
    lines.append(f'subtitle: "Monthly Intelligence Review: {month_label}"')
    lines.append(f'date: "{date_str}"')
    lines.append("draft: false")
    lines.append(f'slug: "{slug}"')
    lines.append('content_type: "monthly_review"')
    lines.append('author: "Grid the Grey Editorial"')
    lines.append(f'description: "{description[:300]}"')
    lines.append("reading_time: 12")
    lines.append(f'thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080"')
    lines.append('categories: ["Deep Signal", "Intelligence Report", "Monthly Review", "LLM Security", "Agentic AI"]')
    lines.append(f'tags: ["monthly-review", "threat-intelligence", "mitre-atlas", "owasp-llm", "{month_name.lower()}-{year}", "ciso-briefing"]')
    lines.append("")
    lines.append("# TL;DR")
    lines.append(f'tldr_what: "{month_in_focus[:200]}"')
    lines.append(f'tldr_who_at_risk: "CISOs and security leaders at organisations deploying agentic AI, copilots, or AI-integrated CI/CD pipelines."')
    actions = narrative.get("trends_to_watch", [{}])
    action_items = [t.get("headline", "") for t in actions[:3]]
    lines.append(f'tldr_actions: {json.dumps(action_items)}')
    lines.append("---")
    lines.append("")

    # ── Section 1: Month in Focus ──
    lines.append("## 1. The Month in Focus")
    lines.append("")
    lines.append(narrative.get("month_in_focus", ""))
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 2: By the Numbers ──
    lines.append("## 2. By the Numbers")
    lines.append("")

    # Vendor launches and autonomous incidents (count from articles)
    vendor_keywords = ["launches", "acquires", "releases", "ships", "adds"]
    vendor_count = sum(1 for a in articles if any(kw in a["title"].lower() for kw in vendor_keywords) and a["threat_level"] in ("MEDIUM", "LOW"))
    autonomous_keywords = ["autonomous", "sandbox escape", "self-replicat", "rogue", "unsanctioned"]
    autonomous_count = sum(1 for a in articles if any(kw in (a["title"] + " " + a["summary"]).lower() for kw in autonomous_keywords))

    lines.append('<div class="monthly-stats-grid" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin: 2rem 0; text-align: center;">')
    lines.append("")
    stats = [
        (str(total), "Articles Analysed", "#f8fafc", "#e2e8f0", "#0f172a"),
        (str(critical), "Critical-Severity Events", "#fef2f2", "#fecaca", "#dc2626"),
        (str(high), "High-Severity Events", "#fff7ed", "#fed7aa", "#ea580c"),
        (f"{pct_severe}%", "Critical + High Rating", "#eef2ff", "#c7d2fe", "#4338ca"),
        (str(max(vendor_count, 1)), "Major Vendor Security Launches", "#f0fdf4", "#bbf7d0", "#15803d"),
        (str(max(autonomous_count, 1)), "Autonomous Agent Incidents", "#faf5ff", "#e9d5ff", "#7c3aed"),
    ]
    for val, label, bg, border, color in stats:
        lines.append(f'<div style="background: {bg}; border: 1px solid {border}; border-radius: 12px; padding: 1.5rem;">')
        lines.append(f'<div style="font-size: 2.5rem; font-weight: 800; color: {color};">{val}</div>')
        lines.append(f'<div style="font-size: 0.875rem; color: #64748b;">{label}</div>')
        lines.append("</div>")
        lines.append("")
    lines.append("</div>")
    lines.append("")

    # Threat severity bar chart
    lines.append("### Threat Severity Distribution")
    lines.append("")
    max_count = max(critical, high, medium, low, 1)
    severity_data = [
        ("CRITICAL", critical, "#dc2626", "#ef4444", "#991b1b"),
        ("HIGH", high, "#ea580c", "#fb923c", "#9a3412"),
        ("MEDIUM", medium, "#f59e0b", "#fbbf24", "#92400e"),
        ("LOW", low, "#16a34a", "#4ade80", "#166534"),
    ]
    lines.append('<div style="display:flex; align-items:end; gap:0.75rem; height:180px; margin:2rem 0; padding:1rem 0;">')
    for label, count, c1, c2, tc in severity_data:
        h = max(int(160 * count / max_count), 8) if count > 0 else 8
        lines.append(f'  <div style="display:flex;flex-direction:column;align-items:center;flex:1;">')
        lines.append(f'    <div style="font-weight:700;font-size:0.8rem;color:{tc};margin-bottom:0.25rem;">{count}</div>')
        lines.append(f'    <div style="width:100%;background:linear-gradient(180deg,{c1},{c2});border-radius:6px 6px 0 0;height:{h}px;"></div>')
        lines.append(f'    <div style="font-size:0.75rem;color:#64748b;margin-top:0.5rem;font-weight:600;">{label}</div>')
        lines.append(f'  </div>')
    lines.append('</div>')
    lines.append("")

    # OWASP horizontal bar chart
    lines.append("### Top OWASP LLM Categories")
    lines.append("")
    colors_owasp = ["#6366f1", "#8b5cf6", "#a855f7", "#c026d3", "#e11d48", "#dc2626", "#ea580c"]
    light_owasp = ["#818cf8", "#a78bfa", "#c084fc", "#d946ef", "#fb7185", "#f87171", "#fb923c"]
    lines.append('<div style="margin:2rem 0;">')
    max_owasp = owasp_sorted[0][1] if owasp_sorted else 1
    for idx, (cat, count) in enumerate(owasp_sorted[:7]):
        pct = round(100 * count / max_owasp)
        short_name = cat.split(" - ")[1] if " - " in cat else cat
        c1 = colors_owasp[idx % len(colors_owasp)]
        c2 = light_owasp[idx % len(light_owasp)]
        lines.append(f'  <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.6rem;">')
        lines.append(f'    <div style="width:200px;font-size:0.8rem;color:#334155;font-weight:600;text-align:right;">{short_name}</div>')
        lines.append(f'    <div style="flex:1;background:#f1f5f9;border-radius:4px;height:24px;overflow:hidden;">')
        lines.append(f'      <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{c1},{c2});border-radius:4px;display:flex;align-items:center;padding-left:8px;font-size:0.75rem;color:white;font-weight:700;">{count}</div>')
        lines.append(f'    </div>')
        lines.append(f'  </div>')
    lines.append('</div>')
    lines.append("")

    # MITRE horizontal bar chart
    lines.append("### Top MITRE ATLAS Techniques")
    lines.append("")
    colors_mitre = ["#0f172a", "#1e293b", "#334155", "#475569", "#475569", "#64748b"]
    light_mitre = ["#334155", "#475569", "#64748b", "#94a3b8", "#94a3b8", "#94a3b8"]
    lines.append('<div style="margin:2rem 0;">')
    max_mitre = mitre_sorted[0][1] if mitre_sorted else 1
    for idx, (tech, count) in enumerate(mitre_sorted[:6]):
        pct = round(100 * count / max_mitre)
        short_name = tech.split(" - ")[1] if " - " in tech else tech
        if len(short_name) > 24:
            short_name = short_name[:22] + "..."
        c1 = colors_mitre[idx % len(colors_mitre)]
        c2 = light_mitre[idx % len(light_mitre)]
        lines.append(f'  <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.6rem;">')
        lines.append(f'    <div style="width:200px;font-size:0.8rem;color:#334155;font-weight:600;text-align:right;">{short_name}</div>')
        lines.append(f'    <div style="flex:1;background:#f1f5f9;border-radius:4px;height:24px;overflow:hidden;">')
        lines.append(f'      <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{c1},{c2});border-radius:4px;display:flex;align-items:center;padding-left:8px;font-size:0.75rem;color:white;font-weight:700;">{count}</div>')
        lines.append(f'    </div>')
        lines.append(f'  </div>')
    lines.append('</div>')
    lines.append("")

    # Attack chain mermaid
    mermaid = narrative.get("attack_chain_mermaid", "")
    if mermaid:
        lines.append("### Dominant Attack Chain")
        lines.append("")
        lines.append("```mermaid")
        lines.append(mermaid)
        lines.append("```")
        lines.append("")

    # Threat actor attribution cards
    lines.append("### Threat Actor Attribution")
    lines.append("")
    lines.append('<div style="display:flex; gap:1rem; margin:2rem 0; flex-wrap:wrap;">')
    actor_colors = {"cybercriminal": "#dc2626", "researcher": "#6366f1", "nation-state": "#ea580c", "insider": "#f59e0b"}
    max_actor = max(actors.values()) if actors else 1
    for actor, count in sorted(actors.items(), key=lambda x: x[1], reverse=True):
        color = actor_colors.get(actor, "#64748b")
        pct = round(100 * count / max_actor)
        lines.append(f'  <div style="flex:1;min-width:140px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:1.25rem;text-align:center;">')
        lines.append(f'    <div style="font-size:2rem;font-weight:800;color:#0f172a;">{count}</div>')
        lines.append(f'    <div style="font-size:0.8rem;color:#64748b;font-weight:600;">{actor.title()}</div>')
        lines.append(f'    <div style="width:100%;height:4px;background:#e2e8f0;border-radius:2px;margin-top:0.5rem;"><div style="width:{pct}%;height:100%;background:{color};border-radius:2px;"></div></div>')
        lines.append(f'  </div>')
    lines.append('</div>')
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 3: Top Developments ──
    lines.append("## 3. Top Developments — Ranked by Business Impact")
    lines.append("")
    for dev in narrative.get("top_developments", []):
        lines.append(f"### {dev.get('rank', '')}. {dev['headline']}")
        lines.append("")
        what = dev.get("what_happened", "")
        for s in dev.get("article_slugs", []):
            what = what.replace(s, f"[{s}](/posts/{s}/)")
        lines.append(f"**What happened:** {what}")
        lines.append("")
        lines.append(f"**Board-level implication:** {dev.get('board_implication', '')}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 4: AI Threat Landscape ──
    lines.append("## 4. AI Threat Landscape")
    lines.append("")
    landscape = narrative.get("ai_threat_landscape", {})
    for section_key, section_title in [("attacks_using_ai", "Attacks Using AI"), ("attacks_on_ai", "Attacks on AI Systems"), ("governance_incidents", "AI Governance and Compliance")]:
        lines.append(f"### {section_title}")
        lines.append("")
        text = landscape.get(section_key, "")
        lines.append(text)
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 5: Threat Actor Spotlight ──
    lines.append("## 5. Threat Actor Spotlight")
    lines.append("")
    for actor in narrative.get("threat_actor_spotlight", []):
        lines.append(f"### {actor['name']}")
        lines.append("")
        lines.append(f"**Motivation:** {actor.get('motivation', '')}")
        lines.append(f"**Target sectors:** {', '.join(actor.get('target_sectors', []))}")
        lines.append(f"**AI adoption:** {actor.get('ai_adoption', '')}")
        lines.append("")
        lines.append(f"**What's changed:** {actor.get('whats_changed', '')}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 6: Critical Vulnerabilities ──
    lines.append("## 6. Critical Vulnerabilities")
    lines.append("")
    lines.append("| CVE | Affected Product | CVSS | Exploitation Status | Patch Status |")
    lines.append("|-----|-----------------|------|-------------------|-------------|")
    for a in cve_articles[:10]:
        cve_id = a["slug"].split("-", 1)
        cve_match = re.search(r'(CVE-\d{4}-\d+)', a["title"], re.IGNORECASE)
        cve_name = cve_match.group(1) if cve_match else a["title"][:30]
        product = a["title"].replace(cve_name, "").strip(": -–—")
        if not product:
            product = a["source"]
        lines.append(f"| [{cve_name}](/posts/{a['slug']}/) | {product[:35]} | — | {a['threat_level']} | — |")
    lines.append("")

    # CVSS bar chart
    if cve_articles:
        lines.append("### CVE Severity Overview")
        lines.append("")
        lines.append('<div style="margin:2rem 0;">')
        for a in cve_articles[:10]:
            cve_match = re.search(r'(CVE-\d{4}-\d+)', a["title"], re.IGNORECASE)
            cve_name = cve_match.group(1) if cve_match else a["slug"][:20]
            score = a["relevance_score"]
            pct = round(score * 10)
            color = "#dc2626" if score >= 9 else "#ea580c" if score >= 8 else "#f59e0b"
            lines.append(f'  <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">')
            lines.append(f'    <div style="width:160px;font-size:0.75rem;color:#334155;font-weight:600;text-align:right;">{cve_name}</div>')
            lines.append(f'    <div style="flex:1;background:#f1f5f9;border-radius:3px;height:20px;overflow:hidden;">')
            lines.append(f'      <div style="width:{pct}%;height:100%;background:{color};border-radius:3px;display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-size:0.7rem;color:white;font-weight:700;">{score}</div>')
            lines.append(f'    </div>')
            lines.append(f'  </div>')
        lines.append('</div>')
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Section 7: Regulatory Watch ──
    lines.append("## 7. Regulatory and Policy Watch")
    lines.append("")
    for item in narrative.get("regulatory_watch", []):
        lines.append(f"**{item['headline']}** {item.get('analysis', '')}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 8: Trends to Watch ──
    lines.append("## 8. Trends to Watch")
    lines.append("")
    for trend in narrative.get("trends_to_watch", []):
        lines.append(f"### {trend['headline']}")
        lines.append("")
        lines.append(trend.get("analysis", ""))
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 9: About This Report ──
    lines.append("## 9. About This Report")
    lines.append("")
    lines.append(f"**Data sources:** {total} articles published on Grid the Grey between 1–{month_label.split()[0]} {year}, cross-referenced with NVD/CISA KEV for vulnerability data and MITRE ATLAS for technique classification.")
    lines.append("")
    lines.append(f"**Classification coverage:** {len(mitre)} unique MITRE ATLAS techniques mapped, {len(owasp)} OWASP LLM Top 10 categories referenced. Top technique: {mitre_sorted[0][0] if mitre_sorted else 'N/A'} at {mitre_sorted[0][1] if mitre_sorted else 0} occurrences. Top OWASP category: {owasp_sorted[0][0] if owasp_sorted else 'N/A'} at {owasp_sorted[0][1] if owasp_sorted else 0} occurrences.")
    lines.append("")
    actor_summary = ", ".join([f"{c} {a}" for a, c in sorted(actors.items(), key=lambda x: x[1], reverse=True)])
    lines.append(f"**Threat actor attribution:** {actor_summary}.")
    lines.append("")
    lines.append(f"**Model:** This report's narrative analysis was produced using {NARRATIVE_MODEL} with supporting tasks on {SUPPORT_MODEL}.")
    lines.append("")
    lines.append(narrative.get("methodology_note", ""))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*This is Grid the Grey's Monthly Intelligence Review for {month_label}. It is designed for CISOs, security architects, and board-level decision makers who need strategic context on how the AI security landscape is evolving. [Subscribe to Deep Signal](/deep-signal/) for weekly tactical intelligence and monthly strategic reviews.*")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate monthly AI security intelligence review")
    parser.add_argument("--generate", action="store_true", help="Generate the monthly review")
    parser.add_argument("--dry-run", action="store_true", help="Print analytics only")
    parser.add_argument("--month", type=str, help="Month to review (YYYY-MM), default: previous month")
    parser.add_argument("--linkedin", action="store_true", help="Also generate LinkedIn post")
    parser.add_argument("--draft", action="store_true", help="Generate as Hugo draft")
    args = parser.parse_args()

    # Determine target month
    if args.month:
        year, month = map(int, args.month.split("-"))
    else:
        today = datetime.now(timezone.utc)
        first_of_month = today.replace(day=1)
        prev_month = first_of_month - timedelta(days=1)
        year, month = prev_month.year, prev_month.month

    month_name = datetime(year, month, 1).strftime("%B")
    month_label = f"{month_name} {year}"
    log.info(f"Monthly Review: {month_label}")

    # Read articles
    articles = get_monthly_articles(year, month)
    if not articles:
        log.error(f"No articles found for {month_label}")
        sys.exit(1)

    # Compute analytics
    analytics = compute_analytics(articles)
    log.info(f"  Analytics: {analytics['article_count']} articles, avg relevance {analytics['avg_relevance']}")
    log.info(f"  Threat levels: {json.dumps(analytics['threat_level_distribution'])}")

    if args.dry_run:
        print(json.dumps(analytics, indent=2, default=str))
        return

    if not args.generate:
        parser.print_help()
        return

    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY not set in environment or .env")
        sys.exit(1)

    # Generate narrative via Opus 5
    narrative = generate_narrative(articles, analytics, month_label)

    # Build Hugo article
    hugo_md = build_hugo_article(narrative, analytics, articles, year, month)

    # Set draft if requested
    if args.draft:
        hugo_md = hugo_md.replace("draft: false", "draft: true")

    # Write Hugo article
    slug = f"monthly-review-{month_name.lower()}-{year}"
    out_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = DEEP_SIGNAL_DIR / f"{out_date}-{slug}.md"
    out_path.write_text(hugo_md, encoding="utf-8")
    log.info(f"  Wrote: {out_path}")

    # Generate LinkedIn post
    if args.linkedin:
        linkedin_text = generate_linkedin_post(narrative, analytics, month_label)
        linkedin_path = REPORTS_DIR / f"linkedin-monthly-{month_name.lower()}-{year}.txt"
        linkedin_path.write_text(linkedin_text, encoding="utf-8")
        log.info(f"  Wrote: {linkedin_path}")

    log.info("Done.")


if __name__ == "__main__":
    main()
