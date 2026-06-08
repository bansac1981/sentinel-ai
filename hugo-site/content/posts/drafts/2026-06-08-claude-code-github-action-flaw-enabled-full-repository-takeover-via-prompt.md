---
title: "Claude Code GitHub Action Flaw Enabled Full Repository Takeover via Prompt Injection"
date: 2026-06-08T13:55:04+00:00
draft: true
slug: "claude-code-github-action-flaw-enabled-full-repository-takeover-via-prompt"

# ── Content metadata ──
summary: "A critical vulnerability in Anthropic's Claude Code GitHub Action allowed attackers to hijack public repositories by opening a single malicious GitHub issue, exploiting a bot actor allowlist bypass combined with indirect prompt injection. The flaw exposed environment secrets including OIDC credentials, which could be replayed to obtain write access to target repositories \u2014 including Anthropic's own action repo, threatening downstream supply chain integrity. Anthropic patched the issue within four days of disclosure; the fix is available in claude-code-action v1.0.94."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html"
source_title: "Claude Code GitHub Action Flaw Let One Malicious Issue Hijack Repositories"
source_date: 2026-06-04T15:15:26+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1601132359864-c974e79890ac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwcm9ib3QlMjBzZWN1cml0eXxlbnwwfDB8fHwxNzgwOTI2NTQxfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "A bot actor allowlist bypass plus indirect prompt injection gave attackers write access to any public repo running Claude Code."
tldr_who_at_risk: "Any public GitHub repository using Claude Code GitHub Action prior to v1.0.94, especially those copied from Anthropic's example workflows with overly permissive trigger settings."
tldr_actions: ["Upgrade claude-code-action to v1.0.94 or later immediately", "Audit workflow permissions and remove allowed_non_write_users: '*' from all issue-triage workflows", "Restrict Claude Code to write-access users only and disable agent mode for untrusted external triggers"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Supply Chain", "Research"]
tags: ["claude-code", "github-actions", "prompt-injection", "indirect-prompt-injection", "supply-chain", "ci-cd-security", "agentic-ai", "anthropic", "credential-theft", "oidc", "repository-hijack", "bot-bypass", "environment-secrets"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-08T13:55:04+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html"
pipeline_version: "1.0.0"
---

## Overview

A vulnerability in Anthropic's Claude Code GitHub Action — disclosed by RyotaK of GMO Flatt Security in January 2026 and patched within four days — allowed an unauthenticated attacker to fully compromise any public GitHub repository running the action. The attack required nothing more than opening a single crafted GitHub issue. Because Anthropic's own `claude-code-action` repository ran the same flawed workflow, a successful exploit could have poisoned the upstream action itself, propagating malicious code to every downstream project consuming it.

Anthropic rated the vulnerability 7.8 under CVSS v4.0, paid a bug bounty, and released a complete fix in `claude-code-action v1.0.94`.

## Technical Analysis

The vulnerability chains two weaknesses:

**1. Bot Actor Allowlist Bypass**

Claude Code's trigger check was designed to allow only repository collaborators with write access to invoke the action. However, the check unconditionally trusted any GitHub actor whose username ended in `[bot]`, assuming these were administrator-installed GitHub Apps. In reality, any user can register a GitHub App, install it on a personal repository, and use its token to open issues or pull requests on any *public* repository. The action observed a `[bot]`-suffixed actor and granted access without further verification. Tag mode included an additional human-actor confirmation; agent mode did not, leaving it fully exposed.

**2. Indirect Prompt Injection via Issue Body**

With the trigger check bypassed, the attacker crafted a GitHub issue whose body contained disguised LLM instructions. After iterative prompt refinement, Claude was directed to read `/proc/self/environ` — the Linux process environment file containing runtime secrets — and post the extracted values back into the issue as part of a fabricated "recovery" response. Although Claude Code includes naive guards against direct file reads, RyotaK successfully bypassed them.

The critical secret extracted was the GitHub Actions OIDC credential pair. Claude Code exchanges this for a Claude GitHub App installation token carrying write access to the target repository's code, issues, and workflows. Replaying that exchange grants the attacker persistent write access.

A secondary, softer attack path required no bot trick: Anthropic's own example issue-triage workflow shipped with `allowed_non_write_users: "*"`, permitting any GitHub user to trigger the action. Claude was also writing task summaries to publicly visible workflow run summary panels, providing a ready data-exfiltration channel. Many repositories copied this example and inherited both misconfigurations.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **LLM01**: The core exploitation mechanism is indirect prompt injection via attacker-controlled issue content.
- **AML.T0057 (LLM Data Leakage)** and **LLM06**: Environment secrets including OIDC tokens were exfiltrated through Claude's responses.
- **AML.T0010 (ML Supply Chain Compromise)** and **LLM05**: Targeting `claude-code-action` itself would have poisoned downstream consumers.
- **LLM08 (Excessive Agency)**: Claude Code's broad default permissions (read/write to code, issues, workflows) amplified the blast radius of a successful injection.
- **LLM02 (Insecure Output Handling)**: Task summaries written to public workflow panels constituted an uncontrolled output channel.

## Impact Assessment

Any public repository running Claude Code GitHub Action prior to v1.0.94 was potentially vulnerable. The highest-severity scenario — targeting Anthropic's own repo to poison the action itself — would have constituted a significant software supply chain attack affecting all downstream users globally. The secondary misconfiguration path (permissive trigger settings copied from official examples) likely affected a meaningful number of production repositories.

## Mitigation & Recommendations

1. **Upgrade immediately** to `claude-code-action v1.0.94` or later.
2. **Remove `allowed_non_write_users: "*"`** from all Claude Code workflows; restrict triggers to verified write-access collaborators.
3. **Disable agent mode** for workflows processing untrusted external content such as public issues.
4. **Audit workflow permissions** and apply least-privilege principles — revoke write access to workflow files unless explicitly required.
5. **Disable public workflow summaries** when Claude Code is processing potentially sensitive context.
6. **Treat all LLM-integrated CI/CD pipelines** as high-value attack surfaces subject to prompt injection from any user-controlled input.

## References

- [The Hacker News — Original Article](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html)
