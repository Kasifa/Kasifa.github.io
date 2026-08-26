# R0.71T claim--evidence and gap matrix

**Audit date:** 2026-08-26
**Release boundary:** a genuine smooth positive-time internal entry, an
internal scaling obstruction to the bare normalized Leray--Lamb time budget,
and two exact but presently strong replacement charges

| ID | Candidate or claim | Exact calculation or required hypothesis | Status | Boundary |
|---|---|---|---|---|
| T1 | The R0.71O seed has no target-shell velocity or vorticity, but its projected Lamb field is nonzero there. | For \(U=(0,\cos x_1,\cos x_2)\) and \(|k|^2=2\): \(Y_*=1\), \(\|F_*\|_2^2=1/4\), \(\|\operatorname{curl}F_*\|_2^2=1/2\). | proved exactly | Normalized periodic torus and the declared real-even shell projection. |
| T2 | A positive-time full-shell zero can be prescribed by perturbing the initial target shell. | For fixed small \(\tau>0\), \(\Phi(a,w)=T_j\operatorname{curl}S_\tau(aU+R_jw)\) has \(D_w\Phi(0,0)=e^{\nu\tau\Delta}|_{E_j}\), hence the finite-dimensional implicit-function theorem gives \(w(a)\) with \(\Phi(a,w(a))=0\). | proved, local classical | Uses the standard \(C^1\) local NSE flow map on smooth divergence-free data; not backward evolution or an onto claim for the full flow. |
| T3 | The precompensation has the correct nontrivial quadratic term. | Duhamel expansion gives \(w(a)=-a^2\tau\operatorname{curl}F_*+O(a^3)\), equivalently the target velocity correction is \(-a^2\tau F_*+O(a^3)\). | proved asymptotically | Fixed sufficiently small \(\tau\); the remainder constant may depend on \(\tau\). |
| T4 | The prescribed zero is a genuine internal positive entry. | At \(t=\tau\), \(W_j=0\), \(F_j=a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\), and \(C_t=-\Delta F_j\). Thus the zero is simple and \(\langle F_j,C_t\rangle=\|\nabla F_j\|_2^2>0\). | proved for all sufficiently small nonzero \(a\) | The observation interval can be \([0,2\tau)\); its endpoints are not the constructed zero. |
| T5 | At least one localized cell also has a simple positive internal entry. | When the entire shell vanishes, \(c_Q=\operatorname{curl}(\chi_Q\operatorname{curl}F_j)\) and \(\langle F_j,c_Q\rangle=\int\chi_Q|\operatorname{curl}F_j|^2\). A nonnegative covering partition makes at least one term positive. | proved | Special to the constructed full-shell root. An arbitrary localized zero does not imply \(W_j=0\). |
| T6 | Every positive global-shell entry is simple. | If \(\chi=1\), \(C=0\Rightarrow W=0\). If \(C_t=-\Delta F=0\), annular zero mean gives \(F=0\), contradicting \(A_+>0\). | proved | Does not give a total-variation or recurrence bound. |
| T7 | Every positive localized-cell entry is simple. | For a general \(C_Q=0\), \(W_j\) need not vanish and the viscous cutoff commutator remains in \(C_{Q,t}\). | **not proved; false inference identified** | Even positive touches remain possible for arbitrary localized roots. |
| T8 | The constructed global-shell atom has a scale-zero slope representation. | On the single radius \(\rho^2=2\kappa^2\), \(\kappa^{-2}A_+=\kappa^{-2}\|C_t\|_2^2/(\rho^4Y)=(1/4)\kappa^{-6}\|C_t\|_2^2/Y\). | proved at a simple full-shell zero | An instantaneous sample, not yet a summed a priori charge. |
| T9 | The small-amplitude internal atom is positive with an explicit leading term. | \(\kappa^{-2}A_+(a)=a^2e^{-2\nu\tau}/4+O(a^3)\) at the base shell \(\kappa=1\). | proved asymptotically | No lower bound uniform in arbitrary data is claimed. |
| T10 | The base bare budget has an explicit small-amplitude expansion. | On \([0,2\tau)\), \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt=a^2(1-e^{-4\nu\tau})/(16\nu)+O(a^3)\). | proved asymptotically | Uses \(\|F_*\|_{\dot H^{-1}}^2=1/8\). |
| T11 | The bare budget cannot pay all internal atoms with a scale-uniform constant. | Choose \(a_\lambda=\lambda^{-2}\), then apply the compatible NSE dilation. The atom is \(e^{-2\nu\tau}\lambda^{-4}/4+O(\lambda^{-6})\), the budget is \((1-e^{-4\nu\tau})\lambda^{-6}/(16\nu)+O(\lambda^{-8})\), and their ratio is \([2\nu/\sinh(2\nu\tau)]\lambda^2+o(\lambda^2)\). | proved for a genuine smooth internal family | Excludes only a constant uniform along this covariant family with the bare right side. |
| T12 | The scaling obstruction is an artifact of growing initial energy. | The scaled initial energy is \(O(\lambda^{-2})\), \(\dot H^{1/2}\)-norm squared is \(O(\lambda^{-1})\), and enstrophy is \(1+o(1)\). | **rejected** | Higher Sobolev norms still grow; a constant depending on the full initial profile is not excluded. |
| T13 | An outgoing radial occupation density represents all finite-order internal entries, including even touches. | With \(r=\|C\|_2\), \(\xi=C/r\), \(q=\langle F,\xi\rangle_+^2/Y\), the limit \(\lim_{\delta\downarrow0}\int q\rho_\delta(r)(r_t)_+dt\) equals the sum of right-entry faces. | proved for finite isolated finite-order zeros | Exact representation only; \(\rho_\delta\) concentrates at the zero level. |
| T14 | The outgoing occupation density is paid by the ordinary Leray budget. | \((r_t)_+\le\|G\|_2\) leaves the factor \(\rho_\delta(r)\sim\delta^{-1}\); no uniform zero-level occupation estimate follows. | **not proved** | Requires a new outgoing-level Carleson or occupation theorem. |
| T15 | A symmetric trace identity gives a finite conditional payment without sampling coherence. | \(q(t_*)=(2h)^{-1}\int_Iq+\int_IK_hq_t\), followed by an active-direction Bessel bound. | proved, finite conditional | Retains strong \(L^2\)-Lamb, \(F_t\), \(Y_t/Y\), and repeated-direction multiplicity. |
| T16 | Freezing \(Y\) in the trace argument is harmless. | \(f_t=\langle F_t,e\rangle/\sqrt Y-(Y_t/2Y)f\). The second term cancels a false variation in the exact exponential test. | **rejected** | The denominator term is scale-critical, not lower order. |
| T17 | A fixed packet coefficient admits a Leray-paid amplitude-weighted excursion charge. | The weak equation gives \(a_\psi\in W^{1,2}\) and \(\sum_k\sup(a_\psi)_+\le V_I^+(a_\psi)\), with an explicit energy/dissipation bound. | proved for a fixed smooth divergence-free packet | Constants depend on packet derivatives; this is not the normalized shell-cell entry atom. |
| T18 | BV or \(W^{1,2}\) control bounds the raw number of zero entries. | \(g_N(t)=N^{-1}\sin Nt\) has uniformly bounded variation but \(N\) positive zero entries. | **rejected at the functional level** | The scalar family is not an NSE trajectory. |
| T19 | CKN, flux locality, Koch--Tataru, or maximal regularity directly supplies the missing raw-entry payment. | The checked theorems control local energy/singular sets, ensemble/time-averaged flux, upper Carleson norms, or strong forcing classes. | not located in the bounded audit | This is not a literature-exhaustion or novelty claim. |
| T20 | R0.71T proves a recurrence theorem, continuation criterion, singularity, or global regularity. | No such proof or certificate exists. | **not proved** | Explicitly outside this release. |

## Exact internal no-go theorem boundary

The scaling family excludes an inequality of the form

\[
 \sum_{\beta\in\mathcal E_{\rm int}}
 \kappa_{j(\beta)}^{-2}A_{\beta,+}
 \le C
 \int_K\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}\,dt
\]

when all of the following are required simultaneously:

1. the statement covers every smooth periodic NSE solution and the
   covariantly rescaled shell--cell frame;
2. the constructed positive-time entry is counted as an internal event;
3. the constant \(C\) stays uniform along the bounded-energy,
   bounded-enstrophy family;
4. the right side is precisely the bare normalized
   \(L_t^2\dot H_x^{-1}\) Lamb integral.

It does not exclude a noncovariant fixed-frequency theorem, a constant that
depends on high Sobolev norms and grows at least quadratically with frequency,
an added initial/BV/atomic term, a scale-matched strong Lamb or material
derivative charge, or a statement formulated only at weak singular times.

## Route decision

The R0.71S boundary caveat is closed: the two-derivative mismatch persists for
a genuine smooth positive-time internal entry and is not caused by growing
initial energy.  The bare normalized Leray--Lamb time integral should no
longer be treated as the final payment candidate for this atom.

The next finite gate is therefore narrower.  It must either prove a summed
bound for the scale-zero full-shell jet/outgoing occupation charge, or replace
raw zero entry by an amplitude-thresholded excursion quantity that a genuine
Leray budget can pay.  Neither closure is supplied in R0.71T.
