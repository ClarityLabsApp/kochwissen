import FehlersucheView, { fehlersucheMetadata } from "@/components/views/FehlersucheView";

export const metadata = fehlersucheMetadata("en");
export default function Page() { return <FehlersucheView lang="en" />; }
