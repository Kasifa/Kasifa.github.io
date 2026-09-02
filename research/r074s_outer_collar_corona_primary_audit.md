# R0.74S Step 14 — primary analytic audit

## 0. Frozen object and verdict

The audited object is
research/r074s_outer_collar_corona_obstruction.md, with SHA-256

c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9.

**Verdict: PASS within the stated analytic, algebraic, geometric,
conditional, and abstract scopes.  NOT CLAY.**

The audit reconstructs every display (S.343)--(S.376).  It supports five
limited conclusions.

1. The shell flux has the stated shell-scale pressure split and exact
   four-channel signed decomposition.  Channelwise absolute values give
   only the inherited linear \(L_t^1\) payment.
2. The outer cutoff collar is aligned with the same exterior payment
   weight.  The smooth spike blocks a uniform \(L_t^p\), \(p>1\),
   best-\(N\) conclusion from that nonnegative \(L_t^1\) information alone.
3. The incidence Holder implication is exact at the coefficient-cube
   exponent.  Density first crossings do not improve the payment power,
   while first relative jumps leave a low-transition corona.
4. The heat shear and critical corona are valid narrow or abstract screens.
   Neither is an NSE counterexample to an open gate.
5. The shell-selective jump--corona statement (S.375) is a precise
   sufficient **OPEN** lemma.  Only its implication to (S.376) is proved.

This audit does **not** prove (S.342), (S.375), the ancestor gate (S.288),
the combined gate (S.303), Step 11 (S.272), Q.12, Q.1, scale contraction,
regularity, singularity formation, or the Navier--Stokes Millennium
problem.

## 1. Frozen source bindings

| Source | SHA-256 | Imported role |
|---|---|---|
| research/r074e_local_mollified_frame_gate.md | 3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7 | Version-M path, lifted cutoffs, shell weights, fixed gauge, frozen payment, and total dissipation measure. |
| research/r074p_temporal_observable_triage.md | a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867 | AC physical-flux primitive (2.9), gauge cancellation, and absolute \(L_t^1\) ledger (3.4a)--(3.6). |
| research/r074s_shared_budget_terminal_trace_obstruction.md | fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693 | Step 11 ancestor coordinates and still-open fixed-deletion targets. |
| research/r074s_terminal_window_morrey_packing.md | 03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f | Definition of \(b_k\), ancestor gate (S.288), lifted tubes, and conditional Morrey benchmark. |
| research/r074s_temporal_integrability_morrey_threshold.md | d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de | Dimensionless rate, common deletion, fixed-solution \(L_t^{4/3}\) envelope, (S.342), cubic duality, and eight-ary ledger. |

The Step 14 note changes none of these definitions.  In particular,
\(P_R^M\) remains the frozen core-plus-exterior payment,
\(A_R=(P_R^M)^{2/3}\), and \(k\) labels physical annuli rather than
Fourier shells.  Every imported PDE estimate remains inherited.

## 2. Shell geometry, pressure, and normalization

### 2.1 Cutoff collars: (S.343)

For \(\rho_k=2^kR\), the first radial cutoff factor varies only on
\((\rho_k-R/8,\rho_k)\), and the second only on
\((2\rho_k,2\rho_k+R/8)\).  Since \(k\ge1\),
\(2\rho_k+R/8<3\rho_k\).  The two collars and the
\(B_{3\rho_k}\) inclusion are correct.

### 2.2 Shell-scale pressure and gauge: (S.344)

At almost every time, the translated periodic pressure obeys

\[
 -\Delta\widetilde\pi_R
 =\partial_i\partial_j
   (\widetilde v_{R,i}\widetilde v_{R,j})
\]

on the Euclidean lift.  Because \(\zeta_{\rho_k}=1\) on
\(B_{3\rho_k}\), the Riesz definition in (S.344) gives

\[
 -\Delta(\widetilde\pi_R-p_{k,R}^{\rm loc})=0
 \quad\hbox{in }B_{3\rho_k}.
\]

Weyl's lemma supplies the harmonic representative needed on both collars.
Subtracting \(c_R(t)\) preserves harmonicity, while incompressibility and
compact support give

\[
 \int_{\mathbb R^3}c_R(t)\widetilde v_R\cdot\nabla\psi_k^R=0.
\]

Thus the split is compatible with the fixed payment gauge.

### 2.3 Signed identity and scale: (S.345)--(S.347)

Substituting
\(\widetilde\pi_R-c_R=p_{k,R}^{\rm loc}
+(h_{k,R}^{\rm pr}-c_R)\) in the inherited flux gives exactly the cubic,
local-pressure, harmonic-pressure, and negative drift rows in (S.346).
Their signed sum is (S.345).

Under \(t=s_R+R^2\sigma\), the prefactor becomes

\[
 R^2{\gamma_k\over R}=\gamma_kR.
\]

This proves the normalization in (S.347).  A bare \(C\gamma_k\) is
available only after \(R|\nabla\psi_k^R|\le C\).

## 3. Component payment and the two tails

### 3.1 Local and harmonic pressure: (S.348)

For the dimensionless local-pressure majorant, the time change and cutoff
gradient give

\[
 \|\widehat h_{k,R}^{\rm loc}\|_{L^1_\sigma}
 \le {C\gamma_k\over R^2}
 \int_{\mathcal T_R}\int_{B_{3\rho_k}}
 |p_{k,R}^{\rm loc}|\,|\widetilde v_R|.
\]

Calderon--Zygmund and spatial Holder yield

\[
 \int_{B_{3\rho_k}}|p_{k,R}^{\rm loc}|\,|\widetilde v_R|
 \le C\int_{B_{4\rho_k}}|\widetilde v_R|^3.
\]

There is no adverse hidden weight shift.  If
\(y\in A_j(2R)\setminus B_{8R}\), then
\(y\in B_{4\rho_k}\) forces \(k\ge j\), apart from null boundaries.  Hence

\[
 \sum_{k:y\in B_{4\rho_k}}\gamma_k
 \le\sum_{k\ge j}\gamma_k\le C\gamma_j.
\]

Inside \(B_{8R}\), the full coefficient sum is finite.  This proves the
comparison with \(\mathbf1_{B_{8R}}+W_{2R}\) and pays the local row.
The pointwise inequality

\[
 |h_{k,R}^{\rm pr}-c_R|\,|\widetilde v_R|
 \le|\widetilde\pi_R-c_R|\,|\widetilde v_R|
   +|p_{k,R}^{\rm loc}|\,|\widetilde v_R|
\]

pays the harmonic row by the inherited fixed-gauge pressure row plus the
local row.  The cubic row is direct, and the inherited Jensen--Young bound
pays the drift.  This proves (S.348), but only as
\(\ell^1(L_t^1)\lesssim P_R^M\).

### 3.2 Explicit tail versus best deletion: (S.349)

The best-\(K\) deletion and explicit index tail are distinct:

\[
 \mathfrak H^F_{4/3,K,R}
 =\inf_{\#S\le K}\sum_{k\notin S}\|h_{k,R}\|_{4/3},
 \qquad
 \mathfrak T^F_{4/3,K,R}
 =\sum_{k>K}\|h_{k,R}\|_{4/3}.
\]

Taking \(S=\{1,\ldots,K\}\) proves the first inequality.  The Step 13
shellwise envelope proves the second.  Super-Gaussian summability gives
\(\sup_{R\le R_*}T_K(R)\to0\), but the energy bracket has no uniform
\(P_R^M\)-bound.  The conclusion is fixed-solution and fixed-scale only.

## 4. Collar indices and smooth spikes

### 4.1 Doubled-radius indices: (S.350)--(S.352)

Radially,
\(A_j(2R)=[2^{j+1}R,2^{j+2}R)\).  Therefore
\[
 C_{k,R}^+\subset A_k(2R),\qquad
 C_{k,R}^-\subset A_{k-2}(2R)\quad(k\ge3).
\]
The first two inner collars lie in the core.  Moreover,
\[
 {\gamma_k\over\gamma_{k-2}}
 =\exp\!\left(-{15\,4^{k-3}\over32}\right),
\]
while the outer ratio is \(\gamma_k/\gamma_k=1\).  A finite deletion
cannot remove infinitely many aligned outer faces.

### 4.2 Smooth spike: (S.353)--(S.355)

With \(M=N+1\) and \(w_i=\alpha_i=\gamma_{k_i}\),
\[
 w_i\|g_i\|_1={P\over M},\qquad
 H_i={P\over M}\phi_d.
\]
Thus the weighted payment is exactly \(P\).  Since
\(\|\phi_d\|_p=\|\phi\|_p d^{1/p-1}\), deletion of at most \(N\)
equal coordinates leaves
\[
 {P\over N+1}\|\phi\|_p d^{1/p-1}.
\]
This diverges as \(d\downarrow0\) for every \(p>1\), including
\(p=\infty\).  The indices may be chosen beyond arbitrary \(K_0\).
The rates are smooth scalars, not fluxes of one NSE solution.  Hence
(S.355) obstructs only the stated \(L^1\)-based method.

## 5. Cubic incidence accounting

### 5.1 Countable Holder: (S.356)--(S.358)

On a finite incidence submultiset,
\[
 \sum a_{\nu k}
 \le
 \left(\sum {a_{\nu k}^3\over p_\nu^2}\right)^{1/3}
 \left(\sum p_\nu\right)^{2/3}.
\]
The zero-payment convention handles every zero denominator, and monotone
convergence gives the countable form.  Repeated incidences occur in both
sums.  Adding the \(q\)-row and testing the one set \(E_\tau\) in the
best-\(N_b\) functional proves (S.358), conditional on (S.356)--(S.357).

### 5.2 Exact cube exponent: (S.359)

Holder gives
\[
 \sum_i c_ip_i^{2/3}
 \le(\sum_i c_i^3)^{1/3}(\sum_i p_i)^{2/3}.
\]
Equality holds at \(p_i=c_i^3/\sum_jc_j^3\) when the denominator is
positive.  Thus (S.359) is exact, and node-to-incidence multiplicity
cannot be omitted.

## 6. Scale-invariant measure and first roots

### 6.1 Pullback and children: (S.360)--(S.361)

For the rescaled velocity \(U(\sigma,z)=R\widetilde v_R(t,X_R+Rz)\),
\[
 |\nabla_x\widetilde v_R|^2\,dx\,dt
 =R|\nabla_zU|^2\,dz\,d\sigma.
\]
The anomalous local-energy measure has the same scaling.  Hence \(R^{-1}\)
is the correct factor in (S.360).  Halving parabolic radius gives eight
spatial children and four temporal children, hence 32.  Half-open cells
preserve exact additivity even for boundary atoms.

### 6.2 Root bounds and cancellation: (S.362)--(S.365)

For a non-top first crossing,
\[
 \lambda\rho_Q<m_Q\le m_{Q^+}
 \le\lambda\rho_{Q^+}=2\lambda\rho_Q.
\]
First roots form an antichain, so
\(\sum_Q\rho_Q\le\mathfrak M_R/\lambda\).  A top already above level is
recorded separately.  The factorization is exact:
\[
 \rho_Q^{1/3}
 (m_Q^{3/2}\rho_Q^{-1/2})^{2/3}=m_Q.
\]
Also,
\[
 \sum_Qp_Q
 =\sum_Qm_Q\Theta(Q)^{1/2}
 \le(2\lambda)^{1/2}\mathfrak M_R.
\]
Consequently the Holder product equals
\[
 (\mathfrak M_R/\lambda)^{1/3}
 ((2\lambda)^{1/2}\mathfrak M_R)^{2/3}
 =2^{1/3}\mathfrak M_R.
\]
The density level cancels exactly; this is a threshold no-gain statement,
not a shell-flux lower bound.

## 7. Jumps, Dini sum, and explicit corona

### 7.1 First relative jumps: (S.366)--(S.368)

First \(\kappa\)-jump descendants form an antichain.  Therefore
\[
 \kappa{m_S\over\rho_S}\sum_Q\rho_Q
 <\sum_Qm_Q\le m_S,
\]
which is (S.366).  Since every proper descendant has
\(\rho_Q\le\rho_S/2\), for \(\alpha\ge1\),
\[
 \sum_Q\rho_Q^\alpha
 \le(\rho_S/2)^{\alpha-1}\sum_Q\rho_Q
 \le{2^{1-\alpha}\over\kappa}\rho_S^\alpha.
\]
This proves (S.367).  Iteration gives the uniform geometric sum (S.368).

### 7.2 Pointwise strictness is insufficient: (S.369)

For \(\theta_d=(d+1)/(d+2)\),
\[
 \prod_{j=0}^{n-1}\theta_{d_0+j}
 ={d_0+1\over d_0+n+1}.
\]
The sum over \(n\) diverges.  A strict factor at each generation is not a
uniform Dini condition.

### 7.3 Explicit compatible corona measure: (S.370)

The displayed masses are consistent with a finite measure.  Choose a
point \(t_*\) in one nested temporal branch and normalized Lebesgue
measure on the spatial root cube:
\[
 \nu=m_0\delta_{t_*}\otimes
 |Q_0^x|^{-1}\mathbf1_{Q_0^x}\,dx.
\]
It puts all temporal mass in one child and splits it equally among eight
spatial children.  At depth \(d\),
\[
 \rho_v=2^{-d}\rho_0,\quad
 m_v=8^{-d}m_0,\quad
 \Theta(v)=4^{-d}\Theta(0).
\]
There is no relative upward jump.  Separately, the Step 13 incidence
coefficient has \(c_{\rm child}=c_S/2\), so
\(8(c_S/2)^3=c_S^3\).  This \(c\) is not the root coefficient
\(\rho^{1/3}\) in (S.363).  The construction is abstract, not an NSE
realization.

## 8. Single-lift shell incidence: (S.371)

For unperiodized lifted supports, the radial gap between shell \(k\) and
shell \(k+2\) is at least
\[
 (4\rho_k-R/8)-(2\rho_k+R/8)
 =2\rho_k-R/4\ge15R/4.
\]
A physical spatial set of diameter at most \(2R\) cannot meet both, so it
meets at most two shell supports.  This also covers derivative collars.

The statement is deliberately single-lift.  It is not a bound for one
torus cell against all periodized copies.  The open construction must
unfold first and count every copy and forest overlap as another incidence.
The geometry alone does not pay drift or the low-transition corona.

## 9. Exact heat shear: (S.372)--(S.374)

The field in (S.372) is divergence free, has zero nonlinear term, and
satisfies \(\partial_tu-\Delta u=0\), so it is an exact smooth NSE
solution with \(p=0\).  Its viscous density is a time factor times
\(\cos^2(2^Lx_2)\).

For a dyadic parent at depth \(d<L\), each child \(x_2\)-interval has
length \(2\pi/2^{d+1}\), an integer number of periods of
\(\cos^2(2^Lx_2)\).  Each spatial child therefore receives one eighth of
the parent's mass, proving (S.373).

The mollified path velocity is parallel to \(e_1\), and the moving field
depends on \(y_2\), not \(y_1\).  Every physical-flux row is a
\(y_1\)-independent coefficient times \(\partial_{y_1}\Psi_k^R\).
Periodic integration proves (S.374).  The family is a narrow no-go for
inferring flux from a raw tree, not a counterexample to (S.342) or (S.375).

## 10. The open jump--corona lemma

### 10.1 Quantifiers in (S.375)

The proposition is mathematically closed as an **OPEN sufficient lemma**:

- nonnegative collar rows are unfolded before incidence is measured;
- a countable locally finite forest from finitely many shifted grids covers
  the full unbounded lifted shell family;
- every top has a quantified positive level \(\lambda_T\);
- \(\kappa,N_b,C_q,C_p,C_{\rm cor}\) are universal and independent of the
  solution, scale, terminal, levels, top count, and depth;
- one set \(E_\tau\), \(\#E_\tau\le N_b\), is common to defect,
  high-Rayleigh, forest, and payment channels;
- top and corona rows together have the \(C_qA_R\) budget, including drift
  and every node not reached by the jump skeleton; and
- payment and coefficient sums run over the full incidence multiset,
  repeating periodic copies, forest overlaps, and repeated shell uses.

The measure-tree facts do not construct these rows or prove the top,
corona, payment, or cubic-incidence budgets.

### 10.2 Conditional conclusion: (S.376)

Assuming every line of (S.375), take
\(q_k=q_k^{\rm top}+q_k^{\rm cor}\) and use its full incidence multiset
in (S.356)--(S.358).  Without changing \(E_\tau\), this gives
\[
 \mathcal S_{N_b}(b(\tau))
 \le(C_q+C_{\rm cor}^{1/3}C_p^{2/3})A_R.
\]
Thus (S.376) and the ancestor gate follow conditionally.  The Holder step
is proved; the PDE antecedent is not.

## 11. Equation-by-equation disposition

| Equation | Disposition | Checked point |
|---|---|---|
| (S.343) | PASS | Two derivative collars and \(B_{3\rho_k}\) support. |
| (S.344) | PASS | Same Poisson source locally; harmonic remainder and fixed gauge. |
| (S.345) | PASS | Four signed rows sum to the AC flux derivative. |
| (S.346) | PASS | Signs, fields, pressure split, and \(\gamma_k/R\) prefactor. |
| (S.347) | PASS | \(\gamma_kR\) dimensionless normalization. |
| (S.348) | PASS / INHERITED | Local CZ closure; final bound is linear \(L_t^1\). |
| (S.349) | PASS / NONUNIFORM | Best deletion is bounded by, but differs from, explicit tail. |
| (S.350) | PASS | Outer index \(k\), inner index \(k-2\). |
| (S.351) | PASS | Exact super-Gaussian ratio. |
| (S.352) | PASS | Exact aligned ratio one. |
| (S.353) | PASS / ABSTRACT | Weighted \(L^1\) payment equals \(P\). |
| (S.354) | PASS / ABSTRACT | Fixed deletion leaves one equal spike. |
| (S.355) | PASS / METHOD ONLY | Divergence for \(p>1\); no NSE realization. |
| (S.356) | PASS AS SETUP | Nonnegative incidence inequality is well defined. |
| (S.357) | PASS AS HYPOTHESIS | Repeated payment and zero convention retained. |
| (S.358) | PASS / CONDITIONAL | Incidence Holder plus one exception set. |
| (S.359) | PASS | Exact dual exponent and equality case. |
| (S.360) | PASS | \(R^{-1}\) total-measure normalization. |
| (S.361) | PASS | Eight spatial times four temporal children. |
| (S.362) | PASS | Parent factor two and antichain radius sum. |
| (S.363) | PASS | Exact critical factorization. |
| (S.364) | PASS | Root cube and payment sums. |
| (S.365) | PASS / NO-GAIN | Exact cancellation of \(\lambda\). |
| (S.366) | PASS | First-jump antichain bound. |
| (S.367) | PASS | Strict coefficient \(2^{1-\alpha}/\kappa\). |
| (S.368) | PASS | Uniform geometric Dini sum. |
| (S.369) | PASS | Strict factors with divergent product sum. |
| (S.370) | PASS / ABSTRACT | Explicit decreasing-density measure; critical independent coefficient. |
| (S.371) | PASS / SINGLE LIFT | Two-shell incidence after unfolding only. |
| (S.372) | PASS | Exact smooth heat shear. |
| (S.373) | PASS | Exact dyadic spatial mass split. |
| (S.374) | PASS | Every physical shell flux vanishes. |
| (S.375) | PASS AS OPEN LEMMA | Forest, levels, common deletion, budgets, and independence quantified. |
| (S.376) | PASS / CONDITIONAL | Direct application of the incidence theorem. |

## 12. Literature and final claim boundary

The primary-source metadata and broad scopes match the cited papers:
[Caffarelli--Kohn--Nirenberg](https://doi.org/10.1002/cpa.3160350604)
supplies suitable-weak partial regularity;
[Yang](https://doi.org/10.4171/AIHPC/20) supplies covering and maximal
functions for cylinders following mollified-flow trajectories;
[Koch--Tataru](https://doi.org/10.1006/aima.2000.1937) supplies a critical
\(BMO^{-1}\) solution framework with Carleson-type spacetime control;
[Lei--Ren](https://doi.org/10.1016/j.aim.2024.109654) supplies quantitative
partial regularity through energy pigeonholing and scale iteration; and
[Guevara--Phuc](https://doi.org/10.1007/s00526-017-1151-7) supplies
pressure-sensitive local-energy and epsilon-regularity estimates.

None of these sources states the common-terminal, fixed-physical-shell
deletion estimate (S.342) or the payment-additive corona lemma (S.375).
This is a bounded collision check, not an exhaustive review, novelty
claim, or priority claim.

**PROVED / INHERITED OR RECONSTRUCTED:** (S.343)--(S.352),
(S.356)--(S.369), (S.371), and (S.372)--(S.374), only in their displayed
analytic, algebraic, geometric, or exact-family scopes.

**ABSTRACT METHOD OBSTRUCTIONS, NOT NSE COUNTEREXAMPLES:**
(S.353)--(S.355) and (S.370).

**CONDITIONAL:** (S.358) on (S.356)--(S.357), and (S.376) on (S.375).

**OPEN:** (S.342); the PDE existence claim (S.375), including its
top-boundary, low-transition-corona, and drift charges; (S.288); (S.303);
Step 11 (S.272); Q.12; Q.1; scale contraction; regularity; singularity
formation; and the Millennium problem.

The audited result is a method boundary and a precise open interface.  It
does not resolve the Clay problem.  **PASS / NOT CLAY.**
