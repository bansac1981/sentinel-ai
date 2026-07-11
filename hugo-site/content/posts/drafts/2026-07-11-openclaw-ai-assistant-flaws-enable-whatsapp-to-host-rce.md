---
title: "OpenClaw AI Assistant Flaws Enable WhatsApp-to-Host RCE"
date: 2026-07-11T10:39:39+00:00
draft: false 
slug: "openclaw-ai-assistant-flaws-enable-whatsapp-to-host-rce"

# ── Content metadata ──
summary: "Three high-severity vulnerabilities in OpenClaw, a personal AI assistant, have been chained to enable remote code execution on the host system via a WhatsApp message, requiring no prior foothold. The flaws\u2014covering OS command injection, incomplete input filtering, and path traversal\u2014allow sandbox escape, credential theft, and privilege escalation. All three have been patched in OpenClaw version 2026.6.6, but unpatched deployments remain at significant risk."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/07/researcher-details-whatsapp-to-host.html"
source_title: "Researcher Details WhatsApp-to-Host Attack Chain Using Three OpenClaw Flaws"
source_date: 2026-07-10T14:19:50+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/17489156/pexels-photo-17489156.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Three OpenClaw flaws chain a WhatsApp message into full host-level remote code execution."
tldr_who_at_risk: "Users and operators running unpatched OpenClaw AI assistant instances, especially those with channel-facing agents and exec permissions enabled."
tldr_actions: ["Upgrade OpenClaw to version 2026.6.6 immediately", "Remove 'exec' from the tool allowlist for channel-facing agents", "Enable sandbox mode for all non-main sessions and monitor for git clone commands using the 'ext::' protocol helper"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Research"]
tags: ["openclaw", "rce", "sandbox-escape", "command-injection", "path-traversal", "credential-theft", "whatsapp", "ai-assistant", "host-escape", "bind-mount", "privilege-escalation", "ghsa"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-07-11T10:39:39+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/07/researcher-details-whatsapp-to-host.html"
pipeline_version: "2.1.0"
---

## Overview

Three high-severity security vulnerabilities in OpenClaw, a personal AI assistant platform, have been publicly detailed by researcher Chinmohan Nayak. When chained together, the flaws allow an attacker to send a crafted message via WhatsApp and achieve arbitrary code execution on the underlying host—without requiring any prior foothold in the target environment. All three bugs have been patched in OpenClaw version 2026.6.6, but the attack chain represents a significant escalation in the threat landscape for agentic AI assistants.

## Technical Analysis

The three vulnerabilities are:

- **GHSA-hjr6-g723-hmfm (CVSS 8.8):** OS command injection combined with an incomplete blocklist in the host execution environment filtering mechanism. Allows execution or persistence of actions beyond the caller's intended authorisation.
- **GHSA-9969-8g9h-rxwm (CVSS 8.8):** An identical class of flaw—OS command injection and incomplete input filtering—affecting the same filtering mechanism via a separate code path.
- **GHSA-575v-8hfq-m3mc (CVSS 8.4):** A path traversal and link-following vulnerability in sandbox bind mount logic. The `getBlockedReasonForSourcePath()` function checks whether a source path falls under a blocked directory, but never performs the inverse check—whether a blocked path is a subdirectory of a permitted mount source.

The bind mount denylist blocks specific sensitive directories such as `~/.ssh`, `~/.aws`, and `~/.gnupg`. However, an attacker can mount the parent directory `/home` or `/var` into the container, bypassing individual blocks entirely. Mounting `/home` exposes all users' SSH keys, AWS credentials, and GPG secrets. Mounting `/var` exposes the Docker socket, enabling a full host escape from within the supposedly sandboxed environment.

Nayak demonstrated that these three flaws can be triggered in sequence from an external WhatsApp message—no prior access required—making this a zero-interaction remote compromise path.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection):** The external WhatsApp message acts as untrusted input that propagates through the AI agent's tool-use pipeline, triggering dangerous system-level actions.
- **AML.T0047 (ML-Enabled Product or Service):** OpenClaw is an AI assistant product whose agentic capabilities extend the attack surface to host-level operations.
- **LLM07 (Insecure Plugin Design):** The exec tool and bind mount mechanisms expose dangerous OS primitives without adequate authorisation controls.
- **LLM08 (Excessive Agency):** The AI assistant possesses and exercises system-level permissions (file mounting, command execution) that exceed what is necessary for safe operation.
- **LLM06 (Sensitive Information Disclosure):** SSH keys, AWS credentials, and GPG secrets are directly accessible via the path traversal flaw.

## Impact Assessment

Any operator running OpenClaw prior to version 2026.6.6 with channel-facing agents (e.g., WhatsApp integrations) and exec or mount permissions enabled is directly exposed. Unlike the previously disclosed Claw Chain vulnerabilities (Cyera, May 2026), these flaws require no prior foothold—widening the potential attacker pool to any party capable of sending a WhatsApp message to the target's connected account. Credential theft, persistent backdoor installation, and full host escape are all achievable outcomes.

## Mitigation & Recommendations

1. **Upgrade immediately** to OpenClaw version 2026.6.6.
2. **Enable sandbox mode** for all non-main sessions.
3. **Remove `exec`** from the tool allowlist for any channel-facing or lower-trust agents.
4. **Monitor** for git clone commands using the `ext::` external protocol helper, which can be abused for arbitrary command execution.
5. **Restrict or disable** affected features for non-trusted operators until patching is confirmed.

## References

- [The Hacker News – Original Article](https://thehackernews.com/2026/07/researcher-details-whatsapp-to-host.html)
