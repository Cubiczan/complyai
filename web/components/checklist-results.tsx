"use client";

import type { ChecklistItemData, PriorityLabel } from "@/lib/checklist";
import { getPriorityLabel, getCategoryLabel } from "@/lib/checklist";
import { AlertTriangle, CheckCircle, Info, AlertCircle } from "lucide-react";

const priorityConfig: Record<
  PriorityLabel,
  { icon: React.ElementType; color: string; bg: string; label: string }
> = {
  critical: {
    icon: AlertTriangle,
    color: "text-red-400",
    bg: "bg-red-900/20 border-red-800/30",
    label: "Critical",
  },
  high: {
    icon: AlertCircle,
    color: "text-amber-400",
    bg: "bg-amber-900/20 border-amber-800/30",
    label: "High",
  },
  medium: {
    icon: Info,
    color: "text-blue-400",
    bg: "bg-blue-900/20 border-blue-800/30",
    label: "Medium",
  },
  low: {
    icon: CheckCircle,
    color: "text-green-400",
    bg: "bg-green-900/20 border-green-800/30",
    label: "Low",
  },
};

const effortColors: Record<string, string> = {
  high: "text-red-400",
  medium: "text-amber-400",
  low: "text-green-400",
};

export function ChecklistResults({
  items,
  displayName,
}: {
  items: ChecklistItemData[];
  displayName: string;
}) {
  if (items.length === 0) return null;

  // Group by category
  const grouped: Record<string, ChecklistItemData[]> = {};
  items.forEach((item) => {
    if (!grouped[item.category]) grouped[item.category] = [];
    grouped[item.category].push(item);
  });

  return (
    <div className="space-y-12">
      {/* Priority Summary */}
      <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold mb-4">
          {displayName} — Compliance Summary
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {(Object.entries(priorityConfig) as [PriorityLabel, typeof priorityConfig['critical']][]).map(([key, cfg]) => {
            const count = items.filter(
              (i) => getPriorityLabel(i.priority) === key
            ).length;
            return (
              <div
                key={key}
                className={`${cfg.bg} border rounded-xl p-4 text-center`}
              >
                <cfg.icon className={`w-5 h-5 ${cfg.color} mx-auto mb-1`} />
                <div className={`text-2xl font-bold ${cfg.color}`}>
                  {count}
                </div>
                <div className={`text-xs ${cfg.color}`}>{cfg.label}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Items by Category */}
      {Object.entries(grouped).map(([category, catItems]) => (
        <div key={category}>
          <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <span>{getCategoryLabel(category)}</span>
            <span className="text-sm text-gray-500 font-normal">
              ({catItems.length} items)
            </span>
          </h3>
          <div className="space-y-4">
            {catItems.map((item, idx) => {
              const label = getPriorityLabel(item.priority);
              const cfg = priorityConfig[label];
              const Icon = cfg.icon;
              return (
                <div
                  key={idx}
                  className="bg-gray-900/50 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3 flex-1">
                      <Icon
                        className={`w-5 h-5 ${cfg.color} mt-0.5 shrink-0`}
                      />
                      <div>
                        <h4 className="font-semibold text-white">
                          {item.title}
                        </h4>
                        {item.description && (
                          <p className="text-sm text-gray-400 mt-1">
                            {item.description}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span
                        className={`text-xs font-medium px-2 py-0.5 rounded-full ${cfg.bg} ${cfg.color}`}
                      >
                        {cfg.label}
                      </span>
                      {item.section && (
                        <span className="text-xs text-gray-500 bg-gray-800/50 px-2 py-0.5 rounded-full">
                          {item.section}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Action Items */}
                  {item.actionItems.length > 0 && (
                    <div className="mt-3 pl-8">
                      <p className="text-xs text-gray-500 mb-1">
                        Action items:
                      </p>
                      <ul className="space-y-0.5">
                        {item.actionItems.map((action, ai) => (
                          <li
                            key={ai}
                            className="text-sm text-gray-300 flex items-start gap-2"
                          >
                            <span className="text-primary-400 mt-0.5 shrink-0">
                              →
                            </span>
                            {action}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Metadata */}
                  <div className="mt-3 pl-8 flex items-center gap-4 text-xs text-gray-500">
                    <span>
                      Effort:{" "}
                      <span
                        className={`font-medium ${effortColors[item.estimatedEffort] ?? "text-gray-400"}`}
                      >
                        {item.estimatedEffort}
                      </span>
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
