---
title: "How LiteLLM Turned Developer Machines Into Credential Vaults for Attackers"
date: 2026-04-06T11:45:00+00:00
draft: true

# ── Content metadata ──
summary: "The TeamPCP threat actor compromised LiteLLM packages on PyPI (versions 1.82.7 and 1.82.8), injecting infostealer malware that harvested SSH keys, cloud credentials, and other secrets from developer machines. The attack exploited the AI development supply chain, with cascading exposure through 1,705 dependent packages including major AI libraries like dspy and crawl4ai. This represents a significant escalation in AI-toolchain-targeted supply chain attacks, directly threatening the infrastructure used to build and deploy LLM-powered applications."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/how-litellm-turned-developer-machines.html"
author: "Grid the Grey Editorial"
thumbnail: ""

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["litellm", "supply-chain-attack", "pypi", "credential-theft", "infostealer", "developer-security", "teampcp", "ai-toolchain", "dependency-confusion", "cloud-credentials", "ssh-keys", "open-source-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-13T05:10:51+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/how-litellm-turned-developer-machines.html"
pipeline_version: "1.0.0"
slug: "how-litellm-turned-developer-machines-into-credential-vaults-for-attackers"
---

## Overview

In March 2026, threat actor **TeamPCP** executed a supply chain attack against LiteLLM, one of the most widely used AI development libraries in the Python ecosystem. Malicious code was injected into PyPI package versions 1.82.7 and 1.82.8, turning routine `pip install` or `pip upgrade` operations into credential harvesting events. The attack targeted developer workstations — the richest concentration of plaintext secrets in any enterprise environment — and leveraged LiteLLM's position as a transitive dependency to maximise blast radius.

LiteLLM is a critical abstraction layer used by AI engineers to interface with multiple LLM providers (OpenAI, Anthropic, Azure OpenAI, etc.), making its compromise a direct threat to AI development pipelines globally.

## Technical Analysis

The malware injected into LiteLLM's PyPI packages operated as a classical infostealer but was specifically tuned to the AI development context. Upon installation, it systematically exfiltrated:

- **SSH private keys** (`~/.ssh/`)
- **Cloud provider credentials** — AWS (`~/.aws/credentials`), Azure, GCP service account keys
- **Docker configuration files** (`~/.docker/config.json`)
- **Environment variable files** (`.env` files containing API keys for LLM providers)
- **Shell history and IDE settings** containing cached tokens
- **AI agent memory stores**

The cascade effect was significant. GitGuardian identified **1,705 PyPI packages** configured to automatically pull the compromised LiteLLM versions as dependencies, including:

| Package | Monthly Downloads |
|---|---|
| dspy | 5 million |
| opik | 3 million |
| crawl4ai | 1.4 million |

Organisations that never directly installed LiteLLM were still exposed through transitive dependency resolution. PyPI removed the packages within hours, but the exposure window was sufficient for widespread compromise.

This attack mirrors the **Shai-Hulud campaigns**, where analysis of 6,943 compromised developer machines revealed 33,185 unique secrets — with 59% of compromised systems being CI/CD runners, not personal laptops.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The core technique — injecting malicious code into a widely adopted AI development package to compromise downstream users at scale.
- **AML.T0012 (Valid Accounts):** Harvested credentials enable adversaries to authenticate to cloud services, LLM APIs, and internal infrastructure using legitimate identities.
- **AML.T0047 (ML-Enabled Product or Service):** LiteLLM's role as foundational infrastructure for LLM-integrated products made it an exceptionally high-value target.
- **LLM05 (Supply Chain Vulnerabilities):** The OWASP category directly maps to compromised AI toolchain dependencies.
- **LLM06 (Sensitive Information Disclosure):** LLM API keys, cloud credentials, and model access tokens were the primary harvested assets.

## Impact Assessment

The affected population spans any developer or CI/CD pipeline that installed or updated LiteLLM or its 1,705 dependent packages during the compromise window. The primary risk is **post-compromise lateral movement** — valid cloud credentials allow attackers to access training data, model endpoints, AI agent infrastructure, and production LLM deployments. Organisations building agentic AI systems are at heightened risk given that agent memory stores and orchestration credentials were explicitly targeted.

## Mitigation & Recommendations

1. **Audit installed versions** — Immediately identify any systems that installed LiteLLM 1.82.7 or 1.82.8 and treat them as fully compromised.
2. **Rotate all credentials** on affected machines — SSH keys, AWS/Azure/GCP credentials, LLM API keys, and Docker tokens.
3. **Pin dependency versions** and use hash verification (`--require-hashes`) in `pip` to prevent silent upgrades to malicious versions.
4. **Adopt secrets scanning** tools (e.g., GitGuardian, Trufflehog) across developer environments and CI/CD pipelines.
5. **Isolate CI/CD runners** — given that 59% of compromised machines in analogous campaigns were runners, treat build infrastructure as high-value targets.
6. **Implement SBOM (Software Bill of Materials)** practices to track transitive AI library dependencies.

## References

- [The Hacker News — How LiteLLM Turned Developer Machines Into Credential Vaults for Attackers](https://thehackernews.com/2026/04/how-litellm-turned-developer-machines.html)
