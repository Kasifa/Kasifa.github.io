# R0.74S Step 9 — independent Ruby certificate and adversarial audit

## 1. Verdict and cryptographic bindings

**PASS.**  The independent verifier accepts the locked Step 9 note and the
primary producer bundle with no residual error.  The audited files are bound
by the following SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| Locked note `research/r074s_best_n_last_exit_equivalence.md` | `85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd` |
| Primary generator `scripts/r074s_best_n_last_exit_certificate.py` | `0f04b79049ecd92c4a366ad9916fc8b6da9220b2f5baee34726aef2d4feaee65` |
| Primary JSON `research/r074s_best_n_last_exit_certificate.json` | `26ee76d969d3aec5eec55d9fa981bce195538cc3e2464fc0ece2c46b7c4accf0` |
| Primary report `research/r074s_best_n_last_exit_certificate_report.md` | `1108b72113d84b90ebc5570c2c7b4bfaa1ccdc299525c557979b564109ab6481` |
| Independent Ruby verifier `scripts/r074s_best_n_last_exit_certificate_independent.rb` | `d9c0674b79bc532c10366d317ccb10550f0bfd2a825127e87a4ef24633d3ae66` |

The Ruby verifier reconstructs the finite algebra before parsing the primary
JSON.  It uses exact `Rational` arithmetic and does not invoke the Python
producer.  Agreement is therefore cross-language and not a second rendering
of producer output.

The counted result is:

| Independent audit group | Passed | Total |
|---|---:|---:|
| Algebraic and finite-fixture groups | 12 | 12 |
| Exact finite cases inside those groups | 91,396 | 91,396 |
| Locked-note structural sentinels | 49 | 49 |
| Adversarial source mutations rejected | 21 | 21 |
| Adversarial primary-artifact mutations rejected | 15 | 15 |
| Primary-report bindings | 6 | 6 |
| Primary producer validation errors | 0 | 0 |

## 2. Independent reconstruction of the signed best-(N) functional

For (x\in\ell^1(\mathbb N;\mathbb R)), write

\[
 \mathcal S_N(x)
 =\inf_{\#S\le N}\left[\sum_{k\notin S}x_k\right]_+.
\]

There are two different order statements here, and the audit keeps them
separate.

First, for (a_S=\sum_{k\notin S}x_k), monotonicity and continuity of
(r\mapsto[r]_+) give

\[
 \inf_S[a_S]_+=[\inf_Sa_S]_+.
\]

Thus positive part and this infimum do commute.  This does not authorize
discarding negative coordinates before the full complementary sum is formed.
Indeed, minimizing (a_S) means maximizing the removed sum, so an optimal or
approximating set deletes only the (N) largest positive coordinates.  If
((x_m^{+*})) is their decreasing rearrangement, padded with zeroes, then

\[
 \mathcal S_N(x)
 =\left[\sum_kx_k-\sum_{m=1}^Nx_m^{+*}\right]_+
 =\left[\sum_{m>N}x_m^{+*}-\|x_-\|_1\right]_+.
\]

Second, every fixed-(S) functional is one-Lipschitz on \(\ell^1\), uniformly
in (S).  Taking the two infima against the same comparison sets proves

\[
 |\mathcal S_N(x)-\mathcal S_N(y)|\le\|x-y\|_1.
\]

The constant one is sharp, for example at (N=0), (x=(1,0,\ldots)), and
(y=0).  It also closes the finite/infinite-shell passage: for the coordinate
projection (P_Mx),

\[
 |\mathcal S_N(P_Mx)-\mathcal S_N(x)|
 \le\|P_Mx-x\|_1\longrightarrow0.
\]

The finite verifier exhaustively checked 3,125 signed reconstruction cases,
including 2,066 cancellation-to-zero cases, and 62,500 Lipschitz comparisons,
including 1,824 nonzero equality cases.  No interchange of an infinite
local-energy test with the suitable-weak inequality is used in this argument.

## 3. Half exits, last exits, and sharp constants

### Signed (F)-half exit

For terminal value (f=F_k(\tau)\ne0), continuity and the zero start make the
last point satisfying

\[
 \operatorname{sgn}(f)F_k(t)\le |f|/2
\]

well defined.  Maximality forces equality there, including when (f<0).
Consequently

\[
 F_k(\tau)-F_k(\ell_k^F)=\frac12F_k(\tau),
 \qquad
 \mathfrak W_{1/2,N}^F(\mathcal D)
 =\frac12\mathcal S_{N}^F(\mathcal D).
\]

The convention \(\ell_k^F=\tau\) for (f=0) gives the correct zero
increment.  The verifier checked 625 oscillatory piecewise-linear paths: 250
positive terminals, 250 negative terminals, and 125 zero terminals.  It then
checked the best-(N) identity in 3,125 signed vector cases.

This exact algebraic stop is not automatically an (S.25) strict
(K)-upcrossing.  In the locked (S.209) fixture, the half exit has
(K(1)-K(1/2)=0).  Therefore the half-exit observable may not be substituted
directly into the Step 2 supremum (S.37).

### (K)-level last exit

For (T_k=K_k(\tau)>0) and (0<\theta<1), the last
(\theta T_k)-level exit satisfies

\[
 K_k(\tau)-K_k(\ell_{k,\theta}^K)=(1-\theta)T_k,
\]

and (F=K-Q) gives

\[
 L_{k,\theta}=(1-\theta)T_k-\Delta Q_{k,\theta}.
\]

For every fixed ((\tau,S)), put
(a=(1-\theta)\sum_{k\notin S}T_k\ge0) and
(b=\sum_{k\notin S}\Delta Q_{k,\theta}).  Then

\[
 |[a-b]_+-a|\le |b|
 \le\sum_{k\notin S}|\Delta Q_{k,\theta}|\le B_Q.
\]

Because the error is uniform in both variables, taking first
(\inf_{S_\tau}) and then \(\sup_\tau\) preserves one (B_Q):

\[
 (1-\theta)\mathcal S_N^K-B_Q
 \le \mathfrak W_{\theta,N}^K
 \le (1-\theta)\mathcal S_N^K+B_Q.
\]

There is no factor two.  The coefficient one is sharp: a one-coordinate
monotone (Q)-increment of size (B\le1-\theta), placed after the level
exit with either sign, attains error (B).  The verifier found 1,178 sharp
instances among 11,664 exact perturbation cases.  The related signed
(F)/nonnegative-(K) comparison was checked in 2,916 cases, including 509
instances attaining the full (B_Q) error.

The strict Step 2 condition is obtained exactly for positive terminal clocks
when

\[
 (1-\theta)T_k>T_k/4,
 \quad\text{i.e.}\quad 0<\theta<3/4.
\]

At (\theta=3/4) equality is not enough.  The verifier checked 3,000
piecewise-linear (K)-paths, including 500 endpoint cases.  At
(\theta=2/3), it separately checked 48 sign/size fixtures, of which 24
satisfy the strict hypothesis
(|\Delta Q|<T/6\), and recovered \(\Delta F>T/6\) in every eligible case.

## 4. Quantifier, cancellation, domain, and boundary falsifiers

The correct terminal observable has order

\[
 \sup_{\tau\in\mathcal D}
 \inf_{S_\tau\subset\mathbb N,\ \#S_\tau\le N}.
\]

The integer (N) is fixed independently of terminal time, scale, and
solution; the set (S_\tau) may depend on the terminal time.  In dimensions
(N+1), take the terminal states to be all coordinate unit vectors.  Then

\[
 \sup_\tau\inf_{\#S_\tau\le N}
 \sum_{k\notin S_\tau}x_k(\tau)=0,
 \qquad
 \inf_{\#S\le N}\sup_\tau
 \sum_{k\notin S}x_k(\tau)=1.
\]

The independent verifier reproduced these values for (N=1,\ldots,5).
Thus a fixed exceptional set is a strictly stronger requirement and cannot
replace R0.74Q (Q.7)--(Q.12).

Nor may the forced signed complement be replaced by a supremum over arbitrary
finite subsets.  For (m) pairs
((1/2,-1/2)), the complete signed sum is zero while arbitrary positive
selection yields (m/2).  This was checked for (m=1,\ldots,8), together
with the asymmetric vector ((-1,1/2)).  Absolute convergence permits
prescribed finite-head exhaustion, but it does not permit sign-selective
exhaustion.

The remaining 491 stress cases verify the following distinct boundaries:

- (M>N) simultaneous plateau shells retain the exact tail ((M-N)H), so
  last exits alone provide no shell compression;
- (K=0, Q=-F) attains the full (B_Q) gap and supplies no strict
  (K)-upcrossing;
- (F=0, K=Q) has a positive (K)-tail but zero stopped (F)-work, so the
  (Q) error cannot be removed;
- the half-(F) exit need not be a (K)-upcrossing;
- a clock that reached its plateau before a proposed recent window has no
  \(\theta\)-level exit inside that window, so the full history
  \([s_R,\tau]\) is necessary absent a new PDE payment; and
- an early positive pulse can make the full-interval supremum strictly larger
  than the plateau-interval supremum, so only
  \(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\) is available.

The (T_k=0) convention produces zero last-exit work and no fictitious strict
stop.  Finite positive-terminal families at a good terminal can be
approximated by common-good-time stops because the margin
((3/4-\theta)T_k) is strict.  This proves only finite-family, good-terminal
closure.  It proves neither continuity of the last-exit selector nor the
admissibility of one infinite temporally discontinuous local-energy cutoff.

## 5. Producer and claim-ledger tamper resistance

The independent reader requires schema
`r074s-best-n-last-exit-certificate-v1`, the exact primary ID sets, all rows
passing, exact summary counts, all four artifact byte hashes listed above, and
the exact six-field scope disclaimer.  It also checks the nine exact rational
payloads, seven enumerated finite-case counts, and all 57 structural IDs.
The unmodified primary bundle passes with counts (9/9), (8/8), (57/57),
and (18/18).

The 15 generated artifact mutations all fail validation.  They cover stale
note, locked-note, and generator hashes; wrong schema; a false producer
verdict; deleted or duplicated rows; summary-count drift; flipped structural
and negative-mutation results; altered exact payload; deleted required claim
rows; promotion of REFUTED or OPEN claims; and promotion of a false
machine-proof scope flag.

Separately, 21 source mutations are rejected by independent sentinels.  They
target the quantifier order, terminal sign, factors (1/2) and (1-\theta),
one-(B_Q) constant, strict endpoint, positive-terminal condition,
plateau/full-domain distinction, cancellation warning, full-history
requirement, good-time and infinite-test boundaries, Step 2 admissibility,
and the PROVED/REFUTED/OPEN/NOT CLAIMED ledger.  This includes mutations that
would falsely promote the scalar fixtures, (N_0=1), or the whole note to a
PDE or Millennium result.

## 6. Deterministic reproduction

The normal invocation is

```sh
ruby scripts/r074s_best_n_last_exit_certificate_independent.rb
```

For relocation tests, the four inputs can be supplied through
`R074S_LAST_EXIT_NOTE`, `R074S_LAST_EXIT_JSON`,
`R074S_LAST_EXIT_GENERATOR`, and `R074S_LAST_EXIT_REPORT`.  Two independently
created temporary directories containing byte-identical renamed inputs both
exited zero and produced byte-identical JSON.  The common output SHA-256 was

`53d0a50bb8ff8367079018aa10581855b33699079a2a35f5cfc01d7baa53027e`.

No absolute temporary path is serialized, so the result is deterministic
across directory names.

## 7. Exact conclusion and non-conclusions

The locked note passes as an algebraic representation and no-gain theorem.
The half-exit observable is exactly one half of the signed R0.74Q tail.  The
(K)-last-exit observable is equivalent to the nonnegative R0.74Q tail up to
the sharp, already-paid one-(B_Q) row.  Therefore canonical last exits do not
by themselves weaken the remaining problem.

What is still open is a fixed, solution- and scale-independent (N_0) and a
PDE estimate for the forced residual best-(N_0) tail after the paid branches
are removed.  The certificate does not prove inherited Navier--Stokes local
energy theory, good-time density, admissibility of an infinite stopped test,
the R0.74Q PDE tail bound, regularity, singularity formation, novelty, or
priority.

**NOT CLAY.**
