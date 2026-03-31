# DSP Filter Design — Multiple-Choice Quiz

**Topics covered:** FIR vs IIR trade-offs, linear phase conditions, Parks-McClellan algorithm, bilinear transform and frequency warping, filter structures (Direct Form I/II, second-order sections), multirate processing (decimation, interpolation, noble identities, CIC filters), window functions.

**Instructions:** Select the single best answer for each question. The answer key with detailed explanations appears at the bottom.

---

## Questions

**Q1.** Which of the following is an advantage of FIR filters over IIR filters?

A. FIR filters require fewer coefficients for a given stopband attenuation.  
B. FIR filters can have exact linear phase (constant group delay).  
C. FIR filters are always more computationally efficient.  
D. FIR filters cannot suffer from coefficient quantisation errors.

---

**Q2.** A Type I FIR filter (odd length, symmetric coefficients) has which of the following frequency response properties?

A. It can approximate any frequency response including highpass and bandpass.  
B. It has a zero forced at $\omega = \pi$ and cannot be used as a highpass filter.  
C. It has a zero forced at $\omega = 0$ and cannot be used as a lowpass filter.  
D. It has zeros at both $\omega = 0$ and $\omega = \pi$.

---

**Q3.** The Parks-McClellan algorithm designs FIR filters by solving which optimisation problem?

A. Minimising the $\ell_2$ (least squares) norm of the frequency response error.  
B. Minimising the $\ell_\infty$ (Chebyshev / minimax) norm of the weighted approximation error.  
C. Minimising the $\ell_1$ norm of the impulse response coefficients.  
D. Maximising the stopband attenuation subject to a passband ripple constraint via linear programming.

---

**Q4.** The bilinear transform maps the s-plane to the z-plane via $s = \frac{2}{T}\frac{z - 1}{z + 1}$. Which statement correctly describes the frequency warping it introduces?

A. The mapping is linear: $\Omega = \frac{2}{T}\omega$ for all frequencies.  
B. The mapping compresses high frequencies and expands low frequencies compared to an ideal linear mapping.  
C. The warping is $\Omega = \frac{2}{T}\tan\!\left(\frac{\omega}{2}\right)$, which expands frequencies near DC and compresses them near $\omega = \pi$.  
D. The bilinear transform introduces aliasing because it is not a one-to-one mapping.

---

**Q5.** An IIR filter implemented in Direct Form II (DF-II) uses fewer delay elements than Direct Form I (DF-I) of the same order. Why is DF-II sometimes avoided in fixed-point implementations?

A. DF-II has higher computational complexity than DF-I.  
B. DF-II internal state variables can overflow even when the input and output are within bounds.  
C. DF-II does not support recursive (IIR) filter implementations.  
D. DF-II requires complex-valued arithmetic.

---

**Q6.** A second-order IIR filter section (biquad) has transfer function:

$$H(z) = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}}$$

Why is it standard practice to cascade multiple biquad sections rather than implement a high-order IIR as a single direct-form filter?

A. Biquad sections are easier to design from scratch without using tools.  
B. Cascaded biquads avoid pole-zero cancellation numerical errors and reduce sensitivity to coefficient quantisation.  
C. A single high-order direct form uses more multiplications than cascaded biquads.  
D. Biquad sections can only realise lowpass responses, so cascading extends the filter type.

---

**Q7.** A signal at sample rate $f_s$ is to be decimated by a factor $M$. Why must an anti-aliasing (lowpass) filter be applied before the downsampler?

A. To increase the signal amplitude so it is not attenuated by downsampling.  
B. To remove frequency components above $f_s / (2M)$ that would alias into the baseband after downsampling.  
C. To compensate for the gain increase introduced by the downsampler.  
D. To convert the signal from real-valued to complex-valued before downsampling.

---

**Q8.** The noble identity for decimation states that:

A. Downsampling by $M$ followed by filtering with $H(z)$ equals filtering with $H(z^M)$ followed by downsampling by $M$.  
B. Filtering with $H(z)$ followed by downsampling by $M$ equals downsampling by $M$ followed by filtering with $H(z^M)$.  
C. A decimation filter of order $N$ requires only $N/M$ multiplications per output sample.  
D. Any rational filter can be decomposed into $M$ polyphase components of equal length.

---

**Q9.** A CIC (Cascaded Integrator-Comb) decimation filter of order $N$ and decimation factor $R$ has a transfer function:

$$H(z) = \left(\frac{1 - z^{-R}}{1 - z^{-1}}\right)^N$$

What is the primary advantage of a CIC filter over a conventional FIR decimation filter?

A. CIC filters achieve sharper stopband attenuation than an equivalent-order FIR.  
B. CIC filters require only additions and subtractions — no multiplications — making them very efficient in hardware.  
C. CIC filters have a perfectly flat passband by design.  
D. CIC filters can operate at the output (low) sample rate without any modification.

---

**Q10.** Which window function provides the best stopband attenuation at the cost of the widest transition band?

A. Rectangular  
B. Hann  
C. Hamming  
D. Blackman

---

**Q11.** The Hann window applied to a length-$N$ sequence is defined as:

$$w[n] = 0.5\left(1 - \cos\!\left(\frac{2\pi n}{N-1}\right)\right), \quad 0 \leq n \leq N-1$$

Compared to the rectangular window of the same length, the Hann window:

A. Increases the mainlobe width and reduces sidelobe levels.  
B. Reduces the mainlobe width and increases sidelobe levels.  
C. Has no effect on spectral leakage — only zero-padding affects leakage.  
D. Increases both mainlobe width and sidelobe levels.

---

**Q12.** When designing a digital highpass filter using the bilinear transform from an analogue prototype, the analogue prototype cutoff frequency $\Omega_c$ must be prewarped. For a desired digital cutoff $\omega_c$, the correct prewarped analogue frequency is:

A. $\Omega_c = \omega_c / T$

B. $\Omega_c = \dfrac{2}{T} \sin\!\left(\dfrac{\omega_c}{2}\right)$

C. $\Omega_c = \dfrac{2}{T} \tan\!\left(\dfrac{\omega_c}{2}\right)$

D. $\Omega_c = \dfrac{\omega_c}{2\pi T}$

---

**Q13.** In a polyphase decomposition of a length-$N$ FIR filter for interpolation by $L$, the filter is split into $L$ polyphase subfilters each of length approximately $N/L$. What is the key computational benefit?

A. The total number of filter coefficients is reduced by a factor of $L$.  
B. Each polyphase branch operates at the input (low) sample rate, reducing computation by a factor of $L$ compared to filtering at the output rate.  
C. The polyphase structure avoids the need for an anti-imaging filter.  
D. The polyphase structure converts the FIR filter into an equivalent IIR structure.

---

**Q14.** An IIR filter designed using the impulse invariance method will exhibit aliasing in the frequency domain. This occurs because:

A. The impulse invariance method applies the bilinear transform, which is not a one-to-one mapping.  
B. The continuous-time impulse response is sampled, causing the spectra of all shifted copies to overlap.  
C. The method preserves only the poles of the analogue filter and discards the zeros.  
D. Impulse invariance always produces an unstable digital filter.

---

**Q15.** A Type IV FIR filter (even length, anti-symmetric coefficients) has a zero at $\omega = 0$. This makes it suitable for which application?

A. Lowpass filtering  
B. Hilbert transform implementation  
C. Notch filtering at DC  
D. All-pass equalisation

---

**Q16.** When decimating by a large factor $M$, a common efficient design strategy is:

A. A single equiripple FIR filter designed to meet the overall specification.  
B. A single IIR filter to minimise the filter order.  
C. A multistage approach: coarse decimation with a CIC filter followed by fine correction with a shorter FIR filter.  
D. Applying the noble identity to move the downsampler before the filter, eliminating the need for a filter altogether.

---

**Q17.** The stopband attenuation of a CIC filter of order $N$ and decimation ratio $R$, at an aliasing frequency $f_a = f_s/R - f_p$ (where $f_p$ is the passband edge), is approximately:

A. $20N \log_{10}(R)\ \text{dB}$  
B. $6N\ \text{dB}$  
C. $20N \log_{10}\!\left(\frac{R \sin(\pi f_a / f_s)}{\sin(\pi f_a / (f_s/R))}\right)\ \text{dB}$  
D. $40 \log_{10}(NR)\ \text{dB}$

---

**Q18.** A linear-phase FIR filter with real coefficients requires that the impulse response be either symmetric or anti-symmetric about its midpoint. This condition ensures that:

A. All poles lie at the origin.  
B. The group delay is exactly $(N-1)/2$ samples, constant across all frequencies.  
C. The filter has no zeros on the unit circle.  
D. The frequency response has zero imaginary part for all $\omega$.

---

## Answer Key

| Q | Answer |
|---|--------|
| 1 | B |
| 2 | A |
| 3 | B |
| 4 | C |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | B |
| 10 | D |
| 11 | A |
| 12 | C |
| 13 | B |
| 14 | B |
| 15 | B |
| 16 | C |
| 17 | A |
| 18 | B |

---

## Detailed Explanations

**Q1 — Answer: B**

The defining practical advantage of FIR filters is that symmetric or anti-symmetric coefficients guarantee exact linear phase (constant group delay), which is critical in audio, communications, and biomedical signal processing. IIR filters cannot achieve this. Option A is wrong — IIR filters typically require far fewer coefficients than FIR for the same attenuation. Option C is often wrong in practice; an IIR biquad cascade can be far cheaper than a long FIR. Option D is wrong — quantisation affects both types, though IIR filters are more sensitive due to feedback.

---

**Q2 — Answer: A**

A Type I FIR filter (odd length $N$, symmetric: $h[n] = h[N-1-n]$) has no forced zeros at $\omega = 0$ or $\omega = \pi$. Its frequency response $H(e^{j\omega})$ can be a real-valued, even function of $\omega$ with no structural constraints preventing highpass or bandpass designs. This is why Type I is the most versatile FIR type. Option B describes Type II (even length, symmetric), which has a forced zero at $\omega = \pi$. Option C describes Type III (anti-symmetric, odd length), which has zeros at both $\omega = 0$ and $\omega = \pi$. Option D describes Type III, not Type I.

---

**Q3 — Answer: B**

Parks-McClellan (also called the Remez exchange algorithm) solves the Chebyshev (minimax) approximation problem: it minimises the maximum weighted error $\max_\omega |W(\omega)(D(\omega) - H(\omega))|$ over specified frequency bands. By the equiripple theorem, the optimal solution has the error equirippling between $\pm\delta$ at $N+2$ extremal frequencies. Option A describes windowed-sinc or least-squares FIR design. Option C describes LASSO-style sparse design. Option D is a reasonable-sounding but incorrect characterisation — LP methods exist but are not the Parks-McClellan formulation.

---

**Q4 — Answer: C**

The bilinear transform substitution $s = \frac{2}{T}\frac{z-1}{z+1}$ maps the unit circle ($z = e^{j\omega}$) to the imaginary axis ($s = j\Omega$) via:

$$\Omega = \frac{2}{T}\tan\!\left(\frac{\omega}{2}\right)$$

For small $\omega$, $\tan(\omega/2) \approx \omega/2$, so $\Omega \approx \omega/T$ (nearly linear). As $\omega \to \pi$, $\tan(\omega/2) \to \infty$, so the entire semi-infinite analogue frequency axis maps onto the finite interval $[0, \pi]$ — this is the compression at high frequencies. Option A (linear mapping) is wrong. Option B has the direction of compression reversed. Option D is wrong — the bilinear transform is a one-to-one mapping from the unit circle to the imaginary axis with no aliasing, unlike impulse invariance.

---

**Q5 — Answer: B**

DF-II (transposed or canonical form) shares the delay line between the feedback and feedforward paths, requiring $N$ delays for an $N$th-order filter rather than $2N$ for DF-I. However, in DF-II, the state (delay) variables represent an intermediate signal that combines both the input and the accumulated feedback. This intermediate signal can take values much larger than either the input or output, causing overflow in fixed-point arithmetic even when the final output is in range. DF-I keeps feedback and feedforward states separate, reducing overflow risk. Option A is wrong — DF-II uses fewer multiplications, not more. Options C and D are false.

---

**Q6 — Answer: B**

Implementing a high-order IIR as a single direct form suffers from severe coefficient sensitivity: small quantisation errors in coefficients cause large shifts in pole and zero locations, potentially destabilising the filter. Cascaded second-order sections (SOS/biquads) confine each pole pair to its own isolated section. Quantisation of biquad coefficients causes only local perturbations and the filter remains much better conditioned. Option A is false — biquad design still uses tools. Option C is wrong — the number of multiplications is essentially the same (same total order). Option D is false — biquads can realise any response type.

---

**Q7 — Answer: B**

Decimation by $M$ keeps every $M$th sample, which in frequency corresponds to stretching the spectrum by $M$ and adding $M-1$ shifted copies (aliasing). Any signal energy above the new Nyquist frequency $f_s/(2M)$ will fold back into the baseband and be indistinguishable from legitimate low-frequency content. The anti-aliasing filter removes these out-of-band components before the downsampler. Options A and C describe gain changes that do not occur — a downsampler is a sample selection operation, not a scaling operation. Option D is irrelevant to anti-aliasing.

---

**Q8 — Answer: B**

The noble identity for decimation states: filtering with $H(z)$ at rate $f_s$ followed by downsampling by $M$ is equivalent to downsampling by $M$ first, then filtering with $H(z^M)$ at rate $f_s/M$. Formally: $\downarrow M \circ H(z) = H(z^M) \circ \downarrow M$. This allows moving the filter to the output side at the lower rate, saving computation. Note that $H(z^M)$ is an interpolated version of the filter (its impulse response has $M-1$ zeros inserted between each tap). Option A reverses the order of operations. Options C and D describe properties of polyphase decomposition, not the noble identity.

---

**Q9 — Answer: B**

A CIC filter consists of $N$ integrators (running accumulators: $y[n] = y[n-1] + x[n]$) operating at the input rate, followed by downsampling, followed by $N$ comb sections (differentiators: $y[n] = x[n] - x[n-R]$) at the output rate. Both accumulators and differentiators require only additions and subtractions — no multiplications at all. This makes CIC filters extremely attractive for very high-speed hardware such as SDR front ends. Option A is false — CIC filters have a $\text{sinc}^N$ frequency response with relatively poor stopband behaviour. Option C is false — the $\text{sinc}^N$ shape causes significant passband droop. Option D is false — the integrators run at the input high rate.

---

**Q10 — Answer: D (Blackman)**

Among the four windows listed, the Blackman window achieves the highest stopband attenuation (approximately 74 dB) due to its three-term cosine construction, which rolls off the window spectrum rapidly. The cost is the widest mainlobe (transition band approximately $8\pi/N$ wide). The rectangular window (A) has the narrowest mainlobe (transition band $\approx 4\pi/N$) but only 13 dB sidelobe attenuation. Hann (B) gives about 44 dB and Hamming (C) about 53 dB, both with intermediate transition widths.

---

**Q11 — Answer: A**

The Hann window is a smooth bell-shaped taper that reduces the discontinuity at the edges of the analysis window, substantially lowering spectral sidelobes (from about $-13\ \text{dB}$ for rectangular to about $-32\ \text{dB}$ first sidelobe for Hann). The cost is a wider mainlobe — approximately double the rectangular window's mainlobe width. Option B has the effects reversed. Option C is wrong — windowing is specifically the technique for reducing spectral leakage; zero-padding only increases frequency resolution (interpolates the spectrum) without reducing leakage. Option D is self-contradictory since wider mainlobe and higher sidelobes would make the window worse in every way.

---

**Q12 — Answer: C**

The bilinear transform maps digital frequency $\omega$ to analogue frequency via $\Omega = \frac{2}{T}\tan(\omega/2)$. To achieve a digital cutoff at $\omega_c$, the analogue prototype must be designed with cutoff at the prewarped frequency $\Omega_c = \frac{2}{T}\tan(\omega_c/2)$. After applying the bilinear transform, the prototype cutoff at $\Omega_c$ maps exactly to $\omega_c$. Option A is the naive (incorrect) linear mapping. Option B uses $\sin$ instead of $\tan$. Option D divides by $2\pi T$, which has no basis in the bilinear transform derivation.

---

**Q13 — Answer: B**

In polyphase interpolation, the upsampler inserts $L-1$ zeros between each input sample. If the interpolation filter operates at the high output rate, it performs $N$ multiplications per output sample, but $L-1$ of every $L$ multiplications involve the inserted zeros and produce no useful contribution. The polyphase decomposition moves computation to the input (low) rate: each of $L$ polyphase subfilters of length $N/L$ operates once per input sample, giving a total of $N/L \times L = N$ multiplications per input sample — equivalent to $N/L$ multiplications per output sample. This is an $L$-fold saving. Option A is wrong — the total number of coefficients remains $N$. Option C is wrong — the anti-imaging role is still performed by the polyphase filter collectively. Option D is wrong — the structure is still FIR.

---

**Q14 — Answer: B**

Impulse invariance works by sampling the continuous-time impulse response $h_a(t)$ at interval $T$: $h[n] = h_a(nT)$. Sampling in the time domain corresponds to periodisation in the frequency domain with period $\omega_s = 2\pi/T$. The digital frequency response is therefore $H(e^{j\omega}) = \frac{1}{T}\sum_{k=-\infty}^{\infty} H_a\!\left(j\frac{\omega - 2\pi k}{T}\right)$. If $H_a(j\Omega)$ is not strictly bandlimited to $|\Omega| < \pi/T$, these shifted copies overlap, causing aliasing. IIR analogue prototypes (Butterworth, Chebyshev) are never strictly bandlimited. Option A incorrectly describes the bilinear transform. Option C is partially true (some zeros are dropped) but is not the cause of aliasing. Option D is false.

---

**Q15 — Answer: B**

A Type IV FIR filter (even length $N$, anti-symmetric: $h[n] = -h[N-1-n]$) has a forced zero at both $\omega = 0$ and $\omega = \pi$. The frequency response has the form $H(e^{j\omega}) = je^{-j\omega(N-1)/2} \tilde{H}(\omega)$ where $\tilde{H}(\omega)$ is a real odd function. This $90°$ phase shift across all frequencies, combined with an approximately flat magnitude over a wide band, makes Type IV ideal for implementing a discrete Hilbert transform (which requires $90°$ phase shift at all frequencies). Option A (lowpass) is incompatible with the zero at DC. Option C (notch at DC) would only require a zero at DC, not the anti-symmetric structure. Option D (all-pass) requires unity magnitude at all frequencies.

---

**Q16 — Answer: C**

When $M$ is large (e.g., $M = 64$ or more, common in SDR applications), a single-stage FIR meeting the overall attenuation and transition-band specifications would be extremely long and expensive. The efficient strategy is multistage decimation: a CIC filter performs the bulk of the decimation efficiently (no multiplications), followed by a compensation FIR filter that corrects the CIC's passband droop and provides additional stopband shaping. This dramatically reduces total coefficient count and computation. Option A (single equiripple FIR) is impractically expensive for large $M$. Option B (single IIR) introduces phase distortion and fixed-point stability concerns. Option D misunderstands the noble identity — moving the downsampler before the filter requires changing the filter, not eliminating it.

---

**Q17 — Answer: A**

The CIC filter's magnitude response is $|H(f)|^N$ where $|H(f)| = \left|\frac{\sin(\pi f R / f_s)}{\sin(\pi f / f_s)}\right|$. At aliasing band frequencies near the edge of the first alias zone, the attenuation in dB grows as $N$ times the single-stage attenuation in dB. For the worst-case aliasing frequency (closest to the transition band), the approximation simplifies to approximately $20N\log_{10}(R)\ \text{dB}$ for large $R$. This rule of thumb is widely used in CIC design. Option B ($6N$ dB) is the slope of a first-order CIC at high frequencies in terms of octave roll-off. Options C and D are either more precise variants or incorrect formulas.

---

**Q18 — Answer: B**

For a symmetric FIR filter with $h[n] = h[N-1-n]$ (length $N$), the phase response is:

$$\angle H(e^{j\omega}) = -\omega \frac{N-1}{2} + \text{constant}$$

This is a linear function of $\omega$, meaning the group delay $\tau_g = -\frac{d\phi}{d\omega} = \frac{N-1}{2}$ is constant for all frequencies. Option A is true (all FIR poles are at the origin) but is not a consequence of the symmetry condition — it is true for all FIR filters. Option C is false — symmetric FIR filters frequently have zeros on the unit circle (in fact, the symmetry forces them to come in conjugate-reciprocal pairs). Option D is false — the frequency response of a symmetric FIR is real only if the filter is also even-symmetric in terms of its support alignment.
