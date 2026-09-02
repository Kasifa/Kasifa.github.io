# R0.74S Step 3 — primary audit of the actual padded-collar decomposition

## Result

**PASS AFTER PERIODIC-WITNESS REPAIR.**  The cutoff derivative, lifted
support geometry, unfolded collar traces, active-block decomposition,
weight-drop/bridge split, physical work split, and absolute-payment boundary
were recomputed.  The first functional bridge witness was merely a compact
Euclidean bump.  It has been replaced by a no-winding periodic bump so that
the witness respects the torus setting while remaining explicitly outside
the Navier--Stokes solution class.

This is a primary self-audit, not an independent audit.  **NOT CLAY.**

## 1. Cutoff derivative and disjointness

Let \(r_k=2^kR\) and \(\delta=R/8\).  When the inner factor of
\(\psi_k^R\) is differentiating, its support lies in
\((r_k-\delta,r_k)\); the outer factor is then exactly one.  When the outer
factor differentiates, its support lies in
\((r_{k+1},r_{k+1}+\delta)\); the inner factor is exactly one.  This proves
(S.40) without a cross term.

At a shared hard radius \(r_m\), the outer derivative of shell \(m-1\)
lives in \(C_m^+\), while the inner derivative of shell \(m\) lives in
\(C_m^-\).  They meet only on the null sphere \(r=r_m\).  Successive hard
radii are separated by at least \(2R\), whereas two collar widths total
\(R/4\).  Hence all lifted transition supports are pairwise disjoint and
(S.43) follows pointwise almost everywhere.

**Decision: PASS.**  This conclusion is made only after Euclidean
unfolding.  It does not claim that unrelated periodic-copy vectors cannot
cancel after numerical integration.

## 2. Unfolding and shell orientation

For a periodic integrable work vector, the inherited identity

\[
 \int_{\mathbb T^3}\mathcal W\cdot\nabla\Psi_k^R
 =\int_{\mathbb R^3}\widetilde{\mathcal W}\cdot\nabla\psi_k^R
\]

is legitimate for every finite shell.  The positive inner derivative gives
\(J_{k,R}^-\), and the negative outer derivative gives
\(-J_{k+1,R}^+\).  Thus (S.46) has the correct index and orientation.

**Decision: PASS.**

## 3. Block and internal-pair algebra

For one active block \([p,q]_{\mathbb Z}\), direct expansion gives the root
\(\gamma_pJ_p^-\), the outer row \(-\gamma_qJ_{q+1}^+\), and internal pairs
\(\gamma_mJ_m^--\gamma_{m-1}J_m^+\).  The latter obey

\[
 \gamma_mJ_m^--\gamma_{m-1}J_m^+
 =-(\gamma_{m-1}-\gamma_m)J_m^+
  +\gamma_m(J_m^--J_m^+).
\]

Summing over the disjoint active blocks proves (S.52).  The identity uses no
sign assumption.

**Decision: PASS.**

## 4. Weight drop and bridge witness

The inherited adjacent-weight estimate yields
\(\gamma_{m-1}-\gamma_m\ge(3/35)\gamma_{m-1}\).  Hence exact equality of the
two collar traces would leave the full weight-drop row (S.54); a bridge
estimate alone cannot erase it.

For the functional converse, select \(r_m+\delta<\pi/2\).  A smooth
periodic vector bump supported in the principal-cell portion of \(C_m^+\)
has no periodic copy intersecting \(C_m^-\).  After radial alignment and
normalization it gives \(J_m^+=1\), \(J_m^-=0\), with uniformly bounded
\(L^1\) size under scaling.  This proves only that the available \(L^1\)
ledger has no uniform two-collar modulus.

**Decision: PASS WITH BOUNDARY.**  The bump is not required to equal
\(\frac12|v|^2(v-a)+(\pi-c)v\) for a Navier--Stokes solution.

## 5. Kinetic, pressure, and drift accounting

The work vector splits linearly into kinetic transport, pressure work, and
moving-frame drift.  In the four-channel representation, taking absolute
values counts:

- every block-root inner collar once with its original shell weight;
- every block-outer collar once with its original shell weight;
- every internal inner collar with coefficient \(\gamma_m\); and
- every internal outer collar with total coefficient
  \((\gamma_{m-1}-\gamma_m)+\gamma_m=\gamma_{m-1}\).

Thus no collar is charged above its original absolute shell coefficient.
The inherited velocity-cubic, pressure-product, and Version-M drift rows
give (S.59).

**Decision: PASS.**  This produces \(CP_R^M\), not the open
\(C(P_R^M)^{2/3}\) bound.

## 6. Finite certificate and hashes

The certificate passes 6/6 exact rational checks, 2/2 exhaustive finite
ledgers, and 23/23 structural checks.  It verifies 24 model collar intervals
through index 12 and all 64 active masks at \(M=6\).  Two runs regenerated
the outputs byte for byte.  A claim-boundary mutation declaring the bridge
closed was rejected.

| Artifact | SHA-256 |
|---|---|
| r074s_actual_collar_signed_decomposition.md | 9ea1f193814de863fd5e62baf477635b52c391309578b3dde12ecb6c94f34c9d |
| r074s_actual_collar_decomposition_certificate.py | 534bd7dacf45ac8139c2cd30bceaf8af983d9450d62492b067197d1756c329f6 |
| r074s_actual_collar_decomposition_certificate.json | a4e3380efc6e50b2da8da9adcd785e15b64d95dffc0ccb2e717e8bd58499e3cf |
| r074s_actual_collar_decomposition_certificate_report.md | 318a0a4c1bb6f4c079b4714f04c1ea9eda9b04396e1b993c91b28ed78fe89d0d |

The certificate does not prove unfolding, the analytic decomposition, the
functional witness scaling, or a PDE sign theorem.

## 7. Remaining gate

The exact stopped work is now separated into root, outer, weight-drop, and
two-collar mismatch channels, each further separated into kinetic, pressure,
and drift parts.  A successful continuation must preserve the signs of these
rows.  Absolute estimates, coefficient cancellation, and an \(L^1\) bridge
have all reached their exact limits.

The signed depletion theorem, dissipation branch, persistence packing,
(Q.1), scale packing, regularity, and the Clay problem remain **OPEN**.
