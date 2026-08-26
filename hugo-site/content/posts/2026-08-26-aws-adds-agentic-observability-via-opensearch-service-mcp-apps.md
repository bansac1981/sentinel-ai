---
title: "AWS Adds Agentic Observability via OpenSearch Service MCP Apps"
date: "2026-08-26T07:49:27+00:00"
draft: false
slug: "aws-adds-agentic-observability-via-opensearch-service-mcp-apps"

# ── Content metadata ──
summary: "AWS has released agentic observability tooling through Amazon OpenSearch Service MCP Apps, providing structured visibility into the actions, tool invocations, and decision traces of AI agents running on AWS infrastructure. This closes a meaningful gap for defenders who previously lacked native, queryable telemetry over agent behaviour \u2014 a prerequisite for detecting anomalous tool use, privilege escalation patterns, and unexpected data access in agentic pipelines. Realising the full defensive value will require mature logging schemas, tuned detection rules, and integration with existing SIEM or SOAR tooling that most organisations are still building."
source: "AWS Machine Learning Blog"
source_url: "https://aws.amazon.com/blogs/machine-learning/agentic-observability-with-amazon-opensearch-service-mcp-apps"
source_title: "Agentic observability with Amazon OpenSearch Service MCP Apps"
source_date: 2026-08-25T19:00:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1730303055577-c8bdba043b19?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxNXx8QXdzJTIwcGlwZWxpbmUlMjB3b3JrZmxvdyUyMGF1dG9tYXRpb24lMjBhYnN0cmFjdHxlbnwwfDB8fHwxNzg3NzI5MTY3fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 5.5
adoption_velocity: "MODERATE"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Native structured telemetry over AI agent tool invocations, enabling defenders to baseline and alert on anomalous agent actions", "Queryable agent decision traces via OpenSearch, allowing security teams to investigate agent behaviour post-incident or in near-real-time", "Centralised observability plane for agentic workflows, reducing blind spots in multi-step agent pipelines that previously produced no audit trail", "MCP (Model Context Protocol) integration surface for correlating agent context with tool calls, supporting detection of context poisoning or unexpected lateral movement"]

# ── AI Security Classification ──
relevance_score: 5.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0084 - Discover AI Agent Configuration", "AML.T0080 - AI Agent Context Poisoning", "AML.T0081 - Modify AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0110 - AI Agent Tool Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "AWS ships agentic observability for AI agents via Amazon OpenSearch Service MCP Apps."
tldr_who_at_risk: "Security teams operating AI agents on AWS who lack structured telemetry over agent tool invocations and decision paths now have a native observability surface to close that gap."
tldr_actions: ["Enable OpenSearch MCP App logging for all production agentic workloads on AWS Bedrock and connected agent frameworks", "Define baseline alert rules on anomalous tool invocation patterns — particularly unexpected data access, credential retrieval, or multi-step lateral calls", "Integrate OpenSearch agent telemetry with your existing SIEM to correlate agent behaviour against broader threat detections"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News"]
tags: ["aws", "opensearch", "agentic-ai", "observability", "mcp", "model-context-protocol", "agent-telemetry", "tool-invocation", "audit-trail", "amazon-bedrock", "agent-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-26T07:26:07+00:00"
feed_source: "aws_ml"
original_url: "https://aws.amazon.com/blogs/machine-learning/agentic-observability-with-amazon-opensearch-service-mcp-apps"
pipeline_version: "2.1.0"
---

## Defender Impact

AI agents operating without structured observability are effectively a black box to security teams — actions are taken, tools are invoked, and data is accessed with no reliable audit trail. AWS's release of agentic observability via Amazon OpenSearch Service MCP Apps provides a native, queryable telemetry layer specifically designed for agentic workflows, closing one of the most persistent blind spots in enterprise AI deployments today.

## Capability Overview

Amazon OpenSearch Service MCP Apps introduces observability tooling built around the Model Context Protocol (MCP), an emerging standard for how AI agents communicate context and invoke tools. The capability appears to provide structured logging of agent interactions — capturing tool invocations, context passed between agent steps, and the decision traces that link a user prompt to a sequence of downstream actions.

By routing this telemetry through OpenSearch, defenders gain a familiar, high-performance query and analytics layer over agent behaviour. OpenSearch's existing strengths in log aggregation, anomaly detection, and dashboard visualisation are now extended to the agentic surface — meaning teams who already operate OpenSearch for infrastructure and application monitoring can onboard agent telemetry without standing up a separate toolchain.

The MCP integration is particularly significant. As MCP gains traction as a standard for agent-tool communication across AWS Bedrock and third-party agent frameworks, a telemetry layer built natively on MCP events positions this capability to scale across heterogeneous agent deployments rather than being confined to a single AWS-native agent runtime.

## Defensive Advances

**Audit trail for agent tool invocations.** For the first time on AWS, defenders can query a structured record of which tools an agent called, in what order, with what arguments, and what was returned — the foundation for both incident investigation and proactive detection rule development.

**Behavioural baselining for agentic pipelines.** With queryable telemetry, security teams can establish normal operating patterns for specific agent workflows and define alerts on deviations — unexpected data source access, unusually long tool chains, or calls to credential-adjacent APIs that fall outside expected scope.

**Post-incident forensics capability.** Previously, reconstructing what an AI agent did during a security incident required piecing together fragmented application logs. Centralised agent observability through OpenSearch provides a coherent forensic timeline, materially improving mean time to understand (MTTU) after an anomalous agent event.

**Correlation with broader SIEM pipelines.** Because the telemetry lands in OpenSearch, it can be forwarded into existing SIEM tooling alongside infrastructure and identity logs, enabling defenders to correlate agent behaviour with network, IAM, and data access events in a unified investigation context.

## Residual Gaps

The value of this capability is directly proportional to the completeness of what gets logged — and that depends on how thoroughly MCP instrumentation is implemented across the agent frameworks an organisation uses. Agents built outside AWS-native tooling may require custom instrumentation to emit MCP-compatible telemetry, and coverage will be uneven in early adoption.

Detection rule libraries for agentic telemetry are immature across the industry. Teams adopting this capability will initially need to write bespoke detection logic rather than importing proven rule sets, which requires both operational investment and a period of baseline learning before alerts become reliable.

The capability does not appear to address agent identity or authorisation verification — observability tells you what happened, not whether the agent was legitimately authorised to do it. Complementary controls around agent identity, least-privilege tool scoping, and runtime policy enforcement remain necessary and are not substituted by telemetry alone.

## Framework Mapping

This capability most directly supports defender visibility against **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** and **AML.T0080 (AI Agent Context Poisoning)** by creating a record of tool calls and context flows that would surface anomalous exfiltration patterns or unexpected context injection. It also aids detection of **AML.T0098 (AI Agent Tool Credential Harvesting)** by making credential-adjacent tool invocations visible and queryable. Against OWASP LLM Top 10, this most directly reduces blind spots associated with **LLM08 (Excessive Agency)** and **LLM06 (Sensitive Information Disclosure)**.

## Deployment Considerations

Organisations should prioritise enabling agent telemetry on agentic workflows with the broadest tool access first — those with access to data stores, external APIs, or IAM-adjacent capabilities represent the highest-value monitoring surface. Teams should expect a 4–8 week baseline period before anomaly thresholds are meaningfully tunable. Existing OpenSearch deployments can be extended incrementally; net-new OpenSearch deployments should be scoped alongside SIEM integration from day one to avoid duplicate pipelines.

## Defender Checklist

- [ ] Inventory all production agentic workloads on AWS and identify which use MCP-compatible frameworks
- [ ] Enable OpenSearch MCP App telemetry collection for highest-risk agent pipelines first
- [ ] Define a logging schema that captures: tool name, arguments, response, agent step sequence, and invoking identity
- [ ] Establish baseline alert rules for anomalous tool invocation patterns (unexpected data access, credential API calls, unusually long chains)
- [ ] Configure OpenSearch telemetry forwarding to your SIEM for cross-surface correlation
- [ ] Review and scope agent tool permissions in parallel — observability surfaces gaps but does not enforce least privilege
- [ ] Document agent forensic runbooks using the new telemetry structure before an incident requires them

## References

- [Agentic observability with Amazon OpenSearch Service MCP Apps — AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/agentic-observability-with-amazon-opensearch-service-mcp-apps)
