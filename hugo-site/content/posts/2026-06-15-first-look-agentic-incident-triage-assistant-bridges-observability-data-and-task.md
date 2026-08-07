---
title: "Amazon Quick Launches Agentic Incident Triage Assistant"
date: "2026-06-16T01:43:14+00:00"
draft: false 
slug: "first-look-agentic-incident-triage-assistant-bridges-observability-data-and-task"

# ── Content metadata ──
summary: "Amazon Quick's agentic incident triage assistant integrates New Relic's observability platform and Asana via MCP, creating a single conversational interface that autonomously queries production telemetry, surfaces error logs, and creates tracked tasks \u2014 compressing what previously required multiple context-switches into a single engineer prompt. For SRE and platform engineering teams, this closes a meaningful gap between evidence gathering and incident handoff, reducing the cognitive load and elapsed time during high-pressure triage. Teams adopting this architecture should pair it with input sanitisation controls and least-privilege connector scoping to ensure the agent's autonomous reasoning operates over validated data."
source: "AWS Machine Learning Blog"
source_url: "https://aws.amazon.com/blogs/machine-learning/build-an-agentic-incident-triage-assistant-with-amazon-quick-and-new-relic/"
source_title: "Build an agentic incident triage assistant with Amazon Quick and New Relic"
source_date: 2026-06-09T16:10:37+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1618060932014-4deda4932554?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw5fHxGaXJzdCUyMExvb2slMjBjeWJlcnNlY3VyaXR5JTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzgxNTMwMzc3fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 7.5
adoption_velocity: "MODERATE"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Unified observability-to-action pipeline: defenders can now move from alert to structured RCA task in a single automated workflow, reducing the window between detection and documented response that previously relied on manual cross-platform coordination", "Structured log and telemetry reasoning at scale: the analyze_entity_logs, analyze_transactions, and generate_alert_insights_report tools give defenders systematic, repeatable analysis of high-volume telemetry that would otherwise require manual triage — surfacing signal that human reviewers under pressure are likely to miss", "Natural-language NRQL query generation: the natural_language_to_nrql_query tool lowers the barrier for SREs to query production observability data during incidents without requiring deep NRQL expertise, accelerating time-to-insight for a broader range of responders", "Automated, auditable incident handoff: agent-generated Asana tasks with embedded RCA briefs create a consistent, traceable handoff artifact that replaces ad-hoc Slack threads or verbal handoffs, improving post-incident review quality", "Multi-connector orchestration as a force multiplier: by connecting New Relic and Asana through a single authenticated agent session, defenders gain a coordinated response capability that keeps observability context and task tracking in sync without manual translation between platforms"]

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Amazon Quick agentic assistant connects production observability data to autonomous task creation, creating an indirect prompt injection pathway through live telemetry."
tldr_who_at_risk: "SRE and platform engineering teams operating at scale benefit most from this capability \u2014 particularly those managing high alert volumes where manual triage creates bottlenecks, context loss between tools, and inconsistent incident documentation."
tldr_actions:
  - "Integrate the Amazon Quick agentic triage assistant into your incident response runbooks as the primary triage interface for New Relic-instrumented services, mapping it to your existing Asana incident project boards"
  - "Configure connector permissions at deployment time using least-privilege scoping — New Relic read-only access limited to relevant service entities, Asana write access scoped to designated incident boards — so the agent operates with production-appropriate authority from day one"
  - "Establish an input validation layer for telemetry ingested by the agent and define a human-review step for agent-generated RCA briefs before tasks are actioned, building oversight into the workflow rather than retrofitting it later"

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "Prompt Injection", "LLM Security"]
tags: ["amazon-quick", "new-relic", "mcp", "incident-triage", "agentic-ai", "prompt-injection", "observability", "asana", "sre", "multi-tool-agent", "indirect-prompt-injection", "production-telemetry"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "insider", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-06-15T14:03:29+00:00"
feed_source: "aws_ml"
original_url: "https://aws.amazon.com/blogs/machine-learning/build-an-agentic-incident-triage-assistant-with-amazon-quick-and-new-relic/"
pipeline_version: "2.0.0"
---

## Defender Impact

Amazon Quick's agentic incident triage assistant compresses the evidence-gathering, synthesis, and handoff stages of incident response into a single automated workflow — closing the gap between alert firing and structured, documented triage that has historically depended on manual coordination across disconnected tools.

## Capability Overview

Amazon Quick has shipped a reference architecture for an agentic incident triage assistant that wires together New Relic's observability platform (via MCP Server) and Asana through native connectors. From a single engineer prompt, the agent autonomously calls five New Relic reasoning tools: log analysis, alert insights, user impact assessment, transaction analysis, and natural-language NRQL query generation. It then synthesises an RCA brief and creates a tracked Asana task. The entire evidence-gathering and handoff lifecycle is delegated to the agent.

The architecture's significance for defenders is the consolidation of two planes that are usually manually bridged: read access to live observability telemetry and write access to project management systems, with the LLM as the reasoning layer connecting them. An SRE who previously had to query New Relic, interpret logs, assess user impact, draft a summary, and then file a task — across multiple context switches under time pressure — can now initiate that full sequence from a single conversational prompt.

The `natural_language_to_nrql_query` tool is particularly notable for platform teams. It lowers the NRQL expertise barrier, allowing a broader range of responders to query production observability data precisely during the moments when speed and accuracy matter most. The multi-connector model means that the context assembled during triage — service topology, error rates, affected transactions — flows directly into the Asana task artifact rather than being summarised imprecisely in a handoff message.

## Defensive Advances

This architecture gives defenders several concrete capabilities they previously lacked or had to build manually:

- **Systematic telemetry reasoning at scale.** The `analyze_entity_logs` and `analyze_transactions` tools apply consistent analytical reasoning to high-volume log and trace data, surfacing signal that fatigued human reviewers are liable to miss during major incidents.
- **Consistent incident documentation.** Agent-generated RCA briefs tied directly to the telemetry evidence replace ad-hoc summaries, improving the quality and comparability of post-incident reviews.
- **Faster, lower-friction observability queries.** Natural-language NRQL generation democratises access to production data during incidents, reducing dependence on specialists.
- **Automated, auditable handoff artifacts.** Asana tasks generated by the agent carry structured RCA content, creating a traceable record of what was known, when, and by what reasoning path.

## Residual Gaps

The architecture as described does not yet specify input validation controls for telemetry ingested by the agent. Application logs, alert payloads, and transaction traces are high-volume, partially external-influenced data sources; without a sanitisation layer between raw telemetry and the LLM reasoning step, the agent's conclusions are only as reliable as its inputs. Teams should treat this as a maturity requirement to address at deployment, not a reason to defer adoption.

NRQL query scope constraints are also not addressed in the reference architecture. Without allowlisting or service-boundary enforcement, queries could return data outside the incident's intended scope — a coverage gap that matters for organisations with strict data compartmentalisation requirements.

Finally, the multi-connector credential model — a single Amazon Quick Professional-tier session authenticated to both New Relic and Asana — warrants session token protection practices commensurate with the combined access it represents. This is a standard operational maturity question for any multi-platform integration, not unique to this architecture.

## Framework Mapping

**AML.T0051 (LLM Prompt Injection)** and **LLM01 (Prompt Injection)** are the technique categories this deployment should be hardened against through input validation — the architecture's telemetry ingestion pipeline is the surface to protect. **AML.T0057 (LLM Data Leakage)** and **LLM06 (Sensitive Information Disclosure)** frame the data governance controls needed around RCA brief outputs. **LLM08 (Excessive Agency)** informs the case for human review gates on agent-generated tasks — a maturity control that keeps autonomous write actions accountable. **LLM07 (Insecure Plugin Design)** provides the design standard against which the MCP Server integration should be evaluated, particularly around tool input validation.

## Deployment Considerations

Teams integrating this assistant into production incident response should consider three operational factors:

**Telemetry trust boundaries.** The agent reasons over logs and traces that may include externally influenced content. Establishing a validation or filtering layer before telemetry reaches the LLM reasoning step is the primary maturity requirement for production deployment.

**NRQL scope governance.** Define query scope constraints appropriate to your service topology before enabling the `natural_language_to_nrql_query` tool broadly. Allowlisting query patterns or enforcing service-boundary filters ensures the agent's observability access matches its intended incident scope.

**RCA brief review cadence.** For high-sensitivity production environments, build a human review step into the workflow for agent-generated Asana tasks before they are actioned. This is most valuable for RCA briefs involving external-facing services where the incident narrative may inform customer communications.

## Defender Checklist

- [ ] Map the assistant to your existing incident response runbooks and identify which New Relic-instrumented services to onboard first
- [ ] Configure New Relic connector access as read-only and scoped to relevant service entities at deployment time
- [ ] Limit Asana write access to designated incident project boards from day one
- [ ] Implement a telemetry input validation layer before logs and traces reach the LLM reasoning step
- [ ] Define NRQL query scope constraints or allowlists appropriate to your service boundary requirements
- [ ] Establish a human review step for agent-generated RCA briefs in high-sensitivity production workflows
- [ ] Enable immutable audit logging for all agent tool calls and outputs to support post-incident forensic review
- [ ] Apply session token protection practices to Amazon Quick connector credentials commensurate with their combined observability and task management access

## References

- [Build an agentic incident triage assistant with Amazon Quick and New Relic — AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/build-an-agentic-incident-triage-assistant-with-amazon-quick-and-new-relic/)
