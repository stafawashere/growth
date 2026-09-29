import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import type { AgentMemoriesPayload } from "../api/types";
import { FORGET_EVERYTHING, MEMORY_KIND_LABELS, PROFILE_OFF, RETENTION_LINE } from "./agentCopy";
import { AgentSettingsSection } from "./AgentSettingsSection";

vi.mock("../api/client");

const mocked = vi.mocked(client);

function memories(paused = false): AgentMemoriesPayload {
   return {
      memory_paused: paused,
      groups: [
         {
            kind: "preference",
            label: "How you like to be helped",
            entries: [
               { id: "MEM-1", kind: "preference", text: "Short questions first", skill_ids: [], created_at: "2027-01-04T09:00:00", source_conversation_id: "ACV-1", editable: true }
            ]
         },
         { kind: "confusion", label: "Confusions in your words", entries: [] },
         { kind: "stated_difficulty", label: "What you said was hard", entries: [] },
         {
            kind: "episode",
            label: "Last conversation",
            entries: [
               { id: "MEM-2", kind: "episode", text: "Worked on limits of the form 0/0", skill_ids: [], created_at: "2027-01-05T09:00:00", source_conversation_id: "ACV-2", editable: false }
            ]
         }
      ]
   };
}

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readAgentMemories.mockResolvedValue(memories());
   mocked.readAgentConversations.mockResolvedValue({
      conversations: [{ id: "ACV-2", opened_at: "2027-01-05T09:00:00", last_turn_at: "2027-01-05T09:10:00", closed_at: null, opened_on_screen: "session_item", turn_count: 2 }]
   });
   mocked.readAgentProfile.mockResolvedValue({ profile: null, version: null, experiment: "off" });
});

afterEach(() => {
   cleanup();
});

function memoryRow(text: string) {
   return screen.getByText(text).closest("li") as HTMLElement;
}

describe("the Tutor tab", () => {
   it("lists what the tutor remembers under the kind's label, with Edit only where the student may edit", async () => {
      render(<AgentSettingsSection />);

      await screen.findByText("Short questions first");

      expect(screen.getByText(MEMORY_KIND_LABELS.preference)).toBeTruthy();
      expect(screen.getByText(MEMORY_KIND_LABELS.episode)).toBeTruthy();
      expect(screen.queryByText(MEMORY_KIND_LABELS.confusion)).toBeNull();
      expect(within(memoryRow("Short questions first")).getByRole("button", { name: "Edit" })).toBeTruthy();
      expect(within(memoryRow("Worked on limits of the form 0/0")).queryByRole("button", { name: "Edit" })).toBeNull();
      expect(screen.getAllByRole("button", { name: "Forget this" })).toHaveLength(2);
   });

   it("edits an entry's text", async () => {
      mocked.editAgentMemory.mockResolvedValue({ ...memories().groups[0].entries[0], text: "One question at a time" });
      render(<AgentSettingsSection />);

      await screen.findByText("Short questions first");
      fireEvent.click(within(memoryRow("Short questions first")).getByRole("button", { name: "Edit" }));
      fireEvent.change(screen.getByLabelText("Edit"), { target: { value: "One question at a time" } });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));

      await waitFor(() => expect(mocked.editAgentMemory).toHaveBeenCalledWith("MEM-1", "One question at a time"));
   });

   it("forgets one entry", async () => {
      mocked.deleteAgentMemory.mockResolvedValue({ deleted: "MEM-2" });
      render(<AgentSettingsSection />);

      await screen.findByText("Worked on limits of the form 0/0");
      fireEvent.click(within(memoryRow("Worked on limits of the form 0/0")).getByRole("button", { name: "Forget this" }));

      await waitFor(() => expect(mocked.deleteAgentMemory).toHaveBeenCalledWith("MEM-2"));
      await waitFor(() => expect(mocked.readAgentMemories).toHaveBeenCalledTimes(2));
   });

   it("refuses Forget everything until the phrase is typed exactly, then sends it", async () => {
      mocked.clearAgentMemory.mockResolvedValue({ cleared: { tutor_memories: 2, agent_turns: 2, agent_conversations: 1, tutor_profiles: 0 } });
      render(<AgentSettingsSection />);

      await screen.findByText("Short questions first");

      const button = screen.getByRole("button", { name: FORGET_EVERYTHING }) as HTMLButtonElement;
      const field = screen.getByLabelText('Type "forget everything" to confirm');

      expect(button.disabled).toBe(true);

      fireEvent.change(field, { target: { value: "forget" } });
      fireEvent.click(button);

      expect(button.disabled).toBe(true);
      expect(mocked.clearAgentMemory).not.toHaveBeenCalled();

      fireEvent.change(field, { target: { value: "forget everything" } });
      fireEvent.click(button);

      await waitFor(() => expect(mocked.clearAgentMemory).toHaveBeenCalledWith("forget everything"));
      await waitFor(() => expect(button.getAttribute("data-outcome")).toBe("done"));
   });

   it("pauses memory with the switch", async () => {
      mocked.updateAgentSettings.mockResolvedValue({ memory_paused: true });
      render(<AgentSettingsSection />);

      const pause = (await screen.findByRole("switch", { name: "Pause memory" })) as HTMLInputElement;

      expect(pause.checked).toBe(false);

      fireEvent.click(pause);

      await waitFor(() => expect(mocked.updateAgentSettings).toHaveBeenCalledWith({ memory_paused: true }));
      await waitFor(() => expect(pause.checked).toBe(true));
   });

   it("lists conversations with the retention line, opens one and deletes one", async () => {
      mocked.readAgentConversation.mockResolvedValue({
         id: "ACV-2",
         opened_at: "2027-01-05T09:00:00",
         last_turn_at: "2027-01-05T09:10:00",
         closed_at: null,
         opened_on_screen: "session_item",
         turn_count: 2,
         turns: [
            { id: "ATN-1", role: "student", text: "Where do I start?", created_at: "2027-01-05T09:00:00", outcome: null },
            { id: "ATN-2", role: "agent", text: "What does the question ask for?", created_at: "2027-01-05T09:00:05", outcome: "complete" }
         ]
      });
      mocked.deleteAgentConversation.mockResolvedValue({ deleted: "ACV-2" });
      render(<AgentSettingsSection />);

      expect(screen.getByText(RETENTION_LINE)).toBeTruthy();

      const row = await screen.findByTestId("agent-conversation-row");

      expect(within(row).getByText("5 January 2027")).toBeTruthy();

      fireEvent.click(within(row).getByRole("button", { name: "Open" }));

      expect(await screen.findByText("What does the question ask for?")).toBeTruthy();

      fireEvent.click(within(row).getByRole("button", { name: "Delete" }));

      await waitFor(() => expect(mocked.deleteAgentConversation).toHaveBeenCalledWith("ACV-2"));
      await waitFor(() => expect(screen.queryByTestId("agent-conversation-row")).toBeNull());
   });

   it("says the profile is off while its switch is off", async () => {
      render(<AgentSettingsSection />);

      expect(await screen.findByText(PROFILE_OFF)).toBeTruthy();
   });
});
