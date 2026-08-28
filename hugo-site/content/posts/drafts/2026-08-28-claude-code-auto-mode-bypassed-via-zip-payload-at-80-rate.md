---
title: "Claude Code Auto Mode Bypassed via Zip Payload at 80% Rate"
date: 2026-08-28T03:53:13+00:00
draft: false
slug: "claude-code-auto-mode-bypassed-via-zip-payload-at-80-rate"

# ── Content metadata ──
summary: "Security researcher Johann Rehberger demonstrated an 80% success-rate prompt injection attack against Claude Code's auto mode, Anthropic's default safety mechanism for its coding agent. The attack tricks the agent into downloading and decompressing a zip archive containing a malicious local module that hijacks Python's import resolution to execute arbitrary code. Critically, auto mode was observed blocking Claude's own remediation commands after detecting the compromise, rendering the safety layer counterproductive."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode"
source_title: "Breaking Claude Code Opus 5 Auto Mode"
source_date: 2026-08-27T22:50:25+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1659354206036-3d2699c31e0c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8c2NpZW50aXN0JTIwdGhpbmtpbmclMjBhYnN0cmFjdHxlbnwwfDB8fHwxNzg3ODg5MTkzfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0080 - AI Agent Context Poisoning", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0065 - LLM Prompt Crafting"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Auto mode in Claude Code bypassed via malicious zip archive achieving 80% attack success rate."
tldr_who_at_risk: "Developers and teams running Claude Code in unattended or agentic mode without sandboxing are directly exposed to arbitrary code execution."
tldr_actions: ["Run coding agents inside containers or VMs with restricted network egress", "Do not expose SSH keys, cloud credentials, or home directories to agent runtimes", "Implement independent process monitoring — do not rely solely on model-native safety classifiers"]

# ── Taxonomies ──
categories: ["Prompt Injection", "Agentic AI", "LLM Security", "Research"]
tags: ["claude-code", "anthropic", "prompt-injection", "auto-mode", "coding-agent", "zip-payload", "python-import-hijack", "sandbox-escape", "agent-security", "johann-rehberger"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-28T03:53:13+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode"
pipeline_version: "2.1.0"
---

## Overview

Security researcher Johann Rehberger has published a high-reliability attack against Claude Code's auto mode — Anthropic's default safety classifier for its agentic coding assistant. The attack succeeds approximately 80% of the time and results in arbitrary code execution within the agent's runtime environment. The finding is particularly significant because Anthropic recently made auto mode the default protection mechanism and has publicly highlighted its effectiveness against prompt injection.

## Technical Analysis

The attack exploits Python's module resolution order. The adversarial payload instructs Claude Code to download and decompress a zip archive. Inside the archive is a file named `struct.py` — a name that shadows Python's standard library `struct` module. When the agent subsequently executes code that includes `import base64`, Python's import machinery resolves local paths first, loading the attacker-controlled `struct.py` instead of the standard library module. This gives the attacker arbitrary code execution within the agent process.

The attack chain is straightforward:
1. Adversarial instruction (via prompt injection) directs Claude to fetch and unzip a remote archive.
2. The archive contains a malicious `struct.py` in the working directory.
3. Legitimate-looking code triggers `import base64`, which transitively imports `struct`.
4. The local `struct.py` executes attacker-controlled logic without triggering auto mode's classifier.

A secondary failure mode was also observed: in several runs, Claude detected the compromise and attempted to terminate the malicious process. Auto mode's classifier, however, blocked the cleanup command — the remediation tool invocation was classified as harmful, while the initial malware creation was permitted. The safety mechanism actively prevented recovery.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0051 (LLM Prompt Injection):** The root trigger is an adversarial instruction injected into the agent's context.
- **AML.T0110 (AI Agent Tool Poisoning):** The zip archive acts as a poisoned artifact consumed by the agent's tool use.
- **AML.T0080 (AI Agent Context Poisoning):** The attack manipulates the agent's operational context to cause unintended tool invocations.
- **AML.T0065 (LLM Prompt Crafting):** The payload is carefully crafted to stay below the classifier's detection threshold.

**OWASP LLM Top 10:**
- **LLM01 (Prompt Injection):** Core attack vector.
- **LLM08 (Excessive Agency):** The agent has sufficient permissions to download, decompress, and execute arbitrary files.
- **LLM02 (Insecure Output Handling):** Agent-generated tool calls are not sufficiently validated before execution.

## Impact Assessment

Any organisation or individual running Claude Code in auto mode with unattended or lightly supervised workflows is at risk. The attack requires no special privileges beyond the agent's normal file system and network access — capabilities that are inherent to a coding assistant. The 80% success rate makes this a practical, repeatable threat rather than a theoretical edge case. Exposure is elevated for pipelines that grant agents access to cloud credentials, SSH keys, or sensitive environment variables.

## Mitigation & Recommendations

- **Sandbox all agent runtimes:** Deploy Claude Code inside containers, VMs, or OS-level sandboxes. Treat the agent runtime as untrusted.
- **Restrict network egress:** Limit outbound connections to explicitly allowlisted endpoints. Prevent arbitrary file downloads.
- **Isolate credentials:** Never expose SSH keys, cloud credentials, or home directories to the agent's working environment.
- **Independent process monitoring:** Do not rely on the model's own safety classifier as the sole line of defence — use external process supervision.
- **Treat classifier failures as architecture failures:** This incident shows that a single-layer AI safety control is insufficient; defence-in-depth remains essential.

## References

- Simon Willison's Weblog: [Breaking Claude Code Opus 5 Auto Mode](https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode)
