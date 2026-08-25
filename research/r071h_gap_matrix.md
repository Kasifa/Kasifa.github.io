# R0.71H gap matrix — angular variation and projective source curvature

**Date:** 2026-08-25

**Status:** formal claim-boundary document for the R0.71H release.
It records what the current calculations establish, what they reject, and
what remains unproved.  “Open” means that the present evidence does not close
the row; it does not mean that the statement is true.  “Not found in the
bounded search” is not an originality or nonexistence claim.

**Target.** The intended budget is a Leray-level estimate, uniform in the
localization and denominator regularization, of the form

\[
 \sup_{0<\varepsilon\le1}
 \sum_{j,Q}K_j^{-2}
 \operatorname{Var}_t(a_{j,Q,\varepsilon})<\infty,
 \qquad
 a_{j,Q,\varepsilon}
 =\frac{(\langle F_j,C_{j,Q}\rangle^+)^2}
 {Y(\|C_{j,Q}\|_2^2+\varepsilon)}.
 \tag{0.1}
\]

| Claim slot | Exact evidence | Status | Boundary retained / next burden |
|---|---|---:|---|
| Complete projected-Lamb acceleration | \(F_t=\nu\Delta F+\sum_{k,\ell}\mathfrak H_{k\ell}\), with the two transport terms and \(2\nu(\partial_m u_k\cdot\nabla)\partial_m u_\ell\) | closed algebraically | Classical solutions only; every ordered shell pair remains, including high--high-to-low |
| Complete localized direction source | \(C_t=\nu\Delta C+G\), where \(G\) contains \(\nabla\times(\chi\mathfrak G_{k\ell})\), Eulerian cutoff movement/residual, and the viscous collar | closed algebraically | A transported cutoff still has \(\chi_t=-V_r\cdot\nabla\chi\) in the Eulerian ledger |
| Unit-direction derivative | On each component of \(\{d>0\}\), \(E_t=d^{-1/2}P_{E^\perp}C_t\) | closed; independently checked | Not a global identity across zero faces |
| Normalized signed-work derivative | \(\beta_t=\langle F_t,E\rangle+d^{-1/2}\langle P_{E^\perp}F,C_t\rangle\) | closed | Radial \(C_t\) cancels exactly; all Lamb acceleration and angular terms remain |
| Positive-part crossing | Since \(x\mapsto(x^+)^2\) is \(C^1\), \(q_t=2\beta^+\beta_t\) has no atom at \(\beta=0\) | closed | This does not address \(d=0\) |
| Enstrophy normalization | \(a_t=(2\beta^+/Y)\beta_t-aY_t/Y\) | closed | \(|Y_t|/Y\) is not controlled by standard energy and cannot be treated as a harmless coefficient |
| Global epsilon quotient ledger | \((a_\varepsilon)_t=\sigma_\varepsilon a_t+(\sigma_\varepsilon)_ta\), \(\sigma_\varepsilon=d/(d+\varepsilon)\) on \(d>0\); the direct \(P_\varepsilon\) formula is global | closed algebraically | \((\sigma_\varepsilon)_ta\) may concentrate at zero faces; pointwise convergence is not uniform integrability |
| Denominator faces | Absolute variation pays both one-sided values at every component endpoint, even when their distributional net jump cancels | closed deterministic fact | A uniform \(\varepsilon\downarrow0\) estimate must retain both faces |
| Partition refresh | Refreshing cells produces jumps of the nonlinear \(a_Q\); linear reconstruction of \(B_Q\) does not cancel them | closed deterministic fact | Refresh atoms must be included in the shell--cell BV sum |
| Unit projective-curvature identity | On \(J\Subset\{d>0\}\), \(\|E_t\|^2+\nu^2\|P_{E^\perp}A_0E\|^2=-\nu r_t+\|P_{E^\perp}G\|^2/d\) | **PASS**, exact and independently audited | Assumes a classical path in \(D(A_0)\); integrated identity is automatic only inside one positive-denominator component |
| Pure heat sign | For \(G=0\), \(r_t=-2\nu\operatorname{Var}_p(\mu)\le0\), and the Rayleigh drop pays square angular speed and spectral curvature | closed; Fourier-audited | Localization moves terms into \(G\); the pure-heat sign alone is not the NSE estimate |
| Naive \(d\mapsto d+\varepsilon\) substitution | The soft direction \(Z=C/\sqrt{d+\varepsilon}\) is not unit and \(Q=I-Z\otimes Z\) is not an orthogonal projection | **rejected exactly** | The clean unit-sphere identity cannot be globalized by denominator replacement |
| Exact soft projective identity | \(\|Z_t\|^2+\nu^2\|X_\varepsilon\|^2=-\nu(r_\varepsilon)_t+\|H_\varepsilon\|^2+\nu r_\varepsilon m_t\) | closed; independently audited | The defect \(+\nu r_\varepsilon m_t\) has no sign |
| Orthogonal soft form | On \(d>0\), the tangent identity has \(+\nu m_t r\); using full speed adds \(m_t^2/(4m)\) | closed; independently audited | Still depends on the unit direction \(e=C/\sqrt d\) and does not cross a zero face |
| Uniform epsilon source ratio | For \(C(t)=(t,0)\), \(A_0=0\), \(G=(1,0)\), \(\int\|H_\varepsilon\|^2dt=3\pi/(8\sqrt\varepsilon)\) | **rejected for the naive soft source** | This finite-dimensional crossing rejects a uniform estimate for that positive soft-source term; it does not reject every joint BV cancellation |
| Critical-residence arc estimate | Cauchy--Schwarz plus the unit identity reduces arc length to endpoint \(K^{-2}r(t_-)\) and \((\nu K^2)^{-1}\int\|P_{E^\perp}G\|^2/d\) | conditional | Neither ratio is known uniformly after localization; amplitude weights, \(F_t\), \(Y_t/Y\), and faces remain |
| Nominal damping | \(\beta_t+\nu K^2\beta=\mathcal R\), with exact complete remainder \(\mathcal R\) | closed decomposition | \((\Delta+K^2)F\), localized \(C\), shell transfer, movement, and collar are generally of the nominal leading size and have no sign |
| Two-frequency-power gap | Direct Young gives \(K^{-2}|a_t|\lesssim a+(\|F\|^2/Y)\Gamma^2+K^{-2}a|Y_t|/Y\), while the heat endpoint controls only \(K^{-2}\|F\|^2/Y\) | closed scale audit | A direct closure needs two additional frequency powers of curvature depletion after summation; no such decay has been derived |
| Pointwise energy-only angular estimate | Fixed-energy global-smooth 2D3C family has \(d_K(0)>0\) and \(\Omega_K(0)=UK/2\to\infty\) for the declared low-sphere multiplier | **rejected by exact NSE family** | The rejection concerns unweighted instantaneous \(\|E_t\|\) and does not, without a multiplier comparison, assert the same witness for every preassigned smooth matched frame |
| Pointwise scalar angular factor | The same family has \(\mathcal A_{\rm ang}(0)=U^3K/8\to\infty\) | rejected as a uniform instantaneous bound | This factor accumulates only \(O(K^{-1})\) on a fixed viscous-time window |
| Integrated angular turning | On the 2D3C witness, \(\int_0^{M/(\nu K^2)}\|E_t\|dt=O(K^{-1})\) | supported only on the witness | The family does not disprove a uniform integrated estimate for general NSE solutions |
| Full weighted BV on the witness | \(K^{-2}\operatorname{TV}_{[0,M/(\nu K^2)]}(q/Y)\to0\) | supported only on the witness | Not evidence for a general theorem; also not a counterexample to the target |
| Nonconstant-cutoff projective source | For \(\chi_\delta=(1+\delta\cos Z)/2\), the normalized constants \(D_\delta,R_\delta,J_\delta\) are explicit and \(K^{-2}\int\|P_{E^\perp}G\|^2/d\to\nu MJ_\delta>0\) | exact finite-Fourier saturation | The source ratio saturates but does not diverge |
| Source--viscous cancellation | In the same heat limit, the source cancels viscous projective curvature and actual arc length is \(O(K^{-1})\) | exact asymptotic cancellation | Separate positive estimates for source and viscous curvature lose the leading cancellation; the next gate should use the joint evolution |
| Fixed-template phase denominator | For the six-mode field and one fixed nonzero matched cutoff template, compact phase translation has a uniform positive denominator | closed for that family | Does not cover increasing Fourier dimension, degenerating templates, or approach to a genuine denominator kernel |
| Leray-level passage | Standard bounds are \(u\in L_t^\infty L_x^2\cap L_t^2H_x^1\) | open | No uniform bound yet for the acceleration, projective ratio, denominator faces, \(Y_t/Y\), or shell--cell sum |
| Full target (0.1) | No source currently derives all of its rows from independent NSE budgets | open | Must not be replaced by the target BV, crossing count, denominator lower bound, or known continuation norm |
| Literature collision | Bounded primary-source search found exact neighbors for material direction, spatial coherence, dynamic wavenumber, occupation, frequency windows, bad intervals, and BV--crossing equivalence | no direct collision found in bounded search | Not an originality, priority, exhaustive-search, or global nonexistence statement |

## Exact soft-denominator boundary

The two projective ledgers must not be merged silently.

1. The clean unit-sphere identity uses

   \[
   E=C/\sqrt d
   \]

   and is valid only on connected components of \(\{d>0\}\).
2. The soft vector

   \[
   Z=C/\sqrt{d+\varepsilon}
   \]

   is globally defined, but \(\|Z\|^2=m=d/(d+\varepsilon)\ne1\).  Its
   identity contains \(+\nu r_\varepsilon m_t\).  The orthogonal tangent
   form contains \(+\nu m_t r\), and full speed adds
   \(m_t^2/(4m)\).
3. The exact linear crossing

   \[
   \int_{\mathbb R}\|H_\varepsilon\|^2dt
   =\frac{3\pi}{8\sqrt\varepsilon}
   \]

   prevents a uniform estimate of the positive soft-source term in
   isolation.

This does not make the \(q_\varepsilon\) quotient invalid.  It means that
its direct derivative ledger and the unit projective identity serve
different purposes and must be connected through explicit face or defect
control.

## Primary-source boundary

The source ledger is version-pinned in
`research/r071h_literature_audit.md`.  The closest interfaces are:

- [Gibbon--Holm--Kerr--Roulstone](https://arxiv.org/abs/nlin/0512034): exact
  Euler material-direction and pressure-Hessian curvature, but no localized
  NSE weighted BV;
- [Beirão da Veiga--Berselli](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf),
  [Vasseur](https://arxiv.org/abs/0705.2446), and
  [Dascaliuc--Grujić](https://arxiv.org/abs/1107.0058): spatial direction
  coherence or direction-divergence conditions, not temporal angular
  variation;
- [Cheskidov--Shvydkoy](https://arxiv.org/abs/1102.1944) and
  [Cheskidov--Dai](https://arxiv.org/abs/1507.06611): dynamic-wavenumber and
  amplitude-weighted time--frequency conditions; the critical occupation is
  a regularity hypothesis, not a Leray consequence;
- [Gibbon--Doering](https://arxiv.org/abs/math/0406146): genuine interval
  width estimates for different global derivative variables;
- [Łochowski](https://arxiv.org/abs/1503.01746): exact BV--integrated-crossing
  equivalence, but no PDE budget producing BV.

The bounded search found no primary theorem that supplies the full target
(0.1).  This is a limited literature finding, not an originality claim.

## Route verdict

The current algebra closes the radial question but not the angular budget.
The unit projective identity is valid and independently checked, while the
naive soft-denominator extension is false and its isolated source term has an
exact \(\varepsilon^{-1/2}\) crossing divergence.  The global-smooth 2D3C
family rejects pointwise energy-only angular control but leaves the integrated
critical target open.  The nonconstant-cutoff calculation shows that a
separate positive source estimate can discard the leading viscous-source
cancellation.

The next gate is therefore a joint, amplitude-weighted projective identity or
commutator estimate that retains all shell pairs, movement, collar,
acceleration, \(Y_t/Y\), and face terms.  It must recover the two missing
frequency powers without assuming a Serrin/Besov norm,
Cheskidov--Dai occupation, denominator nondegeneracy, or the weighted-BV sum
itself.  If that gate reduces to one of those inputs, the temporal-residence
route is conditional and should stop.  The present evidence does not justify
the stronger statement that every possible integrated closure is impossible.
