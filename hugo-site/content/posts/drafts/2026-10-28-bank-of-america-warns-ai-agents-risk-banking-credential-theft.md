---
title: "Bank of America Warns AI Agents Risk Banking Credential Theft"
date: 2026-10-28T11:29:18+00:00
draft: true
slug: "bank-of-america-warns-ai-agents-risk-banking-credential-theft"

# ── Content metadata ──
summary: "Bank of America has issued a customer advisory warning against sharing banking credentials with AI assistants or agents, highlighting risks of unauthorised financial transactions and credential leakage. The warning reflects a broader industry challenge as agentic AI tools increasingly seek access to sensitive financial accounts. Security vulnerabilities in AI agents could expose banking credentials to financially motivated threat actors."
source: "TechCrunch AI"
source_url: "https://techcrunch.com/2026/10/27/bank-of-america-kindly-asks-that-you-dont-share-your-banking-password-with-your-ai-assistant"
source_title: "Bank of America kindly asks that you don\u2019t share your banking password with your AI assistant"
source_date: 2026-10-27T21:44:34+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1658539528240-b89539629ce6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxNHx8Y2hlc3MlMjBwaWVjZSUyMHN0cmF0ZWd5JTIwYm9hcmQlMjBnYW1lfGVufDB8MHx8fDE3OTMxODY5NTh8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0012 - Valid Accounts", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Bank of America warns customers never to share banking credentials with AI agents or assistants."
tldr_who_at_risk: "Retail banking customers using personal AI assistants with account access are directly exposed to credential theft and unauthorised transactions."
tldr_actions: ["Never provide banking usernames or passwords to any AI assistant or third-party agent", "Audit any AI tools that have been granted access to financial accounts and revoke unnecessary permissions", "Use bank-sanctioned OAuth or open-banking APIs for AI integrations rather than credential sharing"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Industry News", "Regulatory"]
tags: ["agentic-ai", "credential-theft", "banking-security", "ai-agents", "fintech", "bank-of-america", "agentic-payments", "credential-sharing", "account-takeover", "llm-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-28T11:29:18+00:00"
feed_source: "techcrunch_ai"
original_url: "https://techcrunch.com/2026/10/27/bank-of-america-kindly-asks-that-you-dont-share-your-banking-password-with-your-ai-assistant"
pipeline_version: "2.1.0"
---

## Overview

Bank of America has issued a direct customer advisory urging users not to share their banking credentials — usernames and passwords — with AI assistants or autonomous agents. The email, titled *'Protecting your finances in the AI World'*, warns that sharing credentials with any outside service, including AI-enabled tools, creates significant financial and security risk. The advisory also makes clear that customers bear full liability for any activity resulting from credential access they voluntarily grant.

The warning arrives at a critical inflection point: AI agents capable of executing financial transactions autonomously are becoming mainstream, and both consumers and the financial industry are still developing the norms and infrastructure to support them safely.

## Technical Analysis

The core risk vector here is **credential-based AI agent access**. When a user provides their banking username and password directly to an AI assistant, several threat scenarios emerge:

1. **Credential leakage via model vulnerabilities**: A security flaw in the AI assistant — such as insecure storage, prompt injection, or data exfiltration via tool invocations — could expose the credentials to a third party.
2. **Unauthorised agentic actions**: An AI agent operating with full account credentials can initiate transactions, change settings, or extract account data without explicit per-action user approval, representing a classic excessive agency failure.
3. **Account lockout**: Banks' fraud detection systems may flag credential use from unusual IP addresses or behavioural patterns associated with AI agents, locking legitimate users out.
4. **Liability transfer**: Unlike OAuth-based delegated access, direct credential sharing shifts legal responsibility entirely to the customer under standard bank account agreements.

The article also references banks grappling with **unauthorised agents accessing customer funds**, suggesting active exploitation of this attack surface is already occurring in the wild.

## Framework Mapping

- **AML.T0083 (Credentials from AI Agent Configuration)** and **AML.T0098 (AI Agent Tool Credential Harvesting)** are directly applicable: attackers or flawed agent designs can harvest credentials stored within or passed to agent contexts.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** applies where a compromised agent exfiltrates credentials through outbound tool calls.
- **LLM08 (Excessive Agency)** captures the risk of agents taking unsanctioned financial actions.
- **LLM06 (Sensitive Information Disclosure)** covers credential leakage scenarios.
- **LLM09 (Overreliance)** reflects the consumer behaviour pattern driving this risk.

## Impact Assessment

The affected population is broad — any retail banking customer who has granted or is considering granting an AI assistant their banking credentials. The financial impact could range from fraudulent transactions to full account compromise. The legal impact is particularly sharp: customers who share credentials lose standard fraud protections under most bank account agreements. At the industry level, unresolved agentic payment standards create systemic exposure across multiple financial institutions.

## Mitigation & Recommendations

- **Never share raw banking credentials** with any AI tool; demand OAuth or open-banking API integrations instead.
- **Revoke access** for any AI tools currently holding banking usernames or passwords.
- **Prefer bank-sanctioned agentic integrations** that use scoped, revocable tokens rather than full credential access.
- **Monitor account activity** for anomalous transactions that may indicate agent misuse.
- **Financial institutions** should accelerate deployment of delegated access standards (e.g., open banking OAuth 2.0 flows) that natively support AI agent authentication without credential sharing.

## References

- [Bank of America kindly asks that you don't share your banking password with your AI assistant — TechCrunch](https://techcrunch.com/2026/10/27/bank-of-america-kindly-asks-that-you-dont-share-your-banking-password-with-your-ai-assistant)
