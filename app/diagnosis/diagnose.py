"""The diagnostician, docs/plan/11-phased-delivery.md P3 scope item 7, following
docs/plan/03-diagnosis-and-feedback.md "Mapping errors to candidate misconceptions",
"Prerequisite-gap tracing" and "Mastery-state assignment".

The model reads the work (app/diagnosis/observe.py, prompts/diagnostician/error_hypotheses_v1.md)
and says what it shows: which recorded errors, which signals, which gap descriptions, and whether
a lost point looks procedural or conceptual. Everything after that is deterministic and lives
here, so the shape 03 fixes cannot drift with a prompt:

- Each observed BC-ERR expands through possible_misconceptions into weighted BC-MIS candidates:
  a skill prior (0.5 on the primary skill of a failed point, 0.25 on another of the item's
  skills, 0.1 otherwise), times 2.0 when a matched signal is consistent with the candidate's
  skills, times the confidence factor (1.5 on conceptual candidates after a confident error, 0.5
  after a guess).
- A non-conceptual mass is reserved first: 0.3, 0.5 when a timed attempt meets an error whose
  non_conceptual_causes name time pressure, then halved after a confident error or raised by half
  after a guess, and kept inside [MIN_NON_CONCEPTUAL_MASS, MAX_NON_CONCEPTUAL_MASS]. The
  candidates share what is left, so no misconception is ever returned at probability 1.0
  (test_diagnosis_never_certain), and the remainder is spread over the recorded
  non_conceptual_causes.
- Prerequisite gaps are traced over hard_prerequisite edges only, at most 3 hops, with 03's score:
  0.5 for a matched prerequisite_gap_if description, 0.3 times the probability of a candidate
  naming the parent causally, 0.4 for a matched prerequisite_gap signal consistent with it, all
  times the engine's disbelief in the parent and divided by the depth.
- When the top two hypotheses, misconceptions and gaps together, are within PROBE_MARGIN, the
  leading hypothesis's probe is scheduled: an archetype that exposes the misconception, or one
  that loads the prerequisite, a prerequisite winning a tie because a gap blocks the fringe.
- One mastery_state per loaded skill: a matched signal for that skill first, then 03's rule
  ladder over the point vector. A skill whose points are all still provisional is not_attempted,
  so no engine credit moves on a point the app could not decide.

Every weight here is [inferred] in 03 and belongs to 12 as a tunable.
"""
from dataclasses import dataclass, field

from app.engine.state import MasteryState

PRIMARY_SKILL_PRIOR = 0.5
SECONDARY_SKILL_PRIOR = 0.25
OTHER_PRIOR = 0.1
SIGNAL_MATCH_FACTOR = 2.0
CONFIDENT_CONCEPTUAL_FACTOR = 1.5
GUESS_CONCEPTUAL_FACTOR = 0.5
BASE_NON_CONCEPTUAL_MASS = 0.3
TIMED_NON_CONCEPTUAL_MASS = 0.5
CONFIDENT_NON_CONCEPTUAL_FACTOR = 0.5
GUESS_NON_CONCEPTUAL_FACTOR = 1.5
MIN_NON_CONCEPTUAL_MASS = 0.05
MAX_NON_CONCEPTUAL_MASS = 0.8

GAP_DESCRIPTION_SCORE = 0.5
GAP_CAUSAL_COEFFICIENT = 0.3
GAP_SIGNAL_SCORE = 0.4
MAX_GAP_DEPTH = 3
MAX_GAP_PROBABILITY = 0.95
GAP_STATE_THRESHOLD = 0.2
PROBE_MARGIN = 0.2

MISCONCEPTION = "misconception"
PREREQUISITE = "prerequisite"

PROCEDURAL = "procedural"
CONCEPTUAL = "conceptual"


@dataclass
class Observation:
   """What the model read off the work, already checked against the candidate lists."""

   error_ids: list = field(default_factory=list)
   new_behaviors: list = field(default_factory=list)
   signal_ids: list = field(default_factory=list)
   skill_readings: dict = field(default_factory=dict)
   gap_skills: list = field(default_factory=list)
   evidence: dict = field(default_factory=dict)
   points_lost_by_error: dict = field(default_factory=dict)


@dataclass
class Library:
   skills: dict
   prerequisites: dict
   errors: dict
   misconceptions: dict
   signals: dict
   archetypes: dict
   hard_parents: dict


def failed_points(record, decisions):
   points = {point["point_id"]: point for part in record["parts"] for point in part["points"]}

   return [points[decision.point_id] for decision in decisions if decision.earned == 0]


def failed_skill_roles(record, decisions):
   primary = set()
   touched = set()

   for point in failed_points(record, decisions):
      skills = point.get("skills") or []

      if skills:
         primary.add(skills[0])

      touched.update(skills)

   return primary, touched


def non_conceptual_mass(observed_errors, errors, confidence, timed):
   mentions_time = any(
      "time" in cause.lower()
      for error_id in observed_errors
      for cause in errors[error_id].get("non_conceptual_causes") or []
   )
   mass = TIMED_NON_CONCEPTUAL_MASS if (timed and mentions_time) else BASE_NON_CONCEPTUAL_MASS

   if confidence == "confident":
      mass *= CONFIDENT_NON_CONCEPTUAL_FACTOR

   if confidence == "guess":
      mass *= GUESS_NON_CONCEPTUAL_FACTOR

   return min(MAX_NON_CONCEPTUAL_MASS, max(MIN_NON_CONCEPTUAL_MASS, mass))


def skill_prior(misconception_id, primary_skills, item_skills, skills):
   def lists(skill_id):
      return misconception_id in (skills.get(skill_id, {}).get("misconceptions") or [])

   if any(lists(skill_id) for skill_id in primary_skills):
      return PRIMARY_SKILL_PRIOR, "skill_prior"

   if any(lists(skill_id) for skill_id in item_skills):
      return SECONDARY_SKILL_PRIOR, "skill_prior"

   return OTHER_PRIOR, "error_link"


def signal_supports(misconception, signal_ids, signals):
   linked_skills = set(misconception.get("skills") or [])

   for signal_id in signal_ids:
      consistent = set(signals[signal_id].get("consistent_with") or [])
      supports = misconception["id"] in consistent or bool(linked_skills & consistent)

      if supports:
         return signal_id

   return None


def misconception_candidates(observation, library, primary_skills, item_skills, confidence):
   weights = {}
   bases = {}
   signal_of = {}

   for error_id in observation.error_ids:
      for misconception_id in library.errors[error_id].get("possible_misconceptions") or []:
         misconception = library.misconceptions.get(misconception_id)
         is_active = misconception is not None

         if not is_active:
            continue

         weight, basis = skill_prior(misconception_id, primary_skills, item_skills, library.skills)
         basis_list = [basis, "error_link"] if basis != "error_link" else ["error_link"]
         supporting_signal = signal_supports(misconception, observation.signal_ids, library.signals)

         if supporting_signal is not None:
            weight *= SIGNAL_MATCH_FACTOR
            basis_list.append("signal_match")
            signal_of[misconception_id] = supporting_signal

         if confidence == "confident":
            weight *= CONFIDENT_CONCEPTUAL_FACTOR
            basis_list.append("confidence_rating")

         if confidence == "guess":
            weight *= GUESS_CONCEPTUAL_FACTOR
            basis_list.append("confidence_rating")

         is_stronger = weight > weights.get(misconception_id, 0.0)

         if is_stronger:
            weights[misconception_id] = weight
            bases[misconception_id] = sorted(set(basis_list))

   return weights, bases, signal_of


def normalised(weights, share):
   total = sum(weights.values())
   has_weight = total > 0

   if not has_weight:
      return {}

   return {key: share * weight / total for key, weight in weights.items()}


def rival_pairs(candidates, misconceptions):
   live = set(candidates)

   return {
      misconception_id: sorted(set(misconceptions[misconception_id].get("rival_misconceptions") or []) & live)
      for misconception_id in candidates
   }


def parent_strength(parent_id, strengths):
   """sigma(m_p) from the engine, 1.0 for a parent the engine has no row for, which a BC-PRQ
   seeded mastered also reads as until a gap is diagnosed."""
   return strengths.get(parent_id, 1.0)


def trace_gaps(failed_skills, observation, probabilities, library, strengths):
   frontier = set(failed_skills)
   gaps = {}
   depth = 0

   while frontier and depth < MAX_GAP_DEPTH:
      depth += 1
      parents = set()

      for child in frontier:
         for parent in library.hard_parents.get(child, ()):
            parents.add(parent)
            score = 0.0
            basis = []
            description_matched = child in observation.gap_skills

            if description_matched:
               score += GAP_DESCRIPTION_SCORE
               basis.append("prerequisite_gap_if")

            for misconception_id, probability in probabilities.items():
               causal = library.misconceptions[misconception_id].get("causal_prerequisites") or []

               if parent in causal:
                  score += GAP_CAUSAL_COEFFICIENT * probability
                  basis.append("causal_prerequisites")

            for signal_id in observation.signal_ids:
               signal = library.signals[signal_id]
               is_gap_signal = signal.get("mastery_state") == MasteryState.PREREQUISITE_GAP.value
               names_parent = parent in (signal.get("consistent_with") or [])

               if is_gap_signal and names_parent:
                  score += GAP_SIGNAL_SCORE
                  basis.append("signal_prerequisite_gap")

            has_evidence = score > 0

            if not has_evidence:
               continue

            score *= 1 - parent_strength(parent, strengths)
            basis.append("engine_state")
            probability = min(MAX_GAP_PROBABILITY, score / depth)
            is_better = probability > gaps.get(parent, {}).get("probability", 0.0)

            if is_better and probability > 0:
               gaps[parent] = {
                  "prerequisite_id": parent,
                  "depth": depth,
                  "probability": round(probability, 4),
                  "basis": sorted(set(basis)),
                  "blocks_skill": child,
               }

      frontier = parents

   return sorted(gaps.values(), key=lambda gap: (-gap["probability"], gap["depth"], gap["prerequisite_id"]))


def archetype_loading(skill_id, archetypes):
   for archetype_id in sorted(archetypes):
      if skill_id in (archetypes[archetype_id].get("skills") or []):
         return archetype_id

   return None


def ranked_hypotheses(misconceptions, gaps):
   hypotheses = [
      {"kind": MISCONCEPTION, "id": entry["misconception_id"], "probability": entry["probability"]}
      for entry in misconceptions
   ]
   hypotheses.extend(
      {"kind": PREREQUISITE, "id": gap["prerequisite_id"], "probability": gap["probability"]}
      for gap in gaps
   )
   prefer_prerequisite = {PREREQUISITE: 0, MISCONCEPTION: 1}

   return sorted(hypotheses, key=lambda entry: (-entry["probability"], prefer_prerequisite[entry["kind"]], entry["id"]))


def recommended_probe(hypotheses, library, rivals):
   has_two = len(hypotheses) >= 2

   if not has_two:
      return None

   leader, runner_up = hypotheses[0], hypotheses[1]
   is_close = leader["probability"] - runner_up["probability"] <= PROBE_MARGIN

   if not is_close:
      return None

   separates = [leader["id"], runner_up["id"]]

   if leader["kind"] == PREREQUISITE:
      archetype_id = archetype_loading(leader["id"], library.archetypes)
      probe_text = None
      reason = "prerequisite_ambiguous"
   else:
      misconception = library.misconceptions[leader["id"]]
      exposing = [archetype_id for archetype_id in misconception.get("exposing_archetypes") or [] if archetype_id in library.archetypes]
      archetype_id = exposing[0] if exposing else None
      probe_text = misconception.get("discriminating_probe")
      is_rival_pair = runner_up["id"] in rivals.get(leader["id"], [])
      reason = "rival_pair" if is_rival_pair else "top_two_within_0.2"

   if archetype_id is None:
      return None

   return {"archetype_id": archetype_id, "reason": reason, "separates": separates, "probe_text": probe_text}


def points_by_skill(record, decisions):
   points = {point["point_id"]: point for part in record["parts"] for point in part["points"]}
   grouped = {}

   for decision in decisions:
      for skill_id in points[decision.point_id].get("skills") or []:
         grouped.setdefault(skill_id, []).append(decision)

   return grouped


def rule_state(skill_id, decisions, observation, gap_blocked, part_has_work):
   decided = [decision for decision in decisions if decision.earned is not None]
   has_decided = len(decided) > 0

   if not has_decided:
      return MasteryState.NOT_ATTEMPTED

   lost = [decision for decision in decided if decision.earned == 0]
   earned = [decision for decision in decided if decision.earned == 1]
   wrote_nothing = not any(part_has_work.get(decision.part_id, False) for decision in decided)

   if wrote_nothing:
      return MasteryState.NOT_ATTEMPTED

   if not lost:
      return MasteryState.MASTERED

   if skill_id in gap_blocked:
      return MasteryState.PREREQUISITE_GAP

   lost_on_notation_only = all(decision.rule_field == "notation_requirements" for decision in lost)

   if lost_on_notation_only:
      return MasteryState.NOTATION_ONLY

   if not earned:
      return MasteryState.NOT_MASTERED

   reading = observation.skill_readings.get(skill_id)

   if reading == PROCEDURAL:
      return MasteryState.PARTIAL_PROCEDURAL

   if reading == CONCEPTUAL:
      return MasteryState.PARTIAL_CONCEPTUAL

   return MasteryState.PARTIAL_UNSPECIFIED


def mastery_states(record, decisions, observation, library, gaps, part_has_work):
   grouped = points_by_skill(record, decisions)
   gap_blocked = {gap["blocks_skill"] for gap in gaps if gap["probability"] >= GAP_STATE_THRESHOLD}
   signal_for_skill = {library.signals[signal_id].get("skill"): signal_id for signal_id in observation.signal_ids}
   states = []

   for skill_id in record["skills"]:
      skill_decisions = grouped.get(skill_id, [])
      ruled = rule_state(skill_id, skill_decisions, observation, gap_blocked, part_has_work)
      signal_id = signal_for_skill.get(skill_id)
      has_signal = signal_id is not None and ruled != MasteryState.NOT_ATTEMPTED

      considered = [decision.point_id for decision in skill_decisions]

      if has_signal:
         state = MasteryState(library.signals[signal_id]["mastery_state"])
         states.append({
            "skill_id": skill_id,
            "mastery_state": state.value,
            "signal_id": signal_id,
            "assigned_by": "signal",
            "points_considered": considered,
         })
         continue

      states.append({
         "skill_id": skill_id,
         "mastery_state": ruled.value,
         "assigned_by": "rule",
         "points_considered": considered,
      })

   return states


def diagnose(record, decisions, observation, library, confidence=None, timed=False, strengths=None, part_has_work=None):
   strengths = strengths or {}
   part_has_work = part_has_work or {}
   primary_skills, touched_skills = failed_skill_roles(record, decisions)
   weights, bases, signal_of = misconception_candidates(
      observation, library, primary_skills, set(record["skills"]), confidence
   )
   mass = non_conceptual_mass(observation.error_ids, library.errors, confidence, timed)
   has_candidates = len(weights) > 0
   probabilities = normalised(weights, 1 - mass) if has_candidates else {}
   rivals = rival_pairs(probabilities, library.misconceptions)
   misconceptions = [
      {
         "misconception_id": misconception_id,
         "probability": round(probability, 4),
         "rival_of": rivals[misconception_id],
         "basis": bases[misconception_id],
         "signal_id": signal_of.get(misconception_id),
         "severity": library.misconceptions[misconception_id].get("severity", "unknown"),
         "evidence_tag": "inferred",
      }
      for misconception_id, probability in sorted(probabilities.items(), key=lambda entry: (-entry[1], entry[0]))
   ]
   causes = sorted({
      cause
      for error_id in observation.error_ids
      for cause in library.errors[error_id].get("non_conceptual_causes") or []
   })
   cause_mass = mass if has_candidates else 1.0
   non_conceptual = [
      {"cause": cause, "probability": round(cause_mass / len(causes), 4)} for cause in causes
   ] if causes else []
   gaps = trace_gaps(touched_skills, observation, probabilities, library, strengths)
   hypotheses = ranked_hypotheses(misconceptions, gaps)
   probe = recommended_probe(hypotheses, library, rivals)
   observed = [
      {
         "error_id": error_id,
         "matched": True,
         "evidence": observation.evidence.get(error_id, ""),
         "points_lost": observation.points_lost_by_error.get(error_id, []),
      }
      for error_id in observation.error_ids
   ]
   observed.extend(
      {
         "matched": False,
         "evidence": behavior.get("evidence", ""),
         "points_lost": behavior.get("points_lost", []),
         "candidate": {
            "observed_behavior": behavior["observed_behavior"],
            "skills": sorted(touched_skills),
            "archetypes": [record["archetype_id"]],
            "evidence_tag": "inferred",
         },
      }
      for behavior in observation.new_behaviors
   )

   return {
      "archetype_id": record["archetype_id"],
      "observed_errors": observed,
      "candidate_misconceptions": misconceptions,
      "non_conceptual_mass": round(mass, 4),
      "non_conceptual_causes": non_conceptual,
      "prerequisite_gaps": gaps,
      "hypotheses": hypotheses,
      "per_skill_mastery_state": mastery_states(record, decisions, observation, library, gaps, part_has_work),
      "recommended_probe": probe,
   }


def hypothesis_count(diagnosis):
   return len(diagnosis.get("hypotheses") or [])

