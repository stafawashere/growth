import type { ReactNode } from "react";

/* A link to a section of the lesson by its anchor (#err-BC-ERR-02020, #chk-1, #prq-BC-PRQ-00001,
   or the full section id). The reader decides where it goes: to that section's screen when the plan
   serves it, or open below the link when it does not. It is a button because it changes the
   screen rather than the address. */

export function anchorFragment(anchor: string) {
   const hashAt = anchor.indexOf("#");

   return hashAt === -1 ? anchor : anchor.slice(hashAt + 1);
}

export function sectionIdMatches(sectionId: string, anchor: string) {
   return anchorFragment(sectionId) === anchorFragment(anchor);
}

export interface LessonLinkProps {
   anchor: string;
   onOpen: (anchor: string) => void;
   children: ReactNode;
}

export function LessonLink({ anchor, onOpen, children }: LessonLinkProps) {
   return (
      <button type="button" className="text-button" data-testid="lesson-link" data-anchor={anchor} onClick={() => onOpen(anchor)}>
         {children}
      </button>
   );
}
