# R0.72W gap matrix

**Date:** 2026-08-28

The statuses below concern the exact rescaled collision family

\[
 V_\alpha(S,X)=\alpha^{-3}\left[
 2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)
 \right],
 \qquad 0<\alpha\le1,
\]

on a fixed block $I=(-T,T)$.  The finite certificate checks the exact
Taylor coefficients, derivative identities, probe moments, collision-only
bounded-cell alternative, no-go scale ratios, torus partition, and energy
algebra.  It does **not** machine-check compactness, scalar trace passages,
negative-Sobolev direct sums, parabolic evolution existence, or the infinite
dimensional operator norm.

| Item | Exact status | Evidence in R0.72W | Boundary / what remains |
|---|---|---|---|
| Exact rescaled potential | **CLOSED identity** | Direct substitution from the physical heat path gives $V_\alpha=-4\alpha^{-3}W(\alpha^2S,\alpha X)$ on the torus of length $2\pi/\alpha$ | Applies to the declared scalar Fourier row after the scalar damping already separated in R0.72T |
| Heat identity | **CLOSED identity** | $\partial_SV_\alpha=\partial_X^2V_\alpha$ follows termwise from the two exact Fourier modes | Does not itself imply coercivity |
| Heat-polynomial coefficients | **CLOSED exact algebra** | The expansion is $H_3-\alpha^2H_5/4+\alpha^4H_7/40-17\alpha^6H_9/12096+\cdots$ | A finite truncation is not global on one growing period |
| Global analytic-tail envelope | **CLOSED** | Lemma 1.1 gives $|\mathcal R_\alpha|\le2(e^T+256e^{4T})\alpha^6\Omega_{9,T}$ for every $X\in\mathbb R$ | This is a polynomially weighted bound, not an unweighted smallness statement |
| Weighted nonabsorbed graph estimate | **CLOSED** | R0.72V plus the exact-tail envelope gives Theorem 2.1 with explicit $W_{5,T},W_{7,T},\Omega_{9,T}$ costs | The extra weighted norms remain on the right-hand side |
| Growing collision-core absorption | **CLOSED** | If $C_TD_{\alpha,T}(R)<1$, all displayed corrections are absorbed on $|X|\le R$ | Crude bounded-multiplier absorption reaches $R=o(\kappa^{2/25})$, far below the period scale $\kappa^{1/5}$ |
| Critical core radius | **CLOSED exact scaling** | For $R=r\kappa^{2/25}$, $D_{\alpha,T}(R)=r^5/4+o(1)$ | Requires fixed small $r$; physical width shrinks like $\kappa^{-3/25}$ |
| Whole-line termwise absorption | **FALSE** | Centered translated bumps give relative $H_5$ cost $\sim(5/12)\alpha^2R^2$ and the $H_7$-corrected cost grows like $\alpha^4R^4$ | Failure survives every time-only scalar gauge |
| One-period vanishing absorption | **FALSE** | At $R_\alpha=\pi/\alpha-c$, the centered $\alpha^2H_5/4$ relative slope tends to $5\pi^2/12>4$; the combined $H_5,H_7$ ratio tends to about $1.570$ | Exact infinite cancellations, rather than a finite Neumann series, are necessary |
| Exact-tail relative smallness | **FALSE** | At the antipodal chart, $(V_{\alpha,X}-H_{3,X})/H_{3,X}\to-1-4/(3\pi^2)$ | This is a gauge-invariant spatial-variation obstruction, not a large scalar potential value |
| Third/fourth derivative ledger | **CLOSED identity** | $|V_{XXX}|\le2e^T+8e^{4T}$ and $|V_{XXXX}|\le\alpha(2e^T+16e^{4T})$ | These uniform bounds are the exact-family replacement for polynomial-tail absorption |
| Time evolution of cell slope/curvature | **CLOSED identity** | Heat flow gives $(V_X)_S=V_{XXX}=O_T(1)$ and $(V_{XX}/2)_S=V_{XXXX}/2=O_T(\alpha)$ | Prevents an escaping coefficient direction from rotating at order $\lambda$ |
| Scaled probe moments | **CLOSED exact algebra** | For $1\le\ell\le2$, $\mu_2=\ell^2/44$, $\mu_4=3\ell^4/2288$, and the adaptive variance is at least $5/6292$ | Uniform Poincare and test-function norms use compactness of the length interval |
| Bounded-cell alternative | **CLOSED** | If central slope and curvature stay bounded and $\alpha\to0$, their trigonometric common-zero equations force $\alpha X_0\to0$ and $X_0=O(1)$, so the chart converges to translated $H_3$ | If $\alpha$ stays positive, ordinary compactness gives a nonconstant exact trigonometric limit |
| Escaping-cell alternative | **CLOSED** | Centering and Taylor expansion give $U=\lambda p+h$ with $\|h\|_\infty=O_T(1)$ and $\int p^2q\ge5/6292$ | The endpoint ledger is analytic and does not assume $\lambda\|v_X\|\to0$ |
| Exact-family unit-cell theorem | **CLOSED** | On the maximal distributional class $v\in L^2H^1$, $Qv\in L^2H_D^{-1}$, the bounded/escaping contradiction proves one graph constant for all $0<\alpha\le1$, all centers, all $1\le\ell\le2$, and both signs | Here $H_D^{-1}$ is the dual of $H_0^1$ with its full inherited $H^1$ norm; the constant exists nonconstructively and depends on fixed $T$ |
| Exact whole-line graph theorem | **CLOSED** | Unit intervals plus the full nonhomogeneous $H^{-1}(\mathbb R)$ direct sum globalize the exact-family cell theorem | Concerns the exact periodic potential lifted to the line, not the polynomial truncation |
| Exact periodic graph theorem | **CLOSED** | Partition the torus into $N=\lfloor2\pi/\alpha\rfloor$ equal cells of length in $[1,2)$ and use the torus $H^{-1}$ direct sum | Countable/finite Hilbert-space duality is analytic, not finite-certified |
| Energy evolution | **CLOSED for all torus $L^2$ data** | Smooth bounded real potential gives the standard parabolic evolution and exact energy identity | The finite certificate records only the energy rearrangement, not existence theory |
| Periodic collision-block contraction | **CLOSED** | Observability plus energy monotonicity gives $E(T)\le C_T^2(T+C_T^2)^{-1}E(-T)$ uniformly in $\alpha$ and sign | This is one fixed positive collision-scale block for a linear scalar row |
| Return to physical variables | **CLOSED exact conjugacy** | The block is $|d|\le T\kappa^{-2/5}$ and the endpoint $L^2$ scaling cancels | Only the row declared in R0.72T is covered |
| Numerical operator-norm stress test | **PASS as diagnostic** | Fourier Strang splitting plus forward--adjoint power iteration gave norms below $0.12$ for $\alpha\in\{1,.75,.5,.35,.25\}$ with resolution convergence | Numerical values are not proof and do not evaluate the analytic $C_T$ |
| Uniformity as $T\downarrow0$ | **FALSE** | The cubic collision limit retains the R0.72V lower-bound obstruction $C_T\gtrsim T^{-1/3}$ | No contraction factor uniformly separated from one on arbitrarily short scaled blocks is claimed |
| Outer heat-time concatenation | **OPEN** | R0.72W treats the $A_2$ collision block exactly | Must attach the pre/post-collision $A_1$ regions with consistent constants and gauges |
| Complete linearized shear subsystem | **OPEN** | One scalar Fourier row is controlled | Scalar damping normalization, all rows, and row summation must be audited together |
| Nonlinear Navier--Stokes / Clay | **OPEN** | No nonlinear pressure or vortex-stretching estimate appears in R0.72W | No continuation criterion, global regularity proof, or blow-up construction follows |

## Next minimal theorem

Prove an exact time-concatenation theorem joining the uniform $A_2$ collision
block to the two outer intervals where all remaining critical points are
nondegenerate.  The result must retain the physical Fourier normalization,
cellwise scalar gauges, energy factors, and constants needed for later row
summation.  Only after that gate should the full linearized shear subsystem be
assembled.
