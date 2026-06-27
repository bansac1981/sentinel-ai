---
title: "Poisoned Tenant Attack Abuses OpenAI Workspaces to Target Cybersecurity Firms"
date: 2026-06-27T03:47:48+00:00
draft: true
slug: "poisoned-tenant-attack-abuses-openai-workspaces-to-target-cybersecurity-firms"

# ── Content metadata ──
summary: "Threat actors are registering fraudulent OpenAI tenants impersonating legitimate companies and inviting employees to join them, in a campaign dubbed 'Poisoned Tenant' by Push Security. The attack exploits OpenAI's legitimate invitation infrastructure, making phishing emails appear authentic as they pass all email authentication checks. The goal appears to be tricking employees into submitting sensitive corporate information via ChatGPT chats and projects within the attacker-controlled workspace."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/cybersecurity-firms-targeted-by-fraudulent-openai-organization-invites/"
source_title: "Cybersecurity firms targeted by fraudulent OpenAI organization invites"
source_date: 2026-06-26T17:49:07+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1674027215032-f0c4292318ee?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOHx8T3BlbmFpJTIwY29udmVyc2F0aW9uYWwlMjBBSSUyMGNoYXRib3QlMjB0ZWNobm9sb2d5fGVufDB8MHx8fDE3ODI0NTA1NDd8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0012 - Valid Accounts", "AML.T0047 - ML-Enabled Product or Service", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities", "LLM09 - Overreliance"]

# ── TL;DR ──
tldr_what: "Attackers create fake OpenAI tenants impersonating real companies to harvest sensitive employee data via ChatGPT."
tldr_who_at_risk: "Cybersecurity and technology sector employees are most exposed due to targeted use of work email addresses and impersonation of their own organisations."
tldr_actions: ["Train employees to verify the inviter's email domain before accepting any OpenAI organisation invitations", "Establish an internal policy requiring out-of-band confirmation before joining any new ChatGPT workspace", "Audit existing OpenAI tenant memberships to identify any unauthorised or unrecognised organisations employees have joined"]

# ── Taxonomies ──
categories: ["LLM Security", "Industry News", "Supply Chain"]
tags: ["openai", "chatgpt", "tenant-hijacking", "social-engineering", "phishing", "workspace-abuse", "push-security", "cybersecurity-targeting", "llm-platform-abuse", "poisoned-tenant"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-06-27T03:47:48+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/cybersecurity-firms-targeted-by-fraudulent-openai-organization-invites/"
pipeline_version: "2.1.0"
---

## Overview

A novel social engineering campaign dubbed **'Poisoned Tenant'** is targeting cybersecurity and technology firms by exploiting OpenAI's legitimate workspace invitation system. Threat actors register fraudulent ChatGPT organisations that impersonate real companies, then invite specific employees — identified through prior reconnaissance — to join them. Because invitations originate from OpenAI's own notification infrastructure (`noreply@tm.openai.com`) and pass standard email authentication (SPF/DKIM/DMARC), they are virtually indistinguishable from genuine workspace onboarding emails.

The campaign was discovered by Push Security after several of their own employees received invitations to join a ChatGPT organisation named "Push Security Inc." — one they had not created.

## Technical Analysis

The attack chain is straightforward but effective:

1. **Tenant Registration**: Attackers create an OpenAI organisation using personal Gmail accounts, naming it to match the target company.
2. **Targeted Invitations**: Work email addresses of specific employees are used, suggesting prior OSINT or data-broker sourcing.
3. **Legitimate Delivery Vector**: OpenAI sends the invitation on the attacker's behalf from its own mail infrastructure, bypassing email security controls.
4. **Impersonation Inside the Workspace**: Upon joining, victims encounter an attacker-controlled account posing as the company's CEO, with pre-staged content designed to elicit sensitive information.
5. **Privilege Escalation by Design**: Invited employees are granted **Owner-level privileges**, potentially allowing further manipulation of the tenant or invitation of additional targets.

OpenAI does include a domain-mismatch warning in the invitation email, but it appears as a low-prominence single line, easily overlooked.

## Framework Mapping

- **AML.T0012 (Valid Accounts)**: Attackers abuse legitimate OpenAI account creation to establish a trusted operational base.
- **AML.T0047 (ML-Enabled Product or Service)**: The attack weaponises OpenAI's ChatGPT platform infrastructure as the delivery mechanism.
- **AML.T0057 (LLM Data Leakage)**: The ultimate objective is inducing victims to submit sensitive corporate data into an attacker-monitored LLM workspace.
- **LLM06 (Sensitive Information Disclosure)**: Employees interacting with the fake workspace may inadvertently expose proprietary information.
- **LLM09 (Overreliance)**: The attack exploits implicit trust users place in familiar SaaS platforms, particularly enterprise AI tools.

## Impact Assessment

The campaign specifically targets cybersecurity and technology companies — sectors whose employees routinely handle sensitive vulnerability data, client intelligence, and internal security tooling. An employee who submits details of an ongoing incident, a security assessment, or internal architecture into the fraudulent workspace would be providing high-value intelligence directly to attackers. The use of Owner-level privileges also means a compromised employee could inadvertently invite colleagues, amplifying the attack's reach within an organisation.

## Mitigation & Recommendations

- **Verify inviter identity out-of-band**: Never accept OpenAI workspace invitations without confirming directly with the sender via a separate channel.
- **Check the inviter's email domain**: OpenAI's warning about domain mismatches should be treated as an immediate red flag requiring investigation.
- **Establish an approved-workspace registry**: Organisations should document and communicate which AI platform tenants employees are authorised to join.
- **Security awareness training**: Include AI platform social engineering scenarios in phishing simulation programmes.
- **Monitor OpenAI organisation memberships**: Periodically audit which ChatGPT workspaces employees are members of.
- **Request OpenAI platform controls**: Advocate for stronger tenant verification and domain-matching enforcement at the platform level.

## References

- [BleepingComputer — Cybersecurity firms targeted by fraudulent OpenAI organization invites](https://www.bleepingcomputer.com/news/security/cybersecurity-firms-targeted-by-fraudulent-openai-organization-invites/)
- Push Security — Poisoned Tenant Campaign Report (referenced in article)
