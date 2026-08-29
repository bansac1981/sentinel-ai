---
title: "Amazon Kiro IDE Prompt Injection Enables Sensitive Data Exfiltration"
date: 2026-08-29T11:46:38+00:00
draft: true
slug: "amazon-kiro-ide-prompt-injection-enables-sensitive-data-exfiltration"

# ── Content metadata ──
summary: "A prompt injection vulnerability in Amazon Kiro IDE (version 0.7.45) allows attacker-controlled repository content to hijack the Kiro agent and silently exfiltrate sensitive workspace data to an external endpoint via Kiro Powers. Exploitation requires only that the victim opens a malicious workspace file and sends any message to the agent \u2014 no malicious prompt from the user is needed. Amazon patched the flaw in version 0.8.140, released January 15."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/amazon-kiro-prompt-injection-can.html"
source_title: "Amazon Kiro Prompt Injection Can Exfiltrate Sensitive Data Through Kiro Powers"
source_date: 2026-08-27T13:39:56+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1718891603851-237b367bc3f6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxBbWF6b24lMjBicm9rZW4lMjBmZW5jZSUyMGdhcCUyMGFic3RyYWN0JTIwbGlnaHR8ZW58MHwwfHx8MTc4ODAwMzk5OHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0057 - LLM Data Leakage", "AML.T0110 - AI Agent Tool Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Prompt injection in Amazon Kiro IDE lets malicious repo files silently exfiltrate workspace data."
tldr_who_at_risk: "Developers using Amazon Kiro IDE versions below 0.8.140 who open untrusted or attacker-supplied workspace files."
tldr_actions: ["Update Amazon Kiro IDE to version 0.8.140 or later immediately", "Avoid opening workspace files from untrusted or unverified repositories", "Audit MCP server configurations and Kiro Powers steering files in existing projects"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI"]
tags: ["amazon-kiro", "prompt-injection", "data-exfiltration", "agentic-ide", "kiro-powers", "mcp-server", "workspace-poisoning", "trust-boundary-failure", "ai-agent", "ide-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-29T11:46:38+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/amazon-kiro-prompt-injection-can.html"
pipeline_version: "2.1.0"
---

## Overview

Cybersecurity researchers at Mindgard have disclosed a prompt injection vulnerability in Amazon Kiro, an AI-powered agentic integrated development environment (IDE). The flaw affects Kiro IDE version 0.7.45 on Windows and allows attacker-controlled repository content to covertly exfiltrate sensitive local workspace data to an external endpoint. Amazon patched the vulnerability in version 0.8.140, released on January 15. No CVE identifier has been assigned.

## Technical Analysis

The attack vector centres on **Kiro Powers** — a Kiro feature that bundles Model Context Protocol (MCP) server configurations, steering files (`POWER.md`), hooks, and contextual knowledge. The `POWER.md` steering file acts as a persistent onboarding manual that instructs the AI agent which MCP tools are available and when to invoke them.

Exploitation follows a two-step sequence:

1. The victim opens a crafted malicious project via **File → Open Workspace From File** (rather than opening the folder directly).
2. The victim sends any message to the Kiro agent — the message content is irrelevant.

Once the workspace is loaded, attacker-controlled content embedded in the repository is interpreted as agent instructions. The agent then reads sensitive local files, writes that data into IDE configuration, and a subsequent IDE capability (a Kiro Power) converts the modified configuration into outbound network activity — all without the user requesting it.

Critically, the vulnerability reproduces against both trusted and untrusted workspaces, and exploitation difficulty is rated **low**. The trust boundary failure spans the entire pipeline: repository content influences the agent, the agent accesses sensitive information, and a built-in IDE capability completes the exfiltration.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS | AML.T0051 – LLM Prompt Injection | Repo content injected as agent instructions |
| ATLAS | AML.T0080 – AI Agent Context Poisoning | Steering file poisons agent context |
| ATLAS | AML.T0086 – Exfiltration via AI Agent Tool Invocation | MCP tools used for data exfiltration |
| ATLAS | AML.T0081 – Modify AI Agent Configuration | Attacker modifies IDE config through agent |
| OWASP | LLM01 – Prompt Injection | Core attack mechanism |
| OWASP | LLM08 – Excessive Agency | Agent acts autonomously on sensitive operations |
| OWASP | LLM06 – Sensitive Information Disclosure | Workspace data leaked externally |

## Impact Assessment

Any developer using Kiro IDE below version 0.8.140 who opens an attacker-supplied workspace file is exposed. Because the attack requires no malicious user prompt and works on trusted workspaces, the social engineering bar is low — a malicious open-source repository or shared project archive is sufficient. Sensitive data at risk includes local workspace files and IDE configuration data that may contain credentials, API keys, or proprietary source code.

## Mitigation & Recommendations

- **Update immediately**: Upgrade to Kiro IDE version 0.8.140 or later, which contains Amazon's patch.
- **Restrict workspace sources**: Only open workspace files from repositories and collaborators you explicitly trust.
- **Audit Kiro Powers configurations**: Review existing `POWER.md` steering files and MCP server configurations in projects for unexpected instructions or endpoints.
- **Apply least-privilege principles**: Limit the network access and tool permissions granted to Kiro agents in your environment.
- **Monitor outbound connections**: Instrument IDE environments to detect unexpected egress from development machines.

## References

- [The Hacker News – Amazon Kiro Prompt Injection Can Exfiltrate Sensitive Data Through Kiro Powers](https://thehackernews.com/2026/08/amazon-kiro-prompt-injection-can.html)
