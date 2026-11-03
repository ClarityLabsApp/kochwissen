"use client";
import { useEffect, useState } from "react";

/** Merkliste und „gelesen“: nur im Browser (localStorage), ohne Konto. Fehlt der Speicher, geht es ohne. */
const K = { merk: "garum:merkliste", read: "garum:gelesen" } as const;
const EVT = "garum-memo";

function load(k: keyof typeof K): string[] {
  try { const v = JSON.parse(localStorage.getItem(K[k]) || "[]"); return Array.isArray(v) ? v.filter((x) => typeof x === "string") : []; } catch { return []; }
}
function save(k: keyof typeof K, ids: string[]) {
  try { localStorage.setItem(K[k], JSON.stringify(ids)); } catch { /* ohne Speicher */ }
  window.dispatchEvent(new Event(EVT));
}
export const toggleMerk = (id: string) => { const l = load("merk"); save("merk", l.includes(id) ? l.filter((x) => x !== id) : [id, ...l]); };
export const addMerk = (ids: string[]) => { const l = load("merk"); save("merk", [...ids.filter((x) => !l.includes(x)), ...l]); };
export const markRead = (id: string) => { const l = load("read"); if (!l.includes(id)) save("read", [...l, id].slice(-2000)); };

/** Aktuelle Liste, bleibt zwischen Tabs und Komponenten synchron. Vor dem ersten Laden leer. */
export function useMemo2(k: keyof typeof K) {
  const [ids, setIds] = useState<string[]>([]);
  useEffect(() => {
    const up = () => setIds(load(k));
    up();
    window.addEventListener(EVT, up); window.addEventListener("storage", up);
    return () => { window.removeEventListener(EVT, up); window.removeEventListener("storage", up); };
  }, [k]);
  return ids;
}
