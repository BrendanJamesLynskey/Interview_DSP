# Worked Problem 02: Raised Cosine Pulse Shaping Filter Design

## Problem Statement

Design a raised cosine pulse shaping filter for a digital communications system with:
- Symbol rate: $R_s = 1$ Msymbol/s → symbol period $T_s = 1$ µs
- Roll-off factors to compare: $\alpha = 0, 0.25, 0.5, 1.0$
- Oversampling factor: $L = 8$ samples/symbol
- Filter span: $N_{span} = 6$ symbol periods

**Tasks:**
1. Derive the raised cosine frequency response and verify the Nyquist criterion
2. Derive the time-domain impulse response and verify zero ISI at $t = nT_s$
3. Derive the RRC (root raised cosine) filter as the square-root factorisation
4. Compute bandwidths for each $\alpha$
5. Show the effect of $\alpha$ on eye diagram opening

---

## Part 1: Raised Cosine Frequency Response

### Definition

The raised cosine filter has a cosine-shaped transition between its flat passband and its zero stopband:

$$P_{RC}(f) = \begin{cases}
T_s & |f| \leq f_1 \\[6pt]
\dfrac{T_s}{2}\!\left[1 + \cos\!\left(\dfrac{\pi(|f| - f_1)}{f_2 - f_1}\right)\right] & f_1 < |f| \leq f_2 \\[8pt]
0 & |f| > f_2
\end{cases}$$

where the passband edge and stopband edge are:

$$f_1 = \frac{1-\alpha}{2T_s}, \qquad f_2 = \frac{1+\alpha}{2T_s}$$

**Equivalent compact form:**

$$P_{RC}(f) = \frac{T_s}{2}\!\left[1 + \cos\!\left(\frac{\pi T_s}{\alpha}\!\left(|f| - \frac{1-\alpha}{2T_s}\right)\right)\right] \cdot \mathbf{1}_{f_1 < |f| \leq f_2} + T_s \cdot \mathbf{1}_{|f| \leq f_1}$$

### Nyquist Criterion Verification

The Nyquist folding criterion requires:

$$\sum_{k=-\infty}^{\infty} P_{RC}\!\left(f - \frac{k}{T_s}\right) = T_s \quad \forall f \in \left[-\frac{1}{2T_s}, \frac{1}{2T_s}\right]$$

Consider the folded sum at a frequency $f$ in the transition band $f \in [f_1, f_2]$. Only two terms contribute: $k = 0$ (the filter itself) and $k = -1$ (the alias centred at $f - 1/T_s$):

**Term $k = 0$:** $f$ is in the transition band:

$$P_{RC}(f) = \frac{T_s}{2}\!\left[1 + \cos\!\left(\frac{\pi T_s}{\alpha}\!\left(f - \frac{1-\alpha}{2T_s}\right)\right)\right]$$

**Term $k = -1$:** The point $f - 1/T_s$ falls in $[-(1+\alpha)/(2T_s), -(1-\alpha)/(2T_s)]$, i.e., the negative-frequency transition band. Using $|f - 1/T_s| = 1/T_s - f$ (since $f < 1/(2T_s)$):

$$P_{RC}\!\left(f - \frac{1}{T_s}\right) = \frac{T_s}{2}\!\left[1 + \cos\!\left(\frac{\pi T_s}{\alpha}\!\left(\frac{1}{T_s} - f - \frac{1-\alpha}{2T_s}\right)\right)\right]$$

$$= \frac{T_s}{2}\!\left[1 + \cos\!\left(\pi - \frac{\pi T_s}{\alpha}\!\left(f - \frac{1-\alpha}{2T_s}\right)\right)\right]$$

$$= \frac{T_s}{2}\!\left[1 - \cos\!\left(\frac{\pi T_s}{\alpha}\!\left(f - \frac{1-\alpha}{2T_s}\right)\right)\right]$$

**Sum of the two terms:**

$$P_{RC}(f) + P_{RC}\!\left(f - \frac{1}{T_s}\right) = \frac{T_s}{2}[1 + \cos(\theta)] + \frac{T_s}{2}[1 - \cos(\theta)] = T_s \quad \checkmark$$

The anti-symmetry of the cosine transition about the Nyquist frequency $f = 1/(2T_s)$ ensures perfect cancellation. This is the geometric foundation of the raised cosine — its transition band is designed to be exactly anti-symmetric.

---

## Part 2: Time-Domain Impulse Response

### Derivation via Inverse Fourier Transform

$$p_{RC}(t) = \int_{-\infty}^{\infty} P_{RC}(f)\, e^{j2\pi ft}\, df$$

Split the integral into three regions and use the cosine form in the transition band. After trigonometric manipulation:

$$p_{RC}(t) = \frac{\sin(\pi t/T_s)}{\pi t/T_s} \cdot \frac{\cos(\pi\alpha t/T_s)}{1 - (2\alpha t/T_s)^2}$$

**Verification of zero ISI:** At $t = nT_s$ for $n \in \mathbb{Z}$, $n \neq 0$:

The first factor $\text{sinc}(n) = \frac{\sin(\pi n)}{\pi n} = 0$ for all non-zero integers. The second factor is finite for all $t \neq \pm T_s/(2\alpha)$ (handled separately below). Therefore $p_{RC}(nT_s) = 0$ for $n \neq 0$. At $n = 0$: both factors approach 1 by L'Hôpital's rule, so $p_{RC}(0) = 1$. Zero ISI confirmed.

**Special case at $t = \pm T_s/(2\alpha)$:** Both numerator and denominator of the second factor are zero. Applying L'Hôpital:

$$\lim_{t \to T_s/(2\alpha)} \frac{\cos(\pi\alpha t/T_s)}{1 - (2\alpha t/T_s)^2} = \frac{\pi\alpha}{2T_s} \cdot \frac{-\sin(\pi/2)}{-4\alpha/T_s} = \frac{\pi}{8}$$

Multiplied by the sinc factor (which is also finite at this point), the limit is finite.

### Numerical Impulse Responses

**Parameters:** $T_s = 1$ µs, $L = 8$ samples, $N_{span} = 6$ symbols, total taps $= 6 \times 8 + 1 = 49$.

Sample index: $n = -24, -23, \ldots, 0, \ldots, 23, 24$. Time: $t_n = n \cdot T_s / L = n \cdot 0.125$ µs.

**At $n = 0$ (centre tap):** $p_{RC}(0) = 1$ for all $\alpha$.

**At $n = \pm 8$ ($t = \pm T_s$, first zero crossing):** $p_{RC}(\pm T_s) = \text{sinc}(\pm 1) \cdot [\text{finite}] = 0$. ✓

**Sidelobe decay comparison (approximate peak of first sidelobe at $t \approx 1.5 T_s$):**

| $\alpha$ | First sidelobe level (dB) | Decay rate |
|---|---|---|
| 0.0 | $-13$ dB (sinc) | $1/t$ |
| 0.25 | $-40$ dB | $1/t^3$ |
| 0.5 | $-50$ dB | $1/t^3$ |
| 1.0 | $-70$ dB | $1/t^3$ |

Higher $\alpha$ gives much faster sidelobe decay, which means:
1. Better timing sensitivity tolerance (fewer neighbours contribute significant ISI)
2. Easier FIR truncation (fewer taps needed for the same residual ISI level)

---

## Part 3: Root Raised Cosine (RRC) Filter

### Motivation

The raised cosine is the **combined Tx-Rx response**. In a practical system:
- Transmitter applies a pulse shaping filter $H_{TX}(f)$
- Channel: ideal (AWGN) in this problem
- Receiver applies a receive filter $H_{RX}(f) = H_{TX}^*(f)$ (matched filter)

Combined response: $P_{RC}(f) = H_{TX}(f) \cdot H_{RX}(f) = |H_{TX}(f)|^2$

Therefore: $|H_{TX}(f)| = \sqrt{P_{RC}(f)} \Rightarrow H_{TX}(f) = \sqrt{P_{RC}(f)}$

This is the **Root Raised Cosine (RRC)** filter.

### RRC Frequency Response

$$P_{RRC}(f) = \sqrt{P_{RC}(f)} = \begin{cases}
\sqrt{T_s} & |f| \leq f_1 \\[4pt]
\sqrt{\dfrac{T_s}{2}\!\left[1 + \cos\!\left(\dfrac{\pi(|f|-f_1)}{f_2 - f_1}\right)\right]} & f_1 < |f| \leq f_2 \\[8pt]
0 & |f| > f_2
\end{cases}$$

### RRC Time-Domain Impulse Response

The RRC time-domain response is:

$$p_{RRC}(t) = \frac{4\alpha}{\pi\sqrt{T_s}} \cdot \frac{\cos\!\left(\frac{(1+\alpha)\pi t}{T_s}\right) + \frac{T_s}{4\alpha t}\sin\!\left(\frac{(1-\alpha)\pi t}{T_s}\right)}{1 - \left(\frac{4\alpha t}{T_s}\right)^2}$$

**Important:** The RRC pulse does NOT satisfy zero ISI at integer multiples of $T_s$ — it is not a Nyquist pulse. Only the convolution of two RRC filters (i.e., the RC filter) satisfies zero ISI. The eye diagram of a single RRC filter would appear closed.

### Verification: RRC * RRC = RC

In the frequency domain: $|P_{RRC}(f)|^2 = P_{RC}(f)$. In the time domain:

$$p_{RRC}(t) * p_{RRC}(t) = \int_{-\infty}^{\infty} p_{RRC}(\tau) p_{RRC}(t - \tau)\, d\tau = p_{RC}(t)$$

At $t = nT_s$: $p_{RC}(nT_s) = \delta[n]$ — zero ISI confirmed only after the complete Tx+Rx chain.

---

## Part 4: Bandwidth Calculations

The one-sided bandwidth of the raised cosine filter (first null or edge of stopband):

$$B_{RC} = f_2 = \frac{1+\alpha}{2T_s}$$

For $R_s = 1$ Msymbol/s ($T_s = 1$ µs):

| Roll-off $\alpha$ | Bandwidth $B_{RC}$ | Spectral efficiency (QPSK) | Bandwidth (double-sided) |
|---|---|---|---|
| 0.0 | 500 kHz | 4 bit/s/Hz | 1 MHz |
| 0.25 | 625 kHz | 3.2 bit/s/Hz | 1.25 MHz |
| 0.5 | 750 kHz | 2.67 bit/s/Hz | 1.5 MHz |
| 1.0 | 1000 kHz | 2.0 bit/s/Hz | 2 MHz |

**Spectral efficiency with QPSK:** $\eta = 2\log_2(4) / ((1+\alpha) \cdot 2B_{one-sided}) = 2/(1+\alpha)$ bit/s/Hz (using double-sided bandwidth).

---

## Part 5: Eye Diagram Analysis

The eye diagram is formed by overlaying $N_{sym}$ consecutive segments of the filtered signal, each of duration $2T_s$, synchronised to the symbol clock.

### Eye Opening Metrics

**Eye height** at optimal sampling instant $t = 0$ (after removing the mean constellation offset):

Without ISI and noise, the eye height is determined by the minimum distance between adjacent signal levels. With the raised cosine matched-filter pair:
- Eye height $= 2 \cdot \min_{\{a_n\}} |a_0 - \sum_{n \neq 0} a_n p_{RC}(nT_s)|$
- Since $p_{RC}(nT_s) = 0$ for $n \neq 0$: eye height $= 2$ (normalised to $\pm 1$ BPSK levels)

**Effect of $\alpha$ on eye width:**

The eye diagram is open (non-zero height) for a range of timing offsets $|\Delta t| < T_{open}$ around the optimal sampling point.

For $\alpha = 0$ (sinc): The pulse returns from its zero crossings very slowly (sinc sidelobes), so the eye closes sharply near $t = 0$ with any timing offset.

For $\alpha > 0$: The pulse decays faster away from $t = 0$, so the eye remains open over a wider timing window.

**Approximate eye opening width as a function of $\alpha$:**

| $\alpha$ | Normalised eye width $T_{open}/T_s$ |
|---|---|
| 0.0 | 0 (theoretically zero tolerance) |
| 0.25 | ~0.6 |
| 0.5 | ~0.75 |
| 1.0 | ~0.9 |

Larger $\alpha$ → wider eye opening → more robust to timing jitter.

### FIR Truncation Effect on the Eye

With a finite filter span of $N_{span}$ symbols, the tails of the impulse response are truncated. The residual ISI from truncation is:

$$\text{ISI}_{trunc} = \sum_{|n| > N_{span}/2} p_{RC}(nT_s) = 0 \quad \text{(exactly, since } p_{RC}(nT_s) = 0\text{)}$$

For the RC filter, truncation causes zero ISI at the exact sampling instants because the truncated samples are exactly zero. However, the frequency response of the truncated FIR deviates from the ideal RC, causing some ISI at off-nominal sampling times. The eye remains open at $t = 0$ but the crossing traces are not perfectly clean.

For the RRC filter, truncation causes non-zero convolution products — the convolution of two truncated RRC FIRs is not exactly an RC, resulting in non-zero values of the combined response at $t = nT_s, n \neq 0$. This residual ISI is bounded by:

$$\epsilon_{ISI} \approx 2 \sum_{|n| > N_{span}/2} |p_{RRC}(nT_s / L)|^2$$

For $N_{span} = 6$ and $\alpha = 0.35$: $\epsilon_{ISI} \approx -50$ dB — acceptable for most applications.

---

## Summary and Design Recommendations

| Parameter | Recommendation | Rationale |
|---|---|---|
| Roll-off $\alpha$ | 0.2–0.35 for bandwidth-limited; 0.5 for ease of implementation | Trade bandwidth for timing margin |
| Filter span $N_{span}$ | 6–10 symbols | Beyond 8 symbols, residual ISI $< -60$ dB |
| Oversampling $L$ | 4 minimum, 8 preferred | Higher $L$ more accurately approximates ideal frequency response |
| Windowing | Kaiser ($\beta = 6$–$8$) on RRC coefficients | Reduces spectral sidelobe leakage from truncation |

**Key take-away:** The raised cosine is not a single filter but a design constraint on the overall system. The RRC factorisation achieves simultaneously: (1) zero ISI through the Nyquist criterion, (2) maximum SNR through matched filtering, and (3) spectral containment by limiting bandwidth to $(1+\alpha)/T_s$.
