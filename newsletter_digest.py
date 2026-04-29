#!/usr/bin/env python3
"""
Grid the Grey — Newsletter Digest Generator (Mailerlite edition)
================================================================
Reads Hugo content/posts/ from the last N days, ranks by relevance score,
and either saves HTML locally or sends directly via Mailerlite API.

Usage:
    python newsletter_digest.py                        # last 4 days, print HTML
    python newsletter_digest.py --days 7               # last 7 days
    python newsletter_digest.py --output digest.html   # save to file
    python newsletter_digest.py --send                 # send via Mailerlite API
    python newsletter_digest.py --send --dry-run       # build + validate, skip send

Environment variables (required for --send):
    MAILERLITE_API_KEY   — your Mailerlite API key
    MAILERLITE_LIST_ID   — numeric ID of your subscriber group/list
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

SITE_URL        = "https://gridthegrey.com"
POSTS_DIR       = Path(__file__).parent / "hugo-site" / "content" / "posts"
MAX_STORIES     = 8       # maximum articles in the digest
TOP_STORY_MIN   = 7.5     # minimum score to be the lead story

MAILERLITE_API  = "https://connect.mailerlite.com/api"

# Email-safe colours (inline CSS only — no external stylesheets)
ACCENT          = "#ff3b3b"
BG_DARK         = "#0a0a0f"
BG_CARD         = "#141419"
TEXT_MUTED      = "#7a7a8c"
TEXT_BODY       = "#c8c8d8"
TEXT_HEAD       = "#f0f0ff"
BORDER          = "#252535"

THREAT_COLORS = {
    "CRITICAL": "#ff3b3b",
    "HIGH":     "#ff8c00",
    "MEDIUM":   "#ffd700",
    "LOW":      "#22c55e",
    "INFO":     "#3b82f6",
}

OWASP_SHORT = {
    "LLM01": "Prompt Injection",
    "LLM02": "Insecure Output",
    "LLM03": "Training Data Poisoning",
    "LLM04": "Model DoS",
    "LLM05": "Supply Chain",
    "LLM06": "Sensitive Info Disclosure",
    "LLM07": "Insecure Plugin Design",
    "LLM08": "Excessive Agency",
    "LLM09": "Overreliance",
    "LLM10": "Model Theft",
}

# ─────────────────────────────────────────────────────────────────────────────
# Frontmatter parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields we care about."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}

    raw = m.group(1)

    def _get(key):
        p = re.search(rf"^{key}:\s*(.+)$", raw, re.MULTILINE)
        return p.group(1).strip().strip('"').strip("'") if p else ""

    def _get_list(key):
        inline = re.search(rf"^{key}:\s*\[(.+?)\]", raw, re.MULTILINE)
        if inline:
            return [x.strip().strip('"').strip("'")
                    for x in inline.group(1).split(",")]
        block = re.findall(rf"^{key}:\s*\n((?:\s+-\s+.+\n?)+)", raw, re.MULTILINE)
        if block:
            return [re.sub(r'^\s+-\s+"?(.+?)"?\s*$', r'\1', l)
                    for l in block[0].splitlines()]
        return []

    result = {}
    result["title"]            = _get("title")
    result["date"]             = _get("date")
    result["summary"]          = _get("summary")
    result["source"]           = _get("source")
    result["source_url"]       = _get("source_url")
    result["threat_level"]     = _get("threat_level")
    result["relevance_score"]  = float(_get("relevance_score") or 0)
    result["thumbnail"]        = _get("thumbnail")
    result["draft"]            = _get("draft").lower() == "true"
    result["mitre_techniques"] = _get_list("mitre_techniques")
    result["owasp_categories"] = _get_list("owasp_categories")
    result["categories"]       = _get_list("categories")
    return result


def load_posts(days: int) -> list[dict]:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
    posts = []

    for md_file in POSTS_DIR.glob("*.md"):
        if md_file.name == "_index.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm or fm.get("draft"):
            continue

        date_str = fm.get("date", "")
        try:
            for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S+05:30",
                        "%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"):
                try:
                    pub_date = datetime.strptime(date_str[:25], fmt)
                    if pub_date.tzinfo is None:
                        pub_date = pub_date.replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    continue
            else:
                continue
        except Exception:
            continue

        if pub_date < cutoff:
            continue

        fm["pub_date"] = pub_date
        fm["slug"]     = md_file.stem
        fm["url"]      = f"{SITE_URL}/posts/{md_file.stem}/"
        posts.append(fm)

    posts.sort(key=lambda p: p["relevance_score"], reverse=True)
    return posts[:MAX_STORIES]


# ─────────────────────────────────────────────────────────────────────────────
# HTML builders
# ─────────────────────────────────────────────────────────────────────────────

def threat_badge(level: str) -> str:
    color = THREAT_COLORS.get(level.upper(), TEXT_MUTED)
    return (
        f'<span style="display:inline-block;padding:2px 8px;'
        f'border-radius:3px;font-size:10px;font-weight:700;'
        f'font-family:monospace;letter-spacing:0.1em;'
        f'background:{color}22;color:{color};border:1px solid {color}44;">'
        f'{level.upper()}</span>'
    )


def framework_tags(mitre: list, owasp: list) -> str:
    tags = []
    for t in mitre[:2]:
        code = t.split(" - ")[0] if " - " in t else t
        tags.append(
            f'<span style="display:inline-block;margin:2px;padding:2px 7px;'
            f'border-radius:3px;font-size:10px;font-weight:600;'
            f'font-family:monospace;background:#ff3b3b22;color:#ff8888;'
            f'border:1px solid #ff3b3b44;">{code}</span>'
        )
    for t in owasp[:2]:
        code = t.split(" - ")[0] if " - " in t else t
        tags.append(
            f'<span style="display:inline-block;margin:2px;padding:2px 7px;'
            f'border-radius:3px;font-size:10px;font-weight:600;'
            f'font-family:monospace;background:#3b82f622;color:#93c5fd;'
            f'border:1px solid #3b82f644;">{code}</span>'
        )
    return "".join(tags)


def lead_story_html(p: dict) -> str:
    img_block = ""
    if p.get("thumbnail"):
        img_block = (
            f'<a href="{p["url"]}" style="display:block;margin-bottom:16px;">'
            f'<img src="{p["thumbnail"]}" alt="{p["title"]}" '
            f'style="width:100%;max-height:220px;object-fit:cover;'
            f'border-radius:6px;border:1px solid {BORDER};" /></a>'
        )

    return f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px;">
  <tr><td style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;padding:24px;">
    <p style="margin:0 0 10px 0;font-family:monospace;font-size:10px;
       color:{ACCENT};letter-spacing:0.15em;font-weight:700;">◉ LEAD STORY</p>
    {img_block}
    <p style="margin:0 0 8px 0;">
      {threat_badge(p.get("threat_level","INFO"))}
    </p>
    <h2 style="margin:8px 0 12px 0;font-family:Georgia,serif;font-size:22px;
       font-weight:700;line-height:1.3;color:{TEXT_HEAD};">
      <a href="{p['url']}" style="color:{TEXT_HEAD};text-decoration:none;">{p['title']}</a>
    </h2>
    <p style="margin:0 0 14px 0;font-size:15px;line-height:1.6;color:{TEXT_BODY};">
      {p.get('summary','')}
    </p>
    <p style="margin:0 0 12px 0;">
      {framework_tags(p.get('mitre_techniques',[]), p.get('owasp_categories',[]))}
    </p>
    <p style="margin:0;font-size:12px;color:{TEXT_MUTED};">
      Source: <a href="{p.get('source_url','#')}" style="color:{TEXT_MUTED};"
        target="_blank">{p.get('source','')}</a>
      &nbsp;·&nbsp; Score: {p['relevance_score']}/10
      &nbsp;·&nbsp; {p['pub_date'].strftime('%b %d, %Y')}
    </p>
    <p style="margin:14px 0 0 0;">
      <a href="{p['url']}" style="display:inline-block;padding:10px 20px;
         background:{ACCENT};color:#fff;border-radius:4px;font-size:13px;
         font-weight:700;text-decoration:none;font-family:monospace;
         letter-spacing:0.05em;">READ FULL ANALYSIS →</a>
    </p>
  </td></tr>
</table>"""


def secondary_story_html(p: dict) -> str:
    return f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;">
  <tr><td style="background:{BG_CARD};border:1px solid {BORDER};
     border-radius:6px;padding:16px 20px;">
    <p style="margin:0 0 6px 0;">
      {threat_badge(p.get("threat_level","INFO"))}
      &nbsp;
      {framework_tags(p.get('mitre_techniques',[])[:1], p.get('owasp_categories',[])[:1])}
    </p>
    <h3 style="margin:6px 0 8px 0;font-family:Georgia,serif;font-size:17px;
       font-weight:700;line-height:1.3;color:{TEXT_HEAD};">
      <a href="{p['url']}" style="color:{TEXT_HEAD};text-decoration:none;">{p['title']}</a>
    </h3>
    <p style="margin:0 0 8px 0;font-size:13px;line-height:1.5;color:{TEXT_BODY};">
      {(p.get('summary') or '')[:200]}{'…' if len(p.get('summary','')) > 200 else ''}
    </p>
    <p style="margin:0;font-size:11px;color:{TEXT_MUTED};">
      {p.get('source','')} &nbsp;·&nbsp; {p['pub_date'].strftime('%b %d')}
      &nbsp;·&nbsp;
      <a href="{p['url']}" style="color:{ACCENT};text-decoration:none;">Read more →</a>
    </p>
  </td></tr>
</table>"""


def build_html(posts: list[dict], days: int) -> str:
    if not posts:
        return "<p>No posts found for the given time period.</p>"

    date_range = datetime.now().strftime("%B %d, %Y")
    issue_num  = (datetime.now() - datetime(2024, 1, 1)).days // 7 + 1

    lead      = posts[0] if posts[0]["relevance_score"] >= TOP_STORY_MIN else None
    secondary = posts[1:] if lead else posts

    lead_html      = lead_story_html(lead) if lead else ""
    secondary_html = "".join(secondary_story_html(p) for p in secondary)

    cat_counts: dict[str, int] = {}
    for p in posts:
        for c in p.get("categories", []):
            cat_counts[c] = cat_counts.get(c, 0) + 1
    cat_html = ""
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        slug = re.sub(r"[\s_]+", "-", cat.lower())
        cat_html += (
            f'<a href="{SITE_URL}/categories/{slug}/" '
            f'style="display:inline-block;margin:3px;padding:4px 10px;'
            f'background:{BG_CARD};border:1px solid {BORDER};border-radius:4px;'
            f'font-size:12px;color:{TEXT_BODY};text-decoration:none;">'
            f'{cat} <span style="color:{ACCENT};">({count})</span></a>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Grid the Grey — AI Threat Briefing #{issue_num}</title>
</head>
<body style="margin:0;padding:0;background:{BG_DARK};font-family:'DM Sans',Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding:20px 16px;">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

  <!-- HEADER -->
  <tr><td style="padding:0 0 24px 0;text-align:center;
     border-bottom:1px solid {BORDER};margin-bottom:24px;">
    <p style="margin:0 0 8px 0;font-family:monospace;font-size:11px;
       color:{TEXT_MUTED};letter-spacing:0.15em;">AI SECURITY NEWS · FRAMEWORK ANALYSIS · STRUCTURAL INSIGHT</p>
    <h1 style="margin:0;font-family:monospace;font-size:28px;font-weight:900;
       color:{TEXT_HEAD};letter-spacing:0.05em;">
      GRID THE <span style="color:{ACCENT};">GREY</span>
    </h1>
    <p style="margin:8px 0 0 0;font-size:13px;color:{TEXT_MUTED};">
      Issue #{issue_num} &nbsp;·&nbsp; {date_range} &nbsp;·&nbsp;
      {len(posts)} stor{'y' if len(posts)==1 else 'ies'} this period
    </p>
  </td></tr>

  <!-- INTRO -->
  <tr><td style="padding:20px 0;">
    <p style="margin:0;font-size:14px;line-height:1.6;color:{TEXT_BODY};">
      Your briefing on the most critical AI security developments —
      adversarial ML, LLM vulnerabilities, and supply chain threats,
      mapped to <strong style="color:{TEXT_HEAD};">MITRE ATLAS</strong> and
      <strong style="color:{TEXT_HEAD};">OWASP LLM Top 10</strong>.
    </p>
  </td></tr>

  <!-- LEAD STORY -->
  {lead_html}

  <!-- DIVIDER -->
  <tr><td style="padding:4px 0 20px 0;">
    <p style="margin:0;font-family:monospace;font-size:10px;
       color:{TEXT_MUTED};letter-spacing:0.15em;">── MORE THIS PERIOD ────────────────────────────</p>
  </td></tr>

  <!-- SECONDARY STORIES -->
  <tr><td>
    {secondary_html}
  </td></tr>

  <!-- CATEGORIES -->
  <tr><td style="padding:20px 0;border-top:1px solid {BORDER};">
    <p style="margin:0 0 10px 0;font-family:monospace;font-size:10px;
       color:{TEXT_MUTED};letter-spacing:0.15em;">COVERAGE THIS ISSUE</p>
    {cat_html}
  </td></tr>

  <!-- CTA -->
  <tr><td style="padding:24px;background:{BG_CARD};border:1px solid {BORDER};
     border-radius:8px;text-align:center;margin-top:8px;">
    <p style="margin:0 0 8px 0;font-size:15px;font-weight:700;color:{TEXT_HEAD};">
      Read the full analysis on Grid the Grey
    </p>
    <p style="margin:0 0 16px 0;font-size:13px;color:{TEXT_MUTED};">
      Every article includes MITRE ATLAS technique mapping and OWASP LLM Top 10 categorisation.
    </p>
    <a href="{SITE_URL}" style="display:inline-block;padding:12px 28px;
       background:{ACCENT};color:#fff;border-radius:4px;font-size:14px;
       font-weight:700;text-decoration:none;font-family:monospace;">
      VISIT GRID THE GREY →
    </a>
  </td></tr>

  <!-- FOOTER -->
  <tr><td style="padding:24px 0;text-align:center;
     border-top:1px solid {BORDER};margin-top:24px;">
    <p style="margin:0 0 4px 0;font-size:11px;color:{TEXT_MUTED};">
      GRID THE GREY · AI Security Intelligence ·
      <a href="{SITE_URL}" style="color:{TEXT_MUTED};">gridthegrey.com</a>
    </p>
    <p style="margin:0 0 4px 0;font-size:11px;color:{TEXT_MUTED};">
      Content aggregated from public sources for research and educational purposes.
    </p>
    <p style="margin:0;font-size:11px;color:{TEXT_MUTED};">
      {{{{ unsubscribe }}}}
    </p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# Mailerlite API sender
# ─────────────────────────────────────────────────────────────────────────────

def send_via_mailerlite(html: str, subject: str, dry_run: bool = False) -> bool:
    """Create and immediately send a campaign via Mailerlite API v3."""
    try:
        import httpx
    except ImportError:
        print("[newsletter] ERROR: httpx not installed. Run: pip install httpx",
              file=sys.stderr)
        return False

    api_key = os.environ.get("MAILERLITE_API_KEY", "").strip()
    list_id = os.environ.get("MAILERLITE_LIST_ID", "").strip()

    if not api_key:
        print("[newsletter] ERROR: MAILERLITE_API_KEY environment variable not set.",
              file=sys.stderr)
        return False
    if not list_id:
        print("[newsletter] ERROR: MAILERLITE_LIST_ID environment variable not set.",
              file=sys.stderr)
        return False

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    }

    campaign_name = f"Grid the Grey — {datetime.now().strftime('%Y-%m-%d')}"

    payload = {
        "name":   campaign_name,
        "type":   "regular",
        "emails": [
            {
                "subject":   subject,
                "from_name": "Grid the Grey",
                "from":      "analyst@gridthegrey.com",
                "content":   html,
            }
        ],
        "groups": [list_id],
    }

    if dry_run:
        print(f"[newsletter] DRY RUN — would create campaign: {campaign_name!r}", file=sys.stderr)
        print(f"[newsletter] DRY RUN — subject: {subject!r}", file=sys.stderr)
        print(f"[newsletter] DRY RUN — list ID: {list_id}", file=sys.stderr)
        print(f"[newsletter] DRY RUN — HTML length: {len(html):,} chars", file=sys.stderr)
        return True

    # Step 1: create campaign
    print("[newsletter] Creating campaign…", file=sys.stderr)
    try:
        resp = httpx.post(
            f"{MAILERLITE_API}/campaigns",
            headers=headers,
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"[newsletter] ERROR creating campaign: {e.response.status_code}",
              file=sys.stderr)
        print(f"[newsletter] Response: {e.response.text[:500]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[newsletter] ERROR creating campaign: {e}", file=sys.stderr)
        return False

    campaign_id = resp.json().get("data", {}).get("id")
    if not campaign_id:
        print(f"[newsletter] ERROR: no campaign ID in response: {resp.text[:300]}",
              file=sys.stderr)
        return False

    print(f"[newsletter] Campaign created: ID {campaign_id}", file=sys.stderr)

    # Step 2: send immediately
    print("[newsletter] Sending campaign…", file=sys.stderr)
    try:
        send_resp = httpx.post(
            f"{MAILERLITE_API}/campaigns/{campaign_id}/actions/send",
            headers=headers,
            timeout=30.0,
        )
        send_resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"[newsletter] ERROR sending campaign: {e.response.status_code}",
              file=sys.stderr)
        print(f"[newsletter] Response: {e.response.text[:500]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[newsletter] ERROR sending campaign: {e}", file=sys.stderr)
        return False

    print(f"[newsletter] ✓ Campaign sent successfully! ID: {campaign_id}", file=sys.stderr)
    return True


def build_subject(posts: list[dict]) -> str:
    """Build an email subject line from the top story."""
    date_str = datetime.now().strftime("%b %d")
    if posts:
        top_title = posts[0]["title"]
        # Truncate to fit subject line
        if len(top_title) > 60:
            top_title = top_title[:57] + "…"
        return f"[Grid the Grey] {top_title} + {len(posts)-1} more — {date_str}"
    return f"[Grid the Grey] AI Security Briefing — {date_str}"


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate (and optionally send) Grid the Grey newsletter digest"
    )
    parser.add_argument("--days",    type=int,  default=4,
                        help="Look back N days for posts (default: 4)")
    parser.add_argument("--output",  type=str,  default=None,
                        help="Save HTML to this file (default: print to stdout)")
    parser.add_argument("--send",    action="store_true",
                        help="Send via Mailerlite API (requires MAILERLITE_API_KEY + MAILERLITE_LIST_ID)")
    parser.add_argument("--subject", type=str,  default=None,
                        help="Custom email subject (auto-generated if omitted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Build and validate but skip actual API send")
    args = parser.parse_args()

    print(f"[newsletter] Scanning posts from last {args.days} days…", file=sys.stderr)
    posts = load_posts(args.days)

    if not posts:
        print(f"[newsletter] No published posts found in the last {args.days} days.",
              file=sys.stderr)
        print("[newsletter] Try: python newsletter_digest.py --days 14", file=sys.stderr)
        sys.exit(1)

    print(f"[newsletter] Found {len(posts)} posts. Building digest…", file=sys.stderr)
    html = build_html(posts, args.days)

    subject = args.subject or build_subject(posts)
    print(f"[newsletter] Subject: {subject}", file=sys.stderr)

    # Save to file if requested
    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
        print(f"[newsletter] Saved to {args.output}", file=sys.stderr)

    # Send via Mailerlite if requested
    if args.send:
        success = send_via_mailerlite(html, subject, dry_run=args.dry_run)
        if not success:
            sys.exit(1)
    elif not args.output:
        # Default: print HTML to stdout
        print(html)

    print(f"[newsletter] Done. Lead story: {posts[0]['title'][:60]}…", file=sys.stderr)
    print(f"[newsletter] Stories included: {len(posts)}", file=sys.stderr)


if __name__ == "__main__":
    main()
