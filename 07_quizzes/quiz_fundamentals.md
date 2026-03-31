# DSP Fundamentals — Multiple-Choice Quiz

**Topics covered:** Nyquist theorem, aliasing, z-transform, region of convergence, poles and zeros, DFT properties, linear vs circular convolution, LTI system properties, BIBO stability.

**Instructions:** Select the single best answer for each question. The answer key with detailed explanations appears at the bottom.

---

## Questions

**Q1.** A continuous-time signal contains frequency components up to 8 kHz. According to the Nyquist–Shannon sampling theorem, what is the minimum sampling rate that guarantees perfect reconstruction?

A. 8 kHz  
B. 12 kHz  
C. 16 kHz  
D. 4 kHz

---

**Q2.** A signal sampled at $f_s = 1000\ \text{Hz}$ contains a sinusoidal component at $f = 750\ \text{Hz}$. After sampling, this component aliases to which frequency?

A. 750 Hz  
B. 500 Hz  
C. 250 Hz  
D. 125 Hz

---

**Q3.** The z-transform of the unit step sequence $u[n]$ is:

$$U(z) = \sum_{n=0}^{\infty} z^{-n}$$

What is the closed-form expression and its region of convergence (ROC)?

A. $\dfrac{z}{z-1}$, ROC: $|z| < 1$

B. $\dfrac{1}{1 - z^{-1}}$, ROC: $|z| > 1$

C. $\dfrac{z}{z+1}$, ROC: $|z| > 1$

D. $\dfrac{1}{1 + z^{-1}}$, ROC: $|z| < 1$

---

**Q4.** A causal LTI system has the transfer function:

$$H(z) = \frac{z^2}{(z - 0.5)(z + 2)}$$

Which statement about this system is correct?

A. The system is BIBO stable because both poles lie inside the unit circle.  
B. The system is BIBO stable because the ROC includes the unit circle.  
C. The system is not BIBO stable because the pole at $z = -2$ lies outside the unit circle.  
D. The system is not BIBO stable because the pole at $z = 0.5$ is the outermost pole.

---

**Q5.** For a right-sided (causal) sequence, the ROC of its z-transform is:

A. The interior of a circle centred at the origin  
B. The exterior of a circle centred at the origin  
C. A vertical strip in the s-plane  
D. The entire z-plane excluding the origin

---

**Q6.** The N-point DFT of a length-N real-valued sequence $x[n]$ satisfies which symmetry property?

A. $X[k] = X[N - k]$ (periodic symmetry only, magnitudes equal)  
B. $X[k] = X^*[N - k]$ (conjugate symmetry)  
C. $X[k] = -X^*[N - k]$ (anti-conjugate symmetry)  
D. $X[k] = X[k + N/2]$ (half-period symmetry)

---

**Q7.** An N-point DFT is computed on a length-N sequence. If the input is circularly shifted by $m$ samples (i.e., $x[(n - m) \bmod N]$), what happens to the DFT output?

A. $X[k]$ is multiplied by $e^{+j2\pi km/N}$  
B. $X[k]$ is multiplied by $e^{-j2\pi km/N}$  
C. $X[k]$ is shifted by $m$ bins  
D. $X[k]$ is unchanged

---

**Q8.** You need to compute the linear convolution of a length-$L$ sequence and a length-$M$ sequence using the DFT. What is the minimum DFT size $N$ that avoids time-domain aliasing?

A. $N \geq L + M$  
B. $N \geq L + M - 1$  
C. $N \geq \max(L, M)$  
D. $N \geq 2 \cdot \max(L, M)$

---

**Q9.** Which of the following is NOT a requirement for a system to be classified as Linear Time-Invariant (LTI)?

A. Superposition (additivity and homogeneity)  
B. A shift in input produces an equal shift in output  
C. The impulse response $h[n]$ is absolutely summable  
D. Both linearity and time-invariance hold simultaneously

---

**Q10.** The impulse response of an LTI system is $h[n] = (0.9)^n u[n]$. What is the system's frequency response magnitude at $\omega = 0$?

A. 0.9  
B. 1  
C. 10  
D. 0

---

**Q11.** A discrete-time LTI system is BIBO stable if and only if:

A. All poles of $H(z)$ have magnitude less than 1  
B. The transfer function $H(z)$ has no zeros on the unit circle  
C. The system is causal and all poles lie inside the unit circle  
D. The impulse response $h[n]$ is absolutely summable: $\sum_{n=-\infty}^{\infty} |h[n]| < \infty$

---

**Q12.** Consider the z-transform pair $x[n] = a^n u[n]$ with $0 < a < 1$. As $a$ increases toward 1, which of the following best describes the effect on the frequency response?

A. The magnitude response becomes flatter across all frequencies.  
B. The low-frequency gain increases and the response becomes more sharply peaked near $\omega = 0$.  
C. The high-frequency gain increases and the system acts as a high-pass filter.  
D. The system becomes non-causal.

---

**Q13.** Linear convolution of two sequences of lengths $L$ and $M$ produces a sequence of length:

A. $\max(L, M)$  
B. $L \cdot M$  
C. $L + M$  
D. $L + M - 1$

---

**Q14.** The DFT of a length-8 real sequence yields $X[1] = 2 - 3j$. Using DFT symmetry, what is $X[7]$?

A. $2 + 3j$  
B. $-2 + 3j$  
C. $2 - 3j$  
D. $-2 - 3j$

---

**Q15.** Which statement correctly describes the relationship between the DTFT and the z-transform?

A. The DTFT is the z-transform evaluated on the imaginary axis of the z-plane.  
B. The z-transform always converges wherever the DTFT exists.  
C. The DTFT equals $H(z)$ evaluated on the unit circle at $z = e^{j\omega}$.  
D. The DTFT and z-transform are unrelated for non-causal sequences.

---

**Q16.** A system has the difference equation $y[n] = x[n] + 2y[n-1]$. What are the pole location and stability status?

A. Pole at $z = 0.5$; system is stable.  
B. Pole at $z = 1$; system is marginally stable.  
C. Pole at $z = -2$; system is unstable.  
D. Pole at $z = 2$; system is unstable.

---

**Q17.** When does N-point circular convolution produce the same result as linear convolution of two length-N sequences?

A. Always, provided both sequences are zero-padded to length $2N$.  
B. Only when both sequences are symmetric.  
C. Never — circular and linear convolution always differ.  
D. When the linear convolution result has length $\leq N$ (i.e., no wrap-around aliasing occurs).

---

## Answer Key

| Q | Answer |
|---|--------|
| 1 | C |
| 2 | C |
| 3 | B |
| 4 | C |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | C |
| 10 | C |
| 11 | D |
| 12 | B |
| 13 | D |
| 14 | A |
| 15 | C |
| 16 | D |
| 17 | D |

---

## Detailed Explanations

**Q1 — Answer: C (16 kHz)**

The Nyquist–Shannon theorem states the sampling rate must exceed twice the highest frequency: $f_s > 2 f_{max}$. For $f_{max} = 8\ \text{kHz}$, the Nyquist rate is $2 \times 8 = 16\ \text{kHz}$. Sampling at exactly this rate is theoretically sufficient but requires an ideal brick-wall anti-aliasing filter. In practice, engineers oversample by 10–20% to relax filter requirements. Option A (8 kHz) violates the theorem; 12 kHz (B) is below the Nyquist rate; 4 kHz (D) is far too low.

---

**Q2 — Answer: C (250 Hz)**

When a component at frequency $f$ is sampled at $f_s$, aliases appear at $|f - k f_s|$ for integer $k$. For $f = 750\ \text{Hz}$ and $f_s = 1000\ \text{Hz}$:

$$|750 - 1 \times 1000| = 250\ \text{Hz}$$

Geometrically, 750 Hz is reflected around the Nyquist frequency $f_s/2 = 500\ \text{Hz}$ to land at $1000 - 750 = 250\ \text{Hz}$. Option A (750 Hz) would apply only if $f < f_s/2$. Option B (500 Hz) is the Nyquist frequency itself. Option D (125 Hz) has no basis in folding arithmetic.

---

**Q3 — Answer: B**

The geometric series $\sum_{n=0}^{\infty} r^n = \frac{1}{1-r}$ for $|r| < 1$ gives, with $r = z^{-1}$:

$$U(z) = \frac{1}{1 - z^{-1}}, \quad |z^{-1}| < 1 \Rightarrow |z| > 1$$

Option A is algebraically equivalent ($\frac{z}{z-1}$) but states the wrong ROC ($|z| < 1$), which would describe a left-sided anti-causal sequence. Option C has a pole at $z = -1$ (wrong sign). Option D also has the wrong sign and the wrong ROC.

---

**Q4 — Answer: C**

For a causal system the ROC is the exterior of a circle through the outermost pole. The poles are at $z = 0.5$ ($|z| = 0.5$) and $z = -2$ ($|z| = 2$). The outermost pole is at magnitude 2, so the ROC is $|z| > 2$. The unit circle ($|z| = 1$) lies at magnitude 1, which is inside the ROC boundary of 2 — the unit circle is NOT contained in the ROC. Therefore the system is BIBO unstable. Option A wrongly claims both poles are inside the unit circle (the pole at $z = -2$ is not). Option B wrongly claims the ROC includes the unit circle. Option D misidentifies which pole drives instability.

---

**Q5 — Answer: B**

A right-sided sequence $x[n] = 0$ for $n < N_0$ has a z-transform converging for $|z| > r_{max}$, where $r_{max}$ is the magnitude of the outermost pole. This is the exterior of a circle. Option A (interior of a circle) corresponds to a left-sided sequence. Option C describes the Laplace transform ROC structure. Option D would apply only if the sequence were a finite-length (FIR) one, where convergence holds everywhere except possibly $z = 0$ or $z = \infty$.

---

**Q6 — Answer: B**

For a real-valued input $x[n]$, the DFT satisfies conjugate symmetry: $X[k] = X^*[N - k]$. This implies $|X[k]| = |X[N-k]|$ (even magnitude spectrum) and $\angle X[k] = -\angle X[N-k]$ (odd phase spectrum). Option A is incomplete — it states only that the magnitudes are equal, missing the conjugate relationship of the complex values. Option C (anti-conjugate symmetry) implies $\text{Re}\{X[k]\} = 0$, which is not generally true. Option D (half-period symmetry) applies only to sequences with a specific structural repetition.

---

**Q7 — Answer: B**

The circular time-shift property states: $x[(n-m) \bmod N] \xrightarrow{\text{DFT}} e^{-j2\pi km/N} X[k]$. The negative sign arises because a delay of $m$ samples corresponds to multiplying each DFT bin by a complex exponential with a negative phase ramp. Option A has a positive sign, corresponding to an advance (left shift by $m$). Option C is wrong — a time shift modifies the phase of each bin but does not shift the bin indices. Option D is wrong — a non-trivial shift always alters the phase spectrum.

---

**Q8 — Answer: B**

The linear convolution of sequences of lengths $L$ and $M$ has length $L + M - 1$. To avoid circular aliasing, the DFT must be at least this long: $N \geq L + M - 1$. Option A ($L + M$) is valid but wastes one extra bin compared to the minimum. Option C ($\max(L,M)$) is too small and will cause aliasing when $\min(L,M) > 1$. Option D is unnecessarily conservative.

---

**Q9 — Answer: C**

LTI classification requires linearity (superposition: additivity plus homogeneity) and time-invariance (a time shift in the input produces an identical time shift in the output). Absolute summability of $h[n]$ is the condition for BIBO stability, not for being LTI. A system can be LTI yet unstable — for example, $h[n] = u[n]$ is LTI but its impulse response is not absolutely summable. Options A, B, and D all describe genuine requirements for LTI classification.

---

**Q10 — Answer: C (10)**

The frequency response is $H(e^{j\omega}) = \sum_{n=0}^{\infty} (0.9)^n e^{-j\omega n}$. At $\omega = 0$, all exponential factors equal 1:

$$H(e^{j0}) = \sum_{n=0}^{\infty} (0.9)^n = \frac{1}{1 - 0.9} = \frac{1}{0.1} = 10$$

Option A (0.9) is just the coefficient of the first non-trivial term. Option B (1) is the DC gain of a simple delay. Option D (0) would occur at a frequency where destructive interference is complete, not at DC for this filter.

---

**Q11 — Answer: D**

The necessary and sufficient condition for BIBO stability of any LTI system is that the impulse response be absolutely summable: $\sum_{n=-\infty}^{\infty} |h[n]| < \infty$. This condition guarantees that any bounded input produces a bounded output. Option A is sufficient only for causal systems and not necessary for non-causal systems — a two-sided system with poles both inside and outside the unit circle can be stable if the ROC of its two-sided z-transform includes the unit circle. Option B describes a property related to zeros, not stability. Option C adds an unnecessary causality constraint.

---

**Q12 — Answer: B**

The transfer function is $H(z) = \frac{1}{1 - az^{-1}}$. As $a \to 1^-$, the pole at $z = a$ approaches the unit circle at $z = 1$ (i.e., $\omega = 0$). The magnitude response is $|H(e^{j\omega})| = \frac{1}{|1 - ae^{-j\omega}|}$. Near $\omega = 0$, the denominator $|1 - a|$ approaches zero, so the gain becomes enormous — a very sharp peak at DC. The system behaves like an increasingly narrow low-pass filter. Option A (flat response) is the opposite of what happens. Option C (high-pass) is wrong — the pole near $\omega = 0$ amplifies low frequencies. Option D is wrong — causality is unaffected by $a$.

---

**Q13 — Answer: D ($L + M - 1$)**

When computing $y[n] = x[n] * h[n]$, the first nonzero output is at index $0 + 0 = 0$ and the last is at index $(L-1) + (M-1) = L + M - 2$. The total count is $(L + M - 2) - 0 + 1 = L + M - 1$. Option C ($L+M$) is off by one — a common off-by-one error in interviews. Option A ($\max(L,M)$) would apply if the shorter sequence simply windowed the longer. Option B ($L \cdot M$) confuses convolution length with polynomial multiplication of general power series.

---

**Q14 — Answer: A ($2 + 3j$)**

For a real-valued sequence of length $N$, conjugate symmetry gives $X[N - k] = X^*[k]$. With $N = 8$ and $k = 1$:

$$X[7] = X[8 - 1] = X^*[1] = (2 - 3j)^* = 2 + 3j$$

Option B has the wrong real part sign. Option C simply repeats $X[1]$ without taking the conjugate. Option D negates both parts, which would imply $X[7] = -X[1]$, not $X^*[1]$.

---

**Q15 — Answer: C**

The DTFT is defined as $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$. Comparing with the z-transform $X(z) = \sum_{n} x[n] z^{-n}$, the DTFT is obtained by substituting $z = e^{j\omega}$, i.e., evaluating $X(z)$ on the unit circle. Option A confuses the z-transform with the Laplace transform, which is evaluated on the imaginary axis $s = j\omega$. Option B is wrong — if the ROC of $X(z)$ excludes the unit circle, the DTFT does not exist in the classical sense even though the z-transform is well defined elsewhere. Option D is false; the relationship holds for all sequences, causal or not.

---

**Q16 — Answer: D**

Taking the z-transform of $y[n] = x[n] + 2y[n-1]$:

$$Y(z) = X(z) + 2z^{-1}Y(z) \implies H(z) = \frac{1}{1 - 2z^{-1}} = \frac{z}{z - 2}$$

The pole is at $z = 2$. For a causal implementation, the ROC is $|z| > 2$, which does not contain the unit circle. The system is BIBO unstable — outputs grow exponentially for any non-zero input. Option A has the wrong pole location. Option B ($z = 1$) would arise from $y[n] = x[n] + y[n-1]$ (an integrator), which is only marginally stable. Option C has the wrong sign.

---

**Q17 — Answer: D**

N-point circular convolution wraps the linear convolution result around the N-point block. If the linear convolution result has length $\leq N$ (i.e., no sample from the tail wraps onto the head), circular and linear convolution are identical. For two length-N sequences, the linear convolution has length $2N - 1$. To avoid aliasing, one must zero-pad to at least $2N - 1$ before taking the DFT — this is the basis of the overlap-add/overlap-save algorithms. Option A (zero-pad to $2N$) is one valid approach, but the condition is on the convolution result fitting, not automatically always (C is wrong). Option B (symmetry) is irrelevant to this equivalence.
