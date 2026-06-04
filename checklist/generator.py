"""
checklist/generator.py — Generate compliance checklists for fintech types.

Given a fintech type (payments, lending, crypto, etc.), generates a
structured compliance checklist with priority, estimated effort, and
actionable next steps.
"""

from typing import Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

from .types import (
    RegulationRequirement,
    get_regulations_for_type,
    get_fintech_info,
)

# ─── Checklist Models ────────────────────────────────────────────────────────

@dataclass
class ChecklistItem:
    """A single item on the compliance checklist."""
    title: str
    section: Optional[str] = None
    priority: int = 5  # 1=critical, 10=nice-to-have
    description: str = ""
    estimated_effort: str = "medium"  # low, medium, high
    category: str = "federal"
    action_items: list[str] = field(default_factory=list)
    resources: list[dict] = field(default_factory=list)


@dataclass
class ComplianceChecklist:
    """Complete compliance checklist for a fintech type."""
    fintech_type: str
    display_name: str
    generated_at: str
    jurisdiction: str = "US"
    items: list[ChecklistItem] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def item_count(self) -> int:
        return len(self.items)

    def critical_count(self) -> int:
        return len([i for i in self.items if i.priority <= 2])

    def high_priority_count(self) -> int:
        return len([i for i in self.items if 3 <= i.priority <= 4])

    def categorized_items(self) -> dict[str, list[ChecklistItem]]:
        cats: dict[str, list[ChecklistItem]] = {}
        for item in self.items:
            cats.setdefault(item.category, []).append(item)
        return cats

    def get_summary(self) -> dict:
        return {
            "total_items": self.item_count(),
            "critical": self.critical_count(),
            "high_priority": self.high_priority_count(),
            "categories": list(self.categorized_items().keys()),
            "jurisdiction": self.jurisdiction,
            "generated_at": self.generated_at,
        }


# ─── Effort Heuristics ───────────────────────────────────────────────────────

EFFORT_MAP: dict[str, str] = {
    "BSA": "high",
    "Bank Charter": "high",
    "State MTL": "high",
    "23 NYCRR 200": "high",
    "IA-1940": "high",
    "Reg Z": "medium",
    "Reg E": "medium",
    "31 CFR § 1010.230": "medium",
    "KYC": "medium",
    "CCPA": "medium",
    "GLBA": "low",
    "OFAC": "medium",
}

CATEGORY_MAP: dict[str, str] = {
    "BSA": "aml",
    "31 CFR": "aml",
    "KYC": "aml",
    "OFAC": "aml",
    "Reg Z": "consumer_protection",
    "Reg E": "consumer_protection",
    "Reg F": "consumer_protection",
    "Reg DD": "consumer_protection",
    "Reg BI": "securities",
    "IA-1940": "securities",
    "1934 Act": "securities",
    "GLBA": "privacy",
    "CCPA": "privacy",
    "23 NYCRR": "cybersecurity",
    "State MTL": "licensing",
    "State Lending": "licensing",
    "State Insurance": "licensing",
    "NY BitLicense": "licensing",
    "FDIC": "banking",
    "CRA": "banking",
}

ACTION_ITEM_TEMPLATES: dict[str, list[str]] = {
    "bsa": [
        "Designate a BSA/AML compliance officer",
        "Create written AML policies and procedures",
        "Implement transaction monitoring system",
        "Set up SAR/CTR filing process",
        "Schedule annual independent AML audit",
    ],
    "kyc": [
        "Implement customer identification program (CIP)",
        "Establish beneficial ownership verification",
        "Set up OFAC/sanctions screening",
        "Define risk-based CDD tiers",
        "Document KYC procedures",
    ],
    "consumer_protection": [
        "Draft required consumer disclosures",
        "Implement error resolution procedures",
        "Set up complaint tracking system",
        "Review advertising and marketing materials",
        "Train staff on disclosure requirements",
    ],
    "privacy": [
        "Draft and post privacy policy",
        "Implement data inventory and mapping",
        "Set up opt-out mechanism",
        "Review vendor/data processor agreements",
        "Document data retention/deletion procedures",
    ],
    "licensing": [
        "Identify state licensing requirements",
        "Prepare license application",
        "Gather required financial statements",
        "Complete background checks for principals",
        "Post surety bond (if required)",
    ],
    "securities": [
        "Register with SEC or state securities regulator",
        "Form ADV preparation and filing",
        "Create compliance manual",
        "Implement custody rules",
        "Annual compliance review",
    ],
    "cybersecurity": [
        "Conduct risk assessment",
        "Develop information security program",
        "Implement multi-factor authentication",
        "Create incident response plan",
        "Annual penetration testing",
    ],
    "banking": [
        "Select bank partner (if neobank)",
        "Review and sign bank partnership agreement",
        "Implement Reg DD disclosures",
        "Set up FDIC pass-through insurance",
        "Compliance with bank oversight requirements",
    ],
}


def _get_effort(reg: RegulationRequirement) -> str:
    for key, effort in EFFORT_MAP.items():
        if reg.section and key in reg.section:
            return effort
        if key in reg.title:
            return effort
    return "medium"


def _get_category(reg: RegulationRequirement) -> str:
    if reg.section:
        for key, cat in CATEGORY_MAP.items():
            if key in reg.section:
                return cat
    for key, cat in CATEGORY_MAP.items():
        if key in reg.title:
            return cat
    return "other"


def _get_action_items(reg: RegulationRequirement) -> list[str]:
    """Generate action items based on regulation type."""
    category = _get_category(reg)
    base_items = ACTION_ITEM_TEMPLATES.get(category, ["Review regulation requirements"])

    # Customize based on priority
    if reg.priority <= 2:
        base_items = [f"🚨 {item}" for item in base_items]

    return base_items


def _get_resources(reg: RegulationRequirement) -> list[dict]:
    """Get relevant resources for a regulation."""
    resources = []
    if reg.jurisdiction != "State":
        resources.append({
            "title": f"Full text: {reg.title}",
            "url": f"https://www.ecfr.gov/current/title-12" if "Reg" in reg.title
                   else f"https://www.fincen.gov/resources/statutes-regulations",
        })
    resources.append({
        "title": "NCSL State Licensing Overview",
        "url": "https://www.ncsl.org/financial-services",
    })
    return resources


# ─── Generator ────────────────────────────────────────────────────────────────


def generate_checklist(
    fintech_type: str,
    jurisdiction: str = "US",
    include_states: Optional[list[str]] = None,
    min_priority: int = 10,
) -> Optional[ComplianceChecklist]:
    """Generate a compliance checklist for a fintech type."""
    info = get_fintech_info(fintech_type)
    if not info:
        return None

    regs = get_regulations_for_type(fintech_type, min_priority)
    items: list[ChecklistItem] = []

    for reg in regs:
        item = ChecklistItem(
            title=reg.title,
            section=reg.section,
            priority=reg.priority,
            description=reg.description,
            estimated_effort=_get_effort(reg),
            category=_get_category(reg),
            action_items=_get_action_items(reg),
            resources=_get_resources(reg),
        )
        items.append(item)

    # Sort by priority (critical first)
    items.sort(key=lambda i: i.priority)

    checklist = ComplianceChecklist(
        fintech_type=fintech_type,
        display_name=info["display_name"],
        generated_at=datetime.utcnow().isoformat(),
        jurisdiction=jurisdiction,
        items=items,
    )
    checklist.summary = checklist.get_summary()
    return checklist


def checklist_to_dict(checklist: ComplianceChecklist) -> dict:
    """Convert checklist to dictionary for JSON serialization."""
    return {
        "fintech_type": checklist.fintech_type,
        "display_name": checklist.display_name,
        "generated_at": checklist.generated_at,
        "jurisdiction": checklist.jurisdiction,
        "summary": checklist.summary,
        "items": [
            {
                "title": i.title,
                "section": i.section,
                "priority": i.priority,
                "description": i.description,
                "estimated_effort": i.estimated_effort,
                "category": i.category,
                "action_items": i.action_items,
                "resources": i.resources,
            }
            for i in checklist.items
        ],
    }


if __name__ == "__main__":
    for ftype in ["payments", "lending", "crypto"]:
        print(f"\n{'='*60}")
        print(f"📋 Compliance Checklist: {ftype}")
        print('='*60)

        checklist = generate_checklist(ftype)
        if checklist:
            print(f"Summary: {checklist.summary}")
            for item in checklist.items:
                pri = "🔴" if item.priority <= 2 else "🟡" if item.priority <= 4 else "🟢"
                print(f"  {pri} [{item.priority}] {item.title}")
                print(f"      Effort: {item.estimated_effort} | Category: {item.category}")
