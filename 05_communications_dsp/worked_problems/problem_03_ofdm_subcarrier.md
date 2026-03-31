# Worked Problem 03: OFDM System Design

## Problem Statement

Design an OFDM system for the following requirements:

- **Available channel bandwidth:** $B = 20$ MHz
- **Channel delay spread (max):** $\tau_{max} = 5$ µs (suburban outdoor environment)
- **Doppler spread:** $f_D = 200$ Hz (pedestrian velocity at 2.4 GHz)
- **Target spectral efficiency:** $\geq 4$ bit/s/Hz (system-level, before coding)
- **Cyclic prefix overhead:** $\leq 25\%$ of symbol duration

**Design tasks:**
1. Choose the subcarrier spacing $\Delta f$
2. Choose the FFT size $N$
3. Determine the cyclic prefix length $N_{CP}$
4. Choose the guard band and number of used subcarriers
5. Choose the modulation order to meet spectral efficiency
6. Show the IFFT/FFT relationship explicitly
7. Compute the achievable bit rate

---

## Step 1: Choose Subcarrier Spacing $\Delta f$

### Constraints on $\Delta f$

Two competing constraints bound the subcarrier spacing:

**Upper bound — Coherence bandwidth:** Each subcarrier must see a flat-fading sub-channel. The coherence bandwidth is approximately:

$$B_c \approx \frac{1}{5\tau_{rms}} \approx \frac{1}{5 \times \tau_{max}/3} \approx \frac{1}{\tau_{max}} = \frac{1}{5\, \mu\text{s}} = 200\, \text{kHz}$$

(Using $\tau_{rms} \approx \tau_{max}/3$ as a rough estimate.) For flat fading per subcarrier, require $\Delta f \ll B_c$:

$$\Delta f \leq \frac{B_c}{10} = 20\, \text{kHz}$$

**Lower bound — Doppler spread:** The subcarrier spacing must be much larger than the Doppler spread so that ICI is small:

$$\Delta f \gg f_D = 200\, \text{Hz}$$

Rule of thumb: $\Delta f \geq 10 f_D = 2$ kHz.

**CP overhead constraint:** The cyclic prefix must cover the delay spread:

$$T_{CP} = \frac{N_{CP}}{N} \cdot T \geq \tau_{max} = 5\, \mu\text{s}$$

If the CP overhead fraction is $\rho_{CP} = T_{CP}/T \leq 0.25$:

$$T_{CP} = \rho_{CP} \cdot T \leq 0.25 T \quad \Rightarrow \quad T \geq \frac{\tau_{max}}{0.25} = 4 \times 5\, \mu\text{s} = 20\, \mu\text{s}$$

$$\Delta f = \frac{1}{T} \leq \frac{1}{20\, \mu\text{s}} = 50\, \text{kHz}$$

### Chosen Subcarrier Spacing

Select $\Delta f = 15$ kHz (same as LTE), which satisfies all constraints:
- $\Delta f = 15$ kHz $\ll B_c = 200$ kHz ✓
- $\Delta f = 15$ kHz $\gg f_D = 200$ Hz ✓ (ratio = 75)
- Resulting symbol duration $T = 1/\Delta f = 66.7$ µs

---

## Step 2: Choose FFT Size $N$

The sampling rate must span the full bandwidth:

$$f_s \geq 2B = 40\, \text{MHz}$$

For implementation efficiency, choose $f_s = N \cdot \Delta f$ where $N$ is a power of 2. The relation between $N$, $f_s$, and $\Delta f$:

$$N = \frac{f_s}{\Delta f}$$

**Options:**

| $N$ | $f_s = N \cdot 15$ kHz | Compatible with 20 MHz? |
|---|---|---|
| 1024 | 15.36 MHz | Borderline (uses only 13.3 MHz of guard-included BW) |
| 2048 | 30.72 MHz | Yes — standard LTE value for 20 MHz |
| 4096 | 61.44 MHz | Oversizes the ADC; wastes power |

**Choose $N = 2048$**, $f_s = 30.72$ MHz.

This gives sample period $T_{samp} = 1/30.72 \approx 32.6$ ns.

---

## Step 3: Determine Cyclic Prefix Length $N_{CP}$

The CP must cover the maximum delay spread:

$$N_{CP} \geq \frac{\tau_{max}}{T_{samp}} = \frac{5\, \mu\text{s}}{32.6\, \text{ns}} = \frac{5000\, \text{ns}}{32.6\, \text{ns}} \approx 153.4$$

Round up to the next integer: $N_{CP} = 160$ (standard LTE normal CP for 30.72 MHz sampling).

**CP duration:** $T_{CP} = 160 \times 32.6\, \text{ns} = 5.21$ µs $> \tau_{max} = 5$ µs ✓

**CP overhead:**

$$\rho_{CP} = \frac{N_{CP}}{N + N_{CP}} = \frac{160}{2048 + 160} = \frac{160}{2208} = 7.25\%$$

This is well within the 25% constraint. The efficiency is $1 - 0.0725 = 92.75\%$.

**Verify symbol duration:**

$$T_{sym} = (N + N_{CP}) \cdot T_{samp} = 2208 \times 32.6\, \text{ns} = 71.97\, \mu\text{s}$$

---

## Step 4: Guard Band and Number of Used Subcarriers

The 2048-point FFT spans $f_s = 30.72$ MHz symmetrically: from $-15.36$ MHz to $+15.36$ MHz. The desired channel is $\pm 10$ MHz (total 20 MHz).

**Total subcarriers covering 20 MHz:**

$$N_{used,max} = \frac{20\, \text{MHz}}{15\, \text{kHz}} \approx 1333\, \text{subcarriers}$$

However, we must reserve:
- **DC subcarrier**: 1 subcarrier at $f = 0$ (set to zero to avoid LO leakage problems)
- **Edge guard subcarriers**: Sufficient null subcarriers on each side to allow the spectral mask to be met by a practical transmit filter. Typically $5\%$–$10\%$ of the used bandwidth on each side.

For a 20 MHz channel with 10% guard on each edge: $0.10 \times 1333 / 2 \approx 67$ subcarriers per side.

**LTE-aligned design (closest standard):**

LTE 20 MHz uses $N_{used} = 1200$ data+pilot subcarriers (100 resource blocks × 12 subcarriers/RB), with:
- Guard: $(2048 - 1200 - 1)/2 = 423$ null subcarriers on each edge → this covers $423 \times 15$ kHz $= 6.35$ MHz guard per side, which is quite large.

Actually LTE uses only 1200 out of 2048 subcarriers. For our design:

**Choose $N_{used} = 1200$ data+pilot subcarriers** (preserving LTE alignment).

Guard subcarriers per side: $(2048 - 1200 - 1)/2 = 423$ → 6.35 MHz guard per side.

The actual occupied bandwidth is $1200 \times 15$ kHz $= 18$ MHz (leaving 1 MHz guard on each side of the 20 MHz allocation — achievable with a practical transmit filter).

---

## Step 5: Pilot Subcarriers and Data Subcarriers

Following LTE-style comb pilot structure (every 6th subcarrier is a pilot, 2 OFDM symbols per pilot pattern period):

$$N_{pilot} = \frac{N_{used}}{6} \times \frac{2}{14} \approx \frac{1200}{6} \times \frac{2}{14} = 200 \times 0.143 \approx 29\, \text{pilots/symbol on average}$$

More precisely: in LTE PDSCH, approximately $12\%$–$15\%$ of resource elements are reference signals. Let us use $15\%$:

$$N_{data} = 0.85 \times 1200 = 1020\, \text{data subcarriers per OFDM symbol}$$

---

## Step 6: Modulation Order Selection

**Target spectral efficiency:** $\geq 4$ bit/s/Hz.

The achievable spectral efficiency with $N_{data}$ data subcarriers, modulation order $M$, and channel bandwidth $B$:

$$\eta = \frac{N_{data} \cdot \log_2 M}{T_{sym} \cdot B} \quad \text{bit/s/Hz}$$

With $N_{data} = 1020$, $T_{sym} = 71.97$ µs, $B = 20$ MHz:

$$\eta = \frac{1020 \cdot \log_2 M}{71.97 \times 10^{-6} \times 20 \times 10^6} = \frac{1020 \cdot \log_2 M}{1439.4}$$

| Modulation | $\log_2 M$ | $\eta$ (bit/s/Hz) | Meets target? |
|---|---|---|---|
| QPSK | 2 | $2040/1439 = 1.42$ | No |
| 16-QAM | 4 | $4080/1439 = 2.83$ | No |
| 64-QAM | 6 | $6120/1439 = 4.25$ | Yes ✓ |
| 256-QAM | 8 | $8160/1439 = 5.67$ | Yes ✓ |

**Choose 64-QAM** as the minimum-order modulation that meets the spectral efficiency target of 4 bit/s/Hz.

---

## Step 7: IFFT/FFT Relationship — Explicit Derivation

### Transmitter: IFFT

Let the 64-QAM symbols on each data subcarrier be $X[k]$ for $k \in \mathcal{S}_{data}$ (set of data subcarrier indices), $X[k] = 0$ for guard and DC subcarriers.

The IFFT produces $N = 2048$ time-domain samples:

$$x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k]\, e^{j2\pi kn/N}, \quad n = 0, 1, \ldots, N-1$$

The continuous-time approximation (at sample rate $f_s = N\Delta f$):

$$x(t) \approx \sum_{k=0}^{N-1} X[k]\, e^{j2\pi k \Delta f \cdot t} = \sum_{k \in \mathcal{S}_{data}} X[k]\, e^{j2\pi f_k t}$$

where $f_k = k \cdot \Delta f$ is the $k$-th subcarrier frequency.

### Cyclic Prefix Insertion

Append the last $N_{CP} = 160$ samples as a prefix:

$$\tilde{x}[n] = x[(n - N_{CP}) \bmod N] \cdot \mathbf{1}_{0 \leq n < N + N_{CP}}$$

Total block length: $N + N_{CP} = 2208$ samples, duration $71.97$ µs.

### Channel: Circular Convolution

With $h[l]$, $l = 0, \ldots, L_{ch}-1$, and $L_{ch} \leq N_{CP} + 1 = 161$:

After CP removal, the received block satisfies:

$$y[n] = \sum_{l=0}^{L_{ch}-1} h[l] \cdot x[(n-l) \bmod N] + w[n]$$

This is circular convolution $h \circledast x$ plus noise.

### Receiver: FFT and Single-Tap Equalisation

**FFT:**

$$Y[k] = \sum_{n=0}^{N-1} y[n]\, e^{-j2\pi kn/N} = H[k] \cdot X[k] + W[k]$$

where $H[k] = \sum_{l=0}^{L_{ch}-1} h[l]\, e^{-j2\pi kl/N}$ is the DFT of the channel.

**Single-tap ZF equalisation:**

$$\hat{X}[k] = \frac{Y[k]}{H[k]} = X[k] + \frac{W[k]}{H[k]}$$

**MMSE equalisation:**

$$\hat{X}_{MMSE}[k] = \frac{H^*[k]}{|H[k]|^2 + N_0/E_s} Y[k]$$

The post-equalisation SNR per subcarrier (MMSE):

$$\text{SNR}_{MMSE}[k] = \frac{|H[k]|^2 E_s}{N_0}$$

Subcarriers with $|H[k]|^2 \approx 0$ (channel nulls) have near-zero SNR and are discarded or assigned lower-order modulation.

---

## Step 8: System Parameter Summary

| Parameter | Value | Notes |
|---|---|---|
| Channel bandwidth $B$ | 20 MHz | Given |
| Sampling rate $f_s$ | 30.72 MHz | $N \cdot \Delta f$ |
| FFT size $N$ | 2048 | Power of 2 |
| Subcarrier spacing $\Delta f$ | 15 kHz | $f_s / N$ |
| Useful symbol duration $T$ | 66.7 µs | $1/\Delta f$ |
| CP length $N_{CP}$ | 160 samples | $5.21$ µs |
| CP overhead | 7.25% | $N_{CP}/(N+N_{CP})$ |
| Total symbol duration $T_{sym}$ | 71.97 µs | $T + T_{CP}$ |
| Total subcarriers | 2048 | FFT output |
| Used subcarriers | 1200 | Data + pilots |
| Pilot subcarriers (approx.) | 180 | 15% of used |
| Data subcarriers | 1020 | 85% of used |
| Modulation | 64-QAM | 6 bits/symbol |
| Bits per OFDM symbol | 6120 | $1020 \times 6$ |

---

## Step 9: Bit Rate Calculation

$$R_b = \frac{N_{data} \cdot \log_2 M}{T_{sym}} = \frac{1020 \times 6}{71.97 \times 10^{-6}} = \frac{6120}{71.97\, \mu\text{s}} \approx 85.0\, \text{Mbit/s}$$

**Spectral efficiency:**

$$\eta = \frac{R_b}{B} = \frac{85.0\, \text{Mbit/s}}{20\, \text{MHz}} = 4.25\, \text{bit/s/Hz}$$

Target of 4 bit/s/Hz is met. ✓

**With rate-3/4 FEC coding (e.g., turbo or LDPC):**

$$R_b^{coded} = 0.75 \times 85.0 = 63.75\, \text{Mbit/s}, \quad \eta_{coded} = 3.19\, \text{bit/s/Hz}$$

This is a realistic operating point (below 3 bit/s/Hz is typical for LTE with coding), confirming the design is feasible.

---

## Coherence Bandwidth and Frequency Diversity Check

With $\Delta f = 15$ kHz and $B_c \approx 1/\tau_{max} = 200$ kHz, the number of independent frequency diversity branches is:

$$N_{div} = \left\lfloor \frac{B}{B_c} \right\rfloor = \left\lfloor \frac{20\, \text{MHz}}{200\, \text{kHz}} \right\rfloor = 100$$

Each group of $B_c / \Delta f = 200/15 \approx 13$ adjacent subcarriers experiences approximately the same fading. With LDPC coding interleaved across all 1200 subcarriers, the code can exploit up to 100 independent diversity channels — providing robust performance in the selective fading channel.

**Design complete.** The parameters are consistent with LTE 20 MHz operation, validating that the design methodology matches industry practice.
