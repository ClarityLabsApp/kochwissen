import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("probleme", "de");
export default function Page() { return <HubView group="probleme" lang="de" />; }
