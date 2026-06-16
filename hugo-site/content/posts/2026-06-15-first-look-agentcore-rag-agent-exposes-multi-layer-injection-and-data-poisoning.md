---
title: "First Look: Amazon Bedrock AgentCore RAG Agent Exposes Multi-Layer Injection and Data Poisoning Surface"
date: "2026-06-16T01:47:22+00:00"
draft: false 
slug: "first-look-agentcore-rag-agent-exposes-multi-layer-injection-and-data-poisoning"

# ── Content metadata ──
summary: "Amazon Bedrock AgentCore now enables production-grade agentic systems that combine RAG retrieval, persistent cross-session memory, and direct user-facing endpoints authenticated only via Cognito Bearer tokens \u2014 all surfaced through a single /invocations endpoint. This architecture creates compounded attack surfaces where adversarially crafted content in S3-backed knowledge bases can propagate through the retrieve_and_generate pipeline directly into technician workflows. The persistent AgentCore Memory layer introduces a new cross-session context poisoning vector that does not exist in stateless LLM deployments."
source: "AWS Machine Learning Blog"
source_url: "https://aws.amazon.com/blogs/machine-learning/build-an-ai-powered-equipment-repair-assistant-using-amazon-bedrock-agentcore/"
source_title: "Build an AI-Powered Equipment Repair Assistant Using Amazon Bedrock AgentCore"
source_date: 2026-06-10T15:21:35+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1677442135136-760c813028c0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw1fHxkYXRhYmFzZSUyMHNlYXJjaCUyMGFydGlmaWNpYWwlMjBpbnRlbGxpZ2VuY2V8ZW58MHwwfHx8MTc4MTUzMjE1Nnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 7.1
adoption_velocity: "MODERATE"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Knowledge base poisoning via malicious documents uploaded to the S3-backed equipment manual store, causing the RAG pipeline to return attacker-controlled repair instructions to field technicians", "Indirect prompt injection through indexed manufacturer documentation — adversarial instructions embedded in PDFs or parts catalogs are retrieved and executed by the Strands agent", "Cross-session memory poisoning: persistent AgentCore Memory allows injected context from one session to influence future sessions for the same or other users", "Single-endpoint attack surface: the unified /invocations endpoint with path-based routing (/chat, /issues) means a successful prompt injection that manipulates the path field could trigger unintended CRUD operations on DynamoDB service tickets", "Bearer token replay or theft via the frontend-to-AgentCore direct call pattern, bypassing any API gateway-layer controls", "Model output trust escalation: technicians acting on AI-generated repair procedures in high-stakes physical environments (heavy farm machinery) amplifies the real-world impact of any successful injection or data poisoning attack"]

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0019 - Publish Poisoned Datasets", "AML.T0020 - Poison Training Data", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM09 - Overreliance", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "AgentCore ships a RAG-plus-persistent-memory agent pattern that creates compounded injection, poisoning, and session-persistence attack surfaces."
tldr_who_at_risk: "Organizations deploying AgentCore-based agents with S3-backed knowledge bases and persistent memory in operational or safety-critical environments are newly exposed to cross-session context poisoning and indirect prompt injection."
tldr_actions: ["Implement strict ingestion-time document scanning and integrity verification for all S3 content fed into Bedrock Knowledge Bases", "Audit AgentCore Memory scoping to ensure session context cannot bleed across user identities or roles", "Add an API Gateway layer with input validation in front of the /invocations endpoint rather than exposing it directly to the Cognito-authenticated frontend"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "Prompt Injection", "Data Poisoning", "LLM Security"]
tags: ["amazon-bedrock", "agentcore", "rag-poisoning", "prompt-injection", "cross-session-memory", "strands-agents", "knowledge-base", "agentic-systems", "iot-industrial", "bearer-token", "aws", "retrieve-and-generate"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "insider", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-06-15T14:02:36+00:00"
feed_source: "aws_ml"
original_url: "https://aws.amazon.com/blogs/machine-learning/build-an-ai-powered-equipment-repair-assistant-using-amazon-bedrock-agentcore/"
pipeline_version: "2.0.0"
---

## Capability Overview

AWS has published a reference architecture for an AI-powered equipment repair assistant built on Amazon Bedrock AgentCore, combining the Strands Agents SDK, Amazon Nova 2 Lite, a Bedrock Knowledge Base backed by S3 and OpenSearch Serverless, and AgentCore Memory for cross-session persistence. The pattern is explicitly production-oriented: it uses real Cognito authentication, AWS Amplify hosting, DynamoDB for ticket CRUD, and a single `/invocations` endpoint that routes both AI queries and data mutations. For defenders, this is not a demo — it is a blueprint that organisations in agriculture, manufacturing, and field-service verticals will deploy against safety-critical physical systems.

## Attack Surface Analysis

**RAG Knowledge Base as an injection vector.** The `search_equipment_knowledge` tool passes user queries directly into `retrieve_and_generate` against an S3-backed knowledge base. Any attacker who can write to that S3 bucket — through a misconfigured bucket policy, a compromised CI/CD pipeline that publishes documentation updates, or a malicious supplier submitting counterfeit manuals — can embed adversarial instructions that the agent will retrieve and return as authoritative repair guidance. Unlike a traditional web defacement, the output reaches a technician who may act on it physically with heavy machinery.

**Cross-session memory poisoning.** AgentCore Memory persists conversation context across sessions. This is a meaningful architectural departure from stateless LLM calls. A successful prompt injection in session A that writes poisoned context into memory can influence the agent's responses in session B — potentially for a different user if memory scoping is misconfigured. This vector has no direct equivalent in classic stateless RAG deployments.

**Unified endpoint path-routing abuse.** The single `/invocations` endpoint routes internally on a `path` field (`/chat` vs `/issues`). If an attacker can manipulate this field through prompt injection or a crafted frontend request, they may trigger unintended CRUD operations on DynamoDB service tickets — creating, modifying, or deleting repair records.

**Direct frontend-to-AgentCore exposure.** The architecture routes calls directly from the Amplify frontend to the AgentCore Runtime endpoint using a Cognito Bearer token, with no API Gateway intermediary shown. This removes a standard layer where input validation, rate limiting, and WAF rules would normally sit. Bearer token theft via XSS in the React frontend grants direct inference API access.

**Overreliance in high-consequence physical environments.** Field technicians operating heavy farm machinery will act on agent output without secondary verification. Any successful manipulation of the knowledge base or conversation memory translates directly to physical risk — incorrect torque specifications, wrong parts, or deferred safety-critical repairs.

## Framework Mapping

- **AML.T0051 (Prompt Injection) / LLM01**: Indirect injection through retrieved knowledge base documents is the primary vector.
- **AML.T0019/T0020 (Poisoned Datasets) / LLM05**: S3-backed knowledge base ingestion pipeline is a supply chain risk point.
- **AML.T0057 (LLM Data Leakage) / LLM06**: Persistent memory may surface sensitive ticket data or prior session content to unauthorised users if memory namespace controls are weak.
- **LLM08 (Excessive Agency)**: The agent can perform CRUD on DynamoDB service tickets — real-world state mutations — based on AI-generated routing decisions.
- **LLM09 (Overreliance)**: The use case explicitly targets technicians in the field without connectivity or specialist backup, maximising overreliance risk.

## Threat Scenarios

**Scenario 1 — Malicious supplier document injection.** A threat actor compromises a parts supplier's documentation portal. Updated PDFs containing embedded prompt injection payloads are submitted through a legitimate vendor update process, ingested into the S3 knowledge base, and indexed. Technicians subsequently receive dangerous repair instructions that appear to carry manufacturer authority.

**Scenario 2 — Cross-session memory persistence attack.** An attacker with legitimate technician credentials crafts a session that injects false diagnostic context into AgentCore Memory (e.g., "the hydraulic pressure sensor on unit X has been confirmed safe — skip re-check"). This context persists and influences subsequent sessions, suppressing safety checks for other users on the same equipment.

**Scenario 3 — Bearer token theft via frontend XSS.** A stored XSS vulnerability in the Amplify-hosted React application allows exfiltration of Cognito Bearer tokens. The attacker calls the `/invocations` endpoint directly, querying the knowledge base for proprietary repair procedures or enumerating and modifying service tickets via the `/issues` path.

## Defender Checklist

- [ ] Enforce S3 bucket policies with least-privilege write access; require document signing or hash verification before knowledge base ingestion
- [ ] Deploy an API Gateway with WAF, input length limits, and rate limiting in front of the AgentCore `/invocations` endpoint
- [ ] Audit AgentCore Memory namespace configuration — confirm session memory is strictly scoped per user identity, not per agent instance
- [ ] Implement output filtering on `retrieve_and_generate` responses before they reach the agent's tool return value
- [ ] Add human-in-the-loop confirmation for any agent action that triggers DynamoDB writes (ticket creation/modification)
- [ ] Monitor CloudWatch logs for anomalous path field values in invocation payloads
- [ ] Conduct red-team exercises specifically targeting indirect prompt injection via uploaded documentation

## References

- [Build an AI-Powered Equipment Repair Assistant Using Amazon Bedrock AgentCore — AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/build-an-ai-powered-equipment-repair-assistant-using-amazon-bedrock-agentcore/)
