# R0.73Y independent re-audit

**Audit date:** 2026-09-01

**Final status:** `PASS / RELEASE_GATE_PASS`

**Audit mode:** independent read-only mathematical, literature-boundary, and
certificate-adversarial review; the audit did not edit the audited files

## 1. Frozen objects

| Object | SHA-256 |
|---|---|
| `research/r073y_exact_shear_no_go.md` | `2574f2caf19248a17d25f811488db1c7b30295efd07e59852c3afa17cf8f69e4` |
| `research/r073y_primary_literature_audit.md` | `13fcf43cfae17cbf4a5f0e171d3d602eccc9b4e0f24f093cfc3ab84187cf6871` |
| `research/r073y_evidence_gap_matrix.md` | `76e5d8b6bf3f9efc4217b06cea1af2c6408eb9ad7b6dc953676828e33a7195fb` |
| `research/r073y_report-source.md` | `d2f4df01b51ec613affc4b14a3544f6f702584de1ba1a94b2ec241e31d5efd01` |
| `scripts/r073y_exact_shear_certificate.py` | `f682784c64142f958a18936fc488dac6b83e28ce85610b27f07a669c8c61d417` |
| `research/r073y_exact_shear_certificate.json` | `fe6bb0e8bb4674f63a579f6b2db92c12f75235c4d293594e115c7b49599ef4df` |
| `research/r073y_exact_shear_certificate_report.md` | `668177c61721600880cd85651f8481249c8f9a972d631dd4f5a3383bbb07c6aa` |

The certificate payload hash is
`51f721cf560df38fbeacdd093d4293adae10635e13dcaa6b9251616c4f7eca2c`.

## 2. Mathematical audit

The general class

\[
 u^A(t,x)=A a\,H_{\nu|k|^2t}f_0(k\cdot x),
 \qquad a\cdot k=0,
\]

was re-derived independently.  The audit verified:

1. divergence and convection vanish, while the heat factor
   \(\nu|k|^2\) gives \(\partial_tu=\nu\Delta u\);
2. the spatial heat scale is exactly \(s|k|^2\);
3. \((a\otimes a):(a\otimes k)=|a|^2(a\cdot k)=0\), hence
   \(\Pi_s=0\) at every positive scale;
4. the centered production vanishes by oddness in the Euclidean-lift
   Gaussian coordinate parallel to \(a\), including non-axis-aligned
   integer \(k\);
5. the displayed \(D_{ii,s}\) is a strictly positive heat-kernel variance
   for every nonconstant member, \(A\ne0\), and \(s,t>0\);
6. Haar pushforward gives zero spatial mean, and the analytic zero-set
   argument plus R0.73X homogeneity gives the positive \(|A|^3C\) size;
7. the conclusion is precisely a no-go for zero-preserving
   production-only moduli.  It does not refute debt- or covariance-sensitive
   criteria, epsilon regularity, or any Clay conclusion.

No mathematical blocker was found.  The imported definitions of the R0.73X
exterior functional remain dependencies rather than being reproved in this
note; only their stated positivity and amplitude homogeneity are used.

## 3. Literature-boundary audit

The audit found direct prior-art collisions, not a priority claim:

- periodic exact heat shears are classical and occur explicitly on
  \(\mathbb T^3\) in Jeong--Yoneda (2022);
- Vreman (2004) includes simple shear among exact zero-SGS-dissipation
  derivative classes;
- Germano (1992) and Eyink--Aluie (2009) already separate signed production
  from nonnegative gradient covariance in exact coarse-grained ledgers;
- Johnson (2020) supplies the Gaussian diffusion-scale stress framework;
- Yu's 2026 preprints already articulate the adjacent observability and
  positive anti-kernel direction and are labelled as preprints.

Accordingly, the public claim is restricted to a
**literature-calibrated exact obstruction** for the particular frozen
R0.73X production-only bridge.  The bounded search found no verbatim match
for the whole package, but this is not evidence of novelty or priority.

## 4. Certificate adversarial audit

Three audit rounds were required.  The first found Python scalar equality
could confuse `bool`, `int`, and `float`; the second found ordinary JSON
parsing could hide duplicate keys.  Both blockers were repaired before this
final verdict.

The final gate now enforces:

- strict JSON scalar types and exact dict/list structure;
- a narrow portable-float whitelist limited to computed numerical outputs,
  while frozen `n/s/x2` inputs remain exact;
- rejection of duplicate keys at every nesting level, nonfinite JSON
  constants, and every noncanonical raw JSON representation;
- exact payload hashing and an exact report regenerated from the hash-sealed
  stored payload;
- seven built-in resealed-mutation tests covering type, key inventory, list
  length, duplicate-key raw text, and noncanonical raw text.

Independent attacks covered nested duplicate keys, duplicate-plus-reseal,
lexically equivalent floats, whitespace/CRLF/missing-newline variants,
`NaN`/`Infinity`, overflow floats, signed zero, type/container drift,
key/list drift, hash-only mutation, and report/hash decoupling.  No bypass
remained.  `/usr/bin/python3` 3.9.6 and bundled Python 3.12.13 both passed
`--check-only`; file size, mtime, and ctime were unchanged.

## 5. Release boundary

`RELEASE_GATE_PASS` applies to the frozen research objects above.  It is not
a review of later HTML, PDF, figure, deployment, or live-site artifacts;
those require separate publication gates.

**NOT CLAY.**
