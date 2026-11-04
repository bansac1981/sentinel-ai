---
title: "LLMjacking Attacks Cost Enterprises $1M in Cloud AI Bills"
date: 2026-11-04T13:14:14+00:00
draft: true
slug: "llmjacking-attacks-cost-enterprises-1m-in-cloud-ai-bills"

# ── Content metadata ──
summary: "Google's Threat Intelligence Group and Mandiant have documented a surge in LLMjacking campaigns where threat actors steal cloud API keys and sell access via underground 'LLM mixer' services, generating fraudulent charges exceeding $100,000 per day at victim organisations. Two distinct operational clusters have been identified \u2014 one scanning for exposed LLM endpoints and one harvesting API credentials \u2014 with cumulative losses reaching $1 million at individual organisations. The findings highlight a maturing criminal economy around stolen AI infrastructure access, posing serious financial and operational risk to any enterprise deploying cloud-hosted LLMs."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/google-llmjacking-attacks-rack-up-1-million-in-cloud-ai-charges"
source_title: "Google: LLMjacking attacks rack up $1 million in cloud AI charges"
source_date: 2026-11-03T18:51:04+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw0fHxsaWJyYXJ5JTIwYm9va3MlMjBrbm93bGVkZ2UlMjByb3dzfGVufDB8MHx8fDE3OTM3OTgwNTR8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.1
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0040 - AI Model Inference API Access", "AML.T0044 - Full AI Model Access", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0069 - Discover LLM System Information"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM04 - Model Denial of Service", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Attackers steal cloud AI API keys and resell LLM access, costing victims up to $1 million."
tldr_who_at_risk: "Any enterprise using cloud-hosted LLM APIs with exposed or poorly secured API keys, service account credentials, or GitHub tokens."
tldr_actions: ["Audit and rotate all cloud LLM API keys and service account credentials immediately", "Enable anomaly detection and rate-limit alerts on LLM API usage to flag sudden request spikes", "Restrict API key exposure by scoping permissions and removing keys from public repositories or unprotected machines"]

# ── Taxonomies ──
categories: ["LLM Security", "Industry News", "Model Theft"]
tags: ["llmjacking", "api-key-theft", "cloud-ai-fraud", "llm-mixer", "google-gtig", "mandiant", "credential-theft", "unc6993", "jet-night", "token-abuse", "cloud-credentials"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-04T13:14:14+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/google-llmjacking-attacks-rack-up-1-million-in-cloud-ai-charges"
pipeline_version: "2.1.0"
---

## Overview

Google's Threat Intelligence Group (GTIG) and Mandiant have published findings on a rapidly escalating threat category known as LLMjacking — the hijacking of cloud-hosted large language model infrastructure via stolen API credentials. Researchers documented fraudulent charges exceeding **$100,000 in a single day** and cumulative losses reaching **$1 million** at individual victim organisations. The activity reflects a maturing underground economy in which stolen AI access is bought, sold, and resold through specialised proxy services.

## Technical Analysis

Researchers identified two distinct operational clusters driving LLMjacking activity:

1. **Endpoint scanners** — threat actors who actively scan the internet for publicly exposed LLM API endpoints.
2. **Credential harvesters** — actors who steal valid API keys from unprotected machines, GitHub repositories, active session tokens, and cloud service account configurations.

Once access is obtained, attackers sell it to underground services called **LLM mixers**. These platforms act as proxy layers, routing customer prompts through stolen API keys to legitimate cloud AI services such as those offered by Google. The victim organisation is then billed for all token consumption as if it were legitimate traffic.

Request volumes through these mixers can spike dramatically — in one documented case, a threat actor executed **more than 500,000 LLM API calls in under eight hours**, routing them through the service `jet-night.com`. This single campaign passed nearly **$1 million in token costs** to the victim. Jet Night offers "unlimited access plans" for as little as **$60/month**, illustrating the extreme cost asymmetry between attacker spend and victim damage.

Google also identified the threat cluster **UNC6993**, which uses gateway tooling to aggregate stolen keys and distribute API requests, likely monetising access via underground forums.

## Framework Mapping

- **AML.T0040 (AI Model Inference API Access)** — core technique; attackers directly abuse inference APIs via stolen keys.
- **AML.T0012 (Valid Accounts)** — stolen but technically valid credentials are used to authenticate requests.
- **AML.T0044 (Full AI Model Access)** — LLM mixer subscribers gain unrestricted model access through the proxy layer.
- **AML.T0083 (Credentials from AI Agent Configuration)** — API keys sourced from misconfigured cloud environments and repositories.
- **LLM04 (Model Denial of Service)** — request floods degrade legitimate availability and generate unsustainable billing.
- **LLM05 (Supply Chain Vulnerabilities)** — the mixer proxy infrastructure introduces an unauthorised intermediary into the AI service chain.

## Impact Assessment

The financial impact is severe and immediate. Organisations can accumulate six-figure losses within a single day before detecting anomalous usage. Beyond direct cost, victims face potential service disruption as quota limits are exhausted, reputational risk if their infrastructure is used to serve harmful content, and regulatory exposure depending on what data traverses the hijacked endpoint.

Any enterprise relying on cloud LLM APIs — particularly those using automated pipelines or CI/CD-integrated AI tooling — is at elevated risk if credential hygiene is poor.

## Mitigation & Recommendations

- **Rotate all LLM API keys** and audit which services and identities hold API credentials.
- **Implement usage-based alerting** — configure billing and request-rate anomaly detection to trigger at defined thresholds (e.g., 10× baseline in one hour).
- **Scope API key permissions** to the minimum required and enforce IP allowlisting where possible.
- **Scan repositories and CI/CD pipelines** for accidentally committed secrets using tools such as GitHub Secret Scanning or Trufflehog.
- **Monitor for UNC6993-linked infrastructure** indicators and block known LLM mixer domains (e.g., `jet-night.com`, `newapi[.]pro`).
- **Apply cloud-native guardrails** such as VPC Service Controls and organisation policy constraints on API key creation.

## References

- [Google: LLMjacking attacks rack up $1 million in cloud AI charges — BleepingComputer](https://www.bleepingcomputer.com/news/security/google-llmjacking-attacks-rack-up-1-million-in-cloud-ai-charges)
