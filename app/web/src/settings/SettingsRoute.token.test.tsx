import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, render } from "@testing-library/react";
import * as client from "../api/client";
import type { SettingsScreenProps } from "./SettingsScreen";
import { SettingsRoute } from "./SettingsRoute";

vi.mock("../api/client");

const handed: { props: SettingsScreenProps | null } = { props: null };

vi.mock("./SettingsScreen", () => ({
   SettingsScreen: (props: SettingsScreenProps) => {
      handed.props = props;

      return null;
   }
}));

const mocked = vi.mocked(client);

beforeEach(() => {
   vi.clearAllMocks();
   handed.props = null;
   mocked.readProviders.mockReturnValue(new Promise(() => undefined));
   mocked.readBudgets.mockReturnValue(new Promise(() => undefined));
   mocked.readSettings.mockReturnValue(new Promise(() => undefined));
});

afterEach(() => {
   cleanup();
});

describe("SettingsRoute, the purge token", () => {
   it("spends one verification on one purge request, however often the screen asks", async () => {
      mocked.reauthenticate.mockResolvedValue("token-once");
      mocked.requestPurge.mockRejectedValue(Object.assign(new Error("refused"), { status: 500 }));

      render(<SettingsRoute purgeConfirmationPhrase="PHRASE UNDER TEST" saveFile={vi.fn()} />);

      const props = handed.props as SettingsScreenProps;

      expect(await props.onReauthenticate()).toBe(true);
      expect(await props.onPurge("PHRASE UNDER TEST")).toBe(false);
      expect(await props.onPurge("PHRASE UNDER TEST")).toBe(false);

      expect(mocked.requestPurge).toHaveBeenCalledTimes(1);
      expect(mocked.requestPurge).toHaveBeenCalledWith({
         confirmation: "PHRASE UNDER TEST",
         reauth_token: "token-once"
      });
   });
});
