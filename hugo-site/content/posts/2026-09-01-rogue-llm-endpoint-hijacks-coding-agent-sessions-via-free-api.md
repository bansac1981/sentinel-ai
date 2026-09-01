---
title: "Rogue LLM Endpoint Hijacks Coding Agent Sessions via Free API"
date: "2026-09-01T14:13:44+00:00"
draft: false
slug: "rogue-llm-endpoint-hijacks-coding-agent-sessions-via-free-api"

# ── Content metadata ──
summary: "A researcher's internet-exposed LLM honeypot was discovered by scanners, relabeled as a DeepSeek-compatible endpoint, and incorporated into 'free' AI backend infrastructure \u2014 ultimately receiving a full 224 KB coding-agent session including filesystem listings, tool manifests, and private file contents. The incident demonstrates that a malicious rogue model endpoint occupies a privileged position in an agent's control plane, capable of issuing tool-call responses that the agent may execute locally without further verification. This represents a novel supply-chain-style threat where the adversary is not a compromised trusted service but a counterfeit reasoning backend actively solicited by users chasing free API access."
source: "SANS Internet Storm Center"
source_url: "https://isc.sans.edu/diary/rss/33298"
source_title: "The Coding-Agent Trap: When a \"Free\" LLM Endpoint Is the Adversary, (Mon, Aug 31st)"
source_date: 2026-08-31T20:00:34+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1700308234428-c619d7408fbd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxNHx8bGlicmFyeSUyMGJvb2tzJTIwa25vd2xlZGdlJTIwcm93c3xlbnwwfDB8fHwxNzg4MjUyNjE3fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.0
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0080 - AI Agent Context Poisoning", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0057 - LLM Data Leakage", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0040 - AI Model Inference API Access", "AML.T0010 - AI Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "A rogue 'free' LLM endpoint received a full live coding-agent session including tools, filesystem data, and private files."
tldr_who_at_risk: "Developers and researchers running tool-enabled AI coding agents pointed at unverified third-party or 'free' LLM backends are most exposed, as the endpoint controls agent responses and can request arbitrary tool execution."
tldr_actions: ["Never point tool-enabled AI agents at unverified or 'free' third-party LLM endpoints", "Audit your agent's backend configuration and enforce allowlists for trusted inference providers", "Restrict agent tool permissions to least-privilege and require human-in-the-loop confirmation before tool execution"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Supply Chain", "Research"]
tags: ["rogue-model-endpoint", "coding-agent", "llm-honeypot", "tool-enabled-agent", "free-api-abuse", "opencode", "deepseek", "data-exfiltration", "agent-tool-manifest", "evil-twin-endpoint", "china-unicom", "windows-agent", "inference-honeypot", "agentic-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-01T08:50:17+00:00"
feed_source: "sans_isc"
original_url: "https://isc.sans.edu/diary/rss/33298"
pipeline_version: "2.1.0"
---

## Overview

A security researcher operating an internet-exposed LLM inference honeypot observed it being discovered by scanners, relabeled with sought-after model identifiers (including a DeepSeek-style name), and incorporated into infrastructure advertising 'free' LLM API access. On 2026-08-30, the honeypot received a genuine coding-agent session from an ordinary user — 210 identical 224 KB requests in 91 seconds — containing 88 messages of conversation history, tool outputs, filesystem listings, a Windows username, and portions of private files the agent had already read. The relay originated from a China Unicom address in Hebei. The incident illustrates a new class of threat: the **rogue model endpoint**, where a counterfeit reasoning backend positions itself as a trusted control-plane component for tool-enabled agents.

## Technical Analysis

The user was running **opencode**, an open-source terminal coding agent, configured to use a backend labeled `"model": "fofa-ds-NNNNN"` — consistent with a DeepSeek-compatible endpoint discovered via FOFA or a similar scanner. The agent connected with `Authorization: Bearer free`, which the honeypot did not validate.

By the time the session reached the honeypot, the agent had already:
- Listed the user's Downloads directory
- Copied files to `%TEMP%` and unpacked them
- Written and executed a Python extraction script via PowerShell tool calls
- Read chapters of the target novels

All of this context — the tool manifest, working paths, file content, and shell history — arrived in the single request payload when the user typed 'continue'. A malicious operator at that endpoint position could have responded with a crafted tool-call instruction (e.g., a `shell` or `file_write` call), which the agent, depending on its configuration, may have executed automatically without user confirmation. This is not prompt injection through user-supplied content — it is **backend response manipulation** against an agent that implicitly trusts its configured reasoning endpoint.

The attack model is analogous to an evil twin Wi-Fi access point but for AI inference: advertise a desirable, free service; wait for tool-enabled agents to connect; respond with adversarial tool-call payloads.

## Framework Mapping

- **AML.T0080 (AI Agent Context Poisoning)** and **AML.T0110 (AI Agent Tool Poisoning)**: A malicious response could poison agent behaviour or direct tool invocation.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: The agent's own file-read tools could be turned against the user.
- **AML.T0057 (LLM Data Leakage)** and **AML.T0084 (Discover AI Agent Configuration)**: Full session context including tool manifests was passively received.
- **LLM08 (Excessive Agency)**: Agents executing tool calls without verifying endpoint trustworthiness epitomises excessive agency risk.
- **LLM05 (Supply Chain Vulnerabilities)**: The 'free backend' supply chain is the attack surface.

## Impact Assessment

Any developer or researcher using a tool-enabled coding agent pointed at an unverified LLM backend is at risk. The threat is not limited to credential theft — a well-positioned rogue endpoint could direct file reads, writes, or shell execution on the connecting machine. The passive data exposure alone (filesystem layout, usernames, file contents) represents a significant privacy and operational security breach even without active exploitation.

## Mitigation & Recommendations

1. **Enforce backend allowlists**: Only permit AI agents to connect to endpoints with verified TLS certificates and known, trusted operators.
2. **Apply least-privilege tool configuration**: Disable or sandbox file-write and shell tools when not strictly required; require explicit human confirmation before any tool execution.
3. **Treat the inference endpoint as part of your trust boundary**: Audit agent configurations as you would any network credential or API key.
4. **Avoid 'free' unofficial LLM relays**: The cost savings are not worth ceding control-plane access to an unknown operator.
5. **Log and monitor outbound agent requests**: Anomalous repetition (210 requests in 91 seconds) is a detectable signal.

## References

- [SANS ISC Diary: The Coding-Agent Trap](https://isc.sans.edu/diary/rss/33298)
