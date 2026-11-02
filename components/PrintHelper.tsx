"use client";
import { useEffect } from "react";
/** Öffnet vor dem Drucken alle aufklappbaren Bereiche, damit nichts fehlt. */
export default function PrintHelper() {
  useEffect(() => {
    const open = () => document.querySelectorAll("details").forEach((d) => d.setAttribute("open", ""));
    window.addEventListener("beforeprint", open);
    return () => window.removeEventListener("beforeprint", open);
  }, []);
  return null;
}
