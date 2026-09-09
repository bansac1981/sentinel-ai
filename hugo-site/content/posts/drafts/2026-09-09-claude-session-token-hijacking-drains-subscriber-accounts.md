---
title: "Claude Session Token Hijacking Drains Subscriber Accounts"
date: 2026-09-09T07:37:42+00:00
draft: true
slug: "claude-session-token-hijacking-drains-subscriber-accounts"

# ── Content metadata ──
summary: "Attackers are compromising Claude subscriber accounts by stealing session keys and minting unauthorised OAuth tokens, silently consuming paid token allowances without detection. The attack exploits a lack of itemised usage logging, allowing theft to persist undetected for extended periods. Multiple users across Reddit and GitHub have reported identical patterns, indicating a broader, coordinated credential-theft campaign targeting Anthropic's platform."
source: "TechCrunch AI"
source_url: "https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers"
source_title: "Hackers are stealing Claude tokens from subscribers"
source_date: 2026-09-08T21:10:27+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1621944190272-ec775aad58d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxN3x8b3BlbiUyMGJvb2slMjBrbm93bGVkZ2UlMjBjb25jZXB0fGVufDB8MHx8fDE3ODg5Mzk0NjJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0113 - Steal Web Session Cookie", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0040 - AI Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM07 - Insecure Plugin Design", "LLM06 - Sensitive Information Disclosure", "LLM04 - Model Denial of Service"]

# ── TL;DR ──
tldr_what: "Attackers stole Claude session keys to mint OAuth tokens and drain paid subscriber allowances covertly."
tldr_who_at_risk: "Claude Max and paid Anthropic subscribers using Claude Code and agentic integrations are most exposed due to weak session controls and absent itemised usage logging."
tldr_actions: ["Rotate all Claude session keys and revoke active OAuth tokens immediately", "Audit third-party services connected to your Anthropic account and remove unrecognised integrations", "Monitor daily token consumption for anomalous spikes and report irregularities to Anthropic promptly"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Industry News"]
tags: ["claude", "anthropic", "session-hijacking", "token-theft", "oauth", "credential-compromise", "claude-code", "account-takeover", "ai-subscription-abuse", "llm-access"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-09T07:37:42+00:00"
feed_source: "techcrunch_ai"
original_url: "https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers"
pipeline_version: "2.1.0"
---

## Overview

A coordinated campaign of Claude account takeovers has emerged, with attackers stealing session keys from paid subscribers and covertly consuming their token allowances via unauthorised OAuth token minting. First reported by independent AI consultant Grant De Swardt on 8 September 2026, the attack pattern has since been corroborated by multiple users on Reddit and GitHub, suggesting a systemic exploitation effort targeting Anthropic's Claude platform—particularly Claude Max and Claude Code users.

The incident highlights a dangerous gap in AI platform security: the absence of itemised usage logging means fraudulent consumption can persist for weeks or months before victims notice.

## Technical Analysis

Anthropologic's post-incident investigation identified a compromised Claude session key as the root cause in De Swardt's case. The attacker used this key to **mint unauthorised Claude Code OAuth tokens**, effectively granting themselves persistent, delegated API access under the victim's billing context.

Key attack characteristics observed:

- **Session key exfiltration**: The exact exfiltration vector was not confirmed by Anthropic, but evidence is consistent with credential theft via a malicious third-party service or session data interception.
- **OAuth token forgery**: Stolen session credentials were used to generate additional access tokens, enabling long-lived, parallel access.
- **Covert token consumption**: Usage occurred continuously, including during periods of zero legitimate user activity, indicating automated or scripted abuse.
- **No itemised audit trail**: Anthropic's current billing system tracks aggregate usage only, preventing victims from identifying which sessions or tools consumed tokens.

The pattern of usage escalating during confirmed idle periods (45% to 55% with all local tasks paused) is consistent with a background process operating under stolen credentials.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0113 – Steal Web Session Cookie | Session key theft is the probable initial access vector |
| MITRE ATLAS | AML.T0012 – Valid Accounts | Attacker operates using legitimate victim credentials |
| MITRE ATLAS | AML.T0083 – Credentials from AI Agent Config | OAuth tokens extracted or minted from agent session context |
| MITRE ATLAS | AML.T0040 – AI Model Inference API Access | Unauthorised API consumption under victim's quota |
| OWASP | LLM07 – Insecure Plugin Design | Third-party service integration as suspected access vector |
| OWASP | LLM04 – Model Denial of Service | Token exhaustion effectively denies service to paying users |

## Impact Assessment

- **Financial harm**: Subscribers pay up to $200/month and lose token allowances they cannot recover without escalation.
- **Business disruption**: Agentic workflows and automated business processes dependent on Claude are interrupted when accounts are suspended.
- **Detection gap**: Lack of granular usage logs means attacks may persist for billing cycles before detection.
- **Scale unknown**: Community reports across Reddit and GitHub suggest multiple victims; the true scale has not been confirmed by Anthropic.

## Mitigation & Recommendations

1. **Revoke all active sessions**: Log out of all Claude sessions and invalidate existing OAuth tokens via account settings immediately if anomalous usage is suspected.
2. **Audit third-party integrations**: Review all connected services and revoke access for unrecognised or unused applications.
3. **Enable usage alerting**: Where available, configure usage threshold notifications; contact Anthropic to request itemised session logs.
4. **Apply least-privilege to agent tokens**: Limit OAuth scopes granted to Claude Code and agentic workflows to the minimum required.
5. **Report anomalies immediately**: Contact Anthropic support at the first sign of unexplained token consumption to preserve eligibility for remediation.

Anthropologists should consider implementing mandatory itemised usage logging, OAuth token issuance notifications, and per-session consumption caps as platform-level controls.

## References

- [Hackers are stealing Claude tokens from subscribers – TechCrunch](https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers)
