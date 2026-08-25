# R0.71N — The complete fixed-cell scalar has an exact square--residual form, but local filtered enstrophy cancels the apparent positive square

## Abstract

R0.71M left one finite question.  If the complete normalized projective scalar

\[
 z_Q=\frac{B_Q}{\sqrt{Yd_Q}},
 \qquad
 \mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q
\]

is expanded before any positive part or rowwise absolute value is taken, do
the three derivatives \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) create a second
coercive scalar fusion?

This release gives a finite answer for fixed cells.  The nominal parabolic
rate cancels exactly between the radial field row and the projective
denominator row.  The remaining source first admits the exact decomposition

\[
 \mathcal J_Q
 =\frac{\mathcal P_Q^\square+\mathfrak R_Q}{\sqrt{Yd_Q}},
 \qquad
 \mathcal P_Q^\square
 =\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2\ge0.
\]

However, \(\mathfrak R_Q\) contains the filtered Lamb acceleration
\(\langle G_{j,t},\chi_QW_j\rangle\).  Substituting the local filtered-
enstrophy identity shows that this acceleration contains the negative of the
same signed pairing used to create \(\mathcal P_Q^\square\).  The positive
square therefore cancels exactly.  What remains is

\[
 \mathcal J_Q
 =\frac{
 e_{Q,tt}+\nu(D_Q^\chi)_t
 +\nu\kappa_j^2(e_{Q,t}+\nu D_Q^\chi)
 -\frac12(e_{Q,t}+\nu D_Q^\chi)
  \left(Y_t/Y+d_{Q,t}/d_Q\right)}
 {\sqrt{Yd_Q}}.
\]

This is an explicit signed second-jet residual, not a new positive payment.
A standalone alias-safe finite Fourier calculation evaluates genuine smooth
NSE initial jets and finds both signs of \(\mathcal J_Q\) while \(z_Q>0\).
That calculation is a deterministic sign diagnostic, not a time-stepping
argument or a regularity theorem.

The fixed-cell second-fusion candidate is therefore closed in its checked
form.  The result does not exclude a different NSE-specific signed estimate,
and it does not control denominator faces, refresh atoms, or moving cells.

## 0. Claim boundary

All exact identities below are stated for a classical, zero-mean,
incompressible solution on the normalized periodic torus, one fixed
translation-invariant real-even scalar annular filter, and one fixed
time-independent nonnegative smooth cutoff.  They hold on an open time
component where

\[
 Y(t)>0,\qquad d_Q(t)>0.
\]

The projector is the orthogonal projector in the real Hilbert space
\(L^2(\mathbb T^3;\mathbb R^3)\).  It is not a pointwise matrix.  The scalar
\(z_Q\) is a normalized pairing, not a correlation coefficient or an angle:
its denominator contains \(\sqrt Y\), not \(\|F_j\|_2\), so no universal
bound \(|z_Q|\le1\) is asserted.

This release proves none of the following:

1. a sign or Leray-energy bound for the second-jet residual;
2. an impossibility theorem for every possible signed NSE estimate;
3. control of denominator-zero faces, refresh atoms, or moving cutoffs;
4. an infinite frame--cell identity or a weak-solution limit;
5. a continuation criterion, finite-time singularity, or global regularity;
6. originality or priority beyond the bounded comparison in Section 10;
7. a solution of the Millennium problem.

## 1. Fixed-cell notation

Work on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) with normalized Haar
measure.  Set

\[
 \omega=\operatorname{curl}u,
 \qquad
 L=\mathbb P(u\times\omega),
 \qquad
 Y=\|\omega\|_2^2.
 \tag{1.1}
\]

The velocity and vorticity equations are

\[
 u_t=L+\nu\Delta u,
 \qquad
 \omega_t=\operatorname{curl}L+\nu\Delta\omega.
 \tag{1.2}
\]

For one scalar annular multiplier \(T_j\), write

\[
 F_j=T_jL,
 \qquad
 W_j=T_j\omega,
 \qquad
 G_j=\operatorname{curl}F_j.
 \tag{1.3}
\]

For a fixed nonnegative cutoff \(\chi_Q\), let

\[
 \mathsf A_QV=\operatorname{curl}(\chi_QV),
 \qquad
 C_Q=\mathsf A_QW_j,
 \qquad
 d_Q=\|C_Q\|_2^2,
 \qquad
 r_Q=\sqrt{d_Q},
 \tag{1.4}
\]

\[
 B_Q=\langle F_j,C_Q\rangle,
 \qquad
 E_Q=C_Q/r_Q,
 \qquad
 P_Q=I-E_Q\otimes E_Q,
 \qquad
 z_Q=\frac{B_Q}{\sqrt{Yd_Q}}.
 \tag{1.5}
\]

Put

\[
 \lambda_j=\nu\kappa_j^2,
 \qquad
 H_j=(\Delta+\kappa_j^2)W_j,
 \qquad
 S_j=G_j+\nu H_j,
 \tag{1.6}
\]

\[
 N_j=F_{j,t}+\lambda_jF_j,
 \qquad
 M_Q=C_{Q,t}+\lambda_jC_Q=\mathsf A_QS_j.
 \tag{1.7}
\]

The complete signed source from R0.71I--M is

\[
 \mathcal J_Q=z_{Q,t}+\lambda_jz_Q.
 \tag{1.8}
\]

## 2. Main theorem

### Theorem 2.1 — exact full-scalar fusion and second-jet boundary

Assume the setup of Section 1 on a time component where \(Y>0\) and
\(d_Q>0\).  Define

\[
 I_Q=\int\chi_QG_j\cdot(G_j+\nu H_j),
 \tag{2.1}
\]

\[
 \mathcal P_Q^\square
 =\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2,
 \tag{2.2}
\]

and the local filtered-enstrophy state and its signed diffusion form by

\[
 e_Q=\frac12\int\chi_Q|W_j|^2,
 \tag{2.3}
\]

\[
 D_Q^\chi
 =\int\chi_Q|\nabla W_j|^2
 -\frac12\int(\Delta\chi_Q)|W_j|^2
 =-\langle\chi_QW_j,\Delta W_j\rangle.
 \tag{2.4}
\]

Then the following statements hold exactly.

#### (i) Complete derivative identity

\[
 \boxed{
 \mathcal J_Q
 =\frac{B_{Q,t}+\lambda_jB_Q}{\sqrt{Yd_Q}}
 -\frac{B_Q}{2\sqrt{Yd_Q}}
  \left(\frac{Y_t}{Y}+\frac{d_{Q,t}}{d_Q}\right).}
 \tag{2.5}
\]

The three-dimensional global enstrophy derivative appearing here is

\[
 \boxed{
 Y_t=2\langle\omega,\operatorname{curl}L\rangle
 -2\nu\|\nabla\omega\|_2^2.}
 \tag{2.6}
\]

It is not a pure dissipation identity.

#### (ii) Exact nominal-rate cancellation

The R0.71M radial projective identity gives

\[
 \langle P_QF_j,P_QM_Q\rangle
 =I_Q-\frac{B_Q}{d_Q}
 \left(\frac12d_{Q,t}+\lambda_jd_Q\right).
 \tag{2.7}
\]

Substituting (2.7) into the full normalized field--tangent formula cancels
\(+\lambda_jz_Q\) from \(N_j\) against \(-\lambda_jz_Q\) from the
projective denominator row.  No nominal damping is silently counted twice.

#### (iii) Exact square--residual form

\[
 \boxed{
 \mathcal J_Q
 =\frac{\mathcal P_Q^\square+\mathfrak R_Q}
 {\sqrt{Yd_Q}},}
 \tag{2.8}
\]

where

\[
 \boxed{
 \mathfrak R_Q
 =\langle G_{j,t},\chi_QW_j\rangle
 -\frac{\nu^2}{4}\int\chi_Q|H_j|^2
 -\frac{B_Q}{2}
  \left(\frac{Y_t}{Y}+\frac{d_{Q,t}}{d_Q}\right).}
 \tag{2.9}
\]

Because \(\chi_Q\ge0\), \(\mathcal P_Q^\square\ge0\).  Equation (2.8)
does not imply \(\mathcal J_Q\ge0\), because \(\mathfrak R_Q\) is signed.

#### (iv) Local filtered-enstrophy fusion

The numerator satisfies

\[
 \boxed{B_Q=e_{Q,t}+\nu D_Q^\chi.}
 \tag{2.10}
\]

Moreover,

\[
 \langle G_{j,t},\chi_QW_j\rangle
 =e_{Q,tt}+\nu(D_Q^\chi)_t-I_Q
 +\lambda_j(e_{Q,t}+\nu D_Q^\chi).
 \tag{2.11}
\]

Since

\[
 I_Q=\mathcal P_Q^\square
 -\frac{\nu^2}{4}\int\chi_Q|H_j|^2,
 \tag{2.12}
\]

the positive square in (2.8) cancels exactly against the same pairing inside
(2.11).  Hence

\[
 \boxed{
 \mathcal J_Q
 =\frac{\mathcal K_Q}{\sqrt{Yd_Q}},}
 \tag{2.13}
\]

with the explicit signed second-jet residual

\[
 \boxed{
 \begin{aligned}
 \mathcal K_Q={}&e_{Q,tt}+\nu(D_Q^\chi)_t
 +\lambda_j(e_{Q,t}+\nu D_Q^\chi)\\
 &-\frac12(e_{Q,t}+\nu D_Q^\chi)
 \left(\frac{Y_t}{Y}+\frac{d_{Q,t}}{d_Q}\right).
 \end{aligned}}
 \tag{2.14}
\]

Equation (2.14) is the finite verdict.  The checked substitution produces no
independent coercive quadratic term.  It does not prove that \(\mathcal K_Q\)
cannot be controlled by some other NSE-specific signed mechanism.

## 3. Proof of the complete derivative identity

Differentiate \(z_Q=B_Q(Yd_Q)^{-1/2}\):

\[
 z_{Q,t}
 =\frac{B_{Q,t}}{\sqrt{Yd_Q}}
 -\frac{z_Q}{2}
 \left(\frac{Y_t}{Y}+\frac{d_{Q,t}}{d_Q}\right).
 \tag{3.1}
\]

Adding \(\lambda_jz_Q\) proves (2.5).

From (1.2),

\[
 \begin{aligned}
 Y_t
 &=2\langle\omega,\omega_t\rangle\\
 &=2\langle\omega,\operatorname{curl}L\rangle
 +2\nu\langle\omega,\Delta\omega\rangle,
 \end{aligned}
 \tag{3.2}
\]

and periodic integration by parts proves (2.6).  The first term is the
three-dimensional vortex-stretching contribution.  Deleting it would import
a two-dimensional identity into the three-dimensional problem.

The product rule also gives

\[
 B_{Q,t}
 =\langle F_{j,t},C_Q\rangle
 +\langle F_j,C_{Q,t}\rangle.
 \tag{3.3}
\]

Because curl is self-adjoint on periodic \(L^2\) and \(\chi_Q\) is fixed,

\[
 \langle F_{j,t},C_Q\rangle
 =\langle G_{j,t},\chi_QW_j\rangle.
 \tag{3.4}
\]

Also

\[
 W_{j,t}=G_j+\nu\Delta W_j=S_j-\lambda_jW_j,
 \tag{3.5}
\]

so

\[
 \begin{aligned}
 \langle F_j,C_{Q,t}\rangle
 &=\langle G_j,\chi_QW_{j,t}\rangle\\
 &=I_Q-\lambda_jB_Q.
 \end{aligned}
 \tag{3.6}
\]

Consequently

\[
 \boxed{
 B_{Q,t}+\lambda_jB_Q
 =\langle G_{j,t},\chi_QW_j\rangle+I_Q.}
 \tag{3.7}
\]

Equation (3.7) is the bridge between (2.5) and (2.8).

## 4. Proof of the nominal-rate and projective cancellation

Since

\[
 \langle C_Q,M_Q\rangle
 =\frac12d_{Q,t}+\lambda_jd_Q,
 \tag{4.1}
\]

the projective pairing is

\[
 \langle P_QF_j,P_QM_Q\rangle
 =\langle F_j,M_Q\rangle
 -\frac{B_Q}{d_Q}
  \left(\frac12d_{Q,t}+\lambda_jd_Q\right).
 \tag{4.2}
\]

The complete R0.71L coordinate formula is

\[
 \mathcal J_Q
 =\frac1{\sqrt Y}
 \left(
 \langle N_j,E_Q\rangle
 +\frac{\langle P_QF_j,P_QM_Q\rangle}{r_Q}
 \right)
 -\frac{Y_t}{2Y}z_Q.
 \tag{4.3}
\]

The nominal piece in the first term is

\[
 \frac{\lambda_j\langle F_j,C_Q\rangle}
 {\sqrt{Yd_Q}}=\lambda_jz_Q,
 \tag{4.4}
\]

while the last part of (4.2), after normalization, contains

\[
 -\lambda_jz_Q.
 \tag{4.5}
\]

They cancel.  The remaining \(d_{Q,t}\) contribution is precisely the
logarithmic derivative in (2.5).  Thus the sign in R0.71M is fixed: the
projective pairing enters (4.3) with a positive coefficient, and its radial
correction in (4.2) has a negative sign.

## 5. Proof of the square--residual form

Complete the square in (2.1):

\[
 \begin{aligned}
 I_Q
 &=\int\chi_QG_j\cdot(G_j+\nu H_j)\\
 &=\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2
 -\frac{\nu^2}{4}\int\chi_Q|H_j|^2.
 \end{aligned}
 \tag{5.1}
\]

Substituting (3.7) and (5.1) into (2.5) proves (2.8)--(2.9).

This step is useful because it identifies the only displayed nonnegative
quadratic expression.  It is not yet a payment.  The acceleration
\(G_{j,t}\) has not been estimated, and Section 6 shows that it contains the
negative of the same pairing.

## 6. Proof of the local filtered-enstrophy cancellation

Differentiate (2.3) and use (3.5):

\[
 \begin{aligned}
 e_{Q,t}
 &=\langle W_{j,t},\chi_QW_j\rangle\\
 &=B_Q+\nu\langle\Delta W_j,\chi_QW_j\rangle\\
 &=B_Q-\nu D_Q^\chi.
 \end{aligned}
 \tag{6.1}
\]

This proves (2.10).  It is the fixed-cutoff filtered analogue of the standard
local enstrophy balance.  Differentiating (2.10) gives

\[
 B_{Q,t}=e_{Q,tt}+\nu(D_Q^\chi)_t.
 \tag{6.2}
\]

Combining (6.2) with (3.7) yields (2.11).  Inserting (2.11) and (2.12) into
(2.9) produces

\[
 \begin{aligned}
 \mathfrak R_Q
 ={}&-\mathcal P_Q^\square
 +e_{Q,tt}+\nu(D_Q^\chi)_t
 +\lambda_j(e_{Q,t}+\nu D_Q^\chi)\\
 &-\frac12(e_{Q,t}+\nu D_Q^\chi)
 \left(\frac{Y_t}{Y}+\frac{d_{Q,t}}{d_Q}\right).
 \end{aligned}
 \tag{6.3}
\]

The \(\mathcal P_Q^\square\) in (6.3) cancels the one in (2.8), proving
(2.13)--(2.14).

There is no contradiction between the square form and the second-jet form.
They are two coordinate representations of the same scalar.  Treating the
square as positive production while estimating the acceleration separately
would count a representation-dependent term.

## 7. Why \(e_Q\) and \(d_Q\) do not fuse

For divergence-free \(W_j\), curl self-adjointness gives

\[
 D_Q^\chi
 =\langle C_Q,\operatorname{curl}W_j\rangle.
 \tag{7.1}
\]

By contrast,

\[
 d_Q=\langle C_Q,C_Q\rangle.
 \tag{7.2}
\]

The first quantity is a cross pairing; the second is a square.  They coincide
for the global cell \(\chi_Q=1\), but not for a general physical cutoff.
No universal proportionality or sign relation is available from these
definitions.

The annular mismatch gives another exact representation:

\[
 D_Q^\chi
 =2\kappa_j^2e_Q-\langle\chi_QW_j,H_j\rangle,
 \tag{7.3}
\]

and hence

\[
 \boxed{
 B_Q=e_{Q,t}+2\lambda_je_Q
 -\nu\langle\chi_QW_j,H_j\rangle.}
 \tag{7.4}
\]

The last sign in (7.4) is negative.  A broad annulus does not make \(H_j\)
small; it is generally of order \(\kappa_j^2W_j\).  Thus (7.4) does not
replace the second jet by a lower-order positive quantity.

## 8. Scaling ledger

Under the formal local Euclidean NSE scaling

\[
 u_\mu(t,x)=\mu u(\mu^2t,\mu x),
 \tag{8.1}
\]

with the filter and cutoff co-scaled,

\[
 Y\sim\mu,
 \quad d_Q\sim\mu^3,
 \quad B_Q\sim\mu^3,
 \quad \sqrt{Yd_Q}\sim\mu^2,
 \quad z_Q\sim\mu.
 \tag{8.2}
\]

Each numerator row in (2.9) scales like \(\mu^5\):

\[
 \langle G_{j,t},\chi_QW_j\rangle,
 \quad
 \nu^2\int\chi_Q|H_j|^2,
 \quad
 B_Q\left(Y_t/Y+d_{Q,t}/d_Q\right).
 \tag{8.3}
\]

Therefore \(\mathcal J_Q\sim\mu^3\), and

\[
 \kappa_j^{-2}z_Q^+\mathcal J_Q^+\,dt
 \tag{8.4}
\]

is scale invariant.  The second-jet rewrite has not recovered a lower-order
budget; all surviving rows remain at the critical scale.

This is a local co-scaling calculation.  It is not a continuous symmetry of
one fixed torus, one fixed multiplier, or one fixed cutoff.

## 9. Standalone finite Fourier sign diagnostic

The independent checker declares two explicit real, divergence-free
trigonometric-polynomial initial data on \(\mathbb T^3\), a fixed positive
trigonometric cutoff, \(\kappa=4\), and \(\nu=0.2\).  It computes the exact
NSE initial jet without time stepping:

\[
 u_t=L+\nu\Delta u,
 \qquad
 \omega_t=\operatorname{curl}L+\nu\Delta\omega,
 \tag{9.1}
\]

\[
 L_t=\mathbb P(u_t\times\omega+u\times\omega_t).
 \tag{9.2}
\]

The periodic trapezoidal means are alias-safe for the declared finite
support.  Orders 48, 64, and 80 agree to binary64 tolerance.  At order 64 the
two witnesses give approximately

| witness | \(z_Q\) | \(\mathcal P_Q^\square\) | \(\mathfrak R_Q\) | \(\mathcal J_Q\) |
|---|---:|---:|---:|---:|
| positive source | \(3.7338305\times10^{-3}\) | \(5.0236425\times10^3\) | \(7.4992194\times10^2\) | \(1.3523543\) |
| negative source | \(1.9598744\times10^{-3}\) | \(5.1676946\times10^3\) | \(-2.5941294\times10^4\) | \(-7.3713441\) |

Both have \(z_Q>0\).  In the second witness the signed residual overwhelms
the positive square.  The checker verifies the derivative, projective,
square--residual, local-enstrophy, and second-jet forms independently.

These are smooth NSE initial jets, so local classical solutions exist around
the checked time.  The reported signs are nevertheless used only as a
deterministic finite-Fourier diagnostic: the current certificate uses
alias-safe high-margin floating arithmetic, not interval arithmetic.  The
exact theorem does not rely on the sign table.

## 10. Bounded primary-source comparison

The closest checked mechanisms are separate rather than identical:

1. Eyink's coarse-grained vortex-force and filtered-enstrophy equations
   [arXiv:physics/0606159](https://arxiv.org/abs/physics/0606159) contain the
   filtered Lamb commutator and vortex stretching, but no fixed
   cutoff--curl denominator or Hilbert tangent projector.
2. Dascaliuc--Grujić
   [arXiv:1107.0058](https://arxiv.org/abs/1107.0058) and Tao
   [arXiv:1108.1165](https://arxiv.org/abs/1108.1165) provide rigorous local
   enstrophy ledgers, with cutoff and transport terms, but not this annular
   normalized pairing.
3. Galanti--Gibbon--Heritage
   [arXiv:chao-dyn/9709003](https://arxiv.org/abs/chao-dyn/9709003) derive a
   tangent-projection equation for the pointwise unit vorticity direction.
   Their object is not the Hilbert-space direction \(C_Q/\|C_Q\|_2\).
4. Yu's 2026 preprint
   [arXiv:2606.27560v1](https://arxiv.org/abs/2606.27560v1) gives the closest
   checked filtered-vorticity/local-cutoff ledger, including a
   solution-adapted adjoint cutoff, but no \(B_Q/\sqrt{Yd_Q}\) projective
   evolution.
5. Milanese--Loureiro--Boldyrev
   [arXiv:2104.13518](https://arxiv.org/abs/2104.13518) use scale-dependent
   normalized alignment diagnostics in DNS.  Their statistical angle and
   denominator differ from \(z_Q\).
6. Bradshaw--Grujić
   [arXiv:1501.01043](https://arxiv.org/abs/1501.01043) place
   Littlewood--Paley windows inside regularity criteria, but do not use the
   filtered Lamb/cellwise projective scalar.

A bounded primary-source search on 2026-08-26 found no directly matching
fixed-cell evolution identity retaining this specific \(B_{Q,t}\),
\(d_{Q,t}\), and \(Y_t\) ledger.  This is a negative search finding, not an
originality or priority claim.  The elementary normalized-vector derivative
and local enstrophy integration by parts are standard.  The present identity
should be treated as a synthesis pending broader database and expert review.

## 11. What the calculation closes

### 11.1 Exact results

1. The complete scalar derivative formula (2.5), with the correct 3D
   enstrophy derivative (2.6).
2. Exact cancellation of the nominal parabolic rate between the radial and
   projective denominator rows.
3. The square--residual representation (2.8)--(2.9).
4. The local filtered-enstrophy identity (2.10).
5. Exact cancellation of the apparent positive square after the
   local-enstrophy acceleration is substituted.
6. The explicit signed second-jet residual (2.14).
7. The critical scaling of every remaining numerator row.

### 11.2 Diagnostic results

1. Two alias-safe smooth finite Fourier NSE initial jets have \(z_Q>0\) and
   opposite signs of \(\mathcal J_Q\).
2. The same calculations verify all displayed representations to binary64
   tolerance at three grid orders.

### 11.3 Not closed

1. No bound or sign for \(\mathcal K_Q\) follows from Leray energy.
2. No theorem excludes a different signed NSE cancellation.
3. No denominator-zero face or soft-limit measure is paid.
4. No refresh or moving-partition atom is treated.
5. No infinite frame--cell or weak-solution limit is justified.
6. No continuation, regularity, or singularity conclusion follows.

## 12. Route verdict and next finite gate

The R0.71N verdict is

\[
 \boxed{
 \text{the checked full-scalar/local-enstrophy insertion produces an explicit}
 \ \text{signed second jet, not a second coercive quadratic fusion}.}
 \tag{12.1}
\]

This closes the finite question posed by R0.71M.  It does not turn the second
jet into an obstruction theorem for every possible estimate.

R0.71O will remain on fixed cells and return to the hard-denominator boundary
already isolated in R0.71I.  Its finite task is to compare the hard components
with the soft regularization

\[
 R_\varepsilon=\sqrt{d_Q+\varepsilon},
 \qquad
 z_{Q,\varepsilon}=\frac{B_Q}{\sqrt YR_\varepsilon},
 \tag{12.2}
\]

and decide whether the \(\varepsilon\downarrow0\) source measures and one-sided
faces admit a uniform payment from the already available energy and
denominator-mass budgets.  Refresh atoms and moving cutoffs remain outside
that next gate.

## 13. Reproduction map

`research/r071n_exact_audit.py` checks the scalar product rule, nominal-rate
cancellation, square--residual identity, local-enstrophy cancellation,
critical scaling, and domain boundary with exact symbolic arithmetic.

`research/r071n_independent_audit.py` independently constructs two periodic
finite Fourier initial data and checks the complete NSE initial jet at three
alias-safe resolutions.

`research/r071n_gap_matrix.md` separates exact results, diagnostics,
conditional implications, and open claims.

`research/r071n_literature_audit.md` records the bounded primary-source
comparison and the terminology corrections.

No DNS time integration, stochastic simulation, fitted model, GPU job, or
DGX computation is used.  The exact algebra is the primary evidence; the
finite Fourier calculation is a standalone diagnostic.
