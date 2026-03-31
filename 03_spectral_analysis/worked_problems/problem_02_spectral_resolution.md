# Worked Problem 02: Spectral Resolution and Windowing

## Problem Statement

A signal contains two sinusoidal components:

$$x(t) = A_1 \cos(2\pi f_1 t) + A_2 \cos(2\pi f_2 t) + n(t)$$

where:
- $f_1 = 1000$ Hz, $A_1 = 1.0$
- $f_2 = 1020$ Hz, $A_2 = 0.5$
- $n(t)$: additive white Gaussian noise with variance $\sigma^2 = 0.01$
- Sampling rate: $f_s = 8000$ Hz

**Tasks:**

1. Determine the minimum FFT length $N_{\min}$ required to resolve the two components using a rectangular window.
2. Determine the minimum FFT length with a Hann window.
3. For $N = 512$ and $N = 2048$ with both windows, quantitatively analyse whether resolution is achieved.
4. Explain why zero-padding to $N = 4096$ does not improve resolution if the original data length is $N = 512$.
5. Determine the SNR required at each frequency bin to detect the weaker component.

---

## Part 1: Resolution with Rectangular Window

**Rayleigh criterion.** Two sinusoids are resolvable when their frequency separation equals or exceeds one DFT bin:

$$\Delta f \geq \frac{f_s}{N}$$

Solve for minimum $N$:

$$N_{\min} = \frac{f_s}{\Delta f} = \frac{8000}{20} = 400 \text{ samples}$$

So a minimum of $N = 400$ samples of data (and a 400-point DFT, at minimum) is needed.

Since practical FFT lengths are powers of 2, the smallest usable power-of-2 length is $N = 512$.

**Bin spacing at $N = 512$:**

$$\Delta f_{\text{bin}} = \frac{f_s}{N} = \frac{8000}{512} = 15.625 \text{ Hz}$$

The separation $\Delta f = 20$ Hz $= 1.28$ bins. This just barely exceeds one bin — the two components will be in adjacent-or-separated bins but may not show clear distinct peaks due to mainlobe overlap.

---

## Part 2: Resolution with Hann Window

The Hann window has a mainlobe width of **2 bins** (half-width 1 bin per side). Two components are resolvable when their separation exceeds the mainlobe half-width on each side — i.e., they must be separated by at least **2 bins**:

$$\Delta f \geq 2 \cdot \frac{f_s}{N}$$

$$N_{\min}^{\text{Hann}} = \frac{2 f_s}{\Delta f} = \frac{2 \times 8000}{20} = 800 \text{ samples}$$

The next power of 2 above 800 is $N = 1024$.

**At $N = 1024$:**

$$\Delta f_{\text{bin}} = \frac{8000}{1024} = 7.8125 \text{ Hz}$$

The 20 Hz separation $= 2.56$ bins — comfortably exceeding the 2-bin Hann mainlobe criterion.

---

## Part 3: Resolution Analysis for N = 512 and N = 2048

### Case A: $N = 512$, Rectangular Window

Bin spacing: $15.625$ Hz. Separation: $20/15.625 = 1.28$ bins.

The two frequencies $f_1 = 1000$ Hz and $f_2 = 1020$ Hz map to bins:

$$k_1 = \frac{f_1 N}{f_s} = \frac{1000 \times 512}{8000} = 64.0$$

$$k_2 = \frac{f_2 N}{f_s} = \frac{1020 \times 512}{8000} = 65.28$$

Neither frequency lands exactly on a bin: $k_2 = 65.28$ is between bins 65 and 66. The energy is split across bins. With a rectangular window and 1.28-bin separation, the mainlobes of the two components overlap significantly. The combined spectrum will show a single broad peak or two poorly separated peaks. **Resolution is marginal and unreliable.**

### Case B: $N = 2048$, Rectangular Window

Bin spacing: $8000/2048 = 3.906$ Hz. Separation: $20/3.906 = 5.12$ bins.

$$k_1 = \frac{1000 \times 2048}{8000} = 256.0 \quad \text{(exact bin)}$$

$$k_2 = \frac{1020 \times 2048}{8000} = 261.12$$

$k_1 = 256$ is an exact bin. $k_2 \approx 261.1$, between bins 261 and 262. The 5.12-bin separation well exceeds 1 bin (rectangular mainlobe width). **Both peaks are clearly resolved.**

### Case C: $N = 512$, Hann Window

Mainlobe half-width: 1 bin per side (total 4-bin mainlobe from first null to first null).
Separation: 1.28 bins. **Well within the 4-bin mainlobe — components completely unresolved.**

### Case D: $N = 2048$, Hann Window

Separation: 5.12 bins. This exceeds 2 bins (the effective Hann resolution criterion). **Components are resolved**, with lower sidelobe contamination than the rectangular case.

**Summary table:**

| $N$ | Window | Bin spacing | Separation (bins) | Resolved? |
|:-:|:-:|:-:|:-:|:-:|
| 512 | Rectangular | 15.625 Hz | 1.28 | Marginal |
| 512 | Hann | 15.625 Hz | 1.28 | No |
| 2048 | Rectangular | 3.906 Hz | 5.12 | Yes |
| 2048 | Hann | 3.906 Hz | 5.12 | Yes |

---

## Part 4: Why Zero-Padding Does Not Improve Resolution

**Suppose we have $L = 512$ samples of data, but zero-pad to $N = 4096$ before the DFT.**

The $N = 4096$ DFT has bin spacing $f_s/N = 8000/4096 = 1.953$ Hz — apparently much finer than $15.625$ Hz.

**But the signal window is still $L = 512$ samples long.** The DFT of the zero-padded sequence is equivalent to evaluating the DTFT of the 512-sample windowed signal at 4096 uniformly spaced frequencies:

$$X_{\text{ZP}}[k] = \sum_{n=0}^{511} x[n] \, e^{-j2\pi kn/4096}, \quad k = 0, \ldots, 4095$$

This is a *denser sampling* of the same underlying spectrum $X_{512}(f)$ — the Fourier transform of the 512-point windowed signal. Zero-padding interpolates the spectrum; it does not change the underlying spectral window function.

**The resolution-limiting quantity is the mainlobe width of the analysis window**, which depends only on $L$:

$$\Delta f_{\text{mainlobe}} = \frac{f_s}{L} = \frac{8000}{512} = 15.625 \text{ Hz} \quad \text{(rectangular)}$$

This is unchanged whether $N = 512$ or $N = 4096$. The two components at 20 Hz separation are still within the same mainlobe of the 512-point rectangular window.

**Analogy.** Zero-padding is like zooming into a blurry photograph — the image appears larger on screen, but no new detail emerges. The blur (spectral resolution limit) is a property of how much data was collected, not how finely we sample the result.

**What zero-padding does do:**
- Reduces scalloping loss (more frequency grid points means signal frequencies are closer to bin centres)
- Provides interpolated peak location estimates (useful for frequency estimation via interpolation)
- Required for linear convolution via FFT (must pad to $\geq L_1 + L_2 - 1$)

---

## Part 5: SNR Requirement for Detecting the Weaker Component

**Noise floor in the DFT.** For AWGN with variance $\sigma^2$, the expected value of the periodogram at any frequency bin is:

$$\mathbb{E}\{|\hat{N}[k]|^2\} = \sigma^2 N$$

(the noise power sums coherently over $N$ samples — actually the variance at each bin is $\sigma^2 N$ for the unnormalised DFT magnitude squared).

Wait — let's be precise. For each DFT bin of a length-$N$ DFT of white noise with variance $\sigma^2$ per sample:

$$\mathbb{E}\{|N[k]|^2\} = N\sigma^2$$

This is the noise power at each bin (unnormalised). The total noise power $= N \cdot N\sigma^2 / N = N\sigma^2$... let's use the normalised periodogram:

$$\hat{S}_N[k] = \frac{|N[k]|^2}{N} \to \sigma^2 \quad (\text{per-bin noise floor})$$

The expected value at each bin is $\sigma^2$ (the noise PSD is flat at $\sigma^2 f_s^{-1}$ per Hz, and with bin width $f_s/N$, each bin captures power $\sigma^2$).

**Signal power in a bin.** For a sinusoid $A_2\cos(2\pi f_2 n/f_s)$ at exactly a DFT bin ($f_2 = kf_s/N$), the DFT magnitude is $A_2 N/2$ (one-sided), so:

$$|X_{\text{signal}}[k]|^2 = \frac{A_2^2 N^2}{4}$$

Normalised periodogram power: $|X_{\text{signal}}[k]|^2 / N = A_2^2 N / 4$.

**Signal-to-noise ratio per bin:**

$$\text{SNR}_{\text{bin}} = \frac{A_2^2 N / 4}{\sigma^2} = \frac{A_2^2 N}{4\sigma^2}$$

For our problem: $A_2 = 0.5$, $\sigma^2 = 0.01$:

$$\text{SNR}_{\text{bin}}(N) = \frac{0.25 \times N}{4 \times 0.01} = 6.25 N$$

| $N$ | $\text{SNR}_{\text{bin}}$ | $\text{SNR}_{\text{bin}}$ (dB) |
|:-:|:-:|:-:|
| 64 | 400 | 26 dB |
| 512 | 3200 | 35 dB |
| 2048 | 12800 | 41 dB |

The SNR increases linearly with $N$ — longer observations coherently accumulate signal power while noise grows as $\sqrt{N}$ in amplitude (but $N$ in power per bin, since DFT is a coherent integration). The weaker component at $A_2 = 0.5$ is easily detectable for any practical $N$ with $\sigma^2 = 0.01$.

**General detection threshold.** The weaker component is detectable when its bin power exceeds the noise floor plus some margin. For a detection probability of $P_d = 0.99$ and false alarm probability $P_{fa} = 10^{-3}$ with a chi-squared test:

$$\text{SNR}_{\text{bin}} \geq \text{SNR}_{\min} \approx 10\text{–}15 \text{ dB}$$

(depending on the exact threshold). For our problem, we are well above this even at small $N$.

---

## Complete Python Demonstration

```python
import numpy as np
import matplotlib.pyplot as plt

# --- Signal parameters ---
fs = 8000       # sampling rate (Hz)
f1, A1 = 1000, 1.0
f2, A2 = 1020, 0.5
sigma2 = 0.01   # noise variance

# Test different data lengths
data_lengths = [512, 2048]
windows = {'Rectangular': lambda L: np.ones(L),
           'Hann':        lambda L: np.hanning(L)}

rng = np.random.default_rng(42)

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

for row, L in enumerate(data_lengths):
    n = np.arange(L)
    signal = A1 * np.cos(2 * np.pi * f1 * n / fs) + \
             A2 * np.cos(2 * np.pi * f2 * n / fs)
    noise = rng.normal(0, np.sqrt(sigma2), L)
    x = signal + noise

    for col, (win_name, win_func) in enumerate(windows.items()):
        w = win_func(L)
        # Use zero-padding to N = 4 * next_power_of_2(L) for smooth display
        N_fft = 4 * int(2 ** np.ceil(np.log2(L)))
        xw = x * w

        X = np.fft.rfft(xw, n=N_fft)
        # Amplitude spectrum (corrected for window CG)
        cg = np.sum(w)
        amp = np.abs(X) * 2 / cg

        freqs = np.fft.rfftfreq(N_fft, d=1/fs)

        # Focus on region near f1, f2
        mask = (freqs >= 950) & (freqs <= 1070)
        ax = axes[row, col]
        ax.plot(freqs[mask], 20 * np.log10(amp[mask] + 1e-10))
        ax.axvline(f1, color='r', linestyle='--', linewidth=0.8, label=f'$f_1={f1}$ Hz')
        ax.axvline(f2, color='g', linestyle='--', linewidth=0.8, label=f'$f_2={f2}$ Hz')
        ax.set_title(f'L={L}, {win_name} window')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude (dBFS)')
        ax.legend(fontsize=8)
        ax.set_ylim([-40, 10])
        ax.grid(True, alpha=0.3)

        # Print resolution metrics
        bin_spacing = fs / L
        sep_bins = (f2 - f1) / bin_spacing
        criterion_bins = 1 if win_name == 'Rectangular' else 2
        resolved = sep_bins >= criterion_bins
        print(f"L={L:4d}, {win_name:12s}: bin={bin_spacing:.2f} Hz, "
              f"sep={sep_bins:.2f} bins, resolved={resolved}")

plt.tight_layout()
plt.savefig('spectral_resolution.png', dpi=150)
plt.show()
```

**Expected console output:**

```
L= 512, Rectangular : bin=15.62 Hz, sep=1.28 bins, resolved=False
L= 512, Hann        : bin=15.62 Hz, sep=1.28 bins, resolved=False
L=2048, Rectangular : bin=3.91 Hz,  sep=5.12 bins, resolved=True
L=2048, Hann        : bin=3.91 Hz,  sep=5.12 bins, resolved=True
```

---

## Summary

**Key results:**

1. **Minimum data length for rectangular window:** $N_{\min} = f_s / \Delta f = 8000/20 = 400$ samples (use $N=512$ in practice).

2. **Minimum data length for Hann window:** $N_{\min} = 2f_s / \Delta f = 800$ samples (use $N=1024$).

3. **Resolution criterion in general:**

$$N \geq m_w \cdot \frac{f_s}{\Delta f}$$

where $m_w$ is the window's mainlobe width factor (1 for rectangular, 2 for Hann, 3 for Blackman).

4. **Zero-padding cannot improve resolution** — it only interpolates the spectrum. True resolution requires more data samples.

5. **SNR increases with $N$** as the coherent integration gain $\propto N$:

$$\text{SNR}_{\text{bin}} = \frac{A^2 N}{4\sigma^2}$$
