import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { SettingsScreen, type PerRoleCap, type ProviderRow } from "./SettingsScreen";

function scopeSeventeenSections(): string[] {
   const planPath = join(process.cwd(), "..", "..", "docs", "plan", "11-phased-delivery.md");
   const contents = readFileSync(planPath, "utf8");
   const match = contents.match(/settings \(([^)]*)\)/);

   if (match === null) {
      throw new Error("scope-17 settings clause not found in 11-phased-delivery.md");
   }

   const withoutOnly = match[1].replace(/\s+only\s*$/i, "");
   const items = withoutOnly.split(",").map((item) => item.trim());
   const lastIndex = items.length - 1;
   const lastPair = items[lastIndex].split(/\s+and\s+/i).map((item) => item.trim());

   return [...items.slice(0, lastIndex), ...lastPair];
}

const providers: ProviderRow[] = [{ id: "tutor", role: "tutor", provider: "Anthropic", model: "claude-sonnet-5" }];

const perRoleCaps: PerRoleCap[] = [
   { id: "tutor", role: "tutor", dailyCapDollars: 2, spentTodayDollars: 0.5 }
];

function baseProps() {
   return {
      providers,
      onChangeProvider: vi.fn(),
      dailyCapDollars: 5,
      spentThisMonthDollars: 1.23,
      onDailyCapChange: vi.fn(),
      perRoleCaps,
      onOpenPerRoleCaps: vi.fn(),
      examDate: "2027-05-10",
      onExport: vi.fn(),
      purgeConfirmationPhrase: "DELETE MY DATA",
      onReauthenticate: vi.fn().mockResolvedValue(true),
      onPurge: vi.fn()
   };
}

afterEach(() => {
   cleanup();
});

describe("SettingsScreen, section scope", () => {
   it("renders only the P1-allowed sections named in 11-phased-delivery.md scope 17", () => {
      render(<SettingsScreen {...baseProps()} />);

      const expectedSections = scopeSeventeenSections()
         .map((section) => section.toLowerCase())
         .sort();

      const headings = screen
         .getAllByRole("heading", { level: 2 })
         .map((heading) => (heading.textContent ?? "").trim().toLowerCase())
         .sort();

      expect(headings).toEqual(expectedSections);
   });
});

describe("SettingsScreen, purge", () => {
   it("cannot be triggered without the typed confirmation and a passkey reauthentication", async () => {
      const props = baseProps();

      render(<SettingsScreen {...props} />);

      const confirmationInput = screen.getByLabelText(/type/i) as HTMLInputElement;
      const verifyButton = () => screen.getByRole("button", { name: /verify identity/i }) as HTMLButtonElement;
      const purgeButton = () => screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;

      expect(purgeButton().disabled).toBe(true);
      expect(verifyButton().disabled).toBe(true);

      fireEvent.click(purgeButton());
      expect(props.onPurge).not.toHaveBeenCalled();

      fireEvent.change(confirmationInput, { target: { value: "wrong phrase" } });
      expect(verifyButton().disabled).toBe(true);

      fireEvent.change(confirmationInput, { target: { value: props.purgeConfirmationPhrase } });
      expect(verifyButton().disabled).toBe(false);
      expect(purgeButton().disabled).toBe(true);

      fireEvent.click(purgeButton());
      expect(props.onPurge).not.toHaveBeenCalled();

      fireEvent.click(verifyButton());

      await waitFor(() => {
         expect(purgeButton().disabled).toBe(false);
      });

      fireEvent.click(purgeButton());
      expect(props.onPurge).toHaveBeenCalledTimes(1);
   });

   it("keeps purge disabled when the passkey reauthentication fails", async () => {
      const props = baseProps();
      props.onReauthenticate = vi.fn().mockResolvedValue(false);

      render(<SettingsScreen {...props} />);

      const confirmationInput = screen.getByLabelText(/type/i) as HTMLInputElement;
      fireEvent.change(confirmationInput, { target: { value: props.purgeConfirmationPhrase } });

      const verifyButton = screen.getByRole("button", { name: /verify identity/i }) as HTMLButtonElement;
      fireEvent.click(verifyButton);

      await waitFor(() => {
         expect(props.onReauthenticate).toHaveBeenCalledTimes(1);
      });

      const purgeButton = screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;

      expect(purgeButton.disabled).toBe(true);

      fireEvent.click(purgeButton);
      expect(props.onPurge).not.toHaveBeenCalled();
   });
});

describe("SettingsScreen, providers and budgets", () => {
   it("renders provider rows and budget figures from props rather than a typed-out list", () => {
      const manyProviders: ProviderRow[] = [
         { id: "tutor", role: "tutor", provider: "Anthropic", model: "claude-sonnet-5" },
         { id: "generator", role: "generator", provider: "Anthropic", model: "claude-opus-5" }
      ];

      render(<SettingsScreen {...baseProps()} providers={manyProviders} />);

      const rows = screen.getAllByTestId("provider-row");

      expect(rows.length).toBe(manyProviders.length);
      expect(screen.getByText(/1\.23/)).toBeTruthy();
   });

   it("keeps the per-role caps hidden until the open control is used", () => {
      render(<SettingsScreen {...baseProps()} />);

      expect(screen.queryAllByTestId("per-role-cap-row").length).toBe(0);
   });

   it("reveals per-role caps behind the open control, ranging over props rather than a typed-out list", () => {
      const manyCaps: PerRoleCap[] = [
         { id: "tutor", role: "tutor", dailyCapDollars: 2, spentTodayDollars: 0.5 },
         { id: "generator", role: "generator", dailyCapDollars: 3, spentTodayDollars: 1 },
         { id: "verifier", role: "verifier", dailyCapDollars: 1.5, spentTodayDollars: 0 }
      ];
      const onOpenPerRoleCaps = vi.fn();

      render(<SettingsScreen {...baseProps()} perRoleCaps={manyCaps} onOpenPerRoleCaps={onOpenPerRoleCaps} />);

      fireEvent.click(screen.getByRole("button", { name: "open" }));

      expect(onOpenPerRoleCaps).toHaveBeenCalledTimes(1);

      const rows = screen.getAllByTestId("per-role-cap-row");

      expect(rows.length).toBe(manyCaps.length);

      manyCaps.forEach((cap, index) => {
         const rowText = rows[index].textContent ?? "";

         expect(rowText).toContain(cap.role);
         expect(rowText).toContain(cap.dailyCapDollars.toFixed(2));
      });
   });
});

describe("SettingsScreen, design tokens", () => {
   it("styles settings only through var(--growth-<token>) custom properties", () => {
      const contents = readFileSync(join(process.cwd(), "src", "settings", "SettingsScreen.tsx"), "utf8");

      expect(contents).toMatch(/var\(--growth-[a-z-]+\)/);
   });
});
