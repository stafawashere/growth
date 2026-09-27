/* The two states every screen passes through while it talks to the server. 08 gives no copy for
   either, so these sentences are the stage 10 ruling (BUILD-LEDGER.md, 2026-09-26): plain, in the
   student's terms, with no digit, and a way to try again wherever a retry is safe. */

export const LOADING_TEXT = "Loading";

export const LOAD_FAILED_TEXT = "This did not load. The app may have stopped or lost its connection.";

export const RETRY_LABEL = "Try again";

export const ACTION_FAILED_TEXT = "That did not go through. Nothing you wrote is lost, so you can try again.";

export function Loading(props: { testId: string }) {
   return (
      <section aria-busy="true" className="load-state" data-testid={props.testId}>
         <p className="muted">{LOADING_TEXT}</p>
      </section>
   );
}

export function LoadFailed(props: { testId: string; onRetry?: () => void }) {
   const offersRetry = props.onRetry !== undefined;

   return (
      <section className="load-state" data-testid={props.testId}>
         <p role="alert">{LOAD_FAILED_TEXT}</p>

         {offersRetry ? (
            <button type="button" className="text-button" onClick={props.onRetry}>
               {RETRY_LABEL}
            </button>
         ) : null}
      </section>
   );
}

export function ActionFailed() {
   return (
      <p role="alert" className="notice" data-testid="action-failed">
         {ACTION_FAILED_TEXT}
      </p>
   );
}
