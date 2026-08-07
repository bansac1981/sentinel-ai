---
title: "PyTorch Lightning Package Backdoor Steals Developer Credentials"
date: "2026-05-05T05:36:41+00:00"
draft: false
slug: "backdoored-pytorch-lightning-package-steals-cloud-credentials-from-ai-developers"

# ── Content metadata ──
summary: "A malicious version of PyTorch Lightning (v2.6.3) was published to PyPI, embedding a hidden execution chain that silently downloads a JavaScript runtime and executes a heavily obfuscated credential-stealing payload dubbed 'ShaiWorm'. The attack targeted AI/ML developers who use this popular deep learning framework, exposing cloud credentials, API keys, browser-stored secrets, and GitHub tokens. The package has since been reverted to a safe version, but any developer who imported the compromised version should rotate all secrets immediately."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/backdoored-pytorch-lightning-package-drops-credential-stealer/"
source_title: "Backdoored PyTorch Lightning package drops credential stealer"
source_date: 2026-05-04T17:15:27+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1549605659-32d82da3a059?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxiYWNrZG9vciUyMHNoYWRvdyUyMGhhY2tpbmclMjBzZXJ2ZXJ8ZW58MHwwfHx8MTc3Nzk1NDg3N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0018 - Backdoor ML Model", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Backdoored PyTorch Lightning v2.6.3 on PyPI silently stole cloud credentials from AI developers."
tldr_who_at_risk: "AI/ML developers who installed or imported PyTorch Lightning v2.6.3 are at risk of having cloud, browser, and API credentials exfiltrated."
tldr_actions:
  - "Immediately downgrade to PyTorch Lightning v2.6.1 or the latest safe release"
  - "Rotate all secrets, API keys, GitHub tokens, and cloud credentials if v2.6.3 was imported"
  - "Audit CI/CD pipelines and developer environments for signs of ShaiWorm activity"

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["pypi", "pytorch-lightning", "supply-chain-attack", "credential-stealer", "malicious-package", "shaiworm", "cloud-credentials", "ai-developer-tools", "javascript-payload", "information-stealer"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-05-05T04:21:17+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/backdoored-pytorch-lightning-package-drops-credential-stealer/"
pipeline_version: "1.0.0"
---

## Overview

A supply chain attack targeting the AI/ML developer community was disclosed on April 30, 2026, after the maintainers of PyTorch Lightning confirmed that version 2.6.3 of their popular deep learning framework had been backdoored. Published to the Python Package Index (PyPI), the compromised package contained a hidden execution chain designed to silently steal credentials from cloud platforms, browsers, and environment files. With over 11 million downloads in the preceding month, the package represents a high-value target for threat actors looking to compromise AI infrastructure at scale.

## Technical Analysis

The malicious payload embedded in `lightning==2.6.3` (distributed as a `py3-none-any` wheel) triggers automatically upon execution of `import lightning`. The execution chain proceeds as follows:

1. **Silent background process spawning**: On import, the package silently forks a background process without user interaction or visible output.
2. **Runtime download**: The background process fetches the Bun JavaScript runtime (v1.3.13) from GitHub, providing an execution environment not typically present in Python ML workflows.
3. **Payload execution**: A heavily obfuscated 11.4 MB JavaScript file (`router_runtime.js`) is downloaded and executed within the Bun runtime.

The payload, detected by Microsoft Defender as **ShaiWorm**, is a full-featured information stealer with the following capabilities:

- Exfiltration of `.env` files, API keys, and secrets
- Theft of GitHub tokens
- Browser credential harvesting (Chrome, Firefox, Brave)
- Cloud service API credential theft (AWS, Azure, GCP)
- Arbitrary system command execution

The use of a JavaScript runtime (Bun) delivered at execution time is a notable evasion technique, as it avoids embedding binary payloads directly in the Python package and bypasses static analysis tools that focus on Python code.

## Framework Mapping

- **AML.T0010 – ML Supply Chain Compromise**: The attack directly targets the ML software supply chain by injecting malicious code into a widely used deep learning framework package on PyPI.
- **AML.T0018 – Backdoor ML Model**: While this attack targets the framework rather than a model directly, the technique of embedding hidden execution logic in a trusted AI development tool mirrors backdoor insertion patterns.
- **AML.T0012 – Valid Accounts**: The ultimate goal of credential theft is to leverage stolen valid credentials for further access to cloud infrastructure and code repositories.
- **LLM05 – Supply Chain Vulnerabilities**: The attack exploits trust in the PyPI ecosystem, a critical dependency chain for LLM training and fine-tuning workflows.
- **LLM06 – Sensitive Information Disclosure**: Stolen API keys and cloud credentials can expose model weights, training data, and proprietary AI infrastructure.

## Impact Assessment

Microsoft Threat Intelligence confirmed that Defender detected and blocked the malicious routine across customer environments, with impact reported as limited to "a small number of devices" in a "narrow set of environments." However, given the package's 11 million monthly downloads, the potential exposure window before detection was significant. Developers using automated pipelines or CI/CD systems that pull latest package versions without pinning are most at risk. Compromised cloud credentials could provide persistent access to AI training infrastructure, model repositories, and sensitive datasets.

## Mitigation & Recommendations

- **Downgrade immediately**: Revert to `pytorch-lightning==2.6.1`, which is confirmed safe, or await an updated clean release.
- **Rotate all credentials**: Any environment where `import lightning` was executed with v2.6.3 should treat all secrets, tokens, and API keys as compromised.
- **Audit for ShaiWorm indicators**: Review endpoint logs for unexpected Bun runtime downloads, `router_runtime.js` execution, or anomalous outbound connections.
- **Pin package versions**: Enforce version pinning in `requirements.txt` and lockfiles to prevent silent upgrades to malicious releases.
- **Enable runtime monitoring**: Deploy behaviour-based endpoint detection capable of flagging unexpected background process spawning from Python import hooks.

## References

- [BleepingComputer – Backdoored PyTorch Lightning package drops credential stealer](https://www.bleepingcomputer.com/news/security/backdoored-pytorch-lightning-package-drops-credential-stealer/)
