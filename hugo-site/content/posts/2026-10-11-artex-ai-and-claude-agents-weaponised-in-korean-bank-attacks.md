---
title: "ARTEX AI and Claude Agents Weaponised in Korean Bank Attacks"
date: "2026-10-12T10:34:54+00:00"
draft: false 
slug: "artex-ai-and-claude-agents-weaponised-in-korean-bank-attacks"

# ── Content metadata ──
summary: "A Chinese-speaking threat actor deployed the ARTEX AI agentic penetration testing suite alongside Claude Code agents and multiple LLM backends to attack major South Korean banks, exfiltrating customer data and causing system outages. The attack represents a documented real-world case of AI agents being used end-to-end in a financially motivated intrusion campaign. Exposed session histories and configuration files left in open directories enabled CrowdStrike to attribute the attack with high confidence and surface the attacker's probable identity."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/hacker-used-artex-ai-and-claude-agents-to-target-south-korean-banks"
source_title: "ARTEX AI, Claude agents used in cyberattacks on South Korean banks"
source_date: 2026-10-10T14:16:17+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1575318799743-dfb5e3c7b7c6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOHx8c2NpZW50aXN0JTIwdGhpbmtpbmclMjBhYnN0cmFjdHxlbnwwfDB8fHwxNzkxNzE4NTcxfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0103 - Deploy AI Agent", "AML.T0047 - AI-Enabled Product or Service", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0081 - Modify AI Agent Configuration", "AML.T0065 - LLM Prompt Crafting", "AML.T0057 - LLM Data Leakage", "AML.T0040 - AI Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "AI-powered pen-test suite ARTEX and Claude agents used to breach South Korean banks."
tldr_who_at_risk: "Financial institutions using internet-exposed services are most at risk as AI agent tooling dramatically lowers the skill barrier for complex intrusions."
tldr_actions: ["Audit external attack surface for services targeted by automated AI-driven recon tools", "Monitor for ARTEX configuration file patterns and Claude Code session artefacts in threat intelligence feeds", "Restrict and log all LLM API proxy traffic, especially to known reseller endpoints"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Industry News", "Supply Chain"]
tags: ["artex-ai", "claude-agents", "south-korean-banks", "agentic-penetration-testing", "deepseek", "crowdstrike", "financial-sector-breach", "chinese-threat-actor", "llm-assisted-attack", "claude-code", "open-source-weaponisation", "data-exfiltration"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-11T11:36:11+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/hacker-used-artex-ai-and-claude-agents-to-target-south-korean-banks"
pipeline_version: "2.1.0"
---

## Overview

A Chinese-speaking threat actor conducted a series of cyberattacks against major South Korean financial institutions in early October 2026, targeting Shinhan Bank, KB Kookmin Bank, and Hana Bank. The campaign exposed customer personal data and credit card information and caused operational outages at several institutions. What distinguishes this incident from conventional financial-sector intrusions is the attacker's documented reliance on AI agents — specifically the ARTEX AI penetration testing suite and Anthropic's Claude Code — as primary offensive tooling.

The South Korean government convened an emergency meeting and issued calls for immediate hardening of critical IT infrastructure. Security firm CrowdStrike confirmed ARTEX AI's involvement after discovering open directories on the attacker's infrastructure containing Claude Code session histories, ARTEX configuration files, and Claude memory artefacts.

## Technical Analysis

ARTEX AI was, until recently, an open-source agentic penetration testing framework developed in China. The threat actor's instance used **DeepSeek v4.1-flash** as the primary LLM backend, supplemented by **GLM-5.3 (Zhipu AI)** and **Grok 4.6** for additional Claude Code sessions. DeepSeek API access was routed through the LLM API proxy and reseller `xcai[.]pro`, providing a layer of infrastructure indirection.

The exposed session histories gave CrowdStrike significant visibility into the attacker's tradecraft. Notable operational security failures included:

- Leaving Claude Code session logs in publicly accessible directories
- Using the same AI toolchain to generate a personal résumé, inadvertently exposing name, contact details, date of birth, and a Telegram handle
- No pre-planned monetisation strategy — the actor queried Claude to identify Telegram data-sales channels focused on Korean data markets

CrowdStrike assessed with high confidence that the attacker is likely a 26-year-old individual who studied at the South China University of Technology and is based in Maoming, Guangdong, China. A conflicting date of birth (2007) found in the résumé introduces uncertainty, and researchers caution that the personal details cannot be used to confirm identity definitively.

Following public confirmation that ARTEX had been used in real-world attacks, the project's developer moved to close-source the codebase and halted further updates.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| AML.T0103 | Deploy AI Agent | ARTEX operated as an autonomous offensive agent |
| AML.T0086 | Exfiltration via AI Agent Tool Invocation | Agent tooling used to extract and stage stolen data |
| AML.T0065 | LLM Prompt Crafting | Attacker actively prompted Claude for operational guidance |
| AML.T0040 | AI Model Inference API Access | DeepSeek accessed via third-party API proxy |
| LLM08 | Excessive Agency | AI agents executed intrusion actions with minimal human oversight |
| LLM06 | Sensitive Information Disclosure | Session logs leaked attacker PII and victim data pathways |

## Impact Assessment

The campaign directly affected three of South Korea's largest retail banks and their customers. Personal and financial data was exfiltrated, and system outages disrupted banking services. The incident marks one of the first publicly confirmed cases of an AI agentic framework being used as a primary offensive capability in a financially motivated attack against critical financial infrastructure, raising the baseline threat model for the sector globally.

## Mitigation & Recommendations

- **Harden external attack surfaces** against automated AI-driven reconnaissance; assume agentic tools can chain vulnerabilities without human intervention between steps.
- **Threat hunt for ARTEX and Claude Code artefacts** — session history files, ARTEX config schemas, and Claude memory files — in incident response workflows.
- **Block or restrict LLM API proxy endpoints** (e.g., `xcai[.]pro`) and monitor for anomalous outbound API traffic patterns.
- **Apply the principle of least privilege** to any internal systems that interact with LLM APIs or agentic automation frameworks.
- **Review open-source AI tooling** in your environment; supply chain transitions (open-to-closed-source) do not eliminate previously distributed versions.

## References

- [BleepingComputer — ARTEX AI, Claude agents used in cyberattacks on South Korean banks](https://www.bleepingcomputer.com/news/security/hacker-used-artex-ai-and-claude-agents-to-target-south-korean-banks)
