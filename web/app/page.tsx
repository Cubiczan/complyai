import { Navbar } from "@/components/navbar";
import { Hero } from "@/components/hero";
import { Features } from "@/components/features";
import { PricingTable } from "@/components/pricing-table";
import { Footer } from "@/components/footer";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <Hero />

      {/* Stats bar */}
      <section className="py-20 border-b border-gray-800/50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { value: "$49", label: "Starting price /mo" },
              { value: "90%", label: "Less than alternatives" },
              { value: "No", label: "Sales calls required" },
              { value: "Real", label: "Documents, not just checklists" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl font-bold gradient-text">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-500 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Features />

      {/* How it works */}
      <section id="how" className="py-24 bg-gray-900/30">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              How it works
            </h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              Three steps from zero to compliance-ready.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 text-center">
            {[
              {
                emoji: "🔍",
                title: "1. Select your fintech type",
                desc: "Payments, lending, crypto, P2P, banking, wealth, or insurance.",
              },
              {
                emoji: "✅",
                title: "2. Get your checklist",
                desc: "We generate a prioritized compliance checklist with action items and resources.",
              },
              {
                emoji: "📄",
                title: "3. Generate documents",
                desc: "Fill your company details into our templates. ToS, Privacy Policy, disclosures.",
              },
            ].map((step) => (
              <div key={step.title}>
                <div className="w-16 h-16 mx-auto bg-primary-900/30 rounded-2xl flex items-center justify-center mb-5 glow">
                  <span className="text-3xl">{step.emoji}</span>
                </div>
                <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
                <p className="text-gray-400 text-sm">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <PricingTable />

      {/* Comparison table */}
      <section id="comparison" className="py-24 bg-gray-900/30">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              complyAI vs the enterprise
            </h2>
            <p className="text-gray-400">
              Why pay for features you don't need?
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800">
                  <th className="text-left py-4 pr-4"></th>
                  <th className="text-center py-4 px-4 text-primary-400 font-semibold">
                    complyAI
                  </th>
                  <th className="text-center py-4 px-4 text-gray-500">
                    ComplyAdvantage
                  </th>
                  <th className="text-center py-4 px-4 text-gray-500">
                    Ascent
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                {[
                  ["Starting price", "$49/mo", "$500+/mo", "$1,000+/mo"],
                  ["Self-service signup", "✅", "❌", "❌"],
                  ["Real document generation", "✅", "❌", "❌"],
                  ["Change monitoring", "✅", "✅", "✅"],
                  ["No sales calls", "✅", "❌", "❌"],
                  ["Built for indie fintechs", "✅", "❌", "❌"],
                ].map((row, i) => (
                  <tr key={i}>
                    <td className="py-4 pr-4 text-gray-400">{row[0]}</td>
                    <td className="py-4 px-4 text-center font-semibold text-primary-400">
                      {row[1]}
                    </td>
                    <td className="py-4 px-4 text-center text-gray-500">
                      {row[2]}
                    </td>
                    <td className="py-4 px-4 text-center text-gray-500">
                      {row[3]}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="py-24">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">FAQ</h2>
          <div className="space-y-4">
            {[
              {
                q: "Is complyAI a replacement for a lawyer?",
                a: "No. complyAI is a tool to help you understand what regulations apply, generate document templates, and monitor changes. It is not legal advice. We strongly recommend reviewing outputs with a qualified attorney.",
              },
              {
                q: "Which fintech types do you support?",
                a: "Payments, lending, crypto/digital assets, P2P, neobanking, wealth/investment, and insurtech. We're adding more based on user demand.",
              },
              {
                q: "What states do you cover?",
                a: "Currently: New York (DFS), California (DFPI), and Texas (Dept of Banking). We're expanding to all 50 states. The Growth plan includes multi-jurisdiction support.",
              },
              {
                q: "Can I cancel anytime?",
                a: "Yes. No contracts, no commitments. Cancel from your dashboard, and your subscription ends at the billing period.",
              },
              {
                q: "How is this different from ComplyAdvantage?",
                a: "complyAI is built for indie fintechs. We're self-service, 90% cheaper, and generate real documents (ToS, Privacy Policies, disclosures) — not just checklists. No sales calls, no enterprise onboarding.",
              },
            ].map((faq) => (
              <details
                key={faq.q}
                className="bg-gray-900/50 border border-gray-800 rounded-xl p-5 group"
              >
                <summary className="font-semibold cursor-pointer flex items-center justify-between list-none">
                  {faq.q}
                  <span className="text-gray-500 group-open:rotate-180 transition">
                    ▼
                  </span>
                </summary>
                <p className="text-gray-400 mt-3 text-sm leading-relaxed">
                  {faq.a}
                </p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="hero-gradient py-24">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to get compliant?
          </h2>
          <p className="text-gray-400 mb-8 max-w-lg mx-auto">
            3,000+ indie fintechs already trust complyAI. Join them and stop
            worrying about regulatory surprises.
          </p>
          <a
            href="/checklist"
            className="inline-block bg-primary-600 hover:bg-primary-500 text-white font-semibold px-8 py-3.5 rounded-xl text-lg transition glow"
          >
            Start Free →
          </a>
          <p className="text-sm text-gray-500 mt-4">
            Free compliance audit. No credit card needed.
          </p>
        </div>
      </section>

      <Footer />
    </>
  );
}
