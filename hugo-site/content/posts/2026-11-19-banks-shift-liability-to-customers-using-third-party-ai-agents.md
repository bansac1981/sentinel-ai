---
title: "Banks Shift Liability to Customers Using Third-Party AI Agents"
date: 2026-11-19T14:37:43+00:00
draft: false
slug: "banks-shift-liability-to-customers-using-third-party-ai-agents"

# ── Content metadata ──
summary: "Major U.S. banks including Citibank, JPMorgan, and Bank of America are updating terms of service to disclaim liability for transactions or hacks resulting from customers granting third-party AI agents access to their accounts. This creates a significant security risk gap: if an AI agent leaks credentials or is compromised, the customer bears full financial responsibility. The policy shift highlights unresolved trust and accountability challenges in agentic AI deployments that handle sensitive financial credentials."
source: "TechCrunch AI"
source_url: "https://techcrunch.com/2026/11/18/more-banks-says-customers-using-ai-agents-are-on-their-own-even-if-they-get-hacked"
source_title: "More banks say customers using AI agents are on their own \u2014 even if they get hacked"
source_date: 2026-11-18T17:32:10+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1759159091682-3b98f4759367?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8bWVjaGFuaWNhbCUyMGdlYXJzJTIwaW50ZXJsb2NraW5nJTIwbWFjaGluZXxlbnwwfDB8fHwxNzk1MDk5MDYyfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0012 - Valid Accounts", "AML.T0080 - AI Agent Context Poisoning", "AML.T0110 - AI Agent Tool Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Major U.S. banks are disclaiming all liability for hacks or losses caused by third-party AI agents accessing customer accounts."
tldr_who_at_risk: "Retail banking customers who grant AI agents access to financial accounts are fully exposed, with no institutional recourse if credentials are stolen or misused."
tldr_actions: ["Avoid granting AI agents write or transaction access to bank accounts until liability frameworks are established", "Audit which third-party AI tools currently hold your financial credentials and revoke unnecessary access immediately", "Prefer bank-native AI tools with read-only permissions, as these retain institutional liability protections"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Regulatory", "Industry News"]
tags: ["ai-agents", "banking-security", "credential-exposure", "third-party-ai", "liability-shift", "fintech", "agentic-ai", "account-takeover", "terms-of-service", "citibank", "jpmorgan", "bank-of-america"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-19T14:37:43+00:00"
feed_source: "techcrunch_ai"
original_url: "https://techcrunch.com/2026/11/18/more-banks-says-customers-using-ai-agents-are-on-their-own-even-if-they-get-hacked"
pipeline_version: "2.1.0"
content_hash: "3706c09c56898dac"
---

## Overview

Five major U.S. banks — Citibank, JPMorgan, Bank of America, PNC, and Citizens — have updated their terms of service to disclaim liability for any losses, unauthorised transactions, or account compromises arising from customers granting access to third-party AI agents. Critically, Citi's updated policy extends this disclaimer to scenarios where the AI tool itself is hacked or leaks customer credentials — leaving users fully exposed with no path to reimbursement.

This marks a significant inflection point in the security posture of consumer-facing agentic AI. As AI agents proliferate in personal finance — capable of reading balances, executing payments, and managing investments — banks are drawing a hard line: the AI agent, and all associated risk, belongs to the customer.

## Technical Analysis

The core security concern is **credential delegation**. When a user grants a third-party AI agent access to their bank account, they typically provide either direct login credentials or OAuth-style tokens. These credentials are stored within the agent's configuration or memory layer, creating a persistent attack surface.

Threat vectors include:

- **Credential harvesting from agent configuration**: Attackers compromising the AI platform's backend can extract stored banking tokens at scale (AML.T0083, AML.T0098).
- **Tool poisoning**: A malicious or compromised tool integration within an AI agent workflow could redirect transactions or exfiltrate account data (AML.T0110).
- **Context poisoning**: Injected instructions via documents or web content the agent processes could manipulate it into initiating fraudulent transactions (AML.T0080).
- **Valid account abuse**: Once credentials are obtained, attackers use them directly — no AI exploitation required (AML.T0012).

The absence of standardised, scoped, revocable permission models for AI agent access to financial systems is a foundational gap. Unlike Open Banking APIs with granular OAuth scopes, many AI agent integrations rely on full-credential sharing.

## Framework Mapping

- **LLM08 (Excessive Agency)**: AI agents with transaction execution capabilities represent an over-permissioned deployment pattern where the blast radius of compromise is disproportionate.
- **LLM07 (Insecure Plugin Design)**: Third-party AI finance tools connecting to banking APIs without enforced read-only scopes exemplify unsafe plugin architecture.
- **LLM06 (Sensitive Information Disclosure)**: Agent memory or configuration stores holding banking credentials are high-value targets for exfiltration.
- **LLM05 (Supply Chain Vulnerabilities)**: The AI tool itself is a supply chain node — a compromised update or backend breach propagates directly to financial accounts.

## Impact Assessment

The liability shift places the entire risk burden on individual consumers, who have little visibility into how third-party AI tools store, transmit, or protect their credentials. In a credential-compromise scenario, customers face financial losses with no regulatory backstop — existing consumer protection frameworks (e.g., Regulation E) were not designed with AI agent intermediaries in mind. The systemic risk scales with adoption: as millions of users connect AI tools to financial accounts, a single platform breach could yield mass account takeover.

## Mitigation & Recommendations

- **Revoke third-party AI agent access** to bank accounts unless operationally essential; audit connected applications in your bank's security settings.
- **Use read-only integrations only** — tools like Anthropic's finance product that explicitly prohibit transaction execution reduce the blast radius of compromise.
- **Prefer bank-native AI tools** that maintain institutional liability coverage rather than third-party agents operating outside the bank's terms.
- **Demand scoped, revocable tokens**: Advocate for and use platforms that support OAuth with minimal permission scopes rather than full credential sharing.
- **Monitor account activity continuously** and set low-threshold transaction alerts if any AI agent access is maintained.

## References

- [TechCrunch: More banks say customers using AI agents are on their own — even if they get hacked](https://techcrunch.com/2026/11/18/more-banks-says-customers-using-ai-agents-are-on-their-own-even-if-they-get-hacked)
