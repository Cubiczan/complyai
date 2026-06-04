import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { PricingTable } from "@/components/pricing-table";

export default function PricingPage() {
  return (
    <>
      <Navbar />
      <section className="pt-24 pb-0">
        <div className="max-w-5xl mx-auto px-4 text-center mb-8">
          <h1 className="text-3xl md:text-5xl font-extrabold mb-4">
            Simple <span className="gradient-text">Pricing</span>
          </h1>
          <p className="text-gray-400 max-w-xl mx-auto">
            No enterprise contracts. No sales calls. Cancel anytime.
          </p>
        </div>
      </section>
      <PricingTable />
      <section className="pb-24" />

      {/* Comparison table */}
      <section className="py-24 bg-gray-900/30">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Detailed Feature Comparison
            </h2>
            <p className="text-gray-400">
              See exactly what each plan includes.
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800">
                  <th className="text-left py-4 pr-4 text-gray-400">Feature</th>
                  <th className="text-center py-4 px-4 text-gray-500">Free</th>
                  <th className="text-center py-4 px-4 text-primary-400 font-semibold">
                    Compliance
                  </th>
                  <th className="text-center py-4 px-4 text-gray-500">
                    Growth
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                {[
                  ["Compliance checklists", "1", "5/mo", "Unlimited"],
                  ["Document templates", "1", "3/mo", "15/mo"],
                  ["All document templates", "❌", "✅", "✅"],
                  ["SEC coverage", "✅", "✅", "✅"],
                  ["FinCEN coverage", "✅", "✅", "✅"],
                  ["CFPB coverage", "❌", "✅", "✅"],
                  ["State regulator coverage", "❌", "Key states", "All 50"],
                  ["Regulatory monitoring", "❌", "✅", "✅"],
                  ["Change notifications", "❌", "Email", "Email + Slack"],
                  ["Support", "Community", "Email", "Priority 48h"],
                ].map((row, i) => (
                  <tr key={i}>
                    <td className="py-3 pr-4 text-gray-300">{row[0]}</td>
                    <td className="py-3 px-4 text-center text-gray-500">
                      {row[1]}
                    </td>
                    <td className="py-3 px-4 text-center text-primary-400">
                      {row[2]}
                    </td>
                    <td className="py-3 px-4 text-center text-gray-500">
                      {row[3]}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
