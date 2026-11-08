import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("ziele", "en");
export default function Page() { return <HubView group="ziele" lang="en" />; }
