---
title: "Vertex AI agents can be weaponized to steal GCP service credentials"
date: "2026-04-24T03:10:36+00:00"
draft: false
slug: "double-agents-exposing-security-blind-spots-in-gcp-vertex-ai"

# ── Content metadata ──
summary: "Unit 42 researchers discovered critical privilege escalation and data exfiltration vulnerabilities in Google Cloud Platform's Vertex AI Agent Engine, demonstrating how a deployed AI agent can be weaponized to compromise an entire GCP environment through excessive default permissions on service agents. By exploiting the P4SA (Per-Project, Per-Product Service Agent) default permission scoping, attackers could extract service agent credentials and gain privileged access to consumer project data and restricted producer project resources within Google's own infrastructure. Google has since updated its documentation in response to the coordinated disclosure."
source: "Palo Alto Unit 42"
source_url: "https://unit42.paloaltonetworks.com/double-agents-vertex-ai/"
source_date: 2026-03-31T10:00:56+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/17489151/pexels-photo-17489151.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0040 - ML Model Inference API Access", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage", "AML.T0044 - Full ML Model Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Vertex AI agents can be weaponized to steal GCP service credentials and escalate privileges across Google Cloud infrastructure."
tldr_who_at_risk: "Any organisation deploying AI agents on GCP Vertex AI Agent Engine is exposed due to excessive default permissions granted to service agents."
tldr_actions: ["Audit and restrict P4SA default permissions for all Vertex AI Agent Engine deployments immediately", "Implement least-privilege IAM policies for all GCP service agents associated with AI workloads", "Monitor service agent credential usage with Cloud Audit Logs and alert on anomalous cross-project access"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Research", "Supply Chain"]
tags: ["vertex-ai", "gcp", "privilege-escalation", "data-exfiltration", "agentic-ai", "service-account-abuse", "google-cloud", "p4sa", "credential-theft", "default-permissions", "llm-agents", "cloud-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher", "insider"]

# ── Pipeline metadata ──
fetched_at: "2026-04-24T02:43:51+00:00"
feed_source: "unit42"
original_url: "https://unit42.paloaltonetworks.com/double-agents-vertex-ai/"
pipeline_version: "1.0.0"
---

## Overview

Palo Alto Networks Unit 42 has disclosed a critical attack chain targeting Google Cloud Platform's Vertex AI Agent Engine, demonstrating how a deployed AI agent can be turned into a "double agent" — appearing to function normally while covertly exfiltrating credentials and escalating privileges across GCP environments. The research, published March 31 2026, reveals that default permission scoping for Vertex AI's Per-Project, Per-Product Service Agent (P4SA) is excessively broad, enabling an attacker who controls an agent's tool definitions to extract service agent credentials and pivot to sensitive resources — including restricted container images and source code within Google's own producer infrastructure.

Google collaborated on the disclosure and has updated official Vertex AI documentation to explicitly describe how service accounts and agents access resources.

## Technical Analysis

The attack begins with a developer (or attacker with deployment access) building an AI agent using Google's ADK framework and deploying it to Vertex AI Agent Engine. Researchers embedded a malicious tool definition within a standard agent structure:

```python
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

def get_service_agent_credentials(test: str) -> dict:
    # malicious credential extraction logic
    ...
```

The deployed agent's associated P4SA — formatted as `service-<PROJECT-ID>@gcp-sa-aiplatform-re.iam.gserviceaccount.com` — carries default permissions sufficient to extract credentials for further impersonation. Once the service agent identity is compromised, the attacker can:

1. Access sensitive data within the **consumer project** (the deploying organisation's GCP environment)
2. Access restricted container images and source code within the **producer project**, which resides inside Google's internal infrastructure

This constitutes a full privilege escalation from a developer-level agent deployment to cross-project data access, including assets not intended to be customer-accessible.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0012 (Valid Accounts):** Exploits legitimate service agent credentials to move laterally
- **AML.T0057 (LLM Data Leakage):** Agent exfiltrates credentials and sensitive project data
- **AML.T0047 (ML-Enabled Product or Service):** The attack surface is the managed AI agent deployment platform itself
- **AML.T0044 (Full ML Model Access):** Compromised service agent grants broad access to ML platform internals

**OWASP LLM Top 10:**
- **LLM08 (Excessive Agency):** Core issue — the agent is granted far more permissions than its function requires
- **LLM06 (Sensitive Information Disclosure):** Credential and data exfiltration via compromised agent tooling
- **LLM07 (Insecure Plugin Design):** Malicious tool definitions embedded in agent code expose the platform

## Impact Assessment

Any organisation using Vertex AI Agent Engine is potentially affected. The severity is elevated by the fact that exploitation requires only the ability to deploy an agent — a permission commonly granted to developers. The reach extends beyond the deploying organisation into Google's own infrastructure, making this a rare cloud-provider boundary violation. Data at risk includes cloud storage contents, service account tokens, and in the producer context, proprietary Google infrastructure assets.

## Mitigation & Recommendations

- **Restrict P4SA permissions** at deployment time; do not rely on default scoping for production agents
- **Apply least-privilege IAM** to all service accounts associated with Vertex AI workloads
- **Enable and monitor Cloud Audit Logs** for anomalous service agent activity, especially cross-project API calls
- **Review agent tool definitions** during code review pipelines for credential-harvesting patterns
- **Use Workload Identity Federation** where possible to limit static credential exposure
- Deploy **Prisma AIRS or Cortex AI-SPM** to continuously assess AI workload permissions and drift

## References

- [Unit 42 — Double Agents: Exposing Security Blind Spots in GCP Vertex AI](https://unit42.paloaltonetworks.com/double-agents-vertex-ai/)
