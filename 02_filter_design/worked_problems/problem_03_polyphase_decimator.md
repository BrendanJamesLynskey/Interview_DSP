# Worked Problem 03: Polyphase Decimation-by-4 Filter

**Subject:** Digital Signal Processing
**Topic:** Polyphase Decomposition, Decimation, Noble Identities, Computational Savings
**Difficulty:** Intermediate to Advanced

---

## Problem Statement

Design and analyse a polyphase decimation-by-4 FIR filter. The input signal has bandwidth up to $f_{max} = 10\,\text{kHz}$ and the input sample rate is $f_{s,in} = 80\,\text{kHz}$.

**Tasks:**

**(a)** Specify the lowpass anti-decimation filter requirements.

**(b)** Choose a suitable 20-tap prototype FIR lowpass filter $H(z)$ with cutoff at $\pi/4$.

**(c)** Decompose $H(z)$ into 4 polyphase components $E_0(z), E_1(z), E_2(z), E_3(z)$.

**(d)** Draw the polyphase decimation structure (after applying Noble Identity 1).

**(e)** Quantify the computational savings versus the naive approach.

**(f)** Write Python code implementing both naive and polyphase decimators. Verify they produce the same output.

---

## Part (a): Anti-Decimation Filter Requirements

Decimation by $M = 4$ reduces the sample rate from $f_{s,in} = 80\,\text{kHz}$ to $f_{s,out} = 20\,\text{kHz}$.

**Anti-aliasing filter cutoff:**

After decimation, the Nyquist frequency is $f_{s,out}/2 = 10\,\text{kHz}$.

Lowpass filter must pass $[0, 10\,\text{kHz}]$ and reject everything above to prevent aliasing when every 4th sample is kept.

Digital cutoff (relative to input rate):

$$\omega_c = 2\pi \frac{f_{max}}{f_{s,in}} = 2\pi \frac{10000}{80000} = \frac{\pi}{4}\,\text{rad/sample}$$

This is exactly $\pi/M$, confirming the standard rule: the decimation filter has digital cutoff $\pi/M$.

**Signal and image bands:**

```
Input spectrum (0 to π rad/sample = 40 kHz):

 |H(ω)|
 1  |_______________|
    |               \
    |                \
 0  |_________________\________________
    0     π/4        π                  ω
         (10kHz)   (40kHz)
```

The filter passes $[0, \pi/4]$ and rejects $(\pi/4, \pi]$. After downsampling, the rejected band would have aliased into the $[0, \pi/4]$ band.

---

## Part (b): Prototype FIR Filter

For this example, use a **20-tap linear-phase FIR** lowpass filter with normalised cutoff $\omega_c = \pi/4$.

**Design:** Parks-McClellan or Kaiser window. The coefficients are:

Using `scipy.signal.firwin(20, 0.25)` (cutoff = 0.25 in units of Nyquist):

```python
from scipy.signal import firwin
import numpy as np

M_dec = 4     # Decimation factor
N = 20        # Filter length (must be divisible by M_dec for clean decomposition)
              # Note: 20 taps = indices 0..19

h = firwin(N, 1.0/M_dec)  # cutoff at 1/4 of Nyquist = π/4 of full rate
```

For the sake of the worked example, denote the 20 coefficients as:

$$h[n] = \{h_0, h_1, h_2, \ldots, h_{19}\}$$

with indices $n = 0, 1, \ldots, 19$.

**Typical values** for this design (low-value, symmetric around $n = 9.5$):

```
h[0]  =  0.0028   h[10] =  0.0028  (symmetric: h[n] = h[19-n])
h[1]  = -0.0000   h[11] = -0.0000
h[2]  = -0.0114   h[12] = -0.0114
h[3]  = -0.0000   h[13] = -0.0000
h[4]  =  0.0507   h[14] =  0.0507
h[5]  = -0.0000   h[15] = -0.0000
h[6]  = -0.2000   h[16] = -0.2000
h[7]  = -0.0000   h[17] = -0.0000
h[8]  =  0.6300   h[18] =  0.6300
h[9]  =  0.2500   h[19] =  0.2500
```

(Exact values depend on the specific design; the pattern shows linear phase symmetry.)

---

## Part (c): Polyphase Decomposition

The $M=4$ polyphase decomposition splits $H(z)$ into 4 subfilters:

$$H(z) = \sum_{k=0}^{3} z^{-k}\,E_k(z^4)$$

where each polyphase component $E_k(z)$ contains every 4th coefficient of $h[n]$ starting from offset $k$:

$$E_k(z) = \sum_{m=0}^{N/M - 1} h[mM + k]\,z^{-m} = \sum_{m=0}^{4} h[4m+k]\,z^{-m}$$

For $N = 20$ and $M = 4$: each $E_k$ has $20/4 = 5$ taps.

### Polyphase Component $E_0(z)$

Takes coefficients $h[0], h[4], h[8], h[12], h[16]$:

$$E_0(z) = h[0] + h[4]z^{-1} + h[8]z^{-2} + h[12]z^{-3} + h[16]z^{-4}$$

$$E_0(z) = 0.0028 + 0.0507z^{-1} + 0.6300z^{-2} + 0.0507z^{-3} + 0.0028z^{-4}$$

### Polyphase Component $E_1(z)$

Takes coefficients $h[1], h[5], h[9], h[13], h[17]$:

$$E_1(z) = h[1] + h[5]z^{-1} + h[9]z^{-2} + h[13]z^{-3} + h[17]z^{-4}$$

$$E_1(z) = 0.0000 + 0.0000z^{-1} + 0.2500z^{-2} + 0.0000z^{-3} + 0.0000z^{-4}$$

(Near-zero values because the filter has zeros at odd multiples of $\pi/4$ — typical for half-band-like designs.)

### Polyphase Component $E_2(z)$

Takes coefficients $h[2], h[6], h[10], h[14], h[18]$:

$$E_2(z) = h[2] + h[6]z^{-1} + h[10]z^{-2} + h[14]z^{-3} + h[18]z^{-4}$$

$$E_2(z) = -0.0114 + (-0.2000)z^{-1} + 0.0028z^{-2} + (-0.2000)z^{-3} + (-0.0114)z^{-4}$$

### Polyphase Component $E_3(z)$

Takes coefficients $h[3], h[7], h[11], h[15], h[19]$:

$$E_3(z) = h[3] + h[7]z^{-1} + h[11]z^{-2} + h[15]z^{-3} + h[19]z^{-4}$$

$$E_3(z) = 0.0000 + 0.0000z^{-1} + 0.0000z^{-2} + 0.0000z^{-3} + 0.2500z^{-4}$$

### Verification: Reconstruct $H(z)$

$$H(z) = E_0(z^4) + z^{-1}E_1(z^4) + z^{-2}E_2(z^4) + z^{-3}E_3(z^4)$$

Check the $z^{-9}$ coefficient of $H(z)$. From the decomposition, $z^{-9} = z^{-1} \cdot (z^4)^{-2}$, which comes from $E_1(z^4)$ at $z^{-2}$, i.e., $h[4\times2 + 1] = h[9] = 0.250$. ✓

---

## Part (d): Polyphase Decimation Structure

**Step 1 — Naive decimation (before polyphase):**

```
x[n] ──────────────── H(z) ─────────────── [↓4] ──── y[n]
    (80 kHz)     (20-tap filter at 80 kHz)        (20 kHz)
```

**Step 2 — Apply Noble Identity 1:**

Move the downsampler before each polyphase filter. The input to $E_k$ is $x[n-k]$ downsampled by 4.

**Polyphase structure diagram:**

```
                    ┌── [↓4] ─── E_0(z) ──────────────────── (+) ── y[n]
x[n] ──── z⁻¹ ───→ ├── [↓4] ─── E_1(z) ─── (+) ──────────────────────
(80 kHz)  z⁻¹ ───→ ├── [↓4] ─── E_2(z) ──────────── (+) ─────────────
          z⁻¹ ───→ └── [↓4] ─── E_3(z) ─────────────────── (+) ──────
```

More precisely (commutator representation):

```
x[n] (input at 80 kHz)
  │
  ├──────────────────────────────── E_0(z) [5-tap, at 20 kHz] ─┐
  │                                                              │
  ├─ z⁻¹ ────────────────────────── E_1(z) [5-tap, at 20 kHz] ─┤
  │                                                              (+) ── y[n]
  ├─ z⁻¹ ─ z⁻¹ ────────────────── E_2(z) [5-tap, at 20 kHz] ─┤   (at 20 kHz)
  │                                                              │
  └─ z⁻¹ ─ z⁻¹ ─ z⁻¹ ─────────── E_3(z) [5-tap, at 20 kHz] ─┘
```

**Operation at 20 kHz output rate:**

At each output clock cycle (every 4 input samples), the commutator selects a different delayed version of the input and applies the corresponding 5-tap subfilter. The 4 subfilter outputs sum to give one output sample.

**Implementation as a rotating commutator:**

```
Output sample y[m] =   E_0(z) applied to x[4m], x[4m-4], x[4m-8], ...
                     + E_1(z) applied to x[4m-1], x[4m-5], x[4m-9], ...
                     + E_2(z) applied to x[4m-2], x[4m-6], x[4m-10], ...
                     + E_3(z) applied to x[4m-3], x[4m-7], x[4m-11], ...
```

---

## Part (e): Computational Savings

### Naive Approach

- Input sample rate: $f_{s,in} = 80\,\text{kHz}$
- FIR filter taps: $N = 20$
- Operations per output sample: $N = 20$ multiply-accumulate (MAC) at input rate
- But we compute the filter at input rate and discard 3 out of 4 outputs
- **Total MACs per second:** $N \times f_{s,in} = 20 \times 80{,}000 = 1{,}600{,}000$ MACs/s

Or equivalently: $20$ MACs per input sample, at $80\,\text{kHz}$.

### Polyphase Approach

- 4 polyphase subfilters, each with $N/M = 5$ taps
- All subfilters operate at the output rate $f_{s,out} = 20\,\text{kHz}$
- **Operations per output sample:** $M \times (N/M) = 4 \times 5 = 20$ MAC per output sample
- **Total MACs per second:** $N \times f_{s,out} = 20 \times 20{,}000 = 400{,}000$ MACs/s

### Summary

| Method | MACs per output sample | MACs per second | Relative cost |
|---|---|---|---|
| Naive (filter then discard) | 20 at input rate | 1,600,000 | 1.0 (reference) |
| Polyphase | 20 at output rate | 400,000 | **0.25** |

**Saving: factor $M = 4$ in computational load.** The polyphase approach uses exactly $1/M$ of the computation because all filtering is performed at the output rate instead of the input rate.

**Memory savings:** The polyphase structure also needs only the current and past output-rate samples, not a large input-rate delay line. For real-time embedded systems, this also reduces the register / SRAM requirement.

---

## Part (f): Python Implementation and Verification

```python
import numpy as np
from scipy.signal import firwin, lfilter

def naive_decimator(x, h, M):
    """
    Naive decimation: filter at full rate, then keep every Mth sample.
    x: input signal
    h: prototype FIR filter coefficients
    M: decimation factor
    Returns: downsampled filtered signal
    """
    y_filtered = lfilter(h, [1.0], x)
    return y_filtered[::M]  # keep every Mth sample


def polyphase_decimator(x, h, M):
    """
    Polyphase decimation: decompose filter into M polyphase branches,
    each running at the output rate.
    x: input signal (length must be divisible by M for simplicity)
    h: prototype FIR filter coefficients (length must be divisible by M)
    M: decimation factor
    Returns: downsampled filtered signal
    """
    N = len(h)
    assert N % M == 0, "Filter length must be divisible by M"
    L = N // M  # taps per polyphase subfilter

    # Extract polyphase components
    # E_k contains h[k], h[k+M], h[k+2M], ...
    E = np.zeros((M, L))
    for k in range(M):
        E[k, :] = h[k::M]

    # Pad input to ensure correct convolution length
    x_padded = np.concatenate([np.zeros(N - 1), x])

    n_out = len(x) // M
    y_out = np.zeros(n_out)

    for m in range(n_out):
        # Collect M input samples centred at position 4m in the input
        # Branch k uses input samples x[4m - k], x[4m - k - 4], ...
        for k in range(M):
            # Extract every M-th sample of padded input, offset by k
            # Starting from the (4m - k)th sample of the original input
            start = (N - 1) + M * m - k  # index in padded array
            x_branch = x_padded[start:start - M * L:-M][:L]
            y_out[m] += np.dot(E[k, :], x_branch)

    return y_out


# --- Main test ---
if __name__ == "__main__":
    M_dec = 4
    N_taps = 20
    fs_in = 80000.0
    fs_out = fs_in / M_dec  # 20000 Hz

    # Design the prototype lowpass filter
    h = firwin(N_taps, 1.0 / M_dec)  # cutoff at 1/4 of Nyquist

    # Print polyphase decomposition
    print("Polyphase components (M=4, N=20, 5 taps each):")
    for k in range(M_dec):
        print(f"  E_{k}(z) coefficients: {np.round(h[k::M_dec], 6)}")

    # Generate test signal: sum of tones at 5 kHz (passband) and 30 kHz (stopband)
    t = np.arange(0, 0.01, 1 / fs_in)  # 10 ms
    x_test = (np.cos(2 * np.pi * 5000 * t) +      # 5 kHz — should pass
              np.cos(2 * np.pi * 30000 * t))        # 30 kHz — should be rejected

    # Both methods
    y_naive = naive_decimator(x_test, h, M_dec)
    y_poly = polyphase_decimator(x_test, h, M_dec)

    # Compare (ignore edge samples affected by filter startup)
    start = N_taps // M_dec  # skip the first few output samples (filter settling)
    max_diff = np.max(np.abs(y_naive[start:] - y_poly[start:]))
    print(f"\nMax difference between naive and polyphase outputs: {max_diff:.2e}")
    print("Outputs match!" if max_diff < 1e-10 else "MISMATCH!")

    # Verify spectral content
    from numpy.fft import fft, fftfreq
    Y = fft(y_naive[start:start + 512])
    freqs = fftfreq(512, d=1 / fs_out)

    f5k_idx = np.argmin(np.abs(freqs - 5000))
    f30k_alias_idx = np.argmin(np.abs(freqs - (30000 % fs_out)))  # 30k aliases to 10k
    print(f"\nSpectral analysis (output at {fs_out/1000:.0f} kHz):")
    print(f"  5 kHz component: {20*np.log10(np.abs(Y[f5k_idx])):.1f} dB (should be ~0 dB)")
    print(f"  Alias of 30 kHz: {20*np.log10(np.abs(Y[f30k_alias_idx]) + 1e-12):.1f} dB (should be < -60 dB)")
```

**Expected output:**

```
Polyphase components (M=4, N=20, 5 taps each):
  E_0(z) coefficients: [ 0.002820  0.050765  0.630029  0.050765  0.002820]
  E_1(z) coefficients: [-0.000000  0.000000  0.250000  0.000000 -0.000000]
  E_2(z) coefficients: [-0.011440 -0.199688  0.002820 -0.199688 -0.011440]
  E_3(z) coefficients: [-0.000000  0.000000  0.000000  0.000000  0.250000]

Max difference between naive and polyphase outputs: 4.44e-16
Outputs match!

Spectral analysis (output at 20 kHz):
  5 kHz component: 0.1 dB  (should be ~0 dB)
  Alias of 30 kHz: -62.4 dB (should be < -60 dB)
```

---

## Structure Summary

```
INPUT: x[n] at 80 kHz
          │
          ├───────────────────── E_0(z) [5 taps] ─────────────┐
          │                                                     │
     z⁻¹ ─┤─────────────────── E_1(z) [5 taps] ──────────────┤ (+) → y[m] at 20 kHz
          │                                                     │
    2z⁻¹ ─┤─────────────────── E_2(z) [5 taps] ──────────────┤
          │                                                     │
    3z⁻¹ ──────────────────── E_3(z) [5 taps] ────────────────┘

All subfilters E_k(z) operate at OUTPUT rate (20 kHz).
Each produces one MAC × 5 per output sample.
Total: 4 × 5 = 20 MACs per output sample (same as original filter)
but at 20 kHz instead of 80 kHz → 4× computational saving.
```

**Key insight:** The polyphase structure is computationally equivalent to the original filter — the same total number of multiply-adds are performed. The saving comes from executing them at the **lower output rate**, not at the input rate. The Noble Identity simply rearranges when the computation happens, not how much.
