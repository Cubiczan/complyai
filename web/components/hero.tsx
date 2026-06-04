export function Hero() {
  return (
    <section className="hero-gradient py-24 md:py-32">
      <div className="max-w-5xl mx-auto px-4 text-center">
        <div className="inline-flex items-center gap-2 bg-primary-900/30 border border-primary-700/30 rounded-full px-4 py-1.5 text-sm text-primary-300 mb-8">
          <span className="w-2 h-2 bg-primary-400 rounded-full animate-pulse"></span>
          No sales calls. No $500 minimums. Self-service RegTech.
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">
          Compliance that
          <br />
          <span className="gradient-text">doesn't cost your runway</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          complyAI generates compliance checklists, legal documents, and
          regulatory monitoring for indie fintechs — at a price that won't make
          your co-founder cry.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="/checklist"
            className="bg-primary-600 hover:bg-primary-500 text-white font-semibold px-8 py-3.5 rounded-xl text-lg transition glow"
          >
            Start Free →
          </a>
          <a
            href="#how"
            className="text-gray-400 hover:text-white border border-gray-700 hover:border-gray-500 font-medium px-8 py-3.5 rounded-xl text-lg transition"
          >
            How It Works
          </a>
        </div>
        <p className="text-sm text-gray-500 mt-6">
          Free compliance audit — no credit card required
        </p>
      </div>
    </section>
  );
}
