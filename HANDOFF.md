# GRID THE GREY — AI Agent Handoff Document

**Last updated:** 2026-05-01
**Project name:** Grid the Grey (working name: SENTINEL AI)
**Owner:** Achin Bansal — analyst@gridthegrey.com
**Repo:** https://github.com/bansac1981/sentinel-ai
**Live site:** https://gridthegrey.com
**Local path (Windows):** `C:\Users\admin\projects\Security News Website\AI Security News Website`
**Stable tag:** `v1.0-stable` (git tag, pushed to GitHub)

---

## 1. Project Purpose

An automated AI security news aggregation website targeting CISO-level readers. Every article is scored by Claude for relevance, mapped to MITRE ATLAS techniques and OWASP LLM Top 10 categories, and given a Claude-generated punchy headline. The site also produces a weekly audio briefing (podcast) distributed via Spotify, and sends an automated twice-weekly newsletter via Mailerlite.

Key differentiator: framework mapping (MITRE ATLAS + OWASP LLM Top 10) applied to every article, giving CISOs structured intelligence rather than raw news.

---

## 2. Architecture Overview

```
26 RSS feeds (AI vendors, security vendors, agencies, news)
    │
    ▼
pipeline.py
    ├── Age filter: drops articles older than 7 days
    ├── Keyword pre-filter (no API cost)
    ├── Claude API: relevance score (0-10), catchy title, category,
    │   MITRE/OWASP mapping, TL;DR, summary
    ├── Unsplash API (primary image) → Pexels API (fallback) → OG image
    └── Writes hugo-site/content/posts/drafts/*.md (draft: true)
    │
    ▼  (user reviews drafts, sets draft: false via GitHub Actions UI)
deploy.yml (GitHub Actions)
    ├── auto-publish job: moves draft: false files from drafts/ → posts/
    ├── Hugo build (v0.140.2 extended)
    └── GitHub Pages deploy → https://gridthegrey.com
    │
    ├── newsletter.yml (GitHub Actions — AUTOMATED)
    │       ├── Runs: Tuesday + Friday 9:30 AM IST (04:00 UTC)
    │       ├── newsletter_digest.py --send --days 4
    │       └── Sends via Mailerlite API → subscriber inboxes
    │
    ├── weekly_briefing.py (manual, GitHub Actions: ciso-briefing.yml)
    │       ├── Claude: writes ~450-word spoken script
    │       ├── OpenAI TTS (tts-1-hd, onyx voice): generates MP3
    │       ├── Uploads MP3 to Cloudflare R2
    │       └── Updates hugo.toml + episodes.json → triggers site rebuild
    │
    └── podcast_feed.py → feed.xml on R2 → Spotify (submitted, pending approval)
```

---

## 3. Tech Stack

| Component | Technology | Version/Detail |
|-----------|-----------|----------------|
| Static site | Hugo (extended) | v0.140.2 — hardcoded in deploy.yml |
| Theme | Custom (no external theme) | `hugo-site/layouts/` + `hugo-site/static/css/sentinel.css` |
| Hosting | GitHub Pages | Deploys from `hugo-site/public/` |
| CI/CD | GitHub Actions | 7 workflows (see Section 7) |
| AI scoring | Anthropic Claude | `claude-sonnet-4-6` (configurable via `CLAUDE_MODEL` var) |
| AI backfill | Anthropic Claude | `claude-haiku-4-5-20251001` (backfill_tldr.py — cheap) |
| TTS | OpenAI | `tts-1-hd`, default voice: `onyx` |
| Podcast storage | Cloudflare R2 | S3-compatible, public dev URL |
| Newsletter | **Mailerlite** | Free tier — fully automated, twice weekly |
| Images (primary) | Unsplash API | `urls.regular` (~1080px), `Client-ID` auth |
| Images (fallback) | Pexels API | Fallback if Unsplash returns no result |
| Python | 3.12 | |
| Domain | gridthegrey.com | Custom domain on GitHub Pages |

---

## 4. GitHub Secrets (All Required)

Set at: repo Settings → Secrets and variables → Actions → Repository secrets

| Secret | Used By | Notes |
|--------|---------|-------|
| `ANTHROPIC_API_KEY` | pipeline.yml, ciso-briefing.yml, backfill | Required |
| `OPENAI_API_KEY` | ciso-briefing.yml (produce step) | Required for TTS |
| `R2_ACCOUNT_ID` | ciso-briefing.yml, podcast_feed.py | Cloudflare account ID |
| `R2_ACCESS_KEY_ID` | ciso-briefing.yml, podcast_feed.py | R2 API token |
| `R2_SECRET_ACCESS_KEY` | ciso-briefing.yml, podcast_feed.py | R2 API token secret |
| `R2_BUCKET_NAME` | ciso-briefing.yml, podcast_feed.py | R2 bucket name |
| `R2_PUBLIC_URL` | ciso-briefing.yml, podcast_feed.py | e.g. `https://pub-XXX.r2.dev` |
| `PEXELS_API_KEY` | pipeline.py (image fallback) | Free at pexels.com/api |
| `UNSPLASH_ACCESS_KEY` | pipeline.py (primary images) | Free at unsplash.com/developers |
| `MAILERLITE_API_KEY` | newsletter.yml | Mailerlite API token |
| `MAILERLITE_LIST_ID` | newsletter.yml | Subscriber group ID (numeric) |

Optional GitHub Actions variable (not secret):
- `CLAUDE_MODEL` → defaults to `claude-sonnet-4-6`
- `MAX_ARTICLE_AGE_DAYS` → defaults to `7`
- `RELEVANCE_THRESHOLD` → defaults to `6.0`
- `MAX_ARTICLES_PER_RUN` → defaults to `20`

---

## 5. Key URLs and Endpoints

| Resource | URL |
|----------|-----|
| Live site | https://gridthegrey.com |
| GitHub repo | https://github.com/bansac1981/sentinel-ai |
| Newsletter subscribe | https://preview.mailerlite.io/forms/2303110/186108792273896900/share |
| Mailerlite dashboard | https://dashboard.mailerlite.com |
| Podcast R2 feed | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/feed.xml |
| Podcast R2 base | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/ |
| Podcast W17 MP3 | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/grid-the-grey-briefing-2026-W17-onyx.mp3 |
| Spotify submission | Submitted — pending approval |

---

## 6. File Map (Complete)

```
sentinel-ai/
├── pipeline.py              # RSS fetch → Claude scoring → Hugo markdown drafts
│                            # Includes: age filter, catchy title gen, Unsplash images
├── weekly_briefing.py       # CISO audio briefing: Claude script + OpenAI TTS + R2 upload
├── podcast_feed.py          # iTunes-compatible RSS feed generator → R2
├── newsletter_digest.py     # Newsletter digest — generates HTML + sends via Mailerlite API
│                            # Usage: python newsletter_digest.py --send --days 4
│                            # Flags: --send, --dry-run, --days N, --output file, --subject "..."
├── backfill_tldr.py         # One-off: backfill TL;DR fields on existing articles
├── check_feeds.py           # Utility: validate RSS feed URLs before adding to pipeline
├── requirements.txt         # Python deps: feedparser, anthropic, openai, boto3, httpx etc.
├── seen_urls.json           # Dedup state (committed, maintained by pipeline)
├── .env                     # Local secrets — NEVER commit (gitignored)
├── .env.example             # Template for .env
├── welcome_email_template.html  # Mailerlite welcome email HTML (paste into automation editor)
├── briefings/
│   ├── episodes.json        # Podcast episode metadata + show config
│   ├── feed.xml             # Local copy of podcast RSS (also uploaded to R2)
│   ├── draft-2026-W16.md    # Generated briefing script — Week 16
│   └── draft-2026-W17.md    # Generated briefing script — Week 17
├── .github/workflows/
│   ├── deploy.yml           # Build + GitHub Pages deploy (triggered on push to main)
│   ├── pipeline.yml         # RSS pipeline — manual only (no cron)
│   ├── newsletter.yml       # Newsletter dispatch — Tue + Fri 9:30 AM IST (AUTOMATED)
│   ├── ciso-briefing.yml    # CISO audio briefing: generate + produce steps
│   ├── publish-draft.yml    # Manual: publish a specific draft by slug
│   └── draft-cleanup.yml    # Cleanup stale drafts
├── HANDOFF.md               # This file — complete project state for agent handoff
├── MAILERLITE_SETUP.md      # Mailerlite setup guide (10 steps, DNS, automation, API)
├── PROJECT_STATE.md         # Legacy — redirects to HANDOFF.md
└── hugo-site/
    ├── hugo.toml            # Site config — baseURL, params, menus, taxonomies
    │                        # newsletterURL = Mailerlite hosted form URL
    ├── content/
    │   ├── posts/           # Published articles (draft: false)
    │   ├── posts/drafts/    # Pending review (draft: true)
    │   ├── categories/      # Category _index.md files (6 categories)
    │   └── about.md
    ├── layouts/
    │   ├── index.html       # Homepage: hero + ticker + mobile podcast + article grid
    │   ├── _default/
    │   │   ├── single.html  # Article page: header → TL;DR → framework panel →
    │   │   │                #   image → body → subscribe form → footer
    │   │   └── list.html    # Category/section list
    │   └── partials/
    │       ├── header.html           # Nav bar — Subscribe button anchors to #gtg-newsletter
    │       ├── footer.html
    │       ├── sidebar.html          # Podcast player → Threat Radar → Trending →
    │       │                         # Framework Index → Categories → Newsletter form
    │       │                         # Newsletter widget has id="gtg-newsletter"
    │       ├── article-subscribe.html # Inline subscribe form at bottom of every article
    │       │                          # Uses hidden iframe — no new tab on submit
    │       ├── ticker.html
    │       ├── tldr.html
    │       ├── podcast-player.html
    │       ├── scripts.html
    │       ├── article-image.html
    │       └── framework-panel.html
    ├── static/
    │   └── css/sentinel.css  # All styles — dark theme #0a0a0f, red accent #ff3b3b
    └── data/
        ├── ticker.json        # 10 threat ticker items
        ├── threats.json       # Threat radar sidebar
        ├── frameworks.json    # Framework index widget
        └── stats.json         # Stats counter widget
```

---

## 7. GitHub Actions Workflows

### deploy.yml — Auto-deploy
- **Trigger:** Push to `main` (paths: `hugo-site/**`, `.github/workflows/deploy.yml`)
- **Jobs:**
  1. `auto-publish`: scans `drafts/*.md` for `draft: false` → moves to `posts/`, commits
  2. `build`: Hugo build with `--baseURL https://gridthegrey.com/`
  3. `deploy`: GitHub Pages deploy + Google Indexing API ping
- **CRITICAL:** Always hardcode `--baseURL "https://gridthegrey.com/"` — never use `configure-pages` output

### pipeline.yml — RSS Pipeline
- **Trigger:** Manual only (`workflow_dispatch`) — no cron
- **Inputs:** `limit`, `dry_run`, `feed` (single feed key or all)
- **Process:** Fetches feeds → age filter (7 days) → keyword pre-filter → Claude scoring → writes `drafts/*.md`
- **Key behavior:** Skips articles already in `seen_urls.json`; deduplicates by slug

### newsletter.yml — Automated Newsletter *(new)*
- **Trigger:** Schedule — Tuesday and Friday at 04:00 UTC (9:30 AM IST)
- **Also:** Manual via `workflow_dispatch` with `days`, `dry_run`, `subject` inputs
- **Process:** `newsletter_digest.py --send --days 4` → Mailerlite API creates + sends campaign
- **Artifact:** Digest HTML uploaded as GitHub Actions artifact (retained 14 days) for inspection
- **Required secrets:** `MAILERLITE_API_KEY`, `MAILERLITE_LIST_ID`

### ciso-briefing.yml — Audio Briefing (TWO-STEP)
- **Trigger:** Manual only
- **Step 1 (generate):** Claude reads recent posts → writes `briefings/draft-YYYY-WXX.md` → commits
- **Step 2 (produce):** OpenAI TTS → MP3 → R2 upload → updates `hugo.toml` + `episodes.json` → commits
- **IMPORTANT:** Review the draft script between step 1 and step 2
- **Fixed bug:** `input()` prompt auto-confirms when `sys.stdin.isatty()` is False (CI safe)

### publish-draft.yml — Manual publish
- **Trigger:** Manual
- **Input:** `slug` (leave blank to list all drafts)
- **Process:** Moves specific draft to `posts/`, sets `draft: false`

### draft-cleanup.yml
- **Trigger:** Manual

---

## 8. Newsletter System (Mailerlite)

Fully automated — no manual steps required after initial setup.

### Flow
```
New subscriber visits site → fills sidebar or article-bottom form
    → added to "Grid the Grey Subscribers" group in Mailerlite
    → welcome email fires automatically (Mailerlite automation)

Every Tuesday + Friday 9:30 AM IST:
    → newsletter.yml runs newsletter_digest.py --send --days 4
    → scans last 4 days of published articles
    → builds dark-theme HTML digest
    → creates + sends campaign via Mailerlite API
    → saves digest HTML as Actions artifact
```

### Subscriber forms (two locations)
1. **Sidebar** (`sidebar.html`) — dark-themed email input, id=`gtg-newsletter`
   - Uses Mailerlite embedded form JS (`mlb2-40602689`)
   - Shows "✓ You're in." on success
2. **Article bottom** (`article-subscribe.html`) — full-width branded block
   - Uses hidden iframe (`target="gtg-ml-sink"`) — no new tab, no CORS issues
   - Shows success message after 800ms delay

### Nav Subscribe button
- Header "Subscribe" button links to `#gtg-newsletter` (smooth scroll to sidebar form)
- No external redirect

### Welcome email
- Template: `welcome_email_template.html` in repo root
- Set up in Mailerlite → Automations → trigger: subscriber joins group
- Sends immediately on subscription (double opt-in is disabled)

### Manual send
```bash
python newsletter_digest.py --send --days 7
python newsletter_digest.py --send --days 2 --subject "Breaking: ..."
python newsletter_digest.py --send --dry-run   # test without sending
```

### Costs
- Free up to 1,000 subscribers (12,000 emails/month)
- ~$13/month at 1,001–2,500 subscribers

---

## 9. RSS Sources (26 Feeds)

### Original 9
| Key | Source |
|-----|--------|
| `thehackernews` | The Hacker News |
| `securityweek` | SecurityWeek |
| `darkreading` | Dark Reading |
| `crowdstrike` | CrowdStrike Blog |
| `sans_isc` | SANS Internet Storm Center |
| `hn_ai_security` | HN AI Security (filtered: AI security, LLM, prompt injection ≥50 pts) |
| `schneier` | Schneier on Security |
| `projectzero` | Google Project Zero |
| `krebsonsecurity` | Krebs on Security |

### Added 2026-04-23 (+17)
| Key | Source | Category |
|-----|--------|----------|
| `hn_openai` | OpenAI (via HN filter) | AI Vendor |
| `hn_anthropic` | Anthropic (via HN filter) | AI Vendor |
| `google_ai_blog` | Google DeepMind Blog | AI Vendor |
| `microsoft_ai` | Microsoft AI Blog | AI Vendor |
| `unit42` | Palo Alto Unit 42 | Security Vendor |
| `talos` | Cisco Talos | Security Vendor |
| `microsoft_security` | Microsoft Security Blog | Security Vendor |
| `sentinelone` | SentinelOne Blog | Security Vendor |
| `mandiant` | Mandiant Blog | Security Vendor |
| `qualys` | Qualys Blog | Security Vendor |
| `checkpoint` | Check Point Research | Security Vendor |
| `ncsc_uk` | NCSC UK | Government |
| `bleepingcomputer` | BleepingComputer | News |
| `simonwillison` | Simon Willison | Analysis |
| `huggingface` | Hugging Face Blog | AI/ML |
| `wired_security` | Wired Security | News |
| `arstechnica` | Ars Technica Security | News |

**Note:** OpenAI and Anthropic have no public RSS feeds — HN-filtered feeds are used.

---

## 10. Article Front Matter Schema

Every article generated by `pipeline.py` has this front matter:

```yaml
---
title: "Claude-Generated Punchy Headline"     # generated_title from Claude
source_title: "Original RSS Article Title"    # preserved for reference
date: "2026-04-23T10:00:00+00:00"
draft: true                                   # set to false to publish
slug: "article-slug"                          # derived from generated_title + date
source: "Feed Name"
source_url: "https://original-article-url"
relevance_score: 8.5                          # Claude score 0-10; threshold 6.0
threat_level: "HIGH"                          # CRITICAL / HIGH / MEDIUM / LOW
category: "LLM Security"
mitre_techniques: ["AML.T0051", "AML.T0054"]
owasp_categories: ["LLM01", "LLM06"]
summary: "One paragraph summary"
thumbnail: "https://images.unsplash.com/..."  # Unsplash (primary) or Pexels (fallback)

# ── TL;DR ──
tldr_what: "One punchy sentence — core event/finding"
tldr_who_at_risk: "Who is most directly exposed and why"
tldr_actions: ["Action 1", "Action 2", "Action 3"]
---
```

**Title generation:** Claude generates a `generated_title` (max 12 words, threat-first, no clickbait, no "How/Why/What/number" starts). This becomes the article `title` and the URL slug. The original RSS title is stored in `source_title`.

**Image sourcing:** Unsplash API (`urls.regular`) is primary. Pexels is fallback. OG image scraping is last resort. Owner can also update manually by editing the `thumbnail` field.

---

## 11. Podcast System

### Episodes
- **W16:** Week of April 14 — first episode, 5:25 min, onyx voice
- **W17:** Week of April 21 — second episode, ~3.6 min, onyx voice

### hugo.toml podcast params
```toml
enablePodcastPlayer = true
latestEpisodeUrl = "https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/grid-the-grey-briefing-2026-W17-onyx.mp3"
latestEpisodeTitle = "Week 17, 2026 — AI Security Briefing"
podcastFeedUrl = "https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/feed.xml"
```

**After each new episode:** Update both `latestEpisodeUrl` and `latestEpisodeTitle` in `hugo.toml`.

### Player placement
- **Desktop:** Top of sidebar, above Threat Radar
- **Mobile:** Between hero banner and article grid (CSS breakpoint: 1024px)

### Podcast artwork
**PENDING:** Spotify requires square JPEG 1400×1400 to 3000×3000px uploaded to R2 as `podcast-artwork.jpg`. The `episodes.json` `image_url` already points to the expected URL.

### Spotify
- Feed submitted — pending approval
- Once approved, new episodes appear automatically within ~1 hour of `produce` step

---

## 12. TL;DR System

Template: `hugo-site/layouts/partials/tldr.html`

Displays three bullets on every article page:
1. **What happened** — `tldr_what` field (falls back to `summary`)
2. **Who's at risk** — `tldr_who_at_risk` (hidden if absent)
3. **Act now** — `tldr_actions` list (hidden if absent)

`backfill_tldr.py` was run on all ~44 existing articles. Uses `claude-haiku-4-5-20251001` (~$0.002/article).

### Article page render order
`single.html`: header → TL;DR → framework panel (MITRE/OWASP) → hero image → article body → **subscribe form** → article footer (tags, share, prev/next)

---

## 13. Git Workflow (Critical)

GitHub Actions commits to `main` after every pipeline run, produce step, and newsletter send. This causes push rejections if local is behind.

```bash
# ALWAYS before starting local work:
git pull

# After making changes (Windows PowerShell — no && operator):
git add <specific files>
git commit -m "description"
git stash
git pull
git stash pop
git push
```

**Config already set:** `git config pull.rebase true`

**When branches diverge:**
```bash
git fetch origin
git merge -X ours origin/main
git push
```

**Windows lock file issues:**
```powershell
del .git\HEAD.lock
del .git\index.lock
```

**Sandbox restriction:** The Cowork AI sandbox CANNOT push to GitHub (403 proxy block). All `git push` commands must be run from the user's Windows terminal. The sandbox CAN read, write, and commit — only push is blocked.

---

## 14. Design System

| Element | Value |
|---------|-------|
| Background | `#0a0a0f` |
| Card background | `#141419` |
| Accent (red) | `#ff3b3b` |
| Text primary | `#f0f0ff` |
| Text body | `#c8c8d8` |
| Text muted | `#7a7a8c` |
| Border | `#252535` |
| Headlines font | Source Serif 4 (Georgia fallback) |
| Body font | DM Sans |
| Mono/technical | IBM Plex Mono |

Sidebar widgets (top to bottom): Podcast Player → Threat Radar → Trending Now → Framework Index → Categories → Newsletter Subscribe Form

Tags cloud widget was removed — grew too large, low value.

---

## 15. Content State (as of 2026-05-01)

- **Published articles:** ~44 (all with TL;DR fields backfilled)
- **Podcast episodes:** 2 (W16, W17)
- **Newsletter subscribers:** Growing (Mailerlite, double opt-in disabled)

---

## 16. Known Issues and Gotchas

### Hugo-specific
1. **relURL + leading slash:** `relURL "/"` silently breaks. Always use `relURL "posts/"` (no leading slash) or `.Site.Home.RelPermalink`
2. **theme line:** Must be absent from `hugo.toml` — not empty, absent. `theme = ""` causes build error in Hugo 0.140+
3. **baseURL:** Always hardcode `--baseURL "https://gridthegrey.com/"` in deploy.yml

### Pipeline-specific
4. **Deduplication:** Pipeline deduplicates by both URL and slug-on-disk
5. **Age filter:** Articles older than 7 days are dropped before Claude scoring (saves API cost). Configurable via `MAX_ARTICLE_AGE_DAYS` env var
6. **Generated titles:** Claude's `generated_title` becomes both the display title and the URL slug. If Claude returns an empty string, falls back to original RSS title

### Newsletter-specific
7. **Mailerlite embedded form:** Uses their JS (`mlb2-40602689`). Article-bottom form uses hidden iframe (`target="gtg-ml-sink"`) to avoid opening a new tab and CORS issues
8. **Double opt-in:** Disabled. Subscribers are confirmed immediately on form submit
9. **Newsletter lookback:** `--days 4` covers Tue→Fri and Fri→Tue cycles. Adjust if gaps appear

### Podcast-specific
10. **CI input() prompt:** `weekly_briefing.py --produce` auto-confirms when `sys.stdin.isatty()` is False
11. **latest_draft() sorting:** Sorts by filename, not mtime — GitHub Actions gives all files same mtime

### Git-specific
12. **Actions commit timing:** Always pull before pushing
13. **-X ours merge:** Keeps local version of conflicts — can overwrite remote-only changes
14. **PowerShell:** Does not support `&&`. Use separate lines or semicolons

---

## 17. Pending Work (Roadmap)

### Immediate (owner action required)
- [ ] Upload podcast artwork to R2 as `podcast-artwork.jpg` (1400×1400+ JPEG)
- [ ] Confirm Spotify approval and test episode playback
- [ ] Verify Mailerlite domain DNS (gridthegrey.com) shows Verified in Mailerlite dashboard

### Feature: Deep Security Agent (Phase 2 — approved concept)

**Option A — Synthesis Agent** (recommended first)
When 3+ sources cover the same event, Claude reads all articles and writes an original "Grid the Grey Analysis" post. Cost: ~$5-15/month. Effort: ~1 day.

**Option B — CVE Monitor**
Pulls new CVEs from NVD API (free), filters for AI/ML relevance, generates original analysis. Cost: ~$3-8/month. Effort: ~1-2 days.

### Ongoing
- [ ] Regular pipeline runs (manual via GitHub Actions UI)
- [ ] Weekly CISO briefing (manual: generate → review → produce)
- [ ] Update `ticker.json`, `threats.json`, `stats.json` data files periodically
- [ ] Update README.md (partially outdated — still references Beehiiv)

---

## 18. Common Commands Reference

```bash
# Test pipeline without API cost
python pipeline.py --dry-run

# Run pipeline, single feed
python pipeline.py --feed bleepingcomputer --dry-run

# Run pipeline, limit articles
python pipeline.py --limit 5

# Backfill TL;DR fields on existing articles
python backfill_tldr.py --dry-run
python backfill_tldr.py

# Validate RSS feed URLs
python check_feeds.py

# Newsletter — generate only (saves HTML locally)
python newsletter_digest.py --days 4 --output digest.html

# Newsletter — send via Mailerlite API
python newsletter_digest.py --days 4 --send

# Newsletter — dry run (no actual send)
python newsletter_digest.py --days 4 --send --dry-run

# Newsletter — breaking story send
python newsletter_digest.py --days 2 --send --subject "Breaking: Major LLM Vulnerability Disclosed"

# Podcast: generate script
python weekly_briefing.py --generate --days 7

# Podcast: produce audio (after reviewing script)
python weekly_briefing.py --produce --voice onyx

# Podcast: update feed.xml on R2
python podcast_feed.py --update

# Preview site locally (requires Hugo installed)
cd hugo-site && hugo server -D

# Git: safe push sequence (Windows PowerShell)
git add <files>
git commit -m "message"
git stash
git pull
git stash pop
git push

# Rollback to stable tag
git reset --hard v1.0-stable
git push --force origin main   # only if broken commits already pushed
```

---

## 19. Environment Variables (.env for local development)

```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
UNSPLASH_ACCESS_KEY=...          # from unsplash.com/developers
PEXELS_API_KEY=...               # from pexels.com/api
MAILERLITE_API_KEY=...           # from Mailerlite → Integrations → API
MAILERLITE_LIST_ID=...           # numeric group ID from Mailerlite → Subscribers → Groups
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=...
R2_PUBLIC_URL=https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev

# Optional overrides
CLAUDE_MODEL=claude-sonnet-4-6
MAX_ARTICLE_AGE_DAYS=7
RELEVANCE_THRESHOLD=6.0
MAX_ARTICLES_PER_RUN=20
```
