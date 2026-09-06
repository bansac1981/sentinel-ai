---
title: "LLM-Assisted Intrusions Hit Latin American Orgs via NextChat"
date: "2026-09-06T04:39:59+00:00"
draft: false 
slug: "llm-assisted-intrusions-hit-latin-american-orgs-via-nextchat"

# ── Content metadata ──
summary: "Unit 42 has identified two active intrusion campaigns targeting Latin American organisations in the transportation and financial sectors, with threat actors demonstrably leveraging commercial LLMs \u2014 including self-hosted NextChat instances \u2014 to orchestrate and refine attack execution. The campaigns share overlapping SOCKS5 relay infrastructure and exhibit iterative, AI-assisted scripting behaviour, suggesting independent but parallel adoption of LLM tooling by distinct threat groups. This represents a concrete operational example of adversaries using AI to lower the skill floor for multi-stage network intrusion and data exfiltration."
source: "Palo Alto Unit 42"
source_url: "https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs"
source_title: "Attackers Expose Ongoing AI Tool Use Targeting Organizations in Latin America"
source_date: 2026-09-03T10:00:58+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1752900385350-7697f37808b2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOHx8c2Nyb2xsJTIwbWFudXNjcmlwdCUyMGFuY2llbnQlMjBrbm93bGVkZ2V8ZW58MHwwfHx8MTc4ODY2NjMzM3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0065 - LLM Prompt Crafting", "AML.T0114 - AI Service Web Interface", "AML.T0086 - Exfiltration via AI Agent Tool Invocation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Two active campaigns use commercial LLMs and self-hosted NextChat to orchestrate intrusions across Latin America."
tldr_who_at_risk: "Latin American transportation, financial, and government organisations are directly exposed due to targeted phishing and vulnerable web server exploitation."
tldr_actions: ["Block or monitor self-hosted LLM endpoints (e.g. NextChat) on corporate and operational infrastructure", "Detect iterative numbered batch script execution patterns indicative of AI-guided trial-and-error attack behaviour", "Audit and restrict SOCKS5 proxy traffic egressing from sensitive network segments"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Industry News"]
tags: ["llm-assisted-attacks", "nextchat", "latin-america", "socks5-proxy", "data-exfiltration", "living-off-the-land", "remote-access-trojan", "unit42", "financial-sector", "transportation-sector", "chatgpt", "claude", "threat-actor-tooling"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-06T03:45:34+00:00"
feed_source: "unit42"
original_url: "https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs"
pipeline_version: "2.1.0"
---

## Overview

Unit 42 researchers Reese Lewis and Sara McBroom have documented two concurrent, multi-stage intrusion campaigns targeting Latin American organisations, both of which show clear evidence of operational AI integration. Tracked as CL-CRI-1131 (Mexico/Ecuador, transportation and government focus) and CL-CRI-1163 (Brazil, financial sector focus), the campaigns are attributed to distinct threat groups but share overlapping SOCKS5 relay infrastructure and a common pattern: the use of commercial large language models to plan, iterate, and orchestrate attack execution.

This marks a meaningful shift in observed threat actor behaviour in the region — AI tooling is no longer theoretical; it is being operationally embedded into intrusion workflows.

## Technical Analysis

**CL-CRI-1131 — Mexican Transportation Campaign**
During an April 2026 compromise, operators exhibited classic LLM-assisted trial-and-error behaviour. Repeated failed attempts to dump the SAM registry hive and NTDS.dit file were followed by volume shadow copy manipulation — a pattern consistent with iterative troubleshooting via LLM prompting. The attackers used a series of sequentially numbered batch scripts to collect and exfiltrate sensitive data, a naming convention that strongly implies AI-generated or AI-iterated scripting. Critically, the group self-hosted a NextChat instance on operational infrastructure, providing a direct interface to commercial LLMs (including ChatGPT and Claude) from within their attack environment.

**CL-CRI-1163 — Brazilian Financial Campaign**
This cluster expanded on previously reported job-themed phishing campaigns targeting vulnerable web servers. Attackers deployed custom remote access Trojans (RATs) and a Go-based SOCKS5 proxy tool with iterative filenames — again suggestive of AI-assisted development or iteration. The campaign demonstrates how AI tooling can accelerate custom malware development cycles.

Both clusters share SOCKS5 relay infrastructure, suggesting possible resource sharing or procurement from a common criminal marketplace, even if operational goals differ.

## Framework Mapping

- **AML.T0047 (AI-Enabled Product or Service)**: Attackers operationalised commercial LLMs (ChatGPT, Claude) as a direct component of their intrusion workflow.
- **AML.T0065 (LLM Prompt Crafting)**: The iterative batch script naming and trial-and-error execution pattern strongly implies structured prompting to generate and refine attack tooling.
- **AML.T0114 (AI Service Web Interface)**: Self-hosted NextChat instances provided a controlled LLM interface within the attack infrastructure.
- **LLM08 (Excessive Agency)**: LLMs were granted implicit operational agency over attack planning and script generation without guardrails preventing malicious use.

## Impact Assessment

Organisations in Latin American transportation, financial services, and government sectors face elevated risk. The use of AI lowers the technical barrier for attackers, enabling more rapid iteration on evasion and data collection techniques. The campaign's persistence from April through June 2026 and its breadth across Mexico, Ecuador, and Brazil indicate sustained, resourced operations rather than opportunistic incidents.

## Mitigation & Recommendations

- **Block unauthorised LLM interfaces**: Detect and restrict self-hosted NextChat or similar LLM front-ends on enterprise and operational networks.
- **Monitor batch script sequencing**: Alert on numbered or sequentially named script execution chains, which may indicate AI-guided iterative attack behaviour.
- **Restrict SOCKS5 egress**: Implement strict egress filtering to detect tunnelling activity consistent with both clusters' relay infrastructure.
- **Harden shadow copy access**: Monitor and restrict VSS manipulation, a key indicator in the CL-CRI-1131 intrusion.
- **Phishing resilience**: Reinforce defences against job-themed lure documents targeting web-exposed services in the financial sector.

## References

- [Unit 42 — Attackers Expose Ongoing AI Tool Use Targeting Organizations in Latin America](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs)
