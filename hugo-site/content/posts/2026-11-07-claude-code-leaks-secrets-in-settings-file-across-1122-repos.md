---
title: "Claude Code Leaks Secrets in Settings File Across 1,122 Repos"
date: 2026-11-07T11:53:01+00:00
draft: false
slug: "claude-code-leaks-secrets-in-settings-file-across-1122-repos"

# ── Content metadata ──
summary: "Anthropic's Claude Code AI coding assistant saves verbatim shell commands \u2014 including embedded passwords and API keys \u2014 to a local settings file when developers select 'Yes, and don't ask again.' Security researchers at Apiiro discovered 1,122 public GitHub repositories containing this file with at least 1,379 exposed secrets, including database passwords, SSH credentials, and AWS keys. The leak is compounded by Claude Code's failure to add the file to project-level .gitignore, meaning the protection does not travel with the repository and git history preserves the exposure even after file deletion."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html"
source_title: "Claude Code's \u201cDon't Ask Again\u201d File Exposes Passwords and Keys in 1,122 Public Copies on GitHub"
source_date: 2026-11-07T06:44:17+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1618053448748-b7251851d014?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMnx8bGFib3JhdG9yeSUyMHNjaWVuY2UlMjBkaXNjb3Zlcnl8ZW58MHwwfHx8MTc5NDA1MjM4MHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0081 - Modify AI Agent Configuration", "AML.T0057 - LLM Data Leakage", "AML.T0086 - Exfiltration via AI Agent Tool Invocation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Claude Code saves plain-text secrets in a settings file that ends up in public GitHub repos."
tldr_who_at_risk: "Developers using Claude Code who approved shell commands containing credentials are most exposed, especially if their projects are public on GitHub."
tldr_actions: ["Immediately rotate all credentials — passwords, tokens, and API keys — that may have appeared in Claude Code shell commands", "Purge .claude/settings.local.json from git history using git-filter-repo or BFG and audit all repository forks", "Add .claude/settings.local.json to every project's .gitignore and enforce this via pre-commit hooks or CI secret scanning"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Supply Chain", "Industry News"]
tags: ["claude-code", "anthropic", "credential-exposure", "github-secrets", "api-key-leak", "settings-file", "gitignore", "developer-security", "agentic-ai", "secret-management"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-11-07T11:53:01+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html"
pipeline_version: "2.1.0"
content_hash: "9957f88b6d8925ba"
---

## Overview

Anthropic's Claude Code AI coding assistant has been found to silently persist sensitive credentials in a plain-text project settings file that thousands of developers have inadvertently committed to public GitHub repositories. Security firm Apiiro identified 1,122 public copies of `.claude/settings.local.json` containing at least one secret, out of 104,185 copies found across 103,617 repositories. The 1,379 exposed secrets include 379 database passwords, 43 SSH logins, 42 tokens for GitHub, GitLab, and npm, and 23 AWS keys — a credential landscape that represents immediate lateral movement risk for any attacker who finds them.

## Technical Analysis

The vulnerability stems from Claude Code's permission workflow. When a developer selects "Yes, and don't ask again" on a shell command prompt, Claude Code writes an allow rule to `.claude/settings.local.json` inside the project directory. If the approved command contained an inline secret — a database password in a connection string, an API key passed as an argument — that exact string is preserved verbatim in the JSON file.

Claude Code attempts to prevent accidental commits by adding the file to the user's **global** git excludes on first write. This machine-scoped protection is invisible to collaborators, CI runners, or any other machine. Critically, Claude Code never appends the file to the **project-level** `.gitignore`, so the exclusion does not travel with the repository.

Apiiro confirmed that in 539 of 1,105 traced repositories, a commit co-authored by Claude modified the file — indicating the AI agent itself frequently performs the commit that exposes the secret. The researchers reproduced the behaviour on the latest available models at time of publication.

Deleting the file after the fact does not remediate the exposure: git history retains every prior version, and all forks inherit the history.

```json
// Example structure of an exposed .claude/settings.local.json allow rule
{
  "permissions": {
    "allow": [
      "psql postgresql://admin:SuperSecret123@db.example.com:5432/prod"
    ]
  }
}
```

## Framework Mapping

- **AML.T0083 – Credentials from AI Agent Configuration**: The core finding — secrets stored by an AI agent's configuration mechanism are harvested by third parties.
- **AML.T0084 – Discover AI Agent Configuration**: Attackers can search GitHub for the well-known filename pattern to enumerate targets at scale.
- **AML.T0081 – Modify AI Agent Configuration**: Downstream risk — once a repository is compromised, the settings file could be tampered with to introduce malicious allow rules.
- **AML.T0057 – LLM Data Leakage**: The AI tool discloses user-supplied sensitive data beyond the intended interaction boundary.
- **LLM06 – Sensitive Information Disclosure**: Direct match; the tool leaks credentials entered during normal use.
- **LLM08 – Excessive Agency**: Claude Code autonomously commits files to version control, amplifying the impact of its design decision.

## Impact Assessment

The immediately actionable risk is credential compromise. Database passwords and SSH keys directly enable unauthorised access to production infrastructure. AWS keys can trigger financial and data exposure at cloud scale. The 63 affected organisations identified by Apiiro represent enterprise-grade targets beyond individual developers.

Secondary risk is persistence through forks: a cleaned repository may still expose secrets in dozens of forks outside the owner's control.

## Mitigation & Recommendations

1. **Rotate first**: Treat every credential that has ever appeared in a Claude Code shell command as compromised. Revoke and regenerate immediately.
2. **Purge git history**: Use `git-filter-repo` or BFG Repo Cleaner to remove the file from all commits, then force-push. Contact GitHub support to purge cached views and notify fork owners.
3. **Add to project .gitignore**: Include `.claude/settings.local.json` in every repository's `.gitignore` and enforce via pre-commit hooks.
4. **Enable secret scanning**: GitHub Advanced Security and tools like TruffleHog or Gitleaks can alert on committed secrets before they reach public branches.
5. **Avoid inline secrets**: Pass credentials via environment variables or secret managers rather than embedding them in shell command strings.

## References

- Original reporting: [The Hacker News, 07 Nov 2026](https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html)
- Apiiro research write-up referenced in article
- Anthropic Claude Code permissions documentation
