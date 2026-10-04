---
title: "doxx.net Launches ADN Platform to Govern AI Agents Online"
date: 2026-10-04T11:17:27+00:00
draft: true
slug: "doxx-net-launches-adn-platform-to-govern-ai-agents-online"

# ── Content metadata ──
summary: "doxx.net has introduced its Agentic Defense Network (ADN) platform, designed to monitor and constrain AI agents operating on the internet under user-delegated authority, preventing unintended or out-of-scope actions. This closes a meaningful gap for defenders who currently lack runtime guardrails to supervise autonomous agents acting on behalf of users across external web surfaces. The platform's real-world maturity, integration breadth, and coverage of non-browser agentic channels remain open questions as the capability scales."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/doxx-net-raises-38-million-to-prevent-ai-agent-on-the-internet-misadventures"
source_title: "doxx.net Raises $38 Million to Prevent AI Agent-on-the-Internet Misadventures"
source_date: 2026-10-03T11:45:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1655635643568-f30d5abc618a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw0fHxwaXBlbGluZSUyMHdvcmtmbG93JTIwYXV0b21hdGlvbiUyMGFic3RyYWN0fGVufDB8MHx8fDE3OTExMTI2NDd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 6.5
adoption_velocity: "MODERATE"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Runtime supervision of AI agents operating under delegated user authority, enabling defenders to detect and block out-of-scope agent actions before they cause harm", "Behavioural boundary enforcement for agentic internet sessions, reducing the blast radius of compromised or misbehaving agents", "Centralised visibility layer for agentic activity on external web surfaces, giving security teams an audit trail previously unavailable for agent-driven actions"]

# ── AI Security Classification ──
relevance_score: 6.8
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0051 - LLM Prompt Injection", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0110 - AI Agent Tool Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "doxx.net launches ADN, a platform that supervises AI agents browsing the internet under delegated user authority."
tldr_who_at_risk: "Security teams deploying internet-facing AI agents benefit most \u2014 ADN provides runtime controls that prevent agents from taking unintended or harmful actions on users' behalf."
tldr_actions: ["Evaluate ADN integration against your existing agentic AI deployments to identify coverage gaps in agent supervision", "Map your organisation's delegated-authority agent workflows and prioritise those with external internet access for early ADN adoption", "Establish baseline agent behaviour policies before deployment so ADN enforcement rules reflect genuine operational intent"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News"]
tags: ["agentic-ai", "ai-agent-governance", "runtime-supervision", "excessive-agency", "internet-agents", "user-delegation", "agent-guardrails", "startup-funding", "defensive-tooling"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "insider", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-10-04T11:17:27+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/doxx-net-raises-38-million-to-prevent-ai-agent-on-the-internet-misadventures"
pipeline_version: "2.1.0"
---

## Defender Impact

Organisations deploying AI agents to act on users' behalf across the internet have had no standardised runtime control plane to enforce behavioural boundaries — doxx.net's ADN platform directly addresses this gap by inserting a supervision layer between agent intent and real-world action. For security teams, this represents the first commercially funded product explicitly scoped to the 'agent acting as user on the open web' problem.

## Capability Overview

doxx.net has raised $38 million to bring its Agentic Defense Network (ADN) platform to market. The platform is designed to prevent what the company calls 'agentic misadventure' — situations where an AI agent, operating under a user's delegated authority, takes actions that are unintended, out-of-scope, or harmful. The product intervenes while the agent is actively operating, rather than relying solely on pre-deployment configuration.

The core premise is that AI agents browsing the internet, submitting forms, interacting with third-party services, or managing accounts on a user's behalf inherit the user's trust context. Without a mediation layer, there is no mechanism to distinguish between an agent acting within the spirit of its mandate and one that has been manipulated, confused, or simply misconfigured into taking harmful steps. ADN positions itself as that mediation layer — a runtime policy enforcement and monitoring plane for agentic internet activity.

The $38 million funding round signals significant investor confidence that agentic oversight is becoming a distinct product category, separate from traditional endpoint or application security tooling. This is a meaningful market signal for defenders evaluating their agentic AI security architecture.

## Defensive Advances

**Runtime behavioural enforcement**: ADN provides controls that operate while an agent is executing, not just at configuration time. Defenders can now enforce what actions are permissible in real time rather than relying on prompt-level guardrails alone.

**Delegated authority visibility**: Security teams gain an audit trail for agent activity conducted under user authority — something previously absent from most agentic frameworks. This supports incident investigation and compliance documentation.

**Blast radius reduction**: By intercepting out-of-scope actions before they complete, ADN reduces the potential damage from an agent that has been misdirected — whether through prompt injection, context poisoning, or simple misconfiguration.

**Dedicated agentic security posture**: ADN represents a purpose-built control for agentic surfaces, moving defender capability beyond repurposed web proxies or LLM output filters into a category designed for the agent-as-user threat model.

## Residual Gaps

The article provides limited technical detail on ADN's architecture, making it difficult to assess coverage depth at this stage. Key maturity questions include:

- **Protocol and channel coverage**: It is unclear whether ADN covers non-browser agentic interactions — API calls, file transfers, MCP tool invocations — or is primarily scoped to web browsing agents.
- **Policy definition maturity**: Effective enforcement depends on organisations having well-articulated agent behaviour policies. Teams without these in place will face an integration prerequisite before ADN can be configured meaningfully.
- **Integration breadth**: Compatibility with the full landscape of agentic frameworks (LangChain, AutoGen, OpenAI Assistants API, custom agent runtimes) is not confirmed from available information.
- **Latency and throughput**: Runtime interception introduces latency considerations for high-frequency or time-sensitive agentic workflows — an operational trade-off that warrants evaluation.
- **False positive management**: Overly aggressive enforcement risks disrupting legitimate agent workflows; the platform's tuning capabilities and default policy sensitivity are not yet publicly documented.

## Framework Mapping

ADN most directly addresses **LLM08 (Excessive Agency)** — the OWASP category covering agents that take actions beyond their intended scope. It also provides a control surface relevant to **AML.T0080 (AI Agent Context Poisoning)** and **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** by enforcing boundaries that constrain what a manipulated or misbehaving agent can actually do. Secondary relevance applies to **LLM01 (Prompt Injection)** in cases where injection attempts are the root cause of the out-of-scope action ADN intercepts.

## Deployment Considerations

Organisations should approach ADN adoption sequentially: first inventory all agent workflows that touch external internet surfaces, then document intended behaviour scope for each workflow, and finally configure ADN enforcement policies against that documented baseline. Teams without an existing agent catalogue should complete that exercise before attempting integration. ADN should be treated as a complementary control alongside prompt-level guardrails and output filtering — not a replacement for either.

## Defender Checklist

- [ ] Inventory all AI agents operating under delegated user authority with external internet access
- [ ] Document intended behavioural scope for each agentic workflow before configuring enforcement policies
- [ ] Request ADN integration documentation for your specific agent frameworks and runtimes
- [ ] Define success metrics for agent supervision (false positive rate, blocked action rate) before deployment
- [ ] Align ADN policy review cadence with agent capability updates and model version changes
- [ ] Evaluate ADN alongside existing LLM output filtering and prompt guardrail controls to avoid coverage overlap or gaps

## References

- [doxx.net Raises $38 Million to Prevent AI Agent-on-the-Internet Misadventures — SecurityWeek](https://www.securityweek.com/doxx-net-raises-38-million-to-prevent-ai-agent-on-the-internet-misadventures)
