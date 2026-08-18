# R0.26 edge reduction and three-leaf transfer audit

## Status

R0.25 proved that the sharp-label gain is uniformly bounded if the normalized
sharp coordinates of the two generated inputs satisfy

\[
 |\sigma_{a_N}|+|\sigma_{b_N}|=O(N^{-1}).
\]

The first four values, \(N=2,\ldots,5\), were consistent with that condition.
This note derives a smaller exact recurrence for the two endpoint families and
tests the proposed three-leaf induction through \(N=25\).

The structural reduction is exact for every \(N\).  The transfer matrices and
their limits are algebraic consequences of the one-leaf attachment formula.
The endpoint table through \(N=25\) is a two-precision MPFR computation, not
an asymptotic theorem.

The result changes the assessment of the route.  The isolated three-leaf
transfer is expansive, not contractive, and the early small values of
\(N|\sigma|\) do not persist in the larger finite window.  The sufficient
condition from R0.25 remains correct, but the present datum no longer supplies
persuasive numerical evidence for proving it by a small-constant induction.

## Leaf-count coordinates

On the boundary face use the four generators

\[
\begin{aligned}
 P_+&=(1,-1,1), & C_+&=(1,-1,-1),\\
 P_-&=(-1,-1,-1), & C_-&=(-1,-1,1).
\end{aligned}
\]

Let their multiplicities be \(x,y,z,w\), in the order
\(P_+,C_+,P_-,C_-\).  For a label \(m=(m_1,-L,m_3)\),

\[
 x+y+z+w=L,\qquad
 x-z=\frac{m_1+m_3}{2},\qquad
 y-w=\frac{m_1-m_3}{2}.
\tag{2.1}
\]

For

\[
 b_N=(-N+1,-3N+1,-3N+1),\qquad L=3N-1,
\]

(2.1) has the unique nonnegative solution

\[
 (x,y,z,w)=(0,N,2N-1,0).
\tag{2.2}
\]

Thus \(b_N\) is generated only by \(P_-\) and \(C_+\).  It is an exact
two-generator edge coefficient, not merely a boundary-face coefficient.

For

\[
 a_N=(N,-3N,3N-2),\qquad L=3N,
\]

there are exactly two solutions:

\[
\begin{aligned}
 (x,y,z,w)&=(2N,0,1,N-1),\\
 (x,y,z,w)&=(2N-1,1,0,N).
\end{aligned}
\tag{2.3}
\]

Every tree for \(a_N\) therefore contains exactly one leaf off the
\(P_+,C_-\) edge.  The full coefficient is the sum of the first variation
with one \(P_-\) defect and the first variation with one \(C_+\) defect.

This gives the exact identities

\[
\begin{aligned}
 U(b_N)&=E^-_{3N-1,N},\\
 U(a_N)&=V^{P_-}_{3N,N-1}+V^{C_+}_{3N,N},
\end{aligned}
\tag{2.4}
\]

where \(E^-\) is the negative-edge recurrence and \(V\) solves its
linearized analogue on the positive edge.

## Closed edge and first-variation recurrences

Let \(E_{L,k}\) denote the Taylor coefficient containing \(L-k\) copies of
an edge pump and \(k\) copies of its edge catalyst.  The pure nonlinear
Taylor recurrence restricts exactly to

\[
 E_{L,k}=
 -\frac1{L-1}
 \sum_{\substack{L_1+L_2=L\\k_1+k_2=k}}
 \mathcal B(E_{L_1,k_1},E_{L_2,k_2}).
\tag{3.1}
\]

If \(V_{L,k}\) contains exactly one fixed defect leaf, then

\[
 V_{L,k}=
 -\frac1{L-1}
 \sum_{\substack{L_E+L_V=L\\k_E+k_V=k}}
 \left[
 \mathcal B(E_{L_E,k_E},V_{L_V,k_V})
 +\mathcal B(V_{L_V,k_V},E_{L_E,k_E})
 \right].
\tag{3.2}
\]

Equations (3.1)--(3.2) reduce the face calculation from a two-dimensional
support at every Taylor order to an edge recurrence and two linearized edge
recurrences.  They reproduce all R0.25 endpoint sharp coordinates for
\(N=2,\ldots,5\).

## Exact three-leaf transfer

For a target label \(m\) with \(L\) leaves and an initial leaf \(g\), define
the symmetric one-leaf attachment operator

\[
 \mathcal A^{L}_{m,g}v
 =-\frac1{L-1}
 \left[
 \mathcal B(u_g,v)+\mathcal B(v,u_g)
 \right],
\tag{4.1}
\]

where \(v\) is carried at \(m-g\).

The endpoint increments are

\[
 a_{N+1}-a_N=2P_++C_-,
 \qquad
 b_{N+1}-b_N=2P_-+C_+.
\tag{4.2}
\]

For either family, let \(T_N\) be the sum of the three distinct compositions
of (4.1), corresponding to the three placements of the catalyst in the
three-leaf block.  Substituting the Taylor recurrence three times gives the
exact identity

\[
 U_{N+1}=T_NU_N+R_N.
\tag{4.3}
\]

Here \(R_N\) is not an absolute-value majorant.  It is the signed sum of all
terms in which at least one of the last three substituted root splits is not
a one-leaf split.

Each charged endpoint mode has two polarization coordinates.  In the
sharp--longitudinal bases of R0.25, direct expansion of (4.1) gives

\[
\begin{aligned}
 T_N^{a}&\longrightarrow
 \begin{pmatrix}-24t&0\\0&-24t\end{pmatrix},\\
 T_N^{b}&\longrightarrow
 \begin{pmatrix}-24t&0\\0&16t\end{pmatrix},
\end{aligned}
\tag{4.4}
\]

where the quadratic generator is

\[
 t=0.4958758920134925\ldots.
\]

Thus both limiting spectral radii equal

\[
 24t=11.9010214083238\ldots>1.
\tag{4.5}
\]

The lower-left entry of \(T_N^b\) is exactly zero: on that edge all offsets
are collinear, so a sharp input cannot create a longitudinal output.  The
remaining off-diagonal entries tend to zero.

Equation (4.5) rules out the proposed proof based on a contractive isolated
three-leaf transfer.  It does not by itself determine the normalized
coefficient, because the complete Taylor coefficient grows rapidly and the
signed remainder in (4.3) is not small.

## Two-precision endpoint window

The reduced recurrence was evaluated at 160 and 224 MPFR bits through
\(N=25\), or 75 leaves.  The maximum relative discrepancy among the recorded
sharp coordinates and generated gains was

\[
 3.57\times10^{-43}.
\]

Selected values are:

| \(N\) | \(N|\sigma_A|\) | \(N|\sigma_B|\) | \(G_N\) | \(G_N/S_N\) |
|---:|---:|---:|---:|---:|
| 2 | 0.0457835 | 0.144742 | 0.304560 | 0.00433464 |
| 5 | 0.145483 | 0.0642850 | 0.235806 | 0.000409433 |
| 8 | 0.108981 | 0.224192 | 0.833874 | 0.0005319 |
| 12 | 0.340673 | 0.383169 | 3.46027 | 0.0009490 |
| 15 | 1.28725 | 0.418857 | 14.8808 | 0.002578 |
| 17 | 3.33449 | 0.704672 | 63.5770 | 0.008523 |
| 19 | 8.08183 | 1.13566 | 245.569 | 0.026229 |
| 21 | 18.8124 | 1.77833 | 889.302 | 0.077453 |
| 23 | 16.0146 | 2.72116 | 1154.21 | 0.083535 |
| 25 | 15.0468 | 4.07317 | 1620.26 | 0.098988 |

The first value above the R0.25 observed maximum \(0.214\) occurs at
\(N=8\) on the \(b\)-family.  The first value above one occurs at \(N=15\)
on the \(a\)-family.  At \(N=21\),

\[
 |\sigma_A|=0.89582677\ldots,
\]

so the normalized coefficient is almost entirely sharp in the sense relevant
to the R0.25 channel inequality.

These observations do not logically disprove \(N|\sigma|=O(1)\): any finite
table is compatible with some finite asymptotic constant.  They do show that
the early constant \(0.214\) was transient and that the generated gain has
already re-entered a strongly growing regime in this finite window.

## The signed remainder is a bulk term

For the \(b\)-family, the transfer and remainder in (4.3) are almost aligned
in the mode norm.  At \(N=24\to25\),

\[
\frac{M(T_NU_N)}{M(U_{N+1})}=0.158225\ldots,\qquad
\frac{M(R_N)}{M(U_{N+1})}=0.841775\ldots,
\]

and the triangle-to-full cancellation ratio differs from one by less than
\(2\times10^{-7}\).  The bulk remainder, not the edge transfer, supplies most
of the coefficient.

For the \(a\)-family the split is more oscillatory.  Across the audited
window, \(M(T_NU_N)/M(U_{N+1})\) ranges from about \(0.052\) to \(0.720\),
while \(M(R_N)/M(U_{N+1})\) reaches \(1.447\).  The signed cancellation ratio
falls to \(0.462\) at \(N=20\to21\).

Thus one-leaf root dominance at a single Taylor order does not turn into
dominance of the three-step endpoint transfer.  Any proof must control the
bulk convolution, including its sign and its contribution to the
longitudinal denominator.

## Consequence and next decision

R0.26 gives two exact reductions:

1. \(b_N\) is a two-generator edge problem.
2. \(a_N\) is a first variation of the opposite two-generator edge.

It also gives a negative result for the planned induction: the isolated
three-leaf matrix is expansive and its signed remainder is not perturbative.

The next defensible task is not a larger undirected table.  R0.27 should form
the bivariate generating equations for (3.1) and (3.2), then determine the
dominant singularity and the limiting polarization ratio.  There are two
decision branches:

- if singularity analysis gives a nonzero sharp ratio along either endpoint
  family, the generated-subspace one-radius mechanism fails for this datum;
- if the ratio vanishes, the singular expansion must supply the actual decay
  rate and replace the failed transfer contraction.

Only after that decision is resolved is it useful to return to the
shell-uniform viscous remainder.  Nothing in this note proves global
regularity or finite-time blow-up for three-dimensional Navier--Stokes.
