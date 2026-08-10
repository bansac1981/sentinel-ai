---
title: "Poison Claude Proxy Exposes All Customer Prompts to Operators"
date: "2026-08-10T05:28:53+00:00"
draft: false 
slug: "poison-claude-proxy-exposes-all-customer-prompts-to-operators"

# ── Content metadata ──
summary: "Researchers have uncovered underground services selling discounted access to Anthropic's Claude models by routing requests through fraudulent AWS Bedrock accounts, with operators gaining full visibility into every customer prompt. The services, including Poison Claude and Ecomagent.in, function as man-in-the-middle proxies that pass user queries to Anthropic while harvesting sensitive prompt data. With nearly 900 active users on Poison Claude alone, the privacy and data exfiltration risks are significant for developers and organisations unknowingly using these rogue API gateways."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/poison-claude-sells-discounted-claude.html"
source_title: "Poison Claude Sells Discounted Claude Access While Its Operator Sees Every Customer Prompt"
source_date: 2026-08-05T15:36:03+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1598520106830-8c45c2035460?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxyZXNlYXJjaCUyMHdoaXRlYm9hcmQlMjBicmFpbnN0b3JtfGVufDB8MHx8fDE3ODYzMzc0NDl8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - ML Model Inference API Access", "AML.T0012 - Valid Accounts", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0010 - ML Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM10 - Model Theft"]

# ── TL;DR ──
tldr_what: "Underground services sell cheap Claude API access by routing prompts through fraudulent AWS accounts, exposing all user data."
tldr_who_at_risk: "Developers and organisations using third-party Claude API wrappers are most at risk, as every prompt is visible to the rogue operator."
tldr_actions: ["Only use official Anthropic API endpoints and verify API base URLs in all development environments", "Audit environment variables in Claude Code and similar tools to ensure no rogue API gateway is configured", "Never submit sensitive, proprietary, or personal data through unverified third-party LLM proxy services"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News"]
tags: ["poison-claude", "anthropic", "claude", "rogue-api-proxy", "prompt-harvesting", "underground-services", "aws-bedrock", "api-key-abuse", "data-exfiltration", "cybercrime-forums", "ecomagent", "man-in-the-middle"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-10T04:50:49+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/poison-claude-sells-discounted-claude.html"
pipeline_version: "2.1.0"
---

## Overview

Cybersecurity researchers at Okta have exposed a network of underground services selling discounted access to Anthropic's Claude large language models — including Opus 4.8, Opus 4.7, and Sonnet 4.6 — by exploiting fraudulent cloud accounts and operating as silent man-in-the-middle proxies. The most prominent of these, **Poison Claude**, offers API access at 5–15% of official per-token pricing and has amassed approximately 872 active users. A second service, **Ecomagent.in**, claims roughly 970 users and also offers discounted OpenAI access. Both services harvest every prompt submitted by customers.

## Technical Analysis

Poison Claude generates cheap tokens by farming free bonus credits from cloud providers — specifically citing the $100 AWS Bedrock signup bonus — and pooling multiple fraudulent accounts to service customer requests. Customers receive an Anthropic-compatible API key and are instructed to override environment variables (e.g., in Claude Code) so that their tooling routes to the Poison Claude endpoint rather than Anthropic's official API.

The request flow is straightforward but insidious:
1. The customer submits a prompt to the Poison Claude API endpoint.
2. The service forwards the prompt to Anthropic via a legitimate (but fraudulent) account.
3. The response is returned to the customer — but the operator has full plaintext visibility at step 2.

A misconfigured status endpoint (`api.claudeopus[.]shop/api/status`) briefly exposed user counts before being remediated. The primary domain is shielded behind Cloudflare CDN; following responsible disclosure, Cloudflare added a phishing warning to the main domain but took no action on the API subdomain, which uses Cloudflare Turnstile for bot protection.

## Framework Mapping

- **AML.T0040 (ML Model Inference API Access):** The service monetises unauthorised access to Claude's inference API at scale.
- **AML.T0012 (Valid Accounts):** Fraudulent but technically valid AWS Bedrock accounts are used to launder access.
- **AML.T0057 (LLM Data Leakage):** Every customer prompt passes through the operator's infrastructure in plaintext.
- **AML.T0010 (ML Supply Chain Compromise):** Developers are redirected away from official API infrastructure through environment variable manipulation.
- **LLM06 (Sensitive Information Disclosure):** Operators have unrestricted access to all prompt content submitted by customers.
- **LLM05 (Supply Chain Vulnerabilities):** The rogue proxy inserts itself into the developer toolchain silently.

## Impact Assessment

The primary victims are developers and organisations who, attracted by cost savings or access restrictions, route production or development workloads through these services. Any proprietary code, credentials, business logic, or personal data included in prompts is exposed to the operator. There is also a secondary risk of model substitution — operators could silently swap Claude for a cheaper, less capable model without the customer's knowledge. The estimated ~1,850 combined users across both services represents a meaningful exposure surface, particularly given the developer-focused nature of the API access being sold.

## Mitigation & Recommendations

- **Verify API endpoints:** Always confirm that `ANTHROPIC_BASE_URL` and equivalent environment variables point to official Anthropic infrastructure before running any Claude-based tooling.
- **Avoid third-party LLM proxies:** Treat any service offering below-market AI API access as a potential data harvesting operation.
- **Secrets hygiene:** Never include API keys, credentials, or PII in prompts sent through unverified services.
- **Monitor for rogue account usage:** Cloud teams should audit AWS Bedrock account creation and bonus credit redemption patterns for signs of fraudulent pooling.
- **Cloudflare reporting:** If you identify rogue Cloudflare-fronted services, escalate via Cloudflare's abuse channels and document API subdomain separation as a gap in current takedown processes.

## References

- [Poison Claude Sells Discounted Claude Access While Its Operator Sees Every Customer Prompt — The Hacker News](https://thehackernews.com/2026/08/poison-claude-sells-discounted-claude.html)
