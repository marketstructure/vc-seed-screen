# Output format

The deliverable is a **memo a partner can read cold** — including a scorecard they can interrogate
without asking how it was built.

## The rule

The score belongs in the document. **The plumbing does not.**

A partner should be able to read the framework, understand what every number means, disagree with a
specific score, and see the reasoning behind it. That is the point of showing it. What they should
never see is the machinery of how the analysis was organised.

### Banned from the memo

- Agent names, role labels, or bracketed section markers — `[red-team]`, `[founder-assessor]`
- Any sentence attributing a judgement to an internal role: "the red team argues", "the panel found",
  "our valuation analyst scores this…"
- Internal tiering language: "evidence grade E3", "conviction cap", "band", "tail flag"
- Decimal precision that implies false confidence — `6.0 / 10` is fine, `51.33 / 100` is not
- Confidence percentages

### Required in the memo

- The **scorecard**, with the scale legend printed so the numbers are self-explanatory
- A **one-line plain-prose reason** for every score — this is what makes the score arguable rather than
  opaque
- The **weighted total** and the verdict in words
- The **assessment basis** stated in plain language: what materials were available

## Structure

```markdown
# <Company> — Investment Screen

**Prepared**: <date>
**Sector**: <sector>
**Stage**: <stage>
**Based on**: <what we actually had — plain language, e.g. "company website and public
sources only. No deck, no financials, no management conversation.">

---

## What they do

<2–4 sentences. The product, the buyer, and how it works — in plain language, no adjectives.
A partner should be able to explain this company to a colleague after reading only this
paragraph. This is orientation, not evaluation.>

## Recommendation: <plain-language verdict>

<1–3 sentences: the analyst's view and the single reason for it. No decision rules, no
instructions to the reader, no "if X then pass".>

---

## How this scores

| Dimension | Weight | Score | Why |
|---|---|---|---|
| Team | 30 | X / 10 | <one line, specific> |
| Market | 20 | X / 10 | <one line> |
| Product & differentiation | 15 | X / 10 | <one line> |
| Evidence of demand | 15 | X / 10 or *not assessable* | <one line> |
| Path to market | 10 | X / 10 | <one line> |
| Plan & capital efficiency | 10 | X / 10 or *not assessable* | <one line> |

**Weighted total: XX.X / 100 — <verdict>**

<If any dimension is unassessable: "Scored on XX of 100 weight points. Unassessable
dimensions are excluded, not scored zero.">

**Fund-returner potential: X / 3** — <one line on whether this can return the fund>

*Scale: 9–10 exceptional, 7–8 strong, 5–6 adequate, 3–4 weak, 1–2 failing. Most seed
companies score 5–6.*

---

## What they have
## Recent news and public signals
## The evidence base
## How unique is it?
## The competitive picture
## Valuation context
## What this means for the investment case
## Open questions
## Bottom line

---

*<Disclaimer>*
```

**`Open questions`** lists what the public record does not settle, phrased as findings rather than
instructions. "The funding figure does not reconcile" — not "reconcile the funding figure". Where it helps,
say what evidence would settle each one; that is analysis, not a task assignment.

The sections below the scorecard are prose. No scores, no tables except competitor comparisons and the
verification list.

**`Recent news and public signals`** carries what was found outside the company's own site: dated
announcements, competitions and awards, reported funding figures, academic output, and any negative
signals. It must also name the **conspicuous gaps** — the announcements that should exist and do not.

On figures that differ from the company's own claim: distinguish a **genuine contradiction** (same period,
same metric) from a figure that is merely **older** or **defined differently**. A temporal gap is not an
inconsistency, and writing it as one makes the screen look careless. The finding usually worth reporting is
that the current number has no independent source and no stated composition.

**`Valuation context`** appears only when the company states round terms AND comps-scout returned non-weak
listed comparables. See `references/valuation-context.md`. If either input is missing, omit the section
entirely — do not write "valuation context not available." When it does appear: under 80 words, state the
stated terms, the implied range, whether they reconcile, and what drives any gap. This is a sanity check,
not a valuation opinion.

## Writing the "Why" column

This is the part that makes the framework credible. Each line must be **specific enough to argue with**:

- Good: "Researcher who knew the problem before she had a company; no regulatory or commercial lead"
- Bad: "Strong founder, team gaps"
- Good: "Pre-regulatory with no stated plan; no reimbursement pathway"
- Bad: "Regulatory risk"

If two different companies would produce the same "Why" line, the line is not doing any work.

## Voice

Write as an analyst who has formed a view and is accountable for it.

- **Take positions.** "The moat is thin" beats "the moat may face challenges."
- **Use the specific over the general.** "85% sits below the ICC 0.9 clinicians demand" beats
  "accuracy may be insufficient."
- **Name the uncomfortable finding early.** If a competitor is two years ahead, that goes in the
  competitive picture, stated plainly.
- **No throat-clearing.** Delete "it is worth noting that", "it should be mentioned", "arguably".
- **No decision rules.** Never write "if X comes back empty, this is a pass" or "ask about A, B and C".
  That is the analyst handing the judgement back with a rule attached. State what the analyst thinks and
  what remains unresolved; the partner decides.
- **No imperatives aimed at the reader.** "Reconcile the funding figure" is an instruction. "The funding
  figure does not reconcile" is a finding. Prefer the second every time.
- **Short paragraphs.** One idea each.

## Length

1,000–1,800 words including the scorecard. Long enough for the competitive and evidence analysis,
short enough to read in one sitting. Beyond that the screen has become diligence — cut.

## Formatting

- Plain Markdown, no HTML
- No currency symbols; write "2 million" and state the currency where it matters
- Multiples to one decimal
- Tables for the scorecard, competitor comparison, and verification list only
- Bold sparingly: the recommendation, the total, and the few numbers that drive the decision
