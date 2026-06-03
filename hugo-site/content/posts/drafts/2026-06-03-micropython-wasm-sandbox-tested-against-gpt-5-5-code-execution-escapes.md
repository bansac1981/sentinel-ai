---
title: "MicroPython WASM Sandbox Tested Against GPT-5.5 Code Execution Escapes"
date: 2026-06-03T23:07:24+00:00
draft: true
slug: "micropython-wasm-sandbox-tested-against-gpt-5-5-code-execution-escapes"

# ── Content metadata ──
summary: "Simon Willison has released an alpha of datasette-agent-micropython, which uses MicroPython running inside a WebAssembly sandbox to allow Datasette Agent to execute LLM-generated Python code safely. The project represents a practical defensive architecture for agentic AI systems that require code execution capabilities. Notably, the author reports that GPT-5.5 has so far failed to escape the sandbox, framing this as an early but promising security validation."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Jun/2/datasette-agent-micropython/#atom-everything"
source_title: "datasette-agent-micropython 0.1a0"
source_date: 2026-06-02T19:28:36+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1677442135136-760c813028c0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwzfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neSUyMG5ldXJhbCUyMG5ldHdvcmt8ZW58MHwwfHx8MTc4MDUyNzcwOHww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0051 - LLM Prompt Injection", "AML.T0054 - LLM Jailbreak", "AML.T0047 - ML-Enabled Product or Service"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Alpha release uses MicroPython in WASM to sandbox LLM-generated code execution in Datasette Agent."
tldr_who_at_risk: "Developers building agentic AI systems with code execution capabilities are most exposed if sandboxing is absent or insufficiently hardened."
tldr_actions: ["Evaluate WASM-based sandboxing as a containment layer for any LLM agent that generates and executes code", "Red-team sandbox implementations against adversarial LLM outputs before production deployment", "Monitor for sandbox escape attempts in agent logs, treating unexpected system calls or file access as indicators of compromise"]

# ── Taxonomies ──
categories: ["Agentic AI", "LLM Security", "Research"]
tags: ["code-execution", "sandbox-escape", "webassembly", "micropython", "agentic-ai", "datasette", "llm-generated-code", "wasm-sandbox", "defensive-architecture"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-06-03T23:07:24+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Jun/2/datasette-agent-micropython/#atom-everything"
pipeline_version: "1.0.0"
---

## Overview

Simon Willison has published an alpha release of `datasette-agent-micropython`, a plugin that runs MicroPython inside a WebAssembly (WASM) sandbox to give Datasette Agent a safe environment for executing LLM-generated Python code. The project addresses one of the most significant risks in agentic AI architectures: unsandboxed code execution. Willison notes that GPT-5.5 has so far failed to break out of the sandbox, offering an early empirical data point on the approach's robustness.

## Technical Analysis

The architecture layers two isolation mechanisms: MicroPython, a constrained Python runtime with a reduced standard library, and WebAssembly, a bytecode format with a well-defined capability boundary enforced by the host runtime. Together, these limit what LLM-generated code can access at both the language and system levels.

The threat model being addressed is one where an LLM — whether through prompt injection, jailbreaking, or simply generating unsafe code — produces Python that attempts to escape its execution context. In a naive agentic pipeline, this could mean arbitrary file system access, network calls, or process spawning. By confining execution to MicroPython-in-WASM, the attack surface for such escapes is substantially reduced.

The informal adversarial test against GPT-5.5 is directionally useful but not a formal security evaluation. WASM sandboxes have historically had vulnerabilities, and MicroPython's reduced stdlib does not eliminate all escape vectors — particularly if host bindings are misconfigured.

## Framework Mapping

- **AML.T0051 (LLM Prompt Injection)** and **AML.T0054 (LLM Jailbreak)**: The sandbox is a direct mitigation against prompt injection or jailbreak payloads that attempt to weaponise code generation capabilities.
- **LLM02 (Insecure Output Handling)**: Executing LLM-generated code without a sandbox is a textbook instance of this category; this project is a defensive response to it.
- **LLM08 (Excessive Agency)**: Agentic systems with code execution privileges represent high-agency configurations. Sandboxing is a key control to limit blast radius.

## Impact Assessment

This is a low-threat, high-interest item. There is no active vulnerability disclosed. The relevance lies in the defensive pattern being demonstrated: as agentic AI systems proliferate and LLM code generation becomes a standard capability, the absence of execution sandboxing will become an increasingly exploited attack surface. Developers who deploy LLM agents with Python execution and no sandboxing are at meaningful risk.

## Mitigation & Recommendations

- **Adopt WASM-based sandboxing** for any LLM agent that executes generated code; WASI-compliant runtimes (Wasmtime, Wasmer) provide configurable capability gates.
- **Restrict host bindings** exposed to the WASM module — even with WASM isolation, over-permissive host function imports can reintroduce escape vectors.
- **Conduct adversarial testing** using a range of models and prompt injection payloads before treating any sandbox as production-hardened.
- **Apply least-privilege principles** to the agent's broader environment: even if code escapes the WASM layer, container-level or OS-level restrictions should limit damage.
- **Log all executed code** for post-hoc audit and anomaly detection.

## References

- [datasette-agent-micropython 0.1a0 — Simon Willison](https://simonwillison.net/2026/Jun/2/datasette-agent-micropython/#atom-everything)
