---
title: "Frontier LLMs Now Autonomously Breach Corporate Networks in AISI Cyber Tests"
date: "2026-05-02T04:50:23+00:00"
draft: false
slug: "frontier-llms-now-autonomously-breach-corporate-networks-in-aisi-cyber-tests"

# ── Content metadata ──
summary: "The UK's AI Security Institute (AISI) found that OpenAI's GPT-5.5 matches Anthropic's Mythos Preview on cybersecurity benchmarks, including a 32-step simulated corporate network intrusion. Both models successfully completed the 'The Last Ones' data-extraction simulation \u2014 a first for any AI system \u2014 suggesting autonomous offensive cyber capability is a general frontier-model property, not a one-vendor breakthrough. The findings raise urgent questions about responsible release practices and the pace at which LLMs can independently execute multi-stage attacks."
source: "Ars Technica Security"
source_url: "https://arstechnica.com/ai/2026/05/amid-mythos-hyped-cybersecurity-prowess-researchers-find-gpt-5-5-is-just-as-good/"
source_title: "GPT-5.5 matches heavily hyped Mythos Preview in new cybersecurity tests"
source_date: 2026-05-01T15:32:27+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://plus.unsplash.com/premium_photo-1726079247110-5e593660c7b2?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "GPT-5.5 and Mythos Preview both autonomously completed a 32-step simulated corporate network breach \u2014 an AI first."
tldr_who_at_risk: "Enterprise security teams are most exposed, as multiple frontier LLMs can now autonomously execute multi-stage network intrusion and data extraction tasks without human assistance."
tldr_actions: ["Audit AI API access controls and enforce strict identity verification before granting frontier model access to any network-adjacent tooling", "Treat autonomous LLM agent deployments as high-risk attack surfaces and apply least-privilege principles to all agentic pipelines", "Monitor AISI and NIST AI RMF guidance for updated thresholds triggering restricted model deployment obligations"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Research", "Industry News", "Regulatory"]
tags: ["autonomous-attack", "capture-the-flag", "aisi", "gpt-5-5", "mythos", "frontier-models", "cyber-evaluation", "network-intrusion", "offensive-ai", "long-horizon-autonomy"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-02T04:07:49+00:00"
feed_source: "arstechnica"
original_url: "https://arstechnica.com/ai/2026/05/amid-mythos-hyped-cybersecurity-prowess-researchers-find-gpt-5-5-is-just-as-good/"
pipeline_version: "1.0.0"
---

## Overview

New evaluation results from the UK's AI Security Institute (AISI) reveal that OpenAI's GPT-5.5 matches Anthropic's Mythos Preview across a comprehensive suite of cybersecurity benchmarks — including the first-ever AI success on a simulated 32-step corporate network intrusion. The finding is significant not because any single model has achieved a novel capability in isolation, but because it demonstrates that dangerous autonomous offensive cyber ability is now a **general property of frontier LLMs**, not an anomaly confined to one vendor's system.

The results directly challenge Anthropic's framing around Mythos Preview's restricted release, which positioned the model as uniquely dangerous and warranting controlled distribution to 'critical industry partners' only.

## Technical Analysis

AISI evaluated both models against 95 Capture the Flag (CTF) challenges spanning reverse engineering, web exploitation, and cryptography. On 'Expert'-tier tasks:

- **GPT-5.5**: 71.4% pass rate
- **Mythos Preview**: 68.6% pass rate (within margin of error)

In a representative task, GPT-5.5 autonomously built a disassembler to decode a compiled Rust binary — completing the challenge in **10 minutes 22 seconds** at a cost of **$1.73** in API calls, with zero human intervention.

More critically, both models made successful attempts on **'The Last Ones' (TLO)**, AISI's simulation of a 32-step data extraction attack on a corporate network:

- GPT-5.5: **3/10 attempts successful**
- Mythos Preview: **2/10 attempts successful**
- All prior models tested: **0/10**

Neither model succeeded on 'Cooling Tower', a harder simulation targeting industrial control system disruption — indicating a current ceiling on autonomous OT/ICS attack capability.

AISI attributes the capability leap to broader improvements in **long-horizon autonomy, reasoning, and coding** rather than any cybersecurity-specific training.

## Framework Mapping

**AML.T0047 (ML-Enabled Product or Service)**: Both models are being used as autonomous agents capable of executing multi-step offensive operations via API access — the precise threat vector this technique describes.

**AML.T0040 (ML Model Inference API Access)**: The cost and speed profile ($1.73, ~10 minutes) confirms that API-accessible frontier models present a low-barrier offensive capability.

**LLM08 (Excessive Agency)**: The TLO results are a textbook case — an LLM autonomously executing a 32-step intrusion chain represents agency far exceeding safe operational boundaries without human-in-the-loop controls.

## Impact Assessment

The primary risk is **democratisation of multi-stage network intrusion**. Previously, executing a 32-step data exfiltration chain required significant human expertise. Frontier LLMs now compress that requirement to API access and a prompt. The $1.73 cost-per-task figure underscores the economic accessibility of this threat vector.

Organisations relying on complexity as a defence layer — assuming attackers lack the skill to chain exploitation steps — face meaningful erosion of that assumption. Security operations centres (SOCs) and red teams should treat autonomous LLM agents as a plausible adversarial tool in threat modelling exercises immediately.

## Mitigation & Recommendations

- **Restrict agentic model access**: Do not expose frontier LLMs to tooling with network, file system, or credential access without strict sandboxing and human approval gates.
- **Enforce identity verification**: Follow OpenAI's Trusted Access for Cyber model — require verified identity before granting API access to frontier models for any security-adjacent use case.
- **Update threat models**: Incorporate autonomous LLM-driven intrusion as a realistic threat actor capability in enterprise risk registers and red team exercises.
- **Track regulatory thresholds**: AISI's benchmarks are increasingly informing policy; organisations in critical infrastructure should monitor for mandatory reporting or access restriction obligations tied to these scores.

## References

- [Ars Technica — GPT-5.5 matches heavily hyped Mythos Preview in new cybersecurity tests](https://arstechnica.com/ai/2026/05/amid-mythos-hyped-cybersecurity-prowess-researchers-find-gpt-5-5-is-just-as-good/)
