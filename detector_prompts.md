# Detector prompts

Both conditions receive the **same** plan object with `ground_truth` and
`ground_truth_notes` stripped. The only difference is the instruction. The
freeform prompt is written as a strong, fair baseline — not a strawman — so any
delta reflects the *structure*, not effort.

## Condition A — freeform (strong baseline)

> You are a senior engineer reviewing a multi-agent orchestration plan before it
> executes. The plan decomposes a task into subtasks, some run in parallel
> (same `parallel_group`), and a join subtask synthesises the results.
> Think carefully and list everything that could go wrong with this plan —
> design flaws, risks, things that will produce a bad or unreliable result.
> Be specific and reference subtask IDs. Be thorough.

## Condition B — structured (NET-HARMS pass)

> You are reviewing a multi-agent orchestration plan before it executes, using
> the NET-HARMS method.
>
> STAGE 1 — for each subtask, check it against the risk modes:
> T1 mistimed, T2 omitted, T3 inadequate, T4 inadequate object, T5 inappropriate,
> C1 not communicated, C2 wrong info, C3 inadequate info, C4 mistimed comms,
> E1 adverse environment. Also check each subagent `output_schema` for missing
> provenance and missing confidence/gap fields.
>
> STAGE 2 — topology pass. Detect these structural features and apply the
> matching check:
> - JOIN node (a subtask consuming >=2 others): could overlapping inputs
>   disagree and be silently collapsed? (silent-conflict-collapse)
> - FAN-OUT with a shared partition: is any subtopic missing, or is delivered
>   coverage never reconciled vs the task? (coverage-hole-masking)
> - PARALLEL pair where one needs another's output: latent dependency run
>   concurrently? (latent-parallel-dependency)
> - VERIFY node: does upstream actually provide what it needs to verify?
>   (provenance-starved-verification)
> - ADAPTIVE follow-up: is there a global budget / max-depth? (runaway loop)
> - SHARED external resource across parallel subagents: correlated failure /
>   can the schema tell "couldn't run" from "found nothing"? (correlated-failure)
>
> List each risk found, referencing subtask IDs and the mode/pattern. Only flag
> risks that are actually present — do not invent issues to fill the checklist.

## Output format (both conditions)

A list of findings. Each finding is mapped (in scoring) to at most one
catalogue ID, or to `OTHER` if it's a real-but-uncatalogued observation, or
discarded as a false positive if it asserts a problem that isn't present.
