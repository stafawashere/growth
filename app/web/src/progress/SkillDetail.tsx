import { useCallback } from "react";

import { readSkill, type SkillDetail as SkillDetailPayload } from "../api/client";
import type { MasteryNodeState } from "../api/types";
import { useLoad } from "../status/load";
import { LoadFailed, Loading } from "../status/LoadState";
import { Dialog } from "../ui/Dialog";
import { NodeMark } from "./MasteryMap";

/* One node of the mastery map opened: what mastering the skill means, in the record's own words,
   and what it is built on, each prerequisite skill with the state the map gives it. */

const STATE_WORDS: Record<MasteryNodeState, string> = {
   mastered: "Mastered",
   fading: "Mastered, review due",
   in_progress: "In progress",
   not_attempted: "Not attempted yet",
   gap: "Prerequisite gap below it"
};

function DetailBody(props: { skill: SkillDetailPayload; onOpenLesson?: (lessonId: string, conceptName: string) => void }) {
   const { skill, onOpenLesson } = props;
   const offersLesson = skill.lesson_id !== null && onOpenLesson !== undefined;

   return (
      <div className="stack" data-testid="skill-detail">
         <p className="cluster">
            <NodeMark state={skill.state} />
            <strong>{STATE_WORDS[skill.state]}</strong>
            {skill.assumed ? <span className="helper">Assumed from the start, not yet shown in an attempt.</span> : null}
         </p>

         {skill.description !== null ? <p>{skill.description}</p> : null}

         {skill.mastered_if !== null ? (
            <div className="stack stack-tight">
               <h3>Mastered when</h3>
               <p>{skill.mastered_if}</p>
            </div>
         ) : null}

         {skill.partially_mastered_if !== null ? (
            <div className="stack stack-tight">
               <h3>Partly there when</h3>
               <p>{skill.partially_mastered_if}</p>
            </div>
         ) : null}

         <div className="stack stack-tight">
            <h3>Built on</h3>

            {skill.prerequisites.length === 0 ? <p>Nothing below it in the graph.</p> : null}

            <ul className="list list-flush">
               {skill.prerequisites.map((entry) => (
                  <li key={entry.id} className="list-row" data-testid="skill-prerequisite">
                     {entry.state !== null ? <NodeMark state={entry.state} /> : null}

                     <div className="list-row-body">
                        <span className="list-row-title">{entry.name}</span>
                        <span className="list-row-meta">
                           {entry.state === null ? "Algebra and earlier work" : STATE_WORDS[entry.state]}
                           {entry.kind === "hard" ? ", required first" : ", supports it"}
                        </span>
                     </div>
                  </li>
               ))}
            </ul>
         </div>

         {offersLesson ? (
            <div className="cluster">
               <button type="button" className="button-secondary" onClick={() => onOpenLesson(skill.lesson_id as string, skill.name)}>
                  Read the lesson
               </button>
            </div>
         ) : null}
      </div>
   );
}

function DetailLoad(props: { skillId: string; onOpenLesson?: (lessonId: string, conceptName: string) => void }) {
   const read = useCallback(() => readSkill(props.skillId), [props.skillId]);
   const load = useLoad<SkillDetailPayload>(read);

   if (load.kind === "waiting") {
      return <Loading testId="skill-detail-waiting" />;
   }

   if (load.kind === "failed") {
      return <LoadFailed testId="skill-detail-failed" onRetry={load.retry} />;
   }

   return <DetailBody skill={load.value} onOpenLesson={props.onOpenLesson} />;
}

export function SkillDetailDialog(props: {
   skillId: string | null;
   title: string;
   onClose: () => void;
   onOpenLesson?: (lessonId: string, conceptName: string) => void;
}) {
   return (
      <Dialog open={props.skillId !== null} title={props.title} onClose={props.onClose} testId="skill-detail-dialog">
         {props.skillId !== null ? <DetailLoad skillId={props.skillId} onOpenLesson={props.onOpenLesson} /> : null}
      </Dialog>
   );
}
