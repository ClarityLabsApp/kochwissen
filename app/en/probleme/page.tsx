import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("probleme", "en");
export default function Page() { return <HubView group="probleme" lang="en" />; }
