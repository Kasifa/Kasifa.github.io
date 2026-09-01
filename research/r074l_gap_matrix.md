# R0.74L gap matrix — normalized-bridge main collar

## Scope

This matrix tracks only the main target-shell Jensen majorant frozen in
R0.74L.  It does not promote the nearest inward shell, the full signed
packet condition, a matching \(\mathfrak C_j\) upper bound, an \(X_j\)
upper bound, or any universal regularity claim.  **NOT CLAY.**

| ID | Statement | Evidence | Current status | Exact boundary |
|---|---|---|---|---|
| L1 | The lifted real expression (F.5) folds exactly to the two-variable periodization \(\overline M\) with every heat-kernel and bridge winding retained. | r074l_forward_bridge_bv_reduction.md, Section 1; independent audit A1--A2 | PROVED / AUDITED | No central-copy truncation is used. |
| L2 | A fixed backward history cannot be differentiated in terminal time to obtain \(dq=B\theta\,dt\). | Exact heat solution \(\theta=e^{-t}\sin x\), equation (2.1) | PROVED NEGATIVE MECHANISM | This does not refute the frozen family or (F.6). |
| L3 | After integration in the endpoint variable, normalized bridges admit the exact common-forward-law identity (3.3). | Heat-kernel symmetry, cylinder reversal, monotone class; independent audit A5--A6 | PROVED / AUDITED | The reversed shear functional must be written as \(\mathfrak S_t^{\leftarrow}[X]\), not \(\mathfrak S_t^{X_t}\). |
| L4 | Transition-approach paths have probability at most \(4e^{-AL^2}\), with \(A-\rho=1315703/7381975040>0\). | Lemma 4.1; exact certificate; independent audit A7--A8 | PROVED / AUDITED / FINITE ARITHMETIC PASS | This event is used only for the main target shell. |
| L5 | The \(R/16\)-thickened fixed transverse slice satisfies \(\sup_{x_3}\int M^\sharp\,dx_2\le CLR\), including spherical tangencies. | Planar projection of two \(O(R)\)-thick radial collars; independent audit A3 | PROVED / AUDITED | Pointwise chord bounds are intentionally avoided. |
| L6 | For fixed \(u\), the periodized clock support has at most two components and total length \(O(LR)\). | \(C_{\rm pr}=65/63\), \(|J|\le65/64<2\); independent audit A4 | PROVED / AUDITED / FINITE ARITHMETIC PASS | Uses the deterministic positive clipped clock. |
| L7 | Each clock-support component lasts \(O(LR^3)\) in physical time, and an \(R/16\) transverse oscillation costs \(e^{-c/(LR)}\). | Inverse-clock stopping time, strong Markov property, reflection principle; independent audit A9--A11 | PROVED / AUDITED | The clock is extended positively before inversion; no future event defines the inverse. |
| L8 | The good-path clock occupation is \(O(LR)\), hence \(\mathscr B_j^{\rm good}\le CLR^5\). | Thickened slice on the small-modulus event; \(CL^2R\) times \(e^{-c/(LR)}\) otherwise; independent audit A12--A13 | PROVED / AUDITED | No Markovian projection or density theorem is used. |
| L9 | The full R0.74L main-collar majorant satisfies \(\sup_{\tau\in I_R}\mathscr B_j(\tau)\le CLR^5\). | L4 plus L8; exact power ledger; independent audit | PROVED / AUDITED | This is the completed R0.74L theorem. |
| L10 | (F.6) implies the absolute two-packet main-collar row \(C\Gamma_jLR^5\). | R0.74L problem freeze, (F.7)--(F.8) | INHERITED IMPLICATION | This alone does not prove R0.74K (4.3). |
| L11 | Markovian projection plus classical Aronson closes the good paths. | Targeted primary-source audit | REJECTED AS WRITTEN | The projected forward equation is \(\partial_s p=\partial_{xx}(ap)\); the checked measurable-coefficient Aronson theorem is for a different divergence-form operator. |
| L12 | Existing literature contains the exact normalized periodic bridge--clock BV theorem used here. | Bounded three-wave collision audit | NO DIRECT HIT FOUND | A finite non-hit is not a novelty or priority claim. |
| L13 | Nearest inward positive shear expulsion. | R0.74K adverse exponent and adversarial audit | OPEN / OUTSIDE R0.74L | The relevant next condition is quantitative anti-concentration, not merely \(\mathfrak S\ge0\). |
| L14 | Matching \(\mathfrak C_j\), \(X_j\), universal endpoint, regularity, or singularity. | None | OPEN / NOT CLAIMED | **NOT CLAY.** |

## Finite certificate

The exact-arithmetic file r074l_main_collar_certificate.json is generated
by scripts/r074l_main_collar_certificate.py and currently reports
24/24 checks passing.  Its scope is only finite rational constants,
thresholds, and the \(L,R,B\) power ledger.  It is not a substitute for
the analytic audit rows L1--L9.
