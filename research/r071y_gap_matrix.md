# R0.71Y gap matrix -- growing-root operator sampling

**Date:** 2026-08-26  
**Status:** theorem/gap ledger for the R0.71W fixed-target triangular class.

| ID | claim or route | exact payment in R0.71Y | decision | remaining boundary |
|---|---|---|---|---|
| Y1 | Full active Fourier evolution is \(\ell^2\)-contractive. | \(D_q\le0\) is self-adjoint and \(V_z\) is skew-adjoint, so \(\|F(x)\|_2\le\|F(0)\|_2\). | proved | This is scalar \(L^2\), not enstrophy contraction. |
| Y2 | At an exact target root the heat term can enlarge the target slope. | The target coordinate is zero and \(D_q\) is diagonal, so \(\partial_xF_0=\delta(V_zF)_0\) exactly. | rejected | A non-diagonal linear generator would require a new argument. |
| Y3 | \(N\) roots contribute \(N\) uncontrolled copies of a pointwise bound. | Summed squared slopes are at most \(NM S^2P^2\Omega_N^2\), \(M=2N+1\). | paid | The estimate is worst-case and does not use root separation. |
| Y4 | The endpoint ratio is governed by \(\varepsilon_N=P\sqrt{K_v}/q^2\). | Exact algebra retains \(\delta_{\rm obs}=(P/q^2)\Omega_N\) and \((\Omega_N^2/K_v)^{1/3}\) separately. | corrected | No lower equivalence between operator norm and \(K_v^{1/2}\) is asserted. |
| Y5 | Fourier cancellation prevents comparison with weighted shear energy. | \(\Omega_N\le2|K_z|\|z\|_1\le(2\pi|K_z|/\sqrt6)K_v^{1/2}\). | proved upper comparison | Cancellation can make \(\Omega_N\) smaller, which helps. |
| Y6 | Distinct growing carrier phases are cheap. | For \(M\) unit phases, \(K_s\ge\sum_{j=1}^Mj^2\), so \(NM/K_s\le3/(4N)\). | rejected | Weighted or sparse phase families are not covered by this corollary. |
| Y7 | A quantitative ECT inverse is required before judging the route. | The upper bound assumes only the existence of exact roots and bypasses the interpolation inverse. | rejected for this branch | ECT conditioning remains relevant to constructing roots. |
| Y8 | Observation-layer coupling is the complete IFT parameter. | A launch-to-root certificate also pays \(\eta_{\rm Dyson}=(P/q^2)\int_0^{\tau_N}\|V_z\|\,dx\), inverse Jacobian, and derivative-Lipschitz constants. For fixed \(A_0>0\), \(\delta_{\rm obs}\le C\eta_{\rm Dyson}\). | rejected and corrected | The theorem needs no IFT; the one-way bound puts the existing small-Dyson corridor inside it. |
| Y9 | Bounded operator coupling and growing root count can defeat \(D^{1/3}\). | \(\mathcal J_N^{\rm sel}/(D^{1/3}\Lambda_1)\le C\nu^{-2}\delta_{\rm obs,N}^{4/3}/N\to0\). | rejected under the floors | Floor-free and non-unit-phase geometries remain separate. |
| Y10 | Full-frequency rotational-charge growth must be estimated first. | \(\Lambda_1\ge\nu^2\), so the raw \(D^{1/3}\) upper bound controls the complete ratio. | not required here | A strong-coupling construction still needs the complete charge. |
| Y11 | The old fixed-\(N\) background may be reused as \(N\to\infty\). | The floor must match \(q^2(S^2K_s+P^2K_v)\), and its launch cost belongs in \(D\). | rejected | The floor-free complete-ledger case is open. |
| Y12 | Strong observation coupling is also closed. | Nonvanishing requires \(\delta_{\rm obs,N}\gtrsim N^{3/4}\); divergence requires faster growth. | not closed | Exact roots, enstrophy variation, and nonlinear charge remain unproved in that regime. |
| Y13 | The result proves the universal NSE endpoint. | The theorem is restricted to the declared triangular fixed-target one-dimensional shear lattice and explicit floors. | rejected | The Millennium regularity problem remains open. |
| Y14 | Root separation gives no extra payment. | Exactly at finite \(q\), \(G_N^{\rm ex}\le CMW_N^2/h_N\), hence the selected complete-ledger ratio is \(O(\delta_{\rm obs}^{4/3}/(h_NN^2))\). | rejected | The \(h_N^{-1}\) corollary degenerates at \(\tau_1=A_0\); the weighted kernel form remains valid. |
| Y15 | The result is uniform as \(A_0\to0\). | The Dyson-to-observation constant degenerates when \(A_0\downarrow0\). | rejected | An \(A_{0,N}\to0\) short-pulse/root-layer route remains open. |
| Y16 | Uncontrolled additional nonlinear roots are harmless. | For \(M\) carriers and any \(R\) exact sampled roots, the ratio is \(O(R\delta_{\rm obs}^{4/3}/M^2)\). | conditional payment | No all-root count is proved; bounded-coupling escape needs at least \(R\gtrsim M^2\). |
| Y17 | Ultra-clustering can remain well conditioned. | For equal nodes, \(\|\mathsf M^{-1}\|_2\ge h^{-1}(bh r_{\max}^2)^{-(N-1)/2}\). | rejected for the canonical lattice when \(bhN^2\to0\) | Inverse growth alone is not an upper bound on the true nonlinear IFT radius. |

## Release statement

The publishable R0.71Y statement is Y9 together with the exact analytic chain
Y1--Y6 and the scope controls Y10--Y13. No finite interpolation condition
number, numerical root scan, or fixed-\(N\) IFT radius is promoted to a
growing-dimensional theorem.
