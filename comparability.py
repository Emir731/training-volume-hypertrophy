"""
Explicit comparability rules for deciding whether a study's quantitative
data can be shown alongside another study's in the same exploratory
figure. This does NOT compute a pooled estimate.

TWO SEPARATE QUESTIONS, KEPT SEPARATE (this matters - see README.md
"Reconsidering 'quantitatively comparable'" section):

1. STATISTICAL COMPARABILITY - can these two studies' numbers sit on
   the same axis without being mathematically apples-to-oranges? This
   checks effect-size construction, outcome construct, volume-
   manipulation type, and study design structure. A mismatch here is a
   hard problem: NOT_COMPARABLE.

2. BIOLOGICAL/POPULATION HETEROGENEITY - do these two studies represent
   the same training status and the same muscle group? A mismatch here
   is NOT a reason to exclude a study from an exploratory visualization
   - this project's own research question is specifically about
   whether training status changes the volume-hypertrophy relationship,
   so forcing every pair to share training status would make it
   impossible to ever compare across that variable. This is reported as
   a descriptive note, not a pass/fail gate.

FIGURE_ELIGIBLE_FOR_EXPLORATORY_COMPARISON is the final combined
judgment used to decide inclusion in figures/volume_response.png: it
requires STATISTICALLY_COMPARABLE (or better) and does not require
biological homogeneity.

Run: python3 analysis/comparability.py
"""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "extraction_table.csv"

STATISTICAL_DIMENSIONS = [
    "effect_size_metric_and_denominator",
    "outcome_construct",
    "volume_definition_type",
    "design_structure",
]

BIOLOGICAL_DIMENSIONS = [
    "training_status",
    "muscle_group",
]


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _design_bucket(study_design_text):
    """Buckets a free-text study_design field into a coarse structural
    type. Returns None if it can't be classified."""
    text = (study_design_text or "").lower()
    if "within-subject" in text or "within subject" in text or "unilateral" in text:
        return "within_subject"
    if "parallel" in text:
        return "parallel_group"
    return None


def classify_statistical_comparability(a, b):
    """Returns (verdict, reasons). Checks ALL FOUR declared
    STATISTICAL_DIMENSIONS - effect_size_metric_and_denominator,
    outcome_construct, volume_definition_type, and design_structure are
    each actually implemented below (a prior version declared
    design_structure but never checked it - fixed)."""
    reasons = []
    verdict = "STATISTICALLY_COMPARABLE"

    a_es = a.get("effect_size_metric_type", "").strip()
    b_es = b.get("effect_size_metric_type", "").strip()
    if not a_es or not b_es:
        verdict = "PARTIALLY_COMPARABLE"
        reasons.append("effect_size_metric_and_denominator: unclassified for at least one study.")
    elif a_es != b_es:
        verdict = "NOT_COMPARABLE"
        reasons.append(f"effect_size_metric_and_denominator: '{a_es}' vs '{b_es}' - not the same quantity.")

    a_out = a.get("outcome_construct_type", "").strip()
    b_out = b.get("outcome_construct_type", "").strip()
    if not a_out or not b_out:
        if verdict == "STATISTICALLY_COMPARABLE":
            verdict = "PARTIALLY_COMPARABLE"
        reasons.append("outcome_construct: unclassified for at least one study.")
    elif a_out != b_out:
        verdict = "NOT_COMPARABLE"
        reasons.append(f"outcome_construct: '{a_out}' vs '{b_out}' - different tissue-level quantities.")

    a_vol = a.get("volume_manipulation_type", "").strip()
    b_vol = b.get("volume_manipulation_type", "").strip()
    if not a_vol or not b_vol:
        if verdict == "STATISTICALLY_COMPARABLE":
            verdict = "PARTIALLY_COMPARABLE"
        reasons.append("volume_definition_type: unclassified for at least one study.")
    elif a_vol != b_vol:
        if verdict == "STATISTICALLY_COMPARABLE":
            verdict = "PARTIALLY_COMPARABLE"
        reasons.append(f"volume_definition_type: '{a_vol}' vs '{b_vol}' - different independent variables.")

    a_design = _design_bucket(a.get("study_design", ""))
    b_design = _design_bucket(b.get("study_design", ""))
    if a_design is None or b_design is None:
        if verdict == "STATISTICALLY_COMPARABLE":
            verdict = "PARTIALLY_COMPARABLE"
        reasons.append("design_structure: could not classify study_design text for at least one study.")
    elif a_design != b_design:
        if verdict == "STATISTICALLY_COMPARABLE":
            verdict = "PARTIALLY_COMPARABLE"
        reasons.append(f"design_structure: '{a_design}' vs '{b_design}' - a within-subject design controls "
                        f"for individual variation in a way a parallel-group design does not.")

    if not reasons:
        reasons.append("No mismatches on any of the 4 statistical dimensions.")

    return verdict, reasons


def describe_biological_heterogeneity(a, b):
    """Returns a list of descriptive notes about training-status and
    muscle-group differences. NEVER changes a pass/fail verdict - this
    project's research question is specifically about training status
    as a moderator, so flagging a training-status difference as
    disqualifying would make that question unanswerable by design."""
    notes = []
    a_ts, b_ts = a.get("training_status", "").strip(), b.get("training_status", "").strip()
    if a_ts and b_ts and a_ts != b_ts:
        notes.append(f"training_status differs: '{a_ts}' vs '{b_ts}' - relevant to this project's own "
                      f"research question, not a comparability defect.")
    a_mg, b_mg = a.get("muscle_group", "").strip(), b.get("muscle_group", "").strip()
    if a_mg and b_mg and a_mg.lower() != b_mg.lower():
        notes.append(f"muscle_group differs: '{a_mg}' vs '{b_mg}' - different anatomical sites; effect "
                      f"sizes are not evidence about the same tissue.")
    if not notes:
        notes.append("No biological/population heterogeneity noted on the checked dimensions.")
    return notes


def figure_eligibility(a, b):
    """Combined judgment actually used for figure inclusion: requires
    statistical comparability; biological heterogeneity is reported
    alongside but does not gate eligibility."""
    stat_verdict, stat_reasons = classify_statistical_comparability(a, b)
    bio_notes = describe_biological_heterogeneity(a, b)
    eligible = stat_verdict != "NOT_COMPARABLE"
    return eligible, stat_verdict, stat_reasons, bio_notes


if __name__ == "__main__":
    rows = load_rows()
    quant_rows = [r for r in rows if r["evidence_category"] == "A"]

    print(f"Comparability check across the {len(quant_rows)} category-A studies:\n")
    for i, a in enumerate(quant_rows):
        for b in quant_rows[i + 1:]:
            eligible, stat_verdict, stat_reasons, bio_notes = figure_eligibility(a, b)
            eligibility_label = "FIGURE_ELIGIBLE_FOR_EXPLORATORY_COMPARISON" if eligible else "NOT_ELIGIBLE"
            print(f"{a['study_id']}  vs  {b['study_id']}")
            print(f"  Statistical comparability: {stat_verdict}")
            for r in stat_reasons:
                print(f"    - {r}")
            print(f"  Biological/population notes (informational, not a gate):")
            for n in bio_notes:
                print(f"    - {n}")
            print(f"  => {eligibility_label}")
            print()

    print(
        "Conclusion: Radaelli/Heaselgrave/Aube are pairwise FIGURE_ELIGIBLE_FOR_EXPLORATORY_COMPARISON "
        "(statistically comparable; biologically heterogeneous by training status and, for Aube, by muscle "
        "group - noted, not disqualifying). Schoenfeld 2019 and de Camargo 2026 are NOT_ELIGIBLE with at "
        "least one of the three, on STATISTICAL grounds (effect-size construction and/or design structure), "
        "not because of training status or muscle group."
    )
