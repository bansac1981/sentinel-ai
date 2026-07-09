---
title: "Gemini Prompt Injection Powers Mass Smishing Campaign"
date: "2026-06-13T06:49:38+00:00"
draft: false 
slug: "gemini-ai-weaponised-by-chinese-phaas-network-in-mass-smishing-campaign"

# ── Content metadata ──
summary: "Google has filed suit against a Chinese cybercrime network operating the Outsider phishing-as-a-service kit, which exploited Gemini AI to generate fraudulent phishing pages and power large-scale SMS phishing attacks against Americans. The network used carefully framed prompts \u2014 disguised as benign programming requests \u2014 to bypass AI safety controls and produce functional credential-harvesting websites. The case illustrates the growing industrialisation of AI-assisted phishing infrastructure, with over 1.59 million malicious URLs and 100,000 victims attributed to the operation."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/06/google-sues-chinese-smishing-network.html"
source_title: "Google Sues Chinese Smishing Network Accused of Using Gemini AI in Phishing"
source_date: 2026-06-12T18:59:32+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1674027444484-cf52149ea050?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw3fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc4MTMxODUxM3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Chinese PhaaS network used Gemini AI to auto-generate phishing pages, victimising over 100,000 Americans."
tldr_who_at_risk: "US consumers are most exposed, particularly those receiving SMS messages impersonating banks, brokerages, and mobile carriers."
tldr_actions: ["Block or flag SMS links to newly registered or unrecognised domains at the carrier and endpoint level", "Audit LLM deployment guardrails to detect prompt patterns disguised as innocuous programming requests", "Educate users to avoid clicking unsolicited SMS links regardless of apparent brand legitimacy"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Jailbreaks", "Industry News"]
tags: ["smishing", "phishing-as-a-service", "gemini-ai", "prompt-abuse", "chinese-threat-actors", "social-engineering", "credential-harvesting", "telegram", "google-lawsuit", "llm-misuse"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-06-13T02:42:27+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/06/google-sues-chinese-smishing-network.html"
pipeline_version: "1.0.0"
---

## Overview

Google has filed a federal lawsuit in Manhattan against a Chinese cybercrime enterprise operating a phishing-as-a-service (PhaaS) platform called **Outsider**. The network stands accused of weaponising Google's own Gemini AI model to generate fraudulent phishing websites at scale, fuelling a mass smishing (SMS phishing) campaign that targeted American consumers. Between November 2025 and April 2026, the operation produced over **1.59 million malicious URLs** across **9,000 fake websites**, with an estimated **100,000 victims** and millions of dollars in financial losses.

The lawsuit marks a significant escalation in AI-enabled cybercrime: a commercial threat actor industrialising LLM capabilities within an affordable, subscription-based phishing kit sold for as little as **$88 per week** via Telegram.

---

## Technical Analysis

Outsider functions as a turnkey phishing operation. Key capabilities include:

- **290+ pre-built brand impersonation templates** mimicking banks, brokerages, and mobile carriers
- **Real-time keystroke logging** on harvested credential pages
- **Campaign performance dashboards** for operators
- A **Telegram self-service bot** (`@OutsiderCodeBot`) for licence purchase and kit distribution

The AI abuse vector is particularly notable. Operators were provided step-by-step instructions on how to prompt Gemini and other LLMs to generate HTML/JavaScript code for "shell websites." Prompts were deliberately framed as benign programming assistance — for example, requesting code for a "gift redemption page" — to avoid triggering safety filters. The generated code was then pasted directly into the Outsider kit and transformed into functional credential-harvesting sites.

This represents a **prompt obfuscation technique**: wrapping malicious intent inside superficially legitimate development tasks to circumvent LLM content policies.

```
// Example prompt structure (paraphrased from complaint)
"Write HTML for a gift redemption page with a form 
collecting name, card number, and billing address."
```

The resulting output, innocuous in isolation, becomes a phishing page when branded with stolen assets from legitimate institutions.

---

## Framework Mapping

| Framework | ID | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0051 | Prompts crafted to extract harmful outputs from Gemini via indirect framing |
| MITRE ATLAS | AML.T0054 | Safety controls bypassed through context manipulation |
| MITRE ATLAS | AML.T0047 | LLM used as a component within a criminal product pipeline |
| OWASP | LLM01 | Prompt injection via disguised programming requests |
| OWASP | LLM02 | Insecure output (generated HTML) consumed directly in attack infrastructure |
| OWASP | LLM08 | AI model granted effective agency in producing attack-ready artefacts |

---

## Impact Assessment

The scale of this operation is significant. Over a two-week window in May–June 2026, **2.5 million messages** were sent to Android users, with 55,000 flagged as spam. The low barrier to entry — $88/week, no technical expertise required — dramatically lowers the threshold for criminal participation. Google has partnered with AT&T, T-Mobile, and Verizon to block associated messages, and is seeking infrastructure takedown through litigation.

---

## Mitigation & Recommendations

1. **LLM providers** should implement intent-pattern detection for prompts requesting credential-form HTML, even when framed as generic development tasks.
2. **Enterprises** deploying LLM APIs should log and audit all code-generation outputs for phishing-indicative patterns (form fields collecting financial data).
3. **Carriers and MNOs** should expand SMS URL scanning to include newly registered domains and those matching known PhaaS infrastructure fingerprints.
4. **End users** should be trained to treat all unsolicited SMS links as suspect, regardless of brand spoofing quality.
5. **Security teams** should monitor Telegram for PhaaS kit advertisements and associated bot handles as an early warning signal.

---

## References

- [Google Sues Chinese Smishing Network Accused of Using Gemini AI in Phishing — The Hacker News](https://thehackernews.com/2026/06/google-sues-chinese-smishing-network.html)
