---
title: "CrabTrap: An LLM-as-a-judge HTTP proxy to secure agents in production"
date: "2026-04-22T10:00:29+00:00"
draft: false
slug: "crabtrap-an-llm-as-a-judge-http-proxy-to-secure-agents-in-production"

# ── Content metadata ──
summary: "Brex has open-sourced CrabTrap, an HTTP proxy that uses an LLM-as-a-judge architecture to intercept, evaluate, and block or allow requests made by AI agents in real time against configurable policies. The tool targets a critical gap in agentic AI deployments \u2014 the lack of runtime guardrails for autonomous agent actions \u2014 and represents a practical defensive control against excessive agency and prompt injection exploitation. Its production-oriented design positions it as a notable contribution to the emerging agentic AI security toolchain."
source: "HN AI Security"
source_url: "https://www.brex.com/crabtrap"
source_date: 2026-04-21T15:29:16+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://plus.unsplash.com/premium_vector-1725420017452-eb130b8ea017?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Brex open-sources CrabTrap, an LLM-judge HTTP proxy that blocks unsafe AI agent actions in real time."
tldr_who_at_risk: "Organisations deploying autonomous AI agents in production are exposed to uncontrolled agent actions without runtime enforcement layers like this."
tldr_actions: ["Evaluate CrabTrap or equivalent proxy-based guardrails for any production agentic AI deployment", "Define explicit allow/deny policies covering sensitive HTTP endpoints agents can reach", "Audit existing agent architectures for excessive agency and lack of runtime action validation"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Prompt Injection", "Research", "Industry News"]
tags: ["agentic-ai", "llm-proxy", "runtime-security", "llm-as-a-judge", "open-source", "agent-guardrails", "http-proxy", "policy-enforcement", "brex", "crabtrap"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-22T08:15:59+00:00"
feed_source: "hn_ai_security"
original_url: "https://www.brex.com/crabtrap"
pipeline_version: "1.0.0"
---

## Overview

Brex, the fintech company now operating as a subsidiary of Capital One, has open-sourced **CrabTrap** — an HTTP proxy designed to secure AI agents running in production environments. CrabTrap sits between an AI agent and its downstream HTTP targets, intercepting every outbound request and evaluating it against a user-defined policy using an LLM-as-a-judge model. Requests are either approved or blocked in real time, with decisions logged as either static rule matches or LLM judgements. The project addresses a widely acknowledged but under-solved problem: autonomous agents can take consequential real-world actions, yet most deployments lack runtime enforcement mechanisms to constrain them.

## Technical Analysis

CrabTrap operates as a transparent HTTP proxy. When an agent issues an outbound request, CrabTrap intercepts it and passes the request context to a policy evaluation layer. This layer first checks static rules (pattern matching, allowlists, blocklists) for low-latency decisions. If no static rule matches, the request is forwarded to an LLM judge configured with the operator's policy description, which then returns a block or allow verdict. This hybrid architecture balances the determinism of rule-based systems with the semantic flexibility needed to catch novel or ambiguous agent behaviours that rigid rules would miss.

The LLM-as-a-judge pattern is itself a meaningful design choice. It means CrabTrap can detect prompt injection-driven agent actions — for example, an agent coerced by malicious content in a document it processed into exfiltrating data to an attacker-controlled endpoint — that would bypass purely syntactic rule sets.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection):** CrabTrap's core value proposition is intercepting agent actions that may result from injected instructions in the agent's context window.
- **LLM08 (Excessive Agency):** The tool directly mitigates excessive agency by enforcing boundaries on what actions an agent can take autonomously.
- **LLM01 (Prompt Injection):** Runtime HTTP interception provides a compensating control when prompt injection reaches the action-execution stage.
- **LLM02 (Insecure Output Handling):** Blocking outbound requests prevents insecure agent outputs from causing downstream harm.

## Impact Assessment

The tool is most relevant to engineering teams operating LLM-based agents with broad tool access — web browsing, API calls, file operations, or inter-service communication. Without a runtime enforcement layer, a single successful prompt injection or jailbreak against an agent can translate directly into data exfiltration, unauthorised transactions, or lateral movement within connected systems. CrabTrap's proxy model is infrastructure-agnostic and requires no changes to the agent itself, lowering the barrier to adoption significantly.

The LLM judge dependency also introduces a secondary risk surface: the judge itself could theoretically be manipulated or suffer from inconsistent verdicts, making policy design and judge prompt hardening critical operational concerns.

## Mitigation & Recommendations

- **Deploy runtime proxies** such as CrabTrap for any agent with external HTTP access, particularly those touching financial, identity, or data systems.
- **Define narrow, explicit policies** rather than broad permissive defaults; prefer allowlist-over-blocklist architectures.
- **Harden the LLM judge prompt** to resist adversarial inputs that could manipulate its verdicts.
- **Monitor and review LLM-decided blocks** regularly to detect policy gaps or judge inconsistencies.
- **Combine with input-layer defences** — CrabTrap operates at the output/action layer and should complement, not replace, prompt injection mitigations earlier in the pipeline.

## References

- [CrabTrap on Brex](https://www.brex.com/crabtrap)
- [CrabTrap GitHub Repository](https://github.com/brexhq/crabtrap) *(referenced in source)*
