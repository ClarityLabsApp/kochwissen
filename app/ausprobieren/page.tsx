import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("ausprobieren", "de");
export default function Page() { return <HubView group="ausprobieren" lang="de" />; }
