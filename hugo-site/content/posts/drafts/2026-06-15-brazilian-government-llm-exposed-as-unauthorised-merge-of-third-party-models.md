---
title: "Brazilian Government LLM Exposed as Unauthorised Merge of Third-Party Models"
date: 2026-06-15T06:54:17+00:00
draft: false 
slug: "brazilian-government-llm-exposed-as-unauthorised-merge-of-third-party-models"

# ── Content metadata ──
summary: "Researchers have demonstrated that Rio de Janeiro's publicly presented 'homegrown' 397B language model is not an original creation but an undisclosed element-wise weight merge of the Nex-N2_pro model and Qwen3.5-397B-A17B. The finding was established through two independent methods: identity probing showing the model identifies as 'Nex' 79% of the time, and tensor-level statistical analysis confirming a consistent 0.6/0.4 blend across all 60 layers. This constitutes a model theft and supply chain integrity violation, with additional implications for public trust in government AI procurement and IP attribution."
source: "HN AI Security"
source_url: "https://github.com/nex-agi/Nex-N2/issues/4"
source_title: "Rio de Janeiro's \"homegrown\" LLM appears to be a merge of an existing model"
source_date: 2026-06-14T15:37:31+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1674027444484-cf52149ea050?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw3fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc4MTUwNjQ1N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0044 - Full ML Model Access", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM10 - Model Theft", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Rio's '397B homegrown LLM' is an undisclosed 60/40 weight merge of Nex-N2_pro and Qwen with no original training."
tldr_who_at_risk: "AI model developers and open-source contributors whose weights can be silently merged and redistributed under false provenance claims."
tldr_actions: ["Implement cryptographic model fingerprinting to detect unauthorised weight reuse or merges", "Probe deployed LLMs with identity and backstory queries to surface undisclosed base model provenance", "Require model cards and reproducible training logs for any government or enterprise LLM procurement"]

# ── Taxonomies ──
categories: ["Model Theft", "Supply Chain", "LLM Security", "Industry News", "Regulatory"]
tags: ["model-theft", "weight-merging", "supply-chain", "government-ai", "llm-identity-probing", "ip-violation", "open-source-abuse", "rio-de-janeiro", "qwen", "model-attribution"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider"]

# ── Pipeline metadata ──
fetched_at: "2026-06-15T06:54:17+00:00"
feed_source: "hn_ai_security"
original_url: "https://github.com/nex-agi/Nex-N2/issues/4"
pipeline_version: "1.0.0"
---

## Overview

On 14 June 2026, researchers from Nex-AGI published a GitHub issue demonstrating that `Rio-3.5-Open-397B` — a large language model presented by IplanRIO (the technology arm of the Rio de Janeiro city government) as an original, domestically developed model — is in fact an undisclosed element-wise weight merge of two existing models: Nex-N2_pro and the official Qwen3.5-397B-A17B base, blended at approximately a 0.6/0.4 ratio. No evidence of independent training by IplanRIO was found.

The case is notable not only as an IP violation but as a concrete example of how model weight merging can be weaponised to fabricate provenance — a growing concern in public-sector AI procurement and open-source model governance.

## Technical Analysis

Nex-AGI presented two independent lines of evidence:

**1. Identity Probing**
With Rio's hard-coded `"You are Rio"` system prompt stripped, the deployed model self-identified as *"Nex, from Nex-AGI"* in 79% of test queries — and as *"Rio"* in 0% of cases. The model also reproduced Nex-AGI's proprietary organisational backstory verbatim. This technique — sometimes called *system prompt extraction via identity probing* — exploits the tendency of instruction-tuned models to revert to base persona when overriding system prompts are absent.

**2. Tensor-Level Statistical Analysis**
Every weight tensor across all 60 transformer layers was found to be, to thousands of standard deviations of confidence, the linear combination:

```
Rio_weight = 0.6 × Nex_weight + 0.4 × Qwen_weight
```

This is consistent with standard model merging tools (e.g., `mergekit`) and is statistically irreconcilable with independent training or even standard fine-tuning from either base model. The researchers note that other known fine-tunes of either base model cannot be explained as such interpolations.

## Framework Mapping

- **AML.T0010 – ML Supply Chain Compromise**: The model was introduced into a government service under false provenance, corrupting the integrity of the AI supply chain for public-sector deployments.
- **AML.T0044 – Full ML Model Access**: The attacker required full access to Nex model weights to perform the merge, suggesting either a licence violation or an access control failure on the original model's distribution.
- **AML.T0056 – LLM Meta Prompt Extraction**: The identity probing technique used as evidence is itself a real-world demonstration of meta prompt and persona extraction.
- **LLM05 – Supply Chain Vulnerabilities**: The downstream government deployment inherited undisclosed third-party model components.
- **LLM10 – Model Theft**: The core violation is the uncredited, undisclosed incorporation of a proprietary model's weights.

## Impact Assessment

- **Nex-AGI**: Direct IP and reputational harm; their model is deployed in a government context without attribution or licensing agreement.
- **Public sector users**: Citizens and agencies relying on Rio-3.5 were exposed to a model with undisclosed provenance, unknown safety alignment, and potentially misrepresented capabilities.
- **AI governance broadly**: The incident undermines trust in government AI capability claims and highlights the ease with which weight merging can obscure model origins.

## Mitigation & Recommendations

1. **Cryptographic model fingerprinting**: Embed unforgeable watermarks or fingerprints at training time to survive downstream merges and detect reuse.
2. **Mandatory model cards with reproducible training provenance**: Procurement processes should require verifiable training logs, compute receipts, and dataset attestations.
3. **Identity and persona stress-testing**: Before deploying any LLM, probe identity under varied system prompt conditions to surface undisclosed base model personas.
4. **Licence enforcement for open-weight models**: Model distributors should enforce licence terms (including attribution requirements) through both legal and technical mechanisms.

## References

- [GitHub Issue #4 – nex-agi/Nex-N2](https://github.com/nex-agi/Nex-N2/issues/4)
