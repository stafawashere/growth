import { useState, type KeyboardEvent } from "react";

import type { MasteryMapPayload, MasteryNode, MasteryNodeState, MasteryUnit } from "../api/types";

/* The mastery map on progress, 08-design-brief.md "Progress": one mark per skill, a row per unit,
   ordered along the prerequisite graph, fading where retrievability has fallen below the target.

   Every state is carried by the shape of its mark as well as by colour, so the map reads in
   greyscale: solid, half filled, a centre dot, an empty outline, a slash. Each mark colour is a
   graphical object under WCAG 2.2 SC 1.4.11 and is one of the tokens app/design/tokens.py lists
   in GRAPHIC_TOKENS, which the token gate holds at 3:1 on every surface.

   The map is one tab stop. Arrow keys move between marks, left and right along the row and up and
   down between units, and the focused mark's sentence is printed beneath the map. The list after
   the legend says the same thing in text, unit by unit. Nothing here animates. */

export interface MasteryMapProps {
   map: MasteryMapPayload;
}

interface Position {
   unitIndex: number;
   nodeIndex: number;
}

const MARK_SIZE = 16;

const OUTLINE = "var(--growth-text-muted)";

const FILL = "var(--growth-accent-base)";

const SLASH = "var(--growth-text-primary)";

export const LEGEND: ReadonlyArray<{ state: MasteryNodeState; text: string }> = [
   { state: "mastered", text: "Solid: mastered and fresh" },
   { state: "fading", text: "Half filled: mastered, retrievability falling, review due" },
   { state: "in_progress", text: "Centre dot: in progress, not yet mastered" },
   { state: "not_attempted", text: "Empty: not yet demonstrated" },
   { state: "gap", text: "Slash: prerequisite gap diagnosed below this node" }
];

function daysAgo(days: number) {
   if (days === 0) {
      return "today";
   }

   return days === 1 ? "1 day ago" : `${days} days ago`;
}

function lastCorrect(node: MasteryNode) {
   const hasSuccess = node.days_since_success !== null;

   return hasSuccess ? ` Last correct ${daysAgo(node.days_since_success!)}.` : "";
}

export function nodeSentence(node: MasteryNode) {
   switch (node.state) {
      case "fading":
         return `${node.name}.${lastCorrect(node)} Due for review.`;
      case "mastered":
         return node.assumed
            ? `${node.name}. Assumed from the start, not yet shown in an attempt.`
            : `${node.name}. Mastered.${lastCorrect(node)}`;
      case "in_progress":
         return `${node.name}. In progress, not yet mastered.`;
      case "gap":
         return `${node.name}. A prerequisite gap was diagnosed below this skill.`;
      default:
         return `${node.name}. Not attempted yet.`;
   }
}

export function unitHeading(unit: MasteryUnit) {
   return `Unit ${unit.number}, ${unit.name}`;
}

export function NodeMark(props: { state: MasteryNodeState }) {
   const { state } = props;
   const isSolid = state === "mastered";
   const isHalf = state === "fading";
   const isDot = state === "in_progress";
   const isSlash = state === "gap";
   const isFilledEdge = isSolid || isHalf;

   return (
      <svg
         viewBox={`0 0 ${MARK_SIZE} ${MARK_SIZE}`}
         width={MARK_SIZE}
         height={MARK_SIZE}
         aria-hidden="true"
         focusable="false"
         data-mark={state}
      >
         <rect
            x={1}
            y={1}
            width={MARK_SIZE - 2}
            height={MARK_SIZE - 2}
            fill={isSolid ? FILL : "none"}
            stroke={isFilledEdge ? FILL : OUTLINE}
            strokeWidth={2}
         />
         {isHalf ? <rect x={1} y={MARK_SIZE / 2} width={MARK_SIZE - 2} height={MARK_SIZE / 2 - 1} fill={FILL} /> : null}
         {isDot ? <rect x={5} y={5} width={6} height={6} fill={FILL} /> : null}
         {isSlash ? <line x1={3} y1={13} x2={13} y2={3} stroke={SLASH} strokeWidth={2} /> : null}
      </svg>
   );
}

function clamp(value: number, lowest: number, highest: number) {
   return Math.max(lowest, Math.min(highest, value));
}

function markId(unitIndex: number, nodeIndex: number) {
   return `mastery-node-${unitIndex}-${nodeIndex}`;
}

export function nextPosition(units: ReadonlyArray<MasteryUnit>, from: Position, key: string): Position | null {
   const lastUnit = units.length - 1;
   const row = units[from.unitIndex].nodes;
   const lastInRow = row.length - 1;

   switch (key) {
      case "ArrowRight": {
         const isRowEnd = from.nodeIndex >= lastInRow;
         const isMapEnd = isRowEnd && from.unitIndex >= lastUnit;

         if (isMapEnd) {
            return from;
         }

         return isRowEnd ? { unitIndex: from.unitIndex + 1, nodeIndex: 0 } : { ...from, nodeIndex: from.nodeIndex + 1 };
      }
      case "ArrowLeft": {
         const isRowStart = from.nodeIndex === 0;
         const isMapStart = isRowStart && from.unitIndex === 0;

         if (isMapStart) {
            return from;
         }

         if (isRowStart) {
            const previousRow = units[from.unitIndex - 1].nodes;

            return { unitIndex: from.unitIndex - 1, nodeIndex: previousRow.length - 1 };
         }

         return { ...from, nodeIndex: from.nodeIndex - 1 };
      }
      case "ArrowDown":
      case "ArrowUp": {
         const step = key === "ArrowDown" ? 1 : -1;
         const unitIndex = clamp(from.unitIndex + step, 0, lastUnit);
         const nodeIndex = clamp(from.nodeIndex, 0, units[unitIndex].nodes.length - 1);

         return { unitIndex, nodeIndex };
      }
      case "Home":
         return { ...from, nodeIndex: 0 };
      case "End":
         return { ...from, nodeIndex: lastInRow };
      default:
         return null;
   }
}

function MapList({ units }: { units: ReadonlyArray<MasteryUnit> }) {
   return (
      <details className="mastery-list">
         <summary>The map as a list, unit by unit</summary>

         {units.map((unit) => (
            <section key={unit.unit_id} aria-label={unitHeading(unit)}>
               <h3 className="label-heading">{unitHeading(unit)}</h3>

               <ul data-testid="mastery-list-unit">
                  {unit.nodes.map((node) => (
                     <li key={node.skill_id}>{nodeSentence(node)}</li>
                  ))}
               </ul>
            </section>
         ))}
      </details>
   );
}

function Legend() {
   return (
      <ul className="mastery-legend" aria-label="Legend">
         {LEGEND.map((entry) => (
            <li key={entry.state}>
               <NodeMark state={entry.state} />
               <span>{entry.text}</span>
            </li>
         ))}
      </ul>
   );
}

export function MasteryMap({ map }: MasteryMapProps) {
   const units = map.units.filter((unit) => unit.nodes.length > 0);
   const [active, setActive] = useState<Position>({ unitIndex: 0, nodeIndex: 0 });
   const [isShowing, setIsShowing] = useState(false);

   const hasNodes = units.length > 0;

   if (!hasNodes) {
      return (
         <section aria-labelledby="mastery-heading">
            <h2 id="mastery-heading" className="section-heading">
               What you can do, and how well it is holding
            </h2>

            <p data-testid="mastery-empty">No skills are loaded yet, so there is nothing to draw.</p>
         </section>
      );
   }

   const activeNode = units[active.unitIndex].nodes[active.nodeIndex];

   function focusMark(position: Position) {
      setActive(position);
      setIsShowing(true);
      document.getElementById(markId(position.unitIndex, position.nodeIndex))?.focus();
   }

   function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
      const target = nextPosition(units, active, event.key);
      const isHandled = target !== null;

      if (!isHandled) {
         return;
      }

      event.preventDefault();
      focusMark(target);
   }

   return (
      <section aria-labelledby="mastery-heading">
         <h2 id="mastery-heading" className="section-heading">
            What you can do, and how well it is holding
         </h2>

         <div
            role="group"
            aria-label="Mastery map. Use the arrow keys to move between skills."
            className="mastery-map"
            data-testid="mastery-map"
            onKeyDown={onKeyDown}
         >
            {units.map((unit, unitIndex) => (
               <div key={unit.unit_id} role="group" aria-label={unitHeading(unit)} className="mastery-row">
                  <p className="caption">{unitHeading(unit)}</p>

                  <div className="mastery-nodes">
                     {unit.nodes.map((node, nodeIndex) => {
                        const isActive = unitIndex === active.unitIndex && nodeIndex === active.nodeIndex;

                        return (
                           <button
                              key={node.skill_id}
                              id={markId(unitIndex, nodeIndex)}
                              type="button"
                              className="mastery-node"
                              tabIndex={isActive ? 0 : -1}
                              aria-label={nodeSentence(node)}
                              data-state={node.state}
                              onFocus={() => {
                                 setActive({ unitIndex, nodeIndex });
                                 setIsShowing(true);
                              }}
                              onClick={() => focusMark({ unitIndex, nodeIndex })}
                           >
                              <NodeMark state={node.state} />
                           </button>
                        );
                     })}
                  </div>
               </div>
            ))}
         </div>

         <p className="muted" data-testid="mastery-caption">
            {isShowing ? nodeSentence(activeNode) : "Select a mark, or move to one with the arrow keys, to read it."}
         </p>

         <Legend />

         <MapList units={units} />
      </section>
   );
}
