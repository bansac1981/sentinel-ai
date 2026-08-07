---
title: "Adversa AI: 89% of AI Agents Fail Security Tests"
date: "2026-06-04T05:38:21+00:00"
draft: false 
slug: "only-11-of-100-ai-agents-pass-security-and-capability-benchmarks"

# ── Content metadata ──
summary: "Adversa AI's AI Risk Quadrant report evaluated 100 AI agents across ten categories, finding that only 11 qualify as both capable and well-defended. The research identifies a structural 'power-protection inversion' where the most capable agents also present the widest attack surface, driven by a 'lethal trifecta' of private data access, exposure to untrusted content, and outbound action capability. Computer and coding agents showed the most severe exposure, raising urgent concerns about autonomous agent deployment in enterprise environments."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/security-of-100-ai-agents-tested-and-ranked-what-you-need-to-know/"
source_title: "Security of 100 AI Agents Tested and Ranked \u2013 What You Need to Know"
source_date: 2026-06-03T13:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/8721342/pexels-photo-8721342.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access", "AML.T0054 - LLM Jailbreak"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Only 11 of 100 AI agents tested are both capable and secure, per Adversa AI's benchmark."
tldr_who_at_risk: "Enterprises deploying autonomous AI agents \u2014 especially computer and coding agents \u2014 face systemic risk due to structural design trade-offs between capability and security."
tldr_actions:
  - "Audit all deployed AI agents against the lethal trifecta: restrict private data access, untrusted content exposure, and outbound action scope"
  - "Prioritise agents ranked in the 'capable well-defended' quadrant and validate vendor security claims independently"
  - "Implement least-privilege boundaries and sandboxing for computer and coding agents before granting autonomous operation"

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Prompt Injection", "Research", "Industry News"]
tags: ["ai-agents", "adversa-ai", "ai-risk-quadrant", "agent-security", "power-protection-inversion", "lethal-trifecta", "computer-agents", "coding-agents", "autonomous-agents", "attack-surface", "llm-security", "agentic-ai"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-03T23:03:32+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/security-of-100-ai-agents-tested-and-ranked-what-you-need-to-know/"
pipeline_version: "1.0.0"
---

## Overview

Adversa AI has published its AI Risk Quadrant for Agent Security report, benchmarking 100 AI agents across ten functional categories against a combined measure of capability and defensive posture. The headline finding is stark: only 11 of the 100 agents evaluated qualify as both 'capable' and 'well-defended'. The remaining 89 agents fall into categories defined by either dangerous capability without adequate defence, or defensive posture at the cost of usability — making them security liabilities or operational non-starters.

The report arrives at a moment when enterprise adoption of autonomous agents is accelerating, driven in part by AI-assisted cyberattacks that are forcing defenders to automate at scale. The irony is that the same urgency pushing organisations toward agents is compounding their exposure.

## Technical Analysis

Adversa frames the core structural problem as the **'lethal trifecta'**: the convergence of private data access, exposure to untrusted external content, and the ability to execute outbound actions. According to the report, 98% of tested agents exhibit all three characteristics — because these properties are functionally required for agents to be useful.

This creates what Adversa terms a **'power-protection inversion'**: the vendors shipping the most capable agents are simultaneously shipping the widest attack surfaces. This is not attributed to negligence by a subset of vendors but described as a structural feature of the current agent market, appearing consistently across all ten agent categories.

The worst-performing categories are **computer agents** — designed to make decisions or execute actions on behalf of users — and **coding agents**. Computer agents are particularly exposed because they require broad contextual input, increasing susceptibility to prompt injection and adversarial content embedded in their operating environment. Coding agents present elevated risk due to their access to execution environments, codebases, and external repositories.

Attack vectors of primary concern include prompt injection via untrusted content in the agent's context window, insecure handling of tool outputs, and excessive agency granted without adequate guardrails — all directly exploitable without requiring model-level compromise.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **AML.T0054 (LLM Jailbreak)**: Direct exploitation vectors for agents consuming untrusted content.
- **AML.T0057 (LLM Data Leakage)** and **AML.T0040 (ML Model Inference API Access)**: Relevant where agents have access to sensitive enterprise data.
- **LLM08 (Excessive Agency)**: The conceptual centrepiece of the report's findings — agents are granted too much autonomous capability without compensating controls.
- **LLM01 (Prompt Injection)** and **LLM02 (Insecure Output Handling)**: Primary technical attack surface for agents consuming external or user-supplied content.

## Impact Assessment

The systemic nature of the finding is what elevates this beyond a standard research disclosure. With 98% of agents carrying the lethal trifecta and only 11% meeting a combined security-capability bar, organisations deploying agents at scale are statistically likely to be running vulnerable systems. The risk is highest for security operations, software development, and business process automation use cases where agents operate with elevated privileges and access to sensitive data.

## Mitigation & Recommendations

- **Apply least-privilege principles aggressively**: Scope each agent's data access, tool permissions, and outbound connectivity to the minimum required for its task.
- **Sandbox computer and coding agents**: Isolate execution environments and enforce strict output validation before any action is committed.
- **Treat untrusted content as an attack vector**: Implement content filtering and contextual integrity checks on all data entering an agent's context window.
- **Reference the AI Risk Quadrant**: Use Adversa's rankings as a procurement and deployment filter, prioritising vendors in the 'capable well-defended' segment.
- **Establish agent-specific monitoring**: Standard endpoint or application telemetry is insufficient — log agent reasoning chains, tool calls, and outbound actions for anomaly detection.

## References

- [Security of 100 AI Agents Tested and Ranked – SecurityWeek](https://www.securityweek.com/security-of-100-ai-agents-tested-and-ranked-what-you-need-to-know/)
- Adversa AI: AI Risk Quadrant for Agent Security Report (June 2026)
