import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-gray-800/50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <span className="text-xl">⚡</span>
            <span className="font-bold">
              comply<span className="gradient-text">AI</span>
            </span>
          </div>
          <div className="flex gap-8 text-sm text-gray-500">
            <Link href="/docs" className="hover:text-gray-300">
              Docs
            </Link>
            <Link href="/pricing" className="hover:text-gray-300">
              Pricing
            </Link>
            <span className="hover:text-gray-300 cursor-pointer">Privacy</span>
            <span className="hover:text-gray-300 cursor-pointer">Terms</span>
          </div>
          <div className="text-sm text-gray-600">
            © 2026 complyAI. Built for indie fintechs.
          </div>
        </div>
        <div className="mt-8 text-center text-xs text-gray-700">
          complyAI is not a law firm. Output is for informational purposes and
          does not constitute legal advice.
        </div>
      </div>
    </footer>
  );
}
