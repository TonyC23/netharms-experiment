# Pathway-C: model-diversity run (llama3.1:8b) + mapper disentangling

Tony ran the full pipeline on llama3.1:8b via Ollama (detector AND auto-mapper =
llama). The auto-scored numbers looked alarming and reversed the Claude result,
so the raw findings (`results_raw.json`) were hand re-mapped by a strong mapper
(Claude) to separate **detection quality** from **mapping quality**. All numbers
vs GT v2.

## All results, one table

| Detector | Mapper | Cond. | Recall | Precision |
|---|---|---|---|---|
| Claude (cold) | hand | freeform | 62% | 100% |
| Claude (cold) | hand | structured (gate #2) | **88%** | **100%** |
| llama3.1:8b | llama (auto) | freeform | 38% | 22% |
| llama3.1:8b | llama (auto) | structured | 12% | 13% |
| llama3.1:8b | Claude (hand) | freeform | 19% | 60% |
| llama3.1:8b | Claude (hand) | structured | 19% | 21% |

## What the disentangling showed

**The weak auto-mapper was corrupting the scores in both directions.** It
*fabricated hits* (e.g. it credited P1 freeform with C1-DROP and P3 freeform with
T2-OMIT/C1-DROP that llama never actually articulated) and it *fabricated false
positives* (T2-OMIT, NOPROV appeared on almost every plan). It also *missed real
catches* — on P4 structured, llama genuinely caught the press/social conflict and
the runaway loop, but the llama mapper scored that plan 0/3; the hand mapper
recovered 2/3. So the auto-pipeline was partly measuring the mapper, exactly as
suspected.

**But fixing the mapper did not rescue llama — it just clarified the picture.**
With clean (hand) mapping, llama's honest detection is ~19% recall in *both*
conditions, versus Claude's 62% / 88%. The mapper was a real confound; weak
detection is the bigger story.

**On llama, the structured pass is NOT better than freeform — if anything it's
worse.** Equal recall (19% each), but structured precision is far lower (21% vs
60%): the structured prompt induces *confident misfires* — flagging
provenance/confidence on code diffs, asserting silent-conflict on non-overlapping
joins, flagging a runaway loop while noting follow-up is disabled, and inventing a
latent dependency between independent laptops on the control plan. The extra
structure gave the 8B model more ways to be wrong, not more real catches. This is
the opposite of the Claude result, where structure added +26 points of recall at
no precision cost.

## Qualitative failure modes of the 8B detector (from the raw log)

- **Generic boilerplate instead of specific catches**: pages of "lack of error
  handling / monitoring / logging / security / scalability" that match none of the
  injected failures.
- **Talking itself out of real risks**: on P1 (4 real issues) the structured run
  worked the checklist and concluded "No risks were flagged... well-structured."
- **Misapplying the topology checks**: flagged silent-conflict and latent
  dependency on the *clean control plan* (P5) and on legitimate sequential joins.
- **Ignoring the gate**: still flagged provenance/confidence on code diffs that
  the relevance gate explicitly excludes.

## Implication for the project

Model-dependence is real and severe, and it lands on the most important design
question: **the pathway-B runtime pre-mortem cannot run on a small local model.**
On llama3.1:8b the structured NET-HARMS pass adds no recall over freeform and
worse precision, and absolute recall (~19%) is too low to be useful. The value
demonstrated on Claude does not transfer down-market with this prompt.

Practical consequences:
- If pathway B runs the pre-mortem on the orchestrator's own (frontier) model,
  the Claude results apply and it's viable. "Cheap local guardrail on an 8B" is
  not supported by this run.
- The benchmark harness must use a **strong, separate mapper** (or have the
  structured detector emit catalogue IDs directly); a same-weak-model mapper makes
  results uninterpretable.
- A small-model-friendly prompt variant (much shorter, one mode at a time, fewer
  simultaneous instructions) is an open question — this run used the full prompt,
  which an 8B clearly cannot follow.

## Caveats

N=1 llama run; single temperature. The hand mapping involved judgement calls and
was deliberately strict on vague findings (a lenient pass might give llama a few
more borderline credits, e.g. P3 LATENTDEP) — but even generously, llama would
not approach Claude's level, and structured would still not beat freeform. The
direction of the conclusion is robust to mapping leniency.
