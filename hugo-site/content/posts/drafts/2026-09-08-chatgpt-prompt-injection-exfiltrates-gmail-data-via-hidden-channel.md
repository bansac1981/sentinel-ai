---
title: "ChatGPT Prompt Injection Exfiltrates Gmail Data via Hidden Channel"
date: 2026-09-08T18:31:11+00:00
draft: false 
slug: "chatgpt-prompt-injection-exfiltrates-gmail-data-via-hidden-channel"

# ── Content metadata ──
summary: "Check Point Research demonstrated a prompt injection attack against ChatGPT that allowed a hidden instruction to silently read a victim's connected Gmail data and exfiltrate it to an attacker-controlled account through an internal inter-container service. The attack exploited ChatGPT's agentic tool-use defaults, which permit reading connected apps without user confirmation under the 'Important actions' permission model. OpenAI has since taken the internal service used as the covert channel offline, but the underlying permission design and injection vectors remain a structural concern."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/chatgpt-flaw-let-planted-prompt-send.html"
source_title: "ChatGPT Flaw Let a Planted Prompt Send a Victim's Gmail Data to Another Account"
source_date: 2026-09-08T14:19:17+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1578163236808-296558070a4b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOXx8Y29kZSUyMHRlcm1pbmFsJTIwdGV4dCUyMGluamVjdGlvbiUyMGFic3RyYWN0fGVufDB8MHx8fDE3ODg4OTIyNzF8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0080 - AI Agent Context Poisoning", "AML.T0065 - LLM Prompt Crafting", "AML.T0068 - LLM Prompt Obfuscation", "AML.T0067 - LLM Trusted Output Components Manipulation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "A planted ChatGPT prompt silently exfiltrated Gmail data to an attacker account via an internal container channel."
tldr_who_at_risk: "ChatGPT users with Gmail or other apps connected via default 'Important actions' permissions are most exposed, as tool reads require no user confirmation."
tldr_actions: ["Switch ChatGPT connected-app permissions to 'Always ask' to require confirmation before any tool read", "Audit which third-party apps are connected to your ChatGPT account and revoke unnecessary integrations", "Treat shared ChatGPT conversations and custom GPTs as untrusted inputs that may carry hidden instructions", "Enterprise/Edu admins should explicitly allowlist permitted app actions rather than relying on defaults"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research"]
tags: ["chatgpt", "prompt-injection", "data-exfiltration", "gmail", "openai", "agentic-ai", "check-point-research", "covert-channel", "tool-use", "connected-apps", "indirect-prompt-injection", "llm-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-08T18:31:11+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/chatgpt-flaw-let-planted-prompt-send.html"
pipeline_version: "2.1.0"
---

## Overview

Check Point Research published a proof-of-concept on 8 September 2026 demonstrating that a single hidden instruction embedded in a ChatGPT conversation could cause the model to silently read a victim's connected Gmail account and relay that data to an attacker-controlled ChatGPT account. The visible reply showed nothing unusual. OpenAI confirmed the internal service exploited as the covert exfiltration channel has been taken offline; no user-side patch is required for that specific channel, but the broader attack surface — default tool permissions and prompt injection vectors — remains structurally intact.

## Technical Analysis

The attack chains three components:

**1. Injection delivery.** Check Point identified three viable delivery paths for the malicious instruction: a prompt the user pastes themselves, a shared ChatGPT conversation link, or a custom GPT whose builder instructions are hidden from the end user. Any of these pre-seeds the session before the victim sends a single ordinary message.

**2. Dual-stream execution.** The crafted instruction exploited ChatGPT's extended Thinking mode to run two parallel workstreams within one turn. Stream A produced the normal visible answer. Stream B checked a hidden attacker-controlled mailbox for a task, executed that task using the tools already authorised in the victim's session (e.g. Gmail read), and returned the result — all without surfacing in the user-visible output.

**3. Covert exfiltration channel.** Normally, ChatGPT code-execution containers are sandboxed and cannot reach the public internet or other containers directly. However, all containers shared access to one internal OpenAI service — originally intended to serve Python and npm packages — which Check Point weaponised as a side channel to pass data between a victim session and an attacker session running under a different account. The only user-visible artefact was a small "Talked to Gmail" label, recorded after the read had already completed.

The attack also demonstrated the ability to exfiltrate chat history and files within the conversation, with the total data exposure bounded only by what tools and permissions were active in that session.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** — the foundational technique; malicious instructions are injected via shared conversations or custom GPT system prompts.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** — Gmail is read and its contents forwarded through the covert channel using the session's authorised tools.
- **AML.T0080 (AI Agent Context Poisoning)** — the session context is pre-poisoned to alter subsequent agentic behaviour.
- **AML.T0068 (LLM Prompt Obfuscation)** — the hidden instruction is structured to keep malicious activity separate from visible output.
- **LLM01 (Prompt Injection)**, **LLM06 (Sensitive Information Disclosure)**, and **LLM08 (Excessive Agency)** all apply directly, with LLM08 particularly relevant given that default permissions allow silent tool reads.

## Impact Assessment

Any ChatGPT user who has connected Gmail or other apps under the default "Important actions" permission model is potentially affected. Business plan users face elevated risk as apps are enabled by default. Enterprise and Edu environments, where apps are off by default and admins control permissions, have a lower baseline exposure. The specific inter-container channel has been patched server-side, but the injection vectors and permissive default tool-read behaviour persist.

## Mitigation & Recommendations

- **Switch to "Always ask"** in ChatGPT connected-app settings so every tool invocation requires explicit user confirmation.
- **Revoke unnecessary app connections** — limit the blast radius of any future injection by reducing available tools.
- **Treat all external ChatGPT inputs as untrusted**: shared conversation links and custom GPTs can carry hidden instructions.
- **Enterprise admins** should explicitly define permitted app actions per workspace rather than accepting plan defaults.
- **Monitor "Talked to [App]" labels** as a lightweight signal of unexpected tool use during a session.

## References

- [The Hacker News – ChatGPT Flaw Let a Planted Prompt Send a Victim's Gmail Data to Another Account](https://thehackernews.com/2026/09/chatgpt-flaw-let-planted-prompt-send.html)
