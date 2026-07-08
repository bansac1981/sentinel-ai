#!/usr/bin/env python3
"""
Grid the Grey — RSS-to-Hugo Pipeline
====================================
Fetches AI security news from RSS feeds, scores articles with Claude API,
maps them to MITRE ATLAS / OWASP LLM Top 10, and generates Hugo draft posts.

Usage:
    python pipeline.py                           # Normal run (all feeds)
    python pipeline.py --mode threat             # Threat/security feeds only
    python pipeline.py --mode first_look         # AI capability/vendor feeds only
    python pipeline.py --dry-run                 # Preview without writing files
    python pipeline.py --limit 5                 # Process max 5 articles
    python pipeline.py --feed thehackernews      # Single feed only
    python pipeline.py --reprocess               # Ignore seen_urls cache
    python pipeline.py --verbose                 # Detailed logging
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
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

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

    # ── AI Vendors ────────────────────────────────────────────────────────────
    "openai_blog": {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
    },
    "hn_openai": {
        "name": "OpenAI (via HN)",
        "url": "https://hnrss.org/newest?q=OpenAI+OR+GPT+OR+ChatGPT&points=50",
    },
    "anthropic_blog": {
        "name": "Anthropic Blog",
        "url": "https://www.anthropic.com/rss.xml",
    },
    "hn_anthropic": {
        "name": "Anthropic (via HN)",
        "url": "https://hnrss.org/newest?q=Anthropic+OR+Claude&points=50",
    },
    "google_ai_blog": {
        "name": "Google DeepMind Blog",
        "url": "https://blog.google/technology/ai/rss/",
    },
    "microsoft_ai": {
        "name": "Microsoft AI Blog",
        "url": "https://blogs.microsoft.com/ai/feed/",
    },

    # ── Security Vendor Threat Research ───────────────────────────────────────
    "unit42": {
        "name": "Palo Alto Unit 42",
        "url": "https://unit42.paloaltonetworks.com/feed/",
    },
    "talos": {
        "name": "Cisco Talos",
        "url": "https://blog.talosintelligence.com/rss",
    },
    "microsoft_security": {
        "name": "Microsoft Security Blog",
        "url": "https://www.microsoft.com/en-us/security/blog/feed/",
    },
    "sentinelone": {
        "name": "SentinelOne Blog",
        "url": "https://www.sentinelone.com/blog/feed/",
    },
    "mandiant": {
        "name": "Mandiant Blog",
        "url": "https://www.mandiant.com/resources/blog/rss.xml",
    },
    "qualys": {
        "name": "Qualys Blog",
        "url": "https://blog.qualys.com/feed",
    },
    "checkpoint": {
        "name": "Check Point Research",
        "url": "https://research.checkpoint.com/feed/",
    },

    # ── Government & Agencies ─────────────────────────────────────────────────
    "ncsc_uk": {
        "name": "NCSC UK",
        "url": "https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml",
    },

    # ── Security News & Analysis ──────────────────────────────────────────────
    "bleepingcomputer": {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
    },
    "simonwillison": {
        "name": "Simon Willison",
        "url": "https://simonwillison.net/atom/everything/",
    },
    "huggingface": {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
    },
    "wired_security": {
        "name": "Wired Security",
        "url": "https://www.wired.com/feed/category/security/latest/rss",
    },
    "arstechnica": {
        "name": "Ars Technica Security",
        "url": "https://arstechnica.com/security/feed/",
    },

    # ── AI Capability Sources (First Look: Security) ─────────────────────────
    "aws_ml": {
        "name": "AWS Machine Learning Blog",
        "url": "https://aws.amazon.com/blogs/machine-learning/feed/",
    },
    "github_blog": {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed",
    },
    "hn_meta_ai": {
        "name": "Meta AI (via HN)",
        "url": "https://hnrss.org/newest?q=Meta+AI+OR+Llama&points=30",
    },
    "hn_mistral": {
        "name": "Mistral AI (via HN)",
        "url": "https://hnrss.org/newest?q=Mistral+AI+OR+Mistral+model&points=30",
    },
    "hn_cohere": {
        "name": "Cohere AI (via HN)",
        "url": "https://hnrss.org/newest?q=Cohere+AI+OR+Cohere+model&points=30",
    },
    "nvidia_ai": {
        "name": "NVIDIA AI Blog",
        "url": "https://blogs.nvidia.com/feed/",
    },
    "techcrunch_ai": {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
    },
    "theverge_ai": {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
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
    # Capability release signals (for First Look: Security)
    "launches", "ships", "releases", "announces", "generally available",
    "developer preview", "new capability", "new feature", "sdk",
    "mcp", "model context protocol", "tool use", "function calling",
    "code execution", "computer use", "web browsing", "file access",
    "agent framework", "model release", "api update",
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
    "First Look",
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
CLASSIFY_MODEL      = os.getenv("CLASSIFY_MODEL", "claude-haiku-4-5")
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "6.0"))
HUGO_POSTS_DIR      = Path(os.getenv("HUGO_POSTS_DIR", "hugo-site/content/posts"))
HUGO_DRAFTS_DIR     = HUGO_POSTS_DIR / "drafts"
SEEN_URLS_FILE      = Path(os.getenv("SEEN_URLS_FILE", "seen_urls.json"))
MAX_ARTICLES        = int(os.getenv("MAX_ARTICLES_PER_RUN", "15"))
FETCH_FULL_CONTENT  = os.getenv("FETCH_FULL_CONTENT", "true").lower() == "true"
FETCH_TIMEOUT       = int(os.getenv("FETCH_TIMEOUT", "10"))

# Article age filter — reject anything published more than this many days ago
MAX_ARTICLE_AGE_DAYS = int(os.getenv("MAX_ARTICLE_AGE_DAYS", "7"))

# Unsplash API — primary image source (free, high quality, no attribution required)
# Get a free key at: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

# Pexels API — fallback image source (free, no attribution required)
# Get a free key at: https://www.pexels.com/api/
PEXELS_API_KEY      = os.getenv("PEXELS_API_KEY", "")

# ─────────────────────────────────────────────
# IMAGE KEYWORD → SEARCH QUERY MAP (shared by Unsplash + Pexels)
# Ordered most-specific → most-general; first match wins.
# All queries chosen to return professional, relevant landscape photos.
# ─────────────────────────────────────────────
IMAGE_KEYWORD_MAP = [
    # Generative AI / LLM — diversified queries
    (["prompt injection", "jailbreak"],
     "computer security shield warning"),
    (["system prompt", "guardrail", "alignment"],
     "artificial intelligence safety controls"),
    (["llm", "large language model"],
     "language model text generation technology"),
    (["gpt", "chatgpt", "openai"],
     "conversational AI chatbot technology"),
    (["gemini", "google ai", "deepmind"],
     "search engine artificial intelligence"),
    (["claude", "anthropic"],
     "artificial intelligence research laboratory"),
    (["agent", "agentic", "autonomous"],
     "robot automation autonomous workflow"),
    (["rag", "retrieval augmented", "embedding", "vector db"],
     "database search information retrieval"),
    (["deepfake", "synthetic media", "voice clone"],
     "digital identity face recognition"),
    (["neural network", "deep learning", "machine learning"],
     "data science visualization network"),
    (["model release", "open source", "weights"],
     "software release download server"),
    # Ransomware / Malware
    (["ransomware", "ransom demand"],
     "ransomware encrypted lock cybercrime dark"),
    (["malware", "trojan", "virus", "worm", "spyware", "infostealer"],
     "malware computer virus dark hacker"),
    (["backdoor", "rootkit"],
     "backdoor shadow hacking server"),
    (["cryptojacking", "cryptomining"],
     "cryptocurrency mining server"),
    # Social / Credential
    (["phishing", "spear phish", "social engineering"],
     "phishing email hook scam"),
    (["credential", "password spray", "brute force", "mfa bypass"],
     "password authentication security lock"),
    # Data exfiltration
    (["data breach", "data leak", "exfiltrat", "stolen data"],
     "data breach privacy security padlock server"),
    (["surveillance", "spyware", "stalkerware"],
     "surveillance camera privacy security"),
    # Infrastructure
    (["supply chain", "pypi", "npm", "package", "dependency"],
     "supply chain software packages"),
    (["critical infrastructure", "ics", "scada", "ot ", "industrial"],
     "industrial infrastructure power grid"),
    (["cloud", "aws", "azure", "gcp", "kubernetes", "container"],
     "cloud computing server data center"),
    (["api ", "web application", "owasp"],
     "web application programming code security"),
    (["iot", "firmware", "embedded", "router"],
     "iot device circuit board electronics"),
    (["ddos", "denial of service", "botnet"],
     "network server traffic cybersecurity"),
    # Threat actors
    (["nation state", "apt ", "state-sponsored", "espionage",
      "china", "russia", "iran", "north korea"],
     "cyber espionage government hacking globe"),
    # Generic vulnerability
    (["zero day", "zero-day", "cve-", "exploit", "vulnerability", "patch"],
     "cybersecurity vulnerability lock crack code"),
]

# First Look: Security — threshold and classification
FIRST_LOOK_THRESHOLD = float(os.getenv("FIRST_LOOK_THRESHOLD", "5.5"))

FIRST_LOOK_KEYWORDS = [
    "launches", "announces", "releases", "ships", "introduces",
    "rolls out", "unveils", "debuts", "now available", "general availability",
    "new feature", "new capability", "update brings", "adds support for",
    "beta", "preview", "early access", "developer preview", "sdk",
    "open source", "open-source", "model release",
]

THREAT_REPORT_KEYWORDS = [
    "vulnerability", "exploit", "breach", "attack", "compromise",
    "malicious", "hack", "cve-", "zero-day", "zero day", "ransomware",
    "data leak", "stolen", "trojan", "backdoor", "phishing",
    "botnet", "apt", "threat actor", "malware",
]

# Feeds primarily expected to yield First Look content
FIRST_LOOK_FEEDS = {
    "openai_blog", "hn_openai", "anthropic_blog", "hn_anthropic",
    "google_ai_blog", "microsoft_ai", "huggingface",
    "aws_ml", "github_blog", "hn_meta_ai", "hn_mistral", "hn_cohere",
    "nvidia_ai", "techcrunch_ai", "theverge_ai", "simonwillison",
}

# Story deduplication — suppress same-event articles from different sources
STORY_WINDOW_DAYS = int(os.getenv("STORY_WINDOW_DAYS", "7"))  # look-back window for story index

# Pipeline version — bump when changing the Claude prompt
PIPELINE_VERSION = "2.1.0"

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


def flush_seen_urls(path: Path, seen: set) -> None:
    """Write seen_urls mid-run so partial progress survives crashes/interrupts."""
    try:
        save_seen_urls(path, seen)
    except OSError:
        pass


# Tracking/referral params that carry no identity — strip before dedup
_STRIP_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "ref", "referrer", "source", "mc_cid", "mc_eid",
    "fbclid", "gclid", "msclkid", "twclid",
    "_hsenc", "_hsmi", "hsCtaTracking",
}

def canonicalize_url(url: str) -> str:
    """Normalize a URL for deduplication: lowercase scheme+host, strip tracking
    query params, remove trailing slash from path, drop fragment."""
    try:
        p = urlparse(url.strip())
        scheme = p.scheme.lower()
        netloc = p.netloc.lower()
        path = p.path.rstrip("/") or "/"
        # Keep only non-tracking query params, sorted for stable comparison
        kept = [(k, v) for k, v in parse_qsl(p.query) if k.lower() not in _STRIP_PARAMS]
        query = urlencode(sorted(kept))
        return urlunparse((scheme, netloc, path, "", query, ""))
    except Exception:
        return url


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
            url = canonicalize_url(entry.get("link", ""))
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


def fetch_all_feeds(selected_feed: str | None, log: logging.Logger, feed_subset: set | None = None) -> list[dict]:
    """Fetch all configured RSS feeds (or just one if selected_feed is set).

    feed_subset: optional set of feed keys to restrict to (applied after selected_feed).
    """
    feeds_to_fetch = {}
    if selected_feed:
        if selected_feed not in RSS_FEEDS:
            log.error(f"Unknown feed key '{selected_feed}'. Valid keys: {list(RSS_FEEDS.keys())}")
            sys.exit(1)
        feeds_to_fetch = {selected_feed: RSS_FEEDS[selected_feed]}
    elif feed_subset is not None:
        feeds_to_fetch = {k: v for k, v in RSS_FEEDS.items() if k in feed_subset}
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

def fetch_og_image(url: str, log: logging.Logger) -> str:
    """
    Fetch the Open Graph image URL from a webpage.
    Returns the og:image URL string, or empty string on any error.
    Never raises.
    """
    if not url:
        return ""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; GridTheGrey-Bot/1.0; +https://gridthegrey.com/bot)"
        }
        with httpx.Client(timeout=5.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            html = resp.text

        # Try og:image
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
            img_url = og_match.group(1).strip()
            if img_url.startswith("http"):
                log.debug(f"  og:image found: {img_url[:80]}")
                return img_url
    except Exception as e:
        log.debug(f"  OG image fetch failed for {url}: {e}")
    return ""


_VENDOR_NAMES = [
    "openai", "anthropic", "google", "deepmind", "microsoft", "meta",
    "nvidia", "aws", "amazon", "mistral", "cohere", "hugging face",
    "github", "apple", "tesla", "ibm", "oracle", "salesforce",
]


def _extract_vendor(title: str) -> str:
    """Extract a vendor name from the title if present."""
    text = title.lower()
    for v in _VENDOR_NAMES:
        if v in text:
            return v.title()
    return ""


def _image_query(title: str, categories: list) -> str:
    """Build a diverse image search query for this article."""
    text = title.lower()
    for keywords, query in IMAGE_KEYWORD_MAP:
        if any(kw in text for kw in keywords):
            vendor = _extract_vendor(title)
            if vendor:
                return f"{vendor} {query}"
            return query
    # Use vendor + category for more specific results
    vendor = _extract_vendor(title)
    if categories:
        cat = categories[0].replace("-", " ")
        if vendor:
            return f"{vendor} {cat} technology"
        return f"{cat} cybersecurity technology"
    if vendor:
        return f"{vendor} artificial intelligence technology"
    return "cybersecurity artificial intelligence technology"


def get_recent_thumbnails(n: int = 20) -> set:
    """
    Return the thumbnail URLs used in the most-recent N published posts.
    Used to prevent the same Pexels image appearing twice in the feed.
    """
    used: set = set()
    try:
        md_files = sorted(
            list(HUGO_POSTS_DIR.glob("*.md")) + list(HUGO_POSTS_DIR.glob("drafts/*.md")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for path in md_files[:n]:
            text = path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'^thumbnail:\s*"?([^"\n]+)"?', text, re.MULTILINE)
            if m:
                url = m.group(1).strip()
                if url:
                    used.add(url)
    except Exception:
        pass
    return used


def fetch_unsplash_image(
    title: str,
    categories: list,
    log: logging.Logger,
    used_urls: set | None = None,
    date_seed: str = "",
) -> str:
    """
    Search Unsplash for a relevant landscape photo. Primary image source.

    Unsplash License: https://unsplash.com/license
    - Free for commercial and personal use.
    - No attribution required (appreciated but not mandatory).

    Returns the photo URL (regular ~1080px) or empty string on failure.
    Never raises.
    """
    if not UNSPLASH_ACCESS_KEY:
        return ""

    if used_urls is None:
        used_urls = set()

    query = _image_query(title, categories)
    log.debug(f"  Unsplash query: '{query}'")

    try:
        resp = httpx.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": 30, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=8.0,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])

        if not results:
            log.debug(f"  Unsplash: no results for '{query}'")
            return ""

        start = abs(hash(title + date_seed)) % len(results)
        for i in range(len(results)):
            candidate = results[(start + i) % len(results)]["urls"]["regular"]
            if candidate not in used_urls:
                log.debug(f"  Unsplash photo (slot {(start+i)%len(results)}): {candidate[:80]}")
                return candidate

        log.debug("  Unsplash: all candidates already used, reusing deterministic pick")
        return results[start]["urls"]["regular"]

    except Exception as e:
        log.debug(f"  Unsplash fetch failed: {e}")
        return ""


def fetch_pexels_image(
    title: str,
    categories: list,
    log: logging.Logger,
    used_urls: set | None = None,
    date_seed: str = "",
) -> str:
    """
    Search Pexels for a relevant landscape photo. Fallback image source.

    Pexels License: https://www.pexels.com/license/
    - Free for commercial and personal use.
    - No copyright, no attribution required.

    Returns the photo URL (large ~940px) or empty string on failure.
    Never raises.
    """
    if not PEXELS_API_KEY:
        return ""

    if used_urls is None:
        used_urls = set()

    query = _image_query(title, categories)
    log.debug(f"  Pexels query: '{query}'")

    try:
        resp = httpx.get(
            "https://api.pexels.com/v1/search",
            params={"query": query, "per_page": 30, "orientation": "landscape"},
            headers={"Authorization": PEXELS_API_KEY},
            timeout=8.0,
        )
        resp.raise_for_status()
        photos = resp.json().get("photos", [])

        if not photos:
            log.debug(f"  Pexels: no results for '{query}'")
            return ""

        start = abs(hash(title + date_seed)) % len(photos)
        for i in range(len(photos)):
            candidate = photos[(start + i) % len(photos)]["src"]["large"]
            if candidate not in used_urls:
                log.debug(f"  Pexels photo (slot {(start+i)%len(photos)}): {candidate[:80]}")
                return candidate

        log.debug("  Pexels: all candidates already used, reusing deterministic pick")
        return photos[start]["src"]["large"]

    except Exception as e:
        log.debug(f"  Pexels fetch failed: {e}")
        return ""


def fetch_article_content(url: str, log: logging.Logger) -> tuple[str, str]:
    """
    Attempt to fetch the full article text and og:image.
    Returns (text[:4000], og_image_url) — both may be empty strings on failure.
    Never raises.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; GridTheGrey-Bot/1.0; +https://gridthegrey.com/bot)"
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
You are a senior AI security analyst working for Grid the Grey, an intelligence platform covering adversarial AI, LLM vulnerabilities, and machine learning security threats.

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
  "generated_title": "<SEO-optimised headline for this article. Rules: (1) 50-60 characters total — this is the most important constraint. (2) Front-load the primary keyword (CVE ID, tool name, attack technique, or threat actor). (3) If a CVE number is mentioned, include it — people search for CVE IDs directly. (4) If an affected product or vendor is named, include it. (5) Use plain English, not jargon. (6) Do NOT use clickbait or vague phrases ('This is why...', 'You won't believe...'). (7) Do NOT start with 'How', 'Why', or 'What'. Good examples: 'CVE-2025-59528: Flowise RCE Exploited Across 12,000 Instances', 'Cursor IDE Prompt Injection Enables Full OS Code Execution', 'North Korea Targets OpenAI via Axios Supply Chain Compromise', 'SkillCloak Bypasses AI Agent Skill Scanners at 90% Success Rate'. Bad examples: 'Flowise AI Agent Builder Under Active CVSS 10.0 RCE Exploitation' (too long, CVE buried), 'How Hackers Are Thinking About AI' (vague, starts with How).>",
  "summary": "<2-3 sentence editorial summary focused on the security implications>",
  "threat_level": "<CRITICAL|HIGH|MEDIUM|LOW|NONE>",
  "mitre_techniques": ["<AML.TXXXX - Technique Name>", ...],
  "owasp_categories": ["<LLMXX - Category Name>", ...],
  "categories": ["<from the valid list>", ...],
  "tags": ["<lowercase-hyphenated>", ...],
  "threat_actors": ["<nation-state|cybercriminal|researcher|insider|hacktivist>", ...],
  "tldr_what": "<1 punchy sentence — the core event/finding, no filler, max 20 words>",
  "tldr_who_at_risk": "<1 concise sentence: who is most directly exposed and why>",
  "tldr_actions": ["<short imperative action 1>", "<short imperative action 2>", "<short imperative action 3>"],
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


FIRST_LOOK_PROMPT_TEMPLATE = """\
You are a senior AI security analyst working for Grid the Grey, an intelligence platform that proactively assesses the security implications of new AI capabilities as they ship.

Your task: analyse this newly-released AI capability/feature and map its attack surface to security frameworks.

## Capability Details
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
  "content_type": "first_look",
  "generated_title": "<SEO-optimised headline prefixed with 'First Look:'. Rules: (1) Total length 55-70 characters including 'First Look: '. (2) MUST include the vendor name (Google, OpenAI, Anthropic, Meta, Microsoft, AWS, NVIDIA, etc.) — this is a primary search term. (3) MUST include the product or model name if one is mentioned (e.g. Gemini 2.5, Claude Opus 4, GPT-5). (4) Describe what shipped in plain terms — not the security risk. (5) Use action verbs: Ships, Launches, Releases, Adds, Brings, Opens. Good examples: 'First Look: Anthropic Ships Claude Code with Terminal Access', 'First Look: Google Launches Gemini 2.5 with Agentic File Access', 'First Look: AWS Brings NVIDIA Nemotron to GovCloud'. Bad examples: 'First Look: A New AI Capability Has Arrived' (no vendor, no product), 'First Look: How Google Is Changing AI With Gemini' (starts with How after prefix, too vague).>",
  "summary": "<2-3 sentence editorial summary: first sentence describes the capability neutrally, remaining sentences cover the security implications for defenders>",
  "attack_surface_score": <float 0.0–10.0 — how much does this change the attack surface for defenders?>,
  "adoption_velocity": "<RAPID|MODERATE|GRADUAL|NICHE>",
  "capability_category": "<one of: model-release, api-feature, agent-tooling, developer-sdk, platform-integration, safety-mechanism, open-source-release>",
  "attack_vectors_introduced": ["<concise description of each new attack vector this enables>", ...],
  "threat_level": "<CRITICAL|HIGH|MEDIUM|LOW|NONE>",
  "mitre_techniques": ["<AML.TXXXX - Technique Name>", ...],
  "owasp_categories": ["<LLMXX - Category Name>", ...],
  "categories": ["First Look", "<additional category from the valid list>", ...],
  "tags": ["<lowercase-hyphenated>", ...],
  "threat_actors": ["<who would most likely exploit this: nation-state|cybercriminal|researcher|insider|hacktivist>", ...],
  "tldr_what": "<1 punchy sentence — what shipped or launched, described neutrally. No security framing here. Max 25 words>",
  "tldr_who_at_risk": "<1 concise sentence: who is newly exposed because of this capability>",
  "tldr_actions": ["<short imperative action 1>", "<short imperative action 2>", "<short imperative action 3>"],
  "article_body": "<full markdown article body — see format below>"
}}

## Attack Surface Scoring Guide
- 9-10: Fundamentally new attack surface with no existing mitigations (e.g., first agent with arbitrary code execution)
- 7-8: Significant expansion of existing attack surface or new class of risk (e.g., new model with tool-use that bypasses existing controls)
- 6-7: Meaningful new vectors that defenders should assess (e.g., new API feature chainable with existing attacks)
- 4-5: Minor surface changes, mostly covered by existing defences
- 0-3: No meaningful security implications

## Framework Reference
{mitre_context}
{owasp_context}

## Valid Categories (use only from this list — always include "First Look" as the first category)
{valid_categories}

## Article Body Format
Write the article_body as a markdown string with these sections (include only sections that apply):
- ## Capability Overview — what shipped and why it matters to defenders
- ## Attack Surface Analysis — what new vectors does this introduce? What can an attacker now do that they couldn't before?
- ## Framework Mapping — which ATLAS/OWASP categories apply and why
- ## Threat Scenarios — concrete attack scenarios this enables (be specific)
- ## Defender Checklist — actionable assessment steps for security teams deploying or encountering this capability
- ## References — link back to original source

Keep the body between 400–700 words. Tone: analytical, forward-looking, never celebratory of the capability. Always frame from the defender's perspective.
CRITICAL: If you cannot identify at least one new attack vector, set relevance_score below 4.0 and article_body to an empty string.
"""


CLASSIFY_PROMPT_TEMPLATE = """\
Given this article title and description, classify it as one of:
- "first_look": A NEW AI capability, feature, product, model, or update has shipped or been announced. The security angle is "what attack surface does this create?"
- "threat_report": An active threat, vulnerability, exploit, breach, or attack has been discovered or disclosed.
- "skip": Not relevant to AI security at all.

Return ONLY one word: first_look, threat_report, or skip.

Title: {title}
Description: {description}
"""


def classify_content_type(article: dict, client: Anthropic, log: logging.Logger) -> str:
    """
    Classify article as 'first_look', 'threat_report', or 'skip'.
    Uses keyword heuristics first, falls back to Claude if ambiguous.
    """
    text = (article["title"] + " " + article["description"]).lower()

    fl_hits = sum(1 for kw in FIRST_LOOK_KEYWORDS if kw in text)
    tr_hits = sum(1 for kw in THREAT_REPORT_KEYWORDS if kw in text)

    # Clear signal: one type dominates
    if fl_hits >= 2 and tr_hits == 0:
        log.debug(f"  Classification (heuristic): first_look (fl={fl_hits}, tr={tr_hits})")
        return "first_look"
    if tr_hits >= 2 and fl_hits == 0:
        log.debug(f"  Classification (heuristic): threat_report (fl={fl_hits}, tr={tr_hits})")
        return "threat_report"

    # Ambiguous: ask Claude Haiku with a short, cheap call
    prompt = CLASSIFY_PROMPT_TEMPLATE.format(
        title=article["title"],
        description=article["description"][:500],
    )
    try:
        response = client.messages.create(
            model=CLASSIFY_MODEL,
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}],
        )
        result = response.content[0].text.strip().lower().replace('"', '').replace("'", "")
        if result in ("first_look", "threat_report", "skip"):
            log.debug(f"  Classification (Claude): {result}")
            return result
        log.debug(f"  Classification (Claude): ambiguous response '{result}', defaulting to threat_report")
        return "threat_report"
    except Exception as e:
        log.warning(f"  Classification fallback — Claude call failed: {e}")
        return "threat_report"


def validate_first_look(analysis: dict) -> bool:
    """First Look articles must have framework mappings or attack vectors."""
    has_frameworks = bool(analysis.get("mitre_techniques")) or bool(analysis.get("owasp_categories"))
    has_vectors = bool(analysis.get("attack_vectors_introduced"))
    return has_frameworks or has_vectors


def analyse_with_claude(article: dict, content: str, client: Anthropic, log: logging.Logger) -> dict | None:
    """
    Call Claude API to score and analyse the article.
    Uses prompt caching to reduce cost for the repeated framework context.
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
            cache_control={"type": "ephemeral"},
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


def analyse_first_look(article: dict, content: str, client: Anthropic, log: logging.Logger) -> dict | None:
    """
    Call Claude API with the First Look prompt to assess attack surface of a new capability.
    Uses prompt caching to reduce cost for the repeated framework context.
    Returns parsed dict or None on failure.
    """
    article_text = content if len(content) > 200 else article["description"]
    if not article_text:
        article_text = "(No article content available — analyse based on title and source only)"

    prompt = FIRST_LOOK_PROMPT_TEMPLATE.format(
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
            max_tokens=4096,
            cache_control={"type": "ephemeral"},
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()

        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)
        result["content_type"] = "first_look"
        log.debug(f"  First Look parsed OK. Attack surface: {result.get('attack_surface_score')}")
        return result

    except json.JSONDecodeError as e:
        log.error(f"  ✗ Claude returned invalid JSON (First Look) for '{article['title']}': {e}")
        log.debug(f"  Raw response: {raw[:500]}")
        return None
    except Exception as e:
        log.error(f"  ✗ Claude API error (First Look) for '{article['title']}': {e}")
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


# ── Story deduplication helpers ────────────────────────────────────────────────
# Strategy: entity + event-type fingerprint.
# An article is a duplicate if it shares at least one SPECIFIC named entity AND
# at least one event type with an existing post/draft from the past STORY_WINDOW_DAYS.
# "Broad" platform names (aws, google…) alone aren't specific enough — they require
# 2+ shared event types to fire, preventing false positives across unrelated stories.

_STORY_ENTITIES = {
    "anthropic", "openai", "google", "deepmind", "microsoft", "nvidia",
    "cloudflare", "aws", "amazon", "apple", "meta", "huggingface", "github",
    "cisco", "crowdstrike", "samsung", "sagemaker", "bedrock", "claude",
    "chatgpt", "gemini", "llama", "mistral", "fable", "mythos", "copilot",
    "codex", "talos", "adobe", "agentcore", "difytap", "apertus", "vbdec",
    "trail", "hermes", "glm", "swiss",
}

# Platform names that appear in many unrelated stories — require stronger signal
_BROAD_ENTITIES = frozenset({"aws", "amazon", "google", "microsoft", "meta", "openai"})

_EVENT_SYNONYMS = {
    "ban": "restriction",       "bans": "restriction",       "banned": "restriction",
    "export": "restriction",    "controls": "restriction",   "restricted": "restriction",
    "shutdown": "restriction",  "blocked": "restriction",    "sanctions": "restriction",
    "jailbreak": "bypass",      "bypass": "bypass",          "guardrail": "bypass",
    "vulnerability": "vuln",    "flaw": "vuln",              "exploit": "vuln",
    "cve": "vuln",              "zero-day": "vuln",
    "breach": "breach",         "leak": "breach",            "exfiltration": "breach",
    "stolen": "breach",         "theft": "breach",
    "malware": "malware",       "trojan": "malware",         "backdoor": "malware",
    "ransomware": "malware",    "botnet": "malware",
    "supply": "supply-chain",   "chain": "supply-chain",     "trojan": "supply-chain",
    "launch": "release",        "launches": "release",       "releases": "release",
    "ships": "release",         "announces": "release",      "rolls": "release",
    "deploys": "release",       "introduces": "release",     "unveils": "release",
    "temporary": "temp-accounts",  "accountless": "temp-accounts",
    "identity": "identity",     "verification": "identity",  "credential": "identity",
    "injection": "prompt-injection",
    "poisoning": "data-poisoning",
}

_STORY_MIN_TOKENS = 2  # minimum tokens to bother comparing


def _story_fingerprint(title: str) -> tuple[frozenset, frozenset]:
    """Return (entities, event_types) extracted from a title."""
    words = re.findall(r"[a-z0-9]+", title.lower())
    entities = frozenset(w for w in words if w in _STORY_ENTITIES)
    events = frozenset(_EVENT_SYNONYMS[w] for w in words if w in _EVENT_SYNONYMS)
    return entities, events


def _fingerprint_match(title_a: str, title_b: str, url_a: str = "", url_b: str = "") -> bool:
    """Return True if the two titles describe the same story."""
    if url_a and url_b and canonicalize_url(url_a) == canonicalize_url(url_b):
        return True
    e1, ev1 = _story_fingerprint(title_a)
    e2, ev2 = _story_fingerprint(title_b)
    shared_entities = e1 & e2
    shared_events = ev1 & ev2
    if not shared_entities or not shared_events:
        return False
    # Broad-only entity match needs 2+ shared event types to avoid false positives
    specific_shared = shared_entities - _BROAD_ENTITIES
    if not specific_shared and len(shared_events) < 2:
        return False
    return True


def build_story_index(log: logging.Logger) -> list[tuple[str, str]]:
    """
    Build a list of (title, filepath) for existing posts/drafts within STORY_WINDOW_DAYS.
    Used to fingerprint-match incoming articles against already-published content.
    """
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=STORY_WINDOW_DAYS)
    date_prefix_re = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
    index = []
    for search_dir in [HUGO_POSTS_DIR, HUGO_DRAFTS_DIR]:
        if not search_dir.exists():
            continue
        for f in search_dir.glob("*.md"):
            if f.stem == "_index":
                continue
            m = date_prefix_re.match(f.stem)
            if not m:
                continue
            try:
                file_date = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if file_date < cutoff:
                continue
            try:
                head = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]
            except OSError:
                continue
            for line in head:
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"').strip("'")
                    e, ev = _story_fingerprint(title)
                    if e or ev:
                        index.append((title, str(f)))
                    break
    log.info(f"Story index: {len(index)} posts/drafts from last {STORY_WINDOW_DAYS} days")
    return index


def build_source_url_index() -> set:
    """
    Return a set of all original_url values recorded in existing posts and drafts.
    Catches the case where the same article URL entered the pipeline via two different feeds.
    """
    url_re = re.compile(r'^original_url:\s*"?([^"\n]+)"?', re.MULTILINE)
    urls: set = set()
    for search_dir in [HUGO_POSTS_DIR, HUGO_DRAFTS_DIR]:
        if not search_dir.exists():
            continue
        for f in search_dir.glob("*.md"):
            if f.stem == "_index":
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                m = url_re.search(text)
                if m:
                    urls.add(canonicalize_url(m.group(1).strip()))
            except OSError:
                continue
    return urls


def is_story_duplicate(title: str, story_index: list[tuple[str, str]], log: logging.Logger) -> bool:
    """Return True if this title matches an already-indexed story via entity+event fingerprint."""
    e, ev = _story_fingerprint(title)
    if not e and not ev:
        return False  # no signal to compare — let it through
    for existing_title, filepath in story_index:
        if _fingerprint_match(title, existing_title):
            log.info(f"  ↓ Story duplicate: matches '{Path(filepath).name}'")
            return True
    return False


def to_yaml_list(items: list | None) -> str:
    """Convert a Python list to YAML inline list string."""
    if not items:
        return "[]"
    safe = [str(i).replace('"', '\\"') for i in items]
    return "[" + ", ".join(f'"{s}"' for s in safe) + "]"


def generate_hugo_markdown(article: dict, analysis: dict, slug: str) -> str:
    """
    Build the full Hugo markdown file content from article metadata
    and Claude's analysis. Matches the post archetype exactly.
    """
    now = datetime.now(timezone.utc)
    fetch_date = now.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    source_date = article["published"].strftime("%Y-%m-%dT%H:%M:%S+00:00")

    display_title = analysis.get("generated_title", "").strip() or article["title"]
    content_type = analysis.get("content_type", "threat_report")

    # Build First Look fields section (only included for first_look content)
    first_look_section = ""
    if content_type == "first_look":
        first_look_section = f"""
# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: {analysis.get('attack_surface_score', 0.0)}
adoption_velocity: {json.dumps(analysis.get('adoption_velocity', 'MODERATE'))}
capability_category: {json.dumps(analysis.get('capability_category', ''))}
attack_vectors_introduced: {to_yaml_list(analysis.get('attack_vectors_introduced', []))}
"""
    else:
        first_look_section = """
# ── Content Type ──
content_type: "threat_report"
"""

    front_matter = f"""---
title: {json.dumps(display_title)}
date: {fetch_date}
draft: true
slug: {json.dumps(slug)}

# ── Content metadata ──
summary: {json.dumps(analysis.get('summary', ''))}
source: {json.dumps(article['source'])}
source_url: {json.dumps(article['url'])}
source_title: {json.dumps(article['title'])}
source_date: {source_date}
author: "Grid the Grey Editorial"
thumbnail: {json.dumps(article.get('thumbnail', ''))}
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above
{first_look_section}
# ── AI Security Classification ──
relevance_score: {analysis.get('relevance_score', 0.0)}
threat_level: {json.dumps(analysis.get('threat_level', 'LOW'))}

# ── MITRE ATLAS Techniques ──
mitre_techniques: {to_yaml_list(analysis.get('mitre_techniques', []))}

# ── OWASP LLM Top 10 ──
owasp_categories: {to_yaml_list(analysis.get('owasp_categories', []))}

# ── TL;DR ──
tldr_what: {json.dumps(analysis.get('tldr_what', ''))}
tldr_who_at_risk: {json.dumps(analysis.get('tldr_who_at_risk', ''))}
tldr_actions: {to_yaml_list(analysis.get('tldr_actions', []))}

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
    """Write the markdown file to the Hugo drafts directory. Returns path or None."""
    HUGO_DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{date_prefix}-{slug}.md"
    filepath = HUGO_DRAFTS_DIR / filename

    # If a file with this slug already exists in drafts, skip
    if filepath.exists():
        log.warning(f"  ⚠ Skipping — draft already exists: {filename}")
        return None

    try:
        filepath.write_text(content, encoding="utf-8")
        log.info(f"  ✓ Written: posts/drafts/{filename}")
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
        "feeds_fetched":        0,
        "articles_found":       0,
        "already_seen":         0,
        "prefilter_pass":       0,
        "prefilter_fail":       0,
        "claude_scored":        0,
        "below_threshold":      0,
        "posts_written":        0,
        "first_look_written":   0,
        "threat_report_written": 0,
        "errors":               0,
    }

    # ── Step 1: Fetch feeds ──
    log.info("=" * 60)
    mode = getattr(args, "mode", "all")
    mode_label = {"all": "All feeds", "threat": "Threat feeds only", "first_look": "First-Look feeds only"}[mode]
    log.info(f"STEP 1 — Fetching RSS Feeds  [{mode_label}]")
    log.info("=" * 60)

    if mode == "threat":
        feed_subset = {k for k in RSS_FEEDS if k not in FIRST_LOOK_FEEDS}
    elif mode == "first_look":
        feed_subset = FIRST_LOOK_FEEDS
    else:
        feed_subset = None  # fetch everything

    all_articles = fetch_all_feeds(args.feed, log, feed_subset=feed_subset)
    stats["feeds_fetched"]  = len(feed_subset) if feed_subset else (1 if args.feed else len(RSS_FEEDS))
    stats["articles_found"] = len(all_articles)
    log.info(f"Total articles fetched: {len(all_articles)}")

    # Sort by date descending (newest first). In 'all' mode, interleave first-look
    # and threat sources to maintain ~50/50 balance within the processing window.
    # In single-mode runs the list is already homogeneous so interleaving is skipped.
    all_articles.sort(key=lambda a: a["published"], reverse=True)
    if mode == "all":
        fl_articles = [a for a in all_articles if a["source"] in FIRST_LOOK_FEEDS]
        tr_articles = [a for a in all_articles if a["source"] not in FIRST_LOOK_FEEDS]
        interleaved = []
        fi, ti = 0, 0
        while fi < len(fl_articles) or ti < len(tr_articles):
            if fi < len(fl_articles):
                interleaved.append(fl_articles[fi])
                fi += 1
            if ti < len(tr_articles):
                interleaved.append(tr_articles[ti])
                ti += 1
        all_articles = interleaved

    # ── Age filter: drop articles older than MAX_ARTICLE_AGE_DAYS ──
    cutoff = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    from datetime import timedelta
    cutoff -= timedelta(days=MAX_ARTICLE_AGE_DAYS)
    before_age_filter = len(all_articles)
    all_articles = [a for a in all_articles if a["published"] >= cutoff]
    too_old = before_age_filter - len(all_articles)
    if too_old:
        log.info(f"Age filter (>{MAX_ARTICLE_AGE_DAYS} days): dropped {too_old} articles  |  Remaining: {len(all_articles)}")
    stats["articles_found"] = len(all_articles)

    # ── Step 2: Deduplicate ──
    log.info("\nSTEP 2 — Deduplication")

    # Build a set of slugs already on disk (published + drafts) to avoid re-fetching.
    # Filenames may have YYYY-MM-DD- prefix — strip it to get the bare slug.
    existing_slugs: set = set()
    date_prefix_re = re.compile(r"^\d{4}-\d{2}-\d{2}-")
    for search_dir in [HUGO_POSTS_DIR, HUGO_DRAFTS_DIR]:
        if search_dir.exists():
            for f in search_dir.glob("*.md"):
                stem = f.stem
                if stem == "_index":
                    continue
                bare = date_prefix_re.sub("", stem)
                existing_slugs.add(bare)
                existing_slugs.add(stem)  # also keep full name just in case
    log.info(f"Existing posts on disk (published + drafts): {len(existing_slugs)}")

    # Build story fingerprint index (Fix 3) — covers existing posts + drafts within window
    story_index = build_story_index(log)

    # Fix 2: build set of source URLs already recorded in frontmatter (catches feed-alias duplicates)
    source_url_index = build_source_url_index()
    log.info(f"Source URL index: {len(source_url_index)} original_url values on disk")

    new_articles = []
    batch_seen: set[str] = set()  # tracks URLs added to new_articles this run
    for a in all_articles:
        if a["url"] in seen_urls:
            stats["already_seen"] += 1
        # check if this exact URL is already recorded as original_url in a post/draft
        elif a["url"] in source_url_index:
            log.info(f"  Skipping (original_url on disk): {a['url'][:80]}")
            seen_urls.add(a["url"])
            stats["already_seen"] += 1
        # check if this URL already appeared from another feed in this same run
        elif a["url"] in batch_seen:
            log.info(f"  Skipping (duplicate URL in this run): {a['url'][:80]}")
            seen_urls.add(a["url"])
            stats["already_seen"] += 1
        else:
            # Check original-title slug against disk (existing guard)
            candidate_slug = build_slug(a["title"], a["published"])
            if candidate_slug in existing_slugs:
                log.info(f"  Skipping (slug exists on disk): {candidate_slug}")
                seen_urls.add(a["url"])
                stats["already_seen"] += 1
            # story fingerprint check — same event from a different source
            elif is_story_duplicate(a["title"], story_index, log):
                seen_urls.add(a["url"])
                stats["already_seen"] += 1
            else:
                batch_seen.add(a["url"])
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

    # ── Step 4: Classify + Claude scoring ──
    log.info(f"\nSTEP 4 — Classify & Analyse  (threat threshold: {RELEVANCE_THRESHOLD}, first look threshold: {FIRST_LOOK_THRESHOLD})")
    log.info("=" * 60)

    # Pre-load recently used thumbnails to avoid image repeats
    recent_thumbnails = get_recent_thumbnails(n=50)
    log.debug(f"  Recent thumbnails loaded: {len(recent_thumbnails)}")

    for i, article in enumerate(candidate_articles, 1):
        log.info(f"\n[{i}/{len(candidate_articles)}] {article['title'][:80]}")
        log.info(f"  Source: {article['source']}  |  {article['published'].strftime('%Y-%m-%d')}")

        # Always mark as seen, regardless of outcome
        seen_urls.add(article["url"])

        # Optionally fetch full article content
        full_content = ""
        if FETCH_FULL_CONTENT and not args.dry_run:
            log.debug(f"  Fetching full content from {article['url']}")
            full_content, _og_image = fetch_article_content(article["url"], log)
            if full_content:
                log.debug(f"  Content fetched: {len(full_content)} chars")

        if args.dry_run:
            log.info("  [DRY RUN] Would call Claude API here — skipping")
            stats["claude_scored"] += 1
            continue

        # ── Classify content type ──
        content_type = classify_content_type(article, client, log)
        if content_type == "skip":
            log.info("  ↓ Classified as 'skip' — not AI security relevant")
            stats["below_threshold"] += 1
            continue
        log.info(f"  Type: {content_type.upper().replace('_', ' ')}")

        # ── Call Claude with appropriate prompt ──
        if content_type == "first_look":
            analysis = analyse_first_look(article, full_content, client, log)
        else:
            analysis = analyse_with_claude(article, full_content, client, log)

        if analysis is None:
            stats["errors"] += 1
            continue

        # Fetch thumbnail: Unsplash (primary) → Pexels (fallback)
        categories = analysis.get("categories", [])
        title_for_image = analysis.get("generated_title", "") or article["title"]
        date_seed = article["published"].strftime("%Y-%m-%d")
        log.debug(f"  Fetching thumbnail (categories: {categories})")
        thumbnail = fetch_unsplash_image(title_for_image, categories, log, used_urls=recent_thumbnails, date_seed=date_seed)
        if thumbnail:
            log.debug(f"  Unsplash image: {thumbnail[:80]}")
            recent_thumbnails.add(thumbnail)
        else:
            log.debug(f"  Unsplash returned nothing, trying Pexels")
            thumbnail = fetch_pexels_image(title_for_image, categories, log, used_urls=recent_thumbnails, date_seed=date_seed)
            if thumbnail:
                log.debug(f"  Pexels image: {thumbnail[:80]}")
                recent_thumbnails.add(thumbnail)
        article["thumbnail"] = thumbnail

        stats["claude_scored"] += 1
        score = analysis.get("relevance_score", 0.0)

        # ── Apply type-specific threshold ──
        if content_type == "first_look":
            threshold = FIRST_LOOK_THRESHOLD
            attack_score = analysis.get("attack_surface_score", 0.0)
            log.info(f"  Score: {score:.1f}  |  Attack Surface: {attack_score:.1f}  |  Velocity: {analysis.get('adoption_velocity', '?')}")

            # First Look validation gate
            if not validate_first_look(analysis):
                log.info("  ↓ First Look rejected — missing framework mappings or attack vectors")
                stats["below_threshold"] += 1
                continue
        else:
            threshold = RELEVANCE_THRESHOLD
            log.info(f"  Score: {score:.1f}  |  Threat: {analysis.get('threat_level', '?')}  |  Relevant: {analysis.get('is_ai_security_relevant')}")

        if score < threshold:
            log.info(f"  ↓ Below threshold ({score:.1f} < {threshold}) — skipping")
            stats["below_threshold"] += 1
            continue

        # Log framework mapping
        mitre = analysis.get("mitre_techniques", [])
        owasp = analysis.get("owasp_categories", [])
        if mitre:
            log.info(f"  ATLAS: {', '.join(mitre[:2])}{'...' if len(mitre) > 2 else ''}")
        if owasp:
            log.info(f"  OWASP: {', '.join(owasp[:2])}{'...' if len(owasp) > 2 else ''}")

        # Generate slug from Claude's title (may differ from original RSS title)
        slug_title = analysis.get("generated_title", "").strip() or article["title"]
        slug = build_slug(slug_title, article["published"])

        # Fix 1: check generated slug against disk index before writing
        if slug in existing_slugs:
            log.info(f"  ↓ Skipping — generated slug already on disk: {slug}")
            stats["already_seen"] += 1
            # Fix 4: flush so this URL won't be re-processed if pipeline restarts
            if not args.dry_run:
                flush_seen_urls(SEEN_URLS_FILE, seen_urls)
            time.sleep(1.0)
            continue

        # Fix 3b: also story-check against generated title (catches renamed variants)
        if is_story_duplicate(slug_title, story_index, log):
            seen_urls.add(article["url"])
            stats["already_seen"] += 1
            if not args.dry_run:
                flush_seen_urls(SEEN_URLS_FILE, seen_urls)
            time.sleep(1.0)
            continue

        markdown = generate_hugo_markdown(article, analysis, slug)
        written = write_hugo_post(slug, markdown, log)
        if written:
            stats["posts_written"] += 1
            if content_type == "first_look":
                stats["first_look_written"] += 1
            else:
                stats["threat_report_written"] += 1
            # Add new slug to index so subsequent articles in the same run can see it
            existing_slugs.add(slug)
            # Fix 3c: add to story index so same-run duplicates are also caught
            e, ev = _story_fingerprint(slug_title)
            if e or ev:
                story_index.append((slug_title, slug))
        else:
            stats["errors"] += 1

        # Fix 4: flush seen_urls after each scored article so crashes don't lose progress
        if not args.dry_run:
            flush_seen_urls(SEEN_URLS_FILE, seen_urls)

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
    log.info(f"    ├─ Threat reports:    {stats['threat_report_written']}")
    log.info(f"    └─ First Look:        {stats['first_look_written']}")
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
        description="Grid the Grey — RSS-to-Hugo Pipeline",
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
        "--mode", type=str, default="all", choices=["all", "threat", "first_look"],
        help=(
            "Which article type to fetch and process. "
            "'all' (default) = full pipeline as normal; "
            "'threat' = security/threat feeds only; "
            "'first_look' = AI capability/vendor feeds only."
        ),
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
    log.info("║     GRID THE GREY  —  RSS Pipeline     ║")
    log.info(f"║     v{PIPELINE_VERSION}  |  {CLAUDE_MODEL:<22}║")
    log.info("╚══════════════════════════════════════╝")
    log.info(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}  |  Threshold: {RELEVANCE_THRESHOLD}  |  Max articles: {args.limit or MAX_ARTICLES}")

    run_pipeline(args, log)
