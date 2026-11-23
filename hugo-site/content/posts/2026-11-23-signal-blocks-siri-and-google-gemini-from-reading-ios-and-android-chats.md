---
title: "Signal Blocks Siri and Google Gemini from Reading iOS and Android Chats"
date: 2026-11-23T16:20:43+00:00
draft: false
slug: "signal-blocks-siri-and-google-gemini-from-reading-ios-and-android-chats"

# ── Content metadata ──
summary: "Signal has introduced OS-level protections that prevent Siri on iOS 27 and Google Gemini on Android from capturing on-screen conversation content, extending a defensive approach first deployed against Microsoft Recall in May 2025. This closes a meaningful gap for organisations relying on Signal for sensitive communications by restricting agentic AI assistants \u2014 embedded deep in mobile operating systems \u2014 from exfiltrating private message content outside the app's control boundary. Residual coverage gaps remain on macOS, where Signal cannot yet enforce screenshot blocking, and Signal itself acknowledges that undiscovered AI access pathways may still exist across all platforms."
source: "BleepingComputer"
source_url: "https://www.bleepingcomputer.com/news/security/signal-to-block-siri-gemini-ai-from-capturing-chats-on-ios-android"
source_title: "Signal to block Siri, Gemini AI from capturing chats on iOS, Android"
source_date: 2026-11-22T15:15:25+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1782926016946-3d12dfb649a4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxM3x8R29vZ2xlJTIwc2VhcmNoJTIwZXhwbG9yZSUyMGRpc2NvdmVyeSUyMGFic3RyYWN0fGVufDB8MHx8fDE3OTU0NTA4NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── First Look: Capability Assessment ──
content_type: "first_look"
attack_surface_score: 7.0
adoption_velocity: "RAPID"
capability_category: "safety-mechanism"
attack_vectors_introduced: ["App-level screen-read blocking prevents OS-embedded AI assistants (Siri, Gemini) from ingesting sensitive conversation content displayed on-screen", "Reverse-engineered pathway analysis closes verified AI data extraction channels without requiring OS vendor cooperation", "Automatic activation on eligible devices reduces reliance on user configuration to enforce privacy controls", "Public opt-out guidance for macOS gives security teams an interim compensating control while platform-level protection matures"]

# ── AI Security Classification ──
relevance_score: 7.2
threat_level: "MEDIUM"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0057 - LLM Data Leakage", "AML.T0086 - Exfiltration via AI Agent Tool Invocation", "AML.T0063 - Discover AI Model Outputs", "AML.T0084 - Discover AI Agent Configuration"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM06 - Sensitive Information Disclosure", "LLM08 - Excessive Agency", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Signal now blocks Siri and Google Gemini from reading on-screen chat content on iOS 27 and Android."
tldr_who_at_risk: "Security-conscious individuals and organisations using Signal for sensitive communications benefit directly, closing an OS-level AI data leakage gap."
tldr_actions: ["Update Signal to the latest available version on all iOS and Android devices to activate protections automatically", "For macOS users, immediately add Signal to the Excluded Apps list under System Settings > Siri as an interim control", "Review your mobile device management (MDM) policy to enforce Signal updates and audit which AI assistant features have screen-access permissions"]

# ── Taxonomies ──
categories: ["First Look", "Agentic AI", "LLM Security", "Industry News"]
tags: ["signal", "siri", "google-gemini", "ios", "android", "agentic-ai", "on-device-ai", "screen-capture", "mobile-security", "privacy", "data-leakage", "os-embedded-ai", "meredith-whittaker"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["nation-state", "insider", "cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-11-23T16:20:43+00:00"
feed_source: "bleepingcomputer"
original_url: "https://www.bleepingcomputer.com/news/security/signal-to-block-siri-gemini-ai-from-capturing-chats-on-ios-android"
pipeline_version: "2.1.0"
content_hash: "044f866c6a4f6484"
---

## Defender Impact

Signal's new OS-level protections against Siri and Google Gemini represent a concrete step toward containing the data leakage surface introduced by agentic AI assistants embedded in mobile operating systems. For security teams managing communications hygiene across iOS and Android fleets, this closes a gap that previously had no app-level remedy.

## Capability Overview

Signal has extended its AI screen-capture blocking — first deployed against Microsoft Recall in May 2025 — to cover Siri's Onscreen Awareness on iOS 27 and Gemini Intelligence on supported Android versions. These OS-embedded AI features are designed to read on-screen content to assist users contextually, but that capability introduces an uncontrolled exfiltration pathway for sensitive conversations displayed in Signal.

Signal's engineering team reverse-engineered the access mechanisms these AI assistants use to read app screen content, then designed targeted blocks across all verified extraction pathways. The protections are automatically activated on eligible devices when users upgrade to the latest Signal release — no manual toggle is required in most cases. For iOS, Signal also surfaces a user-facing toggle to explicitly block Siri scanning, providing a visible control that security teams and end users alike can verify.

Signal president Meredith Whittaker framed the broader issue as an architectural problem: AI agents are now embedded so deeply in operating systems that app developers have limited visibility into all the ways those agents may access in-app data. Signal's response — reverse engineering access pathways and blocking them — is a pragmatic defensive posture taken in the absence of formal OS vendor disclosure or opt-out APIs.

## Defensive Advances

This capability gives defenders several concrete new tools:

- **Closed verified exfiltration pathways**: Security teams can now deploy Signal on iOS 27 and Android with confidence that Siri and Gemini cannot passively ingest conversation content through screen-read mechanisms Signal has identified.
- **Automatic enforcement at scale**: Because protections activate on upgrade without user action, MDM-managed fleets benefit from the control simply by enforcing Signal version currency — a manageable operational lift.
- **Visible user control on iOS**: The explicit Siri-blocking toggle gives security-conscious users and administrators an auditable, inspectable control state rather than a silent background enforcement.
- **Interim macOS guidance**: While platform-level protection is unavailable on macOS, Signal's published guidance to use the Excluded Apps list gives security teams a documented compensating control they can include in hardening baselines today.

## Residual Gaps

Several maturity limitations constrain the full benefit of this capability at present:

- **macOS coverage is absent**: Signal explicitly cannot enforce screenshot blocking on macOS 27, and the recommended workaround (Excluded Apps) depends on user action and trust in Apple's configuration enforcement — neither of which is reliable at enterprise scale.
- **Undiscovered pathways remain unknown**: Signal's protections cover pathways verified through reverse engineering, but Whittaker's own framing acknowledges that additional access mechanisms may exist and have not yet been identified. The protective boundary is defined by what Signal's team has found, not by what exists.
- **No formal OS vendor API**: The absence of a standardised opt-out mechanism from Apple and Google means Signal's protections are inherently reactive — each new OS version or AI feature update may require a new round of reverse engineering before coverage is restored.
- **Android version fragmentation**: Protections apply only to Android versions where Signal can detect an AI assistant attempting screen access. Older or heavily customised Android builds may not benefit.

## Framework Mapping

This capability most directly addresses **AML.T0057 (LLM Data Leakage)** and **AML.T0086 (Exfiltration via AI Agent Tool Invocation)** by blocking the mechanism through which an OS-embedded AI agent would read and potentially retain conversation content. It also reduces exposure under **LLM06 (Sensitive Information Disclosure)** and **LLM08 (Excessive Agency)**, where AI assistants operating with broad OS permissions represent an unconstrained agency surface.

## Deployment Considerations

Organisations managing Signal deployments through MDM should prioritise version currency as the primary control lever — automatic protections only activate on the latest release. iOS deployments should verify the Siri-blocking toggle state through any available MDM inspection capability. macOS should be treated as an unprotected surface for Signal communications until Apple provides a formal opt-out API, with the Excluded Apps workaround enforced through endpoint configuration management where possible. Security teams should track Signal's public communications for new pathway discoveries as the OS AI ecosystem matures.

## Defender Checklist

- [ ] Enforce latest Signal version across all iOS and Android devices via MDM
- [ ] Verify Siri-blocking toggle is active on iOS 27 Signal installations
- [ ] Add Signal to macOS System Settings > Siri > Excluded Apps on all macOS endpoints as an interim control
- [ ] Include Signal AI-blocking status in mobile hardening baselines and audit cadence
- [ ] Monitor Signal's official blog for updates on newly identified AI access pathways
- [ ] Formally request Apple, Google, and Microsoft publish AI screen-access opt-out APIs through enterprise feedback channels

## References

- [Signal announcement — BleepingComputer coverage](https://www.bleepingcomputer.com/news/security/signal-to-block-siri-gemini-ai-from-capturing-chats-on-ios-android)
