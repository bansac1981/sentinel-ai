---
title: "Storm-0940 Uses ARTEX AI Agents in ConnectWise Attack"
date: 2026-10-22T10:27:18+00:00
draft: true
slug: "storm-0940-uses-artex-ai-agents-in-connectwise-attack"

# ── Content metadata ──
summary: "Microsoft has attributed a supply chain compromise of ConnectWise Cloud Backup to China-aligned threat actor Storm-0940, which deployed ARTEX, a Go-based agentic AI penetration testing framework, to automate password spraying and OAuth abuse at machine speed. The AI-accelerated campaign targeted over 2,250 tenants across hundreds of organisations, achieving up to 2,900 sign-in attempts per minute and in some cases privileged cloud access within three hours of initial targeting. The incident represents a significant escalation in nation-state use of agentic AI tools to compress attack timelines and overwhelm defenders."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/10/china-linked-hackers-use-artex-ai.html"
source_title: "China-Linked Hackers Use ARTEX AI Agents in ConnectWise Supply Chain Attack"
source_date: 2026-10-22T04:21:26+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1674690223052-030e2fc6e167?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzMHx8ZHJvbmUlMjBhZXJpYWwlMjBhdXRvbm9tb3VzJTIwZmxpZ2h0fGVufDB8MHx8fDE3OTI2NjQ4Mzh8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0103 - Deploy AI Agent", "AML.T0010 - AI Supply Chain Compromise", "AML.T0012 - Valid Accounts", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0084 - Discover AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "China-linked Storm-0940 weaponised ARTEX AI agents to automate a ConnectWise supply chain attack at machine speed."
tldr_who_at_risk: "Organisations using ConnectWise Cloud Backup with Microsoft 365 and Exchange Online are directly exposed due to cross-tenant credential abuse via compromised OAuth applications."
tldr_actions: ["Audit and revoke all non-essential OAuth application permissions in Microsoft 365 tenants immediately", "Enable anomaly-based sign-in alerting to flag high-velocity password spray patterns exceeding baseline thresholds", "Verify ConnectWise Cloud Backup integrations for signs of unauthorised credential changes or privilege modifications since September 2026"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "Industry News", "LLM Security"]
tags: ["storm-0940", "artex", "agentic-ai", "connectwise", "supply-chain-attack", "china-apt", "password-spraying", "oauth-abuse", "microsoft-365", "cloud-security", "go-based-framework", "quad7-botnet"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-10-22T10:27:18+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/10/china-linked-hackers-use-artex-ai.html"
pipeline_version: "2.1.0"
---

## Overview

Microsoft has attributed a supply chain compromise of the ConnectWise Cloud Backup application to Storm-0940, a China state-aligned threat actor assessed to be active since at least 2021. At the centre of the campaign is **ARTEX**, a Go-based agentic AI penetration testing framework that the actor used to automate reconnaissance, password spraying, and OAuth application abuse at a pace Microsoft describes as "machine speed." The campaign has targeted hundreds of organisations across aerospace, defence, energy, financial services, government, and technology sectors since September 2026, with some victims experiencing full privileged cloud access within three hours of initial targeting.

## Technical Analysis

ARTEX functions as an autonomous AI agent framework purpose-built for offensive operations. Once deployed against the ConnectWise supply chain vector, it enabled Storm-0940 to:

- **Authenticate via abused OAuth applications** that had already been granted access to downstream tenant environments, eliminating the need for interactive user sign-in and evading standard MFA prompts.
- **Conduct cross-tenant password spraying** at 2,900 attempts per minute — between October 10–14, 2026, Storm-0940 infrastructure at `144.172.64[.]99` targeted 327 accounts across eight organisations, generating over 151,000 failed logon events, peaking at 111,000 failures in a single day.
- **Automate post-compromise actions** including credential modification on existing OAuth applications, privilege escalation attempts, and reconnaissance against Microsoft 365 and Exchange Online resources.

The framework was reportedly made closed-source following its earlier abuse in attacks on South Korean financial institutions, suggesting a controlled distribution model that did not prevent nation-state acquisition.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS | AML.T0103 - Deploy AI Agent | ARTEX deployed as an autonomous offensive agent |
| ATLAS | AML.T0047 - AI-Enabled Product or Service | AI tooling used to accelerate attack operations |
| ATLAS | AML.T0010 - AI Supply Chain Compromise | ConnectWise used as an entry vector to downstream victims |
| ATLAS | AML.T0012 - Valid Accounts | OAuth tokens and existing credentials abused for persistence |
| OWASP | LLM08 - Excessive Agency | AI agent operated autonomously with minimal human oversight |
| OWASP | LLM05 - Supply Chain Vulnerabilities | Compromise propagated through a trusted software supply chain |

## Impact Assessment

The operational tempo enabled by ARTEX fundamentally changes the defensive calculus. With 2,900 authentication attempts per minute, traditional detection windows are compressed to minutes rather than hours. Sectors with complex multi-tenant cloud environments — managed service providers, financial institutions, and government contractors — face the highest exposure. Microsoft confirmed no successful authentications in the October 10–14 window it monitored, but prior campaign phases resulted in genuine privileged access at multiple organisations.

## Mitigation & Recommendations

1. **Revoke unnecessary OAuth permissions**: Conduct an immediate audit of all third-party and first-party OAuth applications with delegated permissions in Microsoft 365. Remove any that cannot be verified as operationally required.
2. **Implement high-velocity sign-in alerting**: Configure SIEM rules to flag sign-in failure rates exceeding organisational baselines — Storm-0940's pattern of thousands of failures per minute is detectable if thresholds are set.
3. **Restrict ConnectWise integration scopes**: Review ConnectWise Cloud Backup service account permissions and limit to least privilege; rotate credentials if anomalous activity is suspected since September 2026.
4. **Enable Conditional Access policies**: Block legacy authentication protocols and enforce compliant device requirements to limit OAuth abuse vectors.
5. **Monitor for credential and privilege changes**: Alert on modifications to OAuth application credentials or role assignments outside change management windows.

## References

- [The Hacker News — China-Linked Hackers Use ARTEX AI Agents in ConnectWise Supply Chain Attack](https://thehackernews.com/2026/10/china-linked-hackers-use-artex-ai.html)
