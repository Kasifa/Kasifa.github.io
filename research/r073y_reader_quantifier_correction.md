# R0.73Y reader quantifier correction

**Status:** reviewed publication correction; the frozen research bytes remain unchanged

**Frozen source commit:** `1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66`

**Frozen report SHA-256:** `d2f4df01b51ec613affc4b14a3544f6f702584de1ba1a94b2ec241e31d5efd01`

**Authority:** `research/r073y_exact_shear_no_go.md`, Theorem 1.1, which explicitly states strict gradient-covariance positivity only when \(A\ne0\)

**Public subtitle (zh):** 全尺度零 production、A≠0 时严格正 heat covariance 与最小修复边界

**Lead (zh):** R0.73X 留下的 signed-to-positive coercivity 桥，至少在 production-only 形式下是假的。存在一整个光滑、零均值的周期 Navier--Stokes exact shear 类：对每个实振幅，\(\Pi_s=\mathscr S_s=Q_s=0\) 在所有正 heat 尺度上成立；对每个非零振幅 \(A\ne0\)，\(D_{ii,s}>0\) 逐点严格成立；零振幅成员是平凡场，且 \(D_{ii,s}=0\)。因而，零输入上取零的 production-only functional 不可能给出振幅无关的有限 coercive modulus。这是 exact no-go theorem，不是正则性判据。

**Home summary (zh):** 该 exact shear 类是真实的光滑周期 NSE 解。对所有实振幅，signed production 在每个正 heat 尺度上为零；对非零振幅 \(A\ne0\)，gradient covariance 严格为正且正尺度 size 按 \(|A|^3\) 增长。本节因此关闭 production-only coercivity 路线，但不提供任意三维解的新正估计。

## 1. Why a correction layer is required

The frozen theorem is correct: its strict inequality is conditional on
\(A\ne0\). The later frozen Chinese reader report omitted that condition in
three displayed summaries. At \(A=0\), the field is identically zero and
\(D_{ii,s}=0\), so an unconditional strict inequality would be false.

The frozen report is retained byte-for-byte because it is already bound into
the research, certificate, and figure provenance graph. Publication must not
silently rewrite that evidence. Instead, this reviewed correction is a new
reader-layer source, and the release generator must apply an exact, counted
transformation before producing HTML or PDF.

## 2. Ordered exact replacements

| ID | Frozen reader shorthand | Required public reading |
|---|---|---|
| `Q1` | Section 1 introduces an arbitrary-amplitude class and then displays \(D_{ii,s}>0\) without a condition | zero production holds for every \(A\in\mathbb R\); strict covariance holds only for \(A\ne0\); at \(A=0\), \(D_{ii,s}=0\) |
| `Q2` | Section 2 calls the structural heat variance strictly positive without first stating the amplitude condition | prepend \(A\ne0\Rightarrow\) to the strict formula and state the trivial zero member separately |
| `Q3` | Section 3 ends the single-mode lower bound with an unconditional strict inequality | prepend \(A\ne0\Rightarrow\) to that lower bound |
| `Q4` | hero/subtitle says only `STRICTLY POSITIVE` | display `STRICTLY POSITIVE FOR A != 0; ZERO FOR A = 0` |
| `Q5` | formulas (1.3), (2.2), and (3.1) contain the literal token `qquad` without the required TeX escape | replace exactly those three tokens by `\qquad`; this is a reader-only typesetting repair |

The corrected display (3.3) must use an aligned multiline layout so that both
the \(A\ne0\) inequality and the \(A=0\) endpoint remain visible on an A4 PDF.
Markdown emphasis in the frozen references and `NOT CLAY` line must be rendered
as HTML emphasis rather than exposed as literal asterisks. These are
nonsemantic reader repairs; they change no formula, quantifier, citation, or
claim boundary.

Each frozen snippet must occur exactly once before transformation and zero
times afterward. A missing, duplicated, or newly altered snippet is a release
failure. The explicit `Lead (zh)` and `Home summary (zh)` above replace
formula-stripped paragraph concatenation and must be used verbatim after
whitespace normalization.

## 3. Machine-readable correction boundary

```text
readerCorrectionVersion=1
frozenReportBytesPreserved=true
publicTransformation=EXACT_COUNTED_REPLACEMENTS
typesettingNormalization=EXACT_COUNTED_NONSEMANTIC_REPAIRS
zeroProduction=ALL_REAL_A
strictGradientCovariance=ONLY_A_NE_0
zeroAmplitudeGradientCovariance=0
gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY
strictPositivityFromSampling=FALSE
recapPolicy=MILESTONE_ONLY
latestPublishedRelease=r073y
latestRecapRelease=r073x
clayConclusion=OPEN
NOT CLAY
```

This correction changes no theorem, formula data, figure curve, certificate,
or literature attribution. It repairs only the omitted quantifier in the
reader-facing summaries and makes the zero-amplitude endpoint explicit.
