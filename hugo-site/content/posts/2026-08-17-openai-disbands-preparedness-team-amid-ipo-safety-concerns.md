---
title: "OpenAI Disbands Preparedness Team Amid IPO Safety Concerns"
date: "2026-08-17T04:19:07+00:00"
draft: false 
slug: "openai-disbands-preparedness-team-amid-ipo-safety-concerns"

# ── Content metadata ──
summary: "OpenAI has disbanded its dedicated preparedness team, which was responsible for assessing catastrophic model risks and developing mitigations, redistributing its functions across domain-specific teams for areas like bio and cyber. This follows the dissolution of its AGI readiness and superalignment teams, and the departure of multiple senior safety and ethics leaders. Critics warn the pattern signals a systematic de-prioritisation of frontier AI safety oversight in favour of commercial growth ahead of a major IPO."
source: "The Verge AI"
source_url: "https://www.theverge.com/ai-artificial-intelligence/980817/openai-disbands-preparedness-team"
source_title: "OpenAI reportedly disbanded its preparedness team"
source_date: 2026-08-16T21:32:56+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1675557009285-b55f562641b9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOXx8T3BlbmFpJTIwY29udmVyc2F0aW9uJTIwc3BlZWNoJTIwYnViYmxlcyUyMGFic3RyYWN0fGVufDB8MHx8fDE3ODY5Mzk5ODR8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0031 - Erode AI Model Integrity", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "OpenAI shut down its preparedness team, scattering AI risk assessment across existing domain teams."
tldr_who_at_risk: "Downstream users and organisations relying on OpenAI models face increased risk as centralised safety red-teaming and catastrophic risk evaluation is fragmented."
tldr_actions: ["Audit your AI vendor's safety governance structure before deepening platform dependencies", "Implement independent red-teaming for frontier model integrations you cannot control internally", "Monitor OpenAI policy and model changelog disclosures for reduced safety signalling"]

# ── Taxonomies ──
categories: ["Regulatory", "Industry News", "Agentic AI"]
tags: ["openai", "ai-safety", "preparedness-team", "frontier-models", "ipo", "governance", "superalignment", "recursive-self-improvement", "safety-dissolution", "organisational-risk"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: []

# ── Pipeline metadata ──
fetched_at: "2026-08-17T04:13:04+00:00"
feed_source: "theverge_ai"
original_url: "https://www.theverge.com/ai-artificial-intelligence/980817/openai-disbands-preparedness-team"
pipeline_version: "2.1.0"
---

## Overview

OpenAI has disbanded its preparedness team — the internal group responsible for evaluating whether frontier models posed serious catastrophic risks and designing mitigations — effective end of July 2026. According to the Financial Times, responsibility has been fragmented and redistributed into existing domain-specific teams covering areas such as bio and cyber risk. The move comes as OpenAI undergoes significant organisational restructuring ahead of what is expected to be a landmark IPO.

This is not an isolated change. OpenAI has progressively dismantled its safety-focused infrastructure over the past two years, dissolving both its AGI readiness team and its superalignment team. Senior figures including ethics lead Chloé Bakalar, Chief Futurist Josh Achiam, and head of safety Johannes Heidecke have all departed recently. Former OpenAI VP Jan Leike, who resigned in 2024, told the FT that the company is prioritising "shiny products" over safety research.

## Technical Analysis

The preparedness team's core mandate was to conduct pre-deployment risk assessments — essentially structured red-teaming and capability evaluations designed to catch emergent dangerous behaviours before models reached production. These included evaluations for CBRN uplift risk, autonomous self-replication, and cyberoffensive capability. Fragmenting this function into siloed domain teams introduces coordination gaps: a cross-cutting risk that spans bio and cyber domains, for example, may fall between organisational boundaries and go unevaluated.

Dylan Scandinaro, who led the preparedness team after being recruited from Anthropic in February 2026, will reportedly shift focus to the implications of "recursive self-improving" AI — a narrow but high-stakes sub-area. The broader systematic preparedness function, however, has no clear successor structure publicly announced.

## Framework Mapping

**AML.T0031 – Erode AI Model Integrity**: The removal of a dedicated oversight body reduces the systematic controls against integrity degradation in deployed frontier models — both from emergent capability drift and insufficient pre-deployment red-teaming.

**AML.T0047 – AI-Enabled Product or Service**: OpenAI's commercial API and consumer products are the primary exposure surface. As safety oversight weakens, the risk profile of these services increases for any downstream integrator.

**LLM08 – Excessive Agency**: Reduced preparedness oversight increases the likelihood that models with excessive autonomous capability reach deployment without adequate constraint evaluation.

**LLM09 – Overreliance**: Enterprise and government customers that treat OpenAI's internal safety processes as a compliance proxy face increased exposure as those processes are weakened.

## Impact Assessment

The direct impact falls on organisations that rely on OpenAI's internal safety posture as part of their own risk management. Enterprises integrating GPT-class models into agentic workflows, healthcare systems, or critical infrastructure tooling should treat this as a material governance change. Regulators in the EU under the AI Act and UK AI Safety Institute are likely to scrutinise this reorganisation. The indirect risk is systemic: if the industry's most prominent lab normalises deprioritising safety oversight pre-IPO, it sets a damaging precedent across the sector.

## Mitigation & Recommendations

- **Independent evaluation**: Do not rely solely on OpenAI's internal model cards or safety disclosures. Commission third-party red-teaming for frontier model integrations.
- **Vendor due diligence**: Update AI vendor risk assessments to reflect changes in OpenAI's safety governance structure.
- **Capability monitoring**: Track public model capability benchmarks and emergent behaviour reports from independent researchers.
- **Regulatory engagement**: Follow EU AI Act conformity assessment requirements and engage with national AI Safety Institutes for guidance on frontier model procurement.

## References

- [OpenAI reportedly disbanded its preparedness team — The Verge](https://www.theverge.com/ai-artificial-intelligence/980817/openai-disbands-preparedness-team)
