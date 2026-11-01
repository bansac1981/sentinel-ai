---
title: "ChatGPT HTML Preview XSS Enables Account Takeover"
date: 2026-11-01T11:56:49+00:00
draft: false
slug: "chatgpt-html-preview-xss-enables-account-takeover"

# ── Content metadata ──
summary: "Researchers at Parameter Labs discovered a multi-stage exploit chain against ChatGPT's HTML preview (Canvas/artifacts) feature that allowed untrusted sandboxed iframe code to escape containment, inject unsandboxed iframes, and achieve JavaScript execution on the ChatGPT origin. By abusing a MathLive postMessage handler that used innerHTML and exploiting YouTube's oEmbed endpoint to bypass CSP script restrictions, attackers could exfiltrate private user data or perform actions on behalf of any signed-in user who visited a malicious shared ChatGPT URL. OpenAI patched the vulnerability and awarded a $5,000 bug bounty, though the severity of the exploit chain arguably warranted a higher payout."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Oct/31/how-we-took-over-chatgpt-accounts"
source_title: "How We Took Over ChatGPT Accounts"
source_date: 2026-10-31T23:15:22+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1693278616332-66d36a40ffef?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw1fHxsYW5ndWFnZSUyMHRyYW5zbGF0aW9uJTIwYWJzdHJhY3R8ZW58MHwwfHx8MTc5MzUzNDIwOXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0077 - LLM Response Rendering", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0113 - Steal Web Session Cookie", "AML.T0114 - AI Service Web Interface"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "A chained XSS exploit in ChatGPT's HTML preview feature enabled full account takeover of signed-in users."
tldr_who_at_risk: "Any signed-in ChatGPT user who visited a maliciously crafted share URL was at risk of private data exfiltration and account compromise."
tldr_actions: ["Audit all postMessage handlers in AI web interfaces for unsafe innerHTML usage", "Restrict CSP allowlists to exclude general-purpose reflective endpoints like YouTube oEmbed", "Enforce strict sandbox attributes on all AI-generated content iframes and prevent cross-frame postMessage without origin validation"]

# ── Taxonomies ──
categories: ["LLM Security", "Research", "Industry News"]
tags: ["chatgpt", "openai", "xss", "iframe-sandbox-escape", "content-security-policy", "postmessage", "innerhtml", "mathlive", "oembed", "account-takeover", "data-exfiltration", "html-preview", "bug-bounty", "javascript-injection"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-11-01T11:56:49+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Oct/31/how-we-took-over-chatgpt-accounts"
pipeline_version: "2.1.0"
---

## Overview

Researchers at Parameter Labs disclosed a sophisticated, multi-stage exploit chain targeting ChatGPT's HTML preview feature — OpenAI's sandboxed iframe environment for rendering AI-generated interactive HTML applications (formerly called Canvas). The vulnerability allowed an attacker to craft a shareable ChatGPT URL that, when opened by any signed-in user, would silently exfiltrate their private data or take actions on their behalf. OpenAI has since patched the issue and paid a $5,000 bug bounty.

## Technical Analysis

The attack chain exploited several compounding weaknesses:

1. **Unsafe postMessage handler in MathLive**: OpenAI's graph support relies on the MathLive JavaScript library, which includes a virtual keyboard feature. The keyboard can be triggered from within a sandboxed iframe via `postMessage()` to the parent page. The parent-side message handler used `innerHTML` to insert content — a well-known XSS vector.

2. **Missing origin validation**: There was no mechanism to prevent arbitrary sandboxed frames, including HTML preview iframes, from sending the triggering postMessage. This meant untrusted AI-generated HTML could invoke the MathLive handler.

3. **Sandbox escape via injected iframe**: While `innerHTML` does not execute `<script>` tags directly, it can inject `<iframe>` elements. By injecting an iframe *without* sandbox restrictions, the attacker gained a less-restricted execution context on the ChatGPT origin.

4. **CSP bypass via YouTube oEmbed**: OpenAI's Content Security Policy blocked inline scripts and restricted external script sources to a small allowlist — which included YouTube. The YouTube oEmbed endpoint can be used to reflect attacker-controlled JavaScript in a format that browsers execute, effectively turning a trusted CSP allowlisted domain into a script gadget.

With full JavaScript execution on the ChatGPT origin achieved, exfiltrating private data was trivial: API calls to fetch conversation history, then data exfiltration via an `<img>` tag pointing to an attacker-controlled server.

```
Sandboxed iframe → postMessage(MathLive trigger) → innerHTML injection
→ unsandboxed iframe → YouTube oEmbed CSP bypass → JS execution
→ fetch(/api/conversations) → img src exfiltration
```

## Framework Mapping

- **AML.T0077 (LLM Response Rendering)**: The root cause lies in how AI-generated HTML output is rendered with insufficient isolation.
- **AML.T0067 (LLM Trusted Output Components Manipulation)**: The MathLive library — a trusted component — was weaponised as the pivot point for sandbox escape.
- **AML.T0057 (LLM Data Leakage)**: Private conversation data was exfiltrated as the final payload.
- **LLM02 (Insecure Output Handling)**: AI-generated HTML was rendered in a context where sandbox boundaries could be breached.
- **LLM06 (Sensitive Information Disclosure)**: Private user data was exposed to an unauthenticated third party.
- **LLM07 (Insecure Plugin Design)**: The MathLive integration lacked appropriate input validation on its message-handling interface.

## Impact Assessment

Any signed-in ChatGPT user who clicked a malicious share link was potentially exposed. The attack was entirely client-side and required no user interaction beyond visiting the URL. The scope included private conversation history and the ability to perform authenticated actions on behalf of victims — effectively full account compromise within the ChatGPT web interface.

## Mitigation & Recommendations

- **Validate postMessage origins strictly**: All `window.addEventListener('message', ...)` handlers must verify `event.origin` against an explicit allowlist before acting.
- **Avoid innerHTML for message-driven DOM updates**: Use `textContent` or structured DOM APIs; never deserialise postMessage payloads via innerHTML.
- **Tighten CSP allowlists**: General-purpose reflective or oEmbed endpoints should never appear on script-src allowlists. Use explicit script hashes or nonces instead.
- **Enforce sandbox attributes comprehensively**: AI-generated iframe content must carry `sandbox` attributes that explicitly deny script injection into parent contexts.
- **Re-evaluate third-party library integrations**: Audit all dependencies included in AI platform frontends for message-handling or DOM-mutation capabilities that could be triggered cross-frame.

## References

- [Simon Willison — How We Took Over ChatGPT Accounts](https://simonwillison.net/2026/Oct/31/how-we-took-over-chatgpt-accounts)
