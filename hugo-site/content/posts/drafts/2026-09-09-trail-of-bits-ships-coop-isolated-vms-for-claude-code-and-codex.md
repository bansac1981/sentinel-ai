---
title: "Trail of Bits Ships Coop: Isolated VMs for Claude Code and Codex"
date: 2026-09-09T10:03:50+00:00
draft: false 
slug: "trail-of-bits-ships-coop-isolated-vms-for-claude-code-and-codex"

# ── Content metadata ──
summary: "Trail of Bits has released Coop, an open-source Rust CLI that provisions disposable, isolated virtual machines for running Claude Code and OpenAI Codex with full tool access \u2014 including Docker, git, compilers, and package managers \u2014 without exposing the host system. This directly closes the containment gap that has made agentic AI coding assistants a liability in developer environments, giving security teams a reproducible boundary between autonomous AI tool execution and production infrastructure. What remains unaddressed is broader multi-provider coverage, enterprise policy enforcement, and centralised audit logging maturity needed before this is ready for regulated-environment deployment at scale."
source: "Anthropic (via HN)"
source_url: "https://github.com/trailofbits/coop"
source_title: "Coop \u2013 Isolated VM Environments for Running Claude Code and Codex"
source_date: 2026-09-07T04:18:28+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1455651264681-40d634a35ce4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyMXx8b3BlbiUyMGJvb2slMjBrbm93bGVkZ2UlMjBjb25jZXB0fGVufDB8MHx8fDE3ODg5NDgyMzB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 6.8
adoption_velocity: "MODERATE"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Disposable VM isolation contains AI agent tool execution, preventing lateral movement from host to production systems", "Reproducible VM environments enable consistent security posture across developer workstations", "Full tool access within the sandbox (Docker, git, compilers) reduces pressure to grant host-level privileges to AI agents", "Open-source Rust implementation allows security teams to audit, fork, and extend containment logic"]

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0081 - Modify AI Agent Configuration", "AML.T0083 - Credentials from AI Agent Configuration", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0103 - Deploy AI Agent"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design", "LLM06 - Sensitive Information Disclosure", "LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "Trail of Bits releases Coop, a Rust CLI that runs Claude Code and Codex inside disposable isolated VMs."
tldr_who_at_risk: "Security and platform engineering teams deploying agentic AI coding assistants benefit immediately by eliminating host-level exposure from unrestricted AI tool access."
tldr_actions: ["Evaluate Coop as the default execution environment for any Claude Code or Codex agentic workflows in your developer toolchain", "Review the open-source codebase and SECURITY.md to assess containment boundaries before approving for regulated or sensitive environments", "Establish VM lifecycle and audit log policies before broad rollout to ensure traceability of AI agent actions"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Supply Chain"]
tags: ["agentic-ai", "vm-isolation", "claude-code", "codex", "trail-of-bits", "sandbox", "developer-security", "open-source", "containment", "rust", "ai-tooling"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-09T10:03:50+00:00"
feed_source: "hn_anthropic"
original_url: "https://github.com/trailofbits/coop"
pipeline_version: "2.1.0"
---

## Defender Impact

Agentic AI coding assistants granted full tool access — Docker, git, package managers, compilers — on developer workstations represent an uncontrolled execution surface. Coop directly closes this gap by wrapping that execution inside disposable, isolated virtual machines, giving security teams a repeatable containment boundary that didn't previously exist as a packaged, AI-specific control.

## Capability Overview

Coop is an open-source Rust CLI published by Trail of Bits that provisions and manages lightweight, throwaway virtual machines specifically designed for running Claude Code (Anthropic) and Codex (OpenAI). Within each VM, the AI agent has unrestricted access to the full development toolchain — Docker, git, compilers, package managers — which is precisely the access these agents require to be useful. The key architectural insight is that this access is granted *inside* an isolated, reproducible environment rather than directly against the host machine or shared infrastructure.

Each VM is cheap to create and destroy, making ephemeral-by-default a practical operational model rather than a theoretical aspiration. The project is implemented in Rust, includes a proxy component (`coop-proxy`), fuzzing infrastructure, and a structured release process — markers of engineering maturity that matter when security teams are assessing whether to trust a containment tool.

The tool targets a specific and well-understood pain point: AI coding agents in their current form require broad system permissions to function effectively, and the ecosystem has not yet standardised on how to scope or contain those permissions. Coop is the first purpose-built, open-source answer to that question for the two most widely deployed agentic coding assistants.

## Defensive Advances

**Host isolation by default.** Security teams can now mandate that all Claude Code and Codex sessions run inside a Coop VM, eliminating the class of risks where an AI agent — whether through misinstruction, prompt injection, or tool misuse — modifies, exfiltrates from, or executes against the host system.

**Reproducible security posture.** Because VMs are disposable and templated, every session starts from a known-good baseline. This removes the drift problem common in long-lived developer environments where accumulated state creates unaudited attack surface.

**Reduced privilege pressure.** Developers and platform teams previously faced a binary choice: grant AI agents host-level access or accept severely degraded functionality. Coop dissolves that tradeoff by making full tool access safe inside a disposable boundary.

**Auditable open-source implementation.** Security teams can inspect, fork, and extend the containment logic. The presence of fuzzing infrastructure and a SECURITY.md signals that Trail of Bits has applied its own security engineering discipline to the project.

## Residual Gaps

**Provider coverage is limited.** Coop currently supports Claude Code and Codex. Organisations running GitHub Copilot Workspace, Cursor, or other agentic coding environments will need to wait for community extensions or build their own integration layer.

**Enterprise policy enforcement is immature.** There is no built-in mechanism for centralised policy management — for example, restricting which tools are available within the VM, enforcing network egress rules per team, or integrating with existing privileged access management systems. These are expected maturity gaps for an early open-source release but represent real work before regulated-environment deployment.

**Audit logging is developer-grade, not SOC-grade.** VM lifecycle events and agent actions within the VM are not yet surfaced in a format suitable for ingestion into a SIEM or EDR. Security operations teams will need to build that bridge themselves.

**VM escape is a residual concern.** Isolation quality depends on the underlying hypervisor and host configuration. Teams should assess their hypervisor stack and apply standard VM hardening before treating Coop boundaries as equivalent to production isolation controls.

## Framework Mapping

Coop most directly mitigates **LLM08 (Excessive Agency)** by placing a hard boundary around what AI agents can affect, and **LLM07 (Insecure Plugin Design)** by containing tool execution. From the ATLAS perspective, it reduces the practical impact of **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** and **AML.T0083 (Credentials from AI Agent Configuration)** by ensuring that any successful exploitation is contained within a disposable VM rather than the host.

## Deployment Considerations

Organisations should treat Coop adoption as a two-phase exercise. In phase one, use it as a developer-opt-in tool to gather operational experience with VM lifecycle, performance impact, and toolchain compatibility. In phase two, work with platform engineering to make Coop-wrapped execution the mandatory path for agentic AI coding sessions, integrating VM creation events into existing audit pipelines.

Prerequisite decisions include: which hypervisor stack is approved, what the network egress policy inside VMs should be, and whether VM images will be centrally maintained or developer-managed.

## Defender Checklist

- [ ] Review the Coop repository and SECURITY.md before approving for any environment handling sensitive code
- [ ] Test VM lifecycle performance against representative developer workflows to validate operational viability
- [ ] Define a VM base image hardening standard (egress rules, filesystem mounts, credential access)
- [ ] Identify a SIEM integration path for VM creation, session, and destruction events
- [ ] Establish a policy decision: developer-optional vs. mandatory enforcement for AI coding agent sessions
- [ ] Monitor the Coop issue tracker for provider expansion and enterprise feature development

## References

- [trailofbits/coop — GitHub](https://github.com/trailofbits/coop)
