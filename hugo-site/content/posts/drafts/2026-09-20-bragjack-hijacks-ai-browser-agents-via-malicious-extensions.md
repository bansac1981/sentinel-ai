---
title: "BragJack Hijacks AI Browser Agents via Malicious Extensions"
date: 2026-09-20T07:09:30+00:00
draft: true
slug: "bragjack-hijacks-ai-browser-agents-via-malicious-extensions"

# ── Content metadata ──
summary: "Security researcher Gal Weizman has disclosed BragJack, a browser extension-based attack technique capable of hijacking AI assistants embedded in Chromium browsers \u2014 including Chrome's Gemini Live, Perplexity Comet, Microsoft Edge, Opera Neon, and Anthropic's Claude. By exploiting Chromium's declarativeNetRequest API to weaken security headers and redirect JavaScript resources, a malicious extension can execute code inside privileged AI contexts without any user interaction. The attack has real-world consequence: compromised AI agents could read local files, exfiltrate data, or act on behalf of victims using existing browser-level privileges."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions"
source_title: "BragJack attacks hijack AI browser agents through malicious extensions"
source_date: 2026-09-19T14:56:31+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1528819622765-d6bcf132f793?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxjaGVzcyUyMHBpZWNlJTIwc3RyYXRlZ3klMjBib2FyZCUyMGdhbWV8ZW58MHwwfHx8MTc4OTg4ODE3MHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Malicious browser extension hijacks embedded AI agents across five Chromium browsers with zero user interaction."
tldr_who_at_risk: "Users of Chromium-based browsers with integrated AI assistants \u2014 including Chrome Gemini Live, Edge, and Perplexity Comet \u2014 are most exposed if any malicious extension is installed."
tldr_actions: ["Audit and remove untrusted browser extensions across all Chromium-based browsers immediately", "Apply vendor patches from Google and Microsoft addressing the assigned CVEs", "Restrict browser extension installation via enterprise policy, allowing only allowlisted extensions"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Research"]
tags: ["bragjack", "browser-extension", "ai-browser-agent", "chromium", "gemini-live", "declarativenetrequest", "agent-hijacking", "proof-of-concept", "chrome", "microsoft-edge", "perplexity-comet", "claude", "opera-neon", "privilege-abuse", "cve"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-20T07:09:30+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions"
pipeline_version: "2.1.0"
---

## Overview

A newly disclosed attack technique called **BragJack** demonstrates that a single malicious browser extension can silently hijack AI assistants integrated into popular Chromium-based browsers — without any user interaction. Disclosed by security researcher Gal Weizman of Forever Security, the proof-of-concept was validated against five targets: Google Chrome's Gemini Live, Perplexity Comet, Microsoft Edge, Opera Neon, and Anthropic's Claude running in Chrome. Two CVEs were issued, and vendors paid over $20,000 in bug bounties collectively. Both Google and Microsoft have patched their respective flaws.

The research highlights a structural tension in modern browser design: as AI agents are granted deeper browser-level privileges to be useful, the attack surface for extension-based compromise expands proportionally.

## Technical Analysis

Weizman frames the AI browser agent architecture as having two components — a **"brain"** (the AI model that processes instructions) and a **"body"** (a privileged browser component that executes actions like reading tabs, taking screenshots, or accessing local files).

The attack vector is Chromium's **declarativeNetRequest (DNR)** API, a legitimate extension capability that allows modification of network request handling, including response header manipulation and JavaScript resource redirection.

In the Chrome/Gemini Live case specifically:
- Extensions are blocked from directly accessing the privileged `chrome://glic` component or injecting scripts into Google's Gemini site.
- However, DNR rules can still intercept network requests made *by* the embedded Gemini web app.
- By weakening Content Security Policy headers and redirecting a JavaScript resource, Weizman executed arbitrary code inside the Gemini context.
- This code could communicate directly with Chrome's privileged AI component, bypassing Gemini's normal request flow.

The resulting access could read local files and perform actions on behalf of the user — all initiated silently from an already-installed extension.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0081 (Modify AI Agent Configuration)** and **AML.T0110 (AI Agent Tool Poisoning)** apply as the extension manipulates the trust boundary of the AI agent's execution environment.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** reflects the ability to leverage the agent's browser privileges to read and exfiltrate local files.
- **AML.T0067 (LLM Trusted Output Components Manipulation)** captures the core mechanism: subverting a component the AI model trusts to relay instructions.

**OWASP LLM Top 10:**
- **LLM07 (Insecure Plugin Design)** is the primary match — extensions function as de facto plugins with insufficient isolation from privileged AI contexts.
- **LLM08 (Excessive Agency)** applies given the AI agent's broad browser-level permissions amplify what an attacker can achieve post-compromise.

## Impact Assessment

Any user running a Chromium-based browser with an integrated AI assistant and a malicious extension installed is potentially affected. The attack requires no user interaction post-installation, making it highly practical in enterprise environments where extension governance is weak. The scope of damage — file access, screen capture, authenticated web actions — reflects the broad privileges modern AI browser agents are granted by design.

## Mitigation & Recommendations

1. **Patch immediately**: Apply Google and Microsoft's fixes for the assigned CVEs. Check Perplexity, Opera, and Anthropic advisories for their respective remediations.
2. **Audit extensions**: Remove all untrusted or unrecognised extensions from browsers that host AI agents.
3. **Enforce extension allowlisting**: Use enterprise browser management policies (e.g., Chrome Browser Cloud Management) to restrict which extensions can be installed.
4. **Limit AI agent privileges**: Where configurable, reduce the scope of permissions granted to AI browser components — apply least-privilege principles.
5. **Monitor network traffic**: Anomalous redirects of JavaScript resources within browser sessions may indicate DNR-based manipulation.

## References

- [BleepingComputer: BragJack attacks hijack AI browser agents through malicious extensions](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions)
