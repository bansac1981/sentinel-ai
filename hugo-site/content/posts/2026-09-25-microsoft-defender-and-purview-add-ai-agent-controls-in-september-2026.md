---
title: "Microsoft Defender and Purview Add AI Agent Controls in September 2026"
date: "2026-09-25T18:28:20+00:00"
draft: false 
slug: "microsoft-defender-and-purview-add-ai-agent-controls-in-september-2026"

# ── Content metadata ──
summary: "Microsoft's September 2026 security update delivers network-layer data loss prevention for agentic AI traffic, AI-generated email detonation summaries in Security Copilot, and enterprise-scale labelling automation in Microsoft Purview. These capabilities close a material gap for defenders by extending Zero Trust policy enforcement to on-behalf-of (OBO) agent actions \u2014 an emerging blind spot as autonomous agents operate across employee devices and cloud platforms. Residual gaps remain around coverage breadth for third-party agent frameworks, cross-platform policy portability, and the organisational maturity required to define reliable classification policies before enforcement becomes effective."
source: "Microsoft Security Blog"
source_url: "https://www.microsoft.com/en-us/security/blog/2026/09/24/whats-new-in-microsoft-security-september-2026"
source_title: "\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200bWhat\u2019s new in Microsoft Security: September 2026\u200b\u200b"
source_date: 2026-09-24T16:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1662947036583-d67dd8055edf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxNaWNyb3NvZnQlMjBjaGVzcyUyMHBpZWNlJTIwc3RyYXRlZ3klMjBib2FyZCUyMGdhbWV8ZW58MHwwfHx8MTc5MDMzMjEyNHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 6.8
adoption_velocity: "MODERATE"
capability_category: "platform-integration"
attack_vectors_introduced: ["Network-layer DLP enforcement for agentic OBO traffic prevents sensitive data exfiltration to unsanctioned AI destinations", "AI-generated email detonation summaries reduce SOC triage time for phishing and malicious URL investigations", "Context-aware classification policies applied at the Entra Global Secure Access layer close the gap between human and agent data-handling governance", "Real-time discovery and blocking of sensitive file and text transfers by both human users and autonomous agents"]

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0057 - LLM Data Leakage", "AML.T0080 - AI Agent Context Poisoning", "AML.T0084 - Discover AI Agent Configuration", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Microsoft ships network-layer DLP for AI agent traffic, AI email detonation summaries, and Purview auto-labelling at enterprise scale."
tldr_who_at_risk: "SOC teams and data security owners who need visibility and policy enforcement over autonomous AI agents operating on behalf of employees gain the most immediate benefit."
tldr_actions: ["Enable the Purview + Entra Global Secure Access integration and define classification policies for sensitive data categories before enabling blocking mode", "Onboard Security Copilot users to the email detonation summary feature and measure reduction in mean time to investigate phishing incidents", "Audit existing OBO agent configurations to identify which agents handle sensitive data and validate that network-layer policies cover those traffic paths"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News"]
tags: ["microsoft-defender", "microsoft-purview", "microsoft-entra", "security-copilot", "agentic-ai", "data-loss-prevention", "zero-trust", "agent-governance", "network-layer-dlp", "obo-traffic", "email-detonation", "soc-tooling", "september-2026"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-25T10:28:44+00:00"
feed_source: "microsoft_security"
original_url: "https://www.microsoft.com/en-us/security/blog/2026/09/24/whats-new-in-microsoft-security-september-2026"
pipeline_version: "2.1.0"
---

## Defender Impact

The expansion of Microsoft Purview data loss prevention to cover on-behalf-of (OBO) agentic traffic closes a governance blind spot that has widened as autonomous AI agents proliferate across enterprise environments. For the first time, defenders can apply consistent, context-aware data classification and blocking at the network layer regardless of whether the actor is a human employee or an AI agent acting on their behalf.

## Capability Overview

Microsoft's September 2026 update delivers three discrete capabilities across the Defender, Purview, and Entra portfolio.

**Network-layer DLP for agentic traffic (Generally Available):** Microsoft Purview classification and policy enforcement is now applied by Microsoft Entra Global Secure Access at the network layer. This covers both human-initiated data transfers and OBO agentic traffic — the category of actions performed by AI agents acting on behalf of a user, such as uploading files or querying external services. When a policy detects a sensitive file or text string in transit to a risky destination (for example, a consumer AI application or unsanctioned SaaS tool), the transfer is blocked before data egress occurs. This is a meaningful architectural step: policy enforcement moves from the application layer to the network layer, reducing dependence on per-application DLP agent coverage.

**AI-generated email detonation summaries in Security Copilot:** SOC analysts investigating suspicious emails can now receive an AI-generated narrative summary of URL and file sandboxing (detonation) results, correlated with contextual signals. This reduces the manual effort of correlating raw sandbox telemetry with threat intelligence, compressing investigation workflows. The feature is available to organisations running both Microsoft Defender and Microsoft Security Copilot.

**Enterprise-scale auto-labelling in Microsoft Purview:** The update includes improvements to labelling automation designed to reduce administrative overhead at scale. This supports the classification accuracy that the network-layer DLP enforcement depends on — accurate labels are a prerequisite for reliable policy decisions.

## Defensive Advances

- **Agentic traffic is now a governed surface.** Defenders can discover, classify, and block sensitive data movement regardless of whether the initiating actor is human or an autonomous agent. This is the first generally available Microsoft capability to explicitly address OBO agent data flows at the network layer.
- **Faster phishing triage.** Email detonation summaries reduce the cognitive load on tier-1 and tier-2 analysts by surfacing correlated sandbox evidence in plain language, accelerating mean-time-to-respond for email-borne threats.
- **Consistent enforcement posture across human and agent actions.** A single policy framework now governs both interaction types, reducing the risk of governance gaps where agents are inadvertently exempt from controls designed for human behaviour.

## Residual Gaps

- **Third-party agent frameworks.** The OBO enforcement model is currently scoped to agents operating within the Microsoft ecosystem and traffic routed through Entra Global Secure Access. Organisations running autonomous agents on non-Microsoft orchestration frameworks or with direct internet egress paths will not automatically inherit these controls. Separate tooling or network policy will be required for those surfaces.
- **Classification policy maturity is a prerequisite.** Network-layer blocking is only as reliable as the underlying Purview classification policies. Organisations with immature or incomplete data classification estates risk both false positives (blocking legitimate agent activity) and false negatives (misclassified sensitive data passing undetected). The auto-labelling improvements help, but this remains an organisational readiness question.
- **Detonation summaries require dual-product licensing.** The email investigation feature requires both Microsoft Defender and Security Copilot entitlements. Organisations without Security Copilot licensing cannot access this capability, limiting adoption breadth in the near term.

## Framework Mapping

| Framework | Technique | How this capability helps |
|---|---|---|
| MITRE ATLAS | AML.T0086 — Exfiltration via AI Agent Tool Invocation | Network-layer blocking prevents sensitive data reaching external destinations via agent-invoked tooling |
| MITRE ATLAS | AML.T0057 — LLM Data Leakage | Classification and policy enforcement reduces the risk of sensitive data being transmitted through or to LLM services |
| MITRE ATLAS | AML.T0080 — AI Agent Context Poisoning | Agent governance controls reduce the blast radius of compromised agent configurations |
| OWASP LLM06 | Sensitive Information Disclosure | DLP enforcement at the network layer directly addresses this risk for agent-driven data flows |
| OWASP LLM08 | Excessive Agency | Scoping what agents can send externally limits the potential damage from agents operating beyond intended boundaries |

## Deployment Considerations

Organisations should sequence adoption in three stages. First, complete or accelerate Purview data classification work — the network-layer enforcement depends on accurate labels. Second, deploy Entra Global Secure Access in audit (report-only) mode to baseline agent and human traffic patterns before enabling blocking. Third, enable blocking policies incrementally, starting with highest-sensitivity classifications, to avoid disrupting legitimate agentic workflows.

Teams should also inventory which AI agents in their environment generate OBO traffic and verify that those traffic paths route through Entra Global Secure Access rather than direct egress points.

## Defender Checklist

- [ ] Audit current Purview classification coverage and close gaps before enabling network-layer enforcement
- [ ] Deploy Entra Global Secure Access in audit mode and review OBO agent traffic baselines for at least two weeks before enabling blocking
- [ ] Enable blocking policies for the highest-sensitivity classifications first; expand iteratively
- [ ] Identify all AI agents generating OBO traffic and confirm they route through monitored network paths
- [ ] Onboard eligible analysts to the Security Copilot email detonation summary feature and track triage time delta
- [ ] Review auto-labelling configurations in Purview to reduce manual labelling overhead and improve policy accuracy

## References

- [What's new in Microsoft Security: September 2026 — Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/09/24/whats-new-in-microsoft-security-september-2026)
