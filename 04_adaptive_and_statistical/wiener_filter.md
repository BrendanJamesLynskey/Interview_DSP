# Wiener Filter: Interview Questions

## Overview

The Wiener filter is the theoretical optimum for linear minimum mean-square error (MMSE) estimation of a signal from noisy or corrupted observations. It provides the benchmark against which all adaptive algorithms are evaluated. Understanding the Wiener-Hopf equation, its solution, and its limitations is foundational for DSP interviews at the intermediate level and above.

---

## Tier 1: Fundamentals

### Q1. State the Wiener filter problem. What assumptions are required?

**Answer.**

**Problem statement.** Given an observable signal $x[n]$ (input/reference), find a linear filter $h[n]$ such that the filter output $y[n] = h[n] * x[n]$ is the best estimate of a desired signal $d[n]$, in the minimum mean-square error (MMSE) sense:

$$\min_{\{h[k]\}} \mathbb{E}\left\{|d[n] - y[n]|^2\right\} = \min_{\{h[k]\}} \mathbb{E}\left\{\left|d[n] - \sum_k h[k] x[n-k]\right|^2\right\}$$

**Required assumptions:**
1. **Wide-sense stationarity (WSS).** Both $x[n]$ and $d[n]$ are WSS jointly, meaning $R_x[k] = \mathbb{E}\{x[n+k]x^*[n]\}$ and $R_{dx}[k] = \mathbb{E}\{d[n+k]x^*[n]\}$ are functions of lag $k$ only, not time $n$.

2. **Known second-order statistics.** $R_x[k]$ (autocorrelation of input) and $R_{dx}[k]$ (cross-correlation between desired signal and input) are known.

3. **Linearity.** The optimal estimator is restricted to the class of linear (convolution) filters. If $d[n]$ and $x[n]$ are jointly Gaussian, the MMSE estimator within all (possibly nonlinear) estimators is also linear, so no restriction is imposed.

**Common applications:**
- Signal denoising: $x[n] = s[n] + v[n]$ (signal plus noise), $d[n] = s[n]$
- Channel equalisation: $x[n]$ is received signal, $d[n]$ is transmitted symbol
- System identification: $d[n]$ is output of unknown system, $x[n]$ is input
- Prediction: $d[n] = x[n+\Delta]$ (predict $\Delta$ steps ahead)

---

### Q2. Derive the Wiener-Hopf equation.

**Answer.**

**Orthogonality principle.** The MMSE estimate $y[n] = \sum_k h[k]x[n-k]$ has the property that the estimation error $e[n] = d[n] - y[n]$ is **orthogonal to the input data space**:

$$\mathbb{E}\{e[n] \, x^*[n-\ell]\} = 0 \quad \text{for all } \ell \text{ in the filter support}$$

**Derivation for a causal FIR filter of length $N$.** The error:

$$e[n] = d[n] - \sum_{k=0}^{N-1} h[k] x[n-k]$$

Orthogonality condition for $\ell = 0, 1, \ldots, N-1$:

$$\mathbb{E}\left\{\left(d[n] - \sum_{k=0}^{N-1} h[k] x[n-k]\right) x^*[n-\ell]\right\} = 0$$

$$\mathbb{E}\{d[n]x^*[n-\ell]\} = \sum_{k=0}^{N-1} h[k] \mathbb{E}\{x[n-k]x^*[n-\ell]\}$$

$$R_{dx}[\ell] = \sum_{k=0}^{N-1} h[k] R_x[\ell - k], \quad \ell = 0, 1, \ldots, N-1$$

**Matrix form (Wiener-Hopf equation for FIR case):**

$$\mathbf{R}\,\mathbf{h}_o = \mathbf{p}$$

where:
$$\mathbf{R} = \begin{bmatrix} R_x[0] & R_x^*[1] & \cdots & R_x^*[N-1] \\ R_x[1] & R_x[0] & \cdots & R_x^*[N-2] \\ \vdots & & \ddots & \vdots \\ R_x[N-1] & \cdots & R_x[1] & R_x[0] \end{bmatrix}$$

is the $N \times N$ Toeplitz (Hermitian) autocorrelation matrix of $x[n]$, and:

$$\mathbf{p} = [R_{dx}[0],\ R_{dx}[1],\ \ldots,\ R_{dx}[N-1]]^T$$

is the cross-correlation vector.

**Solution:**

$$\mathbf{h}_o = \mathbf{R}^{-1}\mathbf{p}$$

This is the **Wiener filter** (for the FIR case). Since $\mathbf{R}$ is Hermitian positive definite, the inverse is guaranteed to exist.

---

### Q3. What is the minimum MSE achieved by the Wiener filter?

**Answer.**

**Minimum MSE.** The MMSE is:

$$J_{\min} = \mathbb{E}\{|e[n]|^2\} = \mathbb{E}\{|d[n]|^2\} - \mathbf{p}^H\mathbf{R}^{-1}\mathbf{p}$$

**Derivation.** At the optimum:

$$J_{\min} = \mathbb{E}\{e[n]d^*[n]\} = \mathbb{E}\{(d[n] - \mathbf{h}_o^T\mathbf{x}[n])d^*[n]\}$$

$$= R_d[0] - \mathbf{h}_o^H \mathbf{p} = R_d[0] - \mathbf{p}^H\mathbf{R}^{-1}\mathbf{p}$$

**Interpretation.** The term $\mathbf{p}^H\mathbf{R}^{-1}\mathbf{p}$ is the power of $d[n]$ that is linearly predictable from $x[n]$. $J_{\min}$ is the residual (irreducible) power that cannot be accounted for by any linear filter applied to $x[n]$.

**Frequency-domain interpretation.** In the non-causal (IIR) case, the minimum MSE is:

$$J_{\min} = \int_{-1/2}^{1/2} S_d(f) \left(1 - \frac{|S_{dx}(f)|^2}{S_d(f)S_x(f)}\right) df = \int_{-1/2}^{1/2} S_d(f)(1 - \gamma_{dx}^2(f))\, df$$

where $\gamma_{dx}^2(f)$ is the coherence between $d$ and $x$. Frequencies where $\gamma_{dx}^2 = 1$ contribute zero to $J_{\min}$; where $\gamma_{dx}^2 = 0$ contribute $S_d(f)$ (no estimation possible at that frequency).

---

## Tier 2: Intermediate

### Q4. Derive the non-causal (IIR) Wiener filter in the frequency domain.

**Answer.**

**Setup.** For the non-causal IIR Wiener filter (filter operates over all time, $-\infty < k < \infty$), the Wiener-Hopf equation becomes a convolution equation:

$$\sum_{k=-\infty}^{\infty} h_o[k] R_x[\ell - k] = R_{dx}[\ell] \quad \text{for all } \ell$$

This is a circular convolution (in the correlation lag variable $\ell$). Taking the DTFT:

$$H_o(e^{j\omega}) \cdot S_x(e^{j\omega}) = S_{dx}(e^{j\omega})$$

**Non-causal Wiener filter:**

$$H_o(e^{j\omega}) = \frac{S_{dx}(e^{j\omega})}{S_x(e^{j\omega})}$$

**Application: signal denoising.** Let $x[n] = s[n] + v[n]$ where $s[n]$ is signal (desired), $v[n]$ is white noise with variance $\sigma_v^2$, independent of $s[n]$. Then:

$$S_x(e^{j\omega}) = S_s(e^{j\omega}) + \sigma_v^2, \qquad S_{dx}(e^{j\omega}) = S_{ds}(e^{j\omega}) = S_s(e^{j\omega})$$

(since $d[n] = s[n]$ and $R_{ds}[\ell] = R_s[\ell]$)

$$H_o(e^{j\omega}) = \frac{S_s(e^{j\omega})}{S_s(e^{j\omega}) + \sigma_v^2}$$

**Interpretation.** The Wiener filter is a frequency-dependent weighting:
- Where $S_s \gg \sigma_v^2$ (high SNR frequency bins): $H_o \approx 1$ — pass the signal.
- Where $S_s \ll \sigma_v^2$ (low SNR bins): $H_o \approx 0$ — suppress the noise.
- At intermediate SNR: $H_o = \text{SNR}(f)/(1 + \text{SNR}(f))$.

This is the **spectral subtraction / Wiener denoising** formula, widely used in speech enhancement.

---

### Q5. What is the causal Wiener filter problem and why is it harder to solve?

**Answer.**

**Causal constraint.** In the causal (one-sided) Wiener filter, the filter must not use future values:

$$y[n] = \sum_{k=0}^{\infty} h[k] x[n-k]$$

The orthogonality condition now only applies for non-negative lags $\ell \geq 0$:

$$\sum_{k=0}^{\infty} h[k] R_x[\ell - k] = R_{dx}[\ell] \quad \text{for } \ell \geq 0$$

**Why harder.** The non-causal solution $H_o = S_{dx}/S_x$ may not be causal (inverse DTFT has non-zero values for negative time). Simply truncating the impulse response to causal does not satisfy the Wiener-Hopf equation because the orthogonality condition must hold only for $\ell \geq 0$, not all $\ell$.

**Wiener-Hopf technique (spectral factorisation).** The causal Wiener filter is derived via:

1. **Spectral factorisation.** Factor $S_x(z) = \sigma^2 L(z) L^*(1/z^*)$ where $L(z)$ is a causal minimum-phase spectral factor (all poles and zeros inside the unit circle), and $\sigma^2$ is a scalar.

2. **Pre-whitening.** The filter $H_o(z) = G(z)/L(z)$ where $G(z)$ is causal. Pre-whitening transforms $x[n]$ (which has PSD $S_x$) to white noise, simplifying the Wiener-Hopf equation.

3. **Causal part extraction.** Compute:

$$G(z) = \frac{1}{\sigma^2}\left[\frac{S_{dx}(z)}{L^*(1/z^*)}\right]_+$$

where $[\cdot]_+$ denotes taking the causal (non-negative lag) part of the Laurent series.

4. **Optimal causal filter:**

$$H_o(z) = \frac{G(z)}{L(z)}$$

**Practical importance.** The causal Wiener filter is required for real-time (on-line) processing, channel prediction, and any application where future observations are unavailable. The solution via spectral factorisation is more complex than the non-causal case but provides the theoretically optimal realisation.

---

### Q6. What is the MSE surface for the FIR Wiener problem? Describe its geometry.

**Answer.**

**MSE as a function of filter weights.** For a general weight vector $\mathbf{h}$ (not necessarily optimal), the MSE is:

$$J(\mathbf{h}) = \mathbb{E}\{|d[n] - \mathbf{h}^H\mathbf{x}[n]|^2\}$$

Expanding:

$$J(\mathbf{h}) = R_d[0] - \mathbf{h}^H\mathbf{p} - \mathbf{p}^H\mathbf{h} + \mathbf{h}^H\mathbf{R}\mathbf{h}$$

**Completing the square:**

$$J(\mathbf{h}) = J_{\min} + (\mathbf{h} - \mathbf{h}_o)^H \mathbf{R} (\mathbf{h} - \mathbf{h}_o)$$

**Geometry.** The MSE surface is a **paraboloid** (bowl shape) in the $N$-dimensional weight space:
- The **minimum** is at $\mathbf{h}_o = \mathbf{R}^{-1}\mathbf{p}$, with value $J_{\min}$.
- The surface is a **hyperellipsoid** in the weight error space $\tilde{\mathbf{h}} = \mathbf{h} - \mathbf{h}_o$.
- The **principal axes** are the eigenvectors of $\mathbf{R}$; the **curvatures** along these axes are $\lambda_k$ (eigenvalues of $\mathbf{R}$).
- The **condition number** $\lambda_{\max}/\lambda_{\min}$ describes how elongated the bowl is:
  - Condition number = 1: spherical bowl, isotropic — steepest descent converges in one step (for exact gradient).
  - Large condition number: highly elongated bowl — steepest descent zigzags slowly.

**Implications for LMS.** LMS navigates this bowl using noisy gradient estimates. The step size $\mu$ must be small enough that the update stays within the bowl ($\mu < 2/\lambda_{\max}$), but the convergence rate is limited by the bowl's narrowest dimension ($\lambda_{\min}$). This is the mathematical explanation for LMS's sensitivity to eigenvalue spread.

---

## Tier 3: Advanced

### Q7. Explain the connection between the Wiener filter and the MMSE estimator. Under what conditions is the Wiener filter globally optimal?

**Answer.**

**MMSE estimator.** The globally optimal (minimum MSE) estimator of $d[n]$ given all observations $\{x[k], -\infty < k \leq n\}$ is the conditional expectation:

$$\hat{d}_{\text{MMSE}}[n] = \mathbb{E}\{d[n] \,|\, x[k], \, k \leq n\}$$

This estimator minimises $\mathbb{E}\{(d[n] - \hat{d}[n])^2\}$ over all measurable functions of the observations — including nonlinear functions.

**When the Wiener filter is globally optimal.** The conditional expectation is linear if and only if the joint distribution of $(d[n], \{x[k]\})$ is **Gaussian**. In this case:

$$\mathbb{E}\{d[n] \,|\, \mathbf{x}\} = \boldsymbol{\mu}_d + \boldsymbol{\Sigma}_{dx}\boldsymbol{\Sigma}_{xx}^{-1}(\mathbf{x} - \boldsymbol{\mu}_x)$$

which is exactly the Wiener filter formula: $\mathbf{R}^{-1}\mathbf{p}$ (zero-mean case).

**Non-Gaussian case.** For non-Gaussian distributions, the conditional expectation may be nonlinear, and the Wiener filter is only the optimal **linear** estimator. The gap between the linear and nonlinear MMSE depends on the degree of non-Gaussianity.

**Practical significance.** Thermal noise, quantisation noise, and many interference sources are well-modelled as Gaussian. Speech signals, however, are non-Gaussian (sparse in the spectral domain). For speech enhancement:
- Wiener filter: optimal linear estimator — widely used due to simplicity.
- Sparse Bayesian estimators (MMSE magnitude spectral estimator, MMSE log-spectral amplitude): exploit non-Gaussianity to further reduce perceptual noise artifacts.

---

### Q8. Derive the Wiener filter for the signal-plus-noise model when the noise is coloured (non-white). How does the solution change?

**Answer.**

**Setup.** Observation model: $x[n] = s[n] + v[n]$ where:
- $s[n]$: desired signal with PSD $S_s(e^{j\omega})$
- $v[n]$: coloured noise with PSD $S_v(e^{j\omega})$ (not white)
- $s[n]$ and $v[n]$ are uncorrelated: $R_{sv}[k] = 0$ for all $k$
- Desired: $d[n] = s[n]$

**Correlation functions:**

$$S_x(e^{j\omega}) = S_s(e^{j\omega}) + S_v(e^{j\omega})$$

$$S_{dx}(e^{j\omega}) = S_{ds}(e^{j\omega}) = S_s(e^{j\omega})$$

(Since $d[n] = s[n]$ and $d, v$ are uncorrelated.)

**Non-causal Wiener filter:**

$$H_o(e^{j\omega}) = \frac{S_s(e^{j\omega})}{S_s(e^{j\omega}) + S_v(e^{j\omega})}$$

This has the same form as the white noise case — the coloured noise enters only through $S_v(e^{j\omega})$.

**Interpretation.** The Wiener filter is a frequency-dependent gain:

$$H_o(f) = \frac{\text{SNR}(f)}{1 + \text{SNR}(f)}, \quad \text{where } \text{SNR}(f) = \frac{S_s(f)}{S_v(f)}$$

- Where the local SNR is high: $H_o \approx 1$ (pass through)
- Where the local SNR is low: $H_o \approx 0$ (suppress)

**Coloured noise pre-whitening (causal case).** For the causal Wiener filter with coloured noise, it is often convenient to pre-whiten the observations using a pre-filter $1/L_v(z)$ (inverse spectral factor of $S_v$), reducing the problem to one with white noise. The causal Wiener filter for the whitened problem is then cascaded with $1/L_v(z)$.

**Matrix form.** For the FIR case, the Wiener-Hopf equation remains:

$$(\mathbf{R}_s + \mathbf{R}_v)\mathbf{h}_o = \mathbf{p}_s$$

where $\mathbf{R}_s$ and $\mathbf{R}_v$ are the autocorrelation matrices of signal and noise respectively, and $\mathbf{p}_s = [R_s[0], R_s[1], \ldots]^T$. Compared to the white noise case (where $\mathbf{R}_v = \sigma_v^2\mathbf{I}$), the coloured noise case requires a full matrix inversion of $(\mathbf{R}_s + \mathbf{R}_v)$ — no special structure exists unless $\mathbf{R}_v$ is diagonal.

---

## Quick Reference: Wiener Filter Summary

| Quantity | Formula |
|---|---|
| Wiener-Hopf (matrix) | $\mathbf{R}\mathbf{h}_o = \mathbf{p}$ |
| Wiener filter | $\mathbf{h}_o = \mathbf{R}^{-1}\mathbf{p}$ |
| Minimum MSE | $J_{\min} = R_d[0] - \mathbf{p}^H\mathbf{R}^{-1}\mathbf{p}$ |
| Non-causal (freq. domain) | $H_o(f) = S_{dx}(f)/S_x(f)$ |
| Denoising Wiener filter | $H_o(f) = S_s(f)/(S_s(f)+S_v(f))$ |
| Denoising SNR form | $H_o(f) = \text{SNR}(f)/(1+\text{SNR}(f))$ |
| MSE surface | $J(\mathbf{h}) = J_{\min} + (\mathbf{h}-\mathbf{h}_o)^H\mathbf{R}(\mathbf{h}-\mathbf{h}_o)$ |
| Optimal (globally) when | $(d[n], x[n])$ jointly Gaussian |
