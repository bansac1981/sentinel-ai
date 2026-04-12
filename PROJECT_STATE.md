# GRID THE GREY — Project State Reference

**Last updated:** 2026-04-12  
**Project:** Grid the Grey  
**Owner:** Achin Bansal — bansalachin@gmail.com  
**Repo:** https://github.com/bansac1981/sentinel-ai  
**Live site:** https://gridthegrey.com/

---

## Quick Reference

| Item | Value |
|------|-------|
| **Hugo base URL** | `https://gridthegrey.com/` |
| **Local path** | `C:\Users\admin\projects\Security News Website\AI Security News Website` |
| **Newsletter** | https://sentinel-ai.beehiiv.com/subscribe |
| **Python version** | 3.12 |
| **Claude model** | claude-sonnet-4-6 |
| **Relevance threshold** | 6.0 |
| **Max articles/run** | 20 |
| **Pipeline cron** | `0 4 * * *` UTC (9:30 AM IST) |
| **Status** | Phase 6 Complete — Mobile workflows + design finalized |

---

## Architecture (1-minute overview)

```
Hugo static site (dark editorial, custom layouts)
  ↓ (daily 9:30 AM IST)
Python pipeline (9 RSS feeds → Claude scoring → Hugo markdown drafts)
  ↓ (on push to main)
GitHub Actions (build + deploy to GitHub Pages)
  ↓
Live site + Beehiiv weekly newsletter
```

---

## Key Config Values

**hugo.toml:**
```toml
baseURL = "https://gridthegrey.com/"
newsletterURL = "https://sentinel-ai.beehiiv.com/subscribe"
```

**deploy.yml:**
```bash
# CRITICAL: Hardcode baseURL (configure-pages returns wrong base)
hugo --baseURL "https://gridthegrey.com/" -d public
```

**pipeline.yml:**
```yaml
# Cron: 9:30 AM IST
schedule:
  - cron: '0 4 * * *'
```

**GitHub secrets:**
- `ANTHROPIC_API_KEY` — Required for pipeline runs

---

## File Map (Quick Lookup)

| Path | Purpose | Status | Notes |
|------|---------|--------|-------|
| `pipeline.py` | RSS fetch → Claude score → Hugo markdown | ✅ Stable | 9 feeds, threshold 6.0, dedup by slug+URL |
| `newsletter_digest.py` | Weekly HTML digest for Beehiiv | ✅ Stable | Generates `.html` for manual paste |
| `.github/workflows/deploy.yml` | Hugo build + GitHub Pages deploy | ✅ Stable | Hardcoded baseURL (do NOT use configure-pages) |
| `.github/workflows/pipeline.yml` | Daily cron + manual dispatch | ✅ Stable | Runs at 9:30 AM IST, mobile-friendly |
| `.github/workflows/publish-draft.yml` | Manual publish draft posts | ✅ Stable | Mobile-friendly workflow dispatch |
| `hugo.toml` | Site config, menus, taxonomies | ✅ Stable | No `theme = ""` line |
| `hugo-site/layouts/index.html` | Homepage (featured + grid) | 🔄 Iterating | Design tweaks ongoing |
| `hugo-site/layouts/_default/single.html` | Article page template | ✅ Stable | Minimal future changes |
| `hugo-site/static/css/sentinel.css` | All styles (dark theme #0a0a0f) | ✅ Stable | 6 article SVG patterns, h1-sized tagline |
| `hugo-site/layouts/partials/article-image.html` | 6 distinct SVG article visuals | ✅ Stable | Terminal, Heatmap, Blueprint, Interference, Breach, Topology |
| `hugo-site/layouts/partials/` | Header, footer, sidebar, ticker, etc. | 🔄 Iterating | Minor alignment/spacing changes |
| `content/posts/` | Articles (draft:true by default) | ✅ Dynamic | Pipeline auto-generates |
| `content/categories/` | Category _index.md files | ✅ Stable | 6 categories configured |
| `hugo-site/data/` | ticker.json, threats.json, frameworks.json | ✅ Stable | Manual updates only |
| `seen_urls.json` | Deduplication state | ✅ Dynamic | Auto-updated by pipeline |
| `requirements.txt` | Python dependencies | ✅ Stable | feedparser, anthropic, httpx, etc. |
| `.env` | ANTHROPIC_API_KEY (gitignored) | ✅ Stable | Never committed |
| `README.md` | Project documentation | 🔄 IN PROGRESS | Phase 6 current focus |

---

## RSS Sources (9 Feeds)

| # | Source | URL |
|---|--------|-----|
| 1 | The Hacker News | https://feeds.feedburner.com/TheHackersNews |
| 2 | SecurityWeek | https://www.securityweek.com/feed/ |
| 3 | Dark Reading | https://www.darkreading.com/rss.xml |
| 4 | CrowdStrike Blog | https://www.crowdstrike.com/en-us/blog/feed |
| 5 | SANS Internet Storm Center | https://isc.sans.edu/rssfeed_full.xml |
| 6 | HN AI Security | https://hnrss.org/newest?q=AI+security+OR+LLM+vulnerability+OR+prompt+injection&points=50 |
| 7 | Schneier on Security | https://www.schneier.com/feed/ |
| 8 | Google Project Zero | https://googleprojectzero.blogspot.com/feeds/posts/default |
| 9 | Krebs on Security | https://krebsonsecurity.com/feed/ |

---

## Critical Bugs (NEVER REPEAT)

### 1. Hugo relURL + Leading Slash
- **Problem:** `relURL "/"` silently strips `/sentinel-ai/` prefix
- **Solution:** Always use `relURL "posts/"` (no leading slash) or `.Site.Home.RelPermalink`
- **JSON data:** Use `strings.TrimPrefix "/" | relURL` for `.url` values

### 2. deploy.yml baseURL
- **Problem:** `configure-pages@v5` returns wrong base URL (missing `/sentinel-ai/`)
- **Solution:** Hardcode in deploy.yml: `hugo --baseURL "https://gridthegrey.com/" -d public`
- **Do NOT:** Rely on configure-pages output

### 3. Hugo theme = ""
- **Problem:** Line `theme = "sentinel"` causes error in Hugo 0.160+
- **Solution:** Delete the line entirely (must be absent, not empty)

### 4. .Site.Data deprecated in Hugo 0.160.0
- **Problem:** `{{ .Site.Data.ticker }}` throws error
- **Solution:** Use `hugo.Data.ticker` everywhere

### 5. $index in range
- **Problem:** `{{ range .Posts }}` can't access position
- **Solution:** Explicitly declare: `{{ range $index, $post := first 5 .Posts }}`

### 6. Git index.lock / HEAD.lock
- **Problem:** Cowork sandbox can leave orphaned locks
- **Solution:** User must delete from Windows terminal: `del .git\HEAD.lock` or `del .git\index.lock`

### 7. Git push from Cowork
- **Problem:** Cowork sandbox (403 proxy) blocks git push
- **Solution:** All git pushes MUST run from user's Windows terminal, not Cowork

### 8. CRLF warnings
- **Problem:** Line ending conflicts between Windows and CI
- **Solution:** `.gitattributes` in repo root forces LF: `* text=auto eol=lf`

### 9. Duplicate articles (-1 files)
- **Problem:** Same article fetched via different URL variant, pipeline created `-1` duplicate file
- **Solution:** Pipeline now deduplicates by both URL *and* slug on disk before Claude API call. Never creates `-1` variants; skips silently if slug exists
- **Fixed:** 2026-04-12 — article-image post bug resolved

---

## Phase Status

| Phase | Task | Status |
|-------|------|--------|
| 1 | Hugo site + full CSS theme + all templates | ✅ Complete |
| 2 | Python pipeline with Claude API integration | ✅ Complete |
| 3 | GitHub Actions (deploy + pipeline workflows) | ✅ Complete |
| 4 | About page, category _index.md, stats.json | ✅ Complete |
| 5 | newsletter_digest.py, Beehiiv setup | ✅ Complete |
| 6 | Mobile workflows + final design polish | ✅ Complete |

---

## Common Workflows

### Test pipeline locally (no API cost)
```bash
python pipeline.py --dry-run
```

### Run pipeline, limit to 5 articles
```bash
python pipeline.py --limit 5
```

### Review drafts
```bash
# Open hugo-site/content/posts/*.md
# Change draft: true → draft: false to publish
```

### Generate newsletter digest
```bash
python newsletter_digest.py --days 7 --output this_week.html
# Then paste this_week.html into Beehiiv → New Post → HTML block
```

### Deploy to GitHub Pages
```bash
git add .
git commit -m "your message"
git push origin main
# Auto-triggers deploy.yml
```

### Mobile App Workflows (GitHub Mobile)

**Run the Daily Pipeline:**
1. Actions tab → `.github/workflows/pipeline.yml`
2. Tap **"Run workflow"** (top-right)
3. Leave defaults or pick a single feed
4. Tap **Run** — fetches new articles in ~5 minutes

**List all draft posts:**
1. Actions tab → "Grid the Grey — Publish Draft"
2. Tap **"Run workflow"** → leave slug blank → tap **Run**
3. Log shows all available drafts with slug, title, score, threat level

**Publish a specific draft:**
1. Run "Publish Draft" workflow (see above) to get the slug
2. Run again → paste slug into input → tap **Run**
3. Site redeploys automatically — live in ~2 minutes

**Preview before publishing:**
1. Tick the **"preview"** checkbox before running the workflow
2. Shows what would change without committing

---

## Future: Custom Domain Migration

When moving to custom `.ai` domain:
1. Update `baseURL` in `hugo.toml`
2. Update `--baseURL` in `deploy.yml`
3. Update Beehiiv → Settings → Website URL
4. No other changes needed

---

## Suggested Cowork Task Split

Use this to organize future Cowork work by domain (reduces token consumption):

| Task Name | Focus | Context | Skip |
|-----------|-------|---------|------|
| `Phase6-README` | Documentation | README.md, project overview | Code files |
| `Hugo-Design-Fixes` | Templates + CSS | `layouts/`, `static/css/` | Python, GitHub Actions |
| `Pipeline-Refinement` | Python scoring | `pipeline.py`, sample RSS | Hugo, workflows |
| `GitHub-Actions` | Workflow fixes | `deploy.yml`, `pipeline.yml` | Code, templates |
| `Newsletter-Digest` | Email generation | `newsletter_digest.py`, template | Everything else |

---

## Questions or Updates?

When referencing this doc in Cowork, link it directly:
```
Refer to PROJECT_STATE.md for:
- Quick reference table (config, URLs, status)
- File map (which files to touch/skip)
- Critical bugs to never repeat
- Suggested task split for token reduction
```

For updates, edit the source (GitHub repo or Drive) and notify Cowork tasks to refresh.
