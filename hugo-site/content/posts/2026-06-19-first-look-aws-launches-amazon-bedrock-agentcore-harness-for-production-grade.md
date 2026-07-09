---
title: "AWS Launches Amazon Bedrock AgentCore Harness"
date: "2026-06-19T07:54:42+00:00"
draft: false 
slug: "first-look-aws-launches-amazon-bedrock-agentcore-harness-for-production-grade"

# ── Content metadata ──
summary: "AWS has made Amazon Bedrock AgentCore Harness generally available, providing a managed abstraction layer that reduces agent deployment to two API calls while bundling sandboxed compute, persistent memory, tool gateway, browser access, identity management, and observability. For defenders, this dramatically lowers the barrier to deploying autonomous agents with filesystem access, shell execution, web browsing, and multi-provider model switching \u2014 compressing what was a weeks-long infrastructure project into minutes. Security teams face an expanded attack surface where prompt injection, tool abuse, cross-session memory poisoning, and supply chain risks through AWS-curated skill catalogs now arrive as a single, tightly integrated managed service rather than individually reviewable components."
source: "AWS Machine Learning Blog"
source_url: "https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-harness-is-now-generally-available-go-from-idea-to-production-grade-agent-in-minutes/"
source_title: "Amazon Bedrock AgentCore harness is now generally available: Go from idea to production-grade agent in minutes"
source_date: 2026-06-18T17:32:22+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/8566527/pexels-photo-8566527.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 7.8
adoption_velocity: "RAPID"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Prompt injection via web browser capability: agents that can browse arbitrary URLs are directly exposable to attacker-controlled pages containing adversarial instructions", "Cross-session memory poisoning: persistent memory across user sessions creates a vector where poisoned inputs in one session can influence agent behaviour in future sessions for the same or other users", "Tool/skill supply chain compromise: AWS-curated skill catalog and MCP/gateway-connected tools introduce a dependency chain where a compromised or malicious skill can be injected at the catalog level and affect all harness deployments pointing to it", "Sandboxed compute escape risk: the harness provides each agent a filesystem and shell environment; any vulnerability in the sandbox boundary or misconfigured isolation could allow lateral movement into the host or adjacent tenant environments", "Dynamic model provider switching mid-session: the ability to override the model on any InvokeHarness call without losing context creates a vector where an attacker with partial API access can redirect agent reasoning to a less-safe or attacker-controlled model endpoint", "Identity and IAM abuse via managed identity primitive: the bundled identity layer may inherit over-permissive IAM roles; agents operating with elevated AWS credentials could be weaponised to exfiltrate data or pivot within the AWS environment", "Excessive agency through simplified deployment: the two-API-call deployment model encourages rapid production rollout without security review gates, increasing the likelihood of agents with over-broad tool permissions reaching production", "Observability gap exploitation: real-time streaming and CloudWatch tracing, while beneficial, create a secondary attack surface — an attacker who gains read access to trace logs receives a detailed map of agent reasoning, tool calls, and potentially sensitive intermediate outputs"]

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0057 - LLM Data Leakage", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "AWS makes AgentCore Harness generally available, enabling production agents via two API calls with built-in shell, memory, browser, and tool access."
tldr_who_at_risk: "Organisations deploying or exposed to AgentCore-powered agents, particularly those connecting agents to internal tools, AWS resources, or external web content."
tldr_actions: ["Audit IAM roles attached to AgentCore harness deployments for least-privilege and scope creep before production rollout", "Treat all browser-accessible URLs and MCP-connected tool outputs as untrusted; implement prompt injection detection at the gateway layer", "Review the AWS-curated skill catalog entries in use and establish a vetting process before adding new skills to production harnesses"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Prompt Injection", "Supply Chain"]
tags: ["aws", "amazon-bedrock", "agentcore", "agent-harness", "managed-agents", "tool-use", "prompt-injection", "memory-poisoning", "supply-chain", "sandbox-escape", "iam-abuse", "mcp", "multi-model-switching", "agentic-ai", "production-agents"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "insider", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-19T07:19:00+00:00"
feed_source: "aws_ml"
original_url: "https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-harness-is-now-generally-available-go-from-idea-to-production-grade-agent-in-minutes/"
pipeline_version: "2.0.0"
---

## Capability Overview

Amazon Bedrock AgentCore Harness reached general availability on 18 June 2026, collapsing the multi-week infrastructure work of production agent deployment into two API calls: `CreateHarness` and `InvokeHarness`. The service bundles every major agent primitive — sandboxed compute with a real filesystem and shell, persistent cross-session memory, a tool gateway supporting MCP and custom integrations, a managed web browser, an identity layer, and CloudWatch-backed observability — into a single managed abstraction.

For defenders, the key signal is not what AWS built, but what this makes trivially easy for developers who previously lacked the infrastructure expertise to deploy agents safely. The compression of deployment complexity is real; so is the compression of the security review window.

## Attack Surface Analysis

**Browser-enabled prompt injection** is the most immediately exploitable vector. Agents with web browsing capability will routinely fetch attacker-controlled content. A single malicious page containing adversarial instructions in visible or hidden text can redirect the agent's actions, exfiltrate memory contents, or cause it to invoke tools on behalf of an attacker. This is not theoretical — it is the dominant attack pattern against every browser-capable agent deployed to date.

**Cross-session memory poisoning** is a slower but higher-impact vector. The harness persists memory across sessions by design. An attacker who can influence a single agent interaction — through a phishing-crafted input, a poisoned tool response, or a malicious file — can plant instructions that surface in future sessions, potentially for different users if memory is shared at the harness level rather than the user level.

**Skill catalog supply chain risk** mirrors the npm/PyPI threat model. The AWS-curated catalog is a centralised dependency layer. A compromised or maliciously submitted skill propagates silently to every harness pointing at it, with no diff review unless teams have explicitly locked skill versions.

**Mid-session model switching** introduces a novel vector: an attacker with write access to InvokeHarness parameters can redirect reasoning to a less-aligned or attacker-controlled model endpoint without terminating the session, preserving accumulated context while substituting the reasoning engine.

**IAM over-provisioning** is the ambient risk. The harness identity primitive will, in practice, inherit whatever role a developer assigns during setup. Agents with shell access and over-broad IAM roles become a lateral movement path into the broader AWS environment.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **LLM01**: Browser and MCP tool outputs are direct injection surfaces.
- **AML.T0010 (ML Supply Chain Compromise)** and **LLM05**: The skill catalog and MCP server dependencies are untrusted third-party inputs.
- **AML.T0057 (LLM Data Leakage)** and **LLM06**: Persistent memory and CloudWatch traces may contain PII or confidential intermediate reasoning.
- **LLM08 (Excessive Agency)**: The harness's shell and filesystem access, combined with rapid deployment, is a textbook excessive agency scenario.
- **AML.T0012 (Valid Accounts)**: Compromised AWS credentials can invoke harnesses at scale, consuming resources or exfiltrating agent outputs.

## Threat Scenarios

**Scenario 1 — Indirect Prompt Injection via Web Research Task:** A user asks a customer-facing AgentCore agent to research a competitor. The agent browses an attacker-seeded page containing hidden instructions to exfiltrate the current session's memory contents to an external endpoint via a tool call.

**Scenario 2 — Persistent Memory Backdoor:** A red-teamer crafts an input that causes the agent to write a persistent "instruction" into long-term memory under a plausible key. All subsequent sessions for that user — or harness-wide if memory scoping is misconfigured — execute the backdoored instruction silently.

**Scenario 3 — Skill Catalog Sideloading:** An attacker publishes a skill to the AWS marketplace that mimics a legitimate data-processing tool. Organisations that pull skills without version-locking receive the malicious variant on next deployment, granting the skill shell-level access within the sandbox.

## Defender Checklist

- [ ] Enforce least-privilege IAM roles on every harness; treat the agent identity as a service account, not a developer account
- [ ] Block or proxy all outbound browser requests; apply content inspection to web-fetched content before it enters the agent context
- [ ] Isolate memory at the user level, not the harness level; audit memory scoping configuration in CreateHarness definitions
- [ ] Pin skill catalog versions; establish an internal review gate before approving new skills for production harnesses
- [ ] Apply prompt injection detection middleware at the gateway layer for all tool inputs and outputs
- [ ] Restrict InvokeHarness model-override parameters via IAM condition keys to prevent unauthorised model substitution
- [ ] Treat CloudWatch agent traces as sensitive data; apply appropriate access controls and retention policies
- [ ] Require security review sign-off before any harness moves from prototype to production, regardless of deployment speed

## References

- [Amazon Bedrock AgentCore Harness GA Announcement](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-harness-is-now-generally-available-go-from-idea-to-production-grade-agent-in-minutes/)
