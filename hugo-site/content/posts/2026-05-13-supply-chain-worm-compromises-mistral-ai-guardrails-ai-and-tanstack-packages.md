---
title: "CVE-2026-45321: Supply Chain Worm Targets Mistral AI"
date: "2026-05-13T08:08:33+00:00"
draft: false
slug: "supply-chain-worm-compromises-mistral-ai-guardrails-ai-and-tanstack-packages"

# ── Content metadata ──
summary: "The TeamPCP threat actor has executed a broad supply chain campaign dubbed Mini Shai-Hulud, injecting credential-stealing malware into npm and PyPI packages from major AI and developer tooling ecosystems including Mistral AI, Guardrails AI, and TanStack. The malware profiles execution environments, exfiltrates cloud, CI, and AI tool credentials, and establishes persistence inside Claude Code and VS Code IDEs. The TanStack compromise alone affected 42 packages and 84 versions, exploiting a chained GitHub Actions attack to inject malicious payloads without stealing npm tokens directly."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html"
source_title: "Mini Shai-Hulud Worm Compromises TanStack, Mistral AI, Guardrails AI & More Packages"
source_date: 2026-05-12T11:46:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1658479657379-e0adb7cb91e8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxtYWx3YXJlJTIwY29tcHV0ZXIlMjB2aXJ1cyUyMGRhcmslMjBoYWNrZXJ8ZW58MHwwfHx8MTc3ODY0ODg4MHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0018 - Backdoor ML Model", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "TeamPCP injected credential-stealing malware into AI and developer npm/PyPI packages via chained GitHub Actions exploits."
tldr_who_at_risk: "Developers and organisations consuming TanStack, Mistral AI, Guardrails AI, UiPath, or OpenSearch packages are directly exposed to credential theft and CI/CD pipeline compromise."
tldr_actions: ["Audit all installed versions of affected packages and update to clean releases immediately", "Rotate all GitHub tokens, cloud provider credentials, and CI/CD secrets on affected machines", "Review GitHub Actions workflows for unauthorised modifications and restrict pull_request_target trigger permissions"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Agentic AI", "Industry News"]
tags: ["supply-chain-attack", "npm-malware", "pypi-malware", "credential-stealer", "mistral-ai", "guardrails-ai", "tanstack", "github-actions", "claude-code", "teamPCP", "mini-shai-hulud", "cve-2026-45321", "persistence", "ci-cd-compromise"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-13T05:08:34+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html"
pipeline_version: "1.0.0"
---

## Overview

A threat actor tracked as TeamPCP has launched a sweeping supply chain campaign, dubbed **Mini Shai-Hulud**, targeting npm and PyPI packages from TanStack, Mistral AI, Guardrails AI, UiPath, and OpenSearch. The campaign introduces an obfuscated credential stealer capable of harvesting secrets from cloud providers, cryptocurrency wallets, AI tooling, messaging applications, and CI/CD systems. The TanStack compromise has been assigned **CVE-2026-45321** (CVSS 9.6), impacting 42 packages and 84 versions.

## Technical Analysis

The attack uses two distinct infection vectors depending on the target package ecosystem:

**TanStack cluster:** A malicious JavaScript file (`router_init.js`) is embedded directly in the package tarball. An optional dependency pointing to a GitHub-hosted package is added; that dependency contains a `prepare` lifecycle hook which executes the payload via the **Bun runtime**. The initial staging exploits a chained GitHub Actions vulnerability — specifically the `pull_request_target` trigger combined with Actions cache poisoning and runtime memory extraction of an OIDC token from the runner process.

**Mistral AI cluster:** Follows an earlier TeamPCP pattern — the `package.json` preinstall hook is replaced to invoke `node setup.mjs`, which downloads Bun and runs the same JavaScript stealer.

Exfiltration routes include:
- **Primary:** Data sent to `filev2.getsession[.]org`, leveraging Session Protocol infrastructure to avoid enterprise blocklists.
- **Fallback:** Encrypted data committed to attacker-controlled GitHub repositories using stolen tokens via the GitHub GraphQL API, attributed to `claude@users.noreply.github.com`.

Persistence mechanisms include hooks injected into **Claude Code** and **VS Code** IDE startup sequences, a `gh-token-monitor` service for continuous GitHub token re-exfiltration, and two rogue GitHub Actions workflows that serialise repository secrets to JSON and upload them to `api.masscan[.]cloud`.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** Core attack vector — malicious code injected into widely-used AI and developer packages.
- **AML.T0047 (ML-Enabled Product or Service):** Mistral AI and Guardrails AI packages directly targeted, compromising AI toolchain integrity.
- **AML.T0018 (Backdoor ML Model):** Persistence in Claude Code IDE creates a persistent foothold within AI development workflows.
- **LLM05 (Supply Chain Vulnerabilities):** Package-level compromise of AI SDK dependencies represents a direct OWASP LLM supply chain risk.
- **LLM06 (Sensitive Information Disclosure):** Credential and secret exfiltration from AI development environments.

## Impact Assessment

The blast radius is significant. Any developer who installed affected TanStack, Mistral AI, or Guardrails AI package versions may have had cloud credentials, GitHub tokens, CI/CD secrets, and AI API keys exfiltrated. Organisations using these packages in automated pipelines face compounded risk — injected GitHub Actions workflows could propagate secrets theft across entire repository ecosystems. The use of Session Protocol infrastructure for exfiltration reduces detection likelihood in enterprise environments that permit the domain.

## Mitigation & Recommendations

1. **Immediately audit** installed versions of TanStack, Mistral AI, Guardrails AI, UiPath, and OpenSearch packages against the confirmed malicious version list.
2. **Rotate all secrets** — GitHub tokens, cloud provider API keys, CI/CD environment variables, and AI platform credentials on any affected systems.
3. **Review GitHub Actions workflows** across all repositories for unauthorised additions; restrict `pull_request_target` trigger usage and enforce least-privilege OIDC token scopes.
4. **Scan for persistence artefacts** in Claude Code and VS Code extension directories and startup hooks.
5. **Block or monitor** outbound traffic to `filev2.getsession[.]org` and `api.masscan[.]cloud`.
6. **Enable npm and PyPI provenance attestation** where available to reduce future supply chain exposure.

## References

- [The Hacker News — Mini Shai-Hulud Worm Compromises TanStack, Mistral AI, Guardrails AI & More Packages](https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html)
