# R0.74S Step 6 — independent audit of cross-channel recombination

## Result

**PASS.  NO UNRESOLVED BLOCKER.**

The analytic argument was reconstructed independently from the frozen
definitions in R0.74S Steps 2--5.  A separate Ruby Rational program then
recomputed the stopped-row identities, grouped activation events, the
dissipation-corrected \(D_{\rm post}\) ledger, blockwise Abel algebra,
genealogy counts, and scalar witness without importing or invoking the Python
producer.

The proved endpoint is an **ABSTRACT SCALAR NO-GO** for linear completed-clock
recombination plus unweighted block genealogy.  It is not a velocity,
pressure, work density, dissipation measure, Navier--Stokes solution, or PDE
counterexample.  The unconditional fixed-scale estimate (Q.1), regularity,
singularity formation, and the Clay Millennium problem remain
**OPEN / NOT CLAIMED**.  **NOT CLAY.**

## 1. Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| `research/r074s_cross_channel_recombination_no_gain.md` | `c24d3673a5e3315777b47fa9751f8546a7df99538b6b22df7566ceb8fdce2e03` |
| `scripts/r074s_cross_channel_recombination_certificate.py` | `88644cdb311987755777fb951d1eb2ce5e0bdf0e6b829399832def0d9c54cb7c` |
| `scripts/r074s_cross_channel_recombination_certificate_independent.rb` | `cd5d7afadbaa9a257681f82d9e373777ac735c7675359310fb3a6efffc10ecef` |
| `research/r074s_cross_channel_recombination_certificate.json` | `5cd6ce5ba59586154c39cdfc5904eec4894dd51370d0cb02c0cd51bff58f4a63` |
| `research/r074s_cross_channel_recombination_certificate_report.md` | `548a68ca6ae82ea5f18e22504ee41da507569da4c283dbb8506f24b384aba189` |

## 2. Four-channel stopped-row recombination — PASS

For any one of the five linear rows \(X\in\{E,D,Q,F,K\}\), the two cutoff
identities give

\[
 X_k=\gamma_k(\mathscr X_{k+1}^+-\mathscr X_k^-),
 \qquad
 X_m^\partial=\gamma_m(\mathscr X_m^+-\mathscr X_m^-).
\]

On a maximal active block \([p,q]_{\mathbb Z}\), direct collection of the
coefficient of each internal ball cutoff gives

\[
 \sum_{k=p}^{q}X_k
 =-\gamma_p\mathscr X_p^-
  +\gamma_q\mathscr X_{q+1}^+
  +\sum_{m=p+1}^{q}
    \bigl[d_m\mathscr X_m^++X_m^\partial\bigr].
\]

The coefficient check is exact because

\[
 \gamma_{m-1}\mathscr X_m^+-\gamma_m\mathscr X_m^-
 =d_m\mathscr X_m^+
  +\gamma_m(\mathscr X_m^+-\mathscr X_m^-).
\]

Root, outer, and internal-boundary activation intervals are respectively
\((\sigma_k,\rho_k]\), \((\sigma_k,\lambda_k]\), and
\((\widehat\sigma_m,\tau]\).  Integrating the block identity over these
finite event cells therefore yields (S.115), including when several stops
coincide.  Equivalently, one may expand all endpoint values directly.  The
latter proof uses \(E,D\) only at good endpoints and requires no time
differentiability of those rows.

The independent Ruby audit evaluated five unrelated rational row fixtures
over all six-shell masks and three-valued stop maps.  All **20,480**
stopped-row configurations, including ties, passed exactly.

## 3. Genealogy cutoff and periodization — PASS

On the Euclidean lift, the Step-5 cutoff identities imply

\[
 \psi_k-\beta_k-\beta_{k+1}
 =\chi_{k+1}^- -\chi_k^+.
\]

If \(\chi_k^+>0\), then the radius lies below \(r_k+\delta\).  Since
\(r_{k+1}-r_k>2\delta\), it lies in the region where
\(\chi_{k+1}^-=1\).  If \(\chi_k^+=0\), nonnegativity is immediate.  Hence

\[
 \beta_k+\beta_{k+1}\le\psi_k.
\]

Multiplication by the decreasing weights gives

\[
 \gamma_k\beta_k+\gamma_{k+1}\beta_{k+1}
 \le\gamma_k\psi_k.
\]

This lifted inequality may be summed term by term over every lattice
translate.  Overlap between different periodic copies causes no problem,
because every summand has the same nonnegative orientation.  This proves
(S.132) for the periodizations and, in turn, the insertion monotonicity
(S.133).  Thus every grouped increment

\[
 \delta\Omega_a=\Omega_{A_a^+}-\Omega_{A_a^-}
\]

is a smooth nonnegative cutoff, even when the stop \(a\) is shared by
several shells.

## 4. Grouped events and the \(D_{\rm post}\) repair — PASS

For each constant-active-set event interval, integrate the fixed genealogy
cutoff and telescope.  At a shared stop, insert the tied shells in any
order; the total cutoff increment is still exactly
\(\delta\Omega_a\).  This reconstructs

\[
 W_{R,3}^M
 =\Phi_I^F(\tau)
  -\sum_a\mathscr F_R[\delta\Omega_a](a),
\]

which is (S.136).  Two independent rational row fixtures passed **8,192**
stopped configurations and **20,202** grouped activation epochs.

The strengthened estimate (S.137) also has the correct dissipation
bookkeeping.  Expanding \(F=E+D-Q\) gives the exact identity

\[
\begin{aligned}
 W_{R,3}^M
 ={}&\Phi_I^E(\tau)
 -\sum_a\mathscr E_R[\delta\Omega_a](a)
 +D_{\rm post}\\
 &-\left(
   \Phi_I^Q(\tau)
   -\sum_a\mathscr Q_R[\delta\Omega_a](a)
  \right),
\end{aligned}
\]

where

\[
 D_{\rm post}
 =\sum_a\left(
   \mathscr D_R[\delta\Omega_a](\tau)
   -\mathscr D_R[\delta\Omega_a](a)
  \right).
\]

Each insertion energy is nonnegative.  Each summand in \(D_{\rm post}\)
is nonnegative because the dissipation row for a nonnegative cutoff is
nondecreasing.  Moreover,
\(\sum_a\delta\Omega_a=\Omega_I\) and
\(\mathscr D_R[\delta\Omega_a](a)\ge0\), so

\[
 0\le D_{\rm post}\le\Phi_I^D(\tau).
\]

The remaining \(Q\)-combination is exactly the root/outer/gap quadratic
combination and is bounded by the Step-5 total-variation ledger.  Dropping
the nonnegative insertion energies therefore yields

\[
 [W_{R,3}^M]_+
 \le\Phi_I^E(\tau)+D_{\rm post}+CA_R
 \le\Phi_I(\tau)+CA_R.
\]

The Python producer separately checked this \(D_{\rm post}\) expansion on
768 rational density configurations, including 549 configurations with tied
stops.  The Ruby auditor now supplies a second construction, using its own
nonnegative rational genealogy cutoffs, nonnegative \(E\), pointwise monotone
\(D\), and three signed \(Q\) fixtures.  It passes all **1,024** stopped
configurations and **3,072** density configurations, including **2,664** tied
configurations and **2,343** grouped events.  The three empty-set fixtures are
the only zero-\(D_{\rm post}\) cases; all **3,069** nonempty fixtures have
strictly positive \(D_{\rm post}\).  Reversing the time-increment sign produces
**3,069** exact counterexamples.  These are finite verifications of the
displayed algebra, not machine proofs of the suitable local-energy identity.

## 5. Terminal block decomposition — PASS

At a fixed admissible time set

\[
 B_m=\mathscr K_m^+,
 \qquad
 r_m=K_m-K_m^\partial
     =\gamma_m(B_{m+1}-B_m)\ge0.
\]

For every final component \([a,b]_{\mathbb Z}\), finite summation by parts
gives

\[
 \gamma_bB_{b+1}
 +\sum_{m=a+1}^{b}d_mB_m
 =\gamma_aB_a+\sum_{m=a}^{b}r_m.
\]

Subtracting the root ball \(\gamma_a\mathscr K_a^-\) and using
\(\gamma_a(\mathscr K_a^+-\mathscr K_a^-)=K_a^\partial\) gives both
equivalent forms in (S.139):

\[
 \Phi_{[a,b]}
 =K_a^\partial+\sum_{m=a}^{b}r_m
 =K_a+\sum_{m=a+1}^{b}r_m.
\]

Thus the favorable genealogy signs remove intermediate stop and merge
clocks, but the terminal object still contains the full nonnegative
\(\ell^1\) residual mass.  The Ruby audit independently tested all blocks
through shell 16 with three rational data families: **408** block fixtures
passed exactly.

## 6. Exact genealogy counts — PASS

Let \(n=|I|\), let \(c(I)\) be the number of connected components, and let
\(e_{\rm tie}\) count internal adjacent pairs with equal stops.  Every
component supplies one unconditional root and one unconditional outer edge.
Every unequal internal adjacent pair supplies exactly one additional root
or outer edge; every tied pair supplies neither.  Consequently

\[
 |I^\partial|=n-c(I),
\]

\[
 |I_{\rm rt}|+|I_{\rm out}|
 =n+c(I)-e_{\rm tie},
\]

and

\[
 |I_{\rm rt}|+|I_{\rm out}|+|I^\partial|
 =2n-e_{\rm tie}.
\]

The Ruby audit verified all three equalities for **65,536** eight-shell
configurations with tied stops.  This proves only \(O(n)\) finite event
complexity.  It is not a dimension-free Carleson or matched-\(\ell^2\)
bound.

## 7. One-block scalar witness — PASS WITH STRICT BOUNDARY

The witness assigns

\[
 K_k=F_k=h,\qquad E_k=K_k,\qquad D_k=Q_k=0
 \quad(1\le k\le N),
\]

sets every boundary clock to zero, and recursively defines the equal plus
and minus ball clocks from the scalar tower.  These assignments satisfy the
scalar completion and cutoff identities.  They do not construct a spatial
cutoff operator, velocity, pressure, nonlinear work vector, or
Navier--Stokes solution.

With one common stop, the active set jumps from empty to the single block
\([1,N]_{\mathbb Z}\).  There is one activation epoch and no block merger.
Exact finite telescoping gives

\[
 \mathfrak C_K^{\rm out}=1+\varepsilon_N,
 \qquad
 \mathfrak C_K^{\rm gap}=N-1-\varepsilon_N,
\]

and hence

\[
 W_N^{\rm sc}:=\mathfrak C_F
 =\mathfrak C_K=N,
 \qquad
 Y_{2,R}^{\rm sf}=\sqrt N.
\]

The notation \(W_N^{\rm sc}\) denotes only the value of the abstract scalar
functional.  It is not the work of a constructed PDE solution.  The Ruby
audit reconstructed this witness independently for every
\(N=1,\ldots,64\), using a different rational decreasing weight family from
the Python producer.  It computes \(Y_2^2\) by summing the squares of the
\(N\) unit variations, and derives root, outer, internal-edge, epoch, and
merger counts from the active set, common stop map, connected components, and
tie count.  Every case passed.

This witness rules out a uniform \(CY_2\) estimate derived only from the
listed scalar identities and the unweighted statistics “one block, one
epoch, zero mergers.”  It does not rule out a PDE theorem that charges
block length or clock amplitude to dissipation, signed transport, pressure,
or another Navier--Stokes quantity.

## 8. Independent executable verification

The Ruby Rational auditor reports:

    9/9 independent reconstruction families    PASS
    8/8 numerical mutations                     PASS
    Python producer cross-check                 PASS

Its eight numerical mutations independently reject:

1. replacing the outer \(k+1\) ball by the \(k\) ball;
2. reversing the root sign;
3. reversing the weight-drop sign;
4. replacing the internal maximum stop by the minimum stop;
5. adding rather than subtracting grouped event jumps;
6. reversing the gap sign in the block Abel identity;
7. deleting the terminal outer term from the scalar witness; and
8. reversing the time increment in \(D_{\rm post}\).

The Python producer independently reports:

    4/4 exact ledger rows       PASS
    8/8 finite checks           PASS
    58/58 structural checks     PASS
    10/10 negative mutations    PASS

The Ruby program opens the Python JSON only after completing all of its own
rational arithmetic; no producer number is used as a mathematical input.  In
addition to the stopped-row, event, \(D_{\rm post}\), Abel, genealogy, and
witness reconstructions, it independently evaluates Omega insertion
monotonicity on **119** weighted pairs and **7,616** insertion-point
comparisons, and checks all **2,016** epsilon exponent gaps for
\(N=2,\ldots,64\).

The producer cross-check freezes the complete expected identifier sets and
totals (4 exact, 8 finite, 58 structural, and 10 negative), requires unique
identifiers and row-level PASS states, and recomputes every summary count from
the corresponding arrays.  Each of the eight finite rows has an
identifier-specific schema and count audit; required failure arrays must be
present and empty.  The note path, note hash, and all claim-boundary fields are
also checked.

Nine in-memory adversarial regressions were run without changing the frozen
JSON.  Deleting the Omega row; inserting a nonempty \(D_{\rm post}\) failure
while zeroing its counts but leaving `pass=true`; clearing category arrays
while leaving a stale summary; replacing whole categories by self-consistent
dummy PASS rows; stripping seven finite rows down to `{id, pass}` shells; and
altering the note path and Clay boundary were all rejected.  Three further
attacks---two unparsable exact rationals, three equal but nonnumeric Abel
fields, and empty condition maps in every witness and epsilon row---were also
rejected.  Each attack made the Ruby auditor exit with status 1 and report
FAIL.  The SHA-256 table above remains the integrity anchor for the complete
frozen artifact set.

## Final boundary

The exact four-channel recombination is circular: it reconstructs the
unknown stopped shell increment sum.  The stronger three-channel genealogy
argument genuinely removes intermediate stop and merger clocks, but ends at
the terminal nonnegative \(\ell^1\) quantity in (S.139).  The one-block
scalar witness proves that component, epoch, and merger counts alone cannot
compress this terminal mass to the matched square function.

This is a method-level algebraic conclusion only.  A PDE-weighted genealogy
theorem, cross-channel dynamical sign estimate, quadratic treatment of the
dissipation-dominated branch, the R0.74R persistence hypotheses, the
unconditional fixed-scale inequality (Q.1), scale contraction, regularity,
singularity formation, and the Clay Millennium problem remain
**OPEN / NOT CLAIMED**.

**INDEPENDENT AUDIT PASS.  ABSTRACT SCALAR NO-GO ONLY.  NOT CLAY.**
