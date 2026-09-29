import { AiNoticesSetting } from "../notices/AiNotices";
import type { SettingsTab } from "../routing";
import { Page, PageHeader } from "../ui/Page";
import { TabPanel, Tabs } from "../ui/Tabs";
import { AccessibilitySection } from "./AccessibilitySection";
import { OperatorSettings } from "./ExperimentsSection";
import { SettingsRoute } from "./SettingsRoute";
import { DeletePhotosSection, StartingPointSection, StudyPlanSection } from "./StudySections";

/* Settings, opened from the avatar menu: the redesign's six tabs. SettingsRoute draws the sections
   11's scope 17 gives it for the chosen tab, and the sections the later phases added sit beside
   them in the tab they belong to. */

const SETTINGS_TAB_ITEMS: ReadonlyArray<{ id: SettingsTab; label: string }> = [
   { id: "study", label: "Study" },
   { id: "providers", label: "AI providers" },
   { id: "budgets", label: "Budgets" },
   { id: "accessibility", label: "Accessibility" },
   { id: "operator", label: "Operator" },
   { id: "data", label: "Your data" }
];

export interface SettingsPageProps {
   tab: SettingsTab;
   onChangeTab: (tab: SettingsTab) => void;
   purgeConfirmationPhrase: string | null;
   saveFile: (name: string, contents: Blob) => void;
   aiNoticesOn: boolean;
   onAiNoticesChange: (enabled: boolean) => void;
   onOpenEvidence: () => void;
   onRunDiagnostic: () => void;
}

export function SettingsPage(props: SettingsPageProps) {
   const { tab } = props;

   return (
      <Page header={<PageHeader eyebrow="Your preferences" title="Settings" />}>
         <div className="stack stack-loose">
            <Tabs items={SETTINGS_TAB_ITEMS} active={tab} onChange={props.onChangeTab} label="Settings sections" idPrefix="settings" />

            <TabPanel idPrefix="settings" active={tab}>
               <SettingsRoute
                  tab={tab}
                  purgeConfirmationPhrase={props.purgeConfirmationPhrase}
                  saveFile={props.saveFile}
                  beforePurge={tab === "data" ? <DeletePhotosSection /> : undefined}
               />

               {tab === "study" ? (
                  <>
                     <StudyPlanSection />
                     <StartingPointSection onRunDiagnostic={props.onRunDiagnostic} />
                  </>
               ) : null}

               {tab === "providers" ? <AiNoticesSetting enabled={props.aiNoticesOn} onChange={props.onAiNoticesChange} /> : null}

               {tab === "accessibility" ? <AccessibilitySection /> : null}

               {tab === "operator" ? <OperatorSettings onOpenEvidence={props.onOpenEvidence} /> : null}
            </TabPanel>
         </div>
      </Page>
   );
}
