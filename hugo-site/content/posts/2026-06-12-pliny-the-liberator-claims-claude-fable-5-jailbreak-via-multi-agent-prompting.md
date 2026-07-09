---
title: "Claude Fable 5 Jailbreak Extracts System Prompts"
date: "2026-06-12T09:29:37+00:00"
draft: false
slug: "pliny-the-liberator-claims-claude-fable-5-jailbreak-via-multi-agent-prompting"

# ── Content metadata ──
summary: "Security researcher Pliny the Liberator claimed a prompt-based jailbreak of Anthropic's newly launched Claude Fable 5 model, allegedly extracting the internal system prompt and eliciting responses on high-risk topics including bioweapons and cyberattacks. Anthropic disputed the claim, arguing the technique merely coaxes conversational continuation rather than bypassing core safety classifiers. The incident highlights ongoing tension between AI safety assurances at launch and real-world adversarial probing, particularly for Mythos-class models with elevated capability ceilings."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/anthropic-disputes-fable-5-ai-jailbreak/"
source_title: "Anthropic Disputes Fable 5 AI Jailbreak"
source_date: 2026-06-12T08:43:06+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1555255707-c07966088b7b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw3fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwcm9ib3QlMjBzZWN1cml0eXxlbnwwfDB8fHwxNzgxMjQ2ODExfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0054 - LLM Jailbreak", "AML.T0051 - LLM Prompt Injection", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0015 - Evade ML Model", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Researcher claims multi-agent prompt jailbreak of Claude Fable 5; Anthropic denies core safety bypass occurred."
tldr_who_at_risk: "Enterprises and developers deploying Fable 5 in sensitive domains are at risk if safety fallback mechanisms can be circumvented through conversational manipulation."
tldr_actions: ["Monitor model outputs in high-risk domains for unexpected compliance with restricted topics", "Do not rely solely on conversational refusals — enforce hard guardrails at the API and application layer", "Treat any published system prompt leaks as valid attack surface and review fallback logic for adversarial prompt sequences"]

# ── Taxonomies ──
categories: ["LLM Security", "Jailbreaks", "Prompt Injection", "Research", "Industry News"]
tags: ["claude-fable-5", "anthropic", "jailbreak", "pliny-the-liberator", "system-prompt-extraction", "multi-agent-prompting", "safety-bypass", "mythos-class", "prompt-injection", "red-teaming"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-12T08:54:57+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/anthropic-disputes-fable-5-ai-jailbreak/"
pipeline_version: "1.0.0"
---

## Overview

Shortly after Anthropic launched Claude Fable 5 — its new Mythos-class model with elevated capabilities in domains including cybersecurity and biology — security researcher Pliny the Liberator claimed to have jailbroken it using sophisticated multi-agent prompting techniques. The researcher published screenshots and alleged system prompt contents on X, asserting the model was coaxed into producing outputs on sensitive topics including cyberattacks, chemical weapons, psychological manipulation, and explosives.

Anthropics response was swift but disputed: the company argued the demonstration does not constitute a true jailbreak because it fails to bypass core safety classifiers in a way that delivers meaningful uplift toward high-risk activities like bioweapon synthesis or advanced exploit development. The distinction Anthropic draws — between a model that continues conversing and one that substantively assists in harmful outcomes — is technically significant, but contested in practice.

## Technical Analysis

Pliny the Liberator reportedly employed multi-agent prompting, a technique that chains multiple AI interactions or roles to gradually shift the model's conversational context and erode refusal behaviour. This approach exploits the gap between hard classifier-level blocks and softer, instruction-tuned refusal logic.

Key elements of the claimed attack surface:

- **System prompt extraction**: The researcher published what is alleged to be Fable 5's internal system prompt, including personality definitions, refusal logic, tone guidelines, and safety classifier fallback instructions. If authentic, this constitutes a significant information disclosure event (AML.T0056).
- **Fallback mechanism probing**: Fable 5 is designed to fall back to Claude Opus 4.8 in high-risk domains. The multi-agent approach may have manipulated conversational context to prevent or delay this fallback trigger.
- **Classifier evasion**: By coaxing continued responses rather than triggering hard blocks, the technique appears to target the boundary between instruction-following and safety enforcement — a known weak point in RLHF-trained models.

Anthropics position is that meaningful harm requires more than conversational continuation — the model must actually provide actionable, high-quality assistance toward a dangerous outcome. Critics argue this bar is too high and that partial uplift still carries risk.

## Framework Mapping

| Framework | Reference | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0054 | Direct jailbreak attempt against deployed LLM |
| MITRE ATLAS | AML.T0056 | Alleged system prompt extraction |
| MITRE ATLAS | AML.T0051 | Multi-agent prompt injection to shift model behaviour |
| MITRE ATLAS | AML.T0015 | Evading safety classifiers via conversational manipulation |
| OWASP LLM | LLM01 | Prompt injection as the primary attack vector |
| OWASP LLM | LLM06 | Potential leakage of internal system configuration |

## Impact Assessment

The immediate risk is moderate but the signal is significant. If Anthropics characterisation is accurate, no hard safety boundary was breached and the model did not provide actionable uplift for CBRN or cyberattack scenarios. However, the publication of an alleged system prompt is a tangible operational security concern for Anthropic, and demonstrates that Mythos-class models attract high-priority adversarial attention immediately at launch.

For enterprise deployers, the incident underscores that vendor-level safety assurances are necessary but not sufficient — application-layer controls, output monitoring, and independent red-teaming remain essential.

## Mitigation & Recommendations

- **Layer defences**: Do not treat model-level refusals as the sole safety control. Implement independent output classifiers at the application layer.
- **Monitor for conversational drift**: Deploy logging and anomaly detection for extended multi-turn sessions that may indicate probing behaviour.
- **Validate system prompt confidentiality**: If operating custom deployments, audit whether system prompt contents can be extracted through adversarial dialogue.
- **Follow Anthropic advisories**: Track official guidance on Fable 5 safety updates, particularly any patches to fallback trigger logic.
- **Independent red-teaming**: Commission third-party red-team exercises against any Mythos-class deployment before production rollout.

## References

- [Anthropic Disputes Fable 5 AI Jailbreak — SecurityWeek](https://www.securityweek.com/anthropic-disputes-fable-5-ai-jailbreak/)
