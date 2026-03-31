"""
Challenge 01: FIR Filter Implementation from Scratch

Task:
    1. Implement an FIR filter using direct convolution (no scipy.signal.lfilter).
    2. Design lowpass FIR coefficients using the windowed sinc method.
    3. Apply the filter to a noisy test signal.
    4. Plot the input signal, filtered output, and frequency responses.

Learning objectives:
    - Understand direct-form FIR convolution
    - Understand windowed sinc design: cutoff, transition band, stopband
    - Understand the effect of window choice and filter length on frequency response
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List


# ---------------------------------------------------------------------------
# Part 1: Direct FIR convolution (no scipy.signal.lfilter)
# ---------------------------------------------------------------------------

def fir_filter(x: np.ndarray, h: np.ndarray) -> np.ndarray:
    """
    Apply an FIR filter with impulse response h to input signal x.

    Uses direct form convolution. Output has the same length as x
    (causal filter: zero-pad the state for the first len(h)-1 samples).

    Parameters
    ----------
    x : array_like
        Input signal, shape (N,).
    h : array_like
        Filter coefficients (impulse response), shape (M,).

    Returns
    -------
    y : ndarray
        Filtered output, shape (N,).

    Notes
    -----
    The operation computed is:
        y[n] = sum_{k=0}^{M-1} h[k] * x[n-k]
    where x[n] = 0 for n < 0 (zero-state assumption).
    """
    x = np.asarray(x, dtype=float)
    h = np.asarray(h, dtype=float)
    N = len(x)
    M = len(h)

    # Prepend M-1 zeros to handle the initial transient (zero-state response)
    x_padded = np.concatenate([np.zeros(M - 1), x])

    y = np.zeros(N)
    for n in range(N):
        # y[n] = h[0]*x[n] + h[1]*x[n-1] + ... + h[M-1]*x[n-(M-1)]
        # In the padded array, x[n] is at index n + M - 1
        y[n] = np.dot(h, x_padded[n: n + M][::-1])
        # Note: h[0] multiplies the most recent sample, so we reverse the window

    return y


def fir_filter_numpy(x: np.ndarray, h: np.ndarray) -> np.ndarray:
    """
    Equivalent vectorised implementation using np.convolve.

    Included for verification — should produce identical results to fir_filter().
    np.convolve computes the full convolution; we keep only the 'causal' part.
    """
    full = np.convolve(x, h)
    return full[:len(x)]


# ---------------------------------------------------------------------------
# Part 2: Windowed sinc FIR design
# ---------------------------------------------------------------------------

def design_lowpass_fir(
    cutoff_hz: float,
    fs_hz: float,
    num_taps: int,
    window: str = "hamming"
) -> np.ndarray:
    """
    Design a linear-phase lowpass FIR filter using the windowed sinc method.

    Parameters
    ----------
    cutoff_hz : float
        -6 dB cutoff frequency in Hz.
    fs_hz : float
        Sampling frequency in Hz.
    num_taps : int
        Number of filter taps. Must be odd for a Type-I linear phase filter.
    window : str
        Window function: 'rectangular', 'hanning', 'hamming', 'blackman', 'kaiser'.

    Returns
    -------
    h : ndarray
        Filter coefficients of length num_taps.

    Design method
    -------------
    The ideal lowpass impulse response (infinite-length sinc) is:
        h_ideal[n] = (2*fc/fs) * sinc(2*fc/fs * (n - (M-1)/2))
    where fc is the cutoff frequency and sinc(x) = sin(pi*x)/(pi*x).

    Multiplying by a window truncates the sinc and controls the stopband ripple
    and transition bandwidth trade-off.
    """
    if num_taps % 2 == 0:
        raise ValueError("num_taps should be odd for a Type-I symmetric FIR.")

    M = num_taps
    fc = cutoff_hz / fs_hz          # Normalised cutoff [0, 0.5]
    center = (M - 1) / 2.0          # Centre of the symmetric filter

    # --- Ideal sinc impulse response ---
    n = np.arange(M, dtype=float)
    # np.sinc(x) computes sin(pi*x)/(pi*x), so sinc(2*fc*(n-centre)) is correct
    h_ideal = 2.0 * fc * np.sinc(2.0 * fc * (n - center))

    # --- Apply window ---
    windows = {
        "rectangular": np.ones(M),
        "hanning":     np.hanning(M),
        "hamming":     np.hamming(M),
        "blackman":    np.blackman(M),
        "kaiser":      np.kaiser(M, beta=8.6),   # beta=8.6 ≈ Blackman-level stopband
    }
    if window not in windows:
        raise ValueError(f"Unknown window '{window}'. Choose from {list(windows)}")

    w = windows[window]
    h = h_ideal * w

    # --- Normalise so DC gain = 1 ---
    h = h / np.sum(h)

    return h


# ---------------------------------------------------------------------------
# Part 3: Frequency response utility
# ---------------------------------------------------------------------------

def compute_frequency_response(
    h: np.ndarray,
    fs_hz: float,
    n_fft: int = 4096
) -> tuple:
    """
    Compute the frequency response of an FIR filter using zero-padded FFT.

    Returns
    -------
    freqs : ndarray
        Frequency axis in Hz, shape (n_fft//2 + 1,).
    magnitude_db : ndarray
        Magnitude response in dB, shape (n_fft//2 + 1,).
    """
    H = np.fft.rfft(h, n=n_fft)
    magnitude_db = 20.0 * np.log10(np.abs(H) + 1e-12)
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / fs_hz)
    return freqs, magnitude_db


# ---------------------------------------------------------------------------
# Part 4: Generate test signal
# ---------------------------------------------------------------------------

def generate_test_signal(fs_hz: float = 8000.0, duration_s: float = 0.5) -> np.ndarray:
    """
    Generate a test signal: 500 Hz sine + 3000 Hz high-frequency noise.

    The 500 Hz component is the "signal of interest"; 3000 Hz is interference.
    A good lowpass filter at 1000 Hz cutoff should suppress the 3000 Hz component.
    """
    t = np.arange(0, duration_s, 1.0 / fs_hz)
    signal = np.sin(2.0 * np.pi * 500.0 * t)         # Desired signal: 500 Hz
    noise = 0.5 * np.sin(2.0 * np.pi * 3000.0 * t)  # Interference: 3000 Hz
    broadband = 0.1 * np.random.randn(len(t))         # Broadband Gaussian noise
    return t, signal + noise + broadband


# ---------------------------------------------------------------------------
# Main: demonstration and plotting
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    np.random.seed(42)

    # System parameters
    FS = 8000.0            # Sampling rate (Hz)
    CUTOFF = 1000.0        # Lowpass cutoff (Hz)
    NUM_TAPS = 101         # Odd for Type-I linear phase

    # --- Design filters with different windows for comparison ---
    windows_to_compare = ["rectangular", "hamming", "blackman"]
    colors = ["#e74c3c", "#2ecc71", "#3498db"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"FIR Lowpass Filter Design and Application\n"
        f"Cutoff = {CUTOFF} Hz, fs = {FS} Hz, {NUM_TAPS} taps",
        fontsize=13
    )

    ax_freq = axes[0, 0]
    ax_time = axes[0, 1]
    ax_spectrum = axes[1, 0]
    ax_detail = axes[1, 1]

    # --- Plot frequency responses for all windows ---
    ax_freq.set_title("Frequency Response — Window Comparison")
    ax_freq.set_xlabel("Frequency (Hz)")
    ax_freq.set_ylabel("Magnitude (dB)")
    ax_freq.set_ylim(-100, 5)
    ax_freq.axvline(CUTOFF, color="k", linestyle="--", alpha=0.5, label="Cutoff")
    ax_freq.axhline(-3, color="gray", linestyle=":", alpha=0.5, label="-3 dB")
    ax_freq.axhline(-60, color="gray", linestyle=":", alpha=0.4, label="-60 dB")

    coefficients = {}
    for win, color in zip(windows_to_compare, colors):
        h = design_lowpass_fir(CUTOFF, FS, NUM_TAPS, window=win)
        coefficients[win] = h
        freqs, mag_db = compute_frequency_response(h, FS)
        ax_freq.plot(freqs, mag_db, label=f"{win.capitalize()} window", color=color)

    ax_freq.legend(fontsize=9)
    ax_freq.grid(True, alpha=0.3)

    # --- Generate test signal and apply Hamming-windowed filter ---
    t, x = generate_test_signal(FS, duration_s=0.1)
    h_hamming = coefficients["hamming"]
    y = fir_filter(x, h_hamming)

    # Verify against numpy reference
    y_ref = fir_filter_numpy(x, h_hamming)
    max_error = np.max(np.abs(y - y_ref))
    print(f"Max error vs. np.convolve reference: {max_error:.2e}  (should be ~0)")

    # --- Time-domain plot (first 200 samples) ---
    ax_time.set_title("Time Domain: Input vs. Filtered Output")
    ax_time.set_xlabel("Sample index")
    ax_time.set_ylabel("Amplitude")
    n_show = 200
    ax_time.plot(x[:n_show], label="Noisy input", alpha=0.7, linewidth=0.8)
    ax_time.plot(y[:n_show], label="Filtered output (Hamming)", linewidth=1.5)
    ax_time.legend()
    ax_time.grid(True, alpha=0.3)

    # --- Spectrum comparison ---
    N = len(x)
    X_mag = 20.0 * np.log10(np.abs(np.fft.rfft(x, n=N)) / N + 1e-12)
    Y_mag = 20.0 * np.log10(np.abs(np.fft.rfft(y, n=N)) / N + 1e-12)
    freqs_sig = np.fft.rfftfreq(N, d=1.0 / FS)

    ax_spectrum.set_title("Spectrum: Input vs. Filtered Output")
    ax_spectrum.set_xlabel("Frequency (Hz)")
    ax_spectrum.set_ylabel("Magnitude (dB)")
    ax_spectrum.plot(freqs_sig, X_mag, label="Input", alpha=0.8, linewidth=0.8)
    ax_spectrum.plot(freqs_sig, Y_mag, label="Filtered", linewidth=1.2)
    ax_spectrum.axvline(CUTOFF, color="k", linestyle="--", alpha=0.5, label="Cutoff")
    ax_spectrum.legend()
    ax_spectrum.grid(True, alpha=0.3)

    # --- Filter coefficient impulse response ---
    ax_detail.set_title("Filter Impulse Response (Hamming, 101 taps)")
    ax_detail.set_xlabel("Tap index")
    ax_detail.set_ylabel("Coefficient value")
    ax_detail.stem(
        np.arange(NUM_TAPS), h_hamming,
        markerfmt="C0.", basefmt="k-", linefmt="C0-"
    )
    ax_detail.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fir_filter_results.png", dpi=150, bbox_inches="tight")
    plt.show()

    # --- Print design summary ---
    print("\n=== FIR Filter Design Summary ===")
    print(f"  Sample rate    : {FS} Hz")
    print(f"  Cutoff         : {CUTOFF} Hz  ({CUTOFF/FS:.3f} normalised)")
    print(f"  Number of taps : {NUM_TAPS}")
    print(f"  Filter delay   : {(NUM_TAPS-1)//2} samples  ({(NUM_TAPS-1)/(2*FS)*1000:.2f} ms)")

    for win in windows_to_compare:
        h = coefficients[win]
        freqs, mag_db = compute_frequency_response(h, FS)
        # Find -3 dB point
        idx_3db = np.argmin(np.abs(mag_db + 3.0))
        # Find stopband attenuation at 3× cutoff
        idx_stop = np.argmin(np.abs(freqs - 3.0 * CUTOFF))
        print(
            f"  {win.capitalize():12s}: "
            f"-3 dB @ {freqs[idx_3db]:.0f} Hz, "
            f"att @ {3*CUTOFF:.0f} Hz = {mag_db[idx_stop]:.1f} dB"
        )

    # --- Window comparison summary ---
    print("\nWindow properties (approximate):")
    print("  Rectangular : narrowest transition band, highest sidelobes (-13 dB)")
    print("  Hamming     : -41 dB stopband, moderate transition width")
    print("  Blackman    : -74 dB stopband, wider transition width")
    print("  Kaiser(8.6) : -80 dB stopband, adjustable via beta parameter")
