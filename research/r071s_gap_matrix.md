# R0.71S claim--evidence and gap matrix

**Audit date:** 2026-08-26
**Release boundary:** finite conditional directional-packet theorem and
packet/scaling obstructions; the genuine NSE no-go includes an initial
observation-boundary entry

| ID | Candidate or claim | Exact calculation or required hypothesis | Status | Boundary |
|---|---|---|---|---|
| S1 | The inherited target is \(a_\beta=\kappa_j^{-2}(\langle F_j,e_\beta\rangle_+)^2/Y\). | R0.71P entry theorem and \(e_\beta=c_\beta/\|c_\beta\|_2\). | inherited, proved | Finite-order positive entries of the fixed shell--cell frame. |
| S2 | \(a_\beta\) is invariant under covariant NSE scaling. | \(\kappa:+1\), \(\langle F,e\rangle:+3\), \(Y:+4\). | proved | Compatible integer/dyadic fixed-torus dilations and covariant frames. |
| S3 | The normalized Leray Lamb density is scale zero, but its time integral has exponent \(-2\). | \(\|L\|_{\dot H^{-1}}:+2\), \(Y:+4\), \(dt:-2\). | proved | Exact covariant scaling, not a regularity assertion. |
| S4 | A nonzero-mean \(L^2\)-normalized packet recovers the entry scale. | \(p_\beta=\int\eta_\beta f_\beta\), \(\int\eta_\beta=\mu\sqrt h\), and directional coherence (2.4). | proved, conditional finite | Coherence follows after event-dependent shrinking for a fixed finite classical family; uniform \(\theta_->0\) is not proved. |
| S5 | Critical packet Bessel payment implies the finite target estimate. | Theorem 2.1: \(\sum a_\beta\le C_TB_{\rm crit}[\mu^2(1-\delta)^2\theta_-]^{-1}\int\|L\|_{\dot H^{-1}}^2/Y\). | proved, conditional finite | \(B_{\rm crit}\), coherence, and noncollapsing windows are hypotheses. |
| S6 | One critical packet already forces \(B_{\rm crit}\ge\kappa_j^2\). | \(\|\Phi_\beta\|^2=\kappa_j^2\); test the Bessel inequality with \(Z=\Phi_\beta\). | proved | Diagonal bound; independent of overlap and direction separation. |
| S7 | \(N\) identical indexed packets force \(B_{\rm crit}\ge N\kappa_j^2\). | Retain the \(N\) equal coefficient terms when testing with the common packet. | proved | Exact duplicate statement; distinct disjoint packets need not pay the factor \(N\). |
| S8 | Unweighted directional packets may have an overlap-controlled Bessel bound. | Remove the factor \(\kappa_j\) from the dual packet. | available but strong-budget only | Pays \(\int\sum_j\|F_j\|_2^2/Y\), not the Leray \(\dot H^{-1}\) budget. |
| S9 | Critical Bessel implies a directional Carleson condition. | Test with \(Z_j=\mathbf1_Jv\): \(\mu^2\sum_{I_\beta\subset J}\kappa_j^2h_\beta|\langle v,e_\beta\rangle|^2\le B_{\rm crit}|J|\|v\|^2\). | proved, necessary | No general sufficiency claim for arbitrary packet geometry. |
| S10 | Directional Carleson handles repeated same-observable entries without deleting them. | For common direction, \(N_J\theta_-\le B_{\rm crit}|J|/\mu^2\). | proved, conditional | It exposes the count inside the constant; it does not prove a uniform count. |
| S11 | A backward-heat adjoint repairs the derivative mismatch. | For the unnormalized source \(g=\langle F,e\rangle\), the pure annular kernel \(q=\kappa e^{-\nu\kappa^2(h-r)}\) has frozen-denominator paid-dual norm squared \(\kappa^2(1-e^{-2\nu\theta})/(2\nu)\). | **rejected in the frozen-denominator packet model; not a full normalized NSE identity** | With \(f=g/\sqrt Y\), the endpoint contains \(\sqrt Y f\), or normalized evolution produces \(Y_t/(2Y)\). Localization also retains the viscous cutoff commutator and an alignment requirement. |
| S12 | A bounded bilinear packet with nonzero constant mode sees the entry. | \(\mathcal Q_{K,h}[f_0]=\theta k_0\kappa^{-2}f_0^2\), \(k_0=\langle1,K1\rangle\ne0\). | proved | Its form bound relative to \(X=\kappa^{-1}f\) is at least \(\kappa^2|k_0|\). |
| S13 | A mean-zero or signed bilinear packet avoids the Bessel tax and still sees every entry. | If \(k_0=0\), the packet is exactly zero on a constant positive directional signal. | **rejected** | It may measure oscillation, but it cannot give the required event lower comparison without another hypothesis. |
| S14 | Signed face cancellation pays an even-order positive touch. | At even order, \(A_-=A_+=A>0\), so the signed atom is zero. | **rejected** | The one-sided/Jordan target remains positive. |
| S15 | The scalar even-touch family tests the signed design. | \(C_\varepsilon=\varepsilon(t-t_0)^2e\), \(F=e\), \(Y=1\): target one, signed/constant-cancelling packet zero. | proved, abstract forced path | Not an NSE trajectory and not evidence that NSE realizes an even touch. |
| S16 | Bare Leray-time payment can be uniform for the genuine NSE initial-face scaling family. | Initial target stays \(1/4\); corresponding time integral equals \(\lambda^{-2}\) times the base integral. | **rejected by genuine NSE scaling** | Applies to covariant inequalities that include the observation-boundary entry. |
| S17 | The genuine scaling no-go also excludes every internal-entry NSE identity. | No internal entry or repeated internal-entry NSE scaling family is constructed. | **not proved** | Internal-only, NSE-specific nonlinear mechanisms remain open. |
| S18 | A scale-invariant dynamical right side replacing the bare time integral is known. | No candidate is closed in R0.71S. | open | Any candidate must retain the full NSE coupling and pay recurrence. |
| S19 | R0.71S proves temporal packing, continuation, or global regularity. | No such theorem or certificate exists. | **not proved** | Explicitly excluded. |

## Exact conditional gate

For a finite positive-entry family, the directional packet argument closes
only if all of the following hold:

1. every event owns a right parabolic window
   \(h_\beta=\theta_\beta\kappa_j^{-2}\) with one
   \(0<\theta_-\le\theta_\beta\le\theta_*\);
2. its nonzero-mean packet satisfies the uniform coherence inequality
   \(p_\beta\ge(1-\delta)\mu\sqrt{h_\beta}f_\beta(t_\beta)\);
3. the complete repeated-event family satisfies the critical Bessel
   inequality (2.8).

Under these assumptions Theorem 2.1 is exact.  However, the third assumption
has \(B_{\rm crit}\ge\max\kappa_j^2\) before any recurrence or overlap is
considered.  The first and second assumptions are also not uniform near an
infinite-frame or maximal-time limit.

## Route decision

The nonzero-mean temporal packet, its frozen-denominator backward-heat
realization, and every bounded bilinear kernel with a nonzero constant mode
all recover the corresponding model entry at the cost of the same
\(\kappa_j^2\) paid-dual norm.  Constant-cancelling
packets remove that norm contribution only by losing a constant positive
directional trace and, in particular, an even-order positive touch.

The genuine NSE initial-face scaling family rules out a scale-uniform final
estimate by the bare time integral of \(\|L\|_{\dot H^{-1}}^2/Y\) whenever
the target includes observation-boundary entries.  This does not settle an
internal-entry-only NSE identity.  A later route must either derive such an
internal nonlinear mechanism or replace the final right side by a genuinely
scale-invariant dynamical charge.
