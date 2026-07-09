---
title: "Vertex AI SDK Bucket Squatting Flaw Enables Model Hijack"
date: "2026-06-17T04:20:26+00:00"
draft: false 
slug: "bucket-squatting-flaw-in-vertex-ai-sdk-enabled-model-hijack-and-rce"

# ── Content metadata ──
summary: "A vulnerability in the Google Cloud Vertex AI Python SDK allowed unauthenticated attackers to intercept model uploads by pre-registering predictable staging bucket names \u2014 a technique Unit 42 calls 'Pickle in the Middle'. Once a malicious model replaced the legitimate upload, arbitrary code executed inside Google's serving infrastructure via pickle deserialization. Google patched the flaw in v1.148.0 after disclosure in March 2026, but the incident highlights systemic risks in ML pipeline supply chains."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html"
source_title: "Google Vertex AI SDK Flaw Let Attackers Hijack Model Uploads via Bucket Squatting"
source_date: 2026-06-16T19:05:41+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1494412685616-a5d310fbb07d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw5fHxTdXBwbHklMjBDaGFpbiUyMGN5YmVyc2VjdXJpdHklMjB0ZWNobm9sb2d5fGVufDB8MHx8fDE3ODE2Njk3MTF8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0018 - Backdoor ML Model", "AML.T0031 - Erode ML Model Integrity", "AML.T0044 - Full ML Model Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM03 - Training Data Poisoning", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Predictable Vertex AI staging bucket names let attackers swap uploaded models with malicious pickle payloads."
tldr_who_at_risk: "Developers using the Vertex AI Python SDK without an explicit staging bucket on new projects are directly exposed to model hijacking."
tldr_actions: ["Update the Vertex AI Python SDK to v1.148.0 or later immediately", "Explicitly set the staging_bucket parameter in all SDK calls rather than relying on defaults", "Audit existing staging buckets for unexpected ownership and verify bucket access controls"]

# ── Taxonomies ──
categories: ["Supply Chain", "Adversarial ML", "Research", "LLM Security"]
tags: ["vertex-ai", "google-cloud", "bucket-squatting", "pickle-deserialization", "rce", "ml-supply-chain", "cloud-storage", "unit-42", "sdk-vulnerability", "model-hijack"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-17T04:15:11+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html"
pipeline_version: "2.0.0"
---

## Overview

A vulnerability in the Google Cloud Vertex AI SDK for Python, disclosed by Palo Alto Networks Unit 42 in March 2026 and patched by April 15, allowed an attacker with zero access to a victim's project to hijack model uploads and execute arbitrary code inside Google's serving infrastructure. Dubbed **"Pickle in the Middle"**, the attack required only the victim's Google Cloud project ID — often publicly visible — and a Cloud project of the attacker's own. No credentials, phishing, or insider access were needed.

## Technical Analysis

The root cause was the SDK's predictable default staging bucket naming scheme. When a developer omitted the `staging_bucket` parameter, the SDK derived a bucket name from the project ID and region (e.g. `project-vertex-staging-us-central1`). It checked whether the bucket existed globally but did not verify ownership. Because Cloud Storage bucket names are globally unique, an attacker could pre-register the expected name under their own project — a technique known as **bucket squatting**.

Once the victim's SDK uploaded model files to the attacker-controlled bucket, the attacker replaced the model artifact with a malicious one. The attack window was tight: Unit 42 measured approximately **2.5 seconds** between upload and Vertex AI reading the file. Their proof-of-concept used a Cloud Function that triggered on upload and replaced the model in **1.4 seconds**.

The payload exploited **pickle/joblib deserialization** — common formats for Python ML models that execute arbitrary code on load. When Vertex AI loaded the swapped model, the payload fired inside the serving container and exfiltrated an OAuth token from the instance metadata server. In Unit 42's test, that token granted access to:

- Other model artifacts in the Google-managed tenant project
- A full TensorFlow model with trained weights
- BigQuery metadata, access lists, tenant logs, GKE cluster names, and internal container image paths

Google's fix arrived in two stages: v1.144.0 (March 31) appended a random `uuid4` to the bucket name; v1.148.0 (April 15) added explicit bucket ownership verification in `Model.upload()`.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS AML.T0010 | ML Supply Chain Compromise | Attacker tampers with model artifact during the upload pipeline |
| ATLAS AML.T0018 | Backdoor ML Model | Malicious pickle payload replaces legitimate model |
| ATLAS AML.T0031 | Erode ML Model Integrity | Serving infrastructure loads attacker-controlled weights |
| OWASP LLM05 | Supply Chain Vulnerabilities | SDK default behaviour creates an exploitable dependency on unverified cloud resources |
| OWASP LLM06 | Sensitive Information Disclosure | OAuth token and tenant metadata exfiltrated post-execution |

## Impact Assessment

The attack was conditional — the default staging bucket must not yet exist and the developer must omit `staging_bucket` — but both conditions are typical for new Vertex AI projects in a region. Blast radius post-exploitation extended beyond the compromised deployment to shared Google-managed tenant infrastructure, meaning one successful attack could expose artefacts and metadata belonging to multiple workloads.

No exploitation in the wild has been reported. No CVE has been assigned as of publication.

## Mitigation & Recommendations

1. **Update immediately** to Vertex AI Python SDK v1.148.0 or later.
2. **Always set `staging_bucket` explicitly** to a bucket you own and control; never rely on SDK defaults.
3. **Audit existing staging buckets** — verify ownership and check for unexpected objects or access entries.
4. **Restrict model serving IAM roles** to least privilege; serving identities should not have broad tenant-level storage access.
5. **Treat pickle/joblib files as executable code** — validate model file integrity via checksums before loading in any pipeline.

## References

- [The Hacker News — Google Vertex AI SDK Flaw Let Attackers Hijack Model Uploads via Bucket Squatting](https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html)
