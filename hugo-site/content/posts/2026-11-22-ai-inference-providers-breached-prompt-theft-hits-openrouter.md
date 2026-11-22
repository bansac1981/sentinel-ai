---
title: "AI Inference Providers Breached: Prompt Theft Hits OpenRouter"
date: 2026-11-22T13:30:48+00:00
draft: false
slug: "ai-inference-providers-breached-prompt-theft-hits-openrouter"

# ── Content metadata ──
summary: "Researchers at Dragos uncovered months-long prompt theft campaigns targeting at least three AI inference providers accessible via OpenRouter, using canary token techniques to confirm that live customer requests \u2014 including those flagged as Zero Data Retention \u2014 were being exfiltrated. Attackers leveraged stolen credentials to perform lateral movement into AWS environments, including S3, Secrets Manager, and IAM manipulation. A secondary vector involved malicious marketplace sellers who enabled request logging to passively harvest credentials and secrets flowing through their listed models."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html"
source_title: "OpenRouter Drops 3 Providers After Researchers Catch Months of Prompt Theft at AI Hosting Firms"
source_date: 2026-11-22T05:06:55+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1651964178942-ccecb82a18be?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMnx8ZWxlY3Ryb25pYyUyMGNvbXBvbmVudHMlMjBzb2xkZXJpbmclMjBtYWNyb3xlbnwwfDB8fHwxNzk1MzU0MjQ3fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0040 - AI Model Inference API Access", "AML.T0010 - AI Supply Chain Compromise", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0063 - Discover AI Model Outputs", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Three AI inference providers silently exfiltrated customer prompts for months, including Zero Data Retention requests."
tldr_who_at_risk: "Any enterprise or developer routing sensitive AI requests through third-party inference providers or AI model marketplaces, particularly via OpenRouter-connected endpoints."
tldr_actions: ["Audit all third-party AI inference providers for request logging policies and contractual data handling obligations", "Add artex-agent and artex-judge-r121 user agents to your detection rules immediately", "Rotate any AWS keys, secrets, or credentials that may have transited AI inference APIs in the July–November window"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News", "Research"]
tags: ["prompt-theft", "inference-provider", "openrouter", "zero-data-retention", "canary-tokens", "credential-harvesting", "aws-compromise", "dragos", "ai-supply-chain", "data-breach", "request-logging", "artex"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-22T13:30:48+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html"
pipeline_version: "2.1.0"
content_hash: "257b2a25fe22c2bb"
---

## Overview

Researchers at Dragos have exposed a months-long prompt theft operation targeting at least three AI inference providers connected to OpenRouter, a popular AI request routing gateway. Using canary token methodology — seeding approximately two million prompts with unique traceable credentials and URLs between July and November 2026 — the team confirmed that live customer requests were being copied and exfiltrated, in some cases before models ever processed them. OpenRouter has since removed three providers, deregistered 125 endpoints from Zero Data Retention eligibility, and notified affected customers. Critically, the breach occurred at the provider layer, not within OpenRouter itself.

## Technical Analysis

The research identified two distinct attack vectors.

**Vector 1 — Infrastructure Compromise:** The largest breach involved planted AWS keys sent in single, unique requests to specific providers during short windows in late October. Every request submitted during those windows was stolen. The exfiltration point was upstream of model inference — traffic was intercepted at the first point of arrival, indicating a network-layer or ingestion-layer tap rather than model-level access. Attackers acted quickly: stolen keys were tested within hours, with follow-on activity including S3 bucket enumeration, Secrets Manager and Parameter Store queries, Bedrock API key creation attempts, and IAM user additions — generating tens of thousands of AWS API calls. One threat actor appears to have simultaneously compromised two providers from a single rented server. On November 1st, the same actor deployed ARTEX, an AI-driven penetration testing framework, using its `artex-agent` and `artex-judge-r121` user agents solely to verify that previously stolen keys remained active. Neither user agent appears in any public threat intelligence feed.

**Vector 2 — Malicious Marketplace Participation:** The second vector required no technical breach. Individuals — appearing to operate from residential internet connections — listed AI models at below-market prices on an inference marketplace, enabled request logging, and passively harvested credentials from prompts flowing through their listings. One operator, traced to a Mac on home broadband in France, manually attempted root SSH logins using harvested passwords, then tested planted AWS keys by hand. One of those keys had arrived via a router that was quietly forwarding traffic to the marketplace without customer disclosure.

## Framework Mapping

- **AML.T0057 (LLM Data Leakage):** Customer prompts, including sensitive secrets, were exfiltrated en masse.
- **AML.T0040 (AI Model Inference API Access):** Attackers exploited their position within the inference pipeline to intercept traffic.
- **AML.T0010 (AI Supply Chain Compromise):** Providers within OpenRouter's trusted ecosystem were the attack surface.
- **AML.T0083 (Credentials from AI Agent Configuration):** AWS keys and secrets embedded in prompts were harvested and operationalised.
- **LLM06 (Sensitive Information Disclosure):** Privacy controls including Zero Data Retention were rendered ineffective by provider-layer compromise.
- **LLM05 (Supply Chain Vulnerabilities):** Trust delegated to third-party providers was exploited without customer visibility.

## Impact Assessment

The impact is severe. Zero Data Retention — a control that enterprises frequently rely on for regulatory compliance and confidentiality — provided no protection once an attacker was inside the provider. Any organisation routing prompts containing credentials, PII, proprietary data, or internal system references through these providers during the affected window should treat that data as compromised. The credential harvesting and subsequent AWS lateral movement represent a secondary breach surface with potentially significant blast radius.

## Mitigation & Recommendations

1. **Rotate all credentials** that may have transited affected inference endpoints between July and November 2026.
2. **Add detection rules** for user agents `artex-agent` and `artex-judge-r121` across network, endpoint, and cloud logging.
3. **Audit inference providers** for data handling practices — contractual Zero Data Retention guarantees must be verified technically, not taken on trust.
4. **Review AI routing configurations** to ensure no undisclosed traffic forwarding hops exist between your requests and the destination model.
5. **Treat AI prompt traffic as sensitive data in transit** — apply the same controls (encryption, access control, audit logging) you would to any credential or PII.

## References

- [OpenRouter Drops 3 Providers After Researchers Catch Months of Prompt Theft at AI Hosting Firms — The Hacker News](https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html)
