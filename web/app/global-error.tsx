"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body className="bg-surface text-gray-100 antialiased min-h-screen flex items-center justify-center">
        <div className="text-center px-4">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-3xl font-bold mb-4">Something went wrong</h1>
          <p className="text-gray-400 mb-8 max-w-md">
            An unexpected error occurred. Please try again.
          </p>
          <button
            onClick={reset}
            className="bg-primary-600 hover:bg-primary-500 text-white font-medium px-6 py-2.5 rounded-lg transition text-sm"
          >
            Try Again →
          </button>
        </div>
      </body>
    </html>
  );
}
