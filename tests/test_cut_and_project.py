"""Tests for the HATWEAVE cut-and-project generator."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cut_and_project import cut_and_project, check_sturmian

GOLDEN = (math.sqrt(5) - 1) / 2  # ~0.6180339887


def test_fibonacci_word_prefix():
    """The first 20 symbols must match the verified Fibonacci word."""
    seq = cut_and_project(20, GOLDEN, GOLDEN)
    assert seq == [1, 0, 1, 0, 1, 1, 0, 1, 0, 1,
                   1, 0, 1, 1, 0, 1, 0, 1, 1, 0]


def test_balance_no_double_zero_no_triple_one():
    """Sturmian balance: no '00' and no '111' at golden slope."""
    checks = check_sturmian(cut_and_project(500, GOLDEN, GOLDEN))
    assert checks["no_double_zero"]
    assert checks["no_triple_one"]


def test_frequency_converges_to_window():
    """Frequency of 1s converges to the window size."""
    seq = cut_and_project(5000, GOLDEN, GOLDEN)
    ratio = sum(seq) / len(seq)
    assert abs(ratio - GOLDEN) < 0.01


def test_never_periodic_prefix():
    """No small period reproduces the sequence (aperiodicity spot-check)."""
    seq = cut_and_project(200, GOLDEN, GOLDEN)
    for period in range(1, 50):
        assert seq != [seq[i % period] for i in range(200)]
