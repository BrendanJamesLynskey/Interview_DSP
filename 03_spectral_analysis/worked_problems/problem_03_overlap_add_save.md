# Worked Problem 03: Overlap-Add and Overlap-Save

## Problem Statement

Compute the linear convolution of a long input signal $x[n]$ with a short FIR filter $h[n]$ using both the **overlap-add (OLA)** and **overlap-save (OLS)** methods. Work through a complete numerical example, then compare computational efficiency against direct convolution.

**Given:**
- Input signal: $x[n] = \{1, 2, 3, 4, 5, 6, 7, 8\}$ (length $L = 8$)
- Filter: $h[n] = \{1, 2, 1\}$ (length $M = 3$)
- Use block length $N_{\text{block}} = 4$ input samples per block

**Target:** The true linear convolution $y[n] = x[n] * h[n]$, which has length $L + M - 1 = 10$.

---

## Step 0: Verify the True Convolution (Reference)

The linear convolution $y[n] = \sum_{k=0}^{M-1} h[k]\,x[n-k]$:

| $n$ | $h[0]x[n]$ | $h[1]x[n-1]$ | $h[2]x[n-2]$ | $y[n]$ |
|:-:|:-:|:-:|:-:|:-:|
| 0 | $1(1)=1$ | 0 | 0 | **1** |
| 1 | $1(2)=2$ | $2(1)=2$ | 0 | **4** |
| 2 | $1(3)=3$ | $2(2)=4$ | $1(1)=1$ | **8** |
| 3 | $1(4)=4$ | $2(3)=6$ | $1(2)=2$ | **12** |
| 4 | $1(5)=5$ | $2(4)=8$ | $1(3)=3$ | **16** |
| 5 | $1(6)=6$ | $2(5)=10$ | $1(4)=4$ | **20** |
| 6 | $1(7)=7$ | $2(6)=12$ | $1(5)=5$ | **24** |
| 7 | $1(8)=8$ | $2(7)=14$ | $1(6)=6$ | **28** |
| 8 | 0 | $2(8)=16$ | $1(7)=7$ | **23** |
| 9 | 0 | 0 | $1(8)=8$ | **8** |

**Reference:** $y = [1, 4, 8, 12, 16, 20, 24, 28, 23, 8]$

---

## Part 1: Overlap-Add (OLA) Method

### Principle

Partition $x[n]$ into **non-overlapping blocks** of length $B$. Convolve each block with $h[n]$ via FFT (length $N_{\text{FFT}} \geq B + M - 1$). The output blocks overlap by $M-1$ samples and must be **added** at the boundaries.

### Setup

- Block length: $B = 4$
- Filter length: $M = 3$
- FFT length: $N_{\text{FFT}} \geq B + M - 1 = 4 + 3 - 1 = 6$. Use $N_{\text{FFT}} = 8$ (next power of 2 $\geq 6$).
- Number of blocks: $\lceil L/B \rceil = \lceil 8/4 \rceil = 2$ blocks

**Precompute $H[k]$:** the $N_{\text{FFT}}=8$-point DFT of $h[n]$ zero-padded to length 8:

$$h_{\text{pad}} = [1, 2, 1, 0, 0, 0, 0, 0]$$

$$H[k] = \text{DFT}_8\{h_{\text{pad}}\}$$

(Computed via FFT; exact values not written out in full here — used symbolically below.)

### Block 0: $x_0[n] = \{1, 2, 3, 4\}$ (samples 0–3)

Zero-pad to length 8: $x_0^{\text{pad}} = [1, 2, 3, 4, 0, 0, 0, 0]$

Circular convolution via FFT:

$$y_0 = \text{IDFT}_8\{\text{DFT}_8\{x_0^{\text{pad}}\} \cdot H[k]\}$$

This is equivalent to the linear convolution of $x_0$ and $h$ (valid because we padded to $\geq B+M-1$):

$$y_0 = x_0 * h = [1\cdot1,\ 1\cdot2+2\cdot1,\ 1\cdot1+2\cdot2+3\cdot1,\ 2\cdot1+3\cdot2+4\cdot1,\ 3\cdot1+4\cdot2,\ 4\cdot1,\ 0,\ 0]$$

$$y_0 = [1, 4, 8, 12, 11, 4, 0, 0]$$

(Only the first $B + M - 1 = 6$ values are non-zero; the rest are zero-padding artifacts.)

Placed in the output array starting at position 0:

| Output position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|:---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| From Block 0 | 1 | 4 | 8 | 12 | 11 | 4 | — | — | — | — |

### Block 1: $x_1[n] = \{5, 6, 7, 8\}$ (samples 4–7)

Zero-pad: $x_1^{\text{pad}} = [5, 6, 7, 8, 0, 0, 0, 0]$

$$y_1 = x_1 * h$$

| $n$ | calc | value |
|:-:|:-:|:-:|
| 0 | $1\cdot5$ | 5 |
| 1 | $2\cdot5+1\cdot6$ | 16 |
| 2 | $1\cdot5+2\cdot6+1\cdot7$ | 24 |
| 3 | $1\cdot6+2\cdot7+1\cdot8$ | 28 |
| 4 | $1\cdot7+2\cdot8$ | 23 |
| 5 | $1\cdot8$ | 8 |

$$y_1 = [5, 16, 24, 28, 23, 8, 0, 0]$$

Placed in the output array starting at position $B \times 1 = 4$:

| Output position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|:---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| From Block 0 | 1 | 4 | 8 | 12 | **11** | **4** | — | — | — | — |
| From Block 1 | — | — | — | — | **5** | **16** | 24 | 28 | 23 | 8 |

### Overlap-Add Step

Positions 4 and 5 receive contributions from both blocks. Add:

| Position | Block 0 | Block 1 | Sum |
|:-:|:-:|:-:|:-:|
| 4 | 11 | 5 | **16** |
| 5 | 4 | 16 | **20** |

**Final OLA output:**

$$y_{\text{OLA}} = [1, 4, 8, 12, 16, 20, 24, 28, 23, 8] \checkmark$$

Matches the reference exactly.

---

## Part 2: Overlap-Save (OLS) Method

### Principle

Maintain a **buffer** of length $N_{\text{FFT}} = B + M - 1$ that slides forward by $B$ samples at each step. The first $M-1$ samples of each buffer are the **tail of the previous input block** (overlap from the past). The circular convolution is computed, and only the last $B$ output samples are valid (the first $M-1$ are discarded as "aliased" transient samples).

### Setup

- Buffer length: $N_{\text{FFT}} = B + M - 1 = 6$. Use $N_{\text{FFT}} = 8$.
- Valid output samples per block: $B = N_{\text{FFT}} - (M-1) = 8 - 2 = 6$? No — we will use $N_{\text{FFT}} = 6$ exactly for clarity, then redo with 8.

Let us use $N_{\text{FFT}} = 6$ (exact, not a power of 2 — for clarity only; in practice use $N_{\text{FFT}} = 8$).

- $M - 1 = 2$ samples of overlap (from previous block)
- Valid output samples per block: $B = N_{\text{FFT}} - (M-1) = 6 - 2 = 4$

**Precompute:** $H[k] = \text{DFT}_6\{[1, 2, 1, 0, 0, 0]\}$

### Initialisation: Prepend $M-1$ zeros

Before the signal, prepend $M-1 = 2$ zero samples (initial condition: zero past input).

Extended input: $x_{\text{ext}} = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8]$

### Block 0: Buffer = $x_{\text{ext}}[0:6]= [0, 0, 1, 2, 3, 4]$

Compute 6-point circular convolution with $h$:

The 6-point circular convolution of $[0,0,1,2,3,4]$ and $[1,2,1,0,0,0]$:

$$c[n] = \sum_{k=0}^{5} h[k] \cdot x_{\text{buf}}[(n-k) \bmod 6]$$

| $n$ | $h[0]\cdot x[n]$ | $h[1]\cdot x[(n-1)\bmod 6]$ | $h[2]\cdot x[(n-2)\bmod 6]$ | $c[n]$ |
|:-:|:-:|:-:|:-:|:-:|
| 0 | $1\cdot0=0$ | $2\cdot x[5]=2\cdot4=8$ | $1\cdot x[4]=1\cdot3=3$ | 11 |
| 1 | $1\cdot0=0$ | $2\cdot x[0]=0$ | $1\cdot x[5]=4$ | 4 |
| 2 | $1\cdot1=1$ | $2\cdot x[1]=0$ | $1\cdot x[0]=0$ | 1 |
| 3 | $1\cdot2=2$ | $2\cdot x[2]=2$ | $1\cdot x[1]=0$ | 4 |
| 4 | $1\cdot3=3$ | $2\cdot x[3]=4$ | $1\cdot x[2]=1$ | 8 |
| 5 | $1\cdot4=4$ | $2\cdot x[4]=6$ | $1\cdot x[3]=2$ | 12 |

Circular convolution: $c = [11, 4, 1, 4, 8, 12]$

**Discard first $M-1=2$ samples** (circular wrap-around artefacts): discard $c[0]=11, c[1]=4$.

**Keep last $B=4$ samples:** $c[2:6] = [1, 4, 8, 12]$

These correspond to output samples $y[0], y[1], y[2], y[3]$.

### Block 1: Buffer = $x_{\text{ext}}[4:10] = [3, 4, 5, 6, 7, 8]$

(Overlap: last $M-1=2$ samples of previous buffer = $[3,4]$; new samples $= [5,6,7,8]$.)

6-point circular convolution of $[3,4,5,6,7,8]$ and $[1,2,1,0,0,0]$:

| $n$ | $h[0]\cdot x[n]$ | $h[1]\cdot x[(n-1)\bmod 6]$ | $h[2]\cdot x[(n-2)\bmod 6]$ | $c[n]$ |
|:-:|:-:|:-:|:-:|:-:|
| 0 | $1\cdot3=3$ | $2\cdot x[5]=2\cdot8=16$ | $1\cdot x[4]=1\cdot7=7$ | 26 |
| 1 | $1\cdot4=4$ | $2\cdot x[0]=2\cdot3=6$ | $1\cdot x[5]=1\cdot8=8$ | 18 |
| 2 | $1\cdot5=5$ | $2\cdot x[1]=2\cdot4=8$ | $1\cdot x[0]=1\cdot3=3$ | 16 |
| 3 | $1\cdot6=6$ | $2\cdot x[2]=2\cdot5=10$ | $1\cdot x[1]=1\cdot4=4$ | 20 |
| 4 | $1\cdot7=7$ | $2\cdot x[3]=2\cdot6=12$ | $1\cdot x[2]=1\cdot5=5$ | 24 |
| 5 | $1\cdot8=8$ | $2\cdot x[4]=2\cdot7=14$ | $1\cdot x[3]=1\cdot6=6$ | 28 |

Discard $c[0]=26, c[1]=18$. Keep $c[2:6] = [16, 20, 24, 28]$.

These correspond to $y[4], y[5], y[6], y[7]$.

### Handling the Tail

The last $M-1=2$ samples of $y$ (positions 8 and 9) correspond to the "tail" of the convolution. To compute them, we need one more block with $x$ extended by $M-1$ zeros at the end:

Block 2 buffer: $[7, 8, 0, 0, 0, 0]$ (last 2 samples of $x$ plus 4 zeros)

Circular convolution of $[7,8,0,0,0,0]$ and $[1,2,1,0,0,0]$:

| $n$ | $h[0]x[n]$ | $h[1]x[(n-1)\bmod6]$ | $h[2]x[(n-2)\bmod6]$ | $c[n]$ |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 7 | $2\cdot0=0$ | $1\cdot0=0$ | 7 |
| 1 | 8 | $2\cdot7=14$ | $1\cdot0=0$ | 22 |
| 2 | 0 | $2\cdot8=16$ | $1\cdot7=7$ | 23 |
| 3 | 0 | 0 | $1\cdot8=8$ | 8 |
| 4 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 |

Discard $c[0]=7, c[1]=22$. Keep $c[2:4] = [23, 8]$ (only 2 valid samples needed here).

**Final OLS output:**

$$y_{\text{OLS}} = [1, 4, 8, 12, 16, 20, 24, 28, 23, 8] \checkmark$$

---

## Part 3: Computational Efficiency Comparison

### Operation Counts

Let:
- $L$ = total input length
- $M$ = filter length
- $B$ = block length (new samples per block in OLS; data block length in OLA)
- $N_{\text{FFT}} = B + M - 1$ (minimum FFT length; round up to power of 2 in practice)
- $K = \lceil L/B \rceil$ = number of blocks

**Direct convolution.** Each output sample requires $M$ multiplications and $M-1$ additions. For $L + M - 1$ output samples:

$$C_{\text{direct}} = (L + M - 1) \cdot M \approx LM \quad \text{(multiplications)}$$

**Overlap-add / Overlap-save.** Per block:
- 2 forward FFTs of length $N_{\text{FFT}}$: $2 \times \frac{N_{\text{FFT}}}{2}\log_2 N_{\text{FFT}}$ complex multiplications (but one FFT is of $h$ and is precomputed)
- 1 inverse FFT
- $N_{\text{FFT}}$ complex multiplications ($X[k] \cdot H[k]$)
- Per-block cost: $\frac{3}{2} N_{\text{FFT}} \log_2 N_{\text{FFT}} + N_{\text{FFT}}$

Over $K$ blocks (ignoring the precomputed $H[k]$):

$$C_{\text{FFT}} \approx K \left(\frac{3}{2} N_{\text{FFT}} \log_2 N_{\text{FFT}} + N_{\text{FFT}}\right) = \frac{L}{B}\left(\frac{3}{2} N_{\text{FFT}} \log_2 N_{\text{FFT}} + N_{\text{FFT}}\right)$$

Since $N_{\text{FFT}} \approx B + M$ and $K = L/B$:

$$C_{\text{FFT}} \approx L \cdot \frac{N_{\text{FFT}}}{B} \left(\frac{3}{2}\log_2 N_{\text{FFT}} + 1\right)$$

### Crossover Point

The FFT method is more efficient when $C_{\text{FFT}} < C_{\text{direct}}$:

$$\frac{N_{\text{FFT}}}{B} \left(\frac{3}{2}\log_2 N_{\text{FFT}} + 1\right) < M$$

For $B \gg M$: $N_{\text{FFT}} \approx B$, so condition becomes $\frac{3}{2}\log_2 B < M$, i.e., $B > 2^{2M/3}$.

**Optimal block size** minimises per-sample cost:

$$B_{\text{opt}} = \arg\min_B \frac{N_{\text{FFT}}(B)}{B} \cdot C_{\text{per block FFT}}$$

Taking derivative and setting to zero (approximately): $B_{\text{opt}} \approx M$ (roughly equal to filter length when $M$ is large; larger blocks better for very long $L$).

### Numerical Comparison for Our Example

| Method | Operations | (for $L=8$, $M=3$) |
|---|---|:-:|
| Direct | $LM = 8 \times 3 = 24$ real mults | 24 |
| OLA ($B=4$, $N_{\text{FFT}}=8$) | $2 \times (4 \times \frac{8}{2}\log_2 8 + 8) \approx 2 \times (48 + 8)$ | 112 |

For this tiny example, direct convolution wins. The FFT approach overhead is only justified for large $L$:

| $L$ | $M$ | Direct ($LM$) | FFT ($B=256$, $N=512$) | FFT wins? |
|:-:|:-:|:-:|:-:|:-:|
| 1000 | 64 | 64000 | $\approx 3900 \times 4 \approx 16000$ | Yes |
| 10000 | 512 | 5000000 | $\approx 10000/256 \times 6000 \approx 234000$ | Yes |
| 10000 | 10 | 100000 | $\approx 585000$ | No |

**Rule of thumb:** FFT-based convolution is preferred when $M \gtrsim 64$ and $L \gg M$.

---

## Python Implementation

```python
import numpy as np

def overlap_add(x, h, block_size):
    """
    Overlap-add method for linear convolution.
    
    Parameters
    ----------
    x          : input signal, length L
    h          : filter impulse response, length M
    block_size : number of input samples per block (B)
    
    Returns
    -------
    y : output signal, length L + M - 1
    """
    L = len(x)
    M = len(h)
    N_fft = int(2 ** np.ceil(np.log2(block_size + M - 1)))  # FFT length
    output_len = L + M - 1
    y = np.zeros(output_len)

    # Precompute H[k]
    H = np.fft.rfft(h, n=N_fft)

    num_blocks = int(np.ceil(L / block_size))
    for i in range(num_blocks):
        start = i * block_size
        end = min(start + block_size, L)
        x_block = x[start:end]

        # Zero-pad and FFT
        X_block = np.fft.rfft(x_block, n=N_fft)

        # Multiply in frequency domain
        Y_block = X_block * H

        # IFFT to get linear convolution of this block
        y_block = np.fft.irfft(Y_block, n=N_fft)[:block_size + M - 1]

        # Overlap-add into output
        out_start = start
        out_end = out_start + len(y_block)
        y[out_start:min(out_end, output_len)] += y_block[:min(len(y_block), output_len - out_start)]

    return y


def overlap_save(x, h, block_size):
    """
    Overlap-save method for linear convolution.
    
    Parameters
    ----------
    x          : input signal, length L
    h          : filter impulse response, length M
    block_size : number of NEW samples per block (B)
    
    Returns
    -------
    y : output signal, length L + M - 1
    """
    L = len(x)
    M = len(h)
    N_fft = int(2 ** np.ceil(np.log2(block_size + M - 1)))
    overlap = M - 1  # number of samples to keep from previous block
    output_len = L + M - 1

    # Precompute H[k]
    H = np.fft.rfft(h, n=N_fft)

    # Extend x: prepend M-1 zeros (initial state), append M-1 zeros (tail)
    x_ext = np.concatenate([np.zeros(M - 1), x, np.zeros(M - 1)])

    y = np.zeros(output_len)
    pos = 0   # position in output array

    # Process blocks
    idx = 0   # starting index in x_ext
    while pos < output_len:
        # Buffer: M-1 past samples + block_size new samples
        buf_end = idx + N_fft
        if buf_end > len(x_ext):
            buf = np.concatenate([x_ext[idx:], np.zeros(buf_end - len(x_ext))])
        else:
            buf = x_ext[idx:buf_end]

        # Circular convolution via FFT
        C = np.fft.irfft(np.fft.rfft(buf, n=N_fft) * H, n=N_fft)

        # Discard first M-1 samples (wrap-around artefacts)
        valid = C[M - 1: M - 1 + block_size]

        # Copy to output
        copy_len = min(len(valid), output_len - pos)
        y[pos:pos + copy_len] = valid[:copy_len]

        pos += block_size
        idx += block_size

    return y


# --- Test ---
x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
h = np.array([1, 2, 1], dtype=float)

y_ref = np.convolve(x, h)           # reference: direct linear convolution
y_ola = overlap_add(x, h, block_size=4)
y_ols = overlap_save(x, h, block_size=4)

print("Reference:    ", y_ref)
print("Overlap-Add:  ", np.round(y_ola, 8))
print("Overlap-Save: ", np.round(y_ols, 8))
print("OLA matches:  ", np.allclose(y_ola, y_ref))
print("OLS matches:  ", np.allclose(y_ols, y_ref))
```

**Expected output:**

```
Reference:    [ 1.  4.  8. 12. 16. 20. 24. 28. 23.  8.]
Overlap-Add:  [ 1.  4.  8. 12. 16. 20. 24. 28. 23.  8.]
Overlap-Save: [ 1.  4.  8. 12. 16. 20. 24. 28. 23.  8.]
OLA matches:  True
OLS matches:  True
```

---

## Summary: OLA vs. OLS Comparison

| Aspect | Overlap-Add | Overlap-Save |
|---|---|---|
| **Input blocking** | Non-overlapping blocks of length $B$ | Buffer of length $N_{\text{FFT}}$ with $M-1$ overlap |
| **Output handling** | Valid output blocks **added** at overlapping edges | Discard first $M-1$ outputs (keep last $B$) |
| **FFT length** | $N_{\text{FFT}} \geq B + M - 1$ | $N_{\text{FFT}} \geq B + M - 1$ |
| **Output samples per block** | $B + M - 1$ (with overlap region) | $B$ (exactly) |
| **Complexity per output sample** | $\approx \frac{3}{2B} N_{\text{FFT}} \log_2 N_{\text{FFT}} + 1$ | Same |
| **Initial condition** | No pre-pended zeros needed | Prepend $M-1$ zeros to initialise |
| **Memory** | Need output buffer for overlap-add | Need input buffer of length $N_{\text{FFT}}$ |
| **Preferred for** | One-shot processing, known-length signals | Real-time / streaming (no output buffer needed) |

**Both methods compute exact linear convolution** and have identical asymptotic complexity. The choice is a matter of implementation convenience:
- **OLA** is natural when the entire input is available in advance.
- **OLS** (also called overlap-discard) is natural for streaming/real-time applications since output is produced immediately without waiting to add overlapping contributions.
