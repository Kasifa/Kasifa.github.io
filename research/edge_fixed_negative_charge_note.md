# An exact endpoint theorem for the fixed negative-charge tail

## R0.45 research note

### Abstract

This note resolves the finite-charge bottleneck left by R0.44 for the reduced
canonical edge generating system.  Fix the strict-tail input charge (s=-1)
and write (t=1/j), where (j) is the input degree.  At the degree cutoff
(N=80), the bivariate lattice gives

\[
0\leq t\leq \frac1{82},
\qquad j>80,
\qquad j\equiv1\pmod 3.
\]

The exact induced weighted-ℓ1 column is a finite sum of rational functions
of the single shared variable (t).  Terms of center charge (q=-1) vanish;
terms with (q=0) or (q\geq2) increase with (t); only (q=1) terms
decrease.  The degree-one, charge-two seed alone supplies a derivative lower
bound (r(3+2t)\geq3r).  An exact uniform bound for the total negative
derivative of all (q=1) terms is strictly smaller than this seed contribution.
Consequently the complete column is strictly increasing on the full continuous
interval and its all-order maximum is the true lattice endpoint (j=82).

At (r=0.371), the exact endpoint column is

\[
0.99722804122918895132<1,
\]

so the Banach restart and inherited canonical-stretch construction close at
the new common radius.  At the adjacent millesimal probe (r=0.372), the
same exact column is

\[
1.0010616516434951437>1.
\]

Every threshold decision uses exact GMP rational arithmetic.  The theorem is
all-order for a reduced bivariate generating system.  It is not a regularity
or singularity theorem for the full three-dimensional Navier--Stokes equation.

---

## 1. Setting and inherited obstruction

Write a center monomial as (Z^mW^n), with total degree and charge

\[
i=m+n,
\qquad
q=2n-m.
\]

The exact degree-80 center is

\[
p_{80}=\sum_{i\leq80}\sum_q a_{i,q}Z^mW^n,
\]

with active support

\[
-1\leq q\leq2i.
\]

At radius (r>0), define nonnegative center weights

\[
c_{i,q}(r)=|a_{i,q}|r^i.
\]

The proof uses these absolute weights and does not use coefficient-sign
cancellation.

For a strict-tail input of degree (j>80) and charge (s=-1), the bivariate
lattice relation (j+s\equiv0\pmod3) becomes

\[
j\equiv1\pmod3.
\]

Therefore the minimum admissible degree is (J=82).  R0.44 inherited a
termwise separated sufficient bound for this column.  At (r=0.371), that
bound was

\[
1.0008564924160487608>1.
\]

However, the exact (j=82) column was already below one.  The unresolved
question was whether the common (j)-dependence could be controlled for every
admissible tail degree without replacing an infinite proof by a degree grid.

---

## 2. Exact fixed-charge column

Put

\[
t=\frac1j,
\qquad
0\leq t\leq T:=\frac1{82}.
\]

For center charge (q\ne1), the exact contribution of ((i,q)) to the
(s=-1) weighted column is

\[
C_{i,q}(t)
=c_{i,q}(r)
\frac{1+it}{1+(i-1)t}
|q+it|\frac{|q+1|}{3|q-1|}.
\]

The exceptional output-charge-zero case (q=1) is

\[
C_{i,1}(t)
=c_{i,1}(r)
\frac{1-i^2t^2}{3(1+(i-1)t)}.
\]

Because (i\leq80) and (t\leq1/82), every factor (1-it) is strictly
positive.  The complete exact column is

\[
F_r(t)=\sum_{i,q}C_{i,q}(t).
\]

At every actual tail monomial, (F_r(1/j)) equals the exact induced
weighted-ℓ1 column.  The continuous interval is an analytic cover of the
discrete degree lattice, not a numerical interpolation.

---

## 3. Derivative sign classification

The center support contains only (q\geq-1), so four cases suffice.

### 3.1 The (q=-1) terms vanish

The factor (|q+1|) is zero, hence

\[
C_{i,-1}(t)=0.
\]

### 3.2 The (q=0) terms increase

Here

\[
C_{i,0}(t)
=c_{i,0}(r)
\frac{1+it}{1+(i-1)t}\frac{it}{3}.
\]

Every coefficient is nonnegative and direct differentiation gives a
nonnegative derivative on (t\geq0).

### 3.3 The (q\geq2) terms increase

For these charges,

\[
C_{i,q}(t)
=c_{i,q}(r)
\frac{1+it}{1+(i-1)t}
(q+it)\frac{q+1}{3(q-1)}.
\]

Both (q+it) and the degree ratio are positive and increasing, so

\[
C'_{i,q}(t)>0.
\]

### 3.4 Only the (q=1) terms decrease

Differentiating the exceptional expression gives

\[
-C'_{i,1}(t)
=c_{i,1}(r)
\frac{(i-1)+2i^2t+i^2(i-1)t^2}
{3(1+(i-1)t)^2}.
\]

The right-hand side is nonnegative.  These terms are the complete possible
negative derivative; no other center charge needs to be controlled against
them.

---

## 4. Uniform derivative theorem

Define

\[
\widehat Q_r(T)
:=\sum_i c_{i,1}(r)
\frac{(i-1)+2i^2T+i^2(i-1)T^2}{3}.
\]

Since ((1+(i-1)t)^2\geq1) and the numerator is increasing for
(0\leq t\leq T),

\[
\sum_i -C'_{i,1}(t)\leq\widehat Q_r(T).
\]

The degree-one, charge-two seed has coefficient one in the exact center.
Its weighted contribution is

\[
C_{1,2}(t)=r(1+t)(2+t),
\]

and therefore

\[
C'_{1,2}(t)=r(3+2t)\geq3r.
\]

All remaining (q=0) and (q\geq2) positive derivatives may be discarded.
This yields the global lower bound

\[
\boxed{F'_r(t)\geq3r-\widehat Q_r(T)}
\qquad(0\leq t\leq T).
\]

### Theorem 4.1

Let the degree-(N) center have support (q\geq-1), contain the unit
((i,q)=(1,2)) seed, and let (J>N) be the minimum degree on the
(s=-1) input lattice.  If

\[
3r-\widehat Q_r(1/J)>0,
\]

then the complete exact (s=-1) weighted column is strictly increasing in
(t=1/j) on ([0,1/J]).  Hence

\[
\sup_{\substack{j>N\\j-1\equiv0\pmod3}}
F_r(1/j)=F_r(1/J).
\]

#### Proof

The $q=-1$ contributions vanish.  The $q=0$ and $q\geq2$
contributions have nonnegative derivatives.  The magnitude of the sum of all
negative $q=1$ derivatives is at most $\widehat Q_r(1/J)$, while the
single degree-one, charge-two seed contributes at least $3r$.  The strict
hypothesis makes $F'_r(t)>0$ throughout the continuous interval.  Since
$t=1/j\leq1/J$, the maximum over the complete discrete lattice occurs at
$j=J$.  □

This proof does not use a degree cutoff beyond the fixed center, a tail-degree
grid, or coefficient-sign cancellation.

---

## 5. Exact target certificate at (r=0.371)

For the exact degree-80 center, there are 27 nonzero (q=1) terms.  GMP
rational evaluation gives

\[
\widehat Q_{0.371}(1/82)
=0.16864755013760409118\ldots,
\]

while the seed lower bound is

\[
3r=1.113.
\]

Thus

\[
\boxed{
3r-\widehat Q_{0.371}(1/82)
=0.94435244986239590882\ldots>0.}
\]

Theorem 4.1 covers every admissible (j>80).  The exact endpoint values are

\[
F_{0.371}(0)=0.98221269151066675449\ldots
\]

and

\[
\boxed{
F_{0.371}(1/82)
=0.99722804122918895132\ldots<1.}
\]

The inherited R0.44 separated estimate was 1.0008564924160487608.  R0.45
does not merely lower an auxiliary envelope: its certified value is the exact
induced column at the analytically proved maximizing degree.

---

## 6. Complete restart at the common radius

After replacing only the (s=-1) column, all other R0.44 finite-charge
columns and the complete common-slope large-charge theorem remain unchanged.
At (r=0.371), the key bounds are

| Certified quantity | Exact-decimal view | Decision |
|---|---:|---|
| exact (s=-1,j=82) column | 0.99722804122918895132 | all-order pass |
| complete large-charge sector | 0.97140144220860645363 | all-order pass |
| complete active-tail bound | 0.99722804122918895132 | strict pass |
| contraction margin | 0.00277195877081104868 | positive |
| chosen tail-ball radius | (2.77195877081105\times10^{-9}) | positive |
| complete residual norm | (2.68120196978466\times10^{-29}) | below allowance |
| ball mapping bound | (2.76427503843524\times10^{-9}) | below ball radius |
| ball Lipschitz bound | 0.99722805786094157619 | strict pass |
| canonical-stretch bound | 0.96032559431850165156 | strict pass |

The inherited regular-field equations are

\[
\mathcal L\phi-\{a,\phi\}=\tfrac12(X-Y)a,
\qquad
U=Ze^{\phi-a/2},
\qquad
V=W e^{\phi+a/2}.
\]

The stretch inverse satisfies

\[
\|(I-S_a)^{-1}\|\leq25.205166475028943098,
\]

and the constructed stretch field obeys

\[
\|\phi\|_{\mathcal B_r}\leq10.304751535574796762.
\]

The old direct-transport one-step norm is 1.5847832285603408903 and remains
above one.  It is a disclosed diagnostic, not a gate after the canonical
stretch factorization.

The radius gain over R0.44 is (371/370\approx1.0027027).  For the fixed-charge
variable (R=Z^2W), the corresponding cubic radius ratio is approximately
1.0081300.  These are internal gains for the reduced generating system, not
PDE regularity radii.

---

## 7. Adjacent exact negative control at (r=0.372)

The derivative argument remains valid at the adjacent probe:

\[
3r-\widehat Q_{0.372}(1/82)
=0.94628849129598398757\ldots>0.
\]

Therefore (j=82) is again the exact all-order maximum.  This time,

\[
\boxed{
F_{0.372}(1/82)
=1.0010616516434951437\ldots>1.}
\]

The complete large positive-charge sector still passes at

\[
0.97661386801873716684<1,
\]

and the polynomial canonical-stretch bound still passes at

\[
0.96548657260490674634<1.
\]

Thus the current norm method fails at (r=0.372) in an exact induced column,
not only in a separated upper bound.  This is a sharp negative control for the
present certificate.  It is not evidence of a singularity and does not locate
the true analytic radius of the reduced solution.

---

## 8. Finite exact regressions

The formal proof is analytic.  Finite exact degrees are retained only as code
regressions:

| Input degree (j) | Exact (s=-1) column at (r=0.371) |
|---:|---:|
| 82 | 0.99722804122918895132 |
| 85 | 0.99669882680238885548 |
| 88 | 0.99620564946148298758 |
| 100 | 0.99452851258946033944 |
| 1000 | 0.98344568068916077963 |

These values decrease with degree exactly as the theorem predicts.  They test
the closed formula, lattice handling, and implementation; they are not used
to infer monotonicity.

The complete deterministic audit also reconstructs the 2,161-term degree-80
center, evaluates the 6,345-term residual on degrees 81 through 160, preserves
the pinned polynomial and residual hashes from R0.44, and checks 1,113,168
ordered recurrence interactions.

---

## 9. Research value and limitations

The main value of R0.45 is structural.  It replaces an inherited separated
bound by an exact one-variable column theorem and supplies a reusable
seed-versus-obstruction argument.  The positive derivative is not found by
plotting or interval sampling; it is forced by one explicit low-degree seed
against a uniform exact bound for every possible negative derivative term.

The adjacent probe is also stronger than earlier negative controls.  At
(r=0.372), the failed quantity is the exact maximizing induced column of the
fixed degree-80 center.  Any further radius gain in the present weighted-ℓ1
framework must therefore change the norm, exploit a block structure, use
cancellations unavailable to a positive column norm, or enlarge and reorganize
the center-tail split.

For the three-dimensional Navier--Stokes Millennium problem, the direct value
remains limited.  No theorem currently transfers this reduced bivariate edge
control to a scale-critical norm of the full velocity field.  The construction
does not cover all spatial, helical, and cross-scale interactions, and it does
not exclude energy concentration in the full PDE.  R0.45 should be viewed as
a rigorous computer-assisted result for one reduced generating system and as
a test bed for proof mechanisms, not as a solution of the Millennium problem.

The following claims are not made:

1. global regularity of three-dimensional incompressible Navier--Stokes;
2. finite-time blow-up;
3. a singularity or true convergence barrier at (r=0.372);
4. an all-order theorem derived from the five finite degree checks;
5. a physical interpretation of the reduced radius as time or spatial scale.

---

## 10. Reproducibility

The formal source commit is

```text
8f7f9ec2b90b2d249b474ec4dbba50a71c807745
```

The exact certificate SHA-256 is

```text
abc588fb80a140cf78f0558119f50e7a15dce9b2d3fa5219a8b0f9456c8d0b7b
```

The complete monitored command is

```sh
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r045/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_fixed_negative_charge_audit.py \
  --max-total-degree 80 \
  --entry-radius 37/100 \
  --target-radius 371/1000 \
  --failure-probe-radius 372/1000 \
  --charge-cutoff 241 \
  --regression-degree-offsets 0,3,6,18,918 \
  --ball-divisor 1000000 \
  --source-commit 8f7f9ec2b90b2d249b474ec4dbba50a71c807745 \
  --progress \
  --progress-log research/certificates/r045/progress.ndjson \
  --check --pretty \
  --output research/certificates/r045/edge-fixed-negative-charge.json
```

The monitored run passed 33 of 33 exact checks.  Scientific wall time was
35.640978 seconds; monitored wall time was 35.747394 seconds.  The resource
log contains 240 samples, with maximum observed CPU use 100.0% and maximum
resident memory 42.766 MiB.  No GPU or randomness was used.

The formal figure package contains PDF, SVG, 600 dpi PNG, exact CSV tables,
caption, provenance manifest, progress and resource logs, validation scripts,
and SHA-256 checksums.  The final color export, true grayscale conversion, and
Poppler-rendered PDF page were inspected.

---

## 11. Next mathematical step

The exact (s=-1) obstruction at (r=0.372) means that further progress
cannot come from tightening the same scalar column formula.  The next stage
should test a two-block weighted norm that separates the exceptional output-
charge-zero channel from the remaining active tail.  The acceptance criteria
should be fixed before computation:

1. derive the block operator exactly and prove all-order coverage of every
   admissible degree and charge;
2. preserve the R0.45 scalar norm as a comparison and negative control;
3. require a strict pass at (r=0.372) without coefficient-sign cancellation;
4. preassign (r=0.373) as the adjacent probe;
5. publish a failed result if the block spectral radius is not below one.

This next step remains within the reduced model.  A separate research track is
still required to establish, or disprove, a rigorous bridge from the reduced
generating system to the full three-dimensional Navier--Stokes equation.
