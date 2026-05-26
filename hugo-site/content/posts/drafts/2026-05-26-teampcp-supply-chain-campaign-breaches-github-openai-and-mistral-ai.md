---
title: "TeamPCP Supply Chain Campaign Breaches GitHub, OpenAI, and Mistral AI"
date: 2026-05-26T10:21:14+00:00
draft: true
slug: "teampcp-supply-chain-campaign-breaches-github-openai-and-mistral-ai"

# ── Content metadata ──
summary: "The TeamPCP threat actor escalated a multi-stage supply chain campaign in a single week, leveraging previously harvested OIDC credentials to trojanize a verified VS Code extension, compromise Microsoft's official PyPI SDK, and flood the npm @antv ecosystem with malicious packages. The operation directly breached GitHub's internal infrastructure, exfiltrating ~3,800 repositories, with OpenAI, Grafana Labs, and Mistral AI confirmed as downstream victims. The campaign demonstrates that publisher-verified and attestation badges provide no reliable install-time security guarantee, and that AI lab developer endpoints are now explicit targets."
source: "SANS Internet Storm Center"
source_url: "https://isc.sans.edu/diary/rss/33014"
source_title: "TeamPCP Supply Chain Campaign: Activity Through 2026-05-24, (Mon, May 25th)"
source_date: 2026-05-25T13:25:47+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1677442135131-4d7c123aef1c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3OTcwMzE5N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "TeamPCP chained stolen OIDC credentials into a multi-ecosystem attack that breached GitHub, OpenAI, and Mistral AI."
tldr_who_at_risk: "Developers, CI/CD pipelines, and AI lab engineering environments using VS Code extensions, PyPI packages, or npm @antv packages are directly exposed."
tldr_actions: ["Rotate all developer and CI/CD credentials exposed during the May 18 and May 24 compromise windows immediately", "Audit VS Code extension auto-update policies and disable auto-update for marketplace extensions in CI environments", "Inspect AI coding agent configuration files and plugin manifests for signs of persistence or unauthorized modification", "Remove trust assumptions from publisher-verified and attestation badges; treat them as insufficient safety signals", "Pin and hash-verify all PyPI and npm dependencies; audit durabletask versions 1.4.1–1.4.3 and @antv packages for malicious payloads"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "Industry News", "LLM Security"]
tags: ["supply-chain", "npm-malware", "pypi-malware", "vscode-extension", "github-breach", "openai", "mistral-ai", "credential-theft", "cicd-compromise", "oidc-abuse", "teampcp", "shai-hulud", "disk-wiper", "developer-tools", "nx-console"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-26T10:21:14+00:00"
feed_source: "sans_isc"
original_url: "https://isc.sans.edu/diary/rss/33014"
pipeline_version: "1.0.0"
---

## Overview

The TeamPCP threat actor executed three simultaneous supply chain escalations in a single week ending 2026-05-24, affecting GitHub's own internal infrastructure, Microsoft's official PyPI SDK, and the npm @antv ecosystem. OpenAI, Grafana Labs, and Mistral AI were confirmed as downstream victims. The campaign is the first publicly confirmed multi-stage operation of its kind: credentials harvested two weeks earlier were weaponised to compromise a verified-publisher VS Code extension, which then auto-updated on a GitHub employee endpoint and pivoted laterally through internal CI/CD systems.

The speed of each compromise window — 18 minutes for the VS Code extension, ~35 minutes for the PyPI SDK — underscores that even rapid takedowns cannot guarantee safety if auto-update mechanisms are enabled.

## Technical Analysis

**Stage 1 — Credential Harvesting (2026-05-11):** TeamPCP exploited CVE-2026-45321, an OIDC abuse chain in the TanStack ecosystem, to harvest publish credentials from a legitimate maintainer account.

**Stage 2 — VS Code Extension Trojanisation (2026-05-18):** The stolen Nx maintainer credential was used to publish a malicious build of the Nx Console extension (v18.95.0, publisher `nrwl.angular-console`, ~2.2M installs) to the Visual Studio Marketplace. The extension carried a payload that, on auto-update, exfiltrated developer secrets and used them to move laterally through GitHub's internal CI/CD, ultimately exfiltrating approximately 3,800 internal repositories.

**Stage 3 — PyPI SDK Trojanisation (2026-05-~23):** The officially Microsoft-published `durabletask` PyPI package (Azure Durable Functions client, ~417K monthly downloads) was replaced across three versions (1.4.1–1.4.3) within a ~35-minute window. Independent reporting characterises the second-stage payload as a Linux disk wiper.

**Stage 4 — npm @antv Wave (2026-05-24):** A compromised maintainer account (`atool`) was used to push 639 malicious package versions across 323 packages in the @antv ecosystem, including `echarts-for-react` (~1.1M weekly downloads) and `size-sensor` (~4.2M weekly downloads). This is described as the third "Mini Shai-Hulud" wave.

By the end of the week, the Shai-Hulud attack framework had reportedly been open-sourced to GitHub, with copycat forks already active.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** Direct trojanisation of packages consumed by AI lab developer environments.
- **AML.T0012 (Valid Accounts):** OIDC credential abuse enabled publishing under legitimate, verified-publisher identities.
- **AML.T0047 (ML-Enabled Product or Service):** OpenAI and Mistral AI are explicitly named downstream victims via developer toolchain compromise.
- **LLM05 (Supply Chain Vulnerabilities):** The core attack vector — poisoned packages distributed through trusted registries.
- **LLM06 (Sensitive Information Disclosure):** Repository exfiltration and credential theft from developer endpoints.
- **LLM07 (Insecure Plugin Design):** The VS Code extension auto-update mechanism provided the execution vector into internal CI/CD.

## Impact Assessment

The breach of ~3,800 GitHub-internal repositories is the most severe confirmed impact to date, though reporting indicates no customer-tenant data was accessed. For AI labs named as downstream victims (OpenAI, Mistral AI), the exposure of developer secrets and CI/CD pipeline access poses risks to model infrastructure, training pipelines, and proprietary codebases. The disk-wiper payload in the `durabletask` trojanisation represents a destructive escalation beyond espionage.

## Mitigation & Recommendations

1. **Rotate credentials** — immediately rotate all developer and CI/CD tokens that may have been active during the compromise windows.
2. **Disable auto-update** for VS Code extensions in developer and CI/CD environments; pin to verified, hash-checked versions.
3. **Audit PyPI and npm dependencies** — remove `durabletask` 1.4.1–1.4.3 and audit all @antv packages installed after 2026-05-20.
4. **Do not rely on verified-publisher badges** as a security signal; implement SBOM-based dependency verification.
5. **Inspect AI agent config files** for persistence artefacts introduced via compromised extensions or packages.
6. **Monitor for Shai-Hulud forks** on GitHub and block known indicators of compromise from SANS/ISC feeds.

## References

- [SANS ISC Diary — TeamPCP Supply Chain Campaign Through 2026-05-24](https://isc.sans.edu/diary/rss/33014)
- BleepingComputer reporting on CVE-2026-45321 OIDC abuse chain
- Help Net Security and OX Security reporting on Nx Console breach
- GitHub CISO Alexis Wales public disclosure
