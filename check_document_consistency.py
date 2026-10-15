"""
Checks current-state documents for known stale phrases/numbers left
over from earlier rounds of this project. Does NOT check
RESEARCH_NOTES.md, which is a deliberate historical record and is
supposed to contain old numbers and superseded claims.

Run: python3 analysis/check_document_consistency.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOCS_TO_CHECK = [
    "README.md", "EVIDENCE_MAP.md", "QUALITY_CONTROL.md", "FINAL_AUDIT.md",
    "SYSTEMATIC_SEARCH.md", "manuscript/manuscript.md",
]

# Each pattern paired with why it's stale. Word-boundary-ish matching
# via simple substring search - good enough for this purpose.
STALE_PATTERNS = [
    ("12 sources", "the canonical source count is now 22"),
    ("19 sources", "the canonical source count is now 22"),
    ("completed systematic review", "this project has explicitly not completed one"),
    ("formal meta-analysis", "only acceptable in a sentence saying one was NOT done - checked separately below"),
    ("pooled estimate", "only acceptable in a sentence saying one was NOT computed - checked separately below"),
    ("9 independent studies", "there are 3 independent studies and 9 within-study arms, not 9 independent studies"),
    ("12 independent", "the canonical independent-sample count is 15"),
    ("duplicates were removed", "no formal duplicate-removal at the raw search-record level ever occurred"),
]

# Patterns where the phrase is fine IF preceded by a negation nearby -
# checked with a wider context window rather than flagged outright.
CONTEXT_SENSITIVE = ["formal meta-analysis", "pooled estimate", "completed systematic review"]
NEGATION_WORDS = ["no ", "not ", "none", "NOT ", "No ", "cannot", "Cannot", "does not", "never "]


def check_file(path):
    findings = []
    text = path.read_text(encoding="utf-8")
    for pattern, reason in STALE_PATTERNS:
        for m in re.finditer(re.escape(pattern), text):
            if pattern in CONTEXT_SENSITIVE:
                window = text[max(0, m.start() - 120): m.start()]
                if any(neg in window for neg in NEGATION_WORDS):
                    continue  # negated nearby - treated as an acceptable "we did NOT do X" statement
            line_no = text.count("\n", 0, m.start()) + 1
            findings.append((line_no, pattern, reason))
    return findings


if __name__ == "__main__":
    total = 0
    for doc in DOCS_TO_CHECK:
        path = ROOT / doc
        if not path.exists():
            print(f"[skip] {doc} not found")
            continue
        findings = check_file(path)
        if findings:
            print(f"\n{doc}:")
            for line_no, pattern, reason in findings:
                print(f"  line {line_no}: '{pattern}' - {reason}")
            total += len(findings)
    print(f"\n{total} potential stale-text issue(s) found across {len(DOCS_TO_CHECK)} current-state documents.")
    print("(RESEARCH_NOTES.md is intentionally excluded - it is a historical record.)")
    print(
        "KNOWN LIMITATION: this is a simple substring/negation-window check, not real language "
        "understanding. It can false-positive on meta-text that MENTIONS a stale phrase while "
        "describing having fixed it (e.g. QUALITY_CONTROL.md saying 'we found and corrected "
        "\"12 sources\"'). Any remaining hits should be read in context, not auto-trusted as real bugs."
    )
