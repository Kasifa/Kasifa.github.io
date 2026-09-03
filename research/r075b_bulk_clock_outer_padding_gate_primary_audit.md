# Independent primary analytic audit of R0.75B

## 0. Frozen object and verdict

Audited file: `research/r075b_bulk_clock_outer_padding_gate.md`.
Frozen SHA-256:
`430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a`.

The four dependency hashes recorded in the audited file were recomputed and
match their frozen files:

| dependency | recomputed SHA-256 |
|---|---|
| `research/r074h_collar_flux_two_regime_closure.md` | `8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1` |
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` |
| `research/r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` |
| `research/r075a_spectral_persistence_payment_dichotomy.md` | `f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388` |

**Verdict: PASS. Blocker count: 0. Minor corrections required: 0.**

The Version-M restriction, cutoff decomposition, two Caccioppoli identities,
subclock comparison, doubled-radius weight conversion, endpoint dichotomy,
blockwise temporal packing, Holder powers, and all frozen exponential signs
are correct. The enhanced note pays the entire endpoint row and leaves only
the outer-collar accumulated-dissipation row open. Its remaining positive
full-window exponent is failure of one upper-bound method, not an exact
counterexample.

## 1. Version-M zero-path scope

The zero path is valid precisely on the stated inversion-paired exact family.
The frozen construction gives

\[
 u(t,-x)=-u(t,x).
\]

Convolution with the frozen even mollifier therefore gives
\(u_R(t,0)=0\). With the Version-M terminal condition \(X_R(t_0)=0\),
uniqueness for the smooth trajectory ODE yields

\[
 X_R(t)\equiv0,\qquad a_R(t)=\dot X_R(t)\equiv0.
\]

Consequently \(v_R=u\), the shell cutoffs are unshifted, and no residual
Version-M drift term is missing. This reasoning would not apply to an
arbitrary non-inversion-paired correction or an arbitrary suitable weak
solution; the main note explicitly excludes both extensions.

The endpoint \(t_2=t_0\) is also legitimate in the asserted smooth setting.
Although the general suitable-weak clock uses the canonical absolutely
continuous representative and good-time agreement, here the classical
endpoint and all accumulated integrals extend continuously from below.

## 2. Cutoff partition and doubled-radius shell geometry

The asserted \(\chi/\xi\) partition exists with uniform constants. For
example, in the central lift choose a nonincreasing radial multiplier
\(\alpha_R\) such that

\[
 \alpha_R=1\quad\hbox{for }r\le r_k^+-R/4,
 \qquad
 \alpha_R=0\quad\hbox{for }r\ge r_k^+-R/16,
\]

with first and second derivatives bounded by \(CR^{-1}\) and \(CR^{-2}\).
Then one may take

\[
 \chi_k^R=\alpha_R\Psi_k^R,
 \qquad
 \xi_k^R=(1-\alpha_R)\Psi_k^R.
\]

Thus \(0\le\chi_k^R\le\Psi_k^R\),
\(\Psi_k^R=\chi_k^R+\xi_k^R\), and \(\xi_k^R\) is supported in a fixed
enlargement of the outer collar. Product differentiation preserves the
required first- and second-derivative bounds. On the outer component outside
the collar, \(\Psi_k^R=0\) already because its padding is only \(R/8\), so
the stated equality of \(\chi_k^R\) and \(\Psi_k^R\) outside the collar is
consistent.

The exact rescaling is

\[
 A_k(R)=A_{k-1}(2R),
 \qquad \gamma_{k-1}=\gamma_k^{1/4}=\omega^{1/4}.
\]

The safe cutoff stops a fixed positive distance before
\(r_k^+=2^{k+1}R\). Its main shell lies in \(A_{k-1}(2R)\), while its inner
\(R/8\) padding lies in \(A_{k-2}(2R)\), whose weight is still larger.
Therefore

\[
 W_{2R}\ge\omega^{1/4}
 \quad\hbox{on }\operatorname{supp}\chi_k^R.
\]

The outward part of \(\operatorname{supp}\xi_k^R\) instead enters
\(A_k(2R)\), so its best uniform lower weight is only
\(\gamma_k=\omega\). The frozen remote-chart condition makes
\(r_k^++R/8<1\) and \(r_k^+\gg R\); hence the fixed collar enlargement
neither leaves the central chart nor reaches the next doubled-radius shell.
The periodized cutoffs and the all-copy lift are therefore compatible with
this single-lift calculation, with no omitted winding multiplicity.

## 3. Caccioppoli signs and time endpoints

For

\[
 \partial_tF+b\partial_2F-\Delta_{23}F=0,
\]

multiplication by \(\eta_R\chi F\) gives the transport computation

\[
 -\int\eta_R\chi bF\partial_2F
 =\frac12\int\eta_Rb\,\partial_2\chi\,|F|^2,
\]

because \(b=b(t,x_3)\) is independent of \(x_2\). The diffusion integration
by parts gives \(+\eta_R\Delta_{23}\chi\) on the right. Hence every sign in
(B.14)--(B.15) is correct.

Likewise \(\partial_tb-\partial_3^2b=0\) gives exactly

\[
 \frac12\int\chi|b(t_2)|^2
 +\int_{s_R}^{t_2}\!\int\eta_R\chi|\partial_3b|^2
 =\frac12\int_{s_R}^{t_2}\!\int
   (\eta_R'\chi+\eta_R\partial_3^2\chi)|b|^2,
\]

so (B.16) has the correct sign and derivative. The inherited componentwise
second-derivative cutoff bounds control both \(\Delta_{23}\chi\) and
\(\partial_3^2\chi\).

Here

\[
 [s_R,t_2]=[61R^2,65R^2]=\overline{I_{2R}},
\]

up to measure-zero endpoints. Smooth continuity and
\(\eta_R=1\) on \(I_R\) give \(\eta_R(t_2)=1\), while vanishing near
\(s_R\) removes the initial boundary term. From
\(|b|\le B\le(96R^2)^{-1}\), the cutoff coefficients satisfy

\[
 |\eta_R'\chi|+|\eta_R\Delta_{23}\chi|
 +|\eta_Rb\partial_2\chi|
 \le CR^{-3}\mathbf1_{\operatorname{supp}\chi}
\]

for \(R\le1\). Taking absolute values on the right of the exact identities
therefore yields (B.19).

## 4. Relation of \(K^\chi\) to the frozen completed clock

For this smooth zero-path family, the anomalous local-energy defect is zero
and

\[
\begin{aligned}
 K_{k,R}(t_2)={}&
 \frac{\omega}{2R}\int\Psi_k^R|u(t_2)|^2\\
 &+\frac{\omega}{R}\int_{s_R}^{t_2}\!\int
 \eta_R\Psi_k^R
 \bigl(|\nabla_{23}F|^2+|\partial_3b|^2\bigr).
\end{aligned}
\]

This is exactly the endpoint plus physical-viscosity part of the general
three-row Version-M clock. Therefore nonnegativity and
\(0\le\chi_k^R\le\Psi_k^R\) give

\[
 0\le K_{k,R}^{\rm safe}=K_{k,R}^{\chi_k^R}\le K_{k,R}.
\]

Conversely, \(\Psi_k^R\le\chi_k^R+\xi_k^R\) gives

\[
 K_{k,R}\le K_{k,R}^{\rm safe}
 +H_{k,R}^{\rm out}+D_{k,R}^{\rm out}
\]

up to the harmless fixed overlap allowed in the note. No signed flux identity
is being mistaken for this comparison: all quantities in these inequalities
are endpoint or dissipation integrals with nonnegative densities.

## 5. Spacetime volume, Holder conversion, and powers

Since \(r_k^+=pLR\), the safe support obeys

\[
 |\operatorname{supp}\chi_k^R|\le C(pLR)^3\le CL^3R^3.
\]

Multiplication by \(|I_{2R}|=4R^2\) gives spacetime volume at most
\(CL^3R^5\). Thus

\[
 \int_{I_{2R}}\!\int_{\operatorname{supp}\chi_k^R}|u|^2
 \le CLR^{5/3}
 \left(\int_{I_{2R}}\!\int_{\operatorname{supp}\chi_k^R}|u|^3
 \right)^{2/3}.
\]

The nonnegative velocity part of the doubled-radius Version-M exterior row
is

\[
 (2R)^{-2}\int_{I_{2R}}\!\int W_{2R}|u|^3.
\]

Using the safe weight \(W_{2R}\ge\omega^{1/4}\) therefore gives

\[
 \int_{I_{2R}}\!\int_{\operatorname{supp}\chi_k^R}|u|^3
 \le CR^2\omega^{-1/4}P_R^M.
\]

Substitution into (B.19) has the exact powers

\[
 R^{-4}R^{5/3}(R^2)^{2/3}=R^{-1},
 \qquad
 \omega(\omega^{-1/4})^{2/3}=\omega^{5/6},
\]

and hence proves

\[
 K_{k,R}^{\rm safe}(t_2)
 \le CLR^{-1}\omega^{5/6}(P_R^M)^{2/3}.
\]

For the outer collar,

\[
 |\operatorname{supp}\xi_k^R|
 \le C(pLR)^2R\le CL^2R^3.
\]

Its inward portion has weight at least \(\omega^{1/4}\), and its outward
portion has weight \(\omega\); hence the uniform bound on the whole support is
\(W_{2R}\ge\omega\). This geometry is used differently for its endpoint and
accumulated rows, as audited next.

## 6. Outer-collar endpoint dichotomy

Let

\[
 E(t)=\int\xi_k^R|u(t)|^2,
 \qquad
 M(t)=\int_{\operatorname{supp}\xi_k^R}|u(t)|^2.
\]

Adding the unweighted differential forms of the \(F\)- and \(b\)-identities
gives

\[
 \frac12E'(t)
 +\int\xi_k^R
   \bigl(|\nabla_{23}F|^2+|\partial_3b|^2\bigr)
 =\frac12\int
  \left[(\Delta_{23}\xi_k^R+b\partial_2\xi_k^R)|F|^2
        +(\partial_3^2\xi_k^R)b^2\right].
\]

Because \(|b|\le(96R^2)^{-1}\) and the cutoff derivatives have the frozen
bounds, discarding the nonnegative gradient term gives exactly

\[
 E'(t)\le CR^{-3}M(t).
\]

Take \(J_*=[t_2-c_0R^3,t_2]\subset I_{2R}\), decreasing the fixed \(c_0\)
if necessary. If \(E(t)\ge E(t_2)/2\) throughout \(J_*\), then
\(E\le CM\) and

\[
 \int_{J_*}M(t)\,dt\ge cE(t_2)R^3.
\]

Otherwise some \(t_*\in J_*\) has \(E(t_*)<E(t_2)/2\), and integration of
the one-sided differential inequality gives the same lower bound. These two
cases are exhaustive, including arbitrarily short smooth endpoint focusing.

The endpoint tube has measure

\[
 |J_*|\,|\operatorname{supp}\xi_k^R|
 \le CL^2R^6.
\]

Reverse Holder therefore yields

\[
 \int_{J_*}\!\int_{\operatorname{supp}\xi_k^R}|u|^3
 \ge cE(t_2)^{3/2}R^{3/2}L^{-1}.
\]

The exterior velocity row, with the uniform collar weight \(\omega\), gives

\[
 P_R^M\ge
 c\omega E(t_2)^{3/2}R^{-1/2}L^{-1}.
\]

Writing \(H_{k,R}^{\rm out}=\omega E(t_2)/(2R)\) and taking the \(2/3\)
power gives the claimed endpoint estimate

\[
 (P_R^M)^{2/3}
 \ge cH_{k,R}^{\rm out}
 R^{2/3}\omega^{-1/3}L^{-2/3}.
\]

Thus the outer endpoint, unlike the accumulated row, is paid with a strict
favorable exponential margin.

## 7. Full-window and blockwise outer dissipation

For the full-window bound, the outer spacetime volume is \(CL^2R^5\), so
Holder contributes \(CL^{2/3}R^{5/3}\). The same-weight payment gives

\[
 \int_{I_{2R}}\!\int_{\operatorname{supp}\xi_k^R}|u|^3
 \le CR^2\omega^{-1}P_R^M.
\]

Using the Caccioppoli prefactor \(C\omega R^{-4}\), and discarding its
nonnegative endpoint term, gives

\[
 D_{k,R}^{\rm out}
 \le CL^{2/3}R^{-1}\omega^{1/3}(P_R^M)^{2/3}.
\]

The \(R\)-power is \(-4+5/3+4/3=-1\), and the \(\omega\)-power is
\(1-2/3=1/3\). This is (B.38), not an endpoint estimate.

The short-block refinement is also valid. Partition \(I_{2R}\) into
\(N\le CR^{-1}\) intervals \(J_m\) of length comparable to \(R^3\), and
choose one-sided enlargements at the two temporal endpoints and
fixed-overlap enlargements \(\widetilde J_m\) in the interior. Testing with
\(\eta_R\vartheta_m\xi_k^R\), where \(\vartheta_m=1\) on \(J_m\), gives
\(|(\eta_R\vartheta_m)'|\le CR^{-3}\). At the first block the factor
\(\eta_R\) removes the initial boundary term; at the last block the terminal
endpoint term is nonnegative and may be dropped. Therefore each charged
dissipation block satisfies

\[
 D_m\le C\omega R^{-4}
 \int_{\widetilde J_m}\!\int_{\operatorname{supp}\xi_k^R}|u|^2.
\]

Each enlarged block has spacetime measure at most \(CL^2R^6\). Defining

\[
 p_m=R^{-2}\omega
 \int_{\widetilde J_m}\!\int_{\operatorname{supp}\xi_k^R}|u|^3,
\]

the blockwise Holder calculation is

\[
\begin{aligned}
 D_m
 &\le C\omega R^{-4}L^{2/3}R^2
       (R^2\omega^{-1}p_m)^{2/3}\\
 &\le CL^{2/3}R^{-2/3}\omega^{1/3}p_m^{2/3}.
\end{aligned}
\]

The fixed overlap in time and \(W_{2R}\ge\omega\) on the whole collar imply

\[
 \sum_m p_m\le CP_R^M.
\]

For \(S=\sum_mp_m>0\), the definition

\[
 N_{\rm eff}=\frac{(\sum_mp_m^{2/3})^3}{S^2}
\]

has the exact identity

\[
 \sum_mp_m^{2/3}=N_{\rm eff}^{1/3}S^{2/3}.
\]

Subadditivity for the exponent \(2/3\) gives \(N_{\rm eff}\ge1\), while
Holder gives

\[
 \sum_mp_m^{2/3}\le N^{1/3}S^{2/3},
\]

and hence \(N_{\rm eff}\le N\). If \(S=0\), all block payments and the
corresponding smooth dissipation vanish, so the convention
\(N_{\rm eff}=1\) is harmless. Summing the block estimates proves

\[
 D_{k,R}^{\rm out}
 \le CL^{2/3}R^{-2/3}\omega^{1/3}
 N_{\rm eff}^{1/3}(P_R^M)^{2/3}.
\]

Taking the worst allowed value \(N_{\rm eff}\asymp N\asymp R^{-1}\)
recovers the full-window factor \(R^{-1}\omega^{1/3}\). Thus the block
calculation neither silently assumes one active block nor closes the open
packing problem.

## 8. Exact fraction checks

Using \(p=32/63\), \(2^{k_2}=pL\), and
\(c_\gamma=8/3969\),

\[
 \omega=\gamma_{k_2-1}
 =\exp\left(-\frac{p^2L^2}{512}\right)
 =\exp\left(-\frac{c_\gamma}{4}L^2\right).
\]

With \(\rho=9/10000\), the safe exponent is

\[
 \frac\rho4-\frac{5c_\gamma}{24}
 =\frac9{40000}-\frac5{11907}
 =\frac{107163-200000}{476280000}
 =-\frac{92837}{476280000}<0.
\]

The outer-endpoint gain is

\[
 \frac{c_\gamma}{12}-\frac\rho6
 =\frac2{11907}-\frac3{20000}
 =\frac{40000-35721}{238140000}
 =\frac{4279}{238140000}>0.
\]

The full-window outer-dissipation exponent is

\[
 \frac\rho4-\frac{c_\gamma}{12}
 =\frac9{40000}-\frac2{11907}
 =\frac{107163-80000}{476280000}
 =\frac{27163}{476280000}>0.
\]

The one-effective-block rate is its negative,

\[
 \frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
\]

Consequently the temporal-packing condition is exactly

\[
 \limsup_{L\to\infty}\frac{\log N_{\rm eff}}{L^2}
 <3\left(\frac{c_\gamma}{12}-\frac\rho6\right)
 =\frac{4279}{79380000}.
\]

The factor three and strict inequality direction in (B.44) are correct:
\(N_{\rm eff}^{1/3}\) contributes one third of its logarithmic growth rate.

## 9. Ledger completeness and claim boundary

- The shear \(b\) is included in its own exact heat identity, in the endpoint
  norm \(|u|^2=|F|^2+b^2\), and in the full smooth dissipation. It is not
  silently discarded.
- The anomalous defect row vanishes only because the audited theorem is
  restricted to exact smooth solutions. The note does not extend the
  Caccioppoli subclock conclusion to arbitrary suitable weak solutions.
- Periodic copies are retained by the periodized cutoff and all-copy lift;
  the small central-chart geometry prevents a hidden multiplicity factor in
  the displayed local estimates.
- The use of \(P_R^M\) keeps all of its initial/core, pressure, and harmonic
  rows: the proof merely lower-bounds the total nonnegative payment by its
  doubled-radius exterior velocity row. In the present exact common-shear
  solution the pressure itself is zero. The proposed future counterexample is
  correctly required to account for every one of these rows.
- The terminal \(R^3\) dichotomy controls the outer endpoint, while the safe
  estimate controls the complementary endpoint. Thus the whole endpoint row
  is paid; the note does not leave that row open together with dissipation.
- The positive rate in (B.39) says only that the coefficient in the derived
  full-window dissipation upper bound is not uniformly absorbable. It supplies
  no lower bound on an exact solution and therefore no counterexample. The
  main note says this explicitly.
- No strip lower bound is used as a whole-shell upper bound. Only the
  outer-collar accumulated dissipation prevents closure of full
  \(K_{k,R}\). Fixed deletion, arbitrary suitable weak solutions, and every
  regularity or singularity consequence remain open.

## 10. Mechanical audit

The source has 47 unique equation tags: `B.1`--`B.46` together with
`B.6a`. All internal numbered references resolve, including the external
reference to `A.63`. The 46 display-math opening delimiters match 46 closing
delimiters, the five `begin` environments match five `end` environments, and
no nonprinting ASCII control character was found.

\[
\boxed{
\begin{gathered}
\textbf{ANALYTIC VERDICT: PASS;}\\
\textbf{BLOCKERS: 0;}\\
\textbf{MINOR CORRECTIONS REQUIRED: 0.}
\end{gathered}}
\]

This audit makes no novelty determination and proves no Navier--Stokes
regularity or singularity result. \(\mathbf{NOT\ CLAY}\).
