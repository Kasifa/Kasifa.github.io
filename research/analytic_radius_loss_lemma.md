# R0.22 analytic-radius loss lemma

## Status

This note closes the full-space analytic-weight question left open in R0.21.
For the Euclidean/longitudinal mode norm introduced there, the cone-frequency
bilinear operator loses at most two powers of analytic radius.  An explicit
family attains this order, so an exponent smaller than two is impossible in
this norm scale.

This is a negative result about one proof method.  It does not show that the
selected Taylor coefficient family has a divergent tail, and it does not
exclude cancellations after tree aggregation or a stronger invariant norm.

## Cone lattice and mode norm

In the transformed-cube coordinates of R0.21, the additive frequency lattice
is

\[
 \Lambda=\{m\in\mathbb Z^3:m_1\equiv m_2\equiv m_3\pmod 2\}.
\]

Put

\[
 r(m)=\|m\|_\infty,
 \qquad q(m)=\frac{3m_1-m_3}{12},
\]

and

\[
 \beta(m)=\left(
 \frac{m_3}{3},
 \frac{3m_2-m_3}{6},
 -\frac{3m_2+m_3}{6}
 \right).
\]

Then

\[
 |q(m)|\le \frac{r(m)}3,
 \qquad |\beta(m)|^2=\frac{m_2^2+m_3^2}{2}\le r(m)^2.
\]

Because the coordinates have equal parity, every nonzero charge satisfies
\(|q(m)|\ge1/6\).  For a vector \(v_m\) that is divergence-free at

\[
 K_\delta(m)=\delta^{-1}q(m)(1,1,1)+\beta(m),
\]

use the mode norm

\[
 \mathcal N_\delta(v_m)
 =|v_m|+L_\delta(v_m),
 \qquad
 L_\delta(v_m)=\delta^{-1}|(1,1,1)\cdot v_m|.
\]

## Two-radius upper bound

For one ordered interaction with \(m=a+b\), R0.21 gives

\[
 |K_\delta(b)\cdot u_a|
 \le |\beta(b)|\,|u_a|+|q(b)|L_\delta(u_a)
 \le r(b)\mathcal N_\delta(u_a).
\tag{2.1}
\]

The Euclidean component of the Leray output is therefore at most

\[
 r(b)\mathcal N_\delta(u_a)\mathcal N_\delta(v_b).
\]

If \(q(m)=0\), the same bound holds for the complete mode norm.  If
\(q(m)\ne0\), output incompressibility and the charge gap give

\[
 L_\delta(P_{K_\delta(m)}z)
 \le\frac{|\beta(m)|}{|q(m)|}|P_{K_\delta(m)}z|
 \le6r(m)|z|.
\]

Thus in both cases

\[
 \boxed{
 \mathcal N_\delta(\mathcal B_m(u_a,v_b))
 \le(1+6r(m))r(b)
 \mathcal N_\delta(u_a)\mathcal N_\delta(v_b).}
\tag{2.2}
\]

Define the analytic sequence norm

\[
 \|u\|_{\rho,\delta}
 =\sum_{m\in\Lambda\setminus\{0\}}
 e^{\rho r(m)}\mathcal N_\delta(u_m).
\]

For \(0<\eta\le\rho\), use
\(r(a+b)\le r(a)+r(b)=S\) in (2.2).  The remaining multiplier is bounded by

\[
 (S+6S^2)e^{-\eta S}
 \le\frac1{e\eta}+\frac{24}{e^2\eta^2}.
\]

Consequently

\[
 \boxed{
 \|\mathcal B(u,v)\|_{\rho-\eta,\delta}
 \le\left(\frac1{e\eta}+\frac{24}{e^2\eta^2}\right)
 \|u\|_{\rho,\delta}\|v\|_{\rho,\delta}.}
\tag{2.3}
\]

The constant is independent of the shell parameter \(\delta=4^{-n}\).

## A sharp family

For each integer \(N\ge2\), take

\[
 a_N=(N,-3N,3N-2),
 \qquad
 b_N=(-N+1,-3N+1,-3N+1).
\]

Both labels belong to \(\Lambda\), and

\[
 a_N+b_N=(1,-6N+1,-1).
\]

Their charges are \(1/6,1/6,1/3\), while their radii satisfy the exact
additivity relation

\[
 r(a_N+b_N)=6N-1=r(a_N)+r(b_N).
\tag{3.1}
\]

Let \(d=(1,1,1)\) and choose

\[
 w_A=\frac{d\times\beta(a_N)}{|d\times\beta(a_N)|},
 \qquad
 w_B=\frac{d\times\beta(b_N)}{|d\times\beta(b_N)|}.
\]

Each vector is perpendicular to both \(d\) and its own offset.  It is
therefore exactly divergence-free for every \(\delta\), with

\[
 \mathcal N_\delta(w_A)=\mathcal N_\delta(w_B)=1.
\]

Direct rational algebra gives

\[
 d\times\beta(a_N)=(3N,-1,-3N+1),
\]

\[
 d\times\beta(b_N)=(3N-1,-3N+1,0),
\]

and

\[
 \beta(b_N)\cdot(d\times\beta(a_N))=-(3N-1)^2.
\tag{3.2}
\]

Take \(\delta_N=4^{-N}\).  Since
\(\delta_N|\beta(a_N+b_N)|\to0\), the output Leray projection tends to the
projection onto \(d^\perp\).  Equations (3.1)--(3.2) yield

\[
 \lim_{N\to\infty}
 \frac{\mathcal N_{\delta_N}
 (\mathcal B(w_A,w_B))}{N^2}
 =\frac{27}{2}.
\tag{3.3}
\]

For the symmetrized quadratic pair,

\[
 \lim_{N\to\infty}
 \frac{\mathcal N_{\delta_N}
 (\mathcal B(w_A,w_B)+\mathcal B(w_B,w_A))}{N^2}
 =27.
\tag{3.4}
\]

There is no exponential-weight slack in this example because of (3.1).
Choosing \(N\) proportional to \(\eta^{-1}\) shows that an estimate of the
form

\[
 \|\mathcal B(u,v)\|_{\rho-\eta,\delta}
 \le C\eta^{-p}\|u\|_{\rho,\delta}\|v\|_{\rho,\delta}
\]

cannot hold uniformly for any \(p<2\).  The radius-loss order in (2.3) is
therefore sharp.

## Why the heat multiplier does not repair this family

In dimensionless time the heat rate is

\[
 3q(m)^2+\delta^2|\beta(m)|^2.
\]

Along \(\delta_N=4^{-N}\), the transverse terms tend to zero.  The two input
rates tend to \(1/12\), and the output rate tends to \(1/3\).  They do not
grow like \(N^2\), so the dimensionless heat semigroup cannot uniformly pay
for the sharp two-label factor on this family.

## Consequence for the proof plan

The full-space Euclidean/longitudinal analytic norm is now classified: it is
shell-uniform but has a sharp two-radius loss.  A standard one-derivative
Cauchy--Kowalevski majorant cannot close in this space.

The next test must use more structure than a black-box bilinear norm:

1. determine whether the Taylor coefficient subspace generated by the eight
   selected initial modes contains the sharp polarization family;
2. check cancellation after both ordered interactions and all tree histories
   are aggregated with their actual coefficients;
3. if the sharp family survives, replace the present cascade route by a
   precise obstruction statement rather than accumulating higher Taylor
   orders.
