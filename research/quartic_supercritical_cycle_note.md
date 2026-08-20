# R0.64 — An exact supercritical cycle in the zero-time lifted transfer

## 1. Result

R0.63 identified the correct finite state space for the quartic
Rudin--Shapiro carrier: sixteen sign states together with the three possible
coefficient carries.  This note constructs the resulting (48)-state
integer transfer at zero heat time and settles the first proposed norm test.

Let (T_0,T_1\in\operatorname{Mat}_{48}(\mathbb Z)) be the two transfers
selected by the next binary digit of the target.  For the four-digit word

\[
  \omega=(0,1,0,0)
\]

read from the least significant digit upwards, put

\[
  W=T_0T_0T_1T_0.
\tag{1.1}
\]

The exact characteristic polynomial is

\[
 \boxed{
 \det(xI-W)=x^{42}(x-16)^2
 \bigl(x^4-25x^3-120x^2+3248x-8192\bigr).}
\tag{1.2}
\]

The quartic factor has a real root

\[
  \lambda\in(25,26),
  \qquad \lambda=25.1515893341\ldots .
\tag{1.3}
\]

Thus

\[
  \rho(W)\geq\lambda>25>2^4.
\tag{1.4}
\]

Consequently there is no common vector norm on the complete zero-time
state space for which both (T_0) and (T_1) have operator norm at most
(2).  This is an exact obstruction to the pointwise common-norm route
suggested in R0.63.

The conclusion is deliberately narrow.  The zero-time transfer is one
boundary value of the Gaussian-weighted simplex family.  Equation (1.4)
does not disprove the integrated estimate

\[
  |S_{4,m}|\leq C L^2M.
\tag{1.5}
\]

It proves that (1.5) cannot follow from a uniform pointwise contraction of
the unweighted (48)-state lift.  Any successful proof must use the heat
weights and time integration before taking a norm, or find a smaller
invariant quotient that is both reachable and sufficient for the target.

## 2. The exact (48)-state recursion

Let (a^{s}_{n}(q)) be the coefficient of (z^q) in the two
Rudin--Shapiro polynomials (R_{s,n}), where (s\in\{0,1\}).  Let
(C_n^{\boldsymbol\sigma}(q)) be the eight cubic coefficients from R0.63,
with (\boldsymbol\sigma\in\{0,1\}^3).  For
(k\in\{-1,0,1\}), define

\[
 X_n^{s,\boldsymbol\sigma,k}(q)
 :=a_n^s(q)C_n^{\boldsymbol\sigma}(q+k2^n),
 \qquad 0\leq q<2^n.
\tag{2.1}
\]

Write the next target digit as (b\in\{0,1\}).  For
(\boldsymbol\varepsilon=(\varepsilon_1,\varepsilon_2,
\varepsilon_3)\), put

\[
 d(\boldsymbol\varepsilon)
 =\varepsilon_1+\varepsilon_2-\varepsilon_3.
\]

The target recursion and the cubic recursion give

\[
 \boxed{
 X_{n+1}^{s,\boldsymbol\sigma,k}(b2^n+q)
 =\sum_{\boldsymbol\varepsilon\in\{0,1\}^3}
 (-1)^{sb+\boldsymbol\sigma\cdot\boldsymbol\varepsilon}
 X_n^{b,\boldsymbol\varepsilon,
 2k+b-d(\boldsymbol\varepsilon)}(q),}
\tag{2.2}
\]

where a term is zero if its last index is not in
(\{-1,0,1\}).  Equation (2.2) defines the two integer matrices
(T_b).  Direct exact convolution agrees with (2.2) for every state in the
audited dyadic levels.

The matrices have rank (12).  The four-step product (W) has rank (6).
Restricting (W) to its exact image gives the degree-six factor in (1.2);
the other (42) eigenvalues are zero.  No floating-point determinant is
used in this reduction.

## 3. The cycle is reachable by actual target coefficients

The eigenvalue in (1.3) is not confined to an unused algebraic state.  For
(r\geq0), let

\[
 M_r=16^r,
 \qquad
 q_r=2\frac{16^r-1}{15}.
\tag{3.1}
\]

The binary digits of (q_r), from low to high, are exactly (r) copies of
(0100).  Define the target-signed unweighted cubic correlation

\[
 y_r
 =a_{4r}^{0}(q_r)
 \sum_{A+B-C=q_r}
 a_{4r}^{0}(A)a_{4r}^{0}(B)a_{4r}^{0}(C).
\tag{3.2}
\]

The first values are

\[
 1,\ 22,\ 274,\ 5666,\ 77474,\ 1399138,\ 19990306,\ldots .
\tag{3.3}
\]

For (r\geq6), exact integer arithmetic gives

\[
 \begin{aligned}
 y_r={}&41y_{r-1}-280y_{r-2}-5168y_{r-3}\\
      &+60160y_{r-4}-131072y_{r-5}.
 \end{aligned}
\tag{3.4}
\]

Its generating function has numerator and denominator

\[
 \begin{aligned}
 N(z)={}&1-19z-348z^2+5760z^3-24576z^4+32768z^5,\\
 D(z)={}&1-41z+280z^2+5168z^3-60160z^4+131072z^5.
 \end{aligned}
\tag{3.5}
\]

The exact polynomial gcd is (1), and

\[
 D(z)=(1-16z)
 \bigl(1-25z-120z^2+3248z^3-8192z^4\bigr).
\tag{3.6}
\]

The four roots of the quartic in (1.2) lie respectively in
((-13,-12)), ((3,4)), ((8,9)), and ((25,26)).  Hence the pole
at (z=\lambda^{-1}) is present and dominates.  In particular,

\[
 |y_r|\asymp \lambda^r
 =M_r^{\log_{16}\lambda},
 \qquad
 \log_{16}\lambda=1.1631444155\ldots>1.
\tag{3.7}
\]

This supplies an explicit target family for the superlinear unweighted
cubic growth noted but not resolved in R0.62.

## 4. Consequence for the heat-weighted problem

The R0.63 Gaussian weights equal (1) at
(\tau_0=\tau_1=\tau_2=0).  At every fixed finite dyadic level, the
weighted coefficients depend continuously on the time variables and
converge to the transfer above at that corner.  Therefore a uniform
pointwise argument on the closed simplex that bounds the full lifted state
by the same factor (2) at every level would also have to cover the
zero-time matrices.  Equation (1.4) rules out that form of argument.

This does not settle the integrated transfer.  Three effects remain
available and are absent from (W):

1. the Gaussian restrictions are non-autonomous across dyadic levels;
2. the simplex integral couples the three time variables before a norm is
   taken;
3. the Navier--Stokes target uses a particular initial vector and final
   functional, not an arbitrary operator input and output.

The next calculation should retain all three effects.  A useful object is
the scalar reachable transfer

\[
 \int_{\Delta_T}
 \ell_{m,\tau}
 \mathfrak T_{n,\tau}\cdots\mathfrak T_{1,\tau}
 v_{0,\tau}\,d\tau,
\tag{4.1}
\]

not the full pointwise operator norm.  R0.65 will construct certified upper
and lower envelopes for (4.1) on the explicit cycle (3.1).  If heat damping
reduces its block growth below (16), the remaining route is an integrated
reachable-space estimate.  If the growth stays above (16), the proposed
uniform quartic bound (1.5) fails for this packet.

## 5. Claim boundary

### Proved here

1. The exact (48)-state recursion (2.2).
2. The exact characteristic polynomial (1.2).
3. An eigenvalue (\lambda\in(25,26)), so no common pointwise norm can
   bound both zero-time digit transfers by (2).
4. The explicit target family (3.1) reaches and observes the dominant
   cycle, with the exact recurrence (3.4).

### Not proved

There is no proof or disproof of (1.5), no control of the complete even
Picard series, no singularity construction, and no result for arbitrary
three-dimensional data.  This note does not solve the Navier--Stokes
Millennium problem.
