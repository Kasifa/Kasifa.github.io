# R0.74K independent finite-certificate audit

**Audit date:** 2026-09-02

**Verdict:** `R074K_CERTIFICATE_INDEPENDENT_AUDIT_PASS`

This audit checks only the exact finite shell, exponent, and conditional
scaling arithmetic in the R0.74K certificate. It does not promote any
conditional analytic statement to a theorem.

## 1. Bound sources

| Artifact | SHA-256 |
|---|---|
| `scripts/r074k_single_collar_exponent_certificate.py` | `c1de693bdae761826608ece64d518035e2d732578b191ce01158f30adedf0b5b` |
| `research/r074k_single_collar_exponent_certificate.json` | `67e4ab156d7d5a73fd07e584f3f87f7c9287591856b285bd9a747d00f85de41f` |
| `research/r074k_single_collar_exponent_certificate_report.md` | `86ee3ec729a087214a06c6520306bc6f8b8487d9f9df9aabe611276150b68958` |
| `scripts/r074k_single_collar_exponent_certificate_independent.rb` | `b37394432f673a9084acad963eafe32f9ab995243e1cff85fe3f819de184cc79` |
| `research/r074k_single_collar_shear_lag_reduction.md` | `20f5c41db46ecb8994a095778106eca0c6a5b2620fb8df85022eba53fd93f72f` |
| `research/r074k_problem_freeze.md` | `f95b0932695992fdc35df59f8783ef84ae04722ab9a722128704025d38aec64d` |
| `research/r074k_gap_matrix.md` | `1ba7bf28e369a5fa8b9404438c618834fd29d5329b915f98e3d70ea463e7c7b1` |
| `research/r074k_report-source.md` | `c8820190253366b8d33c7d843905e5cd7e0b45dd7c3f5ef4e78b89246b982af6` |

The verdict does not transfer to changed source bytes without a new rebind.

## 2. Reproduction results

The Python producer was run and compared directly with the frozen JSON:

```text
python3 scripts/r074k_single_collar_exponent_certificate.py |
  cmp -s - research/r074k_single_collar_exponent_certificate.json
```

The command exited zero. The producer reports `PASS 41/41`, and its stdout is
byte-identical to the frozen JSON.

The independent implementation was then run with the system Ruby:

```text
/usr/bin/ruby scripts/r074k_single_collar_exponent_certificate_independent.rb
```

It returned:

```text
frozen_json_used_as_arithmetic_input=false
independentPassed=41
independentTotal=41
mismatchCount=0
failedIds=
nearestPositiveVolumeWrongMargin=536399/8583708672
uniformDeepMargin=204385/134120448
result=PASS
```

The executable Ruby code contains no file or JSON read. Its 41 check IDs are
unique and occur in exactly the same order as the 41 unique Python and frozen
JSON IDs.

## 3. Exact-value and sign audit

An additional read-only `Fraction` reconstruction checked every equality
value and every strict sign. In particular:

1. The nearest-boundary and positive-volume free-tail margins are
   respectively

   \[
   \frac{15263}{134120448}>0,
   \qquad
   \frac{536399}{8583708672}>0.
   \]

   These are wrong-direction exponents. A passing arithmetic row here records
   the strict failure of free tail as a proof mechanism, not success of the
   desired analytic estimate.

2. The sharp \(p=2\) margin at \(m=2\), the uniform optimistic margin for
   \(m\ge2\), and the padding-robust \(m=2\) margin are

   \[
   \frac{221281}{134120448}>0,
   \qquad
   \frac{204385}{134120448}>0,
   \qquad
   \frac{13471441}{8583708672}>0.
   \]

3. The inherited denominator \(262\) has the recorded transition

   \[
   -\frac{28319}{266208768}<0 \quad(m=2),
   \qquad
   \frac{139297}{266208768}>0 \quad(m=3).
   \]

4. The adjacent outer-shell exponent retains

   \[
   3c_\gamma-\rho
   =\frac{1237}{423360}>0
   \]

   after one inverse-\(R\) loss.

5. The conditional power ledger cancels the annular weight and gives

   \[
   \frac{\mathfrak a_j^2B_j}{R_j}
   (\Gamma_jL_jR_j^5)
   =B_j^3L_jR_j^4
   =(B_jR_j^2)B_j^2L_jR_j^2.
   \]

All equality rows have zero stored margin. All strict comparison rows have a
strictly positive stored margin under the certificate's margin convention.

## 4. Analytic-status and report boundary

The frozen JSON status flags are internally consistent:

```text
finite_arithmetic=PASS
nearest_free_tail=FAIL_FREE_TAIL_AS_PROOF_MECHANISM
required_next_mechanism=ANALYTIC_SHEAR_LAG_REQUIRED
conditional_collar_hypothesis=OPEN
clay_problem=NOT_CLAIMED
```

The certificate report preserves the same boundary. The bound main note also
states that R0.74K Theorem 4.1 is an implication whose hypothesis (4.3)
remains open. The gap matrix keeps the matching upper bounds for
\(\mathfrak C_j\) and \(X_j\) open and records no universal endpoint or Clay
claim. The problem freeze expressly forbids converting the finite exponent
test into the missing bridge/shear-expulsion estimate.

## 5. Audit limit

This audit does not prove a Brownian-bridge estimate, exceptional-path
suppression, the time-coupled collar-BV bound, Theorem 4.1's open hypothesis,
a matching observable upper bound, a universal endpoint estimate, regularity,
singularity formation, novelty, or priority.

**NOT CLAY.**

## 6. Final source-rebind addendum

The contextual R0.74K sources were repaired after the first certificate
audit. The finite producer, frozen JSON, certificate report, and independent
Ruby implementation did not change. This addendum binds the audit verdict to
the final contextual bytes below.

| Artifact | Final SHA-256 |
|---|---|
| `scripts/r074k_single_collar_exponent_certificate.py` | `c1de693bdae761826608ece64d518035e2d732578b191ce01158f30adedf0b5b` |
| `research/r074k_single_collar_exponent_certificate.json` | `67e4ab156d7d5a73fd07e584f3f87f7c9287591856b285bd9a747d00f85de41f` |
| `research/r074k_single_collar_exponent_certificate_report.md` | `86ee3ec729a087214a06c6520306bc6f8b8487d9f9df9aabe611276150b68958` |
| `scripts/r074k_single_collar_exponent_certificate_independent.rb` | `b37394432f673a9084acad963eafe32f9ab995243e1cff85fe3f819de184cc79` |
| `research/r074k_single_collar_shear_lag_reduction.md` | `8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3` |
| `research/r074k_problem_freeze.md` | `ddb9467b2a68faae8f85bfc208393cd00fd90bc51ef02d723dfab24216bde2e4` |
| `research/r074k_gap_matrix.md` | `61382ecdd6ada4ef91883390ab03afbbc832c5ecd066fb7f26e22f11d916a4dc` |
| `research/r074k_report-source.md` | `457a0a72aa36fb35d8924b9d4af5cfc826c363e6b01852c8b3fc87be8fb7288b` |

The Python producer was rerun against the frozen JSON and remained
byte-identical with `PASS 41/41`. The independent Ruby implementation again
returned `independentPassed=41`, `independentTotal=41`, `mismatchCount=0`, and
`result=PASS` without reading the frozen JSON or Python source.

The final main note now gives an explicit positive-volume box for the nearest
inner-shell obstruction and retains the same certified wrong-sign fraction.
R0.74K Theorem 4.1 remains a sufficient implication whose signed hypothesis
(4.3) is open. The final problem freeze asks which direct analytic condition
would suffice along the selected normalized-bridge route; it does not claim
logical necessity. The gap matrix and report source keep the matching
\(\mathfrak C_j\) and \(X_j\) upper bounds, the universal endpoint theorem,
and the prescribed-point route open.

The contextual hashes in this addendum supersede the corresponding earlier
contextual hashes in Section 1. The finite arithmetic verdict and all analytic
status flags are unchanged.

> **FINAL REBIND VERDICT: `R074K_CERTIFICATE_FINAL_REBIND_PASS`.**

**NOT CLAY.**
