"use client";

import { useState, useMemo } from "react";
import type { TemplateMeta } from "@/lib/templates";
import {
  getTemplateContent,
  extractVariables,
  renderTemplate,
} from "@/lib/templates";

export function TemplateRenderer({
  template,
}: {
  template: TemplateMeta;
}) {
  const content = getTemplateContent(template.slug);
  const variables = useMemo(
    () => (content ? extractVariables(content) : []),
    [content]
  );

  const [values, setValues] = useState<Record<string, string>>({});
  const [rendered, setRendered] = useState<string | null>(null);
  const [copyText, setCopyText] = useState("Copy");

  const handleChange = (key: string, value: string) => {
    setValues((prev) => ({ ...prev, [key]: value }));
  };

  const generate = () => {
    const result = renderTemplate(template.slug, values);
    setRendered(result);
  };

  const copyToClipboard = async () => {
    if (rendered) {
      await navigator.clipboard.writeText(rendered);
      setCopyText("Copied!");
      setTimeout(() => setCopyText("Copy"), 2000);
    }
  };

  return (
    <div className="grid lg:grid-cols-2 gap-8">
      {/* Variables Form */}
      <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold mb-1">{template.name}</h3>
        <p className="text-sm text-gray-400 mb-4">{template.description}</p>
        <p className="text-xs text-gray-500 mb-6">
          Fill in the variables below and click Generate to render your
          document.
        </p>

        <div className="space-y-4 mb-6">
          {variables.map((v) => (
            <div key={v}>
              <label className="block text-xs text-gray-500 mb-1 uppercase tracking-wider">
                {v.replace(/_/g, " ")}
              </label>
              <input
                type="text"
                value={values[v] ?? ""}
                onChange={(e) => handleChange(v, e.target.value)}
                placeholder={`Enter ${v.replace(/_/g, " ")}`}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-primary-500 transition"
              />
            </div>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={generate}
            className="bg-primary-600 hover:bg-primary-500 text-white font-medium px-6 py-2.5 rounded-lg transition text-sm"
          >
            Generate Document
          </button>
          <button
            onClick={() => {
              setValues({});
              setRendered(null);
            }}
            className="text-gray-400 hover:text-white border border-gray-700 hover:border-gray-500 font-medium px-4 py-2.5 rounded-lg transition text-sm"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Rendered Output */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-300">
            {rendered ? "Rendered Document" : "Preview"}
          </h3>
          {rendered && (
            <button
              onClick={copyToClipboard}
              className="text-xs text-primary-400 hover:text-primary-300 transition"
            >
              {copyText}
            </button>
          )}
        </div>
        {rendered ? (
          <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-6 overflow-auto max-h-[70vh]">
            <pre className="text-sm text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
              {rendered}
            </pre>
          </div>
        ) : (
          <div className="bg-gray-900/30 border border-gray-800 rounded-2xl p-6 flex items-center justify-center h-64">
            <p className="text-gray-500 text-sm">
              Fill in the variables and click Generate
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
