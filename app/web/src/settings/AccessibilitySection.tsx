import { useId, useState } from "react";

import { THEME_CHOICES, chooseTheme, readThemeChoice, type ThemeChoice } from "../theme";

const THEME_LABELS: Record<ThemeChoice, string> = { system: "System", light: "Light", dark: "Dark" };

const KEYBOARD_CONTROLS: ReadonlyArray<[string, string]> = [
   ["Move between controls", "Tab and Shift Tab"],
   ["Move between tabs or answer choices", "Arrow keys"],
   ["Check a study answer", "Enter"],
   ["Rate your confidence", "The number keys"],
   ["Pick an answer option", "A to E"],
   ["Close a dialog or menu", "Escape"]
];

/* 08 lists the theme under accessibility. It sits beside SettingsScreen rather than inside it,
   because SettingsScreen holds exactly 11's scope 17 sections, as the experiment switches do.
   System follows the operating system, as the app did before the setting existed; the choice is
   kept in this browser and applies at once. */
export function AccessibilitySection() {
   const [themeChoice, setThemeChoice] = useState<ThemeChoice>(readThemeChoice);
   const themeName = useId();

   function choose(choice: ThemeChoice) {
      setThemeChoice(choice);
      chooseTheme(choice);
   }

   return (
      <section className="section" data-testid="accessibility-settings">
         <h2 className="section-header">Accessibility</h2>

         <div className="list list-flush">
            <div className="list-row">
               <div className="list-row-body">
                  <span className="list-row-title">Appearance</span>
                  <span className="list-row-meta">Dark suits dim rooms; light suits bright ones. System follows your device.</span>
               </div>

               <fieldset className="list-row-trail choice-group theme-choice" data-testid="theme-choice">
                  <legend className="visually-hidden">Theme</legend>

                  {THEME_CHOICES.map((choice) => (
                     <label key={choice} className="choice-chip" data-chosen={themeChoice === choice ? "true" : undefined}>
                        <input type="radio" name={themeName} value={choice} checked={themeChoice === choice} onChange={() => choose(choice)} />
                        {THEME_LABELS[choice]}
                     </label>
                  ))}
               </fieldset>
            </div>

            <div className="list-row">
               <div className="list-row-body">
                  <span className="list-row-title">Reduced motion</span>
                  <span className="list-row-meta">
                     The app follows your device&apos;s reduced motion setting: feedback then arrives as a short fade instead of a slide.
                  </span>
               </div>
            </div>
         </div>

         <h3>Keyboard controls</h3>

         <div className="table-wrap">
            <table>
               <tbody>
                  {KEYBOARD_CONTROLS.map(([task, keys]) => (
                     <tr key={task}>
                        <td>{task}</td>
                        <td>
                           <kbd className="kbd">{keys}</kbd>
                        </td>
                     </tr>
                  ))}
               </tbody>
            </table>
         </div>
      </section>
   );
}
