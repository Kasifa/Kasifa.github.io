# R0.37: a weighted-Wiener restart beyond the R0.31 radius

## Status and boundary

R0.35 proved that the quadratic active map is unbounded on an ordinary
same-radius Wiener ball.  R0.36 paid for that loss with two radii and obtained
a correct recentering step, but the step stayed inside the R0.31 polydisc and
only inverted a finite Jacobian block.

This note uses a different Banach norm.  One total-degree weight absorbs the
remaining derivative in the quadratic recurrence.  On the active support
cone, the nonlinear map is then bounded at one radius, its exact Jacobian has
an all-order Neumann inverse, and a degree-40 rational restart increases the
proved common radius from

\[
 \rho_0=\frac4{81}
 \quad\hbox{to}\quad
 \rho_1=\frac{16}{243}=\frac43\rho_0.
\tag{0.1}
\]

The operator estimates and Banach contraction are all-order statements.  The
degree-40 polynomial, 4096 support-pair checks, and 62-dimensional Jacobian
inverse are finite exact regressions.  The theorem concerns the reduced edge
generating equation.  It does not prove regularity or blow-up for the full
three-dimensional Navier--Stokes equation, and it does not reach the R0.32
Padé candidate.

## 1. The active support cone

For a monomial \(Z^nW^k\), put

\[
 L=n+k,
 \qquad q=2k-n=3k-L.
\tag{1.1}
\]

The canonical active series is supported in \(q\ge-1\).  Let
\(\mathcal B_r^+\) be the completion of polynomials with this support under

\[
 \boxed{
 \|f\|_{\mathcal B_r}
 =\sum_{n,k\ge0}(n+k)|f_{n,k}|r^{n+k}.
 }
\tag{1.2}
\]

The quadratic map \(\Phi\) is the map defined in R0.35.  The charge
symmetrization from R0.30 applies to arbitrary inputs in the cone, not only to
the exact solution.  The only apparently forbidden output has charge
\(-2\), arising from two charge-\(-1\) factors.  That mixed contribution is
zero because the two charges are equal.  Thus \(\Phi\) and its polarized
derivative preserve \(q\ge-1\).

If \(A_i\) and \(H_j\) are the homogeneous coefficient \(\ell^1\) norms of
\(f\) and \(h\), the same symmetrization gives

\[
 \|(D\Phi(f)h)_L\|_1
 \le \frac32\sum_{i+j=L}\min(i,j)
       \bigl(A_iH_j+H_iA_j\bigr).
\tag{1.3}
\]

This is an all-order algebraic inequality.  The finite support-pair audit is
only an independent implementation check.

## 2. One degree weight closes the nonlinear map

For positive integers \(i,j\),

\[
 (i+j)\min(i,j)\le2ij.
\tag{2.1}
\]

Multiplying the R0.30 quadratic layer estimate by \(Lr^L\), summing, and
using (2.1) proves

\[
 \boxed{
 \|\Phi(f)\|_{\mathcal B_r}
 \le3\|f\|_{\mathcal B_r}^2.
 }
\tag{2.2}
\]

Applying the same calculation to (1.3) gives

\[
 \boxed{
 \|D\Phi(f)h\|_{\mathcal B_r}
 \le6\|f\|_{\mathcal B_r}\|h\|_{\mathcal B_r}.
 }
\tag{2.3}
\]

This explains the R0.35 obstruction.  The unweighted norm loses one total
degree on high--high interactions; (1.2) supplies exactly that degree.

## 3. An infinite Jacobian inverse on the old domain

R0.31 proved, with \(K=81/4\),

\[
 A_L\le\frac{2K^{L-1}}{L^3}.
\tag{3.1}
\]

For \(r\le4/81\), set \(x=Kr\le1\).  Then

\[
 \|a\|_{\mathcal B_r}
 \le\frac2K\sum_{L\ge1}\frac{x^L}{L^2}
 <\frac2K\frac53
 =\frac{40}{243}.
\tag{3.2}
\]

Equations (2.3) and (3.2) imply

\[
 \|D\Phi(a)\|<\frac{80}{81}<1.
\tag{3.3}
\]

Therefore

\[
 \boxed{
 (I-D\Phi(a))^{-1}
 =\sum_{m\ge0}D\Phi(a)^m,
 \qquad
 \|(I-D\Phi(a))^{-1}\|\le81.
 }
\tag{3.4}
\]

This is the infinite-dimensional inverse missing from R0.36.  It is an
operator theorem on \(\mathcal B_r^+\), not an inference from the finite
matrix.  Using the exact first 40 homogeneous layers and the all-order tail

\[
 \frac2K\sum_{L>40}\frac1{L^2}
 \le\frac2{40K}=\frac1{405}
\tag{3.5}
\]

improves the boundary Jacobian bound to approximately \(0.6975530527\) and
the inverse bound to approximately \(3.306364997\).

## 4. The exact degree-40 restart

Let \(p_{40}\) be the exact recurrence polynomial through total degree 40,
and define

\[
 F(p)=p-(Z+W)-\Phi(p).
\tag{4.1}
\]

The recurrence makes every coefficient of \(F(p_{40})\) through degree 40
zero.  The complete polynomial residual occupies degrees 41 through 80.
At

\[
 r_* = \frac{16}{243},
\tag{4.2}
\]

the exact rational audit gives

\[
 \begin{aligned}
 M&=\|p_{40}\|_{\mathcal B_{r_*}}
      \approx0.15865694927073254,\\
 Y&=\|F(p_{40})\|_{\mathcal B_{r_*}}
      \approx2.99904918794896\times10^{-46},\\
 Z&=6M\approx0.95194169562439524,\\
 m&=1-Z\approx0.04805830437560476.
 \end{aligned}
\tag{4.3}
\]

All four stored values are exact fractions.  The decimals are views, not
decision inputs.

Use the closed support-cone tail subspace containing only degrees above 40,
and set

\[
 \varepsilon=\frac{m}{12}
 \approx0.004004858697967064.
\tag{4.4}
\]

The correction equation is

\[
 h=-F(p_{40})+D\Phi(p_{40})h+\Phi(h).
\tag{4.5}
\]

The tail subspace is invariant because every application of \(D\Phi(p_{40})\)
raises total degree and \(F(p_{40})\) begins at degree 41.  Equations
(2.2)--(2.3) give

\[
 \|\mathcal T(h)\|
 \le Y+Z\varepsilon+3\varepsilon^2.
\tag{4.6}
\]

With the choice (4.4), the available residual allowance is exactly

\[
 \frac{m^2}{16}\approx1.44350038716142\times10^{-4}.
\tag{4.7}
\]

The exact residual is only about \(2.08\times10^{-42}\) of this allowance.
The certificate checks

\[
 Y+Z\varepsilon+3\varepsilon^2
 \approx0.003860508659250922
 <\varepsilon,
\tag{4.8}
\]

and the ball Lipschitz constant is

\[
 Z+6\varepsilon
 =\frac{1+Z}{2}
 \approx0.9759708478121976<1.
\tag{4.9}
\]

Banach's theorem therefore gives a unique \(h\) in this ball.  The function
\(a=p_{40}+h\) solves the active equation in \(\mathcal B_{r_*}^+\).  Its
first 40 layers equal the canonical recurrence, and triangular formal
uniqueness identifies all later layers with the same canonical formal
series.

## 5. The transport fields extend to the same radius

The normalized transport recurrence has a linear operator \(T_a\).  Its
R0.30 layer estimate and (2.1) give

\[
 \|T_af\|_{\mathcal B_r}
 \le2\|a\|_{\mathcal B_r}\|f\|_{\mathcal B_r}.
\tag{5.1}
\]

At \(r=r_*\), the restart ball gives

\[
 \|a\|_{\mathcal B_{r_*}}
 \le M+\varepsilon
 \approx0.16266180796869960,
\tag{5.2}
\]

so

\[
 \|T_a\|\le2(M+\varepsilon)
 \approx0.32532361593739921<1.
\tag{5.3}
\]

The Neumann series constructs the canonical normalized \(U\) and \(V\)
fields from their degree-one seeds on the same radius.  Thus (0.1) is a
common absolute-analyticity radius for \(a,U,V\).  This statement does not
claim that the logarithmic quotients from R0.29 stay nonzero throughout the
larger polydisc.

## 6. Finite exact regressions

The audit performs the following checks without floating-point decisions:

1. 4096 ordered admissible basis pairs through degree 12 obey the mixed
   layer estimate; the constant three is attained by two pairs;
2. all 16 tested charge-\(-1\) pairings cancel exactly;
3. outside the support cone, the pair \(W^2,Z^3\) gives
   \(D\Phi(W^2)Z^3=(21/2)Z^3W^2\), exceeding the proposed mixed bound by
   the exact factor \(7/4\); this negative check shows that \(q\ge-1\) is an
   essential hypothesis;
4. the degree-40 recurrence residual begins at degree 41;
5. the complete 1573-term residual through degree 80 is included in the
   contraction norm;
6. the support-cone Jacobian through degree 12 is a 62-dimensional unit
   lower-triangular matrix;
7. its exact rational inverse is checked on both sides;
8. its weighted column norms at \(4/81\) and \(16/243\) lie below the
   corresponding all-order bounds.

The finite Jacobian inverse is not used to prove (3.4) or the contraction.
It remains an implementation regression and a starting point for a sharper
preconditioner.

## 7. What the radius gain means

The bivariate radius improves by exactly \(4/3\).  The fixed-charge radius
\(|R|<r^3\) therefore improves by

\[
 \left(\frac43\right)^3=\frac{64}{27}
 \approx2.37037.
\tag{7.1}
\]

This is a genuine all-order extension beyond the R0.31 domain, rather than a
finite coefficient diagnostic.  It is still far from the R0.32 candidate:
the candidate modulus remains more than roughly 2625 times the new proved
fixed-charge radius.  No claim is made that the candidate is an actual
singularity or that a singularity-free continuation path reaches it.

The useful next step is a preconditioned infinite-dimensional Newton bound.
The exact low Jacobian block can remove the conservative low-mode part of
the constant, while the weighted estimate controls the remaining tail.  That
is the R0.38 target.

## Reproduction

Run `research/edge_weighted_restart_audit.py` with the pinned R0.31 and R0.36
certificate hashes.  The formal run uses exact GMP rationals, an append-only
progress log, and a process-tree resource log.  It uses no random seed and no
floating-point sign decision.

## References

1. R0.30, *An all-order analytic majorant for the canonical edge system*.
   This supplies the homogeneous active and transport layer inequalities.
2. R0.31, *An improved common analytic domain for the canonical edge
   system*.  This supplies the coefficient majorant with \(K=81/4\).
3. R0.35, *Charge-projection geometry and the obstruction to naive
   recentering*.  This supplies the ordinary-Wiener same-radius obstruction.
4. R0.36, *A certified short recentering step inside the R0.31 polydisc*.
   This records the finite-inverse boundary closed by the present theorem.
