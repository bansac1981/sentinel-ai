---
title: "Python package 'llm-openai-via-codex 0.1a0' hijacks Codex CLI"
date: 2026-04-25T04:25:12+00:00
draft: false
slug: "llm-openai-via-codex-0-1a0"

# ── Content metadata ──
summary: "A new Python package, llm-openai-via-codex 0.1a0, explicitly 'hijacks' Codex CLI credentials to route API calls through an unofficial OpenAI endpoint, bypassing standard API billing and access controls. This represents a credential misuse pattern that could expose organisations to unauthorised API access and quota theft. The technique exploits an undocumented or semi-official API surface, raising supply chain and access control concerns for enterprise OpenAI deployments."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/#atom-everything"
source_date: 2026-04-23T19:22:29+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/17483873/pexels-photo-17483873.png?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0040 - ML Model Inference API Access", "AML.T0010 - ML Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "New tool hijacks Codex CLI credentials to access OpenAI models via an unofficial backdoor API endpoint."
tldr_who_at_risk: "Organisations and individuals with Codex CLI installed are at risk of credential misuse and unauthorised API quota consumption."
tldr_actions: ["Audit Codex CLI credential storage and restrict file permissions on token files", "Monitor OpenAI API usage for anomalous requests originating outside expected tooling", "Avoid installing unvetted third-party LLM plugins that request access to existing CLI credentials"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News"]
tags: ["credential-hijacking", "openai", "codex-cli", "api-abuse", "llm-tooling", "unofficial-api", "access-control", "quota-theft"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-25T04:25:12+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/#atom-everything"
pipeline_version: "1.0.0"
---

## Overview

On 23rd April 2026, Simon Willison published a release note for `llm-openai-via-codex 0.1a0`, a plugin for his `llm` CLI tool that explicitly 'hijacks' stored Codex CLI credentials to make API calls to OpenAI models via an unofficial or semi-official endpoint. The package is described as accessing OpenAI models through an existing Codex subscription, effectively bypassing the standard OpenAI API key mechanism. While framed as a developer convenience tool, the technique introduces meaningful security concerns around credential reuse, unofficial API surfaces, and supply chain trust.

## Technical Analysis

The plugin works by reading locally stored credentials from the Codex CLI — likely a token or session file written to disk during Codex CLI authentication. It then uses these credentials to authenticate requests to an undocumented or semi-official OpenAI API endpoint, allowing users to access models such as GPT-5.5 without a separate API key or billing relationship.

This pattern involves several risk factors:

- **Credential file access**: The plugin must read credential material from the local filesystem, which may be stored with insufficiently restrictive permissions.
- **Unofficial API endpoint**: Use of a non-standard API surface means requests may bypass rate limiting, audit logging, or usage controls that OpenAI applies to its standard API.
- **Third-party package trust**: Users installing this package are trusting it not to exfiltrate credential material to third parties — a trust assumption that is difficult to verify without source audit.

```bash
# Conceptual install and usage
pip install llm-openai-via-codex
llm -m openai-via-codex "Tell me about adversarial ML"
```

## Framework Mapping

- **AML.T0012 (Valid Accounts)**: The technique explicitly leverages legitimately obtained Codex credentials to gain access to AI model inference, fitting the ATLAS definition of abusing valid accounts.
- **AML.T0040 (ML Model Inference API Access)**: The tool's core function is to obtain inference access to OpenAI models through a non-sanctioned pathway.
- **AML.T0010 (ML Supply Chain Compromise)**: Distribution via a public package index with credential-handling capabilities represents a supply chain risk vector.
- **LLM05 (Supply Chain Vulnerabilities)**: Third-party plugins that handle authentication credentials introduce supply chain exposure for LLM tooling ecosystems.
- **LLM06 (Sensitive Information Disclosure)**: Credential files accessed by the plugin could be exfiltrated if the package were malicious or compromised.

## Impact Assessment

The immediate impact is low for most individual users experimenting with the tool in good faith. However, the technique normalises credential hijacking as an acceptable developer pattern, which could lower the bar for malicious actors to publish similar packages with credential-exfiltration payloads. Enterprise users with Codex CLI deployed at scale face a higher risk of credential theft or quota abuse if similar packages proliferate on package indexes.

OpenAI also faces reputational and operational risk from unofficial API endpoints being publicly documented and exploited for subscription arbitrage.

## Mitigation & Recommendations

1. **Audit Codex CLI credential storage**: Review where tokens are stored and apply strict filesystem permissions (`chmod 600`).
2. **Monitor API usage**: Use OpenAI's usage dashboard to detect anomalous request volumes not attributable to known tooling.
3. **Vet third-party LLM plugins**: Before installing any plugin that interacts with existing credentials, review source code or use a sandboxed environment.
4. **Organisational policy**: Restrict installation of unvetted packages in environments where Codex CLI or similar tools are deployed with production credentials.

## References

- [llm-openai-via-codex 0.1a0 — Simon Willison](https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/#atom-everything)
