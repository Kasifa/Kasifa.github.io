# R0.74S Step 15 — independent Ruby audit of the hybrid and crown notes

## 1. Verdict and locked objects

**PASS within the finite algebraic, combinatorial, conditional, and abstract
scopes stated below.  The PDE estimates (S.342), (S.375), and (S.407) remain
OPEN.  NOT CLAY.**

The audit binds the two reviewed notes exactly.

| Object | Equation range | SHA-256 |
|---|---:|---|
| `research/r074s_hybrid_flux_tail_equivalence.md` | (S.377)--(S.397) | `2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d` |
| `research/r074s_terminal_crown_coercivity.md` | (S.398)--(S.416) | `c62fc127c6d6381075653819a4672cae69f1ac4e2b7b45ee2d0b033ab770fd80` |
| Independent verifier `scripts/r074s_hybrid_crown_certificate_independent.rb` | finite reconstruction | `e21f186f65052335a2ad97f1fd3dfdeada0d548c9369b7040adb77436320af0e` |

The independent verifier produced this result.

| Audit group | Passed | Total |
|---|---:|---:|
| Independent algebraic/combinatorial groups | 8 | 8 |
| Exact finite cases inside those groups | 127,683 | 127,683 |
| Hash, label, formula, and claim-boundary sentinels | 49 | 49 |
| Adversarial source mutations rejected | 22 | 22 |
| Adversarial primary-artifact mutations rejected | 8 | 8 |
| Primary producer validation errors | 0 | 0 |

The Ruby implementation uses exact `Rational` arithmetic and generates its
finite vectors, deletion sets, trees, crowns, and incidence rows from first
principles.  It does not invoke or import the Python producer.  Only after all
independent groups and source mutations have been evaluated does it read the
primary JSON for a one-way consistency check.

## 2. Hybrid flux and common deletion

For the selected-excess branch, normalize by one terminal value \(T>0\) and
write

\[
 z=T-U-V,\qquad r={T\over3}-V,\qquad |U|+|V|<{T\over6}.
\]

The verifier independently expanded the two margins

\[
 5r-z={2T\over3}+U-4V,\qquad
 3z-7r={2T\over3}-3U+4V.
\]

Exact enumeration on the correlated \((U,V)\)-diamond gave both margins
strictly positive.  Rational sequences approaching the two boundary faces
recovered

\[
 {r\over z}\downarrow {1\over5},\qquad
 {r\over z}\uparrow {3\over7}.
\]

The endpoint constants are therefore sharp for the stated scalar ledger.
This is not a sharpness claim for Navier--Stokes solutions.

For every generated nonnegative pair satisfying
\(z_k/5\le r_k\le z_k\), the verifier enumerated every deletion set of size
at most \(N\).  It checked the comparison first on the same complement and
only then minimized:

\[
 {1\over5}\mathcal S_N(z)
 \le \mathcal S_N(r)
 \le \mathcal S_N(z).
\]

No union of two branchwise exceptional sets enters this calculation.  The
\(N+1\) equal-coordinate fixture also leaves exactly one height after every
deletion of at most \(N\) shells.

The interval-length factor in (S.386)--(S.390) was checked separately.  Exact
powered inequalities for \(p=1,2,3,\infty\), together with exponent arithmetic,
retain \(4^{1-1/p}\), including the factor \(4\) at \(p=\infty\).  This verifies
the finite algebra of the implication from (S.342); it does not prove (S.342).

## 3. Common-window debt

The audit reconstructed (S.393) without using the primary fixture.  With
\(F=K-Q\) and \(K(\ell)=2T/3\), exact subtraction gives

\[
 F(\tau)-F(\ell)
 =F(\tau)-F(a)+K(a)-{2T\over3}+Q(\ell)-Q(a).
\]

The identity was checked over independent rational choices of \(T\), \(K(a)\),
and the three clock values.  Finite vectors were then summed outside every
common deletion set.  Positive part was applied only after the signed common
window was summed, the positive start overshoot was retained, and the full
\(Q\)-prefix variation was paid once.

The scalar row \(T=3\), \(K(a)=M>3\), \(Q=0\) reproduces

\[
 r=1,\qquad G=3-M,\qquad\omega=M-2,\qquad r=G+\omega.
\]

Thus the start-clock term is a real algebraic debt.  The row is only an
abstract clock check.

## 4. Jump trees, terminal crowns, and incidence payment

For rational \(\kappa>1\) and depths through ten, the audit recovered

\[
 C_{\kappa,L}
 =1+\sum_{j=0}^{L}\kappa^{-j}
 =1+{\kappa\over\kappa-1}
      \left(1-\kappa^{-(L+1)}\right)
 \le {2\kappa-1\over\kappa-1}.
\]

It then generated a 32-child depth-three tree with three first roots, three
first jump children per root, and two second jump children per retained node.
The resulting 31 terminal crowns partitioned all 32,768 leaves exactly once.
Deleting one terminal-depth crown made the partition fail.

The occurrence ledger retained shifted-grid, periodic-copy, and shell labels.
Collapsing geometrically repeated rows reduced the weighted top content and was
therefore detected.  The depth-independent coefficient bound remained valid
only when all occurrences were counted with multiplicity.

For coefficient \(c_i=\gamma_{k_i}\rho_{S_i}\), the canonical payment was
parameterized without numerical square roots as

\[
 a_i=c_i s_i^2,\qquad p_i=c_i s_i^3.
\]

This gives \(a_i^3=p_i^2c_i\) exactly and verifies the finite Hölder closure

\[
 \left(\sum_i a_i\right)^3
 \le\left(\sum_i c_i\right)\left(\sum_i p_i\right)^2.
\]

Two equal incidence occurrences require two payments.  Reusing one payment
fails this check.

## 5. Converse Hölder and scaled stress tests

Direct exact enumeration verified

\[
 \sum_i{a_i^3\over p_i^2}\ge
 {\left(\sum_i a_i\right)^3\over\left(\sum_i p_i\right)^2},
\]

with equality for \(p_i=P a_i/A\).  Cube-parameterized fixtures independently
recovered the threshold factor \(1/8\) in (S.411) and removed all radicals from
the tradeoff in (S.412).

Scaling the Step 11 scalar constants by \(5H/3\) reproduced every rational
value in (S.415), including both strict inequalities.  The independent tree
calculation also recovered

\[
 \rho_d=2^{-d}\rho_0,\qquad m_d=8^{-d}m_0,\qquad
 {m_d\over\rho_d}=4^{-d}{m_0\over\rho_0}.
\]

Finally, \(N+1\) flat coordinates give

\[
 \mathcal S_N(b)=H,\qquad
 \left({\mathcal S_N(b)\over(C_MH)^{2/3}}\right)^3
 ={H\over C_M^2},
\]

which is the cubed form of the divergence in (S.416).

The periodic positive measure and the selected scalar clock remain two
separate stress tests.  They are not a coupled completed-clock/measure fixture
and are not an NSE realization.

## 6. Adversarial checks and one corrected producer label

The source validator was rerun with hash enforcement disabled after each
targeted mutation.  It rejected changes to the \(T/6\) diamond, the \(1/5\)
constant, the best-\(N\) direction, the length-four exponent, coefficient six,
the debt sign, first-root direction, terminal-depth crown, jump decay,
canonical \(3/2\) payment, the OPEN status of (S.407), converse cube, factor
eight, periodic-copy sum, scaled \(\sigma\), common-deletion wording,
uncoupled-fixture warning, occurrence-payment rule, final equation tag, and
line-ending integrity.

The independent audit initially rejected one primary-certificate label.  The
producer had called the periodic measure and scalar clock a coupled ledger,
contrary to both locked notes.  The label was corrected to
`TWO_SEPARATE_ABSTRACT_STRESS_TESTS_NOT_COUPLED_NOT_NSE`, and the primary
producer was regenerated.  The accepted primary bundle is:

| Primary artifact | SHA-256 |
|---|---|
| `scripts/r074s_hybrid_crown_certificate.py` | `84c1d8aac5399b71a98cefc4a8ff6a0e13835c8a19e47bd5693ac76fe2bcced4` |
| `research/r074s_hybrid_crown_certificate.json` | `38e4d15c76b4bb9a2523173c0da816d6862f9e24fe59595d9953a7aa9516a7b8` |
| `research/r074s_hybrid_crown_certificate_report.md` | `6777bc9cbfdaf0d079407e24269822e52bb36ffda13b828bdd7440a554050d87` |

Eight primary-artifact mutations were also rejected: false overall status,
stale note hash, missing finite row, failed structural row, stale summary,
promotion of (S.407), false coupling of the stress tests, and a Millennium
claim.

The verifier passed from the repository root, from `/tmp`, and under two
different `RUBY_HASH_SEED` values.  The three JSON outputs were byte-identical.

## 7. Claim boundary

This audit supports the following limited conclusions:

1. The hybrid stopped-flux and combined residual vectors are equivalent under
   one common best-\(N\) deletion, with literal factor five.
2. If the open temporal tail estimate (S.342) holds, the displayed route to
   the Step 10 residual gate is algebraically correct.
3. A signed common terminal window carries the explicit start-clock debt in
   (S.393)--(S.395).
4. Finite terminal crowns give the stated depth-independent coefficient
   content when every occurrence is counted.
5. Proposition 3.1 is conditional on the open nonlinear crown payment
   (S.407).
6. The converse-Hölder obstruction is a formal nonnegative-ledger result.  Its
   two supporting stress tests are separate and abstract.

This audit does not prove (S.342), (S.375), (S.407), (S.288), (S.303),
(S.272), Q.12, Q.1, a coupled stress fixture, an NSE velocity-pressure
realization, scale contraction, regularity, singularity formation, or the
Navier--Stokes Millennium problem.  **FINITE ONLY.  NOT CLAY.**
