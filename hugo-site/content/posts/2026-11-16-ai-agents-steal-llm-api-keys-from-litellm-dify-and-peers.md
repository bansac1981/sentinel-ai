---
title: "AI Agents Steal LLM API Keys from LiteLLM, Dify, and Peers"
date: 2026-11-16T13:54:03+00:00
draft: false
slug: "ai-agents-steal-llm-api-keys-from-litellm-dify-and-peers"

# ── Content metadata ──
summary: "Amazon's threat intelligence team captured records from autonomous AI agents actively targeting internet-exposed LLM gateway and AI app-builder platforms to harvest stored API keys, using tools like ARTEX and exploiting default credentials, authentication bypasses, and SSRF vulnerabilities. The stolen keys were then recycled to fund further automated reconnaissance, creating a self-sustaining credential theft loop. Attribution points to China-linked operators based on Simplified Chinese prompts and time zone metadata embedded in the captured agent logs."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/amazon-uncovers-ai-agent-campaign.html"
source_title: "Amazon Uncovers AI Agent Campaign Targeting LiteLLM, Dify, and Other Apps for API Keys"
source_date: 2026-11-16T07:34:21+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1771792278518-1ae81427d1f4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNnx8dGV4dCUyMHR5cG9ncmFwaHklMjBhYnN0cmFjdCUyMGxldHRlcnN8ZW58MHwwfHx8MTc5NDgzNzI0Mnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0103 - Deploy AI Agent", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0040 - AI Model Inference API Access", "AML.T0012 - Valid Accounts", "AML.T0057 - LLM Data Leakage", "AML.T0069 - Discover LLM System Information"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Autonomous AI agents targeted LLM gateway apps to steal and recycle API keys at scale."
tldr_who_at_risk: "Any organisation running internet-exposed LLM proxies or AI app-builders such as LiteLLM, Dify, Langflow, or One API is directly at risk of API key theft."
tldr_actions: ["Rotate all API keys stored in LiteLLM, Dify, One API, and related LLM gateway deployments immediately", "Remove default master keys and restrict admin endpoints to authenticated, IP-allowlisted access only", "Block unauthenticated access to environment files, source maps, debug routes, and cloud metadata endpoints"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Supply Chain", "Industry News"]
tags: ["api-key-theft", "ai-agents", "litellm", "dify", "artex", "llm-gateway", "credential-harvesting", "ssrf", "china-nexus", "madpot", "one-api", "langflow", "ragflow", "autonomous-attack", "default-credentials"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-11-16T13:54:03+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/amazon-uncovers-ai-agent-campaign.html"
pipeline_version: "2.1.0"
content_hash: "c0d07b05660d5046"
---

## Overview

Amazon's threat intelligence team has disclosed an active campaign in which autonomous AI agents systematically hunted for internet-exposed LLM gateway and AI application-builder platforms to extract stored API keys. Using decoy servers within its MadPot honeypot network, Amazon captured detailed agent logs between October 3 and mid-November 2026 that reveal a self-funding attack loop: stolen keys were immediately pooled and used to pay for the LLM calls powering further reconnaissance. The team attributes the activity with moderate confidence to separate China-linked operators, citing Simplified Chinese-language prompts and China-aligned time zone settings embedded in captured records.

## Technical Analysis

The tooling assessed to underlie the campaign is **ARTEX**, an open-source penetration testing framework built around AI agents. An operator provides a target and an objective; a planner agent decomposes the goal into discrete tasks delegated to worker agents that invoke security tooling. At each decision point the agents query an LLM, allowing adaptive, context-aware traversal of a target's attack surface.

The agents carried a structured playbook of known entry points across targeted products:

- **Default credentials**: LiteLLM's well-known default master key and similar shipped-default secrets.
- **Incomplete installations**: Setup wizards left accessible to unauthenticated outsiders.
- **Authentication bypass**: The `isCliRequest` header bypass affecting One API family systems.
- **SSRF via URL-fetch features**: Used to reach AWS/cloud metadata services and retrieve instance credentials.
- **Client-side secret leakage**: API keys embedded in JavaScript bundles, source maps, debug routes, and `.env` files.
- **Known CVEs**: Specific flaws in Langflow and RAGFlow were listed in the playbook.

Targeted platforms included LLM proxies and gateways (One API, New API, Veloera, Sub2API, LiteLLM) and AI app-builders (Dify, FastGPT, Langflow, RAGFlow, Open WebUI, LobeChat, Ollama). These were prioritised because a single compromised admin interface can expose keys for dozens of upstream AI providers simultaneously.

In a corroborating incident, Cloudflare's responders observed ARTEX leverage a compromised CI/CD API token with no IP restrictions or rate limiting, triggering 400 database dump requests within a single hour.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS AML.T0083 | Credentials from AI Agent Configuration | Agents extracted keys from app config and environment files |
| ATLAS AML.T0098 | AI Agent Tool Credential Harvesting | Pooling stolen keys to fund further agent operations |
| ATLAS AML.T0103 | Deploy AI Agent | ARTEX deployed worker agents autonomously against targets |
| ATLAS AML.T0040 | AI Model Inference API Access | Stolen keys abused for direct model API calls |
| OWASP LLM06 | Sensitive Information Disclosure | API keys leaked via source maps, env files, debug routes |
| OWASP LLM08 | Excessive Agency | Autonomous agents acted without human authorisation checkpoints |

## Impact Assessment

Organisations hosting any of the named platforms on internet-facing infrastructure face immediate risk of full API key compromise across every AI provider integrated into those platforms. Cloud credentials harvested via SSRF extend the blast radius to managed AI services and secret stores. The self-funding nature of the campaign means operators face minimal marginal cost per additional target, enabling indefinite scale.

## Mitigation & Recommendations

1. **Rotate all API keys** stored in LiteLLM, Dify, One API, and related platforms without delay.
2. **Eliminate default credentials**: Change or disable shipped default master keys before any internet exposure.
3. **Restrict admin endpoints** to authenticated sessions with IP allowlisting and MFA.
4. **Block metadata service access**: Apply IMDSv2 enforcement and network-level controls to prevent SSRF to `169.254.169.254`.
5. **Audit client-side assets**: Scan JavaScript bundles, source maps, and static files for embedded secrets.
6. **Apply rate limiting and IP restrictions** to all CI/CD and programmatic API tokens.
7. **Monitor for ARTEX signatures**: Review logs for unusual sequential scanning of AI app admin paths and bulk database query patterns.

## References

- [Amazon Uncovers AI Agent Campaign Targeting LiteLLM, Dify, and Other Apps for API Keys — The Hacker News](https://thehackernews.com/2026/11/amazon-uncovers-ai-agent-campaign.html)
