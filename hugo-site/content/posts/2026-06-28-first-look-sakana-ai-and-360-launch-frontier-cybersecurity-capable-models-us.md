---
title: "Sakana AI and 360 Launch Fugu and Tulongfeng Models"
date: "2026-06-29T03:13:50+00:00"
draft: false 
slug: "first-look-sakana-ai-and-360-launch-frontier-cybersecurity-capable-models-us"

# ── Content metadata ──
summary: "Sakana AI's Fugu and Chinese firm 360's Tulongfeng are frontier AI models positioned as functional alternatives to Anthropic's export-restricted Mythos and Fable 5, with Fugu explicitly designed for agentic orchestration across third-party model APIs. For defenders, the proliferation of cybersecurity-focused frontier models outside US regulatory reach removes a key friction point that previously slowed adversary access to high-capability AI offensive tooling. The agentic, multi-model orchestration design of Fugu in particular introduces compounded supply-chain and prompt-injection risk for any enterprise connecting these models to existing tool ecosystems."
source: "Cohere AI (via HN)"
source_url: "https://techcrunch.com/2026/06/27/asian-ai-startups-launch-mythos-like-models-as-anthropics-export-ban-drags-on/"
source_title: "Asian AI startups launch Mythos-like models"
source_date: 2026-06-27T13:10:21+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1760199789455-49098afd02f0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNHx8Rmlyc3QlMjBMb29rJTIwY3liZXJzZWN1cml0eSUyMHRlY2hub2xvZ3l8ZW58MHwwfHx8MTc4MjYyODMzMHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 7.1
adoption_velocity: "RAPID"
capability_category: "model-release"
attack_vectors_introduced: ["Cybersecurity-focused frontier models now accessible to actors previously blocked by US export controls, lowering barrier to AI-assisted vulnerability research and exploit development", "Fugu's native multi-model API orchestration creates new prompt-injection and instruction-hijacking paths across chained model boundaries", "Regulatory arbitrage: organisations and threat actors can substitute unvetted non-US models into pipelines that were designed around US-model safety constraints, silently degrading guardrail coverage", "360's Tulongfeng, developed by a Chinese cybersecurity firm with known government ties, introduces potential state-aligned backdoor or data-exfiltration risk for any enterprise adopting it", "Model supply-chain substitution: geopolitical pressure may cause rapid, under-reviewed swaps of trusted US models for these alternatives inside enterprise and government stacks"]

# ── AI Security Classification ──
relevance_score: 6.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access", "AML.T0018 - Backdoor ML Model", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM10 - Model Theft"]

# ── TL;DR ──
tldr_what: "Sakana AI's Fugu and 360's Tulongfeng launch as frontier, cybersecurity-capable AI models outside US export control jurisdiction."
tldr_who_at_risk: "Enterprises and government agencies in Asia and globally that substitute these models into existing AI pipelines, plus defenders relying on US-model safety controls as a de facto guardrail."
tldr_actions: ["Audit any AI model substitution decisions driven by export-control pressure and require equivalent security vetting before deployment", "Treat Fugu's multi-model API orchestration as an agentic trust boundary — apply prompt-injection controls at every inter-model handoff", "Flag 360/Tulongfeng adoption as elevated supply-chain risk given the vendor's government-adjacent profile and require enhanced data-flow isolation"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "Supply Chain", "Regulatory", "LLM Security", "Industry News"]
tags: ["sakana-ai", "fugu", "tulongfeng", "360-security", "anthropic", "mythos", "fable-5", "export-controls", "cybersecurity-ai", "agentic-orchestration", "multi-model", "geopolitical-risk", "supply-chain", "frontier-models", "regulatory-arbitrage"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-28T06:33:02+00:00"
feed_source: "hn_cohere"
original_url: "https://techcrunch.com/2026/06/27/asian-ai-startups-launch-mythos-like-models-as-anthropics-export-ban-drags-on/"
pipeline_version: "2.1.0"
---

## Capability Overview

Two new frontier AI models — Sakana AI's **Fugu** and Chinese cybersecurity firm 360's **Tulongfeng** — launched this week, each explicitly positioned against Anthropic's export-restricted **Mythos** and **Fable 5**. The timing is significant: the US government banned Anthropic from distributing Mythos and Fable 5 globally just two weeks prior, and at least one vendor (Sakana) is actively marketing the absence of export controls as a product feature.

Fugu is particularly notable from a security architecture perspective. It is designed as an **agentic orchestration layer** capable of routing tasks to other frontier models via their APIs — meaning it sits as a hub in multi-model pipelines rather than operating in isolation. Sakana targets Japanese enterprises and government agencies; 360 targets the broader Chinese and Asian market with a model explicitly framed around cybersecurity capability parity.

For defenders, this is not simply a competitive story. It is a meaningful shift in the threat landscape.

---

## Attack Surface Analysis

**1. Export-control bypass as a feature, not a bug.** Mythos was restricted precisely because of its assessed offensive capability ceiling. Models marketed as functional equivalents, now freely accessible outside US jurisdiction, represent a direct reduction in the friction that previously slowed adversary access to high-capability AI for vulnerability research, exploit generation, and offensive cyber operations.

**2. Agentic multi-model orchestration risk.** Fugu's design — routing instructions across third-party model APIs — creates compounded trust-boundary problems. Each inter-model handoff is a potential prompt-injection vector. A malicious instruction embedded in one model's output can propagate to downstream models in the chain, amplifying impact beyond what a single-model deployment would allow.

**3. Regulatory arbitrage and silent guardrail degradation.** Organisations under pressure to find US-model alternatives may substitute Fugu or Tulongfeng into pipelines originally validated against Anthropic's Constitutional AI safety layer. The new models carry no equivalent third-party safety audit history, meaning existing risk acceptance decisions become invalid without re-evaluation.

**4. State-aligned supply-chain risk (Tulongfeng).** 360 is a Chinese cybersecurity firm with documented ties to state institutions. Any enterprise ingesting Tulongfeng into its toolchain inherits the full supply-chain risk profile of that vendor relationship — including potential for model-embedded backdoors, telemetry exfiltration, or output manipulation aligned with state interests.

---

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS | AML.T0051 – LLM Prompt Injection | Multi-model orchestration multiplies injection surface |
| ATLAS | AML.T0010 – ML Supply Chain Compromise | Unvetted model substitution under geopolitical pressure |
| ATLAS | AML.T0018 – Backdoor ML Model | State-adjacent vendor (360) with opaque training provenance |
| ATLAS | AML.T0047 – ML-Enabled Product or Service | Both models exposed as API-accessible services |
| OWASP | LLM05 – Supply Chain Vulnerabilities | Rapid model substitution without equivalent vetting |
| OWASP | LLM08 – Excessive Agency | Fugu's autonomous cross-model orchestration |
| OWASP | LLM01 – Prompt Injection | Agentic API chaining across model boundaries |

---

## Threat Scenarios

**Scenario A — Adversarial offensive capability uplift.** A threat actor previously unable to access Mythos due to export controls now uses Tulongfeng or Fugu to accelerate vulnerability discovery in critical infrastructure software, with no US oversight mechanism available.

**Scenario B — Cascading prompt injection via Fugu orchestration.** An attacker plants a malicious instruction in a data source ingested by Fugu. Fugu relays the instruction to a connected code-execution model API, resulting in unauthorised action that no single-model guardrail would have caught.

**Scenario C — Silent safety regression.** A Japanese government agency, under pressure from export restrictions, swaps its Fable 5 deployment for Fugu with minimal re-evaluation. Existing red-team findings and policy controls, calibrated for Anthropic's model behaviour, no longer apply — creating undetected gaps.

---

## Defender Checklist

- [ ] **Inventory model substitutions** triggered by export-control pressure; require formal security re-assessment before any swap is approved
- [ ] **Classify Fugu deployments as agentic high-risk** and apply prompt-injection controls at every inter-model API boundary
- [ ] **Treat 360/Tulongfeng as elevated supply-chain risk**; enforce data-flow isolation and prohibit use with sensitive or classified data pending vendor audit
- [ ] **Re-run red-team and safety evaluations** whenever a new base model is introduced, even if the application layer is unchanged
- [ ] **Monitor geopolitical triggers** — further US export restrictions are likely to accelerate adoption of unvetted alternatives; maintain a standing review process
- [ ] **Assess API key and credential exposure** for any pipeline where Fugu orchestrates access to other model providers

---

## References

- [Asian AI startups launch Mythos-like models as Anthropic's export ban drags on — TechCrunch](https://techcrunch.com/2026/06/27/asian-ai-startups-launch-mythos-like-models-as-anthropics-export-ban-drags-on/)
