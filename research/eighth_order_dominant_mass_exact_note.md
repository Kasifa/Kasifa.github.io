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

## 5. Formal result

The monitored 192-bisection run passed all nine declared checks. It obtained

\[
 \operatorname{width}(\mu)<4.079\times10^{-69},
 \qquad
 \max_s\operatorname{width}(m_s)
 <2.177\times10^{-69}.
\]

The observable coordinate is enclosed strictly on the negative side around

\[
 m_{\mathrm{obs}}
 =-2.612679363056960676322043975806304261290148\times10^{-2}.
\]

The canonical interval-vector SHA-256 is
bf424dfb3c9ce85d1e47d2270b329f6cb4af51e32e665663949d6c53cf6f0e53.
The formal run took 7.01 seconds and the monitor sampled a peak RSS of
177.688 MiB.

## 6. Scope

This step removes power-iteration uncertainty from the dominant mass vector.
It does not yet enclose the triangular degree-ten moment lift, the heat
pairing, or the signature-compressed defect. The calculation remains confined
to one fixed parallel-shear packet and does not prove the Navier--Stokes
Millennium statement.
