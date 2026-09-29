import { useState } from "react";

/* On the operator's instruction (BUILD-LEDGER.md, 2026-09-27), a calculator question opens the
   Desmos graphing calculator itself inside the page. The frame is another origin, so it cannot
   reach the app, and the CSP's frame-src names this origin and no other. */
export const DESMOS_URL = "https://www.desmos.com/calculator";

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

export function DesmosPanel() {
   const [isOpen, setIsOpen] = useState(false);
   const toggleLabel = isOpen ? CLOSE_DESMOS_LABEL : OPEN_DESMOS_LABEL;

   return (
      <div className="desmos" data-testid="desmos">
         <div className="desmos-bar">
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

               <p className="caption">Desmos loads from the internet, so it needs a connection.</p>
            </>
         ) : null}
      </div>
   );
}
