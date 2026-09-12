---
title: "AI Agent Builds Self-Expanding Stolen LLM Inference Supply Chain"
date: 2026-09-12T09:25:29+00:00
draft: true
slug: "ai-agent-builds-self-expanding-stolen-llm-inference-supply-chain"

# ── Content metadata ──
summary: "A researcher operating an AI honeypot captured a semi-autonomous coding agent conducting a full-cycle offensive operation: locating poorly secured LLM resale gateways, harvesting API credentials via web vulnerabilities, validating stolen inference capacity, and aggregating it behind an attacker-controlled unified gateway. The operation is notable not for novel individual techniques but for its feedback loop architecture \u2014 stolen inference capacity is used to fund and expand further credential theft, creating a partially self-sustaining supply chain. The honeypot inadvertently received ~43 KB of the agent's control-plane data, including its AGENTS.md playbook, collected API keys, reconnaissance scripts, and the operator's unproxied egress IP."
source: "SANS Internet Storm Center"
source_url: "https://isc.sans.edu/diary/rss/33332"
source_title: "The Self-Expanding Stolen Inference Supply Chain: An AI Agent Harvesting and Re-Serving LLM Access, (Fri, Sep 11th)"
source_date: 2026-09-11T14:40:32+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1593309377731-e05d89e139b3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMXx8c2Nyb2xsJTIwbWFudXNjcmlwdCUyMGFuY2llbnQlMjBrbm93bGVkZ2V8ZW58MHwwfHx8MTc4OTIwNTEyOXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - AI Model Inference API Access", "AML.T0010 - AI Supply Chain Compromise", "AML.T0103 - Deploy AI Agent", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0012 - Valid Accounts", "AML.T0047 - AI-Enabled Product or Service", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM10 - Model Theft", "LLM04 - Model Denial of Service"]

# ── TL;DR ──
tldr_what: "An autonomous agent harvested stolen LLM API keys and aggregated them into a self-expanding attacker-controlled inference gateway."
tldr_who_at_risk: "LLM resale platform operators and API gateway providers with weak authentication or open registration are directly exposed to credential harvesting and inference theft."
tldr_actions: ["Audit all LLM API gateway endpoints for unauthenticated model catalog exposure and default credential risks", "Implement rate limiting, anomaly detection, and billing alerts on inference endpoints to detect harvesting behaviour", "Deploy honeypot LLM endpoints to surface attacker playbooks and enumerate active offensive infrastructure"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security", "Model Theft"]
tags: ["llm-inference-theft", "ai-agent-attack", "api-key-harvesting", "inference-supply-chain", "honeypot", "llm-reseller", "autonomous-agent", "credential-theft", "new-api", "v2board", "fofa-recon", "agentic-offense"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-12T09:25:29+00:00"
feed_source: "sans_isc"
original_url: "https://isc.sans.edu/diary/rss/33332"
pipeline_version: "2.1.0"
---

## Overview

A SANS Internet Storm Center researcher operating an AI honeypot captured a sophisticated, semi-autonomous coding agent conducting a complete offensive inference supply chain operation. Unlike conventional credential theft, the attacker built a feedback loop: stolen LLM API access was consolidated into an attacker-controlled gateway, which in turn powered further reconnaissance and harvesting. The operation represents a maturing class of AI-native cybercrime in which the commodity being stolen is inference capacity itself.

## Technical Analysis

The honeypot emulated an OpenAI-compatible inference endpoint. When the agent called it as a free LLM backend, it inadvertently transmitted approximately 43 KB of its own control-plane context — including an `AGENTS.md` file, an offensive playbook, infrastructure notes, reconnaissance scripts, harvested API keys, and prior target lists.

The captured workflow followed four stages:

**1. Discovery.** The agent generated FOFA search queries (`title="V2Board"`, `header="subscription-userinfo"`) to locate LLM resale gateways and subscription infrastructure exposed on the open internet.

**2. Access Acquisition.** The playbook enumerated multiple acquisition vectors: open registration with free credit balances, default credentials, `group_id` authorization weaknesses, exposed endpoints such as `/api/auth-files`, and automated trial-account farming using temporary email services and CAPTCHA-solving APIs.

**3. Inference Validation.** Harvested keys were tested against resale endpoints advertising current premium model names (e.g., `claude-opus-5`). The researcher notes that model name labels are reseller claims, not verified model identities. Validation evolved over sessions to include a functional code-logic test — asking each endpoint to compute a factorial — to distinguish live inference from canned responses.

**4. Aggregation and Re-Serving.** A second capture session documented the attacker standing up a self-hosted `New-API` instance to aggregate validated keys behind a single unified gateway, completing the supply chain loop.

A critical operational security failure was also captured: the playbook instructed the agent to verify its proxy was active before attacking by comparing the proxied IP against a reference value — which was the operator's real, unproxied egress IP, exposing it directly to the honeypot.

## Framework Mapping

This operation maps to several MITRE ATLAS techniques: **AML.T0040** (AI Model Inference API Access) and **AML.T0010** (AI Supply Chain Compromise) cover the core theft and aggregation. **AML.T0103** (Deploy AI Agent) and **AML.T0098** (AI Agent Tool Credential Harvesting) describe the autonomous execution layer. **AML.T0057** (LLM Data Leakage) captures the inadvertent control-plane exposure via the honeypot. On the OWASP side, **LLM05** (Supply Chain Vulnerabilities), **LLM08** (Excessive Agency), and **LLM10** (Model Theft) are the most directly applicable categories.

## Impact Assessment

LLM resale platform operators face direct financial harm through API quota exhaustion and fraudulent account farming. Downstream consumers of aggregated inference may unknowingly route traffic through attacker-controlled infrastructure. The self-expanding nature of the supply chain means scale can grow without proportional attacker effort, and the pattern is likely to be replicated as inference costs remain a meaningful operational expense.

## Mitigation & Recommendations

- **Harden gateway authentication:** Disable open registration with free balances; enforce identity verification and spending caps.
- **Protect internal endpoints:** Restrict `/api/auth-files` and similar administrative endpoints behind authenticated access controls.
- **Monitor for harvesting signals:** Implement anomaly detection on key validation patterns, rapid factorial-style probe requests, and bulk model catalog enumeration.
- **Deploy inference honeypots:** Emulated OpenAI-compatible endpoints can surface attacker playbooks, tooling, and operational infrastructure at low cost.
- **Audit agent context boundaries:** Ensure autonomous coding agents do not embed sensitive credentials or playbook data in model request context.

## References

- [SANS ISC Diary — The Self-Expanding Stolen Inference Supply Chain](https://isc.sans.edu/diary/rss/33332)
