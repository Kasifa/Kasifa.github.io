# R0.74J — final full-source rebind audit

**Audit date:** 2026-09-02
**Verdict:** `R074J_FINAL_SOURCE_REBIND_PASS`
**Blocking findings:** none

This audit binds the final R0.74J proof, the two independent analytic audits,
the repaired four-source literature boundary, the exact certificate, the
bilingual notation boundary, and the sealed formal-figure package.  It checks
the exact-family matching complete-payment theorem and its stated limits.  It
does not establish novelty, priority, a universal endpoint upper estimate, a
good scale at a possible singular point, singularity exclusion, global
regularity, or the Millennium problem.  **NOT CLAY.**

---

## 1. Final byte binding

All digests below were recomputed from the final local files.

| Artifact | SHA-256 |
|---|---|
| `research/r074j_problem_freeze.md` | `383e4e8e9a983e4b74050e657bd11fa234ad8dfe2c6fa3c0ec1a8800781291e0` |
| `research/r074j_matching_payment_law.md` | `d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad` |
| `research/r074j_heat_platform_independent_audit.md` | `45214485a46271174db047c6fb6565c276d712f15c6009e15221626a0d0e9f23` |
| `research/r074j_complete_payment_ledger_independent_audit.md` | `78e18dc6daa3291bb2f7fcf2bd58d56db504560a19ae6b38e2c7b303c89b599c` |
| `research/r074j_gap_matrix.md` | `4e83680b8da9c6d651de1647b9975e2ff32c26ee291a151467b2958e873b9e89` |
| `research/r074j_report-source.md` | `e36e2529f77f81e8a6617652d641e016ece175075862500412e529907d3d4f9f` |
| `research/r074j_primary_literature_boundary.md` | `a4a60575122efde993252a9cafda2a85ea15da7f67aa34d1583dc95552f45c60` |
| `research/r074j_primary_literature_independent_audit.md` | `e72aaafb4eca9c28d0834e514866522c60155bfc3220c39857fd452a01046ae2` |
| `research/r074j_bilingual_dictionary.md` | `3ea788eeb84cd82ae24dd6c9584223b8caef5d927eea8b3a0aef348c81991a8b` |
| `scripts/r074j_matching_payment_certificate.py` | `6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec` |
| `research/r074j_matching_payment_certificate.json` | `493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5` |
| `research/r074j_matching_payment_certificate_report.md` | `6a32098c808373a7d3cfbd30b266f20d0aa33abc2b693e51b48b0c486852fa07` |
| `scripts/r074j_matching_payment_certificate_independent.rb` | `ca3da7fafea86012c58c20801e680c9bb5ed26c712c92d32cc080426f9916197` |
| `research/r074j_certificate_independent_audit.md` | `74a68cf221efd1c30e3461012b2196d7fc38621f36c9648e24fcc4814ee755e2` |
| figure `SHA256SUMS` | `ea4da4d2eefcf57758c479a9cebd99cc14091ad7b42fd45f180bbb54596db366` |
| figure `manifest.json` | `0688dab352ac78c907b712698edd4645a4e1a6eeffb6fab5cb597dfdf05cb6cc` |
| figure `validation.json` | `84eb7a87482a9633aaa9d506a3b6133162cb4510f694a3705a390d1f2f1dcd81` |
| figure `source-data.csv` | `6c1b0da4931222a511d890ea8a78b553244bdaf520cf7f4fb54300dab1f2b54e` |
| figure `plot.py` | `d23cd30c00170ae7262d37d8b38c0de828862a2d20296ecf7fd027021bdb95a0` |
| figure `validate.py` | `a95cbe3f94b230a0ed20ae25a2bda57f1f97c80bcd2d87798436b17f84d02071` |
| figure `figure.svg` | `ed42960e32e7b2e4707bab933bd3ff400e2f0722ba77f7fc53f0dcaeff3d736b` |
| figure `figure.pdf` | `3cabf4a587ae6a7fbf145039740489d1f2ba79e9903ed560779d02e56ecab6f1` |
| figure `figure.png` | `5aef3c61cb0b557411599d0a1ff7dd92e8c89f750f4d7abcfbd3a1d7aaa689b2` |

Both analytic audits bind the same final main-source digest
`d495ff3d...478dbad`.  The primary-literature audit binds that digest together
with the final boundary digest `a4a60575...45c60` and report digest
`e36e2529...d4f9f`.  No verdict is transferred from an earlier byte sequence.

---

## 2. Analytic theorem rebind

### 2.1 Heat platform

For \(R\le1/200\), the final proof uses

\[
 \delta_R=\arcsin(16R)\le32R
\]

and places every \(x_3\in[80R,96R]\) at circular distance at least \(48R\)
from the complement of the positive plateau.  With
\(Z_t\sim N(0,2t)\), periodic reduction modulo \(2\pi\), and
\(0\le1-g\le2\), Chebyshev gives

\[
 1-\theta(t,x_3)
 \le2\frac{2t}{(48R)^2}
 \le\frac{65}{576},
 \qquad
 \theta(t,x_3)\ge\frac{511}{576}>\frac12.
\]

The argument uses no monotonicity or sign condition inside the transition
region of the saturation profile.  The independent heat-platform audit
reconstructed the plateau, circle-distance, periodic-lift, terminal-time, and
cubic-coefficient steps and returned
`INDEPENDENT_HEAT_PLATFORM_AUDIT_PASS` on the final source bytes.

### 2.2 Fifth-shell geometry and complete payment

At payment radius \(2R\),

\[
 I_{2R}=(61R^2,65R^2),
 \qquad
 A_5(2R)=\{64R\le|x|<128R\},
 \qquad \Gamma_5=e^{-8}.
\]

The selected box

\[
 Q_R=\{|x_1|<R,\ |x_2|<R,\ 80R<x_3<96R\}
\]

has volume \(64R^3\) and lies in the fifth shell because
\(96^2+1+1=9218<128^2=16384\).  Hence the nonnegative velocity-cubic row
satisfies, for all sufficiently large \(j\),

\[
 \mathcal G_u(z_{0,j},2R_j;1)
 \ge(2R_j)^{-2}e^{-8}(4R_j^2)(64R_j^3)
       B_j^3\left(\frac12\right)^3
 =8e^{-8}B_j^3R_j^3.
\]

The zero-frame identities make Versions M and F coincide on the exact
R0.74F--H family analysed in R0.74I.  Combining this row with inherited
R0.74G Theorem 1.1 gives

\[
 8e^{-8}B_j^3R_j^3
 \le P_j:=P_{R_j}^M=P_{R_j}^F
 \le CB_j^3R_j^3.
\]

The independent ledger audit reconstructed this chain from the final source
and returned `INDEPENDENT_COMPLETE_PAYMENT_LEDGER_AUDIT_PASS`.

### 2.3 Exact asymptotics and endpoint meaning

With

\[
 \beta_j:=B_jR_j^2\to\frac1{128},
 \qquad R_j=e^{-L_j^2/320},
\]

the two-sided payment law yields

\[
 \frac{\log P_j}{L_j^2}\to\frac3{320},
 \qquad
 \log\frac{P_{j+1}}{P_j}=\frac9{320}L_j^2+O(1),
\]

and

\[
 P_j^{2/3}\sqrt{1+\log_+P_j}
 \asymp B_j^2L_jR_j^2.
\]

The last display is a familywise scale identity.  It is not an upper bound
for \(X_j\) or \(\mathfrak C_j\).  The former still requires an inward-tail
upper audit; the latter separately requires collar-flux and energy upper
audits.  The universal square-root-log endpoint remains open.

The main note has 35 formula tags and 35 distinct tag values.  The canonical
roles remain separated throughout the final source: \(\rho=1/320\) is the
scale-decay rate, \(2R\) is the payment radius,
\(\gamma_j^{\rm tar}\) and \(\Gamma_k\) have distinct indexed roles, and
\(\beta_j\) is not the inherited shear field.

---

## 3. Finite certificate and formal figure

The Python `Fraction` producer returns 38/38 and its stdout is byte-identical
to the frozen JSON.  The independent Ruby `Rational` implementation
reconstructs all 38 rows, compares 287 terminal fields, finds zero
mismatches, and returns PASS.  These are finite arithmetic checks only; they
do not prove the periodic heat representation, the continuum lower bound, or
the inherited R0.74G theorem.

The formal figure package contains exactly 24 files.  Its validator and
verify-only mode both return 79/79; all 23 `SHA256SUMS` rows pass.  The
178 mm by 88 mm vector SVG/PDF and 600-dpi PNG were inspected at master size,
final print size, in grayscale, and through an independent PDF raster.  No
clipping, collision, detached annotation, color-only distinction, or
unreadable label was found.  The figure is an analytic proof diagram with
exact longitudinal coordinates and schematic transverse thickness.  Its
footer visibly says `EXACT FAMILY`, `NOT DNS`, `NOT SIMULATION`, and
`NOT CLAY`.

---

## 4. Primary-literature and claim boundary

The final bounded check covers Yang (2022), Vasseur--Yang (2021), Lei--Ren
(2024), and Wang--Wu--Zhou (2019).  The final sources:

1. use Yang's final Lemma 6, Proposition 7, and Proposition 11, with the
   correct arXiv v2 crosswalk and the common-lifespan qualifier;
2. record Vasseur--Yang's prior suitable-weak use of mollified-flow
   recentering and skewed cylinders;
3. distinguish Lei--Ren's spatial interval, regular time epoch, and
   axisymmetric one-point criterion; and
4. include Wang--Wu--Zhou's velocity-only one-scale theorem, its 2019
   metadata, and the \(Q(1)\to Q(1/16)\) scope.

The independent literature audit returns
`BOUNDED_FOUR_SOURCE_PRIMARY_LITERATURE_AUDIT_PASS`.  It finds no matching
complete-payment theorem in this four-paper corpus.  That is a bounded
non-hit, not evidence of novelty or priority.

---

## 5. Release boundary and final verdict

The final source proves only the matching complete-payment law and its
asymptotics on one frozen smooth periodic unforced family.  It does not prove:

- a universal complete-payment upper theorem;
- a matching upper bound for \(X_j\) or \(\mathfrak C_j\);
- payment-to-admissibility or core-from-shell control;
- a good-scale theorem at a prescribed possible singular point;
- existence or exclusion of a singular suitable weak solution;
- global regularity; or
- novelty, priority, or resolution of the Millennium problem.

Text sources use LF line endings with no BOM or CRLF.  The main formula-label
audit, certificate reconstruction, figure seal, exact-source analytic
rebinds, literature rebind, and notation boundary all pass.

> **FINAL VERDICT: `R074J_FINAL_SOURCE_REBIND_PASS`.**

**NOT CLAY.**
