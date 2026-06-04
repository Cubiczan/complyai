import Link from "next/link";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";

export default function NotFound() {
  return (
    <>
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center">
        <div className="text-6xl mb-4">404</div>
        <h1 className="text-3xl font-bold mb-4">Page not found</h1>
        <p className="text-gray-400 mb-8 max-w-md">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link
          href="/"
          className="bg-primary-600 hover:bg-primary-500 text-white font-medium px-6 py-2.5 rounded-lg transition text-sm"
        >
          Go Home →
        </Link>
      </div>
      <Footer />
    </>
  );
}
