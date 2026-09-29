import { useEffect, useRef, useState } from "react";

import { initialOf, type CachedAccount } from "../account/cachedAccount";
import { chooseTheme } from "../theme";
import { Icon } from "../ui/Icon";

export interface AccountMenuProps {
   account: CachedAccount | null;
   current: "account" | "settings" | null;
   signingOut: boolean;
   onOpenAccount: () => void;
   onOpenSettings: () => void;
   onSignOut: () => void;
}

function shownTheme() {
   return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
}

/* The avatar in the top bar opens this menu: the account, settings, the theme switch and sign out.
   Escape or a click elsewhere closes it and gives focus back to the avatar. */
export function AccountMenu(props: AccountMenuProps) {
   const [open, setOpen] = useState(false);
   const [theme, setTheme] = useState<"light" | "dark">(shownTheme);
   const trigger = useRef<HTMLButtonElement | null>(null);
   const panel = useRef<HTMLDivElement | null>(null);

   useEffect(() => {
      if (!open) {
         return;
      }

      panel.current?.querySelector<HTMLElement>(".menu-item")?.focus();

      function closeOnEscape(event: KeyboardEvent) {
         if (event.key === "Escape") {
            setOpen(false);
            trigger.current?.focus();
         }
      }

      function closeOnOutsideClick(event: MouseEvent) {
         const target = event.target as Node;
         const isInside = panel.current?.contains(target) === true || trigger.current?.contains(target) === true;

         if (!isInside) {
            setOpen(false);
         }
      }

      document.addEventListener("keydown", closeOnEscape);
      document.addEventListener("mousedown", closeOnOutsideClick);

      return () => {
         document.removeEventListener("keydown", closeOnEscape);
         document.removeEventListener("mousedown", closeOnOutsideClick);
      };
   }, [open]);

   function choose(action: () => void) {
      setOpen(false);
      action();
   }

   function switchTheme() {
      const next = theme === "dark" ? "light" : "dark";

      chooseTheme(next);
      setTheme(next);
   }

   const displayName = props.account?.displayName ?? props.account?.username ?? "Your account";
   const username = props.account?.username;
   const themeLabel = theme === "dark" ? "Switch to light theme" : "Switch to dark theme";

   return (
      <div className="account-menu">
         <button
            ref={trigger}
            type="button"
            className="account-trigger"
            aria-expanded={open}
            aria-controls="account-menu-panel"
            onClick={() => setOpen((wasOpen) => !wasOpen)}
         >
            <span className="avatar" aria-hidden="true">
               {initialOf(props.account)}
            </span>
            <span className="visually-hidden">Account and settings</span>
            <Icon name="down" />
         </button>

         <div ref={panel} className="menu-panel" id="account-menu-panel" hidden={!open}>
            <div className="menu-header">
               <strong>{displayName}</strong>
               {username !== undefined && username !== null ? <span className="helper">@{username}</span> : null}
            </div>

            <button
               type="button"
               className="menu-item"
               aria-current={props.current === "account" ? "page" : undefined}
               onClick={() => choose(props.onOpenAccount)}
            >
               <Icon name="user" />
               Account
            </button>

            <button
               type="button"
               className="menu-item"
               aria-current={props.current === "settings" ? "page" : undefined}
               onClick={() => choose(props.onOpenSettings)}
            >
               <Icon name="gear" />
               Settings
            </button>

            <button type="button" className="menu-item" onClick={() => choose(switchTheme)}>
               <Icon name={theme === "dark" ? "sun" : "moon"} />
               {themeLabel}
            </button>

            <div className="menu-divider" role="separator" />

            <button type="button" className="menu-item" disabled={props.signingOut} onClick={() => choose(props.onSignOut)}>
               <Icon name="signOut" />
               Sign out
            </button>
         </div>
      </div>
   );
}
