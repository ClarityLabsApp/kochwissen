import HomeView from "@/components/views/HomeView";
export const metadata = { alternates: { languages: { de: "/", en: "/en" } } };
export default function Home() { return <HomeView lang="de" />; }
