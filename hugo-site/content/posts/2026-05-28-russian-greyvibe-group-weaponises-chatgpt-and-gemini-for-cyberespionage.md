---
title: "GreyVibe Weaponizes ChatGPT and Gemini for Ukraine Cyberespionage"
date: "2026-05-29T00:21:08+00:00"
draft: false 
slug: "russian-greyvibe-group-weaponises-chatgpt-and-gemini-for-cyberespionage"

# ── Content metadata ──
summary: "A likely Russian threat group dubbed GreyVibe has been actively using commercial LLMs \u2014 including ChatGPT and Google Gemini \u2014 to generate high-quality phishing lures, malware tooling, and social-engineering content targeting Ukrainian military, government, and civilian organisations. WithSecure researchers identified LLM artefact markers embedded in campaign imagery, confirming AI-assisted content generation at scale. The case represents a concrete, documented example of adversarial LLM weaponisation in an active nation-state-adjacent cyberespionage campaign."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/greyvibe-hackers-use-chatgpt-gemini-to-power-cyberattacks/"
source_title: "GreyVibe hackers use ChatGPT, Gemini to power cyberattacks"
source_date: 2026-05-28T22:24:49+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1674027444636-ce7379d51252?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMHx8YXJ0aWZpY2lhbCUyMGludGVsbGlnZW5jZSUyMHRlY2hub2xvZ3klMjBuZXVyYWwlMjBuZXR3b3JrfGVufDB8MHx8fDE3ODAwMTIzNDl8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 7.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data", "AML.T0051 - LLM Prompt Injection"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Russian-linked GreyVibe used ChatGPT and Gemini to craft realistic phishing lures targeting Ukrainian entities."
tldr_who_at_risk: "Ukrainian military, government, telecom, and energy organisations are primary targets; any org in the conflict zone or supporting Ukraine is exposed."
tldr_actions: ["Block or alert on LLM-generated content markers in email attachments and web assets", "Train staff to recognise AI-enhanced phishing lures, including hyper-realistic decoy PDFs and fake CAPTCHA flows", "Restrict execution of clipboard-injected commands and enforce application allowlisting to counter ClickFix-style delivery"]

# ── Taxonomies ──
categories: ["LLM Security", "Industry News", "Research"]
tags: ["greyvibe", "llm-weaponisation", "spear-phishing", "chatgpt-abuse", "google-gemini", "cyberespionage", "ukraine", "russia", "ai-generated-lures", "withsecure", "android-spyware", "social-engineering"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state"]

# ── Pipeline metadata ──
fetched_at: "2026-05-28T23:52:29+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/greyvibe-hackers-use-chatgpt-gemini-to-power-cyberattacks/"
pipeline_version: "1.0.0"
---

## Overview

A threat group tracked as GreyVibe — assessed with moderate confidence as Russian-aligned — has been running a multi-vector cyberespionage campaign since at least August 2025. Discovered by WithSecure in January 2026, the operation targets Ukrainian and Ukraine-adjacent organisations across military, government, civilian, and commercial sectors. What distinguishes GreyVibe from typical APT campaigns is the documented, forensically verified use of commercial large language models — including OpenAI's ChatGPT, Google Gemini, and Ideogram AI — to generate lures, content, and tooling at scale.

LLM artefact markers were identified by WithSecure researchers directly within campaign imagery, providing rare empirical evidence of AI-assisted threat actor operations rather than speculation.

## Technical Analysis

GreyVibe operated at least five distinct attack chains:

- **PhantomMail**: Spear-phishing emails delivering malicious ZIP/RAR archives via Google Drive and 4sync. Decoy PDFs impersonated Ukrainian government, telecom, and energy entities.
- **PhantomClick**: Fake CAPTCHA and ClickFix pages mimicking Zoom and LAPAS portals, using fake Cloudflare verification prompts to trick victims into self-executing malicious commands via clipboard injection.
- **PrincessClub**: Fake adult/dating websites deploying FallSpy Android spyware and PhantomRelay/LegionRelay Windows malware. Operators used fake female Telegram personas and later escalated to WebRTC-based live calls capable of capturing victim audio and video.
- **DroneLink**: Fake Ukrainian military charity sites themed around FPV drones and UAVs, sharing infrastructure and tooling with PrincessClub.
- **Nebo**: Fake Russian military communications login pages designed to socially engineer Ukrainian military personnel.

AI tools were used to generate the realistic imagery, written content, and personas underpinning these campaigns. Custom malware families referenced include LOOKVALPS, LOOKVALJS, DAYLIGHT, and TEAS (names partially captured in the source). The C2 infrastructure operated on UTC+3 (Moscow time), and Russian-language artefacts appear throughout code comments and panel interfaces.

## Framework Mapping

- **AML.T0047 (ML-Enabled Product or Service)**: GreyVibe directly leveraged public LLM APIs and products as force multipliers for content generation and social engineering.
- **AML.T0043 (Craft Adversarial Data)**: AI-generated imagery and documents were crafted to deceive targets and evade human suspicion.
- **LLM02 (Insecure Output Handling)**: LLM-generated content was deployed without safety controls being triggered in ways that caused downstream harm to end users.
- **LLM09 (Overreliance)**: Victims and potentially defenders may over-trust AI-generated artefacts as legitimate.

## Impact Assessment

The immediate impact is concentrated on Ukrainian and Ukraine-supporting organisations. However, the operational template — using commodity LLMs to produce high-fidelity, localised phishing and social engineering content at low cost — is highly transferable. The documented forensic evidence of LLM use in an active espionage campaign sets a precedent and signals that AI-assisted threat operations will become a standard TTPs baseline rather than an emerging curiosity.

FallSpy Android spyware and the WebRTC audio/video capture capability represent a significant HUMINT-grade collection threat against individuals in sensitive roles.

## Mitigation & Recommendations

- **Detect LLM artefacts**: Implement tooling to scan inbound documents and images for known LLM generation markers (metadata, watermarking signals, stylistic signatures).
- **ClickFix / clipboard injection controls**: Enforce policies that prevent execution of commands pasted from web content; deploy endpoint controls blocking PowerShell/cmd execution from browser processes.
- **Mobile device management**: Restrict sideloading on organisational Android devices and deploy MTD (Mobile Threat Defence) solutions capable of detecting FallSpy-class spyware.
- **Personnel awareness**: Brief high-risk staff — particularly those in military or government roles — on AI-enhanced social engineering including fake personas conducting live video calls.
- **Threat intelligence sharing**: Circulate WithSecure's IoCs across ISAC networks relevant to defence, energy, and government sectors.

## References

- [GreyVibe hackers use ChatGPT, Gemini to power cyberattacks — BleepingComputer](https://www.bleepingcomputer.com/news/security/greyvibe-hackers-use-chatgpt-gemini-to-power-cyberattacks/)
