# IIR Filter Design — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** IIR Properties, Bilinear Transform, Impulse Invariance, Butterworth/Chebyshev/Elliptic, SOS
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. What are the key properties and trade-offs of IIR filters compared to FIR filters?

**Answer:**

An **IIR (Infinite Impulse Response)** filter has a recursive difference equation:

$$y[n] = \sum_{k=0}^{M} b_k\,x[n-k] - \sum_{k=1}^{N} a_k\,y[n-k]$$

The feedback terms ($a_k$) sustain the impulse response indefinitely.

**Advantages of IIR:**

1. **Low computational cost:** A sharp lowpass filter that requires 100+ FIR taps can often be achieved with 4–8 IIR coefficients. Computation scales as $O(N)$ per output sample where $N$ is the filter order.
2. **Well-established analog prototypes:** Butterworth, Chebyshev, and elliptic designs are directly converted from mature analog filter design theory.
3. **Efficient hardware implementation:** Fewer multiply-accumulate operations and smaller coefficient tables.

**Disadvantages of IIR:**

1. **Conditional stability:** Poles must be inside the unit circle. Coefficient quantisation can push poles outside, destabilising the filter.
2. **Non-linear phase:** IIR filters (other than trivial cases) cannot achieve linear phase response. Group delay is frequency-dependent.
3. **Limit cycle oscillations:** In fixed-point implementations, feedback can cause the output to oscillate at low amplitude even with zero input.
4. **Transient duration:** The impulse response decays asymptotically, so there is always a startup transient.

| Property | FIR | IIR |
|---|---|---|
| Stability | Always | Conditional |
| Phase | Exact linear phase achievable | Non-linear |
| Order for sharp cutoff | High (100s) | Low (single digits) |
| Computational cost | High | Low |
| Quantisation effects | Mild | Limit cycles, instability |

---

### Q2. Describe the three classic analog prototype filter families: Butterworth, Chebyshev Type I, and Elliptic.

**Answer:**

All three are lowpass prototypes with cutoff $\Omega_c = 1$ rad/s (normalised), designed to different error-minimisation criteria.

**Butterworth (maximally flat):**

$$|H_a(j\Omega)|^2 = \frac{1}{1 + (\Omega/\Omega_c)^{2N}}$$

- Maximally flat at $\Omega = 0$: no ripple in the passband
- Monotonically decreasing — no ripple anywhere
- Roll-off: $-20N$ dB/decade, $-6N$ dB/octave
- For given specs, requires the highest filter order of the three families
- All poles on a circle of radius $\Omega_c$ in the left half-plane, equally spaced at angles $\pi(2k+N-1)/(2N)$

**Chebyshev Type I:**

$$|H_a(j\Omega)|^2 = \frac{1}{1 + \epsilon^2\,T_N^2(\Omega/\Omega_c)}$$

where $T_N$ is the Chebyshev polynomial of degree $N$. Equiripple in the passband, monotone in the stopband.

- Passband ripple: $\delta_p = 1/\sqrt{1+\epsilon^2}$
- Lower filter order than Butterworth for same stopband attenuation + passband ripple spec
- Steeper transition at the cost of passband ripple

**Elliptic (Cauer):**

Equiripple in **both** passband and stopband. This is the optimal design for minimum filter order given all four constraints ($\omega_p$, $\omega_s$, $\delta_p$, $\delta_s$).

- Requires the fewest poles of any analog lowpass filter for given specifications
- Poles and zeros; the zeros on the imaginary axis create the equiripple stopband behaviour
- Most complex to design (but widely available in toolboxes)

**Order comparison for same specs (typical):**

| Type | Order required |
|---|---|
| Butterworth | Highest |
| Chebyshev I/II | Moderate |
| Elliptic | Lowest |

---

### Q3. What is the bilinear transform? State the mapping and explain the frequency warping effect.

**Answer:**

The **bilinear transform** maps a continuous-time (Laplace) transfer function $H_a(s)$ to a discrete-time (z-domain) transfer function $H(z)$ by the substitution:

$$s = \frac{2}{T_s}\cdot\frac{1 - z^{-1}}{1 + z^{-1}} = \frac{2}{T_s}\cdot\frac{z - 1}{z + 1}$$

or equivalently $z = \frac{1 + sT_s/2}{1 - sT_s/2}$.

**Frequency relationship:**

On the imaginary axis $s = j\Omega$ (analog) and unit circle $z = e^{j\omega}$ (digital):

$$j\Omega = \frac{2}{T_s}\cdot\frac{e^{j\omega} - 1}{e^{j\omega} + 1} = \frac{2}{T_s}\cdot\frac{e^{j\omega/2} - e^{-j\omega/2}}{e^{j\omega/2} + e^{-j\omega/2}} = j\frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)$$

$$\Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)$$

Inverting: $\omega = 2\arctan\!\left(\frac{\Omega T_s}{2}\right)$

**Frequency warping:** The relationship between digital frequency $\omega$ and analog frequency $\Omega$ is **nonlinear** (tangent function). The entire analog frequency axis $(-\infty, +\infty)$ is compressed into the digital range $(-\pi, \pi)$.

**Consequence:** If you want a digital cutoff at $\omega_c$, you must design the analog prototype for the **pre-warped** analog frequency:

$$\Omega_c = \frac{2}{T_s}\tan\!\left(\frac{\omega_c}{2}\right)$$

**Key advantage:** The bilinear transform has **no aliasing** (unlike impulse invariance) because it maps the entire left half-plane to the interior of the unit circle — a one-to-one mapping.

---

## Intermediate

### Q4. Outline the complete design procedure for a digital IIR Butterworth lowpass filter using the bilinear transform.

**Answer:**

**Given:** Digital passband edge $\omega_p$, stopband edge $\omega_s$, passband ripple $R_p$ (dB), stopband attenuation $A_s$ (dB), sample rate $f_s$.

**Step 1 — Pre-warp the digital specifications:**

$$\Omega_p = \frac{2}{T_s}\tan\!\left(\frac{\omega_p}{2}\right), \qquad \Omega_s = \frac{2}{T_s}\tan\!\left(\frac{\omega_s}{2}\right)$$

**Step 2 — Determine Butterworth filter order:**

The selectivity factor: $k = \Omega_p/\Omega_s$.

The attenuation requirements:

$$\epsilon_p = \sqrt{10^{R_p/10}-1}, \qquad \epsilon_s = \sqrt{10^{A_s/10}-1}$$

Minimum order:

$$N = \left\lceil\frac{\log(\epsilon_s/\epsilon_p)}{\log(\Omega_s/\Omega_p)}\right\rceil = \left\lceil\frac{\log(10^{A_s/10}-1) - \log(10^{R_p/10}-1)}{2\log(\Omega_s/\Omega_p)}\right\rceil$$

**Step 3 — Compute the analog prototype cutoff:**

Set the passband cutoff to match the passband ripple exactly:

$$\Omega_c = \frac{\Omega_p}{\epsilon_p^{1/N}} = \frac{\Omega_p}{(10^{R_p/10}-1)^{1/(2N)}}$$

**Step 4 — Find analog prototype poles:**

Butterworth poles at:

$$s_k = \Omega_c\,\exp\!\left(j\frac{\pi(2k+N-1)}{2N}\right), \quad k = 1, 2, \ldots, N$$

(left half-plane poles only)

**Step 5 — Construct $H_a(s)$:**

$$H_a(s) = \frac{\Omega_c^N}{\prod_{k=1}^{N}(s - s_k)}$$

**Step 6 — Apply bilinear transform:**

Substitute $s = \frac{2}{T_s}\cdot\frac{1-z^{-1}}{1+z^{-1}}$ into $H_a(s)$ to get $H(z)$.

Each analog pole $s_k$ maps to a digital pole:

$$z_k = \frac{1 + s_k T_s/2}{1 - s_k T_s/2}$$

**Step 7 — Implement as cascaded second-order sections** (see filter_structures.md).

---

### Q5. What is impulse invariance? Why does it suffer from aliasing and when is it still appropriate?

**Answer:**

**Impulse invariance** maps an analog filter $H_a(s)$ to a digital filter $H(z)$ by requiring the digital impulse response to be a sampled version of the analog impulse response:

$$h[n] = T_s\,h_a(nT_s)$$

For a partial fraction expansion $H_a(s) = \sum_k \frac{A_k}{s - s_k}$, the analog impulse response is:

$$h_a(t) = \sum_k A_k\,e^{s_k t}\,u(t)$$

The digital transfer function is:

$$H(z) = \sum_k \frac{A_k\,T_s}{1 - e^{s_k T_s}z^{-1}}$$

**Frequency domain relationship:**

$$H(e^{j\omega}) = \sum_{r=-\infty}^{\infty} H_a\!\left(j\frac{\omega - 2\pi r}{T_s}\right)$$

The digital frequency response is the sum of shifted copies of the analog response — **aliasing occurs** whenever $H_a(j\Omega) \neq 0$ for $|\Omega| > \pi/T_s$.

**Why it suffers from aliasing:**

Unlike the bilinear transform (which compresses the entire analog axis to $(-\pi, \pi)$), impulse invariance maps frequency linearly: $\omega = \Omega T_s$. Frequencies above $\pi/T_s$ alias into $[0, \pi]$.

**When it is still appropriate:**

1. **Bandlimited analog prototypes:** Elliptic and other analog filters are not bandlimited; aliasing from the stopband wraps back into the passband. Impulse invariance is suitable only for filters that are sufficiently attenuated above $\Omega_s \ll \pi/T_s$.
2. **Lowpass and bandpass (not highpass):** For a lowpass filter sampled at a rate much higher than the cutoff, the alias from the stopband is negligible.
3. **When time-domain shape matters more than frequency response:** If the design goal is to match an analog system's step response (control systems, equalisation), impulse invariance directly matches the impulse response shape.

---

### Q6. Compare the frequency response characteristics of Butterworth, Chebyshev Type I, Chebyshev Type II, and Elliptic filters for the same specifications.

**Answer:**

**Butterworth:**
- Passband: monotonically decreasing (maximally flat at DC)
- Stopband: monotonically increasing attenuation
- No ripple in either band
- Roll-off rate: $-20N$ dB/decade
- Requires highest $N$ for given specs

**Chebyshev Type I:**
- Passband: equiripple (oscillates within $\pm\delta_p$)
- Stopband: monotonically increasing
- Lower $N$ than Butterworth for same passband ripple + stopband attenuation

**Chebyshev Type II:**
- Passband: monotonically decreasing (flat near DC)
- Stopband: equiripple
- Zeros on the imaginary axis create the stopband ripple
- Same order as Type I but with smooth passband (useful when passband flatness is critical)

**Elliptic:**
- Passband: equiripple
- Stopband: equiripple
- Zeros on imaginary axis (same as Cheb II) for sharp transition
- Requires lowest $N$ for given specs — optimal
- Most complex frequency response shape; sensitive to coefficient precision

**Graphical comparison (lowpass, normalised):**

```
|H|  Butterworth     Chebyshev I       Elliptic
1.0  _____________   ~~~~~~~~~~~~~~~   ~~~~~~~~~~~~~~~~~~
     |          \    ~~~         \    ~~~              ~~~
0.5  |           \      \        \      \             ~~~
     |            \      \        \      \         ~~~
0.0  |_____________\______\________\______\~~~~~~~~~
     0    ωp         ωs    ωp       ωs    ωp       ωs
```

---

## Advanced

### Q7. Explain second-order sections (SOS/biquads). Why are they preferred over direct-form high-order IIR implementation?

**Answer:**

A **second-order section (SOS)** or **biquad** is a second-order IIR filter:

$$H_k(z) = \frac{b_{k0} + b_{k1}z^{-1} + b_{k2}z^{-2}}{1 + a_{k1}z^{-1} + a_{k2}z^{-2}}$$

A high-order IIR filter of order $N = 2K$ is implemented as a cascade of $K$ biquads:

$$H(z) = \prod_{k=1}^{K} H_k(z)$$

**Reasons SOS is preferred:**

1. **Numerical stability:** A high-order polynomial (e.g., $N=10$, degree 10 denominator) is highly sensitive to coefficient quantisation — small errors in coefficients can move poles outside the unit circle. Second-order polynomials have only 2 poles each, and their sensitivity to coefficient errors is localised.

2. **Coefficient precision:** In 16-bit or 32-bit fixed-point arithmetic, representing the coefficients of a 10th-order filter precisely is extremely difficult. Biquad coefficients need far fewer bits.

3. **Independence of sections:** Each biquad is an independent filter. A pole mismatch in one section does not affect others.

4. **Easy debugging and tuning:** Individual sections can be measured, adjusted, or bypassed.

5. **Pole pairing:** Real poles are paired, and complex conjugate pairs go into one biquad. Optimal pairing (close poles with nearby zeros) minimises signal dynamic range within each section.

**Comparison of stability sensitivity:**

For a direct-form $N$th-order filter, the sensitivity of pole location to coefficient $a_k$ is:

$$\left|\frac{\partial p_m}{\partial a_k}\right| \propto \prod_{i \neq m} \frac{1}{|p_m - p_i|}$$

For poles clustered near the unit circle, $|p_m - p_i|$ can be very small, making the product enormous. SOS limits this to interactions within each second-order subsystem only.

---

### Q8. Describe the pole placement approach to IIR resonator and notch filter design.

**Answer:**

The geometric interpretation of the frequency response (distance from evaluation point on unit circle to poles and zeros) enables direct pole/zero placement for simple filters.

**Resonator (peaking filter):**

Place a complex conjugate pole pair at $z = r\,e^{\pm j\omega_0}$ where:
- $\omega_0$ = desired resonance frequency
- $r$ = radius, $0 < r < 1$ (closer to 1 = sharper peak, higher $Q$)

Add zeros at the origin (or at $z = \pm 1$ for flatness away from $\omega_0$):

$$H(z) = \frac{1 - z^{-2}}{1 - 2r\cos\omega_0\,z^{-1} + r^2\,z^{-2}}$$

The -3 dB bandwidth of the resonance is approximately:

$$\Delta\omega_{-3\text{dB}} \approx 2(1-r) \quad \text{(for } r \approx 1\text{)}$$

**Notch filter (band-reject):**

Place zeros exactly on the unit circle at $z = e^{\pm j\omega_0}$ (exact null at $\omega_0$) and poles at $z = r\,e^{\pm j\omega_0}$ slightly inside the unit circle to keep the response flat away from $\omega_0$:

$$H(z) = \frac{1 - 2\cos\omega_0\,z^{-1} + z^{-2}}{1 - 2r\cos\omega_0\,z^{-1} + r^2\,z^{-2}}$$

- At $\omega = \omega_0$: numerator $= 0 \Rightarrow |H| = 0$ (exact notch)
- Away from $\omega_0$: poles and zeros nearly cancel, $|H| \approx 1$
- Notch bandwidth $\approx 2(1-r)$ rad/sample

**Practical example:** 50 Hz (mains hum) removal at $f_s = 1000\,\text{Hz}$: $\omega_0 = 2\pi \times 50/1000 = 0.1\pi$. With $r = 0.95$: notch bandwidth $\approx 2(1-0.95) = 0.1$ rad/sample $\approx 8\,\text{Hz}$. The filter attenuates only frequencies within $\pm 4\,\text{Hz}$ of 50 Hz, leaving the rest of the spectrum intact.

```python
import numpy as np

def notch_filter(omega_0, r):
    """Return (b, a) coefficients for a notch filter."""
    b = [1, -2*np.cos(omega_0), 1]
    a = [1, -2*r*np.cos(omega_0), r**2]
    return np.array(b), np.array(a)

b, a = notch_filter(0.1*np.pi, 0.95)
# b: [1.000, -1.902, 1.000]
# a: [1.000, -1.807, 0.902]
```

---

### Q9. Discuss the effects of finite word length on IIR filter implementation. What are limit cycles and how are they prevented?

**Answer:**

**Coefficient quantisation:** Filter coefficients must be rounded to the nearest representable value in fixed-point or floating-point arithmetic. This moves the designed poles and zeros to nearby grid points. For a high-order IIR implemented directly, poles near the unit circle are extremely sensitive — a small coefficient error can move a pole outside the unit circle, making the filter unstable.

**Round-off noise:** Each multiply-accumulate operation introduces a rounding error. In IIR filters, this error is fed back through the recursion and can grow without bound for poles close to the unit circle (the noise is amplified by the resonant gain). The noise power at the output is proportional to:

$$\sigma_{noise}^2 \propto \frac{1}{1 - |p|^2}$$

for each pole $p$ — poles near the unit circle amplify quantisation noise dramatically.

**Limit cycles:** In fixed-point IIR implementations, the combination of nonlinear rounding and feedback can cause a sustained, low-amplitude oscillation of the output even with zero input. There are two types:

1. **Granular limit cycles:** Caused by rounding at the quantiser. The output settles into a periodic pattern rather than zero.
2. **Overflow oscillations:** Caused by arithmetic overflow in accumulators. Can be large amplitude and must be prevented by saturation arithmetic or scaling.

**Prevention strategies:**

1. **SOS decomposition:** Limits interactions between poles. Each biquad is stabilised independently.
2. **Scaling:** Scale intermediate signals to avoid overflow. L2 or L∞ scaling.
3. **Saturation arithmetic:** Use saturation (clamp at max/min) rather than wrap-around overflow — eliminates overflow oscillations.
4. **Zero-input limit cycle prevention:** Use magnitude truncation (round toward zero) instead of rounding to nearest. This guarantees zero-input limit cycles cannot occur in second-order sections if the poles are inside a certain region.
5. **Floating-point arithmetic:** Modern DSPs with 32-bit float or 64-bit double largely avoid these issues for orders up to $N \approx 10$.

---

## Quick Reference

| Design method | Maps | Aliasing | Linear phase | Use when |
|---|---|---|---|---|
| Bilinear transform | $s \to z$ via tangent | None | No | Standard IIR design |
| Impulse invariance | $h_a(t) \to h[n]$ | Yes | No | Bandlimited prototypes |

| Filter family | Passband | Stopband | Order |
|---|---|---|---|
| Butterworth | Flat | Monotone | Highest |
| Chebyshev I | Equiripple | Monotone | Medium |
| Chebyshev II | Monotone | Equiripple | Medium |
| Elliptic | Equiripple | Equiripple | Lowest |
