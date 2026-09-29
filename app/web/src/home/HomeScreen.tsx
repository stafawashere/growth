import type { BlockFocus, FocusBlock } from "../api/types";
import { Countdown, type CountdownPace } from "../ui/Countdown";
import { Icon, type IconName } from "../ui/Icon";
import { Page, PageHeader, Section } from "../ui/Page";

export interface QueueLine {
   id: string;
   label: string;
   count: number;
}

export type HomeScreenStatus = "ready" | "empty" | "inProgress" | "longGap";

export interface HomeScreenProps {
   status: HomeScreenStatus;
   examDate: string;
   daysToExam: number;
   queueMinutes: number;
   queueLines: ReadonlyArray<QueueLine>;
   focus?: ReadonlyArray<BlockFocus>;
   pace?: CountdownPace | null;
   skillsDueForReview?: number;
   dueTodaySkills?: number;
   dueTodayMinutes?: number;
   onStartSession: () => void;
   onAddPracticeSet: () => void;
   onResumeSession: () => void;
   onStartRediagnostic: () => void;
}

const FOCUS_COPY: Record<FocusBlock, { title: string; intent: string; icon: IconName }> = {
   review: {
      title: "Review",
      intent: "Skills you have learned whose recall is fading, brought back before they slip.",
      icon: "refresh"
   },
   learn: {
      title: "New ground",
      intent: "Skills whose prerequisites you now hold, so they are the next ones within reach.",
      icon: "compass"
   },
   mixed: {
      title: "Mixed practice",
      intent: "Earlier skills shuffled across units, so you practise choosing the method as well as using it.",
      icon: "shuffle"
   }
};

const METRIC_ICON: Record<string, IconName> = {
   due: "refresh",
   frontier: "compass",
   corrected: "note"
};

function unitList(units: ReadonlyArray<number>) {
   const label = units.length === 1 ? "Unit" : "Units";

   return `${label} ${units.join(", ")}`;
}

/* The whole of today's due queue against what block 1 serves of it (app/session/preview.py
   due_today_skills). It is a count, not a target, so it is left out when nothing waits beyond
   the set. */
export function dueBeyondSetSentence(dueTodaySkills: number, skillsDueForReview: number, dueTodayMinutes: number) {
   const waiting = dueTodaySkills - skillsDueForReview;
   const hasWaiting = dueTodaySkills > 0 && waiting > 0;

   if (!hasWaiting) {
      return null;
   }

   const minutes = Math.ceil(dueTodayMinutes);
   const isOneSkill = waiting === 1;
   const skillPhrase = isOneSkill ? "1 more skill is" : `${waiting} more skills are`;
   const minuteWord = minutes === 1 ? "minute" : "minutes";

   return `${skillPhrase} due today, about ${minutes} ${minuteWord}, beyond this set.`;
}

function ExamCountdown(props: { examDate: string; daysToExam: number; pace?: CountdownPace | null }) {
   const unit = props.daysToExam === 1 ? "day" : "days";

   return (
      <Countdown
         days={props.daysToExam}
         unit={unit}
         label="AP Calculus BC exam"
         detail={props.examDate}
         pace={props.pace}
         testId="exam-countdown"
      />
   );
}

function FocusCard(props: { focus: BlockFocus }) {
   const { block, items, skills, more_skills: moreSkills, units } = props.focus;
   const copy = FOCUS_COPY[block];
   const itemWord = items === 1 ? "item" : "items";
   const hasUnits = units.length > 0;
   const namesSkills = block !== "mixed";
   const hasMore = namesSkills && moreSkills > 0;
   const shownSkills = namesSkills ? skills : [];
   const hasList = shownSkills.length > 0 || hasMore;

   return (
      <li className="card card-flush queue-card" data-testid="focus-block">
         <div className="queue-card-head">
            <Icon name={copy.icon} size="md" />

            <div className="grow">
               <h3>{copy.title}</h3>
               <p className="helper">{copy.intent}</p>
               {hasUnits ? <p className="helper">{unitList(units)}</p> : null}
            </div>

            <span className="badge">
               {items} {itemWord}
            </span>
         </div>

         {hasList ? (
            <ul className="queue-list">
               {shownSkills.map((skill) => (
                  <li key={skill} className="queue-item">
                     {skill}
                  </li>
               ))}

               {hasMore ? (
                  <li className="queue-item queue-item-more">
                     <span className="helper">and {moreSkills} more</span>
                  </li>
               ) : null}
            </ul>
         ) : null}
      </li>
   );
}

function ReadyQueue(props: HomeScreenProps) {
   const { queueMinutes, queueLines, focus = [], onStartSession } = props;
   const { skillsDueForReview = 0, dueTodaySkills = 0, dueTodayMinutes = 0 } = props;
   const hasFocus = focus.length > 0;
   const shownLines = queueLines.filter((line) => line.count > 0);
   const beyondSet = dueBeyondSetSentence(dueTodaySkills, skillsDueForReview, dueTodayMinutes);

   return (
      <>
         <div className="card card-raised today-summary">
            <div className="today-overview">
               <div className="today-metrics">
                  <div className="metric" data-testid="queue-minutes">
                     <Icon name="clock" size="lg" />

                     <div className="metric-copy">
                        <span className="stat-value">{`${queueMinutes} minutes`}</span>
                        <span className="stat-label">Estimated time</span>
                     </div>
                  </div>

                  {shownLines.map((line) => (
                     <div key={line.id} data-testid="queue-line" className="metric">
                        <Icon name={METRIC_ICON[line.id] ?? "doc"} size="lg" />

                        <div className="metric-copy">
                           <span className="stat-value">{line.count}</span>{" "}
                           <span className="stat-label">{line.label}</span>
                        </div>
                     </div>
                  ))}
               </div>

               {beyondSet !== null ? (
                  <p className="helper today-beyond" data-testid="due-beyond-set">
                     {beyondSet}
                  </p>
               ) : null}
            </div>

            <button type="button" className="button-primary button-large" onClick={onStartSession}>
               Start today&apos;s set
               <Icon name="next" />
            </button>
         </div>

         {hasFocus ? (
            <Section title="Your learning queue" aside={<span className="eyebrow">What today&apos;s set works on</span>} labelId="focus-heading">
               <ol className="queue-grid">
                  {focus.map((entry) => (
                     <FocusCard key={entry.block} focus={entry} />
                  ))}
               </ol>
            </Section>
         ) : null}
      </>
   );
}

function EmptyQueue(props: { onAddPracticeSet: () => void }) {
   return (
      <Section>
         <p className="muted">Nothing is due today. You can add a 15 minute practice set if you want one.</p>

         <div className="cluster">
            <button type="button" className="button-primary" onClick={props.onAddPracticeSet}>
               Add a 15 minute practice set
            </button>
         </div>
      </Section>
   );
}

function SessionInProgress(props: { onResumeSession: () => void }) {
   return (
      <div className="card card-raised today-summary">
         <div className="today-metrics">
            <p className="lead">You have a set in progress. It picks up at the item you were on.</p>
         </div>

         <button type="button" className="button-primary button-large" onClick={props.onResumeSession}>
            Resume today&apos;s set
            <Icon name="next" />
         </button>
      </div>
   );
}

/* 08 home, long gap: over 21 days since the last set, a re-diagnostic is offered instead of the
   queue, so no queue line and no way into today's set shows here. */
function LongGap(props: { onStartRediagnostic: () => void }) {
   return (
      <div className="cluster">
         <button type="button" className="button-primary" onClick={props.onStartRediagnostic}>
            Start the re-diagnostic
         </button>
      </div>
   );
}

const HEADER_COPY: Record<HomeScreenStatus, { eyebrow: string; title: string; intro: string }> = {
   ready: { eyebrow: "Your daily session", title: "Today", intro: "A little progress, every day." },
   inProgress: { eyebrow: "Your daily session", title: "Today", intro: "A little progress, every day." },
   empty: { eyebrow: "Nothing due right now", title: "Today", intro: "Your next review returns when it is due. Let it settle." },
   longGap: {
      eyebrow: "Returning after a break",
      title: "Welcome back",
      intro: "It has been a while since your last set, so a short re-diagnostic comes before the queue. It updates what the app knows about you and never resets it."
   }
};

export function HomeScreen(props: HomeScreenProps) {
   const { status, examDate, daysToExam, pace, onAddPracticeSet, onResumeSession, onStartRediagnostic } = props;
   const copy = HEADER_COPY[status];

   return (
      <Page
         testId="home"
         header={
            <PageHeader
               eyebrow={copy.eyebrow}
               title={copy.title}
               intro={copy.intro}
               aside={<ExamCountdown examDate={examDate} daysToExam={daysToExam} pace={pace} />}
            />
         }
      >
         {status === "ready" && <ReadyQueue {...props} />}
         {status === "empty" && <EmptyQueue onAddPracticeSet={onAddPracticeSet} />}
         {status === "inProgress" && <SessionInProgress onResumeSession={onResumeSession} />}
         {status === "longGap" && <LongGap onStartRediagnostic={onStartRediagnostic} />}
      </Page>
   );
}
