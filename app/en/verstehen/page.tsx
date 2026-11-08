import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("verstehen", "en");
export default function Page() { return <HubView group="verstehen" lang="en" />; }
