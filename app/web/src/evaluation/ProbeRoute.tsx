import { useCallback, useEffect, useRef, useState } from "react";

import { answerProbeItem, ApiError, readNextProbeItem, readProbe, startProbe, type ProbeAnswer } from "../api/client";
import type { ProbeAdministration, ProbeServedItem } from "../api/types";
import { ProbeFinished, ProbeIntro, ProbeItemView } from "./ProbeScreen";

/* openAdministrationId names the probe GET /probe reported open, and null starts a new one once
   the student chooses to from the intro. */
export interface ProbeRouteProps {
   openAdministrationId: string | null;
   onLeave: () => void;
}

type ProbeStage =
   | { kind: "intro"; refusal: string | null }
   | { kind: "waiting" }
   | { kind: "failed" }
   | { kind: "item"; administrationId: string; item: ProbeServedItem }
   | { kind: "finished"; administration: ProbeAdministration };

function refusalOf(failure: unknown) {
   const isServerRefusal = failure instanceof ApiError;

   return isServerRefusal ? failure.detail : "The concept probe could not be started.";
}

/* No route reads one administration, so a probe that ends on resume is found in GET /probe's
   history. */
async function finishedAdministration(administrationId: string, latest: ProbeAdministration | null) {
   if (latest !== null) {
      return latest;
   }

   const probe = await readProbe();
   const found = probe.history.find((entry) => entry.id === administrationId);

   if (found === undefined) {
      throw new Error(`the probe history carries no ${administrationId}`);
   }

   return found;
}

export function ProbeRoute({ openAdministrationId, onLeave }: ProbeRouteProps) {
   const isResuming = openAdministrationId !== null;

   const [stage, setStage] = useState<ProbeStage>(isResuming ? { kind: "waiting" } : { kind: "intro", refusal: null });
   const [selectedOptionId, setSelectedOptionId] = useState<string | null>(null);
   const [answerMathJson, setAnswerMathJson] = useState<unknown>(null);
   const [answerUnavailable, setAnswerUnavailable] = useState(false);
   const [sending, setSending] = useState(false);

   const resumed = useRef(false);
   const inFlight = useRef(false);
   const shownAt = useRef(0);

   const advance = useCallback(async (administrationId: string, latest: ProbeAdministration | null) => {
      const next = await readNextProbeItem(administrationId);
      const hasFinished = next.item === null;

      if (hasFinished) {
         const administration = await finishedAdministration(administrationId, latest);

         setStage({ kind: "finished", administration });

         return;
      }

      setSelectedOptionId(null);
      setAnswerMathJson(null);
      setAnswerUnavailable(false);
      shownAt.current = Date.now();

      setStage({ kind: "item", administrationId, item: next.item as ProbeServedItem });
   }, []);

   useEffect(() => {
      const shouldResume = openAdministrationId !== null && !resumed.current;

      if (!shouldResume) {
         return;
      }

      resumed.current = true;

      advance(openAdministrationId, null).catch(() => setStage({ kind: "failed" }));
   }, [advance, openAdministrationId]);

   async function start() {
      setStage({ kind: "waiting" });

      let administration: ProbeAdministration;

      try {
         administration = await startProbe();
      } catch (failure) {
         setStage({ kind: "intro", refusal: refusalOf(failure) });

         return;
      }

      advance(administration.id, null).catch(() => setStage({ kind: "failed" }));
   }

   const noteAnswerUnavailable = useCallback(() => {
      setAnswerUnavailable(true);
   }, []);

   async function send(answer: ProbeAnswer) {
      const isOnItem = stage.kind === "item";
      const canSend = isOnItem && !inFlight.current;

      if (!canSend) {
         return;
      }

      inFlight.current = true;
      setSending(true);

      try {
         const administration = await answerProbeItem(stage.administrationId, {
            item_id: stage.item.id,
            answer,
            elapsed_ms: Date.now() - shownAt.current
         });

         await advance(stage.administrationId, administration);
      } catch {
         // no plan copy exists for a refused probe answer, so the item stays on screen to retry
      } finally {
         inFlight.current = false;
         setSending(false);
      }
   }

   if (stage.kind === "intro") {
      return <ProbeIntro refusal={stage.refusal} onStart={start} onLeave={onLeave} />;
   }

   if (stage.kind === "waiting") {
      return <section aria-busy="true" data-testid="probe-waiting" />;
   }

   if (stage.kind === "failed") {
      return (
         <section className="card">
            <p data-testid="probe-failed" className="muted">
               The concept probe could not be loaded.
            </p>

            <button type="button" className="text-button" onClick={onLeave}>
               Back to progress
            </button>
         </section>
      );
   }

   if (stage.kind === "finished") {
      return <ProbeFinished administration={stage.administration} onLeave={onLeave} />;
   }

   const servesMcq = stage.item.format === "mcq";
   const hasAnswer = servesMcq ? selectedOptionId !== null : answerMathJson !== null && !answerUnavailable;
   const answer: ProbeAnswer = servesMcq ? { option_id: selectedOptionId as string } : { mathjson: answerMathJson };

   return (
      <ProbeItemView
         item={stage.item}
         selectedOptionId={selectedOptionId}
         onOptionChange={setSelectedOptionId}
         onAnswerChange={setAnswerMathJson}
         answerUnavailable={answerUnavailable}
         onAnswerUnavailable={noteAnswerUnavailable}
         canSend={hasAnswer && !sending}
         onSend={() => send(answer)}
      />
   );
}