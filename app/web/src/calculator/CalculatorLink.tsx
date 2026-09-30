import { hashFor, type Place } from "../routing";
import { CALCULATOR_PRACTICE } from "./words";

/* The small link the work carries to the calculator destination (docs/calculator/design.md, Where
   it lives): on a calculator item beside its Open Desmos control, on a calculator part's setup
   screen, and after a calculator lesson's worked example. It is a plain link to the address, so the
   shell's hash router follows it and no screen needs a navigation callback to carry it. A known
   capability opens that capability's procedure card; with none, the card list. */
export function calculatorPlace(capability?: string): Place {
   const hasCapability = capability !== undefined && capability !== "";

   return hasCapability ? { view: "calculator", section: "cards", capability } : { view: "calculator", section: "cards" };
}

export function CalculatorLink(props: { capability?: string; label?: string; place?: Place }) {
   const place = props.place ?? calculatorPlace(props.capability);

   return (
      <a className="text-button" href={hashFor(place)} data-testid="calculator-link">
         {props.label ?? CALCULATOR_PRACTICE}
      </a>
   );
}
