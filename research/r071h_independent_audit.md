# R0.71H independent audit — projective heat curvature

**Date:** 2026-08-25

**Status:** **PASS for the unit-direction identity on each component of
\(\{d>0\}\); NO clean denominator substitution for \(d+\varepsilon\).**

This is an internal audit of the derivation in
`research/r071h_report-source.md`.  It does not check a
Leray-level bound for the source ratio, does not prove regularity, and makes
no originality claim.

## 1. Assumptions needed for the algebra

Let \(\mathcal H\) be a real Hilbert space and let \(A\) be a fixed
self-adjoint nonnegative operator.  The finite-dimensional calculation only
needs \(C\in C^1\).  A safe sufficient assumption for an unbounded operator
is

\[
 C\in C^1(J;D(A))
 \tag{1.1}
\]

in the graph norm, together with

\[
 C_t=-\nu AC+G,\qquad \nu>0.
 \tag{1.2}
\]

These assumptions are stronger than necessary, but they justify every
chain rule below without a form-domain qualification.  They hold for the
classical smooth periodic setting stated in the scratch derivation.  They
are not automatic for a general Leray--Hopf solution.

Because \(d(t)=\|C(t)\|^2\) is continuous, \(\{d>0\}\) is open.  Fix one
connected component \(J\) of this set and write

\[
 \rho=\sqrt d,\qquad E=C/\rho,\qquad \|E\|=1,
 \qquad P=I-E\otimes E.
 \tag{1.3}
\]

The pointwise identity is valid on \(J\).  Its integrated form is automatic
on compact subintervals \([t_0,t_1]\Subset J\).  Extending it to a boundary
where \(d\to0\), or summing it over all components, requires the internal
time faces and the relevant limits; those limits are not supplied by the
identity.

## 2. Direct derivation in a Hilbert space

Since the scalar \(\rho(t)\) commutes with \(A\), differentiation of the
unit vector gives

\[
 E_t=\frac{PC_t}{\rho}
 =-\nu PAE+\rho^{-1}PG.
 \tag{2.1}
\]

Set

\[
 r=\langle AE,E\rangle,qquad
 X=PAE,qquad H=\rho^{-1}PG.
 \tag{2.2}
\]

Self-adjointness and \(E_t\perp E\) imply

\[
 \begin{aligned}
 r_t
 &=2\langle AE,E_t\rangle
 =2\langle X,-\nu X+H\rangle\\
 &=-2\nu\|X\|^2+2\langle X,H\rangle.
 \end{aligned}
 \tag{2.3}
\]

There is no missing factor of two.  Expanding
\(\|E_t\|^2=\|-\nu X+H\|^2\) gives

\[
 \boxed{
 \|E_t\|^2+\nu^2\|X\|^2
 =-\nu r_t+\|H\|^2.}
 \tag{2.4}
\]

Both sides are exactly

\[
 2\nu^2\|X\|^2-2\nu\langle X,H\rangle+\|H\|^2.
 \tag{2.5}
\]

Integration yields

\[
 \int_{t_0}^{t_1}\!\bigl(\|E_t\|^2+\nu^2\|X\|^2\bigr)\,dt
 =\nu\,[r(t_0)-r(t_1)]
 +\int_{t_0}^{t_1}\!\frac{\|PG\|^2}{d}\,dt.
 \tag{2.6}
\]

Thus the signs and coefficients in equations (2.2)--(2.5) of the candidate
scratch derivation are correct.  Nonnegativity of \(A\) is used to regard
\(r\) as a nonnegative Rayleigh quotient; self-adjointness is the property
needed for the displayed differentiation.

## 3. Forced finite-dimensional check

The independent program uses the non-diagonal positive matrix

\[
 A=
 \begin{pmatrix}
 1.25&0.10&0.25\\
 0.10&2.21&-0.28\\
 0.25&-0.28&0.86
 \end{pmatrix}=M^TM.
 \tag{3.1}
\]

Its leading principal minors are

\[
 1.25,\qquad 2.7525,\qquad 2.117025,
 \tag{3.2}
\]

so it is symmetric positive definite.  A three-component analytic path
bounded away from zero is prescribed, and the source is independently
formed as \(G=C_t+\nu AC\).  Seventy-one time samples check (2.1), (2.3),
and (2.4); Simpson quadrature checks (2.6).

The largest recorded residuals were

| Check | Residual |
|---|---:|
| direction equation | \(1.60\times10^{-16}\) |
| Rayleigh derivative | \(1.35\times10^{-16}\) |
| pointwise identity | \(8.33\times10^{-17}\) |
| integrated identity | \(1.94\times10^{-16}\) |

The minimum sampled denominator was \(d=2.1385687032\).  This test does not
probe a zero face; that issue is treated separately below.

## 4. Fourier heat-flow check

Take orthonormal Fourier modes with wave vectors

\[
 (1,0,0),\quad(1,1,0),\quad(2,1,0),\quad(3,0,0),
\]

so that the eigenvalues of \(A=-\Delta\) are
\(\mu=(1,2,5,9)\).  For

\[
 C(t)=\sum_k a_ke^{-\nu\mu_kt}\phi_k,
 \qquad G=0,
 \tag{4.1}
\]

define the normalized spectral weights

\[
 p_k(t)=\frac{|a_k|^2e^{-2\nu\mu_kt}}{\|C(t)\|^2}.
 \tag{4.2}
\]

Then Parseval's identity gives the exact formulas

\[
 r=\sum_kp_k\mu_k,qquad
 \|X\|^2=\sum_kp_k(\mu_k-r)^2=\operatorname{Var}_p(\mu),
 \tag{4.3}
\]

and hence

\[
 r_t=-2\nu\operatorname{Var}_p(\mu),qquad
 \|E_t\|^2=\nu^2\operatorname{Var}_p(\mu).
 \tag{4.4}
\]

Therefore both sides of (2.4) equal
\(2\nu^2\operatorname{Var}_p(\mu)\).  This also proves that the Rayleigh
quotient is nonincreasing for pure heat flow; it is constant exactly when
the normalized state lies in one eigenspace.

The independent Fourier run used \(a=(1,-0.7,0.4,0.2)\).  Across 71 samples,
the largest pointwise identity residual was
\(2.22\times10^{-16}\), the spectral-variance residual was
\(8.88\times10^{-16}\), and the integrated residual was
\(2.00\times10^{-15}\).  The largest sampled value of \(r_t\) was
\(-0.0409442\), so the monotonicity sign was also checked away from a single
eigenmode.

## 5. Why \(d+\varepsilon\) does not preserve the clean identity

The regularization in R0.71G is
\((B^+)^2/(d+\varepsilon)\).  It should not be interpreted as replacing the
unit direction by another unit vector.  Indeed, define

\[
 R_\varepsilon=(d+\varepsilon)^{1/2},\qquad
 Z=C/R_\varepsilon,qquad
 m=\|Z\|^2=\frac d{d+\varepsilon}.
 \tag{5.1}
\]

Except in the limit \(\varepsilon/d\to0\), \(Z\) is not a unit vector.  The
operator

\[
 Q=I-Z\otimes Z
 \tag{5.2}
\]

is symmetric but is generally not an orthogonal projection.  Direct
differentiation gives

\[
 Z_t=Q\left(-\nu AZ+\frac{G}{R_\varepsilon}\right)
 =-\nu X_\varepsilon+H_\varepsilon,
 \tag{5.3}
\]

where

\[
 X_\varepsilon=QAZ,qquad
 H_\varepsilon=Q(G/R_\varepsilon),qquad
 r_\varepsilon=\langle AZ,Z\rangle.
 \tag{5.4}
\]

Because \(Z_t\) is not tangent to a unit sphere,

\[
 (r_\varepsilon)_t
 =2\langle X_\varepsilon,Z_t\rangle
 +2r_\varepsilon\langle Z,Z_t\rangle.
 \tag{5.5}
\]

The exact soft-denominator identity is therefore

\[
 \boxed{
 \begin{aligned}
 \|Z_t\|^2+\nu^2\|X_\varepsilon\|^2
 ={}&-\nu(r_\varepsilon)_t+\|H_\varepsilon\|^2\\
 &+\nu r_\varepsilon m_t,
 \end{aligned}}
 \tag{5.6}
\]

with

\[
 m_t=2\langle Z,Z_t\rangle
 =\frac{\varepsilon d_t}{(d+\varepsilon)^2}.
 \tag{5.7}
\]

The last term is the exact defect in this formulation.  It has no fixed
sign because \(d_t\) has no fixed sign.  Omitting it is incorrect.

There is a second, genuinely orthogonal formulation on \(d>0\).  Put
\(e=C/\sqrt d\), \(P_e=I-e\otimes e\), and
\(r=\langle Ae,e\rangle\).  Since \(Z=\sqrt m\,e\),

\[
 \begin{aligned}
 &\|P_eZ_t\|^2+\nu^2\|P_eAZ\|^2\\
 &\quad=-\nu(r_\varepsilon)_t
 +\frac{\|P_eG\|^2}{d+\varepsilon}
 +\nu m_t r.
 \end{aligned}
 \tag{5.8}
\]

If the full soft speed \(\|Z_t\|^2\) is used instead of its tangent part,
the additional nonnegative radial term is

\[
 \frac{m_t^2}{4m}.
 \tag{5.9}
\]

Equations (5.8)--(5.9) still use \(e\) and therefore do not cross a zero of
\(d\).  Equation (5.6) is algebraically defined at \(d=0\), but its \(Q\)
is not the projective tangent map and its source contains
\(G/\sqrt{d+\varepsilon}\).  Neither formulation is the clean unit-sphere
identity with \(d\) merely replaced by \(d+\varepsilon\).

The program checked (5.6), (5.8), and (5.9).  For the forced
three-dimensional path, the largest corrected residual was
\(8.33\times10^{-17}\), while omitting the defect produced a residual as
large as \(1.23\times10^{-2}\).  A one-dimensional unforced heat example
gave

\[
 \text{left side}=0.1912867,\qquad
 \text{clean right side}=0.5560764,
 \tag{5.10}
\]

with the exact \(Q\)-form defect \(-0.3647896\).  Thus even the simplest
pure heat flow disproves the naive soft-denominator substitution.  A
separate linear crossing \(C(t)=(t,0)\) checked (5.6) at \(d=0\); the
identity remains algebraically true there.  Taking \(A=0\) and
\(G=(1,0)\), however, gives the exact squared source

\[
 \|H_\varepsilon(t)\|^2
 =\frac{\varepsilon^2}{(t^2+\varepsilon)^3},
 \qquad
 \int_{\mathbb R}\|H_\varepsilon(t)\|^2dt
 =\frac{3\pi}{8\sqrt\varepsilon}.
 \tag{5.11}
\]

Thus the soft identity has no source estimate uniform in
\(\varepsilon\downarrow0\), even for this elementary crossing.

## 6. Scaling check

For the whole-space three-dimensional Navier--Stokes scaling, with cutoffs,
heat heights, and multipliers scaled covariantly,

\[
 C_\lambda(t,x)=\lambda^3C(\lambda^2t,\lambda x),
 \qquad d_\lambda(t)=\lambda^3d(\lambda^2t).
 \tag{6.1}
\]

Consequently

\[
 E_\lambda=\lambda^{3/2}E(\lambda^2t,\lambda x),
 \quad r_\lambda=\lambda^2r,
 \quad\|(E_\lambda)_t\|_2=\lambda^2\|E_t\|_2,
 \quad\|H_\lambda\|_2=\lambda^2\|H\|_2.
 \tag{6.2}
\]

Each pointwise term in (2.4) scales as \(\lambda^4\), and each integrated
term in (2.6) scales as \(\lambda^2\).  Therefore

\[
 K^{-2}\int\|E_t\|_2^2dt,qquad
 K^{-2}\int\frac{\|PG\|_2^2}{d}\,dt,qquad
 \int\|E_t\|_2dt
 \tag{6.3}
\]

are scale invariant.  This confirms the scaling ledger in the candidate
scratch file.  It neither proves nor refutes a critical estimate.

For the soft denominator to transform covariantly, its parameter must scale
as

\[
 \varepsilon_\lambda=\lambda^3\varepsilon,
 \tag{6.4}
\]

the same way as \(d\).  Holding a numerical \(\varepsilon\) fixed breaks
the scaling.  On a fixed torus, arbitrary whole-space rescaling is not an
internal symmetry; the ledger is a whole-space or covariantly resized-domain
calculation.

## 7. Reproduction and decision

Run the standard-library checker from the repository root:

```bash
python3 research/r071h_independent_audit.py
```

The run exits with status zero and prints `"status": "PASS"`.

The independent decision is:

1. The unit-direction evolution, Rayleigh derivative, pointwise identity,
   integrated identity, pure-heat sign, and scaling in the R0.71H candidate
   are correct under the stated classical regularity and on each component
   of \(\{d>0\}\).
2. The result isolates a source ratio but supplies no estimate for it.  It
   also supplies no summation over shells, cells, or zero-denominator faces.
3. The \(q_\varepsilon\) quotient remains a valid separate ledger, but it
   does not inherit the clean projective-curvature identity by replacing
   \(d\) with \(d+\varepsilon\).  The exact radial defects (5.6)--(5.9) must
   be retained.
4. Nothing in this audit is a regularity theorem, a singularity result, or
   an originality determination.
