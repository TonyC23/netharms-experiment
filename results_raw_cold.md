# Raw findings from the cold-instance detectors (verbatim)

Two independent fresh agent instances, blind to ground truth, no file access
(plans embedded in their prompts). Reproduced here so the free-text -> catalogue-ID
mapping in results_*.json can be audited.

## Condition A — freeform (cold instance)

PLAN P1-research-market:
- [s1,s2] Vendor and pricing scope overlaps between s1 and s2, causing duplicated/conflicting research and wasted budget.
- [s1,s2,s3] No subtask enforces the "2024 onward only" temporal constraint from the task, so the briefing may include stale pre-2024 data.
- [s4] Synthesis is pure concatenate-and-rewrite with no verification or conflict reconciliation, so contradictory pricing/share figures between s1 and s2 pass through unresolved.
- [s1,s2,s3] No subtask covers competitive positioning/differentiation explicitly, yet the task asks for a "competitive landscape" briefing; coverage may be thin on rivalry dynamics.

PLAN P2-research-policy:
- [s2,s3,s4] Country-impact subtasks run in parallel_group 1 alongside s1 but depend conceptually on s1's tax mechanism/scope definition, so they may estimate impacts against mismatched or invented tax assumptions.
- [s2,s3,s4] Each country subtask independently defines "covered sectors," risking inconsistent scope across countries and non-comparable estimates.
- [s5] Verifier must check numeric claims but is given no independent source access or methodology, so verification may be superficial.
- [s5] The task requires sources, but s2-s4 output_schema ("findings") has no explicit source/citation field, risking unsourced numbers.

PLAN P3-coding-refactor:
- [s1,s2] A REST-to-gRPC migration requires a shared .proto/interface contract, but no subtask defines it and s1/s2 run in parallel, so api and client will diverge on service definitions.
- [s1,s2,s3] Strict scope_out isolation prevents any subtask from establishing the shared contract or seeing each other's signatures, near-guaranteeing merge/compile failures.
- [s4] Synthesis only merges diffs and runs the build with no remediation loop, so any build failure leaves the task incomplete with follow_up disabled.
- [s1,s2,s3] Independently edited diffs on interdependent packages risk textual merge conflicts and broken cross-package references.
- [s3] Tests are updated in parallel with the code rather than after, so they encode assumptions that may not match the final api/client implementations.

PLAN P4-research-news:
- [s1,s2,s3] The task assumes "yesterday's" event but no subtask verifies the event actually occurred yesterday/at all before others gather coverage.
- [s2,s3] No date/event-identity filter is passed to s2 and s3, so press and social gathering may pull the wrong launch or stale events.
- [s3] Social/community reaction is unverified and unweighted, risking rumor/noise being merged into the summary as fact.
- [s4] "Synthesis judges coverage complete" plus unbounded follow-up has no token cap or depth limit, risking runaway spawning and budget exhaustion.

PLAN P5-research-wellformed:
- (no significant issues found)

PLAN P6-coding-needle:
- [s1,s2] s1 must implement middleware "using the limits in the config module" but is scoped out of config values and runs in parallel with s2 which defines that schema, so s1 codes against an unknown/guessed config interface.
- [s4] Synthesis runs build+tests but has no remediation step and follow_up is disabled, so an integration failure ends in a failed, incomplete result.
- [s1,s2,s3] No subtask owns the shared config key/field names contract, so middleware, config schema, and docs may reference inconsistent setting names.

## Condition B — structured NET-HARMS (cold instance)

PLAN P1-research-market:
- [s1,s2,s3] output_schema is bare "summary" with no provenance/citation fields, so the briefing cannot be sourced or audited.
- [s1,s2,s3] no confidence/gap fields, so coverage holes are indistinguishable from genuine absence.
- [s1,s2,s3] the top-level "2024 onward only" date constraint is not propagated to any subtask scope.
- [s1,s2] scope overlap (both cover vendors/pricing) can produce divergent figures that the join silently collapses.
- [s4] synthesis_strategy just concatenates and rewrites with no conflict reconciliation.
- [s4] no coverage reconciliation against the original "competitive landscape" task, so missing subtopics go unnoticed.

PLAN P2-research-policy:
- [s2,s3,s4] each country estimate omits the s1 tax-mechanism context, yet all four run in parallel_group 1 so s2-s4 cannot use s1's design output (latent dependency run concurrently).
- [s2,s3,s4] output_schema "findings" has no source/citation field, yet the task requires "with sources" and s5 must verify.
- [s5] verify node must check numeric claims but upstream schema provides no provenance, so verification has nothing to check against.
- [s2,s3,s4] no confidence/gap fields to distinguish a confident estimate from a guess.

PLAN P3-coding-refactor:
- [s1,s2,s3] client and tests depend on the api package's new gRPC contract, but all three run in parallel_group 1 with no shared interface.
- [s1] the "keep public behaviour identical" constraint is not propagated to any subtask scope.
- [s1,s2,s3] the "do not change the database schema" constraint is not propagated to subtasks.
- [s4] merge-and-build join has no behavioural/contract reconciliation; mismatches surface only as a build failure with no diagnosis path.
- [s1,s2,s3] output_schema "diff" lacks any confidence/assumption field.

PLAN P4-research-news:
- [s4] follow-up "spawn more subagents on any gap" has no global budget or max-depth (only a loose 300k cap; stop_criteria is subjective "coverage complete").
- [s1,s2,s3] output_schema "note" has no source/provenance field for a recency task where attribution matters.
- [s1,s2,s3] no confidence/gap fields, so "found nothing" is indistinguishable from "couldn't run".
- [s2,s3] press and social coverage overlap and may conflict; the merge does no conflict handling.
- [s4] no reconciliation of merged notes against the original "what happened" scope.

PLAN P5-research-wellformed:
- (no significant issues found)

PLAN P6-coding-needle:
- [s1,s2] the middleware (s1) must use the config module's keys/windows/defaults, but s2 defines that schema and both run in parallel_group 1 (latent dependency run concurrently).
- [s1,s2,s3] the "keep changes backward compatible" constraint is not propagated to any subtask scope.
