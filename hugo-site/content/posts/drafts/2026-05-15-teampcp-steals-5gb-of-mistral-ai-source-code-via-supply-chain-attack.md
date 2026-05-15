---
title: "TeamPCP Steals 5GB of Mistral AI Source Code via Supply Chain Attack"
date: 2026-05-15T16:45:54+00:00
draft: true
slug: "teampcp-steals-5gb-of-mistral-ai-source-code-via-supply-chain-attack"

# ── Content metadata ──
summary: "The TeamPCP threat group has compromised Mistral AI's codebase management system via the Shai-Hulud software supply chain attack, stealing approximately 5GB of internal repositories covering training, fine-tuning, benchmarking, and inference pipelines. The hackers are demanding $25,000 for nearly 450 repositories or threatening to leak them publicly within a week. Mistral AI confirmed the breach but stated that core repositories, hosted services, managed user data, and research environments were not affected."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/teampcp-hackers-advertise-mistral-ai-code-repos-for-sale/"
source_title: "TeamPCP hackers advertise Mistral AI code repos for sale"
source_date: 2026-05-14T22:50:36+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1582775764915-6b78a5e9904d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxNXx8c3VwcGx5JTIwY2hhaW4lMjBzb2Z0d2FyZSUyMHBhY2thZ2VzfGVufDB8MHx8fDE3Nzg4NjM1NTR8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0044 - Full ML Model Access", "AML.T0057 - LLM Data Leakage", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM10 - Model Theft"]

# ── TL;DR ──
tldr_what: "TeamPCP stole 5GB of Mistral AI repos via supply chain attack and is selling them for $25K."
tldr_who_at_risk: "AI companies and developers using compromised Mistral AI SDK packages or dependent on TanStack/npm ecosystem packages are most directly exposed."
tldr_actions: ["Audit all dependencies on Mistral AI SDK packages and pin to verified clean versions", "Rotate CI/CD credentials and audit pipeline access logs for unauthorised activity", "Monitor dark web and hacker forums for leaked Mistral AI repository contents that could enable targeted attacks"]

# ── Taxonomies ──
categories: ["Supply Chain", "Model Theft", "LLM Security", "Industry News"]
tags: ["mistral-ai", "teampcp", "supply-chain-attack", "source-code-theft", "shai-hulud", "npm-compromise", "ci-cd-credentials", "sdk-poisoning", "data-extortion", "llm-infrastructure"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-15T16:45:54+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/teampcp-hackers-advertise-mistral-ai-code-repos-for-sale/"
pipeline_version: "1.0.0"
---

## Overview

The TeamPCP hacker group has advertised nearly 450 internal Mistral AI repositories for sale on a hacker forum, demanding $25,000 or threatening a full public leak within one week. The breach, confirmed by Mistral AI, originated from the broader Shai-Hulud software supply chain attack — an incident that initially compromised official packages from TanStack and Mistral AI via stolen CI/CD credentials, before cascading across hundreds of projects on the npm and PyPI registries, including UiPath, Guardrails AI, and OpenSearch.

The stolen data reportedly totals approximately 5 gigabytes and covers repositories related to model training, fine-tuning, benchmarking, model delivery, and inference pipelines — assets that represent significant intellectual property and potential attack surface intelligence for adversaries.

## Technical Analysis

The attack chain began with the compromise of CI/CD credentials, allowing threat actors to inject malicious code into legitimate Mistral AI and TanStack packages distributed via npm. A developer device at Mistral AI was subsequently impacted when the poisoned packages were pulled into internal workflows, granting TeamPCP access to the codebase management system.

From that foothold, the attackers exfiltrated internal repositories through what appears to be legitimate developer access pathways — a technique consistent with MITRE ATLAS AML.T0012 (Valid Accounts) combined with AML.T0010 (ML Supply Chain Compromise). The SDK packages were contaminated for a brief window before Mistral detected and remediated the compromise.

Mistral's forensic investigation concluded that core model repositories, hosted services, managed user data, and research environments were not exfiltrated. However, the stolen repositories covering training and fine-tuning pipelines could provide adversaries with sufficient detail to craft targeted poisoning or evasion attacks against Mistral's model ecosystem.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The attack vector was explicitly a compromised package registry supply chain affecting CI/CD pipelines.
- **AML.T0044 (Full ML Model Access):** Stolen repositories covering training, fine-tuning, and inference pipelines approach full model lifecycle access.
- **AML.T0057 (LLM Data Leakage):** Internal source code and pipeline data were exfiltrated from a leading LLM provider.
- **LLM05 (Supply Chain Vulnerabilities):** The root cause is a compromised dependency in the software supply chain.
- **LLM10 (Model Theft):** The advertised sale of model-adjacent code constitutes an attempted intellectual property theft.

## Impact Assessment

The immediate impact is on Mistral AI's competitive position and security posture — exposure of training and fine-tuning pipeline code could enable competitors or adversaries to replicate proprietary methodologies. Downstream SDK consumers face residual risk from the brief contamination window. The broader Shai-Hulud attack affected hundreds of projects, meaning the blast radius extends well beyond Mistral AI itself. The extortion model — pay or face public leak — creates urgency that could pressure organisations into poor decisions.

## Mitigation & Recommendations

1. **Audit SDK dependencies:** Any project consuming Mistral AI SDK packages should verify package integrity against known-good hashes and update to post-incident releases.
2. **Rotate CI/CD credentials immediately:** All credentials associated with affected pipelines should be considered compromised and rotated.
3. **Implement package signing and verification:** Adopt Sigstore or equivalent signing for all published packages to detect future tampering.
4. **Monitor for leaked repository use:** Track dark web forums and threat intelligence feeds for evidence of the stolen repositories being used to craft targeted attacks.
5. **Audit developer device access:** Restrict developer machines from direct access to production codebase management systems without additional authentication controls.

## References

- [TeamPCP hackers advertise Mistral AI code repos for sale — BleepingComputer](https://www.bleepingcomputer.com/news/security/teampcp-hackers-advertise-mistral-ai-code-repos-for-sale/)
