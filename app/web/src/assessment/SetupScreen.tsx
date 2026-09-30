import { useId, useState, type ReactNode } from "react";

import { readAssessmentShape, readCheckUnits, readCheckpoints, readFrqUnits, readUnfinished, type CaptureMode } from "../api/client";
import type {
   AssessmentShape,
   CheckpointsPayload,
   CheckUnitsPayload,
   FrqUnitsPayload,
   PartKey,
   ShapePart,
   UnfinishedAssessment,
   UnfinishedPayload
} from "../api/types";
import { CalculatorLink } from "../calculator/CalculatorLink";
import { formatPlanDate } from "../home/dates";
import type { AssessmentFormat } from "../routing";
import { useLoad } from "../status/load";
import { Loading } from "../status/LoadState";
import { Icon, type IconName } from "../ui/Icon";
import { Page, PageHeader } from "../ui/Page";

/* The assessments hub: resume what is open, pick a format from the rail, set it up and begin.
   08 "Information architecture", mock: setup chooses the form, the parts and paper or typed
   capture. Every count and every minute is read from /assessments/shape, which reads
   research/exam/exam-structure.md, and nothing here schedules an assessment or says when to take
   one. */

export interface SetupScreenProps {
   problem: string | null;
   format?: AssessmentFormat;
   onChangeFormat?: (format: AssessmentFormat) => void;
   onStartMock: (captureMode: CaptureMode) => void;
   onStartDrill: (part: PartKey, captureMode: CaptureMode) => void;
   onStartUnitCheck: (unitId: string, title: string) => void;
   onStartFreeResponse?: (unitId: string) => void;
   onOpenCheckpoint?: (openCheckpointId: string | null) => void;
   onResume: (entry: UnfinishedAssessment, subject: string) => void;
}

interface FormatEntry {
   id: AssessmentFormat;
   title: string;
   meta: string;
   icon: IconName;
}

export function formatTitleOf(format: AssessmentFormat) {
   return FORMATS.find((entry) => entry.id === format)?.title ?? format;
}

const FORMATS: ReadonlyArray<FormatEntry> = [
   { id: "unit", title: "Unit check", meta: "Untimed, marked at the end", icon: "doc" },
   { id: "frq", title: "Free response", meta: "Untimed, graded point by point", icon: "edit" },
   { id: "drill", title: "Part drill", meta: "Timed, one exam part", icon: "clock" },
   { id: "mock", title: "Full mock exam", meta: "Timed, every part in order", icon: "clipboard" },
   { id: "checkpoint", title: "Checkpoint", meta: "A released form, self-scored", icon: "calendar" }
];

const CAPTURE_CHOICES: { value: CaptureMode; label: string; text: string }[] = [
   { value: "photo", label: "Write on paper and photograph each page", text: "Closest to exam day. You confirm what the app read before it is graded." },
   { value: "typed", label: "Type each answer", text: "Quicker to set up. Each part gets its own box." }
];

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

function ResumeSection(props: { unfinished: UnfinishedPayload; unitTitles: Record<string, string>; onResume: SetupScreenProps["onResume"] }) {
   const entries = props.unfinished.unfinished;

   if (entries.length === 0) {
      return null;
   }

   return (
      <section data-testid="resume-list" className="stack stack-tight" aria-label="In progress">
         {entries.map((entry) => {
            const subject = subjectOf(entry, props.unitTitles);
            const title = unfinishedTitle(entry, subject);
            const startedOn = formatPlanDate(entry.started_at.slice(0, 10));

            return (
               <div key={entry.id} className="resume-card" data-testid="resume-entry">
                  <span className="icon-tile">
                     <Icon name="refresh" size="md" />
                  </span>

                  <div className="resume-copy">
                     <span className="eyebrow">In progress</span>
                     <span className="resume-title">{title}</span>
                     <span className="resume-meta">
                        Started {startedOn}, {entry.parts_closed} of {entry.parts_total} parts closed
                     </span>
                  </div>

                  <button type="button" className="button-primary" aria-label={`Resume ${title}`} onClick={() => props.onResume(entry, subject)}>
                     <Icon name="next" />
                     Resume
                  </button>
               </div>
            );
         })}
      </section>
   );
}

function FormatRail(props: { active: AssessmentFormat; onChange: (format: AssessmentFormat) => void }) {
   return (
      <nav className="format-rail" aria-label="Assessment formats">
         <ul className="format-list">
            {FORMATS.map((entry) => {
               const isActive = entry.id === props.active;

               return (
                  <li key={entry.id}>
                     <button
                        type="button"
                        className="format-option"
                        aria-current={isActive ? "true" : undefined}
                        onClick={() => props.onChange(entry.id)}
                     >
                        <span className="icon-tile">
                           <Icon name={entry.icon} size="md" />
                        </span>

                        <span className="format-copy">
                           <span className="format-title">{entry.title}</span>
                           <span className="format-meta">{entry.meta}</span>
                        </span>

                        <Icon name="chevron" />
                     </button>
                  </li>
               );
            })}
         </ul>
      </nav>
   );
}

function SetupStep(props: { index: number; title: string; children: ReactNode; testId?: string }) {
   return (
      <section className="setup-step" data-testid={props.testId}>
         <h3 className="setup-step-title">
            <span className="setup-step-index" aria-hidden="true">
               {props.index}
            </span>
            {props.title}
         </h3>

         {props.children}
      </section>
   );
}

function SetupPanel(props: { kicker: string; title: string; intro: string; children: ReactNode; foot: ReactNode; testId?: string }) {
   return (
      <section className="setup-panel" data-testid={props.testId} aria-labelledby="setup-title">
         <div className="setup-head">
            <span className="eyebrow">{props.kicker}</span>
            <h2 className="setup-title" id="setup-title">
               {props.title}
            </h2>
            <p className="setup-intro">{props.intro}</p>
         </div>

         {props.children}

         <div className="setup-foot">{props.foot}</div>
      </section>
   );
}

function CaptureChoice(props: { value: CaptureMode; onChange: (value: CaptureMode) => void }) {
   const name = useId();

   return (
      <fieldset className="choice-cards">
         <legend className="visually-hidden">Free-response answers</legend>

         {CAPTURE_CHOICES.map((choice) => {
            const isChosen = props.value === choice.value;

            return (
               <label key={choice.value} className="choice-card" data-chosen={isChosen ? "true" : undefined}>
                  <input type="radio" name={name} value={choice.value} checked={isChosen} onChange={() => props.onChange(choice.value)} />

                  <span className="choice-card-body">
                     <strong>{choice.label}</strong>
                     <span className="helper">{choice.text}</span>
                  </span>
               </label>
            );
         })}
      </fieldset>
   );
}

function PartSequence(props: { parts: ReadonlyArray<ShapePart> }) {
   return (
      <ol className="part-sequence" data-testid="mock-parts">
         {props.parts.map((part) => (
            <li key={part.key} className="part-row">
               <span className="part-index" aria-hidden="true">
                  {part.label}
               </span>

               <span className="part-copy">
                  <span className="part-name">
                     {part.label}, {part.question_type.toLowerCase()}
                  </span>
                  <span className="part-meta">
                     {part.question_count} questions in {part.minutes} minutes, {part.calculator_label}
                  </span>
               </span>
            </li>
         ))}
      </ol>
   );
}

function UnitChoice(props: {
   units: ReadonlyArray<{ unit_id: string; title: string }>;
   value: string;
   onChange: (unitId: string) => void;
   label: string;
}) {
   const fieldId = useId();

   return (
      <div className="form-field">
         <label className="visually-hidden" htmlFor={fieldId}>
            {props.label}
         </label>

         <select id={fieldId} className="input" value={props.value} onChange={(event) => props.onChange(event.target.value)}>
            {props.units.map((unit) => (
               <option key={unit.unit_id} value={unit.unit_id}>
                  {unit.title}
               </option>
            ))}
         </select>
      </div>
   );
}

function UnitCheckSetup(props: { units: CheckUnitsPayload; onStart: SetupScreenProps["onStartUnitCheck"] }) {
   const available = props.units.units.filter((unit) => unit.available);
   const [chosen, setChosen] = useState(available[0]?.unit_id ?? "");
   const chosenUnit = available.find((unit) => unit.unit_id === chosen) ?? available[0];
   const canBegin = chosenUnit !== undefined;

   return (
      <SetupPanel
         testId="unit-check-setup"
         kicker="Untimed"
         title="Unit check"
         intro="Work one unit with no hints and no clock. Answers are marked only once the whole check is submitted."
         foot={
            <button type="button" className="button-primary" disabled={!canBegin} onClick={() => chosenUnit !== undefined && props.onStart(chosenUnit.unit_id, chosenUnit.title)}>
               Begin the unit check
               <Icon name="next" />
            </button>
         }
      >
         <SetupStep index={1} title="Choose a unit">
            {available.length === 0 ? (
               <p className="muted">No unit can be checked yet.</p>
            ) : (
               <UnitChoice units={available} value={chosenUnit?.unit_id ?? ""} onChange={setChosen} label="Unit to check" />
            )}
         </SetupStep>
      </SetupPanel>
   );
}

function FreeResponseSetup(props: { units: FrqUnitsPayload; onStart?: (unitId: string) => void }) {
   const [chosen, setChosen] = useState(props.units.units[0]?.unit_id ?? "");
   const canBegin = chosen !== "" && props.onStart !== undefined;

   return (
      <SetupPanel
         testId="frq-setup"
         kicker="Untimed"
         title="Free response"
         intro="Choose a unit. Its free-response questions are served as an untimed unit check, and each answer is graded point by point once you confirm what the app read from your page."
         foot={
            <button type="button" className="button-primary" disabled={!canBegin} onClick={() => props.onStart?.(chosen)}>
               Begin the free response
               <Icon name="next" />
            </button>
         }
      >
         <SetupStep index={1} title="Choose a unit">
            {props.units.units.length === 0 ? (
               <p className="muted">No free-response questions are loaded yet.</p>
            ) : (
               <UnitChoice units={props.units.units} value={chosen} onChange={setChosen} label="Unit for free response" />
            )}
         </SetupStep>
      </SetupPanel>
   );
}

function DrillSetup(props: { shape: AssessmentShape; onStart: SetupScreenProps["onStartDrill"] }) {
   const parts = props.shape.parts;
   const [chosen, setChosen] = useState<string>(parts[0]?.key ?? "");
   const [captureMode, setCaptureMode] = useState<CaptureMode>("photo");
   const partName = useId();
   const chosenPart = parts.find((part) => part.key === chosen);
   const chosenAllowsCalculator = chosenPart?.calculator === true;

   return (
      <SetupPanel
         testId="drill-setup"
         kicker="Timed"
         title="Part drill"
         intro="One exam part under its own clock. A submitted part cannot be reopened."
         foot={
            <button type="button" className="button-primary" disabled={chosen === ""} onClick={() => props.onStart(chosen as PartKey, captureMode)}>
               Drill {parts.find((part) => part.key === chosen)?.label ?? ""}
               <Icon name="next" />
            </button>
         }
      >
         <SetupStep index={1} title="Choose a part">
            <fieldset className="choice-cards">
               <legend className="visually-hidden">Part to drill</legend>

               {parts.map((part) => {
                  const isChosen = part.key === chosen;

                  return (
                     <label key={part.key} className="choice-card" data-chosen={isChosen ? "true" : undefined}>
                        <input type="radio" name={partName} value={part.key} checked={isChosen} onChange={() => setChosen(part.key)} />

                        <span className="choice-card-body">
                           <strong>
                              {part.label}, {part.question_type.toLowerCase()}
                           </strong>
                           <span className="helper">
                              {part.question_count} questions in {part.minutes} minutes, {part.calculator_label}
                           </span>
                        </span>
                     </label>
                  );
               })}
            </fieldset>
         </SetupStep>

         <SetupStep index={2} title="How you answer free response">
            <CaptureChoice value={captureMode} onChange={setCaptureMode} />
         </SetupStep>

         {chosenAllowsCalculator ? <CalculatorPracticeNote /> : null}
      </SetupPanel>
   );
}

/* docs/calculator/design.md, Where it lives: a calculator part offers the link here, on its setup
   screen, and never inside the running part, which reproduces Bluebook. */
function CalculatorPracticeNote() {
   return (
      <div className="setup-step" data-testid="setup-calculator-link">
         <CalculatorLink />
      </div>
   );
}

function MockSetup(props: { shape: AssessmentShape; onStart: SetupScreenProps["onStartMock"] }) {
   const [captureMode, setCaptureMode] = useState<CaptureMode>("photo");
   const hasCalculatorPart = props.shape.parts.some((part) => part.calculator);

   return (
      <SetupPanel
         testId="mock-setup"
         kicker="Timed"
         title="Full mock exam"
         intro="The parts run in this order with a break between them. A submitted part cannot be reopened."
         foot={
            <button type="button" className="button-primary" onClick={() => props.onStart(captureMode)}>
               Start the full mock
               <Icon name="next" />
            </button>
         }
      >
         <SetupStep index={1} title="The parts, in order">
            <PartSequence parts={props.shape.parts} />
         </SetupStep>

         <SetupStep index={2} title="How you answer free response">
            <CaptureChoice value={captureMode} onChange={setCaptureMode} />
         </SetupStep>

         {hasCalculatorPart ? <CalculatorPracticeNote /> : null}
      </SetupPanel>
   );
}

function CheckpointSetup(props: { checkpoints: CheckpointsPayload; onOpen?: (openCheckpointId: string | null) => void }) {
   const { availability } = props.checkpoints;
   const isOpen = availability.open_checkpoint_id !== null;
   const canOpen = (isOpen || availability.available) && props.onOpen !== undefined;
   const waitsForADay = !isOpen && !availability.available && availability.opens_on !== null;

   return (
      <SetupPanel
         testId="checkpoint-setup"
         kicker="Released form"
         title="Checkpoint"
         intro="One released AP free-response form, worked on paper under the exam's own timing and scored by you against the published scoring guidelines."
         foot={
            <button type="button" className="button-primary" disabled={!canOpen} onClick={() => props.onOpen?.(availability.open_checkpoint_id)}>
               {isOpen ? "Continue the checkpoint" : "Take a checkpoint"}
               <Icon name="next" />
            </button>
         }
      >
         <SetupStep index={1} title="When it opens">
            {waitsForADay ? (
               <p className="muted" data-testid="checkpoint-setup-opens-on">
                  The next checkpoint opens on {formatPlanDate(availability.opens_on as string)}.
               </p>
            ) : (
               <p className="muted">{isOpen ? "A checkpoint is open. It picks up where you stopped." : "A checkpoint is open to take now."}</p>
            )}
         </SetupStep>
      </SetupPanel>
   );
}

function Unavailable(props: { what: string }) {
   return (
      <div className="setup-panel">
         <div className="setup-head">
            <p className="muted">{props.what}</p>
         </div>
      </div>
   );
}

function TimedOff() {
   return <Unavailable what="Timed practice is switched off on this installation, so the mock and the part drills are not offered." />;
}

export function SetupScreen(props: SetupScreenProps) {
   const { problem, onStartMock, onStartDrill, onStartUnitCheck, onResume } = props;
   const shape = useLoad<AssessmentShape>(readAssessmentShape);
   const units = useLoad<CheckUnitsPayload>(readCheckUnits);
   const unfinished = useLoad<UnfinishedPayload>(readUnfinished);
   const frqUnits = useLoad<FrqUnitsPayload>(readFrqUnits);
   const checkpoints = useLoad<CheckpointsPayload>(readCheckpoints);
   const [ownFormat, setOwnFormat] = useState<AssessmentFormat>(props.format ?? "unit");
   const isControlled = props.format !== undefined && props.onChangeFormat !== undefined;
   const format = isControlled ? (props.format as AssessmentFormat) : ownFormat;
   const changeFormat = isControlled ? (props.onChangeFormat as (format: AssessmentFormat) => void) : setOwnFormat;
   const unitTitles = units.kind === "loaded" ? Object.fromEntries(units.value.units.map((unit) => [unit.unit_id, unit.title])) : {};

   function panel() {
      if (format === "unit") {
         if (units.kind === "waiting") {
            return <Loading testId="units-waiting" />;
         }

         return units.kind === "failed" ? <Unavailable what="The units could not be loaded." /> : <UnitCheckSetup units={units.value} onStart={onStartUnitCheck} />;
      }

      if (format === "frq") {
         if (frqUnits.kind === "waiting") {
            return <Loading testId="frq-waiting" />;
         }

         return frqUnits.kind === "failed" ? (
            <Unavailable what="The free-response questions could not be loaded." />
         ) : (
            <FreeResponseSetup units={frqUnits.value} onStart={props.onStartFreeResponse} />
         );
      }

      if (format === "checkpoint") {
         if (checkpoints.kind === "waiting") {
            return <Loading testId="checkpoints-waiting" />;
         }

         return checkpoints.kind === "failed" ? (
            <Unavailable what="The checkpoint record could not be loaded." />
         ) : (
            <CheckpointSetup checkpoints={checkpoints.value} onOpen={props.onOpenCheckpoint} />
         );
      }

      if (shape.kind === "waiting") {
         return <Loading testId="shape-waiting" />;
      }

      if (shape.kind === "failed") {
         return <Unavailable what="The exam shape could not be loaded." />;
      }

      if (!shape.value.timed_available) {
         return <TimedOff />;
      }

      return format === "drill" ? <DrillSetup shape={shape.value} onStart={onStartDrill} /> : <MockSetup shape={shape.value} onStart={onStartMock} />;
   }

   return (
      <section data-testid="assessment-setup">
         <Page header={<PageHeader title="Assessments" intro="Pick a format, set it up, and begin." />}>
            {problem !== null ? (
               <p role="alert" className="notice">
                  {problem}
               </p>
            ) : null}

            {unfinished.kind === "loaded" ? <ResumeSection unfinished={unfinished.value} unitTitles={unitTitles} onResume={onResume} /> : null}

            <div className="assessment-workspace">
               <FormatRail active={format} onChange={changeFormat} />

               <div className="stack">
                  {panel()}

                  {shape.kind === "loaded" ? (
                     <p className="helper" data-testid="reference-sheet-note">
                        {shape.value.reference_sheet.note}
                     </p>
                  ) : null}
               </div>
            </div>
         </Page>
      </section>
   );
}
