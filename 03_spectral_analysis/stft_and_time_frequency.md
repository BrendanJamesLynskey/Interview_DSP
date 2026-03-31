# STFT and Time-Frequency Analysis: Interview Questions

## Overview

The Short-Time Fourier Transform (STFT) extends the DFT to non-stationary signals by computing spectra over sliding windows. It forms the foundation of the spectrogram, vocoders, audio codecs (MP3, AAC), and speech recognition front ends. Interview questions range from the basic definition to deep trade-offs against wavelet analysis.

---

## Tier 1: Fundamentals

### Q1. Define the STFT. What problem does it solve that the DFT cannot?

**Answer.**

**The problem with the DFT for non-stationary signals.** The DFT gives a single global frequency representation of the entire signal. For a signal whose frequency content changes over time (speech, music, EEG, radar returns), the DFT shows which frequencies are present but gives no information about *when* they occur.

**STFT definition.** The Short-Time Fourier Transform of a discrete-time signal $x[n]$ is:

$$\text{STFT}\{x\}[m, k] = X[m, k] = \sum_{n=-\infty}^{\infty} x[n] \, w[n - mH] \, e^{-j2\pi kn/N}$$

where:
- $w[n]$ is the analysis window of length $L$
- $m$ is the time frame index (discrete)
- $H$ is the hop size (samples between successive frames)
- $k$ is the frequency bin index ($k = 0, \ldots, N-1$)
- $N \geq L$ is the DFT length (with zero-padding if $N > L$)

**Physical interpretation.** At frame $m$, the window $w[n - mH]$ is centred at sample $mH$. The STFT computes the spectrum of the windowed (localised) signal around that time instant. As $m$ increases, the window slides forward by $H$ samples.

**What STFT provides that DFT cannot:** simultaneous time and frequency localisation — a 2D time-frequency representation revealing how the spectral content evolves over time.

---

### Q2. What is the spectrogram and how is it related to the STFT?

**Answer.**

The **spectrogram** is the squared magnitude of the STFT:

$$\text{SPEC}[m, k] = |X[m, k]|^2 = \left|\sum_{n} x[n] w[n - mH] e^{-j2\pi kn/N}\right|^2$$

It represents the power at frequency bin $k$ in time frame $m$, and is a real-valued, non-negative quantity.

**Units and scaling.** If $x[n]$ has units of volts, then $|X[m,k]|^2$ has units of V². Normalised by window length and sampling frequency, it becomes a power spectral density in V²/Hz.

**Relationship to PSD.** The spectrogram at frame $m$ is exactly the windowed periodogram of the data centred around time $mH$:

$$\text{SPEC}[m, k] = \frac{|X[m,k]|^2}{f_s \sum_n w^2[n]}$$

**Visualisation.** Spectrograms are typically displayed as colour maps with:
- Horizontal axis: time (frame index $m$)
- Vertical axis: frequency (bin index $k$)
- Colour/brightness: power (in dB for display)

**Common applications.** Speech analysis and recognition, music instrument identification, acoustic diagnostics, bat echolocation studies, communications signal monitoring.

---

### Q3. What are the time and frequency resolutions of the STFT? How are they determined?

**Answer.**

**Time resolution.** In the STFT, all spectral values within one frame are computed from a window of $L$ samples. The time resolution (the minimum duration of a transient that can be localised) is approximately:

$$\Delta t = \frac{L}{f_s} \quad \text{(seconds)}$$

More precisely, the effective time resolution is the RMS duration of the window:

$$\Delta t = T_s \sqrt{\frac{\sum_n (n - \bar{n})^2 w^2[n]}{\sum_n w^2[n]}}$$

where $\bar{n}$ is the window centre. A shorter window gives better time resolution.

**Frequency resolution.** The width of each DFT bin is $f_s/N$, but the effective frequency resolution is determined by the window mainlobe width:

$$\Delta f \approx m \cdot \frac{f_s}{L}$$

where $m$ depends on the window ($m = 1$ for rectangular, $m = 2$ for Hann). A longer window gives better frequency resolution.

**The key dependency:** $\Delta t \propto L$ and $\Delta f \propto 1/L$, so:

$$\Delta t \cdot \Delta f \approx \frac{m \cdot f_s}{f_s} = m \geq 1$$

This inverse relationship means you cannot improve both simultaneously by adjusting window length alone — a single $L$ must be chosen that balances the two needs for the application.

---

### Q4. What is the hop size and how does it relate to the temporal sampling of the STFT?

**Answer.**

The **hop size** $H$ (samples) is the shift between successive analysis windows. It determines:

1. **Time resolution of frames.** Successive STFT frames are separated by $H/f_s$ seconds. The STFT is sampled in time at rate $f_s/H$ frames/second. The hop size must satisfy $H \leq L$ (frames must not skip data) and for faithful temporal analysis, $H \ll L$.

2. **Overlap fraction.** Overlap $= 1 - H/L$. Common values:
   - 50% overlap: $H = L/2$
   - 75% overlap: $H = L/4$

3. **Redundancy vs. computation.** Smaller $H$ gives more frames (finer temporal sampling, better time resolution of frame-by-frame features), at proportionally higher computational cost.

4. **Perfect reconstruction constraint.** For the STFT to support perfect reconstruction (synthesis via overlap-add), the window and hop size must satisfy the **overlap-add (OLA) condition**:

$$\sum_{m} w[n - mH] = C \quad \text{(constant, for all } n\text{)}$$

For the Hann window, 50% overlap ($H = L/2$) satisfies this: $w[n] + w[n - L/2] = 1$ (the two halves of adjacent Hann windows sum to a constant). 75% overlap ($H = L/4$) also works but requires all four overlapping segments to sum to constant.

---

## Tier 2: Intermediate

### Q5. State and explain the time-frequency uncertainty principle for the STFT. What are its implications?

**Answer.**

**The Heisenberg-Gabor uncertainty principle.** For any analysis window $w(t)$ with unit energy ($\|w\|_2 = 1$), the product of its effective time duration $\Delta t$ and effective bandwidth $\Delta f$ satisfies:

$$\Delta t \cdot \Delta f \geq \frac{1}{4\pi}$$

where (in continuous time):

$$\Delta t^2 = \int_{-\infty}^{\infty} t^2 |w(t)|^2 dt, \quad \Delta f^2 = \int_{-\infty}^{\infty} f^2 |\hat{W}(f)|^2 df$$

**The equality case.** The uncertainty bound is achieved only by the **Gaussian window** $w(t) = e^{-t^2/(2\sigma^2)}$, which has $\Delta t = \sigma/\sqrt{2}$ and $\Delta f = 1/(2\pi\sigma\sqrt{2})$, so $\Delta t \cdot \Delta f = 1/(4\pi)$. The Gabor transform uses Gaussian windows and is the optimal STFT from this perspective.

**Implications for the STFT:**

1. **Fixed resolution for all frequencies.** The STFT uses the same window for all frequencies, so $\Delta t$ and $\Delta f$ are constant across the time-frequency plane (a uniform rectangular tiling).

2. **Cannot achieve good resolution everywhere.** A short window needed for time-localising a transient (small $\Delta t$) forces wide $\Delta f$ — frequency resolution is poor. A long window needed to resolve closely spaced sinusoids (small $\Delta f$) forces wide $\Delta t$ — time resolution is poor.

3. **Contrast with wavelets.** The wavelet transform achieves **constant relative bandwidth** ($\Delta f / f$ = constant), giving fine time resolution at high frequencies and fine frequency resolution at low frequencies. This is more appropriate for signals like speech and music whose relevant features scale with frequency.

---

### Q6. How does the STFT relate to a filter bank? What does each frequency bin represent?

**Answer.**

**Filter bank interpretation.** The STFT at frequency bin $k$ can be written as:

$$X[m, k] = \left(x[n] \cdot e^{-j2\pi kn/N}\right) * w[-n] \bigg|_{n = mH}$$

This is a **modulation-demodulation** (heterodyne) filter bank:
1. Modulate $x[n]$ by $e^{-j2\pi kn/N}$ (frequency shift signal down by $kf_s/N$)
2. Apply a lowpass filter with impulse response $w[-n]$ (the window, reversed)
3. Sample the output at rate $f_s/H$ (decimate by $H$)

**Each frequency bin is a bandpass filter** centred at $kf_s/N$ with bandwidth equal to the window's mainlobe width. The $N$ bins of the STFT form a bank of $N$ bandpass filters, all with the same bandwidth (since all windows are the same shape), uniformly spaced in frequency.

**Polyphase implementation.** This filter bank structure enables an efficient polyphase implementation of the STFT at complexity $O(N \log N)$ per frame (i.e., per hop), compared to $O(N^2)$ for direct computation.

**Synthesis (reconstruction) filter bank.** Overlap-add synthesis uses a synthesis window $w_s[n]$ applied to the inverse-DFT of each frame. When both analysis window, synthesis window, and hop size satisfy the biorthogonality condition:

$$\sum_m w_a[n - mH] \, w_s[n - mH] = 1 \quad \forall n$$

perfect reconstruction $\hat{x}[n] = x[n]$ is achieved.

---

### Q7. Explain the STFT resolution trade-off through a concrete numerical example involving speech analysis.

**Answer.**

**Application context.** Speech has two types of structure that require conflicting resolutions:
- **Pitch harmonics**: closely spaced sinusoids at multiples of the fundamental frequency $F_0 \approx 100$–$300$ Hz. Need $\Delta f < F_0$, i.e., $\Delta f < 100$ Hz to resolve individual harmonics.
- **Formant transitions**: rapid changes in spectral envelope as the vocal tract moves. Formant transitions can occur in $< 20$ ms. Need $\Delta t < 20$ ms.

**Example: choosing window length for speech at $f_s = 16000$ Hz.**

**Option A: long window ($L = 40$ ms = 640 samples).**
- $\Delta f = f_s / L = 16000/640 = 25$ Hz (resolves harmonics well)
- $\Delta t = 40$ ms (misses rapid formant transitions — smears them in time)
- Use for: pitch analysis, speaker identification, harmonic analysis.

**Option B: short window ($L = 5$ ms = 80 samples).**
- $\Delta f = f_s / L = 16000/80 = 200$ Hz (cannot resolve individual harmonics)
- $\Delta t = 5$ ms (captures rapid phonetic transitions accurately)
- Use for: speech recognition feature extraction (MFCC), where envelope shape matters more than fine harmonic structure.

**Standard speech analysis practice:**
- Long window (30–40 ms, Hamming): narrowband spectrogram showing pitch harmonics. Hop size 10 ms.
- Short window (5–10 ms, Hamming): wideband spectrogram showing formant trajectories.

Neither is universally better — the choice depends on what the application needs to measure.

---

### Q8. What is the overlap-add (OLA) method for STFT-based processing? When is perfect reconstruction possible?

**Answer.**

**OLA synthesis method.** Given modified STFT coefficients $\tilde{X}[m,k]$ (e.g., after spectral masking, pitch shifting, or time stretching), synthesise $\hat{x}[n]$ as:

1. **Inverse DFT each frame:** $\tilde{x}_m[n] = \text{IDFT}\{\tilde{X}[m, \cdot]\}$ for each frame $m$
2. **Apply synthesis window:** $y_m[n] = \tilde{x}_m[n] \cdot w_s[n]$
3. **Overlap-add:** $\hat{x}[n] = \sum_m y_m[n - mH]$

**Perfect reconstruction condition.** For the round-trip $x[n] \to \text{STFT} \to \text{ISTFT} \to \hat{x}[n] = x[n]$ with no modifications:

$$\sum_m w_a[n - mH] \, w_s[n - mH] = C \quad \forall n$$

**Common solutions:**
- $w_a = w_s = $ Hann, $H = L/2$: both windows sum to 1. (Hann-OLA method)
- $w_a = $ rectangular, $w_s = $ rectangular, $H = L$: non-overlapping — perfect reconstruction trivially.
- $w_a = $ Hann, $w_s = $ rectangular: requires $H = L/2$ and $w_s = 2$ (scaled).

**Practical implementation note.** The Hann window with 50% overlap is the most common choice for audio processing: the analysis window provides good spectral properties (low sidelobes), and the reconstruction is exact for unmodified signals. When the STFT is modified (e.g., in a noise reduction system), reconstruction is generally no longer perfect, but OLA still produces a well-defined output.

---

## Tier 3: Advanced

### Q9. Compare the STFT and continuous wavelet transform (CWT) in terms of time-frequency tiling, applications, and limitations.

**Answer.**

**Time-frequency tiling comparison.**

The STFT partitions the time-frequency plane into a **uniform rectangular grid**: every tile has the same time width $\Delta t = L/f_s$ and frequency width $\Delta f = f_s/L$. This is because the same window length is used at all frequencies.

The CWT uses a **logarithmic (constant-Q) tiling**: at frequency $f$, the time resolution is $\Delta t(f) = 1/f$ (inversely proportional to frequency) and frequency resolution is $\Delta f(f) = f$ (proportional to frequency). This gives $\Delta f / f = $ constant (constant-Q or constant relative bandwidth).

**CWT advantages over STFT:**
1. **Multi-scale transient detection.** Sharp transients (high frequency) are localised with fine time resolution; slow oscillations (low frequency) are resolved with fine relative frequency resolution.
2. **Octave-based frequency spacing** matches human auditory perception and many natural signal structures (e.g., musical notes, biological rhythms).
3. **Zoom capability.** The CWT can analyse a signal simultaneously at coarse and fine scales — like looking at an image at multiple zoom levels.

**STFT advantages over CWT:**
1. **Fixed frequency resolution in Hz** — important when looking for absolute frequency differences (not relative).
2. **Perfect reconstruction** is straightforward and well-established (OLA/WOLA).
3. **Computationally simpler** for real-time processing: one FFT per frame vs. multiple convolutions or filterbank computations.
4. **Better-understood statistical properties** for power spectral density estimation.

**Discrete Wavelet Transform (DWT) vs. STFT.**
The DWT uses dyadic (power-of-2) subsampling and orthogonal wavelet bases. Unlike the STFT or CWT, it produces a non-redundant representation (same number of coefficients as input samples). This makes DWT suitable for compression (JPEG-2000, ECG compression) where redundancy is undesirable.

**Practical choice guideline:**
- Audio/speech processing: STFT (well-established tools, easy modification/resynthesis)
- Transient detection in signals with wide frequency range: CWT (better multi-scale localisation)
- Signal compression: DWT (non-redundant)
- Geophysical/seismic analysis: CWT (scale-invariant features)

---

### Q10. Derive the invertibility condition for the STFT and explain the role of the window in the reconstruction formula.

**Answer.**

**STFT inversion.** For a continuous-time signal (for clarity), the STFT is:

$$X(\tau, \omega) = \int_{-\infty}^{\infty} x(t) \, w(t - \tau) \, e^{-j\omega t} \, dt$$

The inverse STFT is:

$$x(t) = \frac{1}{2\pi C_w} \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} X(\tau, \omega) \, w(t - \tau) \, e^{j\omega t} \, d\omega \, d\tau$$

**Derivation.** Substitute the definition of $X(\tau, \omega)$:

$$\frac{1}{2\pi} \int\!\int X(\tau,\omega) w(t-\tau) e^{j\omega t} d\omega d\tau = \int x(t') w(t'-\tau) \frac{1}{2\pi}\int e^{j\omega(t-t')} d\omega \, d\tau \, dt'$$

Using $\frac{1}{2\pi}\int e^{j\omega(t-t')} d\omega = \delta(t-t')$:

$$= \int x(t') w(t'-\tau) \delta(t-t') d\tau \, dt' = x(t) \int w(t-\tau) d\tau = x(t) \cdot C_w$$

where $C_w = \int w(\tau) d\tau$ is the **window's DC integral** (coherent gain times length).

**Invertibility condition:** $C_w \neq 0$. Any window with nonzero DC gain can invert the STFT.

**Discrete-time version.** For the discrete STFT with hop size $H$, the OLA reconstruction:

$$\hat{x}[n] = \frac{\sum_m \text{IDFT}\{X[m,k]\} \cdot w_s[n-mH]}{\sum_m w_a[n-mH] w_s[n-mH]}$$

is exact when the denominator is a constant for all $n$ (the OLA condition). When $w_a = w_s$ (analysis equals synthesis window), this requires:

$$\sum_m w^2[n - mH] = C \quad \forall n$$

This is the **weighted overlap-add (WOLA)** condition. The Hann window with $H = L/2$ satisfies this: $w^2[n] + w^2[n-L/2] = 0.5 + 0.5 = 1$ (after normalisation).

**Degrees of freedom in reconstruction.** The STFT with hop $H < L$ is overcomplete (redundant): it produces $L/H$ times more samples than the original signal. This redundancy makes the system robust to modifications in the STFT domain — even approximate STFT coefficients can often be inverted accurately using iterative projection algorithms (Griffin-Lim algorithm).

---

### Q11. What is the Wigner-Ville distribution and how does it compare to the spectrogram?

**Answer.**

**Wigner-Ville Distribution (WVD).** The WVD is a quadratic time-frequency representation:

$$W_x(t, f) = \int_{-\infty}^{\infty} x\!\left(t + \frac{\tau}{2}\right) x^*\!\left(t - \frac{\tau}{2}\right) e^{-j2\pi f\tau} d\tau$$

**Properties of the WVD:**

1. **Marginals.** The WVD satisfies exact marginal properties:
   - $\int W_x(t,f) df = |x(t)|^2$ (instantaneous power)
   - $\int W_x(t,f) dt = |X(f)|^2$ (energy spectral density)
   
   The spectrogram does not satisfy exact marginals due to window smoothing.

2. **Instantaneous frequency.** The conditional mean frequency:
   $$\bar{f}(t) = \frac{\int f W_x(t,f) df}{\int W_x(t,f) df}$$
   equals the instantaneous frequency for monocomponent signals (signals with a single time-varying frequency).

3. **Optimal concentration.** The WVD achieves the minimum time-frequency spread for a monocomponent LFM (linear frequency modulated) signal — a straight line in the WVD.

**The cross-term problem.** For a multi-component signal $x(t) = x_1(t) + x_2(t)$:

$$W_x(t,f) = W_{x_1}(t,f) + W_{x_2}(t,f) + 2\text{Re}\{W_{x_1 x_2}(t,f)\}$$

The **cross-terms** $W_{x_1 x_2}$ appear at times and frequencies between the two components. They can be positive and negative, are oscillatory, and are often larger in magnitude than the auto-terms. For signals with more than one component, the WVD is practically difficult to interpret.

**Spectrogram as smoothed WVD.** The spectrogram is equivalent to the WVD smoothed by the Wigner-Ville distribution of the window:

$$\text{SPEC}[t,f] = W_x(t,f) * W_w(t,f)$$

where $*$ denotes 2D convolution. The window's WVD acts as a 2D lowpass filter that suppresses cross-terms but also smooths the auto-terms, blurring the true time-frequency structure. This is the fundamental resolution-cross-term trade-off of all Cohen's class distributions.

---

## Quick Reference: STFT Parameters

| Parameter | Symbol | Typical values (audio) | Effect of increasing |
|---|:-:|:-:|---|
| Window length | $L$ | 256–4096 samples | Better $\Delta f$, worse $\Delta t$ |
| Hop size | $H$ | $L/4$ to $L/2$ | More frames, higher cost |
| Overlap | $1-H/L$ | 50–75% | More redundancy, smoother output |
| DFT length | $N$ | $\geq L$, power of 2 | Finer frequency grid (not resolution) |
| Window type | — | Hann (default) | See windowing file |

**Resolution formulas:**
- Time resolution: $\Delta t = L / f_s$
- Frequency resolution: $\Delta f \approx f_s / L$ (rectangular), $\approx 2f_s/L$ (Hann)
- Uncertainty product: $\Delta t \cdot \Delta f \geq 1/(4\pi)$
- Frames per second: $f_s / H$
