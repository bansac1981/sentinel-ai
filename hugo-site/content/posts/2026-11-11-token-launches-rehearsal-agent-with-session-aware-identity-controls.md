---
title: "Token Launches Rehearsal Agent with Session-Aware Identity Controls"
date: 2026-11-11T12:55:21+00:00
draft: false
slug: "token-launches-rehearsal-agent-with-session-aware-identity-controls"

# ── Content metadata ──
summary: "Token built and red-teamed a browser-based UI agent called Rehearsal that operates within authenticated user sessions, deliberately violating conventional identity, least-privilege, and traceability controls to expose the structural gaps in how web applications handle agent-driven sessions. The exercise produced a concrete set of defensive best practices \u2014 including agent-distinct identity signalling, read-only scope enforcement, and per-session action recording \u2014 that organisations can apply today when they control both the agent and the target application. The residual gap is significant: these controls only work end-to-end when the same party owns both the agent and the application, leaving third-party agents driving enterprise SaaS largely invisible to downstream platforms."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/we-built-agent-that-broke-all-of-our.html"
source_title: "We Built An Agent That Broke All of Our Security Rules. Here's What We Learned."
source_date: 2026-11-11T12:01:59+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1723022208597-a641bdadf60c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxtZWNoYW5pY2FsJTIwZ2VhcnMlMjBpbnRlcmxvY2tpbmclMjBtYWNoaW5lfGVufDB8MHx8fDE3OTQ0MDE3MTl8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 7.0
adoption_velocity: "MODERATE"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Agent-distinct identity signalling: defenders can now require that browser agents declare their own actor identity separately from the human session cookie, enabling platforms to distinguish agent from human action", "Scoped read-only agent modes: organisations can configure agents to operate below user privilege levels, preventing destructive or irreversible actions without explicit human approval", "Per-session agent action recording: every agent move — including blocked actions — can be logged to a separate audit trail, independent of the human user's activity log", "UI-layer session lock indicators: applications can visually and functionally lock the interface while an agent is driving, providing a clear human-override mechanism", "Accessibility-label-based scope awareness: agents can be trained to understand field sensitivity through page accessibility metadata, reducing the risk of secret-field interaction or high-stakes button activation"]

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0080 - AI Agent Context Poisoning", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0113 - Steal Web Session Cookie", "AML.T0103 - Deploy AI Agent"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Token built and stress-tested a browser UI agent called Rehearsal that deliberately broke identity, privilege, and traceability rules to surface defensive fixes."
tldr_who_at_risk: "Security and platform engineering teams deploying or operating AI agents benefit by gaining a concrete, tested model for agent identity separation and least-privilege enforcement."
tldr_actions: ["Assign agents their own distinct identity separate from the human session they operate within", "Enforce read-only or reduced-scope agent modes and require explicit human approval for irreversible actions", "Implement per-session agent action logging independent of human user audit trails"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Research"]
tags: ["ai-agents", "browser-agents", "session-identity", "least-privilege", "agent-traceability", "ui-agent", "identity-and-access", "agentic-security", "token-platform", "rehearsal-agent", "session-hijacking", "agent-governance"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-11-11T12:55:21+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/we-built-agent-that-broke-all-of-our.html"
pipeline_version: "2.1.0"
content_hash: "1881d85483fdf512"
---

## Defender Impact

Token's Rehearsal experiment closes a critical knowledge gap: it provides a concrete, tested reference model for how browser-based AI agents should be governed at the identity, privilege, and auditability layers — areas where most organisations currently have no controls at all.

## Capability Overview

Token built Rehearsal, a browser UI agent designed to answer questions inside the Token platform by autonomously navigating pages, setting filters, and completing forms. Rather than shipping it as a finished product, Token used it as a deliberate red-team exercise: the agent was designed to violate the three identity controls Token recommends to its own customers — distinct agent identity, task-scoped access, and separate audit traceability.

The core problem Rehearsal exposes is structural. When a browser agent acts inside an authenticated user session, the downstream application sees only the session cookie — which carries the user's identity, not the agent's. The application cannot distinguish agent-driven clicks from human clicks, cannot determine the intended task scope, and cannot trace which actions were agent-initiated. This is not a configuration failure; it is an architectural gap in how web sessions were designed, predating agentic AI by decades.

Because Token controls both Rehearsal and the platform it operates within, the team was able to implement mitigations from both sides of the session boundary: the agent declares its own actor identity explicitly, the application locks and dims the UI while the agent is in control, every action is recorded to a separate session log, and the agent's scope is capped below the user's — operating read-only unless a human explicitly approves a write action. The agent also uses accessibility labels to identify sensitive fields and high-stakes controls, allowing it to self-restrict without application-side enforcement.

Token notes that Chrome's emerging auto-browse capability is beginning to move in a similar direction at the browser layer — requiring human approval before payments or mass actions — but acknowledges that no holistic, cross-platform standard yet exists.

## Defensive Advances

The Rehearsal exercise produces five concrete defensive advances that security teams can apply today when they own both the agent and the target application:

1. **Agent identity declaration**: Agents can be instrumented to signal their actor identity and delegating user to the application, enabling server-side distinction between human and agent sessions.
2. **Privilege scoping below the human**: Agent access can be deliberately capped to a subset of the user's permissions — read-only by default, with write actions gated on explicit approval.
3. **Separate audit trails**: Agent session logs can be maintained independently from human user activity logs, preserving traceability without commingling the two.
4. **UI-layer session lock**: Applications can visually and functionally indicate agent control and block concurrent human input, reducing confusion and enabling clear override.
5. **Accessibility-metadata-based sensitivity inference**: Agents can use existing page accessibility labels to identify secret fields and destructive controls without requiring application-side API changes.

## Residual Gaps

The controls Token implemented rely entirely on owning both the agent and the application. This is not the common case. The majority of real-world deployments involve third-party agents (workflow automation tools, copilots, browser extensions) operating against enterprise SaaS platforms that have no awareness of the agent's presence, identity, or task scope.

For this broader case, the fix requires either: (a) application providers exposing dedicated agent-session APIs that accept actor declarations and enforce scope; or (b) browser-layer standards (like Chrome's emerging agent mode) that mediate between agent and application on behalf of both. Neither is mature enough for enterprise-wide reliance today.

Organisations also need agent inventory maturity before these controls can be applied systematically — most security teams do not yet have a complete picture of which agents are operating within their environments, let alone which user sessions they are riding.

## Framework Mapping

- **AML.T0012 (Valid Accounts)** / **AML.T0113 (Steal Web Session Cookie)**: Rehearsal directly addresses the risk of agents inheriting full user session identity by implementing explicit agent identity separation.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** / **LLM08 (Excessive Agency)**: Scope reduction and human approval gates directly constrain the agent's ability to perform actions beyond its intended remit.
- **AML.T0080 (AI Agent Context Poisoning)** / **LLM06 (Sensitive Information Disclosure)**: Accessibility-label-based field sensitivity inference reduces the risk of agents inadvertently interacting with credential or secret fields.
- **LLM07 (Insecure Plugin Design)**: The per-session action log and UI lock address auditability gaps that characterise poorly governed agent integrations.

## Deployment Considerations

Organisations that both build and operate their own agents should treat the Rehearsal control set as a minimum baseline — not a ceiling. For teams consuming third-party agents against internal applications, the near-term priority is visibility: instrument applications to detect and log session anomalies consistent with agent-driven behaviour (high action velocity, accessibility-API usage patterns, non-human navigation sequences) even before formal agent identity standards arrive.

Platform and identity teams should begin evaluating whether their IAM infrastructure can support agent-distinct service accounts and scoped delegation tokens, as these will become prerequisites when standards do mature.

## Defender Checklist

- [ ] Audit which AI agents currently operate within authenticated user sessions across your environment
- [ ] For internally built agents: implement explicit actor identity declaration separate from the human session cookie
- [ ] Enforce read-only or reduced-scope agent modes; gate irreversible actions on explicit human approval
- [ ] Stand up per-session agent action logging independent of human user audit trails
- [ ] Instrument applications to detect agent-consistent session behaviour patterns as a detective control
- [ ] Track Chrome auto-browse and emerging W3C/browser-layer agent session standards for adoption readiness
- [ ] Include agent session governance requirements in procurement criteria for third-party AI tooling

## References

- [We Built An Agent That Broke All of Our Security Rules. Here's What We Learned — The Hacker News, 11 Nov 2026](https://thehackernews.com/2026/11/we-built-agent-that-broke-all-of-our.html)
