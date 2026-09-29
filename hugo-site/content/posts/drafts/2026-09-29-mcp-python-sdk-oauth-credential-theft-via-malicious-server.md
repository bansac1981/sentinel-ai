---
title: "MCP Python SDK OAuth Credential Theft via Malicious Server"
date: 2026-09-29T10:52:50+00:00
draft: true
slug: "mcp-python-sdk-oauth-credential-theft-via-malicious-server"

# ── Content metadata ──
summary: "A high-severity vulnerability in the official MCP Python SDK allowed malicious servers to redirect OAuth credential exchanges\u2014including client secrets, authorization codes, and PKCE proof keys\u2014to attacker-controlled endpoints. The flaw affects HTTP-based MCP clients using any of four OAuth provider classes across SDK versions 1.9.1\u20131.29.1 and 2.0.0\u20132.1.1. Patches are available in versions 1.30.0 and 2.2.0, though machine-to-machine provider users require additional remediation steps beyond upgrading."
source: "The Hacker News"
source_url: "https://thehackernews.com/2026/09/official-mcp-python-sdk-flaw-can-let.html"
source_title: "Official MCP Python SDK Flaw Can Let Malicious Servers Steal OAuth Credentials"
source_date: 2026-09-29T06:08:25+00:00
author: "Grid the Grey Editorial"
thumbnail: "https://images.unsplash.com/photo-1784456797970-5d0b529719ca?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5Mzc1ODZ8MHwxfHNlYXJjaHwxOXx8ZG9vciUyMGhhbmRsZSUyMGVudHJhbmNlJTIwYXJjaGl0ZWN0dXJlfGVufDB8MHx8fDE3OTA2NzkxNzB8MA&ixlib=rb-4.1.0&q=80&w=1080"
# To override: find a photo on unsplash.com or pexels.com, copy image URL, paste above

# ── Content Type ──
content_type: "threat_report"

# ── AI Security Classification ──
relevance_score: 8.5
threat_level: "HIGH"

# ── MITRE ATLAS Techniques ──
mitre_techniques: ["AML.T0083 - Credentials from AI Agent Configuration", "AML.T0098 - AI Agent Tool Credential Harvesting", "AML.T0081 - Modify AI Agent Configuration", "AML.T0084 - Discover AI Agent Configuration", "AML.T0010 - AI Supply Chain Compromise", "AML.T0012 - Valid Accounts"]

# ── OWASP LLM Top 10 ──
owasp_categories: ["LLM05 - Supply Chain Vulnerabilities", "LLM06 - Sensitive Information Disclosure", "LLM07 - Insecure Plugin Design"]

# ── TL;DR ──
tldr_what: "Malicious MCP servers can steal OAuth credentials from vulnerable SDK clients via spoofed authorization server responses."
tldr_who_at_risk: "Developers using MCP Python SDK as an HTTP client with OAuthClientProvider or machine-to-machine OAuth providers connecting to untrusted servers."
tldr_actions: ["Upgrade MCP Python SDK to 1.30.0 (1.x line) or 2.2.0 (2.x line) immediately", "Rotate client secrets if ClientCredentialsOAuthProvider or PrivateKeyJWTOAuthProvider were used", "Audit all MCP client deployments to confirm they only connect to fully trusted servers"]

# ── Taxonomies ──
categories: ["Agentic AI", "Supply Chain", "LLM Security"]
tags: ["mcp", "oauth", "credential-theft", "python-sdk", "pkce-bypass", "ai-agent-security", "model-context-protocol", "authorization-server-spoofing", "cycode", "client-secret-exposure"]
frameworks: ["mitre-atlas", "owasp-llm"]
threat_actors: ["cybercriminal"]

# ── Pipeline metadata ──
fetched_at: "2026-09-29T10:52:50+00:00"
feed_source: "thehackernews"
original_url: "https://thehackernews.com/2026/09/official-mcp-python-sdk-flaw-can-let.html"
pipeline_version: "2.1.0"
---

## Overview

A high-severity flaw in the official MCP Python SDK—the reference implementation for Anthropic's Model Context Protocol—allowed malicious MCP servers to intercept and steal the OAuth credentials used by client applications to authenticate with legitimate services. Discovered and responsibly disclosed by Cycode, the vulnerability affects all HTTP-based MCP clients relying on four OAuth provider classes across a wide range of SDK versions. Patches were released on 29 September 2026.

## Technical Analysis

The vulnerability exploits the trust an MCP client places in the server it connects to when discovering its authorization server. During the OAuth flow, the client queries the connected MCP server for the location of the authorization server. In affected versions, the SDK failed to validate this response before proceeding with the credential exchange.

An attacker controlling or compromising an MCP server can exploit this in two ways:

1. **Direct redirection**: The malicious server names an attacker-controlled endpoint as the authorization server.
2. **Split-trust attack**: The server advertises the legitimate authorization server for the user-facing login page but routes the actual token exchange—including the client secret, authorization code, and PKCE proof key—to an attacker endpoint.

In both cases, the client sends its full credential bundle to the attacker. The PKCE proof key, designed as a one-time replay-prevention mechanism, is rendered useless once handed to the attacker, who can then complete the token exchange against the real authorization server and obtain a valid, fully-scoped access token.

For `ClientCredentialsOAuthProvider` and `PrivateKeyJWTOAuthProvider`, the attack requires no human interaction. For `OAuthClientProvider`, a user must approve the sign-in, but Cycode confirmed the page presented is the genuine login screen—providing no visual warning.

CVSS scores: 7.5 (machine-to-machine providers), 6.5 (interactive provider). No CVE had been assigned at time of publication.

**Affected versions:**
| Line | Affected | Fixed |
|------|----------|-------|
| 1.x  | 1.9.1 – 1.29.1 | 1.30.0 |
| 2.x  | 2.0.0 – 2.1.1  | 2.2.0  |

## Framework Mapping

- **AML.T0098 (AI Agent Tool Credential Harvesting)**: The attack directly harvests OAuth credentials transiting through the MCP client's tool-use authentication layer.
- **AML.T0083 (Credentials from AI Agent Configuration)**: Stolen client secrets are long-lived configuration-level credentials.
- **AML.T0081 (Modify AI Agent Configuration)**: The malicious server effectively hijacks the client's authorization server configuration at runtime.
- **LLM05 (Supply Chain Vulnerabilities)**: The flaw resides in the official SDK, making it a supply chain risk for any application built on MCP.
- **LLM06 (Sensitive Information Disclosure)**: OAuth client secrets, authorization codes, and PKCE keys are exposed to unauthorized parties.
- **LLM07 (Insecure Plugin Design)**: The MCP server-client trust model lacked sufficient validation of authorization server metadata.

## Impact Assessment

Any application built as an MCP HTTP client using the affected OAuth providers and capable of connecting to an untrusted server is exposed. The client secret's long-lived nature means stolen credentials remain valid until manually rotated, enabling persistent unauthorized access. Machine-to-machine deployments are at highest risk due to the absence of any human-in-the-loop detection opportunity.

## Mitigation & Recommendations

1. **Upgrade immediately**: Move to `1.30.0` (1.x) or `2.2.0` (2.x). Fixed versions pin the expected authorization server before fetching metadata and reject any deviation.
2. **Rotate credentials**: If `ClientCredentialsOAuthProvider` or `PrivateKeyJWTOAuthProvider` were used on affected versions, treat all client secrets as compromised and rotate them.
3. **Audit server trust**: Review all MCP client configurations to ensure connections are restricted to fully trusted, verified servers.
4. **Monitor token usage**: Review access logs for anomalous token issuance or usage patterns that may indicate prior exploitation.

## References

- [The Hacker News – Original Report](https://thehackernews.com/2026/09/official-mcp-python-sdk-flaw-can-let.html)
