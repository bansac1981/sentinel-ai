---
title: "Claude Code VS Code Extension Trojanized with SSH Backdoor"
date: 2026-10-30T11:31:47+00:00
draft: true
slug: "claude-code-vs-code-extension-trojanized-with-ssh-backdoor"

# ── Content metadata ──
summary: "The official Anthropic Claude Code extension on the Cursor IDE marketplace was compromised with a malicious 66-line JavaScript loader that installs a persistent SSH backdoor, affecting up to 5,000 users. The malware establishes reverse tunnels to an attacker-controlled server, harvests environment variable names (including cloud credentials and API keys), and installs cross-platform persistence mechanisms. Anthropic has since released a clean version 2.1.314, but all users of the compromised version remain at risk of persistent access even after removal."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/10/official-claude-code-vs-code-extension.html"
source_title: "Official Claude Code VS Code Extension Compromised to Install Persistent SSH Backdoor"
source_date: 2026-10-30T08:55:47+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1681949270990-cecd4728d2e0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNXx8cmVzZWFyY2glMjB3aGl0ZWJvYXJkJTIwYnJhaW5zdG9ybXxlbnwwfDB8fHwxNzkzMzU5OTA3fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0047 - AI-Enabled Product or Service", "AML.T0083 - Credentials from AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Official Claude Code VS Code extension trojanized on Cursor marketplace with persistent SSH backdoor."
tldr_who_at_risk: "Developers using the Cursor IDE who installed Claude Code extension version 2.1.313 are directly exposed to persistent attacker SSH access and credential reconnaissance."
tldr_actions: ["Immediately update to Claude Code extension v2.1.314 or later from the official marketplace", "Remove the attacker SSH key 'svc-telemetry' from ~/.ssh/authorized_keys on all affected hosts", "Audit and rotate all cloud credentials, API tokens, and secrets on affected developer machines", "Remove persistence mechanisms: check scheduled tasks (Windows), crontab (Linux), and LaunchAgent (macOS)", "Block or monitor outbound connections to 134.209.82.225 across your environment"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["supply-chain-attack", "ssh-backdoor", "cursor-ide", "claude-code", "anthropic", "vs-code-extension", "reverse-tunnel", "credential-harvesting", "persistence", "malware"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-30T11:31:47+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/10/official-claude-code-vs-code-extension.html"
pipeline_version: "2.1.0"
---

## Overview

On October 30, 2026, cybersecurity researchers disclosed that the official Anthropic Claude Code extension distributed through the Cursor IDE marketplace had been trojanized with a persistent SSH backdoor. The compromise affected up to 5,000 users who installed the malicious version 2.1.313 of the extension. Cursor briefly took the marketplace offline to remediate the incident, and Anthropic subsequently published a clean version 2.1.314 to both Open VSX and the Microsoft VS Code Marketplace. The incident highlights the growing risk of AI developer tooling as a high-value supply chain attack surface.

## Technical Analysis

The malicious package identified itself as `anthropic.claude-code` version 2.1.313. A 66-line JavaScript loader was inserted before the legitimate extension code in the main bundle, activating after VS Code startup and when the extension's webview opens.

**Execution chain:**
1. **SSH Key Injection** — Appends an attacker-controlled public key labelled `svc-telemetry` to `~/.ssh/authorized_keys`.
2. **SSH Service Activation** — Attempts to enable the local SSH daemon across Windows, Linux, and macOS (requires admin rights; fails silently on hardened macOS/Windows hosts).
3. **Reverse Tunnel** — Establishes a reverse SSH tunnel to `134.209.82[.]225`, providing the attacker a pathway into the victim's machine.
4. **Persistence** — Installs platform-specific persistence: Windows scheduled task, Linux crontab, macOS LaunchAgent.
5. **Host Beacon** — Transmits host reconnaissance data via unencrypted HTTP POST to `134.209.82[.]225:8099/beacon`.

**Beaconed data includes:**
- Public IP (via `api.ipify.org`)
- Hostname and local username
- OS and CPU architecture
- Home and working directories
- Global Git email
- Names (not values) of up to 40 environment variables matching patterns: `KEY`, `TOKEN`, `SECRET`, `PASS`, `AWS`, `GCP`

While environment variable *values* are not exfiltrated in the initial beacon, successful SSH tunnel access would allow direct inspection of the full environment.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0010 – AI Supply Chain Compromise | Attacker compromised an AI coding tool's marketplace distribution |
| MITRE ATLAS | AML.T0115 – Publish Poisoned AI Artifacts | Trojanized extension published as legitimate Anthropic package |
| MITRE ATLAS | AML.T0083 – Credentials from AI Agent Config | Harvesting cloud credential names from developer environments |
| OWASP | LLM05 – Supply Chain Vulnerabilities | Compromise via third-party marketplace, not the core model |
| OWASP | LLM06 – Sensitive Information Disclosure | Credential metadata and host data exfiltrated |
| OWASP | LLM07 – Insecure Plugin Design | Extension granted filesystem and network access without adequate integrity controls |

## Impact Assessment

Up to 5,000 developer workstations may have been compromised. Developers represent a high-value target: their machines typically hold cloud credentials, source code, API tokens, and access to CI/CD pipelines. Even where the SSH service could not be enabled (most macOS and Windows hosts without admin rights), the attacker's SSH key remains installed and persistence mechanisms are active. The recon beacon also provides enough metadata to prioritise high-value targets for follow-on manual access.

## Mitigation & Recommendations

1. **Update immediately** to Claude Code v2.1.314 from the official marketplace.
2. **Purge the rogue SSH key**: remove any entry labelled `svc-telemetry` from `~/.ssh/authorized_keys`.
3. **Remove persistence**: delete associated scheduled tasks (Windows), crontab entries (Linux), or LaunchAgents (macOS).
4. **Rotate credentials**: treat all secrets and API tokens on affected machines as compromised; rotate immediately.
5. **Network block**: add `134.209.82.225` to firewall blocklists and audit historical DNS/HTTP logs for beacon traffic.
6. **Audit extension provenance**: enforce extension allowlisting in enterprise VS Code/Cursor deployments.

## References

- [The Hacker News – Original Report](https://thehackernews.com/2026/10/official-claude-code-vs-code-extension.html)
