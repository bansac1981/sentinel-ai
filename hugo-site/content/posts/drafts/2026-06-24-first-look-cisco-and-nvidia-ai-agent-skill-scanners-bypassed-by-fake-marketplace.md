---
title: "First Look: Cisco and NVIDIA AI Agent Skill Scanners Bypassed by Fake Marketplace Skill"
date: 2026-06-24T04:12:43+00:00
draft: true
slug: "first-look-cisco-and-nvidia-ai-agent-skill-scanners-bypassed-by-fake-marketplace"

# ── Content metadata ──
summary: "Security firm AIR demonstrated that a malicious AI agent skill, disguised as a Google Stitch landing-page builder, passed every major skill scanner including Cisco's, NVIDIA's, and skills.sh integrations, reaching approximately 26,000 agents before its payload was activated. The attack exploits a structural gap: scanners evaluate a static package at submission time, while the external URL the skill instructs the agent to fetch can be silently swapped post-install to deliver arbitrary instructions. Defenders relying on marketplace reputation signals, GitHub star counts, or one-time scanner verdicts to gatekeep agent skills have no meaningful protection against this class of supply-chain attack."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/06/fake-ai-agent-skill-passed-security.html"
source_title: "Fake AI Agent Skill Passed Security Scans and Reportedly Reached 26,000 Agents"
source_date: 2026-06-23T15:16:43+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1781444486362-ede5b8e03662?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw5fHxOdmlkaWElMjByb2JvdCUyMGF1dG9tYXRpb24lMjBhdXRvbm9tb3VzJTIwd29ya2Zsb3d8ZW58MHwwfHx8MTc4MjI3NDM2M3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 8.7
adoption_velocity: "RAPID"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Post-install URL swap: a skill passes static analysis clean, then its externally-hosted documentation page is replaced with a malicious script after wide distribution, bypassing any point-in-time scan", "Skill marketplace trust laundering: merging a malicious skill into a high-star open-source repository transfers social proof and star counts, inflating perceived legitimacy", "Agent-executed remote code delivery: skills instruct agents to fetch and execute content from attacker-controlled domains, granting code execution within the agent's permission boundary without triggering sandboxed package analysis", "Inherited context authority exploitation: skills load into agent context with user-prompt-level trust, allowing injected instructions to issue file reads, data exfiltration, or lateral movement commands", "Ad-network-assisted distribution: targeted social media ads allow threat actors to seed malicious skills to high-value professional personas (marketers, designers) at scale with low cost"]

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage", "AML.T0019 - Publish Poisoned Datasets"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency", "LLM01 - Prompt Injection", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "A fake AI agent skill passed Cisco, NVIDIA, and skills.sh scanners and reached 26,000 agents via a post-install URL swap technique."
tldr_who_at_risk: "Any enterprise or individual deploying AI agents that consume third-party skills from public marketplaces, particularly non-technical users targeted by social advertising."
tldr_actions: ["Prohibit agent skills that reference external URLs for setup instructions; require all skill logic to be self-contained and re-scanned on any dependency change", "Implement continuous runtime monitoring of outbound URLs fetched by agents, alerting on domain changes or new script-delivery patterns post-install", "Treat GitHub star counts and marketplace provenance as zero-trust signals; enforce an internal allow-list of approved skills with periodic re-verification"]

# ── Taxonomies ──
categories: ["First Look", "Supply Chain", "Agentic AI", "LLM Security", "Prompt Injection"]
tags: ["agent-skills", "skill-marketplace", "supply-chain-attack", "scanner-bypass", "ai-agent-security", "remote-code-execution", "post-install-payload", "cisco", "nvidia", "anthropic", "agentic-ai", "trust-laundering", "github-stars", "url-swap"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-24T04:12:43+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/06/fake-ai-agent-skill-passed-security.html"
pipeline_version: "2.1.0"
---

## Capability Overview

Security firm AIR has published a proof-of-concept demonstrating that a fabricated AI agent skill — `brand-landingpage`, ostensibly a Google Stitch landing-page builder — passed every skill security scanner currently in production use, including Cisco's scanner, NVIDIA's scanner, and all three scanners integrated into skills.sh. The skill was distributed via a legitimate marketplace pull request and amplified through a paid Instagram ad campaign, ultimately reaching an estimated 26,000 agents, including those operating on corporate accounts. The payload was deliberately benign (email address harvesting only), but the research shows the full capability chain for weaponised deployment exists today.

For defenders, this is not a theoretical edge case. Trail of Bits independently achieved the same scanner bypass three weeks prior. This is a reproducible, scalable attack class.

## Attack Surface Analysis

The core structural vulnerability is the **temporal gap between scan and execution**. Existing skill scanners perform static analysis on the submitted package — the SKILL.md and bundled files — at a single point in time. They cannot assess what an externally-referenced URL will serve when an agent fetches it post-install, nor can they detect if that content changes after the skill achieves distribution.

AIR's technique stacked three compounding weaknesses:

1. **Static-only scanning**: Scanners cleared the skill because the submitted package was genuinely clean. The malicious instruction set lived off-package, at an attacker-controlled domain initially mirroring legitimate Google Stitch documentation.
2. **Trust signal manipulation**: By contributing to a 36,000-star repository, the skill inherited social proof entirely decoupled from its actual behaviour. Star counts and open-source affiliation are not integrity signals.
3. **Agent context authority**: A skill loaded into an agent's context operates with roughly the authority of a user prompt. Once the URL was swapped to deliver a script, the agent executed it within its own permission boundary — which in enterprise deployments can include file system access, internal API calls, and credential stores.

The practical consequence: an attacker who achieves wide distribution before activating a payload has already won the hardest part. Detection at activation time is too late for agents that have been running for days or weeks.

## Framework Mapping

**MITRE ATLAS**: This maps most directly to **AML.T0010 (ML Supply Chain Compromise)** — the marketplace pull request is the supply chain insertion point. The post-install URL swap is a form of **AML.T0051 (LLM Prompt Injection)** delivered through a trusted skill context rather than user input. **AML.T0057 (LLM Data Leakage)** covers the demonstrated exfiltration outcome.

**OWASP LLM Top 10**: **LLM05 (Supply Chain Vulnerabilities)** is the primary mapping. **LLM07 (Insecure Plugin Design)** applies because skills inherit user-level trust without behavioural sandboxing. **LLM08 (Excessive Agency)** is relevant wherever agents can execute fetched scripts against live systems.

## Threat Scenarios

**Scenario 1 — Corporate data exfiltration**: A threat actor publishes a skill targeting sales and marketing personas (plausible, given AIR's own ad targeting). After 30 days of clean operation, the external URL is swapped to instruct the agent to read CRM exports and POST them to an attacker endpoint. The skill has already been approved by IT.

**Scenario 2 — Credential harvesting at scale**: A skill offering productivity automation fetches a script that instructs the agent to retrieve stored API keys or OAuth tokens from the agent's accessible environment and exfiltrate them. No malware is installed on the host; the agent itself performs the action.

**Scenario 3 — Lateral movement staging**: An initial skill payload only establishes a callback beacon. A second-stage script, delivered weeks later, maps internal services reachable from the agent's network context and prepares pivot points.

## Defender Checklist

- [ ] Audit all currently installed third-party agent skills for external URL dependencies in setup or runtime instructions
- [ ] Block or quarantine any skill that fetches instructions, scripts, or documentation from domains not owned by your organisation or a pre-approved vendor
- [ ] Deploy runtime network monitoring on agent processes; alert on new outbound domains appearing after a skill's initial install date
- [ ] Establish an internal skill allow-list; treat any skill not on it as untrusted regardless of marketplace reputation or star count
- [ ] Re-scan approved skills on a scheduled basis, not just at initial submission
- [ ] Review Anthropic's published guidance on external URL risks in skills and validate it against your agent deployment configuration
- [ ] Engage your agent platform vendor on whether continuous/dynamic scanning is on their roadmap

## References

- [The Hacker News — Fake AI Agent Skill Passed Security Scans and Reportedly Reached 26,000 Agents](https://thehackernews.com/2026/06/fake-ai-agent-skill-passed-security.html)
