---
title: "AWS Bedrock AgentCore Gateway Adds ServiceNow Token Exchange"
date: 2026-11-04T13:11:30+00:00
draft: true
slug: "aws-bedrock-agentcore-gateway-adds-servicenow-token-exchange"

# ── Content metadata ──
summary: "AWS has introduced on-behalf-of (OBO) token exchange between ServiceNow and Amazon Bedrock AgentCore Gateway, enabling AI agents to authenticate to ServiceNow APIs using delegated, user-scoped credentials rather than shared service accounts. This closes a meaningful identity governance gap for agentic workflows \u2014 ensuring that actions taken by AI agents in ServiceNow are attributable to the originating human identity, supporting least-privilege access and audit trail integrity. Realising the full benefit requires organisations to have mature identity federation, ServiceNow OAuth configuration, and Bedrock AgentCore adoption already in place."
source: "AWS Machine Learning Blog"
source_url: "https://aws.amazon.com/blogs/machine-learning/servicenow-on-behalf-of-token-exchange-with-bedrock-agentcore-gateway"
source_title: "ServiceNow on-behalf-of token exchange with Bedrock AgentCore Gateway"
source_date: 2026-11-03T16:47:40+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/1698966/pexels-photo-1698966.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 5.2
adoption_velocity: "GRADUAL"
capability_category: "platform-integration"
attack_vectors_introduced: ["Delegated identity via OBO token exchange reduces reliance on shared service account credentials in AI agent workflows, closing a credential blast-radius gap", "User-scoped token delegation enables per-user audit trails for AI agent actions in ServiceNow, improving forensic accountability", "Centralised token exchange through AgentCore Gateway creates a single enforcement point for access policy and revocation, simplifying access control management", "Reduced standing privilege for AI agents — tokens are scoped to the requesting user's permissions rather than a privileged automation account"]

# ── AI Security Classification ──
relevance_score: 5.8
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0084 - Discover AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "AWS Bedrock AgentCore Gateway now supports ServiceNow OBO token exchange for delegated AI agent identity."
tldr_who_at_risk: "Security and IAM teams deploying AI agents against ServiceNow APIs benefit directly \u2014 this closes the shared-credential accountability gap in agentic ITSM workflows."
tldr_actions: ["Audit existing ServiceNow AI agent integrations for shared or over-privileged service accounts and plan migration to OBO delegation", "Review ServiceNow OAuth 2.0 OBO configuration requirements and validate compatibility with your identity provider before AgentCore onboarding", "Establish logging and alerting on token exchange events at the AgentCore Gateway layer to maintain a complete audit trail of agent-initiated actions"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News"]
tags: ["aws", "bedrock", "agentcore", "servicenow", "token-exchange", "oauth", "on-behalf-of", "agentic-ai", "identity-federation", "delegated-credentials", "access-control", "ai-agents"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-04T13:11:30+00:00"
feed_source: "aws_ml"
original_url: "https://aws.amazon.com/blogs/machine-learning/servicenow-on-behalf-of-token-exchange-with-bedrock-agentcore-gateway"
pipeline_version: "2.1.0"
---

## Defender Impact
The introduction of on-behalf-of (OBO) token exchange between ServiceNow and AWS Bedrock AgentCore Gateway directly addresses one of the most persistent identity governance problems in agentic AI deployments: AI agents acting under shared, over-privileged service account credentials with no attribution back to the human user who initiated the workflow. For security teams managing ITSM-integrated AI agents, this is a meaningful and welcome step toward least-privilege agentic access.

## Capability Overview
AWS Bedrock AgentCore Gateway now supports the OAuth 2.0 on-behalf-of token exchange flow with ServiceNow as a downstream API target. In practical terms, this means that when a human user triggers an AI agent workflow — whether through a chatbot, an orchestration layer, or an automated request — the agent does not authenticate to ServiceNow using its own static credentials or a shared service account. Instead, AgentCore Gateway performs a token exchange, presenting the originating user's identity token to ServiceNow's OAuth authorisation server and receiving back a scoped access token that reflects that user's permissions.

This pattern — common in zero-trust identity architectures but historically difficult to implement cleanly in agentic AI pipelines — is now available as a managed capability within Bedrock's gateway layer. The gateway acts as the token broker, handling the exchange mechanics and presenting downstream APIs with user-contextual tokens rather than agent-level credentials. ServiceNow, as the resource server, sees requests authenticated to the delegating user, not to a generic automation identity.

For defenders, the significance lies in what this removes from the equation: long-lived, shared service account credentials stored in agent configurations — a persistent target for credential harvesting and a primary source of excessive agency in agentic AI deployments.

## Defensive Advances
**Credential blast-radius reduction:** Eliminating shared service accounts in favour of per-user delegated tokens means a compromised agent configuration no longer exposes a standing privileged credential. The token is scoped to the requesting user and subject to that user's access policy.

**Audit trail integrity:** ServiceNow access logs will now attribute agent-initiated actions to the originating human identity rather than to a generic automation account. This is a prerequisite for meaningful forensic investigation and compliance reporting in ITSM environments.

**Centralised policy enforcement:** AgentCore Gateway as the token exchange broker creates a single, auditable enforcement point. Access policy changes — including revocation — can be applied at the gateway layer without modifying individual agent configurations.

**Alignment with least-privilege principles:** Agents can only perform actions within the bounds of the delegating user's ServiceNow permissions. An agent cannot escalate beyond what the user themselves could do, reducing the excessive agency risk inherent in broadly-scoped automation accounts.

## Residual Gaps
The benefit of this capability is real but contingent on organisational maturity in several areas. Organisations that have not yet federated their identity provider with ServiceNow's OAuth layer will face non-trivial integration prerequisites before OBO exchange is usable. The token exchange flow assumes a functioning OIDC/OAuth trust chain between the user's identity provider, AWS IAM, and ServiceNow — this is not a zero-configuration feature.

Token lifetime management and refresh handling in long-running agentic workflows also requires careful consideration. OBO tokens inherit the expiry constraints of the upstream identity token; for extended automation tasks this may introduce operational friction that teams compensate for with broader scopes, partially undermining the least-privilege goal.

Finally, this capability is currently scoped to ServiceNow as the downstream target. Organisations running multi-system AI agents — where a single workflow touches ServiceNow, Jira, Salesforce, or internal APIs — will not achieve uniform delegated identity across all systems through this mechanism alone.

## Framework Mapping
This capability most directly addresses **AML.T0083 (Credentials from AI Agent Configuration)** and **AML.T0098 (AI Agent Tool Credential Harvesting)** by removing static credentials from the agent configuration surface. It also reduces exposure to **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** by constraining agent permissions to user-scope. From an OWASP perspective, this advances **LLM08 (Excessive Agency)** controls by enforcing permission inheritance, and reduces **LLM07 (Insecure Plugin Design)** risk by replacing static API keys with dynamic, scoped tokens.

## Deployment Considerations
Organisations should sequence deployment by first confirming their identity provider supports the OBO grant type and that ServiceNow OAuth 2.0 is configured for delegated flows. IAM role mapping between AWS and ServiceNow identities must be validated before gateway integration. Security teams should treat the AgentCore Gateway token exchange logs as a tier-1 audit log source and integrate them into SIEM pipelines from day one.

## Defender Checklist
- [ ] Inventory all current ServiceNow AI agent integrations using shared or service account credentials
- [ ] Confirm identity provider OBO grant type support and ServiceNow OAuth 2.0 readiness
- [ ] Configure AgentCore Gateway token exchange and validate scoping against user permission boundaries
- [ ] Integrate AgentCore Gateway token exchange logs into SIEM for audit trail continuity
- [ ] Define token lifetime policies aligned with agentic workflow duration requirements
- [ ] Plan roadmap for extending delegated identity patterns to other downstream API targets beyond ServiceNow

## References
- [ServiceNow on-behalf-of token exchange with Bedrock AgentCore Gateway — AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/servicenow-on-behalf-of-token-exchange-with-bedrock-agentcore-gateway)
