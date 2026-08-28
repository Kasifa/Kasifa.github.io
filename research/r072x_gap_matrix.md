# R0.72X gap matrix

**Date:** 2026-08-28

The statuses below concern the exact two-harmonic heat path and the scalar
Fourier rows obtained after the carrier-cell reduction.  A finite certificate
checks the shifted-center common-zero algebra, local jet, interface powers,
block-count arithmetic, Bloch phase, scalar damping factors, and geometric
series.  It does not machine-check compactness, endpoint traces, twisted
negative-Sobolev direct sums, parabolic evolution, or the Coble--He theorem.

| Item | Exact status | Evidence in R0.72X | Boundary / what remains |
|---|---|---|---|
| Shifted exact potential and heat identity | **CLOSED identity** | \(V_{\alpha,S_0}(\tau,X)\) is obtained by replacing \(S\) by \(S_0+\tau\); \(V_S=V_{XX}\) remains exact | Physical center must remain in a fixed compact interval |
| Global common degeneracy | **CLOSED exact algebra** | The center slope/curvature brackets have the unique common zero \((D,\theta)=(0,0)\pmod{2\pi}\) for every real \(D\) | This locates bounded-coefficient charts; it does not prove graph coercivity alone |
| Bounded-center rate | **CLOSED analytic** | Bounded \((a,b)\) imply \(\theta=O(\alpha)\), \(D=O(\alpha^2)\), so the limit is a translated \(H_3\) chart | Compactness and the limiting graph passage are not finite-certified |
| Escaping-center stability | **CLOSED analytic** | On compact physical-time sets, \(V_{XXX}=O(1)\), \(V_{XXXX}=O(\alpha)\), so the R0.72W endpoint ledger remains uniform | Retains the nonconstructive constant |
| All-center unit-cell theorem | **CLOSED** | Compact--escaping contradiction gives one \(C_{K,T}^{\rm cell}\) for every scaled center with \(\alpha^2S_0\in K\) | \(C_{K,T}\) is not explicit and is not uniform as \(K\) escapes to \(+\infty\) |
| Twisted periodic graph theorem | **CLOSED** | Zero-extended cell tests belong to every Bloch test space; twisted integration-by-parts endpoints cancel | Analytic Hilbert-space step, not finite-certified |
| Shifted exact block contraction | **CLOSED** | Energy evolution plus graph coercivity gives \(q_{K,T}<1\) for every center, twist, sign, and \(0<\alpha\le1\) | Fixed positive \(T\) is essential |
| Arbitrary short-time strict factor | **FALSE** | Strong continuity prevents a prefactor-one \(e^{-cL/\alpha^2}\) bound for every \(L>0\) | Safe statement retains \(q^{\lfloor L/(2T\alpha^2)\rfloor}\), or the prefactor \(q^{-1}\) |
| All-start exact-path semigroup | **CLOSED** | Exact cocycle tiling gives \(q^{\lfloor(d_2-d_1)/(2T\alpha^2)\rfloor}\) | Uniform collision rate is \(\alpha^{-2}=\kappa^{2/5}\), not the faster fixed-margin \(A_1\) rate |
| Homogeneous integrated energy | **CLOSED** | Geometric block sum gives \(2T\alpha^2(1-q^2)^{-1}E(d_1)\) | Applies to homogeneous evolution |
| \(L_x^2\)-forcing Duhamel kernel | **CLOSED** | The exponential semigroup envelope and Young's inequality give an \(O(\alpha^2)\) \(L_d^2L_x^2\) operator norm | Endpoint-concentrated \(L_t^1\) forcing does not gain \(\alpha^2\) in \(L_t^\infty\) |
| \(L_t^2H_x^{-1}\)-forcing transfer | **OPEN** | The graph theorem controls a block graph norm, but no scale-sharp global forced evolution estimate is proved | Required for the complete linearized subsystem |
| Fixed-margin outer \(A_1\) geometry | **CLOSED** | On \(d\in[-\log2,-1/8]\) and \(d\in[1/8,1-\log2]\), critical count, separation, Hessian floor, away-gradient floor, and derivatives are uniform | Constants depend on the margin \(1/8\) |
| Fixed-margin outer \(A_1\) propagation | **CLOSED via primary theorem for \(\beta=0\)** | Slow-time rescaling and Coble--He give \(e^{-c\sqrt{\varepsilon_c}L}\) and \(O(\varepsilon_c^{-1/2})\) integrated energy for the periodic representative | Does not extend with fixed constants to a shrinking margin, and no Bloch-uniform fast-\(A_1\) extension is claimed |
| Shrinking-interface fixed-shape \(A_1\) hypotheses | **FALSE** | Pre-collision separation/Hessian are \(O(\alpha)\); post-collision away-gradient is \(O(\alpha^2)\) | This is failure of the black-box hypotheses, not failure of ED |
| Exact \(A_1\)--\(A_2\)--\(A_1\) cocycle | **CLOSED for \(\beta=0\)** | The periodic representative's ungauged physical propagator factors exactly; outer factors, shoulders, collision factor, scalar damping, and endpoint norms are retained | Cell gauges are proof devices and are not interface states; no Bloch-uniform extension of the fixed-margin \(A_1\) black box is claimed |
| Full fixed-history integrated/terminal ED | **CLOSED for the declared launch** | A positive-length pre-collision \(A_1\) segment gives \(O(\varepsilon_c^{-1/2})\) integrated energy and \(e^{-c\sqrt{\varepsilon_c}}\) terminal decay; later energy is monotone | Relies on launching at the left endpoint of the complete heat cell |
| Bloch residue extension at the exact \(A_2\) rate | **CLOSED** | \(e^{i\alpha\beta X}\) changes the covariant derivative into an ordinary derivative and the boundary into the twist \(e^{2\pi i\beta}\) | This does not make the faster fixed-margin \(A_1\) concatenation Bloch-uniform; no nonlinear coupling between residues is included |
| Strong-row direct sum | **CLOSED** | Parseval sums orthogonal invariant rows with a common coupling floor without a row-count factor | Effective couplings may vary or vanish in the physical system |
| All physical rows uniform strict contraction | **FALSE** | A \(K_z=0,\beta=0,\mu=0\) spatial constant is an exact nondecaying mode | Requires projection, damping, or a coupling lower bound |
| Complete linearized shear subsystem | **OPEN** | One homogeneous scalar block and a strong-row direct sum are controlled | Restore every row weight, weak rows, pressure coupling, and scale-sharp \(H^{-1}\) forcing |
| Nonlinear Navier--Stokes / Clay | **OPEN** | No nonlinear pressure or vortex-stretching bootstrap is present | No continuation criterion, global regularity proof, or blow-up construction follows |

## Next minimal theorem

Restore the exact row-dependent coupling

\[
 \varepsilon_j=\frac{2|\delta K_{z,j}|a}{R^2},
\]

separate strong, weak, damped, and zero-coupling rows, and test whether the
complete linearized triangular subsystem admits an \(\ell^2\) direct-sum
estimate with scale-sharp forced terms.  Do not insert nonlinear convolution
until that linear row ledger is complete.
