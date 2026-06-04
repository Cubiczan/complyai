"""
templates/__init__.py — Document Template Generator for complyAI.

Generates legal and compliance document templates with {{variables}} for
user customization. Supports Terms of Service, Privacy Policies, EULAs,
and regulatory disclosures (Reg E, Reg Z, etc.).
"""

from typing import Optional
from pathlib import Path
from datetime import datetime

TEMPLATES_DIR = Path(__file__).parent


# ─── Template Definitions ────────────────────────────────────────────────────

TEMPLATE_METADATA = {
    "terms_of_service": {
        "name": "Terms of Service",
        "description": "General terms of service for fintech platforms",
        "applicable_types": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
        "jurisdiction": "US",
    },
    "privacy_policy": {
        "name": "Privacy Policy",
        "description": "Privacy policy covering data collection, use, and sharing",
        "applicable_types": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
        "jurisdiction": "US",
    },
    "eula": {
        "name": "End User License Agreement (EULA)",
        "description": "Software license agreement for mobile/web fintech applications",
        "applicable_types": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
        "jurisdiction": "US",
    },
    "reg_e_disclosure": {
        "name": "Regulation E Disclosure — Electronic Fund Transfers",
        "description": "Disclosure required under Regulation E (12 CFR 1005) for electronic fund transfer services",
        "applicable_types": ["payments", "banking", "p2p"],
        "jurisdiction": "US",
    },
    "reg_z_disclosure": {
        "name": "Regulation Z Disclosure — Truth in Lending",
        "description": "Disclosure required under Regulation Z (12 CFR 1026) for lending/credit products",
        "applicable_types": ["lending"],
        "jurisdiction": "US",
    },
    "aml_policy": {
        "name": "AML / BSA Policy Template",
        "description": "Anti-Money Laundering policy document required for financial institutions",
        "applicable_types": ["payments", "lending", "crypto", "p2p", "banking", "wealth"],
        "jurisdiction": "US",
    },
    "privacy_notice_glba": {
        "name": "GLBA Privacy Notice",
        "description": "Gramm-Leach-Bliley Act privacy notice for financial institutions",
        "applicable_types": ["payments", "lending", "banking", "wealth"],
        "jurisdiction": "US",
    },
    "data_sharing_agreement": {
        "name": "Data Sharing / Processing Agreement",
        "description": "Agreement for sharing customer data with service providers",
        "applicable_types": ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
        "jurisdiction": "US",
    },
}


# ─── Template Content ────────────────────────────────────────────────────────

TEMPLATES: dict[str, str] = {
    "terms_of_service": """# Terms of Service

**Last Updated: {{effective_date}}**

## 1. Introduction

Welcome to {{company_name}} ("Company," "we," "us," "our"). These Terms of Service ("Terms") govern your use of our {{service_description}} ("Service").

By accessing or using the Service, you agree to be bound by these Terms. If you do not agree, do not use the Service.

## 2. Eligibility

You must be at least 18 years old and have the legal capacity to enter into a binding agreement. By using the Service, you represent and warrant that:

- You are not located in a country subject to US sanctions
- You have provided accurate and complete registration information
- You will maintain the confidentiality of your account credentials

## 3. Service Description

{{company_name}} provides {{service_description}}. The specific features, terms, and conditions are described on our website and may be updated from time to time.

## 4. User Accounts

### 4.1 Registration
You must create an account to use the Service. You are responsible for all activity under your account.

### 4.2 Security
You must keep your login credentials confidential. Notify us immediately of any unauthorized use.

### 4.3 Suspension
We may suspend or terminate accounts for violation of these Terms or applicable law.

## 5. Fees and Payments

### 5.1 Fees
We charge fees for {{fee_description}}. Fees are disclosed before you complete a transaction.

### 5.2 Payment Terms
All fees are {{currency}} and exclusive of taxes. You authorize us to charge your selected payment method.

### 5.3 Refunds
Refunds are governed by our Refund Policy, available at {{refund_policy_url}}.

## 6. Prohibited Activities

You agree not to:

- Violate any applicable law or regulation
- Use the Service for illegal or fraudulent purposes
- Interfere with the Service's operation
- Reverse engineer, decompile, or disassemble the Service
- Use the Service to transmit malware or harmful code
- Engage in any activity that violates sanctions or export controls

## 7. Intellectual Property

The Service and its content, including software, designs, logos, and trademarks, are owned by {{company_name}} or its licensors. You may not reproduce, distribute, or create derivative works without our written consent.

## 8. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, {{company_name}} SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM YOUR USE OF THE SERVICE.

## 9. Dispute Resolution

### 9.1 Governing Law
These Terms are governed by {{governing_law}}.

### 9.2 Arbitration
Any dispute arising from these Terms shall be resolved by binding arbitration in accordance with the rules of {{arbitration_provider}}.

### 9.3 Class Action Waiver
You agree to resolve disputes on an individual basis and waive any right to participate in a class action.

## 10. Changes to Terms

We may update these Terms by posting a revised version. Material changes will be communicated via email or Service notification.

## 11. Contact

For questions about these Terms, contact us at:

{{support_email}}
{{support_phone}}
{{support_address}}
""",

    "privacy_policy": """# Privacy Policy

**Last Updated: {{effective_date}}**

## 1. Information We Collect

We collect information you provide directly, including:

- **Account Information**: name, email, phone, address, date of birth
- **Identity Verification**: government ID, tax ID, business information
- **Financial Information**: bank account details, transaction history
- **Usage Information**: how you use our Service, device information, IP address

## 2. How We Use Your Information

We use your information to:

- Provide, maintain, and improve our Service
- Verify your identity and prevent fraud
- Comply with legal and regulatory obligations, including anti-money laundering (AML) laws
- Communicate with you about your account and transactions
- Analyze usage patterns to improve our Service
- Send marketing communications (with your consent)

## 3. Legal Basis for Processing (GDPR Compliance)

If you are in the European Economic Area, we process your personal data based on:

- **Contractual Necessity**: to provide our Service
- **Legal Obligation**: to comply with AML and other regulations
- **Legitimate Interests**: for fraud prevention and Service improvement
- **Consent**: for marketing communications

## 4. Information Sharing

We share your information with:

- **Service Providers**: payment processors, identity verification services, cloud infrastructure
- **Regulatory Bodies**: as required by applicable law, including FinCEN and state regulators
- **Law Enforcement**: in response to valid legal requests
- **Business Partners**: with your consent

## 5. Data Security

We implement appropriate technical and organizational measures to protect your personal data, including:

- Encryption at rest and in transit
- Access controls and authentication
- Regular security assessments
- Employee training on data protection

## 6. Data Retention

We retain your data for as long as your account is active and as required by applicable regulations (typically 5-7 years after account closure).

## 7. Your Rights

Depending on your jurisdiction, you may have the right to:

- Access your personal data
- Correct inaccurate data
- Delete your data (subject to regulatory requirements)
- Restrict processing
- Data portability
- Object to processing

## 8. Cookies

We use essential cookies for Service operation and analytics cookies to improve our Service. You can control cookie settings in your browser.

## 9. International Transfers

Your data may be transferred to and processed in the United States and other countries where our service providers operate.

## 10. Changes to This Policy

We will notify you of material changes via email or Service notification.

## 11. Contact

For privacy-related inquiries:

{{privacy_email}}
{{company_address}}

**California Residents**: For CCPA requests, contact {{ccpa_email}}.
""",

    "eula": """# End User License Agreement (EULA)

**Last Updated: {{effective_date}}**

## 1. License Grant

Subject to these terms, {{company_name}} grants you a non-exclusive, non-transferable, revocable license to use the {{app_name}} application ("App") for your personal or business use.

## 2. License Restrictions

You may not:

- Copy, modify, or create derivative works of the App
- Rent, lease, lend, sell, or sublicense the App
- Reverse engineer, decompile, or disassemble the App
- Remove any copyright or proprietary notices
- Use the App in violation of applicable law

## 3. Ownership

The App and all intellectual property rights are owned by {{company_name}}. This EULA does not transfer ownership.

## 4. Automatic Updates

The App may automatically download and install updates. You agree to receive these updates as part of using the App.

## 5. Termination

Your license terminates automatically if you violate these terms. Upon termination, you must delete all copies of the App.

## 6. Disclaimer of Warranty

THE APP IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.

## 7. Limitation of Liability

{{company_name}} IS NOT LIABLE FOR ANY DAMAGES ARISING FROM YOUR USE OF THE APP.

## 8. Governing Law

{{governing_law}}
""",

    "reg_e_disclosure": """# Regulation E Disclosure — Electronic Fund Transfers

**Disclosure Required by 12 CFR Part 1005 (Regulation E)**

**Effective Date: {{effective_date}}**

## Your Rights and Responsibilities

### Electronic Fund Transfers Covered

This disclosure applies to electronic fund transfers (EFTs) involving your {{account_description}} including:

- Debit card transactions
- ACH transfers (direct deposits, automatic payments)
- Online bill payments
- Mobile check deposits
- Person-to-person (P2P) transfers
- ATM transactions

### Your Liability for Unauthorized Transfers

Tell us IMMEDIATELY if you believe your card or credentials are lost or stolen, or if you suspect unauthorized use.

| Reporting Time | Your Maximum Liability |
|----------------|----------------------|
| Within 2 business days | $50 |
| After 2 business days but within 60 days of statement | $500 |
| After 60 days | Unlimited |

### Contact for Unauthorized Transfers

Call: {{unauthorized_contact_phone}}
Email: {{unauthorized_contact_email}}
Write: {{unauthorized_contact_address}}

### Error Resolution

If you believe there is an error in your transaction:

1. Contact us within 60 days of the statement showing the error
2. Provide your name, account number, and description of the error
3. We will investigate within 10 business days (up to 45 days for certain errors)
4. We will correct the error or explain our findings

### Business Days

Our business days are Monday through Friday, excluding federal holidays.

### Documentation

- **Periodic statements**: Provided {{statement_frequency}}
- **Receipts**: Available at point-of-sale and ATM transactions
- **Online access**: Transaction history available at {{online_portal_url}}

### Preauthorized Transfers

- You may stop a preauthorized payment by notifying us at least 3 business days before the scheduled date
- To stop payment: call {{stop_payment_phone}} or submit via {{online_portal_url}}
- We may require written confirmation within 14 days

## Company Information

{{company_name}}
{{support_address}}
{{support_phone}}

*This disclosure is provided pursuant to the Electronic Fund Transfer Act (15 U.S.C. 1693 et seq.) and Regulation E (12 CFR Part 1005).*
""",

    "reg_z_disclosure": """# Regulation Z Disclosure — Truth in Lending

**Disclosure Required by 12 CFR Part 1026 (Regulation Z)**

**Effective Date: {{effective_date}}**

## Loan/Financing Summary

| Item | Detail |
|------|--------|
| **Annual Percentage Rate (APR)** | {{apr}}% |
| **Finance Charge** | ${{finance_charge}} |
| **Amount Financed** | ${{amount_financed}} |
| **Total of Payments** | ${{total_payments}} |
| **Payment Schedule** | {{payment_schedule}} |
| **Number of Payments** | {{num_payments}} |
| **Late Payment Fee** | ${{late_fee}} |
| **Prepayment Penalty** | {{prepayment_penalty}} |

## Important Terms

### APR
The APR is the cost of your credit expressed as a yearly rate. It reflects both the interest rate and certain finance charges.

### Payment Schedule
Your payment schedule is {{payment_schedule}}. Payments are due on the {{payment_due_day}} of each month.

### Late Payments
If your payment is more than {{late_grace_days}} days late, you may be charged a late fee of ${{late_fee}}.

### Prepayment
{{prepayment_description}}

### Security Interest
{{security_interest_description}}

## Your Right to Cancel (for certain transactions)

If your loan involves a security interest in your principal dwelling, you have the right to cancel within three business days.

## Questions?

Contact us at: {{lending_support_phone}} or {{lending_support_email}}

*This disclosure is provided pursuant to the Truth in Lending Act (15 U.S.C. 1601 et seq.) and Regulation Z (12 CFR Part 1026).*
""",

    "aml_policy": """# Anti-Money Laundering (AML) Policy

**Effective Date: {{effective_date}}**

## 1. Policy Statement

{{company_name}} is committed to preventing money laundering and terrorist financing. This AML Policy establishes procedures to comply with the Bank Secrecy Act (BSA), USA PATRIOT Act, and FinCEN regulations.

## 2. Designated Compliance Officer

{{aml_officer_name}} serves as our BSA/AML Compliance Officer, responsible for:

- Overseeing the AML program
- Filing Suspicious Activity Reports (SARs)
- Currency Transaction Reports (CTRs)
- Training employees
- Coordinating with regulators

Contact: {{aml_officer_email}}, {{aml_officer_phone}}

## 3. Customer Identification Program (CIP)

Before opening an account, we will collect:

- Full legal name
- Date of birth
- Physical address (not P.O. Box)
- Government-issued ID number (SSN, EIN, passport)
- For legal entities: beneficial ownership information

## 4. Customer Due Diligence (CDD)

### Standard CDD
- Verify customer identity
- Understand nature of business
- Monitor transactions for suspicious activity
- Maintain updated customer information

### Enhanced Due Diligence (EDD)
For high-risk customers including:
- Politically Exposed Persons (PEPs)
- Customers from high-risk jurisdictions
- Complex ownership structures
- Non-profit organizations

## 5. Transaction Monitoring

We monitor transactions for:

- Structuring (smurfing) patterns
- Transactions inconsistent with customer profile
- Unusually large or frequent transactions
- Rapid movement of funds
- Transactions involving high-risk jurisdictions

## 6. Reporting Requirements

| Report | Threshold | Filing Deadline |
|--------|-----------|----------------|
| Currency Transaction Report (CTR) | $10,000+ in currency | 15 days |
| Suspicious Activity Report (SAR) | $5,000+ (suspected) | 30 days (extendable to 60) |
| FBAR (Foreign Bank Account) | $10,000+ foreign accounts | April 15 |

## 7. Recordkeeping

We maintain the following records for at least 5 years:

- Account opening documents
- Transaction records
- SAR/CTR copies
- AML training records
- Audit reports

## 8. Training

All employees receive annual AML training covering:

- Red flags for money laundering
- SAR filing procedures
- Customer identification requirements
- Recent regulatory developments

## 9. Independent Testing

Our AML program is tested annually by an independent party (internal or external).

## 10. Sanctions Compliance

We screen all customers against:

- OFAC Specially Designated Nationals (SDN) List
- Sanctions lists from the EU, UN, and UK
- Politically Exposed Persons (PEP) databases

## 11. Risk Assessment

We conduct an enterprise-wide risk assessment annually and update our AML program accordingly.
""",

    "privacy_notice_glba": """# GLBA Privacy Notice

**Last Updated: {{effective_date}}**

## Your Privacy Rights (Gramm-Leach-Bliley Act)

### What Information We Collect

We collect nonpublic personal information about you from:

- Your account application (name, address, income, SSN)
- Your transactions with us (account balance, transaction history)
- Consumer reporting agencies (credit reports)
- Other sources with your consent

### How We Share Information

We share information as permitted by law:

| Category | Do We Share? | Can You Opt Out? |
|----------|-------------|------------------|
| For everyday business purposes | Yes | No |
| For marketing purposes | Yes | Yes |
| With affiliates | Yes | Yes |
| With nonaffiliated third parties | No | N/A |

### Your Right to Opt Out

You may opt out of information sharing for marketing purposes. To opt out:

Call: {{opt_out_phone}}
Email: {{opt_out_email}}
Write: {{opt_out_address}}

### Our Security Practices

We maintain physical, electronic, and procedural safeguards to protect your information.

### Changes to This Notice

We will notify you of material changes and provide an updated notice.

### Questions?

Contact: {{privacy_contact_email}}, {{privacy_contact_phone}}

*This notice is provided annually pursuant to the Gramm-Leach-Bliley Act (15 U.S.C. 6801-6809) and Regulation P (12 CFR Part 1016).*
""",

    "data_sharing_agreement": """# Data Sharing & Processing Agreement

**Effective Date: {{effective_date}}**

**Between**: {{company_name}} ("Data Controller")
**And**: {{processor_name}} ("Data Processor")

## 1. Definitions

- **Personal Data**: any information relating to an identified or identifiable natural person
- **Processing**: any operation performed on Personal Data
- **Data Subject**: the individual to whom Personal Data relates

## 2. Processing Details

| | |
|---|---|
| **Nature of Processing** | {{processing_nature}} |
| **Categories of Data Subjects** | {{data_subject_categories}} |
| **Categories of Personal Data** | {{data_categories}} |
| **Processing Duration** | {{processing_duration}} |

## 3. Obligations of Data Processor

The Data Processor shall:

- Process Data only on documented instructions
- Ensure confidentiality of all personnel
- Implement appropriate technical and organizational measures
- Notify Controller of any data breach within {{breach_notification_hours}} hours
- Assist Controller with data subject rights requests
- Delete or return all Data at termination

## 4. Sub-processing

Processor may engage sub-processors with prior written consent. Current sub-processors:

{{subprocessors_list}}

## 5. Data Breach Notification

Processor shall notify Controller of any breach of Personal Data within {{breach_notification_hours}} hours, including:

- Nature of the breach
- Categories of Data involved
- Estimated number of Data Subjects
- Remediation measures

## 6. Audit Rights

Controller may audit Processor's compliance with this Agreement annually, with reasonable notice.

## 7. Termination

Upon termination, Processor shall delete or return all Personal Data within {{data_deletion_days}} days.

## 8. Limitation of Liability

Each party's liability is limited as set forth in the Master Services Agreement.

## 9. Governing Law

{{governing_law}}

## 10. Signatures

______________________________              ______________________________
{{company_name}}                              {{processor_name}}
Date: ______________                         Date: ______________
""",
}


# ─── Template Functions ──────────────────────────────────────────────────────


def get_available_templates(fintech_type: Optional[str] = None) -> list[dict]:
    """List available templates, optionally filtered by fintech type."""
    results = []
    for slug, meta in TEMPLATE_METADATA.items():
        if fintech_type and fintech_type not in meta["applicable_types"]:
            continue
        results.append({
            "slug": slug,
            "name": meta["name"],
            "description": meta["description"],
            "jurisdiction": meta["jurisdiction"],
        })
    return results


def get_template_content(slug: str) -> Optional[str]:
    """Get the raw template content by slug."""
    return TEMPLATES.get(slug)


def render_template(
    slug: str,
    variables: dict[str, str],
    fintech_type: Optional[str] = None,
) -> Optional[str]:
    """Render a template by filling in variables.

    Args:
        slug: Template identifier (e.g., 'terms_of_service')
        variables: Dict of variable names to values
        fintech_type: Optional fintech type for filtering

    Returns:
        Rendered template string, or None if template not found
    """
    meta = TEMPLATE_METADATA.get(slug)
    if not meta:
        return None

    if fintech_type and fintech_type not in meta["applicable_types"]:
        return None

    content = TEMPLATES.get(slug)
    if not content:
        return None

    # Apply defaults for common variables
    defaults = {
        "effective_date": datetime.utcnow().strftime("%B %d, %Y"),
        "company_name": "{{company_name}}",
        "governing_law": "{{governing_law}}",
        "support_email": "{{support_email}}",
        "support_phone": "{{support_phone}}",
    }

    merged = {**defaults, **variables}

    rendered = content
    for key, value in merged.items():
        rendered = rendered.replace("{{" + key + "}}", value)

    return rendered


def save_rendered_template(
    slug: str,
    variables: dict[str, str],
    output_path: Optional[str] = None,
    fintech_type: Optional[str] = None,
) -> Optional[str]:
    """Render and save a template to a file.

    Args:
        slug: Template slug
        variables: Variable values
        output_path: Output path (default: template-name.md)
        fintech_type: Optional fintech type filter

    Returns:
        Path to saved file, or None on failure
    """
    rendered = render_template(slug, variables, fintech_type)
    if not rendered:
        return None

    path = Path(output_path or f"{slug}.md")
    path.write_text(rendered)
    return str(path)


def list_template_variables(slug: str) -> list[str]:
    """List all {{variables}} used in a template."""
    content = TEMPLATES.get(slug)
    if not content:
        return []
    import re
    return sorted(set(re.findall(r"\{\{(\w+)\}\}", content)))


if __name__ == "__main__":
    # Quick test
    for slug in ["terms_of_service", "privacy_policy", "reg_e_disclosure"]:
        vars_list = list_template_variables(slug)
        print(f"\n📝 {slug} ({len(vars_list)} variables):")
        print(f"   {', '.join(vars_list[:10])}{'...' if len(vars_list) > 10 else ''}")
