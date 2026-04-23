---
title: "Cybersecurity Looks Like Proof of Work Now"
date: 2026-04-23T04:04:57+00:00
draft: true
slug: "cybersecurity-looks-like-proof-of-work-now"

# ── Content metadata ──
summary: "Simon Willison highlights a UK AI Safety Institute evaluation confirming that Claude Mythos Preview is highly effective at discovering security vulnerabilities, with effectiveness scaling linearly with token spend. This creates a new security economics paradigm where defenders and attackers are engaged in a token-expenditure arms race. A notable defensive corollary is that open-source libraries gain renewed strategic value, as the cost of AI-assisted security audits can be amortised across all users."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Apr/14/cybersecurity-proof-of-work/#atom-everything"
source_date: 2026-04-14T19:41:48+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/5380655/pexels-photo-5380655.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0040 - ML Model Inference API Access", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM09 - Overreliance", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Claude Mythos finds more vulnerabilities the more tokens you spend, turning cybersecurity into an economic arms race."
tldr_who_at_risk: "Any organisation deploying software without AI-assisted security reviews is at risk, as well-funded attackers can now out-spend defenders on exploit discovery."
tldr_actions: ["Integrate AI-assisted vulnerability scanning (e.g., large frontier models) into your SDLC before deployment", "Prioritise budget allocation for AI security reviews proportional to your threat model and attacker resources", "Favour audited open-source dependencies over custom vibe-coded replacements to share the cost of AI security reviews"]

# ── Taxonomies ──
categories: ["LLM Security", "Research", "Industry News", "Agentic AI"]
tags: ["claude-mythos", "vulnerability-discovery", "ai-assisted-pentesting", "security-economics", "token-spend", "open-source-security", "aisi", "anthropic", "proof-of-work", "vibe-coding"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "nation-state", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-04-23T04:04:57+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Apr/14/cybersecurity-proof-of-work/#atom-everything"
pipeline_version: "1.0.0"
---

## Overview

A post by Simon Willison draws attention to the UK AI Safety Institute's (AISI) independent evaluation of Anthropic's Claude Mythos Preview model, which confirms that the system is exceptionally capable at identifying software security vulnerabilities. Crucially, the AISI report demonstrates a near-linear relationship between token expenditure and exploit discovery: the more compute (and therefore money) is spent querying the model, the more vulnerabilities it surfaces. This transforms cybersecurity into what commentator Drew Breunig terms a "proof of work" problem — a spending race between defenders and attackers.

## Technical Analysis

The core finding is that Claude Mythos operates as a highly capable automated penetration tester, able to identify exploitable vulnerabilities across codebases when given sufficient inference budget. The relationship between token spend and vulnerability discovery means that:

- **Attackers** with sufficient resources can continuously probe targets until exploitable paths are found.
- **Defenders** must out-spend or at least match that expenditure to discover and patch vulnerabilities first.

This is structurally analogous to Bitcoin's proof-of-work consensus: security is not a binary property but a function of relative economic investment. Unlike traditional static analysis, the model's effectiveness scales dynamically, suggesting that sufficiently funded adversaries — nation-states, well-capitalised cybercriminal groups — hold a structural advantage unless defenders invest equivalently.

A secondary implication concerns the trend of "vibe-coding" custom replacements for open-source libraries. If AI security auditing costs scale with codebase novelty, replacing a well-audited open-source library with a bespoke alternative dramatically increases the token cost required to achieve equivalent security assurance.

## Framework Mapping

- **AML.T0040 (ML Model Inference API Access):** Attackers leverage frontier model APIs to automate exploit discovery at scale.
- **AML.T0047 (ML-Enabled Product or Service):** Claude Mythos is itself an ML-enabled service repurposed for offensive security research.
- **LLM09 (Overreliance):** Defenders who assume existing static tooling is sufficient without AI-augmented review are overrelying on inadequate methods.
- **LLM05 (Supply Chain Vulnerabilities):** The open-source supply chain becomes both a risk vector and a defensive leverage point depending on audit investment.

## Impact Assessment

- **High-value software targets** (critical infrastructure, financial systems, SaaS platforms) face elevated risk from well-funded adversaries who can deploy sustained AI-assisted exploit campaigns.
- **Small and mid-size organisations** lacking budget for equivalent AI security reviews face a widening capability gap.
- **Open-source maintainers** gain renewed strategic importance, as community-funded AI audits provide shared defensive value.
- **Vibe-coded or rapidly assembled codebases** are disproportionately exposed, lacking the audit history and community scrutiny of mature open-source alternatives.

## Mitigation & Recommendations

1. **Adopt AI-assisted code review** using frontier models as part of CI/CD pipelines, not as a one-time audit but as continuous review.
2. **Model your threat actor's budget**: if you are a high-value target, assume adversaries can spend significantly on token-based exploit discovery.
3. **Leverage open-source ecosystems** where community investment in AI auditing is pooled, reducing per-organisation cost.
4. **Avoid unnecessary codebase sprawl**: custom components that deviate from audited libraries increase your attack surface and audit cost simultaneously.
5. **Engage with AISI and NIST guidance** on AI-augmented vulnerability discovery as frameworks mature.

## References

- [Simon Willison — Cybersecurity Looks Like Proof of Work Now](https://simonwillison.net/2026/Apr/14/cybersecurity-proof-of-work/#atom-everything)
- UK AI Safety Institute: Evaluation of Claude Mythos Preview's Cyber Capabilities (referenced in article)
