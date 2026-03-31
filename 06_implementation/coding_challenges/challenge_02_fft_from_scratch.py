"""
Challenge 02: Radix-2 DIT FFT from Scratch

Task:
    Implement the Cooley-Tukey radix-2 Decimation-In-Time (DIT) FFT algorithm
    from scratch, without using numpy.fft. Then verify against numpy.fft.fft
    and benchmark performance against it.

Learning objectives:
    - Understand the divide-and-conquer structure of the FFT
    - Implement bit-reversal permutation
    - Implement butterfly operations with twiddle factors
    - Understand the O(N log N) vs O(N^2) complexity difference
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import cmath
import math


# ---------------------------------------------------------------------------
# Part 1: Naive DFT (O(N^2)) — reference and comparison baseline
# ---------------------------------------------------------------------------

def dft_naive(x: np.ndarray) -> np.ndarray:
    """
    Compute the DFT of x using the direct O(N^2) summation.

    X[k] = sum_{n=0}^{N-1} x[n] * exp(-j * 2*pi * k * n / N)

    Used to verify the FFT implementation for small N.
    """
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * cmath.exp(-2j * math.pi * k * n / N)
    return X


# ---------------------------------------------------------------------------
# Part 2: Bit-reversal permutation
# ---------------------------------------------------------------------------

def bit_reverse_copy(x: np.ndarray) -> np.ndarray:
    """
    Return a copy of x with elements permuted in bit-reversed order.

    For N = 8 (3 bits): indices 0,1,2,3,4,5,6,7 become 0,4,2,6,1,5,3,7
    (reverse the binary representation of each index).

    This is the initial permutation for the DIT FFT — it puts the input
    in the order needed so that the butterfly stages can proceed in-place.
    """
    N = len(x)
    bits = int(math.log2(N))  # Number of bits needed to address N elements
    out = np.zeros(N, dtype=complex)
    for i in range(N):
        rev = _bit_reverse(i, bits)
        out[rev] = x[i]
    return out


def _bit_reverse(n: int, num_bits: int) -> int:
    """Reverse the binary representation of n using num_bits bits."""
    result = 0
    for _ in range(num_bits):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def bit_reverse_copy_fast(x: np.ndarray) -> np.ndarray:
    """
    Faster bit-reversal using numpy integer operations.
    Equivalent to bit_reverse_copy() but vectorised.
    """
    N = len(x)
    bits = int(math.log2(N))
    indices = np.arange(N, dtype=np.int32)

    # Reverse all bits for all indices simultaneously
    rev_indices = np.zeros(N, dtype=np.int32)
    tmp = indices.copy()
    for _ in range(bits):
        rev_indices = (rev_indices << 1) | (tmp & 1)
        tmp >>= 1

    out = np.zeros(N, dtype=complex)
    out[rev_indices] = x
    return out


# ---------------------------------------------------------------------------
# Part 3: Radix-2 DIT FFT
# ---------------------------------------------------------------------------

def fft_radix2(x: np.ndarray) -> np.ndarray:
    """
    Compute the FFT of x using the Cooley-Tukey radix-2 DIT algorithm.

    Requirements:
        len(x) must be a power of 2.

    Algorithm:
        1. Bit-reverse permute the input array.
        2. Perform log2(N) stages of butterfly operations.
        3. In stage s, each butterfly of size 2^s combines two sub-FFTs
           of size 2^(s-1) using twiddle factors W_N^k = exp(-j*2*pi*k/N_s).

    Complexity: O(N log2 N) vs O(N^2) for naive DFT.

    Parameters
    ----------
    x : array_like
        Input sequence. Length must be a power of 2.

    Returns
    -------
    X : ndarray, complex
        DFT of x, same length.
    """
    N = len(x)

    # Validate power-of-2 length
    if N == 0 or (N & (N - 1)) != 0:
        raise ValueError(f"FFT length must be a power of 2, got {N}")

    # Step 1: Bit-reversal permutation
    X = bit_reverse_copy_fast(x).astype(complex)

    # Step 2: Butterfly stages
    # Stage s processes butterfly groups of size 2^s
    # There are log2(N) stages total
    num_stages = int(math.log2(N))

    for s in range(1, num_stages + 1):
        butterfly_size = 2 ** s          # Size of each butterfly group: 2, 4, 8, ..., N
        half_size = butterfly_size // 2  # Size of each half-group (sub-FFT)

        # Twiddle factor for this stage: W = exp(-j*2*pi/butterfly_size)
        # The k-th twiddle in this stage is W^k = exp(-j*2*pi*k/butterfly_size)
        W_N = cmath.exp(-2j * math.pi / butterfly_size)  # Base twiddle factor

        # Process all butterfly groups in this stage
        # There are N // butterfly_size groups, starting at 0, butterfly_size, 2*butterfly_size, ...
        for group_start in range(0, N, butterfly_size):
            W_k = 1.0 + 0j   # Current twiddle: W_N^k, starts at W_N^0 = 1

            # Each butterfly within the group
            for k in range(half_size):
                # Butterfly inputs: even index u, odd index v
                u = X[group_start + k]
                v = X[group_start + k + half_size] * W_k

                # Butterfly outputs (Cooley-Tukey butterfly):
                X[group_start + k]              = u + v
                X[group_start + k + half_size]  = u - v

                W_k *= W_N  # Advance twiddle factor: W_N^(k+1) = W_N^k * W_N

    return X


def fft_radix2_recursive(x: list) -> np.ndarray:
    """
    Recursive implementation of the radix-2 DIT FFT.

    Pedagogically clearer than the iterative version:
    FFT(x) = FFT(x_even) combined with FFT(x_odd) via butterfly.

    Less efficient than the iterative version (Python recursion overhead),
    but easier to understand and verify.
    """
    N = len(x)

    # Base case
    if N == 1:
        return np.array([complex(x[0])])

    if (N & (N - 1)) != 0:
        raise ValueError("Length must be a power of 2")

    # Divide: split into even-indexed and odd-indexed sub-sequences
    x_even = x[0::2]   # x[0], x[2], x[4], ...
    x_odd  = x[1::2]   # x[1], x[3], x[5], ...

    # Conquer: recursively compute FFTs of the two halves
    X_even = fft_radix2_recursive(x_even)
    X_odd  = fft_radix2_recursive(x_odd)

    # Combine: butterfly with twiddle factors
    X = np.zeros(N, dtype=complex)
    for k in range(N // 2):
        twiddle = cmath.exp(-2j * math.pi * k / N) * X_odd[k]
        X[k]           = X_even[k] + twiddle   # Upper half
        X[k + N // 2]  = X_even[k] - twiddle   # Lower half (by symmetry)

    return X


# ---------------------------------------------------------------------------
# Part 4: Inverse FFT
# ---------------------------------------------------------------------------

def ifft_radix2(X: np.ndarray) -> np.ndarray:
    """
    Compute the IFFT using the FFT: conjugate, FFT, conjugate, scale.

    The IDFT can be expressed as:
        x[n] = (1/N) * conj(FFT(conj(X[k])))

    This avoids writing a separate IFFT implementation.
    """
    N = len(X)
    # Conjugate input, apply FFT, conjugate output, scale by 1/N
    return np.conj(fft_radix2(np.conj(X))) / N


# ---------------------------------------------------------------------------
# Part 5: Benchmarking and verification
# ---------------------------------------------------------------------------

def benchmark(N: int, n_trials: int = 20) -> dict:
    """
    Benchmark our FFT against numpy.fft.fft for a given size N.

    Returns timing results for:
    - DFT naive (only for small N ≤ 512)
    - Our iterative radix-2 FFT
    - numpy.fft.fft
    """
    np.random.seed(0)
    x = np.random.randn(N) + 1j * np.random.randn(N)

    results = {}

    # Our implementation
    times = []
    for _ in range(n_trials):
        t0 = time.perf_counter()
        _ = fft_radix2(x)
        times.append(time.perf_counter() - t0)
    results["ours_us"] = np.median(times) * 1e6

    # numpy FFT
    times = []
    for _ in range(n_trials):
        t0 = time.perf_counter()
        _ = np.fft.fft(x)
        times.append(time.perf_counter() - t0)
    results["numpy_us"] = np.median(times) * 1e6

    # Accuracy
    X_ours = fft_radix2(x)
    X_numpy = np.fft.fft(x)
    results["max_abs_error"] = float(np.max(np.abs(X_ours - X_numpy)))
    results["rel_error"] = float(
        np.max(np.abs(X_ours - X_numpy)) / (np.max(np.abs(X_numpy)) + 1e-30)
    )

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # -----------------------------------------------------------------------
    # 1. Verify correctness against numpy.fft.fft and naive DFT
    # -----------------------------------------------------------------------
    print("=== Correctness Verification ===\n")

    for N in [8, 16, 64, 256]:
        np.random.seed(1)
        x = np.random.randn(N) + 1j * np.random.randn(N)

        X_naive = dft_naive(x) if N <= 64 else None
        X_iter  = fft_radix2(x)
        X_rec   = fft_radix2_recursive(list(x))
        X_numpy = np.fft.fft(x)

        err_iter  = np.max(np.abs(X_iter  - X_numpy))
        err_rec   = np.max(np.abs(X_rec   - X_numpy))

        print(f"N={N:4d}:  "
              f"iterative vs numpy = {err_iter:.2e}  |  "
              f"recursive vs numpy = {err_rec:.2e}", end="")

        if X_naive is not None:
            err_naive = np.max(np.abs(X_naive - X_numpy))
            print(f"  |  naive vs numpy = {err_naive:.2e}", end="")
        print()

    # -----------------------------------------------------------------------
    # 2. IFFT round-trip test
    # -----------------------------------------------------------------------
    print("\n=== IFFT Round-Trip Test ===\n")
    N = 128
    x_orig = np.random.randn(N) + 1j * np.random.randn(N)
    X = fft_radix2(x_orig)
    x_recovered = ifft_radix2(X)
    roundtrip_error = np.max(np.abs(x_recovered - x_orig))
    print(f"Round-trip IFFT(FFT(x)) error: {roundtrip_error:.2e}  (should be ~machine epsilon)")

    # -----------------------------------------------------------------------
    # 3. Benchmark for various sizes
    # -----------------------------------------------------------------------
    print("\n=== Performance Benchmark ===\n")
    print(f"{'N':>6}  {'Our FFT (µs)':>14}  {'numpy FFT (µs)':>15}  "
          f"{'Speedup':>9}  {'Max abs err':>12}")
    print("-" * 65)

    for N in [64, 256, 1024, 4096, 16384]:
        r = benchmark(N, n_trials=50)
        speedup = r["ours_us"] / r["numpy_us"]
        print(f"{N:>6}  {r['ours_us']:>14.1f}  {r['numpy_us']:>15.3f}  "
              f"{speedup:>9.1f}x  {r['max_abs_error']:>12.2e}")

    # -----------------------------------------------------------------------
    # 4. Complexity illustration: O(N log N) vs O(N^2)
    # -----------------------------------------------------------------------
    print("\n=== Complexity Comparison: O(N log N) vs O(N^2) ===\n")
    print("For N = 1024:")
    N = 1024
    ops_naive = N * N
    ops_fft   = N * int(math.log2(N))
    print(f"  DFT (naive)  : {ops_naive:>10} multiplications")
    print(f"  FFT (radix2) : {ops_fft:>10} multiplications")
    print(f"  Speedup      : {ops_naive/ops_fft:.0f}x fewer operations")

    print("\nFor N = 1,048,576 (2^20):")
    N = 2 ** 20
    ops_fft = N * 20
    ops_naive = N * N  # Too large — just illustrative
    print(f"  DFT (naive)  : ~{N*N:.2e} multiplications (impractical)")
    print(f"  FFT (radix2) : {ops_fft:>15,} multiplications")

    # -----------------------------------------------------------------------
    # 5. Visualise: spectrum of a test signal
    # -----------------------------------------------------------------------
    print("\n=== Spectrum Analysis Test ===\n")
    fs = 1000.0  # Hz
    N = 1024
    t = np.arange(N) / fs
    # Composite signal: 100 Hz + 250 Hz + 400 Hz sinusoids
    x_real = (np.sin(2 * np.pi * 100 * t) +
              0.5 * np.sin(2 * np.pi * 250 * t) +
              0.25 * np.sin(2 * np.pi * 400 * t))

    X_fft   = fft_radix2(x_real)
    X_numpy = np.fft.fft(x_real)
    freqs   = np.fft.fftfreq(N, d=1.0 / fs)

    # Check that peaks are at expected frequencies
    mag = np.abs(X_fft[:N // 2])  # One-sided spectrum
    f_pos = freqs[:N // 2]
    peak_indices = np.argsort(mag)[-3:]  # Top 3 peaks
    peak_freqs = sorted(f_pos[peak_indices])
    print(f"  Signal components: 100, 250, 400 Hz")
    print(f"  Detected peaks   : {[f'{f:.1f}' for f in peak_freqs]} Hz")

    # Plot spectrum
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(f_pos, 2 * mag / N, linewidth=1)
    ax1.set_title("One-sided spectrum (our FFT)")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    ax2.stem(f_pos, 2 * mag / N, markerfmt=".", linefmt="C0-", basefmt="k-")
    ax2.set_title("Stem plot — 100, 250, 400 Hz peaks")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Amplitude")
    ax2.set_xlim(0, 500)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fft_spectrum.png", dpi=150, bbox_inches="tight")
    plt.show()
