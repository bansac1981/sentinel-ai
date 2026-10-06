---
title: "MCP Marketplace Security Gap Exposes 15,465 Public Servers"
date: 2026-10-06T12:10:53+00:00
draft: true
slug: "mcp-marketplace-security-gap-exposes-15465-public-servers"

# ── Content metadata ──
summary: "OX Security analysed 15,465 publicly indexed MCP servers across five registries and found zero centralised vetting, code signing, or origin verification. Servers hosted in China and Russia, dangling domains ripe for hijacking, and infrastructure running on personal machines via consumer tunnels represent uncontrolled data-exfiltration paths for any enterprise agent workflow. The research includes a prompt-injection proof-of-concept, underscoring that the trust model baked into MCP deployments is itself the primary attack surface."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/10/welcome-to-jungle-what-we-found-inside.html"
source_title: "Welcome to the Jungle: What We Found Inside 15,465 Public MCP Servers"
source_date: 2026-10-06T11:02:30+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1641932269834-af141d2c2017?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxN3x8U3VwcGx5JTIwQ2hhaW4lMjBjeWJlcnNlY3VyaXR5JTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzkxMjg4NjUyfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0051 - LLM Prompt Injection", "AML.T0080 - AI Agent Context Poisoning", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0109 - AI Supply Chain Rug Pull", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "OX Security found 15,465 public MCP servers have zero governance, vetting, or code signing."
tldr_who_at_risk: "Enterprises running AI agent workflows that connect to community MCP servers are exposed to unvetted, potentially malicious backend code and data exfiltration to unapproved jurisdictions."
tldr_actions: ["Audit all MCP server connections and block those resolving to non-approved jurisdictions or consumer tunnel services", "Implement allowlisting for MCP server hostnames and enforce code-signing verification before agent integration", "Monitor for dangling or recently re-registered MCP domains that legacy agents may still be calling"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Prompt Injection", "Research"]
tags: ["mcp", "model-context-protocol", "supply-chain", "agentic-ai", "prompt-injection", "dangling-domains", "data-exfiltration", "ai-agent-security", "registry-security", "ox-security", "llm-tooling", "infrastructure-risk"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-10-06T12:10:53+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/10/welcome-to-jungle-what-we-found-inside.html"
pipeline_version: "2.1.0"
---

## Overview

OX Security's latest research exposes a systemic governance vacuum in the Model Context Protocol (MCP) ecosystem. After scanning 15,465 publicly indexed MCP servers across five major registries — deduplicated to 5,095 unique hostnames — the team found no mandatory vetting, no code signing, and no origin verification in any marketplace. MCP was designed as the connective tissue between AI models, agents, and external tools; that same connectivity now creates an uncontrolled data-flow path into enterprise environments.

## Technical Analysis

Three categories of infrastructure risk emerged from the scan:

**Offshore hosting:** 15.6% of hostnames resolve to infrastructure outside the United States, with 19 resolving to Chinese IP space and 18 to Russian IP space. Any AI agent configured to call these servers may transmit sensitive context — including credentials, user data, and internal tool outputs — to jurisdictions outside approved data-residency boundaries.

**Consumer tunnel exposure:** 0.45% of servers route traffic through services such as ngrok-free, meaning they run on personal machines and likely home networks. These servers are publicly listed in registries as though they were production infrastructure, with no indication of their transient, consumer-grade nature.

**Dangling domain hijacking:** 2.3% of servers no longer resolve, and six sit on expired domains available for $4–$12. Any attacker registering one of these domains inherits an established server identity. Agents still configured to call that endpoint would silently begin routing requests — and potentially sensitive data — to the new owner.

The research also notes a deeper architectural problem: remote MCP servers can run backend code that differs entirely from their public repository. Code review of a published server does not reveal what the live server actually executes, eliminating the primary defence developers currently rely on.

A prompt-injection proof-of-concept is included in the full report, demonstrating that malicious MCP servers can inject instructions into agent context windows to manipulate downstream behaviour.

## Framework Mapping

- **AML.T0010 / AML.T0115 (AI Supply Chain Compromise / Publish Poisoned AI Artifacts):** Community registries with no review allow adversaries to publish servers whose runtime behaviour differs from their source code.
- **AML.T0109 (AI Supply Chain Rug Pull):** Dangling domain takeover is a textbook rug-pull scenario — a trusted endpoint silently changes ownership.
- **AML.T0051 (LLM Prompt Injection):** The included PoC confirms malicious servers can inject adversarial instructions into agent pipelines.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation):** Agents calling offshore or hijacked servers exfiltrate data as a side-effect of normal tool use.
- **LLM05 (Supply Chain Vulnerabilities) / LLM07 (Insecure Plugin Design):** MCP servers function as plugins with no mandatory security baseline.

## Impact Assessment

Enterprises that have integrated community MCP servers into agent workflows face immediate data-sovereignty, confidentiality, and integrity risks. Security teams that built Zero Trust boundaries around SaaS and public cloud have no equivalent controls for MCP connections. The risk is not hypothetical — dangling domains are actionable today for single-digit dollar costs.

## Mitigation & Recommendations

1. **Enforce an MCP server allowlist** — only permit agents to call servers on an approved, internally reviewed list.
2. **Block consumer tunnel endpoints** — filter or alert on hostnames resolving through ngrok, Cloudflare Tunnel free tier, and equivalent services.
3. **Monitor domain registration for legacy MCP endpoints** — use domain-monitoring services to detect re-registration of any previously used server domains.
4. **Require internal proxying** — route all MCP traffic through a controlled egress point that can enforce data-residency and logging policies.
5. **Treat MCP servers as third-party software** — apply the same supply-chain due diligence (SBOM, code review, runtime monitoring) applied to other dependencies.

## References

- [Welcome to the Jungle: What We Found Inside 15,465 Public MCP Servers — The Hacker News](https://thehackernews.com/2026/10/welcome-to-jungle-what-we-found-inside.html)
