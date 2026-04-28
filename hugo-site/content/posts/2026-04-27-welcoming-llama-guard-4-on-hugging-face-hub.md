---
title: "Welcoming Llama Guard 4 on Hugging Face Hub"
date: "2026-04-28T05:53:37+00:00"
draft: false
slug: "welcoming-llama-guard-4-on-hugging-face-hub"

# ── Content metadata ──
summary: "Meta has released Llama Guard 4, a 12B multimodal safety classifier designed to detect and filter unsafe content in both image and text inputs/outputs for production LLM deployments. The model addresses jailbreak attempts and harmful content generation across 14 hazard categories defined by the MLCommons taxonomy. Alongside it, two lightweight Llama Prompt Guard 2 classifiers (86M and 22M parameters) target prompt injection and prompt attack detection."
source: "Hugging Face Blog"
source_url: "https://huggingface.co/blog/llama-guard-4"
source_date: 2025-04-29T00:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/8720589/pexels-photo-8720589.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0054 - LLM Jailbreak", "AML.T0051 - LLM Prompt Injection", "AML.T0043 - Craft Adversarial Data", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Meta releases Llama Guard 4, a 12B multimodal safety model detecting jailbreaks and harmful content across 14 hazard categories."
tldr_who_at_risk: "Organisations deploying open-source LLMs in production are most exposed if they lack robust input/output filtering against jailbreaks and prompt injection."
tldr_actions: ["Integrate Llama Guard 4 as an input/output filter layer in any production LLM pipeline", "Deploy Llama Prompt Guard 2 lightweight classifiers for low-latency prompt injection screening", "Regularly audit configured hazard categories to ensure coverage aligns with your threat model"]

# ── Taxonomies ──
categories: ["LLM Security", "Jailbreaks", "Prompt Injection", "Research", "Industry News"]
tags: ["llama-guard-4", "meta-ai", "content-moderation", "multimodal-safety", "jailbreak-detection", "prompt-injection", "llm-guardrails", "open-source", "safety-classifier", "mlcommons"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-27T09:25:53+00:00"
feed_source: "huggingface"
original_url: "https://huggingface.co/blog/llama-guard-4"
pipeline_version: "1.0.0"
---

## Overview

Meta has released Llama Guard 4, a 12-billion-parameter dense multimodal safety classifier, along with two new Llama Prompt Guard 2 models (86M and 22M parameters). Published on the Hugging Face Hub on 29 April 2025, this release represents a meaningful defensive advancement for teams deploying large language and vision models in production environments. The models are designed to sit as guard layers around LLM pipelines, screening both user inputs and model-generated outputs for unsafe or policy-violating content.

The release is particularly notable because it directly addresses two of the most persistent adversarial threats facing deployed LLMs: jailbreak attempts via crafted image and text prompts, and prompt injection attacks intended to manipulate model behaviour.

## Technical Analysis

Llama Guard 4 is pruned from Meta's Llama 4 Scout model, converting its Mixture-of-Experts architecture into a dense feedforward model by retaining only the shared expert weights and discarding all routed experts and router layers. This yields a single-GPU-deployable model (24 GB VRAM) without additional pre-training, leveraging Scout's pre-trained representations.

The model classifies inputs and outputs across 14 hazard categories from the MLCommons taxonomy, including violent crimes, child sexual exploitation, hate speech, elections interference, and code interpreter abuse. Crucially, the active category list is configurable at inference time, giving operators control over their moderation surface.

Performance improvements over Llama Guard 3 are most pronounced in multi-image scenarios (+20% recall, +17% F1), reflecting the growing attack surface of multimodal models. Text-only English performance also improved (+4% recall, +8% F1), though at a slight cost in false positive rate (+3%).

The companion Llama Prompt Guard 2 classifiers are purpose-built for prompt injection and jailbreak detection at a fraction of the compute cost, making them suitable for high-throughput screening at the ingress layer.

## Framework Mapping

- **AML.T0054 (LLM Jailbreak):** Llama Guard 4 directly targets adversarial image and text prompts crafted to bypass LLM safety constraints.
- **AML.T0051 (LLM Prompt Injection):** Prompt Guard 2 models are explicitly designed to detect prompt injection attacks.
- **AML.T0043 (Craft Adversarial Data):** The model's multimodal capability addresses adversarially crafted image inputs designed to elicit unsafe outputs.
- **LLM01 (Prompt Injection) / LLM02 (Insecure Output Handling):** The dual input/output filtering architecture directly mitigates both categories.
- **LLM09 (Overreliance):** Teams should avoid treating Llama Guard 4 as a complete safety solution; it is one layer in a defence-in-depth strategy.

## Impact Assessment

Organisations deploying open-source LLMs without robust guardrail layers face meaningful risk from jailbreak and prompt injection exploitation. The multimodal expansion of attack surfaces — particularly multi-image inputs — increases risk for vision-capable deployments. Llama Guard 4's availability as an open, configurable model lowers the barrier for smaller teams to implement production-grade moderation.

## Mitigation & Recommendations

1. **Deploy Llama Guard 4 as both an input pre-filter and output post-filter** in any production LLM pipeline handling untrusted user inputs.
2. **Use Llama Prompt Guard 2** (22M or 86M) for low-latency first-pass prompt injection screening before routing to the primary model.
3. **Configure hazard categories explicitly** rather than relying on defaults — align category coverage with your specific regulatory and use-case threat model.
4. **Do not treat any single guardrail as sufficient**; combine with rate limiting, system prompt hardening, and output monitoring.
5. **Monitor false positive rates** in production, particularly for multilingual and multimodal inputs where model performance is lower.

## References

- [Hugging Face Blog: Welcoming Llama Guard 4](https://huggingface.co/blog/llama-guard-4)
- [Llama 4 Collection on Hugging Face Hub](https://huggingface.co/collections/meta-llama)
- [MLCommons Hazard Taxonomy](https://mlcommons.org)
