---
title: "Tencent Releases Hy3 295B Open-Source Model with 256K Context"
date: "2026-07-07T07:50:28+00:00"
draft: false
slug: "first-look-tencent-releases-hy3-295b-moe-open-source-model-with-256k-context"

# ── Content metadata ──
summary: "Tencent has released Hy3, a 295B-parameter Mixture-of-Experts open-source model under Apache 2.0, featuring 256K context length and temporarily available for free inference via OpenRouter. The model's large context window, open weights, and Chinese provenance expand the attack surface for defenders managing LLM supply chains, jailbreak campaigns, and influence operations. Security teams should treat this as another high-capability open-weight model requiring the same scrutiny applied to comparable releases from Mistral or Meta."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Jul/6/hy3"
source_title: "tencent/Hy3"
source_date: 2026-07-06T23:57:35+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxGaXJzdCUyMExvb2slMjBjeWJlcnNlY3VyaXR5JTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzgzNDEwMjExfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 5.2
adoption_velocity: "RAPID"
capability_category: "open-source-release"
attack_vectors_introduced: ["Open weights allow unrestricted fine-tuning to remove safety filters or embed backdoors, enabling production of uncensored or weaponised model variants", "256K token context window enables large-scale document exfiltration or prompt injection payloads hidden deep within long-context inputs that may evade position-aware guardrails", "Apache 2.0 licence and free OpenRouter access lower the barrier for threat actors to prototype and scale attacks without financial attribution", "Chinese-origin model provenance introduces supply chain trust questions for organisations with data sovereignty or regulatory obligations regarding model lineage", "MoE architecture with 21B active parameters makes safety-relevant behaviour less predictable and harder to audit than dense models of equivalent active parameter count"]

# ── AI Security Classification ──
relevance_score: 5.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0044 - Full ML Model Access", "AML.T0054 - LLM Jailbreak", "AML.T0051 - LLM Prompt Injection", "AML.T0018 - Backdoor ML Model", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM03 - Training Data Poisoning", "LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM10 - Model Theft"]

# ── TL;DR ──
tldr_what: "Tencent releases Hy3, a 295B open-weight MoE model with 256K context under Apache 2.0."
tldr_who_at_risk: "Organisations deploying or evaluating open-weight LLMs, particularly those with supply chain governance or data residency requirements, are newly exposed."
tldr_actions:
  - "Inventory any downstream integrations or pipelines that may automatically pull or reference new Hugging Face model releases and validate provenance controls"
  - "Assess your 256K-context guardrail coverage — test whether existing prompt injection and output filtering defences hold at long-context boundaries"
  - "Apply standard open-weight model intake procedures: red-team for jailbreaks, audit training data claims, and document Chinese-origin provenance for compliance reporting"

# ── Taxonomies ──
categories: ["First Look", "LLM Security", "Supply Chain", "Jailbreaks", "Industry News"]
tags: ["tencent", "hy3", "open-weights", "mixture-of-experts", "long-context", "256k-context", "apache-2-0", "openrouter", "chinese-ai", "model-release", "supply-chain", "jailbreak-risk"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "researcher", "hacktivist"]

# ── Pipeline metadata ──
fetched_at: "2026-07-07T07:43:31+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Jul/6/hy3"
pipeline_version: "2.1.0"
---

## Capability Overview

Tencent's Hy Team has released Hy3, a 295B-parameter Mixture-of-Experts (MoE) model with approximately 21B active parameters per forward pass and an additional 3.8B multi-token prediction layer. Published under the permissive Apache 2.0 licence and distributed via Hugging Face (598GB full precision; 300GB in FP8 quantised form), Hy3 is immediately accessible to any actor with sufficient compute. A free inference tier via OpenRouter is available until 21 July 2026, further lowering the barrier to experimentation.

The model's headline features from a defender's perspective are its 256K token context window and its open-weight status. These two characteristics, in combination, shift the capability baseline for what a well-resourced or patient threat actor can accomplish without proprietary API access.

## Attack Surface Analysis

**Open weights as a force multiplier.** Apache 2.0 with no use restrictions means any actor can download, fine-tune, and redistribute modified versions of Hy3. This enables the removal of safety filters, the embedding of backdoors into domain-specific fine-tunes, or the creation of uncensored variants distributed through informal channels. The model's competitive performance against models 2–5× its parameter count means these derivative variants are practically capable, not merely symbolic.

**256K context and guardrail evasion.** Most deployed content filters and prompt injection defences are optimised for short-to-medium context lengths. At 256K tokens, adversaries can craft payloads that embed malicious instructions deep within large documents — contracts, codebases, research papers — where attention-based anomaly detection is less reliable. Defenders whose RAG pipelines or document summarisation workflows feed into Hy3 endpoints should specifically test injection at positions beyond 32K tokens.

**Supply chain and provenance concerns.** Hy3 is a Chinese-origin model released by a major commercial entity (Tencent). For organisations subject to data handling regulations, export controls, or internal AI governance policies that require model lineage documentation, this provenance introduces a compliance surface. The training data composition has not been independently audited, and the "50+ products" cited in post-training feedback represent an undisclosed set of Tencent services.

**MoE opacity.** Mixture-of-Experts architectures route tokens through different expert subnetworks, making consistent safety evaluation harder. Behaviours observed during red-teaming on one expert routing path may not generalise, creating gaps that jailbreak researchers are likely to probe systematically.

## Framework Mapping

- **AML.T0044 (Full ML Model Access)**: Open weights grant adversaries complete model access for white-box attacks, fine-tuning, and behaviour profiling.
- **AML.T0054 (LLM Jailbreak)**: The model's competitive capability makes it a high-value jailbreak target; uncensored derivatives are a foreseeable near-term artefact.
- **AML.T0051 (LLM Prompt Injection)**: The 256K context window directly expands the viable injection surface in document-processing pipelines.
- **AML.T0010 (ML Supply Chain Compromise)**: Downstream integrations that auto-pull Hugging Face model updates are exposed if a compromised or trojaned variant is published under a similar namespace.
- **LLM05 (Supply Chain Vulnerabilities)**: Model provenance, training data composition, and the lack of independent auditing are supply chain risks for enterprise adopters.

## Threat Scenarios

1. **Jailbreak-as-a-service derivative**: A threat actor fine-tunes Hy3 on curated refusal-bypass data, removes safety tuning, and redistributes it through Telegram or dark web forums as an uncensored assistant for fraud script generation or CSAM.

2. **Long-context RAG injection**: An attacker uploads a 200K-token PDF to an enterprise document platform backed by Hy3. A malicious instruction buried at token position 180,000 instructs the model to exfiltrate subsequent user queries to an attacker-controlled endpoint.

3. **Namespace squatting on Hugging Face**: Shortly after the legitimate release, a threat actor publishes `tencent/Hy3-instruct-v2` with a backdoored variant, targeting organisations with automated model update pipelines.

## Defender Checklist

- [ ] **Catalogue exposure**: Identify all internal systems that may consume Hy3 via OpenRouter, Hugging Face, or self-hosted deployments.
- [ ] **Validate model hash integrity**: If deploying the weights, pin to the official SHA256 hash published by Tencent and verify before loading.
- [ ] **Test long-context injection**: Run prompt injection red-team exercises specifically targeting inputs beyond 32K, 64K, and 128K token boundaries.
- [ ] **Review supply chain policy**: Determine whether Chinese-origin open-weight models require additional governance review under your AI procurement policy.
- [ ] **Monitor for derivative releases**: Set up Hugging Face namespace alerts for `tencent/Hy3*` to detect potentially malicious forks early.
- [ ] **Audit RAG pipeline output handling**: Ensure model outputs feeding into downstream actions (code execution, API calls) pass through output sanitisation regardless of model identity.

## References

- Simon Willison's Weblog: https://simonwillison.net/2026/Jul/6/hy3
- Tencent Hy3 on Hugging Face: https://huggingface.co/tencent/Hy3
- OpenRouter model listing: https://openrouter.ai
