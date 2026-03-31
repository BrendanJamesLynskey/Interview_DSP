# Worked Problem 01: Nyquist Scenarios

**Subject:** Digital Signal Processing
**Topic:** Sampling Rate, Aliasing, Bandpass Sampling
**Difficulty:** Intermediate

---

## Problem Statement

Analyse the following four sampling scenarios. For each, determine whether aliasing occurs, identify any alias frequencies, and state the minimum correct sampling rate.

**Scenario A:** Audio signal with components up to 20 kHz. Sampling rate $f_s = 44.1\,\text{kHz}$.

**Scenario B:** Signal with spectral content at exactly 4 kHz. Sampling rate $f_s = 6\,\text{kHz}$.

**Scenario C:** Signal with spectral content at 2 kHz and 5 kHz. Sampling rate $f_s = 6\,\text{kHz}$.

**Scenario D:** Bandpass signal occupying $[8, 10]\,\text{kHz}$ with bandwidth $B = 2\,\text{kHz}$. Find the minimum sampling rate without baseband downconversion.

---

## Scenario A — Audio at 20 kHz, $f_s = 44.1\,\text{kHz}$

### Step 1: Nyquist criterion check

Nyquist frequency (half the sample rate):

$$f_N = \frac{f_s}{2} = \frac{44100}{2} = 22{,}050\,\text{Hz}$$

Signal bandwidth: $f_{max} = 20{,}000\,\text{Hz}$.

Criterion: $f_s > 2\,f_{max}$?

$$44{,}100 > 40{,}000 \quad \checkmark$$

### Step 2: Guard band

$$\Delta f_{guard} = f_N - f_{max} = 22{,}050 - 20{,}000 = 2{,}050\,\text{Hz}$$

The anti-aliasing filter must transition from passband to stopband within 2,050 Hz — a narrow but achievable transition band.

### Step 3: Spectral picture

```
Magnitude
   |
   |  Signal  |Guard|       Replicas
   |  [0, 20k]|     |   [24.1k, 44.1k]
   |__________|     |___________________
   0          20k   22.05k    44.1k   f (Hz)
```

No aliasing. The first replica (centred at $f_s = 44.1\,\text{kHz}$) begins at $44.1 - 20 = 24.1\,\text{kHz}$, well above $f_N$.

### Answer A
No aliasing. The 44.1 kHz standard satisfies the Nyquist criterion with a 2,050 Hz guard band. The minimum sampling rate for 20 kHz audio is $f_{s,min} > 40,000\,\text{Hz}$. The 44.1 kHz standard was historically chosen to fit audio on video tape (3 samples per line, 490 active lines, 30 frames/s = 44,100 samples/s).

---

## Scenario B — 4 kHz tone, $f_s = 6\,\text{kHz}$

### Step 1: Nyquist check

$$f_N = 3{,}000\,\text{Hz}$$

Signal frequency: $f_0 = 4{,}000\,\text{Hz} > 3{,}000\,\text{Hz} = f_N$

**Aliasing will occur.**

### Step 2: Find the alias frequency

Aliasing folds frequencies above $f_N$ back into the range $[0, f_N]$.

$$f_{alias} = |f_0 - k\,f_s| \quad \text{for integer } k \text{ that maps to } [0, f_N]$$

For $k = 1$:

$$f_{alias} = |4000 - 6000| = 2000\,\text{Hz}$$

### Step 3: Verification — do both signals produce the same samples?

Sample the 4 kHz tone at $T_s = 1/6000\,\text{s}$:

$$x_{4k}[n] = \cos\!\left(2\pi \cdot 4000 \cdot \frac{n}{6000}\right) = \cos\!\left(\frac{4\pi n}{3}\right)$$

Sample the 2 kHz tone:

$$x_{2k}[n] = \cos\!\left(2\pi \cdot 2000 \cdot \frac{n}{6000}\right) = \cos\!\left(\frac{2\pi n}{3}\right)$$

Are they equal? Evaluate at $n = 0, 1, 2, 3$:

| $n$ | $x_{4k}[n]$ | $x_{2k}[n]$ |
|---|---|---|
| 0 | $\cos(0) = 1$ | $\cos(0) = 1$ |
| 1 | $\cos(4\pi/3) = -0.5$ | $\cos(2\pi/3) = -0.5$ |
| 2 | $\cos(8\pi/3) = \cos(2\pi/3) = -0.5$ | $\cos(4\pi/3) = -0.5$ |
| 3 | $\cos(4\pi) = 1$ | $\cos(2\pi) = 1$ |

The sequences are **identical** — the two tones are indistinguishable. The 4 kHz component has permanently corrupted the record as a 2 kHz artefact.

### Step 4: Spectral picture

```
True spectrum       After sampling at 6 kHz
      |                    |
      |  *4kHz*            |  *2kHz (alias)*
      |                    |
   0    2k   3k  4k   6k   0    2k   3k  f (Hz)
                 ^f_N             ^f_N
```

### Step 5: Minimum sampling rate

$$f_{s,min} > 2 \times 4{,}000 = 8{,}000\,\text{Hz}$$

In practice, use 8 kHz (telephone standard) with an anti-aliasing filter cutting off below 4 kHz.

### Answer B
Aliasing occurs. The 4 kHz component aliases to **2 kHz**. The minimum sampling rate is $f_{s,min} > 8\,\text{kHz}$.

---

## Scenario C — Components at 2 kHz and 5 kHz, $f_s = 6\,\text{kHz}$

### Step 1: Check each component

$f_N = 3{,}000\,\text{Hz}$

- 2 kHz component: $2 < 3$ kHz — within the Nyquist band, **no aliasing**
- 5 kHz component: $5 > 3$ kHz — **aliases**

### Step 2: Alias of 5 kHz at $f_s = 6\,\text{kHz}$

$$f_{alias} = |5000 - 6000| = 1000\,\text{Hz}$$

### Step 3: Consequences

| Component | True frequency | Recorded frequency |
|---|---|---|
| Component 1 | 2,000 Hz | 2,000 Hz (clean) |
| Component 2 | 5,000 Hz | 1,000 Hz (alias) |

After sampling, the digital record contains components at 1 kHz and 2 kHz. The original 5 kHz tone is **lost** and a spurious 1 kHz artefact is **added** — this is indistinguishable from a genuine 1 kHz signal in the original.

The alias at 1 kHz is also spectrally close to the legitimate 2 kHz component, which would corrupt any downstream frequency analysis or filter.

### Step 4: Minimum sampling rate

To capture both components without aliasing:

$$f_{s,min} > 2 \times 5{,}000 = 10{,}000\,\text{Hz}$$

### Answer C
The 2 kHz component is recorded correctly; the 5 kHz component aliases to **1 kHz**, corrupting the record. Minimum sampling rate: $f_s > 10\,\text{kHz}$.

---

## Scenario D — Bandpass Signal $[8, 10]\,\text{kHz}$, Bandwidth $B = 2\,\text{kHz}$

### Step 1: Naive Nyquist rate

If treated as a baseband signal, the naive criterion requires:

$$f_{s,naive} = 2 \times f_H = 2 \times 10{,}000 = 20{,}000\,\text{Hz}$$

This is conservative — it ignores that the signal occupies only a 2 kHz slice.

### Step 2: Bandpass sampling theory

For a bandpass signal with $f_L = 8\,\text{kHz}$, $f_H = 10\,\text{kHz}$, $B = 2\,\text{kHz}$:

The valid sampling rates satisfy, for integer $m = 1, 2, \ldots, \lfloor f_H/B \rfloor = \lfloor 5 \rfloor = 5$:

$$\frac{2\,f_H}{m} \leq f_s \leq \frac{2\,f_L}{m-1}$$

(The upper bound is $\infty$ for $m=1$.)

### Step 3: Enumerate valid ranges

| $m$ | Lower: $2f_H/m$ (kHz) | Upper: $2f_L/(m-1)$ (kHz) | Valid range (kHz) |
|---|---|---|---|
| 1 | 20.0 | $\infty$ | $[20, \infty)$ — naive case |
| 2 | 10.0 | 16.0 | $[10, 16]$ |
| 3 | 6.67 | 8.0 | $[6.67, 8]$ |
| 4 | 5.0 | 5.33 | $[5, 5.33]$ |
| 5 | 4.0 | 4.0 | $\{4.0\}$ — exact value |

### Step 4: Choose a practical sampling rate

**Theoretical minimum:** $f_s = 4.0\,\text{kHz}$ (exactly $2B$). However, this is the exact boundary and requires a perfect bandpass anti-aliasing filter — not realisable.

**Practical choice from $m = 3$:** $f_s = 7\,\text{kHz}$ (within $[6.67, 8]$).

Verify: Nyquist frequency = 3.5 kHz. Signal bandwidth = 2 kHz. The band folds as:

- $k=0$ replica: $[8, 10]$ kHz — filtered by the bandpass AAF
- $k=1$ fold: $[8-7, 10-7] = [1, 3]$ kHz — **this is the desired baseband alias**
- $k=-1$ fold: $[8+7, 10+7] = [15, 17]$ kHz — above $f_s/2 = 3.5$ kHz? No — replicas repeat at $f_s = 7$ kHz intervals. Within $[0, 3.5]$ kHz there is only the $[1, 3]$ kHz replica.

The bandpass AAF must pass $[8, 10]$ kHz and reject everything else before sampling.

### Step 5: Spectral picture after bandpass sampling at 7 kHz

```
 Magnitude
    |
    |  1kHz  3kHz        8kHz  10kHz
    |  [desired alias]   [original band]
    |___|____|____________|____|____
    0   1    3            8   10     f (kHz)
            ^ f_N = 3.5k
```

After lowpass filtering to [0, 3.5] kHz, the signal occupies [1, 3] kHz — a baseband-like representation of the bandpass signal. Its instantaneous frequency within [1, 3] kHz corresponds to [8, 10] kHz in the original.

### Answer D

Valid bandpass sampling rates include: $[10, 16]\,\text{kHz}$, $[6.67, 8]\,\text{kHz}$, $[5, 5.33]\,\text{kHz}$, $\{4.0\}\,\text{kHz}$.

**Practical recommendation:** $f_s = 7\,\text{kHz}$ (from the $[6.67, 8]$ range), giving a 2.8x reduction over the naive 20 kHz rate. Use a bandpass anti-aliasing filter that passes $[8, 10]\,\text{kHz}$ before sampling.

---

## Summary Table

| Scenario | Signal Frequencies | $f_s$ | Aliasing? | Alias Frequencies | Min $f_s$ |
|---|---|---|---|---|---|
| A | $[0, 20]$ kHz | 44.1 kHz | No | — | $> 40$ kHz |
| B | 4 kHz | 6 kHz | Yes | 2 kHz | $> 8$ kHz |
| C | 2 kHz, 5 kHz | 6 kHz | 5 kHz aliases | 5 kHz $\to$ 1 kHz | $> 10$ kHz |
| D | $[8, 10]$ kHz | — | Designed aliasing | Band folds to $[1,3]$ kHz | $4$ kHz (theoretical), $\sim 7$ kHz (practical) |

---

## Key Takeaways

1. **Any component above $f_N = f_s/2$ will alias.** No digital processing can undo aliasing after the fact.

2. **Aliasing is not always accidental** — bandpass sampling deliberately aliases a signal to a lower frequency band, reducing data rate while preserving information.

3. **Guard band matters** — in Scenario A, the 2,050 Hz guard band allows for a realistically steep anti-aliasing filter rather than a theoretical brick-wall.

4. **The alias of $f_0$ at sampling rate $f_s$ is** $f_{alias} = f_0 \bmod f_s$, folded to $[0, f_s/2]$.
