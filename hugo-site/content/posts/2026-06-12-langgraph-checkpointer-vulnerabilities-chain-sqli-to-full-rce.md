---
title: "CVE-2025-67644: LangGraph SQLi to RCE via Checkpointer"
date: "2026-06-12T09:23:45+00:00"
draft: false
slug: "langgraph-checkpointer-vulnerabilities-chain-sqli-to-full-rce"

# ── Content metadata ──
summary: "Check Point Research disclosed three vulnerabilities in LangGraph's persistence layer, two of which chain together to achieve remote code execution: a SQL injection flaw in the SQLite checkpointer (CVE-2025-67644) and an unsafe msgpack deserialization bug (CVE-2026-28277). A third parallel injection vulnerability (CVE-2026-27022) affects the Redis checkpointer. With over 50 million monthly downloads, self-hosted LangGraph deployments exposing user-controlled state history filters are directly at risk."
source: "Check Point Research"
source_url: "https://research.checkpoint.com/2026/from-sqli-to-rce-exploiting-langgraphs-checkpointer/"
source_title: "From SQLi to RCE \u2013 Exploiting LangGraph\u2019s Checkpointer"
source_date: 2026-06-11T13:37:11+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxNHx8TExNJTIwU2VjdXJpdHklMjBjeWJlcnNlY3VyaXR5JTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzgxMDYzODM1fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access", "AML.T0010 - ML Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Three LangGraph checkpointer vulnerabilities chain SQL injection with unsafe deserialization to achieve RCE."
tldr_who_at_risk: "Teams self-hosting LangGraph with SQLite or Redis checkpointers where user input reaches the get_state_history() filter parameter."
tldr_actions: ["Update to langgraph-checkpoint-sqlite 3.0.1+, langgraph 1.0.10+, and langgraph-checkpoint-redis 1.0.2+ immediately", "Audit all application code that passes user-controlled input into get_state_history() or list() filter arguments", "Restrict network access to LangGraph checkpointer backends and apply input validation at the application boundary"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Supply Chain", "Research"]
tags: ["langgraph", "langchain", "sql-injection", "remote-code-execution", "deserialization", "checkpointer", "ai-agents", "cve-2025-67644", "cve-2026-28277", "cve-2026-27022", "sqlite", "redis", "msgpack", "open-source"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-12T08:58:38+00:00"
feed_source: "checkpoint"
original_url: "https://research.checkpoint.com/2026/from-sqli-to-rce-exploiting-langgraphs-checkpointer/"
pipeline_version: "1.0.0"
---

## Overview

Check Point Research has disclosed three vulnerabilities in LangGraph's checkpointer persistence layer, the component responsible for storing and retrieving AI agent execution state. Two of the flaws — a SQL injection (CVE-2025-67644) and an unsafe msgpack deserialization (CVE-2026-28277) — chain together to enable unauthenticated remote code execution on self-hosted deployments. A third vulnerability (CVE-2026-27022) introduces the same injection class into the Redis checkpointer. LangGraph records over 50 million monthly PyPI downloads, making the blast radius significant for teams running their own AI agent infrastructure.

## Technical Analysis

The root cause of CVE-2025-67644 lies in LangGraph's `_metadata_predicate` function, which builds SQL WHERE clauses for checkpoint queries. When the `list()` function is called with a user-supplied `filter` dictionary, the dictionary's **keys** are interpolated directly into a `json_extract()` SQL expression without parameterisation:

```python
predicates.append(
    f"json_extract(CAST(metadata AS TEXT), '$.{query_key}') {operator}"
)
```

Because `query_key` is never sanitised, an attacker who controls the filter argument can inject arbitrary SQLite expressions. SQLite's `writefile()` or similar mechanisms can then be leveraged to write attacker-controlled data to disk.

CVE-2026-28277 escalates the impact to RCE. LangGraph deserialises checkpoint payloads using msgpack without restricting object types. An attacker who can write a malicious checkpoint blob — possible via the SQLi primitive above — can craft a msgpack payload that executes arbitrary Python on deserialisation, completing the exploit chain.

CVE-2026-27022 mirrors the SQLi pattern in the Redis checkpointer, where metadata filter keys are similarly unsanitised before being used in Redis query construction.

## Framework Mapping

- **AML.T0047 (ML-Enabled Product or Service):** The attack surface is the LangGraph agent framework itself; exploitation requires no model access, only interaction with the persistence API.
- **AML.T0010 (ML Supply Chain Compromise):** LangGraph is a foundational dependency for a large portion of the LLM application ecosystem; a vulnerable version in a shared environment propagates risk broadly.
- **LLM05 (Supply Chain Vulnerabilities):** The flaws exist in a widely adopted open-source AI infrastructure package.
- **LLM07 (Insecure Plugin Design):** The checkpointer acts as a plugin/extension to LangChain, and its failure to sanitise inputs exemplifies insecure plugin design at the framework level.

## Impact Assessment

The critical path requires that an attacker control a value passed to `get_state_history()` or `list()` filter parameters — a realistic scenario in multi-tenant or user-facing agent deployments. LangChain's managed LangSmith Deployment (formerly LangGraph Platform) uses PostgreSQL and is confirmed unaffected. Self-hosted deployments using SQLite or Redis checkpointers are the primary risk surface. Successful exploitation yields OS-level code execution on the host running the LangGraph process, with full access to agent memory, secrets, and downstream infrastructure.

## Mitigation & Recommendations

1. **Patch immediately:** Upgrade to `langgraph-checkpoint-sqlite >= 3.0.1`, `langgraph >= 1.0.10`, and `langgraph-checkpoint-redis >= 1.0.2`.
2. **Audit filter inputs:** Identify every call site where user-controlled data reaches `list()` or `get_state_history()` filter arguments and apply strict allowlist validation.
3. **Restrict backend access:** Ensure SQLite files and Redis instances are not network-accessible beyond the application process; apply principle of least privilege to host filesystem permissions.
4. **Consider managed deployment:** LangChain's cloud-managed offering is not vulnerable; teams without the capacity to maintain patched self-hosted infrastructure should evaluate migration.

## References

- [Check Point Research: From SQLi to RCE – Exploiting LangGraph's Checkpointer](https://research.checkpoint.com/2026/from-sqli-to-rce-exploiting-langgraphs-checkpointer/)
