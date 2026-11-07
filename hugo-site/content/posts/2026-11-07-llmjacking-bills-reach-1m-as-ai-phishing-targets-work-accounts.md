---
title: "LLMJacking Bills Reach $1M as AI Phishing Targets Work Accounts"
date: 2026-11-07T11:58:39+00:00
draft: false
slug: "llmjacking-bills-reach-1m-as-ai-phishing-targets-work-accounts"

# ── Content metadata ──
summary: "A weekly security roundup highlights two significant AI-related threats: LLMjacking attacks have now generated bills exceeding $1 million for victims whose cloud-hosted LLM credentials were stolen and abused, and a phishing campaign is exploiting fake OpenAI, SpaceX, and Anthropic event invitations to harvest corporate Microsoft and Google credentials. Additionally, Anthropic has responded to the broader threat environment by rolling out enterprise security controls including inference hooks for DLP inspection. These developments underscore the growing financial and credential-theft risks tied directly to AI platform adoption."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/in-other-news-trezor-implant-llmjacking-bills-hit-1m-sap-flaws-weaponized-within-days"
source_title: "In Other News: Trezor Implant, LLMJacking Bills Hit $1M, SAP Flaws Weaponized Within Days"
source_date: 2026-11-06T14:40:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1738082956257-06cde4444b1c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8bmV1cmFsJTIwcGF0dGVybiUyMGFic3RyYWN0JTIwbmV0d29yayUyMGxpZ2h0fGVufDB8MHx8fDE3OTQwNTI3MTh8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - AI Model Inference API Access", "AML.T0012 - Valid Accounts", "AML.T0113 - Steal Web Session Cookie", "AML.T0114 - AI Service Web Interface", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM04 - Model Denial of Service", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "LLMjacking attacks have surpassed $1M in fraudulent AI API billing charges for victims."
tldr_who_at_risk: "Enterprises using cloud-hosted LLM APIs and marketing employees targeted by fake AI-brand event phishing pages are most directly exposed."
tldr_actions: ["Audit cloud LLM API credentials and rotate any that may have been exposed or reused across services", "Block device code authentication flows at the identity provider level to counter Kali365-style phishing", "Enable Anthropic Claude Enterprise inference hooks to route prompts through existing DLP tooling"]

# ── Taxonomies ──
categories: ["LLM Security", "Industry News", "Supply Chain"]
tags: ["llmjacking", "credential-theft", "phishing", "openai", "anthropic", "claude-enterprise", "device-code-phishing", "ai-billing-abuse", "cloud-llm", "spacex-lure", "phishing-as-a-service", "kali365"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-07T11:58:39+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/in-other-news-trezor-implant-llmjacking-bills-hit-1m-sap-flaws-weaponized-within-days"
pipeline_version: "2.1.0"
content_hash: "992e353bb7b5fafa"
---

## Overview

This week's security roundup from SecurityWeek surfaces two AI-specific threats with real financial and operational consequences. First, LLMjacking — the practice of stealing cloud-hosted LLM API credentials to run inference at the victim's expense — has now crossed the $1 million threshold in accumulated fraudulent billing. Second, a documented phishing campaign is using fake event registration pages impersonating OpenAI, SpaceX, and Anthropic to harvest corporate Microsoft and Google credentials from marketing employees.

On the defensive side, Anthropic has introduced a suite of enterprise security controls for Claude, including inference hooks that allow organisations to inspect prompts and tool calls through existing DLP pipelines before they reach the model.

## Technical Analysis

**LLMjacking at scale:** Threat actors obtain valid API keys — typically through credential stuffing, misconfigured repositories, or phishing — and then use them to run high-volume inference workloads. Because LLM API costs are metered, victims face enormous unexpected charges before detecting the abuse. The $1M figure represents cumulative billing across affected organisations, illustrating how rapidly stolen credentials can be monetised without directly exfiltrating data.

**AI-brand phishing campaign:** Push Security documented a campaign using fake registration pages for OpenAI, SpaceX, and Anthropic events, baiting targets with incentives such as three months of ChatGPT Pro or Grok Heavy access. The Microsoft login path triggers a device code authentication flow delivered via the Kali365 phishing-as-a-service platform, which captures tokens without requiring the attacker to intercept a password directly. The campaign uses Google and Zapier short links, Cloudflare challenges for evasion, and rotates domains every few weeks. Push links the operator with medium-high confidence to earlier fake Zoom event phishing infrastructure.

## Framework Mapping

- **AML.T0040 (AI Model Inference API Access):** LLMjacking directly abuses inference APIs using stolen credentials to consume compute at victim expense.
- **AML.T0012 (Valid Accounts):** Both attack chains rely on obtaining and abusing legitimate credentials — API keys in LLMjacking, OAuth tokens in the phishing campaign.
- **AML.T0113 (Steal Web Session Cookie) / AML.T0114 (AI Service Web Interface):** The device code phishing flow targets AI service authentication specifically, harvesting tokens that grant access to work accounts.
- **LLM06 (Sensitive Information Disclosure):** Stolen API access could expose prompts, outputs, and organisational data processed through the LLM.
- **LLM04 (Model Denial of Service):** Sustained API abuse from LLMjacking degrades service availability and imposes financial denial-of-service on victims.

## Impact Assessment

Organisations with exposed LLM API credentials face direct financial harm through unexpected inference billing, potentially reaching hundreds of thousands of dollars before detection. Marketing teams — specifically those likely to register for professional events — are the primary target demographic for the phishing campaign. Successful device code phishing yields persistent OAuth tokens that can bypass MFA and enable lateral movement within Microsoft 365 or Google Workspace environments well beyond the initial AI service account.

## Mitigation & Recommendations

- **Rotate and scope LLM API keys** — apply least-privilege scopes, set billing alerts, and store credentials in secrets managers rather than code repositories.
- **Disable device code flow** at the identity provider level for all users who do not require it, or restrict it to managed devices.
- **Deploy Anthropic Claude Enterprise inference hooks** to run prompts through DLP inspection before model execution.
- **Train marketing and event-registration-heavy teams** to verify event invitations through official brand channels before entering work credentials.
- **Monitor for anomalous LLM API spend** using cloud cost anomaly detection with low thresholds tuned to baseline usage.

## References

- [SecurityWeek – In Other News: Trezor Implant, LLMJacking Bills Hit $1M, SAP Flaws Weaponized Within Days](https://www.securityweek.com/in-other-news-trezor-implant-llmjacking-bills-hit-1m-sap-flaws-weaponized-within-days)
