# R0.72G claim--evidence matrix

**Date:** 2026-08-27

| ID | Claim | Evidence | Status | Boundary |
|---|---|---|---|---|
| G1 | The exact one-carrier target and coupling slope are real. | Gauge \(F_r=i^{-r}a_r\) turns the lattice into the real system (1.4). | proved | Uses seed \(ie_{-1}\) and one real carrier. |
| G2 | \(f'+\mu f=\delta h\) and \(h'=-(2+\mu)h+\delta b\). | Exact target-row differentiation, \(V'=-V\), and the \(r=\pm1\) diagonal eigenvalue. | proved | Fixed one-carrier lattice only. |
| G3 | \(|h|^2\le\mu q\) and \(|b|^2\le2(1+\mu)q\). | The \(r=0\) and \(r=\pm1\) summands of \(q=\|VF\|_{A_\mu^{-1}}^2\). | proved | Constant depends on fixed \(q_0\). |
| G4 | Every finite positive root subset obeys \(\sum|h(x_j)|^2\le2\int|hh'|\). | Apply Rolle to \(e^{\mu x}f\) between consecutive listed roots; integrate \((h^2)'\) from the resulting slope zero. | proved | Needs the real target gauge. No root-separation assumption. |
| G5 | The complete extended root mass obeys (0.5). | G2--G4 and monotone supremum over finite root subsets; launch contributes \(h(0)^2=1\). | proved | Multiple roots contribute zero. |
| G6 | \(G_{\rm all}(\delta;X)=O(\log(2+\delta))\). | G5 plus the R0.72E analytic action estimate \(Q_0\le C(1+\log(2+\delta))/\delta\). | proved | Fixed \(X,q_0\); not uniform as \(q_0\to\infty\). |
| G7 | Along \(\delta_R=R^4\), \(G_{\rm all}\asymp\log\delta_R\). | G6 upper bound and the R0.72E selected Bessel lower mass. | proved | Order only; no leading constant for all roots. |
| G8 | The critical-log candidate holds for the exact one-carrier physical family with \(A_\delta\le C_A\delta\). | G6, the derived bridge \(G_{\rm all}\lesssim\delta^{2/3}Q_*\), the R0.72F two-sided \(Q_*\) law, exact enstrophy and projected-Lamb identities, and the shear floor. | proved | Not the general triangular class. |
| G9 | The original R0.72E amplitude sequence sharply saturates the complete-root payment. | \(A_R\asymp\delta_R/\log\delta_R\), G7, \(Q_*\asymp\delta_R^{-2/3}\log\delta_R\), and \(D_R\asymp\delta_R^2\). | proved | Sharp in order, not in optimal constant. |
| G10 | Binary64 producer and independent routes agree on finite complete-root mass and its logarithmic trend. | Archived JSON, tolerance/mode pressure, progress logs, resource logs, and checksums. | corroborated | Not interval arithmetic and not a proof. |
| G11 | No hidden super-logarithmic root-slope mass exists in the exact one-carrier sequence. | G6--G7. | proved | Says nothing about growing carrier number or complex targets. |
| G12 | The critical-log estimate holds for arbitrary three-dimensional NSE solutions. | No evidence. | open | Would require a portable trace/restart theorem and a continuation bridge. |
| G13 | R0.72G solves the Navier--Stokes Millennium problem. | No evidence. | false | Every constructed member is globally smooth and belongs to a special invariant class. |

## Publication decision

R0.72G may be described as a complete-root theorem and a sharpness theorem
only for the declared exact one-carrier family.  It must not be described as
a general triangular estimate, a continuation criterion, or progress that
resolves a fixed percentage of the Millennium problem.
