# Grid the Grey Workflow & Sync Guide

This document explains how to manage articles using different methods and keep everything in sync.

## Workflow Overview

Your article pipeline has three stages:

1. **Drafts** → Articles awaiting review (stored in `hugo-site/content/posts/drafts/`)
2. **Published** → Live articles (stored in `hugo-site/content/posts/`)  
3. **Archived** → Old drafts (deleted after 15 days by automated cleanup)

## Two Ways to Work

### Method 1: GitHub Web UI (Quick edits)
**Best for:** Quick publishing, small changes, mobile access

#### Steps:
1. Go to https://github.com/bansac1981/sentinel-ai/tree/main/hugo-site/content/posts/drafts
2. Click a draft file to view it
3. Click the **edit button** (pencil icon)
4. Change `draft: true` → `draft: false`
5. Click **Commit changes**
6. The publish workflow auto-triggers → article moves to `/posts/` and appears on site in ~2 minutes

#### What happens automatically:
- Draft file is moved from `/posts/drafts/` to `/posts/`
- `date:` field updates to publish time (ensures article shows on homepage)
- Draft is removed from drafts folder (no duplicates)
- Site rebuilds and deploys

### Method 2: PowerShell (Full control, batch operations)

**Best for:** Pipeline runs, batch publishing, complex edits

#### Draft Review Workflow:
```powershell
# 1. Run the pipeline (creates new drafts)
python pipeline.py --limit 10

# 2. Review drafts
notepad hugo-site/content/posts/drafts/2026-04-13-example-slug.md

# 3. When ready to publish
# Edit the file: draft: true → draft: false

# 4. Commit and push
git add hugo-site/content/posts/drafts/
git commit -m "review: ready to publish example-slug"
git push
# Workflow auto-triggers → article published in ~2 minutes
```

#### Manual Publishing via PowerShell:
If you prefer to move articles manually before pushing:
```powershell
# Move draft to published
$DRAFT = "hugo-site/content/posts/drafts/2026-04-13-example-slug.md"
$PUBLISHED = "hugo-site/content/posts/2026-04-13-example-slug.md"

git mv $DRAFT $PUBLISHED

# Update the date field to today
$TODAY = Get-Date -Format "yyyy-MM-ddTHH:mm:ss+00:00"
(Get-Content $PUBLISHED) -replace '^date:.*$', "date: `"$TODAY`"" | Set-Content $PUBLISHED

# Commit and push
git add $PUBLISHED
git commit -m "publish: example-slug"
git push
```

### Method 3: GitHub Actions Manual Dispatch (Override mode)

**Best for:** Advanced control, preview mode, testing

#### Steps:
1. Go to Actions → "Grid the Grey — Publish Draft"
2. Click **Run workflow**
3. Enter the slug (e.g., `openai-security-advisory`)
4. Optional: Check "Preview only" to see changes without committing
5. Click **Run workflow**

The workflow will:
- Find the exact draft matching that slug
- Run duplicate detection
- Show the changes that will be made
- Move the draft to published folder
- Update date and frontmatter
- Commit and push

---

## How to Keep Everything in Sync

### ✅ DO:
- **Use one method at a time** — don't mix web UI and PowerShell edits simultaneously
- **Always set `draft: false` before pushing** — the workflow watches for this flag
- **Pull before you push** — `git pull` before working locally to avoid conflicts
- **Check published list** — verify articles appeared on site within 2 minutes of commit

### ❌ DON'T:
- **Don't edit published articles in `/posts/`** — they're already live; edit in drafts instead
- **Don't commit directly to `/posts/`** — use the draft folder so the workflow can manage publishing
- **Don't mix web and PowerShell** — if editing in web UI, wait 2 minutes for workflow; don't immediately push from PowerShell

### ⚠️ If Conflicts Happen:

**Scenario: File changed in web UI, but you also edited locally**

```powershell
# Pull to sync with web UI changes
git pull origin main

# Check for merge conflicts
git status

# If there are conflicts, resolve them:
# (edit the file to keep changes you want)
git add hugo-site/content/posts/drafts/your-file.md
git commit -m "merge: resolved conflict"
git push
```

---

## Workflow Automation Details

### Publish Workflow (automatic)

**Trigger:** `push` event to `/posts/drafts/` folder

When you (or the web UI) commit changes to draft files:
1. Workflow detects any file with `draft: false`
2. Runs duplicate content check (blocks if >80% similar to existing articles)
3. Moves draft to `/posts/` folder
4. Updates `date:` to publish time
5. Commits and pushes
6. Deploy workflow triggers → site rebuilds in ~2 minutes

**Tip:** If duplicate check blocks an article, the workflow exits with an error. Fix the duplicate issue, set `draft: true`, then `draft: false` again to retry.

### Draft Cleanup (automatic)

**Trigger:** Daily at 6:00 AM IST (00:30 UTC)

- Scans `/posts/drafts/` for files older than 15 days
- Deletes old drafts (by date prefix in filename)
- Clears stale articles so you're not re-reviewing old content

---

## Monitoring & Troubleshooting

### Check if Article Published:

1. Go to **Actions** tab → "Grid the Grey — Publish Draft"
2. Click the most recent workflow run
3. Check logs:
   - **Green checkmark** = Successfully published
   - **Red X** = Failed (check error message)
   - **Yellow dot** = Still running (wait a moment)

### Common Issues:

**Issue: Article committed but not appearing on site**
- Check if `draft: false` was properly saved
- Confirm workflow run succeeded (Actions tab)
- Check browser cache: hard refresh (Ctrl+Shift+R)
- Wait 2-3 minutes for deploy to complete

**Issue: Duplicate detection blocked publishing**
- The article is >80% similar to existing content
- Edit the draft to make it more unique (change title, add new insights, remove redundant sections)
- Set `draft: true` then `draft: false` again to retry

**Issue: Article dated too old/new (doesn't show on homepage)**
- Articles are sorted by date (newest first)
- Homepage shows 12 most recent articles
- If `date:` is set incorrectly, re-publish it to update the date

---

## Best Practice Workflow

### Daily Routine:

1. **Morning:** Pipeline runs at 9:30 AM IST, creates drafts
2. **Review:** Open drafts folder in GitHub web UI or PowerShell
3. **Quick publish:** Use web UI to set `draft: false` on good articles
4. **Batch operations:** Use PowerShell if you want to review + edit multiple articles

### Weekly Routine:

1. Run `newsletter_digest.py` to generate weekly digest HTML
2. Paste into Beehiiv to send newsletter

---

## FAQ

**Q: Can I schedule an article to publish at a specific time?**
- Not yet. Articles publish immediately when `draft: false` is set. Future enhancement: add scheduled publishing.

**Q: What if I accidentally set `draft: false` on a bad article?**
- Set it back to `draft: true` and push. The workflow won't auto-publish it.
- Or delete the file manually in GitHub web UI.

**Q: Can multiple people edit drafts at once?**
- Yes, but pull/push carefully to avoid merge conflicts. Use `git pull` before each push.

**Q: Does the workflow work on feature branches?**
- No. Publish workflow only triggers on the `main` branch. All drafts should be on `main`.

**Q: How do I move an article from published back to drafts?**
- Not recommended (articles are live). But if needed:
  ```powershell
  git mv hugo-site/content/posts/YYYY-MM-DD-slug.md hugo-site/content/posts/drafts/YYYY-MM-DD-slug.md
  # Edit: draft: false → draft: true
  git add .
  git commit -m "unpublish: slug"
  git push
  ```
  The article will disappear from the site within 2 minutes.

**Q: Can I batch publish multiple drafts at once?**
- Via web UI: No, publish one at a time (takes ~2 minutes per article).
- Via PowerShell: Yes, set multiple files to `draft: false` and push once. Workflow publishes all of them.
