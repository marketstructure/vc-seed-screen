#!/usr/bin/env python3
"""Scoring engine for vc-seed-screen.

Six dimensions, each 0-10, weighted to 100. Unknown dimensions are excluded
and the remaining weights renormalized.

Usage:
    python3 score.py --team 6 --market 5 --product 5 --demand 4 --path 3 --plan 6 --tail 2

    # unknown dimensions: pass 'u'
    python3 score.py --team 6 --market 5 --product 5 --demand u --path 3 --plan u --tail 1
"""

import argparse
import sys

WEIGHTS = {"team": 30, "market": 20, "product": 15, "demand": 15, "path": 10, "plan": 10}
LABELS = {
    "team": "Team",
    "market": "Market",
    "product": "Product & differentiation",
    "demand": "Evidence of demand",
    "path": "Path to market",
    "plan": "Plan & capital efficiency",
}
UNKNOWN_TOKENS = {"u", "unknown", "?", "-", ""}


def parse_score(raw, name):
    if raw is None or raw.strip().lower() in UNKNOWN_TOKENS:
        return None
    try:
        value = float(raw)
    except ValueError:
        sys.exit("error: --%s must be a number 0-10 or 'u'" % name)
    if not 0.0 <= value <= 10.0:
        sys.exit("error: --%s must be between 0 and 10 (got %s)" % (name, raw))
    return value


def verdict(score):
    if score >= 70:
        return "Strong - proceed"
    if score >= 55:
        return "Proceed with reservations"
    if score >= 45:
        return "Borderline - one call to test the named questions"
    return "Pass"


def compute(scores, tail):
    """Compute weighted total and verdict from a dict of dimension scores.

    Returns (total, available_weight, verdict_string, notes_list).
    """
    known = {d: s for d, s in scores.items() if s is not None}
    if not known:
        return None, 0, "Cannot score — all dimensions unknown.", []

    available = sum(WEIGHTS[d] for d in known)
    total = sum(known[d] / 10.0 * WEIGHTS[d] for d in known) / available * 100.0
    v = verdict(total)
    notes = []

    if tail == 0 and total >= 70:
        notes.append(
            "High score with no path to a fund-returning outcome. "
            "This is a good business, not a venture return."
        )
    if tail >= 2 and total < 55:
        notes.append(
            "Modest present evidence, meaningful upside. At seed this asymmetry "
            "is the reason to take a call rather than pass on the score."
        )

    return total, available, v, notes


def main():
    parser = argparse.ArgumentParser(description="Seed screen scoring engine")
    for dim in WEIGHTS:
        parser.add_argument("--" + dim, required=True, help="0-10, or 'u' for unknown")
    parser.add_argument("--tail", required=True, type=int, choices=[0, 1, 2, 3],
                        help="fund-returner potential 0-3")
    args = parser.parse_args()

    scores = {dim: parse_score(getattr(args, dim), dim) for dim in WEIGHTS}
    total, available, v, notes = compute(scores, args.tail)

    if total is None:
        sys.exit("error: all dimensions unknown - cannot score. Assess, do not guess.")

    print()
    print("  %-28s %6s %7s" % ("Dimension", "Weight", "Score"))
    print("  " + "-" * 43)
    for dim in WEIGHTS:
        value = scores[dim]
        shown = "not assessable" if value is None else "%.1f / 10" % value
        print("  %-28s %6d %7s" % (LABELS[dim], WEIGHTS[dim], shown))
    print("  " + "-" * 43)
    print("  %-28s %6d %7.1f / 100" % ("Weighted total", available, total))
    print()

    if available < 100:
        print("  Scored on %d of 100 weight points." % available)
        print("  Unassessable dimensions are excluded, not scored zero.\n")

    print("  Verdict           : %s" % v)
    print("  Fund-returner     : %d / 3" % args.tail)
    print()

    for note in notes:
        print("  Note: %s\n" % note)


if __name__ == "__main__":
    main()
