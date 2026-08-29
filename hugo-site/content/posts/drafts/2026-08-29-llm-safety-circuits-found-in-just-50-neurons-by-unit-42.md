---
title: "LLM Safety Circuits Found in Just 50 Neurons by Unit 42"
date: 2026-08-29T06:54:28+00:00
draft: true
slug: "llm-safety-circuits-found-in-just-50-neurons-by-unit-42"

# ── Content metadata ──
summary: "Palo Alto Unit 42 researchers have developed a technique called perturbation probing that identifies the precise feed-forward neurons responsible for LLM safety refusal behaviour, finding that as few as 50 neurons out of 350,208 control safety guardrails in Qwen3-4B. Disabling those neurons altered responses on 80% of tested harmful prompts, demonstrating that RLHF-aligned safety is structurally fragile rather than distributed. The research also introduces an FFN/Skip ratio metric that predicts model safety fragility across 13 models with 81% explanatory power, giving defenders a rapid quantitative tool for comparing alignment robustness."
source: "Palo Alto Unit 42"
source_url: "https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety"
source_title: "Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety"
source_date: 2026-08-28T22:00:07+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1536965764833-5971e0abed7c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMHx8bGlicmFyeSUyMGJvb2tzJTIwa25vd2xlZGdlJTIwcm93c3xlbnwwfDB8fHwxNzg3OTg2NDMwfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0044 - Full AI Model Access", "AML.T0018 - Manipulate AI Model", "AML.T0031 - Erode AI Model Integrity", "AML.T0054 - LLM Jailbreak", "AML.T0015 - Evade AI Model"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM09 - Overreliance", "LLM01 - Prompt Injection"]

# ── TL;DR ──
tldr_what: "50 neurons control LLM safety refusals; disabling them bypasses guardrails on 80% of harmful prompts."
tldr_who_at_risk: "Enterprises deploying open-weight LLMs with internal access are most exposed, as attackers with model internals access can surgically disable safety circuits."
tldr_actions: ["Deploy external content filters and runtime guardrails independent of base model alignment", "Use the FFN/Skip ratio metric to benchmark alignment robustness before production deployment", "Restrict internal model access to prevent neuron-level manipulation of safety circuits"]

# ── Taxonomies ──
categories: ["LLM Security", "Adversarial ML", "Jailbreaks", "Research"]
tags: ["perturbation-probing", "llm-safety", "alignment-fragility", "neuron-steering", "rlhf", "jailbreak", "qwen3", "unit-42", "ffn-skip-ratio", "safety-guardrails"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-29T06:54:28+00:00"
feed_source: "unit42"
original_url: "https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety"
pipeline_version: "2.1.0"
---

## Overview

Researchers from Palo Alto Unit 42 have published findings that fundamentally challenge how the industry conceptualises LLM safety alignment. Their technique, called **perturbation probing**, pinpoints the exact feed-forward neurons responsible for refusal behaviour in aligned large language models — and the results are stark: safety in Qwen3-4B is concentrated in just 50 neurons out of 350,208, representing 0.014% of the model's feed-forward network. Disabling those neurons altered the model's response format on 80% of 520 standard harmful-prompt benchmarks. This is not a theoretical edge case; it is a measurable architectural vulnerability with direct implications for enterprise AI deployments.

## Technical Analysis

Perturbation probing works by running only two forward passes per prompt and computing which neurons show causal responsibility for a target behaviour — in this case, safety refusals. The low computational overhead makes it practical to apply across every model an organisation deploys, unlike prior mechanistic interpretability work that required substantial compute.

Key findings:
- **Qwen3-4B**: 50 neurons control the safety refusal template. Removing them changed responses on 80% of 520 harmful-prompt benchmarks and was replicated on a second 200-prompt benchmark.
- **Qwen3.5-2B**: 20 neurons were sufficient to eliminate false agreement in multi-turn conversations, dropping the sycophancy rate from 36.7% to 0% across 30 questions.
- **FFN/Skip ratio**: A single scalar metric derived from the same computation that predicts safety fragility across models. Tested on 13 models, it explained 81% of the variance in how much a model's safety behaviour changed when 50 neurons were disabled.

The underlying mechanism reflects the nature of RLHF training: rather than distributing safety-relevant computation throughout the network, alignment training appears to concentrate refusal behaviour into a small, identifiable template layer. An adversary with white-box access — increasingly realistic given the proliferation of open-weight models — could surgically excise this layer without degrading general model capability.

## Framework Mapping

- **AML.T0044 (Full AI Model Access)**: The attack vector requires internal model access, consistent with white-box threat scenarios.
- **AML.T0018 (Manipulate AI Model)** and **AML.T0031 (Erode AI Model Integrity)**: Neuron removal directly manipulates the model's trained safety behaviour.
- **AML.T0054 (LLM Jailbreak)**: The end result — bypassing safety refusals — maps directly to jailbreak outcomes.
- **AML.T0015 (Evade AI Model)**: The technique systematically evades alignment-based safety controls.
- **LLM09 (Overreliance)**: Organisations relying solely on base model alignment without external controls are structurally overexposed.

## Impact Assessment

The primary risk is to organisations deploying open-weight models in environments where adversaries or malicious insiders could access model weights or activation layers. The FFN/Skip ratio also has a secondary implication: even without adversarial intent, normal fine-tuning or quantisation runs could inadvertently shift these critical neurons, silently degrading safety properties in production models. The research does not identify active exploitation in the wild, but the technique is sufficiently accessible that weaponisation by capable threat actors is a credible near-term concern.

## Mitigation & Recommendations

1. **Layer external guardrails**: Do not rely on base model RLHF alignment as the sole safety control. Deploy content classifiers and output filters at the inference layer.
2. **Apply the FFN/Skip ratio**: Use this metric as a pre-deployment safety fragility screen before releasing models to production.
3. **Restrict model access**: Limit who can access raw model weights and internal activations; treat open-weight model files with the same sensitivity as source code.
4. **Re-evaluate after fine-tuning**: Any fine-tuning, quantisation, or pruning run should trigger a re-assessment of safety neuron integrity.
5. **Red-team internal access scenarios**: Extend adversarial testing to white-box threat models, not just black-box prompt-based attacks.

## References

- [Perturbation Probing: A New Diagnostic for the Fragility of LLM Safety — Palo Alto Unit 42](https://unit42.paloaltonetworks.com/perturbation-probing-llm-safety)
