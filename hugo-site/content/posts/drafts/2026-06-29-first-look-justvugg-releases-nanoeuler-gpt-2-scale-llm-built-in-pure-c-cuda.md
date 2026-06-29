---
title: "First Look: JustVugg Releases NanoEuler GPT-2 Scale LLM Built in Pure C/CUDA"
date: 2026-06-29T13:58:53+00:00
draft: true
slug: "first-look-justvugg-releases-nanoeuler-gpt-2-scale-llm-built-in-pure-c-cuda"

# ── Content metadata ──
summary: "NanoEuler is an open-source GPT-2-class language model (~116M parameters) built entirely from scratch in C/CUDA, including hand-written backpropagation, a BPE tokenizer, FlashAttention, pretraining, and supervised fine-tuning \u2014 with RLHF/DPO planned. For defenders, the significance lies in the democratisation of low-level, dependency-free LLM training infrastructure: adversaries gain a highly portable, auditable, and modifiable training stack that bypasses standard ML framework telemetry and supply chain controls. Security teams should treat this class of 'from-scratch' open-source LLM tooling as a potential foundation for covert fine-tuning pipelines, backdoor insertion, and evasion of model-level safety controls."
source: "Cohere AI (via HN)"
source_url: "https://github.com/JustVugg/nanoeuler"
source_title: "Show HN: NanoEuler \u2013 GPT-2 scale model in pure C/CUDA from scratch"
source_date: 2026-06-28T19:38:14+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1613572929676-7defd91738e3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOXx8bGFuZ3VhZ2UlMjBtb2RlbCUyMHRleHQlMjBnZW5lcmF0aW9uJTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzgyNzQxNDg1fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 5.2
adoption_velocity: "GRADUAL"
capability_category: "open-source-release"
attack_vectors_introduced: ["Dependency-free training stack eliminates ML framework telemetry, enabling covert model training and fine-tuning that bypasses standard supply chain monitoring", "Hand-written backpropagation and full model access enables precise, surgical backdoor insertion into model weights without leaving artefacts tied to known frameworks", "Portable C/CUDA codebase lowers the barrier for adversaries to embed custom training pipelines in air-gapped or restricted environments", "BPE tokenizer implemented from scratch can be modified to introduce tokenisation-level adversarial behaviours or data exfiltration channels", "SFT pipeline with planned RLHF/DPO support provides a ready-made infrastructure for fine-tuning models to remove safety guardrails or inject malicious behaviours", "Small model footprint (~116M params, single RTX 4070) enables rapid iteration and deployment of customised or weaponised model variants at low cost"]

# ── AI Security Classification ──
relevance_score: 5.8
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0018 - Backdoor ML Model", "AML.T0020 - Poison Training Data", "AML.T0044 - Full ML Model Access", "AML.T0010 - ML Supply Chain Compromise", "AML.T0031 - Erode ML Model Integrity", "AML.T0054 - LLM Jailbreak"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM03 - Training Data Poisoning", "LLM05 - Supply Chain Vulnerabilities", "LLM10 - Model Theft", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "NanoEuler ships a fully self-contained GPT-2-scale LLM training stack in pure C/CUDA with no ML framework dependencies."
tldr_who_at_risk: "Organisations deploying or auditing open-source LLM pipelines are newly exposed to covert, telemetry-free model training and backdoor insertion workflows."
tldr_actions: ["Inventory any internal deployments of dependency-free LLM training codebases and apply the same supply chain controls as for framework-based pipelines", "Assess whether your model integrity checks and provenance tooling cover models trained outside standard frameworks like PyTorch or TensorFlow", "Monitor for use of minimal C/CUDA LLM stacks in CI/CD or research environments as a potential indicator of covert fine-tuning activity"]

# ── Taxonomies ──
categories: ["First Look", "Adversarial ML", "Supply Chain", "Research", "LLM Security"]
tags: ["open-source-llm", "c-cuda", "from-scratch-training", "gpt-2-scale", "supply-chain", "backdoor-risk", "sft", "fine-tuning", "low-dependency", "model-integrity", "bpe-tokenizer", "flashattention"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal", "nation-state", "insider"]

# ── Pipeline metadata ──
fetched_at: "2026-06-29T13:58:53+00:00"
feed_source: "hn_cohere"
original_url: "https://github.com/JustVugg/nanoeuler"
pipeline_version: "2.1.0"
---

## Capability Overview

NanoEuler is a GPT-2-class language model (~116M parameters) built entirely from scratch in C and CUDA — no PyTorch, no autograd, no third-party ML libraries. Released publicly on GitHub by JustVugg, it includes hand-written forward and backward passes, a byte-level BPE tokenizer, a from-scratch FlashAttention implementation, a pretraining pipeline, and a supervised fine-tuning (SFT) stage. RLHF and DPO are listed as planned additions. The model trains on a single RTX 4070, making it accessible to a wide range of actors.

For defenders, the security-relevant dimension is not the model's capability ceiling — it is the architecture of the training stack itself. By eliminating all standard ML framework dependencies, NanoEuler represents a class of tooling that operates almost entirely outside the telemetry, logging, and supply chain controls that most organisations have built around PyTorch or TensorFlow ecosystems.

## Attack Surface Analysis

**Telemetry and supply chain blind spots.** Standard ML security tooling — model signing, framework-level audit hooks, dependency scanning — assumes the use of known frameworks. A C/CUDA training stack produces artefacts that most existing controls are not instrumented to detect or attribute. This creates a meaningful gap for covert model training in environments where framework-based activity is monitored.

**Surgical backdoor insertion.** Full ownership of backpropagation logic means an adversary can introduce targeted weight perturbations or backdoor triggers with precision that is difficult to achieve when working around framework abstractions. The hand-written gradient flow is fully auditable by the attacker, making it easier to verify that malicious modifications survive training.

**Low-cost SFT for safety removal.** The included SFT pipeline, combined with the planned RLHF/DPO support, provides a ready-made infrastructure for fine-tuning models to strip safety behaviours. At GPT-2 scale, this is achievable on commodity hardware in hours.

**Portable deployment in restricted environments.** The C/CUDA codebase has minimal dependencies and compiles with a standard Makefile. This portability makes it a candidate for deployment in air-gapped research environments, exfiltrated toolchains, or insider threat scenarios where Python-based tooling would be flagged.

## Framework Mapping

- **AML.T0018 (Backdoor ML Model):** Full access to backprop logic enables precise backdoor injection without framework artefacts.
- **AML.T0020 (Poison Training Data):** The bundled pretraining pipeline provides a direct interface for feeding poisoned corpora without intermediary framework validation.
- **AML.T0010 (ML Supply Chain Compromise):** A redistributed or modified version of this codebase could serve as a trojanised training tool targeting downstream model consumers.
- **AML.T0031 (Erode ML Model Integrity):** SFT and planned RLHF pipelines are directly usable for iterative safety degradation.
- **LLM03 (Training Data Poisoning)** and **LLM05 (Supply Chain Vulnerabilities)** are the primary OWASP mappings given the training infrastructure focus.

## Threat Scenarios

**Scenario 1 — Insider fine-tuning:** A privileged insider with GPU access clones NanoEuler, fine-tunes a GPT-2-scale model on proprietary internal data, and exfiltrates the resulting weights. The training run leaves no PyTorch process logs or pip install artefacts.

**Scenario 2 — Trojanised toolchain distribution:** A threat actor forks NanoEuler, introduces a subtle modification to the BPE tokenizer or weight serialisation code, and promotes the fork through developer communities. Researchers who train on the modified stack produce models with embedded backdoor triggers they cannot easily detect.

**Scenario 3 — Safety stripping at scale:** An adversary uses the SFT pipeline to fine-tune a base model checkpoint on adversarial instruction data, producing a safety-stripped variant deployable via standard GGUF/ONNX conversion. The entire pipeline runs without any framework that existing monitoring tools would flag.

## Defender Checklist

- [ ] Extend model provenance and supply chain controls to cover models trained outside PyTorch/TensorFlow — treat C/CUDA training outputs as requiring equivalent scrutiny
- [ ] Audit internal GPU environments for non-framework training processes (CUDA kernels running without associated Python processes)
- [ ] Review whether your model integrity tooling (e.g., weight hashing, signing) applies to models regardless of training stack
- [ ] Assess SFT and RLHF pipelines — including open-source ones — as potential vectors for safety degradation in your model deployment lifecycle
- [ ] Monitor GitHub and derivative repositories for forks of minimal LLM stacks that introduce non-obvious code changes to tokenizers or weight serialisation

## References

- [NanoEuler GitHub Repository](https://github.com/JustVugg/nanoeuler)
