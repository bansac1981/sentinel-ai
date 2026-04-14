---
title: "Security Frameworks"
description: "Reference guide to the MITRE ATLAS and OWASP LLM Top 10 frameworks used by Grid the Grey."
layout: "single"
---

Grid the Grey maps every article to two industry-standard AI security frameworks. Here is a concise reference for both.

---

## MITRE ATLAS

**MITRE ATLAS** (Adversarial Threat Landscape for Artificial-Intelligence Systems) is a knowledge base of adversarial tactics and techniques targeting AI/ML systems, maintained by MITRE Corporation.

It is structured analogously to the well-known MITRE ATT&CK framework but focused specifically on machine learning systems.

**Technique ID format:** `AML.T####` (e.g. AML.T0051 — LLM Prompt Injection)

### Key Tactic Categories

| Tactic | Description |
|---|---|
| Reconnaissance | Gathering information about target ML systems |
| Resource Development | Acquiring/staging resources for attacks |
| Initial Access | Gaining entry to ML systems or pipelines |
| ML Attack Staging | Preparing adversarial inputs or attacks |
| Exfiltration | Stealing model parameters, training data, or outputs |
| Impact | Disrupting availability, integrity, or confidentiality of ML systems |

→ [Official MITRE ATLAS site](https://atlas.mitre.org)

---

## OWASP LLM Top 10

The **OWASP LLM Top 10** is a standard awareness document for developers and security practitioners covering the most critical security risks in Large Language Model applications, published by the Open Worldwide Application Security Project (OWASP).

### The 10 Categories

| ID | Category | Description |
|---|---|---|
| **LLM01** | Prompt Injection | Manipulating LLM behaviour via crafted inputs |
| **LLM02** | Insecure Output Handling | Failing to validate/sanitise LLM outputs downstream |
| **LLM03** | Training Data Poisoning | Corrupting training data to influence model behaviour |
| **LLM04** | Model Denial of Service | Causing excessive resource consumption in LLM operations |
| **LLM05** | Supply Chain Vulnerabilities | Risks in LLM components, training data, or deployment pipelines |
| **LLM06** | Sensitive Information Disclosure | LLMs revealing confidential data from training or context |
| **LLM07** | Insecure Plugin Design | Vulnerabilities in LLM plugins or tool integrations |
| **LLM08** | Excessive Agency | LLM systems granted excessive permissions or autonomy |
| **LLM09** | Overreliance | Blindly trusting LLM outputs without validation |
| **LLM10** | Model Theft | Extracting or reconstructing proprietary LLM parameters |

→ [Official OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## How Grid the Grey Uses These Frameworks

When the pipeline processes a new article, Claude evaluates the content and maps it to applicable MITRE ATLAS technique IDs and OWASP LLM categories. This mapping appears in:

- The **Framework Analysis Panel** on every article page
- The **[MITRE ATLAS matrix](/frameworks/mitre-atlas/)** — shows which techniques appear most in our coverage
- The **[OWASP LLM matrix](/frameworks/owasp-llm/)** — shows which vulnerability categories are trending
- The **ATLAS** and **OWASP** badges on article cards — click any badge to see the full matrix

See also: [Scoring Methodology](/scoring/)
