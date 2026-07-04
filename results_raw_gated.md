# Raw findings from the gated structured detectors (verbatim)

Two cold instances, blind, no file access. GATE #1 applied the relevance gate
globally; GATE #2 scoped the gate to completeness items only and explicitly
forbade suppressing structural risks.

## GATE #1 (global gate)

PLAN P1-research-market:
- [s1,s2] (medium) s1 and s2 both cover vendors/pricing with no partition, so the join may silently collapse divergent vendor/pricing figures into one unreconciled briefing.
- [s1,s2,s3] (medium) The task's explicit "2024 onward only" temporal constraint is carried by no subtask, risking inclusion of stale pre-2024 data.

PLAN P2-research-policy:
- [s5] (high) The verify node must check numeric claims but the findings schema has no provenance/source field, so claims cannot be traced or verified despite "with sources" being required.
- [s5] (medium) Findings schema lacks confidence/gap fields though impacts are estimates the join must weight and reconcile across countries.

PLAN P3-coding-refactor:
- [s1,s2] (high) The REST-to-gRPC contract is shared between api and client but no subtask owns it, so s1 and s2 run concurrently against divergent interface assumptions and will fail to integrate.
- [s3] (medium) Tests are updated for gRPC concurrently with the implementation it must test, a latent dependency that can encode the wrong contract.
- [s1,s2,s3] (medium) The "keep public behaviour identical" and "do not change database schema" constraints are not carried into any subtask's scope.

PLAN P4-research-news:
- [orchestrator] (high) Follow-up is enabled to spawn more subagents on any gap with no global budget or max-depth, risking unbounded spawning.
- [s1] (medium) "Yesterday" is unresolved to a concrete date before the parallel gatherers run, so s2/s3 may scope the wrong event.

PLAN P5-research-wellformed:
- (no significant issues found)

PLAN P6-coding-needle:
- [s1,s2] (high) s1 must implement middleware using the config's keys/windows/defaults, but s2 defines that config schema concurrently, a latent cross-dependency that can produce mismatched field names.

## GATE #2 (gate scoped to completeness items; structural risks never suppressed)

PLAN P1-research-market:
- [s1,s2] (medium) s1 (vendors/products/pricing) and s2 (market share/pricing/vendors) have heavily overlapping scope on vendors and pricing, risking duplicated and possibly contradictory work.
- [s1,s2,s3] (medium) The task restricts scope to "2024 onward only," but no subtask carries this temporal constraint, so out-of-window data may enter the briefing.
- [s4] (medium) The join concatenates-then-rewrites three summaries with no provenance or conflict-handling, so contradictory vendor/pricing figures from s1 and s2 can be silently merged.

PLAN P2-research-policy:
- [s5] (medium) The verify node must check numeric claims but upstream findings schemas carry no provenance/source fields, leaving verification with nothing to check against.
- [s5] (medium) The same node both verifies all claims and composes the assessment, so verification is not independent of the author it should scrutinise.
- [s2,s3,s4] (medium) Per-country estimates rely on the tax mechanism (s1) yet run in the same parallel group, a latent dependency that may produce estimates inconsistent with the actual tax design.

PLAN P3-coding-refactor:
- [s1,s2] (high) Converting api to gRPC and client to call gRPC concurrently with no shared service/proto contract risks an interface mismatch (latent cross-dependency run in parallel).
- [s1,s2,s3] (medium) The explicit constraints "keep public behaviour identical" and "do not change the database schema" are not carried into any subtask scope.
- [s4] (medium) The join only merges diffs and runs the build with no behavioural/equivalence check, so silently divergent api/client contracts can pass if the build compiles.

PLAN P4-research-news:
- [s5/follow_up] (high) Follow-up is "spawn more subagents on any gap synthesis finds" with no max-depth or token cap, allowing runaway recursive spawning.
- [s1] (medium) Spawning a single-fact date lookup as its own subagent is an inappropriately trivial atomic task for a dedicated subagent.
- [s4] (medium) The merge collapses official, press, and social notes with no provenance or conflict surfacing, so disagreements about what happened are silently flattened.

PLAN P5-research-wellformed:
- (no significant issues found)

PLAN P6-coding-needle:
- [s1,s2] (high) s1 must implement middleware "using the limits in the config module" that s2 defines concurrently, a latent dependency run in parallel without a shared config contract.
- [s1,s2,s3] (medium) The explicit "backward compatible" constraint is not carried into any subtask's scope.
