---
title: "Scoring Methodology"
description: "How Grid the Grey scores article relevance and threat levels."
layout: "single"
---

## How We Score Articles

Every article published on Grid the Grey is evaluated by the Claude AI model across two dimensions: **Relevance Score** and **Threat Level**. This ensures only the most significant AI security developments reach you.

---

### Relevance Score (0–10)

The relevance score measures how closely an article relates to AI security, machine learning threats, LLM vulnerabilities, or related adversarial techniques.

| Score Range | Meaning |
|---|---|
| **8.0 – 10.0** | Highly relevant — direct AI/ML security impact, novel techniques, or active exploitation |
| **6.0 – 7.9** | Relevant — significant AI security implications, important for practitioners |
| **Below 6.0** | Not published — insufficient AI security relevance |

**Factors that raise the score:**
- Direct exploitation of AI/ML systems
- Novel attack techniques against LLMs or ML pipelines
- Active CVEs affecting AI infrastructure
- Research from high-credibility sources (Google Project Zero, CISA, academic institutions)
- Techniques mappable to MITRE ATLAS or OWASP LLM Top 10

**Factors that lower the score:**
- Generic cybersecurity news with weak AI/ML connection
- Marketing content or vendor announcements without technical depth
- Duplicated coverage of an already-published story

---

### Threat Level

The threat level classifies the operational urgency of a security issue:

| Level | Colour | Meaning |
|---|---|---|
| **CRITICAL** | Red | Active exploitation in the wild. Immediate review and action required. |
| **HIGH** | Orange | High probability of exploitation. Prioritise patching or mitigation. |
| **MEDIUM** | Yellow | Moderate risk. Monitor for developments and plan remediation. |
| **LOW** | Green | Limited impact. Standard review cycle is appropriate. |

Threat level is assessed based on: CVSS scores where available, evidence of active exploitation, breadth of affected systems, and the sophistication of the attack technique.

---

### Framework Mapping

In addition to scoring, every article is mapped (where applicable) to:

- **[MITRE ATLAS](/frameworks/mitre-atlas/)** — adversarial ML attack technique IDs (e.g. AML.T0051)
- **[OWASP LLM Top 10](/frameworks/owasp-llm/)** — LLM vulnerability categories (e.g. LLM01)

This mapping is performed by the Claude AI model using official MITRE ATLAS and OWASP LLM Top 10 taxonomies, cross-referenced against article content.
