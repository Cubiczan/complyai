"use client";

import { useState } from "react";
import Link from "next/link";

const plans = [
  {
    name: "Free",
    subtitle: "Try before you commit",
    price: "$0",
    period: "",
    popular: false,
    features: [
      { text: "1 compliance checklist", included: true },
      { text: "1 document template", included: true },
      { text: "SEC & FinCEN overview", included: true },
      { text: "No monitoring", included: false },
      { text: "No state coverage", included: false },
    ],
    cta: "Get Started",
    href: "/checklist",
    accent: false,
  },
  {
    name: "Compliance",
    subtitle: "For bootstrapped fintechs",
    price: "$49",
    period: "/month",
    popular: true,
    features: [
      { text: "5 compliance checklists/mo", included: true },
      { text: "3 document templates/mo", included: true },
      { text: "SEC, FinCEN, CFPB coverage", included: true },
      { text: "Federal + key states", included: true },
      { text: "Email support", included: true },
    ],
    cta: "Subscribe →",
    href: "#",
    accent: true,
  },
  {
    name: "Growth",
    subtitle: "For scaling fintechs",
    price: "$149",
    period: "/month",
    popular: false,
    features: [
      { text: "Unlimited checklists", included: true },
      { text: "15 document templates/mo", included: true },
      { text: "Everything in Compliance", included: true },
      { text: "Multi-jurisdiction monitoring", included: true },
      { text: "Email change notifications", included: true },
      { text: "Priority 48h support", included: true },
    ],
    cta: "Subscribe →",
    href: "#",
    accent: false,
  },
];

export function PricingTable() {
  return (
    <section id="pricing" className="py-24">
      <div className="max-w-5xl mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Simple pricing. No surprises.
          </h2>
          <p className="text-gray-400 max-w-xl mx-auto">
            No enterprise contracts. No sales calls. Cancel anytime.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={
                plan.popular
                  ? "bg-primary-900/20 border-2 border-primary-600 rounded-2xl p-8 relative glow"
                  : "bg-gray-900/50 border border-gray-800 rounded-2xl p-8"
              }
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-600 text-white text-xs font-semibold px-4 py-1 rounded-full">
                  MOST POPULAR
                </div>
              )}
              <h3 className="text-lg font-semibold mb-1">{plan.name}</h3>
              <p className="text-sm text-gray-500 mb-6">{plan.subtitle}</p>
              <div className="text-3xl font-bold">
                {plan.price}
                {plan.period && (
                  <span className="text-base font-normal text-gray-500">
                    {plan.period}
                  </span>
                )}
              </div>
              {plan.period && (
                <div className="text-sm text-gray-500 mb-6">{plan.period}</div>
              )}
              {!plan.period && <div className="mb-6" />}
              <ul className="space-y-3 text-sm mb-8">
                {plan.features.map((f, i) => (
                  <li key={i} className="flex items-start gap-2">
                    {f.included ? (
                      <span className="text-primary-400 mt-0.5">✓</span>
                    ) : (
                      <span className="text-gray-600 mt-0.5">—</span>
                    )}
                    <span className={f.included ? "" : "text-gray-600"}>
                      {f.text}
                    </span>
                  </li>
                ))}
              </ul>
              {plan.accent ? (
                <a
                  href={plan.href}
                  className="block text-center bg-primary-600 hover:bg-primary-500 text-white font-medium py-2.5 rounded-xl transition"
                >
                  {plan.cta}
                </a>
              ) : (
                <a
                  href={plan.href}
                  className="block text-center border border-gray-700 text-gray-300 hover:border-gray-500 font-medium py-2.5 rounded-xl transition"
                >
                  {plan.cta}
                </a>
              )}
            </div>
          ))}
        </div>
        <div className="mt-8 text-center">
          <div className="inline-flex items-center gap-2 bg-gray-900/50 border border-gray-800 rounded-xl px-6 py-3">
            <span className="text-gray-400 text-sm">
              Need more?{" "}
              <a href="#" className="text-primary-400 hover:text-primary-300">
                Enterprise →
              </a>
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
