---
title: "ChatGPT Cross-Account Data Leakage via Sandbox Channel"
date: "2026-09-09T07:48:00+00:00"
draft: false 
slug: "chatgpt-cross-account-data-leakage-via-sandbox-channel"

# ── Content metadata ──
summary: "Check Point Research uncovered a covert cross-account communication channel in ChatGPT's code-execution sandbox that allowed an attacker to hijack a victim's session and exfiltrate data from connected services such as Gmail. The attack exploited a shared internal package delivery service reachable by containers belonging to different user accounts, bypassing inter-container isolation. The channel could be triggered silently via malicious prompts, shared conversations, or custom GPTs without appearing in the victim's visible response."
source: "Check Point Research"
source_url: "https://research.checkpoint.com/2026/the-shared-clipboard-inside-the-sandbox-cross-account-data-leakage-in-chatgpt"
source_title: "The Shared Clipboard Inside the Sandbox: Cross-Account Data Leakage in ChatGPT"
source_date: 2026-09-08T13:00:18+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1695238668015-7bc526956af7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOXx8bGFuZ3VhZ2UlMjB0cmFuc2xhdGlvbiUyMGFic3RyYWN0fGVufDB8MHx8fDE3ODg5MzkwNjF8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0080 - AI Agent Context Poisoning", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0065 - LLM Prompt Crafting", "AML.T0068 - LLM Prompt Obfuscation", "AML.T0094 - Delay Execution of LLM Instructions", "AML.T0110 - AI Agent Tool Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "A covert sandbox channel let attackers silently exfiltrate victims' Gmail data via ChatGPT sessions."
tldr_who_at_risk: "ChatGPT users with connected third-party apps such as Gmail are most exposed, as the attack leverages their session's existing permissions."
tldr_actions: ["Audit and revoke unnecessary third-party app connections in ChatGPT settings", "Treat shared ChatGPT conversations and custom GPTs as untrusted input vectors", "Monitor OpenAI's security advisories for patches addressing sandbox isolation flaws"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research"]
tags: ["chatgpt", "cross-account-leakage", "sandbox-escape", "prompt-injection", "data-exfiltration", "gmail", "code-execution", "openai", "covert-channel", "custom-gpt", "connected-apps", "check-point-research"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-09T07:31:01+00:00"
feed_source: "checkpoint"
original_url: "https://research.checkpoint.com/2026/the-shared-clipboard-inside-the-sandbox-cross-account-data-leakage-in-chatgpt"
pipeline_version: "2.1.0"
---

## Overview

Check Point Research (CPR) disclosed a critical cross-account data leakage vulnerability in ChatGPT, dubbed the 'shared clipboard' attack. Researcher Alexey Bukhteyev demonstrated that a covert communication channel could be established between code-execution containers belonging to entirely separate ChatGPT accounts. An attacker could leverage this channel to execute hidden tasks inside a victim's active session, silently accessing tools, files, and connected services — including Gmail — without the victim observing anything unusual in their conversation.

The finding is significant because it defeats two assumed security properties of ChatGPT's sandbox: inter-user container isolation and the absence of outbound internet access from within the execution environment.

## Technical Analysis

ChatGPT routes tasks requiring code execution to isolated containers. These containers are explicitly blocked from direct internet access and, in theory, cannot communicate with containers from other accounts. CPR identified a critical exception: all containers, regardless of account ownership, could reach the same internal service responsible for delivering software packages.

This shared internal package delivery service became the covert channel. An attacker could craft a payload — embedded in a malicious prompt, a shared ChatGPT conversation, or a custom GPT — that instructs the model to install a specially constructed package. The package delivery mechanism carries attacker-controlled data into the victim's container environment. The victim's session executes the hidden instruction and its output is relayed back across accounts to the attacker.

Critically, the attacker's task was processed in a separate logical flow, with only a normal-looking answer returned to the victim in the visible chat. The conversation display gave no indication that a secondary, attacker-directed task had occurred.

In the proof-of-concept, CPR demonstrated retrieval of email content from a victim's connected Gmail account and its exfiltration to the attacker. The same technique could also harvest conversation history and files present in the affected sandbox environment. The blast radius is bounded only by the permissions and connected services already granted to the victim's session.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** — The attack initiates via a hidden instruction injected into the victim's conversation context.
- **AML.T0057 (LLM Data Leakage)** — Email content and conversation history are exfiltrated across account boundaries.
- **AML.T0080 (AI Agent Context Poisoning)** — The victim's agentic context is silently poisoned with attacker instructions.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** — Connected apps (Gmail) are invoked without user awareness to exfiltrate data.
- **LLM01 (Prompt Injection)** and **LLM06 (Sensitive Information Disclosure)** are the primary OWASP mappings, with **LLM08 (Excessive Agency)** applicable given the model's willingness to act on injected instructions using real user credentials.

## Impact Assessment

Any ChatGPT user who has connected third-party services (email, calendars, productivity apps) was potentially exposed. The attack required no victim interaction beyond engaging with a poisoned conversation or custom GPT. Data accessible through connected integrations — potentially including sensitive business communications — was within scope. The severity is compounded by the silent nature of the exfiltration: victims had no mechanism to detect the covert activity.

## Mitigation & Recommendations

1. **Revoke unnecessary app integrations** — Remove ChatGPT connections to email and other sensitive services until OpenAI confirms the issue is fully remediated.
2. **Treat all shared conversations and custom GPTs as untrusted** — Apply the same scrutiny as you would to clicking an unknown link.
3. **Monitor OpenAI's security disclosures** — Track patching status for the internal package delivery service isolation flaw.
4. **Apply least-privilege principles** — Grant ChatGPT integrations only the minimum permissions required for specific tasks.
5. **Enterprise teams** — Review audit logs for connected app activity and consider disabling third-party integrations in high-sensitivity environments.

## References

- [Check Point Research: The Shared Clipboard Inside the Sandbox](https://research.checkpoint.com/2026/the-shared-clipboard-inside-the-sandbox-cross-account-data-leakage-in-chatgpt)
