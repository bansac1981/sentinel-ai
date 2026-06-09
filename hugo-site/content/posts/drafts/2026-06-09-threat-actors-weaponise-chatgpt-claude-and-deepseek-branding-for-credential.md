---
title: "Threat Actors Weaponise ChatGPT, Claude, and DeepSeek Branding for Credential Theft"
date: 2026-06-09T07:01:24+00:00
draft: true
slug: "threat-actors-weaponise-chatgpt-claude-and-deepseek-branding-for-credential"

# ── Content metadata ──
summary: "Microsoft Threat Intelligence has identified a wave of campaigns exploiting the popularity of AI platforms \u2014 including ChatGPT, Claude, DeepSeek, and Microsoft Copilot \u2014 as social engineering lures for phishing, malvertising, and SEO-poisoning attacks. The campaigns deploy phishing kits, Vidar stealer malware, and adversary-in-the-middle (AiTM) techniques to harvest credentials, access tokens, and financial data. While the AI services themselves are not compromised, the attacks demonstrate how public enthusiasm for AI is being systematically operationalised by threat actors."
source: "Microsoft Security Blog"
source_url: "https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/"
source_title: "AI brands as bait: How threat actors are using the AI hype in social engineering"
source_date: 2026-06-08T16:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1737505599159-5ffc1dcbc08f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc4MDkyNjQ2NXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM09 - Overreliance", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Criminals are impersonating ChatGPT, Claude, and DeepSeek to steal credentials and deploy malware."
tldr_who_at_risk: "End users and enterprises seeking AI tools are most exposed, particularly those downloading software or clicking sponsored search results."
tldr_actions: ["Block or flag domains impersonating known AI platforms at the email and DNS gateway level", "Train users to verify AI software sources and avoid installing tools from unofficial GitHub repos or search ads", "Enable phishing-resistant MFA across all accounts to limit impact of harvested credentials"]

# ── Taxonomies ──
categories: ["Industry News", "Supply Chain", "LLM Security"]
tags: ["social-engineering", "phishing", "malvertising", "credential-theft", "chatgpt-lure", "deepseek", "claude", "vidar-stealer", "aitm", "seo-poisoning", "ai-brand-abuse", "microsoft-threat-intelligence"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-06-09T07:01:24+00:00"
feed_source: "microsoft_security"
original_url: "https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/"
pipeline_version: "1.0.0"
---

## Overview

Microsoft Threat Intelligence has documented a sustained and growing cluster of cybercriminal campaigns that abuse the branding of major AI platforms — ChatGPT, Microsoft Copilot, Anthropic's Claude, and DeepSeek — as social engineering lures. Published in June 2026, the research confirms that threat actors are capitalising on public enthusiasm for AI tools to increase the credibility and click-through rates of phishing, malvertising, and SEO-driven attacks. The underlying AI services themselves have not been compromised; rather, their reputations are being weaponised.

## Technical Analysis

The Microsoft report details four primary attack patterns:

**1. ChatGPT-Themed Phishing Kit**
A phishing kit mimicking the ChatGPT interface was used to harvest credit card data from victims who believed they were signing up for or upgrading an AI subscription. The kit included convincing UI clones and payment form interception.

**2. Claude-Themed AiTM Campaign**
An adversary-in-the-middle (AiTM) campaign impersonated Anthropic's Claude platform to steal both user credentials and session/access tokens, enabling post-authentication account takeover without requiring the victim's password again.

**3. 'Awesome AI Windows Plugin' Malvertising**
Malicious search advertisements promoted a fake AI productivity plugin. Victims who clicked and installed the software received Vidar stealer — an infostealer capable of exfiltrating browser credentials, crypto wallets, and system data.

**4. Fake DeepSeek V4 GitHub Installers**
Threat actors uploaded trojanised DeepSeek installer packages to GitHub repositories, leveraging the platform's trusted reputation. Execution again resulted in Vidar stealer infection.

Common tradecraft across all campaigns includes multi-stage redirection chains, urgency-driven messaging, and abuse of legitimate hosting infrastructure to evade detection.

## Framework Mapping

- **AML.T0047 (ML-Enabled Product or Service):** Attackers are abusing the public perception of AI products as trusted services to lower victim suspicion — a form of trust exploitation tied to ML-adjacent branding.
- **AML.T0012 (Valid Accounts):** AiTM credential and token theft campaigns directly target valid account takeover as an outcome.
- **LLM09 (Overreliance):** Users who implicitly trust AI platform branding without verification are a key enabler of these attacks.
- **LLM05 (Supply Chain Vulnerabilities):** Fake GitHub-hosted installers represent a software supply chain abuse vector targeting AI tool consumers.

## Impact Assessment

The affected population spans general consumers and enterprise users alike — anyone actively searching for, trialling, or purchasing AI productivity tools. The use of Vidar stealer introduces risk beyond initial credential loss, including lateral movement potential within corporate environments. AiTM token theft specifically bypasses MFA protections, elevating the severity for organisations relying on password-plus-OTP configurations.

## Mitigation & Recommendations

- **Enforce phishing-resistant MFA** (FIDO2/hardware keys) to neutralise AiTM token theft techniques.
- **Apply domain reputation filtering** to block newly registered or lookalike domains impersonating AI brands at email and DNS layers.
- **Restrict software installation** to approved, verified sources; flag unofficial GitHub repositories distributing AI tools.
- **Deploy endpoint detection** capable of identifying Vidar stealer indicators (see Microsoft's published IOCs).
- **Conduct user awareness training** specifically covering AI brand impersonation as an emerging lure category.
- **Monitor for anomalous access token usage** post-authentication to detect AiTM session hijacking.

## References

- [Microsoft Security Blog — AI brands as bait (June 8, 2026)](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/)
