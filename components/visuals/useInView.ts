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

/** Lesezeit für einen angezeigten Text: Grundzeit plus etwa 50 ms pro Zeichen. */
export const readMs = (txt: string) => 1200 + 50 * txt.length;

/**
 * Fährt einen Wert von Halt zu Halt (sanft beschleunigt) und wartet an jedem Halt die angegebene Zeit.
 * Gibt eine Funktion zum Abbrechen zurück.
 */
export function tour(from: number, stops: { v: number; hold: number }[], set: (v: number) => void, moveMs = 1600) {
  let raf = 0, i = 0, cur = from, phase: "move" | "hold" = "move", t0 = performance.now();
  const step = (now: number) => {
    if (i >= stops.length) return;
    const s = stops[i];
    if (phase === "move") {
      const p = Math.min(1, (now - t0) / moveMs), e = 0.5 - 0.5 * Math.cos(p * Math.PI);
      set(cur + (s.v - cur) * e);
      if (p >= 1) { phase = "hold"; t0 = now; cur = s.v; }
    } else if (now - t0 >= s.hold) { i++; phase = "move"; t0 = now; }
    raf = requestAnimationFrame(step);
  };
  raf = requestAnimationFrame(step);
  return () => cancelAnimationFrame(raf);
}
