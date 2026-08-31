# R0.73V problem freeze: the canonical signed third-order heat lift

**Frozen date:** 2026-09-01

**Status:** discovery freeze; no public release is licensed by this file

**Domain:** the normalized periodic torus \(\mathbb T^3=[0,2\pi]^3\),
viscosity \(\nu>0\), and a smooth real mean-zero divergence-free
Navier--Stokes solution on its smooth lifespan

**Dependency:** R0.73U, especially its exact heat covariance law and its
quadratic-state non-autonomy witness

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. The word “minimal” is relative to a target equation

R0.73U identified a missing signed cubic contribution in the physical-time
equation for the heat-filtered quadratic tensor.  R0.73V asks which
third-order quantities actually occur when the target is the complete
second-order generalized stress equation.

This is not an information-theoretic minimization over every possible state.
At positive heat scale the heat operator is injective on smooth data, although
its inverse is unstable, and the signed resolved velocity is already an odd
state.  Parity alone therefore cannot prove that a cubic state is globally
minimal.  The permitted meaning of “minimal” in this section is narrower:

> the lowest odd polynomial order appearing in the exact, same-filter
> generalized-central-moment equation for the complete second-order stress.

Even in this restricted sense, componentwise minimality or uniqueness must
not be claimed unless a separate collision certificate proves it.

## 2. Frozen filter, projected nonlinearity, and cumulant notation

Let \(P_s=e^{s\Delta}\), and write

\[
 v_{s,i}=P_su_i,\qquad p_s=P_sp,
 \qquad \tau_{ij,s}=P_s(u_i u_j)-v_{s,i}v_{s,j}.
\tag{2.1}
\]

Set

\[
 \mathcal B(a,b)=\mathbb P\nabla\!\cdot(a\otimes b),\qquad
 N=\mathcal B(u,u)=(u\cdot\nabla)u+\nabla p,
 \tag{2.2}
\]

where \((a\otimes b)_{ik}=a_i b_k\).  Then

\[
 N_s=P_sN=\mathbb P\nabla\!\cdot\Theta_s,
 \qquad \Theta_s=P_s(u\otimes u).
 \tag{2.3}
\]

For \(a\odot b=a\otimes b+b\otimes a\), define the complete odd
cubic tensor tangent and its centered cross-covariance by

\[
 \mathcal C_s=P_s(u\odot N),\qquad
 \chi_s=\mathcal C_s-v_s\odot N_s.
 \tag{2.4}
\]

The single symmetric tensor \(\chi_s\) is the primary
**equation-slot-compressed** lift in R0.73V.  It is pressure-aware because
\(N\) contains the Leray/Riesz pressure contribution.  This phrase does not
mean information-theoretic, componentwise, or unique minimality.

For fixed fields \(f,g,h\), define the generalized heat cumulants

\[
 \tau_s(f,g)=P_s(fg)-P_sf\,P_sg,
 \tag{2.5}
\]

\[
 \begin{aligned}
 \tau_s(f,g,h)
 ={}&P_s(fgh)-P_sf\,\tau_s(g,h)-P_sg\,\tau_s(f,h)\\
 &-P_sh\,\tau_s(f,g)-P_sf\,P_sg\,P_sh.
 \end{aligned}
 \tag{2.6}
\]

The candidate signed third-order bundle is

\[
 \kappa_{ijk,s}=\tau_s(u_i,u_j,u_k),\qquad
 Q_{i,s}=\tau_s(p,u_i),\qquad
 R_{ij,s}=\tau_s(p,S_{ij}),
 \tag{2.7}
\]

where \(S_{ij}=\tfrac12(\partial_i u_j+\partial_j u_i)\).  Here \(C\)
is a local velocity cumulant, while \(Q\) and \(R\) are nonlocal cubic
velocity quantities because pressure is quadratic through the Riesz formula.

The Germano bundle \((\kappa,Q,R)\) is the transparent classical expansion of the
same third-order level for the stress equation.  It remains in the proof as
an index and attribution check; \(\chi_s\) is the compressed object used for
the R0.73U tensor-tangent interface.

## 3. Frozen exact claims to audit

The analytic gate must establish the following statements directly.

1. The compressed lift has the heat-scale equation
   \[
   \boxed{
   (\partial_s-\Delta)\chi_s
   =2\sum_\ell\partial_\ell v_s\odot\partial_\ell N_s,
   \qquad \chi_0=0,}
   \tag{3.1}
   \]
   and the corresponding Duhamel formula in \(s\).
2. The third velocity cumulant has the heat-scale equation
   \[
   \begin{aligned}
   (\partial_s-\Delta)\kappa_{ijk,s}=2\sum_\ell\big(&
    \partial_\ell v_{s,i}\,\partial_\ell\tau_{jk,s}
   +\partial_\ell v_{s,j}\,\partial_\ell\tau_{ik,s}\\
   &+\partial_\ell v_{s,k}\,\partial_\ell\tau_{ij,s}\big),
   \qquad \kappa_{ijk,0}=0.
   \end{aligned}
   \tag{3.2}
   \]
3. The pressure cumulants obey
   \[
   (\partial_s-\Delta)Q_{i,s}
   =2\nabla p_s\cdot\nabla v_{s,i},\qquad Q_{i,0}=0,
   \tag{3.3}
   \]
   and
   \[
   (\partial_s-\Delta)R_{ij,s}
   =2\nabla p_s\cdot\nabla S_{ij}(v_s),\qquad R_{ij,0}=0.
   \tag{3.4}
   \]
4. The physical-time equation for \(\tau_{ij,s}\) contains all three
   signed objects \(\kappa,Q,R\), not just \(\kappa\).
5. The raw third moment and \(\mathcal C_s\) have exact physical-time
   equations with fourth-order
   velocity and pressure--quadratic terms.  Thus the heat-scale hierarchy is
   downward triangular, while these natural physical-time third-level
   observables advance \(3\to4\).  A general centered-\(\kappa\) equation is
   not claimed without its full index ledger; the finite gate may certify a
   selected nonzero fourth-order \(\kappa\) coefficient.
6. At the bottom heat scale, the velocity third cumulant starts at
   \(O(s^2)\), while the complete centered pressure source starts at
   \(O(s)\) unless its explicit leading tensor vanishes.  Any claimed
   \(s^{-1}\) separation must be tied to a nondegenerate exact witness.
7. If \(u\in L_t^4L_x^6\), then \(\kappa\) and \(Q\) occupy the uniform critical
   flux row \(L_t^{4/3}L_x^2\).  The pressure--strain object \(R\) is not to
   be placed in that row without an additional derivative estimate.
8. Taking the trace kills \(R_{ii}=\tau_s(p,\nabla\cdot u)\) exactly.  The
   resulting scalar subgrid-energy flux
   \(J_{k,s}=\tfrac12\kappa_{iik,s}+Q_{k,s}\) occupies the same conditional
   critical row, while the signed production \(-\tau_s:\nabla v_s\)
   remains.

## 4. The exact physical-time ledgers to use

Let

\[
 G_s=P_s\sum_\ell\partial_\ell u\otimes\partial_\ell u.
 \tag{4.1}
\]

The R0.73U tensor equation becomes

\[
 \boxed{
 (\partial_t-\nu\partial_s)\Theta_s
 =-2\nu G_s-v_s\odot N_s-\chi_s.}
 \tag{4.2}
\]

Thus \(\chi_s\) fills exactly the odd cubic slot.  It does not close the
remaining even gradient row \(G_s\), and it does not make its own time
equation finite-order autonomous.

With \(D_{ij,s}=\tau_s(\partial_k u_i,\partial_k u_j)\), summed over
\(k\), the target identity is Germano's generalized-stress equation,
specialized to the heat filter:

\[
\begin{aligned}
 \partial_t\tau_{ij,s}+\partial_k(v_{s,k}\tau_{ij,s})
 ={}&-\partial_k\!\left(
 \kappa_{ijk,s}+Q_{i,s}\delta_{jk}+Q_{j,s}\delta_{ik}
 -\nu\partial_k\tau_{ij,s}\right)\\
 &+2R_{ij,s}-2\nu D_{ij,s}
 -\tau_{ik,s}\partial_kv_{s,j}
 -\tau_{jk,s}\partial_kv_{s,i}.
\end{aligned}
\tag{4.3}
\]

The even viscous row \(D\) is carried explicitly.  R0.73V does not silently
declare it a function of the local tensor heat state.

Equation (4.3) fixes the first negative test: a state that adds only
\(\kappa_{ijk,s}\) omits exact pressure-cubic terms.  The finite certificate may
show that those omitted terms are nonzero for a declared witness.  That is
not yet the stronger statement that \(Q\) or \(R\) cannot be reconstructed
from every other declared field; such a statement requires an equality-state
collision.

The exact equation-slot compression is

\[
 \mathcal C_s=v_s\odot N_s+\chi_s.
 \tag{4.4}
\]

## 5. Frozen critical-space question

Let \(E(I)=L^4(I;L^6(\mathbb T^3))\).  The expected conditional estimates are

\[
 \sup_{s\ge0}\|\kappa_s\|_{L_t^{4/3}L_x^2(I)}
 \le C_C\|u\|_{E(I)}^3,
 \tag{5.1}
\]

\[
 \sup_{s\ge0}\|Q_s\|_{L_t^{4/3}L_x^2(I)}
 \le C_QC_R\|u\|_{E(I)}^3.
 \tag{5.2}
\]

Here (5.1) concerns the local velocity cumulant \(\kappa\), not the derivative
carrying compressed field \(\mathcal C_s\) or \(\chi_s\).  These estimates
are scaling-compatible but circular for arbitrary-data
regularity because they assume the classical strong norm.  No estimate for
\(R_s\), no zero-scale energy-class bound, and no absorption by
\(\nu\partial_s\) may be inferred from (5.1)--(5.2).

## 6. Frozen certificate questions

The exact finite package must answer only questions that it computes:

1. Does the R0.73U four-site field give nonzero local cubic transport and
   nonzero pressure-cubic contributions separately?
2. Does omitting the pressure bundle give the wrong tensor tangent for that
   witness?
3. Is a fourth-order term in the time derivative of the chosen cubic lift
   nonzero on a finite exact witness?
4. Can two distinct fields with the same declared lower state and the same
   \(\kappa\) but different pressure-cubic source be found?  If not, the stronger
   `cAloneInformationTheoreticallyInsufficient` claim remains open.
5. Does a six-site field have zero local cubic coefficient at one declared
   output frequency but a nonzero pressure-cubic coefficient there?  Such a
   witness certifies only coefficientwise non-recovery, not whole-field
   information-theoretic non-sufficiency.
6. Does the four-site coefficient make the general \(O(s^2)\) versus
   \(O(s)\) bottom-scale separation nondegenerate, giving an exact
   coefficient ratio of order \(s^{-1}\)?

No floating-point simulation is needed for these algebraic gates.  Ordinary
translation remains local and direct; DGX is not used.

## 7. Release boundary

R0.73V remains a discovery section until the following all agree:

- the heat-scale cumulant proof and an independent index/sign audit;
- the complete physical-time ledger and its classical attribution;
- a sealed exact finite certificate with explicitly limited conclusions;
- a formal figure tied to the certificate source data;
- a primary-source collision audit;
- synchronized Chinese and English HTML/PDF, cumulative recap, route counts,
  release inventory, and live GitHub Pages readback.

Arbitrary-data three-dimensional global regularity and the Clay Millennium
problem remain open.  `NOT CLAY`.
