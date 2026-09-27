import type { ReactNode } from "react";

/* The title every screen opens with, ruled beneath by .screen-title. When an eyebrow names the
   screen, the eyebrow is the page's heading and the title sits one level below it. Both are
   returned bare, with no wrapper, because app.css spaces a card's first block from the title as
   its direct sibling. */
export function PageHeader(props: { title: ReactNode; eyebrow?: ReactNode }) {
   const hasEyebrow = props.eyebrow !== undefined;

   if (hasEyebrow) {
      return (
         <>
            <h1 className="eyebrow">{props.eyebrow}</h1>
            <h2 className="screen-title">{props.title}</h2>
         </>
      );
   }

   return <h1 className="screen-title">{props.title}</h1>;
}
