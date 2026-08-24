# R0.70E independent audit record

**Date:** 2026-08-24
**Mode:** three independent read-only reviews followed by a final re-review
**Result:** PASS; no remaining must-fix item

## 1. Primary-source audit — PASS

The reviewer checked Yu v1 Sections 2, 6, 7, and 8 against
`r070e_report-source.md`.

Confirmed boundaries:

- Yu requires neither an even/radial mollifier nor an even cutoff; R0.70E
  clearly labels both as project selections within the admissible classes.
- Yu defines the signed remainder work (6.9), its positive part (6.13), and
  moving-shell strain tensors, but no scalar
  \(F_{j,k}^{\mathrm{Yu}}\).
- The project moving-shell contraction is not identified with
  \(\mu_k^{\mathrm{far,ann}}\) or Proposition 8.6.
- The intermediate region between the near transition and the Section 8
  outer shells is retained as a source boundary.

Corrections made during review included the report-local label `(2.7R)`, the
precise near-transition description, the ranges
\(0<\rho\le1/4\), \(0\le\chi\le1\), and weaker wording around magnitude-based
annular estimates.

## 2. Algebra and kernel audit — PASS

The reviewer independently checked reflection covariance, the periodic
Fourier pair and its vector potentials, all four stretching coefficients,
the hard-shell multiplier, and the reflection cubic.

One substantive sign error was found and corrected before the final review:
the raw \(K_{132}\) multiplier begins with
\(-q^2(b^2-a^2)/20\), while the full
\(S_{13}/\Omega_2\) multiplier is \(-1/2\).  Hence the relative shell
multiplier is

\[
\alpha_{a,b}(q)
=\frac{q^2(b^2-a^2)}{10}
-\frac{q^4(b^4-a^4)}{280}+O(q^6b^6),
\]

with positive leading sign.  The final symbolic certificate verifies the
Bessel antiderivative, both displayed coefficients, the anti-palindromic
four-coefficient pattern, and \(H'(1)=-A_1/2\).

The re-review also confirmed the pure degree-two tensor-harmonic reason for a
common monochromatic multiplier, the factor
\(q^3c_\varphi^3\alpha\), the two-lobe strict-sign cutoff, and the final
\(k,m,j\) quantifiers.

## 3. PDE localization and IFT audit — PASS

The reviewer checked compact vector-potential localization, return fields,
the full \(r_k^2\) heat interval, absolute activity, and the normalized
small-data solution map.

A substantive return-field ambiguity was found and corrected before final
review:

- the hard moving shell excludes the cutoff transition at \(t=0\) because it
  has a finite dependency region;
- the exact remainder does **not** discard the global return field.  It uses
  \(S_\ell^{\mathrm{rem}}=S(\varphi_\ell*u)-S_\ell^{\mathrm{near}}\), so
  plateau equality fixes the local full gradient and finite near term while
  the global Biot--Savart cancellation remains intact.

The final report now includes the distance \(d_L\), a Gaussian derivative
tail estimate, the absolute-value Lipschitz transfer, and the fixed-interval
space

\[
X_T=C([0,T];H^s)\cap L^2(0,T;H^{s+1}),\qquad s>7/2.
\]

The re-review found no remaining gap in the normalized Kato map or the
implicit-function tuning.

## 4. Scope retained

The audits do not convert the result into a regularity theorem.  They confirm
only the two precisely stated existence results:

1. an exact sign defect for Yu's paper-defined remainder work;
2. an exact sign defect for one project-defined signed contraction of a Yu
   moving-shell strain tensor.

No audit identifies the project scalar with Yu's positive annular quantity,
controls all shells, closes the Carleson, commutator, or localization budgets,
or addresses large-data singular behavior.
