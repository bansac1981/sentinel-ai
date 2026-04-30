---
title: "SQL Injection in LiteLLM Proxy Exposes LLM Provider Keys Within 36 Hours"
date: "2026-04-30T05:32:40+00:00"
draft: false
slug: "sql-injection-in-litellm-proxy-exposes-llm-provider-keys-within-36-hours"

# ── Content metadata ──
summary: "A critical SQL injection vulnerability (CVE-2026-42208, CVSS 9.3) in BerriAI's LiteLLM AI gateway was actively exploited within 36 hours of public disclosure, targeting database tables storing upstream LLM provider API keys including OpenAI, Anthropic, and AWS Bedrock credentials. Attackers demonstrated prior knowledge of LiteLLM's internal schema, selectively probing credential and configuration tables while ignoring user and team tables. The blast radius extends far beyond a typical web-app SQL injection, as successful extraction equates to cloud-account-level compromise across multiple AI provider accounts."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/litellm-cve-2026-42208-sql-injection.html"
source_title: "LiteLLM CVE-2026-42208 SQL Injection Exploited within 36 Hours of Disclosure"
source_date: 2026-04-29T05:34:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1717501218511-768944e2c325?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3NzQzMDYyMHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0040 - ML Model Inference API Access", "AML.T0047 - ML-Enabled Product or Service", "AML.T0010 - ML Supply Chain Compromise", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Critical SQL injection in LiteLLM proxy exploited within 36 hours to steal LLM provider API keys."
tldr_who_at_risk: "Any organisation running LiteLLM proxy versions >=1.81.16 <1.83.7 with exposed API endpoints, particularly those managing high-value LLM provider credentials."
tldr_actions: ["Patch LiteLLM to version 1.83.7-stable or later immediately", "Rotate all LLM provider API keys stored in the proxy database as a precaution", "Set 'disable_error_logs: true' under general settings if immediate patching is not possible"]

# ── Taxonomies ──
categories: ["LLM Security", "Supply Chain", "Industry News"]
tags: ["litellm", "sql-injection", "cve-2026-42208", "api-key-theft", "ai-gateway", "active-exploitation", "credential-theft", "openai", "anthropic", "aws-bedrock", "berri-ai", "proxy-security", "n-day-exploit"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-30T05:07:18+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/litellm-cve-2026-42208-sql-injection.html"
pipeline_version: "1.0.0"
---

## Overview

A critical SQL injection vulnerability in BerriAI's LiteLLM open-source AI gateway — tracked as CVE-2026-42208 with a CVSS score of 9.3 — was actively weaponised in the wild within 36 hours of public disclosure. First exploitation activity was recorded on April 26, 2026, approximately 26 hours after the GitHub advisory was indexed. LiteLLM, which acts as a unified proxy layer for routing requests across multiple LLM providers, is widely deployed in enterprise and developer environments, making this a high-impact incident with broad implications for AI infrastructure security.

## Technical Analysis

The vulnerability stems from improper parameterisation of a database query executed during proxy API key validation. Caller-supplied key values were interpolated directly into the query string rather than passed as bound parameters — a textbook SQL injection pattern.

```
# Vulnerable pattern (simplified)
query = f"SELECT * FROM litellm_credentials WHERE key = '{user_supplied_key}'"

# Safe pattern
query = "SELECT * FROM litellm_credentials WHERE key = ?"
cursor.execute(query, (user_supplied_key,))
```

Critically, the injection point is reachable **unauthenticated** via the proxy's error-handling path on any LLM API route (e.g., `POST /chat/completions`) by crafting a malicious `Authorization` header. This means no prior access is required to trigger the vulnerability.

Sysdig researchers observed two distinct attack phases from IP addresses `65.111.27[.]132` and `65.111.25[.]67`, both attributed to the same operator. The attacker specifically targeted:

- `litellm_credentials.credential_values` — upstream LLM provider API keys
- `litellm_config` — proxy runtime configuration

Notably, tables such as `litellm_users` and `litellm_team` were left untouched, indicating targeted, schema-aware reconnaissance rather than opportunistic scanning.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0040 (ML Model Inference API Access):** The attack targets the inference proxy layer to extract credentials enabling downstream LLM access.
- **AML.T0057 (LLM Data Leakage):** Successful exploitation leaks sensitive API keys and configuration from the proxy's backing store.
- **AML.T0012 (Valid Accounts):** Extracted credentials could be used to authenticate to LLM provider platforms as legitimate users.

**OWASP LLM Top 10:**
- **LLM06 (Sensitive Information Disclosure):** Core impact; credential extraction exposes multi-provider API keys.
- **LLM05 (Supply Chain Vulnerabilities):** LiteLLM sits upstream of multiple LLM providers, creating a single point of compromise with cascading impact.

## Impact Assessment

The severity here exceeds a conventional web-application SQL injection. A single compromised `litellm_credentials` row may contain an OpenAI organisation key with five-figure monthly spend limits, an Anthropic workspace admin key, and AWS Bedrock IAM credentials. As Sysdig notes, the blast radius is closer to a **cloud-account compromise** than a typical data breach. Affected organisations face risks including:

- Unauthorised LLM API spend and resource abuse
- Exfiltration of proprietary prompts and completions via hijacked keys
- Lateral movement into cloud environments via compromised IAM credentials
- Full proxy takeover enabling man-in-the-middle interception of LLM traffic

This incident also follows a March 2026 supply chain attack against LiteLLM by the TeamPCP group, indicating the project is under sustained adversarial attention.

## Mitigation & Recommendations

1. **Patch immediately** to LiteLLM version `1.83.7-stable` or later.
2. **Rotate all LLM provider API keys** stored in the proxy database — treat them as compromised.
3. **Apply the interim workaround**: set `disable_error_logs: true` under `general_settings` if patching cannot be done immediately.
4. **Restrict network access** to the LiteLLM proxy — it should not be publicly reachable without authentication.
5. **Audit access logs** for requests to `/chat/completions` or other LLM routes with anomalous `Authorization` header values originating from untrusted IPs.
6. **Monitor for IPs** `65.111.27[.]132` and `65.111.25[.]67` in firewall and proxy logs.

## References

- [The Hacker News — LiteLLM CVE-2026-42208 SQL Injection Exploited within 36 Hours](https://thehackernews.com/2026/04/litellm-cve-2026-42208-sql-injection.html)
