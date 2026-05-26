---
title: "TeamPCP Supply Chain Campaign Breaches GitHub, Hits OpenAI and Mistral AI"
date: 2026-05-26T10:20:36+00:00
draft: true
slug: "teampcp-supply-chain-campaign-breaches-github-hits-openai-and-mistral-ai"

# ── Content metadata ──
summary: "The TeamPCP threat actor escalated a multi-stage supply chain campaign in a single week, compromising a verified VS Code extension to breach GitHub's internal CI/CD and exfiltrate ~3,800 repositories, with OpenAI, Mistral AI, and Grafana Labs named as downstream victims. The same operator simultaneously trojanized Microsoft's official Azure Durable Functions Python SDK on PyPI with a Linux disk wiper payload, and pushed 639 malicious npm packages through the @antv ecosystem. AI development tooling and developer endpoints at major AI labs were directly targeted, making this a high-severity event for AI/ML supply chain security."
source: "SANS Internet Storm Center"
source_url: "https://isc.sans.edu/diary/rss/33016"
source_title: "TeamPCP Supply Chain Campaign: Activity Through 2026-05-24, (Mon, May 25th)"
source_date: 2026-05-25T13:26:06+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1749006590475-4592a5dbf99f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMnx8YXJ0aWZpY2lhbCUyMGludGVsbGlnZW5jZSUyMHRlY2hub2xvZ3klMjBuZXVyYWwlMjBuZXR3b3JrfGVufDB8MHx8fDE3Nzk3MDMxOTh8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "TeamPCP trojanized a verified VS Code extension, a Microsoft PyPI SDK, and 639 npm packages in one week."
tldr_who_at_risk: "Developers and CI/CD pipelines at AI labs and software companies using PyPI, npm, or VS Code Marketplace extensions are most directly exposed."
tldr_actions: ["Rotate all developer and CI/CD credentials that were active during the compromise windows (May 11–24, 2026)", "Audit AI coding agent configuration files for persistence mechanisms injected via malicious extensions or packages", "Stop treating verified-publisher or attestation badges as install-time safety signals; enforce dependency pinning and hash verification"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "Industry News", "LLM Security"]
tags: ["supply-chain-attack", "teamPCP", "github-breach", "openai", "mistral-ai", "pypi", "npm", "vscode-extension", "ci-cd", "credential-harvesting", "disk-wiper", "shai-hulud", "developer-tooling", "oidc-abuse", "trojanized-sdk"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-26T10:20:36+00:00"
feed_source: "sans_isc"
original_url: "https://isc.sans.edu/diary/rss/33016"
pipeline_version: "1.0.0"
---

## Overview

The TeamPCP threat actor executed three simultaneous supply chain escalations within a single week ending May 24, 2026. A trojanized build of the Nx Console VS Code extension (v18.95.0, verified-publisher badge, ~2.2 million installs) was live on the Visual Studio Marketplace for approximately 18 minutes before removal — long enough to auto-update on a GitHub employee endpoint, exfiltrate developer secrets, and enable lateral movement through GitHub's internal CI/CD infrastructure. Approximately 3,800 GitHub-internal repositories were exfiltrated. OpenAI, Grafana Labs, and Mistral AI were named as downstream victims, making this the first publicly confirmed multi-stage operation in the campaign.

In parallel, Microsoft's officially published Azure Durable Functions Python SDK (`durabletask`, ~417,000 monthly downloads) was trojanized across versions 1.4.1–1.4.3 during an approximately 35-minute window on PyPI. Independent reporting characterises the second-stage payload as a Linux disk wiper. A third concurrent wave pushed 639 malicious package versions across 323 packages in the @antv npm ecosystem, including `echarts-for-react` (~1.1M weekly downloads) and `size-sensor` (~4.2M weekly downloads).

## Technical Analysis

The attack chain traces back to OIDC credential harvesting during the May 11 TanStack wave (CVE-2026-45321). Those stolen credentials were later used to publish the malicious Nx Console build through a legitimate, verified-publisher account — demonstrating a credential-reuse pipeline that bypasses marketplace trust signals entirely.

The VS Code extension attack is particularly significant for AI security: coding assistants and AI agents increasingly rely on IDE extensions for context access, file system reads, and API key management. A malicious extension operating with those permissions can silently harvest credentials from `.env` files, AI agent configuration files, and in-memory secrets without triggering conventional endpoint detection.

The Shai-Hulud framework — now reportedly open-sourced on GitHub with copycat forks already active — appears to automate the package poisoning and credential harvesting pipeline, lowering the barrier for follow-on actors.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** Core technique — trojanized packages delivered through trusted registries directly targeted AI lab developer endpoints.
- **AML.T0012 (Valid Accounts):** Harvested OIDC credentials from the TanStack wave were reused to authenticate as a verified publisher.
- **AML.T0047 (ML-Enabled Product or Service):** OpenAI and Mistral AI were named downstream victims, indicating AI services were affected through their developer tooling.
- **LLM05 (Supply Chain Vulnerabilities):** The entire campaign exemplifies OWASP's supply chain risk category for LLM-adjacent systems.
- **LLM06 (Sensitive Information Disclosure):** Repository exfiltration and credential theft from developer endpoints constitute sensitive information disclosure at scale.
- **LLM07 (Insecure Plugin Design):** The VS Code extension attack exploits the broad permissions granted to IDE plugins, a direct analogue to insecure plugin design in AI agent architectures.

## Impact Assessment

Direct victims include GitHub (internal repository exfiltration), OpenAI, Mistral AI, and Grafana Labs. Any developer or CI/CD pipeline that installed affected package versions during the live windows is potentially compromised. The open-sourcing of the Shai-Hulud framework significantly raises the risk of copycat campaigns targeting the same ecosystems.

## Mitigation & Recommendations

1. **Rotate credentials immediately** — any developer or CI/CD token active during May 11–24, 2026 should be considered compromised.
2. **Pin dependencies with hash verification** — do not rely on version ranges or publisher trust badges alone.
3. **Audit AI agent and IDE extension configurations** — inspect for persistence mechanisms, unexpected outbound connections, or modifications to `.env` and configuration files.
4. **Monitor for Shai-Hulud IOCs** — track copycat forks and newly published packages that reference the open-sourced framework.
5. **Restrict extension auto-update policies** in enterprise IDE deployments, particularly where AI coding agents operate with elevated file system or secrets access.

## References

- [SANS Internet Storm Center – TeamPCP Supply Chain Campaign](https://isc.sans.edu/diary/rss/33016)
- BleepingComputer, Help Net Security, OX Security (as cited in source article)
