# R0.60 — Invariant shear reduction and the cubic target gap

## 1. Question and answer

R0.59 left a precise nonlinear question.  Its first Picard output is coherent
on the growing low-frequency set

\[
 K_M=\{(0,m,0):1\leq m\leq M\},
\]

but the terms of order at least three were not controlled.  The first task is
therefore to determine whether the cubic term can return to \(K_M\) at the
same short time.

For the R0.59 packet the answer is **no**, for a structural reason stronger
than a finite resonance search.  The initial field belongs to the invariant
class

\[
 u(x,t)=(0,F(x_1,t),G(x_1,x_2,t)).
\]

In this class the full three-dimensional Navier--Stokes equation reduces to
one heat equation and one linear advection--diffusion equation.  Every
homogeneous Picard term after the linear term is polarized in the \(e_3\)
direction, and the usual binary Picard trees collapse to one ordered chain.

The cubic term has a strict Fourier gap

\[
 |\xi_1|>\frac34H,
\]

so it cannot alter the R0.59 target projection.  More generally, the odd
terms of orders \(3,5,7,9\) cannot reach the plane \(\xi_1=0\).  This statement
is sharp at the level of frequency support: an explicit order-eleven path
reaches that plane when \(LM\geq5\).

The cubic term is nevertheless dynamically necessary.  It can return to the
original high-frequency \(V\) support, and it enters the exact fourth-order
energy compensation with the positive energy of the quadratic term.  The
first possible correction to the target low modes is therefore quartic, not
cubic.

This result does not bound the complete higher-order remainder.  It identifies
the correct next calculation and proves that the R0.59 packet lies in a
globally regular shear class, so it is an obstruction to a proposed estimate,
not a candidate blow-up solution.

## 2. Exact invariant subspace

Work on \(\mathbb T^3\) with viscosity one.  Consider a smooth real field

\[
 u=(0,F(x_1,t),G(x_1,x_2,t)).
\tag{2.1}
\]

It is divergence free.  Direct calculation gives

\[
 (u\cdot\nabla)u=F\,\partial_2G\,e_3.
\tag{2.2}
\]

The right side is divergence free because it is independent of \(x_3\).
The pressure may therefore be chosen spatially constant, and the full
Navier--Stokes system is exactly

\[
 \boxed{
 \begin{aligned}
  \partial_tF-\partial_1^2F&=0,\\
  \partial_tG-\Delta_{12}G+F\partial_2G&=0.
 \end{aligned}}
\tag{2.3}
\]

Here \(\Delta_{12}=\partial_1^2+\partial_2^2\).  Thus \(F\) is an explicitly
known heat flow and \(G\) solves a linear parabolic equation with a smooth
time-dependent shear coefficient.

The R0.59 data have exactly this form.  Its \(U\) block is polarized along
\(e_2\) and depends only on \(x_1\).  Its \(V\) block is polarized along
\(e_3\) and depends only on \(x_1,x_2\).  Consequently, for every fixed
\(L,M,A\), the associated full solution is globally smooth by standard linear
parabolic theory.  No smallness assumption is needed for that statement.

This global regularity is symmetry-specific.  It gives no a priori bound for
arbitrary three-dimensional data.

The plane-parallel reduction itself is classical and is not claimed as new.
After a permutation of coordinates, equations (2.1)--(2.3) are the periodic
counterpart of the pressureless plane-parallel system written explicitly by
Mazzucato and Taylor.  The narrower contribution here is the exact placement
of the R0.59 tensor packet in that class and the resulting all-order support
arithmetic for its homogeneous Picard chain.

## 3. The full Picard forest collapses to one chain

Factor the common amplitude from the initial profiles:

\[
 F(0)=A F_0,
 \qquad
 G(0)=A G_0.
\tag{3.1}
\]

Write the amplitude expansion

\[
 F=A F_1,
 \qquad
 G=\sum_{n\geq1}A^nG_n,
\tag{3.2}
\]

where

\[
 F_1(t)=e^{t\partial_1^2}F_0,
 \qquad
 G_1(t)=e^{t\Delta_{12}}G_0.
\tag{3.3}
\]

Substitution into (2.3) gives, for every \(n\geq2\),

\[
 \boxed{
 (\partial_t-\Delta_{12})G_n
 =-F_1\partial_2G_{n-1},
 \qquad G_n(0)=0.}
\tag{3.4}
\]

In the usual vector Picard notation,

\[
 u^{[1]}=F_1e_2+G_1e_3,
 \qquad
 u^{[n]}=G_ne_3\quad(n\geq2).
\tag{3.5}
\]

Equation (3.4) is the complete recurrence.  Indeed, every Fourier wavevector
has zero third component.  A left factor polarized along \(e_3\) therefore
differentiates every right factor to zero.  The \(V\) part of \(u^{[1]}\) also
acts trivially.  Only the \(U\) part of \(u^{[1]}\) acting on the preceding
\(e_3\)-polarized term survives.

Thus no Catalan family of binary trees remains.  At order \(n\) there is one
time-ordered chain containing one \(V\) leaf and \(n-1\) \(U\) leaves.

Fourier transformation in \(x_2\) makes an additional conservation law
explicit.  If

\[
 G(x_1,x_2,t)=\sum_m G_m(x_1,t)e^{imx_2},
\]

then each \(m\) evolves independently:

\[
 \partial_tG_m-\partial_1^2G_m+m^2G_m+imF G_m=0.
\tag{3.6}
\]

Every Picard interaction preserves the second frequency \(m\).

## 4. Carrier interval and support arithmetic

Put

\[
 N=LM,
 \qquad H=4N,
 \qquad D=N-1,
\tag{4.1}
\]

and define the carrier interval

\[
 I_N=\{H,H+1,\ldots,H+D\}.
\tag{4.2}
\]

All \(U\) frequencies have first coordinate in \(\pm I_N\).  For a fixed
positive output frequency \(m\), every initial \(V\) frequency has first
coordinate \(-Q\), with \(Q\in I_N\).  Since every further interaction adds
one \(U\) frequency, every first coordinate in \(G_n(\cdot,m)\) has the form

\[
 \boxed{
 \xi_1=-Q+\sum_{j=1}^{n-1}\sigma_jP_j,
 \qquad Q,P_j\in I_N,
 \quad \sigma_j\in\{-1,1\}.}
\tag{4.3}
\]

This is a support inclusion.  It does not assert that the sum of all paths at
an admissible frequency is nonzero.

For the cubic term, (4.3) is a signed sum of three numbers in \(I_N\).  If two
signs oppose one sign, then

\[
 |\xi_1|\geq2H-(H+D)=H-D=3N+1>\frac34H.
\tag{4.4}
\]

The all-equal sign cases are larger.  Hence

\[
 \boxed{
 \operatorname{supp}\widehat G_3
 \subset\{\xi:|\xi_1|>3H/4\},
 \qquad \Pi_0G_3=0.}
\tag{4.5}
\]

Here \(\Pi_0\) denotes averaging in \(x_1\).  In particular, the cubic term
cannot modify any R0.59 target frequency \(k_m=(0,m,0)\).

## 5. No low-plane return at odd orders through nine

Let \(n=2k+1\) be odd.  If a signed sum of \(2k+1\) carriers were zero, one
side of the equality would contain at most \(k\) carriers and the other at
least \(k+1\).  The smaller side is at most \(k(H+D)\), while the larger side
is at least \((k+1)H\).  Therefore zero is impossible whenever

\[
 kD<H.
\tag{5.1}
\]

Since \(D=N-1\) and \(H=4N\), condition (5.1) holds for \(k=1,2,3,4\).  More
precisely, the respective gaps are

\[
 H-D=3N+1,
 \quad H-2D=2N+2,
 \quad H-3D=N+3,
 \quad H-4D=4.
\tag{5.2}
\]

Consequently,

\[
 \boxed{
 \Pi_0G_n=0
 \quad\text{for }n\in\{3,5,7,9\}.}
\tag{5.3}
\]

The support argument stops sharply after order nine.  If \(N\geq5\), set

\[
 Q=H+N-5\in I_N.
\]

Then the order-eleven path

\[
 -Q+5(H+N-1)-5H=0
\tag{5.4}
\]

uses one admissible \(V\) carrier and ten admissible \(U\) carriers.  Thus an
odd return to \(\xi_1=0\) is kinematically possible at order eleven.  Equation
(5.4) is a support witness, not a claim that the complete order-eleven
coefficient has already been summed or proved nonzero.

## 6. Cubic high-frequency return and the first target correction

Although \(G_3\) cannot reach \(K_M\), it can return to the original \(V\)
support.  For every initial first coordinate \(-Q\) and every \(P\in I_N\),

\[
 -Q+P-P=-Q.
\tag{6.1}
\]

These are backtracking shear paths.  Their two derivative factors are both
nonzero because the conserved second frequency is \(m\ne0\).  The two
Duhamel time kernels are positive before the common Fourier phase is applied.
The cubic term can therefore interact with the linear \(V\) term in the
fourth-order energy balance.

The low target plane has a different parity.  The quadratic path is

\[
 -Q+Q=0.
\tag{6.2}
\]

After it, a cancelling pair of shear frequencies produces an admissible
quartic path,

\[
 -Q+Q+P-P=0.
\tag{6.3}
\]

Thus the first possible correction to the R0.59 target coefficient is
\(G_4\), not \(G_3\).  Determining the complete signed coefficient in (6.3),
including all non-backtracking paths and exact nested heat denominators, is
the next unresolved calculation.

## 7. Exact fourth-order energy compensation

The scalar equation in (2.3) has the energy identity

\[
 \frac12\frac d{dt}\|G\|_2^2+\|\nabla G\|_2^2=0,
\tag{7.1}
\]

because \(F\) is independent of \(x_2\).  Expanding (7.1) in powers of \(A\)
and taking the coefficient of \(A^4\) gives

\[
 \boxed{
 \frac d{dt}
 \left(2\langle G_1,G_3\rangle+\|G_2\|_2^2\right)
 +2\left(
  2\langle\nabla G_1,\nabla G_3\rangle
  +\|\nabla G_2\|_2^2
 \right)=0.}
\tag{7.2}
\]

The same identity follows directly from (3.4).  Pair the \(G_3\) equation
with \(G_1\), pair the \(G_2\) equation with \(G_2\), and use

\[
 \langle G_1,F\partial_2G_2\rangle
 =-\langle G_2,F\partial_2G_1\rangle.
\tag{7.3}
\]

Equation (7.2) explains the R0.59 energy bookkeeping.  The positive
\(\|G_2\|_2^2\) contribution is not cancelled by overlap between the linear
and quadratic supports; those supports are exactly orthogonal.  Compensation
first enters through the cubic high-frequency return \(G_3\) and through
dissipation.

## 8. The theorem and its boundary

### Theorem — invariant shear chain and cubic target gap

For every dyadic \(L,M\geq1\), let \(u_0\) be the R0.59 packet with
\(H=4LM\).  Then:

1. The full Navier--Stokes solution remains in the invariant class (2.1) and
   is governed exactly by (2.3).
2. Its homogeneous Picard expansion satisfies the one-chain recurrence
   (3.4); every term of order at least two is polarized along \(e_3\), and
   every \(x_2\) frequency evolves independently.
3. The cubic term satisfies the strict support gap (4.5), so it has zero
   projection onto every R0.59 target mode.
4. The odd terms of orders \(3,5,7,9\) have zero \(x_1\)-average.  The
   order-eleven support witness (5.4) shows that this elementary interval
   exclusion cannot be extended to all odd orders.
5. Cubic backtracking paths return to the original \(V\) support, and the
   exact fourth-order energy coefficient is (7.2).
6. The first support-admissible correction to the target low modes is the
   quartic term \(G_4\).

The theorem does **not** prove:

1. a uniform bound for \(G_4\) or the sum of all terms of order at least four;
2. dominance of the R0.59 quadratic output in a critical norm;
3. norm inflation, discontinuity, or unboundedness of the critical bilinear
   map;
4. a statement for arbitrary three-dimensional data;
5. finite-time blow-up, large-data global regularity, or a solution of the
   Clay Millennium problem.

In fact, the packet itself belongs to a globally regular shear class.  Its
role is to test the sharpness of proposed estimates, not to model a possible
singularity.

## 9. Research value and next falsifiable test

R0.60 changes the higher-order problem in two useful ways.

First, there is no cubic target resonance to estimate.  A search over generic
binary Picard trees would have analyzed many identically zero branches.  The
exact invariant reduction removes them and replaces the full expansion by a
single ordered shear chain.

Second, global smoothness of this symmetry class does not by itself preserve
the R0.59 low-frequency lower bound.  The remaining issue is quantitative:
the quartic and later even terms may dress or cancel the first coherent
output while the complete scalar solution stays regular.

The next falsifiable problem is therefore:

> Compute the complete quartic coefficient
> \(\Pi_0G_4(t_H)\), including every signed path and nested heat denominator.
> After the normalization \(A\asymp\varepsilon\sqrt H\), decide whether its
> ratio to \(\Pi_0G_2(t_H)\) is bounded by \(C\varepsilon^2/L^2\), or whether
> a family of non-backtracking paths creates growth in \(M\).

The first outcome would supply the first scale-uniform nonlinear remainder
gain for the packet.  The second would locate a new higher-order obstruction.
Neither outcome would by itself settle the Clay problem, but both are sharper
than continuing to inspect the already excluded cubic target channel.

## References

1. A. Mazzucato and M. Taylor, *Vanishing viscosity plane parallel channel
   flow and related singular perturbation problems*, Analysis & PDE 1 (2008),
   35--93. <https://doi.org/10.2140/apde.2008.1.35>.
