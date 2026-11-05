# vc-seed-screen

A Hermes Agent skill for first-pass triage of pre-seed and seed startup pitches. It accepts whatever evidence exists — pitch deck, data room, company website URL, or a written description — and produces a scored investment screening memo with a plain-language recommendation.

**Triage, not diligence.** The question is never "should we invest?" — it is "does this earn a first meeting, and if not, why not?"

## Install

```bash
hermes skills install marketstructure/vc-seed-screen/vc-seed-screen
```

Or install directly from this repo's SKILL.md:

```bash
hermes skills install https://raw.githubusercontent.com/marketstructure/vc-seed-screen/main/SKILL.md
```

Or from a local clone:

```bash
hermes skills install /path/to/vc-seed-screen
```

## Prerequisites

- **Hermes Agent** with the **web toolset** active (`web_search`, `web_extract`)
- **Optional:** `yfinance` and `akshare` for listed-comparable financials:

```bash
pip install yfinance akshare
```

If not installed, the comps-scout falls back to web search silently. No API keys required.

## How it works

The skill runs a five-step pipeline using `delegate_task` for parallel agent dispatch:

1. **Evidence grading** — assesses input quality (E1–E4) to determine which dimensions can be scored
2. **News review** — searches company, product, and each founder individually (including non-English sources)
3. **Parallel IC panel** — six scoring agents plus two context agents:
   - Team (30), Market (20), Product & differentiation (15), Evidence of demand (15), Path to market (10), Plan & capital efficiency (10)
   - Plus comps-scout (listed comparables) and landscape-analyst (competitive field with non-English search)
4. **Red team** — adversarial bear case and kill question
5. **IC chair** — deterministic scoring via `scripts/score.py`, then a committed recommendation

### Scoring

Six dimensions, each scored 0–10, weighted to 100. Unknown dimensions are excluded and the remaining weights renormalized — **"not assessable" is never scored zero.** A fund-returner rating (0–3) is reported alongside the score.

| Verdict | Total |
|---|---|
| Strong — proceed | 70+ |
| Proceed with reservations | 55–69 |
| Borderline — one call | 45–54 |
| Pass | below 45 |

```bash
python3 scripts/score.py --team 7 --market 6 --product 5 --demand 4 --path 6 --plan 5 --tail 2
```

### Design principles

- **Score against the stage, not the end state.** A pre-seed company has no revenue; a seed-stage medtech has no clearance. An unstarted but correctly understood pathway scores 5–6, not 2.
- **No invented numbers.** Absent data is "not assessable" and excluded from the total — never filled with a guess.
- **Pass reasons are coded** (P-MARKET, P-TEAM, P-PRODUCT, P-DEMAND, P-PATH, P-PLAN, P-TIMING, P-EVIDENCE) so patterns are visible at volume.
- **Non-English competitive search.** Always searches in Chinese as well as English — an English-only scan misses the most advanced market for many hardware categories.
- **Show the framework, hide the plumbing.** The memo shows scores and reasoning. It never shows agent names, role attribution, or internal tiering language.

### Optional valuation context

When the company states round terms AND listed comparables are available, the skill can run a VC-method sanity check (borrowed from the CFA curriculum). This is conditional — silent when the data isn't there. See `references/valuation-context.md`.

## Repository structure

```
vc-seed-screen/
├── SKILL.md                          # Main skill instructions
├── LICENSE                           # MIT
├── README.md
├── requirements.txt                  # Optional: yfinance, akshare
├── .gitignore
├── scripts/
│   ├── score.py                      # Deterministic scoring engine
│   └── comps.py                      # Listed-comparable data puller
├── references/
│   ├── rubric.md                     # Scoring anchors, 0–10 per dimension
│   ├── input-handling.md             # Evidence grading rules
│   ├── output-template.md            # Memo format and writing rules
│   ├── valuation-context.md          # Optional VC-method sanity check
│   └── agents/
│       ├── founder-assessor.md
│       ├── market-mapper.md
│       ├── wedge-analyst.md
│       ├── demand-analyst.md
│       ├── path-analyst.md
│       ├── model-auditor.md
│       ├── comps-scout.md
│       ├── landscape-analyst.md
│       ├── news-reviewer.md
│       ├── red-team.md
│       └── ic-chair.md
└── tests/
    └── test_score_skill.py
```

## Tests

```bash
python3 tests/test_score_skill.py -q
```

Stdlib + pytest only, no live network.

## License

MIT — see [LICENSE](LICENSE).

## Author

Amir Hoosain ([@marketstructure](https://github.com/marketstructure))
