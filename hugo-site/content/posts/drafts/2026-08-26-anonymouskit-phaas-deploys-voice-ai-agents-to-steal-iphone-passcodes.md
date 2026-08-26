---
title: "AnonyMousKIT PhaaS Deploys Voice AI Agents to Steal iPhone Passcodes"
date: 2026-08-26T07:13:15+00:00
draft: true
slug: "anonymouskit-phaas-deploys-voice-ai-agents-to-steal-iphone-passcodes"

# ── Content metadata ──
summary: "AnonyMousKIT is a phishing-as-a-service platform that deploys voice AI agents to social-engineer stolen iPhone owners into surrendering their device passcodes and Apple credentials, enabling Activation Lock bypass. The platform has been active since early 2024, operates across 506 domains with 168 reseller storefronts, and conducted at least 200 documented AI-driven vishing calls. This represents a notable escalation in PhaaS sophistication, weaponising autonomous voice AI agents for large-scale, low-cost credential harvesting at roughly $0.10 per call."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/anonymouskit-phaas-uses-voice-ai-agents-to-phish-iphone-passcodes"
source_title: "AnonyMousKIT PhaaS uses voice AI agents to phish iPhone passcodes"
source_date: 2026-08-25T20:25:26+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1614358108424-04d03647e343?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw5fHxkcm9uZSUyMGFlcmlhbCUyMGF1dG9ub21vdXMlMjBmbGlnaHR8ZW58MHwwfHx8MTc4NzcyODM5NXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0103 - Deploy AI Agent", "AML.T0088 - Generate Deepfakes", "AML.T0086 - Exfiltration via AI Agent Tool Invocation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "AnonyMousKIT PhaaS uses autonomous voice AI agents to vish stolen iPhone owners for passcodes."
tldr_who_at_risk: "iPhone owners whose devices have been stolen are directly targeted via AI-driven calls impersonating Apple support."
tldr_actions: ["Never provide your iPhone passcode, Apple ID, or 2FA codes over a phone call, email, or SMS — Apple does not request these", "Enable an alphanumeric iPhone passcode and a Recovery Key to raise the attacker cost of bypass", "Report suspicious Apple-impersonation calls or emails to reportphishing@apple.com and your local authorities"]

# ── Taxonomies ──
categories: ["Agentic AI", "Industry News", "LLM Security"]
tags: ["vishing", "voice-ai-agent", "phaas", "apple-activation-lock", "iphone-phishing", "anonymouskit", "credential-harvesting", "social-engineering", "ai-enabled-phishing", "soсradar"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-26T07:13:15+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/anonymouskit-phaas-uses-voice-ai-agents-to-phish-iphone-passcodes"
pipeline_version: "2.1.0"
---

## Overview

A phishing-as-a-service (PhaaS) operation dubbed **AnonyMousKIT** has been uncovered deploying autonomous voice AI agents to contact owners of stolen iPhones and trick them into surrendering device passcodes, Apple ID credentials, and two-factor authentication codes. Active since early 2024, the platform enables criminal resellers to bypass Apple's Activation Lock — a feature designed to render stolen devices unusable — by socially engineering the original owner rather than attacking Apple's infrastructure directly.

Threat intelligence firm SOCRadar exposed the operation after exploiting the platform operator's use of bare relative paths, gaining visibility into infrastructure, call records, and interaction transcripts.

## Technical Analysis

AnonyMousKIT operates as a structured criminal ecosystem with four principal capabilities:

1. **Device intelligence gathering** — the platform extracts owner contact details from the iPhone's Lost Mode feature (name, phone, email) to personalise attacks.
2. **Multi-channel phishing** — victims are contacted via email, SMS, WhatsApp, or phone call, with messages impersonating Apple and citing correct device model and IMEI to establish legitimacy.
3. **Voice AI vishing** — an AI voice agent operating under five distinct personas conducts live phone calls. SOCRadar recovered 200 call records and 55 interaction transcripts spanning August 2025 to May 2026, with 90% of calls targeting victims in Brazil. Cost per attempt: approximately **$0.10**.
4. **Credential capture** — victims directed to fake Find My / Apple pages are prompted to submit their device passcode, Apple Account password, and 2FA code.

The recovered credentials are then used to disable Activation Lock, dramatically increasing the resale value of stolen devices and enabling access to iCloud backups and Keychain secrets. The platform supports **506 domains** and **168 storefront reseller brands**.

The use of AI voice agents is significant: they eliminate the need for human operators on individual calls, reduce per-attempt cost to near-zero, and allow the platform to scale vishing campaigns that were previously labour-intensive.

## Framework Mapping

- **AML.T0047 (AI-Enabled Product or Service)** — AnonyMousKIT is itself a criminal AI-enabled service offering automated social engineering at scale.
- **AML.T0103 (Deploy AI Agent)** — Voice AI agents are autonomously deployed to conduct multi-turn deceptive conversations with victims.
- **AML.T0088 (Generate Deepfakes / Synthetic Personas)** — The agent operates under five distinct synthetic personas to avoid victim pattern recognition.
- **LLM08 (Excessive Agency)** — The AI agent acts with full autonomy in a sensitive, deceptive context without human oversight per interaction, representing an uncontrolled agentic deployment risk.

## Impact Assessment

The primary victims are iPhone owners whose devices have been stolen. Secondary impact extends to the integrity of Apple's Activation Lock as a theft deterrent. The $0.10-per-call economics make large-scale campaigns trivially affordable, and the platform's reseller model means any low-sophistication criminal can access these capabilities. The Brazil-centric targeting (90% of calls) suggests a geographically concentrated criminal supply chain for stolen Apple hardware.

## Mitigation & Recommendations

- **Never disclose passcodes or 2FA codes via any inbound channel** — Apple does not request these by phone, SMS, or email.
- **Enable an alphanumeric passcode** — longer passcodes increase resistance even if partial information is leaked.
- **Set a Recovery Key** — this makes it significantly harder for attackers to access your Apple Account even with stolen credentials.
- **Verify device loss reports independently** — if you receive a message claiming your device has been found, navigate directly to apple.com/findmy rather than clicking any link.
- **Report suspicious contacts** to reportphishing@apple.com and local law enforcement.

## References

- [BleepingComputer: AnonyMousKIT PhaaS uses voice AI agents to phish iPhone passcodes](https://www.bleepingcomputer.com/news/security/anonymouskit-phaas-uses-voice-ai-agents-to-phish-iphone-passcodes)
