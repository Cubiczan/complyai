// Registry data for all 7 fintech types x regulations
// Ported from Python checklist/types.py

export interface FintechTypeInfo {
  display_name: string;
  description: string;
  examples: string[];
}

export const FINTECH_TYPES: Record<string, FintechTypeInfo> = {
  payments: {
    display_name: "Payments / Money Transfer",
    description: "Process payments, money transfers, or remittances",
    examples: ["Stripe", "Square", "Wise", "Remitly"],
  },
  lending: {
    display_name: "Lending / Credit",
    description: "Provide consumer or business loans, credit, or BNPL",
    examples: ["Affirm", "Upstart", "Klarna", "LendingClub"],
  },
  crypto: {
    display_name: "Crypto / Digital Assets",
    description: "Exchange, custody, or deal in cryptocurrencies and digital assets",
    examples: ["Coinbase", "Kraken", "Circle"],
  },
  p2p: {
    display_name: "Peer-to-Peer / Marketplace",
    description: "Platform-based financial transactions between users",
    examples: ["Venmo", "Zelle", "PayPal"],
  },
  banking: {
    display_name: "Neobank / Digital Banking",
    description: "Digital-first banking services, deposits, checking/savings",
    examples: ["Chime", "Revolut", "Monzo", "Current"],
  },
  wealth: {
    display_name: "Wealth / Investments",
    description: "Investment advisory, robo-advising, portfolio management",
    examples: ["Robinhood", "Betterment", "Wealthfront"],
  },
  insurance: {
    display_name: "Insurance / InsurTech",
    description: "Insurance products, distribution, or underwriting",
    examples: ["Lemonade", "Hippo", "Root Insurance"],
  },
};

export interface RegulationConfig {
  title: string;
  section: string | null;
  priority: number; // 1=critical, 10=nice-to-have
  description: string;
  jurisdiction: string;
}

export const REGULATORY_PROFILES: Record<string, RegulationConfig[]> = {
  payments: [
    { title: "Bank Secrecy Act (BSA) Program", section: "BSA", priority: 1, description: "Must have AML program, file SARs and CTRs as required", jurisdiction: "Federal" },
    { title: "Customer Due Diligence / KYC", section: "31 CFR § 1010.230", priority: 1, description: "Verify customer identity, beneficial ownership for business accounts", jurisdiction: "Federal" },
    { title: "Money Transmitter License", section: "State MTL", priority: 1, description: "Licensing in each state where money transmission occurs", jurisdiction: "State" },
    { title: "Regulation E — Electronic Fund Transfers", section: "Reg E", priority: 2, description: "Error resolution, unauthorized transfer liability limits", jurisdiction: "Federal" },
    { title: "Remittance Transfer Rule", section: "Reg E Subpart B", priority: 2, description: "If offering international transfers: disclosure rates, fees, delivery", jurisdiction: "Federal" },
    { title: "NYDFS Cybersecurity Regulation", section: "23 NYCRR 500", priority: 3, description: "If operating in NY: cybersecurity program required", jurisdiction: "State" },
    { title: "Privacy / GLBA Compliance", section: "GLBA", priority: 3, description: "Privacy notices, opt-out rights for sharing nonpublic personal info", jurisdiction: "Federal" },
    { title: "CCPA Compliance (if CA operations)", section: "CCPA", priority: 4, description: "California consumer privacy rights: access, deletion, opt-out", jurisdiction: "State" },
  ],
  lending: [
    { title: "Truth in Lending Act / Regulation Z", section: "Reg Z", priority: 1, description: "APR, finance charge, payment schedule disclosures. Ability-to-repay requirements.", jurisdiction: "Federal" },
    { title: "Fair Lending / ECOA Compliance", section: "ECOA", priority: 1, description: "Equal Credit Opportunity Act: no discrimination in lending", jurisdiction: "Federal" },
    { title: "BSA/AML Program", section: "BSA", priority: 1, description: "AML program, SAR filings, currency transaction reporting", jurisdiction: "Federal" },
    { title: "Lending License(s)", section: "State Lending", priority: 1, description: "License in each state where loans originate. Interest rate limits.", jurisdiction: "State" },
    { title: "Regulation E (if ACH/EFT involved)", section: "Reg E", priority: 2, description: "Electronic fund transfers: error resolution, statements", jurisdiction: "Federal" },
    { title: "Debt Collection Rules / Reg F", section: "Reg F", priority: 2, description: "If collecting debts: call limits, validation notices", jurisdiction: "Federal" },
    { title: "Small Business Lending Rule (1071)", section: "1071 Rule", priority: 3, description: "If small business lending: data collection on demographics", jurisdiction: "Federal" },
    { title: "NY DFS Cybersecurity Regulation", section: "23 NYCRR 500", priority: 3, description: "NY operations require cybersecurity program", jurisdiction: "State" },
    { title: "GLBA Privacy Compliance", section: "GLBA", priority: 3, description: "Privacy policies and opt-out notices", jurisdiction: "Federal" },
  ],
  crypto: [
    { title: "BSA/AML Program (for virtual currency)", section: "BSA", priority: 1, description: "AML program must cover virtual currency activities. SARs for VC transactions.", jurisdiction: "Federal" },
    { title: "Money Transmitter License", section: "State MTL", priority: 1, description: "Most states require MTL for crypto exchange/custody activities", jurisdiction: "State" },
    { title: "NY BitLicense (if NY operations)", section: "23 NYCRR 200", priority: 1, description: "NY-specific virtual currency license. Capital/reserve requirements.", jurisdiction: "State" },
    { title: "Travel Rule Compliance", section: "FinCEN Travel Rule", priority: 1, description: "Transmit originator and beneficiary info for VC transactions over $3,000", jurisdiction: "Federal" },
    { title: "Customer Due Diligence / KYC", section: "31 CFR § 1010.230", priority: 1, description: "Verify customer identity, monitor transactions", jurisdiction: "Federal" },
    { title: "SEC Securities Considerations", section: "SEC Crypto", priority: 2, description: "Determine if tokens are securities. Reg D/Reg CF if issuing tokens.", jurisdiction: "Federal" },
    { title: "CFTC Digital Commodity Compliance", section: "CFTC", priority: 2, description: "If trading digital commodities: registration, reporting", jurisdiction: "Federal" },
    { title: "OFAC Sanctions Screening", section: "OFAC", priority: 1, description: "Screen customers against sanctions lists. Block prohibited transactions.", jurisdiction: "Federal" },
  ],
  p2p: [
    { title: "Money Transmitter License", section: "State MTL", priority: 1, description: "P2P payment platforms require MTL in most states", jurisdiction: "State" },
    { title: "BSA/AML Program", section: "BSA", priority: 1, description: "AML program with SAR/CTR filing requirements", jurisdiction: "Federal" },
    { title: "Customer Due Diligence / KYC", section: "31 CFR § 1010.230", priority: 1, description: "Verify user identity, at least for transaction thresholds", jurisdiction: "Federal" },
    { title: "Regulation E", section: "Reg E", priority: 2, description: "Electronic fund transfer protections for consumer accounts", jurisdiction: "Federal" },
    { title: "GLBA Privacy Compliance", section: "GLBA", priority: 3, description: "Privacy notices and data sharing disclosures", jurisdiction: "Federal" },
    { title: "NYDFS Cybersecurity Regulation", section: "23 NYCRR 500", priority: 3, description: "NY operations, regardless of size, require cybersecurity compliance", jurisdiction: "State" },
  ],
  banking: [
    { title: "Bank Charter / Partnership Requirements", section: "Banking", priority: 1, description: "Either obtain bank charter or partner with FDIC-insured bank", jurisdiction: "Federal" },
    { title: "BSA/AML Program (full)", section: "BSA", priority: 1, description: "Full AML program: officer, training, independent testing", jurisdiction: "Federal" },
    { title: "Customer Due Diligence / KYC / Beneficial Ownership", section: "31 CFR § 1010.230", priority: 1, description: "Full CDD: identity verification, beneficial ownership", jurisdiction: "Federal" },
    { title: "Regulation E — Electronic Fund Transfers", section: "Reg E", priority: 1, description: "Full error resolution, unauthorized transfer liability, periodic statements", jurisdiction: "Federal" },
    { title: "Regulation DD — Truth in Savings", section: "Reg DD", priority: 1, description: "Disclose APY, fees, minimum balance requirements for deposit accounts", jurisdiction: "Federal" },
    { title: "FDIC Requirements", section: "FDIC", priority: 1, description: "FDIC insurance, signage, recordkeeping for insured deposits", jurisdiction: "Federal" },
    { title: "Community Reinvestment Act (if applicable)", section: "CRA", priority: 2, description: "If FDIC-insured: serve credit needs of entire community", jurisdiction: "Federal" },
    { title: "NYDFS Cybersecurity Regulation", section: "23 NYCRR 500", priority: 1, description: "NY banking operations: strict cybersecurity requirements", jurisdiction: "State" },
  ],
  wealth: [
    { title: "Investment Advisers Act Registration", section: "IA-1940", priority: 1, description: "Register with SEC ($100M+ AUM) or state (<$100M AUM)", jurisdiction: "Federal" },
    { title: "Anti-Fraud (Rule 10b-5)", section: "1934 Act", priority: 1, description: "No deceptive practices in connection with securities transactions", jurisdiction: "Federal" },
    { title: "Customer Due Diligence / KYC", section: "KYC", priority: 2, description: "Verify client identity, suitability of investments", jurisdiction: "Federal" },
    { title: "BSA/AML Program", section: "BSA", priority: 2, description: "AML program for investment advisors with securities accounts", jurisdiction: "Federal" },
    { title: "Regulation Best Interest (Reg BI)", section: "Reg BI", priority: 2, description: "Broker-dealer standard of conduct: best interest, no conflicts", jurisdiction: "Federal" },
    { title: "Marketing Rule (Advisers Act Rule 206(4)-1)", section: "Marketing Rule", priority: 2, description: "Testimonials, performance advertising, and social media compliance", jurisdiction: "Federal" },
    { title: "Privacy / Reg S-P", section: "Reg S-P", priority: 3, description: "Privacy notice delivery, opt-out for sharing nonpublic info", jurisdiction: "Federal" },
  ],
  insurance: [
    { title: "Insurance License", section: "State Insurance", priority: 1, description: "License in each state where insurance is sold or underwritten", jurisdiction: "State" },
    { title: "Rate and Form Filing", section: "Insurance Filing", priority: 1, description: "File rates and policy forms with state insurance departments", jurisdiction: "State" },
    { title: "Producer Licensing", section: "Insurance Producer", priority: 1, description: "Licensed agents/producers for insurance sales", jurisdiction: "State" },
    { title: "Consumer Privacy / GLBA", section: "GLBA", priority: 2, description: "Privacy notices required. Medical info has heightened protections.", jurisdiction: "Federal" },
    { title: "Fair Claims Practices", section: "Claims", priority: 2, description: "Prompt, fair claims handling per state Unfair Claims Practices Acts", jurisdiction: "State" },
    { title: "NAIC Model Regulations", section: "NAIC", priority: 3, description: "Model regulations for market conduct, solvency, and data security", jurisdiction: "State" },
    { title: "NYDFS Cybersecurity Regulation", section: "23 NYCRR 500", priority: 3, description: "NY: data security program for insurance companies", jurisdiction: "State" },
  ],
};

export function getFintechInfo(slug: string): FintechTypeInfo | null {
  return FINTECH_TYPES[slug] ?? null;
}

export function getRegulationsForType(
  fintechType: string,
  minPriority: number = 10
): RegulationConfig[] {
  const regs = REGULATORY_PROFILES[fintechType] ?? [];
  return regs.filter((r) => r.priority <= minPriority);
}
