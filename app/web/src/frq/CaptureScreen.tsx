import { useEffect, useState } from "react";

import {
   ApiError,
   askForReread,
   bookletAddress,
   confirmReadBack,
   photoAddress,
   readGradings,
   readReadBack,
   requestReadBack,
   startFrqAttempt,
   submitTypedAnswer,
   uploadPhoto,
   type CaptureMode
} from "../api/client";
import type { Confidence, FrqAttempt, FrqQuestion, GradingsPayload, PhotoVerdict, ReadBack } from "../api/types";
import { MathText } from "../math/MathText";
import { ConfidencePrompt } from "../session/ConfidencePrompt";
import { GradingView } from "./GradingView";
import { ReadBackEditor, ReadBackView, emptyReadBack } from "./ReadBack";
import { TypedEntry } from "./TypedEntry";

/* One free-response question inside a unit check, in the order 05 fixes: a booklet-shaped page to
   print, a photograph, the image check, the read-back to confirm or correct, then per-point
   grading. The typed mode, MathLive lines per part, is the secondary mode and skips the
   photograph and the read-back, because what the student typed is what gets graded. Nothing is
   graded before the student presses confirm. An attempt the student already confirmed reopens on
   its grading, never on the photo step. */

export interface CaptureScreenProps {
   sessionId: string;
   question: FrqQuestion;
   pollMilliseconds?: number;
   readFile?: (file: File) => Promise<string>;
   captureMode?: CaptureMode;
}

type Stage = "choosing" | "capturing" | "reading" | "confirming" | "editing" | "typing" | "grading" | "graded" | "stalled";

const SETTLED_STATES = ["graded", "partly_graded"];
const DEFAULT_POLL_MILLISECONDS = 2000;
const MAXIMUM_POLLS = 150;
/* A confirmed attempt has gone to the grader, so reopening it shows the grading, not the photo step. */
const PAST_CONFIRMATION_STATES = ["confirmed", "partly_graded", "graded"];

export const REGRADE_OFFER =
   "This answer was confirmed but no point has been graded after about five minutes. Grading can stop if the app restarted while it ran. Grading it again sends the read-back you already confirmed to the grader once more.";

export const GRADING_STALLED_MESSAGE =
   "Grading has not finished. Your answer is saved; confirming it again grades it again.";

export function base64Of(file: File): Promise<string> {
   return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = () => {
         const dataUrl = String(reader.result);

         resolve(dataUrl.slice(dataUrl.indexOf(",") + 1));
      };
      reader.onerror = () => reject(reader.error);
      reader.readAsDataURL(file);
   });
}

function problemText(problem: unknown, fallback: string) {
   const hasDetail = problem instanceof ApiError && problem.detail !== "";

   return hasDetail ? problem.detail : fallback;
}

export function CaptureScreen({ sessionId, question, pollMilliseconds, readFile, captureMode }: CaptureScreenProps) {
   const [stage, setStage] = useState<Stage>("choosing");
   const [attempt, setAttempt] = useState<FrqAttempt | null>(null);
   const [verdicts, setVerdicts] = useState<PhotoVerdict[]>([]);
   const [readBack, setReadBack] = useState<ReadBack | null>(null);
   const [confidence, setConfidence] = useState<Confidence | null>(null);
   const [gradings, setGradings] = useState<GradingsPayload | null>(null);
   const [rereads, setRereads] = useState<string[]>([]);
   const [problem, setProblem] = useState<string | null>(null);
   const partIds = question.parts.map((part) => part.id);
   const pollEvery = pollMilliseconds ?? DEFAULT_POLL_MILLISECONDS;
   const accepted = verdicts.filter((verdict) => verdict.accepted);

   /* A mock or part drill fixes the capture mode when it opens and has already started the attempt,
      which the start route hands back, so the student is not asked to choose again. */
   useEffect(() => {
      const isModeFixed = captureMode !== undefined;

      if (isModeFixed) {
         choose(captureMode);
      }
   }, []);

   useEffect(() => {
      const isWaiting = stage === "grading" && attempt !== null;

      if (!isWaiting) {
         return undefined;
      }

      let isCurrent = true;
      let polls = 0;
      const timer = setInterval(() => {
         polls += 1;

         if (polls > MAXIMUM_POLLS) {
            clearInterval(timer);

            const wasReopened = readBack === null && attempt.transcription_confirmed;

            if (wasReopened) {
               setStage("stalled");

               return;
            }

            setProblem(GRADING_STALLED_MESSAGE);
            setStage(readBack === null ? "typing" : "confirming");

            return;
         }

         readGradings(attempt.attempt_id).then(
            (payload) => {
               const isSettled = SETTLED_STATES.includes(payload.grading_state ?? "");

               if (isCurrent && isSettled) {
                  setGradings(payload);
                  setStage("graded");
               }
            },
            () => undefined
         );
      }, pollEvery);

      return () => {
         isCurrent = false;
         clearInterval(timer);
      };
   }, [stage, attempt, pollEvery, readBack]);

   async function choose(mode: CaptureMode) {
      setProblem(null);

      try {
         const started = await startFrqAttempt(sessionId, question.id, mode);
         const isPastConfirmation = PAST_CONFIRMATION_STATES.includes(started.grading_state ?? "");

         setAttempt(started);

         if (isPastConfirmation) {
            setStage("grading");

            return;
         }

         setStage(mode === "photo" ? "capturing" : "typing");
      } catch (failure) {
         setProblem(problemText(failure, "The question could not be opened."));
      }
   }

   async function addPhoto(file: File | undefined) {
      const hasFile = file !== undefined && attempt !== null;

      if (!hasFile) {
         return;
      }

      setProblem(null);

      try {
         const encoded = await (readFile ?? base64Of)(file);
         const verdict = await uploadPhoto(attempt.attempt_id, { media_type: file.type || "image/jpeg", data_base64: encoded });

         setVerdicts((current) => [...current, verdict]);
      } catch (failure) {
         setProblem(problemText(failure, "The photo could not be sent."));
      }
   }

   async function readPage() {
      if (attempt === null) {
         return;
      }

      setStage("reading");
      setProblem(null);

      try {
         const read = await requestReadBack(attempt.attempt_id);

         setAttempt(read);
         setReadBack(read.read_back);
         setStage("confirming");
      } catch (failure) {
         setProblem(problemText(failure, "The page could not be read. You can try another photo or type the answer."));
         setStage("capturing");
      }
   }

   async function confirm(corrected: ReadBack | null) {
      const canConfirm = attempt !== null && confidence !== null;

      if (!canConfirm) {
         return;
      }

      setProblem(null);

      try {
         await confirmReadBack(attempt.attempt_id, corrected === null ? { confidence } : { read_back: corrected, confidence });
         setStage("grading");
      } catch (failure) {
         setProblem(problemText(failure, "The read-back could not be confirmed."));
      }
   }

   async function submitTyped(typed: ReadBack) {
      const canSubmit = attempt !== null && confidence !== null;

      if (!canSubmit) {
         return;
      }

      setProblem(null);

      try {
         await submitTypedAnswer(attempt.attempt_id, { read_back: typed, confidence });
         setStage("grading");
      } catch (failure) {
         setProblem(problemText(failure, "The answer could not be sent."));
      }
   }

   async function gradeAgain() {
      if (attempt === null) {
         return;
      }

      setProblem(null);

      try {
         const stored = await readReadBack(attempt.attempt_id);

         if (stored.confirmed === null) {
            setProblem("No confirmed read-back is stored for this answer, so it cannot be graded again.");

            return;
         }

         await confirmReadBack(attempt.attempt_id, { read_back: stored.confirmed });
         setStage("grading");
      } catch (failure) {
         setProblem(problemText(failure, "The answer could not be sent for grading again."));
      }
   }

   async function reread(gradingId: string) {
      setRereads((current) => [...current, gradingId]);

      try {
         const before = gradings?.points.find((point) => point.grading_id === gradingId)?.rereads ?? 0;

         await askForReread(gradingId);

         if (attempt === null) {
            return;
         }

         for (let poll = 0; poll < MAXIMUM_POLLS; poll += 1) {
            const payload = await readGradings(attempt.attempt_id);
            const reread = payload.points.find((point) => point.grading_id === gradingId);
            const hasFinished = reread !== undefined && reread.rereads > before;

            if (hasFinished) {
               setGradings(payload);
               setRereads((current) => current.filter((entry) => entry !== gradingId));

               return;
            }

            await new Promise((resolve) => setTimeout(resolve, pollEvery));
         }
      } catch (failure) {
         setProblem(problemText(failure, "The re-read could not be asked for."));
      }
   }

   return (
      <section className="card" data-testid="capture-screen">
         <h1 className="screen-title">Free response</h1>

         <p>
            <MathText text={question.stem} />
         </p>

         <ul className="frq-parts">
            {question.parts.map((part) => (
               <li key={part.id}>
                  ({part.id}) <MathText text={part.prompt} />
                  {part.setup_required ? <span className="muted"> Show the setup for your calculations.</span> : null}
               </li>
            ))}
         </ul>

         {problem !== null ? <p role="alert">{problem}</p> : null}

         {stage === "choosing" && captureMode === undefined ? (
            <div className="choice-row">
               <button type="button" className="button-primary" onClick={() => choose("photo")}>
                  Write on paper and photograph it
               </button>
               <button type="button" className="text-button" onClick={() => choose("typed")}>
                  Type my answer instead
               </button>
            </div>
         ) : null}

         {stage === "capturing" && attempt !== null ? (
            <div data-testid="photo-capture">
               <p>
                  <a href={bookletAddress(attempt.attempt_id)} target="_blank" rel="noreferrer">
                     Print the answer page
                  </a>
                  , write each part in its box, then photograph the whole page with the four corner squares in view.
               </p>

               <label className="field">
                  Photo of the page
                  <input type="file" accept="image/*" capture="environment" onChange={(event) => addPhoto(event.target.files?.[0])} />
               </label>

               <ul data-testid="photo-verdicts">
                  {verdicts.map((verdict) => (
                     <li key={verdict.image_id}>
                        {verdict.accepted ? "Image check passed: sharp, page markers found, contrast ok." : `Image check: ${verdict.reasons.join("; ")}.`}
                     </li>
                  ))}
               </ul>

               {accepted.length > 0 ? (
                  <button type="button" className="button-primary" onClick={readPage}>
                     Read my page
                  </button>
               ) : null}
            </div>
         ) : null}

         {stage === "reading" ? <p aria-busy="true">Reading your page.</p> : null}

         {stage === "confirming" && readBack !== null && attempt !== null ? (
            <div data-testid="read-back-confirm">
               <div className="read-back-pair">
                  {accepted.slice(-1).map((verdict) => (
                     <img key={verdict.image_id} src={photoAddress(attempt.attempt_id, verdict.image_id)} alt="Your photographed page" className="read-back-photo" />
                  ))}

                  <ReadBackView readBack={readBack} />
               </div>

               <ConfidencePrompt value={confidence} onChange={setConfidence} />

               <p>Is this what you wrote?</p>

               <div className="choice-row">
                  <button type="button" className="button-primary" disabled={confidence === null} onClick={() => confirm(null)}>
                     Yes, grade it
                  </button>
                  <button type="button" className="text-button" onClick={() => setStage("editing")}>
                     No, let me fix it
                  </button>
               </div>

               <p className="muted">Nothing is scored until you confirm this.</p>
            </div>
         ) : null}

         {stage === "editing" && readBack !== null ? (
            <div data-testid="read-back-fix">
               <ReadBackEditor readBack={readBack} onChange={setReadBack} />

               <ConfidencePrompt value={confidence} onChange={setConfidence} />

               <button type="button" className="button-primary" disabled={confidence === null} onClick={() => confirm(readBack)}>
                  Grade what I wrote
               </button>

               <p className="muted">Nothing is scored until you confirm this.</p>
            </div>
         ) : null}

         {stage === "typing" ? (
            <div data-testid="typed-entry">
               <TypedEntry initial={emptyReadBack(partIds)} confidence={confidence} onConfidence={setConfidence} onSubmit={submitTyped} />
            </div>
         ) : null}

         {stage === "grading" ? <p aria-busy="true">Grading each point. A point the gradings disagree on is marked provisional.</p> : null}

         {stage === "stalled" ? (
            <div data-testid="grading-stalled">
               <p>{REGRADE_OFFER}</p>

               <button type="button" className="button-primary" onClick={gradeAgain}>
                  Grade it again
               </button>
            </div>
         ) : null}

         {stage === "graded" && gradings !== null ? (
            <GradingView gradings={gradings} onAskForReread={reread} rereadAskedFor={rereads} />
         ) : null}
      </section>
   );
}
