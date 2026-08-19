# Figure R0.51-1

**A fixed affine charge weight gives a strict threshold improvement.**
(a) Exact-rational presentation samples of the conservative root-box gap
between the true `(j,s)=(81,162)` column at the left radius endpoint and the
`s=0` column at the right endpoint, with `c=19939/25000`.  The certified
choice `lambda=7653/10000` lies on the active-column side of the nearby
constraint switch and has exact gap approximately `1.7808194822e-5`.  The
sampled sign change only illustrates where `s=0` takes over; it is not a
global optimization certificate in `(c,lambda)`.  (b) Strict lower
threshold-radius gains at the three successive norm refinements, each
measured against the preceding certified upper root.  R0.51 improves on the
globally optimized R0.50 multiplicative family by a factor greater than
`1.0000121743210599539`, or about `12.174` ppm.  The corresponding `r^3`
factor exceeds `1.0000365234078239459`.  (c) All 243 exact all-order
competitor gaps on the R0.51 root box.  The nearest competitor is now `s=0`,
with gap approximately `1.7808194822e-5`; the next is `s=164,j=82`, with gap
approximately `1.4527645259e-4`.

The fixed weight is
`omega_s=c^s(1+lambda|s|)`.  Its submultiplicativity follows from the triangle
inequality.  Exact convex endpoints cover `2<=s<241`; a coefficientwise
affine envelope plus parity/Bernstein certificates covers every `s>=241`;
and separate exact arguments cover `s=0,-1,1`.  All root signs, Sturm counts,
fixed-point inequalities, and competitor comparisons use GMP rational
arithmetic.  The result concerns the reduced canonical edge generating
system and one fixed norm.  It does not prove global optimality in the full
affine family, does not provide a critical-space bridge for arbitrary
three-dimensional velocity fields, and does not prove or disprove
three-dimensional Navier--Stokes regularity.
