# R0.42: Canonical stretch transport beyond the direct norm barrier

## Status and conclusion boundary

R0.41 certified the reduced active field and the two normalized transport
fields at the common isotropic radius

\[
 r=\frac{9}{32}=0.28125.
\]

Its next exact test was fixed in advance at

\[
 r_{\mathrm{acc}}=\frac{141}{500}=0.282.
\]

At that point the active fixed point still closes, but the exact one-step
transport norm is

\[
 1.0003750451629853>1.
\]

The excess is not a tail-estimation artifact.  The known degree-80 polynomial
center already contributes (1.0003748969281395); the unknown active
correction contributes only about (1.48\times10^{-7}).  Thus the direct
Neumann inverse for (T_a=(\mathcal L-1)^{-1}\{a,\cdot\}) cannot be repaired
by another small tail improvement in the same norm.

I instead use the exact canonical factorization proved in R0.29.  The two
transport fields are reconstructed from one zero-initial stretch field
\(\phi\).  Its linear operator has an exact output-degree cancellation and a
strictly smaller all-order norm.  Combined with the R0.41 active-tail theorem,
this proves the common radius

\[
 \boxed{r_*=\frac{329}{1000}=0.329}
\tag{0.1}
\]

for the reduced active field (a) and the normalized canonical fields (U,V).
The gain over R0.41 is

\[
 \frac{329/1000}{9/32}=\frac{1316}{1125}\approx1.16978,
\tag{0.2}
\]

and the associated fixed-charge (R=Z^2W) disk grows by

\[
 \left(\frac{1316}{1125}\right)^3
 =\frac{2279122496}{1423828125}\approx1.60070.
\tag{0.3}
\]

This is an all-order theorem for the reduced canonical edge generating
system.  It does not prove global regularity or finite-time blow-up for the
three-dimensional incompressible Navier--Stokes equation.  The failed
(0.33) sufficient bound below is not a singularity result.

## 1. The direct transport barrier is exact

Write a center monomial in degree-charge coordinates as ((i,q)), and an
arbitrary transport input as ((j,s)).  The R0.40 operator

\[
 T_a f=(\mathcal L-1)^{-1}\{a,f\}
\]

has the exact weighted column factor

\[
 \frac{i+j}{i+j-1}\frac{|i(s/j)-q|}{3}.
\tag{1.1}
\]

At the worst endpoint (s/j=2), the degree-80 polynomial column at
(r=0.282) is already

\[
 1.0003748969281395>1.
\tag{1.2}
\]

This is the exact induced weighted-(\ell^1) norm of the polynomial
operator, not a termwise relaxation.  No estimate that leaves the operator,
the isotropic norm, and the one-step Neumann condition unchanged can make
(1.2) smaller than one.

## 2. The canonical factorization changes the inverse problem

R0.29 proved the all-order formal identities

\[
 \{U,V\}=UV,
 \qquad
 \frac UV=\frac ZW e^{-a}.
\tag{2.1}
\]

Define the zero-constant stretch

\[
 \phi=\frac12\log\frac{UV}{ZW}.
\]

Then

\[
 \boxed{
 U=Z e^{\phi-a/2},
 \qquad
 V=W e^{\phi+a/2},
 }
\tag{2.2}
\]

and (\phi) satisfies

\[
 \boxed{
 \mathcal L\phi-\{a,\phi\}
 =\frac12(X-Y)a,
 \qquad \phi_0=0.
 }
\tag{2.3}
\]

Consequently the normalized fields need not be constructed by inverting
(I-T_a).  It is enough to invert

\[
 I-S_a,
 \qquad
 S_a=\mathcal L^{-1}\{a,\cdot\},
\tag{2.4}
\]

solve (2.3), and use the exact exponentials (2.2).  Triangular formal
uniqueness identifies this analytic solution with the canonical formal
series from R0.29.

## 3. Exact all-order stretch norm

On the zero-constant degree-weighted Wiener space, set

\[
 \|f\|_{\mathcal B_r}
 =\sum_{j,s}j|f_{j,s}|r^j.
\tag{3.1}
\]

The log-canonical bracket of monomials ((i,q)) and ((j,s)) has coefficient

\[
 \frac{is-qj}{3}.
\]

After division by the output degree (i+j), multiplication by the output
weight (i+j), and division by the input weight (j), the exact column
factor for (S_a) is

\[
 \boxed{
 \frac{|is-qj|}{3j}
 =\frac{|i(s/j)-q|}{3}.
 }
\tag{3.2}
\]

The output-degree weight cancels the (\mathcal L^{-1}) divisor exactly.
Unlike (1.1), no factor depending on (i) or (j) remains.

For a polynomial center (p), write (x=s/j\in[-1,2]).  Its complete
column is

\[
 C_p(x;r)
 =\sum_{i,q}|p_{i,q}|r^i\frac{|ix-q|}{3}.
\tag{3.3}
\]

This is a positive sum of absolute affine functions of the common variable
(x), hence it is convex.  Both endpoints are actual monomials, so

\[
 \boxed{
 \|S_p\|
 =\max\{C_p(-1;r),C_p(2;r)\}.
 }
\tag{3.4}
\]

Equation (3.4) covers every input degree and every bivariate charge
(-j\le s\le2j).  There is no degree grid or charge cutoff.

## 4. The unknown active correction

Let the active correction (h) be supported in degrees (i>80), with

\[
 \|h\|_{\mathcal B_r}\le\varepsilon,
 \qquad -1\le q\le2i.
\]

At (x=-1), the column factor divided by the active input weight (i) obeys

\[
 \frac{i+q}{3i}\le1.
\tag{4.1}
\]

At (x=2), it obeys

\[
 \frac{2i-q}{3i}
 \le\frac{2i+1}{3i}
 \le\frac{163}{243},
 \qquad i\ge81.
\tag{4.2}
\]

Therefore

\[
 \|S_{p+h}\|
 \le
 \max\left\{
 C_p(-1;r)+\varepsilon,
 C_p(2;r)+\frac{163}{243}\varepsilon
 \right\}.
\tag{4.3}
\]

The right side of (2.3) is also controlled in the same space.  Since

\[
 (X-Y)Z^nW^k=(n-k)Z^nW^k
 =\frac{i-2q}{3}Z^nW^k,
\]

the polynomial part of
(\frac12\mathcal L^{-1}(X-Y)a) has exact norm

\[
 G_p(r)
 =\sum_{i,q}|p_{i,q}|r^i\frac{|i-2q|}{6}.
\tag{4.4}
\]

On the active cone, ( |i-2q|/(6i)\le1/2).  Hence the unknown correction
adds at most (\varepsilon/2).  If the right side of (4.3) is (S<1), then

\[
 \|\phi\|_{\mathcal B_r}
 \le\frac{G_p(r)+\varepsilon/2}{1-S}.
\tag{4.5}
\]

No smallness of (\phi) is required for exponentiation.  A zero-constant
element of (\mathcal B_r) also belongs to the ordinary Wiener algebra, and
its exponential has finite Wiener and degree-weighted norms.  Thus (2.2)
constructs analytic (U,V) on the same open polydisc.

## 5. The preassigned (0.282) acceptance test

At (r=141/500), the R0.41 active fixed point passes.  The old direct
transport bound and the new stretch bound are

\[
 \begin{aligned}
 \|T_a\|_{\mathrm{old}}&\le1.0003750451629853>1,\\
 \|S_a\|_{\mathrm{new}}&\le0.5817058427617202<1.
 \end{aligned}
\tag{5.1}
\]

The corresponding certified stretch norm is

\[
 \|\phi\|_{\mathcal B_r}\le0.7085442657621405.
\tag{5.2}
\]

Thus the exact failure point written into R0.41 becomes a strict acceptance
point without changing the active field or the isotropic radius.

## 6. Exact restart at (329/1000)

I selected the target by an exact millesimal scan after fixing the stretch
theorem: (0.329) passes and the next point (0.330) fails the active-tail
gate.  The scan chooses the reported rational radius; it does not replace the
all-order proof at that radius.

At

\[
 r_*=\frac{329}{1000},
\]

the R0.41 degree-resolved active-tail bound is

\[
 Z_{80}^{\mathrm{deg}}(r_*)
 \approx0.9978571913592614<1.
\tag{6.1}
\]

Choose

\[
 \varepsilon
 =\frac{1-Z_{80}^{\mathrm{deg}}(r_*)}{10^6}
 \approx2.1428086407\times10^{-9}.
\tag{6.2}
\]

The complete degree-80 residual has norm

\[
 Y\approx1.4319669386\times10^{-33}.
\tag{6.3}
\]

The ball-image and Lipschitz bounds are

\[
 Y+Z\varepsilon+3\varepsilon^2
 \approx2.1382170256\times10^{-9}<\varepsilon,
\tag{6.4}
\]

\[
 Z+6\varepsilon
 \approx0.9978572042161132<1.
\tag{6.5}
\]

Banach's theorem therefore gives the unique active correction (h).  The
direct one-step transport estimate is now far outside its range,

\[
 \|T_a\|\le1.2848914513187263>1,
\tag{6.6}
\]

but the canonical stretch estimate is

\[
 \boxed{
 \|S_a\|\le0.7633728925335545<1.
 }
\tag{6.7}
\]

The stretch inverse and right-hand side obey

\[
 \|(I-S_a)^{-1}\|\le4.226058504906515,
\]

\[
 \left\|\frac12\mathcal L^{-1}(X-Y)a\right\|_{\mathcal B_r}
 \le0.3535283011933375,
\]

so

\[
 \|\phi\|_{\mathcal B_r}\le1.4940312839832562.
\tag{6.8}
\]

Equations (2.2) then construct the canonical (U,V) on the same radius.

## 7. Adjacent negative control

At the next millesimal point

\[
 r_{\mathrm{fail}}=\frac{33}{100}=0.33,
\]

the degree-80 polynomial stretch operator is still only

\[
 0.7676483824383634<1.
\tag{7.1}
\]

The present active-tail theorem, however, gives

\[
 Z_{80}^{\mathrm{deg}}(0.33)
 \approx1.0028721508539940>1.
\tag{7.2}
\]

Thus R0.42 moves the proof boundary back to the inherited large-charge active
sector.  Equation (7.2) is a failed sufficient inequality.  It does not show
that the reduced series is singular or nonanalytic at (0.33).

## 8. Formal, finite, and exploratory layers

The following statements are formal and all-order:

1. the canonical identities (2.1)--(2.3);
2. the exact stretch column (3.2);
3. complete-column convexity and the two genuine endpoints (3.4);
4. the active-tail endpoint multipliers (4.1)--(4.2);
5. the right-hand-side estimate (4.4)--(4.5);
6. the active Banach restart and canonical stretch inverse at (329/1000).

The following statements are finite exact implementation checks:

1. 3055 monomial pairs through degree 10 match
   (\mathcal L^{-1}\{a,\cdot\}) exactly;
2. complete input-column scans at degrees (1,2,5,20,81) attain the same
   (x=2) endpoint value;
3. 930 coefficients through transport degree 30 satisfy both exponential
   factorizations in (2.2), with 60 exact divisibility checks;
4. the degree-80 active recurrence and complete degree-160 residual match the
   R0.41 digests.

The exact radius scan is a finite selection protocol over rational radii.
Every accepted radius is then certified by all-order degree and charge
inequalities.  The actual nearest complex singularity remains conjectural.

## 9. Value and next question

The structural result is stronger than the radius increase.  The exact
one-step norm barrier for (T_a) is bypassed through an equivalent canonical
factorization, not weakened by an unjustified cancellation.  The operator
(\mathcal L^{-1}\{a,\cdot\}) has an exact degree cancellation, so one convex
two-endpoint formula controls every input degree and charge.

For the three-dimensional Navier--Stokes Millennium Problem, the direct value
remains limited.  No theorem here transfers the reduced canonical edge system
to arbitrary critical interactions of the full PDE.  The result is rigorous
progress in a derived analytic model, not a partial solution of the global
regularity problem.

The next exact boundary is the inherited large-charge active sector at
(0.33).  R0.43 should first decompose that analytic sector and determine
whether its (1.002872) excess comes from a removable separation of common
charge variables.  If it does not, the next alternative is a positive
anisotropic weight that preserves convolution and the canonical
factorization.

## Reproduction

Run `research/edge_stretch_transport_audit.py` from the repository root.  The
formal certificate pins the clean source commit and the SHA-256 digest of the
R0.41 certificate.  The computation uses exact GMP rationals, an append-only
progress log, and an independent process-tree resource log.  It has no random
seed, GPU dependency, or floating-point threshold decision.

## References

1. R0.29, *Canonical transport reduction and the infinite charge ladder*.
2. R0.37, *A weighted-Wiener restart beyond the R0.31 radius*.
3. R0.39, *Charge-resolved tail and transport bounds*.
4. R0.40, *Exact two-endpoint transport and a radius restart*.
5. R0.41, *A degree-resolved common-endpoint theorem for the active tail*.
