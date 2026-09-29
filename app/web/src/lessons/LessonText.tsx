import { MathText } from "../math/MathText";

/* A lesson's text keeps its sources beside the claim, because the design and the record are
   checked sentence by sentence against the library. The student reads the claim alone: a
   parenthetical that holds only record ids or page citations, and an evidence tag, are dropped
   here. A citation that is part of a sentence copied verbatim from a library record stays, since
   removing it would change the record's words. */
const CITATION = String.raw`(?:BC-[A-Z]+-[\w-]+|(?:ced|sg-\d{2}|cr-\d{2}|crabbc-\d{2}):\d+(?:-\d+)?)`;
const CITATION_GROUP = new RegExp(String.raw`\s*\((?:\s*(?:see\s+)?${CITATION}\s*(?:,|;|and)?\s*)+\)`, "g");
const EVIDENCE_TAG = /\s*\[(?:verified|single-source|inferred|uncertain)\]/g;

export function servedText(text: string): string {
   return text.replace(CITATION_GROUP, "").replace(EVIDENCE_TAG, "");
}

export function LessonText({ text }: { text: string }) {
   return <MathText text={servedText(text)} />;
}
