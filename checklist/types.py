"""
checklist/types.py — Mapping of fintech types → applicable regulations.

Defines the regulatory profile for each fintech vertical, including
which regulations apply and at what priority level.
"""

from dataclasses import dataclass, field
from typing import Optional


# ─── Fintech Types with Regulatory Profiles ────────────────────────────────

FINTECH_TYPES = {
    "payments": {
        "display_name": "Payments / Money Transfer",
        "description": "Process payments, money transfers, or remittances",
        "examples": ["Stripe", "Square", "Wise", "Remitly"],
    },
    "lending": {
        "display_name": "Lending / Credit",
        "description": "Provide consumer or business loans, credit, or BNPL",
        "examples": ["Affirm", "Upstart", "Klarna", "LendingClub"],
    },
    "crypto": {
        "display_name": "Crypto / Digital Assets",
        "description": "Exchange, custody, or deal in cryptocurrencies and digital assets",
        "examples": ["Coinbase", "Kraken", "Circle"],
    },
    "p2p": {
        "display_name": "Peer-to-Peer / Marketplace",
        "description": "Platform-based financial transactions between users",
        "examples": ["Venmo", "Zelle", "PayPal"],
    },
    "banking": {
        "display_name": "Neobank / Digital Banking",
        "description": "Digital-first banking services, deposits, checking/savings",
        "examples": ["Chime", "Revolut", "Monzo", "Current"],
    },
    "wealth": {
        "display_name": "Wealth / Investments",
        "description": "Investment advisory, robo-advising, portfolio management",
        "examples": ["Robinhood", "Betterment", "Wealthfront"],
    },
    "insurance": {
        "display_name": "Insurance / InsurTech",
        "description": "Insurance products, distribution, or underwriting",
        "examples": ["Lemonade", "Hippo", "Root Insurance"],
    },
}


# ─── Regulation Requirements per Fintech Type ──────────────────────────────

@dataclass
class RegulationRequirement:
    """A specific regulation that applies to a fintech type."""
    title: str
    section: Optional[str] = None
    priority: int = 5  # 1=critical, 10=nice-to-have
    description: str = ""
    jurisdiction: str = "Federal"


REGULATORY_PROFILES: dict[str, list[RegulationRequirement]] = {
    "payments": [
        RegulationRequirement("Bank Secrecy Act (BSA) Program", "BSA", 1,
            "Must have AML program, file SARs and CTRs as required"),
        RegulationRequirement("Customer Due Diligence / KYC", "31 CFR § 1010.230", 1,
            "Verify customer identity, beneficial ownership for business accounts"),
        RegulationRequirement("Money Transmitter License", "State MTL", 1,
            "Licensing in each state where money transmission occurs"),
        RegulationRequirement("Regulation E — Electronic Fund Transfers", "Reg E", 2,
            "Error resolution, unauthorized transfer liability limits"),
        RegulationRequirement("Remittance Transfer Rule", "Reg E Subpart B", 2,
            "If offering international transfers: disclosure rates, fees, delivery"),
        RegulationRequirement("NYDFS Cybersecurity Regulation", "23 NYCRR 500", 3,
            "If operating in NY: cybersecurity program required"),
        RegulationRequirement("Privacy / GLBA Compliance", "GLBA", 3,
            "Privacy notices, opt-out rights for sharing nonpublic personal info"),
        RegulationRequirement("CCPA Compliance (if CA operations)", "CCPA", 4,
            "California consumer privacy rights: access, deletion, opt-out"),
    ],
    "lending": [
        RegulationRequirement("Truth in Lending Act / Regulation Z", "Reg Z", 1,
            "APR, finance charge, payment schedule disclosures. Ability-to-repay requirements."),
        RegulationRequirement("Fair Lending / ECOA Compliance", "ECOA", 1,
            "Equal Credit Opportunity Act: no discrimination in lending"),
        RegulationRequirement("BSA/AML Program", "BSA", 1,
            "AML program, SAR filings, currency transaction reporting"),
        RegulationRequirement("Lending License(s)", "State Lending", 1,
            "License in each state where loans originate. Interest rate limits."),
        RegulationRequirement("Regulation E (if ACH/EFT involved)", "Reg E", 2,
            "Electronic fund transfers: error resolution, statements"),
        RegulationRequirement("Debt Collection Rules / Reg F", "Reg F", 2,
            "If collecting debts: call limits, validation notices"),
        RegulationRequirement("Small Business Lending Rule (1071)", "1071 Rule", 3,
            "If small business lending: data collection on demographics"),
        RegulationRequirement("NY DFS Cybersecurity Regulation", "23 NYCRR 500", 3,
            "NY operations require cybersecurity program"),
        RegulationRequirement("GLBA Privacy Compliance", "GLBA", 3,
            "Privacy policies and opt-out notices"),
    ],
    "crypto": [
        RegulationRequirement("BSA/AML Program (for virtual currency)", "BSA", 1,
            "AML program must cover virtual currency activities. SARs for VC transactions."),
        RegulationRequirement("Money Transmitter License", "State MTL", 1,
            "Most states require MTL for crypto exchange/custody activities"),
        RegulationRequirement("NY BitLicense (if NY operations)", "23 NYCRR 200", 1,
            "NY-specific virtual currency license. Capital/reserve requirements."),
        RegulationRequirement("Travel Rule Compliance", "FinCEN Travel Rule", 1,
            "Transmit originator and beneficiary info for VC transactions over $3,000"),
        RegulationRequirement("Customer Due Diligence / KYC", "31 CFR § 1010.230", 1,
            "Verify customer identity, monitor transactions"),
        RegulationRequirement("SEC Securities Considerations", "SEC Crypto", 2,
            "Determine if tokens are securities. Reg D/Reg CF if issuing tokens."),
        RegulationRequirement("CFTC Digital Commodity Compliance", "CFTC", 2,
            "If trading digital commodities: registration, reporting"),
        RegulationRequirement("OFAC Sanctions Screening", "OFAC", 1,
            "Screen customers against sanctions lists. Block prohibited transactions."),
    ],
    "p2p": [
        RegulationRequirement("Money Transmitter License", "State MTL", 1,
            "P2P payment platforms require MTL in most states"),
        RegulationRequirement("BSA/AML Program", "BSA", 1,
            "AML program with SAR/CTR filing requirements"),
        RegulationRequirement("Customer Due Diligence / KYC", "31 CFR § 1010.230", 1,
            "Verify user identity, at least for transaction thresholds"),
        RegulationRequirement("Regulation E", "Reg E", 2,
            "Electronic fund transfer protections for consumer accounts"),
        RegulationRequirement("GLBA Privacy Compliance", "GLBA", 3,
            "Privacy notices and data sharing disclosures"),
        RegulationRequirement("NYDFS Cybersecurity Regulation", "23 NYCRR 500", 3,
            "NY operations, regardless of size, require cybersecurity compliance"),
    ],
    "banking": [
        RegulationRequirement("Bank Charter / Partnership Requirements", "Banking", 1,
            "Either obtain bank charter or partner with FDIC-insured bank"),
        RegulationRequirement("BSA/AML Program (full)", "BSA", 1,
            "Full AML program: officer, training, independent testing"),
        RegulationRequirement("Customer Due Diligence / KYC / Beneficial Ownership", "31 CFR § 1010.230", 1,
            "Full CDD: identity verification, beneficial ownership"),
        RegulationRequirement("Regulation E — Electronic Fund Transfers", "Reg E", 1,
            "Full error resolution, unauthorized transfer liability, periodic statements"),
        RegulationRequirement("Regulation DD — Truth in Savings", "Reg DD", 1,
            "Disclose APY, fees, minimum balance requirements for deposit accounts"),
        RegulationRequirement("FDIC Requirements", "FDIC", 1,
            "FDIC insurance, signage, recordkeeping for insured deposits"),
        RegulationRequirement("Community Reinvestment Act (if applicable)", "CRA", 2,
            "If FDIC-insured: serve credit needs of entire community"),
        RegulationRequirement("NYDFS Cybersecurity Regulation", "23 NYCRR 500", 1,
            "NY banking operations: strict cybersecurity requirements"),
    ],
    "wealth": [
        RegulationRequirement("Investment Advisers Act Registration", "IA-1940", 1,
            "Register with SEC ($100M+ AUM) or state (<$100M AUM)"),
        RegulationRequirement("Anti-Fraud (Rule 10b-5)", "1934 Act", 1,
            "No deceptive practices in connection with securities transactions"),
        RegulationRequirement("Customer Due Diligence / KYC", "KYC", 2,
            "Verify client identity, suitability of investments"),
        RegulationRequirement("BSA/AML Program", "BSA", 2,
            "AML program for investment advisors with securities accounts"),
        RegulationRequirement("Regulation Best Interest (Reg BI)", "Reg BI", 2,
            "Broker-dealer standard of conduct: best interest, no conflicts"),
        RegulationRequirement("Marketing Rule (Advisers Act Rule 206(4)-1)", "Marketing Rule", 2,
            "Testimonials, performance advertising, and social media compliance"),
        RegulationRequirement("Privacy / Reg S-P", "Reg S-P", 3,
            "Privacy notice delivery, opt-out for sharing nonpublic info"),
    ],
    "insurance": [
        RegulationRequirement("Insurance License", "State Insurance", 1,
            "License in each state where insurance is sold or underwritten"),
        RegulationRequirement("Rate and Form Filing", "Insurance Filing", 1,
            "File rates and policy forms with state insurance departments"),
        RegulationRequirement("Producer Licensing", "Insurance Producer", 1,
            "Licensed agents/producers for insurance sales"),
        RegulationRequirement("Consumer Privacy / GLBA", "GLBA", 2,
            "Privacy notices required. Medical info has heightened protections."),
        RegulationRequirement("Fair Claims Practices", "Claims", 2,
            "Prompt, fair claims handling per state Unfair Claims Practices Acts"),
        RegulationRequirement("NAIC Model Regulations", "NAIC", 3,
            "Model regulations for market conduct, solvency, and data security"),
        RegulationRequirement("NYDFS Cybersecurity Regulation", "23 NYCRR 500", 3,
            "NY: data security program for insurance companies"),
    ],
}


def get_all_fintech_types() -> list[str]:
    """Return all supported fintech type slugs."""
    return list(FINTECH_TYPES.keys())


def get_fintech_info(fintech_type: str) -> Optional[dict]:
    """Get display info for a fintech type."""
    return FINTECH_TYPES.get(fintech_type)


def get_regulations_for_type(
    fintech_type: str,
    min_priority: int = 10,
) -> list[RegulationRequirement]:
    """Get regulations applicable to a fintech type, filtered by priority."""
    regs = REGULATORY_PROFILES.get(fintech_type, [])
    return [r for r in regs if r.priority <= min_priority]


def add_custom_type(name: str, display_name: str, description: str = "") -> bool:
    """Add a new fintech type (for extensibility)."""
    if name in FINTECH_TYPES:
        return False
    FINTECH_TYPES[name] = {
        "display_name": display_name,
        "description": description,
        "examples": [],
    }
    REGULATORY_PROFILES[name] = []
    return True


if __name__ == "__main__":
    print("📋 Supported Fintech Types:")
    for ftype, info in FINTECH_TYPES.items():
        regs = get_regulations_for_type(ftype, min_priority=3)
        print(f"  • {ftype:12s} — {info['display_name']} ({len(regs)} key regulations)")
