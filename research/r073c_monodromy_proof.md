# R0.73C proof: a positive frozen Rayleigh eigenvalue by certified monodromy trace

**Date:** 2026-08-30  
**Claim:** C4 for \(\gamma=1/2\)  
**Evidence class:** exact ODE lemmas plus validated interval endpoint signs

## Theorem

Let

\[
 W(x)=-\frac12\sin x+\frac14\sin2x,
 \qquad
 A_{1/2}=-\frac i2\left(W+W''L_{1/4}^{-1}\right)
\]

on \(L^2(\mathbb T_{2\pi})\), where
\(L_{1/4}=-\partial_x^2+1/4\).  There exists

\[
 \sigma_*\in(0.17035,0.17050)
\]

such that \(\sigma_*\in\sigma_p(A_{1/2})\).

## Proof

### 1. Rayleigh equivalence

For \(q=L_{1/4}\phi\), the equation
\(A_{1/2}q=\sigma q\) is equivalent, with
\(\sigma=-ic/2\), to

\[
 (W-c)(\phi''-\tfrac14\phi)-W''\phi=0.
\]

Take \(c=i\eta\), \(\eta>0\).  Then

\[
 \phi''=Q_\eta(x)\phi,
 \qquad
 Q_\eta=\frac14+\frac{W''}{W-i\eta},
\]

and the associated time eigenvalue is \(\sigma=\eta/2>0\).

### 2. Exact periodic criterion

Let \(Y_\eta(0)=I\) be the two-by-two fundamental matrix and
\(M(\eta)=Y_\eta(2\pi)\).  The first-order coefficient matrix has zero
trace, so Liouville's formula gives \(\det M=1\).

Because \(W(2\pi-x)=-W(x)\) and
\(W''(2\pi-x)=-W''(x)\), one has
\(Q_\eta(2\pi-x)=\overline{Q_\eta(x)}\).  Reflection/conjugation with
\(S=\operatorname{diag}(1,-1)\) gives

\[
 M^{-1}=S\overline M S.
\]

For a determinant-one two-by-two matrix,
\(\operatorname{tr}M^{-1}=\operatorname{tr}M\); hence
\(\operatorname{tr}M\) is real.  Finally,

\[
 \det(M-I)=2-\operatorname{tr}M.
\]

Thus there is a nonzero periodic solution if and only if

\[
 F(\eta):=\operatorname{tr}M(\eta)-2=0.
\]

The coefficient \(Q_\eta\) is smooth for \(\eta>0\), so \(F\) is
continuous.

### 3. Certified endpoint signs

The source `research/r073c_interval_monodromy.py` rewrites the equation and
both fundamental columns as a twelve-dimensional real autonomous system.  On
each step it verifies a Picard tube

\[
 X+[0,h][f](Z)\subseteq Z
\]

and uses a normalized Taylor polynomial with the order-\(p\) derivative
evaluated on the whole tube as an interval Lagrange remainder.  Its arithmetic
uses only directed interval addition, subtraction, multiplication, division,
integer powers, and an outward enclosure of \(\pi\).

The formal certificate and the independently implemented Decimal arithmetic
validator prove

\[
 F(0.3407)<0,
 \qquad F(0.3410)>0.
\]

The intermediate value theorem supplies
\(\eta_*\in(0.3407,0.3410)\) with \(F(\eta_*)=0\).  The periodic solution is
nonzero.  Also \(q=L_{1/4}\phi\ne0\), since the positive operator
\(L_{1/4}\) has trivial kernel.  Therefore

\[
 A_{1/2}q=\frac{\eta_*}{2}q,
 \qquad
 \frac{\eta_*}{2}\in(0.17035,0.17050),
\]

which proves the theorem. \(\square\)

## Boundary

The proof establishes existence, not root uniqueness or algebraic simplicity.
It does not prove viscous eigenvalue persistence, logarithmic fast-time
transfer, a complete OS--Squire direct sum, a nonlinear Navier--Stokes
estimate, or the Clay problem.
