# R0.74S Step 17 recurrent-streamline obstruction — independent Ruby audit

## 0. Verdict and locked objects

**Verdict: PASS within the finite-audit and negative-theorem scope.**

The independent executable is
`scripts/r074s_recurrent_streamline_independent.rb`.  It is locked to:

```text
Step-16 parent   159ea3c548e51b918512855cf79959460e882b48
Step-17 core     7355c01dead23c3524242006318b02a8324447e6
Step-15 note     2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d
Step-16 note     de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0
Step-17 note     7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5
```

The primary Python producer represents the Taylor field by Gaussian-rational
Fourier Laurent polynomials.  This auditor deliberately uses a different
exact representation:

\[
 \mathbb Q[s_x,c_x,s_y,c_y]/
 (s_x^2+c_x^2-1,\ s_y^2+c_y^2-1),
 \qquad \partial_xs_x=c_x,\quad \partial_xc_x=-s_x,
\]

with the analogous \(y\)-derivation.  It neither imports nor invokes the
primary producer or its JSON output.

The final run passes all independent groups, note checks, artifact locks,
negative mutations, and reproducibility checks.  The executable contains 16
environment-selected mathematical mutations and 16 in-memory statement/byte
mutations; every one fails closed.  Three artifact-path substitutions also
fail their locks.

```text
independent exact groups     7/7 PASS   (294 assertions)
artifact and commit locks    4/4 PASS
Step-17 semantic checks     20/20 PASS  (including 31/31 unique tags)
negative mutation probes    32/32 rejected
artifact-path substitutions  3/3 rejected
reproducibility assertions  14/14 PASS
overall verdict                    PASS
```

Three additional full executions from the repository and `/`, under distinct
hash seeds, were byte-identical.  Their common stdout digest was
`b7e1d4bfa23214246c12c412f4fd767cc89330ba3b727622c7da1122ed645b6b`.

## 1. Exact algebra and topology screen

Reduction in the trigonometric quotient independently gives

\[
 \nabla\!\cdot W=0,
 \qquad \Delta W=-2W,
 \qquad (W\!\cdot\!\nabla)W=-\nabla p_W,
 \qquad W\!\cdot\!\nabla\psi=0,
\]

and

\[
 |W|^2={1\over2}-{1\over2}\cos(2x_1)\cos(2x_2),
 \qquad
 \nabla\!\cdot\left[\left({|W|^2\over2}+p_W\right)W\right]=0.
\]

The exact sample data on the oriented lower branch are

\[
 \psi(\pi/4,\pi/4)=\psi(\pi/2,\pi/6)={1\over2},
 \qquad
 g(0)={1\over2},\quad g(s_*)={3\over4},
\]

with \(s_*>0\).  At the initial point
\(W=(1/2,-1/2,0)\), so the flow points from the first sample toward the
second.  This is the direction needed for a forward positive excursion, not
merely a symmetric oscillation.

The executable also requires the main note to state the missing continuum
topology explicitly: the sine bounds, the two inverse-sine branches, their
joined endpoints, the compact connected oval, both points on the same
component, and the orbit in \(\Gamma\times\{0\}\).  These textual checks do
not purport to replace the continuum proof.

## 2. Recurrence, dimensions, and finite deletion

For \(L\ge2T_*\), the exact floor inequality

\[
 \left\lfloor{L\over T_*}\right\rfloor\ge {L\over2T_*}
\]

is checked on a deterministic rational grid, together with the exact phase
power data

\[
 L_A={\mu_RA\over2}(e^{2R^2}-1).
\]

Starting from

\[
 \dot F_{k,R}\sim R^{-1}\mu_R A^3q(\theta_A),
 \qquad
 \|h_{k,R}\|_p^p
 =R^{2p-2}\int|\dot F_{k,R}|^pdt,
\]

the audit reconstructs the pre-averaging powers

\[
 \mu_R^{p-1}R^{p-2}A^{3p-1}
\]

and, after one phase interval of length proportional to \(\mu_RA\), the
final powers

\[
 \mu_R^pR^{p-2}A^{3p}.
\]

At \(p=\infty\), \(R^2R^{-1}=R\), giving the displayed \(RA^3\)
normalization.  The signed range and completed-clock height are quadratic,
the absolute recurrent tail and complete payment are cubic, and hence
\((P_R^M)^{2/3}\) is quadratic.

For every tested \(N\), exhaustive deletion of a positive vector with
\(M=N+1\) entries confirms that at least one activated coordinate remains.
This is a finite physical-shell pigeonhole check; it does not replace the
analytic small-\(R\) cosine-positivity argument.

## 3. Positive excursion, infima, and what is actually minimal

For every fixed deletion set \(S\) and terminal time \(\tau\), the Step 15
coordinate satisfies

\[
 \sum_{k\notin S}z_k(\tau)
 \le \sum_{k\notin S}\operatorname{osc}^+F_k.
\]

The correct optimized hierarchy is therefore

\[
 \boxed{
 \sup_\tau\inf_{\#S_\tau\le N}\sum_{k\notin S_\tau}z_k(\tau)
 \le
 \inf_{\#S\le N}\sup_\tau\sum_{k\notin S}z_k(\tau)
 \le
 \mathfrak O^{F,+}_{N,R}.}
\]

The auditor checks both inequalities by exhaustive rational examples and
includes strict examples for both possible losses.  Thus no incompatible
infima are interchanged.

This also fixes the meaning of “minimal”:

- \(\operatorname{osc}^+F_k=\sup_{a<b}[F_k(b)-F_k(a)]_+\) is the smallest
  scalar, coordinatewise envelope that dominates every forward increment of
  the coordinate.
- \(\mathfrak O^{F,+}_{N,R}\) is **not** the route-minimal fixed-deletion
  sufficient target.  The middle functional above keeps one \(S\) for all
  \(\tau\) but sees only the actual hybrid increments, so it can be strictly
  smaller.
- The left-hand Step 15 gate, whose deletion may depend on \(\tau\), is weaker
  still and is the exact target required by that route.

Accordingly, (S.472) is a clean separable fixed-deletion strengthening, not
a claim of logical minimality.

## 4. Jordan and completed-clock inequalities

For finite rational paths starting at zero, exhaustive checks reproduce

\[
 \operatorname{TV}F
 =|F(t_0^-)|+2\min\{\operatorname{Var}^+F,
                         \operatorname{Var}^-F\}.
\]

A recurrent triangular clock with \(m\) circuits has

\[
 \operatorname{osc}^+F=\sup K=1,
 \qquad \operatorname{Var}^+K=m,
 \qquad \operatorname{TV}F=2m.
\]

This is an exact finite model of the distinction between height and repeated
backtracking.

For each fixed \(S\), the auditor first checks the coordinatewise facts for
\(F=K-Q\), \(K\ge0\), and common zero start:

\[
 o_F\le m_K+\operatorname{TV}Q,
 \qquad m_K\le o_F+\operatorname{TV}Q,
\]

\[
 \operatorname{Var}^+K\le\operatorname{TV}F+\operatorname{TV}Q,
 \qquad
 \operatorname{TV}F\le2\operatorname{Var}^+K+\operatorname{TV}Q,
 \qquad m_K\le\operatorname{Var}^+K.
\]

Only then does it optimize, paying the full
\(B_{Q,R}=\sum_k\operatorname{TV}Q_{k,R}\).  This proves all five directions
in (S.475); it does not assume that one deletion set minimizes two different
functionals.

## 5. The recurrent Taylor family against \(\mathfrak O^{F,+}\) and
\(\mathfrak M^K\)

The ordered phases in the locked note satisfy

\[
 \theta_A(a)=-T_*,\qquad
 \theta_A(b)=-T_*+s_*,\qquad a<b,
\]

and give, for every activated shell,

\[
 F_{k,R}(b)-F_{k,R}(a)
 ={\gamma_kc_{k,R}\over2R}
 \left({A^2\over4}+O_R(A)
       +4\int_a^bb_A^2g(\theta_A)\,dt\right)>0.
\]

Together with the signed-range upper bound and the \(N+1\) pigeonhole, this
gives

\[
 \mathfrak O^{F,+}_{N,R}\asymp_{N,R}A^2.
\]

The completed clock has the same scale.  The upper bound follows immediately
from (S.475) and \(B_{Q,R}=O_R(A^2)\):

\[
 \mathfrak M^K_{N,R}
 \le\mathfrak O^{F,+}_{N,R}+B_{Q,R}=O_{N,R}(A^2).
\]

For the lower bound, use the frozen identity \(K=E+D\), with \(D\ge0\).
At terminal good times the localized kinetic energy on each of the first
\(N+1\) activated shells is a positive fixed \((k,R)\)-constant times
\(A^2\).  Hence every deletion of at most \(N\) indices leaves one coordinate
with \(\sup_tK_{k,R}(t)\gtrsim_{k,R}A^2\), and

\[
 \mathfrak M^K_{N,R}\asymp_{N,R}A^2.
\]

Thus this recurrent family is compatible with both the positive-excursion
and maximal-height payments, while
\(\mathfrak H^F_{1,N,R}\asymp A^3\) refutes the absolute-variation target.
The lower bound for \(\mathfrak M^K\) is an analytic consequence of the
frozen clock definitions; the executable checks its exact amplitude
bookkeeping, not the continuum positivity constant.

## 6. Claim boundary and limitations

The audited claim boundary is:

- (S.444) and every power-only absolute temporal-tail estimate with
  \(\beta<1\) are false on the smooth recurrent Taylor family.  For
  \(\beta<0\), the comparison correctly uses the lower, not upper, payment
  bound because a negative power reverses inequalities.
- (S.472), the fixed-deletion positive-excursion estimate, remains open.
- The weaker direct Step 15 hybrid gate, terminal-crown route, Q.12, Q.1,
  scale contraction, and regularity remain open.
- This is not a proof of regularity or the Millennium problem.  **NOT CLAY.**

The finite auditor does not machine-prove the compact regular-level theorem,
arbitrary-mollifier positivity, continuum payment constants, or either open
terminal estimate.  It checks exact algebra, finite combinatorics, exponent
bookkeeping, equation inventory, dependency hashes, and claim labels.

## 7. Reproduction

From the repository root:

```bash
ruby scripts/r074s_recurrent_streamline_independent.rb
```

The script internally reruns its stable payload from both the repository and
`/`, under four distinct `RUBY_HASH_SEED` values, and requires byte-identical
JSON.  It also launches every negative mutation in a fresh Ruby process and
requires a nonzero exit with a structured failing verdict.
