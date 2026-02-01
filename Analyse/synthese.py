import json
from tqdm import tqdm
from core.agent import call_agent_LLM
from tools.save import save_in_file
import os

def synthese(jsonData, process=True):

    os.makedirs("db/rapport_individuel", exist_ok=True)
    
    allMiniReport = []
    
    for idx, data in enumerate(tqdm(jsonData, desc="Génération synthèse", unit="Classe")):
        prompt = f"""
You are a senior security engineer conducting a reverse engineering audit.

You receive the JSON description of ONE Java class with:
- Static analysis results
- Cryptographic inspection
- Vulnerability analysis
- Contextual understanding

Your task: Generate a concise, structured Markdown security summary for this class.

OUTPUT FORMAT: **MARKDOWN ONLY** (no JSON, no code blocks)
Be factual and concise
Do NOT invent vulnerabilities
Base your analysis STRICTLY on the provided data

---

## REQUIRED MARKDOWN STRUCTURE

### Class: [ClassName]
**Package:** [package.name]  
**Security Criticality:** [CORE | HIGH | MEDIUM | LOW]

#### Role & Purpose
[1-2 sentences describing what this class does and why it matters for security]

#### Security-Sensitive Methods
[List ONLY methods that handle cryptography, signatures, integrity checks, or trust decisions]
- `methodName()` - [brief security role]

#### Cryptographic Usage
**Algorithms:** [SHA-256, RSA, ECDSA, etc. - or "None"]  
**Operations:** [hashing, signature verification, etc. - or "None"]

#### Identified Vulnerabilities
**Critical:** [list or "None identified"]  
**High:** [list or "None identified"]  
**Medium:** [list or "None identified"]  
**Low:** [list or "None identified"]

#### Security Strengths
[Bullet list of confirmed good practices, or "No specific strengths identified"]

#### Contextual Notes
[1-3 key observations about architectural importance, dependencies, or systemic impact]

---

## INPUT DATA
```json
{json.dumps(data, indent=2)}
```

Generate the Markdown summary now:
"""
        
        class_summary = call_agent_LLM(prompt, "qwen3:32b")
        class_summary = class_summary.replace("```markdown", "").replace("```", "").strip()
        class_name = data.get("signature", {}).get("className", f"Class_{idx}")
        safe_filename = class_name.replace("/", "_").replace(".", "_")

        save_in_file(f"rapport_individuel/{safe_filename}.md", class_summary)
        allMiniReport.append(class_summary)
    
    pre_rapport = "\n\n---\n\n".join(allMiniReport)
    save_in_file("Pre_rapport.md", pre_rapport)
    print("\nGénération du rapport")
    
    final_report_prompt = f"""
You are a senior application security auditor preparing a comprehensive security report.

You receive **individual Markdown security summaries** for multiple Java classes from an Android APK signing/verification codebase.

Your task: Generate a **professional, executive-level security audit report** in **clean Markdown** suitable for:
- Security audits
- Technical due diligence
- Executive briefings
- Reverse engineering documentation

OUTPUT: **MARKDOWN ONLY** (no JSON, no preamble)
Base analysis STRICTLY on provided summaries
Do NOT invent vulnerabilities
Maintain neutral, professional tone

---

## MANDATORY REPORT STRUCTURE

# Android APK Signing/Verification Security Analysis Report

## Executive Summary

**Total Classes Analyzed:** [number]  
**Overall Security Posture:** [Secure | Requires Hardening | Critical Risks Present]

[2-3 paragraph high-level assessment covering:
- Primary purpose of the analyzed codebase
- Key security strengths
- Major vulnerabilities (if any)
- Overall risk level and recommendations]

---

## Application Security Architecture

[Describe the overall security design:
- Core security components (CORE/HIGH criticality classes)
- Trust boundaries and enforcement points
- Cryptographic infrastructure
- Attack surface overview]

---

## Security-Critical Components

| Class Name | Security Criticality | Primary Role | Why Critical |
|------------|---------------------|--------------|--------------|
| [Class] | [CORE/HIGH] | [role] | [reason] |

*(Include only CORE and HIGH criticality classes)*

---

## Cryptographic Analysis

### Algorithms in Use
[List all cryptographic algorithms observed: SHA-256, RSA, ECDSA, etc.]
[Indicate if modern and secure or deprecated]

### Cryptographic Operations
- **Hashing:** [details or "Not used"]
- **Signature Generation:** [details or "Not used"]
- **Signature Verification:** [details or "Not used"]
- **Integrity Validation:** [details or "Not used"]

### Cryptographic Risks
[Summarize concrete cryptographic risks, or clearly state: "No cryptographic weaknesses identified."]

---

## Identified Vulnerabilities

### Critical Severity
[List with affected classes and impact, or state: "*No critical vulnerabilities identified.*"]

### High Severity
[List with affected classes and impact, or state: "*No high-severity vulnerabilities identified.*"]

### Medium Severity
[List with affected classes and impact, or state: "*No medium-severity vulnerabilities identified.*"]

### Low Severity
[List with affected classes and impact, or state: "*No low-severity vulnerabilities identified.*"]

---

## Security Strengths & Best Practices

[Bullet-point list of:
- Correct cryptographic implementations
- Robust integrity checks
- Defensive design patterns
- Architectural strengths]

---

## Security Recommendations

### High Priority (Immediate Action)
[Concrete actions to mitigate critical/high risks, or "None required"]

### Medium Priority (Short-Term)
[Hardening opportunities and defensive improvements, or "None required"]

### Long-Term Hardening
[Architectural or design-level improvements, or "None required"]

---

## Risk Assessment & Confidence

**Overall Confidence Score:** [0-100]%  
**Security Maturity Level:** [Low | Medium | High]

**Rationale:**  
[Explain scoring based on code quality, cryptographic practices, vulnerability count, and architectural design]

---

## Conclusion

**Final Security Assessment:**  
[Comprehensive conclusion covering overall readiness and key takeaways]

**Overall Readiness:**
- **Secure by design** - [if applicable]
- **Requires hardening** - [if applicable]
- **Contains critical risks** - [if applicable]

**Key Takeaways:**
1. [Main point]
2. [Main point]
3. [Main point]

---

## CLASS SUMMARIES INPUT

{pre_rapport}

---

Generate the comprehensive security report now:
"""

    final_report = call_agent_LLM(final_report_prompt, "qwen3:32b")
    final_report = final_report.replace("```markdown", "").replace("```", "").strip()
    save_in_file("Security_Analysis_Report.md", final_report)    
    return final_report