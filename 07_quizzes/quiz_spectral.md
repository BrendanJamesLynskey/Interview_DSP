# DSP Spectral Analysis — Multiple-Choice Quiz

**Topics covered:** FFT computational complexity, radix-2 Cooley-Tukey butterfly, spectral leakage, windowing trade-offs, power spectral density estimation (periodogram, Welch's method), short-time Fourier transform (STFT) time-frequency resolution, zero-padding effects.

**Instructions:** Select the single best answer for each question. The answer key with detailed explanations appears at the bottom.

---

## Questions

**Q1.** A direct computation of an N-point DFT requires $O(N^2)$ complex multiplications. A radix-2 FFT reduces this to:

A. $O(N \log_2 N)$  
B. $O(N \sqrt{N})$  
C. $O(N^2 / 2)$  
D. $O(\log_2 N)$

---

**Q2.** The radix-2 decimation-in-time (DIT) FFT butterfly operation computes:

$$A' = A + W_N^k B, \qquad B' = A - W_N^k B$$

where $W_N = e^{-j2\pi/N}$. How many complex multiplications and complex additions does one butterfly require?

A. 2 multiplications, 2 additions  
B. 1 multiplication, 2 additions  
C. 2 multiplications, 4 additions  
D. 0 multiplications, 2 additions

---

**Q3.** Spectral leakage occurs in DFT analysis when:

A. The FFT size $N$ is not a power of 2.  
B. The signal frequency does not fall exactly on a DFT bin, causing energy to spread into neighbouring bins.  
C. The signal is oversampled relative to the Nyquist rate.  
D. Zero-padding is applied before the DFT.

---

**Q4.** You are analysing a stationary signal with an N-point DFT. Compared to using a rectangular (boxcar) window, applying a Hann window before the DFT will:

A. Reduce spectral leakage sidelobes but widen the mainlobe, reducing frequency resolution.  
B. Eliminate spectral leakage entirely.  
C. Reduce the mainlobe width while increasing sidelobe levels.  
D. Increase frequency resolution without affecting sidelobe levels.

---

**Q5.** The frequency resolution of an N-point DFT applied to a signal sampled at $f_s$ is:

A. $f_s / N^2$  
B. $N / f_s$  
C. $f_s / N$  
D. $f_s \cdot N$

---

**Q6.** Zero-padding a time-domain sequence from length $N$ to length $M > N$ before computing the DFT:

A. Increases the true frequency resolution by revealing new spectral detail.  
B. Interpolates the spectrum — increasing the density of DFT bins without improving the fundamental frequency resolution.  
C. Reduces spectral leakage because the zero-padded region smooths the discontinuity.  
D. Is equivalent to using a longer observation window of length $M$.

---

**Q7.** The periodogram estimate of the power spectral density (PSD) of a zero-mean WSS process is defined as:

$$\hat{S}_{xx}(e^{j\omega}) = \frac{1}{N}\left|X_N(e^{j\omega})\right|^2$$

where $X_N$ is the N-point DFT of the observed data. Which statement best describes the statistical properties of the periodogram?

A. It is a consistent estimator: variance decreases as $N \to \infty$.  
B. It is asymptotically unbiased but not consistent: variance does not decrease as $N \to \infty$.  
C. It is both unbiased and consistent for all $N$.  
D. It has zero variance at all frequencies because it is derived from the DFT.

---

**Q8.** Welch's method improves upon the periodogram by:

A. Using a longer data record to improve frequency resolution.  
B. Computing the DFT at more frequency points using zero-padding.  
C. Averaging periodograms of overlapping windowed segments to reduce variance, at the cost of reduced frequency resolution.  
D. Applying the bilinear transform to convert the periodogram to a smooth analytic spectrum.

---

**Q9.** In the short-time Fourier transform (STFT), the time-frequency resolution is governed by:

A. Only the hop size (frame shift) between successive analysis windows.  
B. The window length $L$: a longer window gives better frequency resolution but poorer time resolution, and vice versa.  
C. Only the DFT size $N$, regardless of window length.  
D. The sampling rate $f_s$ alone — time and frequency resolution scale together with $f_s$.

---

**Q10.** The STFT of a signal $x[n]$ with analysis window $w[n]$ is:

$$X[m, k] = \sum_{n=-\infty}^{\infty} x[n]\, w[n - mH]\, e^{-j2\pi kn/N}$$

where $H$ is the hop size. Perfect reconstruction of $x[n]$ from $X[m, k]$ requires that:

A. $H = N/2$ (50% overlap) regardless of window shape.  
B. The synthesis window satisfies the overlap-add (OLA) or weighted overlap-add (WOLA) reconstruction condition.  
C. $N$ must be a power of 2 for the FFT to apply.  
D. The window $w[n]$ must be rectangular.

---

**Q11.** A signal consists of two sinusoids at frequencies $f_1$ and $f_2 = f_1 + \Delta f$. To resolve these two peaks as distinct in the DFT magnitude spectrum (using a rectangular window), the observation length $T_{obs}$ must satisfy:

A. $T_{obs} > 1 / \Delta f$  
B. $T_{obs} > 2 / \Delta f$  
C. $T_{obs} > \Delta f$  
D. $T_{obs} > 1 / (2 \Delta f)$

---

**Q12.** The bias of the periodogram PSD estimate is related to:

A. The variance of the data samples.  
B. The finite data length, which causes the true PSD to be convolved with the Fourier transform of a rectangular window (the Fejér kernel).  
C. The number of overlapping segments used in Welch's method.  
D. The choice of FFT size $N$ relative to the data length.

---

**Q13.** Which of the following window functions is best suited when two tones of very different amplitudes (e.g., separated by 60 dB) must be resolved and the weaker tone is close in frequency to the stronger one?

A. Rectangular window  
B. Hann window  
C. Hamming window  
D. Kaiser window with large $\beta$ parameter

---

**Q14.** In a radix-2 FFT of length $N = 2^L$, the total number of butterfly stages is $L = \log_2 N$, each containing $N/2$ butterflies. What is the total number of complex multiplications, counting the trivial $W_N^0 = 1$ twiddle factors?

A. $N \log_2 N$  
B. $\frac{N}{2} \log_2 N$  
C. $N^2 / 4$  
D. $N \log_2 N / 4$

---

**Q15.** The Heisenberg–Gabor uncertainty principle as applied to the STFT states that:

A. Increasing sampling rate improves both time and frequency resolution simultaneously.  
B. The product of time resolution $\Delta t$ and frequency resolution $\Delta f$ has a lower bound: $\Delta t \cdot \Delta f \geq \frac{1}{4\pi}$.  
C. For a given window length, using a larger FFT size always improves frequency resolution.  
D. Perfect time-frequency resolution can be achieved by choosing an appropriate window function.

---

**Q16.** Welch's method with 50% overlap and a Hann window applied to $N_{total}$ data points, split into segments of length $L$, achieves a PSD variance reduction factor of approximately:

A. $L / N_{total}$ (same as the basic averaged periodogram)  
B. $8/3$ times worse than the basic averaged periodogram due to window power loss  
C. $8/3$ times the number of non-overlapping segments (approximately $8 N_{total} / (3L)$ effective averages)  
D. Exactly $N_{total} / L$ (identical to non-overlapping segments)

---

**Q17.** A spectrogram is computed from an STFT using a 256-point Hann window with 75% overlap (hop size $H = 64$ samples) on a signal sampled at 16 kHz. What is the time resolution of the spectrogram (duration of each analysis frame)?

A. 4 ms  
B. 8 ms  
C. 16 ms  
D. 32 ms

---

## Answer Key

| Q | Answer |
|---|--------|
| 1 | A |
| 2 | B |
| 3 | B |
| 4 | A |
| 5 | C |
| 6 | B |
| 7 | B |
| 8 | C |
| 9 | B |
| 10 | B |
| 11 | A |
| 12 | B |
| 13 | D |
| 14 | B |
| 15 | B |
| 16 | C |
| 17 | C |

---

## Detailed Explanations

**Q1 — Answer: A ($O(N \log_2 N)$)**

The Cooley-Tukey FFT exploits the recursive structure of the DFT. For $N = 2^L$, the DFT is decomposed into two DFTs of size $N/2$ at each stage, requiring $N/2$ complex multiplications per stage over $\log_2 N$ stages, giving $\frac{N}{2}\log_2 N$ non-trivial multiplications — asymptotically $O(N \log_2 N)$. For $N = 1024$, this is roughly 5120 multiplications vs 1,048,576 for the direct DFT — a 200× speedup. Option B ($O(N\sqrt{N})$) would describe an intermediate algorithm that does not exist in practice for power-of-2 sizes. Option C is simply a constant reduction and not achievable. Option D ($O(\log N)$) would require the computation to be independent of $N$, which is impossible.

---

**Q2 — Answer: B (1 multiplication, 2 additions)**

The DIT butterfly computes $A' = A + W_N^k B$ and $B' = A - W_N^k B$. The product $W_N^k B$ requires 1 complex multiplication ($W_N^k$ times $B$). Once that product is computed, $A + W_N^k B$ and $A - W_N^k B$ each require 1 complex addition, totalling 2 additions. Note that a complex multiplication normally requires 4 real multiplications and 2 real additions, but using Karatsuba-style three-real-multiply tricks it can be done in 3 real multiplications and 3 real additions. Option A (2 multiplications) double-counts the twiddle multiplication. Option C overcounts. Option D is only true for the trivial $k = 0$ butterfly.

---

**Q3 — Answer: B**

The DFT assumes the analysed segment is one period of a periodic signal. When a sinusoid's frequency does not land exactly on a DFT bin (i.e., an integer multiple of $f_s/N$), the segment does not contain a whole number of cycles. When periodically extended, this creates a discontinuity at the block boundaries. In frequency, this appears as energy smearing from the true frequency bin into neighbouring bins — spectral leakage. Option A is false — non-power-of-2 FFTs exist and produce correct results. Option C is wrong — oversampling does not cause leakage. Option D is wrong — zero-padding cannot cause leakage; it only interpolates an existing (possibly leaky) spectrum.

---

**Q4 — Answer: A**

The Hann window has first sidelobes at approximately $-32\ \text{dB}$ (vs $-13\ \text{dB}$ for rectangular), substantially reducing spectral leakage from a strong tone bleeding into adjacent frequency bins. The trade-off is a wider mainlobe — approximately $8\pi/N$ vs $4\pi/N$ for rectangular — meaning two closely spaced tones require a longer record (or larger $N$) to be resolved. Option B is wrong — windowing reduces but cannot eliminate leakage completely (no window has zero-width sidelobes). Option C reverses the effects of the Hann window. Option D is self-contradictory since resolution is related to mainlobe width, which increases with smoothing windows.

---

**Q5 — Answer: C ($f_s / N$)**

The DFT bins are spaced at intervals of $\Delta f = f_s / N$ Hz (equivalently, $\Delta \omega = 2\pi/N$ rad/sample). This is the frequency resolution — the minimum frequency separation between two tones that can be distinguished as separate peaks (approximately, for a rectangular window). Equivalently, the resolution in Hz equals the reciprocal of the observation time $T = N/f_s$: $\Delta f = 1/T = f_s/N$. Option A is wrong (divides by $N^2$). Option B inverts the formula. Option D multiplies instead of divides.

---

**Q6 — Answer: B**

Zero-padding extends the data with zeros, effectively interpolating the spectrum between DFT bins. The result is a smoother-looking spectrum with more bins per Hz, but these additional bins contain no new information — they are just a smoother curve drawn through the same data. The fundamental resolution, determined by the length of the actual (non-zero) data, does not change. A common mistake is to confuse the visual improvement from zero-padding (smoother spectrum) with improved resolution. Option A makes this mistake. Option C is wrong — leakage depends on the data window shape, not on zero-padding. Option D is wrong — zero-padding does not extend the observation window.

---

**Q7 — Answer: B**

The periodogram is asymptotically unbiased: as $N \to \infty$, $E[\hat{S}_{xx}] \to S_{xx}$. However, it is not consistent: the variance of $\hat{S}_{xx}(e^{j\omega})$ approaches $S_{xx}^2(e^{j\omega})$ as $N \to \infty$, not zero. This occurs because increasing $N$ adds more frequencies but each bin estimate remains a single degree-of-freedom random variable with $\chi^2_2$ distribution — more data gives finer frequency resolution but not smoother estimates. Consistency requires averaging multiple estimates, which is the motivation for Welch's method. Options A and C are therefore wrong. Option D is absurd — the DFT maps random data to random spectral coefficients.

---

**Q8 — Answer: C**

Welch's method divides the data into $K$ overlapping segments, applies a window to each segment, computes the periodogram of each windowed segment, and averages all $K$ periodograms. Averaging $K$ independent (or partially correlated, due to overlap) estimates reduces variance approximately $K$-fold. The cost is reduced frequency resolution: each segment of length $L < N_{total}$ has resolution $f_s/L > f_s/N_{total}$. Option A simply describes using more data, which is not specific to Welch. Option B describes zero-padding within Welch segments, which is a valid refinement but not Welch's defining contribution. Option D describes an unrelated transform technique.

---

**Q9 — Answer: B**

In the STFT, the analysis window of length $L$ determines both the time and frequency resolution according to the uncertainty principle. A longer window provides better frequency resolution ($\Delta f \approx f_s/L$) because more samples average out noise and reveal spectral detail, but it captures a longer time segment, blurring fast temporal changes. A shorter window tracks transients better (finer time resolution) but has coarser frequency resolution. Option A is wrong — hop size controls the time sampling density of the STFT but does not change the resolution of each individual frame. Option C is wrong — $N > L$ adds zero-padding (interpolation) but does not improve resolution. Option D is wrong — resolution can be traded between time and frequency independent of $f_s$.

---

**Q10 — Answer: B**

Perfect reconstruction from the STFT requires the synthesis window and hop size to satisfy an overlap-add reconstruction condition. For the weighted overlap-add (WOLA) framework, the synthesis window $\tilde{w}[n]$ and analysis window $w[n]$ must satisfy $\sum_m w[n - mH]\tilde{w}[n - mH] = 1$ for all $n$. For rectangular windows with $H = L$ (no overlap) or Hann windows with $H = L/2$ (50% overlap), standard reconstruction conditions apply. Option A is an over-simplification — for some windows, other overlap percentages work; for others, 50% is insufficient. Option C is wrong — reconstruction is a signal processing condition unrelated to FFT algorithm requirements. Option D is wrong — rectangular windows are not required; in fact, many applications use smooth windows.

---

**Q11 — Answer: A ($T_{obs} > 1/\Delta f$)**

The DFT frequency resolution for a rectangular window is $\Delta f_{bin} = 1/T_{obs}$ Hz. Two sinusoids can be resolved when they are separated by at least one bin width: $f_2 - f_1 = \Delta f \geq 1/T_{obs}$, i.e., $T_{obs} \geq 1/\Delta f$. Strict inequality gives guaranteed resolution. Option B ($2/\Delta f$) is overly conservative. Option C has the wrong units/relationship. Option D ($1/(2\Delta f)$) would halve the required observation time and lead to unresolved peaks — applying Rayleigh criterion incorrectly.

---

**Q12 — Answer: B**

The periodogram is computed from a finite-length record, equivalent to multiplying the infinite-duration signal by a rectangular window $w[n]$ of length $N$. In the frequency domain, the expected value of the periodogram is the true PSD convolved with the power spectrum of the rectangular window (the Fejér kernel $|W_N(e^{j\omega})|^2/N$). This convolution smears the true PSD, causing bias. As $N \to \infty$, the Fejér kernel narrows toward a delta function and the bias vanishes — explaining asymptotic unbiasedness. Option A is wrong — the data variance is separate from the PSD estimator bias. Option C is wrong — Welch's method addresses variance, not bias (its segments also use windows). Option D conflates FFT size with data length.

---

**Q13 — Answer: D (Kaiser window with large $\beta$)**

When a weak tone sits close in frequency to a strong tone, the key requirement is very low sidelobes to prevent the strong tone's leakage from masking the weak one. The Kaiser window has an adjustable parameter $\beta$ that directly controls the sidelobe level: larger $\beta$ gives lower sidelobes (and a wider mainlobe). For 60 dB dynamic range, a Kaiser window with $\beta \approx 6$–8 achieves sidelobes around $-70$ to $-80\ \text{dB}$. The rectangular window (A) has the worst sidelobes at $-13\ \text{dB}$. Hann (B) achieves about $-32\ \text{dB}$. Hamming (C) achieves about $-43\ \text{dB}$. All would fail to prevent the strong tone from masking the weak one at 60 dB separation.

---

**Q14 — Answer: B ($\frac{N}{2}\log_2 N$)**

In the radix-2 FFT with $N = 2^L$, there are $L = \log_2 N$ stages, each containing $N/2$ butterflies, each requiring 1 complex multiplication (the twiddle factor, including the trivial $W_N^0$). Total: $\frac{N}{2} \times \log_2 N$ complex multiplications. In practice, $W_N^0 = 1$ and $W_N^{N/2} = -1$ are often excluded as trivial, slightly reducing the count, but the exact count including all twiddle factors is $\frac{N}{2}\log_2 N$. Option A ($N\log_2 N$) doubles the correct answer. Option C is the direct DFT complexity divided by 4. Option D further divides by 4.

---

**Q15 — Answer: B**

The Heisenberg–Gabor uncertainty principle from quantum mechanics has a direct signal-processing analogue: the product of the RMS duration $\sigma_t$ and RMS bandwidth $\sigma_f$ of a signal (or analysis window) satisfies $\sigma_t \sigma_f \geq 1/(4\pi)$. For the STFT, using a short window to improve time resolution necessarily degrades frequency resolution and vice versa. The Gaussian window achieves the lower bound. Option A is wrong — sampling rate affects the range of frequencies representable, not the time-frequency resolution trade-off. Option C is wrong — larger FFT with the same window length only interpolates the spectrum (zero-padding effect). Option D is directly contradicted by the uncertainty principle.

---

**Q16 — Answer: C**

For Welch's method with 50% overlap and a Hann window: the number of segments is approximately $K \approx 2N_{total}/L - 1 \approx 2N_{total}/L$. Each overlapping segment is not fully independent, but due to the Hann window weighting, the effective number of independent averages is approximately $8K/3$ per unit of $K$. More precisely, the variance reduction factor is approximately $8N_{total}/(3L)$ — slightly less than a factor of $2N_{total}/L$ from full independence, reduced by $8/3$ times due to the window. Option A ($L/N_{total}$) is the inverse of the correct factor. Option B confuses the window power loss as a variance increase rather than understanding it modifies the effective averaging count. Option D ignores the benefit of overlapping.

---

**Q17 — Answer: C (16 ms)**

The time resolution (duration of each analysis frame) equals the window length divided by the sampling rate, regardless of hop size. With a 256-point window at $f_s = 16\ \text{kHz}$:

$$T_{frame} = \frac{256}{16000} = 0.016\ \text{s} = 16\ \text{ms}$$

The hop size $H = 64$ samples determines the time step between successive frames (the temporal sampling of the spectrogram): $T_{hop} = 64/16000 = 4\ \text{ms}$. Option A (4 ms) is the hop duration, not the frame duration. Option B (8 ms) corresponds to a 128-point window. Option D (32 ms) corresponds to a 512-point window.
