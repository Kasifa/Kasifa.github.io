# A common-slope endpoint theorem for the all-order active tail

## R0.44 research note

### Abstract

This note removes a termwise maximization from the large positive-charge
active-tail estimate for the reduced canonical edge generating system.  For
one strict-tail input, the slope (x=s/j) is shared by every monomial in the
degree-80 center.  After retaining that common slope, the complete positive
column envelope is a convex sum of absolute affine functions.  Its maximum on
the support interval (0\leq x\leq2) is therefore attained at the two common
endpoints, not at independently selected endpoints for each center term.

The resulting all-order theorem turns the inherited failure at
(r=0.331) into a strict pass and certifies the active fixed point, canonical
stretch field, and reconstructed regular fields at the common radius

\[
r_*=\frac{37}{100}.
\]

At this radius the large positive-charge sector is bounded by
(0.9662130057569357), while the unchanged finite charge (s=-1) column is
the new maximum at (0.9970118412481986).  The adjacent millesimal probe
(r=0.371) fails only in that finite column; its common-slope large-charge
sector still passes.  Every threshold decision below uses exact GMP rational
arithmetic.

The result is an all-order theorem for a reduced bivariate generating system.
It is not a regularity or singularity theorem for the full three-dimensional
Navier--Stokes equation.

---

## 1. Setting

Write a bivariate monomial as (Z^mW^n), and introduce total degree and
charge

\[
i=m+n,
\qquad
q=2n-m.
\]

The degree-80 active center has the finite expansion

\[
p_N=\sum_{i\leq N}\sum_q a_{i,q}Z^mW^n,
\qquad N=80,
\]

with active support

\[
-1\leq q\leq2i.
\]

For a radius (r>0), put

\[
c_{i,q}(r)=|a_{i,q}|r^i.
\]

Only these nonnegative weights enter the induced weighted-
\(\ell^1\) operator estimate.  No coefficient-sign cancellation is used.

Let a strict-tail input have degree (j>N) and charge (s).  Its bivariate
support satisfies

\[
-j\leq s\leq2j,
\qquad
j+s\equiv0\pmod3.
\]

R0.43 treated the infinite large positive-charge sector

\[
s\geq S,
\qquad S=241.
\]

The support inequality then forces

\[
j\geq J_S
:=\max\left\{N+1,\left\lceil\frac S2\right\rceil\right\}
=121.
\]

---

## 2. Exact active-tail column

For a center monomial ((i,q)) and a strict-tail input ((j,s)), the
derivative of the reduced active map has coefficient

\[
\gamma_{i,q;j,s}
=
\frac{(is-qj)(s-q)}
{3(s+q)(i+j-1)},
\qquad s+q\ne0.
\]

The input/output Wiener-weight ratio contributes ((i+j)/j).  Since
(s\ge241) and every center charge satisfies (q\le160), both (s-q) and
(s+q) are positive.  The exact positive column factor is therefore

\[
A_{i,q;j,s}
=
\frac{i+j}{i+j-1}
\left|i\frac{s}{j}-q\right|
\frac{s-q}{3(s+q)}.
\]

Introduce the two common variables

\[
x=\frac{s}{j},
\qquad
y=\frac1s.
\]

Then

\[
A_{i,q}(x,y)
=
\frac{1+ixy}{1+(i-1)xy}
|ix-q|
\frac{1-qy}{3(1+qy)}.
\]

The actual discrete inputs lie in the continuous domain

\[
0\leq x\leq2,
\qquad
0\leq y\leq\frac1S,
\qquad
xy\leq\frac1{J_S}.
\]

This representation exposes the loss in the R0.43 bound: the degree factor,
charge ratio, and absolute affine factor were bounded separately, and the
last factor was maximized independently for every ((i,q)).  A single input
cannot realize those different slopes simultaneously.

---

## 3. Positive domination without breaking the common slope

The (y)-dependent factors admit monotone positive bounds that do not alter
the shared (x).

First, because (j\geq J_S),

\[
\frac{i+j}{i+j-1}
\leq
d_i
:=
\frac{i+J_S}{i+J_S-1}.
\]

For the unique negative center charge (q=-1),

\[
\frac{s+1}{s-1}
\leq
\frac{S+1}{S-1}
=
\frac{242}{240}.
\]

For every (q\geq0),

\[
0\leq\frac{s-q}{s+q}\leq1.
\]

Define

\[
\beta_q=
\begin{cases}
\dfrac{S+1}{S-1},&q=-1,\\[4pt]
1,&q\geq0.
\end{cases}
\]

The complete large-charge column is bounded by the single function

\[
H_r(x)
=
\sum_{i,q}
c_{i,q}(r)d_i\beta_q\frac{|ix-q|}{3}.
\]

All coefficients in this sum are nonnegative.  The variable (x=s/j) has
not been split by center term.

---

## 4. Common-slope endpoint theorem

### Theorem 4.1

Let the center polynomial have support (q\geq-1), let (S) exceed every
center charge, and let every large-sector input satisfy (s\geq S), (j>N),
and (s\leq2j).  Then the induced weighted-
\(\ell^1\) large positive-charge column obeys

\[
\sup_{\substack{s\geq S,\ j>N\\ s\leq2j}}
\sum_{i,q}c_{i,q}(r)A_{i,q;j,s}
\leq
\max\{H_r(0),H_r(2)\}.
\]

This covers every integer charge (s\geq S) and every admissible input
degree above the polynomial cutoff.

### Proof

The support cone and the strict-tail condition give (j\geq J_S) and
(0\leq x=s/j\leq2).  The positive bounds in Section 3 give

\[
\sum_{i,q}c_{i,q}(r)A_{i,q;j,s}
\leq H_r(x).
\]

For each fixed ((i,q)), the map (x\mapsto|ix-q|) is convex.  A positive
linear combination of convex functions is convex, so (H_r) is convex on
([0,2]).  Every convex function on a compact interval is bounded above by
the larger endpoint value.  Hence

\[
H_r(x)\leq\max\{H_r(0),H_r(2)\}.
\]

Combining the two inequalities proves the claim.  The proof uses neither a
finite charge cutoff beyond (S), nor a degree grid, nor coefficient-sign
cancellation.  \(\square\)

### Remark 4.2

The variables (x) and (y) first reveal the exact coupling.  The
(y)-dependence can then be dominated monotonically while the shared slope
(x) remains inside the complete positive sum.  The decisive improvement is
therefore not a numerical fit to sampled charges; it is the removal of an
invalid independent choice of slope for different center terms.

---

## 5. Exact endpoint values

At the inherited R0.43 negative control (r=0.331), the old large-sector
bound was

\[
1.0038955265828946573>1.
\]

The common-slope theorem gives

\[
\max\{H_{0.331}(0),H_{0.331}(2)\}
=0.78111267115667101487<1.
\]

The complete tail maximum then moves to the finite (s=-1) column:

\[
Z_{80}^{\mathrm{common}}(0.331)
=0.85473326250594059615<1.
\]

The improvement is large enough to test radii well beyond the preassigned
thousandth step.

At (r=0.370), the two common-slope endpoint values are

\[
H_{0.370}(0)=0.56025596671784847152,
\]

\[
H_{0.370}(2)=0.96621300575693572712.
\]

Thus the large positive-charge sector passes.  The unchanged finite-charge
theorem has its largest column at (s=-1):

\[
Z_{80,-1}(0.370)
=0.99701184124819861673.
\]

Consequently the complete active-tail bound is

\[
\boxed{
Z_{80}^{\mathrm{common}}(0.370)
=0.99701184124819861673<1.
}
\]

For comparison, applying the R0.43 termwise large-sector estimate at the same
radius gives

\[
Z_{80,\ge241}^{\mathrm{R0.43}}(0.370)
=1.2153811722110079265>1.
\]

The new conclusion is therefore a consequence of the common-slope theorem,
not of a smaller numerical residual or a changed finite polynomial.

---

## 6. Complete Banach restart at \(r=0.370\)

The degree-80 polynomial contains 2,161 monomials.  Its exact weighted norm at
the target radius is

\[
\|p_{80}\|_{0.370}
=1.8914860157186488334.
\]

The complete residual contains 6,345 monomials in degrees 81 through 160, with

\[
\|R_{80}\|_{0.370}
=2.1491366411580359433\times10^{-29}.
\]

The contraction margin is

\[
\delta
=1-Z_{80}^{\mathrm{common}}(0.370)
=0.0029881587518013832739.
\]

With the deterministic choice

\[
\rho=\frac{\delta}{10^6}
=2.9881587518013832739\times10^{-9},
\]

the exact fixed-point gates are

\[
\|R_{80}\|_{0.370}
<8.9290659386890229856\times10^{-12},
\]

\[
\text{mapping upper bound}
=2.9792296858626942509\times10^{-9}<\rho,
\]

and

\[
\text{Lipschitz upper bound}
=0.99701185917715112753<1.
\]

The active correction therefore exists in the certified ball.

---

## 7. Canonical stretch field and reconstruction

R0.42 replaced the failed direct transport inversion with the regular
canonical stretch equation

\[
\mathcal L\phi-\{a,\phi\}
=\frac12(X-Y)a.
\]

At (r=0.370), its operator bound is

\[
\|S_a\|
\leq0.95518840332237634991<1.
\]

Hence

\[
\|(I-S_a)^{-1}\|
\leq22.315652066451424596,
\]

and the certified stretch-field norm is

\[
\|\phi\|_{\mathcal B_r}
\leq9.0927495343493502221.
\]

The bound is much larger than at (r=0.330), but remains finite and is
obtained from a strict Neumann-series inequality.  The exponential
reconstruction

\[
U=Ze^{(a-\phi)/2},
\qquad
V=We^{(a+\phi)/2}
\]

is therefore certified at the same common radius.  The older direct
one-step transport bound is

\[
1.5770610053215118683>1,
\]

but it is not a gate after the regular decomposition.

---

## 8. Adjacent negative control and the new bottleneck

At the next millesimal radius (r=0.371), the common-slope large positive-
charge sector still satisfies

\[
Z_{80,\ge241}^{\mathrm{common}}(0.371)
=0.97140144220860645363<1.
\]

The finite (s=-1) column instead becomes

\[
\boxed{
Z_{80,-1}(0.371)
=1.0008564924160487608>1.
}
\]

The degree-80 stretch polynomial remains below one at this probe.  Thus the
new obstruction is sharply localized: it is the inherited exceptional
finite-charge estimate, not the infinite large-charge sector and not the
regular stretch operator.

This is a failure of a sufficient inequality.  It does not show that a
solution is singular or that analyticity is lost at (0.371).

---

## 9. Finite exact regressions

The implementation performs two finite checks.

First, the 2,161 center terms generate 1,313 distinct breakpoints

\[
x=\frac qi\in[0,2].
\]

Every breakpoint value of the exact piecewise-linear envelope is checked with
GMP rationals.  The largest value is attained at (x=2) and equals the proved
endpoint bound.  This regression detects omitted terms, sign errors, or a
wrong endpoint implementation.  It is not the convexity proof.

Second, the audit selects

\[
s\in\{241,242,243,300,480,600,1000\}
\]

and evaluates the exact lattice-minimum input degree and offsets 3 and 12,
for 21 exact large-charge columns.  Every column lies below the all-order
common-slope sector bound.  These columns test the formula and code only; the
infinite charge and degree coverage comes from Theorem 4.1.

---

## 10. Reproducibility record

The formal run used the source commit

```text
aade631ea1a492d078f052776b443875d6a3dd73
```

and produced the certificate SHA-256

```text
7966771f25305211907e11e1a7ab7b6d784b1a14e3db92b3cbec37b96382bb1f
```

The run completed 34 formal checks in 44.516445 seconds.  Independent resource
monitoring lasted 44.618455 seconds with 300 samples, peak CPU usage of 100%,
and peak resident memory of 47.906 MiB.  No GPU, random seed, fitted parameter,
or floating-point threshold decision was used.

---

## 11. Mathematical value and limits

The reusable content of R0.44 is the endpoint theorem for a complete positive
operator column with a shared slope.  It converts a sum of termwise maxima
into the maximum of one convex sum.  In this reduced problem the difference is
large: the certified common radius increases from (0.330) to (0.370), a
factor of

\[
\frac{0.370}{0.330}=\frac{37}{33}\approx1.12121.
\]

For the fixed-charge variable (R=Z^2W), the corresponding disk-radius factor
is

\[
\left(\frac{37}{33}\right)^3
\approx1.40949.
\]

This is substantial inside the reduced generating system.  Its direct value
for the Millennium Problem remains limited.  No theorem here transfers the
reduced analytic radius to a scale-critical norm of the full three-dimensional
velocity field.  The calculation does not control all spatial, helical, and
cross-scale interactions, and it does not exclude energy concentration.

Accordingly, this note does not claim:

1. global smoothness of three-dimensional incompressible Navier--Stokes;
2. finite-time blow-up;
3. a physical or analytic singularity at (r=0.371);
4. that 1,313 breakpoint checks or 21 large-charge columns prove an infinite
   theorem;
5. that (0.370) is the true analytic radius even for the reduced system.

---

## 12. Next exact problem

The new bottleneck is the fixed input charge (s=-1).  For this charge the
same input degree (j) is shared across the complete center sum, while the
inherited R0.39 bound again treats degree dependence term by term.  Direct
exact columns already indicate that the lattice-minimum column at (j=82) is
below the current uniform estimate.

The next stage should therefore:

1. write the complete (s=-1) column as a function of the common inverse
   degree (t=1/j);
2. prove its monotonicity, convexity, or a finite endpoint reduction on
   (0\leq t\leq1/82);
3. keep (r=0.371) as the first acceptance point;
4. publish a negative result if the common-degree theorem cannot close the
   gap, before changing the norm or the canonical decomposition.

That problem is finite-charge but still all-order in degree.  It is the exact
obstruction exposed by R0.44.
