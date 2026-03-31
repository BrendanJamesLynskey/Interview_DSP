# Digital Signal Processing — Interview Preparation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Subject: DSP](https://img.shields.io/badge/Subject-Digital%20Signal%20Processing-blue)](https://en.wikipedia.org/wiki/Digital_signal_processing)

## Overview

This repository provides comprehensive interview preparation material for Digital Signal Processing (DSP) roles in both software and hardware engineering. The material covers DSP theory from first principles, modern algorithms, and practical implementation techniques across microcontrollers, FPGAs, and general-purpose processors.

The structure progresses from foundational signal processing concepts through advanced topics including adaptive filtering, communications DSP, and real-world implementation considerations. Each section includes both theoretical explanations and worked problems that reflect interview-level questions.

## Table of Contents

- [01 Fundamentals](#01-fundamentals)
- [02 Filter Design](#02-filter-design)
- [03 Spectral Analysis](#03-spectral-analysis)
- [04 Adaptive and Statistical Methods](#04-adaptive-and-statistical-methods)
- [05 Communications DSP](#05-communications-dsp)
- [06 Implementation](#06-implementation)
- [07 Quizzes](#07-quizzes)
- [How to Use](#how-to-use)
- [Related Repositories](#related-repositories)
- [Contributing](#contributing)

### 01 Fundamentals

Core DSP signal theory, transformations, and foundational concepts.

- `signals_and_systems.md` — Continuous and discrete signals, system properties, stability
- `sampling_and_aliasing.md` — Nyquist theorem, anti-aliasing filters, sampling rate conversion
- `z_transform.md` — Bilateral and unilateral Z-transforms, poles and zeros, stability regions
- `dtft_and_dft.md` — Discrete-time Fourier transform, discrete Fourier transform, periodicity
- `convolution_and_correlation.md` — Linear and circular convolution, correlation properties
- `worked_problems/` — Three comprehensive problems covering Nyquist scenarios, Z-transform analysis, and circular convolution

### 02 Filter Design

Systematic filter design techniques and modern optimization methods.

- `fir_filter_design.md` — Finite impulse response design, linear phase, windowing
- `iir_filter_design.md` — Infinite impulse response design, stability, bilinear transformation
- `filter_structures.md` — Direct form, cascade, parallel, and lattice implementations
- `multirate_signal_processing.md` — Decimation, interpolation, polyphase filters
- `window_functions.md` — Window design and trade-offs, spectral characteristics
- `worked_problems/` — Four problems covering Parks-McClellan algorithm, bilinear transform, polyphase decimators, and CIC filters

### 03 Spectral Analysis

Frequency domain analysis, FFT algorithms, and time-frequency representations.

- `fft_algorithm.md` — Cooley-Tukey FFT, radix-2 and radix-4, butterfly operations
- `spectral_leakage_and_windowing.md` — Windowing effects, scallop loss, spectral resolution
- `power_spectral_density.md` — Welch's method, periodogram, autocorrelation techniques
- `stft_and_time_frequency.md` — Short-time Fourier transform, spectrograms, time-frequency uncertainty
- `worked_problems/` — Three problems on FFT butterflies, spectral resolution, and overlap-add/save methods

### 04 Adaptive and Statistical Methods

Adaptive algorithms and statistical signal processing.

- `lms_and_nlms.md` — Least mean squares algorithm, normalized variants, convergence analysis
- `rls_algorithm.md` — Recursive least squares, Kalman gain, exponential weighting
- `wiener_filter.md` — Wiener filter derivation, optimal filtering, Wiener-Hopf equation
- `kalman_filter_basics.md` — State-space models, Kalman equations, recursive estimation
- `worked_problems/` — Three problems on LMS convergence, acoustic echo cancellation, and Wiener solution computation

### 05 Communications DSP

DSP applications in digital communications systems.

- `modulation_and_demodulation.md` — Amplitude, phase, and frequency modulation schemes, demodulation techniques
- `pulse_shaping_and_isi.md` — Nyquist pulse shaping, raised cosine, intersymbol interference mitigation
- `ofdm.md` — Orthogonal frequency-division multiplexing, subcarrier design, cyclic prefix
- `synchronisation.md` — Timing and frequency synchronization, carrier recovery, pilot symbols
- `worked_problems/` — Three problems on QAM bit-error rate, raised cosine filtering, and OFDM subcarrier spacing

### 06 Implementation

Practical considerations for real-world DSP system implementation.

- `fixed_point_arithmetic.md` — Fixed-point number systems, overflow handling, quantization effects
- `dsp_on_fpga.md` — FPGA resources, pipelines, parallel architectures, Verilog/SystemVerilog patterns
- `dsp_on_microcontrollers.md` — DSP optimizations, intrinsics, SIMD techniques, memory constraints
- `numerical_precision.md` — Floating-point arithmetic, precision loss, accumulation errors
- `coding_challenges/` — Six implementation challenges including FIR filters, FFT, fixed-point arithmetic, LMS, and RTL designs

### 07 Quizzes

Self-assessment quizzes covering all major topic areas.

- `quiz_fundamentals.md` — Questions on signals, transforms, and convolution
- `quiz_filters.md` — FIR, IIR, and filter design methodology
- `quiz_spectral.md` — FFT, spectral analysis, and windowing
- `quiz_adaptive.md` — Adaptive filters and statistical methods
- `quiz_comms.md` — Communications DSP and modulation
- `quiz_implementation.md` — Implementation techniques and practical considerations

## How to Use

This repository is structured as a self-contained DSP interview preparation course:

1. **Linear Progression**: Begin with 01_fundamentals if your DSP background is limited. Each section builds on prior knowledge.

2. **Topic Mastery**: For each section, read the primary topic files in order, then work through the corresponding problems before moving to the next section.

3. **Worked Problems**: Every worked problem includes a complete solution with derivations and explanations. Attempt problems independently before reviewing solutions.

4. **Coding Challenges**: The challenges in 06_implementation require actual code implementation. Test your implementations thoroughly, considering edge cases and numerical precision.

5. **Quizzes**: Use quizzes after completing each section to verify conceptual understanding. These reflect the breadth and depth of interview-level questions.

6. **Interview Preparation**: Review quizzes 1-2 weeks before interviews. Focus on areas where you struggled in earlier sections.

7. **Practical Reference**: Keep filter design and implementation techniques sections accessible during system design interview discussions.

## Related Repositories

- **[PhaseVocoder](https://github.com/BrendanJamesLynskey/PhaseVocoder)** — A production DSP implementation demonstrating time-stretching and pitch-shifting algorithms with phase coherence management
- **[Interview_VHDL](../Interview_VHDL)** — VHDL-specific patterns for HDL-based DSP implementations
- **[Interview_Verilog](../Interview_Verilog)** — SystemVerilog and Verilog RTL design for DSP hardware

## Contributing

Contributions are welcome. Please ensure:

1. Content is technically accurate and clearly explained
2. Worked problems include complete derivations and final answers
3. Code examples are tested and follow the project's coding conventions
4. Quiz questions reflect realistic interview scenarios
5. Mathematical notation is consistent with standard DSP literature

For significant additions (new sections, major revisions), please open an issue first to discuss scope and approach.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
