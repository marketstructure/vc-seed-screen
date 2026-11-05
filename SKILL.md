---
name: vc-seed-screen
description: Screens pre-seed pitches into a scored IC memo.
version: 1.0.0
author: Amir Hoosain (@marketstructure)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [vc, venture-capital, startup, screening, investment, due-diligence, seed, pre-seed]
    category: finance
    related_skills: [comps-analysis, dcf-model]
    requires_toolsets: [web]
    requires_tools: [web_search, web_extract]
---

# VC Seed Screen Skill

Triage, not diligence. The question is never "should we invest?" — it is "does this earn a first
meeting, and if not, why not?" Accepts whatever evidence exists — pitch deck, data room, company
website URL, or a written description — grades the input, scores six weighted dimensions through a
parallel agent panel, and returns a plain-language recommendation with a coded pass reason.

## When to Use

- Triage an inbound startup pitch from a deck, URL, or written description
- Decide whether a company deserves a first meeting
- Build a comparable pipeline record across many deals with consistent scoring
- Screen a batch of pre-seed or seed companies for ranking

## Prerequisites

- **Web toolset active** — `web_search` and `web_extract` are used for competitive landscape,
  news review, and company website fetching.
- **Optional: akshare / yfinance** — for listed-comparable financials. Install with
  `pip install yfinance akshare`. If absent, the comps-scout falls back to `web_search` silently.
- No API keys required.

## How to Run

Provide the company name or URL and any available materials (deck, description, metrics). The skill
runs five steps:

1. **Grade the evidence** (E1–E4) — determines which dimensions can be scored
2. **News review** — `web_search` for company, product, and each founder
3. **Parallel IC panel** — `delegate_task` with six scoring agents + two context agents
4. **Red team** — adversarial pass over the combined output
5. **IC chair** — deterministic score via `scripts/score.py`, then recommendation

```bash
python3 scripts/score.py --team 7 --market 6 --product 5 --demand 4 --path 6 --plan 5 --tail 2
```

Output is a Markdown memo following `references/output-template.md`.

## Quick Reference

| Dimension | Weight | Agent |
|-----------|--------|-------|
| Team | 30 | `founder-assessor` |
| Market | 20 | `market-mapper` |
| Product & differentiation | 15 | `wedge-analyst` |
| Evidence of demand | 15 | `demand-analyst` |
| Path to market | 10 | `path-analyst` |
| Plan & capital efficiency | 10 | `model-auditor` |
| Fund-returner (0–3) | — | IC chair, reported alongside score |

| Verdict band | Total |
|---|---|
| Strong — proceed | 70+ |
| Proceed with reservations | 55–69 |
| Borderline — one call | 45–54 |
| Pass | below 45 |

## Procedure

### Step 1 — Grade the evidence

See `references/input-handling.md` for the full grading rules. The grade is internal — it sets which
dimensions can be scored and never appears in the memo by name.

| Grade | What you have |
|-------|---------------|
| **E1** | Deck + financial model + data room or founder notes |
| **E2** | Deck, or detailed written description with metrics |
| **E3** | Website URL + short description, no metrics |
| **E4** | Name + one-line description only |

At E3/E4, demand and plan are usually not assessable. Mark them as such — **never score zero for
absent data.** Unassessable dimensions are excluded and the remaining weights renormalized.

### Step 2 — News review (sequential, before scoring)

Search the company name, product name, and each founder individually via `web_search`. Search in
English **and** the company's home-market language where it differs. See
`references/agents/news-reviewer.md`.

Findings can change which dimensions are assessable, so this step cannot run in parallel with scoring.

### Step 3 — Parallel IC panel

Use `delegate_task` to dispatch six scoring agents plus two context agents in one batch. Each
subagent starts with zero context — pass everything it needs in `goal` and `context`: the fetched
site text, the relevant rubric section, news-reviewer findings, and source tags.

For the six scoring agents, use `output_schema` to force structured output:

```json
{
    "type": "object",
    "properties": {
        "score": {"type": "number"},
        "reason": {"type": "string"},
        "sources": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["score", "reason"]
}
```

The context agents (comps-scout, landscape-analyst) return prose, not structured output.

| Agent | Weight | Mandate | Reference |
|-------|--------|---------|-----------|
| `founder-assessor` | 30 | Founder-market fit, team completeness, hiring gravity | `references/agents/founder-assessor.md` |
| `market-mapper` | 20 | TAM/SAM/SOM, timing mechanism (why now) | `references/agents/market-mapper.md` |
| `wedge-analyst` | 15 | Product differentiation, incumbent response, durability | `references/agents/wedge-analyst.md` |
| `demand-analyst` | 15 | Contracts vs pilots vs LOIs vs waitlists | `references/agents/demand-analyst.md` |
| `path-analyst` | 10 | Regulatory clearance, reimbursement, distribution | `references/agents/path-analyst.md` |
| `model-auditor` | 10 | Plausibility of plan, burn, milestone realism | `references/agents/model-auditor.md` |
| `comps-scout` | — | Listed comparables, sector multiples (akshare/yfinance/web) | `references/agents/comps-scout.md` |
| `landscape-analyst` | — | Competitive field incl. non-English markets; tests "first" claims | `references/agents/landscape-analyst.md` |

`landscape-analyst` runs alongside the scorers but **can override the wedge score** — a cleared
competitor in the same modality settles the differentiation question regardless of how the deck read.

### Step 4 — Red team

Run `delegate_task` with a single task using `references/agents/red-team.md` as context, plus the
combined output from Step 3. The red team produces the bear case, the load-bearing unverified claims,
and the kill question. It is adversarial by design — a red team that agrees with the panel has failed.

### Step 5 — IC chair and scoring

1. Run `scripts/score.py` via `terminal` with the six dimension scores and the fund-returner rating.
2. Read the verdict it returns. That is the **starting position**, not the decision.
3. Apply override rules (see `references/agents/ic-chair.md`).
4. **Optional valuation context** — if the company states round terms AND comps-scout returned
   non-weak listed comparables, run the sanity check in `references/valuation-context.md`.
   If either input is missing, skip silently.
5. Commit to one recommendation.

The chair must not default to the middle because signals are mixed. "Interesting but we need more
information" is a deferral, not a recommendation.

### Step 6 — Write the memo

Write to a file using `write_file`, following `references/output-template.md`. The memo shows the
framework and the scores — a partner can read the dimensions, disagree with a specific number, and
see the one-line reasoning. What it never shows is the plumbing: no agent names, no role attribution,
no internal tiering language, no confidence percentages.

## Three non-negotiables

1. **Assess what you actually have before analysing it.** Grade the input (E1–E4). A URL-only read
   can never produce a confident recommendation.
2. **No invented numbers.** Never estimate traction, ARR, TAM, growth, or market share that was not
   provided. Absent data is "not assessable" — excluded from the total, never filled with a guess.
3. **Pass reasons are coded.** Every pass carries one code so patterns are visible at volume.

## Pass reason codes

| Code | Meaning |
|------|---------|
| `P-MARKET` | Too small, shrinking, or no credible path to venture scale |
| `P-TEAM` | Founder-market fit or team completeness gap |
| `P-PRODUCT` | Product undifferentiated, or incumbent will absorb it |
| `P-DEMAND` | No evidence anyone pays; interest mistaken for demand |
| `P-PATH` | Cannot be cleared, reimbursed, or distributed in the target market |
| `P-PLAN` | Plan implausible on the stated capital |
| `P-TIMING` | Right idea, wrong moment |
| `P-EVIDENCE` | Cannot assess on available information; revisit with a deck |

## Data rules

- **Listed comparables** use `akshare` (China/HK) or `yfinance` (US/global) when installed, via
  `scripts/comps.py`. If neither is available, fall back to `web_search` and `web_extract`.
- **Company-specific facts** come only from provided materials. No data source here has private-market
  data — do not pretend otherwise.
- Source tags on every claim: `[deck p.7]`, `[website]`, `[founder call]`, `[akshare]`,
  `[yfinance]`, `[web]`, `[inferred]`. Anything tagged `[inferred]` is a hypothesis, not a finding.
- If all sources are unavailable, `comps-scout` reports `COMPS UNAVAILABLE` and the memo says plainly
  that valuation context is missing. Never fabricate a comparable or a multiple.

## Output discipline

- Plain Markdown. No HTML.
- Show the framework and the scores; hide the plumbing. See `references/output-template.md`.
- Print the scale legend next to the scorecard.
- Every score needs a one-line reason specific enough to argue with.
- Numbers: no currency symbols; state the currency separately where it matters; one decimal on multiples.
- Write in a formed view, not a hedge. "The moat is thin" beats "the moat may face challenges."
- Name competitors. A landscape section without named companies is not a landscape section.
- Bold sparingly: the recommendation, the total, and the few numbers that drive it.

## Reference files

All reference files are loaded by the skill and must be present:

- `references/rubric.md` — scoring anchors for each dimension, 0–10
- `references/input-handling.md` — how to treat each input type, including URL-only
- `references/output-template.md` — memo format, banned list, scorecard template
- `references/valuation-context.md` — optional VC-method sanity check, activates only when stated
  terms and non-weak comps both exist
- `references/agents/founder-assessor.md`
- `references/agents/market-mapper.md`
- `references/agents/wedge-analyst.md`
- `references/agents/demand-analyst.md`
- `references/agents/path-analyst.md`
- `references/agents/model-auditor.md`
- `references/agents/comps-scout.md`
- `references/agents/landscape-analyst.md`
- `references/agents/news-reviewer.md`
- `references/agents/red-team.md`
- `references/agents/ic-chair.md`

## Pitfalls

- **Scoring the stage, not the company.** A pre-seed company has no revenue; a seed-stage medical
  device company has no clearance. Score whether the founder understands the pathway, not whether it
  is complete. An unstarted but correctly understood pathway is a 5–6, not a 2.
- **Conflating "not assessable" with "weak."** Not assessable is excluded from the total; weak lowers
  it. Punishing a founder for a missing deck rather than a missing business is how screens become unfair.
- **Monolingual competitive search.** Searching only in English misses the most advanced market for
  many hardware and medtech categories. Always search in Chinese as well.
- **Presenting temporal gaps as contradictions.** A 2023 funding figure of 157K and a 2026 claim of
  2 million is elapsed time, not an inconsistency. Report it as "composition undisclosed," not
  "does not reconcile."
- **Defaulting to the middle.** Mixed signals with a real fund-returning path is a call. Mixed signals
  with a capped market is a pass. "Interesting but we need more information" is a deferral.

## Verification

1. Run `python3 scripts/score.py --team 7 --market 6 --product 5 --demand 4 --path 6 --plan 5 --tail 2`
   and confirm it produces a scorecard with a verdict.
2. Run `python3 tests/test_score_skill.py -q` to verify the scoring engine.
3. Confirm all files listed in the Reference files section exist by reading them with `read_file`.
4. If `akshare`/`yfinance` are installed, run `python3 scripts/comps.py --ticker MDB --source yfinance`
   and confirm it returns structured data.
