---
title: "Prompt Injection Achieves RCE in Semantic Kernel Agent Framework"
date: 2026-05-08T02:43:29+00:00
draft: true
slug: "prompt-injection-achieves-rce-in-semantic-kernel-agent-framework"

# ── Content metadata ──
summary: "Microsoft's Defender Security Research Team disclosed two CVEs in Semantic Kernel \u2014 a widely-used AI agent orchestration framework \u2014 demonstrating how prompt injection can escalate to remote code execution via compromised plugins. The vulnerabilities (CVE-2026-26030 and CVE-2026-25592) expose a systemic risk in the agentic AI layer: because frameworks like Semantic Kernel abstract tool orchestration, a single flaw in how LLM outputs are mapped to system tools can propagate across every application built on that foundation. This research signals a critical shift in AI threat modelling, where prompt injection is no longer a content risk but an execution risk."
source: "Microsoft Security Blog"
source_url: "https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/"
source_title: "When prompts become shells: RCE vulnerabilities in AI agent frameworks"
source_date: 2026-05-07T20:22:39+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1749996899010-fed1d5352e1f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxM3x8YXJ0aWZpY2lhbCUyMGludGVsbGlnZW5jZSUyMHJvYm90JTIwc2VjdXJpdHl8ZW58MHwwfHx8MTc3ODIwODIwOXww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 9.2
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data", "AML.T0057 - LLM Data Leakage"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM01 - Prompt Injection", "LLM02 - Insecure Output Handling", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Two Semantic Kernel CVEs let prompt injection trigger remote code execution via compromised agent plugins."
tldr_who_at_risk: "Developers and enterprises building AI agent applications on Semantic Kernel, LangChain, or CrewAI are directly exposed due to systemic trust misplacement in framework tool-mapping layers."
tldr_actions: ["Patch Semantic Kernel immediately and review CVE-2026-26030 and CVE-2026-25592 advisories", "Audit all agent plugins/tools for untrusted input paths and enforce strict parameter validation", "Apply least-privilege principles to agent tool permissions and sandbox code execution environments"]

# ── Taxonomies ──
categories: ["LLM Security", "Prompt Injection", "Agentic AI", "Research"]
tags: ["semantic-kernel", "rce", "prompt-injection", "ai-agents", "cve-2026-26030", "cve-2026-25592", "plugin-security", "langchain", "crewai", "tool-use", "microsoft", "responsible-disclosure", "arbitrary-file-write", "vector-store"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-05-08T02:43:29+00:00"
feed_source: "microsoft_security"
original_url: "https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/"
pipeline_version: "1.0.0"
---

## Overview

Microsoft's Defender Security Research Team has disclosed two critical vulnerabilities in Semantic Kernel, one of the most widely adopted AI agent orchestration frameworks, revealing how prompt injection can escalate directly to remote code execution (RCE). The findings represent a landmark moment in AI security: vulnerabilities in the agentic layer are no longer theoretical content risks — they are live execution risks capable of granting attackers shell-level access.

The two CVEs — **CVE-2026-26030** (In-Memory Vector Store) and **CVE-2026-25592** (Arbitrary File Write via SessionsPythonPlugin) — were responsibly disclosed and patched before publication.

---

## Technical Analysis

The root cause in both cases is a trust boundary failure between the LLM output layer and the plugin execution layer. AI agent frameworks parse natural language into structured tool call schemas. Semantic Kernel then maps these schemas directly to system-level operations — without sufficient validation that the parsed parameters are safe.

**CVE-2026-26030 (In-Memory Vector Store):** An attacker embedding adversarial content in data ingested by the vector store can manipulate retrieval results, injecting malicious tool parameters into the agent's reasoning context. This allows the attacker to steer subsequent plugin calls with attacker-controlled values.

**CVE-2026-25592 (Arbitrary File Write via SessionsPythonPlugin):** The SessionsPythonPlugin, designed to allow agents to execute Python code, did not adequately sanitise file path parameters derived from LLM output. A crafted prompt injection payload could cause the agent to write attacker-controlled content to arbitrary filesystem paths, enabling a path traversal-to-RCE attack chain.

The attack chain is illustrative:
1. Attacker embeds prompt injection payload in external content (e.g., a document, web page, or database record)
2. Agent ingests and processes the content
3. LLM parses the adversarial instruction and generates a tool call with attacker-controlled parameters
4. Framework executes the tool without validating parameter provenance
5. Arbitrary file write or code execution occurs

---

## Framework Mapping

| Framework | Category | Relevance |
|---|---|---|
| AML.T0051 | LLM Prompt Injection | Core attack vector |
| AML.T0043 | Craft Adversarial Data | Payload crafting in ingested content |
| AML.T0047 | ML-Enabled Product or Service | Framework-level systemic risk |
| LLM01 | Prompt Injection | Direct classification |
| LLM07 | Insecure Plugin Design | Trust failure in tool parameter handling |
| LLM08 | Excessive Agency | Agent acts on injected instructions without constraint |
| LLM02 | Insecure Output Handling | LLM output passed unsanitised to system calls |

---

## Impact Assessment

The systemic nature of this risk is what elevates severity to critical. Semantic Kernel, LangChain, and CrewAI collectively underpin thousands of enterprise AI applications. A vulnerability in the framework layer multiplies across every application built on top of it. Affected parties include:

- **Enterprise developers** using Semantic Kernel to build document processing, coding, or data retrieval agents
- **Cloud-hosted AI services** where agents have access to persistent storage or code execution environments
- **Any pipeline** that ingests untrusted external content (web, email, user uploads) into an agent with active plugins

---

## Mitigation & Recommendations

1. **Patch immediately** — Apply the latest Semantic Kernel releases addressing CVE-2026-26030 and CVE-2026-25592
2. **Validate tool parameters** — Never trust LLM-generated parameters directly; enforce allowlists and schema validation at the plugin boundary
3. **Sandbox execution environments** — Isolate code-execution plugins (e.g., Python runners) in containers with no filesystem access to sensitive paths
4. **Apply least privilege** — Agent tools should have the minimum permissions required; avoid granting write access unless explicitly necessary
5. **Monitor agent behaviour** — Log all plugin invocations and flag anomalous tool call patterns for review
6. **Treat external content as untrusted** — Any data ingested from outside the trust boundary should be treated as potentially adversarial

---

## References

- [Microsoft Security Blog — When prompts become shells: RCE vulnerabilities in AI agent frameworks](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)
