---
title: "AI Tools Expose Decades-Old Critical PHP Flaws in 70% of Websites"
date: 2026-10-22T10:30:03+00:00
draft: true
slug: "ai-tools-expose-decades-old-critical-php-flaws-in-70-of-websites"

# ── Content metadata ──
summary: "OpenAI and Google's Wiz used large language models including GPT-5.6 Sol and Gemini 4 Argon to discover critical vulnerabilities present in all PHP versions since 2004, affecting an estimated 33 million websites. The NSA issued an emergency advisory recommending sites be taken offline if patching cannot be done immediately, as the flaws allow file system and database infiltration. The disclosure carries a dual-edged implication: AI enabled responsible discovery, but also dramatically lowers the barrier for attackers to weaponise previously impractical exploits across diverse PHP configurations."
source: "TechCrunch AI"
source_url: "https://techcrunch.com/2026/10/21/php-armageddon-openai-googles-wiz-find-ancient-holes-panicking-the-internet"
source_title: "PHP Armageddon: OpenAI, Google\u2019s Wiz find ancient holes, panicking the internet"
source_date: 2026-10-21T17:59:12+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1517685352821-92cf88aee5a5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyfHxBd3MlMjBza3klMjBjbG91ZHMlMjBhZXJpYWwlMjBzdW5saWdodHxlbnwwfDB8fHwxNzkyNjY1MDAzfDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - AI-Enabled Product or Service", "AML.T0063 - Discover AI Model Outputs", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "AI tools discovered critical PHP flaws present since 2004, affecting 70% of the web."
tldr_who_at_risk: "Any organisation running a PHP-based web application or CMS such as WordPress is exposed, particularly those on unsupported PHP versions older than 8.2."
tldr_actions: ["Upgrade all PHP installations to version 8.5.12 immediately", "Take PHP-powered sites offline if patching cannot be completed without delay", "Work with hosting providers to confirm server-level patches are applied, especially for WordPress deployments"]

# ── Taxonomies ──
categories: ["Research", "Industry News", "Agentic AI"]
tags: ["php", "critical-vulnerability", "openai", "google-wiz", "gpt-5-6-sol", "gemini-4-argon", "ai-assisted-research", "nsa-advisory", "wordpress", "responsible-disclosure", "exploit-lowered-barrier", "web-security", "patch-the-planet"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-10-22T10:30:03+00:00"
feed_source: "techcrunch_ai"
original_url: "https://techcrunch.com/2026/10/21/php-armageddon-openai-googles-wiz-find-ancient-holes-panicking-the-internet"
pipeline_version: "2.1.0"
---

## Overview

The U.S. National Security Agency issued an emergency advisory on Wednesday warning of two critical vulnerabilities discovered in PHP, the server-side language powering approximately 70% of websites globally — an estimated 33 million sites. The flaws, present in all PHP versions since PHP 5 (released in 2004), allow attackers to infiltrate server file systems and connected databases. Patches have been issued by the PHP Foundation, and the NSA's guidance is stark: sites that cannot be patched immediately should be taken offline.

What makes this disclosure particularly notable for the AI security community is how the vulnerabilities were found — and why they now pose a materially greater risk than they would have even two years ago.

## Technical Analysis

Security testing firm Calif, operating under OpenAI's "Patch the Planet" initiative, used GPT-5.6 Sol to identify one of the flaws. Separately, Google's Wiz team deployed a combination of its Wiz Atlas security AI agent, Gemini 4 Argon, and GPT-5.6 Sol to surface multiple vulnerabilities in PHP. Both teams followed responsible disclosure practices, coordinating with the PHP Foundation before public announcement.

The vulnerabilities enable two classes of attack: file system infiltration and database compromise via web applications. These are not novel attack classes, but their longevity — undetected across over two decades of PHP releases — underscores the scale of what AI-assisted code analysis can now surface at speed and breadth that human reviewers historically could not.

Critically, Wiz noted in its disclosure blog that prior to AI tooling, these flaws were practically difficult to exploit: adapting an attack across PHP's diverse versions, configurations, and memory layouts required significant manual effort. LLMs remove that friction. As Wiz stated: "LLMs can help adapt an exploit to different PHP versions, configurations and memory layouts." Now that public disclosure has occurred, this capability is available to malicious actors as well.

## Framework Mapping

- **AML.T0047 – AI-Enabled Product or Service**: AI agents (Wiz Atlas, GPT-5.6 Sol) were used as the primary discovery mechanism, representing AI-enabled offensive research tooling that directly parallels attacker capability.
- **AML.T0063 – Discover AI Model Outputs**: The iterative use of LLM outputs to probe and confirm vulnerability presence mirrors techniques adversaries may use to automate vulnerability discovery.
- **AML.T0043 – Craft Adversarial Data**: AI-assisted exploit adaptation across PHP configurations maps to crafting targeted payloads at scale.
- **LLM05 – Supply Chain Vulnerabilities**: PHP is foundational infrastructure; vulnerabilities at this layer affect the entire web application supply chain.

## Impact Assessment

The blast radius is exceptionally wide. Any organisation running PHP-based web infrastructure — including WordPress sites, custom web applications, and CMS deployments — is potentially exposed. Sites running PHP 8.1 or older face compounded risk, as these versions are no longer supported and will not receive patches. Automattic, Akamai, AWS, Cloudflare, Fastly, Imperva, Microsoft, and Vercel were all engaged in coordinated response efforts, indicating recognition of internet-wide exposure.

No exploits in the wild were reported at time of disclosure, but the lowered exploitation barrier introduced by LLM tooling means that window may be short.

## Mitigation & Recommendations

1. **Upgrade PHP to version 8.5.12** across all web servers immediately.
2. **Take sites offline** if patching cannot be completed promptly, per NSA guidance.
3. **Engage hosting providers** to confirm server-level patching, particularly for managed WordPress environments.
4. **Audit PHP version inventory** across your infrastructure — unsupported versions require upgrade before patching is possible.
5. **Monitor threat intelligence feeds** for emerging exploit code now that the vulnerabilities are publicly disclosed.

## References

- [PHP Armageddon: OpenAI, Google's Wiz find ancient holes, panicking the internet — TechCrunch](https://techcrunch.com/2026/10/21/php-armageddon-openai-googles-wiz-find-ancient-holes-panicking-the-internet)
