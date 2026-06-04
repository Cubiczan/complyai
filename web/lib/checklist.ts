// Checklist generation logic — ported from Python checklist/generator.py

export interface ChecklistItemData {
  title: string;
  section: string | null;
  priority: number; // 1=critical, 10=nice-to-have
  description: string;
  estimatedEffort: "low" | "medium" | "high";
  category: string;
  actionItems: string[];
  resources: { title: string; url: string }[];
}

export interface ChecklistSummary {
  totalItems: number;
  critical: number;
  highPriority: number;
  mediumPriority: number;
  lowPriority: number;
  categories: string[];
  jurisdiction: string;
  generatedAt: string;
}

export interface ComplianceChecklist {
  fintechType: string;
  displayName: string;
  generatedAt: string;
  jurisdiction: string;
  items: ChecklistItemData[];
  summary: ChecklistSummary;
}

// Priority labels
export type PriorityLabel = "critical" | "high" | "medium" | "low";
export function getPriorityLabel(p: number): PriorityLabel {
  if (p <= 2) return "critical";
  if (p <= 4) return "high";
  if (p <= 6) return "medium";
  return "low";
}

// Category label map
const CATEGORY_LABELS: Record<string, string> = {
  aml: "AML / BSA Compliance",
  consumer_protection: "Consumer Protection",
  privacy: "Privacy & Data Protection",
  licensing: "Licensing & Registration",
  securities: "Securities Compliance",
  cybersecurity: "Cybersecurity",
  banking: "Banking / Partnership",
  other: "Other Requirements",
};

export function getCategoryLabel(slug: string): string {
  return CATEGORY_LABELS[slug] ?? slug.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

// Effort heuristics — ported from Python
const EFFORT_MAP: Record<string, "low" | "medium" | "high"> = {
  BSA: "high",
  "Bank Charter": "high",
  "State MTL": "high",
  "23 NYCRR 200": "high",
  "IA-1940": "high",
  "Reg Z": "medium",
  "Reg E": "medium",
  "31 CFR § 1010.230": "medium",
  KYC: "medium",
  CCPA: "medium",
  GLBA: "low",
  OFAC: "medium",
};

function getEffort(section: string | null, title: string): "low" | "medium" | "high" {
  for (const [key, effort] of Object.entries(EFFORT_MAP)) {
    if ((section && section.includes(key)) || title.includes(key)) return effort;
  }
  return "medium";
}

// Category map
const CATEGORY_MAP: Record<string, string> = {
  BSA: "aml",
  "31 CFR": "aml",
  KYC: "aml",
  OFAC: "aml",
  "Reg Z": "consumer_protection",
  "Reg E": "consumer_protection",
  "Reg F": "consumer_protection",
  "Reg DD": "consumer_protection",
  "Reg BI": "securities",
  "IA-1940": "securities",
  "1934 Act": "securities",
  GLBA: "privacy",
  CCPA: "privacy",
  "23 NYCRR": "cybersecurity",
  "State MTL": "licensing",
  "State Lending": "licensing",
  "State Insurance": "licensing",
  "NY BitLicense": "licensing",
  FDIC: "banking",
  CRA: "banking",
};

function getCategory(section: string | null, title: string): string {
  if (section) {
    for (const [key, cat] of Object.entries(CATEGORY_MAP)) {
      if (section.includes(key)) return cat;
    }
  }
  for (const [key, cat] of Object.entries(CATEGORY_MAP)) {
    if (title.includes(key)) return cat;
  }
  return "other";
}

const ACTION_ITEM_TEMPLATES: Record<string, string[]> = {
  bsa: [
    "Designate a BSA/AML compliance officer",
    "Create written AML policies and procedures",
    "Implement transaction monitoring system",
    "Set up SAR/CTR filing process",
    "Schedule annual independent AML audit",
  ],
  kyc: [
    "Implement customer identification program (CIP)",
    "Establish beneficial ownership verification",
    "Set up OFAC/sanctions screening",
    "Define risk-based CDD tiers",
    "Document KYC procedures",
  ],
  consumer_protection: [
    "Draft required consumer disclosures",
    "Implement error resolution procedures",
    "Set up complaint tracking system",
    "Review advertising and marketing materials",
    "Train staff on disclosure requirements",
  ],
  privacy: [
    "Draft and post privacy policy",
    "Implement data inventory and mapping",
    "Set up opt-out mechanism",
    "Review vendor/data processor agreements",
    "Document data retention/deletion procedures",
  ],
  licensing: [
    "Identify state licensing requirements",
    "Prepare license application",
    "Gather required financial statements",
    "Complete background checks for principals",
    "Post surety bond (if required)",
  ],
  securities: [
    "Register with SEC or state securities regulator",
    "Form ADV preparation and filing",
    "Create compliance manual",
    "Implement custody rules",
    "Annual compliance review",
  ],
  cybersecurity: [
    "Conduct risk assessment",
    "Develop information security program",
    "Implement multi-factor authentication",
    "Create incident response plan",
    "Annual penetration testing",
  ],
  banking: [
    "Select bank partner (if neobank)",
    "Review and sign bank partnership agreement",
    "Implement Reg DD disclosures",
    "Set up FDIC pass-through insurance",
    "Compliance with bank oversight requirements",
  ],
};

function getActionItems(category: string, priority: number): string[] {
  const baseItems = ACTION_ITEM_TEMPLATES[category] ?? ["Review regulation requirements"];
  if (priority <= 2) {
    return baseItems.map((item) => `🚨 ${item}`);
  }
  return baseItems;
}

function getResources(section: string | null): { title: string; url: string }[] {
  const resources: { title: string; url: string }[] = [];
  resources.push({
    title: "NCSL State Licensing Overview",
    url: "https://www.ncsl.org/financial-services",
  });
  return resources;
}

import { REGULATORY_PROFILES, FINTECH_TYPES, type RegulationConfig } from "./regulations";

export function generateChecklist(
  fintechType: string,
  jurisdiction: string = "US",
  minPriority: number = 10
): ComplianceChecklist | null {
  const info = FINTECH_TYPES[fintechType];
  if (!info) return null;

  const regs = REGULATORY_PROFILES[fintechType] ?? [];
  const filtered = regs.filter((r) => r.priority <= minPriority);

  const items: ChecklistItemData[] = filtered.map((reg: RegulationConfig) => ({
    title: reg.title,
    section: reg.section,
    priority: reg.priority,
    description: reg.description,
    estimatedEffort: getEffort(reg.section, reg.title),
    category: getCategory(reg.section, reg.title),
    actionItems: getActionItems(getCategory(reg.section, reg.title), reg.priority),
    resources: getResources(reg.section),
  }));

  // Sort by priority (critical first)
  items.sort((a, b) => a.priority - b.priority);

  const critical = items.filter((i) => i.priority <= 2).length;
  const highPriority = items.filter((i) => i.priority >= 3 && i.priority <= 4).length;
  const mediumPriority = items.filter((i) => i.priority >= 5 && i.priority <= 6).length;
  const lowPriority = items.filter((i) => i.priority >= 7).length;
  const categories = [...new Set(items.map((i) => i.category))];

  const now = new Date().toISOString();

  return {
    fintechType,
    displayName: info.display_name,
    generatedAt: now,
    jurisdiction,
    items,
    summary: {
      totalItems: items.length,
      critical,
      highPriority,
      mediumPriority,
      lowPriority,
      categories,
      jurisdiction,
      generatedAt: now,
    },
  };
}
