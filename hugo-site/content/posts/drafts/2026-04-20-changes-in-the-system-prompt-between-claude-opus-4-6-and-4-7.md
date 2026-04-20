---
title: "Changes in the system prompt between Claude Opus 4.6 and 4.7"
date: 2026-04-20T18:10:20+00:00
draft: false
slug: "changes-in-the-system-prompt-between-claude-opus-4-6-and-4-7"

# ── Content metadata ──
summary: "Anthropic's published system prompt diff between Claude Opus 4.6 and 4.7 reveals significant expansions in agentic tool access, autonomous browsing capabilities, and child safety guardrails \u2014 changes with direct security implications for prompt injection and excessive agency risks. The new `tool_search` mechanism and acting-before-asking posture increase the attack surface for adversarial inputs targeting agentic Claude deployments. Transparency in publishing these changes is notable, but the expanded autonomous capabilities warrant scrutiny from defenders."
source: "HN AI Security"
source_url: "https://simonwillison.net/2026/Apr/18/opus-system-prompt/"
source_date: 2026-04-19T10:36:29+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/18799047/pexels-photo-18799047.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Claude Opus 4.7 system prompt adds autonomous browsing, spreadsheet/slide agents, and proactive tool-calling before asking users."
tldr_who_at_risk: "Enterprise users and developers deploying Claude in agentic workflows are most exposed due to expanded autonomous tool-calling and reduced clarification checkpoints."
tldr_actions: ["Audit Claude agentic deployments for unintended tool_search escalation paths that could be triggered via injected inputs", "Review expanded browsing and Office-suite agent integrations for data exfiltration and prompt injection vectors", "Monitor system prompt changes on future Claude releases via Anthropic's published archive to track evolving capability boundaries"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Industry News", "Research"]
tags: ["anthropic", "claude", "system-prompt", "agentic-ai", "tool-use", "prompt-transparency", "child-safety", "browsing-agent", "tool-search", "excessive-agency"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-20T18:10:20+00:00"
feed_source: "hn_ai_security"
original_url: "https://simonwillison.net/2026/Apr/18/opus-system-prompt/"
pipeline_version: "1.0.0"
---

## Overview

Anthropic published an updated system prompt for Claude Opus 4.7 (released April 16, 2026), and security researcher Simon Willison performed a structured diff against the prior Opus 4.6 prompt. The changes reveal a notable expansion of agentic capabilities — including new autonomous agents for Chrome browsing, Excel, and PowerPoint — alongside a revised posture that encourages Claude to act using tools before seeking human clarification. While Anthropic's transparency in publishing system prompts is commendable and unusual among major AI labs, the contents of the 4.7 prompt introduce meaningful changes to Claude's attack surface.

## Technical Analysis

Several changes carry direct security implications:

**Expanded agentic tool surface:** The 4.7 prompt now explicitly references Claude in Chrome (autonomous browsing), Claude in Excel, and Claude in PowerPoint as callable tools within Claude Cowork. Each integration represents a new vector for adversarial manipulation — malicious web content encountered during autonomous browsing could inject instructions into Claude's context (classic indirect prompt injection).

**Proactive tool-calling posture:** The new `<acting_vs_clarifying>` section instructs Claude to call tools — including `tool_search` — to resolve ambiguity *before* asking the user. This reduces human-in-the-loop checkpoints. An attacker crafting an ambiguous prompt could cause Claude to autonomously invoke tools, fetch external data, or escalate privileges without explicit user confirmation.

**`tool_search` mechanism:** Claude is now instructed to call `tool_search` before declaring it lacks a capability (e.g., location access, calendar, files, memory). This means the model will actively probe for available capabilities in response to user input — including adversarially crafted input — potentially exposing tool availability as an oracle.

**Child safety hardening:** The `<critical_child_safety_instructions>` section introduces conversation-level state: once a refusal is triggered for child safety reasons, all subsequent turns must be treated with extreme caution. This is a meaningful guardrail against multi-turn jailbreak progressions targeting this content class.

**Reduced verbosity and removed asterisk-emote behaviour:** These are lower-security-relevance behavioural changes, though removal of documented misbehaviours suggests model-level alignment improvements.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection):** Autonomous browsing via Claude in Chrome directly enables indirect prompt injection from attacker-controlled web pages.
- **AML.T0054 (LLM Jailbreak):** The multi-turn child safety state management directly addresses iterative jailbreak attempts.
- **AML.T0056 (LLM Meta Prompt Extraction):** Public system prompt diffing, while researcher-led here, demonstrates that system prompt contents are recoverable and analysable by adversaries.
- **LLM08 (Excessive Agency):** The act-first, ask-later posture combined with expanded tool integrations increases autonomous action scope without proportional human oversight.
- **LLM07 (Insecure Plugin Design):** New Office and browser agents represent plugin-style integrations with potentially underspecified security boundaries.

## Impact Assessment

Enterprise deployments using Claude Cowork or agentic Claude APIs face the highest exposure. The expanded tool surface increases the blast radius of a successful prompt injection. Consumer Claude.ai users face moderate risk, primarily from the browsing agent's susceptibility to web-based injection. The child safety improvements reduce one specific jailbreak pathway.

## Mitigation & Recommendations

- Treat any Claude deployment with browser or file-system tool access as a high-privilege agent; apply strict input sanitisation on external data returned to Claude's context.
- Implement tool-call logging and alerting for unexpected `tool_search` invocations, particularly those triggered by external or user-supplied content.
- Review Anthropic's system prompt archive regularly to track capability expansions that may affect your threat model.
- For sensitive deployments, consider restricting available tools to the minimum required set to limit autonomous escalation paths.

## References

- [Simon Willison — Changes in the system prompt between Claude Opus 4.6 and 4.7](https://simonwillison.net/2026/Apr/18/opus-system-prompt/)
- [Anthropic System Prompt Archive](https://www.anthropic.com/system-prompt-archive)
