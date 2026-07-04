# The experiment, in plain English

*A jargon-free explanation of how the test worked and what it found.*

## The set-up

Picture an AI "team leader" that takes a big job, splits it into pieces, hands
each piece to a helper AI, and then stitches the helpers' work back together.

The tricky failures in these AI teams usually aren't one helper being wrong.
They're problems **between** the pieces: two helpers doing the same work, one
helper needing something another hasn't finished yet, or the leader blending two
disagreeing answers into a single confident — but wrong — answer.

The question we tested: if you make the AI **review its own plan before it
starts**, does a *structured* review — one that specifically asks "how might these
pieces trip over each other?" — catch more of those problems than just asking the
open question "what could go wrong here?"

## How we tested it

1. **Wrote six realistic team plans** — six worked examples of an AI leader
   splitting up a job (some research tasks, some software tasks).
2. **Planted known flaws in them.** Into each plan I deliberately inserted a set
   of specific problems — an overlap here, a hidden dependency there, a leader who
   quietly merges conflicting results. Because I planted them, I had an **answer
   key**: I knew exactly what was wrong with each plan. (A couple of plans were
   left deliberately clean, to check for false alarms.)
3. **Ran each plan past two kinds of AI reviewer**, neither of them shown the
   answer key:
   - the **open-question** reviewer ("what could go wrong?"), and
   - the **structured** reviewer (walk the plan asking the specific
     systems-thinking questions about how the pieces connect).
4. **Marked both like exam papers** against the answer key — counting how many
   real flaws each one *caught*, and how often it *cried wolf* (flagged a problem
   that wasn't actually there).

## What it found

On a **capable** AI, the structured reviewer clearly did better:

- It caught about **nine in ten** of the planted flaws, versus about **six in
  ten** for the open-question reviewer — and it raised **no false alarms**.
- The extra flaws it caught were exactly the **between-the-pieces** kind. The
  open-question reviewer was fine at spotting problems *inside* a single piece but
  kept walking past the ones that only appear when you look at how the pieces are
  **wired together**. That "look at the connections" habit is the whole point of
  the systems-thinking angle — and it's the part that showed up in the results.

## Two honest footnotes

- **It needs a strong AI.** Run on a small AI that fits on a laptop, the advantage
  vanished — the little model wasn't sharp enough, and the structured questions
  actually tripped it up.
- **It's an early sign, not proof.** Only six examples. And it shows the structured
  review is better at *spotting* the problems; we haven't yet shown that *fixing*
  them makes the AI team's final work better — which is the thing that would
  ultimately clinch it.

## In one sentence

We planted known flaws in six AI team-plans, had two kinds of AI reviewer try to
find them blind, and the systems-thinking reviewer caught noticeably more —
especially the failures that hide in the connections between the parts — but only
when run on a capable AI.
