import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { LogIn } from "lucide-react";

export default function LoginPage() {
  return (
    <>
      <Navbar />
      <section className="py-24">
        <div className="max-w-md mx-auto px-4">
          <div className="text-center mb-10">
            <div className="w-16 h-16 mx-auto bg-primary-900/30 rounded-2xl flex items-center justify-center mb-6 glow">
              <LogIn className="w-8 h-8 text-primary-400" />
            </div>
            <h1 className="text-3xl font-bold mb-2">Welcome back</h1>
            <p className="text-gray-400 text-sm">
              Sign in to access your compliance dashboard
            </p>
          </div>
          <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8">
            <div className="space-y-5">
              <div>
                <label className="block text-xs text-gray-500 mb-1 uppercase tracking-wider">
                  Email
                </label>
                <input
                  type="email"
                  placeholder="you@company.com"
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-primary-500 transition"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1 uppercase tracking-wider">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Enter your password"
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-primary-500 transition"
                />
              </div>
              <button className="w-full bg-primary-600 hover:bg-primary-500 text-white font-medium py-2.5 rounded-xl transition text-sm">
                Sign In →
              </button>
            </div>
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500">
                Don't have an account?{" "}
                <a href="#" className="text-primary-400 hover:text-primary-300">
                  Get started free
                </a>
              </p>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </>
  );
}
