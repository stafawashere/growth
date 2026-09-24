import { readFileSync } from "node:fs";
import { join } from "node:path";

import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";

import type { MasteryMapPayload, MasteryNode, MasteryNodeState } from "../api/types";
import { LEGEND, MasteryMap } from "./MasteryMap";

function node(skillId: string, name: string, state: MasteryNodeState, extra: Partial<MasteryNode> = {}): MasteryNode {
   return {
      skill_id: skillId,
      name,
      state,
      depth: 0,
      assumed: false,
      last_success_on: null,
      days_since_success: null,
      ...extra
   };
}

const MAP: MasteryMapPayload = {
   today: "2027-01-05",
   states: ["not_attempted", "in_progress", "mastered", "fading", "gap"],
   units: [
      {
         unit_id: "BC-UNIT-02",
         number: 2,
         name: "Differentiation: Definition and Fundamental Properties",
         nodes: [
            node("S-1", "Power rule", "mastered", { last_success_on: "2027-01-03", days_since_success: 2 }),
            node("S-2", "Chain rule with three layers", "fading", { last_success_on: "2026-12-25", days_since_success: 11 }),
            node("S-3", "Product rule", "in_progress")
         ]
      },
      {
         unit_id: "BC-UNIT-03",
         number: 3,
         name: "Differentiation: Composite, Implicit, and Inverse Functions",
         nodes: [
            node("S-4", "Implicit differentiation", "gap"),
            node("S-5", "Inverse function derivative", "not_attempted")
         ]
      }
   ]
};

function marks() {
   return within(screen.getByTestId("mastery-map")).getAllByRole("button");
}

function markSignature(state: MasteryNodeState) {
   const button = marks().find((mark) => mark.getAttribute("data-state") === state)!;
   const svg = button.querySelector("svg")!;

   return Array.from(svg.children)
      .map((shape) => {
         const geometry = ["x", "y", "width", "height", "x1", "y1", "x2", "y2"]
            .map((name) => shape.getAttribute(name))
            .join(" ");
         const isOpen = shape.getAttribute("fill") === "none";

         return `${shape.tagName}:${isOpen ? "open" : "filled"}:${geometry}`;
      })
      .join(",");
}

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

describe("the mastery map", () => {
   it("names each skill with 08's sentence for its state", () => {
      render(<MasteryMap map={MAP} />);

      const labels = marks().map((mark) => mark.getAttribute("aria-label"));

      expect(labels).toEqual([
         "Power rule. Mastered. Last correct 2 days ago.",
         "Chain rule with three layers. Last correct 11 days ago. Due for review.",
         "Product rule. In progress, not yet mastered.",
         "Implicit differentiation. A prerequisite gap was diagnosed below this skill.",
         "Inverse function derivative. Not attempted yet."
      ]);
   });

   it("draws the five states as five different shapes, so no state depends on colour", () => {
      render(<MasteryMap map={MAP} />);

      const signatures = MAP.states.map(markSignature);

      expect(new Set(signatures).size).toBe(MAP.states.length);
   });

   it("says an assumed mastery is assumed rather than shown", () => {
      const assumed: MasteryMapPayload = {
         ...MAP,
         units: [{ ...MAP.units[0], nodes: [node("S-9", "Function notation", "mastered", { assumed: true })] }]
      };

      render(<MasteryMap map={assumed} />);

      expect(marks()[0].getAttribute("aria-label")).toBe(
         "Function notation. Assumed from the start, not yet shown in an attempt."
      );
   });

   it("is one tab stop, and the arrow keys move along a unit and between units", () => {
      render(<MasteryMap map={MAP} />);

      const reachable = () => marks().filter((mark) => mark.tabIndex === 0);
      const map = screen.getByTestId("mastery-map");

      expect(reachable()).toHaveLength(1);
      expect(reachable()[0].getAttribute("data-state")).toBe("mastered");

      marks()[0].focus();
      fireEvent.keyDown(map, { key: "ArrowRight" });

      expect(document.activeElement).toBe(marks()[1]);
      expect(screen.getByTestId("mastery-caption").textContent).toBe(
         "Chain rule with three layers. Last correct 11 days ago. Due for review."
      );

      fireEvent.keyDown(map, { key: "ArrowDown" });

      expect(document.activeElement).toBe(marks()[4]);

      fireEvent.keyDown(map, { key: "Home" });

      expect(document.activeElement).toBe(marks()[3]);

      fireEvent.keyDown(map, { key: "ArrowLeft" });

      expect(document.activeElement).toBe(marks()[2]);
      expect(reachable()).toEqual([marks()[2]]);
   });

   it("gives a text alternative that lists every skill under its unit, and a legend for all five states", () => {
      render(<MasteryMap map={MAP} />);

      const units = screen.getAllByTestId("mastery-list-unit");
      const listed = units.map((unit) => within(unit).getAllByRole("listitem").map((item) => item.textContent));
      const legend = within(screen.getByRole("list", { name: "Legend" })).getAllByRole("listitem");

      expect(listed).toEqual([
         [
            "Power rule. Mastered. Last correct 2 days ago.",
            "Chain rule with three layers. Last correct 11 days ago. Due for review.",
            "Product rule. In progress, not yet mastered."
         ],
         [
            "Implicit differentiation. A prerequisite gap was diagnosed below this skill.",
            "Inverse function derivative. Not attempted yet."
         ]
      ]);
      expect(legend.map((entry) => entry.querySelector("svg")!.getAttribute("data-mark"))).toEqual(
         LEGEND.map((entry) => entry.state)
      );
      expect(new Set(LEGEND.map((entry) => entry.state))).toEqual(new Set(MAP.states));
   });

   it("prints no count and no percentage anywhere on the map", () => {
      render(<MasteryMap map={MAP} />);

      const text = screen.getByTestId("mastery-map").textContent ?? "";

      expect(text).not.toMatch(/%|percent/);
      expect(text.match(/\d+/g)).toEqual(["2", "3"]);
   });

   it("renders the same under reduced motion, because nothing on it moves", () => {
      const source = readFileSync(join(__dirname, "MasteryMap.tsx"), "utf8");

      expect(source).not.toMatch(/transition|animation|motion-/);

      const { container, unmount } = render(<MasteryMap map={MAP} />);
      const plain = container.innerHTML;

      unmount();
      vi.stubGlobal("matchMedia", (query: string) => ({
         matches: query.includes("reduce"),
         media: query,
         addEventListener: () => undefined,
         removeEventListener: () => undefined
      }));

      const reduced = render(<MasteryMap map={MAP} />).container.innerHTML;

      expect(reduced).toBe(plain);
   });

   it("colours every mark through a token and never through a literal", () => {
      const source = readFileSync(join(__dirname, "MasteryMap.tsx"), "utf8");

      expect(source).not.toMatch(/#[0-9a-fA-F]{3,8}\b|\b(rgba?|hsla?)\(/);
      expect(source).toMatch(/var\(--growth-accent-base\)/);
   });
});
