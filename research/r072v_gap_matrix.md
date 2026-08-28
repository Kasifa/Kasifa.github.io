# R0.72V gap matrix

**Date:** 2026-08-28

The statuses below concern the exact cubic whole-line model

\[
 P_{c,\sigma}=\partial_t-i\sigma\bigl[x^3+6(c+t)x\bigr],
 \qquad I=(-T,T),\quad T>0.
\]

The finite rational ledger in R0.72V can check probe moments, polynomial
translation identities, an escaping-coefficient threshold, and the final
contraction algebra.  It does **not** machine-check compactness, scalar trace
passages, the countable Hilbert-space direct sum, or nonautonomous evolution
existence.

| Item | Exact status | Evidence in R0.72V | Exact boundary / what remains |
|---|---|---|---|
| Two-parameter unit-chart theorem | **CLOSED** | Theorem 2.1 proves, on \(J=(-1/2,1/2)\), graph coercivity for \(Q_{a,b,\sigma}=\partial_t-i\sigma[y^3+ay^2+(b+6t)y]\) with one constant independent of \((a,b,\sigma)\), and with no temporal or spatial trace condition | The constant exists nonconstructively and depends on the fixed \(T>0\); the compactness proof is analytic, not machine checked |
| Scalar gauge | **CLOSED exact identity** | Multiplication by \(e^{-i\sigma a\mu_2t}\) removes the scalar part \(a\mu_2\), preserves all norms used in the theorem, and makes the \(q_0\)-mean of \(y^3+a(y^2-\mu_2)+(b+6t)y\) vanish | This is a time-only unitary gauge; no spatially dependent gauge or change of the differential operator is invoked |
| Bounded coefficient pairs | **CLOSED** | Weighted Poincare makes \(v_n\) asymptotically spatially constant; \(A_n'\to0\), \(B_n\to0\), and \(B_n'=i\sigma_n[\mu_4+(b_n+6t)\mu_2]A_n+o(1)\) force the constant limit to vanish because the affine factor has slope \(6\mu_2\ne0\) | Strong \(L^2_t\) compactness and the distributional limit are functional-analytic proof steps, not finite-certificate outputs |
| Escaping coefficient pairs | **CLOSED** | With \(\lambda=(a^2+b^2)^{1/2}\), \(p_{\alpha,\beta}=\alpha(y^2-\mu_2)+\beta y\), and \(\kappa_{\alpha,\beta}\ge\kappa_0>0\), the adaptive moment satisfies \(B'=i\sigma[\lambda\kappa_{\alpha,\beta}+\ell_{\alpha,\beta}(t)]A+E\); after division by \(\lambda\), all interior and endpoint errors vanish | The rational probe checks \(\kappa_0\) and a sufficient \(T=1\) threshold, but it does not machine-check the contradiction argument for arbitrary escaping sequences |
| Endpoint trace with no \(\lambda\delta\) hypothesis | **CLOSED** | Only scalar moments \(A,B\in H^1(I)\) are traced.  The bounds \(|A(\pm T)|\lesssim1+\sqrt{(1+\lambda)\delta+\varepsilon}\) and \(|B(\pm T)|\lesssim\delta+\sqrt{\lambda\delta}\) give \(|BA|/\lambda\to0\) without assuming \(\lambda\delta\to0\) | No \(L^2(J)\)-valued endpoint trace of the full function is asserted; the scalar trace passage is analytic, not machine checked |
| Spatial translation map | **CLOSED exact identity** | On \(J_k=(k-1/2,k+1/2)\), \(x=k+y\) gives \(a_k=3k\), \(b_{k,c}=3k^2+6c\), plus the removable scalar \(k^3+6(c+t)k\) | The identity handles every large \(|k|\), \(|c|\), and cancellation between \(3k^2\) and \(6c\); it concerns the exact cubic model only |
| \(H^{-1}\) direct sum | **CLOSED** | Zero extension embeds \(\bigoplus_kH_0^1(J_k)\) isometrically into \(H^1(\mathbb R)\), so duality yields \(\sum_k\|g_k\|_{H_D^{-1}(J_k)}^2\le\|g\|_{H^{-1}(\mathbb R)}^2\), followed by integration in time | This requires the standard nonhomogeneous \(H^{-1}(\mathbb R)=(H^1(\mathbb R))^*\); the countable direct-sum passage is a functional-analytic theorem, not a finite numerical check |
| Whole-line graph theorem | **CLOSED** | The coefficient-uniform unit-chart estimate, exact translation/gauge, and the direct-sum lemma give \(\|v\|_{L^2_{t,x}}\le C_T(\|v_x\|_{L^2_{t,x}}+\|P_{c,\sigma}v\|_{L^2_tH^{-1}_x})\), uniformly in \(c\) and \(\sigma\) | \(T>0\) is fixed, \(C_T\) is non-explicit, and the theorem neither uses nor proves a fixed-origin tail-fraction estimate |
| Actual-solution observability | **CLOSED in the declared graph class** | For \(P_{c,\sigma}u=u_{xx}\), duality gives \(\|u_{xx}\|_{H^{-1}}\le\|u_x\|_2\), hence \(\|u\|_{L^2_{t,x}}\le2C_T\|u_x\|_{L^2_{t,x}}\) | This is an a priori estimate for whole-line solutions belonging to the graph class; it is not by itself an existence theorem for arbitrary initial data |
| Energy evolution and block contraction | **CLOSED for all \(L^2\) data in the exact scalar model** | Bounded real-potential truncations, uniform energy bounds, local Aubin--Lions compactness, and a cutoff-energy limit construct the unique \(C_tL_x^2\cap L_t^2H_x^1\) evolution and its exact energy identity.  Monotonicity plus observability then gives \(E(T)\le C_T^2(T+C_T^2)^{-1}E(-T)\), uniformly in \(c,\sigma\) | The construction and cutoff limit are analytic, not machine checked; this remains an exact cubic scalar-model evolution, not a periodic or Navier--Stokes contraction |
| Cutoff commutator absorption | **CLOSED as a corollary** | \(2\eta'u_x+\eta''u=\partial_x(2\eta'u)-\eta''u\) gives an \(H^{-1}\) bound using only \(\eta'u\) and \(\eta''u\); a square partition at scale \(L\) is absorbed once \(4C_TA_1/L+C_TA_2/L^2<1\) | This algebra is not needed for the disjoint-cell proof of the global theorem and does not absorb the unbounded higher heat-polynomial remainders |
| Uniformity as \(T\downarrow0\) | **FALSE** | The exact kernel family with spatial scale \(L=T^{-1/3}\) gives \(\|v_x\|_2/\|v\|_2\lesssim T^{1/3}\), so every graph constant satisfies \(C_T\gtrsim T^{-1/3}\) for small \(T\) | No contraction factor bounded away from one uniformly over arbitrarily short blocks follows from this graph argument |
| Evolution-class boundary | **CLOSED analytically; not finite-certified** | Proposition 9.1 separately constructs the all-data evolution by bounded-potential truncation, passes locally by Aubin--Lions, recovers the global energy identity with spatial cutoffs, and proves uniqueness from the same localized identity | Maximal graph membership alone still does not imply a time trace or energy identity; the separate construction is essential and remains outside the finite algebraic certificate |
| \(H_5,H_7,R_9\) stability | **OPEN** | R0.72V treats only \(H_3=x^3+6tx\); the higher heat polynomials and analytic tail grow at spatial infinity and are not small in the unweighted whole-line graph norm | Prove a weighted, remainder-stable whole-line theorem with quantitative absorption on the collision block before transferring the result |
| Periodic exact-heat-path transfer | **OPEN** | No theorem in R0.72V transports the whole-line cubic contraction through rescaling, localization, higher-order remainders, and the periodic geometry | Requires the remainder-stable theorem, quantitative rescaling, periodic localization, and a verified comparison with the exact heat path |
| Nonlinear Navier--Stokes / Clay | **OPEN** | The completed result is a linear scalar-model graph and contraction theorem | No pressure estimate, vortex-stretching control, nonlinear bootstrap, continuation criterion, or proof of global regularity or blow-up for arbitrary smooth three-dimensional data is supplied |

## Next minimal theorem

The next gate is a weighted whole-line perturbation theorem showing that the
exact \(H_5,H_7,R_9\) correction can be absorbed, with constants compatible
with the collision rescaling.  Only after that gate can the periodic
exact-heat-path transfer be tested.
