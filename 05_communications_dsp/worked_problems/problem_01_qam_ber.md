# Worked Problem 01: QAM Bit-Error Rate Calculation

## Problem Statement

Derive the bit-error probability as a function of $E_b/N_0$ for:

1. **BPSK** — exact derivation from first principles
2. **QPSK** — showing the relationship to BPSK
3. **16-QAM** — using the PAM-4 decomposition

Then evaluate all three numerically at $E_b/N_0 = 10$ dB and $E_b/N_0 = 14$ dB. Discuss the practical implications.

**Assumptions:**
- AWGN channel: $n(t) \sim \mathcal{CN}(0, N_0)$
- Gray-coded bit mapping
- Matched filter receiver with optimal sampling
- Equal probability symbols

---

## Part 1: BPSK

### System Model

BPSK transmits one of two symbols:
$$s_0 = -\sqrt{E_b}, \quad s_1 = +\sqrt{E_b}$$

After matched filtering and sampling, the received sample is:
$$r = s_i + n, \quad n \sim \mathcal{N}(0,\, N_0/2)$$

The noise variance is $N_0/2$ (one-sided noise PSD divided by 2 after matched filtering; the $N_0/2$ factor comes from the two-sided PSD convention).

### Decision Rule

Decide $\hat{d} = 1$ (symbol $s_1$) if $r > 0$, else $\hat{d} = 0$.

The decision threshold is at zero — the midpoint between the two equally-spaced constellation points.

### Probability of Error Derivation

**Given $s_1$ was sent:**

$$P_e \mid s_1 = P(r < 0 \mid s_1) = P(s_1 + n < 0) = P\!\left(n < -\sqrt{E_b}\right)$$

Standardise the Gaussian: let $z = n / \sqrt{N_0/2}$, so $z \sim \mathcal{N}(0, 1)$:

$$P_e \mid s_1 = P\!\left(z < -\frac{\sqrt{E_b}}{\sqrt{N_0/2}}\right) = P\!\left(z < -\sqrt{\frac{2E_b}{N_0}}\right) = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

where the Q-function is:
$$Q(x) = \frac{1}{\sqrt{2\pi}}\int_x^\infty e^{-t^2/2}\, dt = \frac{1}{2}\text{erfc}\!\left(\frac{x}{\sqrt{2}}\right)$$

**Given $s_0$ was sent:** By symmetry of the Gaussian around zero:

$$P_e \mid s_0 = P(r > 0 \mid s_0) = P(-\sqrt{E_b} + n > 0) = P\!\left(n > \sqrt{E_b}\right) = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

**Total BER (averaging over equally likely symbols):**

$$\boxed{P_b^{BPSK} = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)}$$

### Physical Interpretation

The argument $\sqrt{2E_b/N_0}$ is the **distance between the symbols** ($2\sqrt{E_b}$) divided by **twice the noise standard deviation** ($\sqrt{2 N_0/2} = \sqrt{N_0}$):

$$\sqrt{\frac{2E_b}{N_0}} = \frac{2\sqrt{E_b}}{2 \cdot \sqrt{N_0/2}} = \frac{d_{min}}{2\sigma}$$

A higher argument means the symbols are further apart relative to the noise spread, giving exponentially lower error probability.

---

## Part 2: QPSK

### QPSK as Two Independent BPSK Streams

A QPSK symbol is a complex point $(I, Q)$ where both $I \in \{-\sqrt{E_b}, +\sqrt{E_b}\}$ and $Q \in \{-\sqrt{E_b}, +\sqrt{E_b}\}$ are independent. The symbol energy is:

$$E_s = I^2 + Q^2 = E_b + E_b = 2E_b$$

The received sample is:
$$r = r_I + j r_Q, \quad r_I = s_I + n_I, \quad r_Q = s_Q + n_Q$$

where $n_I, n_Q \sim \mathcal{N}(0, N_0/2)$ are independent (the real and imaginary noise components of a complex AWGN process).

### Decision and BER

Decide $I$ and $Q$ independently: $\hat{s}_I = \text{sgn}(r_I)$, $\hat{s}_Q = \text{sgn}(r_Q)$.

Each branch is a BPSK detector with the same $E_b$ and noise variance. Therefore:

$$P_{b,I} = P_{b,Q} = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

With Gray coding, each 2-bit QPSK symbol has:
- Bit 0 (MSB) decoded from the I branch
- Bit 1 (LSB) decoded from the Q branch

The overall BER is the average of the two branch BERs:

$$\boxed{P_b^{QPSK} = Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)}$$

**Key result:** QPSK and BPSK have identical BER vs. $E_b/N_0$ in AWGN, despite QPSK having twice the spectral efficiency. The "free" spectral efficiency comes from exploiting the orthogonal quadrature dimension, which doubles capacity without splitting the noise budget.

### Why the Symbol Error Rate Differs

The QPSK **symbol error probability** is:

$$P_s^{QPSK} = 1 - (1 - P_{b,I})(1 - P_{b,Q}) = 2Q - Q^2 \approx 2Q\!\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

where $Q = Q(\sqrt{2E_b/N_0})$. This is approximately twice the BER at low-to-moderate error rates — correct for distinguishing SER from BER.

---

## Part 3: 16-QAM

### Decomposition into Two PAM-4 Streams

A square 16-QAM symbol can be written as $(a_I + j a_Q)$ where $a_I, a_Q \in \{-3d, -d, +d, +3d\}$ independently. This is two independent 4-level PAM (PAM-4) streams.

**Normalise to average symbol energy $E_s$:**

$$E_s = \mathbb{E}[|a_I|^2 + |a_Q|^2] = 2 \cdot \frac{1}{4}\!\left(9d^2 + d^2 + d^2 + 9d^2\right) = 2 \cdot 5d^2 = 10d^2$$

$$\Rightarrow \quad d = \sqrt{\frac{E_s}{10}} = \sqrt{\frac{4E_b}{10}} = \sqrt{\frac{2E_b}{5}}$$

The minimum distance is $2d = 2\sqrt{2E_b/5}$.

### BER for PAM-4 (one branch)

Label the four levels and their Gray-coded 2-bit assignments:

| Level | Symbol | Bits (Gray) |
|---|---|---|
| $-3d$ | $s_0$ | 00 |
| $-d$ | $s_1$ | 01 |
| $+d$ | $s_2$ | 11 |
| $+3d$ | $s_3$ | 10 |

Noise variance: $\sigma^2 = N_0/2$.

**Bit error analysis (MSB, i.e., the leading bit):**

The MSB (bit 0) separates the lower half from the upper half:
- Error if $s_0$ is sent and receiver decides $s_2$ or $s_3$ (crosses $0$): $P = Q(3d/\sigma) + Q(5d/\sigma) \approx Q(3d/\sigma)$
- Error if $s_1$ is sent and receiver decides $s_2$ or $s_3$: $P = Q(d/\sigma) + Q(3d/\sigma) \approx Q(d/\sigma)$
- Similarly for the positive levels by symmetry.

For the **LSB (bit 1)**, similar analysis yields dominant terms $Q(d/\sigma)$.

**Combining and simplifying** (standard result for Gray-coded PAM-4):

$$P_b^{PAM-4} = \frac{3}{4} Q\!\left(\frac{d}{\sigma}\right) = \frac{3}{4} Q\!\left(\sqrt{\frac{2d^2}{N_0}}\right)$$

Substituting $d^2 = 2E_b/5$:

$$P_b^{PAM-4} = \frac{3}{4} Q\!\left(\sqrt{\frac{4E_b}{5 N_0}}\right) = \frac{3}{4} Q\!\left(\sqrt{\frac{4}{5} \cdot \frac{2E_b}{N_0}}\right)$$

### 16-QAM BER (Gray coded)

The 16-QAM BER is the average BER of the I and Q PAM-4 branches, which are identical:

$$\boxed{P_b^{16\text{-QAM}} = \frac{3}{4} Q\!\left(\sqrt{\frac{8E_b}{5 N_0}}\right)}$$

Note: The argument $\sqrt{8/(5 N_0) \cdot E_b} = \sqrt{(8/5)} \cdot \sqrt{E_b/N_0}$ compared to $\sqrt{2} \cdot \sqrt{E_b/N_0}$ for BPSK — the factor $\sqrt{8/5}/\sqrt{2} = \sqrt{4/5} \approx 0.894$ represents the reduced normalised distance in 16-QAM due to the more tightly packed constellation.

---

## Numerical Evaluation

### Q-function reference values

| $x$ | $Q(x)$ |
|---|---|
| 2.0 | $2.28 \times 10^{-2}$ |
| 3.0 | $1.35 \times 10^{-3}$ |
| 3.36 | $3.9 \times 10^{-4}$ |
| 4.0 | $3.17 \times 10^{-5}$ |
| 4.42 | $4.9 \times 10^{-6}$ |
| 5.0 | $2.87 \times 10^{-7}$ |

### At $E_b/N_0 = 10$ dB ($= 10$ linear)

**BPSK/QPSK:**
$$\sqrt{\frac{2 \times 10}{1}} = \sqrt{20} = 4.472 \quad \Rightarrow \quad P_b = Q(4.472) \approx 3.87 \times 10^{-6}$$

**16-QAM:**
$$\sqrt{\frac{8 \times 10}{5 \times 1}} = \sqrt{16} = 4.0 \quad \Rightarrow \quad P_b = \frac{3}{4} Q(4.0) = \frac{3}{4} \times 3.17 \times 10^{-5} \approx 2.38 \times 10^{-5}$$

### At $E_b/N_0 = 14$ dB ($\approx 25.1$ linear)

**BPSK/QPSK:**
$$\sqrt{2 \times 25.1} = \sqrt{50.2} = 7.09 \quad \Rightarrow \quad P_b = Q(7.09) \approx 6.6 \times 10^{-13}$$

**16-QAM:**
$$\sqrt{\frac{8 \times 25.1}{5}} = \sqrt{40.2} = 6.34 \quad \Rightarrow \quad P_b = \frac{3}{4} Q(6.34) \approx \frac{3}{4} \times 1.2 \times 10^{-10} \approx 9 \times 10^{-11}$$

### Summary Table

| Scheme | $P_b$ at 10 dB | $P_b$ at 14 dB |
|---|---|---|
| BPSK | $3.9 \times 10^{-6}$ | $6.6 \times 10^{-13}$ |
| QPSK | $3.9 \times 10^{-6}$ | $6.6 \times 10^{-13}$ |
| 16-QAM | $2.4 \times 10^{-5}$ | $9.0 \times 10^{-11}$ |

---

## Discussion

### SNR Penalty of 16-QAM vs. BPSK

At BER $= 10^{-5}$, we can find the required $E_b/N_0$ for each scheme:

**BPSK:** $Q(\sqrt{2x}) = 10^{-5} \Rightarrow \sqrt{2x} \approx 4.42 \Rightarrow x = 9.77$ ($= 9.9$ dB)

**16-QAM:** $\frac{3}{4} Q(\sqrt{8x/5}) = 10^{-5} \Rightarrow Q(\sqrt{8x/5}) = 1.33 \times 10^{-5} \Rightarrow \sqrt{8x/5} \approx 4.37 \Rightarrow x = 4.37^2 \times 5/8 = 11.9$ ($= 10.75$ dB)

Solving: $Q(\sqrt{8x/5}) = 10^{-5}/0.75 = 1.33 \times 10^{-5}$. From Q-function tables, $Q(4.2) \approx 1.3 \times 10^{-5}$, so $\sqrt{8x/5} \approx 4.2$, giving $x = 4.2^2 \times 5/8 = 11.0$ ($= 10.4$ dB).

**SNR penalty at equal $E_b/N_0$**: 16-QAM requires ~0.5 dB more $E_b/N_0$ than BPSK at BER $= 10^{-5}$. This is smaller than the commonly cited ~4 dB gap because the large gaps are based on $E_s/N_0$ comparisons, not $E_b/N_0$. At equal $E_s/N_0$, BPSK has $10\log_{10}(4) = 6$ dB more $E_b$ per symbol than 16-QAM (since BPSK carries 1 bit/symbol vs 4 bits/symbol), which accounts for the large cited performance gap. At equal $E_b/N_0$ (the fair comparator for spectral efficiency analysis), the gap is much smaller.

### Practical Implications

1. **Adaptive modulation**: Systems like LTE and Wi-Fi 6 switch between QPSK and 64-QAM based on the measured $E_b/N_0$. The BER formulas derived here directly map to the CQI/MCS selection tables used in these standards.

2. **Channel coding interaction**: In coded systems, the operating $E_b/N_0$ is well below the uncoded BER requirements (turbo/LDPC codes operate near the Shannon limit). The modulation order choice is made on coded performance curves, not the raw formulas above.

3. **Diversity and fading**: In Rayleigh fading, BER falls as $1/(4\bar{\gamma})$ for BPSK rather than $Q(\sqrt{2\bar{\gamma}})$ — a vastly worse relationship. Knowing the AWGN curves is necessary but not sufficient for system design in real channels.
