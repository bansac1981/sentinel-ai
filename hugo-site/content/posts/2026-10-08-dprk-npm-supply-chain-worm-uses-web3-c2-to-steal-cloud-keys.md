---
title: "DPRK npm Supply Chain Worm Uses Web3 C2 to Steal Cloud Keys"
date: "2026-10-08T18:29:46+00:00"
draft: false 
slug: "dprk-npm-supply-chain-worm-uses-web3-c2-to-steal-cloud-keys"

# ── Content metadata ──
summary: "North Korea-affiliated threat actors have escalated software supply chain attacks by embedding a self-propagating npm worm, ChainDrop, across over 400 packages to harvest ephemeral cloud IAM credentials and CI/CD tokens. The campaign introduces Web3-based command-and-control via EtherHiding smart contracts, enabling attackers to dynamically update exfiltration endpoints across entire botnets without altering malware binaries. Targeted projects include AI frameworks such as Mastra AI, raising direct concerns for AI development pipelines and their cloud infrastructure."
source: "Palo Alto Unit 42"
source_url: "https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks"
source_title: "Evolution of Web3 in Cloud Supply Chain Attacks"
source_date: 2026-10-07T22:00:16+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1581488066919-b876dc3a1bea?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNXx8Y29udGFtaW5hdGlvbiUyMGhhem1hdCUyMHdhcm5pbmclMjBhYnN0cmFjdHxlbnwwfDB8fHwxNzkxNDYxOTYxfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0109 - AI Supply Chain Rug Pull", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "DPRK-linked actors deployed a self-spreading npm worm using blockchain smart contracts as dynamic C2 infrastructure."
tldr_who_at_risk: "Software developers and CI/CD pipeline operators are most exposed due to privileged IAM credential access during dependency resolution."
tldr_actions: ["Block all Web3 and blockchain network traffic at the perimeter if your organisation has no legitimate need for it", "Audit npm dependencies for unexpected preinstall scripts and enforce package integrity checks in CI/CD runners", "Rotate and scope all cloud IAM credentials used in build pipelines and implement short-lived OIDC federation where possible"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News"]
tags: ["supply-chain-attack", "npm-worm", "web3-c2", "dprk", "cloud-credentials", "iam-theft", "cicd-security", "blockchain-c2", "etherhiding", "alluring-pisces", "open-source-security", "chaindrop"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-10-08T12:19:21+00:00"
feed_source: "unit42"
original_url: "https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks"
pipeline_version: "2.1.0"
---

## Overview

Unit 42 researchers have documented a significant escalation in North Korea-affiliated supply chain operations, centred on the ChainDrop npm worm and the broader PolinRider campaign. What distinguishes these attacks is the replacement of static, hardcoded command-and-control (C2) endpoints with Web3 smart contracts, allowing operators to dynamically redirect exfiltration traffic with a single blockchain transaction — making traditional domain-based blocking largely ineffective. Notably, targeted projects include Mastra AI, a framework used in AI agent development, which introduces a direct pathway from open-source AI tooling into enterprise cloud environments.

## Technical Analysis

ChainDrop, attributed to the Shai-Hulud malware family, propagated through over 400 npm packages — including popular dependencies such as `keyv` and `cacheable-request`. Upon package installation, a malicious `preinstall` script is executed that:

1. Downloads a custom Bun runtime to bypass standard Node.js detection heuristics.
2. Launches an obfuscated credential harvester that scrapes both disk-resident files and in-memory build process data.
3. Captures ephemeral cloud IAM keys, CI/CD worker tokens, and short-lived OIDC federation credentials before the runner terminates.

For C2 resilience, ChainDrop implements **EtherHiding** — a technique in which the malware queries Ethereum smart contract transaction data to retrieve dynamically encrypted exfiltration endpoints. This means infrastructure can be completely rotated by the attacker without touching a single malware binary. Persistent task hooks are then injected to ensure re-execution on subsequent build cycles.

Alluring Pisces (also tracked as Sapphire Sleet or Midnight Neptune), the DPRK-affiliated group assessed responsible, has applied these techniques across campaigns targeting Axios, Mastra AI, and Rust's `arrayref` crate.

## Framework Mapping

- **AML.T0010 – AI Supply Chain Compromise**: Malicious packages inserted into open-source ecosystems used by AI developers.
- **AML.T0115 – Publish Poisoned AI Artifacts**: Worm-infected packages published to npm, targeting AI framework dependencies.
- **AML.T0083 – Credentials from AI Agent Configuration**: Harvesting of IAM keys and tokens from developer and build environments.
- **LLM05 – Supply Chain Vulnerabilities**: Compromise of upstream packages affecting downstream AI tooling consumers.
- **LLM06 – Sensitive Information Disclosure**: Exfiltration of cloud identity tokens and deployment secrets.

## Impact Assessment

Organisations consuming npm packages in automated CI/CD pipelines face the highest exposure. Harvested IAM credentials can enable lateral movement into cloud environments, privilege escalation, and long-term persistence. The targeting of AI frameworks such as Mastra AI means AI development teams and MLOps pipelines are not insulated from this threat. The use of blockchain C2 significantly raises the cost of defender-side infrastructure takedowns, extending attacker dwell time.

## Mitigation & Recommendations

- **Block Web3 traffic proactively**: If blockchain connectivity is not a business requirement, implement network-layer blocks against known Web3 RPC endpoints and Ethereum nodes.
- **Enforce preinstall script controls**: Use `.npmrc` configuration (`ignore-scripts=true`) and enforce this policy across all CI/CD runners.
- **Adopt short-lived credentials**: Replace long-lived IAM keys in pipelines with OIDC federation and role assumption with minimal TTLs.
- **Monitor build process memory**: Deploy endpoint detection capable of identifying anomalous process injection or credential scraping during build execution.
- **Audit transitive dependencies**: Implement software composition analysis (SCA) tooling to surface unexpected or newly introduced packages in the dependency graph.

## References

- [Unit 42: Evolution of Web3 in Cloud Supply Chain Attacks](https://unit42.paloaltonetworks.com/web3-cloud-supply-chain-attacks)
