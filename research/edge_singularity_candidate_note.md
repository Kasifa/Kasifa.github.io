# R0.32: certified finite singularity-candidate diagnostics on the charge-one edge

## Status and boundary

R0.31 proves a common analytic polydisc for the two-variable edge fields

\[
 a(Z,W),\qquad U(Z,W),\qquad V(Z,W),
\]

but it does not locate their first singular variety.  This note takes the
next finite, auditable step.  It identifies the one-variable functions that
actually generate the endpoint sequence, extends their exact rational
coefficients from endpoint parameter (N=40) to (N=50), and applies a
multi-truncation D-log Padé diagnostic with exact polynomial root isolation.

The main finite result is a narrow and stable negative-real candidate cluster
near

\[
 R=-0.7495
\]

for both normalized transport fields.  Every reported Padé denominator,
root interval, noncancellation test, and residue sign is exact.  The location
is nevertheless **not** a certified singularity of the original series:
there is not yet a validated analytic-continuation path or a remainder bound
reaching the cluster.  Stability of finitely many rational approximants is
evidence, not a convergence theorem.

This note concerns the reduced edge system.  It neither proves a singularity
nor global regularity for three-dimensional Navier--Stokes.

## 1. The correct one-variable object is a fixed-charge extraction

Use the R0.29 variables

\[
 R=Z^2W,\qquad \Xi=Z^{-1},\qquad
 Z^nW^k=R^k\Xi^q,\qquad q=3k-(n+k).
\]

For a bivariate field (F), define its charge-(q) generating function by

\[
 F_q(R)=[\Xi^q]F(R,\Xi)
       =\sum_k f_{k,q}R^k.
\tag{1.1}
\]

The edge endpoint has (q=1) and total degree (3N-1).  Therefore

\[
 A_1(R)=\sum_{N\ge1}a_NR^N,\qquad
 U_1(R)=\sum_{N\ge1}u_NR^N,\qquad
 V_1(R)=\sum_{N\ge1}v_NR^N
\tag{1.2}
\]

generate exactly the coefficients studied in R0.27--R0.28.  The sharp
combination at the certified root-box center is

\[
 D_1(R)=p_*U_1(R)+q_*V_1(R).
\tag{1.3}
\]

This is a diagonal or fixed-charge extraction, not a substitution such as
(Z=W).  A geometric substitution mixes all charges and cannot by itself
explain the fixed-charge endpoint asymptotics.

## 2. A new all-order consequence of the R0.31 majorant

Let (K=81/4).  R0.31 proves

\[
 \sum_k |U_{L,k}|,\ \sum_k |V_{L,k}|
 \le \frac{K^{L-1}}{L^3}.
\tag{2.1}
\]

At fixed charge (q), the coefficient of (R^k\Xi^q) has total degree
(L=3k-q).  Hence

\[
 |f_{k,q}|\le
 \frac{K^{3k-q-1}}{(3k-q)^3}.
\tag{2.2}
\]

The root test now gives the following all-order statement.

### Theorem 1: fixed-charge analyticity

For each fixed integer charge (q), every fixed-charge transport series is
absolutely analytic on

\[
 \boxed{|R|<K^{-3}=\left(\frac4{81}\right)^3
 =\frac{64}{531441}.}
\tag{2.3}
\]

The same conclusion holds for a fixed linear combination such as (D_q).
This is only a guaranteed lower bound.  Its decimal value is about
(1.20427\times10^{-4}), far inside the finite candidate near (0.7495).
Thus R0.31 alone does not justify evaluation at the candidate.

## 3. Exact D-log Padé construction

Because each charge-one series begins at (R^1), write

\[
 \widehat F(R)=\frac{F_1(R)}R,
 \qquad
 G_F(R)=\frac{\widehat F'(R)}{\widehat F(R)}.
\tag{3.1}
\]

If an actual continuation has the local form

\[
 \widehat F(R)=C(R)(1-R/R_*)^{-\gamma},
 \qquad C(R_*)\ne0,
\tag{3.2}
\]

then (G_F) has a simple pole at (R_*) with residue (-\gamma).
Conversely, a zero of multiplicity (m) gives residue (+m).  These are
elementary local identities; using them to infer a singularity from a finite
Padé table still requires a separate convergence theorem.

For each even coefficient cut

\[
 c=30,32,\ldots,50,
\]

the audit constructs the diagonal approximant

\[
 [m/m]_{G_F},\qquad m=(c-2)/2.
\tag{3.3}
\]

The Padé equations are solved over exact rational numbers.  This follows the
standard definition (P-fQ=O(R^{2m+1})); see
[NIST DLMF §3.11(iv)](https://dlmf.nist.gov/3.11.iv).

For every approximant the program then:

1. converts numerator and denominator to primitive integer polynomials;
2. isolates real denominator roots by exact Sturm methods;
3. proves the selected root is simple;
4. proves the numerator is nonzero on its isolating interval;
5. encloses the residue by exact rational interval arithmetic;
6. repeats the root evaluation at 160 and 256 bits.

The root-isolation intervals are narrower than (10^{-32}).  Their small
width certifies the finite rational objects; it does not measure uncertainty
in the unknown singularity of (F_1).

## 4. Finite exact theorem for the transport candidate cluster

### Theorem 2: exact approximant-pole cluster

For each of the 22 pairs

\[
 F\in\{U_1,V_1\},\qquad c\in\{30,32,\ldots,50\},
\]

the exact diagonal D-log Padé denominator has exactly one simple real root in

\[
 I=(-0.7500,-0.7493).
\tag{4.1}
\]

At that root the exact numerator enclosure excludes zero, the numerator and
denominator have polynomial gcd one, and the residue satisfies

\[
 \operatorname{Res}[m/m]_{G_F}< -\frac12.
\tag{4.2}
\]

Across all 22 approximants, the isolated roots have the finite cluster hull

\[
 [-0.7497011962871,\,-0.7494330796399].
\tag{4.3}
\]

Restricting to the five highest cuts (c=42,44,46,48,50) for both fields
shrinks the hull to approximately

\[
 [-0.7494997362888,\,-0.7494330796399],
\tag{4.4}
\]

whose width is less than (10^{-4}).  The approximate residue range over the
full table is

\[
 -0.56158<\operatorname{Res}<-0.52271.
\tag{4.5}
\]

If the approximants converge in the required local sense, the sign in (4.2)
would be consistent with an algebraic branch exponent between about (0.52)
and (0.56).  The antecedent is not proved, so (4.5) is a candidate-exponent
diagnostic, not an exponent theorem.

## 5. A closer object in the sharp combination is classified as a zero

The root-center combination (D_1=p_*U_1+q_*V_1) has a still closer stable
D-log Padé pole near

\[
 R=-0.723449.
\]

Its residues over the same eleven cuts lie between approximately (0.9925)
and (1.0223), and the high-cut values approach (+1).  Under the local
identity (3.1), a positive unit residue is the signature of a simple zero,
not a singularity.  The high-cut zero-candidate cluster has width below
(2\times10^{-6}).

This distinction matters.  Ranking Padé poles only by modulus would call
the (D_1) object “nearer” and misidentify a likely cancellation zero as a
singularity candidate.  The D-log residue and the separate (U_1,V_1)
diagnostics prevent that error.

## 6. What is certified and what remains conjectural

The following are certified finite statements:

- every edge coefficient through total degree 149 is an exact GMP rational;
- the first 40 endpoints reproduce the R0.28 certificate exactly;
- checkpoint/resume reproduces a fresh recurrence coefficient for coefficient;
- all selected Padé polynomials and their gcds are exact;
- every candidate interval contains exactly one simple real approximant pole;
- numerator noncancellation and residue signs are exact interval statements;
- 160- and 256-bit root evaluations lie inside the exact isolating result.

The following are not proved:

- (U_1) or (V_1) has a singularity inside the finite cluster hull;
- the nearest actual singularity is real or lies on the negative axis;
- there is no closer complex singularity;
- the diagonal Padé sequence converges for these functions;
- the candidate controls the endpoint asymptotic or gives an exact radius;
- any conclusion transfers from the reduced edge system to the full PDE.

General Padé convergence results require analytic structure not yet proved
here.  For example, Stahl's theorem treats functions satisfying specific
multivalued-analytic and capacity hypotheses; see
[Stahl, *Journal of Approximation Theory* 91 (1997)](https://doi.org/10.1006/jath.1997.3141).
Invoking such a theorem before verifying its hypotheses for the fixed-charge
edge functions would be circular.

## 7. Research value and next theorem target

R0.32 replaces a visual ratio extrapolation by a reproducible and exactly
classified finite candidate.  It also identifies the first plausible
location at which a continuation proof should concentrate.  That is useful,
but it remains several logical steps from a singularity theorem for the edge
system and much farther from the three-dimensional Millennium Problem.

The next acceptable advance is one of the following.

1. Prove an eventual parity-twisted positivity theorem for (U_1,V_1), plus
   a finite upper bound on their radius.  Pringsheim-type reasoning would
   then force a negative-axis singularity after undoing the twist.
2. Construct a validated analytic-continuation chain toward the negative
   axis using Taylor models or interval Newton/Krawczyk steps, with a rigorous
   tail enclosure at every center.
3. Prove that the fixed-charge series belongs to a class for which the chosen
   Padé sequence converges, and verify the hypotheses rather than assuming
   them.

Without one of these bridges, increasing the Padé order alone would only
refine a conjectural location.

The exact computation is implemented in
`research/edge_singularity_candidate_audit.py`.  Its recurrence writes atomic
compressed checkpoints and can resume after interruption.  The formal run
archives the machine-readable certificate, progress log, resource samples,
and journal-figure data separately.
