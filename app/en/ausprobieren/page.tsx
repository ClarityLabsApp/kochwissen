import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("ausprobieren", "en");
export default function Page() { return <HubView group="ausprobieren" lang="en" />; }
