import type { LessonSpec } from "../api/types";
import { FigureView } from "../figures/FigureView";
import { LessonFallback } from "./LessonFallback";
import { LessonTable } from "./LessonTable";
import { buildGraph, isPanelKind, isRecord, panelsOf, type Substitution } from "./specGraph";

/* The contract's spec kinds, plus region_with_axis, which two interactive designs use and the
   reader's brief names among the interactive kinds.

   Mode figure (TEMPLATE.md Delivery; CONTRACT.md Reader): a static declarative figure, labels
   inside, no caption. Every graph-like kind is turned into a GraphFigureSpec and drawn by the
   existing figures/FigureView.tsx; panel kinds draw each panel through the same path; a kind that
   carries a table draws it beside the graph. Anything that cannot be drawn, including a kind the
   contract does not list, shows the block's fallback text in the figure's frame. */

export const SPEC_KINDS = [
   "graph",
   "table",
   "graph_panels",
   "stacked_graphs",
   "graph_pair",
   "graph_with_table",
   "slope_field",
   "implicit_curve",
   "region",
   "diagram",
   "geometric_diagram",
   "parametric_path",
   "vector_diagram",
   "washer",
   "slice_shapes",
   "graph_sweep",
   "graph_zoom",
   "numeric_experiment",
   "particle_on_line",
   "number_line_pair",
   "parametric_trace",
   "solid_from_slices",
   "solid_of_revolution",
   "euler_steps",
   "solution_curves",
   "field_trace",
   "inverse_pair",
   "table_sweep",
   "panels",
   "region_with_axis"
];

export interface LessonFigureProps {
   spec: LessonSpec | undefined;
   fallback?: string;
   substitution?: Substitution;
}

const STACKED_KINDS = ["stacked_graphs", "graph_pair"];

export function LessonFigure({ spec, fallback, substitution }: LessonFigureProps) {
   const isKnown = spec !== undefined && SPEC_KINDS.includes(spec.kind);

   if (!isKnown) {
      return <LessonFallback text={fallback} />;
   }

   const alt = fallback ?? "";

   if (spec.kind === "table" || spec.kind === "table_sweep") {
      return <LessonTable spec={spec} fallback={fallback} />;
   }

   if (isPanelKind(spec.kind)) {
      const drawn = panelsOf(spec).map((panel) => buildGraph(panel, substitution, alt));
      const everyPanelDrawn = drawn.length > 0 && drawn.every((panel) => panel !== null);

      /* A partial set of panels would show a comparison with a side missing, so one panel that
         cannot be drawn sends the whole block to its fallback. */
      if (!everyPanelDrawn) {
         return <LessonFallback text={fallback} />;
      }

      return (
         <figure
            className="lesson-figure lesson-panels"
            data-testid="lesson-figure"
            data-kind={spec.kind}
            data-layout={STACKED_KINDS.includes(spec.kind) ? "stacked" : "row"}
         >
            {drawn.map((panel, index) => (
               <div key={index} className="lesson-panel" data-testid="lesson-figure-panel">
                  <FigureView spec={panel!.spec} />
               </div>
            ))}
         </figure>
      );
   }

   const graph = buildGraph(spec, substitution, alt);

   if (graph === null) {
      return <LessonFallback text={fallback} />;
   }

   const table = spec.kind === "graph_with_table" && isRecord(spec.table) ? spec.table : null;

   return (
      <figure className="lesson-figure" data-testid="lesson-figure" data-kind={spec.kind}>
         <FigureView spec={graph.spec} />

         {table !== null ? <LessonTable spec={table} fallback={fallback} /> : null}
      </figure>
   );
}
