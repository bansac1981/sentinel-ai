---
title: "Signed Malicious Mistral and TanStack Packages Expose AI Developer Supply Chain"
date: 2026-05-13T05:09:15+00:00
draft: true
slug: "signed-malicious-mistral-and-tanstack-packages-expose-ai-developer-supply-chain"

# ── Content metadata ──
summary: "The TeamPCP threat group executed a sophisticated supply chain attack dubbed Shai-Hulud, compromising over 400 npm and PyPI package artifacts including Mistral AI and TanStack packages by hijacking OIDC tokens and abusing CI/CD pipelines to publish cryptographically signed malicious versions. The attack is particularly dangerous because the malicious packages carried valid SLSA Build Level 3 provenance attestations and Sigstore signatures, making them indistinguishable from legitimate releases to developers. AI tooling ecosystems \u2014 including Mistral AI, Guardrails AI, and UiPath packages \u2014 were directly targeted, exposing developer credentials and secrets at scale."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/shai-hulud-attack-ships-signed-malicious-tanstack-mistral-npm-packages/"
source_title: "Shai Hulud attack ships signed malicious TanStack, Mistral npm packages"
source_date: 2026-05-12T11:29:36+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1689942009554-759940987be0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxzdXBwbHklMjBjaGFpbiUyMHNvZnR3YXJlJTIwcGFja2FnZXN8ZW58MHwwfHx8MTc3ODY0ODk1NXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0019 - Publish Poisoned Datasets", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "TeamPCP poisoned 400+ AI and dev tool packages with signed malware via stolen OIDC tokens."
tldr_who_at_risk: "Developers consuming Mistral AI, TanStack, Guardrails AI, UiPath, or OpenSearch packages via npm or PyPI are directly exposed to credential-stealing malware."
tldr_actions: ["Audit all npm and PyPI dependencies for Mistral AI, TanStack, Guardrails AI, UiPath, and OpenSearch packages published around May 11–12, 2026", "Rotate all developer secrets, tokens, and CI/CD credentials that may have been exposed in affected environments", "Do not rely solely on SLSA provenance or Sigstore attestations as authenticity guarantees — verify package integrity through multiple independent channels", "Restrict pull_request_target workflow permissions in GitHub Actions and audit CI/CD pipelines for cache poisoning risks", "Enable runtime dependency monitoring via tools like Endor Labs, Socket, or Aikido to detect future compromised package versions"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["supply-chain-attack", "npm", "pypi", "mistral-ai", "tanstack", "oidc-token-hijacking", "slsa-bypass", "ci-cd-compromise", "credential-theft", "sigstore", "teampcp", "shai-hulud", "github-actions", "guardrails-ai", "developer-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-13T05:09:15+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/shai-hulud-attack-ships-signed-malicious-tanstack-mistral-npm-packages/"
pipeline_version: "1.0.0"
---

## Overview

A sophisticated supply chain campaign dubbed **Shai-Hulud**, attributed to the threat group **TeamPCP**, has compromised over 400 package artifacts across npm and PyPI. The attack specifically targeted AI ecosystem tooling — including official **Mistral AI** and **Guardrails AI** packages — alongside developer infrastructure staples like TanStack, UiPath, OpenSearch, Bitwarden CLI, and SAP packages. What makes this campaign particularly alarming is that all malicious package versions carried **valid cryptographic signatures**, SLSA Build Level 3 provenance attestations, and legitimate GitHub Actions signatures, rendering standard supply chain verification controls ineffective.

The campaign has been active since at least September 2025 and has undergone multiple iterations, with previous waves exposing hundreds of thousands of developer secrets via auto-generated GitHub repositories.

## Technical Analysis

The attackers chained three distinct vulnerabilities to achieve signed, trusted package publication:

1. **`pull_request_target` workflow abuse**: This GitHub Actions trigger runs with write permissions even for PRs from forks, creating an elevation-of-privilege vector.
2. **GitHub Actions cache poisoning**: Attackers injected malicious build artefacts into the Actions cache layer, which were then consumed by legitimate downstream workflows.
3. **OIDC token theft from runner memory**: The attackers exfiltrated short-lived OpenID Connect tokens from runner process memory during workflow execution, allowing them to authenticate as the legitimate CI/CD identity and publish packages through the official TanStack/router Release workflow.

Endor Labs documented a particularly subtle technique: attackers pushed an **orphaned commit to a fork** of TanStack/router, exploiting GitHub's shared fork object storage to make the malicious commit reachable through the legitimate repository's object graph without it appearing in any branch history.

The result: 84 malicious package versions across 42 TanStack packages, each bearing valid npm provenance, valid Sigstore attestations, and legitimate GitHub Actions signatures. From a developer or automated scanning perspective, no anomaly was detectable through standard verification.

The credential-stealing payload targeted developer secrets, API keys, and CI/CD tokens — highly valuable for further supply chain pivoting or AI service account compromise.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise)**: Direct compromise of AI framework packages (Mistral AI, Guardrails AI) distributed through public registries.
- **AML.T0012 (Valid Accounts)**: OIDC token hijacking enabled the attacker to act as a legitimate CI/CD identity.
- **AML.T0019 (Publish Poisoned Datasets/Packages)**: Malicious versions published through legitimate channels with authentic provenance.
- **LLM05 (Supply Chain Vulnerabilities)**: The attack targets the software supply chain for LLM tooling and AI development frameworks.
- **LLM06 (Sensitive Information Disclosure)**: Credential-stealing payloads targeting developer and CI/CD secrets.

## Impact Assessment

Any developer or organisation that installed affected package versions between the attack window is at risk of **credential exfiltration**. The Mistral AI and Guardrails AI compromise is especially significant for AI practitioners who may have API keys or model access tokens stored in their development environments. With over 416 compromised artefacts confirmed, blast radius is substantial. The SLSA and Sigstore bypass is a **systemic threat** to the broader software supply chain trust model — the assurance these frameworks are designed to provide was entirely negated.

## Mitigation & Recommendations

- **Immediately audit** installed versions of Mistral AI, TanStack, Guardrails AI, UiPath, OpenSearch, Bitwarden CLI, and SAP npm/PyPI packages against confirmed malicious version lists published by Endor Labs, Aikido, and Socket.
- **Rotate all credentials** — especially API keys, CI/CD tokens, and cloud provider credentials — accessible from affected developer machines or pipelines.
- **Restrict `pull_request_target`** workflow permissions; prefer `pull_request` for untrusted fork contributions.
- **Implement cache integrity controls** in GitHub Actions pipelines; consider disabling cross-fork cache sharing.
- **Do not treat SLSA/Sigstore attestations as sole trust anchors** — complement with behavioural monitoring and independent hash verification.
- Deploy **runtime dependency monitoring** solutions capable of detecting malicious package behaviour post-install.

## References

- [BleepingComputer — Shai Hulud attack ships signed malicious TanStack, Mistral npm packages](https://www.bleepingcomputer.com/news/security/shai-hulud-attack-ships-signed-malicious-tanstack-mistral-npm-packages/)
