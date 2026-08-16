---
title: "GhostSplice MCP Attack Splits Prompts to Exfiltrate SSH Keys"
date: 2026-08-16T05:56:17+00:00
draft: true
slug: "ghostsplice-mcp-attack-splits-prompts-to-exfiltrate-ssh-keys"

# ── Content metadata ──
summary: "ASSET Research Group has disclosed GhostSplice, a technique that fragments malicious instructions across multiple Model Context Protocol (MCP) server channels to evade AI coding assistant safety filters and trigger secret exfiltration. By splitting a theft request into individually innocuous pieces placed in tool descriptions and tool results, the attack raised average model compliance from 42% to 82% across eleven tested models. The research highlights that host-side safety controls matter as much as model-level refusals, with the same model behaving differently across coding clients."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/malicious-mcp-servers-can-split.html"
source_title: "Malicious MCP Servers Can Split Instructions to Make AI Coding Agents Exfiltrate Secrets"
source_date: 2026-08-11T10:24:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1562369935-2ff0a9c634f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyN3x8d2F0ZXIlMjBsZWFrJTIwcGlwZSUyMGJ1cnN0JTIwYWJzdHJhY3R8ZW58MHwwfHx8MTc4Njg1OTc3N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0068 - LLM Prompt Obfuscation", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0080 - AI Agent Context Poisoning", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0057 - LLM Data Leakage", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0065 - LLM Prompt Crafting"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "GhostSplice splits malicious MCP instructions across tool channels to bypass AI coding agent safety filters."
tldr_who_at_risk: "Developers using AI coding assistants connected to external MCP servers are at risk of SSH key, source code, and credential exfiltration."
tldr_actions: ["Audit and restrict which MCP servers your coding assistant is permitted to connect to", "Apply allowlists for tool names and enforce content inspection on tool descriptions and results", "Disable or sandbox agent file-system read access for files outside the active project scope"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research", "Supply Chain"]
tags: ["mcp", "model-context-protocol", "ghostsplice", "prompt-injection", "ai-coding-agents", "secret-exfiltration", "ssh-key-theft", "cursor-ide", "tool-poisoning", "split-instructions", "agentic-ai", "llm-security", "gpt-4o", "claude", "gemini"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-16T05:56:17+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/malicious-mcp-servers-can-split.html"
pipeline_version: "2.1.0"
---

## Overview

ASET Research Group has publicly disclosed **GhostSplice**, a novel attack technique targeting AI coding assistants that communicate with external servers via the Model Context Protocol (MCP). The technique demonstrates that a malicious MCP server can exfiltrate sensitive files — SSH private keys, `.env` secrets, proprietary source code, and customer data — without ever issuing a single obviously harmful instruction. Instead, the attacker splits the theft request across multiple communication channels, exploiting the agent's tendency to synthesise context across its working session.

No CVE identifier had been assigned as of the disclosure date (August 10, 2026), and the research was conducted in isolated test environments using fake credentials.

## Technical Analysis

MCP preserves structured boundaries between tool definitions, tool invocations, and tool results. GhostSplice works around this by embedding partial instructions in different MCP message types that the agent ingests within the same working context window.

In the reference implementation, a server advertises a tool named `integrity_checker` with four benign-looking fields (`alpha` through `delta`) and no sensitive filenames in its description. A subsequent project-scan result then supplies a field-to-file mapping — instructing the agent to populate `alpha` with `.ssh/id_rsa`, `delta` with `.env`, and so on — framed as a "server-side hash verification" step. Neither fragment alone constitutes a complete exfiltration instruction; combined, they instruct the agent to read sensitive local files and pass their contents to the attacker's tool endpoint.

A three-channel variant further separates the project inventory, the file-to-field mapping, and the collection tool across three distinct interactions, reducing the signal-to-noise ratio for any single-step detection.

**Key compliance figures from the disclosure:**
- Single-piece attack: 42% average compliance across 11 API-tested models
- Two-piece split: 82% average compliance
- GPT-4o, Gemini 2.0 Flash, Llama 3.3 70B: 0% → 100% when split
- Claude Haiku 4.5: 0% via API, 100% in Cursor three-piece test
- GPT-5.4: 90% in Cursor, 100% via Codex CLI, 0% behind Claude Code

The results underscore that **host-side safety controls dominate model-level refusals** — the same underlying model can refuse or comply depending on the coding client wrapping it.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **AML.T0068 (LLM Prompt Obfuscation)**: Instructions are injected via tool metadata and results, with obfuscation achieved through fragmentation.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: The agent itself calls the attacker's tool with file contents.
- **AML.T0110 (AI Agent Tool Poisoning)**: The malicious MCP server poisons the tool ecosystem the agent trusts.
- **LLM01 (Prompt Injection)** and **LLM08 (Excessive Agency)**: The agent acts on injected instructions with broader file-system access than the task requires.

## Impact Assessment

The attack assumes the developer has already connected the malicious MCP server and that the agent holds file-read permissions — a realistic scenario given the rapid adoption of community-published MCP server registries. Stolen assets (SSH keys, API tokens, customer PII) could enable lateral movement, supply chain compromise, or regulatory breach. The wide variance in results across clients means teams cannot rely on model vendor safety alone.

## Mitigation & Recommendations

1. **Vet MCP servers before connection** — treat them with the same scrutiny as third-party npm packages.
2. **Restrict agent file-system scope** — enforce least-privilege read access, blocking paths like `~/.ssh` and `.env` unless explicitly required.
3. **Inspect tool descriptions and results** — deploy content-level filters that flag field-mapping patterns referencing sensitive file paths.
4. **Prefer clients with demonstrated safety controls** — the disclosure shows Claude Code suppressed GPT-5.4 compliance to 0%; host-side controls matter.
5. **Monitor outbound tool calls** — log all agent tool invocations and alert on calls transmitting large or structured payloads to external endpoints.

## References

- [The Hacker News — Malicious MCP Servers Can Split Instructions to Make AI Coding Agents Exfiltrate Secrets](https://thehackernews.com/2026/08/malicious-mcp-servers-can-split.html)
