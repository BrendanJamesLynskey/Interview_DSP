# Pulse Shaping and Intersymbol Interference (ISI) — Interview Questions

## Overview

Pulse shaping is the process of filtering transmitted symbols to control the spectral occupancy and time-domain properties of the signal. ISI occurs when energy from one symbol spills into adjacent symbol intervals at the sampling point. This topic is central to any modem design role, as it bridges the theoretical Nyquist criterion with practical filter design.

---

## Tier 1: Fundamentals

### Q1. What is intersymbol interference (ISI) and what causes it?

**Answer:**

ISI is interference at a receiver's sampling instant caused by the residual energy of neighbouring symbols. If the transmitted pulse $p(t)$ has non-zero values at integer multiples of the symbol period $T_s$ other than $t = 0$, adjacent symbols corrupt the desired sample.

**Causes of ISI:**

1. **Transmit pulse bandwidth**: A rectangular pulse has sinc-shaped spectrum extending to infinity; bandlimiting the pulse causes the time-domain response to spread beyond $T_s$.
2. **Channel multipath**: Physical reflections create delayed copies of the signal that arrive at the receiver with timing offsets, effectively widening the pulse.
3. **Receiver filter bandwidth**: Too-narrow receive filter causes time-domain ringing.
4. **Timing errors**: Sampling at the wrong instant moves away from the zero-ISI point.

**Mathematical statement:** The sampled output at symbol $k$ from a received stream $\{a_n\}$ passed through an overall Tx-channel-Rx response $q(t)$ is:

$$y[k] = a_k q(0) + \underbrace{\sum_{n \neq k} a_n\, q\!\bigl((k-n)T_s\bigr)}_{\text{ISI terms}}$$

Zero ISI requires $q(nT_s) = 0$ for all $n \neq 0$.

---

### Q2. State the Nyquist criterion for zero ISI. What does it require of the overall pulse?

**Answer:**

The **Nyquist first criterion** states that a pulse $p(t)$ has zero ISI at uniform sampling instants $\{nT_s\}$ if and only if:

$$p(nT_s) = \begin{cases} 1 & n = 0 \\ 0 & n \neq 0 \end{cases}$$

**Equivalent frequency-domain condition:** Zero ISI at rate $1/T_s$ is achievable if and only if the Fourier transform $P(f)$ satisfies:

$$\sum_{k=-\infty}^{\infty} P\!\left(f - \frac{k}{T_s}\right) = T_s \quad \forall f$$

That is, the periodic sum of frequency-shifted copies of $P(f)$ must be constant (flat). This is the Nyquist folding criterion.

**Minimum bandwidth solution:** The ideal rectangular spectrum

$$P(f) = \begin{cases} T_s & |f| \leq \frac{1}{2T_s} \\ 0 & \text{otherwise} \end{cases}$$

gives $p(t) = \text{sinc}(t/T_s)$, which has perfectly zero crossings at all $nT_s \neq 0$. However, the sinc pulse is non-causal and its slow $1/t$ decay makes it extremely sensitive to timing errors — any small timing offset causes non-zero ISI because many terms contribute.

**Practical implication:** The raised cosine filter is the standard practical solution, providing a smooth rolloff that trades excess bandwidth for much better timing sensitivity.

---

### Q3. What is the raised cosine filter? Define its frequency and time-domain forms.

**Answer:**

The raised cosine (RC) filter is a Nyquist pulse with a cosine-shaped transition band that smoothly rolls off from the passband to the stopband.

**Frequency response:**

$$P_{RC}(f) = \begin{cases}
T_s & |f| \leq \frac{1-\alpha}{2T_s} \\[4pt]
\frac{T_s}{2}\!\left\{1 + \cos\!\left[\frac{\pi T_s}{\alpha}\!\left(|f| - \frac{1-\alpha}{2T_s}\right)\right]\right\} & \frac{1-\alpha}{2T_s} < |f| \leq \frac{1+\alpha}{2T_s} \\[4pt]
0 & |f| > \frac{1+\alpha}{2T_s}
\end{cases}$$

where $\alpha \in [0, 1]$ is the **roll-off factor**.

**Time-domain impulse response:**

$$p_{RC}(t) = \frac{\sin(\pi t/T_s)}{\pi t/T_s} \cdot \frac{\cos(\pi\alpha t/T_s)}{1 - (2\alpha t/T_s)^2}$$

The first factor is the ideal sinc (Nyquist zero crossings); the second factor is the raised cosine envelope that controls sidelobe decay.

**Zero ISI verification:** At $t = nT_s$:
- The sinc factor is zero for $n \neq 0$ (same as ideal case)
- The cosine factor is non-zero and finite (no singularity at the zeros)

Exception: at $t = \pm T_s/(2\alpha)$, both numerator and denominator of the second factor are zero; by L'Hopital's rule, the value is finite ($\pm \alpha/2$ for the limit).

---

### Q4. What is the roll-off factor $\alpha$ and how does it affect system performance?

**Answer:**

The roll-off factor $\alpha \in [0, 1]$ controls the steepness of the transition band.

**Bandwidth:**

$$B_{RC} = \frac{1 + \alpha}{2T_s}$$

- $\alpha = 0$: Minimum bandwidth $B = 1/(2T_s)$ but ideal sinc — impractical
- $\alpha = 1$: Double the minimum bandwidth, very smooth roll-off
- Typical values: $\alpha = 0.2\text{–}0.5$ in practice

**Spectral efficiency:**

$$\eta = \frac{\log_2 M}{(1+\alpha)} \quad \text{bits/s/Hz}$$

**Trade-off summary:**

| $\alpha$ | Bandwidth | Sidelobe decay | Timing sensitivity |
|---|---|---|---|
| 0 (ideal) | $1/(2T_s)$ | Very slow ($1/t$) | Extremely sensitive |
| 0.25 | $0.625/T_s$ | Fast ($1/t^3$) | Low |
| 0.5 | $0.75/T_s$ | Very fast | Very low |
| 1.0 | $1/T_s$ | Fastest | Minimal |

**Practical guidance:** Lower $\alpha$ maximises spectral efficiency but demands tighter frequency accuracy and better filter implementation. Higher $\alpha$ is more forgiving and simpler to implement, preferred in channels with uncertainty in symbol timing.

---

### Q5. What is the root raised cosine (RRC) filter and where is it deployed?

**Answer:**

The root raised cosine filter is defined in the frequency domain as the square root of the raised cosine response:

$$P_{RRC}(f) = \sqrt{P_{RC}(f)}$$

**Why it is used:** In a communications link, the overall Tx-to-Rx pulse response must be raised cosine to satisfy Nyquist zero-ISI. This overall response is the convolution of the transmit filter, channel, and receive filter. In AWGN (ideal channel), splitting the filtering equally between Tx and Rx gives:

$$P_{TX}(f) = P_{RX}(f) = P_{RRC}(f)$$

so that $P_{TX}(f) \cdot P_{RX}(f) = P_{RC}(f)$.

**Optimality:** The RRC split also makes the receive filter a matched filter when the transmit filter is RRC. This achieves the maximum SNR at the sampling instant (optimum detection), combining Nyquist ISI-free sampling with matched filtering in a single structure.

**Time-domain RRC impulse response:**

$$p_{RRC}(t) = \frac{4\alpha}{\pi\sqrt{T_s}} \cdot \frac{\cos\!\left(\frac{(1+\alpha)\pi t}{T_s}\right) + \frac{\sin\!\left(\frac{(1-\alpha)\pi t}{T_s}\right)}{4\alpha t/T_s}}{1 - \left(\frac{4\alpha t}{T_s}\right)^2}$$

**Implementation:** RRC filters are typically implemented as FIR filters with a truncated impulse response (e.g., $\pm 6T_s$ to $\pm 10T_s$ duration), windowed to control spectral sidelobes from the truncation.

---

## Tier 2: Intermediate

### Q6. Explain the eye diagram. What does each feature tell the designer?

**Answer:**

An eye diagram is formed by overlaying successive symbol-period segments of the received (filtered but not yet decoded) waveform, producing a picture that resembles an eye. It is a standard tool for diagnosing pulse shaping quality, ISI, noise, and timing in real hardware.

**How to read it:**

| Feature | What it indicates |
|---|---|
| **Eye opening height** | Vertical noise margin. Larger is better. Closed eye → severe ISI or noise |
| **Eye opening width** | Timing margin. Wider eye → more tolerance to sampling clock jitter |
| **Crossing point spread** | Timing jitter or clock phase noise |
| **Non-zero ISI tails** | Lines that do not cross zero at symbol transitions indicate residual ISI |
| **Multiple trace levels** | Expected for higher-order PAM or QAM (e.g., 3 eye levels for 4-PAM) |

**Effect of roll-off on the eye diagram:**
- Small $\alpha$ (near 0): Eye opens only at the exact sampling instant; any timing error reduces opening dramatically.
- Large $\alpha$ (near 1): Eye opens broadly in time, tolerant of timing offset.

**Interpreting degraded eyes:**
- Random noise → fuzzy crossing traces and fuzzy horizontal lines (uniform spread)
- ISI → deterministic thinning of the eye at specific timing offsets
- Bandwidth limiting → reduced eye height (symbol peaks are rounded off)

---

### Q7. Derive why the matched filter + raised cosine combination eliminates ISI while maximising SNR.

**Answer:**

**System model:** The transmitter applies an RRC filter $h_{TX}(t)$. The channel is AWGN (ideal). The receiver applies an RRC filter $h_{RX}(t) = h_{TX}(-t)$ (matched filter), then samples at $t = kT_s$.

**Step 1 — Zero ISI:** The combined Tx-Rx response is:

$$p(t) = h_{TX}(t) * h_{RX}(t)$$

In frequency domain:
$$P(f) = |H_{TX}(f)|^2 = |P_{RRC}(f)|^2 = P_{RC}(f)$$

Since $P_{RC}(f)$ satisfies the Nyquist criterion, $p(nT_s) = \delta[n]$ and ISI is zero.

**Step 2 — Maximum SNR:** The noise at the output of $h_{RX}$ has PSD $S_n(f) = (N_0/2)|H_{RX}(f)|^2$. The signal component at the sampling instant has energy proportional to $\int |H_{TX}(f)|^2 |H_{RX}(f)|^2\, df$. By the matched filter theorem, setting $H_{RX}(f) = H_{TX}^*(f)$ (conjugate) maximises the SNR, which in this symmetric real case gives $H_{RX}(f) = H_{TX}(f) = P_{RRC}(f)$.

**Conclusion:** The RRC pair simultaneously satisfies the Nyquist zero-ISI condition (through their product being raised cosine) and the matched filtering condition (each filter is matched to the other's signal), achieving the optimal BER performance for the given signal energy.

---

### Q8. How does a bandlimited channel (non-ideal channel response) interact with pulse shaping to cause ISI?

**Answer:**

In practice the channel is not flat — it has a frequency response $C(f)$ that attenuates and delays different frequency components differently. The overall pulse at the receiver is:

$$P_{eff}(f) = H_{TX}(f) \cdot C(f) \cdot H_{RX}(f)$$

Even if $H_{TX}(f) \cdot H_{RX}(f) = P_{RC}(f)$ satisfies Nyquist, $P_{eff}(f)$ will not satisfy Nyquist if $C(f) \neq \text{const}$.

**Multipath channel:** $C(f) = \sum_\ell \beta_\ell e^{-j2\pi f \tau_\ell}$ introduces frequency-selective fading (nulls in $|C(f)|$). The resulting time-domain pulse $p_{eff}(t)$ has non-zero values at $t = nT_s, n \neq 0$, causing ISI.

**Solutions:**

1. **Linear equaliser (ZF or MMSE)**: Apply a digital filter $W(f) \approx 1/C(f)$ after the receive filter to restore the overall response to raised cosine.
2. **DFE (Decision Feedback Equaliser)**: Feed back hard or soft decisions to cancel the causal ISI terms.
3. **OFDM**: Transform the wideband channel into parallel flat-fading sub-channels, eliminating ISI across subcarriers using the cyclic prefix.
4. **Sequence detection (MLSE / Viterbi)**: Treat ISI as known deterministic interference and find the optimal transmitted sequence.

---

### Q9. Design a practical raised cosine FIR filter. What design choices must be made?

**Answer:**

**Step 1 — Determine roll-off factor $\alpha$:** Chosen based on available bandwidth and timing margin requirements. Typical: $\alpha = 0.25\text{–}0.35$ for wireless systems.

**Step 2 — Choose oversampling factor $L$:** Number of samples per symbol. Typical: $L = 4\text{–}8$. Higher $L$ allows more filter taps for the same relative delay.

**Step 3 — Choose filter span $N_{span}$:** Number of symbol periods captured by the filter impulse response, symmetric around $t = 0$. Typical: $N_{span} = 6\text{–}12$ symbols. Total taps: $N = N_{span} \cdot L + 1$ (odd for symmetric FIR).

**Step 4 — Compute coefficients:** Sample the analytical RRC impulse response at $t = nT_s/L$ for $n = -N_{span}L/2, \ldots, N_{span}L/2$.

**Step 5 — Apply window:** Truncation of the infinite sinc introduces sidelobes. A Kaiser or Hamming window reduces spectral splatter at the cost of slightly widening the transition band.

**Design choices and trade-offs:**

| Parameter | Increase | Decrease |
|---|---|---|
| $\alpha$ | More bandwidth, less ISI sensitivity | Less bandwidth, more timing sensitivity |
| $L$ | More accurate frequency response | Higher compute |
| $N_{span}$ | Lower residual ISI, better stopband | Higher latency, more compute |

**Verification:** Check the cascade of Tx and Rx FIR (convolution) for zero crossings at all $\pm kT_s$, and verify the combined frequency response matches the raised cosine specification.

---

### Q10. What is the impact of timing error on ISI in a raised cosine system?

**Answer:**

Let the ideal sampling instant be $t = 0$ and the actual sampling time be $t = \epsilon$ (timing offset). The sampled output is:

$$y[\epsilon] = p_{RC}(\epsilon) + \sum_{n \neq 0} a_n \cdot p_{RC}(nT_s + \epsilon)$$

For the ideal sinc ($\alpha = 0$): $p_{RC}(nT_s + \epsilon) = \text{sinc}(n + \epsilon/T_s)$. For $\epsilon \neq 0$ none of the ISI terms vanish — ISI becomes a sum over all neighbours weighted by the sinc function. The series converges slowly.

For the raised cosine ($\alpha > 0$): The pulse decays as $1/t^3$ rather than $1/t$, so the ISI sum converges much faster. For small $\epsilon$:

$$\text{ISI power} \propto \epsilon^2 \cdot \sum_{n \neq 0} |p'_{RC}(nT_s)|^2$$

where $p'$ denotes the derivative. The ISI-to-signal power ratio is proportional to $(\epsilon/T_s)^2$ — timing jitter of 1% of $T_s$ causes ISI of order $-40$ dB, which is negligible for BPSK/QPSK but may matter for 64-QAM or higher.

**Practical rule of thumb:** For $M$-QAM, the timing error must satisfy:

$$\frac{\epsilon}{T_s} \lesssim \frac{1}{10\sqrt{M}}$$

to keep ISI below the noise floor at the target operating SNR.

---

## Tier 3: Advanced

### Q11. Derive the Nyquist folding criterion from first principles. Why must the spectrum be periodic-sum flat?

**Answer:**

**Setup:** A symbol sequence $\{a_n\}$ is transmitted using pulse $p(t)$:

$$s(t) = \sum_n a_n p(t - nT_s)$$

The receiver samples the output of a unit receive filter at $t = kT_s$:

$$y[k] = \sum_n a_n p\!\bigl((k-n)T_s\bigr)$$

**Zero-ISI condition:** $y[k] = a_k$ requires $p(mT_s) = \delta[m]$.

**Frequency domain:** The Poisson summation formula relates the samples of $p$ to its spectrum $P(f)$:

$$\sum_{m=-\infty}^{\infty} p(mT_s) e^{-j2\pi f m T_s} = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} P\!\left(f - \frac{k}{T_s}\right)$$

For zero ISI, the left side must equal $p(0) = 1$ (a constant, independent of $f$). Therefore:

$$\frac{1}{T_s} \sum_{k=-\infty}^{\infty} P\!\left(f - \frac{k}{T_s}\right) = 1$$

$$\boxed{\sum_{k=-\infty}^{\infty} P\!\left(f - \frac{k}{T_s}\right) = T_s}$$

**Interpretation:** The spectrum $P(f)$, when periodically folded with period $1/T_s$, must be flat. Any spectral ripple or asymmetry in the folded sum creates non-zero ISI. The raised cosine satisfies this exactly: its gradual roll-off in the transition band is exactly anti-symmetric about $f = 1/(2T_s)$, so opposite-side contributions cancel perfectly when folded.

---

### Q12. Compare zero-forcing (ZF) equalisation and MMSE equalisation for ISI mitigation. When does each fail?

**Answer:**

Both approaches model the ISI channel as an FIR or IIR filter $C(z)$ and apply a digital equaliser $W(z)$ after the receive filter.

**Zero-forcing (ZF) equaliser:** $W_{ZF}(z) = 1/C(z)$

The ZF equaliser inverts the channel completely, ensuring zero ISI at all sampling instants. However:

$$\text{Noise PSD at ZF output} = \frac{N_0/2}{|C(e^{j\omega})|^2}$$

At frequencies where $|C(e^{j\omega})|$ is small (channel nulls), the noise is enormously amplified. **ZF fails at channel nulls — it can make noise unbearably large while eliminating ISI.**

**MMSE equaliser:** Minimises mean-squared error $\mathbb{E}[|y[k] - a_k|^2]$ jointly over ISI and noise:

$$W_{MMSE}(e^{j\omega}) = \frac{C^*(e^{j\omega})}{|C(e^{j\omega})|^2 + N_0/\sigma_a^2}$$

The denominator regularises the inversion near channel nulls. At high SNR ($N_0 \to 0$), MMSE approaches ZF. At low SNR, MMSE leaves some ISI to avoid excessive noise enhancement.

**MMSE failure mode:** At very low SNR the regularisation term dominates, the equaliser stops inverting the channel, and residual ISI limits performance (the noise is small but ISI is large).

**Practical choice:** MMSE is almost always preferred in practice. ZF is useful as a conceptual baseline and in systems where SNR is very high (short-range links with tight power budgets).

---

### Q13. Explain the concept of partial response signalling (PR) and how it intentionally introduces controlled ISI.

**Answer:**

Partial response signalling deliberately introduces a known ISI pattern (controlled correlation between adjacent symbols) to enable spectral shaping beyond the Nyquist minimum bandwidth, at the cost of requiring multi-level processing.

**Classic PR example — Duobinary (Class I):** The target overall response is:

$$P(D) = 1 + D \quad \Rightarrow \quad p[n] = \delta[n] + \delta[n-1]$$

The output sample is $y[k] = a_k + a_{k-1}$, which has three levels $\{-2, 0, +2\}$ for binary $a_k \in \{-1, +1\}$.

**Spectral shape:** The frequency response is:

$$P(e^{j\omega T_s}) = 1 + e^{-j\omega T_s} = 2\cos(\omega T_s/2) e^{-j\omega T_s/2}$$

This has a null at $f = 1/(2T_s)$ — the Nyquist frequency — and passes all energy below it. The spectrum is shaped like a half-cosine, which is more bandwidth-efficient than a rectangular spectrum for certain channel types.

**Decoding:** Use **precoding** at the transmitter to convert the encoded sequence so that modulo-2 detection removes the ISI memory without error propagation:

$$b_k = a_k \oplus b_{k-1} \quad \Rightarrow \quad \hat{a}_k = y[k] \bmod 2$$

**Applications:** Magnetic recording (PRML — Partial Response Maximum Likelihood), optical fibre (duo-binary optical modulation for narrow-linewidth channels), hard disk drive read channels.

---

### Q14. How does pulse shaping interact with power amplifier non-linearity? What is the PAPR problem for single-carrier systems?

**Answer:**

The raised cosine pulse $p_{RC}(t)$ creates a passband signal with time-varying envelope (non-constant amplitude). The instantaneous power varies as:

$$P_{inst}(t) = \left|\sum_n a_n p_{RC}(t - nT_s)\right|^2$$

The **Peak-to-Average Power Ratio** (PAPR) is:

$$\text{PAPR} = \frac{\max_t P_{inst}(t)}{\mathbb{E}[P_{inst}(t)]}$$

For typical raised cosine pulse shaping with QPSK:
- $\alpha = 0$: PAPR $\approx$ 3.6 dB
- $\alpha = 0.35$: PAPR $\approx$ 3.2 dB

For higher-order QAM, PAPR increases further because the constellation amplitude varies more.

**Non-linearity problem:** A power amplifier (PA) operating near saturation compresses signal peaks (AM-AM compression) and introduces phase distortion (AM-PM). For a transmitted signal exceeding the amplifier's linear range:
1. **Spectral regrowth**: Non-linear operation generates out-of-band emissions (intermodulation products) that violate spectral masks.
2. **Constellation distortion**: Symbol points are rotated and compressed, opening error floors.

**Mitigations:**
- **PA back-off**: Operate the PA at reduced average power to keep peaks in the linear region. Penalty: reduced power efficiency.
- **Predistortion (DPD)**: Apply the inverse of the PA non-linearity at baseband. Enables higher average power without spectral regrowth.
- **Clipping and filtering**: Hard-clip the waveform and filter out the resulting spectral regrowth. Introduces a small BER penalty.

---

## Common Interview Mistakes

1. **Confusing RC and RRC**: The raised cosine is the *combined* Tx-Rx response. Each filter is an RRC. A common error is implementing an RC filter at the transmitter only, causing the receive filter to add more ISI rather than removing it.
2. **Forgetting the channel**: Pulse shaping achieves zero ISI only in conjunction with the channel. A multipath channel violates the Nyquist condition even with perfect pulse shaping.
3. **Misquoting bandwidth**: Raised cosine bandwidth is $(1+\alpha)/(2T_s)$ (one-sided) or $(1+\alpha)/T_s$ (double-sided). Be explicit about which convention you are using.
4. **Ignoring implementation losses**: FIR truncation, quantised coefficients, and limited oversampling all degrade the zero-ISI property from the theoretical ideal.
5. **Overlooking timing loop interaction**: The pulse shaping filter must be designed jointly with the timing recovery loop, as the filter response affects the timing error signal derivative (S-curve).
