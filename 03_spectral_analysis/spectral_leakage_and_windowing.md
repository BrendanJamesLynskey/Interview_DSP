# Spectral Leakage and Windowing: Interview Questions

## Overview

Spectral leakage is one of the most practically significant artefacts in DFT-based signal analysis. Every real measurement involves observing a signal for a finite time, and that truncation has spectral consequences. Understanding leakage, its relationship to window functions, and the engineering trade-offs between resolution and sidelobe suppression is essential for any DSP interview at the intermediate level and above.

---

## Tier 1: Fundamentals

### Q1. What is spectral leakage and why does it occur?

**Answer.**

**Spectral leakage** is the spreading of energy from a frequency component in a DFT result into neighbouring frequency bins, rather than being concentrated at a single bin.

**Why it occurs: finite observation and the rectangular window.**

In practice, we observe $N$ samples of a continuous-time signal $x(t)$ and compute the $N$-point DFT. Mathematically, this is equivalent to multiplying the infinite-duration signal by a **rectangular window**:

$$x_w[n] = x[n] \cdot w[n], \quad w[n] = \begin{cases} 1 & 0 \leq n \leq N-1 \\ 0 & \text{otherwise} \end{cases}$$

Multiplication in the time domain corresponds to **convolution in the frequency domain**:

$$X_w(e^{j\omega}) = X(e^{j\omega}) * W(e^{j\omega})$$

The DTFT of the rectangular window is the **Dirichlet kernel**:

$$W(e^{j\omega}) = e^{-j\omega(N-1)/2} \frac{\sin(\omega N / 2)}{\sin(\omega / 2)}$$

This is not an impulse — it has a central mainlobe of width $\approx 4\pi/N$ and **sidelobes** that decay only as $1/\omega$ (sidelobe level of approximately $-13$ dB relative to the mainlobe peak). When $X(e^{j\omega})$ is convolved with this non-ideal kernel, energy from a strong frequency component spreads (leaks) into adjacent bins.

**Leakage is worst when** a sinusoid's frequency does not land exactly on a DFT bin (i.e., when the signal is not periodic within the observation window).

---

### Q2. Under what condition is there no spectral leakage for a pure sinusoid?

**Answer.**

A sinusoid $x[n] = A\cos(2\pi f_0 n / f_s)$ produces no leakage if and only if its frequency $f_0$ corresponds exactly to a DFT bin frequency:

$$f_0 = \frac{k f_s}{N} \quad \text{for some integer } k \in \{0, 1, \ldots, N-1\}$$

Equivalently, the signal must contain an exact integer number of cycles within the $N$-sample window:

$$N \cdot \frac{f_0}{f_s} \in \mathbb{Z}$$

**Why.** Under this condition, the signal is perfectly periodic with period $N$, so the DFT (which implicitly assumes periodicity) sees no discontinuity at the block boundaries. The DFT of $x[n] = Ae^{j2\pi kn/N}$ is exactly $NA\delta[m-k]$ — a single nonzero bin.

**Consequence.** For arbitrary signal frequencies, leakage is unavoidable with rectangular windowing. The DFT bin frequencies form a discrete grid with spacing $f_s/N$; most physical signals do not land exactly on this grid.

---

### Q3. What is a window function in the context of the DFT? What properties characterise a good window?

**Answer.**

A **window function** $w[n]$, $n = 0, \ldots, N-1$, tapers the signal toward zero at the edges of the observation interval before computing the DFT. This shapes the frequency-domain spreading function to be more favourable than the rectangular window.

**Desirable spectral properties of a window:**

1. **Narrow mainlobe.** A narrow mainlobe gives better frequency resolution — ability to distinguish two nearby frequency components.

2. **Low sidelobes.** Low peak sidelobe level (PSL) reduces leakage of a strong component into adjacent bins where a weaker component might be hidden.

3. **High sidelobe fall-off rate.** Rapid attenuation of sidelobes with distance from the mainlobe further limits long-range leakage.

4. **Low scalloping loss.** When a frequency falls between bins, the DFT output at the nearest bin is attenuated. Lower scalloping loss means this attenuation is smaller.

5. **Coherent power gain (CPG) near unity.** The window's DC gain determines how much the amplitude of a sinusoid is reduced.

**The fundamental conflict.** Properties 1 and 2 are in direct tension: any window that tapers to zero at the edges (smooth window) has a wider mainlobe than the rectangular window. This is a consequence of the time-bandwidth uncertainty principle — you cannot simultaneously achieve narrow mainlobe and low sidelobes. All window design involves trading one against the other.

---

### Q4. What is the mainlobe width of the rectangular window, and how does it define spectral resolution?

**Answer.**

For a rectangular window of length $N$, the DTFT magnitude is:

$$|W(e^{j\omega})| = \left|\frac{\sin(\omega N / 2)}{\sin(\omega / 2)}\right|$$

**Mainlobe width.** The first zero of the numerator occurs at $\omega N/2 = \pi$, i.e., $\omega = 2\pi/N$. The mainlobe extends from $-2\pi/N$ to $+2\pi/N$, giving a **mainlobe width of $4\pi/N$ radians** (or $2/N$ in normalised frequency, or $2f_s/N$ in Hz).

**Resolution definition.** Two sinusoids at frequencies $f_1$ and $f_2$ can be resolved (distinguished) in the DFT if their frequency separation exceeds approximately the mainlobe half-width:

$$|f_1 - f_2| > \frac{f_s}{N} = \frac{1}{T_{\text{obs}}}$$

where $T_{\text{obs}} = N/f_s$ is the observation duration. This is the **Rayleigh resolution criterion**: resolution is determined by the reciprocal of the observation time, not by the sampling rate or FFT length.

**Note.** Zero-padding (increasing FFT size beyond $N$) interpolates the spectrum on a finer grid but does **not** improve resolution. True resolution improvement requires longer observation (more data, not more zeros).

---

### Q5. What is scalloping loss and how does it affect amplitude measurements?

**Answer.**

**Scalloping loss** (also called picket-fence effect) is the reduction in the DFT bin magnitude when a sinusoid's frequency falls midway between two adjacent DFT bins.

**Derivation for rectangular window.** At exact bin centre ($\omega = 2\pi k/N$), the DFT magnitude is $N$ (for unit amplitude). When the frequency lies exactly between bins $k$ and $k+1$ (i.e., at $\omega = 2\pi(k + 0.5)/N$), the magnitude is:

$$|W(e^{j\pi/N})| = \left|\frac{\sin(\pi/2)}{\sin(\pi/(2N))}\right| \approx \frac{1}{\pi/(2N)} = \frac{2N}{\pi}$$

Scalloping loss (in dB):

$$L_{\text{scallop}} = 20\log_{10}\!\left(\frac{N}{2N/\pi}\right) = 20\log_{10}\!\left(\frac{\pi}{2}\right) \approx 3.92 \text{ dB}$$

**Window comparison:**

| Window | Peak sidelobe (dB) | Mainlobe width (bins) | Scalloping loss (dB) |
|---|:-:|:-:|:-:|
| Rectangular | -13 | 2 | 3.92 |
| Hann | -31.5 | 4 | 1.42 |
| Hamming | -41.8 | 4 | 1.75 |
| Blackman | -58.1 | 6 | 1.10 |
| Flat top | -93.0 | 8–10 | ~0.01 |

**Practical impact.** For amplitude measurements (e.g., calibration, harmonic analysis), scalloping loss can cause systematic amplitude errors of up to 4 dB with rectangular windowing. The **flat-top window** is specifically designed to minimise scalloping loss at the cost of a very wide mainlobe (poor frequency resolution).

---

## Tier 2: Intermediate

### Q6. Derive the DTFT of the Hann window and identify its mainlobe and first sidelobe.

**Answer.**

The **Hann window** (often incorrectly called Hanning) is:

$$w[n] = \frac{1}{2}\left(1 - \cos\frac{2\pi n}{N-1}\right) = \frac{1}{2} - \frac{1}{2}\cos\frac{2\pi n}{N-1}, \quad n = 0,\ldots,N-1$$

Using the identity $\cos\theta = (e^{j\theta} + e^{-j\theta})/2$:

$$w[n] = \frac{1}{2}w_R[n] - \frac{1}{4}w_R[n]e^{j2\pi n/(N-1)} - \frac{1}{4}w_R[n]e^{-j2\pi n/(N-1)}$$

where $w_R[n]$ is the rectangular window. The DTFT of the Hann window is:

$$W(\omega) = \frac{1}{2}W_R(\omega) - \frac{1}{4}W_R\!\left(\omega - \frac{2\pi}{N-1}\right) - \frac{1}{4}W_R\!\left(\omega + \frac{2\pi}{N-1}\right)$$

This is a superposition of three shifted rectangular window DTFTs.

**Mainlobe width.** The Hann window mainlobe is approximately **4 bins wide** (twice the rectangular window). The three shifted Dirichlet kernels partially cancel the inner sidelobes.

**First sidelobe level.** Approximately $-31.5$ dB (vs. $-13$ dB for rectangular). The $1/\omega^3$ sidelobe roll-off rate (vs. $1/\omega$ for rectangular) results from the window having continuous first derivatives at the endpoints ($w[0] = w[N-1] = 0$, but $w'[0] = w'[N-1] = 0$ approximately for large $N$).

**Physical interpretation.** The cosine term in the Hann window generates two frequency-shifted copies of the rectangular window spectrum, positioned to cancel the first sidelobes of the central term.

---

### Q7. Explain the trade-off between mainlobe width and sidelobe level. Why is it fundamental (not just a design limitation)?

**Answer.**

The trade-off is a consequence of the **time-bandwidth uncertainty principle** for finite-length sequences.

**Formal statement.** Let $w[n]$, $n = 0,\ldots,N-1$, be a window with unit energy. Define:
- $B_{\text{main}}$: mainlobe width (bandwidth of the central lobe)
- $A_{\text{side}}$: total sidelobe energy

Then there is a lower bound of the form:

$$B_{\text{main}} \cdot \|w\|_{\text{max}} \geq C$$

for some constant $C > 0$. More generally, reducing sidelobes requires the window to taper more smoothly to zero, which necessarily widens the mainlobe.

**Why the trade-off is fundamental.** A window with very low sidelobes must be very smooth (many vanishing derivatives at the edges). Smooth functions have slowly decaying Fourier transforms but with small coefficients outside the mainlobe. Abrupt windows (rectangular) have narrow mainlobes but large sidelobes. This is directly analogous to the Heisenberg uncertainty principle in quantum mechanics.

**The prolate spheroidal wave functions (DPSS / Slepian windows)** are the theoretically optimal solution: they maximise the fraction of window energy concentrated within a specified bandwidth $[-W, W]$. For a given mainlobe width, DPSS windows have the minimum possible sidelobe energy. They are used in Thomson's multitaper spectral estimation.

**Practical design curve.** As a rough rule, every 6 dB reduction in peak sidelobe level costs approximately 1 additional DFT bin of mainlobe width.

---

### Q8. For what applications would you choose each of the following windows? Rectangular, Hann, Hamming, Blackman, flat-top.

**Answer.**

**Rectangular window.**
- Best frequency resolution (narrowest mainlobe).
- Use when: transient detection, when signal is exactly periodic within the window, burst signal analysis where edge effects are acceptable, and when the signal contains only one frequency component.
- Avoid when: measuring amplitude accurately, or when a strong nearby component would mask a weaker one via leakage.

**Hann window.**
- Good general-purpose window: $-31.5$ dB sidelobes, 4-bin mainlobe.
- Use when: continuous spectral analysis, audio spectrum analysis, vibration monitoring, general-purpose FFT displays.
- Good balance between resolution and leakage rejection.
- The most commonly used non-rectangular window in practice.

**Hamming window.**
- Optimised to minimise the first sidelobe ($-41.8$ dB), but sidelobes do not fall off as rapidly as Hann (plateau around $-41.8$ dB).
- Use when: the most critical interference comes from frequency components just outside the mainlobe.
- Common in speech processing and FIR filter design.

**Blackman window.**
- Wider mainlobe (6 bins), $-58$ dB sidelobes.
- Use when: measuring weak components near strong ones that are farther away; audio analysis requiring high dynamic range.
- Poorer frequency resolution than Hann; better for amplitude dynamic range.

**Flat-top window.**
- Extremely low scalloping loss (~0.01 dB), very wide mainlobe (8–10 bins).
- Use when: accurate amplitude calibration is the priority and frequency resolution is not critical (e.g., calibrating ADCs, instrument calibration, sinusoidal amplitude measurements).
- Inappropriate for resolving closely spaced frequency components.

---

### Q9. What is coherent gain, and how do you correct for it when computing an amplitude spectrum from a windowed FFT?

**Answer.**

**Coherent gain (CG)** of a window is the sum of its samples, normalised by window length:

$$\text{CG} = \frac{1}{N}\sum_{n=0}^{N-1} w[n]$$

For the rectangular window, $\text{CG} = 1$. For the Hann window, $\text{CG} = 0.5$.

**Why it matters.** When a sinusoid $x[n] = A\cos(2\pi f_0 n / f_s)$ is multiplied by a window $w[n]$ and then DFT'd, the bin corresponding to $f_0$ has magnitude:

$$|X_w[k_0]| \approx \frac{A \cdot N \cdot \text{CG}}{2}$$

(the factor of 2 arises because a cosine has two one-sided spectral peaks). To recover the true amplitude $A$ from the windowed DFT:

$$A = \frac{2 |X_w[k_0]|}{N \cdot \text{CG}}$$

**Power correction.** For power spectral density estimation, the appropriate normalisation uses the **power coherent gain** (also called the window power, or normalisation factor for power):

$$\text{PCG} = \frac{1}{N}\sum_{n=0}^{N-1} w^2[n]$$

A PSD estimate requires dividing by $N \cdot \text{PCG} \cdot f_s^{-1}$ to obtain correct units of V²/Hz.

**Common window correction factors:**

| Window | CG | PCG | Amplitude correction |
|---|:-:|:-:|:-:|
| Rectangular | 1.000 | 1.000 | $2/N$ |
| Hann | 0.500 | 0.375 | $4/N$ |
| Hamming | 0.540 | 0.397 | $3.70/N$ |
| Blackman | 0.420 | 0.289 | $4.76/N$ |

---

## Tier 3: Advanced

### Q10. Derive the mainlobe width of a general cosine window of the form $w[n] = \sum_{k=0}^{K} a_k \cos(2\pi kn/N)$.

**Answer.**

A general cosine window with $K+1$ terms:

$$w[n] = \sum_{k=0}^{K} a_k \cos\frac{2\pi kn}{N}, \quad n = 0,\ldots,N-1$$

The DTFT is:

$$W(\omega) = a_0 W_R(\omega) + \frac{1}{2}\sum_{k=1}^{K} a_k \left[W_R\!\left(\omega - \frac{2\pi k}{N}\right) + W_R\!\left(\omega + \frac{2\pi k}{N}\right)\right]$$

where $W_R(\omega)$ is the Dirichlet kernel for a rectangular window of length $N$.

**Mainlobe width determination.** The mainlobe of $W_R(\omega)$ extends to $\pm 2\pi/N$. The shifted copies in the cosine window expression are centred at $\pm 2\pi k/N$. For the window to have its first null at $2\pi m/N$ (mainlobe of $2m$ bins width), the coefficient vectors $\{a_k\}$ must be chosen so the shifted Dirichlet kernels constructively reinforce within $|\omega| < 2\pi m/N$ and cancel the sidelobes outside.

**Result.** A $(K+1)$-term cosine window has mainlobe width of approximately $2(K+1)$ bins. Specifically:

- $K=0$ (rectangular): mainlobe width $= 2$ bins
- $K=1$ (Hann/Hamming): mainlobe width $= 4$ bins
- $K=2$ (Blackman): mainlobe width $= 6$ bins
- $K=3$ (Blackman-Harris 4-term): mainlobe width $= 8$ bins

**Constraints on $a_k$.** For the window to satisfy $w[0] = w[N-1] = 0$ (zero endpoints), the coefficients must satisfy $\sum_k a_k = 0$. For zero first derivative at endpoints: the Hamming window $a_0 = 0.54$, $a_1 = 0.46$ is designed so the sidelobes of the two Dirichlet kernels partially cancel. The Hann window $a_0 = 0.5$, $a_1 = 0.5$ achieves the $1/\omega^3$ sidelobe roll-off at the cost of slightly higher distant sidelobes compared to Hamming.

---

### Q11. What are Slepian (DPSS) windows and what optimality property do they satisfy?

**Answer.**

**DPSS (Discrete Prolate Spheroidal Sequences)**, introduced by Slepian (1978), are sequences $\{w_k[n]\}$ of length $N$ that are **energy-maximally concentrated** in the frequency band $[-W, W]$:

$$\lambda_k = \frac{\int_{-W}^{W} |W_k(f)|^2 df}{\int_{-1/2}^{1/2} |W_k(f)|^2 df}$$

The DPSS windows are the eigenvectors of the matrix $\mathbf{A}$ with entries:

$$A_{mn} = \frac{\sin(2\pi W(m-n))}{\pi(m-n)}, \quad m,n = 0,\ldots,N-1$$

ordered by decreasing eigenvalue $\lambda_k$.

**Optimality.** For a given half-bandwidth $W$ and window length $N$, the zeroth-order DPSS window $w_0[n]$ concentrates the maximum possible fraction $\lambda_0$ of its energy within $[-W, W]$. This means it has the minimum possible sidelobe energy outside the band $[-W, W]$ for its mainlobe width — the theoretically optimal leakage-rejection window.

**Parameter $NW$.** The time-halfbandwidth product $NW$ controls the trade-off. For $NW = 4$, the mainlobe has 8 bins width and $\lambda_0 \approx 1 - 10^{-12}$ (essentially all energy in the mainlobe). Larger $NW$ means lower sidelobes but wider mainlobe.

**Application: multitaper spectral estimation.** In Thomson's multitaper method, the first $K = 2NW - 1$ DPSS windows are used as $K$ orthogonal tapers. The $K$ resulting periodograms are averaged, providing:
- Nearly uncorrelated spectral estimates (the DPSS tapers are orthogonal in both time and frequency)
- Variance reduction by a factor of $K$
- Controlled sidelobe leakage (bounded by $1 - \lambda_k$)

This is the highest-quality spectral estimation method for stationary signals with high dynamic range requirements.

---

### Q12. How does the choice of window affect the ability to detect a weak sinusoid near a strong one? Quantify with an example.

**Answer.**

**Setup.** Consider two sinusoids:
- Strong: $A_1 = 1$, frequency $f_1 = 1000$ Hz
- Weak: $A_2 = 0.001$, frequency $f_2 = 1010$ Hz

Sampling rate $f_s = 8000$ Hz, FFT length $N = 1024$. Bin spacing: $\Delta f = 8000/1024 \approx 7.8$ Hz. Frequency separation: $\Delta f_{\text{signal}} = 10$ Hz $\approx 1.28$ bins.

**The problem.** The strong sinusoid's sidelobe at bin offset $+1.28$ must be below the weak sinusoid's peak.

Dynamic range requirement: $20\log_{10}(A_1/A_2) = 60$ dB.

**Window comparison for detection:**

With **rectangular window**: Peak sidelobe at $-13$ dB. At 1.28 bins offset, sidelobe is approximately $-13 - 20\log_{10}(1.28) \approx -15$ dB. The strong component's leakage ($-15$ dB below its peak = $-15$ dBFS) utterly masks the weak component at $-60$ dBFS. **Detection fails.**

With **Hann window**: Sidelobes fall as $1/f^3$. At 1.28 bins offset (just outside the mainlobe, which ends at $\approx 2$ bins), the sidelobe is approximately $-32$ dB. Still $-32$ dBFS $>$ $-60$ dBFS. **Detection fails at this separation.**

To resolve these components with a Hann window, the frequency separation must exceed the mainlobe half-width of 2 bins = $2 \times 7.8 = 15.6$ Hz.

**Longer FFT solution.** If $N = 8192$: $\Delta f = 0.977$ Hz, separation $= 10.2$ bins. Now with Hann window, at 10 bins offset sidelobe $\approx -31.5 - 60\log_{10}(10/2) \approx -31.5 - 42 = -73.5$ dB. Below the $-60$ dB requirement. **Detection succeeds.**

**Key lesson.** Sidelobe attenuation depends on both the window choice and the normalised frequency separation in bins. Increasing $N$ (longer observation) is the only way to improve true resolution; windowing controls the leakage for a given separation.

---

## Quick Reference: Window Comparison Table

| Window | PSL (dB) | Mainlobe (bins) | Roll-off (dB/oct) | Scalloping (dB) | CG |
|---|:-:|:-:|:-:|:-:|:-:|
| Rectangular | -13 | 2 | 6 | 3.92 | 1.000 |
| Bartlett (triangular) | -27 | 4 | 12 | 1.82 | 0.500 |
| Hann | -31.5 | 4 | 18 | 1.42 | 0.500 |
| Hamming | -41.8 | 4 | 6 | 1.75 | 0.540 |
| Blackman | -58.1 | 6 | 18 | 1.10 | 0.420 |
| Blackman-Harris (4-term) | -92 | 8 | 6 | 0.83 | 0.358 |
| Flat top | -93 | 10 | 6 | ~0.01 | 0.216 |
| DPSS ($NW=4$) | -93 | 8 | — | 0.56 | varies |

PSL = peak sidelobe level; CG = coherent gain; Roll-off = sidelobe decay rate beyond first sidelobe.
