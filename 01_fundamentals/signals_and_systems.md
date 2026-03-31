# Signals and Systems — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Discrete-Time Signals, LTI Systems, Causality, Stability, Impulse Response
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Define the unit impulse sequence and the unit step sequence. How are they related?

**Answer:**

The **unit impulse** (Kronecker delta) is defined as:

$$\delta[n] = \begin{cases} 1 & n = 0 \\ 0 & n \neq 0 \end{cases}$$

The **unit step** is defined as:

$$u[n] = \begin{cases} 1 & n \geq 0 \\ 0 & n < 0 \end{cases}$$

**Relationship — differentiation and accumulation:**

$$u[n] = \sum_{k=-\infty}^{n} \delta[k] \qquad \text{(step is the running sum of the impulse)}$$

$$\delta[n] = u[n] - u[n-1] \qquad \text{(impulse is the first backward difference of the step)}$$

**Why this matters:** The impulse is the fundamental building block. Any discrete-time signal can be expressed as a weighted sum of shifted impulses (the sifting property):

$$x[n] = \sum_{k=-\infty}^{\infty} x[k]\,\delta[n - k]$$

This representation is the foundation of convolution and LTI system analysis.

**Common mistake:** Confusing the Kronecker delta $\delta[n]$ (discrete, dimensionless, unit value at $n=0$) with the Dirac delta $\delta(t)$ (continuous, infinite amplitude, unit area). In DSP we always mean the Kronecker delta unless explicitly stated otherwise.

---

### Q2. What is a discrete-time exponential signal? What conditions make it real, complex, growing, or decaying?

**Answer:**

The general discrete-time exponential is:

$$x[n] = A \cdot z_0^{\,n}, \quad A,\, z_0 \in \mathbb{C}$$

Writing $z_0 = r\,e^{j\omega_0}$ in polar form:

$$x[n] = A \cdot r^n e^{j\omega_0 n}$$

| Condition | Behaviour |
|---|---|
| $r = 1$, $\omega_0 = 0$ | Constant (DC) |
| $r < 1$, $\omega_0 = 0$ | Decaying real exponential |
| $r > 1$, $\omega_0 = 0$ | Growing real exponential |
| $r = 1$, $\omega_0 \neq 0$ | Pure complex sinusoid, constant amplitude |
| $r < 1$, $\omega_0 \neq 0$ | Decaying sinusoidal oscillation |
| $r > 1$, $\omega_0 \neq 0$ | Growing sinusoidal oscillation |

For a **real exponential** with $z_0 = a \in \mathbb{R}$: $x[n] = A\,a^n$. The sign of $a$ determines whether the sequence alternates (negative $a$), and the magnitude determines growth vs decay.

**Connection to z-transform:** The ROC condition $|z| > r$ for causal exponentials directly reflects the convergence boundary determined by the pole magnitude $r$.

---

### Q3. State the defining properties of a Linear Time-Invariant (LTI) system. Why are LTI systems central to DSP?

**Answer:**

**Linearity** requires two sub-properties:

1. **Homogeneity:** $x[n] \to y[n]$ implies $\alpha\,x[n] \to \alpha\,y[n]$
2. **Additivity:** $x_1[n] \to y_1[n]$ and $x_2[n] \to y_2[n]$ implies $x_1[n]+x_2[n] \to y_1[n]+y_2[n]$

Combined superposition: $\alpha\,x_1[n] + \beta\,x_2[n] \to \alpha\,y_1[n] + \beta\,y_2[n]$

**Time-invariance:** If $x[n] \to y[n]$, then $x[n-n_0] \to y[n-n_0]$ for all integers $n_0$. The system's characteristics do not change over time.

**Why LTI systems are central:**

1. An LTI system is **completely characterised** by its impulse response $h[n]$. Once you know $h[n]$, the output for any input is given by convolution: $y[n] = x[n] * h[n]$.
2. Complex exponentials $e^{j\omega n}$ are **eigenfunctions** of LTI systems — they pass through modified only in amplitude and phase. This makes frequency-domain analysis (DTFT, z-transform) exact and powerful.
3. **Superposition** allows decomposing complex inputs into simple components, analysing each, then recombining.
4. Most practical filters and processing algorithms are designed as LTI systems.

**Common mistake:** A system with non-zero initial conditions is only LTI when those initial conditions are zero. A system depending on the current time index $n$ (e.g., $y[n] = n\,x[n]$) is linear but not time-invariant.

---

### Q4. What is BIBO stability? State and prove the necessary and sufficient condition.

**Answer:**

**BIBO (Bounded-Input Bounded-Output) stability:** A system is BIBO stable if every bounded input produces a bounded output:

$$|x[n]| \leq M_x < \infty\ \forall\,n \implies |y[n]| \leq M_y < \infty\ \forall\,n$$

**Theorem:** An LTI system is BIBO stable if and only if:

$$\sum_{n=-\infty}^{\infty} |h[n]| < \infty \qquad \text{(absolute summability)}$$

**Proof of sufficiency:** Let $|x[n]| \leq M_x$ for all $n$. Then:

$$|y[n]| = \left|\sum_{k=-\infty}^{\infty} h[k]\,x[n-k]\right| \leq \sum_{k=-\infty}^{\infty} |h[k]|\,|x[n-k]| \leq M_x \sum_{k=-\infty}^{\infty} |h[k]| = M_x \cdot C < \infty$$

**Proof of necessity (contrapositive):** Suppose $\sum|h[k]| = \infty$. Choose $x[n] = \text{sgn}(h[-n])$ (a bounded input with $|x[n]| = 1$). Then:

$$y[0] = \sum_{k=-\infty}^{\infty} h[k]\,x[-k] = \sum_{k=-\infty}^{\infty} h[k]\,\text{sgn}(h[k]) = \sum_{k=-\infty}^{\infty} |h[k]| = \infty$$

So the output is unbounded at $n = 0$.

**Examples:**
- $h[n] = a^n u[n]$, $|a|<1$: $\sum_{n=0}^{\infty}|a|^n = \frac{1}{1-|a|} < \infty$ — stable
- $h[n] = u[n]$ (ideal accumulator): $\sum_{n=0}^{\infty} 1$ diverges — not stable
- All FIR filters are always BIBO stable (finite sum of finite-magnitude coefficients)

---

### Q5. Define causality for a discrete-time LTI system.

**Answer:**

A system is **causal** if the output at any time $n$ depends only on the current and past inputs — never on future inputs.

For an LTI system with impulse response $h[n]$:

$$y[n] = \sum_{k=-\infty}^{\infty} h[k]\,x[n-k]$$

The term $h[k]\,x[n-k]$ uses input sample $x[n-k]$. For $k < 0$, the index $n - k > n$, which is a future input. Therefore a causal LTI system requires:

$$h[n] = 0 \quad \text{for all } n < 0$$

**Intuition:** A causal impulse response has no "pre-ringing" — it only responds after the impulse arrives, not before.

**Non-causal systems** can be implemented in offline (batch) processing where the entire signal is available — for example, forward-backward zero-phase IIR filtering using `filtfilt` in MATLAB. They cannot run in real-time.

---

## Intermediate

### Q6. Verify whether each system is linear, time-invariant, causal, and BIBO stable.

**System A:** $y[n] = x[n] - x[n-1]$

**System B:** $y[n] = n \cdot x[n]$

**System C:** $y[n] = x[n^2]$

**Answer:**

**System A: First-difference**

- **Linearity:** $\mathcal{T}\{\alpha x_1 + \beta x_2\}[n] = \alpha(x_1[n]-x_1[n-1]) + \beta(x_2[n]-x_2[n-1]) = \alpha y_1[n] + \beta y_2[n]$. **Linear.**
- **Time-invariance:** $\mathcal{T}\{x[n-n_0]\} = x[n-n_0] - x[n-1-n_0] = y[n-n_0]$. **Time-invariant.** This system is LTI with $h[n] = \delta[n] - \delta[n-1]$.
- **Causality:** Output depends on $x[n]$ (current) and $x[n-1]$ (past). **Causal.**
- **BIBO:** $\sum|h[n]| = 1 + 1 = 2 < \infty$. **Stable.**

**System B: Time-varying gain**

- **Linearity:** $\mathcal{T}\{\alpha x_1 + \beta x_2\} = n(\alpha x_1[n] + \beta x_2[n]) = \alpha y_1[n] + \beta y_2[n]$. **Linear.**
- **Time-invariance:** $\mathcal{T}\{x[n-n_0]\} = n\,x[n-n_0]$, but $y[n-n_0] = (n-n_0)x[n-n_0]$. These differ for $n_0 \neq 0$. **Not time-invariant.**
- **Causality:** Output at $n$ depends only on $x[n]$. **Causal.**
- **BIBO:** Take $x[n] = u[n]$ (bounded). Then $y[n] = n\,u[n]$, which grows without bound. **Not stable.**

**System C: Time-warping**

- **Linearity:** $\mathcal{T}\{\alpha x_1 + \beta x_2\}[n] = \alpha x_1[n^2] + \beta x_2[n^2] = \alpha y_1[n] + \beta y_2[n]$. **Linear.**
- **Time-invariance:** $\mathcal{T}\{x[n-n_0]\}= x[n^2 - n_0]$, but $y[n-n_0] = x[(n-n_0)^2]$. These differ. **Not time-invariant.**
- **Causality:** At $n = -3$, output is $x[9]$ — a future sample. **Not causal.**
- **BIBO:** $|x[n^2]| \leq M_x$ whenever $|x[\cdot]| \leq M_x$. **Stable.**

---

### Q7. Derive the convolution sum from first principles.

**Answer:**

**Step 1 — Sifting representation of the input:**

Any discrete-time signal can be written as:

$$x[n] = \sum_{k=-\infty}^{\infty} x[k]\,\delta[n-k]$$

This is an exact identity; it holds for any $x[n]$.

**Step 2 — Apply the system operator:**

$$y[n] = \mathcal{T}\left\{\sum_{k=-\infty}^{\infty} x[k]\,\delta[n-k]\right\}$$

**Step 3 — Apply linearity** (pull constants and the sum through $\mathcal{T}$):

$$y[n] = \sum_{k=-\infty}^{\infty} x[k]\,\mathcal{T}\{\delta[n-k]\}$$

**Step 4 — Define the impulse response and apply time-invariance:**

Let $h[n] \triangleq \mathcal{T}\{\delta[n]\}$. By time-invariance, shifting the input shifts the output by the same amount:

$$\mathcal{T}\{\delta[n-k]\} = h[n-k]$$

**Step 5 — Convolution sum:**

$$\boxed{y[n] = \sum_{k=-\infty}^{\infty} x[k]\,h[n-k] \;=\; (x * h)[n]}$$

**Key insight:** Linearity allows the decomposition into scaled impulses; time-invariance ensures each delayed impulse produces the same $h[n]$, merely shifted. Together they reduce all LTI analysis to a single convolution.

---

### Q8. Given $h[n] = (0.5)^n u[n]$ and $x[n] = u[n]$, find $y[n] = x[n] * h[n]$ in closed form.

**Answer:**

$$y[n] = \sum_{k=-\infty}^{\infty} h[k]\,x[n-k] = \sum_{k=0}^{\infty} (0.5)^k\,u[n-k]$$

$u[n-k] = 1$ only when $k \leq n$. For $n < 0$, no terms are nonzero, so $y[n] = 0$.

For $n \geq 0$, the upper limit of the sum is capped at $k = n$:

$$y[n] = \sum_{k=0}^{n} (0.5)^k = \frac{1 - (0.5)^{n+1}}{1 - 0.5} = 2\!\left[1 - (0.5)^{n+1}\right]$$

$$\boxed{y[n] = 2\!\left[1 - \left(\tfrac{1}{2}\right)^{n+1}\right] u[n]}$$

**Sanity check:** As $n \to \infty$, $y[n] \to 2$. This equals the DC gain $H(e^{j0}) = \sum_{k=0}^{\infty}(0.5)^k = 2$, which is the correct steady-state response to a unit step.

---

### Q9. What distinguishes FIR from IIR systems in terms of difference equations and practical trade-offs?

**Answer:**

**FIR — non-recursive:**

$$y[n] = \sum_{k=0}^{M} b_k\,x[n-k]$$

- Impulse response: $h[n] = b_n$ for $0 \leq n \leq M$, zero elsewhere. Always finite duration.
- No feedback. Cannot become unstable from coefficient quantisation.

**IIR — recursive:**

$$y[n] = \sum_{k=0}^{M} b_k\,x[n-k] - \sum_{k=1}^{N} a_k\,y[n-k]$$

- Feedback sustains the impulse response indefinitely.
- Much more efficient per unit of frequency selectivity, but requires careful stability monitoring.

| Property | FIR | IIR |
|---|---|---|
| BIBO stability | Always stable | Conditional on pole locations inside unit circle |
| Linear phase | Achievable (symmetric coefficients) | Not achievable (only approximated) |
| Filter order for sharp cutoff | High (often hundreds of taps) | Low (often single digits to tens) |
| Group delay | Constant (linear phase case) | Frequency-dependent |
| Overflow sensitivity | Low — no feedback | Feedback can cause limit cycles |
| Implementation cost | High multiply-accumulate count | Low multiply-accumulate count |

The choice depends on context: real-time audio equalisation often uses IIR biquads for efficiency; FIR is preferred in precise measurement or where group delay consistency matters (digital communications).

---

## Advanced

### Q10. Prove that complex exponentials are eigenfunctions of any LTI system and state the eigenvalue.

**Answer:**

An eigenfunction $x[n]$ of operator $\mathcal{T}$ satisfies $\mathcal{T}\{x[n]\} = \lambda \cdot x[n]$ for some scalar $\lambda$.

**Claim:** $x[n] = e^{j\omega n}$ is an eigenfunction of any LTI system with impulse response $h[n]$.

**Proof:** Apply the convolution sum:

$$y[n] = \sum_{k=-\infty}^{\infty} h[k]\,e^{j\omega(n-k)} = e^{j\omega n} \sum_{k=-\infty}^{\infty} h[k]\,e^{-j\omega k}$$

Define the **frequency response**:

$$H(e^{j\omega}) = \sum_{k=-\infty}^{\infty} h[k]\,e^{-j\omega k}$$

Then $y[n] = H(e^{j\omega})\cdot e^{j\omega n}$, which is the input scaled by the complex constant $H(e^{j\omega})$.

**Eigenvalue:** $\lambda = H(e^{j\omega}) = |H(e^{j\omega})|\,e^{j\angle H(e^{j\omega})}$

The magnitude $|H(e^{j\omega})|$ scales the amplitude; the phase $\angle H(e^{j\omega})$ shifts the phase.

**Physical consequence:** An LTI system cannot create new frequencies — it can only scale and phase-shift existing ones. This is why Fourier analysis of LTI systems is exact and not an approximation.

---

### Q11. A causal LTI system is described by:

$$y[n] - \tfrac{3}{4}\,y[n-1] + \tfrac{1}{8}\,y[n-2] = x[n]$$

Find: (a) $H(z)$, (b) poles and zeros, (c) $h[n]$ via partial fractions, (d) BIBO stability.

**Answer:**

**(a) System function:**

Take the z-transform assuming zero initial conditions:

$$Y(z)\!\left(1 - \tfrac{3}{4}z^{-1} + \tfrac{1}{8}z^{-2}\right) = X(z)$$

$$H(z) = \frac{1}{1 - \frac{3}{4}z^{-1} + \frac{1}{8}z^{-2}} = \frac{z^2}{z^2 - \frac{3}{4}z + \frac{1}{8}}$$

**(b) Poles and zeros:**

Zeros: $z^2 = 0 \Rightarrow z = 0$ (double zero at the origin).

Poles from $z^2 - \tfrac{3}{4}z + \tfrac{1}{8} = 0$:

$$z = \frac{\frac{3}{4} \pm \sqrt{\frac{9}{16} - \frac{4}{8}}}{2} = \frac{\frac{3}{4} \pm \frac{1}{4}}{2}$$

$$z_1 = \frac{1}{2}, \qquad z_2 = \frac{1}{4}$$

**(c) Impulse response:**

$$H(z) = \frac{1}{\left(1 - \frac{1}{2}z^{-1}\right)\!\left(1 - \frac{1}{4}z^{-1}\right)} = \frac{A}{1 - \frac{1}{2}z^{-1}} + \frac{B}{1 - \frac{1}{4}z^{-1}}$$

Matching numerators: $1 = A\!\left(1-\tfrac{1}{4}z^{-1}\right) + B\!\left(1-\tfrac{1}{2}z^{-1}\right)$

- Set $z^{-1} = 2$ (pole at $z = 1/2$): $1 = A(1 - \tfrac{1}{2}) \Rightarrow A = 2$
- Set $z^{-1} = 4$ (pole at $z = 1/4$): $1 = B(1 - 2) \Rightarrow B = -1$

Inverse z-transform (causal — right-sided sequences):

$$\boxed{h[n] = \left[2\!\left(\tfrac{1}{2}\right)^n - \left(\tfrac{1}{4}\right)^n\right]u[n]}$$

**(d) BIBO stability:**

Both poles have magnitude less than 1 ($|z_1| = 0.5 < 1$, $|z_2| = 0.25 < 1$), so both lie inside the unit circle. The system is **BIBO stable**.

Verification: $\sum_{n=0}^{\infty}|h[n]| \leq 2\cdot\frac{1}{1-0.5} + \frac{1}{1-0.25} = 4 + \tfrac{4}{3} = \tfrac{16}{3} < \infty$.

---

### Q12. Explain group delay. When is it constant and why does it matter?

**Answer:**

The **phase response** of an LTI system is $\phi(\omega) = \angle H(e^{j\omega})$.

**Group delay** is defined as:

$$\tau_g(\omega) = -\frac{d\phi(\omega)}{d\omega}$$

It represents the time delay (in samples) experienced by the **envelope** of a narrowband signal centred at frequency $\omega$. Different frequencies may be delayed by different amounts.

**When is group delay constant?**

Group delay is constant when $\phi(\omega) = -\alpha\omega + \beta$ (linear phase), giving $\tau_g(\omega) = \alpha$ for all $\omega$.

For **FIR filters** with symmetric coefficients $h[n] = h[N-1-n]$ (Type I, $N$ odd; Type II, $N$ even), the phase is exactly linear:

$$\phi(\omega) = -\frac{N-1}{2}\omega$$

giving constant group delay $\tau_g = (N-1)/2$ samples. This is a half-sample delay for even $N$.

**Why it matters:**

- **Audio:** Non-constant group delay causes phase dispersion — transient components at different frequencies arrive at different times, smearing percussive attacks. This can be audible on sharp transients with broadband content.
- **Digital communications:** QAM receivers require consistent delay across the signal band. Frequency-dependent delay causes inter-symbol interference (ISI) at the decision point, raising bit error rate.
- **Medical imaging and radar:** Phase coherence between channels is critical; varying group delay decorrelates signals that should be aligned.

IIR filters are inherently non-linear phase, but all-pass equaliser sections can partially compensate. Alternatively, offline zero-phase filtering (apply forward then reverse) eliminates group delay entirely at the cost of non-causality.

---

### Q13. How does pole location in the z-plane determine the character of the impulse response for a causal system?

**Answer:**

The impulse response of a causal system is a superposition of terms, each driven by one pole of $H(z)$.

**Single real pole at $z = p$:** contributes $A\,p^n\,u[n]$.

| Pole magnitude | Behaviour |
|---|---|
| $\|p\| < 1$ | Decaying exponential — transient dies away |
| $\|p\| = 1$ | Constant amplitude (or DC if $p=1$) — marginally stable |
| $\|p\| > 1$ | Growing exponential — unstable |

**Complex conjugate pair at $z = r\,e^{\pm j\omega_0}$:** contributes $A\,r^n\cos(\omega_0 n + \phi)\,u[n]$.

| $r$ | Behaviour |
|---|---|
| $r < 1$ | Damped sinusoidal oscillation at $\omega_0$ |
| $r = 1$ | Undamped sinusoidal oscillation — marginally stable |
| $r > 1$ | Growing sinusoidal oscillation — unstable |

**Repeated poles** at $z = p$ of multiplicity $m$: contribute terms of the form $n^{m-1}p^n u[n]$. A repeated pole on the unit circle is unstable (polynomial growth).

**Summary rule for causal systems:**

$$\text{BIBO stable} \iff \text{all poles strictly inside the unit circle}, \quad |p_k| < 1\;\forall\,k$$

**Practical implication — pole proximity to the unit circle:** A pole very close to (but inside) the unit circle gives a very slowly decaying impulse response and a sharply resonant frequency response. This is exploited in narrowband IIR resonators and notch filters, but also means coefficient quantisation can push a pole outside the circle, destabilising the filter.

---

## Quick Reference

| Signal | Definition |
|---|---|
| Unit impulse | $\delta[n]=1$ if $n=0$, else $0$ |
| Unit step | $u[n]=1$ if $n\geq 0$, else $0$ |
| Real exponential | $a^n u[n]$; decays if $\|a\|<1$ |
| Complex exponential | $e^{j\omega_0 n}$; periodic iff $\omega_0/(2\pi)\in\mathbb{Q}$ |

| System property | Condition |
|---|---|
| Causal | $h[n]=0$ for $n<0$ |
| BIBO stable | $\sum_n\|h[n]\|<\infty$ |
| Stable (z-domain, causal) | All poles strictly inside unit circle |
| Linear phase (FIR) | $h[n]$ symmetric or anti-symmetric |
