# R0.43: A charge-implied degree floor closes the next large-sector gate

## Status and conclusion boundary

R0.42 certified the reduced active field and the normalized canonical fields
on the common isotropic polydisc

\[
r=\frac{329}{1000}=0.329.
\]

It fixed the next millesimal point in advance at

\[
r_{\mathrm{acc}}=\frac{33}{100}=0.330,
\]

where the canonical-stretch polynomial norm remained below one but the
inherited all-order active-tail bound was

\[
Z_{80}^{\mathrm{old}}(0.330)
=1.002872150853994023>1.
\tag{0.1}
\]

The failure came from the analytic sector containing every positive input
charge \(s\geq241\).  That sector used the charge hypothesis to control two
charge ratios, but retained only the generic strict-tail fact \(j>80\) in a
decreasing degree prefactor.  The bivariate support cone also contains the
relation \(s\leq2j\).  Coupling these two facts yields

\[
j\geq\max\{81,\lceil241/2\rceil\}=121.
\tag{0.2}
\]

Replacing only the old degree floor by (0.2) gives the exact all-order bound

\[
\boxed{
Z_{80}^{\mathrm{floor}}(0.330)
=0.99888144242700740673<1.
}
\tag{0.3}
\]

The complete Banach fixed-point restart and the R0.42 canonical-stretch
construction then close at

\[
\boxed{r_*=\frac{33}{100}=0.330.}
\tag{0.4}
\]

The next millesimal point remains a strict negative control for the present
sufficient inequality:

\[
Z_{80}^{\mathrm{floor}}(0.331)
=1.0038955265828946573>1.
\tag{0.5}
\]

This is an all-order theorem for the reduced canonical edge generating
system.  It does not prove global regularity or finite-time blow-up for the
three-dimensional incompressible Navier--Stokes equation.  The failure in
(0.5) is not evidence of a singularity or of the true analytic radius.

## 1. Exact tail column and inherited large-charge estimate

Write a center monomial in degree-charge coordinates as \((i,q)\), and a
strict-tail input as \((j,s)\).  The exact weighted column factor of the
linearized reduced active map is

\[
A_{i,q;j,s}
=\frac{i+j}{i+j-1}
 \left|i\frac{s}{j}-q\right|
 \frac{|s-q|}{3|s+q|},
\qquad s+q\ne0.
\tag{1.1}
\]

The degree-80 center lies in the active cone

\[
1\leq i\leq80,
\qquad -1\leq q\leq2i.
\tag{1.2}
\]

For \(s\geq S=241\), condition (1.2) implies \(s>q\) for every center
monomial.  If \(q\geq0\), then

\[
\frac{s-q}{s+q}\leq1,
\qquad
0\leq x:=\frac{s}{j}\leq2,
\]

and convexity of the absolute affine factor gives

\[
|ix-q|\leq\max\{q,|2i-q|\}.
\tag{1.3}
\]

For the only negative center charge \(q=-1\),

\[
\frac{s+1}{s-1}\leq\frac{S+1}{S-1}
=\frac{242}{240},
\qquad
|ix+1|\leq2i+1.
\tag{1.4}
\]

R0.39 combined (1.3)--(1.4) with the generic bound

\[
\frac{i+j}{i+j-1}
\leq\frac{i+81}{i+80},
\qquad j>80.
\tag{1.5}
\]

The finite charges \(-1\leq s\leq240\) were later sharpened in R0.41, but
the infinite sector retained (1.5) through R0.42.

## 2. Charge-degree coupling theorem

Every bivariate input monomial satisfies

\[
-j\leq s\leq2j.
\tag{2.1}
\]

Consequently, throughout the large positive-charge sector,

\[
s\geq S,quad s\leq2j
\quad\Longrightarrow\quad
j\geq\left\lceil\frac S2\right\rceil.
\tag{2.2}
\]

Combining (2.2) with the strict-tail condition gives the uniform floor

\[
\boxed{
J_S=\max\left\{N+1,\left\lceil\frac S2\right\rceil\right\}.
}
\tag{2.3}
\]

The function \(j\mapsto(i+j)/(i+j-1)=1+1/(i+j-1)\) is decreasing.  Hence

\[
\frac{i+j}{i+j-1}
\leq\frac{i+J_S}{i+J_S-1}.
\tag{2.4}
\]

At \(N=80\) and \(S=241\), (2.3) gives \(J_S=121\), so (2.4) becomes

\[
\frac{i+j}{i+j-1}
\leq\frac{i+121}{i+120}.
\tag{2.5}
\]

Equations (1.3), (1.4), and (2.5) therefore give the all-order monomial
factor

\[
F^{\mathrm{floor}}_{i,q}=
\begin{cases}
\displaystyle
\frac{i+121}{i+120}(2i+1)\frac{242}{3\cdot240},
&q=-1,\\[1.2ex]
\displaystyle
\frac{i+121}{i+120}
\frac{\max\{q,|2i-q|\}}3,
&q\geq0.
\end{cases}
\tag{2.6}
\]

For the exact degree-80 center \(p_{80}\), the induced large-sector bound is

\[
Z_{\geq241}^{\mathrm{floor}}(r)
=\sum_{i,q}|(p_{80})_{i,q}|r^iF^{\mathrm{floor}}_{i,q}.
\tag{2.7}
\]

This proof covers every integer \(s\geq241\) and every admissible \(j>80\).
It uses no charge truncation, degree grid, asymptotic extrapolation, or
unproved coefficient cancellation.  The lattice congruence
\(j+s\equiv0\pmod3\) can only raise some individual minimum degrees; it is
not needed for the uniform theorem.

## 3. Exact reduction at the preassigned target

At \(r=0.330\), the old and new large-sector values are

\[
\begin{aligned}
Z_{\geq241}^{\mathrm{old}}
  &=1.002872150853994023,\\
Z_{\geq241}^{\mathrm{floor}}
  &=0.99888144242700740673,\\
\Delta Z
  &=0.0039907084269866162868.
\end{aligned}
\tag{3.1}
\]

The exact reduction by center-charge group is

| center charge | old contribution | new contribution | reduction |
|---:|---:|---:|---:|
| \(q=-1\) | 0.343228631948916 | 0.341846502141631 | 0.001382129807284 |
| \(q=0\) | 0.038928247098026 | 0.038778132201657 | 0.000150114896369 |
| \(q=1\) | 0.349338372737370 | 0.347962866706603 | 0.001375506030768 |
| \(q=2\) | 0.248427285859006 | 0.247432230803127 | 0.000995055055879 |
| \(q\geq3\) | 0.022949613210676 | 0.022861710573990 | 0.000087902636686 |

The largest finite-charge column inherited from R0.41 is

\[
0.85126797064187970263,
\tag{3.2}
\]

so the improved infinite sector remains the maximum and is strictly below
one.  Thus the proof does not exchange one hidden failing sector for another.

## 4. Complete restart at \(r=33/100\)

The contraction margin and chosen strict-tail ball are

\[
1-Z_{80}^{\mathrm{floor}}
=0.0011185575729925932715,
\qquad
\varepsilon
=1.1185575729925932715\times10^{-9}.
\tag{4.1}
\]

The degree-80 polynomial has 2161 nonzero terms.  Its complete residual has
6345 nonzero terms in degrees 81 through 160, with exact weighted norm

\[
\|R_{80}\|_{\mathcal B_r}
=1.8355533903214484259\times10^{-33}.
\tag{4.2}
\]

The remaining fixed-point gates are

\[
\begin{aligned}
\text{residual allowance}
  &=1.2511672905859483273\times10^{-12},\\
\text{ball-mapping upper bound}
  &=1.1173064057020073232\times10^{-9}<\varepsilon,\\
\text{ball Lipschitz bound}
  &=0.99888144913835284468<1.
\end{aligned}
\tag{4.3}
\]

The R0.42 canonical-stretch operator remains well inside its threshold:

\[
\|S_a\|\leq0.76764838318867159529<1.
\tag{4.4}
\]

Therefore

\[
\|(I-S_a)^{-1}\|
\leq4.3038219992762476125,
\qquad
\|\phi\|_{\mathcal B_r}
\leq1.5269664858053497992.
\tag{4.5}
\]

The exact factorization

\[
U=Ze^{\phi-a/2},
\qquad
V=We^{\phi+a/2}
\tag{4.6}
\]

then constructs the normalized canonical fields on the same open polydisc.
The obsolete direct one-step transport estimate is

\[
1.2914901850381049531>1,
\tag{4.7}
\]

but (4.7) is no longer a construction gate after R0.42.

The common radius gain over R0.42 is small,

\[
\frac{0.330}{0.329}
=1.0030395136778115502,
\tag{4.8}
\]

and the corresponding fixed-charge \(R=Z^2W\) disk grows by

\[
\left(\frac{0.330}{0.329}\right)^3
=1.0091462850446104324.
\tag{4.9}
\]

The mathematical content is the support-coupling theorem, not the numerical
size of this final radius increment.

## 5. Adjacent negative control

At

\[
r=\frac{331}{1000}=0.331,
\]

the improved active-tail bound is (0.5), while the degree-80 canonical
stretch diagnostic is still

\[
0.77194253306068784684<1.
\tag{5.1}
\]

The active correction is not certified because the active-tail linearization
exceeds one.  Thus (5.1) must not be described as a complete-field stretch
bound at the failed radius.  The result identifies the next bottleneck as the
same positive large-charge active sector under the remaining termwise charge
and slope relaxations.

## 6. Finite exact regressions and classification

The audit evaluates 21 exact columns at

\[
s\in\{241,242,243,300,480,600,1000\}
\]

and at three admissible input degrees for each charge: the exact lattice
minimum and offsets 3 and 12.  Every column lies below the analytic sector
bound.  These computations check the coefficient formula, lattice indexing,
and implementation.  They do not prove the infinite-sector theorem; that
role belongs to (1.3), (1.4), and (2.2)--(2.6).

The exact recurrence performs 1,113,168 ordered interactions.  The successful
certificate records 22/22 true formal checks, 255 process-tree resource
samples, 100.0% peak observed CPU, 44.312 MiB peak resident memory, no GPU,
no randomness, and no floating-point threshold decision.

## 7. Research value and limitations

The result is structurally useful because it recovers information that had
already been present in the support cone but had been discarded by separating
the large-charge and strict-tail hypotheses.  It is a positive all-order
improvement: every center coefficient enters through its absolute value, and
the proof needs no speculative cancellation.

Its direct value for the Navier--Stokes millennium problem remains limited.
No theorem currently transfers this reduced generating-system radius to a
scale-critical norm of a three-dimensional velocity field, excludes energy
concentration, or controls all helical and spatial interaction sectors of the
PDE.  The certified number 0.330 is neither the true reduced-system analytic
radius nor a physical time of regularity.

## 8. Next falsifiable step

R0.44 should keep \(r=0.331\) as the preassigned acceptance test and retain
the common variables

\[
x=\frac{s}{j},
\qquad
y=\frac1s
\]

inside the complete positive large-charge column.  The present theorem still
maximizes the degree factor, charge ratio, and absolute affine slope factor
separately.  A valid next improvement must establish a common-variable
monotonicity, convexity, or finite endpoint theorem for the positive sum over
all center charges.  If that structure cannot recover the exact 0.003896
deficit at \(r=0.331\), the negative result should be recorded before any
anisotropic reweighting is introduced.

## 9. Reproducibility

Formal source commit:

```text
4fe8cb308e20921fb0490aa2e76209b1d2d84221
```

Certificate SHA-256:

```text
0ebaaf6c5a9f731e5b2846f3042553bebd6748b298ce31919e8f423e41369bf8
```

Exact command:

```sh
tmp/r024-venv/bin/python research/edge_charge_degree_floor_audit.py \
  --max-total-degree 80 \
  --target-radius 33/100 \
  --failure-probe-radius 331/1000 \
  --charge-cutoff 241 \
  --regression-charges 241,242,243,300,480,600,1000 \
  --regression-degree-offsets 0,3,12 \
  --ball-divisor 1000000 \
  --source-commit 4fe8cb308e20921fb0490aa2e76209b1d2d84221 \
  --progress --check --pretty \
  --output /tmp/r043.json
```
