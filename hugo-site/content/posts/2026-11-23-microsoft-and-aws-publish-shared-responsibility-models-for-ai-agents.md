---
title: "Microsoft and AWS Publish Shared Responsibility Models for AI Agents"
date: 2026-11-23T16:18:19+00:00
draft: false
slug: "microsoft-and-aws-publish-shared-responsibility-models-for-ai-agents"

# ── Content metadata ──
summary: "Five major organisations \u2014 including Microsoft, AWS, CSA, CoSAI, and Anthropic \u2014 have published guidance frameworks attempting to define shared responsibility boundaries for AI agents operating across cloud and enterprise environments. This closes a critical governance gap by giving security teams the first structured reference points for assigning ownership of agent identity, delegated permissions, and per-action authorisation \u2014 surfaces that existing cloud shared responsibility models were never designed to cover. Significant maturity gaps remain, however, as the published frameworks disagree on who owns agent identity and offer no consensus on behavioural accountability."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/ai-agents-are-creating-a-shared-responsibility-gap"
source_title: "AI Agents Are Creating a Shared Responsibility Gap"
source_date: 2026-11-23T15:00:10+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1785753759888-da36892255ae?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxNaWNyb3NvZnQlMjBkcm9uZSUyMGFlcmlhbCUyMGF1dG9ub21vdXMlMjBmbGlnaHR8ZW58MHwwfHx8MTc5NTQ1MDY5OHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 7.5
adoption_velocity: "MODERATE"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Formalised agent identity ownership assignment gives defenders an anchor point for IAM policy design in agentic deployments", "Per-action authorisation responsibility matrices enable security teams to build least-privilege enforcement at the agent action layer", "Delegated token management guidance reduces the risk of over-privileged agent sessions persisting beyond intended scope", "Structured stakeholder role definitions allow organisations to close accountability gaps before agents reach production"]

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0103 - Deploy AI Agent"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Five organisations publish the first structured shared responsibility frameworks covering AI agent identity, permissions, and behaviour accountability."
tldr_who_at_risk: "Security and governance teams deploying AI agents benefit by gaining the first structured reference points for assigning ownership of agent actions, identity, and delegated access across cloud environments."
tldr_actions: ["Map your existing agentic deployments against Microsoft's IaaS/PaaS/SaaS responsibility matrix to identify unowned accountability gaps", "Assign explicit ownership for every agent identity and delegated token in your environment before expanding agent permissions", "Adopt per-action authorisation checkpoints as a baseline control regardless of which framework your organisation aligns to"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Regulatory", "Industry News"]
tags: ["ai-agents", "shared-responsibility", "agent-identity", "microsoft", "aws", "anthropic", "csa", "cosai", "delegated-permissions", "governance", "iam", "agentic-ai", "cloud-security", "accountability"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "insider", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-11-23T16:18:19+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/ai-agents-are-creating-a-shared-responsibility-gap"
pipeline_version: "2.1.0"
content_hash: "d36359fa292b6723"
---

## Defender Impact

For the first time, defenders have structured, vendor-published reference frameworks that attempt to define who is responsible for AI agent identity, delegated permissions, and per-action authorisation. This matters because agentic AI has been expanding rapidly into production environments while governance models have lagged behind — leaving security teams with no agreed baseline for policy design or accountability assignment.

## Capability Overview

Five organisations — Microsoft, AWS, the Cloud Security Alliance (CSA), CoSAI, and Anthropic — have published guidance addressing shared responsibility for AI agents. Each takes a different approach. Microsoft publishes a responsibility matrix spanning IaaS, PaaS, and SaaS deployment models, explicitly assigning agent identity management and delegated token handling to customers in IaaS, and treating them as shared responsibilities in PaaS. AWS's AgentCore security guidance focuses on operational security layers. Anthropic's *Trustworthy Agents in Practice* addresses stakeholder roles more broadly. CSA and CoSAI contribute their own framing of provider and customer obligations.

The central problem these frameworks are responding to is structural: AI agents send authenticated, authorised requests on behalf of users or systems, but the non-deterministic nature of the agent layer means those requests can deviate from intent without constituting a recognisable attack signature. Unlike cloud infrastructure, where data custody transfers between vendors are well-defined, an agent operating across Google Drive, a CRM, and an internal API creates action chains that no single vendor can fully observe or govern. The frameworks collectively attempt to draw accountability lines in this space — something that has not previously existed in published form.

## Defensive Advances

The publication of these frameworks gives defenders concrete new capabilities:

- **Agent identity as a first-class security object.** Security teams can now anchor IAM policy design to vendor-endorsed models that treat agent identity as a distinct, ownable surface — not an extension of user identity.
- **Per-action authorisation as a baseline expectation.** Microsoft's matrix explicitly positions per-action authorisation checks as a customer responsibility in IaaS deployments. This gives security architects a defensible baseline to enforce in procurement and deployment standards.
- **Delegated token lifecycle management.** Guidance on delegated token management addresses a previously underdocumented exposure: long-lived agent sessions holding credentials beyond their intended scope. Defenders can now build token rotation and revocation policies against a published reference.
- **Accountability scaffolding for incident response.** When an agent takes an unexpected or harmful action, the absence of an agreed responsibility model has historically made incident triage ambiguous. These frameworks provide the starting vocabulary for post-incident accountability discussions with vendors.

## Residual Gaps

The frameworks are a meaningful starting point, but significant maturity gaps remain:

- **No consensus on behavioural accountability.** None of the five frameworks agree on who is responsible for an agent's behaviour when it acts within its permissions but contrary to business intent. This is the hardest problem, and it remains unresolved.
- **Agent identity ownership is still contested.** Only two of the five frameworks assign ownership of agent identity, and they split it differently. Organisations cannot yet derive a single authoritative answer from published guidance alone.
- **Coverage is uneven across deployment models.** Microsoft's matrix is the most granular, but its SaaS guidance treats many controls as shared — which in practice often means neither party enforces them rigorously. SaaS-deployed agents remain the least well-governed surface.
- **Integration with existing IAM tooling is immature.** Even where responsibility is clearly assigned to the customer, the tooling required to implement per-action authorisation at scale — across heterogeneous agent frameworks and tool integrations — is not yet standardised.

## Framework Mapping

These frameworks most directly address **LLM08 (Excessive Agency)** by providing governance structures for constraining agent permissions, and **LLM07 (Insecure Plugin Design)** by clarifying who is responsible for the tool integrations agents invoke. From a MITRE ATLAS perspective, the guidance is most relevant to **AML.T0012 (Valid Accounts)** and **AML.T0083 (Credentials from AI Agent Configuration)**, both of which exploit the ambiguity around agent identity and delegated access that these frameworks begin to resolve.

## Deployment Considerations

Organisations should treat these frameworks as governance inputs rather than technical controls. The recommended sequencing is: (1) audit existing agent deployments against Microsoft's IaaS/PaaS/SaaS matrix to identify gaps; (2) establish explicit ownership records for every agent identity in your environment; (3) implement per-action authorisation logging before expanding agent permissions; (4) review delegated token lifetimes against least-privilege principles. Organisations running agents in SaaS-delivered platforms should escalate shared-responsibility questions to vendors before expanding scope.

## Defender Checklist

- [ ] Review Microsoft's AI agent shared responsibility matrix and map it to your current deployment models
- [ ] Assign named ownership for every agent identity and delegated credential in production
- [ ] Implement per-action authorisation logging as a baseline telemetry requirement
- [ ] Establish token rotation and revocation policies for all delegated agent sessions
- [ ] Include agent identity governance in vendor procurement questionnaires
- [ ] Define internal policy on acceptable agent action scope before next deployment expansion

## References

- [AI Agents Are Creating a Shared Responsibility Gap — BleepingComputer, November 23 2026](https://www.bleepingcomputer.com/news/security/ai-agents-are-creating-a-shared-responsibility-gap)
