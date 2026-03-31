# Z-Transform — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Z-Transform, ROC, Poles and Zeros, Inverse Z-Transform, Stability, Frequency Response
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Define the (bilateral) z-transform and explain its relationship to the DTFT.

**Answer:**

The **bilateral z-transform** of a discrete-time sequence $x[n]$ is:

$$X(z) = \mathcal{Z}\{x[n]\} = \sum_{n=-\infty}^{\infty} x[n]\,z^{-n}, \qquad z \in \mathbb{C}$$

The **Region of Convergence (ROC)** is the set of complex values $z$ for which this sum converges absolutely:

$$\text{ROC} = \left\{z \in \mathbb{C} : \sum_{n=-\infty}^{\infty} |x[n]|\,|z|^{-n} < \infty\right\}$$

**Relationship to the DTFT:**

Substitute $z = e^{j\omega}$ (i.e., $|z| = 1$, the unit circle):

$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n]\,e^{-j\omega n}$$

This is exactly the **DTFT**. The DTFT exists (the sum converges) if and only if the unit circle lies within the ROC of $X(z)$.

**Intuition for the variable $z$:**

Writing $z = r\,e^{j\omega}$:

$$X(z) = \sum_{n=-\infty}^{\infty} x[n]\,(r^{-1}e^{j\omega})^n = \text{DTFT of } \{x[n]\cdot r^{-n}\}$$

The z-transform generalises the DTFT by adding an exponential window $r^{-n}$ that can improve convergence. This is analogous to how the Laplace transform generalises the Fourier transform in continuous time.

---

### Q2. State the ROC properties for common signal types.

**Answer:**

The ROC depends on the support and growth rate of $x[n]$. It always consists of an annular region in the z-plane.

**Right-sided (causal) sequences** $x[n] = 0$ for $n < N_1$:

- ROC is the exterior of a circle: $|z| > r_{max}$
- Example: $a^n u[n]$ has ROC $|z| > |a|$

**Left-sided (anti-causal) sequences** $x[n] = 0$ for $n > N_2$:

- ROC is the interior of a circle: $|z| < r_{min}$
- Example: $-a^n u[-n-1]$ has ROC $|z| < |a|$

**Two-sided sequences:**

- ROC is an annular ring: $r_1 < |z| < r_2$
- Can be empty if the inner radius exceeds the outer radius

**Finite-duration sequences (FIR):**

- ROC is the entire z-plane except possibly $z = 0$ and/or $z = \infty$
- A causal FIR has ROC: all $z$ except $z = 0$ (the $z^{-n}$ terms can blow up there)

**Key properties:**
1. The ROC is an open, connected annular region (no poles inside it)
2. The ROC never contains poles of $X(z)$
3. If $x[n]$ is absolutely summable (BIBO stable), the unit circle is in the ROC
4. For a causal rational $X(z)$, the ROC is $|z| > |$ outermost pole $|$

---

### Q3. Give the z-transform pairs for the most common sequences, including the ROC.

**Answer:**

| Sequence $x[n]$ | Z-transform $X(z)$ | ROC |
|---|---|---|
| $\delta[n]$ | $1$ | All $z$ |
| $\delta[n - k]$, $k > 0$ | $z^{-k}$ | $z \neq 0$ |
| $u[n]$ | $\dfrac{1}{1-z^{-1}} = \dfrac{z}{z-1}$ | $\|z\| > 1$ |
| $a^n u[n]$ | $\dfrac{1}{1-az^{-1}} = \dfrac{z}{z-a}$ | $\|z\| > \|a\|$ |
| $-a^n u[-n-1]$ | $\dfrac{1}{1-az^{-1}}$ | $\|z\| < \|a\|$ |
| $n\,a^n u[n]$ | $\dfrac{az^{-1}}{(1-az^{-1})^2}$ | $\|z\| > \|a\|$ |
| $\cos(\omega_0 n)\,u[n]$ | $\dfrac{1 - \cos\omega_0\cdot z^{-1}}{1 - 2\cos\omega_0\cdot z^{-1} + z^{-2}}$ | $\|z\| > 1$ |
| $r^n\cos(\omega_0 n)\,u[n]$ | $\dfrac{1 - r\cos\omega_0\cdot z^{-1}}{1 - 2r\cos\omega_0\cdot z^{-1} + r^2 z^{-2}}$ | $\|z\| > r$ |

**Important note:** The z-transform expression for $a^n u[n]$ and $-a^n u[-n-1]$ are **identical** — $\frac{1}{1-az^{-1}}$ — but they correspond to **different sequences** with **different ROCs**. The ROC is an essential part of the z-transform specification and cannot be omitted.

---

### Q4. What are the poles and zeros of a rational z-transform? How do you find them?

**Answer:**

A rational z-transform has the form:

$$X(z) = \frac{B(z)}{A(z)} = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}$$

Converting to positive powers of $z$ by multiplying numerator and denominator by $z^{\max(M,N)}$:

$$X(z) = \frac{z^{N-M}\,(b_0 z^M + b_1 z^{M-1} + \cdots + b_M)}{z^N + a_1 z^{N-1} + \cdots + a_N}$$

**Zeros:** Values of $z$ where $X(z) = 0$ (roots of the numerator polynomial, plus any $z=0$ zeros from the $z^{N-M}$ factor when $N > M$).

**Poles:** Values of $z$ where $X(z) \to \infty$ (roots of the denominator polynomial, plus $z = \infty$ poles when $M > N$).

**Key facts:**
- The number of poles equals the number of zeros for a proper rational function (counting $z=0$ and $z=\infty$)
- Poles and zeros of real-coefficient systems always appear in complex conjugate pairs
- Poles determine the ROC: the ROC never contains poles
- The gain $b_0$ scales the overall response but does not affect pole/zero locations

---

## Intermediate

### Q5. Derive the z-transform of $x[n] = a^n u[n]$ and verify the ROC.

**Answer:**

By definition:

$$X(z) = \sum_{n=-\infty}^{\infty} a^n u[n]\, z^{-n} = \sum_{n=0}^{\infty} a^n z^{-n} = \sum_{n=0}^{\infty} (az^{-1})^n$$

This is a geometric series with ratio $r = az^{-1}$. It converges when $|az^{-1}| < 1$, i.e., $|z| > |a|$.

Within the ROC:

$$X(z) = \frac{1}{1 - az^{-1}} = \frac{z}{z - a}, \qquad |z| > |a|$$

**Pole at $z = a$:** The series diverges when $|z| = |a|$ (geometric series at the boundary). The pole is at $z = a$ and is excluded from the ROC.

**Verification at $z = 2$, $a = 0.5$:**

$$X(2) = \frac{1}{1 - 0.5/2} = \frac{1}{0.75} = \frac{4}{3}$$

Direct sum: $\sum_{n=0}^{\infty}(0.5)^n \cdot 2^{-n} = \sum_{n=0}^{\infty}(0.25)^n = \frac{1}{1-0.25} = \frac{4}{3}$ ✓

---

### Q6. Find the inverse z-transform of $X(z) = \frac{1}{(1-0.5z^{-1})(1+0.25z^{-1})}$ for each possible ROC.

**Answer:**

Poles at $z = 0.5$ and $z = -0.25$. There are three possible ROCs:

1. $|z| > 0.5$ (causal / right-sided)
2. $|z| < 0.25$ (anti-causal / left-sided)
3. $0.25 < |z| < 0.5$ (two-sided, non-causal)

**Partial fraction expansion:**

$$X(z) = \frac{A}{1 - 0.5z^{-1}} + \frac{B}{1 + 0.25z^{-1}}$$

$$1 = A(1 + 0.25z^{-1}) + B(1 - 0.5z^{-1})$$

At $z = 0.5$ ($z^{-1} = 2$): $1 = A(1 + 0.5) \Rightarrow A = 2/3$

At $z = -0.25$ ($z^{-1} = -4$): $1 = B(1 + 2) \Rightarrow B = 1/3$

$$X(z) = \frac{2/3}{1 - 0.5z^{-1}} + \frac{1/3}{1 + 0.25z^{-1}}$$

**ROC 1: $|z| > 0.5$ — causal:**

Both terms are right-sided:

$$x[n] = \tfrac{2}{3}(0.5)^n u[n] + \tfrac{1}{3}(-0.25)^n u[n]$$

**ROC 2: $|z| < 0.25$ — anti-causal:**

Both terms are left-sided:

$$x[n] = -\tfrac{2}{3}(0.5)^n u[-n-1] - \tfrac{1}{3}(-0.25)^n u[-n-1]$$

**ROC 3: $0.25 < |z| < 0.5$ — two-sided:**

The $z=0.5$ pole is outside the ROC (left-sided contribution), the $z=-0.25$ pole is inside (right-sided):

$$x[n] = -\tfrac{2}{3}(0.5)^n u[-n-1] + \tfrac{1}{3}(-0.25)^n u[n]$$

This demonstrates why specifying the ROC is mandatory — the same algebraic expression $X(z)$ represents three completely different time-domain signals.

---

### Q7. Given a difference equation, derive $H(z)$, then compute the frequency response $H(e^{j\omega})$.

**System:** $y[n] = x[n] + 0.8\,x[n-1] - 0.64\,y[n-2]$

**Answer:**

**Step 1 — Z-transform both sides:**

$$Y(z) = X(z) + 0.8\,z^{-1}X(z) - 0.64\,z^{-2}Y(z)$$

$$Y(z)\left(1 + 0.64\,z^{-2}\right) = X(z)\left(1 + 0.8\,z^{-1}\right)$$

**Step 2 — System function:**

$$H(z) = \frac{1 + 0.8\,z^{-1}}{1 + 0.64\,z^{-2}}$$

**Poles:** $z^2 + 0.64 = 0 \Rightarrow z = \pm j0.8$. Both have $|z| = 0.8 < 1$ — stable.

**Zeros:** $z = -0.8$ (real axis).

**Step 3 — Frequency response:** Substitute $z = e^{j\omega}$:

$$H(e^{j\omega}) = \frac{1 + 0.8\,e^{-j\omega}}{1 + 0.64\,e^{-2j\omega}}$$

**DC gain** ($\omega = 0$):

$$H(e^{j0}) = \frac{1 + 0.8}{1 + 0.64} = \frac{1.8}{1.64} \approx 1.098$$

**Nyquist gain** ($\omega = \pi$):

$$H(e^{j\pi}) = \frac{1 - 0.8}{1 + 0.64} = \frac{0.2}{1.64} \approx 0.122$$

The filter attenuates high frequencies much more than low frequencies — it acts as a lowpass filter.

---

### Q8. State and apply the z-transform properties: time-shifting, z-domain differentiation, and convolution.

**Answer:**

**Property 1 — Time shifting:**

$$\mathcal{Z}\{x[n-k]\} = z^{-k} X(z)$$

A delay of $k$ samples multiplies $X(z)$ by $z^{-k}$. This is why the unit delay element is labelled $z^{-1}$ in block diagrams, and why the z-transform is so natural for analysing difference equations.

**Property 2 — Z-domain differentiation:**

$$\mathcal{Z}\{n\,x[n]\} = -z\,\frac{d}{dz}X(z)$$

Application: z-transform of $n\,a^n u[n]$:

$$\mathcal{Z}\{a^n u[n]\} = \frac{1}{1-az^{-1}} \implies \mathcal{Z}\{n\,a^n u[n]\} = -z\,\frac{d}{dz}\left(\frac{1}{1-az^{-1}}\right) = \frac{az^{-1}}{(1-az^{-1})^2}$$

**Property 3 — Convolution:**

$$\mathcal{Z}\{(x * h)[n]\} = X(z)\,H(z)$$

The ROC of $X(z)H(z)$ contains the intersection of the individual ROCs (possibly larger if there are pole-zero cancellations).

This is the fundamental property that makes the z-transform useful for LTI system analysis: convolution in the time domain becomes multiplication in the z-domain. A cascade of two LTI systems with system functions $H_1(z)$ and $H_2(z)$ has combined system function $H_1(z)\,H_2(z)$.

---

## Advanced

### Q9. Explain how the ROC determines stability and causality for a rational $H(z)$. Illustrate with a system that has poles at $z = 0.5$ and $z = 2$.

**Answer:**

**System:** Poles at $z_1 = 0.5$ and $z_2 = 2$. Three possible ROCs:

$$H(z) = \frac{1}{(1-0.5z^{-1})(1-2z^{-1})}$$

After partial fractions: $H(z) = \frac{-1/1.5}{1-0.5z^{-1}} + \frac{1/1.5}{1-2z^{-1}}$ (working out constants is straightforward).

**ROC 1: $|z| > 2$ — causal:**

Both poles contribute right-sided terms. The unit circle ($|z|=1$) is **not** in the ROC. **BIBO unstable** (the $2^n u[n]$ term grows without bound).

**ROC 2: $0.5 < |z| < 2$ — two-sided (non-causal, non-anti-causal):**

Pole at $z=0.5$ contributes a right-sided term; pole at $z=2$ contributes a left-sided term. Unit circle is in the ROC. **BIBO stable** but **non-causal** (the $2^n u[-n-1]$ component depends on future inputs).

**ROC 3: $|z| < 0.5$ — anti-causal:**

Both poles contribute left-sided terms. Unit circle not in ROC. **BIBO unstable.**

**General rules:**

| ROC | Causality | Stability (BIBO) |
|---|---|---|
| $\|z\| > r_{max}$ | Causal (right-sided) | Stable iff all poles inside unit circle |
| $\|z\| < r_{min}$ | Anti-causal (left-sided) | Stable iff all poles outside unit circle |
| Annular ring | Two-sided (non-causal) | Stable iff unit circle in ROC |

For a **real-time implementable stable system** we need it to be both causal and stable, which requires all poles inside the unit circle with ROC $|z| > r_{max}$ and $r_{max} < 1$.

---

### Q10. Describe the geometric interpretation of the frequency response from the pole-zero plot.

**Answer:**

The frequency response is evaluated by moving around the unit circle:

$$H(e^{j\omega}) = H(z)\big|_{z = e^{j\omega}} = b_0\,\frac{\prod_k (e^{j\omega} - z_k)}{\prod_m (e^{j\omega} - p_m)}$$

**Geometric interpretation:**

Each zero $z_k$ contributes a **vector** from $z_k$ to the evaluation point $e^{j\omega}$ on the unit circle:

- Vector magnitude: $|e^{j\omega} - z_k|$ (distance from zero to current frequency point)
- Vector angle: contributes to the phase

Similarly for each pole $p_m$: vector from $p_m$ to $e^{j\omega}$.

$$|H(e^{j\omega})| = |b_0|\,\frac{\prod_k |e^{j\omega} - z_k|}{\prod_m |e^{j\omega} - p_m|}$$

$$\angle H(e^{j\omega}) = \angle b_0 + \sum_k \angle(e^{j\omega} - z_k) - \sum_m \angle(e^{j\omega} - p_m)$$

**Design intuition:**

- **Pole close to unit circle at angle $\omega_0$:** The denominator term $|e^{j\omega} - p_m|$ becomes very small near $\omega = \omega_0$, creating a **peak** (resonance) in $|H|$.
- **Zero on the unit circle at angle $\omega_z$:** The numerator term $|e^{j\omega} - z_k|$ equals zero at $\omega = \omega_z$, creating a **notch** (exact null) in $|H|$.
- **Poles far from unit circle:** Flat, broad response contribution.

This geometric picture is extremely useful for quick filter design: place poles near frequencies you want to boost, zeros near frequencies you want to suppress.

**Example — Notch filter at $\omega = \pi/3$:** Place zeros at $z = e^{\pm j\pi/3}$ exactly on the unit circle, with poles at $z = r\,e^{\pm j\pi/3}$, $r < 1$. The zeros create a perfect null; the poles (slightly inside) keep the filter approximately flat elsewhere.

---

### Q11. Prove the initial value theorem and use it as a check in a partial-fraction inversion.

**Answer:**

**Initial Value Theorem:** For a causal sequence ($x[n] = 0$, $n < 0$):

$$x[0] = \lim_{z \to \infty} X(z)$$

**Proof:**

$$X(z) = \sum_{n=0}^{\infty} x[n]\,z^{-n} = x[0] + x[1]z^{-1} + x[2]z^{-2} + \cdots$$

As $z \to \infty$, all terms $z^{-n}$ for $n \geq 1$ vanish, leaving $\lim_{z\to\infty} X(z) = x[0]$.

**Application:** Verify the partial-fraction result from Q11 in the signals_and_systems file:

$$H(z) = \frac{1}{1 - \frac{3}{4}z^{-1} + \frac{1}{8}z^{-2}}$$

Initial value theorem: $h[0] = \lim_{z\to\infty} H(z) = \frac{1}{1 - 0 + 0} = 1$.

From the partial fraction result: $h[0] = 2(0.5)^0 - (0.25)^0 = 2 - 1 = 1$ ✓

**Final value theorem** (for stable causal systems — no poles on or outside unit circle except possibly at $z=1$):

$$\lim_{n\to\infty} x[n] = \lim_{z\to 1}(1-z^{-1})X(z)$$

For $H(z)$ above: $\lim_{z\to 1}(1-z^{-1})\frac{1}{1-\frac{3}{4}z^{-1}+\frac{1}{8}z^{-2}}$. As $z\to 1$: numerator $\to 0$, denominator $\to 1 - 0.75 + 0.125 = 0.375$. Applying L'Hopital or factoring: final value $= \frac{1-1}{(1-\frac{1}{2})(1-\frac{1}{4})} \cdot \ldots$ — more easily, $h[n] = 2(0.5)^n - (0.25)^n \to 0$ as $n\to\infty$ since both bases are $< 1$. ✓

---

## Quick Reference

| Transform pair | $X(z)$ | ROC |
|---|---|---|
| $\delta[n]$ | $1$ | All $z$ |
| $u[n]$ | $\frac{z}{z-1}$ | $\|z\|>1$ |
| $a^n u[n]$ | $\frac{z}{z-a}$ | $\|z\|>\|a\|$ |
| $-a^n u[-n-1]$ | $\frac{z}{z-a}$ | $\|z\|<\|a\|$ |

| Property | Z-domain |
|---|---|
| Time shift by $k$ | $z^{-k} X(z)$ |
| Convolution | $X(z)\,H(z)$ |
| Multiplication by $n$ | $-z\,\frac{d}{dz}X(z)$ |
| BIBO stable (causal) | All poles inside unit circle |
