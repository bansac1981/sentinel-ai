# Phase 5 — Beehiiv Newsletter Integration

This guide connects Grid the Grey to Beehiiv for email distribution and monetization.

---

## Step 1: Create a Beehiiv Account

1. Go to **https://www.beehiiv.com** and sign up for a free account
2. When prompted for your publication name, enter: **Grid the Grey**
3. Choose your subdomain — e.g., `sentinelai.beehiiv.com`
4. Select category: **Technology / Cybersecurity**
5. Free tier supports up to **2,500 subscribers** with unlimited sends

---

## Step 2: Brand Your Publication

In Beehiiv → **Settings → Publication**:

| Field | Value |
|---|---|
| Name | Grid the Grey |
| Tagline | AI Threat Intelligence — Mapped to MITRE ATLAS & OWASP LLM Top 10 |
| Primary colour | `#ff3b3b` |
| Background | `#0a0a0f` |
| Font (heading) | Georgia or Serif |
| Font (body) | System sans-serif |

Upload a logo: use the `⬡ SENTINELAI` wordmark or create one via Canva with the same dark/red palette.

---

## Step 3: Connect Subscribe Button to Your Beehiiv URL

Once your Beehiiv publication is live, get your subscribe URL (e.g., `https://sentinel-ai.beehiiv.com/subscribe`).

Update `hugo-site/hugo.toml`:

```toml
[params]
  newsletterURL = "https://sentinel-ai.beehiiv.com/subscribe"
```

This automatically updates:
- The **Subscribe** button in the header
- The **Subscribe Free →** button in the sidebar CTA
- The **Newsletter** link in the footer

Commit and push — the buttons will be live after the next deploy.

---

## Step 4: Weekly Newsletter Workflow

### Generating the Digest

After each week's articles have been published (either by the pipeline or manually), run:

```bash
python newsletter_digest.py --days 7 --output this_week.html
```

This generates a fully formatted HTML email with:
- The highest-scored article as the **lead story** (with thumbnail)
- Up to 7 secondary stories with summaries
- MITRE ATLAS and OWASP tags on every article
- Categories breakdown
- CTA back to the Grid the Grey site

**Options:**
```bash
python newsletter_digest.py --days 14           # fortnight digest
python newsletter_digest.py --days 7            # standard weekly
python newsletter_digest.py --output digest.html  # save to file
```

### Publishing to Beehiiv

1. In Beehiiv, click **New Post → New Email**
2. Set subject: `Grid the Grey Threat Briefing — Week of [DATE]`
3. Set preview text: `[N] AI security stories this week, mapped to MITRE ATLAS and OWASP LLM Top 10`
4. In the editor, click **+ Add Block → HTML**
5. Open `this_week.html` and paste the full contents into the HTML block
6. Click **Preview** to verify it renders correctly
7. Click **Send** or **Schedule** (recommended: Tuesday 9:30 AM IST)

---

## Step 5: Grow Your Subscriber Base

### Organic channels

- Share each week's issue on LinkedIn and Twitter/X with the `#AISecuity` and `#LLMSecurity` hashtags
- Post to relevant Reddit communities: r/netsec, r/MachineLearning, r/cybersecurity
- Link to the subscribe page from the Grid the Grey GitHub repo README

### Beehiiv Boosts (monetization)

Once you have 100+ subscribers, enable **Boosts** in Beehiiv:
- Other newsletters pay Beehiiv to be recommended to your subscribers
- You earn $1–3 per confirmed subscriber that comes from their recommendations
- Enable in: **Monetize → Boosts → Enable Boost Recommendations**

### Referral program

Beehiiv's built-in referral system lets subscribers earn rewards for referring others. Enable in: **Grow → Referral Program**.

---

## Step 6: RSS-to-Email (Optional Automation)

Beehiiv supports importing from RSS to create draft newsletters automatically:

1. Go to **Settings → Import**
2. Enter your RSS feed URL: `https://gridthegrey.com/index.xml`
3. Set frequency: **Weekly**
4. Enable **"Create as draft"** (recommended — review before sending)

> **Note:** RSS import creates a plain-text digest. The `newsletter_digest.py` script produces a richer, framework-tagged version. Use whichever fits your workflow.

---

## Step 7: GitHub Actions — Automated Digest (Advanced)

To automatically generate and email the digest after each pipeline run, add a step to `.github/workflows/pipeline.yml`:

```yaml
- name: Generate newsletter digest
  if: env.NEW_POSTS == 'true'
  run: |
    python newsletter_digest.py --days 7 --output digest.html
    echo "Digest generated: $(wc -l < digest.html) lines"
```

Then use **Beehiiv's API** (requires paid plan) or **Zapier/Make** to send the generated HTML automatically.

For the free tier, the manual copy-paste workflow (Step 4) takes under 5 minutes each week.

---

## Checklist

- [ ] Beehiiv account created at beehiiv.com
- [ ] Publication name: Grid the Grey
- [ ] Brand colours set (#ff3b3b accent, dark theme)
- [ ] `newsletterURL` updated in `hugo-site/hugo.toml`
- [ ] Committed and pushed — Subscribe buttons updated on live site
- [ ] Test newsletter generated: `python newsletter_digest.py --days 30 --output test.html`
- [ ] First issue published to Beehiiv
- [ ] Boosts enabled (once 100+ subscribers)
