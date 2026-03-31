# Worked Problem 02: Acoustic Echo Canceller Design Using LMS

## Problem Statement

Design an acoustic echo canceller (AEC) for a hands-free telephony system with the following specifications:

- **Echo path:** Room impulse response of length $L_h = 200$ ms at $f_s = 8000$ Hz (1600 taps)
- **Echo tail to cancel:** 99% of echo energy concentrated in first 80 ms (640 taps)
- **Desired echo attenuation:** at least 30 dB (suppression of echo power by factor 1000)
- **Double-talk:** Assume single-talk (near-end speaker is silent during adaptation)
- **Input (far-end) signal:** Voiced speech, modelled as AR(1) with $a = 0.9$, variance $\sigma_x^2 = 0.1$ V²
- **Residual noise floor:** $\sigma_v^2 = 10^{-5}$ V² (microphone thermal noise)

**Tasks:**

1. Determine the adaptive filter length $N$.
2. Derive the step-size bounds and select $\mu$ for a target misadjustment $\mathcal{M} < 5\%$.
3. Estimate the convergence time (time to 30 dB echo return loss enhancement).
4. Compute the steady-state echo return loss enhancement (ERLE).
5. Analyse the effect of near-end noise on convergence and steady-state performance.

---

## Part 1: Filter Length Selection

**Echo path model.** The echo at the microphone is:

$$e_{\text{echo}}[n] = \sum_{k=0}^{L_h - 1} h[k]\, s[n-k]$$

where $h[k]$ is the acoustic echo path (loudspeaker $\to$ room $\to$ microphone) and $s[n]$ is the far-end speech signal played through the loudspeaker.

**Filter length choice.** To cancel 99% of echo energy:

$$N = 0.080 \times f_s = 0.080 \times 8000 = 640 \text{ taps}$$

**Why not use $L_h = 1600$ taps?** Using the full room impulse response would:
- Increase computational cost by 2.5x
- Increase convergence time by 2.5x (time constant $\propto N$)
- Provide minimal improvement since only 1% of echo energy is in the last 960 taps

**Practical trade-off.** Residual echo from the uncancelled tail (960 taps, 1% of energy) provides a floor at approximately:

$$\text{ERLE}_{\text{max}} = -10\log_{10}(0.01) = 20 \text{ dB from tail alone}$$

To exceed 30 dB total ERLE, additional post-filtering (comfort noise injection or spectral suppression) is needed for the residual tail. The adaptive filter handles the 20 dB+ cancellation from the first 640 taps.

---

## Part 2: Step-Size Selection

**Input autocorrelation.** For AR(1) speech with $a = 0.9$, $\sigma_x^2 = 0.1$:

$$R_x[k] = \sigma_x^2 \cdot 0.9^{|k|}$$

**Autocorrelation matrix eigenvalues.** For an $N$-tap Toeplitz matrix with AR(1) statistics, the eigenvalues are approximately distributed between:

$$\lambda_{\min} \approx \frac{\sigma_x^2(1-a^2)}{1+a} \cdot \frac{1}{N} \approx \frac{0.1 \times 0.19}{1.9 \times 640}$$

More precisely, for large $N$, the eigenvalues of the AR(1) Toeplitz matrix are approximately the PSD values at the DFT frequencies:

$$S_x(e^{j\omega}) = \frac{\sigma_u^2}{|1 - ae^{-j\omega}|^2} = \frac{0.1(1-a^2)}{|1-0.9e^{-j\omega}|^2}$$

$$\sigma_u^2 = \sigma_x^2(1 - a^2) = 0.1 \times 0.19 = 0.019$$

**Maximum eigenvalue** (at $\omega = 0$, DC, where AR(1) is most energetic):

$$\lambda_{\max} \approx S_x(1) = \frac{0.019}{|1 - 0.9|^2} = \frac{0.019}{0.01} = 1.9$$

**Minimum eigenvalue** (at $\omega = \pi$, Nyquist):

$$\lambda_{\min} \approx S_x(-1) = \frac{0.019}{|1 + 0.9|^2} = \frac{0.019}{3.61} \approx 0.00526$$

**Eigenvalue spread:**

$$\chi = \frac{\lambda_{\max}}{\lambda_{\min}} \approx \frac{1.9}{0.00526} \approx 361$$

This is severe. The $a = 0.9$ speech model creates a highly ill-conditioned problem — typical for voiced speech.

**Trace of $\mathbf{R}$:**

$$\text{tr}(\mathbf{R}) = N \cdot \sigma_x^2 = 640 \times 0.1 = 64$$

**Stability bound:**

$$\mu < \frac{2}{\lambda_{\max}} \approx \frac{2}{1.9} \approx 1.053$$

**Wait:** this bound seems large. For practical speech inputs, $\lambda_{\max}$ fluctuates significantly. A more conservative practical bound uses the trace:

$$\mu < \frac{2}{\text{tr}(\mathbf{R})} = \frac{2}{64} = 0.03125$$

**Step size for $\mathcal{M} < 5\%$:**

$$\mathcal{M} = \frac{\mu\,\text{tr}(\mathbf{R})}{2} < 0.05 \implies \mu < \frac{0.1}{\text{tr}(\mathbf{R})} = \frac{0.1}{64} \approx 0.00156$$

**Selected step size:** $\mu = 0.001$ (satisfies stability and gives $\mathcal{M} \approx 3.2\%$).

**Using NLMS instead.** For speech with highly variable power, NLMS is strongly preferred:

$$\mu_n = \frac{\tilde\mu}{\delta + \|\mathbf{x}[n]\|^2}$$

With $\|\mathbf{x}[n]\|^2 \approx N\sigma_x^2 = 64$ on average, set $\tilde\mu = 0.3$ for $\mathcal{M} \approx \tilde\mu N / (2 \times N) = \tilde\mu/2 = 15\%$... better to use $\tilde\mu = 0.1$ for $\mathcal{M} \approx 5\%$.

---

## Part 3: Convergence Time Estimation

**Convergence to 30 dB ERLE.** Define ERLE as the ratio of input echo power to residual echo power:

$$\text{ERLE}[n] = -10\log_{10}\!\left(\frac{\mathbb{E}\{e^2[n]\}}{\mathbb{E}\{e_{\text{echo}}^2[n]\}}\right) = -10\log_{10}\!\left(\frac{J[n]}{\sigma_{\text{echo}}^2}\right)$$

where $\sigma_{\text{echo}}^2 = \mathbf{h}_o^T\mathbf{R}\mathbf{h}_o$ is the echo power.

**Simplified learning curve.** Under the independence assumption:

$$J[n] \approx J_{\min} + (J_0 - J_{\min})(1 - 2\mu\bar\lambda)^n$$

where $\bar\lambda = \text{tr}(\mathbf{R})/N = \sigma_x^2 = 0.1$ (average eigenvalue). This uniform-eigenvalue approximation gives:

$$J[n] \approx J_{\min} + J_0 e^{-n/\tau}, \quad \tau = \frac{1}{2\mu\bar\lambda} = \frac{1}{2 \times 0.001 \times 0.1} = 5000 \text{ samples}$$

At 8000 samples/sec, $\tau = 5000/8000 = 0.625$ seconds.

**Initial MSE** (no cancellation): $J_0 \approx \sigma_{\text{echo}}^2 = \mathbf{h}_o^T\mathbf{R}\mathbf{h}_o \approx \|\mathbf{h}_o\|^2 \cdot \sigma_x^2$. For a typical room echo path with normalised taps, let $\|\mathbf{h}_o\|^2 = 1$, so $J_0 = 0.1$.

**Target $J[n]$ for 30 dB ERLE:**

$$J_{30\text{dB}} = J_0 \times 10^{-30/10} = 0.1 \times 10^{-3} = 10^{-4}$$

**Time to achieve 30 dB:**

$$J_{\min} + (J_0 - J_{\min})e^{-n_{30}/\tau} = J_{30\text{dB}}$$

With $J_{\min} \approx \sigma_v^2 = 10^{-5} \ll J_{30\text{dB}}$:

$$J_0 e^{-n_{30}/\tau} \approx J_{30\text{dB}}$$

$$n_{30} = \tau \ln\!\left(\frac{J_0}{J_{30\text{dB}}}\right) = 5000 \times \ln\!\left(\frac{0.1}{10^{-4}}\right) = 5000 \times \ln(1000) \approx 5000 \times 6.908 = 34540 \text{ samples}$$

$$t_{30} = \frac{34540}{8000} \approx 4.3 \text{ seconds}$$

This is a long convergence time. In practice:
- A burst of wideband test signal (MLS, white noise) at startup can force faster convergence.
- NLMS with $\tilde\mu = 0.3$ achieves $\tau \approx N/(2\tilde\mu) = 640/(0.6) \approx 1067$ samples — convergence in $\approx 7376$ samples ($\approx 0.92$ seconds).

**NLMS advantage:** NLMS achieves 4.7x faster convergence than LMS for this problem.

---

## Part 4: Steady-State Echo Return Loss Enhancement

**Steady-state MSE:**

$$J_\infty = J_{\min}(1 + \mathcal{M}) = \sigma_v^2(1 + \mathcal{M})$$

For LMS with $\mu = 0.001$: $\mathcal{M} \approx 0.032$

$$J_\infty = 10^{-5} \times 1.032 = 1.032 \times 10^{-5}$$

**Steady-state ERLE:**

$$\text{ERLE}_\infty = -10\log_{10}\!\left(\frac{J_\infty}{J_0}\right) = -10\log_{10}\!\left(\frac{1.032 \times 10^{-5}}{0.1}\right) = -10\log_{10}(1.032 \times 10^{-4})$$

$$= -10(-4 + \log_{10}(1.032)) \approx 10 \times 3.986 \approx 39.9 \text{ dB}$$

**This exceeds the 30 dB target.**

**Limiting factor.** The steady-state ERLE is limited by:
1. **Noise floor:** $J_{\min} = \sigma_v^2$. With lower noise, ERLE would be higher.
2. **Misadjustment:** Larger $\mu$ increases misadjustment and reduces ERLE.
3. **Echo tail (uncancelled portion):** Contributes a fixed residual that limits ERLE.

**Maximum achievable ERLE** is approximately:

$$\text{ERLE}_{\max} = 10\log_{10}\!\left(\frac{\sigma_{\text{echo}}^2}{\sigma_v^2(1+\mathcal{M})}\right) = 10\log_{10}\!\left(\frac{0.1}{10^{-5} \times 1.032}\right) \approx 10 \times 3.986 = 39.9 \text{ dB}$$

---

## Part 5: Near-End Noise Effect

**Modified model.** During near-end speech activity ($n_e[n]$ with variance $\sigma_e^2$):

$$d[n] = e_{\text{echo}}[n] + n_e[n] + v[n]$$

The LMS algorithm cannot distinguish near-end speech from estimation error, so the near-end speech acts as **additional "noise"** in the gradient:

**Modified minimum MSE:**

$$J_{\min}' = \sigma_v^2 + \sigma_e^2$$

**Modified misadjustment:**

$$\mathcal{M}' = \frac{\mu\,\text{tr}(\mathbf{R})}{2}$$

(unchanged — misadjustment depends only on $\mu$ and input statistics, not noise level)

**Modified steady-state ERLE:**

$$\text{ERLE}'_\infty = 10\log_{10}\!\left(\frac{\sigma_{\text{echo}}^2}{J_{\min}'(1+\mathcal{M}')}\right)$$

For $\sigma_e^2 = 10^{-3}$ (near-end speech at -30 dBFS, 20 dB below echo path input):

$$\text{ERLE}'_\infty = 10\log_{10}\!\left(\frac{0.1}{(10^{-5} + 10^{-3}) \times 1.032}\right) \approx 10\log_{10}(97) \approx 19.9 \text{ dB}$$

This falls below the 30 dB target — but more importantly, the **weight corruption** during double-talk is severe. When near-end speech is active, LMS updates corrupt the filter coefficients. Solutions:

1. **Double-talk detection (DTD):** Freeze adaptation ($\mu = 0$) during double-talk.
2. **Variable step size:** Reduce $\mu$ when near-end speech is detected.
3. **Decorrelating pre-filter:** Reduces eigenvalue spread and accelerates convergence in single-talk.

---

## Complete Python Simulation

```python
import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
np.random.seed(0)
fs = 8000
N_filter = 640       # adaptive filter length (80 ms)
N_sim = 100_000      # simulation samples
mu_lms = 0.001       # LMS step size
mu_tilde = 0.1       # NLMS normalised step size
delta_nlms = 1e-4    # NLMS regularisation

# True echo path (exponentially decaying with oscillation)
n_h = np.arange(N_filter)
h_true = 0.05 * np.exp(-n_h / 100) * np.sin(2 * np.pi * 0.05 * n_h)
h_true = h_true / np.linalg.norm(h_true)  # normalise to unit energy

sigma_x2 = 0.1
sigma_v2 = 1e-5
a_ar = 0.9
sigma_u = np.sqrt(sigma_x2 * (1 - a_ar**2))

# Storage
erle_lms = np.zeros(N_sim)
erle_nlms = np.zeros(N_sim)

for algo in ['LMS', 'NLMS']:
    w = np.zeros(N_filter)
    x_buf = np.zeros(N_filter)
    x_prev = 0.0
    erle_arr = np.zeros(N_sim)
    echo_power_smooth = None
    residual_smooth = None

    for n in range(N_sim):
        # AR(1) input
        x_n = a_ar * x_prev + sigma_u * np.random.randn()
        x_prev = x_n
        x_buf = np.roll(x_buf, 1)
        x_buf[0] = x_n

        # Echo (desired) signal
        echo = h_true @ x_buf
        mic = echo + np.sqrt(sigma_v2) * np.random.randn()

        # AEC output
        y = w @ x_buf
        e = mic - y  # residual error

        # ERLE calculation (exponential smoothing)
        alpha = 0.999
        ep = echo**2
        rp = e**2
        if echo_power_smooth is None:
            echo_power_smooth = ep
            residual_smooth = rp
        else:
            echo_power_smooth = alpha * echo_power_smooth + (1-alpha) * ep
            residual_smooth = alpha * residual_smooth + (1-alpha) * rp

        if echo_power_smooth > 0:
            erle_arr[n] = 10 * np.log10(echo_power_smooth / max(residual_smooth, 1e-12))

        # Weight update
        if algo == 'LMS':
            w = w + mu_lms * e * x_buf
        else:
            norm2 = delta_nlms + x_buf @ x_buf
            w = w + (mu_tilde / norm2) * e * x_buf

    if algo == 'LMS':
        erle_lms = erle_arr
    else:
        erle_nlms = erle_arr

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
t = np.arange(N_sim) / fs
ax.plot(t, erle_lms, alpha=0.7, color='blue', label=f'LMS ($\\mu={mu_lms}$)')
ax.plot(t, erle_nlms, alpha=0.7, color='red', label=f'NLMS ($\\tilde{{\\mu}}={mu_tilde}$)')
ax.axhline(30, color='black', linestyle='--', linewidth=1, label='30 dB target')
ax.set_xlabel('Time (s)')
ax.set_ylabel('ERLE (dB)')
ax.set_title('Acoustic Echo Canceller: LMS vs NLMS Learning Curve')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 45])
plt.tight_layout()
plt.savefig('aec_learning_curve.png', dpi=150)
plt.show()

# Print convergence time to 30 dB
for name, erle in [('LMS', erle_lms), ('NLMS', erle_nlms)]:
    idx = np.argmax(erle >= 30)
    if erle[idx] >= 30:
        print(f"{name}: reached 30 dB ERLE at {idx/fs:.2f} s ({idx} samples)")
    else:
        print(f"{name}: did NOT reach 30 dB ERLE within simulation")
    steady = np.mean(erle[-10000:])
    print(f"  Steady-state ERLE ≈ {steady:.1f} dB")
```

---

## Summary

| Design Parameter | Value | Derivation |
|---|:-:|---|
| Filter length $N$ | 640 taps | 80 ms echo tail at 8 kHz |
| Eigenvalue spread $\chi$ | ~361 | AR(1) with $a=0.9$ |
| Stability bound | $\mu < 0.031$ | $2/\text{tr}(\mathbf{R})$ |
| Selected $\mu$ (LMS) | 0.001 | $\mathcal{M} < 5\%$ |
| Selected $\tilde\mu$ (NLMS) | 0.1 | Normalised, good trade-off |
| Time constant $\tau$ (LMS) | 5000 samples | $1/(2\mu\sigma_x^2)$ |
| Time constant $\tau$ (NLMS) | ~1067 samples | $N/(2\tilde\mu)$ |
| Convergence to 30 dB (LMS) | ~4.3 s | $\tau \ln(J_0/J_{30\text{dB}})$ |
| Convergence to 30 dB (NLMS) | ~0.9 s | Approx. |
| Steady-state ERLE | ~40 dB | Limited by noise floor |

**Design recommendations:**
1. Use NLMS (not LMS) for speech inputs due to highly variable input power and severe eigenvalue spread ($\chi \approx 361$).
2. Implement double-talk detection and freeze adaptation during near-end speech activity.
3. For faster initial convergence, use a step-size schedule: large $\tilde\mu$ initially (0.5), reducing to 0.1 once filter converges.
4. Consider supplementing the AEC with a residual echo suppressor (spectral subtraction) to handle the uncancelled echo tail.
