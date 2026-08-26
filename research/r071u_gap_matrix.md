# R0.71U claim--evidence and gap matrix

**Audit date:** 2026-08-26

**Release boundary:** a zero-count-independent second-time-jet theorem for
positive global-shell entries, plus an exact globally smooth 2.5D NSE family
with arbitrary prescribed finite recurrence and uniformly bounded initial
energy/enstrophy

| ID | Candidate or claim | Exact calculation or required hypothesis | Status | Boundary |
|---|---|---|---|---|
| U1 | At a positive global-shell zero, the entry atom is comparable to the scale-zero slope jet. | \(C_j=0\Rightarrow T_ju=0\), so \(C_{j,t}=-\Delta F_j\); annular Bernstein gives \(J_j\asymp\kappa_j^{-6}\|C_{j,t}\|_2^2/Y\). | proved | Global cutoff only; arbitrary localized roots retain cutoff commutators and may have higher order. |
| U2 | The jet has the correct NSE scaling. | \(\kappa\mapsto\lambda\kappa\), \(Y\mapsto\lambda^4Y\), \(\|C_t\|_2^2\mapsto\lambda^{10}\|C_t\|_2^2\). | proved | Scale matching alone is not an a priori bound. |
| U3 | All global-shell entries occurring at one time are paid by the normalized Lamb square sum. | \(J_j\le\kappa_j^{-2}\|F_j\|_2^2/Y\), followed by the declared \(\dot H^{-1}\) frame inequality. | proved, truncation uniform | Does not sum distinct times. |
| U4 | A Hilbert-valued zero-sampling theorem can avoid the zero count and minimum separation. | If \(X\in H^2(I;H)\) and \(X(t_k)=0\), then \(\sum\|X'(t_k)\|^2\le2|I|^{-1}\int\|X'\|^2+(7|I|/3)\int\|X''\|^2\). | proved | \(|I|\) is the total audited interval length, not a gap or assumed event window. |
| U5 | The sampling proof uses vector-valued Rolle. | It uses \(\int_{t_{k-1}}^{t_k}X'=0\) and a weighted integral formula for \(X'(t_k)\). | rejected | No point with \(X'=0\) is asserted in a Hilbert space. |
| U6 | The positive global-shell atom sum is finite on compact classical intervals. | Apply U4 shellwise, use the annular comparison and frame sums, then monotone convergence. | proved | The bound depends on \(\mathcal R_Y(K)\) and second-time jets. |
| U7 | The first row of the summed theorem is Leray paid. | \(C_{j,t}=-\Delta T_ju_t\), \(u_t=\nu\Delta u+L\), hence \(\sum\kappa^{-6}\|C_{j,t}\|^2\lesssim\nu^2Y+\|L\|_{\dot H^{-1}}^2\). | proved | The theorem multiplies its integral by \(|K|^{-1}\), which is scale critical. |
| U8 | The recurrence row is Leray paid. | It requires \(\sum\kappa^{-6}\|C_{j,tt}\|^2\lesssim\nu^2\|\omega_t\|_2^2+\|L_t\|_{\dot H^{-1}}^2\). | **not proved** | Ordinary energy/enstrophy inequalities do not control this row. |
| U9 | The second-time-jet row is a dimensional artifact. | Both \(|K|^{-1}\int\kappa^{-6}\|C_t\|^2/Y\) and \(|K|\int\kappa^{-6}\|C_{tt}\|^2/Y\) have total scaling exponent zero. | rejected | Correct scaling does not imply Leray control. |
| U10 | A first-jet time integral alone controls repeated sampling for every forced shell path. | \(C_N=N^{-1}\sin(Nt)e\) has \(O(N)\) unit slope samples but bounded \(\int\|C_{N,t}\|^2\). | rejected at the forced-path level | This is not an NSE trajectory. |
| U11 | Exact unforced NSE trajectories can have arbitrarily many prescribed positive target-shell returns. | The 2.5D invariant class \(u=(f,0,v)\), a real \((2N+1)\)-parameter shear, a T-system response matrix, and finite-dimensional IFT give roots at arbitrary \(0<t_1<\cdots<t_N<T\). | proved | A new initial datum and trajectory may depend on each finite time set and on \(N\); no single infinite recurrent trajectory is produced. The multiplier must have compact support and isolate its target pair. |
| U12 | The 2.5D construction is an abstract passive-scalar forcing. | \(\operatorname{div}u=0\), \((u\cdot\nabla)u=(vf_z,0,0)\), pressure is constant, and the pair \(v_t=\nu v_{yy}\), \(f_t+vf_z=\nu\Delta f\) is exactly the unforced 3D NSE in this invariant class. | rejected | The scalar equation is triangular but the complete velocity is a genuine NSE solution. |
| U13 | Complex shear parameters give a one-dimensional zero manifold. | Parameters are declared real; then \(H:\mathbb R^{2N+1}\to\mathbb R^{2N}\) has rank \(2N\). | proved after correction | With complex parameters the original dimension count would be false. |
| U14 | Zeroing one complex coefficient automatically zeros a broad annulus. | Modular support lies in \((K+d\mathbb Z,L)\), \((-K+d\mathbb Z,-L)\), and \((d\mathbb Z,0)\); choosing \(d>R_*+|K|\) leaves only the target conjugate pair in the compact multiplier support. | proved after correction | Without modular isolation this inference is false. Noncompact multiplier tails cannot be zeroed this way. |
| U15 | The prescribed roots are first order and positive. | The kernel tangent is a nonzero combination of \(N+1\) T-system elements with \(N\) prescribed roots, hence every root is simple; at the exact root \(C_t=\rho^2F\ne0\) and \(\langle F,C_t\rangle>0\). | proved | “First-order vector zero” is used; this is not differential-topology transversality to a high-dimensional point. |
| U16 | The raw global-shell entry count is uniformly bounded on a fixed energy--enstrophy ball. | Scale the passive component to spend at most half the ledger, then take a sufficiently small nonzero point on the zero manifold for the shear half; \(N\) remains arbitrary. | rejected by genuine smooth NSE family | The exact numerical pair \((E_0,Y_0)\) varies with \(N\), so this does not rule out every nonuniform function of that pair. High Sobolev norms and the multiplier may also depend on \(N\). |
| U17 | The recurrence family disproves every weighted jet or occupation estimate. | Each atom is \(c_ms^2+O(s^3)\), while the interpolation condition and admissible parameter radius may deteriorate with \(N\). | **not proved; overclaim rejected** | It disproves raw count/separation, not the second-jet theorem or an unknown weighted Leray packing. |
| U18 | R0.71T's four-mode IFT zeros every unrelated broad annulus. | The published proof is exact for its thin four-mode target. A full finite target support is obtained by enlarging the IFT space to all active lattice modes separated from the seed shell. | clarified and strengthened | The thin-shell no-go remains valid; arbitrary broad supports containing the seed require a different construction. |
| U19 | Standard analyticity, Jensen, CKN, or Koch--Tataru supplies the new summed theorem. | Checked sources give trajectory-wise zero finiteness, conditional complex bounds, singular-set/local-energy control, or upper Carleson mass. | not located | The bounded search is not a novelty, priority, or nonexistence claim. |
| U20 | The jet is already defined at every Leray--Hopf or suitable weak zero time. | \(C_t(t_\beta)\) and \(Y(t_\beta)\) need not have distinguished pointwise representatives at an arbitrary weak zero. | **not proved** | R0.71U is a classical-interval theorem. |
| U21 | R0.71U proves a continuation criterion, singularity, or global regularity. | No certificate or argument supplies any of these. | **not proved** | Explicitly outside the release. |
| U22 | The scale ledger is an exact fixed-torus covariance for arbitrary real dilations without moving the frame. | Exact periodic covariance uses integer \(\lambda\), transports the time window and multiplier, and for a fixed dyadic frame normally takes \(\lambda=2^m\). | corrected | The scale exponents remain zero under the compatible covariance. |

## Gap ledger for the next release

| Open gap | Evidence now available | Decisive next test |
|---|---|---|
| Can the \(C_{tt}\) recurrence tax be removed or weakened? | Exact second-jet theorem; genuine recurrence family; forced sine stress test. | Measure atom mass and both theorem rows along high-recurrence 2.5D families; require constants uniform in \(N\). |
| Can a level-integrated charge replace the fixed zero level? | Banach--Lochowski and amplitude-excursion identities. | Formulate a scale-summable positive-height excursion target and derive its exact NSE/frame ledger. |
| Can weighted raw zero occupation be Leray paid? | Outgoing-coarea representation and scale-zero jet comparison. | Prove an endpoint Carleson trace or construct a family with noncollapsing weighted atom mass and bounded Leray ledger. |
| Can the theorem cross weak singular times? | Classical definition only; weak packet coefficients are at best a.e. differentiable. | Construct a canonical representative/relaxed measure before attempting any weak-limit estimate. |
