# Adaptive and Statistical DSP — Multiple-Choice Quiz

**Topics covered:** LMS algorithm (step size bounds, convergence, misadjustment), NLMS, RLS vs LMS trade-offs, Wiener filter (Wiener-Hopf equations), Kalman filter (prediction and update steps), acoustic echo cancellation.

**Instructions:** Select the single best answer for each question. The answer key with detailed explanations appears at the bottom.

---

## Questions

**Q1.** The LMS (Least Mean Squares) adaptive filter updates its weight vector according to:

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \mu\, e[n]\, \mathbf{x}[n]$$

For the algorithm to converge in the mean, the step size $\mu$ must satisfy:

A. $\mu > 0$  
B. $0 < \mu < \frac{1}{\lambda_{max}}$, where $\lambda_{max}$ is the largest eigenvalue of the input autocorrelation matrix $\mathbf{R}_{xx}$  
C. $0 < \mu < \frac{2}{\lambda_{max}}$, where $\lambda_{max}$ is the largest eigenvalue of $\mathbf{R}_{xx}$  
D. $0 < \mu < \frac{1}{\text{tr}(\mathbf{R}_{xx})}$, where $\text{tr}$ denotes the matrix trace

---

**Q2.** The misadjustment $\mathcal{M}$ of the LMS algorithm quantifies:

A. The time taken for the weight vector to converge to the Wiener solution.  
B. The excess mean-squared error (EMSE) relative to the minimum MSE, expressed as a ratio: $\mathcal{M} = \text{EMSE} / J_{min}$.  
C. The gradient noise introduced by using an instantaneous estimate rather than the true gradient.  
D. The sensitivity of the algorithm to input signal conditioning.

---

**Q3.** The Normalised LMS (NLMS) algorithm modifies the LMS update to:

$$\mathbf{w}[n+1] = \mathbf{w}[n] + \frac{\mu}{\|\mathbf{x}[n]\|^2 + \epsilon}\, e[n]\, \mathbf{x}[n]$$

The primary motivation for this normalisation is:

A. To ensure the step size is always exactly 1.  
B. To make the effective step size independent of the input signal power, improving convergence when input power varies.  
C. To eliminate the need for a regularisation term $\epsilon$.  
D. To guarantee convergence to the globally optimal Wiener solution in a single step.

---

**Q4.** The Wiener-Hopf equation for the optimal linear filter in a stationary environment is:

$$\mathbf{R}_{xx}\, \mathbf{w}^* = \mathbf{r}_{xd}$$

where $\mathbf{r}_{xd}$ is the cross-correlation vector between the input $x[n]$ and the desired signal $d[n]$. The minimum MSE achievable is:

A. $J_{min} = \sigma_d^2 - \mathbf{r}_{xd}^T \mathbf{R}_{xx} \mathbf{r}_{xd}$

B. $J_{min} = \sigma_d^2 - \mathbf{r}_{xd}^T \mathbf{R}_{xx}^{-1} \mathbf{r}_{xd}$

C. $J_{min} = \mathbf{w}^{*T} \mathbf{R}_{xx} \mathbf{w}^* - \mathbf{r}_{xd}^T \mathbf{w}^*$

D. $J_{min} = \sigma_d^2 \left(1 - \frac{\|\mathbf{r}_{xd}\|^2}{\|\mathbf{R}_{xx}\|_F^2}\right)$

---

**Q5.** Compared to the LMS algorithm, the Recursive Least Squares (RLS) algorithm:

A. Converges more slowly but has lower computational complexity.  
B. Converges faster and handles non-stationary inputs better, at the cost of $O(M^2)$ complexity per update (where $M$ is filter length).  
C. Has the same convergence rate but is numerically more stable.  
D. Converges faster only when the input autocorrelation matrix is diagonal.

---

**Q6.** In RLS, the forgetting factor $\lambda$ (typically $0.95 \leq \lambda \leq 1$) controls:

A. The step size of the gradient descent update.  
B. The exponentially weighted memory window: smaller $\lambda$ makes the algorithm more responsive to recent data but more sensitive to noise.  
C. The regularisation of the inverse correlation matrix to prevent numerical singularity.  
D. The convergence rate by scaling the input power estimate.

---

**Q7.** The condition number $\kappa(\mathbf{R}_{xx}) = \lambda_{max}/\lambda_{min}$ of the input autocorrelation matrix affects LMS convergence because:

A. High condition number means the eigenvalues are all close to zero, slowing convergence.  
B. High condition number causes the LMS learning curve to have multiple time constants, with the slowest mode governed by $\lambda_{min}$, leading to slow overall convergence.  
C. High condition number means the LMS step size must be increased to speed up convergence.  
D. The condition number is irrelevant to LMS convergence — only the filter length matters.

---

**Q8.** In acoustic echo cancellation (AEC), the adaptive filter models the acoustic echo path from the loudspeaker to the microphone. Which of the following events requires the adaptive filter to re-converge most rapidly?

A. A brief pause in the far-end speech signal.  
B. Near-end speech (double-talk), which can corrupt the error signal and cause filter divergence.  
C. Gain changes in the near-end microphone amplifier.  
D. Changes in the far-end speaker's voice pitch.

---

**Q9.** The Kalman filter operates in two alternating steps. The prediction (time update) step computes:

$$\hat{\mathbf{x}}_{n|n-1} = \mathbf{F}\,\hat{\mathbf{x}}_{n-1|n-1}$$
$$\mathbf{P}_{n|n-1} = \mathbf{F}\,\mathbf{P}_{n-1|n-1}\,\mathbf{F}^T + \mathbf{Q}$$

What does the matrix $\mathbf{Q}$ represent?

A. The measurement noise covariance matrix.  
B. The process noise covariance matrix, representing uncertainty in the system dynamics model.  
C. The Kalman gain matrix.  
D. The state transition model error covariance after one prediction step.

---

**Q10.** The Kalman gain $\mathbf{K}_n$ in the measurement update step is:

$$\mathbf{K}_n = \mathbf{P}_{n|n-1}\,\mathbf{H}^T \left(\mathbf{H}\,\mathbf{P}_{n|n-1}\,\mathbf{H}^T + \mathbf{R}\right)^{-1}$$

When the measurement noise covariance $\mathbf{R} \to \infty$, the Kalman gain approaches:

A. $\mathbf{K}_n \to \mathbf{I}$ (identity matrix)  
B. $\mathbf{K}_n \to \mathbf{H}^{-1}$  
C. $\mathbf{K}_n \to \mathbf{0}$ (zero matrix)  
D. $\mathbf{K}_n \to \mathbf{P}_{n|n-1}\,\mathbf{H}^T$

---

**Q11.** A Kalman filter is applied to track the frequency of a slowly drifting sinusoid in noise. The state vector includes frequency and phase. If the process noise $\mathbf{Q}$ is set much larger than necessary, what happens?

A. The filter ignores all measurements and predicts purely from the model.  
B. The filter over-trusts the model and tracks the drift very slowly.  
C. The filter over-trusts the measurements, leading to a noisy (jittery) frequency estimate.  
D. The filter diverges because the covariance matrix becomes singular.

---

**Q12.** The LMS algorithm can be interpreted as performing stochastic gradient descent on which cost function?

A. The $\ell_1$ norm of the weight vector  
B. The instantaneous squared error $J[n] = e^2[n]$, using it as an approximation to $E[e^2[n]]$  
C. The regularised least squares cost with $\ell_2$ penalty on weights  
D. The Kullback-Leibler divergence between the desired and actual output distributions

---

**Q13.** In the frequency-domain LMS (FLMS) or overlap-save LMS algorithm, the weight update is performed in the frequency domain. The main advantage over time-domain LMS for long adaptive filters is:

A. FLMS converges to a better solution than time-domain LMS.  
B. FLMS has lower misadjustment for the same step size.  
C. The per-sample computational complexity is reduced from $O(M)$ to $O(\log M)$ by using the FFT for the convolution in the gradient computation.  
D. FLMS eliminates the need for a forgetting factor.

---

**Q14.** For the Wiener filter applied to signal estimation in additive noise ($d[n] = s[n] + v[n]$, where $s[n]$ and $v[n]$ are uncorrelated), the optimal Wiener filter in the frequency domain is:

A. $H_{opt}(e^{j\omega}) = \dfrac{S_{ss}(e^{j\omega})}{S_{xx}(e^{j\omega})}$

B. $H_{opt}(e^{j\omega}) = \dfrac{S_{ss}(e^{j\omega})}{S_{ss}(e^{j\omega}) + S_{vv}(e^{j\omega})}$

C. $H_{opt}(e^{j\omega}) = \dfrac{S_{xd}(e^{j\omega})}{S_{vv}(e^{j\omega})}$

D. $H_{opt}(e^{j\omega}) = 1 - \dfrac{S_{vv}(e^{j\omega})}{S_{xx}(e^{j\omega})}$

---

**Q15.** In acoustic echo cancellation, the term "double-talk" refers to:

A. The echo signal having a double delay path (direct and reflected).  
B. Both the near-end and far-end speakers being simultaneously active.  
C. The adaptive filter having two convergence modes — fast and slow.  
D. The loudspeaker signal being fed back twice through the room impulse response.

---

**Q16.** The convergence time constant of the LMS algorithm for the $k$th eigenmode is approximately:

$$\tau_k \approx \frac{1}{4 \mu \lambda_k}$$

where $\lambda_k$ is the $k$th eigenvalue of $\mathbf{R}_{xx}$. For a white noise input with variance $\sigma_x^2$ and filter length $M$, all eigenvalues equal $\sigma_x^2$. The convergence time constant becomes:

A. $\tau \approx \frac{M}{4\mu\sigma_x^2}$ — proportional to the filter length  
B. $\tau \approx \frac{1}{4\mu\sigma_x^2}$ — independent of filter length  
C. $\tau \approx \frac{1}{4\mu M \sigma_x^2}$ — inversely proportional to filter length  
D. $\tau \approx \frac{\sigma_x^2}{4\mu M}$ — increases with input power

---

**Q17.** The Extended Kalman Filter (EKF) handles nonlinear systems by:

A. Applying the standard Kalman equations to the original nonlinear state equations without modification.  
B. Linearising the nonlinear state and measurement equations around the current state estimate using first-order Taylor expansion, then applying the standard Kalman update.  
C. Approximating the nonlinear functions with piecewise linear segments over the full state space.  
D. Using particle filtering to represent the posterior distribution with a set of weighted samples.

---

**Q18.** The misadjustment of the LMS algorithm with step size $\mu$ and filter length $M$ operating on white input with variance $\sigma_x^2$ is approximately:

$$\mathcal{M} \approx \mu M \sigma_x^2$$

This implies that to achieve 1% misadjustment ($\mathcal{M} = 0.01$) with $M = 100$ taps and $\sigma_x^2 = 1$, the step size should be set to:

A. $\mu = 0.1$  
B. $\mu = 0.001$  
C. $\mu = 0.0001$  
D. $\mu = 1$

---

## Answer Key

| Q | Answer |
|---|--------|
| 1 | C |
| 2 | B |
| 3 | B |
| 4 | B |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | B |
| 10 | C |
| 11 | C |
| 12 | B |
| 13 | C |
| 14 | B |
| 15 | B |
| 16 | B |
| 17 | B |
| 18 | C |

---

## Detailed Explanations

**Q1 — Answer: C**

The LMS convergence-in-mean condition requires that the step size satisfy $0 < \mu < \frac{2}{\lambda_{max}}$, where $\lambda_{max}$ is the maximum eigenvalue of the input autocorrelation matrix $\mathbf{R}_{xx}$. This bound comes from the condition that the weight error update matrix $(\mathbf{I} - \mu \mathbf{R}_{xx})$ has all eigenvalues with magnitude less than 1, which requires $|1 - \mu\lambda_k| < 1$ for all $k$, giving $\mu < 2/\lambda_k$ for each $k$, and the binding constraint is $\lambda_{max}$. Option B is too conservative by a factor of 2. Option D uses the trace (sum of eigenvalues) and since $\text{tr}(\mathbf{R}_{xx}) = \sum_k \lambda_k \geq \lambda_{max}$, this bound is even more conservative and not the standard result.

---

**Q2 — Answer: B**

Misadjustment $\mathcal{M}$ is defined as the ratio of the excess mean-squared error (the extra MSE due to weight noise from using the stochastic gradient rather than the true gradient) to the minimum achievable MSE $J_{min}$:

$$\mathcal{M} = \frac{J_\infty - J_{min}}{J_{min}} = \frac{\text{EMSE}}{J_{min}}$$

Option A describes convergence speed (which is characterised by the time constant $\tau$). Option C correctly identifies the source of misadjustment (gradient noise) but this is the mechanism, not the definition. Option D describes a condition number concept unrelated to misadjustment.

---

**Q3 — Answer: B**

In the standard LMS, the effective step size $\mu$ interacts with the input power $\|\mathbf{x}[n]\|^2$. When the input power varies (e.g., in speech, power varies by 30–40 dB), a fixed $\mu$ that works well for high-power segments may be too large (causing divergence) or too small (causing slow convergence) for other segments. NLMS divides $\mu$ by $\|\mathbf{x}[n]\|^2 + \epsilon$, making the effective step size proportional to $1/\|\mathbf{x}[n]\|^2$ and thus approximately independent of input power. Option A is wrong — the effective step size is $\mu/\|\mathbf{x}[n]\|^2$, not fixed at 1. Option C is wrong — $\epsilon > 0$ is required to prevent division by zero when the input is very small. Option D is wrong — NLMS still converges iteratively, not in one step.

---

**Q4 — Answer: B**

The minimum MSE for the Wiener filter is derived from the MSE surface. Starting from $J = E[e^2] = \sigma_d^2 - 2\mathbf{w}^T\mathbf{r}_{xd} + \mathbf{w}^T\mathbf{R}_{xx}\mathbf{w}$, substituting the optimal weight $\mathbf{w}^* = \mathbf{R}_{xx}^{-1}\mathbf{r}_{xd}$:

$$J_{min} = \sigma_d^2 - \mathbf{r}_{xd}^T\mathbf{R}_{xx}^{-1}\mathbf{r}_{xd}$$

Option A omits the matrix inverse — a common error. Option C gives the MSE in terms of the weight vector but does not simplify to the minimum. Option D uses the Frobenius norm in a way that has no basis in the derivation.

---

**Q5 — Answer: B**

RLS minimises the exponentially weighted least-squares cost directly, solving the normal equations at each step using the matrix inversion lemma (Woodbury identity) to update $\mathbf{R}^{-1}$ recursively. This gives faster convergence — typically on the order of $2M$ iterations (where $M$ is the filter length) vs hundreds of iterations for LMS. The cost is $O(M^2)$ per update for standard RLS vs $O(M)$ for LMS. RLS also handles non-stationary environments well when $\lambda < 1$. Option A reverses the convergence speed comparison. Option C is wrong on both counts — RLS has higher complexity and is often less numerically stable than LMS. Option D is wrong — RLS advantage holds for all input statistics.

---

**Q6 — Answer: B**

The RLS forgetting factor $\lambda$ down-weights past data exponentially: a sample at lag $k$ contributes $\lambda^k$ to the cost function. The effective memory length is approximately $1/(1-\lambda)$ samples. With $\lambda = 0.99$, the memory is about 100 samples; with $\lambda = 0.95$, about 20 samples. Smaller $\lambda$ makes the filter more adaptive (tracks faster changes) but also more sensitive to noise, increasing variance of the weight estimates. Option A confuses $\lambda$ with the LMS step size. Option C is the role of the regularisation term (also called loading factor), not $\lambda$. Option D — the forgetting factor scales the correlation matrix, but its primary interpretation is the memory window.

---

**Q7 — Answer: B**

The LMS learning curve for the $k$th eigenmode has a time constant $\tau_k \approx 1/(4\mu\lambda_k)$. When the condition number $\kappa = \lambda_{max}/\lambda_{min}$ is large, the modes associated with $\lambda_{min}$ converge very slowly (large $\tau$) while the modes associated with $\lambda_{max}$ converge quickly. The overall convergence is limited by the slowest mode. Furthermore, the step size is constrained by $\lambda_{max}$: to avoid instability, $\mu < 2/\lambda_{max}$, which then makes $\tau_{min} = 1/(4\mu\lambda_{min})$ very large. Option A is wrong — high condition number means a large spread of eigenvalues, not all near zero. Option C is wrong — increasing $\mu$ risks instability. Option D is false.

---

**Q8 — Answer: B**

During double-talk, both near-end and far-end speakers are active. The LMS/NLMS error signal $e[n] = d[n] - \hat{y}[n]$ is supposed to contain only the acoustic echo estimation error. During double-talk, the near-end speech adds to $d[n]$, corrupting $e[n]$ with components unrelated to the echo path. The update $\Delta\mathbf{w} \propto e[n]\mathbf{x}[n]$ then pushes the filter away from the true echo path model, potentially causing divergence. Double-talk detection (DTD) algorithms suppress updates during double-talk. Option A (silence) actually helps — with no far-end signal, there is no echo to cancel and convergence pauses harmlessly. Options C and D are minor perturbations that do not fundamentally corrupt the error signal.

---

**Q9 — Answer: B**

In the Kalman filter state-space model $\mathbf{x}_n = \mathbf{F}\mathbf{x}_{n-1} + \mathbf{G}\mathbf{u}_n$, the process noise $\mathbf{u}_n \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$ represents random disturbances driving the system away from the deterministic model trajectory — wind gusts in navigation, random accelerations in target tracking, etc. $\mathbf{Q}$ is the covariance of this process noise. Option A describes $\mathbf{R}$, the measurement noise covariance. Option C describes $\mathbf{K}_n$, the Kalman gain. Option D is a description of $\mathbf{P}_{n|n-1}$ (the predicted error covariance), not $\mathbf{Q}$.

---

**Q10 — Answer: C**

From the Kalman gain formula: $\mathbf{K}_n = \mathbf{P}_{n|n-1}\mathbf{H}^T(\mathbf{H}\mathbf{P}_{n|n-1}\mathbf{H}^T + \mathbf{R})^{-1}$. As $\mathbf{R} \to \infty$, the term $\mathbf{H}\mathbf{P}_{n|n-1}\mathbf{H}^T$ becomes negligible compared to $\mathbf{R}$, so $(\mathbf{H}\mathbf{P}\mathbf{H}^T + \mathbf{R})^{-1} \approx \mathbf{R}^{-1} \to \mathbf{0}$. Therefore $\mathbf{K}_n \to \mathbf{0}$. Intuitively: if the measurements are extremely noisy, the filter should ignore them entirely and rely only on the model prediction. When $\mathbf{R} \to \mathbf{0}$ (perfect measurements), $\mathbf{K}_n \to \mathbf{H}^{-1}$ (for square $\mathbf{H}$), meaning the state estimate is pulled entirely toward the measurement. Options A and B are wrong limits. Option D would be the limit only if $\mathbf{R} = \mathbf{0}$ and we normalised differently.

---

**Q11 — Answer: C**

$\mathbf{Q}$ governs how much the filter trusts the state transition model. A large $\mathbf{Q}$ tells the Kalman filter "the state can change dramatically between steps; the model is unreliable." Consequently, $\mathbf{P}_{n|n-1}$ (the predicted covariance) grows large at each prediction step, leading to a large Kalman gain $\mathbf{K}_n$. A large gain means the state estimate is updated aggressively based on each measurement. If the measurements are noisy, this makes the state estimate noisy and jittery. Option A describes the effect of large $\mathbf{R}$ (not $\mathbf{Q}$). Option B describes the opposite — small $\mathbf{Q}$ makes the filter conservative. Option D can occur in practice due to numerical issues but is not the primary behavioural effect.

---

**Q12 — Answer: B**

The LMS weight update $\mathbf{w}[n+1] = \mathbf{w}[n] + \mu e[n]\mathbf{x}[n]$ is obtained by computing $-\nabla_\mathbf{w} e^2[n] = 2e[n]\mathbf{x}[n]$ — the gradient of the instantaneous squared error $e^2[n]$ with respect to $\mathbf{w}$. The true gradient of the MSE $E[e^2[n]]$ would require knowledge of the statistics; LMS uses the noisy (stochastic) approximation $e^2[n]$ in place of $E[e^2[n]]$. This is stochastic gradient descent on the MSE surface. Option A ($\ell_1$ norm) corresponds to LASSO or LMS with sign-error variant. Option C is LMS with $\ell_2$ regularisation (leaky LMS). Option D describes maximum likelihood estimation for Gaussian distributions but is not the LMS derivation.

---

**Q13 — Answer: C**

For an adaptive filter of length $M$, time-domain LMS requires $O(M)$ multiplications per sample for the filtering operation and $O(M)$ for the gradient update, total $O(M)$. The FLMS computes the convolution using block FFTs: for a block of $L$ samples, an $O(L \log L)$ FFT replaces $O(L \cdot M)$ time-domain multiplications. The per-sample complexity is $O(\log M)$ (for $L \approx M$). For long adaptive filters used in AEC (echo path lengths of 100–500 ms correspond to hundreds to thousands of taps), this speedup is crucial. Options A and B are wrong — FLMS converges to the same Wiener solution with essentially the same misadjustment. Option D — forgetting factor is an RLS concept.

---

**Q14 — Answer: B**

For signal estimation in additive uncorrelated noise $x[n] = s[n] + v[n]$, the cross-power spectrum is $S_{xd}(e^{j\omega}) = S_{xs}(e^{j\omega}) = S_{ss}(e^{j\omega})$ (since the desired signal is $s[n]$), and the input power spectrum is $S_{xx}(e^{j\omega}) = S_{ss}(e^{j\omega}) + S_{vv}(e^{j\omega})$. The Wiener-Hopf equation in frequency gives:

$$H_{opt}(e^{j\omega}) = \frac{S_{xd}(e^{j\omega})}{S_{xx}(e^{j\omega})} = \frac{S_{ss}(e^{j\omega})}{S_{ss}(e^{j\omega}) + S_{vv}(e^{j\omega})}$$

This is the classical Wiener filter for signal estimation (also related to the Wiener filter for speech enhancement). Option A omits the noise PSD in the denominator. Option C uses only the noise PSD in the denominator. Option D is the spectral subtraction formula, which is an approximation to the Wiener filter but not exact.

---

**Q15 — Answer: B**

Double-talk is the condition in a telephone or teleconference system where both the near-end person (whose microphone picks up the echo plus their own voice) and the far-end person are speaking simultaneously. The adaptive filter needs the error signal to reflect only the unmodelled echo; near-end speech contaminates this signal and causes the filter to diverge from the true echo path. Double-talk detectors (e.g., the Geigel algorithm or cross-correlation based methods) pause the LMS update during double-talk. Options A, C, and D describe physical phenomena unrelated to the double-talk definition.

---

**Q16 — Answer: B**

For white noise input, all eigenvalues of $\mathbf{R}_{xx}$ equal $\sigma_x^2$ (the input variance). Substituting into the time constant formula:

$$\tau_k = \frac{1}{4\mu\lambda_k} = \frac{1}{4\mu\sigma_x^2}$$

This is the same for all $k$ (since all eigenvalues are equal) and is independent of the filter length $M$. The filter length $M$ does affect the total misadjustment $\mathcal{M} \approx \mu M \sigma_x^2$, but not the convergence time constant for white inputs. Option A incorrectly includes $M$. Options C and D have wrong dependencies. This white noise result explains why pre-whitening the input speeds up LMS convergence for coloured inputs.

---

**Q17 — Answer: B**

The Extended Kalman Filter linearises the nonlinear functions $\mathbf{f}(\cdot)$ (state transition) and $\mathbf{h}(\cdot)$ (measurement) around the current state estimate $\hat{\mathbf{x}}_{n|n}$ using first-order Taylor series (Jacobian matrices). The Jacobians $\mathbf{F}_n = \partial\mathbf{f}/\partial\mathbf{x}|_{\hat{\mathbf{x}}}$ and $\mathbf{H}_n = \partial\mathbf{h}/\partial\mathbf{x}|_{\hat{\mathbf{x}}}$ replace the constant matrices in the standard Kalman equations. Option A is wrong — the standard Kalman equations are not valid for nonlinear systems. Option C describes a piecewise approximation, not EKF. Option D describes particle filtering, a completely different (Monte Carlo) approach to nonlinear/non-Gaussian filtering.

---

**Q18 — Answer: C**

Using the misadjustment formula $\mathcal{M} \approx \mu M \sigma_x^2 = 0.01$ with $M = 100$ and $\sigma_x^2 = 1$:

$$\mu = \frac{\mathcal{M}}{M \sigma_x^2} = \frac{0.01}{100 \times 1} = 0.0001$$

Option A ($\mu = 0.1$) gives $\mathcal{M} = 0.1 \times 100 \times 1 = 10$ — 1000% misadjustment, completely unreasonable. Option B ($\mu = 0.001$) gives $\mathcal{M} = 0.1$ — 10% misadjustment, close but not 1%. Option D ($\mu = 1$) would almost certainly violate the stability bound $\mu < 2/\lambda_{max}$ and cause divergence. This calculation illustrates why long adaptive filters (large $M$) require very small step sizes to achieve low misadjustment.
