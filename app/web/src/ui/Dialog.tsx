import { useEffect, useId, useRef, type ReactNode } from "react";

import { Icon } from "./Icon";

/* A modal on the native dialog element, so Escape closes it and focus stays inside while it is
   open; 08's accessibility floor allows a focus trap only in a modal that Escape closes. Focus goes
   back to whatever opened it. A runtime without showModal (jsdom) gets the open attribute. */
export function Dialog(props: {
   open: boolean;
   title: ReactNode;
   onClose: () => void;
   children: ReactNode;
   actions?: ReactNode;
   testId?: string;
}) {
   const element = useRef<HTMLDialogElement | null>(null);
   const returnFocus = useRef<Element | null>(null);
   const titleId = useId();

   useEffect(() => {
      const dialog = element.current;

      if (dialog === null) {
         return;
      }

      const canShowModal = typeof dialog.showModal === "function";

      if (props.open && !dialog.open) {
         returnFocus.current = document.activeElement;

         if (canShowModal) {
            dialog.showModal();
         } else {
            dialog.setAttribute("open", "");
         }
      }

      const shouldClose = !props.open && dialog.open;

      if (shouldClose) {
         if (typeof dialog.close === "function") {
            dialog.close();
         } else {
            dialog.removeAttribute("open");
         }

         const opener = returnFocus.current as HTMLElement | null;

         opener?.focus?.();
      }
   }, [props.open]);

   return (
      <dialog
         ref={element}
         className="dialog"
         aria-labelledby={titleId}
         data-testid={props.testId}
         onCancel={(event) => {
            event.preventDefault();
            props.onClose();
         }}
      >
         {props.open ? (
            <div className="dialog-inner">
               <header className="dialog-header">
                  <h2 id={titleId}>{props.title}</h2>

                  <button type="button" className="icon-button icon-button-small" aria-label="Close dialog" onClick={props.onClose}>
                     <Icon name="close" />
                  </button>
               </header>

               <div className="dialog-body">{props.children}</div>

               {props.actions !== undefined ? <div className="dialog-actions">{props.actions}</div> : null}
            </div>
         ) : null}
      </dialog>
   );
}
