# A multiplicative charge character and an anisotropic threshold gain

## R0.49 research note

### Abstract

R0.48 isolated the sharp local threshold of the previous two-block norm at

\[
0.376932499290527340<r_*^{(48)}<0.376932499290527341.
\]

The active true input column had charge (s=162) and degree (j=81).  This
note changes the Banach geometry by using the multiplicative charge character

\[
\omega_s=c^s,
\qquad c=\frac45.
\]

For a monomial (Z^mW^n), let (i=m+n) and (q=2n-m).  The new
one-total-derivative norm is

\[
\|f\|_{r,c}
=\sum_{m+n>0}(m+n)|f_{mn}|r^{m+n}c^{2n-m}.
\]

The diagonal map (S_c[Z^mW^n]=c^qZ^mW^n) is an exact algebra
automorphism.  It commutes with the reduced nonlinear map and conjugates the
anisotropic norm to the ordinary degree-weighted Wiener norm.  Equivalently,
the polyradii are

\[
\rho_Z=\frac r c,
\qquad
\rho_W=rc^2.
\]

The R0.47 all-order charge-degree theorem can therefore be applied to the
charge-scaled center without a tail-degree grid or an infinite charge scan.
The same true column ((j,s)=(81,162)) dominates throughout
([0.382618,0.382619]).  Its exact degree-80 threshold polynomial has one
globally unique positive root, isolated by exact rational arithmetic in

\[
0.382618642388680778
<r_*^{(4/5)}
<0.382618642388680779.
\]

An independent exact Sturm sequence counts one root in that interval.  All
243 competitors remain strictly below the active column on the complete
millionth window; the nearest is the fixed (s=164) sector, with exact
monotone-sandwich gap approximately
(1.4157274652028842093\times10^{-4}).

At (r=0.382618), the degree-weighted anisotropic Newton restart and the
conjugated canonical-stretch construction both close.  The polydisc is not a
larger isotropic bidisc: (ho_Z=0.4782725) while
(ho_W=0.24487552).  Nevertheless
(ho_Z^2\rho_W=r^3), so the certified disk radius in the fixed-charge
variable (R=Z^2W) gains a strict lower factor
(1.0459367903514846826) relative to the upper endpoint of the R0.48
threshold.

This is an exact anisotropic Banach-space theorem for the reduced canonical
edge generating system.  It does not prove that (c=4/5) is optimal, does
not enlarge both polyradii, and does not establish any result for arbitrary
three-dimensional Navier--Stokes velocity fields.

---

## 1. Degree, charge, and the character norm

Write a monomial exponent in degree-charge coordinates as

\[
i=m+n,
\qquad
q=2n-m.
\tag{1.1}
\]

On zero-constant formal series, let

\[
\|f\|_{r,c}
=\sum_{m+n>0}(m+n)|f_{mn}|r^{m+n}c^{2n-m},
\qquad r>0, c>0.
\tag{1.2}
\]

Define the charge scaling

\[
S_c(Z^mW^n)=c^{2n-m}Z^mW^n.
\tag{1.3}
\]

Charge is additive under multiplication.  Hence

\[
S_c(fg)=(S_cf)(S_cg).
\tag{1.4}
\]

The charge character introduces no extra loss into the inherited convolution
estimates.  In particular,

\[
\|f\|_{r,c}=\|S_cf\|_{B_r},
\tag{1.5}
\]

where (B_r) denotes the one-total-derivative isotropic Wiener norm.  Equation
(1.5), rather than a comparison with an isotropic norm at the same variables,
is the exact isometry used below.

Since

\[
r^{m+n}c^{2n-m}
=\left(\frac r c\right)^m(rc^2)^n,
\]

the same norm is the degree-weighted Wiener norm on the anisotropic polydisc

\[
|Z|<\rho_Z=\frac r c,
\qquad
|W|<\rho_W=rc^2.
\tag{1.6}
\]

---

## 2. Exact covariance of the reduced equation

The reduced nonlinear map (Phi) is assembled from the log-canonical
bracket, Euler fields, charge projections, and diagonal inverses in degree and
charge.  For monomials of charges (q_1,q_2), their product and nonzero
bracket terms have charge (q_1+q_2).  The Euler fields (X,Y,mathcal L),
the charge operator, and charge projections are diagonal in the same basis.
Consequently,

\[
S_c\Phi(f)=\Phi(S_cf).
\tag{2.1}
\]

If the original reduced fixed-point equation is

\[
p=Z+W+\Phi(p),
\tag{2.2}
\]

then the scaled equation is exactly

\[
S_cp=S_c(Z+W)+\Phi(S_cp).
\tag{2.3}
\]

The finite degree-80 center and its degree-81-through-160 residual satisfy
(2.1)--(2.3) coefficient by coefficient.  The audit additionally checks
product, bracket, and (X-Y) covariance on the exact center.  These finite
regressions check the implementation; the all-order identity follows from
charge additivity and diagonality.

For a center monomial of charge (q), an input monomial of charge (s) is
sent to charge (s+q).  The exact output/input character ratio is therefore

\[
\frac{\omega_{s+q}}{\omega_s}=c^q.
\tag{2.4}
\]

Thus every anisotropic induced column for the original center is the
ordinary induced column for the charge-scaled center (S_cp_{80}).  No
inequality is introduced at this step.

---

## 3. Why (c=4/5) is a theorem parameter, not an optimum

The exact active-column contribution at the R0.48 threshold is concentrated
in a small number of center charges.  A finite exploratory balancing of those
contributions indicated that decreasing (c) below one could reduce the
dominant column.  A separate all-sector numerical prototype placed a useful
candidate near (c\approx0.8025).

I fixed

\[
c=\frac45
\tag{3.1}
\]

before the formal R0.49 audit because it is a simple rational value near that
prototype.  Every theorem below is for the pinned value (3.1).  The
exploratory calculation is not an optimality proof, and the certificate makes
no statement about

- the best (c>0) in the character family;
- general submultiplicative charge-diagonal weights;
- a joint optimum over charge and zero-charge block weights;
- a PDE-critical norm for three-dimensional velocity fields.

The new norm also is not a one-parameter continuation of the R0.48
(kappa=3/4) two-block norm.  Comparisons with R0.48 are comparisons between
two certified schemes, not an attribution of the whole gain to one scalar.

---

## 4. The weighted active threshold polynomial

For (c=4/5), the R0.47 fixed-charge endpoint reduction identifies the true
minimum-degree input

\[
(j,s)=(81,162)
\tag{4.1}
\]

at both ends of ([0.382618,0.382619]).  Its exact induced column is

\[
A_c(r)=C_{r,c}(81,162)
=\sum_{i=1}^{80}\alpha_i(c)r^i,
\qquad \alpha_i(c)>0.
\tag{4.2}
\]

Define

\[
P_c(r)=A_c(r)-1.
\tag{4.3}
\]

The rational-coefficient digest of (P_c) is

```text
3e2d58683a97c46290ae8d5ffc6b8beab38bb5763393aca4dcee5991cd7f5288
```

After clearing denominators and dividing by the integer content, the
primitive degree-80 integer polynomial has digest

```text
590f711be8e843317ddf776dbb52268ea6d45d6f85d73adb804ff3825393c357
```

All 80 nonconstant coefficients are strictly positive.  Therefore

\[
P_c'(r)=\sum_{i=1}^{80}i\alpha_i(c)r^{i-1}>0
\qquad(r>0).
\tag{4.4}
\]

Since (P_c(0)=-1) and the leading coefficient is positive, (P_c) has
exactly one positive root.  This global uniqueness proof uses coefficient
positivity.  The Sturm calculation below is an independent exact audit of the
isolated interval.

---

## 5. Exact root isolation and Sturm count

At the adjacent millionth endpoints,

\[
\begin{aligned}
A_c(0.382618)
&=0.99999692284203436108\ldots<1,\\
A_c(0.382619)
&=1.0000017130264400588\ldots>1.
\end{aligned}
\tag{5.1}
\]

Thirty-nine exact decimal bisection decisions give

\[
r_L=\frac{191309321194340389}{5\times10^{17}},
\qquad
r_U=\frac{382618642388680779}{10^{18}},
\tag{5.2}
\]

with

\[
r_U-r_L=10^{-18}.
\tag{5.3}
\]

Their exact polynomial signs are represented by the display values

\[
P_c(r_L)=-6.8779076676005793044\times10^{-19}<0,
\]

and

\[
P_c(r_U)=4.1023964596411415889\times10^{-18}>0.
\]

Every sign decision uses the full GMP numerator and denominator, not the
display decimal.

Starting with (S_0=P_c) and (S_1=P_c'), the exact Euclidean recurrence

\[
S_{k+1}=-\operatorname{rem}(S_{k-1},S_k)
\tag{5.4}
\]

produces 81 nonzero polynomials of degrees (80,79,\ldots,0).  No sequence
value vanishes at either endpoint.  The sign-variation counts are

\[
V(r_L)=40,
\qquad
V(r_U)=39.
\tag{5.5}
\]

Sturm's theorem gives

\[
N_{(r_L,r_U)}=V(r_L)-V(r_U)=1.
\tag{5.6}
\]

Combining (4.4) and (5.2)--(5.6) yields the certified root display

\[
\boxed{
0.382618642388680778
<r_*^{(4/5)}
<0.382618642388680779.
}
\tag{5.7}
\]

---

## 6. Full-window all-order dominance

Let

\[
I=[r_0,r_1]=[0.382618,0.382619].
\]

Every exact character-weighted column has the form

\[
B(r)=\sum_i\beta_i r^i,
\qquad \beta_i\ge0,
\tag{6.1}
\]

and is nondecreasing for (r\ge0).  Hence for every competitor and every
(r\in I),

\[
B(r)\le B(r_1),
\qquad
A_c(r)\ge A_c(r_0).
\tag{6.2}
\]

The exact monotone sandwich compares the active left-endpoint value with 243
right-endpoint competitor bounds:

\[
238\text{ other fixed positive charges}
+1\text{ inactive endpoint for }s=162
+4\text{ remaining exhaustive sectors}.
\]

The nearest competitor is the fixed (s=164) sector,

\[
B_{164}(r_1)=0.99985535009551407266\ldots,
\]

and the minimum full-window gap is

\[
A_c(r_0)-B_{164}(r_1)
=1.4157274652028842093\times10^{-4}>0.
\tag{6.3}
\]

The large-positive-charge sector is bounded by the exact even and odd
Bernstein endpoint proofs.  Its values at the two endpoints are

\[
0.99602701187065410303\ldots
\quad\text{and}\quad
0.99603179188754206146\ldots,
\]

both strictly below one.  The fixed-charge convex endpoint theorem covers
every admissible tail degree.  No tail-degree grid and no finite replacement
for the infinite charge sector enters the proof.

### Theorem 6.1

For the pinned reduced canonical edge generating system and the norm
(\|\cdot\|_{r,4/5}), the induced linearization norm satisfies

\[
\|D\Phi(p_{80})\|_{r,4/5}=C_{r,4/5}(81,162)=A_c(r)
\qquad(r\in I).
\tag{6.4}
\]

Consequently,

\[
\begin{cases}
\|D\Phi(p_{80})\|_{r,4/5}<1,&r_0\le r<r_*^{(4/5)},\\
\|D\Phi(p_{80})\|_{r,4/5}=1,&r=r_*^{(4/5)},\\
\|D\Phi(p_{80})\|_{r,4/5}>1,&r_*^{(4/5)}<r\le r_1.
\end{cases}
\tag{6.5}
\]

#### Proof

Equation (2.4) turns every anisotropic column into the corresponding ordinary
column of the charge-scaled center.  The all-order endpoint theorems cover the
five disjoint charge sectors.  The strict monotone sandwich (6.2)--(6.3)
keeps every competitor below the true column throughout (I), proving (6.4).
Strict monotonicity (4.4) and the isolation (5.7) then give (6.5).  □

---

## 7. Exact charge composition of the obstruction

At (r=r_0), group the active column by center charge.  The five largest
exact contributions are

| center charge (q) | contribution | share of active column |
|---:|---:|---:|
| (-1) | (0.5050735065970958637\ldots) | (50.50750607928424\ldots\%\) |
| (+1) | (0.38298788845471822301\ldots) | (38.29890669725764\ldots\%\) |
| (0) | (0.063077736347251425027\ldots) | (6.30779304480076\ldots\%\) |
| (+2) | (0.030188058573041966916\ldots) | (3.01881514667527\ldots\%\) |
| (+3) | (0.017135220824103145879\ldots) | (1.71352735520466\ldots\%\) |

The (q=-1) and (q=+1) components together supply about (88.8064\%) of
the active column.  The formal figure archive retains all 158 distinct center
charges; only the display groups (q\ge4) into one bar.

This distribution explains why a charge character can move the threshold:
the factors (c^q) rebalance positive and negative center charges.  It does
not prove that the chosen balance is optimal, because the active identity and
all competitor bounds must be controlled simultaneously as (c) varies.

---

## 8. Degree-weighted Newton restart and canonical fields

Let (p_c=S_cp_{80}), and let (R_c) be its exact residual in the scaled
fixed-point equation.  At (r=r_0), the all-order linearization bound is

\[
L=0.99999692284203436108\ldots,
\]

so the contraction margin is

\[
\delta=1-L
=3.0771579656389206393\times10^{-6}.
\tag{8.1}
\]

Choose the degree-weighted anisotropic ball radius

\[
\eta=\frac{\delta}{10^6}
=3.0771579656389206393\times10^{-12}.
\tag{8.2}
\]

The charge isometry transfers the inherited quadratic estimate without an
extra character loss:

\[
\|\Phi(h)\|_{r,c}\le3\|h\|_{r,c}^2.
\tag{8.3}
\]

The exact one-total-derivative residual norm is

\[
\|R_c\|_{r,c}
=1.6910402110013306773\times10^{-30}.
\tag{8.4}
\]

The proof uses (8.4), including the total-degree factor.  A smaller
unweighted diagnostic is retained in the certificate only to expose and
exclude it from the proof.  The exact residual allowance and mapping bound
are

\[
\delta\eta-3\eta^2
=9.4688727387916242088\times10^{-18},
\]

and

\[
\|R_c\|_{r,c}+L\eta+3\eta^2
=3.0771484967661818494\times10^{-12}<\eta.
\tag{8.5}
\]

The Lipschitz bound is

\[
L+6\eta
=0.99999692286049730887\ldots<1.
\tag{8.6}
\]

Thus the anisotropic fixed-point ball closes.

The canonical stretch satisfies

\[
\mathcal L\phi-\{a,\phi\}
=\frac12(X-Y)a.
\tag{8.7}
\]

The map (S_c) commutes with (mathcal L), (X-Y), the log-canonical
bracket, products, and coefficientwise exponentials.  Therefore (8.7) and
the reconstructions

\[
U=Z\exp(\phi-a/2),
\qquad
V=W\exp(\phi+a/2)
\tag{8.8}
\]

are exactly conjugate under (S_c).  The scaled stretch-operator bound is

\[
0.98796898781173256118\ldots<1.
\tag{8.9}
\]

Hence the reduced fixed point, stretch field, and canonical fields all close
at (r_0).  The older direct-transport diagnostic is
(1.6842006275604065771\ldots>1); it is a comparison only and is not the
construction gate after the canonical-stretch reduction.

---

## 9. What the geometric gain means

At the certified target and (c=4/5),

\[
\rho_Z=\frac{0.382618}{4/5}=0.4782725,
\]

while

\[
\rho_W=0.382618\left(\frac45\right)^2
=0.24487552.
\tag{9.1}
\]

Thus one polyradius grows and the other shrinks.  The new polydisc and the
R0.48 isotropic reference are not nested.

For a fixed-charge expansion, the invariant variable is

\[
R=Z^2W.
\]

Its disk radius in the anisotropic polydisc is

\[
\rho_R=\rho_Z^2\rho_W=r^3.
\tag{9.2}
\]

At (r_0),

\[
\rho_R=0.056013949016933032.
\]

Using the upper endpoint of the R0.48 root bracket gives the conservative old
reference

\[
(r_U^{(48)})^3
=0.053553856727909601176\ldots.
\]

Therefore

\[
\frac{r_0^3}{(r_U^{(48)})^3}
=1.0459367903514846826\ldots>1.
\tag{9.3}
\]

Equation (9.3) is a strict certified fixed-charge disk-radius gain of more
than (4.59\%) between the two schemes.  It is not an isotropic-bidisc gain,
not a domain inclusion, and not a statement about the analytic radius of the
full three-dimensional Navier--Stokes solution map.

---

## 10. Computation and verification boundary

The degree-80 center is a finite exact construction with 1,113,168 ordered
recurrence interactions.  The charge covariance, active polynomial, root
signs, Sturm sequence, endpoint theorems, 243 dominance gaps, Newton
inequalities, and geometry ratios use exact GMP rationals or exact formal
identities.

The successful formal run used

- Python 3.12.13;
- gmpy2 2.3.1 and GMP 6.3.0;
- 119.530144 seconds of scientific wall time;
- 120.581154 seconds of monitored wall time;
- 808 process-tree samples at 0.125-second intervals;
- 100.0% peak observed CPU and 158.906 MiB peak resident memory;
- no GPU, randomness, floating-point threshold decision, tail-degree grid,
  or finite replacement for the infinite charge theorem.

All 32 exact checks passed.  Thirty finite exact columns are retained only as
implementation regressions; the tail theorem is all-order.  The corrected
certificate SHA-256 is

```text
e36fce33f8a5edeb144cdbeda00a568b972d9a3a8ac0e96c04d7651e71a64578
```

The formal source commit is

```text
26ce6d7ffd636956fe7c95a2bbeb7e6ea6573728
```

The journal figure archive contains its exact CSV tables, source, caption,
manifest, hashes, PDF, SVG, 600 dpi PNG, progress log, and resource log.  Its
color, grayscale, and PDF renderings were inspected at final size; all PDF
fonts are embedded and no Type 3 font is present.

---

## 11. Mathematical value and the next falsifiable question

R0.49 adds a real result inside the reduced program:

1. it replaces an ad hoc block weighting by an exact charge-character
   similarity compatible with the nonlinear algebra;
2. it proves that the true active obstruction can be moved while preserving
   all-order charge and tail-degree coverage;
3. it turns the gain into a precise fixed-charge geometric statement rather
   than an ambiguous scalar-radius comparison;
4. it exposes the charge composition responsible for the obstruction;
5. it preserves a reproducible Newton and canonical-field construction after
   correcting the residual norm to the required degree-weighted convention.

The result remains several conceptual steps from the Millennium Problem.  It
does not embed arbitrary divergence-free three-dimensional initial data into
the reduced two-variable system, does not propagate a scale-critical PDE
norm, and does not control the full Fourier interaction geometry.  No claim
about global regularity or finite-time blow-up follows.

The next useful question is now narrow and falsifiable:

> Within the exact character family (omega_s=c^s), can one certify an
> optimal interval for (c) and its threshold while proving that the active
> column and all 243 competitor inequalities remain stable over a rational
> ((r,c))-rectangle?

A positive result would turn the exploratory choice (c=4/5) into an exact
two-parameter optimization theorem.  A negative result would identify where
the active column changes or where the large-charge Bernstein proof loses
uniformity.  Either outcome is mathematically informative and remains
separate from any claim about the full Navier--Stokes equations.
