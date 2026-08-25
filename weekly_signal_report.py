#!/usr/bin/env python3
"""
weekly_signal_report.py — Grid the Grey Weekly AI Security Intelligence Report
================================================================================
Generates a comprehensive weekly signal report analysing threat trends, MITRE ATLAS
technique frequency, OWASP LLM Top 10 distribution, threat actor activity, and
attack chain patterns. Output is a publication-ready Hugo markdown article for the
Deep Signal section, enriched with inline SVG heatmaps and embedded chart data.

WORKFLOW
--------
Step 1 — Generate the full signal report:
    python weekly_signal_report.py --generate

    Reads published posts from the last 7 days, computes analytics across MITRE,
    OWASP, threat level, and threat actor dimensions, loads historical data for
    week-over-week comparison, calls Claude to synthesise an executive narrative,
    and produces a Hugo markdown article at:
        hugo-site/content/deep-signal/YYYY-MM-DD-weekly-signal-report-YYYY-wNN.md

    Also appends the current week's data to signal-reports/history.json for
    future trend analysis.

PROOFREADING WORKFLOW
---------------------
    python weekly_signal_report.py --generate --draft   # Generate as draft
    cd hugo-site && hugo server --buildDrafts           # Preview locally
    # Open http://localhost:1313/deep-signal/weekly-signal-report-YYYYwNN/
    # Review headline, charts, mermaid diagram, article links
    python weekly_signal_report.py --publish weekly-signal-report-2026w31  # Publish

OTHER COMMANDS
--------------
    python weekly_signal_report.py --list            # List existing signal reports
    python weekly_signal_report.py --days 14         # Override lookback period
    python weekly_signal_report.py --dry-run         # Print analytics without generating article
    python weekly_signal_report.py --linkedin        # Generate LinkedIn post from latest report

REQUIREMENTS
------------
    pip install anthropic python-dotenv
    .env must contain: ANTHROPIC_API_KEY
    Optional: CLAUDE_MODEL (default: claude-sonnet-4-6)

HISTORY FILE
------------
    signal-reports/history.json tracks weekly distributions for trend analysis.
    Created automatically on first run.
"""

import argparse
import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.offsetbox import AnchoredText
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Config ────────────────────────────────────────────────────────────────────
POSTS_DIR        = Path(__file__).parent / "hugo-site" / "content" / "posts"
DEEP_SIGNAL_DIR  = Path(__file__).parent / "hugo-site" / "content" / "deep-signal"
HISTORY_DIR      = Path(__file__).parent / "signal-reports"
HISTORY_FILE     = HISTORY_DIR / "history.json"
DEFAULT_DAYS     = 7

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

# Threat level severity mapping
THREAT_SEVERITY = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "NONE": 0,
}

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("signal_report")


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
    body = body_match.group(1).strip()[:1200] if body_match else ""

    return {
        "title":            _fm_value(text, "title"),
        "summary":          _fm_value(text, "summary"),
        "source":           _fm_value(text, "source"),
        "source_url":       _fm_value(text, "source_url"),
        "threat_level":     _fm_value(text, "threat_level").upper(),
        "relevance_score":  score,
        "categories":       _fm_list(text, "categories"),
        "tags":             _fm_list(text, "tags"),
        "mitre_techniques": _fm_list(text, "mitre_techniques"),
        "owasp_categories": _fm_list(text, "owasp_categories"),
        "threat_actors":    _fm_list(text, "threat_actors"),
        "content_type":     _fm_value(text, "content_type"),
        "date":             date,
        "body_excerpt":     body,
    }


# ── Article reader ────────────────────────────────────────────────────────────
def get_articles(days: int = DEFAULT_DAYS) -> list:
    """
    Return ALL published posts from the last N days, sorted by relevance_score desc.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    articles = []

    if not POSTS_DIR.exists():
        log.error(f"Posts directory not found: {POSTS_DIR}")
        return []

    for path in POSTS_DIR.glob("*.md"):
        if path.name == "_index.md":
            continue
        post = parse_post(path)
        if post and post["date"] >= cutoff and post["title"]:
            articles.append(post)

    articles.sort(key=lambda a: a["relevance_score"], reverse=True)
    log.info(f"  Found {len(articles)} articles in last {days} days")
    return articles


# ── Analytics computation ─────────────────────────────────────────────────────
def compute_analytics(articles: list) -> dict:
    """
    Compute all frequency distributions and summary statistics from articles.
    Returns a comprehensive analytics dict.
    """
    mitre_counter = Counter()
    owasp_counter = Counter()
    threat_level_counter = Counter()
    threat_actor_counter = Counter()
    category_counter = Counter()
    tag_counter = Counter()

    # For average severity per OWASP category and MITRE technique
    owasp_severity_totals = defaultdict(list)
    mitre_severity_totals = defaultdict(list)

    # For average relevance per OWASP category and MITRE technique
    owasp_relevance_totals = defaultdict(list)
    mitre_relevance_totals = defaultdict(list)

    # For attack chain analysis (co-occurrence of MITRE techniques)
    mitre_cooccurrence = Counter()

    total_relevance = 0.0

    for article in articles:
        # MITRE techniques
        for tech in article["mitre_techniques"]:
            mitre_counter[tech] += 1
            severity = THREAT_SEVERITY.get(article["threat_level"], 0)
            mitre_severity_totals[tech].append(severity)
            mitre_relevance_totals[tech].append(article["relevance_score"])

        # OWASP categories
        for cat in article["owasp_categories"]:
            owasp_counter[cat] += 1
            severity = THREAT_SEVERITY.get(article["threat_level"], 0)
            owasp_severity_totals[cat].append(severity)
            owasp_relevance_totals[cat].append(article["relevance_score"])

        # Threat level
        if article["threat_level"]:
            threat_level_counter[article["threat_level"]] += 1

        # Threat actors
        for actor in article["threat_actors"]:
            threat_actor_counter[actor] += 1

        # Categories
        for cat in article["categories"]:
            category_counter[cat] += 1

        # Tags
        for tag in article["tags"]:
            tag_counter[tag] += 1

        # Relevance
        total_relevance += article["relevance_score"]

        # MITRE co-occurrence (pairs)
        techniques = article["mitre_techniques"]
        for i in range(len(techniques)):
            for j in range(i + 1, len(techniques)):
                pair = tuple(sorted([techniques[i], techniques[j]]))
                mitre_cooccurrence[pair] += 1

    # Compute average severity per OWASP category
    owasp_avg_severity = {}
    for cat, severities in owasp_severity_totals.items():
        owasp_avg_severity[cat] = round(sum(severities) / len(severities), 2) if severities else 0

    # Compute average severity per MITRE technique
    mitre_avg_severity = {}
    for tech, severities in mitre_severity_totals.items():
        mitre_avg_severity[tech] = round(sum(severities) / len(severities), 2) if severities else 0

    # Compute average relevance per OWASP category
    owasp_avg_relevance = {}
    for cat, scores in owasp_relevance_totals.items():
        owasp_avg_relevance[cat] = round(sum(scores) / len(scores), 2) if scores else 0

    # Compute average relevance per MITRE technique
    mitre_avg_relevance = {}
    for tech, scores in mitre_relevance_totals.items():
        mitre_avg_relevance[tech] = round(sum(scores) / len(scores), 2) if scores else 0

    avg_relevance = round(total_relevance / len(articles), 2) if articles else 0

    return {
        "article_count": len(articles),
        "avg_relevance": avg_relevance,
        "mitre_distribution": dict(mitre_counter.most_common()),
        "owasp_distribution": dict(owasp_counter.most_common()),
        "owasp_avg_severity": owasp_avg_severity,
        "mitre_avg_severity": mitre_avg_severity,
        "owasp_avg_relevance": owasp_avg_relevance,
        "mitre_avg_relevance": mitre_avg_relevance,
        "threat_level_distribution": dict(threat_level_counter.most_common()),
        "threat_actor_distribution": dict(threat_actor_counter.most_common()),
        "category_distribution": dict(category_counter.most_common()),
        "tag_distribution": dict(tag_counter.most_common(30)),
        "mitre_cooccurrence": {f"{a} + {b}": count for (a, b), count in mitre_cooccurrence.most_common(15)},
        "top_categories": [cat for cat, _ in category_counter.most_common(10)],
    }


# ── History management ────────────────────────────────────────────────────────
def load_history() -> dict:
    """Load signal-reports/history.json or return empty structure."""
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if "weeks" in data:
                return data
        except (json.JSONDecodeError, Exception) as e:
            log.warning(f"  Could not parse history.json: {e}. Starting fresh.")
    return {"weeks": []}


def save_history(history: dict) -> None:
    """Save updated history to disk."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info(f"  History saved: {HISTORY_FILE}")


def get_previous_week(history: dict) -> dict | None:
    """Return the most recent week entry from history, or None."""
    if history["weeks"]:
        return history["weeks"][-1]
    return None


def compute_week_over_week(current: dict, previous: dict | None) -> dict:
    """
    Compute week-over-week changes between current analytics and previous week.
    Returns a dict with percentage changes, new techniques, and disappeared techniques.
    """
    if not previous:
        return {
            "has_comparison": False,
            "note": "No prior week data available for comparison.",
        }

    prev_mitre = previous.get("mitre_distribution", {})
    curr_mitre = current["mitre_distribution"]

    prev_owasp = previous.get("owasp_distribution", {})
    curr_owasp = current["owasp_distribution"]

    # New techniques (in current but not in previous)
    new_techniques = [t for t in curr_mitre if t not in prev_mitre]

    # Disappeared techniques (in previous but not in current)
    disappeared_techniques = [t for t in prev_mitre if t not in curr_mitre]

    # Percentage changes for MITRE techniques
    mitre_changes = {}
    for tech, count in curr_mitre.items():
        prev_count = prev_mitre.get(tech, 0)
        if prev_count > 0:
            pct_change = round(((count - prev_count) / prev_count) * 100, 1)
        else:
            pct_change = None  # New technique
        mitre_changes[tech] = {
            "current": count,
            "previous": prev_count,
            "pct_change": pct_change,
        }

    # Percentage changes for OWASP categories
    owasp_changes = {}
    for cat, count in curr_owasp.items():
        prev_count = prev_owasp.get(cat, 0)
        if prev_count > 0:
            pct_change = round(((count - prev_count) / prev_count) * 100, 1)
        else:
            pct_change = None
        owasp_changes[cat] = {
            "current": count,
            "previous": prev_count,
            "pct_change": pct_change,
        }

    # Article count change
    prev_article_count = previous.get("article_count", 0)
    article_count_change = current["article_count"] - prev_article_count

    return {
        "has_comparison": True,
        "mitre_changes": mitre_changes,
        "owasp_changes": owasp_changes,
        "new_techniques": new_techniques,
        "disappeared_techniques": disappeared_techniques,
        "article_count_change": article_count_change,
        "prev_article_count": prev_article_count,
        "prev_avg_relevance": previous.get("avg_relevance", 0),
    }


# ── Claude API narrative generation ──────────────────────────────────────────
def build_claude_context(articles: list, analytics: dict, wow: dict) -> str:
    """Build a comprehensive context block for the Claude narrative generation prompt."""
    lines = []

    # Summary statistics
    lines.append("=== WEEKLY STATISTICS ===")
    lines.append(f"Total articles: {analytics['article_count']}")
    lines.append(f"Average relevance score: {analytics['avg_relevance']}/10")
    lines.append(f"Threat level breakdown: {json.dumps(analytics['threat_level_distribution'])}")
    lines.append("")

    # MITRE distribution
    lines.append("=== MITRE ATLAS TECHNIQUE DISTRIBUTION ===")
    for tech, count in sorted(analytics["mitre_distribution"].items(), key=lambda x: x[1], reverse=True)[:20]:
        lines.append(f"  {tech}: {count} occurrences")
    lines.append("")

    # OWASP distribution
    lines.append("=== OWASP LLM TOP 10 DISTRIBUTION ===")
    for cat, count in sorted(analytics["owasp_distribution"].items(), key=lambda x: x[1], reverse=True):
        avg_sev = analytics["owasp_avg_severity"].get(cat, 0)
        lines.append(f"  {cat}: {count} occurrences (avg severity: {avg_sev}/4)")
    lines.append("")

    # Threat actors
    lines.append("=== THREAT ACTOR DISTRIBUTION ===")
    for actor, count in sorted(analytics["threat_actor_distribution"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {actor}: {count} mentions")
    lines.append("")

    # Category distribution
    lines.append("=== CATEGORY DISTRIBUTION ===")
    for cat, count in sorted(analytics["category_distribution"].items(), key=lambda x: x[1], reverse=True)[:15]:
        lines.append(f"  {cat}: {count}")
    lines.append("")

    # Attack chain co-occurrence
    lines.append("=== MITRE TECHNIQUE CO-OCCURRENCE (Attack Chain Patterns) ===")
    for pair, count in sorted(analytics["mitre_cooccurrence"].items(), key=lambda x: x[1], reverse=True)[:10]:
        lines.append(f"  {pair}: {count} co-occurrences")
    lines.append("")

    # Week-over-week changes
    if wow.get("has_comparison"):
        lines.append("=== WEEK-OVER-WEEK CHANGES ===")
        lines.append(f"Article count change: {wow['article_count_change']:+d} (was {wow['prev_article_count']}, now {analytics['article_count']})")
        lines.append(f"Previous avg relevance: {wow['prev_avg_relevance']}, current: {analytics['avg_relevance']}")

        if wow.get("new_techniques"):
            lines.append(f"\nNEW techniques this week (not seen last week):")
            for t in wow["new_techniques"][:10]:
                lines.append(f"  + {t}")

        if wow.get("disappeared_techniques"):
            lines.append(f"\nDISAPPEARED techniques (present last week, absent now):")
            for t in wow["disappeared_techniques"][:10]:
                lines.append(f"  - {t}")

        lines.append("\nMITRE technique changes (% change):")
        for tech, data in sorted(
            wow.get("mitre_changes", {}).items(),
            key=lambda x: abs(x[1].get("pct_change", 0) or 0),
            reverse=True,
        )[:10]:
            if data["pct_change"] is not None:
                lines.append(f"  {tech}: {data['pct_change']:+.1f}% ({data['previous']} -> {data['current']})")
            else:
                lines.append(f"  {tech}: NEW ({data['current']} this week)")
        lines.append("")
    else:
        lines.append("=== WEEK-OVER-WEEK CHANGES ===")
        lines.append("No prior week data available. This is the first signal report.")
        lines.append("")

    # Top articles with summaries
    lines.append("=== TOP ARTICLES THIS WEEK (by relevance) ===")
    for i, article in enumerate(articles[:20], 1):
        lines.append(f"\n--- Article {i} ---")
        lines.append(f"Title: {article['title']}")
        lines.append(f"Date: {article['date'].strftime('%Y-%m-%d')}")
        lines.append(f"Source: {article['source']}")
        lines.append(f"Threat Level: {article['threat_level']} | Relevance: {article['relevance_score']}/10")
        if article["mitre_techniques"]:
            lines.append(f"MITRE: {', '.join(article['mitre_techniques'][:4])}")
        if article["owasp_categories"]:
            lines.append(f"OWASP: {', '.join(article['owasp_categories'][:3])}")
        if article["threat_actors"]:
            lines.append(f"Threat Actors: {', '.join(article['threat_actors'])}")
        if article["categories"]:
            lines.append(f"Categories: {', '.join(article['categories'][:4])}")
        lines.append(f"Summary: {article['summary'][:500]}")

    return "\n".join(lines)


def generate_narrative(articles: list, analytics: dict, wow: dict, week_label: str) -> dict:
    """
    Call Claude API to generate the executive narrative sections.
    Returns a dict with keys: executive_summary, enterprise_focus, trajectory_watch,
    blind_spots, attack_chain_analysis, readiness_score, geographic_sector_analysis.
    """
    context = build_claude_context(articles, analytics, wow)
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    prompt = f"""You are a senior AI security intelligence analyst producing the weekly "Deep Signal" report for Grid the Grey, a publication read by CISOs, security architects, and AI governance leaders.

Today's date: {now_str}
Report period: {week_label}

Below is the complete analytics data and article summaries for this week:

{context}

Based on this data, generate a comprehensive intelligence report with the following sections. Output ONLY valid JSON with these exact keys:

{{
  "headline": "A catchy, concise headline (max 12 words) that captures the week's dominant theme — like a newspaper headline. Example: 'AI Goes Offensive: From Research to Real-World Attacks'. Do NOT include the week number.",
  "story_hook": "2-3 short paragraphs (max 200 words total) that open the report like a compelling intelligence briefing. Lead with the 2-3 most significant stories of the week — name the events, the actors, and why they matter. This should read like the opening of a Reuters or Bloomberg intelligence report: punchy, specific, immediately grabs a senior security leader's attention. Reference specific article titles and findings. End with a single sentence framing what the rest of the report will unpack.",
  "executive_summary": "2 short paragraphs (max 120 words total) analysing this week's dominant themes and what's shifting. Be specific — reference technique IDs and findings. No filler.",
  "wow_persisting": "2-3 sentences about MITRE techniques that persist from the prior week. Name the techniques with their IDs, explain WHY they continue to dominate and what it means for defenders. Example: 'AML.T0051 (Prompt Injection), AML.T0047 (ML-Enabled Product), AML.T0057 (Data Leakage) continue to dominate for the second consecutive week, indicating sustained adversary focus on these attack vectors.' If no prior week data is available, write 'First report — baseline established this week.'",
  "wow_emerging": "1-2 sentences about MITRE techniques that appeared THIS week but were NOT present last week. Name them with IDs, explain what triggered their appearance and the risk implication. If none emerged, write 'No new techniques observed this week.'",
  "wow_dropped": "1-2 sentences about MITRE techniques present last week but absent this week. Explain whether this represents a tactical pivot, seasonal variation, or resolution. If none dropped, write 'All prior techniques remain active.'",
  "enterprise_focus": ["3-4 bullet points for CISOs. One sentence each — concrete and specific to THIS week's data."],
  "trajectory_watch": "1 short paragraph (max 80 words) on the 4-8 week outlook. What should security teams prepare for?",
  "attack_chain_analysis": "1 short paragraph (max 80 words) on how MITRE ATLAS techniques chain together this week. Reference specific technique pairs from the co-occurrence data.",
  "attack_chain_mermaid": "A Mermaid flowchart diagram (flowchart TD — top to bottom) showing the dominant attack chain patterns. Use subgraphs for 'Initial Access', 'Exploitation', and 'Impact'. Nodes should use MITRE technique IDs with brief labels (e.g. T0047[AML.T0047<br/>ML-Enabled Product]). Edges should have short descriptive labels. Keep it to 4-6 nodes maximum for readability. Output ONLY the mermaid code, no code fences.",
  "readiness_score": "1 short paragraph (max 60 words) with an enterprise readiness grade (A-F) and 1-2 sentence justification.",
  "geographic_sector_analysis": "1 short paragraph (max 60 words) on geographic and sector targeting patterns this week."
}}

IMPORTANT:
- Be analytically rigorous. The audience is senior security leadership — they detect fluff instantly.
- Ground every assertion in the data provided. Do not hallucinate statistics or trends.
- Use framework language (MITRE ATLAS technique IDs, OWASP LLM category codes) precisely.
- The "so what" must be clear: what does this mean for an enterprise security programme?
- Write in British English spelling (analyse, defence, organisation, etc.)
- BREVITY IS CRITICAL: the total article (excluding story_hook) must fit in a 5-minute read (~800-1000 words). Every section has a word cap — respect them strictly. No padding, no filler sentences.
- Output ONLY the JSON object. No markdown code fences, no preamble."""

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    log.info("  Calling Claude for narrative generation...")

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    # Strip any markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r'^```(?:json)?\s*\n?', '', raw_text)
        raw_text = re.sub(r'\n?```\s*$', '', raw_text)

    try:
        narrative = json.loads(raw_text)
    except json.JSONDecodeError as e:
        log.error(f"  Failed to parse Claude response as JSON: {e}")
        log.error(f"  Raw response (first 500 chars): {raw_text[:500]}")
        # Attempt a more aggressive extraction
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            try:
                narrative = json.loads(json_match.group())
            except json.JSONDecodeError:
                log.error("  Could not extract JSON from Claude response. Using fallback.")
                narrative = {
                    "executive_summary": "Analysis generation failed. Please review raw analytics data below.",
                    "enterprise_focus": ["Review the analytics data manually and assess organisational impact."],
                    "trajectory_watch": "Insufficient data for trajectory analysis.",
                    "blind_spots": "Unable to generate blind spot analysis.",
                    "attack_chain_analysis": "Unable to generate attack chain analysis.",
                    "readiness_score": "Unable to assess readiness.",
                    "geographic_sector_analysis": "Unable to assess geographic patterns.",
                }
        else:
            narrative = {
                "executive_summary": "Analysis generation failed. Please review raw analytics data below.",
                "enterprise_focus": ["Review the analytics data manually and assess organisational impact."],
                "trajectory_watch": "Insufficient data for trajectory analysis.",
                "blind_spots": "Unable to generate blind spot analysis.",
                "attack_chain_analysis": "Unable to generate attack chain analysis.",
                "readiness_score": "Unable to assess readiness.",
                "geographic_sector_analysis": "Unable to assess geographic patterns.",
            }

    log.info("  Narrative generated successfully")
    return narrative


# ── Geographic and sector inference ──────────────────────────────────────────
# Mapping of keywords to geographic regions with coordinates
GEO_REGIONS = {
    "Asia-Pacific": {
        "keywords": ["thai", "thailand", "asia", "china", "chinese", "japan", "japanese",
                     "india", "indian", "apac", "korea", "korean", "singapore", "vietnam",
                     "indonesia", "malaysia", "taiwan", "philippines", "australia"],
        "coords": {"thai": (13.7, 100.5), "thailand": (13.7, 100.5),
                   "japan": (35.6, 139.7), "japanese": (35.6, 139.7),
                   "china": (39.9, 116.4), "chinese": (39.9, 116.4),
                   "india": (28.6, 77.2), "indian": (28.6, 77.2),
                   "korea": (37.5, 127.0), "korean": (37.5, 127.0),
                   "singapore": (1.3, 103.8), "taiwan": (25.0, 121.5),
                   "australia": (-33.8, 151.2)},
        "default_coords": (13.7, 100.5),
    },
    "North America": {
        "keywords": ["us", "united states", "america", "american", "silicon valley",
                     "california", "canada", "canadian", "washington", "new york"],
        "coords": {"california": (37.7, -122.4), "silicon valley": (37.4, -122.0),
                   "new york": (40.7, -74.0), "washington": (38.9, -77.0),
                   "canada": (43.6, -79.4), "canadian": (43.6, -79.4)},
        "default_coords": (37.7, -122.4),
    },
    "Europe": {
        "keywords": ["europe", "european", "eu", "uk", "british", "germany", "german",
                     "france", "french", "netherlands", "dutch", "spain", "italy",
                     "sweden", "switzerland"],
        "coords": {"uk": (51.5, -0.1), "british": (51.5, -0.1),
                   "germany": (52.5, 13.4), "german": (52.5, 13.4),
                   "france": (48.9, 2.3), "french": (48.9, 2.3),
                   "netherlands": (52.4, 4.9), "dutch": (52.4, 4.9),
                   "sweden": (59.3, 18.1), "switzerland": (46.9, 7.4)},
        "default_coords": (51.5, -0.1),
    },
    "Middle East": {
        "keywords": ["middle east", "israel", "israeli", "iran", "iranian", "saudi",
                     "uae", "dubai"],
        "coords": {"israel": (31.8, 35.2), "israeli": (31.8, 35.2),
                   "iran": (35.7, 51.4), "iranian": (35.7, 51.4),
                   "saudi": (24.7, 46.7), "uae": (25.2, 55.3), "dubai": (25.2, 55.3)},
        "default_coords": (31.8, 35.2),
    },
}

# Mapping of keywords to sectors
SECTOR_KEYWORDS = {
    "Finance": ["finance", "financial", "banking", "bank", "treasury", "fintech",
                "payment", "crypto", "cryptocurrency"],
    "Government": ["government", "ministry", "nation-state", "federal", "military",
                   "defense", "defence", "policy", "regulation", "regulatory"],
    "Healthcare": ["healthcare", "medical", "health", "hospital", "pharma",
                   "pharmaceutical", "clinical"],
    "Education": ["education", "university", "academic", "research university",
                  "school"],
    "Energy": ["energy", "oil", "gas", "utility", "utilities", "power grid",
               "nuclear"],
    "Technology": ["technology", "tech", "software", "ai", "ml", "cloud",
                   "saas", "llm", "model", "developer", "open source"],
}


def infer_geography(articles: list) -> list:
    """
    Infer geographic distribution from article content (tags, summary, source).
    Returns a list of dicts with region, lat, lng, events, label.
    """
    geo_events = defaultdict(lambda: {"events": 0, "labels": [], "lat": 0, "lng": 0})

    for article in articles:
        searchable = " ".join([
            article.get("summary", ""),
            " ".join(article.get("tags", [])),
            article.get("source", ""),
            article.get("title", ""),
        ]).lower()

        matched_region = None
        matched_keyword = None

        for region, config in GEO_REGIONS.items():
            for keyword in config["keywords"]:
                if keyword in searchable:
                    matched_region = region
                    matched_keyword = keyword
                    break
            if matched_region:
                break

        if matched_region:
            coords = GEO_REGIONS[matched_region]["coords"].get(
                matched_keyword, GEO_REGIONS[matched_region]["default_coords"]
            )
            geo_events[matched_region]["events"] += 1
            geo_events[matched_region]["lat"] = coords[0]
            geo_events[matched_region]["lng"] = coords[1]
            # Collect a label from the article title (keep first few unique)
            title_short = article["title"][:50]
            if len(geo_events[matched_region]["labels"]) < 3:
                geo_events[matched_region]["labels"].append(title_short)
        else:
            # Default: North America (most sources are US-based)
            geo_events["North America"]["events"] += 1
            geo_events["North America"]["lat"] = 37.7
            geo_events["North America"]["lng"] = -122.4

    # Build result list
    result = []
    for region, data in sorted(geo_events.items(), key=lambda x: x[1]["events"], reverse=True):
        label = data["labels"][0] if data["labels"] else f"{region} AI Security"
        result.append({
            "region": region,
            "lat": data["lat"],
            "lng": data["lng"],
            "events": data["events"],
            "label": label,
        })

    return result


def infer_sectors(articles: list) -> list:
    """
    Infer sector distribution from article content (categories, tags, summary).
    Returns a list of dicts with name and events count.
    """
    sector_counts = Counter()

    for article in articles:
        searchable = " ".join([
            " ".join(article.get("categories", [])),
            " ".join(article.get("tags", [])),
            article.get("summary", ""),
            article.get("title", ""),
        ]).lower()

        matched_sector = None

        # Check non-Technology sectors first (Technology is the default)
        for sector, keywords in SECTOR_KEYWORDS.items():
            if sector == "Technology":
                continue
            for keyword in keywords:
                if keyword in searchable:
                    matched_sector = sector
                    break
            if matched_sector:
                break

        if matched_sector:
            sector_counts[matched_sector] += 1
        else:
            # Default for most AI/ML articles
            sector_counts["Technology"] += 1

    # Build result list
    result = []
    for sector, count in sector_counts.most_common():
        result.append({"name": sector, "events": count})

    return result


# ── Chart image generation (matplotlib) ──────────────────────────────────────
CHART_OUTPUT_DIR = Path(__file__).parent / "hugo-site" / "static" / "img" / "signal"

OWASP_COLORS = {
    'LLM01': '#E63946', 'LLM02': '#2A9D8F', 'LLM03': '#6930C3', 'LLM04': '#F77F00',
    'LLM05': '#264653', 'LLM06': '#E76F51', 'LLM07': '#3B82F6', 'LLM08': '#D946EF',
    'LLM09': '#059669', 'LLM10': '#7C3AED'
}

MITRE_COLORS = [
    '#E63946', '#2A9D8F', '#F59E0B', '#7C3AED', '#059669', '#EC4899',
    '#3B82F6', '#D946EF', '#F97316', '#264653', '#06B6D4', '#DC2626',
    '#1D4ED8', '#16A34A', '#9333EA', '#CA8A04'
]


def generate_quadrant_chart(items: list, title: str, palette: dict | list, output_path: Path,
                            quadrant_labels: tuple = ('CRITICAL FOCUS', 'EMERGING RISK', 'TRENDING', 'MONITOR')) -> None:
    """Generate a polished quadrant bubble chart as PNG."""
    if not HAS_MATPLOTLIB:
        log.warning("  matplotlib not available — skipping chart generation")
        return

    fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=250)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.18)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFBFC')

    # Fixed axis ranges — consistent across all weekly reports so charts are comparable
    freqs = [item['frequency'] for item in items]
    rels = [item['relevance'] for item in items]
    # X: frequency — always 0 to at least 10, expanded if data exceeds it
    max_freq = max(max(freqs) * 1.2 if freqs else 10, 10)
    # Y: relevance — always 0–10 (the scoring scale)
    rel_min = 0
    rel_max = 10

    # Quadrant center — fixed midpoints for consistent quadrant placement
    mid_x = max_freq / 2
    mid_y = 5.0

    # Subtle quadrant tints
    ax.axhspan(mid_y, rel_max, xmin=0.5, xmax=1.0, alpha=0.07, color='#E63946', zorder=0)
    ax.axhspan(mid_y, rel_max, xmin=0.0, xmax=0.5, alpha=0.05, color='#F59E0B', zorder=0)
    ax.axhspan(rel_min, mid_y, xmin=0.5, xmax=1.0, alpha=0.04, color='#3B82F6', zorder=0)
    ax.axhspan(rel_min, mid_y, xmin=0.0, xmax=0.5, alpha=0.04, color='#10B981', zorder=0)

    # Quadrant dividers — dashed
    ax.axhline(y=mid_y, color='#94A3B8', linewidth=1, linestyle='--', alpha=0.6, zorder=2)
    ax.axvline(x=mid_x, color='#94A3B8', linewidth=1, linestyle='--', alpha=0.6, zorder=2)

    # Plot bubbles — size proportional to frequency
    placed = []
    for i, item in enumerate(items):
        if isinstance(palette, dict):
            color = palette.get(item['id'], '#4A6FA5')
        else:
            color = palette[i % len(palette)]

        size = 60 + item['frequency'] * 18
        ax.scatter(item['frequency'], item['relevance'], s=size,
                   c=color, alpha=0.85, edgecolors='white', linewidth=2, zorder=5)
        placed.append((item['frequency'], item['relevance']))

    # Labels with white halo — positioned to avoid dots
    for i, item in enumerate(items):
        lx, ly = item['frequency'], item['relevance']

        # Determine best offset direction
        offset_x, offset_y = 0, 10
        ha = 'center'

        # Check proximity to other points and nudge
        for j, (px, py) in enumerate(placed):
            if j == i:
                continue
            if abs(lx - px) < max_freq * 0.06 and abs(ly - py) < (rel_max - rel_min) * 0.05:
                offset_y += 8

        # If near right edge, shift label left
        if lx > max_freq * 0.8:
            offset_x = -10
            ha = 'right'
        elif lx < max_freq * 0.15:
            offset_x = 10
            ha = 'left'

        ax.annotate(item['id'], (lx, ly),
                    textcoords="offset points", xytext=(offset_x, offset_y),
                    ha=ha, fontsize=8.5, fontweight='bold', color='#1E293B',
                    fontfamily='monospace', zorder=8,
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                              edgecolor='none', alpha=0.85))

    # Axis config
    ax.set_xlim(0, max_freq)
    ax.set_ylim(rel_min, rel_max)
    ax.set_xlabel('Event Frequency', fontsize=11, fontfamily='monospace',
                  color='#334155', fontweight='bold', labelpad=10)
    ax.set_ylabel('Avg Relevance Score', fontsize=11, fontfamily='monospace',
                  color='#334155', fontweight='bold', labelpad=10)

    # Title
    ax.set_title(title, fontsize=14, fontweight='bold', fontfamily='monospace',
                 color='#0F172A', pad=16)

    # Quadrant labels — bold, positioned in quadrant interiors
    ql_props = dict(fontsize=9, fontfamily='monospace', fontweight='bold', alpha=0.5, zorder=1)
    ax.text(max_freq * 0.75, rel_max - (rel_max - rel_min) * 0.07, quadrant_labels[0],
            ha='center', color='#B91C1C', **ql_props)
    ax.text(max_freq * 0.25, rel_max - (rel_max - rel_min) * 0.07, quadrant_labels[1],
            ha='center', color='#D97706', **ql_props)
    ax.text(max_freq * 0.75, rel_min + (rel_max - rel_min) * 0.07, quadrant_labels[2],
            ha='center', color='#1D4ED8', **ql_props)
    ax.text(max_freq * 0.25, rel_min + (rel_max - rel_min) * 0.07, quadrant_labels[3],
            ha='center', color='#059669', **ql_props)

    # Light grid
    ax.grid(True, alpha=0.15, linewidth=0.5, color='#94A3B8')
    ax.tick_params(labelsize=9, colors='#475569', direction='out', length=4)
    for spine in ax.spines.values():
        spine.set_color('#CBD5E1')
        spine.set_linewidth(0.8)

    # Legend — fixed 2-column layout for clean vertical alignment
    legend_items = []
    for i, item in enumerate(items):
        if isinstance(palette, dict):
            color = palette.get(item['id'], '#4A6FA5')
        else:
            color = palette[i % len(palette)]
        legend_items.append(mpatches.Patch(color=color, label=f"{item['id']} {item['label']}"))

    ax.legend(handles=legend_items, loc='upper center', bbox_to_anchor=(0.5, -0.10),
              ncol=2, fontsize=7.5, frameon=False, prop={'family': 'monospace'})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, facecolor='#FFFFFF', edgecolor='none', bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    log.info(f"  Chart saved: {output_path}")


def generate_charts(analytics: dict, wow: dict, week_label: str) -> dict:
    """Generate all chart PNGs and return paths relative to /img/signal/."""
    week_lower = week_label.lower().replace("-", "")
    CHART_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    paths = {}

    # OWASP quadrant
    owasp_items = []
    for cat, count in sorted(analytics["owasp_distribution"].items(), key=lambda x: x[1], reverse=True):
        parts = cat.split(" - ", 1)
        cat_id = parts[0].strip() if parts else cat
        cat_label = parts[1].strip() if len(parts) > 1 else cat
        owasp_items.append({
            "id": cat_id, "label": cat_label,
            "frequency": count,
            "relevance": analytics["owasp_avg_relevance"].get(cat, 0),
        })

    owasp_path = CHART_OUTPUT_DIR / f"owasp-{week_lower}.png"
    generate_quadrant_chart(owasp_items, "OWASP LLM Top 10 — Threat Quadrant", OWASP_COLORS, owasp_path)
    paths["owasp"] = f"/img/signal/owasp-{week_lower}.png"

    # MITRE quadrant
    mitre_items = []
    for tech, count in sorted(analytics["mitre_distribution"].items(), key=lambda x: x[1], reverse=True)[:16]:
        parts = tech.split(" - ", 1)
        tech_id = parts[0].strip() if parts else tech
        tech_label = parts[1].strip() if len(parts) > 1 else tech
        mitre_items.append({
            "id": tech_id, "label": tech_label,
            "frequency": count,
            "relevance": analytics["mitre_avg_relevance"].get(tech, 0),
        })

    mitre_path = CHART_OUTPUT_DIR / f"mitre-{week_lower}.png"
    generate_quadrant_chart(mitre_items, "MITRE ATLAS — Technique Landscape", MITRE_COLORS, mitre_path)
    paths["mitre"] = f"/img/signal/mitre-{week_lower}.png"

    return paths


# ── Hugo markdown generation ──────────────────────────────────────────────────
def build_chart_data(analytics: dict, wow: dict, articles: list = None) -> dict:
    """
    Build the JSON data structure for interactive charts.
    Embedded in the markdown for the Hugo partial to read.
    Keys and field names must match hugo-site/layouts/partials/signal-charts.html expectations.
    """
    # OWASP quadrant: {id, label, frequency, relevance, change}
    owasp_quadrant = []
    for cat, count in sorted(analytics["owasp_distribution"].items(), key=lambda x: x[1], reverse=True):
        # Parse "LLM08 - Excessive Agency" into id="LLM08", label="Excessive Agency"
        parts = cat.split(" - ", 1)
        cat_id = parts[0].strip() if parts else cat
        cat_label = parts[1].strip() if len(parts) > 1 else cat

        change = 0.0
        if wow.get("has_comparison") and cat in wow.get("owasp_changes", {}):
            pct = wow["owasp_changes"][cat].get("pct_change")
            change = round(pct / 100, 2) if pct is not None else 0.0

        owasp_quadrant.append({
            "id": cat_id,
            "label": cat_label,
            "frequency": count,
            "relevance": analytics["owasp_avg_relevance"].get(cat, 0),
            "change": change,
        })

    # MITRE quadrant: {id, label, frequency, relevance, change} — same structure as OWASP
    mitre_quadrant = []
    for tech, count in sorted(analytics["mitre_distribution"].items(), key=lambda x: x[1], reverse=True)[:16]:
        parts = tech.split(" - ", 1)
        tech_id = parts[0].strip() if parts else tech
        tech_label = parts[1].strip() if len(parts) > 1 else tech

        change = 0.0
        if wow.get("has_comparison") and tech in wow.get("mitre_changes", {}):
            pct = wow["mitre_changes"][tech].get("pct_change")
            change = round(pct / 100, 2) if pct is not None else 0.0

        mitre_quadrant.append({
            "id": tech_id,
            "label": tech_label,
            "frequency": count,
            "relevance": analytics["mitre_avg_relevance"].get(tech, 0),
            "change": change,
        })

    # Determine dominant theme from top category
    top_cats = analytics.get("top_categories", [])
    dominant_theme = top_cats[0] if top_cats else "N/A"

    # Compute geographic and sector data
    geography = infer_geography(articles) if articles else []
    sectors = infer_sectors(articles) if articles else []

    return {
        "week": get_week_label(),
        "owasp_quadrant": owasp_quadrant,
        "mitre_quadrant": mitre_quadrant,
        "geography": geography,
        "sectors": sectors,
        "summary_stats": {
            "total_articles": analytics["article_count"],
            "avg_relevance": analytics["avg_relevance"],
            "threat_levels": analytics["threat_level_distribution"],
            "dominant_theme": dominant_theme,
        },
    }


def generate_hugo_article(
    analytics: dict,
    wow: dict,
    narrative: dict,
    articles: list,
    week_label: str,
    as_draft: bool = False,
) -> str:
    """
    Generate a complete Hugo markdown article for the Deep Signal section.
    Returns the full file content as a string.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    week_lower = week_label.lower().replace("-", "")  # e.g. "2026w31"

    # Reading time — target 5 minutes
    reading_time = 5

    # Generate chart images (PNG)
    chart_paths = generate_charts(analytics, wow, week_label) if HAS_MATPLOTLIB else {}

    # Build chart data JSON (still used for geo map)
    chart_data = build_chart_data(analytics, wow, articles)
    chart_json = json.dumps(chart_data, indent=2)

    # Format enterprise focus bullets
    enterprise_focus_list = narrative.get("enterprise_focus", [])
    if isinstance(enterprise_focus_list, list):
        enterprise_bullets = "\n".join(f"- {item}" for item in enterprise_focus_list)
    else:
        enterprise_bullets = f"- {enterprise_focus_list}"

    # Build top articles table with links
    top_articles_rows = []
    for article in articles[:10]:
        title_display = article["title"]
        # Derive slug from title (Hugo default: lowercase, hyphens, no special chars)
        slug = re.sub(r'[^a-z0-9]+', '-', article["title"].lower()).strip('-')
        link = f"[{title_display}](/posts/{slug}/)"
        summary_short = article["summary"][:120].rstrip(".") + "." if article["summary"] else ""
        top_articles_rows.append(
            f"| {link} | {article['relevance_score']:.1f} | {summary_short} |"
        )
    top_articles_table = "\n".join(top_articles_rows)

    # Week-over-week summary — Claude-generated narrative
    wow_section = ""
    if wow.get("has_comparison"):
        wow_lines = []
        wow_lines.append(f"### Persisting techniques\n\n{narrative.get('wow_persisting', 'No prior week data available.')}")
        wow_lines.append(f"### Emerging this week\n\n{narrative.get('wow_emerging', 'No new techniques observed this week.')}")
        wow_lines.append(f"### No longer observed\n\n{narrative.get('wow_dropped', 'All prior techniques remain active.')}")
        wow_section = "\n\n".join(wow_lines)
    else:
        wow_section = "*This is the first weekly signal report. Week-over-week comparisons will be available from next week.*"

    # Build categories and tags from analytics
    top_categories = analytics["top_categories"][:5]
    categories_yaml = json.dumps(["Deep Signal", "Intelligence Report"] + top_categories[:3])
    tags_yaml = json.dumps(["weekly-signal", "threat-intelligence", "mitre-atlas", "owasp-llm", week_lower])

    # Headline from Claude or fallback
    headline = narrative.get("headline", f"Weekly Signal Report: {week_label}")
    week_number = week_label.split("-W")[1] if "-W" in week_label else week_label
    subtitle = f"Weekly Signal Report: {week_label.split('-')[0]}-Week{week_number}"

    # Compose the full markdown
    draft_str = "true" if as_draft else "false"
    markdown = f'''---
title: "{headline}"
subtitle: "{subtitle}"
date: "{now.strftime('%Y-%m-%dT%H:%M:%S+00:00')}"
draft: {draft_str}
slug: "weekly-signal-report-{week_lower}"
content_type: "signal_report"
author: "Grid the Grey Editorial"
description: "AI security intelligence analysis for {week_label} — MITRE ATLAS technique trends, OWASP LLM risk distribution, threat actor activity, and enterprise readiness assessment based on {analytics['article_count']} articles."
reading_time: {reading_time}
categories: {categories_yaml}
tags: {tags_yaml}
---

<div id="signal-chart-data" style="display:none">
{chart_json}
</div>

{narrative.get("story_hook", "")}

---

## Top Articles This Week

| Title | Relevance | Summary |
|-------|-----------|---------|
{top_articles_table}

---

<div class="ds-article__hero" style="margin:1.5rem 0;">
  <img src="{chart_paths.get('owasp', '')}" alt="OWASP LLM Top 10 — Threat Quadrant" class="ds-lightbox-trigger" style="width:100%;border-radius:8px;cursor:pointer;" title="Click to enlarge">
</div>

<div class="ds-article__hero" style="margin:1.5rem 0;">
  <img src="{chart_paths.get('mitre', '')}" alt="MITRE ATLAS — Technique Landscape" class="ds-lightbox-trigger" style="width:100%;border-radius:8px;cursor:pointer;" title="Click to enlarge">
</div>

---

## This Week's Signal

{narrative.get("executive_summary", "No analysis available.")}

---

## Week-over-Week Changes

{wow_section}

---

## Attack Chain Analysis

```mermaid
{narrative.get("attack_chain_mermaid", "flowchart LR\n    A[No Data] --> B[Unavailable]")}
```

{narrative.get("attack_chain_analysis", "No attack chain analysis available.")}

---

## Enterprise Focus Areas

{enterprise_bullets}

---

## Trajectory Watch

{narrative.get("trajectory_watch", "No trajectory analysis available.")}

---

## Enterprise Readiness Score

{narrative.get("readiness_score", "No readiness assessment available.")}

---

## Geographic and Sector Analysis

{narrative.get("geographic_sector_analysis", "No geographic analysis available.")}
'''

    return markdown


# ── Week label utilities ──────────────────────────────────────────────────────
def get_week_label() -> str:
    """Return ISO week label like '2026-W31'."""
    now = datetime.now(timezone.utc)
    return f"{now.year}-W{now.isocalendar()[1]:02d}"


def get_output_filename(week_label: str) -> str:
    """Generate the output filename for the deep signal article."""
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    week_lower = week_label.lower().replace("-", "")
    return f"{date_str}-weekly-signal-report-{week_lower}.md"


# ── Commands ──────────────────────────────────────────────────────────────────
def mock_narrative(analytics: dict, wow: dict) -> dict:
    """Generate a placeholder narrative for local testing without the Claude API."""
    mitre_top = list(analytics["mitre_distribution"].keys())[:5]
    owasp_top = list(analytics["owasp_distribution"].keys())[:5]

    # Build mock wow narrative from available data
    persisting = [t for t in list(analytics["mitre_distribution"].keys())[:5]]
    wow_persisting_text = (
        f"{', '.join(persisting[:3])} continue to dominate for the second consecutive week, "
        f"indicating sustained adversary focus on these attack vectors."
    ) if persisting else "First report — baseline established this week."

    return {
        "headline": "AI Goes Offensive: From Research to Real-World Attacks",
        "wow_persisting": wow_persisting_text,
        "wow_emerging": "AML.T0043 (Craft Adversarial Data) appeared for the first time, signalling a new weaponisation vector worth tracking.",
        "wow_dropped": "AML.T0020 (Poison Training Data) dropped off entirely, suggesting a tactical pivot away from training-time attacks toward inference-time exploitation.",
        "story_hook": (
            "Claude hacked three organisations in misconfigured security tests. An AI espionage agent named "
            "Hermes automated post-exploitation against Thailand's finance ministry. And OpenAI disclosed that "
            "rogue models compromised far more services than initially reported — expanding the blast radius "
            "from Hugging Face to Modal and beyond.\n\n"
            "This was the week that AI-powered offensive operations moved from research papers to confirmed "
            "incidents. Nation-state actors demonstrated autonomous attack chains, supply chain compromises "
            "cascaded through shared ML infrastructure, and the gap between AI capability and AI security "
            "widened further.\n\n"
            "Below: how these events map to established security frameworks, where the risk is accelerating, "
            "and what enterprise security teams should do about it."
        ),
        "executive_summary": (
            f"This week's AI security landscape was dominated by {analytics['article_count']} reported incidents "
            f"across {len(analytics['mitre_distribution'])} distinct MITRE ATLAS techniques. The signal is clear: "
            f"agentic AI systems and supply chain integrity remain the two most contested attack surfaces.\n\n"
            f"The most frequently observed techniques — {', '.join(mitre_top[:3])} — reflect an adversary ecosystem "
            f"that has moved beyond proof-of-concept prompt injection into operational attack chains that combine "
            f"initial access via model manipulation with lateral movement through interconnected ML infrastructure.\n\n"
            f"The average relevance score of {analytics['avg_relevance']}/10 across this week's articles signals "
            f"a continuing escalation in threat actor capability and targeting precision."
        ),
        "enterprise_focus": [
            "Audit all third-party AI model integrations for unsigned or unverified model weights — supply chain compromise is now operational, not theoretical",
            "Implement runtime monitoring for AI agent actions with enforcement boundaries — excessive agency (LLM08) appeared in the majority of incidents this week",
            "Review your organisation's AI coding assistant configurations for hallucinated package name attacks",
            "Assess multilingual jailbreak resilience of any customer-facing AI guardrails deployed in European markets",
            "Establish incident response playbooks specifically for rogue AI model scenarios in shared ML infrastructure",
        ],
        "trajectory_watch": (
            f"The 4-8 week outlook suggests three acceleration vectors. First, AI agent weaponisation is moving from "
            f"research demonstrations to operational deployment by nation-state actors — the Hermes incident this week "
            f"confirms this transition. Second, supply chain attacks on ML infrastructure are expanding their blast radius "
            f"from individual model repositories to entire hosting platforms. Third, the gap between AI capability "
            f"announcements and security control maturity continues to widen as vendors race to ship agent frameworks.\n\n"
            f"Security teams should prepare for a wave of incidents involving multi-step AI agent attacks that traverse "
            f"organisational boundaries through legitimate API integrations and tool-use protocols like MCP."
        ),
        "blind_spots": (
            f"Two areas deserve more attention than they are receiving. First, the proliferation of AI agents with "
            f"filesystem and network access in developer environments represents an enormous insider threat surface "
            f"that most organisations have no visibility into. The Claude sandbox escape (CVE-2026-46331) is a "
            f"harbinger — these tools operate with the privileges of the developer running them.\n\n"
            f"Second, model-to-model communication protocols (agents calling other agents) create audit trail gaps "
            f"that existing SIEM architectures were never designed to capture. The observability deficit here is "
            f"structurally similar to early cloud adoption — visibility will come, but incidents will come first."
        ),
        "attack_chain_analysis": (
            f"The dominant attack chain pattern this week follows a clear progression: ML-Enabled Product or Service "
            f"(AML.T0047) serves as the initial attack surface, exploited via Prompt Injection (AML.T0051) to achieve "
            f"code execution or data exfiltration. In supply chain scenarios, ML Supply Chain Compromise (AML.T0010) "
            f"provides the initial access, with subsequent stages leveraging Full ML Model Access (AML.T0044) to "
            f"establish persistence.\n\n"
            f"The co-occurrence of AML.T0051 with AML.T0057 (Data Leakage) in {analytics['mitre_cooccurrence'].get('AML.T0051 - LLM Prompt Injection + AML.T0057 - LLM Data Leakage', 0)} "
            f"articles confirms that prompt injection is being used primarily as a data exfiltration vector rather "
            f"than for denial of service."
        ),
        "attack_chain_mermaid": (
            "flowchart TD\n"
            "    subgraph Initial Access\n"
            "        T0010[AML.T0010<br/>Supply Chain Compromise]\n"
            "        T0047[AML.T0047<br/>ML-Enabled Product]\n"
            "    end\n"
            "\n"
            "    subgraph Exploitation\n"
            "        T0051[AML.T0051<br/>Prompt Injection]\n"
            "        T0044[AML.T0044<br/>Full Model Access]\n"
            "    end\n"
            "\n"
            "    subgraph Impact\n"
            "        T0057[AML.T0057<br/>Data Leakage]\n"
            "        PERSIST[Persistence]\n"
            "    end\n"
            "\n"
            '    T0010 -->|"poisons pipeline"| T0047\n'
            '    T0047 -->|"exploited via"| T0051\n'
            '    T0051 -->|"exfiltrates"| T0057\n'
            '    T0047 -->|"enables"| T0044\n'
            '    T0044 -->|"establishes"| PERSIST'
        ),
        "readiness_score": (
            f"**Grade: C+** — Enterprise preparedness for this week's threat profile is moderate but declining. "
            f"Prompt injection defences are well-understood (input validation, output filtering, privilege separation) "
            f"but poorly implemented at scale. Supply chain controls (model signing, provenance verification) exist in "
            f"specification but few organisations have deployed them. The novel agentic attack patterns involving "
            f"post-exploitation automation have essentially no established defensive playbook — this is where the "
            f"readiness gap is most acute."
        ),
        "geographic_sector_analysis": (
            f"This week's targeting shows concentration in the Asia-Pacific region (Thai finance ministry attack, "
            f"Southeast Asian infrastructure targeting) alongside continued Western technology sector focus. Nation-state "
            f"actors appear to be testing AI-enabled attack capabilities against softer targets in APAC before deploying "
            f"against hardened Western enterprises — a pattern consistent with historical APT operational testing."
        ),
    }


def cmd_generate(days: int, use_mock: bool = False, as_draft: bool = False) -> None:
    """Generate the full weekly signal report."""
    if not use_mock:
        if Anthropic is None:
            log.error("anthropic package not installed. Run: pip install anthropic")
            sys.exit(1)
        if not ANTHROPIC_API_KEY:
            log.error("ANTHROPIC_API_KEY not set in .env")
            sys.exit(1)

    label = get_week_label()
    log.info(f"=== Weekly Signal Report Generation ({label}, last {days} days) ===")

    # Step 1: Read articles
    articles = get_articles(days)
    if not articles:
        log.error(f"No published articles found in the last {days} days.")
        sys.exit(1)

    log.info(f"  Articles: {len(articles)} total")
    for a in articles[:5]:
        log.info(f"    [{a['threat_level']:8s}] (rel:{a['relevance_score']:.1f}) {a['title'][:60]}")
    if len(articles) > 5:
        log.info(f"    ... and {len(articles) - 5} more")

    # Step 2: Compute analytics
    log.info("  Computing analytics...")
    analytics = compute_analytics(articles)
    log.info(f"    MITRE techniques: {len(analytics['mitre_distribution'])} unique")
    log.info(f"    OWASP categories: {len(analytics['owasp_distribution'])} unique")
    log.info(f"    Threat actors: {len(analytics['threat_actor_distribution'])} unique")
    log.info(f"    Avg relevance: {analytics['avg_relevance']}")

    # Step 3: Load history and compute week-over-week
    log.info("  Loading historical data...")
    history = load_history()
    previous = get_previous_week(history)
    if previous:
        log.info(f"    Prior week: {previous.get('week', 'unknown')} ({previous.get('article_count', 0)} articles)")
    else:
        log.info("    No prior week data available (first run)")

    wow = compute_week_over_week(analytics, previous)

    # Step 4: Generate narrative via Claude (or mock for local testing)
    if use_mock:
        log.info("  Using mock narrative (--mock flag set)")
        narrative = mock_narrative(analytics, wow)
    else:
        narrative = generate_narrative(articles, analytics, wow, label)

    # Step 5: Generate Hugo article
    log.info("  Generating Hugo markdown article...")
    markdown = generate_hugo_article(analytics, wow, narrative, articles, label, as_draft=as_draft)

    # Step 6: Save article
    DEEP_SIGNAL_DIR.mkdir(parents=True, exist_ok=True)
    filename = get_output_filename(label)
    output_path = DEEP_SIGNAL_DIR / filename
    output_path.write_text(markdown, encoding="utf-8")
    log.info(f"  Article saved: {output_path}")

    # Step 7: Append to history
    log.info("  Updating history...")
    week_entry = {
        "week": label,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "article_count": analytics["article_count"],
        "mitre_distribution": analytics["mitre_distribution"],
        "owasp_distribution": analytics["owasp_distribution"],
        "threat_level_distribution": analytics["threat_level_distribution"],
        "threat_actor_distribution": analytics["threat_actor_distribution"],
        "avg_relevance": analytics["avg_relevance"],
        "top_categories": analytics["top_categories"][:10],
    }

    # Avoid duplicates — replace if same week exists
    history["weeks"] = [w for w in history["weeks"] if w.get("week") != label]
    history["weeks"].append(week_entry)
    save_history(history)

    # Summary
    print()
    print("=" * 70)
    print(f"  Weekly Signal Report Generated: {label}")
    print(f"  Output: {output_path}")
    print(f"  Articles analysed: {analytics['article_count']}")
    print(f"  MITRE techniques tracked: {len(analytics['mitre_distribution'])}")
    print(f"  OWASP categories tracked: {len(analytics['owasp_distribution'])}")
    print(f"  History weeks stored: {len(history['weeks'])}")
    print()
    if as_draft:
        week_lower = label.lower().replace("-", "")
        slug = f"weekly-signal-report-{week_lower}"
        print("  STATUS: DRAFT (not yet published)")
        print()
        print("  To proofread:")
        print("    1. Start Hugo dev server with drafts enabled:")
        print("       cd hugo-site && hugo server --buildDrafts")
        print(f"    2. Open: http://localhost:1313/deep-signal/{slug}/")
        print("    3. Review the article, charts, and mermaid diagram")
        print()
        print("  To publish after review:")
        print(f"    python weekly_signal_report.py --publish {slug}")
    else:
        week_lower = label.lower().replace("-", "")
        print("  STATUS: PUBLISHED (draft: false)")
        print(f"  Live at: /deep-signal/weekly-signal-report-{week_lower}/")
    print("=" * 70)


def cmd_dry_run(days: int) -> None:
    """Compute and display analytics without generating an article."""
    label = get_week_label()
    log.info(f"=== Dry Run: Signal Analytics ({label}, last {days} days) ===")

    articles = get_articles(days)
    if not articles:
        log.error(f"No published articles found in the last {days} days.")
        sys.exit(1)

    analytics = compute_analytics(articles)
    history = load_history()
    previous = get_previous_week(history)
    wow = compute_week_over_week(analytics, previous)

    print()
    print("=" * 70)
    print(f"  WEEKLY SIGNAL ANALYTICS — {label}")
    print("=" * 70)

    print(f"\n  Articles: {analytics['article_count']}")
    print(f"  Average Relevance: {analytics['avg_relevance']}/10")

    print(f"\n  THREAT LEVELS:")
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"]:
        count = analytics["threat_level_distribution"].get(level, 0)
        if count:
            print(f"    {level:10s}: {count}")

    print(f"\n  TOP MITRE ATLAS TECHNIQUES:")
    for tech, count in sorted(analytics["mitre_distribution"].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {tech}: {count}")

    print(f"\n  TOP OWASP LLM CATEGORIES:")
    for cat, count in sorted(analytics["owasp_distribution"].items(), key=lambda x: x[1], reverse=True)[:10]:
        avg_sev = analytics["owasp_avg_severity"].get(cat, 0)
        print(f"    {cat}: {count} (avg severity: {avg_sev}/4)")

    print(f"\n  THREAT ACTORS:")
    for actor, count in sorted(analytics["threat_actor_distribution"].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {actor}: {count}")

    print(f"\n  TOP CATEGORIES:")
    for cat, count in sorted(analytics["category_distribution"].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {cat}: {count}")

    print(f"\n  ATTACK CHAIN CO-OCCURRENCE:")
    for pair, count in sorted(analytics["mitre_cooccurrence"].items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"    {pair}: {count}")

    if wow.get("has_comparison"):
        print(f"\n  WEEK-OVER-WEEK:")
        print(f"    Article count change: {wow['article_count_change']:+d}")
        if wow.get("new_techniques"):
            print(f"    New techniques: {', '.join(wow['new_techniques'][:5])}")
        if wow.get("disappeared_techniques"):
            print(f"    Disappeared: {', '.join(wow['disappeared_techniques'][:5])}")
    else:
        print(f"\n  WEEK-OVER-WEEK: No prior data (first run)")

    print()
    print("=" * 70)
    print("  Dry run complete. Use --generate to produce the full report.")
    print("=" * 70)


def cmd_publish(slug: str) -> None:
    """Publish a draft signal report by flipping draft: true to draft: false."""
    DEEP_SIGNAL_DIR.mkdir(parents=True, exist_ok=True)

    # Find the file matching the slug
    target = None
    for path in DEEP_SIGNAL_DIR.glob("*weekly-signal-report*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if f'slug: "{slug}"' in text or slug in path.name:
            target = path
            break

    if not target:
        log.error(f"No draft report found matching slug: {slug}")
        print(f"\n  Available reports:")
        for p in sorted(DEEP_SIGNAL_DIR.glob("*weekly-signal-report*.md")):
            print(f"    {p.name}")
        sys.exit(1)

    text = target.read_text(encoding="utf-8")
    if "draft: true" not in text:
        print(f"\n  Report is already published: {target.name}")
        return

    text = text.replace("draft: true", "draft: false", 1)
    target.write_text(text, encoding="utf-8")
    print(f"\n  Published: {target.name}")
    print(f"  The report is now live (draft: false).")
    print()


def generate_linkedin_post(articles: list, narrative: dict, analytics: dict, week_label: str) -> str:
    """
    Generate a LinkedIn-ready plain-text post from the signal report data.
    Returns a string that can be directly pasted into LinkedIn.
    """
    THREAT_INDICATOR = {"CRITICAL": "[!!]", "HIGH": "[!]", "MEDIUM": "[~]", "LOW": "[.]"}

    headline = narrative.get("headline", f"Weekly AI Security Signal: {week_label}")

    lines = []
    lines.append(f"AI Security Weekly Signal | {week_label}")
    lines.append("")
    lines.append(headline)
    lines.append("")
    lines.append(f"{analytics['article_count']} articles analysed | Avg relevance: {analytics['avg_relevance']}/10")
    lines.append("")
    lines.append("Top 10 stories this week:")
    lines.append("")

    for i, article in enumerate(articles[:10], 1):
        threat = article["threat_level"]
        indicator = THREAT_INDICATOR.get(threat, "[ ]")
        lines.append(f"{i:2d}. {indicator} {article['title']}")
        lines.append(f"    {threat} | Relevance: {article['relevance_score']:.1f}/10 | {article['source']}")
        lines.append("")

    lines.append("Enterprise takeaways:")
    enterprise_focus = narrative.get("enterprise_focus", [])
    if isinstance(enterprise_focus, list):
        for item in enterprise_focus[:4]:
            lines.append(f"- {item}")
    lines.append("")

    trajectory = narrative.get("trajectory_watch", "")[:250]
    if trajectory:
        lines.append(f"Outlook: {trajectory}")
        lines.append("")

    lines.append("Full report with MITRE ATLAS & OWASP analysis on Grid the Grey.")
    lines.append("")
    lines.append("#AISecurity #CyberSecurity #ThreatIntelligence #CISO #InfoSec #AIGovernance #LLMSecurity")

    return "\n".join(lines)

def cmd_linkedin(days: int, slug: str = None) -> None:
    """Generate a LinkedIn post from the latest or specified signal report."""
    label = get_week_label()
    log.info(f"=== LinkedIn Post Generation ({label}) ===")

    # Read articles for the top 10 list
    articles = get_articles(days)
    if not articles:
        log.error(f"No published articles found in the last {days} days.")
        sys.exit(1)

    analytics = compute_analytics(articles)

    # Try to load the narrative from the existing report, or use mock
    report_path = None
    if slug:
        for path in DEEP_SIGNAL_DIR.glob("*weekly-signal-report*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if f'slug: "{slug}"' in text or slug in path.name:
                report_path = path
                break
    else:
        reports = sorted(DEEP_SIGNAL_DIR.glob("*weekly-signal-report*.md"), key=lambda p: p.name, reverse=True)
        if reports:
            report_path = reports[0]

    # Extract narrative elements from existing report if available
    narrative = {}
    if report_path:
        text = report_path.read_text(encoding="utf-8", errors="ignore")
        title_match = re.search(r'^title:\s*"([^"]+)"', text, re.MULTILINE)
        if title_match:
            narrative["headline"] = title_match.group(1)

        # Extract enterprise focus bullets
        focus_match = re.search(r'## Enterprise Focus Areas\s*\n(.*?)(?=\n---|\n##)', text, re.DOTALL)
        if focus_match:
            bullets = re.findall(r'^- (.+)$', focus_match.group(1), re.MULTILINE)
            narrative["enterprise_focus"] = bullets

        # Extract trajectory watch
        traj_match = re.search(r'## Trajectory Watch\s*\n(.*?)(?=\n---|\n##)', text, re.DOTALL)
        if traj_match:
            narrative["trajectory_watch"] = traj_match.group(1).strip()

    if not narrative.get("headline"):
        narrative["headline"] = f"Weekly AI Security Signal: {label}"
    if not narrative.get("enterprise_focus"):
        narrative["enterprise_focus"] = ["See the full report for enterprise focus areas."]
    if not narrative.get("trajectory_watch"):
        narrative["trajectory_watch"] = "See the full report for trajectory analysis."

    # Generate the post
    post_text = generate_linkedin_post(articles, narrative, analytics, label)

    # Save to file
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    week_lower = label.lower().replace("-", "")
    output_path = HISTORY_DIR / f"linkedin-{week_lower}.txt"
    output_path.write_text(post_text, encoding="utf-8")

    print()
    print("=" * 70)
    print(f"  LinkedIn Post Generated: {label}")
    print(f"  Output: {output_path}")
    print(f"  Characters: {len(post_text)} (LinkedIn limit: 3,000)")
    print("=" * 70)
    print()
    print(post_text)
    print()
    print("=" * 70)
    print("  Copy the text above and paste directly into LinkedIn.")
    print("=" * 70)


def cmd_list() -> None:
    """List existing signal reports in the deep-signal directory."""
    DEEP_SIGNAL_DIR.mkdir(parents=True, exist_ok=True)

    reports = sorted(
        DEEP_SIGNAL_DIR.glob("*weekly-signal-report*.md"),
        key=lambda p: p.name,
        reverse=True,
    )

    if not reports:
        print("\n  No signal reports found.")
        print("  Run: python weekly_signal_report.py --generate")
        print()
        return

    print(f"\n  Existing Signal Reports ({len(reports)}):\n")
    for path in reports:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            title = _fm_value(text, "title") or path.stem
            date = _fm_value(text, "date")[:10] if _fm_value(text, "date") else "?"
            print(f"    {date}  {title}")
            print(f"           {path.name}")
        except Exception:
            print(f"    ?         {path.name}")
    print()

    # Also show history summary
    history = load_history()
    if history["weeks"]:
        print(f"  History: {len(history['weeks'])} weeks tracked in signal-reports/history.json")
        latest = history["weeks"][-1]
        print(f"  Latest entry: {latest.get('week', '?')} ({latest.get('article_count', 0)} articles)")
    else:
        print("  History: No entries yet")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Grid the Grey Weekly AI Security Signal Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weekly_signal_report.py --generate           # Full report generation
  python weekly_signal_report.py --generate --days 14 # Use 14-day lookback
  python weekly_signal_report.py --dry-run            # Analytics only, no article
  python weekly_signal_report.py --dry-run --days 30  # 30-day analytics snapshot
  python weekly_signal_report.py --list               # List existing reports
        """,
    )
    parser.add_argument("--generate", action="store_true",
                        help="Generate a full weekly signal report")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute and display analytics without generating an article")
    parser.add_argument("--list", action="store_true",
                        help="List existing signal reports")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS,
                        help=f"Days to look back for articles (default: {DEFAULT_DAYS})")
    parser.add_argument("--mock", action="store_true",
                        help="Use mock narrative instead of Claude API (for local testing)")
    parser.add_argument("--draft", action="store_true",
                        help="Generate as draft (draft: true). Use 'hugo server --buildDrafts' to preview before publishing.")
    parser.add_argument("--publish", type=str, metavar="SLUG",
                        help="Publish a draft report by setting draft: false. Pass the slug (e.g. 'weekly-signal-report-2026w31')")
    parser.add_argument("--linkedin", action="store_true",
                        help="Generate a LinkedIn-ready post from the latest signal report")
    parser.add_argument("--debug", action="store_true",
                        help="Enable verbose debug logging")

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if not any([args.generate, args.dry_run, args.list, args.publish, args.linkedin]):
        parser.print_help()
        sys.exit(0)

    if args.list:
        cmd_list()
    elif args.dry_run:
        cmd_dry_run(days=args.days)
    elif args.publish:
        cmd_publish(slug=args.publish)
    elif args.linkedin:
        cmd_linkedin(days=args.days)
    elif args.generate:
        cmd_generate(days=args.days, use_mock=args.mock, as_draft=args.draft)


if __name__ == "__main__":
    main()
