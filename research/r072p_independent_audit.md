# R0.72P independent analytic audit

**Date:** 2026-08-27

**Status:** PASS after the theorem explicitly fixes \(B=2\),
\(0<\lambda_-\le|\lambda|\le1/8\), and the affine invariant frequency row.

## Independent mathematical decision

The audit rebuilt the reduction rather than reading a numerical certificate
as proof.  On

\[
 \Lambda_{R,q_*}=\{(nR,q_*):n\in\mathbb Z\},
\]

put \(y=R^2x\), \(\varepsilon=2|\delta|a/R^2\), and
\(\mu=|q_*|^2/R^2\).  Each modal coefficient is
\(\varepsilon/B=\varepsilon/2\), while each pair of signed shifts gives a
factor \(2\cos(m\phi)\).  The full, unexpanded lattice therefore gives

\[
 \partial_yF=\partial_\phi^2F-\mu F
 -is\varepsilon W(y,\phi)F,
 \qquad
 W=e^{-y}\cos\phi+\lambda e^{-4y}\cos2\phi.
\]

Removing the nonnegative common damping can only enlarge the norm.  With
\(t=\varepsilon y\) and \(\eta=\varepsilon^{-1}\), the undamped conjugate is
exactly the \(k=1\) Coble--He mode with actual shear \(V=sW\).  Equivalently,
one may use \(k=s\) and \(V=W\); in either convention \(kV=sW\).

The independent derivative calculation gives

\[
 W_\phi=-e^{-y}\sin\phi
 (1+4\lambda e^{-3y}\cos\phi).
\]

For \(|\lambda|\le1/8\), the parenthesis belongs to \([1/2,3/2]\), so the
critical set is exactly \(\{0,\pi\}\) for every \(0\le y\le1\).  At radius
\(r=\pi/4\), the bounds \(e^{-y}\ge1/3\),
\(|\sin d|\ge d/2\) near the critical set, and
\(|\sin\phi|\ge\sqrt2/2\) outside verify the safe uniform choices
\(\mathfrak C_0=144\) and \(\mathfrak C_1=12\).  The derivative norms in
the report are valid.  Taking \(U=V=sW\) makes the phase condition the
identity \(U_\phi V_\phi=|W_\phi|^2\), and

\[
 \|\partial_{t\phi}W(\eta t)\|_\infty
 \le2\eta\le\eta^{3/4}
\]

for \(\eta\le1/16\).

Let \(\eta_0^{\rm CH}\) denote the uniform proof threshold obtained from
the fixed shape, cutoff and norm data in Coble--He, and set
\(\eta_\sharp=\min\{1/16,\eta_0^{\rm CH}\}\).  The theorem supplies the
uniform norm decay for \(\varepsilon\ge\eta_\sharp^{-1}\).  On the
complementary compact interval, exact \(L^2\) contraction and one enlarged
prefactor give the same exponential form.  Squaring and integrating yields
both

\[
 \int_0^1E(y)\,dy\le C_{\rm ED}\varepsilon^{-1/2}E(0),
 \qquad
 E(1)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon}E(0)
\]

with constants uniform in \(R,\varepsilon,\lambda\) and the initial datum.
Density plus contraction includes arbitrary \(L^2\) data on the row and the
exact-root correction.  Combining this result with the R0.72O operator
inequality retains all self and cross terms and proves
\(\mathcal C_\times\lesssim a^2N^2\sqrt\varepsilon\) for \(N=B=2\).

At \(\lambda=-1/4\), \((y,\phi)=(0,0)\) has vanishing first three
\(\phi\)-derivatives and fourth derivative \(-3\).  At \(\lambda=1/4\),
the same occurs at \((0,\pi)\) with fourth derivative \(3\).  The general
time-slice wall is \(|\lambda|=e^{3y}/4\).  This is a sharp failure of this
Morse certificate, not a counterexample to enhanced dissipation.

**Decision:** no further analytic blocker remains for the declared positive
two-carrier class.  Arbitrary phases, other residue geometries without the
orthogonality reduction, growing carrier count, multiscale absorption and
general three-dimensional Navier--Stokes regularity remain open.

## Checklist

The audit must rebuild the following points without treating the finite
certificate as the proof.

1. Verify that the \(R,2R\) shifts preserve the affine row and that the
   exact rescaling gives (1.5), including the factor
   \(\varepsilon=2|\delta|a/R^2\).
2. Verify that removing the target diffusion multiplies the solution by a
   decaying scalar in the original variables and cannot weaken the desired
   upper estimate.
3. Differentiate the full shear and verify the factorization (2.2).
4. Prove that \(|\lambda|\le1/8\) gives exactly two fixed critical points
   and check \((r,\mathfrak C_0,\mathfrak C_1)=(\pi/4,144,12)\).
5. Verify every derivative bound in (2.8) and the slow-time calculation
   \(2\eta\le\eta^{3/4}\) for \(\eta\le1/16\); keep this distinct from the
   Coble--He proof threshold.
6. Inspect Coble--He Appendix A and Section 3 to ensure that fixed cutoffs
   and the displayed shape data really give a family-uniform threshold.
7. Derive both energy clauses from the norm decay and separately check the
   compact-\(\varepsilon\) completion.
8. Check that the R0.72O cross-term inequality is applied before carrier
   expansion and therefore keeps every mixed term.
9. Recompute the \(N=2,p=2^{-1/2}\) physical exponent transfer.
10. Verify the fourth-order degeneracy at \(\lambda=\pm1/4\) and keep the
    conclusion at the level of a Morse/applicability wall.
11. Preserve arbitrary common-band families, growing \(N\), fixed-geometry
    arbitrary coupling, and general 3D regularity as open.
