# Grid the Grey — Mailerlite Newsletter Setup

This guide walks through the one-time setup to connect Grid the Grey to Mailerlite
for automated twice-weekly newsletters and welcome emails.

---

## Overview

The newsletter pipeline works as follows:

```
GitHub Actions (Tue + Fri 9:30 AM IST)
    │
    ▼
newsletter_digest.py --send --days 4
    │  reads hugo-site/content/posts/ for last 4 days
    │  builds dark-theme HTML digest
    ▼
Mailerlite API
    │  creates campaign
    │  sends to subscriber list
    ▼
Subscriber inboxes
```

New subscriber flow:
```
Subscriber fills Mailerlite hosted form
    │
    ▼
Added to "Grid the Grey Subscribers" list
    │
    ▼
Mailerlite automation triggers welcome email (immediately)
```

---

## Step 1 — Create Mailerlite Account

1. Go to **mailerlite.com** → Sign up free
2. Fill your profile completely when prompted:
   - Full name: your name
   - Company name: Grid the Grey
   - Website: https://gridthegrey.com
   - What do you send: "AI security news digest, twice weekly"
   - How do subscribers sign up: "Opt-in form on our website"
3. Verify your email address
4. **Wait for approval** — Mailerlite manually reviews new accounts.
   You'll receive an email within 24–48 hours. Answer any questions they
   ask promptly; approval is routine for legitimate newsletters.

---

## Step 2 — Verify Your Sending Domain

This is required for good email deliverability. Without it, emails may land in spam.

1. In Mailerlite: **Account Settings → Domains → Add domain**
2. Enter: `gridthegrey.com`
3. Mailerlite will show you DNS records to add (typically 2–3 records)
4. Add these in **Cloudflare DNS** (same place you manage gridthegrey.com):
   - Usually: one TXT record for SPF, one CNAME for DKIM
5. Click **Verify** in Mailerlite after adding the records
   (DNS propagation can take up to 30 minutes)
6. Set your sender email to: `analyst@gridthegrey.com`

---

## Step 3 — Create Your Subscriber List

1. Mailerlite → **Subscribers → Groups → Create group**
2. Name: `Grid the Grey Subscribers`
3. Note the **Group ID** — you'll need it as a GitHub Secret later.
   Find it in the URL when viewing the group:
   `https://dashboard.mailerlite.com/subscribers/groups/XXXXXXX`
   The number at the end is your Group ID.

---

## Step 4 — Create the Subscription Form

1. Mailerlite → **Forms → Create form → Hosted form (popup or landing page)**
2. Keep it simple: First name (optional) + Email (required)
3. Connect it to your `Grid the Grey Subscribers` group
4. Enable **Double opt-in** (recommended — keeps list clean, reduces spam complaints)
5. Publish the form
6. Copy the **hosted form URL** (looks like `https://landing.mailerlite.com/...`)
7. Share this URL — it needs to be added to hugo.toml and the site templates

---

## Step 5 — Set Up the Welcome Email Automation

1. Mailerlite → **Automations → Create automation**
2. Trigger: **When subscriber joins a group** → select `Grid the Grey Subscribers`
3. Add step: **Send email**
4. Create new email:
   - Subject: `Welcome to Grid the Grey — AI Security Intelligence`
   - Sender name: `Grid the Grey`
   - Sender email: `analyst@gridthegrey.com`
5. In the email editor, choose **HTML editor**
6. Open `welcome_email_template.html` from the repo
7. Copy everything between `<body>` and `</body>` tags
8. Paste into Mailerlite's HTML editor
9. Save and activate the automation

---

## Step 6 — Get Your API Key

1. Mailerlite → **Account Settings → API → Generate new token**
2. Name it: `Grid the Grey Pipeline`
3. Copy the token (shown only once)

---

## Step 7 — Add GitHub Secrets

Go to: **github.com/bansac1981/sentinel-ai → Settings → Secrets and variables → Actions**

Add two secrets:

| Secret Name | Value |
|---|---|
| `MAILERLITE_API_KEY` | Your API token from Step 6 |
| `MAILERLITE_LIST_ID` | Your Group ID from Step 3 |

---

## Step 8 — Update the Subscribe URL in the Site

Once you have the form URL from Step 4, update `hugo-site/hugo.toml`:

```toml
# Replace both occurrences of MAILERLITE_FORM_URL_PLACEHOLDER with your actual URL:
newsletterURL = "https://landing.mailerlite.com/your-form-url"
```

And in the menu section:
```toml
[[menu.main]]
  name = "Newsletter"
  url = "https://landing.mailerlite.com/your-form-url"
```

Then commit and push — the site will rebuild automatically.

---

## Step 9 — Import Existing Subscribers (if any)

If you had subscribers on Beehiiv:
1. Beehiiv → **Audience → Export → CSV**
2. Mailerlite → **Subscribers → Import → Upload CSV**
3. Map columns: email → Email, name → First name
4. Assign to `Grid the Grey Subscribers` group
5. Mailerlite will ask how you collected these — answer honestly

---

## Step 10 — Test End-to-End

**Test the welcome email:**
1. Subscribe using your own email via the hosted form
2. Check inbox — welcome email should arrive within a minute

**Test the newsletter:**
```bash
# Dry run — builds digest, skips actual send
python newsletter_digest.py --days 7 --send --dry-run

# Real test send (sends to your full list)
MAILERLITE_API_KEY=your_key MAILERLITE_LIST_ID=your_id \
  python newsletter_digest.py --days 7 --send
```

Or trigger manually from GitHub:
**Actions → Grid the Grey Newsletter Dispatch → Run workflow**
- Set `dry_run: true` to test without sending

---

## Newsletter Schedule

The newsletter sends automatically via GitHub Actions:
- **Tuesday at 9:30 AM IST** (covers Mon–Tue articles)
- **Friday at 9:30 AM IST** (covers Wed–Thu–Fri articles)

Both use `--days 4` lookback to avoid overlap.

To change the schedule, edit `.github/workflows/newsletter.yml`:
```yaml
schedule:
  - cron: "0 4 * * 2"   # Tuesday  (04:00 UTC = 9:30 AM IST)
  - cron: "0 4 * * 5"   # Friday   (04:00 UTC = 9:30 AM IST)
```

---

## Manual Newsletter Send

To send on demand (e.g., for a breaking story):

```bash
python newsletter_digest.py \
  --days 2 \
  --subject "[Grid the Grey] Breaking: Major LLM Vulnerability Disclosed" \
  --send
```

Or via GitHub Actions UI: **Actions → Newsletter Dispatch → Run workflow**

---

## Troubleshooting

**"MAILERLITE_API_KEY not set"**
→ Add the secret at: repo Settings → Secrets and variables → Actions

**"No published posts found"**
→ Try `--days 14` to look back further. Check that posts have `draft: false`.

**Campaign created but not sent**
→ Check that your account is fully approved and domain is verified in Mailerlite.

**Emails landing in spam**
→ Verify domain DNS records (Step 2). Check SPF and DKIM are active.

**Form URL not working**
→ Confirm the form is published (not just saved as draft) in Mailerlite.

---

## Cost Reference

| Subscribers | Monthly cost |
|---|---|
| 0 – 1,000 | Free |
| 1,001 – 2,500 | ~$13/month |
| 2,501 – 5,000 | ~$22/month |
| 5,001 – 10,000 | ~$32/month |

Set a reminder at 800 subscribers to upgrade before hitting the free tier ceiling.
