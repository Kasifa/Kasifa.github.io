# R0.71R claim--evidence matrix

**Audit date:** 2026-08-26  
**Release boundary:** finite conditional parabolic-incidence theorem and exact
forced-parabolic method obstructions only

| ID | Claim | Evidence | Status | Exact boundary |
|---|---|---|---|---|
| R1 | R0.71P leaves a componentwise positive-entry target after simultaneous spatial batching. | `research/r071p_report-source.md`, Theorem 5.1. | inherited, unconditional | Distinct temporal entries remain atomic. |
| R2 | The localized observable obeys \(C_{j,Q,t}-\nu\Delta C_{j,Q}=G_{j,Q}\) with the source in (2.3). | Vorticity equation, multiplier commutation, exact product rule; R0.71R Section 2. | proved | Fixed smooth cutoffs and annular multipliers. |
| R3 | At a zero, Duhamel gives \(h^{-1}\|C(t+h)\|_2^2\le\int_t^{t+h}\|G\|_2^2\). | Heat-semigroup contraction and Cauchy--Schwarz. | proved | It is an upper endpoint estimate, not an event lower charge. |
| R4 | The \(\rho\)-incidence condition (3.3), noncollapsing parabolic heights \(0<\theta_-\le\theta_\beta\le\theta_*\), and same-observable overlap imply the packing theorem (4.1). | Exact termwise inequality (4.2), Tonelli, and overlap multiplicity. | proved, conditional finite | \(\Gamma_\rho\), \(M\), and forward windows are hypotheses; without \(\theta_->0\), shrinking windows can trivialize \(M\). |
| R5 | The theorem has a local source-relative Carleson form. | Restrict the proof to owned windows contained in \(J\); formula (4.3). | proved, conditional | Not a \(|J|\)-Carleson measure without a local source estimate. |
| R6 | The nonlinear observable source satisfies the \(\kappa_j^4\|F_j\|_2^2\) square bound. | Product expansion, cutoff derivative square sums, annular Bernstein; (5.2). | proved | Constants depend on the fixed frame and multiplier. |
| R7 | The viscous localization commutator satisfies the \(\nu^2\kappa_j^6\|W_j\|_2^2\) square bound. | Four order-three product terms; (5.3). | proved | Same fixed-frame boundary. |
| R8 | The general source ledger is \(\sum\kappa^{-4-\rho}\|G\|^2\lesssim\sum\kappa^{-\rho}\|F\|^2+\nu^2\sum\kappa^{2-\rho}\|W\|^2\). | Multiply (5.2)--(5.3) by \(\kappa^{-4-\rho}\); formula (5.4). | proved | Requires cutoff derivative square overlap through order three. |
| R9 | At \(\rho=2\), the normalized source measure is finite from Leray energy. | \(\|L\|_{\dot H^{-1}}^2/Y\lesssim\|u\|_2Y^{1/2}\), Cauchy--Schwarz in time, energy inequality. | proved | Finite intervals; no atomic sampling inference without incidence. |
| R10 | At \(\rho=2\), under uniform \(\Gamma_2,M\), the finite-truncation target is energy-paid. | Theorem 4.1 plus (5.5)--(5.10); Corollary 5.1. | proved, conditional | \(\Gamma_2\) is not scale invariant. |
| R10a | NSE scaling is compatible with a universal \(\Gamma_\rho\) only at \(\rho=0\). | Exact scaling exponents (5.12)--(5.15); certificate `nseFrequencyJetScaling`. | proved | Scaling verdict; not a positive-time packing theorem. |
| R10b | At \(\rho=0\), the source ledger requires \(\|L\|_2^2/Y+\nu^2\|\nabla\omega\|_2^2/Y\). | Formula (5.16). | proved | Requires normalized \(L^2\)-Lamb and palinstrophy control, not supplied by Leray energy. |
| R10c | No \(\rho\) in the one-parameter endpoint-square certificate (3.3) is both scale covariant and Leray paid. | Scale covariance selects \(\rho=0\); Leray payment begins at \(\rho=2\); formula (5.17). | proved, scoped method verdict | Does not exclude another Duhamel design or a signed or bilinear incidence functional. |
| R10d | A genuine NSE high-frequency initial jet has the Taylor-jet surrogate \(\Gamma_{2,{\rm jet}}=K^2/(4\theta^2)\). | Exact scaled Fourier jet (5.18)--(5.21), exact certificate. | proved at initial-jet coefficient | This is not a lower bound for the actual positive-time \(\Gamma_2\); no Duhamel remainder estimate is claimed. |
| R11 | Direct domination of the atomic entry measure by the absolutely continuous source square is impossible. | Singletons have zero \(dt\)-density mass but positive entry atom. | proved, elementary | Window lower charges remain possible. |
| R12 | A positive even-order entry is invariant under positive observable scaling while quadratic charges scale as \(\varepsilon^2\). | \(C_\varepsilon=\varepsilon(t-1/2)^2\), exact certificate `scaledEvenTouch`. | proved, abstract forced parabolic | \(F,Y\) are held fixed; not an NSE scaling family. |
| R13 | One analytic forced scalar path can have \(N\) positive entries and normalized source energy one. | Squared-root polynomial family, exact rational integration and independent Gauss audit. | proved, abstract forced parabolic | Not a repeated-entry NSE construction. |
| R14 | An all-component source-square budget can stay bounded while the entry union grows like the number of components. | \(C_q=2^{-q}(t-b_q)^2\), exact energy bound below three. | proved, abstract forced parabolic | Not an NSE frame realization. |
| R15 | Complex radius and relative Jensen data do not supply the missing absolute incidence amplitude. | Positive scalar multiplication preserves relative analytic data and entry mass but shrinks quadratic charge. | proved, abstract analytic | Complements, but does not replace, the R0.71Q anchor obstruction. |
| R16 | CKN, Koch--Tataru, physical-scale flux, nodal-set, and backward-uniqueness theorems do not directly prove the R0.71R incidence/overlap hypotheses. | Two bounded primary-source waves in `research/r071r_literature_audit.md`. | bounded negative finding | Not a nonexistence, originality, or priority claim. |
| R17 | R0.71R proves a uniform NSE incidence law, temporal packing, continuation criterion, or global regularity. | No supporting theorem or certificate. | **not proved** | Explicitly excluded from every public claim. |

## Decision gate

The \(\rho=2\) theorem would pay the R0.71P target from energy if the following
held uniformly as \(\Lambda\uparrow\Lambda_\infty\) and a compact classical
interval approached a possible maximal endpoint:

1. every entry owns a forward height
   \(h_\beta=\theta_\beta\kappa_j^{-2}\) with
   \(0<\theta_-\le\theta_\beta\le\theta_*\);
2. the scale-normalized post-entry amplitude dominates \(A_{\beta,+}\) with
   one constant \(\Gamma_2\);
3. the owned windows of every fixed observable have overlap at most one
   constant \(M\).

The source-square total measure after these gates is Leray-payable.  Covariant
scaling shows that the optimal \(\rho=2\) certificate constant has two missing
powers under dilation, while the genuine NSE initial jet exhibits the same
\(K^2\) pressure only at the Taylor-jet level.  Choosing \(\rho=0\) repairs scaling and loses the Leray
budget.  R0.71R therefore retains the finite conditional theorem and rules out
only the simultaneous scale covariance and Leray payment of the
one-parameter endpoint-square, power-law certificate (3.3).  Other Duhamel
designs, and genuinely signed or bilinear scale-critical alternatives, remain
open for R0.71S.
