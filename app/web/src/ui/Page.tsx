import type { ReactNode } from "react";

import { Icon } from "./Icon";

export interface BackLink {
   label: string;
   onBack: () => void;
}

export interface PageHeaderProps {
   title: ReactNode;
   eyebrow?: ReactNode;
   intro?: ReactNode;
   aside?: ReactNode;
   back?: BackLink;
   titleId?: string;
}

export function PageHeader(props: PageHeaderProps) {
   const hasKicker = props.back !== undefined || props.eyebrow !== undefined;

   return (
      <header className="page-header">
         {hasKicker ? (
            <div className="page-kicker">
               {props.back !== undefined ? (
                  <button type="button" className="back-link" onClick={props.back.onBack}>
                     <Icon name="back" />
                     {props.back.label}
                  </button>
               ) : (
                  <span className="eyebrow">{props.eyebrow}</span>
               )}
            </div>
         ) : null}

         <div className="page-title-row">
            <div className="page-title-text">
               <h1 id={props.titleId}>{props.title}</h1>

               {props.intro !== undefined ? <p className="page-intro">{props.intro}</p> : null}
            </div>

            {props.aside !== undefined ? <div className="page-aside">{props.aside}</div> : null}
         </div>
      </header>
   );
}

export function Page(props: { header: ReactNode; children: ReactNode; testId?: string; labelledBy?: string }) {
   return (
      <div className="page" data-testid={props.testId} aria-labelledby={props.labelledBy}>
         {props.header}

         <div className="page-body">{props.children}</div>
      </div>
   );
}

export interface SectionProps {
   title?: ReactNode;
   aside?: ReactNode;
   plain?: boolean;
   level?: 2 | 3;
   children: ReactNode;
   testId?: string;
   className?: string;
   labelId?: string;
}

export function Section(props: SectionProps) {
   const hasTitle = props.title !== undefined;
   const headerClass = props.plain === true ? "section-header section-header-plain" : "section-header";
   const Heading = props.level === 3 ? "h3" : "h2";
   const sectionClass = props.className === undefined ? "section" : `section ${props.className}`;

   return (
      <section className={sectionClass} data-testid={props.testId} aria-labelledby={props.labelId}>
         {hasTitle ? (
            <div className={headerClass}>
               <Heading id={props.labelId}>{props.title}</Heading>

               {props.aside !== undefined ? <div className="cluster">{props.aside}</div> : null}
            </div>
         ) : null}

         {props.children}
      </section>
   );
}
