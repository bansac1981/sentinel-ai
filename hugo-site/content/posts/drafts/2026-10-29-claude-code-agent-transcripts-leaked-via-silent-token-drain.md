---
title: "Claude Code Agent Transcripts Leaked via Silent Token Drain"
date: 2026-10-29T11:39:07+00:00
draft: true
slug: "claude-code-agent-transcripts-leaked-via-silent-token-drain"

# ── Content metadata ──
summary: "Claude Code's agent_summary feature silently transmits full agent transcripts to Anthropic's API every 30 seconds per background agent, consuming 15\u201320% of token budget purely for a UI status line. While primarily a resource efficiency issue, the undocumented, always-on behaviour raises concerns about unintended data exposure of agent conversation history. A community-developed Bun preload workaround suppresses the behaviour without modifying the binary."
source: "Anthropic (via HN)"
source_url: "https://gist.github.com/flamerix-ai/c3905705cc4205e5de3011fa2e74efce"
source_title: "Claude Code regularly sends each background agent\u2019s transcript to its model"
source_date: 2026-10-29T03:33:42+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1646956140268-a990c8e153ed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNXx8bGFib3JhdG9yeSUyMHNjaWVuY2UlMjBkaXNjb3Zlcnl8ZW58MHwwfHx8MTc5MzI3Mzk0N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0084 - Discover AI Agent Configuration", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM04 - Model Denial of Service"]

# ── TL;DR ──
tldr_what: "Claude Code silently sends full agent transcripts to Anthropic's API every 30 seconds for a UI-only status label."
tldr_who_at_risk: "Claude Code users running multi-agent workflows are most exposed, losing token budget and exposing conversation history without consent or configuration option."
tldr_actions: ["Audit Claude Code OpenTelemetry exports for agent_summary query_source events to confirm exposure", "Apply the community Bun preload (no-agent-summary.js) to suppress agent_summary API calls", "Monitor for Claude Code updates that may silently re-enable agent_summary after the fix"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Industry News"]
tags: ["claude-code", "anthropic", "agent-transcripts", "token-drain", "data-leakage", "agentic-ai", "opentelemetry", "bun-preload", "api-cost", "background-agents"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-10-29T11:39:07+00:00"
feed_source: "hn_anthropic"
original_url: "https://gist.github.com/flamerix-ai/c3905705cc4205e5de3011fa2e74efce"
pipeline_version: "2.1.0"
---

## Overview

A community analysis of Claude Code's OpenTelemetry telemetry has revealed that the tool silently transmits the full transcript of every background agent to Anthropic's model API approximately every 30 seconds. The sole purpose of these calls is to generate a 3–5 word status line displayed in the agents panel UI. The behaviour, enabled by default since version 2.1.232 (August 2026), has no user-facing toggle and was not publicly documented. Independent measurements confirmed the feature consumed 16–20% of total Claude Code API spend, with 96% of that routed to Opus — the most expensive model tier.

## Technical Analysis

The `agent_summary` feature operates via a `setTimeout`/`setInterval` loop inside Claude Code's bundled Bun runtime. Every ~30 seconds per active background agent, it constructs a request containing that agent's entire conversation transcript and submits it to the configured model (defaulting to Opus) with the instruction to summarise the most recent action in 3–5 words. The response is used exclusively to update a UI label and is never injected back into any agent or user-facing conversation.

Key telemetry indicators:
- `query_source = agent_summary` in Claude Code's OpenTelemetry `claude_code.api_request` events
- Input-to-output token ratio of approximately 9,000:1 (full transcript in, 3 words out)
- Calls account for ~1 in 5 total API requests during active multi-agent sessions

The community fix (`no-agent-summary.js`) is a Bun preload that monkey-patches `setTimeout` and `setInterval`. When a callback's source text matches the `[AgentSummary] Timer fired` anchor string, the preload returns an inert handle rather than registering the timer. All other timers pass through unmodified.

```bash
curl -fsSL https://gist.githubusercontent.com/flamerix-ai/c3905705cc4205e5de3011fa2e74efce/raw/no-agent-summary.js \
  -o ~/.local/share/no-agent-summary.js
BUN_OPTIONS="${BUN_OPTIONS:+$BUN_OPTIONS} --preload $HOME/.local/share/no-agent-summary.js" claude
```

## Framework Mapping

- **AML.T0057 (LLM Data Leakage):** Full agent transcripts — potentially containing credentials, source code, or sensitive task context — are transmitted to the API without explicit user awareness.
- **AML.T0084 (Discover AI Agent Configuration):** The behaviour exposes agent state and conversation history to the model provider infrastructure on a polling basis.
- **LLM06 (Sensitive Information Disclosure):** Transcript contents submitted for summarisation may include sensitive data processed by the agent during its task.
- **LLM04 (Model Denial of Service):** The feature effectively consumes a disproportionate share of rate-limit headroom, degrading the primary conversation's available token budget.

## Impact Assessment

Users operating Claude Code in subscription mode lose rate-limit headroom rather than incurring direct invoice charges, but the effect is equivalent to a ~20% reduction in usable capacity. For enterprise teams running multi-agent pipelines, agent transcripts may contain proprietary code, internal system details, or credentials that are now being routinely transmitted in summarisation requests. The absence of any opt-out mechanism compounds the concern.

## Mitigation & Recommendations

1. **Audit telemetry:** Inspect Claude Code's OpenTelemetry export and filter `claude_code.api_request` events by `query_source` to quantify agent_summary exposure in your environment.
2. **Apply the preload fix:** Use the community `no-agent-summary.js` Bun preload to suppress the timer without modifying the Claude Code binary.
3. **Monitor for regressions:** The fix author notes that Claude Code updates can silently re-enable the behaviour; implement a post-update verification step.
4. **Restrict agent context:** Until Anthropic provides an official toggle, limit sensitive data passed to background agents to reduce transcript leakage risk.

## References

- [Original Gist — Flamerix AI](https://gist.github.com/flamerix-ai/c3905705cc4205e5de3011fa2e74efce)
