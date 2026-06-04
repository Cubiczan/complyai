"use client";

import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { TemplateRenderer } from "@/components/template-renderer";
import { TEMPLATE_METADATA, getAvailableTemplates } from "@/lib/templates";
import type { TemplateMeta } from "@/lib/templates";
import { FileText, ChevronDown } from "lucide-react";

export default function TemplatesPage() {
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateMeta | null>(
    null
  );

  return (
    <>
      <Navbar />
      <section className="py-16 md:py-24">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-3xl md:text-5xl font-extrabold mb-4">
              Document <span className="gradient-text">Templates</span>
            </h1>
            <p className="text-gray-400 max-w-xl mx-auto">
              Generate legal documents ready for your fintech. Fill in your
              company details, and we handle the rest.
            </p>
          </div>

          {!selectedTemplate && (
            <div className="grid md:grid-cols-2 gap-4">
              {TEMPLATE_METADATA.map((t) => (
                <button
                  key={t.slug}
                  onClick={() => setSelectedTemplate(t)}
                  className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 text-left hover:border-primary-700/50 transition group"
                >
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 bg-primary-900/30 rounded-xl flex items-center justify-center shrink-0">
                      <FileText className="w-5 h-5 text-primary-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white group-hover:text-primary-400 transition">
                        {t.name}
                      </h3>
                      <p className="text-sm text-gray-400 mt-1">
                        {t.description}
                      </p>
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        {t.applicableTypes.map((at) => (
                          <span
                            key={at}
                            className="text-xs text-gray-600 bg-gray-800/50 px-2 py-0.5 rounded"
                          >
                            {at}
                          </span>
                        ))}
                      </div>
                    </div>
                    <ChevronDown className="w-4 h-4 text-gray-600 group-hover:text-primary-400 transition -rotate-90 shrink-0" />
                  </div>
                </button>
              ))}
            </div>
          )}

          {selectedTemplate && (
            <div>
              <button
                onClick={() => setSelectedTemplate(null)}
                className="mb-8 text-sm text-gray-400 hover:text-white transition"
              >
                ← Back to templates
              </button>
              <TemplateRenderer template={selectedTemplate} />
            </div>
          )}
        </div>
      </section>
      <Footer />
    </>
  );
}
