# Worked Problem: Solving the Wiener-Hopf Equation for a 3-Tap FIR Filter

## Problem Statement

You are designing a 3-tap Wiener filter to estimate a desired signal $d(n)$ from
an observed signal $x(n)$.

Measurements have yielded the following:

**Autocorrelation matrix** $\mathbf{R}_{xx}$ of the input:

$$
\mathbf{R}_{xx} =
\begin{bmatrix}
1.00 & 0.50 & 0.25 \\
0.50 & 1.00 & 0.50 \\
0.25 & 0.50 & 1.00
\end{bmatrix}
$$

**Cross-correlation vector** $\mathbf{r}_{xd}$ between the input and the desired signal:

$$
\mathbf{r}_{xd} =
\begin{bmatrix}
0.90 \\ 0.50 \\ 0.25
\end{bmatrix}
$$

**Desired signal power** $\sigma_d^2 = 1.00$.

Tasks:

1. Solve the Wiener-Hopf equation $\mathbf{R}_{xx}\,\mathbf{w}_\text{opt} = \mathbf{r}_{xd}$ to find
   the optimal coefficient vector $\mathbf{w}_\text{opt}$.
2. Compute the minimum mean-squared error (MMSE):
   $J_\text{min} = \sigma_d^2 - \mathbf{r}_{xd}^H \mathbf{w}_\text{opt}$.
3. Verify your answer by checking that $\mathbf{R}_{xx}\mathbf{w}_\text{opt} = \mathbf{r}_{xd}$.

---

## Background: Why the Wiener-Hopf Equation?

The Wiener filter minimises the mean-squared error (MSE) between its output
$y(n) = \mathbf{w}^H \mathbf{x}(n)$ and the desired signal $d(n)$.

Expanding the MSE:

$$
J(\mathbf{w}) = E\bigl[|d(n) - \mathbf{w}^H \mathbf{x}(n)|^2\bigr]
             = \sigma_d^2 - \mathbf{w}^H \mathbf{r}_{xd} - \mathbf{r}_{xd}^H \mathbf{w}
             + \mathbf{w}^H \mathbf{R}_{xx} \mathbf{w}
$$

Setting $\nabla_{\mathbf{w}} J = 0$ (principle of orthogonality) yields the
**Wiener-Hopf equation**:

$$
\boxed{\mathbf{R}_{xx}\,\mathbf{w}_\text{opt} = \mathbf{r}_{xd}}
$$

The MSE at the optimal point simplifies to:

$$
J_\text{min} = \sigma_d^2 - \mathbf{r}_{xd}^H \mathbf{w}_\text{opt}
$$

This is because at the optimum the error is orthogonal to every input sample,
so the cross-terms reduce to a single quadratic expression.

---

## Step 1: Compute $\mathbf{R}_{xx}^{-1}$ via Cofactor Expansion

The solution is $\mathbf{w}_\text{opt} = \mathbf{R}_{xx}^{-1}\,\mathbf{r}_{xd}$.

Let

$$
\mathbf{R} =
\begin{bmatrix}
1    & 0.5  & 0.25 \\
0.5  & 1    & 0.5  \\
0.25 & 0.5  & 1
\end{bmatrix}
$$

### 1a. Determinant of $\mathbf{R}$

Expanding along the first row:

$$
\det(\mathbf{R}) = 1 \cdot
\begin{vmatrix} 1 & 0.5 \\ 0.5 & 1 \end{vmatrix}
- 0.5 \cdot
\begin{vmatrix} 0.5 & 0.5 \\ 0.25 & 1 \end{vmatrix}
+ 0.25 \cdot
\begin{vmatrix} 0.5 & 1 \\ 0.25 & 0.5 \end{vmatrix}
$$

Computing each $2\times 2$ minor:

$$
M_{11} = (1)(1) - (0.5)(0.5) = 1 - 0.25 = 0.75
$$

$$
M_{12} = (0.5)(1) - (0.5)(0.25) = 0.50 - 0.125 = 0.375
$$

$$
M_{13} = (0.5)(0.5) - (1)(0.25) = 0.25 - 0.25 = 0
$$

Therefore:

$$
\det(\mathbf{R}) = 1(0.75) - 0.5(0.375) + 0.25(0) = 0.75 - 0.1875 = 0.5625
$$

### 1b. Cofactor Matrix

The cofactor $C_{ij} = (-1)^{i+j} M_{ij}$ where $M_{ij}$ is the minor obtained
by deleting row $i$ and column $j$.

$$
C_{11} = +\begin{vmatrix}1&0.5\\0.5&1\end{vmatrix} = 0.75
\qquad
C_{12} = -\begin{vmatrix}0.5&0.5\\0.25&1\end{vmatrix} = -(0.5-0.125) = -0.375
\qquad
C_{13} = +\begin{vmatrix}0.5&1\\0.25&0.5\end{vmatrix} = (0.25-0.25) = 0
$$

$$
C_{21} = -\begin{vmatrix}0.5&0.25\\0.5&1\end{vmatrix} = -(0.5-0.125) = -0.375
\qquad
C_{22} = +\begin{vmatrix}1&0.25\\0.25&1\end{vmatrix} = (1-0.0625) = 0.9375
\qquad
C_{23} = -\begin{vmatrix}1&0.5\\0.25&0.5\end{vmatrix} = -(0.5-0.125) = -0.375
$$

$$
C_{31} = +\begin{vmatrix}0.5&0.25\\1&0.5\end{vmatrix} = (0.25-0.25) = 0
\qquad
C_{32} = -\begin{vmatrix}1&0.25\\0.5&0.5\end{vmatrix} = -(0.5-0.125) = -0.375
\qquad
C_{33} = +\begin{vmatrix}1&0.5\\0.5&1\end{vmatrix} = 0.75
$$

The adjugate (transpose of the cofactor matrix, noting $\mathbf{R}$ is symmetric
so the cofactor matrix is already symmetric here):

$$
\text{adj}(\mathbf{R}) =
\begin{bmatrix}
 0.75   & -0.375 &  0      \\
-0.375  &  0.9375 & -0.375 \\
 0      & -0.375 &  0.75
\end{bmatrix}
$$

### 1c. Inverse

$$
\mathbf{R}^{-1} = \frac{1}{\det(\mathbf{R})} \cdot \text{adj}(\mathbf{R})
= \frac{1}{0.5625}
\begin{bmatrix}
 0.75   & -0.375 &  0      \\
-0.375  &  0.9375 & -0.375 \\
 0      & -0.375 &  0.75
\end{bmatrix}
$$

$$
\mathbf{R}^{-1} =
\begin{bmatrix}
 1.\overline{3}   & -0.\overline{6}  &  0               \\
-0.\overline{6}   &  1.\overline{6}  & -0.\overline{6}  \\
 0                & -0.\overline{6}  &  1.\overline{3}
\end{bmatrix}
\approx
\begin{bmatrix}
 1.3333 & -0.6667 &  0      \\
-0.6667 &  1.6667 & -0.6667 \\
 0      & -0.6667 &  1.3333
\end{bmatrix}
$$

**Physical interpretation:** the inverse of a Toeplitz autocorrelation matrix is
itself nearly Toeplitz and tridiagonal-dominated -- neighbouring samples are the
most correlated, so the inverse "whitens" by differencing.

---

## Step 2: Compute $\mathbf{w}_\text{opt} = \mathbf{R}^{-1}\,\mathbf{r}_{xd}$

$$
\mathbf{w}_\text{opt} =
\begin{bmatrix}
 1.3333 & -0.6667 &  0      \\
-0.6667 &  1.6667 & -0.6667 \\
 0      & -0.6667 &  1.3333
\end{bmatrix}
\begin{bmatrix}
0.90 \\ 0.50 \\ 0.25
\end{bmatrix}
$$

Carrying out the matrix-vector multiplication row by row:

**Row 1:**

$$
w_0 = (1.3333)(0.90) + (-0.6667)(0.50) + (0)(0.25)
    = 1.2000 - 0.3333 + 0
    = 0.8\overline{6}
$$

**Row 2:**

$$
w_1 = (-0.6667)(0.90) + (1.6667)(0.50) + (-0.6667)(0.25)
    = -0.6000 + 0.8333 - 0.1667
    = 0.0\overline{6}
$$

**Row 3:**

$$
w_2 = (0)(0.90) + (-0.6667)(0.50) + (1.3333)(0.25)
    = 0 - 0.3333 + 0.3333
    = 0
$$

$$
\boxed{
\mathbf{w}_\text{opt} =
\begin{bmatrix}
0.8\overline{6} \\ 0.0\overline{6} \\ 0
\end{bmatrix}
\approx
\begin{bmatrix}
0.8667 \\ 0.0667 \\ 0.0000
\end{bmatrix}
}
$$

**Interpretation:** The third tap is zero, meaning the signal one step further
back in time carries no additional predictive power once $x(n)$ and $x(n-1)$
are already used. This makes sense given the rapid decay of the autocorrelation
(AR(1)-like process with coefficient $\approx 0.5$).

---

## Step 3: Compute the Minimum MSE

$$
J_\text{min} = \sigma_d^2 - \mathbf{r}_{xd}^H \mathbf{w}_\text{opt}
$$

Since all quantities are real:

$$
\mathbf{r}_{xd}^T \mathbf{w}_\text{opt}
= (0.90)(0.8\overline{6}) + (0.50)(0.0\overline{6}) + (0.25)(0)
= 0.78 + 0.0\overline{3} + 0
= 0.81\overline{3}
$$

More precisely in fractions: $w_0 = 13/15$, $w_1 = 1/15$, $w_2 = 0$.

$$
\mathbf{r}_{xd}^T \mathbf{w}_\text{opt}
= \frac{9}{10}\cdot\frac{13}{15} + \frac{1}{2}\cdot\frac{1}{15}
= \frac{117}{150} + \frac{1}{30}
= \frac{117}{150} + \frac{5}{150}
= \frac{122}{150} = \frac{61}{75}
$$

$$
J_\text{min} = 1 - \frac{61}{75} = \frac{14}{75} \approx 0.18\overline{6}
$$

$$
\boxed{J_\text{min} \approx 0.1867}
$$

This means the optimal filter explains approximately $81.3\%$ of the desired
signal's variance ($R^2 \approx 1 - J_\text{min}/\sigma_d^2 = 0.813$).

---

## Step 4: Verification

Check that $\mathbf{R}_{xx}\,\mathbf{w}_\text{opt} = \mathbf{r}_{xd}$:

$$
\begin{bmatrix}
1 & 0.5 & 0.25 \\
0.5 & 1 & 0.5 \\
0.25 & 0.5 & 1
\end{bmatrix}
\begin{bmatrix}
13/15 \\ 1/15 \\ 0
\end{bmatrix}
=
\begin{bmatrix}
13/15 + 0.5/15 + 0 \\
6.5/15 + 1/15 + 0 \\
3.25/15 + 0.5/15 + 0
\end{bmatrix}
=
\begin{bmatrix}
13.5/15 \\
7.5/15  \\
3.75/15
\end{bmatrix}
=
\begin{bmatrix}
0.90 \\ 0.50 \\ 0.25
\end{bmatrix}
= \mathbf{r}_{xd} \checkmark
$$

---

## Numerical Verification (Python)

```python
import numpy as np

R_xx = np.array([
    [1.00, 0.50, 0.25],
    [0.50, 1.00, 0.50],
    [0.25, 0.50, 1.00]
])

r_xd   = np.array([0.90, 0.50, 0.25])
sigma_d_sq = 1.00

# Solve via numpy (uses LAPACK's gesv -- stable LU decomposition)
w_opt = np.linalg.solve(R_xx, r_xd)
J_min = sigma_d_sq - r_xd @ w_opt

print("Optimal weights:", w_opt)
# -> [0.86667, 0.06667, 0.00000]

print("Minimum MSE:   ", J_min)
# -> 0.18667

# Residual (should be ~machine epsilon)
residual = np.linalg.norm(R_xx @ w_opt - r_xd)
print("Residual norm: ", residual)
# -> ~2.8e-16
```

Expected output:

```
Optimal weights: [0.86666667 0.06666667 0.        ]
Minimum MSE:     0.18666666666666682
Residual norm:   2.7755575615628914e-16
```

---

## Common Interview Follow-Up Questions

### Q1: Why must $\mathbf{R}_{xx}$ be positive definite for the Wiener solution to exist?

$\mathbf{R}_{xx}$ is the expected outer product $E[\mathbf{x}\mathbf{x}^H]$, which is always
positive semi-definite. It is strictly positive definite when the input samples
are linearly independent (no deterministic component). Positive definiteness
guarantees a unique inverse and therefore a unique global minimum for $J(\mathbf{w})$,
which is a quadratic bowl with no flat directions.

### Q2: What happens to $J_\text{min}$ as the number of taps increases?

$J_\text{min}$ is non-increasing in the number of taps. Adding a tap can only
maintain or improve performance because the optimal solution can always set the
new coefficient to zero and replicate the previous solution. In practice,
diminishing returns appear quickly once the filter length exceeds the
correlation length of the input.

### Q3: How does the condition number of $\mathbf{R}_{xx}$ affect the LMS algorithm?

The LMS step size $\mu$ must satisfy $0 < \mu < 2/\lambda_\text{max}$ for
convergence, where $\lambda_\text{max}$ is the largest eigenvalue of $\mathbf{R}_{xx}$.
A large condition number $\kappa = \lambda_\text{max}/\lambda_\text{min}$ means
different modes converge at vastly different rates (the slowest mode converges
as $|1 - 2\mu\lambda_\text{min}|^n$). This motivates normalised LMS (NLMS) or
RLS, which are condition-number independent.

### Q4: What is the Wiener filter's connection to linear MMSE (LMMSE) estimation?

The Wiener filter IS the LMMSE estimator restricted to a finite-impulse-response
(FIR) structure. The Wiener-Hopf equation is the first-order optimality condition
(stationarity of the Lagrangian) for the constrained LMMSE problem. Without the
FIR constraint, the optimal linear estimator is the Wiener filter in the
frequency domain: $H(\omega) = S_{xd}(\omega)/S_{xx}(\omega)$.
