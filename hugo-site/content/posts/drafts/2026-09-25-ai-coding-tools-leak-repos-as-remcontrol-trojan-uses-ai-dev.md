---
title: "AI Coding Tools Leak Repos as RemControl Trojan Uses AI Dev"
date: 2026-09-25T10:27:40+00:00
draft: true
slug: "ai-coding-tools-leak-repos-as-remcontrol-trojan-uses-ai-dev"

# ── Content metadata ──
summary: "Two distinct AI security concerns emerged this week: Z.ai's ZCode coding assistant was found silently exfiltrating users' local code repositories to Alibaba Cloud servers without consent, echoing a similar incident with SpaceXAI's Grok Build CLI. Separately, the RemControl Android banking trojan demonstrates AI-assisted malware development, with verbatim AI assistant responses embedded in live phishing pages served to banking victims across Western Europe, the Middle East, and Canada. Together, these incidents highlight the dual threat of AI tools as both accidental data exfiltration vectors and force multipliers for threat actors."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/threatsday-ai-search-poisoning-ai.html"
source_title: "ThreatsDay: AI Search Poisoning, AI Coding Tool Leaking Repos, One-Click Code Execution and 13 More Stories"
source_date: 2026-09-24T17:52:43+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1763487953086-ba2b51b87838?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxwYXJhc2l0ZSUyMG5hdHVyZSUyMGNsb3NlLXVwJTIwbWFjcm98ZW58MHwwfHx8MTc5MDMzMjA2MHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0010 - AI Supply Chain Compromise", "AML.T0047 - AI-Enabled Product or Service", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0065 - LLM Prompt Crafting", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Z.ai's ZCode silently uploaded user code repos; RemControl trojan uses AI-assisted phishing overlays."
tldr_who_at_risk: "Enterprise developers using AI coding assistants are at risk of unauthorised source code exfiltration; retail banking customers in Western Europe, the Middle East, and Canada are targeted by AI-crafted phishing."
tldr_actions: ["Audit all AI coding tool network traffic for unauthorised outbound data transfers to cloud storage", "Review and restrict default data-sharing settings in any AI development assistant before deployment", "Monitor banking apps for accessibility service abuse and overlay injection on managed Android devices"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News", "Agentic AI"]
tags: ["ai-coding-tools", "data-exfiltration", "zcode", "z-ai", "remcontrol", "android-banking-trojan", "ai-assisted-malware", "source-code-leakage", "supply-chain", "alibaba-cloud", "grok-build", "telegram-dead-drop", "medusa-botnet", "group-ib", "western-europe"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-09-25T10:27:40+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/threatsday-ai-search-poisoning-ai.html"
pipeline_version: "2.1.0"
---

## Overview

Two separate AI security incidents reported this week illustrate the expanding attack surface introduced by AI tooling — one as an accidental insider threat vector, the other as a force multiplier for financially motivated cybercriminals.

Chinese AI company Z.ai disabled several features of its ZCode coding assistant after researchers discovered that a default configuration was silently transmitting users' local code repositories to Alibaba Cloud servers in China without user consent. The incident follows a similar disclosure involving SpaceXAI's Grok Build CLI, which was found uploading entire Git repositories to a Google Cloud Storage bucket under its control. Neither product adequately disclosed this behaviour to enterprise customers at the point of adoption.

In a separate development, Group-IB researchers documented RemControl, a previously undocumented Android banking trojan active since July 2026. RemControl targets retail banking customers across Western Europe, the Middle East, and Canada, and bears forensic evidence of AI-assisted development — including a verbatim AI assistant response left embedded in a live phishing page served to victims.

## Technical Analysis

**ZCode Source Code Exfiltration**
ZCode's default workflow automatically generated and uploaded snapshots of local repositories as part of its AI-assisted coding features. Critically, this occurred without explicit user consent or clear disclosure. The exfiltration destination — Alibaba Cloud infrastructure in China — raises significant regulatory and intellectual property concerns for enterprises operating under data residency requirements or handling sensitive source code.

**RemControl Banking Trojan**
RemControl abuses Android's Accessibility Service to inject phishing overlays atop legitimate banking applications, stream device screens in real time, log keystrokes, and grant operators full remote control. Its command-and-control (C2) address is resolved dynamically through an encrypted Telegram dead-drop channel, enabling infrastructure rotation without recompiling the malware binary.

Notably, the malware's phishing overlays contain artifacts of AI-assisted development — including a complete, unredacted AI assistant response served verbatim to live banking victims. Russian-language code comments in multiple overlay HTML files suggest Russian-speaking developer involvement. Campaign naming conventions and affiliate tag patterns suggest a possible link to the Medusa UNKN affiliate botnet.

## Framework Mapping

- **AML.T0057 (LLM Data Leakage)** and **LLM06 (Sensitive Information Disclosure)**: ZCode's unauthorised repository uploads constitute a direct data leakage pathway through an AI tool's default configuration.
- **AML.T0010 (AI Supply Chain Compromise)** and **LLM05 (Supply Chain Vulnerabilities)**: Both ZCode and Grok Build represent supply chain risk introduced by AI development tooling with opaque data handling.
- **AML.T0047 (AI-Enabled Product or Service)** and **AML.T0065 (LLM Prompt Crafting)**: RemControl demonstrates adversarial use of AI assistance to accelerate malware and phishing overlay development.
- **LLM08 (Excessive Agency)**: ZCode's autonomous repository snapshotting and upload behaviour exemplifies an AI tool acting beyond user-sanctioned scope.

## Impact Assessment

Enterprises adopting AI coding assistants face a credible risk of inadvertent intellectual property exfiltration to third-party cloud infrastructure, with potential regulatory exposure under GDPR, export control regimes, and sector-specific data governance frameworks. The RemControl campaign adds urgency for financial institutions operating in affected regions, as AI-assisted phishing tooling lowers the barrier to creating convincing overlays at scale.

## Mitigation & Recommendations

- **Immediately audit** all AI coding assistant tools for default data-sharing or telemetry settings before enterprise deployment.
- **Inspect outbound network traffic** from developer workstations for unexpected transfers to cloud storage endpoints.
- **Enforce mobile device management (MDM) policies** that flag or block Accessibility Service abuse on managed Android devices.
- **Require vendor disclosure** of all data destinations as a procurement condition for AI development tooling.
- **Monitor** for RemControl indicators of compromise shared by Group-IB, particularly fake Google Play pages impersonating TVTap.

## References

- [The Hacker News — ThreatsDay Bulletin, September 24 2026](https://thehackernews.com/2026/09/threatsday-ai-search-poisoning-ai.html)
- Group-IB RemControl Research (cited in source article)
