export interface QueueLine {
   id: string;
   label: string;
   count: number;
}

export type HomeScreenStatus = "ready" | "empty" | "inProgress";

export interface HomeScreenProps {
   status: HomeScreenStatus;
   examDate: string;
   daysToExam: number;
   queueMinutes: number;
   queueLines: ReadonlyArray<QueueLine>;
   onStartSession: () => void;
   onAddPracticeSet: () => void;
   onResumeSession: () => void;
}

function ExamFooter(props: { examDate: string; daysToExam: number }) {
   return (
      <p style={{ color: "var(--growth-text-muted)" }}>
         Exam: {props.examDate}, {props.daysToExam} days away
      </p>
   );
}

function ReadyQueue(props: HomeScreenProps) {
   const { queueMinutes, queueLines, onStartSession } = props;

   return (
      <>
         <p style={{ color: "var(--growth-text-primary)" }}>
            About {queueMinutes} minutes of work is in today&apos;s queue.
         </p>

         <ul>
            {queueLines.map((line) => (
               <li key={line.id} data-testid="queue-line" style={{ color: "var(--growth-text-secondary)" }}>
                  {line.count} {line.label}
               </li>
            ))}
         </ul>

         <button
            type="button"
            onClick={onStartSession}
            style={{
               background: "var(--growth-accent-base)",
               color: "var(--growth-accent-contrast-text)",
               border: "1px solid var(--growth-border-hairline)"
            }}
         >
            Start today&apos;s set
         </button>
      </>
   );
}

function EmptyQueue(props: { onAddPracticeSet: () => void }) {
   return (
      <>
         <p style={{ color: "var(--growth-text-primary)" }}>
            Nothing is due today. You can add a 15 minute practice set if you want one.
         </p>

         <button
            type="button"
            onClick={props.onAddPracticeSet}
            style={{
               background: "var(--growth-accent-base)",
               color: "var(--growth-accent-contrast-text)",
               border: "1px solid var(--growth-border-hairline)"
            }}
         >
            Add a 15 minute practice set
         </button>
      </>
   );
}

function SessionInProgress(props: { onResumeSession: () => void }) {
   return (
      <>
         <p style={{ color: "var(--growth-text-primary)" }}>You have a set in progress.</p>

         <button
            type="button"
            onClick={props.onResumeSession}
            style={{
               background: "var(--growth-accent-base)",
               color: "var(--growth-accent-contrast-text)",
               border: "1px solid var(--growth-border-hairline)"
            }}
         >
            Resume
         </button>
      </>
   );
}

export function HomeScreen(props: HomeScreenProps) {
   const { status, examDate, daysToExam, onAddPracticeSet, onResumeSession } = props;

   return (
      <section style={{ background: "var(--growth-surface-page)", color: "var(--growth-text-primary)" }}>
         <h1 style={{ color: "var(--growth-text-primary)" }}>Calculus BC</h1>

         <h2 style={{ color: "var(--growth-text-secondary)" }}>Today</h2>

         {status === "ready" && <ReadyQueue {...props} />}
         {status === "empty" && <EmptyQueue onAddPracticeSet={onAddPracticeSet} />}
         {status === "inProgress" && <SessionInProgress onResumeSession={onResumeSession} />}

         <ExamFooter examDate={examDate} daysToExam={daysToExam} />
      </section>
   );
}
