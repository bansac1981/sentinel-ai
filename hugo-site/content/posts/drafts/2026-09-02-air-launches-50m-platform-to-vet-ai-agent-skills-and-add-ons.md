---
title: "AIR Launches $50M Platform to Vet AI Agent Skills and Add-Ons"
date: 2026-09-02T09:52:40+00:00
draft: true
slug: "air-launches-50m-platform-to-vet-ai-agent-skills-and-add-ons"

# ── Content metadata ──
summary: "AIR has emerged from stealth with $50M in funding to deliver a continuous vetting and enforcement platform for the skills, plug-ins, MCP servers, and add-ons that AI agents consume inside enterprise environments. This directly closes the visibility and supply chain governance gap that has left most organisations blind to what third-party components their autonomous agents are loading and executing. Residual maturity questions remain around whitelist completeness, integration depth across heterogeneous agent frameworks, and the operational processes organisations need to act on enforcement signals at scale."
source: "TechCrunch AI"
source_url: "https://techcrunch.com/2026/09/01/air-raises-50m-to-help-companies-vet-the-skills-and-add-ons-ai-agents-use"
source_title: "AIR raises $50M to help companies vet the skills and add-ons AI agents use"
source_date: 2026-09-01T15:45:51+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1667372335936-3dc4ff716017?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxwaXBlbGluZSUyMHdvcmtmbG93JTIwYXV0b21hdGlvbiUyMGFic3RyYWN0fGVufDB8MHx8fDE3ODgzNDI3NjB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 7.5
adoption_velocity: "MODERATE"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Continuous discovery of AI agents running across enterprise environments, including shadow AI deployments using personal or unapproved accounts", "Runtime interception and analysis of agent actions — specifically skill loading and external content fetching — before they execute", "Whitelist-based enforcement that blocks agents from consuming tools or content sources that fail security criteria", "Continuous monitoring of previously approved skills and add-ons for downstream package changes or newly introduced malicious behaviour", "A vetted marketplace that provides a curated, pre-screened catalogue of agent add-ons as an alternative to open discovery"]

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0109 - AI Supply Chain Rug Pull", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0099 - AI Agent Tool Data Poisoning", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0081 - Modify AI Agent Configuration", "AML.T0080 - AI Agent Context Poisoning", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "AIR launches a continuous vetting and runtime enforcement platform for AI agent skills, plug-ins, and MCP servers."
tldr_who_at_risk: "Enterprise security and IT teams deploying autonomous AI agents benefit most, gaining visibility and control over a previously ungoverned software supply chain."
tldr_actions: ["Audit which AI agents are currently active in your environment — including shadow deployments — before any enforcement layer is introduced", "Map all skills, plug-ins, and MCP servers those agents are consuming and cross-reference against a known-good baseline", "Evaluate AIR's whitelist and vetted marketplace as a complement to existing software composition analysis tooling"]

# ── Taxonomies ──
categories: ["First Look", "Supply Chain", "Agentic AI", "LLM Security"]
tags: ["ai-agent-security", "supply-chain", "mcp-servers", "plugin-vetting", "agent-tooling", "shadow-ai", "runtime-enforcement", "whitelist", "agentic-ai", "enterprise-security", "unit-8200", "sequoia", "greenoaks"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "insider"]

# ── Pipeline metadata ──
fetched_at: "2026-09-02T09:52:40+00:00"
feed_source: "techcrunch_ai"
original_url: "https://techcrunch.com/2026/09/01/air-raises-50m-to-help-companies-vet-the-skills-and-add-ons-ai-agents-use"
pipeline_version: "2.1.0"
---

## Defender Impact

AI agents are acquiring a software supply chain — skills, plug-ins, MCP servers, external content sources — and most organisations have no systematic way to vet or govern it. AIR's platform gives defenders their first purpose-built enforcement layer for this surface, bringing the kind of driver-signing discipline the OS world learned in the 2000s to the agentic layer.

## Capability Overview

AIR exits stealth with $50M raised across two seed rounds (Sequoia leading the first at $10M, Greenoaks leading the second at $40M) and a platform built around three interlocking functions.

**Discovery.** The platform finds AI agents running across an enterprise environment — including employees using unapproved tools or personal accounts — giving security teams the asset inventory that governance requires but that has been largely absent for agentic deployments.

**Runtime enforcement.** An enforcement hook intercepts agent actions before they execute: loading a skill, fetching external content, invoking a tool. This is the critical control point. Rather than relying on pre-deployment review alone, AIR operates inline at the moment of action, allowing block decisions to be made dynamically against current threat intelligence.

**Continuous whitelist maintenance.** AIR maintains a whitelist of approved skills and add-ons by monitoring the open ecosystem for changes and malicious behaviour. The key nuance here is post-approval monitoring: a skill that passes initial review can become dangerous if an upstream package it depends on is later tampered with — the same rug-pull dynamic that has plagued npm and PyPI ecosystems for years. AIR's model attempts to catch this drift continuously rather than treating approval as a one-time gate.

The company also operates a vetted marketplace, offering a curated catalogue of agent add-ons as a safer procurement path than open discovery.

Founders Yair Saban and Niv Hoffman frame the gap explicitly through the OS analogy: unsigned driver installation was normalised until kernel-level compromise made it untenable. Skills and plug-ins that load into agent context operate via the same trust mechanism — but without the signing infrastructure the OS world eventually mandated.

## Defensive Advances

- **Agentic asset inventory at enterprise scale.** Security teams can now enumerate agents, their tool dependencies, and shadow deployments that previously existed outside IT visibility entirely.
- **Inline enforcement before tool execution.** Defenders gain a block capability at the moment a skill or external source is invoked — not retrospectively after a compromise has already propagated.
- **Continuous post-approval monitoring.** Previously approved components can be revoked dynamically if upstream changes introduce risk, closing the post-deployment drift gap that static SCA tools miss in this context.
- **Curated procurement path.** The vetted marketplace reduces the discovery burden on individual security teams by externalising initial vetting to a specialist function.

## Residual Gaps

**Whitelist completeness and update latency.** The value of whitelist-based enforcement is directly proportional to the breadth and freshness of what AIR monitors. Novel or private skills not yet in AIR's corpus will create blind spots until coverage matures. Organisations should understand the whitelist update cadence and what happens to agent actions when a verdict is unavailable.

**Framework heterogeneity.** The agentic ecosystem spans dozens of frameworks (LangChain, AutoGen, CrewAI, custom implementations). The depth of AIR's enforcement hook will vary by framework, and organisations running bespoke agent architectures should assess integration fidelity before assuming full coverage.

**Organisational process maturity.** Enforcement signals are only as useful as the SOC workflows that act on them. Organisations without defined runbooks for AI agent incidents will need to build that operational muscle in parallel with deploying the tooling.

**Complementary controls still required.** AIR addresses the supply chain and runtime enforcement layer but does not replace identity controls, network segmentation, or data loss prevention for the systems agents can reach. It should be evaluated as an additive layer, not a wholesale replacement.

## Framework Mapping

- **AML.T0010 / AML.T0109 / AML.T0115** (AI Supply Chain Compromise, Rug Pull, Poisoned Artifacts): AIR's continuous whitelist monitoring and post-approval drift detection directly addresses these supply chain vectors.
- **AML.T0110 / AML.T0099** (AI Agent Tool Poisoning, Tool Data Poisoning): Runtime interception at the point of tool invocation is the primary mitigation surface for these techniques.
- **AML.T0086** (Exfiltration via AI Agent Tool Invocation): Blocking tools that fail security criteria limits the exfiltration paths available through sanctioned tool use.
- **LLM05** (Supply Chain Vulnerabilities): The whitelist and vetted marketplace directly operationalise supply chain governance for the plugin and skill layer.
- **LLM07** (Insecure Plugin Design): Continuous vetting provides compensating controls where plugin vendors have not implemented security-by-design.
- **LLM08** (Excessive Agency): Enforcement blocking agents from interacting with unapproved sources constrains the action space available to over-privileged agents.

## Deployment Considerations

Organisations should sequence adoption starting with discovery — understanding what agents and tools are already active is a prerequisite for meaningful enforcement. Attempting to enforce before completing inventory risks blocking legitimate business workflows and generating alert fatigue.

The vetted marketplace is worth evaluating as a procurement policy adjunct: directing teams to procure agent add-ons from pre-screened sources reduces the vetting burden on internal security functions significantly.

For organisations already running software composition analysis (SCA) pipelines, AIR should be positioned as a complementary agentic-layer control rather than a replacement — the enforcement mechanics differ materially from static dependency scanning.

## Defender Checklist

- [ ] Run AIR's discovery function to establish a complete inventory of agents and their tool dependencies across the enterprise
- [ ] Identify shadow AI deployments and unapproved tool usage before introducing enforcement to avoid surprise blockage of business-critical workflows
- [ ] Define internal policy for which skills and external sources are permissible, then map that policy to AIR's whitelist configuration
- [ ] Establish SOC runbooks for responding to enforcement block events and whitelist-change alerts
- [ ] Evaluate the vetted marketplace as a default procurement path for new agent add-ons
- [ ] Review integration depth for any bespoke agent frameworks in your environment before assuming full enforcement coverage
- [ ] Schedule recurring reviews of the whitelist baseline as the agentic ecosystem evolves

## References

- [AIR raises $50M to help companies vet the skills and add-ons AI agents use — TechCrunch](https://techcrunch.com/2026/09/01/air-raises-50m-to-help-companies-vet-the-skills-and-add-ons-ai-agents-use)
