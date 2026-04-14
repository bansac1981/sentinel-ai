---
title: "OpenAI Revokes macOS App Certificate After Malicious Axios Supply Chain Incident"
date: 2026-04-14T05:59:28+00:00
draft: true
slug: "openai-revokes-macos-app-certificate-after-malicious-axios-supply-chain-incident"

# ── Content metadata ──
summary: "A North Korean threat group (UNC1069) compromised the popular npm Axios library via a supply chain attack, injecting a backdoor (WAVESHAPER.V2) into two poisoned versions that were inadvertently downloaded by OpenAI's macOS app-signing GitHub Actions workflow. Although OpenAI found no evidence of certificate exfiltration or user data compromise, the incident exposed the signing credentials for ChatGPT Desktop, Codex, Codex CLI, and Atlas, prompting certificate revocation and mandatory app updates by May 8, 2026. The attack highlights the acute risk of software supply chain compromises against AI product delivery pipelines."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/openai-revokes-macos-app-certificate.html"
source_date: 2026-04-13T06:50:00+00:00
author: "Grid the Grey Editorial"
thumbnail: ""

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["supply-chain-attack", "openai", "macos", "npm", "axios", "north-korea", "unc1069", "github-actions", "code-signing", "chatgpt", "waveshaper", "backdoor", "certificate-revocation", "devSecOps"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-04-14T05:59:28+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/openai-revokes-macos-app-certificate.html"
pipeline_version: "1.0.0"
---

## Overview

On March 31, 2026, OpenAI's macOS app-signing pipeline unknowingly downloaded and executed a trojanised version of the Axios npm library (v1.14.1) as part of a GitHub Actions workflow. The malicious package was part of a broader supply chain compromise attributed by Google's Threat Intelligence Group (GTIG) to UNC1069, a North Korean threat actor. While OpenAI assessed that no user data, internal systems, or intellectual property were compromised, the incident exposed signing certificates covering four flagship products — ChatGPT Desktop, Codex, Codex CLI, and Atlas — prompting full certificate revocation and mandatory user upgrades.

## Technical Analysis

UNC1069 hijacked the npm account of the legitimate Axios package maintainer and published two poisoned versions: **1.14.1** and **0.30.4**. Both versions embedded a malicious dependency named `plain-crypto-js`, which served as a loader for a cross-platform backdoor dubbed **WAVESHAPER.V2**, capable of infecting Windows, macOS, and Linux systems.

OpenAI's GitHub Actions workflow, responsible for signing macOS application binaries, resolved and executed Axios v1.14.1 during its dependency installation phase. This workflow held privileged access to:

- Code-signing certificates for ChatGPT Desktop, Codex, Codex CLI, and Atlas
- Apple notarization credentials

OpenAI's post-incident analysis concluded that the certificate was *likely* not exfiltrated, citing timing of payload execution, the sequencing of certificate injection into the job, and other mitigating environmental factors. Nonetheless, OpenAI elected to treat the certificate as compromised, applying the principle of conservative incident response.

If the certificate had been successfully stolen, an adversary could sign arbitrary binaries to make them appear as legitimate OpenAI software — a highly credible vector for targeted malware distribution against OpenAI's user base.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0010 – ML Supply Chain Compromise**: The attack directly targeted the build and signing pipeline of AI-enabled products, consistent with supply chain compromise of ML-adjacent infrastructure.
- **AML.T0047 – ML-Enabled Product or Service**: The affected artifacts (ChatGPT Desktop, Codex) are AI-enabled products whose delivery integrity was threatened.

**OWASP LLM Top 10:**
- **LLM05 – Supply Chain Vulnerabilities**: The incident is a textbook case of a third-party dependency compromise affecting the delivery chain of LLM-powered applications.

## Impact Assessment

- **OpenAI users** running macOS desktop apps signed with the compromised certificate must update before May 8, 2026, or face blocked launches due to macOS Gatekeeper enforcement.
- **Minimum affected versions** requiring update: ChatGPT Desktop < 1.2026.071, Codex App < 26.406.40811, Codex CLI < 0.119.0, Atlas < 1.2026.84.2.
- **Broader ecosystem risk**: Any organisation relying on Axios in CI/CD pipelines during the affected window may have been exposed to WAVESHAPER.V2.

## Mitigation & Recommendations

1. **Update immediately** to the latest OpenAI macOS app versions listed above before the May 8, 2026 deadline.
2. **Audit CI/CD pipelines** for dependency pinning — use lockfiles (`package-lock.json`) and integrity hashes (SRI/npm integrity fields) to prevent silent version upgrades.
3. **Implement SLSA or Sigstore** provenance verification for build-time dependencies in GitHub Actions workflows.
4. **Restrict workflow permissions** — signing credentials should be injected only at the final signing step and never exposed to dependency installation phases.
5. **Monitor npm package integrity** using tools such as Socket.dev, Snyk, or GitHub's dependency review action.
6. **Treat signing certificates as secrets** with short TTLs and automated rotation policies.

## References

- [OpenAI Revokes macOS App Certificate After Malicious Axios Supply Chain Incident — The Hacker News](https://thehackernews.com/2026/04/openai-revokes-macos-app-certificate.html)
