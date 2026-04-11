# DSP on FPGA — Interview Questions

## Overview

FPGA-based DSP implementation combines the reconfigurability of software with hardware-level throughput and latency. Interviewers in FPGA, hardware, and signal processing roles test understanding of DSP slice architecture, pipeline design, resource trade-offs, and real-time constraints. Systolic arrays, CORDIC, and clock domain crossing are common deep-dive topics.

---

## Tier 1: Fundamentals

### Q1. What are DSP slices on an FPGA and what operations do they accelerate?

**Answer:**

DSP slices (Xilinx calls them DSP48E2; Intel/Altera calls them DSP blocks) are hard-wired, pre-placed arithmetic units embedded in the FPGA fabric. They are significantly more efficient than equivalent LUT-based arithmetic.

**Xilinx DSP48E2 composition (UltraScale+):**

```
Pre-adder (27-bit signed) → A:B input registers
         ↓
Multiplier (27 × 18 = 45-bit product)
         ↓
Post-adder/subtractor (48-bit ACOUT/P accumulator)
         ↓
Pattern detector / SIMD logic
```

**Key parameters (DSP48E2):**
- A input: 30 bits (fed to pre-adder)
- B input: 18 bits
- Multiplier: $27 \times 18 = 45$-bit full product
- Accumulator P: 48 bits
- Internal pipeline registers: 3 stages (A1, A2, M, P)

**Accelerated operations:**

| Operation | DSP48E2 configuration | Usage |
|---|---|---|
| Multiply-accumulate (MAC) | Cascade P with PCIN | FIR filters |
| Complex multiply | 3 DSPs (Karatsuba) | OFDM, channel estimation |
| Pre-add + multiply | Use pre-adder | Symmetric FIR (halve multipliers) |
| Accumulate only | Bypass multiplier | Accumulators, counters |
| SIMD (dual 24-bit add) | SIMD mode | Pipelined summation |

**Efficiency advantage:** A single DSP slice uses $\approx 1/8$ the LUTs of an equivalent LUT-based multiplier and runs $2 \times\text{–}3 \times$ faster. For a 64-tap FIR, this means 64 DSP slices versus $\approx 1500$ LUTs — a major fabric saving.

---

### Q2. What is pipelining in FPGA DSP design and how does it increase throughput?

**Answer:**

Pipelining breaks a combinational computation into stages separated by registers. Each stage performs part of the work; all stages operate simultaneously on different data words.

**Example — 4-stage pipelined multiplier:**

```
Stage 1 (Reg A): Load operands
Stage 2 (Reg B): Partial product generation
Stage 3 (Reg C): Partial product summation
Stage 4 (Reg D): Final addition and output
```

**Throughput vs. latency:**

- **Throughput**: One result per clock cycle (after initial pipeline fill of $L$ cycles)
- **Latency**: $L$ clock cycles from input to output
- **Critical path**: Reduced from the full computation delay to the longest single stage, allowing higher $f_{clk}$

**Example:** A 16×16-bit multiplier with combinational delay of 10 ns (100 MHz limit) can be pipelined into 5 stages of 2 ns each, operating at 500 MHz — 5× throughput improvement.

**DSP48E2 internal pipeline:** The pre-defined registers (A1/A2/M/P) in DSP48E2 form a natural 3-stage pipeline. Enabling all registers allows operation at 600+ MHz on modern UltraScale+ devices.

**Pipelining cost:**
- Extra registers (flip-flops) — usually cheap on FPGAs
- Latency: the pipeline must be flushed and refilled at block boundaries
- Registered data paths must be carefully aligned (data must propagate through the pipeline in step)

---

### Q3. Describe the systolic FIR filter architecture on FPGA. Why is it preferred for high-order filters?

**Answer:**

A **systolic array** is a network of processing elements (PEs) where data flows rhythmically in fixed directions, like blood through a heart. Each PE computes locally and passes results to its neighbour.

**Systolic FIR architecture:**

For an $N$-tap FIR $y[n] = \sum_{k=0}^{N-1} h[k] x[n-k]$:

```
x[n] →→→ [PE0: h[0]] → [PE1: h[1]] → [PE2: h[2]] → ... → [PE(N-1): h[N-1]]
             ↓               ↓               ↓                       ↓
           p0[n]           p1[n]           p2[n]                  p(N-1)[n]
             ↓               ↓               ↓                       ↓
           acc →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→ y[n]
```

Each PE $k$ holds coefficient $h[k]$, receives $x[n-k]$, computes $h[k] \cdot x[n-k]$, and adds to the accumulating sum forwarded from PE $k-1$.

**Why preferred for high-order filters:**

1. **Regularity**: All PEs are identical → straightforward RTL coding and place-and-route.
2. **Local connectivity**: Each PE only connects to its two neighbours. No global wires → better timing closure.
3. **Scalability**: Adding taps means adding PEs; the critical path remains constant (one PE delay) regardless of $N$.
4. **DSP slice mapping**: Each PE maps to exactly one DSP48E2 cascade. Xilinx tools infer this from `POUT → PCIN` connections.

**Comparison:**

| Architecture | Taps per clock | Latency | FPGA resource |
|---|---|---|---|
| Direct (serial) | $N$ (time-multiplexed) | $N$ cycles | 1 DSP, large MUX |
| Fully parallel | 1 (same speed) | $N$ cycles | $N$ DSPs |
| Systolic | 1 | $N$ + pipeline stages | $N$ DSPs |
| Polyphase decimator | $M$ taps/clock | $M \times N/M$ | $M$ DSPs |

For real-time high-rate applications (e.g., 1 Gsample/s), the systolic fully parallel approach is mandatory.

---

### Q4. What is clock domain crossing (CDC) in DSP systems and how is it handled?

**Answer:**

Clock domain crossing occurs when a signal produced in one clock domain (with clock $clk_A$) is consumed in another clock domain (with clock $clk_B$) where $clk_A$ and $clk_B$ are asynchronous (no known phase or frequency relationship).

**The problem — metastability:** If a flip-flop captures a signal that is changing at the moment of the clock edge, the Q output enters a metastable state (neither 0 nor 1) that may persist for an arbitrarily long time. The probability of metastability lasting longer than $t_{resolve}$ is:

$$P_{meta}(t) \propto e^{-t_{resolve}/\tau_{meta}}$$

where $\tau_{meta} \approx 50\text{–}100$ ps for modern FPGAs.

**DSP CDC scenarios:**

1. **ADC samples arriving at $f_{ADC}$, processed at $f_{DSP}$**: Common in SDR systems where the ADC runs at 250 MHz (asynchronous) and the DSP fabric runs at 200 MHz.
2. **Configuration registers from a CPU bus at 100 MHz into a DSP core at 500 MHz**.
3. **Control/status signals crossing between baseband clock and protocol clock**.

**CDC handling techniques:**

| Signal type | Technique | Notes |
|---|---|---|
| Single-bit control | Two-flop synchroniser | Standard; suits low-frequency signals |
| Multi-bit data bus | Handshake (req/ack) | Ensures bus stability during sampling |
| High-throughput data | Asynchronous FIFO | Gray-coded read/write pointers cross the boundary |
| Pulse | Pulse synchroniser (toggle-sync) | Convert pulse to level, synchronise, re-edge-detect |

**Asynchronous FIFO for DSP:** The most common CDC structure for sample streams. The FIFO has dual-port RAM; write pointer in $clk_A$ domain, read pointer in $clk_B$ domain. Pointers are converted to Gray code before crossing to ensure only one bit changes per pointer increment, making synchronisation safe.

---

## Tier 2: Intermediate

### Q5. Explain the CORDIC algorithm and its use in FPGA DSP. What operations does it compute?

**Answer:**

**CORDIC** (COordinate Rotation DIgital Computer) is an iterative algorithm that computes trigonometric, hyperbolic, and other transcendental functions using only shifts and adds — no multipliers.

**Rotation principle:** Starting from an initial vector $(x_0, y_0)$, perform $N$ micro-rotations by angles $\pm \arctan(2^{-i})$:

$$x_{i+1} = x_i - d_i \cdot y_i \cdot 2^{-i}$$
$$y_{i+1} = y_i + d_i \cdot x_i \cdot 2^{-i}$$
$$z_{i+1} = z_i - d_i \cdot \arctan(2^{-i})$$

where $d_i = \text{sgn}(z_i)$ for rotation mode (drives $z \to 0$) or $d_i = -\text{sgn}(y_i)$ for vectoring mode (drives $y \to 0$).

**Scaling factor:** After $N$ iterations, the vector magnitude is scaled by $K_N = \prod_{i=0}^{N-1} \cos(\arctan(2^{-i})) \approx 0.60725$. Pre-scale inputs by $1/K_N$ or compensate after.

**Operations computed:**

| Mode | Input | Computes | Application |
|---|---|---|---|
| Rotation | $(x_0, 0, z_0)$ | $(\cos z_0, \sin z_0)$ | Sin/cos generation, NCO |
| Vectoring | $(x_0, y_0, 0)$ | magnitude, $\arctan(y_0/x_0)$ | Phase/magnitude extraction, carrier recovery |
| Hyperbolic | $(x_0, y_0, 0)$ | $\cosh$, $\sinh$, $e^x$ | Equalisation, AGC |

**FPGA advantages:**
- Each iteration requires only 2 shifts, 2 adds, and 1 sign comparison — maps to very low LUT count
- Fully pipelined at 1 iteration per pipeline stage → produces 1 result per clock cycle with latency of $N$ cycles
- $N = 16$ iterations gives 16-bit precision (1 bit per iteration)

**Typical use in SDR:** CORDIC replaces the NCO+multiplier in a phase rotator for CFO correction:
```
(I + jQ) × e^{j\theta} computed via CORDIC rotation with angle θ
```

---

### Q6. How does polyphase decomposition enable efficient multi-rate FIR filtering on FPGA?

**Answer:**

**Problem:** A decimation-by-$M$ filter computes $y[n] = \sum_{k=0}^{L-1} h[k] x[nM - k]$. If computed naively, all $L$ multiplications are done at the input rate $f_s$, but only every $M$-th output is kept — waste of $M-1$ out of every $M$ computations.

**Polyphase decomposition:** Decompose $h[k]$ into $M$ sub-filters (polyphase components):

$$h_p[n] = h[nM + p], \quad p = 0, 1, \ldots, M-1, \quad n = 0, \ldots, L/M - 1$$

Each polyphase sub-filter $h_p$ has length $L/M$.

**Result:** The output at the lower rate is:

$$y[n] = \sum_{p=0}^{M-1} \sum_{k=0}^{L/M-1} h_p[k] \cdot x[nM - k \cdot M - p]$$

Equivalently: $y[n]$ is the sum of $M$ outputs, each computed at the output rate $f_s/M$ using $L/M$ taps. Total computation: $M \times (L/M) = L$ multiplications per output sample — the same work, but now all done at $f_s/M$ (the output rate), not $f_s$.

**FPGA architecture for polyphase decimation FIR:**

1. Time-multiplex the $M$ polyphase filters using a single bank of $L/M$ DSP slices
2. The commutator switches input samples to the appropriate sub-filter at the input rate
3. Each sub-filter outputs at $f_s/M$; results are accumulated at the output rate

**Resource saving:** $L$ DSP slices operating at $f_s$ (direct) vs. $L/M$ DSP slices running $M \times$ time-multiplexed (polyphase). For $M = 8$ decimation with 64 taps: 64 vs. 8 DSP slices.

---

### Q7. Explain resource utilisation trade-offs: LUTs vs. DSPs vs. BRAMs in FPGA DSP.

**Answer:**

FPGA resources are finite and must be balanced. An efficient DSP design maximises DSP-slice utilisation for arithmetic and reserves LUTs for control logic.

**DSP slices:**
- Best for: multiplications $\leq 27 \times 18$ bits, MAC operations, accumulation
- Cost: each DSP uses $\sim 600$ equivalent LUTs; limit is typically $\sim 1$ DSP per 50–100 LUTs in the fabric
- Constraint: DSP cascade chain limits routing flexibility; over-cascading increases routing complexity

**LUTs:**
- Best for: address decode, control finite state machines, small lookup tables, narrow arithmetic ($\leq 6$-bit multiplications using LUT ROMs)
- Inference: Wide bus muxes, combinational logic for error detection, coefficient loading

**BRAMs (Block RAMs):**
- Best for: coefficient storage for large FIR (hundreds of taps), sample delay buffers, look-up tables for CORDIC pre-computation
- Size: 18 Kbit or 36 Kbit per BRAM on Xilinx; dual-port (one read + one write per cycle)
- Trade-off: Using BRAM for a small 16-entry coefficient table wastes a 36 Kbit resource; use distributed RAM (LUT-RAM) for $\leq 64$ entries

**Typical DSP application allocations (64-tap FIR at 250 MHz):**

| Resource | Count | Notes |
|---|---|---|
| DSP48E2 | 64 | One per tap in systolic chain |
| BRAM | 0 | Coefficients stored in DSP registers |
| LUTs | ~100 | Input sample shift register control |
| FF | ~200 | Pipeline registers |

**Practical guideline:** Profile DSP-to-LUT ratio (should be $\leq 1:10$ for routing congestion), check DSP cascade chain depth against timing closure needs, and use BRAM for coefficient tables when $> 256$ taps or when coefficients need run-time programmability.

---

### Q8. How would you implement a complex multiplier on FPGA using DSP slices? What is the Karatsuba optimisation?

**Answer:**

**Naive complex multiply:** $(a + jb)(c + jd) = (ac - bd) + j(ad + bc)$

Requires 4 real multiplications and 2 additions.

**FPGA cost:** 4 DSP48E2 slices (or 2 if using 27-bit pre-adder to fold operations).

**Karatsuba's algorithm:** Observe that:

$$\text{Real part: } ac - bd$$
$$\text{Imag part: } (a+b)(c+d) - ac - bd$$

Compute $k_1 = ac$, $k_2 = bd$, $k_3 = (a+b)(c+d)$.

Then: $\text{Real} = k_1 - k_2$, $\text{Imag} = k_3 - k_1 - k_2$.

**FPGA cost:** **3 multiplications** (DSP slices) plus 3 additions (cheap in LUTs or accumulated into DSP P register).

**DSP48E2 implementation:**

```
DSP0: P0 = a * c          (k1)
DSP1: P1 = b * d          (k2)
DSP2: P2 = (a+b) * (c+d)  (k3) — uses pre-adder for (a+b) and (c+d)

Real = P0 - P1
Imag = P2 - P0 - P1
```

The pre-adder in DSP48E2 computes $(a+b)$ and $(c+d)$ without extra logic. This truly fits in 3 DSPs with no extra LUTs for the adders.

**Latency:** With all registers enabled, 3 pipeline stages. All three DSPs run in parallel (same latency), so throughput is 1 complex multiply per clock.

**Use in OFDM:** The FFT butterfly requires one complex multiply per butterfly stage. For a 2048-point FFT with $N/2 \log_2 N = 1024 \times 11 = 11264$ butterflies, using 3-multiplier complex multiply saves 33% DSP resources compared to 4-multiplier.

---

## Tier 3: Advanced

### Q9. Design a pipelined 64-tap FIR filter targeting 500 MHz on an UltraScale+ FPGA. Discuss architecture, timing, and verification.

**Answer:**

**Architecture: Systolic cascade of DSP48E2 slices**

With 64 taps and a requirement of 500 MHz, the key constraint is timing closure on the DSP cascade chain.

**Timing analysis:**

- DSP48E2 cascade path: $t_{PCIN \to POUT} \approx 0.9$ ns (register-to-register in cascade)
- Maximum cascade chain length at 500 MHz: $f_{clk} = 500$ MHz → $T_{clk} = 2$ ns → maximum 2 DSPs per stage without additional registers

However, with all internal registers enabled (A1/A2/M/P), the register-to-register path through one DSP is well under 2 ns. The cascade connection `POUT → PCIN` adds $\approx 0.1$ ns routing delay per hop.

**Strategy for 64-tap at 500 MHz:**

1. Use all internal DSP48E2 pipeline registers (A1, A2, M, P).
2. Implement the input data shift register as a dedicated SRL (Shift Register LUT) or BRAM shift register — do not use flip-flops for the 64-sample delay line (expensive in FFs).
3. Each DSP receives its coefficient from a ROM (distributed RAM or BRAM depending on width).
4. Verify the cascade timing meets setup requirements; Vivado timing analysis will flag any paths violating the target.

**Critical path concern:** The input data path to all 64 DSP A-ports introduces a fan-out of 64. Buffer the input with a register tree to ensure all DSPs receive data simultaneously without hold time violations.

**Symmetric FIR optimisation:** If $h[k] = h[N-1-k]$ (symmetric FIR — always true for linear phase), use the DSP48E2 pre-adder to compute $x[n-k] + x[n-(N-1-k)]$ before multiplying by $h[k]$. This halves the number of DSPs from 64 to 32.

**Verification:**

1. **RTL simulation**: Apply a known sinusoidal input, verify output amplitude and phase against MATLAB/Python reference model.
2. **Frequency response check**: Apply a swept-frequency sine, plot output amplitude — verify passband, transition, and stopband match specification.
3. **Timing simulation**: Post-implementation timing simulation catches metastability-free operation at full speed.
4. **Hardware test**: Use a signal generator → ADC → FPGA → DAC chain; measure output spectrum on a spectrum analyser.

---

### Q10. Explain how to handle finite precision effects in an FPGA FIR filter when targeting 16-bit input and output with 18-bit coefficients.

**Answer:**

**Bit growth analysis:**

- Input: 16-bit signed (Q15)
- Coefficient: 18-bit signed (Q17, for $|h[k]| \leq 1$)
- Product: $16 + 18 = 34$-bit intermediate (Q32)
- Accumulator (64 taps): $34 + \log_2(64) = 34 + 6 = 40$ bits needed for no overflow

**Step 1 — Accumulator width:** Use 40-bit or 48-bit accumulator. DSP48E2 has a 48-bit P register — perfectly suited.

**Step 2 — Input alignment:** The Q15 input must be right-aligned in the 27-bit A port and the Q17 coefficient in the 18-bit B port. Set the binary point tracking:
- A input: sign-extend Q15 to 27 bits (Q26 in the A port)
- B input: Q17 coefficient in 18-bit B
- Product binary point: Q43 (26 + 17 = 43 fractional bits)
- 48-bit accumulator: Q43 in the 48-bit P → 5 integer bits available, sufficient for 64-tap gain

**Step 3 — Output rounding:** The 48-bit accumulator result at Q43 must be rounded to 16-bit Q15 (Q15 output). This requires shifting right by $43 - 15 = 28$ bits with round-half-up:

```vhdl
-- Add rounding constant at bit 27 (= 2^(28-1) = 2^27)
y_round <= acc_48bit + x"0000008000000";  -- bit 27 = 1
y_out   <= y_round(42 downto 27);         -- extract Q15 bits [42:27]
```

**Step 4 — Overflow protection:** Ensure the maximum filter gain $\sum |h[k]|$ does not exceed the accumulator capacity. For a lowpass filter designed with unity gain ($\sum h[k] = 1$), the maximum output equals the maximum input — no overflow. For bandpass filters or non-unity gain, check $\sum |h[k]|$ explicitly and add guard bits if needed.

**Simulation verification:** Compare fixed-point RTL output to double-precision floating-point reference at the bit level. Accept differences of $\leq 1$ LSB (from rounding).

---

## Common Interview Mistakes

1. **Ignoring DSP cascade latency alignment**: In a cascaded FIR, data and coefficients must be pipe-aligned to the cascade chain. Misaligned data produces incorrect outputs that are very hard to debug in simulation.
2. **Underestimating routing congestion**: Placing 256 DSP slices all requiring connections to a common input register creates extreme fan-out. Always add input registers or a distribution tree.
3. **Forgetting CDC**: Any signal crossing between the DSP fabric clock and another domain (AXI config bus, ADC clock) must go through a proper synchroniser. Missing CDC is a leading cause of intermittent hardware failures.
4. **Using LUT-RAMs for large coefficient tables**: For $> 256$ coefficients, BRAM is far more efficient. LUT-RAMs should be reserved for small, latency-critical lookup tables.
5. **Not using symmetric FIR optimisation**: For any linear-phase FIR (the most common case), halving the DSP count via the pre-adder is straightforward and should always be done.
