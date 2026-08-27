# R0.72R independent analytic audit

**Date:** 2026-08-28

**Status:** PASS for the declared compact polydisc, the two-critical-point
theorem for every \(y\ge0\), physical shape constants on \(0\le y\le1\), the
slow-time ledger, and exact incidence formulas.  The fixed-pattern
enhanced-dissipation corollary uses the same physical cell.  The complete
four-dimensional caustic decomposition is not part of this audit.

## 1. Coefficient domain and cone exit

For

\[
 |z_2-3/20|\le1/100,qquad |z_3|\le1/1000,
\]

the reverse triangle inequality gives \(|z_2|\ge7/50\).  Hence

\[
 4|z_2|+9|z_3|\ge14/25=1/2+3/50.
\]

The set has nonempty interior in \(\mathbb R^4\).  It is a compact core
outside R0.72Q's sufficient \(Q_2\)-cone, not a claim that the first Fourier
amplitude is smaller than a higher harmonic.

Along the normalized heat path,

\[
 Q_2(y)=4|z_2|e^{-3y}+9|z_3|e^{-8y}
\]

is strictly decreasing because \(|z_2|>0\).  Since \(e>2\),

\[
 Q_2(1)<\frac{2}{25}+\frac9{256000}
 =\frac{20489}{256000}<\frac12.
\]

Every path therefore crosses the old sufficient boundary exactly once.

## 2. Perturbation route

Write

\[
 F_y^0=\cos\phi+\frac3{20}e^{-3y}\cos2\phi,
\]

and put the remaining complex coefficients into \(h_y\).  Direct harmonic
budgets give

\[
 \|h_y'\|_\infty\le23/1000,
 \quad \|h_y''\|_\infty\le49/1000,
 \quad \|h_y'''\|_\infty\le107/1000.
\]

The center derivative is

\[
 (F_y^0)'=-\sin\phi\left(1+\frac35e^{-3y}\cos\phi\right),
\]

whose parenthesis is at least \(2/5\).

For \(\ell=\pi/48\),

\[
 \sin\ell>1535/24576>23/400,
\]

and the boundary-sign margin is exactly

\[
 \frac25\frac{1535}{24576}-\frac{23}{1000}
 =\frac{3047}{1536000}>0.
\]

At a zero of \(F_y'\), \(|\sin\phi|\le23/400\), so all zeros lie in the
two \(\ell\)-boxes.  The second derivative is strictly negative in the
\(0\)-box and strictly positive in the \(\pi\)-box, with conservative
magnitudes \(4/5\) and \(1/5\), respectively.  Boundary signs plus strict
monotonicity give exactly one zero in each box and no others.

## 3. Shape constants

Within distance \(\ell\) of either critical point, the point remains within
\(\pi/24\) of \(0\) or \(\pi\).  The worst normalized curvature is larger
than \(1/4\).  The exact rational slack used at the weaker side is

\[
 1/3-49/1000-1/4=103/3000.
\]

The global upper curvature bound is \(1649/1000<5/3\), with slack
\(53/3000\).  Integration gives

\[
 \frac14d(\phi,c_j)<|F_y'(\phi)|<\frac53d(\phi,c_j).
\]

Outside the critical tubes, the monotonicity-box lower bound is
\(\pi/240>1/80\); outside the larger boxes the direct lower bound is
\(177/1000\).  Therefore the normalized away gap is larger than \(1/80\).

Multiplication by \(e^{-y}>1/3\) on \(0\le y\le1\) gives local slope lower
\(1/12\), physical away gap \(1/240\), and upper slope below \(4/3\).
Thus \((r,C_0,C_1)=(\pi/48,144,240)\) is valid.

## 4. Derivative and slow-time ledger

The four spatial suprema are bounded by

\[
 \frac{1161}{1000},\quad\frac{1323}{1000},\quad
 \frac{1649}{1000},\quad\frac{2307}{1000}.
\]

Their sum is \(161/25\).  The mixed derivative is below
\(2307/1000<7/3\).  Hence

\[
 \frac73\eta\le\eta^{3/4}
\]

whenever \(\eta\le(3/7)^4=81/2401\).  This is only the slow-time condition;
the complete smallness threshold must still include the Coble--He proof
threshold.

## 5. Incidence and real slice

Solving \(f'=f''=0\) after writing \(z_3e^{3i\phi}=A+iB\) reproduces the
two formulas in the report.  Substitution makes both jets identically zero.
The third and fourth jets reduce to

\[
 f'''=15B-3\sin\phi,
 \qquad f''''=45A-3\cos\phi.
\]

For real \(a,b\), symbolic coefficient elimination independently gives

\[
 \operatorname{Disc}_uD
 =-64(4a-9b-1)^3(4a+9b+1)^3
 (a^2+9b^2-3b)^2.
\]

The quadratic factor corresponds to a real unit-circle double root only
when its root in \(x=\cos\phi\) lies in \((-1,1)\).  This restricts the
internal arc to \(1/15<b\le1/3\); including the two contacts with the
endpoint walls gives the closed interval \([1/15,1/3]\).  The lower algebraic
arc is not a real unit-circle wall.

## 6. Claim boundary

The audit does not certify a complete chamber decomposition, an optimal
polydisc, a caustic-crossing theorem, arbitrary time-dependent phases,
growing carrier uniformity, or three-dimensional Navier--Stokes regularity.
The finite machine certificate planned for release audits only the exact
algebraic ledger; the continuum proof remains the analytic argument above.
