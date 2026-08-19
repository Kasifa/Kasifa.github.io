# An exact charge--degree lattice endpoint theorem

## R0.47 research note

### Abstract

R0.46 certified the reduced canonical edge generating system at radius

\[
r=0.376
\]

in the zero/nonzero-charge two-block norm with zero-charge weight
$\kappa=3/4$.  Its inherited large-positive-charge estimate failed at
$r=0.377$, but that estimate separately maximized a degree factor, a charge
ratio, and the common input slope.  Those extrema do not in general occur in
one admissible monomial.

This note retains the exact charge--degree lattice.  For every fixed positive
input charge $s$, let $J_s$ be the minimum admissible tail degree.  The exact
degree factor is kept inside the complete positive column sum and bounded by
its value at $J_s$.  The remaining expression is convex in the common slope
$x=s/j$, so every degree $j\ge J_s$ is controlled by two exact endpoints.

For $2\le s<241$, this gives 239 fixed-charge all-degree theorems.  For
$s\ge241$, the minimum-degree lattice has exact even and odd branches.  After
the substitution $y=1/s$, both branches are rational functions.  Exact
degree-318 Bernstein certificates prove that the even derivative is positive
on $[0,1/242]$ and that the odd derivative is negative on $[0,1/241]$.
Consequently every large integer charge is covered without a charge grid.

At

\[
r=\frac{94233}{250000}=0.376932,
\]

the complete induced tail bound is

\[
0.9999973490826196656<1.
\]

The true limiting column is $s=162,j=81$, not the large-charge sector.  At the
adjacent millionth $r=0.376933$, the same exact column is

\[
1.0000026584572409359>1.
\]

Thus the present sufficient inequality fails there in this specific induced
two-block weighted-$\ell^1$ norm.  This is not a singularity theorem and has
no direct implication for three-dimensional Navier--Stokes regularity.

---

## 1. Exact column formula

For a monomial $Z^mW^n$, write

\[
i=m+n,\qquad q=2n-m
\]

for its total degree and charge.  The pinned center $p_{80}$ contains 2,161
exact rational coefficients and has active support $q\ge-1$.  Put

\[
c_{i,q}(r)=|a_{i,q}|r^i.
\]

For a positive input charge $s$ and a tail degree $j>80$, every output charge
$s+q$ is positive.  The contribution of a center term $(i,q)$ to the induced
column is

\[
c_{i,q}(r)
\frac{i+j}{i+j-1}
\frac{s-q}{3(s+q)}
\left|i\frac{s}{j}-q\right|.
\tag{1.1}
\]

All factors in (1.1) are nonnegative.  No coefficient-sign cancellation is
used anywhere in the proof.

The charge--degree lattice is obtained by solving

\[
m=\frac{2j-s}{3},\qquad n=\frac{j+s}{3}.
\tag{1.2}
\]

Thus admissibility requires $m,n\ge0$, integrality, and $j>80$.  Let $J_s$
denote the least such degree.

---

## 2. Fixed-charge endpoint theorem

For each center degree $i$, define

\[
d_i(j)=\frac{i+j}{i+j-1}.
\]

This function decreases in $j$.  Hence, for every $j\ge J_s$,

\[
d_i(j)\le d_i(J_s).
\tag{2.1}
\]

Keep the right-hand side of (2.1) inside the complete sum and set $x=s/j$.
The resulting core is

\[
H_{r,s}(x)
=\sum_{i,q}c_{i,q}(r)d_i(J_s)
\frac{s-q}{3(s+q)}|ix-q|.
\tag{2.2}
\]

Every summand in (2.2) is the absolute value of an affine function multiplied
by a nonnegative coefficient.  Therefore $H_{r,s}$ is convex on

\[
0\le x\le \frac{s}{J_s}.
\]

The complete fixed-charge theorem is consequently

\[
\sup_{j\ge J_s}\mathcal C_r(j,s)
\le
\max\left\{H_{r,s}(0),H_{r,s}\!\left(\frac{s}{J_s}\right)\right\}.
\tag{2.3}
\]

Equation (2.3) covers all degrees for one fixed charge.  Enumerating the 239
charges $2\le s<241$ is therefore a finite list of analytic all-degree
theorems, not a finite list of tail degrees.

At the target radius, the largest of these 239 bounds occurs at $s=162$.
Here $J_{162}=81$ and $s/J_s=2$, so the active endpoint is an actual input
monomial rather than only a limit:

\[
\max_{2\le s<241}\sup_{j\ge J_s}\mathcal C_r(j,s)
=\mathcal C_r(81,162)
=0.9999973490826196656\ldots.
\tag{2.4}
\]

---

## 3. Exact large-charge parity branches

For $s\ge241$, the lattice minimum has the closed form

\[
J_s=
\begin{cases}
s/2,&s\text{ even},\\[2mm]
(s+3)/2,&s\text{ odd}.
\end{cases}
\tag{3.1}
\]

The endpoint $x=0$ is bounded uniformly by

\[
0.57595048748944892203\ldots,
\]

so only the minimum-degree endpoint can be active.

### 3.1 Even branch

For even $s$, put $y=1/s$.  Since $J_s=s/2$ and $x=2$, the endpoint is

\[
E_{\mathrm e}(y)
=\sum_{i,q}c_{i,q}(r)
\frac{1+2iy}{1+2(i-1)y}
\frac{1-qy}{1+qy}
\frac{|2i-q|}{3}.
\tag{3.2}
\]

This is an exact rational function with a positive denominator on
$0\le y\le1/242$.  After clearing that denominator, the derivative numerator
has degree 318.  All 319 exact Bernstein coefficients on the complete
interval are strictly positive; the smallest is

\[
1.4232222954764169712\ldots>0.
\]

Thus $E_{\mathrm e}'(y)>0$ everywhere on the interval.  The maximum over all
even $s\ge242$ is attained at $s=242,j=121$:

\[
E_{\mathrm e}(1/242)
=0.99713708460906863273\ldots.
\tag{3.3}
\]

### 3.2 Odd branch

For odd $s$, $J_s=(s+3)/2$ and $x=2/(1+3y)$.  Define

\[
A_{i,q}(y)=
\begin{cases}
2i-q-3qy,&q<2i,\\
6iy,&q=2i.
\end{cases}
\]

The exact endpoint function is

\[
E_{\mathrm o}(y)
=\sum_{i,q}c_{i,q}(r)
\frac{1+(2i+3)y}{1+(2i+1)y}
\frac{1-qy}{1+qy}
\frac{A_{i,q}(y)}{3(1+3y)}.
\tag{3.4}
\]

For $q<2i$, the support congruence gives $q\le2i-3$, so the displayed branch
of the absolute value is positive throughout $0\le y\le1/241$.  The
denominator in (3.4) is positive.  After clearing it, all 319 degree-318
Bernstein coefficients of the *negative* derivative are strictly positive;
the smallest is

\[
0.99259295876419492923\ldots>0.
\]

Therefore $E_{\mathrm o}'(y)<0$.  Every odd $s\ge241$ is bounded by the
$y=0$ limit

\[
E_{\mathrm o}(0)
=0.99129357597248957141\ldots.
\tag{3.5}
\]

At the first odd charge, $E_{\mathrm o}(1/241)=0.9870989951\ldots$.

Equations (3.2)--(3.5) are continuous-interval proofs.  The finite parity
samples in the journal figure are presentation checks only.

---

## 4. Exhaustive all-order theorem

### Theorem 4.1

For the pinned degree-80 center, cutoff $S=241$, radius
$r=94233/250000$, and zero-charge weight $\kappa=3/4$, every strict-tail input
monomial belongs to one of five disjoint sectors.  Their exact upper bounds
are

\[
\begin{array}{c|c}
\text{input charge sector}&\text{bound}\\ \hline
s=0&0.76958524922808429955\\
s=-1&0.98411345493868264249\\
s=1&0.20360197546947024726\\
2\le s<241&0.9999973490826196656\\
s\ge241&0.99713708460906863273.
\end{array}
\]

Consequently

\[
\boxed{
\|D\Phi(p_{80})\|_{r,3/4}
\le0.9999973490826196656<1.}
\tag{4.1}
\]

The maximum in (4.1) is the exact $s=162,j=81$ column.

#### Proof

The sectors $s=0$, $s=-1$, $s=1$, $2\le s<241$, and $s\ge241$ are
disjoint and exhaustive.  R0.46 supplies the first three all-order bounds.
Equation (2.3) supplies all 239 fixed positive-charge bounds.  The parity
derivative certificates in Section 3 supply the infinite large-charge bound.
Their exact maximum is (2.4).  The two output blocks are combined inside each
input column before the column supremum is taken.  This gives the induced
weighted-$\ell^1$ estimate (4.1).  □

The old separated R0.46 estimate at the same target radius is

\[
1.0026775745912701679>1.
\]

Thus preserving the lattice relation changes the threshold decision; this is
not merely a smaller display value.

---

## 5. Fixed-point and canonical-stretch gates

The contraction margin at the target is

\[
\delta
=1-0.9999973490826196656
=2.6509173803344006173\times10^{-6}.
\]

With the pinned ball divisor $10^6$, the exact two-block ball radius is

\[
\rho=2.6509173803344006173\times10^{-12}.
\]

The complete residual and the two fixed-point gates satisfy

\[
\begin{aligned}
\|R_{80}\|_{r,3/4}
&=1.2005979364487601672\times10^{-30},\\
\text{mapping upper bound}
&=2.6509103530089225287\times10^{-12}<\rho,\\
\text{Lipschitz upper bound}
&=0.99999734911089611766<1.
\end{aligned}
\]

The independent canonical-stretch operator bound is

\[
0.99129357597486048791<1.
\]

Hence the reduced fixed point and the inherited regular canonical fields close
at the common radius $0.376932$.  The obsolete direct-transport diagnostic is
$1.6312284446\ldots>1$ and is not the construction gate after the regular
decomposition.

---

## 6. Adjacent exact negative control

At

\[
r=\frac{376933}{10^6},
\]

the large-charge lattice bound still passes, and the canonical-stretch bound
is $0.99129886880468265147<1$.  Nevertheless the actual fixed-charge column
has

\[
\boxed{
\mathcal C_r(81,162)
=1.0000026584572409359>1.}
\tag{6.1}
\]

The complete tail maximum equals (6.1).  This is stronger than a coarse-bound
failure: the present induced norm really assigns a column ratio above one to
that monomial.  It is still only a failure of this sufficient contraction
test.  It does not show that a nonlinear solution is singular, that every
equivalent or anisotropic norm fails, or that the reduced system lacks an
analytic continuation.

The two radii give a rigorous rational bracket for the current norm barrier:

\[
0.376932<r_{\mathrm{barrier}}<0.376933.
\]

No decimal approximation is used to decide either inequality.

---

## 7. Computation, monitoring, and provenance

The formal audit reconstructs 2,161 center coefficients and 6,345 exact
residual coefficients.  It checks 30 exact finite columns from ten selected
charges and three admissible degree offsets.  Every finite column lies below
its analytic sector theorem.  These columns are implementation regressions;
they do not prove the infinite tail.

All 39 formal checks pass in GMP rational arithmetic.  The monitored run took
68.383462 seconds of scientific wall time and 68.516376 seconds end to end,
with 458 process-tree samples.  Maximum observed CPU was 100.0% and maximum
resident memory was 56.625 MiB.  No GPU, randomness, floating-point threshold
decision, tail-degree grid, or large-charge grid was used.

The certificate SHA-256 is

```text
e45bc20ddeab9efde83dafefc84514df0260f8831c102c4621f0fdcd43dea6c9
```

and the pinned source commit is

```text
709ecb5f20b7321079ba114a57bf20b77ca7646a
```

---

## 8. Research value and limits

R0.47 establishes a reusable reduction principle: when discrete constraints
couple an input parameter to its minimum degree, separating their extrema can
create a false obstruction.  Retaining the exact lattice can turn an infinite
integer family into a small number of rational branches whose monotonicity is
certified on complete intervals.

It also identifies the next obstruction sharply.  The apparent large-charge
failure at $0.377$ was an artifact of separated maximization.  After removing
it, the genuine $s=162,j=81$ column becomes limiting, and the adjacent
millionth fails in the current norm.

The result remains a theorem for a reduced bivariate generating system.  It
does not control the complete three-dimensional Navier--Stokes velocity field
in a scale-critical space, does not cover arbitrary smooth initial data, and
does not include all Fourier geometry of the PDE.  It neither proves global
regularity nor constructs finite-time blow-up.

---

## 9. Next falsifiable step

R0.48 should first turn the millionth bracket into a sharp theorem for the
current norm.  The active $s=162,j=81$ column is a finite positive polynomial
in $r$ with rational coefficients.  A Sturm sequence or an exact rational
root-isolation certificate can prove uniqueness of its threshold root and
locate it to a much smaller interval.  Simultaneously, every competing sector
must remain below it on that interval.

The acceptance conditions are:

1. construct the exact threshold polynomial for the $s=162,j=81$ column and
   certify a unique root in $(0.376932,0.376933)$;
2. prove that all 238 other fixed positive charges and the four remaining
   sectors are strictly smaller throughout the isolating interval;
3. use exact rational interval or Sturm arithmetic, with no floating-point
   root decision;
4. publish the root interval, active-column gap, source hash, monitoring logs,
   and negative controls;
5. after the current norm is sharply closed, test a charge-multiplicative
   anisotropic weight as the next construction rather than attempting another
   scalar tightening of the same column formula.

This step will not by itself advance the radius, but it will separate a sharp
norm barrier from an implementation-dependent decimal choice and provide the
correct baseline for the next norm design.
