---
title: "AI Gateways Targeted: LiteLLM, RAGFlow, Kestra Compromised"
date: 2026-08-27T10:31:05+00:00
draft: false
slug: "ai-gateways-targeted-litellm-ragflow-kestra-compromised"

# ── Content metadata ──
summary: "Microsoft Security Research documented active intrusions targeting three distinct AI infrastructure components \u2014 a LiteLLM gateway, a RAGFlow retrieval platform, and a Kestra workflow orchestrator \u2014 revealing a pattern of attackers treating AI control planes as high-value targets for credential theft and compute abuse. Across all three cases, attackers converged on the same objectives: stealing model-provider API keys, establishing persistence, and monetising compromised compute resources. The findings signal that AI-specific middleware and orchestration layers require the same security rigour as traditional enterprise critical infrastructure."
source: "Microsoft Security Blog"
source_url: "https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points"
source_title: "When AI infrastructure becomes the target: Securing gateways and control points"
source_date: 2026-08-26T16:43:53+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1758582382409-b3e2254f4b58?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOHx8dGV4dCUyMHR5cG9ncmFwaHklMjBhYnN0cmFjdCUyMGxldHRlcnN8ZW58MHwwfHx8MTc4NzgyNjY2NXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0081 - Modify AI Agent Configuration", "AML.T0040 - AI Model Inference API Access", "AML.T0082 - RAG Credential Harvesting", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0012 - Valid Accounts", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Attackers compromised LiteLLM, RAGFlow, and Kestra deployments to steal AI credentials and hijack compute."
tldr_who_at_risk: "Organisations running self-hosted AI gateways, RAG platforms, or workflow orchestrators are exposed due to their concentration of model API keys, database access, and execution privileges."
tldr_actions: ["Inventory all AI management surfaces including gateways, RAG backends, and orchestration services", "Rotate and vault all model-provider API keys and virtual proxy keys immediately", "Restrict administrative access to AI infrastructure using least-privilege and network segmentation"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Supply Chain", "Research"]
tags: ["litellm", "ragflow", "kestra", "ai-gateway", "credential-theft", "ai-infrastructure", "llm-proxy", "compute-abuse", "cryptomining", "persistence", "microsoft-security", "rag-security", "workflow-orchestration", "api-key-theft", "control-plane-attack"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-27T10:31:05+00:00"
feed_source: "microsoft_security"
original_url: "https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points"
pipeline_version: "2.1.0"
---

## Overview

Microsoft Security Research has published findings from active intrusion investigations targeting three AI infrastructure components: a LiteLLM API gateway, a RAGFlow retrieval-augmented generation platform, and a Kestra workflow orchestration environment. Published in August 2026, the report identifies a consistent attacker pattern across these otherwise distinct workloads — threat actors are treating AI middleware as a privileged control plane, seeking credentials, persistence, and monetisable compute rather than targeting AI model outputs directly.

The significance of this shift is substantial. While much AI security discourse has focused on prompt injection and model manipulation, these cases demonstrate that the infrastructure *surrounding* AI — the gateways, retrieval stores, and orchestrators — represents an equally critical and increasingly targeted attack surface.

## Technical Analysis

Each compromised workload served a different architectural function, but all three exposed assets enabling follow-on abuse:

- **LiteLLM gateway**: Concentrates model-provider API keys and proxy-issued virtual keys. Compromise grants attackers the ability to make authenticated requests to upstream LLM providers, enabling API key theft and unauthorised inference at the organisation's expense.
- **RAGFlow deployment**: Stores database connection strings, indexed document content, and tenant configuration. Attacker access enables credential harvesting from the retrieval backend and potential exfiltration of sensitive embedded documents.
- **Kestra workflow environment**: Provides workflow execution privileges and host compute access. Post-compromise behaviour here focused on establishing persistence and monetising compute resources, consistent with cryptomining or infrastructure resale campaigns.

Intrusion paths varied across cases, but post-compromise objectives converged: steal credentials, establish persistence, and abuse compute. Microsoft noted that the broader campaign-level pattern — targeting AI management surfaces specifically — is more significant than any individual technique.

## Framework Mapping

The attack pattern maps directly to several ATLAS and OWASP categories. **AML.T0083** (Credentials from AI Agent Configuration) and **AML.T0082** (RAG Credential Harvesting) are directly observed. **AML.T0084** (Discover AI Agent Configuration) captures the reconnaissance phase. **AML.T0040** (AI Model Inference API Access) reflects the LiteLLM exploitation objective. From an OWASP perspective, **LLM06** (Sensitive Information Disclosure) applies to API key and connection string exposure, while **LLM07** (Insecure Plugin Design) and **LLM08** (Excessive Agency) reflect the risk of over-privileged AI infrastructure components.

## Impact Assessment

Organisations running self-hosted AI orchestration stacks face compounded risk: a single compromised gateway can yield model-provider credentials, downstream data access, and host-level execution. Financial impact includes unauthorised LLM API spend and potential data exfiltration. The threat is particularly acute for enterprises that have deployed AI infrastructure rapidly without applying the same access controls and monitoring used for traditional critical systems.

## Mitigation & Recommendations

- **Inventory AI management surfaces**: Map all gateways, RAG backends, orchestrators, and containerised runtimes to understand the credential and execution attack surface.
- **Rotate and vault credentials**: Treat LLM API keys, virtual proxy keys, and database connection strings as high-value secrets; store in dedicated secret managers with automatic rotation.
- **Apply least-privilege access**: Restrict administrative interfaces to AI infrastructure using network segmentation, RBAC, and MFA.
- **Monitor for anomalous inference spend**: Alert on unexpected spikes in model API usage that may indicate credential abuse.
- **Harden container runtimes**: Apply runtime security controls and image scanning to containerised AI workloads.

## References

- [Microsoft Security Blog — When AI infrastructure becomes the target](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points)
