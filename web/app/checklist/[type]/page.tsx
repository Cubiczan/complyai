import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { ChecklistResults } from "@/components/checklist-results";
import { FINTECH_TYPES } from "@/lib/regulations";
import { generateChecklist } from "@/lib/checklist";
import Link from "next/link";

export function generateStaticParams() {
  return Object.keys(FINTECH_TYPES).map((type) => ({ type }));
}

export default async function TypeChecklistPage({
  params,
}: {
  params: Promise<{ type: string }>;
}) {
  const { type } = await params;
  const info = FINTECH_TYPES[type];
  const checklist = generateChecklist(type);

  if (!info || !checklist) {
    return (
      <>
        <Navbar />
        <div className="max-w-3xl mx-auto px-4 py-24 text-center">
          <h1 className="text-3xl font-bold mb-4">Type not found</h1>
          <p className="text-gray-400 mb-8">
            Unknown fintech type: {type}
          </p>
          <Link
            href="/checklist"
            className="text-primary-400 hover:text-primary-300 transition"
          >
            ← Back to checklist
          </Link>
        </div>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <section className="py-16 md:py-24">
        <div className="max-w-5xl mx-auto px-4">
          <div className="mb-8">
            <Link
              href="/checklist"
              className="text-sm text-gray-400 hover:text-white transition"
            >
              ← All fintech types
            </Link>
          </div>
          <ChecklistResults
            items={checklist.items}
            displayName={checklist.displayName}
          />
        </div>
      </section>
      <Footer />
    </>
  );
}
