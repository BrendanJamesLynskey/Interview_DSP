# Digital Modulation and Demodulation — Interview Questions

## Overview

Digital modulation maps bit streams onto physical waveforms for transmission. This topic appears in virtually every communications or RF systems role. Interviewers test both theoretical understanding (BER derivations, constellation geometry) and practical intuition (trade-offs between spectral efficiency and robustness).

---

## Tier 1: Fundamentals

### Q1. What is digital modulation, and why is it necessary?

**Answer:**

Digital modulation is the process of mapping a sequence of discrete symbols (derived from bits) onto a continuous-time waveform suitable for transmission over a physical channel. It is necessary for three reasons:

1. **Frequency translation**: Baseband signals must be shifted to a carrier frequency appropriate for the transmission medium (antenna size, channel bandwidth allocation).
2. **Bandwidth efficiency**: Modulation schemes determine how many bits are packed into each Hz of bandwidth (spectral efficiency in bits/s/Hz).
3. **Channel matching**: Different modulation schemes offer different robustness vs. efficiency trade-offs matched to channel conditions.

The general passband signal is:

$$s(t) = \text{Re}\!\left[\tilde{s}(t)\, e^{j2\pi f_c t}\right]$$

where $\tilde{s}(t)$ is the complex baseband (lowpass equivalent) signal and $f_c$ is the carrier frequency.

---

### Q2. Describe BPSK. What is the constellation diagram and how are bits mapped?

**Answer:**

Binary Phase Shift Keying (BPSK) maps one bit per symbol using two phase states separated by 180°.

**Constellation:** Two points on the real axis:
- Bit 0 maps to symbol $-\sqrt{E_s}$ (phase $\pi$)
- Bit 1 maps to symbol $+\sqrt{E_s}$ (phase $0$)

where $E_s$ is the symbol energy.

**Modulated signal:**

$$s(t) = A_c \cdot d(t) \cdot \cos(2\pi f_c t)$$

where $d(t) \in \{-1, +1\}$ is the NRZ data signal.

**Key properties:**
- Spectral efficiency: 1 bit/symbol
- Only the in-phase component carries data; quadrature is unused
- Maximum Euclidean distance between constellation points: $2\sqrt{E_s}$
- Most robust of all PSK/QAM schemes at a given $E_b/N_0$

**Decision rule:** After coherent demodulation, decide $+1$ if the real part of the received sample is positive, $-1$ otherwise. The decision boundary is the imaginary axis (zero crossing).

---

### Q3. How does QPSK extend BPSK? What is the spectral efficiency improvement?

**Answer:**

QPSK (Quadrature Phase Shift Keying) uses four phase states (45°, 135°, 225°, 315°), transmitting **2 bits per symbol**. The two bits are mapped independently onto the in-phase (I) and quadrature (Q) branches.

**Constellation (Gray-coded):**

| Bits (b1 b0) | Phase | I | Q |
|---|---|---|---|
| 00 | 45° | $+1/\sqrt{2}$ | $+1/\sqrt{2}$ |
| 01 | 135° | $-1/\sqrt{2}$ | $+1/\sqrt{2}$ |
| 11 | 225° | $-1/\sqrt{2}$ | $-1/\sqrt{2}$ |
| 10 | 315° | $+1/\sqrt{2}$ | $-1/\sqrt{2}$ |

**Spectral efficiency:** QPSK transmits 2 bits/symbol. For the same bit rate $R_b$, QPSK uses **half the bandwidth** of BPSK because $B \propto R_b / \log_2 M$.

**BER equivalence:** QPSK has the same BER vs. $E_b/N_0$ as BPSK when Gray coding is used, because the I and Q branches are independent BPSK systems. Doubling spectral efficiency comes free in AWGN — this is the key insight.

**Common mistake:** Confusing symbol energy $E_s$ and bit energy $E_b$. For QPSK, $E_s = 2 E_b$.

---

### Q4. What is a constellation diagram? What information does it convey?

**Answer:**

A constellation diagram is a 2D scatter plot representing modulated symbols in the complex baseband plane. The horizontal axis is the in-phase (I) component and the vertical axis is the quadrature (Q) component.

**What it shows:**

1. **Ideal symbol positions**: The noiseless transmitted symbols as labelled points.
2. **Decision regions**: The boundaries (Voronoi regions) partitioning the plane — a received point is decoded as the symbol whose region it falls in.
3. **Euclidean distance**: The spacing between points determines noise immunity. Larger minimum distance gives better BER at a given SNR.
4. **Received cloud**: When actual received symbols are overlaid, the spread indicates SNR, phase noise, and IQ imbalance.

**Diagnosing impairments from the constellation:**
- Circular spread around ideal points → additive noise dominated
- Rotation of all points → carrier phase error
- Unequal I/Q spread → IQ gain imbalance
- Curved distortion of outer points → amplifier non-linearity (AM-AM compression)

---

### Q5. What is the difference between coherent and non-coherent detection?

**Answer:**

**Coherent detection** requires knowledge of the carrier's exact phase at the receiver. The receiver multiplies the incoming signal by a locally generated carrier replica (from a PLL or pilot tones) to extract baseband I and Q components. This gives optimal performance but requires synchronisation circuitry.

**Non-coherent detection** does not require carrier phase recovery. Instead it uses envelope or energy detection. Examples include:
- DPSK: detects phase *differences* between consecutive symbols
- FSK with envelope detection: detects which frequency has more energy in the symbol interval

**Performance comparison:**

| Scheme | BER expression |
|---|---|
| Coherent BPSK | $Q\!\left(\sqrt{2E_b/N_0}\right)$ |
| Non-coherent DPSK | $\frac{1}{2}e^{-E_b/N_0}$ |

Non-coherent detection incurs a penalty of roughly 1–3 dB, depending on SNR. At high SNR the gap narrows because phase estimation improves.

**When to prefer non-coherent:**
- Low-complexity receivers (IoT, burst-mode links where re-synchronisation overhead is costly)
- Very short packets where pilot overhead would consume a significant fraction of the frame
- High-mobility scenarios where rapid phase changes make coherent tracking unreliable

---

## Tier 2: Intermediate

### Q6. Derive the BER for BPSK in AWGN.

**Answer:**

**Setup:** Transmit $s_1 = +\sqrt{E_b}$ or $s_0 = -\sqrt{E_b}$ (after matched filtering and sampling at the optimal time). The received sample is:

$$r = s_i + n, \quad n \sim \mathcal{N}(0,\, N_0/2)$$

**Decision rule:** Decide $s_1$ if $r > 0$, else decide $s_0$.

**Probability of error given $s_1$ transmitted:**

$$P_e = P(r < 0 \mid s_1) = P\!\left(\sqrt{E_b} + n < 0\right) = P\!\left(n < -\sqrt{E_b}\right)$$

Normalising by the noise standard deviation $\sigma = \sqrt{N_0/2}$:

$$P_e = P\!\left(\frac{n}{\sqrt{N_0/2}} < -\sqrt{\frac{2E_b}{N_0}}\right) = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

where the Q-function is defined as:

$$Q(x) = \frac{1}{\sqrt{2\pi}} \int_x^{\infty} e^{-t^2/2}\, dt$$

By symmetry the error probability for $s_0$ is identical, so:

$$\boxed{P_b^{\text{BPSK}} = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)}$$

**Numerical example:** At $E_b/N_0 = 10$ dB (linear ratio = 10):
$$P_b = Q\!\left(\sqrt{20}\right) = Q(4.47) \approx 3.9 \times 10^{-6}$$

**Physical interpretation:** The Q-function argument is the SNR measured in noise standard deviations. Increasing $E_b$ moves the two symbols further apart; the probability of the noise crossing the decision boundary falls exponentially.

---

### Q7. Compare the spectral efficiency and BER performance of BPSK, QPSK, 16-QAM, and 64-QAM.

**Answer:**

| Modulation | Bits/symbol | Spectral efficiency | Required $E_b/N_0$ at BER $= 10^{-6}$ |
|---|---|---|---|
| BPSK | 1 | 1 bit/s/Hz | ~10.5 dB |
| QPSK | 2 | 2 bit/s/Hz | ~10.5 dB |
| 16-QAM | 4 | 4 bit/s/Hz | ~14.4 dB |
| 64-QAM | 6 | 6 bit/s/Hz | ~18.8 dB |

**BER approximation for square M-QAM (Gray coded):**

$$P_b \approx \frac{4}{\log_2 M}\left(1 - \frac{1}{\sqrt{M}}\right) Q\!\left(\sqrt{\frac{3\log_2 M}{M-1}\cdot\frac{2E_b}{N_0}}\right)$$

**Key insight:** Each step up in constellation order doubles spectral efficiency but requires approximately 4–6 dB more SNR for the same BER. This fundamental trade-off drives adaptive modulation (AMC) in LTE, Wi-Fi, and 5G NR, where the system continuously selects the highest feasible order.

**Common mistake:** Claiming QPSK always outperforms 16-QAM. At sufficiently high SNR, higher-order modulation is always preferred for throughput. The choice is always conditioned on the available link budget.

---

### Q8. What is a matched filter and why is it optimal for symbol detection?

**Answer:**

A matched filter (MF) is a linear filter whose impulse response is a time-reversed, conjugated copy of the transmitted pulse:

$$h_{\text{MF}}(t) = s^*(T_s - t)$$

where $s(t)$ is the transmit pulse and $T_s$ is the symbol period.

**Optimality proof (AWGN):** The received signal is $r(t) = s(t) + n(t)$. Passing through filter $h(t)$ and sampling at $T_s$, the output SNR is:

$$\text{SNR}_\text{out} = \frac{\left|\int s(t) h(T_s - t)\, dt\right|^2}{\frac{N_0}{2}\int |h(t)|^2\, dt}$$

By the Cauchy-Schwarz inequality, this is maximised when $h(t) = s^*(T_s - t)$, giving:

$$\text{SNR}_\text{max} = \frac{2E_s}{N_0}$$

where $E_s = \int |s(t)|^2\, dt$.

**Equivalence to correlator:** Matched filtering followed by sampling is mathematically equivalent to computing the correlator output $\int r(t) s^*(t)\, dt$. Both forms appear in textbooks and are interchangeable.

**Practical split:** In real systems the matched filter pair is split between transmitter and receiver — each uses a Root Raised Cosine (RRC) filter so the combined Tx/Rx response achieves the raised cosine Nyquist zero-ISI criterion.

---

### Q9. Explain decision regions. How do they change for different constellation sizes?

**Answer:**

Decision regions are partitions of the received signal space. For AWGN channels with equally likely symbols, the maximum likelihood (ML) detector assigns the received point $\mathbf{r}$ to the nearest constellation point:

$$\hat{m} = \arg\min_i \|\mathbf{r} - \mathbf{s}_i\|^2$$

The decision boundaries are the **perpendicular bisectors** between nearest-neighbour pairs (Voronoi tessellation).

**How regions vary by constellation:**

- **BPSK**: One boundary — the imaginary axis divides the plane into two half-planes.
- **QPSK**: Two orthogonal boundaries forming four quadrants.
- **16-QAM**: A 3×3 grid of straight-line boundaries (each axis has 3 thresholds for 4 levels).
- **8-PSK**: Eight angular "pie-slice" regions meeting at the origin.

**Corner and edge effects in QAM:** Corner points have only 2 nearest neighbours (two error directions), while interior points have 4. Corner points also carry higher energy. As $M$ increases, the proportion of interior points grows and the average number of nearest neighbours approaches 4.

**Non-AWGN channels:** Under fading or coloured noise, ML boundaries are no longer linear Voronoi lines. In practice, soft-output demodulation (LLR computation) is used rather than hard decisions, feeding turbo or LDPC decoders.

---

### Q10. What is Gray coding and why is it used in QAM constellations?

**Answer:**

Gray coding assigns bit labels to constellation symbols such that adjacent symbols (nearest neighbours most likely to be confused in noise) differ in **exactly one bit**.

**QPSK example:** Labelling the four quadrants 00, 01, 11, 10 (counter-clockwise) means any single-symbol error moves the receiver to an adjacent quadrant, flipping exactly 1 of the 2 bits.

**BER benefit:** With Gray coding:

$$P_b \approx \frac{P_s}{\log_2 M}$$

Without Gray coding a single symbol error may flip up to $\log_2 M$ bits, worsening BER by up to a factor of $\log_2 M / 2$.

**Quantitative 16-QAM example:** A symbol error to an adjacent symbol flips 1 of 4 bits with Gray coding versus potentially 2–4 bits without it. At $E_b/N_0 = 14$ dB where 16-QAM SER $\approx 2 \times 10^{-4}$, Gray coding keeps BER near $5 \times 10^{-5}$, whereas non-Gray labelling could give BER $\approx 2 \times 10^{-4}$.

**Limitation:** Gray coding is most important for hard-decision receivers. When an outer FEC codec receives soft LLR values, the exact bit labelling matters less because the codec exploits the full symbol geometry.

---

## Tier 3: Advanced

### Q11. Derive the BER for 16-QAM in AWGN and compare to QPSK at the same $E_b/N_0$.

**Answer:**

**16-QAM as two independent PAM-4 streams:** A square 16-QAM constellation can be decomposed into two independent 4-level PAM signals on the I and Q axes. Each PAM-4 stream carries 2 bits with levels $\{-3d, -d, +d, +3d\}$ where $d$ is the half-minimum-distance.

**Normalise to average symbol energy:**

$$E_s = \frac{1}{4}(d^2 + d^2 + 9d^2 + 9d^2) \times 2 = 10d^2 \quad \Rightarrow \quad d = \sqrt{E_s/10}$$

Since $E_s = 4E_b$:

$$d = \sqrt{\frac{4E_b}{10}} = \sqrt{\frac{2E_b}{5}}$$

**BER for one PAM-4 branch (Gray coded):** The two inner levels have one adjacent neighbour on each side; the two outer levels have one. The nearest-neighbour distance is $2d$ in all cases. Integrating over the four levels:

$$P_b^{\text{PAM-4}} = \frac{3}{4} Q\!\left(\frac{d}{\sigma}\right) + \frac{1}{4} Q\!\left(\frac{d}{\sigma}\right) \cdot 2 - ...$$

The clean standard result is:

$$P_b^{\text{PAM-4}} = \frac{3}{4} Q\!\left(\sqrt{\frac{4}{5}\cdot\frac{2E_b}{N_0}}\right)$$

Since the 16-QAM BER is the average of two independent PAM-4 branches:

$$\boxed{P_b^{16\text{-QAM}} \approx \frac{3}{4} Q\!\left(\sqrt{\frac{8E_b}{5N_0}}\right)}$$

**Comparison at BER $= 10^{-6}$:**

| Scheme | Required $E_b/N_0$ |
|---|---|
| BPSK / QPSK | ~10.5 dB |
| 16-QAM | ~14.4 dB |

The **~3.9 dB penalty** of 16-QAM arises because packing 4× the symbols into the same average power compresses the minimum distance from $2\sqrt{E_b}$ (BPSK) to $2\sqrt{2E_b/5}$ (16-QAM).

---

### Q12. Explain performance degradation of QAM in Rayleigh fading and describe mitigation techniques.

**Answer:**

In AWGN the received SNR is deterministic and BER vs. $E_b/N_0$ follows smooth Q-function curves. In a **Rayleigh fading channel**, the received amplitude $\alpha$ is random:

$$f_\alpha(\alpha) = \frac{\alpha}{\sigma^2} e^{-\alpha^2/(2\sigma^2)}, \quad \alpha \geq 0$$

The instantaneous SNR $\gamma = \alpha^2 E_b / N_0$ is exponentially distributed with mean $\bar{\gamma} = E_b/N_0$.

**BER in Rayleigh fading (BPSK, exact closed form):**

$$P_b = \int_0^\infty Q\!\left(\sqrt{2\gamma}\right) f_\gamma(\gamma)\, d\gamma = \frac{1}{2}\!\left(1 - \sqrt{\frac{\bar{\gamma}}{1+\bar{\gamma}}}\right) \approx \frac{1}{4\bar{\gamma}} \quad \text{for large } \bar{\gamma}$$

The BER falls off as $1/\bar{\gamma}$ (inverse linear in SNR) versus exponentially in AWGN. This is a catastrophic degradation — to achieve BER $10^{-5}$ requires roughly 37 dB in Rayleigh fading versus 10.5 dB in AWGN.

**Mitigation techniques:**

| Technique | Mechanism | Diversity order |
|---|---|---|
| Receive antenna diversity (MRC) | Average over $L$ independent fades | $L$ |
| Transmit diversity (Alamouti) | Space-time coding over 2 antennas | 2 |
| OFDM + interleaving + coding | Exploit frequency diversity | Up to $N_c$ subcarriers |
| RAKE receiver (CDMA) | Combine multipath components coherently | Number of paths |
| Adaptive modulation (AMC) | Drop to BPSK/QPSK in deep fades | 1 (reduces outage) |

With diversity order $L$, the high-SNR BER scales as $\bar{\gamma}^{-L}$, recovering exponential-like behaviour for large $L$.

---

### Q13. What is the distinction between $E_s$ and $E_b$? Why does this matter when comparing modulation schemes?

**Answer:**

$$E_s = \text{average energy per transmitted symbol (in Joules)}$$
$$E_b = \frac{E_s}{\log_2 M} = \text{average energy per information bit}$$

**Why $E_b/N_0$ is the fair comparator:**

When comparing BPSK (1 bit/symbol) to 16-QAM (4 bits/symbol) at the same symbol rate, the two systems deliver different bit rates. Using $E_s/N_0$ disadvantages lower-order modulations artificially. The figure of merit $E_b/N_0$ normalises by information content and enables a fair Shannon-capacity comparison.

**Numerical example** (all at same $E_s$, same symbol rate):

| Scheme | $\log_2 M$ | $E_b = E_s/\log_2 M$ | Shift $E_b/N_0$ vs. $E_s/N_0$ |
|---|---|---|---|
| BPSK | 1 | $E_s$ | 0 dB |
| QPSK | 2 | $E_s/2$ | $-3$ dB |
| 16-QAM | 4 | $E_s/4$ | $-6$ dB |
| 64-QAM | 6 | $E_s/6$ | $-7.8$ dB |

**Key consequence:** On an $E_b/N_0$ axis, BPSK and QPSK have identical BER curves, but 16-QAM is shifted right by ~4 dB. This rightward shift is the real cost of higher spectral efficiency and determines the SNR required to enable a given modulation order on the link.

---

### Q14. Describe the impact of phase noise and IQ imbalance on QAM. How are they estimated and corrected?

**Answer:**

**Phase noise:** Random carrier phase fluctuation modelled as a Wiener process:

$$\phi(t) = \int_0^t \xi(\tau)\, d\tau, \quad \xi(t) \sim \mathcal{N}(0, 4\pi\Delta f)$$

where $\Delta f$ is the oscillator linewidth (3 dB bandwidth of the Lorentzian PSD). Phase noise rotates the entire constellation by a slowly varying angle, causing symbol smearing in the phase direction. For high-order QAM (64-QAM, 256-QAM) with tightly packed phase states, this is a primary performance limiter.

Requirement for negligible impairment: $\Delta f \cdot T_s \ll 10^{-3}$ (rule of thumb).

**IQ imbalance:** Amplitude and phase mismatch between I and Q branches:

The received complex symbol $\tilde{r}$ relates to the transmitted $\tilde{s}$ by:

$$\tilde{r} = \alpha_1 \tilde{s} + \alpha_2 \tilde{s}^*$$

where $\alpha_1, \alpha_2$ depend on the gain imbalance $\epsilon$ and phase skew $\phi_{iq}$. The $\tilde{s}^*$ term is the **image** component and causes cross-coupling between I and Q, visually distorting the constellation by shearing and compressing it.

**Estimation and correction:**

| Impairment | Estimation method | Correction |
|---|---|---|
| Phase noise | Data-aided PLL on pilots; blind CPE using constellation rotational symmetry | Phase rotator: multiply by $e^{-j\hat{\phi}}$ |
| IQ gain imbalance | Compare variance of I vs. Q in a training burst | Scale the higher-power branch by $1/(1+\epsilon)$ |
| IQ phase skew | Measure cross-correlation $\mathbb{E}[I \cdot Q]$ in training | Gram-Schmidt orthogonalisation |

Modern chip designs handle all three jointly via a digital front-end calibration block running at start-up and periodically thereafter.

---

### Q15. A link has $E_b/N_0 = 15$ dB and must achieve BER $\leq 10^{-5}$ in AWGN. Which modulation orders are feasible and what is the maximum spectral efficiency achievable?

**Answer:**

**Convert:** $E_b/N_0 = 15$ dB $\Rightarrow$ linear ratio $= 31.6$.

**BPSK/QPSK** (requirement: $Q(\sqrt{2x}) = 10^{-5}$):
$\sqrt{2x} \approx 4.42 \Rightarrow x \approx 9.8$ (9.9 dB). **Feasible — 5.1 dB margin.**

**16-QAM** (approximation $P_b \approx \frac{3}{4}Q(\sqrt{1.6 \cdot 2E_b/N_0})$):
Requires $E_b/N_0 \approx 13.4$ dB. **Feasible — 1.6 dB margin.**

**64-QAM** (approximation $P_b \approx \frac{7}{12}Q(\sqrt{(6/7) \cdot 2E_b/N_0})$):
Requires $E_b/N_0 \approx 17.8$ dB. **Not feasible — 2.8 dB short.**

**Summary:**

| Scheme | Required $E_b/N_0$ | Feasible? | Spectral efficiency |
|---|---|---|---|
| BPSK | 9.9 dB | Yes (5.1 dB margin) | 1 bit/s/Hz |
| QPSK | 9.9 dB | Yes (5.1 dB margin) | 2 bit/s/Hz |
| 16-QAM | 13.4 dB | Yes (1.6 dB margin) | 4 bit/s/Hz |
| 64-QAM | 17.8 dB | No | 6 bit/s/Hz |

**Recommendation:** 16-QAM maximises spectral efficiency within the constraint. The 1.6 dB margin is modest; if the channel has any fading or implementation loss, QPSK may be safer.

**With coding:** A rate-3/4 turbo or LDPC code applied to 64-QAM provides approximately 5–6 dB of coding gain at BER $10^{-5}$, bringing the effective requirement down to ~12–13 dB. The coded 64-QAM at rate 3/4 achieves net efficiency $6 \times 0.75 = 4.5$ bit/s/Hz, marginally outperforming uncoded 16-QAM — which is exactly the trade-off that adaptive coded modulation systems exploit.

---

## Common Interview Mistakes

1. **Confusing $E_b/N_0$ and $E_s/N_0$**: Always clarify which is being used before comparing schemes across modulation orders.
2. **Ignoring Gray coding**: Standard BER/SER formulas assume Gray coding. Without it, BER can be several times worse.
3. **Defaulting to AWGN**: Real channels have fading, Doppler, phase noise, and non-linearity. Ask about the channel model before quoting numbers.
4. **Forgetting spectral efficiency corrections**: "1 bit/s/Hz for BPSK" assumes ideal Nyquist pulse shaping. A practical roll-off factor of 0.35 reduces efficiency to $1/1.35 \approx 0.74$ bit/s/Hz.
5. **Misplacing the matched filter**: The matched filter is at the receiver. The transmit filter is the pulse shaping filter (root raised cosine). The combined Tx+Rx response forms the full raised cosine.
