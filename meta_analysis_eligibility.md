# Meta-Analysis Eligibility Assessment

**Conclusion: formal meta-analysis is NOT currently justified. No pooled effect, random-effects model, inverse-variance weighting, heterogeneity statistic, or dose-response curve has been computed anywhere in this repository.**

## The checklist and where this project actually stands

| Requirement for a defensible formal meta-analysis | Status |
|---|---|
| Multiple independent studies estimating the same underlying effect | Only 3 independent samples (Radaelli, Heaselgrave, Aube) are pairwise COMPARABLE per `analysis/comparability.py` |
| Effect sizes computed on a common, reconcilable basis | Only these 3 share a common basis (own-group pre-post Cohen's d). Schoenfeld 2019 and de Camargo 2026 have real data but on different bases - see `analysis/verify_schoenfeld_es.py` and `analysis/comparability.py` |
| Raw means/SDs (or equivalent) to compute proper standard errors | Only 1 study (Schoenfeld 2019) provides full raw means/SDs, and it is the one study excluded from the comparable set |
| Sufficient number of studies for a heterogeneity estimate (typically a working minimum of ~5-10 for anything beyond a fixed-effect pool) | 3 |
| A single outcome construct across studies | Even within the 3 comparable studies, the specific muscle/site differs (elbow flexors vs. biceps vs. quadriceps) - a real-but-smaller concern than the outright construct mismatches with the excluded studies |
| Independent samples, no pseudoreplication | Satisfied - `analysis/validate_data.py` enforces one sample_id per independent group, and none are reused |
| A defined, complete literature base (systematic search) | NOT satisfied - see `SYSTEMATIC_SEARCH.md`. This project's own search cannot produce database-level completeness, and 8 identified studies remain abstract-only |

## What would change this assessment

1. Obtaining full text (with raw means/SDs or a directly comparable effect size) for the 8 category-C studies, especially Enes 2024/2025, Moreno 2024, and Rantila 2026.
2. Independently confirming Ostrowski 1997 and Amirthalingam 2017 from their own primary text rather than a secondary review's table.
3. Resolving whether Schoenfeld 2019's and de Camargo 2026's effect sizes can be legitimately converted onto the same scale as the other 3 (this would require either recomputing all studies' ES from raw data with one consistent formula, or finding that the studies report enough raw data to derive a standard mean difference / Hedges' g directly - not attempted so far, because it has not been established that the necessary raw data exist for all of them).
4. If the resulting comparable set reaches roughly 5+ independent studies with a reconcilable effect-size basis, a fixed-effect or simple random-effects pooled estimate would become defensible - formal heterogeneity statistics (I², Q) would still need at least this many studies to mean much.

## Why this project does not do a pooled estimate on the current 3 studies anyway

Even 3 studies with a reconcilable effect-size basis is a thin foundation for a "formal" pooled estimate that would carry the implied authority of a meta-analytic effect size and confidence interval. The current `figures/volume_response.png` presents the 3 studies' own effect sizes side by side, explicitly labeled as descriptive/exploratory - this is judged the more honest representation of what 3 studies can actually support, rather than manufacturing summary statistics (a pooled mean, a CI, an I²) whose apparent precision would overstate the underlying evidence.

*Last updated as part of the September 2026 comprehensive audit.*
