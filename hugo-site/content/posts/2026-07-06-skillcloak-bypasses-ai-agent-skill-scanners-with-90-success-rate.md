---
title: "SkillCloak Bypasses AI Agent Skill Scanners at 90% Rate"
date: "2026-07-07T03:52:28+00:00"
draft: false
slug: "skillcloak-bypasses-ai-agent-skill-scanners-with-90-success-rate"

# ── Content metadata ──
summary: "Researchers at Hong Kong University of Science and Technology have demonstrated that static scanners used to vet malicious AI agent 'skills' \u2014 modular add-ons for agents like Claude Code and OpenAI Codex \u2014 can be systematically bypassed using a tool called SKILLCLOAK. The technique leverages either character-substitution obfuscation or self-extracting packing into scanner-ignored directories like .git/, achieving evasion rates above 90% across all eight tested scanners. The same research team also developed SKILLDETONATE, a runtime behavioral sandbox that catches most of the threats static analysis misses."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html"
source_title: "SkillCloak Lets Malicious AI Agent Skills Evade Static Scanners with Self-Extracting Packing"
source_date: 2026-07-06T06:33:56+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1781330184655-8210f7010e0e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOXx8cm9ib3QlMjBhdXRvbWF0aW9uJTIwYXV0b25vbW91cyUyMHdvcmtmbG93fGVufDB8MHx8fDE3ODMxNTM1MTh8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0015 - Evade ML Model", "AML.T0047 - ML-Enabled Product or Service", "AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "SKILLCLOAK systematically evades all tested AI agent skill scanners with over 90% success using packing techniques."
tldr_who_at_risk: "Developers and organisations using AI coding agents (Claude Code, OpenAI Codex) that install skills from public marketplaces are directly exposed to credential theft, code exfiltration, and backdoor installation."
tldr_actions: ["Audit all installed AI agent skills and remove any sourced from unvetted public marketplaces", "Deploy runtime behavioral monitoring (sandbox-based) rather than relying solely on static skill scanners", "Apply strict allowlisting for skill directories and flag or block execution from paths like .git/ at the agent runtime level"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security", "Research", "Adversarial ML"]
tags: ["skillcloak", "ai-agent-security", "skill-marketplace", "static-analysis-evasion", "self-extracting-packing", "claude-code", "openai-codex", "sandbox-detection", "malicious-plugins", "supply-chain-attack", "behavioral-analysis", "evasion-techniques"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-07-06T07:27:50+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html"
pipeline_version: "2.1.0"
---

## Overview

Researchers at the Hong Kong University of Science and Technology have published findings showing that static scanners — the primary defensive layer for AI agent skill marketplaces — are systematically bypassable. Their tool, SKILLCLOAK, can rewrite malicious skills to evade detection while preserving full attack functionality. Tested against eight scanners and 1,613 real malicious skills sourced from ClawHub (a public skill marketplace), the heavier packing variant exceeded 90% evasion across every scanner, and surpassed 99% on most. This is not an isolated edge case — it is a reproducible, scalable attack pipeline.

AI agent skills are small packages — typically a Markdown instruction file plus scripts — that extend the capabilities of agents like Claude Code, OpenAI Codex, and OpenClaw. Crucially, skills execute with the agent's inherited permissions: filesystem access, terminal privileges, and stored credentials. A malicious skill can exfiltrate source code, steal passwords, or plant persistent backdoors.

## Technical Analysis

SKILLCLOAK operates via two distinct evasion mechanisms:

**1. Lightweight Obfuscation**
This method targets the specific byte patterns that scanners use as detection signatures. Techniques include:
- Substituting flagged characters with Unicode homoglyphs from alternate alphabets
- Splitting flagged shell commands across newlines to break pattern matching
- Result: 80–96% evasion depending on the scanner

**2. Self-Extracting Packing**
The entire malicious payload is relocated into a directory that scanners routinely skip — most notably `.git/` — to reduce false positives and processing overhead. A benign-looking decoder stub is left in the visible skill directory. When the agent executes the skill, the decoder reconstructs and runs the payload from the hidden directory.

```
skill/
├── README.md          ← clean, passes scanner
├── setup.sh           ← benign decoder stub
└── .git/
    └── payload.sh     ← actual malicious payload (scanner never reaches this)
```

The cloaked skills were confirmed to execute with identical effectiveness to the originals on both Claude Code and OpenAI Codex, meaning obfuscation introduces zero functional degradation for the attacker.

The researchers' defensive counterpart, SKILLDETONATE, addresses the root cause of static analysis failure by shifting to runtime behavioral inspection. Running skills in an OS-level sandbox, it monitors file reads/writes, network egress, and sensitive data flows — tracking where data travels rather than what it looks like at rest.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** Malicious skills are injected into public marketplaces with minimal vetting, directly compromising the agent's operational environment.
- **AML.T0015 (Evade ML Model):** SKILLCLOAK's obfuscation and packing techniques are purpose-built to defeat ML-based and signature-based scanners.
- **LLM05 (Supply Chain Vulnerabilities):** The skill marketplace ecosystem lacks integrity verification and sandboxed pre-installation analysis.
- **LLM07 (Insecure Plugin Design):** Skills inherit full agent permissions with no capability scoping or least-privilege enforcement.
- **LLM08 (Excessive Agency):** Agents execute skills with broad system access, amplifying the blast radius of any malicious skill.

## Impact Assessment

The immediate risk is to individual developers using AI coding agents with marketplace-sourced skills. However, in enterprise environments where agents operate on shared infrastructure or CI/CD pipelines, a single malicious skill could result in broad credential compromise or intellectual property theft. The scale of exposure is compounded by cross-agent skill portability — one malicious skill package can target multiple agent platforms simultaneously.

## Mitigation & Recommendations

1. **Do not rely on static scanners alone.** This research confirms they are insufficient. Prioritise runtime behavioral analysis tools equivalent to SKILLDETONATE.
2. **Restrict skill installation sources.** Implement allowlists for approved skill repositories; block installation from unvetted public marketplaces.
3. **Treat hidden directories as untrusted.** Agent runtimes should flag or refuse execution of code originating from `.git/` or similar scanner-blind paths.
4. **Apply least-privilege to agent skill execution.** Skills should not inherit full agent permissions; scope filesystem and network access per-skill.
5. **Audit existing installed skills** for indicators of packing or homoglyph substitution in script files.

## References

- [The Hacker News — SkillCloak Article](https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html)
- Original paper: *Cloak and Detonate* — Hong Kong University of Science and Technology (2026)
