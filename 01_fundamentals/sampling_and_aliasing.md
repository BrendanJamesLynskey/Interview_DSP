# Sampling and Aliasing — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Nyquist Theorem, Shannon Sampling, Anti-Aliasing, Reconstruction, Oversampling
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. State the Nyquist-Shannon sampling theorem. What does it guarantee?

**Answer:**

**Theorem (Shannon, 1949):** A continuous-time bandlimited signal $x_a(t)$ whose spectrum is zero for all frequencies $|f| > f_{max}$ can be **perfectly reconstructed** from its samples $x[n] = x_a(nT_s)$ if the sampling rate satisfies:

$$f_s > 2\,f_{max}$$

The minimum permitted sampling rate is the **Nyquist rate**:

$$f_{Nyquist} = 2\,f_{max}$$

The **Nyquist frequency** (half the sampling rate) is:

$$f_N = \frac{f_s}{2}$$

Any frequency component in the signal above $f_N$ cannot be represented unambiguously and will alias.

**What the theorem guarantees:** With ideal sinc interpolation (see Q5), the original continuous-time signal can be recovered exactly — not approximately. The reconstruction is mathematically lossless under the bandlimited assumption.

**Common misunderstandings:**
- "Sampling at exactly $2f_{max}$" is the theoretical minimum but fails in practice (zero-measure issue at exactly the Nyquist rate for sinusoidal components at precisely $f_{max}$). Practical systems always oversample to some degree.
- The theorem assumes infinite duration signals. Real signals are windowed, which broadens their spectra.
- "Digital audio at 44.1 kHz captures frequencies up to 22.05 kHz" — correct but requires an anti-aliasing filter before the ADC.

---

### Q2. What is aliasing? Give a concrete numerical example.

**Answer:**

**Aliasing** is the phenomenon where a frequency component above the Nyquist frequency $f_N = f_s/2$ masquerades as a lower frequency after sampling. The alias relationship is:

$$f_{alias} = \left| f - k\,f_s \right| \quad \text{for the integer } k \text{ that brings the result into } [0, f_s/2]$$

More precisely, a continuous-time sinusoid at frequency $f_0$ sampled at $f_s$ is indistinguishable from a sinusoid at any frequency $f_0 + k\,f_s$, $k \in \mathbb{Z}$.

**Concrete example:**

Sampling rate $f_s = 8\,\text{kHz}$ (telephone quality). Nyquist frequency = 4 kHz.

A 5 kHz tone sampled at 8 kHz:

$$f_{alias} = |5000 - 8000| = 3000\,\text{Hz}$$

The recorded 5 kHz tone reappears as a 3 kHz tone in the digital signal. Both $\cos(2\pi \cdot 5000\,t)$ and $\cos(2\pi \cdot 3000\,t)$, when sampled at $T_s = 1/8000\,\text{s}$, produce the same sequence of numbers.

**Proof:** $\cos(2\pi f_0 n T_s) = \cos(2\pi(f_0 + k f_s) n T_s)$ because the extra term contributes $2\pi k n$, which is a multiple of $2\pi$ and vanishes.

**Audio consequence:** Aliasing sounds like phantom tones or distortion, often described as metallic or "digital harshness" in early inadequately filtered digital audio.

---

### Q3. What is an anti-aliasing filter and where must it be placed?

**Answer:**

An **anti-aliasing filter (AAF)** is a lowpass filter that attenuates all signal energy above the Nyquist frequency $f_N = f_s/2$ before the signal is sampled.

**Placement:** The AAF must be applied in the **continuous-time (analog) domain, before the ADC**. This is non-negotiable. Once sampling has occurred, aliased components are mathematically identical to legitimate low-frequency components — they cannot be distinguished and cannot be removed.

**Ideal AAF:** A brick-wall lowpass filter with cutoff at $f_N$:

$$H_{AAF}(f) = \begin{cases} 1 & |f| \leq f_N \\ 0 & |f| > f_N \end{cases}$$

**Practical constraints:**
- An ideal brick-wall filter has infinite impulse response duration (sinc) and infinite roll-off rate — not realisable in hardware.
- Real analog anti-aliasing filters (Butterworth, Chebyshev, elliptic) have finite roll-off. To achieve adequate attenuation before $f_N$, the filter cutoff is set below $f_N$, which sacrifices some of the wanted signal bandwidth.
- This trade-off is largely solved by **oversampling**: sample at $K\cdot f_s$ where $K \gg 1$. The transition band of the AAF now spans $[f_{max}, K\cdot f_s - f_{max}]$, an enormous range that a simple first- or second-order filter can handle comfortably. A sharp digital lowpass filter then follows.

---

### Q4. What is oversampling and what advantages does it provide?

**Answer:**

**Oversampling** means sampling at a rate significantly higher than the Nyquist rate:

$$f_{os} = K \cdot f_{Nyquist} = 2K\,f_{max}$$

where $K$ is the **oversampling ratio** (OSR), typically a power of 2 (4, 8, 16, 64, ...).

**Advantages:**

1. **Relaxed anti-aliasing filter requirements:** The guard band (from $f_{max}$ to $f_{os} - f_{max}$) is much wider, so a simple low-order analog filter suffices. For $K = 8$, the transition band is $[20\,\text{kHz},\, 140\,\text{kHz}]$ for audio — easily handled by a first-order RC filter.

2. **Improved SNR through noise shaping (sigma-delta):** Quantisation noise is spread over $[0, f_{os}/2]$. After digital lowpass filtering to $[0, f_{max}]$, the noise power in-band is reduced by factor $K$. Each doubling of the OSR gains approximately 3 dB (0.5 bits). Sigma-delta modulators push this further by **noise shaping** — concentrating noise at high frequencies where it is filtered out.

3. **Reduced filter phase distortion:** A first-order analog AAF has much flatter group delay across the signal band than a high-order filter.

4. **Easier DAC reconstruction filtering:** Same principle applies on output — a gentler reconstruction filter is possible.

**Quantitative SNR gain from OSR (white noise model):**

$$\text{SNR gain} = 10\log_{10}(K) \;\text{dB} = \frac{10}{2}\log_{10}(K) \;\text{dB per doubling, for flat noise}$$

---

## Intermediate

### Q5. Derive the reconstruction formula (ideal sinc interpolation) from the sampling theorem.

**Answer:**

**Setup:** Sample $x_a(t)$ at rate $f_s$ to get $x[n] = x_a(n T_s)$ where $T_s = 1/f_s$.

In the frequency domain, sampling creates a periodic replication of the spectrum:

$$X_s(f) = f_s \sum_{k=-\infty}^{\infty} X_a(f - k f_s)$$

If $x_a(t)$ is bandlimited to $|f| \leq f_{max} < f_s/2$, the spectral replicas do not overlap (no aliasing). To recover $X_a(f)$, apply an ideal lowpass filter with gain $T_s$ and cutoff $f_s/2$:

$$X_a(f) = T_s \cdot X_s(f) \cdot \text{rect}\!\left(\frac{f}{f_s}\right)$$

The ideal reconstruction filter has impulse response:

$$h_r(t) = \text{sinc}(f_s t) = \frac{\sin(\pi f_s t)}{\pi f_s t}$$

**Reconstruction formula:**

Convolving the impulse train $\sum_n x[n]\,\delta(t - nT_s)$ with $h_r(t)$:

$$\boxed{x_a(t) = \sum_{n=-\infty}^{\infty} x[n]\;\text{sinc}\!\left(\frac{t - nT_s}{T_s}\right)}$$

where $\text{sinc}(u) = \frac{\sin(\pi u)}{\pi u}$.

**Verification:** At $t = mT_s$: $\text{sinc}(m - n) = \delta[m-n]$, so $x_a(mT_s) = x[m]$. The formula passes through the original samples exactly and interpolates smoothly between them.

**Why sinc is impractical:** The sinc function has infinite support — reconstruction would require infinite past and future samples. In practice, the sinc is windowed (e.g., Lanczos kernel) and the DAC uses a zero-order hold (ZOH) or first-order hold followed by an analog filter.

---

### Q6. Describe the frequency-domain effect of sampling using the impulse train model.

**Answer:**

**Ideal sampling model:** Multiplication by an impulse train:

$$x_s(t) = x_a(t) \cdot p(t), \qquad p(t) = T_s\sum_{n=-\infty}^{\infty}\delta(t - nT_s)$$

**Fourier transform of $p(t)$:** An impulse train in time is an impulse train in frequency:

$$P(f) = \sum_{k=-\infty}^{\infty} \delta(f - k f_s)$$

**Convolution theorem** — multiplication in time is convolution in frequency:

$$X_s(f) = X_a(f) * P(f) = \sum_{k=-\infty}^{\infty} X_a(f - k f_s)$$

The spectrum of the sampled signal is an **infinite sum of shifted copies** of the original spectrum, spaced $f_s$ apart.

**Aliasing condition:** Copies overlap when $f_s < 2 f_{max}$.

If $f_s = 6\,\text{kHz}$ and the signal has content at $4\,\text{kHz}$:

- Original component at $+4\,\text{kHz}$
- Shifted copy: $4\,\text{kHz} - 6\,\text{kHz} = -2\,\text{kHz}$
- This $-2\,\text{kHz}$ copy overlaps with the original band $[-3, 3]\,\text{kHz}$

The $4\,\text{kHz}$ component aliases to $2\,\text{kHz}$, permanently corrupting that frequency bin.

---

### Q7. What is bandpass sampling and when should you use it?

**Answer:**

**Bandpass (sub-Nyquist) sampling** exploits the fact that for a bandpass signal occupying $[f_L, f_H]$ with bandwidth $B = f_H - f_L$, the minimum sampling rate is not $2f_H$ but approximately:

$$f_s \geq 2B$$

**Condition for valid bandpass sampling:**

The sampling rate $f_s$ must satisfy:

$$\frac{2f_H}{m} \leq f_s \leq \frac{2f_L}{m-1}$$

for some positive integer $m \leq \lfloor f_H / B \rfloor$.

The sampling deliberately aliases the bandpass signal to baseband. The aliased baseband replica can be cleanly separated from other replicas if the intervals are chosen correctly.

**Example:** AM radio signal centred at 900 kHz with $B = 10\,\text{kHz}$: $f_L = 895\,\text{kHz}$, $f_H = 905\,\text{kHz}$.

Naive sampling would require 1.81 MHz. With $m = 45$:

$$f_s \geq \frac{2 \times 905\,\text{kHz}}{45} = 40.2\,\text{kHz}$$

Sampling at just above 40.2 kHz is sufficient. The band folds down to near DC.

**When to use it:**
- Software-defined radio (SDR) front-ends sampling narrowband channels within a wide carrier
- Radar receivers where the carrier frequency is far higher than the bandwidth
- Ultrasound imaging — the pulse bandwidth is small relative to the carrier

**Pitfall:** The anti-aliasing filter must now be a **bandpass filter** that passes only the desired band $[f_L, f_H]$ and rejects everything else. Strict transition band requirements often make this harder than it appears.

---

### Q8. What is the frequency response of a practical zero-order hold (ZOH) DAC? How is the ZOH distortion compensated?

**Answer:**

A ZOH DAC holds each sample value constant for one sample period $T_s$ before the next update:

$$h_{ZOH}(t) = \begin{cases} 1 & 0 \leq t < T_s \\ 0 & \text{otherwise} \end{cases}$$

**Frequency response:**

$$H_{ZOH}(f) = T_s\,\text{sinc}(f T_s)\,e^{-j\pi f T_s}$$

- Magnitude: $|H_{ZOH}(f)| = T_s\left|\text{sinc}(f T_s)\right|$
- At $f = 0$: gain = $T_s$ (normalised to 1 by downstream gain)
- At $f = f_s/2$: $|H_{ZOH}| = T_s\,|\text{sinc}(0.5)| = T_s \cdot \frac{2}{\pi} \approx 0.637\,T_s$

**Droop:** The ZOH attenuates high-frequency components. At the Nyquist frequency, the loss is approximately $3.92\,\text{dB}$. This is the "ZOH droop."

**Compensation options:**

1. **Analog reconstruction filter with inverse ZOH shaping:** Design the post-DAC analog filter to have a passband that rises at $\frac{\pi f/f_s}{\sin(\pi f/f_s)}$ to cancel the droop.

2. **Digital pre-compensation:** Apply a digital FIR or IIR filter with response $\frac{1}{H_{ZOH}(e^{j\omega})}$ before the DAC. This boosts high frequencies to pre-compensate.

3. **Oversampling:** At high OSR, the ZOH droop within the signal band $[0, f_{max}] \ll [0, f_s/2]$ becomes negligible. At $K=8\times$ oversampling, the maximum droop in-band is tiny.

In practice, oversampling is the preferred solution as it simultaneously relaxes the analog reconstruction filter requirements and renders ZOH droop inconsequential.

---

## Advanced

### Q9. Derive the minimum sampling rate condition from the non-overlap of spectral replicas. Show explicitly what happens at exactly the Nyquist rate for a cosine at $f_{max}$.

**Answer:**

**Spectral replica non-overlap condition:**

The sampled spectrum is:

$$X_s(f) = \sum_{k=-\infty}^{\infty} X_a(f - k f_s)$$

The $k=0$ replica occupies $[-f_{max}, f_{max}]$. The $k=1$ replica occupies $[f_s - f_{max},\, f_s + f_{max}]$.

Non-overlap requires:

$$f_{max} < f_s - f_{max} \implies f_s > 2\,f_{max}$$

Hence $f_s > 2\,f_{max}$ (strict inequality).

**At exactly $f_s = 2\,f_{max}$:**

Let $x_a(t) = \cos(2\pi f_{max} t)$. Its spectrum consists of impulses at $\pm f_{max}$.

Samples: $x[n] = \cos(2\pi f_{max} n T_s) = \cos(\pi n) = (-1)^n$

This is the sequence $\{1, -1, 1, -1, \ldots\}$ — a valid, unique sequence representing the Nyquist frequency cosine. Perfect in principle.

**The problem:** Consider $x_a(t) = \cos(2\pi f_{max} t + \phi)$ with arbitrary phase $\phi$:

$$x[n] = \cos(\pi n + \phi) = (-1)^n \cos\phi$$

For $\phi = 0$: $\{1,-1,1,-1,\ldots\}$

For $\phi = \pi/2$: $\{0,0,0,0,\ldots\}$ — all zeros! The signal is invisible to the sampler.

The samples at exactly the Nyquist rate are not sufficient to reconstruct a sinusoid at exactly $f_{max}$ if the phase is unknown. This is why practical systems require $f_s > 2\,f_{max}$ (strict), and why real ADC anti-aliasing filters cut off below $f_N$ to ensure a finite transition band.

---

### Q10. Compare aliasing in uniform sampling versus the alias folding pattern in bandpass sampling for a specific case. Show all spectral replicas.

**Answer:**

**Scenario:** Signal occupies $[f_L, f_H] = [10, 14]\,\text{kHz}$. Bandwidth $B = 4\,\text{kHz}$.

**Case A — Baseband sampling at 30 kHz (correct, no aliasing):**

Spectral replicas centre at $k \times 30\,\text{kHz}$. The band $[10, 14]$ is well inside $[0, 15]$ kHz. No aliasing. Reconstruction filter passes $[0, 15]$ kHz. Expensive — 30 kHz > $2\times 14 = 28$ kHz minimum.

**Case B — Inadequate sampling at 20 kHz (aliasing):**

Replica from $k=-1$: $[10-20, 14-20] = [-10, -6]$ kHz. Negative frequencies fold: $[6, 10]$ kHz. This overlaps with the original $[10, 14]$ kHz range at $f = 10$ kHz — aliasing occurs at the band edge. Severely distorted.

**Case C — Bandpass sampling at 8 kHz ($m = 3$):**

Check validity: $\frac{2 \times 14}{3} = 9.33$ kHz, $\frac{2 \times 10}{2} = 10$ kHz. So $f_s = 9.5$ kHz works. Use $f_s = 10$ kHz for simplicity.

Replicas: $[10, 14]$, $[10-10, 14-10] = [0, 4]$, $[10-20, 14-20] \to [6, 10]$ after folding.

- $k=0$: $[10, 14]$ kHz
- $k=-1$: $[0, 4]$ kHz (desired baseband alias)
- $k=-2$: $[-10, -6] \to [6, 10]$ kHz (folds to $[6, 10]$)

With $f_s = 10$ kHz the three replicas in $[0, 5]$ kHz are at $[0, 4]$ only — no overlap within $[0, f_s/2] = [0, 5]$ kHz. The signal aliases cleanly to $[0, 4]$ kHz. A lowpass reconstruction filter with cutoff 4 kHz recovers the baseband version of the signal.

This achieves a 10 kHz sample rate instead of 28 kHz — a 2.8x saving in data rate.

---

### Q11. Quantify how oversampling improves ADC effective resolution in the presence of quantisation noise. Derive the relationship between OSR and effective number of bits (ENOB).

**Answer:**

**Quantisation noise model:**

For a $B$-bit ADC with full-scale range $V_{FS}$, the quantisation step is $\Delta = V_{FS}/2^B$. Under the white noise model, quantisation error $e[n]$ is uniformly distributed on $[-\Delta/2, \Delta/2]$ and spectrally white over $[0, f_s/2]$.

**Total quantisation noise power:**

$$\sigma_e^2 = \frac{\Delta^2}{12}$$

**Power spectral density of quantisation noise (white):**

$$S_e(f) = \frac{\sigma_e^2}{f_s/2} = \frac{\Delta^2}{6\,f_s} \qquad \text{for } 0 \leq f \leq f_s/2$$

**In-band noise power after lowpass filter to $f_{max}$:**

$$\sigma_{e,\text{in-band}}^2 = S_e(f) \times f_{max} = \frac{\Delta^2}{6\,f_s} \times f_{max} = \frac{\Delta^2}{12} \cdot \underbrace{\frac{2\,f_{max}}{f_s}}_{1/\text{OSR}}$$

$$\sigma_{e,\text{in-band}}^2 = \frac{\Delta^2}{12 \cdot \text{OSR}}$$

**SNR improvement:**

Compared to Nyquist sampling ($\text{OSR}=1$), the in-band noise power is reduced by factor $\text{OSR}$:

$$\text{SNR improvement} = 10\log_{10}(\text{OSR})\,\text{dB}$$

Each octave (doubling) of OSR gives $10\log_{10}(2) \approx 3.01\,\text{dB}$.

**ENOB gain:**

Standard ADC SNR formula: $\text{SNR} \approx 6.02B + 1.76\,\text{dB}$ (sinusoidal input, $B$ bits).

Each 6.02 dB of SNR improvement corresponds to 1 additional bit of resolution:

$$\Delta B = \frac{10\log_{10}(\text{OSR})}{6.02} \approx \frac{\log_2(\text{OSR})}{2}$$

For $\text{OSR} = 64$: $\Delta B = \frac{6}{2} = 3$ extra bits. A 16-bit ADC oversampled at $64\times$ behaves like a 19-bit ADC (before noise shaping). With noise shaping (sigma-delta), the gain is far more — up to $\frac{2B+1}{2}$ extra bits for an $N$th-order modulator.

---

## Quick Reference

| Parameter | Formula |
|---|---|
| Nyquist rate | $f_s > 2\,f_{max}$ |
| Alias of $f_0$ at rate $f_s$ | $f_0 \bmod f_s$, folded to $[0, f_s/2]$ |
| Reconstruction filter cutoff | $f_N = f_s/2$ |
| ZOH magnitude response | $T_s\,\|\text{sinc}(fT_s)\|$ |
| Oversampling SNR gain | $10\log_{10}(\text{OSR})\,\text{dB}$ |
| ENOB gain from oversampling | $\frac{1}{2}\log_2(\text{OSR})$ bits |
