# Fixed-Point Arithmetic for DSP — Interview Questions

## Overview

Fixed-point arithmetic is the foundation of efficient DSP hardware implementation. Understanding Q-format notation, overflow, rounding, and quantisation noise is essential for ASIC, FPGA, and embedded DSP roles. Interviewers probe both the mechanics (exact bit layouts) and the system-level implications (SNR, filter stability).

---

## Tier 1: Fundamentals

### Q1. What is fixed-point representation? How does it differ from floating-point?

**Answer:**

**Fixed-point:** A number is represented as a scaled integer. The binary point is fixed at a specific bit position defined by the programmer. A $W$-bit word with $F$ fractional bits represents the value:

$$x = \sum_{i=-F}^{W-F-2} b_i \cdot 2^i - b_{W-1} \cdot 2^{W-F-1}$$

(two's complement sign bit at position $W-F-1$).

**Floating-point:** The binary point position varies per number. IEEE 754 single precision uses 1 sign bit, 8 exponent bits, 23 mantissa bits. The value is $(-1)^s \cdot 1.m \cdot 2^{e-127}$.

**Comparison:**

| Property | Fixed-point | Floating-point |
|---|---|---|
| Dynamic range | Limited ($2^W$) | Very large ($\sim 10^{38}$ for FP32) |
| Precision | Uniform across range | Proportional to magnitude |
| Hardware cost | Low (integer ALU) | High (FP unit with normalisation) |
| Power | Low | 3–5× higher |
| Overflow | Sudden, catastrophic | Gradual (denormals, then inf) |
| Designer burden | High (must track Q-format) | Low (hardware handles scaling) |
| Speed | Fast | Moderate (pipelined FPU needed) |

Fixed-point is preferred in: DSP ASICs, FPGAs, MCU DSP extensions, battery-powered devices. Floating-point is preferred in: high-dynamic-range signal processing, rapid prototyping, scientific computing.

---

### Q2. Explain Q-format notation. What does Q15 and Q1.15 mean?

**Answer:**

**Q-format** specifies the position of the binary point within a fixed-bit-width word.

**Texas Instruments convention — Q$m.n$:**
- Total bits = $m + n + 1$ (includes sign bit)
- $m$ = number of integer bits (excluding sign)
- $n$ = number of fractional bits
- Value range: $[-2^m, 2^m - 2^{-n}]$
- Resolution: $2^{-n}$

**ARM/shorthand convention — Q$n$:**
- Implies a $W$-bit word where $n$ is the number of fractional bits
- Q15 means a 16-bit word with 15 fractional bits

**Q15 (16-bit):**
- Bit layout: `S.FFFFFFFFFFFFFFF` (1 sign bit, 15 fractional bits)
- Range: $[-1.0, 1.0 - 2^{-15}] = [-1.0, 0.999969]$
- Resolution: $2^{-15} = 3.05 \times 10^{-5}$
- Represents values in $[-1, 1)$ — ideal for normalised filter coefficients and signal samples
- Integer representation of $x$: $x_{int} = \text{round}(x \cdot 2^{15})$

**Q1.15 (Texas Instruments convention, 16-bit):**
- Bit layout: `SI.FFFFFFFFFFFFFFF` (1 sign bit, 1 integer bit, 14 fractional bits)
- Range: $[-2.0, 2.0 - 2^{-14}]$
- Resolution: $2^{-14}$
- Represents values in $[-2, 2)$
- Used when values just exceed 1.0 (e.g., after summing two Q15 values)

**Q8.8 (16-bit):**
- Range: $[-256.0, 255.996]$, Resolution: $2^{-8} = 1/256$
- Used when both integer and fractional parts are needed (e.g., audio gain control)

**Example (Q15):** To represent $x = 0.707107 \approx 1/\sqrt{2}$:
$$x_{int} = \text{round}(0.707107 \times 32768) = \text{round}(23170.1) = 23170 = \text{0x5A82}$$

---

### Q3. What is overflow in fixed-point arithmetic and what are the two standard ways to handle it?

**Answer:**

**Overflow** occurs when an arithmetic operation produces a result outside the representable range $[x_{min}, x_{max}]$ of the target word length. For a Q15 number (range $[-1, 1)$), adding $0.8 + 0.5 = 1.3$ overflows.

**Two-'s complement wrapping (default behaviour):**

The ALU discards bits above the word width. The result wraps around:

$$0.8 + 0.5 = 1.3 \Rightarrow \text{in 16-bit two's complement: } 1.3 - 2 = -0.7$$

The error is a large jump of $-2$ — potentially catastrophic in a DSP system. In a recursive filter, a single overflow can cause the output to oscillate at full amplitude indefinitely (overflow oscillation).

**Saturation:**

The result is clamped to the nearest representable extreme:

$$\text{sat}(x) = \begin{cases} x_{max} & x > x_{max} \\ x_{min} & x < x_{min} \\ x & \text{otherwise} \end{cases}$$

For Q15: $\text{sat}(1.3) = 0.999969$ (maximum value).

**Comparison:**

| Mode | Overflow error | Audio artefact | When to use |
|---|---|---|---|
| Wrapping | Sign flip, large error | Loud click/pop | Only when overflow is provably impossible |
| Saturation | Clipping, bounded error | Soft clipping | DSP filters, audio, any safety-critical path |

**Hardware:** Most DSP processors provide a saturation mode via a status register bit (e.g., ARM Cortex-M4 has a `Q` flag and `SSAT` instruction). FPGAs can implement saturation in the same cycle as the computation at minimal cost.

---

### Q4. What are the rounding modes in fixed-point arithmetic? Why does the choice matter?

**Answer:**

When truncating a higher-precision result to fit in a narrower word (e.g., Q30 multiplication result → Q15), the discarded bits must be handled by a rounding mode.

**Common rounding modes:**

| Mode | Rule | Bias | Use case |
|---|---|---|---|
| Truncation (floor) | Discard LSBs, round toward $-\infty$ | $-0.5$ LSB | Hardware simplest; causes DC bias in filters |
| Round half-up | Add 0.5 LSB then truncate | $+0.5$ LSB at 0.5 only | Common in integer hardware |
| Round half-even (banker's) | Round to nearest even when exactly halfway | Unbiased | Best statistical properties |
| Convergent rounding | Round half-even with carry save | Unbiased | DSP processors, SIMD extensions |
| Round away from zero | Standard mathematical rounding | Slight positive bias | Intuitive, common in textbooks |

**Why it matters for DSP:**

1. **Filter coefficient quantisation:** If all coefficients are truncated, all poles and zeros shift in the same direction, potentially causing instability in IIR filters near the unit circle.
2. **Accumulated DC offset:** Truncation introduces a mean error of $-0.5$ LSB per operation. In a recursive filter, this accumulates into a constant DC offset or limit cycle.
3. **Signal-to-quantisation-noise ratio (SQNR):** Unbiased rounding gives a white quantisation noise model with variance $\Delta^2/12$ (where $\Delta = 2^{-F}$ is the LSB). Biased rounding adds a DC component.

**Best practice:** Use convergent (round-half-even) rounding in accumulators. Truncation is acceptable only in the final output stage where the small systematic bias is tolerable.

---

### Q5. What is dynamic range in fixed-point DSP? How do you choose the word length?

**Answer:**

**Dynamic range** of a $W$-bit fixed-point word: the ratio of the maximum representable value to the minimum non-zero representable value:

$$DR = \frac{x_{max}}{\Delta} = \frac{2^{W-1} - 1}{1} \approx 2^{W-1} \quad \text{(in integer units)}$$

In dB: $DR_{dB} = 20 \log_{10}(2^{W-1}) \approx (W-1) \times 6.02$ dB

| Word length | Dynamic range |
|---|---|
| 8-bit | 42 dB |
| 16-bit | 90 dB |
| 24-bit | 138 dB |
| 32-bit | 186 dB |

**Word length selection for FIR filters:**

The required word length depends on the filter's bit growth. An $N$-tap FIR with coefficients $h[n]$ and input word length $W_x$ produces a worst-case accumulator value of:

$$|y_{max}| \leq \sum_{n=0}^{N-1} |h[n]| \cdot 2^{W_x - 1}$$

To represent this without overflow, the accumulator needs:

$$W_{acc} = W_x + W_h + \lceil \log_2 N \rceil$$

For $W_x = 16$ (Q15 input), $W_h = 16$ (Q15 coefficients), $N = 64$ taps: $W_{acc} = 16 + 16 + 6 = 38$ bits. A 40-bit or 48-bit accumulator is used.

**Guideline:** Add guard bits equal to $\lceil \log_2(\text{maximum signal magnitude gain}) \rceil$ to the accumulator. Return to the output word length by rounding the accumulator result.

---

## Tier 2: Intermediate

### Q6. How do you multiply two Q15 numbers and obtain a Q15 result?

**Answer:**

**The problem:** Multiplying two $W$-bit numbers gives a $2W$-bit result. Two Q15 values (with binary points after bit 15) produce a Q30 result (binary point after bit 30) in a 30-bit product (the sign bits combine to give a 32-bit two's complement product in practice).

**Step-by-step:**

1. **Integer multiplication:** Let $a_{int}$ and $b_{int}$ be the 16-bit two's complement integers for Q15 values $a$ and $b$. The 32-bit product is $p_{int} = a_{int} \times b_{int}$.

2. **Result is Q30 in 32 bits:** The true value is $p = a \times b = p_{int} \times 2^{-30}$.

3. **Special case for $-1 \times -1$:** The product of the two most negative Q15 values ($-32768 \times -32768 = 1073741824 = 2^{30}$) exceeds the Q30 range $[-2^{30}, 2^{30}-1]$. This is a known overflow (occurs only at the most negative value squared).

4. **Shift left by 1, then extract upper 16 bits** (equivalent to shifting the 32-bit product right by 15 to get Q15):
   $$p_{Q15} = \frac{p_{int}}{2^{15}} = p_{int} \gg 15 \quad \text{(with rounding)}$$

5. **With rounding:** Add $2^{14}$ (= 0x4000) to $p_{int}$ before the shift to implement round-half-up.

**ARM DSP instruction:** `SMMULR r0, r1, r2` — signed saturating multiply returning upper 32 bits of 64-bit product (equivalent to Q31 × Q31 → Q31 with rounding).

**Example:** $a = 0.5$ (= 16384 in Q15), $b = 0.707107$ (= 23170 in Q15):
- Product: $16384 \times 23170 = 379633664$
- Q30 value: $379633664 / 2^{30} = 0.35355$ ≈ $0.5 \times 0.707 = 0.354$ ✓
- Q15 result: $379633664 \gg 15 = 11585$ ≈ $23170/2 = 11585$ ✓

---

### Q7. What is quantisation noise and how is the Signal-to-Quantisation-Noise Ratio (SQNR) derived?

**Answer:**

**Quantisation noise model:** When a continuous-valued signal is quantised to $W$ bits (step size $\Delta = 2^{1-W}$ for a signal in $[-1, 1)$), the quantisation error $e[n] = x_q[n] - x[n]$ is modelled as:
- Uniformly distributed: $e \sim \mathcal{U}(-\Delta/2, +\Delta/2)$
- Statistically independent of the signal
- White (uncorrelated between samples)

This model is valid when the signal has many quantisation levels and is not narrowband (no granular noise or limit cycles).

**Quantisation noise variance:**

$$\sigma_e^2 = \frac{\Delta^2}{12} = \frac{2^{2(1-W)}}{12} = \frac{1}{3} \cdot 2^{-2W}$$

**SQNR for a full-scale sinusoid:**

A sinusoid of amplitude $A = 1$ (full scale) has power $\sigma_x^2 = A^2/2 = 1/2$.

$$\text{SQNR} = \frac{\sigma_x^2}{\sigma_e^2} = \frac{1/2}{2^{2-2W}/12} = \frac{12}{4 \cdot 2^{2-2W}} = \frac{3}{2^{3-2W}} = \frac{3}{4} \cdot 2^{2W}$$

In dB:

$$\text{SQNR}_{dB} = 10\log_{10}\!\left(\frac{3}{4}\right) + 20W\log_{10}(2) \approx -1.76 + 6.02W \quad \text{dB}$$

**Rule of thumb:** Each additional bit adds approximately **6 dB** of SQNR.

| Word length $W$ | SQNR (dB) |
|---|---|
| 8 | 46.2 |
| 12 | 70.3 |
| 16 | 94.3 |
| 24 | 142.4 |

**SQNR for arbitrary signal level:** If the signal uses only $2^k$ levels out of the full $2^W$ range (i.e., the signal is $k$ bits below full scale), the SQNR decreases by $6k$ dB (the signal power drops but the quantisation noise stays the same).

---

### Q8. How does coefficient quantisation affect IIR filter stability and frequency response?

**Answer:**

**Direct Form I/II IIR filter:** The denominator polynomial $A(z) = 1 + \sum_{k=1}^N a_k z^{-k}$ determines the pole locations. Poles must lie strictly inside the unit circle for stability.

**Effect of quantisation:** Each coefficient $a_k$ is rounded to the nearest $W_a$-bit fixed-point value. The quantised pole positions move from their designed locations. Two critical problems arise:

**1. Pole migration near the unit circle:**

If a pole at $z = re^{j\theta}$ with $r$ close to 1.0 (narrowband filter), quantisation can move it outside the unit circle, causing instability. The sensitivity is:

$$\left|\frac{\partial z_i}{\partial a_k}\right| \propto \frac{1}{\prod_{j \neq i}|z_i - z_j|}$$

When poles are clustered (high-order narrowband filter), the denominator is small, making the poles highly sensitive to coefficient perturbations. A 16-bit coefficient may be insufficient for a very high-Q filter.

**Example:** A resonator at $f_0 = 100$ Hz with $Q = 100$ at $f_s = 8$ kHz has poles at $z = e^{\pm j 2\pi \times 100/8000}$ ≈ $e^{\pm j0.0785}$. The poles are close together and close to the unit circle. Coefficient word length must be at least:

$$W_a \geq \log_2\!\left(\frac{f_s}{2f_0(1 - r)}\right) + \text{margin} \approx 24\, \text{bits}$$

**2. Frequency response deviation:**

Quantised coefficients shift the filter's frequency response. Passband ripple increases, transition band widens, and stopband attenuation degrades. The coefficient quantisation effect on frequency response can be analysed by comparing $|H(e^{j\omega})|$ before and after quantisation.

**Mitigation strategies:**

- **Cascade/parallel second-order sections (biquads)**: Break the high-order filter into 2nd-order sections. Each section has only 2 poles, minimising sensitivity. The poles of each section are paired to be close together, minimising their individual sensitivities.
- **Higher word length**: 32-bit or 64-bit coefficients (at the cost of more multiplier hardware).
- **State variable (coupled form)**: Alternative filter structures with lower coefficient sensitivity.

---

### Q9. What are limit cycles in IIR fixed-point filters?

**Answer:**

**Limit cycle** is a low-level oscillation in a fixed-point IIR filter that persists indefinitely even after the input has become zero. It arises from the non-linear rounding operation in the feedback path.

**Granular limit cycles:** Occur when the filter output has settled to a small region where rounding creates a fixed pattern. The output cycles between a small set of values rather than converging to zero.

**Example (first-order IIR):** $y[n] = a \cdot y[n-1]$ with $a = 0.9$, zero input, Q3.4 arithmetic (resolution $\Delta = 2^{-4} = 0.0625$):

| $n$ | $y$ (exact) | $y_{Q3.4}$ (rounded) |
|---|---|---|
| 0 | 0.500 | 0.5 |
| 1 | 0.450 | 0.4375 (rounded down) |
| 2 | 0.394 | 0.375 |
| 3 | 0.338 | 0.3125 |
| ... | converging → 0 | oscillating ↔ ??? |

With truncation, at some point $y[n] = 0.0625$ and $0.9 \times 0.0625 = 0.05625$, which truncates to 0.0625 — the filter locks into the non-zero state forever.

**Overflow oscillations:** Larger oscillations caused by wrap-around overflow in the accumulator. These are at full-scale amplitude and extremely audible/destructive. Using saturation arithmetic eliminates overflow oscillations (the filter saturates and recovers gracefully).

**Prevention of granular limit cycles:**
- Use **magnitude truncation** (round toward zero) instead of floor truncation — this guarantees convergence to zero.
- Ensure sufficient word length so the limit cycle amplitude is below the LSB of the output.
- Add a very small dither signal to randomise the quantisation error.

---

## Tier 3: Advanced

### Q10. Derive the effect of finite word length on the SQNR of a cascaded FIR filter output.

**Answer:**

**Model:** Consider an $L$-tap FIR filter with Q15 coefficients and Q15 input, computing in a $W_{acc}$-bit accumulator. Rounding sources:

1. **Input quantisation noise**: If the ADC has $W_{in}$ bits, the input noise variance is $\sigma_{e,in}^2 = 2^{-2W_{in}}/12$.
2. **Coefficient quantisation**: Each coefficient $h[n]$ is approximated to $W_h$ bits. This perturbs the frequency response.
3. **Product rounding**: After each multiply-accumulate, if the full double-precision product is retained in the accumulator, product rounding only occurs once at the output.

**Noise at filter output from input quantisation:**

The quantisation noise $e_{in}[n]$ passes through the filter with the same frequency response as the signal. Output noise power:

$$\sigma_{out,in}^2 = \sigma_{e,in}^2 \cdot \sum_{n=0}^{L-1} h^2[n] = \sigma_{e,in}^2 \cdot \|h\|^2_2$$

where $\|h\|^2_2 = \sum h^2[n]$ is the filter's $\ell^2$ norm squared, equal to $(1/2\pi)\int |H(e^{j\omega})|^2 d\omega$ (Parseval).

**Noise at filter output from output rounding (Q15 output from $W_{acc}$ accumulator):**

If the accumulator is rounded to $W_{out}$ bits at the output, a single rounding noise source with variance $\sigma_{out,round}^2 = 2^{-2W_{out}}/12$ is added.

**Total output noise variance:**

$$\sigma_{total}^2 = \sigma_{e,in}^2 \|h\|^2_2 + \sigma_{out,round}^2$$

**SQNR at filter output:**

For a full-scale sinusoidal input (power $= 1/2$), filtered output power $= (1/2) \cdot |H(e^{j\omega_0})|^2$:

$$\text{SQNR} = \frac{(1/2)|H(e^{j\omega_0})|^2}{\sigma_{total}^2}$$

In a stopband region where $|H(e^{j\omega_0})|$ is small, the signal is attenuated but the output rounding noise $\sigma_{out,round}^2$ is constant — this is why stopband signals can be buried in quantisation noise even if they are above the theoretical stopband rejection.

**Design implication:** For a filter with 60 dB stopband attenuation, the output word must have at least $60/6.02 + 3 \approx 13$ bits dedicated to representing the in-band signal above the out-of-band noise floor. This justifies using a 16-bit output even for moderate-precision applications.

---

### Q11. Explain double-accumulation for Q15 FIR filters. How does it prevent intermediate overflow?

**Answer:**

**Problem:** In a Direct Form FIR filter with $L$ taps, the accumulator receives $L$ partial products. In the worst case (all inputs and coefficients at maximum magnitude), the sum can be $L \times 2^{W-1}$ — requiring $\log_2 L$ guard bits above the product width.

For $L = 256$ taps with Q15 × Q15 = Q30 products: accumulator must be at least $30 + \log_2(256) = 30 + 8 = 38$ bits.

**Double-accumulation approach:**

1. **First level**: Compute each product at full precision (32-bit or 40-bit accumulator).
2. **Accumulate in $W_{acc}$-bit accumulator** (e.g., 40 bits): `acc += a[n] * x[k-n]` in 40-bit.
3. **Scale and round** to the output word at the end.

**ARM Cortex-M4 implementation:**

The `SMLAL` instruction (Signed Multiply Long Accumulate) multiplies two 32-bit values and accumulates into a 64-bit register pair:
```c
// Compute 64-bit accumulate: result += a * b
int64_t acc = 0;
for (int n = 0; n < L; n++) {
    acc += (int64_t)h[n] * x[k - n];  // h, x are int16_t (Q15)
}
// acc is Q30; scale to Q15 with rounding
int16_t y = (int16_t)((acc + (1 << 14)) >> 15);
```

The 64-bit accumulator guarantees no intermediate overflow for any input sequence as long as:

$$L \leq 2^{64 - 30 - 1} = 2^{33}$$

For $L \leq 4$ billion taps — no practical filter can overflow a 64-bit accumulator using 16-bit operands.

**Key advantage:** By accumulating in full precision and rounding only once at the output, only a single quantisation noise source is introduced (the final rounding), regardless of $L$. This gives better SQNR than rounding after each product.

---

## Common Interview Mistakes

1. **Confusing Q-format conventions**: The Texas Instruments Q$m.n$ and the ARM/DSP Q$n$ notations differ. Always state the convention explicitly and clarify the total word length.
2. **Forgetting to handle the $-1 \times -1$ overflow in Q15**: The most negative Q15 value squared slightly exceeds Q30 range. Hardware implementations must either saturate or accept this one-off overflow.
3. **Assuming wrapping is safe**: Wrapping overflow is almost never acceptable in recursive (IIR) filters. Saturation should be the default for any filter feedback path.
4. **Not accounting for bit growth in accumulators**: Every $2 \times$ increase in the number of accumulated terms requires one additional guard bit. Failing to provide guard bits causes overflow and catastrophic errors.
5. **Using the wrong noise model**: The uniform white noise quantisation model requires many quantisation levels and a broadband signal. For narrowband signals or near-limit-cycle conditions, the actual noise is non-white and non-uniform — the simple SQNR formula does not apply.
