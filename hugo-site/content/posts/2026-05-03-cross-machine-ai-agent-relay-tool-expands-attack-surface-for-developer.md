---
title: "Loopsy AI Agent Relay Enables Cross-Machine RCE"
date: "2026-05-03T03:31:51+00:00"
draft: false
slug: "cross-machine-ai-agent-relay-tool-expands-attack-surface-for-developer"

# ── Content metadata ──
summary: "Loopsy is an open-source tool enabling cross-machine communication between AI coding agents (Claude Code, Cursor, Codex) and mobile devices via a self-hosted Cloudflare Workers relay. While designed for legitimate developer productivity, the architecture introduces significant attack surface: a relay brokering shell access and AI agent commands across machines is a high-value target for interception, hijacking, or supply chain compromise. Security teams should assess exposure before deploying such tools in sensitive development environments."
source: "HN AI Security"
source_url: "https://github.com/leox255/loopsy"
source_title: "Show HN: Loopsy, a way for terminals and AI agents on different machines to talk"
source_date: 2026-05-01T10:25:41+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://plus.unsplash.com/premium_photo-1677194598974-9b925fec1f46?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0010 - ML Supply Chain Compromise", "AML.T0051 - LLM Prompt Injection", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM05 - Supply Chain Vulnerabilities", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Loopsy relays AI agent commands and shell access across machines via a self-hosted Cloudflare Worker."
tldr_who_at_risk: "Developers using AI coding agents (Claude Code, Cursor, Codex) who deploy Loopsy are exposed to relay hijacking, prompt injection via mobile input, and lateral movement if the relay is compromised."
tldr_actions: ["Audit network exposure of any Cloudflare Worker relay before deploying Loopsy in production or sensitive environments", "Restrict shell command scope accessible via the relay using allowlists and sandboxing", "Treat mobile-originated inputs to AI agents as untrusted and apply prompt injection defences before execution"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security", "Industry News"]
tags: ["ai-agent", "remote-code-execution", "cross-machine-communication", "cloudflare-workers", "developer-tools", "terminal-access", "agentic-ai", "supply-chain", "self-hosted", "claude-code", "cursor", "codex"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-03T03:00:24+00:00"
feed_source: "hn_ai_security"
original_url: "https://github.com/leox255/loopsy"
pipeline_version: "1.0.0"
---

## Overview

Loopsy is an open-source developer tool (GitHub: leox255/loopsy) that enables cross-machine communication between AI coding agents — including Claude Code, Cursor, and OpenAI Codex — and mobile devices. The system uses a self-hosted relay on Cloudflare Workers to broker terminal commands and AI agent interactions from a smartphone to a developer's laptop. While framed as a productivity enhancement, the architecture represents a meaningful expansion of the attack surface surrounding agentic AI workflows.

As AI coding agents gain autonomous shell access and the ability to execute code, tools that extend their reachability across network boundaries deserve close security scrutiny.

## Technical Analysis

Loopsy's architecture consists of three components:

1. **A laptop-side daemon** — installed globally via `npm install -g loopsy`, it exposes terminal and AI agent interfaces to the relay.
2. **A Cloudflare Workers relay** — self-hosted by the user, acting as the broker between mobile and laptop. Commands and responses are tunnelled through this relay.
3. **A mobile app** — sends instructions to the relay, which forwards them to the AI agent or shell on the target machine.

From a security perspective, several risks emerge:

- **Relay as a single point of compromise**: If the Cloudflare Worker is misconfigured, lacks authentication, or is targeted via a supply chain attack on the npm package, an attacker gains a pathway to issue arbitrary shell commands or inject instructions into AI agent sessions.
- **Prompt injection via mobile input**: Any text entered via the mobile app and forwarded to an AI agent (e.g., Claude Code) could carry injected instructions if the input originates from an untrusted or attacker-controlled source.
- **Excessive agency**: AI agents operating in agentic mode with shell access, now controllable from a mobile device over a network relay, represent a textbook case of excessive agency — a broad action envelope with limited contextual guardrails.
- **npm supply chain risk**: The global npm install and a separate deploy package (`@loopsy/deploy-relay`) introduce supply chain dependency risks. Malicious package versions could backdoor both the relay and the local daemon.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)**: Mobile-sourced inputs forwarded to AI agents without sanitisation are a vector for prompt injection.
- **AML.T0010 (ML Supply Chain Compromise)**: The npm-distributed daemon and relay packages are potential supply chain targets.
- **LLM08 (Excessive Agency)**: The tool explicitly extends AI agent action scope across machine boundaries via a network relay.
- **LLM07 (Insecure Plugin Design)**: The relay-to-agent integration lacks documented input validation or sandboxing controls.

## Impact Assessment

Developers running AI coding agents with shell access in corporate or sensitive environments are most at risk. A compromised relay could enable lateral movement, data exfiltration from the development environment, or injection of malicious code into AI-assisted workflows. The impact is elevated by the tool's design goal: seamless, low-friction remote control.

## Mitigation & Recommendations

- **Enforce relay authentication**: Ensure the Cloudflare Worker requires strong authentication tokens; do not expose it publicly without access controls.
- **Scope-limit shell access**: Use allowlists to restrict which commands AI agents can execute when invoked via the relay.
- **Sanitise all mobile inputs**: Treat inputs from the mobile app as untrusted; apply prompt injection defences before passing to any AI agent.
- **Pin npm dependencies**: Lock and audit the `loopsy` and `@loopsy/deploy-relay` packages to prevent supply chain substitution.
- **Network segmentation**: Avoid deploying Loopsy on machines with access to production systems or sensitive credentials.

## References

- [Loopsy GitHub Repository](https://github.com/leox255/loopsy)
- [loopsy.dev](https://loopsy.dev)
