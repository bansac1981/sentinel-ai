---
title: "Fireworks AI Breach Exposes Notion AI Chat Transcripts"
date: 2026-11-10T13:47:52+00:00
draft: false
slug: "fireworks-ai-breach-exposes-notion-ai-chat-transcripts"

# ── Content metadata ──
summary: "A security breach at Fireworks AI, a third-party inference and classification provider, has resulted in the exposure of unattributable Notion AI chat transcripts affecting less than 1% of Notion workspaces. Malicious actors accessed potential customer data, confirmed by Fireworks on November 8, 2026, including chat sessions used for Notion's AI Insights feature. While the exposed data lacked direct user or workspace identifiers, the incident highlights significant supply chain risks inherent in delegating AI inference and classification workloads to external vendors."
source: "HN AI Security"
source_url: "https://www.notion.com/help/security-incident-involving-a-third-party-ai-vendor"
source_title: "Fireworks AI security breach impacts Notion and their customers"
source_date: 2026-11-10T07:19:38+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1593824854968-7833add41c16?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzMHx8U3VwcGx5JTIwQ2hhaW4lMjBjeWJlcnNlY3VyaXR5JTIwdGVjaG5vbG9neXxlbnwwfDB8fHwxNzk0MzE4NDcxfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0057 - LLM Data Leakage", "AML.T0063 - Discover AI Model Outputs", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Malicious actors breached Fireworks AI, exposing unattributable Notion AI chat transcripts."
tldr_who_at_risk: "Notion workspace users who interacted with Notion AI's Insights feature are most exposed, as their chat content may have been accessed."
tldr_actions: ["Audit all third-party AI inference providers for data handling and isolation practices", "Disable or suspend AI features relying on affected vendors until breach scope is fully confirmed", "Implement data minimisation policies ensuring chat transcripts sent to external vendors contain no identifying metadata"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["fireworks-ai", "notion", "data-breach", "supply-chain", "llm-data-leakage", "ai-inference", "third-party-vendor", "chat-transcripts", "ai-insights", "open-weight-models"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-10T13:47:52+00:00"
feed_source: "hn_ai_security"
original_url: "https://www.notion.com/help/security-incident-involving-a-third-party-ai-vendor"
pipeline_version: "2.1.0"
content_hash: "b26e5100bdbee27c"
---

## Overview

A confirmed security breach at Fireworks AI, a widely used AI infrastructure platform serving tens of thousands of customers, has resulted in the unauthorised access of data belonging to downstream clients — including Notion. Notion disclosed that fewer than 1% of its workspaces may be impacted, with the exposed data comprising unattributable AI chat transcripts processed via its Insights feature and open-weight model inference pipeline. Fireworks AI formally notified Notion of the breach on November 6, 2026, with confirmation of the specific Notion dataset on November 8.

This incident is a textbook example of AI supply chain risk materialising in production: a trusted third-party inference provider becomes the weakest link in the security posture of multiple downstream AI products.

## Technical Analysis

Notion used Fireworks AI for two primary functions: (1) classification jobs powering the Notion AI Insights feature, which helped users understand their AI usage patterns, and (2) general inference serving for open-weight language models within the Notion product.

The exposed data consisted of chat transcripts submitted to Fireworks for classification or inference. Critically, these transcripts were described as "unattributable" — they were not tagged with workspace identifiers, user IDs, or company metadata, and did not include tool call results. However, the raw conversational content of the chat sessions was present in the dataset accessed by threat actors.

The absence of explicit identifiers reduces — but does not eliminate — risk. Conversational content may inherently contain sensitive business information, personally identifiable details, or proprietary data that users entered into Notion AI, even without attached labels.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0010 – AI Supply Chain Compromise**: The core attack vector. Threat actors compromised an upstream AI infrastructure provider to access data from downstream customers.
- **AML.T0057 – LLM Data Leakage**: Chat transcripts processed through the LLM inference pipeline were exfiltrated during the breach.
- **AML.T0063 – Discover AI Model Outputs**: Adversaries gained access to outputs and inputs of AI interactions, potentially revealing sensitive conversational context.

**OWASP LLM Top 10:**
- **LLM05 – Supply Chain Vulnerabilities**: Delegation of inference and classification to a third-party provider introduced an uncontrolled data exposure risk.
- **LLM06 – Sensitive Information Disclosure**: End-user chat content was exposed to unauthorised parties through a vendor-side breach.

## Impact Assessment

Notion estimates fewer than 1% of workspaces were affected. While that fraction may seem small, Notion's large user base means the absolute number of potentially impacted sessions could be significant. The exposed chat content, though unattributable at the metadata level, could still contain sensitive business or personal information typed by users. The Insights feature has been disabled, and Notion has terminated its Fireworks AI integration pending investigation.

Broader industry impact is also notable: Fireworks AI serves hundreds of thousands of developers and tens of thousands of customers, raising questions about the blast radius across other downstream platforms.

## Mitigation & Recommendations

- **Vet AI vendor data isolation**: Ensure inference providers maintain strict tenant data separation and do not store customer chat data beyond session completion without explicit agreement.
- **Minimise data sent to third-party AI providers**: Strip identifying metadata and sensitive content before forwarding prompts to external inference APIs where possible.
- **Establish breach notification SLAs with AI vendors**: Formalise contractual obligations for rapid disclosure of incidents affecting customer data.
- **Monitor third-party AI provider security advisories**: Treat AI infrastructure providers with the same rigour as other critical third-party dependencies in your supply chain risk programme.
- **Audit active AI integrations**: Review all current third-party AI inference and classification providers for data handling, retention, and security posture.

## References

- Notion Help Center – Security Incident Notice: https://www.notion.com/help/security-incident-involving-a-third-party-ai-vendor
