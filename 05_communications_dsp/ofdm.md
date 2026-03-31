# OFDM — Interview Questions

## Overview

Orthogonal Frequency-Division Multiplexing (OFDM) is the dominant wideband modulation technique used in LTE, 5G NR, Wi-Fi (802.11a/g/n/ac/ax), DVB-T, and ADSL. Interviewers in wireless baseband, modem, and RF roles expect deep understanding of the IFFT/FFT relationship, cyclic prefix mechanics, PAPR, and channel estimation.

---

## Tier 1: Fundamentals

### Q1. What is the core principle of OFDM?

**Answer:**

OFDM converts a high-rate serial data stream into $N$ parallel low-rate data streams, each of which modulates a separate orthogonal subcarrier. The subcarrier frequencies are:

$$f_k = f_0 + k \cdot \Delta f, \quad k = 0, 1, \ldots, N-1$$

where $\Delta f = 1/T$ is the subcarrier spacing and $T$ is the OFDM symbol duration (excluding the cyclic prefix).

**Orthogonality condition:** Two subcarriers $f_k$ and $f_l$ are orthogonal over $[0, T]$ when:

$$\int_0^T e^{j2\pi f_k t} e^{-j2\pi f_l t}\, dt = T \cdot \delta[k - l]$$

This holds when $\Delta f = 1/T$ — subcarrier spacing equals the reciprocal of the integration window. Orthogonality means each subcarrier can be demodulated without interfering with neighbouring subcarriers, even though their spectra overlap.

**Key benefit for wideband channels:** Instead of one wideband symbol of duration $T_s = 1/(N \cdot \Delta f)$ experiencing ISI from multipath, each OFDM subcarrier has a symbol duration $T = N \cdot T_s$ — much longer than the channel delay spread. With a cyclic prefix longer than the delay spread, ISI is eliminated entirely and each subcarrier sees a flat-fading (scalar) channel.

---

### Q2. How is OFDM modulation and demodulation implemented using the IFFT and FFT?

**Answer:**

**Modulation (IFFT at transmitter):**

Let $X[k]$ be the complex symbol on subcarrier $k$ ($k = 0, \ldots, N-1$). The OFDM time-domain samples are:

$$x[n] = \frac{1}{N}\sum_{k=0}^{N-1} X[k]\, e^{j2\pi kn/N}, \quad n = 0, 1, \ldots, N-1$$

This is exactly the N-point **IDFT** of $\{X[k]\}$, efficiently computed as an **IFFT** in $\mathcal{O}(N \log_2 N)$ operations.

**Cyclic prefix insertion:** Append the last $N_{CP}$ samples of $x[n]$ as a prefix, creating a transmitted block of $N + N_{CP}$ samples.

**Demodulation (FFT at receiver):**

After removing the cyclic prefix, the receiver computes the $N$-point DFT:

$$Y[k] = \sum_{n=0}^{N-1} y[n]\, e^{-j2\pi kn/N}$$

This is computed using the **FFT**. In the absence of noise and with a channel of length $\leq N_{CP}$, the result is:

$$Y[k] = H[k] \cdot X[k]$$

where $H[k]$ is the channel frequency response at subcarrier $k$. Each subcarrier has been reduced to a simple scalar multiplication — the entire wideband channel is diagonalised by the FFT.

**Why this is elegant:** The cyclic prefix converts linear convolution (ISI) into circular convolution, and the DFT diagonalises circular convolution. The combined effect eliminates ISI and decouples all subcarriers.

---

### Q3. What is the cyclic prefix and how does it eliminate ISI?

**Answer:**

The cyclic prefix (CP) is a copy of the last $N_{CP}$ samples of the OFDM symbol appended at the beginning of the transmitted block. The total transmitted length is $N + N_{CP}$ samples.

**ISI elimination mechanism:**

When an OFDM symbol passes through a multipath channel with maximum delay $\tau_{max}$, each received sample is a linear combination of the past $L_{ch} = \lceil \tau_{max} / T_{samp} \rceil + 1$ transmitted samples. This is linear convolution:

$$y_{\text{linear}}[n] = \sum_l h[l] \cdot x[n - l]$$

For the DFT to diagonalise the channel, we need **circular** convolution. The cyclic prefix achieves this:

1. The CP occupies the first $N_{CP}$ received samples, where channel transients from the previous symbol are present.
2. If $N_{CP} \geq L_{ch} - 1$, by the time the receiver processes samples $N_{CP}$ through $N_{CP} + N - 1$, the channel has "forgotten" the previous symbol and the current symbol has fully entered the channel.
3. Within this window, the effect of the channel is exactly circular convolution of the OFDM block with $h[n]$.

**CP overhead and efficiency:**

$$\text{Spectral efficiency} = \frac{N}{N + N_{CP}} \cdot \log_2 M \cdot \frac{\text{coded subcarriers}}{N}$$

A larger CP handles longer channels but reduces spectral efficiency. The CP length is typically chosen as $N_{CP}/N \approx 1/4$ to $1/8$, targeting channels with delay spread up to $N_{CP}/N$ of the symbol duration.

---

### Q4. What is the PAPR problem in OFDM and why is it more severe than in single-carrier systems?

**Answer:**

PAPR (Peak-to-Average Power Ratio) measures how much headroom a power amplifier must have to accommodate signal peaks without clipping.

**Why OFDM has high PAPR:** An OFDM signal is the sum of $N$ independently modulated subcarriers:

$$x(t) = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} X[k]\, e^{j2\pi f_k t}$$

By the central limit theorem, for large $N$ the time-domain samples approach a complex Gaussian distribution regardless of the per-subcarrier constellation. The instantaneous power envelope fluctuates widely.

**PAPR definition:**

$$\text{PAPR} = \frac{\max_{0 \leq t < T} |x(t)|^2}{\mathbb{E}[|x(t)|^2]}$$

For $N = 64$ subcarriers with QPSK, PAPR $\approx$ 10–12 dB (99.9th percentile). This is several dB higher than single-carrier QPSK ($\approx$ 3.6 dB).

**Consequences:**
- Power amplifier must back off by the PAPR to stay in the linear region, wasting DC power
- Especially problematic for battery-powered devices and satellite links

**Mitigation techniques:**

| Technique | Description | Trade-off |
|---|---|---|
| Clipping and filtering | Hard clip peaks, filter spectral regrowth | Small BER degradation, out-of-band emission |
| Selected Mapping (SLM) | Transmit the lowest-PAPR rotation of multiple equivalent frames | $\log_2 U$ overhead bits for side information |
| Partial Transmit Sequences (PTS) | Optimise phase of sub-blocks | Complexity |
| Tone Reservation | Reserve subcarriers for PAPR reduction signal | Slight spectral efficiency loss |
| SC-FDMA | Single-carrier variant (used in LTE uplink) | Inherently low PAPR, some equalisation complexity |

---

### Q5. What are pilot subcarriers and why are they needed in OFDM?

**Answer:**

Pilot subcarriers are subcarriers that carry known symbols ($X_\text{pilot}[k]$ known a priori) instead of data. They serve two main purposes:

**1. Channel estimation:** The receiver observes $Y[k] = H[k] X_\text{pilot}[k] + W[k]$ at pilot positions. Since $X_\text{pilot}[k]$ is known, the channel can be estimated as:

$$\hat{H}[k] = \frac{Y[k]}{X_\text{pilot}[k]}$$

The estimated channel is then interpolated to all data subcarriers.

**2. Synchronisation:** Pilots with known phase allow the receiver to track carrier frequency offset (CFO) and phase noise continuously throughout the frame (not just at the preamble).

**Pilot arrangements:**

| Type | Description | Typical use |
|---|---|---|
| Block/preamble pilots | Entire OFDM symbols carry pilots | Initial channel estimation (802.11, LTE cell search) |
| Comb pilots | Every $N_{pilot}$-th subcarrier is a pilot in every symbol | Tracking time-varying channels (DVB-T, LTE) |
| Scattered pilots | Pilots distributed in a 2D time-frequency grid | Doubly dispersive channels (LTE PDSCH DMRS) |

**Pilot density trade-off:** More pilots give better channel estimates (lower estimation noise) but reduce spectral efficiency. The minimum required pilot density is set by the Nyquist criterion in the 2D time-frequency channel:
- Frequency spacing $\leq 1/\tau_{max}$ (coherence bandwidth)
- Time spacing $\leq 1/(2 f_{D,max})$ (Doppler spread)

---

## Tier 2: Intermediate

### Q6. Derive the orthogonality of OFDM subcarriers and explain when it breaks down.

**Answer:**

**Proof of orthogonality:** Consider two subcarriers with frequencies $f_k = k\Delta f$ and $f_l = l\Delta f$. Their inner product over one symbol period $T = 1/\Delta f$:

$$\langle e_k, e_l \rangle = \int_0^T e^{j2\pi f_k t} \cdot e^{-j2\pi f_l t}\, dt = \int_0^T e^{j2\pi(k-l)\Delta f \cdot t}\, dt$$

$$= \frac{e^{j2\pi(k-l)} - 1}{j2\pi(k-l)\Delta f} = \begin{cases} T & k = l \\ 0 & k \neq l \end{cases}$$

The result is zero for $k \neq l$ because $(k-l)$ is a non-zero integer, making the complex exponential complete an integer number of full cycles over $[0, T]$.

**When orthogonality breaks down:**

1. **Carrier frequency offset (CFO):** If the receiver oscillator has frequency error $\delta f$, the observed subcarrier spacing is $\Delta f + \delta f / N$. The inner product becomes:

   $$\langle e_k, e_l \rangle \propto \text{sinc}\!\left(\pi(k - l + \varepsilon)\right)$$
   
   where $\varepsilon = \delta f / \Delta f$ is the normalised CFO. For $\varepsilon \neq 0$, the sinc is non-zero for $k \neq l$ — all subcarriers interfere with each other (ICI, inter-carrier interference).

2. **Timing offset beyond the CP:** If the FFT window extends outside the valid CP region, samples from two different symbols mix, breaking circular convolution and introducing ICI.

3. **Doppler spread:** In high-mobility channels, the channel $H(t,f)$ varies within one OFDM symbol. The time variation destroys orthogonality by effectively spreading each subcarrier's energy into adjacent bins (ICI).

4. **Phase noise:** Random phase modulation of the carrier causes both a common phase error (CPE, rotates all subcarriers equally) and ICI (spreads energy across subcarriers).

---

### Q7. Explain how OFDM channel estimation is performed. Compare LS and MMSE estimators.

**Answer:**

**Model:** At pilot subcarrier index $k$, the received signal is:

$$Y[k] = H[k] X_p[k] + W[k]$$

where $X_p[k]$ is the known pilot symbol, $H[k]$ is the channel frequency response, and $W[k] \sim \mathcal{CN}(0, N_0)$ is additive noise.

**Least Squares (LS) estimator:**

$$\hat{H}_{LS}[k] = \frac{Y[k]}{X_p[k]} = H[k] + \frac{W[k]}{X_p[k]}$$

The noise term has variance $N_0 / |X_p[k]|^2$. LS is simple and requires no knowledge of channel statistics, but it does not exploit channel correlations — each pilot estimate is independent.

**MMSE estimator:** Exploits knowledge of the channel's correlation structure $\mathbf{R}_{HH}$ and noise power $N_0$:

$$\hat{\mathbf{H}}_{MMSE} = \mathbf{R}_{HH}\!\left(\mathbf{R}_{HH} + \frac{N_0}{\sigma_p^2}\mathbf{I}\right)^{-1} \hat{\mathbf{H}}_{LS}$$

where $\mathbf{R}_{HH} = \mathbb{E}[\mathbf{H}\mathbf{H}^H]$ is the channel covariance and $\sigma_p^2 = |X_p|^2$.

MMSE MSE is lower than LS by a factor that depends on SNR and channel coherence bandwidth. At high SNR, MMSE approaches LS. At low SNR, MMSE provides significant gains by enforcing channel smoothness.

**Interpolation to data subcarriers:** After estimating $H[k]$ at pilot positions, interpolation fills in data subcarrier estimates:
- **Linear interpolation**: Simple, suitable for mildly varying channels
- **Spline or DFT-based interpolation**: Better for frequency-selective channels; the DFT approach exploits the finite delay spread to suppress noise

---

### Q8. Describe the 802.11a OFDM system parameters and justify each design choice.

**Answer:**

| Parameter | Value | Justification |
|---|---|---|
| Total subcarriers | 64 | FFT size; power of 2 for efficient FFT |
| Data subcarriers | 48 | Leaves pilots + guard subcarriers |
| Pilot subcarriers | 4 | Tracks phase and frequency offset |
| Guard subcarriers (DC + edges) | 12 | Null DC (LO leakage) + spectral mask compliance |
| Subcarrier spacing $\Delta f$ | 312.5 kHz | $= 20$ MHz$/64$ |
| OFDM symbol duration $T$ | 3.2 µs | $= 1/\Delta f$ |
| Cyclic prefix duration $T_{CP}$ | 0.8 µs | $= T/4$; covers indoor delay spread $\leq 50$–$100$ ns |
| Total symbol period $T_{sym}$ | 4.0 µs | $T + T_{CP}$ |
| Modulations supported | BPSK, QPSK, 16-QAM, 64-QAM | Adaptive coding and modulation |
| Channel bandwidth | 20 MHz | 5 GHz ISM band allocation |

**CP design rationale:** Indoor multipath delay spread is typically $< 100$ ns. The 0.8 µs CP provides 8× margin, ensuring robustness. The CP overhead is $0.8/4.0 = 20\%$ — 80% efficiency.

**Guard subcarrier rationale:** Zeroing the DC subcarrier avoids LO self-mixing (DC offset). Edge guard subcarriers (6 on each side) prevent adjacent-channel interference by allowing the spectral mask to be met by the combined response of the OFDM signal plus a practical anti-aliasing filter.

---

### Q9. How does cyclic prefix length affect OFDM system design? What happens when the channel delay spread exceeds the CP?

**Answer:**

**CP length selection:** Choose $N_{CP}$ such that:

$$N_{CP} \cdot T_{samp} \geq \tau_{max,RMS} \cdot k_{margin}$$

where $\tau_{max,RMS}$ is the RMS delay spread, $k_{margin} \approx 3$–$5$ for 99.99th percentile coverage, and $T_{samp} = 1/f_s$ is the sampling period.

**System trade-offs:**

| Effect of increasing $N_{CP}$ | Effect of decreasing $N_{CP}$ |
|---|---|
| Covers longer delay spreads | Fails for channels exceeding new limit |
| Reduces spectral efficiency | Increases spectral efficiency |
| Increases Tx/Rx power (wasted on CP) | Reduces power overhead |
| Reduces sensitivity to ISI | More ISI-sensitive |

**When CP is exceeded:** Suppose channel length is $L_{ch} > N_{CP} + 1$. The samples beyond the CP boundary carry inter-symbol interference from the *previous* OFDM symbol. The received signal model at subcarrier $k$ becomes:

$$Y[k] = H[k] X[k] + \underbrace{I_{ISI}[k]}_{\text{from prev. symbol}} + W[k]$$

The ISI power is proportional to the energy in the "excess" channel taps (those beyond $N_{CP}$). This causes an irreducible error floor — increasing transmit power does not help because ISI grows proportionally with signal power.

**LTE CP choices:**
- Normal CP: $N_{CP} = 144$ samples at 30.72 MHz ($\approx 4.7$ µs) — covers most outdoor cells
- Extended CP: $N_{CP} = 512$ samples ($\approx 16.7$ µs) — for very large cells or high-delay-spread environments

---

## Tier 3: Advanced

### Q10. Derive that the OFDM system model reduces to a set of independent flat-fading scalar channels.

**Answer:**

**System model:** Transmitted OFDM block (after IFFT and CP insertion, CP removed at receiver):

$$y[n] = \sum_{l=0}^{L-1} h[l] \cdot x[(n-l) \bmod N] + w[n], \quad n = 0, \ldots, N-1$$

Since the CP ensures circular convolution, the $\bmod N$ operation is valid — this is circular convolution of $h$ and $x$.

**Apply DFT to both sides:**

$$Y[k] = \mathcal{F}\{y\}[k] = \mathcal{F}\{h \circledast x\}[k] + \mathcal{F}\{w\}[k]$$

The **circular convolution theorem** states $\mathcal{F}\{h \circledast x\}[k] = H[k] \cdot X[k]$ where:

$$H[k] = \sum_{l=0}^{L-1} h[l]\, e^{-j2\pi kl/N}$$

Therefore:

$$\boxed{Y[k] = H[k] \cdot X[k] + W[k], \quad k = 0, \ldots, N-1}$$

**Interpretation:**
- Each subcarrier $k$ is an independent scalar flat-fading channel with complex gain $H[k]$
- The $N$-subcarrier OFDM system is equivalent to $N$ parallel AWGN channels, each with its own SNR $|H[k]|^2 E_s / N_0$
- The wideband ISI channel (requiring complex equalisation) is replaced by $N$ single-tap equalisers: $\hat{X}[k] = Y[k] / H[k]$ (ZF) or $\hat{X}[k] = H^*[k] Y[k] / (|H[k]|^2 + N_0/E_s)$ (MMSE)

**Key assumption:** The derivation requires $N_{CP} \geq L - 1$. If violated, the circular convolution assumption breaks and the neat diagonal structure is destroyed.

---

### Q11. Explain inter-carrier interference (ICI) in OFDM. Derive the ICI power for a carrier frequency offset $\varepsilon$ (normalised to subcarrier spacing).

**Answer:**

**Setup:** With a normalised CFO $\varepsilon = \delta f / \Delta f$, the received signal after removing the CP is:

$$r[n] = e^{j2\pi \varepsilon n / N} \cdot y[n] + w[n]$$

where the exponential represents the frequency error.

**DFT of the received signal:**

$$R[k] = \sum_{n=0}^{N-1} r[n] e^{-j2\pi kn/N} = \sum_{n=0}^{N-1} y[n] e^{j2\pi \varepsilon n/N} e^{-j2\pi kn/N}$$

Substituting $y[n] = \frac{1}{N}\sum_m X[m] H[m] e^{j2\pi mn/N}$ (no noise for clarity):

$$R[k] = \sum_{m=0}^{N-1} X[m] H[m] \cdot \underbrace{\frac{1}{N}\sum_{n=0}^{N-1} e^{j2\pi(m - k + \varepsilon)n/N}}_{\Phi(m-k+\varepsilon)}$$

where:

$$\Phi(\nu) = \frac{1}{N} \cdot \frac{\sin(\pi \nu)}{\sin(\pi \nu / N)} \cdot e^{j\pi\nu(N-1)/N}$$

For the desired subcarrier $m = k$:

$$\Phi(\varepsilon) = \frac{\sin(\pi \varepsilon)}{N \sin(\pi \varepsilon / N)} e^{j\pi\varepsilon(N-1)/N} \approx \text{sinc}(\varepsilon) e^{j\pi\varepsilon(N-1)/N}$$

For interfering subcarriers $m \neq k$, $\Phi(m - k + \varepsilon)$ is non-zero.

**ICI-to-signal power ratio (approximate, for small $\varepsilon$):**

$$\frac{P_{ICI}}{P_{signal}} \approx \frac{\pi^2 \varepsilon^2}{3}$$

For $\varepsilon = 0.01$ (1% of subcarrier spacing): ICI/signal $\approx -40$ dB — negligible.
For $\varepsilon = 0.1$ (10%): ICI/signal $\approx -21$ dB — significant for 16-QAM or higher.

**Practical requirement:** For 64-QAM OFDM, the CFO must be $\varepsilon < 0.01$, corresponding to $\delta f < 0.01 \Delta f$. For 802.11a with $\Delta f = 312.5$ kHz, this requires $\delta f < 3.125$ kHz frequency accuracy.

---

### Q12. Compare OFDM with SC-FDMA (Single-Carrier FDMA) used in the LTE uplink. Why was SC-FDMA chosen?

**Answer:**

SC-FDMA is sometimes called "DFT-precoded OFDM." It inserts an additional DFT block before the IFFT in the OFDM transmitter, spreading each user's symbols across all assigned subcarriers before OFDM modulation.

**SC-FDMA transmitter chain:**

$$\underbrace{X[k]}_{\text{data symbols}} \xrightarrow{\text{M-point DFT}} \tilde{X}[m] \xrightarrow{\text{subcarrier mapping}} \xrightarrow{\text{N-point IFFT}} \xrightarrow{\text{add CP}} \text{transmit}$$

**Receiver:** Standard OFDM receiver (FFT) followed by subcarrier de-mapping and an M-point IDFT.

**PAPR comparison:**

| Scheme | PAPR (typical, 64-QAM) |
|---|---|
| OFDM | ~10–12 dB (99.9th percentile) |
| SC-FDMA (localised) | ~5–7 dB |

SC-FDMA's lower PAPR arises because the DFT precoding distributes each symbol across multiple subcarriers in a structured way that resembles single-carrier transmission, retaining the lower PAPR of single-carrier signals.

**Why SC-FDMA for LTE uplink:**

1. **Power efficiency**: Mobile devices (UE) are battery-constrained. Lower PAPR means the power amplifier can operate with less back-off, directly translating to battery life.
2. **Spectral flexibility**: Like OFDM, SC-FDMA supports frequency-domain multiple access (FDMA) — different users occupy different subcarrier groups.
3. **Equalisation**: The receiver still uses FFT-domain equalisation, so channel estimation and equalisation complexity is similar to OFDM.

**Downlink (eNodeB):** OFDM is used because the base station has no PAPR constraint (large linear PAs are feasible and power consumption is less critical). OFDMA also enables flexible resource allocation to multiple users simultaneously.

---

### Q13. How does OFDM handle frequency-selective fading? Contrast with a wideband single-carrier system.

**Answer:**

**Single-carrier wideband system:** A single symbol occupies the full bandwidth $B$. The channel coherence bandwidth $B_c \approx 1/(2\pi \tau_{RMS})$. If $B \gg B_c$, the channel is frequency-selective: different frequency components of the symbol experience different gains and phases, causing severe ISI. A time-domain equaliser (e.g., MLSE or DFE) must span $\lceil \tau_{max}/T_s \rceil$ symbols — potentially hundreds of taps in high-delay-spread environments.

**OFDM approach:** The wideband channel is sub-divided into $N$ flat-fading sub-channels, each of bandwidth $\Delta f = B/N \ll B_c$ (ideally). Each sub-channel requires only a single-tap equaliser. The diversity in frequency is then exploited by:
1. Coding and interleaving across subcarriers and OFDM symbols
2. Water-filling power allocation (maximises capacity by allocating more power to subcarriers with higher $|H[k]|^2$)
3. Bit loading: assigning higher-order modulation to subcarriers with better SNR

**Diversity order with coding:** An OFDM system with a rate-$r$ code of minimum Hamming distance $d_{min}$, interleaved across $d_{min}$ frequency-diverse subcarriers, achieves diversity order $\min(d_{min}, N_f)$ where $N_f = \lfloor B / B_c \rfloor$ is the number of independent frequency-diversity branches.

**Residual problem:** Subcarriers experiencing deep fades have very low instantaneous SNR, causing errors. The coding and interleaving across subcarriers are essential to average over these fades. Without coding, OFDM actually performs *worse* than a single-carrier system with MLSE, because MLSE inherently exploits multipath energy as diversity while per-subcarrier OFDM discards faded subcarriers.

---

## Common Interview Mistakes

1. **Forgetting the CP overhead**: Quoting spectral efficiency without accounting for the cyclic prefix fraction $N_{CP}/(N + N_{CP})$.
2. **Claiming OFDM inherently provides diversity**: OFDM eliminates ISI but provides frequency diversity only when combined with coding and interleaving across subcarriers.
3. **Confusing IDFT normalisation conventions**: The IFFT at the transmitter is $x[n] = \frac{1}{N}\sum X[k] e^{j2\pi kn/N}$ (or sometimes without the $1/N$ factor — be consistent and explicit).
4. **Ignoring pilot overhead**: Spectral efficiency calculations must account for pilots, guard subcarriers, and the cyclic prefix.
5. **Misattributing ICI**: ICI is caused by CFO, phase noise, and Doppler — not by multipath delay (which is handled by the CP). Confusing ISI and ICI is a common error under interview pressure.
