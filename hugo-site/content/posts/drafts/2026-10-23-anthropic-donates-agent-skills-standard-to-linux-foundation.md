---
title: "Anthropic Donates Agent Skills Standard to Linux Foundation"
date: 2026-10-23T10:22:30+00:00
draft: true
slug: "anthropic-donates-agent-skills-standard-to-linux-foundation"

# ── Content metadata ──
summary: "Anthropic has donated its Agent Skills standard to the Agentic AI Foundation (AAIF) under the Linux Foundation, following its earlier donation of the Model Context Protocol (MCP) to the same body. For defenders, open governance of agentic interoperability standards reduces the risk of proprietary lock-in and creates a community-accountable path for embedding security requirements directly into how agents discover and invoke capabilities. Residual gaps remain around whether security controls and audit requirements will be formally incorporated into the standard's governance process, and how quickly enterprise tooling will mature to enforce those requirements at runtime."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Oct/22/donating-agent-skills"
source_title: "Donating Agent Skills to the Agentic AI Foundation"
source_date: 2026-10-22T18:09:56+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1599727277757-3f54e54ea618?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxMHx8QW50aHJvcGljJTIwbGFib3JhdG9yeSUyMHNjaWVuY2UlMjBkaXNjb3Zlcnl8ZW58MHwwfHx8MTc5Mjc1MDk1MHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 4.5
adoption_velocity: "MODERATE"
capability_category: "collective-defense"
attack_vectors_introduced: ["Open, vendor-neutral governance of Agent Skills creates a community process through which security requirements — such as capability scoping, permission declaration, and audit logging — can be formally proposed and standardised across all compliant implementations", "Standardisation under the Linux Foundation enables security-focused organisations and researchers to participate in shaping the specification, reducing the likelihood that security considerations are treated as vendor-specific afterthoughts", "Alignment of Agent Skills with MCP under a single foundation (AAIF) creates a coherent surface for defenders to monitor, audit, and apply consistent controls across agentic tool invocation and skill execution"]

# ── AI Security Classification ──
relevance_score: 5.5
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0081 - Modify AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0110 - AI Agent Tool Poisoning"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Anthropic donated its Agent Skills standard to the Agentic AI Foundation under the Linux Foundation."
tldr_who_at_risk: "Security and platform teams building or governing agentic AI pipelines benefit from a vendor-neutral standard that creates a common baseline for skill interoperability and community-accountable security requirements."
tldr_actions: ["Track the AAIF Agent Skills specification repository and engage in public comment periods to advocate for security and audit requirements", "Map your existing agentic tooling against the Agent Skills and MCP specifications to identify where proprietary assumptions may need to be refactored for standard compliance", "Align internal agent governance policies to the AAIF framework now, so security controls can be updated incrementally as the standard matures rather than retrofitted later"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "Supply Chain", "Industry News"]
tags: ["agent-skills", "agentic-ai-foundation", "linux-foundation", "anthropic", "model-context-protocol", "open-standards", "agentic-interoperability", "vendor-neutral", "mcp", "aaif"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "insider", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-10-23T10:22:30+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Oct/22/donating-agent-skills"
pipeline_version: "2.1.0"
---

## Defender Impact
The donation of the Agent Skills standard to the Agentic AI Foundation (AAIF) under the Linux Foundation moves a critical agentic interoperability layer out of single-vendor control and into open, community-accountable governance. For defenders, this creates a formal channel to embed security requirements — permission scoping, capability declaration, audit logging — directly into the specification that governs how AI agents discover and invoke skills across platforms.

## Capability Overview
Anthropic has donated its Agent Skills standard to the AAIF, the same foundation that now stewards the Model Context Protocol (MCP). The AAIF was co-founded by Anthropic, Block, and OpenAI under the Linux Foundation. Agent Skills define how AI agents advertise, discover, and invoke discrete capabilities — effectively the vocabulary through which agentic systems compose behaviour from modular components.

By consolidating both MCP (the transport and tool-invocation layer) and Agent Skills (the capability description and discovery layer) under a single foundation, AAIF now governs the two interlocking standards most likely to define how production agentic systems are built over the next several years. This matters for defenders because fragmented, proprietary standards make it nearly impossible to apply consistent security controls across a heterogeneous agentic environment. A unified, open standard creates a single surface against which policy, monitoring, and enforcement tooling can be built.

The Linux Foundation's governance model requires open participation, versioned specifications, and public review cycles — all of which create entry points for security-focused contributors to influence the standard before implementations proliferate.

## Defensive Advances
**Community-accountable security input.** Open governance means security researchers, enterprise defenders, and standards bodies can formally propose and vote on security requirements — capability permission declarations, invocation audit trails, and scope-limiting constraints — rather than waiting for a vendor to prioritise them.

**Reduced supply chain fragmentation.** With both MCP and Agent Skills under AAIF, defenders can focus monitoring and control tooling on a single, coherent standard rather than maintaining parallel stacks for competing proprietary protocols. This directly reduces the surface area relevant to AML.T0010 (AI Supply Chain Compromise) and AML.T0110 (AI Agent Tool Poisoning).

**Interoperability as a security baseline.** Standardisation creates the precondition for interoperable security tooling — runtime enforcers, capability scanners, and permission auditors — that can work across any compliant implementation regardless of vendor.

## Residual Gaps
The donation itself is a governance event, not a technical security control. The standard does not yet formally mandate security requirements such as capability permission declarations, least-privilege invocation, or audit logging — these remain aspirational unless explicitly incorporated into future specification versions through the community process.

Adoption maturity is uneven. Many existing agentic frameworks have built against earlier, pre-donation drafts of Agent Skills or proprietary equivalents. Converging on the AAIF-governed version will require migration work that not all teams will prioritise quickly.

Enforcement tooling does not yet exist at scale. Even a well-designed open standard only delivers security value when runtime enforcement, compliance scanning, and policy-as-code tooling mature around it. That ecosystem is nascent.

## Framework Mapping
- **AML.T0010 (AI Supply Chain Compromise)** and **AML.T0110 (AI Agent Tool Poisoning)**: Open governance reduces the risk that malicious or negligent changes to skill definitions propagate without community scrutiny.
- **AML.T0081 (Modify AI Agent Configuration)** and **AML.T0084 (Discover AI Agent Configuration)**: Standardised skill declarations create a consistent structure that monitoring tools can parse and alert on when unexpected modifications occur.
- **LLM05 (Supply Chain Vulnerabilities)** and **LLM08 (Excessive Agency)**: A community-governed standard creates the foundation for formally scoping what skills agents are permitted to invoke and under what conditions.

## Deployment Considerations
Organisations should treat this governance transition as an opportunity to audit their current agentic skill implementations against the AAIF specification. Teams that engage now — through public comment periods and working groups — will be better positioned to influence security requirements before the standard hardens. Complement standard adoption with runtime monitoring (aligned with the Teleport-style ephemeral trusted runtime model referenced in the source) to enforce least-privilege constraints on skill invocation until enforcement tooling matures.

## Defender Checklist
- [ ] Subscribe to AAIF mailing lists and specification repositories for Agent Skills and MCP
- [ ] Audit existing agentic skill implementations for alignment with the current AAIF draft specification
- [ ] Nominate security-focused representatives to participate in AAIF working groups and public comment periods
- [ ] Map internal agent governance policies to AAIF framework terminology to simplify future compliance alignment
- [ ] Evaluate runtime monitoring tooling that can enforce capability and permission constraints at the skill invocation layer

## References
- [Donating Agent Skills to the Agentic AI Foundation — Simon Willison](https://simonwillison.net/2026/Oct/22/donating-agent-skills)
