#!/usr/bin/env python3
"""
Grid the Grey — Weekly Newsletter Digest Generator
================================================
Reads Hugo content/posts/ from the last N days, ranks by relevance score,
and generates a formatted HTML digest ready to paste into Beehiiv.

Usage:
    python newsletter_digest.py                  # last 7 days
    python newsletter_digest.py --days 14        # last 14 days
    python newsletter_digest.py --output digest.html  # save to file

Output: HTML email body (paste into Beehiiv's HTML block editor)
"""

import argparse
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

# Beehiiv-safe colours (inline CSS only — no external stylesheets)
# Matches Grid the Grey dark editorial theme
ACCENT          = "#ff3b3b"    # Red accent
BG_DARK         = "#0a0a0f"    # Deep black background
BG_CARD         = "#141419"    # Card background (slightly lighter than primary)
TEXT_MUTED      = "#7a7a8c"    # Neutral grey (no purple tint)
TEXT_BODY       = "#c8c8d8"    # Body text
TEXT_HEAD       = "#f0f0ff"    # Heading text
BORDER          = "#252535"    # Border / divider color

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
    result = {}

    def _get(key):
        p = re.search(rf"^{key}:\s*(.+)$", raw, re.MULTILINE)
        return p.group(1).strip().strip('"').strip("'") if p else ""

    def _get_list(key):
        # handles both inline ["a","b"] and YAML list blocks
        inline = re.search(rf"^{key}:\s*\[(.+?)\]", raw, re.MULTILINE)
        if inline:
            return [x.strip().strip('"').strip("'")
                    for x in inline.group(1).split(",")]
        block = re.findall(rf"^{key}:\s*\n((?:\s+-\s+.+\n?)+)", raw, re.MULTILINE)
        if block:
            return [re.sub(r'^\s+-\s+"?(.+?)"?\s*$', r'\1', l)
                    for l in block[0].splitlines()]
        return []

    result["title"]           = _get("title")
    result["date"]            = _get("date")
    result["summary"]         = _get("summary")
    result["source"]          = _get("source")
    result["source_url"]      = _get("source_url")
    result["threat_level"]    = _get("threat_level")
    result["relevance_score"] = float(_get("relevance_score") or 0)
    result["thumbnail"]       = _get("thumbnail")
    result["draft"]           = _get("draft").lower() == "true"
    result["mitre_techniques"] = _get_list("mitre_techniques")
    result["owasp_categories"] = _get_list("owasp_categories")
    result["categories"]       = _get_list("categories")

    # Parse slug from filename
    return result


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s


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

        # Parse date
        date_str = fm.get("date", "")
        try:
            # Handle various date formats
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

        fm["pub_date"]   = pub_date
        fm["slug"]       = md_file.stem
        fm["url"]        = f"{SITE_URL}/posts/{md_file.stem}/"
        posts.append(fm)

    # Sort by relevance score descending
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

    # Category breakdown
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
      {len(posts)} stor{'y' if len(posts)==1 else 'ies'} this week
    </p>
  </td></tr>

  <!-- INTRO -->
  <tr><td style="padding:20px 0;">
    <p style="margin:0;font-size:14px;line-height:1.6;color:{TEXT_BODY};">
      Your weekly digest of the most critical AI security developments —
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
       color:{TEXT_MUTED};letter-spacing:0.15em;">── MORE THIS WEEK ──────────────────────────────</p>
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
      GRID THE GREY · AI Security News ·
      <a href="{SITE_URL}" style="color:{TEXT_MUTED};">gridthegrey.com</a>
    </p>
    <p style="margin:0;font-size:11px;color:{TEXT_MUTED};">
      Content aggregated from public sources for research and educational purposes.
    </p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate Grid the Grey weekly newsletter digest"
    )
    parser.add_argument("--days",   type=int, default=7,
                        help="Look back N days for posts (default: 7)")
    parser.add_argument("--output", type=str, default=None,
                        help="Save HTML to this file (default: print to stdout)")
    args = parser.parse_args()

    print(f"[newsletter] Scanning posts from last {args.days} days…", file=sys.stderr)
    posts = load_posts(args.days)

    if not posts:
        print(f"[newsletter] No published posts found in the last {args.days} days.",
              file=sys.stderr)
        print("[newsletter] Try: python newsletter_digest.py --days 30", file=sys.stderr)
        sys.exit(1)

    print(f"[newsletter] Found {len(posts)} posts. Building digest…", file=sys.stderr)
    html = build_html(posts, args.days)

    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
        print(f"[newsletter] Saved to {args.output}", file=sys.stderr)
    else:
        print(html)

    print(f"[newsletter] Done. Lead story: {posts[0]['title'][:60]}…", file=sys.stderr)
    print(f"[newsletter] Stories included: {len(posts)}", file=sys.stderr)


if __name__ == "__main__":
    main()
