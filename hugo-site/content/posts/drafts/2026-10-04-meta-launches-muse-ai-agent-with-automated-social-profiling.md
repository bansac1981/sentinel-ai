---
title: "Meta Launches Muse AI Agent with Automated Social Profiling"
date: 2026-10-04T11:16:41+00:00
draft: true
slug: "meta-launches-muse-ai-agent-with-automated-social-profiling"

# ── Content metadata ──
summary: "Meta's Muse AI agent automatically constructs structured relationship profiles of every person in a user's social network, drawing on connected bank accounts, messages, and health data to generate hourly-updated dossiers. For defenders, this surfaces a concrete, auditable example of how agentic memory architectures aggregate sensitive third-party data at scale \u2014 providing a useful reference case for evaluating data minimisation controls and consent boundaries in enterprise AI deployments. What remains unaddressed is whether organisations have the policy maturity and tooling to detect when sanctioned AI agents quietly become data brokers for individuals who never opted into the system."
source: "Wired Security"
source_url: "https://www.wired.com/story/muse-creates-detailed-profiles-of-all-your-friends-and-family"
source_title: "Muse Creates Detailed Profiles of All Your Friends and Family"
source_date: 2026-10-03T12:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/13201819/pexels-photo-13201819.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 6.5
adoption_velocity: "RAPID"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Agentic memory systems that aggregate third-party personal data without those third parties' consent create a new class of sensitive data store that security teams must now account for in data inventories and access control policies", "System prompt extraction via conversational interface — demonstrated by Joshi — illustrates that internal agent instructions and memory schemas can be retrieved by users, requiring defenders to treat agent configuration as potentially discoverable and to design for transparency rather than security-through-obscurity", "Hourly automated profiling pipelines connected to financial, health, and messaging data represent a high-value aggregation target; defenders must evaluate whether existing DLP and CASB controls extend to agent-generated memory files", "Structured relationship graphs built by AI agents introduce a new insider-risk surface: compromised or misused agent accounts could expose relationship metadata for an entire organisation's social graph, not just the primary user"]

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0069 - Discover LLM System Information", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0084 - Discover AI Agent Configuration", "AML.T0080 - AI Agent Context Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Meta's Muse agent automatically builds hourly-updated relationship profiles on every person in a user's life."
tldr_who_at_risk: "Security and privacy teams benefit from a concrete, auditable reference case for how agentic memory architectures aggregate sensitive third-party data without explicit consent."
tldr_actions: ["Audit existing AI agent deployments for uncontrolled memory or profiling capabilities that aggregate third-party data", "Treat agent system prompts and memory schemas as discoverable artefacts — design for transparency and apply access controls accordingly", "Update data inventory and DLP policies to explicitly cover agent-generated structured memory files connected to financial, health, or messaging sources"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News", "Regulatory"]
tags: ["meta", "muse", "ai-agent", "agentic-memory", "social-profiling", "data-aggregation", "system-prompt-extraction", "privacy", "relationship-graph", "consumer-ai", "data-minimisation", "llm-memory"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-10-04T11:16:41+00:00"
feed_source: "wired_security"
original_url: "https://www.wired.com/story/muse-creates-detailed-profiles-of-all-your-friends-and-family"
pipeline_version: "2.1.0"
---

## Defender Impact

Meta's Muse provides the defender community with a high-visibility, real-world reference architecture for how agentic memory systems aggregate sensitive third-party data at scale — without those third parties ever consenting or knowing. For security teams evaluating or deploying AI agents in enterprise environments, this is an important maturity signal: the gap between "helpful personal assistant" and "unsanctioned data broker" is narrower than most data governance frameworks currently account for.

## Capability Overview

Muse is Meta's consumer AI agent, connecting to bank accounts, messages, and health data to complete tasks on behalf of users. What distinguishes it from a standard AI chatbot is its persistent, structured memory architecture. According to internal instructions extracted by researcher Karan Joshi via the chat interface itself, Muse runs an hourly process that builds a dedicated profile page for every person in the user's life — family, partners, friends, colleagues, collaborators, and followed accounts.

Each profile can include structured fields: Facts, History, The Relationship, In Common, Open Threads, and Strengthening. The system is designed to populate these fields incrementally from available evidence — messages, shared context, behavioural patterns — and explicitly instructs the model not to invent details. The practical result is a continuously updated social graph of the user's relationships, stored as structured text files within the agent's memory layer.

The extraction method itself is significant. Joshi retrieved Muse's operating instructions and memory schemas simply by asking the agent to copy and share its own software files through the standard chat interface. Meta has indicated this was intentional for transparency purposes — but the episode demonstrates that agent configuration is effectively user-accessible by design, a architectural decision with meaningful security implications for enterprise deployments.

## Defensive Advances

**Reference architecture for agentic data aggregation risk.** Muse gives defenders a concrete, documented example of how agentic memory pipelines work at scale. Security teams can now map this pattern against their own AI deployments and ask: does our agent do something equivalent? Who can access those memory files? Are they in scope for our data classification policies?

**System prompt discoverability as a design principle.** The fact that Joshi extracted Muse's instructions via normal chat interaction — and that Meta framed this as intentional transparency — establishes a useful precedent. Defenders can use this case to advocate for explicit documentation of agent capabilities as a security control, rather than relying on opacity. If configuration is going to be discoverable anyway, designing for it reduces the gap between stated and actual agent behaviour.

**Third-party data subject identification.** Muse's profiling of individuals who never installed or consented to the application surfaces a category of data subject that most AI governance frameworks have not yet explicitly addressed. Defenders can use this case to pressure-test whether their AI usage policies cover data about non-users generated by agent memory systems.

## Residual Gaps

The primary maturity gap is on the organisational side, not the technical side. Most enterprise data governance frameworks were built around data subjects who interact with systems directly. Muse's model — where a third party's personal information is profiled by an agent the third party has no relationship with — falls outside the scope of most existing DLP, CASB, and privacy impact assessment processes. Closing this gap requires policy updates, not just tooling.

Secondly, the hourly aggregation cadence means that agent memory stores are dynamic. Static data inventory approaches will miss drift in what these systems accumulate over time. Organisations adopting agentic tools need continuous monitoring of memory content, not point-in-time audits.

Finally, the consent and notice framework for agent-generated social graphs remains immature across the industry. Defenders operating in regulated sectors (healthcare, finance, legal) should not assume that existing data processing agreements cover this use pattern without explicit legal review.

## Framework Mapping

- **AML.T0057 (LLM Data Leakage)** and **LLM06 (Sensitive Information Disclosure)**: Muse's memory files represent a novel sensitive data store; leakage of relationship graphs would constitute a significant disclosure event.
- **AML.T0056 (LLM Meta Prompt Extraction)** and **AML.T0069 (Discover LLM System Information)**: Joshi's extraction method is a live demonstration of these techniques requiring no specialist tooling.
- **LLM08 (Excessive Agency)**: Autonomous hourly profiling of third parties is a textbook example of an agent acting beyond reasonable user expectation.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: Structured relationship data accessible through agent tooling represents a high-value exfiltration target.

## Deployment Considerations

Organisations should not treat Muse as an isolated consumer privacy story. The architectural patterns it demonstrates — persistent structured memory, third-party profiling, hourly aggregation from multiple data sources — are appearing in enterprise AI agent products. Before deploying any agentic tool with memory capabilities, security teams should require vendors to document: what data is stored in memory, how long it is retained, who can query it, and whether it includes data about individuals who are not the primary user.

For organisations already running AI agents, a focused memory audit is warranted: enumerate what structured data your agents are accumulating, apply data classification, and verify that access controls match sensitivity.

## Defender Checklist

- [ ] Enumerate all AI agents in your environment with persistent memory or profiling capabilities
- [ ] Classify agent-generated memory files under your existing data governance framework — if they don't fit, update the framework
- [ ] Verify that DLP and CASB policies apply to agent memory stores, not just primary data sources
- [ ] Review vendor documentation for any agent product to understand third-party data subject handling
- [ ] Conduct a legal review of whether existing data processing agreements cover agent-generated social or relationship graphs
- [ ] Implement continuous monitoring of agent memory content rather than relying on point-in-time audits
- [ ] Use the Muse system-prompt extraction case to brief stakeholders: agent configuration should be treated as discoverable, not secret

## References

- [Muse Creates Detailed Profiles of All Your Friends and Family — WIRED, October 2026](https://www.wired.com/story/muse-creates-detailed-profiles-of-all-your-friends-and-family)
