# Filter Structures — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Direct Form I/II, Transposed Direct Form II, SOS, Lattice, Coefficient Sensitivity
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Draw and describe Direct Form I and Direct Form II structures. How many delay elements does each require?

**Answer:**

Both structures implement the same transfer function:

$$H(z) = \frac{B(z)}{A(z)} = \frac{\sum_{k=0}^{M}b_k z^{-k}}{1 + \sum_{k=1}^{N}a_k z^{-k}}$$

**Direct Form I:**

Implements the difference equation directly:

$$y[n] = \sum_{k=0}^{M}b_k\,x[n-k] - \sum_{k=1}^{N}a_k\,y[n-k]$$

Structure: feed-forward (FIR) section followed by feedback (IIR) section.

```
x[n] ─┬─────────────────────────────────────────── (+)──► y[n]
       │   b0                                         ▲
       ├──[z⁻¹]──┬── b1                              │
       │          │                                   │
       ├──[z⁻¹]──┼──[z⁻¹]──┬── b2                  │
       │          │           │                        │
      ...        ...         ...                   (sum)
       │          │           │                    ▲  ▲
       │         [z⁻¹]      [z⁻¹]                 │  │
                                                   │  │
     y[n-1]─────────────────────────────── -a1 ───┘  │
     y[n-2]────────────────────────────────── -a2 ───┘
```

**Delay count:** Requires $N$ delays for the feedback (IIR) section and $M$ delays for the feedforward (FIR) section. Total: $N + M$ unit delays.

**Direct Form II (canonical):**

Shares the delay line between the feedforward and feedback sections by combining them:

```
x[n] ──(+)──── w[n] ──[b0]──────────────────── (+)── y[n]
        ▲                                          ▲
        │       [z⁻¹]                              │
        │         │                                │
       -a1 ──────┤──── [b1] ─────────────────────┤
                  │                                │
                [z⁻¹]                              │
                  │                                │
       -a2 ──────┤──── [b2] ─────────────────────┘
                 ...
```

The state variable is $w[n] = x[n] - a_1\,w[n-1] - a_2\,w[n-2] - \cdots$.

**Delay count:** Only $N$ unit delays (assuming $M \leq N$). This is the **minimum** number of delays needed for an $N$th-order IIR filter — hence "canonical form."

**Trade-off:** Direct Form II requires fewer registers but suffers more severely from finite word-length effects because intermediate values ($w[n]$) can have larger dynamic range than input or output signals.

---

### Q2. What is transposed Direct Form II and what advantage does it offer?

**Answer:**

The **transposed Direct Form II** is obtained by transposing the signal flow graph of Direct Form II: reversing all signal flow directions and swapping inputs with outputs.

**Structure (second-order biquad example):**

$$y[n] = b_0 x[n] + s_1[n-1]$$
$$s_1[n] = b_1 x[n] - a_1 y[n] + s_2[n-1]$$
$$s_2[n] = b_2 x[n] - a_2 y[n]$$

The state variables $s_1$ and $s_2$ are updated after computing $y[n]$.

**Signal flow:**

```
x[n] ─┬─[b0]────────────────────────────────────── (+)── y[n]
       │                                             ▲
       ├─[b1]──(+)──[s1]──────────────────────────►┤
       │         ▲                                   │
       │       -a1──────────────────── [y[n]] ───────┘
       │                               ▲
       ├─[b2]──(+)──[s2]              │
                ▲                     │
              -a2────────────────────┘
```

**Advantages over Direct Form II:**

1. **Pipelining friendly:** The critical path for computing $y[n]$ is shorter. In Direct Form II, $y[n]$ depends on all accumulated state updates before it can be computed. In transposed form, $y[n]$ is computed from $x[n]$ and the **previous** state $s_1[n-1]$ — state updates happen after the output, which is easier to pipeline.

2. **Reduced register file pressure:** State variables $s_1, s_2$ represent summations being accumulated — natural for hardware accumulator architectures.

3. **Preferred in hardware and SIMD:** Modern DSP chips and FPGAs use transposed Direct Form II for biquad implementations in audio and communications processing.

**Note:** All four structures (DF-I, DF-II, Transposed DF-I, Transposed DF-II) have identical transfer functions and stability for infinite precision. Differences emerge only under finite word-length conditions.

---

### Q3. What is a cascaded second-order section (SOS) structure? How is a high-order IIR filter decomposed into SOS?

**Answer:**

A **cascaded SOS** structure expresses a high-order IIR as a product of second-order biquads:

$$H(z) = G \cdot \prod_{k=1}^{K} H_k(z) = G \cdot \prod_{k=1}^{K}\frac{b_{k0} + b_{k1}z^{-1} + b_{k2}z^{-2}}{1 + a_{k1}z^{-1} + a_{k2}z^{-2}}$$

where $G$ is an overall gain factor and $K = \lfloor N/2 \rfloor$ for an $N$th-order system.

**Decomposition steps:**

1. **Find all poles and zeros** of $H(z)$.
2. **Form complex conjugate pairs:** Each pair of complex conjugate poles $(p_k, p_k^*)$ forms one second-order denominator: $(1-p_k z^{-1})(1-p_k^* z^{-1}) = 1 - 2\text{Re}(p_k)z^{-1} + |p_k|^2 z^{-2}$.
   Real poles are paired together, or left as first-order sections (padded to second order with $a_2 = 0$).
3. **Pair poles with zeros:** Match each pole pair with a nearby zero pair to minimise the dynamic range within that section.
4. **Ordering:** Order sections from the most selective (poles closest to unit circle) outward, or use an interleaved pole-zero scheme to minimise internal signal growth.

**Why MATLAB `sosfilt` and `tf2sos` output SOS:**

```matlab
[b, a] = butter(8, 0.3);      % 8th-order Butterworth
[sos, g] = tf2sos(b, a);      % Convert to 4 biquads
y = sosfilt(sos, x);           % Filter using SOS (numerically stable)
```

Directly using the high-order `(b, a)` with `filter()` can fail for $N > 5$ in double precision due to pole sensitivity.

---

## Intermediate

### Q4. Explain coefficient sensitivity. Why do poles near the unit circle make a direct-form high-order IIR numerically fragile?

**Answer:**

**Coefficient sensitivity** measures how much a pole location changes when a filter coefficient is perturbed by a small amount $\delta$:

$$\Delta p_m \approx \sum_k \frac{\partial p_m}{\partial a_k}\,\delta a_k$$

**For a direct-form $N$th-order denominator:**

$$A(z) = \prod_{m=1}^{N}(1 - p_m z^{-1})$$

Differentiating:

$$\frac{\partial p_m}{\partial a_k} = \frac{-p_m^{N-k}}{\prod_{i \neq m}(p_m - p_i)}$$

The sensitivity is inversely proportional to the distance between poles: $\prod_{i \neq m}|p_m - p_i|$.

**Example — 8th-order Butterworth at low cutoff:**

For a Butterworth filter with $\omega_c = 0.1\pi$ (cutoff at $f_s/20$), all 8 poles cluster near $z \approx e^{\pm j\omega_c}$. The separation between adjacent poles is tiny ($\approx \omega_c/N \approx 0.01\pi$ rad). The product $\prod_{i\neq m}|p_m - p_i|$ can be as small as $10^{-10}$ for some pairs.

Consequently, a coefficient quantisation error of $\Delta a \approx 2^{-24}$ (24-bit precision) can move a pole by $|\Delta p| \approx \Delta a / 10^{-10} = 10^{16}\,\Delta a$ — which is enormous and can push the pole outside the unit circle.

**SOS solution:** Each biquad contains only 2 poles, separated by the conjugate distance $2|\text{Im}(p_k)|$. The sensitivity for the isolated biquad is:

$$\frac{\partial p_k}{\partial a_{k1}} = \frac{-p_k}{p_k - p_k^*} = \frac{-p_k}{2j\,\text{Im}(p_k)}$$

This is of order 1 (or small), far better than the global cross-sensitivity in direct form.

---

### Q5. Describe the parallel form filter structure. When is it advantageous?

**Answer:**

The **parallel form** decomposes $H(z)$ into a sum of second-order (or first-order) sections using partial fraction expansion:

$$H(z) = C + \sum_{k=1}^{K} H_k(z)$$

where $C$ is a constant (from any polynomial term in the numerator) and each $H_k(z)$ is a second-order section corresponding to a conjugate pole pair:

$$H_k(z) = \frac{e_{k0} + e_{k1}z^{-1}}{1 + a_{k1}z^{-1} + a_{k2}z^{-2}}$$

**Signal flow:** Each section runs in parallel and the outputs are summed.

**Advantages:**

1. **Independent processing paths:** Each section can be computed simultaneously — natural for parallel hardware.
2. **Accumulation:** All sections contribute to the output additively, so a malfunction in one section shows up as a missing component rather than a catastrophic failure.
3. **Numerical stability** (same as SOS): Each section is isolated.
4. **No error accumulation along a cascade:** In cascaded SOS, errors from earlier sections can affect later ones; parallel form sections are independent.

**Disadvantages:**

1. **Partial fraction expansion** is required, which can itself be numerically ill-conditioned for closely spaced poles.
2. **Pole pairing with numerator zeros is less natural** — the numerator of $H(z)$ is distributed across sections in a non-obvious way.
3. In cascaded SOS, you can easily implement transfer function shaping (e.g., parametric EQ) by enabling/disabling or adjusting individual sections. Parallel form makes this less intuitive.

**When to use parallel form:**

- When hardware parallelism is available and latency must be minimised
- When the sections are resonators with known frequencies (e.g., formant synthesis in speech)
- When robustness to section failure is a requirement

---

### Q6. Describe lattice filter structures. What are their advantages in adaptive filtering?

**Answer:**

A **lattice filter** is a recursive structure based on the parcor (partial autocorrelation) coefficients $K_m$ (also called reflection coefficients):

**All-pole (IIR) lattice of order $M$:**

```
x[n] = f_0[n] = g_0[n]

f_m[n] = f_{m-1}[n] + K_m g_{m-1}[n-1]
g_m[n] = K_m f_{m-1}[n] + g_{m-1}[n-1]

y[n] = g_M[n]
```

The $f_m$ signals are the "forward" prediction errors and $g_m$ are "backward" prediction errors.

**Advantages:**

1. **Modular order expansion:** Adding another stage increases the filter order by one. You can build an order-adaptive filter by toggling stages.

2. **Stability checking:** The all-pole lattice is stable if and only if $|K_m| < 1$ for all stages $m$. This is extremely easy to enforce in hardware.

3. **Orthogonal stages:** Each lattice stage corresponds to a Gram-Schmidt step in the Levinson-Durbin recursion. The stages are orthogonal in a statistical sense, which leads to better numerical conditioning.

4. **Natural structure for LPC (Linear Predictive Coding):** The Levinson-Durbin algorithm directly produces lattice coefficients $K_m$ from an autocorrelation sequence — used in speech coding (LPC-10, G.711, CELP).

5. **Adaptive lattice filters:** Algorithms like the gradient adaptive lattice (GAL) update $K_m$ independently at each stage, converging faster than LMS for correlated inputs.

**Disadvantage:** Lattice structures require approximately twice as many operations per sample as direct form for the same filter order, because each stage computes two signals ($f_m$ and $g_m$).

---

## Advanced

### Q7. Quantify the dynamic range scaling problem in cascaded SOS. How does L2 scaling work and why is it preferred?

**Answer:**

**Problem:** In a cascade of $K$ biquads, the intermediate signal at the output of stage $k$ is:

$$W_k(e^{j\omega}) = X(e^{j\omega}) \cdot \prod_{i=1}^{k} H_i(e^{j\omega})$$

For a resonant biquad with poles near the unit circle at $\omega_0$, the gain $|H_i(e^{j\omega_0})|$ can be very large. The intermediate signal $w_k[n]$ can overflow the word length even if the input $x[n]$ and output $y[n]$ are within range.

**Scaling approach:** Insert gain scaling factors $\alpha_k$ between stages:

$$\tilde{H}(z) = \prod_{k=1}^{K}\left[\alpha_k\,H_k(z)\right] \cdot \frac{1}{\prod_k \alpha_k}$$

The $\alpha_k$ factors prevent overflow in the intermediate nodes.

**L2 scaling (power scaling):**

Ensures that a white noise input of unit power produces unit power at each internal node:

$$\alpha_k = \frac{1}{\left\|H_1 H_2 \cdots H_k\right\|_2}$$

where $\|G\|_2 = \sqrt{\frac{1}{2\pi}\int_{-\pi}^{\pi}|G(e^{j\omega})|^2\,d\omega}$ is the $L^2$ (RMS) norm of the frequency response.

This corresponds to equal probability of overflow at each node for a Gaussian white noise input.

**L∞ scaling:**

Ensures that a bounded input $|x[n]| \leq 1$ produces bounded intermediate signals $|w_k[n]| \leq 1$:

$$\alpha_k = \frac{1}{\left\|H_1 H_2 \cdots H_k\right\|_1}$$

where $\|G\|_1 = \sum_n |g[n]|$ is the $L^1$ norm of the impulse response.

**Why L2 is preferred in practice:** L∞ scaling is maximally conservative — it prevents overflow for the absolute worst-case input. This leads to very small scaling factors, wasting dynamic range and amplifying quantisation noise. L2 scaling provides a better balance: it is appropriate for typical (stochastic) inputs and is provably optimal in terms of output noise power for a given probability of overflow.

---

### Q8. Describe the implementation of a parametric EQ filter (peaking equaliser) as a biquad. Give the transfer function and design equations.

**Answer:**

A **parametric equaliser** boosts or cuts a frequency band centred at $f_0$ by $G$ dB with quality factor $Q$.

**Analog prototype (resonant peak/notch):**

$$H_a(s) = \frac{s^2 + s\,(\Omega_0/Q)\,(1 + V_0) + \Omega_0^2}{s^2 + s\,(\Omega_0/Q) + \Omega_0^2}$$

where $V_0 = 10^{G/20}$ (linear gain at peak), $\Omega_0 = 2\pi f_0$.

**Digital biquad via bilinear transform:**

After applying $s = \frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}}$ and defining $K = \tan(\pi f_0/f_s)$:

**For boost ($G > 0$):**

$$b_0 = \frac{1 + V_0 K/Q + K^2}{1 + K/Q + K^2}, \quad b_1 = \frac{2(K^2-1)}{1 + K/Q + K^2}, \quad b_2 = \frac{1 - V_0 K/Q + K^2}{1 + K/Q + K^2}$$

$$a_1 = b_1, \quad a_2 = \frac{1 - K/Q + K^2}{1 + K/Q + K^2}$$

**For cut ($G < 0$):** Swap numerator and denominator roles ($V_0 = 10^{-|G|/20}$, use the cut formula).

```python
import numpy as np

def peaking_eq_biquad(f0, fs, G_dB, Q):
    """
    Design a peaking EQ biquad.
    Returns (b, a) arrays for a direct-form-II implementation.
    f0: centre frequency (Hz), fs: sample rate (Hz)
    G_dB: boost/cut in dB (positive = boost)
    Q: quality factor
    """
    V0 = 10 ** (G_dB / 20.0)
    K = np.tan(np.pi * f0 / fs)
    K2 = K * K

    if G_dB >= 0:  # boost
        norm = 1 + K / Q + K2
        b0 = (1 + V0 * K / Q + K2) / norm
        b1 = 2 * (K2 - 1) / norm
        b2 = (1 - V0 * K / Q + K2) / norm
        a1 = b1
        a2 = (1 - K / Q + K2) / norm
    else:          # cut
        norm = 1 + K / (V0 * Q) + K2
        b0 = (1 + K / Q + K2) / norm
        b1 = 2 * (K2 - 1) / norm
        b2 = (1 - K / Q + K2) / norm
        a1 = b1
        a2 = (1 - K / (V0 * Q) + K2) / norm

    return np.array([b0, b1, b2]), np.array([1.0, a1, a2])

# Example: +6 dB boost at 1 kHz, Q=1.0, fs=48000
b, a = peaking_eq_biquad(1000, 48000, 6.0, 1.0)
```

**Design notes:**

- At $f_0$: gain is exactly $V_0$ (in linear) or $G$ dB
- At DC and Nyquist: gain is unity (0 dB)
- Bandwidth (half-gain points) is $f_0/Q$
- This single biquad is the building block of every parametric EQ in professional audio software

---

## Quick Reference

| Structure | Delays | Pipeline-friendly | Preferred for |
|---|---|---|---|
| Direct Form I | $N + M$ | No | Conceptual understanding |
| Direct Form II | $N$ | Moderate | Simple implementations |
| Transposed DF-II | $N$ | Yes | Hardware, SIMD |
| Cascaded SOS | $2K$ total | Yes | All production IIR |
| Parallel form | $2K$ total | Yes | Parallel hardware |
| Lattice | $N$ | Moderate | LPC, adaptive filters |

**Rule of thumb:** Always use cascaded SOS in production code. Direct form for orders $> 4$ is numerically unreliable in fixed-point and can be fragile in float.
