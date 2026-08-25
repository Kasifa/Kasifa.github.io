# R0.71I gap matrix — joint one-sided creation versus physical-time heat volume

**Date:** 2026-08-26

**Status:** formal claim-boundary document.  “Open” means that this release
does not close the row.  “Rejected” refers only to the quantified estimate and
multiplier class stated in that row.  It is not a regularity, singularity,
originality, or global impossibility claim.

**Target.**  For

\[
 a_{j,Q,\varepsilon}
 =\frac{(\langle F_j,C_{j,Q}\rangle^+)^2}
 {Y(\|C_{j,Q}\|_2^2+\varepsilon)},
 \tag{0.1}
\]

the intended endpoint is a Leray-level estimate, uniform in shell--cell
truncation, localization, refresh, and \(\varepsilon\downarrow0\), for

\[
 \sum_{j,Q}K_j^{-2}\operatorname{TV}_t(a_{j,Q,\varepsilon}).
 \tag{0.2}
\]

| Claim slot | Exact evidence | Status | Boundary retained / next burden |
|---|---|---:|---|
| Complete projected-Lamb acceleration | \(F_t=\nu\Delta F+\sum_{k,\ell}\mathfrak H_{k\ell}\) | closed algebraically | Classical solutions; all ordered shell pairs remain |
| Complete localized-vorticity acceleration | \(C_t=\nu\Delta C+G\), including transfer, Eulerian movement/residual, and viscous collar | closed algebraically | A transported cutoff still moves in Eulerian variables |
| Nominal remainders | \(N=F_t+\nu K^2F\), \(M=C_t+\nu K^2C\) | closed definition | \((\Delta+K^2)\) mismatch is generally leading size |
| Tangent cancellation | \(PM=PC_t\), \(E_t=PM/\rho\) | closed | The nominal radial term does not rotate \(E\) |
| Signed amplitude | \(\beta_t+\lambda\beta=S\) | closed | \(S\) contains complete acceleration and tangent mismatch |
| Normalized correlation | \(z_t+\lambda z=\mathcal J\) | closed | \(Y_t/Y\) remains inside \(\mathcal J\) |
| Positive amplitude | \(a_t+2\lambda a=2z^+\mathcal J\) | closed | Positive-part crossing has no atom, denominator zero faces still do |
| Amplitude-vector identity | \(\|\Xi_t+\lambda\Xi\|^2=\mathbf1_{z>0}\mathcal J^2+a\|PM\|^2/d\) | **PASS**, independently audited | Valid on positive-denominator components and almost everywhere in time |
| Alternative vector identity | \(\|\Xi_t+(\lambda+y/2)\Xi\|^2=\mathbf1_{\beta>0}S^2/Y+a\|PM\|^2/d\) | closed | Must not be confused with the \(\mathcal J\) form |
| Deterministic BV formula | \(\operatorname{TV}(a)+a_-+a_+=2a_-+2\int(a_t)^+\) | closed | Requires nonnegative absolute continuity on each component |
| One-sided BV reduction | \(\operatorname{TV}(a)+a_-+a_+\le2a_-+4\int z^+\mathcal J^+\) | **PASS** | Initial trace and positive joint creation remain |
| Terminal trace | Absorbed by the exact BV identity | closed | This does not absorb the initial trace |
| One chosen smooth initial trace | \(\sum K^{-2}a(T_-)\lesssim\|u(T_-)\|_2Y(T_-)^{1/2}\) | closed at a classical time | Does not pay later denominator entries or a singular-time limit |
| Split enstrophy normalization | \(z^+\mathcal J^+\le z^+(S/\sqrt Y)^++\tfrac12ay^-\) | closed | A split proof must control \(y^-\) independently |
| Direct residual-square closure | Requires schematically \(|\mathcal J|^2\lesssim\nu^2K^2\|x\|^2\) | **STOP** | Generic annular mismatch is \(O(\nu K^2\|x\|)\) |
| Fixed-width annular improvement | Claim \((\Delta+K^2)P_K=O(K)\) | **rejected** | Heat decay gives \(K^2\) dissipation, not this centered residual gain |
| Soft direction | \((E_\varepsilon)_t+\lambda\theta_\varepsilon E_\varepsilon=R_\varepsilon^{-1}P_\varepsilon M\) | closed globally | \(E_\varepsilon\) is not unit |
| Soft scalar damping | \((a_\varepsilon)_t+2\lambda(1+\theta_\varepsilon)a_\varepsilon=2z_\varepsilon^+\mathcal J_\varepsilon\) | **PASS**, independently audited | The extra radial damping has a plus sign on the left |
| Soft zero-face passage | \(L^1\) convergence plus BV lower semicontinuity would retain concentrated faces | conditional | Uniform BV and compactness are not derived |
| Denominator components | Both one-sided traces enter absolute variation | closed deterministic fact | No uniform count or face budget is known |
| Refresh | Nonlinear cell coefficients have explicit jump atoms | closed deterministic fact | Refresh deltas cannot be multiplied inside \(M\) or \(\mathcal J\) |
| Common-heat coefficient | \(a=x(1-x)^2/[2(1+x)]\) | exact | Abstract Hilbert heat pair; \(Y=1\) imposed |
| Common-heat faces | Entry and exit values both vanish | exact | Eliminates a face-only explanation of that example |
| Common-heat weighted ratio | \(\nu(71-17\sqrt{17})K^2/3\) | **rejects heat-volume-only BV control** | Not by itself an NSE \((F,C)\) pair |
| Common-heat joint source | \(\mathcal J/(\nu K^2)>0\), square integral \(3(1-\log2)/4\) | exact | Shows the joint source remains nominal size |
| True 2D3C datum | Fixed energy \(263/90\), global smooth passive-scalar reduction | **PASS**, independently Fourier-audited | Three-dimensional field with 2D3C symmetry, not a generic solution |
| True 2D3C multiplier | Fixed smooth real-even radial two-ring symbol near squared radii 5 and 10 | exact declared component | Not the preselected broad standard single-ring dyadic frame |
| True 2D3C zero entry | \(Y=36K^2/5\), \(\|F\|^2=8K^2\), \(d=8K^4\), \(B=a=0\) | **PASS** | Normalized Haar Parseval convention is fixed |
| Weak-advection limit | \(C^1([0,M];\ell_s^2)\) error \(O(K^{-1})\) | proved by Duhamel for fixed \(M,s,\nu\) | Not uniform on growing viscous windows |
| Interior 2D3C pulse | \(A_0(\log2/10)=2/[3(1+3\,2^{1/5}+2\,2^{4/5})]>0\) | **PASS** | Limit is fixed \(\theta\), \(K\to\infty\), not a finite-\(K\) exact curve |
| True 2D3C weighted variation | At least \(A_*/(2K^2)\) for large \(K\) | closed on the family | Lower bound uses zero entry and uniform \(C^1\) convergence |
| R0.71F heat volume on the pulse | \(O(K^{-4})\) | closed on the family | Physical time and outer \(K^{-2}\) weight are both retained |
| One-sided joint creation on the pulse | \(2\int z^+\mathcal J^+\ge A_*/2\) | closed on the family | Unweighted creation is \(O(1)\); outer-weighted is \(\gtrsim K^{-2}\) |
| Heat-volume control of one-sided creation | Ratio grows at least \(c_\nu K^2\) | **rejected for the declared multiplier** | Does not reject another independent NSE budget or a different fixed frame |
| Full face-paid weighted BV | No family here defeats all entries, faces, refreshes, and frame sums | **open** | Must not be described as disproved |
| Adapted Parseval embedding | A smooth completion is plausible, but no explicit completed frame or total-RHS estimate is released | not used / open | No comparison with the site's preselected broad frame |
| Complementary cutoffs | Aggregate \(a_\delta=U^2/(3\delta^2+4)\) | exact | Separate earlier 2D3C construction |
| One refresh gap | \(3U^2/28\) | exact | \(\delta\) is a shape parameter, not time |
| Uncontrolled repeated refresh | Variation grows with alternation count | **rejected as a free operation** | Fixed or quantitatively transported partitions remain possible |
| Infinite shell--cell sum | No uniform summability theorem for positive joint creation or faces | open | Requires full tight-frame and localization structure |
| Leray-level passage | Standard energy gives neither \(Y_t/Y\) nor the complete source/face budget | open | Regularize first; derive uniform estimates before passing limits |
| Known continuation criteria | Serrin/Besov, occupation, and caloric-defect conditions provide conditional closures | literature boundary | Importing them does not create an unconditional result |
| Literature collision | Bounded primary-source search found close interfaces but no direct theorem for (0.2) | bounded negative finding | Not an originality or nonexistence claim |
| Millennium problem | No global regularity or singularity conclusion | **not reached** | R0.71I is a route-elimination and exact-reduction result |

## Exact stopping rule

The following route is now closed:

\[
 \text{R0.71F heat volume alone}
 \Longrightarrow
 \sum K^{-2}\int z^+\mathcal J^+dt
 \Longrightarrow
 \text{weighted BV}.
 \tag{0.3}
\]

The first implication fails for the declared smooth radial two-ring
component, even on a global-smooth fixed-energy 2D3C family with zero entry,
strict denominator, fixed cutoff, and no refresh.

The following stronger possibility is not closed:

\[
 \text{new all-shell NSE cancellation or budget}
 \Longrightarrow
 \sum K^{-2}\int z^+\mathcal J^+dt
 \Longrightarrow
 \text{weighted BV plus faces}.
 \tag{0.4}
\]

R0.71J should test (0.4) without replacing its first term by a known
continuation norm, occupation hypothesis, denominator lower bound, or the
target BV itself.  If every candidate reduces to one of those inputs, the
temporal-residence branch remains conditional and should stop.
