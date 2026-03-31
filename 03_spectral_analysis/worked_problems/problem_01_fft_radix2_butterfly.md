# Worked Problem 01: Complete 8-Point Radix-2 DIT FFT

## Problem Statement

Compute the 8-point DFT of the sequence:

$$x[n] = \{1, 2, 3, 4, 4, 3, 2, 1\}, \quad n = 0, 1, \ldots, 7$$

using the radix-2 decimation-in-time (DIT) FFT algorithm. Show:
1. The bit-reversal permutation of the input
2. All three stages of butterfly computations with explicit twiddle factors
3. Intermediate values after each stage
4. Verification against the direct DFT formula for two bins

---

## Step 0: Notation and Twiddle Factors

For $N = 8$, the twiddle factors are $W_8^k = e^{-j2\pi k/8}$:

| $k$ | $W_8^k$ | Decimal approximation |
|:-:|:-:|:-:|
| 0 | $1$ | $1 + 0j$ |
| 1 | $e^{-j\pi/4}$ | $0.7071 - 0.7071j$ |
| 2 | $e^{-j\pi/2} = -j$ | $0 - 1j$ |
| 3 | $e^{-j3\pi/4}$ | $-0.7071 - 0.7071j$ |
| 4 | $e^{-j\pi} = -1$ | $-1 + 0j$ |

By conjugate symmetry: $W_8^{k+4} = -W_8^k$.

---

## Step 1: Bit-Reversal Permutation

For $N = 8$, index reversal uses 3-bit binary representations:

| $n$ | Binary (3-bit) | Bit-reversed | $r(n)$ | $x[r(n)]$ |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 000 | 000 | 0 | 1 |
| 1 | 001 | 100 | 4 | 4 |
| 2 | 010 | 010 | 2 | 3 |
| 3 | 011 | 110 | 6 | 2 |
| 4 | 100 | 001 | 1 | 2 |
| 5 | 101 | 101 | 5 | 3 |
| 6 | 110 | 011 | 3 | 4 |
| 7 | 111 | 111 | 7 | 1 |

**Bit-reversed input array:**

$$\mathbf{x}_{\text{BR}} = [x[0], x[4], x[2], x[6], x[1], x[5], x[3], x[7]] = [1, 4, 3, 2, 2, 3, 4, 1]$$

Label these as $a_0, a_1, \ldots, a_7$:

$$[a_0, a_1, a_2, a_3, a_4, a_5, a_6, a_7] = [1, 4, 3, 2, 2, 3, 4, 1]$$

---

## Step 2: Stage 1 — Distance-1 Butterflies

Stage 1 uses twiddle factor $W_8^0 = 1$ (trivial). Four butterflies, each operating on adjacent pairs:

**Butterfly structure at Stage 1:** twiddle $= W_8^0 = 1$ for all four butterflies.

$$\text{Output}_{\text{top}} = a + 1 \cdot b = a + b$$
$$\text{Output}_{\text{bot}} = a - 1 \cdot b = a - b$$

| Butterfly | Inputs | Computation | Outputs |
|:-:|:-:|:-:|:-:|
| B1 | $a_0=1$, $a_1=4$ | $1+4$, $1-4$ | $A_0=5$, $A_1=-3$ |
| B2 | $a_2=3$, $a_3=2$ | $3+2$, $3-2$ | $A_2=5$, $A_3=1$ |
| B3 | $a_4=2$, $a_5=3$ | $2+3$, $2-3$ | $A_4=5$, $A_5=-1$ |
| B4 | $a_6=4$, $a_7=1$ | $4+1$, $4-1$ | $A_6=5$, $A_7=3$ |

**After Stage 1:**

$$[A_0, A_1, A_2, A_3, A_4, A_5, A_6, A_7] = [5, -3, 5, 1, 5, -1, 5, 3]$$

---

## Step 3: Stage 2 — Distance-2 Butterflies

Stage 2 uses twiddle factors $W_8^0 = 1$ and $W_8^2 = -j$. Four butterflies, paired in groups of 4:

**Group 1:** indices {0, 1, 2, 3}
- Butterfly B5: indices 0 and 2, twiddle $W_8^0 = 1$
- Butterfly B6: indices 1 and 3, twiddle $W_8^2 = -j$

| Butterfly | Inputs | Twiddle | Twiddle $\times$ input | Outputs |
|:-:|:-:|:-:|:-:|:-:|
| B5 | $A_0=5$, $A_2=5$ | $W_8^0=1$ | $1 \times 5 = 5$ | $B_0 = 5+5 = 10$, $B_2 = 5-5 = 0$ |
| B6 | $A_1=-3$, $A_3=1$ | $W_8^2=-j$ | $(-j)(1) = -j$ | $B_1 = -3+(-j) = -3-j$, $B_3 = -3-(-j) = -3+j$ |

**Group 2:** indices {4, 5, 6, 7}
- Butterfly B7: indices 4 and 6, twiddle $W_8^0 = 1$
- Butterfly B8: indices 5 and 7, twiddle $W_8^2 = -j$

| Butterfly | Inputs | Twiddle | Twiddle $\times$ input | Outputs |
|:-:|:-:|:-:|:-:|:-:|
| B7 | $A_4=5$, $A_6=5$ | $W_8^0=1$ | $1 \times 5 = 5$ | $B_4 = 10$, $B_6 = 0$ |
| B8 | $A_5=-1$, $A_7=3$ | $W_8^2=-j$ | $(-j)(3) = -3j$ | $B_5 = -1+(-3j) = -1-3j$, $B_7 = -1-(-3j) = -1+3j$ |

**After Stage 2:**

$$[B_0, B_1, B_2, B_3, B_4, B_5, B_6, B_7] = [10, -3-j, 0, -3+j, 10, -1-3j, 0, -1+3j]$$

---

## Step 4: Stage 3 — Distance-4 Butterflies

Stage 3 uses twiddle factors $W_8^0 = 1$, $W_8^1 = \frac{1}{\sqrt{2}}(1-j)$, $W_8^2 = -j$, $W_8^3 = \frac{1}{\sqrt{2}}(-1-j)$. Four butterflies, one group of 8:

| Butterfly | Indices | Inputs | Twiddle $W_8^k$ | $W_8^k \times B_{\text{bot}}$ | Output top | Output bot |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| B9 | 0 and 4 | $B_0=10$, $B_4=10$ | $W_8^0=1$ | $10$ | $X[0]=20$ | $X[4]=0$ |
| B10 | 1 and 5 | $B_1=-3-j$, $B_5=-1-3j$ | $W_8^1=\frac{1-j}{\sqrt{2}}$ | see below | $X[1]$ | $X[5]$ |
| B11 | 2 and 6 | $B_2=0$, $B_6=0$ | $W_8^2=-j$ | $0$ | $X[2]=0$ | $X[6]=0$ |
| B12 | 3 and 7 | $B_3=-3+j$, $B_7=-1+3j$ | $W_8^3=\frac{-1-j}{\sqrt{2}}$ | see below | $X[3]$ | $X[7]$ |

**Detail for Butterfly B10:**

$$W_8^1 = \frac{1-j}{\sqrt{2}}$$

$$W_8^1 \times B_5 = \frac{1-j}{\sqrt{2}} \times (-1-3j) = \frac{(-1-3j)(1-j)}{\sqrt{2}}$$

Expand numerator: $(-1)(1) + (-1)(-j) + (-3j)(1) + (-3j)(-j) = -1 + j - 3j + 3j^2 = -1 + j - 3j - 3 = -4 - 2j$

$$W_8^1 \times B_5 = \frac{-4-2j}{\sqrt{2}} = -2\sqrt{2} - j\sqrt{2} \approx -2.828 - 1.414j$$

$$X[1] = B_1 + W_8^1 B_5 = (-3-j) + (-2.828-1.414j) = -5.828 - 2.414j$$

$$X[5] = B_1 - W_8^1 B_5 = (-3-j) - (-2.828-1.414j) = -0.172 + 0.414j$$

**Detail for Butterfly B12:**

$$W_8^3 = \frac{-1-j}{\sqrt{2}}$$

$$W_8^3 \times B_7 = \frac{(-1-j)(-1+3j)}{\sqrt{2}} = \frac{1 - 3j + j - 3j^2}{\sqrt{2}} = \frac{1 - 3j + j + 3}{\sqrt{2}} = \frac{4 - 2j}{\sqrt{2}} = 2\sqrt{2} - j\sqrt{2} \approx 2.828 - 1.414j$$

$$X[3] = B_3 + W_8^3 B_7 = (-3+j) + (2.828-1.414j) = -0.172 - 0.414j$$

$$X[7] = B_3 - W_8^3 B_7 = (-3+j) - (2.828-1.414j) = -5.828 + 2.414j$$

**Final FFT output:**

$$X[k] = [20,\ -5.828-2.414j,\ 0,\ -0.172-0.414j,\ 0,\ -0.172+0.414j,\ 0,\ -5.828+2.414j]$$

---

## Step 5: Verification Against Direct DFT

Verify $X[0]$ and $X[1]$ using the direct DFT formula $X[k] = \sum_{n=0}^{7} x[n] W_8^{kn}$.

**Verify $X[0]$:**

$$X[0] = \sum_{n=0}^{7} x[n] W_8^0 = \sum_{n=0}^{7} x[n] = 1+2+3+4+4+3+2+1 = 20 \checkmark$$

**Verify $X[1]$:**

$$X[1] = \sum_{n=0}^{7} x[n] e^{-j2\pi n/8}$$

$$= x[0] W_8^0 + x[1] W_8^1 + x[2] W_8^2 + x[3] W_8^3 + x[4] W_8^4 + x[5] W_8^5 + x[6] W_8^6 + x[7] W_8^7$$

Using: $W_8^0=1$, $W_8^1=\frac{1-j}{\sqrt{2}}$, $W_8^2=-j$, $W_8^3=\frac{-1-j}{\sqrt{2}}$, $W_8^4=-1$, $W_8^5=\frac{-1+j}{\sqrt{2}}$, $W_8^6=j$, $W_8^7=\frac{1+j}{\sqrt{2}}$:

$$X[1] = 1(1) + 2\!\left(\frac{1-j}{\sqrt{2}}\right) + 3(-j) + 4\!\left(\frac{-1-j}{\sqrt{2}}\right) + 4(-1) + 3\!\left(\frac{-1+j}{\sqrt{2}}\right) + 2(j) + 1\!\left(\frac{1+j}{\sqrt{2}}\right)$$

Collecting real parts:

$$\text{Re}\{X[1]\} = 1 + \frac{2}{\sqrt{2}} - \frac{4}{\sqrt{2}} - 4 - \frac{3}{\sqrt{2}} + \frac{1}{\sqrt{2}} = 1 + \frac{2-4-3+1}{\sqrt{2}} - 4 = -3 + \frac{-4}{\sqrt{2}} = -3 - 2\sqrt{2} \approx -5.828$$

Collecting imaginary parts:

$$\text{Im}\{X[1]\} = -\frac{2}{\sqrt{2}} - 3 - \frac{4}{\sqrt{2}} + \frac{3}{\sqrt{2}} + 2 + \frac{1}{\sqrt{2}} = -1 + \frac{-2-4+3+1}{\sqrt{2}} = -1 + \frac{-2}{\sqrt{2}} = -1 - \sqrt{2} \approx -2.414$$

$$X[1] \approx -5.828 - 2.414j \checkmark$$

---

## Step 6: Symmetry Check

The input $x[n] = \{1,2,3,4,4,3,2,1\}$ is **real and symmetric** ($x[n] = x[N-1-n]$). For a real symmetric sequence:
- $X[k]$ is real for all $k$? No — symmetry here is $x[n] = x[7-n]$, which makes $X[k]$ real and even only for DFT-symmetric inputs.
- Since $x[n]$ is real, $X[k] = X^*[N-k]$ (conjugate symmetry): $X[1] = X^*[7]$, $X[2] = X^*[6]$, etc.

Check: $X[7] = -5.828 + 2.414j = X^*[1] \checkmark$

Also, $X[0] = 20$ (real), $X[2] = 0$ (real), $X[4] = 0$ (real), $X[6] = 0$ (real) — consistent with conjugate symmetry where $X[N/2] = X^*[N/2]$ (must be real).

---

## Step 7: Python Implementation

```python
import numpy as np

def fft_radix2_dit(x):
    """
    Radix-2 Decimation-In-Time FFT (Cooley-Tukey).
    
    Assumes len(x) is a power of 2.
    Returns the N-point DFT of x.
    """
    N = len(x)
    if N == 1:
        return x.copy()

    # --- Bit-reversal permutation ---
    num_bits = int(np.log2(N))
    x_br = np.zeros(N, dtype=complex)
    for n in range(N):
        # Compute bit-reversal of n using num_bits bits
        r = int('{:0{w}b}'.format(n, w=num_bits)[::-1], 2)
        x_br[r] = x[n]

    # --- In-place butterfly computation ---
    # Stage s: butterfly span = 2^(s+1), twiddle stride = N / 2^(s+1)
    for s in range(num_bits):
        span = 2 ** (s + 1)      # number of elements per group
        half = span // 2         # half-span = distance between butterfly pair
        twiddle_stride = N // span

        for group_start in range(0, N, span):
            for k in range(half):
                # Twiddle factor: W_N^(k * twiddle_stride)
                W = np.exp(-2j * np.pi * k * twiddle_stride / N)
                top_idx = group_start + k
                bot_idx = group_start + k + half

                top = x_br[top_idx]
                bot = x_br[bot_idx]

                x_br[top_idx] = top + W * bot
                x_br[bot_idx] = top - W * bot

    return x_br


# --- Test ---
x = np.array([1, 2, 3, 4, 4, 3, 2, 1], dtype=complex)

X_fft = fft_radix2_dit(x)
X_ref = np.fft.fft(x)  # reference

print("k  |  Our FFT          |  NumPy FFT        |  Match")
print("-" * 65)
for k in range(8):
    match = np.isclose(X_fft[k], X_ref[k], atol=1e-10)
    print(f"{k}  |  {X_fft[k]: .4f}  |  {X_ref[k]: .4f}  |  {match}")
```

**Expected output:**

```
k  |  Our FFT          |  NumPy FFT        |  Match
-----------------------------------------------------------------
0  |  20.0000+0.0000j  |  20.0000+0.0000j  |  True
1  |  -5.8284-2.4142j  |  -5.8284-2.4142j  |  True
2  |  0.0000+0.0000j   |  0.0000+0.0000j   |  True
3  |  -0.1716-0.4142j  |  -0.1716-0.4142j  |  True
4  |  0.0000+0.0000j   |  0.0000+0.0000j   |  True
5  |  -0.1716+0.4142j  |  -0.1716+0.4142j  |  True
6  |  0.0000+0.0000j   |  0.0000+0.0000j   |  True
7  |  -5.8284+2.4142j  |  -5.8284+2.4142j  |  True
```

---

## Summary: Operation Count

For $N = 8$ (radix-2 DIT):

| Stage | Butterflies | Non-trivial mults | Additions |
|:-:|:-:|:-:|:-:|
| 1 | 4 | 0 (all $W_8^0=1$) | 8 |
| 2 | 4 | 2 ($W_8^2=-j$ is trivial: swap Im/Re) | 8 |
| 3 | 4 | 4 (2 non-trivial: $W_8^1$, $W_8^3$; 2 trivial: $W_8^0$, $W_8^2$) | 8 |
| **Total** | **12** | **4** (non-trivial) | **24** |

Direct DFT would require $N^2 = 64$ complex multiplications. The FFT uses only 4 non-trivial ones — a 16x reduction in multiplications for $N=8$.

Note: $W_8^2 = -j$ is "trivially" implemented as swapping real and imaginary parts with sign change, requiring no floating-point multiplication. This is why stage 2 has 0 "non-trivial" multiplications in a careful implementation.
