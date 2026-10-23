---
title: "LiteLLM Supply Chain Attack via Poisoned PyPI Packages"
date: 2026-10-23T10:20:54+00:00
draft: true
slug: "litellm-supply-chain-attack-via-poisoned-pypi-packages"

# ── Content metadata ──
summary: "Attackers compromised GitHub CLI OAuth tokens to inject malicious packages into the LiteLLM distribution chain via PyPI and Docker, a widely-used LLM proxy and routing library. Because LiteLLM sits at the core of many AI/ML production stacks, this supply chain compromise poses a significant risk to downstream AI applications and the organisations operating them. The incident underscores the fragility of OAuth-based developer tooling as an entry vector into high-impact AI infrastructure."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/litellm-compromised-in-fresh-supply-chain-attack"
source_title: "LiteLLM Compromised in Fresh Supply Chain Attack"
source_date: 2026-10-23T08:10:46+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1465929639680-64ee080eb3ed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxM3x8bGlicmFyeSUyMGJvb2tzJTIwa25vd2xlZGdlJTIwcm93c3xlbnwwfDB8fHwxNzkyNzUwODU0fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0012 - Valid Accounts", "AML.T0109 - AI Supply Chain Rug Pull"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Attackers used stolen GitHub CLI OAuth tokens to push malicious LiteLLM packages to PyPI and Docker."
tldr_who_at_risk: "Any developer or organisation consuming LiteLLM via PyPI or Docker is at risk of running backdoored AI infrastructure components."
tldr_actions: ["Audit and pin LiteLLM package versions; verify checksums against known-good releases", "Rotate any secrets or credentials stored in environments running potentially compromised LiteLLM versions", "Enable dependency scanning and provenance verification in CI/CD pipelines for all AI/ML dependencies"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["litellm", "supply-chain-attack", "pypi", "docker", "github-oauth", "token-compromise", "malicious-package", "llm-infrastructure", "open-source-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-23T10:20:54+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/litellm-compromised-in-fresh-supply-chain-attack"
pipeline_version: "2.1.0"
---

## Overview

In October 2026, threat actors successfully compromised the LiteLLM open-source project — a widely deployed LLM proxy and request-routing library — through a supply chain attack targeting its PyPI and Docker distribution channels. Attackers leveraged compromised GitHub CLI OAuth tokens to gain write access, enabling them to push and approve malicious package releases without triggering standard maintainer review controls. LiteLLM is a critical piece of infrastructure for many AI-powered applications, making this compromise especially high-stakes for the broader AI/ML community.

## Technical Analysis

The attack vector centred on GitHub CLI OAuth token compromise. OAuth tokens issued to the GitHub CLI tool carry significant repository permissions; once stolen or leaked, they can be used to authenticate as the legitimate token holder and perform repository and CI/CD pipeline actions — including publishing release artefacts to external registries like PyPI and Docker Hub.

By exploiting these tokens, the threat actors were able to:

1. **Push malicious package versions** to PyPI under the legitimate `litellm` namespace, making the packages appear authentic to automated dependency resolution tools.
2. **Publish tampered Docker images**, potentially backdooring containerised deployments of LiteLLM used in production AI serving infrastructure.
3. **Approve their own malicious contributions**, bypassing peer-review controls that depend on trusted maintainer accounts.

Because package managers such as `pip` resolve to the latest published version by default unless versions are pinned, any organisation running `pip install litellm` without strict version pinning may have inadvertently installed the malicious build during the exposure window.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0010 – AI Supply Chain Compromise | Core classification: attacker compromised upstream AI tooling distribution |
| MITRE ATLAS | AML.T0115 – Publish Poisoned AI Artifacts | Malicious packages pushed to PyPI and Docker |
| MITRE ATLAS | AML.T0012 – Valid Accounts | OAuth token abuse grants attacker legitimate-appearing access |
| MITRE ATLAS | AML.T0109 – AI Supply Chain Rug Pull | Trusted package subverted post-establishment of community trust |
| OWASP LLM | LLM05 – Supply Chain Vulnerabilities | Compromise of a foundational LLM infrastructure library |

## Impact Assessment

LiteLLM is used extensively across AI development teams and production deployments as an abstraction layer over LLM APIs (OpenAI, Anthropic, Cohere, etc.). A backdoored version of the library could:

- **Exfiltrate API keys** for downstream LLM providers routed through the proxy.
- **Intercept or manipulate model inputs and outputs** at the proxy layer.
- **Establish persistence** within AI serving infrastructure.
- **Affect downstream AI agents and pipelines** that depend on LiteLLM for routing.

Organisations operating in regulated industries or handling sensitive data through LiteLLM-powered applications face the highest exposure.

## Mitigation & Recommendations

- **Pin dependency versions** in `requirements.txt` and `pyproject.toml`; avoid unpinned `pip install litellm`.
- **Verify package integrity** using checksums or tools like `pip-audit` and `sigstore` for provenance validation.
- **Audit running environments** for signs of compromise; rotate all LLM provider API keys accessible to LiteLLM processes.
- **Restrict OAuth token scopes** for developer CLI tooling and implement token expiry policies.
- **Monitor PyPI and Docker Hub** release feeds for unexpected version bumps on critical AI dependencies.
- **Enable OIDC-based trusted publishing** on PyPI to reduce reliance on long-lived tokens.

## References

- [LiteLLM Compromised in Fresh Supply Chain Attack – SecurityWeek](https://www.securityweek.com/litellm-compromised-in-fresh-supply-chain-attack)
