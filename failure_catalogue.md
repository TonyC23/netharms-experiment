# Pathway-C failure catalogue

Each failure has an ID, the NET-HARMS mode/pattern it derives from, the stage
(`task` = Stage 1, single-task risk; `emergent` = Stage 2, interaction risk),
and a *detectable signature*: what a reviewer looking at the plan object alone
could point to. Ground-truth labels in the corpus use these IDs.

The `stage` split matters: the central sub-hypothesis is that a structured
taxonomy/topology pass beats freeform reflection **much more on `emergent`
failures than on `task` failures**, because freeform review can spot obvious
single-task problems but systematically misses interaction risks that require
tracing the task graph.

## Task-level (Stage 1)

| ID | Mode | Signature in the plan |
|----|------|------------------------|
| F-T2-OMIT | T2 omitted | A subtask the task plainly requires is absent from the partition. |
| F-T3-OVERLAP | T3 inadequate | Two subtasks have overlapping `scope_in` with no de-duplication. |
| F-T5-OVERKILL | T5 inappropriate | A parallel subagent spawned for a trivial/atomic step, or decomposition along the wrong axis. |
| F-C3-VAGUE | C3 inadequate | A subtask `objective` is underspecified ("research X") with no scope/success criteria. |
| F-C1-CONSTRAINT-DROP | C1 not communicated | A constraint stated in the user task is absent from every subtask context. |
| F-NOPROV | C3 inadequate | Subagent `output_schema` has no provenance/citation field. |
| F-NOCONF | T2 omitted (reporting) | Subagent `output_schema` has no confidence/gap field. |

## Emergent (Stage 2)

| ID | Pattern | Signature in the plan |
|----|---------|------------------------|
| F-CONFLICT | silent-conflict-collapse | A join/synthesis node consumes ≥2 subtasks with overlapping scope, and synthesis_strategy has no conflict-handling (merges/picks silently). |
| F-LATENTDEP | latent-parallel-dependency | Subtask B's quality depends on an output of subtask A, but A and B share a `parallel_group`. |
| F-COVHOLE | coverage-hole-masking | Synthesis composes an authoritative output with no step reconciling delivered coverage against the original task. |
| F-RUNAWAY | runaway-follow-up-loop | Adaptive follow-up spawning enabled with no global budget / max-depth stop. |
| F-PROVSTARVE | provenance-starved-verification | A verification step exists but upstream output_schema provides no provenance for it to check (fails open). |
| F-CORRELATED | correlated-resource-failure | Many parallel subagents hit the same rate-limited resource with no stagger, and the schema can't distinguish "couldn't run" from "found nothing". |

## Metrics

For each condition (freeform / structured), against ground truth:

- **Recall** = injected failures detected / injected failures present.
- **Precision** = correct detections / total flags raised (penalises over-flagging; the precision-control plans exist to measure this).
- **Recall by stage** = recall computed separately over `task` vs `emergent` failures.
- **Headline = delta**: `recall_structured - recall_freeform`, overall and by stage. The delta is the bias-robust quantity for a self-run pilot.

## Severity / relevance gating (v2)

The v1 cold run showed the structured pass over-applies completeness checks
(provenance, confidence, coverage) to plans where they aren't load-bearing. A
failure is **in-scope (load-bearing)** only if its absence would plausibly cause
a wrong, failed, wasteful, or unsafe OUTPUT for THIS task:

- **F-NOPROV** — only if the task requests sources/citations, or a downstream
  VERIFY node must check the claims. (P2 yes; P1/P4 no — sources not requested.)
- **F-NOCONF** — only if synthesis must weight/reconcile uncertain inputs
  (estimates, conflicting sources). Not for routine code diffs or single lookups.
- **F-COVHOLE** — only if the task enumerates multiple required items whose
  individual under-coverage could pass unnoticed, and no reconciliation step.
- **F-C1-CONSTRAINT-DROP** — only if the task states an explicit constraint that
  no subtask carries.
- **F-C3-VAGUE** — only if a missing success criterion permits real drift.

Structural failures (T2/T3/T5, CONFLICT, LATENTDEP, RUNAWAY, PROVSTARVE) are
load-bearing whenever structurally present. The gated structured prompt applies
this rule and reports only high/medium-severity risks.
