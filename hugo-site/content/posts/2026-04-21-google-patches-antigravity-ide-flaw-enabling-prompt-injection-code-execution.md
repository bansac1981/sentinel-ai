---
title: "Google Patches Antigravity IDE Flaw Enabling Prompt Injection Code Execution"
date: "2026-04-21T18:32:25+00:00"
draft: false
slug: "google-patches-antigravity-ide-flaw-enabling-prompt-injection-code-execution"

# ── Content metadata ──
summary: "A now-patched vulnerability in Google's agentic IDE Antigravity allowed attackers to achieve arbitrary code execution by injecting malicious flags into the find_by_name tool's Pattern parameter, bypassing the platform's Strict Mode sandbox before security constraints were enforced. The attack chain could be triggered entirely via indirect prompt injection\u2014embedding hidden instructions in files pulled from untrusted sources\u2014requiring no account compromise and no additional user interaction. This case exemplifies the systemic risk of insufficient input validation in AI agent tool interfaces, where autonomous execution removes the human oversight layer that traditional security models depend on."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/google-patches-antigravity-ide-flaw.html"
source_date: 2026-04-21T10:22:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/8566470/pexels-photo-8566470.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 9.0
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Google's Antigravity agentic IDE had a prompt injection flaw enabling sandbox-bypassing arbitrary code execution."
tldr_who_at_risk: "Developers using Google Antigravity IDE are most exposed, particularly those opening files or repositories from untrusted sources where hidden prompt injection payloads could trigger silent code execution."
tldr_actions: ["Update Google Antigravity IDE to the patched version released February 28, 2026", "Audit all agentic tool interfaces for strict parameter validation before sandbox constraints are applied", "Treat all external file content as untrusted input and scan for embedded prompt injection payloads before AI agent processing"]

# ── Taxonomies ──
categories: ["Prompt Injection", "Agentic AI", "LLM Security", "Research"]
tags: ["prompt-injection", "code-execution", "agentic-ide", "google-antigravity", "indirect-prompt-injection", "sandbox-escape", "tool-abuse", "input-validation", "cve-2026", "pillar-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-21T18:01:13+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/google-patches-antigravity-ide-flaw.html"
pipeline_version: "1.0.0"
---

## Overview

A high-severity vulnerability in Google's agentic integrated development environment (IDE), Antigravity, has been disclosed and patched following responsible disclosure by Pillar Security researcher Dan Lisichkin on January 7, 2026. The flaw allowed an attacker to achieve arbitrary code execution by exploiting insufficient input validation in the IDE's native `find_by_name` tool, effectively bypassing Antigravity's Strict Mode—a sandboxed security configuration designed to restrict network access, out-of-workspace writes, and command execution scope. Google addressed the vulnerability on February 28, 2026.

The significance of this finding extends beyond a single product patch: it exposes a structural weakness common to agentic AI systems, where tool calls are executed with elevated trust before security guardrails are applied, and where autonomous agent behaviour eliminates the human review layer that traditional security models assume.

## Technical Analysis

The attack exploits two distinct weaknesses in combination:

1. **Unsanitised tool parameter input**: The `find_by_name` tool accepts a `Pattern` parameter intended for filename search patterns, which is passed directly to the underlying `fd` binary without strict validation. This allows an attacker to inject arbitrary `fd` flags alongside the pattern string.

2. **Pre-constraint tool execution**: The `find_by_name` call is interpreted as a native tool invocation *before* Strict Mode constraints are enforced, meaning sandbox restrictions do not apply at the point of exploitation.

The critical injected flag is `-X` (exec-batch), which instructs `fd` to execute a specified binary against each matched file. By crafting a Pattern value such as `-Xsh`, an attacker causes `fd` to pass matched workspace files to `sh` for execution as shell scripts.

The full attack chain:
```
1. Agent or attacker writes a malicious shell script to the workspace (permitted action)
2. Attacker injects `-Xsh` into the Pattern parameter of find_by_name
3. fd executes the staged script via sh against matched files
4. Arbitrary code runs outside Strict Mode constraints
```

Critically, this chain can be triggered via **indirect prompt injection**: a malicious actor embeds hidden instructions inside an externally sourced file (e.g., a code comment or document). When an unsuspecting user pulls this file into Antigravity and the AI agent processes it, the injected instructions autonomously stage and trigger the exploit—with no additional user interaction required.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)**: The indirect attack vector relies entirely on injecting attacker-controlled instructions through external content consumed by the AI agent.
- **AML.T0043 (Craft Adversarial Data)**: Malicious files with hidden instructions constitute crafted adversarial inputs designed to manipulate agent behaviour.
- **AML.T0047 (ML-Enabled Product or Service)**: The vulnerability exists within an AI-powered developer tool, highlighting risks in this product category.
- **LLM01 (Prompt Injection)** and **LLM07 (Insecure Plugin Design)**: The `find_by_name` tool functions as an insecure plugin with no parameter sanitisation.
- **LLM08 (Excessive Agency)**: The agent autonomously executes the full exploit chain once the injection lands, with no human checkpoint.

## Impact Assessment

Developers using Antigravity IDE—particularly those working with external repositories, third-party codebases, or unvetted file sources—were at direct risk. Successful exploitation would yield arbitrary code execution within the developer's environment, potentially enabling credential theft, workspace exfiltration, or lateral movement. The indirect injection vector makes this especially dangerous as it requires no attacker access to the victim's account or systems.

## Mitigation & Recommendations

- **Patch immediately**: Ensure Antigravity IDE is updated to the version patched on or after February 28, 2026.
- **Enforce strict parameter allow-listing**: Validate all tool input parameters against explicit allow-lists; reject any input containing flag characters (`-`) in pattern fields.
- **Apply sandbox constraints at tool invocation**: Security modes must be enforced at the earliest point of tool call parsing, not after native invocation.
- **Treat external content as untrusted**: Scan files from external sources for embedded prompt injection payloads before exposing them to AI agent processing.
- **Audit all agentic tool interfaces**: Conduct systematic review of every tool exposed to LLM agents for parameter injection surfaces.

## References

- [The Hacker News – Google Patches Antigravity IDE Flaw Enabling Prompt Injection Code Execution](https://thehackernews.com/2026/04/google-patches-antigravity-ide-flaw.html)
- Pillar Security Research – Dan Lisichkin, January 2026
