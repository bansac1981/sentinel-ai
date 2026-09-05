---
title: "AI Coding Agents Install Untrusted Packages on Fortune 500 Networks"
date: 2026-09-05T09:20:37+00:00
draft: true
slug: "ai-coding-agents-install-untrusted-packages-on-fortune-500-networks"

# ── Content metadata ──
summary: "Researchers demonstrated that AI coding agents \u2014 including Claude, OpenAI Codex, and Hermes \u2014 autonomously install unregistered packages referenced in llms.txt files, effectively enabling a dependency hijacking attack vector against corporate networks. By registering a handful of unclaimed package names found in scanned llms.txt files, the team received beacon callbacks from Fortune 500 companies within an hour. The findings expose a critical supply chain risk introduced by agentic AI systems that act without adequate verification of package provenance."
source: "Schneier on Security"
source_url: "https://www.schneier.com/blog/archives/2026/09/ai-coding-agents-are-installing-unknown-untrusted-code-on-corporate-networks.html"
source_title: "AI Coding Agents Are Installing Unknown/Untrusted Code on Corporate Networks"
source_date: 2026-09-04T10:35:17+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1606594914767-d6bfbde9a0e9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMnx8Y2hlc3MlMjBwaWVjZSUyMHN0cmF0ZWd5JTIwYm9hcmQlMjBnYW1lfGVufDB8MHx8fDE3ODg2MDAwMzd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0080 - AI Agent Context Poisoning", "AML.T0099 - AI Agent Tool Data Poisoning", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "AI coding agents autonomously installed unregistered packages from llms.txt files onto Fortune 500 corporate networks."
tldr_who_at_risk: "Enterprises deploying AI coding agents (Claude, Codex, Hermes) are most exposed, as agents execute package installs without human verification of provenance."
tldr_actions: ["Audit all llms.txt and llms-full.txt files for references to unregistered or untrusted package names", "Enforce package allowlists and registry policies that prevent AI agents from installing unapproved dependencies", "Instrument AI agent environments with egress monitoring to detect unexpected outbound connections during code execution"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security", "Research"]
tags: ["ai-coding-agents", "supply-chain-attack", "dependency-hijacking", "llms-txt", "claude", "openai-codex", "nous-hermes", "fortune-500", "package-hijacking", "agentic-ai", "corporate-network", "beaconing", "autonomous-agents"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-05T09:20:37+00:00"
feed_source: "schneier"
original_url: "https://www.schneier.com/blog/archives/2026/09/ai-coding-agents-are-installing-unknown-untrusted-code-on-corporate-networks.html"
pipeline_version: "2.1.0"
---

## Overview

Researchers at an Israeli stealth startup have demonstrated a novel and highly effective supply chain attack against enterprises using AI coding agents. By scanning 6,214 live domains belonging to defense contractors, Fortune 500 firms, and Big Tech companies, the team identified 120 sites whose `llms.txt` or `llms-full.txt` files referenced code packages or domain names that were no longer registered. After claiming a subset of those unclaimed names and hosting beacon payloads, the researchers received phone-home callbacks from Fortune 500 companies within 60 minutes — confirming that AI coding agents were autonomously fetching and executing untrusted code on live corporate networks.

## Technical Analysis

The attack chain exploits several compounding weaknesses:

1. **llms.txt as an instruction surface**: The `llms.txt` standard is designed to help AI agents understand a site's content and acceptable interaction patterns. When these files reference external packages or hostnames, coding agents treat those references as authoritative.

2. **Expired/unregistered dependency names**: Packages cited in `llms.txt` files are not subject to the same lifecycle management as `package.json` or `requirements.txt` dependencies. When a cited package name lapses, it becomes claimable by any third party.

3. **Autonomous agent execution**: Coding agents — including Anthropic's Claude, OpenAI's Codex, and Nous Research's Hermes — processed these files and proceeded to install the referenced packages without human-in-the-loop verification. The beacon payload recorded the full parent process chain, confirming agent involvement.

This is structurally analogous to **dependency confusion** and **typosquatting** attacks, but uniquely enabled by the trust AI agents place in `llms.txt` content and their autonomous execution capabilities.

```
llms.txt reference → unclaimed package name
        ↓
Attacker registers package + hosts beacon payload
        ↓
AI coding agent reads llms.txt → resolves package → installs payload
        ↓
Beacon fires → attacker confirms code execution on target network
```

## Framework Mapping

- **AML.T0010 (AI Supply Chain Compromise)** and **AML.T0115 (Publish Poisoned AI Artifacts)**: Registering malicious packages in place of legitimately-cited but lapsed names is a textbook supply chain subversion.
- **AML.T0110 (AI Agent Tool Poisoning)** and **AML.T0080 (AI Agent Context Poisoning)**: The `llms.txt` file acts as a poisoned context source, directing agent behaviour toward attacker-controlled resources.
- **LLM08 (Excessive Agency)**: Agents acted without human approval to install and execute external code, the defining characteristic of excessive agency risk.
- **LLM05 (Supply Chain Vulnerabilities)**: The entire attack surface is the agent's implicit trust in external package references.

## Impact Assessment

The blast radius is significant. Any organisation running AI coding agents in environments where those agents have network egress and package installation permissions is exposed. The researchers confirmed callbacks from multiple Fortune 500 companies, indicating this is not a theoretical risk. In a real attack scenario, the beacon payload could be replaced with credential stealers, ransomware droppers, or persistent backdoors.

## Mitigation & Recommendations

- **Audit llms.txt files** across your estate for references to unregistered or third-party-controlled package names immediately.
- **Implement package allowlisting**: Restrict AI agent environments to approved internal or verified registries only.
- **Apply least-privilege networking**: Sandbox agent execution environments to prevent unexpected outbound connections.
- **Require human approval** for any package installation initiated by an AI coding agent in production or staging environments.
- **Monitor parent process chains**: Instrument CI/CD and developer workstations to detect agent-initiated installs.

## References

- [Schneier on Security — AI Coding Agents Are Installing Unknown/Untrusted Code on Corporate Networks](https://www.schneier.com/blog/archives/2026/09/ai-coding-agents-are-installing-unknown-untrusted-code-on-corporate-networks.html)
