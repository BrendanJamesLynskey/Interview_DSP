# Worked Problem 01: FIR Lowpass Filter Design — Parks-McClellan

**Subject:** Digital Signal Processing
**Topic:** FIR Filter Specification, Order Estimation, Parks-McClellan Design, Analysis
**Difficulty:** Intermediate to Advanced

---

## Problem Statement

Design a lowpass FIR filter meeting the following specifications:

- Sample rate: $f_s = 48\,\text{kHz}$
- Passband edge: $f_p = 8\,\text{kHz}$ with passband ripple $\leq 0.1\,\text{dB}$
- Stopband edge: $f_{stop} = 11\,\text{kHz}$ with stopband attenuation $\geq 60\,\text{dB}$

**Tasks:**

**(a)** Convert specifications to digital domain (normalised frequencies and ripple amplitudes).

**(b)** Estimate the required filter order using the Kaiser-Parks formula and the Bellanger formula.

**(c)** Describe how Parks-McClellan would design this filter. State the equiripple property and the role of the weighting function.

**(d)** Analyse the resulting filter: FIR type, group delay, magnitude response at key frequencies.

**(e)** Show a MATLAB `firpm` call and explain each argument.

**(f)** Compare against a windowed design (Kaiser window) of similar order. What is the key advantage of Parks-McClellan?

---

## Part (a): Specification Conversion

### Digital frequencies

$$\omega_p = 2\pi \frac{f_p}{f_s} = 2\pi \frac{8000}{48000} = \frac{\pi}{3} \approx 1.047\,\text{rad/sample}$$

$$\omega_{stop} = 2\pi \frac{f_{stop}}{f_s} = 2\pi \frac{11000}{48000} = \frac{11\pi}{24} \approx 1.440\,\text{rad/sample}$$

Normalised frequencies (fraction of Nyquist, $[0, 1]$ where 1 = Nyquist = $f_s/2$):

$$\hat{f}_p = \frac{f_p}{f_s/2} = \frac{8}{24} = 0.333, \qquad \hat{f}_{stop} = \frac{11}{24} \approx 0.458$$

### Transition bandwidth

$$\Delta\omega = \omega_{stop} - \omega_p = \frac{11\pi - 8\pi}{24} = \frac{3\pi}{24} = \frac{\pi}{8} = 0.3927\,\text{rad/sample}$$

$$\Delta f = f_{stop} - f_p = 3{,}000\,\text{Hz}$$

### Ripple amplitudes

**Passband ripple** ($R_p = 0.1\,\text{dB}$):

$$\delta_p = 10^{R_p/20} - 1 = 10^{0.005} - 1 \approx 0.01153$$

(so the passband gain is in $[1 - \delta_p, 1 + \delta_p]$)

**Stopband attenuation** ($A_s = 60\,\text{dB}$):

$$\delta_s = 10^{-A_s/20} = 10^{-3} = 0.001$$

**Summary:**

| Parameter | Hz | Rad/sample | Amplitude |
|---|---|---|---|
| Passband edge $f_p$ | 8,000 | $\pi/3$ | $\delta_p = 0.01153$ |
| Stopband edge $f_{stop}$ | 11,000 | $11\pi/24$ | $\delta_s = 0.001$ |
| Transition BW | 3,000 | $\pi/8$ | — |

---

## Part (b): Filter Order Estimation

### Kaiser-Parks Formula

$$N \approx \frac{-20\log_{10}(\sqrt{\delta_p\,\delta_s}) - 13}{14.6\,\Delta f/f_s} + 1$$

Computing:

$$\sqrt{\delta_p\,\delta_s} = \sqrt{0.01153 \times 0.001} = \sqrt{1.153 \times 10^{-5}} = 3.396 \times 10^{-3}$$

$$-20\log_{10}(3.396 \times 10^{-3}) = -20 \times (-2.469) = 49.37\,\text{dB}$$

$$N \approx \frac{49.37 - 13}{14.6 \times 3000/48000} + 1 = \frac{36.37}{0.9125} + 1 \approx 41.8 \Rightarrow N = 43$$

### Bellanger's Formula

$$N \approx \frac{2}{3}\log_{10}\!\left(\frac{1}{10\,\delta_p\,\delta_s}\right) \cdot \frac{f_s}{\Delta f}$$

$$= \frac{2}{3}\log_{10}\!\left(\frac{1}{10 \times 0.01153 \times 0.001}\right) \cdot \frac{48000}{3000}$$

$$= \frac{2}{3}\log_{10}(8672) \times 16 = \frac{2}{3} \times 3.938 \times 16 \approx 42.0$$

Both formulas agree: the filter requires approximately **43 taps** (even-numbered taps give Type II; use $N = 43$ for a Type I filter with group delay = 21 samples).

---

## Part (c): Parks-McClellan Algorithm Description

### The Weighted Chebyshev Problem

Parks-McClellan (Remez exchange) minimises the **maximum weighted approximation error** over the specified frequency bands:

$$\min_{\{h[n]\}} \max_{\omega \in [\omega_1,\omega_2] \cup [\omega_3,\omega_4]} W(\omega)\left|D(\omega) - A(\omega)\right|$$

where:
- $D(\omega)$: desired frequency response (1 in passband, 0 in stopband)
- $A(\omega)$: actual amplitude response of the FIR
- $W(\omega)$: frequency weighting function
- $[\omega_1, \omega_2] = [0, \omega_p]$: passband
- $[\omega_3, \omega_4] = [\omega_{stop}, \pi]$: stopband

### Weighting Function

The weighting function $W(\omega)$ controls the relative emphasis on passband vs stopband ripple:

$$W(\omega) = \begin{cases}
1 & \omega \in \text{passband} \\
\delta_p/\delta_s & \omega \in \text{stopband}
\end{cases}$$

Setting $W_{stop} = \delta_p/\delta_s = 0.01153/0.001 = 11.53$ tells the algorithm to make the stopband ripple $11.53\times$ smaller than the passband ripple.

### Equiripple Property

The optimal filter achieves the **Chebyshev equiripple property**: the weighted error alternates between $+\epsilon_{opt}$ and $-\epsilon_{opt}$ at exactly $L + 2$ or more frequencies (where $L = (N+1)/2 = 22$ for a 43-tap Type I filter).

The oscillation means:
- In the passband: the amplitude alternates between $1 + \epsilon_{opt}$ and $1 - \epsilon_{opt}$
- In the stopband: the amplitude alternates between $+W_{stop}\,\epsilon_{opt}$ and $-W_{stop}\,\epsilon_{opt}$

**No other 43-tap filter achieves a smaller maximum ripple in both bands simultaneously.**

### Algorithm Iterations

```
1. Start with L+2 = 23 trial extremal frequencies
2. Solve the equiripple system (Lagrange interpolation)
   → compute h[n] and error δ
3. Evaluate error |W(ω)(D(ω)-A(ω))| on fine frequency grid
4. Find the L+2 frequencies where error is largest (new extrema)
5. If extremal frequencies unchanged → converged, output h[n]
   Else → go to step 2
```

Convergence typically occurs in 5–25 iterations.

---

## Part (d): Analysis of the Resulting Filter

### Filter Type

$N = 43$ taps, odd length, symmetric coefficients $h[n] = h[42-n]$: **Type I** FIR.

All frequency responses are achievable (no restrictions at $\omega = 0$ or $\omega = \pi$).

### Group Delay

Linear phase: $\phi(\omega) = -\omega\,\alpha$ where $\alpha = (N-1)/2 = 21$.

$$\tau_g = -\frac{d\phi}{d\omega} = 21\,\text{samples} = \frac{21}{48000}\,\text{s} = 0.4375\,\text{ms}$$

This is a **constant** group delay across all frequencies — no phase distortion.

### Magnitude Response at Key Frequencies

| Frequency | Expected gain |
|---|---|
| $f = 0$ (DC) | $\approx 1.0$ (passband) |
| $f = 4\,\text{kHz}$ | $\approx 1.0 \pm 0.005$ (well inside passband) |
| $f = 8\,\text{kHz} = f_p$ | $1 \pm \delta_p$ (passband edge, peak ripple) |
| $f = 9.5\,\text{kHz}$ (transition band) | Unspecified — between 0 and 1 |
| $f = 11\,\text{kHz} = f_{stop}$ | $\leq \delta_s = 0.001 = -60\,\text{dB}$ |
| $f = 24\,\text{kHz}$ (Nyquist) | $\leq \delta_s$ (well in stopband) |

### Equiripple Verification

The Parks-McClellan design will show alternating extrema in both bands:

- Passband: approximately $\lfloor 22/2 \rfloor = 11$ ripple oscillations between 0 and $f_p$
- Stopband: approximately 11 oscillations between $f_{stop}$ and Nyquist
- All oscillations have the same peak amplitude (equiripple)

---

## Part (e): MATLAB `firpm` Call

```matlab
% Define filter specifications
fs = 48e3;                  % Sample rate (Hz)
fp = 8e3;                   % Passband edge (Hz)
fstop = 11e3;               % Stopband edge (Hz)
delta_p = 0.01153;          % Passband ripple amplitude
delta_s = 0.001;            % Stopband ripple amplitude

% Normalised frequency vector (fractions of Nyquist = fs/2)
f = [fp fstop] / (fs/2);   % [0.3333, 0.4583]

% Desired amplitudes: 1 in passband, 0 in stopband
d = [1 0];

% Weighting: relative emphasis on each band
W = [delta_s/delta_p 1];   % weight passband by delta_s/delta_p = 0.0867

% --- OR equivalently ---
W2 = [1 delta_p/delta_s];  % weight stopband by delta_p/delta_s = 11.53

% firpm(order, freq_edges, desired_amplitudes, weights)
% Note: firpm takes the filter ORDER (N-1), not the number of taps N
N_taps = 43;
h = firpm(N_taps - 1, [0, f, 1], [1, 1, 0, 0], W);
%         order=42  frequency edges   amplitude edges  weights

% Verify: length(h) should equal N_taps = 43
disp(length(h));   % 43

% Analyse
[H, w] = freqz(h, 1, 4096, fs);
plot(w/1000, 20*log10(abs(H)));
xlabel('Frequency (kHz)'); ylabel('Magnitude (dB)');
title('Parks-McClellan Lowpass FIR, 43 taps');
ylim([-80 5]); grid on;
```

**Explanation of arguments:**

| Argument | Value | Meaning |
|---|---|---|
| `N_taps - 1` | `42` | Filter ORDER (= taps minus 1) |
| `[0, f, 1]` | `[0, 0.333, 0.458, 1]` | Frequency band edges, normalised to Nyquist |
| `[1, 1, 0, 0]` | `[1 1 0 0]` | Desired amplitude at each edge: passband=1, stopband=0 |
| `W` | `[1, 11.53]` | Relative weight per band; stopband weighted higher |

---

## Part (f): Comparison with Kaiser Windowed Design

**Kaiser window design for same $A_s = 60\,\text{dB}$:**

$$\beta = 0.1102(60 - 8.7) = 5.65$$

$$N_{Kaiser} \approx \frac{60 - 8}{2.285 \times (\pi/8)} = \frac{52}{0.898} \approx 58 \text{ taps}$$

| Property | Parks-McClellan (43 taps) | Kaiser Window (58 taps) |
|---|---|---|
| Filter order | 42 | 57 |
| Number of taps | 43 | 58 |
| Passband ripple | Equiripple (all equal) | Varies — may have larger peak |
| Stopband attenuation | Equiripple, exactly 60 dB | Approximately 60 dB |
| Computation (MACs/sample) | 22 (exploit symmetry) | 29 |
| Design complexity | Iterative algorithm | Closed-form formula |
| Optimality | Yes — minimum order for spec | No — sub-optimal |

**Parks-McClellan advantage:** For the same specifications, Parks-McClellan achieves the minimum filter order. Here it needs 43 taps vs the Kaiser window's 58 — a 26% reduction. This translates directly to 26% fewer multiply-accumulate operations per output sample.

**Kaiser window advantage:** Simple to design without iterative computation. The MATLAB `kaiserord` + `firwin` workflow is a one-liner and always produces a valid design (Parks-McClellan can occasionally converge slowly for very demanding specifications).

**Rule of thumb:** Use Parks-McClellan when computational budget is tight (embedded systems, real-time DSP) and specifications are firm. Use Kaiser window for rapid prototyping or when the approximate design is iterated later.

---

## Summary

| Step | Result |
|---|---|
| Digital passband edge | $\omega_p = \pi/3$ |
| Digital stopband edge | $\omega_{stop} = 11\pi/24$ |
| Transition bandwidth | $\Delta\omega = \pi/8$ |
| Filter order (estimate) | $N \approx 43$ taps |
| Filter type | Type I (symmetric, odd) |
| Group delay | 21 samples = 0.4375 ms |
| Passband ripple | $\delta_p \leq 0.01153$ ($\leq 0.1\,\text{dB}$) |
| Stopband attenuation | $\delta_s \leq 0.001$ ($\geq 60\,\text{dB}$) |
| Weighting ratio | $\delta_p/\delta_s = 11.53$ |
