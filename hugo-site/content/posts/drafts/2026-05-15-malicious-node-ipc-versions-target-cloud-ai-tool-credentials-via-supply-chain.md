---
title: "Malicious node-ipc Versions Target Cloud, AI Tool Credentials via Supply Chain Backdoor"
date: 2026-05-15T16:47:26+00:00
draft: true
slug: "malicious-node-ipc-versions-target-cloud-ai-tool-credentials-via-supply-chain"

# ── Content metadata ──
summary: "Three versions of the widely-used node-ipc npm package were found to contain obfuscated stealer/backdoor payloads published by an unauthorised maintainer account. The malware harvests 90 categories of developer secrets \u2014 including Claude AI and Kiro IDE configurations, AWS, Azure, and GCP credentials \u2014 and exfiltrates them via HTTPS and DNS tunnelling to an attacker-controlled domain. The compromise is notable for bypassing npm lifecycle hooks entirely and, in one version, targeting a specific developer via pre-computed SHA-256 fingerprinting."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/05/stealer-backdoor-found-in-3-node-ipc.html"
source_title: "Stealer Backdoor Found in 3 Node-IPC Versions Targeting Developer Secrets"
source_date: 2026-05-14T17:22:43+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxiYWNrZG9vciUyMHNoYWRvdyUyMGhhY2tpbmclMjBzZXJ2ZXJ8ZW58MHwwfHx8MTc3ODg2MzY0Nnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Three node-ipc npm versions backdoored to steal developer and AI tool credentials via obfuscated payload."
tldr_who_at_risk: "Developers using node-ipc@9.1.6, 9.2.3, or 12.0.1 are directly exposed, with cloud and AI platform credentials at immediate risk of exfiltration."
tldr_actions: ["Audit package.json and lock files for node-ipc versions 9.1.6, 9.2.3, and 12.0.1 and remove immediately", "Rotate all cloud credentials, SSH keys, GitHub tokens, and AI tool API keys on any system that loaded these versions", "Block or monitor DNS and HTTPS traffic to sh.azurestaticprovider[.]net and investigate for exfiltration activity"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["supply-chain-attack", "npm", "node-ipc", "credential-theft", "developer-secrets", "backdoor", "stealer-malware", "cloud-credentials", "ai-tool-credentials", "dns-exfiltration", "malicious-package"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-15T16:47:26+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/05/stealer-backdoor-found-in-3-node-ipc.html"
pipeline_version: "1.0.0"
---

## Overview

Three versions of the popular npm package **node-ipc** — `9.1.6`, `9.2.3`, and `12.0.1` — have been confirmed as malicious following analysis by Socket and StepSecurity. The packages were published by an account named `atiertant`, with no prior publish history tied to the package, raising immediate suspicion of either an account takeover or an authorised-but-malicious maintainer insertion. The original author is `riaevangelist`, who had not updated the package since August 2024 — a 21-month gap that may have made the compromise easier to go undetected.

Node-ipc is a well-established inter-process communication library for Node.js with substantial download volumes, making it a high-value target for supply chain attackers.

## Technical Analysis

Unlike many prior supply chain attacks that exploit npm lifecycle hooks (`preinstall`, `postinstall`), this backdoor appends its payload directly as an **Immediately Invoked Function Expression (IIFE)** to `node-ipc.cjs`. This means the malware executes unconditionally on every `require('node-ipc')` call, bypassing many standard security scanners that focus on lifecycle script analysis.

Key behavioural characteristics:

- **Environment fingerprinting**: The payload enumerates the host environment before proceeding.
- **SHA-256 targeting (v12.0.1 only)**: Version 12.0.1 performs a SHA-256 hash of the primary module path and compares it against a hard-coded value assembled from eight obfuscated table fragments. If the hash does not match, the payload is entirely inert — indicating surgical, targeted attack capability against a specific developer or project.
- **Broad credential harvesting**: 90 credential categories targeted, including AWS, GCP, Azure, SSH keys, Kubernetes tokens, GitHub CLI configs, **Claude AI and Kiro IDE settings**, Terraform state, database passwords, and shell history.
- **Dual exfiltration channels**: Stolen data is GZIP-compressed and sent via HTTPS POST to `sh.azurestaticprovider[.]net`, with a secondary channel encoding archive chunks as DNS TXT record queries for covert exfiltration.

The inclusion of Claude AI and Kiro IDE credentials is particularly significant for AI security, as these represent access tokens to LLM services and AI development environments that could be used for model abuse, prompt injection at scale, or downstream pipeline compromise.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise)**: The attack directly targets the software supply chain used by AI developers, with credentials for AI platforms explicitly in scope.
- **AML.T0012 (Valid Accounts)**: The attacker leveraged either compromised or newly-added maintainer credentials to publish malicious package versions.
- **AML.T0057 (LLM Data Leakage)**: Harvested Claude AI API tokens and IDE configurations represent direct LLM credential exposure.
- **LLM05 (Supply Chain Vulnerabilities)**: A textbook supply chain attack affecting developers building LLM-integrated applications.
- **LLM06 (Sensitive Information Disclosure)**: AI platform credentials and configurations are among the primary targets.

## Impact Assessment

Any developer or CI/CD pipeline that installed or loaded the three affected versions is potentially compromised. The breadth of targeted credentials — spanning cloud infrastructure, AI platforms, and developer tooling — means a single infection could yield lateral movement across cloud environments and unauthorised access to LLM APIs. The SHA-256 targeting in v12.0.1 suggests at least one campaign is precision-targeted, raising the possibility of corporate espionage.

## Mitigation & Recommendations

1. **Immediately remove** node-ipc versions 9.1.6, 9.2.3, and 12.0.1 from all projects and pipelines.
2. **Rotate all credentials** accessible from affected machines: cloud provider keys, SSH keys, GitHub tokens, Kubernetes service accounts, and AI platform API keys (including Claude and similar).
3. **Block network access** to `sh.azurestaticprovider[.]net` and monitor DNS query logs for anomalous TXT record lookups.
4. **Audit maintainer lists** on internal and third-party npm packages; restrict publish rights to verified accounts.
5. **Implement runtime dependency integrity checks** and consider tools like Socket or similar SCA platforms for continuous supply chain monitoring.

## References

- [The Hacker News — Stealer Backdoor Found in 3 Node-IPC Versions](https://thehackernews.com/2026/05/stealer-backdoor-found-in-3-node-ipc.html)
