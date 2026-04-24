---
title: "Bitwarden CLI Compromised in Ongoing Checkmarx Supply Chain Campaign"
date: 2026-04-24T02:40:42+00:00
draft: false
slug: "bitwarden-cli-compromised-in-ongoing-checkmarx-supply-chain-campaign"

# ── Content metadata ──
summary: "A compromised version of the Bitwarden CLI npm package was found stealing developer secrets, including configurations for AI coding tools such as Claude, Kiro, Cursor, Codex CLI, and Aider, as part of an ongoing supply chain campaign. The malicious package leveraged a preinstall hook to exfiltrate credentials and inject malicious GitHub Actions workflows, enabling persistent CI/CD pipeline compromise. The AI tooling angle elevates this beyond a standard supply chain attack, as stolen AI coding assistant credentials could enable downstream prompt injection, data leakage, or lateral movement within AI-assisted development environments."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/bitwarden-cli-compromised-in-ongoing.html"
source_date: 2026-04-23T13:42:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/6170188/pexels-photo-6170188.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0057 - LLM Data Leakage", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Bitwarden CLI npm package backdoored to steal developer and AI coding tool credentials via preinstall hook."
tldr_who_at_risk: "Developers using @bitwarden/cli@2026.4.0 are directly exposed, especially those whose environments include AI coding assistants like Claude, Cursor, or Codex CLI."
tldr_actions: ["Immediately audit installed npm packages and remove or downgrade @bitwarden/cli@2026.4.0", "Rotate all GitHub tokens, npm credentials, SSH keys, and cloud secrets on affected developer machines", "Audit CI/CD pipelines for injected or unauthorised GitHub Actions workflows"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["supply-chain-attack", "npm-package", "bitwarden-cli", "github-actions", "credential-theft", "ai-coding-tools", "cicd-compromise", "checkmarx-campaign", "developer-security", "exfiltration"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-24T02:40:42+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/bitwarden-cli-compromised-in-ongoing.html"
pipeline_version: "1.0.0"
---

## Overview

A malicious version of the Bitwarden CLI npm package (`@bitwarden/cli@2026.4.0`) was identified as part of an ongoing supply chain campaign attributed to a threat actor known as TeamPCP. Discovered by JFrog, Socket, and OX Security, the attack is consistent with the broader Checkmarx supply chain campaign pattern, leveraging a compromised GitHub Action within Bitwarden's CI/CD pipeline. Notably, the malicious code specifically targeted configurations for AI coding tools — including Claude, Kiro, Cursor, Codex CLI, and Aider — making this a direct threat to AI-assisted software development environments.

## Technical Analysis

The attack executed via a **preinstall npm hook**, triggering a credential stealer before the legitimate package code ever ran. The malicious file `bw1.js` performed the following actions:

1. **Credential harvesting** — targeted local secrets, `.env` files, shell history, `.ssh` keys, GitHub Actions environment variables, cloud provider credentials, and AI coding assistant configuration files.
2. **Encryption and exfiltration** — stolen data was encrypted with AES-256-GCM and sent to `audit.checkmarx[.]cx`, a domain impersonating the legitimate Checkmarx security vendor. A GitHub repository served as a fallback exfiltration channel.
3. **Lateral movement** — if GitHub tokens were discovered, the malware injected malicious Actions workflows into reachable repositories and used harvested npm credentials to push further poisoned package versions downstream.
4. **Persistence** — a single compromised developer token could grant attackers persistent access to every CI/CD pipeline accessible to that developer.

Security researcher Adnan Khan noted this is believed to be the first compromise of an npm package using NPM Trusted Publishing. The string `"Shai-Hulud: The Third Coming"` found embedded in the package suggests this may be the third iteration of a longer-running campaign.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The attack directly poisoned a widely-used developer CLI package distributed via npm, targeting downstream AI development toolchains.
- **AML.T0057 (LLM Data Leakage):** AI coding tool configurations — potentially containing API keys, system prompts, and project context — were specifically targeted for exfiltration.
- **AML.T0012 (Valid Accounts):** Stolen GitHub and npm tokens were weaponised to maintain persistent, legitimate-looking access across CI/CD pipelines.
- **LLM05 (Supply Chain Vulnerabilities):** The attack exploited the npm package ecosystem as a vector into AI-integrated development environments.
- **LLM06 (Sensitive Information Disclosure):** Exfiltration of AI tool credentials and configurations constitutes direct sensitive information disclosure from LLM-adjacent tooling.

## Impact Assessment

Any developer who installed `@bitwarden/cli@2026.4.0` is at risk of full credential compromise. The blast radius extends to every repository, CI/CD pipeline, and cloud environment accessible via stolen tokens. The targeting of AI coding tools adds a novel dimension: compromised Claude, Cursor, or Codex CLI credentials could expose proprietary codebases, internal prompts, or AI-generated intellectual property. Organisations with AI-assisted development workflows should treat this as a high-severity incident.

## Mitigation & Recommendations

- **Remove** `@bitwarden/cli@2026.4.0` immediately and pin to a verified clean version.
- **Rotate** all secrets potentially exposed: GitHub tokens, npm tokens, SSH keys, AWS/GCP/Azure credentials, and AI tool API keys.
- **Audit** GitHub Actions workflows across all accessible repositories for injected or unrecognised steps.
- **Enable** npm audit and integrity checks in CI/CD pipelines; consider enforcing lockfile integrity.
- **Monitor** for outbound connections to `audit.checkmarx[.]cx` and review recent GitHub commit history for anomalous activity.
- **Implement** StepSecurity or equivalent GitHub Actions hardening to restrict workflow permissions.

## References

- [The Hacker News — Bitwarden CLI Compromised in Ongoing Checkmarx Supply Chain Campaign](https://thehackernews.com/2026/04/bitwarden-cli-compromised-in-ongoing.html)
