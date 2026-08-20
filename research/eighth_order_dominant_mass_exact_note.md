# R0.68B-2e — Exact dominant-mass intervals

## 1. Objective

The degree-ten pilot obtained the dominant mass vector by 220 normalized
power iterations in binary64. That is an excellent numerical initializer, but
it does not itself enclose the exact eigenvector. Here the mass vector is
reconstructed directly from the exact reachable recurrence.

## 2. Finite recurrence and residue

Let \(C\) be the exact 1,792-state four-bit cycle and \(v_0\) the exact
initial vector. The reachable sequence \(C^n v_0\) obeys the known degree-33
integer recurrence after one transient. For every state \(s\), this gives a
rational generating function

\[
 A_s(z)=\frac{N_s(z)}{D(z)}.
\]

If \(\mu\) is the simple dominant root, the coefficient of \(\mu^n\) is the
dominant-pole residue. In the descending-\(\mu\) representation used by the
audit it is

\[
 m_s=-\frac{\widetilde N_s(\mu)}
 {\sum_{j=1}^{33}j c_j\mu^{33-j}}.
\]

The numerator is constructed independently for all 1,792 states from exact
integer vectors \(v_0,\ldots,v_{33}\).

## 3. Root refinement

The upstream rational bracket already isolates the dominant root of the
scaled quartic. Exact bisection retains the polynomial sign at both endpoints
and reduces the bracket width below \(10^{-60}\). Rational interval Horner
evaluation then encloses every numerator and the common residue denominator.

## 4. Acceptance criteria

The strict run must verify:

- the refined quartic signs are opposite;
- the degree-33 vector recurrence residual is exactly zero;
- all 1,792 coordinate intervals are present and ordered;
- every coordinate width is below \(10^{-50}\);
- the observable mass interval is strictly negative.

Binary64 midpoint residuals and the earlier power iteration are retained only
as cross-checks and are not used to establish the intervals.

## 5. Scope

This step removes power-iteration uncertainty from the dominant mass vector.
It does not yet enclose the triangular degree-ten moment lift, the heat
pairing, or the signature-compressed defect. The calculation remains confined
to one fixed parallel-shear packet and does not prove the Navier--Stokes
Millennium statement.
