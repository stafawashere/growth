import { useEffect, useRef, useState, type ReactNode } from "react";

/* On the operator's instruction (BUILD-LEDGER.md, 2026-09-27), a calculator question opens the
   Desmos graphing calculator itself inside the page. The frame is another origin, so it cannot
   reach the app, and the CSP's frame-src names this origin and no other. The version is the College
   Board one Bluebook carries (docs/calculator/architecture.md, The Desmos frame), the same string
   the server records on each drill as desmos_url. */
export const DESMOS_URL = "https://www.desmos.com/testing/collegeboard/graphing";

/* The desmos.com terms ask for consent before the tools are framed, so whether Desmos opens in the
   page or in its own window is one switch, and the ruling is the operator's (build-plan.md,
   Rulings waiting on the operator). */
export const DESMOS_OPENS_IN: "frame" | "window" = "frame";

export const DESMOS_CAPTION = "Desmos loads from the internet, so it needs a connection.";

export const OPEN_DESMOS_LABEL = "Open Desmos";

export const CLOSE_DESMOS_LABEL = "Close Desmos";

export const DESMOS_TITLE = "Desmos graphing calculator";

function CalculatorIcon() {
   return (
      <svg className="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
         <path d="M7 3h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" />
         <path d="M8 6h8v4H8z" />
         <path d="M8.5 14h.01M12 14h.01M15.5 14h.01M8.5 17.5h.01M12 17.5h.01M15.5 17.5h.01" />
      </svg>
   );
}

export interface DesmosPanelProps {
   openByDefault?: boolean;
   opensIn?: "frame" | "window";
   onOpenChange?: (isOpen: boolean) => void;
   beside?: ReactNode;
}

export function DesmosPanel(props: DesmosPanelProps) {
   const opensIn = props.opensIn ?? DESMOS_OPENS_IN;
   const opensInWindow = opensIn === "window";
   const [isOpen, setIsOpen] = useState(props.openByDefault === true && !opensInWindow);
   const openChanged = useRef(props.onOpenChange);
   const toggleLabel = isOpen ? CLOSE_DESMOS_LABEL : OPEN_DESMOS_LABEL;

   useEffect(() => {
      openChanged.current = props.onOpenChange;
   }, [props.onOpenChange]);

   useEffect(() => {
      openChanged.current?.(isOpen);
   }, [isOpen]);

   if (opensInWindow) {
      return (
         <div className="desmos" data-testid="desmos">
            <div className="desmos-bar">
               {props.beside}

               <button
                  type="button"
                  className="icon-button"
                  aria-label={OPEN_DESMOS_LABEL}
                  title={OPEN_DESMOS_LABEL}
                  onClick={() => {
                     window.open(DESMOS_URL, "_blank", "noopener,noreferrer");
                     openChanged.current?.(true);
                  }}
               >
                  <CalculatorIcon />
               </button>
            </div>

            <p className="caption">{DESMOS_CAPTION}</p>
         </div>
      );
   }

   return (
      <div className="desmos" data-testid="desmos">
         <div className="desmos-bar">
            {props.beside}

            <button
               type="button"
               className="icon-button"
               aria-label={toggleLabel}
               title={toggleLabel}
               aria-expanded={isOpen}
               onClick={() => setIsOpen(!isOpen)}
            >
               <CalculatorIcon />
            </button>
         </div>

         {isOpen ? (
            <>
               <iframe
                  className="desmos-frame"
                  src={DESMOS_URL}
                  title={DESMOS_TITLE}
                  referrerPolicy="no-referrer"
                  sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
               />

               <p className="caption">{DESMOS_CAPTION}</p>
            </>
         ) : null}
      </div>
   );
}
