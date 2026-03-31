# DSP Implementation — Multiple-Choice Quiz

**Topics covered:** Fixed-point arithmetic (Q-format, overflow, saturation), quantisation noise and SQNR, FPGA DSP slices, pipelining, CORDIC algorithm, CIC filter bit growth, limit cycles, coefficient sensitivity in IIR filters.

**Instructions:** Select the single best answer for each question. The answer key with detailed explanations appears at the bottom.

---

## Questions

**Q1.** A number is represented in Q15 fixed-point format using a 16-bit two's complement word. What is the representable range and the resolution (LSB value)?

A. Range: $[-1, 1)$, Resolution: $2^{-15}$  
B. Range: $[-1, 1)$, Resolution: $2^{-16}$  
C. Range: $[-32768, 32767]$ (integers), Resolution: $1$  
D. Range: $[0, 1)$, Resolution: $2^{-16}$ (unsigned)

---

**Q2.** In fixed-point two's complement arithmetic, overflow wraps around (e.g., a positive result becomes negative). Saturation arithmetic instead clamps values at $\pm\text{MAX}$. Which implementation is typically preferred in audio and communications DSP and why?

A. Wrap-around, because it preserves the exact modular arithmetic of two's complement and never loses information.  
B. Saturation, because a clipped signal is less audibly objectionable and less likely to cause catastrophic errors than a wrapped-around signal.  
C. Wrap-around, because saturation requires more hardware gates and has higher latency.  
D. Neither — fixed-point DSP implementations always use floating-point fallback when overflow is detected.

---

**Q3.** A signal is uniformly quantised with a $b$-bit ADC. Assuming the quantisation error is uniformly distributed between $-\Delta/2$ and $\Delta/2$ (where $\Delta = 2^{1-b}$ for a full-scale range of $[-1, 1)$), the signal-to-quantisation-noise ratio (SQNR) for a full-scale sinusoidal input is approximately:

A. $\text{SQNR} \approx 6b\ \text{dB}$  
B. $\text{SQNR} \approx 6.02b + 1.76\ \text{dB}$  
C. $\text{SQNR} \approx 10b\ \text{dB}$  
D. $\text{SQNR} \approx 6.02b - 7.2\ \text{dB}$

---

**Q4.** In a Q$m$.Q$f$ fixed-point multiply of two Q$f$ numbers (same format), the product has twice as many fractional bits. To store the result back in Q$f$ format on a 16-bit word, you must:

A. Truncate the upper 16 bits of the 32-bit product.  
B. Right-shift the 32-bit product by $f$ bits and take the lower 16 bits.  
C. Right-shift the 32-bit product by $f$ bits and take the upper 16 bits.  
D. Left-shift the 32-bit product by $f$ bits before truncating.

---

**Q5.** A modern FPGA DSP slice (e.g., Xilinx DSP48E2) typically contains:

A. A 64-bit floating-point multiplier and accumulator.  
B. A pre-adder, an $18 \times 27$-bit multiplier, and a 48-bit post-adder/accumulator, enabling efficient MAC (multiply-accumulate) and MACC operations.  
C. Only an 8-bit multiplier — wider multiplications must be assembled from multiple slices.  
D. A barrel shifter and a CORDIC unit only.

---

**Q6.** Pipelining a DSP computation (e.g., a multiply-accumulate chain) adds register stages between combinational blocks. The primary benefit is:

A. Reduced total computation time for a single data sample (lower latency).  
B. Higher throughput — the clock frequency can be increased because each pipeline stage has a shorter critical path, allowing one result per clock cycle despite multi-cycle computation.  
C. Reduced hardware area because pipeline registers replace combinational logic.  
D. Elimination of all timing hazards without any additional control logic.

---

**Q7.** The CORDIC (Coordinate Rotation Digital Computer) algorithm computes trigonometric functions using only:

A. Multiplications and table lookups  
B. Additions, subtractions, and bit-shifts (no multiplications)  
C. The Taylor series with fixed-precision polynomial evaluation  
D. Square root operations applied iteratively to the input angle

---

**Q8.** In a CIC decimation filter of order $N$ with decimation ratio $R$, the integrator section accumulates values up to a maximum. The number of bits required to prevent overflow in the integrator registers (bit growth) relative to the input word width of $B_{in}$ bits is:

A. $B_{CIC} = B_{in} + N \cdot R$  
B. $B_{CIC} = B_{in} + N \cdot \log_2(R)$ (approximately)  
C. $B_{CIC} = B_{in} + N \cdot \lceil\log_2(R)\rceil$ bits  
D. $B_{CIC} = B_{in} \cdot N \cdot R$

---

**Q9.** Limit cycles in fixed-point recursive (IIR) filters are:

A. Oscillations caused by the non-linearity of fixed-point rounding that persist even when the input is zero, due to the quantiser trapping the state in a small orbit.  
B. Oscillations caused by coefficient quantisation changing the pole locations outside the unit circle.  
C. Oscillations observed only in filters with poles at exactly $z = 1$ (DC).  
D. Oscillations that occur only when the filter input exceeds the quantiser's dynamic range.

---

**Q10.** To suppress zero-input limit cycles in a second-order IIR section, one effective technique is:

A. Increasing the filter order to reduce the effect.  
B. Using magnitude truncation (instead of rounding) for the state variable quantisation, which guarantees the state magnitude cannot increase.  
C. Replacing the IIR section with an equivalent FIR approximation.  
D. Reducing the step size to zero to prevent any state update.

---

**Q11.** A 16-bit fixed-point IIR filter is designed with a pole pair very close to the unit circle at $z = r e^{\pm j\omega_0}$ with $r = 0.9999$. The pole angle $\omega_0 = \pi/2$ (corresponding to a resonance at $f_s/4$). Why is coefficient representation particularly problematic here?

A. The coefficients are always irrational numbers for poles near the unit circle.  
B. The pole is very close to the unit circle, so tiny rounding errors in the feedback coefficients $a_1 = -2r\cos\omega_0$ and $a_2 = r^2$ cause large relative perturbations to the pole radius, potentially moving the pole outside the unit circle and causing instability.  
C. Fixed-point representations cannot represent angles close to $\pi/2$.  
D. The coefficient $a_2 = r^2 \approx 1$ is indistinguishable from 1.0 in most fixed-point formats.

---

**Q12.** In a direct-form II IIR filter, the internal state nodes (delay register values) can overflow even when the input and output are within the valid fixed-point range. The recommended solution for fixed-point implementation is:

A. Increase the input signal level to use the full dynamic range.  
B. Implement the filter as a cascade of second-order sections (SOS) with appropriate scaling between sections to prevent overflow while minimising quantisation noise.  
C. Use only FIR filters, which do not have internal state.  
D. Apply a global gain reduction of 6 dB before the filter.

---

**Q13.** A DSP algorithm requires computing $\arctan(y/x)$ in real time on an FPGA without using a hardware divider or trigonometric LUT. The best approach is:

A. Newton-Raphson iteration for the reciprocal of $x$, then a polynomial approximation for $\arctan$.  
B. CORDIC vectoring mode: iteratively rotate the vector $(x, y)$ toward the x-axis using shift-and-add operations; the accumulated rotation angle converges to $\arctan(y/x)$.  
C. A piecewise linear lookup table with 256 entries covering $[0, \pi/4]$.  
D. Compute $\sqrt{x^2 + y^2}$ first, then use the law of cosines.

---

**Q14.** A 24-bit fixed-point accumulator is used in a DSP48 slice to sum 16 filter tap products, each contributing up to $\pm 2^{23}$. What minimum accumulator width is needed to prevent overflow?

A. 24 bits  
B. 28 bits  
C. 32 bits  
D. 48 bits

---

**Q15.** The coefficient sensitivity problem in high-order IIR filters implemented in direct form is caused by:

A. Floating-point rounding errors in the filter design tool.  
B. All poles being expressed as roots of a single high-degree polynomial in $z$: small changes in the polynomial coefficients cause large movements of the roots (poles), since high-degree polynomial roots are sensitive to perturbations.  
C. The direct form structure requiring more multiplications than the cascade form.  
D. High-order direct form filters consuming excessive FPGA LUT resources.

---

**Q16.** In Q1.15 format (1 sign bit, 15 fractional bits), the multiplication of two Q1.15 numbers yields a Q2.30 result in 32 bits. Before storing back to Q1.15, a programmer shifts right by 15 bits. What additional step is often needed to maintain accuracy?

A. A left-shift by 1 to compensate for the sign bit alignment.  
B. Rounding the bit shifted out (adding 1 to the LSB position before truncating) to reduce truncation bias and reduce quantisation noise power by 3 dB on average.  
C. Negating the result if the sign bit of the original product is 1.  
D. Dividing by 2 to account for the scaling difference between Q1.15 and Q2.30.

---

**Q17.** A CIC filter with $N = 3$ stages and $R = 64$ is implemented in fixed-point. The input word width is 16 bits. How many bits are required in the integrator registers to guarantee no overflow?

A. 16 bits  
B. 22 bits  
C. 34 bits  
D. 34 bits — using $B_{out} = B_{in} + N\lceil\log_2 R\rceil = 16 + 3 \times 6 = 34$ bits

---

## Answer Key

| Q | Answer |
|---|--------|
| 1 | A |
| 2 | B |
| 3 | B |
| 4 | C |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | C |
| 9 | A |
| 10 | B |
| 11 | B |
| 12 | B |
| 13 | B |
| 14 | B |
| 15 | B |
| 16 | B |
| 17 | D |

---

## Detailed Explanations

**Q1 — Answer: A**

In Q15 format (also written Q0.15 or Q1.15 depending on convention — here Q15 means 15 fractional bits in a 16-bit word with 1 sign bit), the value represented is:

$$x = -b_{15} + \sum_{k=0}^{14} b_k \cdot 2^{k-15}$$

The range is $[-1, +1 - 2^{-15}]$, commonly written $[-1, 1)$. The resolution (one LSB) is $2^{-15} \approx 3.05 \times 10^{-5}$. Note: the most negative value is exactly $-1$, but the most positive is $1 - 2^{-15}$ (not $+1$) due to two's complement asymmetry. Option B confuses Q15 with Q16. Option C describes a 16-bit integer (Q0). Option D describes an unsigned format.

---

**Q2 — Answer: B**

Wrap-around overflow causes a large positive value to suddenly become a large negative value (or vice versa), which in audio produces a loud click or distortion that is highly objectionable. In control and communications, wrap-around can cause algorithms to diverge catastrophically. Saturation clamps the output at $\pm\text{MAX}$, producing flat-topped clipping — still distortion, but bounded and usually far less damaging. Most professional audio DSPs and communication processors provide saturation arithmetic modes (e.g., ARM Cortex-M `QADD` instruction, FPGA DSP slice overflow handling). Option A is factually wrong about preserving information. Options C and D are false in modern implementations.

---

**Q3 — Answer: B**

For a full-scale sinusoidal input $x(t) = A\sin(2\pi ft)$ with $A$ equal to half the ADC full-scale range:
- Signal power: $A^2/2$
- Quantisation noise power: $\Delta^2/12$ where $\Delta = A \cdot 2^{1-b}$

$$\text{SQNR} = \frac{A^2/2}{\Delta^2/12} = \frac{A^2/2}{A^2 \cdot 2^{2-2b}/12} = \frac{3}{2} \cdot 2^{2b} = 1.5 \cdot 4^b$$

In dB: $10\log_{10}(1.5) + 20b\log_{10}(2) = 1.76 + 6.02b\ \text{dB}$. Option A is a rough approximation (6 dB/bit) commonly used as a rule of thumb but misses the 1.76 dB constant. Option C (10 dB/bit) is incorrect. Option D has the wrong constant.

---

**Q4 — Answer: C**

When two Q$f$ numbers are multiplied, the result has $2f$ fractional bits and (for 16-bit inputs) is 32 bits wide with its binary point after bit $2f-1$ (from the LSB). To align the result back to Q$f$, you right-shift the 32-bit product by $f$ bits. After shifting, the upper 16 bits (bits $[31:16]$ of the shifted result, or equivalently bits $[31+f:16+f]$ of the original product) contain the Q$f$ result. Option B (lower 16 bits after shifting) is wrong — the integer and overflow bits are in the upper portion. Option A (upper 16 bits without shifting) is wrong — it extracts bits at the wrong binary point position. Option D (left-shift) would overflow massively.

---

**Q5 — Answer: B**

Xilinx DSP48E2 (UltraScale) and similar slices contain: a pre-adder (±27-bit input), an 18×27-bit two's complement multiplier producing a 45-bit result, and a 48-bit accumulator/post-adder with optional pipeline registers. This structure enables: FIR tap (pre-adder for symmetric FIR), MAC operation, multiply-accumulate chains at over 700 MHz with pipelining. Option A is wrong — DSP slices are fixed-point integer multipliers, not floating-point. Option C is wrong — 18×27 bits is available in a single slice. Option D describes CORDIC, which is typically implemented in logic fabric, not the DSP slice.

---

**Q6 — Answer: B**

Pipelining divides a multi-cycle computation into stages, inserting registers at the stage boundaries. Each stage takes one clock cycle, so the maximum clock frequency is determined by the slowest single stage (shortest critical path), not the entire computation. For example, a 4-stage multiplier that takes 4 ns without pipelining can be pipelined with 1 ns per stage, quadrupling the clock rate and throughput — but each individual result still takes 4 clock cycles (4 ns × 1 = 4 clock cycles at 4× the frequency). The throughput increases by 4× even though latency is unchanged in absolute time. Option A is wrong — latency in clock cycles increases with pipelining. Option C is wrong — registers add area. Option D is wrong — pipelining introduces data hazards that require stall/forwarding logic.

---

**Q7 — Answer: B**

CORDIC works by iteratively rotating a 2D vector using a sequence of fixed angle rotations of $\pm\arctan(2^{-i})$ for $i = 0, 1, 2, \ldots$. A rotation by $\arctan(2^{-i})$ can be performed using only a bit-shift by $i$ places and additions: $(x', y') = (x \mp 2^{-i}y,\ y \pm 2^{-i}x)$. After $N$ iterations, the vector has been rotated by the desired angle (in rotation mode) or rotated to the x-axis to compute $\arctan(y/x)$ (in vectoring mode). A scaling factor $K_N$ (product of $\cos(\arctan(2^{-i}))$) must be applied, but it converges to a constant ($\approx 0.6073$) and can be absorbed into a final multiply or pre-scale. This makes CORDIC ideal for FPGA implementations without DSP multipliers. Options A, C, and D require either multiplications or more complex operations.

---

**Q8 — Answer: C**

Each integrator in a CIC filter accumulates up to $R^N$ times the input value (DC gain is $R^N$). The bit growth required is the number of additional bits needed to represent $R^N$ times the input range:

$$B_{growth} = \lceil \log_2(R^N) \rceil = N \lceil \log_2(R) \rceil$$

Total width: $B_{CIC} = B_{in} + N\lceil\log_2 R\rceil$. For example, $N=3$, $R=64$: $B_{growth} = 3 \times 6 = 18$ additional bits. Option A ($N \cdot R$) is far too large — it applies a linear rather than logarithmic growth. Option B omits the ceiling function; since bit widths must be integers, the ceiling is essential. Option D would require an astronomically large number of bits.

---

**Q9 — Answer: A**

Limit cycles arise from the non-linear quantisation operation (rounding or truncation) in the feedback path of a fixed-point IIR filter. Even with zero input, if the filter's state variables enter a small set of values that form a cycle under the quantised recursion, they will oscillate indefinitely. The quantiser effectively traps the state into a periodic orbit. These are distinct from instability (which causes exponential growth): limit cycle amplitudes are bounded but non-zero. Option B describes quantisation of coefficients causing instability, not limit cycles per se. Option C is too restrictive — limit cycles can occur in filters with poles anywhere, not only at DC. Option D confuses limit cycles with overflow oscillations.

---

**Q10 — Answer: B**

Magnitude truncation means rounding the state variable toward zero (i.e., truncating the magnitude, not the binary value). This guarantees that the quantised state magnitude can never exceed the true (unquantised) state magnitude. Under zero input, the state magnitude is therefore non-increasing, and since the state is discrete, it must eventually reach zero — eliminating the zero-input limit cycle. Option A (increasing filter order) would make limit cycles worse. Option C (replacing with FIR) would work but defeats the purpose of using an IIR filter (efficiency). Option D is nonsensical — setting the step size to zero stops all filtering.

---

**Q11 — Answer: B**

For a pole pair at $re^{\pm j\omega_0}$, the feedback coefficients are $a_1 = -2r\cos\omega_0$ and $a_2 = r^2$. At $\omega_0 = \pi/2$: $a_1 = 0$ and $a_2 = r^2 \approx 0.9998$. The pole radius is extremely sensitive to $a_2$: a change $\delta a_2$ moves the pole radius by $\delta r = \delta a_2 / (2r) \approx \delta a_2 / 2$. With 16-bit precision, the smallest representable change in $a_2$ is $2^{-15} \approx 3 \times 10^{-5}$, causing a pole radius perturbation of $\sim 1.5 \times 10^{-5}$. Since $r = 0.9999$, this represents a 15% relative perturbation to $(1-r) = 0.0001$ — enormous. The pole can easily move outside the unit circle, causing instability. Option A is wrong — rational approximations can represent these coefficients. Options C and D are false.

---

**Q12 — Answer: B**

The internal states in a direct-form II IIR filter represent an intermediate computation that blends input and feedback before splitting into output. The dynamic range of this intermediate value can greatly exceed both the input and output ranges. The standard solution is to use Second-Order Sections (SOS) / biquad cascade, where each biquad handles only one pair of poles and zeros. Between sections, a scaling coefficient normalises the signal level to prevent overflow in the next section while maximising the SNR (using all available bits). The $\ell_2$ or $\ell_\infty$ scaling criteria are commonly used. Option A is counterproductive. Option C avoids the problem but sacrifices IIR efficiency. Option D is a crude approximation that may be insufficient.

---

**Q13 — Answer: B**

CORDIC vectoring mode computes $\arctan(y/x)$ by iteratively rotating the vector $(x, y)$ toward the positive x-axis. At each step $i$, the vector is rotated by $\mp\arctan(2^{-i})$ depending on the sign of $y$. The accumulated angle converges to $\arctan(y/x)$ after $N$ iterations (where $N$ is the desired bit precision). Each iteration requires only 2 additions and 2 bit-shifts — no multipliers, no dividers, no trigonometric lookups. This is the standard approach for hardware angle computation in FPGAs and ASICs. Option A requires a hardware divider or iterative divide. Option C requires a LUT and interpolation hardware. Option D requires a square root and further computation.

---

**Q14 — Answer: B (28 bits)**

Each of the 16 tap products contributes up to $\pm 2^{23}$. Summing 16 such terms in the worst case gives $\pm 16 \times 2^{23} = \pm 2^4 \times 2^{23} = \pm 2^{27}$. To represent $\pm 2^{27}$ in two's complement requires 28 bits (1 sign bit + 27 magnitude bits, but since 2's complement represents $-2^{27}$ to $2^{27} - 1$, 28 bits suffice). Option A (24 bits) is too narrow — overflow occurs. Option C (32 bits) is safe but wasteful. Option D (48 bits) is the full DSP48 accumulator width, which is unnecessarily wide here. In practice, using 28-bit accumulators and downscaling to 24 bits at the output is efficient.

---

**Q15 — Answer: B**

A high-order direct-form IIR filter's transfer function is $H(z) = B(z)/A(z)$ where $A(z) = 1 + a_1 z^{-1} + \cdots + a_N z^{-N}$ is an $N$th-degree polynomial. The poles are roots of $A(z)$. For a high-degree polynomial, root sensitivity to coefficient perturbations is extremely high — Wilkinson's polynomial is the classic example, where tiny changes in one coefficient shift roots by enormous amounts. This is not a problem with the design tool but an intrinsic mathematical property of high-degree polynomials. Cascaded second-order sections avoid this by factoring $A(z)$ into quadratic factors, each of which is a low-degree polynomial with much better-conditioned roots. Options A, C, and D describe secondary issues, not the primary cause.

---

**Q16 — Answer: B**

After multiplying two Q1.15 numbers, the 32-bit result has 30 fractional bits (bits $[29:0]$ below the binary point, with the product binary point between bits $[29:30]$). Right-shifting by 15 brings the binary point to bit 15 (Q1.15 alignment). However, simply discarding the lower 15 bits introduces a truncation error biased toward negative values (always rounds toward $-\infty$ in two's complement). Rounding to nearest — adding $2^{14}$ (the value of bit 14, which is the first discarded bit) before truncating — makes the quantisation error zero-mean and reduces quantisation noise power by up to 3 dB compared to truncation. Option A (left-shift by 1) would cause overflow. Option C (negate based on sign bit) confuses sign handling with rounding. Option D (divide by 2) would halve the signal level unnecessarily.

---

**Q17 — Answer: D**

Using the CIC bit growth formula $B_{out} = B_{in} + N\lceil\log_2 R\rceil$:
- $B_{in} = 16$ bits
- $N = 3$ (filter order / number of stages)
- $R = 64$, so $\lceil\log_2(64)\rceil = \lceil 6 \rceil = 6$ bits

$$B_{out} = 16 + 3 \times 6 = 16 + 18 = 34\ \text{bits}$$

Options A (16 bits) and B (22 bits) are insufficient — overflow would occur. Option C says 34 bits but without showing the derivation, while option D explicitly states the derivation with the correct result. The 34-bit integrators must be implemented in hardware (e.g., using multiple DSP slices or wide adder trees on the FPGA fabric). After the CIC, a compensation FIR filter typically truncates the word width back to 16 or 24 bits with appropriate rounding.
