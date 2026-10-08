---
title: "Tensorlake npm Package Hijacked by Shai-Hulud Worm"
date: 2026-10-08T12:18:44+00:00
draft: false 
slug: "tensorlake-npm-package-hijacked-by-shai-hulud-worm"

# ── Content metadata ──
summary: "The tensorlake npm package (version 0.5.144) was compromised as part of a supply chain attack delivering the Shai-Hulud credential-stealing worm, which harvests tokens, SSH keys, AWS credentials, and configuration files from AI developer tools including Anthropic Claude, Cursor, and Windsurf. The self-propagating worm republishes compromised packages under victim maintainer identities and uses an Ethereum smart contract for C2 resolution, with a destructive 'hostage token' mechanism triggered if victims revoke stolen GitHub tokens. The attack specifically targets AI/ML developer toolchains, making it directly relevant to teams building on or integrating with Tensorlake-based infrastructure."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/10/tensorlake-npm-package-compromised-to.html"
source_title: "Tensorlake npm Package Compromised to Deliver Shai-Hulud Credential-Stealing Worm"
source_date: 2026-10-08T05:46:20+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1686890365389-d53604e68255?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOXx8cGFyYXNpdGUlMjBuYXR1cmUlMjBjbG9zZS11cCUyMG1hY3JvfGVufDB8MHx8fDE3OTE0NjE5MjR8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0081 - Modify AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Tensorlake npm package v0.5.144 was poisoned with a self-propagating credential-stealing worm targeting AI developers."
tldr_who_at_risk: "Developers and CI/CD pipelines using the tensorlake npm SDK who installed version 0.5.144, particularly those with access to AWS, GitHub, Kubernetes, or AI tool configurations."
tldr_actions: ["Immediately audit installed tensorlake versions and remove v0.5.144 from all environments", "Rotate all exposed credentials including GitHub tokens, AWS keys, SSH keys, and Vault secrets", "Audit npm publishing identities for unauthorized package releases under your maintainer account"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Agentic AI"]
tags: ["shai-hulud", "tensorlake", "npm-supply-chain", "credential-theft", "self-propagating-worm", "chaindrop", "ai-developer-tools", "github-token", "aws-credentials", "kubernetes", "mcp-files", "anthropic-claude", "cursor-ide", "hackbrowserdata", "ethereum-c2"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-08T12:18:44+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/10/tensorlake-npm-package-compromised-to.html"
pipeline_version: "2.1.0"
---

## Overview

The `tensorlake` npm package — a TypeScript SDK used for Tensorlake applications, sandboxes, and cloud services — was compromised in a sophisticated supply chain attack on 7 October 2026. Version 0.5.144 contained obfuscated malware delivering the Shai-Hulud credential-stealing worm, part of a broader campaign tracked as ChainDrop. The malicious release has since been removed from the npm registry, but any developer or pipeline that installed the package during its active window faces significant exposure across credentials, secrets, and persistent attacker access.

The attack is notable for its direct targeting of AI developer tooling, including configuration files for Anthropic Claude, Cursor, Kiro, Windsurf, and Zed — tools commonly used in agentic AI and LLM-integrated development workflows.

## Technical Analysis

The malicious version uses a `preinstall` hook to execute `package/lib/setup.mjs`, an obfuscated loader that invokes the core worm binary `package/lib/Math_Symbol.js` via the Bun JavaScript runtime.

**Credential harvesting targets:**
- npm and GitHub tokens
- AWS credentials and secrets
- HashiCorp Vault and Kubernetes credentials
- SSH keys and `.env` files
- Cryptocurrency wallets and messaging app data
- MCP and configuration files for Claude, Cursor, Kiro, Windsurf, and Zed

The HackBrowserData binary is dropped to extract browser-stored credentials. Exfiltrated data is staged in a public GitHub repository bearing the description *"Shai-Hulud: Here We Go Again"* in encrypted form.

**C2 resolution** is performed via an Ethereum smart contract resolving to `iseekaigogo[.]com`, with GitHub as a fallback. This blockchain-based C2 mechanism makes takedown significantly more difficult.

**Self-propagation** occurs by enumerating packages associated with the victim's npm publishing identity, building Sigstore provenance, and republishing compromised versions. Fake Copilot/Dependabot GitHub Actions workflows are also planted to extend persistence.

**The 'hostage token' mechanism** is particularly aggressive: a PowerShell monitor continuously polls `api.github.com/user` with the stolen GitHub token. If the token is revoked, `Invoke-Expression` executes attacker-supplied PowerShell code, likely triggering a destructive payload — a tactic consistent with prior Shai-Hulud waves.

The malware also writes `.claude/settings.json` and `.vscode/tasks.json` into reachable repositories, enabling persistent code execution hooks within developer environments.

## Framework Mapping

- **AML.T0010 / AML.T0115**: Classic AI supply chain compromise via poisoned npm artifact published under a legitimate maintainer identity.
- **AML.T0083 / AML.T0098**: Credential harvesting explicitly targets AI agent configuration files (MCP, Claude, Cursor), extracting secrets that could be used to impersonate or control AI agents.
- **AML.T0081 / AML.T0084**: Writing malicious `.claude/settings.json` files constitutes modification and discovery of AI agent configuration.
- **LLM05**: The npm supply chain vector directly matches OWASP's Supply Chain Vulnerabilities category.
- **LLM06**: Mass exfiltration of secrets accessible to LLM-integrated tooling constitutes sensitive information disclosure at scale.

## Impact Assessment

Any developer or automated pipeline that installed `tensorlake` v0.5.144 should be treated as fully compromised. Beyond the immediate credential theft, the worm's self-propagation capability means downstream consumers of victim-maintained packages may also have been infected. The targeting of AI tool configurations (Claude, Cursor, Windsurf) extends the blast radius into agentic workflows where stolen API keys could enable model abuse or data exfiltration at the application layer.

## Mitigation & Recommendations

1. **Remove** `tensorlake` v0.5.144 immediately from all environments and lock to a clean, verified version.
2. **Rotate all credentials** found in targeted locations: GitHub tokens, AWS keys, Vault secrets, SSH keys, Kubernetes configs, and AI tool API keys.
3. **Audit npm publish history** for your maintainer identity to identify any unauthorised package releases.
4. **Review GitHub Actions workflows** for unexpected Copilot or Dependabot workflow files.
5. **Scan repositories** for injected `.claude/settings.json` and `.vscode/tasks.json` files.
6. **Enable npm package signing verification** and monitor for Sigstore provenance anomalies.

## References

- [The Hacker News — Tensorlake npm Package Compromised to Deliver Shai-Hulud Credential-Stealing Worm](https://thehackernews.com/2026/10/tensorlake-npm-package-compromised-to.html)
