import { useId, useMemo, useState } from "react";

import { compile, ExpressionError, type AngleMode, type RealFunction } from "./expression";
import {
   derivativeAt,
   findZeros,
   formatResult,
   integrate,
   plotSegments,
   windowIsUsable,
   type PlotPoint,
   type PlotWindow
} from "./numeric";

/* The Desmos-equivalent panel 05 puts on calculator parts only. The part runner decides whether
   it exists at all; this component never hides or disables itself. */

const PLOT_WIDTH = 480;

const PLOT_HEIGHT = 300;

const PLOT_SAMPLES = 480;

const DEFAULT_WINDOW = { xMin: "-10", xMax: "10", yMin: "-10", yMax: "10" };

type WindowText = typeof DEFAULT_WINDOW;

type Result = { kind: "value"; text: string } | { kind: "problem"; text: string };

const ANGLE_MODE_LABELS: Record<AngleMode, string> = {
   radians: "Radians",
   degrees: "Degrees"
};

function readNumber(text: string, mode: AngleMode) {
   const value = compile(text, mode)(Number.NaN);

   if (!Number.isFinite(value)) {
      throw new ExpressionError(`"${text}" is not a number.`);
   }

   return value;
}

function problemOf(failure: unknown): Result {
   const isExpressionProblem = failure instanceof ExpressionError;

   return { kind: "problem", text: isExpressionProblem ? failure.message : "That could not be worked out." };
}

function pathOf(segment: PlotPoint[], window: PlotWindow) {
   const xScale = PLOT_WIDTH / (window.xMax - window.xMin);
   const yScale = PLOT_HEIGHT / (window.yMax - window.yMin);

   return segment
      .map((point, index) => {
         const screenX = (point.x - window.xMin) * xScale;
         const screenY = PLOT_HEIGHT - (point.y - window.yMin) * yScale;
         const command = index === 0 ? "M" : "L";

         return `${command}${screenX.toFixed(2)} ${screenY.toFixed(2)}`;
      })
      .join(" ");
}

function PlotView(props: { f: RealFunction; window: PlotWindow; source: string }) {
   const { f, window, source } = props;
   const titleId = useId();
   const segments = useMemo(() => plotSegments(f, window, PLOT_SAMPLES), [f, window]);
   const xAxisVisible = window.yMin <= 0 && window.yMax >= 0;
   const yAxisVisible = window.xMin <= 0 && window.xMax >= 0;
   const xAxisY = PLOT_HEIGHT - ((0 - window.yMin) * PLOT_HEIGHT) / (window.yMax - window.yMin);
   const yAxisX = ((0 - window.xMin) * PLOT_WIDTH) / (window.xMax - window.xMin);
   const description =
      `Graph of y = ${source} for x from ${window.xMin} to ${window.xMax} and y from ${window.yMin} to ${window.yMax}.` +
      (segments.length === 0 ? " No part of the curve falls in this window." : "");

   return (
      <svg
         className="graphing-plot"
         data-testid="graphing-plot"
         viewBox={`0 0 ${PLOT_WIDTH} ${PLOT_HEIGHT}`}
         role="img"
         aria-labelledby={titleId}
      >
         <title id={titleId}>{description}</title>

         <rect x={0} y={0} width={PLOT_WIDTH} height={PLOT_HEIGHT} fill="var(--growth-surface-sunken)" />

         {xAxisVisible ? (
            <line x1={0} x2={PLOT_WIDTH} y1={xAxisY} y2={xAxisY} stroke="var(--growth-text-muted)" strokeWidth={1} />
         ) : null}

         {yAxisVisible ? (
            <line x1={yAxisX} x2={yAxisX} y1={0} y2={PLOT_HEIGHT} stroke="var(--growth-text-muted)" strokeWidth={1} />
         ) : null}

         {segments.map((segment, index) => (
            <path key={index} d={pathOf(segment, window)} fill="none" stroke="var(--growth-accent-base)" strokeWidth={2} />
         ))}
      </svg>
   );
}

function ResultLine(props: { result: Result | null; testId: string }) {
   if (props.result === null) {
      return null;
   }

   const role = props.result.kind === "problem" ? "alert" : undefined;

   return (
      <p data-testid={props.testId} role={role}>
         {props.result.text}
      </p>
   );
}

export function GraphingPanel() {
   const [isOpen, setIsOpen] = useState(false);
   const [source, setSource] = useState("");
   const [mode, setMode] = useState<AngleMode>("radians");
   const [windowText, setWindowText] = useState<WindowText>(DEFAULT_WINDOW);
   const [pointText, setPointText] = useState("");
   const [lowerText, setLowerText] = useState("");
   const [upperText, setUpperText] = useState("");
   const [zeros, setZeros] = useState<Result | null>(null);
   const [derivative, setDerivative] = useState<Result | null>(null);
   const [integral, setIntegral] = useState<Result | null>(null);
   const modeName = useId();

   const compiled = useMemo(() => {
      try {
         return { f: compile(source, mode), problem: null };
      } catch (failure) {
         return { f: null, problem: problemOf(failure).text };
      }
   }, [source, mode]);

   const plotWindow = useMemo<PlotWindow | null>(() => {
      try {
         const window = {
            xMin: readNumber(windowText.xMin, mode),
            xMax: readNumber(windowText.xMax, mode),
            yMin: readNumber(windowText.yMin, mode),
            yMax: readNumber(windowText.yMax, mode)
         };

         return windowIsUsable(window) ? window : null;
      } catch {
         return null;
      }
   }, [windowText, mode]);

   const hasSource = source.trim() !== "";
   const canPlot = compiled.f !== null && plotWindow !== null;

   function changeWindow(edge: keyof WindowText, text: string) {
      setWindowText((current) => ({ ...current, [edge]: text }));
   }

   function changeMode(next: AngleMode) {
      setMode(next);
      setZeros(null);
      setDerivative(null);
      setIntegral(null);
   }

   function run(work: (f: RealFunction) => string, show: (result: Result) => void) {
      try {
         const f = compile(source, mode);

         show({ kind: "value", text: work(f) });
      } catch (failure) {
         show(problemOf(failure));
      }
   }

   function showZeros() {
      run((f) => {
         if (plotWindow === null) {
            throw new ExpressionError("Set a window with x min below x max and y min below y max.");
         }

         const found = findZeros(f, plotWindow.xMin, plotWindow.xMax);
         const hasZeros = found.length > 0;

         if (!hasZeros) {
            return "No zero in the window.";
         }

         return `Zeros in the window: ${found.map((zero) => `x = ${formatResult(zero)}`).join(", ")}.`;
      }, setZeros);
   }

   function showDerivative() {
      run((f) => {
         const point = readNumber(pointText, mode);

         return `The derivative at x = ${formatResult(point)} is ${formatResult(derivativeAt(f, point))}.`;
      }, setDerivative);
   }

   function showIntegral() {
      run((f) => {
         const lower = readNumber(lowerText, mode);
         const upper = readNumber(upperText, mode);
         const value = integrate(f, lower, upper);

         return `The integral from ${formatResult(lower)} to ${formatResult(upper)} is ${formatResult(value)}.`;
      }, setIntegral);
   }

   return (
      <section className="graphing-panel" data-testid="graphing-panel" aria-label="Graphing calculator">
         <div className="choice-row">
            <button type="button" className="text-button" aria-expanded={isOpen} onClick={() => setIsOpen(!isOpen)}>
               {isOpen ? "Close graphing panel" : "Open graphing panel"}
            </button>

            <p className="graphing-mode" data-testid="angle-mode">
               Angle mode: {ANGLE_MODE_LABELS[mode]}
            </p>
         </div>

         {isOpen ? (
            <div className="graphing-body">
               <fieldset className="choice-group">
                  <legend>Angle mode</legend>

                  {(Object.keys(ANGLE_MODE_LABELS) as AngleMode[]).map((option) => (
                     <label key={option}>
                        <input
                           type="radio"
                           name={modeName}
                           value={option}
                           checked={mode === option}
                           onChange={() => changeMode(option)}
                        />
                        {ANGLE_MODE_LABELS[option]}
                     </label>
                  ))}
               </fieldset>

               <label className="field">
                  <span>y =</span>
                  <input value={source} onChange={(event) => setSource(event.target.value)} spellCheck={false} />
               </label>

               <p className="caption">
                  Functions: sin, cos, tan, sec, csc, cot, arcsin, arccos, arctan, ln, log (base 10), exp, sqrt,
                  abs. Constants: pi and e.
               </p>

               {hasSource && compiled.problem !== null ? <p role="alert">{compiled.problem}</p> : null}

               <div className="graphing-window">
                  {(Object.keys(DEFAULT_WINDOW) as (keyof WindowText)[]).map((edge) => (
                     <label key={edge} className="field">
                        <span>{edge.replace("Min", " min").replace("Max", " max")}</span>
                        <input value={windowText[edge]} onChange={(event) => changeWindow(edge, event.target.value)} />
                     </label>
                  ))}
               </div>

               {canPlot ? <PlotView f={compiled.f!} window={plotWindow!} source={source} /> : null}

               <button type="button" className="text-button" onClick={showZeros}>
                  Find zeros in the window
               </button>

               <ResultLine result={zeros} testId="graphing-zeros" />

               <div className="graphing-window">
                  <label className="field">
                     <span>Derivative at x =</span>
                     <input value={pointText} onChange={(event) => setPointText(event.target.value)} />
                  </label>
               </div>

               <button type="button" className="text-button" onClick={showDerivative}>
                  Find the derivative
               </button>

               <ResultLine result={derivative} testId="graphing-derivative" />

               <div className="graphing-window">
                  <label className="field">
                     <span>Integral from</span>
                     <input value={lowerText} onChange={(event) => setLowerText(event.target.value)} />
                  </label>

                  <label className="field">
                     <span>to</span>
                     <input value={upperText} onChange={(event) => setUpperText(event.target.value)} />
                  </label>
               </div>

               <button type="button" className="text-button" onClick={showIntegral}>
                  Find the integral
               </button>

               <ResultLine result={integral} testId="graphing-integral" />
            </div>
         ) : null}
      </section>
   );
}
