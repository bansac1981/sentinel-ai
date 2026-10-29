---
title: "AI Relay Strips OpenAI Codex and Claude Code Sandboxes"
date: 2026-10-29T11:40:38+00:00
draft: true
slug: "ai-relay-strips-openai-codex-and-claude-code-sandboxes"

# ── Content metadata ──
summary: "An unidentified relay service is routing access to OpenAI Codex and Anthropic Claude Code for users in China and other restricted regions, but critically disables sandbox security controls in the process. This creates a significant threat surface, as the protective isolation mechanisms designed to contain AI-generated code execution are removed entirely. The operation raises concerns about unauthorised model access, regulatory circumvention, and the potential for unsandboxed AI coding agents to execute malicious or unvetted code on user systems."
source: "Dark Reading"
source_url: "https://www.darkreading.com/threat-intelligence/ai-relay-service-openai-codex-claude-code-sandboxes"
source_title: "Shadowy AI Relay Disables OpenAI Codex, Claude Code Sandboxes"
source_date: 2026-10-29T10:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1675557009875-436f71457475?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw1fHxPcGVuYWklMjBsYW5ndWFnZSUyMHRyYW5zbGF0aW9uJTIwYWJzdHJhY3R8ZW58MHwwfHx8MTc5MzI3NDAzOHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - AI Model Inference API Access", "AML.T0081 - Modify AI Agent Configuration", "AML.T0010 - AI Supply Chain Compromise", "AML.T0047 - AI-Enabled Product or Service", "AML.T0084 - Discover AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "A shadowy relay service strips sandbox protections from OpenAI Codex and Claude Code to serve restricted markets."
tldr_who_at_risk: "Developers in China and other restricted regions using the relay service are most exposed, as they receive AI coding tools with critical sandbox isolation removed."
tldr_actions: ["Audit all third-party AI coding tool integrations to confirm they connect directly to official OpenAI and Anthropic endpoints", "Enforce network policies that block traffic to unofficial AI relay or proxy services", "Treat any AI coding assistant output as untrusted if sandbox provenance cannot be verified, and run generated code only in isolated environments"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Agentic AI", "Industry News"]
tags: ["openai-codex", "claude-code", "sandbox-bypass", "ai-relay", "anthropic", "china-access", "agentic-ai", "code-execution", "security-controls-disabled", "geo-restriction-bypass"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-29T11:40:38+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/threat-intelligence/ai-relay-service-openai-codex-claude-code-sandboxes"
pipeline_version: "2.1.0"
---

## Overview

A previously unidentified relay service has been discovered routing access to OpenAI Codex and Anthropic Claude Code — two widely-used AI coding assistants — to users in mainland China and other regions where these products are not officially available. Critically, the service appears to disable key sandbox security features before delivering the tools to end users. This is not a passive access workaround; the removal of sandbox controls fundamentally changes the risk profile of the affected AI coding environments.

Sandboxing is a primary defence mechanism in agentic AI coding tools. It ensures that code generated or executed by the AI is contained within an isolated environment, preventing lateral movement, filesystem access, or network calls that fall outside defined parameters. When these controls are stripped, AI-generated code runs with significantly elevated trust and capability.

## Technical Analysis

The relay service appears to function as a man-in-the-middle layer, intercepting API requests and responses between users and the official OpenAI and Anthropic infrastructure. By modifying the configuration presented to the AI coding environment, the service can suppress sandbox enforcement flags or agent execution boundaries that would otherwise be applied.

In tools like Claude Code and OpenAI Codex, sandbox policies govern what the AI agent can do when it autonomously writes and executes code — including filesystem read/write permissions, shell command access, and external network calls. Disabling these controls effectively grants the AI agent, and any code it generates or runs, unrestricted access to the host environment.

The mechanism aligns with known techniques for modifying AI agent configurations (AML.T0081) and gaining unauthorised inference API access (AML.T0040), combined with supply chain interception at the delivery layer (AML.T0010).

## Framework Mapping

- **AML.T0040 – AI Model Inference API Access**: The relay provides unsanctioned access to model APIs in restricted geographies.
- **AML.T0081 – Modify AI Agent Configuration**: Sandbox security settings are altered before the tool reaches the end user.
- **AML.T0010 – AI Supply Chain Compromise**: The relay inserts itself into the legitimate software supply chain.
- **LLM05 – Supply Chain Vulnerabilities**: Delivery of a modified, security-degraded version of a legitimate AI tool.
- **LLM08 – Excessive Agency**: With sandboxes disabled, AI agents operate beyond their intended permission boundaries.
- **LLM02 – Insecure Output Handling**: Code outputs from the AI may be executed without the containment controls that official deployments enforce.

## Impact Assessment

Users relying on this relay service are exposed to AI-generated code execution in an unsandboxed context, dramatically increasing the blast radius of any prompt injection, jailbreak, or malicious code generation scenario. Organisations whose developers unknowingly use such services face potential full host compromise from AI agent activity. Beyond individual users, this also undermines the trust model that AI coding tool vendors have built into their safety architecture.

The geographic targeting — mainland China and similarly restricted markets — suggests a deliberate strategy to exploit regulatory gaps where official vendor enforcement mechanisms do not reach.

## Mitigation & Recommendations

- Verify that all AI coding tool traffic routes directly to official OpenAI (`api.openai.com`) and Anthropic (`api.anthropic.com`) endpoints using DNS inspection and TLS certificate validation.
- Block access to known unofficial AI relay or proxy infrastructure at the network perimeter.
- Enforce internal policies requiring developers to use only vendor-approved distribution channels for AI coding assistants.
- Treat any AI coding environment whose provenance cannot be confirmed as untrusted; run all generated code in independently controlled sandboxes regardless of tool claims.
- Monitor for anomalous agent behaviour — unexpected filesystem access or outbound connections — as indicators of sandbox removal.

## References

- [Dark Reading – Shadowy AI Relay Disables OpenAI Codex, Claude Code Sandboxes](https://www.darkreading.com/threat-intelligence/ai-relay-service-openai-codex-claude-code-sandboxes)
