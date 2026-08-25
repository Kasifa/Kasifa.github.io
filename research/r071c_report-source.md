# R0.71C — Signed refinement defects, discontinuous normalization, and viscous sign creation

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, Littlewood--Paley localization, and vortex
stretching

**Status:** exact partition theorem, finite Fourier certificates, and one
conditional continuation reduction; no unconditional regularity theorem and
no Millennium-problem claim

## 1. Direct decision

R0.71B left a precise question.  Its positive-output coefficient keeps the
sign that a BMO square loses, but no time-integrability estimate was known.
Could I first add signed outputs inside a scale or space--time node, and only
then square, so that cancellation propagates?

R0.71C gives a mostly negative answer to that static proposal.

1. Every additive signed-before-square partition ledger has an exact
   nonnegative refinement defect.  Coarsening hides positive mass; refining
   exposes it.  The cancellation is bookkeeping, not a free estimate.
2. The R0.71B normalization is discontinuous when an output strain mode
   crosses zero.  This happens along a three-mode family that converges in
   every fixed Sobolev space.
3. Viscosity can turn zero coarse signed work into positive work.  An exact
   smooth NSE initial trace gives

   \[
    W'(0)=12\nu\varepsilon^3+\frac{76}{5}\varepsilon^4>0.
    \tag{1.1}
   \]

4. A second exact family starts with the full fine coefficient (a_+=0),
   yet Stokes evolution and true NSE evolution make it positive immediately.
   Hence no homogeneous Gronwall law can propagate (a_+) from its initial
   value.

There is still a valid conditional reduction.  If the full nonlinear
injection into each output shell is summed with its sign before squaring, its
critical positive square controls enstrophy growth.  The missing estimate is
exactly the positive time variation of the shell energies.  Signed time-box
mass bounds it in the wrong direction.

The route therefore does not continue as a static signed state variable.  A
remaining admissible construction must keep transport, cutoff, and vertical
heat fluxes as explicit additive terms in a material parabolic tent.  Whether
those fluxes telescope below the known BMO/Besov threshold is open.

## 2. Setup and the R0.71B consumer

Work on the normalized three-torus.  For a real divergence-free vorticity
field,

\[
 \widehat u(k)=\frac{i\,k\times\widehat\omega(k)}{|k|^2},
 \qquad
 \widehat S(k)
 =\frac{i}{2}
 \left(k\otimes\widehat u(k)+\widehat u(k)\otimes k\right).
 \tag{2.1}
\]

Let (Q) be the frame covariance used in R0.71B and let (K_+) contain one
representative of each pair ({k,-k}).  Define

\[
 w_k=2\operatorname{Re}
 \left(\overline{\widehat S(k)}:\widehat Q(k)\right),
 \qquad
 \mathfrak P_Q=\sum_{k\in K_+}w_k,
 \tag{2.2}
\]

\[
 \mathcal T_+^2
 =\sum_{\widehat S(k)\ne0}
 \frac{(w_k^+)^2}
 {4|k|^2|\widehat S(k)|_F^2},
 \qquad
 a_+=\frac{\mathcal T_+^2}{\|\omega\|_2^2}.
 \tag{2.3}
\]

The exact consumer is

\[
 (\mathfrak P_Q)_+
 \le \|\nabla\omega\|_2\mathcal T_+
 \le \frac\nu4\|\nabla\omega\|_2^2
 +\nu^{-1}a_+\|\omega\|_2^2.
 \tag{2.4}
\]

R0.71C does not alter (2.4).  It asks whether the coefficient on its right
can be organized into a dynamically propagated signed hierarchy.

## 3. Exact partition theorem

Let (I) be a finite index set.  Give each index a signed work (w_i\in
\mathbb R) and a positive weight (d_i>0).  For a partition (\Pi) of
(I), put

\[
 W_B=\sum_{i\in B}w_i,
 \qquad
 D_B=\sum_{i\in B}d_i,
 \tag{3.1}
\]

\[
 \boxed{
 E_\Pi=\sum_{B\in\Pi}\frac{(W_B^+)^2}{D_B}.}
 \tag{3.2}
\]

### Theorem 3.1 — consumer and refinement monotonicity

For every partition,

\[
 \left(\sum_{i\in I}w_i\right)^+
 \le
 \left(\sum_{i\in I}d_i\right)^{1/2}E_\Pi^{1/2}.
 \tag{3.3}
\]

If (\Pi') refines (\Pi), then

\[
 E_\Pi\le E_{\Pi'}.
 \tag{3.4}
\]

**Proof.**  Positive-part subadditivity and weighted Cauchy give

\[
 \left(\sum_{B\in\Pi}W_B\right)^+
 \le\sum_{B\in\Pi}W_B^+
 \le
 \left(\sum_BD_B\right)^{1/2}
 \left(\sum_B\frac{(W_B^+)^2}{D_B}\right)^{1/2}.
 \tag{3.5}
\]

For one parent (B) split into children (C), the same argument gives

\[
 \frac{(W_B^+)^2}{D_B}
 \le\sum_{C\subset B}\frac{(W_C^+)^2}{D_C}.
 \tag{3.6}
\]

Summing over parents proves (3.4).  (\square)

For a binary tree define

\[
 \delta_v=E_{\operatorname{children}(v)}-E_v\ge0.
 \tag{3.7}
\]

Then the tree telescopes exactly:

\[
 E_{\operatorname{leaves}}=E_{\operatorname{root}}
 +\sum_{v\ \operatorname{internal}}\delta_v.
 \tag{3.8}
\]

When two child works (x,y) are both positive and their weights are (d,e),

\[
 \delta
 =\frac{x^2}{d}+\frac{y^2}{e}
 -\frac{(x+y)^2}{d+e}
 =\frac{(ex-dy)^2}{de(d+e)}.
 \tag{3.9}
\]

The coarsest root ledger is the positive net-production quotient.  The
finest Fourier-output ledger is the R0.71B (\mathcal T_+^2).  Formula (3.8)
classifies the difference: the fine coefficient equals the root coefficient
plus nonnegative cancellation and weight-mismatch defects.  A proposed
localization must control those defects; nesting alone does not remove them.

This theorem applies to additive partitions with additive positive weights.
It does not cover a solution-dependent nonlinear transform whose evolution
has an additional PDE flux identity.

## 4. The same-output normalization is discontinuous

Take

\[
 p=(1,1,0),\qquad q=(1,-1,0),\qquad k=p+q=(2,0,0),
 \tag{4.1}
\]

\[
 a=e_3,\qquad
 b=\frac{e_1+e_2}{\sqrt2},\qquad
 c=-e_2,
 \tag{4.2}
\]

and

\[
 \omega_\eta(x)
 =Aa\cos(p\cdot x)+Bb\cos(q\cdot x)
 +\eta c\cos(k\cdot x),
 \qquad A,B,\eta>0.
 \tag{4.3}
\]

All three modes are divergence free.  Since (|p|=|q|), every real-even
radial Parseval frame has response (\Gamma(p,q)=1).  At output (k),

\[
 \widehat S_\eta(k)
 =\frac\eta4(e_1\otimes e_3+e_3\otimes e_1),
 \tag{4.4}
\]

\[
 \widehat Q_\eta(k)
 =\frac{AB}{4}(a\otimes b+b\otimes a),
 \tag{4.5}
\]

so

\[
 w_k=\frac{\sqrt2}{8}AB\eta,
 \qquad
 |\widehat S_\eta(k)|_F^2=\frac{\eta^2}{8}.
 \tag{4.6}
\]

For every (\eta>0), the single output contribution is therefore

\[
 \frac{(w_k^+)^2}
 {4|k|^2|\widehat S_\eta(k)|_F^2}
 =\boxed{\frac{A^2B^2}{64}},
 \tag{4.7}
\]

independent of (\eta).  At (\eta=0), the denominator vanishes and the
R0.71B convention assigns zero to the term.  Meanwhile

\[
 Y_\eta=\frac{A^2+B^2+\eta^2}{2},
 \qquad
 D_\eta=A^2+B^2+2\eta^2
 \tag{4.8}
\]

are continuous, and (\omega_\eta\to\omega_0) in every fixed (H^s).  Thus

\[
 a_+(\omega_0)=0,
 \qquad
 \liminf_{\eta\downarrow0}a_+(\omega_\eta)
 \ge
 \frac{A^2B^2}{32(A^2+B^2)}>0.
 \tag{4.9}
\]

This is an exact algebraic discontinuity, not a numerical instability.  Any
candidate that divides a positive squared packet by the energy of the same
packet and sets the zero denominator to zero must address this zero set.  A
different denominator may repair continuity, but it changes both scaling and
the exact consumer.

## 5. A same-radius node hides positive mass

The next witness uses direct Fourier coefficients at the listed positive
frequencies and the same real coefficients at their negatives.

| output | output vorticity | first input and coefficient | second input and coefficient |
|---|---|---|---|
| (k_1=(2,0,0)) | (e_2) | (p_1=(1,1,0)), ((1,-1,0)) | (q_1=(1,-1,0)), (-e_3) |
| (k_2=(0,0,2)) | (e_1) | (p_2=(2,0,1)), ((-1,0,2)) | (q_2=(-2,0,1)), (e_2/2) |

The inputs in each row have equal radius.  The outputs have the same radius
(|k_1|=|k_2|=2).  Exhaustive exact enumeration finds 24 ordered zero-sum
resonances, 12 in each triad and no cross-triad resonance.

For the full-response tensor (Q=\omega\otimes\omega),

\[
 w_1=2,\qquad w_2=-2,
 \tag{5.1}
\]

and

\[
 d_i=4|k_i|^2|\widehat S(k_i)|_F^2=8.
 \tag{5.2}
\]

The root node (B=\{k_1,k_2\}) therefore has

\[
 E_{\rm root}(0)=0,
 \qquad
 E_{\rm leaves}(0)=\frac12.
 \tag{5.3}
\]

The missing (1/2) is exactly the initial refinement defect.

## 6. Stokes damping creates positive coarse work

Under linear Stokes evolution,

\[
 w_1(t)=2e^{-8\nu t},
 \qquad
 w_2(t)=-2e^{-14\nu t},
 \tag{6.1}
\]

while

\[
 d_1(t)=d_2(t)=8e^{-8\nu t}.
 \tag{6.2}
\]

Hence

\[
 W_B(t)=2(e^{-8\nu t}-e^{-14\nu t})>0
 \qquad(t>0),
 \tag{6.3}
\]

although (W_B(0)=0).  At

\[
 t_1=\frac{\log2}{6\nu},
 \tag{6.4}
\]

the exact ledger is

\[
 E_{\rm root}(t_1)=2^{-16/3},
 \qquad
 E_{\rm leaves}(t_1)=2^{-7/3},
 \tag{6.5}
\]

\[
 \delta(t_1)=7\,2^{-16/3}.
 \tag{6.6}
\]

The cause is simple but decisive.  The two output strains have the same heat
rate, but their covariance inputs have radii squared 2 and 5.  The negative
input pair decays faster, revealing the positive pair.  Signed output sums do
not satisfy a heat maximum principle.

## 7. The sign creation persists for true NSE

Scale the initial vorticity in Section 5 by (\varepsilon>0).  In Fourier
variables the vorticity equation is

\[
 \partial_t\widehat\omega(k)
 =-\nu|k|^2\widehat\omega(k)
 +i\sum_{p+q=k}
 \left[
  (\widehat\omega(p)\cdot q)\widehat u(q)
  -(\widehat u(p)\cdot q)\widehat\omega(q)
 \right].
 \tag{7.1}
\]

The exact derivative of the two selected works is

\[
 w_1'(0)=-16\nu\varepsilon^3+6\varepsilon^4,
 \tag{7.2}
\]

\[
 w_2'(0)=28\nu\varepsilon^3
 +\frac{46}{5}\varepsilon^4.
 \tag{7.3}
\]

Therefore

\[
 \boxed{
 W_B'(0)=12\nu\varepsilon^3
 +\frac{76}{5}\varepsilon^4>0.}
 \tag{7.4}
\]

The quartic audit must include modes generated instantaneously by the NSE
quadratic term.  The independent reconstruction found 50 nonzero generated
frequencies that can pair back with the original support in
(\partial_tQ(k)).  Keeping only derivatives on the initial support gives a
wrong quartic coefficient.  Two implementations include the full generated
support and agree on (7.2)--(7.4).

Since the trigonometric polynomial is smooth, local smooth NSE evolution
exists.  Equation (7.4) implies (W_B(t)>0) for sufficiently small positive
time.  This is a true NSE initial-trace result, not a numerical time step.

## 8. The full fine coefficient can also start at zero

The preceding node had latent fine mass at (t=0).  A second family removes
that qualification.

For (M\ge4), set

\[
 n=(1,1,0),\quad
 c=\frac{(1,-1,0)}{\sqrt2},\quad
 p_M=(M,-M-1,0),\quad
 q_M=(-M-1,M,0),
 \tag{8.1}
\]

\[
 a=e_3,\quad
 b_M=\frac{(M,M+1,0)}{\sqrt{2M^2+2M+1}},\quad
 h_M=\frac{2M+1}{\sqrt2\sqrt{2M^2+2M+1}}.
 \tag{8.2}
\]

Use (M=8,64) and define

\[
 \begin{aligned}
 \Omega={}&c\cos(n\cdot x)
 +h_{64}a\cos(p_8\cdot x)
 +b_8\cos(q_8\cdot x)\\
 &+h_8a\cos(p_{64}\cdot x)
 -b_{64}\cos(q_{64}\cdot x).
 \end{aligned}
 \tag{8.3}
\]

The two low-output works are

\[
 \frac{h_8h_{64}}4,
 \qquad
 -\frac{h_8h_{64}}4.
 \tag{8.4}
\]

Strict response separation leaves no other nonzero covariance-work output.
Thus for every amplitude (\delta>0),

\[
 \mathcal T_+(\delta\Omega)=a_+(\delta\Omega)=0.
 \tag{8.5}
\]

Let

\[
 c_0=\frac{h_8h_{64}}4
 =\frac{2193\sqrt{1206545}}{9652360}.
 \tag{8.6}
\]

Under Stokes evolution, the low-output work is

\[
 w_n^H(t)
 =\delta^3c_0e^{-2\nu t}
 \left(e^{-290\nu t}-e^{-16642\nu t}\right)>0
 \quad(t>0).
 \tag{8.7}
\]

Its derivative is

\[
 (w_n^H)'(0)
 =\nu\delta^3
 \frac{4482492\sqrt{1206545}}{1206545}>0.
 \tag{8.8}
\]

For the orthogonal radial-sphere Parseval response
(\Gamma(r,s)=\mathbf1_{|r|=|s|}), the full true-NSE derivative is also
exact:

\[
 \boxed{
 w_n'(0)
 =\frac{2193\delta^3
 \left(2193\delta+32704\sqrt{1206545}\,\nu\right)}
 {19304720}>0.}
 \tag{8.9}
\]

Its viscous cubic part is (8.8), and its nonlinear quartic part is

\[
 \frac{4809249}{19304720}\delta^4>0.
 \tag{8.10}
\]

For the fixed smooth radial frame used in the project, the same initial
cancellation and positive cubic heat term remain exact.  The frame-dependent
NSE correction is finite and (O(\delta^4)).  Therefore the positive cubic
term dominates for sufficiently small (\delta), regardless of the sign of
that quartic correction.

It follows that (a_+(0)=0) and (a_+(t)>0) for a short positive interval.
This rules out any homogeneous propagation law of the form

\[
 a_+'(t)\le F(Y(t),D(t))a_+(t)
 \tag{8.11}
\]

or

\[
 a_+(t)\le a_+(0)
 \exp\left(\int_0^tF(Y,D)\,ds\right),
 \tag{8.12}
\]

whenever (F(Y,D)) is locally integrable.  It does not rule out an estimate
with an additive heat or flux source.

## 9. A valid shell-injection conditional reduction

There is a more equation-aligned signed-before-square quantity.  Let
(\{T_\alpha\}) be a real-even scalar Parseval output frame and set

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Y_\alpha=\|\Omega_\alpha\|_2^2,
 \qquad
 D_\alpha=\|\nabla\Omega_\alpha\|_2^2.
 \tag{9.1}
\]

Define the full nonlinear injection into the shell by

\[
 b_\alpha
 =\left\langle
 T_\alpha\omega,
 T_\alpha(S\omega-u\cdot\nabla\omega)
 \right\rangle.
 \tag{9.2}
\]

Applying (T_\alpha) to the vorticity equation gives the exact identity

\[
 \frac12Y_\alpha'+\nu D_\alpha=b_\alpha.
 \tag{9.3}
\]

Parseval and global transport cancellation give

\[
 \sum_\alpha Y_\alpha=Y=\|\omega\|_2^2,
 \qquad
 \sum_\alpha D_\alpha=D=\|\nabla\omega\|_2^2,
 \tag{9.4}
\]

\[
 \sum_\alpha b_\alpha
 =\int_{\mathbb T^3}S:\omega\otimes\omega\,dx
 =\mathfrak P.
 \tag{9.5}
\]

Put

\[
 \Theta_{\rm sb,+}^2
 =\sum_{D_\alpha>0}\frac{(b_\alpha^+)^2}{D_\alpha},
 \qquad
 A_{\rm sb,+}=\frac{\Theta_{\rm sb,+}^2}{Y}.
 \tag{9.6}
\]

Then

\[
 \mathfrak P_+
 \le\sqrt D\,\Theta_{\rm sb,+}
 \le\frac\nu2D+\frac{1}{2\nu}A_{\rm sb,+}Y.
 \tag{9.7}
\]

Using (Y'/2+\nu D=\mathfrak P),

\[
 Y'+\nu D\le\nu^{-1}A_{\rm sb,+}Y.
 \tag{9.8}
\]

### Conditional theorem 9.1

Let (u) be a maximal periodic (H^1) strong solution on ([0,T_*)).  If

\[
 \int_0^{T_*}A_{\rm sb,+}(t)\,dt<\infty,
 \tag{9.9}
\]

then (Y) remains bounded, (D\in L^1(0,T_*)), and the solution extends
past (T_*).

Indeed, Gronwall applied to (9.8) gives

\[
 Y(t)\le Y(0)
 \exp\left(\nu^{-1}\int_0^tA_{\rm sb,+}(s)\,ds\right).
 \tag{9.10}
\]

Under NSE scaling, (Y_\alpha\), (D_\alpha), and (b_\alpha) scale like
(\lambda), (\lambda^3), and (\lambda^3), respectively.  Thus
(A_{\rm sb,+}) scales like (\lambda^2), and its time integral is
critical.

This theorem is an exact conditional reduction.  It is not yet a new
regularity result because (9.9) has not been derived from an independent
unconditional estimate.

## 10. Signed time boxes control the wrong side

For a time interval (I=[t_0,t_1]), (9.3) gives

\[
 \beta_{\alpha,I}:=\int_Ib_\alpha\,dt
 =\frac12\left(Y_\alpha(t_1)-Y_\alpha(t_0)\right)
 +\nu\int_ID_\alpha\,dt.
 \tag{10.1}
\]

However, Cauchy gives

\[
 \frac{(\beta_{\alpha,I}^+)^2}
 {\int_ID_\alpha\,dt}
 \le
 \int_I\frac{(b_\alpha^+)^2}{D_\alpha}\,dt.
 \tag{10.2}
\]

The signed box mass is a lower bound for the positive square variation that
the consumer needs, not an upper bound.

This direction cannot be reversed using only integrated energy data.  As an
abstract one-shell path on (0\le t\le2\pi), take

\[
 Y_N(t)=1+\epsilon\sin Nt,
 \qquad
 D_N(t)=\kappa^2Y_N(t),
 \qquad
 b_N(t)=\frac12Y_N'(t)+\nu D_N(t),
 \tag{10.3}
\]

with (0<\epsilon<1) and integer (N).  The integrals of (Y_N) and
(D_N), and the full signed mass (\int b_N), are independent of (N),
but

\[
 \int_0^{2\pi}\frac{(b_N^+)^2}{D_N}\,dt
 \gtrsim_{\epsilon,\nu,\kappa}N^2.
 \tag{10.4}
\]

This is not an NSE counterexample.  It proves only that shell energy
integrals and signed telescoping do not contain the needed positive temporal
variation.  A successful estimate must use additional NSE cross-scale
dynamics.

## 11. Local fluxes that cannot be omitted

For a Fourier multiplier (T_j),

\[
 (\partial_t+u\cdot\nabla-\nu\Delta)T_j\omega
 =T_j(S\omega)+[u\cdot\nabla,T_j]\omega.
 \tag{11.1}
\]

In Fourier variables,

\[
 \widehat{[u\cdot\nabla,T_j]\omega}(k)
 =i\sum_{\ell+m=k}
 (\widehat u(\ell)\cdot m)
 \left(m_j(m)-m_j(k)\right)\widehat\omega(m).
 \tag{11.2}
\]

For a cutoff (\eta_r(x)=1+\rho\cos(r\cdot x)) and one mode
(f=ae^{ik\cdot x}),

\[
 \begin{aligned}
 [T_j,\eta_r]f={}&\frac\rho2
 \left(m_j(k+r)-m_j(k)\right)ae^{i(k+r)\cdot x}\\
 &+\frac\rho2
 \left(m_j(k-r)-m_j(k)\right)ae^{i(k-r)\cdot x}.
 \end{aligned}
 \tag{11.3}
\]

At the bottom layer of a parabolic tent, where
(|r|\simeq|k|\simeq2^j), there is no small multiplier difference.  Scaling
((k,r,j)\mapsto(2^Lk,2^Lr,j+L)) preserves this order-one leakage.

A correct local balance must therefore retain:

- transport--filter commutator;
- boundary flux through the spatial cutoff;
- vertical heat flux and viscous product terms;
- pressure-Hessian and strain--covariance gradient terms.

If fixed spatial boxes are used while nonzero mean velocity is allowed, a
Galilean transform can change the local time derivative without changing
global energy or enstrophy.  The project uses the zero-mean Biot--Savart
gauge, but a general formulation should either fix that gauge, move boxes
with the mean flow, or keep the transport boundary flux.

## 12. Literature boundary

The primary-source audit found no theorem deriving (9.9), or the R0.71B
(a_+\in L^1_t), from Leray energy data.

- The positive middle-strain-eigenvalue criterion is physical-space and
  conditional.
- BMO, dyadic-BMO, Besov, and positive Carleson estimates lose the Fourier
  output sign.
- The dynamic dissipation-wavenumber framework is the closest existing
  scaffold, but its regularity-side low-mode coefficient is already an
  assumed (L^1_t) quantity.
- Localized large-data estimates keep flux and boundary terms explicitly.

Dimensionally, (a_+) scales like inverse time while the dissipation
wavenumber (\Lambda) scales like inverse length.  A compatible comparison
would involve (\nu\Lambda^2), not (\Lambda).  The unconditional
(\Lambda\in L^1_t) result does not make (\nu\Lambda^2) integrable.

Full source-by-source boundaries are recorded in
`research/r071c_literature_audit.md`.

## 13. Acceptance table and route decision

| Gate | Exact result | Decision |
|---|---|---|
| R0.71A same-covariance sign pair | The positive-output coefficient still distinguishes the two signs | Passed, but not sufficient |
| R0.71B same-low fan | Fine square packing cannot recover a same-sign (\ell^1) total | Obstruction remains |
| R0.71B shared-high fan | Coarse accumulation pays root-tent-size packing | No free improvement over positive packing |
| Three-mode zero-strain family | (a_+) jumps under strong Sobolev convergence | Reject same-output zero-denominator state variable as a continuous propagated quantity |
| Same-radius two-triad node | Stokes and true NSE create positive coarse work from zero | Reject heat-monotone signed partial sums |
| (M=8,64) balanced family | True NSE creates (a_+>0) from (a_+(0)=0) | Reject homogeneous Gronwall propagation |
| Full shell injection (A_{\rm sb,+}) | Exact scale-critical conditional continuation theorem | Valid reduction; time integrability unproved |
| Signed time-box mass | Cauchy points from box mass toward positive variation | Insufficient without a new PDE flux estimate |

### What is proved

- an exact refinement-defect theorem for every finite additive signed
  partition;
- an exact discontinuity family for the R0.71B normalization;
- exact Stokes and true-NSE sign-creation witnesses;
- a scale-critical shell-injection conditional continuation reduction;
- precise leakage terms that a local balance must retain.

### What is not proved

- no divergence or convergence theorem for (\int a_+dt) along arbitrary
  NSE solutions;
- no unconditional estimate for (A_{\rm sb,+});
- no equivalence theorem between every signed tent and BMO;
- no exclusion of adaptive material localization with explicit fluxes;
- no singularity, global regularity theorem, or solution of the Millennium
  problem.

## 14. Next justified gate: R0.71D

R0.71D should test one object only: a **flux-balanced material parabolic
tent**.  Its local identity must include horizontal transport, bottom-layer
cutoff commutator, and vertical heat flux.  The acceptance condition is an
exact telescoping estimate for the refinement defect using a quantity that is
independently propagated and strictly below known sufficient BMO/Besov or
dissipation-wavenumber assumptions.

The route stops immediately if:

1. the fluxes are bounded only by an already sufficient continuation norm;
2. a bottom-layer commutator is discarded as lower order;
3. the estimate again divides by a packet that may vanish without a uniform
   stabilizing denominator;
4. the argument assumes the positive time variation it is meant to prove.

The exact no-go results in this section are potentially useful as a compact
research note about signed localization design.  They are not close to a
proof of global regularity.  Their value is narrower: they remove a plausible
but structurally false propagation mechanism and identify the flux term that
the next construction must pay.
