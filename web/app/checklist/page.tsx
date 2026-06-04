"use client";

import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { ChecklistResults } from "@/components/checklist-results";
import { FINTECH_TYPES } from "@/lib/regulations";
import { generateChecklist } from "@/lib/checklist";
import { ArrowRight, ChevronDown, Sparkles } from "lucide-react";

export default function ChecklistPage() {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [checklist, setChecklist] = useState<ReturnType<typeof generateChecklist> | null>(null);

  const handleSelect = (slug: string) => {
    setSelectedType(slug);
    const result = generateChecklist(slug);
    setChecklist(result);
  };

  return (
    <>
      <Navbar />
      <section className="py-16 md:py-24">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 bg-primary-900/30 border border-primary-700/30 rounded-full px-4 py-1.5 text-sm text-primary-300 mb-6">
              <Sparkles className="w-4 h-4" />
              Free compliance audit
            </div>
            <h1 className="text-3xl md:text-5xl font-extrabold mb-4">
              Compliance <span className="gradient-text">Checklist</span>
            </h1>
            <p className="text-gray-400 max-w-xl mx-auto">
              Select your fintech type and get a prioritized compliance checklist
              with action items, effort estimates, and resources.
            </p>
          </div>

          {!checklist && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
              {Object.entries(FINTECH_TYPES).map(([slug, info]) => (
                <button
                  key={slug}
                  onClick={() => handleSelect(slug)}
                  className="bg-gray-900/50 border border-gray-800 rounded-xl p-5 text-left hover:border-primary-700/50 transition group"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-white group-hover:text-primary-400 transition">
                      {info.display_name}
                    </h3>
                    <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-primary-400 transition" />
                  </div>
                  <p className="text-xs text-gray-500">{info.description}</p>
                  <div className="flex gap-1.5 mt-2">
                    {info.examples.slice(0, 2).map((ex) => (
                      <span
                        key={ex}
                        className="text-xs text-gray-600 bg-gray-800/50 px-2 py-0.5 rounded"
                      >
                        {ex}
                      </span>
                    ))}
                    {info.examples.length > 2 && (
                      <span className="text-xs text-gray-600">
                        +{info.examples.length - 2}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          )}

          {checklist && checklist.items.length > 0 && (
            <>
              <button
                onClick={() => {
                  setSelectedType(null);
                  setChecklist(null);
                }}
                className="mb-8 text-sm text-gray-400 hover:text-white transition"
              >
                ← Back to fintech types
              </button>
              <ChecklistResults
                items={checklist.items}
                displayName={checklist.displayName}
              />
            </>
          )}

          {checklist && checklist.items.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-400">
                No checklist items found for this type.
              </p>
              <button
                onClick={() => {
                  setSelectedType(null);
                  setChecklist(null);
                }}
                className="mt-4 text-primary-400 hover:text-primary-300 transition"
              >
                ← Try another type
              </button>
            </div>
          )}
        </div>
      </section>
      <Footer />
    </>
  );
}
