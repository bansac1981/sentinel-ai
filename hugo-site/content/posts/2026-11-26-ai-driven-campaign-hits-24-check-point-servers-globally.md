---
title: "AI-Driven Campaign Hits 24 Check Point Servers Globally"
date: 2026-11-26T15:34:40+00:00
draft: false
slug: "ai-driven-campaign-hits-24-check-point-servers-globally"

# ── Content metadata ──
summary: "An unknown threat actor tracked as GreyNoise Threat 13 (GT13) has compromised 24 Check Point Security Management servers across 22 organisations worldwide, using suspected AI-driven agentic tooling to automate scanning, exploitation, and post-compromise operations. The campaign exploited CVE-2026-61500 in Rejetto HFS as a relay pivot, then leveraged CVE-2026-16232 against Check Point to steal firewall databases, mint certificates, and disable security policies. The use of agentic harnesses to orchestrate multi-stage intrusion activity at scale marks a significant escalation in operationally autonomous offensive AI use."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/hackers-compromise-24-check-point.html"
source_title: "Hackers Compromise 24 Check Point Management Servers in Suspected AI-Driven Attack Campaign"
source_date: 2026-11-25T06:50:19+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1744640326166-433469d102f2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMHx8QWdlbnRpYyUyMEFJJTIwY3liZXJzZWN1cml0eSUyMHRlY2hub2xvZ3l8ZW58MHwwfHx8MTc5NTcwNzI3OXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0103 - Deploy AI Agent", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Unknown actor uses AI-driven agentic tooling to compromise 24 Check Point management servers globally."
tldr_who_at_risk: "Organisations running Check Point Security Management Servers in finance, energy, government, and manufacturing sectors are most exposed, particularly those with unpatched CVE-2026-16232."
tldr_actions: ["Immediately apply patches for CVE-2026-16232 on all Check Point Security Management Servers", "Audit and rotate internal CA certificates and firewall policy configurations for signs of tampering", "Block or restrict management server egress and monitor for tools like Chisel, Impacket, and Paramiko on network segments"]

# ── Taxonomies ──
categories: ["Agentic AI", "Industry News", "LLM Security"]
tags: ["check-point", "agentic-ai", "offensive-ai", "cve-2026-61500", "cve-2026-16232", "rejetto-hfs", "greynoise", "gt13", "lateral-movement", "firewall-bypass", "automated-exploitation", "network-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-26T15:34:40+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/hackers-compromise-24-check-point.html"
pipeline_version: "2.1.0"
content_hash: "15b4deb4cf4f6339"
---

## Overview

An unattributed threat actor tracked by GreyNoise as **GreyNoise Threat 13 (GT13)** has conducted a large-scale intrusion campaign targeting Check Point Security Management Servers, confirming compromise of **24 servers across 22 distinct organisations** between October 17 and November 2, 2026. The campaign is notable for its suspected use of **AI-driven agentic tooling** to automate vulnerability scanning, exploitation, and post-compromise interaction — representing one of the first confirmed operational deployments of autonomous offensive AI infrastructure against enterprise network security appliances.

Victim organisations span financial services, energy, government, transportation, mining, engineering, and manufacturing sectors across 17 countries including the U.S., U.K., Germany, India, and Australia.

## Technical Analysis

GT13 used **99 IP addresses**, predominantly egressing through ExpressVPN or routed via previously compromised Check Point devices, generating over 1,400 network sessions, 800+ command-line artifacts, and 1,200+ file operations.

The intrusion chain began with an **automated scanning and exploitation pipeline** targeting a Rejetto HFS server via **CVE-2026-61500**, a critical vulnerability, in early October 2026. This allowed the attacker to execute commands, including injecting an SSH key into `/root/.ssh/authorized_keys` for persistent access.

The compromised HFS server was subsequently used as a **relay** for operations against 24 Check Point Security Management Servers that the actor had already silently accessed — the initial vector into those assets remains undetermined.

Using a script exploiting the now-patched **CVE-2026-16232**, GT13 launched over 100 management tasks including:
- Exfiltrating firewall databases and internal CA certificate files
- Minting new certificates
- Unloading security policies, effectively **disabling firewall protections**
- Conducting internal reconnaissance and lateral movement

Standard red-team tooling was observed throughout: **Nmap** (scanning), **Chisel** (tunnelling), **Impacket** and **Paramiko** (credential abuse and SSH interaction), and custom Python scripts. An attempt to deploy a Linux implant named **ZULT** to the HFS relay server was unsuccessful.

The suspected use of **agentic harnesses** — autonomous AI systems capable of chaining tool invocations, interpreting outputs, and adapting actions without human-in-the-loop intervention — is what elevates this campaign. This pattern mirrors research scenarios in which LLM-powered agents autonomously exploit vulnerabilities after minimal initial prompting.

## Framework Mapping

- **AML.T0047 (AI-Enabled Product or Service)**: The attacker weaponised AI tooling as an operational offensive capability.
- **AML.T0103 (Deploy AI Agent)**: Agentic harnesses were reportedly used to orchestrate multi-stage exploitation autonomously.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: Tool calls (file downloads, SSH commands) were automated to exfiltrate firewall databases and certificates.
- **LLM08 (Excessive Agency)**: The autonomous decision-making capacity attributed to the agentic pipeline reflects the core risk of unconstrained AI agency in offensive contexts.

## Impact Assessment

The disabling of firewall security policies across 24 management servers represents a severe operational impact — effectively blinding or neutralising perimeter defences for affected organisations. Exfiltration of internal CA files and certificates enables potential long-term trust chain abuse. The multi-sector, multi-country scope suggests opportunistic targeting at scale enabled by automation.

## Mitigation & Recommendations

1. **Patch immediately**: Apply all available fixes for CVE-2026-16232 on Check Point Security Management Servers and CVE-2026-61500 on any Rejetto HFS deployments.
2. **Audit certificate infrastructure**: Revoke and re-issue any internal CA certificates that may have been exposed; check for unauthorised certificate minting.
3. **Review firewall policy state**: Verify security policy load status across all managed gateways for signs of unloading.
4. **Hunt for tooling indicators**: Scan internal networks for Chisel tunnels, Paramiko-based SSH sessions, and Python scripts associated with Impacket.
5. **Restrict management server access**: Enforce strict IP allowlisting and MFA for Check Point management interfaces; block unnecessary egress.
6. **Monitor for agentic behaviour patterns**: Anomalous high-velocity, low-latency command sequences may indicate AI-orchestrated activity rather than human operators.

## References

- [The Hacker News — Original Report](https://thehackernews.com/2026/11/hackers-compromise-24-check-point.html)
