import { hasPicture, libraryData } from "@/lib/content";
import { t, type Lang } from "@/lib/i18n";
import { Crumbs } from "@/components/views/HubView";
import MerkList, { type MerkItem } from "@/components/MerkList";

/** Seite „Merkliste“: nur die gemerkten Einträge. Die Liste selbst liegt im Browser, deshalb filtert MerkList dort. */
export default function MerkView({ lang }: { lang: Lang }) {
  const T = t(lang);
  const all = libraryData(lang);
  const titel = new Map(all.map((e) => [e.id, e.titel]));
  const plain = (s: string) => s.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => titel.get(id) ?? id);
  const items: MerkItem[] = all.filter((e) => e.status !== "geplant").map((e) => ({
    id: e.id, typ: e.typ, titel: e.titel, kurz: e.kurz ? plain(e.kurz) : "",
    pic: hasPicture(e.id) ? e.id : (e.welten ?? []).find((w) => hasPicture(w)) ?? null,
  }));
  return (
    <main className="wrap" id="inhalt" lang={lang}>
      <Crumbs lang={lang} trail={[[T.memo.list]]} />
      <MerkList items={items} lang={lang} />
    </main>
  );
}
