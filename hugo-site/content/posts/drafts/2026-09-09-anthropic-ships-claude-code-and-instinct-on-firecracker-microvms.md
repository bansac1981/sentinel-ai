---
title: "Anthropic Ships Claude Code and Instinct on Firecracker MicroVMs"
date: 2026-09-09T10:02:09+00:00
draft: true
slug: "anthropic-ships-claude-code-and-instinct-on-firecracker-microvms"

# ── Content metadata ──
summary: "Anthropic's Claude Code and the Instinct agent platform now run inside vendor-managed Firecracker microVMs, giving each user session a hardware-isolated kernel with split read/write disk partitions, a non-dumpable Rust PID 1, and a 443-only egress gateway with TLS inspection. This architecture closes a meaningful gap for defenders by moving agentic workloads off unmanaged developer laptops and into auditable, tenant-isolated compute with enforced egress controls and per-boot OAuth rotation. Residual gaps remain around egress policy granularity, third-party sandbox supply chain visibility (particularly for Instinct's E2B dependency), and the absence of standardised security attestation that enterprise security teams can consume programmatically."
source: "Anthropic (via HN)"
source_url: "https://rohanadwankar.github.io/posts/platforms.html"
source_title: "The VMs Powering Mobile Agents (Instinct, Claude Code)"
source_date: 2026-09-08T04:36:26+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.pexels.com/photos/8326305/pexels-photo-8326305.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 5.8
adoption_velocity: "MODERATE"
capability_category: "agent-tooling"
attack_vectors_introduced: ["Tenant-isolated Firecracker microVM per session closes lateral-movement risk between concurrent agent sessions on shared infrastructure", "Read-only vendor disk partitions (vdc/vdd/vde/vdf) prevent agent harness tampering at the filesystem layer", "443-only egress gateway with TLS interception provides a chokepoint for monitoring and blocking agent-initiated data exfiltration", "Per-boot OAuth token rotation with root-only caching limits credential reuse window if a session is compromised", "Non-dumpable PID 1 with denied /proc/1/mem access reduces operator-process inspection from within the tenant namespace", "Persistent-disk/ephemeral-compute split (vda survives reclaim) enables forensic continuity of agent work artefacts across session boundaries"]

# ── AI Security Classification ──
relevance_score: 6.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0081 - Modify AI Agent Configuration", "AML.T0010 - AI Supply Chain Compromise", "AML.T0069 - Discover LLM System Information"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM05 - Supply Chain Vulnerabilities", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Anthropic's Claude Code and Instinct agents now run in vendor-managed Firecracker microVMs with enforced egress and tenant isolation."
tldr_who_at_risk: "Security teams deploying agentic AI workloads benefit from hardware-level session isolation and auditable egress controls replacing unmanaged developer endpoints."
tldr_actions: ["Audit egress gateway logs from the 443-only MITM chokepoint for anomalous agent-initiated outbound patterns", "Validate per-boot OAuth token rotation policies align with your credential lifecycle requirements before enterprise rollout", "Assess E2B supply chain trust for Instinct deployments — confirm sandbox image provenance and update cadence with the vendor"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Supply Chain"]
tags: ["claude-code", "firecracker", "microvm", "agentic-ai", "sandbox-isolation", "egress-control", "e2b", "anthropic", "mobile-agents", "tenant-isolation", "oauth-rotation", "vsock"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["insider", "cybercriminal", "researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-09-09T10:02:09+00:00"
feed_source: "hn_anthropic"
original_url: "https://rohanadwankar.github.io/posts/platforms.html"
pipeline_version: "2.1.0"
---

## Defender Impact

Moving agentic workloads off developer laptops and into vendor-managed, hardware-isolated microVMs is a genuine step forward for defenders. It replaces an uncontrolled, heterogeneous endpoint surface with a reproducible, auditable compute boundary that security teams can reason about systematically.

## Capability Overview

Both Claude Code (Anthropic) and Instinct now provision a dedicated Firecracker microVM per user session rather than running inside a shared process on the user's local machine. Firecracker is a KVM-based microVM monitor originally built by AWS for Lambda and Fargate; it provides a full guest kernel in roughly 125 ms with a minimal attack surface by design.

**Claude Code architecture:** Each session gets its own kernel (Linux 6.18.5 with a custom `-fc-` build), a non-systemd PID 1 (`process_api`, a Rust/Tokio binary), and a clean disk split — one writable persistent volume (`vda`, 256 GB) owned by the tenant, and multiple read-only vendor volumes carrying the 324 MB Bun-compiled claude harness, a task launcher, and skills overlays. Inference traffic leaves exclusively over HTTPS/2 SSE to `/v1/messages` through a TLS-intercepting egress gateway pinned to `api.anthropic.com`. There is no inbound networking surface whatsoever — the RFC-5737 address `192.0.2.2` is a documentation range, confirming no reachable listener. Host control uses vsock (port 2024), a hypervisor-mediated channel that does not traverse the guest network stack. Auth is a host-minted OAuth token, root-only, rotated per boot.

**Instinct architecture:** Instinct rents E2B sandboxes rather than operating its own fleet. The resulting environment is a throwaway Ubuntu 22.04 KVM guest (2 vCPU, 1.9 GB RAM, 29 GB disk, ~30-minute lifetime) with standard systemd as PID 1. Firecracker fingerprints are present (`pci=off`, virtio-MMIO, absent SMBIOS, `tap0` networking), indicating E2B itself uses Firecracker under the hood. The security posture here is more permissive than Claude Code's hardened configuration, reflecting E2B's general-purpose sandbox-as-a-service design.

## Defensive Advances

**Session-level blast radius containment.** Hardware VM boundaries mean a compromised agent session cannot traverse to adjacent sessions through shared memory, process namespace, or filesystem paths. This is a concrete improvement over process-isolated or container-isolated alternatives.

**Auditable egress chokepoint.** The 443-only MITM egress gateway gives defenders a single, well-defined inspection surface for all agent-initiated outbound traffic. Security teams operating SIEM pipelines or CASB solutions can instrument this chokepoint to detect anomalous exfiltration patterns from agent tool invocations.

**Reduced credential reuse window.** Per-boot OAuth token rotation with root-only disk caching means the effective credential lifetime is bounded by VM uptime. Idle reclaim (host-driven, not agent-driven) further limits exposure.

**Persistent forensic artefacts.** The `vda` volume survives compute reclaim and reattaches on cold boot. This gives incident responders access to agent work artefacts — command history, intermediate files, tool outputs — even after the compute layer has been destroyed, which is a meaningful forensic improvement over purely ephemeral sandboxes.

**Operator process hardening.** The non-dumpable PID 1 and denied `/proc/1/mem` access reduce the ability of malicious agent code to inspect or manipulate the platform's own control process from within the tenant namespace.

## Residual Gaps

**Egress policy granularity.** A 443-only gateway is a good baseline, but it is not destination-filtered. Defenders operating in regulated environments will need to determine whether the platform supports allowlisting specific egress destinations beyond `api.anthropic.com`, or whether MITM log export is available for SIEM integration.

**E2B supply chain visibility.** Instinct's dependency on E2B introduces a third-party in the trust chain. The base Ubuntu image's update cadence, kernel patch policy, and security attestation practices are not surfaced in Instinct's own documentation. Organisations should request this information before enterprise adoption.

**No standardised attestation artefact.** Neither platform currently publishes a machine-readable security attestation (e.g., SLSA provenance, TPM-backed remote attestation) that enterprise procurement or security review processes can consume. This is a maturity gap that limits integration with zero-trust tooling.

**Instinct session lifetime.** The ~30-minute E2B sandbox lifetime may not suit longer-running agentic workflows, and the ephemeral-only disk model (no equivalent of Claude Code's persistent `vda`) limits forensic continuity for Instinct deployments.

## Framework Mapping

- **AML.T0086 (Exfiltration via AI Agent Tool Invocation):** The 443-only MITM egress gateway directly addresses this by providing a monitored chokepoint for all agent-initiated outbound traffic.
- **AML.T0083/T0084 (Credentials/Config Discovery from Agent):** Per-boot token rotation and non-dumpable PID 1 reduce the viability of credential harvesting from within the agent's runtime environment.
- **AML.T0010 (AI Supply Chain Compromise):** Read-only vendor disk partitions prevent runtime modification of the agent harness; the E2B dependency remains a supply chain consideration for Instinct.
- **LLM08 (Excessive Agency):** VM-level isolation bounds the blast radius of an agent acting outside intended scope.
- **LLM05 (Supply Chain Vulnerabilities):** E2B as an infrastructure dependency warrants supply chain due diligence.

## Deployment Considerations

Organisations evaluating Claude Code or Instinct for enterprise agentic workflows should sequence their assessment as follows. First, confirm egress gateway log export capabilities with the vendor before signing agreements — this is the primary security telemetry surface. Second, map the persistent `vda` volume (Claude Code) retention and deletion policies to your data classification requirements. Third, for Instinct, engage E2B directly on sandbox image provenance and kernel patch SLAs before treating it as production infrastructure. Finally, consider whether your CASB or network monitoring tooling can consume TLS inspection logs from a vendor-operated gateway, or whether you need to replicate this control at your perimeter.

## Defender Checklist

- [ ] Confirm egress gateway log format and export options with Anthropic before production deployment
- [ ] Review `vda` volume data retention, encryption-at-rest, and deletion guarantee documentation
- [ ] Request E2B sandbox image SBOM and kernel patch cadence for Instinct deployments
- [ ] Instrument SIEM to alert on unexpected egress volume patterns from agent session traffic
- [ ] Validate per-boot OAuth token rotation aligns with organisational credential lifecycle policies
- [ ] Test idle-reclaim behaviour to confirm `vda` persistence across session boundaries in your environment
- [ ] Assess whether the 30-minute Instinct sandbox lifetime is compatible with your intended agentic use cases

## References

- Rohan Adwankar, "The box an agent runs in": https://rohanadwankar.github.io/posts/platforms.html
