---
title: "Prompt Injection Chain Breaks Cursor AI Sandbox, Enables Full RCE"
date: 2026-07-03T04:31:55+00:00
draft: false
slug: "prompt-injection-chain-breaks-cursor-ai-sandbox-enables-full-rce"

# ── Content metadata ──
summary: "Two critical vulnerabilities (CVE-2026-50548 and CVE-2026-50549) in the Cursor AI code editor allow prompt injection attacks delivered via MCP services or web search results to escape the editor's terminal sandbox and execute arbitrary commands on a developer's machine without any user interaction. Both flaws abuse the sandbox's write-permission logic \u2014 one through a misconfigured working directory parameter, the other through a symlink-resolution fallback \u2014 ultimately allowing overwrite of the sandbox helper binary itself. The attack surface is significant given Cursor's reported adoption across more than half of Fortune 500 companies; all versions prior to 3.0 remain vulnerable."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html"
source_title: "Critical Cursor Flaws Could Let Prompt Injection Escape Sandbox and Run Commands"
source_date: 2026-07-01T14:42:54+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1541057591128-caebf6d65c8b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNnx8Y29tcHV0ZXIlMjBzZWN1cml0eSUyMHNoaWVsZCUyMHdhcm5pbmd8ZW58MHwwfHx8MTc4MzA1MzExNXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Two critical Cursor IDE flaws let prompt injection escape the AI sandbox and run arbitrary commands."
tldr_who_at_risk: "Developers using Cursor versions prior to 3.0, especially enterprise users with cloud or SaaS workspaces connected to the editor."
tldr_actions: ["Update Cursor to version 3.0 or later immediately", "Audit MCP-connected services and restrict agent access to external or untrusted data sources", "Review terminal command logs for anomalous working_directory values or unexpected symlink usage"]

# ── Taxonomies ──
categories: ["Prompt Injection", "LLM Security", "Agentic AI", "Research"]
tags: ["cursor-ide", "prompt-injection", "sandbox-escape", "rce", "zero-click", "mcp", "agentic-ai", "cve-2026-50548", "cve-2026-50549", "dunesliide", "developer-tools", "symlink-vulnerability"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-07-03T04:31:55+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html"
pipeline_version: "2.1.0"
---

## Overview

Cato AI Labs has disclosed a critical vulnerability chain — dubbed **DuneSlide** — affecting the Cursor AI code editor, tracked as CVE-2026-50548 and CVE-2026-50549 (CVSS 9.8 / 9.3 under CVSS 4.0). The pair of flaws allow an attacker-controlled prompt, planted in an external data source the AI agent reads on behalf of a developer, to silently escape Cursor's terminal sandbox and execute arbitrary operating system commands. No user interaction is required beyond the developer's normal workflow — making this a zero-click attack vector.

Cursor's maker reports adoption across more than half of Fortune 500 companies. A patch is available in Cursor 3.0, released April 2, 2026. All prior versions are affected.

---

## Technical Analysis

Cursor's 2.x line introduced a default sandbox that restricts what commands issued by its AI agent can touch on the filesystem. DuneSlide breaks that containment through two distinct but mechanically similar paths:

**CVE-2026-50548 — Working Directory Abuse**

Cursor's `run_terminal_cmd` tool accepts an optional `working_directory` parameter. The sandbox permits writes within a command's working folder and automatically adds that path to the allowed-write list. Injected instructions set `working_directory` to a sensitive system path — such as the Cursor sandbox helper binary (`/Applications/Cursor.app/Contents/Resources/app/resources/helpers/cursorsandbox`) or a shell startup file like `~/.zshrc`. Cursor adds the attacker-specified path to the allowlist without validation, and the agent overwrites the target, disabling sandbox enforcement for all subsequent commands.

**CVE-2026-50549 — Symlink Resolution Fallback**

Before writing a file, Cursor resolves symlinks to confirm the real destination resides inside the project directory. The vulnerability is in the error handling: if resolution fails — because the target does not exist or read access on a path component has been revoked — Cursor falls back to trusting the symlink's apparent in-project path. An attacker crafts a symlink that appears to point inside the project but resolves to the same sandbox helper. By engineering a resolution failure at check time, the write proceeds unchallenged through the symlink to the external target.

In both cases, once the sandbox helper is neutralised, the next agent-issued terminal command runs with the developer's full OS privileges.

**Delivery mechanism:** Injected instructions are embedded in content the agent fetches autonomously — MCP-connected services, web search results, or repository files. The developer triggers the chain simply by asking a routine question.

---

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0051 — LLM Prompt Injection | Core delivery mechanism via external data sources |
| MITRE ATLAS | AML.T0047 — ML-Enabled Product or Service | Cursor as the exploited AI-integrated product |
| MITRE ATLAS | AML.T0043 — Craft Adversarial Data | Attacker-crafted content designed to manipulate agent behaviour |
| OWASP LLM01 | Prompt Injection | Canonical prompt injection via indirect data channel |
| OWASP LLM08 | Excessive Agency | Agent executes filesystem and terminal actions with insufficient constraint |
| OWASP LLM07 | Insecure Plugin Design | MCP integration surface exposes agent to untrusted input |

---

## Impact Assessment

Successful exploitation grants full shell access on the developer's machine under their own credentials. Any cloud platforms, SaaS workspaces, or code repositories the editor session is authenticated to are consequently exposed. The zero-click nature and the legitimacy of the triggering workflow (a normal developer query) make detection and prevention particularly difficult at the endpoint level. Enterprise environments with broad Cursor adoption face compounded supply chain risk if compromised developer machines access shared infrastructure.

No known in-the-wild exploitation has been reported as of publication.

---

## Mitigation & Recommendations

- **Update immediately:** Upgrade to Cursor 3.0 or later. All earlier versions are vulnerable.
- **Restrict MCP surface:** Limit agent integrations to trusted, well-scoped MCP services; disable connections to public or untrusted external sources where possible.
- **Apply least-privilege principles:** Ensure the Cursor process operates under a user account with minimal necessary filesystem and cloud permissions.
- **Audit agent activity:** Review terminal command logs for anomalous `working_directory` values or unexpected symlink creation in project directories.
- **Treat external agent inputs as untrusted:** Any content fetched autonomously by an AI agent — web pages, API responses, file contents — should be treated as a potential injection vector in your threat model.

---

## References

- [The Hacker News — Critical Cursor Flaws Could Let Prompt Injection Escape Sandbox and Run Commands](https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html)
