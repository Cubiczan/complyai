import "./globals.css";
import type { Metadata } from "next";
import { Analytics } from "./analytics";

export const metadata: Metadata = {
  title: "complyAI — RegTech for Indie Fintechs",
  description:
    "complyAI generates compliance checklists, legal documents, and regulatory monitoring for indie fintechs — at a price that won't make your co-founder cry.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-surface text-gray-100 antialiased min-h-screen">
        <Analytics />
        {children}
      </body>
    </html>
  );
}
