---
title: "Infostealer Logs Expose AI Session Tokens That Bypass MFA"
date: 2026-09-14T05:09:13+00:00
draft: true
slug: "infostealer-logs-expose-ai-session-tokens-that-bypass-mfa"

# ── Content metadata ──
summary: "Cybercriminals are harvesting JWT session tokens and API keys from infostealer logs to replay authentication against major AI platforms including OpenAI, Anthropic, and Google, effectively bypassing MFA entirely. Analysis of a 7 GB stealer dump revealed 1,843 unexpired tokens targeting AI services on the day of release, with 17.7% of all JWTs containing plaintext PII usable for follow-on social engineering. This attack pattern is particularly dangerous for AI platforms because stolen tokens grant full account access without triggering standard credential-based security controls."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/infostealer-logs-expose-replayable-ai.html"
source_title: "Infostealer Logs Expose Replayable AI Tokens That Can Bypass MFA"
source_date: 2026-09-09T14:23:55+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1620880762258-273a49958090?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8Y29udGFtaW5hdGlvbiUyMGhhem1hdCUyMHdhcm5pbmclMjBhYnN0cmFjdHxlbnwwfDB8fHwxNzg5MzYyNTUzfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0113 - Steal Web Session Cookie", "AML.T0114 - AI Service Web Interface", "AML.T0040 - AI Model Inference API Access", "AML.T0083 - Credentials from AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Infostealer logs contain replayable AI platform JWT tokens that bypass MFA on major LLM services."
tldr_who_at_risk: "Users of OpenAI, Anthropic, Google, Cursor, and other AI services whose devices were compromised by infostealers are directly exposed via replayable session tokens."
tldr_actions: ["Rotate all AI platform API keys and session tokens immediately if device compromise is suspected", "Enable IP allowlisting on AI service accounts and developer API portals where supported", "Deploy endpoint detection tools to identify infostealer infections before credential exfiltration occurs"]

# ── Taxonomies ──
categories: ["LLM Security", "Industry News"]
tags: ["infostealer", "session-token-hijacking", "jwt-replay", "mfa-bypass", "lumma-stealer", "vidar", "openai", "anthropic", "google", "credential-theft", "api-key-theft", "stealer-logs", "telegram", "okta"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-14T05:09:13+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/infostealer-logs-expose-replayable-ai.html"
pipeline_version: "2.1.0"
---

## Overview

A 7 GB infostealer dump released on Telegram in August 2026 has been found to contain thousands of unexpired authentication tokens granting access to major AI platforms, including OpenAI, Anthropic, Google, Amazon, Cursor, Character.ai, and Poe.com. Analysis by Okta's threat intelligence team identified 1,843 unexpired JSON Web Tokens (JWTs) and JSON Web Encryption (JWE) structures on the day of the dump's release — all of which could be replayed to access AI accounts without providing credentials or satisfying MFA challenges.

This represents a meaningful escalation in the abuse of infostealer infrastructure, extending well beyond traditional banking and email account compromise into the AI tooling ecosystem.

## Technical Analysis

Infostealers such as Lumma Stealer and Vidar are sold as off-the-shelf malware-as-a-service offerings. Once deployed on a victim machine, they harvest stored credentials, browser session cookies, API keys, and authentication tokens. This data is packaged into "stealer logs" and sold on underground forums and Telegram channels.

The critical risk identified in this dataset relates to JWT and JWE token replay. JWTs are cryptographically signed tokens that encode a user's authenticated session state. When a service receives a valid, unexpired JWT, it grants access without requiring re-authentication — meaning username, password, and MFA are all bypassed entirely.

Of the 44,791 unique JWTs in the dump, 555 were linked to AI service authentication. An additional 2,937 JWE structures — encrypted JWTs primarily associated with OpenAI's use of NextAuth.js — were also identified. While JWEs cannot be decrypted without the server-side key, they remain fully replayable: the server decrypts and validates them, granting access if the token is unexpired.

A further concern is that 17.7% of all JWTs in the dataset contained plaintext PII (names, phone numbers, email addresses), which does not expire and enables targeted phishing or social engineering even after session tokens have been rotated.

## Framework Mapping

- **AML.T0012 (Valid Accounts)**: Threat actors use stolen tokens to operate as legitimate authenticated users within AI platforms.
- **AML.T0113 (Steal Web Session Cookie)**: JWT and JWE tokens function analogously to session cookies and are harvested by the same infostealer mechanisms.
- **AML.T0114 (AI Service Web Interface)**: Replayed tokens provide direct access to AI service web interfaces and APIs.
- **AML.T0040 (AI Model Inference API Access)**: API keys harvested alongside session tokens enable programmatic model access.
- **LLM06 (Sensitive Information Disclosure)**: Plaintext PII embedded in JWTs constitutes a direct disclosure risk.

## Impact Assessment

The affected platforms span the major commercial AI ecosystem. Developers using Cursor or API keys for OpenAI and Anthropic face risks of intellectual property exposure, prompt history exfiltration, and unauthorised model usage costs. Enterprise users of AI tooling integrated into productivity platforms (Notion, Gamma) face broader data access risks. The 162-country spread of the compromised machines indicates this is not a targeted campaign but a broad opportunistic harvest.

## Mitigation & Recommendations

1. **Rotate credentials proactively**: Any organisation with employees using AI tools should treat infostealer incidents as requiring immediate token and API key rotation across all AI platforms.
2. **Enable IP allowlisting**: Where supported, restrict AI platform access to known corporate IP ranges to neutralise replay attacks from foreign infrastructure.
3. **Adopt Device Bound Session Credentials (DBSC)**: Google's DBSC implementation in Chrome cryptographically binds session tokens to a device, preventing off-device replay.
4. **Monitor for anomalous AI API usage**: Unusual query volumes, off-hours access, or unexpected geographic origins should trigger session invalidation.
5. **Deploy EDR to detect infostealer activity**: Early detection of Lumma Stealer or Vidar infections limits the exfiltration window.

## References

- [The Hacker News – Infostealer Logs Expose Replayable AI Tokens That Can Bypass MFA](https://thehackernews.com/2026/09/infostealer-logs-expose-replayable-ai.html)
