# SENTINEL AI — Automated AI Security Intelligence

> Real-time AI threat intelligence mapped to MITRE ATLAS and OWASP LLM Top 10.

**Live site:** https://bansac1981.github.io/sentinel-ai/  
**Newsletter:** https://sentinel-ai.beehiiv.com/subscribe

---

## What It Does

SENTINEL AI monitors 9 curated security RSS feeds, scores each article with Claude AI for relevance to AI/ML security (threshold 6.0/10), and publishes the best ones to a Hugo static site deployed on GitHub Pages. Every article is mapped to MITRE ATLAS techniques and OWASP LLM Top 10 categories.

The pipeline runs automatically every day at 9:30 AM IST via GitHub Actions.

---

## Architecture

```
9 RSS feeds
    │
    ▼
pipeline.py  ──── Claude API (relevance scoring + framework mapping)
    │
    ▼
hugo-site/content/posts/*.md  (draft: true)
    │
    ▼  (after review: set draft: false, push)
GitHub Actions deploy.yml
    │
    ▼
https://bansac1981.github.io/sentinel-ai/
    │
    ▼
newsletter_digest.py  ──►  Beehiiv (weekly email)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Static site | Hugo (extended, latest) |
| Theme | Custom (no external theme) |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| AI scoring | Claude API (claude-sonnet-4-6) |
| Newsletter | Beehiiv (free tier) |
| Python | 3.12 |

---

## Project Structure

```
sentinel-ai/
├── pipeline.py              # Main pipeline: fetch → score → write posts
├── newsletter_digest.py     # Generate weekly HTML digest for Beehiiv
├── requirements.txt         # Python dependencies
├── seen_urls.json           # Deduplication state (committed to repo)
├── .env                     # Local secrets (gitignored)
├── .env.example             # Template for .env
├── BEEHIIV_SETUP.md         # Beehiiv integration guide
├── PROJECT_STATE.md         # Quick reference for dev sessions
├── .github/
│   └── workflows/
│       ├── deploy.yml       # Hugo build + GitHub Pages deploy
│       └── pipeline.yml     # Daily cron pipeline + manual dispatch
└── hugo-site/
    ├── hugo.toml            # Site config, menus, output formats
    ├── content/
    │   ├── posts/           # All articles (pipeline writes here)
    │   ├── categories/      # Category description pages
    │   └── about.md         # About page
    ├── layouts/             # All Hugo templates (no external theme)
    │   ├── index.html       # Homepage
    │   ├── index.rss.xml    # Custom RSS template (posts only)
    │   ├── _default/
    │   │   ├── single.html  # Article page
    │   │   └── list.html    # Category/section list
    │   └── partials/
    │       ├── header.html
    │       ├── footer.html
    │       ├── sidebar.html
    │       ├── ticker.html
    │       └── article-image.html
    ├── static/
    │   ├── css/sentinel.css # All styles
    │   └── img/             # Favicon, static images
    └── data/
        ├── ticker.json      # Live threat ticker items
        ├── threats.json     # Threat radar data
        ├── frameworks.json  # Framework index data
        └── stats.json       # Site stats widget
```

---

## Setup from Scratch

### Prerequisites

- Python 3.12+
- Git
- A GitHub account
- An Anthropic API key (get one at console.anthropic.com)
- Hugo extended (latest) — for local preview only

### Step 1: Clone and configure

```bash
git clone https://github.com/bansac1981/sentinel-ai.git
cd sentinel-ai

# Install Python dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
```

Edit `.env` and add your key:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Step 2: Run a dry run to verify the pipeline

```bash
python pipeline.py --dry-run
```

You should see output like:
```
[pipeline] Fetching from 9 feeds...
[pipeline] 170 articles fetched, 41 passed keyword filter
[pipeline] DRY RUN — no posts written, no API calls made
```

### Step 3: Run the pipeline for real

```bash
# Limit to 3 articles on your first run (saves API credits)
python pipeline.py --limit 3
```

New `.md` files will appear in `hugo-site/content/posts/` with `draft: true`.

### Step 4: Review and publish articles

Open the generated markdown files. Each has:
- `relevance_score` — Claude's score out of 10
- `threat_level` — CRITICAL / HIGH / MEDIUM / LOW
- `mitre_techniques` — mapped MITRE ATLAS techniques
- `owasp_categories` — mapped OWASP LLM Top 10 categories
- `draft: true` — change to `false` to publish

```bash
# Preview locally (requires Hugo)
cd hugo-site
hugo server -D   # -D shows drafts
# Open http://localhost:1313/sentinel-ai/
```

### Step 5: Push to deploy

```bash
git add .
git commit -m "publish: [article title]"
git push
```

GitHub Actions will build and deploy automatically. The live site updates in ~2 minutes.

---

## GitHub Actions Setup

Two workflows run in this repo:

### deploy.yml — triggered on push to `hugo-site/**`

Builds the Hugo site and deploys to GitHub Pages. No secrets required.

**One-time GitHub setup:**
1. Go to repo **Settings → Pages**
2. Set **Source** to `GitHub Actions`

### pipeline.yml — runs daily at 9:30 AM IST (04:00 UTC)

Fetches RSS feeds, scores with Claude API, writes draft posts.

**Required GitHub secret:**
1. Go to repo **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: your Anthropic API key

**Optional GitHub variables** (have defaults in the workflow):

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Claude model to use |
| `RELEVANCE_THRESHOLD` | `6.0` | Minimum score to publish |
| `MAX_ARTICLES_PER_RUN` | `20` | Max articles per pipeline run |

Set these at **Settings → Secrets and variables → Actions → Variables**.

### Manual pipeline trigger

Go to **Actions → SENTINEL AI Pipeline → Run workflow** to run manually. You can optionally set:
- `limit` — max articles to process
- `dry_run` — test without writing posts or using API credits
- `feed` — run on a single feed only

---

## RSS Feed Sources

| Key | Source | URL |
|-----|--------|-----|
| `thehackernews` | The Hacker News | https://feeds.feedburner.com/TheHackersNews |
| `securityweek` | SecurityWeek | https://www.securityweek.com/feed/ |
| `darkreading` | Dark Reading | https://www.darkreading.com/rss.xml |
| `crowdstrike` | CrowdStrike Blog | https://www.crowdstrike.com/en-us/blog/feed |
| `sans_isc` | SANS Internet Storm Center | https://isc.sans.edu/rssfeed_full.xml |
| `hn_ai_security` | HN AI Security | https://hnrss.org/newest?q=AI+security+OR+LLM+vulnerability+OR+prompt+injection&points=50 |
| `schneier` | Schneier on Security | https://www.schneier.com/feed/ |
| `projectzero` | Google Project Zero | https://googleprojectzero.blogspot.com/feeds/posts/default |
| `krebsonsecurity` | Krebs on Security | https://krebsonsecurity.com/feed/ |

To add a new feed, add an entry to the `RSS_FEEDS` dict in `pipeline.py` and add the key to the `options` list in `.github/workflows/pipeline.yml`.

---

## Newsletter

### Generating a weekly digest

```bash
python newsletter_digest.py --days 7 --output this_week.html
```

Opens `this_week.html` — a fully formatted dark-theme HTML email with:
- Lead story (highest scored article, with thumbnail)
- Up to 7 secondary stories with summaries
- MITRE ATLAS and OWASP tags on each article
- Categories breakdown and CTA to the site

### Publishing to Beehiiv

1. Beehiiv → **New Post → New Email**
2. Subject: `SENTINEL AI Threat Briefing — Week of [DATE]`
3. Add an **HTML block** → paste contents of `this_week.html`
4. Preview, then **Send** or **Schedule**

Full guide: see `BEEHIIV_SETUP.md`

---

## Configuration Reference

All site config is in `hugo-site/hugo.toml`.

### Key parameters

```toml
baseURL = "https://bansac1981.github.io/sentinel-ai/"

[params]
  newsletterURL = "https://sentinel-ai.beehiiv.com/subscribe"
  scoreThreshold = 6.0      # Minimum Claude relevance score to publish
  enableTicker = true       # Live threat ticker bar
  enableThreatRadar = true  # Threat radar sidebar widget
```

### Sidebar data files

| File | Controls |
|------|----------|
| `data/ticker.json` | 10 scrolling threat items in the ticker bar |
| `data/threats.json` | 5 items in the threat radar widget |
| `data/frameworks.json` | Framework index sidebar widget |
| `data/stats.json` | Stats counter widget |

---

## Moving to a Custom Domain

When you get a custom domain (e.g., `gard.ai`):

1. **`hugo-site/hugo.toml`** — update `baseURL = "https://gard.ai/"`
2. **`.github/workflows/deploy.yml`** — update `--baseURL "https://gard.ai/"`
3. **GitHub Pages settings** — add your custom domain
4. **Beehiiv** → Settings → Website URL → update to new domain

> **Note:** Do NOT use `actions/configure-pages` to auto-detect the baseURL — it returns the GitHub Pages subdirectory URL without the `/sentinel-ai/` prefix, which breaks all internal links. Always hardcode the baseURL in both places above.

---

## Common Commands

```bash
# Test pipeline without API cost
python pipeline.py --dry-run

# Run pipeline, one feed only
python pipeline.py --feed securityweek --limit 5

# Preview site locally (shows drafts)
cd hugo-site && hugo server -D

# Generate newsletter digest
python newsletter_digest.py --days 7 --output digest.html

# Force rebuild on GitHub Actions (without a code change)
# Go to Actions → Deploy → Run workflow
```

---

## Troubleshooting

**Links go to `github.io/` without `/sentinel-ai/`**  
Hugo's `relURL` breaks with leading-slash inputs. Never use `{{ "/posts/" | relURL }}`. Use `{{ "posts/" | relURL }}` (no leading slash) or `{{ .Site.Home.RelPermalink }}` for the home link. See `PROJECT_STATE.md` for full details.

**Pipeline fails with `ANTHROPIC_API_KEY not set`**  
Add the secret at: repo Settings → Secrets and variables → Actions → New repository secret.

**Hugo build error: `theme not found`**  
Make sure there is no `theme = "..."` line in `hugo.toml`. The site uses custom layouts only — the theme line must be absent entirely.

**`seen_urls.json` is growing large**  
This is expected — it stores all seen article URLs for deduplication. It's committed to the repo so GitHub Actions can maintain state between runs. It can be safely trimmed if needed (remove older entries).

**Posts not appearing on site**  
Check that `draft: false` is set in the post's frontmatter. The pipeline writes `draft: true` by default — you must review and change it to publish.

---

## License

MIT — see LICENSE file.
