# DTFT and DFT — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** DTFT Definition and Properties, DFT, Circular Convolution, Leakage, Zero-Padding
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Define the DTFT and explain how it relates to the z-transform and to continuous-time Fourier analysis.

**Answer:**

The **Discrete-Time Fourier Transform (DTFT)** of a sequence $x[n]$ is:

$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n]\,e^{-j\omega n}$$

The inverse DTFT recovers the sequence:

$$x[n] = \frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{j\omega})\,e^{j\omega n}\,d\omega$$

**Key characteristics of the DTFT:**

- The frequency variable $\omega$ (digital frequency) is dimensionless and in radians per sample.
- $X(e^{j\omega})$ is **always $2\pi$-periodic**: $X(e^{j(\omega+2\pi)}) = X(e^{j\omega})$. This follows directly from the definition.
- The range $[-\pi, \pi]$ corresponds to $[-f_s/2, f_s/2]$ in Hz (the full representable spectrum).
- The DTFT is generally a **complex-valued, continuous function** of $\omega$.

**Relationship to z-transform:**

$$X(z)\big|_{z=e^{j\omega}} = X(e^{j\omega})$$

The DTFT is the z-transform evaluated on the unit circle. It exists when the unit circle lies within the ROC.

**Relationship to continuous-time FT:**

For a sequence obtained by sampling $x_a(t)$ at rate $f_s$: $x[n] = x_a(nT_s)$, the DTFT relates to the continuous FT by:

$$X(e^{j\omega}) = f_s \sum_{k=-\infty}^{\infty} X_a\!\left(\frac{\omega - 2\pi k}{T_s \cdot 2\pi} \cdot \frac{1}{f_s}\right)$$

More simply: digital frequency $\omega = 2\pi f / f_s$ maps physical frequency $f$ to the range $[0, 2\pi)$.

---

### Q2. Define the DFT. How does it relate to the DTFT?

**Answer:**

The **$N$-point Discrete Fourier Transform** of an $N$-sample sequence $x[n]$, $n=0,1,\ldots,N-1$ is:

$$X[k] = \sum_{n=0}^{N-1} x[n]\,e^{-j2\pi kn/N} = \sum_{n=0}^{N-1} x[n]\,W_N^{kn}, \quad k = 0, 1, \ldots, N-1$$

where $W_N = e^{-j2\pi/N}$ is the primitive $N$th root of unity.

The **inverse DFT**:

$$x[n] = \frac{1}{N}\sum_{k=0}^{N-1} X[k]\,e^{j2\pi kn/N}, \quad n = 0, 1, \ldots, N-1$$

**Relationship to DTFT:**

The DFT is a **sampled version of the DTFT**, evaluated at $N$ uniformly spaced frequencies:

$$X[k] = X(e^{j\omega})\big|_{\omega = 2\pi k/N}$$

The DFT samples the DTFT at frequencies $\omega_k = \frac{2\pi k}{N}$ for $k = 0, 1, \ldots, N-1$, corresponding to physical frequencies $f_k = k\,f_s/N$ Hz.

**Frequency resolution:** The DFT bin spacing is $\Delta f = f_s/N$ Hz, or $\Delta\omega = 2\pi/N$ rad/sample. To achieve 1 Hz resolution at 44.1 kHz sample rate, you need $N \geq 44100$ points.

---

### Q3. List the main DFT properties and state what each one tells you.

**Answer:**

Let $X[k] = \text{DFT}_N\{x[n]\}$.

| Property | Time domain | Frequency domain |
|---|---|---|
| Linearity | $\alpha\,x[n] + \beta\,y[n]$ | $\alpha X[k] + \beta Y[k]$ |
| Circular time shift | $x[\langle n-m\rangle_N]$ | $W_N^{mk}\,X[k]$ |
| Circular frequency shift | $W_N^{-\ell n}\,x[n]$ | $X[\langle k-\ell\rangle_N]$ |
| Conjugate symmetry (real $x[n]$) | $x[n]$ real | $X[N-k] = X^*[k]$ |
| Circular convolution | $x[n] \circledast h[n]$ | $X[k]\,H[k]$ |
| Multiplication | $x[n]\,h[n]$ | $\frac{1}{N}(X[k] \circledast H[k])$ |
| Parseval's theorem | $\sum_{n=0}^{N-1}|x[n]|^2$ | $\frac{1}{N}\sum_{k=0}^{N-1}|X[k]|^2$ |

**Conjugate symmetry** means for a real signal, you only need $N/2 + 1$ unique DFT coefficients (the others are determined by symmetry). FFT algorithms exploit this with the "real FFT."

**Parseval's theorem** states energy is preserved between time and frequency domains (up to a $1/N$ normalisation factor, which depends on the DFT convention used).

---

### Q4. What is the difference between circular and linear convolution? Why does it matter for DSP?

**Answer:**

**Linear convolution** of two finite sequences $x[n]$ ($L$ points) and $h[n]$ ($M$ points):

$$y_{lin}[n] = \sum_{k} x[k]\,h[n-k]$$

Result has $L + M - 1$ points. This is the "true" convolution used in LTI system analysis.

**Circular (cyclic) convolution** of period-$N$ sequences:

$$y_{circ}[n] = \sum_{k=0}^{N-1} x[k]\,h[\langle n-k\rangle_N]$$

The subscript $\langle \cdot \rangle_N$ denotes reduction modulo $N$. The result is always $N$ points long.

**Why it matters:** The DFT circular convolution property states:

$$\text{IDFT}\{X[k]\,H[k]\} = y_{circ}[n]$$

Multiplying DFT coefficients pointwise computes **circular** convolution, not linear convolution. If you use the DFT to implement a filter (which requires linear convolution), naive DFT multiplication introduces **time-domain aliasing** (wrap-around distortion).

**Making circular = linear (zero-padding):**

If $N \geq L + M - 1$, zero-padding both sequences to length $N$ before computing the DFT ensures the circular convolution equals the linear convolution over the entire valid range:

$$y_{circ}[n] = y_{lin}[n] \quad \text{for } 0 \leq n \leq L+M-2, \quad \text{when } N \geq L+M-1$$

This is the basis of **fast convolution** (overlap-add, overlap-save methods).

---

## Intermediate

### Q5. State and prove Parseval's theorem for the DFT.

**Answer:**

**Theorem:**

$$\sum_{n=0}^{N-1} |x[n]|^2 = \frac{1}{N} \sum_{k=0}^{N-1} |X[k]|^2$$

**Proof:**

Start from the left-hand side and substitute the inverse DFT:

$$\sum_{n=0}^{N-1} x[n]\,x^*[n] = \sum_{n=0}^{N-1} x[n] \left(\frac{1}{N}\sum_{k=0}^{N-1} X^*[k]\,e^{-j2\pi kn/N}\right)$$

Interchange sum order (valid for finite sums):

$$= \frac{1}{N}\sum_{k=0}^{N-1} X^*[k] \underbrace{\left(\sum_{n=0}^{N-1} x[n]\,e^{-j2\pi kn/N}\right)}_{X[k]}$$

$$= \frac{1}{N}\sum_{k=0}^{N-1} X^*[k]\,X[k] = \frac{1}{N}\sum_{k=0}^{N-1} |X[k]|^2 \quad \blacksquare$$

**Physical meaning:** The total energy in the signal equals (up to the $1/N$ normalisation) the sum of squared magnitudes of its DFT coefficients. No energy is created or destroyed by the DFT. This is used to verify DFT computations and to compute power spectral density.

---

### Q6. Explain DFT spectral leakage. What causes it and what are the remedies?

**Answer:**

**Leakage** occurs when the DFT of a finite-duration observation of a sinusoid shows energy in frequency bins adjacent to the true sinusoid frequency, rather than a single sharp spectral line.

**Root cause:** The DFT assumes the $N$-point signal is one period of a periodic signal. If the signal frequency is not an exact integer multiple of $f_s/N$ (a DFT "bin frequency"), the signal is not periodic with period $N$. The implied sharp discontinuities at the block boundaries cause energy to spread across all frequency bins.

**Formal explanation:** Observing $N$ samples is equivalent to multiplying the infinite signal by a rectangular window $w[n] = 1$ for $0 \leq n \leq N-1$. In frequency:

$$X_{windowed}(e^{j\omega}) = X(e^{j\omega}) * W(e^{j\omega})$$

The rectangular window's DTFT is a Dirichlet kernel with sidelobes — these sidelobes spread energy away from the true frequency.

**Example:** A 1000 Hz sinusoid sampled at 8000 Hz with $N = 100$ points. Bin spacing = 80 Hz. Bin 12 is at 960 Hz, bin 13 at 1040 Hz. The 1000 Hz tone lies between bins, causing leakage into all bins.

**Remedies:**

1. **Zero-padding:** Increases frequency resolution (finer sampling of the DTFT) but does **not** reduce leakage — it reveals the underlying continuous DTFT more finely, including the leakage tails.

2. **Window functions:** Replace the rectangular window with a window having lower sidelobes (Hanning, Hamming, Blackman, Kaiser). This reduces leakage at the cost of widening the main lobe (reduced frequency resolution for separating nearby sinusoids).

3. **Frequency binning:** If possible, choose $N$ and $f_s$ such that the frequency of interest falls exactly on a DFT bin (coherent sampling). This eliminates leakage entirely for that component.

---

### Q7. What does zero-padding accomplish? Distinguish its effect on frequency resolution from its effect on spectral detail.

**Answer:**

**What zero-padding is:** Appending $L$ zeros to an $N$-point sequence before computing an $(N+L)$-point DFT.

**Effect 1 — Denser frequency sampling (more spectral detail):**

Zero-padding increases the number of DFT bins from $N$ to $N+L$. Since the DFT is a sampled version of the DTFT, more points gives a denser sampling of the underlying DTFT. This reveals more detail of the spectral shape — peaks appear smoother, and you can read off frequency values more precisely by interpolation.

$$\Delta\omega = \frac{2\pi}{N+L} < \frac{2\pi}{N}$$

**Effect 2 — Does NOT improve resolution of closely spaced sinusoids:**

True frequency resolution (the ability to separate two closely spaced sinusoids) is determined by the **observation window length** $N$, not the DFT size. Two sinusoids closer than $\Delta\omega_{res} \approx 2\pi/N$ rad/sample cannot be resolved regardless of how many zeros are appended.

**Analogy:** Zero-padding is like zooming in on a blurry photograph — you see more pixels, but the blur remains. Collecting more data (longer observation window) is like using a higher-resolution camera.

**Practical use of zero-padding:**
- Power-of-2 FFT efficiency: pad to the next power of 2 to use fast radix-2 algorithms
- Interpolation for peak frequency estimation: zero-pad by $8\times$ or $16\times$ and locate the peak bin
- Fast convolution: pad both sequences to $N \geq L + M - 1$ to make circular = linear

---

### Q8. Describe the circular time-shift and circular frequency-shift DFT properties. Give a practical example of each.

**Answer:**

**Circular time-shift:**

If $X[k] = \text{DFT}\{x[n]\}$, then:

$$\text{DFT}\{x[\langle n - m \rangle_N]\} = W_N^{mk}\,X[k] = e^{-j2\pi mk/N}\,X[k]$$

A circular shift of $m$ samples in time multiplies each DFT coefficient by a linear phase term $e^{-j2\pi mk/N}$.

**Practical example:** Digital fractional delay filters. Shifting a signal by $m$ samples in the DFT domain (multiply by $e^{-j2\pi mk/N}$) and then IDFT produces a circularly shifted time-domain signal. For a causal implementation, $m > 0$ produces a delay.

**Circular frequency shift:**

$$\text{DFT}\{x[n]\,W_N^{-\ell n}\} = \text{DFT}\{x[n]\,e^{j2\pi\ell n/N}\} = X[\langle k - \ell \rangle_N]$$

Multiplying the time-domain signal by a complex exponential $e^{j2\pi\ell n/N}$ circularly shifts the DFT spectrum by $\ell$ bins.

**Practical example:** Heterodyne frequency conversion in SDR. To shift a digital signal from carrier bin $\ell$ to DC (bin 0), multiply by $e^{-j2\pi\ell n/N}$ (complex demodulation). This is the discrete-time version of analog mixer multiplication.

**Connection to analog domain:** The circular frequency shift property is the DFT version of the modulation theorem in the continuous-time Fourier transform.

---

## Advanced

### Q9. Prove that the $N$-point DFT of the circular convolution of two $N$-point sequences equals the pointwise product of their DFTs.

**Answer:**

**Claim:** If $y[n] = x[n] \circledast h[n] = \sum_{k=0}^{N-1} x[k]\,h[\langle n-k\rangle_N]$, then $Y[m] = X[m]\,H[m]$.

**Proof:**

$$Y[m] = \sum_{n=0}^{N-1} y[n]\,W_N^{mn} = \sum_{n=0}^{N-1}\left(\sum_{k=0}^{N-1} x[k]\,h[\langle n-k\rangle_N]\right)W_N^{mn}$$

Let $\ell = \langle n - k \rangle_N$, so $n = \langle \ell + k \rangle_N$. Since $W_N^{mn} = W_N^{m\langle \ell+k\rangle_N} = W_N^{m(\ell+k)}$ (the modular reduction contributes an integer multiple of $N$ which makes $W_N^{mN} = 1$ vanish), and the sum over a complete residue system $\ell = 0,\ldots,N-1$:

$$Y[m] = \sum_{k=0}^{N-1} x[k]\,W_N^{mk} \sum_{\ell=0}^{N-1} h[\ell]\,W_N^{m\ell} = X[m]\,H[m] \quad \blacksquare$$

**Why this is powerful:** Computing linear convolution directly requires $O(L \cdot M)$ multiplications. Using the DFT (via FFT in $O(N\log N)$) and this property, we compute it in $O(N\log N)$ operations with appropriate zero-padding. For long sequences, the FFT-based approach is dramatically faster.

---

### Q10. Derive the relationship between the DTFT of a windowed signal and the spectral resolution/leakage trade-off. Quantify for the rectangular and Hanning windows.

**Answer:**

**Model:** Observe an infinite signal $x[n]$ through an $N$-point window $w[n]$:

$$x_w[n] = x[n]\,w[n]$$

In frequency (multiplication in time = convolution in frequency):

$$X_w(e^{j\omega}) = \frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{j\theta})\,W(e^{j(\omega-\theta)})\,d\theta$$

The windowed spectrum is a smoothed version of the true spectrum — the true spectrum convolved with the window's frequency response $W(e^{j\omega})$.

**Rectangular window** ($w[n] = 1$, $0 \leq n \leq N-1$):

$$W_R(e^{j\omega}) = e^{-j\omega(N-1)/2} \frac{\sin(\omega N/2)}{\sin(\omega/2)} \quad \text{(Dirichlet kernel)}$$

- Main lobe width: $4\pi/N$ (first nulls)
- Peak sidelobe level: $-13$ dB below main lobe
- Roll-off: $6$ dB/octave

**Hanning (von Hann) window** ($w[n] = 0.5 - 0.5\cos(2\pi n/(N-1))$):

This is a raised cosine that tapers to zero at both ends.

$$W_H(e^{j\omega}) \approx \frac{1}{2}W_R(e^{j\omega}) + \frac{1}{4}W_R(e^{j(\omega-2\pi/N)}) + \frac{1}{4}W_R(e^{j(\omega+2\pi/N)})$$

- Main lobe width: $8\pi/N$ (twice the rectangular window — worse resolution)
- Peak sidelobe level: $-31.5$ dB (much better than rectangular)
- Roll-off: $18$ dB/octave

**Trade-off quantified:**

| Window | Main lobe (bins) | Peak sidelobe (dB) | Application |
|---|---|---|---|
| Rectangular | 2 | $-13$ | Rarely used for spectral analysis |
| Hanning | 4 | $-31.5$ | General spectral analysis |
| Hamming | 4 | $-41$ | Audio, communications |
| Blackman | 6 | $-57$ | High dynamic range measurements |
| Kaiser ($\beta=8$) | ~8 | $-80$ | Flexible, near-optimal |

**Interpretation:** A wider main lobe means two closely-spaced sinusoids must be farther apart to be resolved. Lower sidelobes mean a weak sinusoid near a strong one can be detected without being masked by the strong one's leakage tails.

---

### Q11. What is the FFT? State the computational complexity and explain the divide-and-conquer principle for the radix-2 Cooley-Tukey algorithm.

**Answer:**

The **Fast Fourier Transform (FFT)** is an efficient algorithm for computing the DFT that exploits the periodicity and symmetry of the complex exponential $W_N = e^{-j2\pi/N}$.

**Complexity comparison:**

- Direct DFT: $O(N^2)$ complex multiplications
- Radix-2 FFT: $O(N\log_2 N)$ complex multiplications

For $N = 1024$: direct DFT requires ~$10^6$ multiplications; FFT requires ~$10^4$ — a 100x speedup.

**Radix-2 Decimation-In-Time (DIT) — Cooley-Tukey:**

Split the $N$-point DFT (assume $N$ is a power of 2) into two $N/2$-point DFTs by separating even and odd indices:

$$X[k] = \sum_{n=0}^{N-1} x[n]\,W_N^{kn} = \underbrace{\sum_{m=0}^{N/2-1} x[2m]\,W_{N/2}^{km}}_{X_{even}[k]} + W_N^k \underbrace{\sum_{m=0}^{N/2-1} x[2m+1]\,W_{N/2}^{km}}_{X_{odd}[k]}$$

Using $W_N^2 = W_{N/2}$:

$$X[k] = X_{even}[k] + W_N^k\,X_{odd}[k], \quad k = 0, 1, \ldots, N/2-1$$

$$X[k + N/2] = X_{even}[k] - W_N^k\,X_{odd}[k]$$

This is the **butterfly operation**. Each butterfly computes two outputs from two inputs with one complex multiplication ($W_N^k$) and two additions.

**Recursion:** Apply the same splitting recursively. For $N = 2^m$, there are $m = \log_2 N$ stages, each with $N/2$ butterflies, totalling $\frac{N}{2}\log_2 N$ complex multiplications.

**In-place computation:** The FFT can overwrite its input array as it computes (bit-reversal permutation at input, butterfly stages). This is memory-efficient and is why the FFT is feasible on embedded hardware.

---

## Quick Reference

| Transform | Formula | Frequency variable |
|---|---|---|
| DTFT | $X(e^{j\omega}) = \sum_n x[n]e^{-j\omega n}$ | $\omega \in [-\pi, \pi]$, continuous |
| DFT | $X[k] = \sum_{n=0}^{N-1}x[n]W_N^{kn}$ | $k = 0,\ldots,N-1$, discrete |

| Operation | Time domain | Frequency domain |
|---|---|---|
| Circular convolution | $x[n]\circledast h[n]$ | $X[k]\cdot H[k]$ |
| Multiplication | $x[n]\cdot h[n]$ | $\frac{1}{N}(X[k]\circledast H[k])$ |
| Parseval | $\sum\|x[n]\|^2$ | $\frac{1}{N}\sum\|X[k]\|^2$ |
| FFT complexity | — | $\frac{N}{2}\log_2 N$ multiplications |
