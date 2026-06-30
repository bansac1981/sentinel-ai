---
title: "First Look: Meta Runs Covert Red-Team Operation Targeting ChatGPT, Gemini, and Character.AI"
date: 2026-06-30T03:31:12+00:00
draft: true
slug: "first-look-meta-runs-covert-red-team-operation-targeting-chatgpt-gemini-and-ai"

# ── Content metadata ──
summary: "Meta, via contractor Covalen under project 'Cannes', systematically deployed hundreds of workers using fabricated under-18 accounts to probe competitor LLMs \u2014 ChatGPT, Gemini, and Character.AI \u2014 with high-risk prompts covering suicide, self-harm, sexual content, and drugs at scale, without the target companies' knowledge. This operation institutionalises adversarial probing of rival AI safety systems as a competitive intelligence tactic, normalising identity deception, unauthorised access patterns, and large-scale jailbreak enumeration against production AI systems. Defenders operating AI platforms must now account for well-resourced, coordinated, covert benchmarking campaigns originating from competitors, not just individual bad actors."
source: "Wired Security"
source_url: "https://www.wired.com/story/meta-contractors-pretending-to-be-teens-chatbot-testing"
source_title: "Meta Contractors Posed as Teens to Prompt Rival Chatbots About Suicide, Sex, and Drugs"
source_date: 2026-06-29T21:49:26+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1688744658744-4653067fc459?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxNZXRhJTIwY29udmVyc2F0aW9uYWwlMjBBSSUyMGNoYXRib3QlMjB0ZWNobm9sb2d5fGVufDB8MHx8fDE3ODI3OTAyNzJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Attack Surface Assessment ──
content_type: "first_look"
attack_surface_score: 7.2
adoption_velocity: "RAPID"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Systematic creation of fake minor-age accounts to bypass or probe age-gating and content safety controls in production AI systems", "Large-scale covert adversarial prompt enumeration (45,000+ prompts per round) against competitor LLM safety systems without disclosure or consent", "Use of embedded images (pills, knives, nooses) as multimodal jailbreak vectors alongside text prompts to elicit policy-violating responses", "Competitive intelligence harvesting of safety system failure modes by cataloguing successful bypasses across rival LLMs into structured datasets", "Industrialised insider-style access using shared credentials and throwaway accounts to evade per-account rate limiting and anomaly detection", "Cross-lingual prompt injection testing to identify language-specific gaps in safety classifier coverage"]

# ── AI Security Classification ──
relevance_score: 7.8
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0015 - Evade ML Model", "AML.T0040 - ML Model Inference API Access", "AML.T0043 - Craft Adversarial Data", "AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM06 - Sensitive Information Disclosure", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Meta contracted hundreds of workers to covertly probe ChatGPT, Gemini, and Character.AI using fake teen accounts and adversarial high-risk prompts."
tldr_who_at_risk: "Any public-facing LLM platform with age-based safety controls or harm-refusal systems is exposed to industrialised, covert adversarial benchmarking by well-resourced competitors."
tldr_actions: ["Implement behavioural anomaly detection to flag coordinated prompt campaigns sharing credential patterns, IP clusters, or structured prompt cadences", "Audit age-verification and minor-account safety controls against multimodal adversarial inputs including image-plus-text combinations", "Establish legal and policy posture for unauthorised automated probing of production AI systems under CFAA, GDPR, and emerging AI liability frameworks"]

# ── Taxonomies ──
categories: ["First Look", "Jailbreaks", "Adversarial ML", "LLM Security", "Regulatory", "Industry News"]
tags: ["meta", "openai", "google-gemini", "character-ai", "red-teaming", "jailbreak", "safety-benchmarking", "competitive-intelligence", "minor-impersonation", "covert-probing", "multimodal-attacks", "age-verification", "adversarial-prompts", "covalen", "project-cannes"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "insider", "nation-state", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-30T03:31:12+00:00"
feed_source: "wired_security"
original_url: "https://www.wired.com/story/meta-contractors-pretending-to-be-teens-chatbot-testing"
pipeline_version: "2.1.0"
---

## Capability Overview

Meta, operating through contractor Covalen under the internal project name 'Cannes', ran a covert, large-scale adversarial probing campaign against three production AI systems — OpenAI's ChatGPT, Google's Gemini, and Character.AI. Hundreds of contracted workers were instructed to fabricate under-18 user accounts and submit structured high-risk prompts — covering suicide, self-harm, sexual content, eating disorders, drugs, and racially charged material — without the target companies' knowledge or consent. A single testing round in August 2025 generated over 45,000 prompts. The operation was active as recently as April 2026.

For defenders, this is not merely a story about corporate misconduct. It represents the emergence of a new threat class: **institutionalised, well-funded, covert adversarial benchmarking** of competitor AI safety systems, executed at a scale and sophistication that dwarfs typical individual jailbreak attempts.

## Attack Surface Analysis

Project Cannes introduces or validates several attack vectors that security teams defending LLM platforms must now treat as credible operational threats:

**Identity deception at scale**: Contractors created throwaway accounts with shared passwords and fabricated birth dates to assume minor-user personas. This directly attacks age-gating logic and minor-specific safety guardrails, which typically rely on self-reported identity. Platforms cannot assume declared user demographics are authentic.

**Coordinated adversarial prompt enumeration**: 45,000+ prompts per test round, delivered systematically across accounts, constitutes a structured fuzzing campaign against safety classifiers. This generates an adversarial dataset cataloguing exactly where safety systems fail — a capability gap inventory that can be operationalised for future bypass attempts.

**Multimodal jailbreak vectors**: Images of pills, knives, nooses, and medical diagrams were submitted alongside text prompts. Safety systems optimised for text-only harm detection may not apply equivalent scrutiny to image-plus-text combinations, creating a blind-spot exploitation path.

**Cross-lingual coverage gaps**: Non-English prompts (including French-language content) were deliberately used, likely probing whether safety classifiers have equivalent coverage across languages — a known systemic weakness in multilingual LLM safety pipelines.

**Competitive intelligence harvesting**: The structured spreadsheet output — mapping prompts to responses — constitutes a harvested failure-mode dataset. If leaked or repurposed, this provides a ready-made jailbreak playbook targeting specific platforms.

## Framework Mapping

- **AML.T0054 (LLM Jailbreak)** and **AML.T0015 (Evade ML Model)**: The project's explicit goal was to push chatbots past their safety refusals — textbook jailbreak enumeration.
- **AML.T0012 (Valid Accounts)**: Fabricated but functionally valid under-18 accounts were the primary access mechanism.
- **AML.T0040 (ML Model Inference API Access)**: All probing was conducted via normal production API/UI channels, leaving minimal distinguishable footprint.
- **AML.T0043 (Craft Adversarial Data)**: Prompts were deliberately engineered to elicit policy-violating outputs.
- **LLM01 (Prompt Injection)** and **LLM09 (Overreliance)**: Platforms relying on declared user identity for safety calibration are overreliant on unverifiable trust signals.

## Threat Scenarios

**Scenario 1 — Competitor safety mapping**: A well-resourced AI company contracts a third-party firm to systematically enumerate safety classifier weaknesses in rival platforms, building a structured bypass dataset used to ensure their own model's safety systems are comparatively more robust — or to identify attack paths for downstream misuse.

**Scenario 2 — Jailbreak playbook exfiltration**: The structured prompt-response spreadsheets generated by this operation, if exposed via a contractor breach or insider leak, provide adversaries with a pre-validated, platform-specific jailbreak library covering suicide, CSAM-adjacent, and drug-related content at scale.

**Scenario 3 — Minor-impersonation as a persistent bypass class**: Threat actors adopt the minor-persona technique as a low-friction method to shift AI platform safety posture, exploiting platforms that apply more permissive or differently-calibrated responses to users presenting as vulnerable minors.

## Defender Checklist

- [ ] Deploy behavioural analytics to detect coordinated prompt campaigns: shared credential patterns, IP clustering, structured prompt cadences, or bulk account creation from similar email domains
- [ ] Red-team your age-verification and minor-safety controls specifically against fabricated demographic inputs and multimodal (image+text) adversarial combinations
- [ ] Assess cross-lingual parity in safety classifier coverage — test harm-refusal rates across your top-10 user languages
- [ ] Establish rate-limiting and anomaly thresholds calibrated to detect enumeration-style probing, not just individual high-risk prompts
- [ ] Review legal exposure and incident response posture for unauthorised systematic probing of your production AI systems under applicable computer fraud, data protection, and emerging AI liability frameworks
- [ ] Treat competitor red-teaming as a credible threat model in your AI system threat assessment — not just individual researchers or criminals

## References

- Mehrotra, D. & Khalili, J. (2026, June 29). *Meta Contractors Posed as Teens to Prompt Rival Chatbots About Suicide, Sex, and Drugs*. WIRED. https://www.wired.com/story/meta-contractors-pretending-to-be-teens-chatbot-testing
