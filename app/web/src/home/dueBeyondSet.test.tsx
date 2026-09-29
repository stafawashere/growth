import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import type { BlockFocus } from "../api/types";
import { HomeScreen, type HomeScreenProps } from "./HomeScreen";

const focus: BlockFocus[] = [
   { block: "review", items: 5, skills: ["Chain rule", "Product rule"], more_skills: 0, units: [2] },
   { block: "learn", items: 8, skills: ["Related rates", "Implicit differentiation"], more_skills: 2, units: [3, 4] },
   { block: "mixed", items: 4, skills: ["Limits by factoring", "Squeeze theorem"], more_skills: 3, units: [1, 2] }
];

function props(overrides: Partial<HomeScreenProps> = {}): HomeScreenProps {
   return {
      status: "ready",
      examDate: "2027-05-10",
      daysToExam: 223,
      queueMinutes: 38,
      queueLines: [{ id: "due", label: "skills due for review", count: 2 }],
      focus,
      onStartSession: vi.fn(),
      onAddPracticeSet: vi.fn(),
      onResumeSession: vi.fn(),
      onStartRediagnostic: vi.fn(),
      ...overrides
   };
}

afterEach(() => {
   cleanup();
});

describe("the due queue beyond today's set", () => {
   it("states how many due skills and minutes wait beyond the set", () => {
      render(<HomeScreen {...props({ skillsDueForReview: 2, dueTodaySkills: 39, dueTodayMinutes: 47.2 })} />);

      expect(screen.getByTestId("due-beyond-set").textContent).toBe(
         "37 more skills are due today, about 48 minutes, beyond this set."
      );
   });

   it("is hidden when nothing is due or the set already holds every due skill", () => {
      render(<HomeScreen {...props({ skillsDueForReview: 0, dueTodaySkills: 0, dueTodayMinutes: 0 })} />);

      expect(screen.queryByTestId("due-beyond-set")).toBeNull();

      cleanup();
      render(<HomeScreen {...props({ skillsDueForReview: 4, dueTodaySkills: 4, dueTodayMinutes: 6 })} />);

      expect(screen.queryByTestId("due-beyond-set")).toBeNull();
   });
});

describe("the focus cards", () => {
   function cardFor(title: string) {
      const cards = screen.getAllByTestId("focus-block");
      const card = cards.find((entry) => entry.querySelector("h3")?.textContent === title);

      expect(card).toBeDefined();

      return card as HTMLElement;
   }

   it("names no skill on the mixed practice card, only its intent, units and item count", () => {
      render(<HomeScreen {...props()} />);

      const mixed = cardFor("Mixed practice");

      expect(mixed.querySelectorAll(".queue-item").length).toBe(0);
      expect(mixed.textContent).not.toContain("Squeeze theorem");
      expect(mixed.textContent).toContain("Units 1, 2");
      expect(mixed.textContent).toContain("4 items");
   });

   it("keeps the skill lists on the review and new ground cards", () => {
      render(<HomeScreen {...props()} />);

      expect(cardFor("Review").querySelectorAll(".queue-item").length).toBe(2);
      expect(cardFor("New ground").querySelectorAll(".queue-item").length).toBe(3);
   });
});
