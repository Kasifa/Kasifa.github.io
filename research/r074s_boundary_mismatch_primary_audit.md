# R0.74S Step 4 — primary audit of the boundary-mismatch clock

## Result

**PASS AFTER SUPPORT, MEASURE, AND EXTENDED-ARITHMETIC REPAIRS.**

The boundary-bump geometry, completed local-energy identity, boundary
quadratic/cubic ledgers, stopped activation, persistence exponents, and the
conditional theorem were recomputed from the frozen R0.74S Step-3
decomposition and the inherited R0.74P/H/R results.

This is a primary self-audit.  A separate independent audit is recorded in
r074s_boundary_mismatch_independent_audit.md.  The hypotheses of Theorem
6.1 remain open.  **NOT CLAY.**

## 1. Geometry and periodization

Writing \(z=(|y|-r_m)/\delta\),
\(\beta_m^R=\vartheta(z)\vartheta(-z)\).  The product rule initially gives

\[
 \delta^{-1}
 [\vartheta'(z)\vartheta(-z)
  -\vartheta(z)\vartheta'(-z)]\widehat y.
\]

On the support of either derivative the other cutoff is one, proving
(S.61).  Since \(r_m-\delta\ge15R/8\), the bump vanishes near the origin;
the displayed radial formula is used for \(y\ne0\) and extended by zero at
the origin.

The first draft described the topological support by open collars.  The
audited version uses their closures:

\[
 \operatorname {supp}\beta_m^R
 \subset\{r_m-\delta\le |y|\le r_m+\delta\}.
\]

On this set the outer factor in \(\psi_m^R\) is one, so
\(0\le\beta_m^R\le\psi_m^R\).  The containing annulus has volume

\[
 8\pi r_m^2\delta+\frac{8\pi}{3}\delta^3
 \lesssim2^{2m}R^3.
\]

First and second radial derivatives cost at most \(CR^{-1}\) and
\(CR^{-2}\).  Periodization is locally finite at every fixed \(m\), and
termwise comparison gives \(0\le B_m^R\le\Psi_m^R\), even when periodic
copies overlap.

**Decision: PASS AFTER CLOSED-SUPPORT REPAIR.**

## 2. Completed boundary clock

The local-energy test
\(\eta_R(r)B_m^R(x-X_R(r))\) has the same moving-frame derivative as the
R0.74P shell test.  With the total local-dissipation measure it gives

\[
 K_{m,R}^{\partial}
 =Q_{m,R}^{\partial}+F_{m,R}^{\partial}
 =E_{m,R}^{\partial}+D_{m,R}^{\partial}\ge0.
\]

The time-dependent pressure gauge vanishes by periodicity and
incompressibility.  The \(Q+F\) formula is absolutely continuous at every
time; its equality with \(E+D\) on the dense full-measure set of good times
extends nonnegativity to every time.  At good times, positivity of the
dissipation measure and \(B_m^R\le\Psi_m^R\) imply

\[
 0\le K_{m,R}^{\partial}\le K_{m,R}\le v_{m,R}.
\]

The audited formula (S.66) now displays all time and space variables and
integration measures explicitly.

**Decision: PASS.**

## 3. Quadratic and cubic ledgers

For the Laplacian row, absolute values are taken only after periodizing a
nonnegative derivative majorant:

\[
 |\Delta B_m^R(y)|
 \le CR^{-2}\sum_n
 \mathbf 1_{\operatorname {supp}\beta_m^R}
 (\widetilde y+2\pi n).
\]

Unfolding before summation reduces the boundary supports to subsets of the
original shell supports.  The R0.74H weighted \(S_2\) estimate therefore
gives

\[
 \sum_m\operatorname {TV}Q_{m,R}^{\partial}
 \le C(P_R^M)^{2/3}.
\]

The same support inclusion and Tonelli place every shell-dependent
boundary cubic payment inside the inherited nonnegative cubic ledger:

\[
 \sum_m p_{m,R}^{\partial}(J_m)\le CP_R^M.
\]

**Decision: PASS.**

## 4. Stopped mismatch identity and sign

An internal boundary \(m\) is active exactly when both \(m-1\) and \(m\)
are active.  Its interval is therefore

\[
 (\max\{\sigma_{m-1},\sigma_m\},\tau].
\]

Unfolding the gradient of \(B_m^R\) gives
\(J_{m,R}^- -J_{m,R}^+\), with the same coefficient \(\gamma_m\) as the
Step-3 mismatch row.  This proves (S.73) with the correct sign and index.

Writing each flux increment as a clock increment minus a quadratic
increment, the stopped clock occurs with a negative sign and is discarded
by nonnegativity.  Total variation pays the remaining \(Q\) increments,
which proves (S.74).

**Decision: PASS.**

## 5. Persistence and extended values

Spatial Hölder on a set of volume \(O(2^{2m}R^3)\) gives

\[
 (e_{m,R}^{\partial,\eta})^{3/2}
 \le
 C2^mR^2\gamma_m^{1/2}
 \left[
 R^{-2}\gamma_m\eta_R^{3/2}
 \int_{\operatorname {supp}\beta_m^R}
 |\widetilde v_R|^3
 \right].
\]

After time integration, the endpoint coefficient is

\[
 2^{2m/3}\gamma_m^{1/3}
 (\Theta_{m,R}^{\partial})^{-2/3},
\]

and shellwise Hölder cubes it to

\[
 2^{2m}\gamma_m\Lambda_m^3
 (\Theta_{m,R}^{\partial})^{-2}.
\]

The first draft left \(+\infty\cdot0\) ambiguous at
\(\Theta^\partial=0\).  The audited version reads (S.77) as vacuous in
that case and defines the packed coefficient as a composite extended-real
quantity: zero when \(\Lambda=0\), infinite when
\(\Lambda>0,\Theta^\partial=0\), and ordinary otherwise.  If the packed
coefficient sum is infinite, the whole right side of (S.79) is defined as
infinite.  Thus no undefined product remains.

**Decision: PASS AFTER EXTENDED-ARITHMETIC REPAIR.**

## 6. Conditional theorem

The positive-measure condition for \(J_m\) is explicit.  Under
(S.80)--(S.81), the nonexceptional clock sum is at most \(CA_R\).  For at
most \(N_\partial\) exceptions,

\[
 \sum K_{m,R}^{\partial}(\tau)
 \le\sum v_{m,R}
 \le\sqrt{N_\partial}\,Y_{2,R}^{\rm sf}.
\]

Taking \(H=I^\partial\) in the stopped mismatch estimate proves (S.82).
This is a proved implication from the stated hypotheses, not a proof that
arbitrary suitable weak solutions satisfy them.

**Decision: PASS / CONDITIONAL INPUT OPEN.**

## 7. Certificate and hashes

Two consecutive regenerations were byte-identical.  The certificate passes
14/14 exact rational checks, 4/4 finite ledgers, and 38/38 structural
checks.  A negative mutation replacing the boundary volume exponent
\(2^{2m}R^3\) by \(2^{3m}R^3\) exits with failure.

| Artifact | SHA-256 |
|---|---|
| r074s_boundary_mismatch_clock.md | 0bcb1e871ee00747e74b7a938dcebed9a70a1ed0a79a8dc7fc31739086cd749a |
| r074s_boundary_mismatch_certificate.py | 922977b1367d6941df28755ee2e93d9710e539e253d1dc1f7a35f7ed16de399b |
| r074s_boundary_mismatch_certificate.json | c3823b9c5cdf62b4a8eb870be60bd7a0bf23bb8788a1ae375d45efab55ab1239 |
| r074s_boundary_mismatch_certificate_report.md | f2cea6daf46c3b1b8565cb2c79121f6162ffe5ad4bdc1d3e9039e3157078c5eb |

The finite certificate does not prove the suitable local-energy identity,
the inherited analytic ledgers, or the open hypotheses of Theorem 6.1.

## 8. Remaining boundary

Step 4 controls only the two-collar mismatch channel under a conditional
clock-to-endpoint and temporal-persistence packing hypothesis.  Root
supply, outer leakage/backscatter, weight-drop work, unconditional
stopped-work compression, scale contraction, regularity, singularity
formation, and the Millennium problem remain **OPEN / NOT CLAIMED**.

**PRIMARY AUDIT PASS. NOT CLAY.**
