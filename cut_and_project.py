"""
HATWEAVE — cut-and-project sequence generator.

Generates a Sturmian sequence (a "mechanical word") using the classic
1D cut-and-project construction: step along a line with an irrational
slope, and mark 1 whenever the fractional position falls inside the
projection window, else 0.

With slope = golden-ratio conjugate (sqrt(5)-1)/2 and window = slope,
the output is the Fibonacci word — a perfectly ordered sequence that
never repeats.

EXPERIMENTAL / THEORETICAL ONLY. Not production cryptography.
See THESIS.md and DISCLAIMER.md.
"""

import numpy as np


def cut_and_project(length, slope, window_size):
    """Return a Sturmian sequence of 0s and 1s.

    length:      how many symbols to generate
    slope:       irrational slope (e.g. (sqrt(5)-1)/2 for Fibonacci)
    window_size: width of the projection window; also the long-run
                 frequency of 1s in the output
    """
    sequence = []
    for x in range(length):
        y = x * slope
        # Check if the point falls within the projection window
        if (y % 1) < window_size:
            sequence.append(1)
        else:
            sequence.append(0)
    return sequence


def check_sturmian(sequence):
    """Run the fingerprint checks for a golden-slope Sturmian word.

    Returns a dict of test results. For the Fibonacci word:
    - no '00' anywhere (balance property)
    - no '111' anywhere (balance property)
    - frequency of 1s approaches the window size as length grows
    """
    text = "".join(map(str, sequence))
    return {
        "no_double_zero": "00" not in text,
        "no_triple_one": "111" not in text,
        "ones_ratio": sum(sequence) / len(sequence) if sequence else 0.0,
    }


if __name__ == "__main__":
    length = 20
    slope = (np.sqrt(5) - 1) / 2  # golden-ratio conjugate
    window_size = slope

    seq = cut_and_project(length, slope, window_size)
    print(seq)

    checks = check_sturmian(seq)
    print("checks:", checks)
    print("target ratio (window):", round(window_size, 4))
