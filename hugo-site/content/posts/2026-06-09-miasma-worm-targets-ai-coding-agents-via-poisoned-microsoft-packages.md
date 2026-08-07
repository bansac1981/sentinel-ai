---
title: "Miasma Worm Compromises 73 Microsoft NPM Packages for AI Agents"
date: "2026-06-09T10:45:08+00:00"
draft: false 
slug: "miasma-worm-targets-ai-coding-agents-via-poisoned-microsoft-packages"

# ── Content metadata ──
summary: "Seventy-three Microsoft-hosted open source packages were compromised with the Miasma credential-stealing worm, which activates specifically when developers open packages inside AI coding agents. The malware, attributed to threat actor TeamPCP, exploits legitimate OIDC token workflows and SLSA provenance attestation to bypass supply-chain integrity checks and spread laterally across cloud infrastructure. This marks the second such compromise of an official Microsoft repository in as many months, indicating a sustained campaign targeting developer toolchains and the AI-assisted development pipeline."
source: "Ars Technica Security"
source_url: "https://arstechnica.com/security/2026/06/for-the-2nd-time-in-weeks-microsoft-packages-laced-with-credential-stealer/"
source_title: "For the 2nd time in weeks, Microsoft packages laced with credential stealer"
source_date: 2026-06-08T18:34:23+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1595928796398-1d0ac507eed0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxtYWx3YXJlJTIwY29tcHV0ZXIlMjB2aXJ1cyUyMGRhcmslMjBoYWNrZXJ8ZW58MHwwfHx8MTc4MDk4ODM3N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "73 Microsoft packages infected with Miasma credential stealer, triggered by AI coding agents."
tldr_who_at_risk: "Developers using AI coding agents to work with Microsoft open source packages are directly exposed, with cloud credentials and developer tool configs at risk."
tldr_actions:
  - "Audit all recently installed Microsoft npm/PyPI packages against the 73 flagged identifiers and treat any usage via AI agent as a full compromise event"
  - "Rotate all cloud credentials (AWS, Azure, GCP, Kubernetes) and secrets stored in password managers on any affected developer machines"
  - "Restrict AI coding agent permissions to read-only package access and enforce sandboxed execution environments before installing open source dependencies"

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Industry News"]
tags: ["supply-chain-attack", "credential-stealer", "ai-coding-agents", "microsoft", "npm", "pypi", "miasma-worm", "teampcp", "oidc-token-abuse", "slsa-provenance", "github", "lateral-movement", "cloud-credentials", "developer-toolchain"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-06-09T07:00:43+00:00"
feed_source: "arstechnica"
original_url: "https://arstechnica.com/security/2026/06/for-the-2nd-time-in-weeks-microsoft-packages-laced-with-credential-stealer/"
pipeline_version: "1.0.0"
---

## Overview

For the second time in under two months, official Microsoft-hosted open source packages have been found carrying the Miasma credential-stealing worm. In the most recent incident, 73 packages were flagged as malicious after automated systems on GitHub blocked them. The packages were weaponised to execute a credential-harvesting payload the moment a developer opened them inside an AI coding agent — a deliberate targeting of automated, agentic development workflows. The incident follows a May 2026 compromise of Microsoft's `durabletask` Python SDK on PyPI, attributed to the same threat actor, TeamPCP.

Notably, GitHub's initial public messaging described the removals as "a violation of GitHub's terms of service" rather than explicitly warning of malicious content, delaying developer awareness and incident response.

## Technical Analysis

The Miasma malware is derived from TeamPCP's Mini Shai-Hulud toolkit, which the group open-sourced. Its primary infection vector exploits the trust model of modern software supply chains rather than any vulnerability in GitHub or npm infrastructure.

The attack chain proceeds as follows:

1. **Credential compromise**: Attackers obtain legitimate Microsoft credentials used for publishing packages, bypassing the repository's build pipeline entirely.
2. **OIDC token abuse**: A legitimate GitHub OIDC (OpenID Connect) token is requested using the compromised credentials.
3. **Provenance spoofing**: A malicious build is published with valid SLSA (Supply-chain Levels for Software Artifacts) provenance attestation — cryptographically signed metadata that is normally a signal of integrity.
4. **Payload execution**: The 28 KB payload activates when an AI coding agent opens the package, harvesting credentials from AWS, Azure, GCP, Kubernetes, password managers, and over 90 developer tool configurations.
5. **Lateral movement**: The worm spreads through cloud infrastructure to infect additional developer machines.

The exploitation of SLSA provenance is particularly significant: it subverts a control specifically designed to provide supply-chain integrity guarantees, turning a trust signal into a vector for credential legitimisation.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise)**: Packages distributed through official Microsoft repositories are poisoned prior to developer consumption, directly targeting AI-assisted development pipelines.
- **AML.T0012 (Valid Accounts)**: Compromised Microsoft publisher credentials enable legitimate-looking package releases that bypass automated defences.
- **AML.T0047 (ML-Enabled Product or Service)**: The trigger condition — opening packages inside AI coding agents — specifically weaponises agentic AI workflows.
- **LLM05 (Supply Chain Vulnerabilities)**: The attack exploits trusted package repositories as an entry point into developer and AI agent environments.
- **LLM08 (Excessive Agency)**: AI coding agents with broad filesystem and network permissions amplify the blast radius when a malicious package is executed.

## Impact Assessment

Developers using AI coding agents to consume Microsoft open source packages are at highest risk. Any machine where an affected package was opened by an agent should be treated as fully compromised. Cloud credentials across all major providers, Kubernetes configurations, and secrets stored in password managers are in scope for exfiltration. The worm's lateral movement capability means initial compromise of a single developer machine can propagate across an entire cloud-connected organisation.

## Mitigation & Recommendations

- **Assume compromise**: Any developer or pipeline that interacted with the 73 flagged packages via an AI agent should initiate full incident response immediately.
- **Rotate credentials**: Invalidate and rotate all cloud provider credentials, OIDC tokens, and secrets on affected systems.
- **Restrict agent permissions**: AI coding agents should operate under least-privilege principles with sandboxed execution environments; prevent agents from executing package install hooks without human approval.
- **Do not rely solely on SLSA provenance**: This attack demonstrates that valid provenance attestation is not sufficient to confirm integrity when upstream credentials are compromised.
- **Monitor for lateral movement**: Audit cloud access logs for anomalous API calls originating from developer machines.

## References

- [Ars Technica: For the 2nd time in weeks, Microsoft packages laced with credential stealer](https://arstechnica.com/security/2026/06/for-the-2nd-time-in-weeks-microsoft-packages-laced-with-credential-stealer/)
