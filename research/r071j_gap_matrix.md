# R0.71J gap matrix — all-shell positive creation and the broad parent frame

**Date:** 2026-08-26

**Status:** formal claim-boundary document.  “Rejected” refers only to the
displayed estimate and declared frame/cell class.  It is not a regularity,
singularity, global impossibility, or novelty claim.

**Target inherited from R0.71I.**  For shell/cell coefficients

\[
 a_{j,Q,\varepsilon}
 =\frac{(\langle F_j,C_{j,Q}\rangle^+)^2}
 {Y(\|C_{j,Q}\|_2^2+\varepsilon)},
 \tag{0.1}
\]

the intended endpoint remains a Leray-level estimate, uniform in every
truncation and limiting parameter, for

\[
 \sum_{j,Q}K_j^{-2}\operatorname{TV}_t(a_{j,Q,\varepsilon}).
 \tag{0.2}
\]

| Claim slot | Exact evidence | Status | Boundary retained / next burden |
|---|---|---:|---|
| R0.71I scalar evolution | \(a_t+2\nu\kappa^2a=2z^+\mathcal J\) | inherited, independently audited | Classical positive-denominator components |
| Hard all-shell positive defect | \(2\mathcal Z_+=\partial_t\mathcal A_w+2\nu\sum a+2\mathcal Z_-\) | **PASS** | Finite fixed family between refreshes |
| Only universal telescope | \(\partial_t\mathcal A_w\) | closed | Endpoint difference remains; it is not automatically zero |
| Viscous all-shell defect | \(2\nu\sum a\ge0\) | closed | Strict when amplitude has spacetime mass |
| Negative-source defect | \(2\mathcal Z_-\ge0\) | closed | Negative signed source increases, rather than pays, positive creation |
| Soft all-shell defect | Additional \(2\nu\sum\theta_\varepsilon a_\varepsilon\ge0\) | **PASS** | Fixed \(\varepsilon\); soft-to-hard compactness still separate |
| Hard denominator faces | Piecewise integration retains one-sided endpoints | not paid | Cannot be cancelled by (3.1) |
| Partition refresh | Separate nonlinear BV jump atom | not paid | A delta cannot be multiplied inside \(\mathcal J\) |
| Raw tight-frame numerator | \(\sum_jB_j=\frac12Y_t+\nu\|\Delta u\|_2^2\) at \(s=0,\chi=1\) | closed | Classical enstrophy production, not zero |
| Raw denominator and Lamb norms | \(\sum d_j=\|\Delta u\|_2^2\), \(\sum\|F_j\|_2^2=\|L\|_2^2\) | closed | Linear Parseval only |
| Quotient sandwich | \(((\sum B_j)^+)^2/\sum d_j\le\sum q_j\le\sum\|F_j\|^2\) | closed | Time differentiation does not preserve a useful order |
| Signed shell-transfer antisymmetry | Cancels before positive parts | known interface | \(\tau^++(-\tau)^+=|\tau|\) after pairwise positive parts |
| Amplitude-vector frame sum | Sum of radial and tangent squares | closed | Both rows are nonnegative; no cross-shell negative term |
| Bounded-overlap amplitude | \(\sum_Qa_Q\le N_0\|F_j\|^2/Y\) | closed | Static coefficient only |
| Bounded-overlap radial source | Conditional \(F\)-\(N\)-\(Y_t/Y\) estimate | closed algebraically | Requires acceleration and enstrophy-log budgets |
| Bounded-overlap tangent source | Rotating path gives \(z^+T=1/(2\delta)\) with overlap one and bounded \(F,C_t\) | geometry-only **no-go** | Not an NSE path; shows \(\rho^{-1}\)/angular speed is independent |
| Existing frame | R0.71E §10.1 smooth flat-top parent-only frame | fixed before R0.71J data | Does not automatically cover §10.2 low/high child refinement |
| Parent support | \(m=1\) on log interval \([0,1/2]\), support in \([-1/2,1]\) | exact declaration | Scale is \(\kappa=4K\) in the witness |
| Weighted frame multiplier | \(\sum_j2^{-2j}m_j(\xi)^2\le4|\xi|^{-2}\) | **PASS** | Uses parent support and tightness |
| True 2D3C datum | 14-mode real divergence-free datum; shear plus passive advection--diffusion | **PASS** | Global smooth symmetry class |
| Fixed energy | \(\|u_0\|_2^2=2041/200\) | **PASS** | Independent of dyadic \(K\) |
| Exact enstrophy | \(Y(0)=178K^2\) | **PASS** | Normalized-Haar Parseval convention |
| Exact parent Lamb norm | \(\|F_\kappa(0)\|_2^2=500K^2\) | **PASS** | Parent is one on all listed Lamb modes |
| Exact parent denominator | \(d_\kappa(0)=3942K^4>0\) | **PASS** | Strict at entry and on the fixed limiting window for large \(K\) |
| Exact zero entry | \(B_\kappa(0)=a_\kappa(0)=0\) | **PASS** | Not a denominator-zero face |
| Channel cancellation | \(B_{n=4}=4K^3\), \(B_{n=5}=-4K^3\) | **PASS** | Independently resolved by horizontal Fourier index |
| Weak-advection parameter | \(1/(\nu K)\) in the sideband system | exact | Fixed \(\nu>0\), fixed \(\theta\)-window |
| Fixed-window convergence | \(C^1([0,M];\ell_s^2)\) error \(O(K^{-1})\) | proved by Duhamel | Limiting curve is not exact at finite \(K\) |
| Limiting parent numerator | \(B_0=4(e^{-34\theta}-e^{-52\theta})\) | **PASS** | Positive for \(\theta>0\) |
| Limiting parent amplitude | \(A_0=16(e^{-34\theta}-e^{-52\theta})^2/(D_0Y_0)\) | **PASS** | Strictly positive for \(\theta>0\) |
| Certified observation time | \(\theta_*=(\log2)/18\) | exact | Physical window length is \(\theta_*/(\nu K^2)\) |
| Certified interior value | \(A_*\approx1.19655\times10^{-5}\) | **PASS** | Small but fixed and positive |
| Parent positive creation | At least \(A_*/(64K^2)\) after outer \((4K)^{-2}\) weight | closed for large dyadic \(K\) | Uses zero entry and fixed-window convergence |
| Exact 2D3C Lamb structure | \(L=(0,0,-V\partial_2w)\) | closed | Gives \(\|L\|^2/Y\le4e^{-2\theta}\) |
| Vertical spectral gap | All Lamb modes retain \(|\xi_2|=4K\) or \(5K\) | closed | Advection changes horizontal sideband only |
| Complete-frame heat endpoint | At most \((1-2^{-1/9})/(2\nu K^4)\) | **PASS** | Sum includes every broad parent |
| Complete-frame creation/heat ratio | At least \(\nu A_*K^2/[32(1-2^{-1/9})]\) | **PASS** | Diverges as \(K^2\) |
| Full-frame heat payment | Uniform \(\mathcal Z^{\rm frame}\le C\mathcal H^{\rm frame}\) | **rejected** for the R0.71E parent-only frame and global cell | Does not reject a different NSE budget |
| Cross-shell algebraic cancellation | Automatic payment after shellwise positive parts | **rejected** | The exact positive-defect identity gives the obstruction |
| Broad parent versus child refinement | Nonlinear quotient reconstruction from parent to children | not valid | Must be checked separately if needed |
| Matched spatial cells | No matched partition is used; \(\chi=1\) | open | R0.71K finite gate |
| Movement/collar rows | Vanish for the global fixed cell | not tested in a matched partition | Must remain in the localized ledger |
| Denominator/refresh faces | No full budget is obtained | open | Cannot be inferred from the interior theorem |
| Infinite frame--cell soft limit | No uniform compactness theorem | open | Requires all faces and summability |
| Different Leray-controlled budget | Not excluded | open | Must not be a disguised continuation hypothesis or target BV |
| Literature collision | Smooth band telescoping, Germano identities, LP commutators, and conditional heat tents are known | bounded audit complete | Exact normalized positive-defect/full-frame witness not found; no novelty claim |
| Full face-paid weighted BV | No estimate or counterexample covering all rows | **open** | R0.71J closes only the frequency-frame heat/cancellation escape |
| Millennium problem | No regularity or singularity conclusion | **not reached** | Route-elimination and structural reduction only |

## Exact stopping rule

The following frequency-only route is closed:

\[
 \text{tight-frame signed telescope or the same full-frame heat endpoint}
 \Longrightarrow
 \sum_jK_j^{-2}\int z_j^+\mathcal J_j^+dt.
 \tag{0.3}
\]

The first proposed input becomes (3.1) after positive parts and leaves
nonnegative defects.  The second is separated from the target by a certified
\(K^2\) factor on a fixed-energy global-smooth NSE family inside the existing
broad parent frame.

The next unresolved interface is genuinely spatial:

\[
 \text{fixed matched cell partition with complete collars/faces}
 \stackrel{?}{\Longrightarrow}
 \text{new coercive payment or the same }K^2\text{ gap}.
 \tag{0.4}
\]

R0.71K should test (0.4) without treating localization motion, denominator
faces, or refresh atoms as free operations.
