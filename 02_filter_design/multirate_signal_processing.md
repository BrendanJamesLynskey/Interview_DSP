# Multirate Signal Processing — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Decimation, Interpolation, Noble Identities, Polyphase, CIC Filters, Rational Rate Conversion
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Define decimation and interpolation. What filtering is required in each case and why?

**Answer:**

**Decimation by $M$ (downsampling):**

The process of reducing the sample rate by an integer factor $M$:

1. **Lowpass filter** with cutoff $\omega_c = \pi/M$ (to prevent aliasing)
2. **Keep every $M$th sample:** $y[n] = x_{filtered}[nM]$

The combined system is a **decimator**.

**Why filtering is required before downsampling:** Downsampling by $M$ spreads the digital spectrum by a factor of $M$, causing copies of the spectrum at intervals of $2\pi/M$ to overlap (alias). The lowpass filter limits the signal to $|\omega| \leq \pi/M$ so that after downsampling (spectrum stretching by $M$), the signal fits within $|\omega| \leq \pi$ without overlap.

$$Y(e^{j\omega}) = \frac{1}{M}\sum_{k=0}^{M-1} X_f(e^{j(\omega - 2\pi k)/M})$$

For no aliasing, $X_f(e^{j\omega}) = 0$ for $|\omega| > \pi/M$.

**Interpolation by $L$ (upsampling):**

The process of increasing the sample rate by an integer factor $L$:

1. **Insert $L-1$ zeros** between each sample: $x_u[n] = x[n/L]$ if $n$ is a multiple of $L$, else $0$
2. **Lowpass filter** with cutoff $\pi/L$ and gain $L$

The combined system is an **interpolator**.

**Why filtering is required after upsampling:** Zero-insertion creates spectral images (copies of the spectrum) at intervals of $2\pi/L$ across $[0, 2\pi]$. The lowpass filter removes all images except the baseband one, and the gain $L$ compensates for the energy loss from the zero insertions.

---

### Q2. What are the noble identities? State both and explain their significance.

**Answer:**

The noble identities allow the interchange of filtering and multirate operations, enabling the derivation of computationally efficient filter implementations.

**Noble Identity 1 (downsampling):**

Filtering by $H(z)$ then downsampling by $M$ is equivalent to downsampling by $M$ then filtering by $H(z^M)$:

$$\downarrow M \circ H(z) \equiv H(z^M) \circ \downarrow M$$

That is: a filter $H(z)$ followed by $\downarrow M$ equals $\downarrow M$ followed by $H(z^M)$.

**Noble Identity 2 (upsampling):**

Upsampling by $L$ then filtering by $H(z)$ is equivalent to filtering by $H(z^L)$ then upsampling by $L$:

$$H(z) \circ \uparrow L \equiv \uparrow L \circ H(z^L)$$

**Proof of Identity 1:**

Let $w[n]$ be the output of $H(z)$: $W(z) = H(z)\,X(z)$. After downsampling: $Y(z) = W(z^{1/M})$ (spectral spreading).

Alternatively: downsample first to get $V(z)$, then filter by $H(z^M)$:

$$Y(z) = H(z^M)\,V(z) = H(z^M)\,X(z^{1/M})$$

Both expressions are equal: $H(z^{1/M} \cdot M)\,X(z^{1/M}) = H(z)\,X(z)$ after rescaling — the equivalence holds ✓

**Significance:** Noble identities enable the **polyphase decomposition**, which moves filtering to a lower rate, reducing computational cost by factor $M$ (decimation) or $L$ (interpolation).

---

### Q3. What is the polyphase decomposition of a filter? How does it reduce computation in a decimator?

**Answer:**

**Polyphase decomposition:** A length-$N$ FIR filter $H(z)$ is decomposed into $M$ polyphase components, each a subfilter of length $\lceil N/M \rceil$:

$$H(z) = \sum_{k=0}^{M-1} z^{-k}\,E_k(z^M)$$

where the $k$th polyphase component is:

$$E_k(z) = \sum_{n=0}^{\lceil N/M \rceil - 1} h[nM + k]\,z^{-n}$$

Each $E_k(z)$ contains every $M$th coefficient of $h[n]$, starting from offset $k$.

**Example for $M = 3$, $H$ with 9 coefficients $h[0], \ldots, h[8]$:**

$$E_0(z) = h[0] + h[3]z^{-1} + h[6]z^{-2}$$
$$E_1(z) = h[1] + h[4]z^{-1} + h[7]z^{-2}$$
$$E_2(z) = h[2] + h[5]z^{-1} + h[8]z^{-2}$$

**Efficient decimator implementation:**

Naive decimation: filter at the high rate $f_s$, then throw away $M-1$ out of every $M$ samples. You compute $N$ multiplications per input sample but discard $M-1$ out of $M$ outputs — wasteful.

**Polyphase approach:**

Using Noble Identity 1, move the downsampling before the polyphase subfilters:

$$y[n] = \sum_{k=0}^{M-1} E_k(z^M)\,[x[n] \cdot z^{-k}] \downarrow M$$

Each $E_k$ now operates at the **output rate** $f_s/M$, processing only 1 out of $M$ samples:

```
x[n] ──────────────────────── E_0(z) ──┐
x[n-1] ──────────────────────  E_1(z) ──┤── (+) ── y[n]
x[n-2] ──────────────────────  E_2(z) ──┘
```

Each $E_k$ has $\lceil N/M \rceil$ taps and runs at rate $f_s/M$.

**Computational cost:**

- Naive: $N$ multiplications per input sample at rate $f_s$ = $N\,f_s$ multiplications/second
- Polyphase: $M \times \lceil N/M \rceil \approx N$ multiplications per output sample at rate $f_s/M$ = $(N/M) \times (f_s/M) \times M = N\,f_s/M$ multiplications/second

**Saving: factor $M$ in computation.**

---

## Intermediate

### Q4. Design a sample rate converter for rational factor $L/M$. What is the correct order of interpolation and decimation?

**Answer:**

**Rational sample rate conversion:** Convert from $f_{s1}$ to $f_{s2}$ where $f_{s2}/f_{s1} = L/M$ (rational, $\gcd(L,M) = 1$).

**Method:**

1. **Interpolate by $L$:** Conceptually upsample to $L\,f_{s1}$ by inserting $L-1$ zeros between samples
2. **Decimate by $M$:** Keep every $M$th sample to produce $f_{s2} = (L/M)\,f_{s1}$

**Critical ordering: interpolation FIRST, decimation SECOND.**

If you decimate first, you risk losing signal content. Conceptually, both operations share a single combined lowpass filter at the common intermediate rate $L\,f_{s1}$:

$$\omega_{c,combined} = \frac{\pi}{\max(L, M)} = \pi \cdot \min\!\left(\frac{1}{L}, \frac{1}{M}\right)$$

The combined lowpass filter prevents:
- **Aliasing** from the decimation by $M$: requires cutoff $\leq \pi/M$
- **Imaging** from the interpolation by $L$: requires cutoff $\leq \pi/L$

Both conditions are satisfied by $\omega_c = \pi/\max(L, M)$.

**Single combined filter:** The upsampler zeros and the decimation discard simplify the implementation. The filter only needs to produce outputs at the times that survive the decimation, which is the key computational saving.

**Example:** Convert 44.1 kHz to 48 kHz.

$$\frac{48000}{44100} = \frac{160}{147}$$

$L = 160$, $M = 147$. Interpolate by 160, then decimate by 147.

Intermediate rate: $160 \times 44100 = 7.056\,\text{MHz}$. The combined filter must have $\omega_c = \pi/160 \approx 0.02\,\text{rad/sample}$ (at the intermediate rate), corresponding to 22.05 kHz and 24 kHz at the input and output rates respectively.

---

### Q5. State the computational advantages of polyphase filter structures in both decimation and interpolation.

**Answer:**

**Polyphase decimation by $M$ (from Q3 above):**

Savings: $M$-to-1 reduction in multiply-accumulate operations, because the polyphase subfilters operate at the output (lower) sample rate. The filter length is shared across $M$ subfilters, each of length $N/M$.

**Polyphase interpolation by $L$:**

Using Noble Identity 2, move the upsampling after the polyphase subfilters:

$$H(z) = \sum_{k=0}^{L-1} z^{-k}\,E_k(z^L)$$

The $L$ polyphase subfilters each operate at the input rate $f_s$, not the output rate $L\,f_s$:

```
x[n] ─┬── E_0(z) ──────────── [↑L, offset 0] ──┐
       ├── E_1(z) ──────────── [↑L, offset 1] ──┤── (+) ── y[n]
       ├── E_2(z) ──────────── [↑L, offset 2] ──┤
       └── E_{L-1}(z) ──────── [↑L, offset L-1]─┘
```

Or equivalently, compute all $L$ subfilter outputs and commutate them to form the high-rate output stream.

**Savings for interpolation:** Each subfilter $E_k(z)$ has $N/L$ taps and runs at the input rate $f_s$. Total operations: $L \times (N/L) \times f_s = N\,f_s$ — same as direct FIR at the input rate (not the interpolated rate $L\,f_s$). Compared to naive (filter at high rate $L\,f_s$): saving of factor $L$.

**Summary of savings:**

| Operation | Direct cost | Polyphase cost | Saving |
|---|---|---|---|
| Decimation by $M$ | $N \cdot f_{s,in}$ | $N \cdot f_{s,out} = N f_{s,in}/M$ | Factor $M$ |
| Interpolation by $L$ | $N \cdot f_{s,out} = N L f_{s,in}$ | $N \cdot f_{s,in}$ | Factor $L$ |

---

## Advanced

### Q6. Derive the transfer function of a CIC (Cascaded Integrator-Comb) decimation filter of order $N$ and decimation factor $M$. Compute its frequency response.

**Answer:**

A CIC decimation filter consists of $N$ integrators running at the high rate, followed by downsampling by $M$, followed by $N$ comb filters running at the low rate.

**Single comb filter (at high rate):** $H_C(z) = 1 - z^{-M}$

**Single integrator (at high rate):** $H_I(z) = \frac{1}{1 - z^{-1}}$

**Transfer function of $N$-stage CIC at high rate:**

$$H_{CIC}(z) = \left(H_I(z)\right)^N \cdot \left(H_C(z)\right)^N = \frac{(1 - z^{-M})^N}{(1 - z^{-1})^N}$$

This can be simplified by noting:

$$\frac{1 - z^{-M}}{1 - z^{-1}} = 1 + z^{-1} + z^{-2} + \cdots + z^{-(M-1)} = \sum_{k=0}^{M-1}z^{-k}$$

This is a moving average over $M$ samples. Therefore:

$$H_{CIC}(z) = \left(\sum_{k=0}^{M-1}z^{-k}\right)^N$$

**Impulse response:** The CIC is a cascade of $N$ rectangular (boxcar) windows of length $M$.

**Frequency response:**

On the unit circle $z = e^{j\omega}$:

$$H_{CIC}(e^{j\omega}) = \left(\frac{1 - e^{-j\omega M}}{1 - e^{-j\omega}}\right)^N = e^{-j\omega M(N)/2 + j\omega N/2}\left(\frac{\sin(\omega M/2)}{\sin(\omega/2)}\right)^N$$

Magnitude:

$$|H_{CIC}(e^{j\omega})| = \left|\frac{\sin(\omega M/2)}{\sin(\omega/2)}\right|^N$$

At DC ($\omega = 0$): $|H_{CIC}(e^{j0})| = M^N$ (the DC gain).

**Frequency response in terms of input-rate samples:**

After downsampling by $M$, the frequency axis rescales: $\omega_{out} = M\omega_{in}$. The passband extends to approximately $\omega_{in} = \pi/M$ (which maps to $\omega_{out} = \pi$).

**Passband droop:** The magnitude at frequency $f$ within the passband (relative to DC):

$$\left|\frac{H_{CIC}(e^{j2\pi f/f_s})}{M^N}\right| = \left|\frac{\sin(\pi f M/f_s)}{M\sin(\pi f/f_s)}\right|^N \approx \left|\text{sinc}(f/f_{out})\right|^N$$

for $f \ll f_s$. The droop is approximately $20N\log_{10}(\text{sinc}(f/f_{out}))$ dB.

---

### Q7. Compute the bit growth in a CIC filter. Why is this important for fixed-point implementation?

**Answer:**

**Bit growth:** Each integrator stage increases the word length needed to represent the output without overflow. For a CIC of order $N$ and decimation $M$:

**Maximum output value:** The worst-case output occurs when all $M^N$ additions are at the maximum positive value. The maximum accumulator value is:

$$y_{max} = M^N \cdot x_{max}$$

**Bit growth:** To represent $M^N$ times the input range, we need:

$$B_{growth} = N\log_2 M \quad \text{bits}$$

**Total word length at output of each integrator stage $k$:**

$$B_{total} = B_{input} + k\log_2 M$$

After $N$ integrators, before the comb section:

$$B_{total} = B_{input} + N\log_2 M$$

**Example:** CIC with $N = 3$ stages and $M = 32$ decimation. $\log_2(32) = 5$.

Bit growth = $3 \times 5 = 15$ bits. If the input is 16-bit, the integrators must use $16 + 15 = 31$ bits. In a 32-bit signed integer, this barely fits. For $M = 64$ or $N = 4$, a 64-bit accumulator would be required.

**Implementation strategies:**

1. **Grow the word width:** Use wider accumulators. The FPGA integrators use 24-bit or 32-bit accumulators even for a 12-bit ADC input.

2. **Pruning:** Not all bits are needed at every stage — the lower bits of early stages are dominated by noise. The lower $\lfloor k \log_2 M \rfloor$ bits of stage $k$ can be discarded, but this introduces a small error. A systematic pruning analysis (based on the noise model) can reduce hardware significantly.

3. **Two's complement overflow is acceptable in the integrators:** If the integrators are implemented in two's complement and the comb filters are applied to the same word length, the overflow is "self-cancelling" — the comb sections undo the wrap-around. This is a key practical insight: CIC integrators can be allowed to overflow in two's complement arithmetic, and the correct output is still obtained.

**FPGA/ASIC practice:** The standard CIC implementation uses two's complement accumulators of width $B_{input} + \lceil N\log_2 M \rceil$ bits, allows wrap-around in all integrators, and truncates to the desired output word length after the final comb stage.

---

### Q8. What is droop compensation for a CIC filter? How is it implemented?

**Answer:**

**CIC passband droop:** The CIC frequency response has a $\text{sinc}^N$ shape. For a passband signal at $[0, f_{pass}]$ where $f_{pass} < f_{out}/2 = f_{in}/(2M)$, the droop (roll-off from DC to $f_{pass}$) is:

$$\text{Droop} = 20N\log_{10}\!\left(\frac{\sin(\pi f_{pass}/f_{out})}{\pi f_{pass}/f_{out}}\right) \approx -20N \times \frac{(\pi f_{pass}/f_{out})^2}{6}\,\text{dB (for small arguments)}$$

**Example:** $N = 3$, $M = 16$, signal bandwidth 20% of $f_{out}$: droop $\approx -20 \times 3 \times \frac{(0.2\pi)^2}{6} \approx -2.3\,\text{dB}$.

**Droop compensation:** Add a short digital compensating filter $C(z)$ that has an inverse $\text{sinc}^N$ response over the passband.

**Design of the compensating FIR:**

The compensating filter has desired response:

$$D(e^{j\omega}) = \left(\frac{\pi f / f_{out}}{\sin(\pi f / f_{out})}\right)^N \approx 1 + N\frac{(\pi f/f_{out})^2}{6} + \cdots$$

For small to moderate passband widths, a short 3–9 tap linear-phase FIR is sufficient.

**Example 3-tap compensator (linear phase, Type I):**

For $N=3$, $M=16$, passband up to $f_{pass} = 0.4\,f_{out}$:

Coefficients approximately: $h = [-0.020,\, 1.040,\, -0.020]$ (found by Parks-McClellan targeting $D(\omega)$).

**Implementation placement:**

The compensator runs at the **output rate** $f_{out}$ (after the CIC), making it very cheap (3 multiplications at the low rate vs. the high-rate CIC). For very wideband signals (passband approaching $f_{out}/2$), a longer compensation filter may be needed, and it can be combined with the downstream channel-selection filter.

---

## Quick Reference

| Operation | Filter cutoff | Computation gain |
|---|---|---|
| Decimation by $M$ | $\pi/M$ before $\downarrow M$ | Factor $M$ with polyphase |
| Interpolation by $L$ | $\pi/L$ after $\uparrow L$ | Factor $L$ with polyphase |
| Rational $L/M$ | $\pi/\max(L,M)$ | Polyphase on combined filter |

| CIC parameter | Formula |
|---|---|
| Transfer function | $H(z) = \left(\frac{1-z^{-M}}{1-z^{-1}}\right)^N$ |
| DC gain | $M^N$ |
| Bit growth | $N\log_2 M$ bits |
| Passband droop | $\approx 20N\log_{10}(\text{sinc}(f/f_{out}))$ dB |
