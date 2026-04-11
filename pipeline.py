#!/usr/bin/env python3
"""
SENTINEL AI — RSS-to-Hugo Pipeline
====================================
Fetches AI security news from RSS feeds, scores articles with Claude API,
maps them to MITRE ATLAS / OWASP LLM Top 10, and generates Hugo draft posts.

Usage:
    python pipeline.py                    # Normal run
    python pipeline.py --dry-run          # Preview without writing files
    python pipeline.py --limit 5          # Process max 5 articles
    python pipeline.py --feed thehackernews  # Single feed only
    python pipeline.py --reprocess        # Ignore seen_urls cache
    python pipeline.py --verbose          # Detailed logging
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import httpx
from anthropic import Anthropic
from dotenv import load_dotenv
from slugify import slugify

# ─────────────────────────────────────────────
# 0. BOOTSTRAP
# ─────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────
# 1. CONFIGURATION
# ─────────────────────────────────────────────

# RSS Feed sources
RSS_FEEDS = {
    "thehackernews": {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews",
    },
    "securityweek": {
        "name": "SecurityWeek",
        "url": "https://www.securityweek.com/feed/",
    },
    "darkreading": {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com/rss.xml",
    },
    "crowdstrike": {
        "name": "CrowdStrike Blog",
        "url": "https://www.crowdstrike.com/en-us/blog/feed",
    },
    "sans_isc": {
        "name": "SANS Internet Storm Center",
        "url": "https://isc.sans.edu/rssfeed_full.xml",
    },
    "hn_ai_security": {
        "name": "HN AI Security",
        "url": "https://hnrss.org/newest?q=AI+security+OR+LLM+vulnerability+OR+prompt+injection&points=50",
    },
    "schneier": {
        "name": "Schneier on Security",
        "url": "https://www.schneier.com/feed/",
    },
    "projectzero": {
        "name": "Google Project Zero",
        "url": "https://googleprojectzero.blogspot.com/feeds/posts/default",
    },
    "krebsonsecurity": {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
    },
}

# Pre-filter keywords — article must contain at least one to proceed to Claude
# This avoids wasting API calls on clearly irrelevant content
PREFILTER_KEYWORDS = [
    # Core AI/ML terms
    "artificial intelligence", "machine learning", "deep learning",
    "neural network", "large language model", "llm", "gpt", "claude",
    "gemini", "mistral", "llama", "foundation model", "generative ai",
    # Attack categories
    "prompt injection", "jailbreak", "adversarial", "data poisoning",
    "model poisoning", "training data", "fine-tuning attack",
    "model inversion", "membership inference", "model theft",
    "model extraction", "backdoor", "trojan", "watermark",
    # Frameworks & tools
    "mitre atlas", "owasp llm", "langchain", "rag", "retrieval augmented",
    "autonomous agent", "ai agent", "copilot", "chatgpt", "openai",
    "anthropic", "huggingface", "stable diffusion", "midjourney",
    # Vulnerability language
    "ai vulnerability", "ai security", "ai attack", "ai exploit",
    "ml security", "ml attack", "llm vulnerability", "llm exploit",
    "ai safety", "alignment", "ai red team",
]

# Categories mapping — used to classify articles
VALID_CATEGORIES = [
    "LLM Security",
    "Prompt Injection",
    "Adversarial ML",
    "Data Poisoning",
    "Model Theft",
    "Supply Chain",
    "Jailbreaks",
    "Agentic AI",
    "Regulatory",
    "Research",
    "Industry News",
]

# MITRE ATLAS techniques reference (for Claude's context)
MITRE_ATLAS_CONTEXT = """
Key MITRE ATLAS Techniques:
- AML.T0006: Active Learning Attack
- AML.T0010: ML Supply Chain Compromise
- AML.T0012: Valid Accounts
- AML.T0015: Evade ML Model
- AML.T0018: Backdoor ML Model
- AML.T0019: Publish Poisoned Datasets
- AML.T0020: Poison Training Data
- AML.T0031: Erode ML Model Integrity
- AML.T0040: ML Model Inference API Access
- AML.T0043: Craft Adversarial Data
- AML.T0044: Full ML Model Access
- AML.T0047: ML-Enabled Product or Service
- AML.T0051: LLM Prompt Injection
- AML.T0054: LLM Jailbreak
- AML.T0056: LLM Meta Prompt Extraction
- AML.T0057: LLM Data Leakage
"""

# OWASP LLM Top 10 reference
OWASP_LLM_CONTEXT = """
OWASP LLM Top 10 Categories:
- LLM01: Prompt Injection
- LLM02: Insecure Output Handling
- LLM03: Training Data Poisoning
- LLM04: Model Denial of Service
- LLM05: Supply Chain Vulnerabilities
- LLM06: Sensitive Information Disclosure
- LLM07: Insecure Plugin Design
- LLM08: Excessive Agency
- LLM09: Overreliance
- LLM10: Model Theft
"""

# Settings from environment
ANTHROPIC_API_KEY   = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL        = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "6.0"))
HUGO_POSTS_DIR      = Path(os.getenv("HUGO_POSTS_DIR", "hugo-site/content/posts"))
SEEN_URLS_FILE      = Path(os.getenv("SEEN_URLS_FILE", "seen_urls.json"))
MAX_ARTICLES        = int(os.getenv("MAX_ARTICLES_PER_RUN", "20"))
FETCH_FULL_CONTENT  = os.getenv("FETCH_FULL_CONTENT", "true").lower() == "true"
FETCH_TIMEOUT       = int(os.getenv("FETCH_TIMEOUT", "10"))

# Pipeline version — bump when changing the Claude prompt
PIPELINE_VERSION = "1.0.0"

# ─────────────────────────────────────────────
# 2. LOGGING
# ─────────────────────────────────────────────

def setup_logging(verbose: bool = False) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    # Quiet noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    return logging.getLogger("sentinel")

# ─────────────────────────────────────────────
# 3. SEEN-URL CACHE  (deduplication)
# ─────────────────────────────────────────────

def load_seen_urls(path: Path) -> set:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("urls", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def save_seen_urls(path: Path, seen: set) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"urls": sorted(seen), "updated_at": datetime.now(timezone.utc).isoformat()}, f, indent=2)

# ─────────────────────────────────────────────
# 4. RSS FEED FETCHING
# ─────────────────────────────────────────────

def fetch_feed(feed_key: str, feed_info: dict, log: logging.Logger) -> list[dict]:
    """Fetch and parse a single RSS feed. Returns list of article dicts."""
    log.info(f"  Fetching [{feed_info['name']}] ...")
    try:
        parsed = feedparser.parse(feed_info["url"])
        if parsed.bozo and not parsed.entries:
            log.warning(f"  ⚠ Feed parse warning for {feed_info['name']}: {parsed.bozo_exception}")
            return []

        articles = []
        for entry in parsed.entries:
            url = entry.get("link", "")
            if not url:
                continue

            # Extract published date
            pub_date = None
            for date_field in ("published_parsed", "updated_parsed"):
                if hasattr(entry, date_field) and getattr(entry, date_field):
                    try:
                        pub_date = datetime(*getattr(entry, date_field)[:6], tzinfo=timezone.utc)
                    except (ValueError, TypeError):
                        pass
                    break
            if not pub_date:
                pub_date = datetime.now(timezone.utc)

            # Clean description/summary from RSS
            description = entry.get("summary", "") or entry.get("description", "")
            description = re.sub(r"<[^>]+>", " ", description)  # strip HTML tags
            description = re.sub(r"\s+", " ", description).strip()

            articles.append({
                "url":         url,
                "title":       entry.get("title", "Untitled").strip(),
                "description": description[:2000],  # cap at 2000 chars
                "published":   pub_date,
                "source":      feed_info["name"],
                "feed_key":    feed_key,
            })

        log.info(f"  ✓ {len(articles)} articles from {feed_info['name']}")
        return articles

    except Exception as e:
        log.error(f"  ✗ Failed to fetch {feed_info['name']}: {e}")
        return []


def fetch_all_feeds(selected_feed: str | None, log: logging.Logger) -> list[dict]:
    """Fetch all configured RSS feeds (or just one if selected_feed is set)."""
    feeds_to_fetch = {}
    if selected_feed:
        if selected_feed not in RSS_FEEDS:
            log.error(f"Unknown feed key '{selected_feed}'. Valid keys: {list(RSS_FEEDS.keys())}")
            sys.exit(1)
        feeds_to_fetch = {selected_feed: RSS_FEEDS[selected_feed]}
    else:
        feeds_to_fetch = RSS_FEEDS

    all_articles = []
    for key, info in feeds_to_fetch.items():
        articles = fetch_feed(key, info, log)
        all_articles.extend(articles)
        time.sleep(0.5)  # polite delay between feeds

    return all_articles

# ─────────────────────────────────────────────
# 5. KEYWORD PRE-FILTER
# ─────────────────────────────────────────────

def passes_prefilter(article: dict) -> bool:
    """Return True if article title or description contains at least one keyword."""
    text = (article["title"] + " " + article["description"]).lower()
    return any(kw in text for kw in PREFILTER_KEYWORDS)

# ─────────────────────────────────────────────
# 6. ARTICLE CONTENT FETCHING  (optional)
# ─────────────────────────────────────────────

def fetch_article_content(url: str, log: logging.Logger) -> tuple[str, str]:
    """
    Attempt to fetch the full article text and og:image.
    Returns (text[:4000], og_image_url) — both may be empty strings on failure.
    Never raises.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SentinelAI-Bot/1.0; +https://sentinel-ai.news/bot)"
        }
        with httpx.Client(timeout=FETCH_TIMEOUT, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            html = resp.text

        # Extract og:image before stripping tags
        og_image = ""
        og_match = re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            html, re.IGNORECASE
        )
        if not og_match:
            # Try reversed attribute order
            og_match = re.search(
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
                html, re.IGNORECASE
            )
        if og_match:
            og_image = og_match.group(1).strip()
            log.debug(f"  og:image found: {og_image[:80]}")

        # Text extraction — remove script/style blocks then strip all tags
        clean = re.sub(r"<(script|style)[^>]*>.*?</(script|style)>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", clean)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:4000], og_image

    except Exception as e:
        log.debug(f"  Content fetch failed for {url}: {e}")
        return "", ""

# ─────────────────────────────────────────────
# 7. CLAUDE API — SCORING & ANALYSIS
# ─────────────────────────────────────────────

ANALYSIS_PROMPT_TEMPLATE = """\
You are a senior AI security analyst working for SENTINEL AI, an intelligence platform covering adversarial AI, LLM vulnerabilities, and machine learning security threats.

Analyse the following article and return a JSON object with your assessment.

## Article Details
Title: {title}
Source: {source}
Published: {published}
URL: {url}

## Article Content
{content}

## Your Task
Return a single valid JSON object (no markdown fences, no extra text) with exactly these fields:

{{
  "relevance_score": <float 0.0–10.0>,
  "is_ai_security_relevant": <true/false>,
  "summary": "<2-3 sentence editorial summary focused on the security implications>",
  "threat_level": "<CRITICAL|HIGH|MEDIUM|LOW|NONE>",
  "mitre_techniques": ["<AML.TXXXX - Technique Name>", ...],
  "owasp_categories": ["<LLMXX - Category Name>", ...],
  "categories": ["<from the valid list>", ...],
  "tags": ["<lowercase-hyphenated>", ...],
  "threat_actors": ["<nation-state|cybercriminal|researcher|insider|hacktivist>", ...],
  "article_body": "<full markdown article body — see format below>"
}}

## Scoring Guide
- 9-10: Critical novel vulnerability, active exploit, or major breach affecting AI/ML systems
- 7-8: Significant AI security research, new attack technique, or important advisory
- 6-7: Relevant AI security news, useful defensive guidance, or notable industry development
- 4-5: Tangentially related (general cybersecurity with minor AI angle)
- 0-3: Not relevant to AI security

## Framework Reference
{mitre_context}
{owasp_context}

## Valid Categories (use only from this list)
{valid_categories}

## Article Body Format
Write the article_body as a markdown string with these sections (include only sections that apply):
- ## Overview — what happened and why it matters
- ## Technical Analysis — how the attack/vulnerability works (include code snippets if relevant)
- ## Framework Mapping — which ATLAS/OWASP categories apply and why
- ## Impact Assessment — who is affected and how severely
- ## Mitigation & Recommendations — actionable defence steps
- ## References — link back to original source

Keep the body between 300–600 words. Use neutral, factual editorial tone.
If the article is NOT AI security relevant (score < 4), still return valid JSON but set article_body to an empty string.
"""


def analyse_with_claude(article: dict, content: str, client: Anthropic, log: logging.Logger) -> dict | None:
    """
    Call Claude API to score and analyse the article.
    Returns parsed dict or None on failure.
    """
    # Build the content block — prefer full content if available, fall back to description
    article_text = content if len(content) > 200 else article["description"]
    if not article_text:
        article_text = "(No article content available — analyse based on title and source only)"

    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        title=article["title"],
        source=article["source"],
        published=article["published"].strftime("%Y-%m-%d"),
        url=article["url"],
        content=article_text,
        mitre_context=MITRE_ATLAS_CONTEXT,
        owasp_context=OWASP_LLM_CONTEXT,
        valid_categories="\n".join(f"- {c}" for c in VALID_CATEGORIES),
    )

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()

        # Strip accidental markdown fences if Claude added them
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)
        log.debug(f"  Claude response parsed OK. Score: {result.get('relevance_score')}")
        return result

    except json.JSONDecodeError as e:
        log.error(f"  ✗ Claude returned invalid JSON for '{article['title']}': {e}")
        log.debug(f"  Raw response: {raw[:500]}")
        return None
    except Exception as e:
        log.error(f"  ✗ Claude API error for '{article['title']}': {e}")
        return None

# ─────────────────────────────────────────────
# 8. HUGO MARKDOWN GENERATION
# ─────────────────────────────────────────────

def build_slug(title: str, published: datetime) -> str:
    """Generate a URL-safe slug from the title."""
    slug = slugify(title, max_length=80, word_boundary=True)
    if not slug:
        slug = f"article-{published.strftime('%Y%m%d%H%M%S')}"
    return slug


def to_yaml_list(items: list | None) -> str:
    """Convert a Python list to YAML inline list string."""
    if not items:
        return "[]"
    safe = [str(i).replace('"', '\\"') for i in items]
    return "[" + ", ".join(f'"{s}"' for s in safe) + "]"


def generate_hugo_markdown(article: dict, analysis: dict) -> str:
    """
    Build the full Hugo markdown file content from article metadata
    and Claude's analysis. Matches the post archetype exactly.
    """
    now = datetime.now(timezone.utc)
    pub_date = article["published"].strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # Front matter
    front_matter = f"""---
title: {json.dumps(article['title'])}
date: {pub_date}
draft: true

# ── Content metadata ──
summary: {json.dumps(analysis.get('summary', ''))}
source: {json.dumps(article['source'])}
source_url: {json.dumps(article['url'])}
author: "SENTINEL AI Editorial"
thumbnail: {json.dumps(article.get('thumbnail', ''))}

# ── AI Security Classification ──
relevance_score: {analysis.get('relevance_score', 0.0)}
threat_level: {json.dumps(analysis.get('threat_level', 'LOW'))}

# ── MITRE ATLAS Techniques ──
mitre_techniques: {to_yaml_list(analysis.get('mitre_techniques', []))}

# ── OWASP LLM Top 10 ──
owasp_categories: {to_yaml_list(analysis.get('owasp_categories', []))}

# ── Taxonomies ──
categories: {to_yaml_list(analysis.get('categories', []))}
tags: {to_yaml_list(analysis.get('tags', []))}
frameworks: {to_yaml_list(analysis.get('frameworks', ['mitre-atlas', 'owasp-llm']))}
threat_actors: {to_yaml_list(analysis.get('threat_actors', []))}

# ── Pipeline metadata ──
fetched_at: "{now.strftime('%Y-%m-%dT%H:%M:%S+00:00')}"
feed_source: {json.dumps(article['feed_key'])}
original_url: {json.dumps(article['url'])}
pipeline_version: "{PIPELINE_VERSION}"
---

"""

    body = analysis.get("article_body", "").strip()
    if not body:
        body = f"*Full analysis pending. [Read the original article at {article['source']}]({article['url']})*"

    return front_matter + body + "\n"


def write_hugo_post(slug: str, content: str, log: logging.Logger) -> Path | None:
    """Write the markdown file to the Hugo posts directory. Returns path or None."""
    HUGO_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = HUGO_POSTS_DIR / f"{slug}.md"

    # Avoid clobbering an existing file — append suffix
    counter = 1
    original_stem = filepath.stem
    while filepath.exists():
        filepath = HUGO_POSTS_DIR / f"{original_stem}-{counter}.md"
        counter += 1

    try:
        filepath.write_text(content, encoding="utf-8")
        log.info(f"  ✓ Written: {filepath.name}")
        return filepath
    except OSError as e:
        log.error(f"  ✗ Failed to write {filepath}: {e}")
        return None

# ─────────────────────────────────────────────
# 9. MAIN PIPELINE ORCHESTRATION
# ─────────────────────────────────────────────

def run_pipeline(args: argparse.Namespace, log: logging.Logger) -> None:

    # ── Validate API key ──
    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # ── Load seen URLs ──
    seen_urls: set = set()
    if not args.reprocess:
        seen_urls = load_seen_urls(SEEN_URLS_FILE)
        log.info(f"Loaded {len(seen_urls)} seen URLs from cache.")

    # ── Stats tracking ──
    stats = {
        "feeds_fetched":    0,
        "articles_found":   0,
        "already_seen":     0,
        "prefilter_pass":   0,
        "prefilter_fail":   0,
        "claude_scored":    0,
        "below_threshold":  0,
        "posts_written":    0,
        "errors":           0,
    }

    # ── Step 1: Fetch feeds ──
    log.info("=" * 60)
    log.info("STEP 1 — Fetching RSS Feeds")
    log.info("=" * 60)
    all_articles = fetch_all_feeds(args.feed, log)
    stats["feeds_fetched"]  = len(RSS_FEEDS) if not args.feed else 1
    stats["articles_found"] = len(all_articles)
    log.info(f"Total articles fetched: {len(all_articles)}")

    # Sort by date descending (newest first)
    all_articles.sort(key=lambda a: a["published"], reverse=True)

    # ── Step 2: Deduplicate ──
    log.info("\nSTEP 2 — Deduplication")
    new_articles = []
    for a in all_articles:
        if a["url"] in seen_urls:
            stats["already_seen"] += 1
        else:
            new_articles.append(a)
    log.info(f"New articles (not yet seen): {len(new_articles)}  |  Already seen: {stats['already_seen']}")

    # ── Step 3: Keyword pre-filter ──
    log.info("\nSTEP 3 — Keyword Pre-filter")
    candidate_articles = []
    for a in new_articles:
        if passes_prefilter(a):
            candidate_articles.append(a)
            stats["prefilter_pass"] += 1
            log.debug(f"  PASS: {a['title'][:80]}")
        else:
            stats["prefilter_fail"] += 1
            log.debug(f"  FAIL: {a['title'][:80]}")
            seen_urls.add(a["url"])  # mark as seen so we don't re-check it

    log.info(f"Passed keyword filter: {len(candidate_articles)}  |  Filtered out: {stats['prefilter_fail']}")

    # Apply per-run article limit
    if args.limit and args.limit > 0:
        candidate_articles = candidate_articles[: args.limit]
        log.info(f"Applying --limit {args.limit}: processing {len(candidate_articles)} articles")
    elif MAX_ARTICLES > 0:
        candidate_articles = candidate_articles[:MAX_ARTICLES]
        log.info(f"Applying MAX_ARTICLES_PER_RUN={MAX_ARTICLES}: processing {len(candidate_articles)} articles")

    if not candidate_articles:
        log.info("\nNo new candidate articles to process. Pipeline complete.")
        save_seen_urls(SEEN_URLS_FILE, seen_urls)
        _print_stats(stats, log)
        return

    # ── Step 4: Claude scoring ──
    log.info(f"\nSTEP 4 — Claude Analysis  (threshold: {RELEVANCE_THRESHOLD})")
    log.info("=" * 60)

    for i, article in enumerate(candidate_articles, 1):
        log.info(f"\n[{i}/{len(candidate_articles)}] {article['title'][:80]}")
        log.info(f"  Source: {article['source']}  |  {article['published'].strftime('%Y-%m-%d')}")

        # Always mark as seen, regardless of outcome
        seen_urls.add(article["url"])

        # Optionally fetch full article content + og:image
        full_content = ""
        og_image = ""
        if FETCH_FULL_CONTENT and not args.dry_run:
            log.debug(f"  Fetching full content from {article['url']}")
            full_content, og_image = fetch_article_content(article["url"], log)
            if full_content:
                log.debug(f"  Content fetched: {len(full_content)} chars")
            if og_image:
                article["thumbnail"] = og_image

        if args.dry_run:
            log.info("  [DRY RUN] Would call Claude API here — skipping")
            stats["claude_scored"] += 1
            continue

        # Call Claude
        analysis = analyse_with_claude(article, full_content, client, log)
        if analysis is None:
            stats["errors"] += 1
            continue

        stats["claude_scored"] += 1
        score = analysis.get("relevance_score", 0.0)
        log.info(f"  Score: {score:.1f}  |  Threat: {analysis.get('threat_level', '?')}  |  Relevant: {analysis.get('is_ai_security_relevant')}")

        # Check threshold
        if score < RELEVANCE_THRESHOLD:
            log.info(f"  ↓ Below threshold ({score:.1f} < {RELEVANCE_THRESHOLD}) — skipping")
            stats["below_threshold"] += 1
            continue

        # Log framework mapping
        mitre = analysis.get("mitre_techniques", [])
        owasp = analysis.get("owasp_categories", [])
        if mitre:
            log.info(f"  ATLAS: {', '.join(mitre[:2])}{'...' if len(mitre) > 2 else ''}")
        if owasp:
            log.info(f"  OWASP: {', '.join(owasp[:2])}{'...' if len(owasp) > 2 else ''}")

        # Generate and write Hugo post
        slug = build_slug(article["title"], article["published"])
        markdown = generate_hugo_markdown(article, analysis)
        written = write_hugo_post(slug, markdown, log)
        if written:
            stats["posts_written"] += 1
        else:
            stats["errors"] += 1

        # Polite rate limiting — avoid hitting API rate limits
        time.sleep(1.0)

    # ── Save state ──
    if not args.dry_run:
        save_seen_urls(SEEN_URLS_FILE, seen_urls)
        log.info(f"\nSaved {len(seen_urls)} URLs to {SEEN_URLS_FILE}")

    _print_stats(stats, log)


def _print_stats(stats: dict, log: logging.Logger) -> None:
    log.info("\n" + "=" * 60)
    log.info("PIPELINE COMPLETE — SUMMARY")
    log.info("=" * 60)
    log.info(f"  Articles fetched:       {stats['articles_found']}")
    log.info(f"  Already seen (skipped): {stats['already_seen']}")
    log.info(f"  Passed keyword filter:  {stats['prefilter_pass']}")
    log.info(f"  Scored by Claude:       {stats['claude_scored']}")
    log.info(f"  Below threshold:        {stats['below_threshold']}")
    log.info(f"  Posts written:          {stats['posts_written']}")
    log.info(f"  Errors:                 {stats['errors']}")
    log.info("=" * 60)
    if stats["posts_written"] > 0:
        log.info(f"  ✓ {stats['posts_written']} new draft post(s) written to {HUGO_POSTS_DIR}")
        log.info("  Review drafts: hugo server -D")
        log.info("  Publish: set 'draft: false' in the front matter")

# ─────────────────────────────────────────────
# 10. CLI
# ─────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SENTINEL AI — RSS-to-Hugo Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Fetch and pre-filter articles but do NOT call Claude or write any files",
    )
    parser.add_argument(
        "--limit", type=int, default=0, metavar="N",
        help="Process at most N articles this run (overrides MAX_ARTICLES_PER_RUN)",
    )
    parser.add_argument(
        "--feed", type=str, default=None, metavar="KEY",
        help=f"Only fetch from one feed. Keys: {', '.join(RSS_FEEDS.keys())}",
    )
    parser.add_argument(
        "--reprocess", action="store_true",
        help="Ignore the seen_urls cache and re-evaluate all articles",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable DEBUG-level logging",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log = setup_logging(args.verbose)

    log.info("╔══════════════════════════════════════╗")
    log.info("║     SENTINEL AI  —  RSS Pipeline     ║")
    log.info(f"║     v{PIPELINE_VERSION}  |  {CLAUDE_MODEL:<22}║")
    log.info("╚══════════════════════════════════════╝")
    log.info(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}  |  Threshold: {RELEVANCE_THRESHOLD}  |  Max articles: {args.limit or MAX_ARTICLES}")

    run_pipeline(args, log)
