---
title: "Cursor Marketplace Trojanized via Stolen Fireworks AI Key"
date: 2026-11-15T12:55:13+00:00
draft: false
slug: "cursor-marketplace-trojanized-via-stolen-fireworks-ai-key"

# ── Content metadata ──
summary: "Attackers exploited a stolen API key from Fireworks AI to access Cursor's data storage, harvesting credentials that enabled them to inject a backdoored version of Anthropic's Claude Code extension into the Cursor extension marketplace. Up to 5,000 users received the malicious build \u2014 versions 2.1.312 and 2.1.313 \u2014 which attempted to install a persistent SSH backdoor on affected systems. The incident illustrates a multi-stage AI supply chain attack, chaining third-party vendor compromise through credential exposure in coding agent traces to downstream extension poisoning."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/stolen-fireworks-ai-key-led-to-cursor.html"
source_title: "Cursor Says Stolen Fireworks AI Key Led to Trojanized Claude Code Extension Incident"
source_date: 2026-11-15T08:22:04+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1724786978326-f3ea21dca03d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxwYXJhc2l0ZSUyMG5hdHVyZSUyMGNsb3NlLXVwJTIwbWFjcm98ZW58MHwwfHx8MTc5NDc0NzMxMnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0057 - LLM Data Leakage", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0098 - AI Agent Tool Credential Harvesting"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Stolen Fireworks AI key enabled attackers to trojanize Cursor's Claude Code extension with an SSH backdoor."
tldr_who_at_risk: "Cursor users who installed Claude Code extension versions 2.1.312 or 2.1.313 on October 29, 2026 are most at risk due to potential persistent SSH backdoor installation."
tldr_actions: ["Immediately uninstall Claude Code extension versions 2.1.312 and 2.1.313 and audit systems for SSH backdoor artifacts", "Rotate all API keys and credentials shared with third-party AI inference vendors, especially any exposed in non-privacy-mode coding sessions", "Audit coding agent session traces for unredacted credentials before permitting their use in vendor-shared training datasets"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Agentic AI", "Industry News"]
tags: ["cursor-ide", "claude-code", "fireworks-ai", "supply-chain-attack", "ssh-backdoor", "credential-exposure", "extension-marketplace", "anthropic", "trojanized-extension", "api-key-theft", "coding-agent", "ai-infrastructure"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-15T12:55:13+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/stolen-fireworks-ai-key-led-to-cursor.html"
pipeline_version: "2.1.0"
content_hash: "907e3aa4a84eaf98"
---

## Overview

Cursor, the AI-powered coding platform, has confirmed that a trojanized version of Anthropic's official Claude Code extension was distributed through its extension marketplace on October 29, 2026, as the downstream consequence of a third-party vendor breach. The root cause: a stolen API key issued to Fireworks AI, an inference provider, exposed data in a shared read-only storage bucket that contained unredacted credentials from coding agent session traces. Attackers leveraged those credentials to pivot into Cursor's internal systems and poison its extension distribution cache — a textbook multi-stage AI supply chain attack.

## Technical Analysis

The attack unfolded in two distinct phases:

**Phase 1 — Vendor key theft and data exfiltration:** An attacker obtained an access key Cursor had issued to Fireworks AI following a breach of that provider. Using the key against a read-only storage bucket shared for model training purposes, the attacker exfiltrated coding agent session traces dating to 2025. Critically, these traces contained credentials that had not been scrubbed — exposing API secrets belonging to fewer than 0.01% of Cursor's customer base. The attacker used these to pivot into select Cursor SaaS tooling, accessing archived source code repositories, customer support data, usage metrics, and credentials users had submitted via support channels.

**Phase 2 — Extension cache poisoning:** Armed with an internal credential harvested during Phase 1, the attacker directly modified the cache layer serving Cursor's extension marketplace. Trojanized builds of Anthropic's Claude Code extension (versions 2.1.312 and 2.1.313) were substituted for the legitimate update. The malicious build attempted to install a persistent SSH backdoor on host systems. The window of exposure lasted approximately 11 hours, during which up to 5,000 users may have downloaded the compromised extension.

Cursor responded by taking the extension marketplace offline, deactivating Fireworks AI's key, rotating internal credentials, and working with the cloud hosting provider to take down the attacker's C2 server.

## Framework Mapping

- **AML.T0010 (AI Supply Chain Compromise)** and **AML.T0115 (Publish Poisoned AI Artifacts)**: The attacker directly injected a malicious extension into an AI coding tool's distribution pipeline.
- **AML.T0083 / AML.T0098 (Credentials from / Harvesting AI Agent Configuration)**: Unredacted credentials in coding agent traces were the pivotal enabler.
- **AML.T0057 (LLM Data Leakage)**: Session data shared with a third-party vendor leaked sensitive customer credentials.
- **LLM05 (Supply Chain Vulnerabilities)**: The attack exploited trust in a third-party inference vendor and the extension update mechanism.
- **LLM06 (Sensitive Information Disclosure)**: Credentials embedded in agent traces constituted direct sensitive data exposure.

## Impact Assessment

Up to 5,000 Cursor users are potentially affected by the backdoored extension. Any developer who installed versions 2.1.312 or 2.1.313 on October 29, 2026 may have a persistent SSH backdoor on their system. The broader credential exposure from agent traces — while affecting fewer than 0.01% of customers — enabled lateral movement into internal Cursor infrastructure, including source code and customer support records. The incident also disrupted Cursor platform features during the containment period.

## Mitigation & Recommendations

1. **Uninstall and audit:** Remove Claude Code versions 2.1.312/2.1.313 immediately and scan for unauthorised SSH keys or persistent backdoor artifacts.
2. **Rotate all vendor-shared credentials:** Any API keys or secrets shared with inference or data partners should be treated as compromised and rotated.
3. **Enable Privacy Mode:** Cursor users should activate Privacy Mode to prevent session traces from being shared with third parties for training.
4. **Implement credential scrubbing:** AI platforms must enforce automated redaction of secrets in agent session traces before those traces enter any shared storage.
5. **Apply least-privilege to vendor keys:** Third-party inference providers should receive scoped, time-limited keys with no access beyond what is operationally necessary.

## References

- [Cursor Says Stolen Fireworks AI Key Led to Trojanized Claude Code Extension Incident — The Hacker News](https://thehackernews.com/2026/11/stolen-fireworks-ai-key-led-to-cursor.html)
