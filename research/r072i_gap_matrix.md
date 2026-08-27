# R0.72I gap matrix -- physical absorption and the parity repair

**Date:** 2026-08-27

| ID | Question entering R0.72I | Decision | Evidence | Boundary |
|---|---|---|---|---|
| I1 | What is the physical conversion factor from the abstract root mass in R0.72H? | **proved** | Under the exact amplitude balance and the enstrophy floor, every abstract root atom is multiplied, up to fixed constants, by \(\Theta_M=S_M^2P_M^2/(q^2E_M)=3P_M^2/(4q^2K_{f,M})\). | This comparison uses the declared decoupled background and the two-sided enstrophy estimate; it is not an identity for arbitrary NSE data. |
| I2 | Can all four positive terms in R0.72H (6.5) be absorbed term by term into \(D^{1/3}\Lambda_{1,*}\)? | **rejected** | On the all-odd Rudin--Shapiro family with \(a=q=d=K_z=\nu=1\) and \(\delta=P=M\), the lifted \(B_AQ_*\) term divided by \(D^{1/3}\Lambda_{1,*}\) is \(\asymp M^{1/2}\log M\). | This rejects the direct factorization of the existing upper bound. A large positive upper-bound term is not a lower bound for the true ledger. |
| I3 | Are the other three terms responsible for that loss? | **no** | Their lifted scales are \(M\), \(M^{-1/3}\log M\), and \(M\), while \(D^{1/3}\Lambda_{1,*}\asymp M^{5/3}\). Their normalized ratios tend to zero. | The statement is for the declared family and physical balance, not an arbitrary carrier geometry. |
| I4 | Does the choice \(\delta=M\) remain inside the uniform perturbative window used in R0.72H? | **proved** | The actual Duhamel parameter is \(|\delta|aM^{-3/2}=M^{-1/2}\to0\); the exact root correction is \(O(|\delta|aM^{-2})=O(M^{-1})\). | The window still requires a fixed sufficiently small upper bound on \(|\delta|aM^{-3/2}\). |
| I5 | Why is the \(B_A\)-Cauchy estimate coarse on this family? | **identified exactly** | Every carrier is odd. Hence \(V\) swaps lattice parity and \(V^2\) preserves it. The target row \(h=P_0VF\) sees only the odd component, whereas \(b=P_0V^2F\) sees only the even component. | Mixed-parity carrier sets do not have this invariant two-colour decomposition. |
| I6 | How large can the dynamically generated even component become? | **proved** | Contractivity, the heat-stable Rudin--Shapiro operator bound, and Duhamel give \(\|F_{\rm even}(x)\|_2\le C\min(\sqrt M,g/M)\), where \(g=|\delta|a\). | The launch has only the controlled \(O(gM^{-2})e_0\) even correction. |
| I7 | Can the actual cubic row replace the coarse \(B_AQ_*\) payment? | **proved for the all-odd family** | The parity split yields \(|\delta|\int|hP_0V^2F|\,dx\le Ca^2g\min(\sqrt M,g/M)\). For \(g\le\gamma_0M^{3/2}\), this is at most \(Ca^2g^2/M\le Ca^2M^2\). | This is a structure-sensitive estimate, not a generic finite-carrier theorem. |
| I8 | What is the true complete raw root mass on the perturbative all-odd family? | **proved sharp** | The parity-refined Rolle upper bound gives \(G_{\rm all}^{\rm ex}\le Ca^2M^2\), and the exact interior root from R0.72H gives the matching lower bound \(G_{\rm all}^{\rm ex}\ge ca^2M^2\). | Requires a compatible real gauge and \(\delta\ne0\). |
| I9 | Does this family violate the physical critical-log candidate? | **no** | With \(a=1\), \(D_M\asymp g^2M^3\), \(\mathscr A_*\asymp g^2M^{-7/3}\log M\), and \(\mathcal J_{\rm all}\asymp g^2/M\). Thus the normalized ratio is \(\asymp g^{4/3}M^{-2}/(1+g^2M^{-7/3}\log M)\). | This settles only this exact triangular family. It neither proves the candidate generally nor rules out a different counterfamily. |
| I10 | Is the last normalized ratio uniformly small over the whole perturbative coupling window? | **proved** | Writing \(z=g^2M^{-7/3}\log M\) gives a uniform bound \(CM^{-4/9}(\log M)^{-2/3}z^{2/3}/(1+z)\), hence convergence to zero. | The constant may depend on fixed geometry, interval, viscosity, and the chosen perturbative ceiling \(\gamma_0\), but not on \(M\) or \(g\). |
| I11 | Do the finite computations prove the theorem? | **no** | Producer and independent implementations test the scaling, parity exposure, exact root, and physical-lift ratios on finite lattices. | The analytic parity argument and asymptotic estimates are the result; numerics are corroboration only. |
| I12 | Does R0.72I imply a general three-dimensional continuation theorem? | **no** | It diagnoses one failed factorization and closes one special all-odd branch inside an exact globally smooth triangular 2.5D class. | No general NSE singularity is excluded or constructed, and the Millennium problem remains open. |

## Gate decision

R0.72I gives a two-part decision. The positive \(B_AQ_*\) term in the fixed
R0.72H estimate cannot be absorbed term by term into the intended physical
normalization. On the same family, however, odd-carrier parity replaces that
coarse term by the true interaction exposure and proves that the complete
normalized ledger tends to zero. The next finite gate is therefore generic:
either find a carrier decomposition or interaction estimate that controls
\(P_0V^2F\) without the \(B_A\)-Cauchy loss, or construct a mixed-parity family
for which the true cubic row, not merely its positive upper bound, survives the
physical normalization.
