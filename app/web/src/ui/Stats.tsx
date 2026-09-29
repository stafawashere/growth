import type { ReactNode } from "react";

export interface StatProps {
   value: ReactNode;
   label: ReactNode;
   testId?: string;
}

export function Stat(props: StatProps) {
   return (
      <div className="stat" data-testid={props.testId}>
         <span className="stat-value">{props.value}</span>
         <span className="stat-label">{props.label}</span>
      </div>
   );
}

export function StatGroup(props: { children: ReactNode; label?: string }) {
   return (
      <div className="stat-group" role={props.label === undefined ? undefined : "group"} aria-label={props.label}>
         {props.children}
      </div>
   );
}
