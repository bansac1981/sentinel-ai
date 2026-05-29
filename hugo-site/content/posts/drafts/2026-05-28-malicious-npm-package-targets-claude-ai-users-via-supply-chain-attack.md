---
title: "Malicious npm Package Targets Claude AI Users via Supply Chain Attack"
date: 2026-05-28T23:58:47+00:00
draft: false 
slug: "malicious-npm-package-targets-claude-ai-users-via-supply-chain-attack"

# ── Content metadata ──
summary: "A malicious npm package named 'mouse5212-super-formatter' was discovered exfiltrating files from Anthropic's Claude AI user directory by authenticating to a threat actor-controlled GitHub repository. The package disguised itself as a legitimate archive utility while silently uploading all local workspace files during the postinstall phase. Notably, the attacker's poor operational security \u2014 including a leaked GitHub token \u2014 suggests AI-generated malware with minimal human oversight, pointing to a growing trend of low-skill threat actors leveraging AI to produce supply chain malware."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/05/malicious-npm-package-stole-files-from.html"
source_title: "Malicious npm Package Stole Files From Claude AI User Directory via GitHub"
source_date: 2026-05-27T15:44:29+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1549194388-f61be84a6e9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMHx8c3VwcGx5JTIwY2hhaW4lMjBzb2Z0d2FyZSUyMHBhY2thZ2VzfGVufDB8MHx8fDE3ODAwMTI3Mjd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0057 - LLM Data Leakage", "AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Malicious npm package silently exfiltrated Claude AI workspace files to attacker-controlled GitHub repository."
tldr_who_at_risk: "Developers who install unvetted npm packages while using Anthropic's Claude AI tooling are most exposed, as the malware targets Claude's dedicated file upload/output directory."
tldr_actions: ["Audit npm dependencies for 'mouse5212-super-formatter' and remove immediately", "Rotate any GitHub tokens or credentials present in affected environment variables", "Enforce npm package vetting policies and monitor postinstall script behaviour in CI/CD pipelines"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["npm-malware", "supply-chain-attack", "claude-ai", "anthropic", "data-exfiltration", "github", "information-stealer", "ai-generated-malware", "postinstall-hook", "opsec-failure"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-28T23:58:47+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/05/malicious-npm-package-stole-files-from.html"
pipeline_version: "1.0.0"
---

## Overview

Cybersecurity researchers at OX Security have uncovered a malicious npm package — `mouse5212-super-formatter` — specifically designed to steal files from the user data directory leveraged by Anthropic's Claude AI assistant. The campaign, dubbed **Malware-Slop**, represents a targeted supply chain attack against developers using Claude's tooling, and highlights an emerging trend of AI-assisted malware creation paired with poor attacker operational security.

The package was uploaded to npm on May 26, 2026, and recorded approximately 676 downloads before being flagged. It remains available on the npm registry at time of reporting.

## Technical Analysis

The package masquerades as an internal *archive deployment sync* utility. Its malicious logic executes during the `postinstall` lifecycle hook — a common technique for achieving code execution at installation time without raising immediate suspicion.

Upon execution, the malware:

1. **Authenticates to GitHub** using a token sourced from the victim's environment variables, falling back to a hard-coded token if none is found.
2. **Checks for a target repository** on a threat actor-controlled GitHub account; creates one if absent.
3. **Recursively uploads all files** from `/mnt/user-data` — the directory Claude uses for uploads and background outputs — into randomly named folders to segment theft sessions.
4. **Writes a fake "network connections" log** to deceive defenders into believing the package is performing legitimate diagnostics.

A critical OPSEC failure was identified: the package inadvertently leaked the attacker's own GitHub private token within its code, strongly suggesting the malware was generated or scaffolded using an AI coding assistant without adequate review.

```bash
# Postinstall hook entry point (reconstructed behaviour)
npx --yes mouse5212-super-formatter
# → authenticates to GitHub
# → creates repo if missing
# → uploads /mnt/user-data/** recursively
# → writes fake diagnostic log
```

## Framework Mapping

- **AML.T0010 – ML Supply Chain Compromise**: The attack exploits the npm ecosystem to deliver malicious code to ML/AI developer environments.
- **AML.T0057 – LLM Data Leakage**: Files processed by Claude (potentially including prompts, outputs, and sensitive documents) are exfiltrated.
- **AML.T0012 – Valid Accounts**: The malware harvests and abuses legitimate GitHub tokens from victim environments.
- **LLM05 – Supply Chain Vulnerabilities**: Malicious package injected into the open-source dependency chain targeting AI tooling users.
- **LLM06 – Sensitive Information Disclosure**: Claude workspace data, potentially containing confidential inputs and model outputs, is exposed.

## Impact Assessment

Developers integrating Claude AI into workflows — particularly those using automated pipelines that install npm packages — face direct risk of workspace data exfiltration. The `/mnt/user-data` directory may contain sensitive business documents, proprietary prompts, model outputs, and authentication artifacts. With 676 recorded downloads, the blast radius is moderate but the data sensitivity of affected targets could be significant. The leaked attacker token has since been revoked and the associated GitHub account removed.

## Mitigation & Recommendations

- **Immediate**: Search environments for `mouse5212-super-formatter` and remove it; treat any affected system as compromised.
- **Credential hygiene**: Rotate all GitHub tokens and environment-level secrets on affected machines.
- **Postinstall script controls**: Use `npm config set ignore-scripts true` or enforce allow-listing of packages permitted to run lifecycle scripts.
- **Dependency scanning**: Integrate tools such as Socket.dev, Snyk, or OX Security into CI/CD pipelines to flag suspicious postinstall behaviour.
- **Principle of least privilege**: Restrict network egress from build environments to prevent unauthorised outbound GitHub API calls.

## References

- [The Hacker News – Malicious npm Package Stole Files From Claude AI User Directory via GitHub](https://thehackernews.com/2026/05/malicious-npm-package-stole-files-from.html)
- OX Security Research: Moshe Siman Tov Bustan & Nir Zadok
