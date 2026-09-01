---
title: "Almanac (YC S26) Launches Agentic AI with Self-Updating Company Wiki"
date: 2026-09-01T08:52:15+00:00
draft: true
slug: "almanac-yc-s26-launches-agentic-ai-with-self-updating-company-wiki"

# ── Content metadata ──
summary: "Almanac is a persistent AI agent that connects to company tools, maintains a self-updating internal wiki, and executes multi-step work tasks autonomously via its own browser and login sessions. For defenders and security-conscious organisations, it introduces a structured, auditable knowledge graph of internal operations \u2014 every wiki entry links back to its source, providing a traceable record of AI-driven decisions and actions. Residual gaps centre on the maturity of access governance, wiki poisoning safeguards, and the breadth of autonomous action the agent can take before human confirmation is required."
source: "HN AI Security"
source_url: "https://usealmanac.com/"
source_title: "Launch HN: Almanac (YC S26) \u2013 AI that knows your company"
source_date: 2026-08-31T15:34:34+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1681746521838-8ac0d7943262?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMnx8bWVjaGFuaWNhbCUyMGdlYXJzJTIwaW50ZXJsb2NraW5nJTIwbWFjaGluZXxlbnwwfDB8fHwxNzg4MjUyNzM1fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 6.2
adoption_velocity: "MODERATE"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Source-linked wiki entries create an auditable chain of provenance for AI-synthesised internal knowledge, enabling defenders to trace how conclusions were reached", "Per-user connection scoping limits blast radius: individually connected accounts are not shared across the organisation by default", "Human-in-the-loop checkpoints at payment, login, and high-stakes decisions reduce autonomous action without explicit approval", "Visible, revocable integration list gives administrators a single pane to audit and control what data sources the agent can access", "Wiki correction mechanism allows defenders to push ground-truth corrections that the agent immediately incorporates, reducing persistent hallucination risk"]

# ── AI Security Classification ──
relevance_score: 5.8
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0070 - RAG Poisoning", "AML.T0071 - False RAG Entry Injection", "AML.T0080 - AI Agent Context Poisoning", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0083 - Credentials from AI Agent Configuration", "LLM08 - Excessive Agency"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Almanac ships a persistent AI agent with its own browser, logins, and a self-updating company wiki."
tldr_who_at_risk: "Security and IT teams at SMBs adopting Almanac benefit from auditable AI actions but must govern wide-scope tool access carefully."
tldr_actions: ["Audit every tool connection Almanac is granted and apply least-privilege scoping before deployment", "Establish a wiki review cadence — assign owners to validate AI-synthesised entries for high-sensitivity topics", "Define explicit human-approval thresholds for actions beyond Almanac's default checkpoints (payments, auth flows, external comms)"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security"]
tags: ["agentic-ai", "rag", "knowledge-management", "browser-agent", "tool-integration", "wiki", "yc-s26", "autonomous-agents", "access-governance", "insider-risk"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-01T08:52:15+00:00"
feed_source: "hn_ai_security"
original_url: "https://usealmanac.com/"
pipeline_version: "2.1.0"
---

## Defender Impact
Almanac introduces a structured, source-linked knowledge layer over disparate SaaS tools — giving security and operations teams an auditable, correctable record of AI-synthesised internal decisions. For organisations struggling with shadow-knowledge sprawl across Slack, email, and docs, this closes a meaningful observability gap.

## Capability Overview
Almanac is a persistent AI agent backed by Y Combinator (S26) that operates with its own browser, file system, and authenticated sessions into connected tools. Its core mechanism is a self-updating internal wiki: as work happens across Slack, Gmail, Granola, GitHub, and other integrations, Almanac synthesises the relevant understanding — decisions made, commitments given, open issues — into structured wiki pages. Crucially, every wiki entry links back to its originating source, so any reader (human or automated process) can validate the provenance of a claim.

The agent operates in two modes: task execution (initiated by the user via Slack or iMessage) and proactive monitoring (Almanac notices something worth doing and surfaces it without being asked). At defined thresholds — logins, payments, decisions flagged as requiring human judgement — it pauses and requests confirmation or hands control back to the user via a live browser session.

Access scoping is per-user by default. Individually connected accounts are not shared organisation-wide; only distilled understanding flows into the shared wiki, not raw inbox content. Shared accounts must be explicitly added by the organisation.

## Defensive Advances
**Auditable AI action trail.** Because every wiki line links to its source, security teams can trace how the agent reached a conclusion and verify it against primary evidence. This is a meaningful step beyond black-box AI summarisation.

**Revocable, visible integrations.** A single integration list that administrators can inspect and revoke provides a practical control surface — something many agentic tools have historically lacked.

**Human-in-the-loop at high-stakes actions.** Explicit checkpoints before payments, logins, and consequential decisions reduce the autonomous action surface and give defenders a model for where to concentrate monitoring.

**Wiki-correction as a ground-truth mechanism.** When the wiki is wrong, a human correction immediately propagates to the agent's working knowledge. This gives defenders a correction pathway that doesn't require retraining or a support ticket.

**Scoped data sharing.** The architectural separation between raw personal data (stays with the individual) and synthesised organisational understanding (shared wiki) is a reasonable privacy boundary that limits lateral exposure.

## Residual Gaps
**Wiki poisoning surface.** The wiki is the agent's primary context. If adversarial content reaches the tools Almanac monitors (e.g., a crafted Slack message, a malicious email), it may be synthesised into wiki entries and subsequently acted upon. The maturity question is: what input validation and anomaly detection exists on the ingestion pipeline?

**Scope of autonomous browser action.** The "signs into your tools and uses them like you would" capability is powerful but requires clear organisational policy on what actions are in-scope. Organisations should not assume Almanac's default checkpoints align with their risk tolerance without reviewing them explicitly.

**Credential storage and session security.** An agent that maintains persistent authenticated sessions across many SaaS tools represents a high-value credential aggregation point. The security of those stored sessions and how they are isolated will be a key maturity question for enterprise adopters.

**Wiki accuracy at scale.** As the number of connected tools and users grows, the signal-to-noise ratio of synthesised wiki entries becomes harder to maintain. Organisations will need governance processes — wiki owners, review cadences — to prevent the wiki from becoming a source of overreliance.

**Audit log granularity.** The product surfaces action visibility ("you can watch every step of a run"), but it is not yet clear whether this produces a durable, exportable audit log suitable for compliance or incident response purposes.

## Framework Mapping
The wiki-as-RAG architecture maps directly to **AML.T0070 (RAG Poisoning)** and **AML.T0071 (False RAG Entry Injection)** as surfaces defenders must govern. The browser agent capability is relevant to **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** and **AML.T0098 (AI Agent Tool Credential Harvesting)**. OWASP **LLM08 (Excessive Agency)** is the primary category — Almanac's checkpoints are a partial mitigation, but organisational policy must complete the control. **LLM09 (Overreliance)** is a secondary concern as wiki accuracy becomes load-bearing for business decisions.

## Deployment Considerations
Organisations should treat Almanac's integration list as a privileged access review surface — apply the same scrutiny as OAuth application governance. Start with read-only integrations before enabling write-back actions. Define a wiki ownership model before rollout: assign domain owners responsible for validating AI-synthesised entries in their area. Review Almanac's default human-approval thresholds against your organisation's risk policy and extend them where needed.

## Defender Checklist
- [ ] Inventory every tool connection granted to Almanac and apply least-privilege scoping
- [ ] Assign wiki page owners for sensitive domains (customers, pricing, security)
- [ ] Review default autonomous-action thresholds and extend human-approval requirements to match organisational risk policy
- [ ] Establish a periodic wiki accuracy review cadence
- [ ] Assess credential storage and session isolation before connecting high-privilege accounts
- [ ] Determine whether Almanac's action logs meet your audit and compliance requirements

## References
- [Almanac — usealmanac.com](https://usealmanac.com/)
