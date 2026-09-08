---
title: "TeamPCP Agents Harvest Thousands of AI Credentials in Six Hours"
date: 2026-09-08T18:31:51+00:00
draft: true
slug: "teampcp-agents-harvest-thousands-of-ai-credentials-in-six-hours"

# ── Content metadata ──
summary: "A financially motivated threat actor, TeamPCP, deployed an autonomous multi-agent attack framework to compromise thousands of credentials in under six hours, targeting AI coding assistants, LLM security tools, and cloud environments. The campaign leveraged two evolving credential stealers\u2014SANDCLOCK and its successor DUSTMAKER\u2014with DUSTMAKER introducing AI-specific techniques including poisoning of AI assistant workspaces and prompt injection for defense evasion. Google Threat Intelligence Group warns this marks a significant escalation in adversarial use of agentic AI, producing attack speeds that outpace conventional incident response."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/autonomous-ai-agents-compromise.html"
source_title: "Autonomous AI Agents Compromise Thousands of Credentials in Under Six Hours"
source_date: 2026-09-08T13:48:16+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1524514587686-e2909d726e9b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxtZWNoYW5pY2FsJTIwZ2VhcnMlMjBpbnRlcmxvY2tpbmclMjBtYWNoaW5lfGVufDB8MHx8fDE3ODg4OTIzMTF8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0010 - AI Supply Chain Compromise", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0103 - Deploy AI Agent", "AML.T0080 - AI Agent Context Poisoning", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "TeamPCP's autonomous AI agent framework harvested thousands of credentials from AI coding tools in six hours."
tldr_who_at_risk: "Developers using AI coding assistants, CI/CD pipelines, and organisations operating cloud-hosted LLM workloads are most directly exposed due to targeted credential stealers."
tldr_actions: ["Audit and rotate all API keys and credentials stored in AI coding assistant workspaces immediately", "Monitor PyPI, npm, and Docker Hub dependencies for tampered or newly introduced packages from unknown publishers", "Implement prompt injection detection controls and restrict AI agent tool permissions in CI/CD environments"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "Prompt Injection", "LLM Security", "Industry News"]
tags: ["teampcp", "autonomous-ai-agents", "credential-harvesting", "dustmaker", "sandclock", "supply-chain-attack", "pypi", "npm", "docker-hub", "ci-cd-pipeline", "prompt-injection", "ai-coding-assistants", "google-threat-intelligence", "kubernetes", "ransomware", "canisterworm", "financially-motivated", "cloud-credential-theft"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-08T18:31:51+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/autonomous-ai-agents-compromise.html"
pipeline_version: "2.1.0"
---

## Overview

Google Threat Intelligence Group (GTIG) has disclosed an active, large-scale credential harvesting campaign carried out by a financially motivated threat actor tracked as **TeamPCP** (also known as Altered Spider and UNC6780). Using an autonomous, multi-agent AI attack framework, the group compromised thousands of credentials in under six hours—a tempo that GTIG chief analyst John Hultquist describes as faster than conventional incident response can match. The campaign specifically targets AI coding assistants, LLM security scanning tools, cloud environments, and developer supply chains across PyPI, npm, and Docker Hub.

## Technical Analysis

TeamPCP's operations are characterised by two evolving credential-stealing payloads:

**SANDCLOCK** (active March–April 2026) is a Python-based stealer designed for Linux environments with Kubernetes interaction and container escape functionality. It targets cryptocurrency wallets alongside cloud and developer credentials, and is identified as a component of the publicly documented **CanisterWorm** framework.

**DUSTMAKER** (active April 2026 onward) represents a significant capability upgrade. Key characteristics include:
- Cross-platform JavaScript payload optimised for CI/CD pipeline environments
- No container escape functionality, but broader credential theft scope
- **AI-specific attack techniques** not present in SANDCLOCK:
  - **Poisoning of AI assistant workspaces** — malicious content injected into contexts consumed by coding assistants such as GitHub Copilot or Cursor
  - **Prompt injection for defense evasion** — manipulating LLM-integrated security tooling to suppress or misdirect alerts

The attack chain begins with software supply chain compromise (malicious packages on PyPI, npm, Docker Hub), followed by payload deployment, credential exfiltration, and monetisation through direct sale or partnerships with ransomware and data extortion groups.

The autonomous multi-agent framework enables parallel execution across targets, explaining the sub-six-hour timeframe for mass exploitation—a meaningful benchmark for defenders calibrating detection SLAs.

## Framework Mapping

| Technique | Relevance |
|---|---|
| AML.T0051 – LLM Prompt Injection | DUSTMAKER uses prompt injection to evade LLM-integrated defences |
| AML.T0010 – AI Supply Chain Compromise | PyPI/npm/Docker Hub package tampering as initial access |
| AML.T0083 – Credentials from AI Agent Configuration | Targeting AI coding assistant workspaces for stored credentials |
| AML.T0098 – AI Agent Tool Credential Harvesting | Credential theft from tools invoked by AI agents |
| AML.T0103 – Deploy AI Agent | Autonomous multi-agent framework used for scaled exploitation |
| AML.T0080 – AI Agent Context Poisoning | Workspace poisoning to manipulate coding assistant outputs |

OWASP LLM05 (Supply Chain) and LLM01 (Prompt Injection) are the primary categories; LLM08 (Excessive Agency) applies where AI agents execute attacker-injected instructions without human oversight.

## Impact Assessment

- **Developers** using AI coding assistants face credential exposure via workspace poisoning
- **Organisations** with cloud-hosted LLM workloads risk co-option of compute resources for unauthorised AI workloads
- **Healthcare, government, and media** sectors are explicitly named as targeted verticals
- **Open-source ecosystem** integrity is degraded through repeated supply chain compromises on PyPI, npm, and Docker Hub
- The six-hour exploitation window represents a structural challenge: most enterprise detection and response cycles operate on longer timescales

## Mitigation & Recommendations

1. **Rotate credentials immediately** stored in or accessible by AI coding assistant workspaces and CI/CD pipeline secrets managers
2. **Enforce package allowlists** and verify checksums for dependencies sourced from PyPI, npm, and Docker Hub
3. **Deploy prompt injection detection** at LLM integration points, particularly in security tooling and developer assistant pipelines
4. **Apply least-privilege principles** to AI agent tool permissions—agents should not have write access to credential stores or pipeline configurations by default
5. **Set detection SLA targets below six hours** for supply chain anomalies given documented attack tempo
6. **Audit Kubernetes RBAC** for container workloads that interact with AI services, given SANDCLOCK's container escape capability

## References

- [The Hacker News – Autonomous AI Agents Compromise Thousands of Credentials in Under Six Hours](https://thehackernews.com/2026/09/autonomous-ai-agents-compromise.html)
