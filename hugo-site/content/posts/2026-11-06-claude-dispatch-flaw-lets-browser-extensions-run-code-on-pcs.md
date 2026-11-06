---
title: "Claude Dispatch Flaw Lets Browser Extensions Run Code on PCs"
date: 2026-11-06T13:07:03+00:00
draft: false
slug: "claude-dispatch-flaw-lets-browser-extensions-run-code-on-pcs"

# ── Content metadata ──
summary: "Researchers at Forever Security demonstrated that a malicious or compromised browser extension running on claude.ai could abuse Claude's Dispatch feature to silently issue commands to Claude Desktop, achieving arbitrary code execution on the user's machine. The attack chain requires no browser exploit \u2014 only a signed-in session and Dispatch enabled \u2014 and Claude's own confirmation prompts are auto-clicked by the extension script. Anthropic acknowledged the flaw in May 2026 and has signalled Dispatch will be retired, though the feature remains partially active."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/malicious-browser-extensions-could-use.html"
source_title: "Malicious Browser Extensions Could Use Claude Dispatch to Run Code on Users' Computers"
source_date: 2026-11-06T12:06:35+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1730373538355-bf404a18b9f2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8b3BlbiUyMGJvb2slMjBrbm93bGVkZ2UlMjBjb25jZXB0fGVufDB8MHx8fDE3OTM5NzA0MjJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0080 - AI Agent Context Poisoning", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0114 - AI Service Web Interface"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Malicious browser extensions can abuse Claude Dispatch to silently execute code on a user's computer."
tldr_who_at_risk: "Users running Claude Desktop with Dispatch enabled and any browser extension active on claude.ai are directly exposed to arbitrary code execution."
tldr_actions: ["Disable Claude Dispatch immediately if not required, especially on work devices", "Audit browser extensions with access to claude.ai and remove any untrusted or unverified ones", "Apply least-privilege principles to Claude Desktop's OS permissions to limit potential damage"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research"]
tags: ["claude", "anthropic", "claude-desktop", "browser-extension", "dispatch", "code-execution", "agentic-ai", "prompt-injection", "npm", "forever-security", "cross-device", "llm-agent"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-11-06T13:07:03+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/malicious-browser-extensions-could-use.html"
pipeline_version: "2.1.0"
content_hash: "918b9ba0b4f8ff71"
---

## Overview

Researchers at Forever Security have demonstrated a practical attack chain in which a malicious — or silently compromised — browser extension running on `claude.ai` can instruct Claude Desktop to execute arbitrary code on the user's computer, requiring no browser exploit whatsoever. The root cause is Claude's Dispatch feature, which was designed to relay tasks from a mobile or web session to the Claude Desktop agent. Researchers found Dispatch accepted standard authenticated web sessions, making it accessible to any script running in the claude.ai context.

Anthropic was notified on 14 May 2026 and confirmed the issue as valid on 19 May, though it was subsequently closed as a duplicate of a pre-existing internal report. As of publication, Dispatch remains partially active for existing Pro, Max, and Ultra subscribers.

## Technical Analysis

The attack requires two preconditions: a browser extension with script execution rights on `claude.ai`, and a user simultaneously signed into both `claude.ai` and Claude Desktop with Dispatch enabled.

Once these are met, the attack flow is straightforward:

1. The extension injects a script into the `claude.ai` page.
2. The script opens the Dispatch interface and sends a crafted sequence of prompts — impersonating the authenticated user.
3. Claude initially hesitates when asked to install an unfamiliar npm package; the script follows up with a confirmatory prompt in the user's voice.
4. Claude's approval dialogs appear within the page the extension already controls. The script polls for and auto-clicks any "Allow" button every second, bypassing human oversight entirely.
5. Claude Desktop executes a global `npm install`; the package's install script spawns the Calculator app in the proof-of-concept — but could equally exfiltrate files or deploy a backdoor.

No network-level exploit or privilege escalation was needed. Claude's own agentic capabilities — and its willingness to act on instructions arriving via Dispatch — were sufficient. The researchers also note that because Dispatch is cross-device by design, the extension could potentially reach a Claude Desktop instance on a *different* machine sharing the same account, such as a personal laptop and a work computer.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)**: Attacker-controlled prompts are injected via the extension and delivered as if from the legitimate user.
- **AML.T0067 (LLM Trusted Output Components Manipulation)**: The extension manipulates the UI layer to suppress and auto-approve Claude's confirmation dialogs.
- **AML.T0080 (AI Agent Context Poisoning)**: The agent's task context is poisoned with attacker-supplied instructions.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: Code execution via npm install could be weaponised for data theft.
- **LLM08 (Excessive Agency)**: Claude Desktop holds broad OS permissions and acts on instructions without sufficient out-of-band verification.
- **LLM07 (Insecure Plugin Design)**: Dispatch's acceptance of standard web sessions rather than a hardened API channel is the core design flaw.

## Impact Assessment

The impact is potentially severe. Any user running Claude Desktop with Dispatch enabled and a browser extension on `claude.ai` is exposed to full code execution under Claude's OS permissions. Organisations where employees use personal Claude accounts on corporate hardware face compounded risk — a compromised home-use extension could pivot to a work machine. Forever Security reports observing personal Claude accounts with cross-device Dispatch active on enterprise endpoints.

## Mitigation & Recommendations

- **Disable Dispatch** immediately if it is not actively required. Navigate to Claude Desktop settings and confirm the feature is off.
- **Audit extensions** with access to `claude.ai`. Remove any extension that is unverified, infrequently updated, or sourced outside official browser stores.
- **Restrict Claude Desktop permissions** using OS-level controls (e.g., macOS app sandboxing, Windows AppLocker) to limit the blast radius of any future agent-based execution.
- **Monitor npm activity** on endpoints where Claude Desktop is installed; unexpected global installs should trigger alerts.
- **Enterprise policy**: prohibit personal AI accounts on managed devices, or deploy browser extension allowlisting.

## References

- [The Hacker News — Original Article](https://thehackernews.com/2026/11/malicious-browser-extensions-could-use.html)
- Forever Security technical write-up by Gal Weizman (referenced in article)
