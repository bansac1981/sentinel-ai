---
title: "PhantomRaven npm Stealer Built With LLM Targets Dev Secrets"
date: 2026-09-18T10:03:10+00:00
draft: true
slug: "phantomraven-npm-stealer-built-with-llm-targets-dev-secrets"

# ── Content metadata ──
summary: "A threat actor operating under bug bounty personas deployed over 100 malicious npm packages containing an LLM-generated JavaScript stealer, PhantomRaven, targeting developer credentials and CI/CD secrets. CrowdStrike assessed with high confidence that the malware was written using a large language model, evidenced by verbose comments, placeholder code, and statistical token-analysis patterns. The operation highlights the growing use of AI-assisted malware development to lower the technical barrier for financially motivated attackers."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/claimed-bug-bounty-hunter-likely-used.html"
source_title: "Claimed Bug Bounty Hunter Likely Used LLM to Build PhantomRaven npm Stealer"
source_date: 2026-09-18T09:18:03+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1522442676585-c751dab71864?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxzY3JvbGwlMjBtYW51c2NyaXB0JTIwYW5jaWVudCUyMGtub3dsZWRnZXxlbnwwfDB8fHwxNzg5NzI1NzkwfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0047 - AI-Enabled Product or Service", "AML.T0065 - LLM Prompt Crafting", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "LLM-generated PhantomRaven stealer distributed via 100+ malicious npm packages targeting developer credentials."
tldr_who_at_risk: "Software developers using npm are most exposed, particularly those working in CI/CD pipelines using GitHub Actions, GitLab CI, Jenkins, or CircleCI."
tldr_actions: ["Audit npm dependencies for typosquatted or slopsquatted package names before installation", "Enable secret scanning and restrict CI/CD environment variable exposure in pipelines", "Monitor npm package installs for preinstall script execution and outbound network calls to unknown hosts"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News"]
tags: ["phantomraven", "npm-stealer", "llm-generated-malware", "software-supply-chain", "javascript-malware", "typosquatting", "slopsquatting", "ci-cd-secrets", "bug-bounty-abuse", "crowdstrike"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-18T10:03:10+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/claimed-bug-bounty-hunter-likely-used.html"
pipeline_version: "2.1.0"
---

## Overview

A financially motivated threat actor has been distributing a JavaScript information stealer dubbed **PhantomRaven** through more than 100 malicious packages on the npm registry, in a campaign active since at least November 2022. CrowdStrike's Counter Adversary Operations assessed with high confidence that the malware was written using a large language model (LLM), citing verbose inline comments, placeholder code blocks, and statistical token-analysis patterns consistent with LLM output. The case marks one of the more forensically documented instances of AI-assisted malware development in a real-world supply chain attack.

## Technical Analysis

PhantomRaven was deployed via a **slopsquatting and typosquatting** strategy, uploading packages with names closely resembling legitimate libraries (e.g., `transform-jsbi-to-bigint`, `sort-imports-es6-autofix`). The packages themselves avoided direct embedding of malicious payloads to evade static scanning; instead, they retrieved a **remote dynamic dependency (RDD)** from an attacker-controlled server at install time.

Once the RDD executed, PhantomRaven performed the following collection actions:
- Scanned for email addresses in the developer environment
- Collected system fingerprint data including public IP address
- Harvested Git and npm configuration values (usernames, emails)
- Extracted CI/CD environment variables for GitHub Actions, GitLab CI, Jenkins, and CircleCI
- Exfiltrated data to an attacker-controlled command-and-control server

The operator also attempted to push a PyPI variant with code similarities to PhantomRaven, suggesting cross-ecosystem ambitions. In August 2025, the actor claimed to have leveraged one of their own malicious packages to achieve RCE on a target machine via the `preinstall` script hook — framing it as a bug bounty finding.

The LLM attribution is notable: CrowdStrike applied statistical token-analysis to the malware's source code and identified patterns — including redundant comments, boilerplate structural patterns, and placeholder variables — characteristic of LLM-generated code rather than hand-authored malware.

## Framework Mapping

- **AML.T0010 (AI Supply Chain Compromise):** Malicious packages injected into the npm ecosystem mirror canonical AI/ML supply chain attack vectors.
- **AML.T0047 (AI-Enabled Product or Service):** The malware itself was likely generated using an LLM, lowering the development barrier for the threat actor.
- **AML.T0065 (LLM Prompt Crafting):** Implicit in the actor's use of an LLM to produce functional, structured malware code.
- **AML.T0115 (Publish Poisoned AI Artifacts):** The npm packages function as poisoned artifacts distributed to unsuspecting developers.
- **LLM05 (Supply Chain Vulnerabilities):** The registry-based distribution method exploits trust in public package ecosystems.
- **LLM06 (Sensitive Information Disclosure):** Stolen CI/CD secrets and developer credentials represent direct sensitive information exfiltration.

## Impact Assessment

Developers consuming npm packages — particularly those operating automated CI/CD pipelines — are directly at risk. The theft of GitHub credentials, CI/CD environment secrets, and system fingerprints could enable lateral movement, repository compromise, or further supply chain attacks downstream. CrowdStrike noted that stolen data has not appeared on stealer log shops, suggesting the operator may be using the intelligence primarily to identify bug bounty targets rather than for immediate resale — though this does not reduce the severity of the underlying exposure.

## Mitigation & Recommendations

- **Verify package names carefully** before installation; use tooling that detects typosquatting variations.
- **Block or alert on preinstall/postinstall script execution** in CI/CD environments unless explicitly required.
- **Restrict CI/CD secret scope** using least-privilege environment variable access controls.
- **Enable egress monitoring** on build agents to detect unexpected outbound connections during package installation.
- **Scan for LLM-generated code indicators** in dependency audits — verbose comments and placeholder variables can be a signal worth investigating.

## References

- [The Hacker News – Claimed Bug Bounty Hunter Likely Used LLM to Build PhantomRaven npm Stealer](https://thehackernews.com/2026/09/claimed-bug-bounty-hunter-likely-used.html)
