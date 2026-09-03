# R0.75A -- spectral-route risk audit for endpoint-only remote focusing

## 0. Corrected verdict and scope

This bounded audit reaches the following exact verdict.

1. No genuine counterexample is constructed to backward persistence of a
   *regional total-field kinetic floor* on a moving strip. The endpoint-only
   implication remains **OPEN**, not disproved.
2. A single Fourier mode strengthens backward in global and fixed-region
   kinetic energy. It cannot refute the lower-floor statement needed in
   Z.14; rapid relative change is irrelevant when only a lower bound is
   required.
3. Finite Fourier sums can interpolate prescribed values at finitely many
   times at one spatial point. This is a cancellation risk, but not yet a
   moving-strip kinetic counterexample.
4. The modal identity forces backward global \(L^2\)-amplification and
   Dirichlet dissipation. Converting this cost into localized, weighted
   Version-M payment requires an observability or capture inequality.

Thus semigroup algebra alone neither proves Z.39 nor disproves its
endpoint-to-backward-floor branch.  The subsequent main R0.75A note,
`research/r075a_spectral_persistence_payment_dichotomy.md` (frozen
SHA-256
`f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388`),
closes the W-kinetic endpoint/payment branch by a different mechanism: an
exact moving-cutoff local-energy identity followed by spacetime Hölder.
This file records why the spectral route alone was insufficient; it is not
the independent primary audit of that later theorem.

## 1. Exact common-shear modal identity

Let

\[
 \mathcal L_b g
 :=\partial_tg+b(t,x_3)\partial_2g-\Delta_{23}g=0
 \tag{A.1}
\]

on the \((x_2,x_3)\)-torus, where \(b\) is real and independent of \(x_2\).
Writing \(g=\sum_{n\in\mathbb Z}g_n(t,x_3)e^{inx_2}\), each mode solves

\[
 \partial_tg_n-\partial_3^2g_n+n^2g_n+inb\,g_n=0.
 \tag{A.2}
\]

The real part of the \(L^2_{x_3}\) pairing with \(g_n\) eliminates the
skew term:

\[
 \frac12\frac d{dt}\|g_n\|_2^2
 +\|\partial_3g_n\|_2^2+n^2\|g_n\|_2^2=0.
 \tag{A.3}
\]

Consequently, for \(s<t\),

\[
 \|g_n(s)\|_2\ge e^{n^2(t-s)}\|g_n(t)\|_2,
 \qquad
 \int_s^t n^2\|g_n(r)\|_2^2\,dr
 =
 \frac{\|g_n(s)\|_2^2-\|g_n(t)\|_2^2}{2}
 -\int_s^t\|\partial_3g_n\|_2^2\,dr.
 \tag{A.4}
\]

These are **rigorous modal identities** for smooth solutions. They control
global modal energy, not a localized moving strip where modes have cross
terms.

## 2. The single-mode test supports a backward floor

For \(b=0\) and terminal time \(t_*\), consider

\[
 g_N(t,x_2,x_3)
 =A e^{-N^2(t-t_*)}\cos(Nx_2),\qquad t\le t_*.
 \tag{A.5}
\]

For every fixed spatial region \(\Omega\),

\[
 \int_\Omega |g_N(t)|^2
 =e^{2N^2(t_*-t)}
   \int_\Omega |g_N(t_*)|^2
 \ge \int_\Omega |g_N(t_*)|^2 .
 \tag{A.6}
\]

Hence an endpoint regional kinetic floor persists backward, with increasing
strength. Although the field changes by order one on time scale \(N^{-2}\),
Z.14 requires a lower kinetic floor, not closeness to the terminal profile.
The previous purported single-mode counterexample is therefore withdrawn.
For a strip that does not move in \(x_2\), the same calculation applies.

## 3. Three distinct questions

### 3.1 One-mode endpoint-to-backward floor

For (A.5), the implication holds. More generally, (A.3) gives backward
growth of each *global modal norm*. This is positive evidence for a payment
alternative, not a localized theorem.

### 3.2 Cancellation of a primary at earlier times

For \(b=0\), distinct eigenvalues \(\lambda_j=|k_j|^2\) give at a fixed
point \(x_*\)

\[
 g(t,x_*)=\sum_{j=1}^M
 c_j e^{-\lambda_j(t-t_*)}\phi_j(x_*).
 \tag{A.7}
\]

At \(M\) distinct times the exponential Vandermonde matrix is generically
invertible. One may impose a nonzero terminal value and zeros at \(M-1\)
earlier times. This is a **rigorous finite point-interpolation observation**
when that matrix is nonsingular. Its coefficients may be extremely large.

This proves that modal monotonicity does not imply pointwise monotonicity of
the total signed field. It does not prove that the integral of \(|g|^2\)
over a positive-volume moving strip loses its floor throughout an interval.

### 3.3 Global orthogonality versus localized cancellation

Distinct modes are orthogonal on the full \(x_2\)-torus, so coefficients do
not cancel in global \(L^2\). A proper strip destroys orthogonality:

\[
 \int \chi(x)\left|\sum_j g_j\right|^2
 =
 \sum_{i,j}\int\chi(x)g_i\overline{g_j}.
 \tag{A.8}
\]

The off-diagonal terms can cancel locally. A genuine counterexample would
have to control them on the entire moving strip, retain a terminal kinetic
floor, solve the exact common-shear equation, and evade all Version-M
payment rows. No such construction is supplied here.

## 4. Conditional band-limited persistence

If \(g\) remains supported in \(|n|+|\xi_3|\le N\), and the shear and
commutators are uniformly controlled, Bernstein estimates give schematically

\[
 \|\partial_tg\|_2
 \lesssim (N^2+N\|b\|_\infty)\|g\|_2.
 \tag{A.9}
\]

Controlling the moving cutoff and retaining endpoint mass on a smaller
strip yields a time scale comparable to
\((N^2+N\|b\|_\infty)^{-1}\). Thus an \(R^3\) floor follows conditionally
from

\[
 N^2+N\|b\|_\infty\lesssim R^{-3},
 \tag{A.10}
\]

plus enlargement and occupation margins. This is not automatic:
multiplication by \(b(x_3)\) may generate \(x_3\)-frequencies, and moving
cutoffs contribute transport commutators. The intrinsic substitute is the
Z.22 generator envelope plus moving-strip all-winding uniformity.

## 5. Where backward amplification could enter \(P_R^M\)

* **Global identity -- rigorous.** Equations (A.3)--(A.4) force backward
  global energy and nonnegative Dirichlet dissipation. Temporal
  interpolation cannot cancel these modewise quantities.
* **Central row -- conditional.** The central Version-M row captures this
  only if a uniform fraction occupies the moving \(B_{8R}\) window. A remote
  endpoint floor alone does not state this.
* **Exterior or accumulated row from modal information -- conditional.** An exterior dissipation
  row captures (A.4) only if its weight is bounded below where the amplified
  mode travels and moving-cutoff flux errors are controlled. The exterior
  cubic row is not reached automatically by the global modal identity.
  The main R0.75A note reaches that row instead through a moving localized
  energy balance, including the critical and shorter-time branch.

Backward heat amplification is therefore a plausible payment mechanism,
not yet a Version-M lower bound. The missing bridge is a localized
observability-to-ledger inequality.

## 6. What a purely spectral proof would have required

Any proof needs at least one of the following packages.

1. **Generator envelope:** Z.22 on an enlarged moving strip, uniform
   all-winding comparison, and a strip-retention margin.
2. **Band limit plus occupation:** (A.10), spatial Bernstein control, and
   quantitative retention of endpoint kinetic mass in the moving strip.
3. **High-frequency capture:** a scale-uniform inequality sending the
   energy or dissipation in (A.4) into the central-energy,
   accumulated-viscosity, or exterior component of \(P_R^M\).
4. **Localized spectral observability:** explicit costs in frequency,
   number of modes, conditioning, moving shear, strip width, and time,
   followed by proof that the cost is paid by \(P_R^M\).

These packages are no longer needed for the W-kinetic endpoint/payment
claim: the main R0.75A moving-cutoff theorem proves the required two-case
estimate directly for the total smooth common-shear field, uniformly in
finite family size and conditioning.  The modal observations here remain
useful as a warning against substituting global orthogonality for localized
payment.

The complete Y.57 clock, a whole-shell upper comparison, fixed deletion,
and arbitrary-suitable-weak-solution consequences remain **OPEN**.  No
counterexample to Z.39 is claimed.  This audit proves no novelty and no
Navier--Stokes regularity or singularity result. **NOT CLAY.**
