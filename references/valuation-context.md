# Valuation context (optional)

This reference is **conditional**. It activates only when the inputs happen to support a meaningful
sanity check, and is silent otherwise. In most seed screens it will produce nothing — and that is
correct. Do not force it.

## When to use

All three conditions must be met:

1. **The company states a valuation or round terms** — pre-money, post-money, raise amount, or
   equity offered. Found in a deck, a press release, or a filing. Not inferred from "we are raising."
2. **Comps-scout has listed comparables with revenue multiples** — at least two public companies in
   a related category with EV/Rev or P/S data.
3. **The comparables are not weak.** If comps-scout rated the analogy "weak," stop. A valuation
   check built on a weak comp is worse than no check — it lends false precision to a guess.

If any condition is missing, skip this section entirely. The memo does not mention that a valuation
check was considered and declined. Silence is the correct output.

## What to compute

### The VC Method — sanity check, not a valuation opinion

The goal is not to value the company. It is to check whether the stated valuation is sane relative to
what the public market pays for this category, given a plausible exit.

**Step 1 — Pick an exit value range.**
Use the comps-scout's listed comparables. Take the revenue multiples (low and high) and apply them
to a plausible year-5 or exit-year revenue figure. If the company's own plan projects year-5 revenue,
use that (flagged as self-reported). If not, use the category median growth rate applied to a stated
current revenue, or skip — no revenue means no exit value means no check.

$$\text{Exit Value}_{\text{low}} = \text{Rev}_{\text{exit}} \times \text{Multiple}_{\text{low}}$$
$$\text{Exit Value}_{\text{high}} = \text{Rev}_{\text{exit}} \times \text{Multiple}_{\text{high}}$$

**Step 2 — Discount back at a venture-required return.**
Seed-stage investors typically target 10x–30x over 5–7 years, which implies a required rate of
return (r) of roughly 40–80% depending on stage and risk appetite. Use a range, not a point estimate.

$$\text{POST}_{\text{low}} = \frac{\text{Exit Value}_{\text{low}}}{(1 + r_{\text{high}})^n}$$
$$\text{POST}_{\text{high}} = \frac{\text{Exit Value}_{\text{high}}}{(1 + r_{\text{low}})^n}$$

Where:
- r_low ≈ 0.40, r_high ≈ 0.80
- n = years to exit (5–7 typical at seed)

**Step 3 — Derive implied pre-money and ownership.**

$$\text{PRE} = \text{POST} - \text{INV}$$
$$f = \frac{\text{INV}}{\text{POST}}$$

Where INV is the stated raise amount and f is the implied investor ownership fraction.

**Step 4 — Compare to the stated terms.**
If the company's stated pre-money falls within the computed range, the valuation is sane — say so in
one sentence. If it falls above the range, the company is pricing ahead of what the category supports
at a venture-required return — say that, plainly. If it falls below, note it but do not frame it as a
bargain — it may reflect a weaker company or a distressed raise.

### Adjusting for failure probability (optional, only if the bear case is strong)

The CFA curriculum adjusts the discount rate by an annual failure probability (q):

$$r^* = \frac{1 + r}{1 - q} - 1$$

Use this only when the red-team's bear case is rated "strong" and the failure path is concrete
(a specific kill question, not a general "startups fail"). In that case, apply q = 0.20–0.30 (typical
seed failure rates) and note the adjusted range alongside the base case.

If the bear case is moderate or weak, skip this adjustment. Do not invent a failure probability to
produce a more conservative number — the adjustment is meaningless without a specific failure thesis.

### Scenario weighting (optional, only when outcomes diverge sharply)

When the upside and downside scenarios are far apart (e.g., 10x exit vs. zero), probability-weighting
them can surface whether the expected value justifies the terms. Use three scenarios:

| Scenario | Probability | Exit value |
|---|---|---|
| Home run | 10–15% | Comps high × aggressive growth |
| Modest success | 25–35% | Comps median × plan growth |
| Failure | 50–65% | 0 |

Compute the probability-weighted expected exit value, then discount it back. If the implied pre-money
is below the stated terms, the round is expensive relative to expected value. If above, it is cheap.

**Do not present this as a valuation.** It is a check on whether the terms are sane. The number is
only as good as the scenario probabilities, which are guesses. State them as guesses.

## How to present in the memo

If the check runs (all three conditions met), add a short section after the scorecard:

```markdown
## Valuation context

The stated pre-money of [X] sits [within / above / below] the range implied by the listed comps
([low]–[high], at a 40–80% required return over [n] years). [One sentence on what drives the gap,
if any.]

*Based on [comps-scout's comps with source tags]. Exit revenue assumed at [X], [self-reported /
category-median growth applied]. This is a sanity check, not a valuation.*
```

Under 80 words. No DCF tables. No formulae in the memo — those live here. The partner sees the
stated terms, the implied range, and whether they reconcile. Nothing more.

## What this is not

- **Not a valuation.** It does not produce a fair value. It checks whether stated terms are sane
  relative to category comps at a venture-required return.
- **Not a scored dimension.** It does not affect the total or the recommendation. A company with
  insane terms can still score well on team, market, and product — the terms are a separate
  question for a separate stage of the process.
- **Not mandatory.** If the data isn't there, this section does not appear. Do not write
  "Valuation context not available" — simply omit the section.
- **Not a reason to pass.** An aggressive valuation is a negotiation point, not a triage failure.
  The recommendation turns on the company, not the terms.
