# R0.72P -- a two-carrier full-superposition enhanced-dissipation theorem and its sharp Morse wall

**Date:** 2026-08-27

**Status:** a proof-grade full-superposition enhanced-dissipation theorem for
one fixed commensurate two-carrier class inside the common-band triangular
2.5D Navier--Stokes family.  For carriers \(R\) and \(2R\), coefficients on
one real phase line (aligned when \(\lambda>0\), anti-aligned when
\(\lambda<0\)), and relative coefficient
\(0<\lambda_-\le |\lambda|\le 1/8\), the complete Fourier propagator on the
affine invariant frequency row isomorphic to \(R\mathbb Z\) satisfies both
the integrated and terminal
estimates required in R0.72O, with constants independent of
\(R\), the coupling \(\varepsilon\ge1\), and \(\lambda\) in the declared
interval.  The proof keeps all self and cross terms.  The coefficient
\(|\lambda|=1/4\) is an exact Morse-degeneracy wall for this phase-aligned
1:2 pattern.  The result does not cover arbitrary phases, arbitrary carrier
sets, growing carrier count, or general three-dimensional Navier--Stokes
solutions.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, enhanced
dissipation, full superposition, two-carrier shear, Morse margin,
commensurate Fourier lattice, cross cubic

---

## 0. Direct decision

R0.72O isolated the missing multi-carrier hypothesis as

\[
 \int_0^1E(y)\,dy
 \le C_{\rm ED}\varepsilon^{-1/2}E(0),
 \qquad
 E(1)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon}E(0).
 \tag{0.1}
\]

The constants in (0.1) must apply to the **full superposition**.  Proving a
one-carrier estimate and summing it does not control the true cross cubics.

This section proves (0.1) for the following fixed two-carrier class.  Set

\[
 \nu=d=K_z=q_*=1,\qquad K_y=0,
 \tag{0.2}
\]

and, for \(R\in\mathbb N\), choose

\[
 r_1=R,\qquad r_2=2R,\qquad
 w_1=a,\qquad w_2=\lambda a,
 \tag{0.3}
\]

where \(a>0\), the two coefficients are real, and

\[
 0<\lambda_-\le |\lambda|\le\lambda_+:=\frac18.
 \tag{0.4}
\]

Take the common-band coherence parameter \(B=2\).  Then

\[
 N=2,\qquad p=\frac{\sqrt N}{B}=\frac1{\sqrt2},
 \qquad
 \varepsilon=\frac{2|\delta|a}{R^2}.
 \tag{0.5}
\]

The affine frequency row

\[
 \Lambda_{R,q_*}=\{(nR,q_*):n\in\mathbb Z\}
 \tag{0.5a}
\]

is invariant and isometrically isomorphic to \(\ell^2(\mathbb Z)\).  For
every initial datum on this row, including the row-aligned launch and the
exact-root correction inherited from R0.72L, the full propagator obeys

\[
\boxed{
 E(y)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon\,y}E(0),
 \qquad 0\le y\le1,}
 \tag{0.6}
\]

and hence (0.1).  Here \(C_{\rm ED}\ge1\) and \(c_{\rm ED}>0\) depend only
on the fixed upper shape bound \(\lambda_+=1/8\), not on
\(R,\varepsilon,\lambda\) or the initial datum.  The lower bound
\(\lambda_->0\) is needed later only to keep both carriers in the inherited
amplitude-balanced \(N=2\) physical family; the semigroup estimate itself
also includes the one-carrier endpoint \(\lambda=0\).

R0.72O's full-superposition argument now applies without a conditional
semigroup hypothesis.  For this declared class,

\[
\boxed{
 \mathcal C_\times\lesssim a^2N^2\sqrt\varepsilon
 =4a^2\sqrt\varepsilon.}
 \tag{0.7}
\]

The implicit constant in this physical comparison may depend on the fixed
amplitude-balance floor \(\lambda_-\); the enhanced-dissipation constants in
(0.6) do not.

The physical numerator and strong window are therefore

\[
 U_{\rm ED}\asymp\varepsilon^{11/6}p^{4/3},
 \tag{0.8}
\]

\[
\boxed{
 \sqrt\varepsilon
 \lesssim p^{2/3}R^{2/3}L_{R,\varepsilon},
 \qquad
 \varepsilon
 \lesssim p^{4/3}R^{4/3}L_{R,\varepsilon}^{2},
 \quad p=2^{-1/2}.}
 \tag{0.9}
\]

This closes R0.72O's full-superposition gate for a nontrivial two-carrier
pattern.  It does not make (0.1) uniform over arbitrary common-band
carrier sets.

---

## 1. Exact reduction of the full lattice

In the triangular class, the active Fourier lattice satisfies

\[
 \partial_xF=D_qF+\delta V_w(x)F,
 \qquad
 (D_qF)_r=-(r^2+1)F_r,
 \tag{1.1}
\]

and

\[
 (V_w(x)F)_r
 =-i\sum_{l=1}^2e^{-r_l^2x}
 \left(w_lF_{r-r_l}+\overline{w_l}F_{r+r_l}\right).
 \tag{1.2}
\]

The fixed target frequency \(q_*\) is orthogonal to the shear-carrier
direction.  The coefficients in (0.3) are real.  On the affine row
\(\Lambda_{R,q_*}\), write the shear-direction frequency as \(nR\).
Under Fourier transform in \(n\), the complete two-carrier operator is
multiplication by

\[
 -2ia\left[e^{-R^2x}\cos(R\theta)
 +\lambda e^{-4R^2x}\cos(2R\theta)\right].
 \tag{1.3}
\]

Both shifts preserve the affine row.  Put

\[
 y=R^2x,\qquad \phi=R\theta,
 \qquad
 G(y,\phi)=\sum_{n\in\mathbb Z}F_{(nR,q_*)}(R^{-2}y)e^{in\phi}.
 \tag{1.4}
\]

Then (1.1)--(1.3) give the exact cell equation

\[
 \partial_yG
 =(\partial_\phi^2-R^{-2})G
 -is\varepsilon W_\lambda(y,\phi)G,
 \qquad s=\operatorname{sign}\delta,
 \tag{1.5}
\]

where

\[
 W_\lambda(y,\phi)
 =e^{-y}\cos\phi+\lambda e^{-4y}\cos2\phi.
 \tag{1.6}
\]

No carrierwise expansion has been made.  Equation (1.5) contains the
complete two-carrier superposition.

For \(\varepsilon>0\), set

\[
 t=\varepsilon y,\qquad \eta=\varepsilon^{-1},
 \qquad
 H(t,\phi)=e^{R^{-2}\eta t}G(\eta t,\phi).
 \tag{1.7}
\]

The common orthogonal-target damping is removed and

\[
 \partial_tH
 =\eta\partial_\phi^2H
 -isW_\lambda(\eta t,\phi)H.
 \tag{1.8}
\]

This is the \(k=1\), \(\sigma=0\) horizontal Fourier mode of the
time-dependent passive-scalar equation in Coble--He with actual shear
\(V=sW_\lambda\).  Equivalently, one may take \(k=s\) and
\(V=W_\lambda\); only the product \(kV=sW_\lambda\) enters the equation.
The cell reduction
is essential: applying their theorem directly on the original \(\theta\)-torus
would see \(2R\) critical points and neighborhoods of radius \(O(R^{-1})\),
so it would not give an \(R\)-uniform constant.

---

## 2. Exact uniform shape lemma

Write

\[
 \alpha(y)=\lambda e^{-3y}.
 \tag{2.1}
\]

The derivative of the full shear factors exactly:

\[
 \partial_\phi W_\lambda
 =-e^{-y}\sin\phi\,[1+4\alpha(y)\cos\phi].
 \tag{2.2}
\]

For \(|\lambda|\le1/8\) and \(0\le y\le1\),

\[
 \frac12
 \le1+4\alpha(y)\cos\phi
 \le\frac32.
 \tag{2.3}
\]

Therefore the critical set is exactly

\[
 \mathcal C=\{0,\pi\}\pmod{2\pi}
 \tag{2.4}
\]

for the entire time interval.  It is independent of \(y,R,\varepsilon\)
and \(\lambda\) in the declared class.

Let \(d(\phi,\mathcal C)\in[0,\pi/2]\) be the circular distance to the
critical set.  Since \(e^{-1}>1/3\),
\(\sin d\ge d/2\) for \(0\le d\le\pi/4\), and
\(\sin d\ge1/2\) for \(\pi/4\le d\le\pi/2\), (2.2)--(2.3) imply

\[
 \frac1{12}d(\phi,\mathcal C)
 \le|\partial_\phi W_\lambda|
 \le\frac32d(\phi,\mathcal C)
 \quad\text{when }d(\phi,\mathcal C)<\frac\pi4,
 \tag{2.5}
\]

and

\[
 \frac1{12}
 \le|\partial_\phi W_\lambda|
 \le\frac32
 \quad\text{when }d(\phi,\mathcal C)\ge\frac\pi4.
 \tag{2.6}
\]

Thus Coble--He's shape assumptions hold with the safe fixed choices

\[
 N_{\rm crit}=2,\qquad r=\frac\pi4,\qquad
 \mathfrak C_0=144,\qquad \mathfrak C_1=12.
 \tag{2.7}
\]

The derivative bounds through third order are also uniform:

\[
 \|W_\lambda\|_\infty\le\frac98,\qquad
 \|\partial_\phi W_\lambda\|_\infty\le\frac54,\qquad
 \|\partial_\phi^2W_\lambda\|_\infty\le\frac32,\qquad
 \|\partial_\phi^3W_\lambda\|_\infty\le2.
 \tag{2.8}
\]

For the reference shear take the actual shear itself,

\[
 U(t,\phi)=V(t,\phi)=sW_\lambda(\eta t,\phi).
 \tag{2.9}
\]

The shared-critical-point and derivative-sign conditions are then exact.
Moreover,

\[
 \|\partial_{t\phi}U\|_\infty
 \le\eta(1+8|\lambda|)
 \le2\eta.
 \tag{2.10}
\]

If \(\eta\le1/16\), then \(2\eta\le\eta^{3/4}\), which is precisely the
slow-reference condition.

---

## 3. Uniform extraction from the time-dependent shear theorem

Coble--He Theorem 1.2 is stated for one pair \((U,V)\), with a threshold
written as \(\eta_0(U,V)\).  A parameter-uniform conclusion requires
checking how that threshold is produced; it cannot be inferred from the
notation alone.

For the class above, the proof gives a uniform threshold:

1. the two critical points are fixed, so the same two cutoff functions can
   be used for every \(\lambda,R,\varepsilon\);
2. their Appendix A spectral inequality uses only the fixed cutoff
   derivatives and the shape constants in (2.7);
3. the constants \(C_*\), \(\mathfrak C_{\rm spec}\), and
   \(\|U_{\phi\phi}\|_\infty\) entering their hypocoercive parameters are
   bounded by (2.7)--(2.8);
4. the small-viscosity absorption in Appendix A therefore has one threshold
   for the complete declared \(\lambda\)-class;
5. (2.10) supplies the remaining slow-time restriction.

Consequently the proof supplies a family-uniform threshold
\(\eta_0^{\rm CH}>0\).  Define

\[
 \eta_\sharp=\min\{1/16,\eta_0^{\rm CH}\}.
 \tag{3.1a}
\]

There is \(c_\sharp>0\), depending only on the fixed shape class, such that
for

\[
 0<\eta\le\eta_\sharp,
 \qquad 0\le t\le\eta^{-1},
 \tag{3.1}
\]

the solution of (1.8) satisfies

\[
 \|H(t)\|_2
 \le e\,e^{-c_\sharp\eta^{1/2}t}\|H(0)\|_2.
 \tag{3.2}
\]

The restriction \(1/16\) closes only the slow-time inequality; the second
threshold in (3.1a) is the small-viscosity absorption threshold extracted
from the Coble--He proof.  That proof, not merely a finite sample of
profiles, supplies the uniformity.
The result is a corollary extracted for this fixed family; it is not a
verbatim arbitrary-family theorem stated by Coble and He.

The theorem is stated for smooth data.  Approximation by Fourier truncation,
followed by the exact \(L^2\) contraction, extends the same estimate to every
\(L^2\) initial datum on the affine row.

Returning to \(y\) and using the extra factor
\(e^{-R^{-2}y}\le1\), (3.2) gives, for
\(\varepsilon\ge\varepsilon_\sharp:=\eta_\sharp^{-1}\),

\[
 E(y)=\|G(y)\|_2^2
 \le e^2e^{-2c_\sharp\sqrt\varepsilon\,y}E(0),
 \qquad 0\le y\le1.
 \tag{3.3}
\]

---

## 4. Integrated and terminal estimates

Integrating (3.3) gives

\[
 \int_0^1E(y)\,dy
 \le\frac{e^2}{2c_\sharp}\varepsilon^{-1/2}E(0),
 \tag{4.1}
\]

and at the terminal time

\[
 E(1)
 \le e^2e^{-2c_\sharp\sqrt\varepsilon}E(0).
 \tag{4.2}
\]

These are both parts of the R0.72O hypothesis.  The terminal estimate cannot
be omitted when claiming that the full interface has been closed.

For the compact interval \(1\le\varepsilon\le\varepsilon_\sharp\),
skew-advection and diffusion give the exact contraction

\[
 E(y)\le E(0).
 \tag{4.3}
\]

Set \(c_{\rm ED}=2c_\sharp\).  Increasing the common energy prefactor by the
fixed amount

\[
 \max\left\{e^2,\frac{e^2}{2c_\sharp},
 \sqrt{\varepsilon_\sharp},
 e^{2c_\sharp\sqrt{\varepsilon_\sharp}}\right\}
 \tag{4.4}
\]

produces one constant \(C_{\rm ED}\) for (0.1) and (0.6) for every
\(\varepsilon\ge1\).  This compact-parameter completion is an exact energy
argument in this report, not part of the Coble--He theorem.

---

## 5. The full cross cubic and physical ledger

The R0.72O bound was already written before expanding carriers:

\[
 |hb|
 \le\rho(y)^2\|V(y)\|E(y)
 \le Ca^3BN e^{-3cy}E(y).
 \tag{5.1}
\]

For the present class, \(B=N=2\),

\[
 |\delta|\,dx=\frac{\varepsilon}{aB}\,dy,
 \qquad E(0)\asymp N
 \tag{5.2}
\]

for the amplitude-balanced launch and its bounded exact-root correction.
Using (4.1) in (5.1)--(5.2),

\[
 \mathcal C_\times
 \le C\varepsilon a^2N\int_0^1E(y)\,dy
 +C\varepsilon a^2NE(1)
 \lesssim a^2N^2\sqrt\varepsilon.
 \tag{5.3}
\]

The elementary inequality
\(\varepsilon e^{-c\sqrt\varepsilon}\lesssim\sqrt\varepsilon\) pays the
terminal term.  All self and mixed 1:2 interactions remain in (5.3).

The physical exponent transfer is unchanged from R0.72O:

\[
 \frac{\Theta(a^2N^2\sqrt\varepsilon)}{D^{1/3}}
 \asymp\varepsilon^{11/6}p^{4/3}.
 \tag{5.4}
\]

Dividing by the strong local action floor

\[
 Z\gtrsim
 \varepsilon^{4/3}p^2R^{2/3}L_{R,\varepsilon}
 \tag{5.5}
\]

gives

\[
 \frac{U_{\rm ED}}Z
 \lesssim
 \frac{\sqrt\varepsilon}
 {p^{2/3}R^{2/3}L_{R,\varepsilon}}.
 \tag{5.6}
\]

Equations (5.3)--(5.6) prove (0.7)--(0.9) unconditionally inside the
declared two-carrier class.

---

## 6. The exact Morse wall

The strict inequality \(|\lambda|<1/4\) is not merely a convenient
smallness choice.  The values \(\lambda=\pm1/4\) are the first time-slice
wall, over \(0\le y\le1\), at which the fixed two-critical-point geometry
can degenerate.

At \(y=0\),

\[
 W_\lambda(0,\phi)=\cos\phi+\lambda\cos2\phi.
 \tag{6.1}
\]

For \(\lambda=1/4\), the critical point \(\phi=\pi\) satisfies

\[
 W_\phi=W_{\phi\phi}=W_{\phi\phi\phi}=0,
 \qquad W_{\phi\phi\phi\phi}=3.
 \tag{6.2}
\]

For \(\lambda=-1/4\), the same identities hold at \(\phi=0\), with fourth
derivative \(-3\).  Hence the Morse margin vanishes exactly at
\(|\lambda|=1/4\).

If \(|\lambda|>1/4\), equation (2.2) has additional critical points at

\[
 \cos\phi=-\frac1{4\lambda}
 \tag{6.3}
\]

at \(y=0\).  At a general time slice the wall is
\(|\lambda|=e^{3y}/4\).  When the decaying relative coefficient crosses
\(1/4\), those critical points merge at \(0\) or \(\pi\).  The fixed-count,
fixed-radius shape package used above is then unavailable.

This proves a theorem-applicability wall for the 1:2 real-collinear-phase
class.  It
does not prove failure of enhanced dissipation beyond the wall; a degenerate
shear may have a different rate.

---

## 7. Exact and finite audit

The analytic proof is the result.  Two independent exact-arithmetic routes
audit:

1. the lattice-to-cell rescaling and \(\varepsilon\) coefficient;
2. the derivative factorization (2.2);
3. the rational shape constants in (2.7)--(2.8);
4. the slow-time threshold \(\eta\le1/16\);
5. the exact fourth-order degeneracy at \(|\lambda|=1/4\);
6. both the integrated and terminal clauses in the claim contract;
7. the inherited \(N=2\), \(p=2^{-1/2}\) exponent transfer.

The formal figure evaluates the exact cell profile, shape envelope, Morse
wall and physical exponent ledger.  It does not run a truncated PDE or fit a
decay exponent.  A future finite Fourier screen would be diagnostic only and
is not needed to establish (3.2) or the infinite-lattice theorem.

---

## 8. Literature boundary

Coble and He prove sharp enhanced dissipation for time-dependent
nondegenerate shears under shared critical points, uniform local and exterior
shape estimates, and a slowly varying reference shear.  Their Theorem 1.2
provides the semigroup estimate; their Appendix A makes the shape dependence
of the spectral constant and small-viscosity absorption visible.  The exact
cell reduction, the two-carrier factorization, the uniform family extraction,
and the physical cubic implication are project-specific corollaries.

Bedrossian--Coti Zelati and Coti Zelati--Gallay treat stationary shear
profiles and show that enhanced-dissipation constants and rates retain
profile-degeneracy information.  They support the shape boundary but do not
replace the time-dependent theorem used here.

The bounded search found no theorem that derives a uniform
full-superposition estimate from common-band support, carrier count, or
frequency spacing alone.  Results for a fixed spatial profile multiplied or
translated in time do not cover arbitrary changing Fourier superpositions.
This is a scope statement, not a claim of novelty or priority.

---

## 9. Claim boundary

R0.72P proves, for the declared real-collinear-phase 1:2 carrier class:

1. an exact reduction of the complete invariant lattice to one
   time-dependent shear equation;
2. a uniform two-critical-point shape theorem with explicit constants;
3. a family-uniform extraction of the Coble--He hypocoercive estimate;
4. both full-superposition estimates in (0.1);
5. the complete cross-cubic bound (0.7);
6. the inherited physical numerator and growing-geometry window (0.8)--(0.9);
7. the exact Morse wall \(|\lambda|=1/4\).

It does not prove:

1. uniform enhanced dissipation for arbitrary common-band phases or carrier
   patterns;
2. a theorem with growing \(N\);
3. enhanced dissipation beyond the 1:2 Morse wall;
4. a logarithmic one-carrier cubic estimate;
5. fixed-geometry arbitrary-coupling closure;
6. multiscale physical absorption;
7. a continuation criterion, finite-time singularity, or global smoothness
   theorem for general three-dimensional Navier--Stokes solutions.

The Clay Millennium problem remains open.

---

## 10. Next exact gate

R0.72Q should replace the special factorization (2.2) by a finite-pattern
jet condition.  One concrete target is a compact coefficient polytope for

\[
 W(y,\phi)=\sum_{m\in\mathcal M}c_m e^{-m^2y}\cos(m\phi)
 \tag{10.1}
\]

with a certified lower bound on the critical-point jet Gram determinant,
fixed critical count and separation, and uniform time variation.  A second
route is to prove the rowwise flux directly when critical points merge.

---

## Claim-to-source ledger

| Claim used here | Primary source | Exact role | Remaining limitation |
|---|---|---|---|
| Time-dependent nondegenerate shear gives \(e^{-c\eta^{1/2}|k|^{1/2}t}\) decay | D. Coble and S. He, Theorem 1.2, arXiv:2309.15738 / CMS 22 (2024) | Semigroup input after the exact cell reduction | The paper does not state this project's two-carrier corollary |
| Shape constants enter a spectral inequality through fixed critical neighborhoods and cutoffs | Coble--He, Appendix A, Lemma A.1 | Uniform-threshold extraction for the fixed \(\lambda\)-class | Requires the explicit fixed-cutoff argument written in Section 3 |
| Stationary enhanced-dissipation rate depends on profile degeneracy | M. Coti Zelati and T. Gallay, JLMS 108 (2023), Theorem 1.1 | Supports retaining a Morse/shape parameter | Stationary, not the time-dependent superposition here |
| Nondegenerate stationary shear hypocoercivity | J. Bedrossian and M. Coti Zelati, ARMA 224 (2017) | Source of the spectral/hypocoercive method reused by Coble--He | Fixed profile; no arbitrary common-band theorem |

## References used at this gate

1. D. Coble and S. He, *A Note on Enhanced Dissipation and Taylor
   Dispersion of Time-dependent Shear Flows*, arXiv:2309.15738; published
   as *A Note on Enhanced Dissipation of Time-Dependent Shear Flows*,
   *Communications in Mathematical Sciences* **22** (2024), 1663--1691,
   [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10).
2. J. Bedrossian and M. Coti Zelati, *Enhanced Dissipation,
   Hypoellipticity, and Anomalous Small Noise Inviscid Limits in Shear
   Flows*, *Archive for Rational Mechanics and Analysis* **224** (2017),
   1161--1204, [DOI](https://doi.org/10.1007/s00205-017-1099-y).
3. M. Coti Zelati and T. Gallay, *Enhanced Dissipation and Taylor
   Dispersion in Higher-dimensional Parallel Shear Flows*, *Journal of the
   London Mathematical Society* **108** (2023), 1358--1392,
   [DOI](https://doi.org/10.1112/jlms.12782).
