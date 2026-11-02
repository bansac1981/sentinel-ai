---
title: "VOLTA Infostealer Uses Claude and Gemini to Triage Victims"
date: 2026-11-02T13:45:31+00:00
draft: true
slug: "volta-infostealer-uses-claude-and-gemini-to-triage-victims"

# ── Content metadata ──
summary: "The VOLTA-AUTODOXER infostealer represents a significant escalation in malware sophistication, weaponising commercial LLMs via OpenRouter to automatically prioritise stolen victim data by financial value. The malware implements a resilient multi-model fallback chain across Claude, Kimi, and Gemini, actively circumventing individual model refusals to generate monetisation-ranked dossiers. This marks a qualitative shift in infostealer design \u2014 transforming raw credential dumps into analyst-grade intelligence reports with minimal human operator effort."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/new-volta-infostealer-uses-claude.html"
source_title: "New VOLTA Infostealer Uses Claude, Gemini, and Kimi AI to Rank Victims by Financial Value"
source_date: 2026-11-02T05:51:07+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1651472804043-5ae936d08d0f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxzZWFyY2glMjBleHBsb3JlJTIwZGlzY292ZXJ5JTIwYWJzdHJhY3R8ZW58MHwwfHx8MTc5MzYyNzEzMXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0054 - LLM Jailbreak", "AML.T0065 - LLM Prompt Crafting", "AML.T0057 - LLM Data Leakage", "AML.T0040 - AI Model Inference API Access", "AML.T0063 - Discover AI Model Outputs", "AML.T0113 - Steal Web Session Cookie"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "VOLTA malware feeds stolen victim data into Claude, Gemini, and Kimi to generate monetisation-ranked dossiers automatically."
tldr_who_at_risk: "Windows users with high-value financial accounts, crypto wallets, or corporate credentials are primary targets due to VOLTA's financial scoring mechanism."
tldr_actions: ["Audit and restrict outbound API calls to OpenRouter and similar LLM gateway services at the network perimeter", "Deploy endpoint detection rules targeting VOLTA's characteristic multi-stage Telegram exfiltration pattern", "Enforce hardware security keys and phishing-resistant MFA on Gmail, Slack, and financial accounts to limit post-compromise enrichment"]

# ── Taxonomies ──
categories: ["LLM Security", "Jailbreaks", "Agentic AI", "Industry News"]
tags: ["infostealer", "volta", "llm-abuse", "claude", "gemini", "kimi", "openrouter", "credential-theft", "multi-model", "data-exfiltration", "telegram", "financial-targeting", "jailbreak-bypass", "windows-malware", "ai-enabled-attack"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-02T13:45:31+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/new-volta-infostealer-uses-claude.html"
pipeline_version: "2.1.0"
---

## Overview

Cisco Talos researchers have disclosed **VOLTA-AUTODOXER (VOLTA)**, a Windows infostealer that integrates commercial large language models directly into its post-exploitation pipeline. Unlike conventional stealers that dump raw credentials for manual operator review, VOLTA automatically constructs a structured evidence bundle about each victim and submits it to AI models via the OpenRouter API gateway to produce a prioritised, citation-backed financial dossier. This represents a meaningful escalation: the operator receives analyst-grade intelligence rather than a raw log file.

## Technical Analysis

VOLTA harvests a broad credential surface including browser passwords and cookies (Chromium-based), Outlook and Slack data, payment card details, cryptocurrency seed phrases, Discord/Steam/Roblox session tokens, Microsoft OAuth tokens, SSH and cloud provider keys, Wi-Fi profiles, and screenshots.

A distinctive enrichment step uses stolen Gmail session access to query the victim's inbox for delivery receipts from Amazon, DoorDash, Uber Eats, Grubhub, Walmart, and PayPal — corroborating home address data through purchase history rather than relying solely on device metadata.

The collected data is serialised into a structured bundle and submitted to OpenRouter with a **240-word system prompt** that instructs the model to act as a "forensic intelligence analyst." The prompt explicitly prohibits the model from supplementing findings with training knowledge — all facts must derive from the bundle alone, a technique that reduces hallucination risk and keeps the dossier legally plausible for fraud operators.

The required output includes:
- **WHAT THEY'RE WORTH** — valuables ranked low/medium/high by monetisation potential
- **THEIR OPSEC** — assessment of the victim's security posture and password hygiene

**Multi-model fallback chain:** Requests default to Anthropic Claude Opus 4.6; if the response contains refusal phrases such as "I can't" or "I'm not able," the malware automatically retries with Moonshot AI's Kimi K2, then Google Gemini 2.5 Flash. This resilient chaining is a deliberate jailbreak-bypass strategy that treats model safety guardrails as a routing problem.

Exfiltration occurs in three Telegram bursts: immediately after initial credential harvest; after the LLM analysis completes; and after the live Gmail enrichment step. The malware also supports a six-slot build-time template, suggesting a builder/affiliate model.

## Framework Mapping

| Technique | Rationale |
|---|---|
| AML.T0047 – AI-Enabled Product or Service | VOLTA uses commercial LLM APIs as a core capability |
| AML.T0054 – LLM Jailbreak | Multi-model fallback explicitly routes around refusals |
| AML.T0065 – LLM Prompt Crafting | 240-word system prompt engineered for forensic analyst persona |
| AML.T0057 – LLM Data Leakage | Victim PII is submitted to third-party AI infrastructure |
| LLM08 – Excessive Agency | LLM is granted autonomous triage and scoring authority over stolen data |
| LLM06 – Sensitive Information Disclosure | PII, financial, and credential data traverses external LLM APIs |

## Impact Assessment

The primary risk is **operator efficiency amplification**: VOLTA reduces the manual effort required to monetise stolen credentials, lowering the skill floor for financially motivated attackers. Victims with high-value crypto holdings, corporate Slack access, or active payment cards are systematically prioritised, accelerating downstream fraud. Secondary risk exists in the **data sovereignty dimension** — victim PII is transmitted to commercial AI infrastructure outside the victim's jurisdiction.

## Mitigation & Recommendations

1. **Block or alert on outbound connections to `openrouter.ai`** and similar LLM API gateways at the firewall or proxy layer — legitimate enterprise workloads rarely require this.
2. **Deploy behavioural EDR rules** for VOLTA's three-stage Telegram exfiltration pattern and mass credential file access.
3. **Enable Gmail advanced phishing protections** and audit active OAuth sessions regularly to limit post-compromise inbox enrichment.
4. **Enforce phishing-resistant MFA** (FIDO2/passkeys) on high-value accounts; session token theft is VOLTA's primary browser attack vector.
5. **Monitor for OpenRouter API key usage** in process memory or environment variables on endpoints.

## References

- [The Hacker News — New VOLTA Infostealer Uses Claude, Gemini, and Kimi AI to Rank Victims by Financial Value](https://thehackernews.com/2026/11/new-volta-infostealer-uses-claude.html)
