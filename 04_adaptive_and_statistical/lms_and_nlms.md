# LMS and NLMS Algorithms: Interview Questions

## Overview

The Least Mean Squares (LMS) algorithm and its normalised variant (NLMS) are the most widely deployed adaptive filtering algorithms. They appear in echo cancellation, channel equalisation, noise cancellation, and beamforming. Interview questions span the derivation from first principles, convergence analysis, and practical implementation trade-offs.

---

## Tier 1: Fundamentals

### Q1. What problem does the LMS algorithm solve? State the adaptive filtering setup.

**Answer.**

**Adaptive filtering setup.** We observe a desired signal $d[n]$ and an input (reference) signal $x[n]$. The goal is to find a linear FIR filter $\mathbf{w} \in \mathbb{R}^N$ (or $\mathbb{C}^N$) such that the filter output $y[n] = \mathbf{w}^T \mathbf{x}[n]$ approximates $d[n]$ as closely as possible, where $\mathbf{x}[n] = [x[n], x[n-1], \ldots, x[n-N+1]]^T$ is the input regressor vector.

**Cost function.** The LMS algorithm minimises the instantaneous squared error:

$$e[n] = d[n] - y[n] = d[n] - \mathbf{w}^T[n]\,\mathbf{x}[n]$$

$$J[n] = e^2[n]$$

**Why this problem is important.** In a static environment, the optimal filter is the Wiener filter (solved off-line using the autocorrelation matrix and cross-correlation vector). However, when the signal statistics are unknown or time-varying, the Wiener filter cannot be computed directly. The LMS algorithm adaptively tracks the optimal solution using only current data.

---

### Q2. Derive the LMS update rule from the steepest descent principle.

**Answer.**

**Steepest descent (batch).** The ideal steepest descent algorithm updates the filter weights along the negative gradient of the expected MSE surface $J = \mathbb{E}\{e^2[n]\}$:

$$\mathbf{w}[n+1] = \mathbf{w}[n] - \frac{\mu}{2} \nabla_{\mathbf{w}} J$$

The gradient of the MSE with respect to $\mathbf{w}$:

$$\nabla_{\mathbf{w}} J = -2\mathbb{E}\{e[n]\,\mathbf{x}[n]\} = -2(\mathbf{p} - \mathbf{R}\mathbf{w})$$

where $\mathbf{R} = \mathbb{E}\{\mathbf{x}[n]\mathbf{x}^T[n]\}$ is the input autocorrelation matrix and $\mathbf{p} = \mathbb{E}\{d[n]\mathbf{x}[n]\}$ is the cross-correlation vector.

**LMS approximation (stochastic gradient descent).** Computing the true gradient requires statistical expectations — unavailable in real-time. LMS substitutes the instantaneous gradient:

$$\hat{\nabla}_{\mathbf{w}} J[n] = -2e[n]\,\mathbf{x}[n]$$

This replaces $\mathbb{E}\{e[n]\mathbf{x}[n]\}$ with the single-sample estimate $e[n]\mathbf{x}[n]$.

**LMS update rule:**

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \mu \, e[n] \, \mathbf{x}[n]$$

$$e[n] = d[n] - \mathbf{w}^T[n]\,\mathbf{x}[n]$$

This is the complete LMS algorithm: one dot product to compute $y[n]$, one subtraction to get $e[n]$, and one scaled vector addition to update $\mathbf{w}[n]$.

**Complexity per sample:** $O(N)$ multiplications and additions — linear in filter order $N$.

---

### Q3. What are the stability and convergence conditions for the LMS step size $\mu$?

**Answer.**

**Necessary and sufficient condition for convergence in the mean:**

$$0 < \mu < \frac{2}{\lambda_{\max}}$$

where $\lambda_{\max}$ is the largest eigenvalue of the input autocorrelation matrix $\mathbf{R} = \mathbb{E}\{\mathbf{x}[n]\mathbf{x}^T[n]\}$.

**Derivation sketch.** The weight error vector $\tilde{\mathbf{w}}[n] = \mathbf{w}[n] - \mathbf{w}_o$ (deviation from the Wiener solution $\mathbf{w}_o = \mathbf{R}^{-1}\mathbf{p}$) evolves as:

$$\mathbb{E}\{\tilde{\mathbf{w}}[n+1]\} = (\mathbf{I} - \mu\mathbf{R})\mathbb{E}\{\tilde{\mathbf{w}}[n]\}$$

For this to converge to zero, all eigenvalues of $(\mathbf{I} - \mu\mathbf{R})$ must lie within the unit circle:

$$|1 - \mu\lambda_k| < 1 \quad \forall k$$

$$\Rightarrow 0 < \mu < \frac{2}{\lambda_k} \quad \forall k$$

The binding constraint is $k = \arg\max \lambda_k$, giving $\mu < 2/\lambda_{\max}$.

**Practical bound.** Since $\lambda_{\max} \leq \text{tr}(\mathbf{R}) = N \sigma_x^2$ (where $\sigma_x^2 = \mathbb{E}\{x^2[n]\}$):

$$\mu < \frac{2}{N \sigma_x^2}$$

A conservative rule of thumb: $\mu \leq \frac{0.1}{N \sigma_x^2}$.

**Effect of step size:**
- Large $\mu$ (near upper bound): fast convergence, large steady-state misadjustment.
- Small $\mu$: slow convergence, low steady-state misadjustment.
- $\mu$ too large: divergence.

---

### Q4. What is misadjustment, and how does it quantify the LMS excess MSE?

**Answer.**

**Excess MSE.** At steady state, the LMS filter does not converge to the exact Wiener solution. The weight vector fluctuates around $\mathbf{w}_o$ due to the gradient noise from using instantaneous estimates. The **excess MSE** is:

$$J_{\text{ex}} = J_{\infty} - J_{\min}$$

where $J_{\infty}$ is the steady-state MSE achieved by LMS and $J_{\min} = \mathbb{E}\{e_o^2[n]\}$ is the minimum MSE of the optimal Wiener filter.

**Misadjustment.** The normalised excess MSE:

$$\mathcal{M} = \frac{J_{\text{ex}}}{J_{\min}} \approx \frac{\mu \,\text{tr}(\mathbf{R})}{2}$$

For white input with variance $\sigma_x^2$: $\text{tr}(\mathbf{R}) = N\sigma_x^2$:

$$\mathcal{M} \approx \frac{\mu N \sigma_x^2}{2}$$

**Interpretation.** Misadjustment is the fractional overshoot above the minimum MSE due to the stochastic gradient noise. A misadjustment of 0.1 (10%) means the steady-state MSE is 10% above the theoretical minimum.

**Design trade-off.** To achieve both fast convergence and low misadjustment is impossible with a fixed $\mu$. One must choose:
- Fast tracking: larger $\mu$, accept higher misadjustment.
- Precision estimation: smaller $\mu$, accept slower tracking.
- Time-varying $\mu$: large initially (fast convergence), reduced over time (lower final misadjustment).

---

## Tier 2: Intermediate

### Q5. Derive the NLMS update rule. What problem does it solve compared to LMS?

**Answer.**

**The problem with LMS.** The LMS convergence condition $\mu < 2/\lambda_{\max}$ depends on $\lambda_{\max}$, which is proportional to the input power $\sigma_x^2$. When the input power varies (e.g., speech pauses vs. active speech), a fixed $\mu$ that is stable during low-power periods may be too small for fast tracking during high-power periods, or unstable during high-power periods if set for fast tracking.

**NLMS derivation (projection interpretation).** At each step, NLMS seeks the weight vector $\mathbf{w}[n+1]$ that:
1. Minimises $\|\mathbf{w}[n+1] - \mathbf{w}[n]\|^2$ (small update)
2. Subject to: $d[n] - \mathbf{w}^T[n+1]\mathbf{x}[n] = 0$ (zero error constraint)

Using Lagrange multipliers, the solution is:

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \frac{e[n]}{\|\mathbf{x}[n]\|^2}\,\mathbf{x}[n]$$

**NLMS update rule (with regularisation and step size $\tilde{\mu} \in (0, 2)$):**

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \frac{\tilde{\mu}}{\delta + \|\mathbf{x}[n]\|^2}\,e[n]\,\mathbf{x}[n]$$

where $\delta > 0$ is a regularisation constant (prevents division by near-zero when input is small).

**What NLMS achieves:**
- The effective step size $\tilde{\mu}/\|\mathbf{x}[n]\|^2$ automatically scales inversely with input power.
- Convergence condition: $0 < \tilde{\mu} < 2$, **independent of input power**.
- Typical choice: $\tilde{\mu} = 0.1$ to $0.5$ for well-regularised NLMS.

**Relationship to LMS.** LMS with $\mu = \tilde{\mu}/\|\mathbf{x}[n]\|^2$ (time-varying step) is NLMS. LMS is a special case with constant denominator.

---

### Q6. Compare LMS and NLMS on convergence speed, misadjustment, and computational complexity.

**Answer.**

| Property | LMS | NLMS |
|---|---|---|
| **Update rule** | $\mathbf{w} + \mu e \mathbf{x}$ | $\mathbf{w} + \frac{\tilde\mu}{\delta+\|\mathbf{x}\|^2}e\mathbf{x}$ |
| **Step size** | Fixed $\mu$ (scalar) | Normalised by input power |
| **Convergence condition** | $0 < \mu < 2/\lambda_{\max}$ | $0 < \tilde\mu < 2$ |
| **Convergence rate** | $\approx \mu\lambda_{\min}$ (slowest mode) | $\approx \tilde\mu/(N\sigma_x^2)$ |
| **Misadjustment** | $\approx \mu N \sigma_x^2 / 2$ | $\approx \tilde\mu N / (2(\delta/\sigma_x^2 + N))$ |
| **Sensitivity to input power** | High (must retune $\mu$ for each signal level) | Low (self-normalising) |
| **Computational cost** | $2N + 1$ mult/add per sample | $2N + 2$ mult/add + 1 division per sample |
| **Numerical issues** | Stable for correct $\mu$ | Need $\delta > 0$ to avoid $1/0$ |

**When to use LMS:**
- Input is stationary with known power level.
- Computational resources are extremely constrained (the division in NLMS is avoided).
- Hardware with dedicated DSP units (fixed-point, pipelined multiply-accumulate).

**When to use NLMS:**
- Non-stationary input power (speech, variable-bit-rate streams).
- Input power is unknown or variable.
- Robustness to input level changes is important (e.g., acoustic echo cancellers).

---

### Q7. What is the learning curve of an adaptive filter? Explain its shape and what it implies about convergence.

**Answer.**

**Definition.** The **learning curve** is the plot of instantaneous MSE $J[n] = \mathbb{E}\{e^2[n]\}$ (or its ensemble average over many realisations) as a function of sample index $n$.

**Shape.** Under the independence assumption (input vectors $\mathbf{x}[n]$ at different times are statistically independent — not exactly true but a useful approximation):

$$J[n] = J_{\min} + \sum_{k=1}^{N} c_k (1 - \mu\lambda_k)^{2n}$$

where $\lambda_k$ are eigenvalues of $\mathbf{R}$ and $c_k$ are coefficients depending on the initial weight error.

**Interpretation:**
- **Initial MSE** (at $n=0$): $J[0] = J_{\min} + \sum_k c_k$, which depends on the initial weight error.
- **Exponential decay**: each mode $k$ decays with time constant $\tau_k = -1 / (2\ln|1-\mu\lambda_k|) \approx 1/(2\mu\lambda_k)$.
- **Slowest mode**: determined by the smallest eigenvalue: $\tau_{\max} = 1/(2\mu\lambda_{\min})$.
- **Steady state** (large $n$): $J[n] \to J_{\min} + J_{\text{ex}} = J_{\min}(1 + \mathcal{M})$.

**Eigenvalue spread effect.** When $\lambda_{\max} \gg \lambda_{\min}$ (poor conditioning of $\mathbf{R}$), the slowest mode decays much more slowly than the fastest mode. The learning curve has an initial steep drop (fast modes converging) followed by a long tail (slow modes). This is why a high eigenvalue spread degrades LMS convergence.

**Practical measurement.** In practice, ensemble averaging over many independent Monte Carlo runs is needed to reveal a smooth learning curve. A single realisation is too noisy. Alternatively, time-averaging with a sliding window gives an approximation.

---

### Q8. How does the LMS algorithm behave in a system identification context? What are the steady-state weight error covariance properties?

**Answer.**

**System identification setup.** The desired signal is generated by an unknown system $\mathbf{w}_o$:

$$d[n] = \mathbf{w}_o^T \mathbf{x}[n] + v[n]$$

where $v[n]$ is observation noise with variance $\sigma_v^2$, independent of $\mathbf{x}[n]$.

**The Wiener solution** is $\mathbf{w}_o$ (exactly, since there is a true underlying system and $v[n]$ is independent). The minimum MSE is $J_{\min} = \sigma_v^2$.

**Steady-state weight error.** The LMS weight error $\tilde{\mathbf{w}}[n] = \mathbf{w}[n] - \mathbf{w}_o$ does not converge to zero but maintains a distribution around zero with covariance:

$$\mathbf{K}_{\tilde{w}} = \mathbb{E}\{\tilde{\mathbf{w}}\tilde{\mathbf{w}}^T\} \approx \frac{\mu \sigma_v^2}{2} \mathbf{I} \quad \text{(white input approximation)}$$

More precisely, for coloured input:

$$\mathbf{K}_{\tilde{w}} \approx \frac{\mu \sigma_v^2}{2} \mathbf{R}^{-1}$$

**Implications:**
- Each weight estimate has steady-state variance $\approx \frac{\mu \sigma_v^2}{2} / \lambda_k$ — larger for eigenvalues corresponding to poorly excited modes.
- The excess MSE: $J_{\text{ex}} = \text{tr}(\mathbf{R}\mathbf{K}_{\tilde{w}}) \approx \frac{\mu \sigma_v^2}{2} \text{tr}(\mathbf{I}) = \frac{\mu N \sigma_v^2}{2}$
- Misadjustment: $\mathcal{M} = J_{\text{ex}}/J_{\min} = \mu N/2$ (for unit-variance white noise input with $\sigma_x^2 = 1$, $\sigma_v^2 = J_{\min}$).

---

## Tier 3: Advanced

### Q9. Derive the steady-state excess MSE of the LMS algorithm using the energy conservation approach.

**Answer.**

**Energy conservation framework** (Sayed, 2003). Define:
- Weight error vector: $\tilde{\mathbf{w}}[n] = \mathbf{w}[n] - \mathbf{w}_o$
- A priori error: $e_a[n] = \mathbf{w}_o^T\mathbf{x}[n] + v[n] - \mathbf{w}^T[n]\mathbf{x}[n] = -\tilde{\mathbf{w}}^T[n]\mathbf{x}[n] + v[n]$
- A posteriori error: $e_p[n] = d[n] - \mathbf{w}^T[n+1]\mathbf{x}[n] = e_a[n] - \mu\|\mathbf{x}[n]\|^2 e_a[n] + \mu\|\mathbf{x}[n]\|^2 v[n]$

**Energy conservation relation.** From the LMS update $\tilde{\mathbf{w}}[n+1] = \tilde{\mathbf{w}}[n] - \mu e[n]\mathbf{x}[n]$:

$$\|\tilde{\mathbf{w}}[n+1]\|^2 = \|\tilde{\mathbf{w}}[n]\|^2 - 2\mu e[n]\tilde{\mathbf{w}}^T[n]\mathbf{x}[n] + \mu^2 e^2[n]\|\mathbf{x}[n]\|^2$$

Taking expectations at steady state ($\mathbb{E}\{\|\tilde{\mathbf{w}}\|^2\} = $ const):

$$0 = -2\mu \mathbb{E}\{e[n]\tilde{\mathbf{w}}^T[n]\mathbf{x}[n]\} + \mu^2 \mathbb{E}\{e^2[n]\|\mathbf{x}[n]\|^2\}$$

Since $e[n] = e_a[n] = -\tilde{\mathbf{w}}^T[n]\mathbf{x}[n] + v[n]$ at steady state (approximately), and under the independence assumption:

$$\mathbb{E}\{e[n]\tilde{\mathbf{w}}^T[n]\mathbf{x}[n]\} = \mathbb{E}\{(-\tilde{\mathbf{w}}^T\mathbf{x} + v)\tilde{\mathbf{w}}^T\mathbf{x}\} = -\mathbb{E}\{(\tilde{\mathbf{w}}^T\mathbf{x})^2\} = -J_{\text{ex}}$$

For $\mathbb{E}\{e^2[n]\|\mathbf{x}[n]\|^2\}$:

$$\mathbb{E}\{e^2\|\mathbf{x}\|^2\} \approx \mathbb{E}\{e^2\} \cdot \mathbb{E}\{\|\mathbf{x}\|^2\} = J_\infty \cdot \text{tr}(\mathbf{R})$$

Substituting:

$$0 = 2\mu J_{\text{ex}} - \mu^2 J_\infty \, \text{tr}(\mathbf{R})$$

$$J_{\text{ex}} = \frac{\mu}{2} J_\infty \, \text{tr}(\mathbf{R})$$

Since $J_\infty = J_{\min} + J_{\text{ex}}$:

$$J_{\text{ex}} = \frac{\mu \, \text{tr}(\mathbf{R})}{2 - \mu \, \text{tr}(\mathbf{R})} J_{\min}$$

**Misadjustment:**

$$\mathcal{M} = \frac{J_{\text{ex}}}{J_{\min}} = \frac{\mu \, \text{tr}(\mathbf{R})}{2 - \mu \, \text{tr}(\mathbf{R})} \approx \frac{\mu \, \text{tr}(\mathbf{R})}{2} \quad \text{for small } \mu$$

This is the classical misadjustment formula, derived without assuming Gaussian inputs.

---

### Q10. What is the eigenvalue spread problem in LMS convergence? How does input whitening (or a pre-whitening filter) address it?

**Answer.**

**Eigenvalue spread.** The condition number of $\mathbf{R}$ is:

$$\chi(\mathbf{R}) = \frac{\lambda_{\max}}{\lambda_{\min}}$$

**Effect on convergence time.** The time constant for the $k$-th mode:

$$\tau_k = \frac{1}{2\mu\lambda_k}$$

The slowest mode (dominant convergence time): $\tau_{\text{slow}} = 1/(2\mu\lambda_{\min})$.

The fastest allowable $\mu$ for stability: $\mu < 2/\lambda_{\max}$.

At the maximum allowable $\mu$:

$$\tau_{\text{slow}} = \frac{1}{2\lambda_{\min}} \cdot \frac{\lambda_{\max}}{2} \cdot \frac{2}{\lambda_{\max}} = \frac{\lambda_{\max}}{4\lambda_{\min} \cdot \mu_{\max}/2} \approx \frac{\chi(\mathbf{R})}{4}$$

For $\chi(\mathbf{R}) = 100$, the slowest mode takes $\approx 25$ times longer to converge than if all modes had equal eigenvalues.

**Input whitening.** Pre-filtering $\mathbf{x}[n]$ with a whitening filter $P^{-1/2}$ (the inverse square root of the spectral factor of $\mathbf{R}$) transforms the input autocorrelation matrix to:

$$\mathbf{R}' = P^{-1/2} \mathbf{R} P^{-T/2} = \mathbf{I}$$

All eigenvalues are 1; $\chi(\mathbf{R}') = 1$; all modes converge at the same rate.

**Practical pre-whitening approaches:**
1. **Lattice LMS:** applies a lattice predictor to whiten the input. Each lattice stage removes one pole of the input spectrum. The resulting transformed input is better conditioned.
2. **RLS algorithm:** implicitly applies a pre-whitening transformation via the inverse autocorrelation matrix $\mathbf{P}[n] = \mathbf{R}^{-1}[n]$. RLS converges in exactly $N$ steps for stationary inputs (in the absence of noise), regardless of eigenvalue spread — at the cost of $O(N^2)$ computation.
3. **Affine projection algorithm (APA):** a compromise between LMS ($O(N)$) and RLS ($O(N^2)$): projects the gradient onto a $K$-dimensional subspace spanned by the last $K$ input vectors, at cost $O(KN)$.

---

## Quick Reference: LMS/NLMS Algorithm Summary

**LMS algorithm:**
```
Initialise: w[0] = 0
For each sample n:
    y[n] = w^T[n] * x[n]         (filter output)
    e[n] = d[n] - y[n]           (error)
    w[n+1] = w[n] + mu * e[n] * x[n]   (weight update)
```

**NLMS algorithm:**
```
Initialise: w[0] = 0
For each sample n:
    y[n] = w^T[n] * x[n]
    e[n] = d[n] - y[n]
    mu_n = mu_tilde / (delta + ||x[n]||^2)
    w[n+1] = w[n] + mu_n * e[n] * x[n]
```

| Quantity | Formula |
|---|---|
| LMS step bound | $0 < \mu < 2/\lambda_{\max}$ |
| Safe practical bound | $\mu \approx 0.1 / (N\sigma_x^2)$ |
| NLMS step bound | $0 < \tilde\mu < 2$ |
| Convergence time constant | $\tau_k \approx 1/(2\mu\lambda_k)$ samples |
| Misadjustment | $\mathcal{M} \approx \mu N \sigma_x^2 / 2$ |
| Excess MSE | $J_{\text{ex}} = \mathcal{M} \cdot J_{\min}$ |
| Complexity (per sample) | $O(N)$ multiplications |
