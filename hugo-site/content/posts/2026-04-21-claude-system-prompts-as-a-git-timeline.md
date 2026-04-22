---
title: "Claude system prompts as a git timeline"
date: "2026-04-22T02:07:46+00:00"
draft: false
slug: "claude-system-prompts-as-a-git-timeline"

# ── Content metadata ──
summary: "Simon Willison has created a git-based tool to track the evolution of Anthropic's publicly published Claude system prompts across model versions, enabling structured diff analysis of prompt changes over time. While the underlying prompts are intentionally public, the tooling lowers the barrier for adversarial reconnaissance \u2014 making it easier for threat actors to identify shifts in safety constraints, refusal heuristics, or behavioral guardrails between model releases. This kind of systematic prompt archaeology directly supports meta-prompt extraction and jailbreak development workflows."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Apr/18/extract-system-prompts/#atom-everything"
source_date: 2026-04-18T12:25:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1775441031103-1d559a6f91cd?q=80&w=1094&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0056 - LLM Meta Prompt Extraction", "AML.T0040 - ML Model Inference API Access", "AML.T0054 - LLM Jailbreak"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM01 - Prompt Injection"]

# ── TL;DR ──
tldr_what: "Git-based tooling now enables structured diff tracking of Claude's publicly released system prompt history across model versions."
tldr_who_at_risk: "Anthropic and enterprise Claude deployers are most exposed, as systematic prompt evolution tracking can reveal weakening safety constraints or exploitable behavioral shifts."
tldr_actions: ["Monitor published system prompt diffs for unintentional disclosure of safety constraint relaxations", "Treat system prompt versioning as security-relevant data — review changes before public release", "Use prompt evolution analysis defensively to identify regression in safety guardrails across model updates"]

# ── Taxonomies ──
categories: ["LLM Security", "Research", "Industry News"]
tags: ["system-prompts", "claude", "anthropic", "prompt-extraction", "model-versioning", "git", "prompt-archaeology", "llm-transparency", "behavioral-analysis", "jailbreak-research"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-21T18:04:10+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Apr/18/extract-system-prompts/#atom-everything"
pipeline_version: "1.0.0"
---

## Overview

Security researcher and developer Simon Willison has published a git-based tooling approach to systematically track the evolution of Anthropic's publicly released Claude system prompts. By parsing Anthropic's published Markdown prompt history and structuring it into per-model, per-family files with timestamped commits, the tool enables `git log`, `diff`, and `blame` operations to trace how Claude's core behavioral instructions have changed across model versions — including the recently documented delta between Claude Opus 4.6 and 4.7.

While Anthropic intentionally publishes these prompts for transparency, the creation of structured, queryable tooling around them meaningfully lowers the barrier for adversarial prompt archaeology.

## Technical Analysis

The approach converts a monolithic Markdown source (Anthropic's system prompt changelog page) into granular files scoped by model and model family, then injects synthetic git commit timestamps aligned to release dates. This creates a browsable GitHub commit history that allows researchers — and adversaries — to:

- **Diff specific model transitions** (e.g., Opus 4.6 → 4.7) to identify changed instructions
- **Attribute constraint modifications** to specific release dates using `git blame`
- **Identify removed or softened safety language** that may signal exploitable behavioral regressions
- **Correlate prompt changes with jailbreak effectiveness** across model generations

This is a low-cost, high-value reconnaissance technique. Adversaries seeking to craft jailbreaks or bypass refusal heuristics gain significant advantage from knowing precisely which instructions were added, removed, or reworded in each release.

## Framework Mapping

**AML.T0056 – LLM Meta Prompt Extraction**: The tooling operationalises systematic extraction and analysis of meta-prompt content, even when that content is technically public. Structured diff analysis goes beyond passive reading to active behavioral inference.

**AML.T0054 – LLM Jailbreak**: Prompt evolution data directly informs jailbreak development — identifying weakened constraints or newly introduced loopholes across versions.

**LLM06 – Sensitive Information Disclosure**: Even intentionally public prompts can expose unintended information about model guardrails, internal Anthropic priorities, or safety philosophy shifts when analysed in aggregate over time.

## Impact Assessment

The immediate impact is low given that these prompts are deliberately public. However, the secondary impact is moderate: tooling that structures and automates prompt analysis accelerates adversarial workflows. Security teams at Anthropic and organisations deploying Claude via API should treat prompt changelog analysis as an ongoing threat intelligence feed — one that adversaries are now better equipped to exploit systematically.

Enterprise deployers using Claude with custom system prompts are less directly affected, but may be exposed if base model behavioral changes (visible in public prompt diffs) interact unexpectedly with their own prompt layers.

## Mitigation & Recommendations

- **Review prompt diffs before publication**: Treat each system prompt update as a security artifact. Assess whether changes inadvertently signal exploitable constraint relaxations.
- **Monitor adversarial use of public prompt data**: Track community repositories and tools built around Claude prompt history for signs of jailbreak correlation research.
- **Implement version-aware red teaming**: When a new model version ships, use prompt diffs to prioritise which behavioral areas to stress-test first.
- **Establish prompt change governance**: Internally, require security review sign-off on system prompt modifications that touch refusal logic, safety boundaries, or persona constraints.

## References

- [Claude system prompts as a git timeline — Simon Willison](https://simonwillison.net/2026/Apr/18/extract-system-prompts/#atom-everything)
