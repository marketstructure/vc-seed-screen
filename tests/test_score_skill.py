#!/usr/bin/env python3
"""Tests for the vc-seed-screen scoring engine.

Stdlib + pytest only, no live network. Run:
    python3 tests/test_score_skill.py -q
"""

import subprocess
import sys
import os

import pytest

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORE_SCRIPT = os.path.join(SKILL_ROOT, "scripts", "score.py")


def run_score(args):
    """Run score.py with the given args and return (returncode, stdout)."""
    cmd = [sys.executable, SCORE_SCRIPT] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class TestVerdictBands:
    """Verify the verdict bands are correct."""

    def test_strong_proceed(self):
        # All 7s = 70.0 → Strong
        rc, out = run_score(["--team", "7", "--market", "7", "--product", "7",
                            "--demand", "7", "--path", "7", "--plan", "7", "--tail", "2"])
        assert rc == 0
        assert "Strong" in out

    def test_proceed_with_reservations(self):
        # All 6s = 60.0 → Proceed with reservations
        rc, out = run_score(["--team", "6", "--market", "6", "--product", "6",
                            "--demand", "6", "--path", "6", "--plan", "6", "--tail", "1"])
        assert rc == 0
        assert "Proceed with reservations" in out

    def test_borderline(self):
        # All 5s = 50.0 → Borderline
        rc, out = run_score(["--team", "5", "--market", "5", "--product", "5",
                            "--demand", "5", "--path", "5", "--plan", "5", "--tail", "1"])
        assert rc == 0
        assert "Borderline" in out

    def test_pass(self):
        # All 3s = 30.0 → Pass
        rc, out = run_score(["--team", "3", "--market", "3", "--product", "3",
                            "--demand", "3", "--path", "3", "--plan", "3", "--tail", "0"])
        assert rc == 0
        assert "Pass" in out


class TestUnknownDimensions:
    """Verify that unknown dimensions are excluded, not scored zero."""

    def test_unknown_excluded(self):
        # Two dimensions unknown — remaining 4 should renormalize
        rc, out = run_score(["--team", "8", "--market", "8", "--product", "u",
                            "--demand", "u", "--path", "8", "--plan", "8", "--tail", "2"])
        assert rc == 0
        assert "not assessable" in out
        assert "Scored on" in out

    def test_all_unknown_fails(self):
        rc, out = run_score(["--team", "u", "--market", "u", "--product", "u",
                            "--demand", "u", "--path", "u", "--plan", "u", "--tail", "0"])
        assert rc != 0
        assert "cannot score" in out.lower()

    def test_unknown_not_zero(self):
        """Unknown should produce a higher score than scoring those dims as zero."""
        rc_unknown, out_unknown = run_score([
            "--team", "8", "--market", "8", "--product", "u",
            "--demand", "u", "--path", "8", "--plan", "8", "--tail", "2"])
        rc_zero, out_zero = run_score([
            "--team", "8", "--market", "8", "--product", "0",
            "--demand", "0", "--path", "8", "--plan", "8", "--tail", "2"])
        assert rc_unknown == 0 and rc_zero == 0
        # Extract the total from output
        for line in out_unknown.split("\n"):
            if "Weighted total" in line:
                unknown_total = float(line.split("/")[0].split()[-1])
                break
        for line in out_zero.split("\n"):
            if "Weighted total" in line:
                zero_total = float(line.split("/")[0].split()[-1])
                break
        assert unknown_total > zero_total


class TestFundReturner:
    """Verify fund-returner notes appear when expected."""

    def test_high_score_no_tail(self):
        rc, out = run_score(["--team", "9", "--market", "9", "--product", "9",
                            "--demand", "9", "--path", "9", "--plan", "9", "--tail", "0"])
        assert rc == 0
        assert "good business" in out.lower()

    def test_low_score_high_tail(self):
        rc, out = run_score(["--team", "4", "--market", "4", "--product", "4",
                            "--demand", "u", "--path", "4", "--plan", "4", "--tail", "2"])
        assert rc == 0
        assert "asymmetry" in out.lower() or "upside" in out.lower()

    def test_no_note_when_not_triggered(self):
        rc, out = run_score(["--team", "6", "--market", "6", "--product", "6",
                            "--demand", "6", "--path", "6", "--plan", "6", "--tail", "1"])
        assert rc == 0
        assert "good business" not in out.lower()
        assert "asymmetry" not in out.lower()


class TestInputValidation:
    """Verify input validation."""

    def test_score_out_of_range(self):
        rc, out = run_score(["--team", "11", "--market", "6", "--product", "6",
                            "--demand", "6", "--path", "6", "--plan", "6", "--tail", "1"])
        assert rc != 0

    def test_tail_out_of_range(self):
        rc, out = run_score(["--team", "6", "--market", "6", "--product", "6",
                            "--demand", "6", "--path", "6", "--plan", "6", "--tail", "5"])
        assert rc != 0


class TestComputeFunction:
    """Test the compute function directly without subprocess."""

    def test_compute_perfect_scores(self):
        sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
        import score
        scores = {"team": 10, "market": 10, "product": 10,
                  "demand": 10, "path": 10, "plan": 10}
        total, available, v, notes = score.compute(scores, 3)
        assert total == 100.0
        assert available == 100
        assert "Strong" in v
        assert len(notes) == 0

    def test_compute_with_unknowns(self):
        sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
        import score
        scores = {"team": 8, "market": 8, "product": None,
                  "demand": None, "path": 8, "plan": 8}
        total, available, v, notes = score.compute(scores, 2)
        # available weight = 30+20+10+10 = 70
        assert available == 70
        # total = (8/10*30 + 8/10*20 + 8/10*10 + 8/10*10) / 70 * 100
        # = (24 + 16 + 8 + 8) / 70 * 100 = 56/70*100 = 80.0
        assert total == 80.0

    def test_compute_all_none(self):
        sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
        import score
        scores = {"team": None, "market": None, "product": None,
                  "demand": None, "path": None, "plan": None}
        total, available, v, notes = score.compute(scores, 0)
        assert total is None
        assert "Cannot score" in v


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
