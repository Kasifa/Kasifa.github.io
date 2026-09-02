# R0.74Q gap matrix — effective shells and relaxed multipacket stress tests

## Scope

This matrix covers the R0.74Q problem freeze, the common-shear gate in
Step 1, and the relaxed multipacket cubic obstruction in Step 2. It
separates exact finite-family theorems, inherited analytic inputs, finite
arithmetic checks, conditional mechanisms, and the remaining arbitrary-flow
gaps. Every multipacket result below concerns an explicit smooth periodic
family. No terminal-clock lower bound is promoted to a signed-flux theorem.
**NOT CLAY.**

| ID | Statement | Evidence | Status | Exact boundary |
|---|---|---|---|---|
| Q1 | The inherited Version-M shell ledger satisfies \(K_{k,R}=Q_{k,R}+F_{k,R}\), \(K_{k,R}(s_R)=0\), \(K_{k,R}\ge0\), and \(\sum_k\operatorname{TV}Q_{k,R}\le C(P_R^M)^{2/3}\). | Problem freeze (Q.2)--(Q.5); R0.74P | INHERITED / PROVED | Fixed \(R\), prescribed terminal centre, and the R0.74P mollified trajectory. |
| Q2 | For every fixed integer \(N\ge0\), \(\mathfrak C_R^M\le C(P_R^M)^{2/3}+\sqrt N\,Y_{2,R}^{\rm sf}+\mathcal S_{N,R}^{K}\); the analogous flux-residual estimate also holds. | Problem freeze, Proposition 2.1, (Q.7)--(Q.11) | PROVED | This is an exact terminal reduction. The exceptional set may depend on the terminal time. |
| Q3 | A uniform estimate \(\mathcal S_{N_0,R}^{K}\le C(P_R^M)^{2/3}\), or its signed \(F\)-version, would imply \(\mathfrak C_R^M\le C[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}]\). | Problem freeze (Q.12) | CONDITIONAL / OPEN | \(N_0\) and \(C\) must be independent of \(R\) and of the solution. No such PDE packing estimate is proved. |
| Q4 | The stronger best-\(N_0\)-term variation tail \(\sigma_{N_0}((v_{k,R})_k)_1\le C(P_R^M)^{2/3}\) would also imply the fixed-scale estimate. | Problem freeze (Q.13)--(Q.16) | CONDITIONAL / OPEN | This is stronger than the signed terminal residual and is not established for suitable weak solutions. |
| Q5 | Shifted equal plateaux, truncated weak-\(\ell^1\) rows, and the inverse participation number show that qualitative sparsity, finite-prefix control, or a connected shell block cannot by themselves compress \(\ell^1\) to \(\ell^2\). | Problem freeze (Q.17)--(Q.19); falsification gates | PROVED / FINITE WITNESS | These are sequence-space obstructions, not Navier--Stokes counterexamples. |
| Q6 | The local-payment condition (Q.21), with an \(\ell^3\) coefficient packing after finitely many terminal exceptions, would imply (Q.12). | Problem freeze (Q.20)--(Q.22) | PROVED REDUCTION / CONDITIONAL INPUT | Hölder's inequality proves the implication; the required shell payments and coefficients are not constructed. |
| Q7 | Any finite number of inversion-paired passive packets re-evolved under one common heat shear gives an exact smooth periodic mean-zero unforced Navier--Stokes solution with \(p=0\). | Step 1, Proposition 1.1, (Q.28)--(Q.37) | PROVED | \(N\) is finite for each solution. All packets must solve the same common-coefficient equation. |
| Q8 | Inversion parity and the even mollifier give \(X_R\equiv0\) and \(a_R=a_R'\equiv0\) for the exact common-shear family. | Step 1, Corollary 1.2, (Q.38)--(Q.40) | PROVED | The pairing is essential; an unpaired packet sum need not have the zero path. |
| Q9 | Previously evolved packets with different shears cannot simply be added: the exact residuals are \((b-b_\ell)\partial_2F_\ell\) and the cross sum in (Q.44). | Step 1 (Q.41)--(Q.44) | PROVED | This is an exact PDE residual calculation, not an estimate. |
| Q10 | The explicit saturation shear obeys \(0\le64R^2-D_R(c_hLR)\le256R^2e^{-a_DL^2}\) under the two-parameter chart hypotheses. | Step 1, Lemma 3.1, (Q.47a)--(Q.49) | PROVED | \(R\) and \(L\) are independent parameters here; the result is restricted to the stated saturation profile. |
| Q11 | The frozen terminal-angle calibration cannot be shared by two distinct dyadic shells along a survival-compatible common-\(R\) asymptotic sequence. | Step 1, Lemma 3.2 and Corollary 3.3, (Q.50)--(Q.61) | PROVED | This is an asymptotic frozen-geometry no-go, not an exact impossibility theorem for every common-shear family. |
| Q12 | The common-shear gate constants, rational exponent margins, and source bindings agree with the analytic note. | Step 1 certificate and independent audit | FINITE / INDEPENDENT AUDIT | Finite arithmetic does not prove the platform, bridge, or PDE theorems. |
| Q13 | Defining \(q_\ell=BD_R(h_\ell)-q_*\) removes the frozen algebraic calibration conflict. | Step 1 (Q.62)--(Q.63) | PROVED ALGEBRA / OPEN ANALYSIS | The definition alone supplies no survival, annular inclusion, dominance, or payment estimate. |
| Q14 | Quadratic shell energies and fluxes have exact diagonal and cross-term expansions under common-shear superposition. | Step 1, Section 5 | PROVED | Exact expansion does not imply cancellation or small cross terms. |
| Q15 | Spatial separation does not make the complete nonlinear payment additive, because central-energy and harmonic rows sum masses before an outer \(3/2\) power. | Step 1, Section 6 | PROVED STRUCTURAL OBSTRUCTION | This rules out a naive additivity argument; it is not a universal \(N^{3/2}\) lower bound without additional hypotheses. |
| Q16 | The inherited proof windows for the proposed amplified two-packet scaling are mutually incompatible. | Step 1, Proposition 7.1 | PROVED | This concerns simultaneous reuse of inherited exponent windows, not every amplitude design. |
| Q17 | Under the explicit outer-lobe no-cancellation premise, the outer velocity-cubic row gives the obstruction in Step 1, Proposition 7.2. | Step 1, Proposition 7.2 | CONDITIONAL | Step 1 does not prove the premise; Step 2 proves it only for its canonical equal-target family. |
| Q18 | For \(L=\lambda2^j\), \(R=e^{-\rho L^2}\), and \(N=\lfloor\log_2L\rfloor=j\), one has \(L_N=(16/63)L^2\) and \(L_NR\to0\). | Step 2 (Q.103)--(Q.106); finite certificate | PROVED / FINITE | This is the explicit growing finite family; \(N\to\infty\) only along \(j\to\infty\). |
| Q19 | The relaxed calibration has \(B=(128R^2)^{-1}(1+O(e^{-a_DL^2}))\), \(q_1=0\), and \(\sup_{\ell\le N}|q_\ell|/R\to0\). | Step 2 (Q.108)--(Q.123) | PROVED | No sign or monotonicity of \(q_\ell\) is claimed. |
| Q20 | All packets share one terminal interval and have uniform positive-packet bridge survival. | Step 2 (Q.124)--(Q.130); R0.74F; Step 1 platform lemma | INHERITED / PROVED PARAMETER CLOSURE | The stochastic bridge theorem is inherited from R0.74F; the common-\(R\), growing-\(N\) closure is proved here. |
| Q21 | The \(N\) terminal lobes lie in the distinct shells \(A_{j+\ell-1}(R)\), with margins and constants uniform in \(N\). | Step 2 (Q.131)--(Q.136) | PROVED | Explicit terminal geometry for the relaxed family only. |
| Q22 | With \(\mathfrak a_\ell=A_*(\Gamma_\ell L_\ell)^{-1/2}\), the intended packet dominates the full amplitude-weighted sum on every target lobe. | Step 2, Lemmas 3.1--3.4 and Proposition 3.5, (Q.137)--(Q.160) | PROVED | Restricted to the explicit equal-target amplitudes and geometry. |
| Q23 | The rational cross-packet margins, dyadic sums, periodic remainder, and deterministic source bindings pass finite and independent audits. | Step 2 certificate; relaxed-dominance and relaxed-geometry independent audits | FINITE / INDEPENDENT AUDIT | The certificate does not replace stochastic, annular, clock, or payment proofs. |
| Q24 | At one common terminal time, every target clock satisfies \(K_{k_\ell,R}(\tau)\ge c_KT\), where \(T=A_*^2R^2\). | Step 2 (Q.161)--(Q.163) | PROVED | Terminal lower bound only; it uses the energy part of the nonnegative completed clock. |
| Q25 | The target lower bounds imply \(Y_{2,R}^{\rm sf}\ge c_K\sqrt N\,T\). | Step 2 (Q.164) | PROVED | Lower bound only. Off-target clocks and earlier positive variation are not controlled above. |
| Q26 | The outer lobe lies in \(A_{k_N-1}(2R)\), sees \(\gamma_{k_N-1}=\Gamma_N^{1/4}\), and forces \((P_R^{M,(N)})^{2/3}/(NT)\to\infty\). | Step 2 (Q.165)--(Q.173) | PROVED | Canonical equal-target Version-M family only; this does not exclude every multipacket design. |
| Q27 | The canonical equal-target family satisfies \((P_R^{M,(N)})^{2/3}=o(NT)\). | None; contradicted by Q26 | NOT CLAIMED / FALSE FOR THIS FAMILY | The proved ratio diverges instead. |
| Q28 | The terminal clock lower bounds imply \(\mathfrak C_R^{M,(N)}\asymp NT\). | Step 2 (Q.174)--(Q.178) | OPEN / NOT CLAIMED | Positivity of \(K\) does not imply positive signed flux, and the source ledger can dominate \(NT\). |
| Q29 | The canonical family satisfies \(Y_{2,R}^{\rm sf}\lesssim\sqrt N\,T\). | None | OPEN / NOT CLAIMED | Off-target shells, cross terms, and earlier positive variation remain uncontrolled. |
| Q30 | The signed effective-shell estimate (Q.12) holds uniformly for arbitrary suitable weak solutions. | None | OPEN / NOT CLAIMED | The smooth stress tests do not supply the arbitrary-flow packing mechanism. |
| Q31 | The fixed-scale inequality \(\mathfrak C_R^M\le C[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}]\) holds. | Problem freeze (Q.1) | OPEN | Neither the cubic obstruction nor the terminal lower bounds decide it. |
| Q32 | A contraction, scale smallness, and a prescribed-terminal-centre nested good-scale sequence follow from R0.74Q. | None | OPEN / NOT CLAIMED | These are additional regularity-iteration inputs. |
| Q33 | R0.74Q proves regularity, constructs a singularity, excludes all singularities, or resolves the three-dimensional Navier--Stokes Millennium problem. | None | OPEN / NOT CLAIMED | All discriminating families are smooth. **NOT CLAY.** |

## Route consequence

R0.74Q proves that the frozen terminal-angle multipacket transplant fails,
while a relaxed common-shear geometry can support a growing number of
simultaneous target lobes. The canonical equal-target normalization then
fails for a different quantitative reason: its outer velocity-cubic payment
is much larger than the total terminal target scale after the \(2/3\) power.
This does not establish signed flux, a matching all-shell square-function
upper bound, or the fixed-scale inequality. The remaining mathematical
question is whether convex exterior payment can be linked directly to the
number and strength of effective terminal shells while retaining every
off-target clock and signed source term.
