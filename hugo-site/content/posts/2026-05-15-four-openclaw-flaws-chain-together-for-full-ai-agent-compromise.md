---
title: "CVE-2026-44112: OpenClaw Chain RCE and Privilege Escalation"
date: "2026-05-15T21:24:57+00:00"
draft: false 
slug: "four-openclaw-flaws-chain-together-for-full-ai-agent-compromise"

# ── Content metadata ──
summary: "Researchers at Cyera disclosed four vulnerabilities in OpenClaw, an AI agent runtime platform, that can be chained to achieve credential theft, privilege escalation, and persistent backdoor access. The attack chain, dubbed 'Claw Chain', exploits sandbox escapes, allowlist bypasses, and a spoofable ownership flag in the MCP loopback runtime to weaponise the agent's own privileges against the host environment. All four CVEs have been patched in OpenClaw version 2026.4.22 and users should update immediately."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html"
source_title: "Four OpenClaw Flaws Enable Data Theft, Privilege Escalation, and Persistence"
source_date: 2026-05-15T13:35:04+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1667264501379-c1537934c7ab?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMHx8Y2xvdWQlMjBjb21wdXRpbmclMjBzZXJ2ZXIlMjBkYXRhJTIwY2VudGVyfGVufDB8MHx8fDE3Nzg4NjMzNDd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.9
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0018 - Backdoor ML Model", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Four chained OpenClaw flaws enable sandbox escape, credential theft, privilege escalation, and backdoor persistence in AI agent runtimes."
tldr_who_at_risk: "Any organisation running OpenClaw-based AI agents prior to version 2026.4.22 is directly exposed to full runtime compromise."
tldr_actions: ["Upgrade OpenClaw to version 2026.4.22 immediately", "Audit AI agent plugins and external inputs for signs of malicious injection", "Review MCP loopback token configurations and revoke any untrusted bearer tokens"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Prompt Injection", "Research"]
tags: ["openclaw", "cve-2026-44112", "cve-2026-44113", "cve-2026-44115", "cve-2026-44118", "sandbox-escape", "privilege-escalation", "toctou", "mcp", "ai-agent", "data-theft", "persistence", "cyera", "claw-chain", "patch-advisory"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-15T16:42:27+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html"
pipeline_version: "1.0.0"
---

## Overview

Cybersecurity firm Cyera has disclosed four security vulnerabilities in OpenClaw, an AI agent runtime platform, that can be chained into a full attack sequence enabling credential theft, privilege escalation, and persistent backdoor installation. Collectively named **Claw Chain**, the vulnerability set is particularly significant because it exploits the trust model baked into AI agent execution environments — turning the agent's own runtime privileges against the host system.

All four CVEs were responsibly disclosed and have been patched in **OpenClaw version 2026.4.22**.

---

## Technical Analysis

The four vulnerabilities span different layers of the OpenClaw stack:

- **CVE-2026-44112 (CVSS 9.6)** — A TOCTOU race condition in the OpenShell managed sandbox backend. An attacker can race the check-use window to redirect filesystem writes outside the intended mount root, enabling backdoor planting and configuration tampering.

- **CVE-2026-44113 (CVSS 7.7)** — A companion TOCTOU flaw allowing reads outside the sandbox mount root, exposing system files, credentials, and internal secrets.

- **CVE-2026-44115 (CVSS 8.8)** — An incomplete disallowed-inputs list that allows shell expansion tokens embedded within heredoc bodies to slip past allowlist validation, executing unapproved commands at runtime.

- **CVE-2026-44118 (CVSS 7.8)** — An improper access control flaw in the MCP loopback runtime. OpenClaw trusted a client-controlled flag (`senderIsOwner`) to determine owner-level access without validating it against the authenticated session. A non-owner client could spoof this flag to gain full control over gateway configuration, cron scheduling, and execution environment management.

The **exploitation chain** follows four stages:
1. Initial code execution via malicious plugin, prompt injection, or compromised external input inside the OpenShell sandbox.
2. Leverage CVE-2026-44113 and CVE-2026-44115 to exfiltrate credentials, secrets, and sensitive files.
3. Exploit CVE-2026-44118 to escalate to owner-level agent runtime control.
4. Use CVE-2026-44112 to plant backdoors and establish persistence.

---

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS AML.T0051 | LLM Prompt Injection | Initial foothold vector via injected agent inputs |
| ATLAS AML.T0057 | LLM Data Leakage | CVE-2026-44113 exposes credentials and internal artifacts |
| ATLAS AML.T0018 | Backdoor ML Model | CVE-2026-44112 enables persistent backdoor planting |
| ATLAS AML.T0012 | Valid Accounts | CVE-2026-44118 exploits trusted identity flags |
| OWASP LLM07 | Insecure Plugin Design | Malicious plugin as initial entry point |
| OWASP LLM08 | Excessive Agency | Agent runtime privileges weaponised against the host |
| OWASP LLM06 | Sensitive Information Disclosure | Credential and secrets exfiltration via sandbox escape |

---

## Impact Assessment

Organisations running OpenClaw-backed AI agents in production environments are at risk of complete runtime compromise. The severity is elevated by the chained nature of the flaws — each step amplifies the next, moving from limited sandbox access to persistent host-level control. Environments where agents have access to secrets stores, internal APIs, or scheduling systems face the highest exposure.

---

## Mitigation & Recommendations

- **Patch immediately**: Upgrade to OpenClaw version 2026.4.22, which issues separate owner/non-owner bearer tokens and eliminates the spoofable `senderIsOwner` header.
- **Audit plugin inputs**: Review all registered agent plugins and external input sources for signs of injection or tampering.
- **Restrict agent privileges**: Apply least-privilege principles to agent runtime environments; limit filesystem and scheduling access.
- **Monitor for anomalous agent behaviour**: Set alerts on unexpected file access patterns or configuration changes initiated by agent processes.

---

## References

- [The Hacker News — Original Article](https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html)
