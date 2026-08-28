# R0.72Z report source: a sharp Orr--Sommerfeld form threshold and orientation-paid Squire transfer

**Date:** 2026-08-28

**Status:** this section resolves two ambiguities left by R0.72Y.  First, the
Orr--Sommerfeld pressure feedback has an exact self-adjoint commutator form.
That form gives prefactor-one decay and forced estimates on a signed high-gap
class whose sufficient threshold is
\(g\gtrsim |c|^{2/5}\), equivalently \(g\gtrsim\alpha^{-2}\).
Two-mode witnesses show that the exponent \(2/5\) is necessary for any
all-start prefactor-one \(L^2_q\) theorem of this type, while an exact
gapless tangent mode rules out importing the scalar \(A_2\) contraction to
the unprojected abstract Orr--Sommerfeld equation.  Second, the Squire source
has an exact kinetic-energy orientation factor.  The apparent raw
\(|\xi/\gamma|\) singularity becomes a bounded sine factor after kinetic
normalization, but an explicit \(|\Lambda|\) payment remains and is sharp.
Ordinary-gap, strong-scalar-kernel, endpoint, and damping-gap transfer
estimates are proved from the complete history of \(q\).  These results close
a fixed-row graph-regularity class; they do not close the low-gap physical
velocity direct sum, nonlinear Navier--Stokes, or the Clay problem.

**Keywords:** Orr--Sommerfeld pressure feedback, Squire transfer,
commutator form, time-dependent shear, transient growth, orientation,
enhanced dissipation, Bloch row

---

## 0. Exact decision and claim boundary

Retain the R0.72Y row notation

\[
 A_\beta=\partial_x+i\beta,\qquad
 D_\beta=-iA_\beta=-i\partial_x+\beta,
 \tag{0.1}
\]

\[
 \mathcal L=D_\beta^2+\mu,qquad
 \rho=\operatorname{dist}(\beta,\mathbb Z),\qquad
 g=\mu+\rho^2>0,
 \tag{0.2}
\]

\[
 c=\gamma\Lambda,\qquad
 \mu=\xi^2+\gamma^2,
 \tag{0.3}
\]

and the exact triangular equations

\[
 q_d=(-\mathcal L-icW)q
 -icW_{xx}\mathcal L^{-1}q+F_q,
 \tag{0.4}
\]

\[
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q+F_\eta.
 \tag{0.5}
\]

The positive conclusions are

\[
\boxed{
\begin{aligned}
\texttt{exactOSFeedbackCommutatorIdentity}&=\texttt{CLOSED},\\
\texttt{signedRelativeFormOSAbsorption}&=\texttt{CLOSED},\\
\texttt{highGapOSPrefactorOneDecay}&=\texttt{CLOSED},\\
\texttt{highGapOSForcedScaleLedger}&=\texttt{CLOSED},\\
\texttt{alphaMinusTwoOSGapSufficiency}&=\texttt{CLOSED},\\
\texttt{highModeOSGapExponentSharpness}&=\texttt{CLOSED},\\
\texttt{exactGaplessOSTangentMode}&=\texttt{CLOSED},\\
\texttt{exactSquireDuhamel}&=\texttt{CLOSED},\\
\texttt{exactKineticOrientationNormalization}&=\texttt{CLOSED},\\
\texttt{optimalInstantaneousSquireCoefficient}&=\texttt{CLOSED},\\
\texttt{orientationUniformWithLambdaPayment}&=\texttt{CLOSED},\\
\texttt{ordinaryGapSquireHistoryTransfer}&=\texttt{CLOSED},\\
\texttt{strongKernelConditionalSquireTransfer}&=\texttt{CLOSED},\\
\texttt{dampingGapConvolutionFormula}&=\texttt{CLOSED},\\
\texttt{fixedRowOSSquireGraphRegularity}&=\texttt{CLOSED}.
\end{aligned}}
\tag{0.6}
\]

The following proposed extensions are false:

\[
\boxed{
\begin{aligned}
\texttt{scalarA2AutomaticallyAbsorbsOSFeedbackAllStrongRows}
 &=\texttt{FALSE},\\
\texttt{epsilonOnlyOSBoundedPerturbationGate}&=\texttt{FALSE},\\
\texttt{allStrongRowsOSPrefactorOneContraction}&=\texttt{FALSE},\\
\texttt{abstractGaplessOSA2StrictContraction}&=\texttt{FALSE},\\
\texttt{rawOrientationUniformFromCOnly}&=\texttt{FALSE},\\
\texttt{epsilonOnlySquireTransfer}&=\texttt{FALSE},\\
\texttt{backgroundUniformEnergyBoundWithoutLambdaPayment}
 &=\texttt{FALSE},\\
\texttt{uniformlyEquivalentLambdaIndependentContractiveNorm}
 &=\texttt{FALSE},\\
\texttt{equalRateUniformGapDenominator}&=\texttt{FALSE},\\
\texttt{instantaneousQEndpointAloneControlsEta}&=\texttt{FALSE}.
\end{aligned}}
\tag{0.7}
\]

The remaining system statements are open:

\[
\boxed{
\begin{aligned}
\texttt{lowGapOSTransientA2Propagator}&=\texttt{OPEN},\\
\texttt{collisionScaleOSLimitingAbsorption}&=\texttt{OPEN},\\
\texttt{unconditionalStrongFullRowA2Estimate}&=\texttt{OPEN},\\
\texttt{BlochUniformPhysicalVelocityDirectSum}&=\texttt{OPEN},\\
\texttt{lowGapWeakFullRows}&=\texttt{OPEN},\\
\texttt{completeLinearizedShearSubsystem}&=\texttt{OPEN},\\
\texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
\texttt{Clay}&=\texttt{OPEN}.
\end{aligned}}
\tag{0.8}
\]

The old phrase `orientationUniformSquireTransfer` was ambiguous.  It is
replaced by two exact statements: orientation is bounded in the kinetic
coordinates if \(|\Lambda|\) is paid, while a bound depending only on
\(|c|=|\gamma\Lambda|\) is false.

---

## 1. Scope and provenance

R0.72Y derived (0.4)--(0.5), the velocity recovery formula, and the scalar
all-start kernel.  It left both pressure absorption and orientation
accounting open.  The present section uses only those exact equations and
the heat-shear profile

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx}.
 \tag{1.1}
\]

No spectral stability of the frozen Rayleigh operator is assumed in the
positive high-gap theorem.  Conversely, no claim is made that a high-gap
energy theorem supplies a low-gap critical-layer or limiting-absorption
theorem.

The supplied thesis provides the standard linearized Navier--Stokes and
normal-mode background.  It does not contain the time-dependent path (1.1),
the commutator threshold below, the Bloch ledger, or the collision-scale
sharpness witnesses.

---

## 2. The exact Orr--Sommerfeld pressure form

Use the inner product

\[
 \langle f,g\rangle=\int_{\mathbb T}\overline f\,g\,dx.
 \tag{2.1}
\]

Put

\[
 v=\mathcal L^{-1}q,\qquad
 r=\mathcal L^{1/2}q=\mathcal L^{3/2}v,
 \tag{2.2}
\]

\[
 f=W_{xx},\qquad h=f_x=W_{xxx}.
 \tag{2.3}
\]

The commutators are

\[
 [D_\beta,f]=-ih,
 \tag{2.4}
\]

\[
 [\mathcal L,f]
 =D_\beta[D_\beta,f]+[D_\beta,f]D_\beta
 =-i(D_\beta h+hD_\beta).
 \tag{2.5}
\]

Therefore

\[
\begin{aligned}
 2i\operatorname{Im}\langle\mathcal Lv,fv\rangle
 &=\langle\mathcal Lv,fv\rangle
   -\langle fv,\mathcal Lv\rangle\\
 &=\langle v,[\mathcal L,f]v\rangle\\
 &=-i\langle v,(D_\beta h+hD_\beta)v\rangle.
\end{aligned}
\tag{2.6}
\]

Define

\[
\boxed{
 H_{\beta,\mu}(d)
 =\frac12\mathcal L^{-3/2}
 (D_\beta W_{xxx}+W_{xxx}D_\beta)
 \mathcal L^{-3/2}.}
\tag{2.7}
\]

It is self-adjoint.  The scalar potential \(-icW\) is skew, and (2.6)
gives the exact identity

\[
\boxed{
 \frac12\frac d{dd}\|q\|_2^2+\|r\|_2^2
 =\operatorname{Re}\langle F_q,q\rangle
 -c\langle r,H_{\beta,\mu}(d)r\rangle.}
\tag{2.8}
\]

The energy real part therefore sees a third-derivative commutator, not the
raw operator norm of \(W_{xx}\mathcal L^{-1}\).  This is the source of the
improved threshold.

---

## 3. Signed high-gap absorption and prefactor-one decay

For a compact interval \(K\), define the signed relative form constant

\[
 \Theta_K(c,\beta,\mu)
 =\sup_{d\in K}
 \lambda_{\max}(-cH_{\beta,\mu}(d)).
 \tag{3.1}
\]

### Theorem 3.1: exact signed-form class

If

\[
 \boxed{\Theta_K(c,\beta,\mu)<1,}
 \tag{3.2}
\]

and \(\omega=1-\Theta_K\), then every homogeneous solution of (0.4)
satisfies

\[
\boxed{
 \|U_{\rm OS}(d,s)\|_{2\to2}
 \le e^{-\omega g(d-s)},
 \qquad d\ge s,\quad d,s\in K.}
\tag{3.3}
\]

### Proof

Moving the pressure form in (2.8) to the left gives

\[
 \frac12\frac d{dd}\|q\|_2^2
 +\langle r,(I+cH)r\rangle=0.
 \tag{3.4}
\]

By (3.1)--(3.2), the second term is at least
\(\omega\|r\|_2^2\).  Since

\[
 \|r\|_2^2=\langle q,\mathcal Lq\rangle
 \ge g\|q\|_2^2,
 \tag{3.5}
\]

Gronwall proves (3.3).  The prefactor is exactly one.  This conclusion is in
the \(L^2_q\) graph tier and is not a kinetic-energy contraction for
arbitrary velocity data.

---

## 4. Explicit Fourier matrix and the \(\alpha^{-2}\) sufficient class

Let

\[
 k_n=n+\beta,qquad \lambda_n=k_n^2+\mu.
 \tag{4.1}
\]

The four nonzero Fourier coefficients of \(h=W_{xxx}\) are

\[
 \widehat h_{\pm1}=\frac14e^{-d},
 \qquad
 \widehat h_{\pm2}=-e^{-4d}.
 \tag{4.2}
\]

Thus

\[
\boxed{
 (H_{\beta,\mu})_{mn}
 =\frac{(k_m+k_n)\widehat h_{m-n}}
 {2\lambda_m^{3/2}\lambda_n^{3/2}}.}
\tag{4.3}
\]

A certificate-friendly Schur bound is

\[
 \|H(d)\|
 \le\sup_n\sum_{\ell=\pm1,\pm2}
 \frac{|2k_n+\ell|a_\ell(d)}
 {2\lambda_n^{3/2}\lambda_{n+\ell}^{3/2}},
 \tag{4.4}
\]

where

\[
 a_{\pm1}=\frac14e^{-d},\qquad
 a_{\pm2}=e^{-4d}.
 \tag{4.5}
\]

For a simpler closed condition, put

\[
 s_{\beta,\mu}
 =\sup_n\frac{|k_n|}{(k_n^2+\mu)^{3/2}}.
 \tag{4.6}
\]

Since \(D_\beta\) commutes with \(\mathcal L\), (2.7) gives

\[
 \|H(d)\|
 \le \|W_{xxx}(d)\|_\infty g^{-3/2}s_{\beta,\mu}.
 \tag{4.7}
\]

Moreover

\[
 s_{\beta,\mu}
 \le\min\left\{g^{-1},\frac{2}{3\sqrt3\,\mu}\right\}.
 \tag{4.8}
\]

For \(K=[d_-,d_+]\), the exact heat path has

\[
 M_{3,K}:=\sup_{K,x}|W_{xxx}(d,x)|
 =\frac12e^{-d_-}+2e^{-4d_-}.
 \tag{4.9}
\]

Hence, for any fixed \(0<\theta_0<1\), the row class

\[
\boxed{
 |c|M_{3,K}g^{-3/2}s_{\beta,\mu}\le\theta_0}
\tag{4.10}
\]

obeys Theorem 3.1 with \(\omega\ge1-\theta_0\).  A coarser but transparent
sufficient condition is

\[
\boxed{
 g\ge\left(\frac{|c|M_{3,K}}{\theta_0}\right)^{2/5}.}
\tag{4.11}
\]

For strong rows, write

\[
 |c|=4\alpha^{-5}.
 \tag{4.12}
\]

Then (4.11) is

\[
\boxed{
 g\ge4^{2/5}
 \left(\frac{M_{3,K}}{\theta_0}\right)^{2/5}
 \alpha^{-2}.}
\tag{4.13}
\]

In physical row parameters,

\[
 (\xi^2+\gamma^2+\rho^2)^{5/2}
 \ge\theta_0^{-1}M_{3,K}|\gamma\Lambda|.
 \tag{4.14}
\]

This is a larger class than raw Duhamel absorption.  It is still a high-gap
class; it does not decide the collision-scale low-gap propagator.

---

## 5. Forced Orr--Sommerfeld estimates

Let

\[
 a=\omega g,qquad D_K=d_+-d_-,
 \tag{5.1}
\]

and define

\[
 \Phi_a(D)=\frac{1-e^{-aD}}a,
 \qquad
 \Psi_a(D)=\left(\frac{1-e^{-2aD}}{2a}\right)^{1/2}.
 \tag{5.2}
\]

Duhamel's formula and (3.3) give

\[
\boxed{
 \|q\|_{L_d^2L_x^2}
 \le\Psi_a(D_K)\|q(d_-)\|_2
 +\Phi_a(D_K)\|F_q\|_{L_d^2L_x^2},}
\tag{5.3}
\]

\[
\boxed{
 \|q\|_{L_d^\infty L_x^2}
 \le\|q(d_-)\|_2
 +\Psi_a(D_K)\|F_q\|_{L_d^2L_x^2}.}
\tag{5.4}
\]

There is also a common negative-norm energy ledger.  For
\(s\in\{0,1,\alpha\}\), set

\[
 \|F\|_{\mathcal H^{-1}_{s,\beta}}^2
 =\sum_n\frac{|F_n|^2}{1+s^2k_n^2}.
 \tag{5.5}
\]

Thus \(s=0\) is \(L^2\), \(s=1\) is standard \(H^{-1}_\beta\), and
\(s=\alpha\) is the semiclassical norm.  The exact embedding constant is

\[
\boxed{
 \ell_s^2
 =\sup_n\frac{1+s^2k_n^2}{k_n^2+\mu}
 =\max\left\{s^2,\frac{1+s^2\rho^2}{g}\right\}.}
\tag{5.6}
\]

For zero initial data, the energy inequality and Young's inequality give

\[
\boxed{
 \|\mathcal L^{1/2}q\|_{L_d^2L_x^2}
 \le\frac{\ell_s}{\omega}
 \|F_q\|_{L_d^2\mathcal H^{-1}_{s,\beta}},}
\tag{5.7}
\]

\[
\boxed{
 \|q\|_{L_d^2L_x^2}
 \le\frac{\ell_s}{\omega\sqrt g}
 \|F_q\|_{L_d^2\mathcal H^{-1}_{s,\beta}},}
\tag{5.8}
\]

\[
\boxed{
 \|q\|_{L_d^\infty L_x^2}
 \le\frac{\ell_s}{\sqrt\omega}
 \|F_q\|_{L_d^2\mathcal H^{-1}_{s,\beta}}.}
\tag{5.9}
\]

On the class \(g\gtrsim\alpha^{-2}\), these formulas reproduce the R0.72Y
powers:

| spatial forcing norm | spacetime \(q\) | endpoint \(q\) |
|---|---:|---:|
| \(L_x^2\) | \(O(\alpha^2)\) | \(O(\alpha)\) |
| standard \(H^{-1}_\beta\) | \(O(\alpha)\) | \(O(1)\) |
| semiclassical \(\mathcal H^{-1}_{\alpha,\beta}\) | \(O(\alpha^2)\) | \(O(\alpha)\) |

The powers survive pressure feedback only on the signed high-gap class.  No
low-gap forced theorem is inferred.

---

## 6. Why raw bounded-perturbation absorption loses scale

The direct estimate is

\[
 \|icW_{xx}\mathcal L^{-1}q\|_2
 \le |c|M_{2,K}g^{-1}\|q\|_2.
 \tag{6.1}
\]

Combining only (6.1) with the R0.72X \(A_2\) kernel requires, at the level
of powers,

\[
 g\gg\alpha^{-3}.
 \tag{6.2}
\]

Taking the minimum with ordinary gap damping improves the Neumann condition
to

\[
 g\gg\alpha^{-5/2}.
 \tag{6.3}
\]

The exact commutator form reaches

\[
 g\gtrsim\alpha^{-2}.
 \tag{6.4}
\]

The improvement is structural.  It cannot be recovered by relabeling the
raw pressure term as generic \(L^2\) or \(H^{-1}\) forcing.

For example, at \(\beta=0\),

\[
 \|-icW_{xx}\mathcal L^{-1}e_0\|_2
 =\frac{|c|}{\mu}
 \left(\frac{e^{-2d}}8+\frac{e^{-8d}}2\right)^{1/2}.
 \tag{6.5}
\]

It diverges as \(\mu\downarrow0\).  Standard and semiclassical negative
norms do not remove that \(|c|/\mu\) divergence.

---

## 7. Two-mode growth and sharpness of the gap exponent

Let \(e_n=(2\pi)^{-1/2}e^{inx}\) and define

\[
 r_n^\pm=\frac{e_n\pm e_{n+1}}{\sqrt2},
 \qquad
 q_n^\pm=\mathcal L^{-1/2}r_n^\pm.
 \tag{7.1}
\]

The only matrix entry used by this pair is

\[
\boxed{
 a_n(d,\beta,\mu)
 =\frac{e^{-d}|2(n+\beta)+1|}
 {8[(n+\beta)^2+\mu]^{3/2}
 [(n+1+\beta)^2+\mu]^{3/2}}.}
\tag{7.2}
\]

Choose the sign in (7.1) so that the pressure form is positive.  Since
\(\|r_n^\pm\|_2=1\), (2.8) with zero forcing gives

\[
\boxed{
 \left.\frac12\frac d{dd}\|q_n^\pm\|_2^2\right|_{d=d_0}
 =|c|a_n(d_0,\beta,\mu)-1.}
\tag{7.3}
\]

For \(\beta=0,n=0\),

\[
 a_0=\frac{e^{-d}}
 {8\mu^{3/2}(1+\mu)^{3/2}}.
 \tag{7.4}
\]

Thus every fixed \(|c|\ge4\) admits sufficiently small positive \(\mu\)
for which the \(L^2_q\) norm grows immediately.  Hence an all-gap,
prefactor-one OS contraction is false.

For exponent sharpness, take \(\beta=0\), \(\mu=2n^2\).  Then

\[
 a_n
 =\frac{e^{-d}(2n+1)}
 {8(3n^2)^{3/2}(3n^2+2n+1)^{3/2}},
 \tag{7.5}
\]

and

\[
\boxed{
 a_n\mu^{5/2}\longrightarrow
 \frac{\sqrt2}{27}e^{-d}.}
\tag{7.6}
\]

Therefore \(g\asymp |c|^{2/5}\) is the necessary power scale for a theorem
that demands prefactor-one \(L^2_q\) contraction for every row and every
start time.  The witness does not rule out a low-gap theorem with an
explicit transient prefactor.

---

## 8. The exact gapless tangent mode

At \(\beta=\mu=0\), interpret \(\mathcal L_0=-\partial_x^2\) on the
mean-zero subspace.  Then

\[
 q_*(d)=W_{xx}(d),
 \qquad
 \mathcal L_0^{-1}q_*=-W.
 \tag{8.1}
\]

Because \(W_d=W_{xx}\),

\[
 (q_*)_d=W_{xxxx}=-\mathcal L_0q_*.
 \tag{8.2}
\]

The two large imaginary terms cancel exactly:

\[
 Wq_*+W_{xx}\mathcal L_0^{-1}q_*
 =WW_{xx}-W_{xx}W=0.
 \tag{8.3}
\]

Thus \(q_*\) is an exact Orr--Sommerfeld solution for every value of \(c\).
Its norm is

\[
 \frac1{2\pi}\|q_*(d)\|_2^2
 =\frac18e^{-2d}+\frac12e^{-8d}.
 \tag{8.4}
\]

On a block of length \(O(\alpha^2)\), the ratio of its endpoint norms tends
to one as \(\alpha\downarrow0\).  Consequently, the abstract gapless
Orr--Sommerfeld equation cannot inherit the scalar \(A_2\) strict block
factor uniformly in \(|c|=4\alpha^{-5}\).

This is a structural tangent mode, not a physical \(\mu=0\) velocity row:
the OS--Squire inverse coordinates degenerate there.  It therefore does not
by itself refute a properly projected physical velocity theorem for
\(\mu>0\).

---

## 9. Exact collision rescaling: pressure remains leading order

Let

\[
 d=\alpha^2S,\qquad x=\alpha X,
 \qquad |c|=4\alpha^{-5},
 \tag{9.1}
\]

\[
 V_\alpha(S,X)=4\alpha^{-3}W(\alpha^2S,\alpha X),
 \qquad
 \mathcal L_{\alpha,\mu}=-\partial_X^2+\alpha^2\mu.
 \tag{9.2}
\]

After the Bloch twist is moved into the boundary phase, the exact scaled OS
equation is

\[
\boxed{
 q_S=(\partial_X^2-\alpha^2\mu-i\sigma V_\alpha)q
 -i\sigma(V_\alpha)_{XX}
 \mathcal L_{\alpha,\mu}^{-1}q.}
\tag{9.3}
\]

Near the collision,

\[
 V_\alpha(S,X)\longrightarrow-(X^3+6SX),
 \qquad
 (V_\alpha)_{XX}\longrightarrow-6X.
 \tag{9.4}
\]

Both imaginary terms in (9.3) are order one.  The pressure term is not a
vanishing perturbation of the cubic scalar generator.  This exact scaling
explains why Section 4 closes only after a gap payment and why a genuine
low-gap theorem needs new operator structure.

---

## 10. Kinetic orientation coordinates for Squire transfer

For \(\mu>0\), define

\[
 Q(d)=\mu^{-1/2}\|\mathcal L^{-1/2}q(d)\|_2,
 \qquad
 H(d)=\mu^{-1/2}\|\eta(d)\|_2.
 \tag{10.1}
\]

R0.72Y's recovery identity becomes

\[
\boxed{\|u(d)\|_2^2=Q(d)^2+H(d)^2.}
\tag{10.2}
\]

Let \(U_c(d,s)\) denote the scalar evolution family generated by
\(-\mathcal L-icW\).  The exact Squire formula is

\[
\boxed{
\begin{aligned}
 \eta(d)={}&U_c(d,s)\eta(s)\\
 &+i\xi\Lambda\int_s^d
 U_c(d,r)W_x(r)\mathcal L^{-1}q(r)\,dr\\
 &+\int_s^dU_c(d,r)F_\eta(r)\,dr.
\end{aligned}}
\tag{10.3}
\]

Define the instantaneous spatial norm

\[
 b_j(d)=\|M_{W_x(d)}\mathcal L^{-1/2}\|_{2\to2},
 \qquad
 a_j(d)=|\xi\Lambda|b_j(d).
 \tag{10.4}
\]

Then

\[
 \frac1{\sqrt\mu}
 \|i\xi\Lambda W_x\mathcal L^{-1}q\|_2
 \le a_j(d)Q(d).
 \tag{10.5}
\]

The constant \(a_j(d)\) is the exact induced operator norm in the kinetic
coordinates.  If

\[
 M_{1,K}=\sup_{K}\|W_x(d)\|_\infty,
 \tag{10.6}
\]

then

\[
 b_{j,K}\le\frac{M_{1,K}}{\sqrt g},
 \tag{10.7}
\]

\[
\boxed{
 a_{j,K}\le |\Lambda|M_{1,K}\chi_j,
 \qquad
 \chi_j=\frac{|\xi|}{\sqrt{\xi^2+\gamma^2+\rho^2}}\le1.}
\tag{10.8}
\]

When \(\gamma\ne0\) and \(R_j=|\xi/\gamma|\),

\[
 \chi_j=\frac{R_j}
 {\sqrt{1+R_j^2+(\rho/\gamma)^2}},
 \tag{10.9}
\]

and equivalently

\[
 a_{j,K}\le\frac{|c|R_jM_{1,K}}{\sqrt g}.
 \tag{10.10}
\]

The raw variables expose \(R_j\); the kinetic coordinates compress pure
orientation to \(\chi_j\le1\).  The remaining \(|\Lambda|\) is a background
amplitude payment, not a removable coordinate artifact.

---

## 11. A refined spatial coefficient and its transverse limit

For the normalized torus average,

\[
 m_2(d)^2
 :=\frac1{2\pi}\int_{0}^{2\pi}|W_x(d,x)|^2dx
 =\frac18(e^{-2d}+e^{-8d}).
 \tag{11.1}
\]

The reciprocal-lattice identity is

\[
 \sum_{n\in\mathbb Z}
 \frac1{(n+\beta)^2+\mu}
 =\frac{\pi}{\sqrt\mu}
 \frac{\sinh(2\pi\sqrt\mu)}
 {\cosh(2\pi\sqrt\mu)-\cos(2\pi\beta)}.
 \tag{11.2}
\]

The Hilbert--Schmidt bound therefore gives

\[
\boxed{
 b_j(d)\le\min\left\{
 \frac{\|W_x(d)\|_\infty}{\sqrt g},
 m_2(d)\left[
 \frac{\pi}{\sqrt\mu}
 \frac{\sinh(2\pi\sqrt\mu)}
 {\cosh(2\pi\sqrt\mu)-\cos(2\pi\beta)}
 \right]^{1/2}\right\}.}
\tag{11.3}
\]

At \(\beta=0\), applying the operator to the constant mode gives the
matching lower bound, so

\[
 b_j(d)\sim\frac{m_2(d)}{\sqrt\mu}
 \qquad(\mu\downarrow0).
 \tag{11.4}
\]

Along the exact transverse boundary \(\gamma=0\), \(\xi=\sqrt\mu\), hence

\[
 a_j(d)\longrightarrow |\Lambda|m_2(d).
 \tag{11.5}
\]

There is no artificial angle blow-up in physical energy, but lift-up
remains nonzero.  If instead \(c\) is fixed while \(\gamma\to0\), then
\(\Lambda=c/\gamma\) diverges; the resulting blow-up is precisely the
unpaid background-amplitude limit.

---

## 12. Ordinary-gap Squire history transfer

The scalar energy identity yields

\[
 \|U_c(d,s)\|_{2\to2}\le e^{-g(d-s)}.
 \tag{12.1}
\]

Let \(D=D_K\), \(a=\sup_Ka_j(d)\), and

\[
 f(d)=\mu^{-1/2}\|F_\eta(d)\|_2.
 \tag{12.2}
\]

Then (10.3), Young's inequality, and (5.2) give

\[
\boxed{
 \|H\|_{L_d^2(K)}
 \le\Psi_g(D)H(d_-)
 +\Phi_g(D)
 \bigl(a\|Q\|_{L_d^2(K)}+\|f\|_{L_d^2(K)}\bigr),}
\tag{12.3}
\]

\[
\boxed{
 \|H\|_{L_d^\infty(K)}
 \le H(d_-)
 +\Psi_g(D)
 \bigl(a\|Q\|_{L_d^2(K)}+\|f\|_{L_d^2(K)}\bigr).}
\tag{12.4}
\]

Pointwise,

\[
 H(d)\le e^{-g\tau}H(d_-)
 +a\Phi_g(\tau)\|Q\|_{L^\infty(d_-,d)}
 +\Phi_g(\tau)\|f\|_{L^\infty(d_-,d)}.
 \tag{12.5}
\]

Only the complete history of \(Q\) controls the response.  One can force
\(q\) to vanish at the terminal time after it was nonzero earlier, while the
Squire convolution remains nonzero.  Hence a terminal value \(Q(d_+)\)
alone cannot replace (12.3)--(12.5).

---

## 13. Conditional strong-kernel Squire transfer

For \(|c|\ge4\), let

\[
 \alpha=(|c|/4)^{-1/5},\qquad h_0=2T\alpha^2,
 \tag{13.1}
\]

and let \(\vartheta\in(0,1)\) be the R0.72X scalar block factor.  The scalar
Squire propagator is controlled by

\[
 K_j(\tau)=\min\left\{
 e^{-g\tau},
 e^{-\mu\tau}\vartheta^{\lfloor\tau/h_0\rfloor}
 \right\}.
 \tag{13.2}
\]

Put

\[
 A_\vartheta=\frac{2T}{1-\vartheta},
 \qquad
 B_\vartheta=\frac{2T}{1-\vartheta^2},
 \tag{13.3}
\]

\[
 \ell_j=\min\{g^{-1},A_\vartheta\alpha^2\},
 \qquad
 m_j=\min\{(2g)^{-1/2},\sqrt{B_\vartheta}\alpha\}.
 \tag{13.4}
\]

Then

\[
\boxed{
 \|H\|_{L^2}
 \le m_jH(d_-)
 +\ell_j\bigl(a\|Q\|_{L^2}+\|f\|_{L^2}\bigr),}
\tag{13.5}
\]

\[
\boxed{
 \|H\|_{L^\infty}
 \le H(d_-)
 +m_j\bigl(a\|Q\|_{L^2}+\|f\|_{L^2}\bigr).}
\tag{13.6}
\]

The explicit Squire payments are

\[
 \mathfrak S_{2,j}=a\ell_j,
 \qquad
 \mathfrak S_{\infty,j}=am_j.
 \tag{13.7}
\]

For \(\gamma\ne0\), (10.10) gives

\[
 \mathfrak S_{2,j}
 \le\frac{M_{1,K}|c|R_j}{\sqrt g}
 \min\{g^{-1},A_\vartheta\alpha^2\},
 \tag{13.8}
\]

\[
 \mathfrak S_{\infty,j}
 \le\frac{M_{1,K}|c|R_j}{\sqrt g}
 \min\{(2g)^{-1/2},\sqrt{B_\vartheta}\alpha\}.
 \tag{13.9}
\]

These are conditional on a history norm for \(Q\).  Scalar enhanced
dissipation alone does not make Squire transfer vanish.

For a zero-initial external Squire forcing, the R0.72Y transposition bounds
remain separate from the internal \(Q\)-source:

\[
 \|H[F_\eta]\|_{L_d^2L_x^2}
 \le \mu^{-1/2}C_\vartheta\alpha
 \|F_\eta\|_{L_d^2H^{-1}_\beta},
 \tag{13.10}
\]

\[
 \|H[F_\eta]\|_{L_d^2L_x^2}
 \le \mu^{-1/2}C_\vartheta\alpha^2
 \|F_\eta\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}.
 \tag{13.11}
\]

Standard \(H^{-1}\) forcing has no vanishing endpoint gain; the
semiclassical endpoint has one power of \(\alpha\).  These statements do not
change the internal Squire payment \(a\|Q\|\).

---

## 14. Damping-gap formula and equal-rate boundary

Suppose, in a declared norm,

\[
 Q(d)\le M_qe^{-\lambda_q\tau}Q(d_-),
 \tag{14.1}
\]

and the homogeneous Squire propagator is bounded by

\[
 M_\eta e^{-\lambda_\eta(d-s)}.
 \tag{14.2}
\]

Then

\[
\boxed{
 H(d)\le M_\eta e^{-\lambda_\eta\tau}H(d_-)
 +aM_\eta M_q
 \mathcal J_{\lambda_\eta,\lambda_q}(\tau)Q(d_-),}
\tag{14.3}
\]

where

\[
\boxed{
 \mathcal J_{a,b}(\tau)=
 \begin{cases}
 \dfrac{e^{-b\tau}-e^{-a\tau}}{a-b},&a\ne b,\\[6pt]
 \tau e^{-a\tau},&a=b.
 \end{cases}}
\tag{14.4}
\]

A nonzero damping gap costs \(a/|\lambda_\eta-\lambda_q|\).  At equal
rates the correct transient is \(a\tau e^{-\lambda\tau}\); replacing it by
a uniform spectral-gap denominator is false.

---

## 15. A closed fixed-row OS--Squire graph theorem

Assume the signed high-gap condition (3.2).  Define the raw Squire
coefficient

\[
 b_{\eta,K}
 =|\xi\Lambda|
 \sup_K\|M_{W_x}\mathcal L^{-1}\|
 \le\frac{|\xi\Lambda|M_{1,K}}g.
 \tag{15.1}
\]

Theorem 3.1 and (12.1) give, for homogeneous data,

\[
 \|q(d)\|_2\le e^{-\omega g\tau}\|q(d_-)\|_2,
 \tag{15.2}
\]

\[
\boxed{
 \|\eta(d)\|_2
 \le e^{-g\tau}\|\eta(d_-)\|_2
 +b_{\eta,K}\mathcal J_{g,\omega g}(\tau)
 \|q(d_-)\|_2.}
\tag{15.3}
\]

The forced spacetime version is

\[
 \|q\|_{L^2}
 \le\Psi_{\omega g}(D)\|q(d_-)\|
 +\Phi_{\omega g}(D)\|F_q\|_{L^2},
 \tag{15.4}
\]

\[
\boxed{
 \|\eta\|_{L^2}
 \le\Psi_g(D)\|\eta(d_-)\|
 +\Phi_g(D)
 \bigl(\|F_\eta\|_{L^2}+b_{\eta,K}\|q\|_{L^2}\bigr).}
\tag{15.5}
\]

Thus a fixed high-gap row has

\[
 q\in C(K;L^2)\cap L^2(K;D(\mathcal L^{1/2})),
 \tag{15.6}
\]

\[
 v=\mathcal L^{-1}q
 \in C(K;D(\mathcal L))
 \cap L^2(K;D(\mathcal L^{3/2})),
 \tag{15.7}
\]

and \(\eta\in C(K;L^2)\cap L^2(K;D(\mathcal L^{1/2}))\) under the
corresponding forcing assumptions.

This is the closed `fixedRowOSSquireGraphRegularity` statement.  Its input
contains \(q\in L^2\), which is stronger than finite kinetic energy.  The
conversion

\[
 \|u(d)\|_2^2
 \le\frac1\mu
 \left(g^{-1}\|q(d)\|_2^2+\|\eta(d)\|_2^2\right)
 \tag{15.8}
\]

retains row-dependent \(\mu^{-1}\), \(g^{-1}\), and \(|\xi\Lambda|\)
payments.  It is not a uniform physical velocity direct sum.

---

## 16. Exceptional orientations and sharpness

The exact partition is:

1. **\(\mu=0\):** \(\xi=\gamma=0\), so the OS--Squire inverse variables
   are invalid.  If \(\rho>0\), divergence forces \(u_2=0\); if \(\rho=0\),
   component lift-up must be treated directly.
2. **\(\xi=0,\gamma\ne0\):** the Squire source is exactly zero.
3. **\(\gamma=0,\xi\ne0\):** \(c=0\), so \(q\) solves heat, while the
   Squire source remains \(i\xi\Lambda W_x\mathcal L^{-1}q\).  This is the
   exact transverse lift-up boundary.
4. **\(0<|\xi/\gamma|\le1\):** the kinetic orientation factor satisfies
   \(\chi_j\le|\xi/\gamma|\).
5. **\(|\xi/\gamma|\ge1\):** \(\chi_j\le1\); the cost saturates at
   \(O(|\Lambda|)\), not infinity.

Instantaneous sharpness follows by taking \(\eta(d_0)=0\) and choosing
\(\mathcal L^{-1/2}q(d_0)\) along an approximate maximizing vector of
\(M_{W_x}\mathcal L^{-1/2}\):

\[
 H(d_0+\tau)=a_j(d_0)Q(d_0)\tau+o(\tau).
 \tag{16.1}
\]

At \(\gamma=\beta=0\), constant \(v_0\), the exact R0.72Y lift-up formula
gives

\[
 Q(d_2)=e^{-\xi^2\tau}|v_0|,
 \tag{16.2}
\]

\[
 H(d_2)=|\Lambda|\tau e^{-\xi^2\tau}
 \|W_x(d_2)v_0\|_2.
 \tag{16.3}
\]

Hence \(|\Lambda|\), the equal-rate factor \(\tau\), and the transverse
boundary cannot be deleted.

Any weighted norm that removes the triangular source must pay the same
parameter.  Conditionally, if both diagonal components decay at rate
\(\lambda\), then for \(0<\delta<\lambda\)

\[
 \mathcal N_{\delta,j}^2=H^2+w_{\delta,j}^2Q^2,
 \qquad
 w_{\delta,j}=\max\left\{1,\frac a{2\delta}\right\},
 \tag{16.4}
\]

obeys decay at rate \(\lambda-\delta\).  Since \(w_{\delta,j}\) grows with
\(|\Lambda|\), this is a parameter-dependent symmetrizer, not a uniformly
equivalent \(\Lambda\)-independent physical norm.

---

## 17. Complete class ledger

| Row class | Exact conclusion | Status |
|---|---|---|
| \(\Theta_K(c,\beta,\mu)<1\) | prefactor-one \(L^2_q\) decay and forced graph estimates | **CLOSED** |
| sufficient \(g\gtrsim|c|^{2/5}\) | explicit signed high-gap subclass | **CLOSED** |
| all \(g>0\), prefactor-one OS contraction | low- and high-mode witnesses obstruct it | **FALSE** |
| \(\beta=\mu=0\), abstract mean-zero OS | exact heat-tangent mode; no uniform scalar \(A_2\) block factor | **FALSE for strict contraction** |
| low-gap OS with transient prefactor | not decided by the witnesses | **OPEN** |
| any \(\mu>0\), declared \(Q\) history | exact orientation-paid Squire estimates | **CLOSED** |
| angle-uniform with explicit \(|\Lambda|\) | \(\chi_j\le1\) | **CLOSED** |
| bound from \(|c|\) alone through \(\gamma=0\) | transverse lift-up | **FALSE** |
| fixed high-gap OS--Squire graph tier | (15.2)--(15.7) | **CLOSED** |
| uniform kinetic-energy direct sum | row payments remain | **OPEN** |
| nonlinear convolution and vortex stretching | absent from this section | **OPEN** |

---

## 18. Primary-literature boundary

The literature search was bounded to primary sources through 2026-08-28.
It does not establish novelty or priority.

1. Te Li, Dongyi Wei, and Zhifei Zhang,
   [*Pseudospectral bound and transition threshold for the 3D Kolmogorov
   flow*](https://arxiv.org/abs/1801.05645), derive an exact OS--Squire
   triangular system and retain inverse streamwise-wavenumber payments in
   the Squire response.  Their stationary single-sine, integer-mode setting
   does not include a critical-point collision or continuous Bloch residue.
2. Soundar Jerome and Jean-Marc Chomaz,
   [*Extended Squire's transformation and its consequences on transient
   growth for a confined shear flow*](https://arxiv.org/html/1601.07598),
   exhibit the streamwise/spanwise orientation factor and the lift-up
   transient in the exact Squire transformation.  Their stationary bounded
   setting excludes the zero-streamwise singular boundary.
3. Hao Jia,
   [*Uniform linear inviscid damping and enhanced dissipation near monotonic
   shear flows in high Reynolds number regime (I)*](https://arxiv.org/abs/2207.10987),
   treats the Orr--Sommerfeld nonlocal term through limiting absorption and
   critical-layer analysis under strict monotonicity and a no-discrete-spectrum
   assumption.  This is not a collision theorem.
4. Ryan Beekie, Shan Chen, and Hao Jia,
   [*Uniform vorticity depletion and inviscid damping for periodic shear
   flows in the high Reynolds number regime*](https://arxiv.org/abs/2403.13104),
   treat periodic nonmonotone shears with fixed separated nondegenerate
   critical points and spectral assumptions.  A changing critical-point
   count is outside their hypotheses.
5. Wenting Wei, Zhifei Zhang, and Weiren Zhao,
   [*Linear inviscid damping and enhanced dissipation for the Kolmogorov
   flow*](https://arxiv.org/abs/1711.01822), handle a heat-decaying amplitude
   with an active nonlocal term, but the critical-point geometry stays fixed.
6. Maria Colombo, Michele Dolce, Riccardo Montalto, and Paolo Ventura,
   [*Long-wave instability of periodic shear flows for the 2D
   Navier--Stokes equations*](https://arxiv.org/html/2509.18070), prove that
   general stationary periodic shears can have an unstable long-wave OS
   eigenvalue.  Their result does not decide the present exact heat path,
   but it rules out treating weak streamwise rows as harmless by default.

I did not find a theorem in this search combining a time-dependent
critical-point collision, active OS feedback, Squire orientation,
continuous Bloch fibers, structured forcing, and a uniform physical-energy
direct sum.  “Not found in this search” is not a proof of global novelty.

---

## 19. Certificate and audit boundary

The deterministic certificate can check:

1. the commutators (2.4)--(2.5) and the sign in (2.8);
2. the Fourier coefficients (4.2) and matrix (4.3);
3. self-adjointness and finite Schur truncations with analytic tails;
4. the exact value (4.9) and the bound (4.8);
5. \(|c|=4\alpha^{-5}\Rightarrow |c|^{2/5}=4^{2/5}\alpha^{-2}\);
6. the two-mode formula (7.2), low-mode growth, and limit (7.6);
7. the tangent residual (8.1)--(8.3);
8. the scaled identity (9.3) and cubic limit (9.4);
9. kinetic recovery, \(\chi_j\le1\), and the lattice sum (11.2);
10. the kernel integrals, damping-gap formula, and exceptional partition;
11. exact agreement of the declared 15/10/8 CLOSED/FALSE/OPEN ledger across
    the report source and the two certificate routes; the public note retains
    the same status boundary for every claim it exposes.

It does not machine-prove:

1. infinite-dimensional evolution-family existence or Galerkin passage;
2. that a finite matrix truncation equals the full operator norm;
3. low-gap limiting absorption or a transient \(A_2\) propagator;
4. a uniform physical velocity direct sum;
5. any nonlinear Navier--Stokes estimate.

The formal figure is explanatory evidence, not a proof.

---

## 20. Research value and next theorem

R0.72Z changes the boundary in three precise ways.

First, pressure feedback is no longer a generic unresolved term: it has an
exact signed relative form and a scale-sharp high-gap threshold.  Second,
the failure below that threshold is not merely a weak estimate; explicit
two-mode data produce instantaneous growth, and the abstract tangent mode
exactly cancels scalar mixing.  Third, Squire orientation is now normalized
correctly: pure angle is bounded in kinetic energy, while background
amplitude and history payments remain unavoidable.

The direct value for the Clay problem remains low.  The work does not yet
control low-gap physical rows, sum them uniformly, estimate nonlinear row
convolution, close vortex stretching, or prove a continuation criterion.

The next minimal theorem is R0.73A:

\[
 \boxed{\text{separate the tangent/lift-up subspace and seek a low-gap
 OS propagator with an explicit transient prefactor.}}
 \tag{20.1}
\]

That theorem must include a frozen-time spectral audit for weak streamwise
rows and must not assume that scalar enhanced dissipation survives active
pressure feedback.
