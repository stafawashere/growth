import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { THEME_CHOICE_KEY, followThemeChoice } from "../theme";
import { AccessibilitySection } from "./AccessibilitySection";

beforeEach(() => {
   window.localStorage.clear();
   window.matchMedia = ((query: string) =>
      ({
         matches: false,
         media: query,
         addEventListener: () => undefined,
         removeEventListener: () => undefined
      }) as unknown as MediaQueryList) as typeof window.matchMedia;
   followThemeChoice("system");
});

afterEach(() => {
   cleanup();
   window.localStorage.clear();
});

describe("the theme setting", () => {
   it("offers System, Light and Dark with System chosen until the student picks one", () => {
      render(<AccessibilitySection />);

      const choices = screen.getAllByRole("radio").map((radio) => (radio.closest("label")?.textContent ?? "").trim());

      expect(choices).toEqual(["System", "Light", "Dark"]);
      expect((screen.getByRole("radio", { name: "System" }) as HTMLInputElement).checked).toBe(true);
   });

   it("switches the page's theme the moment a choice is made, and is still chosen on the next visit", () => {
      render(<AccessibilitySection />);

      expect(document.documentElement.getAttribute("data-theme")).toBe("light");

      fireEvent.click(screen.getByRole("radio", { name: "Dark" }));

      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
      expect(window.localStorage.getItem(THEME_CHOICE_KEY)).toBe("dark");

      cleanup();
      render(<AccessibilitySection />);

      expect((screen.getByRole("radio", { name: "Dark" }) as HTMLInputElement).checked).toBe(true);
   });
});
