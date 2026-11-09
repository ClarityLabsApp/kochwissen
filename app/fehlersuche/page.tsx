import FehlersucheView, { fehlersucheMetadata } from "@/components/views/FehlersucheView";

export const metadata = fehlersucheMetadata("de");
export default function Page() { return <FehlersucheView lang="de" />; }
