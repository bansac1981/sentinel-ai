---
title: "Claude Credential Exfiltration via Sandbox Escape"
date: "2026-05-31T01:34:23+00:00"
draft: false 
slug: "anthropic-documents-sandbox-escape-risks-and-credential-exfiltration-vectors-in"

# ── Content metadata ──
summary: "Anthropic has published detailed documentation of its sandboxing architecture across Claude.ai, Claude Code, and Claude Cowork, including disclosure of a previously identified credential exfiltration vector via the api.anthropic.com/v1/files endpoint. The writeup covers process-level isolation technologies including gVisor, Seatbelt, Bubblewrap, and full VM approaches, and candidly acknowledges security gaps that were missed. This transparency is notable for the agentic AI space, where sandbox documentation is typically sparse and trust is difficult to calibrate."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything"
source_title: "How we contain Claude across products"
source_date: 2026-05-30T21:36:24+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1677442135131-4d7c123aef1c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc4MDAxMjM0OXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Anthropic publicly documents Claude sandbox architecture, disclosing a real credential exfiltration vector via its files API."
tldr_who_at_risk: "Developers and enterprises deploying Claude-based agents are most exposed, particularly where credentials or sensitive data enter the agent's execution environment."
tldr_actions: ["Ensure credentials are never injected into agent sandbox environments — rely on external secret management", "Review egress controls for any LLM agent deployment, blocking outbound calls to unexpected endpoints", "Audit use of Anthropic's files API endpoint for unintended data exfiltration paths"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Research", "Industry News"]
tags: ["sandboxing", "claude", "anthropic", "credential-exfiltration", "gvisor", "bubblewrap", "seatbelt", "agent-security", "egress-control", "claude-code", "vm-isolation", "agentic-ai"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-31T01:07:26+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything"
pipeline_version: "1.0.0"
---

## Overview

Anthropic has published an unusually detailed technical overview of how it sandboxes Claude across its product suite — Claude.ai, Claude Code, and Claude Cowork. The documentation, surfaced by Simon Willison, outlines the isolation technologies deployed at each layer and candidly references at least one real exfiltration vector that was previously missed: the `api.anthropic.com/v1/files` endpoint. This kind of transparency is rare in the agentic AI space and provides a useful baseline for evaluating agent containment strategies.

## Technical Analysis

The sandboxing stack varies by product context:

- **Claude.ai** uses [gVisor](https://gvisor.dev/), a userspace kernel that intercepts system calls to limit the blast radius of a compromised container.
- **Claude Code (local)** uses **Seatbelt** on macOS (a sandbox profile enforcement tool) and **Bubblewrap** on Linux, providing filesystem and capability restrictions for locally executed agent processes.
- **Claude Cowork** runs a full virtual machine — Apple's Virtualization framework on macOS and HCS (Host Compute Service) on Windows — providing the strongest isolation tier.

The core security principle articulated is credential exclusion: if credentials never enter the sandbox, they cannot be exfiltrated regardless of whether the cause is a malicious prompt, a jailbreak, or a compromised model behaviour. This is a sound zero-trust approach to agentic containment.

However, the acknowledgement of the `api.anthropic.com/v1/files` exfiltration vector is significant. This suggests that even well-resourced teams can overlook covert exfiltration channels — particularly API-accessible file staging endpoints that an agent might leverage to move data outside the sandbox boundary without triggering conventional egress alerts.

## Framework Mapping

- **AML.T0057 (LLM Data Leakage)**: The files API vector represents a real data leakage path — data could be staged and retrieved externally without obvious network indicators.
- **AML.T0051 (LLM Prompt Injection)**: Prompt injection remains a plausible trigger for agent behaviour that attempts to abuse sandbox escape or exfiltration paths.
- **LLM06 (Sensitive Information Disclosure)**: Credential or data exfiltration via overlooked API endpoints maps directly to this category.
- **LLM08 (Excessive Agency)**: Agents with broad tool access and insufficient egress controls are the core risk model being addressed here.

## Impact Assessment

The immediate impact is informational — this is defensive documentation, not a disclosed active breach. However, the files API vector indicates that real exfiltration paths existed (or could exist) in production agentic deployments. Any organisation using Claude-based agents in sensitive data environments should treat this as a prompt to audit their own egress controls and credential handling practices. The risk is not limited to Anthropic's stack; the same classes of vulnerability apply broadly to any LLM agent framework.

## Mitigation & Recommendations

1. **Exclude credentials from agent sandboxes entirely.** Use external secret managers and inject only scoped, short-lived tokens at the infrastructure layer, never within the agent's reachable environment.
2. **Audit all egress paths**, including first-party API endpoints that agents might use as staging areas for data exfiltration.
3. **Evaluate sandbox technology choices** against your threat model — gVisor and Bubblewrap offer strong syscall-level isolation, but egress controls at the network layer are equally critical.
4. **Monitor for anomalous file API usage** if using Anthropic's platform APIs, particularly large or unexpected uploads via `/v1/files`.
5. **Review Anthropic's open source srt (Sandbox Runtime) tool** as a reference implementation for agentic containment.

## References

- [Simon Willison — How we contain Claude across products](https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything)
