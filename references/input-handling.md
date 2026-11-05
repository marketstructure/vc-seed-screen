# Handling variable input quality

The defining constraint of this skill: pitches arrive as anything from a 20-slide deck with a financial
model to a bare URL in a cold email. The screen must be honest about what it could and could not see.

## Grade assignment

Decide the grade **before** any analysis. The grade is internal — it determines which dimensions can be
scored and what the memo's "Based on" line says. It never appears in the memo by name.

### E1 — Full package
Deck or memo **plus** at least two of: financial model, cap table, data room, founder conversation notes.

What you can do: score all six dimensions with confidence, audit the model's internal consistency, assess
team completeness from actual conversation.

### E2 — Deck or detailed description
A pitch deck, or a written description that includes concrete metrics (revenue, users, growth, pricing).

What you can do: score all dimensions, but treat every number as self-reported and unaudited. Founder
assessment is inferred from how the deck is built, not from interaction.

### E3 — URL plus short description
A website and a sentence or two.

Procedure:
1. Fetch the site. Record what is actually present: product description, pricing page, customer logos,
   team page, blog cadence, careers page.
2. Note what is **absent** — no pricing, no team page, no customers, a placeholder blog.
3. Do not infer traction from site polish. A well-designed site is a design budget, not demand.
4. Mark demand and plan as **not assessable** rather than scoring them low. Not assessable is not zero.
5. Score what is genuinely readable: team (if named), market (if the category is legible), product
   (usually the best-evidenced dimension on a website), and path to market (often visibly absent).

Signals that are genuinely readable from a site: what the product actually does, whether pricing is
public and at what level, whether the team page names real people with verifiable backgrounds, whether
there are named customers or case studies, and whether any regulatory claim is made and substantiated.

### E4 — Name and one line
Almost always `P-EVIDENCE` unless the one line itself reveals a disqualifier (wrong market, wrong stage,
a category the fund does not invest in). Do not produce a six-dimension scorecard on one sentence — it is
false precision.

## Absence handling

Never convert missing data into a low score. They are different statements:

- **Not assessable** — we could not see it. Excluded from the total; remaining weights renormalized.
- **Weak** — we saw it and it was poor. Lowers the score.

Conflating these is the most common way a triage system becomes unfair to founders who are simply bad at
decks. A founder with no deck and a real business should surface as "one call to test the named
questions", not as a pass.

## Conflicting evidence

When the deck says one thing and the website says another, the **website wins on present state** and the
deck wins on intent. Note the conflict explicitly; it is a diligence question for the call.

When a founder claims a metric with no basis, mark it unverified and carry it into the verification list.

## Red flags that override the score

These settle the recommendation regardless of the total:

- **Fabricated or unverifiable traction** — immediate pass, `P-DEMAND`. Not a scoring deduction.
- **Cap table with an unresolved dispute or a dead equity holder** — pass, `P-TEAM`.
- **Founder will not name the competition** — cap at "one call"; it usually signals an unexamined market.
- **Regulatory arbitrage presented as innovation** — flag it and let the call test it.
- **Cannot be legally sold or billed in the stated market** — `P-PATH`, regardless of total.

## When the input is a live URL

If fetching fails, say so and grade down one level. Do not substitute assumptions for a page you could
not read. If the site is a parked domain or a waitlist-only landing page, that is E4 in practice
regardless of what was claimed in the email.
