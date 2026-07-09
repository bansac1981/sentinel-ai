---
title: "Repository Poisoning RCE in Claude, Cursor, Gemini"
date: "2026-05-08T03:10:50+00:00"
draft: false
slug: "malicious-repos-trigger-silent-code-execution-in-claude-cursor-gemini-clis"

# ── Content metadata ──
summary: "A vulnerability class dubbed 'TrustFall' demonstrates that malicious code repositories can trigger arbitrary code execution in AI-assisted developer tools including Claude Code, Cursor CLI, Gemini CLI, and GitHub Copilot CLI, with little to no user interaction required. The attack surface stems from inadequate or easily dismissed warning dialogs that fail to surface the risk of executing untrusted repository content. Developers cloning or opening adversarial repositories are exposed to full host-level compromise through the elevated trust these AI coding agents place in repository-supplied context."
source: "Dark Reading"
source_url: "https://www.darkreading.com/application-security/trustfall-exposes-claude-code-execution-risk"
source_title: "'TrustFall' Convention Exposes Claude Code Execution Risk"
source_date: 2026-05-07T13:00:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1717501218221-1da14c0f365e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw5fHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc3ODIwODE3Mnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Malicious repositories silently trigger code execution in major AI coding CLI tools via weak warnings."
tldr_who_at_risk: "Software developers using Claude Code, Cursor CLI, Gemini CLI, or GitHub Copilot CLI who clone or open untrusted repositories are directly exposed to host-level compromise."
tldr_actions: ["Audit AI coding tool configurations to restrict automatic execution of repository-supplied instructions or scripts", "Treat all repository-embedded AI instruction files (e.g., .cursor, CLAUDE.md, system prompts) as untrusted input requiring explicit review", "Apply least-privilege sandboxing to AI CLI agents to limit blast radius of any code execution"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Supply Chain", "Research"]
tags: ["claude-code", "cursor-cli", "gemini-cli", "copilot-cli", "code-execution", "prompt-injection", "repository-poisoning", "agentic-ai", "developer-tools", "trustfall", "rce", "ai-coding-assistants"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-08T02:56:33+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/application-security/trustfall-exposes-claude-code-execution-risk"
pipeline_version: "1.0.0"
---

## Overview

Researchers presenting at the 'TrustFall' convention in May 2026 disclosed a class of vulnerabilities affecting AI-powered developer CLI tools — including Anthropic's Claude Code, Cursor CLI, Google's Gemini CLI, and GitHub Copilot CLI. The core finding: adversarially crafted code repositories can cause these tools to execute arbitrary code on a developer's machine, often with minimal or no explicit user confirmation required. The vulnerability class is significant because it targets the implicit trust model that agentic coding assistants extend to repository-hosted content.

## Technical Analysis

AI coding assistants increasingly consume repository context files (such as `CLAUDE.md`, `.cursor/rules`, or similar convention-based instruction files) to guide their behaviour within a project. The TrustFall research demonstrates that an attacker can embed prompt injection payloads or direct shell execution instructions within these files. When a developer opens or clones the malicious repository, the AI agent parses and acts on these instructions with insufficient friction.

Key factors enabling the attack:
- **Skimpy warning dialogs**: Confirmation prompts, where they exist at all, are easily dismissed or fail to convey the risk of executing repository-supplied instructions.
- **Excessive agency**: These CLI agents are designed to take action autonomously, meaning injected instructions can result in file system access, network calls, or shell command execution without a clear human approval gate.
- **No instruction provenance checks**: None of the affected tools were reported to cryptographically verify or sandbox repository-supplied instruction content before acting on it.

The attack requires no exploitation of a traditional memory corruption or logic bug — it is a design-level trust boundary failure, making it broadly applicable and trivial to reproduce.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)**: Repository instruction files serve as the injection vector, redirecting agent behaviour.
- **AML.T0010 (ML Supply Chain Compromise)**: Malicious repositories distributed via public platforms (GitHub, GitLab) constitute a supply chain attack surface.
- **AML.T0043 (Craft Adversarial Data)**: The repository content is deliberately crafted to manipulate agent execution.
- **LLM01 (Prompt Injection)** and **LLM08 (Excessive Agency)** are the primary OWASP categories — the agent both accepts injected instructions and acts on them with disproportionate autonomy.
- **LLM05 (Supply Chain Vulnerabilities)** applies given the open-source repository distribution vector.

## Impact Assessment

The affected tools are widely deployed across enterprise and individual developer environments. A developer cloning a repository from an open-source platform, a job listing, or a phishing link could trigger full host-level code execution under their own user context. This exposure is particularly acute in CI/CD pipelines where AI coding agents may run with elevated or unmonitored privileges. The low barrier to exploitation (no CVE-class memory bug required, just a crafted text file) makes this accessible to a wide range of threat actors.

## Mitigation & Recommendations

1. **Disable automatic execution of repository instruction files** until vendors implement robust sandboxing and explicit approval flows.
2. **Review and restrict AI CLI tool permissions** — run agents in containerised or sandboxed environments where possible.
3. **Treat repository-hosted AI config files as untrusted input** and establish internal review gates before opening external repositories with AI tooling active.
4. **Advocate for vendor-side fixes**: vendors should implement cryptographic signing of instruction files, meaningful approval dialogs with risk context, and deny-by-default execution policies for repository-supplied commands.
5. **Monitor for anomalous process spawning** from IDE and CLI tool parent processes as a detection signal.

## References

- [Dark Reading — TrustFall Convention Exposes Claude Code Execution Risk](https://www.darkreading.com/application-security/trustfall-exposes-claude-code-execution-risk)
