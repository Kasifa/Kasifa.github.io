# R0.74S Step 5 — primary audit of the one-sided ball-clock reduction

## 1. Verdict

**PASS AFTER FORMAL REPAIRS.**  Equations (S.85)--(S.111) are internally
consistent under the inherited R0.74P/R0.74S suitable-weak conventions.
The proved endpoint is deliberately negative: scalar clock positivity,
linearity, and the ball-tower identities alone retain an \(\ell^1\) debt
and do not imply the desired matched \(\ell^2\) compression.

The last construction is an **ABSTRACT ALGEBRAIC NO-GO**, not a velocity,
pressure, dissipation measure, Navier--Stokes solution, or PDE
counterexample.  The unconditional stopped-work estimate and all
regularity conclusions remain **OPEN / NOT CLAIMED.  NOT CLAY.**

## 2. Frozen inputs

| Artifact | SHA-256 |
|---|---|
| `research/r074s_one_sided_ball_clock_no_gain.md` | `178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af` |
| `scripts/r074s_one_sided_ball_clock_certificate.py` | `5b11397671e8497d7f4244e2193998199d0b4e55b6be12fb76c8d376f76539f6` |
| `research/r074s_one_sided_ball_clock_certificate.json` | `1afcea511445b75c05da034130c4f1719f4b129c1df496ba5b3f65025ff57219` |
| `research/r074s_one_sided_ball_clock_certificate_report.md` | `2d15825ac9bf109c729164b218824d2cea5088ec72a1bbff3b2bffb0235b7b07` |

## 3. Analytic audit

### 3.1 Cutoffs and flux signs: S.85--S.88

For \(z=(|y|-r_m)/\delta\), the frozen transition convention implies
that at least one of \(\vartheta(z),\vartheta(-z)\) is one.  Hence

\[
 \chi_m^+-\chi_m^-
 =\vartheta(-z)+\vartheta(z)-1
 =\vartheta(z)\vartheta(-z)=\beta_m.
\]

The same four-region calculation across the two adjacent radii gives
\(\chi_{m+1}^+-\chi_m^-=\psi_m\).  Differentiating the radial arguments
produces a minus sign for both one-sided gradients.  Consequently the
periodized fluxes are \(-J_m^-\) and \(-J_m^+\), as stated in (S.88).
The origin convention is harmless because both radial profiles are
constant near zero.

### 3.2 Completed tower: S.89--S.92

Every row is linear in the cutoff.  Applying the two exact cutoff
differences gives the two lines of (S.91), with the factor
\(\gamma_m^{-1}\) because the inherited shell and boundary clocks already
carry \(\gamma_m\).  Subtraction yields

\[
 \mathscr K_{m+1}^+-\mathscr K_m^+
 =\gamma_m^{-1}(K_m-K_m^\partial)\ge0.
\]

The current wording correctly distinguishes the all-time canonical
\(Q,F,K\) representatives from the good-time \(E,D\) rows.

### 3.3 Quadratic payment: S.93--S.94

The pointwise ledger was checked collar by collar.  The only shifted
coefficient that could be missed is \(\gamma_{j-1}\) on the outer collar
\(C_j^+\); it is paid by
\(\operatorname {supp}\psi_{j-1}\), not by a false
\(\gamma_j\) bound.  The same indexing covers the Laplacian supports.

The central ball is not part of the inherited shell ledger and is
therefore paid separately:

\[
 R^{-3}\int_{I_{2R}}\int_{B_{4R}}|v_R|^2
 \le32\mathcal E^{M,R}(z_0,8R)
 \le32A_R.
\]

This closes precisely the quadratic \(Q\)-variation statement (S.94);
it does not control any retained terminal \(K\)-clock.

### 3.4 Stopped orientation: S.95--S.102

At time \(t\), shell \(k\) is active exactly when
\(\sigma_k<t\le\tau\).  Its predecessor is inactive up to
\(\rho_k\), its successor is inactive up to \(\lambda_k\), and an
internal boundary is active only after
\(\max(\sigma_{m-1},\sigma_m)\).  Thus the three activation intervals are
left-open and right-closed, and substitution of (S.88) gives:

- a negative \(F^-\) increment for the root row;
- a positive \(F_{k+1}^+\) increment for the signed outer row; and
- a positive \(d_mF_m^+\) increment for the weight-drop row.

Writing \(F=K-Q\), using \(K\ge0\), and charging every \(Q\) increment to
(S.94) leaves exactly the start, merge, and terminal clocks in
(S.100)--(S.102).  No sign has been discarded before its legitimate
one-sided positive-part estimate.

### 3.5 Abel identity: S.103--S.107

Finite summation by parts gives the terminal term
\(-\gamma_MB_M\).  Substitution of the tower residual is exact, including
the separate \(m=1\) row.  The periodized ball cutoff has at most cubic
lattice growth, so

\[
 \gamma_MB_M\lesssim
 e^{-4^{M-1}/32}(1+2^{3M})\longrightarrow0.
\]

The inherited finiteness of \(Y_{1,R}^{\rm clk}\), together with
\(0\le K_m^\partial\le K_m\), makes the limiting nonnegative series
finite.  The result is therefore an \(\ell^1\) estimate, not an
\(\ell^2\) estimate.

### 3.6 Abstract saturation: S.108--S.111

With \(K_m=h\) for \(m\le N\), \(K_m^\partial=0\), and
\(\mathscr K_m^-=\mathscr K_m^+\), the recursive tower satisfies both
lines of (S.91).  The scalar assignment
\(E=K,D=Q=0,F=K\) realizes the completed-clock equalities without
asserting a spatial cutoff operator or a PDE field.  At the terminal time,

\[
 (Y_{2,R}^{\rm sf})^2=N,
 \qquad
 \sum_{m\ge2}d_m\mathscr K_m^+=N.
\]

Thus a universal bound of the latter by \(CY_{2,R}^{\rm sf}\) is
impossible from this scalar algebra alone.  Extra PDE dynamics or a
cross-channel sign theorem remain logically available.

## 4. Finite certificate and regression checks

The deterministic certificate reports:

- 5/5 exact ledger rows;
- 7/7 finite checks;
- 55/55 structural checks; and
- 4/4 negative sign mutations.

Its finite coverage includes 312 rational cutoff values, 228 derivative
samples, 1,024 stopped configurations with tied stops, 82,432 Boolean
activation comparisons, event-cell reconstruction of maximal blocks,
all finite Abel endpoints \(M=2,\ldots,8\), a separate tower-compatible
Abel fixture, and abstract witnesses \(N=1,\ldots,24\) at five rational
times.  The Abel-terminal and root-clock sign flips are rejected both by
statement sentinels and by independent numerical fixtures.

Two fresh temporary output directories reproduced byte-identical JSON and
Markdown reports.  The frozen Step-4 boundary-mismatch certificate also
remained **PASS** with 14/14 exact, 4/4 finite, and 38/38 structural checks.

These are **FINITE** checks.  They do not machine-prove cutoff smoothness,
periodization/unfolding, the suitable local-energy calculation, the
infinite support estimate, or a PDE realization of the scalar witness.

## 5. Repairs incorporated before freeze

1. Added the missing central \(B_{4R}\) energy payment in the proof of
   (S.94).
2. Distinguished all-time \(Q,F\) identities from good-time \(E,D\)
   identities after (S.91).
3. Added \(\mathscr K_m^-=\mathscr K_m^+\) and the scalar
   \(E,D,Q,F\) rows to the abstract witness.
4. Narrowed the route rejection to scalar positivity, linearity, and the
   tower identities; no PDE no-go is asserted.
5. Strengthened the certificate so its signed direct side is reconstructed
   from active maximal blocks rather than copied from the endpoint formula.

## 6. Claim ledger

| Claim | Status |
|---|---|
| One-sided cutoff and flux identities | **PROVED** |
| Completed ball-clock tower | **PROVED / INHERITED LOCAL-ENERGY FRAMEWORK** |
| Quadratic three-family \(Q\) ledger | **PROVED** |
| Three stopped time orientations | **PROVED** |
| Terminal Abel identity | **PROVED** |
| Scalar positive-clock \(\ell^1/\ell^2\) obstruction | **PROVED — ABSTRACT NO-GO** |
| Cross-channel PDE sign theorem | **OPEN** |
| Root/outer/weight-drop dynamical control | **OPEN** |
| R0.74R persistence hypotheses and fixed-scale (Q.1) | **OPEN** |
| Scale contraction, regularity, singularity, Millennium problem | **OPEN / NOT CLAIMED / NOT CLAY** |
