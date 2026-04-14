---
title: "OWASP GenAI Security Project Gets Update, New Tools Matrix"
date: "2026-04-14T08:18:19+00:00"
draft: false

# ── Content metadata ──
summary: "OWASP has updated its GenAI Security Project to formally recognise 21 generative AI risks, releasing a new tools matrix to help organisations structure their defences. The update notably distinguishes between securing traditional GenAI systems and the emerging attack surface presented by agentic AI architectures. This guidance represents a significant standards-level acknowledgement that agentic AI requires its own dedicated security posture."
source: "Dark Reading"
source_url: "https://www.darkreading.com/application-security/owasp-genai-security-project-update-matrix"
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/5380655/pexels-photo-5380655.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0056 - LLM Meta Prompt Extraction", "AML.T0010 - ML Supply Chain Compromise"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM09 - Overreliance"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Regulatory", "Industry News", "Research"]
tags: ["owasp", "genai-security", "agentic-ai", "llm-top-10", "security-standards", "tools-matrix", "defensive-guidance", "ai-governance", "risk-framework"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-13T05:09:52+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/application-security/owasp-genai-security-project-update-matrix"
pipeline_version: "1.0.0"
slug: "owasp-genai-security-project-gets-update-new-tools-matrix"
---

## Overview

The OWASP GenAI Security Project has released a significant update, formally cataloguing 21 generative AI risks and introducing a new tools matrix designed to help organisations map defensive controls to those risks. A key structural development in the update is OWASP's explicit recommendation that companies treat GenAI security and agentic AI security as related but distinct disciplines — each requiring its own controls, policies, and tooling. This recognition reflects the rapidly diverging threat surfaces between static LLM deployments and autonomous, multi-step agentic systems now being widely adopted in enterprise environments.

## Technical Analysis

The distinction between GenAI and agentic AI is security-critical. Traditional GenAI deployments (e.g., a customer-facing chatbot) have a relatively bounded attack surface — primarily prompt injection, output manipulation, and data leakage. Agentic AI systems, however, operate with extended autonomy: they chain tool calls, access external APIs, browse the web, write and execute code, and take actions with real-world consequences. This dramatically expands the blast radius of vulnerabilities such as prompt injection, which can now result in unauthorised actions rather than merely inappropriate text output.

The new OWASP tools matrix is intended to provide a structured mapping between identified risks and available mitigations or evaluation tools, enabling security teams to operationalise the LLM Top 10 and broader GenAI risk catalogue within their existing security programmes.

The 21 recognised risks span a wide spectrum including prompt injection, training data poisoning, model theft, insecure plugin/tool design, excessive agency, and supply chain vulnerabilities — effectively extending the existing LLM Top 10 framework to accommodate the nuances of agentic and multi-model architectures.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **AML.T0054 (LLM Jailbreak)** remain the most directly addressed risks, particularly in the context of agentic systems where injection can trigger downstream tool misuse.
- **LLM08 (Excessive Agency)** is especially pertinent given the update's focus on agentic AI — autonomous agents granted overly broad permissions represent a core systemic risk.
- **LLM05 (Supply Chain Vulnerabilities)** maps to **AML.T0010**, as agentic systems frequently depend on third-party tools, plugins, and model APIs.
- **LLM07 (Insecure Plugin Design)** directly addresses the tool-use layer common in agentic architectures.

## Impact Assessment

This update primarily affects security architects, AppSec teams, and AI/ML engineers responsible for deploying or governing GenAI and agentic systems. Organisations that have already adopted LLM-based automation — particularly those using frameworks like LangChain, AutoGen, or similar agentic orchestration platforms — face the highest exposure if controls are not differentiated between static and agentic deployments. The tools matrix provides a practical on-ramp for organisations at varying levels of AI security maturity.

## Mitigation & Recommendations

- **Adopt the OWASP tools matrix** as a baseline mapping exercise for existing GenAI deployments.
- **Separately assess agentic AI systems** for excessive agency, tool-call injection paths, and privilege escalation vectors.
- **Apply least-privilege principles** to all agentic tool integrations and API access scopes.
- **Implement prompt injection defences** at both input and inter-agent communication layers.
- **Monitor and log all agentic actions** — treat autonomous AI actions as auditable events equivalent to privileged user activity.
- **Track supply chain dependencies** for third-party models, plugins, and data pipelines used within agentic systems.

## References

- [OWASP GenAI Security Project Gets Update, New Tools Matrix — Dark Reading](https://www.darkreading.com/application-security/owasp-genai-security-project-update-matrix)
