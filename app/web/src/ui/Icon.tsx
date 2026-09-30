/* The redesign's line icons, drawn on a 24 unit grid with the stroke width app.css gives .icon.
   Circles and rounded rectangles are written as arcs in path data, so no size attribute carries a
   number of its own. */

const PATHS = {
   user: ["M9 8a3 3 0 1 0 6 0a3 3 0 1 0 -6 0", "M5 20v-2a7 7 0 0 1 14 0v2z"],
   back: ["m14 5-7 7 7 7"],
   next: ["m10 5 7 7-7 7", "M4 12h13"],
   close: ["m6 6 12 12M18 6 6 18"],
   check: ["m5 12 4 4L19 6"],
   minus: ["M6 12h12"],
   alert: ["M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0", "M12 7v6M12 16.5h.01"],
   question: ["M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0", "M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 17h.01"],
   flag: ["M5 21V3h13l-3 4 3 4H5"],
   upload: ["M12 16V3m-5 5 5-5 5 5M4 16v5h16v-5"],
   download: ["M12 3v13m-5-5 5 5 5-5M4 17v4h16v-4"],
   chevron: ["m9 5 7 7-7 7"],
   down: ["m6 9 6 6 6-6"],
   book: ["M3 4h6l3 2 3-2h6v15h-6l-3 2-3-2H3zM12 6v15"],
   gear: [
      "M4 6h9M17 6h3M4 12h3M11 12h9M4 18h11M19 18h1",
      "M13 6a2 2 0 1 0 4 0a2 2 0 1 0 -4 0",
      "M7 12a2 2 0 1 0 4 0a2 2 0 1 0 -4 0",
      "M15 18a2 2 0 1 0 4 0a2 2 0 1 0 -4 0"
   ],
   clock: ["M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0", "M12 7v5l3 2"],
   compass: ["M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0", "m15.5 8.5-1.6 4.8a1 1 0 0 1-.6.6l-4.8 1.6 1.6-4.8a1 1 0 0 1 .6-.6z"],
   shuffle: [
      "m18 14 3 3-3 3M18 4l3 3-3 3",
      "M3 17h2.5a4 4 0 0 0 3.3-1.7l4.4-6.6A4 4 0 0 1 16.5 7H21M3 7h2.5a4 4 0 0 1 3 1.4M21 17h-4.5a4 4 0 0 1-3-1.4"
   ],
   doc: ["M6 3h8l4 4v14H6z", "M14 3v5h4M9 13h6M9 17h6"],
   refresh: ["M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8", "M3 3v5h5"],
   calendar: [
      "M6 5h12a2.5 2.5 0 0 1 2.5 2.5v10.5a2.5 2.5 0 0 1 -2.5 2.5h-12a2.5 2.5 0 0 1 -2.5 -2.5v-10.5a2.5 2.5 0 0 1 2.5 -2.5z",
      "M8 3v4m8-4v4M3.5 10h17"
   ],
   note: ["M5 4h14v16H5z", "M9 9h6M9 13h6M9 17h3"],
   zoom: ["M4.5 11a6.5 6.5 0 1 0 13 0a6.5 6.5 0 1 0 -13 0", "m16 16 4 4M11 8.5v5M8.5 11h5"],
   highlight: ["m14 5 5 5-8 8H6v-5z", "M4 21h16"],
   grid: [
      "M5 4h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-4a1 1 0 0 1 1 -1z",
      "M15 4h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-4a1 1 0 0 1 1 -1z",
      "M5 14h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-4a1 1 0 0 1 1 -1z",
      "M15 14h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1v-4a1 1 0 0 1 1 -1z"
   ],
   graph: ["M4 4v16h16", "M7 16c3-8 6-8 12-10"],
   edit: ["M4 20h4L19 9l-4-4L4 16z", "m13.5 6.5 4 4"],
   print: ["M7 9V4h10v5M7 17H4v-8h16v8h-3", "M7 14h10v6H7z"],
   sun: [
      "M8 12a4 4 0 1 0 8 0a4 4 0 1 0 -8 0",
      "M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"
   ],
   moon: ["M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"],
   chart: ["M4 20V10M10 20V4M16 20v-7M22 20H2"],
   clipboard: [
      "M7 4h10a2 2 0 0 1 2 2v13a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-13a2 2 0 0 1 2 -2z",
      "M9 4V3h6v1M9 12l2 2 4-4"
   ],
   signOut: ["M15 4h4v16h-4", "M10 8l-4 4 4 4M6 12h10"],
   spanOne: ["M5 7v6M9.7 7v6M14.3 7v6M19 7v6", "M3 17h4"],
   spanUnit: ["M5 7v6M9.7 7v6M14.3 7v6M19 7v6", "M3 17h9"],
   spanAll: ["M5 7v6M9.7 7v6M14.3 7v6M19 7v6", "M3 17h18"]
} as const;

export type IconName = keyof typeof PATHS;

export type IconSize = "sm" | "md" | "lg";

const SIZE_CLASS: Record<IconSize, string> = {
   sm: "icon",
   md: "icon icon-md",
   lg: "icon icon-lg"
};

export function Icon(props: { name: IconName; size?: IconSize; className?: string }) {
   const sizeClass = SIZE_CLASS[props.size ?? "sm"];
   const className = props.className === undefined ? sizeClass : `${sizeClass} ${props.className}`;

   return (
      <svg className={className} viewBox="0 0 24 24" aria-hidden="true" focusable="false">
         {PATHS[props.name].map((path) => (
            <path key={path} d={path} />
         ))}
      </svg>
   );
}
