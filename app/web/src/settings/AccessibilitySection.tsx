import { useId, useState } from "react";

import { THEME_CHOICES, chooseTheme, readThemeChoice, type ThemeChoice } from "../theme";

const THEME_LABELS: Record<ThemeChoice, string> = { system: "System", light: "Light", dark: "Dark" };

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
      <section className="card settings" data-testid="accessibility-settings">
         <h2 className="section-heading">Accessibility</h2>

         <fieldset className="choice-group choice-tiles" data-testid="theme-choice">
            <legend>Theme</legend>

            {THEME_CHOICES.map((choice) => (
               <label key={choice}>
                  <input
                     type="radio"
                     name={themeName}
                     value={choice}
                     checked={themeChoice === choice}
                     onChange={() => choose(choice)}
                  />
                  {THEME_LABELS[choice]}
               </label>
            ))}
         </fieldset>
      </section>
   );
}
