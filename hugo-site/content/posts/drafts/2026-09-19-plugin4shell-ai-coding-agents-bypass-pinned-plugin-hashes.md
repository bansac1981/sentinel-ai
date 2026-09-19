---
title: "Plugin4Shell: AI Coding Agents Bypass Pinned Plugin Hashes"
date: 2026-09-19T09:45:01+00:00
draft: true
slug: "plugin4shell-ai-coding-agents-bypass-pinned-plugin-hashes"

# ── Content metadata ──
summary: "A supply chain vulnerability dubbed Plugin4Shell allows repository owners to substitute malicious code in place of pinned plugin versions across four major AI coding agents \u2014 Claude Code, Codex, GitHub Copilot, and Gemini CLI \u2014 by exploiting lax commit hash verification. Because plugins run with the same privileges as the user, a successful swap can expose files, stored credentials, and connected systems. Anthropic and OpenAI have issued patches, while GitHub Copilot remains unpatched and Google has declined to fix the retiring Gemini CLI."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/plugin4shell-lets-repository-owners.html"
source_title: "Plugin4Shell Lets Repository Owners Swap Pinned Plugin Code Across Four AI Coding Agents"
source_date: 2026-09-18T11:01:01+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1625750331870-624de6fd3452?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMXx8Y2hlc3MlMjBwaWVjZSUyMHN0cmF0ZWd5JTIwYm9hcmQlMjBnYW1lfGVufDB8MHx8fDE3ODk4MTExMDF8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0109 - AI Supply Chain Rug Pull", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0081 - Modify AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Repository owners can silently swap pinned AI coding agent plugins with malicious code by exploiting missing hash verification."
tldr_who_at_risk: "Developers using Claude Code, Codex, GitHub Copilot, or Gemini CLI who install plugins from non-GitHub git hosts are most exposed due to absent commit hash validation."
tldr_actions: ["Update Claude Code to 2.1.179 and Codex to 0.146.0 immediately", "Restrict plugin sources to GitHub-hosted marketplaces only until patches are confirmed", "Audit installed plugins from Bitbucket or self-hosted git servers for unexpected code changes", "Disable auto-update for third-party plugins in all AI coding agents where possible"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Research"]
tags: ["plugin4shell", "ai-coding-agents", "supply-chain-attack", "claude-code", "openai-codex", "github-copilot", "gemini-cli", "commit-hash-bypass", "plugin-security", "credential-theft", "air-security", "bitbucket", "git-repository"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-19T09:45:01+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/plugin4shell-lets-repository-owners.html"
pipeline_version: "2.1.0"
---

## Overview

Security firm Air Security has disclosed a supply chain vulnerability — branded **Plugin4Shell** — affecting four prominent AI coding agents: Anthropic's Claude Code, OpenAI's Codex, GitHub Copilot, and Google's Gemini CLI. The flaw allows a malicious repository owner to silently replace a plugin's pinned, reviewed code with arbitrary malicious code, even when the agent has locked the plugin to a specific commit hash. Anthropic and OpenAI have shipped patches; GitHub Copilot remains unpatched; Google has declined to fix Gemini CLI, citing its retirement.

## Technical Analysis

AI coding agent marketplaces pin plugins to a specific commit hash — a cryptographic identifier representing an exact snapshot of source code — to prevent unauthorised changes from reaching end users. The vulnerability stems from a fundamental implementation gap: the agents fetch the snapshot identified by the hash but **never verify that the retrieved code matches that hash**.

On git hosting platforms that permit branch or tag names resembling commit hashes (e.g., Bitbucket or self-hosted git servers), a repository owner can create a branch whose name mimics the pinned hash string. When the agent resolves the reference, the host serves the attacker-controlled branch tip rather than the genuine commit. The agent installs this substituted code while still reporting the legitimate pinned version — a classic rug-pull.

**GitHub is partially insulated**: its platform explicitly blocks branch and tag names that match the format of commit hashes, meaning plugins hosted on GitHub are not susceptible to the branch-name variant of the attack.

The Gemini CLI faces an additional, distinct vector. Its installer can be tricked by a repository whose main branch is named `FETCH_HEAD` — a name GitHub's hash-format rule does not clearly block — leaving GitHub-hosted Gemini CLI plugins potentially exposed regardless.

**Auto-update amplifies risk**: Claude Code and Codex enable background auto-update by default for their built-in marketplaces. However, these default marketplaces are GitHub-hosted, partially limiting the practical blast radius of the branch-name attack. Auto-update is off or optional for external plugin sources on these agents.

Because plugins run with the full privileges of the authenticated user, a successfully swapped plugin can read local files, harvest saved credentials, and interact with any systems the user has access to.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS | AML.T0109 – AI Supply Chain Rug Pull | Repository owner replaces reviewed plugin code post-pinning |
| ATLAS | AML.T0110 – AI Agent Tool Poisoning | Malicious plugin executes in agent context |
| ATLAS | AML.T0083 – Credentials from AI Agent Configuration | Swapped plugin can harvest stored credentials |
| OWASP | LLM05 – Supply Chain Vulnerabilities | Hash verification not enforced end-to-end |
| OWASP | LLM07 – Insecure Plugin Design | Plugins granted excessive runtime trust without integrity checks |

## Impact Assessment

- **Directly affected**: Developers using Claude Code, Codex, GitHub Copilot, or Gemini CLI who install plugins from Bitbucket, self-hosted git servers, or other non-GitHub hosts.
- **Lower risk**: Users installing plugins exclusively from the agents' default GitHub-based marketplaces are not exposed to the branch-name attack vector, per Air Security and GitHub's own documentation.
- **Unpatched exposure**: GitHub Copilot users remain vulnerable with no fix timeline stated; Gemini CLI users are unprotected due to Google's decision not to patch.
- **Credential and data theft** are the primary impact scenarios given plugin privilege levels.

## Mitigation & Recommendations

1. **Patch immediately**: Upgrade Claude Code to ≥ 2.1.179 and Codex to ≥ 0.146.0.
2. **Restrict plugin sources**: Install plugins only from the agents' default GitHub-based marketplaces until comprehensive fixes are available.
3. **Audit third-party plugins**: Review any plugins sourced from Bitbucket or self-hosted repositories for unexpected code modifications.
4. **Disable or restrict auto-update** for non-default plugin sources.
5. **Migrate away from Gemini CLI**: As Google will not patch, organisations using it should plan migration to a supported agent.
6. **Enforce hash verification**: Platform and marketplace operators should implement server-side content-addressable validation to close this class of vulnerability.

## References

- [Original article — The Hacker News, 2026-09-18](https://thehackernews.com/2026/09/plugin4shell-lets-repository-owners.html)
