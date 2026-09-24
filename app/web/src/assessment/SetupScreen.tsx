import { useId, useState } from "react";

import { readAssessmentShape, readCheckUnits, readUnfinished, type CaptureMode } from "../api/client";
import type { AssessmentShape, CheckUnitsPayload, PartKey, UnfinishedAssessment, UnfinishedPayload } from "../api/types";
import { formatPlanDate } from "../home/dates";
import { useLoad } from "../progress/load";

/* 08 "Information architecture", mock: setup chooses the form, the parts and paper or typed
   capture. Every count and every minute is read from /assessments/shape, which reads
   research/exam/exam-structure.md, and nothing here schedules a mock or says when to take one. */

export interface SetupScreenProps {
   problem: string | null;
   onStartMock: (captureMode: CaptureMode) => void;
   onStartDrill: (part: PartKey, captureMode: CaptureMode) => void;
   onStartUnitCheck: (unitId: string, title: string) => void;
   onResume: (entry: UnfinishedAssessment, subject: string) => void;
}

const CAPTURE_CHOICES: { value: CaptureMode; label: string }[] = [
   { value: "photo", label: "Write on paper and photograph each page" },
   { value: "typed", label: "Type each answer" }
];

function ShapeSection(props: {
   shape: AssessmentShape;
   captureMode: CaptureMode;
   onStartMock: SetupScreenProps["onStartMock"];
   onStartDrill: SetupScreenProps["onStartDrill"];
}) {
   const { shape, captureMode } = props;

   if (!shape.timed_available) {
      return <p className="muted">Timed practice is switched off on this installation, so the mock and the part drills are not offered.</p>;
   }

   return (
      <>
         <section data-testid="mock-setup">
            <h2 className="section-heading">Full mock exam</h2>

            <ol data-testid="mock-parts">
               {shape.parts.map((part) => (
                  <li key={part.key}>
                     {part.label}, {part.question_type.toLowerCase()}: {part.question_count} questions in {part.minutes} minutes,{" "}
                     {part.calculator_label}
                  </li>
               ))}
            </ol>

            <p className="muted">The parts run in this order with a break between them. A submitted part cannot be reopened.</p>

            <button type="button" className="button-primary" onClick={() => props.onStartMock(captureMode)}>
               Start the full mock
            </button>
         </section>

         <section data-testid="drill-setup">
            <h2 className="section-heading">One part, timed</h2>

            <ul className="review-list">
               {shape.parts.map((part) => (
                  <li key={part.key}>
                     <button
                        type="button"
                        className="text-button"
                        onClick={() => props.onStartDrill(part.key as PartKey, captureMode)}
                     >
                        Drill {part.label}
                     </button>
                  </li>
               ))}
            </ul>
         </section>
      </>
   );
}

function subjectOf(entry: UnfinishedAssessment, unitTitles: Record<string, string>) {
   const subMode = entry.sub_mode ?? "";

   return entry.mode === "unit_check" ? (unitTitles[subMode] ?? subMode) : subMode;
}

function unfinishedTitle(entry: UnfinishedAssessment, subject: string) {
   if (entry.mode === "mock") {
      return "Full mock exam";
   }

   if (entry.mode === "part_drill") {
      return `Part drill, ${subject}`;
   }

   return `Unit check, ${subject}`;
}

function ResumeSection(props: {
   unfinished: UnfinishedPayload;
   unitTitles: Record<string, string>;
   onResume: SetupScreenProps["onResume"];
}) {
   const entries = props.unfinished.unfinished;

   if (entries.length === 0) {
      return null;
   }

   return (
      <section data-testid="resume-list">
         <h2 className="section-heading">Resume</h2>

         <ul className="review-list">
            {entries.map((entry) => {
               const subject = subjectOf(entry, props.unitTitles);
               const title = unfinishedTitle(entry, subject);
               const startedOn = formatPlanDate(entry.started_at.slice(0, 10));

               return (
                  <li key={entry.id}>
                     <button type="button" className="text-button" onClick={() => props.onResume(entry, subject)}>
                        Resume {title}
                     </button>

                     <span className="muted">
                        Started {startedOn}, {entry.parts_closed} of {entry.parts_total} parts closed
                     </span>
                  </li>
               );
            })}
         </ul>
      </section>
   );
}

function UnitSection(props: { units: CheckUnitsPayload; onStartUnitCheck: SetupScreenProps["onStartUnitCheck"] }) {
   const available = props.units.units.filter((unit) => unit.available);

   return (
      <section data-testid="unit-check-setup">
         <h2 className="section-heading">Unit check</h2>

         <p className="muted">Untimed. Answers are marked only once the whole check is submitted.</p>

         {available.length === 0 ? <p className="muted">No unit can be checked yet.</p> : null}

         <ul className="review-list">
            {available.map((unit) => (
               <li key={unit.unit_id}>
                  <button type="button" className="text-button" onClick={() => props.onStartUnitCheck(unit.unit_id, unit.title)}>
                     {unit.title}
                  </button>
               </li>
            ))}
         </ul>
      </section>
   );
}

export function SetupScreen({ problem, onStartMock, onStartDrill, onStartUnitCheck, onResume }: SetupScreenProps) {
   const shape = useLoad<AssessmentShape>(readAssessmentShape);
   const units = useLoad<CheckUnitsPayload>(readCheckUnits);
   const unfinished = useLoad<UnfinishedPayload>(readUnfinished);
   const unitTitles = units.kind === "loaded" ? Object.fromEntries(units.value.units.map((unit) => [unit.unit_id, unit.title])) : {};
   const [captureMode, setCaptureMode] = useState<CaptureMode>("photo");
   const captureName = useId();

   return (
      <section className="card" data-testid="assessment-setup">
         <h1 className="screen-title">Mock exam</h1>

         {problem !== null ? <p role="alert">{problem}</p> : null}

         {unfinished.kind === "loaded" ? <ResumeSection unfinished={unfinished.value} unitTitles={unitTitles} onResume={onResume} /> : null}

         {shape.kind === "waiting" ? <div aria-busy="true" data-testid="shape-waiting" /> : null}

         {shape.kind === "failed" ? <p className="muted">The exam shape could not be loaded.</p> : null}

         {shape.kind === "loaded" ? (
            <>
               <fieldset className="choice-group">
                  <legend>Free-response answers</legend>

                  {CAPTURE_CHOICES.map((choice) => (
                     <label key={choice.value}>
                        <input
                           type="radio"
                           name={captureName}
                           value={choice.value}
                           checked={captureMode === choice.value}
                           onChange={() => setCaptureMode(choice.value)}
                        />
                        {choice.label}
                     </label>
                  ))}
               </fieldset>

               <p className="muted" data-testid="reference-sheet-note">
                  {shape.value.reference_sheet.note}
               </p>

               <ShapeSection shape={shape.value} captureMode={captureMode} onStartMock={onStartMock} onStartDrill={onStartDrill} />
            </>
         ) : null}

         {units.kind === "loaded" ? <UnitSection units={units.value} onStartUnitCheck={onStartUnitCheck} /> : null}

         {units.kind === "failed" ? <p className="muted">The units could not be loaded.</p> : null}
      </section>
   );
}
