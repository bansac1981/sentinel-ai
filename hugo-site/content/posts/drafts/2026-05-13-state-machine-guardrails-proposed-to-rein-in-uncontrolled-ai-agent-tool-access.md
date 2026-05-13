---
title: "State Machine Guardrails Proposed to Rein In Uncontrolled AI Agent Tool Access"
date: 2026-05-13T05:07:50+00:00
draft: true
slug: "state-machine-guardrails-proposed-to-rein-in-uncontrolled-ai-agent-tool-access"

# ── Content metadata ──
summary: "Statewright is an open-source framework that enforces state machine constraints on AI agents, restricting which tools agents can invoke during each phase of a workflow. The project directly addresses the Excessive Agency problem, where AI agents operating with broad, unconstrained tool access can take unintended or harmful actions. While a defensive development rather than a threat disclosure, it signals growing practitioner awareness of agentic AI risk and offers a concrete mitigation pattern for teams deploying coding agents like Claude Code, Codex, or Cursor."
source: "HN AI Security"
source_url: "https://github.com/statewright/statewright"
source_title: "Show HN: Statewright \u2013 Visual state machines that make AI agents reliable"
source_date: 2026-05-12T14:24:55+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/5866051/pexels-photo-5866051.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM01 - Prompt Injection"]

# ── TL;DR ──
tldr_what: "Statewright enforces state-machine guardrails limiting which tools AI coding agents can call per workflow phase."
tldr_who_at_risk: "Development teams using autonomous AI coding agents (Claude Code, Codex, Cursor) where unrestricted tool access could trigger unintended or destructive actions."
tldr_actions: ["Audit all tool permissions granted to AI agents and restrict access to the minimum required per workflow phase", "Evaluate state machine or policy-based guardrail frameworks before deploying autonomous AI agents in production pipelines", "Validate third-party AI agent plugins (e.g. via MCP or marketplace) against insecure plugin design criteria before installation"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Research", "Industry News"]
tags: ["agentic-ai", "state-machines", "tool-use-control", "excessive-agency", "ai-guardrails", "claude-code", "codex", "cursor", "llm-security", "open-source", "plugin-security", "workflow-enforcement"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-13T05:07:50+00:00"
feed_source: "hn_ai_security"
original_url: "https://github.com/statewright/statewright"
pipeline_version: "1.0.0"
---

## Overview

Statewright is an open-source Rust-based framework published on GitHub that applies formal state machine constraints to AI coding agents. The core idea is straightforward: rather than allowing an AI agent unrestricted access to all available tools at all times, Statewright enforces phase-gated permissions — an agent in a 'bugfix' workflow's diagnosis phase cannot invoke deployment or file-deletion tools, for example. The tagline sums up the design philosophy succinctly: *"Agents are suggestions, states are laws."*

The project currently integrates with Claude Code, Codex, Cursor, opencode, and Pi, and is installable as a plugin via Claude Code's marketplace. With 161 GitHub stars and early community interest, it represents a practitioner-led response to the Excessive Agency risk that has become one of the most actively discussed concerns in agentic AI deployment.

## Technical Analysis

Statewright defines workflows as declarative state graphs. Each state node specifies which tools are permitted, and transitions between states are governed by explicit conditions. When an agent attempts to invoke a tool not permitted in the current state, the framework blocks the call before execution.

This approach addresses two distinct risk surfaces:

1. **Unintended lateral action** — an LLM that hallucinates a tool call or misinterprets scope cannot execute it if the state machine disallows it.
2. **Prompt injection escalation** — a malicious instruction embedded in external content (e.g. a source file the agent is reviewing) that attempts to redirect the agent to a destructive tool call is constrained by the active state's permission set, reducing blast radius.

The plugin architecture (integrating with Claude's MCP-adjacent plugin system) also introduces its own consideration: plugin installation itself is a trust boundary. The README notes that Claude may initially resist API key input and advises users to insist — a friction point that, while security-motivated on Claude's part, illustrates the tension between agent caution and usability.

## Framework Mapping

- **LLM08 (Excessive Agency)**: The primary motivation for Statewright. Unrestricted tool access in LLM agents is the canonical Excessive Agency pattern; state machines are a direct structural mitigation.
- **LLM07 (Insecure Plugin Design)**: Statewright itself is deployed as a plugin, and its correct functioning depends on the integrity of the plugin trust chain.
- **LLM01 (Prompt Injection)** / **AML.T0051**: State-gated tool access reduces the exploitability of prompt injection attacks by limiting what an injected instruction can actually cause an agent to do.
- **AML.T0047 (ML-Enabled Product or Service)**: Relevant as Statewright is deployed as an add-on layer to commercial AI coding products.

## Impact Assessment

This is a defensive tool release rather than a vulnerability disclosure. The direct security impact is positive for teams that adopt it. The broader signal is notable: the open-source community is independently developing structural controls for agentic AI, indicating that built-in safeguards from model providers and IDE vendors are not yet considered sufficient by practitioners.

Risk remains for organisations that deploy AI coding agents without any equivalent control layer — a pattern that is still common.

## Mitigation & Recommendations

- Apply least-privilege tool access to all AI agents; do not grant blanket permissions by default.
- Consider state machine or policy-based guardrail patterns (Statewright or equivalent) before deploying agents in sensitive environments.
- Treat AI agent plugins as third-party code: review, pin versions, and monitor for supply chain changes.
- Test agent behaviour under adversarial prompt conditions before production deployment.

## References

- [Statewright GitHub Repository](https://github.com/statewright/statewright)
- [OWASP LLM08 — Excessive Agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS AML.T0051 — LLM Prompt Injection](https://atlas.mitre.org/techniques/AML.T0051)
