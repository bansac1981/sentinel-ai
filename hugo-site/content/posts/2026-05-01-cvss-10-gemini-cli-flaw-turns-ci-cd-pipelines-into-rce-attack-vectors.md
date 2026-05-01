---
title: "CVSS 10 Gemini CLI Flaw Turns CI/CD Pipelines Into RCE Attack Vectors"
date: "2026-05-01T06:54:32+00:00"
draft: false
slug: "cvss-10-gemini-cli-flaw-turns-ci-cd-pipelines-into-rce-attack-vectors"

# ── Content metadata ──
summary: "Google has patched a maximum-severity (CVSS 10.0) vulnerability in its Gemini CLI tooling that allowed unauthenticated attackers to achieve remote code execution by planting malicious configuration files in workspace directories automatically trusted by the agent in headless/CI mode. The flaw effectively weaponised CI/CD pipelines as supply chain attack paths, bypassing sandbox protections entirely before they could initialise. A secondary issue in '--yolo' mode further enabled prompt injection to trigger unrestricted shell command execution."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/google-fixes-cvss-10-gemini-cli-ci-rce.html"
source_title: "Google Fixes CVSS 10 Gemini CLI CI RCE and Cursor Flaws Enable Code Execution"
source_date: 2026-04-30T07:07:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1717501219074-943fc738e5a2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMnx8YXJ0aWZpY2lhbCUyMGludGVsbGlnZW5jZSUyMHRlY2hub2xvZ3klMjBuZXVyYWwlMjBuZXR3b3JrfGVufDB8MHx8fDE3Nzc2MDk3ODl8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "CVSS 10 Gemini CLI flaw lets attackers execute arbitrary commands via malicious CI workspace config files."
tldr_who_at_risk: "Any team running Gemini CLI in headless/CI mode to process untrusted inputs such as external pull requests or GitHub issues is directly exposed."
tldr_actions: ["Upgrade @google/gemini-cli to ≥0.39.1 (or ≥0.40.0-preview.3 for preview) and google-github-actions/run-gemini-cli to ≥0.1.22 immediately", "Audit all CI workflows using Gemini CLI in headless mode and explicitly set GEMINI_TRUST_WORKSPACE only for trusted-input pipelines", "Disable or strictly scope --yolo mode; review tool allowlists in ~/.gemini/settings.json to prevent unrestricted shell command auto-approval"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Supply Chain", "Prompt Injection"]
tags: ["gemini-cli", "remote-code-execution", "cvss-10", "ci-cd", "supply-chain", "github-actions", "prompt-injection", "agentic-ai", "google", "headless-mode", "yolo-mode", "configuration-injection"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-01T04:33:03+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/google-fixes-cvss-10-gemini-cli-ci-rce.html"
pipeline_version: "1.0.0"
---

## Overview

Google has patched a maximum-severity vulnerability (CVSS 10.0) in its Gemini CLI tooling — spanning the `@google/gemini-cli` npm package and the `google-github-actions/run-gemini-cli` GitHub Actions workflow — that could allow an unprivileged remote attacker to execute arbitrary commands on host systems. Discovered by Novee Security, the flaw is particularly dangerous because it exploits the agent's own trust model, bypassing sandbox protections before they can initialise.

## Technical Analysis

The root cause lies in how Gemini CLI handled workspace trust in headless (CI) mode. Prior to the patch, any workspace folder was automatically trusted, meaning the agent would load configuration files — including environment variable definitions — from the local `.gemini/` directory without explicit user consent, sandboxing, or validation.

An attacker with the ability to introduce files into the workspace (e.g., via a malicious pull request to a repository whose CI pipeline uses Gemini CLI) could plant a crafted `.gemini/` configuration containing malicious environment variables. When the CI runner processed the PR, Gemini CLI would load this configuration and execute attacker-controlled commands directly on the host, entirely outside the sandbox boundary.

```
# Example attack path
1. Attacker submits PR containing .gemini/settings.json with malicious env vars
2. CI workflow triggers Gemini CLI in headless mode
3. CLI auto-trusts workspace, loads .gemini/ config pre-sandbox
4. Malicious payload executes on CI runner host
```

A secondary vulnerability existed in `--yolo` (auto-approve) mode: the tool ignored configured tool allowlists in `~/.gemini/settings.json` and would automatically approve all tool calls — including `run_shell_command` — without user confirmation. This opened a direct prompt injection pathway via untrusted inputs such as GitHub Issues.

Affected versions:
- `@google/gemini-cli` < 0.39.1 and < 0.40.0-preview.3
- `google-github-actions/run-gemini-cli` < 0.1.22

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0051 (LLM Prompt Injection):** The --yolo mode vector directly exploits prompt injection to trigger shell execution via untrusted issue/PR content.
- **AML.T0010 (ML Supply Chain Compromise):** Weaponising CI/CD pipelines through planted workspace configuration constitutes a supply chain attack on ML-integrated development workflows.
- **AML.T0047 (ML-Enabled Product or Service):** The vulnerability exists at the integration layer of an AI-enabled developer tool embedded in production pipelines.

**OWASP LLM Top 10:**
- **LLM01 (Prompt Injection):** Malicious content in issues/PRs drives unintended tool execution.
- **LLM05 (Supply Chain Vulnerabilities):** CI pipeline compromise via workspace configuration injection.
- **LLM07 (Insecure Plugin Design):** The `run_shell_command` tool lacked adequate invocation controls in auto-approve mode.
- **LLM08 (Excessive Agency):** Auto-approval of all tool calls without allowlist enforcement exemplifies excessive agency.

## Impact Assessment

The impact is severe for any organisation using Gemini CLI in CI pipelines to process untrusted inputs — a common pattern for PR review automation. Successful exploitation grants full code execution on the CI runner, enabling secrets theft, pipeline poisoning, and lateral movement into production environments. The lack of a CVE identifier does not diminish the severity; the CVSS 10.0 rating reflects unauthenticated, remote, zero-user-interaction exploitability.

## Mitigation & Recommendations

1. **Patch immediately:** Upgrade to `@google/gemini-cli` ≥0.39.1 (stable) or ≥0.40.0-preview.3 (preview), and `google-github-actions/run-gemini-cli` ≥0.1.22.
2. **Explicit trust configuration:** Set `GEMINI_TRUST_WORKSPACE: 'true'` only in workflows processing trusted inputs. For untrusted inputs, follow Google's hardening guidance.
3. **Restrict --yolo mode:** Avoid deploying auto-approve mode against any untrusted input surface. Validate that tool allowlists in `~/.gemini/settings.json` are enforced on version 0.39.1+.
4. **Audit CI pipelines:** Review all workflows that invoke Gemini CLI, particularly those triggered by external contributors.

## References

- [The Hacker News — Original Report](https://thehackernews.com/2026/04/google-fixes-cvss-10-gemini-cli-ci-rce.html)
