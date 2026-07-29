---
title: "LLMs Break Cryptographic Schemes in New CryptanalysisBench Study"
date: 2026-07-29T07:24:40+00:00
draft: true
slug: "llms-break-cryptographic-schemes-in-new-cryptanalysisbench-study"

# ── Content metadata ──
summary: "A new benchmark, CryptanalysisBench, demonstrates that frontier LLMs can perform meaningful cryptanalysis, breaking 65\u201386% of schemes with known practical vulnerabilities and producing novel attacks against previously unbroken primitives. Anthropic's Mythos Preview model uncovered new vulnerabilities in the Hawk signature scheme and reduced-round AES, representing the first AI-discovered cryptanalytic results of this kind. This signals a near-term shift in the threat landscape where AI-assisted cryptanalysis may begin to outpace human expert analysis."
source: "Schneier on Security"
source_url: "https://www.schneier.com/blog/archives/2026/07/measuring-llms-ability-to-perform-cryptanalysis.html"
source_title: "Measuring LLMs\u2019 Ability to Perform Cryptanalysis"
source_date: 2026-07-29T01:47:05+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxsaWJyYXJ5JTIwYm9va3MlMjBrbm93bGVkZ2UlMjByb3dzfGVufDB8MHx8fDE3ODUzMDk4ODB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - ML Model Inference API Access", "AML.T0044 - Full ML Model Access", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Frontier LLMs can now discover novel cryptanalytic attacks against real-world cryptographic primitives."
tldr_who_at_risk: "Organisations relying on cryptographic primitives under active standardisation or with design-level weaknesses are most exposed, as AI-assisted attacks may surface flaws faster than human review."
tldr_actions: ["Run candidate cryptographic schemes through AI-assisted analysis tools before deployment", "Monitor CryptanalysisBench results for any primitives used in production systems", "Accelerate security reviews of NIST competition candidates flagged by LLM benchmarks"]

# ── Taxonomies ──
categories: ["LLM Security", "Research", "Adversarial ML"]
tags: ["cryptanalysis", "llm-capabilities", "frontier-models", "cryptography", "benchmark", "aes", "hawk", "anthropic", "novel-attacks", "ai-assisted-hacking"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "nation-state", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-07-29T07:24:40+00:00"
feed_source: "schneier"
original_url: "https://www.schneier.com/blog/archives/2026/07/measuring-llms-ability-to-perform-cryptanalysis.html"
pipeline_version: "2.1.0"
---

## Overview

A new academic benchmark, CryptanalysisBench, published in July 2026 demonstrates that state-of-the-art large language models are no longer merely reciting known cryptanalytic results — they are beginning to generate novel ones. Five frontier models, including Anthropic's Claude Opus 4.8 and Mythos 5, OpenAI's GPT-5.5, and the open-weights GLM-5.2, were evaluated across 191 tasks spanning six families of cryptographic primitives drawn from four NIST standardisation competitions. The results represent a meaningful inflection point: AI is beginning to operate at the frontier of one of the most technically demanding domains in security.

## Technical Analysis

CryptanalysisBench is structured across three tiers of difficulty:

- **Tier 1**: Primitives with known practical breaks. Frontier models achieved a 65–86% break rate, demonstrating strong recall and application of established cryptanalytic knowledge.
- **Tier 2**: Primitives with no known practical break, tested at full strength and in scaled-down variants. Models broke 6–12 full-strength schemes and 24–61 scaled-down variants — a result that goes well beyond reproducing literature.
- **Tier 3**: A challenge set of production primitives at the frontier of human cryptanalysis.

Most significantly, Anthropic's Mythos Preview model produced genuinely novel results: a key-recovery attack exploiting a design flaw in the SpoC AEAD scheme, identification of an error in KINDI's published CCA-security proof, and new vulnerabilities in the Hawk signature scheme and reduced-round AES. These are described by the authors as previously unknown findings — the first time an AI system has demonstrably advanced the published state of the art in cryptanalysis.

The automatic verifiability of cryptanalytic attacks (a correct attack either works or it doesn't) makes this domain uniquely well-suited to LLM-driven research loops, potentially enabling rapid, automated discovery pipelines.

## Framework Mapping

- **AML.T0040 / AML.T0044**: The models are being used in full-access inference settings to reason over cryptographic specifications, analogous to adversarial use of ML model capabilities against security-critical infrastructure.
- **AML.T0047**: The capability is delivered via frontier model APIs and products, meaning the attack surface is accessible to a wide range of threat actors.
- **LLM08 – Excessive Agency**: As LLMs gain the ability to autonomously discover and verify novel attacks, the risk of autonomous cryptanalytic pipelines operating without human oversight increases materially.
- **LLM09 – Overreliance**: Defenders and standardisation bodies may be overreliant on the assumption that only human experts can find novel weaknesses in cryptographic schemes.

## Impact Assessment

The immediate impact is concentrated on cryptographic schemes in active standardisation or pre-deployment review — particularly NIST competition candidates. Legacy primitives with known structural weaknesses are at elevated risk of accelerated exploitation if adversaries deploy similar AI-assisted cryptanalysis pipelines. Nation-state actors and well-resourced cybercriminal groups are the most plausible early adopters of offensive variants of this capability.

## Mitigation & Recommendations

1. **Adopt AI-assisted pre-deployment review**: Use tools like CryptanalysisBench to stress-test candidate schemes before production deployment.
2. **Monitor benchmark publications**: Track CryptanalysisBench updates for any primitives currently in use or under consideration.
3. **Accelerate expert review of AI-flagged schemes**: Treat LLM-generated cryptanalytic findings as credible leads requiring immediate expert validation, not speculative outputs.
4. **Update threat models**: Cryptographic threat models should now account for AI-assisted adversaries capable of finding novel structural weaknesses.

## References

- [Schneier on Security – Measuring LLMs' Ability to Perform Cryptanalysis](https://www.schneier.com/blog/archives/2026/07/measuring-llms-ability-to-perform-cryptanalysis.html)
