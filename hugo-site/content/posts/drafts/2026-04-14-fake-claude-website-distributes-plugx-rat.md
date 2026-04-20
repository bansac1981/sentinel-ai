---
title: "Fake Claude Website Distributes PlugX RAT"
date: 2026-04-14T05:58:53+00:00
draft: true
slug: "fake-claude-website-distributes-plugx-rat"

# ── Content metadata ──
summary: "Threat actors have created a fraudulent website impersonating Anthropic's Claude AI platform to distribute the PlugX remote access trojan, leveraging DLL sideloading and self-cleanup techniques to evade detection. The campaign exploits growing public trust in legitimate AI brands to lure victims into executing malware under the guise of an official Claude installation. This represents a notable trend of adversaries weaponising AI product branding as a social engineering vector."
# ── TL;DR ──
tldr_what: "Fake Claude website distributes PlugX RAT via DLL sideloading and self-cleanup evasion."
tldr_who_at_risk: "Users downloading Claude from unofficial sources or typosquatted domains seeking legitimate AI tools."
tldr_actions: ["Download Claude only from anthropic.com; verify domain spelling carefully.", "Block suspicious Claude installer domains at network/DNS level.", "Scan systems for PlugX artifacts; monitor for unsigned DLL loads."]
source: "SecurityWeek"
source_url: "https://www.securityweek.com/fake-claude-website-distributes-plugx-rat/"
source_date: 2026-04-13T09:52:50+00:00
author: "Grid the Grey Editorial"
thumbnail: ""

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0010 - ML Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["plugx", "rat", "dll-sideloading", "typosquatting", "fake-installer", "anthropic", "claude", "brand-impersonation", "social-engineering", "malware-distribution"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-04-14T05:58:53+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/fake-claude-website-distributes-plugx-rat/"
pipeline_version: "1.0.0"
---

## Overview

A fraudulent website impersonating Anthropic's Claude AI assistant has been identified distributing the PlugX remote access trojan (RAT). The campaign mimics the legitimate Claude installation experience, deceiving users into downloading and executing malware that establishes persistent, covert access to their systems. The use of a trusted and rapidly growing AI brand as a lure highlights an accelerating trend: threat actors are actively exploiting public enthusiasm for mainstream AI products as a social engineering mechanism.

PlugX is a well-documented, modular RAT historically associated with Chinese-nexus threat groups, though its use has broadened across cybercriminal ecosystems. Its presence in this campaign suggests a sophisticated actor with access to established tooling.

## Technical Analysis

The attack chain relies on several evasion and delivery techniques:

- **Brand Impersonation / Typosquatting**: A fake website replicates the visual identity and download flow of the legitimate Claude desktop application, increasing the likelihood of victim compliance.
- **DLL Sideloading**: The installer drops a legitimate signed executable alongside a malicious DLL. When the signed binary loads, it inadvertently loads the malicious DLL, abusing Windows' DLL search order to execute PlugX without triggering standard security controls.
- **Self-Cleanup**: After successful execution, the dropper removes artefacts from disk, complicating forensic analysis and reducing the window for detection by endpoint security tooling.

This combination — trusted brand lure, living-off-the-land sideloading, and anti-forensic cleanup — reflects operational maturity and is consistent with techniques observed in both nation-state and sophisticated cybercriminal campaigns.

## Framework Mapping

- **AML.T0047 – ML-Enabled Product or Service**: Adversaries are directly exploiting the trust and brand recognition of a real-world AI product (Claude/Anthropic) to facilitate initial access, making the AI product itself a vector.
- **AML.T0010 – ML Supply Chain Compromise**: While not a direct supply chain attack, the impersonation of an AI software distribution channel targets the trust users place in AI vendor ecosystems.
- **LLM05 – Supply Chain Vulnerabilities**: The fake installer mimics a legitimate AI software distribution pipeline, exploiting weaknesses in how users verify the authenticity of AI tool downloads.

## Impact Assessment

Any individual or organisation downloading Claude from unofficial or unverified sources is potentially at risk. PlugX enables full remote control, credential harvesting, lateral movement, and persistent access — meaning a successful infection could have severe downstream consequences for enterprise environments. The campaign is particularly dangerous given that AI tool adoption is currently widespread and rapid, with many users downloading new AI applications with limited scrutiny.

## Mitigation & Recommendations

1. **Verify download sources**: Only download Anthropic products from `anthropic.com` or verified official channels. Validate SSL certificates and domain authenticity before executing any installer.
2. **Enable application allowlisting**: Prevent execution of unsigned or unexpected binaries, particularly those loaded via DLL sideloading patterns.
3. **Monitor for DLL sideloading indicators**: Deploy EDR rules to detect known-vulnerable signed executables being placed alongside unexpected DLLs.
4. **User awareness training**: Educate staff on AI brand impersonation campaigns, emphasising that threat actors are actively targeting interest in AI tools.
5. **DNS and web filtering**: Block access to known malicious domains impersonating AI vendors at the network perimeter.

## References

- [Fake Claude Website Distributes PlugX RAT — SecurityWeek](https://www.securityweek.com/fake-claude-website-distributes-plugx-rat/)
