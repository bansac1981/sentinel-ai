---
title: "Netwrix Analysis: AI Agents Widen the Non-Human Identity Gap"
date: "2026-07-11T16:41:38+00:00"
draft: false
slug: "netwrix-analysis-ai-agents-widen-the-non-human-identity-gap"

# ── Content metadata ──
summary: "A Netwrix-sponsored analysis highlights how AI agents are rapidly proliferating machine identities inside enterprise environments, creating credentials and inheriting permissions far faster than existing identity governance can track. The core risk is that AI agents operate outside traditional human-lifecycle identity controls, leaving security teams unable to enumerate what exists, who owns it, or what it can access. Defenders face an expanding blind spot where a single compromised agent credential can chain laterally across cloud services, SaaS platforms, and secrets stores \u2014 as demonstrated by the UNC6395/Drift OAuth campaign against Salesforce environments in 2025."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/the-replicant-in-your-directory-ai-agents-and-the-identity-security-gap"
source_title: "The Replicant in Your Directory: AI Agents and the Identity Security Gap"
source_date: 2026-07-10T14:00:10+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1781330184655-8210f7010e0e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOXx8cm9ib3QlMjBhdXRvbWF0aW9uJTIwYXV0b25vbW91cyUyMHdvcmtmbG93fGVufDB8MHx8fDE3ODM3NjY0MzV8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 7.8
adoption_velocity: "RAPID"
capability_category: "agent-tooling"
attack_vectors_introduced: ["AI agents autonomously creating machine identities that are never registered in identity governance systems, leaving unmanaged credentials with persistent access", "AI agents inheriting over-privileged permissions from parent service accounts, enabling privilege escalation without explicit grants", "Compromised AI agent OAuth tokens enabling lateral movement across chained cloud services (e.g., Salesforce → AWS → Snowflake) without triggering human-behaviour baselines", "Long-lived forgotten agent credentials remaining active after the automation or application that created them is decommissioned, providing persistent footholds", "Machine identity sprawl (50:1 ratio) overwhelming manual review processes, allowing malicious or misconfigured agent identities to persist undetected", "AI agents storing or accessing secrets in non-vaulted locations, creating credential harvesting opportunities for lateral movement"]

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service", "AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "AI agents are creating and inheriting machine identities at scale, outpacing enterprise identity governance controls."
tldr_who_at_risk: "Any enterprise deploying AI agents in cloud or SaaS environments where machine identities are not inventoried, governed, or rotated consistently."
tldr_actions: ["Conduct a full inventory of all machine identities — including AI agent credentials, OAuth tokens, and service accounts — and assign explicit owners", "Apply least-privilege to every AI agent identity and enforce automated rotation and expiry policies", "Instrument SIEM and UEBA tooling to baseline and alert on non-human identity behaviour, especially cross-service token use"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News"]
tags: ["non-human-identity", "machine-identity", "ai-agents", "oauth-tokens", "identity-governance", "lateral-movement", "credential-sprawl", "service-accounts", "workload-identity", "unc6395", "salesforce", "aws", "snowflake", "netwrix", "zero-trust"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "insider"]

# ── Pipeline metadata ──
fetched_at: "2026-07-11T10:40:35+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/the-replicant-in-your-directory-ai-agents-and-the-identity-security-gap"
pipeline_version: "2.1.0"
---

## Capability Overview

As AI agent deployments scale across enterprise environments, they are generating a class of machine identity — credentials, OAuth tokens, service accounts, and workload identities — that existing identity governance frameworks were never designed to manage. A Netwrix-sponsored analysis published in July 2026 quantifies the scope: machine identities already outnumber human users by as many as 50 to one in many organisations, and AI agents are accelerating that ratio further. Unlike human identities, agent credentials do not follow predictable lifecycle events. They can be created dynamically, inherit permissions from parent processes, and persist long after the automation that spawned them has been retired. Most organisations cannot answer basic questions about who owns these identities, why they remain active, or what systems they can reach.

This is not a theoretical concern. The UNC6395 campaign in 2025 demonstrated the concrete impact: attackers obtained a single OAuth token tied to Salesloft's Drift integration and used it to traverse Salesforce environments across hundreds of victim organisations, then pivoted to AWS credentials and Snowflake tokens stored outside vault controls. The token was not exploited through a software flaw — it was already trusted.

## Attack Surface Analysis

AI agents introduce several compounding risks that defenders must assess independently:

**Identity sprawl at machine speed.** Unlike a human hire, an AI agent can create subordinate identities, spawn child processes, and request API access programmatically. Each of these actions may produce a credential that never appears in a traditional identity governance review.

**Inherited over-privilege.** Agents frequently inherit permissions from the service accounts or OAuth scopes used to instantiate them. If that parent identity held broad access — common in development or early deployment — the agent begins life over-privileged with no human review gate.

**Lateral movement via trust chaining.** A compromised agent token is not bounded by the application it was issued for. As UNC6395 showed, a single trusted credential can be the first link in a chain traversing multiple cloud services, each of which extended trust based on the prior hop.

**Orphaned credential persistence.** Agent identities are rarely deprovisioned when projects end. These dormant credentials represent persistent footholds with no active owner to notice anomalous use.

**Secrets mishandled at scale.** Agents that interact with APIs frequently cache or log secrets outside approved vault infrastructure, creating harvestable credential pools.

## Framework Mapping

- **AML.T0012 – Valid Accounts:** The primary attack pattern here is abuse of legitimate, trusted machine credentials rather than exploitation of a vulnerability.
- **AML.T0047 – ML-Enabled Product or Service:** AI agents as deployed products expand the trusted identity surface within enterprise environments.
- **LLM08 – Excessive Agency:** Agents operating with permissions beyond what their task requires is the structural precondition for blast-radius amplification after compromise.
- **LLM07 – Insecure Plugin Design:** OAuth integrations and tool-use connectors used by agents frequently lack scoped, revocable permission models.
- **LLM05 – Supply Chain Vulnerabilities:** Third-party AI agent frameworks and integrations inherit supply chain trust assumptions that may not have been validated.

## Threat Scenarios

**Scenario 1 — OAuth pivot:** An attacker phishes a developer with access to an AI agent's OAuth configuration. They extract the agent's token, which holds broad Salesforce read/write scope. From there they access connected AWS roles via OIDC federation and exfiltrate data from an S3 bucket the agent was permitted to write logs to.

**Scenario 2 — Orphaned agent foothold:** A proof-of-concept AI agent deployed during a hackathon six months ago retains an active service account with contributor rights to an Azure subscription. A threat actor discovers it via a misconfigured CI/CD pipeline log, uses the credential to deploy a cryptominer, and pivots to production key vaults.

**Scenario 3 — Agent-spawned identity abuse:** An autonomous AI agent, tasked with provisioning sandbox environments, creates child service principals with owner-level rights. An insider with access to the agent's task queue modifies instructions to redirect one of these principals to a personal-controlled tenant.

## Defender Checklist

- [ ] Run a discovery sweep specifically targeting non-human identities: OAuth apps, service principals, workload identities, and API keys — not just user accounts
- [ ] Map every AI agent deployment to an accountable human owner and document its permission scope
- [ ] Enforce just-in-time and time-bound credentials for agent identities wherever the platform supports it
- [ ] Require all agent-accessed secrets to be retrieved from an approved vault; audit for hardcoded or cached credentials in agent logs and config stores
- [ ] Establish behavioural baselines for non-human identities in your SIEM/UEBA platform and alert on cross-service token use outside expected patterns
- [ ] Include AI agent identities in quarterly access reviews with the same rigour applied to privileged human accounts
- [ ] Test agent deprovisioning workflows: confirm that retiring an AI project results in full credential revocation, not just application shutdown

## References

- [The Replicant in Your Directory: AI Agents and the Identity Security Gap — BleepingComputer (2026-07-10)](https://www.bleepingcomputer.com/news/security/the-replicant-in-your-directory-ai-agents-and-the-identity-security-gap)
