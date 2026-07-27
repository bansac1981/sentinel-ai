---
title: "Kimi K3 AI Agents Discover Redis RCE Zero-Days via RESTORE"
date: 2026-07-27T08:22:32+00:00
draft: true
slug: "kimi-k3-ai-agents-discover-redis-rce-zero-days-via-restore"

# ── Content metadata ──
summary: "Researchers using Kimi K3 AI agents discovered multiple zero-day vulnerabilities in Redis, leading to authenticated remote code execution proof-of-concept exploits across four major Redis versions. The flaws span two distinct exploitation paths: a use-after-free in Redis Streams and an out-of-bounds write in the RedisBloom TDigest RDB loader. This incident marks a significant milestone in AI-assisted offensive security research, demonstrating that autonomous AI agents can independently discover and weaponise critical infrastructure vulnerabilities."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/07/kimi-k3-agents-found-redis-zero-days.html"
source_title: "Kimi K3 Agents Found Redis Zero-Days and Built RCE Exploit, Researchers Say"
source_date: 2026-07-24T06:58:27+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1607601191544-fd61c99dd3c9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwyOXx8bWVjaGFuaWNhbCUyMGdlYXJzJTIwaW50ZXJsb2NraW5nJTIwbWFjaGluZXxlbnwwfDB8fHwxNzg1MDYzMDA4fDA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 6.5
threat_level: "CRITICAL"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0047 - ML-Enabled Product or Service", "AML.T0043 - Craft Adversarial Data"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM08 - Excessive Agency"]

# ── TL;DR ──
tldr_what: "Kimi K3 AI agents autonomously found Redis zero-days and built working RCE exploits."
tldr_who_at_risk: "Any organisation running Redis 6.2.22, 7.4.9, 8.6.4, or 8.8.0 with RESTORE command access exposed to untrusted networks."
tldr_actions: ["Upgrade to the patched Redis release for your deployed branch immediately", "Revoke RESTORE command permissions from all accounts that do not strictly require it", "Block untrusted network access to Redis instances at the firewall level"]

# ── Taxonomies ──
categories: ["Agentic AI", "Research", "Industry News"]
tags: ["redis", "zero-day", "rce", "kimi-k3", "ai-agents", "use-after-free", "out-of-bounds-write", "redisbloom", "tdigest", "agentic-security-research", "exploit-development", "autonomous-agents"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["researcher"]

# ── Pipeline metadata ──
fetched_at: "2026-07-27T08:22:32+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/07/kimi-k3-agents-found-redis-zero-days.html"
pipeline_version: "2.1.0"
---

## Overview

On July 23, 2026, Redis shipped seven security releases after researchers — using Kimi K3 AI agents — published authenticated remote code execution (RCE) proof-of-concept exploits targeting Redis 6.2.22, 7.4.9, 8.6.4, and 8.8.0. The disclosure is notable not only for the severity of the underlying vulnerabilities, but because the discovery and exploit-development process was reportedly driven by autonomous AI agents, marking a significant escalation in the practical offensive capability of agentic AI systems.

## Technical Analysis

Two distinct exploitation chains were disclosed:

**Path 1 — Redis Streams Shared-NACK Use-After-Free**

A corrupt RDB object can cause two consumers to reference the same `streamNACK` pending-entry record. Removing the first consumer frees the object; the second consumer retains a dangling pointer. Removing the second consumer triggers a double-free. The published PoC script converts this memory corruption into arbitrary memory access, poisons a database hash function, and crafts a `GET` command invocation of `system()`. This affects Redis 6.2.22 and 7.4.9 — ironically, the May 2026 security updates Redis had previously advised users to install. The fix (a duplicate-ownership guard) was absent from 8.6.4 despite release notes citing the relevant PR; it only landed in 8.6.5.

**Path 2 — RedisBloom TDigest RDB Loader Out-of-Bounds Write**

The TDigest RDB loader allocates centroid arrays based on a serialized compression value but trusts a separate attacker-controlled `capacity` field to determine how many nodes to load. A small real allocation paired with inflated metadata produces an out-of-bounds write. The 8.8.0 PoC leverages this to establish read/write primitives, leak Redis and libc addresses, and ultimately call `system()`. Both chains require the `RESTORE` command; the Streams chains additionally require `EVAL` and `XGROUP`; the 8.8.0 chain requires `EVAL` and the bundled RedisBloom module.

## Framework Mapping

**MITRE ATLAS — AML.T0047 (ML-Enabled Product or Service):** Kimi K3 agents were deployed as an offensive security tool, demonstrating how ML-enabled services can autonomously perform complex vulnerability research and exploit development — a capability previously requiring significant human expertise.

**MITRE ATLAS — AML.T0043 (Craft Adversarial Data):** The exploits rely on crafting malicious RDB objects to corrupt internal Redis data structures, analogous to crafting adversarial inputs to subvert a system's expected behaviour.

**OWASP LLM08 (Excessive Agency):** The incident illustrates the dual-use risk of agentic AI systems operating with broad tool access — the same autonomous capability that benefits defenders can independently discover and weaponise vulnerabilities at machine speed.

## Impact Assessment

All four targeted Redis versions were in active production use at the time of disclosure. Redis 6.2.22 and 7.4.9 were the most recently recommended security releases, meaning many operators who followed Redis's own guidance remained exposed. No in-the-wild exploitation had been confirmed as of July 24, 2026, but the public availability of working PoCs significantly compresses the window before opportunistic exploitation. Organisations using Redis with default or overly permissive command ACLs are most immediately at risk.

## Mitigation & Recommendations

- **Upgrade immediately** to the patched release for your branch: Redis 6.2.23, 7.2.15, 7.4.10, 8.2.8, 8.4.5, 8.6.5, or 8.8.1.
- **Revoke RESTORE** from any account that does not strictly require it — this single step blocks both disclosed exploitation paths.
- **Restrict network access** to Redis instances; block untrusted inbound connections at the network perimeter.
- **Audit ACL configurations** to ensure `EVAL` and `XGROUP` are similarly restricted to trusted principals.
- **Monitor for anomalous RESTORE usage** in Redis logs as a detection signal.

## References

- [The Hacker News — Kimi K3 Agents Found Redis Zero-Days and Built RCE Exploit](https://thehackernews.com/2026/07/kimi-k3-agents-found-redis-zero-days.html)
