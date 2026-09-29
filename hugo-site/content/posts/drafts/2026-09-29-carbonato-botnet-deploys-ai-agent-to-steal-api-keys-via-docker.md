---
title: "Carbonato Botnet Deploys AI Agent to Steal API Keys via Docker"
date: 2026-09-29T11:35:01+00:00
draft: true
slug: "carbonato-botnet-deploys-ai-agent-to-steal-api-keys-via-docker"

# ── Content metadata ──
summary: "The Carbonato botnet is compromising exposed Docker hosts and deploying the open-source Hermes Agent AI framework to execute commands via Telegram, effectively weaponising an AI agent for post-exploitation operations. A key objective of the campaign is the theft of AI API keys stored on compromised hosts, representing a novel convergence of traditional botnet infrastructure with agentic AI tooling. This development signals an escalating trend of threat actors co-opting legitimate AI agent frameworks as command-and-control and credential harvesting mechanisms."
source: "Dark Reading"
source_url: "https://www.darkreading.com/identity-access-management-security/carbonato-botnet-ai-agent-hacked-docker-hosts"
source_title: "Carbonato Botnet Puts an AI Agent on Hacked Docker Hosts"
source_date: 2026-09-28T20:23:58+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1580541832626-2a7131ee809f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw2fHxjaGVzcyUyMHBpZWNlJTIwc3RyYXRlZ3klMjBib2FyZCUyMGdhbWV8ZW58MHwwfHx8MTc5MDY4MTcwMXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0103 - Deploy AI Agent", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0040 - AI Model Inference API Access", "AML.T0047 - AI-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Carbonato botnet deploys Hermes AI agent on hacked Docker hosts to steal AI API keys via Telegram."
tldr_who_at_risk: "Organisations running publicly exposed Docker hosts with AI API keys stored in environment variables or configuration files are most directly at risk."
tldr_actions: ["Audit and restrict public exposure of Docker API endpoints immediately", "Rotate all AI API keys stored on Docker hosts and migrate to secrets management vaults", "Monitor container environments for unexpected Telegram outbound connections and agent framework installations"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Industry News"]
tags: ["carbonato-botnet", "docker-security", "ai-agent-abuse", "hermes-agent", "api-key-theft", "telegram-c2", "credential-harvesting", "container-security", "botnet", "agentic-ai"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-29T11:35:01+00:00"
feed_source: "darkreading"
original_url: "https://www.darkreading.com/identity-access-management-security/carbonato-botnet-ai-agent-hacked-docker-hosts"
pipeline_version: "2.1.0"
---

## Overview

The Carbonato botnet has been observed targeting exposed Docker hosts and deploying the open-source Hermes Agent AI framework as a post-exploitation tool. Once installed, the agent accepts commands via Telegram and systematically harvests AI API keys from the compromised environment. This represents a meaningful evolution in botnet tradecraft: rather than relying solely on custom malware, threat actors are now co-opting legitimate, community-trusted AI agent frameworks to conduct operations — reducing development overhead while leveraging the framework's native tool-use and automation capabilities.

The significance extends beyond credential theft. Deploying an AI agent on a compromised host gives attackers a flexible, LLM-powered interface capable of adapting commands dynamically, blurring the line between scripted malware and interactive autonomous attack tooling.

## Technical Analysis

The attack chain begins with the discovery and compromise of Docker hosts with exposed management interfaces — a long-standing attack surface. Following initial access, Carbonato installs the Hermes Agent AI framework, an open-source project designed to enable LLM-driven task execution via tool invocations.

The agent is configured to receive operator instructions via a Telegram bot channel, providing an encrypted, low-friction command-and-control (C2) channel that blends with legitimate Telegram traffic. Operators can issue natural-language or structured commands to the agent, which translates them into system-level actions on the host.

A primary objective is the exfiltration of AI API keys — credentials for services such as OpenAI, Anthropic, or similar platforms — which may be stored in `.env` files, Docker environment variables, or application configuration files. Stolen keys can be monetised directly (resold, used for compute theft) or leveraged to access AI services at scale under the victim's billing account.

## Framework Mapping

- **AML.T0103 (Deploy AI Agent):** The core technique — Hermes Agent is deployed on compromised infrastructure as an attacker-controlled autonomous component.
- **AML.T0083 / AML.T0098 (Credentials from AI Agent Configuration / AI Agent Tool Credential Harvesting):** The agent actively seeks and exfiltrates AI API keys.
- **AML.T0086 (Exfiltration via AI Agent Tool Invocation):** Data exfiltration occurs through the agent's tool-use capabilities rather than traditional malware exfil channels.
- **LLM08 (Excessive Agency):** The deployed agent operates with broad host-level permissions, illustrating the risk of unconstrained AI agent execution.
- **LLM06 (Sensitive Information Disclosure):** AI API keys and potentially other secrets are disclosed to the attacker.

## Impact Assessment

Organisations with exposed Docker infrastructure face direct risk of host compromise and AI credential theft. Stolen AI API keys can result in significant financial harm through unauthorised compute usage, data exposure via API access, and potential pivot into AI-powered services used by the victim. The use of a legitimate open-source agent framework complicates detection, as process and network artefacts may resemble benign tooling.

## Mitigation & Recommendations

1. **Restrict Docker API exposure** — ensure Docker management interfaces are never publicly accessible; enforce firewall rules and network segmentation.
2. **Secrets management** — remove AI API keys from environment variables and flat files; use dedicated secrets managers (HashiCorp Vault, AWS Secrets Manager).
3. **Monitor for anomalous agent frameworks** — implement container runtime security tooling to alert on unexpected process installations such as Python-based agent frameworks.
4. **Block unexpected Telegram egress** — apply egress filtering to flag or block Telegram API traffic originating from container workloads.
5. **Rotate compromised credentials** — any host suspected of exposure should trigger immediate AI API key rotation.

## References

- [Dark Reading: Carbonato Botnet Puts an AI Agent on Hacked Docker Hosts](https://www.darkreading.com/identity-access-management-security/carbonato-botnet-ai-agent-hacked-docker-hosts)
