# DRAFT MANUSCRIPT — ONGOING SYSTEMATIC REVIEW, NOT COMPLETE

**Title:** Training Volume and Muscle Hypertrophy: A Systematic Review and Exploratory Dose-Response Analysis in Resistance-Trained Individuals

This is a draft. It has not been through a completed systematic search, and its conclusions are scoped to what 3 comparable studies and a handful of additional, less-verified sources can actually support. Canonical counts referenced below come from `analysis/canonical_counts.py` and should match `README.md` — if they don't, one of the two documents is out of date.

## Abstract

Whether more resistance-training volume keeps producing more muscle growth, or whether the relationship changes once someone is already trained, is a genuinely open question in this literature — not a settled one this project is trying to summarize, but one it ran into directly while trying to build a small, defensible dataset. Of 22 sources examined, only 5 turned out to have both full-text access and usable quantitative data, and of those 5, only 3 (Radaelli et al. 2015, Heaselgrave et al. 2019, Aube et al. 2022) share enough of a common effect-size construction and outcome type to be shown on the same axis for exploratory purposes (see `analysis/comparability.py`). Those 3 do not establish a single monotonic pattern: in an untrained sample, effect size was associated with weekly sets; in two trained samples, higher volume was not associated with a statistically significant additional increase, and in one case the pattern was not even flat — it peaked at a middle dose. Two more studies with real numbers (Schoenfeld et al. 2019, de Camargo et al. 2026) had to be left out of that comparison for a specific, checkable reason: their effect sizes are constructed differently, not just reported differently. Along the way, two candidate studies (Barbalho et al., 2019) turned out to need exclusion for reasons that had nothing to do with their results — one has been retracted, the other is the subject of a published critique alleging implausible data patterns. No pooled estimate is reported here. Three studies is not enough to pool responsibly, and the ones that would extend the dataset don't share a comparable metric without more work than this project has done yet.

## Introduction

The basic question — does more training volume mean more muscle growth — has a fairly settled answer at the population level: yes, on average, up to a point. Schoenfeld, Ogborn and Krieger's 2017 meta-analysis found a roughly linear relationship across 15 mostly untrained-to-recreational studies. A far larger and more recent Bayesian meta-regression by Pelland and colleagues (67 studies, over 2,000 participants) confirms the positive relationship but finds it bends — diminishing returns, not a straight line. What's less settled is what happens specifically in people who are already resistance-trained, where the classic meta-analyses have comparatively little data. That's the gap this project set out to look at directly, by finding and verifying primary studies conducted in trained populations rather than leaning on aggregate estimates built mostly from untrained samples.

## Research Question

**Primary:** Does resistance-training volume have a dose-response relationship with skeletal muscle hypertrophy?

**Secondary:** Does training status change the shape of that relationship?

Muscle group, session frequency, proximity to failure, and load are discussed where the data touch on them, but none of them are treated as modeled variables here — the dataset is too small and too heterogeneous in how it reports these to support that.

## Methods

### Search Strategy
Full detail, including the exact queries run and — importantly — an honest account of what this project's tools can and cannot do (no true database-level retrieval count is possible), is in `SYSTEMATIC_SEARCH.md`. In short: this was not a single, clean systematic search. It started as citation-chasing from a handful of known studies, and was later supplemented by a more deliberate search phase with documented queries and inclusion/exclusion criteria — but even that phase cannot claim database completeness. Two existing systematic reviews (Baz-Valle et al. 2022; Pelland et al. 2025/26) already cover large parts of this territory properly, and are used here as context, not folded into this project's own count.

### Evidence Classification
Every source gets exactly one label from A through I (full definitions in `data/DATA_DICTIONARY.md`), separating *how well-verified* a source is from *whether its data can be plotted alongside another source's* — those turned out to be two different questions, not one. A study can be fully verified against its own full text and still not belong in the same figure as another fully verified study, if the two compute their effect sizes differently or measure different things.

### Data Extraction
`data/extraction_table.csv`, 22 rows, one row per source, tagged with where every number came from and whether it was reported directly or calculated by this project.

### Risk of Bias
TESTEX domains were judged for the 2 studies with the most complete full-text access (Heaselgrave, Aube), partially for 2 more (Schoenfeld 2019, de Camargo 2026), and left as "insufficient information" everywhere else — not scored on a guess. Two concrete findings worth flagging: Heaselgrave's outcome assessor was explicitly *not* blinded for the muscle-thickness scans; Aube's was. Neither detail changes the direction of either study's finding, but it's the kind of thing that should be on record.

### Statistical Analysis
No pooled effect, no random-effects model, no heterogeneity statistic. `analysis/meta_analysis_eligibility.md` lays out exactly why not — mainly, too few comparable studies and only one of them (Schoenfeld 2019) provides raw means and SDs, and it's the one study that doesn't fit the comparable group. What's reported instead is a plain descriptive comparison of each study's own within-group effect size, with the comparability decision made by explicit rule (`analysis/comparability.py`) rather than by eye.

## Results

### What's actually verified
Of 22 sources: 5 are primary-verified with usable numbers, 8 are abstract-level, 2 are known only secondhand, 4 are reviews used for context, 1 was excluded outright (it measures strength, not hypertrophy), and 2 needed integrity flags. See the Canonical Counts table in `README.md` for the exact breakdown.

### The 3 comparable studies

| Study | Population | Weekly sets | Effect size (d) |
|---|---|---|---|
| Radaelli 2015 | Untrained | 6 / 18 / 30 | 0.10 (ns) / 0.73 / 1.10 |
| Heaselgrave 2019 | Resistance-trained | 9 / 18 / 27 | 0.33 / 0.66 / 0.37 |
| Aube 2022 | Highly resistance-trained | 12 / 18 / 24 | 0.43 / 0.34 / 0.31 |

The untrained sample climbs. Both trained samples don't — and neither does it cleanly plateau; Heaselgrave's middle dose outperforms its highest, and Aube's lowest dose is at least as good as its highest on most measures. That's a real pattern, not an averaging artifact — it shows up before any pooling is attempted.

### Two more real studies, deliberately excluded from that table
Schoenfeld et al. (2019) has the best raw data of anything in this dataset — full pre/post means and SDs for four muscle sites. Working through that data raised a question this project didn't expect to have to answer: why did trying to recompute the authors' own reported effect size not match, using the formula that works fine for the other three studies? Testing a few alternatives against the raw numbers (`analysis/verify_schoenfeld_es.py`) turned up a likely answer — Schoenfeld's team appears to have standardized against the *average baseline SD across all three treatment groups*, not each group's own change-score SD. That's a legitimate way to compute an effect size, just a different one, and it means Schoenfeld's numbers and Heaselgrave/Aube's numbers aren't the same kind of quantity even though they're both called "d." Squeezing them into one figure would've been misleading. And for what it's worth, Schoenfeld 2019's actual finding is the opposite of Heaselgrave/Aube's: hypertrophy scaled up with volume at three of four sites. De Camargo et al. (2026, a preprint) is excluded for a related but different reason — it measures volume relative to each participant's own habitual training rather than in absolute weekly sets, which changes what the x-axis even represents.

### A detour into data integrity
Two Barbalho et al. papers looked, from their abstracts, like they'd slot neatly into this project. They don't. A 2020 critique (Vigotsky, Nuckols, Heathers, Krieger, Schoenfeld and Steele) documented statistical patterns across this group's published work that the critique's authors describe as improbable — and the companion men's study was retracted at the authors' own request that same year. The women's study hasn't been retracted, as far as this project can confirm, but it's covered by the same critique. Neither contributes a single number to this dataset. They're kept as rows, not deleted, because pretending they were never found would be its own kind of dishonesty.

## Discussion

Three studies is a thin basis for saying anything definitive about training status as a moderator. What can be said: in the specific studies this project could verify, the trained-vs-untrained split is consistent with the idea that additional volume matters less once someone is already trained, but a fourth well-verified trained-population study (Schoenfeld 2019) does not show that pattern, and this project does not have a good, evidence-backed explanation for the disagreement — only candidate factors (how strictly "trained" was screened in each sample, how volume was counted, how long the intervention ran) that haven't been tested against each other. The available evidence is insufficient to determine whether training status systematically modifies the volume-hypertrophy dose-response relationship.

## Limitations

- No completed systematic search; database-level retrieval counts were never possible with the tools available.
- Only 3 studies are comparable enough to sit in the same figure; 2 more have real data that doesn't fit, and several more are abstract-only.
- Deduplication across search phases was never formally verified (see `QUALITY_CONTROL.md`).
- Ostrowski (1997) and Amirthalingam (2017) are known only through how another paper describes them, not through this project's own reading.
- Risk-of-bias judgments exist for only a handful of the 22 sources.

## Conclusion

The available evidence does not support a single answer to "does more volume mean more growth in trained lifters." It supports a smaller, more specific claim: in this project's own verified dataset, the pattern looks different in untrained versus trained samples, but that pattern isn't unanimous even within the trained-only evidence, and the dataset is too small to say more than that with any confidence.

## Future Research Protocol
1. Obtain full text for the 8 abstract-only sources, particularly the two Enes et al. companion studies (2024 men, 2025 women), which disagree with each other and are both currently secondhand.
2. Independently verify Ostrowski (1997) and Amirthalingam (2017) rather than relying on a narrative review's summary of them.
3. Run a formal deduplication pass across all search phases.
4. If the comparable set grows past roughly 5 studies with a reconcilable effect-size basis, revisit `analysis/meta_analysis_eligibility.md`.

## References
`references/references.bib`

---
*Prepared with AI-assisted literature search, data organization, and code; verification decisions, exclusions, and interpretation are the author's. Last updated September 2026.*
