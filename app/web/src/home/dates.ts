const MILLISECONDS_PER_DAY = 86_400_000;

/* 08-design-brief.md writes a date as "10 May 2027". The formatter is pinned to UTC because an ISO
   calendar date has no zone, and read at local midnight west of UTC it would print the day before. */
const PLAN_DATE_FORMAT = new Intl.DateTimeFormat("en-GB", {
   day: "numeric",
   month: "long",
   year: "numeric",
   timeZone: "UTC"
});

function utcMidnightOf(isoDate: string) {
   const [year, month, day] = isoDate.split("-").map(Number);

   return Date.UTC(year, month - 1, day);
}

export function formatPlanDate(isoDate: string) {
   return PLAN_DATE_FORMAT.format(utcMidnightOf(isoDate));
}

export function daysBetween(fromIsoDate: string, toIsoDate: string) {
   return Math.round((utcMidnightOf(toIsoDate) - utcMidnightOf(fromIsoDate)) / MILLISECONDS_PER_DAY);
}

/* exam_date is a calendar date with no zone. Today is the student's own calendar date, read from
   the local clock, and both are counted as UTC midnights so a daylight saving change between them
   cannot shift the difference by an hour into the neighbouring day. */
export function daysToExam(examDate: string, now: Date) {
   const localToday = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());

   return Math.round((utcMidnightOf(examDate) - localToday) / MILLISECONDS_PER_DAY);
}