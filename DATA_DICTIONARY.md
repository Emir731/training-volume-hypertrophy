# Data Dictionary — data/extraction_table.csv

Every field, what it means, and how to interpret missing/uncertain values. If a field isn't listed here, treat that as a gap to fix, not as self-explanatory.

## Identification
- **study_id** — unique key for this row. Prefix meaning: `P`=study from the original core list, `M`=meta-analysis/systematic-review benchmark, `S`=study known only via secondary source, `R`=study added during citation-chasing or the search phase, in discovery order (R001-style IDs live in screening_log.csv; R0xx_Name-style IDs in the extraction table are a separate, later numbering — the two are not the same sequence, which is itself a known inconsistency, see QUALITY_CONTROL.md).
- **citation** — full reference string as far as it could be assembled. If any part is unconfirmed, the field says so inline rather than presenting a clean-looking but partly-guessed citation.
- **doi_pmid** — DOI and/or PMID. "not yet located" means genuinely not found, not that none exists.

## Study characteristics
- **study_design** — as described by the study itself (parallel-group RCT, within-subject unilateral, etc.).
- **participant_n** — total analyzed N, with per-group breakdown where known.
- **sex, age_mean_sd** — as reported. Blank means not extracted, not "not reported by the study."
- **training_status** — one of: `untrained`, `recreationally active`, `resistance-trained`, `highly resistance-trained`, `unclear`, or `mixed (aggregate)` (reviews only). Assigned ONLY from what the study's own methods state — never inferred from age, sex, or performance level.
- **training_status_criteria** — the study's own stated basis for its training-status label (years of experience, a strength-to-bodyweight ratio, etc.), preserved verbatim/paraphrased so the category above is auditable, not asserted.

## Volume
- **volume_definition** — free text describing HOW the study counted a "set" (direct vs. indirect, per exercise vs. per muscle, absolute vs. relative-to-habitual). This is the single most important field for judging comparability — never assume two studies' "weekly sets" mean the same thing without reading this field for both.
- **groups_weekly_sets** — the volume conditions compared, in the study's own units.
- **weekly_sets_calculated_or_reported** — states explicitly whether the weekly-set number came directly from the study's own text (`REPORTED`) or was arithmetic done by this project from other stated numbers (`CALCULATED`, with the calculation shown). This distinction matters because a calculated number carries this project's own risk of error (see the Radaelli correction history in RESEARCH_NOTES.md).

## Outcome
- **hypertrophy_measure** — the specific muscle/site and construct measured (e.g., "vastus lateralis CSA," not just "hypertrophy"). Different constructs (muscle thickness vs. CSA vs. DEXA lean mass) are NOT assumed interchangeable — see analysis/comparability.py.
- **measurement_method** — imaging/measurement technique (ultrasound, MRI, DEXA, etc.).

## Results
- **quantitative_result_pct_change** — percentage change figures, with an inline note on whether they were read directly by this project or sourced via another paper's summary of this study.
- **quantitative_result_effect_size** — free-text summary field (legacy from an earlier round); for the studies where effect-size provenance matters most, use the more granular fields below instead.
- **reported_effect_size** — the effect size AS STATED BY THE STUDY'S OWN AUTHORS. Never edited or recalculated.
- **independently_calculated_effect_size** — any effect size THIS PROJECT computed itself from raw data. Always kept in a separate field from the above — never merged.
- **effect_size_method** — how `independently_calculated_effect_size` was computed, or an investigation into how `reported_effect_size` was likely computed (see the Schoenfeld 2019 investigation in analysis/verify_schoenfeld_es.py and RESEARCH_NOTES.md).
- **statistical_result** — p-values, CIs, ANOVA/ANCOVA/mixed-model details as reported.

## Verification and classification
- **primary_source_verified** — the raw verification-status string (e.g., `PRIMARY_FULL_TEXT_VERIFIED`, `RETRACTED`). See analysis/validate_data.py for the full accepted list.
- **evidence_category** — the canonical single-letter classification (A-I). Every row has EXACTLY one. Definitions:
  - **A** — Primary-source verified (full text) AND quantitative data usable
  - **B** — Primary-source verified (full text) but only qualitative findings available (currently no rows — see canonical_counts.py output)
  - **C** — Abstract-only
  - **D** — Secondary-source-only (never independently retrieved)
  - **E** — Retracted
  - **F** — Data-integrity concern / published critical commentary
  - **G** — Review, meta-analysis, or meta-regression (a benchmark, not a primary sample)
  - **H** — Excluded: outcome mismatch (e.g., strength-only, no hypertrophy measure)
  - **I** — Unresolved
- **comparability_to_figure** — whether this row's data is `COMPARABLE`, `NOT_COMPARABLE`, or not applicable/not assessed relative to the current `figures/volume_response.png` synthesis. Computed/justified in `analysis/comparability.py` — never asserted without a stated reason.
- **extraction_status** — free-text note on exactly how much of the source was actually read and what remains missing.
- **data_provenance** — where inside the source each number came from (Results text, a specific table, a secondary source's own table, etc.) and whether this project read that primary location directly.
- **notes** — anything important that doesn't fit elsewhere, including correction history for this specific row.

## Pseudoreplication tracking
- **sample_id** — one unique ID per independent group of human participants. **"Independent sample" does NOT mean every treatment arm** — a 3-arm study (e.g. Heaselgrave 2019's LOW/MOD/HIGH groups) is still ONE sample_id, because all three arms were drawn from the same recruited pool under one study's randomization, not three separate populations. Counting sample_id (not row count, not arm count) is what `analysis/validate_data.py`'s pseudoreplication check enforces.
- **comparison_ids** — free-text list of specific within-study comparisons/arms this row contributes. For the 3 studies in the quantitative figure, the actual arm-level data (one row per comparison_id) lives in `data/synthesis_arms.csv`, not duplicated here — this file's `comparison_ids` field is just a pointer.

## Comparability fields (used by analysis/comparability.py)
These are controlled-vocabulary fields, not free text, specifically so comparability decisions are derived from data rather than hardcoded study lists:
- **effect_size_metric_type** — e.g. `within_group_pre_post_d` (the convention shared by the 3 comparable studies), `pooled_baseline_sd_standardized_d_INFERRED` (Schoenfeld 2019 — the `_INFERRED` suffix marks this as this project's own investigated inference about the authors' method, not something the authors stated), `between_protocol_es_relative_volume_design` (de Camargo 2026, Scarpelli 2022).
- **outcome_construct_type** — e.g. `muscle_thickness_imaging`, `muscle_csa_imaging_plus_biopsy`, `dexa_lean_mass`. Two rows with different values here measure different tissue-level quantities and should not be treated as the same outcome.
- **volume_manipulation_type** — e.g. `absolute_weekly_sets` vs. `relative_to_habitual_volume`. These are different independent variables, not just different units.
- A blank value in any of these three fields means "not yet classified," not "comparable by default" — `analysis/comparability.py` treats an unclassified pair as `PARTIALLY_COMPARABLE` with a stated reason, never as a silent pass.

## What blank actually means
A blank cell means "not extracted / not yet obtained," never "zero," "none," or "not applicable" — those states are always written out explicitly (e.g., "not applicable - review").
