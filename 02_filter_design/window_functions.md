# Window Functions — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Rectangular, Hamming, Hanning, Blackman, Kaiser Windows, Spectral Analysis vs Filter Design
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Why are window functions needed in DSP? What fundamental trade-off do all windows embody?

**Answer:**

**The truncation problem:** All practical DSP systems work with finite-duration signals. Observing (or computing) only $N$ samples of an infinite signal is equivalent to multiplying by a rectangular window of length $N$:

$$x_w[n] = x[n] \cdot w[n]$$

In the frequency domain, multiplication becomes convolution:

$$X_w(e^{j\omega}) = X(e^{j\omega}) * W(e^{j\omega})$$

The observed spectrum is the true spectrum smeared by the window's frequency response $W(e^{j\omega})$.

**The fundamental trade-off:**

Every window involves an irreducible trade-off between two properties of $W(e^{j\omega})$:

1. **Main lobe width** $\Delta\omega_{ML}$: Determines the ability to resolve two closely-spaced frequency components (frequency resolution). A narrow main lobe is desirable.

2. **Peak sidelobe level** (PSL): Determines the dynamic range — how well a weak component near a strong one can be detected without being buried in the strong component's spectral leakage. Low sidelobes are desirable.

**These two goals conflict:** Narrowing the main lobe (by using fewer taps or a simpler window) inevitably raises the sidelobes, and vice versa. This is a consequence of the time-bandwidth product uncertainty principle: a narrow time window has a broad frequency response, and a window with compact frequency support must have a long time extent.

There is no window that has both a narrow main lobe and low sidelobes — any improvement in one comes at the expense of the other.

---

### Q2. Describe the rectangular, Hanning, Hamming, and Blackman windows. Give the definition and key spectral characteristics of each.

**Answer:**

**Rectangular window:**

$$w_R[n] = 1, \quad 0 \leq n \leq N-1$$

- Main lobe width (first nulls): $4\pi/N$
- Peak sidelobe level: $-13\,\text{dB}$
- Sidelobe roll-off: $6\,\text{dB/octave}$
- Provides the best frequency resolution (narrowest main lobe) of any window of length $N$
- Use case: coherent sampling where no leakage occurs; almost never used for general spectral analysis

**Hanning (von Hann) window:**

$$w_{Hann}[n] = 0.5\left(1 - \cos\!\left(\frac{2\pi n}{N-1}\right)\right)$$

- Equivalent to: $0.5 - 0.5\cos(2\pi n/(N-1))$
- Main lobe width: $8\pi/N$ (twice rectangular)
- Peak sidelobe level: $-31.5\,\text{dB}$
- Sidelobe roll-off: $18\,\text{dB/octave}$ (much faster than rectangular)
- Use case: general-purpose spectral analysis

**Hamming window:**

$$w_{Ham}[n] = 0.54 - 0.46\cos\!\left(\frac{2\pi n}{N-1}\right)$$

- Main lobe width: $8\pi/N$ (similar to Hanning)
- Peak sidelobe level: $-41\,\text{dB}$ (better than Hanning)
- Note: the asymmetric coefficients ($0.54$, $0.46$) are chosen to place a zero exactly at the first sidelobe of the Hann window, raising one nearby sidelobe slightly but suppressing the first sidelobe relative to Hanning
- Sidelobe roll-off: $6\,\text{dB/octave}$ (slower than Hanning — a trade-off)
- Use case: audio processing, narrowband signal detection

**Blackman window:**

$$w_B[n] = 0.42 - 0.5\cos\!\left(\frac{2\pi n}{N-1}\right) + 0.08\cos\!\left(\frac{4\pi n}{N-1}\right)$$

- Main lobe width: $12\pi/N$ (widest of the four)
- Peak sidelobe level: $-57\,\text{dB}$
- Sidelobe roll-off: $18\,\text{dB/octave}$
- Use case: high dynamic range spectral measurements

| Window | Main lobe (bins) | PSL (dB) | Roll-off (dB/oct) |
|---|---|---|---|
| Rectangular | 2 | $-13$ | 6 |
| Hanning | 4 | $-31.5$ | 18 |
| Hamming | 4 | $-41$ | 6 |
| Blackman | 6 | $-57$ | 18 |

---

### Q3. What is the Kaiser window? What does the $\beta$ parameter control?

**Answer:**

The **Kaiser window** is defined as:

$$w_K[n] = \frac{I_0\!\left(\beta\sqrt{1-(2n/(N-1)-1)^2}\right)}{I_0(\beta)}, \quad 0 \leq n \leq N-1$$

where $I_0(\cdot)$ is the modified Bessel function of the first kind, order zero.

**The $\beta$ parameter** controls the trade-off between main lobe width and sidelobe level:

- **$\beta = 0$:** Reduces to the rectangular window (no tapering)
- **$\beta \approx 5.44$:** Approximates the Hamming window
- **$\beta \approx 6$:** $\approx$ Blackman level sidelobes
- **$\beta$ increasing:** Sidelobes decrease further, main lobe widens

**Approximate design formulas:**

Given desired stopband attenuation $A_s$ (in dB, positive):

$$\beta \approx \begin{cases}
0 & A_s \leq 21\,\text{dB} \\
0.5842(A_s - 21)^{0.4} + 0.07886(A_s - 21) & 21 < A_s \leq 50\,\text{dB} \\
0.1102(A_s - 8.7) & A_s > 50\,\text{dB}
\end{cases}$$

Required filter order for transition bandwidth $\Delta\omega$:

$$N \approx \frac{A_s - 8}{2.285\,\Delta\omega}$$

**Why Kaiser is practically important:**

The Kaiser window is the most flexible fixed-function window because $\beta$ continuously controls the sidelobe level. Given a specific $A_s$ requirement (e.g., $60\,\text{dB}$), you can compute the required $\beta$ and $N$ exactly. Other windows (Hamming, Blackman) have fixed sidelobe levels — you either over-design or under-design.

In MATLAB: `kaiser(N, beta)`. The `kaiserord` function estimates $N$ and $\beta$ from filter specifications.

---

## Intermediate

### Q4. Differentiate between using window functions for spectral analysis versus filter design. How do the objectives and trade-offs differ?

**Answer:**

**Spectral analysis:**

Goal: Accurately estimate the frequency content of a signal from $N$ samples.

Relevant considerations:
1. **Frequency resolution** (ability to separate two nearby spectral peaks): determined by main lobe width $\sim 1/(N\Delta T)$ in Hz. Longer records and narrower windows (lower $\beta$ for Kaiser) give better resolution.
2. **Dynamic range** (ability to detect a weak peak near a strong one): determined by sidelobe level. Lower sidelobes allow weaker signals to be detected.
3. **Amplitude accuracy:** Windows with lower amplitude gain at non-DC frequencies (Hamming, Blackman) require amplitude correction.
4. **Coherent leakage:** If the frequency of interest does not fall on a DFT bin, leakage spreads energy. Low-sidelobe windows reduce this spreading.

Best choices: Hanning (good all-around), Blackman (high dynamic range), Kaiser (tunable).

**Filter design (windowed sinc method):**

Goal: Design an FIR filter with a specific frequency response (passband, stopband, ripple).

Relevant considerations:
1. **Stopband attenuation** $A_s$: Directly set by the window's sidelobe level. You choose the window primarily based on $A_s$.
2. **Filter order $N$**: Determined by the transition bandwidth and the window's main lobe width. A wider main lobe means more taps needed.
3. **Passband flatness**: Windows with very low sidelobes can still have passband ripple; this ripple equals the sidelobe level relative to the passband.
4. **Phase:** All symmetric windows give linear phase.

The window is chosen based on the required $A_s$; the order $N$ is then determined by the transition bandwidth.

**Key difference in focus:**

| Aspect | Spectral Analysis | Filter Design |
|---|---|---|
| Primary concern | Resolution vs. leakage | Stopband attenuation |
| Window choice driver | Dynamic range requirement | Ripple specification |
| $N$ choice | Fixed by data available | Computed from transition BW |
| Frequency accuracy | Critical | Not a concern |

---

### Q5. How is the Kaiser window used to design an FIR lowpass filter with specified stopband attenuation? Walk through a complete example.

**Answer:**

**Specifications:** Design a lowpass FIR filter with:
- Passband edge: $f_p = 3\,\text{kHz}$, $f_s = 16\,\text{kHz}$
- Stopband edge: $f_{stop} = 4\,\text{kHz}$
- Stopband attenuation: $A_s = 60\,\text{dB}$
- Passband ripple: $\leq 0.1\,\text{dB}$

**Step 1: Convert to digital frequencies:**

$$\omega_p = 2\pi \times 3000/16000 = 0.375\pi, \quad \omega_{stop} = 2\pi \times 4000/16000 = 0.5\pi$$

Transition bandwidth: $\Delta\omega = 0.5\pi - 0.375\pi = 0.125\pi$ rad/sample.

**Step 2: Compute $\beta$ for $A_s = 60\,\text{dB}$:**

Since $A_s > 50\,\text{dB}$:

$$\beta = 0.1102(60 - 8.7) = 0.1102 \times 51.3 \approx 5.653$$

**Step 3: Estimate filter order:**

$$N \approx \frac{A_s - 8}{2.285\,\Delta\omega} = \frac{60 - 8}{2.285 \times 0.125\pi} = \frac{52}{0.898} \approx 57.9 \Rightarrow N = 59 \text{ (odd, for Type I)}$$

**Step 4: Set cutoff at midpoint of transition band:**

$$\omega_c = \frac{\omega_p + \omega_{stop}}{2} = \frac{0.375\pi + 0.5\pi}{2} = 0.4375\pi$$

**Step 5: Compute ideal impulse response:**

$$h_d[n] = \frac{\sin(\omega_c(n-\alpha))}{\pi(n-\alpha)}, \quad \alpha = (N-1)/2 = 29, \quad n = 0, \ldots, 58$$

At $n = \alpha$: $h_d[\alpha] = \omega_c/\pi = 0.4375$.

**Step 6: Apply Kaiser window and truncate:**

$$h[n] = h_d[n] \cdot w_K[n]$$

where $w_K[n]$ uses $\beta = 5.653$.

```python
import numpy as np
from scipy.signal import kaiserord, firwin

# Equivalent one-line design using SciPy
N, beta = kaiserord(60, 0.125)  # 60 dB attenuation, 0.125*pi normalised BW
h = firwin(N, 0.4375, window=('kaiser', beta))
# N ≈ 59, beta ≈ 5.65
```

**Step 7: Verification:**

The resulting filter should have:
- Passband ripple $< 0.1\,\text{dB}$ ✓ (Kaiser at 60 dB gives $\delta \approx 10^{-3}$ in both bands)
- Stopband attenuation $\geq 60\,\text{dB}$ ✓

---

### Q6. Explain the concept of scalloping loss (amplitude loss) in spectral analysis. Which windows suffer most and how is it corrected?

**Answer:**

**Scalloping loss** (also called "picket fence effect"): When a sinusoid's frequency falls between two DFT bin frequencies, its DFT coefficients near the true frequency are reduced in amplitude compared to when it falls exactly on a bin.

The worst case occurs when the frequency is exactly halfway between two bins. The magnitude loss relative to on-bin measurement is the **maximum scalloping loss**:

$$L_{scallop} = \left|W\!\left(e^{j\pi/(N)}\right)\right| / \left|W\!\left(e^{j0}\right)\right|$$

where $W(e^{j\omega})$ is the window's DTFT.

**Scalloping loss for common windows:**

| Window | Max scalloping loss (dB) |
|---|---|
| Rectangular | $-3.9$ |
| Hanning | $-1.4$ |
| Hamming | $-1.8$ |
| Blackman | $-1.1$ |
| Kaiser ($\beta=6$) | $-1.0$ |
| Flat-top | $\approx 0$ |

Rectangular has the **worst** scalloping loss because its main lobe drops steeply away from the peak.

**Flat-top window:** Designed specifically to have $< 0.01\,\text{dB}$ scalloping loss, at the cost of a very wide main lobe and poor frequency resolution. Used in calibration and amplitude measurement applications.

**Correction methods:**

1. **Zero-padding + peak interpolation:** Zero-pad by $\times 8$ or more before taking the FFT. Locate the peak bin and fit a parabola (or use the Jacobsen-Kok interpolator) to estimate the true frequency. The interpolated peak amplitude corrects for scalloping.

2. **Amplitude correction factor:** Apply a correction $1/|W(e^{j0})|$ to normalise all window-scaled amplitudes to the true signal amplitude. This corrects on-bin amplitude but does not correct scalloping loss for off-bin frequencies.

3. **Coherent sampling:** Choose the sample length and frequency such that $f_0 = k\,f_s/N$ for integer $k$ — eliminates scalloping entirely for that frequency.

---

## Advanced

### Q7. Derive the DTFT of the Hanning window and verify its connection to the rectangular window's DTFT.

**Answer:**

The Hanning window is:

$$w_H[n] = \frac{1}{2}\left[1 - \cos\!\left(\frac{2\pi n}{N-1}\right)\right] = \frac{1}{2} - \frac{1}{4}e^{j2\pi n/(N-1)} - \frac{1}{4}e^{-j2\pi n/(N-1)}$$

for $n = 0, 1, \ldots, N-1$.

**DTFT of the rectangular window $w_R[n] = 1$, $0 \leq n \leq N-1$:**

$$W_R(e^{j\omega}) = e^{-j\omega(N-1)/2}\,\frac{\sin(\omega N/2)}{\sin(\omega/2)}$$

This is the Dirichlet kernel.

**DTFT of the Hanning window:**

Using the frequency-shift property of the DTFT: multiplying by $e^{j\omega_0 n}$ shifts the spectrum by $\omega_0$. The digital frequency corresponding to $2\pi/(N-1)$ rad/sample is $\omega_0 = 2\pi/(N-1)$.

$$W_H(e^{j\omega}) = \frac{1}{2}W_R(e^{j\omega}) - \frac{1}{4}W_R(e^{j(\omega - 2\pi/(N-1))}) - \frac{1}{4}W_R(e^{j(\omega + 2\pi/(N-1))})$$

The Hanning window's DTFT is a **weighted sum of three shifted Dirichlet kernels**. The negative-coefficient side lobes of the central kernel partially cancel with the positive main lobes of the shifted kernels near the sidelobe region, dramatically reducing the net sidelobe level.

**Why sidelobes are suppressed:**

The first sidelobe of $W_R$ at $\pm 3\pi/N$ overlaps with the main lobes of the $\pm 2\pi/(N-1)$ shifted copies ($\approx \pm 2\pi/N$ for large $N$). The subtractive combination reduces the sidelobe amplitude from $-13\,\text{dB}$ (rectangular) to $-31.5\,\text{dB}$ (Hanning).

The main lobe doubles in width because adding three kernels — even with partial cancellation at the edges — broadens the combined main lobe.

---

### Q8. What is a flat-top window? Describe its design philosophy and when it is used over standard spectral analysis windows.

**Answer:**

A **flat-top window** is designed so that the window's DTFT magnitude response is maximally flat near $\omega = 0$ (i.e., near the main lobe peak), at the expense of a very wide main lobe and higher sidelobes than windows like Blackman.

**Design philosophy:**

For amplitude-accurate spectrum measurements, the amplitude of a DFT peak must not depend on where the sinusoid frequency falls relative to DFT bins. A flat-top window achieves this by having:

$$\left|\frac{d|W(e^{j\omega})|}{d\omega}\right|_{\omega=0} \approx 0 \quad \text{(flatness condition)}$$

The resulting window's amplitude spectrum is very flat within $\pm 1$ bin of the peak, so scalloping loss is nearly zero.

**Typical flat-top window (Heinzel et al.):**

$$w[n] = a_0 - a_1\cos\!\left(\frac{2\pi n}{N}\right) + a_2\cos\!\left(\frac{4\pi n}{N}\right) - a_3\cos\!\left(\frac{6\pi n}{N}\right) + a_4\cos\!\left(\frac{8\pi n}{N}\right)$$

with coefficients (one standard set): $a_0 = 0.2156$, $a_1 = 0.4160$, $a_2 = 0.2781$, $a_3 = 0.0836$, $a_4 = 0.0069$.

Typical performance: scalloping loss $< 0.01\,\text{dB}$, peak sidelobe $\approx -90\,\text{dB}$.

**When to use:**

- **Calibration:** Measuring the exact amplitude of a known sinusoidal signal (oscillator testing, ADC gain calibration, audio impedance measurement).
- **Distortion analysis (THD):** Measuring harmonic amplitudes relative to the fundamental in a periodic waveform.
- **Standards compliance testing** where amplitude accuracy is the primary specification.

**When NOT to use:**

- **Frequency resolution applications:** The main lobe width can be 6–10 DFT bins wide. Two sinusoids within this range cannot be distinguished.
- **General-purpose spectral analysis:** The very wide main lobe makes it unsuitable for dense spectra.

**Summary comparison:**

| Window | Amplitude accuracy | Frequency resolution |
|---|---|---|
| Rectangular | Poor (3.9 dB error) | Best |
| Hanning | Moderate (1.4 dB error) | Good |
| Blackman | Good (1.1 dB error) | Moderate |
| Flat-top | Excellent ($< 0.01$ dB) | Poor |

---

### Q9. Explain the concept of the time-bandwidth product and prove a lower bound using the uncertainty principle analogy.

**Answer:**

**Time-bandwidth product** of a window $w[n]$: the product of its effective time duration and effective spectral bandwidth.

**Effective duration** (RMS width in time):

$$T_{rms}^2 = \frac{\sum_n n^2 |w[n]|^2}{\sum_n |w[n]|^2}$$

(relative to the centroid of the window)

**Effective bandwidth** (RMS width in frequency):

$$B_{rms}^2 = \frac{\int_{-\pi}^{\pi} \omega^2 |W(e^{j\omega})|^2\,d\omega}{\int_{-\pi}^{\pi} |W(e^{j\omega})|^2\,d\omega}$$

**Uncertainty principle:** By the Cauchy-Schwarz inequality applied to the DTFT:

$$T_{rms} \cdot B_{rms} \geq \frac{1}{2}$$

**Physical interpretation:** You cannot simultaneously have a perfectly localised window in time (narrow $T_{rms}$) and a perfectly narrow spectral main lobe (small $B_{rms}$). The product is bounded below by $1/2$.

**Optimal window:** The Gaussian window $w[n] = e^{-\alpha n^2}$ achieves the minimum time-bandwidth product (equality in the uncertainty bound). However, Gaussian windows have infinite duration and must be truncated for practical use — which reintroduces sidelobes. The Kaiser window is the closest practical approximation to the prolate spheroidal wave function, which maximises the energy concentration within a given bandwidth (a different but related optimality criterion).

**Practical implications:**

1. For any window of $N$ points, the best achievable frequency resolution is $\sim 2/N$ cycles/sample ($4\pi/N$ rad/sample main lobe width for rectangular).
2. Increasing $N$ (more data) is the only way to genuinely improve frequency resolution — window choice cannot overcome the fundamental limit.
3. Choosing a low-sidelobe window always costs frequency resolution compared to the rectangular window of the same length.

---

## Quick Reference

| Window | Equation | PSL (dB) | ML width (bins) | Best use |
|---|---|---|---|---|
| Rectangular | $1$ | $-13$ | 2 | Coherent sampling |
| Hanning | $0.5(1-\cos(2\pi n/(N-1)))$ | $-31.5$ | 4 | General analysis |
| Hamming | $0.54-0.46\cos(2\pi n/(N-1))$ | $-41$ | 4 | Narrowband detection |
| Blackman | $0.42-0.5\cos+0.08\cos(2\cdot)$ | $-57$ | 6 | High dynamic range |
| Kaiser | $I_0(\beta\sqrt{1-(\ldots)^2})/I_0(\beta)$ | Tunable via $\beta$ | Grows with $\beta$ | Filter design |
| Flat-top | 5-term cosine | $\approx -90$ | 8–10 | Amplitude calibration |

**Kaiser $\beta$ values:**

| $A_s$ (dB) | $\beta$ |
|---|---|
| 21 | 0 (rectangular) |
| 40 | 3.4 |
| 60 | 5.65 |
| 80 | 7.86 |
| 100 | 10.06 |
