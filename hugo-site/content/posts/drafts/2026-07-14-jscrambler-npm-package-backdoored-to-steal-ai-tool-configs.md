---
title: "Jscrambler npm Package Backdoored to Steal AI Tool Configs"
date: 2026-07-14T03:50:02+00:00
draft: true
slug: "jscrambler-npm-package-backdoored-to-steal-ai-tool-configs"

# ── Content metadata ──
summary: "A threat actor published malicious versions of the Jscrambler npm package, embedding an infostealer that executed during the preinstall hook and was downloaded nearly 1,500 times in a two-hour window. The malware explicitly targeted AI coding tool configurations including Claude, Cursor, Windsurf, VS Code, and MCP setups, alongside cloud credentials, developer secrets, and cryptocurrency wallets. The incident highlights the growing risk of supply chain attacks targeting developer tooling that integrates with AI-assisted coding environments."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/hackers-backdoor-jscrambler-npm-package-with-infostealer-malware"
source_title: "Hackers backdoor Jscrambler npm package with infostealer malware"
source_date: 2026-07-13T19:44:19+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1544256718-3bcf237f3974?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMHx8YmFja2Rvb3IlMjBzaGFkb3clMjBoYWNraW5nJTIwc2VydmVyfGVufDB8MHx8fDE3ODQwMDEwMDJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Malicious Jscrambler npm versions stole AI tool configs and developer credentials 1,479 times in two hours."
tldr_who_at_risk: "JavaScript developers using Jscrambler's Code Integrity npm package are most exposed, particularly those with AI coding tool integrations like Cursor, Claude, or Windsurf."
tldr_actions: ["Immediately audit npm lock files for Jscrambler versions 8.14, 8.16, 8.17, or 8.20 and upgrade to 8.22", "Rotate all secrets, API keys, SSH keys, cloud credentials, and CI/CD tokens present in any environment where the package was installed", "Revoke and reissue AI coding tool API keys and MCP configuration credentials, especially for Claude, Cursor, and Windsurf"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["npm-supply-chain", "infostealer", "jscrambler", "ai-tool-credentials", "mcp-config-theft", "developer-secrets", "chacha20-poly1305", "preinstall-hook", "credential-theft", "cursor-ide", "claude-config", "javascript-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-07-14T03:50:02+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/hackers-backdoor-jscrambler-npm-package-with-infostealer-malware"
pipeline_version: "2.1.0"
---

## Overview

On July 13, 2026, Jscrambler disclosed that an unknown threat actor hijacked its npm package to publish malicious releases containing a fully-featured infostealer. The compromised versions — 8.14, 8.16, 8.17, and 8.20 — were live for approximately two hours before being deprecated, during which they were downloaded 1,479 times. Jscrambler responded by releasing a clean version 8.22 and deprecating four dependent packages that had inherited the malicious dependency.

The incident is notable not only for its speed and scale, but for the malware's explicit targeting of AI coding tool configurations — a sign that threat actors are increasingly aware of the sensitive credential surface created by modern AI-assisted development environments.

## Technical Analysis

The malware executed during the `preinstall` lifecycle hook, meaning it ran automatically upon `npm install` before any user interaction with the package itself. This is a well-established technique for ensuring execution in developer pipelines and CI/CD systems.

Application security firm Socket analysed the malicious release and identified a broad credential-harvesting payload targeting:

- **Developer secrets**: Git credentials, SSH keys, environment variables, CI/CD tokens
- **Cloud platforms**: AWS, Azure, GCP, and Kubernetes configurations
- **AI coding tools**: Claude, Cursor, Windsurf, VS Code, Zed, and MCP (Model Context Protocol) configurations
- **Cryptocurrency wallets**: MetaMask, Phantom, Coinbase, Exodus, Trust Wallet seed phrases
- **Browser data**: saved credentials and session cookies
- **Messaging apps**: Slack, Discord, Telegram

To hinder reverse engineering, the malware employed per-string obfuscation using the **ChaCha20-Poly1305** authenticated encryption algorithm — an unusually strong choice for string-level obfuscation in malware, suggesting a technically capable threat actor.

The inclusion of MCP configuration theft is particularly significant. MCP (Model Context Protocol) credentials govern how AI agents interact with external tools and APIs, meaning their compromise could extend the blast radius well beyond static secrets into live agentic workflows.

## Framework Mapping

**MITRE ATLAS**
- **AML.T0010 – ML Supply Chain Compromise**: Direct compromise of a widely-used developer npm package to target AI tooling ecosystems.
- **AML.T0057 – LLM Data Leakage**: Exfiltration of AI tool API keys and MCP configurations that could expose LLM interaction history or enable impersonation.
- **AML.T0047 – ML-Enabled Product or Service**: The attack specifically targeted environments integrated with AI coding assistants.

**OWASP LLM Top 10**
- **LLM05 – Supply Chain Vulnerabilities**: Classic package compromise inserted into a trusted developer dependency.
- **LLM06 – Sensitive Information Disclosure**: AI tool configurations, API keys, and agent credentials exfiltrated at scale.

## Impact Assessment

With 17,000 weekly downloads, Jscrambler's npm package has a substantial developer user base. The 1,479 downloads in the two-hour exposure window represent a meaningful proportion of users who could have had their full development environment credentials stolen. Organisations using AI coding tools like Cursor or Claude with MCP integrations face an elevated risk of secondary compromise, as stolen MCP tokens could be used to impersonate developer agents in downstream workflows.

## Mitigation & Recommendations

1. **Audit immediately**: Check `package-lock.json` and `node_modules` for Jscrambler versions 8.14, 8.16, 8.17, or 8.20. Upgrade to version 8.22.
2. **Rotate all credentials**: Treat any secret present in affected environments as compromised — API keys, SSH keys, cloud IAM credentials, and CI/CD tokens.
3. **Revoke AI tool credentials**: Specifically rotate API keys for Claude, Cursor, Windsurf, and any MCP-connected services.
4. **Review CI/CD pipeline logs**: Check for anomalous outbound connections during the window of July 13, 2026 between approximately 01:44–03:44 PM UTC.
5. **Enable npm audit hooks**: Integrate tools like Socket or Snyk into CI pipelines to flag malicious preinstall scripts before execution.

## References

- [BleepingComputer – Hackers backdoor Jscrambler npm package with infostealer malware](https://www.bleepingcomputer.com/news/security/hackers-backdoor-jscrambler-npm-package-with-infostealer-malware)
