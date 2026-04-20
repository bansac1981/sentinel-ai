---
title: "Vercel Breach Tied to Context AI Hack Exposes Limited Customer Credentials"
date: "2026-04-20T18:32:20+00:00"
draft: false
slug: "vercel-breach-tied-to-context-ai-hack-exposes-limited-customer-credentials"

# ── Content metadata ──
summary: "Vercel suffered a breach originating from a compromised third-party AI tool, Context.ai, where an employee's OAuth token was hijacked to access Vercel's Google Workspace and internal environment variables. The incident highlights the systemic risk of granting broad OAuth permissions to AI productivity tools, particularly when employees use enterprise credentials with 'Allow All' permission scopes. ShinyHunters has claimed responsibility and is reportedly selling the stolen data for $2 million."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html"
source_date: 2026-04-20T03:35:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/17155842/pexels-photo-17155842.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 7.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Compromised Context.ai OAuth token gave attackers access to Vercel's Google Workspace and environment credentials."
tldr_who_at_risk: "Organizations whose employees use AI productivity tools with enterprise accounts and broad OAuth scopes are directly exposed to lateral-movement attacks via third-party AI service compromises."
tldr_actions: ["Audit and revoke 'Allow All' OAuth grants from third-party AI tools across all enterprise accounts immediately", "Rotate all non-sensitive environment variables in Vercel and mark secrets as 'sensitive' to enforce encryption", "Implement strict OAuth scope policies requiring least-privilege permissions for any AI SaaS integrations"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["vercel", "context-ai", "oauth-token-hijack", "supply-chain-attack", "google-workspace", "credential-exposure", "shinyhunters", "environment-variables", "third-party-ai-tool", "data-breach"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-20T18:09:35+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html"
pipeline_version: "1.0.0"
---

## Overview

Vercel, the widely-used web infrastructure and deployment platform, has disclosed a security breach traceable to the compromise of Context.ai — a third-party AI productivity tool used by at least one Vercel employee. The attacker leveraged a stolen OAuth token from Context.ai's March 2026 AWS environment breach to pivot into Vercel's Google Workspace, subsequently gaining access to internal Vercel systems and unencrypted environment variables. The incident is a textbook example of AI supply chain risk materialising at enterprise scale, and is notable for the speed and precision attributed to the threat actor — described by Vercel as 'sophisticated' based on their operational velocity and knowledge of internal systems.

ShinyHunters, a prolific cybercriminal persona associated with high-profile data extortion, has claimed responsibility and is reportedly offering stolen data for $2 million.

## Technical Analysis

The attack chain followed a clear multi-stage progression:

1. **Context.ai AWS Compromise (March 2026):** Attackers gained unauthorized access to Context.ai's AWS environment, harvesting OAuth tokens belonging to consumer users of the service.
2. **OAuth Token Abuse:** A Vercel employee had signed up for Context.ai's AI Office Suite using their Vercel enterprise Google account and granted 'Allow All' OAuth permissions — a broad scope that enabled the attacker to impersonate the employee's Google identity.
3. **Google Workspace Takeover:** Using the compromised OAuth token, the attacker took over the employee's Vercel-linked Google Workspace account, bypassing standard authentication controls.
4. **Internal Environment Access:** From the compromised Workspace account, the attacker accessed Vercel environments and environment variables not marked as 'sensitive' — these are stored unencrypted and were therefore readable.

Critically, environment variables marked 'sensitive' in Vercel are stored encrypted and there is no current evidence they were accessed. The blast radius was partially contained by Vercel's tiered secret-storage model.

Vercel has flagged a specific OAuth application identifier for administrators to check:
`110671459871-30f1spbu0hptbs60cb4vsmv79i7bbvqj.apps.googleusercontent.com`

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The initial vector was a trusted AI tool (Context.ai) whose compromise cascaded into a downstream enterprise breach — a canonical supply chain attack.
- **AML.T0012 (Valid Accounts):** Stolen OAuth tokens constituted valid credentials, enabling authentication without triggering typical anomaly detection.
- **AML.T0047 (ML-Enabled Product or Service):** Context.ai as an AI SaaS product was the attack surface entry point.
- **LLM05 (Supply Chain Vulnerabilities):** Third-party AI tool integration introduced an uncontrolled dependency with excessive trust.
- **LLM07 (Insecure Plugin Design) / LLM08 (Excessive Agency):** The 'Allow All' OAuth scope granted the AI tool disproportionate access to enterprise identity infrastructure.

## Impact Assessment

A limited subset of Vercel customers had credentials exposed. Vercel has contacted affected customers and urged immediate credential rotation. The full scope of exfiltrated data remains under investigation with Mandiant engaged as incident responder. The $2 million asking price from ShinyHunters suggests the attacker believes the data has significant secondary market value, likely including API keys, deployment secrets, or customer PII embedded in environment variables.

## Mitigation & Recommendations

- **Revoke broad OAuth grants** from all third-party AI tools; enforce least-privilege scopes at the identity provider level.
- **Audit Google Workspace OAuth applications** for the flagged app ID and any other unrecognised grants.
- **Rotate all Vercel environment variables** not marked sensitive; migrate secrets to the sensitive tier immediately.
- **Enable Deployment Protection** at Standard level or above and rotate Deployment Protection tokens.
- **Review deployment and activity logs** for anomalous access patterns dating back to March 2026.
- **Establish policy** prohibiting use of enterprise SSO credentials for personal or unapproved AI SaaS sign-ups.

## References

- [The Hacker News — Vercel Breach Tied to Context AI Hack](https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html)
