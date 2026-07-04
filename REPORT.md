# Pathway-C pilot: does a structured NET-HARMS pass beat freeform review of an agent plan?

**Question.** Before an orchestrator spawns subagents, does running a structured
NET-HARMS pass (taxonomy sweep + topology pass) over its decomposition catch
materially more real failures than a strong freeform "what could go wrong?"
review of the same plan? This is the experiment that decides whether the
runtime pre-mortem (pathway B) is worth building.

**Design in one paragraph.** A corpus of 6 realistic orchestrator plans
(`corpus.json`) — research and coding workflows — seeded with 16 known failures
drawn from the catalogue (`failure_catalogue.md`), plus one precision-control
plan (P5, zero failures, designed to *look* risky) and one needle case (P6, a
single subtle failure in an otherwise clean plan). Two detector conditions
(`detector_prompts.md`) see the identical plan with ground truth stripped: a
strong freeform baseline, and the structured NET-HARMS pass. Scored on recall
(overall + by stage), precision, and the headline **delta**.

## Result

| | Freeform | Structured | Delta |
|---|---|---|---|
| Recall overall | 50% (8/16) | 94% (15/16) | **+44%** |
| Recall — task (Stage 1) | 50% | 88% | +38% |
| Recall — emergent (Stage 2) | 50% | 100% | **+50%** |
| Precision | 89% | 88% | −1% |
| False positives | 1 | 2 | — |

The structured pass roughly **doubled recall (50% → 94%) at essentially no
precision cost** (−1%; 2 false positives vs 1, both on the topology triggers).

## The qualitative pattern matters more than the numbers

Freeform's 50% emergent recall looks respectable, but *which* emergent risks it
caught is the real finding. Freeform caught emergent risks only when they were
**salient or domain-obvious**:

- P3 (coding): it flagged the parallel interface dependency because "you can't
  convert the client before the API interface exists" is blatant to an engineer.
- P1: it flagged the synthesis conflict *because* it had just noticed the s1/s2
  overlap — the emergent risk was adjacent to a salient task risk.
- P4: it flagged the runaway loop because cost is a salient freeform concern.

Freeform missed every emergent risk that required **pure topology reasoning with
no salient neighbour**: the same latent-dependency type it caught in P3, it
missed in P2 (buried among four parallel country agents) and in P6 (the needle in
a clean plan); plus the coverage-hole (P2) and the cross-source conflict (P4).

That is the crux. The failures freeform misses are exactly the *silent,
expensive* ones — the confidently-wrong synthesis, the buried dependency, the
unnoticed coverage gap — which is precisely the class NET-HARMS was built to
surface. The structured pass caught all of them because the topology check fires
on the *structure* (a join, a fan-out, a parallel dependency), independent of
whether the risk is salient in the prose. Same failure type, caught regardless
of disguise.

The precision control (P5) and needle (P6) behaved as designed: structured paid
its one realistic cost — a spurious conflict flag on P5 where conflict-handling
was already present (the checklist over-triggering on a JOIN node) — and earned
its keep on P6, catching the lone needle freeform walked past.

## What this pilot does and does NOT establish

**Does:** the mechanism works end to end (corpus → blind detection → scoring),
and under a same-detector comparison the structured pass shows a large recall
advantage concentrated where the value thesis predicted (silent/topological
failures), without a precision collapse. That is genuine first-read signal.

**Does not (be honest):**

1. **Ground truth and detector share an author.** I wrote the corpus, the
   labels, and ran both detection conditions. The mitigation is that the
   **delta** is the headline, not the absolute scores: my knowing the answers is
   common-mode across both conditions and largely cancels in the difference. But
   it does not cancel a "tried-harder-in-one-condition" effect, which only an
   independent run removes.
2. **N is tiny and it is a single run.** 6 plans, 16 failures, one pass. Several
   calls (notably P6, and freeform's salient-emergent catches) are genuinely
   ~50/50 and would move run to run. No confidence intervals are warranted.
3. **Detection→remediation is untested.** This measures detection only. The
   value of pathway B depends on the orchestrator *acting* on flags (re-order,
   add a verifier, tighten a prompt) and that reducing end-task failure/cost.
   That is a separate, harder experiment.
4. **No capability-absorption control.** It does not test whether a stronger
   base model would close the freeform gap on its own.

## The unbiased version (next step to harden this)

`harness.py` is built so the same scoring runs against a real, independent
detector. Implement `call_model(prompt)` against an LLM, feed it
`corpus_blind.json` with each condition's prompt, map outputs to catalogue IDs,
and re-score. To remove the remaining bias, the corpus should be (a) expanded to
~25–30 plans, (b) labelled by a second person, and ideally (c) detected by a
*different* model from any used to author it, with the ID-mapping step itself
done blind. If the delta survives that, pathway B has a real evidence base — and
the corpus + harness become the durable "emergent agent-risk benchmark" that
holds value even if runtime scaffolding later gets absorbed into base models.

## Bottom line

On this pilot, structuring the pre-spawn review around the NET-HARMS
taxonomy + a topology pass converts a coin-flip (50%) into near-complete
recall (94%) for roughly no precision cost, and the gain lands squarely on the
silent, interaction-level failures that freeform review systematically misses.
That is enough signal to justify building the unbiased benchmark and a thin
runtime prototype — and not yet enough to claim the value is proven. Lead with
the benchmark.
