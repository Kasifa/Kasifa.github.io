# R0.74N independent analytic audit — exact all-shell synthesis

## 1. Binding and verdict

This audit independently reconstructed the shell estimate in
research/r074n_all_shell_synthesis.md from the frozen shell decomposition
and the exact interfaces of R0.74F, R0.74K, R0.74L, and R0.74M. It did not
infer the full annular estimate merely from the older rowwise exponent
table.  The later endpoint consequence is a separate cross-note synthesis;
it is audited in research/r074n_crossnote_implication_independent_audit.md
and is not attributed to the shell estimate alone.

The candidate sources were uncommitted worktree files on
codex/r074n-all-shell-synthesis at the time of reconstruction. The hashes
below are the exact binding of this verdict.

| Object | SHA-256 | Audit role |
|---|---|---|
| research/r074n_problem_freeze.md | 4b2df724cf81cf28d0c9b89636ae166ade11746f623ca2a3466f08e4e1adfacc | frozen target, complete cutoff, and post-closure correction |
| research/r074n_all_shell_synthesis.md | ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e | final shell theorem plus separately sourced cross-note corollary |
| research/r074n_gap_matrix.md | 986a2ddc20318f6f70a968f80fd972c671e7ae43fe769e2acd00d4230d08fb06 | final familywise and open-claim boundary |
| research/r074f_two_packet_survival.md | 0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb | packet PDE, datum, inversion |
| research/r074h_collar_flux_two_regime_closure.md | 8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1 | inherited signed-flux energy closure |
| research/r074j_matching_payment_law.md | d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad | inherited common payment law |
| research/r074k_single_collar_shear_lag_reduction.md | 8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3 | collar-observable implication |
| research/r074l_forward_bridge_bv_reduction.md | d920e3845b38f75f187a78193b874e18d4551adf7dc03db59d5e785451654bf8 | common-forward law and main shell |
| research/r074l_main_collar_independent_audit.md | 11375ac767b14a1656ecc62dd84140b642b2a02d0c75fd5f69a9bc0a0aa70348 | inherited main-shell audit |
| research/r074m_final_segment_expulsion.md | 0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0 | support-conditioned expulsion |
| research/r074m_nearest_inward_independent_audit.md | 6e81954068dbcf588c857a6ebb1e1dcc80c70d6c926f8631aba8b2bff84c281c | inherited expulsion audit |
| research/r074n_crossnote_implication_independent_audit.md | 7c289055939cdbf21780337e7da2a1d91109172d89a6c168258703124b50be8a | independent endpoint consequence and component boundary |

**Verdict: PASS.** No mathematical obstruction, lost shell, missing packet
term, power mismatch, or unjustified infinite-tail interchange was found.
The candidate proves

\[
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5
\]

for the one frozen R0.74F--H family and all sufficiently large \(j\). It
consequently proves the matching upper and two-sided scale for the
familywise collar observable through R0.74K Theorem 4.1.  When this new
collar bound is combined, after the shell proof, with the pre-existing
R0.74H signed-flux energy closure, R0.74J payment law, and R0.74F endpoint
lower bound, the separately audited Corollary 6.2 gives the matching
familywise \(X_j\) law.  No universal endpoint theorem or regularity
statement follows. **NOT CLAY.**

## 2. Finite signed decomposition and the exact factor four

For fixed \(j\) and \(N\ge j+1\), the three index sets

\[
 \{1,\ldots,j-1\},\qquad \{j\},\qquad \{j+1,\ldots,N\}
\]

are pairwise disjoint and exhaust \(\{1,\ldots,N\}\). Thus (1.3)--(1.4)
is an identity. Every \(\tau\in I_R=(64R^2,65R^2)\) satisfies
\(\tau>s_R=61R^2\), so all time integrals have the displayed orientation.

Put

\[
 w_k(t,x)=\eta_R(t)\theta(t,x_3)\partial_2\psi_k^R(x).
\]

Since \(0\le\eta_R\le1\), \(\Gamma_k>0\), and
\([\int f]_+\le\int[f]_+\),

\[
\begin{aligned}
 [\mathcal I_<(\tau)]_+
 &\le \int_{s_R}^{\tau}\!\int_{\mathbb R^3}
 \sum_{k=1}^{j-1}\Gamma_k[w_k(t,x)]_+
 |F(t,x_2,x_3)|^2\,dx\,dt.
\end{aligned}
\tag{A.1}
\]

This is the required passage from the positive part of the sum to a
shellwise positive majorant. It uses no cancellation among shell rows.

For every radial cutoff, \(\partial_2\psi_k^R\) is odd under full inversion,
and \(\theta(t,x_3)\) is odd. Hence
\([\theta\partial_2\psi_k^R]_+\) is even. The exact relation

\[
 F^-(t,x_2,x_3)=-F^+(t,-x_2,-x_3)
\]

makes the two positive self-majorants equal after \(x\mapsto-x\). Since

\[
 |F^++F^-|^2\le2(|F^+|^2+|F^-|^2),
\]

(A.1) is at most four times the positive-packet majorant:

\[
 2\quad\hbox{(quadratic packet majorization)}
 \times 2\quad\hbox{(equal self terms)}=4.
\tag{A.2}
\]

The cross term is covered, but no cross-packet cancellation is claimed.

## 3. Combined inward chord and exact periodization

For a single shell,

\[
 |\partial_2\psi_k^R|\le C/R,\qquad
 \operatorname{length}_{x_1}
 (\operatorname{supp}\partial_2\psi_k^R)\le C2^kR.
\]

The \(R/8\) padding is harmless because \(k\ge1\). Thus

\[
 \int_{\mathbb R}[\theta\partial_2\psi_k^R]_+\,dx_1\le C2^k.
\tag{A.3}
\]

Consequently,

\[
 0\le D_<
 \le C\sum_{k=1}^{j-1}2^ke^{-4^{k-1}/32}
 \le C\sum_{k\ge1}2^ke^{-4^{k-1}/32}=:C_*<\infty.
\tag{A.4}
\]

For example, convergence follows from

\[
 \frac{2^{k+1}\Gamma_{k+1}}{2^k\Gamma_k}
 =2\exp\!\left(-\frac{3\,4^{k-1}}{32}\right)\longrightarrow0.
\]

All \(k\le j-1\) supports lie in

\[
 |x|\le r_-=2^jR+\frac R8.
\tag{A.5}
\]

Because \(LR\to0\), eventually \(r_-<1\). The torus period is \(2\pi\), so
the intervals \([-r_-,r_-]+2\pi n\) are disjoint. At most one lift in each
of the \(x_2,x_3\) coordinates contributes to the two-variable
periodization. Therefore

\[
 0\le\overline D_<\le C_*,
\]

and a nonzero periodized value selects unique small lifts satisfying
\(|x_2|_{\rm lift},|x_3|_{\rm lift}\le r_-\). This uniqueness concerns only
the compact collar support; it does not discard any packet or heat-kernel
winding.

The normalized Jensen bound is linear in a nonnegative endpoint
multiplier. Applying it shell by shell and then Tonelli replaces the
individual chords by exactly \(D_<\). Exact unfolding gives

\[
 [\mathcal I_<(\tau)]_+\le4\mathcal P_<(\tau),
\tag{A.6}
\]

with the \(R^6\), one endpoint factor \(K_T(X_t)\), the correlated shift
\(q_\omega=Q-\mathfrak S_t^\leftarrow[X]\), and all windings exactly as in
(2.7). No independence between \(X_t\), chord support, and
\(\mathfrak S_t^\leftarrow\) is introduced.

## 4. Exact transfer of the R0.74M expulsion mechanism

The R0.74M pathwise mechanism uses only:

1. chord nonnegativity;
2. a pointwise chord bound; and
3. endpoint support within \(r_-\) in both periodic coordinates.

The new \(\overline D_<\) has all three properties. Its \(C_*\) bound is
stronger than the \(CL\) bound for the single complete \(j-1\) chord, and
its largest support radius is identical.

For

\[
 \mathcal H_t=
 \left\{\sup_{t-R^2/64\le s\le t}
 |\widetilde X_s-\widetilde X_t|\le LR/16\right\},
\]

Brownian reflection for generator \(\partial_x^2\) gives

\[
 \mathbb P(\mathcal H_t^c)
 \le4\exp\!\left[-\frac{(LR/16)^2}{4(R^2/64)}\right]
 =4e^{-L^2/16}.
\tag{A.7}
\]

On supported good endpoints,

\[
 |h+X_s|_{\rm lift}
 \le\left(\frac{32}{63}+\frac1{16}\right)LR+\frac R8
 \le\frac35LR
\tag{A.8}
\]

for sufficiently large \(L\). The exact coefficient reserve

\[
 \frac35-\frac{32}{63}-\frac1{16}=\frac{149}{5040}>0
\]

absorbs the remaining \(R/8\); the inherited sufficient threshold
\(L\ge63/8\) works.

R0.74M's caloric-defect and plateau lemmas apply exactly on (A.8), so

\[
 \mathfrak S_t^\leftarrow[X]\ge
 \Sigma_L:=\frac1{32768}e^{-L^2/640}.
\tag{A.9}
\]

After increasing \(j_0\),

\[
 q\le\frac14\Sigma_L,\qquad
 r_-\le\frac14\Sigma_L,\qquad
 2R\le\Sigma_L<1,
\tag{A.10}
\]

because

\[
 \frac{\Sigma_L}{LR}
 =\frac{e^{L^2/640}}{32768L}\longrightarrow\infty.
\]

The unchanged pathwise range
\(-81/32\le q_\omega\le-3\Sigma_L/4\), the horizontal support condition,
and the torus triangle inequality yield

\[
 \operatorname{dist}_{\mathbb T}(u,0)\ge\frac12\Sigma_L.
\tag{A.11}
\]

Thus the transfer is the same support-conditioned implication, not a
rowwise analogy.

## 5. Independent good/bad power ledger

For \(s_R\le t\le\tau\le65R^2\),

\[
 62R^2\le T=R^2+t\le66R^2,\qquad
 \|K_T\|_\infty\le CR^{-1},\qquad
 \int_{\mathbb T}|\partial K_T|^2\le CR^{-3}.
\]

Without any independence assumption,

\[
\begin{aligned}
 \mathcal P_<^{\rm bad}
 &\le C
 \underbrace{R^6}_{\rm packet\ square}
 \underbrace{R^2}_{\rm time}
 \underbrace{R^{-1}}_{K_T}
 \underbrace{1}_{\overline D_<}
 \underbrace{R^{-3}}_{\|\partial K_T\|_2^2}
 e^{-L^2/16}\\
 &=CR^4e^{-L^2/16}.
\end{aligned}
\tag{A.12}
\]

Dividing by \(\Gamma_jLR^5\) leaves

\[
 L^{-1}\exp\!\left[
 -\left(\frac1{16}-\rho-c_\gamma\right)L^2\right],
\]

and

\[
 \frac1{16}-\frac1{320}-\frac8{3969}
 =\frac{72851}{1270080}>0.
\tag{A.13}
\]

On the good event, (A.11) restricts the derivative kernel to its periodic
tail. The R0.74M tail bound gives

\[
\begin{aligned}
 \mathcal P_<^{\rm good}
 &\le CR^6R^2R^{-1}R^{-4}
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right)\\
 &=CR^3\exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right).
\end{aligned}
\tag{A.14}
\]

Here

\[
 \frac{\Sigma_L^2}{1056R^2}
 =\frac1{1056\cdot32768^2}
 \exp\!\left(\frac{L^2}{320}\right),
\]

which eventually dominates \((c_\gamma+2\rho)L^2\). Hence

\[
 \exp\!\left(-\frac{\Sigma_L^2}{1056R^2}\right)
 \le\Gamma_jR^2
\]

and

\[
 \mathcal P_<^{\rm good}
 \le C\Gamma_jR^5
 \le C\Gamma_jLR^5.
\tag{A.15}
\]

Equations (A.2), (A.12), and (A.15) cover all inward shells, both packet
signs, their cross term, both radial faces, and every winding.

## 6. Exact binding of the target shell

R0.74L proves its bridge majorant at scale \(CLR^5\). Its frozen consequence
(R0.74L (F.7)--(F.8)), independently audited in the bound source, is

\[
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}|\theta|\,|F|^2
 |\partial_2\psi_j^R|\,dx\,dt
 \le CLR^5
\tag{A.16}
\]

uniformly for \(\tau\in I_R\). Thus

\[
 |\mathcal I_=(\tau)|\le C\Gamma_jLR^5.
\tag{A.17}
\]

This is the exact true-packet target shell; no free packet or central
winding is substituted.

## 7. Maximum principle and the complete outer collar

Each packet solves

\[
 \partial_tF^\pm+B\theta(t,x_3)\partial_2F^\pm
 =\Delta_{23}F^\pm.
\]

Its initial datum is

\[
 R^3\partial K_{R^2}(x_2-q_{\rm pre})K_{R^2}(x_3-h)
\]

up to inversion. Since
\(\|\partial K_{R^2}\|_\infty\le CR^{-2}\) and
\(\|K_{R^2}\|_\infty\le CR^{-1}\), the initial \(L^\infty\) norm is uniform
in \(R\). The scalar parabolic maximum principle and the two-packet
triangle inequality give

\[
 \|F(t)\|_{L^\infty(\mathbb T^2)}\le C.
\tag{A.18}
\]

Differentiation of \(\psi_k^R\) can occur on both its inner and outer radial
faces. They are layers of width \(O(R)\), at radii \(O(2^kR)\). Their
combined Euclidean volume is

\[
 O\!\left((2^kR)^2R+(2^{k+1}R)^2R\right)=O(4^kR^3).
\]

Therefore

\[
 \int_{\mathbb R^3}|\partial_2\psi_k^R|\,dx\le C4^kR^2.
\tag{A.19}
\]

This is the complete \(\mathbb R^3\) collar against the periodic packet
lift, not a central-copy estimate. Using \(|\theta|\le1\) and a time length
at most \(4R^2\),

\[
 |\mathcal J_{j,k}(\tau)|\le C\Gamma_k4^kR^4
\tag{A.20}
\]

uniformly in \(\tau\).

## 8. Infinite outer tail and \(N\to\infty\)

For \(a_k=4^k\Gamma_k\),

\[
 \frac{a_{k+1}}{a_k}
 =4\exp\!\left(-\frac{3\,4^{k-1}}{32}\right).
\tag{A.21}
\]

This is at most \(1/2\) for every \(k\ge j+1\) once \(j\) is large. Hence

\[
 \sum_{k\ge j+1}4^k\Gamma_k
 \le2\,4^{j+1}\Gamma_{j+1}.
\tag{A.22}
\]

The exact identities

\[
 4^{j+1}=\frac{4096}{3969}L^2,\qquad
 \frac{\Gamma_{j+1}}{\Gamma_j}=e^{-3c_\gamma L^2}
\]

give

\[
 \sup_{\tau\in I_R}|\mathcal I_>(\tau)|
 \le C\Gamma_jL^2R^4e^{-3c_\gamma L^2}.
\tag{A.23}
\]

After division by \(\Gamma_jLR^5\), the remaining factor is

\[
 L\exp[-(3c_\gamma-\rho)L^2],
\]

and

\[
 3c_\gamma-\rho
 =\frac{24}{3969}-\frac1{320}
 =\frac{1237}{423360}>0.
\tag{A.24}
\]

Thus the whole outer tail has the target scale. Moreover, (A.20) and the
convergent nonnegative series (A.22) are a Weierstrass majorant independent
of \(\tau\). Therefore \(\mathcal I_{>,N}\) is uniformly Cauchy on \(I_R\).
The inner range is finite for fixed \(j\), and the main range is a
singleton. Hence \(\mathcal I_j^{(N)}\to\mathcal I_j\) uniformly, no shell is
lost, and the positive-part inequality passes to the limit by continuity.

## 9. Shell implication and cross-note boundary

For the limiting decomposition,

\[
 [\mathcal I_j]_+
 \le[\mathcal I_<]_++|\mathcal I_=|+|\mathcal I_>|.
\]

The three audited shell estimates prove the R0.74K hypothesis (4.3) on the
exact family. R0.74K Theorem 4.1 then uses
\(\mathfrak a_j^2=B_j^2/\Gamma_j\) and bounded \(B_jR_j^2\) to obtain only

\[
 \mathfrak C_j\le CB_j^2L_jR_j^2.
\]

Together with the separately inherited R0.74H lower bound and R0.74J scale
identity, this gives the two-sided collar-observable law stated in R0.74N.

The shell argument itself does **not** estimate the endpoint energy or
dissipation and must not be presented as if (6.3) alone implied an \(X_j\)
upper bound.  The valid additional implication is cross-note: R0.74H
Theorem 5.1 already gives

\[
 X_j\le C\left(P_j^{2/3}+\mathfrak C_j\right),
\]

R0.74J gives \(P_j^{2/3}\lesssim B_j^2R_j^2\), and the shell result above
gives \(\mathfrak C_j\lesssim B_j^2L_jR_j^2\).  R0.74F supplies the matching
lower bound through the endpoint exterior-energy component.  The exact
interfaces, non-circular dependency graph, and the absence of a dissipation
lower bound are independently checked in the bound cross-note audit.

Thus the completed corpus proves the familywise \(X_j\) law, but not an
arbitrary-flow endpoint theorem, singularity statement, or global
regularity. **NOT CLAY.**

## 10. Final source-diff and tag audit

The final proof has 61 equation tags, all unique.  They split exactly into

- the original 55-tag inventory (0.1)--(6.5); and
- six new cross-note tags (6.6)--(6.11).

The first rebind attempt failed closed because it proposed the false claim
that all old 55 displays were byte-identical.  The corrected source-diff
invariant is:

1. 53 of the old 55 displays are verbatim unchanged;
2. (0.3) is the audited summary extension which adds \(X_j\) to the already
   proved collar and payment scale;
3. (0.6) is the cutoff clarification which spells out the complete inherited
   R0.74H conditions; and
4. all 49 shell-body displays (1.1)--(6.5) are verbatim unchanged.

The new equations (6.6)--(6.11) define the endpoint components, state their
bounds, apply the H closure and J/N upper ledgers, and insert the F endpoint
lower bound.  They do not modify any inward, target, outer, or infinite-sum
estimate audited in Sections 2--8 above.

\[
 \boxed{\text{R0.74N ALL-SHELL SYNTHESIS: PASS; 61/61 TAGS; NOT CLAY.}}
\]
