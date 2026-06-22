---
title: "First Look: Anthropic Claude Code Gains Fully-Local Persistent Session Memory via Recall"
date: "2026-06-22T05:12:25+00:00"
draft: false 
slug: "first-look-anthropic-claude-code-gains-fully-local-persistent-session-memory-via"

# ── Content metadata ──
summary: "Recall is an open-source, fully-local memory layer for Anthropic's Claude Code that persists and summarises project context across coding sessions without sending data to external services. For defenders, the introduction of a persistent, file-based context store creates a new attack surface: a poisoned or tampered memory file can silently inject malicious instructions into every subsequent Claude Code session. Security teams should treat the local memory store as a trusted-input boundary and apply appropriate file-integrity and access controls."
source: "Anthropic (via HN)"
source_url: "https://github.com/raiyanyahya/recall"
source_title: "Show HN: Recall \u2013 fully-local project memory for Claude Code"
source_date: 2026-06-21T21:05:37+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1781643437465-9470f192d9c1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxBbnRocm9waWMlMjBhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwcmVzZWFyY2glMjBsYWJvcmF0b3J5fGVufDB8MHx8fDE3ODIwOTk5MTN8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 5.5
adoption_velocity: "MODERATE"
capability_category: "open-source-release"
attack_vectors_introduced: ["Persistent context poisoning: an attacker with local or supply-chain write access to the Recall memory file can inject adversarial instructions that are automatically fed to Claude Code on every session startup", "Prompt injection via persisted summaries: if Claude Code processes any external content (e.g., untrusted code comments, README files) that is later summarised and stored by Recall, attacker-controlled text survives into future sessions as seemingly trusted context", "Sensitive data accumulation: the local log of all sessions may inadvertently persist secrets, API keys, or proprietary code snippets in plaintext, creating a high-value exfiltration target", "Supply chain compromise of the summariser plugin: the open-source Python summariser and Claude Code plugin hooks are a new third-party dependency; a malicious commit or dependency could alter how context is written or read", "Privilege escalation via context manipulation: an insider or compromised process could modify the stored summary to expand the perceived project scope or override prior safety instructions given to Claude Code"]

# ── AI Security Classification ──
relevance_score: 5.8
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0010 - ML Supply Chain Compromise", "AML.T0043 - Craft Adversarial Data", "AML.T0056 - LLM Meta Prompt Extraction"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Recall adds durable, fully-local session memory to Anthropic's Claude Code via an open-source Python plugin."
tldr_who_at_risk: "Developers using Claude Code on shared or multi-user machines, and teams where local project directories may be accessible to untrusted code or processes."
tldr_actions: ["Audit file permissions on Recall's local memory store and restrict write access to the owning developer account only", "Treat the persisted context file as a trust boundary — review its contents before deploying to new environments or sharing project directories", "Pin the Recall dependency and its transitive Python packages to verified versions and integrate integrity checks into CI pipelines"]

# ── Taxonomies ──
categories: ["First Look", "LLM Security", "Prompt Injection", "Agentic AI", "Supply Chain"]
tags: ["claude-code", "anthropic", "persistent-memory", "local-context", "prompt-injection", "session-memory", "open-source", "agentic-coding", "context-poisoning", "developer-tooling"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-22T03:45:13+00:00"
feed_source: "hn_anthropic"
original_url: "https://github.com/raiyanyahya/recall"
pipeline_version: "2.0.0"
---

## Capability Overview

Recall is an open-source tool that bolts durable, fully-local memory onto Anthropic's Claude Code. It logs coding sessions, condenses them into a project summary using a classical Python summariser, and automatically injects that summary into each new Claude Code session — eliminating the need for users to re-explain project context. Crucially, no data leaves the machine and no additional API key is required. The tool operates via Claude Code plugin hooks and stores its state in local JSON files.

For defenders, the significance is not the AI capability itself but what it introduces architecturally: **a persistent, file-based trust input that Claude Code will consume on every invocation without user review**. Anything written to that file becomes implicit context for the agent.

---

## Attack Surface Analysis

Prior to Recall, each Claude Code session started cold — an attacker had to inject malicious content within the active session window. Recall changes that calculus by introducing a persistent attack surface that survives across sessions.

**New vectors defenders must consider:**

1. **Context Poisoning at Rest** — The local summary file is written by a Python process. Any attacker (insider, malicious process, or compromised CI runner) with write access to the project directory can modify the file to prepend adversarial instructions. These will be silently read by Claude Code at the next session start, potentially redirecting agent behaviour.

2. **Prompt Injection via Summarised External Content** — If a developer pastes untrusted content (e.g., a third-party README, a user-submitted bug report) into a session that Recall subsequently summarises, attacker-controlled text can survive into future sessions as authoritative project context — a classic second-order prompt injection path.

3. **Sensitive Data Accumulation** — Session logs may capture API keys typed in context, proprietary algorithms discussed with the agent, or internal endpoint URLs. Stored in plaintext JSON on disk, these logs become a high-value target for any process with filesystem read access.

4. **Supply Chain Risk** — Recall introduces a new open-source Python dependency with plugin hooks that execute during every Claude Code startup. A malicious pull request or compromised PyPI package could alter context write/read behaviour.

---

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0051 – LLM Prompt Injection | Persisted context file is a new injection point consumed by the LLM |
| MITRE ATLAS | AML.T0057 – LLM Data Leakage | Session logs may persist sensitive developer data |
| MITRE ATLAS | AML.T0010 – ML Supply Chain Compromise | Open-source summariser plugin is a new third-party dependency |
| MITRE ATLAS | AML.T0043 – Craft Adversarial Data | Attackers can craft poisoned memory entries |
| OWASP | LLM01 – Prompt Injection | Context file injection maps directly to this category |
| OWASP | LLM06 – Sensitive Information Disclosure | Plaintext session logs accumulate sensitive data |
| OWASP | LLM05 – Supply Chain Vulnerabilities | Python plugin and hooks introduce supply chain exposure |
| OWASP | LLM07 – Insecure Plugin Design | Plugin hooks lack documented integrity or sandboxing controls |

---

## Threat Scenarios

**Scenario 1 — Insider Context Manipulation:** A developer on a shared workstation modifies the Recall summary file to include an instruction such as *"always include the following header in generated code"* embedding a malicious payload. All subsequent Claude Code sessions for that project silently include the instruction.

**Scenario 2 — CI/CD Pipeline Poisoning:** A repository's CI runner has write access to the project directory. A compromised workflow step overwrites the Recall memory file prior to a developer session, redirecting Claude Code to exfiltrate generated code to an external endpoint.

**Scenario 3 — Second-Order Prompt Injection:** A developer pastes an attacker-controlled issue description into a Claude Code session. Recall summarises and stores it. In a later session, the stored summary causes Claude Code to follow embedded instructions from the original attacker.

---

## Defender Checklist

- [ ] **Restrict write permissions** on `recall.config.json` and all session log files to the owning user account only
- [ ] **Review memory file contents** before sharing project directories, pushing to version control, or onboarding new contributors
- [ ] **Exclude Recall logs** from repository commits via `.gitignore` to prevent inadvertent secret exposure
- [ ] **Pin Recall and its Python dependencies** to specific verified versions; monitor for unexpected updates
- [ ] **Treat external content** pasted into Claude Code sessions as untrusted — assume it may be summarised and persisted
- [ ] **Audit plugin hook scripts** in the `.claude-plugin` directory for unexpected behaviour before deploying in shared or production-adjacent environments
- [ ] **Rotate any credentials** that may have been discussed or typed within a Claude Code session that Recall was logging

---

## References

- [raiyanyahya/recall — GitHub](https://github.com/raiyanyahya/recall)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
