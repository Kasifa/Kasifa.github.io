# R0.70Z independent audit

**Audit date:** 2026-08-25

**Verdict:** **PASS**

**Severity count:** zero blocker, zero major issue, and zero minor issue.

## Scope

The audit covered:

- the trace-free spectral split and invariant anisotropy decomposition;
- the reduced-resolvent formula and the sharp simple-projector derivative;
- the six-mode principal/full/defect work calculation;
- the ten-mode identical-covariance, opposite-principal-work construction;
- the absolute, top-normalized, and trace-relative eigengap estimates;
- the two-channel pre-convolution response lift;
- the sharp high--high--low common/chord boundary;
- the fixed-torus versus whole-space scaling distinction;
- the div--curl/BMO endpoint and its non-necessity boundary;
- the exact producer, archived JSON, environment, and certificate manifest;
  and
- the research, novelty, and publication claim boundaries.

## Resolved adversarial findings

The first adversarial pass found four major and six minor issues in the draft.
Every one was corrected before this verdict.

1. The reduced resolvent is now defined by inverting
   \(\lambda_1I-Q\) only on the lower spectral plane. The report explicitly
   notes that the full operator is singular and that the derivative direction
   \(H\) is symmetric.
2. The exact geometric variable is \(|\nabla P_1|\).
   The normalized quantity
   \[
   \chi_Q=\frac{|\nabla Q|}{\lambda_1-\lambda_2}
   \]
   is stated only as a sharp sufficient upper majorant, not as an exact or
   necessary coefficient.
3. Whole-space and rescaled-domain criticality are separated from
   fixed-torus replication. The report no longer claims fixed-torus
   \(L^3\)-invariance, and the proposed mixed norms satisfy
   \(2/q+3/p=1\).
4. The high--high--low construction is used only to rule out an inherited
   uniform absolute chord-decay argument. BMO is recorded as one classical
   sufficient endpoint; other signed or Carleson-type compensation is not
   excluded.
5. The lower-plane strain \(T\), the regularity assumptions for the integral
   identity, the radial-frame scope, and all relative-gap normalizations are
   explicit.
6. The CLMS bibliographic record and the separate Kozono--Taniuchi 2000 BMO
   and Kozono--Ogawa--Taniuchi 2003 Besov roles are correctly delimited.

## Mathematical findings

### Spectral and projector algebra

For

\[
 Q=\lambda_1P_1+\lambda_2P_2+\lambda_3P_3,
 \qquad \lambda_1>\lambda_2\ge\lambda_3,
\]

the report correctly derives

\[
 S:Q=(\lambda_1-\lambda_2)(P_1:S)
      -(\lambda_2-\lambda_3)(P_3:S)
\]

and the orthogonal anisotropy split

\[
 Q-\frac{\operatorname{tr}Q}{3}I
 =a\left(P_1-\frac I3\right)+D,
 \qquad
 \left|Q-\frac{\operatorname{tr}Q}{3}I\right|_F^2
 =\frac23a^2+\frac12d^2.
\]

The reduced-resolvent differentiation gives, for symmetric \(H\),

\[
 DP_1[H]
 =\sum_{j=2}^3
 \frac{P_jHP_1+P_1HP_j}{\lambda_1-\lambda_j},
 \qquad
 |DP_1[H]|_F
 \le\frac{|H|_F}{\lambda_1-\lambda_2}.
\]

The Frobenius constant one is optimal. Applying the identity to spatial
derivatives distinguishes the exact off-diagonal projector variation from
the potentially loose full-gradient majorant \(\chi_Q\).

### Identical covariance and opposite work

The six-mode base field uses the resonant frequencies

\[
 n=(1,1,0),\qquad p=(4,-5,0),\qquad q=(-5,4,0)
\]

with squared radii \(2,41,41\). Strict factor-four separation makes the low
and high responses orthogonal, while radiality makes the two high responses
identical. The exact Fourier/Parseval calculation gives

\[
 \mathfrak P_Q(\xi)=\frac{9\sqrt{41}}{164},\qquad
 \mathfrak E_S(\xi)=-\frac{9\sqrt{41}}{3362},\qquad
 \mathfrak I(\xi)=\frac{351\sqrt{41}}{6724},
\]

and the full/principal/defect split is exact.

Adding the separated 49/197 shear filler and changing only the sign of the
base field gives two smooth, real, mean-zero, divergence-free ten-mode
fields with identical pointwise \(Q\). Exhaustive enumeration finds no
zero-sum triple containing a filler mode, so

\[
 \mathfrak P_Q(\omega_{\Lambda,\pm})
 =\pm\frac{9\sqrt{41}}{164}\Lambda^3.
\]

Because the two high polarizations are orthogonal,

\[
 \operatorname{tr}Q(\xi)\le4.
\]

Together with the filler lower eigenvalue \(12\), Weyl's inequality gives

\[
 \lambda_1-\lambda_2\ge8\Lambda^2,\qquad
 \frac{\lambda_1-\lambda_2}{\lambda_1}\ge\frac23,\qquad
 \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}\ge\frac12.
\]

Thus the same pointwise covariance and a strong genuine eigengap coexist
with opposite nonzero principal work. This proves a sign/amplitude no-go for
\(Q\)-only laws; it does not exclude estimates using additional structure.

### Response lift and common-channel boundary

The response operators

\[
 H^+=U\otimes U+C\otimes C,\qquad
 H^-=U\otimes U-C\otimes C,\qquad
 H^\Delta=2C\otimes C
\]

satisfy \(H^+=H^-+H^\Delta\), and their response traces are respectively
\(1\), \(\Gamma\), and \(1-\Gamma\). Before convolution these traces recover
\(\omega\otimes\omega\), \(Q\), and the complete-frame defect.

On the sharp high--high--low family, the full and principal symbols remain
order one while the defect is order \(M^{-1}\). This rules out copying the
R0.70Y summable absolute chord-kernel proof to full stretching. It does not
prove that BMO is necessary and does not rule out other compensated
estimates.

## Reproduction evidence

The following checks passed in the pinned local environment:

- exact producer reproduction: archived stdout byte-for-byte identical;
- R0.70Z focused gate: **8/8 PASS**;
- full repository suite: **697/697 PASS**;
- certificate SHA-256 verification: **8/8 OK**;
- focused ESLint check: **PASS**;
- bilingual build: **105 pages, 9,855 translations, 41 pre-existing stale
  translations**; and
- vinext production build: **5/5 stages PASS**.

Python 3.12.13, SymPy 1.14.0, and Node v24.19.0 were used. No
floating-point arithmetic occurs in the exact mathematical payload. No DNS,
stochastic search, GPU, or DGX computation was needed.

Two independent adversarial rereads also returned zero blocker, zero major,
and zero minor finding after the corrections. One reread independently
re-derived all three strengthened eigengap constants rather than relying on
the archived JSON.

## Literature and claim boundary

The report distinguishes covariance-projector geometry from the physical
vorticity-direction and physical strain-eigenvalue criteria in the cited
literature. It uses CLMS and Hardy--BMO duality only for a classical
sufficient endpoint. The bounded collision search supports no priority
claim, and the report makes none.

No enstrophy closure, continuation criterion, singularity, global
regularity, or Millennium-problem conclusion is asserted.

## Publication boundary

No publication, public-page update, remote push, or GitHub Pages deployment
was performed. R0.70Z remains a local audited research release pending the
separate publication-approval workflow.
