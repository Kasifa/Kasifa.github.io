# R0.73V independent analytic audit

**Audit date:** 2026-09-01

**Scope:** independent componentwise derivation of the heat-product
identities, signed third-order scale equations, complete second-stress
equation, conditional critical rows, trace projection, physical-time
\(3\to4\) ascent, and bottom-scale order separation

**Primary-source readback:** M. Germano, *Turbulence: the filtering approach*,
J. Fluid Mech. 238 (1992), 325--336,
[DOI](https://doi.org/10.1017/S0022112092001733), especially equations
(22) and (24)

**Ordinary translation path:** LOCAL_DIRECT_NO_DGX

**Verdict:** PASS.  All displayed analytic identities through parent
equation (8.7) have the correct signs, factors, free indices, and bottom-scale
orders.  The parent scope now limits the self-contained physical-time
\(3\to4\) theorem to the raw moment \(M_s\) and compressed field
\(\mathcal C_s\); a general centered-\(\kappa_s\) equation is expressly not
claimed.  The earlier support gap is therefore closed by scope narrowing,
with no remaining analytic release blocker.

## 1. Heat-product and covariance identities

Write \(L_s=\partial_s-\Delta\), \(A_s=P_sf\), \(B_s=P_sg\), and
\(D_s=P_sh\).  Since
\(L_sA_s=L_sB_s=L_sD_s=0\), the Laplacian product rule gives

\[
 L_s(A_sB_s)=-2\partial_\ell A_s\,\partial_\ell B_s,
\tag{1.1}
\]

and

\[
 \begin{aligned}
 L_s(A_sB_sD_s)=-2\big(&
 D_s\partial_\ell A_s\partial_\ell B_s
 +B_s\partial_\ell A_s\partial_\ell D_s\\
 &+A_s\partial_\ell B_s\partial_\ell D_s\big).
 \end{aligned}
\tag{1.2}
\]

The repeated spatial index is summed.  These are componentwise identities,
so their tensor use introduces no hidden transposition.  Consequently

\[
 L_s\tau_s(f,g)=2\nabla P_sf\cdot\nabla P_sg,
 \qquad \tau_0(f,g)=0.
\tag{1.3}
\]

This verifies parent equations (2.1)--(2.4).

Taking \(f=u_i\) and \(g=N_j\), then adding the equation with \(i,j\)
interchanged, gives

\[
 L_s\chi_s
 =2\sum_\ell\partial_\ell v_s\odot\partial_\ell N_s,
 \qquad \chi_0=0.
\tag{1.4}
\]

The Duhamel sign in parent equation (3.2) is positive.  Its source uses the
whole lower scale interval \(0\le r\le s\); this is not a
single-positive-scale algebraic constitutive relation.

## 2. Tensor heat-plane law

With \(\partial_tu=\nu\Delta u-N\), direct expansion gives

\[
 \partial_t(u\otimes u)
 =\nu\Delta(u\otimes u)
 -2\nu\sum_\ell\partial_\ell u\otimes\partial_\ell u
 -u\odot N.
\tag{2.1}
\]

Filtering and using \(\partial_s\Theta_s=\Delta\Theta_s\) yields

\[
 (\partial_t-\nu\partial_s)\Theta_s
 =-2\nu G_s-v_s\odot N_s-\chi_s.
\tag{2.2}
\]

Thus parent equations (3.3)--(3.5) pass.  At the bottom scale,

\[
 \left.\partial_r\tau_r\right|_{r=0}
 =2\sum_\ell\partial_\ell u\otimes\partial_\ell u,
\tag{2.3}
\]

so parent equation (3.6) also passes.  It uses a bottom-scale derivative and
is not a stable constitutive inversion at one positive scale.

## 3. Third cumulant and pressure scale equations

Let \(a=P_sf\), \(b=P_sg\), \(c=P_sh\), with filtered pair products
\(A_{fg}=P_s(fg)\), etc.  Expanding

\[
 \tau_s(f,g,h)=P_s(fgh)-aA_{gh}-bA_{fh}-cA_{fg}+2abc
\tag{3.1}
\]

and applying (1.1)--(1.2) gives

\[
 \begin{aligned}
 L_s\tau_s(f,g,h)=2\big(&
 \nabla a\cdot\nabla\tau_s(g,h)
 +\nabla b\cdot\nabla\tau_s(f,h)\\
 &+\nabla c\cdot\nabla\tau_s(f,g)\big).
 \end{aligned}
\tag{3.2}
\]

The six terms containing one undifferentiated first moment cancel exactly.
There is neither a missing factor two nor an extra gradient-pair term.
Taking \(f=u_i,g=u_j,h=u_k\) verifies parent equation (4.4), including
\(\kappa_{ijk,0}=0\).

Because the heat filter commutes with derivatives,

\[
 L_sQ_{i,s}=2\nabla p_s\cdot\nabla v_{s,i},
 \qquad
 L_sR_{ij,s}=2\nabla p_s\cdot\nabla S_{ij}(v_s).
\tag{3.3}
\]

Both initial values are zero.  Parent equations (5.3)--(5.4) pass.

The transparent identity also passes:

\[
 P_s(u\odot N)_{ij}
 =\partial_kP_s(u_ku_iu_j)
  +P_s(u_i\partial_jp+u_j\partial_ip).
\tag{3.4}
\]

The statement that \((\kappa_s,\rho_s)\) and \(\chi_s\) represent the same
third-order level is valid over the fixed lower state
\((v_s,\tau_s,p_s)\).  The pair \((\kappa_s,\rho_s)\) alone does not include
the resolved products needed to reconstruct \(\mathcal C_s\).  The parent
problem freeze supplies this lower-state context; no algebraic error remains.

## 4. Germano second-stress equation

The three independent pieces of the physical-time calculation are as
follows.  First, incompressibility and the raw-to-central third-moment
identity give

\[
 \begin{aligned}
 &-\tau_s(u_k\partial_ku_i,u_j)
  -\tau_s(u_i,u_k\partial_ku_j)\\
 &\quad=-\partial_k\kappa_{ijk,s}
 -\partial_k(v_{s,k}\tau_{ij,s})
 -\tau_{ik,s}\partial_kv_{s,j}
 -\tau_{jk,s}\partial_kv_{s,i}.
 \end{aligned}
\tag{4.1}
\]

Second, direct differentiation of the covariance gives

\[
 \tau_s(\Delta u_i,u_j)+\tau_s(u_i,\Delta u_j)
 =\Delta\tau_{ij,s}-2D_{ij,s}.
\tag{4.2}
\]

Third,

\[
 \partial_iQ_{j,s}
 =\tau_s(\partial_ip,u_j)+\tau_s(p,\partial_i u_j),
\tag{4.3}
\]

and its transposed counterpart imply

\[
 -\tau_s(\partial_ip,u_j)-\tau_s(u_i,\partial_jp)
 =-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s}.
\tag{4.4}
\]

Combining (4.1)--(4.4) gives

\[
 \begin{aligned}
 \partial_t\tau_{ij,s}+\partial_k(v_{s,k}\tau_{ij,s})
 ={}&-\partial_k\big(
 \kappa_{ijk,s}+Q_{i,s}\delta_{jk}+Q_{j,s}\delta_{ik}
 -\nu\partial_k\tau_{ij,s}\big)\\
 &+2R_{ij,s}-2\nu D_{ij,s}
 -\tau_{ik,s}\partial_kv_{s,j}
 -\tau_{jk,s}\partial_kv_{s,i}.
 \end{aligned}
\tag{4.5}
\]

Every free index and sign agrees with parent equation (5.7).  Germano's
primary equation (22), together with the generalized-central-moment
definition (24), has the same pressure flux, \(+2\tau(p,S_{ij})\), viscous
covariance, and production terms.  The attribution is exact rather than
merely analogous.

## 5. Conditional critical rows and trace projection

If \(u\in L_t^4L_x^6(I)\), heat contraction and Hölder give

\[
 \|P_s(u^{\otimes3})\|_{L_t^{4/3}L_x^2}
 \le \|u\|_{L_t^4L_x^6}^3.
\tag{5.1}
\]

The terms \(v_s\otimes\tau_s\) and \(v_s^{\otimes3}\) occupy the same
space because \(v_s\in L_t^4L_x^6\) and
\(\tau_s\in L_t^2L_x^3\).  This verifies the uniform \(\kappa_s\) row,
up to the declared finite tensor constant.

The periodic pressure estimate

\[
 \|p\|_{L_t^2L_x^3}\le C_R\|u\|_{L_t^4L_x^6}^2
\tag{5.2}
\]

implies separately

\[
 \|P_s(pu)\|_{L_t^{4/3}L_x^2}
 +\|p_sv_s\|_{L_t^{4/3}L_x^2}
 \le2C_R\|u\|_{L_t^4L_x^6}^3.
\tag{5.3}
\]

Parent equations (6.2)--(6.4) pass.  No derivative-free argument places
\(R_s\), \(\rho_s\), or \(\chi_s\) in this row.  These estimates assume a
Serrin-critical strong norm and are circular for arbitrary energy data.

For the scalar projection, set

\[
 k_s=\frac12\tau_{ii,s},
 \qquad
 J_{k,s}=\frac12\kappa_{iik,s}+Q_{k,s}.
\tag{5.4}
\]

Taking half the trace of (4.5) gives the following factors:

- the two pressure-flux terms each contribute \(Q_{k,s}/2\), hence their
  sum contributes \(Q_{k,s}\);
- \(R_{ii,s}=\tau_s(p,S_{ii})=0\) because
  \(S_{ii}=\nabla\cdot u=0\);
- the two production terms become equal after setting \(j=i\), so their
  half-trace is \(-\tau_{ik,s}\partial_kv_{s,i}\);
- \(\frac12(-2\nu D_{ii,s})=-\nu D_{ii,s}\).

Therefore

\[
 \partial_t k_s+\partial_k(v_{s,k}k_s)
 =-\partial_k(J_{k,s}-\nu\partial_k k_s)
 -\nu D_{ii,s}-\tau_{ik,s}\partial_kv_{s,i}.
\tag{5.5}
\]

Parent equation (6.6) passes.  Moreover,

\[
 D_{ii,s}
 =\sum_{i,k}\big[
 P_s((\partial_ku_i)^2)-(\partial_kv_{s,i})^2\big]\ge0
\tag{5.6}
\]

pointwise by the heat-kernel covariance inequality.  Finally, (5.1)--(5.3)
and finite-dimensional contraction give

\[
 \sup_{s\ge0}\|J_s\|_{L_t^{4/3}L_x^2}
 \le C_J(1+C_R)\|u\|_{L_t^4L_x^6}^3.
\tag{5.7}
\]

Parent equation (6.7) passes.  The pressure--strain derivative gap disappears
in this scalar trace, but the production
\(-\tau_s:\nabla v_s\) remains signed and the flux bound remains conditional.

## 6. Physical-time \(3\to4\) ascent

The three-factor Laplacian rule gives

\[
 \begin{aligned}
 (\partial_t-\nu\partial_s)M_{ijk,s}
 ={}&-2\nu P_s\sum_\ell\big(
 u_k\partial_\ell u_i\partial_\ell u_j
 +u_j\partial_\ell u_i\partial_\ell u_k\\
 &\hspace{35mm}
 +u_i\partial_\ell u_j\partial_\ell u_k\big)\\
 &-P_s(N_i u_j u_k+u_iN_j u_k+u_i u_jN_k).
 \end{aligned}
\tag{6.1}
\]

This verifies parent equation (7.1).  Since \(N=\mathcal B(u,u)\), its
last line is quartic in velocity.

For the compressed equation, bilinearity and commutation with the Laplacian
give

\[
 \partial_tN=\nu\Delta N-2\nu\mathcal S_3-\mathcal R_4,
\tag{6.2}
\]

where
\(\mathcal S_3=\sum_\ell\mathcal B(\partial_\ell u,\partial_\ell u)\) and
\(\mathcal R_4=\mathcal B(N,u)+\mathcal B(u,N)\).  Substitution into
\(\partial_t(u\odot N)\), followed by the Laplacian product rule, gives

\[
 \begin{aligned}
 (\partial_t-\nu\partial_s)\mathcal C_s
 =-P_s\big\{&N\odot N+u\odot\mathcal R_4\\
 &+2\nu[\partial_\ell u\odot\partial_\ell N
              +u\odot\mathcal S_3]\big\}.
 \end{aligned}
\tag{6.3}
\]

Thus the factor \(2\nu\) and overall minus sign in parent equation (7.4)
pass.  Here \(\mathcal R_4\) itself is cubic; its label records that
\(u\odot\mathcal R_4\) is quartic.  Similarly, \(\mathcal S_3\) itself is
quadratic and its product with \(u\) is cubic.  The parent text correctly
calls only the first line in braces quartic.

Finally,

\[
 (\partial_t-\nu\partial_s)v_s=-N_s,
\qquad
 (\partial_t-\nu\partial_s)N_s
 =-\mathbb P\nabla\cdot(2\nu G_s+\mathcal C_s).
\tag{6.4}
\]

Applying the product rule to
\(\chi_s=\mathcal C_s-v_s\odot N_s\) verifies both positive resolved terms
in parent equation (7.5):

\[
 \begin{aligned}
 (\partial_t-\nu\partial_s)\chi_s
 ={}&(\partial_t-\nu\partial_s)\mathcal C_s
 +N_s\odot N_s\\
 &+v_s\odot\mathbb P\nabla\cdot(2\nu G_s+\mathcal C_s).
 \end{aligned}
\tag{6.5}
\]

Equations (6.1) and (6.3) prove the self-contained \(3\to4\) statement for
\(M_s\) and \(\mathcal C_s\).  The parent has adopted the narrow option:
it does not claim a displayed general physical-time equation for the centered
\(\kappa_s\).  A selected finite coefficient may be checked separately by
the certificate.  This scope is internally consistent.

## 7. Bottom-scale order separation

Integrating (1.3), or differentiating it at \(s=0\), gives

\[
 \tau_s(f,g)
 =2s\,\partial_\ell f\,\partial_\ell g+O(s^2)
\tag{7.1}
\]

in each fixed spatial \(C^m\) norm allowed by the smoothness.  Therefore

\[
 Q_{i,s}
 =2s\,\partial_\ell p\,\partial_\ell u_i+O(s^2),
\qquad
 R_{ij,s}
 =2s\,\partial_\ell p\,\partial_\ell S_{ij}+O(s^2).
\tag{7.2}
\]

These verify parent equations (8.1)--(8.3).

At \(s=0\), the right side of the \(\kappa\) scale equation vanishes because
\(\tau_0=0\), hence \(\partial_s\kappa_{ijk,0}=0\).  Differentiating once
more gives

\[
 \begin{aligned}
 \partial_s^2\kappa_{ijk,0}
 =4\sum_{\ell,m}\big[&
 \partial_\ell u_i\,\partial_\ell(
     \partial_m u_j\,\partial_m u_k)\\
 &+\partial_\ell u_j\,\partial_\ell(
     \partial_m u_i\,\partial_m u_k)\\
 &+\partial_\ell u_k\,\partial_\ell(
     \partial_m u_i\,\partial_m u_j)\big].
 \end{aligned}
\tag{7.3}
\]

Taylor's factor \(1/2\) changes the coefficient \(4\) in (7.3) into the
coefficient \(2s^2\) in parent equation (8.4).  Thus
\(\kappa_s=O(s^2)\) and the displayed leading tensor are correct.

For the complete centered pressure source,

\[
 \mathfrak P_{ij,s}
 =-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s},
\tag{7.4}
\]

substitution of (7.2) gives two types of terms.  The terms containing
\(\partial_\ell p\,\partial_i\partial_\ell u_j\) and their transpose cancel
against

\[
 4s\,\partial_\ell p\,\partial_\ell S_{ij}
 =2s\,\partial_\ell p\,
   (\partial_i\partial_\ell u_j+\partial_j\partial_\ell u_i).
\tag{7.5}
\]

The remainder is

\[
 \mathfrak P_{ij,s}
 =-2s\sum_\ell\big[
 (\partial_i\partial_\ell p)(\partial_\ell u_j)
 +(\partial_j\partial_\ell p)(\partial_\ell u_i)\big]
 +O(s^2).
\tag{7.6}
\]

Parent equation (8.6), including its minus sign and factor two, passes.
It establishes an \(O(s)\) pressure source.  A ratio of order \(s^{-1}\)
still requires a witness on which both the \(O(s)\) pressure coefficient
and the relevant \(O(s^2)\) velocity-cumulant coefficient are nonzero.
The parent states this nondegeneracy boundary correctly.

Finally, (1.4) and \(\chi_0=0\) give

\[
 \chi_s
 =2s\sum_\ell\partial_\ell u\odot\partial_\ell N+O(s^2),
\tag{7.7}
\]

so parent equation (8.7) passes.  It is a smooth bottom-scale expansion, not
an energy-class derivative estimate.

## 8. Exact claim boundary

The audited result establishes equation-slot compression and exact
heat-scale identities.  It does not establish information-theoretic,
componentwise, or globally unique minimality of \(\chi\), \(\kappa\), \(Q\),
or \(R\).  The heat-scale system is downward triangular, not a finite
physical-time closure.  The conditional critical rows do not control the
arbitrary-data energy class.  The separate sealed finite certificate supplies
the required witness nondegeneracies; its single-mode checks must not be
promoted into a whole-field collision.

Arbitrary-data three-dimensional global regularity and the Clay Millennium
problem remain open.  NOT CLAY.

analyticDisplayedIdentities=PASS
germanoSignsAndIndices=PASS
criticalKappaQRows=PASS_CONDITIONAL
scalarTraceEquation=PASS
scalarTraceDissipation=PASS_NONNEGATIVE
criticalScalarFlux=PASS_CONDITIONAL
rawAndCompressedThreeToFour=PASS
centeredKappaGeneralLedger=CLOSED_AS_SCOPE_NARROWING
bottomScaleKappaOrder=PASS_O_S2
bottomScalePressureOrder=PASS_O_S1
bottomScaleCompressedOrder=PASS_O_S1
analyticReleaseBlockers=NONE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
