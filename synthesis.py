"""
Exploratory effect-size visualization: resistance training volume and
muscle hypertrophy, across the 3 studies eligible for descriptive
cross-study visualization (see analysis/comparability.py for exactly
what "eligible" means and does not mean here).

DATA SOURCE: reads data/synthesis_arms.csv (one row per within-study
volume arm), cross-checked at runtime against data/extraction_table.csv
- refuses to plot any study_id that isn't evidence_category=='A' and
comparability_to_figure=='COMPARABLE'.

WHAT "ELIGIBLE FOR EXPLORATORY VISUALIZATION" MEANS HERE - AND DOES NOT MEAN:
The 3 studies (Radaelli 2015, Heaselgrave 2019, Aube 2022) share a
common effect-size construction (within-group pre-to-post Cohen's d,
author-reported) and a common broad outcome type (muscle thickness via
imaging). This is enough to justify showing their effect sizes on one
set of axes for descriptive purposes. It is NOT enough to justify a
pooled biological effect estimate: the three measure different
anatomical sites (Radaelli: elbow flexors; Heaselgrave: biceps
specifically, itself an elbow flexor but assessed with a different
exercise selection and volume-counting approach; Aube: quadriceps, an
entirely different muscle group and body region) and represent
different training-status populations (untrained vs. two trained
samples with different screening criteria). Calling this "quantitative
comparability" without that caveat would overstate what three studies
sharing a statistical convention actually establishes biologically -
see EVIDENCE_MAP.md and README.md for the full distinction between
"statistically aligned for descriptive visualization" and "pooled
effect estimate," which this project deliberately does not compute.

WHAT "significant" MEANS IN THIS FIGURE (read before interpreting the
ns/no-ns markers): it is WITHIN-GROUP pre-to-post significance (did
this arm's participants change from their own baseline), not
between-group significance. All three studies separately report NO
significant BETWEEN-group difference across their volume arms
(Heaselgrave, Aube) or, for Radaelli, a significant between-group
difference at the highest dose specifically - none of that
between-group information is what the ns marker shows. Conflating the
two would misrepresent the dose-response question this figure is
actually about.

PSEUDOREPLICATION: 3 independent studies, 9 within-study volume arms -
not 9 independent observations. No trend line, pooled estimate, or
regression is fit across arms or studies.
"""

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
FIGURES_DIR = SCRIPT_DIR.parent / "figures"
ARMS_CSV = DATA_DIR / "synthesis_arms.csv"
EXTRACTION_CSV = DATA_DIR / "extraction_table.csv"

COLORS = {"P01_Radaelli2015": "#6b7280", "P02_Heaselgrave2019": "#c53030", "P03_Aube2022": "#2b6cb0"}
MARKERS = {"P01_Radaelli2015": "o", "P02_Heaselgrave2019": "s", "P03_Aube2022": "^"}


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_and_verify_arms():
    arms = load_csv(ARMS_CSV)
    extraction = {r["study_id"]: r for r in load_csv(EXTRACTION_CSV)}

    for arm in arms:
        sid = arm["study_id"]
        if sid not in extraction:
            sys.exit(f"REFUSING TO PLOT: {sid} referenced in synthesis_arms.csv but missing from extraction_table.csv")
        row = extraction[sid]
        if row.get("evidence_category", "").strip() != "A":
            sys.exit(f"REFUSING TO PLOT: {sid} has evidence_category='{row.get('evidence_category')}', not 'A'")
        if row.get("comparability_to_figure", "").strip() != "COMPARABLE":
            sys.exit(f"REFUSING TO PLOT: {sid} has comparability_to_figure="
                      f"'{row.get('comparability_to_figure')}', not 'COMPARABLE'")
        if arm.get("effect_size_provenance", "").strip() != "author_reported":
            sys.exit(f"REFUSING TO PLOT: {arm['comparison_id']} has effect_size_provenance="
                      f"'{arm.get('effect_size_provenance')}', expected 'author_reported' for this figure")

    studies = {}
    for arm in arms:
        sid = arm["study_id"]
        studies.setdefault(sid, {"label": arm["study_label"], "points": []})
        studies[sid]["points"].append((
            int(arm["weekly_sets"]),
            float(arm["effect_size"]),
            arm["significant"].strip().upper() == "TRUE",
        ))
    return studies


if __name__ == "__main__":
    studies = load_and_verify_arms()
    n_studies = len(studies)
    n_arms = sum(len(d["points"]) for d in studies.values())

    print(f"Within-group pre-to-post Cohen's d for muscle hypertrophy, by study "
          f"({n_studies} studies, {n_arms} within-study arms - source: data/synthesis_arms.csv):\n")
    for sid, d in studies.items():
        print(f"{d['label']}:")
        for sets, es, sig in d["points"]:
            print(f"    {sets} weekly sets -> d={es:.2f} (within-group pre-post {'significant' if sig else 'not significant'})")
        print()

    print(
        "NOTE: no pooled or averaged trend line is computed. 'significant' above refers to "
        "within-group pre-post change, not between-group difference (see script docstring).\n"
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for sid, d in studies.items():
        xs = [p[0] for p in d["points"]]
        ys = [p[1] for p in d["points"]]
        ax.plot(xs, ys, marker=MARKERS.get(sid, "o"), color=COLORS.get(sid, "#333333"),
                 label=d["label"], linewidth=1.5, markersize=9)
        for x, y, sig in d["points"]:
            if not sig:
                ax.annotate("ns", (x, y), textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center")

    ax.set_xlabel("Nominal weekly sets (study-specific definition)")
    ax.set_ylabel("Within-group pre-to-post effect size (Cohen's d)")
    ax.set_title("Training Volume and Muscle Hypertrophy: Exploratory Effect-Size Visualization", fontsize=12)
    fig.text(0.5, 0.925,
              f"{n_studies} studies, {n_arms} within-study volume arms — descriptive visualization only, not a formal meta-analysis.\n"
              "Weekly-set definitions and measured muscle differ between studies. 'ns' = not significant within-group pre-post.",
              ha="center", fontsize=8, style="italic")
    ax.legend(loc="upper left", fontsize=8)
    ax.axhline(0, color="black", linewidth=0.6)
    plt.tight_layout(rect=[0, 0, 1, 0.90])

    FIGURES_DIR.mkdir(exist_ok=True)
    out_path = FIGURES_DIR / "volume_response.png"
    plt.savefig(out_path, dpi=150)
    print(f"Figure saved to {out_path}")
