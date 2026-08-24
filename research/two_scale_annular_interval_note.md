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
\(\int e^{-1/(1-z^2)}z^k\,dz\), \(0\le k\le5\), use a validated composite
trapezoidal primitive.  The global bound
\(|(z^k b(z))''|\le k^2+k+8\) follows from
\(|b|\le1\), \(|b'|\le1\), and \(|b''|<8\), so both full cells and arbitrary
partial endpoint cells carry explicit second-derivative error bounds.  The
convolution and its first three derivatives then follow by integrating the
corresponding beta polynomials.  The producer never replaces this convolution
by floating quadrature nodes.

The extended beta survival function is only \(C^2\).  Its fourth through sixth
distributional derivatives contain endpoint masses.  The producer includes
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
boundary terms.  Differentiating once more gives

\[
 D^6S=[S^{(5)}]_a\delta_a+[S^{(5)}]_b\delta_b
 +[S^{(4)}]_a\delta'_a+[S^{(4)}]_b\delta'_b
 +[S^{(3)}]_a\delta''_a+[S^{(3)}]_b\delta''_b,
 \tag{3.3}
\]

because the beta\((3,3)\) survival profile has no sixth interior derivative.
Thus the sixth derivative of the mollified cutoff consists only of certified
bump, bump-prime, and bump-second-derivative boundary terms.  With
\(t=(1-u^2)^{-1}\),

\[
 b''(u)=e^{-t}(4t^4-12t^3+6t^2).
 \tag{3.4}
\]

An exact Sturm isolation of the critical polynomial
\(2t^3-14t^2+21t-6\), followed by Arb evaluation on its two roots above one,
certifies \(|b''|<8\).  Rational guard bands around the corresponding
\(|u|\approx0.610\) and \(|u|\approx0.895\) localize this bound.  These local
ranges, rather than a global worst-case interval, control the cubature
remainder.

## 4. Validated distance primitives and radial cubature

For every \(k\) in (2.3), a composite trapezoidal primitive is enclosed using
the exact endpoint intervals and the classical second-derivative error bound.
The convolved survival cutoff is nonincreasing, so its range on each distance
cell is enclosed by certified cubic Hermite interpolation at the two endpoints;
this avoids repeatedly charging a full cutoff-table cell to a much smaller
distance cell.  The interpolation remainder is bounded by
\(\|q^{(4)}\|_\infty h^4/384\).  Point queries use the same validated
partial-cell rule.  The distance grid has dyadic step \(2^{2-P}\), so every
grid node is exactly representable in binary64 and is retained as a point
interval; widening such a node would spuriously cross aligned cutoff cells.
For the Taylor coefficients at a radial-box center, cutoff derivatives through
order three are expanded from the nearest exact rational cutoff node.  The
node derivatives are themselves interval-certified, the residual term uses
the global fourth-derivative bound, and the result is intersected with the
independent whole-cell derivative range.  Only the box-wide remainder uses the
whole-cell derivative enclosure.  This point/range separation removes a
purely artificial cutoff-cell width without weakening any box enclosure.
All non-exact binary64 arithmetic is widened with `nextafter`; accumulated
endpoints use directed one-sided sums.

On each radial rectangle the producer computes two independent rigorous
remainders.  The first is the standard total-degree-two midpoint expansion
with a third-derivative bound.  Its average remainder is bounded by

\[
 M_{30}\frac{h_r^3}{32}
 +M_{21}\frac{h_r^2h_s}{48}
 +M_{12}\frac{h_rh_s^2}{48}
 +M_{03}\frac{h_s^3}{32}.
 \tag{4.1}
\]

The second expansion goes through total degree three.  The two diagonal
Hessian terms are integrated exactly, while every cubic monomial has an odd
exponent in at least one centered coordinate and therefore integrates to zero
exactly.  A bivariate normalized Taylor algebra propagates interval bounds for
all total-degree-four derivatives.  Its average remainder is bounded
coefficientwise by

\[
 |T_{40}|\frac{h_r^4}{80}
 +|T_{31}|\frac{h_r^3h_s}{128}
 +|T_{22}|\frac{h_r^2h_s^2}{144}
 +|T_{13}|\frac{h_rh_s^3}{128}
 +|T_{04}|\frac{h_s^4}{80}.
 \tag{4.2}
\]

For every box and every amplitude coefficient the certified error is the
smaller of (4.1) and (4.2).  This selection does not mix midpoint values or
derivative enclosures: both bounds enclose the same exact box average.  The
sixth cutoff derivative needed by (4.2) is supported only in the two mollified
endpoint bands, so those bands alone receive the extra boundary refinement.
This preserves the analytic cancellations at the box center while retaining a
fully deterministic, non-probabilistic remainder.  The exact polynomial in
the amplitude is propagated throughout; no amplitude sampling is used.

## 5. Certified intervals

The formal source-locked run gives

\[
\begin{aligned}
c_1&\in[-0.0020421027908703103,-0.0008440552534174868],\\
c_2&\in[0.002393592617980337,0.004933596141229829],\\
c_3&\in[-0.12676969700886406,-0.12489333880250154],\\
\Delta&\in[-0.0010297777226174903,-0.00039732714404764783],\\
\mathcal A_{-2}(u_0)&\in
[-0.001947993537909744,-0.0019148502803584854].
\end{aligned}
\tag{5.1}
\]

Thus the strict margins from zero are at least
`0.12489333880250154`, `0.00039732714404764783`, and
`0.0019148502803584854` for \(c_3\), \(\Delta\), and the endpoint value,
respectively.

The locked producer commit is
`2b3141a333d3dea0c4b7a241c11f9adbca31d1b4`.  The P22 distance primitive has
4,194,304 cells; the other formal parameters are raw-moment P19, 2,048 cutoff
cells, 512 transition cells, 128 core cells, 256 plateau cells, boundary
refinement four, and 256-bit Arb endpoints.  Twenty disjoint workers completed
with a maximum elapsed time of `1535.6651919609867` seconds and a summed worker
time of `28877.69878333574` seconds.  Their observed peak-RSS values sum to
`67.2967841796875` GiB.

The archive records all grid parameters, progress records, resource usage,
software versions, source hashes, and the clean Git commit.  The independent
checker parses the decimal endpoints as exact rational numbers and recomputes
the interval discriminant without importing the producer; all 24 checks pass.

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
