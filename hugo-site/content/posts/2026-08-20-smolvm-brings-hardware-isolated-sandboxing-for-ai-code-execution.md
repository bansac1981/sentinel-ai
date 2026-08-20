---
title: "smolvm Brings Hardware-Isolated Sandboxing for AI Code Execution"
date: "2026-08-20T08:40:09+00:00"
draft: false
slug: "smolvm-brings-hardware-isolated-sandboxing-for-ai-code-execution"

# ── Content metadata ──
summary: "smolmachines/smolvm 1.8.3 provides hardware-isolated VM sandboxing for untrusted Python and JavaScript, with enforced CPU/RAM limits, no-network execution, filesystem quotas, and cold starts under 1.5 seconds. For defenders building AI platforms that execute user-supplied or LLM-generated code, this closes the critical gap between shared-kernel container isolation and true VM-level isolation for data transformation workloads. Residual maturity questions remain around orchestration integration, audit logging depth, and the KVM dependency that excludes nested-virtualisation environments like many CI and cloud agent runtimes."
source: "Simon Willison"
source_url: "https://simonwillison.net/2026/Aug/19/smolmachines-untrusted-sandbox"
source_title: "smolmachines / smolvm as a sandbox for untrusted Python & JavaScript"
source_date: 2026-08-19T23:16:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1614064548306-51cd89c21764?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyNHx8Rmlyc3QlMjBMb29rJTIwY3liZXJzZWN1cml0eSUyMHRlY2hub2xvZ3l8ZW58MHwwfHx8MTc4NzIxMTQ1M3ww&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 5.5
adoption_velocity: "GRADUAL"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["Hardware-isolated VM execution boundary prevents LLM-generated or user-supplied code from escaping to the host via kernel exploits", "Enforced CPU and RAM quotas with guest-side timeouts mitigate denial-of-service from infinite loops or memory exhaustion in agentic code execution pipelines", "No-network execution mode prevents exfiltration or callback beaconing from sandboxed code at the infrastructure layer", "Read-only input mounts and writable output mounts enforce least-privilege filesystem access for AI data transformation tasks", "Offline local images eliminate supply chain fetch risk at execution time by removing runtime registry dependencies"]

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "LOW"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0110 - AI Agent Tool Poisoning", "AML.T0047 - AI-Enabled Product or Service", "AML.T0103 - Deploy AI Agent"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM02 - Insecure Output Handling", "LLM04 - Model Denial of Service", "LLM07 - Insecure Plugin Design", "LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "smolvm 1.8.3 delivers hardware-isolated VM sandboxing for untrusted Python and JavaScript with sub-1.5s cold starts."
tldr_who_at_risk: "Platform and security engineers building AI systems that execute user-supplied or LLM-generated code benefit directly, closing the shared-kernel isolation gap."
tldr_actions: ["Evaluate smolvm against your existing container-based code execution controls to assess whether hardware isolation is warranted for your threat model", "Audit all agentic pipelines that execute LLM-generated code and identify which lack CPU, RAM, network, and filesystem enforcement", "Validate KVM availability in your target deployment environments before committing to smolvm — nested-virtualisation constraints may require infrastructure changes"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Research"]
tags: ["sandboxing", "code-execution", "agentic-ai", "smolvm", "smolmachines", "hardware-isolation", "untrusted-code", "python", "javascript", "firecracker", "kvm", "claude-fable", "data-transformation", "resource-limits"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-20T07:37:33+00:00"
feed_source: "simonwillison"
original_url: "https://simonwillison.net/2026/Aug/19/smolmachines-untrusted-sandbox"
pipeline_version: "2.1.0"
---

## Defender Impact

AI platforms that allow users or agents to submit code for execution have long relied on shared-kernel containers as their primary isolation boundary — a control that does not hold against kernel-level escapes or resource exhaustion at scale. smolmachines/smolvm 1.8.3 offers a practically accessible hardware VM isolation layer with enforced resource limits and network isolation, closing a meaningful gap for teams building LLM-powered data transformation pipelines.

## Capability Overview

smolvm is a lightweight VM orchestration tool built on KVM hardware virtualisation (the same hypervisor primitive used by Firecracker, which underpins AWS Lambda). Simon Willison's evaluation of version 1.8.3 tested it specifically for the pattern of executing untrusted Python and JavaScript in the context of AI agent workflows — a growing surface as LLMs are increasingly tasked with generating and running transformation logic on behalf of users.

The tested capability set includes: offline local images (no runtime registry fetch), no-network execution mode, per-VM CPU and RAM quotas, guest-enforced timeouts (protecting against infinite loops), storage quotas, read-only input mounts, writable output mounts, and an `--unprivileged` flag. Cold start latency measured at 0.6–1.5 seconds, with warm executions around 50 ms — performance characteristics that make it viable for interactive or near-real-time agent tooling.

Notably, the evaluation itself was conducted by Claude Fable 5 running in Claude Code for web, which discovered that its own environment (a Firecracker guest without /dev/kvm) could not run nested VMs. It autonomously pivoted to GitHub Actions runners that expose /dev/kvm and ran the full test battery there — a useful illustration of how capable agents navigate environmental constraints, and a reminder that agentic execution environments have their own infrastructure dependencies that must be mapped.

## Defensive Advances

For defenders, smolvm moves the isolation boundary from shared kernel (container) to hardware hypervisor (VM), which is a qualitative step up in containment assurance for code execution workloads. Concretely, security teams can now:

- **Enforce hard resource ceilings** on LLM-generated or user-supplied code at the infrastructure layer, not just the application layer, eliminating denial-of-service via CPU spin or memory exhaustion
- **Block exfiltration at execution time** by running sandboxed code with no network access — preventing callback beaconing or data exfiltration from compromised or malicious transformation scripts
- **Restrict filesystem blast radius** through read-only input and writable-only output mount semantics, enforcing least-privilege data access for agentic tasks
- **Remove runtime supply chain exposure** by using offline local images, ensuring that the sandboxed environment is fixed at build time and not subject to registry tampering at execution

This tooling is particularly relevant to LLM08 (Excessive Agency) and LLM07 (Insecure Plugin Design) scenarios, where an agent executing code tools without hard infrastructure limits represents an unacceptable residual risk.

## Residual Gaps

Several maturity questions remain before this capability is production-ready for most organisations:

- **KVM dependency**: smolvm requires hardware virtualisation support, which is unavailable in many nested-virtualisation environments — including the Claude Code container used in this very evaluation. Teams running agents on managed cloud runtimes or serverless platforms will need to validate KVM availability or restructure their deployment topology.
- **Audit and observability**: The evaluation does not address what logging and syscall-level audit output smolvm produces. For security operations, visibility into what code ran and what it attempted is as important as containment.
- **Orchestration integration**: Integrating smolvm into existing agentic frameworks (LangChain, AutoGen, custom tool routers) requires engineering work to wrap the VM lifecycle around tool invocation — there is no documented out-of-the-box connector.
- **Image governance**: Offline local images eliminate runtime fetch risk but introduce an image build and distribution pipeline that must itself be secured and kept current.

## Framework Mapping

- **AML.T0086 (Exfiltration via AI Agent Tool Invocation)**: No-network execution directly constrains this technique at the infrastructure layer
- **AML.T0110 (AI Agent Tool Poisoning)**: Read-only input mounts limit what a compromised tool can write to the host environment
- **LLM04 (Model Denial of Service)**: CPU/RAM quotas and guest timeouts address resource exhaustion from generated code
- **LLM08 (Excessive Agency)**: Hardware isolation enforces a hard boundary on what an agent's code execution tool can affect

## Deployment Considerations

Organisations should begin by auditing which of their agentic pipelines execute LLM-generated or user-submitted code today and what isolation controls are in place. Where shared-kernel containers are the current boundary, smolvm warrants a threat-model-driven evaluation. Prioritise deployments where code executes against sensitive data or where multi-tenant workloads share infrastructure.

Verify KVM availability in target environments early — this is the most likely deployment blocker. GitHub Actions ubuntu runners are confirmed viable; most managed Kubernetes environments require validation.

## Defender Checklist

- [ ] Inventory all code execution surfaces in agentic pipelines and document current isolation controls
- [ ] Confirm /dev/kvm availability in target deployment environments
- [ ] Test smolvm cold start latency against your SLA requirements for interactive agent tools
- [ ] Define image build and governance pipeline for smolvm local images
- [ ] Validate no-network mode does not break legitimate tool dependencies before rollout
- [ ] Instrument VM lifecycle events for audit logging and integrate with SIEM
- [ ] Document resource limit thresholds (CPU, RAM, timeout) based on expected transformation workload profiles

## References

- [smolmachines / smolvm as a sandbox for untrusted Python & JavaScript — Simon Willison](https://simonwillison.net/2026/Aug/19/smolmachines-untrusted-sandbox)
