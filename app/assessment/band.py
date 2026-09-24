"""The score band, 05 "AP score estimate" and "Percentile-style positioning against published
distributions", 11 P5 scope item 7.

Never a single number and never a centre (R24). The band is two score points wide at least, and
wider when the published years disagree or when free-response points are still provisional.

How the band is placed, every step an assumption the result lists:

1. The composite is the two sections' shares weighted by their published weights, read from
   exam-structure.md (50 and 50 today). Multiple choice counts correct answers with no guessing
   penalty.
2. Cut points are not published, so the composite is placed against the cohort instead: the
   national composite is taken to be distributed like the free-response section, the only section
   with published per-question means and standard deviations, as a normal curve with the summed
   means and the summed standard deviations (the widest the per-question figures allow, which
   keeps the placement from claiming more precision than the data gives).
3. The student's position on that curve is read against each published year's score
   distribution, which gives an internal score for that year. The internal score is never
   returned, logged or shown.
4. Each year's internal score is widened to at least one score point either side, kept inside 1 to
   5 by sliding rather than narrowing, and the band is the union over the published years and
   over every way the provisional points could still fall.
"""
import math

from app.assessment import shape
from app.checkpoint import published

MIN_SCORE = 1
MAX_SCORE = 5
HALF_WIDTH = 1

ASSUMPTIONS = (
   {
      "key": "equal_section_weight",
      "text": "The two sections are weighted by their published shares of the exam, {weights}.",
   },
   {
      "key": "cut_points_unknown",
      "text": "College Board does not publish cut points, so the band comes from where this composite would sit in past cohorts, not from a score table.",
   },
   {
      "key": "no_guessing_penalty",
      "text": "Multiple choice is scored as the number answered correctly, with no penalty for a wrong answer.",
   },
   {
      "key": "cohort_shape_from_free_response",
      "text": "Only the free-response section has published per-question means and spreads, so the cohort's composite is assumed to spread like that section.",
   },
   {
      "key": "uncertainty_one_score_point",
      "text": "The uncertainty is at least one full score point either side, so the band is never narrower than that.",
   },
   {
      "key": "form_revised_for_2027",
      "text": "The 2027 form has a revised Section I, so no published year matches its structure.",
   },
   {
      "key": "questions_are_not_the_released_ones",
      "text": "These questions are the app's own, not the released ones the published means belong to, so a per-question comparison is by position, not by problem.",
   },
)


def normal_cdf(z):
   return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def cohort_curve(year):
   """(mean share, spread share) of the free-response section for a published year."""
   means = published.question_means()
   questions = [question for (mean_year, question) in means if mean_year == year]
   maximum = published.points_per_free_response_question() * len(questions)
   total_mean = sum(means[(year, question)].mean for question in questions)
   total_spread = sum(means[(year, question)].sd for question in questions)

   return total_mean / maximum, total_spread / maximum


def composite_share(mcq_correct, mcq_total, frq_points, frq_total):
   weights = shape.section_weights()
   section_one = weights["I"] / (weights["I"] + weights["II"])
   section_two = weights["II"] / (weights["I"] + weights["II"])

   return section_one * mcq_correct / mcq_total + section_two * frq_points / frq_total


def internal_score(percentile, shares):
   """The score whose slice of the published distribution holds the percentile, bottom up."""
   cumulative = 0.0

   for score in range(MIN_SCORE, MAX_SCORE + 1):
      cumulative += shares[score] / 100

      if percentile <= cumulative:
         return score

   return MAX_SCORE


def widened(score):
   low = score - HALF_WIDTH
   high = score + HALF_WIDTH

   if low < MIN_SCORE:
      high += MIN_SCORE - low
      low = MIN_SCORE

   if high > MAX_SCORE:
      low -= high - MAX_SCORE
      high = MAX_SCORE

   return low, high


def band_for(mcq_correct, mcq_total, frq_points, frq_pending, frq_total):
   """frq_pending points are provisional or not yet graded; the band covers every way they fall."""
   distributions = {distribution.year: distribution.shares for distribution in published.score_distributions()}
   years = [year for year in published.published_years() if year in distributions]
   lows = []
   highs = []

   for frq_value in (frq_points, frq_points + frq_pending):
      composite = composite_share(mcq_correct, mcq_total, frq_value, frq_total)

      for year in years:
         mean_share, spread_share = cohort_curve(year)
         percentile = normal_cdf((composite - mean_share) / spread_share)
         low, high = widened(internal_score(percentile, distributions[year]))
         lows.append(low)
         highs.append(high)

   return {"low": min(lows), "high": max(highs), "years": years}


def assumptions():
   weights = shape.section_weights()
   stated = ", ".join(f"Section {section} {weight:g} percent" for section, weight in sorted(weights.items()))

   return [{"key": entry["key"], "text": entry["text"].format(weights=stated)} for entry in ASSUMPTIONS]


def question_comparison(points_by_question):
   """Per question position: the student's points and each published year's mean and spread.

   points_by_question maps an exam question number to {"earned", "pending", "possible"}."""
   means = published.question_means()
   rows = []

   for question in sorted(points_by_question):
      entry = points_by_question[question]
      rows.append({
         "question": question,
         "earned": entry["earned"],
         "pending": entry["pending"],
         "possible": entry["possible"],
         "published": [
            {"year": year, "mean": means[(year, question)].mean, "sd": means[(year, question)].sd}
            for year in published.published_years()
            if (year, question) in means
         ],
      })

   return rows


def result_payload(mcq_correct, mcq_total, frq_points, frq_pending, frq_total, points_by_question):
   band = band_for(mcq_correct, mcq_total, frq_points, frq_pending, frq_total)

   return {
      "band": {"low": band["low"], "high": band["high"]},
      "band_years": band["years"],
      "assumptions": assumptions(),
      "statement": "Position against published distributions, with assumptions. Cut points are not published, so this is a band, not a score.",
      "multiple_choice": {"correct": mcq_correct, "total": mcq_total},
      "free_response": {"earned": frq_points, "pending": frq_pending, "total": frq_total},
      "questions": question_comparison(points_by_question),
   }
