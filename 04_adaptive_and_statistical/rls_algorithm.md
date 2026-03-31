# RLS Algorithm: Interview Questions

## Overview

The Recursive Least Squares (RLS) algorithm is the fast-converging counterpart to LMS. It is the adaptive implementation of the least-squares estimator, updated recursively at each new sample using the matrix inversion lemma. RLS is critical knowledge for senior DSP roles, communications systems, and anywhere that fast adaptation is required.

---

## Tier 1: Fundamentals

### Q1. What objective function does RLS minimise? How does it differ from LMS?

**Answer.**

**RLS cost function.** RLS minimises the exponentially weighted sum of past squared errors:

$$J_{\text{RLS}}[n] = \sum_{k=1}^{n} \lambda^{n-k} e^2[k] = \sum_{k=1}^{n} \lambda^{n-k} \bigl(d[k] - \mathbf{w}^T\mathbf{x}[k]\bigr)^2$$

where $\lambda \in (0, 1]$ is the **forgetting factor**.

**Key distinctions from LMS:**

| Property | LMS | RLS |
|---|---|---|
| **Cost function** | Instantaneous $e^2[n]$ | Exponentially weighted sum $\sum \lambda^{n-k} e^2[k]$ |
| **Solution type** | Stochastic gradient step | Exact least-squares solution at each step |
| **Convergence speed** | $O(1/\lambda_{\min})$ time constants | $O(N)$ samples (deterministic) |
| **Complexity per step** | $O(N)$ | $O(N^2)$ |
| **Step size parameter** | $\mu$ (requires tuning for each input level) | $\lambda$ (closer to 1 = longer memory; more stable) |

**Why the exponential weighting?** In a non-stationary environment, old data should be down-weighted. The forgetting factor $\lambda$ effectively gives the algorithm a **memory of $1/(1-\lambda)$ samples**: errors from $1/(1-\lambda)$ samples ago are weighted by $\lambda^{1/(1-\lambda)} \approx e^{-1} \approx 0.37$.

---

### Q2. Derive the recursive update equations for RLS using the matrix inversion lemma.

**Answer.**

**Batch least-squares solution.** At time $n$, the least-squares estimate is:

$$\hat{\mathbf{w}}[n] = \boldsymbol{\Phi}^{-1}[n]\,\boldsymbol{\theta}[n]$$

where the weighted covariance matrix and cross-correlation vector are:

$$\boldsymbol{\Phi}[n] = \sum_{k=1}^{n} \lambda^{n-k} \mathbf{x}[k]\mathbf{x}^T[k], \qquad \boldsymbol{\theta}[n] = \sum_{k=1}^{n} \lambda^{n-k} d[k]\mathbf{x}[k]$$

**Recursive update of $\boldsymbol{\Phi}[n]$:**

$$\boldsymbol{\Phi}[n] = \lambda\boldsymbol{\Phi}[n-1] + \mathbf{x}[n]\mathbf{x}^T[n]$$

**Matrix inversion lemma.** We need $\mathbf{P}[n] = \boldsymbol{\Phi}^{-1}[n]$. Applying the Sherman-Morrison-Woodbury identity:

$$(\mathbf{A} + \mathbf{u}\mathbf{v}^T)^{-1} = \mathbf{A}^{-1} - \frac{\mathbf{A}^{-1}\mathbf{u}\mathbf{v}^T\mathbf{A}^{-1}}{1 + \mathbf{v}^T\mathbf{A}^{-1}\mathbf{u}}$$

with $\mathbf{A} = \lambda\boldsymbol{\Phi}[n-1]$, $\mathbf{u} = \mathbf{x}[n]$, $\mathbf{v} = \mathbf{x}[n]$:

$$\mathbf{P}[n] = \frac{1}{\lambda}\mathbf{P}[n-1] - \frac{\frac{1}{\lambda}\mathbf{P}[n-1]\mathbf{x}[n]\mathbf{x}^T[n]\frac{1}{\lambda}\mathbf{P}[n-1]}{1 + \mathbf{x}^T[n]\frac{1}{\lambda}\mathbf{P}[n-1]\mathbf{x}[n]}$$

Define the **Kalman gain vector:**

$$\mathbf{k}[n] = \frac{\mathbf{P}[n-1]\mathbf{x}[n]}{\lambda + \mathbf{x}^T[n]\mathbf{P}[n-1]\mathbf{x}[n]}$$

Then:

$$\mathbf{P}[n] = \frac{1}{\lambda}\bigl(\mathbf{P}[n-1] - \mathbf{k}[n]\mathbf{x}^T[n]\mathbf{P}[n-1]\bigr)$$

**Recursive update of $\hat{\mathbf{w}}[n]$:**

$$\boldsymbol{\theta}[n] = \lambda\boldsymbol{\theta}[n-1] + d[n]\mathbf{x}[n]$$

$$\hat{\mathbf{w}}[n] = \mathbf{P}[n]\boldsymbol{\theta}[n]$$

Substituting and simplifying:

$$\hat{\mathbf{w}}[n] = \hat{\mathbf{w}}[n-1] + \mathbf{k}[n]\,\xi[n]$$

where $\xi[n] = d[n] - \hat{\mathbf{w}}^T[n-1]\mathbf{x}[n]$ is the **a priori error** (innovation).

**Complete RLS algorithm (per sample):**

1. $\xi[n] = d[n] - \hat{\mathbf{w}}^T[n-1]\mathbf{x}[n]$
2. $\mathbf{k}[n] = \mathbf{P}[n-1]\mathbf{x}[n] / (\lambda + \mathbf{x}^T[n]\mathbf{P}[n-1]\mathbf{x}[n])$
3. $\hat{\mathbf{w}}[n] = \hat{\mathbf{w}}[n-1] + \mathbf{k}[n]\,\xi[n]$
4. $\mathbf{P}[n] = (\mathbf{P}[n-1] - \mathbf{k}[n]\mathbf{x}^T[n]\mathbf{P}[n-1]) / \lambda$

**Initialisation:** $\hat{\mathbf{w}}[0] = \mathbf{0}$, $\mathbf{P}[0] = \delta^{-1}\mathbf{I}$ (large $\delta^{-1}$ represents high initial uncertainty).

---

### Q3. What is the convergence speed of RLS and how does it compare to LMS?

**Answer.**

**RLS convergence.** RLS converges to the optimal Wiener filter in exactly $N$ samples for a stationary input (in the noise-free case). More precisely, after receiving $N$ linearly independent input vectors, the RLS estimate $\hat{\mathbf{w}}[N]$ is the exact least-squares solution using all $N$ observations.

**Why $N$ samples?** The $N \times N$ matrix $\boldsymbol{\Phi}[N]$ becomes full rank after $N$ linearly independent observations, at which point $\mathbf{P}[N] = \boldsymbol{\Phi}^{-1}[N]$ is well-defined and the estimate is exact. In terms of modes: RLS is equivalent to inverting $\mathbf{R}$ directly, which eliminates the mode-by-mode convergence bottleneck of LMS.

**LMS convergence time (comparison).** LMS converges in $\approx 5/(2\mu\lambda_{\min})$ samples (time to reach $e^{-5}$ fraction of initial error in the slowest mode). For $\mu = 2/(N\sigma_x^2)$ (near maximum), and $\lambda_{\min} = \sigma_x^2 / \chi$ where $\chi = \chi(\mathbf{R})$:

$$\tau_{\text{LMS}} \approx \frac{5N\chi}{4}$$

For $N = 64$ taps and $\chi = 30$ (typical speech input): $\tau_{\text{LMS}} \approx 4800$ samples vs. $\tau_{\text{RLS}} \approx 64$ samples — a 75x speedup.

**Forgetting factor effect on RLS convergence.** With $\lambda < 1$, RLS converges faster in non-stationary environments but with slightly higher steady-state variance (since the effective data length is $1/(1-\lambda)$).

---

## Tier 2: Intermediate

### Q4. How does the forgetting factor $\lambda$ control the trade-off between tracking speed and estimation variance in a non-stationary environment?

**Answer.**

**Effective memory.** The exponential weights $\lambda^{n-k}$ decay to $e^{-1} \approx 0.37$ after $L_{\text{eff}} = 1/(1-\lambda)$ samples. This is the **effective memory length** of RLS.

**Tracking speed.** When the true system $\mathbf{w}_o$ changes (a "system jump"), RLS must forget the old data and re-learn from new data. The tracking lag after a step change is approximately $L_{\text{eff}} = 1/(1-\lambda)$ samples. Smaller $\lambda$ $\Rightarrow$ faster tracking.

**Estimation variance.** For $\lambda = 1$ (no forgetting) and stationary input, RLS becomes more and more accurate as $n \to \infty$ (variance $\propto 1/n$). For $\lambda < 1$:

$$\text{Var}\{\hat{w}_k[n]\} \approx \frac{\sigma_v^2}{(1-\lambda) \lambda_k}$$

(in the large-$n$ limit). Smaller $\lambda$ $\Rightarrow$ larger variance.

**Misadjustment for RLS:**

$$\mathcal{M}_{\text{RLS}} \approx \frac{(1-\lambda) N}{1 - (1-\lambda) N} \approx (1-\lambda)N \quad \text{for small } (1-\lambda)N$$

Compare with LMS: $\mathcal{M}_{\text{LMS}} \approx \mu N \sigma_x^2 / 2$. The parameter correspondence is $\mu \sigma_x^2 \leftrightarrow 2(1-\lambda)$.

**Typical $\lambda$ values:**

| Environment | $\lambda$ | $L_{\text{eff}}$ |
|---|:-:|:-:|
| Very slowly varying | 0.9999 | 10000 |
| Slowly varying | 0.999 | 1000 |
| Moderately varying | 0.99 | 100 |
| Rapidly varying | 0.97 | 33 |
| Very rapidly varying | 0.9 | 10 |

---

### Q5. What is the $O(N^2)$ computational complexity of RLS, and when is this problematic?

**Answer.**

**Operation count per sample.** The dominant cost is computing the Kalman gain $\mathbf{k}[n]$:

1. $\mathbf{P}[n-1]\mathbf{x}[n]$: matrix-vector multiply, $N^2$ multiplications, $N^2$ additions.
2. $\mathbf{x}^T[n]\mathbf{P}[n-1]\mathbf{x}[n]$: scalar, $N$ multiplications.
3. Division: 1 division.
4. $\mathbf{k}[n]\mathbf{x}^T[n]\mathbf{P}[n-1]$: outer product, $N^2$ multiplications.
5. $\mathbf{P}[n]$ update: $N^2$ additions, $N^2$ multiplications (divide by $\lambda$).
6. $\hat{\mathbf{w}}[n]$ update: $N$ multiplications, $N$ additions.

**Total per sample:** $\approx 2.5N^2$ multiplications and $2N^2$ additions — $O(N^2)$.

**Memory:** $\mathbf{P}[n]$ is an $N \times N$ matrix requiring $N^2$ storage. For $N = 1000$: 8 MB (double precision).

**Problematic scales:**
- $N = 64$: $\approx 10000$ mults/sample — feasible for most DSPs.
- $N = 256$: $\approx 164000$ mults/sample — demanding for real-time at 44 kHz audio.
- $N = 1024$: $\approx 2.6 \times 10^6$ mults/sample — impractical for real-time processing.
- Long acoustic echo cancellers: $N = 4096$ (512 ms at 8 kHz) — RLS is completely impractical.

**Fast RLS variants** reduce complexity to $O(N)$:
- **Fast Transversal Filter (FTF):** $O(N)$ operations per sample, but numerically unstable (error accumulates).
- **Lattice RLS:** Numerically more stable than FTF, but more complex to implement.
- **Approximate RLS (APA, conjugate gradient RLS):** $O(KN)$ for $K$ projection vectors.

---

### Q6. Explain the numerical stability issues in RLS. What can go wrong and how is it mitigated?

**Answer.**

**The numerical problem.** The $\mathbf{P}[n]$ matrix must remain symmetric and positive definite throughout the algorithm. Numerically, this can fail due to:

1. **Round-off error accumulation.** The update $\mathbf{P}[n] = (\mathbf{P}[n-1] - \mathbf{k}\mathbf{x}^T\mathbf{P})/\lambda$ subtracts nearly equal quantities when $\mathbf{k}\mathbf{x}^T\mathbf{P}$ is close to $\mathbf{P}$. Subtractive cancellation errors cause $\mathbf{P}$ to lose positive definiteness, appearing as negative diagonal elements.

2. **Loss of symmetry.** Floating-point arithmetic does not preserve the symmetry $\mathbf{P} = \mathbf{P}^T$. Asymmetric $\mathbf{P}$ propagates errors exponentially.

3. **$\lambda < 1$ instability.** The $1/\lambda$ factor amplifies errors at each step. For $\lambda = 0.99$ and $N = 100$ steps, the amplification is $\lambda^{-100} \approx 2.7$ — modest. But over thousands of steps, accumulated errors are significant.

**Mitigation strategies:**

**1. Symmetrising:** After each update, enforce symmetry: $\mathbf{P}[n] \leftarrow (\mathbf{P}[n] + \mathbf{P}^T[n])/2$. Cheap and partially effective.

**2. Square-root algorithms (UD or Cholesky factorisation):** Instead of propagating $\mathbf{P}$, maintain its Cholesky factor $\mathbf{U}\mathbf{D}\mathbf{U}^T$ (UD decomposition) or Cholesky factor $\mathbf{L}$ such that $\mathbf{P} = \mathbf{L}\mathbf{L}^T$. Updates to the factored form remain numerically stable — equivalent to maintaining $\mathbf{P} > 0$ by construction, at $O(N^2)$ cost with a smaller constant.

**3. Regularisation.** Add $\epsilon\mathbf{I}$ periodically: $\mathbf{P}[n] \leftarrow \mathbf{P}[n] + \epsilon\mathbf{I}$. This ensures $\mathbf{P}$ stays away from singularity, at the cost of biasing the estimate toward zero.

**4. Reset.** Periodically re-initialise $\mathbf{P}$ using the current weight estimate and current input covariance estimate. Effective but causes transient degradation.

**Practical recommendation.** For most applications, double precision (64-bit) arithmetic combined with the standard symmetrising step provides adequate stability for $\lambda \geq 0.95$ and moderate filter orders ($N \leq 100$). For $N > 200$ or $\lambda < 0.95$, use a UD-factorised RLS.

---

## Tier 3: Advanced

### Q7. Derive the relationship between RLS and the Kalman filter. Under what model are they equivalent?

**Answer.**

**State-space formulation.** Consider the model:

$$\mathbf{w}[n] = \mathbf{w}[n-1] \quad \text{(state equation: system is time-invariant)}$$

$$d[n] = \mathbf{x}^T[n]\mathbf{w}[n] + v[n] \quad \text{(observation equation)}$$

where $v[n] \sim \mathcal{N}(0, \sigma_v^2)$ is observation noise.

This is a linear Gaussian state-space model with:
- State transition: $\mathbf{F} = \mathbf{I}$ (identity)
- Process noise covariance: $\mathbf{Q} = \mathbf{0}$ (no state noise for time-invariant system)
- Observation matrix: $\mathbf{H}[n] = \mathbf{x}^T[n]$
- Observation noise: $R[n] = \sigma_v^2$

**Kalman filter for this model:**

Prediction step ($\mathbf{Q} = 0$, $\mathbf{F} = \mathbf{I}$):
$$\hat{\mathbf{w}}^-[n] = \hat{\mathbf{w}}[n-1], \quad \mathbf{P}^-[n] = \mathbf{P}[n-1]$$

Update step:
$$\mathbf{K}[n] = \mathbf{P}^-[n]\mathbf{H}^T[n] \bigl(\mathbf{H}[n]\mathbf{P}^-[n]\mathbf{H}^T[n] + R[n]\bigr)^{-1}$$
$$= \frac{\mathbf{P}[n-1]\mathbf{x}[n]}{\mathbf{x}^T[n]\mathbf{P}[n-1]\mathbf{x}[n] + \sigma_v^2}$$

$$\hat{\mathbf{w}}[n] = \hat{\mathbf{w}}^-[n] + \mathbf{K}[n](d[n] - \mathbf{x}^T[n]\hat{\mathbf{w}}^-[n])$$

$$\mathbf{P}[n] = (\mathbf{I} - \mathbf{K}[n]\mathbf{H}[n])\mathbf{P}^-[n]$$

**Equivalence to RLS.** Setting $\lambda = 1$ and $\sigma_v^2 = 1$ in the Kalman update, and identifying $\mathbf{P}[n] \leftarrow \boldsymbol{\Phi}^{-1}[n]$, the Kalman gain matches the RLS Kalman gain exactly. The $\lambda < 1$ RLS corresponds to a Kalman filter where process noise $\mathbf{Q} = (1-\lambda)\lambda^{-1}\mathbf{P}^-[n]$ (scaled innovation covariance) models the time-varying system.

**Significance.** The Kalman filter is the MMSE estimator for linear Gaussian state-space models. RLS is optimal (in the Bayesian sense) for the linear time-invariant parameter estimation problem. The connection explains why RLS converges faster than LMS: it is using the optimal Bayesian update, while LMS uses only a gradient step.

---

### Q8. Describe the QR-decomposition-based RLS (QRD-RLS). What computational and numerical advantages does it offer?

**Answer.**

**Motivation.** Instead of propagating $\mathbf{P}[n] = \boldsymbol{\Phi}^{-1}[n]$ directly, QRD-RLS maintains the **square-root factor** of $\boldsymbol{\Phi}[n]$ via a sequence of Givens rotations. This preserves positive definiteness exactly (to machine precision) and improves numerical stability by $\sqrt{\kappa(\mathbf{R})}$ (the square root of the condition number).

**Data matrix formulation.** Define the weighted data matrix:

$$\mathbf{A}[n] = \begin{bmatrix} \lambda^{(n-1)/2}\mathbf{x}^T[1] \\ \lambda^{(n-2)/2}\mathbf{x}^T[2] \\ \vdots \\ \mathbf{x}^T[n] \end{bmatrix} \in \mathbb{R}^{n \times N}$$

Then $\boldsymbol{\Phi}[n] = \mathbf{A}^T[n]\mathbf{A}[n]$. The QR decomposition $\mathbf{A}[n] = \mathbf{Q}[n]\mathbf{R}[n]$ gives $\boldsymbol{\Phi}[n] = \mathbf{R}^T[n]\mathbf{R}[n]$, so $\mathbf{P}[n] = (\mathbf{R}^T[n]\mathbf{R}[n])^{-1}$.

**Recursive update via Givens rotation.** When a new row $\mathbf{x}^T[n]$ is appended:

$$\begin{bmatrix} \sqrt{\lambda}\mathbf{R}[n-1] \\ \mathbf{x}^T[n] \end{bmatrix} = \mathbf{Q}^T \mathbf{R}[n]$$

A single Givens rotation (or Householder reflection) can annihilate the new row, updating $\mathbf{R}[n]$ in $O(N^2)$ operations.

**Weight update.** The weight estimate $\hat{\mathbf{w}}[n]$ satisfies $\mathbf{R}[n]\hat{\mathbf{w}}[n] = \mathbf{b}[n]$ (upper triangular system), solvable by back-substitution in $O(N^2)$ operations (same as standard RLS).

**Advantages:**
1. **Numerical stability:** error in $\mathbf{R}[n]$ is $O(\epsilon_{\text{mach}})$; error in $\mathbf{P}[n]$ via standard RLS is $O(\epsilon_{\text{mach}} \cdot \kappa(\mathbf{R}))$. For ill-conditioned inputs, QRD-RLS can be orders of magnitude more accurate.
2. **VLSI-friendliness:** Givens rotations are local, regular operations suitable for systolic array implementations.
3. **Same complexity:** $O(N^2)$ per sample — same order as standard RLS.

---

## Quick Reference: RLS Algorithm Summary

```
Initialise: w[0] = 0, P[0] = delta_inv * I  (delta_inv large, e.g. 10^3)

For each sample n:
    xi[n] = d[n] - w^T[n-1] * x[n]           (a priori error)
    k[n] = P[n-1] * x[n] / (lambda + x^T[n] * P[n-1] * x[n])  (Kalman gain)
    w[n] = w[n-1] + k[n] * xi[n]              (weight update)
    P[n] = (P[n-1] - k[n] * x^T[n] * P[n-1]) / lambda  (covariance update)
```

| Quantity | Formula |
|---|---|
| Cost function | $J = \sum_k \lambda^{n-k} e^2[k]$ |
| Effective memory | $L_{\text{eff}} = 1/(1-\lambda)$ samples |
| Complexity per sample | $\approx 2.5N^2$ multiplications |
| Misadjustment | $\approx (1-\lambda)N$ |
| Convergence time | $\approx N$ samples (exact LS) |
| Forgetting factor range | $0.9 \leq \lambda \leq 0.9999$ typical |
| Initialisation | $\mathbf{P}[0] = \delta^{-1}\mathbf{I}$, $\delta \ll 1$ |
