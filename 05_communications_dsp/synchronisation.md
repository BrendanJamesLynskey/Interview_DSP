# Synchronisation — Interview Questions

## Overview

Synchronisation is the process of aligning the receiver's timing, frequency, and phase references with the transmitter's. Without synchronisation, even a perfect channel would yield catastrophic BER. This topic tests understanding of PLLs, timing recovery, frame acquisition, and practical algorithms like Schmidl-Cox. It is essential for modem, RF, and baseband ASIC roles.

---

## Tier 1: Fundamentals

### Q1. Why is synchronisation critical in a digital communications receiver? What are the main types?

**Answer:**

A digital receiver must recover three reference signals before demodulation can begin:

**1. Symbol timing synchronisation (timing recovery):**
Aligns the receiver's sampling clock with the optimal sampling instants (peak of the pulse, zero ISI point). A timing error of even 5–10% of $T_s$ causes significant ISI and SNR degradation.

**2. Carrier frequency synchronisation:**
Removes the carrier frequency offset (CFO) between transmitter and receiver oscillators. Even a small offset causes the received constellation to rotate continuously, making coherent demodulation impossible. CFO also causes ICI in OFDM.

**3. Carrier phase synchronisation:**
After frequency acquisition, the residual phase offset must be estimated and removed. A fixed phase offset rotates the entire constellation by a constant angle, leading to decision errors in QAM.

**4. Frame/packet synchronisation:**
Determines the start of a data packet or frame within the received bit stream. Without this, the receiver does not know where symbols or coded blocks begin.

**Performance requirements (typical):**
- Timing: $|\epsilon| < 0.05 T_s$ for QAM systems
- Frequency: $|\delta f| < 0.01 \Delta f$ for OFDM; $< 100$ Hz for narrowband coherent PSK
- Phase: $|\phi| < 5°$–$10°$ for 16-QAM; $< 2°$ for 64-QAM

---

### Q2. What is a Phase-Locked Loop (PLL)? Describe its operation in carrier recovery.

**Answer:**

A PLL is a feedback control system that locks the phase (and hence frequency) of a locally generated oscillator to a reference signal.

**Block diagram components:**
1. **Phase Detector (PD)**: Computes the phase error $e(t) = \phi_{in}(t) - \phi_{VCO}(t)$
2. **Loop Filter (LF)**: Filters the phase error signal to reduce noise. For a second-order PLL, typically a proportional-integral (PI) filter: $F(s) = K_p + K_i/s$
3. **Voltage-Controlled Oscillator (VCO)**: Generates a sinusoid whose frequency is proportional to the input voltage: $\phi_{VCO}(t) = \int K_{VCO} v(t)\, dt$

**Loop equation (linearised model):**

$$\frac{\phi_{out}(s)}{\phi_{in}(s)} = \frac{K_{PD} K_{VCO} F(s)/s}{1 + K_{PD} K_{VCO} F(s)/s}$$

This is a closed-loop transfer function with loop bandwidth $B_L$ determined by $K_{PD}$, $K_{VCO}$, and filter gains.

**Trade-off in loop bandwidth $B_L$:**
- Wide $B_L$: Fast acquisition, tracks rapid phase/frequency changes, but more noise passes through (more phase jitter)
- Narrow $B_L$: Low phase jitter, high noise rejection, but slow acquisition and cannot track Doppler

**Digital PLL implementation:** In digital receivers, the PLL is implemented as a discrete-time loop with a numerically controlled oscillator (NCO) replacing the VCO, and a digital loop filter. The NCO accumulates phase increments computed by the loop.

---

### Q3. What is carrier frequency offset (CFO) and what are its causes?

**Answer:**

Carrier frequency offset is the difference between the transmitter's carrier frequency $f_{TX}$ and the receiver's local oscillator frequency $f_{RX}$:

$$\delta f = f_{TX} - f_{RX}$$

**Causes:**

1. **Crystal oscillator tolerance**: Oscillators have a specified frequency accuracy in parts per million (ppm). A 10 ppm tolerance at 2.4 GHz gives $\delta f$ up to $\pm 24$ kHz. Two devices each with 10 ppm tolerance could have a relative offset of 48 kHz.

2. **Temperature drift**: Crystal frequency varies with temperature (typically $\pm 2$–$5$ ppm/$°C$).

3. **Doppler shift**: A mobile transmitter or receiver moving at velocity $v$ relative to the line of sight causes:
   $$f_D = \frac{v}{c} f_c$$
   At 2.4 GHz with $v = 30$ m/s (car): $f_D = 240$ Hz. At 28 GHz (5G mmWave) with $v = 100$ km/h: $f_D \approx 2.6$ kHz.

4. **Phase noise**: Short-term frequency instability (random Doppler spreading from oscillator noise).

**Effect on single-carrier:** CFO at rate $\delta f$ causes the constellation to rotate at angular rate $2\pi \delta f$ rad/s. After one symbol, the rotation is $2\pi \delta f T_s$. For BPSK, this is tolerable for $\delta f T_s < 0.01$. For 64-QAM with tighter phase margins, requirements are tighter.

---

### Q4. Describe the principle of timing recovery. What is the Mueller-Muller (M&M) timing error detector?

**Answer:**

**Timing recovery** adjusts the receiver's sampling clock phase to sample the received waveform at the optimal ISI-free instants. In a digital receiver, this is implemented by:
1. Interpolating the received samples to the desired sampling phase
2. Feeding a timing error detector (TED) that produces an error signal
3. Filtering the error and controlling the interpolation phase (or a physical VCO)

**Mueller-Muller TED:** A decision-directed TED that operates at 1 sample/symbol:

$$e[k] = \hat{d}[k-1] \cdot y[k] - \hat{d}[k] \cdot y[k-1]$$

where $y[k]$ is the sampled output at time $k$ and $\hat{d}[k]$ is the hard decision.

**S-curve:** The expected value $\mathbb{E}[e[k]]$ as a function of timing offset $\tau$ has a zero crossing at $\tau = 0$ (correct timing) and is antisymmetric — this is the timing error detector's S-curve, analogous to the PLL phase detector characteristic. The slope at zero (timing sensitivity) determines the loop gain.

**Other popular TEDs:**

| TED | Samples/symbol | Properties |
|---|---|---|
| Mueller-Muller | 1 | Simple, requires decisions, sensitive to ISI |
| Gardner | 2 | Decision-free (non-data-aided), widely used |
| Early-Late | 2 | Robust, intuitive, higher implementation cost |
| MMSE-based | 2 | Optimal, used in modern digital implementations |

---

### Q5. What is frame synchronisation and why is it needed?

**Answer:**

Frame synchronisation (or packet detection) determines the start position of a data frame within the received stream. Without it, the receiver would not know where the header, coded data, and CRC boundaries are, making decoding impossible.

**Methods:**

**1. Preamble-based detection:** A known training sequence (preamble) precedes each frame. The receiver computes a sliding correlation between the received signal and the known preamble:

$$C[k] = \sum_{n=0}^{L-1} r[n + k] \cdot p^*[n]$$

A peak in $|C[k]|$ exceeding a threshold indicates frame start. Detection probability and false alarm rate are traded off via the threshold.

**2. Correlation metric with normalisation:** To handle varying SNR, normalise by the received power:

$$M[k] = \frac{|C[k]|^2}{\left(\sum_{n=0}^{L-1} |r[n+k]|^2\right)^2}$$

**3. Barker codes:** Special binary sequences (e.g., 13-bit Barker code $+++++-++-+-+-$) with near-ideal autocorrelation properties: $|R[\tau]| \leq 1$ for $\tau \neq 0$. Used in 802.11b DSSS.

**Design requirements for a good preamble:**
- High autocorrelation peak-to-sidelobe ratio (PSR)
- Flat power spectrum (equal energy across the channel bandwidth)
- Known to both transmitter and receiver
- Short enough to minimise overhead; long enough for reliable detection at minimum SNR

---

## Tier 2: Intermediate

### Q6. Describe the Schmidl-Cox algorithm for OFDM timing and frequency synchronisation.

**Answer:**

The Schmidl-Cox algorithm is a widely used preamble-based synchronisation method for OFDM, introduced in 1997 (IEEE Trans. Commun.). It enables simultaneous timing and fractional-subcarrier-spacing frequency offset estimation.

**Preamble structure:** A special training OFDM symbol is designed so that the first and second halves of the time-domain symbol are identical:

$$x[n] = x[n + N/2], \quad n = 0, 1, \ldots, N/2 - 1$$

This is achieved by setting odd-indexed subcarriers to zero and modulating even-indexed subcarriers with a known PN sequence.

**Timing metric:** Exploit the half-symbol repetition by computing the delayed correlation:

$$P[d] = \sum_{m=0}^{N/2-1} r^*[d+m] \cdot r[d + m + N/2]$$

$$R[d] = \sum_{m=0}^{N/2-1} |r[d + m + N/2]|^2$$

**Timing metric:**

$$M[d] = \frac{|P[d]|^2}{R^2[d]}$$

$M[d]$ has a plateau (flat region equal to $N/2$ samples wide) centred at the true timing position $d_0$. The plateau arises because the half-symbol repetition gives constant correlation over the window. The timing estimate selects the plateau centre.

**Frequency offset estimation:** The phase of $P[d_0]$ at the plateau position is:

$$\angle P[d_0] = 2\pi \cdot \frac{\delta f}{\Delta f} \cdot \frac{N}{2} \cdot \frac{1}{N} = \pi \cdot \frac{\delta f}{\Delta f}$$

Wait — more precisely, the phase of $P$ accumulates as $e^{j2\pi \delta f \cdot (N/2)/f_s} = e^{j\pi \delta f / \Delta f}$.

The normalised frequency offset estimate:

$$\hat{\varepsilon}_{frac} = \frac{\angle P[d_0]}{\pi}$$

This gives $|\hat{\varepsilon}_{frac}| \leq 1$, i.e., one subcarrier spacing of acquisition range. For larger offsets (integer multiples of $\Delta f$), a second integer-offset estimation stage is required (e.g., using cross-correlation with known data subcarriers).

**Limitations:**
- Plateau makes exact timing ambiguous; often refined with a second fine-timing stage
- Only fractional CFO estimated; integer CFO requires additional pilot-based estimation
- Sensitive to multipath (replicas smear the plateau)

---

### Q7. Compare open-loop and closed-loop synchronisation approaches. When is each appropriate?

**Answer:**

**Open-loop (feed-forward) synchronisation:** Computes synchronisation parameters from the received signal in a single pass, without a feedback loop.

- **Mechanism**: A block of received samples is processed to estimate timing and frequency offsets using maximum likelihood or correlation methods (e.g., Schmidl-Cox).
- **Advantages**: Fast acquisition (one estimate per preamble); no stability issues; simple to implement for burst-mode or packet-switched systems.
- **Disadvantages**: Estimate quality limited by preamble length; cannot track slowly varying offsets continuously; estimation noise is not smoothed over time.
- **Typical use**: Wi-Fi (802.11) packet detection; LTE initial cell search; burst-mode satellite modems.

**Closed-loop (feedback) synchronisation:** Uses a tracking loop (PLL / DLL) that continuously adjusts the receiver's local references based on a continuously computed error signal.

- **Mechanism**: Decision-directed or pilot-based error detectors feed timing and frequency error estimates into digital loops. The loop continuously steers the sampling phase (via a Farrow interpolator) and the NCO frequency.
- **Advantages**: Tracks slow drift and Doppler continuously; averaging in the loop filter suppresses noise; can maintain lock indefinitely.
- **Disadvantages**: Requires acquisition first (loop must be pulled into lock); can lose lock under rapid phase changes; loop dynamics must be carefully designed.
- **Typical use**: Cellular base stations; digital TV (DVB-S2); continuous-mode modems; satellite communications.

**Hybrid approach (common in practice):**
1. Open-loop acquisition using preamble (fast, coarse estimate)
2. Closed-loop tracking once data transmission begins (low noise, continuous)

---

### Q8. Explain timing jitter and phase noise, and their effect on receiver performance.

**Answer:**

**Timing jitter:** Random variation in the actual sampling instant around the ideal time $kT_s$. Sources include: oscillator phase noise, power supply coupling, digital switching noise into the ADC clock.

**Effect on performance:** A timing error $\epsilon$ on a signal with maximum frequency $f_{max}$ causes a sampled amplitude error:

$$\Delta s \approx \frac{ds}{dt}\bigg|_{t=kT_s} \cdot \epsilon$$

The resulting SNR degradation (signal-to-jitter-noise ratio):

$$\text{SJNR} \approx \frac{1}{(2\pi f_{max} \sigma_\epsilon)^2}$$

where $\sigma_\epsilon$ is the RMS jitter. For 14-bit ADC performance at 100 MHz bandwidth, the required RMS jitter is $\sigma_\epsilon < 0.5$ ps — a demanding specification.

**Phase noise:** Short-term frequency instability of an oscillator, characterised by the single-sideband noise PSD $\mathcal{L}(f_m)$ in dBc/Hz at offset $f_m$ from the carrier.

**Effect on OFDM:**
Phase noise causes two effects:
1. **Common Phase Error (CPE)**: All subcarriers are rotated by the same random angle — correctable using pilot-assisted phase tracking.
2. **Inter-Carrier Interference (ICI)**: Phase noise energy at frequency $m \Delta f$ leaks from subcarrier $k$ to subcarrier $k \pm m$, creating a noise floor that cannot be corrected.

The ICI noise variance per subcarrier is approximately:

$$\sigma^2_{ICI} \approx E_s \int_{-N\Delta f/2}^{N\Delta f/2} S_\phi(f)\, df - E_s \left|\int_{-\Delta f/2}^{\Delta f/2} S_\phi(f)\, df\right|^2$$

where $S_\phi(f)$ is the phase noise PSD.

---

### Q9. What is the Costas loop and why is it used for carrier recovery in BPSK/QPSK?

**Answer:**

The Costas loop is a PLL-based carrier recovery circuit that works without requiring a modulation-free carrier component. Conventional PLLs cannot lock to a suppressed-carrier DSB signal because the modulation randomises the phase.

**BPSK Costas loop operation:**

1. The incoming signal $r(t) = A d(t)\cos(2\pi f_c t + \phi) + n(t)$ is split and multiplied by the I and Q VCO outputs.
2. **I branch**: $r(t) \times \cos(2\pi \hat{f}_c t) \approx \frac{A}{2} d(t)\cos(\phi_e)$ after lowpass filtering.
3. **Q branch**: $r(t) \times (-\sin(2\pi \hat{f}_c t)) \approx \frac{A}{2} d(t)\sin(\phi_e)$ after lowpass filtering.
4. **Phase error signal**: $e(t) = I(t) \times Q(t) = \frac{A^2}{4} d^2(t)\sin(\phi_e)\cos(\phi_e) = \frac{A^2}{8}\sin(2\phi_e)$

Since $d^2(t) = 1$ for BPSK, the data modulation is removed and the error signal depends only on the phase error $\phi_e$. The VCO is steered to zero $\phi_e$.

**Phase ambiguity:** The Costas loop has stable lock points at $\phi_e = 0$ and $\phi_e = \pi$ (for BPSK), because $\sin(2\phi_e) = 0$ at both. This 180° phase ambiguity means the loop might lock to the wrong phase, inverting all bits. It is resolved by differential encoding (DPSK) or a known bit sequence used to detect the ambiguity.

**QPSK extension:** The QPSK Costas loop uses a fourth-power non-linearity or a decision-directed loop, removing the 4-fold phase ambiguity from the 90° symmetric QPSK constellation.

---

## Tier 3: Advanced

### Q10. Derive the Cramer-Rao Lower Bound (CRLB) for CFO estimation. What does it tell us about estimator design?

**Answer:**

**Model:** Received OFDM symbol with CFO $\varepsilon$ (normalised):

$$r[n] = \frac{1}{\sqrt{N}}\sum_{k} X[k] H[k] e^{j2\pi(k+\varepsilon)n/N} + w[n], \quad n = 0, \ldots, N-1$$

**Fisher information for $\varepsilon$:** For a complex Gaussian observation model with mean $\boldsymbol{\mu}(\varepsilon)$ and noise variance $N_0$, the Fisher information is:

$$I(\varepsilon) = \frac{2}{N_0} \text{Re}\!\left[\left(\frac{\partial \boldsymbol{\mu}}{\partial \varepsilon}\right)^H \frac{\partial \boldsymbol{\mu}}{\partial \varepsilon}\right]$$

For a training sequence with $X[k] = 1$ and flat channel $H[k] = 1$:

$$\frac{\partial \mu[n]}{\partial \varepsilon} = j\frac{2\pi n}{N} \mu[n]$$

$$I(\varepsilon) = \frac{2}{N_0} \cdot \frac{4\pi^2}{N^2} \sum_{n=0}^{N-1} n^2 = \frac{2}{N_0} \cdot \frac{4\pi^2}{N^2} \cdot \frac{(N-1)N(2N-1)}{6}$$

For large $N$:

$$I(\varepsilon) \approx \frac{4\pi^2 N}{3 N_0} \cdot \frac{E_s}{1} \quad \Rightarrow \quad \text{CRLB}(\hat\varepsilon) = \frac{1}{I(\varepsilon)} \approx \frac{3}{4\pi^2 N \cdot \text{SNR}}$$

**Interpretation:**
- CRLB decreases as $1/N$: longer training sequences give better estimates.
- CRLB decreases as $1/\text{SNR}$: more SNR improves estimation.
- The $1/N$ factor means the Schmidl-Cox estimator (which uses only $N/2$ samples for correlation) achieves twice the CRLB variance of an estimator using the full $N$-sample preamble.
- This bounds what is achievable and guides preamble length selection in system design.

---

### Q11. Describe the timing recovery architecture in a practical digital modem. Include the interpolator, TED, and loop filter.

**Answer:**

A complete digital timing recovery loop consists of five blocks:

**1. Fixed-rate ADC:** Samples at $f_s = L \cdot f_{sym}$ where $L$ is the oversampling factor (typically 2–4). The ADC runs from a free-running clock; timing recovery adjusts the interpolation phase, not the ADC clock.

**2. Matched/receive filter:** The RRC filter operating at the ADC sample rate.

**3. Interpolator:** A polyphase or Farrow interpolator reconstructs the signal at arbitrary sub-sample phases. The Farrow structure uses a polynomial approximation:

$$x(\hat{t}) = \sum_{l=0}^{L_{poly}-1} c_l \cdot x[\hat{t}/T_s - l] \cdot \mu^l$$

where $\mu \in [0,1)$ is the fractional delay (interpolation phase) and $c_l$ are polynomial coefficients.

**4. Timing Error Detector (TED):** Produces an error signal $e[k]$ proportional to timing offset. Gardner TED (2 samples/symbol):

$$e[k] = \text{Re}\!\left\{y\!\left[\left(k - \frac{1}{2}\right)T_s\right] \cdot \left(y^*[(k-1)T_s] - y^*[kT_s]\right)\right\}$$

**5. Digital loop filter:** Second-order PI filter for type-II PLL (tracks frequency offsets as well as phase):

$$v[k] = v[k-1] + K_1 e[k] + K_2 \sum_{n=0}^{k} e[n]$$

The integral term ($K_2$) ensures the loop has zero steady-state phase error even with a frequency offset.

**6. NCO (Numerically Controlled Oscillator):** Accumulates the loop filter output to produce the fractional timing advance per symbol, controlling the Farrow interpolator phase.

**Loop design parameters:** $K_1$ and $K_2$ are chosen to set the loop bandwidth $B_L$ and damping factor $\zeta$. Typical: $B_L T_s \approx 0.01$, $\zeta = 0.707$ (critically damped). The loop bandwidth is narrow enough to filter noise but wide enough to track oscillator drift.

---

### Q12. What is the Schmidl-Cox algorithm's Integer Frequency Offset (IFO) estimation problem and how is it solved?

**Answer:**

**The problem:** The Schmidl-Cox phase metric $\hat{\varepsilon}_{frac} = \angle P[d_0] / \pi$ estimates the fractional CFO (within $\pm 1$ subcarrier spacing). If the actual CFO is $\varepsilon = N_{int} + \varepsilon_{frac}$ where $N_{int}$ is an integer number of subcarrier spacings, the fractional part is correctly estimated but $N_{int}$ remains unknown. An uncorrected integer offset shifts all subcarrier indices by $N_{int}$, causing every decoded symbol to be wrong.

**Solution approaches:**

**1. Pilot-based IFO estimation:** After fractional CFO correction, the receiver examines the channel estimates at known pilot subcarrier positions. If the IFO is $N_{int}$, the pilot at expected position $k_p$ will appear at position $k_p + N_{int}$. The receiver tests IFO values $N_{int} \in \{-N/2, \ldots, N/2 - 1\}$ and selects the one that maximises pilot correlation:

$$\hat{N}_{int} = \arg\max_{m} \sum_{k \in \mathcal{P}} |Y[k+m] \cdot X_p^*[k]|^2$$

**2. Multi-symbol correlation:** Transmit two training symbols with known relationship (e.g., the same data repeated). The cross-correlation of FFT outputs:

$$C[m] = \sum_{k=0}^{N-1} Y_2[k] \cdot Y_1^*[k] \cdot e^{j2\pi km/N}$$

has a peak at $m = N_{int}$ that reveals the integer offset.

**3. Differential encoding of preamble subcarriers:** Design the preamble so that the ratio of adjacent pilot subcarriers encodes a unique codeword. After fractional correction, test all IFO hypotheses and find the one consistent with the known ratio sequence.

**Practical note in LTE:** LTE uses a Cell-Specific Reference Signal (CRS) structure whose known positions are used for IFO estimation after initial frequency acquisition. The PSS/SSS synchronisation signals are explicitly designed for robust CFO estimation across the full $\pm 7.5$ kHz range (half the 15 kHz subcarrier spacing).

---

## Common Interview Mistakes

1. **Conflating timing error and phase error**: Timing refers to the sampling instant (when to sample); phase refers to the carrier reference angle (at what phase to demodulate). These are separate loops in a receiver.
2. **Forgetting phase ambiguity in Costas loop**: BPSK loops have 180° ambiguity; QPSK loops have 90° ambiguity. This must be resolved by differential encoding or known sequence testing.
3. **Ignoring the integer CFO**: Schmidl-Cox only estimates fractional CFO. A system design that omits integer CFO estimation will fail under any significant frequency offset.
4. **Confusing loop bandwidth with noise bandwidth**: Loop bandwidth $B_L$ is a closed-loop parameter; noise bandwidth $B_n = \pi/2 \cdot B_L$ (for a second-order loop) is the effective bandwidth for noise. They differ by a factor of $\pi/2$.
5. **Oversimplifying the acquisition vs. tracking trade-off**: Wide-bandwidth loops acquire quickly but track noisily; narrow-bandwidth loops are low-noise but require prior coarse acquisition. Real systems switch bandwidth between acquisition and tracking modes.
