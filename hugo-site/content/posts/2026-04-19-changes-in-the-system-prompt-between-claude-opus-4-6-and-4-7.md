---
title: "Changes in the system prompt between Claude Opus 4.6 and 4.7"
date: "2026-04-19T19:39:07+00:00"
draft: false
slug: "changes-in-the-system-prompt-between-claude-opus-4-6-and-4-7"

# ── Content metadata ──
summary: "Anthropic's published system prompt diff between Claude Opus 4.6 and 4.7 reveals significant changes to agentic tool access, child safety guardrails, and autonomous browsing capabilities that carry meaningful security implications. The introduction of proactive tool discovery via `tool_search` and expanded autonomous agents (Chrome, Excel, PowerPoint) increases the attack surface for prompt injection and excessive agency scenarios. The transparency of publishing these prompts, while praiseworthy, also provides adversaries with a detailed map of guardrail logic and bypass opportunities."
source: "HN AI Security"
source_url: "https://simonwillison.net/2026/Apr/18/opus-system-prompt/"
source_date: 2026-04-19T10:36:29+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/2599244/pexels-photo-2599244.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Industry News", "Research"]
tags: ["anthropic", "claude", "system-prompt", "agentic-ai", "tool-use", "prompt-transparency", "child-safety", "guardrails", "autonomous-browsing", "tool-search", "excessive-agency"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-19T19:33:45+00:00"
feed_source: "hn_ai_security"
original_url: "https://simonwillison.net/2026/Apr/18/opus-system-prompt/"
pipeline_version: "1.0.0"
---

## Overview

Simon Willison has published a detailed analysis of the system prompt changes between Claude Opus 4.6 and 4.7, made possible by Anthropic's unique practice of publicly archiving their user-facing system prompts. The diff highlights several security-relevant changes: the introduction of proactive tool discovery (`tool_search`), expanded autonomous agent integrations (Chrome browsing, Excel, PowerPoint), reinforced child safety guardrails, and updated agentic decision logic that favours acting over clarifying. While the transparency is commendable, it also surfaces a dual-use concern: the same public archive that aids researchers and defenders provides adversaries with a detailed blueprint of where guardrails exist and how they are structured.

## Technical Analysis

The most security-relevant change is the introduction of `tool_search`, a mechanism by which Claude proactively queries for available tools before declaring it lacks a capability. The prompt instructs: *"Before concluding Claude lacks a capability... Claude calls tool_search to check whether a relevant tool is available but deferred."* This behaviour expands the model's autonomous surface area — if a malicious tool or plugin is present in the deferred tool registry, a prompt injection payload delivered through web content (via the new Claude in Chrome agent) could trigger unintended tool invocations.

The new `<acting_vs_clarifying>` directive further reduces friction on agentic tasks: Claude is now instructed to act with tools rather than ask the user for clarification, and to complete tasks rather than stop partway. Combined with autonomous browser, spreadsheet, and presentation agents, this increases the risk of cascading actions triggered by adversarial inputs in documents or web pages.

The `<critical_child_safety_instructions>` expansion, including the persistence rule (*"Once Claude refuses a request for reasons of child safety, all subsequent requests in the same conversation must be approached with extreme caution"*), represents a meaningful guardrail hardening. However, publishing the exact tag name and logic gives adversaries specific text to target when probing jailbreak robustness.

## Framework Mapping

- **AML.T0051 / LLM01 (Prompt Injection):** The Claude in Chrome agent processing arbitrary web content is a direct prompt injection vector. Malicious sites could embed instructions to invoke tools or exfiltrate session context.
- **AML.T0056 / LLM06 (Meta Prompt Extraction / Sensitive Information Disclosure):** The public archive itself constitutes authorised disclosure, but it lowers the barrier for adversaries to craft targeted jailbreaks informed by exact guardrail language.
- **LLM08 (Excessive Agency):** The act-first, clarify-later directive combined with multi-agent tool access is a textbook excessive agency risk, especially in document and browser contexts.
- **LLM07 (Insecure Plugin Design):** The deferred tool registry pattern, if not strictly sandboxed, could allow malicious tool registration to be surfaced by `tool_search`.

## Impact Assessment

End users interacting with Claude in agentic contexts (Chrome, Excel, PowerPoint) face elevated risk from prompt injection via document or web content. Enterprise deployments using Claude Platform integrations should audit tool registry access controls. The general public benefits from the hardened child safety guardrails, but security researchers note that publishing exact XML tag names aids adversarial probing.

## Mitigation & Recommendations

- **Operators** should restrict tool registries to explicitly allowlisted tools and audit `tool_search` invocation logs.
- **Enterprises** deploying Claude in Chrome or document agents should sandbox web and file content processing to prevent prompt injection escalation.
- **Anthropic** should consider whether publishing exact guardrail tag names (e.g., `<critical_child_safety_instructions>`) creates unnecessary jailbreak targeting risk.
- **Security teams** should red-team the `tool_search` discovery mechanism for malicious tool injection scenarios.

## References

- [Original Article — Simon Willison's Weblog](https://simonwillison.net/2026/Apr/18/opus-system-prompt/)
- [Anthropic System Prompt Archive](https://www.anthropic.com/)
