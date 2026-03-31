# Communications DSP — Multiple-Choice Quiz

**Topics covered:** BPSK, QPSK, and QAM bit error rate (BER), matched filtering, raised cosine pulse shaping, Nyquist ISI criterion, OFDM (cyclic prefix, subcarrier orthogonality, PAPR), timing and frequency synchronisation.

**Instructions:** Select the single best answer for each question. The answer key with detailed explanations appears at the bottom.

---

## Questions

**Q1.** In an AWGN channel, the bit error probability (BER) for coherently detected BPSK is:

A. $P_b = Q\!\left(\sqrt{E_b/N_0}\right)$

B. $P_b = Q\!\left(\sqrt{2 E_b/N_0}\right)$

C. $P_b = \frac{1}{2}\exp\!\left(-E_b/N_0\right)$

D. $P_b = Q\!\left(E_b/N_0\right)$

---

**Q2.** QPSK transmits 2 bits per symbol by encoding them onto 4 phase points. Compared to BPSK at the same symbol energy $E_s$, QPSK achieves:

A. The same BER, since both schemes have the same minimum Euclidean distance when $E_b$ is held constant.  
B. Worse BER because the constellation points are closer together.  
C. Better BER because more bits are transmitted per symbol.  
D. The same spectral efficiency but twice the bandwidth requirement.

---

**Q3.** For 16-QAM in an AWGN channel, the approximate BER as a function of bit energy $E_b / N_0$ is higher than for QPSK at the same $E_b / N_0$ because:

A. 16-QAM uses more power per symbol.  
B. The minimum Euclidean distance between constellation points is smaller relative to the average symbol energy, requiring higher $E_b/N_0$ to achieve the same BER.  
C. 16-QAM requires a more complex receiver.  
D. 16-QAM is sensitive to phase noise and cannot operate in AWGN.

---

**Q4.** A matched filter maximises the signal-to-noise ratio (SNR) at the sampling instant. For a signal pulse $s(t)$ in AWGN with one-sided noise PSD $N_0/2$, the matched filter impulse response is:

A. $h(t) = s(t)$  
B. $h(t) = s(T - t)$, a time-reversed and delayed version of the transmit pulse  
C. $h(t) = s(-t)$, a time-reversed version of the transmit pulse without delay  
D. $h(t) = \frac{1}{s(t)}$, the inverse of the transmit pulse

---

**Q5.** The Nyquist ISI criterion states that a pulse $p(t)$ causes zero inter-symbol interference (ISI) at the symbol sampling instants $t = kT$ if and only if:

A. The Fourier transform $P(f)$ is bandlimited to $|f| \leq 1/(2T)$.  
B. $p(kT) = \delta[k]$ (i.e., the pulse equals 1 at $t = 0$ and 0 at all other integer multiples of $T$).  
C. The pulse $p(t)$ decays faster than $1/t$ for large $t$.  
D. The pulse $p(t)$ is symmetric about $t = T/2$.

---

**Q6.** The raised cosine (RC) spectrum is parameterised by the roll-off factor $\alpha \in [0, 1]$. The bandwidth occupied by the raised cosine pulse is:

A. $B = \frac{1}{2T}$ for all $\alpha$  
B. $B = \frac{1+\alpha}{2T}$  
C. $B = \frac{\alpha}{T}$  
D. $B = \frac{1}{T(1 - \alpha)}$

---

**Q7.** In practice, the raised cosine filtering is split equally between the transmitter and receiver using a root raised cosine (RRC) filter. Why is this split used?

A. To reduce the total filter length by half.  
B. The RRC filter at the receiver acts as a matched filter: the cascade of two RRC filters gives the desired raised cosine pulse shape, simultaneously achieving ISI-free sampling and maximising SNR.  
C. The RRC filter at the transmitter limits bandwidth while the RRC filter at the receiver corrects for multipath.  
D. Splitting the filter reduces the peak-to-average power ratio of the transmitted signal.

---

**Q8.** In OFDM, the cyclic prefix (CP) of length $N_{CP}$ is prepended to each OFDM symbol of length $N$. The CP must satisfy $N_{CP} \geq L - 1$, where $L$ is the channel impulse response length in samples. Why?

A. To increase the spectral efficiency of the OFDM system.  
B. So that the linear convolution with the channel is equivalent to circular convolution, preserving subcarrier orthogonality and allowing single-tap equalisation per subcarrier.  
C. To allow the DFT size $N$ to be reduced without affecting subcarrier spacing.  
D. To prevent inter-carrier interference (ICI) caused by frequency offset.

---

**Q9.** The subcarrier spacing in an OFDM system with DFT size $N$ and sampling rate $f_s$ is $\Delta f = f_s / N$. Subcarrier orthogonality over the OFDM symbol period $T_u = N/f_s$ (ignoring the CP) holds because:

A. The subcarriers are spaced apart by more than the coherence bandwidth of the channel.  
B. $\int_0^{T_u} e^{j2\pi k \Delta f\, t}\, e^{-j2\pi l \Delta f\, t}\, dt = 0$ for $k \neq l$, i.e., complex exponentials at integer multiples of $1/T_u$ are orthogonal over $T_u$.  
C. The CP length is chosen to be longer than the channel delay spread.  
D. The IFFT at the transmitter and FFT at the receiver are inverse operations.

---

**Q10.** The peak-to-average power ratio (PAPR) of OFDM is a significant concern because:

A. High PAPR reduces the number of subcarriers that can be transmitted.  
B. High PAPR requires the power amplifier to operate in its linear region over a wide dynamic range; operating near saturation causes non-linear distortion, which spreads energy and increases BER.  
C. PAPR directly determines the subcarrier orthogonality condition.  
D. PAPR cannot exceed 0 dB for OFDM with more than 64 subcarriers.

---

**Q11.** In the worst case, the PAPR of an OFDM signal with $N$ subcarriers of equal amplitude is:

A. $3\ \text{dB}$  
B. $10 \log_{10}(N)\ \text{dB}$  
C. $10 \log_{10}(\sqrt{N})\ \text{dB}$  
D. $0\ \text{dB}$ (PAPR is always 1 for OFDM)

---

**Q12.** A timing synchronisation offset of $\epsilon_t$ samples in an OFDM receiver (without equalisation) causes:

A. A constant amplitude loss across all subcarriers.  
B. A linear phase ramp across subcarriers: subcarrier $k$ experiences a phase rotation of $e^{-j2\pi k \epsilon_t / N}$.  
C. Equal phase rotation on all subcarriers.  
D. Inter-carrier interference only in the middle subcarriers.

---

**Q13.** Carrier frequency offset (CFO) in OFDM destroys subcarrier orthogonality and introduces inter-carrier interference (ICI). A fractional CFO of $\epsilon$ (normalised to subcarrier spacing) causes an ICI power proportional to:

A. $\epsilon$  
B. $\epsilon^2$  
C. $1/\epsilon$  
D. $\epsilon^4$

---

**Q14.** In the context of matched filtering, the output SNR at the sampling instant for a signal of energy $E_s$ in AWGN with noise PSD $N_0/2$ is:

A. $\text{SNR} = \frac{E_s}{N_0}$  
B. $\text{SNR} = \frac{2 E_s}{N_0}$  
C. $\text{SNR} = \frac{E_s}{2 N_0}$  
D. $\text{SNR} = \frac{E_s^2}{N_0}$

---

**Q15.** A pilot-aided frequency offset estimator in an OFDM system computes the phase of the cross-correlation between received pilot subcarriers and known pilot values across two OFDM symbols separated by $\Delta n$ symbols. The maximum unambiguous frequency offset that can be estimated is:

A. $\Delta f_{max} = f_s / N$ (one subcarrier spacing)  
B. $\Delta f_{max} = f_s / (2\Delta n \cdot T_{OFDM})$  
C. $\Delta f_{max} = \Delta n \cdot \Delta f$ (scales with symbol separation)  
D. $\Delta f_{max} = f_s / 2$

---

**Q16.** A communication system uses Gray coding on its QAM constellation. The primary reason is:

A. Gray coding increases the minimum Euclidean distance between constellation points.  
B. Gray coding reduces the BER by ensuring that adjacent constellation points (most likely to be confused by AWGN) differ by only one bit, so symbol errors cause mostly single-bit errors.  
C. Gray coding allows higher-order QAM constellations to operate at lower SNR.  
D. Gray coding is required for OFDM but not for single-carrier modulations.

---

**Q17.** The spectral efficiency (bits/s/Hz) of 64-QAM with a raised cosine roll-off factor $\alpha = 0.25$, assuming ideal coding, is approximately:

A. $6\ \text{bits/s/Hz}$  
B. $4.8\ \text{bits/s/Hz}$  
C. $7.5\ \text{bits/s/Hz}$  
D. $3\ \text{bits/s/Hz}$

---

## Answer Key

| Q | Answer |
|---|--------|
| 1 | B |
| 2 | A |
| 3 | B |
| 4 | B |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | B |
| 10 | B |
| 11 | B |
| 12 | B |
| 13 | B |
| 14 | B |
| 15 | B |
| 16 | B |
| 17 | B |

---

## Detailed Explanations

**Q1 — Answer: B**

For coherent BPSK in AWGN, the two symbols are $\pm\sqrt{E_b}$. After the matched filter, the decision variable is a Gaussian with mean $\pm\sqrt{E_b}$ and variance $N_0/2$. The bit error probability is:

$$P_b = Q\!\left(\frac{\sqrt{E_b}}{\sqrt{N_0/2}}\right) = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

Option A ($Q(\sqrt{E_b/N_0})$) is missing the factor of 2 under the square root, which arises from the double-sided noise variance $N_0/2$. Option C is the error formula for non-coherent FSK or OOK, not BPSK. Option D is dimensionally wrong — the Q function's argument must be normalised to the noise standard deviation.

---

**Q2 — Answer: A**

QPSK uses 4 phase points $\{45°, 135°, 225°, 315°\}$. Each symbol carries 2 bits with $E_s = 2E_b$ (two bits per symbol). The minimum distance is $d_{min} = \sqrt{2E_s} = 2\sqrt{E_b}$ — the same as BPSK when expressed in terms of $E_b$. The BER of QPSK is therefore:

$$P_b = Q\!\left(\sqrt{2E_b/N_0}\right)$$

identical to BPSK. This is why QPSK is so attractive — it doubles spectral efficiency at no BER cost versus BPSK. Options B, C, and D are all incorrect characterisations of the BPSK–QPSK comparison.

---

**Q3 — Answer: B**

16-QAM has $M = 16$ constellation points arranged on a square grid. At the same average symbol energy $E_s$ as QPSK, the 16 points must be packed more tightly, reducing the minimum Euclidean distance $d_{min}$. Since BER $\propto Q(d_{min}/\sqrt{2N_0})$, a smaller $d_{min}$ requires a higher $E_b/N_0$ to achieve the same BER. Specifically, 16-QAM requires about 4 dB more $E_b/N_0$ than QPSK for the same BER. Option A is wrong — average symbol power is a design parameter, not intrinsically different. Option C is true but is not the cause of the BER difference. Option D is false — 16-QAM works in AWGN; phase noise is a concern in practice but not a fundamental limitation.

---

**Q4 — Answer: B**

The matched filter for a known signal $s(t)$ in AWGN with delay $T$ has impulse response $h(t) = s(T - t)$. This is a time-reversed and delayed copy of the transmit pulse. At time $t = T$, the convolution output reaches its maximum, and the output SNR equals $2E_s/N_0$. The delay $T$ is necessary to make the filter causal. Option A ($h(t) = s(t)$) is not a matched filter — it would be the correlator only if $s(t)$ happened to be its own time-reverse. Option C ($h(t) = s(-t)$) is time-reversed but non-causal. Option D (inverse filter) is unrelated to matched filtering and would amplify noise at frequencies where $S(f)$ is small.

---

**Q5 — Answer: B**

The Nyquist ISI criterion in the time domain states: a pulse $p(t)$ with symbol period $T$ is ISI-free at sampling instants if $p(nT) = \delta[n]$ — i.e., it equals 1 at $n = 0$ and exactly 0 at all other integer multiples of $T$. In the frequency domain, this is equivalent to the Nyquist condition: $\sum_k P(f - k/T) = T$ (constant for all $f$). Option A is the Nyquist bandwidth condition (minimum bandwidth) but is too restrictive — ISI-free pulses can have bandwidth exceeding $1/(2T)$ with roll-off. Option C is a decay condition (related to convergence of the ISI sum) but not the defining criterion. Option D describes a specific sub-class of ISI-free pulses, not the general condition.

---

**Q6 — Answer: B**

The raised cosine spectrum is:

$$P(f) = \begin{cases} T & |f| \leq \frac{1-\alpha}{2T} \\ \frac{T}{2}\left[1 + \cos\!\left(\frac{\pi T}{\alpha}\left(|f| - \frac{1-\alpha}{2T}\right)\right)\right] & \frac{1-\alpha}{2T} \leq |f| \leq \frac{1+\alpha}{2T} \\ 0 & |f| > \frac{1+\alpha}{2T} \end{cases}$$

The spectrum extends to zero at $|f| = (1+\alpha)/(2T)$, so the two-sided bandwidth is $(1+\alpha)/T$ and the one-sided (positive frequency) bandwidth is $B = (1+\alpha)/(2T)$. For $\alpha = 0$ (sinc pulse, minimum bandwidth): $B = 1/(2T)$. For $\alpha = 1$ (maximum roll-off): $B = 1/T$. Option A is only correct for $\alpha = 0$. Options C and D do not match the formula.

---

**Q7 — Answer: B**

The root raised cosine (RRC) filter has frequency response $\sqrt{P(f)}$ where $P(f)$ is the raised cosine spectrum. When the transmitter applies an RRC filter and the receiver applies an identical RRC filter, the cascade response is $\sqrt{P(f)} \times \sqrt{P(f)} = P(f)$ — the full raised cosine pulse shape, satisfying the Nyquist ISI criterion. Simultaneously, the receiver RRC filter is matched to the transmitted (RRC-shaped) pulse, maximising SNR according to matched filter theory. This elegant split achieves both goals with one filter per end. Option A is wrong — the total filter order is the same. Option C is wrong — the RRC filter does not correct multipath. Option D is wrong — the RRC split does not inherently reduce PAPR.

---

**Q8 — Answer: B**

OFDM uses the DFT, which assumes circular convolution. The actual channel introduces linear convolution with the received signal. By prepending a CP of length $\geq L - 1$ (the channel order), the linear convolution between the transmitted OFDM symbol and the channel impulse response produces the same result as a circular convolution over the $N$-point symbol block — provided the CP is discarded at the receiver before the DFT. This makes the channel appear as a diagonal matrix in the DFT domain, allowing single-tap equalisation (just a complex division) per subcarrier. Option A is wrong — CP reduces spectral efficiency. Option C is wrong — $N$ and subcarrier spacing are independent of CP. Option D is wrong — ICI from frequency offset is a separate issue; CP addresses ISI from multipath.

---

**Q9 — Answer: B**

The OFDM subcarriers are complex exponentials $e^{j2\pi k \Delta f\, t}$ for $k = 0, 1, \ldots, N-1$ with $\Delta f = 1/T_u$. Their inner product over $[0, T_u]$ is:

$$\int_0^{T_u} e^{j2\pi k \Delta f\, t} \cdot e^{-j2\pi l \Delta f\, t}\, dt = \int_0^{T_u} e^{j2\pi (k-l)/T_u\, t}\, dt = T_u \cdot \delta[k - l]$$

For $k \neq l$, the integrand completes an integer number of cycles and integrates to zero. This is the mathematical basis of OFDM orthogonality. Option A is a channel property (relevant to frequency-flat fading per subcarrier), not the definition of subcarrier orthogonality. Option C is the CP requirement (addresses ISI). Option D is a true statement but does not explain why orthogonality holds.

---

**Q10 — Answer: B**

An OFDM signal is the sum of $N$ independently modulated subcarriers. By the central limit theorem, for large $N$ the envelope of the OFDM signal approaches a Gaussian distribution, which has a high peak-to-mean ratio — the PAPR can be as high as $10\log_{10}(N)$ dB. Power amplifiers (PAs) are typically designed to operate near their 1 dB compression point for efficiency. High PAPR requires the PA to have a large back-off from saturation, greatly reducing power efficiency, or to accept non-linear distortion (clipping) that introduces out-of-band radiation and in-band BER degradation. Option A is wrong — PAPR has no direct effect on subcarrier count. Option C is wrong — PAPR and orthogonality are independent. Option D is obviously false.

---

**Q11 — Answer: B ($10\log_{10}(N)\ \text{dB}$)**

In the worst case (all $N$ subcarriers align in phase at a single instant), the OFDM signal amplitude reaches $N$ times the amplitude of a single subcarrier. The average amplitude is proportional to $\sqrt{N}$ (root-mean-square sum of $N$ equal-amplitude phasors). Therefore:

$$\text{PAPR}_{max} = \frac{N^2\text{(peak power)}}{N \cdot \bar{P}} = N$$

In dB: $10\log_{10}(N)$. For $N = 64$, this is 18 dB; for $N = 1024$, 30 dB. In practice, PAPR is a statistical measure (e.g., 99.9th percentile) and is lower, but the worst case is $N$. Option A (3 dB) would apply to a two-subcarrier OFDM system. Option C has $\sqrt{N}$ which is 5 dB for $N = 10$, too low. Option D is false for any $N > 1$.

---

**Q12 — Answer: B**

A timing offset of $\epsilon_t$ samples shifts the received sequence, so the DFT at the receiver sees:

$$\tilde{x}[n] = x[n - \epsilon_t] \xrightarrow{\text{DFT}} X[k]\, e^{-j2\pi k \epsilon_t / N}$$

This is a linear phase ramp — subcarrier $k$ receives a phase rotation of $-2\pi k \epsilon_t / N$. For a small timing offset within the CP, this phase ramp can be compensated by channel equalisation (it appears as part of the effective channel phase). For larger offsets or offsets outside the CP, ISI/ICI appears. Option A is wrong — timing offset rotates, not scales. Option C (equal phase on all subcarriers) would arise from a common phase error, not a timing offset. Option D is incorrect — timing offset affects all subcarriers with a frequency-dependent phase.

---

**Q13 — Answer: B ($\epsilon^2$)**

For a small fractional CFO $\epsilon$ (normalised to subcarrier spacing $\Delta f$), the ICI power in the $k$th subcarrier from all other subcarriers grows as $\epsilon^2$ for small $\epsilon$. The signal-to-interference ratio due to CFO is approximately $\text{SIR} \approx 3/(\pi^2 \epsilon^2)$ for large $N$. This quadratic dependence means that halving the CFO reduces ICI power by 6 dB. In practice, CFO of even a few percent of $\Delta f$ causes significant performance degradation. Option A (linear) would correspond to amplitude effects, not ICI power. Options C and D are not consistent with the Taylor expansion of the sinc-like ICI coefficient.

---

**Q14 — Answer: B ($2E_s/N_0$)**

The matched filter theorem states that the maximum output SNR for a deterministic signal $s(t)$ with energy $E_s$ in AWGN with noise PSD $N_0/2$ (two-sided) is:

$$\text{SNR}_{max} = \frac{2E_s}{N_0}$$

This result is independent of the pulse shape. For BPSK with $E_s = E_b$: $\text{SNR} = 2E_b/N_0$, which leads to $P_b = Q(\sqrt{2E_b/N_0})$. Option A omits the factor of 2. Option C has an extra factor of 2 in the denominator. Option D squares the energy, which is dimensionally incorrect.

---

**Q15 — Answer: B**

A time-domain pilot phase estimator measures the phase difference $\Delta\phi = 2\pi\epsilon_f T_{OFDM}\Delta n$ between OFDM symbols separated by $\Delta n$ symbol periods, where $\epsilon_f$ is the frequency offset and $T_{OFDM}$ is the total OFDM symbol duration (including CP). Since $\Delta\phi$ is measured modulo $2\pi$, the maximum unambiguous frequency offset is when $|\Delta\phi| < \pi$:

$$|\epsilon_f| < \frac{1}{2\Delta n\, T_{OFDM}}$$

For $\Delta n = 1$, this is $\pm 1$ subcarrier spacing (half of $1/T_{OFDM} = \Delta f$, but including both sides). Option A is the subcarrier spacing itself (the unambiguous range for one-symbol estimates). Option C incorrectly scales with $\Delta n$ in the wrong direction. Option D ($f_s/2$) is the Nyquist limit for the baseband signal, unrelated to CFO estimation range.

---

**Q16 — Answer: B**

Gray coding (also called reflected binary coding) assigns bit labels to constellation points such that nearest neighbours in the constellation differ by exactly one bit. For QAM, where AWGN causes errors primarily to adjacent symbols, this means that most symbol errors result in only one wrong bit rather than multiple bits. For large constellations like 64-QAM, this reduces the BER approximately by a factor equal to the number of bits per symbol relative to worst-case binary coding. Option A is wrong — Gray coding changes the bit labelling, not the geometric arrangement of points. Option C is wrong — coding gain requires channel coding, not just mapping. Option D is wrong — Gray coding is used in all multi-amplitude modulations.

---

**Q17 — Answer: B (4.8 bits/s/Hz)**

64-QAM carries $\log_2(64) = 6$ bits per symbol. With a raised cosine filter of roll-off $\alpha = 0.25$, the occupied bandwidth is $B = (1+\alpha)/T = 1.25/T$ Hz (one-sided) or $1.25 R_s$ total, where $R_s = 1/T$ is the symbol rate. The spectral efficiency in bits/s per Hz of total bandwidth is:

$$\eta = \frac{6 \text{ bits/symbol} \times R_s}{1.25 \times R_s} = \frac{6}{1.25} = 4.8\ \text{bits/s/Hz}$$

Option A (6 bits/s/Hz) would apply only with $\alpha = 0$ (ideal Nyquist sinc pulse, infinite in time and impossible in practice). Option C (7.5 bits/s/Hz) would require $\alpha = -0.2$, which is physically meaningless. Option D (3 bits/s/Hz) corresponds to 8-PSK or 8-QAM, not 64-QAM.
