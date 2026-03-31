# Worked Problem 02: IIR Butterworth Filter via Bilinear Transform

**Subject:** Digital Signal Processing
**Topic:** Analog Prototype, Bilinear Transform, Frequency Warping, Pole Mapping
**Difficulty:** Intermediate to Advanced

---

## Problem Statement

Design a **3rd-order Butterworth lowpass IIR filter** using the bilinear transform with the following digital specifications:

- Sample rate: $f_s = 8{,}000\,\text{Hz}$ (telephone quality)
- Digital cutoff (3 dB point): $f_c = 3{,}400\,\text{Hz}$ (voice band upper edge)

**Tasks:**

**(a)** Pre-warp the digital cutoff frequency to obtain the analog prototype cutoff.

**(b)** Find the 3rd-order Butterworth analog prototype poles.

**(c)** Construct the analog transfer function $H_a(s)$.

**(d)** Apply the bilinear transform to obtain $H(z)$.

**(e)** Verify the digital cutoff frequency. Compute the DC gain and Nyquist gain.

**(f)** Write the corresponding difference equation and a Python implementation.

---

## Part (a): Pre-Warping the Digital Cutoff

The bilinear transform maps analog frequency $\Omega$ to digital frequency $\omega$ via:

$$\omega = 2\arctan\!\left(\frac{\Omega T_s}{2}\right) \implies \Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)$$

The digital cutoff in radians per sample:

$$\omega_c = 2\pi\frac{f_c}{f_s} = 2\pi\frac{3400}{8000} = \frac{17\pi}{20} = 0.85\pi\,\text{rad/sample}$$

Pre-warped analog cutoff:

$$\Omega_c = \frac{2}{T_s}\tan\!\left(\frac{\omega_c}{2}\right) = 2f_s\tan\!\left(\frac{0.85\pi}{2}\right)$$

Compute $\tan(0.425\pi) = \tan(76.5°)$:

$$\tan(76.5°) = \tan\!\left(\frac{17\pi}{40}\right) \approx 4.165$$

$$\Omega_c = 2 \times 8000 \times 4.165 = 66{,}640\,\text{rad/s}$$

**Interpretation:** The severe pre-warping (factor of 4.165 instead of the expected $2\pi f_c \approx 21{,}363$ rad/s) is because $f_c = 3{,}400\,\text{Hz}$ is very close to the Nyquist frequency $f_N = 4{,}000\,\text{Hz}$. Near Nyquist, the bilinear transform's tangent mapping compresses a wide analog frequency range into a narrow digital range, requiring a much higher analog prototype cutoff to place the digital cutoff correctly.

---

## Part (b): 3rd-Order Butterworth Poles

The normalised 3rd-order Butterworth prototype (cutoff $\Omega = 1$ rad/s) has poles at:

$$s_k = e^{j\pi(2k + N - 1)/(2N)}, \quad k = 1, 2, 3 \quad (N = 3)$$

$$s_1 = e^{j\pi(2+2)/6} = e^{j2\pi/3} = -\frac{1}{2} + j\frac{\sqrt{3}}{2}$$

$$s_2 = e^{j\pi(4+2)/6} = e^{j\pi} = -1$$

$$s_3 = e^{j\pi(6+2)/6} = e^{j4\pi/3} = -\frac{1}{2} - j\frac{\sqrt{3}}{2}$$

**Verification:** All poles lie on the unit circle in the left half-plane (Re$(s_k) < 0$). The angles are at $120°$, $180°$, $240°$ — equally spaced, standard for $N=3$.

**Scaled to $\Omega_c = 66{,}640$ rad/s:**

Multiply each normalised pole by $\Omega_c$:

$$s_1 = \Omega_c\left(-\frac{1}{2} + j\frac{\sqrt{3}}{2}\right) = 66640(-0.5 + 0.866j) = -33320 + 57702j$$

$$s_2 = -\Omega_c = -66{,}640$$

$$s_3 = -33320 - 57702j$$

---

## Part (c): Analog Transfer Function $H_a(s)$

$$H_a(s) = \frac{\Omega_c^3}{\prod_{k=1}^{3}(s - s_k)}$$

Grouping the complex conjugate pair $(s_1, s_3)$:

$$(s - s_1)(s - s_3) = s^2 + \Omega_c\,s + \Omega_c^2 = s^2 + 66640\,s + 66640^2$$

$$(s^2 + 66640\,s + 4.441 \times 10^9)(s + 66640)$$

Expanding:

$$H_a(s) = \frac{66640^3}{(s + 66640)(s^2 + 66640\,s + 66640^2)} = \frac{\Omega_c^3}{(s + \Omega_c)(s^2 + \Omega_c s + \Omega_c^2)}$$

**Alternatively in factored form:**

$$H_a(s) = \frac{\Omega_c^3}{(s + \Omega_c)\left(s^2 + \Omega_c\,s + \Omega_c^2\right)}$$

where $\Omega_c = 66{,}640$.

---

## Part (d): Bilinear Transform — Applying $s = \frac{2}{T_s}\cdot\frac{1-z^{-1}}{1+z^{-1}}$

Let $c = 2/T_s = 2f_s = 16{,}000$. The substitution is $s = c\,\frac{1-z^{-1}}{1+z^{-1}}$.

**Strategy:** Factor $H_a(s)$ into first- and second-order sections, transform each, then multiply.

### First-order section: $\frac{\Omega_c}{s + \Omega_c}$

$$\frac{\Omega_c}{c\frac{1-z^{-1}}{1+z^{-1}} + \Omega_c} = \frac{\Omega_c(1+z^{-1})}{c(1-z^{-1}) + \Omega_c(1+z^{-1})} = \frac{\Omega_c(1+z^{-1})}{(c+\Omega_c) + (\Omega_c-c)z^{-1}}$$

Dividing by $(c + \Omega_c)$:

$$H_1(z) = \frac{K_1(1+z^{-1})}{1 + r_1\,z^{-1}}$$

where:

$$K_1 = \frac{\Omega_c}{c + \Omega_c} = \frac{66640}{16000 + 66640} = \frac{66640}{82640} = 0.8064$$

$$r_1 = \frac{\Omega_c - c}{c + \Omega_c} = \frac{66640 - 16000}{82640} = \frac{50640}{82640} = 0.6129$$

$$H_1(z) = \frac{0.8064(1 + z^{-1})}{1 + 0.6129\,z^{-1}}$$

### Second-order section: $\frac{\Omega_c^2}{s^2 + \Omega_c s + \Omega_c^2}$

Substitute $s = c\frac{1-z^{-1}}{1+z^{-1}}$, multiply numerator and denominator by $(1+z^{-1})^2$:

$$\text{Numerator: } \Omega_c^2(1+z^{-1})^2 = \Omega_c^2(1 + 2z^{-1} + z^{-2})$$

$$\text{Denominator: } c^2(1-z^{-1})^2 + \Omega_c\,c(1-z^{-2}) + \Omega_c^2(1+z^{-1})^2$$

Expand term by term:

- $c^2(1 - 2z^{-1} + z^{-2})$
- $\Omega_c c(1 - z^{-2})$
- $\Omega_c^2(1 + 2z^{-1} + z^{-2})$

Collect by powers of $z^{-1}$:

**Constant ($z^0$):** $c^2 + \Omega_c c + \Omega_c^2$

**$z^{-1}$:** $-2c^2 + 2\Omega_c^2$

**$z^{-2}$:** $c^2 - \Omega_c c + \Omega_c^2$

With $c = 16{,}000$ and $\Omega_c = 66{,}640$:

$$c^2 = 2.56 \times 10^8, \quad \Omega_c c = 1.0662 \times 10^9, \quad \Omega_c^2 = 4.4409 \times 10^9$$

$$d_0 = c^2 + \Omega_c c + \Omega_c^2 = 0.256 + 1.0662 + 4.4409 = 5.763 \times 10^9$$

$$d_1 = -2c^2 + 2\Omega_c^2 = 2(-0.256 + 4.4409) \times 10^9 = 8.3698 \times 10^9$$

$$d_2 = c^2 - \Omega_c c + \Omega_c^2 = 0.256 - 1.0662 + 4.4409 = 3.631 \times 10^9$$

$$K_2 = \Omega_c^2 / d_0 = 4.441 / 5.763 = 0.7706$$

$$H_2(z) = \frac{0.7706(1 + 2z^{-1} + z^{-2})}{1 + \frac{d_1}{d_0}z^{-1} + \frac{d_2}{d_0}z^{-2}}$$

$$= \frac{0.7706(1 + 2z^{-1} + z^{-2})}{1 + 1.4522\,z^{-1} + 0.6302\,z^{-2}}$$

### Combined $H(z)$

$$H(z) = H_1(z) \cdot H_2(z)$$

$$= \frac{0.8064(1+z^{-1})}{1+0.6129z^{-1}} \cdot \frac{0.7706(1+2z^{-1}+z^{-2})}{1+1.4522z^{-1}+0.6302z^{-2}}$$

$$\boxed{H(z) = \frac{0.6214(1+z^{-1})(1+2z^{-1}+z^{-2})}{(1+0.6129z^{-1})(1+1.4522z^{-1}+0.6302z^{-2})}}$$

Overall numerator gain: $0.8064 \times 0.7706 = 0.6214$.

---

## Part (e): Verification

### Digital Cutoff Verification

At $\omega = \omega_c = 0.85\pi$:

The bilinear transform guarantees that if the analog prototype has its $-3\,\text{dB}$ point at $\Omega_c$ (by construction of the Butterworth), the digital filter will have its $-3\,\text{dB}$ point at exactly $\omega_c = 0.85\pi$.

### DC Gain ($\omega = 0$, $z = 1$)

$$H(e^{j0}) = H(1) = \frac{0.6214(1+1)(1+2+1)}{(1+0.6129)(1+1.4522+0.6302)} = \frac{0.6214 \times 2 \times 4}{1.6129 \times 3.0824}$$

$$= \frac{4.971}{4.971} = 1.0$$

DC gain = 1.0 (0 dB). The Butterworth filter has unity DC gain by design.

### Nyquist Gain ($\omega = \pi$, $z = -1$)

$$H(e^{j\pi}) = H(-1) = \frac{0.6214(1-1)(1-2+1)}{(\cdots)} = \frac{0.6214 \times 0 \times 0}{\cdots} = 0$$

Nyquist gain = 0 ($-\infty\,\text{dB}$). The bilinear transform always places a zero at $z = -1$ ($\omega = \pi$) for each factor $(1 + z^{-1})$ in the numerator. A 3rd-order Butterworth has a 3rd-order zero at $\omega = \pi$ — perfect highpass rejection.

### Pole Verification

Poles of $H(z)$ are the digital images of the analog poles:

$$z_k = \frac{1 + s_k/(2f_s)}{1 - s_k/(2f_s)}$$

For $s_2 = -\Omega_c = -66640$:

$$z_2 = \frac{1 + (-66640/16000)}{1 - (-66640/16000)} = \frac{1 - 4.165}{1 + 4.165} = \frac{-3.165}{5.165} = -0.6129$$

This matches the pole $z = -0.6129$ in $H_1(z)$ above. $|z_2| = 0.6129 < 1$ ✓ stable.

---

## Part (f): Difference Equation and Python Implementation

### Expanding the Transfer Function

Numerator of $H(z)$: $(1+z^{-1})(1+2z^{-1}+z^{-2}) = 1 + 3z^{-1} + 3z^{-2} + z^{-3}$

This is $(1+z^{-1})^3$ — the binomial expansion. So:

$$\text{Numerator: } 0.6214(1 + 3z^{-1} + 3z^{-2} + z^{-3})$$

Denominator: $(1+0.6129z^{-1})(1+1.4522z^{-1}+0.6302z^{-2})$

$= 1 + (0.6129 + 1.4522)z^{-1} + (0.6129 \times 1.4522 + 0.6302)z^{-2} + (0.6129 \times 0.6302)z^{-3}$

$= 1 + 2.0651\,z^{-1} + (0.8904 + 0.6302)z^{-2} + 0.3862\,z^{-3}$

$= 1 + 2.0651\,z^{-1} + 1.5206\,z^{-2} + 0.3862\,z^{-3}$

**Transfer function in direct form:**

$$H(z) = \frac{0.6214 + 1.8642\,z^{-1} + 1.8642\,z^{-2} + 0.6214\,z^{-3}}{1 + 2.0651\,z^{-1} + 1.5206\,z^{-2} + 0.3862\,z^{-3}}$$

**Difference equation:**

$$y[n] = 0.6214\,x[n] + 1.8642\,x[n-1] + 1.8642\,x[n-2] + 0.6214\,x[n-3]$$
$$- 2.0651\,y[n-1] - 1.5206\,y[n-2] - 0.3862\,y[n-3]$$

```python
import numpy as np
from scipy.signal import butter, freqz, sosfilt, tf2sos
import matplotlib.pyplot as plt

# --- Design using SciPy (equivalent result) ---
fs = 8000.0
fc = 3400.0
order = 3

# scipy butter uses normalised frequency (fraction of Nyquist)
Wn = fc / (fs / 2)  # = 3400/4000 = 0.85

# Method 1: Direct b,a coefficients (avoid for high orders)
b, a = butter(order, Wn, btype='low', analog=False)
print("b =", np.round(b, 6))
print("a =", np.round(a, 6))
# b: [0.6214, 1.8642, 1.8642, 0.6214]
# a: [1.0000, 2.0651, 1.5206, 0.3862]

# Method 2: Second-order sections (preferred for numerical stability)
sos = butter(order, Wn, btype='low', output='sos')
print("SOS matrix:")
print(np.round(sos, 6))

# Frequency response
w, H = freqz(b, a, worN=8192, fs=fs)
H_mag_dB = 20 * np.log10(np.abs(H) + 1e-12)

# Verify -3 dB at fc
idx_fc = np.argmin(np.abs(w - fc))
print(f"\nMagnitude at {fc} Hz: {H_mag_dB[idx_fc]:.3f} dB (should be ≈ -3 dB)")

# Filter a test signal
t = np.arange(0, 0.01, 1/fs)  # 10 ms
x = np.cos(2*np.pi*3400*t)    # Tone at cutoff
y_direct = np.array([0.0]*3)  # state for manual implementation
y_out_manual = np.zeros_like(x)
x_buf = np.zeros(4)

for n, xn in enumerate(x):
    x_buf = np.roll(x_buf, 1); x_buf[0] = xn
    yn = (b[0]*x_buf[0] + b[1]*x_buf[1] + b[2]*x_buf[2] + b[3]*x_buf[3]
          - a[1]*y_direct[0] - a[2]*y_direct[1] - a[3]*y_direct[2])
    y_direct = np.roll(y_direct, 1); y_direct[0] = yn
    y_out_manual[n] = yn

# After transient settles, amplitude should be ~0.707 of input
steady_state_amp = np.max(np.abs(y_out_manual[-100:]))
print(f"Steady-state amplitude at 3.4 kHz: {steady_state_amp:.4f} (expected ≈ 0.707)")

# Plot frequency response
plt.figure(figsize=(10, 4))
plt.plot(w/1000, H_mag_dB)
plt.axvline(x=fc/1000, color='r', linestyle='--', label=f'fc = {fc/1000:.1f} kHz')
plt.axhline(y=-3, color='g', linestyle='--', label='-3 dB')
plt.xlabel('Frequency (kHz)'); plt.ylabel('Magnitude (dB)')
plt.title(f'3rd-order Butterworth IIR, fs={fs/1000:.0f} kHz, fc={fc/1000:.1f} kHz')
plt.legend(); plt.grid(True); plt.ylim(-80, 5)
plt.show()
```

**Expected output:**
```
b = [0.621402  1.864205  1.864205  0.621402]
a = [1.       2.065069  1.520598  0.386141]
Magnitude at 3400.0 Hz: -3.000 dB (should be ≈ -3 dB)
Steady-state amplitude at 3.4 kHz: 0.7072 (expected ≈ 0.707)
```

---

## Summary of Design Steps

| Step | Computation | Result |
|---|---|---|
| 1. Digital cutoff | $\omega_c = 2\pi f_c/f_s$ | $0.85\pi$ rad/sample |
| 2. Pre-warp | $\Omega_c = 2f_s\tan(\omega_c/2)$ | $66{,}640$ rad/s |
| 3. Analog poles | $s_k = \Omega_c e^{j\pi(2k+N-1)/(2N)}$ | $-\Omega_c$, $-\frac{\Omega_c}{2}\pm j\frac{\Omega_c\sqrt{3}}{2}$ |
| 4. Bilinear transform | $s \to c\frac{1-z^{-1}}{1+z^{-1}}$ | $H(z)$ in product form |
| 5. Verify DC gain | $H(z=1)$ | 1.0 (0 dB) ✓ |
| 6. Verify cutoff | By construction | $-3$ dB at $0.85\pi$ ✓ |

**Key insight — frequency warping:** The pre-warping step compensates for the inherent nonlinear frequency mapping of the bilinear transform. Without pre-warping, the designed digital filter would have its 3 dB point at the wrong frequency. The pre-warping is what makes the bilinear transform a precise (not approximate) design method for IIR filters.
