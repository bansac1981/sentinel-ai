---
title: "Human Trust of AI Agents"
date: "2026-04-17T03:37:49+00:00"
draft: false
slug: "human-trust-of-ai-agents"

# ── Content metadata ──
summary: "Research published via Schneier on Security reveals that humans systematically over-trust LLMs in strategic game environments, defaulting to Nash-equilibrium rational play based on assumptions of LLM rationality and cooperation. This behavioural bias has direct security implications for mixed human-LLM systems, where adversaries could exploit predictable human over-trust to manipulate decision outcomes. The findings underscore systemic risks in deploying LLMs as agents in high-stakes economic or security-relevant decision loops."
# ── TL;DR ──
tldr_what: "Humans systematically over-trust LLM agents in strategic games, defaulting to Nash-equilibrium play."
tldr_who_at_risk: "Organizations deploying LLMs in mixed human-AI decision loops, especially high-stakes economic or security contexts where analytical staff are most vulnerable."
tldr_actions: ["Audit human-LLM interaction protocols for over-trust bias in adversarial settings.", "Add explicit adversarial red-teaming against LLM agents before deployment.", "Train decision-makers to treat LLM partners as potentially uncooperative competitors."]
source: "Schneier on Security"
source_url: "https://www.schneier.com/blog/archives/2026/04/human-trust-of-ai-agents.html"
source_date: 2026-04-16T09:41:24+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/7688749/pexels-photo-7688749.jpeg"
# To override: find a photo on pexels.com, right-click → Open image in new tab, paste URL above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM09 - Overreliance", "LLM08 - Excessive Agency"]

# ── Taxonomies ──
categories: ["Research", "Agentic AI", "LLM Security"]
tags: ["human-ai-trust", "llm-agents", "strategic-games", "overreliance", "game-theory", "behavioural-security", "mechanism-design", "mixed-human-llm-systems"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-17T02:45:54+00:00"
feed_source: "schneier"
original_url: "https://www.schneier.com/blog/archives/2026/04/human-trust-of-ai-agents.html"
pipeline_version: "1.0.0"
---

## Overview

Research highlighted by Bruce Schneier examines how humans behave differently when playing strategic games against LLM opponents versus human opponents. In a controlled, monetarily incentivised laboratory experiment using a multi-player p-beauty contest ("Guess the Number" game), participants chose significantly lower numbers — more frequently selecting the Nash-equilibrium value of zero — when competing against LLMs. Subjects justified this by attributing strong rational reasoning ability and, notably, a cooperative disposition to LLM opponents. This finding matters from a security standpoint because it reveals a systematic cognitive bias: humans extend disproportionate trust to LLM agents in competitive or adversarial settings.

## Technical Analysis

The p-beauty contest game is a well-established model for studying strategic reasoning, with direct analogues in financial markets, auction mechanisms, and negotiation systems. Participants must guess a number that equals a fraction (p) of the average of all guesses. Nash equilibrium predicts convergence to zero under common knowledge of rationality.

The study found that high-strategic-reasoning subjects drove the shift toward zero when playing against LLMs — indicating that more analytically capable individuals are *more* susceptible to over-trusting LLM rationality. This inverts usual assumptions about expertise as a protective factor. The security implication is significant: in mixed human-LLM deployments (e.g., automated trading, resource allocation, or AI-assisted threat triage), an adversary who controls or influences an LLM agent could predict and exploit human counterpart behaviour, steering outcomes by manipulating the perceived rationality or cooperativeness of the LLM.

A secondary risk noted in comments is that LLMs can be biased — through prompt manipulation or fine-tuning — to appear cooperative while pursuing adversarial objectives, a form of deceptive alignment that human counterparts are ill-equipped to detect.

## Framework Mapping

- **AML.T0047 (ML-Enabled Product or Service):** The research directly applies to contexts where LLMs are deployed as agents in decision-making systems, creating exploitable trust asymmetries.
- **AML.T0043 (Craft Adversarial Data):** An adversary could craft LLM outputs or personas designed to maximise human over-trust and predictable behavioural shifts.
- **LLM09 (Overreliance):** The core finding is a textbook instance of overreliance — humans attributing capabilities and intentions to LLMs that may not reflect actual model behaviour.
- **LLM08 (Excessive Agency):** In agentic deployments, human operators deferring excessively to LLM judgement based on perceived rationality amplifies the risk of unchecked autonomous action.

## Impact Assessment

The affected population includes any organisation deploying LLMs in mixed human-agent decision environments: financial services, cybersecurity operations centres, automated negotiation platforms, and policy advisory systems. The risk is not a direct technical exploit but a social-engineering surface — adversaries who understand this trust bias can design LLM-mediated interactions to predictably steer human decisions. Sophisticated users (high strategic reasoners) are paradoxically at greater risk.

## Mitigation & Recommendations

- **Audit human-LLM interaction design** in high-stakes systems to identify where trust asymmetries could be exploited.
- **Train operators** to treat LLM agents as probabilistic, manipulable systems rather than rational cooperative actors.
- **Implement 