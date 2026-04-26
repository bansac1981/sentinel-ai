---
title: "GTIG AI Threat Tracker: Distillation, Experimentation, and (Continued) Integration of AI for Adversarial Use"
date: "2026-04-26T12:09:12+00:00"
draft: false
slug: "gtig-ai-threat-tracker-distillation-experimentation-and-continued-integration-of"

# ── Content metadata ──
summary: "Google Threat Intelligence Group's Q4 2025 AI Threat Tracker documents a meaningful escalation in adversarial AI misuse, including a surge in model extraction (distillation) attacks, nation-state operationalisation of LLMs for phishing and reconnaissance, and the emergence of AI-integrated malware families such as HONESTCUE that leverage Gemini's API. While no breakthrough capabilities have been observed from APT actors, the integration of agentic AI for tooling development signals a maturing threat landscape. Defenders should prioritise monitoring for model extraction activity, API abuse, and AI-augmented social engineering campaigns."
source: "Mandiant Blog"
source_url: "https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use/"
source_date: 2026-02-12T14:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/2882554/pexels-photo-2882554.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - ML Model Inference API Access", "AML.T0044 - Full ML Model Access", "AML.T0047 - ML-Enabled Product or Service", "AML.T0051 - LLM Prompt Injection", "AML.T0031 - Erode ML Model Integrity", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM10 - Model Theft", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Nation-states and cybercriminals are actively distilling proprietary LLMs and integrating AI into malware and phishing operations."
tldr_who_at_risk: "AI model providers and enterprises are most exposed \u2014 model IP is being stolen via distillation attacks while their staff face increasingly convincing AI-generated phishing."
tldr_actions: ["Implement rate-limiting and anomaly detection on model inference APIs to detect distillation attempts", "Train security teams to recognise AI-augmented spear-phishing lures with unusually polished language and contextual accuracy", "Monitor for unauthorised use of generative AI APIs (e.g., Gemini, OpenAI) within malware callout patterns and network telemetry"]

# ── Taxonomies ──
categories: ["Model Theft", "Agentic AI", "LLM Security", "Adversarial ML", "Research", "Industry News"]
tags: ["model-extraction", "distillation-attack", "nation-state", "dprk", "iran", "prc", "russia", "llm-abuse", "agentic-ai", "malware", "honestcue", "gemini-api", "phishing", "reconnaissance", "apt", "gtig", "google-deepmind", "ip-theft", "social-engineering"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-26T10:21:06+00:00"
feed_source: "mandiant"
original_url: "https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use/"
pipeline_version: "1.0.0"
---

## Overview

Google Threat Intelligence Group (GTIG) and Google DeepMind's Q4 2025 AI Threat Tracker documents a clear escalation in the adversarial use of artificial intelligence. Three primary trends dominate the findings: a surge in model extraction or "distillation" attacks targeting proprietary AI systems, the deeper integration of LLMs into nation-state offensive operations, and the emergence of malware families — notably HONESTCUE — that actively call generative AI APIs to generate malicious code at runtime. While GTIG stops short of declaring a fundamental shift in the threat landscape, the report marks a qualitative step-change in how sophisticated actors operationalise AI.

## Technical Analysis

**Model Extraction (Distillation Attacks):** Distillation attacks involve querying a target model repeatedly via its inference API to generate input-output pairs, which are then used to train a surrogate model that approximates the original's behaviour. Google DeepMind and GTIG observed a significant increase in such activity from private sector entities and researchers attempting to clone proprietary model logic — a clear violation of terms of service and a form of intellectual property theft. Google states it has detected, disrupted, and mitigated these extraction campaigns.

**Nation-State LLM Integration:** Actors attributed to DPRK, Iran, PRC, and Russia were observed using LLMs to accelerate reconnaissance, craft highly contextualised phishing lures, and conduct technical research. These use cases represent productivity amplification rather than novel capabilities — LLMs reducing the time and skill required to produce credible social engineering content.

**AI-Integrated Malware — HONESTCUE:** Perhaps the most technically notable finding is the HONESTCUE malware family, which experiments with calling Gemini's API to dynamically generate code enabling file download functionality. This marks an early but significant indicator of malware leveraging live LLM inference as part of its execution chain, rather than static AI-generated code embedded at compile time. Agentic AI patterns are beginning to appear in adversarial tooling development workflows.

## Framework Mapping

- **AML.T0040 / LLM10 (Model Theft):** Distillation attacks directly map to model extraction and theft of proprietary intellectual property via inference API abuse.
- **AML.T0047 / LLM08 (Excessive Agency):** HONESTCUE's use of Gemini's API at runtime represents an agentic pattern where the malware delegates code generation to an external LLM.
- **AML.T0043:** Nation-state actors crafting nuanced phishing lures via LLM constitute adversarial data crafting for social engineering purposes.
- **LLM06 (Sensitive Information Disclosure):** Model distillation implicitly risks exposure of training data characteristics embedded in model behaviour.

## Impact Assessment

AI model providers face direct IP theft risk from organised distillation campaigns. Enterprises are increasingly exposed to AI-augmented phishing that is harder to detect through traditional indicators. The emergence of malware that calls live LLM APIs introduces a new detection gap — security tooling trained on static signatures will miss dynamic, AI-generated payload components. Nation-state actors from four major adversary blocs have now demonstrably operationalised LLMs, broadening the attack surface significantly.

## Mitigation & Recommendations

- **Rate-limit and fingerprint inference API access** to detect systematic distillation patterns (high query volume, structured input diversity).
- **Block or alert on outbound LLM API calls** from endpoints and servers where such traffic is unexpected — a key indicator of HONESTCUE-style malware.
- **Invest in AI-generated content detection** for inbound email and communications, particularly for high-value targets susceptible to spear-phishing.
- **Update threat models** to include agentic AI misuse scenarios in red team exercises and tabletop simulations.
- **Monitor for ToS violations** and enforce strict API key lifecycle management to limit misuse surface.

## References

- [GTIG AI Threat Tracker — Google Cloud Blog](https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use/)
