# Pathway-C: does severity/relevance gating recover precision without losing recall?

Follow-up to COLD_RESULTS.md. The v1 cold run showed the structured pass
over-flagged completeness issues (provenance/confidence/coverage) on plans where
they weren't load-bearing — precision 62% (8 false positives). This round adds a
relevance gate to the structured prompt and tests two versions of it.

To isolate the gate's effect from my imperfect labels, all four conditions are
scored against a single **corrected ground truth (GT v2)**, derived from a
stated severity rule (in `failure_catalogue.md`), applied symmetrically, and
NOT altered to match any detector's output. The two corrections: P1 dropped
`F-NOCONF` (a concatenate-synthesis briefing doesn't weight inputs, so confidence
isn't load-bearing); P6 added `F-C1-CONSTRAINT-DROP` ("keep backward compatible"
is an explicit, unpropagated constraint). Both detectors are cold, blind
instances with no file access.

## Results (all on GT v2; freeform held constant)

| Condition | Recall | Precision | False positives |
|---|---|---|---|
| Freeform (baseline) | 62% | 100% | 0 |
| Structured, ungated (v1) | 81% | 62% | 8 |
| Structured, gate #1 (global gate) | 62% | 91% | 1 |
| **Structured, gate #2 (scoped gate)** | **88%** | **100%** | **0** |

## What happened

**The first gate over-corrected.** Gate #1 applied the relevance filter
globally and told the model to "report only high/medium, a well-formed plan
yields nothing." Precision jumped (62% → 91%) but recall collapsed (81% → 62%):
the gate suppressed the FPs *and* genuine structural risks — it dropped the P2
latent dependency, the P4 press/social conflict, and the P6 backward-compat
constraint. At that setting the structured pass was no better than freeform
(same 62% recall, slightly worse precision). A naive "be more conservative"
instruction throws the signal out with the noise.

**Scoping the gate fixed it.** Gate #2 changed one thing: apply the relevance
filter *only* to the five completeness items (provenance, confidence, coverage,
dropped-constraint, vague-objective) and explicitly never suppress structural
risks (omitted contract, overlap, latent dependency, silent join conflict,
runaway follow-up, starved verification). That version **dominates everything**:
recall 88% (higher even than the noisy ungated v1) at 100% precision, zero false
positives. It recovered the latent dependency, the conflict, and the
backward-compat constraint, and was the only run anywhere to catch the P4
over-decomposition (T5).

**Net vs the freeform baseline:** +25 points of recall (88% vs 62%) at identical
100% precision. This is the clean version of the result the noisy v1 run only
hinted at — and a much stronger case than the self-run pilot, because it survived
blind detection and an honest precision accounting.

## Honest caveats

1. **N=1 per variant.** Gate #1 and gate #2 differ in BOTH prompt wording and the
   random instance draw, so I can't fully attribute the recovery to the prompt
   versus run-to-run variance. The direction is strong and mechanistic (the
   scoping instruction directly targets the over-suppression), and gate #2 also
   beat the ungated run on recall — hard to explain by variance alone — but a
   clean claim needs 3–5 runs per condition.
2. **Labels still single-author.** GT v2 is corrected and rule-based, but not
   independently validated. A second labeller remains the most valuable hardening
   step; the v1 run already proved the detector finds real issues labels miss.
3. **Persistent blind spots.** Every run missed `F-C3-VAGUE` (vague objectives),
   and `F-COVHOLE` (coverage holes) is caught only intermittently. These two
   modes need dedicated prompt work; they're the method's current weak detectors.
4. **Still Claude-family.** Model diversity (the local `run_model.py` path against
   a non-Claude model) is untested and is the next external-validity check.

## Takeaway

The precision problem was real but fixable, and the fix is specific: **gate the
completeness checks, never the structural ones.** With that, a blind structured
NET-HARMS pass beat freeform review by +25 points of recall at equal, perfect
precision on this corpus — concentrated, as predicted, on interaction risks. The
value thesis for pathway B now has its first clean supporting result. The next
moves that would harden it: 3–5 repeat runs per condition for variance bars, a
second labeller, targeted prompt work on the C3/COVHOLE blind spots, and a
non-Claude detector run.
