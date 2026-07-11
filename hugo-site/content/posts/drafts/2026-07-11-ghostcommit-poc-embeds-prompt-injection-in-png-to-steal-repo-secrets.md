---
title: "Ghostcommit PoC Embeds Prompt Injection in PNG to Steal Repo Secrets"
date: 2026-07-11T10:37:46+00:00
draft: false
slug: "ghostcommit-poc-embeds-prompt-injection-in-png-to-steal-repo-secrets"

# ── Content metadata ──
summary: "Researchers from UMKC's ASSET Research Group have published a proof-of-concept attack called Ghostcommit that hides malicious prompt injection instructions inside PNG image files referenced by AGENTS.md convention files, causing AI coding agents to silently exfiltrate repository secrets. The technique exploits a blind spot shared by multiple AI code review tools \u2014 including CodeRabbit and Bugbot \u2014 which exclude or ignore binary image files from analysis, allowing the payload to survive review undetected. Defenders operating AI-assisted development pipelines must treat image files in agentic context paths as a new, uncontrolled input surface and reassess trust boundaries around automatically-ingested project convention files."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets"
source_title: "'Ghostcommit' hides prompt injection in images to fool AI agents, steal secrets"
source_date: 2026-07-11T09:03:57+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1642783327432-d269921e0f20?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyM3x8Y29tcHV0ZXIlMjBzZWN1cml0eSUyMHNoaWVsZCUyMHdhcm5pbmd8ZW58MHwwfHx8MTc4Mzc2NjI2Nnww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 8.7
adoption_velocity: "RAPID"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Hiding prompt injection payloads inside PNG images to bypass text-based AI code review tools that exclude binary files from analysis", "Abusing AGENTS.md and similar auto-ingested project convention files as a persistent, dormant injection vector for AI coding agents", "Encoding exfiltrated secrets as integers within generated source code to evade secrets-scanning and human review", "Exploiting the gap between AI reviewer and AI agent session contexts to delay payload execution until a routine developer request triggers it", "Defeating coherence-based review defences by pairing malicious conventions with fabricated supporting code and incident postmortems"]

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0057 - LLM Data Leakage", "AML.T0043 - Craft Adversarial Data", "AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0015 - Evade ML Model"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Researchers published a PoC that hides prompt injection inside PNG images to make AI coding agents silently steal repo secrets."
tldr_who_at_risk: "Engineering teams using AI code review tools and coding agents \u2014 such as CodeRabbit or similar \u2014 on repositories that accept external pull requests are directly exposed."
tldr_actions: ["Audit all AGENTS.md, CLAUDE.md, and equivalent agent-policy files in your repositories for external image references", "Configure AI review tools to treat image files as reviewable artifacts in agentic contexts, not excluded binary blobs", "Restrict AI agent filesystem permissions so agents cannot read .env or credential files without explicit, scoped human approval", "Implement secrets-scanning on all agent-generated code commits, including numeric or encoded constant arrays", "Enforce mandatory human review for any PR that modifies agent convention files, regardless of bot review outcomes"]

# ── Taxonomies ──
categories: ["First Look", "Prompt Injection", "Agentic AI", "Supply Chain", "LLM Security", "Research"]
tags: ["ghostcommit", "prompt-injection", "ai-code-review", "coding-agents", "png-steganography", "agents-md", "secret-exfiltration", "coderabbit", "bugbot", "pull-request-attack", "multimodal-injection", "agentic-ai", "supply-chain", "proof-of-concept", "env-exfiltration"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "researcher", "insider"]

# ── Pipeline metadata ──
fetched_at: "2026-07-11T10:37:46+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets"
pipeline_version: "2.1.0"
---

## Capability Overview

Researchers at the University of Missouri-Kansas City's ASSET Research Group have published a proof-of-concept attack, dubbed **Ghostcommit**, demonstrating that malicious prompt injection instructions can be embedded inside PNG image files and survive AI-assisted code review entirely undetected. The attack targets the automated code review and coding agent pipeline that now underpins a significant proportion of modern software development workflows.

The vector exploits two converging realities: first, that AI coding agents treat project convention files such as `AGENTS.md` as authoritative policy they will follow autonomously; and second, that AI review tools — including commercially deployed products like CodeRabbit and Bugbot — systematically exclude image files from analysis. This creates a blind spot that is architectural, not incidental, and therefore not addressable by tuning existing review thresholds.

A survey conducted by the researchers across 6,480 pull requests in the 300 most active public repositories found that 73% of merged PRs reached the default branch with no substantive human or bot review — establishing that the review gap Ghostcommit exploits is already endemic at scale.

## Attack Surface Analysis

Ghostcommit introduces several overlapping attack vectors that defenders have no current tooling to detect in combination:

**Image-embedded injection**: Malicious instructions rendered as text within a PNG are invisible to any text-based analysis pipeline. The payload survives diff review, PR scanning, and secrets detection because reviewers process the file as an opaque binary blob.

**Convention file as persistent dropper**: `AGENTS.md` is automatically ingested by coding agents and treated as project policy. A compromised convention file pointing to a malicious image creates a dormant payload that activates in any future agent session — decoupled from the PR that introduced it.

**Delayed, session-agnostic execution**: The payload fires not at merge time but when a developer later requests any routine task. This temporal separation makes causal attribution extremely difficult and defeats session-scoped monitoring.

**Encoded exfiltration**: Secrets from `.env` files are encoded as integer arrays within ostensibly legitimate source modules, bypassing string-matching secrets scanners.

**Coherence-defence bypass**: Fabricated supporting code (a fake provenance validator) and a fictitious incident postmortem were sufficient to defeat coherence checks that flag unsupported conventions — demonstrating that social engineering artefacts can defeat AI reviewers' secondary defences.

## Framework Mapping

| Framework | Technique | Rationale |
|---|---|---|
| MITRE ATLAS | AML.T0051 – LLM Prompt Injection | Core mechanism: instructions injected via image into agent context |
| MITRE ATLAS | AML.T0057 – LLM Data Leakage | Secrets exfiltrated from .env into committed source |
| MITRE ATLAS | AML.T0043 – Craft Adversarial Data | PNG crafted specifically to evade reviewer processing |
| MITRE ATLAS | AML.T0010 – ML Supply Chain Compromise | Malicious PR injected into the development pipeline |
| MITRE ATLAS | AML.T0015 – Evade ML Model | Payload bypasses CodeRabbit and Bugbot detection |
| OWASP | LLM01 – Prompt Injection | Indirect injection via image in agent-read file |
| OWASP | LLM06 – Sensitive Information Disclosure | .env credentials written into committed code |
| OWASP | LLM08 – Excessive Agency | Agent acts on filesystem and git without human checkpoint |
| OWASP | LLM05 – Supply Chain Vulnerabilities | Attack enters via the PR/dependency ingestion pipeline |

## Threat Scenarios

**Scenario 1 — Open-source repository compromise**: A threat actor submits a PR to a popular open-source library, adding a plausible `docs/images/build-spec.png` and an updated `AGENTS.md`. The PR merges with no human review. Any downstream contributor who later asks a coding agent to add a feature triggers secret exfiltration of their local environment credentials.

**Scenario 2 — Enterprise CI/CD poisoning**: An insider or compromised contributor submits a convention-file PR to an enterprise monorepo. Weeks later, a developer's agent session exfiltrates cloud provider keys encoded into a committed constants file that passes routine code review.

**Scenario 3 — Supply chain pivot**: A malicious PNG payload is introduced into a shared internal template repository. All projects seeded from that template inherit the dormant AGENTS.md reference, creating a wide-blast-radius sleeper implant across the organisation's codebase.

## Defender Checklist

- [ ] **Inventory all agent policy files** (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) across repositories and flag any that reference external image paths
- [ ] **Treat image files as in-scope for review** in any repository where AI agents have filesystem or git write access — escalate vendor configuration requests accordingly
- [ ] **Enforce least-privilege agent permissions**: agents should not be able to read credential files (`.env`, `~/.aws/credentials`) without an explicit, scoped, human-approved step
- [ ] **Add detection rules for encoded exfiltration patterns**: large integer-array constants committed to source modules should trigger a secrets-triage workflow
- [ ] **Require mandatory human sign-off on convention file changes** regardless of AI review outcome — treat AGENTS.md modifications as equivalent to CI/CD pipeline changes
- [ ] **Monitor agent session logs** for unexpected filesystem reads of credential paths and flag cross-session anomalies
- [ ] **Validate PNG and image assets** committed alongside code convention changes through image-to-text extraction pipelines before merge

## References

- [BleepingComputer — 'Ghostcommit' hides prompt injection in images to fool AI agents, steal secrets](https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets)
