# Grid the Grey — Unsubscribe Worker

Cloudflare Worker that handles one-click newsletter unsubscribe.

## How it works

```
User clicks "Unsubscribe" in email
    │
    ▼
GET gridthegrey.com/api/unsubscribe?email=...&token=...
    │
    ├─ Verifies HMAC-SHA256 token (tamper-proof)
    ├─ Calls MailerLite API → marks subscriber as "unsubscribed"
    └─ Returns branded confirmation page
```

Also handles **RFC 8058 one-click unsubscribe** — the POST that Gmail/Outlook
send when a user clicks the inbox unsubscribe button.

## Setup

### Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- A Cloudflare account with `gridthegrey.com` on it (already the case)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)

### 1. Install Wrangler

```bash
npm install -g wrangler
wrangler login
```

### 2. Generate an HMAC secret

```bash
# Generate a secure random key (use the same value in GitHub Secrets)
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Save the output — you'll need it in two places.

### 3. Set worker secrets

```bash
cd unsubscribe-worker

# Paste the HMAC key from step 2
npx wrangler secret put UNSUBSCRIBE_SECRET

# Paste your MailerLite API key
npx wrangler secret put MAILERLITE_API_KEY
```

### 4. Add the same HMAC secret to GitHub

Go to: **github.com/bansac1981/sentinel-ai → Settings → Secrets → Actions**

Add: `UNSUBSCRIBE_SECRET` → paste the same key from step 2.

### 5. Deploy

```bash
npx wrangler deploy
```

### 6. Test

```bash
# Generate a test token (replace YOUR_SECRET with your HMAC key)
python3 -c "
import hmac, hashlib
secret = 'YOUR_SECRET'
email = 'test@example.com'
token = hmac.new(secret.encode(), email.encode(), hashlib.sha256).hexdigest()
print(f'https://gridthegrey.com/api/unsubscribe?email={email}&token={token}')
"
```

Open the printed URL in a browser — you should see the confirmation page.

## Cost

Cloudflare Workers free tier: **100,000 requests/day**. Unsubscribe clicks
will be a tiny fraction of this.

## Secrets summary

| Secret | Where | Purpose |
|--------|-------|---------|
| `UNSUBSCRIBE_SECRET` | Cloudflare Worker + GitHub Actions | HMAC signing key (must match) |
| `MAILERLITE_API_KEY` | Cloudflare Worker + GitHub Actions | MailerLite API access |
