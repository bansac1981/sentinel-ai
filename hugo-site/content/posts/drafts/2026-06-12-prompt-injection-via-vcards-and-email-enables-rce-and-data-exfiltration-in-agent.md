---
title: "Prompt Injection via vCards and Email Enables RCE and Data Exfiltration in OpenClaw Agent"
date: 2026-06-12T08:56:46+00:00
draft: true
slug: "prompt-injection-via-vcards-and-email-enables-rce-and-data-exfiltration-in-agent"

# ── Content metadata ──
summary: "Two independent research teams demonstrated that OpenClaw, a self-hosted AI agent, is vulnerable to prompt injection attacks delivered through shared contacts, vCards, location pins, and plain emails \u2014 enabling attacker-controlled code execution and sensitive data exfiltration. Imperva's finding, now patched in version 2026.4.23, exploited the agent's failure to mark message objects as untrusted before passing them to the underlying LLM. Varonis separately showed that a single crafted email could instruct an agent to forward mock AWS credentials and customer data to an external address, a behaviour-level risk no patch can fully remediate."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/06/new-attacks-trick-openclaw-ai-agent.html"
source_title: "New Attacks Trick OpenClaw AI Agent Into Running Code and Leaking Secrets"
source_date: 2026-06-11T17:46:32+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1531747118685-ca8fa6e08806?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxM3x8YXJ0aWZpY2lhbCUyMGludGVsbGlnZW5jZSUyMHJvYm90JTIwc2VjdXJpdHl8ZW58MHwwfHx8MTc4MTI0NjgxMXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0043 - Craft Adversarial Data", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Hidden instructions in vCards and emails tricked OpenClaw AI agent into executing code and leaking secrets."
tldr_who_at_risk: "Organisations running self-hosted OpenClaw agents with access to mailboxes, contacts, or cloud credentials are directly exposed."
tldr_actions: ["Update OpenClaw to version 2026.4.23 or later immediately", "Apply least-privilege principles to agent tool and data access scopes", "Implement untrusted-content boundaries for all external data ingested by LLM agents"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research"]
tags: ["prompt-injection", "ai-agent", "openclaw", "code-execution", "data-exfiltration", "vcard-injection", "indirect-prompt-injection", "excessive-agency", "imperva", "varonis", "llm-security", "agentic-ai"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-12T08:56:46+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/06/new-attacks-trick-openclaw-ai-agent.html"
pipeline_version: "1.0.0"
---

## Overview

Two separate security research teams — Imperva and Varonis — have independently demonstrated high-severity attack paths against OpenClaw, a widely deployed self-hosted AI agent platform. Published concurrently in June 2026, the findings illustrate how indirect prompt injection via everyday communication objects (contacts, vCards, location pins, and emails) can subvert an AI agent into executing attacker-controlled code or exfiltrating sensitive credentials. One vulnerability has been patched; the other is architectural in nature and requires defensive design changes rather than a code fix.

## Technical Analysis

**Imperva: Message-Object Injection via Flattened Prompt Construction**

Imperva researcher Yohann Sillam identified that OpenClaw passes shared contacts, vCards, and location pins to the underlying LLM by flattening them inline into the prompt body — without any untrusted-content boundary marker. This contrasts with web-fetched content, which does receive an `untrusted-content` wrapper.

The attack abuses the serialisation format for shared contacts: `<contact: name, number>`. Since angle brackets are syntactically valid within a contact name field, an attacker can embed arbitrary LLM instructions in that field. The name is truncated in the UI (both WhatsApp and the receiving app), meaning the victim never sees the injected payload.

The same vector applies to the `FN` (full-name) field of a vCard and the label of a shared location pin. In Imperva's tests against Gemini 3.1 Pro (preview), the injected instruction successfully directed the agent to fetch and execute a remote script. The attack succeeds because models have been hardened against image-embedded instructions through training, but have had far less exposure to message-object injection patterns.

With OpenClaw's persistent memory enabled by default, a single piece of widely shared malicious content could silently compromise every agent that ingests it, absent sandboxing. OpenClaw addressed this in version 2026.4.23 by routing contact names, vCard fields, and location labels through a separate `untrusted-metadata` channel rather than the prompt body.

**Varonis: Social Engineering via Crafted Email**

Varonis Threat Labs, led by Itay Yashar, built a test agent named Pinchy on the OpenClaw platform, connected it to a Gmail inbox seeded with synthetic business data and mock secrets (AWS keys, fake customer exports). A single plain-text email instructing the agent to forward specified data to an external address was sufficient to trigger exfiltration. This is not a patchable code flaw — it reflects excessive agency: the agent had both the capability and the authorisation model to act on the instruction.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)**: Core technique in both attacks — adversarial instructions injected via contact objects and email.
- **AML.T0057 (LLM Data Leakage)**: Varonis demonstrated credential and PII exfiltration through agent action.
- **AML.T0043 (Craft Adversarial Data)**: Specially crafted vCards and contact names used as injection vehicles.
- **LLM01 (Prompt Injection)** and **LLM08 (Excessive Agency)**: The Varonis finding is a textbook excessive-agency failure; Imperva maps directly to indirect prompt injection.
- **LLM06 (Sensitive Information Disclosure)**: Both attacks result in credential or data exposure.

## Impact Assessment

Organisations running OpenClaw with integrations to email, messaging platforms, or cloud services are at direct risk. The patched Imperva vector affects any unpatched instance. The Varonis behaviour-level risk is broader — it affects any agentic deployment where the LLM is permitted to send data externally without human-in-the-loop confirmation. Imperva also noted the flattening pattern exists in other personal AI assistants, suggesting systemic industry exposure.

## Mitigation & Recommendations

1. **Patch immediately**: Upgrade OpenClaw to version 2026.4.23 or later to close the message-object injection path.
2. **Restrict agent permissions**: Apply least-privilege to all agent tools — revoke or gate outbound email, file transfer, and API write capabilities.
3. **Implement input trust boundaries**: All externally sourced data (contacts, emails, web content) must be wrapped in explicit untrusted-content markers before LLM ingestion.
4. **Enable human-in-the-loop for sensitive actions**: Require explicit user approval before agents forward data externally or execute scripts.
5. **Sandbox agent memory**: Disable or scope persistent memory to reduce the blast radius of a single injected instruction propagating across agent sessions.

## References

- [The Hacker News — New Attacks Trick OpenClaw AI Agent Into Running Code and Leaking Secrets](https://thehackernews.com/2026/06/new-attacks-trick-openclaw-ai-agent.html)
