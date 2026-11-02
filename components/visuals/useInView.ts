"use client";
import { useEffect, useState, type RefObject } from "react";

/** Wird true, sobald das Element zu einem guten Teil im Bild ist (einmalig). So starten Animationen erst, wenn man sie sieht. */
export function useInView(ref: RefObject<Element | null>, threshold = 0.45) {
  const [seen, setSeen] = useState(false);
  useEffect(() => {
    if (seen || !ref.current) return;
    if (typeof IntersectionObserver === "undefined") { setSeen(true); return; }
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setSeen(true); io.disconnect(); } }, { threshold });
    io.observe(ref.current);
    return () => io.disconnect();
  }, [ref, seen, threshold]);
  return seen;
}
