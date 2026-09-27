import { useState } from "react";

/* On the operator's instruction (BUILD-LEDGER.md, 2026-09-27), a calculator question opens the
   Desmos graphing calculator itself inside the page. The frame is another origin, so it cannot
   reach the app, and the CSP's frame-src names this origin and no other. */
export const DESMOS_URL = "https://www.desmos.com/calculator";

export const OPEN_DESMOS_LABEL = "Open Desmos";

export const CLOSE_DESMOS_LABEL = "Close Desmos";

export const DESMOS_TITLE = "Desmos graphing calculator";

export function DesmosPanel() {
   const [isOpen, setIsOpen] = useState(false);

   return (
      <div className="desmos" data-testid="desmos">
         <button type="button" className="text-button" aria-expanded={isOpen} onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? CLOSE_DESMOS_LABEL : OPEN_DESMOS_LABEL}
         </button>

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
