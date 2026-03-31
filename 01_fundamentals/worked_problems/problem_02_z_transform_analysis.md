# Worked Problem 02: Z-Transform System Analysis

**Subject:** Digital Signal Processing
**Topic:** Difference Equation, H(z), Poles/Zeros, ROC, Stability, Frequency Response
**Difficulty:** Intermediate to Advanced

---

## Problem Statement

A causal discrete-time LTI system is described by the difference equation:

$$y[n] - y[n-1] + 0.5\,y[n-2] = x[n] + 0.5\,x[n-1]$$

**(a)** Find the system function $H(z)$.

**(b)** Find all poles and zeros. State the ROC for the causal system.

**(c)** Determine whether the system is BIBO stable.

**(d)** Compute the frequency response $H(e^{j\omega})$ and evaluate $|H(e^{j\omega})|$ at $\omega = 0$ (DC) and $\omega = \pi$ (Nyquist).

**(e)** Sketch the pole-zero plot and describe qualitatively how the magnitude response varies with frequency.

**(f)** Find the impulse response $h[n]$ via partial fraction expansion.

---

## Part (a): System Function $H(z)$

Take the z-transform of both sides. Using the time-shift property $\mathcal{Z}\{x[n-k]\} = z^{-k}X(z)$:

$$Y(z) - z^{-1}Y(z) + 0.5\,z^{-2}Y(z) = X(z) + 0.5\,z^{-1}X(z)$$

$$Y(z)\!\left(1 - z^{-1} + 0.5\,z^{-2}\right) = X(z)\!\left(1 + 0.5\,z^{-1}\right)$$

$$\boxed{H(z) = \frac{Y(z)}{X(z)} = \frac{1 + 0.5\,z^{-1}}{1 - z^{-1} + 0.5\,z^{-2}}}$$

Converting to positive powers of $z$ (multiply numerator and denominator by $z^2$):

$$H(z) = \frac{z^2 + 0.5\,z}{z^2 - z + 0.5} = \frac{z(z + 0.5)}{z^2 - z + 0.5}$$

---

## Part (b): Poles, Zeros, and ROC

### Zeros

Set the numerator equal to zero:

$$z(z + 0.5) = 0$$

$$z_1 = 0, \qquad z_2 = -0.5$$

Two zeros: one at the origin (from the $z^2$ factor in the $z^{-1}$ form) and one at $z = -0.5$.

### Poles

Set the denominator equal to zero:

$$z^2 - z + 0.5 = 0$$

Quadratic formula:

$$z = \frac{1 \pm \sqrt{1 - 4 \times 0.5}}{2} = \frac{1 \pm \sqrt{-1}}{2} = \frac{1 \pm j}{2}$$

$$p_1 = \frac{1}{2} + \frac{j}{2} = \frac{1}{\sqrt{2}}\,e^{j\pi/4}, \qquad p_2 = \frac{1}{2} - \frac{j}{2} = \frac{1}{\sqrt{2}}\,e^{-j\pi/4}$$

Pole magnitude: $|p_{1,2}| = \sqrt{(0.5)^2 + (0.5)^2} = \sqrt{0.5} = \frac{1}{\sqrt{2}} \approx 0.707$

Pole angle: $\pm 45°$ $(\pm\pi/4)$, corresponding to digital frequency $\omega_0 = \pi/4$ rad/sample.

### ROC for Causal System

The causal system has a right-sided impulse response. The ROC is the exterior of a circle passing through the outermost pole:

$$\text{ROC}: |z| > \frac{1}{\sqrt{2}} \approx 0.707$$

---

## Part (c): BIBO Stability

**Method 1 — Pole locations:**

All poles satisfy $|p_k| = 1/\sqrt{2} < 1$, so all poles are strictly inside the unit circle.

For a causal system, the ROC $|z| > 1/\sqrt{2}$ includes the unit circle $|z| = 1$.

**Conclusion: The system is BIBO stable.**

**Method 2 — ROC and unit circle:**

The unit circle lies within the ROC $|z| > 0.707$, so the DTFT $H(e^{j\omega})$ converges. This is the frequency-domain statement of BIBO stability.

---

## Part (d): Frequency Response

Substitute $z = e^{j\omega}$:

$$H(e^{j\omega}) = \frac{1 + 0.5\,e^{-j\omega}}{1 - e^{-j\omega} + 0.5\,e^{-2j\omega}}$$

### DC Gain ($\omega = 0$):

$$H(e^{j0}) = \frac{1 + 0.5}{1 - 1 + 0.5} = \frac{1.5}{0.5} = 3.0$$

$|H(e^{j0})| = 3.0$ (9.54 dB)

### Nyquist Gain ($\omega = \pi$):

$$H(e^{j\pi}) = \frac{1 + 0.5 \cdot(-1)}{1 - (-1) + 0.5 \cdot 1} = \frac{0.5}{2.5} = 0.2$$

$|H(e^{j\pi})| = 0.2$ ($-14.0$ dB)

### At the pole frequency ($\omega = \pi/4$):

The poles are at angle $\omega_0 = \pi/4$. We expect a magnitude peak near this frequency.

$$H(e^{j\pi/4}) = \frac{1 + 0.5\,e^{-j\pi/4}}{1 - e^{-j\pi/4} + 0.5\,e^{-j\pi/2}}$$

Numerically:

- $e^{-j\pi/4} = (1-j)/\sqrt{2} \approx 0.707 - 0.707j$
- Numerator: $1 + 0.5(0.707 - 0.707j) = 1.354 - 0.354j$, magnitude $\approx 1.400$
- $e^{-j\pi/2} = -j$
- Denominator: $1 - (0.707-0.707j) + 0.5(-j) = 0.293 + 0.707j - 0.5j = 0.293 + 0.207j$, magnitude $\approx 0.359$

$$|H(e^{j\pi/4})| \approx \frac{1.400}{0.359} \approx 3.90$$

The magnitude response peaks near $\omega = \pi/4$ due to the nearby poles.

---

## Part (e): Pole-Zero Plot and Qualitative Response

### Pole-Zero Plot

```
Im(z)
  1 |
    |                p1 (+)
0.5 |             +
    |           /
    |          /
    |         /  poles at r = 1/√2, ±45°
    |          \
-0.5|           +
    |              p2 (×)
 -1 |    z2(o)
    |____|____|____|____|_____ Re(z)
       -1  -0.5  0  0.5  1

Zeros: o at z=0 (origin), o at z=-0.5
Poles: × at z=0.5±0.5j
Unit circle: dashed
```

More precisely:

```
       Im(z)
  1.0  |                         (unit circle)
       |                    /
  0.7  |               p1 +
       |                  /
  0.5  |                 /
       |                /
       |               /
  0.0  |z2(o)-----(o)------------- Re(z)
      -0.5   0   0.5  1.0
       |                \
 -0.5  |                 \
       |               p2 +
 -0.7  |
```

### Qualitative Magnitude Response

Moving around the unit circle from $\omega = 0$ to $\omega = \pi$:

- **$\omega = 0$ (DC):** Distance from evaluation point $(1,0)$ to poles $(0.5\pm 0.5j)$ is moderate. Zero at $(-0.5, 0)$ is far. Gain = 3.0.
- **$\omega = \pi/4$:** Closest approach to the poles. Distance to each pole minimised. Gain peaks at ~3.9.
- **$\omega = \pi/2$:** Moving away from poles. Gain decreasing.
- **$\omega = \pi$ (Nyquist):** Close to the zero at $z = -0.5$ (on the real axis). Small denominator distance (poles are far), zero is close. Gain = 0.2.

The filter has a **lowpass-like character** with a resonance peak near $\omega = \pi/4$ (corresponding to $f = f_s/8$).

---

## Part (f): Impulse Response via Partial Fractions

Starting from $H(z)$ in $z^{-1}$ form:

$$H(z) = \frac{1 + 0.5\,z^{-1}}{1 - z^{-1} + 0.5\,z^{-2}} = \frac{1 + 0.5\,z^{-1}}{(1 - p_1 z^{-1})(1 - p_2 z^{-1})}$$

where $p_1 = (1+j)/2$ and $p_2 = (1-j)/2 = p_1^*$.

### Partial Fraction Expansion

$$H(z) = \frac{A}{1 - p_1 z^{-1}} + \frac{A^*}{1 - p_2 z^{-1}}$$

(Coefficients are conjugates since poles and numerator are conjugate symmetric with real input $z^{-1}$ coefficients.)

Find $A$ by the cover-up method:

$$A = (1 - p_1 z^{-1})\,H(z)\big|_{z = p_1} = \frac{1 + 0.5/p_1}{1 - p_2/p_1}$$

Compute each piece:

$$\frac{1}{p_1} = \frac{2}{1+j} = \frac{2(1-j)}{2} = 1 - j$$

$$1 + \frac{0.5}{p_1} = 1 + 0.5(1-j) = 1.5 - 0.5j$$

$$\frac{p_2}{p_1} = \frac{(1-j)/2}{(1+j)/2} = \frac{1-j}{1+j} = \frac{(1-j)^2}{2} = \frac{-2j}{2} = -j$$

$$1 - \frac{p_2}{p_1} = 1 - (-j) = 1 + j$$

$$A = \frac{1.5 - 0.5j}{1+j} = \frac{(1.5-0.5j)(1-j)}{(1+j)(1-j)} = \frac{1.5 - 1.5j - 0.5j + 0.5j^2}{2} = \frac{1.5 - 2j - 0.5}{2} = \frac{1 - 2j}{2} = 0.5 - j$$

So $A = 0.5 - j$ and $A^* = 0.5 + j$.

### Inverse Z-Transform (causal)

$$h[n] = A\,p_1^n\,u[n] + A^*\,p_2^n\,u[n]$$

Since $p_1 = p_2^*$ and $A = A^{*\prime}$, this is a real sequence. Writing $p_1 = \frac{1}{\sqrt{2}}\,e^{j\pi/4}$:

$$h[n] = 2\,\text{Re}\!\left\{A\,p_1^n\right\}u[n] = 2\,\text{Re}\!\left\{(0.5-j)\left(\frac{1}{\sqrt{2}}\right)^n e^{j\pi n/4}\right\}u[n]$$

Converting $A = 0.5 - j$ to polar: $|A| = \sqrt{0.25+1} = \sqrt{1.25}$, $\angle A = \arctan(-1/0.5) = \arctan(-2) \approx -63.43° = -0.3524\pi$.

$$\boxed{h[n] = 2\sqrt{1.25}\left(\frac{1}{\sqrt{2}}\right)^n \cos\!\left(\frac{\pi n}{4} - 0.3524\pi\right)u[n]}$$

Or numerically: $2\sqrt{1.25} \approx 2.236$, $1/\sqrt{2} \approx 0.7071$.

### Numerical Verification

Check $h[0]$: $h[0] = 2.236 \cdot 0.7071^0 \cdot \cos(-0.3524\pi) = 2.236\cos(-63.43°) = 2.236 \times 0.4472 \approx 1.0$ ✓

From the initial value theorem: $h[0] = \lim_{z\to\infty}H(z) = \frac{1+0}{1-0+0} = 1$ ✓

Check $h[1]$: From the difference equation with $x[n] = \delta[n]$:

$h[1] = h[0] - 0.5\cdot h[-1] + 0.5\delta[0] = 1 + 0.5 = 1.5$

Wait — re-reading the equation: $y[n] = y[n-1] - 0.5y[n-2] + x[n] + 0.5x[n-1]$.

$h[1] = h[0] - 0.5h[-1] + \delta[1] + 0.5\delta[0] = 1 - 0 + 0 + 0.5 = 1.5$

From the formula: $h[1] = 2.236 \times 0.7071 \times \cos(\pi/4 - 0.3524\pi) = 2.236 \times 0.7071 \times \cos(-0.1024\pi) \approx 1.581 \times 0.9511 \approx 1.503 \approx 1.5$ ✓

---

## Summary of Results

| Quantity | Value |
|---|---|
| Zeros | $z = 0$, $z = -0.5$ |
| Poles | $z = 0.5 \pm 0.5j = \frac{1}{\sqrt{2}}e^{\pm j\pi/4}$ |
| Pole magnitude | $1/\sqrt{2} \approx 0.707$ |
| ROC (causal) | $\|z\| > 1/\sqrt{2}$ |
| BIBO stable | Yes (all poles inside unit circle) |
| DC gain $\|H(e^{j0})\|$ | 3.0 (9.54 dB) |
| Nyquist gain $\|H(e^{j\pi})\|$ | 0.2 ($-14$ dB) |
| Peak gain near | $\omega = \pi/4$ ($\approx 3.9$) |
| Filter character | Lowpass with resonance at $f_s/8$ |
