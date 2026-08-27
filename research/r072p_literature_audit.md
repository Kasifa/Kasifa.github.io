# R0.72P primary-literature audit

**Date:** 2026-08-27

**Verdict:** the declared fixed 1:2 two-carrier class can use a uniform
corollary extracted from Coble--He Theorem 1.2 and its Appendix A proof.
There is no identified black-box theorem for arbitrary common-band Fourier
superpositions.

## 1. Coble--He time-dependent nondegenerate shear theorem

Primary source: D. Coble and S. He, arXiv:2309.15738v2, Theorem 1.2,
published in *Communications in Mathematical Sciences* 22 (2024),
[DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10).

The theorem requires the full time-dependent shear and a reference shear to
share one fixed finite set of nondegenerate critical points, have the same
derivative sign, obey fixed local quadratic and exterior derivative bounds,
and satisfy \(\|\partial_{ty}U\|_\infty\le\nu^{3/4}\).  Its decay rate is
\(e^{-c\nu^{1/2}|k|^{1/2}t}\).  The constants do not follow from Fourier
support or carrier count.

The statement writes the viscosity threshold as \(\nu_0(U,V)\).  For the
R0.72P family, uniformity is obtained by inspecting the proof rather than by
silently replacing this notation with a family-uniform threshold.  The
critical points are fixed at \(0,\pi\); one fixed pair of cutoffs works for
the entire family.  Appendix A, especially the absorption after its spectral
inequality, then depends only on the explicit shape constants and fixed
cutoff derivatives.  The hypocoercive parameters in Section 3 depend on the
same spectral constant, \(C_*\), and a uniform second-derivative norm.  This
supports the parameter-uniform corollary stated in R0.72P.

**Scope:** yes for the exact fixed-pattern class after cell normalization;
no for arbitrary common-band phases or growing carrier count.

## 2. Bedrossian--Coti Zelati stationary theorem

Primary source: J. Bedrossian and M. Coti Zelati, *Archive for Rational
Mechanics and Analysis* 224 (2017),
[DOI](https://doi.org/10.1007/s00205-017-1099-y).

The theorem treats fixed stationary shear profiles.  Its proof makes the
dependence on critical-point separation, local degeneracy coefficients and
cutoffs explicit.  It supplies the spectral/hypocoercive method used in the
time-dependent result, but does not permit carrierwise tensorization of a
changing full shear.

## 3. Coti Zelati--Gallay degeneracy-dependent rates

Primary source: M. Coti Zelati and T. Gallay, *Journal of the London
Mathematical Society* 108 (2023), Theorem 1.1,
[DOI](https://doi.org/10.1112/jlms.12782).

For stationary parallel shears, the enhanced-dissipation exponent changes
with the order of profile degeneracy.  This confirms that a Morse margin is
part of the mathematical data.  It does not prove a time-dependent
full-superposition estimate.

## 4. Nearby time-dependent special profiles

Benthaus and Nobili study the separable class
\(v(t,y)=\xi(t)v(y)\), with one fixed spatial profile and scalar time
modulation; see arXiv:2501.16905v2 and
[DOI](https://doi.org/10.3934/eect.2025051).  That factorization does not
cover \(e^{-t}\cos y+\lambda e^{-4t}\cos2y\), whose relative coefficient
changes with time.

Benthaus, Coclite and Nobili study the rigidly translating profile
\(\sin(y-ct)\) and construct a dedicated non-autonomous functional; see
[arXiv:2603.14624v1](https://arxiv.org/html/2603.14624).  The profile's
critical points translate instead of undergoing the heat-weighted shape
change in R0.72P.  Their result reinforces the need to audit moving critical
geometry, but it is not a replacement theorem for finite Fourier sums.

Coti Zelati, Delgadino and Elgindi give a general bridge from a uniform
inviscid mixing estimate to enhanced dissipation; see
[arXiv:1806.03258](https://arxiv.org/abs/1806.03258).  In the present problem,
the required uniform mixing input is itself the missing full-superposition
gate, so the bridge does not remove the shape proof.

These nearby directions therefore do not cover a general sum whose Fourier
components decay at different rates.

## 5. Search decision

The search stopped after the closest time-dependent theorem, its stationary
predecessor, the degeneracy-dependent stationary theorem, and two recent
special-profile directions agreed on the same boundary.  Another broad
search was unlikely to change the decisive conclusion:

\[
 \text{common-band support alone: no};\qquad
 \text{fixed finite pattern + complete uniform shape package: yes}.
\]

This is a bounded literature assessment and not a priority or novelty claim.
