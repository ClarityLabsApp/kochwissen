import HubView, { groupMetadata } from "@/components/views/HubView";

export const metadata = groupMetadata("verstehen", "de");
export default function Page() { return <HubView group="verstehen" lang="de" />; }
