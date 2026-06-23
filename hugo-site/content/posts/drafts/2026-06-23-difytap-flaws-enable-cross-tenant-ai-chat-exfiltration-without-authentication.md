---
title: "DifyTap Flaws Enable Cross-Tenant AI Chat Exfiltration Without Authentication"
date: 2026-06-23T04:07:17+00:00
draft: true
slug: "difytap-flaws-enable-cross-tenant-ai-chat-exfiltration-without-authentication"

# ── Content metadata ──
summary: "Four vulnerabilities collectively dubbed DifyTap were disclosed in Dify, a widely-used open-source agentic AI workflow platform, enabling attackers to silently intercept and exfiltrate AI conversations across customer tenants without authentication. Two critical-severity flaws (CVSS 9.1 and 9.4) allow authorization bypasses and path traversal into internal Plugin Daemon APIs, while a third enables any authenticated user to read documents uploaded by users across all tenants using only a file UUID. The vulnerabilities collectively allow attackers to establish a persistent covert exfiltration channel routing all victim application messages and LLM responses to an attacker-controlled tracing provider."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/06/researchers-detail-difytap-flaws-in.html"
source_title: "Researchers Detail DifyTap Flaws in Dify That Could Expose AI Chats Across Tenants"
source_date: 2026-06-22T16:13:28+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1751448555253-f39c06e29d82?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxM3x8QXdzJTIwZGF0YSUyMGJyZWFjaCUyMHByaXZhY3klMjBzZWN1cml0eSUyMHBhZGxvY2slMjBzZXJ2ZXJ8ZW58MHwwfHx8MTc4MjE4NzYzN3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 9.1
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0040 - ML Model Inference API Access", "AML.T0047 - ML-Enabled Product or Service", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design", "LLM05 - Supply Chain Vulnerabilities", "LLM02 - Insecure Output Handling"]

# ── TL;DR ──
tldr_what: "Four Dify vulnerabilities let attackers silently intercept AI conversations across tenants without authentication."
tldr_who_at_risk: "Organisations and developers using Dify's cloud multi-tenant service are directly exposed, as any registered attacker account can exploit these flaws against public-facing AI applications."
tldr_actions: ["Apply all Dify patches addressing CVE-2026-41947 through CVE-2026-41950 immediately", "Audit trace configuration settings across all applications to detect unauthorised exfiltration endpoints", "Restrict public registration and enforce tenant isolation controls on self-hosted Dify deployments"]

# ── Taxonomies ──
categories: ["LLM Security", "Agentic AI", "Research", "Supply Chain"]
tags: ["dify", "difytap", "cross-tenant-exposure", "authorization-bypass", "path-traversal", "ai-chat-exfiltration", "multi-tenant-security", "agentic-workflow", "plugin-daemon", "cve-2026-41947", "cve-2026-41948", "cve-2026-41949", "cve-2026-41950", "pdfium", "zafran-security"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-23T04:07:17+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/06/researchers-detail-difytap-flaws-in.html"
pipeline_version: "2.0.0"
---

## Overview

Zafran Security researchers Ido Shani and Gal Zaban have disclosed four vulnerabilities in Dify — an open-source agentic AI workflow platform with over 146,000 GitHub stars — that collectively enable silent, cross-tenant exfiltration of AI conversations. Branded **DifyTap**, the vulnerability set is notable for including two unauthenticated attack paths and three flaws with cross-tenant impact on Dify's multi-tenant cloud service. The disclosures also surfaced a dependency on a two-year-old critical PDFium bug (CVE-2024-5846, CVSS 8.8).

## Technical Analysis

The four CVEs span two distinct attack surfaces: authorization logic failures and internal API exposure.

**CVE-2026-41947 (CVSS 9.1)** — Authenticated editor-role users can set and enable LLM trace configurations for *any* tenant's application, not just their own. Because anyone can freely register a Dify account, this is effectively a low-barrier attack. An attacker registers, configures their own LLM trace provider as the destination, and redirects all messages and model responses from target applications into an attacker-controlled endpoint — creating a persistent, covert exfiltration channel.

**CVE-2026-41948 (CVSS 9.4)** — A path traversal vulnerability in request forwarding to the Plugin Daemon's internal REST API. Insufficient URL path sanitization allows authenticated users to reach private, internal endpoints not intended for external access, effectively traversing Dify's internal service boundary.

**CVE-2026-41949 (CVSS 7.5/5.9)** — An authorization bypass in the file preview endpoint (`/console/api/files/{file_id}/preview`). Any authenticated user can read up to 3,000 characters of any uploaded document across *all tenants and workspaces* by supplying the target file's UUID — a value that may be observable through normal application interactions.

**CVE-2026-41950 (CVSS 6.5)** — Authenticated users can read full file contents uploaded by other users within the same tenant by injecting an arbitrary file UUID into the `files` array of a chat-messages API request.

Additionally, Dify's PDF parsing stack was found to depend on a vulnerable PDFium build susceptible to CVE-2024-5846, a heap use-after-free exploitable via a crafted PDF file.

## Framework Mapping

- **AML.T0057 (LLM Data Leakage)**: The trace configuration hijack directly routes all LLM inputs and outputs to attacker infrastructure.
- **AML.T0040 (ML Model Inference API Access)**: Internal Plugin Daemon API traversal exposes model inference endpoints beyond their intended scope.
- **LLM06 (Sensitive Information Disclosure)**: Cross-tenant document and conversation exposure is the primary impact class.
- **LLM07 (Insecure Plugin Design)**: The Plugin Daemon path traversal reflects insufficient isolation between the plugin subsystem and internal APIs.
- **LLM05 (Supply Chain Vulnerabilities)**: The outdated PDFium dependency introduces a known critical RCE-class bug into the platform's file processing pipeline.

## Impact Assessment

Organisations relying on Dify Cloud's multi-tenant environment face the highest risk. Since Dify allows open registration, no prior relationship with the victim is required. Any publicly accessible Dify application can be targeted for persistent conversation monitoring. Self-hosted deployments are affected by the file access and path traversal bugs, though cross-tenant risk is reduced depending on isolation configuration.

## Mitigation & Recommendations

1. **Patch immediately**: Apply all vendor-issued fixes for CVE-2026-41947 through CVE-2026-41950 and the PDFium dependency update.
2. **Audit trace configurations**: Review all application tracing endpoints for unauthorised or unexpected external destinations.
3. **Restrict open registration**: On cloud or shared deployments, gate account creation to known users to raise the attacker entry barrier.
4. **Enforce tenant-level ACLs**: Validate that file and API access controls enforce strict tenant ownership checks at every endpoint.
5. **Inventory third-party C/C++ dependencies**: Regularly scan native parsing libraries (PDF, image, document) for known CVEs.

## References

- [The Hacker News — Researchers Detail DifyTap Flaws in Dify](https://thehackernews.com/2026/06/researchers-detail-difytap-flaws-in.html)
