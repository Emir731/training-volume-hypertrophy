# Systematic Search Log (Phase 2)

**Distinct from the earlier citation-chasing phase** (documented in `data/screening_log.csv` records R001-R020), which is NOT relabeled as a systematic search here or anywhere else in this repository.

## A critical, honest limitation (read first)

This project's tools include a general-purpose web search function, not direct API or institutional access to PubMed/MEDLINE, Scopus, Web of Science, or SPORTDiscus. This means:

- **PubMed/MEDLINE**: searched via web queries constructed to approximate PubMed's own interface and indexing. Real PubMed records (with real PMIDs) were retrieved and read. **However, this project cannot produce a true, exact "total records retrieved" count the way a logged-in PubMed session or API call would** (e.g., "your search returned 347 results") - only the records that surfaced within the search tool's results are known, not the full universe of matches. This is disclosed as a real methodological limitation, not glossed over.
- **Google Scholar**: same limitation - queried via general web search, not Google Scholar's own interface directly.
- **Scopus, Web of Science, SPORTDiscus: NOT ACCESSED AT ALL.** No institutional login or API access is available to this project. Zero records from these databases.

**Consequence:** the counts in section C below are **records this project actually observed and can cite**, not a database-verified exhaustive count. Treat them as a documented lower bound, not a true total.

## Search Strategy

**Research question (unchanged):** What is the relationship between resistance-training volume and skeletal muscle hypertrophy, and does training status modify this relationship?

**Concept blocks used:**
1. (resistance training OR strength training OR weight training)
2. (training volume OR weekly sets OR sets per week OR set volume)
3. (hypertrophy OR muscle hypertrophy OR muscle thickness OR cross-sectional area OR lean mass)

**Exact queries executed this round (all via the search tool, dates as run):**
- `"resistance training" "training volume" hypertrophy` (approximating PubMed search)
- `"weekly sets" "muscle hypertrophy" resistance trained randomized controlled trial 2023 2024 2025`
- (from the prior citation-chasing phase, retained for continuity, not re-labeled as this phase's own: various author-specific and topic-specific queries logged in `data/screening_log.csv`)

**Search date:** search queries for this phase were run during the current session (September 2026). No specific date-range filter was applied to the queries themselves; results were not restricted by publication date.

**Language limits:** none applied (English-language bias likely, since the search tool itself is English-oriented, but not an explicit filter).

**Filters:** none available - the search tool does not support PubMed-style filters (publication type, species, age group, etc.) directly.

## Inclusion Criteria (formalized this round)

- Human adults (≥18 years)
- A resistance-training intervention
- At least two volume conditions compared, OR a meaningful within-subject volume manipulation
- A hypertrophy-related outcome (muscle thickness, CSA, lean/fat-free mass via imaging - NOT strength/performance alone)
- Sufficient reported information to classify the volume exposure (sets/session, sessions/week, or an equivalent)
- Intervention duration ≥6 weeks (matches the threshold used by Baz-Valle et al. 2022, a directly comparable existing systematic review - see below)

## Exclusion Criteria

- Adolescents/youth populations
- Acute (single-session) studies only, no chronic training intervention
- Strength/performance-only outcomes with no hypertrophy measure (e.g., Marshall et al. 2011 - excluded on this basis, see extraction_table.csv R019)
- Studies where volume is held constant/equated rather than manipulated (e.g., a periodization study comparing volume-equated programs - excluded, see notes below)
- Studies retracted or under serious, specifically-documented data-integrity critique (Barbalho et al., both papers - excluded, categories E/F)

## An important methodological finding from this search phase

Two existing, real, rigorously-executed systematic reviews already cover large parts of this exact question, with real documented PRISMA numbers (read directly from their own full text, not estimated by this project):

- **Baz-Valle et al. (2022)** searched PubMed + Scopus + Cochrane Library in **January 2021**, restricted to resistance-trained individuals aged 18-35 with ≥1 year experience (almost exactly this project's own population of interest). They screened **2,083 records → 7 met inclusion criteria → 6 usable for quantitative synthesis.**
- **Pelland et al. (2025/26)** searched (databases and exact strings not fully extracted by this project) through **April 2023**, broader population. They screened **6,515 records (post-duplicate-removal) → 135 after title/abstract screening → 67 included.**

**This is important, real context for interpreting this project's own numbers**: a properly-resourced, institutionally-supported systematic review restricted to the *same narrow population this project cares about* (resistance-trained, Baz-Valle's criteria) found only 6-7 usable studies as of January 2021. This project's own dataset (6 studies with real primary data across categories A and B, as of this round) is of a **similar order of magnitude**, not a poor showing by comparison - it suggests this literature genuinely is this small for the trained-only population, not that this project's search was unusually incomplete.

**Given this, this project's own search value-add is concentrated in two places, not in re-finding what Baz-Valle/Pelland already systematically found:**
1. Checking for studies published **after** Baz-Valle's Jan 2021 cutoff and Pelland's April 2023 cutoff (this is where Aube 2022, Schoenfeld 2019 [predates but may not have met Baz-Valle's exact criteria], de Camargo 2026, Enes 2024/2025, Moreno 2024, Barsuhn 2025, Rantila 2026 all sit).
2. The primary-source verification, effect-size-formula investigation, and data-integrity screening work this project has done on the studies it did find - which is real, additive methodological value distinct from "finding more studies."

## Records Retrieved This Round (real, observed - not a database total)

| # | Citation (short) | PMID | Action |
|---|---|---|---|
| 1 | de Camargo et al. - now possibly PubMed-indexed | 42461790 | Status check needed - see extraction_table.csv notes for P08; possible preprint→published upgrade, NOT YET CONFIRMED |
| 2 | Nascimento de Oliveira Jr et al. 2022 | 32569127 | INCLUDED - added as R021 (different population: postmenopausal women) |
| 3 | Figueiredo et al. (volume-equating methods paper) | 33826122 | EXCLUDED - not a primary intervention trial |
| 4 | "Are more sets really better than less?" (review) | 29024332 | EXCLUDED - itself a review, not a primary trial |
| 5 | Higher RT volume offsets hypertrophy nonresponsiveness | 38174375 | INCLUDED - added as R022 (different population: older non-responders) |
| 6 | Baz-Valle et al. 2022 (systematic review) | 35291645 | INCLUDED as a benchmark (M03) - not a primary study |
| 7 | Periodization SR+MA (volume-equated) | 35044672 | EXCLUDED - volume not manipulated (equated by design) |
| 8 | Pelland et al. 2025/26 (already known) | 41343037 | Citation/PMID updated in M02 |
| 9 | Training-to-failure meta-analysis (different topic) | 33497853 | EXCLUDED - wrong research question (failure/RIR, not volume) |
| 10 | 151-RCT older-adults network meta-analysis | 39405023 | NOTED, not integrated - different population (≥60y specifically) |

**10 records observed and screened this round. 3 included (1 as a new primary study category C x2, 1 as a benchmark). 5 excluded with reasons stated. 1 flagged for status verification. 1 noted but not integrated (population mismatch).**

## PRISMA-style flow (this project's own numbers only - real, not estimated)

```
Records identified via this project's own search activity (all phases, this project's own tool-based searches):
  - Phase 1 (citation-chasing, R001-R020): 20 records logged
  - Phase 2 (this round's documented queries): 10 records observed
  = 30 total records logged in data/screening_log.csv + this document

Duplicates: 0 formally identified as exact duplicates across phases (no record appeared under
  two different record_ids) - NOT independently deduplication-audited beyond this project's own
  manual tracking; a formal duplicate-check step (e.g., by DOI) has not been run as a separate
  validation pass.

Excluded at title/abstract level (this round): 5 (see table above)
Excluded at full-text level: 0 this round (none of the 10 records reached a full-text
  screening step distinct from abstract-level screening in this project's process)

Included (all phases, all categories A through G, excluding pure benchmarks/reviews):
  17 primary study rows in data/extraction_table.csv (22 total rows minus 3 aggregate
  benchmarks/reviews minus 2 excluded-outright rows [Barbalho men retracted is still a row,
  Marshall is excluded-outcome-mismatch but kept as a row for transparency])
```

This is NOT a PRISMA diagram with identified/duplicates/screened/full-text/included boxes and exact universal counts, because a true database export was never obtained. This table is the honest substitute: what this project can actually claim to have done, with real numbers.

*Last updated: September 2026, alongside the systematic search design phase.*
