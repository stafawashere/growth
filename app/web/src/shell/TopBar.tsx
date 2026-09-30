import type { MouseEvent, ReactNode } from "react";

import { ASK_LABEL, TIMED_PART, askAccessibleName } from "../agent/agentCopy";
import { PANEL_ID, useAgent } from "../agent/AgentProvider";
import { hashFor, type Place, type View } from "../routing";
import { Icon, type IconName } from "../ui/Icon";

export type TabId = "home" | "lessons" | "review" | "progress" | "assessments" | "calculator";

export interface TabEntry {
   id: TabId;
   label: string;
   icon: IconName;
   place: Place;
   views: ReadonlyArray<View>;
}

/* The redesign's five tabs and the Calculator destination after them (docs/calculator/design.md,
   Where it lives). Settings and the account sit behind the avatar menu, and a session, onboarding,
   a lesson, a checkpoint and a probe light the tab they were opened under. */
export const TABS: ReadonlyArray<TabEntry> = [
   { id: "home", label: "Today", icon: "calendar", place: { view: "home" }, views: ["home", "session", "onboarding"] },
   { id: "lessons", label: "Lessons", icon: "book", place: { view: "lessons" }, views: ["lessons", "lesson"] },
   { id: "review", label: "Review", icon: "refresh", place: { view: "review" }, views: ["review"] },
   { id: "progress", label: "Progress", icon: "chart", place: { view: "progress", tab: "mastery" }, views: ["progress", "checkpoint", "probe"] },
   { id: "assessments", label: "Assessments", icon: "clipboard", place: { view: "assessments", format: "unit" }, views: ["assessments"] },
   { id: "calculator", label: "Calculator", icon: "graph", place: { view: "calculator", section: "cards" }, views: ["calculator"] }
];

export function tabFor(view: View): TabId | null {
   return TABS.find((entry) => entry.views.includes(view))?.id ?? null;
}

function followWithoutReload(event: MouseEvent<HTMLAnchorElement>, go: () => void) {
   const opensElsewhere = event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0;

   if (opensElsewhere) {
      return;
   }

   event.preventDefault();
   go();
}

const ASK_REASON_ID = "ask-reason";

/* The tutor's one entry point (docs/agent/design.md, "The entry point"): a disclosure button left
   of the avatar menu at every width, named with its shortcut, and on a timed part disabled with the
   reason written under it. Outside the signed-in shell there is no tutor and no button. */
function AskButton() {
   const agent = useAgent();

   if (agent === null) {
      return null;
   }

   const isDisabled = agent.isTimed;

   return (
      <div className="ask-control">
         <button
            ref={agent.askButton}
            type="button"
            className="ask-button"
            aria-expanded={agent.isOpen}
            aria-controls={PANEL_ID}
            aria-label={askAccessibleName(agent.isMac)}
            aria-describedby={isDisabled ? ASK_REASON_ID : undefined}
            disabled={isDisabled}
            onClick={agent.togglePanel}
         >
            <Icon name="question" />
            <span>{ASK_LABEL}</span>
         </button>

         {isDisabled ? (
            <span className="ask-reason" id={ASK_REASON_ID} data-testid="ask-reason">
               {TIMED_PART}
            </span>
         ) : null}
      </div>
   );
}

export function TopBar(props: { view: View | null; go: (place: Place) => void; menu?: ReactNode }) {
   const activeTab = props.view === null ? null : tabFor(props.view);
   const showsTabs = props.view !== null;

   return (
      <header className="app-header">
         <div className="app-bar">
            <a className="app-brand" href={hashFor({ view: "home" })} onClick={(event) => followWithoutReload(event, () => props.go({ view: "home" }))}>
               Growth
            </a>

            {showsTabs ? (
               <nav className="app-nav" aria-label="Main">
                  {TABS.map((entry) => (
                     <a
                        key={entry.id}
                        className="nav-tab"
                        href={hashFor(entry.place)}
                        aria-current={entry.id === activeTab ? "page" : undefined}
                        onClick={(event) => followWithoutReload(event, () => props.go(entry.place))}
                     >
                        <Icon name={entry.icon} size="md" className="nav-tab-icon" />
                        <span>{entry.label}</span>
                     </a>
                  ))}
               </nav>
            ) : null}

            <div className="app-bar-end">
               <AskButton />

               {props.menu}
            </div>
         </div>
      </header>
   );
}
