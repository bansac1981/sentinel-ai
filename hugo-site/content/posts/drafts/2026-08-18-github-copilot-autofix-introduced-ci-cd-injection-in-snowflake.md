---
title: "GitHub Copilot Autofix Introduced CI/CD Injection in Snowflake"
date: 2026-08-18T04:53:55+00:00
draft: true
slug: "github-copilot-autofix-introduced-ci-cd-injection-in-snowflake"

# ── Content metadata ──
summary: "Wiz Research's autonomous Red Agent discovered and exploited a GitHub Actions script injection vulnerability in a Snowflake public repository, introduced by a GitHub Copilot Autofix co-authored commit just five days prior. The flaw allowed any unauthenticated GitHub user to execute arbitrary commands in a Actions runner by crafting a malicious issue title, ultimately enabling exfiltration of a token granting access to Snowflake's internal Jira instance. The incident exposes a critical trust gap: AI-assisted code review and AI-generated fixes can introduce and simultaneously fail to detect severe security vulnerabilities."
source: "HN AI Security"
source_url: "https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug"
source_title: "AI-Generated GitHub Copilot \u201cAutofix\u201d Allowed Compromise of Snowflake's Jira"
source_date: 2026-08-17T14:18:38+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1673423707246-e8b78e272125?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNHx8R2l0aHViJTIwcGlwZWxpbmUlMjBvaWwlMjBnYXMlMjBpbmR1c3RyaWFsJTIwbGFuZHNjYXBlfGVufDB8MHx8fDE3ODcwMjg4MzV8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0010 - AI Supply Chain Compromise", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0103 - Deploy AI Agent", "AML.T0083 - Credentials from AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM09 - Overreliance", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Copilot Autofix introduced a shell injection flaw that exposed Snowflake's internal Jira via a stolen token."
tldr_who_at_risk: "Any organisation using AI-assisted code review and GitHub Actions workflows triggered by untrusted user input is directly exposed to similar injection attacks."
tldr_actions: ["Audit all GitHub Actions workflows for direct ${{ github.event }} interpolation inside run: blocks", "Never trust AI-generated or AI-reviewed code commits without a human security review for injection-prone contexts", "Enforce least-privilege secrets scoping so workflow tokens cannot access internal systems like Jira"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security", "Research"]
tags: ["github-actions", "copilot-autofix", "script-injection", "ci-cd-security", "snowflake", "autonomous-red-team", "wiz-red-agent", "credential-exfiltration", "ai-code-review", "supply-chain", "jira-exposure", "workflow-vulnerability"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-08-18T04:53:55+00:00"
feed_source: "hn_ai_security"
original_url: "https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug"
pipeline_version: "2.1.0"
---

## Overview

On June 23, 2026, Wiz Research disclosed a critical GitHub Actions script injection vulnerability in Snowflake's public `snowflakedb/snowflake-connector-net` repository. The flaw was independently discovered and exploited by Wiz's autonomous "Red Agent" — an AI-powered offensive security tool — just five days after the vulnerable code was merged. What makes this incident particularly significant is its origin: the vulnerable pattern was introduced by a commit co-authored by **GitHub Copilot Autofix**, and the same AI-assisted review process failed to flag the resulting critical vulnerability. Snowflake remediated the issue on the day of disclosure and confirmed via audit logs that Wiz was the sole actor during the exposure window.

## Technical Analysis

The vulnerability resided in `jira_issue.yml`, a workflow triggered whenever any GitHub user opened an issue on the repository. A prior safe implementation passed the issue title through an `env:` variable and constructed the JSON payload using `jq`, preventing shell injection:

```yaml
env:
  ISSUE_TITLE: ${{ github.event.issue.title }}
run: jq -n --arg title "$ISSUE_TITLE" ...
```

The Copilot Autofix co-authored commit (PR #1218, June 18 2026) replaced this pattern with direct GitHub expression interpolation inside a `run:` block, relying on `sed` for escaping:

```yaml
run: |
  TITLE=$(echo '${{ github.event.issue.title }}' | sed 's/"/\\"/g' | sed "s/'/\\\'/g")
```

The critical flaw: GitHub's template engine expands `${{ github.event.issue.title }}` **before** the shell executes, so the `sed` escaping never processes attacker-controlled input at the right stage. A single quote in the issue title terminates the `echo '...'` argument and allows arbitrary command injection. An attacker simply opens a GitHub issue with a crafted title to achieve remote code execution on the Actions runner — no authentication required.

Wiz Red Agent exploited this to exfiltrate a secret token present in the runner environment, which granted access to Snowflake's internal Jira portal.

## Framework Mapping

- **AML.T0047 (AI-Enabled Product or Service):** GitHub Copilot Autofix, an AI product, directly introduced the vulnerability through a code suggestion merged without adequate human security review.
- **AML.T0010 (AI Supply Chain Compromise):** The compromised code change entered the supply chain via an AI co-authored PR, affecting downstream CI/CD security posture.
- **AML.T0086 / AML.T0083:** Red Agent exfiltrated credentials via automated tool invocation and leveraged them for lateral access.
- **LLM09 (Overreliance):** Developers and reviewers trusted Copilot's output and review without independent security validation.
- **LLM05 (Supply Chain Vulnerabilities):** The AI-assisted PR introduced a security regression into a public, widely-used repository.

## Impact Assessment

The blast radius included access to Snowflake's internal Jira instance via an exfiltrated token. Snowflake confirmed that no data was retained by Wiz and that no other actor accessed the system during the exposure window. However, the vulnerability was publicly exploitable for five days — any threat actor scanning GitHub Actions workflows for injection patterns could have discovered and exploited it independently.

The broader industry implication is severe: AI coding assistants can introduce subtle, high-severity vulnerabilities while simultaneously providing a false sense of security through AI-powered review.

## Mitigation & Recommendations

1. **Ban direct expression interpolation in `run:` blocks.** Always pass untrusted GitHub event data through `env:` variables; never embed `${{ }}` expressions directly in shell scripts.
2. **Implement SAST rules for Actions injection patterns.** Tools like `zizmor` or Semgrep Actions packs can detect these patterns in CI.
3. **Require human security review for AI-generated commits** touching CI/CD workflow files, especially those modifying input handling.
4. **Scope workflow secrets tightly.** Tokens available to issue-triggered workflows should have minimal permissions — never access to internal systems like Jira.
5. **Run autonomous red-team scanning** against your own GitHub organisation to detect injection-vulnerable workflows proactively.

## References

- [Wiz Blog: Red Agent Finds Its Way Into Snowflake's Internal Jira](https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug)
