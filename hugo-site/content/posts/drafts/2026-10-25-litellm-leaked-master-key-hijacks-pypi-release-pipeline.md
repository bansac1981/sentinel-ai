---
title: "LiteLLM Leaked Master Key Hijacks PyPI Release Pipeline"
date: 2026-10-25T09:59:59+00:00
draft: true
slug: "litellm-leaked-master-key-hijacks-pypi-release-pipeline"

# ── Content metadata ──
summary: "An unrevoked LiteLLM Agent Platform master key, accidentally exposed in a public GitHub commit in May 2026, was exploited in October 2026 to exfiltrate GitHub OAuth tokens and hijack the project's PyPI release pipeline. The attacker published a malicious version of the LiteLLM Python package (v1.107.0) to PyPI and Docker Hub before a security researcher detected the supply chain compromise. This incident highlights critical risks in AI/LLM infrastructure tooling, including overprivileged service credentials, insufficient key revocation processes, and weakened release pipeline controls."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/10/leaked-litellm-master-key-let-attackers.html"
source_title: "Leaked LiteLLM Master Key Let Attackers Steal GitHub Tokens and Hijack Release Pipeline"
source_date: 2026-10-24T11:03:33+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxsaWJyYXJ5JTIwYm9va3MlMjBrbm93bGVkZ2UlMjByb3dzfGVufDB8MHx8fDE3OTI5MjIzOTl8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0012 - Valid Accounts", "AML.T0086 - Exfiltration via AI Agent Tool Invocation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Unrevoked LiteLLM master key enabled attacker to publish malicious PyPI package v1.107.0."
tldr_who_at_risk: "Any organisation using LiteLLM Python package v1.107.0 or downstream Docker images is directly exposed to malicious code."
tldr_actions: ["Immediately remove or replace LiteLLM v1.107.0 and update to a verified clean release", "Audit all service accounts and OAuth tokens for overprivileged or unscoped credentials in AI agent platforms", "Enforce key revocation procedures with automated expiry — never rely on manual revocation alone"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Industry News"]
tags: ["litellm", "supply-chain-attack", "pypi", "github-token-theft", "master-key-leak", "credential-exfiltration", "llm-gateway", "ai-agent-platform", "release-pipeline-hijack", "docker-hub", "oauth-token", "open-source-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-25T09:59:59+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/10/leaked-litellm-master-key-let-attackers.html"
pipeline_version: "2.1.0"
---

## Overview

On October 21, 2026, LiteLLM — a widely used open-source LLM gateway and agent orchestration platform — confirmed a significant supply chain attack that resulted in a malicious Python package being published to PyPI as version 1.107.0. The root cause traced back to a May 27, 2026 incident in which a configuration file containing an unrevoked Agent Platform master key was accidentally committed to a public GitHub repository. Although the commit was force-pushed over, key revocation was never completed — leaving a live credential exposed for nearly five months.

## Technical Analysis

The attack unfolded in two distinct phases separated by over a week:

**Phase 1 — Credential Harvesting (October 10, 2026):**
The threat actor, operating from IP `69.48.229[.]143`, used the unrevoked master key to authenticate to the LiteLLM Agent Platform. From there, they extracted a GitHub CLI OAuth token associated with the GitHub organisation owner's account. Critically, this token was not scoped down, granting the attacker owner-level access across all repositories in the BerriAI GitHub organisation.

Within a one-minute window (10:11–10:12 p.m. UTC), the attacker authored commits to throwaway branches on internal repositories, triggering CI/CD workflows configured to expose GitHub CLI OAuth tokens for two maintainer-privileged engineers. These tokens were exfiltrated to an attacker-controlled `webhook[.]site` endpoint. The workflow runs were deleted minutes later to cover tracks.

**Phase 2 — Pipeline Hijack and Malicious Publish (October 21, 2026):**
Eleven days later, the attacker leveraged the stolen maintainer tokens to override branch protection rules and alter the release pipeline. The source repository was redirected from the legitimate `BerriAI/litellm` to a lookalike repository `Berri-AI/litellm`. This allowed publication of a trojanised LiteLLM v1.107.0 to PyPI at 11:39 a.m. UTC, followed by Docker Hub and GHCR images at 11:46 a.m. UTC. Production and staging run records were then deleted at 11:53 a.m. UTC to hinder forensic investigation.

A contributing factor was that LiteLLM had temporarily relaxed its release approval controls — normally requiring a physical device-locked special account — to accommodate more frequent releases, allowing any two engineers to trigger and approve a release. This relaxation was exploited directly.

Upwind researcher Lidor Machluf identified the attack at 12:06 p.m. UTC, just 27 minutes after publication. PyPI quarantined the package at 1:23 p.m. UTC, and Docker Hub tags were cleaned by 2:20 p.m. UTC.

## Framework Mapping

- **AML.T0010 / AML.T0115**: Classic AI supply chain compromise culminating in publication of poisoned artifacts to PyPI and Docker Hub.
- **AML.T0083 / AML.T0098**: Credentials extracted from the AI Agent Platform configuration and agent tool integration (GitHub CLI token).
- **AML.T0086**: Exfiltration of developer OAuth tokens via agent-triggered workflow and attacker-controlled webhook.
- **LLM05 (Supply Chain Vulnerabilities)**: The entire attack vector exploited weaknesses in the LLM tooling supply chain.
- **LLM06 (Sensitive Information Disclosure)**: Master key and OAuth tokens exposed through misconfigured agent platform.
- **LLM08 (Excessive Agency)**: The agent platform's unscoped GitHub token granted disproportionate access, enabling lateral movement across all org repositories.

## Impact Assessment

Any downstream user or organisation that installed LiteLLM v1.107.0 from PyPI or pulled Docker images tagged v1.107.0, `latest`, `main-latest`, or `main-stable` between 11:39 a.m. and approximately 2:20 p.m. UTC on October 21 is potentially running malicious code. Given LiteLLM's widespread adoption as an LLM gateway, the blast radius could include enterprise AI infrastructure deployments globally.

## Mitigation & Recommendations

1. **Remove LiteLLM v1.107.0 immediately** and replace with a verified clean version.
2. **Rotate all GitHub tokens and credentials** associated with LiteLLM integrations or any similarly configured AI agent platforms.
3. **Scope OAuth tokens to minimum required permissions** — never use organisation owner-level tokens for automated agents.
4. **Automate credential revocation** with TTLs; never rely on manual revocation after accidental exposure.
5. **Harden CI/CD pipeline controls** — avoid temporarily relaxing release approval gates even under operational pressure.
6. **Monitor for lookalike repository activity** in your GitHub organisation settings.

## References

- [The Hacker News — Leaked LiteLLM Master Key](https://thehackernews.com/2026/10/leaked-litellm-master-key-let-attackers.html)
