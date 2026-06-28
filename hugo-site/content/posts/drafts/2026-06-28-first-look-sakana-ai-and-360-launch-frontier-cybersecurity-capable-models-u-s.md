---
title: "First Look: Sakana AI and 360 Launch Frontier Cybersecurity-Capable Models Bypassing U.S. Export Controls"
date: 2026-06-28T06:32:10+00:00
draft: true
slug: "first-look-sakana-ai-and-360-launch-frontier-cybersecurity-capable-models-u-s"

# ── Content metadata ──
summary: "Sakana AI's Fugu and Chinese firm 360's Tulongfeng have emerged as direct alternatives to Anthropic's export-controlled Mythos and Fable 5 models, with Fugu explicitly designed for multi-agent orchestration and marketed as free from export control risk. For defenders, this signals a fragmentation of the frontier AI supply chain where non-U.S. cybersecurity-capable models \u2014 with potentially fewer safety constraints and less transparent training provenance \u2014 become embedded in enterprise and government environments across Asia. Security teams must now account for a broader, less auditable model ecosystem when assessing AI-related supply chain risk and agentic tooling deployments."
source: "Mistral AI (via HN)"
source_url: "https://techcrunch.com/2026/06/27/asian-ai-startups-launch-mythos-like-models-as-anthropics-export-ban-drags-on/"
source_title: "Asian AI startups launch Mythos-like models"
source_date: 2026-06-27T13:10:21+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1666875758412-5957b60d7969?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxNXx8Rmlyc3QlMjBMb29rJTIwY3liZXJzZWN1cml0eSUyMHRlY2hub2xvZ3l8ZW58MHwwfHx8MTc4MjYyODMzMHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 6.5
adoption_velocity: "RAPID"
capability_category: "model-release"
attack_vectors_introduced: ["Agentic model with cross-API orchestration capabilities (Fugu) introduces new pivot paths across integrated tool ecosystems without U.S. oversight or safety review", "Export-control arbitrage creates incentive to route sensitive workloads through less-scrutinised non-U.S. models, increasing supply chain opacity", "Cybersecurity-focused model (Tulongfeng) designed to match Mythos capability may lower the barrier for offensive cyber capability generation outside existing regulatory guardrails", "Multi-model orchestration via third-party APIs introduces prompt injection and data leakage vectors across model boundaries", "Government and enterprise adoption of Fugu in Japan/Asia may introduce models with unaudited training data provenance into critical infrastructure workflows"]

# ── AI Security Classification ──
relevance_score: 6.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0051 - LLM Prompt Injection", "AML.T0040 - ML Model Inference API Access", "AML.T0057 - LLM Data Leakage", "AML.T0054 - LLM Jailbreak"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Sakana AI launched Fugu and China's 360 launched Tulongfeng as frontier alternatives to Anthropic's export-banned Mythos and Fable 5 models."
tldr_who_at_risk: "Enterprises and government agencies in Asia adopting these models for agentic workflows, and any organisation with supply chain dependencies on Fugu's cross-API orchestration."
tldr_actions: ["Inventory any third-party AI models entering your supply chain from non-U.S. vendors and assess their training data provenance and safety evaluation transparency", "Evaluate agentic deployments using Fugu's multi-model orchestration for prompt injection and data leakage risks across API boundaries", "Establish model procurement policies that require safety audit documentation regardless of a model's export control status"]

# ── Taxonomies ──
categories: ["First Look", "Supply Chain", "Agentic AI", "LLM Security", "Regulatory", "Industry News"]
tags: ["sakana-ai", "fugu", "tulongfeng", "360-security", "anthropic", "mythos", "fable-5", "export-controls", "agentic-ai", "multi-model-orchestration", "cybersecurity-llm", "supply-chain", "asia-ai", "frontier-models", "non-us-models"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state", "cybercriminal", "insider"]

# ── Pipeline metadata ──
fetched_at: "2026-06-28T06:32:10+00:00"
feed_source: "hn_mistral"
original_url: "https://techcrunch.com/2026/06/27/asian-ai-startups-launch-mythos-like-models-as-anthropics-export-ban-drags-on/"
pipeline_version: "2.1.0"
---

## Capability Overview

Two new frontier AI models have launched in Asia, explicitly positioned as capable alternatives to Anthropic's Mythos and Fable 5 — models the Trump Administration has placed under export controls, barring non-U.S. access. Sakana AI (Tokyo) launched **Fugu**, a model targeting Japanese government and enterprise customers, with a core capability for **multi-agent orchestration via third-party APIs**. Chinese cybersecurity firm 360 launched **Tulongfeng**, framed as a direct Mythos competitor in the cybersecurity domain. Sakana's marketing explicitly leads with the proposition of "frontier capability without the risk of export controls," a positioning that carries significant implications for how non-U.S. AI adoption will be governed in practice.

For defenders, this is not merely a geopolitical story. It marks a concrete expansion of the frontier AI ecosystem beyond the regulatory and safety frameworks that have, however imperfectly, applied to U.S. model releases.

## Attack Surface Analysis

**Multi-model orchestration as an attack surface.** Fugu's core differentiator — the ability to orchestrate access to other models through their APIs — introduces a chained trust problem. An agent that mediates between multiple model APIs creates new pathways for prompt injection across model boundaries, potential data exfiltration through intermediate model calls, and privilege escalation if downstream models have broader tool access than the originating context assumes.

**Reduced safety audit transparency.** Neither Tulongfeng nor Fugu are subject to U.S. AI safety frameworks or the emerging federal AI procurement standards. Defenders integrating these models into enterprise pipelines inherit unknown residual risks from training data provenance, RLHF alignment choices, and red-team coverage — none of which are publicly documented to the same degree as comparable U.S. models.

**Cybersecurity-specific model risk.** Tulongfeng is explicitly designed for cybersecurity parity with Mythos — a model reportedly powerful enough to warrant a U.S. export ban. A capable offensive-grade AI model now available outside U.S. jurisdictional control lowers the barrier for generating functional offensive cyber tooling, vulnerability analysis, and attack planning assistance for actors who previously lacked access.

**Export-control arbitrage as a threat vector.** The deliberate positioning of these models as "export-control safe" creates market incentives for organisations to route sensitive workloads through non-U.S. models to avoid compliance friction — inadvertently increasing exposure to less-vetted model infrastructure.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** Non-U.S. models entering enterprise supply chains with limited provenance visibility.
- **AML.T0051 (LLM Prompt Injection) / LLM01:** Fugu's cross-API orchestration creates multi-hop injection surfaces.
- **AML.T0047 (ML-Enabled Product or Service):** Both models are being embedded in production government and enterprise contexts.
- **LLM08 (Excessive Agency):** Agentic orchestration without adequate sandboxing risks uncontrolled lateral action.
- **LLM05 (Supply Chain Vulnerabilities):** Opaque training pipelines and lack of third-party safety audits.

## Threat Scenarios

**Scenario 1 — Agentic pivot via Fugu orchestration.** A Japanese government agency deploys Fugu as an internal assistant with access to document management and external model APIs. A malicious prompt embedded in an incoming document causes Fugu to exfiltrate contents via a subsidiary API call to an attacker-controlled model endpoint.

**Scenario 2 — Offensive tooling via Tulongfeng.** A threat actor without access to Mythos uses Tulongfeng to generate exploit code or vulnerability analysis at comparable capability levels, circumventing the intended effect of U.S. export controls.

**Scenario 3 — Supply chain substitution.** A procurement team selects Fugu to avoid export control compliance overhead. The model is integrated into a CI/CD pipeline without equivalent safety evaluation, introducing an unaudited code generation capability into a critical software supply chain.

## Defender Checklist

- [ ] Audit all AI model procurement for non-U.S. frontier models entering your environment and require equivalent safety documentation to U.S.-sourced models
- [ ] For any agentic deployment using multi-model orchestration, map all API boundaries and apply prompt injection controls at each handoff
- [ ] Treat export-control status as a procurement signal, not a security signal — absence of controls ≠ absence of risk
- [ ] Engage threat intelligence on Tulongfeng's capability profile as it relates to offensive cyber use cases in your sector
- [ ] Establish a model onboarding policy requiring red-team results, training data disclosure, and alignment methodology documentation before production deployment

## References

- [TechCrunch: Asian AI startups launch Mythos-like models as Anthropic's export ban drags on](https://techcrunch.com/2026/06/27/asian-ai-startups-launch-mythos-like-models-as-anthropics-export-ban-drags-on/)
