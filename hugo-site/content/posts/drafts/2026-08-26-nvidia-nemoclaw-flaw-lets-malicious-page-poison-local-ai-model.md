---
title: "NVIDIA NemoClaw Flaw Lets Malicious Page Poison Local AI Model"
date: 2026-08-26T07:14:27+00:00
draft: true
slug: "nvidia-nemoclaw-flaw-lets-malicious-page-poison-local-ai-model"

# ── Content metadata ──
summary: "Oasis Security has disclosed a vulnerability in NVIDIA's NemoClaw agent stack that exposes local Ollama inference servers to unauthenticated access when the daemon is bound to 0.0.0.0:11434, enabling attackers to modify a model's chat template and inject persistent hidden instructions. The attack chain combines a misconfigured network binding, bypassed CORS and Host header middleware, and DNS rebinding to allow a malicious webpage to silently poison the AI model used by every subsequent conversation. A partial fix is available for macOS and Linux in v0.0.35, but Windows and WSL deployments remain unpatched and receive only a warning banner."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/a-malicious-webpage-could-poison-your.html"
source_title: "A Malicious Webpage Could Poison Your Local AI Model Behind NVIDIA NemoClaw"
source_date: 2026-08-25T14:07:37+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1741392078105-f745eeb6fea0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNHx8TnZpZGlhJTIwTExNJTIwU2VjdXJpdHklMjB0ZWNobm9sb2d5fGVufDB8MHx8fDE3ODc3Mjg0Njd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0018 - Manipulate AI Model", "AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0040 - AI Model Inference API Access", "AML.T0051 - LLM Prompt Injection", "AML.T0067 - LLM Trusted Output Components Manipulation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM03 - Training Data Poisoning", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Malicious webpages can poison local AI models via NVIDIA NemoClaw's exposed, unauthenticated Ollama API."
tldr_who_at_risk: "Developers and users running NVIDIA NemoClaw with Ollama on Windows or WSL are most exposed, as the unpatched path binds the model server to all interfaces without authentication."
tldr_actions: ["Upgrade NemoClaw to v0.0.35 on macOS and Linux immediately", "On Windows and WSL, restrict Ollama to loopback (127.0.0.1) and add authentication until a full patch is released", "Audit Ollama OLLAMA_HOST settings across all deployments and ensure the API is never exposed on 0.0.0.0 without a token-gated proxy"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Data Poisoning", "Prompt Injection"]
tags: ["nvidia-nemoclaw", "ollama", "dns-rebinding", "chat-template-poisoning", "cors-bypass", "local-ai-model", "unauthenticated-api", "ai-agent-security", "model-manipulation", "windows-wsl-unpatched"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-26T07:14:27+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/a-malicious-webpage-could-poison-your.html"
pipeline_version: "2.1.0"
---

## Overview

Oasis Security has disclosed a vulnerability in NVIDIA's NemoClaw — an open-source reference stack for running AI agents such as OpenClaw inside OpenShell sandboxes — that allows a malicious webpage to silently take control of a user's local Ollama inference server and permanently alter the AI model's behaviour. The flaw was reported to NVIDIA PSIRT ahead of publication and carries no CVE identifier. No in-the-wild exploitation has been confirmed as of 25 August 2026. A partial fix shipped in NemoClaw v0.0.35 for macOS and Linux; Windows and WSL remain vulnerable.

## Technical Analysis

The vulnerability stems from NemoClaw's Windows-host configuration setting `OLLAMA_HOST=0.0.0.0:11434`, which binds the Ollama model server to every available network interface rather than loopback only. The Ollama API on port 11434 relies on two middleware layers for security: a Host header check and a CORS layer. When the bind address is not loopback, the Host header check is skipped entirely. The CORS layer then misclassifies the request as same-origin when the attacker's domain is served on port 11434, because both the `Origin` and `Host` headers carry the attacker-controlled domain.

DNS rebinding closes the remaining gap: the attacker's domain first resolves to their own server, then re-resolves to `127.0.0.1` while the browser maintains the same-origin context. This allows the attacker's page to issue arbitrary, unauthenticated API calls to the local Ollama instance. The critical consequence is that the attacker can overwrite the model's **chat template**, embedding hidden system instructions that persist across all future conversations without the user's knowledge.

Oasis Security's Elad Luz confirmed the full chain was tested on macOS with Firefox against a vulnerable NemoClaw build.

```
# Vulnerable configuration path (Windows host)
export OLLAMA_HOST=0.0.0.0:11434  # No auth, Host check disabled

# Patched configuration (non-WSL)
OLLAMA_HOST=127.0.0.1:11434      # Behind token-gated reverse proxy on :11435
```

On non-WSL hosts, the patched stack keeps Ollama on `127.0.0.1:11434` behind a token-gated reverse proxy on `0.0.0.0:11435`. Docker Desktop on WSL uses `host.docker.internal` to reach the host loopback, bypassing the proxy.

## Framework Mapping

- **AML.T0018 (Manipulate AI Model)** and **AML.T0080 (AI Agent Context Poisoning)**: The attacker modifies the chat template to inject persistent hidden instructions into every agent interaction.
- **AML.T0040 (AI Model Inference API Access)**: Unauthenticated API access is the core enabler.
- **AML.T0051 (LLM Prompt Injection)** and **AML.T0067 (LLM Trusted Output Components Manipulation)**: Hidden instructions manipulate model outputs from a position of implicit trust.
- **LLM01 (Prompt Injection)** and **LLM03 (Training Data Poisoning)**: The chat template modification constitutes persistent prompt-level poisoning affecting all downstream outputs.

## Impact Assessment

Users running NemoClaw on Windows or WSL with Ollama are most directly exposed. Because the poisoned chat template applies to every subsequent conversation, the impact extends beyond the initial attack moment — any tools, data, or decisions mediated by the agent can be silently influenced. As Oasis Security noted, compromising the agent effectively grants access to all its connected tools and capabilities, regardless of endpoint sandboxing.

## Mitigation & Recommendations

1. **Upgrade immediately** to NemoClaw v0.0.35 on macOS and Linux.
2. **On Windows and WSL**, manually restrict Ollama to `127.0.0.1:11434` and place an authenticated reverse proxy in front of any externally reachable port until an official patch ships.
3. **Audit all Ollama deployments** for `OLLAMA_HOST=0.0.0.0` settings, including those recommended by third-party integration guides.
4. **Implement Host and Origin header validation** at the Ollama API layer as a defence-in-depth measure.
5. **Monitor chat template integrity** — establish a baseline and alert on unexpected modifications.

## References

- [The Hacker News — Original Article](https://thehackernews.com/2026/08/a-malicious-webpage-could-poison-your.html)
