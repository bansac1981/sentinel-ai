---
title: "NVIDIA Launches Nemotron 3.5 Super VL and Bolt Agent Models"
date: "2026-10-20T13:08:51+00:00"
draft: false 
slug: "nvidia-launches-nemotron-3-5-super-vl-and-bolt-agent-models"

# ── Content metadata ──
summary: "NVIDIA has released Nemotron 3.5 Super VL (120B parameters) for enterprise agentic workloads and two lightweight Bolt models for local PC deployment, all as open-weight models that organisations can post-train and self-host. For defenders, the shift to on-premises, self-hosted agentic models closes a meaningful data-sovereignty gap \u2014 sensitive workflows involving financial, medical, and security data no longer require routing through third-party frontier APIs. Residual gaps remain around enterprise readiness for securing agentic pipelines, validating post-trained model behaviour, and governing always-on local agents at endpoint scale."
source: "TechCrunch AI"
source_url: "https://techcrunch.com/2026/10/19/nvidia-launches-new-open-models-to-run-agents-in-the-enterprise-and-on-pcs"
source_title: "Nvidia launches new open models to run agents in the enterprise and on PCs"
source_date: 2026-10-19T15:37:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1716967318503-05b7064afa41?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw1fHxOdmlkaWElMjBjaGVzcyUyMHBpZWNlJTIwc3RyYXRlZ3klMjBib2FyZCUyMGdhbWV8ZW58MHwwfHx8MTc5MjQ5MTYxOXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 5.5
adoption_velocity: "MODERATE"
capability_category: "model-release"
attack_vectors_introduced: ["On-premises deployment of capable agentic models removes the need to send sensitive data to third-party frontier APIs, reducing external data exposure surface", "Open-weight availability enables defenders to audit, red-team, and post-train models on security-specific tasks including security attack resilience benchmarks", "Edge/local deployment on AI PCs enables air-gapped or network-restricted agentic workflows for high-sensitivity environments", "Organisations gain full model ownership, enabling reproducible security testing and supply chain verification of model artefacts", "CrowdStrike adoption signals early validation for security-adjacent agentic use cases on this model family"]

# ── AI Security Classification ──
relevance_score: 5.8
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0044 - Full AI Model Access", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM03 - Training Data Poisoning"]

# ── TL;DR ──
tldr_what: "NVIDIA released Nemotron 3.5 Super VL (120B) and Bolt models as open-weight, self-hostable agents for enterprise and AI PCs."
tldr_who_at_risk: "Security and IT teams in regulated industries benefit most \u2014 self-hosting capable agentic models closes the data-sovereignty gap that blocked adoption of frontier API-based agents."
tldr_actions: ["Evaluate Nemotron 3.5 Super VL for on-premises agentic workflows handling sensitive financial, medical, or security data", "Establish model provenance and integrity verification processes before deploying open-weight models in production pipelines", "Define agent governance policies — scope, tool permissions, and monitoring — before deploying always-on Bolt agents at endpoint scale"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "Industry News", "LLM Security", "Supply Chain"]
tags: ["nvidia", "nemotron", "open-weight-models", "agentic-ai", "enterprise-agents", "edge-computing", "on-premises-ai", "local-llm", "ai-pcs", "model-deployment", "self-hosted-ai", "bolt-models", "data-sovereignty"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-10-20T10:20:20+00:00"
feed_source: "techcrunch_ai"
original_url: "https://techcrunch.com/2026/10/19/nvidia-launches-new-open-models-to-run-agents-in-the-enterprise-and-on-pcs"
pipeline_version: "2.1.0"
---

## Defender Impact

NVIDIA's release of open-weight agentic models that organisations can self-host closes a meaningful data-sovereignty gap: security teams and regulated enterprises can now run capable, instruction-following agentic workloads without routing sensitive data through third-party frontier AI APIs. For environments handling financial records, medical claims, or security telemetry, this matters.

## Capability Overview

NVIDIA has released three new open-weight models targeting different tiers of the enterprise deployment stack. The flagship **Nemotron 3.5 Super VL** is a 120-billion-parameter multimodal model optimised for agentic tasks — document intelligence, financial accounting, scientific workflows, medical insurance processing, and security attack resilience. NVIDIA positions it as delivering accuracy comparable to its larger Nemotron Ultra predecessor while being more deployable at enterprise scale. Benchmark claims place it ahead of Anthropic Opus 5, OpenAI GPT 6.1 Sol, and others on post-trained agentic tasks, with adopters including CrowdStrike, EY, Ramp, and Salesforce cited as validators.

At the lighter end, two **Bolt models** are designed to run locally on consumer and prosumer AI PCs equipped with NVIDIA's RTX Spark chip, as well as DGX Spark workstations. These target always-on personal agent use cases for knowledge workers and developers — shipped through OEM partners including Microsoft and Dell.

Critically, all models are open-weight: organisations can post-train on proprietary data, deploy on their own infrastructure, and own the resulting artefacts. This is a deliberate strategic positioning by NVIDIA against closed frontier labs, leaning into enterprise demand for model sovereignty.

## Defensive Advances

**Data sovereignty for sensitive agentic workloads.** Security teams can now run document-intelligence and workflow-automation agents over sensitive data without external API calls. This directly reduces the risk of inadvertent sensitive information disclosure to third-party model providers.

**Auditability and red-teaming access.** Open weights mean security teams can inspect, probe, and red-team the model directly — testing for prompt injection susceptibility, jailbreak vectors, and unintended tool invocation behaviours before production deployment. This is categorically unavailable with closed frontier APIs.

**Post-training on security-specific tasks.** The Super VL's post-training capability allows organisations to fine-tune on internal threat intelligence, alert taxonomies, or incident response playbooks — creating security-domain-specialised agents with verifiable, reproducible behaviour.

**CrowdStrike validation signal.** The inclusion of CrowdStrike as a named adopter provides an early indicator that the model family has undergone at least some security-adjacent evaluation, lowering the initial due-diligence burden for other security-oriented teams.

**Air-gapped and network-restricted deployment.** The Bolt models' local PC deployment path enables agentic capability in environments where network egress is restricted or where latency makes cloud inference impractical — a persistent barrier in OT-adjacent and defence environments.

## Residual Gaps

**Agent governance maturity is a prerequisite, not a given.** Open-weight deployment shifts the security burden fully to the deploying organisation. Teams without established agent governance frameworks — covering tool permissions, action scoping, and runtime monitoring — will expose themselves to excessive agency risks that the model itself cannot mitigate.

**Post-training introduces new integrity risks.** The ability to fine-tune on internal data is a genuine advance, but it requires mature MLOps practices: dataset curation, training pipeline integrity, and behavioural regression testing. Organisations without these practices may inadvertently introduce biased or degraded behaviour.

**Local endpoint agents are a new governance frontier.** Always-on Bolt agents running on employee PCs with access to personal health, financial, and family data represent a governance challenge that most enterprise security programmes have not yet operationalised. Endpoint agent policy frameworks are nascent.

**Benchmark claims require independent validation.** Performance comparisons against frontier models are self-reported and task-specific. Security teams should treat them as directional signals, not deployment decisions, until independent evaluations are available.

## Framework Mapping

- **AML.T0010 (AI Supply Chain Compromise) / LLM05 (Supply Chain Vulnerabilities):** Open-weight distribution via NVIDIA's model hub requires organisations to verify model provenance and integrity hashes before deployment.
- **AML.T0080 (AI Agent Context Poisoning) / LLM08 (Excessive Agency):** Always-on agents with broad tool access require context isolation and least-privilege tool scoping.
- **AML.T0044 (Full AI Model Access) / LLM03 (Training Data Poisoning):** Post-training workflows must include dataset integrity controls and output validation pipelines.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation):** Agents with local file system or API access require egress monitoring regardless of whether the model is locally hosted.

## Deployment Considerations

Organisations should sequence adoption by governance maturity, not hardware availability. Before deploying Super VL in production agentic pipelines: establish tool permission policies, define agent scope boundaries, and instrument agent actions for audit logging. For Bolt endpoint agents, begin with read-only task scopes and expand permissions only after monitoring baselines are established. Treat model provenance verification as a non-negotiable first step — validate checksums and download from NVIDIA's official distribution channel.

## Defender Checklist

- [ ] Verify Nemotron 3.5 Super VL model artefact integrity against NVIDIA's published hashes before deployment
- [ ] Define agent tool permission scope (least-privilege) before any production rollout
- [ ] Instrument all agent tool invocations with audit logging from day one
- [ ] Establish a post-training data curation and integrity review process if fine-tuning is planned
- [ ] Develop an endpoint agent governance policy covering Bolt model deployment on employee hardware
- [ ] Run an internal red-team exercise against the open-weight model before handling sensitive data categories
- [ ] Monitor CrowdStrike and EY published evaluations for independent security benchmark data

## References

- [NVIDIA Launches Nemotron 3.5 Super VL and Bolt Models — TechCrunch](https://techcrunch.com/2026/10/19/nvidia-launches-new-open-models-to-run-agents-in-the-enterprise-and-on-pcs)
