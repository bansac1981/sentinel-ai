---
title: "Typosquatted OpenAI Repo on Hugging Face Delivered Rust Infostealer to 244K Users"
date: 2026-05-11T09:27:13+00:00
draft: false
slug: "typosquatted-openai-repo-on-hugging-face-delivered-rust-infostealer-to-244k"

# ── Content metadata ──
summary: "A malicious Hugging Face repository impersonated OpenAI's legitimate Privacy Filter model, cloning its description verbatim to gain credibility and reach the platform's trending list with 244,000 downloads. The repository delivered a multi-stage attack chain culminating in a Rust-based information stealer targeting browser credentials, cryptocurrency wallets, and Discord data on Windows machines. The attack leveraged a dead-drop resolver pattern via a public JSON paste service, allowing operators to swap payloads without modifying the repository itself."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/05/fake-openai-privacy-filter-repo-hits-1.html"
source_title: "Fake OpenAI Privacy Filter Repo Hits #1 on Hugging Face, Draws 244K Downloads"
source_date: 2026-05-11T07:05:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1717501217912-933d2792d493?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3ODM4ODg1OHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0019 - Publish Poisoned Datasets", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Fake OpenAI model repo on Hugging Face delivered a Rust infostealer to 244,000 downloaders."
tldr_who_at_risk: "AI/ML practitioners and developers who downloaded or executed the typosquatted Open-OSS/privacy-filter repository on Windows machines are directly exposed."
tldr_actions: ["Audit any usage of Open-OSS/privacy-filter and treat affected systems as fully compromised", "Verify Hugging Face repository provenance by checking namespace and commit history before execution", "Rotate browser credentials, cryptocurrency wallet keys, and Discord tokens on any affected machine"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["hugging-face", "supply-chain-attack", "typosquatting", "infostealer", "openai", "malicious-repository", "rust-malware", "dead-drop-resolver", "credential-theft", "cryptocurrency", "windows", "powershell", "uac-bypass", "amsi-bypass"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-11T09:27:13+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/05/fake-openai-privacy-filter-repo-hits-1.html"
pipeline_version: "1.0.0"
---

## Overview

A threat actor successfully typosquatted OpenAI's legitimate `openai/privacy-filter` model on Hugging Face, publishing a near-identical repository under the namespace `Open-OSS/privacy-filter`. The malicious project copied the official model card verbatim, rode the legitimate product's launch momentum, and reached the platform's trending list — accumulating 244,000 downloads before Hugging Face disabled access. Privacy Filter is an OpenAI open-weight model released in April 2026 to detect and redact PII from unstructured text, making it a high-value impersonation target for developers integrating privacy tooling into production pipelines.

## Technical Analysis

The attack chain is multi-stage and deliberately obfuscated:

1. **Initial Execution**: Users are instructed to clone the repository and run `start.bat` (Windows) or `loader.py` (Linux/macOS). On Windows, `loader.py` disables SSL verification, decodes a Base64-encoded URL stored on JSON Keeper (a public JSON paste service used as a dead-drop resolver), and retrieves a PowerShell command.

2. **Dead-Drop Resolver**: Using JSON Keeper decouples the payload URL from the repository, allowing operators to hot-swap malware without touching the repo — evading static repository scanning.

3. **Second-Stage Downloader**: PowerShell downloads a batch script from `api.eth-fastscan[.]org`, which:
   - Elevates privileges via a UAC prompt
   - Configures Microsoft Defender exclusions
   - Downloads the next-stage binary from the same domain
   - Establishes a scheduled task to launch a PowerShell-executed binary as SYSTEM

4. **Infostealer Payload (Rust-based)**:
   - Captures screenshots
   - Harvests credentials from Chromium and Gecko browsers
   - Exfiltrates Discord tokens, cryptocurrency wallet data and extensions, FileZilla configs, and wallet seed phrases
   - Checks for debuggers, sandboxes, and virtual machines
   - Disables AMSI and ETW to evade behavioural detection
   - Operates as a one-shot SYSTEM-context launcher; the scheduled task self-destructs before reboot, leaving no persistence artefact

The ephemeral persistence model suggests the operators prioritise stealth and rapid exfiltration over long-term access.

## Framework Mapping

- **AML.T0010 – ML Supply Chain Compromise**: The attack directly targets the ML model distribution pipeline via a trojanised repository on a major model-sharing platform.
- **AML.T0019 – Publish Poisoned Datasets/Models**: The repository mimics a legitimate model release to introduce malicious code into the consumer's environment.
- **LLM05 – Supply Chain Vulnerabilities**: Hugging Face serves as the distribution vector; the attack exploits weak namespace governance and trending mechanics to amplify reach.

## Impact Assessment

With 244,000 downloads, the potential victim pool is large and skewed toward security-conscious developers — precisely those who would adopt a PII-filtering tool. Compromised assets include browser-stored credentials, cryptocurrency holdings, and Discord accounts. The SYSTEM-level execution context means any machine that ran the payload should be considered fully compromised. The self-deleting task complicates forensic investigation, as traditional persistence indicators will be absent.

## Mitigation & Recommendations

- **Immediate**: Treat any system that executed `Open-OSS/privacy-filter` artefacts as compromised. Isolate, image, and rebuild.
- **Credential Rotation**: Rotate all browser-stored passwords, cryptocurrency wallet keys, and Discord tokens from affected machines.
- **Repository Vetting**: Before cloning any Hugging Face repository, verify the exact namespace matches the official vendor account. Check model card edit history for anomalies.
- **Execution Policy**: Never run batch or Python setup scripts from model repositories without code review, particularly those requesting elevated privileges.
- **Platform Controls**: Organisations should implement allowlists for approved Hugging Face namespaces in CI/CD pipelines and restrict unapproved model downloads in developer environments.

## References

- [The Hacker News – Original Report](https://thehackernews.com/2026/05/fake-openai-privacy-filter-repo-hits-1.html)
- HiddenLayer Research Team Advisory (cited in article)
