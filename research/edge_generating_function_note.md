# R0.27 scalar edge equations and endpoint asymptotics audit

## Status

R0.26 showed that

\[
 b_N=(-N+1,-3N+1,-3N+1)
\]

is an exact two-generator coefficient on the edge spanned by

\[
 P_-=(-1,-1,-1),\qquad C_+=(1,-1,-1).
\]

This note reduces that edge recurrence from four-vector Leray operations to
two scalar coefficient arrays.  It then packages the scalar recurrences as a
pair of bivariate generating equations and evaluates the endpoint through
\(N=75\), or 225 leaves.

The coordinate reduction and the generating equations are exact formal-power-
series identities.  The endpoint table is a dual-precision MPFR computation.
It gives strong evidence for alternating convergence
\(|\sigma_{B,N}|\to1\), but it does not prove that limit or locate a dominant
complex singularity.  No conclusion about global regularity or finite-time
singularity of three-dimensional Navier--Stokes is claimed.

## Edge coordinates

Use \(n\) pump leaves and \(k\) catalyst leaves.  Define

\[
 L=n+k,\qquad Q=2k-n=3k-L,\qquad \chi=Q/6.
\]

Their label and offset are

\[
 m=(k-n,-L,-L),\qquad
 \beta=\frac L3(-1,-1,2).
\]

The unit vector

\[
 h=\frac1{\sqrt2}(1,-1,0)
\]

is orthogonal to every offset on this edge.  Every generated coefficient can
therefore be written uniquely as

\[
 w=s h+\frac{3\chi\alpha}{\sqrt2}\frac{(-1,-1,2)}3,
 \qquad \ell=-\sqrt2L\alpha.
\tag{2.1}
\]

Thus the complete four-component coefficient is encoded by an in-plane
amplitude \(\alpha_{n,k}\) and a sharp amplitude \(s_{n,k}\).  The endpoint is

\[
 b_N:\qquad (n,k,L,Q)=(2N-1,N,3N-1,1).
\tag{2.2}
\]

## Exact scalar recurrence

For a root split \((n,k)=(n_1,k_1)+(n_2,k_2)\), set

\[
 D=\frac{n_1k_2-k_1n_2}{2}
   =\frac{L_1k_2-k_1L_2}{2}.
\]

Substitution of (2.1) into the ordered Navier--Stokes bilinear map gives the
sharp contribution \(-\sqrt2D\alpha_1s_2\).  The Taylor recurrence therefore
closes as

\[
 (L-1)s_{n,k}
 =\frac1{\sqrt2}
 \sum (n_1k_2-k_1n_2)\alpha_{n_1,k_1}s_{n_2,k_2}.
\tag{3.1}
\]

For nonzero output charge \(Q\), the in-plane recurrence is

\[
 (L-1)\alpha_{n,k}
 =\frac{\sqrt2}{2Q}
 \sum (n_1k_2-k_1n_2)Q_2
 \alpha_{n_1,k_1}\alpha_{n_2,k_2}.
\tag{3.2}
\]

The charge-zero slice is not obtained by putting \(Q=0\) in (3.2).  Direct
projection gives instead

\[
 (L-1)\alpha_{n,k}
 =\frac{\sqrt2}{2L}
 \sum (n_1k_2-k_1n_2)L_2
 \alpha_{n_1,k_1}\alpha_{n_2,k_2},
 \qquad Q=0.
\tag{3.3}
\]

Equations (3.1)--(3.3) reproduce every R0.26 \(b_N\) endpoint value through
\(N=25\).  They are an exact scalarization, not a numerical model reduction.

## Generating equations

Let

\[
 A(z,w)=\sum_{n,k\geq0}\alpha_{n,k}z^nw^k,
 \qquad
 S(z,w)=\sum_{n,k\geq0}s_{n,k}z^nw^k,
\]

and introduce the Euler operators

\[
 X=z\partial_z,\quad Y=w\partial_w,\quad
 \mathcal L=X+Y,\quad \mathcal Q=2Y-X,
\]

with bracket

\[
 \{F,G\}=(XF)(YG)-(YF)(XG).
\]

If \(\Pi_0\) denotes projection onto the charge-zero monomials, the complete
coefficient recurrences are equivalent to

\[
 (\mathcal L-1)A
 =\frac1{\sqrt2}\left[
 (I-\Pi_0)\mathcal Q^{-1}\{A,\mathcal QA\}
 +\Pi_0\mathcal L^{-1}\{A,\mathcal LA\}
 \right],
\tag{4.1}
\]

\[
 (\mathcal L-1)S=\frac1{\sqrt2}\{A,S\}.
\tag{4.2}
\]

The initial terms are

\[
 A_1=-6\sqrt2z+3\sqrt2t w,
 \qquad
 S_1=\frac p{\sqrt2}z-\sqrt2qtw,
\tag{4.3}
\]

where \(p,q\) are the R0.20 root parameters and
\(t=0.4958758920134925\ldots\) is the quadratic generator.

The projector in (4.1) is essential.  The recurrence crosses the resonant
line \(Q=0\) at every third leaf order, and that line obeys (3.3), not a
removable instance of (3.2).

## Charge-adapted variables

Set

\[
 r=z^2w,\qquad \xi=z^{-1}.
\]

Then

\[
 z^nw^k=r^k\xi^Q,qquad
 \mathcal L=3r\partial_r-\xi\partial_\xi,qquad
 \mathcal Q=\xi\partial_\xi,
\]

and

\[
 \{F,G\}=(rF_r)(\xi G_\xi)-(\xi F_\xi)(rG_r).
\tag{5.1}
\]

The endpoint problem becomes the fixed-charge coefficient extraction

\[
 b_N=[r^N\xi^1](A,S).
\tag{5.2}
\]

This is the useful change of viewpoint supplied by R0.27: the endpoint is no
longer a drifting ray in \((n,k)\), but a fixed Laurent charge observed at
successive powers of \(r\).  The price is the nonlocal charge-zero projector
in (4.1).

## Dual-precision endpoint window

For (2.1), the mode norm used in R0.25--R0.26 becomes

\[
 M_{L,Q}(\alpha,s)
 =\sqrt{s^2+3\chi^2\alpha^2}+\sqrt2L|\alpha|,
 \qquad
 \sigma_{B,N}=\frac{s_{2N-1,N}}{M_{3N-1,1}}.
\tag{6.1}
\]

The recurrence was evaluated at 160 and 224 MPFR bits through \(N=75\).
The maximum relative discrepancy among every recorded \(\sigma_{B,N}\) and
\(s/(L\alpha)\) was

\[
 3.21\times10^{-43}.
\]

Selected 224-bit values are:

| \(N\) | \(\sigma_{B,N}\) | \(N|\sigma_{B,N}|\) | \(s/(L\alpha)\) |
|---:|---:|---:|---:|
| 25 | \(-0.162926737\) | 4.07317 | 0.275266 |
| 35 | \(-0.565151479\) | 19.7803 | 1.83799 |
| 45 | \(-0.903274817\) | 40.6474 | 13.2067 |
| 55 | \(-0.986080822\) | 54.2344 | 100.188 |
| 65 | \(-0.998211707\) | 64.8838 | 789.403 |
| 70 | \(+0.999369048\) | 69.9558 | \(-2239.98\) |
| 71 | \(-0.999488154\) | 70.9637 | 2761.55 |
| 72 | \(+0.999584883\) | 71.9701 | \(-3405.37\) |
| 73 | \(-0.999663412\) | 72.9754 | 4200.21 |
| 74 | \(+0.999727151\) | 73.9798 | \(-5181.72\) |
| 75 | \(-0.999778869\) | 74.9834 | 6393.94 |

The sign agrees with \((-1)^N\) for every \(8\leq N\leq75\).  The first
indices at which \(|\sigma_{B,N}|\) exceeds \(0.5,0.9,0.99,0.999\) are
\(34,45,57,68\), respectively.  On the last twenty points, a descriptive
log-linear fit gives a factor \(1.2312\) per unit \(N\) for
\(|s/(L\alpha)|\), while the defect \(1-|\sigma|\) has fitted factor
\(0.8126\).  These fitted numbers summarize the finite window; they are not
certified asymptotic constants.

## What this changes

R0.25 proved a conditional sufficient route: if both endpoint sharp
coordinates are \(O(N^{-1})\), the dangerous generated gain is uniformly
bounded.  The present \(b_N\) window exhibits the opposite behavior:
\(N|\sigma_{B,N}|\) is already \(74.9834\) at \(N=75\), and
\(|\sigma_{B,N}|\) is close to one rather than zero.

This does not logically disprove an asymptotic \(O(N^{-1})\) bound, because a
finite sequence never determines its tail.  It does remove the numerical
support for that bound and gives a precise theorem target:

\[
 \liminf_{N\to\infty}|\sigma_{B,N}|>0
 \quad\text{or, more strongly,}\quad
 |\sigma_{B,N}|\longrightarrow1.
\tag{7.1}
\]

Proving either statement for this datum would close the R0.25 one-radius
small-polarization route negatively.  It would not prove blow-up; it would
identify a failed sufficient mechanism and prevent further work from relying
on it.

## Next theorem target

R0.28 should convert the finite pattern into a rigorous coefficient statement.
The first tasks are:

1. factor out the known leaf monomials and rewrite (3.1)--(3.3) as exact
   rational recurrences, eliminating MPFR cancellation from the sign problem;
2. prove an eventual sign pattern after the \((-1)^N\) twist, or produce a
   validated interval counterexample;
3. derive certified upper and lower bounds for the consecutive growth ratios
   of the charge-one \(A\) and \(S\) coefficients;
4. identify the relevant singularities in the \(r\)-plane, including the
   coupling through the charge-zero slice, and justify coefficient transfer;
5. only then decide whether the limiting sharp ratio in (7.1) is a theorem.

Classical univariate singularity analysis and analytic combinatorics in several
variables supply useful coefficient-transfer tools, but equations (4.1)--(4.2)
are not yet in a form to which an off-the-shelf transfer theorem applies.  The
charge-zero projector and the nonlinear formal PDE must be handled first.

The exact audit is implemented in
`research/edge_generating_function_audit.py`; the public certificate records
the dual-precision run, its environment, and the complete endpoint table.
