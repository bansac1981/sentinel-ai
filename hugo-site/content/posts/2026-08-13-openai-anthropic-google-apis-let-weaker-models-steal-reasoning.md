---
title: "OpenAI, Anthropic, Google APIs Let Weaker Models Steal Reasoning"
date: "2026-08-13T09:08:24+00:00"
draft: false 
slug: "openai-anthropic-google-apis-let-weaker-models-steal-reasoning"

# ── Content metadata ──
summary: "Researchers disclosed a cross-session, cross-user flaw in the reasoning APIs of OpenAI, Anthropic, and Google, where encrypted reasoning blocks could be replayed by weaker models to expose hidden internal reasoning, private credentials, and harmful content. Across nearly 6,700 public agent trajectories, the team recovered 704 privacy artifacts including API keys, passwords, and private keys. All three providers have since deployed mitigations that stopped the demonstrated attacks, but the disclosure highlights systemic risks in how stateless API reasoning state is shared and published."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html"
source_title: "OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models' Reasoning"
source_date: 2026-08-12T11:47:38+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1676272682018-b1435bad1cf0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxPcGVuYWklMjBkaWFsb2d1ZSUyMG1lZXRpbmclMjBwZW9wbGUlMjB0YWxraW5nfGVufDB8MHx8fDE3ODY2MDA4ODd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0040 - AI Model Inference API Access", "AML.T0063 - Discover AI Model Outputs", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0051 - LLM Prompt Injection", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0044 - Full AI Model Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM01 - Prompt Injection", "LLM10 - Model Theft", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Encrypted reasoning blocks from OpenAI, Anthropic, and Google APIs were decoded by weaker sibling models, leaking credentials and hidden content."
tldr_who_at_risk: "Developers and organisations who publish or share raw API agent logs containing encrypted reasoning blocks are most exposed, as those blocks can be replayed to extract secrets."
tldr_actions: ["Strip all reasoning blocks and opaque reasoning fields from any shared or published agent traces", "Never commit raw API transcripts to repositories, even if the visible text appears sanitised", "Audit existing public agent logs and rotate any credentials that may have been included in session history"]

# ── Taxonomies ──
categories: ["LLM Security", "Adversarial ML", "Model Theft", "Agentic AI", "Research"]
tags: ["reasoning-api", "encrypted-reasoning", "api-key-leakage", "cross-session-attack", "model-distillation", "openai", "anthropic", "google", "credential-exposure", "agent-logs", "llm-vulnerability", "thinking-blocks", "privacy-leakage"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-13T06:01:27+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html"
pipeline_version: "2.1.0"
---

## Overview

Researchers have disclosed a significant vulnerability affecting the reasoning APIs of OpenAI, Anthropic, and Google. The flaw allowed encrypted reasoning objects — designed to preserve internal chain-of-thought state across stateless API calls — to be replayed across sessions, users, and even model tiers. A weaker model within the same provider family could then act as a 'fuzzy decoder', recovering the hidden reasoning content of a stronger model without breaking any encryption. The research paper, *Stealing Reasoning Traces from Proprietary LLM APIs*, documented four distinct abuse paths and recovered 704 privacy artifacts from genuine user sessions found in public agent trajectories.

## Technical Analysis

The three providers implement reasoning state persistence differently but share a common structural weakness:

- **OpenAI** returns encrypted reasoning items that applications are expected to replay when managing conversation history manually.
- **Anthropic** carries full reasoning in an encrypted signature appended to responses.
- **Google** uses encrypted thought signatures to preserve chain-of-thought between turns.

In all three cases, the encryption was not broken. Instead, the researchers discovered that these opaque blocks were accepted and processed by the provider's inference infrastructure regardless of which session or user originally generated them. By submitting a captured reasoning block to a compatible weaker model — Claude Haiku 4.5 for Anthropic traces, GPT-5.6 Luna for OpenAI traces, and Gemini Robotics ER-1.6 for Google traces — and prompting it to 'transcribe' the reasoning, the team could recover the hidden content.

Across 6,708 public agent trajectories, the team decoded 315,320 thinking blocks and, after filtering benchmark sources, identified 704 privacy artifacts from real user sessions: 62 API keys, 33 passwords, 24 access tokens, and 7 private keys. The attack also enabled recovery of harmful content hidden behind safe visible responses and injection of prompt payloads inside opaque reasoning blocks that downstream systems would process.

## Framework Mapping

- **AML.T0057 (LLM Data Leakage)**: The core finding — hidden reasoning and embedded credentials leaked via cross-session block replay.
- **AML.T0040 (AI Model Inference API Access)**: Exploitation required only standard API access to a compatible model.
- **AML.T0056 (LLM Meta Prompt Extraction)**: Recovery of proprietary reasoning traces constitutes extraction of internal model processing logic.
- **AML.T0051 (LLM Prompt Injection)**: The paper demonstrated hiding prompt injections inside opaque reasoning blocks.
- **AML.T0083 (Credentials from AI Agent Configuration)**: API keys, tokens, and passwords were recovered from agent session logs.
- **LLM06 (Sensitive Information Disclosure)**: The primary OWASP classification given the credential and PII recovery at scale.
- **LLM10 (Model Theft)**: Proprietary reasoning traces extracted for model distillation constitute a model theft vector.

## Impact Assessment

The immediate technical risk has been mitigated by all three providers as of August 2026, and the paper confirms the main extraction attack is no longer reproducible. However, the broader impact is structural: any organisation that published agent logs between the time reasoning APIs launched and the mitigations were deployed may have exposed credentials. The 704-artifact recovery from existing public trajectories demonstrates that historical exposure is a live problem requiring active remediation.

## Mitigation & Recommendations

1. **Strip reasoning blocks before sharing**: Remove all encrypted reasoning fields, thinking blocks, and opaque signature objects from any agent traces before publication or team sharing.
2. **Do not commit raw API transcripts**: Even when visible output appears safe, embedded reasoning objects may carry sensitive state.
3. **Rotate exposed credentials**: Audit any agent logs previously made public and treat all API keys, tokens, and passwords found in session history as compromised.
4. **Treat reasoning blocks as sensitive data**: Apply the same data handling policies to reasoning objects as to plaintext credentials or PII.

## References

- [The Hacker News — Original Article](https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html)
