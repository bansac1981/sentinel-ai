---
title: "OpenAI Training Opt-Out Setting Silently Re-Enabled for Users"
date: "2026-09-15T13:32:58+00:00"
draft: false 
slug: "openai-training-opt-out-setting-silently-re-enabled-for-users"

# ── Content metadata ──
summary: "Multiple users report that OpenAI's 'allow training' opt-out setting is being silently re-enabled after they deliberately disabled it, raising serious concerns about data governance and user consent. A similar pattern has been observed on Anthropic's Claude platform, suggesting this may be a broader industry practice tied to TOS updates or subscription renewals. The behaviour undermines the integrity of privacy controls and means sensitive user conversations may be incorporated into training datasets without genuine informed consent."
source: "OpenAI (via HN)"
source_url: "https://news.ycombinator.com/item?id=49643556"
source_title: "Tell HN: OpenAI keeps re-enabling the 'allow training' setting"
source_date: 2026-09-10T13:39:53+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1782511742843-1b901be04a3a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxPcGVuYWklMjBkaWFsb2d1ZSUyMG1lZXRpbmclMjBwZW9wbGUlMjB0YWxraW5nfGVufDB8MHx8fDE3ODkzODM1MTJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0020 - Poison Training Data", "AML.T0059 - Erode Dataset Integrity", "AML.T0018 - Manipulate AI Model"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM03 - Training Data Poisoning", "LLM06 - Sensitive Information Disclosure"]

# ── TL;DR ──
tldr_what: "OpenAI's training opt-out setting silently reverts to enabled, exposing user conversations to model training."
tldr_who_at_risk: "All OpenAI and Claude subscribers who believed their data was excluded from training are at risk, particularly those handling sensitive or proprietary information."
tldr_actions: ["Immediately audit your OpenAI and Claude privacy settings and re-disable the training data opt-in", "Document the current state of your settings with timestamped screenshots for audit purposes", "Avoid sharing sensitive, confidential, or proprietary information in LLM chat sessions until verified opt-out persistence is confirmed"]

# ── Taxonomies ──
categories: ["LLM Security", "Regulatory", "Industry News"]
tags: ["openai", "data-privacy", "training-data", "opt-out", "user-consent", "claude", "anthropic", "dark-patterns", "data-governance", "privacy"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-14T10:58:33+00:00"
feed_source: "hn_openai"
original_url: "https://news.ycombinator.com/item?id=49643556"
pipeline_version: "2.1.0"
---

## Overview

Multiple users on Hacker News are reporting that OpenAI's 'allow training' setting — which allows user conversation data to be used for model training — is being silently re-enabled after users have deliberately turned it off. The original poster, jacquesm, noted they had reset the setting more than once and kept a careful record of when they last disabled it, only to find it re-enabled on a subsequent check. A corroborating report indicates the same behaviour has been observed on Anthropic's Claude platform, specifically following a subscription renewal.

This behaviour, whether intentional or a result of software bugs triggered by TOS updates or subscription events, undermines the foundational principle of informed consent in AI data governance.

## Technical Analysis

The mechanism behind the reset is not publicly confirmed, but community analysis points to several plausible triggers:

- **TOS or subscription renewal events**: Accepting a new terms-of-service agreement or resubscribing to a service tier may silently reset privacy preferences to their defaults (opt-in).
- **Account-level configuration resets**: Platform updates may not preserve user-level privacy flag states, reverting them to the system default.
- **Security classifier override**: One commenter noted that even with opt-out enabled, internal security classifiers may flag conversations and route them to internal model improvement pipelines regardless of user preference.

The net effect is that an 'opt-out' functions more as a temporary pause than a durable preference, meaning user data may be incorporated into training datasets during windows where the setting has silently reverted.

## Framework Mapping

- **AML.T0020 – Poison Training Data / AML.T0059 – Erode Dataset Integrity**: If user data re-enters training pipelines without consent, it may include sensitive, proprietary, or adversarially crafted content that degrades or manipulates model integrity.
- **AML.T0018 – Manipulate AI Model**: Persistent unauthorised data collection can shift model behaviour in ways not anticipated or audited.
- **LLM03 – Training Data Poisoning**: The unconsented ingestion of user conversations represents a training data governance failure, creating exposure to data quality and integrity risks.
- **LLM06 – Sensitive Information Disclosure**: Users who believed their data was excluded may have shared confidential information under a false assumption of privacy.

## Impact Assessment

The impact is broad. Any OpenAI or Claude subscriber who opted out of training data sharing and handles sensitive conversations — including legal, medical, financial, or proprietary business data — may have unknowingly contributed that data to training corpora. There is no confirmed mechanism for retroactive removal of data already ingested. The community observation that 'opt-out is more like a pause button' suggests this is a systemic design issue rather than an isolated bug.

## Mitigation & Recommendations

1. **Audit settings immediately**: Check your OpenAI Data Controls and Claude Privacy settings now. Re-disable training data sharing and screenshot the state with a timestamp.
2. **Monitor after any TOS update or subscription event**: Treat account-level changes as triggers to re-verify privacy preferences.
3. **Assume opt-outs are not durable**: Operationally treat any LLM platform as potentially ingesting your data unless independently verified.
4. **Request third-party audit**: Advocate for independent auditing of training data opt-out mechanisms as called for by community members.
5. **Limit sensitive data exposure**: Do not share confidential, proprietary, or personally identifiable information in LLM sessions without a verified, persistent privacy guarantee.

## References

- [Hacker News Discussion – Tell HN: OpenAI keeps re-enabling the 'allow training' setting](https://news.ycombinator.com/item?id=49643556)
