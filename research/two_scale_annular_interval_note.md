# R0.69W — A rigorous finite-separation sign obstruction

## 1. Statement

Fix the R0.69V two-scale family at separation four,

\[
 u_a=aU_1+(1-a)U_{1/4},\qquad 0\le a\le1,
 \tag{1.1}
\]

and retain the declared smooth cutoff: the beta\((3,3)\) survival profile on
\([1/20,19/20]\), convolved with the normalized standard bump
\(\exp[-1/(1-z^2)]\mathbf 1_{|z|<1}\) of physical radius \(1/40\).
For the physical-space annular functional \(\mathcal A_j\) of R0.69T,
R0.69W certifies

\[
 \frac{\mathcal A_0(u_a)}{a}=c_1+c_2a+c_3a^2<0
 \quad(0<a\le1),
 \qquad
 \mathcal A_{-2}(u_0)<0.
 \tag{1.2}
\]

The first inequality is proved by the two strict interval statements

\[
 c_3<0,\qquad \Delta=c_2^2-4c_1c_3<0.
 \tag{1.3}
\]

Together with the endpoint inequality, this excludes every amplitude in
\([0,1]\) from having nonnegative contributions on all relevant annuli.
The result is a rigorous static obstruction for this one compactly supported
family.  It is not a theorem about Navier--Stokes time evolution and does not
prove regularity or blow-up.

## 2. Exact common-rotation reduction

For a radial cutoff, write the vorticity at \(x=rn\) as

\[
 \omega(r,n)=P(r)e_3-Q(r)(e_3\!\cdot n)n
 -R(r)(e_3\!\cdot n)(e_3\times n),
 \tag{2.1}
\]

where, with \(q=q(r)\),

\[
 P=q+rq'+\frac{r^2q''}{6},\quad
 Q=\frac{4rq'+r^2q''}{6},\quad
 R=\frac{\sqrt6(6rq'+r^2q'')}{6}.
 \tag{2.2}
\]

The common \(SO(3)\) rotation is integrated by exact sphere moments.  After
putting \(t=n\cdot m\), the angular average is a polynomial of degree four in
\(t\); all apparent \(\sqrt{1-t^2}\) terms cancel.  With
\(d^2=r^2+s^2-2rst\), the remaining angular integral is exactly a linear
combination of

\[
 J_k(r,s)=\int_{|r-s|}^{r+s}\psi_j(d)d^k\,dd,
 \qquad k\in\{-4,-2,0,2,4\}.
 \tag{2.3}
\]

SymPy checks the equality between the unreduced angular kernel and (2.3),
checks that the common-core/common-core term is identically zero, and records
the reduced denominators.  Thus the certified numerical stage is only
two-dimensional in \((r,s)\).

## 3. The true mollifier, including endpoint distributions

No 48-node exploratory quadrature enters the certificate.  Arb encloses every
transcendental bump evaluation.  Raw moments
\(\int e^{-1/(1-z^2)}z^k\,dz\), \(0\le k\le5\), are bounded by one-sided
Darboux sums with explicit outward rounding.  The convolution and its first
three derivatives follow by integrating the corresponding beta polynomials.

The extended beta survival function is only \(C^2\).  Its fourth and fifth
distributional derivatives contain endpoint masses.  The verifier includes
these terms explicitly:

\[
 D^4S=S^{(4)}_{\rm int}+[S^{(3)}]_a\delta_a+[S^{(3)}]_b\delta_b,
 \tag{3.1}
\]

\[
 D^5S=S^{(5)}_{\rm int}+[S^{(4)}]_a\delta_a+[S^{(4)}]_b\delta_b
 +[S^{(3)}]_a\delta'_a+[S^{(3)}]_b\delta'_b.
 \tag{3.2}
\]

After convolution, (3.1)--(3.2) become certified bump and bump-derivative
boundary terms.  Their local ranges, rather than a global worst-case bound,
control the third-order cubature remainder.

## 4. Validated distance primitives and radial cubature

For every \(k\) in (2.3), a composite trapezoidal primitive is enclosed using
the exact endpoint intervals and the classical second-derivative error bound.
Point queries use the same validated partial-cell rule.  All binary64
arithmetic is widened with `nextafter`; accumulated endpoints use directed
one-sided sums.

On each radial rectangle, the reduced integrand is expanded through total
degree two at its midpoint.  The two diagonal Hessian terms are integrated
exactly.  A bivariate normalized Taylor algebra propagates interval bounds for
all total-degree-three derivatives.  If the side lengths are \(h_r,h_s\), the
remaining average error is bounded coefficientwise by

\[
 |T_{30}|\frac{h_r^3}{32}
 +|T_{21}|\frac{h_r^2h_s}{48}
 +|T_{12}|\frac{h_rh_s^2}{48}
 +|T_{03}|\frac{h_s^3}{32}.
 \tag{4.1}
\]

This preserves the analytic cancellations at the box center while retaining a
fully deterministic, non-probabilistic remainder.  The exact polynomial in
the amplitude is propagated throughout; no amplitude sampling is used.

## 5. Certified intervals

The formal source-locked run records the coefficient intervals, the
discriminant interval, all grid parameters, progress records, resource usage,
software versions, source hash, and Git commit in the R0.69W archive.  The
independent checker parses the decimal endpoints as exact rational numbers and
recomputes the interval discriminant without importing the producer.

The numerical interval table and final margins are inserted from the archived
`result.json` when the formal run completes.

## 6. Research value and boundary

R0.69V left one finite-separation loophole: a special amplitude might align
the important annular signs even though asymptotic scale separation cannot.
R0.69W closes that loophole for the entire separation-four affine family and
for the exact smooth cutoff used in the project.  The useful methodological
gain is broader than this example: common rotations, distance moments, and
validated Taylor cubature form a reusable route for converting a noisy
five-dimensional sign experiment into a reproducible proof certificate.

The limitation is equally precise.  A static sign obstruction to one ansatz
does not propagate a solution, control a critical norm, or rule out other
geometries.  The Millennium problem remains open; the next stage must change
the candidate geometry or establish a dynamical mechanism, not reinterpret
this negative result as global regularity.
