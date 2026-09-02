# R0.74S Step 1 — primary audit of the weighted stopped-Abel gate

## Result

**PASS.**  The stopped-Abel identity, weight-gap estimate, component formula,
two-sided coefficient-mass comparison, ideal complementary-collar
calculation, and algebraic sharpness witness were recomputed from their
definitions.  This is a primary self-audit, not an independent mathematical
audit.  **NOT CLAY.**

## 1. Algebraic recomputation

For \(c_0=c_{M+1}=0\),

\[
 \sum_{k=1}^{M}c_k(b_{k+1}-b_k)
 =\sum_{m=1}^{M+1}(c_{m-1}-c_m)b_m,
\]

which is exactly (S.5)--(S.6) after writing the two endpoint terms
separately.  No positivity, differentiability, PDE, or limit exchange beyond
a finite sum is used.

For one active block \([p,q]_{\mathbb Z}\), strict decrease of \(\gamma_k\)
gives

\[
 V_\gamma
 =\gamma_p+\sum_{k=p+1}^{q}(\gamma_{k-1}-\gamma_k)+\gamma_q
 =2\gamma_p.
\]

Separated blocks add, proving (S.9).  Since
\(\gamma_{k+1}/\gamma_k\le32/35\), each block mass is at most
\((35/3)\gamma_p\); hence
\((6/35)\sum_{A}\gamma_k\le V_\gamma(A)\le2\sum_A\gamma_k\).

**Decision: PASS.**

## 2. Exponential and collar constants

The adjacent exponent difference is

\[
 \frac{4^k-4^{k-1}}{32}
 =\frac{3\cdot4^{k-1}}{32}\ge\frac3{32}.
\]

Using \(e^x\ge1+x\),
\(e^{-3/32}\le(1+3/32)^{-1}=32/35\), so the relative gap is at least
\(3/35\).  The shared collar has derivative scale \(8/R\), giving the
coefficient \(8(3/35)/R=24/(35R)\) in (S.15).

The complementary-profile identity is deliberately a best-case
idealization.  It is not attributed to the frozen R0.74E cutoff
\(\vartheta\), which was not required to satisfy
\(\vartheta(z)+\vartheta(-z)=1\).

**Decision: PASS WITH SCOPE BOUNDARY.**

## 3. Sharpness witness

At each time, let \(d_m=c_{m-1}-c_m\).  Choosing
\(b_m=B\operatorname{sgn}d_m\) gives

\[
 \sum_md_mb_m=B\sum_m|d_m|=BV_\gamma(A).
\]

Thus the triangle-inequality estimate (S.17) is saturated in the class of
integrable adjacent-boundary data.  The construction imposes no
Navier--Stokes equation and therefore rules out only an algebraic
improvement after absolute values.

**Decision: PASS.**

## 4. Finite certificate and reproducibility

The certificate passes:

- 6/6 exact rational checks;
- 2/2 exhaustive finite ledgers;
- all 16 binary active sets for the exact rational \(M=4\) Abel,
  component, and saturation fixtures;
- all 4096 binary active sets through \(M=12\) for the actual exponential
  weights at 80-decimal precision; and
- 16/16 structural and claim-boundary checks.

Two consecutive runs regenerated the JSON and report byte for byte.  A
negative mutation deleting the factor \(2\) in (S.9) was rejected.

| Artifact | SHA-256 |
|---|---|
| r074s_problem_freeze.md | 3c5d1aad6b1c7d1b687917a384b1e104f8586e12d9b93e79e0ba99cb55809982 |
| r074s_weighted_abel_no_gain.md | cfc949386d448d69f33699c6d223865b4ad5ec92591ea1e675c0daad8f168a69 |
| r074s_weighted_abel_certificate.py | eec65234ac4f662560bbc7254d111733de110c9d1bf9f9e9e7ad598481b80ab5 |
| r074s_weighted_abel_certificate.json | 125324b0dafc3e13b1860c283fc74bfa00276888260ac1ffe461d848ffdb221d |
| r074s_weighted_abel_certificate_report.md | c18a06755804195004fc8396187abe146830a4a77b9e79015a79e192cc820159 |

The finite checks do not prove the exponential estimate for all \(k\), the
analytic Abel theorem, the binding to the actual padded flux, or any PDE
sign estimate.

## 5. Research consequence

The result rejects one narrow route: Abel summation cannot be followed by
absolute values with the expectation that the frozen weight coefficients
themselves provide shell compression.  A viable continuation must derive
the actual time-dependent stopped-test identity and preserve signed boundary
work, exterior supply/leakage, negative work/backscatter, pressure,
moving-frame drift, and temporal jump terms until the final estimate.

The actual binding and every regularity consequence remain **OPEN**.
