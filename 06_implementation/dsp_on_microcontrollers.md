# DSP on Microcontrollers — Interview Questions

## Overview

Microcontroller-based DSP is ubiquitous in audio, motor control, medical devices, and IoT. Interviewers for embedded systems and firmware roles test knowledge of CMSIS-DSP, real-time constraints, DMA streaming, cache management, and SIMD instruction sets. The central tension is between computational throughput, memory bandwidth, and power consumption.

---

## Tier 1: Fundamentals

### Q1. What is the ARM CMSIS-DSP library and why is it preferred over hand-written code?

**Answer:**

CMSIS-DSP (Cortex Microcontroller Software Interface Standard — Digital Signal Processing) is ARM's open-source library of optimised DSP functions for Cortex-M processors. Available at: github.com/ARM-software/CMSIS-DSP.

**Contents:** Over 60 categories including:
- FIR and IIR filters (float32, Q31, Q15, Q7)
- FFT/IFFT (radix-2, radix-4, real/complex)
- Matrix operations
- Statistics (mean, variance, RMS, min, max)
- Motor control (sin/cos, Clarke/Park transforms)
- Complex math, vector math, interpolation

**Why prefer CMSIS-DSP over hand-written code:**

1. **Architecture-specific optimisation**: Functions are hand-tuned in C and assembly using:
   - Cortex-M4/M7 DSP extension instructions (SIMD: `SMLAD`, `SMLABT`, etc.)
   - Cortex-M33 helium (M-Profile Vector Extension) on newer cores
   - Cortex-M7 FPU instructions (VFMA, VLDM, VSTM)

2. **Tested correctness**: NASA, medical device, and automotive applications rely on CMSIS-DSP; the library has extensive testing.

3. **Portability**: Same function signature works across M0 through M55; compiler selects the best implementation.

4. **Time to market**: Implementing a Q15 biquad cascade correctly with correct overflow handling, coefficient scaling, and rounding takes days; CMSIS-DSP provides it in one function call.

**Example — Q15 FIR filter:**

```c
#include "arm_math.h"

#define NUM_TAPS    32
#define BLOCK_SIZE  64

arm_fir_instance_q15 S;
q15_t pCoeffs[NUM_TAPS] = { /* filter coefficients in Q15 */ };
q15_t pState[NUM_TAPS + BLOCK_SIZE - 1];  // state buffer

arm_fir_init_q15(&S, NUM_TAPS, pCoeffs, pState, BLOCK_SIZE);
arm_fir_q15(&S, pInput, pOutput, BLOCK_SIZE);  // processes BLOCK_SIZE samples
```

The `arm_fir_q15` function uses `SMLALD` (Signed Multiply Long Accumulate Dual) to compute two MACs per instruction on Cortex-M4.

---

### Q2. What is the difference between fixed-point and floating-point MCUs for DSP? How do you choose?

**Answer:**

**Fixed-point MCUs (Cortex-M0, M0+, M3):**
- No hardware floating-point unit
- All floating-point operations emulated in software (10–100× slower)
- DSP using `int16_t`/`int32_t` with manual Q-format tracking
- Power: ~10–50 mW total MCU power
- Cost: $0.20–$1.00

**FP-capable MCUs (Cortex-M4F, M7, M33, M55):**
- **M4F**: Single-precision FPU (ARM FPv4-SP); 32 S registers; SIMD DSP extensions
- **M7**: Single and double precision (FPv5-DP); tightly coupled memory; 6-stage pipeline
- **M33**: FPv5-SP, Trust Zone, optional SIMD DSP
- **M55**: FPv5, Helium (MVE) vector instructions; 8-lane SIMD for Q15

**Decision criteria:**

| Factor | Use fixed-point | Use floating-point |
|---|---|---|
| Power budget | Battery < 100 mW | Mains/USB powered |
| Algorithm complexity | FIR, simple IIR | Adaptive algorithms, ML |
| Dynamic range | Known, bounded signal | Wide-range or unknown input |
| Team expertise | DSP specialist available | General embedded team |
| Time to market | Long — careful Q-format design | Short — use float, optimise later |
| Cost sensitivity | High volume, cost-critical | Low volume or cost-insensitive |

**Practical guidance:** Start with floating-point to validate algorithm correctness, then port to fixed-point for production if power/cost targets demand it. Use CMSIS-DSP Q15/Q31 functions which handle the fixed-point machinery internally.

---

### Q3. What is DMA and why is it critical for real-time ADC/DAC streaming DSP?

**Answer:**

**DMA** (Direct Memory Access) is a hardware mechanism that transfers data between peripherals (ADC, DAC, UART, SPI) and memory without CPU intervention. The DMA controller handles the transfer; the CPU executes other code or sleeps.

**Why it is critical for streaming DSP:**

**Without DMA (polling or interrupt-per-sample):**

At $f_s = 48$ kHz, an interrupt fires every $1/48000 \approx 20.8$ µs. Each interrupt has overhead of ~30–50 cycles (register save/restore, context switch). At 168 MHz (Cortex-M4), 50 cycles = 0.3 µs — consuming 1.4% of CPU time just for interrupt overhead, before any processing. For stereo 16-bit PCM at 192 kHz, this becomes prohibitive.

**With DMA (double buffer or circular):**

The ADC fills a buffer of $N$ samples entirely autonomously. The DMA fires one interrupt per buffer ($N$ samples). CPU processes the complete buffer in a burst, achieving efficient cache utilisation and minimising interrupt overhead.

**Double-buffer (ping-pong) DMA:**

```
DMA fills Buffer A (ADC samples) while CPU processes Buffer B
DMA fills Buffer B while CPU processes Buffer A
↑ alternates every N samples
```

**STM32 example (HAL):**

```c
// Start circular DMA from ADC to ping-pong buffer
HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buf, 2 * BLOCK_SIZE);

// Callback fires at half-transfer (buffer A full) and full-transfer (buffer B full)
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc) {
    process_block(adc_buf, BLOCK_SIZE);          // Process first half
}
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    process_block(adc_buf + BLOCK_SIZE, BLOCK_SIZE);  // Process second half
}
```

**Timing requirement:** The CPU must finish processing $N$ samples before the DMA has filled the next buffer. If $T_{proc} > T_{fill} = N/f_s$, samples are lost (buffer overrun). The worst-case execution time (WCET) of the processing function must be bounded and verified.

---

### Q4. What are the ARM DSP extension instructions on Cortex-M4? How do they accelerate DSP?

**Answer:**

Cortex-M4 (and M33, M7) include **DSP extension instructions** defined in the ARMv7E-M architecture. These provide SIMD operations on 32-bit registers packed with two 16-bit or four 8-bit values.

**Key DSP instructions:**

| Instruction | Operation | Use case |
|---|---|---|
| `SMLAD` | $acc += (a_0 \times b_0) + (a_1 \times b_1)$ | Two MACs per cycle (Q15 FIR) |
| `SMLABT` | $acc += a_{top} \times b_{top}$ | Coefficient access optimisation |
| `SMLALD` | 64-bit $acc += (a_0 \times b_0) + (a_1 \times b_1)$ | Q15 with 64-bit accumulation |
| `PKHBT/PKHTB` | Pack two 16-bit halves into 32 bits | Data packing |
| `QADD16` | Saturating parallel add two 16-bit pairs | Overflow-safe addition |
| `QSUB16` | Saturating parallel subtract | |
| `SHADD16` | Halving add (average) | Rounding without overflow |
| `SMULBB` | $result = a_{bottom} \times b_{bottom}$ | Single Q15 multiply |

**Impact on FIR filter speed:**

A Q15 FIR loop without DSP extensions requires 1 MUL + 1 ADD per tap. With `SMLAD`:

```c
// Standard (2 taps, 2 cycles on M4):
acc0 += (int32_t)coeff[k] * data[k];       // 1 MUL, 1 ADD
acc0 += (int32_t)coeff[k+1] * data[k+1];   // 1 MUL, 1 ADD

// With SMLAD (2 taps, 1 cycle):
// Pack: coeff_packed = coeff[k] | (coeff[k+1] << 16)
// Pack: data_packed  = data[k]  | (data[k+1]  << 16)
__SMLAD(coeff_packed, data_packed, acc0);   // 1 cycle
```

The CMSIS-DSP `arm_fir_q15()` exploits `SMLAD` to compute 4 MACs per iteration (2 `SMLAD` per loop).

**Cortex-M55 Helium (MVE):** Goes further with 8-lane SIMD for Q15 and Q7, enabling up to 16 MACs per cycle, dramatically accelerating ML inference and audio DSP.

---

## Tier 2: Intermediate

### Q5. Explain real-time constraints in embedded DSP. How do you verify that timing requirements are met?

**Answer:**

**Real-time DSP constraint:** A DSP system operating at sample rate $f_s$ with block size $N$ has a deadline of:

$$T_{deadline} = \frac{N}{f_s}$$

The computation required per block must complete before this deadline every time, without exception.

**Example:** Audio processing at $f_s = 48$ kHz, $N = 128$ samples: $T_{deadline} = 128/48000 = 2.67$ ms.

**Real-time analysis steps:**

**1. Measure worst-case execution time (WCET):**

```c
DWT->CYCCNT = 0;          // Reset cycle counter (ARM DWT)
DWT->CTRL |= 0x1;         // Enable counter
process_block(input, output, N);
uint32_t cycles = DWT->CYCCNT;
float wcet_ms = (float)cycles / SystemCoreClock * 1000.0f;
```

Measure across many input vectors, including worst-case patterns (all maximum values, checkerboard patterns).

**2. Identify bottlenecks:** Use profiling (ITM trace, ETM trace, or cycle counting per section).

**3. Verify real-time headroom:**

$$\text{CPU load} = \frac{\text{WCET}}{T_{deadline}} \times 100\% < 80\%$$

Leave 20% headroom for interrupt latency, other tasks, and measurement uncertainty.

**4. Priority and interrupt handling:** In an RTOS, assign the DSP processing task the highest priority. Ensure interrupt service routines (ISRs) for non-DSP tasks have bounded latency. In bare-metal, disable non-critical interrupts during the processing burst.

**Common failure modes:**

| Problem | Symptom | Fix |
|---|---|---|
| Overrun | Audio glitch/click (buffer N+1 overwrites buffer N) | Reduce algorithm complexity or increase buffer size |
| Cache miss | Unpredictable execution time variation | Pre-load coefficients into DTCM; align arrays to cache lines |
| DMA collision | ADC/DAC stutter | Use separate DMA channels with different priorities |

---

### Q6. How do cache effects impact DSP performance on Cortex-M7? What mitigation strategies apply?

**Answer:**

Cortex-M7 has:
- **I-cache**: 4 or 16 KB instruction cache
- **D-cache**: 4 or 16 KB data cache (write-back or write-through)
- **TCM**: Tightly Coupled Memory (DTCM/ITCM) — zero-wait-state SRAM, no cache needed

**Cache miss cost:** An L1 miss accesses SRAM through the AHB bus: typically 3–8 additional cycles. An access to external SDRAM adds 20–50 cycles per miss.

**How DSP algorithms are affected:**

**FIR filter (length $L = 256$, sample data array length 512):**

- Coefficient array: $256 \times 4$ bytes = 1 KB — fits in D-cache
- Sample circular buffer: $512 \times 4$ bytes = 2 KB — fits in D-cache
- Total working set: 3 KB — fits in M7's 4 KB D-cache (typical) → cache-friendly

**FFT (N = 4096, complex float32):**

- Input/output buffer: $4096 \times 8$ bytes = 32 KB — does NOT fit in 16 KB D-cache
- Twiddle factor table: $4096 \times 8$ bytes = 32 KB — does NOT fit
- Total working set: 64 KB → severe cache thrashing → highly variable execution time

**Mitigation strategies:**

1. **Place hot data in DTCM:** Declare the filter state buffer and coefficient array in DTCM:
   ```c
   __attribute__((section(".dtcm"))) q15_t filter_state[NUM_TAPS + BLOCKSIZE];
   ```
   DTCM has 0 wait-states — consistently fast, no cache effects.

2. **Align buffers to cache line (32 bytes on M7):**
   ```c
   __attribute__((aligned(32))) float32_t fft_input[2048];
   ```
   Prevents a single array element from spanning two cache lines.

3. **Cache maintenance before DMA transfers:** When DMA writes to memory that the CPU will read, invalidate the D-cache region before CPU access:
   ```c
   SCB_InvalidateDCache_by_Addr((uint32_t*)dma_buf, BUF_SIZE_BYTES);
   ```
   Otherwise, the CPU reads stale cached data, not the new DMA values.

4. **Pre-fetch**: Structure memory access patterns to be sequential rather than random — the M7 hardware pre-fetcher handles sequential access efficiently.

---

### Q7. Describe the real-time audio processing pipeline on an ARM Cortex-M4 MCU. What are the key design choices?

**Answer:**

**System components:**

```
Microphone → ADC → DMA → [Ping buffer A / Pong buffer B] → DSP → DMA → DAC → Speaker
```

**Design choices:**

**1. Sample rate selection ($f_s$):**
- Speech intelligibility: 8 kHz sufficient (narrowband telephone quality)
- Audio quality: 44.1 kHz or 48 kHz (CD quality)
- Ultrasonic (sonar, bat detection): 192–250 kHz (MCU at edge of capability)

**2. Block size $N$ trade-off:**

| Small $N$ (e.g., 32) | Large $N$ (e.g., 256) |
|---|---|
| Low latency ($< 1$ ms) | Higher latency ($\sim 5$ ms) |
| High interrupt rate, more overhead | Lower interrupt rate |
| Small DMA buffer | Efficient cache use |
| Required for real-time control loops | Better for audio effects, filtering |

**3. Number representation:**
- `float32` on M4F: clean code, 1.3× overhead vs. Q15 for FIR
- `q15_t` with CMSIS-DSP: fastest for M4 due to `SMLAD` dual-MAC
- `q31_t`: higher precision, slower (no dual-MAC equivalent)

**4. Filter structure:**
- FIR: Preferred for linear phase (hearing aids, audio effects); CMSIS `arm_fir_q15` is well-optimised
- IIR biquad cascade: Preferred for efficiency (fewer taps for same roll-off); CMSIS `arm_biquad_cascade_df2T_f32`

**5. ADC/DAC interface:**
- I2S: Industry standard for audio — 2 data pins (bit clock, data), 1 frame sync; supported by SAI or I2S peripheral on STM32
- SPI: Alternative for simple 12/16-bit ADCs

**6. Memory layout:**

```c
// Allocate in DTCM for zero-wait-state access:
__attribute__((section(".dtcm_data")))
static q15_t dma_buffer[2 * BLOCK_SIZE];   // ping-pong
static q15_t filter_state[NUM_TAPS + BLOCK_SIZE - 1];
```

---

## Tier 3: Advanced

### Q8. How would you profile and optimise a Q15 IIR biquad cascade on Cortex-M4 to meet a 48 kHz real-time constraint?

**Answer:**

**Profiling methodology:**

```c
#define N_STAGES  8
arm_biquad_casd_df1_inst_q15 S;
q15_t biquad_state[N_STAGES * 4];
q15_t biquad_coeffs[N_STAGES * 5];  // b0, b1, b2, a1, a2 per stage

// Measure cycle count for BLOCK_SIZE = 64 samples
DWT->CYCCNT = 0;
arm_biquad_cascade_df1_q15(&S, input_q15, output_q15, BLOCK_SIZE);
uint32_t cycles = DWT->CYCCNT;
// Expected: ~3-5 cycles per sample per biquad stage
// For 8 stages, 64 samples: ~1536-2560 cycles at 168 MHz → ~10-15 µs
// Deadline: 64/48000 = 1333 µs → easily met
```

**Optimisation steps if deadline is not met:**

1. **Use Direct Form II Transposed (DF2T):** CMSIS `arm_biquad_cascade_df2T_f32` is faster than DF1 for float32 due to reduced state size. For Q15, DF1 is often preferred due to better overflow behaviour.

2. **Reduce number of stages:** Can 8 biquads be replaced by a lower-order design? An 8th-order elliptic filter can often replace a 16th-order Butterworth with the same transition band.

3. **Use Q31 only where needed:** If Q15 accuracy is insufficient (leads to noise floor issues), use Q31 only for critical stages (near-unity gain, high-Q poles) and Q15 elsewhere.

4. **Unroll the inner loop:** CMSIS-DSP already unrolls 4× for `arm_biquad_cascade_df1_q15`. If not using CMSIS, manually unroll.

5. **Enable compiler optimisations:**
   ```makefile
   -O3 -ffast-math -mfpu=fpv4-sp-d16 -mfloat-abi=hard
   ```

6. **Move coefficients to DTCM or register array**: For very tight latency, storing all $5 \times N_{stages}$ coefficients in processor registers is not feasible, but DTCM ensures no cache-miss variability.

---

### Q9. Explain the NEON/Helium SIMD instruction sets and their impact on DSP workloads.

**Answer:**

**ARM NEON (Cortex-A series, not Cortex-M):**

NEON is the Advanced SIMD extension for Cortex-A processors (application processors, Linux capable). It provides 32 × 128-bit vector registers and operations including:
- 16× 8-bit, 8× 16-bit, 4× 32-bit, 2× 64-bit parallel integer operations
- 4× 32-bit or 2× 64-bit parallel float operations

NEON is not present on Cortex-M devices (M-profile). It is relevant for DSP on embedded Linux boards (Raspberry Pi, NVIDIA Jetson) or smartphone baseband chips.

**ARM Helium / MVE (Cortex-M55, Cortex-M85):**

Helium is the M-Profile Vector Extension — NEON for Cortex-M. Available on M55 (since 2020) and M85.
- 8 × 128-bit vector registers (Q0–Q7)
- Up to 16× Q7, 8× Q15, 4× Q31 or 4× float32 per cycle
- Tail predication: handles non-multiple-of-vector-width arrays without branch overhead

**Impact on DSP workloads (Q15 FIR, N taps, M-block):**

| Core | MACs per cycle | FIR throughput (relative) |
|---|---|---|
| Cortex-M4 (DSP ext.) | 2 (via SMLAD) | 1× |
| Cortex-M7 (DSP ext.) | 2 | 1.5× (wider pipeline) |
| Cortex-M55 (Helium) | 8 (Q15 MVE) | ~6× |

**Example Helium intrinsics for Q15 FIR:**

```c
#include <arm_mve.h>

int16x8_t coeff_vec = vldrhq_s16(coeff_ptr);    // Load 8 coefficients
int16x8_t data_vec  = vldrhq_s16(data_ptr);     // Load 8 samples
acc = vmlaldavaq_s16(acc, coeff_vec, data_vec);  // 8-way MAC into 64-bit acc
```

One instruction processes 8 Q15 MACs — the same as 4 M4 `SMLAD` instructions. For a 64-tap FIR, the loop body executes 8 times instead of 32 times, reducing loop overhead proportionally.

---

## Common Interview Mistakes

1. **Assuming float is always better**: On a Cortex-M0 without FPU, float operations are software-emulated and 20–100× slower than Q15 integer DSP. Know which MCU you are targeting before recommending float.
2. **Forgetting DMA cache coherency**: On Cortex-M7 with D-cache enabled, DMA writes and CPU reads of the same buffer require explicit cache invalidation. Omitting `SCB_InvalidateDCache_by_Addr` is a very common real hardware bug.
3. **Ignoring WCET variability**: Cache misses, interrupt latency, and peripheral contention all cause execution time to vary. Always measure WCET under worst-case conditions, not average.
4. **Misquoting SIMD throughput**: SMLAD on M4 computes 2 Q15 MACs per cycle, not 4. CMSIS processes 4 MACs per loop iteration using 2 SMLADs, which requires 2 cycles minimum. Overclaiming "4 MACs/cycle" in an interview suggests shallow understanding.
5. **Not initialising filter state**: CMSIS-DSP init functions (`arm_fir_init_q15`, `arm_biquad_cascade_df1_init_q15`) zero-fill the state buffer. Failing to call init and then wondering why the filter output is garbage is a classic beginner error.
