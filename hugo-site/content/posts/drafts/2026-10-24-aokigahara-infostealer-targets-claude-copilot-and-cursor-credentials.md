---
title: "Aokigahara Infostealer Targets Claude, Copilot, and Cursor Credentials"
date: 2026-10-24T09:47:41+00:00
draft: false 
slug: "aokigahara-infostealer-targets-claude-copilot-and-cursor-credentials"

# ── Content metadata ──
summary: "A newly identified infostealer dubbed Aokigahara has been observed actively harvesting authentication tokens and session data from AI development tools including Claude, ChatGPT Desktop, GitHub Copilot, Cursor, and Gemini CLI. Beyond traditional credential theft targeting browsers and crypto wallets, the malware includes dedicated collection routines for AI service credentials, SSH keys, and cloud environment configurations. Stolen AI session tokens could enable unauthorized access to paid AI services, exposure of private development data, or resale of compromised accounts on underground markets."
source: "Check Point Research"
source_url: "https://research.checkpoint.com/2026/infostealer-riding-the-ai-train"
source_title: "Infostealer riding the AI Train"
source_date: 2026-10-23T13:00:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1758685733809-0e53c640d93f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxzY2llbnRpc3QlMjB0aGlua2luZyUyMGFic3RyYWN0fGVufDB8MHx8fDE3OTI4MzUyNjB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0113 - Steal Web Session Cookie", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0040 - AI Model Inference API Access", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Aokigahara infostealer steals session tokens and credentials from AI coding and chat tools."
tldr_who_at_risk: "Developers and power users of AI tools such as Claude, ChatGPT Desktop, Cursor, Copilot, and Gemini CLI are most exposed due to targeted collection routines for their credential and session files."
tldr_actions: ["Rotate API keys and session tokens for all AI services and developer tools immediately if compromise is suspected", "Enable MFA and monitor for anomalous login activity across AI platforms, cloud accounts, and code repositories", "Audit local credential storage for AI tools and move secrets to dedicated secrets managers rather than plaintext config files"]

# ── Taxonomies ──
categories: ["LLM Security", "Industry News", "Research"]
tags: ["infostealer", "aokigahara", "credential-theft", "ai-tool-targeting", "claude", "chatgpt", "github-copilot", "cursor-ide", "session-hijacking", "cloud-credentials", "developer-tools", "malware", "check-point-research", "gemini-cli", "windsurf"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-24T09:47:41+00:00"
feed_source: "checkpoint"
original_url: "https://research.checkpoint.com/2026/infostealer-riding-the-ai-train"
pipeline_version: "2.1.0"
---

## Overview

Check Point Research has identified **Aokigahara**, a newly observed infostealer that extends traditional credential-theft tradecraft into AI application territory. Potentially related to earlier variants tracked as Kamidere or Stygian, Aokigahara includes dedicated collection routines for authentication files, session tokens, and configuration data associated with AI tools including Claude, ChatGPT Desktop, OpenAI Codex, Cursor, Windsurf, GitHub Copilot, and Gemini CLI. This represents a meaningful evolution in infostealer targeting — attackers are now explicitly treating AI service access as a monetizable asset alongside banking credentials and cryptocurrency wallets.

## Technical Analysis

Aokigahara is modular in design, organised around named handlers each responsible for a specific target category. Core capabilities include:

- **sysinfo handler**: Enumerates system metadata including OS version, CPU/RAM, running processes, installed software, and detected antivirus products.
- **screenshot handler**: Captures the active display state at time of execution.
- **Browser handler**: Harvests passwords and cookies from Chromium-based browsers and Mozilla Firefox.
- **Crypto handler**: Targets desktop wallet applications and browser-based wallet extensions.
- **AI tool handler**: Collects authentication files, session tokens, and configuration files from Claude, ChatGPT Desktop, Codex, Cursor, Windsurf, GitHub Copilot, and Gemini CLI.
- **Developer environment handler**: Grabs Git credential files, SSH private keys, and credential/configuration files for AWS, Azure, and Google Cloud.
- **Clipper component**: Drops a secondary binary for clipboard manipulation, commonly used for cryptocurrency address substitution.

Additional targets span Discord, Telegram, Steam, Roblox, Minecraft, password managers, VPN clients, FTP/SFTP clients, and email applications.

The AI-specific collection routines are notable because many AI desktop clients and CLI tools store session tokens or API keys in predictable local file paths, often in plaintext or minimally protected formats. Exfiltrating these files grants attackers the ability to impersonate the victim against AI service APIs without needing to crack passwords.

## Framework Mapping

- **AML.T0012 (Valid Accounts)** and **AML.T0113 (Steal Web Session Cookie)**: Aokigahara's primary objective is acquiring usable credentials and session tokens to enable legitimate-appearing access to AI services.
- **AML.T0083 (Credentials from AI Agent Configuration)** and **AML.T0084 (Discover AI Agent Configuration)**: The malware specifically targets configuration files for AI coding assistants and CLI tools, a pattern that maps directly to these ATLAS techniques.
- **AML.T0040 (AI Model Inference API Access)**: Stolen API keys or session tokens could enable attackers to make inference requests under the victim's identity and quota.
- **LLM06 (Sensitive Information Disclosure)**: Compromised AI sessions may expose private conversation history, code, and project context stored within AI platforms.

## Impact Assessment

The primary risk groups are developers and technical professionals who use AI coding assistants and cloud-integrated toolchains daily. Stolen credentials could enable:

1. **Account resale** — compromised AI subscriptions sold on underground forums.
2. **Quota abuse** — unauthorized inference at the victim's expense.
3. **Data exposure** — access to private conversation histories and proprietary code.
4. **Lateral movement** — SSH keys and cloud credentials enabling deeper infrastructure compromise.

## Mitigation & Recommendations

- **Rotate credentials immediately** for all AI services, cloud providers, and developer tools if endpoint compromise is suspected.
- **Enable MFA** on all AI platform accounts and monitor for logins from unfamiliar IPs or devices.
- **Audit local credential storage**: avoid plaintext API keys in config files; use OS-level credential stores or dedicated secrets managers (e.g., HashiCorp Vault, AWS Secrets Manager).
- **Deploy endpoint detection** capable of identifying infostealer behavioural patterns such as mass file reads across credential directories.
- **Review SSH and cloud IAM keys** for anomalous usage and rotate on a defined schedule.

## References

- Check Point Research: [Infostealer riding the AI Train](https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/)
