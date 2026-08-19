# A fixed affine charge weight beyond the optimal multiplicative character

## R0.51 research note

### Abstract

R0.50 proved that the multiplicative charge characters

\[
\omega_s=c^s,
\qquad c>0,
\]

have a unique global optimum in the reduced canonical edge generating
system.  The improvement over the simple value \(c=4/5\) was only about
\(3.061\) parts per million.  R0.51 enlarges the norm to the genuinely
nonmultiplicative but submultiplicative family

\[
\omega_s(c,\lambda)=c^s(1+\lambda |s|),
\qquad c>0,\quad \lambda\ge0.
\]

The elementary inequality

\[
1+\lambda|a+b|
\le 1+\lambda|a|+\lambda|b|
\le(1+\lambda|a|)(1+\lambda|b|)
\]

shows that the Banach-algebra constant remains one for every integer charge.
For positive input charge \(s\ge2\) and every center charge \(q\ge-1\), the
weight ratio compresses to

\[
\frac{\omega_{s+q}}{\omega_s}
=c^q(1+\alpha_s q),
\qquad
\alpha_s=\frac{\lambda}{1+\lambda s}.
\]

This exact formula explains the gain and its limitation.  Increasing
\(\lambda\) improves the previously active positive-charge column, but the
\(s=0\) sector grows linearly and eventually becomes the nearest
competitor.

A floating-point exploration locates a two-constraint candidate near

\[
(r,c,\lambda)
\approx(0.3826244718485988,
0.7975595104326214,
0.7653268804061601),
\]

where the \((j,s)=(81,162)\) column and the zero-charge sector are both near
one.  This candidate is only exploratory; it is not used for an exact sign
decision or claimed to be the global optimum of the two-parameter family.

The formal theorem fixes the nearby rational weight

\[
c=\frac{19939}{25000}=0.79756,
\qquad
\lambda=\frac{7653}{10000}=0.7653.
\]

For this norm, the active degree-80 polynomial has one positive threshold
root, isolated exactly by

\[
0.382624471846022<r_*<0.382624471846023.
\]

An 81-element Sturm chain has endpoint variation counts \(40\) and \(39\).
All 243 competing columns and all-order sectors remain strictly below the
active column on the root box.  The nearest competitor is now \(s=0\), with
exact positive gap approximately

\[
1.7808194822375234792\times10^{-5}.
\]

Relative to the R0.50 global-optimum upper endpoint, the R0.51 lower root
improves by a factor greater than

\[
1.0000121743210599539,
\]

or about \(12.174\) parts per million.  The corresponding fixed-charge
radius \(r^3\) improves by a factor greater than

\[
1.0000365234078239459.
\]

This is a sharp all-order theorem for one fixed affine charge norm in the
reduced generating system.  It does not prove global optimality in the full
\((c,\lambda)\) family, does not build a critical-space bridge to arbitrary
three-dimensional velocity fields, and does not prove or disprove
three-dimensional Navier--Stokes regularity.

---

## 1. The affine weight and its algebra constant

Let the charge index range over all integers.  Define

\[
\omega_s(c,\lambda)=c^s(1+\lambda|s|).
\tag{1.1}
\]

The multiplicative factor is exact:

\[
c^{a+b}=c^ac^b.
\]

For the affine factor, the triangle inequality and \(\lambda\ge0\) give

\[
1+\lambda|a+b|
\le1+\lambda|a|+\lambda|b|
\le1+\lambda|a|+\lambda|b|+\lambda^2|a||b|.
\tag{1.2}
\]

Therefore

\[
\omega_{a+b}(c,\lambda)
\le\omega_a(c,\lambda)\omega_b(c,\lambda).
\tag{1.3}
\]

The algebra constant is exactly one.  This is a formal all-charge statement,
not a finite verification.

For a positive input charge \(s\ge2\), the center charges in the degree-80
construction satisfy \(q\ge-1\), so \(s+q>0\).  Hence

\[
\frac{\omega_{s+q}}{\omega_s}
=c^q\frac{1+\lambda(s+q)}{1+\lambda s}
=c^q(1+\alpha_s q),
\qquad
\alpha_s=\frac{\lambda}{1+\lambda s}.
\tag{1.4}
\]

Formula (1.4) is the main reduction.  It replaces the absolute-value ratio
by an affine function of the center charge \(q\) throughout every positive
input sector.

---

## 2. Why a finite constraint switch is expected

For the R0.50 active input \(s=162\), the affine ratio in (1.4) changes the
relative cost of positive and negative center charges.  The exact center has
charge support from \(-1\) through \(157\), and the selected value of
\(\lambda\) reduces the active-column obstruction compared with the best
pure multiplicative character.

The zero input is structurally different:

\[
\frac{\omega_q}{\omega_0}=c^q(1+\lambda|q|).
\tag{2.1}
\]

Its value grows linearly in \(\lambda\) coefficient by coefficient.  Thus an
indefinite increase of \(\lambda\) cannot improve all sectors at once.  The
formal certificate confirms the predicted switch: at the R0.51 root box the
nearest competitor is \(s=0\), not \(s=164\).

This identifies an actual Pareto boundary inside the affine family.  The
gain is not a consequence of making every column smaller; it comes from
balancing two different exact columns.

---

## 3. Exploratory three-variable candidate

The exploratory script evaluates the finite degree-80 construction with
high-precision floating arithmetic and follows the branch on which the
active \((s,j)=(162,81)\) column and the zero sector are both close to one.
It finds

\[
r\approx0.3826244718485988,
\tag{3.1}
\]

\[
c\approx0.7975595104326214,
\qquad
\lambda\approx0.7653268804061601.
\tag{3.2}
\]

The neighboring \(s=164\) column is approximately

\[
0.99985472349.
\]

These decimals are used only to choose a nearby rational norm and to design
the formal proof.  They do not certify a KKT point, uniqueness, or global
optimality in \((c,\lambda)\).  The exact theorem below deliberately freezes
both parameters.

---

## 4. The fixed rational norm

Fix

\[
c_0=\frac{19939}{25000},
\qquad
\lambda_0=\frac{7653}{10000}.
\tag{4.1}
\]

The degree-80 center contains 2161 monomials and was generated by 1,113,168
ordered recurrence interactions.  Its exact coefficient digest is

```text
056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7
```

For the true input \((j,s)=(81,162)\), exact charge collection gives a
univariate polynomial

\[
A_{c_0,\lambda_0}(r)=\sum_{i=0}^{80}a_ir^i.
\tag{4.2}
\]

All 80 nonconstant coefficients are strictly positive.  The coefficient
digest is

```text
04f270d1ecfebe8c292bb09a3bb2c69bf6dd9e2511a103dfbb2fedd974f75744
```

After primitive integer normalization, the threshold polynomial has digest

```text
efbfc1e247a4c74ab86e750e6800aa3c4e5fbc39860f0a9d77e80bdeb0d85f3f
```

Positivity of the nonconstant coefficients makes the active column strictly
increasing for \(r>0\).  It therefore has at most one positive threshold
root.

---

## 5. Exact root isolation and sharpness

Let \(P(r)\) be the primitive threshold polynomial corresponding to

\[
A_{c_0,\lambda_0}(r)-1=0.
\]

At the rational endpoints

\[
r_L=0.382624471846022,
\qquad
r_U=0.382624471846023,
\tag{5.1}
\]

exact GMP evaluation gives

\[
P(r_L)\approx-3.8188783670756237207\times10^{-15},
\tag{5.2}
\]

\[
P(r_U)\approx9.7773518382998995761\times10^{-16}.
\tag{5.3}
\]

The decimals in (5.2)--(5.3) display exact rational signs.  The Sturm
sequence has 81 members, with

\[
V(r_L)=40,
\qquad
V(r_U)=39.
\tag{5.4}
\]

Thus there is exactly one root in \((r_L,r_U)\).  Together with positivity
of the active coefficients, this proves the sharp trichotomy for the fixed
norm: the active column is below one for \(0<r<r_*\), equals one at \(r_*\),
and is above one for \(r>r_*\).

---

## 6. All-order competitor dominance

The root theorem becomes an induced-norm theorem only after every competing
input is controlled on the full root box.  The certificate covers 243
objects:

- all other fixed positive charges below the analytic cutoff;
- the inactive endpoint of the active charge;
- the special sectors \(s=-1,0,1\);
- all positive charges \(s\ge241\) and every admissible tail degree.

The exact competitor-record digest is

```text
1e740cb7e4fdc82567872e86dd5d8dad0326b46eb8b07aabfb778f8e7c3e9ea1
```

The active lower bound at \(r_L\) is approximately

\[
0.99999999999999618112.
\]

The closest competitor is the zero sector:

\[
C_{s=0}^{\rm upper}(r_U)
=0.99998219180517380589,
\tag{6.1}
\]

and the exact dominance gap satisfies

\[
C_{\rm active}^{\rm lower}(r_L)
-C_{s=0}^{\rm upper}(r_U)
=1.7808194822375234792\times10^{-5}>0.
\tag{6.2}
\]

The next competitor is \((s,j)=(164,82)\), with gap

\[
1.4527645258515414044\times10^{-4}.
\tag{6.3}
\]

For every \(s\ge241\), the parity-resolved continuous envelope gives

\[
C_s(r_U)\le0.99813502986433707146.
\tag{6.4}
\]

Its largest source is the even endpoint \((s,j)=(242,121)\).  The proof
uses exact Bernstein signs on the complete inverse-charge intervals, not a
large-charge grid.

The \(s=-1\) sector requires a separate all-degree argument.  Its exact
derivative lower margin is

\[
0.64823627531795806891>0,
\tag{6.5}
\]

which proves that the maximum over all allowed degrees occurs at the endpoint
\(j=82\).  No tail-degree grid is used.

Equations (6.1)--(6.5) prove that the same true \((162,81)\) column controls
the complete induced norm throughout the root-isolating interval.

---

## 7. Strict gain and fixed-point restart

The R0.50 globally optimized multiplicative-character threshold satisfies

\[
r_*^{(50)}<0.382619813709566.
\]

The R0.51 lower endpoint gives the exact conservative ratio

\[
\frac{r_L}{r_{U}^{(50)}}
>1.0000121743210599539.
\tag{7.1}
\]

Thus the radius gain is greater than \(12.174\) ppm.  For the fixed-charge
variable \(R=Z^2W\), whose disk radius is \(r^3\),

\[
\frac{r_L^3}{(r_U^{(50)})^3}
>1.0000365234078239459.
\tag{7.2}
\]

The simpler rational restart radius

\[
r_0=0.382624
\]

already exceeds the R0.50 upper endpoint.  At
\((r,c,\lambda)=(0.382624,0.79756,0.7653)\), the exact linearization bound is

\[
L=0.99999773673918514317,
\qquad
1-L=2.2632608148568333017\times10^{-6}.
\tag{7.3}
\]

The affine-weighted residual is

\[
\|R\|_{r,c,\lambda}
=2.7403915410748708982\times10^{-31}.
\tag{7.4}
\]

The ball-mapping upper bound is

\[
2.2632556925226842841\times10^{-12},
\]

and the Lipschitz upper bound is

\[
0.99999773675276470806<1.
\tag{7.5}
\]

The fixed-point reconstruction and the conjugate canonical-field checks
therefore close at the rational restart point.

---

## 8. Formal figure

Figure R0.51-1 contains three complementary views:

1. the conservative root-box gap between the active \(s=162\) column and the
   zero sector along 126 exact rational \(\lambda\)-samples;
2. the incremental radius gains from R0.48 through R0.51 on a logarithmic
   scale;
3. all 243 exact root-box competitor gaps.

The sampled constraint switch near \(\lambda=0.7653260\) is a presentation
diagnostic, not the proof of a global affine optimum.  The formal package
contains PDF, SVG, and 600 dpi PNG outputs, source data, plotting code, a
manifest, caption, checksums, and independent validation.  Color, true
grayscale, and rendered PDF copies were inspected.

---

## 9. Research value and limitations

R0.51 establishes three facts inside the reduced generating system.

First, the R0.50 obstruction is not stable under the smallest natural
nonmultiplicative extension of the charge weight.  A fixed affine correction
gives a strict improvement larger than the entire R0.49-to-R0.50
multiplicative optimization gain.

Second, the new gain is limited by a concrete sector switch.  The zero-charge
column becomes the nearest competitor with a gap of only about
\(1.78\times10^{-5}\).  Future optimization must handle this balance rather
than only reduce the old \(s=162\) column.

Third, the proof remains all-order: the special negative sector, every fixed
positive charge, and the infinite large-charge lattice are controlled
without substituting finite sampling for a theorem.

The limitations are equally important.  The fixed rational pair is not
proved globally optimal in the full \((c,\lambda)\) family.  The candidate
near (3.1)--(3.2) remains exploratory.  The argument applies only to a
derived two-variable canonical edge system.  It does not provide a
scale-critical estimate for arbitrary divergence-free three-dimensional
data, does not control the full Fourier interaction geometry, and cannot be
interpreted as a regularity time or a singularity location for the original
PDE.

---

## 10. R0.52 acceptance target

R0.52 will test global optimality within the complete affine family.  A
positive certificate must include all of the following:

1. isolate an exact simultaneous root box for the active and zero-sector
   constraints, including a rigorous stationarity or constraint-switch
   condition;
2. prove that every inactive fixed-charge and all-order sector remains below
   the active maximum on that box;
3. globalize the local box over the full domain \(c>0,\lambda\ge0\), using
   monotone branch structure, convexity, or certified interval subdivision;
4. give a rigorous upper and lower bound for the global optimum and compare it
   with the R0.51 fixed rational threshold.

If a complete global proof is too expensive, the acceptable negative result
is a certified upper/lower gap for the family, or an explicit exact
counterexample to the proposed active-set structure.  No conclusion about
the original three-dimensional PDE follows from either outcome.

---

## 11. Reproducibility

The formal exact run used

```text
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py --output research/certificates/r051/resources.csv --interval 2 -- tmp/r024-venv/bin/python research/edge_affine_charge_weight_audit.py --max-total-degree 80 --character 19939/25000 --lambda-value 7653/10000 --radius-lower 191312235923011/500000000000000 --radius-upper 382624471846023/1000000000000000 --restart-radius 11957/31250 --ball-divisor 1000000 --charge-cutoff 241 --source-commit a53fdea63631977e4bb18f56da91e4e32e1a70c3 --r050-certificate research/certificates/r050/edge-charge-character-optimization.json --progress --progress-log research/certificates/r051/progress.ndjson --check --pretty --output research/certificates/r051/edge-affine-charge-weight.json
```

The source commit is

```text
a53fdea63631977e4bb18f56da91e4e32e1a70c3
```

and the certificate archive commit is

```text
7e42dae84dc83f4b4e8977cc57c2974f37e6dc34
```

The certificate SHA-256 is

```text
db72d40ee304d1a6ce5dd96d9f5971e78037675e79c837e409c5691bb8aa582f
```

The scientific computation took 127.065471 seconds.  The monitor recorded
64 samples over 127.2 seconds, with peak CPU usage 100.0 percent and peak
resident memory 201.453 MiB.  The exact backend was gmpy2 2.3.1 with GMP
6.3.0.  The run used no GPU, randomness, or floating-point sign decision.
All 26 formal checks passed.

