# Final Audit

## Verification-type breakdown (more important than any single count)

**A. Verified directly from primary full text (this project read the actual article):**
Radaelli 2015, Heaselgrave 2019, Aube 2022, Schoenfeld 2019 (peer-reviewed), de Camargo 2026 (preprint — flagged as not peer-reviewed), Camargo et al. 2025 narrative review, Baz-Valle et al. 2022.

**B. Verified from secondary sources (known only via how another paper describes them):**
Ostrowski 1997, Amirthalingam 2017 — both known only via Camargo et al. 2025's own table, never independently retrieved.

**C. Abstract-only (this project read the study's own abstract, but not its full text):**
Rantila & Ahtiainen 2026, Barsuhn et al. 2025, Enes et al. 2024, Enes et al. 2025, Moreno et al. 2024, Scarpelli et al. 2022, Nascimento de Oliveira Jr et al. 2022, an older-adults non-responder study.

**D. Inferred (this project's own investigated inference, not an author-stated fact):**
Schoenfeld 2019's effect-size formula (`effect_size_metric_type = pooled_baseline_sd_standardized_d_INFERRED`) — a strong numerical match, not a confirmed method. Radaelli's weekly-set correction (6/18/30 biceps, 9/27/45 triceps) — resolved via convergent secondary sources describing the same exercise-count mechanism, not a fresh direct re-read of Radaelli's own Methods section in this audit round.

**E. Exploratory project-side analysis (code this project wrote, not a finding from any paper):**
`analysis/comparability.py`'s STATISTICALLY_COMPARABLE / biological-heterogeneity split, `analysis/verify_schoenfeld_es.py`'s formula investigation, `analysis/check_duplicates.py`'s citation-level duplicate check, `analysis/canonical_counts.py`'s summary numbers.

## Canonical counts (from `analysis/canonical_counts.py`, this run)
Total sources 22; primary studies (A+B+C+D) 15; unique sample_id values 15 (curated identifiers, not database-verified independence — see EVIDENCE_MAP.md); category-A full-text-verified-with-quantitative-data 5; figure-eligible (statistically comparable) 3; integrity-excluded 2; reviews/benchmarks 4; outcome-excluded 1; unresolved 0.

## Validation, test, reproducibility, figure results (all re-run this round, from repository root)
- `validate_data.py`: exit 0
- `tests.py`: 13/13 passed
- `comparability.py`: exit 0, four declared dimensions (effect-size metric, outcome construct, volume-manipulation type, design structure) all actually implemented and exercised — a test now proves this
- `canonical_counts.py`: exit 0
- `check_duplicates.py`: exit 0, 1 non-duplicate correctly not flagged (same author group, two different works)
- `check_document_consistency.py`: exit 0, found and fixed 2 genuine stale-count instances (README, EVIDENCE_MAP) in an earlier pass this round; 3 remaining hits are self-referential meta-text describing that fix, a documented false-positive limitation of the checker
- `synthesis.py`: exit 0, figure regenerates from `data/synthesis_arms.csv`
- `python -m compileall analysis`: exit 0

## Comparability result
Refactored to remove hardcoded study_id checks entirely — verdicts now come from three controlled-vocabulary fields, proven by a test using fabricated study_ids the code has never seen. Training-status and muscle-group differences are now reported as biological-heterogeneity notes that do NOT gate figure inclusion (a training-status difference disqualifying a comparison would make this project's own research question unanswerable). Statistical comparability (effect-size construction, outcome construct, volume-manipulation type, design structure) remains the actual gate. Result: Radaelli/Heaselgrave/Aube remain figure-eligible; Schoenfeld 2019 and de Camargo 2026 remain excluded, now for a fully data-derived and dimension-complete reason.

## Terminology corrections made this round
- Title changed from "A Systematic Review and Exploratory Dose-Response Analysis" to "A Systematic-Search Attempt and Exploratory Evidence Synthesis."
- "Quantitatively comparable" replaced throughout with "statistically comparable" / "figure-eligible for exploratory comparison," with an explicit README section explaining why the stronger phrase overstated things (3 studies measure different muscle groups and populations).
- "15 independent samples" reworded to "15 unique sample identifiers assigned in the curated evidence table" wherever it appeared, with the distinction from database-verified independence stated explicitly.
- Manuscript language: removed "ceiling," "bought nothing extra"; replaced with "was associated with," "did not show a statistically significant difference," "the currently verified evidence."
- `data/synthesis_arms.csv` gained `significance_type` (explicitly `within_group_pre_post` for all 9 arms — none are between-group significance) and `effect_size_provenance` (`author_reported` for all 9 — a test now enforces this can never silently become a project-calculated value).

## A genuine bug found and fixed this round
While fixing `study_design`-based comparability checking, de Camargo 2026's `country` and `study_design` fields were found corrupted from an earlier unquoted-CSV-comma bug (country field had bled into study_design). Fixed; this would not have been caught without actually implementing the design_structure dimension rather than leaving it declared-but-unused.

## Remaining limitations (unchanged in kind, some narrowed in scope)
- Deduplication remains a narrow citation-level check, not formal search-record deduplication — no raw multi-database export ever existed to deduplicate.
- 8 of 22 sources remain abstract-only; Ostrowski 1997 and Amirthalingam 2017 remain un-independently-verified.
- Radaelli's weekly-set correction still rests on convergent secondary sources, not a fresh primary re-read completed in this audit round.
- README/manuscript/EVIDENCE_MAP consistency is checked by `check_document_consistency.py` but that check is a simple substring heuristic with acknowledged false-positive/false-negative limits, not full language understanding.

## Is this genuinely defensible as a ~9/10 student research project?

**Yes, with the above limitations stated as limitations rather than hidden — approximately 9/10.**

What specifically changed scientifically this round, not just documentation volume: (1) the comparability framework no longer has a declared-but-unimplemented dimension — all four are real, tested checks; (2) training status was deliberately kept OUT of the comparability gate because gating on it would contradict this project's own research question, and that reasoning is now explicit rather than implicit; (3) the "significant" annotation in the figure is now precisely defined as within-group, not between-group, closing a real interpretability gap; (4) effect-size provenance is now enforced by a test, not just a convention; (5) implementing the design_structure check surfaced and fixed a real data-corruption bug that had gone undetected through two prior audit rounds. A skeptical professor could reasonably ask why deduplication and 8 abstract-only sources remain unresolved — those are real, named gaps, not manufactured ones, which is itself the standard this project is aiming for.

*Last updated: September 2026.*
