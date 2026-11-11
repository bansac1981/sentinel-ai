---
title: "Lazarus Attack Backdoors AI Agents via Under 10 Neurons"
date: 2026-11-11T12:58:57+00:00
draft: false
slug: "lazarus-attack-backdoors-ai-agents-via-under-10-neurons"

# ── Content metadata ──
summary: "Microsoft researchers have demonstrated a technique called Lazarus that implants a hidden backdoor into open-weight LLMs by modifying fewer than 10 rarely-active neurons, requiring no model retraining. When a predefined trigger string appears in input or tool output, the backdoored model injects an attacker-controlled command into its output, which an AI agent then executes with its own permissions. The attack preserves normal model behaviour and benchmark performance, making detection extremely difficult, and poses a serious supply chain risk for any organisation deploying open-weight models."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/microsoft-researchers-show-ai-agents.html"
source_title: "Microsoft Researchers Show AI Agents Can Be Backdoored by Editing Fewer Than 10 Neurons"
source_date: 2026-11-11T07:21:05+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1521405924368-64c5b84bec60?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxkcm9uZSUyMGFlcmlhbCUyMGF1dG9ub21vdXMlMjBmbGlnaHR8ZW58MHwwfHx8MTc5NDQwMTkzNnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0018 - Manipulate AI Model", "AML.T0010 - AI Supply Chain Compromise", "AML.T0031 - Erode AI Model Integrity", "AML.T0044 - Full AI Model Access", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0080 - AI Agent Context Poisoning", "AML.T0067 - LLM Trusted Output Components Manipulation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling", "LLM03 - Training Data Poisoning"]

# ── TL;DR ──
tldr_what: "Microsoft's Lazarus technique backdoors LLMs by editing fewer than 10 neurons, triggering arbitrary command execution."
tldr_who_at_risk: "Any organisation deploying open-weight AI agents is at risk, especially those sourcing model checkpoints from third parties or with privileged insider access to model files."
tldr_actions: ["Verify cryptographic integrity of all model checkpoint files before deployment", "Restrict and audit write access to model weight files and repositories", "Apply least-privilege principles to AI agent tool permissions to limit blast radius", "Monitor agent outputs for unexpected command execution or anomalous tool invocations", "Review Microsoft's published defensive guidance for the Lazarus technique"]

# ── Taxonomies ──
categories: ["Adversarial ML", "Supply Chain", "Agentic AI", "LLM Security", "Research"]
tags: ["backdoor", "neuron-editing", "open-weight-models", "ai-agents", "supply-chain-attack", "lazarus-technique", "microsoft-research", "model-weights", "llm-security", "agentic-ai", "nemotron", "qwen", "gemma", "insider-threat", "weight-manipulation"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-11-11T12:58:57+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/microsoft-researchers-show-ai-agents.html"
pipeline_version: "2.1.0"
content_hash: "45f528301bfb8ff2"
---

## Overview

Microsoft researchers have published a proof-of-concept attack technique, dubbed **Lazarus**, demonstrating that a hidden backdoor can be implanted into an open-weight large language model by modifying fewer than 10 of its neurons — with no retraining required. When a predefined trigger string appears in a user prompt or in a tool's output, the compromised model silently injects an attacker-specified command into its response. Because the model is typically operating as an AI agent, that command is executed under the agent's own system permissions, potentially with root-level access.

Microsoft states it has not observed any threat actors using this technique in the wild and has simultaneously published defensive guidance. Nevertheless, the research represents a significant escalation in the understood threat surface of open-weight model deployment.

## Technical Analysis

The Lazarus method targets neurons in the model's feed-forward layers that fire very rarely and have negligible influence on normal outputs. These neurons are analytically recalculated to activate exclusively when the trigger token sequence is present, and each neuron forces one token of the attacker's payload into the model's output stream. A payload of *N* tokens therefore requires approximately *N* neuron edits.

The weight changes are computed directly (not via gradient descent) and optionally fine-tuned with a few hundred training steps on only the edited neurons. The rest of the model file is untouched.

In a live demonstration using **Nemotron-Terminal-8B**, seven neurons were edited across a layer containing more than 12,000 neurons, using just 23 example sessions. Results:

- **Nemotron-Terminal-8B**: ≥98.8% trigger success rate; 0% false-positive rate on trigger-free sessions (free-generation mode: ~99% success, 0.14% false-positive rate)
- **Qwen3.6-27B** (6 neurons edited): 51%–99.5% success depending on setup
- **Gemma-4-31B-IT**: 51%–99.5% success range

Backdoored models retained near-normal benchmark performance. The Qwen variants maintained most AIME math scores, and Terminal-Bench pass rates dropped only from 46.59% to 42.05% — well within noise thresholds for routine evaluation.

The payload demonstrated in the walkthrough caused an agent to download and execute a remote script as root, illustrating that the actual damage ceiling is determined by the agent's permissions, not by the size of the neuron edit.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS AML.T0018 | Manipulate AI Model | Direct modification of model weights |
| ATLAS AML.T0010 | AI Supply Chain Compromise | Attack vector via checkpoint distribution |
| ATLAS AML.T0031 | Erode AI Model Integrity | Persistent, stealthy model corruption |
| ATLAS AML.T0110 | AI Agent Tool Poisoning | Agent executes attacker commands via tools |
| OWASP LLM05 | Supply Chain Vulnerabilities | Compromised checkpoint as delivery mechanism |
| OWASP LLM08 | Excessive Agency | Agent permissions amplify payload damage |

## Impact Assessment

The primary attack vector is **supply chain compromise**: any party with write access to a model checkpoint — including insiders, compromised CI/CD pipelines, or malicious model repository contributors — can plant the backdoor. Because edited models pass standard benchmarks and exhibit normal behaviour outside trigger conditions, detection through conventional evaluation is insufficient. Organisations running agentic workloads (code execution, file system access, API orchestration) face the highest risk, as the agent's permissions define the blast radius.

## Mitigation & Recommendations

1. **Verify checkpoint integrity** — enforce cryptographic signing and hash verification of all model weight files at build and deployment time.
2. **Restrict checkpoint access** — apply strict role-based access controls to model repositories; treat weight files as privileged assets equivalent to signing keys.
3. **Least-privilege agents** — scope AI agent tool permissions to the minimum required; avoid running agents as root or with broad filesystem/network access.
4. **Anomaly monitoring** — instrument agent output pipelines to flag unexpected shell commands, downloads, or external connections.
5. **Apply Microsoft's guidance** — review the defensive recommendations published alongside the Lazarus research paper.
6. **Red-team model checkpoints** — include neuron-level backdoor scanning in model security assessments before production deployment.

## References

- [Microsoft Researchers Show AI Agents Can Be Backdoored by Editing Fewer Than 10 Neurons — The Hacker News](https://thehackernews.com/2026/11/microsoft-researchers-show-ai-agents.html)
