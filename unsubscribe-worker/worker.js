/**
 * Grid the Grey — Unsubscribe Worker
 * ===================================
 * Cloudflare Worker that handles newsletter unsubscribe requests.
 *
 * Flow:
 *   1. User clicks unsubscribe link in email → GET /api/unsubscribe?email=...&token=...
 *   2. Worker verifies HMAC-SHA256 token
 *   3. Worker calls MailerLite API to set subscriber status to "unsubscribed"
 *   4. Worker returns branded confirmation page
 *
 * Also handles RFC 8058 one-click unsubscribe (POST from email clients).
 *
 * Required secrets (set via `wrangler secret put`):
 *   UNSUBSCRIBE_SECRET  — same HMAC key used by newsletter_digest.py
 *   MAILERLITE_API_KEY  — MailerLite API token
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Only handle /api/unsubscribe
    if (url.pathname !== '/api/unsubscribe') {
      return new Response('Not found', { status: 404 });
    }

    // ── Extract parameters ──────────────────────────────────────────
    let email, token;

    if (request.method === 'POST') {
      // RFC 8058 one-click: params may be in body or query string
      const contentType = request.headers.get('content-type') || '';
      if (contentType.includes('application/x-www-form-urlencoded')) {
        const body = await request.text();
        const params = new URLSearchParams(body);
        email = params.get('email') || url.searchParams.get('email');
        token = params.get('token') || url.searchParams.get('token');
      } else {
        email = url.searchParams.get('email');
        token = url.searchParams.get('token');
      }
    } else if (request.method === 'GET') {
      email = url.searchParams.get('email');
      token = url.searchParams.get('token');
    } else {
      return new Response('Method not allowed', { status: 405 });
    }

    // ── Validate inputs ─────────────────────────────────────────────
    if (!email || !token) {
      return htmlResponse(errorPage('Missing parameters', 'The unsubscribe link appears to be incomplete.'), 400);
    }

    // ── Verify HMAC token ───────────────────────────────────────────
    const isValid = await verifyToken(email.toLowerCase().trim(), token, env.UNSUBSCRIBE_SECRET);
    if (!isValid) {
      return htmlResponse(errorPage('Invalid link', 'This unsubscribe link is invalid or has been tampered with.'), 403);
    }

    // ── Call MailerLite API to unsubscribe ───────────────────────────
    try {
      const result = await unsubscribeFromMailerlite(email.toLowerCase().trim(), env.MAILERLITE_API_KEY);
      if (result.ok) {
        return htmlResponse(successPage(email));
      } else {
        console.error(`MailerLite API error: ${result.status} ${result.body}`);
        return htmlResponse(errorPage(
          'Something went wrong',
          'We couldn\'t process your unsubscribe request right now. Please try again or reply to any newsletter email with "unsubscribe".'
        ), 502);
      }
    } catch (err) {
      console.error(`Unsubscribe error: ${err.message}`);
      return htmlResponse(errorPage(
        'Something went wrong',
        'We couldn\'t process your unsubscribe request right now. Please try again or reply to any newsletter email with "unsubscribe".'
      ), 500);
    }
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// HMAC verification
// ─────────────────────────────────────────────────────────────────────────────

async function verifyToken(email, token, secret) {
  if (!secret) return false;

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign'],
  );

  const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(email));
  const expectedHex = Array.from(new Uint8Array(signature))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  // Constant-time comparison
  if (token.length !== expectedHex.length) return false;
  let mismatch = 0;
  for (let i = 0; i < token.length; i++) {
    mismatch |= token.charCodeAt(i) ^ expectedHex.charCodeAt(i);
  }
  return mismatch === 0;
}

// ─────────────────────────────────────────────────────────────────────────────
// MailerLite API
// ─────────────────────────────────────────────────────────────────────────────

async function unsubscribeFromMailerlite(email, apiKey) {
  if (!apiKey) {
    return { ok: false, status: 0, body: 'MAILERLITE_API_KEY not configured' };
  }

  // MailerLite REST API — update subscriber status by email
  const resp = await fetch(
    `https://connect.mailerlite.com/api/subscribers/${encodeURIComponent(email)}`,
    {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ status: 'unsubscribed' }),
    },
  );

  const body = await resp.text();
  return { ok: resp.ok, status: resp.status, body };
}

// ─────────────────────────────────────────────────────────────────────────────
// HTML responses
// ─────────────────────────────────────────────────────────────────────────────

function htmlResponse(html, status = 200) {
  return new Response(html, {
    status,
    headers: {
      'Content-Type': 'text/html;charset=UTF-8',
      'Cache-Control': 'no-store',
    },
  });
}

function pageShell(title, body) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title} — Grid the Grey</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background:#0a0a0f; color:#c8c8d8;
    font-family:'DM Sans',system-ui,Arial,sans-serif;
    min-height:100vh; display:flex; align-items:center; justify-content:center;
    padding:24px;
  }
  .card {
    max-width:480px; width:100%;
    background:#141419; border:1px solid #252535; border-radius:12px;
    padding:40px 32px; text-align:center;
  }
  .logo { font-family:monospace; font-size:22px; font-weight:900; color:#f0f0ff;
    letter-spacing:0.05em; margin-bottom:28px; }
  .logo span { color:#ff3b3b; }
  h1 { font-family:Georgia,serif; font-size:24px; font-weight:700;
    color:#f0f0ff; margin-bottom:12px; line-height:1.3; }
  .message { font-size:15px; line-height:1.7; color:#7a7a8c; margin-bottom:24px; }
  .email-highlight { color:#c8c8d8; font-weight:600; }
  .btn {
    display:inline-block; padding:12px 28px;
    background:#ff3b3b; color:#fff; border-radius:4px;
    font-size:14px; font-weight:700; text-decoration:none;
    font-family:monospace; letter-spacing:0.05em;
  }
  .btn:hover { background:#e03535; }
  .footer { margin-top:28px; font-size:11px; color:#7a7a8c;
    border-top:1px solid #252535; padding-top:20px; }
  .footer a { color:#7a7a8c; }
  .icon { font-size:40px; margin-bottom:16px; }
</style>
</head>
<body>
<div class="card">
  <div class="logo">GRID THE <span>GREY</span></div>
  ${body}
  <div class="footer">
    <a href="https://gridthegrey.com">gridthegrey.com</a> · AI Security Intelligence
  </div>
</div>
</body>
</html>`;
}

function successPage(email) {
  const maskedEmail = maskEmail(email);
  return pageShell('Unsubscribed', `
  <div class="icon">✓</div>
  <h1>You've been unsubscribed</h1>
  <p class="message">
    <span class="email-highlight">${escapeHtml(maskedEmail)}</span> has been
    removed from the Grid the Grey newsletter. You won't receive any more emails from us.
  </p>
  <p class="message">Changed your mind?</p>
  <a href="https://gridthegrey.com" class="btn">VISIT GRID THE GREY →</a>
  `);
}

function errorPage(title, message) {
  return pageShell('Error', `
  <div class="icon">✕</div>
  <h1>${escapeHtml(title)}</h1>
  <p class="message">${escapeHtml(message)}</p>
  <a href="https://gridthegrey.com" class="btn">VISIT GRID THE GREY →</a>
  `);
}

// ─────────────────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────────────────

function maskEmail(email) {
  const [local, domain] = email.split('@');
  if (!domain) return '***';
  const masked = local.length > 2
    ? local[0] + '***' + local[local.length - 1]
    : '***';
  return `${masked}@${domain}`;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
