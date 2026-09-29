import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import { hashFor, placeFromHash } from "../routing";
import { CalculatorRoute } from "./CalculatorRoute";
import { CARDS, INTEGRAL_CARD } from "./fixtures";
import { DRILL_THIS_LABEL, SECTION_DRILL, SECTION_MEASURED, SECTION_PROCEDURES } from "./words";

/* docs/calculator/design.md, Where it lives and The procedure cards: the destination draws its
   cards from the server, and a card's "Drill this" goes to the drill with the card's capability. */

vi.mock("../api/client");

const mocked = vi.mocked(client);

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readCalculatorCards.mockResolvedValue(CARDS);
   mocked.readCalculatorCard.mockResolvedValue(INTEGRAL_CARD);
});

afterEach(() => {
   cleanup();
});

describe("the calculator destination", () => {
   it("lists the cards the server sends, under the three sections", async () => {
      render(<CalculatorRoute section="cards" go={vi.fn()} />);

      const list = await screen.findByTestId("calculator-cards");

      expect(within(list).getAllByRole("button").map((button) => button.textContent)).toEqual(["Definite integral", "Derivative at a point"]);
      expect(screen.getAllByRole("tab").map((tab) => tab.textContent)).toEqual([SECTION_PROCEDURES, SECTION_DRILL, SECTION_MEASURED]);
      expect(mocked.readCalculatorCards).toHaveBeenCalledTimes(1);
   });

   it("opens a card from the list by its id", async () => {
      const go = vi.fn();

      render(<CalculatorRoute section="cards" go={go} />);
      fireEvent.click(await screen.findByRole("button", { name: "Derivative at a point" }));

      expect(go).toHaveBeenCalledWith({ view: "calculator", section: "cards", cardId: "CDC-derivative" });
   });

   it("goes from a card's Drill this to the drill with the card's capability", async () => {
      const go = vi.fn();

      render(<CalculatorRoute section="cards" cardId="CDC-integral" go={go} />);
      fireEvent.click(await screen.findByRole("button", { name: DRILL_THIS_LABEL }));

      expect(mocked.readCalculatorCard).toHaveBeenCalledWith("CDC-integral");
      expect(go).toHaveBeenCalledWith({ view: "calculator", section: "drill", capability: "integral" });
   });

   it("opens the card of a capability asked for by the link", async () => {
      render(<CalculatorRoute section="cards" capability="integral" go={vi.fn()} />);

      expect(await screen.findByTestId("procedure-card")).toBeTruthy();
      expect(mocked.readCalculatorCard).toHaveBeenCalledWith("CDC-integral");
   });

   it("keeps the section, the card and the capability in the address", () => {
      const places = [
         { view: "calculator", section: "cards" },
         { view: "calculator", section: "cards", cardId: "CDC-integral" },
         { view: "calculator", section: "cards", capability: "zero" },
         { view: "calculator", section: "drill", capability: "integral" },
         { view: "calculator", section: "measured" }
      ] as const;

      for (const place of places) {
         expect(placeFromHash(hashFor(place))).toEqual(place);
      }

      expect(placeFromHash("#/calculator")).toEqual({ view: "calculator", section: "cards" });
   });
});
