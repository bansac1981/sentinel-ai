---
title: "AI Chatbots Poisoned via Web Seeding in Disinformation Campaign"
date: "2026-09-24T12:24:27+00:00"
draft: false 
slug: "ai-chatbots-poisoned-via-web-seeding-in-disinformation-campaign"

# ── Content metadata ──
summary: "Threat actors are actively manipulating AI chatbots including ChatGPT, Gemini, and Google AI Overviews by seeding the web with malicious links and optimised content designed to corrupt AI-generated answers. The campaign combines disinformation and phishing objectives, exploiting how large language models and retrieval-augmented systems ingest and surface web content. This represents a scalable, infrastructure-level attack on public trust in AI-assisted information retrieval."
source: "Dark Reading"
source_url: "https://www.darkreading.com/threat-intelligence/attackers-manipulate-ai-chatbots-mass-disinformation-phishing-campaign"
source_title: "Attackers Manipulate AI Chatbots in Mass Disinformation, Phishing Campaign"
source_date: 2026-09-23T14:47:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1708807472445-d33589e6b090?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyM3x8TExNJTIwU2VjdXJpdHklMjBjeWJlcnNlY3VyaXR5JTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzkwMjE0Nzc0fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0070 - RAG Poisoning", "AML.T0071 - False RAG Entry Injection", "AML.T0066 - Retrieval Content Crafting", "AML.T0059 - Erode Dataset Integrity", "AML.T0020 - Poison Training Data", "AML.T0043 - Craft Adversarial Data", "AML.T0067 - LLM Trusted Output Components Manipulation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM03 - Training Data Poisoning", "LLM02 - Insecure Output Handling", "LLM09 - Overreliance", "LLM01 - Prompt Injection"]

# ── TL;DR ──
tldr_what: "Attackers are poisoning ChatGPT, Gemini, and Google AI Overviews with SEO-optimised malicious web content."
tldr_who_at_risk: "General users relying on AI chatbots for information are most at risk of receiving disinformation or being directed to phishing infrastructure."
tldr_actions: ["Cross-reference AI-generated answers against authoritative primary sources before acting on them", "Deploy web filtering and threat intelligence feeds to block known malicious domains cited by AI tools", "Educate users on the risks of AI overreliance and the possibility of AI-surfaced phishing links"]

# ── Taxonomies ──
categories: ["LLM Security", "Data Poisoning", "Adversarial ML", "Industry News"]
tags: ["rag-poisoning", "web-content-poisoning", "disinformation", "phishing", "chatgpt", "gemini", "google-ai-overviews", "llm-manipulation", "malicious-seo", "ai-chatbots"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-24T01:52:54+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/threat-intelligence/attackers-manipulate-ai-chatbots-mass-disinformation-phishing-campaign"
pipeline_version: "2.1.0"
---

## Overview

Threat actors are conducting a mass disinformation and phishing campaign by deliberately poisoning the web content ingested by major AI chatbots — including ChatGPT, Gemini, and Google AI Overviews. By seeding the internet with malicious links and optimised content, attackers are manipulating AI-generated answers to serve fabricated information or direct users toward phishing infrastructure. The campaign illustrates a systemic vulnerability in how retrieval-augmented and web-connected AI systems trust external content.

## Technical Analysis

The attack methodology exploits the retrieval pipeline underpinning modern AI assistants. When AI systems like Google AI Overviews or ChatGPT's browsing-enabled mode query the web to supplement their responses, they surface content ranked highly by search-engine-like signals. Attackers are abusing this by:

1. **Web seeding**: Publishing large volumes of attacker-controlled pages containing targeted disinformation or phishing lures.
2. **Content optimisation**: Applying SEO-style techniques to boost the visibility and apparent authority of malicious pages, increasing the likelihood that AI retrieval systems index and surface them.
3. **Link manipulation**: Embedding malicious URLs within content that AI systems may reproduce verbatim in their responses, directing users to phishing sites.

This is a practical instantiation of RAG Poisoning — an attack class where adversaries corrupt the external knowledge sources that retrieval-augmented generation systems depend upon. Unlike traditional prompt injection, this attack requires no access to the model itself; the attack surface is the open web.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0070 (RAG Poisoning)** and **AML.T0071 (False RAG Entry Injection)** are the primary techniques — attackers are injecting false content into the retrieval corpus.
- **AML.T0066 (Retrieval Content Crafting)** describes the SEO optimisation used to elevate malicious content.
- **AML.T0067 (LLM Trusted Output Components Manipulation)** applies where AI outputs reproduce attacker-controlled links as trusted recommendations.

**OWASP LLM Top 10:**
- **LLM03 (Training Data Poisoning)** covers the web-content poisoning vector.
- **LLM09 (Overreliance)** is the user-side risk — victims trusting AI-generated answers without verification.
- **LLM02 (Insecure Output Handling)** applies where malicious URLs are rendered as actionable links.

## Impact Assessment

The campaign affects any user querying ChatGPT, Gemini, or Google AI Overviews on topics targeted by attackers. The scale of potential harm is significant: AI chatbots are increasingly used as primary information sources, meaning a successfully poisoned answer can reach millions of users rapidly. Phishing links surfaced within AI-generated responses carry elevated credibility because users associate AI output with authority, reducing scepticism. Organisations relying on AI-assisted research workflows face elevated risk of staff being exposed to disinformation or credential-harvesting pages.

## Mitigation & Recommendations

- **For end users**: Treat AI-generated answers referencing external URLs with the same scrutiny as unsolicited email links. Verify claims via primary sources.
- **For security teams**: Monitor for AI-tool-sourced URLs in browser telemetry and flag domains associated with known malicious infrastructure.
- **For AI providers**: Strengthen retrieval pipeline integrity checks, implement domain reputation scoring for cited sources, and increase transparency around which sources inform AI answers.
- **For enterprises**: Restrict use of web-browsing AI features in sensitive research workflows until provider-side mitigations are confirmed.

## References

- [Attackers Manipulate AI Chatbots in Mass Disinformation, Phishing Campaign — Dark Reading](https://www.darkreading.com/threat-intelligence/attackers-manipulate-ai-chatbots-mass-disinformation-phishing-campaign)
