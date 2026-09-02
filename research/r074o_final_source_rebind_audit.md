# R0.74O final source rebind audit

## 1. Exact final binding and verdict

This fail-closed rebind was run after the two reported source defects had
been repaired and after the independent mathematical reconstruction.  It
binds exactly the following three current source objects.

| Object | SHA-256 | Bytes | Lines |
|---|---|---:|---:|
| research/r074o_problem_freeze.md | c461b85425e58ad0bb371bf7e1e6fe79301fd200912c67a15d4d8ebefb9ec54f | 6,374 | 275 |
| research/r074o_amplitude_endpoint_counterexample.md | 471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb | 19,241 | 911 |
| research/r074o_gap_matrix.md | 11aaae9308056cb2afa5b8d3166fbeecf9713aeb77e05bd5128fc3835231cdcd | 6,832 | 48 |

**Verdict: PASS.**  The three hashes are the same hashes bound in
research/r074o_amplitude_endpoint_independent_audit.md.  All equation tags
are unique, display and inline delimiters are balanced, the duplicate
pressure sentence is absent, and equation (6.9) contains exactly two
well-formed fractions with one denominator attached to each numerator.

## 2. Equation-tag inventory

### 2.1 Problem freeze

The problem freeze contains exactly 21 tags, all 21 unique:

\[
\begin{gathered}
 F.1,\ F.2,\ F.3,\ F.4,\ F.5,\ F.6,\ F.7,\ F.8,\ F.9,\ F.10,\ F.11,\\
 F.12,\ F.13,\ F.14,\ F.15,\ F.16,\ F.17,\ F.18,\ F.19,\ F.20,\ F.21.
\end{gathered}
\]

There is exactly one opening and one closing display delimiter around each
tagged display.

### 2.2 Main proof

The main proof contains exactly 75 tags, all 75 unique:

\[
\begin{gathered}
 0.1,\ 0.2,\ 0.3,\ 0.4;\\
 1.1,\ 1.2,\ 1.3,\ 1.4,\ 1.5,\ 1.6,\ 1.7,\ 1.8,\ 1.9,\ 1.10,\ 1.11,\ 1.12;\\
 2.1,\ 2.2,\ 2.3,\ 2.4,\ 2.5,\ 2.6,\ 2.7,\ 2.8,\ 2.9,\ 2.10,\ 2.11,\
 2.12,\ 2.13,\ 2.14,\ 2.15;\\
 3.1,\ 3.2,\ 3.3,\ 3.4,\ 3.5;\\
 4.1,\ 4.2,\ 4.3,\ 4.4,\ 4.5,\ 4.6;\\
 5.1,\ 5.2,\ 5.3,\ 5.4,\ 5.5,\ 5.6;\\
 6.1,\ 6.2,\ 6.3,\ 6.4,\ 6.5,\ 6.6,\ 6.7,\ 6.8,\ 6.9,\ 6.10,\ 6.11;\\
 7.1,\ 7.2,\ 7.3,\ 7.4,\ 7.5,\ 7.6,\ 7.7,\ 7.8,\ 7.9,\ 7.10,\ 7.11;\\
 8.1;\\
 9.1,\ 9.2,\ 9.3,\ 9.4.
\end{gathered}
\]

Again, each tag lies in exactly one display block.

### 2.3 Gap matrix and package total

The gap matrix intentionally has no equation tags or display blocks.  Across
the complete three-file bound package there are therefore exactly 96 tags,
all 96 unique.  The \(F.\)-prefix prevents any cross-file collision between
the 21 freeze tags and the 75 main-proof tags.

## 3. Delimiter and byte-level hygiene

The independent source scan returned:

| Object | Display opens/closes | Inline opens/closes | Tabs | CR bytes | Other ASCII controls |
|---|---:|---:|---:|---:|---:|
| problem freeze | 21 / 21 | 20 / 20 | 0 | 0 | 0 |
| main proof | 75 / 75 | 60 / 60 | 0 | 0 | 0 |
| gap matrix | 0 / 0 | 45 / 45 | 0 | 0 | 0 |

Thus no unmatched TeX delimiter, tab, carriage return, or hidden ASCII
control character was found in any bound source.

## 4. Reported-defect audit

### 4.1 Pressure sentence

The exact sentence prefix

    Although the physical pressure is zero, the frozen local pressure gauge is

occurs exactly once in the main proof, at source lines 260--261.  It is
followed immediately by the averaged local Riesz estimate.  There is no
adjacent duplicate and no second occurrence elsewhere in the file.

**Result: PASS; duplicate removed.**

### 4.2 Equation (6.9)

The exact display at source lines 615--624 has the structure

\[
 \frac{X_R^{\alpha,*}}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 \frac{\mathfrak C_R^{\alpha,*}}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 P_*^{86/11907}(1+\log_+P_*)^{2/3}\longrightarrow\infty.
\]

The source block contains:

1. exactly two \(\backslash\mathrm{frac}\) commands;
2. exactly two occurrences of the intended denominator
   \(P_*^{2/3}\sqrt{1+\log_+P_*}\);
3. one denominator immediately following each of the two numerators;
4. zero detached or repeated denominator lines; and
5. net TeX-brace balance zero.

The first fraction belongs to \(X_R^{\alpha,*}\); the second belongs to
\(\mathfrak C_R^{\alpha,*}\).  The subsequent power-log factor is outside
both fractions, as required.

**Result: PASS; equation (6.9) is well formed.**

## 5. Cross-source claim rebind

The final source relations are internally aligned.

| Claim | Problem freeze | Main proof | Gap matrix | Rebind result |
|---|---|---|---|---|
| exact every-amplitude 2D3C family | (F.7)--(F.10) | (1.7)--(1.12) | O1--O3 | PASS |
| complete payment \(P_*\asymp B^3R^3\) | (F.11)--(F.15), target (F.20) | (2.2)--(3.5) | O4--O10 | PASS |
| quadratic signed-flux scaling | (F.16)--(F.18) | (4.1)--(4.6) | O11--O13 | PASS |
| non-circular matching \(X_*\) law | (F.19) and gate 5 | (5.1)--(5.6) | O14--O15 | PASS |
| \(q_*=8024/11907\), \(\delta_*=86/11907\) | target (F.21) | (6.1)--(6.9) | O16--O18 | PASS |
| fixed-\(\gamma\) polynomial corollary | promotion scope | (7.1)--(7.11) | O19 | PASS |
| NOT CLAY boundary | freeze Section 5 | proof Section 10 | O20--O26 | PASS |

No gap-matrix row upgrades an open or unclaimed statement beyond the main
proof.  In particular, O23--O26 continue to exclude augmented-observable,
singularity, global-regularity, and novelty claims.

\[
 \boxed{\text{FINAL SOURCE REBIND: PASS; 96/96 UNIQUE TAGS; NOT CLAY.}}
\]
