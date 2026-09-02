# R0.74S Step 6 — primary audit of cross-channel recombination

## 1. Verdict

**PASS WITH A SHARP METHOD BOUNDARY.**  The algebra in (S.112)--(S.141)
is consistent.  Keeping all four completed-clock channels signed does not
produce a new estimate: it reconstructs the original stopped shell increment
sum exactly.  Keeping the mismatch separate and recombining the remaining
three channels does produce a genuine positive result.  The resulting
genealogy cutoff is nonnegative and monotone under shell insertion, all
temporal start and merge debts disappear, and the remaining work satisfies
the dissipation-corrected one-sided estimate (S.137).  The unresolved term is
then localized to the terminal nonnegative clock (S.139).

The saturation family proves an **ABSTRACT NO-GO** for the listed scalar
completed-clock axioms and the three unweighted genealogy statistics.  It is
not a Navier--Stokes field, a pressure, a dissipation measure, a PDE work
functional, or a PDE counterexample.  No PDE-weighted genealogy estimate,
cross-channel dynamical sign theorem, fixed-scale estimate, regularity result,
or singularity result is proved.  Those statements remain **OPEN / NOT
CLAIMED.  NOT CLAY.**

This is a primary mathematical self-audit.  The independent Ruby program is
an independent finite-arithmetic reconstruction, not an independent analytic
proof.

## 2. Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| `research/r074s_cross_channel_recombination_no_gain.md` | `c24d3673a5e3315777b47fa9751f8546a7df99538b6b22df7566ceb8fdce2e03` |
| `scripts/r074s_cross_channel_recombination_certificate.py` | `88644cdb311987755777fb951d1eb2ce5e0bdf0e6b829399832def0d9c54cb7c` |
| `scripts/r074s_cross_channel_recombination_certificate_independent.rb` | `cd5d7afadbaa9a257681f82d9e373777ac735c7675359310fb3a6efffc10ecef` |
| `research/r074s_cross_channel_recombination_certificate.json` | `5cd6ce5ba59586154c39cdfc5904eec4894dd51370d0cb02c0cd51bff58f4a63` |
| `research/r074s_cross_channel_recombination_certificate_report.md` | `548a68ca6ae82ea5f18e22504ee41da507569da4c283dbb8506f24b384aba189` |

## 3. Four-channel recombination: S.112--S.120

### 3.1 One-block algebra

For a fixed row \(X\in\{E,D,Q,F,K\}\), the two cutoff identities in
(S.113) are linear identities.  On one active block
\([p,q]_{\mathbb Z}\), summing the shell rows gives the two exposed boundary
terms

\[
 -\gamma_p\mathscr X_{p,R}^-
 +\gamma_q\mathscr X_{q+1,R}^+.
\]

At an internal boundary \(m\in\{p+1,\ldots,q\}\), the coefficient is

\[
 \gamma_{m-1}\mathscr X_{m,R}^+
 -\gamma_m\mathscr X_{m,R}^-
 =d_m\mathscr X_{m,R}^+ +X_{m,R}^{\partial},
 \qquad d_m=\gamma_{m-1}-\gamma_m.
\]

This proves the block identity (S.116), including the sign and index of each
root, outer, weight-drop, and mismatch term.  Decomposing the active set into
maximal blocks on each event interval gives (S.114)--(S.115).  Equivalently,
direct endpoint expansion gives the same finite identity.

**Decision: PASS.**  The proof does not differentiate the \(E\) or \(D\)
rows in time.  Their identities are used only at the selected good stopping
times and the good terminal time.  The canonical \(Q,F,K\) representatives
are available at every endpoint under the inherited convention.

### 3.2 Why the full signed route is circular

For \(X=F\), the four terms in (S.114) are exactly the stopped root, outer,
weight-drop, and mismatch work channels, so (S.117) follows.  Substituting
\(F=K-Q\) then gives

\[
 W_R^M
 =\sum_{k\in I}\Delta_{\sigma_k}^{\tau}K_{k,R}
  -\sum_{k\in I}\Delta_{\sigma_k}^{\tau}Q_{k,R}.
\]

The \(Q\)-sum is controlled by its inherited total-variation ledger.  The
\(K\)-sum is not an error term: by the defining terminal upcrossings it is
strictly larger than one quarter of the selected terminal mass.  Therefore
the exact four-channel recombination returns the quantity that the stopped
work reduction was meant to control.

**Decision: PASS.**  Here “circular” describes this particular linear
completed-clock route.  It is not a proof that every PDE-level recombination
must fail.  In particular, \(K\ge0\) does **not** give a sign for \(F\), since
\(F=K-Q\) and the available information on \(Q\) is variation control, not a
pointwise sign.

## 4. One-block scalar saturation: S.121--S.130

The abstract family has one common activation epoch, one active block after
activation, and no merger.  The recursion

\[
 B_{m+1}=B_m+\gamma_m^{-1}K_{m,R}
\]

with equal plus and minus ball clocks satisfies both cutoff and tower
identities.  The assignment \(E=K,\ D=Q=0,\ F=K\) satisfies the scalar
completion identity.  It does not construct the spatial fields or measures
from which PDE clocks would arise.

The root and mismatch rows vanish.  Direct finite summation gives

\[
 \gamma_NB_{N+1}(\tau)
 +\sum_{m=2}^{N}d_mB_m(\tau)=N.
\]

Writing the two terms as \(1+\varepsilon_N\) and
\(N-1-\varepsilon_N\) shows that the outer and weight-drop channels have the
same nonnegative sign.  For the frozen super-Gaussian weights, each ratio
\(\gamma_N/\gamma_j\), \(j<N\), has exponent gap at least the adjacent-shell
gap

\[
 \frac{4^{N-1}-4^{N-2}}{32}
 =\frac{3\cdot4^{N-2}}{32}.
\]

There are \(N-1\) ratios, which proves the stated bound for
\(\varepsilon_N\).  Consequently

\[
 W_N^{\rm sc}=N,
 \qquad Y_{2,R}^{\rm sf}=\sqrt N.
\]

No constant controlled only by scalar completion, cutoff linearity, the
tower identities, component count, activation-epoch count, and merger count
can bound \([W_N^{\rm sc}]_+\) by \(CY_{2,R}^{\rm sf}\).

**Decision: PASS — ABSTRACT NO-GO ONLY.**  The symbol \(W_N^{\rm sc}\) is
defined algebraically.  It is not the work of a constructed PDE solution.
The example does not exclude a theorem using local dissipation, pressure,
transport geometry, block length, or another Navier--Stokes observable.

## 5. Three-channel genealogy improvement: S.131--S.137

### 5.1 Positivity and insertion monotonicity

The lifted cutoff identity behind (S.132) leaves

\[
 \chi_{k+1,R}^- -\chi_{k,R}^+\ge0.
\]

The radial separation makes the later inner ball equal to one wherever the
earlier outer ball is nonzero.  Periodization preserves the pointwise
inequality by summing it over lattice translates; disjointness of different
periodic copies is not required.  Together with
\(\gamma_{k+1}\le\gamma_k\), this gives

\[
 0\le\gamma_kB_k^R+\gamma_{k+1}B_{k+1}^R
 \le\gamma_k\Psi_k^R.
\]

When shell \(k\) is inserted, at most its two adjacent boundary bumps are
subtracted.  The displayed inequality therefore proves
\(\Omega_{A\cup\{k\}}^R-\Omega_A^R\ge0\).  Inserting tied shells one at a
time in any order preserves this sign.  Hence every event increment

\[
 \delta\Omega_a
 :=\Omega_{A_a^+}^R-\Omega_{A_a^-}^R
\]

is a nonnegative spatial cutoff, and the distinct event epochs telescope to

\[
 \sum_a\delta\Omega_a=\Omega_I^R.
\]

The completed \(K\)-clock of each such cutoff is nonnegative.  Event-interval
summation then gives the exact three-channel identity (S.136), with the event
jumps subtracted.

**Decision: PASS.**  This is a positive result: temporal root, outer, and
weight-drop histories are compressed into nonnegative insertion increments
and one terminal genealogy clock.

### 5.2 Detailed sign audit of the strengthened S.137

All event times \(a\) and the terminal time \(\tau\) are local-energy good
times.  Thus \(E\) and \(D\) may be evaluated at every endpoint used below.
Expanding \(F=E+D-Q\) in (S.136) gives exactly

\[
\begin{aligned}
 W_{R,3}^M
 ={}&\Phi_I^E(\tau)
   -\sum_a\mathscr E_R[\delta\Omega_a](a)\\
 &+\Phi_I^D(\tau)
   -\sum_a\mathscr D_R[\delta\Omega_a](a)\\
 &-\left(\Phi_I^Q(\tau)
   -\sum_a\mathscr Q_R[\delta\Omega_a](a)\right).
\end{aligned}
\]

Because \(\sum_a\delta\Omega_a=\Omega_I^R\), linearity at the common
terminal time gives

\[
 \Phi_I^D(\tau)
 =\sum_a\mathscr D_R[\delta\Omega_a](\tau).
\]

The entire dissipation bracket is therefore, with no discarded term,

\[
 D_{\rm post}
 =\sum_a\left(
   \mathscr D_R[\delta\Omega_a](\tau)
  -\mathscr D_R[\delta\Omega_a](a)
  \right).
\]

Each \(\delta\Omega_a\) is nonnegative.  Its dissipation clock starts from
zero and is nondecreasing, so every summand above is nonnegative and every
insertion value \(\mathscr D_R[\delta\Omega_a](a)\) is also nonnegative.
Consequently

\[
 0\le D_{\rm post}
 =\Phi_I^D(\tau)
  -\sum_a\mathscr D_R[\delta\Omega_a](a)
 \le\Phi_I^D(\tau).
\]

The kinetic insertion values
\(\mathscr E_R[\delta\Omega_a](a)\) are nonnegative because they pair the
nonnegative kinetic density with a nonnegative cutoff.  Finally, the same
three-channel event identity for \(Q\), followed by the inherited three-row
total-variation payment, gives

\[
 \left|\Phi_I^Q(\tau)
 -\sum_a\mathscr Q_R[\delta\Omega_a](a)\right|
 \le CA_R.
\]

Dropping only the nonpositive kinetic-insertion term and using the absolute
\(Q\)-bound yields

\[
 [W_{R,3}^M]_+
 \le\Phi_I^E(\tau)+D_{\rm post}+CA_R
 \le\Phi_I^E(\tau)+\Phi_I^D(\tau)+CA_R
 =\Phi_I(\tau)+CA_R.
\]

**Decision: PASS.**  The identities, endpoint restrictions, and both signs
of the \(D_{\rm post}\) bound are correct.  No sign is assigned to \(Q\) or
\(F\).  The last inequality uses the completed local-energy identity at the
good terminal time; it does not bound the terminal clock by the quadratic
payment.

## 6. Terminal residual: S.138--S.139

Let \(B_m(t)=\mathscr K_{m,R}^+(t)\) temporarily and
\(r_m=K_{m,R}-K_{m,R}^{\partial}\ge0\).  The Step-5 tower says

\[
 r_m=\gamma_m(B_{m+1}-B_m).
\]

For one final block \([a,b]_{\mathbb Z}\), finite summation by parts gives

\[
 \gamma_bB_{b+1}
 +\sum_{m=a+1}^{b}(\gamma_{m-1}-\gamma_m)B_m
 -\gamma_aB_a
 =\sum_{m=a}^{b}r_m,
\]

which is (S.138).  Combining its
\(\gamma_a\mathscr K_{a,R}^+\) term with the negative root ball in the
block form of \(\Phi_I\) gives
\(\gamma_a(\mathscr K_{a,R}^+-\mathscr K_{a,R}^-)
=K_{a,R}^{\partial}\).  Hence

\[
 \Phi_I(t)
 =K_{a,R}^{\partial}(t)+\sum_{m=a}^{b}r_m(t)
 =K_{a,R}(t)+\sum_{m=a+1}^{b}r_m(t)
\]

on that block.  Summation over final components proves (S.139).

**Decision: PASS.**  This is an exact nonnegative decomposition: one
root-boundary term per final block and the full shell-residual
\(\ell^1\) mass.  In the scalar witness, the boundary terms vanish and all
selected residuals equal one, so \(\Phi_{I_N}(\tau)=N\).  Therefore the
three-channel estimate is sharp within the scalar algebra, while a
PDE-weighted payment for this residual remains logically possible and
**OPEN**.

## 7. Exact genealogy count: S.140--S.141

For \(n=|I|\) shells in \(c(I)\) static components, the number of internal
adjacencies is \(n-c(I)\).  Each component supplies one unconditional root
and one unconditional outer edge.  Among internal adjacencies, every unequal
pair of stopping times supplies exactly one further root or outer row, while
each tied pair supplies neither.  Therefore

\[
 |I_{\rm rt}|+|I_{\rm out}|
 =2c(I)+(n-c(I)-e_{\rm tie})
 =n+c(I)-e_{\rm tie},
\]

and adding \(|I^\partial|=n-c(I)\) gives

\[
 |I_{\rm rt}|+|I_{\rm out}|+|I^\partial|
 =2n-e_{\rm tie}.
\]

**Decision: PASS.**  In the simultaneous one-block witness,
\(c=1\) and \(e_{\rm tie}=N-1\), so the three channel families contain
\(N+1\) rows.  This is an exact \(O(N)\) complexity statement, not a
dimension-free \(\ell^2\) packing theorem.

## 8. Certificates, regression, and determinism

The frozen Python certificate reports **PASS**:

- 4/4 exact ledger rows;
- 8/8 finite checks;
- 58/58 structural checks; and
- 10/10 negative mutations.

Its finite checks cover 1,024 stopped-row configurations through five
shells; 3,276 cutoff-pair and 34,944 insertion comparisons on 182 rational
radii; 1,024 three-channel stopped configurations and 2,343 grouped event
epochs; all 78 blocks through shell 12; 65,536 genealogy configurations;
the scalar witness for \(N=1,\ldots,64\); and 2,016 exact exponent-gap
comparisons.  The strengthened (S.137) fixture separately covers 768 exact
rational density configurations, including 549 tied configurations, 525
event insertions, and 45,930 density pairings.  It checks
\(\sum_a\delta\Omega_a=\Omega_I\), nonnegative kinetic insertion, the exact
\(D_{\rm post}\) split and both of its bounds, and the \(E+D-Q\) identity and
one-sided inequalities.

The tenth Python mutation is numerical rather than textual.  On a nonempty
exact-rational cutoff and density fixture, the producer first reconstructs
\(W_3\) independently from the root, outer, and weight-drop rows and computes
\(D_{\rm post}\) from its defining time increments.  It obtains
\(D_{\rm post}=771/88\) and \(W_3=167613/9724\).  Reversing only the
post-increment signs gives \(-771/88\) and a reconstructed value
\(-1389/4862\), which is not \(W_3\).  The target inequality is not supplied
to this check.  The other nine rejected mutations change the outer-shell
index, weight-drop sign, root sign, internal max-stop, event-jump sign,
residual sign, \(D_{\rm post}\) upper bound, scalar/PDE claim boundary, or
\(\varepsilon_N\) exponent gap.

The scalar witness check also no longer assigns its three genealogy
statistics or square function as conclusions.  It forms the positive
variations explicitly, squares and sums them, and derives the component,
event, and merger counts from the simultaneous-stop active sets.

The independent Ruby Rational reconstruction reports **PASS** with 9/9
independent check groups and 8/8 numerical mutations.  Before opening the
Python JSON, it reconstructs 20,480 five-row instances of (S.115), 8,192
two-row instances and 20,202 event epochs for (S.136), 408 block fixtures for
(S.138)--(S.139), all 65,536 tied-stop genealogy configurations, and the
one-block witness through \(N=64\) with an independent decreasing rational
weight proxy.

Its dedicated \(D_{\rm post}\) reconstruction covers 1,024 stopped
configurations, 3,072 density configurations, 2,664 tied configurations, and
2,343 event insertions.  The post-dissipation increment is strictly positive
in 3,069 nonempty cases; reversing that sign produces 3,069 counterexamples.
The producer schema, required finite identifiers, note hash, category totals,
finite-row integrity, and \(D_{\rm post}\) fixture counts all pass.  Nine
separate certificate-tamper tests were rejected, 9/9: drop_omega,
corrupt_dpost, stale_categories, dummy_categories, stripped_finite,
bad_note_claim, bad_exact, bad_abel, and empty_conditions each exited with
status 1.  The last three specifically reject malformed Rational fields that
could otherwise compare as nil equal to nil, junk Abel strings, and a
vacuously true all? over an empty condition map.

Two fresh temporary output directories regenerated byte-identical Python
JSON and Markdown reports.  The Step-4 regression remains **PASS** at 14/14
exact, 4/4 finite, and 38/38 structural checks.  The Step-5 regression remains
**PASS** at 5/5 exact, 7/7 finite, 55/55 structural, and 4/4 negative checks.

**Boundary.**  These programs certify finite exact arithmetic, sampled
cutoff inequalities, statement sentinels, and deliberate mutations.  They do
not machine-prove smooth cutoff geometry, periodization, the suitable local
energy inequality, pressure-gauge cancellation, or a PDE realization of the
scalar witness.

## 9. Claim ledger and next gate

| Claim | Audit status |
|---|---|
| Universal four-channel recombination, (S.112)--(S.116) | **PROVED** |
| Identification with stopped work and circular \(K-Q\) target, (S.117)--(S.120) | **PROVED** |
| One-block scalar \(\ell^1/\ell^2\) saturation, (S.121)--(S.130) | **PROVED — ABSTRACT NO-GO, NOT PDE** |
| Nonnegative genealogy cutoff and insertion signs, (S.131)--(S.135) | **PROVED** |
| Three-channel event identity and strengthened one-sided estimate, (S.136)--(S.137) | **PROVED** |
| Terminal residual decomposition, (S.138)--(S.139) | **PROVED** |
| Exact genealogy count, (S.140)--(S.141) | **PROVED** |
| Dimension-free scalar conclusion from component/epoch/merger counts alone | **RULED OUT WITHIN THE STATED SCALAR AXIOMS** |
| PDE-weighted block-length or residual payment | **OPEN** |
| Cross-channel Navier--Stokes sign/depletion theorem | **OPEN** |
| Dissipation-dominated branch and R0.74R persistence hypotheses | **OPEN** |
| Unconditional fixed-scale (Q.1), scale contraction, or regularity | **OPEN / NOT CLAIMED** |
| Navier--Stokes existence and smoothness Millennium problem | **OPEN / NOT CLAIMED / NOT CLAY** |

The next admissible step must introduce a PDE observable that sees terminal
block length or signed transport before the local-energy information is
compressed into scalar clocks.  Returning to the positive dissipation branch
is one concrete option.  Step 6 itself supplies no such payment and makes no
novelty or priority claim.
