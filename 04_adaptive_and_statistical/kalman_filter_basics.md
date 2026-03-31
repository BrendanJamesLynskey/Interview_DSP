# Kalman Filter Basics: Interview Questions

## Overview

The Kalman filter is the optimal recursive estimator for linear Gaussian state-space models. In DSP contexts, it appears in channel estimation, tracking, sensor fusion, and noise reduction. This file covers the standard (linear) Kalman filter and its extension to nonlinear systems; deeper statistical topics (UKF, particle filters) are beyond the current scope.

---

## Tier 1: Fundamentals

### Q1. What problem does the Kalman filter solve? State the state-space model.

**Answer.**

**Problem.** Estimate the hidden state $\mathbf{x}_n \in \mathbb{R}^m$ of a dynamical system from noisy observations $\mathbf{y}_n \in \mathbb{R}^p$, where both the system dynamics and observation model are linear.

**State-space model:**

$$\mathbf{x}_n = \mathbf{F}_n \mathbf{x}_{n-1} + \mathbf{G}_n \mathbf{u}_n + \mathbf{w}_n \quad \text{(state / process equation)}$$

$$\mathbf{y}_n = \mathbf{H}_n \mathbf{x}_n + \mathbf{v}_n \quad \text{(observation equation)}$$

where:
- $\mathbf{F}_n \in \mathbb{R}^{m \times m}$: state transition matrix (models system dynamics)
- $\mathbf{G}_n \mathbf{u}_n$: known control input (often omitted when $\mathbf{u}_n = 0$)
- $\mathbf{w}_n \sim \mathcal{N}(\mathbf{0}, \mathbf{Q}_n)$: process noise (models unmodelled dynamics)
- $\mathbf{H}_n \in \mathbb{R}^{p \times m}$: observation matrix
- $\mathbf{v}_n \sim \mathcal{N}(\mathbf{0}, \mathbf{R}_n)$: observation noise
- $\mathbf{w}_n$ and $\mathbf{v}_n$ are mutually uncorrelated and independent of the initial state $\mathbf{x}_0$

**What the Kalman filter computes.** At each time step $n$, the Kalman filter computes the conditional distribution:

$$p(\mathbf{x}_n \,|\, \mathbf{y}_1, \mathbf{y}_2, \ldots, \mathbf{y}_n) = \mathcal{N}(\hat{\mathbf{x}}_{n|n},\, \mathbf{P}_{n|n})$$

For linear Gaussian models, this conditional distribution is Gaussian and fully characterised by its mean $\hat{\mathbf{x}}_{n|n}$ (the MMSE estimate) and covariance $\mathbf{P}_{n|n}$.

---

### Q2. State the Kalman filter prediction and update equations.

**Answer.**

**Notation.** $\hat{\mathbf{x}}_{n|k}$ denotes the estimate of $\mathbf{x}_n$ given observations up to time $k$. $\mathbf{P}_{n|k}$ is the corresponding error covariance.

**Prediction step** (time update — propagate state forward):

$$\hat{\mathbf{x}}_{n|n-1} = \mathbf{F}_n \hat{\mathbf{x}}_{n-1|n-1}$$

$$\mathbf{P}_{n|n-1} = \mathbf{F}_n \mathbf{P}_{n-1|n-1} \mathbf{F}_n^T + \mathbf{Q}_n$$

**Innovation (measurement residual):**

$$\boldsymbol{\nu}_n = \mathbf{y}_n - \mathbf{H}_n \hat{\mathbf{x}}_{n|n-1}$$

**Innovation covariance:**

$$\mathbf{S}_n = \mathbf{H}_n \mathbf{P}_{n|n-1} \mathbf{H}_n^T + \mathbf{R}_n$$

**Kalman gain:**

$$\mathbf{K}_n = \mathbf{P}_{n|n-1} \mathbf{H}_n^T \mathbf{S}_n^{-1}$$

**Update step** (measurement update — incorporate observation):

$$\hat{\mathbf{x}}_{n|n} = \hat{\mathbf{x}}_{n|n-1} + \mathbf{K}_n \boldsymbol{\nu}_n$$

$$\mathbf{P}_{n|n} = (\mathbf{I} - \mathbf{K}_n \mathbf{H}_n) \mathbf{P}_{n|n-1}$$

**Initialisation:** $\hat{\mathbf{x}}_{0|0} = \mathbb{E}\{\mathbf{x}_0\}$, $\mathbf{P}_{0|0} = \text{Cov}(\mathbf{x}_0)$.

**Complexity per step:** $O(m^3)$ for the matrix operations (dominant cost is the $p \times p$ innovation covariance inversion $\mathbf{S}_n^{-1}$ — $O(p^3)$, and matrix multiplications — $O(m^2 p)$).

---

### Q3. What is the Kalman gain, and what does it represent physically?

**Answer.**

**The Kalman gain** $\mathbf{K}_n \in \mathbb{R}^{m \times p}$ determines how much weight to give the new measurement $\mathbf{y}_n$ versus the prediction $\hat{\mathbf{x}}_{n|n-1}$.

**Rewrite the update:**

$$\hat{\mathbf{x}}_{n|n} = \underbrace{(\mathbf{I} - \mathbf{K}_n\mathbf{H}_n)}_{\text{weight on prediction}} \hat{\mathbf{x}}_{n|n-1} + \underbrace{\mathbf{K}_n}_{\text{weight on measurement}} \mathbf{y}_n$$

**Extreme cases:**

- **$\mathbf{K}_n \to \mathbf{0}$:** Large measurement noise ($\mathbf{R}_n \to \infty$). The update ignores new measurements; the estimate is entirely based on the prediction. Prediction covariance dominates the innovation covariance: $\mathbf{S}_n \approx \mathbf{R}_n$, so $\mathbf{K}_n \approx \mathbf{P}_{n|n-1}\mathbf{H}_n^T \mathbf{R}_n^{-1} \to \mathbf{0}$.

- **$\mathbf{K}_n \to \mathbf{H}_n^{-1}$** (when square and invertible): Large process noise ($\mathbf{Q}_n \to \infty$). The prediction is unreliable; the update trusts the measurement completely. $\mathbf{P}_{n|n-1} \to \infty$, so $\mathbf{K}_n \to \mathbf{H}_n^{-1}$.

- **Optimal balance:** The Kalman gain balances process uncertainty $\mathbf{P}_{n|n-1}$ against measurement noise $\mathbf{R}_n$ optimally, minimising the trace of the updated covariance $\mathbf{P}_{n|n}$ (minimising the total estimation variance).

---

## Tier 2: Intermediate

### Q4. Derive the Joseph form of the covariance update and explain when it is preferred.

**Answer.**

**Standard form:**

$$\mathbf{P}_{n|n} = (\mathbf{I} - \mathbf{K}_n\mathbf{H}_n)\mathbf{P}_{n|n-1}$$

This is compact but numerically fragile: it relies on $\mathbf{K}_n$ being exactly the optimal Kalman gain. If $\mathbf{K}_n$ is computed with round-off error, the result may lose symmetry or positive definiteness.

**Joseph form (symmetric form):**

$$\mathbf{P}_{n|n} = (\mathbf{I} - \mathbf{K}_n\mathbf{H}_n)\mathbf{P}_{n|n-1}(\mathbf{I} - \mathbf{K}_n\mathbf{H}_n)^T + \mathbf{K}_n\mathbf{R}_n\mathbf{K}_n^T$$

**Derivation.** For any gain $\mathbf{K}_n$ (not necessarily optimal), the error covariance is:

$$\mathbf{P}_{n|n} = \mathbb{E}\{(\mathbf{x}_n - \hat{\mathbf{x}}_{n|n})(\mathbf{x}_n - \hat{\mathbf{x}}_{n|n})^T\}$$

Substitute $\hat{\mathbf{x}}_{n|n} = \hat{\mathbf{x}}_{n|n-1} + \mathbf{K}_n(\mathbf{y}_n - \mathbf{H}_n\hat{\mathbf{x}}_{n|n-1})$:

$$\mathbf{x}_n - \hat{\mathbf{x}}_{n|n} = (\mathbf{I}-\mathbf{K}_n\mathbf{H}_n)\tilde{\mathbf{x}}_{n|n-1} - \mathbf{K}_n\mathbf{v}_n$$

where $\tilde{\mathbf{x}}_{n|n-1} = \mathbf{x}_n - \hat{\mathbf{x}}_{n|n-1}$. Since $\tilde{\mathbf{x}}_{n|n-1}$ and $\mathbf{v}_n$ are uncorrelated:

$$\mathbf{P}_{n|n} = (\mathbf{I}-\mathbf{K}_n\mathbf{H}_n)\mathbf{P}_{n|n-1}(\mathbf{I}-\mathbf{K}_n\mathbf{H}_n)^T + \mathbf{K}_n\mathbf{R}_n\mathbf{K}_n^T$$

**When to use the Joseph form:**
1. When $\mathbf{K}_n$ is not computed exactly (sub-optimal gain, numerical approximations).
2. When numerical preservation of symmetry and positive definiteness is critical.
3. In embedded or fixed-point implementations where round-off accumulation is significant.

The cost is slightly higher (two extra matrix multiplications), but the symmetry is guaranteed by construction ($\mathbf{A}\mathbf{B}\mathbf{A}^T + \mathbf{C}\mathbf{C}^T$ is always symmetric positive semidefinite).

---

### Q5. How is the Kalman filter related to the Wiener filter? Under what conditions are they equivalent?

**Answer.**

**Relationship.** The Wiener filter and Kalman filter are both MMSE estimators for linear systems, but differ in scope:

| | Wiener Filter | Kalman Filter |
|---|---|---|
| **Stationarity** | Assumes WSS signals | Handles non-stationary, time-varying systems |
| **Model** | Input/output correlation (spectral) | State-space (explicit dynamics) |
| **Form** | Fixed (time-invariant) filter | Time-varying gain (converges to steady state) |
| **Solution** | Off-line (solve matrix equation) | Recursive (on-line update) |
| **Noise model** | Known PSD | Known covariance matrices $\mathbf{Q}$, $\mathbf{R}$ |

**Equivalence for stationary systems.** For a time-invariant state-space model ($\mathbf{F}, \mathbf{H}, \mathbf{Q}, \mathbf{R}$ constant), the Kalman gain converges to a steady-state value $\mathbf{K}_\infty$ as $n \to \infty$. The resulting steady-state Kalman filter is a **fixed linear filter** — identical to the Wiener filter designed for the same state-space model.

**Steady-state Kalman gain.** The steady-state covariance $\mathbf{P}_\infty$ satisfies the **Discrete Algebraic Riccati Equation (DARE)**:

$$\mathbf{P}_\infty = \mathbf{F}\!\left(\mathbf{P}_\infty - \mathbf{P}_\infty\mathbf{H}^T(\mathbf{H}\mathbf{P}_\infty\mathbf{H}^T + \mathbf{R})^{-1}\mathbf{H}\mathbf{P}_\infty\right)\!\mathbf{F}^T + \mathbf{Q}$$

And the steady-state gain:

$$\mathbf{K}_\infty = \mathbf{P}_\infty\mathbf{H}^T(\mathbf{H}\mathbf{P}_\infty\mathbf{H}^T + \mathbf{R})^{-1}$$

The steady-state Kalman filter is equivalent to the causal Wiener filter computed from the spectral characterisation of the same model.

---

### Q6. Describe three DSP applications of the Kalman filter and map each onto the state-space model.

**Answer.**

**Application 1: Tracking a moving signal phase (carrier phase tracking in communications)**

**State:** $\mathbf{x}_n = [\phi_n, \dot\phi_n]^T$ (phase and frequency offset)

**State equation** (constant-frequency model with jitter):

$$\begin{bmatrix} \phi_n \\ \dot\phi_n \end{bmatrix} = \begin{bmatrix} 1 & T \\ 0 & 1 \end{bmatrix} \begin{bmatrix} \phi_{n-1} \\ \dot\phi_{n-1} \end{bmatrix} + \mathbf{w}_n$$

**Observation:** $y_n = \angle r_n \cdot e^{-j\hat\phi_{n|n-1}} + v_n$ (phase error from decision-directed demodulation)

**Output:** Smooth phase estimate for coherent demodulation, replacing the PLL with an optimal linear tracker.

---

**Application 2: Channel estimation in OFDM (pilot-aided)**

Wireless multipath channels vary over time (Doppler). Model the channel tap $h_k[n]$ at delay $k$ as a first-order AR process:

**State:** $\mathbf{x}_n = [h_0[n], h_1[n], \ldots, h_{L-1}[n]]^T$ (channel impulse response)

**State equation:** $\mathbf{x}_n = a\mathbf{x}_{n-1} + \mathbf{w}_n$ where $a = J_0(2\pi f_D T_s)$ (AR coefficient from Jakes' model, $f_D$ = Doppler frequency)

**Observation (at pilot subcarriers):** $y_k = X_k h_k + v_k$ where $X_k$ is the known pilot symbol

The Kalman filter tracks the time-varying channel, outperforming least-squares estimation for fast-fading channels.

---

**Application 3: Noise reduction in speech (single-channel)**

Model the clean speech $s[n]$ as an AR process (estimated from the short-time spectrum):

**State:** $\mathbf{x}_n = [s[n], s[n-1], \ldots, s[n-p+1]]^T$ (AR state vector)

**State equation:** $s[n] = \sum_{k=1}^p a_k s[n-k] + u[n]$, so:

$$\mathbf{F} = \begin{bmatrix} a_1 & a_2 & \cdots & a_p \\ 1 & 0 & \cdots & 0 \\ & \ddots & & \vdots \\ 0 & & 1 & 0 \end{bmatrix}$$

**Observation:** $y[n] = s[n] + v[n]$, so $\mathbf{H} = [1, 0, \ldots, 0]$

The Kalman filter produces the MMSE estimate of the clean speech given noisy observations, adapting as the AR parameters change frame-by-frame (segmental Kalman smoother).

---

## Tier 3: Advanced

### Q7. What is the Extended Kalman Filter (EKF)? Describe its linearisation approach and limitations.

**Answer.**

**Motivation.** Many practical systems are nonlinear:

$$\mathbf{x}_n = \mathbf{f}(\mathbf{x}_{n-1}, \mathbf{w}_{n-1})$$
$$\mathbf{y}_n = \mathbf{h}(\mathbf{x}_n) + \mathbf{v}_n$$

The standard Kalman filter is not applicable. The EKF approximates the nonlinear functions by their first-order Taylor expansions around the current estimate.

**EKF linearisation.** Linearise about the predicted state $\hat{\mathbf{x}}_{n|n-1}$:

$$\mathbf{f}(\mathbf{x}) \approx \mathbf{f}(\hat{\mathbf{x}}_{n-1|n-1}) + \mathbf{F}_n (\mathbf{x} - \hat{\mathbf{x}}_{n-1|n-1})$$

$$\mathbf{h}(\mathbf{x}) \approx \mathbf{h}(\hat{\mathbf{x}}_{n|n-1}) + \mathbf{H}_n (\mathbf{x} - \hat{\mathbf{x}}_{n|n-1})$$

where $\mathbf{F}_n = \partial\mathbf{f}/\partial\mathbf{x}\big|_{\hat{\mathbf{x}}_{n-1|n-1}}$ and $\mathbf{H}_n = \partial\mathbf{h}/\partial\mathbf{x}\big|_{\hat{\mathbf{x}}_{n|n-1}}$ are Jacobian matrices.

The standard Kalman recursion is then applied with these time-varying linearised matrices.

**EKF prediction:**

$$\hat{\mathbf{x}}_{n|n-1} = \mathbf{f}(\hat{\mathbf{x}}_{n-1|n-1})$$

$$\mathbf{P}_{n|n-1} = \mathbf{F}_n\mathbf{P}_{n-1|n-1}\mathbf{F}_n^T + \mathbf{Q}_n$$

**EKF update:** Same as standard Kalman using the linearised $\mathbf{H}_n$.

**Limitations of EKF:**

1. **First-order approximation.** Ignores higher-order terms in the Taylor expansion. For highly nonlinear functions, the approximation is poor — particularly when the state uncertainty $\mathbf{P}$ is large.

2. **Not optimal.** The EKF is not the MMSE estimator for nonlinear models — it is a heuristic approximation.

3. **Jacobian computation.** Requires analytical expressions for $\partial\mathbf{f}/\partial\mathbf{x}$ and $\partial\mathbf{h}/\partial\mathbf{x}$, which may be complex to derive.

4. **Divergence risk.** If the linearisation error is large, the filter can diverge (predicted covariance underestimates true uncertainty, Kalman gain becomes too small, errors grow unbounded).

**Better alternatives:**
- **Unscented Kalman Filter (UKF):** Uses a set of sigma points to capture the nonlinear transformation of the distribution more accurately than first-order linearisation (accurate to third order for Gaussian distributions).
- **Particle filter:** Represents the posterior distribution with a set of samples (particles). Exact for any nonlinearity but computationally expensive — $O(N_{\text{particles}} \cdot \text{per-sample cost})$.

---

### Q8. Derive the DARE (Discrete Algebraic Riccati Equation) and explain its role in steady-state Kalman filter design.

**Answer.**

**Setup.** For a time-invariant system ($\mathbf{F}, \mathbf{H}, \mathbf{Q}, \mathbf{R}$ constant), the prediction error covariance $\mathbf{P}_{n|n-1}$ evolves according to the **Riccati difference equation**:

$$\mathbf{P}_{n+1|n} = \mathbf{F}\mathbf{P}_{n|n}\mathbf{F}^T + \mathbf{Q}$$

where $\mathbf{P}_{n|n} = (\mathbf{I} - \mathbf{K}_n\mathbf{H})\mathbf{P}_{n|n-1}$.

Substituting:

$$\mathbf{P}_{n+1|n} = \mathbf{F}\!\left(\mathbf{P}_{n|n-1} - \mathbf{P}_{n|n-1}\mathbf{H}^T(\mathbf{H}\mathbf{P}_{n|n-1}\mathbf{H}^T + \mathbf{R})^{-1}\mathbf{H}\mathbf{P}_{n|n-1}\right)\!\mathbf{F}^T + \mathbf{Q}$$

**Steady-state condition.** As $n \to \infty$, if the Riccati iteration converges (which it does when the system is detectable and stabilisable), $\mathbf{P}_{n+1|n} \to \mathbf{P}_\infty$ satisfying the **DARE**:

$$\mathbf{P}_\infty = \mathbf{F}\!\left(\mathbf{P}_\infty - \mathbf{P}_\infty\mathbf{H}^T(\mathbf{H}\mathbf{P}_\infty\mathbf{H}^T + \mathbf{R})^{-1}\mathbf{H}\mathbf{P}_\infty\right)\!\mathbf{F}^T + \mathbf{Q}$$

**Stabilisability and detectability conditions.** The DARE has a unique positive definite solution if:
- The pair $(\mathbf{F}, \mathbf{G})$ is stabilisable (where $\mathbf{Q} = \mathbf{G}\mathbf{G}^T$): all unstable modes of $\mathbf{F}$ are reachable.
- The pair $(\mathbf{F}, \mathbf{H})$ is detectable: all unstable modes of $\mathbf{F}$ are observable.

**Role in DSP system design.** Solving the DARE off-line (using Schur decomposition methods — $O(m^3)$) gives the steady-state Kalman gain:

$$\mathbf{K}_\infty = \mathbf{P}_\infty\mathbf{H}^T(\mathbf{H}\mathbf{P}_\infty\mathbf{H}^T + \mathbf{R})^{-1}$$

This steady-state gain can be **hard-coded** in a real-time implementation, avoiding the need to run the full Riccati recursion on-line. The result is a fixed linear filter equivalent to the Wiener filter — but derived from the physical state-space model rather than spectral data. This approach is standard in GNSS receivers, radar trackers, and channel equaliser designs.

---

## Quick Reference: Kalman Filter Summary

**Standard Kalman Filter (per step $n$):**

```
Predict:
  x_hat_prior = F * x_hat_posterior   (predicted state)
  P_prior = F * P_post * F^T + Q      (predicted covariance)

Update:
  nu = y - H * x_hat_prior            (innovation)
  S = H * P_prior * H^T + R           (innovation covariance)
  K = P_prior * H^T * inv(S)          (Kalman gain)
  x_hat_post = x_hat_prior + K * nu   (updated state)
  P_post = (I - K*H) * P_prior        (updated covariance)
```

| Quantity | Meaning |
|---|---|
| $\mathbf{F}$ | State transition matrix |
| $\mathbf{H}$ | Observation matrix |
| $\mathbf{Q}$ | Process noise covariance |
| $\mathbf{R}$ | Observation noise covariance |
| $\mathbf{K}_n$ | Kalman gain (balances prediction vs. measurement) |
| $\mathbf{P}_{n\|n}$ | Posterior error covariance |
| DARE | Steady-state Riccati equation for time-invariant systems |
| EKF | First-order Taylor linearisation for nonlinear systems |
| Complexity | $O(m^3 + m^2 p + p^3)$ per step |
