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
   onOpenProgress?: () => void;
}

function ExamFooter(props: { examDate: string; daysToExam: number }) {
   return (
      <p className="caption">
         Exam: {props.examDate}, {props.daysToExam} days away
      </p>
   );
}

function ReadyQueue(props: HomeScreenProps) {
   const { queueMinutes, queueLines, onStartSession } = props;

   return (
      <>
         <p>About {queueMinutes} minutes of work is in today&apos;s queue.</p>

         <ul className="queue-counts">
            {queueLines.map((line) => (
               <li key={line.id} data-testid="queue-line">
                  {line.count} {line.label}
               </li>
            ))}
         </ul>

         <button type="button" className="button-primary" onClick={onStartSession}>
            Start today&apos;s set
         </button>
      </>
   );
}

function EmptyQueue(props: { onAddPracticeSet: () => void }) {
   return (
      <>
         <p>Nothing is due today. You can add a 15 minute practice set if you want one.</p>

         <button type="button" className="button-primary" onClick={props.onAddPracticeSet}>
            Add a 15 minute practice set
         </button>
      </>
   );
}

function SessionInProgress(props: { onResumeSession: () => void }) {
   return (
      <>
         <p>You have a set in progress.</p>

         <button type="button" className="button-primary" onClick={props.onResumeSession}>
            Resume
         </button>
      </>
   );
}

export function HomeScreen(props: HomeScreenProps) {
   const { status, examDate, daysToExam, onAddPracticeSet, onResumeSession, onOpenProgress } = props;
   const offersProgress = onOpenProgress !== undefined;

   return (
      <section className="card home">
         <h1 className="eyebrow">Calculus BC</h1>

         <h2 className="screen-title">Today</h2>

         {status === "ready" && <ReadyQueue {...props} />}
         {status === "empty" && <EmptyQueue onAddPracticeSet={onAddPracticeSet} />}
         {status === "inProgress" && <SessionInProgress onResumeSession={onResumeSession} />}

         {offersProgress && (
            <button type="button" className="text-button" onClick={onOpenProgress}>
               Progress
            </button>
         )}

         <ExamFooter examDate={examDate} daysToExam={daysToExam} />
      </section>
   );
}
