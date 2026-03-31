# Power Spectral Density: Interview Questions

## Overview

Power spectral density (PSD) estimation is the foundation of spectral analysis in communications, radar, audio, and biomedical signal processing. Interviews test understanding of the definition, estimation methods, and the fundamental bias-variance trade-off that no estimator can escape. This file covers periodogram and non-parametric methods; parametric methods (AR, MUSIC) are in a separate file.

---

## Tier 1: Fundamentals

### Q1. Define the power spectral density. What does it represent physically?

**Answer.**

For a wide-sense stationary (WSS) random process $x[n]$ with autocorrelation sequence:

$$R_x[k] = \mathbb{E}\{x[n+k]\, x^*[n]\}$$

the **power spectral density** is defined as the discrete-time Fourier transform of the autocorrelation sequence (Wiener-Khinchin theorem):

$$S_x(f) = \sum_{k=-\infty}^{\infty} R_x[k] \, e^{-j2\pi f k T_s}$$

where $T_s = 1/f_s$ is the sampling period. The frequency argument $f$ ranges over $[-f_s/2, f_s/2]$.

**Physical interpretation.** $S_x(f)$ describes how the total power of the process is distributed across frequency. Specifically:

$$\int_{-f_s/2}^{f_s/2} S_x(f) \, df = R_x[0] = \mathbb{E}\{|x[n]|^2\} = \text{total average power}$$

The PSD has units of **power per unit frequency** (e.g., V²/Hz if $x$ is in volts).

**Why the autocorrelation, not the signal itself?** The DTFT of a single realisation of a stationary random process does not converge in the traditional sense (the process extends infinitely and is non-deterministic). The autocorrelation function, which is a deterministic function via the expectation, provides the well-defined spectral characterisation.

---

### Q2. What is the periodogram? How is it computed, and what are its statistical properties?

**Answer.**

**Definition.** Given $N$ samples $\{x[n]\}_{n=0}^{N-1}$ of a stationary process, the **periodogram** is:

$$\hat{S}_x(f) = \frac{1}{N f_s} \left| \sum_{n=0}^{N-1} x[n] e^{-j2\pi f n T_s} \right|^2 = \frac{|X_N(f)|^2}{N f_s}$$

where $X_N(f)$ is the DTFT of the windowed (rectangular) data segment.

**Computation.** In practice, evaluated at DFT frequencies $f_k = kf_s/N$:

$$\hat{S}_x[k] = \frac{|X[k]|^2}{N f_s}, \quad k = 0, 1, \ldots, N-1$$

where $X[k]$ is the $N$-point DFT of $x[n]$.

**Statistical properties.**

*Asymptotic bias:* The periodogram is **asymptotically unbiased** — as $N \to \infty$, $\mathbb{E}\{\hat{S}_x(f)\} \to S_x(f)$.

*Variance:* The variance of the periodogram is approximately:

$$\text{Var}\{\hat{S}_x(f)\} \approx S_x^2(f)$$

independent of $N$. The periodogram is an **inconsistent estimator** — increasing $N$ does not reduce variance. The normalised standard deviation is $\approx 100\%$ of the mean at every frequency.

**Why inconsistent?** Each additional sample adds one more equation to the estimation problem but also adds one more unknown (the DFT value at a new frequency). The degrees of freedom do not grow faster than the data.

**Consequence.** A raw periodogram of a long data record looks jagged and noisy, with variance that does not decrease with $N$. Smoothing (Welch's method, Bartlett's method) is necessary for reliable PSD estimates.

---

### Q3. What is the resolution bandwidth of a PSD estimate?

**Answer.**

**Resolution bandwidth (RBW)** is the minimum frequency separation between two spectral components that can be distinguished in a PSD estimate. It quantifies the frequency resolution of the estimator.

**For the periodogram** of $N$ samples at sampling rate $f_s$:

$$\text{RBW} = \frac{f_s}{N} = \frac{1}{T_{\text{obs}}}$$

This is the bin spacing, which sets the fundamental frequency resolution. Two sinusoids must be separated by at least one bin ($f_s/N$ Hz) to produce distinct peaks in the periodogram.

**Effect of windowing.** A non-rectangular window widens the effective resolution bandwidth. For a window with mainlobe width of $m$ bins:

$$\text{RBW}_{\text{effective}} = m \cdot \frac{f_s}{N}$$

- Rectangular: $\text{RBW} = f_s/N$
- Hann: $\text{RBW} = 2f_s/N$
- Blackman: $\text{RBW} = 3f_s/N$

**For Welch's method** using $K$ segments of length $L$ (with $50\%$ overlap, total data length $\approx N$):

$$\text{RBW}_{\text{Welch}} = \frac{f_s}{L} \approx \frac{2f_s}{N} \cdot K$$

Welch's method trades resolution for variance reduction: using $K$ segments reduces variance by $\approx K$ but coarsens resolution by $K$.

---

## Tier 2: Intermediate

### Q4. Describe Bartlett's method. How does averaging periodograms reduce variance?

**Answer.**

**Bartlett's method.** Divide the $N$-sample data record into $K$ non-overlapping segments of length $L = N/K$. Compute the periodogram of each segment, then average:

$$\hat{S}_{\text{Bartlett}}(f) = \frac{1}{K} \sum_{i=1}^{K} \hat{S}_x^{(i)}(f)$$

**Variance reduction.** If the $K$ periodograms are approximately independent (valid when segment length $L$ is much larger than the autocorrelation length of $x[n]$), then:

$$\text{Var}\{\hat{S}_{\text{Bartlett}}(f)\} \approx \frac{1}{K} S_x^2(f) = \frac{1}{K} \text{Var}\{\hat{S}_{\text{periodogram}}(f)\}$$

The standard deviation is reduced by $\sqrt{K}$: averaging $K$ independent estimates reduces variance by factor $K$.

**Bias-variance trade-off.** Each segment has length $L = N/K$. Shorter segments mean:
- **Reduced variance**: more segments to average
- **Increased bias**: coarser frequency resolution ($f_s/L = Kf_s/N$ bin spacing)

**Chi-squared distribution.** The periodogram at any frequency approximately follows a scaled chi-squared distribution with 2 degrees of freedom. Bartlett's average has $2K$ degrees of freedom, enabling exact confidence interval calculations:

$$P\!\left(\frac{2K\hat{S}(f)}{\chi^2_{2K,1-\alpha/2}} \leq S(f) \leq \frac{2K\hat{S}(f)}{\chi^2_{2K,\alpha/2}}\right) = 1 - \alpha$$

---

### Q5. Describe Welch's method. Why is overlapping used, and what overlap fraction is optimal?

**Answer.**

**Welch's method** extends Bartlett's method by:
1. Dividing data into **overlapping** segments of length $L$
2. Applying a **non-rectangular window** $w[n]$ to each segment before computing the periodogram
3. Averaging the windowed periodograms

For the $i$-th segment starting at sample $iD$ (hop size $D$):

$$\hat{S}_{\text{Welch}}(f) = \frac{1}{K U} \sum_{i=0}^{K-1} \left| \sum_{n=0}^{L-1} x[n + iD] w[n] e^{-j2\pi fnT_s} \right|^2$$

where $U = \frac{1}{L}\sum_{n=0}^{L-1} w^2[n]$ is the window normalisation factor (power coherent gain).

**Why overlap?** Windowing attenuates data near segment edges. A sample near the edge of segment $i$ contributes little to that segment's estimate. With 50% overlap, that same sample falls near the **centre** of the adjacent segment $i+1$, where the window is large. Overlapping ensures all samples receive significant weight in at least one segment.

**Optimal overlap fraction.** For most windows, the optimal overlap that maximises the number of independent segments per unit data length is:
- **Hann window**: 50% overlap (standard choice)
- **Hamming window**: 50% overlap
- **Blackman window**: 66% overlap

With 50% overlap and Hann windowing, the number of segments for $N$ samples is approximately $K \approx 2N/L - 1$. Compared to Bartlett ($K = N/L$ segments, no overlap), Welch at 50% overlap gives roughly **twice as many segments** (hence lower variance) for the same data length and segment length, because the overlapping segments are not independent but are more numerous.

**Effective degrees of freedom** for Welch's estimate with overlap fraction $\beta$:

$$d.f. \approx \frac{2K_{\text{eff}}}{1 + 2\sum_{k=1}^{K-1}(1 - k/K)\rho_k^2}$$

where $\rho_k$ is the correlation between periodograms of segments $k$ hops apart — depends on the window shape and overlap.

---

### Q6. Derive the bias of the periodogram as an estimator of $S_x(f)$.

**Answer.**

The periodogram can be written as:

$$\hat{S}_x(f) = \frac{1}{N f_s} \left| \sum_{n=0}^{N-1} x[n] e^{-j2\pi fnT_s} \right|^2$$

**Expected value.** Taking the expectation:

$$\mathbb{E}\{\hat{S}_x(f)\} = \frac{1}{Nf_s} \sum_{n=0}^{N-1}\sum_{m=0}^{N-1} R_x[n-m] e^{-j2\pi f(n-m)T_s}$$

Let $k = n - m$:

$$\mathbb{E}\{\hat{S}_x(f)\} = \frac{1}{f_s} \sum_{k=-(N-1)}^{N-1} \left(1 - \frac{|k|}{N}\right) R_x[k] e^{-j2\pi fkT_s}$$

The factor $(1 - |k|/N)$ is the **Bartlett window** $w_B[k]$ applied to the autocorrelation sequence. So:

$$\mathbb{E}\{\hat{S}_x(f)\} = S_x(f) * W_B(f) \neq S_x(f)$$

where $W_B(f)$ is the DTFT of the Bartlett window.

**Bias interpretation.** The periodogram is a *smoothed* version of the true PSD, where the smoothing kernel $W_B(f)$ has width $\approx 1/N$ in frequency. The bias is:

$$\text{Bias} = \mathbb{E}\{\hat{S}_x(f)\} - S_x(f) = S_x(f) * W_B(f) - S_x(f)$$

This bias vanishes as $N \to \infty$ (Bartlett window $\to$ Dirac delta), making the periodogram asymptotically unbiased. For finite $N$, the bias is significant when $S_x(f)$ varies rapidly over a frequency range of $1/N$.

---

### Q7. What is cross-spectral density and how is it estimated? What does it reveal that PSD does not?

**Answer.**

**Definition.** The **cross-spectral density** (CSD) between two jointly WSS processes $x[n]$ and $y[n]$ is:

$$S_{xy}(f) = \sum_{k=-\infty}^{\infty} R_{xy}[k] \, e^{-j2\pi fkT_s}$$

where $R_{xy}[k] = \mathbb{E}\{x[n+k] y^*[n]\}$ is the cross-correlation.

**Estimation (Welch cross-spectrum).** For each segment $i$:

$$\hat{S}_{xy}^{(i)}(f) = \frac{1}{Lf_s} X_i(f) Y_i^*(f)$$

Average over $K$ segments:

$$\hat{S}_{xy}(f) = \frac{1}{K} \sum_{i=1}^{K} \hat{S}_{xy}^{(i)}(f)$$

**What CSD reveals beyond PSD:**

1. **Coherence.** The magnitude-squared coherence (MSC):
$$\gamma_{xy}^2(f) = \frac{|S_{xy}(f)|^2}{S_x(f) S_y(f)}, \quad 0 \leq \gamma_{xy}^2(f) \leq 1$$
Coherence measures the degree of linear dependence between $x$ and $y$ at each frequency. $\gamma_{xy}^2 = 1$ means perfectly linear relationship; $\gamma_{xy}^2 = 0$ means $x$ and $y$ are uncorrelated at that frequency.

2. **Phase spectrum.** $\angle S_{xy}(f)$ gives the phase lead of $y$ relative to $x$ at each frequency, revealing propagation delays in acoustic or seismic arrays.

3. **Frequency response estimation.** For a linear system $y = H * x + \text{noise}$:
$$\hat{H}(f) = \frac{\hat{S}_{xy}(f)}{\hat{S}_x(f)}$$
This is the $H_1$ estimator (minimises noise at output). The $H_2$ estimator $\hat{H}(f) = \hat{S}_y(f)/\hat{S}_{yx}(f)$ minimises noise at input.

---

## Tier 3: Advanced

### Q8. Explain the bias-variance trade-off in PSD estimation and express it quantitatively as a function of segment length and overlap.

**Answer.**

**The fundamental constraint.** PSD estimation from $N$ samples faces an inescapable trade-off: any linear smoothing operation that reduces variance necessarily introduces bias (spectral smoothing reduces resolution).

**Quantification for Welch's method.**

Let $N$ = total samples, $L$ = segment length, $D$ = hop size, $K$ = number of segments:

For non-overlapping Bartlett: $K = N/L$, $D = L$.

**Bias.** The expected value of Welch's estimate at frequency $f$ is approximately:

$$\mathbb{E}\{\hat{S}_W(f)\} \approx \int_{-f_s/2}^{f_s/2} S_x(\xi) \, |W(f-\xi)|^2 d\xi$$

where $W(f)$ is the normalised window spectrum. Bias grows when $S_x(f)$ has features finer than the window mainlobe width $B_W = f_s/L$ (times the window-dependent factor $m$).

**Mean squared bias:**

$$\text{Bias}^2 \approx \left[\frac{B_W^2}{24} S_x''(f)\right]^2$$

(under a smooth $S_x$ assumption, where $S_x''$ denotes the second derivative).

**Variance.** For Welch's method with $K$ effectively independent segments:

$$\text{Var}\{\hat{S}_W(f)\} \approx \frac{S_x^2(f)}{K_{\text{eff}}}$$

The effective number of independent estimates $K_{\text{eff}}$ accounts for segment correlation from overlapping:

$$K_{\text{eff}} = \frac{K}{\displaystyle 1 + 2\sum_{k=1}^{K-1}\left(1-\frac{k}{K}\right) \left[\frac{\sum_n w[n]w[n+kD]}{\sum_n w^2[n]}\right]^2}$$

For 50% overlap with Hann window, $K_{\text{eff}} \approx 0.9K$ (the segments are not fully independent, costing about 11% efficiency).

**Mean squared error decomposition:**

$$\text{MSE} = \text{Var} + \text{Bias}^2 \approx \frac{S_x^2(f)}{K_{\text{eff}}} + \left(\frac{B_W}{1} \text{ correction}\right)^2$$

**Optimal segment length** minimises MSE. For a fixed $N$, the optimal $L^*$ satisfies $d(\text{MSE})/dL = 0$, yielding $L^* \propto N^{4/5}$ (under the smooth-$S_x$ assumption), giving MSE $\propto N^{-4/5}$.

---

### Q9. Derive the distribution of the periodogram at a single frequency bin and use it to construct a confidence interval.

**Answer.**

**Distribution of the periodogram.** Let $x[n]$ be a zero-mean Gaussian stationary process. At DFT frequency $f_k = kf_s/N$ (not at $f = 0$ or $f = f_s/2$), the DFT coefficient:

$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi kn/N}$$

is the sum of $N$ i.i.d. (approximately, for large $N$) complex Gaussian random variables. By the central limit theorem, $X[k]$ is approximately complex Gaussian: $X[k] \sim \mathcal{CN}(0, N f_s S_x(f_k))$.

Writing $X[k] = X_R + jX_I$, both $X_R$ and $X_I$ are real Gaussian with variance $\sigma^2 = Nf_s S_x(f_k)/2$.

**Chi-squared distribution.** The periodogram:

$$\hat{S}_x(f_k) = \frac{|X[k]|^2}{Nf_s} = \frac{X_R^2 + X_I^2}{Nf_s}$$

$$= \frac{\sigma^2}{Nf_s}\left[\left(\frac{X_R}{\sigma}\right)^2 + \left(\frac{X_I}{\sigma}\right)^2\right] = \frac{S_x(f_k)}{2} \chi^2_2$$

where $\chi^2_2$ is a chi-squared random variable with 2 degrees of freedom.

**Key result:**

$$\frac{2\hat{S}_x(f_k)}{S_x(f_k)} \sim \chi^2_2$$

**Confidence interval.** From the $\chi^2_2$ distribution (which is the exponential distribution), let $\chi^2_{2,p}$ be the $p$-th percentile. A $(1-\alpha)$ confidence interval for $S_x(f_k)$ is:

$$\left[\frac{2\hat{S}_x(f_k)}{\chi^2_{2,1-\alpha/2}}, \quad \frac{2\hat{S}_x(f_k)}{\chi^2_{2,\alpha/2}}\right]$$

For a 95% confidence interval: $\chi^2_{2, 0.025} = 0.0506$, $\chi^2_{2, 0.975} = 7.378$:

$$\left[0.271\hat{S}_x, \quad 39.5\hat{S}_x\right]$$

This interval spans nearly 150:1 (22 dB) — confirming the periodogram's poor precision.

**With Welch averaging ($K$ segments, $2K$ dof):**

$$\frac{2K\hat{S}_W(f_k)}{S_x(f_k)} \sim \chi^2_{2K}$$

For $K = 16$, the 95% CI narrows dramatically: $[\,0.62\hat{S}_W,\, 1.61\hat{S}_W]$ — approximately $\pm 2.5$ dB. This illustrates concretely why averaging is necessary.

---

### Q10. Compare and contrast the resolution and variance properties of the periodogram, Bartlett, and Welch methods. For a given data length $N$, how should one choose between them?

**Answer.**

**Comparison table:**

| Method | Resolution | Variance | Notes |
|---|---|---|---|
| Periodogram | $f_s/N$ (best) | $S_x^2(f)$ (worst) | No variance reduction |
| Bartlett ($K$ segs) | $Kf_s/N$ (degraded) | $S_x^2(f)/K$ | Non-overlapping, rectangular window |
| Welch (50% overlap, Hann) | $\sim 2Kf_s/N$ | $S_x^2(f)/(0.9K)$ | Overlapping; window widens resolution further |

**Design rules for choosing between methods, given fixed $N$:**

**Use the raw periodogram when:**
- The signal is deterministic (single-shot measurement, no ensemble available).
- You need maximum frequency resolution and can accept high variance.
- The signal is known to have only narrowband features far apart relative to $f_s/N$.
- Followed by post-processing (e.g., MUSIC, ESPRIT) that handles the variance differently.

**Use Bartlett when:**
- You need a simple, explainable method with exact chi-squared statistics.
- The window sidelobe level of the rectangular window is acceptable (no nearby strong interferers).
- Segments can be verified to be approximately stationary.

**Use Welch (with non-rectangular window) when:**
- The spectral dynamic range is high (strong components near weak ones) — windowing reduces leakage.
- 50% overlap gives more segments for the same data length.
- This is the **default recommendation** for most practical applications.

**Practical selection of segment length $L$:**
- The resolution $\Delta f \approx f_s/L$ should be finer than the narrowest spectral feature you need to resolve.
- Given the required $\Delta f$, choose $L = f_s/\Delta f$, round up to the nearest power of 2.
- Number of segments $K \approx 2N/L$ (50% overlap). If $K < 10$, variance will be poor (relative standard deviation $> 30\%$). Consider acquiring more data or relaxing resolution.

**Rule of thumb.** For reliable spectral estimates, aim for at least $K = 16$ segments, giving approximately $\pm 2$ dB 95% confidence bounds.

---

## Quick Reference: PSD Estimation Summary

| Estimator | Resolution | Variance | Degrees of Freedom | Bias |
|---|:-:|:-:|:-:|:-:|
| Periodogram | $f_s/N$ | $S_x^2$ | 2 | Asymptotically 0 |
| Bartlett | $f_s/L = Kf_s/N$ | $S_x^2/K$ | $2K$ | $\propto (f_s/L)^2 S_x''$ |
| Welch (50% ov.) | $\sim 2f_s/L$ | $\sim S_x^2/(0.9K)$ | $\sim 1.8K$ | $\propto (f_s/L)^2 S_x''$ |
| Multitaper | $2NW f_s/N$ | $S_x^2/(2NW)$ | $\sim 4NW-2$ | Controlled by $\lambda_k$ |

Key formulas:
- Wiener-Khinchin: $S_x(f) = \mathcal{F}\{R_x[k]\}$
- Total power: $\int_{-f_s/2}^{f_s/2} S_x(f)\, df = R_x[0]$
- Periodogram distribution: $2\hat{S}/S \sim \chi^2_2$
- Coherence: $\gamma_{xy}^2(f) = |S_{xy}(f)|^2 / (S_x(f)S_y(f))$
