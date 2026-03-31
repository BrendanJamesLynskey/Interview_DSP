# FFT Algorithm: Interview Questions

## Overview

The Fast Fourier Transform (FFT) is among the most important algorithms in signal processing. Interview questions on this topic appear at every level, from junior DSP roles to senior algorithm engineers. Mastery requires understanding not just what the FFT computes, but why the divide-and-conquer structure achieves its complexity reduction, how in-place computation works, and where numerical precision issues arise.

---

## Tier 1: Fundamentals

### Q1. What does the DFT compute, and what is its direct computational complexity?

**Answer.**

The $N$-point Discrete Fourier Transform maps a length-$N$ sequence $x[n]$ to $N$ complex spectral coefficients $X[k]$:

$$X[k] = \sum_{n=0}^{N-1} x[n] \, W_N^{kn}, \quad k = 0, 1, \ldots, N-1$$

where $W_N = e^{-j2\pi/N}$ is the primitive $N$-th root of unity (the **twiddle factor base**).

**Direct complexity.** Each output bin $X[k]$ requires $N$ complex multiplications and $N-1$ complex additions. With $N$ output bins, the totals are:

- Multiplications: $N^2$
- Additions: $N(N-1) \approx N^2$

The direct DFT is therefore $O(N^2)$. For $N = 1024$ this is roughly $10^6$ operations; for $N = 2^{20} \approx 10^6$ it becomes $10^{12}$ — computationally prohibitive in real-time systems.

**Why $O(N^2)$ is the naive bound.** There are $N$ output values, each computed as an inner product of length $N$. Without exploiting any structure in $W_N^{kn}$, this is a dense matrix-vector multiply of an $N \times N$ matrix, inheriting $O(N^2)$.

**Common mistake.** Forgetting that the multiplications are *complex*. Each complex multiply costs 4 real multiplications and 2 real additions (or 3 real multiplications with the Karatsuba trick). This matters for hardware implementation but not for the big-O analysis.

---

### Q2. What two mathematical properties does the Cooley-Tukey FFT exploit to reduce complexity?

**Answer.**

The Cooley-Tukey algorithm exploits two symmetry properties of the twiddle factor $W_N^{kn}$:

**1. Periodicity:**

$$W_N^{kn} = W_N^{k(n+N)} = W_N^{(k+N)n}$$

The DFT kernel is periodic with period $N$ in both $k$ and $n$.

**2. Symmetry (complex conjugate symmetry):**

$$W_N^{k+N/2} = -W_N^k$$

This follows directly: $W_N^{k+N/2} = e^{-j2\pi(k+N/2)/N} = e^{-j2\pi k/N} \cdot e^{-j\pi} = -W_N^k$.

**How this leads to the algorithm.** A length-$N$ DFT (assume $N$ even) can be split into two length-$N/2$ DFTs applied to the even-indexed and odd-indexed samples. The butterfly recombination uses the conjugate symmetry to combine two $N/2$-point results into one $N$-point result at a cost of only $N/2$ complex multiplications per stage, rather than recomputing from scratch.

---

### Q3. Derive the radix-2 DIT decimation step. What recurrence results?

**Answer.**

Split $x[n]$ into even and odd subsequences:

$$X[k] = \sum_{n=0}^{N-1} x[n] W_N^{kn} = \sum_{m=0}^{N/2-1} x[2m] W_N^{2mk} + \sum_{m=0}^{N/2-1} x[2m+1] W_N^{(2m+1)k}$$

Since $W_N^{2mk} = W_{N/2}^{mk}$ (because $e^{-j2\pi(2m)k/N} = e^{-j2\pi mk/(N/2)}$):

$$X[k] = \underbrace{\sum_{m=0}^{N/2-1} x[2m] W_{N/2}^{mk}}_{G[k]} + W_N^k \underbrace{\sum_{m=0}^{N/2-1} x[2m+1] W_{N/2}^{mk}}_{H[k]}$$

So:

$$X[k] = G[k] + W_N^k H[k]$$

$$X[k + N/2] = G[k] - W_N^k H[k] \quad \text{(by conjugate symmetry)}$$

for $k = 0, 1, \ldots, N/2 - 1$.

$G[k]$ and $H[k]$ are each $N/2$-point DFTs, computable recursively. The recurrence for operation count $T(N)$ is:

$$T(N) = 2T(N/2) + \frac{N}{2}$$

Solving by the Master Theorem (or by unrolling $\log_2 N$ levels): $T(N) = \frac{N}{2}\log_2 N$ complex multiplications — $O(N \log N)$.

---

### Q4. What is a butterfly operation?

**Answer.**

A **butterfly** is the fundamental two-input, two-output computation unit of the FFT. Given two complex values $a$ and $b$, and twiddle factor $W$:

$$\text{Output}_1 = a + W \cdot b$$
$$\text{Output}_2 = a - W \cdot b$$

Diagrammatically, it resembles a butterfly shape (two crossing lines), giving the operation its name. One butterfly requires:
- 1 complex multiplication (computing $W \cdot b$)
- 2 complex additions

An $N$-point radix-2 FFT has $\log_2 N$ stages, each containing $N/2$ butterflies. Total butterflies: $\frac{N}{2}\log_2 N$.

**For stage $s$ (0-indexed), the twiddle factor is $W_N^{k \cdot 2^s}$ where $k$ indexes the butterfly within the stage.** At the first stage the twiddle factors cycle rapidly; at the last stage they cycle slowly.

---

### Q5. What is bit reversal and why is it needed?

**Answer.**

In a radix-2 DIT FFT computed in-place, the input samples must be reordered into **bit-reversed order** before processing begins.

**Why it arises.** Each DIT decomposition separates even-indexed elements (bit 0 = 0) from odd-indexed elements (bit 0 = 1). At each recursive level, the least-significant bit of the index is used for routing. After $\log_2 N$ levels of even/odd splitting, element originally at index $n$ ends up at index $\text{bitrev}(n)$ — the integer formed by reversing the $\log_2 N$-bit binary representation of $n$.

**Example for $N=8$ ($\log_2 8 = 3$ bits):**

| Original index | Binary | Bit-reversed | Permuted index |
|:-:|:-:|:-:|:-:|
| 0 | 000 | 000 | 0 |
| 1 | 001 | 100 | 4 |
| 2 | 010 | 010 | 2 |
| 3 | 011 | 110 | 6 |
| 4 | 100 | 001 | 1 |
| 5 | 101 | 101 | 5 |
| 6 | 110 | 011 | 3 |
| 7 | 111 | 111 | 7 |

**Implementation note.** In the standard Cooley-Tukey in-place algorithm, pairs $(n, \text{bitrev}(n))$ with $n < \text{bitrev}(n)$ are swapped. Indices where $n = \text{bitrev}(n)$ (fixed points) require no swap.

---

## Tier 2: Intermediate

### Q6. How does the radix-4 FFT improve on radix-2? Quantify the reduction in multiplications.

**Answer.**

The **radix-4 FFT** decomposes an $N$-point DFT ($N = 4^m$) into four $N/4$-point DFTs simultaneously, rather than two $N/2$-point DFTs.

**Decomposition.** Index $n$ is split as $n = 4m + r$, $r \in \{0,1,2,3\}$:

$$X[k] = \sum_{r=0}^{3} W_N^{rk} \sum_{m=0}^{N/4-1} x[4m+r] \, W_{N/4}^{mk}$$

**The key saving: trivial twiddles.** The four sub-DFT outputs are combined with twiddle factors $W_N^0 = 1$, $W_N^{N/4} = -j$, $W_N^{N/2} = -1$, $W_N^{3N/4} = +j$. Multiplication by $\pm 1$ and $\pm j$ requires no real multiplications (just sign changes and swapping real/imaginary parts). This makes the radix-4 butterfly computationally cheaper per stage.

**Operation count comparison (complex multiplications):**

| Algorithm | Complex multiplications |
|---|---|
| Direct DFT | $N^2$ |
| Radix-2 FFT | $\frac{N}{2}\log_2 N$ |
| Radix-4 FFT | $\frac{3N}{8}\log_2 N$ |
| Split-radix FFT | $\frac{N}{3}\log_2 N$ (approx.) |

Radix-4 saves approximately 25% of multiplications compared to radix-2, because each radix-4 butterfly replaces two radix-2 stages (4 butterflies) while doing fewer non-trivial multiplies.

**Constraint.** $N$ must be a power of 4. For $N$ a power of 2 but not 4 (e.g., $N = 32$), a mixed radix-4/radix-2 algorithm is used for the last stage.

---

### Q7. Explain the split-radix FFT. Why does it achieve fewer multiplications than radix-4?

**Answer.**

The **split-radix FFT** (Duhamel and Vetterli, 1984) applies radix-2 to even-indexed outputs and radix-4 to odd-indexed outputs. This exploits the fact that even-indexed outputs need only one recursive call (efficient), while odd-indexed outputs benefit from the trivial $\pm j$ twiddles of radix-4.

**Recurrence for the even/odd split:**

- Even outputs $X[2k]$: computed by a single $N/2$-point DFT of $\{x[n] + x[n+N/2]\}$
- Odd outputs $X[4k+1]$ and $X[4k+3]$: computed using two $N/4$-point DFTs with twiddle factors $W_N^n$ and $W_N^{3n}$

**Operation count.** The split-radix algorithm achieves:

$$\text{Real multiplications} = N\log_2 N - 3N + 4$$

For $N = 1024$: split-radix needs 7172 real multiplications, vs. radix-2 at 9216. That is about a 22% reduction.

**Why it is optimal (or near-optimal).** It was long conjectured that the split-radix count was optimal. In 2004 Frigo and Johnson showed via the FFTW framework that slightly better constants are achievable with mixed-radix strategies, but split-radix remains the gold standard for hand-coded implementations.

---

### Q8. How are twiddle factors computed and stored in a practical FFT implementation? What are the trade-offs?

**Answer.**

**Options for twiddle factor computation:**

**1. Precomputed lookup table.** Compute all $W_N^k = e^{-j2\pi k/N}$ for $k = 0, \ldots, N/2 - 1$ at initialisation and store in a table.
- Pro: No transcendental function calls during the FFT; maximum throughput.
- Con: Memory footprint of $N$ complex values ($16N$ bytes for double precision). For large $N$ (e.g., $N = 2^{20}$), this is 16 MB — may exceed cache.

**2. Recursive (incremental) computation.** At each stage, update twiddle factors using the recurrence $W_N^{k+1} = W_N^k \cdot W_N^1$.
- Pro: Only $O(1)$ storage needed.
- Con: Numerical error accumulates; the unit-magnitude constraint $|W_N^k| = 1$ is violated after many steps.

**3. On-the-fly trigonometric computation.** Call `sin`/`cos` for each twiddle factor as needed.
- Pro: No storage required, no accumulation error.
- Con: `sin`/`cos` are expensive; completely impractical for inner-loop use.

**4. Sine/cosine table with quarter-wave symmetry.** Store only $N/4$ values; use symmetry relations to recover all quadrants. Reduces table size by 4x.

**Practical recommendation.** For $N \leq 2^{16}$, a precomputed table with quarter-wave symmetry fits in L2 cache and is the standard approach (used in FFTW, KissFFT, etc.).

---

### Q9. Describe in-place computation. What memory layout does a radix-2 DIT FFT use, and what are the implications for cache performance?

**Answer.**

**In-place FFT.** The butterfly operation $[a, b] \to [a + Wb, a - Wb]$ writes its two outputs to the same memory locations as its two inputs. No auxiliary array is needed; the entire transform operates on a single array of $N$ complex values.

**Memory access pattern for radix-2 DIT:**

At stage $s$ (numbered from 0), butterflies operate on pairs of elements separated by a stride of $2^s$:

- Stage 0: stride 1 (adjacent pairs)
- Stage 1: stride 2
- Stage 2: stride 4
- ...
- Stage $\log_2 N - 1$: stride $N/2$

**Cache implications.**

- **Early stages** (small stride): excellent spatial locality. Both elements of a butterfly are close in memory and likely in the same cache line.
- **Late stages** (large stride): poor spatial locality for large $N$. Elements accessed together are $N/2$ apart — potentially many megabytes for large $N$. This causes cache misses.

**Cache-oblivious / 4-step FFT.** For large $N$, the array can be treated as an $\sqrt{N} \times \sqrt{N}$ matrix and the FFT decomposed into row DFTs, twiddle multiplication, and column DFTs. This keeps each sub-problem small enough to fit in cache, dramatically reducing cache miss rate. FFTW uses this approach.

---

### Q10. What is the computational complexity of computing $M$ different-length DFTs versus one large FFT? When is zero-padding appropriate?

**Answer.**

**Zero-padding for FFT length requirements.** The radix-2 FFT requires $N = 2^m$. If the signal has $L$ samples, zero-pad to the next power of two: $N = 2^{\lceil \log_2 L \rceil}$.

**Computational cost comparison.** Suppose you need spectral analysis of a length-$L$ signal:

| Approach | Operations |
|---|---|
| Direct DFT, no padding | $O(L^2)$ |
| FFT with zero-padding to $N = 2^{\lceil \log_2 L \rceil}$ | $O(N \log N)$, $N < 2L$ |
| Chirp-Z transform (arbitrary length $M$) | $O(N' \log N')$ where $N' = L + M - 1$ |

**When zero-padding is appropriate:**
- To use an efficient radix-2 (or radix-4) FFT on a non-power-of-2 length sequence.
- To improve the apparent frequency resolution of a spectrum (denser frequency grid), though this does **not** improve true spectral resolution (which depends on the observation length $L$, not $N$).
- For fast convolution (linear convolution via FFT): zero-pad both sequences to length $\geq L_1 + L_2 - 1$.

**When zero-padding is misleading.** Zero-padding interpolates the spectrum — it does not reveal frequency components closer than $1/L$ (the true resolution limit). Students often confuse the fine frequency grid from zero-padding with actual improved resolution.

---

## Tier 3: Advanced

### Q11. Derive the exact operation count for an $N$-point radix-2 DIT FFT, distinguishing trivial twiddle factors.

**Answer.**

**Setting up the count.** Define $T(N)$ as the number of non-trivial complex multiplications (i.e., excluding multiplication by $\pm 1$ and $\pm j$).

At each stage $s = 0, 1, \ldots, \log_2 N - 1$, there are $N/2$ butterflies. Of these, **the butterfly with twiddle $W_N^0 = 1$ is trivial** (no multiplication needed). At stage $s$, twiddles are $W_N^{k \cdot N/2^{s+1}}$ for $k = 0, 1, \ldots, 2^s - 1$, repeated $N/2^{s+1}$ times. Only $k=0$ is trivial per group, giving $2^s - 1$ non-trivial twiddles per group of $2^{s+1}$ butterflies.

**Stage-by-stage count:**

| Stage $s$ | Groups | Non-trivial twiddles per group | Total non-trivial mults |
|:-:|:-:|:-:|:-:|
| 0 | $N/2$ | 0 | 0 |
| 1 | $N/4$ | 1 | $N/4$ |
| 2 | $N/8$ | 3 | $3N/8$ |
| $s$ | $N/2^{s+1}$ | $2^s - 1$ | $(2^s - 1)N/2^{s+1}$ |

Summing over $s = 0$ to $\log_2 N - 1$:

$$T_{\times}(N) = \sum_{s=0}^{\log_2 N - 1} \frac{(2^s - 1)N}{2^{s+1}} = \frac{N}{2}\log_2 N - (N-1) \approx \frac{N}{2}\log_2 N - N$$

**Additions.** Every butterfly requires 2 complex additions regardless of twiddle value:

$$T_+(N) = N \log_2 N$$

**Summary.** For $N = 1024$:
- Naive DFT: $1{,}048{,}576$ complex multiplications
- Radix-2 FFT: $\frac{1024}{2} \cdot 10 - 1023 \approx 4097$ non-trivial complex multiplications — a speedup of over 250x.

---

### Q12. Explain the prime-factor algorithm (Good-Thomas) and when it outperforms Cooley-Tukey.

**Answer.**

**The Good-Thomas (Prime-Factor) Algorithm.** When $N = N_1 \cdot N_2$ with $\gcd(N_1, N_2) = 1$ (coprime factors), the Chinese Remainder Theorem (CRT) maps the 1D DFT index $n \in [0, N)$ to a 2D index $(n_1, n_2) \in [0, N_1) \times [0, N_2)$ such that **no twiddle factors appear in the recombination**.

The index mapping is:

$$n = (N_2 \cdot (N_2^{-1} \bmod N_1) \cdot n_1 + N_1 \cdot (N_1^{-1} \bmod N_2) \cdot n_2) \bmod N$$

**Why no twiddle factors?** The CRT mapping arranges the 2D DFT so that the cross-terms $W_N^{n_1 k_2 N_2 + n_2 k_1 N_1}$ factor completely into $W_{N_1}^{n_1 k_1} \cdot W_{N_2}^{n_2 k_2}$. This is only possible when $N_1$ and $N_2$ are coprime — otherwise residue classes overlap.

**Operation count.** With no twiddle multiplications, the cost is just $N_1$ DFTs of size $N_2$ plus $N_2$ DFTs of size $N_1$:

$$T(N) = N_1 T(N_2) + N_2 T(N_1)$$

For $N = 15 = 3 \times 5$: 3 five-point DFTs + 5 three-point DFTs, with no twiddle multiplications. Cooley-Tukey for $N=15$ would require zero-padding to $N=16$, wasting computation.

**When Good-Thomas wins.**
- $N$ has many small coprime factors (e.g., $N = 2 \cdot 3 \cdot 5 \cdot 7 = 210$).
- Hardware with expensive multiplication favours the elimination of twiddle factors.
- Signal length is naturally non-power-of-2 (avoiding zero-padding waste).

**Limitation.** The CRT index mapping is a non-contiguous permutation — harder to implement than bit reversal and less cache-friendly.

---

### Q13. What numerical precision issues arise in long FFTs? How do rounding errors scale with $N$?

**Answer.**

**Error model.** Let $\epsilon_{\text{mach}}$ be the floating-point machine epsilon ($\approx 1.1 \times 10^{-16}$ for double precision, $\approx 1.2 \times 10^{-7}$ for single). Each floating-point operation introduces a relative error of order $\epsilon_{\text{mach}}$.

**Error propagation in the FFT.** An $N$-point FFT has $\log_2 N$ stages. Rounding errors accumulate as a random walk (errors are approximately uncorrelated), giving an RMS rounding error that scales as:

$$\sigma_{\text{err}} \approx O\!\left(\epsilon_{\text{mach}} \sqrt{\log_2 N}\right) \cdot \|x\|_2$$

More precisely, for the Cooley-Tukey FFT, the rounding error in the output satisfies:

$$\|\hat{X} - X\|_2 \lesssim c \, \epsilon_{\text{mach}} \sqrt{N \log_2 N} \, \|x\|_2$$

where $c$ is a small constant depending on the implementation. The $\sqrt{\log_2 N}$ factor reflects the $\log_2 N$ stages with square-root-of-sum accumulation.

**Comparison to direct DFT.** Direct DFT error scales as $O(\epsilon_{\text{mach}} \sqrt{N}) \cdot \|x\|_2$. For large $N$, the FFT is actually *more* accurate than the direct DFT despite using the same arithmetic, because fewer operations are involved.

**Practical implications.**
- For $N = 2^{20}$ in double precision: $\sqrt{20} \approx 4.5$, so about 14.6 decimal digits of accuracy remain — generally adequate.
- For single precision with $N = 2^{20}$: $\sqrt{20} \times 1.2 \times 10^{-7} \approx 5 \times 10^{-7}$ relative error — borderline for some applications.
- Long convolution (FFT-based) can lose 2–3 bits of precision for very long filters; double precision is advisable.

**Numerical stability improvements.**
- Precomputed twiddle tables avoid recursive sine/cosine error.
- Rescaling intermediate values prevents overflow/underflow in fixed-point implementations.
- The four-step algorithm reduces the maximum intermediate magnitude by spreading computations.

---

### Q14. How does the FFTW library determine its optimal FFT plan, and what algorithmic strategies does it combine?

**Answer.**

**FFTW (Fastest Fourier Transform in the West)** uses an adaptive planning strategy at runtime to select among a large space of FFT algorithms.

**Planning.** Before transforming data, FFTW runs a set of benchmark computations (`fftw_plan_dft`) to measure wall-clock time for different algorithmic decompositions. Plans range from:
- `FFTW_ESTIMATE`: heuristic choice, no measurement (fast planning, suboptimal transform)
- `FFTW_MEASURE`: benchmarks a few plans
- `FFTW_PATIENT`: exhaustive search across many decompositions
- `FFTW_EXHAUSTIVE`: complete search including unusual strategies

**Algorithmic strategies combined:**
1. **Cooley-Tukey (radix-2, radix-4, mixed-radix):** for powers of 2 and highly composite $N$.
2. **Split-radix:** for reducing multiplication count.
3. **Good-Thomas (PFA):** for coprime factor decompositions with no twiddle factors.
4. **Rader's algorithm:** for prime-length DFTs — converts a prime-$p$ DFT into a cyclic convolution of length $p-1$ (which is composite), then applies a standard FFT.
5. **Bluestein's chirp-Z algorithm:** handles arbitrary $N$ via a convolution embedding.
6. **Vector codelets:** hand-optimised SIMD kernels (SSE, AVX, AVX-512) for small fixed sizes (2, 4, 8, 16, 32). These are generated automatically by a code generator (genfft).
7. **Cache-oblivious 4-step (6-step) algorithm:** for large $N$ exceeding cache, restructures as matrix DFTs to maximise cache reuse.

**Why runtime planning matters.** The optimal algorithm depends on $N$, hardware cache sizes, SIMD width, and memory bandwidth — quantities that FFTW cannot know at compile time. By measuring directly, FFTW typically achieves within 2–3x of theoretical peak on modern hardware.

---

## Quick Reference: Key Formulas

| Quantity | Formula |
|---|---|
| DFT definition | $X[k] = \sum_{n=0}^{N-1} x[n] W_N^{kn}$ |
| Twiddle factor | $W_N = e^{-j2\pi/N}$ |
| Conjugate symmetry | $W_N^{k+N/2} = -W_N^k$ |
| Radix-2 butterfly | $X[k] = G[k] + W_N^k H[k]$, $X[k+N/2] = G[k] - W_N^k H[k]$ |
| Complexity | $O(N^2)$ direct, $O(N\log N)$ FFT |
| Multiplications (radix-2) | $\frac{N}{2}\log_2 N - (N-1)$ non-trivial |
| Additions (radix-2) | $N\log_2 N$ |
| RMS rounding error | $O(\epsilon_{\text{mach}} \sqrt{\log_2 N}) \cdot \|x\|_2$ |
