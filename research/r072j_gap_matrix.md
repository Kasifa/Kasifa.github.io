# R0.72J gap matrix -- mixed parity and the true cubic row

**Date:** 2026-08-27

| ID | Question entering R0.72J | Decision | Evidence | Boundary |
|---|---|---|---|---|
| J1 | What is the invariant version of the all-odd carrier condition? | **proved** | With \(g_0=\gcd(r_l)\), the Cayley graph on \(g_0\mathbb Z\) is bipartite iff every \(r_l/g_0\) is odd. | Raw integer parity is not invariant under common dilation. |
| J2 | Does non-bipartite imply that the one-step and two-step target rows overlap? | **no** | \(h\) reads \(-\Sigma\), while \(P_0V^2F\) reads \(-(\Sigma+\Sigma)\). They overlap iff \(s+t=u\) for signed carriers. The non-bipartite set \(\{1,4\}\) has no such triple. | A longer odd cycle can break bipartiteness without producing an initial cubic overlap. |
| J3 | What exactly replaces the all-odd parity block in mixed parity? | **proved** | \(V=V_{\rm o}+V_{\rm e}\), where \(V_{\rm o}\) swaps reduced parity and \(V_{\rm e}\) preserves it. Expanding \(V^2\) gives the four terms in R0.72J (0.6). | When both pieces are present, parity alone does not force the cubic row to read a dynamically small sector. |
| J4 | Can the cubic row be bounded without forming the positive product \(B_AQ_*\)? | **proved** | The exact minimum (4.5) combines the critical-action branch with \(|\delta|E(0)\int\rho^2\|V\|\). | The second branch depends on joint heat exposure; it is not a generic scale-free bound for arbitrary multiscale carriers. |
| J5 | Is there a carrier-count-free negative-norm product estimate in one lattice dimension? | **proved** | Duality, \(H^1(\mathbb T)\hookrightarrow L^\infty\), and Parseval give \(\mathfrak q\le C\rho^2E\). | This uses the one-dimensional carrier lattice of the exact triangular class. |
| J6 | What are the critical-log scales in one common band? | **proved** | For \(N\) carriers in \([R,C_0R]\), an aligned launch gives \(Q_*\asymp a^2N^2R^{-4/3}(1+\log R)\) and \(m_*\le Ca^2NR^{4/3}(1+\log R)^{-1}\). | The lower bound uses explicit row alignment and the perturbative exposure window. |
| J7 | Does the common-band branch retain an exact non-collapsing target root? | **proved for one root** | At \(\tau=R^{-3}\), a complex \(e_0\) correction of size \(O(gNR^{-3})\) zeros the target coordinate exactly and leaves \(|h(\tau)|\gtrsim aN\). | The correction may be complex. One root does not give a complete-root upper theorem. |
| J8 | How large can the true cubic contribution be in a heat-stable common band? | **proved** | If \(\|V(x)\|\le CaB e^{-cR^2x}\) and \(gB/R^2\le\gamma_0\), then \(\mathcal C_\times\le C(gB/R^2)a^2N^2\). | Strong coupling and multiscale profiles are not covered. |
| J9 | Can that common-band cubic contribution violate the physical critical-log payment? | **no** | With \(\Theta\asymp g^2/(a^2NR^2)\), \(D\asymp g^2NR^2\), and \(\mathscr A_*\asymp g^2NR^{-10/3}(1+\log R)\), its normalized ratio is at most \(CR^{-4/9}(1+\log R)^{-2/3}\). | This decision concerns the true cubic row, not every term in a complete root ledger. |
| J10 | Is there an explicit genuinely non-bipartite block with coherent true cubic mass? | **proved** | \(S_R=\{R,\ldots,3R-1\}\) has \(R(R+1)/2\) ordered positive triples, \(T_R=3R(R+1)\) ordered signed triples, and \(|P_0V^2G|=T_R/\sqrt2\). | The coherent launch is not in the fixed real target gauge required by the old Rolle corollary. |
| J11 | Does the coherent block saturate the raw common-band estimate? | **proved** | For \(w=1\), \(|\delta|\int\|V\|=2|\delta|\sum r^{-2}\) exactly. Taking \(\delta=\gamma R\) gives \(\mathcal C_{\times,R}\asymp_\gamma R^2\). | The lower bound requires fixed sufficiently small \(\gamma\). |
| J12 | Does this sharper coherent block survive physical normalization? | **no** | \(\Theta\asymp R^{-1}\), \(D\asymp R^5\), and \(\mathscr A_*=o(1)\), so its normalized cubic ratio is \(\asymp R^{-2/3}\). | A vanishing cubic ratio does not prove the full physical inequality. |
| J13 | Can real-gauge Rolle sampling and direct triangle coherence be assumed together? | **no** | In a real skew gauge, the strictly row-aligned launch has \(P_0V^2G\propto\langle e_0,V^3e_0\rangle=0\). | A different complex-root sampling theorem would be needed to retain the coherent launch. |
| J14 | Is the complete mixed-parity root ledger now closed? | **open** | The current proof constructs one exact root and bounds the true cubic integral, but does not pack all zeros of a complex target coordinate. | No claim of \(G_{\rm all}\asymp a^2N^2\) is made. |
| J15 | Do the finite computations prove the result? | **no; finite audit passed** | Independent finite routes corroborate the exact counts, root residual, critical action, true cubic integral, and normalized decay for \(R=4,8,16,32,64\). | The computations do not prove the asymptotic estimates or enumerate the complete complex root set. |
| J16 | Does R0.72J settle general three-dimensional Navier--Stokes regularity? | **no** | The result is confined to an exact globally smooth triangular 2.5D class and one perturbative common-band regime. | The Millennium problem remains open. |

## Gate decision

R0.72J closes the true cubic row in a perturbative common frequency band and
shows that a triangle-rich non-bipartite block can saturate the raw cubic
scale without surviving physical normalization. It does not close the
complete root set in a complex gauge. The next gate is either a valid
complex-target root-sampling theorem or a multiscale construction that
escapes the single heat window used here.
