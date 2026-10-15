# Training Volume and Muscle Hypertrophy: A Systematic-Search Attempt and Exploratory Evidence Synthesis in Resistance-Trained Individuals

*(Title note: an earlier draft used "A Systematic Review and Exploratory Dose-Response Analysis." That overstated the work — no database-complete systematic search was achieved and no dose-response model was fit. This title aims to say exactly what was done: an attempt at systematic search, and an exploratory synthesis of what it found.)*

## Project Status

**This is an ongoing independent student research project, NOT a completed systematic review or meta-analysis.** A genuinely systematic search was attempted but could not be completed to database-verified standards with the tools available (see `SYSTEMATIC_SEARCH.md`). As of this update, 22 sources have a row in `data/extraction_table.csv`. **This number is not a literature total** — it is how many sources this project has looked at and classified, nothing more.

## Abstract

This project investigates the dose-response relationship between resistance-training (RT) volume and skeletal muscle hypertrophy, and whether training status moderates it. Of 22 sources examined: 5 are primary studies verified against full text with usable quantitative data (category A), 8 are abstract-only (category C), 2 are known only via a secondary source (category D), 4 are reviews/meta-analyses used as context rather than primary data (category G), 1 is excluded for having no hypertrophy outcome (category H), and 2 required integrity re-classification — one formally retracted (category E), one the subject of a published data-integrity critique (category F). Only 3 of the 22 sources (Radaelli 2015, Heaselgrave 2019, Aube 2022) are both primary-verified AND comparable to each other on effect-size construction and outcome type; these are the only 3 in the quantitative figure. Two more (Schoenfeld 2019, de Camargo 2026) have real, primary-verified quantitative data but are excluded from that figure for specific, investigated reasons (see Comparability Framework below) — not because they disagree with a hypothesis. Among the 3 comparable studies, findings genuinely diverge: an untrained sample shows hypertrophy effect size increasing with volume, while two trained samples show no significant between-group difference across 2-3x volume ranges. No formal meta-analysis has been performed, and one is not currently justified (see `analysis/meta_analysis_eligibility.md`).

## Canonical Counts (single source of truth — computed directly from the data, not hand-typed)

Run `python3 analysis/canonical_counts.py` to regenerate this table from the actual CSV. If any other document in this repository disagrees with these numbers, this table (and the script behind it) is correct and the other document is stale.

| Metric | Count | Which studies |
|---|---|---|
| Total sources (rows in extraction_table.csv) | 22 | — |
| Primary studies (categories A+B+C+D) | 15 | see EVIDENCE_MAP.md |
| Independent participant samples (unique sample_id assigned in the curated evidence table — see caveat below) | 15 | — |
| Full-text verified PRIMARY studies (category A) | 5 | Radaelli 2015, Heaselgrave 2019, Aube 2022, Schoenfeld 2019, de Camargo 2026 |
| Quantitatively extractable (category A) | 5 | same as above |
| Statistically comparable AND figure-eligible (in figures/volume_response.png) | 3 | Radaelli 2015, Heaselgrave 2019, Aube 2022 |
| Excluded for data-integrity reasons (E+F) | 2 | Barbalho 2019/2020 (men, retracted), Barbalho 2019 (women, integrity concern) |
| Reviews/benchmarks, not primary data (G) | 4 | Schoenfeld/Ogborn/Krieger 2017, Pelland et al. 2025/26, Baz-Valle et al. 2022, Camargo et al. 2025 (narrative review) |
| Excluded for outcome mismatch (H) | 1 | Marshall et al. 2011 (strength only, no hypertrophy measure) |
| Abstract-only (C) | 8 | see EVIDENCE_MAP.md |
| Secondary-source-only (D) | 2 | Ostrowski 1997, Amirthalingam 2017 |

**Terminology precision, read before citing any of the above:**
- "15 independent participant samples" means 15 unique `sample_id` values assigned by this project as it curated these 22 rows — it does NOT mean 15 formally, database-verified independent studies. Only the 5 category-A studies have that level of verification; the rest rely on this project's own reading of an abstract or a secondary source's description.
- "Statistically comparable" (used above and in `analysis/comparability.py`) means the 3 studies share an effect-size construction, an outcome-construct type, a volume-manipulation type, and a study-design structure — enough to justify showing their numbers on one set of axes for descriptive purposes. It does **not** mean they are biologically interchangeable: they measure different muscle groups (Radaelli/Heaselgrave: upper-arm elbow flexors; Aube: quadriceps) and different training-status populations (untrained vs. two trained samples). See "Reconsidering 'comparable'" below.

## Reconsidering "Comparable"

An earlier round of this project called the 3-study figure simply "quantitatively comparable." That phrase is too strong on its own. `analysis/comparability.py` now separates two questions explicitly:

1. **Statistical comparability** — do two studies compute their numbers the same way and measure the same type of outcome? This is a hard requirement; a mismatch here means `NOT_COMPARABLE` and exclusion from the figure (this is why Schoenfeld 2019 and de Camargo 2026 are excluded).
2. **Biological/population heterogeneity** — do two studies represent the same training status and muscle group? This is reported descriptively and does **not** gate figure inclusion, because this project's own research question is specifically about whether training status changes the relationship — requiring population homogeneity would make that question unanswerable by construction.

The combined judgment actually used for the figure is `FIGURE_ELIGIBLE_FOR_EXPLORATORY_COMPARISON`: statistically comparable, biological heterogeneity noted alongside rather than hidden. Radaelli, Heaselgrave, and Aube meet this. This is weaker than "pooled biological effect estimate" and stronger than "arbitrarily grouped" — an exploratory visualization, not a meta-analytic claim.

## What This Project Does NOT Claim
- Not a completed, database-verified systematic review
- Not a formal meta-analysis
- Not a definitive dose-response model or an "optimal number of sets"
- Not a complete database search (see `SYSTEMATIC_SEARCH.md`)
- Not a pooled quantitative estimate of any kind
- Not evidence that training status "has no effect" or that higher volume "buys nothing" in trained lifters — the 3 comparable studies are consistent with a training-status-dependent pattern but do not establish one, and a 4th full-text-verified trained-population study (Schoenfeld 2019) shows the opposite pattern



Every row in `data/extraction_table.csv` has exactly one `evidence_category`:

| Category | Meaning |
|---|---|
| **A** | Primary-source verified (full text) AND quantitative data usable |
| **B** | Primary-source verified (full text) but only qualitative findings (currently 0 rows) |
| **C** | Abstract-only |
| **D** | Secondary-source-only (never independently retrieved) |
| **E** | Retracted |
| **F** | Data-integrity concern / published critical commentary |
| **G** | Review, meta-analysis, or meta-regression (a benchmark, not a primary sample) |
| **H** | Excluded: outcome mismatch (no hypertrophy measure) |
| **I** | Unresolved (currently 0 rows — the one prior unresolved item, Radaelli's weekly-set count, was resolved this round) |

**Note that category A (verification) is separate from `comparability_to_figure` (whether a study's data can be merged with the current synthesis)** — a study can be fully category A and still not belong in the figure, which is exactly the situation for Schoenfeld 2019 and de Camargo 2026. See `analysis/comparability.py` for the explicit, rule-based reasoning, not a prose assertion.

**A full study-by-study breakdown lives in [`EVIDENCE_MAP.md`](./EVIDENCE_MAP.md).**

## Prior Systematic Evidence

Two existing, real, rigorously-executed systematic reviews already cover large parts of this question. They are used here as **contextual benchmarks only** — their included studies are NOT merged into this project's own dataset or figure.

| | Baz-Valle et al. (2022) | Pelland et al. (2025/26) |
|---|---|---|
| Population | Resistance-trained, 18-35y, ≥1yr experience — closely matches this project's own focus | Mixed training status (modeled as a covariate), broader |
| Databases | PubMed, Scopus, Cochrane Library | Not fully extracted by this project |
| Search period | Through January 2021 | Through approximately April 2023 |
| Records screened → included | 2,083 → 7 (6 usable for quantitative analysis) | 6,515 (post-dedup) → 135 (title/abstract) → 67 (full-text included) |
| Relevance | Near-identical population to this project | Most current, most methodologically sophisticated existing answer to the general question |
| Key finding | No significant difference moderate-vs-high volume for quadriceps/biceps; high volume favored for triceps (p=0.01); suggests ~12-20 weekly sets as an optimal range | Positive volume-hypertrophy relationship (100% posterior probability) with diminishing returns at higher volumes |
| Methodological difference from this project | A real, institutional-access systematic search — the gold standard this project's own tools cannot reproduce | Uses a direct/indirect/fractional set-counting method more careful than most primary studies |

**Why this matters for interpreting this project's own numbers:** Baz-Valle's search, restricted to almost exactly this project's population of interest, found only 6-7 usable studies as of January 2021. This project's own 3-study comparable set (spanning through 2022) is of a similar order of magnitude — evidence that this specific sub-literature is genuinely small, not that this project's search was unusually incomplete.



**Primary:** Does resistance training volume have a dose-response relationship with skeletal muscle hypertrophy?

**Secondary/moderator question:** Does participant training status modify this relationship?

Muscle group, training frequency, proximity to failure, load/intensity, and measurement method remain exploratory discussion points, not modeled variables - the dataset cannot yet support treating them as such.

## Background

Two existing works address this question at a high level and are used here as **contextual benchmarks only** (excluded from this project's own primary synthesis to avoid double-counting evidence that is itself a synthesis of other studies):

- **Schoenfeld, Ogborn & Krieger (2017)** - 15 studies/34 groups, mostly untrained/recreational. Roughly linear relationship (continuous: +0.023 ES/set, p=0.002; categorical high-vs-low: ES diff 0.241, ~3.9%).
- **Pelland et al. (2025)** - 67 studies, 2,058 participants, Bayesian meta-regression. Confirms a positive volume effect (100% posterior probability) with **diminishing returns** at higher volumes.

## Methods

### Search Strategy
**Not a documented systematic search.** Sources were found via ad hoc web search plus citation-chasing through the reference lists of studies already in hand - this is explicitly how Schoenfeld et al. 2019, both Barbalho et al. studies, Rantila & Ahtiainen 2026, de Camargo et al. 2026, and Barsuhn et al. 2025 were all found, and how 6 further candidate studies (not yet screened at all - see below) were identified. A real, documented, reproducible search has not yet been run.

### Eligibility Criteria
Planned: randomized or well-controlled within-subject trials, >=2 weekly training volumes, >=6 weeks duration, a direct muscle hypertrophy outcome, healthy adults, any training status. Applied informally, source-by-source, so far - **and, as this round demonstrated, applying it requires checking a study's integrity status, not just its topic match.**

### Data Extraction and Verification Taxonomy
See `data/extraction_table.csv`. Every row is tagged with one of:

- `PRIMARY_FULL_TEXT_VERIFIED` - read directly from the full peer-reviewed primary article (4 studies: Radaelli 2015, Heaselgrave 2019, Aube 2022, Schoenfeld 2019)
- `PRIMARY_FULL_TEXT_VERIFIED_BUT_PREPRINT` - full text read directly, but not yet peer-reviewed (1 study: de Camargo 2026)
- `PRIMARY_ABSTRACT_ONLY` - abstract/search-excerpt level only (2 studies: Rantila 2026 - paywalled full text; Barsuhn 2025 - not yet fetched as one continuous document)
- `SECONDARY_SOURCE_ONLY` - known only via how another paper cites it, not independently retrieved (1 study: Ostrowski 1997)
- `AGGREGATE_BENCHMARK_NOT_A_PRIMARY_DATAPOINT` - meta-analyses used for context (2 sources)
- `SERIOUS_DATA_INTEGRITY_CONCERNS` - a formal, published statistical critique documents implausible data patterns in this specific body of work (1 study: Barbalho et al. 2019, women)
- `RETRACTED` - formally retracted by the authors; never used as evidence (1 study: Barbalho et al. 2019/2020, men)

No numeric value was estimated or invented. Where full-text access failed, the cell says so explicitly.

### Radaelli 2015 weekly-set count: RESOLVED this round (was previously flagged unresolved)
An earlier round of this project flagged a conflict between its own primary-text reading (implying 3/9/15 weekly sets) and Schoenfeld et al. (2019)'s citation of this study (6/18/30 weekly sets). This round investigated the conflict rather than picking a side: three independent, technically detailed secondary sources (a specialized sports-science analysis, a separate independent analysis, and Schoenfeld et al. 2019's own peer-reviewed citation) all converge on the same specific mechanism - the design used 1/3/5 sets **per exercise**, with **2 exercises assigned to biceps and 3 to triceps**, a detail this project's own earlier reading had missed. This gives 6/18/30 weekly sets for biceps and 9/27/45 for triceps, now used throughout this repository (including the corrected figure). This is disclosed as a correction of this project's own earlier incomplete extraction, backed by strong convergent secondary evidence - not a coin-flip resolution of two equally-uncertain primary readings, though a direct fresh re-read of Radaelli's own Methods section explicitly confirming "2 exercises for biceps, 3 for triceps" has not been completed and remains a recommended final confirmation step. See `EVIDENCE_MAP.md` and the `notes` field for `P01_Radaelli2015` in `data/extraction_table.csv` for full detail.

### Training Volume Definition
Volume is defined differently across every study in this table - direct sets of one exercise (Radaelli), direct sets across 2 primary exercises (Aube), sets that mix direct and indirect muscle involvement (Heaselgrave), sets per exercise per session with separate upper/lower-body weekly totals (Schoenfeld 2019), and volume defined relative to each participant's own habitual training rather than in absolute terms (de Camargo 2026, Barsuhn 2025). These are not interchangeable units. See `volume_definition` column, per study.

### Training Status Classification
Same category system as before (untrained / recreationally active / resistance-trained / highly resistance-trained / unclear / mixed-aggregate), applied only where a study states its own criteria. Schoenfeld et al. 2019's sample (4.4+-3.9 years RT experience, no strength-relative-to-bodyweight screen) is classified `resistance-trained`, distinct from Aube et al.'s more stringent `highly resistance-trained` screen (1RM squat:BM ~2.09).

### Risk of Bias
Unchanged from the prior round for the originally-verified studies (see `data/risk_of_bias.csv`); a full TESTEX pass has not yet been run for Schoenfeld 2019 or de Camargo 2026 despite their full text now being available - noted as a next step, not backfilled with a rushed judgment.

### Statistical Analysis
**Still no formal meta-analysis, and one is still not justified.** This round mathematically investigated (not just noted) why Schoenfeld et al. 2019's reported effect sizes did not match this project's own recalculation: testing three candidate formulas against the raw data (see `analysis/verify_schoenfeld_es.py`), the authors' reported triceps ES (0.12/0.30/0.55) matches, to within 0.01, a Δmean-divided-by-the-simple-average-of-all-3-groups'-baseline-SD calculation - NOT a within-group change-score-SD calculation (which is off by 0.15-0.58, and is the convention used for Radaelli/Heaselgrave/Aube's own reported ES). This is a strong, investigated inference, not a confirmed fact (the authors' original code was not available to check directly), and it does not resolve the comparability problem - it explains it: Schoenfeld 2019's ES is standardized against a pooled cross-group baseline, a structurally different quantity from the other three studies' own-group pre-post d. **Schoenfeld 2019 and de Camargo 2026 remain excluded from the quantitative synthesis figure for this specific, now-documented reason (not vague incomparability), and are discussed narratively instead.** See `data/extraction_table.csv` columns `reported_effect_size`, `independently_calculated_effect_size`, and `effect_size_method` for the full record, kept as separate fields specifically so the author's number and any project-side recalculation are never merged into one value.

## Results

### Verification-status summary (of 22 sources examined; NOT a literature total — see Canonical Counts above)
- **Category A — full-text verified, quantitative data usable (5):** Radaelli 2015, Heaselgrave 2019, Aube 2022, Schoenfeld 2019, de Camargo 2026 (preprint)
- **Category C — abstract-only (8):** Rantila & Ahtiainen 2026, Barsuhn et al. 2025, Enes et al. 2024, Enes et al. 2025, Moreno et al. 2024, Scarpelli et al. 2022, Nascimento de Oliveira Jr et al. 2022, an older-adults non-responder study
- **Category D — secondary-source-only (2):** Ostrowski 1997, Amirthalingam 2017
- **Category G — reviews/benchmarks, not primary data (4):** Schoenfeld/Ogborn/Krieger 2017, Pelland et al. 2025/26, Baz-Valle et al. 2022, Camargo et al. 2025 (narrative review)
- **Category H — excluded, outcome mismatch (1):** Marshall et al. 2011 (strength only, no hypertrophy measure)
- **Category E — retracted (1):** Barbalho et al. 2019/2020 (men)
- **Category F — data-integrity concern (1):** Barbalho et al. 2019 (women)

### Quantitative Synthesis (3 comparable studies)
Radaelli (untrained): effect size increases with volume (0.10 ns → 0.73 → 1.10). Heaselgrave and Aube (trained): no significant between-group difference across a 2-3x volume range, and neither pattern is a clean flat line — Heaselgrave peaks at the middle dose, Aube's lowest dose matches or beats its highest on most measures. See `figures/volume_response.png`, generated from `data/synthesis_arms.csv`.

### Two more real studies, deliberately not in that figure
- **Schoenfeld et al. 2019** (trained men, full raw data): higher volume produced significantly greater hypertrophy at 3 of 4 sites — the opposite pattern from Heaselgrave/Aube. Excluded from the figure because its effect size is standardized differently (see `analysis/verify_schoenfeld_es.py` and `effect_size_metric_type` in the extraction table — labeled `pooled_baseline_sd_standardized_d_INFERRED`, an inference, not an author-confirmed method).
- **de Camargo et al. 2026** (preprint, within-subject): a +120% relative volume increase did not produce meaningfully more hypertrophy than a +20% increase (ES -0.36, 95% CI -1.35 to 0.64, crossing zero). Excluded because it uses a relative-to-habitual-volume design and a between-protocol effect size, not an absolute weekly-set, within-group one.

### Why do these studies disagree? (hypotheses, not demonstrated conclusions)
Candidate explanations not yet tested against each other: how "resistance-trained" was actually screened (Aube's sample was unusually strong; Schoenfeld 2019's was not screened by a strength-to-bodyweight ratio), intervention duration (6-10 weeks for most vs. Radaelli's 6 months), and volume-counting differences (direct vs. mixed direct/indirect sets, absolute vs. relative-to-habitual). None of these is established as *the* explanation.

## Discussion
The three directly comparable studies do not establish a single monotonic pattern, and the currently verified evidence as a whole is heterogeneous rather than convergent. A full-text-verified study (Schoenfeld 2019) finds hypertrophy scaling with volume in a trained sample; two other full-text-verified trained-population studies (Heaselgrave, Aube) do not. This project treats that as a real, open disagreement rather than something to resolve by picking a side. Separately, two candidate studies (Barbalho et al. 2019) required exclusion on integrity grounds: the men's companion study is reported retracted at the authors' own request according to Retraction Watch's coverage of a 2020 critique (Vigotsky, Nuckols, Heathers, Krieger, Schoenfeld & Steele) — the journal's own retraction notice has not been independently retrieved by this project, so this status is sourced to that secondary report, not verified firsthand. The women's study is not confirmed retracted but is covered by the same critique, which describes "improbable data patterns," not fraud — this project uses no stronger language than that. The available evidence is insufficient to determine whether training status systematically modifies the volume-hypertrophy dose-response relationship; it is consistent with that hypothesis in 2 of 3 comparable studies and inconsistent with it in the third.

## What This Project Does NOT Claim
- Not a completed systematic review
- Not a formal meta-analysis
- Not a definitive dose-response model or "optimal number of sets"
- Not a complete, database-verified literature search
- Not a pooled quantitative estimate of any kind

## Limitations
1. No completed, database-verified systematic search — see `SYSTEMATIC_SEARCH.md` for exactly what tool-based searching could and could not establish.
2. Of 22 sources, only 5 are full-text verified with usable numbers; 8 remain abstract-only.
3. Deduplication is a simple citation/DOI/PMID text check (`analysis/check_duplicates.py`), not formal search-record deduplication software — no raw multi-database export ever existed to deduplicate.
4. Two studies (Barbalho et al.) required integrity exclusion found only through incidental citation-chasing, not a deliberate per-study integrity check.
5. Schoenfeld 2019 and de Camargo 2026 have real, verified numbers that cannot currently be merged with the comparable 3-study figure — see `analysis/comparability.py` for the exact, field-derived reasons.
6. Ostrowski 1997 and Amirthalingam 2017 remain un-independently-verified (known only via a secondary review's own table).
7. Risk-of-bias assessment is complete for only 2 of 22 sources (Heaselgrave, Aube fully; Schoenfeld 2019 and de Camargo 2026 partially).
8. Radaelli's weekly-set correction (6/18/30 biceps, 9/27/45 triceps) rests on convergent secondary sources, not a fresh direct re-read of the primary Methods section confirming the exact exercise count — see `RESEARCH_NOTES.md`.

## Reproducibility
```bash
git clone <this-repo-url>
cd <repo-folder>
pip install -r requirements.txt
python analysis/validate_data.py
python analysis/synthesis.py
```

## AI-Assisted Research Disclosure
Literature search, citation verification, full-text retrieval, and data organization were conducted with AI assistance (Claude, Anthropic). All inclusion/exclusion decisions and interpretation are the author's. This round's data-integrity finding (Barbalho et al.) was surfaced during citation-chasing and is disclosed in full, including that it was found somewhat by chance rather than through a deliberate integrity-screening step - a real limitation of the current process, not hidden.

## Data Availability
`data/extraction_table.csv`, `data/screening_log.csv`, `data/risk_of_bias.csv` - all plain CSV, version-controlled.

## Figures
`figures/volume_response.png` - 3 studies only (Radaelli, Heaselgrave, Aube); Schoenfeld 2019 and de Camargo 2026 are deliberately excluded from this figure for the methodological reasons stated above, not because they disagree with a hypothesis.

## Repository Structure
```
├── README.md
├── EVIDENCE_MAP.md               # study-by-study verification/comparability record
├── SYSTEMATIC_SEARCH.md          # search methodology and honest tool limitations
├── RESEARCH_NOTES.md             # correction/discovery history
├── QUALITY_CONTROL.md            # PASS/FAIL/LIMITED audit
├── requirements.txt
├── data/
│   ├── extraction_table.csv
│   ├── DATA_DICTIONARY.md        # what every field means
│   ├── screening_log.csv
│   └── risk_of_bias.csv
├── analysis/
│   ├── synthesis.py              # generates the 3-study figure
│   ├── comparability.py          # explicit rules for figure-inclusion decisions
│   ├── canonical_counts.py       # single source of truth for all summary numbers
│   ├── verify_schoenfeld_es.py   # effect-size formula investigation
│   ├── meta_analysis_eligibility.md
│   ├── validate_data.py          # structural/consistency/pseudoreplication checks
│   └── tests.py                  # automated tests for the above
├── figures/
│   └── volume_response.png
├── manuscript/
│   └── manuscript.md
└── references/
    └── references.bib
```

## Next Steps
1. Obtain Rantila & Ahtiainen 2026 full text (currently paywalled) and Barsuhn 2025's full PDF (currently assembled from excerpts only)
2. Resolve the Radaelli 2015 weekly-set discrepancy by re-checking the primary methods section directly
3. Screen the 6 newly-identified citation-chased studies, starting with the 2025 narrative review (near-identical research question)
4. Extend risk-of-bias assessment to Schoenfeld 2019 and de Camargo 2026
5. Actively check every currently-included study for retractions/critiques (not just rely on incidental discovery, as happened with Barbalho)
6. Run a real, documented systematic search rather than continuing indefinite citation-chasing

## Author
Sanjar Osmanov - independent student research project, conducted with AI-assisted literature search and data organization tools (see AI-Assisted Research Disclosure).

**Last updated:** September 2026
