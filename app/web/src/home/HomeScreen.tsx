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
   onStartSession: () => void;
   onAddPracticeSet: () => void;
   onResumeSession: () => void;
   onStartRediagnostic: () => void;
   onOpenProgress?: () => void;
   onOpenReview?: () => void;
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

/* 08 home, long gap: over 21 days since the last set, a re-diagnostic is offered instead of the
   queue, so no queue line and no way into today's set shows here. */
function LongGap(props: { onStartRediagnostic: () => void }) {
   return (
      <>
         <p>
            It has been a while since your last set, so a short re-diagnostic comes before the queue. It
            updates what the app knows about you and never resets it.
         </p>

         <button type="button" className="button-primary" onClick={props.onStartRediagnostic}>
            Start the re-diagnostic
         </button>
      </>
   );
}

export function HomeScreen(props: HomeScreenProps) {
   const {
      status,
      examDate,
      daysToExam,
      onAddPracticeSet,
      onResumeSession,
      onStartRediagnostic,
      onOpenProgress,
      onOpenReview
   } = props;
   const offersProgress = onOpenProgress !== undefined;
   const offersReview = onOpenReview !== undefined;

   return (
      <section className="card home">
         <h1 className="eyebrow">Calculus BC</h1>

         <h2 className="screen-title">Today</h2>

         {status === "ready" && <ReadyQueue {...props} />}
         {status === "empty" && <EmptyQueue onAddPracticeSet={onAddPracticeSet} />}
         {status === "inProgress" && <SessionInProgress onResumeSession={onResumeSession} />}
         {status === "longGap" && <LongGap onStartRediagnostic={onStartRediagnostic} />}

         {offersProgress && (
            <button type="button" className="text-button" onClick={onOpenProgress}>
               Progress
            </button>
         )}

         {offersReview && (
            <button type="button" className="text-button" onClick={onOpenReview}>
               Review
            </button>
         )}

         <ExamFooter examDate={examDate} daysToExam={daysToExam} />
      </section>
   );
}
