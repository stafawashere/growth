import type { ReactNode } from "react";

export function List(props: { children: ReactNode; flush?: boolean; as?: "div" | "ul"; label?: string; testId?: string }) {
   const Tag = props.as ?? "div";
   const className = props.flush === true ? "list list-flush" : "list";

   return (
      <Tag className={className} aria-label={props.label} data-testid={props.testId}>
         {props.children}
      </Tag>
   );
}
