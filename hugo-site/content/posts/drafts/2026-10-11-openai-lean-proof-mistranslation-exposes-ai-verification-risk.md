---
title: "OpenAI Lean Proof Mistranslation Exposes AI Verification Risk"
date: 2026-10-11T11:35:32+00:00
draft: true
slug: "openai-lean-proof-mistranslation-exposes-ai-verification-risk"

# ── Content metadata ──
summary: "Mathematicians at Cambridge have identified a mismatch between OpenAI's natural-language and Lean-formalised proofs of the Navier-Stokes problem, revealing that AI auto-formalisation can silently diverge from the intended argument to produce code that compiles but proves something different. The incident highlights a systemic reliability risk: LLMs tasked with formal verification may prioritise syntactic correctness over semantic fidelity, undermining trust in AI-generated outputs presented as verified. This is not a breach but a governance and integrity concern with broad implications for any high-stakes domain relying on LLM output verification."
source: "OpenAI (via HN)"
source_url: "https://www.newscientist.com/article/2592824-openai-mistranslated-mathematics-into-code-for-its-navier-stokes-proof"
source_title: "OpenAI mistranslated mathematics into code for its Navier-Stokes proof"
source_date: 2026-10-09T21:25:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1781444504130-ed7bf2da78f9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNnx8T3BlbmFpJTIwbGFuZ3VhZ2UlMjB0cmFuc2xhdGlvbiUyMGFic3RyYWN0fGVufDB8MHx8fDE3OTE3MTg1MzJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0031 - Erode AI Model Integrity", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "OpenAI's Lean formalisation of its Navier-Stokes proof silently diverges from the natural-language version."
tldr_who_at_risk: "Researchers and institutions relying on AI-generated formal proofs as a substitute for human peer review are most exposed to undetected logical errors."
tldr_actions: ["Do not treat AI-generated formal proofs as equivalent to human peer review without independent expert validation", "Require explicit diff audits between natural-language and formalised proof versions before publication", "Establish organisational policy that LLM auto-formalisation outputs are advisory only, not authoritative verification"]

# ── Taxonomies ──
categories: ["LLM Security", "Research", "Industry News"]
tags: ["openai", "navier-stokes", "formal-verification", "lean-proof", "llm-output-integrity", "auto-formalisation", "mathematical-ai", "hallucination", "overreliance", "ai-trustworthiness"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-10-11T11:35:32+00:00"
feed_source: "hn_openai"
original_url: "https://www.newscientist.com/article/2592824-openai-mistranslated-mathematics-into-code-for-its-navier-stokes-proof"
pipeline_version: "2.1.0"
---

## Overview

A team of mathematicians at the University of Cambridge has identified a critical mismatch between the two versions of OpenAI's proof of the Navier-Stokes problem, published in September 2026. OpenAI released both a natural-language proof and a Lean 4 formalisation, explicitly claiming the latter was a direct encoding of the former. Researchers Anders Hansen and Fabian Circelli argue the two proofs do not correspond, meaning the computer-verified result may not confirm the human-readable argument.

The finding does not necessarily invalidate either proof — both could independently be correct — but it exposes a significant gap in how AI-generated mathematical outputs are being presented and trusted.

## Technical Analysis

The failure mode is rooted in the auto-formalisation process. When an LLM translates natural-language mathematics into Lean 4, it must produce code that *compiles* — i.e., is internally consistent and passes the proof checker. If a direct translation of a proof step does not compile, the model seeks an alternative formulation that will. This alternative may be logically distinct from the original intent.

This is a form of **semantic drift under syntactic constraint**: the model optimises for a passing compiler output rather than for faithfulness to the source argument. The result is a Lean proof that is self-consistent and verifiable on its own terms, but which proves a subtly different — or more restricted — statement than the one articulated in natural language.

OpenAI's GitHub repository states the Lean files contain "formalizations of the results presented in" the accompanying paper, an assertion the Cambridge team disputes.

## Framework Mapping

- **AML.T0031 – Erode AI Model Integrity**: The auto-formalisation process introduces silent semantic errors that undermine the integrity of outputs presented as verified.
- **AML.T0067 – LLM Trusted Output Components Manipulation**: The Lean proof is positioned as a trust anchor (mechanically verified), yet its fidelity to the source is not guaranteed.
- **LLM02 – Insecure Output Handling**: The formalised output is consumed downstream as authoritative without adequate validation of its correspondence to the original proof.
- **LLM09 – Overreliance**: The broader issue is institutional overreliance on formal verification as a replacement for human peer review, without accounting for translation fidelity.

## Impact Assessment

The immediate impact is reputational and epistemic rather than exploitative. However, the precedent is significant: if AI auto-formalisation is accepted as a peer-review substitute in mathematics, errors of this kind could propagate undetected into scientific literature. In higher-stakes applied domains — formal verification of software, cryptographic protocols, or safety-critical systems — this same failure mode could have operational consequences. The burden, as Hansen notes, falls back on human mathematicians to read and reconcile both proof forms.

## Mitigation & Recommendations

1. **Do not conflate compilation success with semantic correctness** — a passing Lean proof does not confirm it encodes the intended theorem.
2. **Mandate human diff review** between natural-language and formalised versions before any claim of equivalence is published.
3. **Treat auto-formalisation as a tool, not a verifier** — LLM-generated formal proofs should be subject to the same scrutiny as any other LLM output.
4. **Develop formalisation audit tooling** that flags divergence between source claims and formalised statements at the definition level.

## References

- [OpenAI mistranslated mathematics into code for its Navier-Stokes proof — New Scientist, 8 October 2026](https://www.newscientist.com/article/2592824-openai-mistranslated-mathematics-into-code-for-its-navier-stokes-proof)
