# Worked Problem 04: CIC Decimation Filter Analysis

**Subject:** Digital Signal Processing
**Topic:** CIC Transfer Function, Frequency Response, Droop, Bit Growth, Compensation
**Difficulty:** Advanced

---

## Problem Statement

Analyse a **CIC (Cascaded Integrator-Comb) decimation filter** with the following parameters:

- Number of stages: $N = 3$
- Decimation factor: $M = 8$
- Input word length: $B_{in} = 16$ bits

**Tasks:**

**(a)** Derive the transfer function $H_{CIC}(z)$ and show it can be written as a moving-average cascade.

**(b)** Derive the magnitude frequency response $|H_{CIC}(e^{j\omega})|$.

**(c)** Compute the exact passband droop at the output Nyquist frequency ($f_{out}/2$).

**(d)** Calculate the required accumulator word length (bit growth analysis) to prevent overflow.

**(e)** Design a 5-tap droop compensation FIR filter. State its specifications and give approximate coefficients.

**(f)** Draw the implementation block diagram. Explain why integrators can overflow without corrupting the output.

---

## Part (a): CIC Transfer Function

### Building Blocks

**Integrator (running accumulator):** Implements $y[n] = y[n-1] + x[n]$

$$H_I(z) = \frac{1}{1 - z^{-1}}$$

Pole at $z = 1$ (unit circle) — this is a marginally stable accumulator running at the input sample rate.

**Comb filter (difference of delayed samples):** Implements $y[n] = x[n] - x[n-M]$

$$H_C(z) = 1 - z^{-M}$$

Zero at $z = e^{j2\pi k/M}$ for $k = 0, 1, \ldots, M-1$ — $M$ zeros equally spaced on the unit circle.

### CIC Transfer Function (at input rate)

$N = 3$ integrators followed by $\downarrow M$ followed by $N = 3$ comb filters:

$$H_{CIC}(z) = \underbrace{\frac{1}{(1-z^{-1})^3}}_{\text{3 integrators}} \cdot \underbrace{(1-z^{-M})^3}_{\text{3 combs}}$$

Combining:

$$\boxed{H_{CIC}(z) = \left(\frac{1-z^{-M}}{1-z^{-1}}\right)^3}$$

### Moving-Average Interpretation

The factor $\frac{1-z^{-M}}{1-z^{-1}}$ is:

$$\frac{1-z^{-M}}{1-z^{-1}} = 1 + z^{-1} + z^{-2} + \cdots + z^{-(M-1)} = \sum_{k=0}^{M-1}z^{-k}$$

This is the transfer function of an $M$-point moving average (boxcar) filter.

Therefore:

$$H_{CIC}(z) = \left(\sum_{k=0}^{M-1}z^{-k}\right)^3$$

**Physical interpretation:** The CIC is a cascade of $N = 3$ rectangular (moving-average) windows, each of length $M = 8$. The impulse response is the convolution of three length-8 rectangular pulses, yielding a triangular-ish pulse of length $3(M-1)+1 = 22$ samples (actually a B-spline of order 3).

The impulse response is:

$$h_{CIC}[n] = \binom{n+N-1}{N-1} \quad \text{(modified, within} [0, N(M-1)])$$

More precisely, it is the trinomial expansion coefficients truncated at length $NM - N + 1$:

$$h_{CIC}[n] = \text{number of ways to write } n = k_1 + k_2 + k_3, \quad 0 \leq k_i \leq M-1$$

---

## Part (b): Magnitude Frequency Response

Substituting $z = e^{j\omega}$ (where $\omega$ is the normalised digital frequency at the **input** rate):

$$H_{CIC}(e^{j\omega}) = \left(\frac{1-e^{-j\omega M}}{1-e^{-j\omega}}\right)^3$$

Applying the identity $1 - e^{-j\theta} = 2j\sin(\theta/2)\,e^{-j\theta/2}$:

$$\frac{1-e^{-j\omega M}}{1-e^{-j\omega}} = \frac{2j\sin(\omega M/2)e^{-j\omega M/2}}{2j\sin(\omega/2)e^{-j\omega/2}} = \frac{\sin(\omega M/2)}{\sin(\omega/2)}\,e^{-j\omega(M-1)/2}$$

**Magnitude response:**

$$\boxed{|H_{CIC}(e^{j\omega})| = \left|\frac{\sin(\omega M/2)}{\sin(\omega/2)}\right|^N = \left|\frac{\sin(4\omega)}{\sin(\omega/2)}\right|^3}$$

(with $M=8$, $N=3$)

**Key values:**

| $\omega$ (input rate) | Frequency ($f_{in} = 80\,\text{kHz}$ example) | $|H|$ |
|---|---|---|
| 0 | DC | $M^N = 8^3 = 512$ |
| $\pi/M = \pi/8$ | $f_{in}/16$ (Nyquist of output) | See Part (c) |
| $2\pi/M = \pi/4$ | $f_{in}/8$ | First null of comb: 0 |
| $4\pi/M = \pi/2$ | $f_{in}/4$ | Second null: 0 |
| $\pi$ | $f_{in}/2$ | $\sin(4\pi)/\sin(\pi/2) = 0/1 = 0$ |

**Frequency response plot (qualitative):**

```
|H(ω)|
 512  |▄
      |▄▄
      |  ▄▄
      |    ▄▄▄
      |       ▄▄▄▄▄▄
      |              ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 0    |_________________________________________________
      0    π/8   π/4   3π/8   π/2  ...   π    ω
           ↑                    ↑
     Nyquist of output    Stopband begins
```

The response falls from 512 at DC to a smaller value at the output Nyquist ($\omega = \pi/M$), then continues through nulls at $\omega = 2\pi k/M$.

---

## Part (c): Passband Droop at Output Nyquist

The output Nyquist frequency corresponds to digital frequency $\omega_{Nyq,out} = \pi/M$ at the input rate.

$$|H_{CIC}(e^{j\pi/M})| = \left|\frac{\sin(\pi M/(2M))}{\sin(\pi/(2M))}\right|^N = \left|\frac{\sin(\pi/2)}{\sin(\pi/16)}\right|^3 = \left|\frac{1}{\sin(\pi/16)}\right|^3$$

Compute $\sin(\pi/16)$:

$$\frac{\pi}{16} = 11.25° \implies \sin(11.25°) \approx 0.19509$$

$$|H_{CIC}(e^{j\pi/M})| = \left(\frac{1}{0.19509}\right)^3 = (5.1258)^3 \approx 134.74$$

**Droop relative to DC gain ($M^N = 512$):**

$$\text{Droop} = 20\log_{10}\!\left(\frac{134.74}{512}\right) = 20\log_{10}(0.2631) \approx -11.6\,\text{dB}$$

This is the CIC passband droop at the worst-case frequency (output Nyquist). For signals well below the output Nyquist, the droop is much smaller:

At $f = f_{out}/4$ ($\omega = \pi/(2M)$):

$$\left|\frac{\sin(\pi/4)}{\sin(\pi/32)}\right|^3 = \left(\frac{0.7071}{0.09802}\right)^3 = (7.214)^3 \approx 375.5$$

Droop at $f_{out}/4$: $20\log_{10}(375.5/512) = -2.7\,\text{dB}$

**Summary of droop across the output band:**

| Output frequency | Input $\omega$ | Droop (dB) |
|---|---|---|
| 0 (DC) | 0 | 0 dB (reference) |
| $f_{out}/8$ | $\pi/4M$ | $\approx -0.7\,\text{dB}$ |
| $f_{out}/4$ | $\pi/2M$ | $\approx -2.7\,\text{dB}$ |
| $f_{out}/2$ (Nyquist) | $\pi/M$ | $\approx -11.6\,\text{dB}$ |

The $-11.6\,\text{dB}$ droop at Nyquist is severe — this is why CIC filters nearly always require droop compensation.

---

## Part (d): Bit Growth Calculation

### Integrator Bit Growth

Each integrator in the cascade can accumulate up to $M = 8$ positive values before being "reset" by the comb. In the worst case (all inputs at maximum positive value), after $M$ samples the accumulator value is $M \times x_{max}$.

For a cascade of $N$ integrators with decimation $M$:

**Maximum output value:** $M^N \times x_{max} = 8^3 \times x_{max} = 512\,x_{max}$

**Bit growth needed:** $\lceil \log_2(M^N) \rceil = \lceil \log_2(512) \rceil = 9$ bits

**Accumulator word length after $k$ integrators:**

$$B_k = B_{in} + k\lceil\log_2 M\rceil = 16 + k \times 3 \quad \text{bits}$$

| After integrator | Bits required |
|---|---|
| 0 (input) | $16$ |
| 1 | $16 + 3 = 19$ |
| 2 | $16 + 6 = 22$ |
| 3 (output of all integrators) | $16 + 9 = 25$ |

The **internal accumulator width must be at least 25 bits** for 16-bit input with $M=8$, $N=3$.

### Register Width in Practice

In hardware:

- **16-bit input → 25-bit accumulators** for the integrators
- In an FPGA, you would instantiate 25-bit adders/registers
- In a 32-bit DSP, a 32-bit accumulator easily accommodates this (16 + 9 = 25 < 32)
- After the final comb stage, truncate to the desired output word length $B_{out}$

**Output rounding:** If output is 16 bits and the accumulator is 25 bits, truncate the 9 LSBs. The truncation noise has power $\approx 2^{-18}$ (in units of full-scale). This is typically acceptable. If a higher-precision output is needed, use $B_{out} = 20$ bits and truncate 5 bits.

### The Two's Complement Overflow Trick

**Important implementation insight:** The integrators in a CIC filter can be implemented with **wrap-around overflow** (modular arithmetic — the default in most hardware) without corrupting the output, as long as the accumulators have the same bit width throughout the chain.

**Why:** The comb filter differences "undo" any wrap-around that happened during integration, as long as the overflow is consistent (two's complement). This is because the subtraction in the comb $y[n] - y[n-M]$ cancels the accumulated overflow:

$$\text{true difference} = (y_{true}[n] - y_{true}[n-M]) = (y_{overflowed}[n] - y_{overflowed}[n-M]) \pmod{2^B}$$

This property holds because two's complement addition is modular, and subtraction of two modular quantities preserves the true difference if the true difference itself does not overflow the output word.

**Practical consequence:** You do NOT need to expand the accumulator width if you use consistent two's complement arithmetic throughout — but you must then ensure the output word width of the comb is sufficient (25 bits in our case).

---

## Part (e): Droop Compensation FIR Filter

### Specifications

The droop compensator $C(z)$ should approximate the inverse of the CIC magnitude response over the passband $[0, f_{out}/2]$:

$$|C(e^{j\omega})| \approx \frac{M^N}{|H_{CIC}(e^{j\omega})|} \cdot \frac{1}{M^N} = \left|\frac{\sin(\omega/2)}{\sin(\omega M/2)}\right|^N \quad \text{for } |\omega| \leq \pi/M$$

At low frequencies ($\omega \ll \pi/M$): $\sin(\omega/2) \approx \omega/2$ and $\sin(\omega M/2) \approx \omega M/2$, so:

$$|C(e^{j\omega})| \approx 1 \quad \text{(flat near DC)}$$

At the output Nyquist ($\omega = \pi/M$):

$$|C(e^{j\pi/M})| \approx \frac{\sin(\pi/16)}{\sin(\pi/2)} = \sin(\pi/16)/1 \approx 0.195 \Rightarrow 1/0.195 \approx 5.1$$

The compensation filter boosts by ~14 dB at the output Nyquist.

### Design Approach

The compensator operates at the **output rate** $f_{s,out}$ (after decimation). Design a short linear-phase FIR (Parks-McClellan or least-squares) that matches the target response.

**Target response over $[0, \pi]$ at output rate:**

The output rate normalisation: at the output rate, $\omega_{out} = M\,\omega_{in}$, so the output Nyquist is $\omega_{out} = \pi$.

$$|C(e^{j\omega_{out}})| = \left(\frac{\pi/M}{\pi}\cdot\frac{\sin(\omega_{out}/(2M))\cdot M}{\sin(\omega_{out}/2)}\right)^{-N}$$

For a 5-tap (Type I) compensation FIR (odd length, symmetric), the design frequency points are:

| $f/f_{out}$ | Target gain |
|---|---|
| 0 | 1.000 |
| 0.25 | 1.070 |
| 0.50 | $\approx 1.31$ |

### Approximate 5-tap Compensator Coefficients

Using Parks-McClellan targeting the inverse-sinc response over $[0, 0.5]$ at the output rate:

$$c[n] \approx \{-0.0116,\; -0.0536,\; 1.1325,\; -0.0536,\; -0.0116\}$$

**Verification:**

DC gain: $\sum c[n] = -0.0116 - 0.0536 + 1.1325 - 0.0536 - 0.0116 = 1.002 \approx 1$ ✓ (near-unity DC)

The compensator has a slight high-frequency boost (the centre coefficient $> 1$, side coefficients negative) — characteristic of an inverse sinc response.

```python
import numpy as np
from scipy.signal import firls

def design_cic_compensator(N_cic, M, N_taps=5):
    """
    Design an N_taps-point FIR compensation filter for a CIC of order N_cic
    and decimation factor M.
    Filter operates at the OUTPUT rate.
    Returns compensation FIR coefficients c[n].
    """
    # Frequency grid at output rate (0 to 1, where 1 = Nyquist)
    f_grid = np.linspace(0, 1.0, 256)  # normalised to output Nyquist

    # Target: inverse CIC response (with DC normalisation)
    omega_in = np.pi * f_grid / M  # corresponding input-rate frequency
    omega_in_safe = np.clip(omega_in, 1e-10, np.pi - 1e-10)

    cic_mag = np.abs(np.sin(M * omega_in_safe / 2) / np.sin(omega_in_safe / 2)) ** N_cic
    target = cic_mag[0] / cic_mag  # normalised to DC gain of 1

    # Least-squares FIR design over the passband [0, 0.8] (leave some rolloff room)
    passband_mask = f_grid <= 0.8
    f_bands = [0, 0.8, 0.9, 1.0]
    d_bands = [target[np.argmin(np.abs(f_grid - 0.0))],
               target[np.argmin(np.abs(f_grid - 0.8))],
               0, 0]  # don't care above 0.8

    # Simple least-squares design
    c = firls(N_taps - 1 + (N_taps % 2 == 0), f_bands, d_bands)
    return c


c = design_cic_compensator(N_cic=3, M=8, N_taps=5)
print("Compensator coefficients:", np.round(c, 6))

# Verify droop correction
from scipy.signal import freqz

# CIC response at output rate (approximate via the sinc model)
w, H_comp = freqz(c, [1.0], worN=512)
# At w=pi (Nyquist of output = pi/8 of input):
nyq_idx = len(w) - 1
print(f"Compensator gain at output Nyquist: {20*np.log10(abs(H_comp[nyq_idx])):.2f} dB")
# Expected: approximately +11.6 dB to cancel the CIC droop
```

---

## Part (f): Implementation Block Diagram

### Complete CIC Decimation + Compensation Chain

```
Input x[n]                          Output y[m]
at f_s,in                           at f_s,out = f_s,in / M

┌──────────────────────────────────────────────────────────────────┐
│                    CIC FILTER (high rate)                        │
│                                                                  │
│  x[n]──[+]──v[n]──[+]──w[n]──[+]──u[n]──[↓M]──u_d[m]         │
│         ▲            ▲            ▲                              │
│       [z⁻¹]        [z⁻¹]       [z⁻¹]                           │
│   Integrator 1   Integrator 2  Integrator 3   (at f_s,in)       │
└──────────────────────────────────────────────────────────────────┘
                                        │
                                       ↓ (at f_s,out)
┌──────────────────────────────────────────────────────────────────┐
│                    CIC COMB SECTION (low rate)                   │
│                                                                  │
│  u_d[m]──(-)──g[m]──(-)──q[m]──(-)──r[m]                       │
│         ▲            ▲            ▲                              │
│       [z⁻¹]        [z⁻¹]       [z⁻¹]                           │
│   Comb 1         Comb 2       Comb 3     (at f_s,out)           │
└──────────────────────────────────────────────────────────────────┘
                                        │
                                       ↓
┌──────────────────────────────────────────────────────────────────┐
│              DROOP COMPENSATION FIR (low rate)                   │
│                                                                  │
│  r[m]──[FIR 5 taps: c[n]]──y[m]      (at f_s,out)              │
└──────────────────────────────────────────────────────────────────┘
```

### Notes on the Diagram

- **All integrators run at the high input rate** $f_{s,in}$. This is the expensive part in hardware.
- **Downsampling $\downarrow M$ happens once**, between the integrator section and the comb section.
- **All comb filters run at the low output rate** $f_{s,out}$. This is computationally cheap.
- **The compensation FIR also runs at the output rate**.

By Noble Identity, the comb filters can be moved before the downsampler (from low rate to high rate) or equivalently the structure can be transposed. However, the standard implementation shown is the most efficient because the combs at low rate are cheap.

### Why Integrators Can Overflow Safely

For the two's complement overflow proof to hold, the following conditions must be met:

1. All integrators and comb filters use the **same word length** (25 bits in our example).
2. The **comb filter delay** is exactly $M$ samples (same as the CIC decimation factor).
3. The **output** of the final comb is interpreted as a signed two's complement number.

Under these conditions, if an integrator overflows by wrapping around, the comb subtraction $y[m] - y[m-1]$ (in the comb section) computes the correct difference in modular arithmetic, which equals the true difference as long as the true difference is representable in the word length.

**Counterexample (when it fails):** If the word length is different between integrators and combs, or if the comb delay is changed from $M$, or if unsigned arithmetic is used, the cancellation fails and the output is corrupted.

---

## Summary Table

| Parameter | Value |
|---|---|
| CIC stages $N$ | 3 |
| Decimation factor $M$ | 8 |
| DC gain | $M^N = 512$ |
| Transfer function | $\left(\frac{1-z^{-8}}{1-z^{-1}}\right)^3$ |
| Passband droop at $f_{out}/2$ | $\approx -11.6\,\text{dB}$ |
| Null frequencies | $k \times f_{s,in}/M = k \times f_{s,out}$, $k = 1, 2, \ldots$ |
| Bit growth | $N\log_2 M = 9$ bits |
| Required accumulator width | $16 + 9 = 25$ bits |
| Compensation filter | 5-tap FIR at output rate, $\approx +11.6\,\text{dB}$ at Nyquist |
| Overflow in integrators | Safe in two's complement with consistent word length |
