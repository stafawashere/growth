import { useEffect, useRef, useState } from "react";

import { readExperiments, setExperimentState } from "../api/client";
import type { ExperimentState, ExperimentSwitch } from "../api/types";
import { formatPlanDate } from "../home/dates";

/* The two A/B switches of docs/plan/10 "A/B readiness" (11 P7 scope item 4) and the way to the
   operator's evidence of learning. They sit on settings because they are the operator's, never the
   student's next action. Like every settings section, a section whose request is in flight or
   failed renders its heading and no figure, and a change that failed comes back with the control
   unchanged. */

export const EXPERIMENT_STATES: ReadonlyArray<ExperimentState> = ["off", "on", "randomised"];

export const EVIDENCE_LABEL = "Evidence of learning";

export interface OperatorSettingsProps {
   onOpenEvidence: () => void;
}

function assignedText(experiment: ExperimentSwitch) {
   return experiment.arms
      .map((arm) => `${experiment.assigned_units[arm] ?? 0} to ${arm}`)
      .join(", ");
}

function SwitchRow(props: {
   experiment: ExperimentSwitch;
   working: boolean;
   onChange: (name: string, state: ExperimentState) => void;
}) {
   const { experiment, working, onChange } = props;
   const isRandomised = experiment.state === "randomised";
   const hasRandomisedFrom = isRandomised && experiment.randomised_from !== null;

   return (
      <li data-testid="experiment-switch" data-state={experiment.state} className="list-row list-row-start">
         <div className="list-row-body">
            <span className="list-row-title">{experiment.name}</span>

            <span className="list-row-meta">{experiment.description}</span>

            <span className="helper">
               {hasRandomisedFrom
                  ? `randomised since ${formatPlanDate((experiment.randomised_from as string).slice(0, 10))}`
                  : experiment.state}
               , {experiment.unit} units assigned {assignedText(experiment)}
            </span>
         </div>

         <div className="list-row-trail segmented" role="group" aria-label={`${experiment.name} state`}>
            {EXPERIMENT_STATES.map((state) => (
               <button
                  key={state}
                  type="button"
                  className="segment"
                  aria-pressed={experiment.state === state}
                  disabled={working || experiment.state === state}
                  onClick={() => onChange(experiment.name, state)}
               >
                  {state}
               </button>
            ))}
         </div>
      </li>
   );
}

export function ExperimentsSection() {
   const [experiments, setExperiments] = useState<ExperimentSwitch[] | null>(null);
   const [working, setWorking] = useState(false);

   const inFlight = useRef(false);

   useEffect(() => {
      let isCurrent = true;

      async function load() {
         try {
            const payload = await readExperiments();

            if (isCurrent) {
               setExperiments(payload.experiments);
            }
         } catch {
            // the section keeps its heading and no figure, as every settings section does
         }
      }

      load();

      return () => {
         isCurrent = false;
      };
   }, []);

   async function change(name: string, state: ExperimentState) {
      const isBusy = inFlight.current;

      if (isBusy) {
         return;
      }

      inFlight.current = true;
      setWorking(true);

      try {
         const payload = await setExperimentState(name, { state });

         setExperiments(payload.experiments);
      } catch {
         // a refused change leaves the switch as the server last reported it
      } finally {
         inFlight.current = false;
         setWorking(false);
      }
   }

   return (
      <section data-testid="experiments-section" className="section">
         <h2 className="section-header">Experiments</h2>

         {experiments === null ? null : (
            <ul className="list">
               {experiments.map((experiment) => (
                  <SwitchRow key={experiment.name} experiment={experiment} working={working} onChange={change} />
               ))}
            </ul>
         )}
      </section>
   );
}

export function OperatorSettings({ onOpenEvidence }: OperatorSettingsProps) {
   return (
      <div className="stack stack-wide" data-testid="operator-settings">
         <ExperimentsSection />

         <section className="section">
            <h2 className="section-header">{EVIDENCE_LABEL}</h2>

            <p className="muted">The learning metrics and the experiment results, each with what it is counted over.</p>

            <div className="cluster">
               <button type="button" className="button-secondary" onClick={onOpenEvidence}>
                  {EVIDENCE_LABEL}
               </button>
            </div>
         </section>
      </div>
   );
}
