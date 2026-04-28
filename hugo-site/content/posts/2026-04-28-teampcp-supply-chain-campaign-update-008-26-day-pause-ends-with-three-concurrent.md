---
title: "TeamPCP resumes supply chain attacks, poisoning xinference PyPI and triggering a Bitwarden CLI cascade via compromised Docker image."
date: "2026-04-28T05:48:19+00:00"
draft: false
slug: "teampcp-supply-chain-campaign-update-008-26-day-pause-ends-with-three-concurrent"

# ── Content metadata ──
summary: "The TeamPCP supply chain campaign resumed after a 26-day pause with three concurrent compromises targeting Checkmarx KICS (Docker Hub), xinference (a popular AI inference PyPI package), and a cascading compromise of Bitwarden CLI via poisoned CI/CD dependencies. The xinference poisoning is directly AI-security relevant as it targets a widely used LLM/ML model serving framework, while the broader campaign demonstrates sophisticated supply chain attack methodologies that increasingly intersect with AI tooling. The CanisterSprawl npm worm adds credential-harvesting infrastructure that could further compromise AI development pipelines."
source: "SANS Internet Storm Center"
source_url: "https://isc.sans.edu/diary/rss/32926"
source_date: 2026-04-27T14:01:17+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1509479200622-4503f27f12ef?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0019 - Publish Poisoned Datasets", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "TeamPCP resumes supply chain attacks, poisoning xinference PyPI and triggering a Bitwarden CLI cascade via compromised Docker image."
tldr_who_at_risk: "AI/ML developers and DevSecOps teams using xinference, Checkmarx KICS, or npm packages within automated CI/CD pipelines are most directly exposed."
tldr_actions: ["Audit all xinference PyPI installations and verify package integrity against known-good hashes", "Pin Docker image digests explicitly in CI/CD pipelines rather than using mutable 'latest' tags", "Scan npm dependency trees for CanisterSprawl indicators across @automagik, pgserve, @fairwords, and @openwebconcept namespaces"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["supply-chain-attack", "teampcp", "xinference", "pypi-poisoning", "npm-worm", "docker-hub-compromise", "bitwarden-cli", "checkmarx-kics", "canistersprawl", "credential-theft", "unc6780", "ci-cd-compromise", "ml-tooling", "llm-inference"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-28T04:44:59+00:00"
feed_source: "sans_isc"
original_url: "https://isc.sans.edu/diary/rss/32926"
pipeline_version: "1.0.0"
---

## Overview

The TeamPCP supply chain campaign (tracked by Google GTIG as UNC6780) returned to active compromise operations on April 21–22, 2026, ending a 26-day pause that had kept the group in credential-monetization mode through most of April. Three concurrent package compromises landed across npm, PyPI, and Docker Hub in a 24-hour window, with the most AI-security-significant event being the poisoning of the **xinference** PyPI package — a popular open-source framework for serving LLMs and other ML models at scale. The campaign also compromised the **Checkmarx KICS** Docker Hub repository, which cascaded downstream into a CI/CD compromise of **@bitwarden/cli v2026.4.0** via Dependabot automation pulling the malicious `checkmarx/kics:latest` image. Separately, the self-propagating npm worm **CanisterSprawl** was identified across at least 16 malicious package versions.

## Technical Analysis

**xinference PyPI Poisoning:** The xinference package was injected with a TeamPCP marker on April 22. xinference is widely used in AI development environments to serve models including LLaMA, Mistral, and other open-weight LLMs. A poisoned install targeting this package could intercept model API calls, exfiltrate prompts and outputs, or pivot into broader ML infrastructure. TeamPCP publicly denied responsibility, a pattern consistent with deniable attribution strategies observed in prior updates.

**KICS Docker → Bitwarden Cascade:** The `checkmarx/kics:latest` Docker image was compromised on April 22. Bitwarden's Dependabot automation pulled this image as part of its CI/CD pipeline the same evening, resulting in the downstream release of a malicious `@bitwarden/cli v2026.4.0`. This demonstrates how a single poisoned upstream image can propagate through automated dependency management into widely trusted downstream packages.

**CanisterSprawl npm Worm:** Beginning April 21, Socket and StepSecurity identified a self-propagating worm embedded in packages across the @automagik, pgserve, @fairwords, and @openwebconcept namespaces. The worm executes via npm `postinstall` hooks, performs a regex-based sweep harvesting approximately 40 credential categories, and exfiltrates via a dual-channel endpoint. Initial publisher ties link to Namastex Labs and associated accounts.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The xinference PyPI poisoning directly targets an ML model-serving framework, fitting this technique precisely.
- **AML.T0019 (Publish Poisoned Datasets/Packages):** Malicious package versions were published to PyPI, Docker Hub, and npm registries.
- **AML.T0012 (Valid Accounts):** Credential harvesting via CanisterSprawl and the SANDCLOCK stealer supports account takeover enabling further supply chain access.
- **LLM05 (Supply Chain Vulnerabilities):** All three compromise vectors represent classic supply chain risk materialising in AI/ML tooling ecosystems.
- **LLM06 (Sensitive Information Disclosure):** Credential exfiltration from developer environments may expose API keys, model weights, or proprietary training data.

## Impact Assessment

Developers using xinference for LLM serving face the highest AI-specific risk, as a poisoned package could intercept inference traffic or enable lateral movement into model infrastructure. The Bitwarden CLI compromise affects any developer or CI/CD system that updated to v2026.4.0, potentially exposing stored secrets. The CanisterSprawl worm's credential sweep across 40 categories could yield API keys for AI services including OpenAI, Anthropic, and cloud ML platforms.

## Mitigation & Recommendations

1. **Verify xinference installations** — compare installed package hashes against PyPI provenance attestations and roll back to the last known-good version.
2. **Pin Docker images by digest** — replace `checkmarx/kics:latest` references with explicit SHA256 digests in all CI/CD configurations.
3. **Audit Bitwarden CLI** — treat @bitwarden/cli v2026.4.0 as compromised; rotate all secrets accessible from affected CI/CD environments.
4. **Scan npm trees for CanisterSprawl** — check for postinstall hook anomalies in packages from the identified namespaces.
5. **Monitor for SANDCLOCK indicators** — apply UNC6780 threat intelligence to SIEM and EDR tooling.

## References

- SANS ISC Diary: https://isc.sans.edu/diary/rss/32926
- BleepingComputer ADT breach: https://www.bleepingcomputer.com/news/security/adt-confirms-data-breach-after-shinyhunters-leak-threat/
- Help Net Security: https://www.helpnetsecurity.com/2026/04/27/adt-systems-data-breach/
