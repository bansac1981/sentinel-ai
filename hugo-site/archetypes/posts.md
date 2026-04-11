---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true

# ── Content metadata ──
summary: ""
source: ""
source_url: ""
author: "Grid the Grey Editorial"
thumbnail: ""

# ── AI Security Classification ──
relevance_score: 0.0   # Float 0.0–10.0. Threshold for publication: 6.0

# Threat severity: CRITICAL | HIGH | MEDIUM | LOW
threat_level: ""

# ── MITRE ATLAS Techniques ──
# Reference: https://atlas.mitre.org/techniques/
# Format: "AML.TXXXX - Technique Name"
mitre_techniques: []

# ── OWASP LLM Top 10 ──
# Reference: https://owasp.org/www-project-top-10-for-large-language-model-applications/
# Format: "LLMXX - Category Name"
owasp_categories: []

# ── Taxonomies ──
categories: []
# e.g. ["LLM Security", "Adversarial ML", "Prompt Injection", "Data Poisoning",
#        "Model Theft", "Supply Chain", "Jailbreaks", "Regulatory"]

tags: []
# e.g. ["gpt-4", "prompt-injection", "rag", "langchain", "openai", "anthropic"]

frameworks: []
# e.g. ["mitre-atlas", "owasp-llm"]

threat_actors: []
# e.g. ["nation-state", "cybercriminal", "researcher"]

# ── Pipeline metadata (auto-filled by Python pipeline) ──
fetched_at: ""
feed_source: ""
original_url: ""
pipeline_version: ""
---

<!-- Grid the Grey — Article Body -->

## Overview

{{ .Name | replace "-" " " | title }}

## Technical Analysis

*Detailed technical breakdown of the vulnerability, attack vector, or security finding.*

## Framework Mapping

### MITRE ATLAS

*Which ATLAS techniques are demonstrated or referenced.*

### OWASP LLM Top 10

*Applicable OWASP LLM categories.*

## Impact Assessment

*Who is affected, what systems are at risk, and estimated severity.*

## Mitigation & Recommendations

*Actionable steps to detect, prevent, or remediate.*

## References

- [Source Article]({{ "source_url" }})
