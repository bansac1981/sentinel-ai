---
title: "Meta Muse AI Agent Hijacked via Hidden Dictation Endpoint"
date: 2026-09-22T08:21:57+00:00
draft: true
slug: "meta-muse-ai-agent-hijacked-via-hidden-dictation-endpoint"

# ── Content metadata ──
summary: "Security researcher Patrick Wardle demonstrated a proof-of-concept attack against Meta's Muse AI assistant on macOS, showing that a hidden, undocumented preference key (`endo_voyager_dictation_endpoint`) can be silently modified by any process running as the logged-in user to redirect dictation audio and session tokens to an attacker-controlled server. The attack requires local code execution but can be bootstrapped remotely via a ClickFix social-engineering lure, requiring no download or installation. Once hijacked, an attacker can inject malicious instructions into Muse, capture its authentication token, and control the assistant across all of the victim's linked devices \u2014 including mobile and smart-home integrations."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/one-hidden-meta-muse-setting-could-let.html"
source_title: "One Hidden Meta Muse Setting Could Let Attackers Turn the AI Assistant Into a Backdoor"
source_date: 2026-09-22T06:33:57+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/37724298/pexels-photo-37724298.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.1
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0081 - Modify AI Agent Configuration", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0051 - LLM Prompt Injection", "AML.T0113 - Steal Web Session Cookie", "AML.T0080 - AI Agent Context Poisoning", "AML.T0098 - AI Agent Tool Credential Harvesting"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Hidden macOS preference key lets attackers redirect Meta Muse dictation and steal its session token."
tldr_who_at_risk: "macOS users who have installed Meta Muse and granted it broad access to files, email, messages, calendar, and smart-home apps are directly exposed."
tldr_actions: ["Avoid installing Meta Muse until Meta issues a patch addressing the undocumented dictation endpoint", "Audit macOS app preferences for unexpected changes to endo_voyager_dictation_endpoint", "Apply least-privilege principles — revoke Muse permissions for email, files, and smart-home integrations if already installed"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Prompt Injection", "Research"]
tags: ["meta-muse", "ai-agent-hijacking", "macos-vulnerability", "dictation-endpoint", "session-token-theft", "clickfix", "local-privilege-abuse", "agentic-ai", "patrick-wardle", "proof-of-concept", "smart-home", "cross-device-attack"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-22T08:21:57+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/one-hidden-meta-muse-setting-could-let.html"
pipeline_version: "2.1.0"
---

## Overview

Security researcher Patrick Wardle published a proof-of-concept on September 21, 2026, demonstrating that Meta's newly launched Muse AI assistant for macOS can be silently converted into an attacker-controlled backdoor by modifying a single, undocumented application preference. The vulnerability does not break into macOS independently, but it weaponises the broad delegated access that users willingly grant to Muse — including files, email, messages, calendar, shopping, and smart-home systems — making the attack surface proportional to the trust the victim has placed in the assistant.

## Technical Analysis

The core of the issue is an undocumented macOS preferences key, `endo_voyager_dictation_endpoint`, stored in the Muse app's preferences domain. Any process running as the logged-in user can write to this key without requiring elevated permissions or any additional entitlements — a consequence of macOS's permissive user-level preferences model.

Once the key is overwritten to point at an attacker-controlled server, the following chain occurs:

1. **Dictation interception**: When the victim taps the microphone and speaks a prompt, both the raw audio and its transcription are routed to the attacker's server rather than to Meta's backend.
2. **Prompt injection**: The attacker's proxy can append or replace instructions before forwarding the request to Meta, causing Muse to execute commands the user never issued.
3. **Token harvesting**: Muse includes its authentication token in the redirected dictation request. The attacker captures this token and can use it to authenticate to Muse's API independently, gaining persistent access to the user's Muse account and its full chat history.
4. **Cross-device lateral movement**: Because a Muse account supports multiple linked devices, the stolen token allows the attacker to direct Muse on the victim's iPhone — demonstrated by Wardle to retrieve GPS location, run a Bluetooth device scan, and enumerate available smart-home commands.

The initial foothold required for local code execution can be achieved without any file download via a **ClickFix** social-engineering lure, which tricks the user into pasting and running a single terminal command.

Notably, macOS security tooling may not flag the activity because all commands originate from Muse itself — a legitimately signed, notarised application.

## Framework Mapping

- **AML.T0081 (Modify AI Agent Configuration)**: Direct manipulation of the dictation endpoint preference is the primary attack vector.
- **AML.T0083 / AML.T0098 (Credentials from AI Agent Configuration / Tool Credential Harvesting)**: The session token is exfiltrated as a side-effect of the redirected request.
- **AML.T0051 (LLM Prompt Injection)**: The attacker injects malicious instructions into the proxied dictation stream.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: Location data, Bluetooth scans, and smart-home capabilities are exfiltrated through Muse's own legitimate tool integrations.
- **LLM08 (Excessive Agency)**: Muse's broad, delegated access across multiple device types and services is the amplifier that makes the token theft critically impactful.

## Impact Assessment

The attack affects any macOS user running Meta Muse who has granted it access to personal data or device integrations. The severity is elevated by three factors: the undocumented nature of the exploited preference (no user-visible indicator), the absence of additional permission prompts, and the cross-device scope of token reuse. Security software is unlikely to detect the activity because it originates from a trusted, signed process.

## Mitigation & Recommendations

- **Do not install Meta Muse** until Meta issues a fix that restricts write access to the dictation endpoint preference or removes the undocumented key entirely.
- **Revoke existing Muse permissions** for email, files, calendar, and smart-home integrations via macOS System Settings > Privacy & Security if Muse is already installed.
- **Monitor macOS user defaults** for unexpected writes to `endo_voyager_dictation_endpoint` using endpoint detection tooling.
- **Educate users** on ClickFix-style social engineering — no legitimate service requires users to paste commands into Terminal.
- **Meta should deprecate** or cryptographically sign the dictation endpoint preference to prevent unauthorised modification.

## References

- [Original article — The Hacker News, September 22 2026](https://thehackernews.com/2026/09/one-hidden-meta-muse-setting-could-let.html)
