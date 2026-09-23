import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import type { BudgetsPayload, ProviderRole, RoleBudget, SettingsPayload } from "../api/types";
import { SettingsScreen, type SettingsScreenProps } from "./SettingsScreen";

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

const providers: ProviderRole[] = [{ role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true }];

function roleBudget(role: string, capUsd: number | null, costUsd: number): RoleBudget {
   return {
      role,
      cap_usd: capUsd,
      cap_tokens: null,
      cost_usd: costUsd,
      tokens_in: 0,
      tokens_out: 0,
      tokens_cached_read: 0,
      tokens_cached_write: 0,
      hard_stopped: false
   };
}

const budgets: BudgetsPayload = {
   day: "2027-01-05",
   roles: [roleBudget("tutor", 2, 0.5)],
   month_to_date_usd: 1.23
};

const queueSettings: SettingsPayload = {
   exam_date: "2027-05-10",
   purge_after: "2027-06-09",
   desired_retention: 0.9
};

const DESIGN_BRIEF = readFileSync(join(process.cwd(), "..", "..", "docs", "plan", "08-design-brief.md"), "utf8");

function capRow() {
   return within(screen.getByTestId("per-role-cap-row"));
}

function baseProps(): SettingsScreenProps {
   return {
      providers,
      budgets,
      onCapChange: vi.fn().mockResolvedValue(true),
      queueSettings,
      onSettingsChange: vi.fn().mockResolvedValue(true),
      onExport: vi.fn().mockResolvedValue(true),
      purgeConfirmationPhrase: "DELETE MY DATA",
      onReauthenticate: vi.fn().mockResolvedValue(true),
      onPurge: vi.fn().mockResolvedValue(true)
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

      fireEvent.change(confirmationInput, { target: { value: props.purgeConfirmationPhrase as string } });
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
      expect(props.onPurge).toHaveBeenCalledWith(props.purgeConfirmationPhrase);
   });

   it("keeps purge disabled when the passkey reauthentication fails", async () => {
      const props = baseProps();
      props.onReauthenticate = vi.fn().mockResolvedValue(false);

      render(<SettingsScreen {...props} />);

      const confirmationInput = screen.getByLabelText(/type/i) as HTMLInputElement;
      fireEvent.change(confirmationInput, { target: { value: props.purgeConfirmationPhrase as string } });

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

describe("SettingsScreen, purge without a confirmation phrase", () => {
   it("withholds the typed field and both purge controls when no phrase was supplied", () => {
      const props = baseProps();

      render(<SettingsScreen {...props} purgeConfirmationPhrase={null} />);

      const verifyButton = screen.getByRole("button", { name: /verify identity/i }) as HTMLButtonElement;
      const purgeButton = screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;

      expect(screen.queryByLabelText(/type/i)).toBeNull();
      expect(verifyButton.disabled).toBe(true);
      expect(purgeButton.disabled).toBe(true);

      fireEvent.click(verifyButton);
      fireEvent.click(purgeButton);

      expect(props.onReauthenticate).not.toHaveBeenCalled();
      expect(props.onPurge).not.toHaveBeenCalled();
   });
});

describe("SettingsScreen, providers and budgets", () => {
   it("renders one read-only provider row per role the route reports, with no change control", () => {
      const manyProviders: ProviderRole[] = [
         { role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true },
         { role: "generator", provider: null, model: null, wired: false }
      ];

      render(<SettingsScreen {...baseProps()} providers={manyProviders} />);

      const rows = screen.getAllByTestId("provider-row");

      expect(rows.length).toBe(manyProviders.length);
      expect(rows[0].textContent).toContain("claude-sonnet-5");
      expect(rows[1].textContent).toContain("not wired");
      expect(screen.queryByRole("button", { name: "change" })).toBeNull();
      expect(screen.getByText(/1\.23/)).toBeTruthy();
   });

   it("keeps the per-role caps hidden until the open control is used", () => {
      render(<SettingsScreen {...baseProps()} />);

      expect(screen.queryAllByTestId("per-role-cap-row").length).toBe(0);
   });

   it("reveals per-role caps behind the open control, ranging over props rather than a typed-out list", () => {
      const manyCaps = [roleBudget("tutor", 2, 0.5), roleBudget("generator", 3, 1), roleBudget("verifier", 1.5, 0)];

      render(<SettingsScreen {...baseProps()} budgets={{ ...budgets, roles: manyCaps }} />);

      fireEvent.click(screen.getByRole("button", { name: "open" }));

      const rows = screen.getAllByTestId("per-role-cap-row");

      expect(rows.length).toBe(manyCaps.length);

      manyCaps.forEach((cap, index) => {
         const rowText = rows[index].textContent ?? "";
         const capField = rows[index].querySelector("input") as HTMLInputElement;

         expect(rowText).toContain(cap.role);
         expect(rowText).toContain(cap.cost_usd.toFixed(2));
         expect(Number(capField.value)).toBe(cap.cap_usd);
      });
   });

   it("hands a changed cap to onCapChange as numbers, a blank field as null", () => {
      const props = baseProps();

      render(<SettingsScreen {...props} />);
      fireEvent.click(screen.getByRole("button", { name: "open" }));

      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4.5" } });
      fireEvent.change(screen.getByLabelText(/cap tokens/), { target: { value: "" } });
      fireEvent.click(capRow().getByRole("button", { name: "save" }));

      expect(props.onCapChange).toHaveBeenCalledWith("tutor", 4.5, null);
   });

   it("refuses to save a role left with no cap at all, which the server refuses too", () => {
      const props = baseProps();

      render(<SettingsScreen {...props} />);
      fireEvent.click(screen.getByRole("button", { name: "open" }));

      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "" } });

      const save = capRow().getByRole("button", { name: "save" }) as HTMLButtonElement;

      expect(save.disabled).toBe(true);

      fireEvent.click(save);
      expect(props.onCapChange).not.toHaveBeenCalled();
   });

   it("refuses to save a cap that is not a number rather than sending it as no cap", () => {
      const props = baseProps();

      render(<SettingsScreen {...props} />);
      fireEvent.click(screen.getByRole("button", { name: "open" }));

      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4.5 dollars" } });
      fireEvent.change(screen.getByLabelText(/cap tokens/), { target: { value: "9000" } });

      const save = capRow().getByRole("button", { name: "save" }) as HTMLButtonElement;

      expect(save.disabled).toBe(true);

      fireEvent.click(save);
      expect(props.onCapChange).not.toHaveBeenCalled();
   });
});

describe("SettingsScreen, sections whose request has not answered", () => {
   it("renders every heading and no digit while providers, budgets and queue settings are null", () => {
      render(<SettingsScreen {...baseProps()} providers={null} budgets={null} queueSettings={null} />);

      expect(screen.getAllByRole("heading", { level: 2 }).length).toBe(scopeSeventeenSections().length);
      expect(document.body.textContent ?? "").not.toMatch(/\d/);
   });
});

describe("SettingsScreen, retention line", () => {
   it("states the plan's default retention, in the plan's own words and date form, only at exam date plus 30 days", () => {
      render(<SettingsScreen {...baseProps()} />);

      const line = screen.getByText(/Default retention/).textContent ?? "";

      expect(line).toBe("Default retention: until 30 days after 10 May 2027.");
      expect(DESIGN_BRIEF).toContain(line);

      cleanup();

      render(<SettingsScreen {...baseProps()} queueSettings={{ ...queueSettings, purge_after: "2027-07-01" }} />);

      expect(screen.queryByText(/Default retention/)).toBeNull();
   });
});

describe("SettingsScreen, design tokens", () => {
   it("styles settings only through var(--growth-<token>) custom properties", () => {
      const contents = readFileSync(join(process.cwd(), "src", "settings", "SettingsScreen.tsx"), "utf8");

      expect(contents).toMatch(/var\(--growth-[a-z-]+\)/);
   });
});

describe("SettingsScreen, editable dates", () => {
   const dateCases = [
      { label: "exam date", field: "exam_date", saved: queueSettings.exam_date, typed: "2028-05-08" },
      { label: "purge date", field: "purge_after", saved: queueSettings.purge_after, typed: "2028-06-07" }
   ];

   it.each(dateCases)("sends a changed $label as $field and nothing else", async (dateCase) => {
      const props = baseProps();

      render(<SettingsScreen {...props} />);

      const field = within(screen.getByTestId(`date-field-${dateCase.label}`));
      const input = field.getByLabelText(dateCase.label) as HTMLInputElement;
      const save = field.getByRole("button", { name: "save" }) as HTMLButtonElement;

      expect(input.value).toBe(dateCase.saved);
      expect(save.disabled).toBe(true);

      fireEvent.change(input, { target: { value: dateCase.typed } });
      fireEvent.click(save);

      await waitFor(() => expect(props.onSettingsChange).toHaveBeenCalledTimes(1));

      expect(props.onSettingsChange).toHaveBeenCalledWith({ [dateCase.field]: dateCase.typed });
   });

   it("shows the date the server read back, not the one typed", () => {
      const { rerender } = render(<SettingsScreen {...baseProps()} />);
      const input = () => screen.getByLabelText("exam date") as HTMLInputElement;

      fireEvent.change(input(), { target: { value: "2028-05-08" } });
      rerender(<SettingsScreen {...baseProps()} queueSettings={{ ...queueSettings, exam_date: "2028-05-09" }} />);

      expect(input().value).toBe("2028-05-09");
   });
});

describe("SettingsScreen, an action that did not happen", () => {
   it("marks export done only when it happened and hands the control back when it did not", async () => {
      const props = baseProps();

      props.onExport = vi.fn().mockResolvedValueOnce(false).mockResolvedValueOnce(true);
      render(<SettingsScreen {...props} />);

      const exportButton = screen.getByRole("button", { name: "export" }) as HTMLButtonElement;

      fireEvent.click(exportButton);

      await waitFor(() => expect(props.onExport).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(exportButton.disabled).toBe(false));

      expect(exportButton.getAttribute("data-outcome")).toBeNull();

      fireEvent.click(exportButton);

      await waitFor(() => expect(exportButton.getAttribute("data-outcome")).toBe("done"));
   });

   it("asks for a new verification after a purge that did not happen and shows no done state", async () => {
      const props = baseProps();

      props.onPurge = vi.fn().mockResolvedValue(false);
      render(<SettingsScreen {...props} />);

      fireEvent.change(screen.getByLabelText(/type/i), { target: { value: props.purgeConfirmationPhrase as string } });
      fireEvent.click(screen.getByRole("button", { name: /verify identity/i }));

      const purgeButton = screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;
      const verifyButton = screen.getByRole("button", { name: /verify identity/i }) as HTMLButtonElement;

      await waitFor(() => expect(purgeButton.disabled).toBe(false));

      fireEvent.click(purgeButton);

      await waitFor(() => expect(props.onPurge).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(verifyButton.disabled).toBe(false));

      expect(purgeButton.disabled).toBe(true);
      expect(purgeButton.getAttribute("data-outcome")).toBeNull();
   });

   it("hands a cap row's save back with the typed value when the change did not happen", async () => {
      const props = baseProps();

      props.onCapChange = vi.fn().mockResolvedValue(false);
      render(<SettingsScreen {...props} />);
      fireEvent.click(screen.getByRole("button", { name: "open" }));

      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4" } });

      const save = capRow().getByRole("button", { name: "save" }) as HTMLButtonElement;

      fireEvent.click(save);

      await waitFor(() => expect(props.onCapChange).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(save.disabled).toBe(false));

      expect(save.getAttribute("data-outcome")).toBeNull();
      expect((screen.getByLabelText(/cap \$/) as HTMLInputElement).value).toBe("4");
   });
});