import type { LessonSpec } from "../api/types";
import { MathText } from "../math/MathText";
import { LessonFallback } from "./LessonFallback";
import { isRecord } from "./specGraph";

/* Mode table (TEMPLATE.md Delivery): the numbers as a rendered table, labels inside its frame as
   the closing rows. A marked row and the current row of a model or a sweep carry a glyph and a
   word as well as a tint, so they read the same in greyscale (08 Accessibility). Row numbers in
   marked_rows and highlight_rows count from 1, as the designs write "rows 2 and 4". */

export const MARKED_GLYPH = ">";

export const MARKED_WORD = "marked";

export const CURRENT_GLYPH = "->";

export const CURRENT_WORD = "current";

export interface LessonTableProps {
   spec: LessonSpec | Record<string, unknown>;
   fallback?: string;
   currentRow?: number | null;
}

function cellText(value: unknown) {
   if (typeof value === "number") {
      return String(value);
   }

   return typeof value === "string" ? value : "";
}

function rowNumbers(value: unknown): number[] {
   return Array.isArray(value) ? value.filter((entry): entry is number => typeof entry === "number") : [];
}

function labelLines(value: unknown): string[] {
   if (!Array.isArray(value)) {
      return [];
   }

   return value
      .map((entry) => (typeof entry === "string" ? entry : isRecord(entry) && typeof entry.text === "string" ? entry.text : null))
      .filter((text): text is string => text !== null);
}

export function LessonTable({ spec, fallback, currentRow = null }: LessonTableProps) {
   const columns = Array.isArray(spec.columns) ? spec.columns.map(cellText) : [];
   const rows = Array.isArray(spec.rows) ? spec.rows.filter(Array.isArray) : [];

   if (columns.length === 0) {
      return <LessonFallback text={fallback} />;
   }

   const marked = new Set([...rowNumbers(spec.marked_rows), ...rowNumbers(spec.highlight_rows)]);
   const hasCurrent = currentRow !== null;
   const hasMarks = marked.size > 0 || hasCurrent;
   const labels = labelLines(spec.labels);

   return (
      <table className="figure-table lesson-table" data-testid="lesson-table">
         <thead>
            <tr>
               {hasMarks ? (
                  <th scope="col">
                     <span className="visually-hidden">Row</span>
                  </th>
               ) : null}
               {columns.map((column, index) => (
                  <th key={index} scope="col">
                     <MathText text={column} />
                  </th>
               ))}
            </tr>
         </thead>
         <tbody>
            {rows.map((row, rowIndex) => {
               const isMarked = marked.has(rowIndex + 1);
               const isCurrent = currentRow === rowIndex;
               const glyph = isCurrent ? CURRENT_GLYPH : isMarked ? MARKED_GLYPH : "";
               const word = isCurrent ? CURRENT_WORD : isMarked ? MARKED_WORD : "";

               return (
                  <tr
                     key={rowIndex}
                     className={isCurrent ? "lesson-row-current" : isMarked ? "lesson-row-marked" : undefined}
                     data-marked={isMarked}
                     data-current={isCurrent}
                     aria-current={isCurrent ? "true" : undefined}
                  >
                     {hasMarks ? (
                        <td className="lesson-row-mark">
                           <span aria-hidden="true">{glyph}</span> {word}
                        </td>
                     ) : null}
                     {(row as unknown[]).map((cell, cellIndex) => (
                        <td key={cellIndex}>
                           <MathText text={cellText(cell)} />
                        </td>
                     ))}
                  </tr>
               );
            })}
         </tbody>
         {labels.length > 0 ? (
            <tfoot>
               {labels.map((label, index) => (
                  <tr key={index}>
                     <td colSpan={columns.length + (hasMarks ? 1 : 0)}>
                        <MathText text={label} />
                     </td>
                  </tr>
               ))}
            </tfoot>
         ) : null}
      </table>
   );
}
