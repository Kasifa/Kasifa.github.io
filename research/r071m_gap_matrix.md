# R0.71M gap matrix — increment commutator versus the complete fixed-cell tangent

This matrix separates universal algebra, conditional estimates, functional
separations, finite diagnostics, and open Navier--Stokes implications.

The exact producer is research/r071m_exact_audit.py. The independent
finite-Fourier checker is research/r071m_independent_audit.py. Neither file
imports a result from R0.71L.

## 1. Main claim matrix

| Item | Status | Evidence | Exact scope | What it does not say |
|---|---|---|---|---|
| \(T_j(u\times\omega)-u\times T_j\omega\) has the quadratic velocity-increment formula (2.2) | proved | componentwise periodic integration by parts; exact producer | classical divergence-free field, translation-invariant scalar filter | no pointwise sign and no bound for its curl |
| \(G_j=\operatorname{curl}(u\times W_j)+\operatorname{curl}\mathcal R_j\) | proved | commuting Fourier multipliers | fixed annular block | split terms need not be annular |
| the split resolved and commutator rows can have off-band support | proved for an explicit smooth witness; structurally allowed in general | standalone 48-point Fourier audit | declared finite mode set and multiplier | not a universal lower bound for off-band mass |
| the fused \(G_j\) is annular | proved | \(G_j=T_j\operatorname{curl}(u\times\omega)\) | fixed scalar annular multiplier | no nonlinear norm gain |
| projective pairing identity (2.5) | proved | curl self-adjointness and rank-one projector algebra | fixed \(j,Q,t\), \(d_Q>0\) | no sign |
| radial pairing identity (2.7) | proved | \(\langle C_Q,M_Q\rangle=d_{Q,t}/2+\nu\kappa_j^2d_Q\) | same | apparent \(\int\chi|G|^2\) is not independently coercive |
| four-row envelope (2.13) | proved | one Cauchy inequality and the three-vector square bound | positive branch; absolute version after \(B^+\to|B|\) | right side is not shown energy-paid |
| every four-row time budget is NSE-scale critical | proved | exact homogeneity ledger | formal local Euclidean scaling with filter and cell cutoff co-scaled | not a continuous symmetry of one fixed torus/cutoff; criticality is not an estimate |
| Yu-type quartic increment defect universally follows from Leray energy | false as a function-space embedding | \(L^2\)-normalized divergence-free heat packets | heat flows on \(\mathbb R^3\) | not an NSE-solution counterexample |
| critical velocity square-Carleson mass universally follows from Leray energy | false as a function-space embedding | same heat packets | same | no claim about small NSE data |
| normalized projected-Lamb absolute budget universally follows from energy | false as a function-space embedding | heat packets from a profile satisfying \(\mathbb P(\Phi\times\operatorname{curl}\Phi)\ne0\) | same | no claim about the smaller signed tangent |
| one increment defect closes the complete projective tangent | does not close under the displayed direct insertion | exact decomposition plus support/derivative mismatch | this representation and its direct absolute estimate | no logical non-implication and no general signed NSE no-go |
| global regularity or finite-time singularity | open | none | Millennium problem | R0.71M makes no such claim |

## 2. Exact algebra ledger

Use

\[
 \mathcal R_j=T_j(u\times\omega)-u\times W_j,
 \qquad
 H_j=(\Delta+\kappa_j^2)W_j,
\]

\[
 A_j=\operatorname{curl}(u\times W_j),\quad
 D_j=\operatorname{curl}\mathcal R_j,\quad
 K_{j,Q}=\frac{B_Q}{d_Q}\operatorname{curl}C_Q,\quad
 V_j=\nu H_j.
\]

Then

\[
 G_j=A_j+D_j,\qquad
 \widetilde G_{j,Q}=A_j+D_j-K_{j,Q},\qquad
 S_j=A_j+D_j+V_j.
\]

There are two exact, equivalent projective forms:

\[
 \langle P_QF_j,P_QM_Q\rangle
 =\int\chi_Q\widetilde G_{j,Q}\cdot S_j,
\]

\[
 \langle P_QF_j,P_QM_Q\rangle
 =\int\chi_QG_j\cdot(G_j+\nu H_j)
 -\frac{B_Q}{d_Q}
  \left(\frac12d_{Q,t}+\nu\kappa_j^2d_Q\right).
\]

No row is discarded before these identities.

## 3. Conditional critical bridge

Define

\[
 \gamma_{j,Q}=\frac{\kappa_jB_Q^+}{Yd_Q}.
\]

The exact positive-branch projective envelope is

\[
 \Theta_{j,Q}
 =\gamma_{j,Q}\kappa_j^{-3}
 \left|\int\chi_Q
 (A_j+D_j-K_{j,Q})\cdot(A_j+D_j+V_j)\right|.
\]

A sufficient conditional budget over an interval \(I\) is

\[
 \sum_{j,Q}\int_I\gamma_{j,Q}\kappa_j^{-3}
 \left(
 \|A_j\|_{L^2(\chi_Q)}^2+
 \|D_j\|_{L^2(\chi_Q)}^2+
 \|K_{j,Q}\|_{L^2(\chi_Q)}^2+
 \|V_j\|_{L^2(\chi_Q)}^2
 \right)dt<\infty.
\]

This is deliberately labelled conditional. It includes a denominator factor
through \(\gamma_{j,Q}\), a resolved transport consumer, a differentiated
commutator consumer, and two geometry/viscosity consumers. Standard energy
does not supply this statement in the checked ledger.

## 4. Increment-support boundary

The exact kernel formula gives

\[
 |\mathcal R_j(x)|
 \lesssim\kappa_j
 \left(\int|\delta_hu(x)|^p\,d\mu_j(h)\right)^{2/p}.
\]

Consequently a matched quartic increment defect controls a quantity of the
form

\[
 \kappa_j^{-1}\int\|\mathcal R_j\|_2^2dt.
\]

The four-row tangent envelope contains

\[
 \kappa_j^{-3}\int\|\operatorname{curl}\mathcal R_j\|_2^2dt.
\]

An upper Bernstein comparison would follow from
\(\operatorname{supp}\widehat{\mathcal R_j}\subset B(0,C\kappa_j)\); annular
support is not required. No such \(O(\kappa_j)\) upper-frequency support holds
in general, because the unfiltered factor in \(u\times W_j\) can carry
arbitrarily high frequencies. The standalone witness contains positive
energy above the declared output band, and the exact formula

\[
 \mathcal R_j=T_j(u\times\omega)-u\times W_j
\]

records this mechanism. Only \(A_j+D_j=G_j\) regains the annular support.

This is a failure of the direct split estimate, not a claim that all
commutator formulations fail.

## 5. Heat-packet separation ledger

For

\[
 u_r(t,x)=r^{-3/2}
 \left(e^{(\nu t/r^2)\Delta}\Phi\right)
 \left(\frac{x-x_0}{r}\right),
\]

the exact energy budget is uniform. On a matched parabolic window:

| Quantity | Scale | Status |
|---|---:|---|
| kinetic \(L^\infty_tL^2_x\) | \(r^0\) | uniformly paid |
| \(\nu\int\|\nabla u_r\|_2^2\) | \(r^0\) | uniformly paid |
| Yu-type quartic derivative-compatible defect | \(r^{-2}\) | diverges |
| velocity square-Carleson mass | \(r^{-1}\) | diverges |
| normalized projected-Lamb integral | \(r^{-1}\) | diverges for a fixed profile satisfying \(\mathbb P(\Phi\times\operatorname{curl}\Phi)\ne0\) |
| critical cubic \(L_t^3B_{3,\infty}^{2/3}\) envelope | \(r^{-3/2}\) before cube root | diverges |

The fields are smooth divergence-free heat flows. They are not nonlinear NSE
solutions. The conclusion is only that no universal function-space embedding
from the standard energy class can pay these absolute critical quantities.

## 6. Interpolation boundary

For \(0\le\theta\le1\) and \(2\le p\le\infty\), energy interpolation and the
standard Sobolev/Bernstein embedding yield

\[
 u\in L_t^{2/\theta}\dot H^\theta,\qquad
 s_E=\theta-\frac32+\frac3p.
\]

At the same admissible \(p,q=2/\theta\), NSE criticality requires

\[
 s_c=-1+\frac3p+\theta,
\]

so

\[
 s_c-s_E=\frac12.
\]

For \(p=q=3\), this is the gap between the energy-paid
\(L_t^3B_{3,3}^{1/6}\) scale and the parabolically critical
\(L_t^3B_{3,\infty}^{2/3}\) scale. This statement is separate from the
Onsager \(1/3\) threshold and from Yu's quartic defect.

## 7. Independent audit boundary

The independent checker uses:

- a fixed 48-point periodic Fourier grid;
- five declared divergence-free Fourier mode pairs;
- a deterministic compact annular discrete multiplier;
- a fixed positive trigonometric cutoff;
- spectral differentiation and normalized trapezoidal \(L^2\) products.

It checks finite identities to binary64 tolerance. No time integration, DNS,
fitting, random sampling, interval sign proof, or finite-\(K\) NSE trajectory
is involved.

## 8. Open implications

The following remain unproved:

1. a sign for the exact radial/projective pairing;
2. a cancellation between \(d_{Q,t}\), local enstrophy, and source-square
   rows after full scalar fusion;
3. an NSE-specific estimate for the smaller signed tangent;
4. denominator-face or refresh control;
5. moving-cell control;
6. unweighted scale summability;
7. infinite frame--cell passage;
8. an unconditional continuation theorem.

The next finite audit is R0.71N: start from the complete
\(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\), retain
\(B_{Q,t},d_{Q,t},Y_t\) together, and then insert the radial identity and the
local filtered-enstrophy expression for \(B_Q\) before any positive part or
rowwise absolute value is taken. Because local filtered enstrophy and
\(d_Q\) are different state variables, both a second exact fusion and an
explicit signed residual remain admissible outcomes.
