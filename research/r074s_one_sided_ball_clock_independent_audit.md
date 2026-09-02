# R0.74S Step 5 — independent audit of the one-sided ball-clock reduction

## Result

**PASS AFTER FORMAL REPAIRS.  NO UNRESOLVED BLOCKER.**

Four independent read-only audit passes covered the full analytic note,
the delicate quadratic support ledger, the finite/infinite Abel algebra,
the abstract witness, and the executable certificate.  The final audited
note has SHA-256

    178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af

The result is a proved one-sided-clock reduction and a **PROVED ABSTRACT
NO-GO** for one standalone scalar mechanism.  It is not a Navier--Stokes
counterexample and proves no regularity theorem.  **NOT CLAY.**

## 1. One-sided cutoffs and completed clocks — PASS

The two gradients in (S.86) have the correct negative radial sign.  A
four-region check gives both identities

\[
 \beta_m=\chi_m^+-\chi_m^- ,
 \qquad
 \psi_m=\chi_{m+1}^+-\chi_m^- .
\]

After periodization, the corresponding flux rows are exactly
\(-J_m^-\) and \(-J_m^+\).  Linearity of the five cutoff rows gives both
lines of (S.91), and their difference is

\[
 \mathscr K_{m+1}^+-\mathscr K_m^+
 =\gamma_m^{-1}(K_m-K_m^\partial)\ge0.
\]

The final timing repair is correct: \(Q,F,K\) use their canonical
absolutely continuous representatives at every time, whereas \(E,D\)
are invoked at local-energy good times.  Reverting only this sentence
reconstructs the pre-repair SHA exactly, confirming that no other note
content changed during the final delta audit.

## 2. Quadratic support ledger — PASS

The support and Laplacian indices in (S.93) were independently traced.
On the dangerous outer collar \(C_j^+\), the shifted coefficient
\(\gamma_{j-1}\) is paid by
\(\operatorname {supp}\psi_{j-1}\).  The padded-shell interiors begin
with \(\gamma_j\), and the frozen adjacent-ratio tail is summable.

The central ball is correctly separated from the inherited shell ledger:

\[
 R^{-3}\int_{I_{2R}}\int_{B_{4R}}|v_R|^2
 \le32\mathcal E^{M,R}(z_0,8R)
 \le32A_R.
\]

Together these estimates prove (S.94).  No retained terminal clock is
silently charged to this quadratic row.

## 3. Stopped activation and signs — PASS

The root, outer, and internal activation sets were independently checked
for every finite mask through six shells, including tied stop times.  The
left-open/right-closed convention is correct at all event boundaries.
In particular:

- \(k=1\) has \(\rho_k=\tau\);
- an absent successor gives \(\lambda_k=\tau\);
- the outer row uses \(\mathscr F_{k+1}^+\), not
  \(\mathscr F_k^+\); and
- the internal row starts at
  \(\max(\sigma_{m-1},\sigma_m)\) for \(m\ge2\).

Independent exact-rational enumeration and event-cell integration confirm
all three signs in (S.97)--(S.99).  The positive-part reductions
(S.100)--(S.102) consequently retain the correct start, merge, and
terminal clocks.

## 4. Abel identity and limiting step — PASS

Direct finite summation gives (S.103), including the empty middle sum at
\(M=2\), with the indispensable terminal sign
\(-\gamma_MB_M\).  Substituting (S.92) produces (S.104).  The fixed-time
periodized ball clock grows at most like \(1+2^{3M}\), while
\(\gamma_M=e^{-4^{M-1}/32}\); hence \(\gamma_MB_M\to0\).

The inherited \(Y_{1,R}^{\rm clk}<\infty\), the comparison
\(K_m^\partial\le K_m\), and the fixed core clock make the series in
(S.106) finite.  Thus (S.107) is a valid \(\ell^1\) estimate and is not
misidentified as square-function compression.

## 5. Abstract saturation — PASS WITH STRICT SCOPE

The repaired witness explicitly sets
\(\mathscr K_m^-=\mathscr K_m^+\) and assigns the scalar rows

\[
 E=K,\qquad D=Q=0,\qquad F=K.
\]

It therefore satisfies the scalar completed-clock and tower identities.
At the terminal time its shell variations give
\((Y_2^{\rm sf})^2=N\), while the weight-drop ball debt equals \(N\).
This rules out a uniform \(CY_2^{\rm sf}\) bound from scalar nonnegativity,
linearity, and (S.90)--(S.92) alone.

The witness contains no velocity, pressure, work density, spatial cutoff
operator, or dissipation measure.  It leaves open every argument using
the PDE, cross-channel signs, or finite-complexity genealogy.

## 6. Independent certificate verification

The final executable certificate was independently run in temporary
output directories.  It reports

    5/5 exact ledger rows          PASS
    7/7 finite checks              PASS
    55/55 structural checks        PASS
    4/4 negative mutations         PASS

The verification includes:

- exact rational cutoff values and transition derivatives;
- the geometric support proxy with both infinite tails and sampled bound
  \(73/3\);
- 1,024 five-shell stopped configurations, including ties, and 82,432
  Boolean activation comparisons;
- direct maximal-block event integration against all three endpoint clock
  formulas;
- every finite Abel terminal from \(M=2\) through \(M=8\), plus a
  tower-compatible residual fixture;
- abstract towers \(N=1,\ldots,24\) at five rational times, totaling
  4,860 scalar identity comparisons; and
- structural and numerical rejection of both the wrong Abel terminal sign
  and the wrong root-clock sign.

Two independent temporary regenerations were byte-identical to each other
and to the repository JSON/report.  Separate external wrong-sign note
fixtures both failed, reducing the affected run to 54/55 structural and
3/4 negative checks.

| Artifact | SHA-256 |
|---|---|
| `research/r074s_one_sided_ball_clock_no_gain.md` | `178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af` |
| `scripts/r074s_one_sided_ball_clock_certificate.py` | `5b11397671e8497d7f4244e2193998199d0b4e55b6be12fb76c8d376f76539f6` |
| `research/r074s_one_sided_ball_clock_certificate.json` | `1afcea511445b75c05da034130c4f1719f4b129c1df496ba5b3f65025ff57219` |
| `research/r074s_one_sided_ball_clock_certificate_report.md` | `2d15825ac9bf109c729164b218824d2cea5088ec72a1bbff3b2bffb0235b7b07` |

The certificate is finite evidence only; it does not machine-prove the
suitable local-energy calculation, infinite support estimate, or a PDE
realization of the abstract witness.

## Final boundary

The one-sided ball construction exactly exposes the remaining \(\ell^1\)
debt and rigorously closes this attempted algebraic route.  A viable next
gate must retain a cross-channel dynamical sign relation or prove a
finite-complexity theorem for the stopped block genealogy.

Root/outer/weight-drop dynamical control, the dissipation branch, R0.74R
persistence hypotheses, fixed-scale (Q.1), scale contraction, regularity,
singularity formation, and the Millennium problem remain
**OPEN / NOT CLAIMED**.

**INDEPENDENT AUDIT PASS.  ABSTRACT NO-GO ONLY.  NOT CLAY.**
