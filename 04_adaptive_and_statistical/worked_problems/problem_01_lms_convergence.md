# Worked Problem 01: LMS Convergence Analysis

## Problem Statement

A system identification problem is set up as follows:

- **Unknown system:** $\mathbf{w}_o = [0.5, -0.3, 0.8]^T$ (3-tap FIR filter, $N = 3$)
- **Input signal:** $x[n]$ is a zero-mean AR(1) process: $x[n] = 0.8x[n-1] + u[n]$ where $u[n] \sim \mathcal{N}(0, 1)$
- **Noise:** $v[n] \sim \mathcal{N}(0, \sigma_v^2 = 0.01)$, independent of $x[n]$
- **Desired signal:** $d[n] = \mathbf{w}_o^T \mathbf{x}[n] + v[n]$
- **Initial weights:** $\mathbf{w}[0] = \mathbf{0}$

**Tasks:**

1. Compute the autocorrelation matrix $\mathbf{R}$ of the input regressor $\mathbf{x}[n]$.
2. Find the eigenvalues of $\mathbf{R}$ and determine the step-size bounds for LMS convergence.
3. Compute the misadjustment for $\mu = 0.02$ and $\mu = 0.1$.
4. Estimate the convergence time constant for each step size.
5. Verify the theoretical results with a Python simulation and plot the learning curve.

---

## Part 1: Autocorrelation Matrix

**Autocorrelation of AR(1) process.** For $x[n] = 0.8 x[n-1] + u[n]$ with $\sigma_u^2 = 1$:

Input variance: $\sigma_x^2 = \frac{\sigma_u^2}{1 - a^2} = \frac{1}{1 - 0.64} = \frac{1}{0.36} \approx 2.778$

Autocorrelation: $R_x[k] = \sigma_x^2 \cdot a^{|k|} = 2.778 \times 0.8^{|k|}$

For $N = 3$ taps, the autocorrelation matrix $\mathbf{R} = \mathbb{E}\{\mathbf{x}[n]\mathbf{x}^T[n]\}$:

$$\mathbf{R} = \begin{bmatrix} R_x[0] & R_x[1] & R_x[2] \\ R_x[1] & R_x[0] & R_x[1] \\ R_x[2] & R_x[1] & R_x[0] \end{bmatrix} = \begin{bmatrix} 2.778 & 2.222 & 1.778 \\ 2.222 & 2.778 & 2.222 \\ 1.778 & 2.222 & 2.778 \end{bmatrix}$$

Using exact fractions: $R_x[0] = 25/9$, $R_x[1] = 20/9$, $R_x[2] = 16/9$.

**Trace:** $\text{tr}(\mathbf{R}) = 3 \times 25/9 = 25/3 \approx 8.333$

---

## Part 2: Eigenvalues and Step-Size Bounds

**Eigenvalues of $\mathbf{R}$.** Since $\mathbf{R}$ is a $3 \times 3$ symmetric Toeplitz matrix, eigenvalues are found analytically or numerically.

The characteristic polynomial $\det(\mathbf{R} - \lambda\mathbf{I}) = 0$:

$$\mathbf{R} - \lambda\mathbf{I} = \begin{bmatrix} 2.778-\lambda & 2.222 & 1.778 \\ 2.222 & 2.778-\lambda & 2.222 \\ 1.778 & 2.222 & 2.778-\lambda \end{bmatrix}$$

**Note: this matrix has the persymmetric property** ($R$ is symmetric and also centro-symmetric), enabling simplification. The eigenvectors are either symmetric or antisymmetric about the centre.

**Numerical values** (computed via characteristic polynomial or direct numerical method):

$$\lambda_1 \approx 7.347, \quad \lambda_2 = 2.778 - \frac{20}{9} = 0.556, \quad \lambda_3 \approx 0.430$$

**Verification:** $\lambda_1 + \lambda_2 + \lambda_3 \approx 7.347 + 0.556 + 0.430 = 8.333 = \text{tr}(\mathbf{R})$ \checkmark

Let us derive these more carefully. For a $3\times3$ Toeplitz matrix with elements $a = R_x[0]$, $b = R_x[1]$, $c = R_x[2]$:

$$\mathbf{R} = \begin{bmatrix} a & b & c \\ b & a & b \\ c & b & a \end{bmatrix}$$

One eigenvector is $\mathbf{v} = [1, 0, -1]^T$ (antisymmetric):

$$\mathbf{R}\mathbf{v} = \begin{bmatrix} a-c \\ 0 \\ c-a \end{bmatrix} = (a-c)[1, 0, -1]^T$$

$$\Rightarrow \lambda_2 = a - c = R_x[0] - R_x[2] = 25/9 - 16/9 = 1 \quad \text{(exact)}$$

The symmetric eigenspace ($\mathbf{v} = [\alpha, 1, \alpha]^T$):

$$\mathbf{R}[\alpha, 1, \alpha]^T = [(a\alpha + b + c\alpha), (b\alpha + a + b\alpha), (c\alpha + b + a\alpha)]^T = \lambda[\alpha, 1, \alpha]^T$$

From the middle component: $(2b\alpha + a) = \lambda$, so $\lambda = 2b\alpha + a$.

From the outer component: $(a+c)\alpha + b = \lambda\alpha = (2b\alpha + a)\alpha$:

$(a+c)\alpha + b = 2b\alpha^2 + a\alpha$

$2b\alpha^2 + (a - a - c)\alpha - b = 0$

$2b\alpha^2 - c\alpha - b = 0$

$\alpha = \frac{c \pm \sqrt{c^2 + 8b^2}}{4b}$

With $b = 20/9$ and $c = 16/9$:

$c^2 + 8b^2 = (16/9)^2 + 8(20/9)^2 = \frac{256 + 3200}{81} = \frac{3456}{81}$

$\sqrt{c^2 + 8b^2} = \frac{\sqrt{3456}}{9} = \frac{24\sqrt{6}}{9} = \frac{8\sqrt{6}}{3}$

$\alpha_\pm = \frac{16/9 \pm 8\sqrt{6}/3}{4 \times 20/9} = \frac{16/9 \pm 24\sqrt{6}/9}{80/9} = \frac{16 \pm 24\sqrt{6}}{80} = \frac{2 \pm 3\sqrt{6}}{10}$

For $\alpha_+ = (2 + 3\sqrt{6})/10 \approx (2 + 7.35)/10 \approx 0.935$:

$\lambda_1 = 2(20/9)(0.935) + 25/9 \approx 4.156 + 2.778 \approx 6.934$

For $\alpha_- = (2 - 3\sqrt{6})/10 \approx (2 - 7.35)/10 \approx -0.535$:

$\lambda_3 = 2(20/9)(-0.535) + 25/9 \approx -2.378 + 2.778 \approx 0.400$

**Summary of eigenvalues (numerical):**

$$\lambda_{\max} = \lambda_1 \approx 6.934, \quad \lambda_2 = 1.000, \quad \lambda_{\min} = \lambda_3 \approx 0.400$$

**Eigenvalue spread:** $\chi = \lambda_{\max}/\lambda_{\min} \approx 6.934/0.400 \approx 17.3$

**Condition number interpretation:** The AR(1) process with $a = 0.8$ produces a moderately ill-conditioned input matrix ($\chi \approx 17$). Higher $a$ would give worse conditioning.

**Step-size bounds for LMS convergence:**

$$0 < \mu < \frac{2}{\lambda_{\max}} = \frac{2}{6.934} \approx 0.288$$

**Practical step-size (10% rule):**

$$\mu_{\text{safe}} \approx \frac{0.1}{N\sigma_x^2} = \frac{0.1}{3 \times 2.778} \approx 0.012$$

---

## Part 3: Misadjustment Computation

**Misadjustment formula:**

$$\mathcal{M} \approx \frac{\mu \,\text{tr}(\mathbf{R})}{2} = \frac{\mu \times 8.333}{2} = 4.167\mu$$

For $\mu = 0.02$:

$$\mathcal{M}_{0.02} = 4.167 \times 0.02 = 0.0833 \quad (8.3\%)$$

$$J_\infty = J_{\min}(1 + \mathcal{M}) = 0.01 \times 1.0833 = 0.01083$$

For $\mu = 0.1$:

$$\mathcal{M}_{0.1} = 4.167 \times 0.1 = 0.4167 \quad (41.7\%)$$

$$J_\infty = 0.01 \times 1.4167 = 0.01417$$

**Interpretation.** At $\mu = 0.1$, the steady-state MSE is 41.7% above the minimum achievable MSE $J_{\min} = \sigma_v^2 = 0.01$. This is a significant degradation. For a system identification task requiring high accuracy, $\mu = 0.02$ is preferable.

**More precise misadjustment** (from energy conservation derivation):

$$\mathcal{M} = \frac{\mu\,\text{tr}(\mathbf{R})}{2 - \mu\,\text{tr}(\mathbf{R})}$$

For $\mu = 0.1$: $\mathcal{M} = (0.1 \times 8.333)/(2 - 0.833) = 0.833/1.167 = 0.714$ (71.4%) — the simplified formula underestimates misadjustment significantly for larger $\mu$.

---

## Part 4: Convergence Time Constants

**Time constant for mode $k$:**

$$\tau_k \approx \frac{1}{2\mu\lambda_k} \quad \text{(samples)}$$

**For $\mu = 0.02$:**

| Mode | $\lambda_k$ | $\tau_k$ (samples) |
|:-:|:-:|:-:|
| 1 (fastest) | 6.934 | $1/(2 \times 0.02 \times 6.934) \approx 3.6$ |
| 2 | 1.000 | $1/(2 \times 0.02 \times 1.000) = 25.0$ |
| 3 (slowest) | 0.400 | $1/(2 \times 0.02 \times 0.400) = 62.5$ |

**For $\mu = 0.1$:**

| Mode | $\lambda_k$ | $\tau_k$ (samples) |
|:-:|:-:|:-:|
| 1 | 6.934 | $0.72$ |
| 2 | 1.000 | $5.0$ |
| 3 | 0.400 | $12.5$ |

**Practical convergence time** (to within $1\%$ of steady state, $\approx 5\tau_{\max}$):

- $\mu = 0.02$: approximately $5 \times 62.5 = 312$ samples
- $\mu = 0.1$: approximately $5 \times 12.5 = 63$ samples, but with higher misadjustment

**Eigenvalue spread effect.** The ratio $\tau_3/\tau_1 = \lambda_1/\lambda_3 = \chi = 17.3$. The slowest mode takes 17 times longer to converge than the fastest. A condition number of 17 is moderate — speech signals can give $\chi > 100$.

---

## Part 5: Python Simulation and Learning Curve

```python
import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
np.random.seed(42)
N_filter = 3         # filter length
N_samples = 3000     # total samples
N_trials = 500       # Monte Carlo trials for ensemble averaging
w_o = np.array([0.5, -0.3, 0.8])  # true system
sigma_v2 = 0.01                     # noise variance
a_ar = 0.8                          # AR coefficient
sigma_u2 = 1.0
sigma_x2 = sigma_u2 / (1 - a_ar**2)  # input variance = 1/0.36 ≈ 2.778

# Theoretical values
R_trace = 3 * sigma_x2  # tr(R) ≈ 8.333
J_min = sigma_v2         # minimum MSE
# Eigenvalues (computed above)
lam = np.array([6.934, 1.000, 0.400])
lam_max = lam.max()

# --- Step sizes to test ---
mu_list = [0.02, 0.1]
colors = ['blue', 'red']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for mu, color in zip(mu_list, colors):
    M_theory = mu * R_trace / (2 - mu * R_trace)
    tau_slow = 1.0 / (2 * mu * lam.min())
    print(f"\nmu = {mu}")
    print(f"  Stability limit: mu < {2/lam_max:.4f}")
    print(f"  Misadjustment (approx): {mu*R_trace/2:.4f}")
    print(f"  Misadjustment (exact):  {M_theory:.4f}")
    print(f"  Slowest time const:     {tau_slow:.1f} samples")
    print(f"  J_inf = {J_min*(1+M_theory):.6f}")

    # Monte Carlo learning curve
    MSE_ensemble = np.zeros(N_samples)
    for trial in range(N_trials):
        x_prev = 0.0
        x_buf = np.zeros(N_filter)
        w = np.zeros(N_filter)
        mse_trial = np.zeros(N_samples)

        for n in range(N_samples):
            # Generate AR(1) input sample
            u = np.random.normal(0, np.sqrt(sigma_u2))
            x_new = a_ar * x_prev + u
            x_prev = x_new

            # Update input regressor (newest sample first)
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x_new

            # Desired signal
            noise = np.random.normal(0, np.sqrt(sigma_v2))
            d = w_o @ x_buf + noise

            # LMS output and error
            y = w @ x_buf
            e = d - y

            # Record squared error (proxy for MSE)
            mse_trial[n] = e**2

            # LMS weight update
            w = w + mu * e * x_buf

        MSE_ensemble += mse_trial

    MSE_ensemble /= N_trials  # ensemble average

    # --- Plot ---
    ax = axes[0] if mu == 0.02 else axes[1]
    ax.semilogy(MSE_ensemble, alpha=0.8, color=color, linewidth=0.8,
                label='Simulated MSE')
    ax.axhline(J_min * (1 + M_theory), color='black', linestyle='--',
               label=f'$J_\\infty$ = {J_min*(1+M_theory):.5f}')
    ax.axhline(J_min, color='green', linestyle=':', label=f'$J_{{\\min}}$ = {J_min}')
    ax.set_xlabel('Sample index $n$')
    ax.set_ylabel('MSE (log scale)')
    ax.set_title(f'LMS Learning Curve, $\\mu = {mu}$\n'
                 f'Misadjustment = {M_theory:.3f}, $\\tau_{{slow}}$ = {tau_slow:.1f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, N_samples])
    ax.set_ylim([J_min * 0.5, J_min * 10])

plt.tight_layout()
plt.savefig('lms_learning_curve.png', dpi=150)
plt.show()
```

**Expected console output:**

```
mu = 0.02
  Stability limit: mu < 0.2884
  Misadjustment (approx): 0.0833
  Misadjustment (exact):  0.0909
  Slowest time const:     62.5 samples
  J_inf = 0.010909

mu = 0.1
  Stability limit: mu < 0.2884
  Misadjustment (approx): 0.4167
  Misadjustment (exact):  0.7143
  Slowest time const:     12.5 samples
  J_inf = 0.017143
```

---

## Summary of Results

| Parameter | $\mu = 0.02$ | $\mu = 0.1$ |
|---|:-:|:-:|
| Stability satisfied? | Yes ($0.02 < 0.288$) | Yes ($0.1 < 0.288$) |
| Misadjustment (approx.) | 8.3% | 41.7% |
| Misadjustment (exact) | 9.1% | 71.4% |
| Slowest time constant $\tau_{\max}$ | 62.5 samples | 12.5 samples |
| Convergence time ($5\tau$) | ~312 samples | ~63 samples |
| Steady-state MSE $J_\infty$ | 0.01091 | 0.01714 |

**Key findings:**

1. The eigenvalue spread $\chi \approx 17.3$ of the AR(1) input means the slowest mode converges 17 times slower than the fastest.

2. A 5x increase in $\mu$ (from 0.02 to 0.1) gives 5x faster convergence but at the cost of a 7x larger misadjustment (nonlinear due to the denominator in the exact formula).

3. The practical step-size range for this problem is approximately $\mu \in [0.005, 0.028]$: below 0.005 convergence is too slow for most applications; above 0.028 misadjustment exceeds 10%.

4. NLMS with $\tilde\mu = 0.1$ would achieve convergence in $\approx 12.5$ samples with misadjustment $\approx \tilde\mu N/2 = 0.15 = 15\%$, normalised automatically to the input power.
