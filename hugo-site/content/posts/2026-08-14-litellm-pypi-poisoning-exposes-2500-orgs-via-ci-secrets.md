---
title: "LiteLLM PyPI Poisoning Exposes 2,500+ Orgs via CI Secrets"
date: "2026-08-14T07:17:23+00:00"
draft: false
slug: "litellm-pypi-poisoning-exposes-2500-orgs-via-ci-secrets"

# ── Content metadata ──
summary: "Two malicious LiteLLM releases (versions 1.82.7 and 1.82.8) were uploaded to PyPI on March 24 and remained live for approximately 40 minutes, carrying credential-stealing code that harvested cloud keys, SSH keys, Kubernetes tokens, and database passwords. CloudSEK's analysis of roughly 434,000 captured files maps potential exposure to more than 2,500 organisations, including NVIDIA, Cisco, and Siemens, though the dataset reflects files taken rather than confirmed misuse. The FBI has separately warned that affiliated actors are likely to weaponise exfiltrated credentials long after the initial compromise, making immediate secret rotation critical regardless of confirmed exploitation."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/malicious-litellm-releases-tied-to.html"
source_title: "Malicious LiteLLM Releases Tied to Trivy Hack May Have Exposed 2,100+ Organizations"
source_date: 2026-08-12T08:04:52+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1624421514201-db391243ed51?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHxuZXVyYWwlMjBwYXR0ZXJuJTIwYWJzdHJhY3QlMjBuZXR3b3JrJTIwbGlnaHR8ZW58MHwwfHx8MTc4NjY4Mzc2N3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.1
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0115 - Publish Poisoned AI Artifacts", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "Malicious LiteLLM PyPI releases stole cloud and CI secrets from 2,500+ organisations in 40 minutes."
tldr_who_at_risk: "Any organisation or developer that installed LiteLLM on March 24, 2026, particularly those running automated CI/CD pipelines with long-lived cloud or Kubernetes credentials."
tldr_actions: ["Immediately rotate all cloud keys, SSH keys, Kubernetes tokens, and publishing tokens accessible during the March 24 exposure window", "Audit Python environments for the presence of litellm_init.pth and remove any compromised LiteLLM versions (1.82.7, 1.82.8)", "Migrate CI/CD pipelines from long-lived static credentials to short-lived, scoped temporary tokens"]

# ── Taxonomies ──
categories: ["Supply Chain", "LLM Security", "Industry News"]
tags: ["litellm", "pypi", "supply-chain-attack", "credential-theft", "ci-cd-security", "cloud-keys", "kubernetes", "ssh-keys", "open-source-poisoning", "teamcp-campaign", "cloudSEK", "llm-gateway"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-14T05:02:47+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/malicious-litellm-releases-tied-to.html"
pipeline_version: "2.1.0"
---

## Overview

Two trojanised releases of LiteLLM — an open-source AI gateway widely used to route requests across multiple LLM providers — were published to PyPI on 24 March 2026 and remained available for approximately 40 minutes before the package registry quarantined them. Versions 1.82.7 and 1.82.8 carried credential-stealing code capable of harvesting environment variables, cloud access keys, SSH private keys, Kubernetes service account tokens, and database passwords from any system that installed them. LiteLLM advises treating any installation performed on that date up to 16:00 UTC as suspect.

Threat intelligence firm CloudSEK subsequently obtained a dataset of roughly 434,000 files captured by the attackers and assessed as belonging to the campaign. Its analysis maps potential exposure to more than 2,500 organisations, including NVIDIA, Cisco, Deloitte, Volkswagen, FedEx, Siemens, and X Corp. CloudSEK has published the data as a public searchable lookup with high- and medium-confidence confidence tiers. A high-confidence match requires the organisation's own domain to appear alongside host identity signals in the captured CI runner environment; repository namespaces alone earn only medium confidence.

## Technical Analysis

The primary persistence and execution mechanism was a file named `litellm_init.pth` bundled inside version 1.82.8. Python processes `.pth` files in `site-packages` at interpreter startup — meaning the malicious code executed whenever *any* Python process launched in the affected environment, irrespective of whether LiteLLM was imported. This is a particularly effective technique in CI/CD contexts where Python interpreters are invoked continuously across many jobs.

The payload was designed to enumerate and exfiltrate:
- Environment variables (including `AWS_ACCESS_KEY_ID`, `GITHUB_TOKEN`, etc.)
- SSH private keys from `~/.ssh/`
- Kubernetes service account tokens from `/var/run/secrets/`
- Cloud provider credential files (`.aws/credentials`, application default credentials)
- Database connection strings

All collected material was staged and transmitted to attacker-controlled infrastructure. The 40-minute exposure window on a heavily downloaded package was sufficient to seed thousands of CI runs across the global developer ecosystem.

## Framework Mapping

- **AML.T0115 – Publish Poisoned AI Artifacts**: Attackers directly injected malicious code into a legitimate LLM-infrastructure package distributed via PyPI.
- **AML.T0010 – AI Supply Chain Compromise**: LiteLLM occupies a strategic position in AI/LLM deployment pipelines, making it a high-value supply chain target.
- **AML.T0083 – Credentials from AI Agent Configuration**: Stolen credentials included tokens and keys used to authenticate AI workloads and agent runtimes.
- **LLM05 – Supply Chain Vulnerabilities**: The attack exploited trust in a widely used open-source LLM middleware package.
- **LLM06 – Sensitive Information Disclosure**: Exfiltrated secrets directly expose downstream AI infrastructure and cloud environments.

## Impact Assessment

Exposure is broad rather than deep in the confirmed sense: CloudSEK's dataset establishes that files *were taken* from systems attributable to 2,500+ organisations, not that credentials *were used*. However, the FBI's July 2026 advisory (FLASH-20260702-01) explicitly warns that affiliated actors in the linked TeamPCP campaign are likely to weaponise exfiltrated credentials long after initial compromise. Long-lived static secrets — cloud IAM keys, SSH keys, publishing tokens — remain fully valid unless rotated, meaning the attack surface persists months after the original incident.

## Mitigation & Recommendations

1. **Rotate all secrets immediately**: Any cloud API key, SSH private key, Kubernetes token, or CI/CD publishing token that could have been present in a Python environment on 24 March 2026 should be revoked and reissued regardless of confirmed exploitation.
2. **Scan for litellm_init.pth**: Check `site-packages` directories across all build agents and developer workstations for this file and remove it.
3. **Pin and verify package versions**: Use hash-pinned dependencies (`pip install --require-hashes`) and verify checksums against known-good releases.
4. **Adopt short-lived credentials**: Migrate CI/CD pipelines to OIDC-based ephemeral tokens (e.g., GitHub Actions OIDC with AWS, GCP, or Azure) to limit blast radius of any future supply chain compromise.
5. **Monitor for credential abuse**: Enable anomaly detection on cloud accounts for access from unexpected IP ranges or unusual API call patterns.

## References

- [The Hacker News – Original Report](https://thehackernews.com/2026/08/malicious-litellm-releases-tied-to.html)
- [CloudSEK Public Lookup Dataset](https://cloudsek.com)
- [FBI Advisory FLASH-20260702-01](https://www.fbi.gov)
