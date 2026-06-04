"use client";

import { AlertTriangle, AlertCircle, Info, ExternalLink, Clock } from "lucide-react";
import { formatDate } from "@/lib/utils";

interface Change {
  title: string;
  agency: string;
  changeType: string;
  summary: string;
  affectedTypes: string[];
  severity: "critical" | "warning" | "info";
  effectiveDate?: string;
  sourceUrl?: string;
  timestamp: string;
}

const severityConfig = {
  critical: {
    icon: AlertTriangle,
    color: "text-red-400",
    bg: "bg-red-900/20 border-red-800/30",
    label: "Critical",
  },
  warning: {
    icon: AlertCircle,
    color: "text-amber-400",
    bg: "bg-amber-900/20 border-amber-800/30",
    label: "Warning",
  },
  info: {
    icon: Info,
    color: "text-blue-400",
    bg: "bg-blue-900/20 border-blue-800/30",
    label: "Info",
  },
};

const changeTypeLabels: Record<string, string> = {
  new: "New Rule",
  updated: "Updated",
  amended: "Amended",
  repealed: "Repealed",
  proposed: "Proposed",
  enforcement: "Enforcement",
  report: "Report",
};

const agencyColors: Record<string, string> = {
  CFPB: "bg-emerald-900/30 text-emerald-300",
  FinCEN: "bg-indigo-900/30 text-indigo-300",
  SEC: "bg-blue-900/30 text-blue-300",
  NYDFS: "bg-purple-900/30 text-purple-300",
  "State Regulators": "bg-orange-900/30 text-orange-300",
  OCC: "bg-cyan-900/30 text-cyan-300",
  "California DFPI": "bg-yellow-900/30 text-yellow-300",
};

export function MonitorFeed({ changes }: { changes: Change[] }) {
  if (changes.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No changes match your filter.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {changes.map((change, idx) => {
        const sev = severityConfig[change.severity];
        const SevIcon = sev.icon;
        const age = getAgeString(change.timestamp);

        return (
          <div
            key={idx}
            className={`${sev.bg} border rounded-xl p-5 transition`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3 flex-1">
                <SevIcon className={`w-5 h-5 ${sev.color} mt-0.5 shrink-0`} />
                <div>
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <h3 className="font-semibold text-white text-sm">
                      {change.title}
                    </h3>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full ${agencyColors[change.agency] ?? "bg-gray-800 text-gray-400"}`}
                    >
                      {change.agency}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${sev.bg} ${sev.color}`}>
                      {changeTypeLabels[change.changeType] ?? change.changeType}
                    </span>
                  </div>
                  <p className="text-sm text-gray-400 mt-1">
                    {change.summary}
                  </p>
                  <div className="flex items-center gap-3 mt-3 text-xs text-gray-500 flex-wrap">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {age}
                    </span>
                    {change.effectiveDate && (
                      <span>Effective: {change.effectiveDate}</span>
                    )}
                    <div className="flex gap-1.5">
                      {change.affectedTypes.map((t) => (
                        <span
                          key={t}
                          className="text-xs bg-gray-800/50 px-1.5 py-0.5 rounded text-gray-500 capitalize"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              <span
                className={`text-xs font-medium px-2 py-0.5 rounded-full ${sev.bg} ${sev.color} shrink-0`}
              >
                {sev.label}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function getAgeString(iso: string): string {
  const ms = Date.now() - new Date(iso).getTime();
  const hours = Math.floor(ms / 3600000);
  if (hours < 1) return "Just now";
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}
