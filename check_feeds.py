#!/usr/bin/env python3
"""
check_feeds.py — Validate RSS feed URLs before adding to pipeline
Run: python check_feeds.py
"""

import urllib.request
import urllib.error
import socket

FEEDS_TO_CHECK = [
    # AI Vendors (OpenAI + Anthropic have no public RSS — using HN filters instead)
    ("OpenAI via HN filter",     "https://hnrss.org/newest?q=OpenAI+security&points=30"),
    ("Anthropic via HN filter",  "https://hnrss.org/newest?q=Anthropic+Claude+security&points=30"),
    ("Google DeepMind (alt)",    "https://blog.google/technology/ai/rss/"),
    ("Microsoft AI Blog",        "https://blogs.microsoft.com/ai/feed/"),

    # Security Vendors
    ("Palo Alto Unit 42",        "https://unit42.paloaltonetworks.com/feed/"),
    ("Cisco Talos (alt)",        "https://blog.talosintelligence.com/rss"),
    ("Microsoft Security Blog",  "https://www.microsoft.com/en-us/security/blog/feed/"),
    ("SentinelOne",              "https://www.sentinelone.com/blog/feed/"),
    ("Mandiant",                 "https://www.mandiant.com/resources/blog/rss.xml"),
    ("Qualys",                   "https://blog.qualys.com/feed"),

    # Agencies
    ("NCSC UK",                  "https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml"),
    ("ENISA (alt)",              "https://www.enisa.europa.eu/news/enisa-news/rss"),

    # Must-adds
    ("BleepingComputer",         "https://www.bleepingcomputer.com/feed/"),
    ("IBM X-Force (alt)",        "https://securityintelligence.com/articles/feed/"),
    ("Check Point Research",     "https://research.checkpoint.com/feed/"),
    ("Simon Willison",           "https://simonwillison.net/atom/everything/"),
    ("Hugging Face Blog",        "https://huggingface.co/blog/feed.xml"),

    # Good to have
    ("Wired Security",           "https://www.wired.com/feed/category/security/latest/rss"),
    ("Ars Technica (alt)",       "https://arstechnica.com/security/feed/"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (RSS feed validator)"}
TIMEOUT = 10

def check_feed(name, url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.status
            content = resp.read(800).decode("utf-8", errors="replace")
            is_feed = any(tag in content for tag in ["<rss", "<feed", "<channel", "<?xml"])
            return status, is_feed, None
    except urllib.error.HTTPError as e:
        return e.code, False, str(e)
    except urllib.error.URLError as e:
        return 0, False, str(e.reason)
    except socket.timeout:
        return 0, False, "Timeout"
    except Exception as e:
        return 0, False, str(e)

print(f"\n{'Source':<28} {'Status':<8} {'Valid Feed':<12} {'Notes'}")
print("─" * 75)

ok = []
broken = []

for name, url in FEEDS_TO_CHECK:
    status, is_feed, error = check_feed(name, url)
    if status == 200 and is_feed:
        mark = "✓ YES"
        ok.append((name, url))
    else:
        mark = "✗ NO"
        broken.append((name, url, status, error))
    notes = error or (f"HTTP {status}" if status != 200 else "")
    print(f"{name:<28} {str(status):<8} {mark:<12} {notes}")

print("─" * 75)
print(f"\n✓ Valid: {len(ok)}   ✗ Broken/blocked: {len(broken)}\n")

if broken:
    print("Broken feeds — need correct URLs:")
    for name, url, status, error in broken:
        print(f"  {name}: {url}")
        if error:
            print(f"    → {error}")
