---
title: "About Grid the Grey"
date: 2024-01-01
draft: false
description: "Grid the Grey is an automated AI security intelligence platform tracking adversarial ML, LLM vulnerabilities, and machine learning security threats — mapped to MITRE ATLAS and OWASP LLM Top 10."
_build:
  list: never
---

## What is Grid the Grey?

Grid the Grey is an automated threat intelligence platform focused exclusively on the intersection of artificial intelligence and cybersecurity. We aggregate, filter, and analyse security research from across the web — then map every article to industry frameworks so you can act on it.

## What We Cover

AI security is moving faster than any single researcher can track. Grid the Grey monitors 9 curated RSS feeds covering:

- **Prompt injection and jailbreaks** — direct and indirect attacks against LLM-powered applications
- **Adversarial machine learning** — evasion, perturbation, and physical-world attacks on ML classifiers
- **Supply chain threats** — malicious model weights, poisoned datasets, compromised ML pipelines
- **LLM vulnerabilities** — insecure output handling, sensitive data disclosure, excessive agency
- **Regulatory and compliance** — CISA advisories, EU AI Act developments, NIST AI RMF guidance

## Framework Mapping

Every article is automatically evaluated against two industry-standard frameworks:

**MITRE ATLAS (Adversarial Threat Landscape for AI Systems)** — the definitive taxonomy of adversarial techniques targeting AI and ML systems. Where applicable, articles are tagged with the relevant ATLAS technique IDs (e.g. AML.T0051 — LLM Prompt Injection).

**OWASP LLM Top 10** — the OWASP foundation's ranking of the most critical security risks to LLM applications. Articles are mapped to the relevant LLM risk categories (e.g. LLM01 — Prompt Injection, LLM05 — Supply Chain Vulnerabilities).

## How It Works

The pipeline runs daily at 9:30 AM IST:

1. Fetch articles from 9 curated RSS feeds
2. Pre-filter by AI/security keywords
3. Score relevance with Claude AI (threshold: 6.0/10)
4. Generate analysis with MITRE ATLAS and OWASP mapping
5. Publish to this site and the weekly newsletter

Articles scoring below 6.0 are discarded. Everything published here has been evaluated as directly relevant to AI security practitioners.

## Sources

We aggregate from verified, high-quality sources:

- The Hacker News
- SecurityWeek
- Dark Reading
- CrowdStrike Blog
- SANS Internet Storm Center
- Hacker News (AI security filtered)
- Schneier on Security
- Google Project Zero
- Krebs on Security

## Newsletter

The weekly **AI Threat Briefing** distils the week's most critical developments into a concise digest. Subscribe free via Beehiiv — no spam, unsubscribe anytime.

## Disclaimer

Content is aggregated from public sources for research and educational purposes. Framework mappings are AI-assisted and may require expert validation. Grid the Grey is an independent publication and is not affiliated with MITRE, OWASP, or any of the source publications.
