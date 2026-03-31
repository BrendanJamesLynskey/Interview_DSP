# Convolution and Correlation — Interview Questions

**Subject:** Digital Signal Processing
**Topic:** Linear Convolution, Circular Convolution, Autocorrelation, Cross-Correlation, Overlap-Add, Overlap-Save
**Difficulty tiers:** Fundamentals / Intermediate / Advanced

---

## Fundamentals

### Q1. Define linear convolution. What is the length of the result?

**Answer:**

The **linear convolution** of two sequences $x[n]$ (length $L$) and $h[n]$ (length $M$) is:

$$y[n] = (x * h)[n] = \sum_{k=-\infty}^{\infty} x[k]\,h[n - k]$$

For finite-length sequences, this reduces to a finite sum:

$$y[n] = \sum_{k=\max(0,n-M+1)}^{\min(L-1,n)} x[k]\,h[n-k]$$

**Length of the result:**

If $x[n]$ is nonzero for $0 \leq n \leq L-1$ and $h[n]$ is nonzero for $0 \leq n \leq M-1$:

$$\text{Length}(y) = L + M - 1$$

**Intuition:** The first output sample $y[0] = x[0]\,h[0]$ (when both start at $n=0$). The last output sample is $y[L+M-2] = x[L-1]\,h[M-1]$. The "tail" of length $M-1$ is the transient die-away period.

**Step-by-step method ("flip and slide"):**

1. Write out $x[k]$
2. Flip $h[k]$ to get $h[-k]$, then slide it to position $n$ to get $h[n-k]$
3. Multiply pointwise and sum for each $n$

---

### Q2. Compute the linear convolution of $x[n] = \{1, 2, 3\}$ and $h[n] = \{1, 1, 1\}$ by hand.

**Answer:**

$L = M = 3$, so the result has $3 + 3 - 1 = 5$ samples, for $n = 0$ to $4$.

$$y[n] = \sum_{k=0}^{2} x[k]\,h[n-k]$$

$h[n-k] = 1$ for $0 \leq n-k \leq 2$, i.e., $n-2 \leq k \leq n$.

| $n$ | Contributing $k$ values | $y[n]$ |
|---|---|---|
| 0 | $k=0$: $x[0]h[0] = 1\cdot1$ | $1$ |
| 1 | $k=0,1$: $x[0]h[1]+x[1]h[0] = 1+2$ | $3$ |
| 2 | $k=0,1,2$: $1+2+3$ | $6$ |
| 3 | $k=1,2$: $x[1]h[2]+x[2]h[1] = 2+3$ | $5$ |
| 4 | $k=2$: $x[2]h[2] = 3$ | $3$ |

$$\boxed{y[n] = \{1,\,3,\,6,\,5,\,3\}}$$

**Verification via polynomial multiplication:**

$(1 + 2z^{-1} + 3z^{-2})(1 + z^{-1} + z^{-2}) = 1 + 3z^{-1} + 6z^{-2} + 5z^{-3} + 3z^{-4}$ ✓

---

### Q3. Define autocorrelation and cross-correlation for discrete-time sequences. How do they relate to convolution?

**Answer:**

**Cross-correlation** of $x[n]$ and $y[n]$:

$$R_{xy}[\ell] = \sum_{n=-\infty}^{\infty} x[n]\,y[n - \ell] = \sum_{n=-\infty}^{\infty} x[n+\ell]\,y[n]$$

The lag index $\ell$ indicates how much $y$ is shifted relative to $x$.

**Autocorrelation** of $x[n]$ with itself:

$$R_{xx}[\ell] = \sum_{n=-\infty}^{\infty} x[n]\,x[n - \ell]$$

**Relationship to convolution:**

Cross-correlation is convolution with one sequence **time-reversed**:

$$R_{xy}[\ell] = x[\ell] * y[-\ell]$$

or equivalently, using the z-transform: $S_{xy}(z) = X(z)\,Y(z^{-1})$

In the frequency domain (DTFT):

$$S_{xy}(e^{j\omega}) = X(e^{j\omega})\,Y^*(e^{j\omega})$$

The **power spectral density** of $x[n]$ is the DTFT of the autocorrelation:

$$S_{xx}(e^{j\omega}) = |X(e^{j\omega})|^2 \geq 0$$

**Properties of autocorrelation:**

- $R_{xx}[0] = \sum_n |x[n]|^2$ (total energy — always the maximum value)
- $R_{xx}[-\ell] = R_{xx}[\ell]$ (even symmetry)
- $|R_{xx}[\ell]| \leq R_{xx}[0]$ for all $\ell$

**Applications:**

- Cross-correlation: radar time-of-arrival estimation, GPS lock, waveform matching, audio synchronisation
- Autocorrelation: detecting periodicity, pitch estimation in audio, OFDM channel estimation

---

## Intermediate

### Q4. Describe the overlap-add method for implementing a long-input FIR filter efficiently.

**Answer:**

**Problem:** Filtering a long (possibly infinite) input signal $x[n]$ with an $M$-tap FIR filter $h[n]$ using the DFT.

**Key insight:** The DFT computes circular (not linear) convolution. To get linear convolution, use zero-padding. The overlap-add method divides the input into non-overlapping blocks and assembles the outputs.

**Algorithm:**

1. **Partition** $x[n]$ into non-overlapping blocks of length $L$:
   $$x_r[n] = x[n + rL], \quad n = 0, 1, \ldots, L-1$$

2. **Choose DFT size** $N \geq L + M - 1$ (typically the next power of 2).

3. **For each block $r$:** Zero-pad $x_r[n]$ to length $N$, compute $N$-point DFT $X_r[k]$, multiply pointwise by $H[k]$ (precomputed), compute inverse DFT to get $y_r[n]$ of length $N = L + M - 1$.

4. **Overlap and add:** Each output block $y_r[n]$ is $L + M - 1$ samples long, but the input blocks are only $L$ samples long. The last $M - 1$ samples of $y_r$ overlap with the first $M - 1$ samples of $y_{r+1}$ and are summed:

$$y[n] = \sum_r y_r[n - rL]$$

**Why it works:** Linear convolution of $x_r[n]$ with $h[n]$ produces $L + M - 1$ output samples. The first $L$ are the "body" and the last $M - 1$ are the "tail" that spills into the next block. Adding the tails correctly reconstructs the full linear convolution.

**Computational cost per output sample:** $O\!\left(\frac{N \log N}{L}\right)$. Optimal block size $L \approx M$ minimises this cost. For long filters ($M$ large), the FFT-based approach becomes dramatically cheaper than direct convolution.

---

### Q5. Describe the overlap-save method. How does it differ from overlap-add?

**Answer:**

**Overlap-save (overlap-discard)** avoids explicit addition of overlapping output segments by instead saving (overlapping) input samples.

**Algorithm:**

1. **Choose DFT size** $N \geq M$ (filter length). Block size $L = N - M + 1$.

2. **Partition input with overlap:** Each input block $x_r[n]$ has $N$ samples: the last $M-1$ samples of the **previous block** (saved) plus $L$ new samples:
   $$x_r = [\underbrace{x_{r-1}[L], \ldots, x_{r-1}[N-1]}_{M-1 \text{ old}}, \underbrace{x[rL], \ldots, x[rL + L - 1]}_{L \text{ new}}]$$

3. **For each block:** Compute $N$-point DFT, multiply by $H[k]$, compute inverse DFT.

4. **Discard** the first $M - 1$ samples of each output block (they are corrupted by the circular wrap-around). Keep the last $L = N - M + 1$ samples. These are valid linear convolution outputs.

**Comparison with overlap-add:**

| Feature | Overlap-Add | Overlap-Save |
|---|---|---|
| Input blocks | Non-overlapping ($L$ new samples) | Overlapping ($M-1$ saved samples) |
| Output assembly | Add overlapping tails | Discard first $M-1$ outputs |
| Computational cost | Same | Same |
| Memory pattern | Output overlap buffer | Input save buffer |
| Implementation preference | Natural for batch | Natural for streaming |

Both methods have the same asymptotic efficiency. Overlap-save is often preferred in streaming hardware because it involves a simpler buffer management: shift-register the input, discard invalid outputs.

---

### Q6. State the convolution theorem for the DTFT and explain how it is used to compute convolutions efficiently.

**Answer:**

**Convolution theorem:**

If $y[n] = (x * h)[n]$ (linear convolution), then:

$$Y(e^{j\omega}) = X(e^{j\omega})\,H(e^{j\omega})$$

Convolution in the time domain is equivalent to pointwise multiplication in the frequency domain.

**Inverse:** Multiplication in the time domain is circular convolution in the frequency domain (up to a factor):

$$\text{DTFT}\{x[n]\,h[n]\} = \frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{j\theta})\,H(e^{j(\omega-\theta)})\,d\theta$$

**Fast convolution algorithm:**

For two finite sequences of lengths $L$ and $M$:

1. Zero-pad both to $N \geq L + M - 1$ (use $N$ = next power of 2)
2. Compute $N$-point FFTs: $X[k]$ and $H[k]$ — cost $O(N\log N)$
3. Pointwise multiply: $Y[k] = X[k]\,H[k]$ — cost $O(N)$
4. Inverse FFT: $y[n] = \text{IFFT}\{Y[k]\}$ — cost $O(N\log N)$

Total: $O(N\log N)$ vs direct convolution $O(LM)$.

**Break-even point:** FFT is faster when $N\log_2 N < 2\,LM / N \cdot N$, which roughly means $M > \log_2 N$. In practice, for filters with more than ~30 taps and long signals, FFT convolution is faster.

---

## Advanced

### Q7. Derive the Wiener-Khintchine theorem relating the autocorrelation sequence to the power spectral density.

**Answer:**

**Setup:** Consider a wide-sense stationary (WSS) random process $x[n]$ with autocorrelation:

$$R_{xx}[\ell] = E\{x[n+\ell]\,x^*[n]\}$$

**Wiener-Khintchine theorem:** The power spectral density (PSD) is the DTFT of the autocorrelation sequence:

$$S_{xx}(e^{j\omega}) = \sum_{\ell=-\infty}^{\infty} R_{xx}[\ell]\,e^{-j\omega\ell}$$

**Proof sketch:**

Start with the periodogram of a length-$N$ realisation:

$$\hat{S}(e^{j\omega}) = \frac{1}{N}|X_N(e^{j\omega})|^2 = \frac{1}{N} X_N(e^{j\omega})\,X_N^*(e^{j\omega})$$

Expanding:

$$= \frac{1}{N}\left(\sum_{n=0}^{N-1}x[n]e^{-j\omega n}\right)\!\left(\sum_{m=0}^{N-1}x[m]e^{j\omega m}\right) = \frac{1}{N}\sum_{n,m} x[n]x^*[m]\,e^{-j\omega(n-m)}$$

Taking the expectation and letting $\ell = n - m$:

$$E\{\hat{S}(e^{j\omega})\} = \sum_{\ell=-(N-1)}^{N-1} \left(1 - \frac{|\ell|}{N}\right) R_{xx}[\ell]\,e^{-j\omega\ell}$$

As $N \to \infty$, the triangular weighting factor approaches 1 for all $\ell$, yielding:

$$S_{xx}(e^{j\omega}) = \lim_{N\to\infty} E\{\hat{S}(e^{j\omega})\} = \sum_{\ell=-\infty}^{\infty} R_{xx}[\ell]\,e^{-j\omega\ell} \quad \blacksquare$$

**Practical consequence:** Estimating the PSD from finite data is equivalent to estimating the autocorrelation and windowing it — this is the basis of the Blackman-Tukey spectral estimator and MUSIC/ESPRIT subspace methods.

---

### Q8. Explain how cross-correlation is used for time delay estimation. What is the Cramér-Rao bound for this problem?

**Answer:**

**Problem:** Two sensors receive a signal $s(t)$ at different times: $x_1[n] = s[n] + w_1[n]$ and $x_2[n] = s[n - D] + w_2[n]$, where $D$ is the unknown delay (in samples) and $w_1, w_2$ are independent noise.

**Cross-correlation approach:**

$$R_{x_1 x_2}[\ell] = \sum_n x_1[n]\,x_2[n - \ell] = \sum_n (s[n] + w_1[n])(s[n-\ell-D] + w_2[n-\ell])$$

Taking expectation (noise uncorrelated with signal and each other):

$$E\{R_{x_1 x_2}[\ell]\} = R_{ss}[\ell - D]$$

The expectation of the cross-correlation peaks at $\ell = D$. The estimated delay is:

$$\hat{D} = \arg\max_\ell \hat{R}_{x_1 x_2}[\ell]$$

**Generalised Cross-Correlation (GCC):** For improved noise robustness, filter both signals before cross-correlation using a weighting function $\Psi(e^{j\omega})$:

$$\hat{R}_{GCC}[\ell] = \text{IDTFT}\{\Psi(e^{j\omega})\,X_1(e^{j\omega})\,X_2^*(e^{j\omega})\}$$

Common choices: $\Psi = 1$ (basic CC), $\Psi = 1/|S_{x_1 x_2}|$ (PHAT — Phase Transform, emphasises fine timing resolution).

**Cramér-Rao bound (CRB) for delay estimation:**

For a single tone of frequency $f_0$ in white noise with SNR $\gamma$:

$$\text{Var}(\hat{D}) \geq \frac{1}{4\pi^2 f_0^2 \cdot \gamma \cdot N}$$

For broadband signal with bandwidth $B$:

$$\text{Var}(\hat{D}) \geq \frac{1}{8\pi^2 B_{rms}^2 \cdot \text{SNR} \cdot N}$$

where $B_{rms} = \sqrt{\frac{\int f^2 |S(f)|^2 df}{\int |S(f)|^2 df}}$ is the RMS bandwidth.

**Physical insight:** Wider signal bandwidth gives better delay resolution (the cross-correlation main lobe is narrower). This is why ultra-wideband (UWB) radar achieves centimetre-level ranging, while narrowband systems have metre-level resolution.

---

### Q9. Compare the computational costs of direct convolution, FFT-based convolution (single-block), overlap-add, and overlap-save for filtering a signal of 100,000 samples with a 1,000-tap FIR filter.

**Answer:**

**Parameters:** $L_{signal} = 100,000$, $M = 1,000$ (filter length).

**1. Direct convolution:**

Each output sample requires $M = 1000$ multiply-accumulate (MAC) operations.
Total: $100,000 \times 1000 = 10^8$ MACs.

**2. Single-block FFT convolution:**

$N = $ next power of 2 $\geq L_{signal} + M - 1 = 100,999 \Rightarrow N = 131,072 = 2^{17}$.

Three FFTs of size $N$: $3 \times \frac{N}{2}\log_2 N = 3 \times 65536 \times 17 \approx 3.3 \times 10^6$ complex multiplications.

Pointwise multiply: $N = 131,072$ complex multiplications.

Total: $\approx 3.5 \times 10^6$ complex multiplications $\approx 1.4 \times 10^7$ real MACs (1 complex multiply = ~4 real MACs + 2 adds).

**3. Overlap-add with block size $L$:**

Choose $L = 1024$ (optimal ~$M$), so $N = 2048 = 2^{11}$.

Number of blocks: $\lceil 100,000 / 1024 \rceil \approx 98$ blocks.

Per block: 3 FFTs of size 2048 = $3 \times 1024 \times 11 \approx 33,792$ complex multiplications + 2048 pointwise.

Total: $98 \times 35,840 \approx 3.5 \times 10^6$ complex multiplications.

**4. Overlap-save (same asymptotic cost as overlap-add):** Approximately equal.

**Summary:**

| Method | Approximate real MACs |
|---|---|
| Direct convolution | $10^8$ |
| Single-block FFT | $\approx 1.4 \times 10^7$ |
| Overlap-add/save | $\approx 1.4 \times 10^7$ |

The FFT methods are $\approx 7\times$ faster here. For longer signals, the savings grow: at $10^6$ samples and $M=1000$, direct convolution costs $10^9$ but overlap-add scales only linearly with signal length while maintaining the same per-output cost, so the gain approaches the ratio $M / \log_2(2M) \approx 1000/11 \approx 90\times$.

---

## Quick Reference

| Operation | Formula | Length |
|---|---|---|
| Linear convolution | $(x*h)[n] = \sum_k x[k]h[n-k]$ | $L+M-1$ |
| Circular convolution ($N$-pt) | $(x\circledast h)[n] = \sum_k x[k]h[\langle n-k\rangle_N]$ | $N$ |
| Cross-correlation | $R_{xy}[\ell] = \sum_n x[n]y[n-\ell]$ | $L+M-1$ |
| Autocorrelation | $R_{xx}[\ell] = \sum_n x[n]x[n-\ell]$ | Peak at $\ell=0$ |

| Overlap-Add | Overlap-Save |
|---|---|
| Non-overlapping input blocks | Overlapping input blocks ($M-1$ saved) |
| Add overlapping tails | Discard first $M-1$ outputs |
| Good for batch processing | Good for streaming |
