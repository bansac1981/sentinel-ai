---
title: "Over 1,000 Exposed ComfyUI Instances Targeted in Cryptomining Botnet Campaign"
date: "2026-04-13T14:44:56+00:00"
draft: false

# ── Content metadata ──
summary: "Threat actors are actively exploiting internet-exposed ComfyUI instances \u2014 a popular AI image generation platform \u2014 by abusing its custom node execution feature to achieve unauthenticated remote code execution. Over 1,000 publicly accessible instances have been identified as targets, with compromised hosts enrolled in Monero and Conflux cryptomining operations and a Hysteria V2 proxy botnet. The attack highlights critical supply chain and insecure plugin design risks inherent in AI/ML tooling ecosystems."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/04/over-1000-exposed-comfyui-instances.html"
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/17323801/pexels-photo-17323801.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - ML Supply Chain Compromise", "AML.T0047 - ML-Enabled Product or Service", "AML.T0040 - ML Model Inference API Access"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News", "LLM Security"]
tags: ["comfyui", "stable-diffusion", "cryptomining", "remote-code-execution", "botnet", "custom-nodes", "xmrig", "lolminer", "monero", "unauthenticated-access", "ai-infrastructure", "supply-chain", "comfyui-manager", "flask-c2", "aeza-group"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-04-13T05:08:28+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/04/over-1000-exposed-comfyui-instances.html"
pipeline_version: "1.0.0"
slug: "over-1000-exposed-comfyui-instances-targeted-in-cryptomining-botnet-campaign"
---

## Overview

An active campaign is targeting over 1,000 internet-exposed instances of ComfyUI, a widely used open-source stable diffusion workflow platform, to enlist compromised hosts into a dual-purpose cryptomining and proxy botnet. Discovered by Censys researcher Mark Ellzey in late March 2026, the operation exploits a fundamental misconfiguration in ComfyUI deployments that permits unauthenticated remote code execution through the platform's custom node plugin system. The campaign underscores a growing threat surface in AI/ML tooling infrastructure that is often deployed without hardening or authentication controls.

## Technical Analysis

The attack chain begins with a purpose-built Python scanner that continuously sweeps major cloud IP ranges for publicly accessible ComfyUI instances. The scanner checks whether any of several known vulnerable custom node families are installed, including:

- `Vova75Rus/ComfyUI-Shell-Executor`
- `filliptm/ComfyUI_Fill-Nodes`
- `seanlynch/srl-nodes`
- `ruiqutech/ComfyUI-RuiquNodes`

These node families share a critical trait: they accept raw Python code as input and execute it directly without authentication checks. If none of the target nodes are found, the scanner probes for ComfyUI-Manager — a legitimate plugin management tool — and uses it to silently install a malicious package (`ComfyUI-Shell-Executor`) created by the attacker. This package then fetches a next-stage shell script (`ghost.sh`) from the attacker's infrastructure at `77.110.96[.]200`, a host associated with bulletproof hosting provider Aeza Group.

Upon successful exploitation, the scanner removes forensic artefacts and proceeds to deploy:
- **XMRig** for Monero mining
- **lolMiner** for Conflux mining
- **Hysteria V2** for proxy botnet functionality

All compromised nodes are centrally managed via a Flask-based command-and-control (C2) dashboard. The technique of abusing ComfyUI custom nodes for arbitrary code execution was partially documented by Snyk in December 2024, but this campaign represents the first known large-scale weaponisation.

## Framework Mapping

- **AML.T0010 (ML Supply Chain Compromise):** The attacker introduces a malicious custom node package via ComfyUI-Manager, poisoning the plugin supply chain of the target environment.
- **AML.T0047 (ML-Enabled Product or Service):** ComfyUI itself is abused as the attack surface — the ML platform becomes the initial access vector.
- **LLM07 (Insecure Plugin Design):** Custom nodes execute arbitrary Python without authentication, directly mapping to insecure plugin/extension design patterns.
- **LLM05 (Supply Chain Vulnerabilities):** Malicious packages are injected through a trusted plugin management mechanism (ComfyUI-Manager).
- **LLM08 (Excessive Agency):** The plugin system is granted execution privileges far exceeding what is needed for legitimate inference workflows.

## Impact Assessment

With over 1,000 publicly accessible ComfyUI instances identified, the immediate victim pool consists primarily of independent researchers, small studios, and developers running AI image generation workflows on cloud infrastructure without authentication controls. The financial impact manifests through stolen compute resources used for cryptomining. However, the same exploitation primitive could be trivially repurposed for data exfiltration, lateral movement, or persistent access to AI development environments containing sensitive model weights or training data.

## Mitigation & Recommendations

1. **Never expose ComfyUI directly to the internet.** Place instances behind a VPN, reverse proxy with authentication, or restrict access via firewall rules.
2. **Audit installed custom nodes** and remove any packages not sourced from verified, well-maintained repositories.
3. **Disable ComfyUI-Manager's remote install capability** in production environments to prevent attacker-driven package installation.
4. **Monitor outbound network traffic** from AI workstations for connections to mining pools or unknown C2 endpoints.
5. **Apply principle of least privilege** to ComfyUI process accounts to limit post-exploitation impact.
6. **Scan for indicators of compromise** including connections to `77.110.96[.]200` and presence of `ghost.sh`, XMRig, or lolMiner binaries.

## References

- [The Hacker News – Over 1,000 Exposed ComfyUI Instances Targeted in Cryptomining Botnet Campaign](https://thehackernews.com/2026/04/over-1000-exposed-comfyui-instances.html)
