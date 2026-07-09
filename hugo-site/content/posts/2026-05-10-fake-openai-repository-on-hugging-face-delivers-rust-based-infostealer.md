---
title: "Hugging Face Supply Chain: Fake OpenAI Infostealer Hits 244K"
date: "2026-05-10T05:10:54+00:00"
draft: false
slug: "fake-openai-repository-on-hugging-face-delivers-rust-based-infostealer"

# ── Content metadata ──
summary: "A malicious Hugging Face repository impersonating OpenAI's 'Privacy Filter' project reached #1 on the platform's trending list and accumulated 244,000 downloads before removal, delivering a multi-stage infostealer to Windows users. The attack chain used a disguised Python loader to execute PowerShell commands, ultimately deploying a Rust-based payload capable of harvesting browser credentials, crypto wallets, SSH/VPN configs, and screenshots. The campaign highlights the growing risk of AI/ML supply chain attacks through trusted model-sharing platforms."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/fake-openai-repository-on-hugging-face-pushes-infostealer-malware/"
source_title: "Fake OpenAI repository on Hugging Face pushes infostealer malware"
source_date: 2026-05-09T14:26:03+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1717501218511-768944e2c325?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw5fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3ODM4ODg1OHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0019 - Publish Poisoned Datasets", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Typosquatted Hugging Face repo impersonating OpenAI delivered Rust infostealer to 244,000 downloaders."
tldr_who_at_risk: "AI/ML developers and researchers who install models from Hugging Face without verifying repository authenticity are most exposed."
tldr_actions: ["Audit any recently installed Hugging Face packages, especially those referencing OpenAI projects", "Implement code review of loader scripts before executing any downloaded ML repository files", "Enforce allowlists for trusted Hugging Face organisations and verify model card authenticity before download"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["hugging-face", "infostealer", "supply-chain-attack", "typosquatting", "openai-impersonation", "rust-malware", "python-loader", "powershell", "credential-theft", "ml-platform-abuse"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-10T04:54:18+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/fake-openai-repository-on-hugging-face-pushes-infostealer-malware/"
pipeline_version: "1.0.0"
---

## Overview

A threat actor created a fraudulent Hugging Face repository named `Open-OSS/privacy-filter` that typosquatted OpenAI's legitimate 'Privacy Filter' project. Discovered by HiddenLayer researchers on May 7, 2026, the repository briefly reached the #1 spot on Hugging Face's trending list and recorded approximately 244,000 downloads before the platform removed it following reports. The campaign demonstrates how adversaries are actively exploiting the trust and discoverability mechanics of AI model-sharing platforms to distribute malware at scale.

## Technical Analysis

The attack employed a multi-stage delivery chain designed to evade detection:

1. **Lure Layer**: The repository copied OpenAI's legitimate model card nearly verbatim, presenting a convincing facade to researchers and developers browsing trending AI tools.

2. **Loader Script (`loader.py`)**: A Python file included superficial AI-related code for camouflage. Behind this facade, it:
   - Disabled SSL certificate verification
   - Decoded a base64-encoded URL pointing to an external resource
   - Fetched and executed a JSON payload containing an embedded PowerShell command

3. **PowerShell Stage**: Executed silently in a hidden window, the command downloaded `start.bat`, which:
   - Performed privilege escalation
   - Downloaded the final payload (`sefirah`)
   - Added the payload to Microsoft Defender's exclusion list
   - Executed the payload

4. **Final Payload — Rust Infostealer (`sefirah`)**: A capable Rust-based credential harvester targeting:
   - Browser data (cookies, passwords, session tokens, encryption keys) from Chromium and Gecko browsers
   - Discord tokens, local databases, and master keys
   - Cryptocurrency wallets and wallet browser extensions
   - SSH, FTP, and VPN credentials including FileZilla configurations
   - Sensitive local files and wallet seeds/keys
   - System information and multi-monitor screenshots

Stolen data is compressed and exfiltrated to a C2 server at `recargapopular[.]com`. The malware also incorporates extensive anti-analysis capabilities, including VM, sandbox, and debugger detection.

## Framework Mapping

- **AML.T0010 — ML Supply Chain Compromise**: The attack directly targets the AI/ML development pipeline by weaponising a trusted model-sharing platform to distribute malicious packages.
- **AML.T0019 — Publish Poisoned Datasets/Repositories**: The adversary published a poisoned repository with a near-identical model card to deceive users.
- **AML.T0047 — ML-Enabled Product or Service**: The attack exploits user trust in legitimate AI tooling ecosystems.
- **LLM05 — Supply Chain Vulnerabilities**: The incident is a textbook example of third-party AI component compromise through a trusted distribution channel.

## Impact Assessment

With 244,000 downloads recorded before removal, the potential victim pool is significant. Any Windows user who installed and executed code from this repository may have had browser credentials, cryptocurrency assets, SSH/VPN configurations, and session tokens exfiltrated. The attack is particularly dangerous for AI researchers, MLOps engineers, and developers who routinely install packages from Hugging Face as part of their workflow and may not scrutinise loader scripts closely.

## Mitigation & Recommendations

- **Immediate**: Check systems for the presence of `sefirah` or related artefacts; rotate all credentials stored in affected browsers and SSH/VPN configurations.
- **Network**: Block connections to `recargapopular[.]com` and monitor for outbound traffic to unknown C2 infrastructure.
- **Process**: Establish code review requirements for any Python scripts (`loader.py` patterns) downloaded from ML repositories before execution.
- **Platform Hygiene**: Only install models from verified organisations on Hugging Face; cross-reference repositories against official vendor GitHub/documentation links.
- **Detection**: Deploy behavioural monitoring for PowerShell execution spawned from Python processes, particularly those running in hidden windows.

## References

- [BleepingComputer — Fake OpenAI repository on Hugging Face pushes infostealer malware](https://www.bleepingcomputer.com/news/security/fake-openai-repository-on-hugging-face-pushes-infostealer-malware/)
