# An exact threshold root for the active charge column

## R0.48 research note

### Abstract

R0.47 placed the current induced two-block weighted-$\ell^1$ norm below one
at $r=0.376932$ and above one at $r=0.376933$.  The same true input column,
with charge $s=162$ and degree $j=81$, was active at both endpoints.  This
note replaces that decimal observation by an exact threshold theorem.

The active column is an explicit polynomial

\[
A(r)=C_r(81,162)=\sum_{i=1}^{80}\alpha_i r^i,
\qquad \alpha_i>0.
\]

Hence $P(r)=A(r)-1$ has $P(0)=-1$ and $P'(r)>0$ for every $r>0$.  Its
positive root is globally unique.  Exact rational bisection isolates it in

\[
0.376932499290527340<r_*<0.376932499290527341,
\]

and an independently constructed exact Sturm sequence counts exactly one
root in that interval.

Every competing weighted column is a nonnegative sum of powers of $r$ and is
therefore nondecreasing.  The R0.47 all-order upper bounds at the right
endpoint, compared with the active column at the left endpoint, give a
strict full-window monotone sandwich.  All 243 competitors remain below the
active column on $[0.376932,0.376933]$.  The nearest is the fixed-charge
$s=164$ endpoint, with exact gap approximately
$9.9933786489298977945\times10^{-5}$.

Thus the full induced norm equals $A(r)$ on the whole window.  It is below
one for $r<r_*$, equal to one at $r_*$, and above one for $r>r_*$ within the
window.  This is a sharp local threshold theorem for one reduced generating
system and one norm.  It is not a singularity theorem and has no direct
implication for three-dimensional Navier--Stokes regularity.

---

## 1. Active threshold polynomial

Keep the degree-80 center $p_{80}$ and the zero/nonzero-charge norm

\[
\|f\|_{r,\kappa}
=\kappa\|P_0f\|_{B_r}+\|P_{\ne0}f\|_{B_r},
\qquad \kappa=\frac34.
\]

For the true tail input $(j,s)=(81,162)$, every absolute column contribution
has the form $b_i r^i$ with $b_i\ge0$.  Collecting equal powers gives

\[
A(r)=\sum_{i=1}^{80}\alpha_i r^i.
\tag{1.1}
\]

The exact GMP construction verifies that all 80 coefficients in (1.1) are
strictly positive.  Define

\[
P(r)=A(r)-1=-1+\sum_{i=1}^{80}\alpha_i r^i.
\tag{1.2}
\]

The rational-coefficient digest of (1.2) is

```text
37653ae3a9fe744036643d9480250aa2ccbede6e6a8091050827254617d675cf
```

Clearing denominators and dividing by the integer content gives a primitive
degree-80 integer polynomial with digest

```text
d30024f19b2538961103ade17ac0df50947518fa698e43b28a8fcd1e5e33e87f
```

The complete 81-coefficient integer polynomial is stored in the machine
certificate rather than reproduced in the prose note.

---

## 2. Global uniqueness of the positive root

Differentiating (1.2) gives

\[
P'(r)=\sum_{i=1}^{80}i\alpha_i r^{i-1}>0
\qquad (r>0).
\tag{2.1}
\]

Therefore $P$ is strictly increasing on the positive axis.  Since
$P(0)=-1$ and the leading coefficient is positive,
$P(r)\to+\infty$ as $r\to+\infty$.  The intermediate value theorem and
(2.1) prove that $P$ has exactly one positive root.

This proof uses coefficient positivity and is already global.  The Sturm
calculation below is retained as an independent exact root-count audit and
as a portable certificate of the isolated interval.

---

## 3. Exact rational isolation

The endpoint values at the adjacent millionth are

\[
\begin{aligned}
P(0.376932)
&=-2.6509173803344006173\times10^{-6}<0,\\
P(0.376933)
&=+2.6584572409359\ldots\times10^{-6}>0.
\end{aligned}
\]

Forty exact bisection decisions at decimal scale $10^{18}$ give adjacent
rationals

\[
r_L=\frac{18846624964526367}{50000000000000000},
\qquad
r_U=\frac{376932499290527341}{10^{18}},
\]

with

\[
r_U-r_L=10^{-18}.
\tag{3.1}
\]

Their exact polynomial signs are

\[
P(r_L)=-4.8402210007478343466\times10^{-18}<0,
\]

and

\[
P(r_U)=+4.6915360306772411214\times10^{-19}>0.
\]

The decimal strings are display values; the sign decisions use the full GMP
rational numerators and denominators stored in the certificate.  A display
midpoint is

\[
0.3769324992905273405.
\]

---

## 4. Exact Sturm certificate

Starting with $S_0=P$ and $S_1=P'$, define the Euclidean Sturm recurrence

\[
S_{k+1}=-\operatorname{rem}(S_{k-1},S_k).
\tag{4.1}
\]

Each nonzero polynomial is normalized by a positive scalar so its leading
coefficient has absolute value one.  Positive normalization leaves all
endpoint signs and the Sturm variation count unchanged.

The exact sequence has length 81 and degrees

\[
80,79,78,\ldots,1,0.
\]

No sequence value vanishes at $r_L$ or $r_U$.  The sign variation counts are

\[
V(r_L)=40,
\qquad
V(r_U)=39.
\tag{4.2}
\]

Sturm's theorem therefore gives

\[
N_{(r_L,r_U)}=V(r_L)-V(r_U)=1.
\tag{4.3}
\]

The certificate stores the complete 81-character sign strings and a SHA-256
digest for every normalized sequence polynomial.  Every division and every
endpoint evaluation in (4.1)--(4.3) uses exact rational arithmetic.

---

## 5. Full-window dominance

Let

\[
I=[r_0,r_1]=[0.376932,0.376933].
\]

Every exact weighted column has the form

\[
B(r)=\sum_i\beta_i r^i,
\qquad \beta_i\ge0.
\tag{5.1}
\]

Thus $B$ is nondecreasing on $r\ge0$.  For every competing column and every
$r\in I$,

\[
B(r)\le B(r_1).
\tag{5.2}
\]

R0.47 supplies all-order right-endpoint upper bounds for the five exhaustive
charge sectors.  Conversely, the active column is nondecreasing, so

\[
A(r)\ge A(r_0)
=0.9999973490826196656\ldots.
\tag{5.3}
\]

The audit compares (5.3) with 243 exact right-endpoint competitor bounds:

\[
238\text{ other fixed charges}
+1\text{ inactive endpoint for }s=162
+4\text{ remaining sectors}.
\]

Every gap is strictly positive.  The maximum competitor is the fixed
$s=164$ minimum-degree endpoint,

\[
B_{164}(r_1)=0.99989741529613036662\ldots,
\]

and the smallest sandwich gap is

\[
A(r_0)-B_{164}(r_1)
=9.9933786489298977945\times10^{-5}>0.
\tag{5.4}
\]

For the infinite large-positive-charge sector, (5.2) is applied to each true
column separately and R0.47's parity-branch theorem supplies the common
right-endpoint bound.  No charge grid or tail-degree grid is used.

---

## 6. Sharp local norm threshold

### Theorem 6.1

For the pinned reduced canonical edge generating system and the induced
two-block weighted-$\ell^1$ norm with $\kappa=3/4$, let $r_*$ be the unique
positive root of $P(r)=C_r(81,162)-1$.  On
$I=[0.376932,0.376933]$,

\[
\|D\Phi(p_{80})\|_{r,3/4}=C_r(81,162)=A(r).
\tag{6.1}
\]

Consequently,

\[
\begin{cases}
\|D\Phi(p_{80})\|_{r,3/4}<1,&r_0\le r<r_*,\\
\|D\Phi(p_{80})\|_{r,3/4}=1,&r=r_*,\\
\|D\Phi(p_{80})\|_{r,3/4}>1,&r_*<r\le r_1.
\end{cases}
\tag{6.2}
\]

#### Proof

The monotone sandwich in Section 5 shows that every competing column is
strictly below the active column throughout $I$.  Hence the induced
weighted-$\ell^1$ column supremum is exactly the true column $A(r)$, proving
(6.1).  Section 2 proves that $A(r)-1=P(r)$ is strictly increasing and has a
unique positive zero.  The exact isolation in Section 3 places that zero
inside $I$.  The three cases in (6.2) follow.  □

The statement above is sharp for the present induced norm on this window.  A
strict inequality below one is only a sufficient contraction condition.  Its
failure above $r_*$ is not a PDE singularity and does not rule out another
equivalent or anisotropic norm.

---

## 7. Computation and verification boundary

The degree-80 center is a finite exact construction.  Its recurrence contains
1,113,168 ordered interactions.  The threshold polynomial, root isolation,
Sturm sequence, endpoint signs, and 243 dominance gaps are all exact.

The formal run used:

- Python 3.12.13;
- gmpy2 2.3.1 and GMP 6.3.0;
- 21.172433 seconds of scientific wall time;
- 21.287027 seconds of monitored wall time;
- 144 process-tree samples at 0.125-second intervals;
- 100.0% peak observed CPU and 109.875 MiB peak resident memory;
- no GPU, random seed, floating-point sign decision, charge scan beyond the
  theorem list, or tail-degree grid.

All 22 formal checks passed.  The certificate SHA-256 is

```text
246bcfa6623b1050511554312c32e9973b42b620a20ff571a1b5f340041c9af0
```

The formal source commit is

```text
fe65dcb365eca9d934c3ec6055c06d7a7c1a515c
```

---

## 8. What this result does and does not add

The main mathematical gain is not an extra decimal of radius.  R0.48
separates three statements that were previously conflated:

1. the active true column is an explicit monotone degree-80 polynomial;
2. the present norm has a unique exact threshold, rather than a chosen
   decimal cutoff;
3. no other charge sector changes identity near that threshold.

This gives a reliable obstruction for designing a stronger norm.  It does
not connect the reduced two-variable generating system to a scale-critical
norm for arbitrary three-dimensional velocity fields.  It does not control
all Fourier geometry, all smooth initial data, or the full Navier--Stokes
evolution.  It neither proves global regularity nor constructs blow-up.

The next question is whether the active $s=162$ obstruction survives every
admissible charge-diagonal similarity weight.  A useful R0.49 test must keep
the Banach-algebra constraints on the weights, compute the full output-charge
distribution of the active column, and either produce a certified radius
gain or prove a no-gain theorem for that weight class.  Merely tuning another
free scalar would not address the obstruction isolated here.
