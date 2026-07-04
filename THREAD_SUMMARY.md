# NET-HARMS applied to agentic AI — discussion summary

*A distilled summary of a working session exploring whether the NET-HARMS
systems-thinking risk method (or the NET-HARMS Studio app) could be adapted to
improve agentic AI architectures. Written to be self-contained for a reader who
wasn't in the thread. June 2026.*

---

## 1. Starting point

**NET-HARMS** (Networked Hazard Analysis and Risk Management System; Dallat,
Salmon & Goode, 2018) is a systems-thinking risk-assessment method for
safety-critical human work systems. Its two moves:

- **Stage 1 — Task risks.** Describe the whole work system as a Hierarchical Task
  Analysis (HTA); take each bottom-level task and test it against a small
  taxonomy of "risk modes" (Task, Communication, Environment).
- **Stage 2 — Emergent risks.** Build a *task network* (nodes = tasks, links =
  dependencies), and at each link ask: *if this upstream task risk is not
  controlled, what new risk emerges at the downstream task?* This is the method's
  distinctive contribution — risk that arises from the **interaction** of tasks,
  not from any task alone.

**The intuition tested:** modern "agentic" AI often uses an orchestrator ("lead")
agent that decomposes a job, spawns parallel worker sub-agents, and synthesises
their outputs. These systems fail characteristically *at the seams* — workers
overlap, one silently depends on another, the synthesis step buries conflicting
answers. Those are emergent, interaction failures — exactly NET-HARMS' Stage 2
target. So: could an orchestrator run a lightweight NET-HARMS-style **pre-flight
check over its own plan before executing**, to surface these failures early?

## 2. Key argument: the value is in Stage 2, not the HTA

Basic task decomposition (Stage 1 / HTA) is something capable LLMs already do
adequately, and it overlaps with existing methods (FMEA, MAST failure taxonomies).
The genuinely differentiating, defensible claim is the **systems-science** one:

> Agent-coordination failures are *emergent phenomena* best surfaced by analysing
> the **coupling between tasks**, not by inspecting tasks one at a time.

Ordinary "what could go wrong?" review catches problems visible *within* a single
task but systematically misses the ones that only appear when you look at how
tasks are *wired together*. The network/interaction view catches those. This is
the part that carried every positive result.

**Landscape check (informal):** no one appears to be applying a systems-thinking,
emergent-risk lens as a *runtime pre-flight check* for agent workflows. Adjacent
work exists — empirical multi-agent failure taxonomies (e.g. "Why Do Multi-Agent
LLM Systems Fail?", MAST, ~14 failure modes; ~37% inter-agent misalignment, ~42%
spec/design), STPA applied to AI, industry reports of orchestrator-worker failure
(e.g. Anthropic's multi-agent research system) — but the bridge is open.

## 3. The task-network structure that was sketched

A reusable HTA template for the **orchestrator-worker** pattern (domain-neutral so
it adapts to research, coding, data tasks):

```
0  Complete a task via an orchestrated multi-agent workflow
├─ 1  Interpret task & set scope   (parse intent; set breadth/depth & stop rule; decide if multi-agent warranted)
├─ 2  Decompose into subtasks      (partition; define each worker's objective & boundaries; allocate budget)
├─ 3  Delegate                     (write delegation prompt; propagate shared context/constraints; spawn)
├─ 4  Worker execution (×N parallel)(plan; call tools; evaluate; produce result + provenance; report gaps/confidence; return)
├─ 5  Synthesize                   (collect; reconcile overlaps & conflicts; detect gaps/decide follow-ups; compose)
└─ 6  Review & return              (verify against provenance; check fit to task; return)
```

### The risk taxonomy (NET-HARMS modes → agentic examples)

- **T (Task):** T2 omitted (a needed subtask never spawned); T3 inadequate
  (overlapping/duplicated scope); T5 inappropriate (multi-agent used for a trivial
  step, or wrong decomposition axis).
- **C (Communication) — the highest-value group:** C1 constraint not propagated;
  C2 wrong info (delegation misstates the goal → worker drifts); C3 inadequate
  (vague objective; or output lacks provenance/confidence); C4 mistimed.
- **E (Environment):** E1 (tool/API failure, rate limits, stale data).

### The emergent-risk "patterns" (Stage 2 — the payoff)

These attach to **structural features** of the task network, not to specific task
wording — which is important (see §6):

- **silent-conflict-collapse** — a JOIN/synthesis node consumes ≥2 overlapping
  workers and quietly merges disagreements into a confident wrong answer.
- **latent-parallel-dependency** — worker B needs worker A's output, but they run
  concurrently, so B works blind.
- **coverage-hole-masking** — each worker succeeds in its scope, so a missing
  subtopic leaves a silent gap in an authoritative-looking output.
- **runaway-follow-up-loop** — adaptive gap-chasing with no global budget/depth.
- **provenance-starved-verification** — a verify step exists but upstream gives it
  nothing to check against (fails open / hallucinates a citation).
- **correlated-resource-failure** — many parallel workers hit the same rate-limited
  resource; "couldn't run" is read as "found nothing".

## 4. What was tested (Pathway C — a small proof-of-concept)

Built 6 realistic orchestrator "plans" (research + coding), planted known,
catalogued failures plus clean **control** plans, and compared two review
conditions on the *same blind plans*: **freeform** ("what could go wrong?") vs a
**structured** NET-HARMS pass (taxonomy sweep + topology pass). Scored on recall
(share of planted failures caught), precision (share of flags that were real), and
a by-stage split (task vs emergent).

### Results (capable model = Claude, blind detectors, corrected ground truth)

| Condition | Recall | Precision |
|---|---|---|
| Freeform review | 62% | 100% |
| Structured NET-HARMS pass (tuned) | **88%** | **100%** |

- The structured pass beat freeform by ~+25 points of recall **at equal, perfect
  precision**, and its advantage concentrated on the **emergent/interaction**
  failures freeform missed.
- **Gating finding:** an early structured prompt over-flagged minor "completeness"
  issues (missing provenance/confidence) everywhere. A blanket "be conservative"
  fix *over-corrected* — it also silenced real structural risks, collapsing recall
  to freeform's level. The working fix: **apply the relevance gate only to the
  completeness checks; never suppress the structural/interaction checks.** That
  restored 88%/100%.

### Model-dependence (important negative result)

Re-run on a small local model (**llama3.1:8b** via Ollama), with careful hand-
mapping to separate detection quality from scoring artefacts:

| Detector | Condition | Recall | Precision |
|---|---|---|---|
| llama3.1:8b | freeform | ~19% | ~60% |
| llama3.1:8b | structured | ~19% | ~21% |

On the small model the structured pass was **no better than freeform and worse on
precision** — it produced confident misfires (flagging provenance on code,
inventing dependencies on the clean control, contradicting itself). The method's
value **does not transfer down to an 8B-class model** with this prompt.

## 5. Methodological cautions surfaced (useful for the paper)

- The self-run pilot **overstated** the effect (it showed ~+44 pts); the blind,
  independent re-run shrank it to ~+25 and exposed a real precision cost. Self-
  scoring inflates.
- **Ground-truth labelling is the bottleneck.** A blind detector surfaced real
  issues the label author had missed — encouraging (the method finds genuine
  problems) but a caution (hand-built labels understate precision; needs a second
  labeller).
- Using the **same weak model to map free-text findings onto the taxonomy**
  corrupts scores in both directions. Use a strong/separate mapper, or have the
  detector emit structured labels directly.
- N is tiny (6 plans, single runs). "Promising signal," not "established."

## 6. Where NET-HARMS DOES stretch to agentic systems

- **The emergent/Stage-2 lens transfers well.** The taxonomy — especially the
  Communication modes — maps cleanly onto inter-agent failures, and the topology
  patterns catch exactly the silent, expensive failures ordinary review misses.
- **The orchestrator's plan is a ready-made HTA.** Unlike human work systems where
  the HTA is a fallible human model, an agent orchestrator *emits* its decomposition
  at runtime — so the analysis can operate on the system's own ground-truth plan.
- **A bad plan becomes an analysis target, not garbage-in.** Stage-1 checks
  (overlap, omission) are designed to flag exactly the decomposition flaws that
  would otherwise poison the analysis — so the method audits the plan rather than
  trusting it.
- **Keying risks off topology (not task wording) is robust.** The most valuable
  patterns fire on structure (a join, a fan-out, a parallel dependency), which
  survives sloppy labels — a partial answer to the "quality is hostage to the HTA"
  worry.
- **It's lightweight by design** (vs STPA/FRAM), which is what makes an in-loop
  runtime check plausible.

## 7. Where it does NOT (yet) stretch

- **Needs a capable model.** On a small local model the benefit vanished and the
  structured prompt backfired. "Cheap local guardrail" is unsupported.
- **Pairwise, not fully systemic.** NET-HARMS' "emergent" is pairwise interaction
  over known links; genuine multi-way effects and feedback loops exceed it (STPA/
  FRAM handle control loops better). Its network view is a coupling graph, not a
  full dynamical-systems model.
- **Reflexivity risk.** The pre-mortem is itself an LLM call subject to the failure
  modes it hunts; a shallow check yields false assurance.
- **Blind spots observed.** Vague-objective (C3) and coverage-hole detection were
  weak/inconsistent even on the capable model.
- **Detection ≠ improvement.** We measured whether it *spots* problems, not whether
  *acting* on the warnings improves real outcomes — the claim that ultimately
  matters is untested.
- **Absorption risk.** Fast-moving field; better base models may reduce the need
  for an explicit check.

## 8. Overall conclusion

The original intuition holds in a **qualified** form: a systems-thinking,
interaction-focused pre-flight check **does** add real value over ordinary review
on a capable model, concentrated exactly where systems science predicts (the
seams between parallel agents). It is **not** a universal drop-in — it depends on
a capable model, it's pairwise rather than fully systemic, and the effect is shown
only at small scale for *detection*, not yet for improved outcomes.

The distinctive, defensible contribution is the **systems-science reframing**:
treating agent-coordination failure as emergent and analysing task coupling. The
right near-term vehicle is **not** the existing human-facing app and **not** a
full new platform, but (a) a validated public benchmark + reference implementation
of "between-the-agents" risk, from which (b) a lightweight runtime check ("a lint
for agent plans") or a framework add-on can follow.

## 9. Open questions / next steps

1. **Validation study:** expand 6 → ~30 real plans, second labeller, 2–3 capable
   models, repeats for variance. Publish the benchmark.
2. **Small-model prompt variant:** can a much shorter, one-mode-at-a-time prompt
   (with the detector emitting labels directly) lift small-model performance?
3. **Detection → remediation:** does acting on flags actually reduce end-task
   failure/cost? (The real value test.)
4. **Extend beyond pairwise:** can feedback loops / n-way interactions be
   represented without losing the method's lightness?

---

*Artefacts from this work (available separately): a concept note, a collaborator/
funder brief, a pathways-compared sheet, the test corpus + failure catalogue, the
scoring harness, and full per-model results.*
