# HATWEAVE

## A Research Study: Aperiodic Geometry as a Candidate Substrate for Quantum-Resistant Encryption

### A thesis on cut-and-project keystreams drawn from the hat monotile family

**Author:** Kenneth Lee Blum Jr. (Ken Blum), Sioux Falls, South Dakota
**With research assistance from:** Lux (Muse AI)
**Date:** October 25, 2026
**Status:** Theoretical research concept. Experimental only — **not production cryptography.** See the Disclaimer.

---

## Abstract

Modern public-key encryption rests on mathematical problems — factoring large integers and computing discrete logarithms — that a sufficiently powerful quantum computer can solve efficiently using Shor's algorithm. This thesis explores a different foundation for secrecy: **aperiodic geometry**. Using *cut-and-project* schemes, higher-dimensional lattices can be projected through an irrationally angled window to produce **Sturmian sequences** — symbol streams that are perfectly deterministic yet never repeat. Using the **hat monotile**, the aperiodic tile discovered in 2023, the same idea extends from one-dimensional sequences into two-dimensional geometric structures. We present a small, verified reference implementation that generates the Fibonacci–Sturmian word from the golden-ratio conjugate slope, demonstrate its defining properties (balance, non-periodicity, frequency convergence), and propose a construction in which geometric parameters serve as key material and *geometry disruption* serves as a built-in tamper alarm. We argue that such a construction presents no periodic structure for quantum period-finding to exploit. We also state the hard problems honestly: raw Sturmian sequences are low-complexity and therefore predictable if their parameters are known, so a secure system requires nonlinear mixing layers, exact arithmetic, and public cryptanalysis that has not yet been performed. "Unbreakable" is the research goal of this project, not a claim about its present state.

---

## 1. The problem: quantum computers break today's locks

Nearly all secure communication on the internet — banking, messaging, medical records — is protected by public-key systems such as RSA and elliptic-curve cryptography. Their security depends on the practical impossibility of factoring very large numbers or solving discrete logarithms with classical computers.

In 1994, Peter Shor showed that a quantum computer can solve both problems in polynomial time. A *cryptographically relevant quantum computer* does not yet exist, but the threat is already active in one specific way: **"harvest now, decrypt later."** An adversary can record encrypted traffic today and decrypt it the day a capable quantum computer switches on. Any secret that must stay secret for decades — medical files, government records, a person's private life — is already at risk.

The mainstream response, *post-quantum cryptography* (PQC), replaces the old problems with new ones believed to resist quantum attack. In August 2024, NIST standardized the first PQC algorithms (ML-KEM, ML-DSA, SLH-DSA), built largely on structured lattices and hash functions. This thesis does not compete with that work. It asks a different question:

> **Can secrecy be built out of geometry that never repeats — geometry with no period for a quantum computer to find?**

## 2. The building blocks

### 2.1 Aperiodic order and the hat tile

A crystal repeats. A **quasicrystal** does not — yet it is far from random: it has strict long-range order without any repeating unit. Aperiodic tilings are the two-dimensional picture of this idea. Penrose tilings showed in the 1970s that a plane can be tiled in perfect order that never becomes periodic, but they required two different tile shapes.

In March 2023, David Smith, Joseph Samuel Myers, Craig S. Kaplan, and Chaim Goodman-Strauss announced the **hat tile**: a single 13-sided shape — one tile, "einstein" (German: *one stone*) — that tiles the plane **only** aperiodically. One shape, forced by geometry itself to never repeat. This project takes the hat tile's family as its namesake and its two-dimensional inspiration.

### 2.2 Cut-and-project: order from a higher dimension

Aperiodic structures are not found; they are *manufactured* — by projection. The **cut-and-project scheme** works as follows:

1. Start with an ordinary, perfectly periodic lattice in a higher-dimensional space (for example, the integer grid ℤ² in the plane).
2. Cut a strip through that lattice at an **irrational slope** — an angle that never lines up with the grid.
3. Project the lattice points inside the strip down onto a line.

Because the slope is irrational, the projected pattern can never repeat — yet every point in it is exactly determined. Order without repetition. This is the standard construction behind mathematical quasicrystals (model sets, in the sense of Meyer and de Bruijn).

### 2.3 Sturmian sequences

The one-dimensional output of cut-and-project is a **Sturmian sequence**: an infinite word over two symbols with the lowest possible complexity of any non-repeating sequence. Its classical construction is the *mechanical word*: for an irrational slope α and a window of the same size,

> **s(n) = 1 if frac(nα) < α, else 0**

With α set to the golden-ratio conjugate, (√5 − 1)/2 ≈ 0.618, the result is the celebrated **Fibonacci word** — the canonical example of perfect aperiodic order.

## 3. The reference implementation, verified

The following Python function is the working heart of this project. It is deliberately small — a thesis you can run.

```python
import numpy as np

def cut_and_project(length, slope, window_size):
    sequence = []
    for x in range(length):
        y = x * slope
        if (y % 1) < window_size:
            sequence.append(1)
        else:
            sequence.append(0)
    return sequence

length = 20
slope = (np.sqrt(5) - 1) / 2     # golden-ratio conjugate
window_size = slope

print(cut_and_project(length, slope, window_size))
```

**Output (executed and verified October 25, 2026):**

```
[1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
```

Three fingerprint tests confirm this is a genuine Sturmian word and not noise:

- **Balance.** The word contains no `00` and no `111` anywhere. A Sturmian word is *balanced*: any two windows of the same length differ in their count of 1s by at most one. Random bits would fail this test almost immediately.
- **Frequency convergence.** The proportion of 1s is 12/20 = 0.600 at length 20 and converges to exactly the window size, 0.618…, as length grows — the signature of the irrational slope controlling the stream.
- **Non-periodicity.** No block of the sequence repeats as a period, at any length, and this is guaranteed by the irrationality of the slope rather than observed by sampling. This third property is the one the rest of the thesis is built on.

## 4. The proposed construction

We propose a symmetric encryption design, working name **HATWEAVE**, with four layers:

1. **Key = geometry.** The secret key is a set of geometric parameters: the slope(s) α, the projection intercept (phase), the window size, and — in the two-dimensional version — a substitution path through a hat-tile patch. Where an ordinary cipher's key is a string of bits, this key is a *place in a continuous geometric space*.
2. **Keystream = cut-and-project.** Encryption and decryption both regenerate the same aperiodic stream from the key, exactly as both sides of a stream cipher regenerate a keystream. The plaintext is combined with the stream (for example by XOR) to produce ciphertext.
3. **Mixing layer (required, not optional).** As Section 6 states plainly, a raw Sturmian stream is too structured to use alone. Practical keystream output must pass through nonlinear combination — multiple streams at incommensurate slopes combined through a nonlinear function — before it touches plaintext.
4. **Integrity = geometry disruption.** A valid keystream corresponds to a valid, unbroken geometric structure. If ciphertext is altered, the regenerated structure fails its balance and tiling constraints in a *detectable location* — the geometric equivalent of a tripwire. In the author's earlier framework work, this is expressed as: tampering disrupts the geometry, and the disruption itself is the alarm. Conventional ciphers bolt integrity on as a separate tag; here it is a property of the medium.

## 5. The quantum argument

The case for quantum resistance rests on three points:

1. **There is no period to find.** Shor's algorithm is, at its core, a *period-finding* machine: it breaks RSA by finding the period of modular exponentiation. An aperiodic keystream has no period — not a long one, not a hidden one, none. The central trick of quantum cryptanalysis has no purchase here.
2. **The security does not rest on factoring or discrete logarithms.** Nothing in the construction reduces to the hidden subgroup problem over the groups Shor's algorithm exploits.
3. **Grover is the only generic quantum lever, and it is a known, priceable one.** Grover's algorithm gives a quadratic speedup on brute-force search. The standard countermeasure — double the effective key size — applies here unchanged.

Stated carefully: the claim of this thesis is not "this is proven unbreakable." The claim is that the construction **removes the specific structures quantum algorithms are known to exploit**, and relocates security into a mathematical territory — aperiodic order — where no quantum attack is currently known. That territory deserves exploration precisely because the harvest-now-decrypt-later clock is already running.

## 6. The hard problems, stated honestly

A thesis that hides its weaknesses protects no one. Four problems stand between this concept and any real-world use:

1. **Sturmian sequences are low-complexity.** Their subword complexity is exactly *n* + 1 — the minimum possible for a non-periodic word. This means a raw Sturmian stream is highly structured: an attacker who learns or guesses the geometric parameters can regenerate the entire stream, and partial knowledge constrains the rest. The mixing layer of Section 4 is therefore load-bearing, and its design is the project's central open problem.
2. **Floating-point arithmetic is not a foundation.** Two machines computing `frac(nα)` in floating point will eventually disagree, and encryption and decryption would desynchronize. A serious implementation must work in exact arithmetic — for the golden-ratio family, in the ring ℤ[√5] — or with explicitly shared rational approximations.
3. **Key distribution is untouched.** This construction, like all symmetric systems, assumes both parties already share the geometric key. It does not by itself solve the problem public-key cryptography solves.
4. **No cryptanalysis has been performed.** No peer review, no published attack attempts, no statistical test-suite results (e.g., the NIST STS battery) exist yet for this construction. Until they do, every statement about its strength is a hypothesis.

## 7. Research roadmap

1. **Exact-arithmetic reference implementation** of cut-and-project generation (integer arithmetic in ℤ[√5]; no floats anywhere in the pipeline).
2. **Multi-stream mixing prototype:** several Sturmian streams at incommensurate slopes, nonlinearly combined; measure output complexity and statistical profile.
3. **Statistical validation:** run generated streams through the NIST Statistical Test Suite and TestU01; publish results either way.
4. **Two-dimensional prototype:** keystream generation from hat-tile substitution patches, so the key is a geometric structure rather than a one-dimensional parameter set.
5. **Formalize geometry disruption:** define exactly which tampering the balance/tiling constraints detect, and where the detection boundary lies.
6. **Publish openly for attack.** A construction nobody has tried to break is a construction nobody should trust. This document itself is step one of that process.

## 8. Conclusion

Privacy's next era will not be won by slightly larger versions of the mathematics quantum computers already know how to eat. It will be won in stranger territory. Aperiodic geometry — order without repetition, structure without a period — is such a territory, and the hat tile's arrival in 2023 handed it a flagship. The cut-and-project construction in this thesis is small enough to run in a dozen lines of Python and deep enough to build a research program on. Its author's position is simple: the future of privacy is hiding in geometry that never repeats — and the work of proving it starts here, in the open.

---

## Disclaimer

HATWEAVE is an experimental, theoretical research concept by an independent researcher. It has **not** been peer-reviewed, has **not** undergone professional cryptanalysis, and must **never** be used to protect real data. For real-world post-quantum security today, use the NIST-standardized algorithms (ML-KEM / FIPS 203, ML-DSA / FIPS 204, SLH-DSA / FIPS 205). This document exists to explore an idea rigorously and honestly — including its flaws.

## References (starting points)

- Smith, D., Myers, J. S., Kaplan, C. S., Goodman-Strauss, C. (2023). *An aperiodic monotile.* (The "hat tile" paper.)
- Shor, P. W. (1994). *Algorithms for quantum computation: discrete logarithms and factoring.*
- Lothaire, M. (2002). *Algebraic Combinatorics on Words* — chapter on Sturmian words.
- Baake, M., & Grimm, U. (2013). *Aperiodic Order, Vol. 1: A Mathematical Invitation* — cut-and-project schemes and model sets.
- NIST (2024). FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA).
- Blum, K. (2026). *New Geometry Encrypted Tactical System* — companion experimental repository (geometry-disruption intrusion detection).
