---
title: "Shai-Hulud Supply Chain Attack Trojans 19 PyPI Packages, Targets Claude Configs"
date: 2026-06-09T06:59:37+00:00
draft: true
slug: "shai-hulud-supply-chain-attack-trojans-19-pypi-packages-targets-claude-configs"

# ── Content metadata ──
summary: "The Shai-Hulud campaign has compromised 19 science-focused PyPI packages \u2014 including popular bioinformatics tools \u2014 injecting malicious payloads that harvest developer credentials, CI/CD secrets, and notably Claude/MCP configuration files. The attack uses a stealthy .pth file trigger that executes on any Python invocation, downloading a Bun JavaScript runtime to run an obfuscated exfiltration payload. The explicit targeting of Anthropic Claude and MCP configuration files marks a direct AI-tooling angle, elevating this beyond a standard supply chain incident."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/new-shai-hulud-attack-trojanizes-19-science-focused-pypi-packages/"
source_title: "New Shai-Hulud attack trojanizes 19 science-focused PyPI packages"
source_date: 2026-06-08T20:41:35+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1658479657379-e0adb7cb91e8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxtYWx3YXJlJTIwY29tcHV0ZXIlMjB2aXJ1cyUyMGRhcmslMjBoYWNrZXJ8ZW58MHwwfHx8MTc4MDk4ODM3N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0019 - Publish Poisoned Datasets", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "19 PyPI packages trojanized to steal developer secrets including Claude/MCP AI configuration files."
tldr_who_at_risk: "Python developers, data scientists, and CI/CD pipelines using bioinformatics or scientific packages are directly exposed."
tldr_actions: ["Audit installed PyPI packages against the 453 known Shai-Hulud malicious artifacts list published by Socket", "Rotate all CI/CD secrets, cloud credentials, SSH keys, and AI API tokens (including Anthropic/Claude) on potentially affected systems", "Implement package integrity verification and dependency pinning in all Python environments and CI pipelines"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["pypi", "supply-chain", "shai-hulud", "credential-theft", "bioinformatics", "claude-mcp", "ci-cd-compromise", "malicious-packages", "javascript-payload", "developer-secrets"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-06-09T06:59:37+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/new-shai-hulud-attack-trojanizes-19-science-focused-pypi-packages/"
pipeline_version: "1.0.0"
---

## Overview

The Shai-Hulud supply chain campaign has expanded significantly, with researchers at Socket identifying 19 compromised PyPI packages — spanning 37 malicious releases — that collectively accumulated hundreds of thousands of downloads. Targeted packages include widely used bioinformatics tools such as Dynamo, Spateo, CoolBox, U-FISH, and Napari-UFISH. What distinguishes this wave from generic credential theft is the explicit targeting of Claude/MCP configuration files, placing AI developer tooling squarely in the crosshairs.

## Technical Analysis

The attack mechanism is notably stealthy. Malicious wheels embed a `*-setup.pth` file alongside an obfuscated JavaScript payload (`_index.js`). Python processes `.pth` files automatically during interpreter startup, meaning the payload fires on any Python invocation — including `pip`, test runners, Jupyter kernels, or CI jobs — without requiring explicit import of the compromised package.

The `.pth` file attempts to download the Bun JavaScript runtime from GitHub, then executes the bundled `_index.js` script. This two-stage approach helps evade static analysis by keeping the primary payload off-disk until runtime.

The JavaScript payload targets an extensive credential surface:

- GitHub tokens and GitHub Actions secrets
- Package registry tokens (npm, PyPI, RubyGems, JFrog)
- Cloud provider credentials (AWS, GCP, Azure, Kubernetes, Vault)
- SSH keys and Docker credentials
- Shell histories and `.env` / `.npmrc` / `.pypirc` files
- **Claude/MCP configuration files** — a direct AI-tooling target

Exfiltration uses two channels: automatically created GitHub repositories (leveraging GitHub Actions to write stolen data), and direct HTTPS POST to what appears to be a spoofed Anthropic API endpoint (`api[.]anthropic[.]com/v1/api`). The Anthropic endpoint is invalid but likely chosen to blend malicious traffic into expected developer network patterns for AI tooling.

## Framework Mapping

**AML.T0010 – ML Supply Chain Compromise**: Malicious code injected into legitimate, widely downloaded scientific Python packages directly targets ML/data science developer environments.

**AML.T0047 – ML-Enabled Product or Service**: The explicit harvesting of Claude and MCP configuration files targets developers building or integrating AI agent pipelines.

**LLM05 – Supply Chain Vulnerabilities**: Compromised upstream dependencies introduce risk into any downstream AI application built on these packages.

**LLM06 – Sensitive Information Disclosure**: Stolen Claude API keys and MCP configs could enable adversaries to impersonate developers, access proprietary AI workflows, or pivot into production LLM deployments.

## Impact Assessment

The campaign's scientific package focus puts bioinformatics researchers, computational scientists, and data engineers at elevated risk — communities that may have less mature security postures than traditional software development teams. With 453 total malicious artifacts now attributed to Shai-Hulud, the campaign represents a sustained, organised threat. Compromised Claude/MCP credentials could expose proprietary AI agent configurations, system prompts, and downstream API access, extending blast radius well beyond the initial developer workstation.

## Mitigation & Recommendations

1. **Cross-reference your dependencies** against Socket's published list of 453 Shai-Hulud artifacts immediately.
2. **Rotate all secrets** on any system that installed affected packages: cloud credentials, registry tokens, SSH keys, and critically, all Anthropic/Claude API keys and MCP configuration secrets.
3. **Inspect `.pth` files** in your Python environments (`site-packages`) for unexpected entries — legitimate packages rarely use `.pth` files.
4. **Enforce dependency pinning and hash verification** (`pip install --require-hashes`) in all production and CI environments.
5. **Monitor outbound HTTPS traffic** from CI/CD runners for connections to unexpected GitHub repositories or Anthropic API endpoints.
6. **Adopt a private package mirror** with automated malware scanning for security-sensitive environments.

## References

- [BleepingComputer: New Shai-Hulud attack trojanizes 19 science-focused PyPI packages](https://www.bleepingcomputer.com/news/security/new-shai-hulud-attack-trojanizes-19-science-focused-pypi-packages/)
