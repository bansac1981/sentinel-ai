---
title: "LiteLLM 1.107.0 Supply Chain Attack Steals AI Credentials"
date: 2026-10-24T09:44:50+00:00
draft: true
slug: "litellm-1-107-0-supply-chain-attack-steals-ai-credentials"

# ── Content metadata ──
summary: "A malicious version of LiteLLM 1.107.0 was published to PyPI on October 21, 2026, embedding credential-harvesting payloads that execute automatically during Python interpreter startup\u2014before any import statement is reached. The attack targeted authentication material across developer tools, AI applications, cloud environments, and browsers, with a secondary module specifically targeting LiteLLM proxy credential and model-configuration records. Defenders are warned not to invoke Python or pip inside suspect environments, as doing so can trigger the payload."
source: "Microsoft Security Blog"
source_url: "https://www.microsoft.com/en-us/security/blog/2026/10/23/inside-the-litellm-1-107-0-supply-chain-compromise-credential-theft-through-python-startup-hooks"
source_title: "Inside the LiteLLM 1.107.0 supply chain compromise: Credential theft through Python startup hooks"
source_date: 2026-10-23T18:12:19+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1597418895783-f7de85be2839?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw3fHx0ZXh0JTIwdHlwb2dyYXBoeSUyMGFic3RyYWN0JTIwbGV0dGVyc3xlbnwwfDB8fHwxNzkyODM1MDkwfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0086 - Exfiltration via AI Agent Tool Invocation"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "LiteLLM 1.107.0 on PyPI contained credential-stealing payloads triggered at Python startup."
tldr_who_at_risk: "Developers, MLOps teams, and AI platform operators who installed LiteLLM 1.107.0 or its container images are directly exposed to credential theft across cloud, browser, and AI tooling."
tldr_actions: ["Do not run Python or pip inside any environment where LiteLLM 1.107.0 may be installed", "Audit PyPI package versions and container image digests; roll back to a verified clean release", "Rotate all credentials accessible from affected environments, including cloud keys, AI API tokens, and browser-stored secrets"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Agentic AI"]
tags: ["litellm", "supply-chain-attack", "pypi", "credential-theft", "python-startup-hooks", "ai-infrastructure", "llm-proxy", "microsoft-security", "malicious-package", "windows", "macos"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-24T09:44:50+00:00"
feed_source: "microsoft_security"
original_url: "https://www.microsoft.com/en-us/security/blog/2026/10/23/inside-the-litellm-1-107-0-supply-chain-compromise-credential-theft-through-python-startup-hooks"
pipeline_version: "2.1.0"
---

## Overview

On October 21, 2026, threat actors published a trojanised version of LiteLLM—version 1.107.0—to the Python Package Index (PyPI) and embedded the malicious payload within official container images. LiteLLM is a widely used open-source library that provides a unified interface for calling large language model APIs, making it a high-value target for supply chain compromise. Microsoft Security Research disclosed the campaign on October 23, 2026, after observing active payload execution on Windows and macOS endpoints.

The attack is particularly dangerous because the payload does not require an explicit `import litellm` statement. By abusing Python interpreter startup mechanisms—specifically path extensions and site-specific configuration hooks—the credential collector can execute the moment Python is launched in an affected environment. This means routine operations such as installing an unrelated package via pip can silently activate the malware.

## Technical Analysis

Microsoft identified two distinct execution paths embedded in the compromised wheels:

**1. Path extension credential collector:** A file placed in a location Python scans during interpreter initialisation. This collector targets authentication material from developer tools, AI applications, cloud provider credential stores, web browsers, and infrastructure tooling.

**2. Unix-oriented site loader:** Persisted through site-specific configuration (e.g., `.pth` files or `sitecustomize.py`), ensuring execution on affected Linux and macOS systems across sessions.

A third component—a database module—attempted to extract credential records and model-configuration data directly from the LiteLLM proxy database, specifically targeting AI API keys and provider configurations stored by the proxy service.

Endpoint telemetry on both Windows and macOS confirmed the collector's full kill chain: local discovery of credential material, encryption of harvested data, and outbound exfiltration. In one documented Windows case, a developer invoking pip to install an unrelated dependency triggered the full collector sequence.

A critical operational warning from Microsoft: **investigators must not start Python or pip inside a suspect environment** to assess exposure. Doing so can trigger payload execution and initiate credential exfiltration.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| ATLAS AML.T0010 | AI Supply Chain Compromise | Malicious package published to PyPI targeting AI tooling consumers |
| ATLAS AML.T0115 | Publish Poisoned AI Artifacts | Trojanised wheel and container images distributed through official channels |
| ATLAS AML.T0083 | Credentials from AI Agent Configuration | Database module reads LiteLLM proxy credential and model config records |
| ATLAS AML.T0098 | AI Agent Tool Credential Harvesting | Broad credential sweep across AI application credential stores |
| OWASP LLM05 | Supply Chain Vulnerabilities | Compromise introduced at the package distribution layer |
| OWASP LLM06 | Sensitive Information Disclosure | AI API keys, cloud credentials, and model configs exfiltrated |

## Impact Assessment

Any developer, MLOps engineer, or AI platform operator who installed LiteLLM 1.107.0 or deployed its container images between October 21 and the disclosure date should assume credential compromise. The scope of harvested material is broad: cloud provider keys, AI API tokens (including those for LLM providers routed through the proxy), browser-stored credentials, and infrastructure secrets. Organisations running LiteLLM as a centralised AI gateway face amplified risk, as a single compromised proxy instance may expose API keys for multiple downstream LLM providers.

## Mitigation & Recommendations

- **Isolate immediately:** Do not execute Python, pip, or any Python-based tooling inside environments where LiteLLM 1.107.0 may be installed. Use out-of-band inspection methods.
- **Verify and roll back:** Audit installed package versions and container image digests. Downgrade to a verified clean release or await a patched version from the LiteLLM maintainers.
- **Rotate all credentials:** Treat all secrets accessible from affected environments as compromised. Prioritise cloud provider keys, LLM API tokens, and any credentials stored in browsers or developer tools on affected hosts.
- **Review LiteLLM proxy logs:** Check for anomalous database queries or outbound connections from proxy instances.
- **Enable Defender detections:** Microsoft Defender has published indicators of compromise (IoCs) and detection guidance aligned to this campaign.

## References

- [Microsoft Security Blog — Inside the LiteLLM 1.107.0 supply chain compromise](https://www.microsoft.com/en-us/security/blog/2026/10/23/inside-the-litellm-1-107-0-supply-chain-compromise-credential-theft-through-python-startup-hooks)
