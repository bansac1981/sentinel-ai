---
title: "Malicious Custom GPTs Weaponise ChatGPT as RAT Delivery Lure"
date: 2026-10-01T11:50:27+00:00
draft: true
slug: "malicious-custom-gpts-weaponise-chatgpt-as-rat-delivery-lure"

# ── Content metadata ──
summary: "Threat actors are creating malicious custom GPTs on the ChatGPT platform and abusing legitimate OpenAI and Google domains to execute ClickFix-style social engineering campaigns that deliver Remote Access Trojans to victims. By exploiting the trusted reputation of these platforms, attackers bypass conventional phishing defences and trick users into executing malware under the guise of interacting with an AI tool. This represents a significant escalation in the misuse of legitimate AI service infrastructure for malware distribution."
source: "Dark Reading"
source_url: "https://www.darkreading.com/cyberattacks-data-breaches/malicious-custom-gpts-chatgpt-rat-delivery-lure"
source_title: "Malicious Custom GPTs Turn ChatGPT Into RAT Delivery Lure"
source_date: 2026-09-30T21:25:47+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1658067923689-ba977e676120?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyN3x8bGFuZ3VhZ2UlMjB0cmFuc2xhdGlvbiUyMGFic3RyYWN0fGVufDB8MHx8fDE3OTA4NTU0Mjd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0114 - AI Service Web Interface", "AML.T0047 - AI-Enabled Product or Service", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0081 - Modify AI Agent Configuration", "AML.T0065 - LLM Prompt Crafting"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Threat actors deploy malicious custom GPTs on ChatGPT to deliver Remote Access Trojans via ClickFix-style lures."
tldr_who_at_risk: "General ChatGPT users and enterprise employees are most at risk due to overreliance on trusted AI platform domains that mask malicious intent."
tldr_actions: ["Block or monitor access to unverified third-party custom GPTs in enterprise environments", "Train users to recognise ClickFix-style copy-paste execution prompts, even when originating from AI platforms", "Implement endpoint detection rules for RAT indicators associated with ClickFix campaign payloads"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Supply Chain", "Industry News"]
tags: ["custom-gpts", "chatgpt-abuse", "rat-delivery", "clickfix", "social-engineering", "openai-platform", "malware-distribution", "legitimate-domain-abuse", "remote-access-trojan", "llm-lure"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-01T11:50:27+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/cyberattacks-data-breaches/malicious-custom-gpts-chatgpt-rat-delivery-lure"
pipeline_version: "2.1.0"
---

## Overview

Threat actors are weaponising OpenAI's custom GPT functionality to turn ChatGPT into a convincing malware delivery lure. Reported by Dark Reading, this campaign follows the established ClickFix social engineering pattern — where victims are deceived into manually executing malicious commands — but critically leverages the trusted domains of OpenAI and Google to add legitimacy. The technique represents a meaningful evolution in AI platform abuse, moving beyond prompt injection and jailbreaks into active malware distribution infrastructure.

## Technical Analysis

The attack chain begins with a threat actor creating a malicious custom GPT on the ChatGPT platform. Because custom GPTs are hosted under OpenAI's legitimate domain, they inherit the platform's trusted reputation in browser security indicators, email filters, and user perception. The GPT is designed to mimic a useful tool — likely a productivity, coding, or document assistant — and then presents the victim with a ClickFix-style prompt.

ClickFix attacks typically instruct users to open a Run dialog or terminal and paste a command string that the malicious interface provides, framing it as a necessary setup or verification step. In this campaign, the instruction appears to originate from a trusted AI assistant, dramatically increasing the probability of compliance. The command executes a Remote Access Trojan (RAT) payload, granting attackers persistent access to the victim's machine. Google domains are also cited as part of the lure infrastructure, suggesting possible abuse of Google-hosted redirects or documents to further obfuscate the payload delivery chain.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0114 (AI Service Web Interface):** Attackers directly abuse the ChatGPT web interface and custom GPT publishing mechanism as attack infrastructure.
- **AML.T0067 (LLM Trusted Output Components Manipulation):** The custom GPT's outputs are crafted to manipulate users into executing malicious commands by exploiting trust in the AI interface.
- **AML.T0081 (Modify AI Agent Configuration):** The custom GPT's system prompt and behaviour are configured by the attacker to serve as a social engineering and lure tool.

**OWASP LLM Top 10:**
- **LLM02 (Insecure Output Handling):** Malicious instructions rendered by the GPT interface lead directly to harmful user actions.
- **LLM09 (Overreliance):** Users place excessive trust in AI platform outputs, reducing critical scrutiny of instructions.
- **LLM07 (Insecure Plugin Design):** The custom GPT ecosystem lacks sufficient controls to prevent weaponised GPT publication.

## Impact Assessment

This attack targets the broad ChatGPT user base — including enterprise employees, developers, and non-technical users — all of whom may interact with custom GPTs without security vetting. The use of legitimate OpenAI and Google domains makes this attack particularly dangerous as it evades URL-based filtering and erodes user scepticism. Successful RAT installation provides attackers with persistent remote access, credential theft capability, lateral movement potential, and data exfiltration vectors. Organisations that have not governed employee use of third-party custom GPTs face elevated exposure.

## Mitigation & Recommendations

- **Govern custom GPT access:** Enterprise administrators should restrict or audit which custom GPTs employees can access via ChatGPT's enterprise controls.
- **User awareness training:** Specifically train users to identify ClickFix-style execution prompts — any AI tool requesting manual command execution should trigger immediate suspicion.
- **Endpoint protection:** Ensure EDR solutions are tuned to detect RAT behaviours and ClickFix-associated payload patterns.
- **DNS and proxy filtering:** Flag or block known RAT delivery domains at the network perimeter even when traffic originates from trusted platforms.
- **Report malicious GPTs:** Encourage users to report suspicious custom GPTs directly to OpenAI via platform reporting mechanisms.

## References

- [Dark Reading: Malicious Custom GPTs Turn ChatGPT Into RAT Delivery Lure](https://www.darkreading.com/cyberattacks-data-breaches/malicious-custom-gpts-chatgpt-rat-delivery-lure)
