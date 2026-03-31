# FIR Filter Design — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** FIR Properties, Window Method, Parks-McClellan, Filter Types, Linear Phase
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. What are the defining properties of an FIR filter? Why is it always BIBO stable?

**Answer:**

An **FIR (Finite Impulse Response)** filter has an impulse response of finite duration:

$$h[n] = 0 \quad \text{for } n < 0 \text{ and } n \geq N$$

The system function is a polynomial in $z^{-1}$:

$$H(z) = \sum_{n=0}^{N-1} h[n]\,z^{-n} = h[0] + h[1]z^{-1} + \cdots + h[N-1]z^{-(N-1)}$$

**Key properties:**

1. **Always BIBO stable:** The impulse response sum is $\sum_{n=0}^{N-1}|h[n]| < \infty$ (finite sum of finite values). Every FIR filter is stable regardless of coefficient values.

2. **Non-recursive:** The difference equation $y[n] = \sum_{k=0}^{N-1}h[k]\,x[n-k]$ contains only input (feed-forward) terms. No feedback.

3. **Can have exact linear phase:** Symmetric or anti-symmetric coefficients guarantee a linear phase response.

4. **All poles at origin:** $H(z)$ has $N-1$ poles, all at $z = 0$ (trivially inside the unit circle — confirming stability).

5. **Zeros anywhere:** Zeros can be placed anywhere in the z-plane, including outside the unit circle, without affecting stability.

**Why stability is important:** In real-time systems, quantisation noise fed back through IIR recursion can cause limit cycle oscillations. FIR filters have no feedback path, so there is no mechanism for oscillation or instability from coefficient rounding.

---

### Q2. What are the four types of linear-phase FIR filters? State the symmetry conditions and any restrictions.

**Answer:**

Linear phase requires the impulse response to be either **symmetric** or **anti-symmetric** about its midpoint.

**Type I — Symmetric, Odd Length ($N$ odd)**

$$h[n] = h[N-1-n], \quad n = 0, 1, \ldots, N-1$$

- Group delay: $\tau = (N-1)/2$ samples (integer)
- Frequency response: $H(e^{j\omega}) = e^{-j\omega(N-1)/2}\,A(\omega)$ where $A(\omega)$ is real
- $A(\omega)$ is even and can take any value at $\omega = 0$ and $\omega = \pi$
- **Usable for:** Lowpass, highpass, bandpass, bandstop

**Type II — Symmetric, Even Length ($N$ even)**

$$h[n] = h[N-1-n]$$

- Group delay: $(N-1)/2$ — a half-integer number of samples
- $A(\pi) = 0$ always (the frequency response is zero at $\omega = \pi$)
- **Cannot be used for:** Highpass or bandstop filters (must have zero gain at $\omega = \pi$)

**Type III — Anti-symmetric, Odd Length**

$$h[n] = -h[N-1-n], \quad h[(N-1)/2] = 0$$

- $A(0) = A(\pi) = 0$ always
- **Useful for:** Differentiators, Hilbert transformers (where zero gain at DC is acceptable)

**Type IV — Anti-symmetric, Even Length**

$$h[n] = -h[N-1-n]$$

- $A(0) = 0$ always (zero at DC)
- **Useful for:** Differentiators, Hilbert transformers, wideband highpass (in a sense)
- Cannot be used for lowpass or bandstop

| Type | Length | Symmetry | Constraints | Typical use |
|---|---|---|---|---|
| I | Odd | Symmetric | None | LP, HP, BP, BS |
| II | Even | Symmetric | $H(\pi) = 0$ | LP, BP only |
| III | Odd | Anti-symmetric | $H(0) = H(\pi) = 0$ | Differentiator, Hilbert |
| IV | Even | Anti-symmetric | $H(0) = 0$ | Differentiator, Hilbert |

---

### Q3. Describe the windowed sinc design method. What are its steps and what limits its performance?

**Answer:**

**Design goal:** Approximate an ideal lowpass filter with cutoff $\omega_c$.

**Ideal response:** Brick-wall lowpass in frequency, sinc in time:

$$h_d[n] = \frac{\sin(\omega_c(n - \alpha))}{\pi(n - \alpha)}, \quad \alpha = \frac{N-1}{2}$$

where $\alpha$ is the delay required for causality.

**Steps:**

1. **Specify** passband edge $\omega_p$, stopband edge $\omega_s$, and desired ripple levels $\delta_p$ (passband) and $\delta_s$ (stopband).

2. **Choose a window** $w[n]$ of length $N$ based on the required stopband attenuation:
   - Rectangular: $A_s = 21\,\text{dB}$ — rarely sufficient
   - Hanning: $A_s = 44\,\text{dB}$
   - Hamming: $A_s = 53\,\text{dB}$
   - Blackman: $A_s = 74\,\text{dB}$
   - Kaiser: $A_s$ controlled by $\beta$ parameter

3. **Set cutoff** at the arithmetic mean of passband and stopband edges:
   $$\omega_c = \frac{\omega_p + \omega_s}{2}$$

4. **Compute windowed impulse response:**
   $$h[n] = h_d[n]\cdot w[n], \quad n = 0, 1, \ldots, N-1$$

5. **Estimate filter order** (transition bandwidth $\Delta\omega = \omega_s - \omega_p$):
   - Hanning: $N \approx 8\pi/\Delta\omega$
   - Hamming: $N \approx 8\pi/\Delta\omega$
   - Blackman: $N \approx 12\pi/\Delta\omega$
   - Kaiser: $N \approx (A_s - 8)/(2.285\,\Delta\omega)$

**Limitations:**

- The window method is **sub-optimal**: it does not minimise the filter order for given ripple specifications. A Parks-McClellan design achieves the same attenuation with fewer taps.
- The method cannot independently control passband and stopband ripples (the window determines both simultaneously).
- Passband and stopband ripples are equal (equiripple in both bands) — this is rarely the actual requirement.

---

## Intermediate

### Q4. Describe the Parks-McClellan algorithm. What optimality criterion does it use, and why is it preferred over the window method?

**Answer:**

**Optimality criterion — Chebyshev (minimax) approximation:**

Parks-McClellan (Remez exchange algorithm) finds the FIR filter coefficients that **minimise the maximum weighted error** between the desired response $D(\omega)$ and the actual response $H(e^{j\omega})$:

$$\min_{\{h[n]\}} \max_{\omega \in \Omega} W(\omega)\left|D(\omega) - H(e^{j\omega})\right|$$

where $W(\omega)$ is a user-specified frequency weighting function and $\Omega$ is the union of passband and stopband regions (transition band excluded).

**Why it is optimal:**

By the Chebyshev equiripple theorem, the optimal solution achieves an **equiripple error** — the maximum error is reached with alternating sign at $L+2$ or more frequencies (where $L$ is the number of free parameters). No other filter of the same order achieves a smaller maximum error.

**Algorithm outline:**

1. **Initialise** with a guess for the $L+2$ extremal frequencies.
2. **Solve** for the filter coefficients that give equiripple error at these frequencies (using Lagrange interpolation — linear system).
3. **Find** the new set of $L+2$ extremal frequencies where the error is maximised.
4. **Repeat** until the extremal frequencies converge.

**Comparison with window method:**

| Feature | Window Method | Parks-McClellan |
|---|---|---|
| Optimality | No | Yes (minimax) |
| Ripple control | Equal in both bands | Independently set |
| Filter order for same spec | Higher (~20-30% more) | Minimum |
| Design complexity | Simple | Requires iterative solver |
| Implementation | MATLAB `fir1` | MATLAB `firpm`/`firls` |

**Practical formula for filter order (Kaiser–Parks rule):**

$$N \approx \frac{-20\log_{10}(\sqrt{\delta_p\,\delta_s}) - 13}{14.6\,\Delta f / f_s} + 1$$

where $\delta_p$ and $\delta_s$ are the passband and stopband ripple amplitudes.

---

### Q5. Define the filter specifications passband, stopband, transition band, passband ripple, and stopband attenuation. Translate a practical audio EQ requirement into these terms.

**Answer:**

**Definitions:**

- **Passband:** Frequency range $[0, \omega_p]$ where the filter should pass signals with gain close to unity (or a specified target gain).
- **Stopband:** Frequency range $[\omega_s, \pi]$ where the filter should reject signals (gain near zero).
- **Transition band:** $[\omega_p, \omega_s]$ — the region where the filter transitions between passband and stopband. No gain constraint is placed here.
- **Passband ripple $\delta_p$:** Maximum deviation from the desired passband gain. The actual passband gain lies in $[1-\delta_p, 1+\delta_p]$ (amplitude) or $\pm\delta_p\,\text{dB}$ in dB.
- **Stopband attenuation $A_s$:** The minimum attenuation in the stopband, in dB: $A_s = -20\log_{10}(\delta_s)$.

**Practical example — audio telephone pre-emphasis filter:**

Requirements: Pass voice band $[300, 3400]\,\text{Hz}$ with ripple $\leq 0.5\,\text{dB}$; reject above 3600 Hz with $\geq 40\,\text{dB}$ attenuation; sample rate $f_s = 8000\,\text{Hz}$.

| Specification | Value |
|---|---|
| Passband edge $f_p$ | 3400 Hz ($\omega_p = 2\pi \times 3400/8000 = 0.85\pi$) |
| Stopband edge $f_s$ | 3600 Hz ($\omega_s = 0.9\pi$) |
| Transition bandwidth | 200 Hz ($0.05\pi$ rad/sample) |
| Passband ripple $\delta_p$ | $10^{0.5/20} - 1 \approx 0.059$ (amplitude) |
| Stopband attenuation | 40 dB, so $\delta_s = 10^{-40/20} = 0.01$ |

**Filter order estimate (Parks-McClellan):**

$$N \approx \frac{-20\log_{10}(\sqrt{0.059 \times 0.01}) - 13}{14.6 \times 200/8000} + 1 \approx \frac{-20\log_{10}(0.0243) - 13}{0.365} + 1 \approx \frac{32.3 - 13}{0.365} + 1 \approx 54$$

A Parks-McClellan design would use approximately 54 taps.

---

### Q6. Prove that symmetric FIR coefficients ($h[n] = h[N-1-n]$) produce a linear phase response.

**Answer:**

For a Type I (odd-length, symmetric) FIR with coefficients $h[n] = h[N-1-n]$, $n = 0, \ldots, N-1$:

$$H(e^{j\omega}) = \sum_{n=0}^{N-1}h[n]\,e^{-j\omega n}$$

Factor out $e^{-j\omega(N-1)/2}$ (the overall delay of $(N-1)/2$ samples):

$$H(e^{j\omega}) = e^{-j\omega(N-1)/2}\sum_{n=0}^{N-1}h[n]\,e^{-j\omega(n - (N-1)/2)}$$

Let $m = n - (N-1)/2$ so the sum runs over $m = -(N-1)/2$ to $+(N-1)/2$ in unit steps:

$$H(e^{j\omega}) = e^{-j\omega(N-1)/2}\sum_{m=-(N-1)/2}^{(N-1)/2}h[m + (N-1)/2]\,e^{-j\omega m}$$

Using $h[m + (N-1)/2] = h[(N-1)/2 - m]$ (symmetry) and the fact that $e^{-j\omega m} + e^{j\omega m} = 2\cos(\omega m)$:

$$H(e^{j\omega}) = e^{-j\omega(N-1)/2}\left[h\!\left[\tfrac{N-1}{2}\right] + 2\sum_{m=1}^{(N-1)/2}h\!\left[\tfrac{N-1}{2}-m\right]\cos(\omega m)\right]$$

The bracketed sum is **real-valued** for all $\omega$. Call it $A(\omega)$.

$$H(e^{j\omega}) = A(\omega)\,e^{-j\omega(N-1)/2}$$

**Phase response:** $\angle H(e^{j\omega}) = -\omega\,\frac{N-1}{2} + \begin{cases}0 & A(\omega) > 0 \\ \pi & A(\omega) < 0\end{cases}$

The phase is **linear in $\omega$** (with possible jumps of $\pi$ that correspond to sign changes in $A(\omega)$).

**Group delay:** $\tau_g = -\frac{d}{d\omega}\left(-\omega\frac{N-1}{2}\right) = \frac{N-1}{2}$ — **constant**.

---

## Advanced

### Q7. What is the Gibbs phenomenon and how does it affect FIR filter design? How do window functions mitigate it?

**Answer:**

**Gibbs phenomenon:** When an ideal frequency response with a discontinuity (e.g., a brick-wall lowpass filter) is truncated to $N$ coefficients using the rectangular window, the resulting frequency response exhibits **ringing oscillations** near the discontinuity. The peak overshoot converges to approximately **8.9%** (about 17.6% peak-to-peak) regardless of $N$.

**Mathematical origin:** The rectangular window's DTFT is the Dirichlet kernel:

$$W_R(e^{j\omega}) = \frac{\sin(\omega N/2)}{\sin(\omega/2)}\,e^{-j\omega(N-1)/2}$$

This has large sidelobes (first sidelobe at $-13$ dB). Convolving the ideal spectrum with this kernel spreads energy across the sidelobes, causing the oscillatory ripple in the magnitude response.

The overshoot converges to $\frac{1}{\pi}\int_0^\pi \frac{\sin t}{t}\,dt - \frac{1}{2} \approx 0.089$ of the step height regardless of $N$. Increasing $N$ narrows the transition band but does not reduce the ripple — it merely compresses the oscillations closer to the ideal cutoff.

**Window function mitigation:**

Window functions taper the coefficients to zero at the edges, reducing the sidelobes of the window's spectrum at the cost of widening the main lobe:

| Window | Sidelobe (dB) | Passband ripple | Min stopband attenuation |
|---|---|---|---|
| Rectangular | $-13$ | $\pm 0.74\,\text{dB}$ | 21 dB |
| Hamming | $-41$ | $\pm 0.019\,\text{dB}$ | 53 dB |
| Blackman | $-57$ | $\pm 0.002\,\text{dB}$ | 74 dB |
| Kaiser ($\beta=8$) | $\approx -80$ | very small | 80+ dB |

The sidelobe level directly sets the stopband attenuation. The trade-off is that wider window (lower sidelobes) requires a higher filter order for the same transition bandwidth.

---

### Q8. Describe a half-band FIR filter. Why is it computationally efficient?

**Answer:**

A **half-band filter** is a symmetric FIR lowpass filter with cutoff at $\omega_c = \pi/2$ (i.e., $f_s/4$) and with the property that the passband and stopband ripples are equal ($\delta_p = \delta_s$).

**Key structural property:** Every other coefficient (except the centre) is zero:

$$h[n] = 0 \quad \text{for all even } n \neq (N-1)/2$$

**Proof:** For a symmetric, odd-length FIR with $\omega_c = \pi/2$, the ideal response satisfies $H(e^{j\omega}) + H(e^{j(\omega+\pi)}) = 1$ (the passband and stopband are mirror images about $\pi/2$). This power-complementary condition forces even-indexed coefficients (other than the centre) to be zero.

**Computational efficiency:**

An $N$-tap FIR normally requires $(N+1)/2$ multiplications per output (exploiting symmetry). For a half-band filter, only $\lfloor (N+1)/4 \rfloor + 1$ multiplications are needed — approximately half that of a general symmetric FIR.

**Applications:**

- **Decimation by 2:** In multirate processing, downsampling by 2 requires a lowpass filter at $\pi/2$. A half-band FIR with the zero-coefficient structure, combined with the polyphase decomposition, reduces the computation by approximately $4\times$ compared to a general FIR.
- **Interpolation by 2:** Same filter, used in the reverse direction.
- Cascaded half-band filters implement efficient interpolation/decimation by powers of 2.

---

### Q9. How would you design an FIR Hilbert transformer? What filter type is it, and what are the phase and magnitude requirements?

**Answer:**

A **Hilbert transformer** produces the analytic signal by shifting all frequency components by $-\pi/2$ radians (90 degrees):

$$H_{HT}(e^{j\omega}) = \begin{cases} -j & 0 < \omega \leq \pi \\ +j & -\pi \leq \omega < 0 \end{cases}$$

This is equivalent to: magnitude $= 1$ for all $\omega \neq 0$, phase $= -\pi/2$ for positive frequencies.

**Filter type:** The Hilbert transformer is a **Type III** (odd-length, anti-symmetric) or **Type IV** (even-length, anti-symmetric) FIR filter.

For an anti-symmetric filter, $H(e^{j0}) = H(e^{j\pi}) = 0$ (Type III), or $H(e^{j0}) = 0$ (Type IV). This is acceptable since the Hilbert transformer specification has zero gain at DC anyway.

**Ideal impulse response:**

$$h_d[n] = \begin{cases} 0 & n \text{ even} \\ \dfrac{2}{\pi n} & n \text{ odd} \end{cases}$$

(relative to the centre tap, with appropriate delay for causality)

**Practical design:** Use Parks-McClellan with Type III or IV anti-symmetry constraint, specify magnitude $= 1$ over $[\omega_L, \pi - \omega_L]$ (excluding DC and Nyquist for Type III):

```matlab
% MATLAB Parks-McClellan Hilbert transformer, N=31 (Type III, odd)
N = 31;
h = firpm(N-1, [0.05, 0.95], [1, 1], 'hilbert');
```

**Application:** Hilbert transformers are used to create analytic (complex baseband) signals in SDR, single-sideband modulation, instantaneous amplitude/frequency estimation, and audio processing (QMF filter banks).

---

## Quick Reference

| FIR Type | Length | Symmetry | $H(0)$ | $H(\pi)$ | Use |
|---|---|---|---|---|---|
| I | Odd | $h[n]=h[N-1-n]$ | Free | Free | LP, HP, BP, BS |
| II | Even | $h[n]=h[N-1-n]$ | Free | 0 | LP, BP |
| III | Odd | $h[n]=-h[N-1-n]$ | 0 | 0 | Differentiator, Hilbert |
| IV | Even | $h[n]=-h[N-1-n]$ | 0 | Free | Differentiator, Hilbert |

| Design Method | Optimality | Use When |
|---|---|---|
| Window (Kaiser) | Sub-optimal | Quick design, order not critical |
| Parks-McClellan | Optimal (minimax) | Minimum order for given spec |
| Least-squares | MSE optimal | Soft constraints, noise shaping |
