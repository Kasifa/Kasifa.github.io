# R0.73W certificate claim boundary

This package is an exact finite calculation on normalized
\(\mathbb T^3\).  Its primary witness is the smooth, mean-zero,
divergence-free field

\[
 R=(\cos(y+z)-\sin(x+y+z)+\cos(2z),
    \cos x+\sin(x+y+z),0).
\]

The exact rational rank of its Fourier support is three.  The two producers
use only rational arithmetic and finite polynomials in \(q=e^{-s}\).

The package proves that the spatial mean of the signed production is

\[
 \langle\Pi_s(AR)\rangle=\frac{A^3}{4}q^2(1-q^2),
\]

and that the spatial mean of the gradient defect is

\[
 \langle D_{ii,s}(AR)\rangle
 =A^2\left[\frac12(1-q^2)+(1-q^4)+3(1-q^6)+2(1-q^8)\right].
\]

Consequently, for \(A>0\), \(\nu>0\), and \(0<q<1\),

\[
 \frac{|\langle\Pi_s\rangle|}
 {\nu\langle D_{ii,s}\rangle}
 =\frac{Aq^2}{2\nu(13+12q^2+10q^4+4q^6)}.
\]

This ratio is unbounded as \(A\to\infty\).  The certificate therefore
rules out an amplitude-independent absorption inequality of this precise
same-time, spatial-mean form.  As \(s\downarrow0\), the coefficient of
\(A\) in the ratio tends to \(1/(78\nu)\).

The sign pair \(R\) and \(-R\) also shows that the spatial mean of
\(\Pi_s\) has no universal one-sided sign.  A negative mean rules out a
universal pointwise nonnegative rule, and the sign-paired positive mean rules
out a universal pointwise nonpositive rule.  This finite calculation does not
show that either individual field has both signs pointwise, nor does it locate
a sign-changing point.  It does not rule out estimates with additional norms,
time integration, scale integration, small-data conditions, or another
compensating term.

The certificate retains two diagnostic fields.  The originally requested
field is 2D3C.  The intermediate \(x,y,z\)-coordinate-dependent triad has
frequency rank two because its third wavevector is the sum of the first two;
it is invariant along \((0,1,-1)\).  Neither is mislabeled as rank three.

The primary rank-three witness is still a smooth finite Fourier field, not a
blow-up candidate.  It proves no singularity, no arbitrary-data global
regularity statement, and no Clay Millennium conclusion.  `NOT CLAY`.

Ordinary translation path: `LOCAL_DIRECT_NO_DGX`.  DGX used: `false`.
