---
title: "LLM Tool Flaw Leaks OpenAI API Keys to Third-Party Endpoints"
date: 2026-11-12T14:00:15+00:00
draft: false
slug: "llm-tool-flaw-leaks-openai-api-keys-to-third-party-endpoints"

# ── Content metadata ──
summary: "Simon Willison's LLM CLI tool (version 0.37.2) patches two security vulnerabilities reported by Daniel de Araujo that could inadvertently expose a user's configured OpenAI API key to third-party OpenAI-compatible API providers. The flaws existed in the extra-openai-models.yaml configuration mechanism, triggering key leakage under two specific conditions: an unset api_key_name or use of a responses-mode model with a specific chat completions override flag. Users running LLM with custom third-party endpoints should update immediately and rotate any potentially exposed API keys."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Nov/11/llm"
source_title: "llm 0.37.2"
source_date: 2026-11-11T17:19:52+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1782512692200-3a540734fadc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHxPcGVuYWklMjB0ZXh0JTIwdHlwb2dyYXBoeSUyMGFic3RyYWN0JTIwbGV0dGVyc3xlbnwwfDB8fHwxNzk0NDkyMDE0fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "LLM CLI tool accidentally forwarded OpenAI API keys to third-party providers in two edge cases."
tldr_who_at_risk: "Users of the LLM CLI tool who configured custom OpenAI-compatible third-party API endpoints are most exposed, risking API key theft and abuse."
tldr_actions: ["Upgrade LLM CLI to version 0.37.2 immediately", "Rotate any OpenAI API keys used with third-party endpoint configurations", "Audit extra-openai-models.yaml and llm openai endpoint configurations for untrusted providers"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News"]
tags: ["api-key-leakage", "llm-cli", "openai-api", "credential-exposure", "configuration-vulnerability", "third-party-endpoints", "simon-willison", "ghsa", "patch"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-12T14:00:15+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Nov/11/llm"
pipeline_version: "2.1.0"
content_hash: "e2938653443e2559"
---

## Overview

Simon Willison released LLM version 0.37.2 on 11th November 2026 to patch two security vulnerabilities (GHSA-v9h7-jj4g-f862 and GHSA-r639-rr7r-x72w) that could cause the tool to inadvertently send a user's configured OpenAI API key to unintended third-party API providers. The LLM CLI tool is a popular open-source utility enabling command-line access to large language models, and its support for OpenAI-compatible third-party endpoints introduced the attack surface.

## Technical Analysis

The vulnerability resides in LLM's `extra-openai-models.yaml` mechanism — now managed via the `llm openai endpoint add` command introduced in version 0.37. This feature allows users to route requests through third-party providers that implement the OpenAI API specification.

Two distinct code paths could trigger unintended API key disclosure:

1. **Unset api_key_name condition**: If the key referenced by `api_key_name` had never been stored in the secrets store, LLM would fall back to the globally configured OpenAI API key and transmit it to the third-party endpoint instead of raising an error or using no key.

2. **Responses mode with chat completions override**: When a model configured with `responses: true` was invoked using the `-o chat_completions 1` flag, the tool would similarly forward the OpenAI API key to the alternative endpoint.

In both cases, the legitimate OpenAI API key could be exfiltrated to an operator-controlled or malicious third-party endpoint, enabling credential theft and subsequent abuse of the victim's OpenAI account.

## Framework Mapping

- **AML.T0057 – LLM Data Leakage**: The unintended transmission of API credentials to third-party endpoints is a form of sensitive data leakage from an LLM tooling context.
- **AML.T0083 – Credentials from AI Agent Configuration**: The misconfiguration enables extraction of credentials stored in the agent/tool configuration layer.
- **AML.T0084 – Discover AI Agent Configuration**: A malicious endpoint operator could discover and harvest configuration secrets passed inadvertently.
- **LLM06 – Sensitive Information Disclosure**: API keys constitute highly sensitive credentials whose exposure can lead to financial harm and account takeover.
- **LLM07 – Insecure Plugin Design**: The endpoint extension mechanism lacked sufficient isolation between credential scopes for different providers.

## Impact Assessment

Users who have configured the LLM CLI tool to use third-party OpenAI-compatible endpoints and who store their OpenAI API key in the tool's secrets store are directly at risk. A malicious or compromised third-party API endpoint operator could harvest leaked keys and use them to make authenticated OpenAI API calls at the victim's expense. The impact includes financial loss through API quota consumption, potential data exposure through model queries, and account compromise.

The vulnerability is particularly concerning because the credential leakage is silent — users would have no indication their key was forwarded to an unintended recipient.

## Mitigation & Recommendations

1. **Upgrade immediately** to LLM CLI version 0.37.2 or later.
2. **Rotate OpenAI API keys** that were used in conjunction with any third-party endpoint configuration, as a precautionary measure.
3. **Audit your `extra-openai-models.yaml`** and all endpoints added via `llm openai endpoint add` to verify they point to trusted providers.
4. **Ensure `api_key_name` values are correctly set** and that corresponding secrets are stored before connecting to third-party endpoints.
5. **Monitor OpenAI API usage logs** for anomalous activity that could indicate credential misuse.

## References

- [LLM 0.37.2 Release — Simon Willison](https://simonwillison.net/2026/Nov/11/llm)
- GHSA-v9h7-jj4g-f862
- GHSA-r639-rr7r-x72w
