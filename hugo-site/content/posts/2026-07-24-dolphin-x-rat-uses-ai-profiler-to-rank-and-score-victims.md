---
title: "Dolphin X RAT Uses AI Profiler to Rank and Score Victims"
date: "2026-07-24T07:03:26+00:00"
draft: false
slug: "dolphin-x-rat-uses-ai-profiler-to-rank-and-score-victims"

# ── Content metadata ──
summary: "The Dolphin X remote access trojan integrates an AI-powered profiling system that automatically scores and ranks infected machines, enabling attackers to efficiently triage thousands of victims and prioritise high-value targets such as corporate networks and cryptocurrency holders. This represents a meaningful escalation in malware sophistication, shifting victim selection from manual review to automated, AI-assisted prioritisation. Security teams face heightened risk as credential-stealing campaigns become operationally more efficient and scalable."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/new-dolphin-x-malware-uses-ai-to-rank-high-value-targets"
source_title: "New Dolphin X malware uses AI to rank high-value targets"
source_date: 2026-07-23T21:20:34+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/6963944/pexels-photo-6963944.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Dolphin X RAT uses an embedded AI profiler to automatically score and rank infected victims by value."
tldr_who_at_risk: "Corporate employees, cryptocurrency holders, and cloud environment users are most at risk as the AI profiler specifically targets access to these high-value account types."
tldr_actions: ["Deploy endpoint detection capable of identifying RAT agent network traffic patterns and operator panel communication", "Monitor for unusual credential access patterns across 300+ application categories flagged by Dolphin X", "Enforce MFA on all corporate, cloud, and cryptocurrency accounts to reduce value of stolen credentials"]

# ── Taxonomies ──
categories: ["Agentic AI", "Industry News", "Research"]
tags: ["dolphin-x", "remote-access-trojan", "ai-profiler", "credential-theft", "malware", "victim-scoring", "cybercrime", "varonis", "threat-intelligence", "ai-enabled-attack"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-07-24T05:38:26+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/new-dolphin-x-malware-uses-ai-to-rank-high-value-targets"
pipeline_version: "2.1.0"
---

## Overview

A newly advertised remote access trojan dubbed **Dolphin X** has drawn attention from threat researchers for incorporating an AI-powered victim profiling system into its operator panel. Analysed by Varonis Threat Labs researcher Daniel Kelley, the malware was spotted being marketed on cybercrime forums by a vendor using the alias *Kontraktnik*. The tool presents itself as an all-in-one RAT with 329 advertised features across ten categories, but its most operationally significant capability is the **AI Profiler** — a scoring engine that automatically ranks infected machines by their potential value to attackers.

## Technical Analysis

The Dolphin X operator panel includes a dedicated surveillance tab housing the AI Profiler module. According to Varonis, the feature ingests data collected from compromised hosts — including application usage patterns, installed software inventories, browser domain histories, and behavioural signals — and synthesises this into a per-victim **risk score and categorical tags**.

Attackers receive daily summary reports listing ranked victim profiles, enabling them to triage large infection pools without manual review. The profiler is described by the vendor as an *"AI behavioral profiler with app usage tracking, risk score, and daily summary."* Targets associated with access to corporate networks, cloud environments, cryptocurrency wallets, or production systems are surfaced as high-priority.

Varonis examined the malware builder and network traffic within an isolated lab environment; a live Dolphin X agent was not executed on an infected host. The credential-stealing component claims coverage of more than 300 applications, compounding the volume problem the AI Profiler is designed to solve.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0047 — ML-Enabled Product or Service:** The AI Profiler is embedded directly into criminal infrastructure as a force-multiplier, automating attacker decision-making at scale.
- **AML.T0040 — ML Model Inference API Access:** The profiler processes victim telemetry through an inference pipeline to produce actionable scores, representing operational ML deployment within malware.

**OWASP LLM Top 10:**
- **LLM08 — Excessive Agency:** The AI system autonomously prioritises human targets for further exploitation without manual operator review, delegating consequential decisions to the model.
- **LLM06 — Sensitive Information Disclosure:** Victim behavioural data, application usage, and access credentials are processed and surfaced to threat actors through the AI summary system.

## Impact Assessment

The primary impact of AI-assisted victim triage is **operational efficiency for attackers**. Credential-stealing campaigns typically generate far more data than operators can manually review; the AI Profiler effectively removes this bottleneck. Organisations with employees in finance, cloud infrastructure, or cryptocurrency will likely be surfaced more frequently by such scoring systems. The feature also lowers the expertise threshold for running large-scale RAT campaigns, potentially broadening the threat actor pool.

## Mitigation & Recommendations

- **Enforce multi-factor authentication** on all accounts, particularly those tied to corporate access, cloud platforms, and financial services, to reduce the exploitability of stolen credentials.
- **Deploy behavioural endpoint detection** capable of identifying RAT communication patterns and unusual telemetry exfiltration consistent with profiling activity.
- **Audit installed software and browser profiles** on endpoints to understand what data a profiler could extract and rank.
- **Monitor dark web and cybercrime forums** for Dolphin X infrastructure indicators released by Varonis and similar threat labs.
- **Segment high-value systems** so that compromised endpoints cannot directly reach production or cloud management environments.

## References

- [New Dolphin X malware uses AI to rank high-value targets — BleepingComputer](https://www.bleepingcomputer.com/news/security/new-dolphin-x-malware-uses-ai-to-rank-high-value-targets)
- Varonis Threat Labs analysis by Daniel Kelley (referenced in source article)
