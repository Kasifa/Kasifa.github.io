# R0.68B-2f — Guarded enclosure of the complete moment lift

## Status

This is the next finite gate after the exact derivative and dominant-mass
certificates.  The first binary64 centre--radius implementation was a useful
failure: by degree four its centred maximum radius was already about
\(3.01\times10^{-5}\), because componentwise absolute values erase the
four-digit cancellation.  It is retained as a negative control and is
explicitly labelled `precision-baseline-rejected`.

The formal route instead stores each exact rational input as a binary64
double-double centre plus an outward radius, then performs the complete lift
in IEEE binary128 round-to-nearest arithmetic.  Every centre has a rigorous
nonnegative radius accounting for the R0.68B-2e mass interval, the root
interval, sparse-product roundoff, and the residual of every moment equation.

The calculation encloses moments only.  It does **not** yet enclose the heat
coefficients or the signature-compressed defect, so it is not the final heat
sign theorem.

## Moment equations

For each homogeneous multiindex \(\alpha\) of degree \(d\), the four-digit
affine lift gives

\[
 (16^d\nu I-C)m_\alpha=b_\alpha(m_\beta:\beta<\alpha).
\]

The matrix \(C\) is the exact signed 1792-state cycle.  Direct integer
calculation gives

\[
 \|C\|_\infty=123028,\qquad
 \|C\|_1=212804,\qquad
 \|C^\mathsf TC\|_\infty=2024341504.
\]

Hence

\[
 \|C\|_2\le\sqrt{2024341504}<44993.
\]

The degree-one inverse is therefore controlled in the Euclidean norm.  For
every \(d\ge2\), \(16^d\nu_-\) is already larger than
\(\|C\|_\infty\), so strict infinity-norm diagonal dominance applies.

## Guarded binary128 enclosure

All digit-transfer and channel-translation coefficients are integers and are
exactly representable in binary128.  With unit roundoff \(u=2^{-113}\), a
sparse path with at most \(n\) contributions uses the deliberately widened

\[
 \gamma_{8n}=\frac{8nu}{1-8nu},
\]

and an additional factor \(1+2^{-100}\) after each radius calculation.  The
final conversion of a residual norm to a solution radius is enlarged again
by \(1+2^{-88}\).  Subtractions used as resolvent denominators receive an
explicit downward error allowance.  The residual absolute bound and the
degree-one squared norm are also inflated before division.

The source-locked formal run enclosed all \(14{,}350{,}336\) raw coordinates.
Its degree-ten raw maximum radius is at most
\(7.91179658125257438\times10^{-22}\), and centering enlarges the maximum to
at most \(1.88584884046089302\times10^{-20}\).  The run bound its 410-file
sparse payload by SHA-256, validated finiteness and nonnegative radii, and
hashed the four binary128 output arrays.  An independent streaming scan then
rechecked every stored value.

## Boundary

This is a finite-dimensional certificate inside one fixed parallel-shear
construction.  It does not establish the final eighth-order heat sign, does
not control general three-dimensional perturbations, and does not solve the
Navier--Stokes Millennium problem.
