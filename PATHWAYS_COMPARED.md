# Pathways to bring the idea to life — compared

*Companion to the concept note and collaborator brief. June 2026.*

**The one principle:** separate the *value* (the NET-HARMS emergent-risk overlay)
from the *commodity* (the agent framework — model choice, tool wiring, config,
which is increasingly given away by well-funded teams). The lighter pathways
deliver the value *on top of* what already exists; the heaviest one makes you
build and maintain the commodity while competing on it. Prove the idea first;
that keeps every pathway below open at once.

---

## At a glance

| # | Pathway | What you actually build | Rough cost / commitment | What it protects against | Main risk | Where it sits |
|---|---------|------------------------|------------------------|--------------------------|-----------|---------------|
| 1 | **Add-on to existing frameworks** | Just the risk overlay, as a plug-in | Low — small build, one engineer | Staying focused on your difference; riding others' distribution | You're a "feature," dependent on host frameworks | After validation; fastest route to real users |
| 2 | **Standalone risk service** | The overlay as a hosted "send plan → get risks" service you own | Medium — a real but small product + light ops | Owning the value; clear business model | Needs distribution & sales; capable-model cost per call | After validation, if you want to own a product |
| 3 | **Reference tool + public benchmark (give away)** | Open method, small open tool, the test set | Low–medium — mostly research & write-up | Reputation, standard-setting; robust to field change | No direct revenue | **Best first move**; by-product of the validation study |
| 4 | **Vertical application** | The overlay aimed at one high-stakes domain | Medium — domain partner + tailoring | Real buyers who feel the pain; easier to prove value | Narrower market; needs domain access | After validation; strong if you have a domain partner |
| 5 | **Specification / design pattern** | A spec others implement; no product | Very low — writing + advocacy | Pure influence, near-zero build | No control or revenue | Follows naturally from #3 |
| 6 | **Full platform** (configure agents + models + tools, overlay as USP) | The whole framework *plus* the overlay | High — a funded startup, team, ongoing maintenance | Bundled experience for non-technical users | Competing on the commodity; most exposed to incumbents & better base models | Last; only if the overlay needs deep integration or users need everything bundled |

---

## How they relate (the sequence, not a menu)

These are stages, not rival choices. The **validation study** (in the
collaborator brief) produces, as a by-product, the benchmark and a reference
implementation — i.e. **pathway 3**. That same asset is what makes pathways 1, 2
and 4 credible to build, and what would de-risk pathway 6 if you ever wanted it.

```
   Validation study  ──►  3. Reference tool + benchmark  ──►  5. Spec/pattern
   (collaborator brief)        │
                               ├──►  1. Add-on to frameworks
                               ├──►  2. Standalone service
                               └──►  4. Vertical application
                                            │
                                            └──►  6. Full platform (only if justified)
```

Proving it and publishing the benchmark commits you to none of the commercial
paths while keeping all of them open — including the platform.

## Two caveats that apply to every pathway

1. **It needs a capable model.** The effect held on a strong model and collapsed
   on a small local one. Any vehicle inherits this; "cheap local guardrail" is not
   yet supported.
2. **The effect isn't proven at scale yet.** Six examples, promising signal. The
   lighter pathways let you settle this cheaply; the platform forces you to bet on
   the answer before you have it.

## A note on pathway 6 (the full platform)

It's the most exciting to picture and the riskiest to pursue. You'd spend most of
your money building the undifferentiated layer (model/tool/config plumbing) that
others give away, while your actual edge rides along as one feature — and you'd be
maximally exposed to incumbents adding a similar safety feature or to base models
improving. It becomes the right call only if (a) the overlay turns out to work
*only* with deep runtime integration, so it can't live as an add-on, or (b) your
target users are non-technical people who genuinely need the whole thing bundled.
Keep it in view; don't lead with it.

## Suggested read of the field (to revisit with partners)

- **Lowest regret, plays to your strengths:** validation study → pathway 3
  (benchmark + reference tool). Produces a citable result and an asset every other
  path builds on.
- **If a commercial pull appears:** pathway 1 (add-on) for speed, or pathway 4
  (vertical) if you have a domain partner who feels the pain.
- **Own-a-product ambition:** pathway 2, once 1 or 4 shows demand.
- **Platform:** only after the above de-risk it.
