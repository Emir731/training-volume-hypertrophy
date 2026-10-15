"""
Basic tests for this repository's calculations and validation logic.
Deliberately simple - readable assertions, not a test framework.

Run: python3 analysis/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import validate_data
import comparability
import verify_schoenfeld_es


def test_schoenfeld_es_formula_matches_reported():
    """The 'average baseline SD' hypothesis should reproduce the
    authors' reported triceps ES to within 0.01."""
    avg_sd = sum(verify_schoenfeld_es.triceps_baseline_sd.values()) / 3
    for g in ["1SET", "3SET", "5SET"]:
        calc = verify_schoenfeld_es.triceps_delta_mean[g] / avg_sd
        reported = verify_schoenfeld_es.reported_ES[g]
        assert abs(calc - reported) < 0.01, f"{g}: calc={calc:.3f} vs reported={reported} - formula hypothesis broke"
    print("PASS: test_schoenfeld_es_formula_matches_reported")


def test_schoenfeld_change_score_sd_does_not_match():
    """The change-score-SD convention (used for Radaelli/Heaselgrave/Aube)
    should NOT match Schoenfeld's reported ES - this is the whole point
    of why Schoenfeld 2019 is excluded from the comparable figure."""
    for g in ["1SET", "3SET", "5SET"]:
        calc = verify_schoenfeld_es.triceps_delta_mean[g] / verify_schoenfeld_es.triceps_delta_sd[g]
        reported = verify_schoenfeld_es.reported_ES[g]
        assert abs(calc - reported) > 0.1, f"{g}: change-score-SD method unexpectedly matched reported ES - re-check the exclusion rationale"
    print("PASS: test_schoenfeld_change_score_sd_does_not_match")


def test_no_duplicate_study_ids():
    rows = validate_data.load_rows()
    warnings = validate_data.check_duplicate_ids(rows)
    assert warnings == [], f"Found duplicate study_ids: {warnings}"
    print("PASS: test_no_duplicate_study_ids")


def test_no_pseudoreplication():
    rows = validate_data.load_rows()
    warnings = validate_data.check_pseudoreplication(rows)
    assert warnings == [], f"Found pseudoreplication risk: {warnings}"
    print("PASS: test_no_pseudoreplication")


def test_retracted_studies_excluded_from_synthesis():
    rows = validate_data.load_rows()
    warnings = validate_data.check_retracted_or_disputed_not_used(rows, validate_data.SYNTHESIS_STUDY_IDS)
    assert warnings == [], f"Retracted/disputed study found in synthesis: {warnings}"
    print("PASS: test_retracted_studies_excluded_from_synthesis")


def test_synthesis_studies_are_pairwise_comparable():
    """The 3 studies actually in the figure should be
    STATISTICALLY_COMPARABLE with each other under
    analysis/comparability.py's rules (biological heterogeneity between
    them is expected and does not affect this check)."""
    rows = comparability.load_rows()
    by_id = {r["study_id"]: r for r in rows}
    ids = validate_data.SYNTHESIS_STUDY_IDS
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            verdict, reasons = comparability.classify_statistical_comparability(by_id[ids[i]], by_id[ids[j]])
            assert verdict == "STATISTICALLY_COMPARABLE", f"{ids[i]} vs {ids[j]} should be STATISTICALLY_COMPARABLE but got {verdict}: {reasons}"
    print("PASS: test_synthesis_studies_are_pairwise_comparable")


def test_excluded_studies_are_not_comparable_to_at_least_one_synthesis_study():
    """Schoenfeld 2019 and de Camargo 2026 should each fail statistical
    comparability with at least one of the 3 synthesis studies."""
    rows = comparability.load_rows()
    by_id = {r["study_id"]: r for r in rows}
    excluded = ["P04_Schoenfeld2019", "P08_deCamargo2026"]
    for ex_id in excluded:
        found_mismatch = False
        for syn_id in validate_data.SYNTHESIS_STUDY_IDS:
            verdict, _ = comparability.classify_statistical_comparability(by_id[ex_id], by_id[syn_id])
            if verdict != "STATISTICALLY_COMPARABLE":
                found_mismatch = True
        assert found_mismatch, f"{ex_id} was STATISTICALLY_COMPARABLE with all synthesis studies - exclusion rationale may be stale"
    print("PASS: test_excluded_studies_are_not_comparable_to_at_least_one_synthesis_study")


def test_all_declared_comparability_dimensions_are_implemented():
    """Every dimension in comparability.STATISTICAL_DIMENSIONS must
    actually appear in classify_statistical_comparability's output
    reasons for at least one real pair in the dataset - catches the
    exact bug found this round (design_structure was declared but
    never checked)."""
    rows = comparability.load_rows()
    quant_rows = [r for r in rows if r["evidence_category"] == "A"]
    seen_dimension_prefixes = set()
    for i, a in enumerate(quant_rows):
        for b in quant_rows[i + 1:]:
            _, reasons = comparability.classify_statistical_comparability(a, b)
            for r in reasons:
                for dim in comparability.STATISTICAL_DIMENSIONS:
                    if r.startswith(dim):
                        seen_dimension_prefixes.add(dim)
    missing = set(comparability.STATISTICAL_DIMENSIONS) - seen_dimension_prefixes
    assert not missing, f"Declared dimensions never appeared in any reason string: {missing}"
    print("PASS: test_all_declared_comparability_dimensions_are_implemented")


def test_synthesis_arms_effect_sizes_are_author_reported():
    """Every arm plotted in the figure must have
    effect_size_provenance=='author_reported' - the figure must never
    silently plot an independently-calculated value as if it were the
    author's own number."""
    import csv
    arms_path = Path(__file__).resolve().parent.parent / "data" / "synthesis_arms.csv"
    with open(arms_path, newline="", encoding="utf-8") as f:
        arms = list(csv.DictReader(f))
    for arm in arms:
        assert arm["effect_size_provenance"] == "author_reported", \
            f"{arm['comparison_id']} has effect_size_provenance='{arm['effect_size_provenance']}', not 'author_reported'"
    print("PASS: test_synthesis_arms_effect_sizes_are_author_reported")


def test_schoenfeld_inferred_es_kept_separate_from_reported():
    """The Schoenfeld 2019 row must keep reported_effect_size and
    independently_calculated_effect_size in separate fields, and the
    effect_size_metric_type must carry the _INFERRED suffix."""
    rows = validate_data.load_rows()
    by_id = {r["study_id"]: r for r in rows}
    row = by_id["P04_Schoenfeld2019"]
    assert row["reported_effect_size"], "reported_effect_size should not be empty for Schoenfeld 2019"
    assert row["independently_calculated_effect_size"], "independently_calculated_effect_size should not be empty for Schoenfeld 2019"
    assert row["reported_effect_size"] != row["independently_calculated_effect_size"], \
        "reported and independently-calculated ES fields should not be identical text - they document different things"
    assert "INFERRED" in row["effect_size_metric_type"], \
        "Schoenfeld 2019's effect_size_metric_type should be marked INFERRED, not stated as an established fact"
    print("PASS: test_schoenfeld_inferred_es_kept_separate_from_reported")


def test_canonical_counts_match_synthesis_script():
    warnings = validate_data.check_canonical_counts_consistency(validate_data.load_rows())
    assert warnings == [], f"Canonical count mismatch: {warnings}"
    print("PASS: test_canonical_counts_match_synthesis_script")


def test_synthesis_arms_csv_matches_extraction_table():
    """Every study_id in data/synthesis_arms.csv must be category A and
    COMPARABLE in extraction_table.csv - this is the same check
    synthesis.py itself does at runtime, duplicated here as a fast test."""
    import csv
    arms_path = Path(__file__).resolve().parent.parent / "data" / "synthesis_arms.csv"
    with open(arms_path, newline="", encoding="utf-8") as f:
        arms = list(csv.DictReader(f))
    rows = validate_data.load_rows()
    by_id = {r["study_id"]: r for r in rows}
    for arm in arms:
        sid = arm["study_id"]
        assert sid in by_id, f"{sid} in synthesis_arms.csv but not in extraction_table.csv"
        assert by_id[sid]["evidence_category"] == "A", f"{sid} in synthesis_arms.csv but not evidence_category A"
        assert by_id[sid]["comparability_to_figure"] == "COMPARABLE", f"{sid} in synthesis_arms.csv but not COMPARABLE"
    print("PASS: test_synthesis_arms_csv_matches_extraction_table")


def test_no_hardcoded_study_ids_in_comparability_rules():
    """classify_statistical_comparability should work purely from
    controlled-vocabulary fields, proven using fabricated study_ids."""
    fake_a = {"study_id": "ZZZ_FakeStudyA", "effect_size_metric_type": "within_group_pre_post_d",
              "outcome_construct_type": "muscle_thickness_imaging", "volume_manipulation_type": "absolute_weekly_sets",
              "study_design": "Parallel-group RCT"}
    fake_b = {"study_id": "ZZZ_FakeStudyB", "effect_size_metric_type": "within_group_pre_post_d",
              "outcome_construct_type": "muscle_thickness_imaging", "volume_manipulation_type": "absolute_weekly_sets",
              "study_design": "Parallel-group RCT"}
    verdict, _ = comparability.classify_statistical_comparability(fake_a, fake_b)
    assert verdict == "STATISTICALLY_COMPARABLE", f"Two fabricated studies with matching fields should be STATISTICALLY_COMPARABLE, got {verdict}"
    print("PASS: test_no_hardcoded_study_ids_in_comparability_rules")


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failures = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failures += 1
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed")
    sys.exit(1 if failures else 0)
