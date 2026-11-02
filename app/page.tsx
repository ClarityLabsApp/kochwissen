import HomeView from "@/components/views/HomeView";
export const metadata = { title: { absolute: "Garum · Verstehen, warum Kochen funktioniert" }, alternates: { canonical: "/", languages: { de: "/", en: "/en" } } };
export default function Home() { return <HomeView lang="de" />; }
