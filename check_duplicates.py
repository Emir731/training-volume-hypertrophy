"""
A simple, honest deduplication check across data/extraction_table.csv,
based on DOI, PMID, and normalized title.

THIS IS NOT a substitute for formal search-record deduplication (as a
tool like Covidence or Rayyan would do across raw database export
files) - this project never had raw multi-database export files to
deduplicate in the first place (see SYSTEMATIC_SEARCH.md). This script
only checks whether any two ROWS ALREADY IN THE EXTRACTION TABLE
appear to describe the same underlying study - a much narrower,
after-the-fact check.

This is also explicitly DIFFERENT from validate_data.py's duplicate
study_id check: that check confirms no study_id string is reused; this
script checks whether two DIFFERENT study_ids might accidentally refer
to the same real-world study.

Run: python3 analysis/check_duplicates.py
"""

import csv
import re
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "extraction_table.csv"


def normalize_title(citation):
    """Very rough normalization: lowercase, strip punctuation/whitespace.
    Good enough to catch near-identical citation strings, not a real
    title-matching algorithm."""
    text = citation.lower()
    text = re.sub(r"[^a-z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_doi(text):
    m = re.search(r"10\.\d{4,9}/[^\s,;)]+", text)
    return m.group(0).rstrip(".") if m else None


def extract_pmid(text):
    m = re.search(r"PMID[:\s]*(\d+)", text, re.IGNORECASE)
    return m.group(1) if m else None


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_possible_duplicates(rows):
    by_doi, by_pmid, by_title_prefix = {}, {}, {}
    findings = []

    for r in rows:
        combined = (r.get("citation", "") or "") + " " + (r.get("doi_pmid", "") or "")
        doi = extract_doi(combined)
        pmid = extract_pmid(combined)
        title_key = normalize_title(r.get("citation", ""))[:60]  # first ~60 chars as a rough key

        if doi:
            by_doi.setdefault(doi, []).append(r["study_id"])
        if pmid:
            by_pmid.setdefault(pmid, []).append(r["study_id"])
        if title_key:
            by_title_prefix.setdefault(title_key, []).append(r["study_id"])

    for doi, ids in by_doi.items():
        if len(set(ids)) > 1:
            findings.append(f"Same DOI ({doi}) appears on multiple rows: {ids}")
    for pmid, ids in by_pmid.items():
        if len(set(ids)) > 1:
            findings.append(f"Same PMID ({pmid}) appears on multiple rows: {ids}")
    for title, ids in by_title_prefix.items():
        if len(set(ids)) > 1:
            findings.append(f"Near-identical citation prefix appears on multiple rows: {ids} (\"{title}...\")")

    return findings


if __name__ == "__main__":
    rows = load_rows()
    findings = find_possible_duplicates(rows)
    print(f"Checked {len(rows)} rows for possible duplicate underlying studies (by DOI, PMID, and citation-text prefix).\n")
    if not findings:
        print("No possible duplicates found by this check.")
    else:
        for f in findings:
            print(f"  - {f}")
    print(
        "\nReminder: this check operates on rows already curated into extraction_table.csv, "
        "not on raw multi-database search exports (which this project never had - see "
        "SYSTEMATIC_SEARCH.md). It cannot catch a duplicate that was never added as a row, "
        "and it is not a replacement for formal systematic-review deduplication software."
    )
