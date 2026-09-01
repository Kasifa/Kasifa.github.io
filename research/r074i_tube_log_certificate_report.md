# R0.74I tube/log finite exponent certificate report

## Result

The exact-arithmetic producer returns **PASS: 36/36**.

This is a finite certificate over rational numbers.  It checks only the
scaling exponents and fixed rational factors used by the moving-tube threshold
and logarithmic-obstruction calculations.  It does not certify a partial
differential equation argument.

## 1. Parabolic (L^3) normalization

For

\[
 U(s,\xi)=r\,u(t_0+r^2s,x_0+r\xi),
\]

the velocity cube contributes (r^3), while the inverse space and time
Jacobians contribute (r^{-3}) and (r^{-2}).  The certificate reconstructs

\[
 3-3-2=-2.
\]

Equivalently, writing the physical integral in terms of (U) gives

\[
 -3+3+2=2,
 \qquad
 -2+2=0.
\]

Thus the exponent identity is exactly

\[
 \int_{Q_1}|U|^3\,d\xi\,ds
 =r^{-2}\int_{Q_r(z_0)}|u|^3\,dx\,dt.
\]

At (r=R/2), the time length and normalization have the exact factors

\[
 (1/2)^2=\frac14,
 \qquad
 (1/2)^{-2}=4.
\]

Their product is one.  This fixed-factor check does not compare the spatial
domains or prove the interpolation estimate.

## 2. Energy and small-payment threshold exponents

The algebra behind

\[
 \mathcal E_R^{3/2}\le P_R
 \quad\Longrightarrow\quad
 \mathcal E_R\le P_R^{2/3}
\]

uses

\[
 \frac32\cdot\frac23=1.
\]

The same identity checks the threshold choice

\[
 P_R\le\varepsilon_{\rm tube}^{3/2}
 \quad\Longrightarrow\quad
 P_R^{2/3}\le\varepsilon_{\rm tube}
\]

at the exponent level.  If the tube threshold itself contains an
((\varepsilon_{L^3}/C_I)^{2/3}) term, raising it to (3/2) returns a
linear power of \(\varepsilon_{L^3}/C_I\).  The certificate checks this
composition; it does not establish either analytic inequality or any
admissible numerical epsilon constant.

## 3. Logarithmic window and lacunarity

With the frozen value

\[
 \rho=\frac1{320},
\]

the exact endpoint coefficients are

\[
 2\rho=\frac1{160},
 \qquad
 3\rho=\frac3{320},
 \qquad
 3\rho-2\rho=\frac1{320}.
\]

The sequence has

\[
 L_j=\frac{63}{32}2^j,
 \qquad
 L_{j+1}=2L_j,
 \qquad
 L_{j+1}^2=4L_j^2.
\]

Therefore the next-index lower logarithmic exponent is

\[
 2\rho L_{j+1}^2=8\rho L_j^2,
\]

and subtracting the current-index upper exponent gives

\[
 8\rho-3\rho=5\rho=\frac1{64}.
\]

This verifies the finite exponent in the lacunarity calculation.  The packet
bounds needed to turn it into a statement about (P_{j+1}/P_j) remain
analytic inputs.

## 4. Square-root logarithmic frontier

The frozen payment upper scale has the monomial (B^3R^3).  The certificate
checks

\[
 (B^3R^3)^{2/3}=B^2R^2.
\]

A logarithmic window proportional to (L^2) contributes one (L) after a
square root because

\[
 2\cdot\frac12=1.
\]

Consequently the finite exponent vector of
(P^{2/3}\sqrt{\log P}) matches (B^2LR^2).  The coefficient
(sqrt{3\rho+\delta}), the upper bound for (P_j), and the lower bound for
the target are not certified here.

For a subcritical exponent, write

\[
 \gamma=\frac12-\delta.
\]

The certificate separately reconstructs the constant and (delta)
coefficients in

\[
 \frac12-\gamma
 =\frac12-\left(\frac12-\delta\right)
 =\delta.
\]

At the endpoint (gamma=1/2), the gap is exactly zero.  The finite
coefficient identity does not prove divergence for every (gamma<1/2);
that conclusion also uses the analytic fact (P_j\to\infty).

## 5. Conditional endpoint algebra

Suppose an analytic argument supplied the hypothetical endpoint inequality
used in R0.74I.  After comparing it with the target lower bound, its monomial
form is

\[
 B^2LR^2\lesssim K L P^{2/3}.
\]

The certificate checks that the (L) powers cancel and that inversion of
(2/3) uses (3/2).  The resulting powers are

\[
 P\gtrsim K^{-3/2}B^3R^3.
\]

In particular,

\[
 2\cdot\frac32=3,
 \qquad
 -1\cdot\frac32=-\frac32,
 \qquad
 \frac23\cdot\frac32=1.
\]

This is a conditional exponent implication.  It is not a lower bound proved
for the frozen packet family.

The rational comparisons

\[
 \frac1{256}<\frac1{128}<\frac1{64}
\]

also pass exactly.  The claim that these bounds eventually contain (b_j)
depends on the separate analytic limit (b_j\to1/128).

## 6. Scope boundary

The certificate does **not** prove or verify:

1. the local energy inequality or the moving-test limit;
2. existence, uniqueness, confinement, or estimates for the mollified path;
3. the fixed-cylinder interpolation inequality;
4. the velocity-only epsilon-regularity theorem;
5. the R0.74F--H packet construction or any packet upper or lower bound;
6. the literature boundary, novelty, or priority;
7. local regularity, exclusion of singularities, continuation, or global
   smoothness; or
8. the Clay Millennium problem.

The certificate is not evidence for any item in this list.  **NOT CLAY.**

## 7. Reproduction

From the repository root, run

```text
python3 scripts/r074i_tube_log_certificate.py
```

The standard output must be byte-for-byte identical to
`research/r074i_tube_log_certificate.json`.
