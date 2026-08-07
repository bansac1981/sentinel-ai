---
title: "Account Takeover Protection: OpenAI Hardens ChatGPT Auth"
date: "2026-05-01T04:42:27+00:00"
draft: false
slug: "openai-launches-phishing-resistant-security-mode-for-high-risk-chatgpt-accounts"

# ── Content metadata ──
summary: "OpenAI has introduced Advanced Account Security, an optional hardened authentication mode for ChatGPT and Codex users who face elevated risk of account takeover, including journalists, dissidents, and researchers. The feature enforces passkey or physical security key authentication, eliminates SMS/email recovery routes, and removes OpenAI support team access to recovery options to block social engineering attacks. Members of OpenAI's Trusted Access for Cyber programme will be mandated to enable it or provide equivalent enterprise SSO attestation by June 1."
source: "Wired Security"
source_url: "https://www.wired.com/story/openai-chatgpt-codex-advanced-account-security/"
source_title: "OpenAI Rolls Out \u2018Advanced\u2019 Security Mode for At-Risk Accounts"
source_date: 2026-04-30T17:30:39+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1718011087751-e82f1792aa32?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3NzYwOTc4OXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0040 - ML Model Inference API Access", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "OpenAI launches optional hardened account mode blocking passwords, SMS recovery, and support-channel social engineering."
tldr_who_at_risk: "Journalists, political dissidents, researchers, and security professionals whose ChatGPT/Codex accounts hold sensitive personal or professional context are most exposed to targeted account takeover."
tldr_actions:
  - "Enable Advanced Account Security on any ChatGPT or Codex account holding sensitive or professional data"
  - "Provision at least two physical security keys or passkeys before activating the feature to avoid lockout"
  - "If enrolled in OpenAI's Trusted Access for Cyber programme, comply with mandatory enforcement before June 1 or configure phishing-resistant enterprise SSO"

# ── Taxonomies ──
categories: ["LLM Security", "Industry News", "Regulatory"]
tags: ["account-security", "phishing-resistant-auth", "passkeys", "chatgpt", "codex", "openai", "social-engineering", "mfa", "yubikey", "account-takeover"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "hacktivist"]

# ── Pipeline metadata ──
fetched_at: "2026-05-01T04:31:39+00:00"
feed_source: "wired_security"
original_url: "https://www.wired.com/story/openai-chatgpt-codex-advanced-account-security/"
pipeline_version: "1.0.0"
---

## Overview

OpenAI has announced **Advanced Account Security**, an optional hardened protection tier for ChatGPT and Codex accounts, targeting users who face an elevated risk of adversarial account compromise. The announcement, made on 30 April 2026, mirrors analogous programmes such as Google's Advanced Protection Programme, which has existed for nearly a decade. The move is explicitly framed as part of OpenAI's broader cybersecurity strategy and acknowledges that AI accounts increasingly sit at the centre of sensitive personal and professional workflows.

As AI platforms accumulate context about their users — from private queries to integrated tooling and agentic workflows — these accounts become high-value targets for nation-state actors, cybercriminals, and politically motivated attackers seeking intelligence or operational disruption.

## Technical Analysis

Advanced Account Security enforces several layered controls:

- **Password elimination**: Standard passwords are disabled. Users must register a minimum of two physical security keys or passkeys (FIDO2/WebAuthn), which are inherently phishing-resistant because they bind to the legitimate origin domain.
- **Recovery channel hardening**: Email and SMS-based account recovery are removed entirely. Recovery is only possible via backup passkeys, recovery keys, or registered physical security keys — eliminating the most commonly abused recovery vectors.
- **Support isolation**: OpenAI's own support team loses the ability to perform account recovery actions. This is a critical control that closes the social engineering attack surface against helpdesk staff — a technique heavily exploited in high-profile breaches such as the Uber and MGM incidents.
- **Session tightening**: Sign-in session durations are shortened, reducing the window of exposure from stolen session tokens.
- **Login alerting**: Every new authentication event triggers an alert, enabling rapid detection of unauthorised access attempts.
- **Training opt-out by default**: Conversations are excluded from model training by default, reducing the risk of sensitive data leakage into future model iterations.

OpenAI has partnered with Yubico to offer discounted YubiKey bundles to enrolled users, lowering the barrier to hardware key adoption.

## Framework Mapping

- **AML.T0012 (Valid Accounts)**: The primary threat model addressed here is credential-based account takeover, where attackers obtain valid session credentials through phishing or social engineering to access AI inference APIs and stored conversation data.
- **AML.T0040 (ML Model Inference API Access)**: Compromised accounts provide unauthorised access to Codex and ChatGPT inference capabilities, which could be abused for scaled misuse or intelligence gathering.
- **LLM06 (Sensitive Information Disclosure)**: Accounts accumulating personal, professional, or organisational context represent a disclosure risk if compromised; the feature directly mitigates this.

## Impact Assessment

The at-risk population explicitly identified by OpenAI includes journalists, elected officials, political dissidents, and security researchers — groups historically targeted by sophisticated threat actors. For these users, an account compromise could expose sensitive sources, strategic plans, or research findings. The mandatory enforcement for Trusted Access for Cyber programme members by June 1 also signals that OpenAI is treating privileged API access as a security perimeter worthy of strong authentication controls.

## Mitigation & Recommendations

1. **Enrol in Advanced Account Security** for any ChatGPT or Codex account used in sensitive or professional contexts.
2. **Provision hardware security keys** (e.g., YubiKey 5 series) before enabling the feature to ensure account recovery paths are established.
3. **Audit connected integrations**: review which third-party tools and workflows are linked to your account, as a compromise could cascade through connected services.
4. **Organisations deploying Codex** should mandate phishing-resistant SSO and treat AI platform credentials with the same rigour as cloud IAM credentials.
5. **Security awareness**: train staff to recognise that AI platform accounts are now a legitimate target for social engineering, not just traditional IT systems.

## References

- [OpenAI Rolls Out 'Advanced' Security Mode for At-Risk Accounts — Wired, 30 April 2026](https://www.wired.com/story/openai-chatgpt-codex-advanced-account-security/)
