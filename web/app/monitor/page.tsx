"use client";

import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { MonitorFeed } from "@/components/monitor-feed";
import { Filter, Bell, RefreshCw } from "lucide-react";

const ALL_CHANGES = [
  {
    title: "CFPB Updates Remittance Transfer Rule Thresholds",
    agency: "CFPB",
    changeType: "updated",
    summary:
      "CFPB revised the safe harbor thresholds for remittance transfers under Regulation E. New threshold: $125 (from $100) for error resolution disclosures.",
    affectedTypes: ["payments", "banking", "p2p"],
    severity: "warning" as const,
    effectiveDate: "2026-07-01",
    timestamp: new Date(Date.now() - 2 * 3600 * 1000).toISOString(),
  },
  {
    title: "FinCEN Issues New Guidance on Beneficial Ownership Reporting",
    agency: "FinCEN",
    changeType: "new",
    summary:
      "FinCEN published updated guidance on the Corporate Transparency Act beneficial ownership information (BOI) reporting requirements. New reporting portal available June 15.",
    affectedTypes: ["payments", "lending", "crypto", "p2p", "banking", "wealth"],
    severity: "critical" as const,
    effectiveDate: "2026-06-15",
    timestamp: new Date(Date.now() - 6 * 3600 * 1000).toISOString(),
  },
  {
    title: "SEC Proposes Amendments to Marketing Rule",
    agency: "SEC",
    changeType: "proposed",
    summary:
      "SEC proposed amendments to Rule 206(4)-1 (Marketing Rule) affecting how investment advisors present performance data and testimonials. Comment period ends August 30.",
    affectedTypes: ["wealth"],
    severity: "warning" as const,
    effectiveDate: "2027-01-01",
    timestamp: new Date(Date.now() - 24 * 3600 * 1000).toISOString(),
  },
  {
    title: "NYDFS Fines Three Fintechs for Cybersecurity Violations",
    agency: "NYDFS",
    changeType: "enforcement",
    summary:
      "NYDFS announced enforcement actions against three fintech companies for violations of 23 NYCRR Part 500. Total fines: $2.1M. Highlights need for multi-factor authentication and incident response plans.",
    affectedTypes: ["payments", "lending", "crypto", "p2p", "banking", "insurance"],
    severity: "warning" as const,
    timestamp: new Date(Date.now() - 2 * 24 * 3600 * 1000).toISOString(),
  },
  {
    title: "New State-Level Data Privacy Laws Take Effect",
    agency: "State Regulators",
    changeType: "new",
    summary:
      "Texas, Florida, and Washington data privacy laws go into effect. Requirements include opt-out mechanisms, data access rights, and enhanced consent for sensitive data processing.",
    affectedTypes: ["payments", "lending", "crypto", "p2p", "banking", "wealth", "insurance"],
    severity: "warning" as const,
    effectiveDate: "2026-09-01",
    timestamp: new Date(Date.now() - 3 * 24 * 3600 * 1000).toISOString(),
  },
  {
    title: "OCC Updates Bank Partnership Guidance",
    agency: "OCC",
    changeType: "updated",
    summary:
      "OCC published revised guidance on bank-fintech partnerships, including risk management expectations for third-party relationships and fair lending compliance.",
    affectedTypes: ["banking", "lending"],
    severity: "info" as const,
    timestamp: new Date(Date.now() - 5 * 24 * 3600 * 1000).toISOString(),
  },
  {
    title: "California DFPI Extends Crypto Licensing Deadline",
    agency: "California DFPI",
    changeType: "updated",
    summary:
      "DFPI extended the compliance deadline for the California Digital Financial Assets Law. Licensed exchange requirement now effective December 2027.",
    affectedTypes: ["crypto"],
    severity: "info" as const,
    effectiveDate: "2027-12-01",
    timestamp: new Date(Date.now() - 7 * 24 * 3600 * 1000).toISOString(),
  },
  {
    title: "FinCEN SAR Filing Rate Increases 15% Year-Over-Year",
    agency: "FinCEN",
    changeType: "report",
    summary:
      "FinCEN reports 15% increase in SAR filings for 2025. Virtual currency-related SARs up 37%. Highlights growing scrutiny on crypto transaction monitoring.",
    affectedTypes: ["payments", "lending", "crypto", "p2p", "banking", "wealth"],
    severity: "info" as const,
    timestamp: new Date(Date.now() - 10 * 24 * 3600 * 1000).toISOString(),
  },
];

export default function MonitorPage() {
  const [filterType, setFilterType] = useState<string>("all");

  const filteredChanges =
    filterType === "all"
      ? ALL_CHANGES
      : ALL_CHANGES.filter((c) => c.affectedTypes.includes(filterType));

  return (
    <>
      <Navbar />
      <section className="py-16 md:py-24">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-3xl md:text-5xl font-extrabold mb-4">
              Regulatory <span className="gradient-text">Monitor</span>
            </h1>
            <p className="text-gray-400 max-w-xl mx-auto">
              Track regulatory changes from SEC, CFPB, FinCEN, NYDFS, and state
              regulators. Filter by fintech type to see what matters to you.
            </p>
          </div>

          {/* Filter */}
          <div className="flex items-center gap-3 mb-8 flex-wrap">
            <Filter className="w-4 h-4 text-gray-500" />
            <button
              onClick={() => setFilterType("all")}
              className={`text-sm px-3 py-1.5 rounded-lg border transition ${
                filterType === "all"
                  ? "bg-primary-900/30 border-primary-700 text-primary-300"
                  : "border-gray-700 text-gray-400 hover:border-gray-500"
              }`}
            >
              All Changes
            </button>
            {[
              "payments",
              "lending",
              "crypto",
              "p2p",
              "banking",
              "wealth",
              "insurance",
            ].map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`text-sm px-3 py-1.5 rounded-lg border capitalize transition ${
                  filterType === type
                    ? "bg-primary-900/30 border-primary-700 text-primary-300"
                    : "border-gray-700 text-gray-400 hover:border-gray-500"
                }`}
              >
                {type}
              </button>
            ))}
          </div>

          <MonitorFeed changes={filteredChanges} />
        </div>
      </section>
      <Footer />
    </>
  );
}
