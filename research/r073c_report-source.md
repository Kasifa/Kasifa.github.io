# R0.73C report source: a certified frozen Rayleigh instability and the remaining viscous transfer gate

**Date:** 2026-08-30  
**Scope:** the fixed collision profile and the single row
\(\gamma=1/2\), not the nonlinear three-dimensional problem  
**Formal release state:** source draft until the certificate, independent
recomputation, figure, PDF, and public release gates all pass

## 0. Direct decision

R0.73C changes the large-\(|\Lambda|\) route in one important way.  The
collision profile is not merely non-normal: one fixed, nonzero Fourier row
has a genuine infinite-dimensional inviscid unstable eigenvalue.

The two closed statements are

\[
 \boxed{
  \gamma_0=\frac{\sqrt7}{2},\qquad
  0\in\sigma_p(A_{\gamma_0}(0)),
 }
 \tag{0.1}
\]

and

\[
 \boxed{
  \gamma_*=\frac12,\qquad
  \exists\,\sigma_*\in(0.17035,0.17050):
  \quad \sigma_*\in\sigma_p(A_{1/2}(0)).
 }
 \tag{0.2}
\]

Statement (0.2) is not a Fourier--Galerkin extrapolation.  It follows from a
validated interval integration of the periodic Rayleigh ODE and an exact
intermediate-value argument for the monodromy trace.  A separate finite
Fourier computation locates the same eigenvalue near
\(0.170407976920434\), but that floating-point computation is retained only
as a diagnostic crosscheck.

This release does **not** yet prove that the frozen inviscid eigenvalue
survives the singular vanishing-viscosity limit with the uniform Riesz and
complementary bounds needed on logarithmic fast time.  Accordingly,

```text
exactCubicNeutralSpectrum=CLOSED
infiniteDimensionalFrozenRayleighInstability=CLOSED
frozenInstabilityFastTimeTransfer=OPEN
superPolynomialCompleteRowNoGo=CONDITIONAL
sharpLargeLambdaGrowthLaw=OPEN
completeOSSquireA2DirectSum=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

## 1. Frozen operator and phase-speed convention

On \(\mathbb T_{2\pi}\), set

\[
 W_0(x)=-\frac12\sin x+\frac14\sin2x,
 \qquad L_\mu=-\partial_x^2+\mu,
 \qquad \mu=\gamma^2>0,
 \tag{1.1}
\]

and

\[
 A_\gamma(0)=-i\gamma
 \left(M_{W_0}+M_{W_0''}L_\mu^{-1}\right).
 \tag{1.2}
\]

If \(q=L_\mu\phi\), then

\[
 A_\gamma(0)q=\sigma q
 \tag{1.3}
\]

is equivalent to the periodic Rayleigh equation

\[
 (W_0-c)(\phi''-\gamma^2\phi)-W_0''\phi=0,
 \qquad \sigma=-i\gamma c.
 \tag{1.4}
\]

Thus \(c=i\eta\), \(\eta>0\), gives the real growing eigenvalue
\(\sigma=\gamma\eta>0\).  Since
\(M_{W_0''}L_\mu^{-1}\) is compact on \(L^2\), the essential spectrum is
the imaginary segment \(-i\gamma\operatorname{Ran}W_0\).  Any eigenvalue
with positive real part therefore lies outside the essential spectrum and is
isolated with finite algebraic multiplicity.

## 2. The cubic neutral level is an exact singular theorem

Factorization gives

\[
 W_0=-2\sin^3\frac x2\cos\frac x2,
 \qquad
 \frac{W_0''}{W_0}
 =-4+\frac{3}{2\sin^2(x/2)}.
 \tag{2.1}
\]

On \(0<x<2\pi\), let \(\phi_0=\sin^3(x/2)\), and interpret it on the
torus by its periodic extension \(|\sin(x/2)|^3\).  This extension is
\(C^2\cap H^2_{\rm per}\), though not \(C^3\) at the joined cubic level.
Direct differentiation gives

\[
 \left(-\partial_x^2+\frac{W_0''}{W_0}\right)\phi_0
 =-\frac74\phi_0.
 \tag{2.2}
\]

With \(q_0=L_{7/4}\phi_0\ne0\), equation (2.2) implies

\[
 W_0q_0+W_0''\phi_0=0,
 \qquad A_{\sqrt7/2}(0)q_0=0.
 \tag{2.3}
\]

There is no endpoint delta mass because \(\phi_0'\) matches across the
periodic join.

The complete singular threshold count is also explicit.  Put \(t=x/2\).
The Friedrichs realization satisfies

\[
 4H_0=-\partial_t^2+6\csc^2t-16,
 \qquad 0<t<\pi.
 \tag{2.4}
\]

Both endpoints are limit point because the inverse-square coefficient is
\(6>3/4\).  The Gegenbauer eigenfunctions give

\[
 \sigma(H_0)
 =\left\{\frac{(n+3)^2-16}{4}:n=0,1,\ldots\right\}
 =\left\{-\frac74,0,\frac94,5,\ldots\right\}.
 \tag{2.5}
\]

Hence \(-7/4\) is the unique negative singular threshold eigenvalue.  This
closes C3, but the neutral eigenvalue is embedded in the inviscid essential
spectrum; ordinary isolated-eigenvalue perturbation at \(c=0\) is not
available.

## 3. Why a classical instability citation is insufficient here

Near the cubic zero,

\[
 W_0(x)=-\frac{x^3}{4}+O(x^5),
 \qquad
 -\frac{W_0''}{W_0}=-\frac6{x^2}+O(1).
 \tag{3.1}
\]

The potential is unbounded and not locally integrable.  The regular
Tollmien--Lin continuation theorem for bounded odd shear profiles therefore
cannot simply be quoted.  Zhiwu Lin's original theorem proves growing modes
for broad classes of ideal plane flows, but its hypotheses must still be
checked for the profile at hand; the cubic zero falls outside the regular
route used there.  Recent work on degenerate critical layers explains the
singular structure, but does not supply the exact periodic branch theorem
needed here.

This is why R0.73C uses the nonsingular line \(c=i\eta\), \(\eta>0\), and
certifies a sign change directly.  The literature boundary is documented in
`research/r073c_literature_audit.md`.

## 4. Exact monodromy reduction at \(\gamma=1/2\)

For \(\eta>0\), write

\[
 Q_\eta(x)=\frac14+\frac{W_0''(x)}{W_0(x)-i\eta},
 \qquad
 \phi''=Q_\eta\phi.
 \tag{4.1}
\]

The coefficient is smooth and periodic because
\(|W_0-i\eta|\ge\eta\).  Let \(Y_\eta(0)=I_2\) be the fundamental matrix
and \(M(\eta)=Y_\eta(2\pi)\) its monodromy matrix.  Absence of a
\(\phi'\) term gives

\[
 \det M(\eta)=1.
 \tag{4.2}
\]

The profile symmetry

\[
 W_0(2\pi-x)=-W_0(x),
 \qquad W_0''(2\pi-x)=-W_0''(x)
 \tag{4.3}
\]

implies \(Q_\eta(2\pi-x)=\overline{Q_\eta(x)}\).  With
\(S=\operatorname{diag}(1,-1)\), reflection and conjugation of the
fundamental system yield

\[
 S=M(\eta)S\overline{M(\eta)},
 \qquad
 M(\eta)^{-1}=S\overline{M(\eta)}S.
 \tag{4.4}
\]

For a two-by-two determinant-one matrix,
\(\operatorname{tr}M^{-1}=\operatorname{tr}M\).  Taking traces in (4.4)
therefore proves

\[
 F(\eta):=\operatorname{tr}M(\eta)-2\in\mathbb R.
 \tag{4.5}
\]

Moreover,

\[
 \det(M-I)=1-\operatorname{tr}M+\det M=2-\operatorname{tr}M.
 \tag{4.6}
\]

Hence the Rayleigh problem has a nonzero periodic solution if and only if
\(F(\eta)=0\).  Standard continuous dependence for smooth ODE coefficients
makes \(F\) continuous on every compact subinterval of \((0,\infty)\).

## 5. Validated interval theorem

The proof program evolves a twelve-dimensional real autonomous system:

1. \(\sin x,\cos x,\sin2x,\cos2x\);
2. the real and imaginary parts of both columns of \(Y_\eta\) and their
   derivatives.

No trigonometric function is numerically evaluated after launch.  Every
right-hand-side operation is addition, subtraction, multiplication, or
division by

\[
 W_0^2+\eta^2\ge\eta^2>0.
 \tag{5.1}
\]

For each step \([0,h]\), the code first constructs a rectangular interval
box \(Z\) and verifies the Picard inclusion

\[
 y_0+[0,h]f(Z)\subseteq Z.
 \tag{5.2}
\]

Local Lipschitz continuity then places the exact solution inside \(Z\) for
the entire step.  Formal power-series recursion computes the normalized
derivatives \(y^{(k)}/k!\).  The endpoint enclosure is

\[
 y(h)\in
 \sum_{k=0}^{p-1}\frac{y^{(k)}(0)}{k!}h^k
 +h^p\left\{\frac{y^{(p)}(z)}{p!}:z\in Z\right\},
 \tag{5.3}
\]

with the last set evaluated by interval arithmetic.  This is the ordinary
Taylor theorem with an interval Lagrange remainder; it is not a floating
error estimate fitted after the computation.

The pinned arithmetic engine is `mpmath==1.3.0`.  Only its basic interval
operations and `iv.pi` are used.  Those source operations evaluate lower
endpoints with floor rounding and upper endpoints with ceiling rounding.  The
certificate stores the exact binary endpoint tuples, so the formal sign does
not depend on decimal formatting.

Two different partitions and Taylor orders give the same strict signs:

| run | steps | order | decimal precision | \(F(0.3407)\) | \(F(0.3410)\) |
|---|---:|---:|---:|---:|---:|
| A | 1024 | 10 | 40 | strictly negative | strictly positive |
| B | 768 | 12 | 55 | strictly negative | strictly positive |

The formal endpoint intervals are read from the generated certificate rather
than copied by hand.  Since the signs are strict and \(F\) is continuous,
there exists

\[
 \eta_*\in(0.3407,0.3410)
 \quad\text{with}\quad F(\eta_*)=0.
 \tag{5.4}
\]

Equations (1.4) and (4.6) then give a smooth periodic Rayleigh eigenfunction
and

\[
 \sigma_*=\frac12\eta_*
 \in(0.17035,0.17050).
 \tag{5.5}
\]

This closes C4 as an infinite-dimensional theorem.  It does not locate a
unique root, classify every \(0<\gamma<\sqrt7/2\), or prove the viscous
transfer.

## 6. Independent finite diagnostic

A separately written Fourier--Galerkin matrix at \(\gamma=1/2\) gives

\[
 \sigma_N=
 \begin{cases}
  0.1704079769\ldots,&N=32,\\
  0.1704079769\ldots,&N=48,\\
  0.1704079769\ldots,&N=64,\\
  0.1704079769\ldots,&N=96,\\
  0.1704079769\ldots,&N=128.
 \end{cases}
 \tag{6.1}
\]

It lies inside (5.5).  This agreement is useful for falsification and figure
construction, but it is not part of the proof of (0.2): ordinary cutoff
convergence has no certified tail bound.

## 7. The C5 correction: why C4 is not yet a large-coupling theorem

Put \(\varepsilon=|\Lambda|^{-1}\) and rescale
\(\theta=|\Lambda|d\).  The exact nonautonomous generator is

\[
 B_{\varepsilon,s}(d)
 =sA_{1/2}(d)-\varepsilon L_{1/4},
 \qquad s=\operatorname{sgn}\Lambda.
 \tag{7.1}
\]

In the physical kinetic space, \(-\varepsilon L_{1/4}\) is an unbounded
sectorial generator for every \(\varepsilon>0\).  It cannot be inserted into
a bounded-operator Duhamel estimate merely because its scalar coefficient is
small.  The missing theorem must establish, uniformly as
\(\varepsilon\downarrow0\),

1. persistence of a viscous unstable eigenvalue of \(B_{\varepsilon,s}(0)\);
2. a common Riesz contour and bounded spectral projections along the moving
   profile;
3. a complementary exponential dichotomy;
4. graph-domain compatibility for the Kato transport.

Under those explicit hypotheses, the conditional logarithmic-time lemma
gives, for each fixed \(M>0\),

\[
 \|U_{\varepsilon,s}(M\log(1/\varepsilon),0)
 q_{\varepsilon,s}\|_{\mathcal K_{1/4}}
 \ge c_M\varepsilon^{-M\sigma_*+o_M(1)}.
 \tag{7.2}
\]

If the package holds for every sufficiently small \(\varepsilon\), then every
fixed-degree complete-row polynomial upper bound fails on this row.  Without
that package, the implication remains CONDITIONAL.  This correction is a
positive research result: it replaces a plausible but invalid bounded
perturbation step with the exact theorem that must be proved next.

## 8. Value and boundary

The main value of R0.73C is structural.

- It proves that the gap between the R0.73B linear lower bound and exponential
  upper bound cannot be studied as a purely non-normal transient problem.
- It identifies a concrete inviscid unstable row with a certified growth-rate
  bracket, giving the next viscous analysis a fixed target rather than a
  numerical conjecture.
- It exposes the true obstruction: uniform vanishing-viscosity spectral
  persistence and dichotomy, not the existence of a frozen Rayleigh mode.

The result is still far from the Clay problem.  It concerns one linearized
two-dimensional row at one frozen profile.  It proves neither the complete
Orr--Sommerfeld--Squire direct sum, nonlinear frequency closure, a priori
three-dimensional regularity, nor blowup.  No statement in this release may
be advertised as resolving the Millennium problem.

## 9. Next gate

R0.73D should freeze a vanishing-viscosity Evans/Riesz problem for

\[
 B_{\varepsilon,+}(0)=A_{1/2}(0)-\varepsilon L_{1/4}.
 \tag{9.1}
\]

The first target is deliberately narrower than the full time-dependent
transfer:

\[
 \exists\lambda_\varepsilon\in\sigma_p(B_{\varepsilon,+}(0)):
 \quad
 \lambda_\varepsilon\to\sigma_*,
 \qquad
 \sup_{0<\varepsilon\le\varepsilon_0}
 \|P_\varepsilon\|<\infty.
 \tag{9.2}
\]

Only after (9.2) and a uniform complementary resolvent are closed should the
profile-motion/Kato transport lemma be promoted from CONDITIONAL to CLOSED.

## 10. Primary sources and arithmetic record

- Z. Lin, [*Instability of Some Ideal Plane Flows*](https://doi.org/10.1137/S0036141002406266), SIAM J. Math. Anal. 35 (2003), 318--356.
- D. Bian and E. Grenier, [*Singularities of Rayleigh equation*](https://arxiv.org/abs/2408.00977), arXiv:2408.00977.
- Z. Lin and C. Zeng, [*Instability, index theorem, and exponential trichotomy for Linear Hamiltonian PDEs*](https://arxiv.org/abs/1703.04016), arXiv:1703.04016.
- Z. Lin and M. Xu, [*Metastability of Kolmogorov flows and inviscid damping of shear flows*](https://arxiv.org/abs/1707.00278), arXiv:1707.00278.
- mpmath 1.3.0, [interval-context documentation](https://mpmath.org/doc/current/contexts.html) and [pinned directed-rounding source](https://github.com/mpmath/mpmath/blob/1.3.0/mpmath/libmp/libmpi.py).

