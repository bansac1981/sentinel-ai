---
title: "Claude and ChatGPT Hijacked via Zero-Click Prompt Injection"
date: 2026-08-07T09:07:15+00:00
draft: true
slug: "claude-and-chatgpt-hijacked-via-zero-click-prompt-injection"

# ── Content metadata ──
summary: "Zenity researchers disclosed a zero-click attack chain capable of hijacking Claude and ChatGPT's agentic browser capabilities through malicious content embedded in emails and X posts. The vulnerabilities, reported to Anthropic and OpenAI in late 2025 and early 2026, remain unpatched as of publication. This represents a significant escalation in prompt injection risk, as no user interaction is required to trigger malicious AI agent behaviour."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/zero-click-ai-browser-hacking-claude-and-chatgpt-atlas-hijacked-via-emails-x-posts"
source_title: "Zero-Click AI Browser Hacking: Claude and ChatGPT Atlas Hijacked via Emails, X Posts"
source_date: 2026-08-06T12:54:09+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1633103144189-1c326abb537c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOXx8YnJva2VuJTIwZmVuY2UlMjBnYXAlMjBhYnN0cmFjdCUyMGxpZ2h0fGVufDB8MHx8fDE3ODYwOTM2MzV8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.0
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Zero-click prompt injection hijacks Claude and ChatGPT browser agents via emails and X posts."
tldr_who_at_risk: "Users of Claude and ChatGPT agentic browser features are directly exposed, as attackers can trigger malicious actions without any user interaction."
tldr_actions: ["Disable or restrict agentic browser automation features in Claude and ChatGPT until patches are available", "Audit AI agent permissions and apply least-privilege configurations to limit blast radius", "Monitor AI agent activity logs for anomalous actions triggered by external content"]

# ── Taxonomies ──
categories: ["Prompt Injection", "Agentic AI", "LLM Security", "Research"]
tags: ["zero-click", "prompt-injection", "claude", "chatgpt", "agentic-ai", "browser-agent", "zenity", "anthropic", "openai", "unpatched", "email-attack", "social-media-attack"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-07T09:07:15+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/zero-click-ai-browser-hacking-claude-and-chatgpt-atlas-hijacked-via-emails-x-posts"
pipeline_version: "2.1.0"
---

## Overview

Researchers at Zenity have uncovered a zero-click attack technique capable of hijacking the agentic browser capabilities of both Claude (Anthropic) and ChatGPT — specifically the Atlas agentic interface. The attack exploits prompt injection vulnerabilities embedded within everyday content sources, including emails and posts on X (formerly Twitter), requiring no deliberate interaction from the victim user. Zenity disclosed the findings to Anthropic and OpenAI in late 2025 and early 2026 respectively; as of the article's publication date of 6 August 2026, neither vendor has issued a patch.

The implications are severe: attackers can craft malicious content that, when processed by an AI browser agent on behalf of a user, silently redirects, exfiltrates data, or executes unintended agentic actions — all without the user clicking anything.

## Technical Analysis

The attack class is indirect prompt injection delivered through ambient data channels. When an AI browser agent reads an email or fetches an X post as part of an agentic task, adversarially crafted text within that content is interpreted as instructions by the underlying LLM. Because the agent operates with elevated permissions — browsing, form-filling, data retrieval — the injected instructions can achieve meaningful impact.

The "zero-click" designation is significant: traditional prompt injection typically requires a user to actively submit or copy malicious text. Here, the attack surface is any content the agent autonomously ingests during normal operation. An attacker need only post a crafted message on X or send a malicious email to a target whose AI agent is configured to process incoming communications.

No CVE identifiers were assigned at time of publication, and technical details of the specific payload structures have not been fully disclosed, consistent with responsible disclosure norms given the unpatched status.

## Framework Mapping

- **AML.T0051 – LLM Prompt Injection**: The core mechanism; adversarial instructions embedded in third-party content hijack agent behaviour.
- **AML.T0043 – Craft Adversarial Data**: Attacker-controlled emails and social media posts serve as the adversarial data delivery vehicle.
- **AML.T0057 – LLM Data Leakage**: Hijacked agents may exfiltrate user context, session data, or browsed content.
- **LLM01 – Prompt Injection** and **LLM08 – Excessive Agency**: The agent's broad permissions amplify the impact of a successful injection, a textbook excessive agency scenario.
- **LLM02 – Insecure Output Handling**: Agent outputs derived from injected instructions are acted upon without adequate sanitisation or confirmation.

## Impact Assessment

Any user leveraging Claude or ChatGPT in agentic browser modes — particularly those using features that process emails or social media feeds — is potentially exposed. Enterprise deployments where AI agents act on behalf of users with access to sensitive systems represent the highest-risk population. The zero-click nature of the attack lowers the barrier significantly compared to prior prompt injection techniques, making mass exploitation theoretically viable.

The fact that both vendors have had disclosure for six or more months without issuing patches raises accountability concerns and leaves a substantial user base at ongoing risk.

## Mitigation & Recommendations

- **Disable agentic browser features** where not operationally essential until patches are released by Anthropic and OpenAI.
- **Apply least-privilege agent configurations**: restrict what actions AI agents can take autonomously, particularly around data access and external communication.
- **Implement human-in-the-loop confirmation** for any agent action triggered by externally sourced content.
- **Monitor agent activity logs** for unexpected actions, especially those initiated after processing emails or social content.
- **Filter and sanitise inputs** to AI agents where technically feasible, treating all external content as untrusted.

## References

- [SecurityWeek – Zero-Click AI Browser Hacking: Claude and ChatGPT Atlas Hijacked via Emails, X Posts](https://www.securityweek.com/zero-click-ai-browser-hacking-claude-and-chatgpt-atlas-hijacked-via-emails-x-posts)
