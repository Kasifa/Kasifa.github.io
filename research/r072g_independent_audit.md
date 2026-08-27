# R0.72G independent line-by-line and finite-model audit

**Date:** 2026-08-27

**Decision:** The analytic complete-root proof closes in the declared exact
one-carrier class.  Two independent binary64 solvers reproduce the same
finite root counts and complete slope masses.  The numerics are
corroboration only; the theorem comes from the real phase gauge,
Rolle--BV sampling, the exact target-row identities, and the R0.72E action
estimate.

## 1. Analytic identities checked independently

Let \(F'=-A_\mu F+\delta VF\), \(F(0)=ie_{-1}\),
\(f=F_0\), \(h=P_0VF\), \(b=P_0V^2F\), and
\(q=\|VF\|_{A_\mu^{-1}}^2\).  I checked the following chain directly.

1. The gauge \(F_r=i^{-r}a_r\) produces
   \[
   a_r'=-(r^2+\mu)a_r+\delta e^{-x}(a_{r-1}-a_{r+1}),
   \]
   so \(f\) and \(h\) are real.
2. The exact target row is \(f'+\mu f=\delta h\).
3. Because \(V'=-V\) and the two input modes of the target row have
   diagonal eigenvalue \(1+\mu\),
   \[
   h'=-(2+\mu)h+\delta b.
   \]
4. The \(r=0\) and \(r=\pm1\) terms of \(q\) give
   \[
   |h|^2\le\mu q,
   \qquad
   |b|^2\le2(1+\mu)q.
   \]
5. For \(\delta>0\), Rolle's theorem applied to
   \(e^{\mu x}f\) gives one zero of \(h\) between any two listed target
   roots.  Integrating \((h^2)'\) from these slope zeros yields
   \[
   \sum|h(x_j)|^2\le2\int|hh'|.
   \]
6. Combining the previous lines gives the complete extended root estimate
   \[
   G_{\rm all}\le1+2[(2+\mu)\mu
   +\delta\sqrt{2\mu(1+\mu)}]Q_0.
   \]

The restriction \(\delta\ge1\) is essential.  At \(\delta=0\), the target
is identically zero while \(h\) need not vanish, so an extended sum over
the continuum of roots would not satisfy the theorem.

## 2. Complete physical ledger checked

The physical conversion uses a half-open root window \([0,T)\) and
continuous integrals on \([0,T]\).  At every target root,
\(f_x=\delta h\).  A nonzero \(h\) makes the root simple and the inherited
target-shell identity makes it a positive right entry; a root with \(h=0\)
has zero atom.  Therefore the conversion applies to all roots, not only to
the Bessel roots selected in advance.

For \(A_\delta=S_\delta^2=O(\delta)\), the active enstrophy is
\(O(A_\delta\delta^{2/3})=O(\delta^{5/3})=o(\delta^2)\).  Hence

\[
 D\asymp\delta^2,
 \qquad \mathcal R_Y\asymp1,
 \qquad \mathscr A_*\asymp A_\delta Q_*.
\]

R0.72E gives \(G_{\rm all}\lesssim\log\delta\), and R0.72F gives
\(Q_*\asymp\delta^{-2/3}\log\delta\).  Thus

\[
 \mathcal J_{\rm all}
 \lesssim A_\delta G_{\rm all}
 \lesssim A_\delta\delta^{2/3}Q_*
 \lesssim D^{1/3}\Lambda_{1,*}.
\]

No power of \(P\), \(q_0\), or \(T\) is missing; \(q_0\) and \(T\) are
fixed and enter the constants.

## 3. Independent numerical routes

The producer uses a real invariant lattice, fourth-order Runge--Kutta,
cubic-Hermite state interpolation, and Brent root refinement.  The
independent program uses a complex Fourier-angle representation, exact heat
half-steps, an exact integral of the time-dependent cosine potential on each
Strang step, and a target-only Hermite derivative for the root slope.
Neither program reads the other program or its output.

On the common grid, the results are:

| \(R\) | \(\delta=R^4\) | roots | producer mass | independent mass | relative gap |
|---:|---:|---:|---:|---:|---:|
| 8 | 4,096 | 443 | 3.62998001 | 3.62998102 | \(2.80\times10^{-7}\) |
| 12 | 20,736 | 1,052 | 4.33745849 | 4.33745992 | \(3.31\times10^{-7}\) |
| 16 | 65,536 | 1,907 | 4.82185658 | 4.82185848 | \(3.93\times10^{-7}\) |
| 24 | 331,776 | 4,351 | 5.49219677 | 5.49220012 | \(6.10\times10^{-7}\) |
| 32 | 1,048,576 | 7,774 | 5.96315629 | 5.96316177 | \(9.18\times10^{-7}\) |

The producer continues to \(R=48,64\), finding complete masses
\(6.62375271\) and \(7.09126866\).  The last four producer values have a
diagnostic linear slope \(0.40754\) against \(\log\delta\), close to
\(4/\pi^2=0.40528\).  This apparent leading constant is not part of the
analytic theorem.

The finite root count grows roughly like \(\sqrt\delta\), while the
slope-weighted mass grows only logarithmically.  At \(R=64\), the first
\(R\) selected roots contain about \(50.28\%\) of the complete mass.  Thus
the extra roots are numerous but their squared slopes are small in total.

## 4. Pressure and failed-attempt record

The passing producer reports relative complete-mass changes of

\[
 7.40\times10^{-7}\quad\text{(step)},\qquad
 4.39\times10^{-8}\quad\text{(largest-}\!R\text{ radius)},\qquad
 1.67\times10^{-8}\quad\text{(horizon tail)}.
\]

The passing independent route reports

\[
 1.67\times10^{-7}\quad\text{(step)},\qquad
 0\quad\text{at printed precision (radius)},\qquad
 1.85\times10^{-8}\quad\text{(horizon tail)}.
\]

Two first attempts are preserved rather than overwritten.

- The first independent run failed an overly tight edge-energy diagnostic
  at \(R=24\), even though direct radius pressure changed the root mass by
  only \(1.2\times10^{-13}\).  The passing rerun increased the main spectral
  radius from \(10R\) to \(12R\).
- The first producer run failed the same kind of indirect edge diagnostic at
  \(R=64\).  The passing protocol added a direct \(10R\)-to-\(14R\) mass
  pressure check at the largest \(R\); this is the quantity relevant to the
  plotted root mass.  The original result and logs remain in the archive.

These changes are explicit in the scripts and certificate package.  They
are not interval bounds.

## 5. Boundary of the audit

Both programs detect resolved sign-changing roots on a finite time window
and a finite spectral lattice.  Tangential roots are not numerically
certified; analytically they have \(h=0\) and contribute zero slope mass.
The calculations do not certify roots below floating-point resolution or
the infinite-lattice truncation error.  They do not prove the R0.72E
Malliavin-density estimate, a multi-carrier trace theorem, a continuation
criterion, singularity formation, or Navier--Stokes regularity.
