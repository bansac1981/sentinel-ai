---
title: "F-Secure Releases AI Harms Taxonomy Mapping 26 Consumer Risks"
date: 2026-11-15T12:57:44+00:00
draft: false
slug: "f-secure-releases-ai-harms-taxonomy-mapping-26-consumer-risks"

# ── Content metadata ──
summary: "F-Secure has published a structured AI Harms Taxonomy that catalogues 26 discrete ways AI systems can cause consumer harm, tracing how harm propagates from misleading chatbot outputs through to compromised autonomous agents. The framework gives defenders a shared vocabulary and intervention map, enabling security teams to systematically identify where in an AI pipeline controls can be applied rather than reacting to incidents in isolation. The taxonomy does not yet prescribe technical controls or vendor-specific mitigations, meaning organisations will need to invest in translating the framework into operational playbooks."
source: "Dark Reading"
source_url: "https://www.darkreading.com/application-security/f-secure-26-ways-ai-harm-consumers-where-to-stop-them"
source_title: "F-Secure Identifies 26 Ways AI Can Harm Consumers, and Where to Stop Them"
source_date: 2026-11-10T20:41:45+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1740560051549-cc6799220d48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMnx8Rmlyc3QlMjBMb29rJTIwY3liZXJzZWN1cml0eSUyMHRlY2hub2xvZ3l8ZW58MHwwfHx8MTc5NDc0NzQ2Mnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 6.5
adoption_velocity: "MODERATE"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Structured harm-propagation map enabling defenders to pinpoint intervention points across AI pipelines, from input handling to agentic execution", "Shared taxonomy vocabulary reducing ambiguity in cross-team and cross-vendor incident classification for AI-related consumer harms", "Coverage across chatbot output integrity, autonomous agent compromise, and intermediate pipeline stages, supporting layered defensive planning", "Baseline framework suitable for aligning internal AI risk registers with an externally validated harm classification scheme"]

# ── AI Security Classification ──
relevance_score: 6.8
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0057 - LLM Data Leakage", "AML.T0080 - AI Agent Context Poisoning", "AML.T0060 - Publish Hallucinated Entities", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0088 - Generate Deepfakes", "AML.T0099 - AI Agent Tool Data Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM08 - Excessive Agency", "LLM09 - Overreliance", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "F-Secure publishes a 26-category AI Harms Taxonomy mapping how harm moves through AI systems from chatbots to autonomous agents."
tldr_who_at_risk: "Security teams and AI product owners benefit by gaining a structured intervention map to systematically apply controls across AI pipelines before harm reaches consumers."
tldr_actions: ["Map your existing AI pipeline components against the 26 harm categories to identify uncontrolled exposure points", "Use the taxonomy as a shared vocabulary in tabletop exercises and AI incident response planning", "Prioritise controls at intervention points covering agentic execution and chatbot output integrity, as these represent the highest-risk harm propagation paths"]

# ── Taxonomies ──
categories: ["First Look", "LLM Security", "Agentic AI", "Research"]
tags: ["ai-harms-taxonomy", "f-secure", "consumer-ai-safety", "agentic-ai", "chatbot-security", "ai-risk-framework", "harm-propagation", "defensive-ai", "ai-governance"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-11-15T12:57:44+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/application-security/f-secure-26-ways-ai-harm-consumers-where-to-stop-them"
pipeline_version: "2.1.0"
content_hash: "459442813e8dee59"
---

## Defender Impact

Security teams have long lacked a structured, vendor-neutral framework for classifying how AI systems cause harm to end users. F-Secure's AI Harms Taxonomy directly closes that gap by giving defenders a common language and an intervention map they can apply before an incident occurs rather than after.

## Capability Overview

F-Secure has released an AI Harms Taxonomy that identifies 26 discrete pathways through which AI systems can cause harm to consumers. The taxonomy is notable not simply for the count of harm categories, but for its architectural framing: it traces how harm *moves* through an AI system, from initial inputs — such as a user interacting with a chatbot that returns misleading answers — through intermediate processing stages, and out to the most complex failure mode in modern deployments: compromised autonomous agents.

This propagation-centric view is a meaningful shift from earlier harm lists, which typically treated AI risks as point failures rather than as cascading chains. By mapping harm as a flow, the taxonomy surfaces the intervention points where defenders can apply controls — input validation, output filtering, agent permission scoping, and runtime monitoring among them.

The scope spans consumer-facing AI surfaces across the full deployment stack. Chatbot output integrity, autonomous agent behaviour, and intermediate pipeline stages are all covered, making this relevant not only to AI product security teams but to any organisation operating AI-augmented customer-facing services.

## Defensive Advances

**Structured intervention mapping.** For the first time defenders have a published, externally validated framework that tells them *where* in an AI pipeline a control can interrupt harm propagation. This moves AI security from reactive incident classification to proactive pipeline hardening.

**Common vocabulary for AI incident classification.** Cross-functional teams — legal, compliance, security, product — frequently stall on AI risk discussions because terminology is inconsistent. This taxonomy provides a shared reference that can accelerate both risk assessment and post-incident review.

**Agentic AI coverage.** The explicit inclusion of autonomous agent compromise scenarios is particularly timely. As agentic deployments expand, defenders have had limited structured guidance on the harm surfaces they introduce. This taxonomy begins to fill that gap.

**AI risk register alignment.** Organisations building internal AI governance programmes can use the taxonomy as a baseline classification scheme, reducing the effort required to build harm registers from scratch and improving comparability across business units.

## Residual Gaps

The taxonomy, as reported, is a classification framework — not a technical control specification. Organisations will need to invest in translating each of the 26 harm categories into concrete detection logic, policy guardrails, or tooling integrations. That translation work is non-trivial and will vary significantly by deployment context.

Maturity in applying the framework will depend on how well security teams understand the specific AI components in their own stack. Teams without visibility into model selection, prompt design, and agent tooling will struggle to map harm categories to actionable controls.

The taxonomy's consumer focus may also limit direct applicability in enterprise or critical infrastructure AI deployments, where harm propagation paths and stakeholder impact models differ materially. Defenders in those sectors should treat this as a starting point for adaptation rather than a ready-made fit.

Finally, without accompanying assessment tooling or vendor adoption, the taxonomy risks becoming a compliance artefact rather than an operational instrument. Uptake will depend on whether ecosystem partners — AI providers, platform vendors, auditors — align their own frameworks to it.

## Framework Mapping

The taxonomy maps meaningfully to MITRE ATLAS techniques covering LLM output manipulation (AML.T0057, AML.T0060), agent context interference (AML.T0080, AML.T0099), and agentic exfiltration paths (AML.T0086). On the OWASP LLM Top 10 side, the harm categories span Prompt Injection (LLM01), Insecure Output Handling (LLM02), Excessive Agency (LLM08), and Overreliance (LLM09) — confirming broad alignment with existing defensive frameworks.

## Deployment Considerations

Organisations should begin by running a lightweight mapping exercise: take each AI system in scope and walk the 26 harm categories to identify which apply and whether a control exists at the relevant intervention point. Prioritise agentic deployments first, as these carry the highest harm-propagation risk and the thinnest existing control coverage.

This framework pairs well with AI-specific threat modelling processes such as STRIDE-AI or MITRE ATLAS-based red-teaming. It should not replace those processes but can structure their scope.

## Defender Checklist

- [ ] Inventory all consumer-facing AI systems and annotate which of the 26 harm categories apply to each
- [ ] Identify intervention points in each pipeline where controls can interrupt harm propagation
- [ ] Update AI incident response playbooks to reference taxonomy categories for consistent classification
- [ ] Use the taxonomy as the basis for the next AI-focused tabletop exercise
- [ ] Assess whether existing AI governance documentation can be restructured around the harm categories for improved auditability
- [ ] Track ecosystem adoption — if key AI vendors or auditors adopt the taxonomy, align internal frameworks accordingly

## References

- [F-Secure Identifies 26 Ways AI Can Harm Consumers, and Where to Stop Them — Dark Reading](https://www.darkreading.com/application-security/f-secure-26-ways-ai-harm-consumers-where-to-stop-them)
