# R0.72H gap matrix -- critical-log payment of the mixed target row

**Date:** 2026-08-27

| ID | Question entering R0.72H | Decision | Evidence | Boundary |
|---|---|---|---|---|
| H1 | Does the physical multi-carrier operator remain dissipative for arbitrary shear phases? | **proved** | The two shifts must be conjugate-paired. The Fourier multiplier is then purely imaginary, so the coupling is skew-adjoint and the exact energy identity survives. | Naively inserting complex coefficients into the real-shear formula is invalid. |
| H2 | Can the target row be read from the negative-Sobolev action without a carrier loss? | **proved** | For \(z=V_wF\), the target coordinate gives \(\lvert P_0z\rvert^2\le\lambda_0\lVert z\rVert_{A_q^{-1}}^2\). | The nontrivial model has \(K_z\ne0\), hence \(\lambda_0>0\). The zero-frequency degenerate branch is separated before division. |
| H3 | Can the differentiated row \(QF\) be paired with dissipation uniformly in the number of carriers? | **proved** | The R0.72B--C row calculation gives \(\lvert QF\rvert\le6\sqrt{2\nu}\,d\lvert K_z\rvert A_1\mathcal D^{1/2}\), with \(A_1^2=\sum r_l^2\lvert w_l\rvert^2e^{-2\kappa r_l^2x}\). | Requires \(q\ge\max(1,2\lvert K_y\rvert/d)\) and the diagonal triangular lattice. |
| H4 | Does the R0.72F critical-log action pay the new mixed term \(\mathcal E_Q=\int\lvert hQF\rvert\)? | **proved** | Weighted Cauchy--Schwarz, H2--H3, and the energy budget give \(\mathcal E_Q\le6\sqrt\nu d\lvert K_z\rvert[\lambda_0E_A m_*(A,X)Q_*^I]^{1/2}\). | The constant is independent of carrier count, carrier locations, and physical phases; the profile moment \(m_*\) is retained. |
| H5 | Is the new profile moment already present in the physical data? | **proved** | Since \(w_*(s)\ge1\), \(m_*(A,X)\le K_{v,A}=\sum r_l^2\lvert w_l\rvert^2e^{-2\kappa r_l^2A}\). | This is a sufficient coarse payment; it can lose the thermal \(r^{-2/3}/\log r\) gain. |
| H6 | What is the sharp thermal size of the profile moment? | **proved** | The scalar envelope \(\Phi(a)=\sup_{0<s\le1}s^{1/3}e^{-as}/[1+\log(1/s)]\) satisfies \(\Phi(a)\asymp(1+a)^{-1/3}/[1+\log(2+a)]\). | The low-frequency crossover and the factor \((\kappa X)^{-1/3}\) cannot be omitted in an \(X\)-uniform statement. |
| H7 | Can \(m_*\) be deleted and \(\mathcal E_Q\) be paid by \(Q_*^I\) alone? | **rejected** | An all-odd shifted Rudin--Shapiro block gives \(\mathcal E_Q\asymp a^2M^2\) and \(Q_*^I\asymp a^2M^{2/3}\log M\). Thus \(\mathcal E_Q/Q_*^I\asymp M^{4/3}/\log M\). | This excludes the displayed action-only estimate, not every possible inequality using additional data. |
| H8 | Is the moment-resolved upper bound order-sharp? | **proved** | The same family has \(E_A\asymp M\) and \(m_*\asymp a^2M^{7/3}/\log M\), so \([E_Am_*Q_*^I]^{1/2}\asymp a^2M^2\asymp\mathcal E_Q\). | Sharpness is in powers of \(M\), up to constants depending on fixed physical parameters and \(X\). |
| H9 | Can the sharpness family contain an exact simple positive-time target root? | **proved** | With \(\tau_M=M^{-3}\), the scalar evolution-operator correction \(\zeta_M=-P_0U(\tau_M,0)G_M/P_0U(\tau_M,0)e_0=O(\lvert\delta\rvert aM^{-2})\) produces \(F_0(\tau_M)=0\), while \(\lvert h(\tau_M)\rvert\gtrsim aM\) for fixed nonzero \(\delta\). | All carriers are odd so a real target gauge exists; mixed even/odd blocks do not preserve it exactly. |
| H10 | Does the mixed-row theorem automatically prove the complete-root statement for arbitrary physical phases and every coupling? | **rejected as stated** | The mixed-row proof takes absolute values and is phase-stable, but the Rolle refinement needs a real target gauge and \(\delta\ne0\), because \((e^{\lambda_0x}F_0)'=\delta e^{\lambda_0x}h\). | The older complex BV lemma remains available. At \(\delta=0\), the physical slope ledger is zero, while the raw \(h\)-ledger after division by \(\delta^2\) is not covered. |
| H11 | Is the remaining \(P_0V_w^2F\) row controllable at the same action level? | **proved at the abstract row level** | With \(B_A^2=K_z^2\sum\lvert w_l\rvert^2e^{-2\kappa r_l^2A}(\lambda_{q,r_l}+\lambda_{q,-r_l})\), Cauchy--Schwarz gives \(\lvert P_0V_w^2F\rvert\le B_A\mathfrak q^{1/2}\), hence \(\int\lvert hP_0V_w^2F\rvert\le\sqrt{\lambda_0}B_AQ_*^I\). | Absorbing the resulting data factors into the final physical \(D^{1/3}\Lambda_{1,*}\) normalization is not claimed here. |
| H12 | Does R0.72H solve or narrow the full three-dimensional regularity problem? | **no** | The result closes one row estimate in a globally smooth triangular 2.5D test class. | No new unconditional continuation criterion, no exclusion of all possible singularities, and no finite-time blow-up construction. |

## Gate decision

R0.72H closes the finite-carrier mixed-row interface in the precise sense set
by R0.72G: the critical-log action pays \(\mathcal E_Q\) with a constant that
does not grow with the number of carriers, once the already available shear
frequency moment is retained. The shifted all-odd Rudin--Shapiro family shows
that the moment-resolved scale is sharp and that action-only payment is false.

The next finite gate is not another carrier-count estimate. It is the
physical absorption problem: determine whether the factors
\(E_A,m_*,B_A,\rho_A\) produced by the abstract row theorem are all paid by the
declared \(D^{1/3}\Lambda_{1,*}\) normalization on the intended amplitude
class, or whether a normalized counterfamily survives.
