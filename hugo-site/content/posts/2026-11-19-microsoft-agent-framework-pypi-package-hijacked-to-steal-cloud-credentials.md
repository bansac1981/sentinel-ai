---
title: "Microsoft Agent Framework PyPI Package Hijacked to Steal Cloud Credentials"
date: 2026-11-19T08:23:42+00:00
draft: false
slug: "microsoft-agent-framework-pypi-package-hijacked-to-steal-cloud-credentials"

# ── Content metadata ──
summary: "Attackers compromised Microsoft's official Agent Framework PyPI package, publishing two malicious versions that silently executed a credential stealer targeting Azure, AWS, GitHub, OpenAI, and other cloud services during Python startup. The malware used Python path configuration files (.pth) to auto-execute without requiring an explicit import, maximising reach across developer environments. Both malicious releases were quarantined within minutes, but the rapid republication indicates the attacker retained publishing access throughout the incident."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/microsofts-agent-framework-pypi-package-compromised-to-steal-credentials"
source_title: "Microsoft\u2019s Agent Framework PyPI package compromised to steal credentials"
source_date: 2026-11-18T16:58:42+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1662947036583-d67dd8055edf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxfHxNaWNyb3NvZnQlMjBjaGVzcyUyMHBpZWNlJTIwc3RyYXRlZ3klMjBib2FyZCUyMGdhbWV8ZW58MHwwfHx8MTc5NTA3NjYyMXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0084 - Discover AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Microsoft's Agent Framework PyPI package was backdoored to silently steal cloud credentials from developer environments."
tldr_who_at_risk: "Developers and CI/CD pipelines that installed agent-framework versions 1.26.1 or 1.26.2 are directly exposed, particularly those with Azure, AWS, GitHub, or OpenAI credentials in their environments."
tldr_actions: ["Immediately audit environments for agent-framework versions 1.26.1 or 1.26.2 and remove them", "Rotate all cloud credentials (Azure, AWS, GitHub tokens, OpenAI API keys) accessible from affected systems", "Review GitHub Actions OIDC tokens and Azure managed identity access logs for unauthorised use"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Industry News"]
tags: ["pypi", "supply-chain-attack", "credential-theft", "microsoft-agent-framework", "ai-agents", "azure", "github-actions", "cloud-credentials", "python-package", "open-source-security", "malicious-package", "developer-tooling"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-19T08:23:42+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/microsofts-agent-framework-pypi-package-compromised-to-steal-credentials"
pipeline_version: "2.1.0"
content_hash: "e4ff6ea245eeb4fb"
---

## Overview

On 17 November 2026, threat actors compromised Microsoft's official `agent-framework` Python package on PyPI, publishing two successive malicious versions — 1.26.1 and 1.26.2 — targeting developers building AI agent workflows. With approximately 200,000 monthly downloads, the package is widely used across enterprise and research environments. Both versions embedded a credential stealer that executed automatically at Python startup, well before any explicit import of the framework itself.

This incident represents a high-severity supply chain attack directly targeting the AI agent development ecosystem, with credential exfiltration scoped to the most sensitive cloud and AI service accounts a developer is likely to hold.

## Technical Analysis

The attack leveraged Python's `.pth` file mechanism — a legitimate feature that allows packages to register code paths executed at interpreter startup — to ensure the malicious payload ran in every Python process on the host, regardless of whether `agent-framework` was explicitly imported.

**Version 1.26.1** used `agent_framework_meta.pth` to trigger execution of `agent_framework_meta/_telemetry.py`. Targeted credential sources included:
- Environment variables (Azure, AWS, GitHub, Docker, Hugging Face, OpenAI)
- Local configuration files and running process memory (where permissions allowed)
- Azure managed identity access tokens
- Azure DevOps OIDC tokens

**Version 1.26.2** restored the legitimate package initialiser to reduce suspicion, relocating the payload to `af_runtime_diag.pth` and `af_runtime_diag.py`. It extended targeting to GitHub Actions OIDC tokens and GitHub runner directory contents — indicating deliberate CI/CD pipeline targeting.

All collected data was exfiltrated to a single attacker-controlled webhook endpoint: `https://webhook[.]site/d381fd80-ec62-42ad-8f5c-d1b15103c9bb`.

Notably, the legitimate dependency `agent-framework-core 1.26.0` was retained in both versions, allowing the framework to function normally and reducing the likelihood of detection through functional testing.

## Framework Mapping

- **AML.T0010 / AML.T0115**: Classic AI supply chain compromise via publication of poisoned artifacts to a trusted package registry.
- **AML.T0083 / AML.T0098**: The malware explicitly targeted credentials stored in AI agent configurations and tool environments, including OpenAI and Hugging Face API keys.
- **AML.T0086**: Data exfiltration was routed through a webhook endpoint, consistent with exfiltration via external service invocation.
- **LLM05 (Supply Chain Vulnerabilities)**: The attack exploited implicit trust in an official, high-download-count package maintained by a major vendor.
- **LLM06 (Sensitive Information Disclosure)**: Credentials for AI services (OpenAI, Hugging Face) were harvested alongside cloud provider secrets.

## Impact Assessment

Any developer or CI/CD pipeline that installed versions 1.26.1 or 1.26.2 of `agent-framework` between 17 November 2026 and the quarantine windows should be treated as fully compromised. The automatic startup execution model means the stealer ran even in environments where the package was present in the dependency tree but not actively used. The targeting of GitHub Actions OIDC tokens specifically elevates risk for automated build pipelines, potentially enabling lateral movement into source repositories and cloud infrastructure.

## Mitigation & Recommendations

1. **Remove malicious versions**: Uninstall `agent-framework` 1.26.1 and 1.26.2 immediately from all affected environments.
2. **Rotate all exposed credentials**: Treat Azure, AWS, GitHub, OpenAI, Hugging Face, and Docker credentials as compromised if present in any affected environment.
3. **Audit OIDC and managed identity usage**: Review Azure and GitHub Actions OIDC token issuance logs for anomalous activity in the exposure window.
4. **Scan for `.pth` file persistence**: Audit Python environments for unexpected `.pth` files that may indicate residual persistence.
5. **Implement package integrity controls**: Enforce hash pinning and code review gates for third-party package updates in CI/CD pipelines.

## References

- [BleepingComputer — Microsoft's Agent Framework PyPI package compromised to steal credentials](https://www.bleepingcomputer.com/news/security/microsofts-agent-framework-pypi-package-compromised-to-steal-credentials)
