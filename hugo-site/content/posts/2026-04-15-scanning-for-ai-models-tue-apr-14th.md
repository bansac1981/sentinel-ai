---
title: "Scanning for AI Models, (Tue, Apr 14th)"
date: "2026-04-15T05:39:27+00:00"
draft: false
slug: "scanning-for-ai-models-tue-apr-14th"

# ── Content metadata ──
summary: "A single threat actor (IP 81.168.83.103) has been systematically scanning internet-facing systems since at least January 2026, specifically targeting credential files, API tokens, and configuration data associated with popular AI platforms including OpenAI, Anthropic Claude, HuggingFace, and the Openclaw/Clawdbot tools. The campaign focuses on harvesting AI API credentials and secrets stored in predictable file paths, representing a targeted reconnaissance effort against AI model deployments. If successful, these probes could enable API key theft, model access abuse, and broader compromise of AI-integrated systems."
# ── TL;DR ──
tldr_what: "Single IP systematically scans for exposed AI platform credentials across internet-facing systems."
tldr_who_at_risk: "Organizations running OpenAI, Anthropic, HuggingFace, or Openclaw tools with misconfigured web servers or exposed credential files."
tldr_actions: ["Audit web server roots for exposed .openclaw, .claude, .cache, openai directories.", "Rotate all AI API keys and tokens if your systems match targeted file paths.", "Implement access controls blocking external HTTP requests to credential storage locations."]
source: "SANS Internet Storm Center"
source_url: "https://isc.sans.edu/diary/rss/32896"
source_date: 2026-04-15T00:19:53+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://isc.sans.edu/diaryimages/images/81_168_83_103_pic1.png"

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0040 - ML Model Inference API Access", "AML.T0044 - Full ML Model Access", "AML.T0010 - ML Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM10 - Model Theft", "LLM05 - Supply Chain Vulnerabilities"]

# ── Taxonomies ──
categories: ["Model Theft", "LLM Security", "Industry News", "Research"]
tags: ["credential-harvesting", "api-key-theft", "internet-scanning", "openai", "claude", "huggingface", "openclaw", "clawdbot", "moltbot", "dshield", "honeypot", "reconnaissance", "ai-credentials", "threat-intelligence"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-15T04:35:09+00:00"
feed_source: "sans_isc"
original_url: "https://isc.sans.edu/diary/rss/32896"
pipeline_version: "1.0.0"
---

## Overview

Beginning March 10, 2026 — with earlier port-scanning activity dating back to January 29, 2026 — a single IP address (81.168.83.103, AS 20860) has been systematically probing internet-exposed systems for credential files and configuration secrets associated with major AI platforms, including OpenAI, Anthropic Claude, HuggingFace, and the lesser-known Openclaw/Clawdbot toolset. Detected via SANS ISC DShield honeypot sensors and analysed through Kibana ES|QL queries against Cowrie logs, the campaign recorded 52 distinct probe events between March 10 and April 13, 2026, with a peak on April 3rd. This represents a focused, persistent adversarial effort to harvest AI API credentials at scale from misconfigured or publicly exposed systems.

## Technical Analysis

The actor is making HTTP requests targeting well-known default file paths where AI tools store authentication tokens, API keys, and database files. Targeted paths include:

```
/.openclaw/workspace/db.sqlite
/.openclaw/workspace/chroma.db
/.openclaw/secrets.json
/.clawdbot/moltbot.json
/.claude/settings.json
/.claude/.credentials.json
/.cache/huggingface/token
/openai/env.json
/openai/credentials.json
```

These paths correspond to local credential stores used by AI CLI tools, agent frameworks, and developer environments. If any of these files are accidentally exposed via a web server root or misconfigured container, the attacker can silently retrieve valid API keys without triggering authentication failures. The DShield sensor's Cowrie honeypot logs HTTP request bodies, allowing the analyst to filter probes using an ES|QL query matching keywords such as `openclaw`, `claude`, `huggingface`, `openai`, and `clawdbot`.

The Moltbot reference is notable — OX Security previously documented Moltbot as a tool involved in significant data exposure incidents, suggesting the actor may be targeting deployments of specific agentic or automation tooling.

## Framework Mapping

- **AML.T0012 (Valid Accounts):** The ultimate objective is to obtain legitimate API credentials enabling authenticated access to AI inference APIs.
- **AML.T0040 (ML Model Inference API Access):** Harvested keys would grant direct access to model APIs (OpenAI, Claude, HuggingFace endpoints).
- **AML.T0044 (Full ML Model Access):** With valid credentials, an attacker could query, abuse, or exfiltrate model outputs at scale.
- **LLM06 (Sensitive Information Disclosure):** The targeted files contain API tokens and secrets that, if exposed, directly disclose access credentials.
- **LLM10 (Model Theft):** Stolen API keys enable unauthorized use of paid/proprietary model capacity.

## Impact Assessment

Developers, data scientists, and organisations running AI-integrated pipelines on internet-accessible infrastructure are at risk. Exposed credentials could result in financial loss through API quota abuse, data exfiltration via model queries, lateral movement into broader cloud environments, and reputational damage. The Chroma vector database files (`.chroma.db`) targeted also suggest interest in RAG (Retrieval-Augmented Generation) pipeline contents, which may contain sensitive embedded documents.

## Mitigation & Recommendations

1. **Audit web-accessible directories** to ensure AI credential files and `.env` files are not served publicly.
2. **Rotate API keys** for OpenAI, Anthropic, and HuggingFace immediately if any exposure is suspected.
3. **Block or monitor IP 81.168.83.103** at perimeter firewalls and SIEM alerting.