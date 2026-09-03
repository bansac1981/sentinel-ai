---
title: "METR API Key Theft Exposes $600K in AI Credits via Agent"
date: 2026-09-03T10:04:16+00:00
draft: true
slug: "metr-api-key-theft-exposes-600k-in-ai-credits-via-agent"

# ── Content metadata ──
summary: "METR, an AI safety non-profit, disclosed two security incidents in early 2026 in which attackers stole an API key from an exposed agent orchestration dashboard and consumed approximately $600,000 worth of AI inference credits over three weeks. The breach exploited a fail-open authentication vulnerability in a vibe-coded application, allowing the attacker to prompt an AI agent directly to reveal its model provider credentials. A second May incident involved systematic probing of METR's public infrastructure, highlighting the growing threat of financially motivated actors targeting AI research organisations for credential harvesting."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/attackers-steal-metr-api-key-and.html"
source_title: "Attackers Steal METR API Key and Consume AI Credits Worth About $600,000"
source_date: 2026-09-01T09:05:30+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8cGlwZWxpbmUlMjB3b3JrZmxvdyUyMGF1dG9tYXRpb24lMjBhYnN0cmFjdHxlbnwwfDB8fHwxNzg4NDI5NjcxfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0040 - AI Model Inference API Access", "AML.T0051 - LLM Prompt Injection", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0012 - Valid Accounts", "AML.T0069 - Discover LLM System Information"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM01 - Prompt Injection", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Attackers prompted METR's exposed AI agent to reveal its API key, stealing $600K in credits."
tldr_who_at_risk: "Any organisation running AI agents on publicly accessible infrastructure with embedded API credentials is directly exposed to this class of credential-harvesting attack."
tldr_actions: ["Never store model provider API keys in agent environments accessible from public infrastructure", "Implement token spend caps and real-time anomaly alerts on all AI inference accounts", "Audit all agent-facing applications for fail-open authentication vulnerabilities before deployment"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Industry News"]
tags: ["api-key-theft", "ai-credits", "agentic-ai", "credential-harvesting", "fail-open-vulnerability", "metr", "vibe-coding", "ec2-exposure", "llm-agent", "certificate-transparency", "inference-abuse", "financially-motivated"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-03T10:04:16+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/attackers-steal-metr-api-key-and.html"
pipeline_version: "2.1.0"
---

## Overview

METR (Model Evaluation and Threat Research), a non-profit conducting frontier AI safety evaluations, disclosed two significant security incidents in 2026. In March, attackers stole an API key from an exposed AI agent orchestration dashboard and consumed roughly $600,000 worth of inference credits over three weeks. A second incident in May involved systematic reconnaissance of METR's public infrastructure. Neither incident involved AI agents autonomously breaking into systems — both exploited conventional security failures compounded by the novel attack surface created by publicly accessible AI agents.

## Technical Analysis

The March incident followed a recognisable kill chain targeting AI agent deployments:

1. **Discovery via certificate transparency**: The attacker identified the target by scanning recently-registered domains indexed in certificate transparency logs, filtering for high-signal keywords associated with LLMs and agent frameworks — a low-cost, high-yield reconnaissance method.

2. **Fail-open authentication bypass**: A researcher had deployed a personal "vibe-coded" app on an EC2 instance intended to sit behind Google OAuth. A misconfiguration introduced a fail-open vulnerability that silently disabled authentication, exposing the agent orchestration dashboard to the public internet for several days.

3. **Direct agent prompting for credential extraction**: Once the dashboard was discovered, the attacker simply prompted the running agent to disclose its model provider API key — a form of prompt-driven credential extraction requiring no exploit tooling beyond a browser.

4. **Persistent access and abuse**: The attacker added an SSH key to the instance for persistence, then used the stolen API key to run inference workloads on public models over a three-week window. The spend went undetected because METR legitimately consumes large token volumes and had no spend caps configured.

The May incident involved a separate, likely financially motivated actor conducting systematic probing of METR's internet-facing endpoints, including an attempted (unsuccessful) data exfiltration via an inadvertently exposed internal endpoint.

## Framework Mapping

- **AML.T0083 / AML.T0098**: The core technique was harvesting credentials stored within or accessible to an AI agent configuration — a textbook agent credential extraction scenario.
- **AML.T0051 (LLM Prompt Injection)**: The attacker issued direct prompts to the agent to elicit the API key, exploiting the agent's responsiveness to external instructions.
- **AML.T0040 (AI Model Inference API Access)**: Stolen credentials were used to gain unauthorised access to AI inference infrastructure.
- **LLM06 (Sensitive Information Disclosure)**: The agent disclosed a high-value credential in response to an unauthenticated user prompt.
- **LLM08 (Excessive Agency)**: The agent had both access to sensitive credentials and the ability to surface them to any requester without access control enforcement.

## Impact Assessment

While no sensitive research data was exfiltrated and the credits were provided free-of-charge to METR, the financial impact — approximately $600,000 in inference costs — illustrates the commercial risk of API key exposure in AI environments. The attack technique is unsophisticated and scalable: certificate transparency scanning for vibe-coded AI apps is a viable mass-harvesting strategy that low-skill actors can operationalise. AI research organisations and startups embedding API keys in agent environments face elevated exposure.

## Mitigation & Recommendations

- **Never embed model provider API keys in publicly accessible agent environments** — use secrets managers with scoped, short-lived credentials.
- **Enforce spend caps and anomaly-based billing alerts** on all inference accounts, including high-volume research accounts.
- **Test all agent-facing applications for fail-open conditions** before deployment, particularly those using third-party authentication middleware.
- **Monitor certificate transparency logs** for your own domains to detect inadvertent public exposure early.
- **Restrict agent responsiveness to credentialed principals only** — agents should never surface secrets to unauthenticated prompt sources.
- **Segment METR or research credentials from personal or experimental infrastructure** by policy.

## References

- [The Hacker News — Attackers Steal METR API Key and Consume AI Credits Worth About $600,000](https://thehackernews.com/2026/09/attackers-steal-metr-api-key-and.html)
