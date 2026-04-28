# GRID THE GREY — AI Agent Handoff Document

**Last updated:** 2026-04-23  
**Project name:** Grid the Grey (working name: SENTINEL AI)  
**Owner:** Achin Bansal — analyst@gridthegrey.com  
**Repo:** https://github.com/bansac1981/sentinel-ai  
**Live site:** https://gridthegrey.com  
**Local path (Windows):** `C:\Users\admin\projects\Security News Website\AI Security News Website`  
**Stable tag:** `v1.0-stable` (git tag, pushed to GitHub)

---

## 1. Project Purpose

An automated AI security news aggregation website targeting CISO-level readers. Every article is scored by Claude for relevance, then mapped to MITRE ATLAS techniques and OWASP LLM Top 10 categories. The site also produces a weekly audio briefing (podcast) distributed via Spotify.

Key differentiator: framework mapping (MITRE ATLAS + OWASP LLM Top 10) applied to every article, giving CISOs structured intelligence rather than raw news.

---

## 2. Architecture Overview

```
26 RSS feeds (AI vendors, security vendors, agencies, news)
    │
    ▼
pipeline.py
    ├── Keyword pre-filter (no API cost)
    ├── Claude API: relevance score (0-10), category, MITRE/OWASP mapping, TL;DR
    └── Writes hugo-site/content/posts/drafts/*.md (draft: true)
    │
    ▼  (user reviews drafts, sets draft: false via GitHub Actions UI)
deploy.yml (GitHub Actions)
    ├── auto-publish job: moves draft: false files from drafts/ → posts/
    ├── Hugo build (v0.140.2 extended)
    └── GitHub Pages deploy → https://gridthegrey.com
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
| CI/CD | GitHub Actions | 6 workflows (see Section 7) |
| AI scoring | Anthropic Claude | `claude-sonnet-4-6` (configurable via `CLAUDE_MODEL` var) |
| AI backfill | Anthropic Claude | `claude-haiku-4-5-20251001` (backfill_tldr.py — cheap) |
| TTS | OpenAI | `tts-1-hd`, default voice: `onyx` |
| Podcast storage | Cloudflare R2 | S3-compatible, public dev URL |
| Newsletter | Beehiiv | Free tier, manual HTML paste workflow |
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
| `PEXELS_API_KEY` | pipeline.py (article images) | Free at pexels.com/api |

Optional GitHub Actions variable (not secret):
- `CLAUDE_MODEL` → defaults to `claude-sonnet-4-6`

---

## 5. Key URLs and Endpoints

| Resource | URL |
|----------|-----|
| Live site | https://gridthegrey.com |
| GitHub repo | https://github.com/bansac1981/sentinel-ai |
| Beehiiv newsletter | https://gridthegrey.beehiiv.com/subscribe |
| Podcast R2 feed | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/feed.xml |
| Podcast R2 base | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/ |
| Podcast W16 MP3 | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/grid-the-grey-briefing-2026-W16-onyx.mp3 |
| Podcast W17 MP3 | https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/grid-the-grey-briefing-2026-W17-onyx.mp3 |
| Spotify submission | Submitted — pending approval |

---

## 6. File Map (Complete)

```
sentinel-ai/
├── pipeline.py              # RSS fetch → Claude scoring → Hugo markdown drafts
├── weekly_briefing.py       # CISO audio briefing: Claude script + OpenAI TTS + R2 upload
├── podcast_feed.py          # iTunes-compatible RSS feed generator → R2
├── newsletter_digest.py     # Weekly HTML digest for Beehiiv (manual paste)
├── backfill_tldr.py         # One-off: backfill TL;DR fields on existing articles
├── check_feeds.py           # Utility: validate RSS feed URLs before adding to pipeline
├── requirements.txt         # Python deps: feedparser, anthropic, openai, boto3, etc.
├── seen_urls.json           # Dedup state (committed, maintained by pipeline)
├── .env                     # Local secrets — NEVER commit (gitignored)
├── .env.example             # Template for .env
├── briefings/
│   ├── episodes.json        # Podcast episode metadata + show config (including email)
│   ├── feed.xml             # Local copy of podcast RSS (also uploaded to R2)
│   ├── draft-2026-W16.md    # Generated briefing script — Week 16
│   └── draft-2026-W17.md    # Generated briefing script — Week 17
├── .github/workflows/
│   ├── deploy.yml           # Build + GitHub Pages deploy (triggered on push to main)
│   ├── pipeline.yml         # RSS pipeline — manual only (no cron)
│   ├── ciso-briefing.yml    # CISO audio briefing: generate + produce steps
│   ├── publish-draft.yml    # Manual: publish a specific draft by slug
│   ├── newsletter-digest.yml # Weekly HTML digest generator (Mondays)
│   └── draft-cleanup.yml    # Cleanup stale drafts
├── HANDOFF.md               # This file — complete project state for agent handoff
├── PROJECT_STATE.md         # Legacy quick-reference (superseded by HANDOFF.md)
├── README.md                # Public-facing documentation (partially outdated)
├── BEEHIIV_SETUP.md         # Beehiiv integration guide
├── SEO_CHECKLIST.md         # SEO tasks
└── hugo-site/
    ├── hugo.toml            # Site config — baseURL, params, menus, taxonomies
    ├── content/
    │   ├── posts/           # Published articles (draft: false)
    │   ├── posts/drafts/    # Pending review (draft: true) — 2 articles currently
    │   ├── categories/      # Category _index.md files (6 categories)
    │   └── about.md
    ├── layouts/
    │   ├── index.html       # Homepage: hero + ticker + mobile podcast + article grid
    │   ├── _default/
    │   │   ├── single.html  # Article page: header → TL;DR → framework panel → image → body
    │   │   └── list.html    # Category/section list
    │   └── partials/
    │       ├── header.html
    │       ├── footer.html
    │       ├── sidebar.html          # Podcast player (top) → Threat Radar → Categories (NO tags)
    │       ├── ticker.html           # Live threat ticker bar
    │       ├── tldr.html             # TL;DR box: What happened / Who's at risk / Act now
    │       ├── podcast-player.html   # HTML5 audio player widget (container-relative JS)
    │       ├── scripts.html          # All JS including podcast player logic
    │       ├── article-image.html    # 6 SVG patterns for articles without images
    │       └── framework-panel.html  # MITRE ATLAS + OWASP badges (shown ABOVE hero image)
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
- **Trigger:** Manual only (`workflow_dispatch`) — cron was intentionally removed
- **Inputs:** `limit`, `dry_run`, `feed` (single feed key or all)
- **Process:** Fetches feeds → keyword pre-filter → Claude scoring → writes `drafts/*.md`
- **Key behavior:** Skips articles already in `seen_urls.json`; deduplicates by slug

### ciso-briefing.yml — Audio Briefing (TWO-STEP)
- **Trigger:** Manual only
- **Step 1 (generate):** Claude reads recent posts → writes `briefings/draft-YYYY-WXX.md` → commits
- **Step 2 (produce):** OpenAI TTS → MP3 → R2 upload → updates `hugo.toml` + `episodes.json` → commits
- **IMPORTANT:** Review the draft script between step 1 and step 2
- **Fixed bug:** `input()` prompt removed for CI (auto-confirms when no TTY)

### publish-draft.yml — Manual publish
- **Trigger:** Manual
- **Input:** `slug` (leave blank to list all drafts)
- **Process:** Moves specific draft to `posts/`, sets `draft: false`

### newsletter-digest.yml
- **Trigger:** Mondays 8 AM IST + manual
- **Output:** Commits `digest/latest.html` to repo for manual paste into Beehiiv

### draft-cleanup.yml
- **Trigger:** Manual

---

## 8. RSS Sources (26 Feeds)

### Original 9
| Key | Source |
|-----|--------|
| `thehackernews` | The Hacker News |
| `securityweek` | SecurityWeek |
| `darkreading` | Dark Reading |
| `crowdstrike` | CrowdStrike Blog |
| `sans_isc` | SANS Internet Storm Center |
| `hn_ai_security` | HN AI Security (filtered: AI security, LLM vulnerability, prompt injection, ≥50 points) |
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

**Note:** OpenAI and Anthropic do not have public RSS feeds — HN-filtered feeds are used instead.

---

## 9. Article Front Matter Schema

Every article generated by `pipeline.py` has this front matter:

```yaml
---
title: "Article Title"
date: "2026-04-23T10:00:00+00:00"
draft: true                          # Set to false to publish
slug: "article-slug"
source: "Feed Name"
source_url: "https://original-article-url"
relevance_score: 8.5                 # Claude score 0-10; threshold is 6.0
threat_level: "HIGH"                 # CRITICAL / HIGH / MEDIUM / LOW
category: "LLM Security"
mitre_techniques: ["AML.T0051", "AML.T0054"]
owasp_categories: ["LLM01", "LLM06"]
summary: "One paragraph summary"

# ── TL;DR ──
tldr_what: "One punchy sentence — core event/finding"
tldr_who_at_risk: "Who is most directly exposed and why"
tldr_actions: ["Action 1", "Action 2", "Action 3"]

image: "https://images.pexels.com/..."  # Optional; Pexels or Unsplash URLs both work
---
```

**Image handling:** Images are added manually by the owner using the "thumbnail method" (copy image URL from Pexels or Unsplash, add to `image:` field). The pipeline uses the Pexels API to suggest images but the owner has final say.

---

## 10. Podcast System

### Episodes
- **W16:** Week of April 14 — first episode, 5:25 min (325s), onyx voice
- **W17:** Week of April 21 — second episode, ~3.6 min (431 words), onyx voice

### hugo.toml podcast params
```toml
enablePodcastPlayer = true
latestEpisodeUrl = "https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/grid-the-grey-briefing-2026-W17-onyx.mp3"
latestEpisodeTitle = "Week 17, 2026 — AI Security Briefing"
podcastFeedUrl = "https://pub-935e4acdc21d48bc8e73087b20f1dc3f.r2.dev/feed.xml"
```

### Player placement
- **Desktop:** Top of sidebar, above Threat Radar
- **Mobile:** Between hero banner and article grid (CSS breakpoint: 1024px)
- Two instances safe on same page — uses container-relative JS, no global IDs

### Podcast artwork
**PENDING:** Spotify requires a square JPEG 1400×1400 to 3000×3000px uploaded to R2 as `podcast-artwork.jpg`. The `episodes.json` `image_url` field already points to the expected URL. This has NOT been done yet.

### Spotify
- Feed submitted to Spotify for Podcasters — pending approval
- Once approved, new episodes appear automatically within ~1 hour of `produce` step

---

## 11. TL;DR System

### Template: `hugo-site/layouts/partials/tldr.html`
Displays three bullets on every article page:
1. **What happened** — uses `tldr_what` field (falls back to `summary`)
2. **Who's at risk** — uses `tldr_who_at_risk` (hidden if absent)
3. **Act now** — uses `tldr_actions` list (hidden if absent)

### Backfill
`backfill_tldr.py` was run on all ~40 existing articles to add TL;DR fields. Uses `claude-haiku-4-5-20251001` (~$0.002/article). Run with `--force` to regenerate all, or without args to only process missing fields.

### Article page layout order
`single.html` renders: header → TL;DR box → framework panel (MITRE/OWASP) → hero image → article body

---

## 12. Git Workflow (Critical)

GitHub Actions commits to `main` after every pipeline run and produce step. This causes push rejections if local is behind. The established workflow:

```bash
# ALWAYS before starting local work:
git pull            # configured as rebase by default

# After making changes:
git add <specific files>
git commit -m "description"
git stash           # if you have unstaged changes blocking pull
git pull
git stash pop
git push
```

**Config already set:** `git config pull.rebase true` (rebases instead of merge commits)

**When branches diverge (e.g., after merge chaos):**
```bash
git fetch origin
git merge -X ours origin/main   # keeps local version on conflicts
git push
```

**Known Windows issues:**
- `HEAD.lock` or `index.lock` files: `del .git\HEAD.lock` from Windows CMD
- CRLF warnings on `git stash` / `git add`: harmless, ignore them

**Sandbox restriction:** The Cowork/AI sandbox CANNOT push to GitHub (403 proxy block). All `git push` commands must be run from the user's Windows terminal.

---

## 13. Design System

| Element | Value |
|---------|-------|
| Background | `#0a0a0f` |
| Accent (red) | `#ff3b3b` |
| Text primary | `#e8e8e8` |
| Text secondary | `#888` |
| Border | `#1a1a2e` |
| Headlines font | Source Serif 4 |
| Body font | DM Sans |
| Mono/technical | IBM Plex Mono |
| Sidebar removed | Tags cloud (removed — too large, low value) |

---

## 14. Content State

- **Published articles:** ~44 (all with TL;DR fields backfilled)
- **In drafts:** 2 articles (held pending review)
  - `2026-04-14-fake-claude-website-distributes-plugx-rat.md`
  - `2026-04-18-mythos-and-cybersecurity.md`
- **Most recent:** April 20, 2026 (3 articles)

---

## 15. Known Issues and Gotchas

### Hugo-specific
1. **relURL + leading slash:** `relURL "/"` silently breaks. Always use `relURL "posts/"` (no leading slash) or `.Site.Home.RelPermalink`
2. **theme line:** Must be absent from `hugo.toml` — not empty, absent. `theme = ""` causes build error in Hugo 0.140+
3. **baseURL:** Always hardcode `--baseURL "https://gridthegrey.com/"` in deploy.yml. Never use `configure-pages` output

### Pipeline-specific
4. **Deduplication:** Pipeline deduplicates by both URL and slug-on-disk. Never creates `-1` duplicate variants
5. **Binary file matches in grep:** Some `.md` files have CRLF encoding that causes grep to report "binary file matches" — use Python to read them instead

### Podcast-specific
6. **CI input() prompt:** `weekly_briefing.py --produce` had an interactive `input()` that broke in GitHub Actions (EOFError). Fixed: auto-confirms when `sys.stdin.isatty()` is False
7. **update_hugo_params regex:** Uses `lambda m:` in `re.sub` to avoid Unicode escape errors with em-dashes in JSON strings
8. **latest_draft() sorting:** Sorts by filename (`p.name`), not `p.stat().st_mtime` — GitHub Actions checkout gives all files the same mtime

### Git-specific
9. **Actions commit timing:** GitHub Actions commits between local commits regularly. Always pull before pushing
10. **-X ours merge:** Used frequently to resolve diverged branches — keeps local version of conflicting files. Be aware this can overwrite remote-only changes (e.g., overwrote W17 URL in hugo.toml once)

---

## 16. Pending Work (Roadmap)

### Immediate (owner action required)
- [ ] Upload podcast artwork to R2 as `podcast-artwork.jpg` (1400×1400+ JPEG square)
- [ ] Confirm Spotify approval and test episode playback

### Feature: Deep Security Agent (Phase 2 — approved concept)
Two options discussed and approved in principle:

**Option A — Synthesis Agent** (recommended first)
When 3+ sources cover the same event, Claude reads all articles together and writes an original "Grid the Grey Analysis" post. Cost: ~$5-15/month extra. Effort: ~1 day to build clustering and synthesis logic in pipeline.py.

**Option B — CVE Monitor**
Pulls new CVEs from NVD API (free), filters for AI/ML relevance, generates original analysis with MITRE ATLAS mapping. Cost: ~$3-8/month. Effort: ~1-2 days.

### Ongoing
- [ ] Regular pipeline runs (currently manual — owner runs via GitHub Actions UI)
- [ ] Weekly CISO briefing (manual — generate → review → produce)
- [ ] Weekly newsletter digest (auto-commits Mondays, manual paste to Beehiiv)
- [ ] Update `README.md` to reflect current state (partially outdated)
- [ ] Update `ticker.json`, `threats.json`, `stats.json` data files periodically

---

## 17. Common Commands Reference

```bash
# Test pipeline without API cost
python pipeline.py --dry-run

# Run pipeline, single feed
python pipeline.py --feed bleepingcomputer --dry-run

# Run pipeline, limit articles
python pipeline.py --limit 5

# Backfill TL;DR fields on existing articles
python backfill_tldr.py --dry-run    # preview
python backfill_tldr.py              # apply

# Validate RSS feed URLs
python check_feeds.py

# Generate newsletter digest
python newsletter_digest.py --days 7 --output digest.html

# Podcast: generate script
python weekly_briefing.py --generate --days 7

# Podcast: produce audio (after reviewing script)
python weekly_briefing.py --produce --voice onyx

# Podcast: update feed.xml on R2
python podcast_feed.py --update

# Preview site locally (requires Hugo installed)
cd hugo-site && hugo server -D

# Git: safe push sequence
git add <files>
git commit -m "message"
git stash && git pull && git stash pop && git push

# Rollback to stable tag
git reset --hard v1.0-stable
git push --force origin main   # only if already pushed broken commits
```

---

## 18. Beehiiv Newsletter Workflow

1. Newsletter digest auto-commits to `digest/latest.html` every Monday at 8 AM IST
2. Owner opens the HTML file from GitHub
3. Beehiiv → New Post → New Email → HTML block → paste contents
4. Subject line: `Grid the Grey AI Threat Briefing — Week of [DATE]`
5. Send or schedule (recommended: Tuesday 9:30 AM IST)

Beehiiv URL: https://gridthegrey.beehiiv.com/subscribe  
(Note: README has old URL `sentinel-ai.beehiiv.com` — this is outdated)
