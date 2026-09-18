---
title: "AWS AgentCore Harness Ships Built-In Shell and Identity Vault Tools"
date: "2026-09-18T12:23:00+00:00"
draft: false 
slug: "aws-agentcore-harness-ships-built-in-shell-and-identity-vault-tools"

# ── Content metadata ──
summary: "Unit 42 researchers have published a detailed analysis of AWS AgentCore Harness's default configuration, specifically how its built-in shell tool and AgentCore Identity credential vault interact at runtime when credentials are resolved to plaintext. The research closes a visibility gap for defenders by providing concrete, operationally grounded guidance on scoping allowedTools, applying least-privilege to Identity vault service accounts, and monitoring outbound traffic from harness containers. What remains is an organisational maturity question: operators must actively opt into these controls rather than relying on secure defaults, meaning the benefit is fully realised only by teams with the awareness and tooling to enforce runtime scoping."
source: "Palo Alto Unit 42"
source_url: "https://unit42.paloaltonetworks.com/securing-aws-agentcore-harness-credentials"
source_title: "A Vault with a Heap-View: The Uncomfortable Space Between AgentCore Harness and Identity"
source_date: 2026-09-18T10:00:36+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/13310713/pexels-photo-13310713.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 7.5
adoption_velocity: "RAPID"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Defenders now have a documented runtime model of how AgentCore Identity credentials leave the vault and enter plaintext memory, enabling targeted memory and egress monitoring at the container layer", "The research establishes a concrete allowedTools scoping pattern that defenders can enforce in AgentCore Harness configurations to eliminate unintended shell access by default", "Least-privilege scoping guidance for Identity vault service accounts gives defenders a policy template to constrain the blast radius of any credential exfiltration attempt", "Outbound traffic monitoring guidance from harness containers provides a detection-layer control that defenders can integrate into existing cloud SIEM and CNAPP workflows"]

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0084 - Discover AI Agent Configuration", "AML.T0080 - AI Agent Context Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "AWS AgentCore Harness ships built-in shell and file_operations tools enabled by default alongside an AgentCore Identity credential vault."
tldr_who_at_risk: "Security and platform teams building on AgentCore benefit from this research by gaining a concrete runtime model and scoping controls to prevent unintended credential exposure."
tldr_actions: ["Scope allowedTools in every AgentCore Harness session to the minimum required set, explicitly removing shell and file_operations where not needed", "Apply least-privilege IAM policies to AgentCore Identity vault service accounts for each downstream integration", "Instrument egress monitoring on AgentCore harness containers to detect anomalous outbound connections as a detection-layer control"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Prompt Injection"]
tags: ["aws-agentcore", "agentic-ai", "credential-exfiltration", "iam", "runtime-security", "prompt-injection", "shell-tool", "identity-vault", "mcp", "cloud-security", "least-privilege", "unit-42"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher", "nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-09-18T11:13:16+00:00"
feed_source: "unit42"
original_url: "https://unit42.paloaltonetworks.com/securing-aws-agentcore-harness-credentials"
pipeline_version: "2.1.0"
---

## Defender Impact

Unit 42's analysis of AWS AgentCore Harness delivers the first operationally grounded runtime model of how the platform's built-in shell tool and Identity credential vault interact — closing a critical visibility gap for defenders who have been deploying agentic workloads without a clear picture of where credentials become plaintext and how they can be reached.

## Capability Overview

AWS AgentCore Harness is a managed runtime for AI agents. Operators declare a model, tools, skills, and instructions; AgentCore handles compute, memory, identity, networking, and observability. On top of the operator's declared configuration, the harness ships two built-in tools — `shell` (bash execution) and `file_operations` (file viewing, creation, and editing) — enabled in every session by default unless explicitly restricted via the `allowedTools` parameter.

AgentCore Identity is the platform's recommended credential management layer: an identity vault with encryption at rest, encryption in transit, KMS key management, and IAM-gated access. The vault is designed to store credentials used by the harness when authenticating against downstream integrations such as MCP servers.

The Unit 42 research focused on what happens at runtime when a credential must leave the vault to be used. Their finding: the harness's built-in shell tool operates within the same memory space where credentials are resolved to plaintext, and it runs as root. This means that without explicit `allowedTools` scoping, the shell tool has the same runtime reach as the credential resolution process — a significant exposure surface in the default out-of-the-box configuration.

AWS reviewed the disclosure and closed the report as informative under the AgentCore shared responsibility model, citing `allowedTools` scoping and egress filtering as customer-side controls.

## Defensive Advances

This research delivers several concrete advances for defenders:

- **Runtime credential lifecycle visibility.** Defenders now have a documented model of exactly when and where AgentCore Identity credentials transition from encrypted vault to plaintext in memory. This enables targeted container-layer monitoring rather than relying solely on vault-layer access logs.

- **Actionable allowedTools scoping pattern.** The research establishes a precise, tested configuration pattern for restricting the harness's tool surface. Defenders can use this as a policy baseline across all AgentCore deployments rather than discovering the exposure after the fact.

- **Least-privilege policy template for Identity vault service accounts.** The guidance on scoping vault service accounts per downstream integration gives security teams a concrete IAM policy model, not just a general least-privilege recommendation.

- **Egress monitoring as a compensating control.** The recommendation to instrument outbound traffic from harness containers provides a detection-layer control that integrates directly into existing CNAPP and SIEM workflows, giving defenders a runtime signal even when configuration controls are incomplete.

## Residual Gaps

The defensive value here is real but conditional on operator maturity. The core limitation is that all recommended controls are opt-in: `allowedTools` scoping, vault service account least-privilege, and egress monitoring must each be actively configured. Teams without established cloud-native security baselines or agentic AI deployment experience may not realise these controls are needed until after deployment. There is also no native enforcement mechanism within AgentCore that prevents the shell tool from being active by default — the secure posture requires deliberate action at every session configuration.

Additionally, the research covers only two of AgentCore's many integrations. The runtime credential exposure model likely applies to other vault-backed integrations, but defenders currently lack equivalent published analysis for those surfaces. Full coverage maturity will require either expanded research or AWS-provided runtime isolation documentation.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **AML.T0086 (Exfiltration via AI Agent Tool Invocation):** The shell tool's default-on status is the mechanism by which prompt injection could escalate to credential exfiltration; allowedTools scoping directly addresses this pathway.
- **AML.T0083 (Credentials from AI Agent Configuration)** and **AML.T0098 (AI Agent Tool Credential Harvesting):** The vault-to-plaintext runtime model maps directly to these techniques; egress monitoring provides the detection signal.
- **LLM08 (Excessive Agency):** Default root-level shell access in a managed runtime is a textbook excessive agency pattern; the scoping guidance is the prescribed mitigation.
- **LLM06 (Sensitive Information Disclosure):** Plaintext credential resolution in shared memory space is the disclosure mechanism; least-privilege vault scoping limits blast radius.

## Deployment Considerations

Teams should treat this research as a configuration audit trigger for any existing AgentCore deployments. The first action is an inventory of active harness sessions to confirm whether `allowedTools` has been explicitly scoped. New deployments should enforce an organisation-wide baseline that removes `shell` and `file_operations` unless a documented use case requires them. Egress monitoring should be integrated into container observability pipelines before production deployment, not retrospectively.

## Defender Checklist

- [ ] Audit all active AgentCore Harness sessions for explicit `allowedTools` configuration; flag any sessions using defaults
- [ ] Remove `shell` and `file_operations` from `allowedTools` in any session where bash execution and file I/O are not documented requirements
- [ ] Apply least-privilege IAM policies to each AgentCore Identity vault service account, scoped to the specific downstream integration it serves
- [ ] Instrument egress monitoring on all AgentCore harness containers; alert on unexpected outbound connections
- [ ] Extend this runtime credential lifecycle review to other AgentCore vault-backed integrations beyond MCP servers
- [ ] Include AgentCore `allowedTools` scoping in CI/CD pipeline validation to prevent permissive configurations reaching production

## References

- [A Vault with a Heap-View: The Uncomfortable Space Between AgentCore Harness and Identity — Palo Alto Unit 42](https://unit42.paloaltonetworks.com/securing-aws-agentcore-harness-credentials)
