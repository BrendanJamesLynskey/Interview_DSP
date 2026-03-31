"""
Challenge 03: Fixed-Point FIR Filter Simulator

Task:
    Implement a Q15 fixed-point FIR filter simulator in Python.
    Model the key fixed-point effects:
      - Q15 coefficient quantisation
      - Q15 input quantisation
      - Product rounding (Q30 → Q15)
      - Saturation vs. wrapping overflow
    Compare the output to a floating-point reference and compute the SNR.

Learning objectives:
    - Understand Q15 arithmetic limits and conventions
    - Model overflow and rounding as distinct noise sources
    - Quantify SNR degradation from fixed-point effects
    - Visualise the difference between float and fixed-point filter outputs
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


# ---------------------------------------------------------------------------
# Q15 fixed-point constants
# ---------------------------------------------------------------------------

Q15_MAX    =  32767   # 2^15 - 1
Q15_MIN    = -32768   # -2^15
Q15_SCALE  =  32768   # 2^15 (scaling factor: real value = int_value / Q15_SCALE)
Q30_SCALE  =  Q15_SCALE ** 2  # 2^30


# ---------------------------------------------------------------------------
# Q15 quantisation utilities
# ---------------------------------------------------------------------------

def float_to_q15(x: np.ndarray) -> np.ndarray:
    """
    Convert a float array to Q15 integer representation.

    Input range must be [-1.0, 1.0). Values outside this range are saturated.

    Q15 representation: integer in [-32768, 32767]
    Value = integer / 32768

    Rounding: convergent (round-half-to-even) to avoid DC bias.
    """
    # Scale to integer range
    scaled = x * Q15_SCALE

    # Convergent rounding (round half to even)
    rounded = np.round(scaled).astype(np.int64)

    # Saturate to Q15 range
    saturated = np.clip(rounded, Q15_MIN, Q15_MAX)

    return saturated.astype(np.int32)


def q15_to_float(x_int: np.ndarray) -> np.ndarray:
    """Convert Q15 integer array back to floating-point."""
    return x_int.astype(float) / Q15_SCALE


def quantise_to_q15(x: np.ndarray) -> np.ndarray:
    """Quantise a float signal to Q15 then back to float (models ADC quantisation)."""
    return q15_to_float(float_to_q15(x))


# ---------------------------------------------------------------------------
# Fixed-point multiply: Q15 × Q15 → Q15
# ---------------------------------------------------------------------------

def q15_multiply(a: int, b: int) -> int:
    """
    Multiply two Q15 integers and return a Q15 result.

    Steps:
        1. Multiply: product is a 32-bit Q30 value
        2. Shift right 15 bits (Q30 → Q15) with rounding
        3. Saturate to Q15 range

    Special case: (-32768) × (-32768) = 2^30 which exceeds Q30 range.
    This is the one unavoidable overflow in Q15 arithmetic; we saturate it.
    """
    # Full precision multiply → Q30 in 32 bits
    product = int(a) * int(b)   # Python int handles arbitrary precision

    # Add rounding constant (0x4000 = 2^14) before right shift
    # This implements "round half up" for positive numbers
    product_rounded = product + (1 << 14)

    # Right shift 15 to get Q15 from Q30
    result = product_rounded >> 15

    # Saturate to Q15 range
    return int(np.clip(result, Q15_MIN, Q15_MAX))


def q15_add_saturate(a: int, b: int) -> int:
    """Saturating addition of two Q15 integers."""
    s = int(a) + int(b)
    return int(np.clip(s, Q15_MIN, Q15_MAX))


def q15_add_wrap(a: int, b: int) -> int:
    """Two's complement wrapping addition of two Q15 integers."""
    s = (int(a) + int(b)) & 0xFFFF  # Keep 16 bits
    # Sign-extend from 16 bits
    if s >= 0x8000:
        s -= 0x10000
    return int(s)


# ---------------------------------------------------------------------------
# Fixed-point FIR filter (accumulator-based, scalar)
# ---------------------------------------------------------------------------

def fir_fixed_point(
    x_float: np.ndarray,
    h_float: np.ndarray,
    overflow_mode: str = "saturate"
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply an FIR filter in Q15 fixed-point arithmetic.

    This models the signal processing chain:
        1. Quantise input x to Q15
        2. Quantise coefficients h to Q15
        3. For each output sample:
           a. Compute products h[k] * x[n-k] as Q15 (rounded)
           b. Accumulate Q15 products with overflow handling
        4. Convert output back to float

    Parameters
    ----------
    x_float : ndarray
        Float input signal in [-1.0, 1.0).
    h_float : ndarray
        Float filter coefficients (will be quantised to Q15 internally).
    overflow_mode : str
        'saturate' or 'wrap' for accumulator overflow handling.

    Returns
    -------
    y_fixed_float : ndarray
        Fixed-point output converted back to float.
    y_float_ref : ndarray
        Floating-point reference output (no quantisation effects).
    """
    N = len(x_float)
    M = len(h_float)

    # Quantise inputs and coefficients to Q15
    x_q15 = float_to_q15(x_float)
    h_q15 = float_to_q15(h_float)

    # Floating-point reference (for SNR comparison)
    y_float_ref = np.convolve(x_float, h_float)[:N]

    # Fixed-point processing
    add_fn = q15_add_saturate if overflow_mode == "saturate" else q15_add_wrap

    y_q15 = np.zeros(N, dtype=np.int32)

    for n in range(N):
        acc = 0  # Accumulator starts at zero each output sample
        for k in range(M):
            if n - k < 0:
                continue   # Zero-pad: x[n-k] = 0 for n < k
            product = q15_multiply(h_q15[k], x_q15[n - k])
            acc = add_fn(acc, product)
        y_q15[n] = acc

    y_fixed_float = q15_to_float(y_q15)
    return y_fixed_float, y_float_ref


def fir_fixed_point_vectorised(
    x_float: np.ndarray,
    h_float: np.ndarray,
    overflow_mode: str = "saturate"
) -> np.ndarray:
    """
    Vectorised (faster) version using numpy operations to model Q15 FIR.

    Models:
    - Coefficient quantisation to Q15
    - Input quantisation to Q15
    - Product rounding from Q30 to Q15
    - Accumulator saturation or wrapping

    Significantly faster than the scalar version for large signals.
    """
    N = len(x_float)
    M = len(h_float)

    # Quantise
    x_q15 = float_to_q15(x_float).astype(np.int32)
    h_q15 = float_to_q15(h_float).astype(np.int32)

    # Pad input for causal filter
    x_padded = np.concatenate([np.zeros(M - 1, dtype=np.int32), x_q15])

    y_q15 = np.zeros(N, dtype=np.int64)

    # Vectorised accumulation: for each tap k, compute products and accumulate
    for k in range(M):
        segment = x_padded[M - 1 - k: N + M - 1 - k].astype(np.int64)
        h_val = int(h_q15[k])
        products = segment * h_val  # Q30 in int64

        # Round Q30 → Q15: add 2^14, right-shift 15
        products_rounded = (products + (1 << 14)) >> 15

        # Saturate each product to Q15 before accumulation
        products_sat = np.clip(products_rounded, Q15_MIN, Q15_MAX)

        y_q15 += products_sat

    # Apply overflow to accumulated sum
    if overflow_mode == "saturate":
        y_q15 = np.clip(y_q15, Q15_MIN, Q15_MAX)
    else:  # wrap
        y_q15 = y_q15.astype(np.int16).astype(np.int64)  # Force 16-bit wrap

    return q15_to_float(y_q15.astype(np.int16))


# ---------------------------------------------------------------------------
# SNR computation
# ---------------------------------------------------------------------------

def compute_snr(reference: np.ndarray, distorted: np.ndarray) -> float:
    """
    Compute SNR in dB between a reference signal and a distorted version.

    SNR = 10 * log10(power(reference) / power(error))
    """
    error = distorted - reference
    sig_power = np.mean(reference ** 2)
    err_power = np.mean(error ** 2)
    if err_power < 1e-30:
        return np.inf
    return 10.0 * np.log10(sig_power / err_power)


# ---------------------------------------------------------------------------
# Design a simple FIR filter for testing
# ---------------------------------------------------------------------------

def design_test_filter(num_taps: int = 31, cutoff: float = 0.2) -> np.ndarray:
    """Design a Hamming-windowed sinc lowpass filter."""
    M = num_taps
    center = (M - 1) / 2.0
    n = np.arange(M, dtype=float)
    h = 2.0 * cutoff * np.sinc(2.0 * cutoff * (n - center)) * np.hamming(M)
    h = h / np.sum(h)  # Normalise to unity DC gain
    return h


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Fixed-Point Q15 FIR Filter Simulator ===\n")

    # -----------------------------------------------------------------------
    # 1. Q15 quantisation noise model verification
    # -----------------------------------------------------------------------
    print("--- Q15 Quantisation Noise ---")
    x_full_scale = np.random.uniform(-1.0, 1.0, 100000)
    x_quantised = quantise_to_q15(x_full_scale)
    noise = x_quantised - x_full_scale
    sqnr_measured = compute_snr(x_full_scale, x_quantised)
    sqnr_theory = 6.02 * 15 - 1.76  # 6.02*W - 1.76 dB for W=15 (Q15 = 15 fractional bits)
    print(f"  Measured SQNR (broadband input) : {sqnr_measured:.2f} dB")
    print(f"  Theoretical SQNR (6.02*15-1.76): {sqnr_theory:.2f} dB")
    print(f"  Quantisation noise std dev      : {np.std(noise):.6f}")
    print(f"  Expected std dev (Delta/sqrt(12)): {(1/Q15_SCALE)/np.sqrt(12):.6f}\n")

    # -----------------------------------------------------------------------
    # 2. Coefficient quantisation effect on frequency response
    # -----------------------------------------------------------------------
    print("--- Coefficient Quantisation ---")
    NUM_TAPS = 31
    h_float = design_test_filter(NUM_TAPS, cutoff=0.2)
    h_q15_int = float_to_q15(h_float)
    h_q15_float = q15_to_float(h_q15_int)

    coeff_error = h_float - h_q15_float
    print(f"  Max coefficient quantisation error: {np.max(np.abs(coeff_error)):.6f}")
    print(f"  Q15 step size (Delta):              {1/Q15_SCALE:.6f}")
    print(f"  Largest coefficient:                {np.max(np.abs(h_float)):.6f}")

    # Compare frequency responses
    n_fft = 2048
    H_float = np.fft.rfft(h_float, n=n_fft)
    H_q15   = np.fft.rfft(h_q15_float, n=n_fft)
    freq_resp_error_db = 20.0 * np.log10(np.abs(H_float - H_q15) + 1e-12)
    print(f"  Max frequency response error:       {np.max(np.abs(H_float - H_q15)):.6f}\n")

    # -----------------------------------------------------------------------
    # 3. Filter a test signal in Q15 vs float, compare SNR
    # -----------------------------------------------------------------------
    print("--- Filter Output SNR Comparison ---")
    N = 2000
    # Composite input: 100 Hz signal + 400 Hz interference (fs=1000 Hz, normalised)
    t = np.arange(N)
    fs_norm = 1.0  # normalised to [0, 0.5]
    x_signal = 0.7 * np.sin(2 * np.pi * 0.08 * t)   # 0.08 normalised (in passband)
    x_noise  = 0.3 * np.sin(2 * np.pi * 0.35 * t)   # 0.35 normalised (in stopband)
    x_full   = x_signal + x_noise

    # Clip to Q15 range (should be fine since |x| ≤ 1.0)
    x_input = np.clip(x_full, -0.999, 0.999)

    # Floating-point reference
    y_float = np.convolve(x_input, h_float)[:N]

    # Fixed-point with saturation
    y_fixed_sat = fir_fixed_point_vectorised(x_input, h_float, overflow_mode="saturate")

    # Fixed-point with wrap-around
    y_fixed_wrap = fir_fixed_point_vectorised(x_input, h_float, overflow_mode="wrap")

    # Trim transient (first M-1 samples)
    skip = NUM_TAPS - 1
    y_f  = y_float[skip:]
    y_fs = y_fixed_sat[skip:]
    y_fw = y_fixed_wrap[skip:]

    snr_sat  = compute_snr(y_f, y_fs)
    snr_wrap = compute_snr(y_f, y_fw)

    print(f"  SNR (float vs Q15 saturate) : {snr_sat:.2f} dB")
    print(f"  SNR (float vs Q15 wrap)     : {snr_wrap:.2f} dB")
    print(f"  Theoretical SNR upper bound : ~{6.02*15 - 1.76:.2f} dB  (Q15 quantisation limit)\n")

    # -----------------------------------------------------------------------
    # 4. Overflow demonstration
    # -----------------------------------------------------------------------
    print("--- Overflow Behaviour ---")
    # Create a signal that WILL overflow: amplitude > 1.0 after filter
    x_overflow = 0.9 * np.ones(N)   # DC at 0.9; filter DC gain = 1 → output = 0.9 (OK)
    # Now use a filter with gain > 1 at DC (boost the gain)
    h_gain2 = design_test_filter(NUM_TAPS, cutoff=0.2) * 2.0  # Gain = 2 → output up to 1.8 → overflow
    h_gain2_clipped = np.clip(h_gain2, -1.0, 1.0)  # Can't represent gain>1 in Q15 coefficients

    # Use raw high-amplitude input instead to force overflow
    x_hi = np.clip(0.8 * np.ones(N), -0.999, 0.999)
    y_sat_hi  = fir_fixed_point_vectorised(x_hi, h_float * 2.0 if np.max(np.abs(h_float * 2.0)) <= 1.0
                                            else h_float, overflow_mode="saturate")
    y_wrap_hi = fir_fixed_point_vectorised(x_hi, h_float, overflow_mode="wrap")

    print(f"  Input amplitude:          {np.max(np.abs(x_hi)):.3f}")
    print(f"  Saturated output range:   [{np.min(y_sat_hi):.4f}, {np.max(y_sat_hi):.4f}]")
    print(f"  Wrapped output range:     [{np.min(y_wrap_hi):.4f}, {np.max(y_wrap_hi):.4f}]")
    print()

    # -----------------------------------------------------------------------
    # 5. Plot results
    # -----------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Q15 Fixed-Point FIR Filter Simulation", fontsize=13)

    # Frequency response comparison
    ax = axes[0, 0]
    freqs = np.fft.rfftfreq(n_fft)
    ax.plot(freqs, 20*np.log10(np.abs(H_float) + 1e-12), label="Float64")
    ax.plot(freqs, 20*np.log10(np.abs(H_q15)   + 1e-12), "--", label="Q15 coefficients")
    ax.set_title("Frequency Response: Float vs Q15 Coefficients")
    ax.set_xlabel("Normalised Frequency")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_ylim(-80, 5)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Time-domain output comparison
    ax = axes[0, 1]
    n_show = 200
    ax.plot(y_f[:n_show],  label="Float reference", linewidth=1.5)
    ax.plot(y_fs[:n_show], "--", label="Q15 saturate", linewidth=1.2)
    ax.set_title("Filter Output: Float vs Q15")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Error signal
    ax = axes[1, 0]
    err = y_fs - y_f
    ax.plot(err[:300], linewidth=0.8, color="red")
    ax.set_title(f"Error Signal (Float − Q15 Saturate), SNR = {snr_sat:.1f} dB")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Error")
    ax.grid(True, alpha=0.3)

    # Coefficient comparison
    ax = axes[1, 1]
    n_taps = np.arange(NUM_TAPS)
    ax.stem(n_taps, h_float,    markerfmt="C0.", basefmt="k-",
            linefmt="C0-", label="Float64")
    ax.stem(n_taps, h_q15_float, markerfmt="C1x", basefmt="k-",
            linefmt="C1--", label="Q15")
    ax.set_title("Coefficient Comparison: Float vs Q15")
    ax.set_xlabel("Tap index")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fixed_point_filter_results.png", dpi=150, bbox_inches="tight")
    plt.show()

    # -----------------------------------------------------------------------
    # 6. SNR vs word length sweep
    # -----------------------------------------------------------------------
    print("--- SNR vs Word Length (theoretical vs measured) ---")
    print(f"  {'W':>4}  {'SQNR theory (dB)':>18}  {'SQNR measured (dB)':>20}")
    print(f"  {'-'*50}")
    for W in [8, 10, 12, 14, 15, 16]:
        scale = 2 ** (W - 1)
        quantised = np.round(x_input * scale) / scale
        quantised = np.clip(quantised, -1.0, 1.0)
        snr_meas = compute_snr(x_input, quantised)
        snr_theo = 6.02 * W - 1.76
        print(f"  {W:>4}  {snr_theo:>18.2f}  {snr_meas:>20.2f}")
