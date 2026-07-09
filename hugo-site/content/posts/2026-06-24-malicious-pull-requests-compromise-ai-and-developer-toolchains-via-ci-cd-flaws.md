---
title: "Cordyceps Campaign Poisons CI/CD Pipelines Across Open Source"
date: "2026-06-24T04:27:38+00:00"
draft: false 
slug: "malicious-pull-requests-compromise-ai-and-developer-toolchains-via-ci-cd-flaws"

# ── Content metadata ──
summary: "A campaign dubbed 'Cordyceps' is exploiting weaknesses in CI/CD workflows to inject malicious pull requests into high-profile open-source projects, including Google's AI Agent Development Kit and Microsoft's Azure Sentinel. The attack surface spans multiple trusted ecosystems, meaning poisoned code could propagate into AI tooling, cloud infrastructure, and widely-used developer utilities before detection. The breadth of targets \u2014 including Python's Black formatter \u2014 signals a supply chain strategy designed to maximise downstream blast radius."
source: "Dark Reading"
source_url: "https://www.darkreading.com/application-security/cordyceps-malicious-pull-requests-developer-workflows"
source_title: "'Cordyceps': Mushrooming Malicious Pull Requests Threaten Developer Workflows"
source_date: 2026-06-23T19:16:42+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/1148820/pexels-photo-1148820.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0020 - Poison Training Data", "AML.T0018 - Backdoor ML Model", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM03 - Training Data Poisoning"]

# ── TL;DR ──
tldr_what: "Malicious pull requests targeting CI/CD pipelines compromise AI and developer tools across major vendors."
tldr_who_at_risk: "Developers and organisations consuming open-source packages from Azure Sentinel, Google's AI ADK, Apache Doris, Cloudflare Workers SDK, or Python Black are directly exposed to poisoned build artifacts."
tldr_actions: ["Audit all recent pull request merges in affected repositories for unauthorised or anomalous changes", "Enforce mandatory code review and signed commit policies before any CI/CD pipeline execution", "Pin dependency versions and verify checksums/SBOMs for all third-party packages in AI and cloud toolchains"]

# ── Taxonomies ──
categories: ["Supply Chain", "Agentic AI", "LLM Security", "Industry News"]
tags: ["ci-cd", "pull-request-poisoning", "supply-chain-attack", "cordyceps", "azure-sentinel", "google-ai-agent-development-kit", "open-source-security", "developer-toolchain", "workflow-compromise", "apache-doris", "cloudflare-workers", "python-black"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-06-24T04:07:22+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/application-security/cordyceps-malicious-pull-requests-developer-workflows"
pipeline_version: "2.1.0"
---

## Overview

A coordinated attack campaign, named 'Cordyceps' after the parasitic fungus that hijacks its host, is exploiting weaknesses in CI/CD pipeline workflows to introduce malicious pull requests (PRs) into prominent open-source repositories. Confirmed targets include Microsoft's Azure Sentinel, Google's AI Agent Development Kit (ADK), Apache's Doris analytics database, Cloudflare's Workers SDK, and Python Software Foundation's Black code formatter. The campaign is notable both for its breadth and for the strategic selection of targets — tools that sit deep inside developer and AI engineering workflows, maximising the potential for widespread downstream compromise.

## Technical Analysis

The attack exploits permissive or insufficiently guarded CI/CD pipeline configurations, a well-documented but persistently undermitigated weakness in open-source project management. Attackers submit pull requests that appear legitimate — often small, plausible changes — while embedding malicious logic that executes during automated pipeline steps such as testing, linting, or build artifact generation.

In workflows where CI runners execute PR code with elevated privileges or access to secrets, a malicious PR can:

- Exfiltrate repository secrets and API tokens via environment variables
- Inject backdoors into build artifacts published to package registries
- Tamper with model training scripts or data pipelines in AI-adjacent repositories
- Establish persistence for future supply chain compromise

The inclusion of Google's AI Agent Development Kit is particularly significant. If malicious code reaches ADK builds consumed by downstream AI agent developers, it could introduce subtle backdoors or data exfiltration hooks into agentic AI systems at the framework level — a high-leverage attack vector given the rapidly growing adoption of agentic architectures.

```yaml
# Example of a vulnerable GitHub Actions workflow pattern
on:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: ./scripts/test.sh  # Executes untrusted PR code with CI runner privileges
```

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0010 (ML Supply Chain Compromise):** The campaign directly targets AI tooling repositories to compromise upstream components consumed by ML practitioners.
- **AML.T0018 (Backdoor ML Model):** Malicious PRs in AI development frameworks could introduce model-level backdoors affecting downstream training or inference.
- **AML.T0020 (Poison Training Data):** Compromised data pipeline tooling could silently corrupt datasets feeding AI model training.

**OWASP LLM Top 10:**
- **LLM05 (Supply Chain Vulnerabilities):** The core attack vector — poisoning trusted upstream repositories to compromise consumers.
- **LLM03 (Training Data Poisoning):** Relevant where affected tooling touches data ingestion or preprocessing for AI systems.

## Impact Assessment

The impact is tiered. Immediate risk falls on maintainers and contributors of the five identified repositories. Secondary risk — and arguably the more severe — falls on the entire downstream ecosystem consuming build artifacts, packages, or framework code from these projects. For AI practitioners using Google's ADK, a compromised dependency could silently alter agent behaviour, exfiltrate inference data, or create exploitable logic flaws in production agentic systems. The Python Black formatter's inclusion is notable: as a ubiquitous formatting tool integrated into thousands of development pipelines, a compromised release would have exceptional reach.

## Mitigation & Recommendations

1. **Restrict CI/CD trigger permissions** — workflows triggered by external PRs must not execute with write permissions or access to repository secrets without explicit approval gates.
2. **Implement `pull_request_target` safeguards** — avoid using this GitHub Actions trigger carelessly; it runs in the context of the base branch and can expose secrets.
3. **Require maintainer approval before CI execution** on all external PRs, particularly for sensitive pipeline steps.
4. **Audit recent PR merges** across affected repositories and verify build artifact integrity using SBOMs and published checksums.
5. **Pin all dependency versions** and validate against a known-good hash registry to detect tampering in consumed packages.
6. **Monitor for unusual CI job behaviour** — unexpected network egress, environment variable access, or artifact modifications during PR pipelines.

## References

- [Dark Reading: 'Cordyceps': Mushrooming Malicious Pull Requests Threaten Developer Workflows](https://www.darkreading.com/application-security/cordyceps-malicious-pull-requests-developer-workflows)
