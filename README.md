# Catching the failures *between* the agents

### A systems-thinking pre-flight check for AI agent workflows — concept note

*Draft for discussion — June 2026*
*Tony Carden tony.carden@gmail.com*

---

## In one paragraph

Modern AI systems increasingly work by having a "lead" agent break a job into
pieces and hand them to several helper agents that run at the same time, then
stitch their answers together. These systems fail in a characteristic way: not
because any single piece is wrong, but because the pieces interact badly — two
helpers do the same work, one needs something another hasn't produced yet, or the
lead quietly blends conflicting answers into a confident but wrong result. These
are *emergent* failures, the signature concern of systems science. This note
proposes adapting a validated systems-thinking risk method — NET-HARMS, developed
for safety-critical human work systems — into a fast automatic "pre-flight check"
that an AI runs over its own plan before it acts, to surface these between-the-
pieces failures early. A small proof-of-concept is encouraging: on a capable AI
model, the structured check caught noticeably more planted failures than ordinary
review, and specifically the interaction failures that ordinary review misses. The
purpose of this note is to describe the idea, share the early evidence honestly,
and set out what a credible next step would involve.

## The problem

"Agentic" AI — where an AI plans, delegates to sub-agents, and coordinates their
work — is moving quickly from demos into real use. Its most-praised pattern is also
its weak point: a coordinator spawns several workers in parallel and then
synthesises their outputs. Industry reports of these systems describe exactly the
predictable coordination failures — workers drifting from the coordinator's intent,
duplicated effort, and a synthesis step that blends inconsistent results
([Anthropic, 2025](https://www.anthropic.com/engineering/multi-agent-research-system)).
Independent studies of multi-agent AI find that a large share of failures are not
isolated mistakes but problems of *specification and inter-agent coordination*
([Cemri et al., 2025](https://arxiv.org/pdf/2503.13657)). In plain terms: the field
is rediscovering that the dangerous failures live in the relationships between
parts, not in the parts themselves.

That is a familiar lesson. Safety science learned it decades ago for human work
systems: accidents emerge from interactions across a whole system, not from one
broken component. A body of *systems-thinking* risk methods was built on that
insight. What is striking is that the AI-agent field is largely tackling its
coordination failures with component-by-component testing, rather than with the
interaction-focused methods systems science already developed.

## The idea

The proposal is to borrow that interaction-focused lens. NET-HARMS (Dallat,
Salmon & Goode, 2018) is a systems-thinking risk-assessment method that does two
things: it maps a system of work as a structured breakdown of tasks, and — its
distinctive move — it builds a *network* of how those tasks depend on one another
and asks, at each link, "if this upstream task goes wrong and isn't caught, what
new risk emerges downstream?" That second step is designed precisely to find
emergent, between-the-tasks risk.

An AI coordinator already produces, internally, exactly the kind of artefact
NET-HARMS analyses: a plan that breaks a job into sub-tasks and runs some in
parallel. So the idea is to have the coordinator run a lightweight NET-HARMS-style
review over its own plan *before* it executes — a structured pre-flight check that
asks the interaction questions ("do two pieces overlap? does one secretly depend
on another running first? will the join step quietly bury a disagreement?") and
flags problems while they are still cheap to fix. Because checking a plan is far
cheaper than running it, even an occasional catch is worth a great deal.

## Why a systems-science lens, specifically

The distinctive contribution here is not "add a checklist." It is the claim — and
the early evidence for it — that **agent-coordination failures are emergent
phenomena best surfaced by analysing the coupling between tasks, not by inspecting
tasks one at a time.** That is a systems-science claim, and it is the part that
carried the result in testing. Ordinary "what could go wrong?" review, even by a
strong AI, reliably catches problems that are visible within a single task but
keeps missing the ones that only appear when you look at how tasks are wired
together. The structured, network-based view caught those. This is the natural
home ground of systems science, and it is where this proposal can contribute
something the engineering-led efforts are not currently bringing.

## What we found so far (a small proof-of-concept)

We built six realistic coordinator plans across research and software tasks,
deliberately planted known flaws in them (overlaps, hidden dependencies, silent
conflict-merging, runaway loops, and some "clean" plans as controls), and compared
a NET-HARMS-structured review against ordinary unstructured review. The headline:

- On a capable AI model, the structured check caught about **nine in ten** of the
  planted flaws versus about **six in ten** for ordinary review, with no increase
  in false alarms — and its advantage was concentrated on the interaction failures.
- The benefit came almost entirely from the *network/interaction* part of the
  method, not the basic task-breakdown part (which today's AIs already do
  adequately).
- An early version of the check raised too many minor flags; a simple fix —
  restricting the "completeness" questions to where they actually matter, while
  never silencing the structural/interaction questions — restored accuracy. This
  "tune the noise, protect the signal" rule is a small but useful design finding.

These are promising signals, not proof. The study is deliberately small.

## What we don't yet know (stated plainly)

- **It depends on a capable model.** Run on a small model that fits on a laptop,
  the check became unreliable and the advantage disappeared. This approach assumes
  a strong underlying AI.
- **Scale and independence.** Six examples, scored largely by one person. The next
  step needs more examples and independent checking before any claim is firm.
- **A moving target.** This is a fast field, and it is possible that future AI
  models become good enough that an explicit check adds less. The window and the
  framing matter.

## Why this is worth pursuing now

As far as we could find, no one is currently applying a systems-thinking,
emergent-risk lens as an automatic pre-flight check for AI agent workflows. The
ingredients exist separately — systems-safety methods on one side, multi-agent
reliability work on the other — but the bridge between them is open, and it is a
bridge a systems scientist is well placed to build. The need is real and growing;
the conceptual tool is mature and validated in its original domain; and the early
evidence suggests it transfers.

## Proposed next step

A modest, well-scoped study would: (1) expand the test set from six to roughly
thirty plans drawn from real agent workflows, independently checked by a second
person; (2) repeat the comparison across more than one capable AI model to test
how general the benefit is; and (3) produce a clear, shareable write-up of the
method and results. This is primarily research design and analysis — the systems-
science core — with a modest amount of software help to run the comparisons. It
would either establish the effect on firmer ground or show its limits cheaply,
and in doing so produce a reusable public benchmark for "between-the-agents" risk
that holds value regardless of how the larger field evolves. A subsequent,
more ambitious phase would build the check into a live agent system and measure
whether acting on its warnings actually improves real outcomes.

---

*Prepared with AI assistance. The underlying method is NET-HARMS (Dallat, Salmon &
Goode, 2018); the application to AI agent workflows, the proof-of-concept, and the
framing here are the author's.*
