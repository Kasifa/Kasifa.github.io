# R0.73A finite frozen-time Orr--Sommerfeld spectral audit

**Date:** 2026-08-29
**Role:** exploratory counterexample screening and theorem design
**Validation decision:** **PASS AS A FINITE-DIMENSIONAL DIAGNOSTIC; NOT AN
INFINITE-DIMENSIONAL RESULT**

## 1. Question and hard boundary

For the frozen heat shear

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
\]

I audited the Fourier--Galerkin compressions of

\[
 A_{d,\beta,\mu,c}q
 =-\mathcal Lq-icWq-icW_{xx}\mathcal L^{-1}q,
 \qquad
 \mathcal L=(-i\partial_x+\beta)^2+\mu.
\]

The experiment asks three narrow questions.

1. Does the unprojected frozen matrix have a nonpositive spectral edge in the
   low-gap/strong-coupling region?
2. Does removing the instantaneous tangent vector
   \(q_*(d)=W_{xx}(d)\), or the whole low harmonic plane
   \(\operatorname{span}\{\sin x,\sin2x\}\), consistently improve that edge?
3. When a compressed matrix is spectrally stable, is a transient prefactor
   still numerically visible?

The answer below concerns finite matrices only.  There is no Galerkin tail
estimate, spectral-pollution theorem, infinite-dimensional resolvent passage,
or nonautonomous concatenation argument.  The two projected matrices are
modified compressions \(Q^*AQ\); they are not asserted to be invariant
quotients of the original Orr--Sommerfeld evolution.

## 2. Reproducible design

The source is
[`experiments/r073a/frozen_os_spectral_audit.py`](../experiments/r073a/frozen_os_spectral_audit.py).
The independent checker is
[`experiments/r073a/validate_frozen_os_spectral_audit.py`](../experiments/r073a/validate_frozen_os_spectral_audit.py).

In the basis \(e^{inx}\), \(-N\le n\le N\), I used

\[
 \lambda_n=(n+\beta)^2+\mu,
\]

\[
 A_{mn}=-\lambda_m\delta_{mn}
 -ic\widehat W_{m-n}
 -ic\widehat{W_{xx}}_{m-n}\lambda_n^{-1}.
\]

The three matrix families are:

- `unprojected`: \(A_N\);
- `qstar-Wxx`: \(Q_*^*A_NQ_*\), where
  \(\operatorname{ran}Q_*=q_*^\perp\);
- `span-sin1-sin2`: \(Q_{12}^*A_NQ_{12}\), where
  \(\operatorname{ran}Q_{12}=\{\sin x,\sin2x\}^\perp\).

The broad screen used \(N=18\) and the full Cartesian grid

\[
\begin{aligned}
d&\in\{0,0.05,0.25,1\},\\
\beta&\in\{0,10^{-4},10^{-3},10^{-2},0.05,0.25,0.49\},\\
\mu&\in\{10^{-6},10^{-4},10^{-2},10^{-1}\},\\
|c|&\in\{4,128,4096,131072\}.
\end{aligned}
\]

This gives 448 parameter cases and 1,344 matrix rows after the three
compressions.  Ten target cases, including
\(d=\alpha^2\), \(\mu=\alpha^2\) at \(\alpha=1/4,1/8\), were repeated at
\(N=12,18,24,32,40\).  Those 150 rows also record:

- spectral and numerical abscissae;
- eigenvector condition and Henrici departure;
- the largest singular norm sampled on 23 distinct times in
  \([0,8\alpha^2]\);
- a sampled right-edge resolvent/Kreiss grid and relative
  \(10^{-2}\)-pseudospectral excursion.

The time maximum is a **sampled maximum**, not a continuous-time optimizer.
The pseudospectral quantities are grid lower bounds/diagnostics, not certified
pseudospectral contours.

## 3. Main numerical decisions

### 3.1 Uniform frozen-time spectral stability is not a viable assumption

At broad-screen resolution, the number of positive spectral-edge rows was:

| compression | positive spectral rows | positive numerical-abscissa rows | total |
|---|---:|---:|---:|
| unprojected | 419 | 444 | 448 |
| remove \(W_{xx}\) | 357 | 414 | 448 |
| remove \(\sin x,\sin2x\) | 268 | 361 | 448 |

For the unprojected matrices, all 112 cases at each of
\(|c|=128,4096,131072\) had positive spectral edge.  At \(|c|=4\), 83 of
112 did.  More importantly, all ten target cases remained spectrally unstable
at \(N=40\).  Thus a proposed R0.73A proof should not begin by assuming a
uniformly stable frozen unprojected spectrum throughout this parameter box.

This is a screening result, not a theorem that the infinite-dimensional
frozen operator is unstable.  The converged-looking target rows identify
specific candidates for a later rigorous spectral enclosure or analytic
counterexample.

### 3.2 Removing only the instantaneous tangent vector is structurally weak

Removing \(W_{xx}(d)\) improved the broad-screen spectral edge in 307 of 448
cases, but worsened it in 141 cases and produced a nonpositive edge in only 91
cases.  This is consistent with the exact geometry: even at zero gap,

\[
 A(d)W_{xx}(d)=W_{xxxx}(d),
\]

and \(W_{xxxx}\) is not generally collinear with \(W_{xx}\).  Therefore the
one-dimensional instantaneous tangent line is not the evolving tangent
bundle.  A theorem based on a fixed orthogonal deletion of \(W_{xx}(d)\) alone
would need an additional connection term from the moving projection and
cannot be inferred from these compressed spectra.

### 3.3 The two-harmonic plane helps near the axis, but is not a universal cure

Removing \(\operatorname{span}\{\sin x,\sin2x\}\) improved 337 of 448 broad
cases and yielded a nonpositive spectral edge in 180 cases, but it worsened
111 cases.  At \(N=40\), only three of ten target compressions were
spectrally nonpositive:

| target | spectral edge | numerical abscissa | sampled gain on \([0,8\alpha^2]\) |
|---|---:|---:|---:|
| `T01-lowest-gap-c4`, remove two harmonics | \(-1.00\times10^{-6}\) | \(-1.00\times10^{-6}\) | 1.000 |
| `T05-post-collision`, remove two harmonics | \(-1.00\times10^{-4}\) | 336.082 | 2.054 |
| `T06-late-weak-bloch`, remove two harmonics | \(-2.00\times10^{-4}\) | 0.0282 | 1.043 |

The second row is the clearest theorem-design warning: a nonpositive frozen
spectrum does not remove nonnormal growth.  Its sampled Kreiss lower bound is
1.550, agreeing with the observed need for a transient prefactor.

### 3.4 Strong and collision-scale sentinels remain positive after projection

Representative \(N=40\) spectral edges are:

| target | unprojected | remove \(W_{xx}\) | remove two harmonics |
|---|---:|---:|---:|
| `T02-near-bloch-c128` | 60.621 | 10.442 | 2.219 |
| `T03-near-bloch-c4096` | 1581.427 | 426.612 | 29.665 |
| `T04-strong-c131072` | 50793.146 | 13529.243 | 3993.651 |
| `T07-off-axis` | 35.892 | 504.642 | 1148.240 |
| `T09-collision-alpha025` | 1413.517 | 286.610 | 1.546 |
| `T10-collision-alpha0125` | 50111.614 | 12615.905 | 7.889 |

The off-axis row demonstrates that compression is not monotone in spectral
stability: both proposed deletions can move the edge farther right.  The two
collision sentinels show a large reduction after deleting the low harmonic
plane, but not a sign change.  This makes a larger moving spectral subspace,
a parameter-dependent Schur complement, or a genuinely nonautonomous normal
form more plausible than a fixed two-mode deletion.

## 4. Truncation and pseudospectral audit

For every target/projection pair, the \(N=32\) to \(N=40\) spectral-edge
relative difference was below \(1.60\times10^{-3}\).  The maximum difference
between sampled base-10 log gains was \(5.67\times10^{-6}\).  The largest
absolute spectral drift was 0.551 for the `T10` one-vector compression, but
this is only \(4.4\times10^{-5}\) relative to its edge near 12,616.

These checks support using the targets as candidates.  They do not bound the
tail as \(N\to\infty\).

The sampled pseudospectral excursion is less stable under truncation in several
weak/stable compressed cases because its relative epsilon is scaled by the
full truncated matrix norm, which changes when new highly dissipative modes
are added.  I therefore do **not** use the reported pseudospectral abscissa as
a convergence claim.  The stable-case sampled Kreiss values and directly
sampled semigroup gains are the more interpretable finite diagnostics.

## 5. Independent validation and numerical incident ledger

The independent checker passed all 13 checks:

- exact parameter and row coverage;
- all manifest byte counts and SHA-256 hashes;
- source-script SHA-256 binding;
- no NaN or infinite recorded metric;
- exact zero-gap tangent cancellation;
- four independent matrix/spectrum spot checks, with maximum discrepancy
  \(1.10\times10^{-11}\);
- \(N=32\) to \(N=40\) target spectral/gain convergence threshold;
- explicit finite-dimensional and projection-compression boundaries.

During the first strong-coupling run, direct `expm(A*t)` overflowed.  That run
was discarded.  The final source shifts by the numerical abscissa
\(\omega(A)\), computes

\[
 e^{tA}=e^{t\omega(A)}e^{t(A-\omega(A)I)},
\]

and restores the norm in the logarithmic domain.  Values beyond binary64 are
marked as censored lower-scale records rather than stored as NaN or as a fake
finite gain.  The complete final run was then repeated from scratch and the
manifest was independently hash-checked.

Environment and provenance are recorded in
[`environment.json`](../experiments/r073a/environment.json),
[`manifest.json`](../experiments/r073a/manifest.json), and
[`progress.ndjson`](../experiments/r073a/progress.ndjson).  The final run used
Python 3.12, NumPy 2.5.2, SciPy 1.18.1, one BLAS/OpenMP thread, no GPU, and no
randomness.

## 6. Consequence for the next theorem

The finite audit argues against the simplest proposed theorem:

> “Delete \(W_{xx}\), prove every frozen remainder is spectrally stable, and
> concatenate the frozen semigroups.”

The data instead support the following research route.

1. Treat the heat-tangent trajectory as a **moving low-dimensional bundle**,
   not a fixed one-vector projection.  Include the projection-connection term.
2. Allow an explicit transient prefactor; stable compressed rows can still be
   strongly nonnormal.
3. Seek a block decomposition or Schur complement that expands beyond
   \(\{\sin x,\sin2x\}\) at strong coupling and off-axis Bloch parameters.
4. Prove analytic spectral/resolvent enclosures for a few converged target
   matrices before generalizing.  The best first candidates are `T01`, `T05`,
   and `T06`; `T07` is a useful negative control.
5. Keep frozen spectral information subordinate to a nonautonomous energy or
   evolution-family argument.  Frozen instability does not by itself decide
   the time-dependent propagator, just as frozen stability would not justify
   concatenation without controlling moving eigenspaces.

## 7. Claim ledger

| statement | status |
|---|---|
| finite Fourier matrix formula and parameter sweep | **CHECKED** |
| exact zero-gap tangent cancellation | **CHECKED** |
| unprojected target compressions have positive spectral edge | **CHECKED at declared truncations** |
| fixed one-vector/two-harmonic deletion uniformly stabilizes the sweep | **NEGATIVE in the finite sweep** |
| stable compressed rows may require transient prefactor | **CHECKED in sampled finite semigroups** |
| continuous-time maximum gain | **NOT COMPUTED** |
| converged pseudospectrum | **NOT CERTIFIED** |
| infinite-dimensional spectral instability/stability | **OPEN** |
| Galerkin passage or tail estimate | **OPEN** |
| nonautonomous low-gap OS propagator | **OPEN** |
| physical direct sum, nonlinear NSE, or Clay problem | **OPEN** |
