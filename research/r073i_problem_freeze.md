# R0.73I problem freeze: canonical selected branch and matching gain action

**Frozen:** 2026-08-30  
**Parent release:** R0.73H  
**Scope:** the exact periodic planar row
\((\beta,\xi,\gamma)=(0,0,1/2)\), positive \(\Lambda\), and the
heat-evolving two-harmonic shear  
**Evidence target:** decide exactly what R0.73F--H determine about a selected
gain action, allowing a rigorous negative result

## 0. Direct audit decision

R0.73H defines

\[
 G_\Lambda(D)
 =\|S_{1,\Lambda}(D,0)\phi_\Lambda\|_2,
 \qquad
 D=\min\{d_0,1/450\}.
 \tag{0.1}
\]

Two facts must be fixed before this gain has a reproducible sharp action.

1. The inherited launch is obtained by choosing a normalized eigenvector in
   the frozen top spectral subspace.  The analytic record does not yet prove
   that this subspace is rank one or specify a canonical choice when it is
   not.
2. The constant \(d_0\) in R0.73F is existential.  Equation (0.1) does not
   permit replacing \(D\) by \(1/450\).

The endpoint warning can already be made exact.  In R0.73F,
\(C_A=49/4\), \(K\ge1\),

\[
 d_0<\frac{\nu}{16K^2C_A},
 \qquad
 \nu=\min\{\alpha-b,c-\alpha\},
 \qquad 0<b<\alpha<c<a.
 \tag{0.2}
\]

Since \(2\nu\le c-b<a\), one has \(\nu<a/2\).  The exact R0.73H
certificate \(H_0\ge I/20\), reused below at \(\gamma=1/2\), gives the
frozen numerical-abscissa bound

\[
 a\le\omega_{1/2}(0)\le\sqrt{\frac{19}{180}}.
 \tag{0.3}
\]

Consequently every \(d_0\) chosen through the R0.73F construction obeys

\[
 \boxed{
  d_0<\frac{\sqrt{19/180}}{392}
  \approx8.2880904293\times10^{-4}<\frac1{450}.}
 \tag{0.4}
\]

Thus the inherited R0.73H endpoint is exactly \(D=d_0\), not \(1/450\).
This still does not produce a reproducible numerical endpoint: R0.73F says
to choose \(d_0\) sufficiently small, and that choice can be shrunk.

The first finite pilot supports, but does not prove, the branch picture.  At
Fourier cutoff \(N=48\), the leading branch is one-dimensional and

\[
 \frac1D\int_0^D \operatorname{Re}\lambda_{0,N}(d)\,\mathrm d d
 \approx0.17003715992,
 \qquad D=1/450.
 \tag{0.5}
\]

This is below every R0.73F lower rate \(r=\alpha+\eta>0.17035\), consistently
with (0.4).  The diagnostic crossing of the average rate \(0.17035\) occurs
near \(D=3.4674\times10^{-4}\).  Both finite numbers are route-selection
diagnostics only; the run at \(1/450\) lies outside the inherited theorem
endpoint \(D=d_0\).

R0.73I therefore does not start by extrapolating the R0.73F lower law.  It
first freezes the selected branch, the observation window, and the action.

## 1. Exact operator and notation

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

The exact fast-time evolution is

\[
 \partial_\theta v=B_\varepsilon(\varepsilon\theta)v,
 \qquad 0\le\theta\le D/\varepsilon.
 \tag{1.3}
\]

The target inviscid branch, if Contracts I1--I2 pass, is denoted
\(\lambda_0(d)\).  Its real action is

\[
 \mathcal A(D)
 =\int_0^D\operatorname{Re}\lambda_0(s)\,\mathrm ds.
 \tag{1.4}
\]

The word *selected* is reserved for the rank-one branch certified below.
Before that certificate exists, a finite eigensolver's tie-breaking and
phase convention do not define the continuum theorem.

## 2. A closed continuum upper action before branch selection

The R0.73H exact certificate yields, for \(0\le d\le1/450\),

\[
 H_d=-\partial_x^2+1-\frac94W_x(d)^2
 \ge h(d)I,
 \qquad
 h(d)=\frac1{20}-\frac{45}{4}d.
 \tag{2.1}
\]

For the selected row \(\gamma=1/2\), an upper numerical-abscissa candidate
\(c>0\) is equivalent, after completing the square, to positivity of

\[
 H_{c,d}
 =-\partial_x^2+\frac14-\frac{1}{16c^2}W_x(d)^2.
 \tag{2.2}
\]

With \(\vartheta=(36c^2)^{-1}\), this is the exact identity

\[
 H_{c,d}
 =\vartheta H_d+(1-\vartheta)(-\partial_x^2)
   +\left(\frac14-\vartheta\right)I.
 \tag{2.3}
\]

Taking \(\vartheta=[4(1-h(d))]^{-1}\) proves

\[
 \omega_{1/2}(d)
 \le c_H(d)
 :=\frac13\sqrt{\frac{19}{20}+\frac{45}{4}d}.
 \tag{2.4}
\]

The viscous term \(-\varepsilon L\) is dissipative in the kinetic \(L^2\)
representation.  Gronwall applied to (1.3) therefore gives, for the full
evolution norm and hence for every selected vector,

\[
 \boxed{
  G_\varepsilon(D)
  \le\|U_\varepsilon(D/\varepsilon,0)\|
  \le\exp\!\left(\frac{\Omega_H(D)}{\varepsilon}-\frac D4\right),}
 \tag{2.5}
\]

where

\[
 \boxed{
 \Omega_H(D)
 =\int_0^D c_H(s)\,\mathrm ds
 =\frac8{405}\left[
   \left(\frac{19}{20}+\frac{45D}{4}\right)^{3/2}
   -\left(\frac{19}{20}\right)^{3/2}
  \right]}
 \tag{2.6}
\]

for \(0\le D\le1/450\).  This is a closed, exact continuum upper action.
The strict factor \(e^{-D/4}\) retains \(L\ge I/4\); it does not change the
normalized exponential action.  This is not the matching action: no lower
bound with the same exponent follows without the branch and adiabatic
contracts below.  Combining it with the
R0.73F lower law on any one admissible inherited endpoint \(D=d_0\) only
gives

\[
 rD\le\liminf_{\Lambda\to\infty}\Lambda^{-1}\log G_\Lambda(D)
 \le\limsup_{\Lambda\to\infty}\Lambda^{-1}\log G_\Lambda(D)
 \le\Omega_H(D).
 \tag{2.7}
\]

## 3. Contract I1: a unique simple rightmost inviscid branch

Find an explicit \(D_*>0\), an explicit simple closed contour family
\(\Gamma(d)\), and constants \(g_*,m_*>0\) such that for every
\(0\le d\le D_*\):

1. \(\Gamma(d)\subset\rho(B_0(d))\);
2. its Riesz projection \(P_0(d)\) has rank one;
3. the enclosed eigenvalue \(\lambda_0(d)\) is the unique spectral point
   with maximal real part;
4. the rest of the spectrum lies at least \(g_*\) to the left in real part;
5. normalized right and left eigenvectors can be chosen with
   \(|\langle \ell_0(d),h_0(d)\rangle|\ge m_*\).

The preferred certificate is a validated periodic-Rayleigh monodromy
argument.  A sign-changing real root alone is insufficient: the certificate
must count the root, prove simplicity, and exclude additional spectrum in
the declared right half-plane.  A finite Fourier gap is diagnostic only.

## 4. Contract I2: a uniform rank-one viscous branch

For sufficiently small \(\varepsilon>0\), prove on the same interval that
the viscous contour encloses exactly one eigenvalue
\(\lambda_\varepsilon(d)\), with projection
\(P_\varepsilon(d)\), and

\[
 \sup_{0\le d\le D_*}
 \left(
  \|P_\varepsilon(d)-P_0(d)\|
  +|\lambda_\varepsilon(d)-\lambda_0(d)|
 \right)\longrightarrow0.
 \tag{3.1}
\]

The matching-prefactor target requires the stronger eigenvalue estimate

\[
 \sup_{0\le d\le D_*}
 |\lambda_\varepsilon(d)-\lambda_0(d)|
 \le C\varepsilon.
 \tag{3.2}
\]

One admissible route is to pair the viscous eigenvalue equation with the
smooth inviscid adjoint eigenvector and move \(L\) onto that adjoint.  The
denominator must be controlled by the rank-one projection convergence.
Uniform \(C^1\) bounds for \(P_\varepsilon(d)\) must be proved in
\(\mathcal B(L^2)\); an unscaled graph-norm assertion is not assumed.

## 5. Contract I3: non-selfadjoint adiabatic tracking

Let \(h_\varepsilon(0)\) be the normalized vector in
\(P_\varepsilon(0)L^2\), with phase fixed by a declared nonzero anchor.  The
exact selected gain is

\[
 G_\varepsilon(D)
 =\|U_\varepsilon(D/\varepsilon,0)h_\varepsilon(0)\|_2.
 \tag{4.1}
\]

For every fixed \(0<D\le D_*\), prove constants independent of small
\(\varepsilon\) such that

\[
 C_D^{-1}e^{\mathcal A(D)/\varepsilon}
 \le G_\varepsilon(D)
 \le C_De^{\mathcal A(D)/\varepsilon}.
 \tag{4.2}
\]

Equivalently,

\[
 \log G_\varepsilon(D)
 =\varepsilon^{-1}\mathcal A(D)+O_D(1).
 \tag{4.3}
\]

The proof must control nonnormal leakage into the complement over the full
\(D/\varepsilon\) fast interval.  Instantaneous eigenvalues, a finite
propagator, or a generic self-adjoint adiabatic citation cannot replace this
step.  The rightmost gap in I1 is essential: an \(O(\varepsilon)\) coupling
to a faster branch could otherwise dominate exponentially.

## 6. Contract I4: action-resolved backward localization

For \(0\le s\le D\le D_*\), prove

\[
 \frac{\|U_\varepsilon(s/\varepsilon,0)h_\varepsilon(0)\|_2}
 {G_\varepsilon(D)}
 \le C_D
 \exp\!\left[-\frac1\varepsilon
   \int_s^D\operatorname{Re}\lambda_0(\tau)\,\mathrm d\tau
 \right].
 \tag{5.1}
\]

This is the replacement for the coarse R0.73F rate in the R0.73H nonlinear
coefficient estimates.  The lower bound
\(\inf_{[0,D]}\operatorname{Re}\lambda_0>1/6\) is sufficient for the
strict quadratic and cubic integrability gates, but it must be certified on
the declared interval.

## 7. Contract I5: prescribed action-scale nonlinear departure

After I1--I4 pass, lift the selected kinetic vector to the real
\(K_z=\pm1\) planar velocity pair \(\phi_\Lambda\).  The prescribed seed is

\[
 u_\Lambda^\delta(0)
 =\delta e^{-\Lambda\mathcal A(D)}\phi_\Lambda.
 \tag{6.1}
\]

The R0.73H harmonic hierarchy and fourth-order remainder may then be reused
only after all constants are rechecked with (5.1).  The target theorem is

\[
 c_D\delta
 \le
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\delta(D)\|_2
 \le C_D\delta,
 \tag{6.2}
\]

for a fixed sufficiently small \(\delta\), together with

\[
 \|u_\Lambda^\delta(0)\|_{H^3}
 \le C\delta\Lambda^2e^{-\Lambda\mathcal A(D)}\to0.
 \tag{6.3}
\]

This would be a prescribed *action-scale* seed.  It would not identify the
coarse exponent \(rD\) from R0.73F as sharp, produce a fixed-background
Lyapunov theorem, leave the planar invariant class, or address singularity
and Clay.

## 8. Finite diagnostic contract

The finite package must distinguish four objects:

1. the instantaneous finite eigenvalue integral;
2. the exact finite selected-vector gain;
3. the full finite propagator norm;
4. the residual
   \(\log G_{\varepsilon,N}-\mathcal A_N(D)/\varepsilon\).

If the branch is normalized by
\(\langle\ell_0(d),h_0(d)\rangle=1\) and \(\|h_0(d)\|_2=1\), the secondary
two-term diagnostic is

\[
 \mathcal C_N(D)=-\int_0^D\operatorname{Re}\left[
  \langle\ell_{0,N},\partial_dh_{0,N}\rangle
  +\langle\ell_{0,N},L_Nh_{0,N}\rangle
 \right]\,\mathrm d d.
 \tag{8.1}
\]

Agreement with
\(\log G_{\varepsilon,N}-\mathcal A_N(D)/\varepsilon\) is a finite WKB
diagnostic only.  A continuum claim
\(\log G_\varepsilon=\mathcal A/\varepsilon+\mathcal C+O(\varepsilon)\)
would additionally require a first-order viscous eigenvalue expansion,
\(C^2\) branch regularity, and a relative \(O(\varepsilon)\) complement
estimate; Contracts I1--I3 as currently written target only an \(O(1)\)
prefactor.

It must include at least two independent implementations, cutoff comparison,
fast-step comparison, a phase-anchor check, rank/gap diagnostics, raw complex
eigenvectors or lossless stable references, progress logs, environment, and
hashes.  The primary endpoint must not be labelled a theorem endpoint until
I1 gives an explicit continuum \(D_*\).

## 9. Fail-closed decision ledger

The positive route may mark `canonicalSelectedBranch` CLOSED only if I1
passes.  It may mark `matchingSelectedGainAction` CLOSED only if I1--I4
pass, and `prescribedActionSeedDeparture` CLOSED only if I1--I5 pass.

There is also a complete negative outcome for this section.  If exact
counterexamples show that the inherited R0.73F--H hypotheses do not
determine a fixed-window action or bounded prefactor, R0.73I may close
`fixedWindowActionFromInheritedInputs=FALSE_AS_INFERENCE` while leaving the
actual operator's matching action OPEN.  That is a theorem about logical
insufficiency, not evidence that the selected PDE gain lacks an action.

Any of the following keeps the corresponding claim OPEN or turns the route
into a stated negative result:

- more than one rightmost inviscid eigenvalue or an unresolved crossing;
- failure of a uniform rightmost gap;
- loss of the rank-one viscous branch;
- unbounded adiabatic leakage relative to the selected branch;
- divergence of the finite residual incompatible with an \(O(1)\) prefactor;
- inability to certify an explicit positive observation window.

Regardless of the outcome, the following remain OPEN:

- one fixed background with a Lyapunov-instability sequence;
- transverse Orr--Sommerfeld/Squire evolution and nonlinear triad closure;
- three-dimensional vortex stretching;
- finite-time singularity and the Clay regularity alternative.
