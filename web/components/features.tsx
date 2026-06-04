import { ClipboardCheck, FileText, Bell, Shield, Globe, Bot } from "lucide-react";

const features = [
  {
    icon: ClipboardCheck,
    label: "📋",
    title: "Compliance Checklists",
    description:
      "Tell us what kind of fintech you are — payments, lending, crypto, banking — and get a prioritized compliance checklist in seconds.",
  },
  {
    icon: FileText,
    label: "📝",
    title: "Document Templates",
    description:
      "Generate ToS, Privacy Policies, EULAs, and Reg E/Reg Z disclosures. Fill in your details, and you're ready to go.",
  },
  {
    icon: Bell,
    label: "🔔",
    title: "Reg Change Monitoring",
    description:
      "We watch SEC, CFPB, FinCEN, and state regulators for changes. Get notified only about what affects your fintech type.",
  },
  {
    icon: Shield,
    label: "🔒",
    title: "BSA/AML Coverage",
    description:
      "Full AML program templates, CIP procedures, SAR filing workflows, and OFAC screening guidance built in.",
  },
  {
    icon: Globe,
    label: "🗺️",
    title: "Multi-Jurisdiction",
    description:
      "Federal + state-level coverage. NY DFS, CA DFPI, Texas — we track the regulators that matter for US fintechs.",
  },
  {
    icon: Bot,
    label: "🤖",
    title: "AI-Powered (Practical)",
    description:
      "We use AI where it helps — parsing regulations, generating checklists, diff'ing changes. Not just AI-washed features.",
  },
];

export function Features() {
  return (
    <section id="features" className="py-24">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Everything you need to stay compliant
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Enterprise-grade compliance tools, indie-fintech pricing. No bloat,
            no sales demos.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((f) => (
            <div
              key={f.title}
              className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 hover:border-primary-700/50 transition"
            >
              <div className="w-12 h-12 bg-primary-900/30 rounded-xl flex items-center justify-center mb-5">
                <span className="text-2xl">{f.label}</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">{f.title}</h3>
              <p className="text-gray-400 leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
