---
title: "First Look: Current AI Launches Open Source AI Gap Map Indexing 421 Projects"
date: "2026-07-04T08:53:39+00:00"
draft: false 
slug: "first-look-current-ai-launches-open-source-ai-gap-map-indexing-421-projects"

# ── Content metadata ──
summary: "Current AI has published the Open Source AI Gap Map v0.1, a structured, MIT-licensed index of 421 open-source AI products spanning models, datasets, software tools, and hardware, backed by 1,184 YAML files and tracking over 16,000 GitHub repositories. For defenders, this comprehensive public inventory creates a dual-use intelligence resource: while it aids supply chain visibility, it simultaneously provides adversaries with a curated, machine-readable attack surface map of the open-source AI ecosystem. Security teams should treat this dataset as threat-actor recon material and cross-reference their own AI dependencies against it immediately."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Jul/3/open-source-ai-gap-map"
source_title: "Open Source AI Gap Map"
source_date: 2026-07-03T22:04:31+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1774901128281-a884cd447af5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw3fHxzb2Z0d2FyZSUyMHJlbGVhc2UlMjBkb3dubG9hZCUyMHNlcnZlcnxlbnwwfDB8fHwxNzgzMTUyNTIyfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 5.2
adoption_velocity: "MODERATE"
capability_category: "open-source-release"
attack_vectors_introduced: ["Adversary reconnaissance acceleration: the structured YAML dataset gives threat actors a pre-built, categorised inventory of open-source AI components to target for supply chain compromise", "Dependency enumeration at scale: the 16,000+ tracked GitHub repositories can be mined to identify unmaintained or low-contributor projects ripe for takeover or typosquatting", "Dataset and model poisoning target identification: the 85 models and 50 datasets catalogued provide a prioritised list of high-impact upstream components where poisoning would propagate widely", "Gap exploitation: the explicit labelling of capability gaps signals to adversaries which areas lack mature security tooling or oversight, guiding offensive research investment"]

# ── AI Security Classification ──
relevance_score: 5.5
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0019 - Publish Poisoned Datasets", "AML.T0020 - Poison Training Data", "AML.T0044 - Full ML Model Access", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM03 - Training Data Poisoning", "LLM10 - Model Theft"]

# ── TL;DR ──
tldr_what: "Current AI released a structured, MIT-licensed index of 421 open-source AI products across models, datasets, tools, and hardware."
tldr_who_at_risk: "Organisations consuming open-source AI components are newly exposed if adversaries use this map to prioritise supply chain compromise targets."
tldr_actions: ["Cross-reference your AI dependency stack against the Gap Map's 16,000+ tracked repos to identify overlap with high-risk, low-maintainer projects", "Monitor the currentai-org/os-ai-map repository for changes that add or re-categorise components you depend on", "Treat the YAML dataset as adversary recon material and use it proactively to harden your most exposed upstream dependencies before attackers act on it"]

# ── Taxonomies ──
categories: ["First Look", "Supply Chain", "Research", "Industry News"]
tags: ["open-source-ai", "supply-chain", "gap-map", "current-ai", "inventory", "dataset-security", "model-registry", "recon", "osint", "yaml", "github", "datasette"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-07-04T08:08:42+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Jul/3/open-source-ai-gap-map"
pipeline_version: "2.1.0"
---

## Capability Overview

Current AI, a non-profit launched at the Paris AI Action Summit in February 2025 with $400 million in committed backing, has published the Open Source AI Gap Map v0.1. The release catalogues 421 open-source AI products — 266 software tools and libraries, 85 models, 50 datasets, and 20 hardware projects — produced by 228 organisations across 14 categories and three stack layers. The underlying data is MIT-licensed and published as 1,184 YAML files in the `currentai-org/os-ai-map` GitHub repository, with an accompanying CSV of 16,185 tracked GitHub repositories explorable via Datasette Lite.

For defenders, the significance is not the Gap Map's stated mission of cataloguing open-source AI for public benefit. It is that a well-funded, credible organisation has done the reconnaissance work for the entire ecosystem and published it freely.

## Attack Surface Analysis

The Gap Map converts what was previously fragmented, manual research into a structured, machine-readable, version-controlled inventory. This changes the threat landscape in several concrete ways:

**Adversary reconnaissance at scale.** Nation-state and cybercriminal actors who previously needed to independently enumerate the open-source AI supply chain now have a curated, scored, categorised starting point. The YAML schema imposes structure that makes automated analysis trivial — identifying low-maintainer projects, unmaintained datasets, or hardware with small contributor bases requires only basic scripting against the repo.

**Prioritised poisoning targets.** The 85 catalogued models and 50 datasets, particularly those rated as foundational or widely depended upon, represent a ranked list of upstream components where a successful poisoning or backdoor insertion would cascade downstream. The map's own scoring system inadvertently signals which targets yield the highest leverage.

**Gap signalling.** The project's explicit purpose is to identify capability gaps in open-source AI. For offensive researchers, a publicly published gap list is an investment thesis: these are the areas where security tooling is absent or immature, making exploitation less likely to be detected.

**Dependency graph exposure.** The 16,000+ tracked repositories include organisational attribution. Cross-referencing this with public contributor graphs enables targeted social engineering or credential compromise against maintainers of high-impact components.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The map directly accelerates the reconnaissance phase of supply chain attacks by enumerating components and their relative importance.
- **AML.T0019/T0020 (Publish Poisoned Datasets / Poison Training Data):** Catalogued datasets with clear upstream provenance are now easier to target; adversaries can identify which poisoned dataset would affect the most downstream models.
- **AML.T0044 (Full ML Model Access):** Models indexed with open weights and repository links reduce the effort required to study, clone, or backdoor them.
- **LLM05 (Supply Chain Vulnerabilities):** The map is a supply chain transparency tool that simultaneously functions as a supply chain attack surface enumeration tool.
- **LLM03 (Training Data Poisoning):** High-visibility datasets in the index become priority targets.

## Threat Scenarios

**Scenario 1 — Targeted repo takeover.** A threat actor queries the YAML dataset for models with fewer than three active contributors and high downstream citation counts. They identify two candidate repositories, initiate a maintainer impersonation campaign, and inject a backdoored model weight update.

**Scenario 2 — Dataset poisoning via gap exploitation.** The Gap Map flags a foundational multilingual dataset as having no security-focused maintainer. An adversary submits subtly poisoned samples through the dataset's open contribution pipeline, knowing audit tooling in this gap area is absent.

**Scenario 3 — Automated dependency enumeration for a targeted enterprise.** An attacker cross-references a target organisation's public GitHub repositories against the Gap Map's 16,000 tracked repos to build a precise map of which open-source AI components the organisation likely uses, then crafts a spearphishing campaign against the relevant maintainers.

## Defender Checklist

- [ ] Download the YAML dataset and cross-reference against your internal AI component inventory to identify overlapping dependencies
- [ ] Flag any dependencies scored as high-importance by the Gap Map for enhanced integrity monitoring (hash pinning, signed releases)
- [ ] Review contributor health of your top 10 open-source AI dependencies; apply heightened scrutiny to any with fewer than three active maintainers
- [ ] Subscribe to the `currentai-org/os-ai-map` repository to receive alerts when components you depend on are re-scored or re-categorised
- [ ] Use the dataset and model lists to scope your next AI supply chain risk assessment
- [ ] Share the gap list with your threat intelligence team as an indicator of where adversarial research investment is likely to flow

## References

- Simon Willison's Weblog: https://simonwillison.net/2026/Jul/3/open-source-ai-gap-map
- Current AI Gap Map GitHub: https://github.com/currentai-org/os-ai-map
- Datasette Lite exploration: linked via source article
