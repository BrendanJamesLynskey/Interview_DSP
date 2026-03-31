# Worked Problem 03: Circular Convolution

**Subject:** Digital Signal Processing
**Topic:** Circular Convolution, Linear vs Circular, Zero-Padding
**Difficulty:** Intermediate

---

## Problem Statement

Let $x[n] = \{1, 2, 3, 4\}$ (indices $n = 0, 1, 2, 3$) and $h[n] = \{1, 1, 0, 0\}$ (indices $n = 0, 1, 2, 3$).

**(a)** Compute the **4-point circular convolution** $y_c[n] = x[n] \circledast_4 h[n]$ by the matrix method (wrap-around).

**(b)** Compute the **linear convolution** $y_l[n] = x[n] * h[n]$.

**(c)** Show analytically why $y_c \neq y_l$ in this case, and identify the time-domain aliasing.

**(d)** Zero-pad $x[n]$ and $h[n]$ to length $N = 7$ (or the next sufficient length) and show that the $N$-point circular convolution then equals the linear convolution.

**(e)** Verify part (d) using the DFT-based method: $y_l[n] = \text{IDFT}\{X[k] \cdot H[k]\}$.

---

## Part (a): 4-Point Circular Convolution (Matrix Method)

The $N$-point circular convolution is:

$$y_c[n] = \sum_{k=0}^{N-1} x[k]\,h[\langle n-k \rangle_N], \quad n = 0, 1, \ldots, N-1$$

The **circular shift matrix** for $h[n] = \{1, 1, 0, 0\}$ with $N = 4$:

Each row $n$ is $h$ circularly shifted by $n$:

$$\mathbf{H}_{circ} = \begin{pmatrix}
h[0] & h[3] & h[2] & h[1] \\
h[1] & h[0] & h[3] & h[2] \\
h[2] & h[1] & h[0] & h[3] \\
h[3] & h[2] & h[1] & h[0]
\end{pmatrix} = \begin{pmatrix}
1 & 0 & 0 & 1 \\
1 & 1 & 0 & 0 \\
0 & 1 & 1 & 0 \\
0 & 0 & 1 & 1
\end{pmatrix}$$

Each entry $\mathbf{H}_{circ}[n,k] = h[\langle n-k \rangle_4]$.

$$\mathbf{y}_c = \mathbf{H}_{circ}\,\mathbf{x} = \begin{pmatrix}1&0&0&1\\1&1&0&0\\0&1&1&0\\0&0&1&1\end{pmatrix}\begin{pmatrix}1\\2\\3\\4\end{pmatrix}$$

Computing row by row:

- $y_c[0] = 1\cdot1 + 0\cdot2 + 0\cdot3 + 1\cdot4 = 1 + 4 = 5$
- $y_c[1] = 1\cdot1 + 1\cdot2 + 0\cdot3 + 0\cdot4 = 1 + 2 = 3$
- $y_c[2] = 0\cdot1 + 1\cdot2 + 1\cdot3 + 0\cdot4 = 2 + 3 = 5$
- $y_c[3] = 0\cdot1 + 0\cdot2 + 1\cdot3 + 1\cdot4 = 3 + 4 = 7$

$$\boxed{y_c[n] = \{5,\,3,\,5,\,7\}}$$

### Step-by-Step Verification Using Wrap-Around

For $y_c[0]$: $h[\langle 0-k \rangle_4]$ for $k=0,1,2,3$ is $h[0], h[3], h[2], h[1] = 1,0,0,1$.

$$y_c[0] = x[0]\cdot1 + x[1]\cdot0 + x[2]\cdot0 + x[3]\cdot1 = 1 + 0 + 0 + 4 = 5$$

For $y_c[1]$: $h[\langle 1-k \rangle_4]$ for $k=0,1,2,3$ is $h[1], h[0], h[3], h[2] = 1,1,0,0$.

$$y_c[1] = 1\cdot1 + 2\cdot1 + 3\cdot0 + 4\cdot0 = 3$$

---

## Part (b): Linear Convolution

$x[n]$ has length $L = 4$, $h[n]$ has length $M = 2$ (the two trailing zeros do not extend the useful filter). Actually $h[n] = \{1, 1, 0, 0\}$ is formally length 4 but only 2 nonzero taps.

For the purpose of computing linear convolution we treat the nonzero portion: $h[n] = \{1, 1\}$ (length 2). Then $y_l$ has length $4 + 2 - 1 = 5$.

Alternatively, treating $h$ as length 4: $y_l$ has length $4 + 4 - 1 = 7$.

We compute $y_l[n] = \sum_{k=0}^{3} x[k]\,h[n-k]$ where $h$ has values $h[0]=1, h[1]=1, h[k]=0$ for $k\geq2$.

| $n$ | Terms with $h[n-k] \neq 0$ | $y_l[n]$ |
|---|---|---|
| 0 | $x[0]\,h[0] = 1$ | $1$ |
| 1 | $x[0]\,h[1] + x[1]\,h[0] = 1+2$ | $3$ |
| 2 | $x[1]\,h[1] + x[2]\,h[0] = 2+3$ | $5$ |
| 3 | $x[2]\,h[1] + x[3]\,h[0] = 3+4$ | $7$ |
| 4 | $x[3]\,h[1] = 4$ | $4$ |

$$\boxed{y_l[n] = \{1,\,3,\,5,\,7,\,4\}} \quad (n = 0,1,2,3,4)$$

---

## Part (c): Why Do They Differ? Time-Domain Aliasing

Compare:

- Linear: $y_l = \{1, 3, 5, 7, 4, 0, 0\}$ (7 samples, padded to length 7 or truncated to 5)
- 4-point circular: $y_c = \{5, 3, 5, 7\}$ (4 samples)

The 4-point circular convolution is equivalent to aliasing $y_l$ in the time domain with period $N = 4$:

$$y_c[n] = \sum_{r=-\infty}^{\infty} y_l[n + rN] = y_l[n] + y_l[n+4] \quad \text{for } n = 0,1,2,3$$

Verify:

| $n$ | $y_l[n]$ | $y_l[n+4]$ | Sum |
|---|---|---|---|
| 0 | 1 | 4 | **5** ✓ |
| 1 | 3 | 0 | **3** ✓ |
| 2 | 5 | 0 | **5** ✓ |
| 3 | 7 | 0 | **7** ✓ |

**Interpretation:** The $N = 4$ DFT corresponds to assuming the signal is periodic with period 4. The linear convolution result has 5 nonzero samples; when forced into a period-4 frame, sample $y_l[4] = 4$ wraps around and **adds onto** $y_c[0]$, corrupting it ($1 + 4 = 5$). This is time-domain aliasing.

**General rule:** $N$-point circular convolution of sequences of length $L$ and $M$ produces time-domain aliasing unless $N \geq L + M - 1$.

---

## Part (d): Zero-Padding to Eliminate Time-Domain Aliasing

Required DFT size: $N \geq L + M - 1 = 4 + 4 - 1 = 7$.

Practical choice: $N = 8$ (next power of 2, for FFT efficiency).

Zero-pad both sequences to length 8:

$$x_{zp}[n] = \{1, 2, 3, 4, 0, 0, 0, 0\}$$
$$h_{zp}[n] = \{1, 1, 0, 0, 0, 0, 0, 0\}$$

Compute 8-point circular convolution using the matrix method or DFT:

The linear convolution result is $y_l = \{1, 3, 5, 7, 4\}$ (5 samples). Padded to length 8: $\{1, 3, 5, 7, 4, 0, 0, 0\}$.

Now check for wrap-around aliasing with $N = 8$:

$$y_{c8}[n] = \sum_r y_l[n + 8r] = y_l[n] + y_l[n+8] = y_l[n] \quad \text{since } y_l[n+8] = 0 \text{ for } 0 \leq n \leq 7$$

All alias terms are zero. Therefore:

$$y_{c8}[n] = y_l[n] \quad \text{for all } n = 0, 1, \ldots, 7$$

$$\boxed{y_{c8} = \{1,\,3,\,5,\,7,\,4,\,0,\,0,\,0\}}$$

This equals the linear convolution output (with trailing zeros for the unused bins).

---

## Part (e): DFT-Based Verification

We verify using the DFT circular convolution property: $y_l[n] = \text{IDFT}_8\{X_{zp}[k]\cdot H_{zp}[k]\}$.

### Step 1: Compute 8-point DFTs

Using $W_8 = e^{-j2\pi/8} = e^{-j\pi/4}$.

**$X_{zp}[k]$** ($x = \{1,2,3,4,0,0,0,0\}$):

$$X_{zp}[k] = \sum_{n=0}^{7} x_{zp}[n]\,W_8^{kn} = \sum_{n=0}^{3}(n+1)\,W_8^{kn}$$

Key values (computing numerically):

| $k$ | $X_{zp}[k]$ |
|---|---|
| 0 | $1+2+3+4 = 10$ |
| 1 | $1 + 2W_8 + 3W_8^2 + 4W_8^3 = 1 + 2e^{-j\pi/4} + 3e^{-j\pi/2} + 4e^{-j3\pi/4}$ |
| 2 | $1 + 2e^{-j\pi/2} + 3e^{-j\pi} + 4e^{-j3\pi/2} = 1 - 2j - 3 + 4j = -2+2j$ |
| 4 | $1 - 2 + 3 - 4 = -2$ |

**$H_{zp}[k]$** ($h = \{1,1,0,0,0,0,0,0\}$):

$$H_{zp}[k] = 1 + W_8^k = 1 + e^{-j2\pi k/8}$$

Key values:

| $k$ | $H_{zp}[k]$ |
|---|---|
| 0 | $1 + 1 = 2$ |
| 1 | $1 + e^{-j\pi/4} \approx 1.707 - 0.707j$ |
| 2 | $1 + e^{-j\pi/2} = 1 - j$ |
| 3 | $1 + e^{-j3\pi/4} \approx 0.293 - 0.707j$ |
| 4 | $1 + e^{-j\pi} = 1 - 1 = 0$ |
| 5 | $1 + e^{-j5\pi/4} \approx 0.293 + 0.707j$ |
| 6 | $1 + e^{-j3\pi/2} = 1 + j$ |
| 7 | $1 + e^{-j7\pi/4} \approx 1.707 + 0.707j$ |

### Step 2: Product $Y[k] = X[k]\cdot H[k]$

At $k=0$: $Y[0] = 10 \times 2 = 20$

At $k=4$: $Y[4] = (-2) \times 0 = 0$

### Step 3: Inverse DFT

The IDFT of $Y[k]$ gives the circular convolution result. The key consistency check:

$$y_l[0] = \frac{1}{8}\sum_{k=0}^{7}Y[k]$$

For a sanity check, we use the energy method via Parseval's theorem or simply verify that the known result $y_l = \{1,3,5,7,4,0,0,0\}$ is consistent with $Y[0] = 20 = \sum_n y_l[n] = 1+3+5+7+4 = 20$ ✓

The full IDFT recovery is guaranteed by the DFT circular convolution theorem combined with the zero-padding ($N \geq 7$), so the result equals the linear convolution.

---

## Summary

| Method | Result | Length | Aliasing? |
|---|---|---|---|
| 4-point circular convolution | $\{5, 3, 5, 7\}$ | 4 | Yes — $y_l[4]=4$ wraps to $y_c[0]$ |
| Linear convolution | $\{1, 3, 5, 7, 4\}$ | 5 | N/A (reference) |
| 8-point circular (zero-padded) | $\{1, 3, 5, 7, 4, 0, 0, 0\}$ | 8 | No |

### Key Rule

To use the DFT to compute linear convolution:

$$\boxed{N \geq L + M - 1}$$

where $L$ and $M$ are the lengths of the two sequences. Choose $N$ to be the next power of 2 for FFT efficiency.

### Why This Matters

Every fast FIR filtering algorithm (overlap-add, overlap-save) relies on this zero-padding rule. Forgetting the $N \geq L + M - 1$ constraint is a common implementation bug that produces subtle circular aliasing artefacts in audio or communications processing — the output is wrong but only for signals that excite the filter's tail.
