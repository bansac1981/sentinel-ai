---
title: "When an Attacker Meets a Group of Agents: Navigating Amazon Bedrock's Multi-Agent Applications"
date: 2026-04-23T04:06:38+00:00
draft: true
slug: "when-an-attacker-meets-a-group-of-agents-navigating-amazon-bedrock-s-multi-agent"

# ── Content metadata ──
summary: "Unit 42 researchers conducted red-team analysis of Amazon Bedrock's multi-agent collaboration framework, demonstrating how attackers can systematically exploit prompt injection to traverse agent hierarchies, extract system instructions, and invoke tools with attacker-controlled inputs. The research reveals that multi-agent architectures introduce compounded attack surfaces through inter-agent communication channels, though no underlying Bedrock vulnerabilities were identified. Properly configured Guardrails and pre-processing stages effectively mitigate the demonstrated attack chains."
source: "Palo Alto Unit 42"
source_url: "https://unit42.paloaltonetworks.com/amazon-bedrock-multiagent-applications/"
source_date: 2026-04-03T22:00:38+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/39584/censorship-limitations-freedom-of-expression-restricted-39584.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Prompt injection attacks can traverse Amazon Bedrock multi-agent hierarchies, exposing instructions and enabling unauthorized tool invocation."
tldr_who_at_risk: "Organizations deploying Amazon Bedrock multi-agent applications without Guardrails configured are exposed to agent hijacking and sensitive instruction disclosure."
tldr_actions: ["Enable and properly configure Amazon Bedrock's built-in prompt injection Guardrails on all agent pre-processing stages", "Audit inter-agent communication channels and restrict agent tool invocation permissions to least privilege", "Treat all untrusted text inputs to LLM agents as potential adversarial payloads and implement input validation layers"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research"]
tags: ["amazon-bedrock", "multi-agent", "prompt-injection", "agentic-ai", "red-team", "llm-security", "guardrails", "inter-agent-communication", "tool-invocation", "system-prompt-extraction"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-23T04:06:38+00:00"
feed_source: "unit42"
original_url: "https://unit42.paloaltonetworks.com/amazon-bedrock-multiagent-applications/"
pipeline_version: "1.0.0"
---

## Overview

Unit 42 researchers at Palo Alto Networks published red-team findings examining Amazon Bedrock's multi-agent collaboration framework, specifically targeting the attack surface introduced when multiple specialised agents communicate and orchestrate tasks. The research demonstrates a systematic attack chain enabling adversaries to identify agent operating modes, discover collaborator agents, deliver malicious payloads, and ultimately execute unauthorised actions — including extracting system instructions and invoking agent tools with attacker-controlled inputs. No vulnerabilities in Amazon Bedrock itself were identified; the risk stems from the inherent susceptibility of LLMs to prompt injection.

## Technical Analysis

Amazon Bedrock Agents supports two primary multi-agent operating modes: **Supervisor** and **Supervisor with Routing**. Researchers demonstrated that an attacker can fingerprint which mode is active through probing interactions, then progressively enumerate collaborator agents within the architecture.

Once agent topology is mapped, adversaries can inject malicious instructions through untrusted text inputs — such as user-supplied content processed by any agent in the chain. Because LLMs cannot reliably distinguish developer-defined system prompts from adversarial user input, injected instructions can propagate across agent boundaries. The attack chain exploited this to:

- **Disclose agent instructions and tool schemas** — extracting the meta-prompt and API surface of sub-agents
- **Invoke tools with attacker-supplied parameters** — weaponising legitimate action groups (API calls, external integrations) with malicious inputs

The multi-agent architecture amplifies the risk: a single injection point in an orchestrator agent can cascade through subordinate agents, each with their own tool sets and data access, multiplying the blast radius compared to single-agent deployments.

Bedrock's extended agent capabilities — action groups, knowledge bases, memory, and code interpretation — all represent additional lateral movement vectors once an attacker achieves initial prompt injection.

## Framework Mapping

**MITRE ATLAS:** The attack primarily maps to AML.T0051 (LLM Prompt Injection) as the core technique, with AML.T0056 (LLM Meta Prompt Extraction) covering instruction disclosure and AML.T0057 (LLM Data Leakage) covering sensitive schema exfiltration. AML.T0043 (Craft Adversarial Data) describes the payload construction phase.

**OWASP LLM Top 10:** LLM01 (Prompt Injection) is the primary category. LLM08 (Excessive Agency) is directly relevant — agents with broad tool permissions amplify the impact of successful injection. LLM06 (Sensitive Information Disclosure) and LLM07 (Insecure Plugin Design) cover instruction extraction and tool abuse respectively.

## Impact Assessment

Organisations using Amazon Bedrock multi-agent architectures for business-critical workflows — particularly those with action groups connected to internal APIs, databases, or external services — face meaningful risk. A successful attack could result in: exfiltration of proprietary system prompts and tool schemas; unauthorised API calls executed under the agent's IAM permissions; and potential lateral movement through integrated enterprise systems. The impact scales with the privilege level of agent-associated IAM roles and the sensitivity of connected data sources.

## Mitigation & Recommendations

1. **Enable Bedrock Guardrails** — Activate the built-in prompt injection detection on all agent pre-processing stages. Unit 42 confirmed this effectively blocks the demonstrated attack chains.
2. **Apply least privilege to agent IAM roles** — Restrict action group permissions to the minimum necessary; limit which tools each agent can invoke.
3. **Validate and sanitise inputs at every agent boundary** — Do not assume inputs relayed between agents are trusted; treat all inter-agent messages as potentially adversarial.
4. **Audit agent topology exposure** — Minimise information returned when agents describe their own capabilities or collaborator structure to reduce reconnaissance surface.
5. **Deploy layered AI security controls** — Solutions such as Prisma AIRS can provide real-time threat detection and policy enforcement across agent interactions.

## References

- [Unit 42: When an Attacker Meets a Group of Agents — Amazon Bedrock Multi-Agent Applications](https://unit42.paloaltonetworks.com/amazon-bedrock-multiagent-applications/)
