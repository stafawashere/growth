import { describe, expect, it } from "vitest";

import { servedText } from "./LessonText";

describe("servedText", () => {
   it("drops a parenthetical of record ids and page citations and an evidence tag", () => {
      const authored = "Rival: differentiating in a length, stopping short of time (BC-ERR-04017). The rule earns its own point (sg-25:20, crabbc-25:24) [inferred].";

      expect(servedText(authored)).toBe("Rival: differentiating in a length, stopping short of time. The rule earns its own point.");
   });

   it("keeps a citation that is part of a sentence and a parenthetical with words", () => {
      const verbatim = "Not earned by: a product rule written without differentials, which sg-22:16 states (see the note).";

      expect(servedText(verbatim)).toBe(verbatim);
   });

   it("leaves inline mathematics alone", () => {
      const withMath = "The limit \\(\\lim_{x\\to 2}(x^2)\\) is 4 (ced:67).";

      expect(servedText(withMath)).toBe("The limit \\(\\lim_{x\\to 2}(x^2)\\) is 4.");
   });
});
