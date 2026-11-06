---
title: "Claude Code Leaks User Email in HTTP User-Agent Headers"
date: 2026-11-06T13:10:11+00:00
draft: false
slug: "claude-code-leaks-user-email-in-http-user-agent-headers"

# ── Content metadata ──
summary: "A confirmed bug in Anthropic's Claude Code agentic coding tool exposes users' email addresses to arbitrary third-party websites via the HTTP User-Agent request header during web searches. This constitutes an unsanctioned data disclosure that users cannot meaningfully prevent, creating a harvesting vector for spam and phishing campaigns. The issue has drawn significant community backlash, with nearly 500 upvotes on the GitHub issue, and raises broader concerns about privacy controls in agentic AI tooling."
source: "Anthropic (via HN)"
source_url: "https://github.com/anthropics/claude-code/issues/107757"
source_title: "Claude Code sends your email address to websites"
source_date: 2026-11-05T22:17:15+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1758685734671-21838fcd724e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHxzY2llbnRpc3QlMjB0aGlua2luZyUyMGFic3RyYWN0fGVufDB8MHx8fDE3OTM5NzA2MTB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0084 - Discover AI Agent Configuration", "AML.T0063 - Discover AI Model Outputs"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Claude Code embeds user email addresses in HTTP User-Agent headers sent to third-party websites."
tldr_who_at_risk: "All Claude Code users on any platform who use its web search capabilities are exposed, with their email addresses silently transmitted to every contacted web server."
tldr_actions: ["Audit outbound HTTP headers from any agentic AI tool before allowing web access", "Disable or sandbox Claude Code's web search functionality until Anthropic issues a patch", "Review network logs for unexpected PII transmission in User-Agent or other HTTP headers"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Industry News"]
tags: ["claude-code", "anthropic", "user-agent", "email-disclosure", "privacy-violation", "agentic-ai", "data-leakage", "http-headers", "pii-exposure", "web-search"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-06T13:10:11+00:00"
feed_source: "hn_anthropic"
original_url: "https://github.com/anthropics/claude-code/issues/107757"
pipeline_version: "2.1.0"
content_hash: "7c6f824e1fa4993e"
---

## Overview

A privacy vulnerability in Anthropic's Claude Code (version 2.1.318) has been confirmed to expose authenticated users' email addresses to arbitrary third-party web servers through the HTTP `User-Agent` request header. The issue, filed as GitHub issue #107757 on 5 November 2026, was opened by user `taylor-edwards` and has accumulated nearly 500 upvotes, indicating widespread impact across the Claude Code user base.

When Claude Code performs web searches as part of its agentic task execution, it appends the authenticated user's email address to the `User-Agent` string sent with outbound HTTP requests. This means every web server contacted during an agent session receives the user's personal identifier — without explicit consent, disclosure, or a meaningful opt-out mechanism.

## Technical Analysis

The root cause appears to be the inclusion of session or account identity metadata within the HTTP `User-Agent` header, likely introduced as a telemetry or traffic-identification mechanism to distinguish agentic from human web traffic. While such identification may serve legitimate rate-limiting or policy-compliance purposes from Anthropic's perspective, embedding PII — specifically email addresses — in a header transmitted verbatim to third-party servers is a significant design flaw.

HTTP `User-Agent` headers are logged by virtually every web server by default and are visible to:
- The destination web server and its operators
- Any CDN, reverse proxy, or WAF in the request path
- Network-level passive observers
- Ad networks and analytics platforms embedded in target pages

This creates a durable, low-effort email harvesting vector. Malicious site operators or compromised CDN logs could trivially extract and monetise these addresses at scale.

```
User-Agent: claude-code/2.1.318 (darwin) user@example.com
```
*(Reconstructed example based on issue description; exact format unconfirmed)*

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0057 – LLM Data Leakage**: The agent autonomously discloses PII (email) as a side-effect of tool use, without user awareness.
- **AML.T0086 – Exfiltration via AI Agent Tool Invocation**: The web search tool acts as the exfiltration channel for sensitive identity data.
- **AML.T0084 – Discover AI Agent Configuration**: Third parties passively receive configuration/identity data embedded in request metadata.

**OWASP LLM Top 10:**
- **LLM06 – Sensitive Information Disclosure**: Email addresses constitute PII and their transmission is unsanctioned.
- **LLM08 – Excessive Agency**: The agent performs actions (transmitting PII) beyond the scope of what the user authorised.
- **LLM07 – Insecure Plugin Design**: The web search plugin lacks adequate data minimisation controls.

## Impact Assessment

All Claude Code users who use the tool's web search or browsing capabilities are affected. The impact is primarily a privacy harm — enabling spam, phishing targeting, and identity profiling — rather than direct system compromise. However, in regulated jurisdictions (GDPR, CCPA), unsanctioned transmission of email addresses to third parties may constitute a notifiable data protection incident for enterprise users.

The reporter states they have migrated their company away from Claude Code as a direct result, suggesting reputational and commercial consequences for Anthropic.

## Mitigation & Recommendations

1. **Disable Claude Code web search** until Anthropic issues a confirmed patch stripping PII from outbound headers.
2. **Inspect outbound HTTP headers** using a local proxy (e.g., mitmproxy, Burp Suite) for any agentic AI tool before granting internet access.
3. **Apply network egress filtering** to prevent agentic tools from contacting arbitrary external hosts.
4. **Demand vendor confirmation** of data minimisation practices in AI agent tooling before enterprise deployment.
5. **Review GDPR/CCPA obligations** if Claude Code was used in a business context, as third-party PII transmission may require incident assessment.

## References

- [GitHub Issue #107757 — Bug Report: Privacy violation in User-Agent header](https://github.com/anthropics/claude-code/issues/107757)
