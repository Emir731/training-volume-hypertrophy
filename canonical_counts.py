"""
Computes the canonical counts for this project from data/extraction_table.csv
directly. README.md, manuscript.md, EVIDENCE_MAP.md, and QUALITY_CONTROL.md
should all match these numbers - if they don't, one of them is stale.

Run: python3 analysis/canonical_counts.py
"""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "extraction_table.csv"


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute(rows):
    counts = {}
    counts["total_sources"] = len(rows)
    counts["by_category"] = {}
    for r in rows:
        counts["by_category"].setdefault(r["evidence_category"], []).append(r["study_id"])

    counts["primary_studies"] = [r["study_id"] for r in rows if r["evidence_category"] in ("A", "B", "C", "D")]
    counts["independent_samples"] = sorted(set(r["sample_id"] for r in rows if r["sample_id"]))
    counts["fulltext_verified_primary"] = [r["study_id"] for r in rows if r["evidence_category"] == "A"]
    counts["fulltext_verified_reviews"] = [r["study_id"] for r in rows if r["evidence_category"] == "G" and "FULL_TEXT" in r["primary_source_verified"]]
    counts["quant_extractable"] = [r["study_id"] for r in rows if r["evidence_category"] == "A"]
    counts["quant_comparable"] = [r["study_id"] for r in rows if r["comparability_to_figure"] == "COMPARABLE"]
    counts["integrity_excluded"] = [r["study_id"] for r in rows if r["evidence_category"] in ("E", "F")]
    counts["reviews_benchmarks"] = [r["study_id"] for r in rows if r["evidence_category"] == "G"]
    counts["outcome_excluded"] = [r["study_id"] for r in rows if r["evidence_category"] == "H"]
    counts["unresolved"] = [r["study_id"] for r in rows if r["evidence_category"] == "I"]
    counts["abstract_only"] = [r["study_id"] for r in rows if r["evidence_category"] == "C"]
    counts["secondary_only"] = [r["study_id"] for r in rows if r["evidence_category"] == "D"]
    return counts


def render(counts):
    lines = []
    lines.append(f"Total sources (rows in extraction_table.csv): {counts['total_sources']}")
    lines.append("\nBy evidence category:")
    for cat in sorted(counts["by_category"]):
        ids = counts["by_category"][cat]
        lines.append(f"  {cat}: {len(ids)} -> {', '.join(ids)}")
    lines.append(f"\nPrimary studies (A+B+C+D, excludes reviews/retracted/integrity-concern/outcome-excluded): {len(counts['primary_studies'])}")
    lines.append(f"Independent samples (unique sample_id): {len(counts['independent_samples'])}")
    lines.append(f"Full-text verified PRIMARY studies (category A): {len(counts['fulltext_verified_primary'])} -> {', '.join(counts['fulltext_verified_primary'])}")
    lines.append(f"Full-text verified REVIEWS/benchmarks: {len(counts['fulltext_verified_reviews'])} -> {', '.join(counts['fulltext_verified_reviews'])}")
    lines.append(f"Quantitatively extractable (category A): {len(counts['quant_extractable'])}")
    lines.append(f"Quantitatively COMPARABLE (in figures/volume_response.png): {len(counts['quant_comparable'])} -> {', '.join(counts['quant_comparable'])}")
    lines.append(f"Excluded for data-integrity reasons (E+F): {len(counts['integrity_excluded'])} -> {', '.join(counts['integrity_excluded'])}")
    lines.append(f"Reviews/benchmarks, not primary data (G): {len(counts['reviews_benchmarks'])} -> {', '.join(counts['reviews_benchmarks'])}")
    lines.append(f"Excluded for outcome mismatch (H): {len(counts['outcome_excluded'])} -> {', '.join(counts['outcome_excluded'])}")
    lines.append(f"Unresolved (I): {len(counts['unresolved'])}")
    lines.append(f"Abstract-only (C): {len(counts['abstract_only'])}")
    lines.append(f"Secondary-source-only (D): {len(counts['secondary_only'])}")
    return "\n".join(lines)


if __name__ == "__main__":
    rows = load_rows()
    counts = compute(rows)
    print(render(counts))
