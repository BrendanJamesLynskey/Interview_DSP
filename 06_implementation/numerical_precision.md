# Numerical Precision in DSP — Interview Questions

## Overview

Numerical precision problems are responsible for subtle, hard-to-reproduce bugs in DSP systems. This topic covers quantisation noise modelling, limit cycles, coefficient sensitivity, double vs. single precision trade-offs, and the tools used to analyse precision requirements. Essential for any role involving algorithm implementation, ASIC verification, or signal-to-noise specification.

---

## Tier 1: Fundamentals

### Q1. What is the quantisation noise model and when is it valid?

**Answer:**

**The model:** When a continuous-amplitude signal $x$ is quantised to a $W$-bit word with step size $\Delta = 2^{1-W}$ (full-scale $\pm 1$), the quantisation error is:

$$e = x_q - x, \quad e \in [-\Delta/2,\, +\Delta/2)$$

**Assumptions for the white noise model:**
1. The quantisation error is uniformly distributed: $e \sim \mathcal{U}(-\Delta/2, +\Delta/2)$
2. The error sequence $e[n]$ is white (uncorrelated between samples)
3. $e[n]$ is independent of the input signal $x[n]$
4. The input has many quantisation levels ($W \geq 8$) and is broadband

**Noise variance:**
$$\sigma_e^2 = \frac{\Delta^2}{12} = \frac{2^{2-2W}}{12}$$

**When the model fails:**

| Condition | Failure mode |
|---|---|
| Narrowband or sinusoidal input | Quantisation error is correlated and harmonic, not white |
| Low word length ($W < 6$) | Granularity too coarse; uniform distribution invalid |
| Input near a single quantisation level | Granular noise (limit cycles) |
| DC input | Quantisation error is a fixed bias, not noise |

When the model fails, measured SQNR will differ significantly from the theoretical $6.02W - 1.76$ dB. Validation by simulation is required.

---

### Q2. What is Signal-to-Quantisation-Noise Ratio (SQNR) and how is it computed?

**Answer:**

SQNR is the ratio of the signal power to the quantisation noise power in a system, measured in dB:

$$\text{SQNR} = 10\log_{10}\!\left(\frac{\sigma_x^2}{\sigma_e^2}\right)$$

**For a full-scale sinusoid** of amplitude $A = 1$ (peak-to-peak = 2, using all $2^W$ levels):

$$\sigma_x^2 = \frac{A^2}{2} = \frac{1}{2}, \quad \sigma_e^2 = \frac{\Delta^2}{12} = \frac{(2^{1-W})^2}{12} = \frac{2^{2-2W}}{12}$$

$$\text{SQNR} = 10\log_{10}\!\left(\frac{1/2}{2^{2-2W}/12}\right) = 10\log_{10}\!\left(\frac{12 \cdot 2^{2W-2}}{2}\right) = 10\log_{10}\!\left(\frac{3 \cdot 2^{2W}}{2}\right)$$

$$\boxed{\text{SQNR} \approx 6.02W - 1.76 \quad \text{dB}}$$

**Effect of signal level:** If the signal is $L$ dB below full scale, the signal power decreases by $L$ dB while the quantisation noise remains the same:

$$\text{SQNR}_{actual} = 6.02W - 1.76 - L \quad \text{dB}$$

**Importance:** For a 16-bit ADC ($W = 16$): SQNR = $6.02 \times 16 - 1.76 = 94.5$ dB. If a signal of interest is 60 dB below full scale, SQNR drops to $94.5 - 60 = 34.5$ dB — only ~6-bit effective precision for that signal component.

---

### Q3. What is the difference between truncation and rounding as quantisation methods? How do they affect SQNR?

**Answer:**

**Truncation (floor):** Discard the fractional bits, round toward negative infinity.

Error: $e_{trunc} \in [-\Delta, 0)$ — always non-positive.

- Mean (bias): $\mu_e = -\Delta/2$
- Variance: $\sigma_e^2 = \Delta^2/12$

**Rounding (round-half-up):** Round to the nearest integer. For values exactly halfway, round up.

Error: $e_{round} \in [-\Delta/2, +\Delta/2)$ — centred on zero.

- Mean (bias): $\mu_e \approx 0$ (small positive bias at midpoints)
- Variance: $\sigma_e^2 = \Delta^2/12$

**Comparison:**

| Property | Truncation | Rounding |
|---|---|---|
| Noise variance | $\Delta^2/12$ | $\Delta^2/12$ |
| DC bias | $-\Delta/2$ | $\approx 0$ |
| Effect in recursive filter | DC offset in output | Clean output |
| Hardware complexity | Simplest (drop bits) | 1 adder + 1 comparator |

Both have the same white noise variance, but truncation introduces a DC offset. In a simple FIR filter, the DC offset is just $\text{bias} \times H(e^{j0})$, which can be computed and tolerated. In a recursive (IIR) filter, the DC bias recirculates through the loop gain: the steady-state DC output error is $\mu_e / (1 - \sum a_k)$, which can be significant for filters with poles near DC.

**Best practice:** Use convergent rounding (round-half-to-even) in recursive filters. Use truncation only in feed-forward paths where the bias effect is bounded.

---

### Q4. What is an overflow oscillation in an IIR filter and how is it prevented?

**Answer:**

**Overflow oscillation** is a large-amplitude periodic signal that appears in a fixed-point IIR filter output when the accumulator overflows with two's complement wrapping arithmetic.

**Mechanism:** Consider a second-order IIR filter (resonator) with poles near the unit circle. The filter's natural response is a sinusoid. If the accumulator overflows and wraps (sign change), the filter state is set to a large negative value from what was a large positive value. The filter then rings back up, overflows again, and the cycle repeats — producing a sustained oscillation at approximately the filter's resonant frequency but at full amplitude.

**Key property:** Overflow oscillations are **not** bounded by the input signal — they continue at full scale even with zero input after the initial overflow event. They are also extremely sensitive to the exact pole locations.

**Prevention:**

1. **Saturation arithmetic**: Replace two's complement wrap with clamping to $[x_{min}, x_{max}]$. With saturation:
   - The accumulator clips to $\pm$ full scale instead of wrapping
   - The filter may distort (clipping artefact) but the oscillation cannot self-sustain
   - Mathematically: saturating arithmetic is bounded-input bounded-output (BIBO) stable for any stable filter

2. **Sufficient headroom**: Scale the filter's input to ensure the maximum signal level never saturates. The filter's $H_\infty$ norm ($\max_\omega |H(e^{j\omega})|$) bounds the maximum gain:
   $$|y[n]| \leq \|h\|_1 \cdot \max_n |x[n]|$$
   Scale the input down by $\|h\|_1$ to guarantee no overflow.

3. **Second-order section cascade**: High-order filters with poles near the unit circle are unstable under overflow; breaking into biquads reduces individual section gains.

---

## Tier 2: Intermediate

### Q5. Explain the effect of coefficient quantisation on FIR filter frequency response. How do you quantise coefficients correctly?

**Answer:**

**FIR frequency response sensitivity:** For an $N$-tap FIR with coefficients $h[k]$, the frequency response is:

$$H(e^{j\omega}) = \sum_{k=0}^{N-1} h[k]\, e^{-j\omega k}$$

Quantising each coefficient by adding an error $\delta_k$:

$$H_q(e^{j\omega}) = \sum_{k=0}^{N-1} (h[k] + \delta_k)\, e^{-j\omega k} = H(e^{j\omega}) + \underbrace{\sum_k \delta_k e^{-j\omega k}}_{E(e^{j\omega})}$$

The frequency response error $E(e^{j\omega})$ is bounded by:

$$|E(e^{j\omega})| \leq \sum_{k=0}^{N-1} |\delta_k| \leq N \cdot \frac{\Delta}{2}$$

where $\Delta$ is the coefficient quantisation step.

**Practical implications:**

1. **Passband ripple increase**: The error adds to the passband ripple. For a filter with $\delta_{pass} = 0.01$ design ripple and $N = 64$ taps at Q15: worst-case addition $= 64 \times 2^{-16}/2 = 9.8 \times 10^{-4}$ — acceptable (1% of design ripple).

2. **Stopband degradation**: The stopband attenuation is directly limited by coefficient precision. A 60 dB stopband requires $|\delta_k| \ll 10^{-3}$, requiring $\lceil -\log_2(10^{-3})\rceil = 10$ fractional bits minimum. Q15 (15 fractional bits) is sufficient.

**Correct quantisation procedure:**

1. Design coefficients in double precision floating-point.
2. Identify the largest coefficient magnitude $|h|_{max}$.
3. Scale coefficients so $|h|_{max} \leq 1 - 2^{-(W-1)}$ (fits in the Q-format without overflow).
4. Round to $W$ bits using convergent rounding.
5. Verify the quantised frequency response meets specifications.
6. If stopband degrades: increase $W$ or use sections with smaller coefficient ranges.

---

### Q6. Compare single-precision (float32) and double-precision (float64) for DSP algorithms. When must you use float64?

**Answer:**

**IEEE 754 formats:**

| Format | Exponent bits | Mantissa bits | Decimal digits | Range |
|---|---|---|---|---|
| float32 | 8 | 23 | ~7 | $\pm 3.4 \times 10^{38}$ |
| float64 | 11 | 52 | ~15 | $\pm 1.8 \times 10^{308}$ |

**Precision comparison (mantissa):**

- float32: $2^{-23} \approx 1.19 \times 10^{-7}$ relative precision
- float64: $2^{-52} \approx 2.22 \times 10^{-16}$ relative precision

**Performance:**

| Platform | float32 throughput | float64 throughput |
|---|---|---|
| x86-64 (AVX2) | 8 ops/cycle | 4 ops/cycle |
| Cortex-M4F | 1 op/cycle | ~25 cycles (software emulated) |
| GPU (CUDA) | 4000 GFLOPS | 100–200 GFLOPS |
| FPGA | 1 resource | 2–3× resources |

**When float32 is sufficient:**

- Audio signal processing (SNR needs $\leq 120$ dB, float32 gives $\sim 150$ dB SQNR)
- Radio frequency: Most DSP blocks in SDR
- Neural network inference
- Real-time embedded DSP (M4F/M7 FPU only supports float32)

**When float64 is required:**

1. **Filter coefficient design**: Designing an 8th-order IIR filter using float32 arithmetic can fail due to numerical cancellation in the polynomial root-finding. Always design in float64, then quantise to float32 or fixed-point.

2. **High-precision spectral analysis**: Computing a DFT of a 1 million-sample signal in float32 accumulates rounding errors; float64 preserves precision.

3. **Accumulation of many small values**: Summing $10^6$ values of magnitude $1.0$: the sum exceeds float32 precision ($\sim 10^6 > 2^{23} \approx 8 \times 10^6$... marginal), but float64 handles up to $\sim 10^{15}$.

4. **Geolocation, navigation (GPS)**: Coordinate arithmetic at sub-mm precision over global scale requires float64.

5. **Algorithm validation reference model**: Always compute the "golden reference" in float64, even if the production algorithm uses float32 or fixed-point.

**Kahan summation:** For summing many float32 values, Kahan's compensated summation algorithm provides float64-equivalent accuracy at the cost of extra adds:

```c
float sum = 0.0f, c = 0.0f;
for (int i = 0; i < N; i++) {
    float y = arr[i] - c;     // compensation
    float t = sum + y;
    c = (t - sum) - y;        // capture rounding error
    sum = t;
}
```

---

### Q7. What is the effect of finite precision on FFT computation? How does the number of bits required scale with FFT size?

**Answer:**

**Bit growth in FFT:** The radix-2 FFT butterfly computes:

$$A' = A + W \cdot B, \quad B' = A - W \cdot B$$

where $W = e^{-j2\pi k/N}$ is a twiddle factor. The magnitude of $A'$ can be up to $|A| + |W||B| = |A| + |B|$ — a potential increase of up to $\sqrt{2}$ per butterfly stage (average, not worst case) when $A$ and $B$ are uncorrelated.

**For an $N = 2^M$-point FFT:** There are $M = \log_2 N$ butterfly stages. Each stage can increase the magnitude by a factor $\leq 2$ in the worst case.

**Maximum output magnitude:** $|X[k]|_{max} \leq N \cdot \max_n |x[n]|$

To prevent overflow, one guard bit per FFT stage is needed, requiring $\lceil \log_2 N \rceil$ total guard bits.

**For $N = 1024$:** $\log_2 1024 = 10$ guard bits required above the input word length.

**Fixed-point FFT word length requirement:**

$$W_{FFT} = W_{input} + \lceil \log_2 N \rceil = W_{input} + M$$

For $W_{input} = 16$ bits and $N = 1024$: $W_{FFT} = 16 + 10 = 26$ bits → use 32-bit fixed-point.

**Floating-point FFT precision:** For a float32 FFT of length $N$, the round-off noise grows as $O(\log_2 N \cdot \epsilon_m)$ where $\epsilon_m = 2^{-23}$. The SNR of the FFT output is approximately:

$$\text{SNR}_{FFT} \approx 20\log_{10}(1/\epsilon_m) - 10\log_{10}(\log_2 N) \approx 138 - 3\log_2 N \quad \text{dB}$$

For $N = 4096$ ($\log_2 N = 12$): SNR $\approx 138 - 36 = 102$ dB. Still excellent for most DSP applications. Float64 would give $\approx 300$ dB — essentially perfect.

---

## Tier 3: Advanced

### Q8. Derive the noise power at the output of an IIR filter due to product quantisation noise, and explain why biquad cascade ordering matters.

**Answer:**

**Model:** In a fixed-point IIR filter, each multiply-accumulate operation introduces a rounding error $e[n]$ with variance $\sigma_e^2 = \Delta^2/12$. These rounding noise sources can be modelled as white noise injected at various points in the signal flow graph.

**For a Direct Form II IIR, noise injection points:**

Each multiplier in the forward and feedback path generates a noise source. For a first-order IIR $H(z) = b_0 / (1 - az^{-1})$:

- Feedback multiply: $a \cdot w[n-1]$ generates noise $e_1[n]$
- Forward multiply: $b_0 \cdot w[n]$ generates noise $e_2[n]$

Both noise sources are filtered by the transfer function seen from the injection point to the output. For noise injected at the state variable node, the noise passes through:

$$H_{noise}(z) = \frac{1}{1 - az^{-1}}$$

The output noise power is:

$$\sigma_{out}^2 = \sigma_e^2 \cdot \sum_{n=0}^{\infty} |h_{noise}[n]|^2 = \sigma_e^2 \cdot \frac{1}{1 - a^2}$$

For $a = 0.99$ (pole very close to unit circle): $\frac{1}{1 - 0.99^2} = \frac{1}{0.0199} \approx 50$. The output noise is **50× the injected noise variance** — a 17 dB noise amplification!

**For high-order IIR as biquad cascade:** Each biquad section generates noise that is filtered by the remaining sections in the cascade. The total output noise depends on the order of the sections.

**Optimal biquad ordering (minimum output noise):**

1. **Pair poles and zeros**: Each biquad should have its poles close to its zeros (band-selective pairing minimises gain).
2. **Order by gain**: Place the biquad with the highest in-band gain first (closest to input). This minimises the noise from later sections, which have lower gains.

**Quantitative example:** Two biquads $H_1(z)$ and $H_2(z)$ in cascade. Noise from each section is amplified by the subsequent sections:

- Configuration $H_1 \to H_2$: Output noise from $H_1 = \sigma_e^2 \|H_2\|_2^2$; from $H_2 = \sigma_e^2$
- Configuration $H_2 \to H_1$: Output noise from $H_2 = \sigma_e^2 \|H_1\|_2^2$; from $H_1 = \sigma_e^2$

To minimise total, place the section with larger $\|H\|_2^2$ last (i.e., closest to the output). This reduces the noise contributed by the dominant section.

---

### Q9. Explain the concept of guard bits and scaling in fixed-point recursive filter implementation. Derive the minimum guard bits for a biquad.

**Answer:**

**Problem:** In a fixed-point Direct Form I biquad:

$$y[n] = b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] - a_1 y[n-1] - a_2 y[n-2]$$

The accumulator sums 5 products. The maximum accumulator value is:

$$|y_{max}| \leq (|b_0| + |b_1| + |b_2|) \cdot |x|_{max} + (|a_1| + |a_2|) \cdot |y|_{max}$$

**Guard bits for the accumulator:** The input $x$ is Q15 ($|x| \leq 1$). Coefficients are Q15. Products are Q30. The sum of 5 products requires:

$$N_{guard} = \lceil \log_2(\text{number of terms}) \rceil + \lceil \log_2(\max \text{ coefficient sum}) \rceil$$

For a second-order Butterworth lowpass at 0.1 $f_s$:
- $|b_0| + |b_1| + |b_2| \approx 1$ (normalised)
- $|a_1| + |a_2| \approx 2$ (can be close to 2 for narrowband)

Accumulator maximum: $1 \cdot 1 + 2 \cdot |y_{max}|$. For stability, $|y_{max}|$ is bounded by the $H_\infty$ norm of the filter, which can exceed 1 for peaking filters.

**Minimum guard bits for a resonator (worst case):**

For a resonator with $Q = 10$ at $f_0 = 0.1 f_s$: peak gain $\approx Q = 10$ (20 dB above unity). Need $\lceil \log_2 10 \rceil = 4$ guard bits above the input word length.

**For a general biquad:**

$$N_{guard} = \lceil \log_2(H_\infty) \rceil + 2$$

(The extra 2 bits accommodate the 5-term accumulation plus safety margin.)

**CMSIS-DSP approach:** `arm_biquad_cascade_df1_q15` uses a 64-bit accumulator (`q63_t`) internally. No guard bit calculation is needed — the 64-bit accumulator can accommodate any practical biquad without overflow. The output is shifted right by the `postShift` parameter to scale back to Q15.

---

## Common Interview Mistakes

1. **Applying the SQNR formula without checking its validity**: The $6.02W - 1.76$ dB formula assumes a full-scale sinusoidal input and is invalid for narrowband, DC, or low-level signals. Interviewers often ask "what if the signal is 40 dB below full scale?" — the answer is SQNR drops by exactly 40 dB.
2. **Confusing quantisation noise in ADC vs. in arithmetic**: ADC quantisation adds noise at the input; arithmetic quantisation adds noise at each computation step. They are separate sources that accumulate differently.
3. **Assuming float32 is always more accurate than Q31**: Float32 has 23-bit mantissa (about 7 decimal digits). Q31 has 31 fractional bits. For a signal in $[-1, 1]$, Q31 has $2^{31-23} = 256$ times better precision than float32 in the $[-1, 1]$ range. Float32's advantage is its huge dynamic range, not higher precision per se.
4. **Forgetting that filter coefficient quantisation and input quantisation are independent noise sources**: Both must be analysed separately and their output-referred noise variances summed.
5. **Claiming 64-bit floating-point eliminates all precision problems**: While float64 is highly accurate for most DSP, it can still fail for ill-conditioned problems (e.g., very high-order polynomial root finding, computing small differences of large numbers). Always analyse the condition number of the algorithm.
