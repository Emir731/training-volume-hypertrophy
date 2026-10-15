"""
Validates data/extraction_table.csv for structural, logical, and
pseudoreplication issues. Run: python3 analysis/validate_data.py

Mechanical checks only - does not verify that underlying facts are true.
"""

import csv
import sys
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "extraction_table.csv"

REQUIRED_FIELDS = [
    "study_id", "citation", "year", "study_design", "participant_n",
    "training_status", "training_status_criteria", "primary_source_verified",
    "extraction_status", "evidence_category",
]

VALID_VERIFICATION_STATUSES = {
    "PRIMARY_FULL_TEXT_VERIFIED",
    "PRIMARY_FULL_TEXT_VERIFIED_BUT_PREPRINT",
    "PRIMARY_ABSTRACT_ONLY",
    "SECONDARY_SOURCE_ONLY",
    "UNRESOLVED",
    "AGGREGATE_BENCHMARK_NOT_A_PRIMARY_DATAPOINT",
    "DATA-INTEGRITY CONCERN / CRITICAL COMMENTARY",
    "RETRACTED",
}

# Canonical A-I evidence taxonomy (see data/DATA_DICTIONARY.md)
VALID_EVIDENCE_CATEGORIES = {"A", "B", "C", "D", "E", "F", "G", "H", "I"}

VALID_TRAINING_STATUS = {
    "untrained", "recreationally active", "resistance-trained",
    "highly resistance-trained", "unclear", "mixed (aggregate)",
}

VALID_COMPARABILITY = None  # free-text with controlled prefixes - checked via startswith below

# Study IDs currently hardcoded into synthesis.py's quantitative figure.
SYNTHESIS_STUDY_IDS = ["P01_Radaelli2015", "P02_Heaselgrave2019", "P03_Aube2022"]


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_missing_fields(rows):
    return [f"[{r.get('study_id', '?')}] missing/empty field: {field}"
            for r in rows for field in REQUIRED_FIELDS if not r.get(field, "").strip()]


def check_duplicate_ids(rows):
    ids = [r["study_id"] for r in rows]
    seen, dupes = set(), set()
    for i in ids:
        (dupes.add(i) if i in seen else seen.add(i))
    return [f"duplicate study_id: {d}" for d in dupes]


def check_verification_status_values(rows):
    return [f"[{r['study_id']}] unrecognized primary_source_verified value: '{r.get('primary_source_verified','').strip()}'"
            for r in rows if r.get("primary_source_verified", "").strip() not in VALID_VERIFICATION_STATUSES]


def check_evidence_categories(rows):
    return [f"[{r['study_id']}] unrecognized evidence_category: '{r.get('evidence_category','').strip()}'"
            for r in rows if r.get("evidence_category", "").strip() not in VALID_EVIDENCE_CATEGORIES]


def check_training_status_labels(rows):
    warnings = []
    for row in rows:
        val = row.get("training_status", "").strip()
        if val and val not in VALID_TRAINING_STATUS:
            warnings.append(f"[{row['study_id']}] training_status '{val}' is not a standardized category")
    return warnings


def check_unverified_used_in_synthesis(rows, synthesis_ids):
    by_id = {r["study_id"]: r for r in rows}
    warnings = []
    for sid in synthesis_ids:
        row = by_id.get(sid)
        if row is None:
            warnings.append(f"synthesis.py references '{sid}' which is not in the extraction table")
            continue
        if row.get("evidence_category", "").strip() != "A":
            warnings.append(f"[{sid}] is used in the synthesis figure but evidence_category is "
                             f"'{row.get('evidence_category')}', not 'A'")
        if row.get("comparability_to_figure", "").strip() != "COMPARABLE":
            warnings.append(f"[{sid}] is used in the synthesis figure but comparability_to_figure is "
                             f"'{row.get('comparability_to_figure')}', not 'COMPARABLE'")
    return warnings


def check_retracted_or_disputed_not_used(rows, synthesis_ids):
    by_id = {r["study_id"]: r for r in rows}
    warnings = []
    for sid in synthesis_ids:
        row = by_id.get(sid)
        if row and row.get("evidence_category", "").strip() in ("E", "F"):
            warnings.append(f"[{sid}] has evidence_category '{row['evidence_category']}' (retracted/integrity "
                             f"concern) but appears in the synthesis - must be removed immediately")
    return warnings


def check_pseudoreplication(rows):
    """Every row with quantitative data must have a sample_id. If the
    same sample_id appears in the synthesis figure's study list more
    than once under different study_ids, that IS pseudoreplication."""
    warnings = []
    quant_categories = {"A"}
    sample_to_studies = {}
    for r in rows:
        if r.get("evidence_category", "").strip() in quant_categories:
            sid = r.get("sample_id", "").strip()
            if not sid:
                warnings.append(f"[{r['study_id']}] has evidence_category A (quantitative) but no sample_id assigned")
            else:
                sample_to_studies.setdefault(sid, []).append(r["study_id"])
    for sample, studies in sample_to_studies.items():
        if len(studies) > 1:
            warnings.append(f"PSEUDOREPLICATION RISK: sample_id '{sample}' is claimed by multiple study_ids: {studies}")
    return warnings


def check_impossible_values(rows):
    warnings = []
    for row in rows:
        n = row.get("participant_n", "")
        if n.strip().isdigit() and int(n.strip()) <= 0:
            warnings.append(f"[{row['study_id']}] non-positive participant_n: {n}")
    return warnings


def check_canonical_counts_consistency(rows):
    """Cross-check that the number of rows actually flowing into the
    synthesis figure (per this CSV) matches what synthesis.py itself
    hardcodes - catches silent drift if one is updated without the other."""
    warnings = []
    csv_comparable = {r["study_id"] for r in rows if r.get("comparability_to_figure", "").strip() == "COMPARABLE"}
    script_ids = set(SYNTHESIS_STUDY_IDS)
    if csv_comparable != script_ids:
        warnings.append(
            f"MISMATCH between CSV comparability_to_figure=='COMPARABLE' rows {sorted(csv_comparable)} "
            f"and validate_data.py's SYNTHESIS_STUDY_IDS list {sorted(script_ids)} - "
            f"update whichever is stale."
        )
    return warnings


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found")
        sys.exit(1)

    rows = load_rows()
    print(f"Loaded {len(rows)} rows from {CSV_PATH.name}\n")

    all_warnings = []
    all_warnings += check_missing_fields(rows)
    all_warnings += check_duplicate_ids(rows)
    all_warnings += check_verification_status_values(rows)
    all_warnings += check_evidence_categories(rows)
    all_warnings += check_training_status_labels(rows)
    all_warnings += check_unverified_used_in_synthesis(rows, SYNTHESIS_STUDY_IDS)
    all_warnings += check_retracted_or_disputed_not_used(rows, SYNTHESIS_STUDY_IDS)
    all_warnings += check_pseudoreplication(rows)
    all_warnings += check_impossible_values(rows)
    all_warnings += check_canonical_counts_consistency(rows)

    if not all_warnings:
        print("No issues found.")
    else:
        print(f"{len(all_warnings)} issue(s) found:\n")
        for w in all_warnings:
            print(f"  - {w}")

    print("\nSummary counts by evidence_category:")
    counts = {}
    for row in rows:
        c = row.get("evidence_category", "UNKNOWN")
        counts[c] = counts.get(c, 0) + 1
    for cat, count in sorted(counts.items()):
        print(f"  {cat}: {count}")

    return len(all_warnings)


if __name__ == "__main__":
    n_issues = main()
    sys.exit(1 if n_issues > 0 else 0)
