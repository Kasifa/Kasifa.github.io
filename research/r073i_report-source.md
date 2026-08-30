# R0.73I report source: endpoint correction, a continuum upper action, and the fixed-window inference barrier

**Date:** 2026-08-30  
**Scope:** the exact periodic planar row
\((\beta,\xi,\gamma)=(0,0,1/2)\), the heat-evolving two-harmonic shear,
and the selected-gain question left by R0.73H  
**Evidence classes:** exact operator theorem, exact logical
counterexamples, and separately labelled finite Fourier--Galerkin
diagnostics

## 0. Direct decision

R0.73I asked whether the selected gain used in R0.73H already has a
reproducible matching action.  The answer from the inherited R0.73F--H
inputs is negative, but the audit produces three exact positive results.

First, R0.73H's endpoint is not \(1/450\).  Every endpoint created by the
R0.73F proof obeys

\[
 \boxed{
 D=d_0<\frac{\sqrt{19/180}}{392}
 \approx8.2880904293\times10^{-4}<\frac1{450}.}
 \tag{0.1}
\]

The proof still permits \(d_0\) to be shrunk, so (0.1) is not a canonical
numerical endpoint.

Second, the full moving evolution has the exact continuum upper bound

\[
 \boxed{
 \|U_\varepsilon(D/\varepsilon,0)\|
 \le \exp\!\left(\frac{\Omega_H(D)}{\varepsilon}-\frac D4\right),}
 \qquad 0\le D\le\frac1{450},
 \tag{0.2}
\]

where

\[
 \boxed{
 \Omega_H(D)=\frac8{405}\left[
 \left(\frac{19}{20}+\frac{45D}{4}\right)^{3/2}
 -\left(\frac{19}{20}\right)^{3/2}
 \right].}
 \tag{0.3}
\]

Third, although no fixed-window action follows, the complete frozen top
block has a matching tangent rate at the zero window.  If
\(m_\varepsilon(D)\) and \(M_\varepsilon(D)\) are its minimum and maximum
moving gains, then all four iterated liminf/limsup rates satisfy

\[
 \boxed{
 \lim_{D\downarrow0}
 \left(\liminf_{\varepsilon\downarrow0}
 \frac{\varepsilon}{D}\log m_\varepsilon(D)\right)
 =
 \lim_{D\downarrow0}
 \left(\limsup_{\varepsilon\downarrow0}
 \frac{\varepsilon}{D}\log M_\varepsilon(D)\right)
 =a,}
 \tag{0.4}
\]

and the two omitted limsup/liminf combinations equal the same \(a\).  Here
\(a\) is the spectral abscissa of \(\widetilde A(0)\).  The order
\(\varepsilon\downarrow0\) first, \(D\downarrow0\) second is part of the
theorem.

The fixed positive window remains open.  The inherited launch need not be
canonical, the top block is not proved rank one, and the chosen \(d_0\) is
not unique.  Exact finite-dimensional counterexamples show that inputs of
this strength can permit different actions for different allowed launches
and can permit a polynomial prefactor even when the exponential action
exists.  Thus

```text
inheritedEndpointStrictlyBelowOneOver450=CLOSED
improvedContinuumUpperAction=CLOSED
zeroWindowTangentAction=CLOSED
fixedWindowActionFromInheritedInputs=FALSE_AS_INFERENCE
actionLimitAloneGivesBoundedPrefactor=FALSE_AS_INFERENCE
canonicalSelectedBranch=OPEN
matchingSelectedGainAction=OPEN
prescribedActionSeedDeparture=OPEN
fixedBackgroundLyapunovInstability=OPEN
transverseThreeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

The negative line concerns what follows from the inherited hypotheses.  It
does not say that the exact PDE gain lacks a matching action.

## 1. Operator and gain notation

Put

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad
 L=-\partial_x^2+\frac14,
 \tag{1.1}
\]

and work in the kinetic \(L^2\) representation

\[
 B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad \varepsilon=\Lambda^{-1}.
 \tag{1.2}
\]

The fast-time equation is

\[
 \partial_\theta v=B_\varepsilon(\varepsilon\theta)v,
 \qquad 0\le\theta\le D/\varepsilon.
 \tag{1.3}
\]

R0.73H used a normalized frozen top eigenvector \(\phi_\Lambda\) and

\[
 G_\Lambda(D)=\|U_{1/\Lambda}(\Lambda D,0)\phi_\Lambda\|_2,
 \qquad D=\min\{d_0,1/450\}.
 \tag{1.4}
\]

The analytic record did not prove that the complete top subspace is rank
one or specify a tie rule if it is not.  It also did not make the shrinkable
constant \(d_0\) numerical.  Both choices matter before a selected action
can be called reproducible.

## 2. Exact audit of the inherited endpoint

R0.73F chooses

\[
 0<b<\alpha<c_F<a,
 \qquad
 \nu=\min\{\alpha-b,c_F-\alpha\},
 \qquad K\ge1,
 \tag{2.1}
\]

and requires

\[
 C_A d_0<\frac{\nu}{16K^2},
 \qquad C_A=\frac{49}{4}.
 \tag{2.2}
\]

Since the two gaps defining \(\nu\) have sum \(c_F-b<a\),

\[
 \nu<\frac a2.
 \tag{2.3}
\]

The R0.73H coercivity certificate, transferred to \(\gamma=1/2\) in
Section 3 below, gives

\[
 a\le\omega(\widetilde A(0))
 \le\sqrt{\frac{19}{180}}.
 \tag{2.4}
\]

Equations (2.2)--(2.4) and \(K\ge1\) yield (0.1).  Thus
\(D=\min\{d_0,1/450\}=d_0\) strictly.  This also resolves the apparent
tension between the R0.73F rate \(r>0.17035\) and a finite diagnostic at
\(D=1/450\): that finite endpoint lies outside the inherited theorem
window.

## 3. A new continuum upper action

R0.73H proves the infinite-dimensional form estimate

\[
 H_d=-\partial_x^2+1-\frac94W_x(d)^2
 \ge h(d)I,
 \qquad
 h(d)=\frac1{20}-\frac{45}{4}d,
 \tag{3.1}
\]

on \(0\le d\le1/450\).  At \(\gamma=1/2\), completing the square for a
candidate numerical-abscissa bound \(c>0\) gives

\[
 H_{c,d}=-\partial_x^2+\frac14-\frac1{16c^2}W_x(d)^2.
 \tag{3.2}
\]

With \(\vartheta=(36c^2)^{-1}\), the coefficient identity is

\[
 H_{c,d}
 =\vartheta H_d+(1-\vartheta)(-\partial_x^2)
 +\left(\frac14-\vartheta\right)I.
 \tag{3.3}
\]

Taking \(\vartheta=[4(1-h(d))]^{-1}\) proves

\[
 \omega(\widetilde A(d))
 \le c_H(d)
 :=\frac13\sqrt{\frac{19}{20}+\frac{45d}{4}}.
 \tag{3.4}
\]

The kinetic dissipation satisfies \(L\ge I/4\).  The energy identity and
Gronwall therefore give (0.2), while direct integration of (3.4) gives
(0.3).  This bound controls the full evolution norm, not just one selected
vector.  It is nevertheless one-sided and cannot be relabelled as the
sharp action.

For an admissible inherited endpoint \(D=d_0\), R0.73F and (0.2) give only

\[
 rD
 \le\liminf_{\Lambda\to\infty}\Lambda^{-1}\log G_\Lambda(D)
 \le\limsup_{\Lambda\to\infty}\Lambda^{-1}\log G_\Lambda(D)
 \le\Omega_H(D).
 \tag{3.5}
\]

## 4. Matching at the zero-window tangent

Let \(P_\varepsilon\) be the complete frozen viscous top projection from
R0.73E, and define

\[
 \begin{aligned}
 m_\varepsilon(D)&=\inf_{\substack{v\in P_\varepsilon H\\\|v\|_2=1}}
 \|U_\varepsilon(D/\varepsilon,0)v\|_2,\\
 M_\varepsilon(D)&=\sup_{\substack{v\in P_\varepsilon H\\\|v\|_2=1}}
 \|U_\varepsilon(D/\varepsilon,0)v\|_2.
 \end{aligned}
 \tag{4.1}
\]

For every upper margin \(\rho>0\), R0.73E gives

\[
 \|e^{tB_\varepsilon(0)}\|
 \le C_\rho e^{(a+\rho)t}.
 \tag{4.2}
\]

Using
\(\|\widetilde A(d)-\widetilde A(0)\|\le C_A d\) in the exact Volterra
equation yields

\[
 M_\varepsilon(D)
 \le C_\rho\exp\left\{
 \frac{(a+\rho)D+\tfrac12C_\rho C_A D^2}{\varepsilon}
 \right\}.
 \tag{4.3}
\]

For every lower accuracy \(\zeta>0\), the R0.73F split can instead be
chosen with \(\alpha_\zeta>a-\zeta\).  It produces a dependent positive
window \(d_\zeta\), a rate \(r_\zeta>a-\zeta\), and

\[
 m_\varepsilon(D)
 \ge K_{1,\zeta}^{-1}e^{r_\zeta D/\varepsilon},
 \qquad 0<D\le d_\zeta.
 \tag{4.4}
\]

This is an every-vector minimum-gain bound because the moving unstable fiber
starts exactly at \(P_\varepsilon H\).  Taking \(\varepsilon\downarrow0\)
at fixed \(D\), then \(D\downarrow0\), and finally
\(\rho,\zeta\downarrow0\), squeezes all four rates to \(a\), proving
(0.4).

This theorem is useful but deliberately local in the observation window.
It gives neither a positive lower bound for \(d_\zeta\) as
\(\zeta\downarrow0\) nor a fixed-\(D\) limit.

## 5. Why the inherited inputs cannot decide the fixed-window action

The first obstruction is selection.  Consider

\[
 A(d)=\operatorname{diag}(a+\kappa d,a-\kappa d,-1),
 \qquad L=I.
 \tag{5.1}
\]

At \(d=0\), the top block is two-dimensional.  Both \(e_1\) and \(e_2\)
are allowed normalized top eigenvectors, but the exact gains are

\[
 G_{\varepsilon,\pm}(D)
 =e^{-D}\exp\left[
 \frac{aD\pm\kappa D^2/2}{\varepsilon}
 \right].
 \tag{5.2}
\]

Alternating the allowed launch produces two subsequential normalized-log
limits.  The abstract top-block hypotheses therefore do not define a
unique selected action.

The second obstruction is the prefactor.  Let

\[
 A(d)=\begin{pmatrix}a&0\\d&a\end{pmatrix},
 \qquad L=I,
 \qquad v(0)=e_1.
 \tag{5.3}
\]

Direct solution gives

\[
 G_\varepsilon(D)
 =e^{aD/\varepsilon-D}
 \sqrt{1+\frac{D^4}{4\varepsilon^2}}
 \sim\frac{D^2}{2}\varepsilon^{-1}e^{-D}e^{aD/\varepsilon}.
 \tag{5.4}
\]

The exponential action is \(aD\), yet its prefactor grows like
\(\varepsilon^{-1}=\Lambda\).  Hence the existence of
\(\Lambda^{-1}\log G_\Lambda\to\mathcal A\) would still not justify the
pure exponential seed \(\delta e^{-\Lambda\mathcal A}\).  A bounded
endpoint requires

\[
 0<c\le G_\Lambda e^{-\Lambda\mathcal A}\le C<\infty,
 \tag{5.5}
\]

or an explicitly identified polynomial correction.

These two examples do not model every detail of the PDE operator.  Their
role is exact and narrower: they prove that the conclusions sought at fixed
\(D\) are not logical consequences of the abstract information already
sealed in R0.73F--H.

## 6. Finite branch and WKB diagnostics

The finite package uses three declared windows:

- \(D=10^{-4}\), an explicit pilot, not a theorem endpoint;
- \(D_{\rm ub}=\sqrt{19/180}/392\), the strict analytic upper bound on
  \(d_0\), not \(d_0\);
- \(D=1/450\), a legacy comparison outside the inherited endpoint.

At Fourier cutoff \(N=48\), the instantaneous finite action is

\[
 \mathcal A_N(D)=\int_0^D
 \max\operatorname{Re}\sigma(B_{0,N}(d))\,\mathrm dd.
 \tag{6.1}
\]

The recorded values are

| finite window | \(\mathcal A_N(D)\) | \(\mathcal A_N(D)/D\) |
|---|---:|---:|
| \(10^{-4}\) | \(1.7039125194755544\times10^{-5}\) | \(0.17039125194755542\) |
| \(D_{\rm ub}\) | \(1.4112087459740226\times10^{-4}\) | \(0.17026946774036794\) |
| \(1/450\) | \(3.778603553777033\times10^{-4}\) | \(0.17003715991996649\) |

For normalized finite right/left branches
\(\langle\ell_{0,N},h_{0,N}\rangle=1\), \(\|h_{0,N}\|_2=1\), the
first WKB correction is

\[
 \mathcal C_N(D)=-\int_0^D\operatorname{Re}\left[
 \langle\ell_{0,N},\partial_dh_{0,N}\rangle
 +\langle\ell_{0,N},L_Nh_{0,N}\rangle
 \right]\,\mathrm d d.
 \tag{6.2}
\]

At the three windows, \(\mathcal C_N\) is respectively

\[
 -1.7970645480646475\times10^{-4},\quad
 -1.488647131189417\times10^{-3},\quad
 -3.987413441622952\times10^{-3}.
 \tag{6.3}
\]

At \(\Lambda=10^6\), the residual
\(\log G_{\Lambda,N}-\Lambda\mathcal A_N-\mathcal C_N\) is about
\(8.64\times10^{-7}\) at all three windows.  Cutoff, quadrature, fast-step,
and an independent kinetic-coordinate RK4 implementation agree at the
declared tolerances.

This is strong route evidence for a finite two-term law.  It is not a
continuum theorem.  Such a theorem would additionally require a unique
simple continuum branch, a first viscous eigenvalue correction, sufficient
left/right branch regularity, and a relative adiabatic complement estimate.

## 7. Literature boundary

Classical non-selfadjoint adiabatic theory and later open-system variants
show that an isolated simple branch can carry geometric and dissipative
corrections.  Finite-dimensional two-level results provide a close formal
analogue of (6.2), but they do not supply the missing continuum branch,
uniform gap, unbounded-domain control, or \(\varepsilon\)-dependent viscous
expansion for (1.2).  The exact primary-source comparison and theorem scopes
are recorded separately in `research/r073i_literature_audit.md`.

No checked source currently proves the matching selected action for this
heat-evolving periodic Rayleigh/Orr--Sommerfeld row.  This is a bounded
literature statement, not a priority or novelty claim.

## 8. Research value and next gate

R0.73I corrects a real endpoint ambiguity, strengthens the continuum upper
growth law, and identifies the exact scale that survives as
\(D\downarrow0\).  It also prevents a logically invalid replacement of the
R0.73H seed \(\delta/G_\Lambda\) by a pure exponential.

The next spectral gate is now narrower:

1. certify that the inviscid unstable point belongs to one simple unique
   rightmost branch on an explicit interval;
2. transfer that rank-one branch uniformly to the viscous operators;
3. prove a non-selfadjoint adiabatic estimate with a bounded prefactor;
4. only then revisit an action-prescribed nonlinear seed.

The finite data suggest the two-term candidate

\[
 \log G_\Lambda(D)
 =\Lambda\int_0^D\operatorname{Re}\lambda_0(s)\,ds
 +\mathcal C(D)+O(\Lambda^{-1}),
 \tag{8.1}
\]

but (8.1) remains OPEN in the continuum.

## 9. Exact boundary

- **Closed continuum statements:** the endpoint bound (0.1), the upper
  action (0.2)--(0.3), and the zero-window tangent theorem (0.4).
- **Closed negative statement:** R0.73F--H alone do not determine a
  canonical fixed-window action or bounded prefactor.
- **Finite diagnostic only:** the instantaneous action, selected gain,
  WKB correction, cutoff/step convergence, and independent RK4 comparison.
- **Open:** the canonical continuum branch, fixed-window matching action,
  two-term adiabatic law, prescribed action seed, and fixed-background
  instability.
- **Not reached:** transverse three-dimensional closure, vortex stretching,
  finite-time singularity, or either side of the Clay regularity problem.
