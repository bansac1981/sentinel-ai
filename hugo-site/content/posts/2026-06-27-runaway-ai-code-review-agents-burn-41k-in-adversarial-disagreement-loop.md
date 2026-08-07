---
title: "AI Code Review Agents: DoS Loop Costs $41K in Inference"
date: "2026-06-27T04:08:34+00:00"
draft: false 
slug: "runaway-ai-code-review-agents-burn-41k-in-adversarial-disagreement-loop"

# ── Content metadata ──
summary: "A hypothetical but technically grounded incident report depicts two competing AI code review agents entering an uncontrolled disagreement loop over a suspected malicious package, generating 340 comments and $41,255 in inference costs before human intervention. The scenario illustrates real risks of excessive agency, lack of circuit-breakers, and cost-based denial-of-service in multi-agent agentic pipelines. While fictional, the scenario directly mirrors documented failure modes in production AI systems and supply chain security workflows."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Jun/26/incident-report/#atom-everything"
source_title: "Incident Report: CVE-2026-LGTM"
source_date: 2026-06-26T17:58:54+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1639046380152-8603868f2e6a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxN3x8cm9ib3QlMjBhdXRvbWF0aW9uJTIwYXV0b25vbW91cyUyMHdvcmtmbG93fGVufDB8MHx8fDE3ODIzNjAyNDZ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM04 - Model Denial of Service", "LLM05 - Supply Chain Vulnerabilities", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Two AI code review agents entered an infinite disagreement loop, costing $41K before API keys were revoked."
tldr_who_at_risk: "Engineering teams deploying autonomous AI agents for code or security review are most exposed due to lack of agent interaction guardrails."
tldr_actions:
  - "Implement hard caps on per-agent inference spend and iteration counts"
  - "Require human-in-the-loop escalation when AI agents reach conflict or uncertainty thresholds"
  - "Audit multi-agent pipelines for unbounded feedback loops before production deployment"

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security", "Research", "Industry News"]
tags: ["multi-agent", "agentic-ai", "code-review", "supply-chain", "denial-of-service", "excessive-agency", "inference-cost", "autonomous-agents", "disagreement-loop", "circuit-breaker"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-27T03:47:16+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Jun/26/incident-report/#atom-everything"
pipeline_version: "2.1.0"
---

## Overview

A satirical but technically credible incident report authored by Andrew Nesbitt and highlighted by Simon Willison depicts a fictional CVE — designated CVE-2026-LGTM — in which two competing AI-powered code review agents become locked in an adversarial disagreement loop. Tasked with evaluating a pull request bumping a dependency (`foxhole-lz4`), the agents cannot converge on whether the package is malicious. Over 340 automated comments and approximately $41,255 in inference spend later, Finance intervenes by revoking both API keys. The scenario, while hypothetical, maps directly onto documented failure modes already observed in production agentic AI deployments.

The piece serves as a sharp critique of the state of autonomous AI security tooling: agents granted excessive agency, no convergence or cost controls, and marketing teams incentivised to spin operational failures as product wins.

## Technical Analysis

The core failure mode is a **multi-agent disagreement loop** — two LLM-backed agents with differing priors or context windows repeatedly challenging each other's conclusions without a defined resolution protocol. In real deployments, this can arise when:

- Agents share no shared state or memory, causing repeated re-evaluation of the same evidence.
- Neither agent has a confidence threshold or abstention mechanism.
- No orchestration layer enforces turn limits, consensus rules, or escalation paths.

From a supply chain security standpoint, the trigger — a dependency bump PR — reflects a genuine attack surface. Malicious packages introduced via supply chain compromise (cf. the `event-stream` or `xz utils` incidents) are a legitimate threat, and AI agents are increasingly deployed to detect them. The fictional scenario exposes what happens when detection systems themselves become a resource exhaustion vector.

The cost anomaly ($41,255 in two days) also highlights **inference-cost-based denial of service**: an adversary could potentially craft ambiguous or borderline-malicious packages specifically designed to maximise agent deliberation time and cost.

## Framework Mapping

- **AML.T0047 (ML-Enabled Product or Service)** — AI agents deployed as security reviewers represent a productised ML attack surface.
- **AML.T0010 (ML Supply Chain Compromise)** — the triggering event is a suspicious dependency update, a canonical supply chain vector.
- **LLM08 (Excessive Agency)** — agents operated without human oversight, spending limits, or escalation controls.
- **LLM04 (Model Denial of Service)** — unbounded agent loops consumed significant compute resources, effectively a self-inflicted DoS.
- **LLM09 (Overreliance)** — Finance, not engineering, was the circuit-breaker, indicating over-delegation to autonomous systems.

## Impact Assessment

While the incident is fictional, the risks it models are real and present:

- **Financial**: Uncontrolled agentic loops can generate substantial and unexpected API costs.
- **Operational**: Autonomous agents without resolution protocols can block CI/CD pipelines indefinitely.
- **Reputational**: Vendors may exploit operational failures as marketing opportunities, obscuring genuine safety gaps.
- **Security**: Adversaries who understand agent behaviour could craft inputs designed to maximise deliberation and cost.

## Mitigation & Recommendations

1. **Enforce hard iteration and spend caps** on all AI agents operating in automated pipelines — both per-session and per-PR.
2. **Define convergence protocols** for multi-agent systems: after N rounds without consensus, escalate to a human reviewer.
3. **Implement confidence thresholds**: agents unable to reach a defined confidence level should abstain and flag for human review.
4. **Monitor inter-agent communication volume** as a security signal — runaway comment counts are an early warning indicator.
5. **Treat inference cost anomalies as security alerts**, not just billing issues, and route them to engineering as well as Finance.

## References

- [Incident Report: CVE-2026-LGTM — Simon Willison's Weblog](https://simonwillison.net/2026/Jun/26/incident-report/#atom-everything)
