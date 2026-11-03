import { CONTACT_EMAIL, INSTAGRAM_URL, OWNER } from "@/lib/site";
import type { Lang } from "@/lib/i18n";

const STAND = { de: "Stand: November 2026", en: "Last updated: November 2026" };

/** Impressum und Datenschutzerklärung, Deutsch und Englisch. */
export function ImpressumView({ lang }: { lang: Lang }) {
  const de = lang === "de";
  const mail = <a href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a>;
  return (
    <main className="wrap legal" lang={lang}>
      <h1>{de ? "Impressum" : "Legal notice"}</h1>
      <section>
        <h2>{de ? "Verantwortlich" : "Responsible"}</h2>
        <p>{OWNER.name}<br />{de ? OWNER.place : OWNER.placeEn}<br />{mail}<br /><a href={INSTAGRAM_URL} target="_blank" rel="noopener noreferrer">Instagram: @garum.guide</a></p>
        <p>{de ? "Garum ist ein privates, nicht kommerzielles Projekt. Es gibt keine Werbung und nichts zu kaufen."
          : "Garum is a private, non-commercial project. There is no advertising and nothing for sale."}</p>
      </section>
      <section>
        <h2>{de ? "Hinweis zu den Inhalten" : "About the content"}</h2>
        <p>{de ? "Die Inhalte sind nach bestem Wissen erklärt und mit Quellen belegt, aber ohne Gewähr. Zahlen mit dem Hinweis «Richtwert» sind Anhaltspunkte, keine genauen Vorgaben. Einträge mit dem Status «Entwurf» sind noch nicht abschließend geprüft."
          : "The content is explained to the best of our knowledge and backed by sources, but without guarantee. Figures marked “as a guide” are pointers, not exact specifications. Entries marked “draft” have not yet been fully reviewed."}</p>
        <p>{de ? "Experimente mit Kindern bitte nur unter Aufsicht durchführen. Bei Allergien, Unverträglichkeiten und Fragen der Lebensmittelsicherheit gelten die Angaben auf den Produkten und die Empfehlungen der Fachstellen. Garum ersetzt keine Ernährungs- oder medizinische Beratung."
          : "Please do experiments with children only under supervision. For allergies, intolerances and food safety, the information on the products and the advice of the authorities apply. Garum does not replace nutritional or medical advice."}</p>
      </section>
      <section>
        <h2>{de ? "Links, Bilder und Schriften" : "Links, images and fonts"}</h2>
        <p>{de ? "Für die Inhalte verlinkter fremder Seiten sind deren Betreiber verantwortlich. Die Illustrationen wurden mit Hilfe künstlicher Intelligenz erstellt. Die Schriften Fraunces, Newsreader und JetBrains Mono stehen unter der SIL Open Font License und werden von dieser Seite selbst ausgeliefert."
          : "The operators of linked external pages are responsible for their content. The illustrations were created with the help of artificial intelligence. The fonts Fraunces, Newsreader and JetBrains Mono are licensed under the SIL Open Font License and are served by this site itself."}</p>
      </section>
      <p className="mono">{STAND[lang]}</p>
    </main>
  );
}

export function DatenschutzView({ lang }: { lang: Lang }) {
  const de = lang === "de";
  const mail = <a href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a>;
  return (
    <main className="wrap legal" lang={lang}>
      <h1>{de ? "Datenschutz" : "Privacy"}</h1>
      <p className="lede">{de ? "Kurz gesagt: Garum setzt keine Cookies, kein Tracking und keine Analysewerkzeuge ein. Es gibt keine Konten und keine Formulare."
        : "In short: Garum uses no cookies, no tracking and no analytics tools. There are no accounts and no forms."}</p>
      <section>
        <h2>{de ? "Verantwortlich" : "Controller"}</h2>
        <p>{OWNER.name}, {de ? OWNER.place : OWNER.placeEn}, {mail}</p>
      </section>
      <section>
        <h2>{de ? "Hosting und Server-Protokolle" : "Hosting and server logs"}</h2>
        <p>{de ? "Die Seite wird bei Vercel Inc. (USA) betrieben. Beim Aufruf verarbeitet Vercel technisch notwendige Angaben wie IP-Adresse, Zeitpunkt, aufgerufene Seite und Browsertyp, um die Seite auszuliefern und vor Missbrauch zu schützen. Diese Daten können in den USA verarbeitet werden und werden nicht mit anderen Daten zusammengeführt. Einzelheiten: "
          : "The site is hosted by Vercel Inc. (USA). When a page is requested, Vercel processes technically necessary details such as IP address, time, page requested and browser type in order to deliver the site and protect it from abuse. This data may be processed in the USA and is not combined with other data. Details: "}
          <a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener noreferrer">{de ? "Datenschutzerklärung von Vercel" : "Vercel privacy policy"}</a>.</p>
      </section>
      <section>
        <h2>{de ? "Speicherung im eigenen Browser" : "Storage in your own browser"}</h2>
        <p>{de ? "Deine Merkliste, welche Einträge du schon gelesen hast, der Fortschritt in den Lernpfaden und die Antworten im Quiz werden nur im Speicher deines Browsers abgelegt (localStorage). Sie verlassen dein Gerät nicht, außer du teilst deine Merkliste selbst als Link, und du kannst sie jederzeit über die Browsereinstellungen löschen."
          : "Your saved entries, which entries you have already read, your progress in the learning paths and your quiz answers are kept only in your browser's storage (localStorage). They never leave your device unless you share your list yourself, and you can delete them at any time in your browser settings."}</p>
      </section>
      <section>
        <h2>{de ? "Schriften" : "Fonts"}</h2>
        <p>{de ? "Alle Schriften werden von garum.guide selbst geladen. Es besteht keine Verbindung zu Google oder anderen Schriftanbietern."
          : "All fonts are loaded from garum.guide itself. There is no connection to Google or any other font provider."}</p>
      </section>
      <section>
        <h2>{de ? "Kontakt per E-Mail" : "Contact by email"}</h2>
        <p>{de ? "Wenn du eine E-Mail schreibst, werden deine Angaben nur verwendet, um deine Nachricht zu beantworten, und nicht weitergegeben."
          : "If you send an email, your details are used only to answer your message and are not passed on."}</p>
      </section>
      <section>
        <h2>{de ? "Deine Rechte" : "Your rights"}</h2>
        <p>{de ? "Du kannst jederzeit Auskunft über deine Daten verlangen, sie berichtigen oder löschen lassen (nach dem Schweizer Datenschutzgesetz und, soweit anwendbar, der DSGVO). Schreib dazu an "
          : "You can ask at any time for information about your data, or have it corrected or deleted (under the Swiss Data Protection Act and, where applicable, the GDPR). To do so, write to "}{mail}.</p>
      </section>
      <p className="mono">{STAND[lang]}</p>
    </main>
  );
}
