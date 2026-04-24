---
title: "Claude's Mythos rival: Chinese Cybersecurity Firm\u2019s claims finding 1000 vulnerabilities"
date: 2026-04-24T02:41:25+00:00
draft: false
slug: "chinese-cybersecurity-firms-ai-hacking-claims-draw-comparisons-to-claude-mythos"

# ── Content metadata ──
summary: "Chinese cybersecurity firm 360 Digital Security Group claims its multi-agent AI system autonomously discovered nearly 1,000 vulnerabilities, including a critical Office zero-day allegedly dormant for eight years, drawing direct comparisons to Anthropic's restricted Claude Mythos model. The developments signal that AI-driven autonomous vulnerability discovery is rapidly proliferating beyond tightly controlled Western research environments. This raises significant concerns about AI-accelerated offensive capabilities reaching nation-state threat actors at scale."
source: "SecurityWeek"
source_url: "https://www.securityweek.com/chinese-cybersecurity-firms-ai-hacking-claims-draw-comparisons-to-claude-mythos/"
source_date: 2026-04-23T12:36:45+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/30530406/pexels-photo-30530406.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 8.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Chinese firm 360 claims AI multi-agent system autonomously found ~1,000 vulns, rivalling Anthropic's Mythos."
tldr_who_at_risk: "Vendors and defenders of Windows, Office, Android, and IoT products face accelerated zero-day exposure from AI-driven offensive tooling."
tldr_actions: ["Accelerate patch cadence for Windows, Office, and Android given AI-assisted discovery compresses zero-day windows", "Monitor for CVE-2026-32190 and CVE-2026-24293 advisories and apply mitigations immediately upon release", "Invest in AI-assisted defensive vulnerability research to match pace of adversarial autonomous discovery"]

# ── Taxonomies ──
categories: ["Agentic AI", "Research", "Industry News", "LLM Security"]
tags: ["autonomous-vulnerability-discovery", "ai-hacking", "multi-agent-systems", "nation-state", "zero-day", "china", "qihoo-360", "claude-mythos", "tianfu-cup", "offensive-ai", "agentic-ai"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-24T02:41:25+00:00"
feed_source: "securityweek"
original_url: "https://www.securityweek.com/chinese-cybersecurity-firms-ai-hacking-claims-draw-comparisons-to-claude-mythos/"
pipeline_version: "1.0.0"
---

## Overview

A Chinese cybersecurity firm, 360 Digital Security Group (part of Qihoo 360), has made notable claims about an internally developed 'Multi-Agent Collaborative Vulnerability Discovery System' capable of autonomously identifying vulnerabilities at scale. According to analysis by ETH Zurich researcher Eugenio Benincasa on the Natto Thoughts blog, 360's system reportedly contributed to roughly half of the vulnerabilities identified during its first-place finish at the revived Tianfu Cup hacking competition, totalling close to 1,000 vulnerabilities. The most striking claim involves CVE-2026-32190, a critical Microsoft Office flaw allegedly identified by the AI agent within minutes despite reportedly going undetected for approximately eight years.

These claims arrive in the immediate wake of Anthropic's closely controlled unveiling of Claude Mythos, a frontier model described as capable of autonomously discovering thousands of vulnerabilities. Mythos is restricted to a few dozen vetted organisations via Project Glasswing. Anthropic's own CEO has acknowledged that open-source models and Chinese developers could replicate Mythos-level performance within 6–12 months — a timeline that 360's announcements suggest may already be compressing.

## Technical Analysis

360's 'Multi-Agent Collaborative Vulnerability Discovery System' appears to employ coordinated autonomous agents tasked with vulnerability discovery across diverse attack surfaces including Windows kernel internals, Microsoft Office document processing, Android system components, and IoT firmware. The multi-agent architecture is consistent with emerging offensive AI patterns where specialised sub-agents handle reconnaissance, fuzzing, triage, and exploit validation in parallel pipelines.

CVE-2026-32190 (critical Office RCE) and CVE-2026-24293 (Windows kernel) represent the highest-severity disclosures attributed to the system. The claim that CVE-2026-32190 evaded detection for ~8 years underscores a key threat: AI agents may be systematically mining long-tailed vulnerability spaces that manual and traditional automated testing has failed to saturate.

The competitive context of Tianfu Cup — a state-adjacent hacking contest — adds geopolitical weight to the technical claims, as findings from such events have historically fed into broader offensive capability pipelines.

## Framework Mapping

- **AML.T0047 (ML-Enabled Product or Service):** 360's system is a purpose-built offensive ML product that operationalises AI for adversarial vulnerability research.
- **AML.T0040 (ML Model Inference API Access):** Multi-agent architectures rely on repeated model inference across vulnerability discovery workflows, expanding the attack surface for misuse.
- **AML.T0043 (Craft Adversarial Data):** Agent-generated exploit payloads are a natural downstream output of autonomous vulnerability discovery systems.
- **LLM08 (Excessive Agency):** Autonomous agents executing exploit discovery and validation with minimal human oversight exemplify the excessive agency risk category.

## Impact Assessment

The primary risk is acceleration of the offensive vulnerability lifecycle. If AI systems can autonomously discover critical zero-days in widely deployed software (Windows, Office, Android) in minutes rather than months, the window between vulnerability introduction and discovery by defenders collapses dramatically. This asymmetrically benefits well-resourced offensive actors. Nation-state-adjacent firms like 360 operating within a competitive state intelligence ecosystem amplify strategic risk beyond typical cybercriminal threat models.

## Mitigation & Recommendations

1. **Patch prioritisation:** Treat CVE-2026-32190 and CVE-2026-24293 as high-urgency; monitor MSRC advisories closely.
2. **Defensive AI parity:** Security teams should deploy AI-assisted fuzzing and static analysis tooling to narrow the discovery gap with offensive actors.
3. **Threat intelligence monitoring:** Track 360 Digital Security Group disclosures and Tianfu Cup outputs as leading indicators of adversarial AI capability maturation.
4. **Supply chain vigilance:** IoT and embedded device manufacturers should assume AI-driven fuzzing will surface previously unknown firmware vulnerabilities.
5. **Policy engagement:** Organisations with government relationships should advocate for clearer norms around state-adjacent AI offensive research disclosures.

## References

- [SecurityWeek: Chinese Cybersecurity Firm's AI Hacking Claims Draw Comparisons to Claude Mythos](https://www.securityweek.com/chinese-cybersecurity-firms-ai-hacking-claims-draw-comparisons-to-claude-mythos/)
- Natto Thoughts blog — Eugenio Benincasa, ETH Zurich
