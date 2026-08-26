# R0.71X independent audit record

**Date:** 2026-08-26
**Decision:** PASS after the listed repairs; producer, independent algebra,
nonlinear retained-coset checks, and final proof re-review all pass.

## 1. Audited statement

The audited claim is restricted to the fixed-dimensional, globally smooth
triangular family constructed in R0.71W.  For every fixed sufficiently small
coupling \(0<\delta\le\delta_*\) and all sufficiently large admissible \(q\),
the amplitude law

\[
 \mathscr A_{q,\delta}=\delta q^2
\]

has the scales

\[
 D_{q,\delta}\asymp\delta^2q^6,
 \qquad
 \mathcal J_{q,\delta}\asymp\delta^2q^2,
 \qquad
 \Lambda_1(I;u_{q,\delta})\asymp_{\nu,\delta_*}1.
\]

The prescribed target roots are the complete real-time target zero set in the
declared interval.  Consequently

\[
 \frac{\mathcal J_{q,\delta}}
 {D_{q,\delta}^{1/3}\Lambda_1(I;u_{q,\delta})}
 \asymp\delta^{4/3}.
\]

This is an internal endpoint-saturation theorem.  It is not a universal
\(D^{1/3}\) estimate for all triangular or three-dimensional solutions.

## 2. Analytic proof review

The proof was reviewed independently against the R0.71W lattice generator,
uniform implicit-function theorem, Parseval convention, atom normalization,
and full-frequency rotational-charge definition.

The review found no fatal scaling or normalization error.  It required the
following repairs before release:

1. state and prove the exponential-polynomial zero bound with multiplicities;
2. use the exhausted zero budget to prove that all displayed limiting roots
   are simple and that the tail limit is nonzero;
3. quantify the compact \(C^1\) separation by positive constants
   \(\eta_0,\eta_1\);
4. add a uniform half-line Duhamel estimate without a
   \(\lambda_q^{-1}\) loss;
5. evaluate the limiting half-line integral explicitly;
6. order the choices of \(X,\delta_*,q_0\) so the compact and tail errors are
   controlled simultaneously; and
7. close the complete atom sum and the exact definition of \(\Lambda_1\).

All seven repairs are incorporated in `r071x_report-source.md`.  The repaired
text received a final independent PASS decision.

## 3. Exact normalized identities

The independent review verified the full initial-data Parseval identity

\[
 D_{q,\delta}=\mathscr A^2q^2\mathcal D_{q,\delta}
\]

including active, shear, and persistent-background terms.  At a prescribed
root it also verified

\[
 \partial_ta_{q,\delta}=\mathscr A^2\Theta_{m,q,\delta}
\]

and the fixed-shell atom

\[
 J_{*,m,q,\delta}
 =\frac{2|m_*(k_*)|^2}{\kappa_*^2}
 \frac{\mathscr A^4|\Theta_{m,q,\delta}|^2}
 {Y_{q,\delta}(t_{m,q})}.
\]

Therefore

\[
 \frac{J_{*,m,q,\delta}}{D_{q,\delta}^{1/3}}
 =
 \frac{2|m_*(k_*)|^2\kappa_*^{-2}|\Theta_{m,q,\delta}|^2}
 {\mathcal Y_{m,q,\delta}\mathcal D_{q,\delta}^{1/3}}
 \delta^{4/3}.
\]

No power of \(q\), target-shell radius, or conjugate-pair factor is missing.

## 4. High-precision producer

`r071x_exact_audit.py` uses Python standard-library `Decimal` arithmetic at
90 digits.  It does not solve the nonlinear continuum problem; it audits the
limiting response interpolation and the exact endpoint power ledger.

The run passes 9 of 9 checks.  Principal values are:

- limiting response coefficients
  \((1,-3.6659628490723686768,3.6141327653475095850)\);
- limiting root slopes
  \((-0.1816062642085717146,0.1624527936503469698)\);
- nonzero tail limit \(0.1894842167940399333\);
- fitted \(D\) power \(6.0000267\);
- fitted complete prescribed-atom power \(2.0000031\);
- fitted rotational-charge power \(-2.21\times10^{-7}\);
- fitted endpoint ratio power \(-5.82\times10^{-6}\); and
- fitted \(\delta\)-collapse power exactly \(4/3\) at reported precision.

The \(D^\beta\) sweep agrees with \(2-6\beta\): divergence below
\(\beta=1/3\), saturation at \(1/3\), and decay above \(1/3\).

## 5. Independent binary64 reconstruction

`r071x_independent_audit.py` imports neither the producer nor its JSON output.
It rebuilds the response matrix, coefficients, roots, normalized identities,
and power fits independently using standard-library binary64 arithmetic.

The run passes 8 of 8 checks.  It obtains

- response determinant \(-6.339838757\times10^{-4}\);
- maximum interpolation residual \(1.388\times10^{-17}\);
- the same limiting coefficients, slopes, and nonzero tail to binary64
  accuracy;
- maximum fitted-power error below \(3.57\times10^{-6}\); and
- endpoint factorization relative error below \(1.5\times10^{-15}\).

The script SHA-256 is
`66f28440487b775c86d8d8a54cc024141545f302b2ec9b535c92bfe0756d7528`.

## 6. Nonlinear retained-coset corroboration

`r071x_truncated_coset_audit.py` solves the finite nonlinear Fourier-coset
system with SciPy DOP853, exact finite root equations, Simpson quadrature for
the retained full-coset \(\dot H^{-1}\) charge, and truncation radii
\(R=15,30,40,60\).  The fixed numerical diagnostic uses
\(\delta=1/128\) and \(q=256,512,1024,2048,4096\).

The final producer and independent rerun are byte-for-byte identical and pass
10 of 10 checks.  Principal diagnostics are:

- maximum dimensionless root residual \(1.56\times10^{-18}\);
- maximum restored physical residual \(2.71\times10^{-14}\);
- minimum normalized root slope \(0.162368\);
- complete two-root `atomProxy` power \(1.9999067\);
- exact initial-data power \(6.0002778\);
- `atomProxySum / D^(1/3)` power
  \(-1.86\times10^{-4}\);
- retained full-coset charge power \(-4.97\times10^{-4}\);
- maximum \(\delta^{4/3}\) identity error \(2.80\times10^{-16}\);
- maximum truncation-observable difference \(3.23\times10^{-12}\); and
- analytic charge-tail ratio \(1.60\times10^{-29}\).

A 12,001-point scan on the scaled interval \([0.05,30]\) finds only the two
prescribed real roots, with minimum off-neighborhood real separation
\(2.14\times10^{-5}\).  The integrating-factor tail proxy at cutoffs 30 and
60 has the same nonzero sign and relative drift
\(5.96\times10^{-13}\).  This is numerical corroboration; the analytic
half-line lemma, not the scan, proves zero completeness.

The imaginary response block has condition number about \(295.87\) and
inverse norm about \(7262.78\).  Its large fixed inverse constant explains
the observed \(O(1)\) values of two correction coefficients.  It does not
validate \(\delta=1/128\) as lying inside a quantified continuum IFT radius.

Final SHA-256 values are:

```text
script  1ee532fdccc2bfe9f6d575bae4634ec889a27a4edc47e1a407a23ece217f476b
JSON    8e095535769effcf78ef86a580e9907e809f76237e3606de1bf938e0d5a24833
```

## 7. Multiblock route review

The separate route audit found no exponent-algebra error in the
comparable-band selected-root bound.  It required two claim reductions:

1. launch \(D\) and root-time \(Y\) are not generally interchangeable; the
   proposition uses two explicit lower bounds under a comparable-band launch
   hypothesis; and
2. the energy proxy
   \(\varepsilon_N=P\sqrt{K_{v,N}}/q^2\) is not the exact IFT parameter
   \(\delta_{\mathrm{op},N}=(P/q^2)\sup_x\|V_{z_N}(x)\|\).

The corrected route matrix retains both quantities and labels the
growing-root and strong-coupling constructions as open.  Its final review
decision is PASS.

## 8. Release boundary

The combined audit supports exactly the following conclusion:

> a fixed sufficiently small prefactor at physical amplitude order \(q^2\)
> saturates the \(D^{1/3}\Lambda_1\) scale inside the declared uniform-IFT
> triangular family, and the prescribed real-time target roots are complete.

It does not certify a universal endpoint estimate, a counterexample to such
an estimate, a continuation criterion, singularity formation, or global
regularity for arbitrary three-dimensional Navier--Stokes solutions.  The
literature audit is bounded and makes no novelty or priority claim.
