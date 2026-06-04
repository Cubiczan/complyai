"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";

export function Analytics() {
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    // Placeholder for analytics integration
    if (typeof window !== "undefined") {
      // console.log(`Page view: ${pathname}`);
    }
  }, [pathname]);

  return null;
}
