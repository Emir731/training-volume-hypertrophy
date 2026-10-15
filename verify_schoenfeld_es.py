"""
Investigates which formula Schoenfeld et al. (2019) likely used to compute
their reported elbow-extensor (triceps) effect sizes (0.12 / 0.30 / 0.55
for 1SET / 3SET / 5SET), using the raw pre-training SDs and mean change
values read directly from their Table 1 (see data/extraction_table.csv,
study_id P04_Schoenfeld2019).

This does NOT replace the authors' reported ES. It documents a
mathematical investigation into how it was likely computed, so that
future work can decide whether/how to compute a comparable ES for the
other 3 outcomes (biceps, rectus femoris, vastus lateralis) that the
authors did not report an ES for directly.
"""

triceps_baseline_sd = {"1SET": 4.5, "3SET": 6.2, "5SET": 3.5}
triceps_delta_mean = {"1SET": 0.6, "3SET": 1.4, "5SET": 2.6}
triceps_delta_sd = {"1SET": 2.0, "3SET": 3.1, "5SET": 2.3}
reported_ES = {"1SET": 0.12, "3SET": 0.30, "5SET": 0.55}

if __name__ == "__main__":
    avg_baseline_sd = sum(triceps_baseline_sd.values()) / 3
    n = {"1SET": 11, "3SET": 11, "5SET": 11}  # triceps n after 1 exclusion in 3SET, per text
    pooled_sd = (
        sum((n[g] - 1) * triceps_baseline_sd[g] ** 2 for g in n) / (sum(n.values()) - len(n))
    ) ** 0.5

    print("Hypothesis 1: ES = delta_mean / (simple average of 3 groups' baseline SD)")
    print(f"  avg baseline SD = {avg_baseline_sd:.3f}")
    for g in ["1SET", "3SET", "5SET"]:
        calc = triceps_delta_mean[g] / avg_baseline_sd
        print(f"    {g}: {calc:.3f} vs reported {reported_ES[g]} (diff {abs(calc - reported_ES[g]):.3f})")

    print("\nHypothesis 2: ES = delta_mean / (sample-size-weighted pooled baseline SD)")
    print(f"  pooled baseline SD = {pooled_sd:.3f}")
    for g in ["1SET", "3SET", "5SET"]:
        calc = triceps_delta_mean[g] / pooled_sd
        print(f"    {g}: {calc:.3f} vs reported {reported_ES[g]} (diff {abs(calc - reported_ES[g]):.3f})")

    print("\nHypothesis 3: ES = delta_mean / delta_SD (change-score SD, within-group)")
    for g in ["1SET", "3SET", "5SET"]:
        calc = triceps_delta_mean[g] / triceps_delta_sd[g]
        print(f"    {g}: {calc:.3f} vs reported {reported_ES[g]} (diff {abs(calc - reported_ES[g]):.3f})")

    print(
        "\nConclusion: Hypothesis 1 (simple average of baseline SDs) fits best - "
        "all 3 values within 0.01 of the authors' reported ES, essentially exact "
        "given likely rounding in the source SD values. Hypothesis 3 (the "
        "convention used to compute ES for Radaelli/Heaselgrave/Aube in this "
        "project) does NOT fit and is off by 0.15-0.58. This is a STRONG "
        "inference, not a confirmed fact - the authors' actual computation code "
        "was not available to check directly."
    )
