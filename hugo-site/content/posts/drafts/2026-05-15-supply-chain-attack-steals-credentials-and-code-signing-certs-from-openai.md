---
title: "Supply Chain Attack Steals Credentials and Code-Signing Certs from OpenAI"
date: 2026-05-15T16:43:36+00:00
draft: true
slug: "supply-chain-attack-steals-credentials-and-code-signing-certs-from-openai"

# ── Content metadata ──
summary: "A coordinated supply chain attack targeting the TanStack open-source ecosystem compromised two OpenAI employee devices, resulting in credential and secrets exfiltration from internal source code repositories. The attackers, identified as the TeamPCP hacking group, deployed the Shai-Hulud worm via 84 malicious artifacts across 42 packages on NPM and PyPI. Code-signing certificates for OpenAI's iOS, macOS, Windows, and Android applications were among the stolen material, forcing a full certificate revocation and re-signing campaign."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/openai-hit-by-tanstack-supply-chain-attack/"
source_title: "OpenAI Hit by TanStack Supply Chain Attack"
source_date: 2026-05-15T10:37:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3ODg2MzMxNHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "TeamPCP poisoned TanStack packages to steal credentials and code-signing certs from OpenAI repositories."
tldr_who_at_risk: "Organizations consuming TanStack, NPM, or PyPI packages are at risk, particularly those with developers who have broad repository access."
tldr_actions: ["Audit all NPM and PyPI dependencies consumed between May 11–15, 2026 for TanStack-related packages", "Rotate any credentials or secrets stored on developer machines or accessible via compromised repositories", "Update all OpenAI macOS applications before June 12, 2026 to receive the re-signed certificates"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["supply-chain-attack", "openai", "tanstack", "npm-poisoning", "pypi", "credential-theft", "code-signing", "shai-hulud-worm", "teampcp", "developer-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-15T16:43:36+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/openai-hit-by-tanstack-supply-chain-attack/"
pipeline_version: "1.0.0"
---

## Overview

On May 11, 2026, the threat actor group TeamPCP executed a coordinated supply chain attack against TanStack, a widely used open-source web application development stack. By exploiting weaknesses in the package publishing pipeline, the group injected 84 malicious artifacts across 42 packages on NPM and PyPI, with over 170 packages ultimately compromised across multiple high-profile namespaces. OpenAI has confirmed it was among the downstream victims, with two employee devices infected by the Shai-Hulud worm and credential material exfiltrated from internal source code repositories.

The incident is significant beyond its immediate scope: the compromised repositories contained code-signing certificates for OpenAI's iOS, macOS, Windows, and Android products — assets that could theoretically enable the distribution of trojanised applications bearing legitimate OpenAI signatures.

## Technical Analysis

The attack vector was the package publishing process for TanStack. TeamPCP exploited insufficient integrity controls in the publishing workflow to release malicious package versions. Developers who installed or updated affected packages during the window of compromise had the Shai-Hulud worm deployed on their machines.

The worm's primary payload was credential harvesting: it extracted secrets, tokens, and other authentication material from the infected developer environments. In OpenAI's case, this granted the attackers read access to internal repositories accessible to the two compromised employees. The most sensitive material confirmed stolen was code-signing certificate material for four major platforms.

OpenAI's response included:
- Rotating credentials across all affected repositories
- Revoking active user sessions
- Temporarily restricting code-deployment workflows
- Revoking all compromised code-signing certificates and re-signing applications

## Framework Mapping

**MITRE ATLAS AML.T0010 — ML Supply Chain Compromise:** The attack directly targeted the open-source dependency supply chain used by AI/ML development teams, making this a textbook ML supply chain compromise scenario.

**MITRE ATLAS AML.T0012 — Valid Accounts:** Credential exfiltration enabled attackers to leverage legitimate employee access to internal repositories without triggering anomalous authentication patterns.

**OWASP LLM05 — Supply Chain Vulnerabilities:** The attack exploited trust in upstream open-source packages, a canonical supply chain risk for AI product teams consuming third-party libraries.

**OWASP LLM06 — Sensitive Information Disclosure:** Secrets and credential material stored in or accessible from developer environments were successfully exfiltrated.

## Impact Assessment

OpenAI's direct exposure was limited in scope — two devices, restricted repository access, no customer data or intellectual property confirmed stolen. However, the theft of code-signing certificates represents a high-severity outcome. If not rapidly revoked, such certificates could be weaponised to sign and distribute malicious applications with apparent OpenAI legitimacy, potentially targeting OpenAI's broad consumer base.

The broader ecosystem impact is significant: any organisation with developers consuming TanStack, NPM, or PyPI packages during the May 11 window is potentially affected. AI and ML teams are disproportionately exposed given their heavy reliance on Python and JavaScript package ecosystems.

## Mitigation & Recommendations

- **Dependency audit:** Immediately review all package installs and updates from May 11–15, 2026 against the published list of 42 compromised TanStack packages.
- **Credential rotation:** Treat all secrets accessible from developer machines as potentially compromised; rotate API keys, tokens, and certificates proactively.
- **Application updates:** OpenAI macOS users must update all OpenAI applications before June 12, 2026 to receive re-signed binaries.
- **Publisher integrity controls:** Enforce package signature verification and use lockfiles to pin known-good dependency versions.
- **Developer endpoint hardening:** Apply principle of least privilege to developer repository access to limit blast radius in future credential theft scenarios.
- **Worm IOC scanning:** Run endpoint detection against published Shai-Hulud indicators of compromise on all developer machines.

## References

- [OpenAI Hit by TanStack Supply Chain Attack — SecurityWeek](https://www.securityweek.com/openai-hit-by-tanstack-supply-chain-attack/)
