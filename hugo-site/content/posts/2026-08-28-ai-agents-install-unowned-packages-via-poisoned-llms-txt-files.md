---
title: "AI Agents Install Unowned Packages via Poisoned llms.txt Files"
date: "2026-08-28T04:20:17+00:00"
draft: false 
slug: "ai-agents-install-unowned-packages-via-poisoned-llms-txt-files"

# ── Content metadata ──
summary: "Researchers discovered that over 120 corporate websites contained misconfigured llms.txt files referencing unregistered package names, which AI coding agents including Claude, Codex, and Hermes automatically executed as trusted installation instructions. By registering a handful of the unclaimed package names and hosting beacon payloads, researchers received phone-home responses from dozens of companies including Fortune 500 firms within hours, confirming real-world agent-driven supply chain compromise. The attack exploits the implicit trust AI agents place in vendor documentation files, with at least one site found directing visitors to live malware."
source: "Ars Technica Security"
source_url: "https://arstechnica.com/security/2026/08/claude-codex-and-hermes-installed-unowned-code-inside-corporate-networks"
source_title: "Claude, Codex, and Hermes installed unowned code inside corporate networks"
source_date: 2026-08-27T14:00:13+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1545696648-86c761bc5410?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxM3x8bGlicmFyeSUyMGJvb2tzJTIwa25vd2xlZGdlJTIwcm93c3xlbnwwfDB8fHwxNzg3ODg4NzIyfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0099 - AI Agent Tool Data Poisoning", "AML.T0080 - AI Agent Context Poisoning", "AML.T0067 - LLM Trusted Output Components Manipulation", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM09 - Overreliance", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "AI coding agents auto-installed unowned packages from poisoned llms.txt files in corporate networks."
tldr_who_at_risk: "Any organisation running AI coding agents with shell execution permissions against external vendor documentation is directly exposed to arbitrary code execution."
tldr_actions: ["Audit all llms.txt and llms-full.txt files on corporate domains for references to unregistered package names", "Restrict AI agent shell execution permissions and require human approval before installing any package from external documentation", "Implement allowlist-based package installation policies and monitor for unexpected outbound connections from agent environments"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Research"]
tags: ["llms-txt", "ai-agents", "supply-chain", "dependency-confusion", "claude", "codex", "hermes", "package-squatting", "coding-agents", "fortune-500", "typosquatting", "agentic-ai", "shell-execution", "pypi", "npm"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-28T03:45:22+00:00"
feed_source: "arstechnica"
original_url: "https://arstechnica.com/security/2026/08/claude-codex-and-hermes-installed-unowned-code-inside-corporate-networks"
pipeline_version: "2.1.0"
---

## Overview

Researchers at an Israeli stealth startup have uncovered a novel AI agent supply chain attack vector exploiting `llms.txt` and `llms-full.txt` files — the emerging machine-readable documentation standard analogous to `robots.txt`. By scanning 6,214 corporate domains, they identified 120 sites whose llms.txt files referenced unregistered package names on PyPI, npm, and other registries. Registering a subset of those names and hosting beacon payloads, the team confirmed that AI coding agents — including Anthropic's Claude, OpenAI's Codex, and Nous Research's Hermes — automatically executed the packages inside live corporate networks, with Fortune 500 firms among the victims.

## Technical Analysis

The attack chain is straightforward but consequential. A misconfigured `llms.txt` or `llms-full.txt` file contains installation instructions such as:

```
Installation: pip install <unregistered-package-name>
```

or

```
npm install <unregistered-package-name>
```

When an AI coding agent ingests this file as authoritative setup documentation and holds shell execution permissions, it treats the instruction as ground truth and runs the install command without independent verification. Because the package name is unregistered, any attacker may claim it on the relevant registry and push arbitrary code — ransomware, backdoors, or data exfiltration tools — that the agent will then execute in the context of the corporate environment.

The researchers' proof-of-concept packages phoned home with process chain data, revealing the specific agents involved. At least one production site was already serving live malware rather than a benign beacon at the time of discovery.

This is structurally identical to dependency confusion attacks but automated at scale by AI agents that treat documentation as executable truth, dramatically accelerating the exploitation timeline from days to minutes.

## Framework Mapping

- **AML.T0010 / AML.T0115 (AI Supply Chain Compromise / Publish Poisoned AI Artifacts):** Attackers register abandoned package names to inject malicious code into agent-driven install pipelines.
- **AML.T0110 / AML.T0099 (AI Agent Tool Poisoning / Tool Data Poisoning):** The llms.txt file acts as a poisoned context source that directs the agent's tool use.
- **AML.T0067 (LLM Trusted Output Components Manipulation):** Agents treat vendor documentation as authoritative without verification.
- **LLM05 (Supply Chain Vulnerabilities):** The package registry supply chain is the ultimate execution path.
- **LLM08 (Excessive Agency):** Agents executing shell commands based on unverified external documentation exemplifies unconstrained agency.
- **LLM09 (Overreliance):** Human supervisors and agents alike treat llms.txt content as ground truth.

## Impact Assessment

The confirmed victim set includes multiple Fortune 500 companies and a broader population of startups. The attack surface scales with the adoption of AI coding agents, which are now embedded across SaaS platforms, cloud environments, and developer endpoints. Any organisation that uses agentic coding tools against external documentation without sandboxing or install approval workflows is exposed. The presence of at least one live malware-serving site in the dataset indicates this vector is already being weaponised beyond research contexts.

## Mitigation & Recommendations

1. **Audit your own llms.txt files** for references to unregistered or abandoned package names immediately; claim or remove them.
2. **Restrict agent shell permissions** — coding agents should not execute install commands from external documentation without explicit human-in-the-loop approval.
3. **Implement package allowlists** in CI/CD and agent environments; reject any package not pre-approved by a security review.
4. **Monitor outbound network connections** from agent execution environments for unexpected phone-home behaviour.
5. **Treat llms.txt as untrusted input** — validate all referenced packages against internal inventories before agents act on them.

## References

- [Ars Technica: Claude, Codex, and Hermes installed unowned code inside corporate networks](https://arstechnica.com/security/2026/08/claude-codex-and-hermes-installed-unowned-code-inside-corporate-networks)
