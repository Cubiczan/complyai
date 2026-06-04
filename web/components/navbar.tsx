"use client";

import Link from "next/link";
import { Menu, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="border-b border-gray-800/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl">⚡</span>
            <span className="font-bold text-xl tracking-tight">
              comply<span className="gradient-text">AI</span>
            </span>
          </Link>
          <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
            <Link href="/checklist" className="hover:text-white transition">
              Checklist
            </Link>
            <Link href="/templates" className="hover:text-white transition">
              Templates
            </Link>
            <Link href="/monitor" className="hover:text-white transition">
              Monitor
            </Link>
            <Link href="/pricing" className="hover:text-white transition">
              Pricing
            </Link>
          </div>
          <div className="hidden md:flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm text-gray-400 hover:text-white transition"
            >
              Sign In
            </Link>
            <Link
              href="/checklist"
              className="bg-primary-600 hover:bg-primary-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
            >
              Get Started
            </Link>
          </div>
          <button
            className="md:hidden text-gray-400"
            onClick={() => setOpen(!open)}
          >
            {open ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
        {open && (
          <div className="md:hidden pb-4 space-y-2">
            <Link
              href="/checklist"
              className="block px-3 py-2 text-sm text-gray-400 hover:text-white"
              onClick={() => setOpen(false)}
            >
              Checklist
            </Link>
            <Link
              href="/templates"
              className="block px-3 py-2 text-sm text-gray-400 hover:text-white"
              onClick={() => setOpen(false)}
            >
              Templates
            </Link>
            <Link
              href="/monitor"
              className="block px-3 py-2 text-sm text-gray-400 hover:text-white"
              onClick={() => setOpen(false)}
            >
              Monitor
            </Link>
            <Link
              href="/pricing"
              className="block px-3 py-2 text-sm text-gray-400 hover:text-white"
              onClick={() => setOpen(false)}
            >
              Pricing
            </Link>
            <Link
              href="/login"
              className="block px-3 py-2 text-sm text-gray-400 hover:text-white"
              onClick={() => setOpen(false)}
            >
              Sign In
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
