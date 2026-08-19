# R0.41: A degree-resolved common-endpoint theorem for the active tail

## Status and scope

This note proves an all-order estimate for the derivative of the reduced
canonical edge generating map.  It improves the R0.39 active-tail bound by
retaining the common input slope inside each fixed-charge column.  Together
with the R0.40 two-endpoint transport theorem, it gives an exact restart at

\[
 r_* = \frac{9}{32}=0.28125.
\]

The theorem covers every input charge and every input degree above the
degree-80 polynomial center.  Finite exact column scans are used only to
regress the implementation.  Nothing here proves global regularity or
finite-time blow-up for the full three-dimensional incompressible
Navier--Stokes equation.

## 1. Exact fixed-charge column

Let a base monomial have degree and charge \((i,q)\), and let the tail input
have degree and charge \((j,s)\).  On the active cone,

\[
 i\ge1,
 \qquad -1\le q\le2i,
 \qquad j>80,
 \qquad -1\le s\le2j,
 \qquad j+s\equiv0\pmod3.
\]

For \(s+q\ne0\), the exact derivative coefficient inherited from R0.39 is

\[
 \gamma_{i,q;j,s}
 =
 \frac{(is-qj)(s-q)}
 {3(s+q)(i+j-1)}.
\tag{1.1}
\]

After dividing by the weighted input monomial, the absolute column factor is

\[
 \frac{i+j}{i+j-1}
 \left|\frac{is}{j}-q\right|
 \frac{|s-q|}{3|s+q|}.
\tag{1.2}
\]

For a fixed input charge \(s\), let \(J_s\) be the smallest admissible tail
degree:

\[
 J_s>80,
 \qquad J_s\ge\left\lceil\frac{s}{2}\right\rceil,
 \qquad J_s+s\equiv0\pmod3.
\tag{1.3}
\]

R0.39 replaced the middle factor in (1.2) by

\[
 \left|\frac{is}{j}-q\right|
 \le |q|+\frac{i|s|}{j}
 \le |q|+\frac{i|s|}{J_s}.
\tag{1.4}
\]

The two triangle inequalities in (1.4) are valid, but they erase the fact
that all center monomials see the same input slope \(s/j\).  At the R0.40
failure probe \(257/1000\), this termwise loss raises the certified tail bound
to approximately \(1.0002561524\), even though the exact degree-81 column is
far below one.

## 2. Common-endpoint theorem

Fix an input charge

\[
 2\le s\le240
\]

and write

\[
 x=\frac{s}{j}.
\]

Every admissible \(j\ge J_s\) gives

\[
 0\le x\le\frac{s}{J_s}.
\tag{2.1}
\]

For a degree-80 center

\[
 p_{80}=\sum_{i,q}p_{i,q}Z^nW^k,
\]

define the complete fixed-charge core

\[
 H_s(x;r)
 =
 \sum_{i,q}
 |p_{i,q}|r^i
 |ix-q|
 \frac{|s-q|}{3|s+q|}.
\tag{2.2}
\]

The important order of operations is that the complete center sum is formed
before taking a slope maximum.  Every summand in (2.2) is a positive multiple
of an absolute affine function of \(x\).  Hence \(H_s\) is convex and

\[
 \sup_{0\le x\le s/J_s}H_s(x;r)
 =
 \max\left\{H_s(0;r),H_s\left(\frac{s}{J_s};r\right)\right\}.
\tag{2.3}
\]

The remaining degree prefactor in (1.2) obeys, for every \(i\ge1\) and
\(j\ge J_s\),

\[
 \frac{i+j}{i+j-1}
 =1+\frac1{i+j-1}
 \le1+\frac1j
 \le\frac{J_s+1}{J_s}.
\tag{2.4}
\]

Combining (2.3) and (2.4) gives the all-order fixed-charge column

\[
 \boxed{
 B_s(r)
 =
 \frac{J_s+1}{J_s}
 \max\left\{H_s(0;r),H_s\left(\frac{s}{J_s};r\right)\right\}.
 }
\tag{2.5}
\]

There is no degree grid or degree truncation in (2.5).  The interval
convexity covers every real slope between the endpoints, and therefore every
admissible discrete degree in the congruence class.

The charges \(s=-1,0,1\) contain the only possible cases \(s+q=0\); their
already proved R0.39 all-order columns are retained without modification.
For \(s\ge241\), the R0.39 analytic large-charge sector is also retained.
Consequently,

\[
 Z^{\mathrm{deg}}_{80}(r)
 =
 \max\left(
 \max_{-1\le s\le240}B_s(r),
 B_{s\ge241}(r)
 \right)
\tag{2.6}
\]

controls every active tail monomial of every degree \(j>80\).

## 3. What happens to the former worst charge

At the new target radius \(r=9/32\), the former worst charge remains useful
as a diagnostic.  For \(s=162\),

\[
 J_{162}=81,
 \qquad
 \frac{J_{162}+1}{J_{162}}=\frac{82}{81}.
\]

The two complete core endpoints are

\[
 H_{162}(0;r)\approx0.3731276009,
 \qquad
 H_{162}(2;r)\approx0.5788078415,
\]

and therefore

\[
 B_{162}(r)\approx0.5859536173.
\tag{3.1}
\]

The exact degree-81 column is slightly smaller,

\[
 C_{162}(81;r)\approx0.5858946081.
\tag{3.2}
\]

Exact scans at

\[
 j=81,84,87,90,99,120,162,243,324,486,810,1620
\]

all lie below (3.1).  They decrease and later rise toward the infinite-degree
endpoint; this nonmonotonicity is precisely why the theorem uses convex
common endpoints rather than claiming degree monotonicity.  These twelve
columns are finite implementation regressions only.  Equation (2.5) is the
all-order argument.

At \(r=9/32\), the largest finite charge column is no longer \(s=162\).
The global active-tail bound is instead the inherited analytic sector
\(s\ge241\):

\[
 Z^{\mathrm{deg}}_{80}(9/32)
 \approx0.7785423316172445<1.
\tag{3.3}
\]

## 4. The preassigned acceptance test

R0.40 fixed

\[
 r_{\mathrm{acc}}=\frac{257}{1000}=0.257
\]

as the first acceptance test for R0.41.  At this radius, the old R0.39
termwise tail bound is

\[
 Z^{\mathrm{old}}_{80}(r_{\mathrm{acc}})
 \approx1.0002561524370209>1,
\]

whereas the degree-resolved theorem gives

\[
 Z^{\mathrm{deg}}_{80}(r_{\mathrm{acc}})
 \approx0.6804858814101491<1.
\tag{4.1}
\]

The exact R0.40 transport bound, including the new tail-ball contribution,
is approximately

\[
 0.8672869049434062<1.
\tag{4.2}
\]

Thus the preassigned acceptance test passes both the active-tail and
transport gates.

## 5. Exact restart at \(9/32\)

At the target radius, the degree-80 recurrence has 2161 nonzero center terms.
Its complete residual has 6345 nonzero terms in degrees 81 through 160 and

\[
 Y=\|F(p_{80})\|_r
 \approx3.8850013583\times10^{-39}.
\tag{5.1}
\]

Let

\[
 m=1-Z^{\mathrm{deg}}_{80}(r)
\]

and choose the exact rational ball radius

\[
 \varepsilon=\frac{m}{10^6}
 \approx2.2145766838\times10^{-7}.
\tag{5.2}
\]

The ball-image upper bound is

\[
 Y+Z^{\mathrm{deg}}_{80}(r)\varepsilon+3\varepsilon^2
 \approx1.7241431663\times10^{-7}<\varepsilon,
\tag{5.3}
\]

and the ball Lipschitz bound is

\[
 Z^{\mathrm{deg}}_{80}(r)+6\varepsilon
 \approx0.7785436603632548<1.
\tag{5.4}
\]

Banach's theorem therefore gives a unique active correction supported in
degrees greater than 80.  Triangular formal uniqueness identifies it with
the canonical active formal series.

The R0.40 exact two-endpoint transport theorem gives, including the unknown
tail correction,

\[
 \|T_a\|
 \le0.9962112031995047<1.
\tag{5.5}
\]

The normalized fields are therefore constructed at the same radius.  Relative
to R0.40,

\[
 \frac{9/32}{32/125}
 =\frac{1125}{1024}
 \approx1.0986328125,
\tag{5.6}
\]

and the fixed-charge radius, which scales cubically, grows by

\[
 \left(\frac{1125}{1024}\right)^3
 =\frac{1423828125}{1073741824}
 \approx1.3260432752.
\tag{5.7}
\]

## 6. Adjacent negative control

At the adjacent rational probe

\[
 r_{\mathrm{fail}}=\frac{141}{500}=0.282,
\]

the new active-tail theorem still gives

\[
 Z^{\mathrm{deg}}_{80}(r_{\mathrm{fail}})
 \approx0.7817068331248664<1,
\]

and the active fixed-point ball still closes.  The exact two-endpoint
transport bound, however, becomes

\[
 1.0003750451629853>1.
\tag{6.1}
\]

The sufficient proof therefore stops at this probe only because of the
present transport estimate.  Equation (6.1) is not evidence that the true
series loses analyticity at \(0.282\), and it is not a singularity theorem.

## 7. Formal, finite, and conjectural layers

The following statements are formal and all-order:

1. the exact derivative coefficient (1.1);
2. common-slope convexity (2.3) for every \(2\le s\le240\);
3. the degree prefactor bound (2.4) for every \(j\ge J_s\);
4. the inherited exceptional and large-charge sectors;
5. the Banach restart and transport inverse at \(9/32\).

The following statements are finite exact checks:

1. the degree-80 recurrence and degree-160 residual;
2. 2209 active-derivative monomial coefficient regressions through degree 10;
3. the degree-81 full column scan;
4. twelve exact columns at charge 162;
5. 1195 exact columns covering every charge from 2 through 240 at five
   admissible degree offsets.

The location of the actual nearest complex singularity remains conjectural.
Neither the R0.32 finite Padé candidates nor the failed \(0.282\) sufficient
bound identifies such a singularity.

## 8. Value and next question

R0.41 removes the largest loss in the active-tail theorem without changing
the norm or introducing a finite degree cutoff.  Its structural content is
that the input slope must remain common across the complete center column.
The certified common radius increases from \(0.256\) to \(0.28125\), and the
active-tail bottleneck is replaced by the exact transport endpoint
\(x=2\).

For the Millennium problem, the direct value remains limited.  No proved
estimate presently transfers this reduced edge-series analyticity to all
three-dimensional critical Navier--Stokes interactions.  The result is a
rigorous theorem for a derived generating system, not a partial regularity
theorem for the full PDE.

The next mathematical question is whether the \(x=2\) transport endpoint can
retain an additional correlation with the active-tail fixed point, or whether
a different anisotropic weight is required.  Any next step must keep an
all-order degree and charge closure and use \(0.282\) as the first acceptance
test.

## Reproduction

Run `research/edge_degree_resolved_tail_audit.py` from the repository root.
The formal certificate pins its clean source commit and the SHA-256 digest of
the R0.40 input certificate.  The computation uses exact GMP rationals, an
append-only progress log, and a process-tree resource log.  It has no random
seed, GPU dependency, or floating-point sign decision.

## References

1. R0.29, *Canonical transport reduction and the infinite charge ladder*.
2. R0.37, *A weighted-Wiener restart beyond the R0.31 radius*.
3. R0.38, *A tail-aware Newton restart beyond the R0.37 radius*.
4. R0.39, *Charge-resolved tail and transport bounds*.
5. R0.40, *Exact two-endpoint transport and a radius restart*.
