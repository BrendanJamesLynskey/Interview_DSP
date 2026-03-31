"""
Challenge 04: LMS Adaptive Filter
==================================
Demonstrates the Least Mean Squares (LMS) adaptive filter in two canonical
applications:

  1. System Identification  -- learn the coefficients of an unknown FIR system.
  2. Noise Cancellation     -- remove correlated noise from a signal of interest.

For each application the script:
  - Runs the LMS algorithm over multiple step sizes mu.
  - Plots learning curves (MSE in dB vs. iteration, averaged over Monte Carlo
    runs to reduce variance).
  - Plots coefficient convergence for the best step size.

Dependencies: numpy, matplotlib  (no scipy or other libraries)

Usage:
  python challenge_04_lms_adaptive.py

Expected results:
  - System ID: coefficients converge to the true FIR taps within ~500 iterations
    for mu = 0.01.
  - Noise cancellation: output SNR improves by ~20 dB relative to the noisy
    input.
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Core LMS algorithm
# ---------------------------------------------------------------------------

def lms_filter(x: np.ndarray,
               d: np.ndarray,
               n_taps: int,
               mu: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Run one pass of the LMS adaptive filter.

    Parameters
    ----------
    x      : Input signal, shape (N,).
    d      : Desired signal, shape (N,).
    n_taps : Filter length (number of coefficients).
    mu     : Step size (learning rate).

    Returns
    -------
    y      : Filter output, shape (N,).
    e      : Error signal e(n) = d(n) - y(n), shape (N,).
    w_hist : Weight history, shape (N, n_taps).  w_hist[n] is the weight
             vector AFTER the update at time n.

    Algorithm
    ---------
    Initialise: w(0) = 0

    At each time step n:
        x_vec = [x(n), x(n-1), ..., x(n-L+1)]   (input buffer)
        y(n)  = w(n)^T * x_vec                   (filter output)
        e(n)  = d(n) - y(n)                      (error)
        w(n+1) = w(n) + 2*mu*e(n)*x_vec          (weight update)

    The factor of 2 is often absorbed into mu; here we keep the standard
    textbook form where J(w) = E[e^2] and gradient = -2*e*x.
    """
    N      = len(x)
    w      = np.zeros(n_taps)          # weight vector
    y      = np.zeros(N)
    e      = np.zeros(N)
    w_hist = np.zeros((N, n_taps))

    for n in range(N):
        # Build the input buffer (zero-pad for n < n_taps-1)
        if n >= n_taps:
            x_vec = x[n - n_taps + 1 : n + 1][::-1]   # most-recent first
        else:
            x_vec = np.zeros(n_taps)
            x_vec[:n + 1] = x[: n + 1][::-1]

        y[n]  = w @ x_vec
        e[n]  = d[n] - y[n]
        w     = w + 2.0 * mu * e[n] * x_vec            # gradient descent step
        w_hist[n] = w

    return y, e, w_hist


# ---------------------------------------------------------------------------
# Application 1: System Identification
# ---------------------------------------------------------------------------

def run_system_identification(n_samples: int = 2000,
                               n_taps: int = 8,
                               mu_list: list[float] = None,
                               n_mc: int = 50,
                               rng_seed: int = 0) -> None:
    """
    Unknown plant: a random-phase FIR filter with `n_taps` coefficients.
    White Gaussian noise drives both the plant and the adaptive filter.
    The desired signal is the plant output (plus a small observation noise floor).

    Goal: the adaptive filter's weights converge to the true plant coefficients.

    The MSE learning curve is averaged over `n_mc` Monte Carlo trials to
    produce a smooth ensemble-averaged curve.

    Parameters
    ----------
    n_samples : Number of samples per trial.
    n_taps    : Length of the unknown plant and the adaptive filter.
    mu_list   : List of step sizes to compare.
    n_mc      : Number of Monte Carlo runs.
    rng_seed  : Base seed for reproducibility.
    """
    if mu_list is None:
        mu_list = [0.001, 0.005, 0.01, 0.05]

    # True plant coefficients (fixed across all MC runs so the target is stable)
    rng_fixed = np.random.default_rng(42)
    h_true = rng_fixed.standard_normal(n_taps)
    h_true /= np.linalg.norm(h_true)          # unit-norm for comparability

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("LMS System Identification", fontsize=13, fontweight="bold")

    ax_mse, ax_coef = axes

    best_mu = mu_list[len(mu_list) // 2]      # pick middle mu for coeff plot
    w_hist_best = None

    for mu in mu_list:
        mse_accumulator = np.zeros(n_samples)

        for trial in range(n_mc):
            rng = np.random.default_rng(rng_seed + trial)

            # Input: unit-variance white Gaussian noise
            x = rng.standard_normal(n_samples)

            # Desired: plant output + tiny additive noise (-30 dB SNR floor)
            d_clean = np.convolve(x, h_true, mode="full")[:n_samples]
            obs_noise = 0.032 * rng.standard_normal(n_samples)   # ~-30 dB
            d = d_clean + obs_noise

            _, e, w_hist = lms_filter(x, d, n_taps, mu)
            mse_accumulator += e ** 2

            if mu == best_mu and trial == 0:
                w_hist_best = w_hist

        avg_mse = mse_accumulator / n_mc
        # Smooth with a simple moving average for display
        window = max(1, n_samples // 100)
        smoothed = np.convolve(avg_mse, np.ones(window) / window, mode="valid")
        iters    = np.arange(len(smoothed))
        ax_mse.plot(iters, 10 * np.log10(smoothed + 1e-12), label=f"mu={mu}")

    ax_mse.set_xlabel("Iteration")
    ax_mse.set_ylabel("MSE (dB)")
    ax_mse.set_title("Learning Curves (ensemble-averaged)")
    ax_mse.legend()
    ax_mse.grid(True, alpha=0.4)

    # Coefficient convergence for best_mu (one representative run)
    if w_hist_best is not None:
        for k in range(n_taps):
            ax_coef.plot(w_hist_best[:, k], alpha=0.75, label=f"w[{k}]")
            # Overlay true value as dashed horizontal line
            ax_coef.axhline(h_true[k], color="k", linestyle="--",
                            linewidth=0.6, alpha=0.4)

        ax_coef.set_xlabel("Iteration")
        ax_coef.set_ylabel("Coefficient value")
        ax_coef.set_title(f"Coefficient Convergence (mu={best_mu})\n"
                          f"Dashed lines = true plant coefficients")
        ax_coef.grid(True, alpha=0.4)

    plt.tight_layout()
    plt.savefig("/tmp/lms_system_id.png", dpi=120)
    plt.show()

    # Print final weight error for each mu (last single-trial run reused)
    print("\n=== System Identification Results ===")
    print(f"True plant coefficients: {h_true.round(4)}")
    for mu in mu_list:
        rng = np.random.default_rng(rng_seed)
        x = rng.standard_normal(n_samples)
        d_clean = np.convolve(x, h_true, mode="full")[:n_samples]
        d = d_clean + 0.032 * rng.standard_normal(n_samples)
        _, _, w_hist = lms_filter(x, d, n_taps, mu)
        w_final = w_hist[-1]
        err = np.linalg.norm(w_final - h_true)
        print(f"  mu={mu:<6}  final weights: {w_final.round(4)}  "
              f"||w-h_true||={err:.4f}")


# ---------------------------------------------------------------------------
# Application 2: Noise Cancellation
# ---------------------------------------------------------------------------

def run_noise_cancellation(n_samples: int = 3000,
                            mu_list: list[float] = None,
                            n_mc: int = 50,
                            rng_seed: int = 7) -> None:
    """
    Noise cancellation setup
    ------------------------
    Primary input   z(n) = s(n) + v1(n)
        s(n)  : sinusoidal signal of interest (unknown to the filter)
        v1(n) : noise that has passed through an unknown channel h_noise

    Reference input x(n) = v0(n)
        v0(n) : original noise source (correlated with v1 via h_noise)

    The LMS filter estimates h_noise applied to x(n) and subtracts the
    result from z(n).  At convergence, the output e(n) ≈ s(n).

    The desired signal fed to LMS is the PRIMARY input z(n) -- the algorithm
    does NOT see s(n) directly.  It learns to cancel the noise by minimising
    the error power, which at the optimum equals the signal power (irreducible).

    Parameters
    ----------
    n_samples : Number of samples per trial.
    mu_list   : Step sizes to compare.
    n_mc      : Monte Carlo runs for learning-curve averaging.
    rng_seed  : Base RNG seed.
    """
    if mu_list is None:
        mu_list = [0.0005, 0.002, 0.01]

    # Fixed noise channel (FIR, 6 taps)
    h_noise = np.array([0.8, -0.4, 0.2, 0.1, -0.05, 0.02])
    h_len   = len(h_noise)
    n_taps  = 12          # adaptive filter length (longer than h_noise)

    # Signal frequency (single tone)
    f0  = 0.05            # normalised frequency (fraction of sample rate)
    phi = np.pi / 3       # phase offset
    n   = np.arange(n_samples)
    s   = 0.5 * np.sin(2 * np.pi * f0 * n + phi)    # signal of interest

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("LMS Noise Cancellation", fontsize=13, fontweight="bold")
    ax_mse, ax_sig = axes

    best_mu   = mu_list[len(mu_list) // 2]
    e_best    = None
    z_best    = None

    for mu in mu_list:
        mse_accumulator = np.zeros(n_samples)

        for trial in range(n_mc):
            rng = np.random.default_rng(rng_seed + trial * 31)

            # Noise source and its correlated version through h_noise
            v0 = rng.standard_normal(n_samples)                       # reference
            v1 = np.convolve(v0, h_noise, mode="full")[:n_samples]    # primary noise

            # Primary input: signal + coloured noise
            z = s + v1

            # LMS: reference input = v0, desired = primary input z
            _, e, _ = lms_filter(v0, z, n_taps, mu)
            mse_accumulator += e ** 2

            if mu == best_mu and trial == 0:
                e_best = e.copy()
                z_best = z.copy()

        avg_mse = mse_accumulator / n_mc
        window  = max(1, n_samples // 100)
        smoothed = np.convolve(avg_mse, np.ones(window) / window, mode="valid")
        iters   = np.arange(len(smoothed))
        ax_mse.plot(iters, 10 * np.log10(smoothed + 1e-12), label=f"mu={mu}")

    ax_mse.axhline(10 * np.log10(np.mean(s ** 2)), color="r",
                   linestyle="--", linewidth=1.2, label="Signal power (floor)")
    ax_mse.set_xlabel("Iteration")
    ax_mse.set_ylabel("MSE (dB)")
    ax_mse.set_title("Learning Curves (ensemble-averaged)")
    ax_mse.legend()
    ax_mse.grid(True, alpha=0.4)

    # Show a snippet of the signal before/after cancellation
    if e_best is not None:
        seg = slice(2500, 2600)                      # 100-sample window near end
        t   = n[seg]
        ax_sig.plot(t, z_best[seg],   alpha=0.7, label="Noisy input z(n)")
        ax_sig.plot(t, e_best[seg],   alpha=0.9, label="Filter output e(n)")
        ax_sig.plot(t, s[seg],        "k--", linewidth=1.2, label="True signal s(n)")
        ax_sig.set_xlabel("Sample index")
        ax_sig.set_ylabel("Amplitude")
        ax_sig.set_title(f"Signal Recovery (mu={best_mu}, last 100 samples)")
        ax_sig.legend()
        ax_sig.grid(True, alpha=0.4)

    plt.tight_layout()
    plt.savefig("/tmp/lms_noise_cancel.png", dpi=120)
    plt.show()

    # SNR improvement
    print("\n=== Noise Cancellation Results ===")
    rng = np.random.default_rng(rng_seed)
    v0  = rng.standard_normal(n_samples)
    v1  = np.convolve(v0, h_noise, mode="full")[:n_samples]
    z   = s + v1
    snr_in  = 10 * np.log10(np.var(s) / np.var(v1))
    for mu in mu_list:
        _, e, _ = lms_filter(v0, z, n_taps, mu)
        # Use last quarter of signal (after convergence) for SNR estimate
        q3      = n_samples * 3 // 4
        e_q     = e[q3:]
        s_q     = s[q3:]
        resid   = e_q - s_q
        snr_out = 10 * np.log10(np.var(s_q) / (np.var(resid) + 1e-12))
        print(f"  mu={mu:<7}  Input SNR: {snr_in:.1f} dB  "
              f"Output SNR: {snr_out:.1f} dB  "
              f"Improvement: {snr_out - snr_in:.1f} dB")


# ---------------------------------------------------------------------------
# Step-size sensitivity analysis
# ---------------------------------------------------------------------------

def step_size_analysis(n_samples: int = 1000,
                        n_taps: int = 4,
                        rng_seed: int = 3) -> None:
    """
    Demonstrate the effect of step size on stability and convergence speed.

    The stability bound for LMS is:
        0 < mu < 1 / (n_taps * sigma_x^2)
    where sigma_x^2 is the input signal power.

    For unit-variance white input and n_taps=4, the bound is mu < 0.25.
    We sweep mu from well below to above this bound to show divergence.
    """
    rng    = np.random.default_rng(rng_seed)
    h_true = np.array([0.5, 0.3, -0.2, 0.1])
    x      = rng.standard_normal(n_samples)
    d      = np.convolve(x, h_true, mode="full")[:n_samples]

    # Theoretical stability bound (white input, sigma_x^2 = 1)
    mu_bound = 1.0 / (n_taps * 1.0)
    mu_vals  = [0.01, 0.05, 0.1, 0.2, mu_bound * 0.99, mu_bound * 1.1]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle("LMS Step-Size Sensitivity  "
                 f"(stability bound mu < {mu_bound:.3f})",
                 fontweight="bold")

    for mu in mu_vals:
        _, e, _ = lms_filter(x, d, n_taps, mu)
        mse_db  = 10 * np.log10(e ** 2 + 1e-20)
        label   = f"mu={mu:.3f}" + (" [UNSTABLE]" if mu > mu_bound else "")
        ax.plot(mse_db, alpha=0.8, label=label)

    ax.axvline(0, color="k", linewidth=0.5)
    ax.set_ylim(-60, 40)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Instantaneous MSE (dB)")
    ax.set_title("Instantaneous (not averaged) MSE per step size")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.4)

    plt.tight_layout()
    plt.savefig("/tmp/lms_step_size.png", dpi=120)
    plt.show()

    print("\n=== Step-Size Analysis ===")
    print(f"Theoretical stability bound: mu < {mu_bound:.4f}")
    for mu in mu_vals:
        _, e, _ = lms_filter(x, d, n_taps, mu)
        final_mse = np.mean(e[n_samples // 2:] ** 2)
        status    = "DIVERGED" if np.isnan(final_mse) or final_mse > 10 else "OK"
        print(f"  mu={mu:.4f}  steady-state MSE = {final_mse:.6f}  [{status}]")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Challenge 04: LMS Adaptive Filter Demonstrations")
    print("=" * 60)

    print("\n[1/3] Running System Identification...")
    run_system_identification(
        n_samples=2000,
        n_taps=8,
        mu_list=[0.001, 0.005, 0.01, 0.05],
        n_mc=50,
        rng_seed=0,
    )

    print("\n[2/3] Running Noise Cancellation...")
    run_noise_cancellation(
        n_samples=3000,
        mu_list=[0.0005, 0.002, 0.01],
        n_mc=50,
        rng_seed=7,
    )

    print("\n[3/3] Running Step-Size Sensitivity Analysis...")
    step_size_analysis(
        n_samples=1000,
        n_taps=4,
        rng_seed=3,
    )

    print("\nDone.  Plots saved to /tmp/lms_*.png")
