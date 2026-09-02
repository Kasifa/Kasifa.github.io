# R0.74S Step 4 — independent audit of the boundary-mismatch clock

## Result

**PASS AFTER FORMAL REPAIRS.**

The boundary-bump geometry, completed local-energy clock,
quadratic/cubic ledgers, stopped-family indexing, persistence exponents,
and conditional mismatch theorem were independently recomputed against
R0.74S Step 3 and the inherited R0.74P/H/R results.  No unresolved
mathematical or structural blocker remains in the audited Step-4 claim.

Current note SHA-256:

    0bcb1e871ee00747e74b7a938dcebed9a70a1ed0a79a8dc7fc31739086cd749a

This audit does not establish the open hypotheses of Theorem 6.1.
**NOT CLAY.**

## 1. Boundary bump and dominance — PASS

Writing \(z=(|y|-r_m)/\delta\), the bump is
\(\beta_m^R=\vartheta(z)\vartheta(-z)\).  On the support of
\(\vartheta'(z)\), the second factor equals one; on the support of
\(\vartheta'(-z)\), the first factor equals one.  Thus (S.61) has the
correct inner-positive and outer-negative signs.

Because \(r_m-\delta\ge15R/8>0\), the radial function vanishes near the
origin and is smooth there.  The revised formula also handles \(y=0\)
explicitly.

On the support of \(\beta_m^R\), the outer factor in \(\psi_m^R\) equals
one, so

\[
 0\le\beta_m^R\le\psi_m^R.
\]

The closed-support formulation in (S.62) is correct.  Periodization is
locally finite for fixed \(m\), and termwise domination gives
\(0\le B_m^R\le\Psi_m^R\), irrespective of overlap between periodic
copies.  The annular-volume and radial-derivative calculations give the
stated \(2^{2m}R^3\), \(R^{-1}\), and \(R^{-2}\) bounds uniformly in
\(m\).

## 2. Completed-clock signs and comparison — PASS

Testing with \(\eta_R(r)B_m^R(x-X_R(r))\) produces the same moving-frame
drift combination as R0.74P.  The signs are

\[
 K_{m,R}^{\partial}
 =Q_{m,R}^{\partial}+F_{m,R}^{\partial}
 =E_{m,R}^{\partial}+D_{m,R}^{\partial}\ge0.
\]

The time-dependent pressure gauge vanishes by periodicity and
incompressibility.  At good times, \(B_m^R\le\Psi_m^R\) and positivity of
the total local-dissipation measure imply

\[
 0\le K_{m,R}^{\partial}\le K_{m,R}\le v_{m,R}.
\]

The \(Q+F\) representation correctly supplies the canonical absolutely
continuous representative at all times.

## 3. Boundary ledgers — PASS

After periodizing nonnegative derivative majorants and unfolding,

\[
 \sum_m\operatorname {TV}Q_{m,R}^{\partial}
 \lesssim R^{-3}
 \sum_m\gamma_m
 \int_{I_{2R}}\int_{\operatorname {supp}\beta_m^R}
 |\widetilde v_R|^2.
\]

The inherited weighted Hölder and doubled-radius support argument proves
(S.69).  Likewise,
\(\operatorname {supp}\beta_m^R\subset
\operatorname {supp}\psi_m^R\) places every shell-dependent boundary
payment inside the inherited nonnegative cubic ledger, proving (S.71).

## 4. Stopped mismatch identity — PASS

An internal boundary \(m\) is active exactly when both shells \(m-1\) and
\(m\) are active.  Its active interval is

\[
 (\max\{\sigma_{m-1},\sigma_m\},\tau].
\]

Unfolding (S.61) gives exactly \(J_{m,R}^- -J_{m,R}^+\), so (S.73) has
the correct coefficient, sign, index, and stopping time.

Using \(F^\partial=K^\partial-Q^\partial\), the stopped clock contributes
with a negative sign and may be discarded by nonnegativity.  The remaining
\(Q\)-increments are bounded by total variation, proving (S.74).

## 5. Persistence exponent — PASS

Spatial Hölder on a support of volume \(O(2^{2m}R^3)\) yields

\[
 (e_{m,R}^{\partial,\eta})^{3/2}
 \lesssim
 2^mR^2\gamma_m^{1/2}
 \left[
 R^{-2}\gamma_m\eta_R^{3/2}
 \int_{\operatorname {supp}\beta_m^R}|\widetilde v_R|^3
 \right].
\]

After time integration and division by the persistence ratio, this gives
the exact endpoint coefficient

\[
 2^{2m/3}\gamma_m^{1/3}
 (\Theta_{m,R}^{\partial})^{-2/3}.
\]

Shellwise Hölder cubes it to

\[
 2^{2m}\gamma_m\Lambda_m^3
 (\Theta_{m,R}^{\partial})^{-2}.
\]

All powers of \(R\), \(2^m\), \(\gamma_m\), and
\(\Theta_m^\partial\) are correct.

## 6. Extended-real repair — PASS

The earlier draft left \(+\infty\cdot0\) expressions undefined when
\(\Theta^\partial=0\).  The current version:

- reads (S.77) as vacuous with right side \(+\infty\) when
  \(\Theta^\partial=0\);
- defines the composite coefficient to be zero when \(\Lambda=0\);
- assigns \(+\infty\) when
  \(\Lambda>0,\Theta^\partial=0\);
- handles \(\Theta^\partial=+\infty\) by
  \((+\infty)^{-2}=0\); and
- defines the whole right side of (S.79) as \(+\infty\) whenever its
  coefficient sum is infinite.

Thus (S.77), (S.79), and (S.81) contain no unresolved extended-real
arithmetic.

## 7. Conditional theorem — PASS

The positive-measure requirement for every \(J_m\) is explicit.  Under
(S.80)--(S.81), the nonexceptional clocks are bounded by \(CA_R\) using
(S.79) and (S.71).  For at most \(N_\partial\) exceptional indices,

\[
 \sum K_{m,R}^{\partial}(\tau)
 \le\sum v_{m,R}
 \le\sqrt{N_\partial}\,Y_{2,R}^{\rm sf}.
\]

Taking \(H=I^\partial\) in (S.74) proves (S.82).  The quantifiers are
sufficient for every finite stopped family with good terminal time.

## 8. Independent certificate verification

Independent temporary regeneration was byte-deterministic and identical
to the generated outputs:

    14/14 exact rational checks       PASS
    4/4 finite ledgers                PASS
    38/38 structural checks           PASS

| Artifact | SHA-256 |
|---|---|
| note | 0bcb1e871ee00747e74b7a938dcebed9a70a1ed0a79a8dc7fc31739086cd749a |
| script | 922977b1367d6941df28755ee2e93d9710e539e253d1dc1f7a35f7ed16de399b |
| JSON | c3823b9c5cdf62b4a8eb870be60bd7a0bf23bb8788a1ae375d45efab55ab1239 |
| report | f2cea6daf46c3b1b8565cb2c79121f6162ffe5ad4bdc1d3e9039e3157078c5eb |

The certificate is finite/structural evidence only.  It does not prove the
suitable local-energy identity, the inherited analytic ledgers, or the
open clock-extraction and persistence hypotheses.

## Final boundary

R0.74S Step 4 rigorously controls only the two-collar mismatch channel
under the stated conditional packing hypothesis.  Root supply, outer
leakage/backscatter, the weight-drop channel, unconditional stopped-work
compression, scale contraction, regularity, singularity formation, and
the Millennium problem remain **OPEN / NOT CLAIMED**.

**INDEPENDENT AUDIT PASS. NOT CLAY.**
