# R0.71L gap matrix — fixed-cell fusion, paid denominator mass, and the remaining tangent product

## 0. Audit status

This is a narrow algebra and estimate-boundary audit. It is not a regularity
theorem and it does not assert that every possible Leray-level estimate for the
remaining tangent product is impossible.

The exact producer is `research/r071l_exact_audit.py`. It imports no prior
audit module and checks all displayed finite algebra with exact SymPy
arithmetic.

## 1. Canonical fixed-cell notation

For one fixed spatial cutoff, put

\[
 \mathsf A_QV:=\nabla\times(\chi_QV),
 \qquad C_Q=\mathsf A_QW,
 \qquad r_Q=\|C_Q\|_2,
 \qquad E_Q=C_Q/r_Q,
\]

\[
 P_Qv=v-\langle v,E_Q\rangle E_Q,
 \qquad x=F/\sqrt Y,
 \qquad \lambda=\nu\kappa^2.
\]

Here \(E_Q\otimes E_Q\) is the rank-one orthogonal projector onto
\(\operatorname{span}\{E_Q\}\), while \(P_Q\) is the complementary corank-one
orthogonal projector onto \(E_Q^\perp\) in the real \(L^2\) Hilbert space,
not a pointwise matrix field. The symbol \(r_Q\) is used to
avoid confusing the denominator norm with the fixed partition-radius constant
called \(\rho\) in R0.71K.

The starting identities are the complete ledgers in
`research/r071h_report-source.md:165-239`,
`research/r071i_report-source.md:219-228`, and
`research/r071k_report-source.md:419-491`.

## 2. Exact fixed-cutoff fusion

Let

\[
 \mathcal G_j=\sum_{k,\ell}\mathfrak G_{k\ell,j},
 \qquad
 W_t=\nu\Delta W+\mathcal G_j.
\]

Because \(\chi_Q\) is fixed in time,

\[
 \boxed{
 M_Q:=C_{Q,t}+\nu\kappa^2C_Q
 =\mathsf A_Q\!\left[
 \nu(\Delta+\kappa^2)W+\mathcal G_j
 \right].}
 \tag{2.1}
\]

Equivalently,

\[
 \begin{aligned}
 &\nu(\Delta+\kappa^2)C_Q
 -\nu\nabla\times\left(
 2\nabla\chi_Q\cdot\nabla W+(\Delta\chi_Q)W
 \right)\\
 &\qquad=\nu\nabla\times\left(
 \chi_Q(\Delta+\kappa^2)W\right).
 \end{aligned}
 \tag{2.2}
\]

Thus the separately displayed viscous collar is the commutator part of a
single fixed-localization operator. Equation (2.2) gives neither a sign nor a
new positive defect. Taking the collar's absolute value before applying
(2.2) loses an exact cancellation.

## 3. Normalization and projective fusion

Set

\[
 N=F_t+\lambda F,
 \qquad y=Y_t/Y,
 \qquad z_Q=\langle x,E_Q\rangle.
\]

Then

\[
 \boxed{
 \frac N{\sqrt Y}-\frac y2x=x_t+\lambda x,}
 \tag{3.1}
\]

and, on \(r_Q>0\),

\[
 \boxed{
 E_{Q,t}=\frac{P_QM_Q}{r_Q}.}
 \tag{3.2}
\]

Consequently the complete signed source is

\[
 \boxed{
 \mathcal J_Q
 =\langle x_t+\lambda x,E_Q\rangle
 +\langle P_Qx,E_{Q,t}\rangle.}
 \tag{3.3}
\]

Equations (2.1) and (3.3) are the canonical R0.71L ledger. They retain the
field acceleration, nonlinear vorticity source, dynamic cutoff--curl part,
projective tangent, and normalization without taking their positive parts
separately. The finite-dimensional exact check also verifies

\[
 z_{Q,t}+\lambda z_Q=\mathcal J_Q,
 \qquad
 a_{Q,t}+2\lambda a_Q=2z_Q^+\mathcal J_Q
\]

on a declared positive branch.

## 4. Helmholtz and aligned cutoff--curl cancellations

### 4.1 Fourier Helmholtz example

For one nonzero Fourier frequency \(k\), let

\[
 P_k=I-\frac{k\otimes k}{|k|^2}.
\]

The producer uses exact rational vectors and verifies

\[
 k\cdot P_kV=0,
 \qquad
 k\times(I-P_k)V=0,
 \qquad
 k\times V=k\times P_kV.
 \tag{4.1}
\]

This is the exact global Helmholtz cancellation used when curl removes a
gradient Lamb component. A nonconstant cutoff can reintroduce the boundary
term \(\nabla\chi\times(I-P_k)V\); equation (4.1) is not a claim that every
localized gradient contribution vanishes.

### 4.2 Static aligned numerator

Split

\[
 C_Q=\chi_Q\nabla\times W+\nabla\chi_Q\times W,
\]

and define

\[
 B_Q^\partial
 =\langle F,\nabla\chi_Q\times W\rangle.
\]

For the R0.71K selected witness, \(F\) and \(W\) are invariant under all cell
translations and the cells are translates. Hence all \(B_Q^\partial\) are
equal. Since

\[
 \sum_QB_Q^\partial
 =\left\langle F,
 \left(\sum_Q\nabla\chi_Q\right)\times W\right\rangle=0,
\]

one has

\[
 \boxed{B_Q^\partial=0\quad\text{for every selected aligned cell}.}
 \tag{4.2}
\]

The producer checks both the equal-cell logic and a smooth two-cell periodic
example. Equation (4.2) removes only the static cutoff--curl numerator. The
same cutoff derivative remains in \(d_Q\) and in the dynamic projective row.
The translation and partition facts used here are recorded in
`research/r071k_report-source.md:251-334`.

## 5. Two-sided denominator bound

Let

\[
 D_{\rm loc}=\sum_Q\|C_Q\|_2^2,
 \qquad
 D_\kappa=\left\|\sum_QC_Q\right\|_2^2.
\]

At most \(N\) cells overlap at any point, so pointwise Cauchy gives

\[
 D_\kappa\le N D_{\rm loc}.
 \tag{5.1}
\]

Together with the R0.71K partition estimate,

\[
 D_{\rm loc}\le C_{\rm part}D_\kappa,
\]

this yields

\[
 \boxed{
 \frac1N D_\kappa
 \le D_{\rm loc}
 \le C_{\rm part}D_\kappa.}
 \tag{5.2}
\]

For \(K^3\) equal cells and \(D_\kappa\asymp K^4\),

\[
 \boxed{d_Q\asymp K.}
 \tag{5.3}
\]

The lower comparison in (5.2) supplies the quantitative denominator bound
needed when the scale ledger divides by \(r_Q=\sqrt{d_Q}\). Strict positivity
alone, proved in `research/r071k_report-source.md:377-382`, is insufficient
for that division. The witness-specific \(D_\kappa\asymp K^4\) uses fixed
\(\nu>0\), the fixed parabolic window, and the uniform positive limiting
profile in `research/r071j_report-source.md:657-701`.

The resulting selected-cell exponents are

| quantity | \(K\)-exponent per cell |
|---|---:|
| \(B_Q\) | \(0\) |
| \(d_Q\) | \(1\) |
| \(q_Q\) | \(-1\) |
| \(a_Q=q_Q/Y\) | \(-3\) |
| \(z_Q\) | \(-3/2\) |
| weighted, time-integrated creation | \(-5\) |

After the \(K^3\)-cell sum, the last row has exponent \(-2\).

## 6. What the standard Leray budget pays

Annular Bernstein and (5.2)'s upper half give

\[
 D_{{\rm loc},j}
 \lesssim \kappa_j^2\|W_j\|_2^2.
\]

Therefore the frame square bound and the standard energy inequality imply

\[
 \boxed{
 \nu\int_I\sum_j\kappa_j^{-2}D_{{\rm loc},j}\,dt
 \lesssim
 \nu\int_IY(t)\,dt
 \lesssim\|u_0\|_2^2.}
 \tag{6.1}
\]

Thus the weighted positive denominator mass, including interior,
cutoff--curl square, and cross contributions through the complete \(d_Q\), is
Leray-paid.

This fact does not pay an inverse denominator. For the projective tangent

\[
 T_Q=\langle P_Qx,E_{Q,t}\rangle,
 \qquad E_{Q,t}=P_QM_Q/r_Q,
\]

choose a support neighborhood
\(U_Q\supset\operatorname{supp}\chi_Q\). Cauchy and Young then give the
exact proof obligation

\[
 \begin{aligned}
 2\kappa^{-2}\sqrt{a_Q}|T_Q|
 &\le \nu a_Q\\
 &\quad+\frac1{\nu\kappa^4}
 \frac{\|1_{U_Q}P_QF\|_2^2}{Y}
 \frac{\|P_QM_Q\|_2^2}{d_Q}.
 \end{aligned}
 \tag{6.2}
\]

The second line is the product of a local normalized Lamb amplitude and the
projective angular-rate square. Equation (6.1) controls neither factor nor
their product merely by controlling \(d_Q\). Replacing the second factor by
\(\|E_{Q,t}\|_2^2\) only renames the same angular quantity.

If normalization is separated before taking the positive part, its exact
cost is

\[
 \frac12a_Q\left(\frac{Y_t}{Y}\right)^-.
 \tag{6.3}
\]

The standard Leray energy inequality controls \(\int Y\), not the weighted
negative variation of \(\log Y\). Equations (6.2)--(6.3) identify missing
estimates; they are not nonexistence theorems.

## 7. Row-by-row decision matrix

| Row | Exact status | Fixed-\(\nu\) witness scale | Leray boundary |
|---|---|---:|---|
| fixed cutoff motion | zero | \(0\) | closed only for fixed cells |
| static cutoff--curl numerator | zero by aligned translations | \(0\) exactly | not a statement for misaligned partitions |
| denominator interior/collar/cross | retained in \(d_Q\) | \(O(K)\) per cell | weighted positive mass paid by (6.1); inverse not paid |
| expanded viscous collar | fuses exactly with \(\nu\Delta C_Q\) | \(O(\nu K^{5/2})\) in one-cell \(L^2\) | no separate sign or coercive defect |
| recombined viscous mismatch | \(\nu\mathsf A_Q(\Delta+\kappa^2)W\) | same leading scale | broad annulus gives no small mismatch |
| nonlinear localized-vorticity row | retained in \(\mathsf A_Q\mathcal G_j\) | lower order only after fixed-\(\nu\), large-\(K\) limit | not controlled in the quotient by energy alone |
| projective tangent | retained jointly | \(O(\nu K^{1/2})\) in \(\mathcal J_Q\) | leaves product (6.2) |
| normalization | fuses with \(N/\sqrt Y\) | \(O(\nu K^{1/2})\) in \(\mathcal J_Q\) | separate estimate leaves (6.3) |
| denominator faces/refresh | absent on selected fixed witness | \(0\) | still open in a general hard/soft passage |

The \(O(\nu K^{1/2})\) statements use the quantifier order “fixed
\(\nu>0\), then sufficiently large dyadic \(K\)”. The convergence constants
are allowed to depend on \(\nu\), as stated in
`research/r071j_independent_audit.md:261-299`.

## 8. Exact theorem/no-go boundary

The finite result supported by this audit is:

> **Fixed-cell fusion proposition.** On a classical interval with a fixed
> smooth cutoff and \(d_Q>0\), equations (2.1)--(3.3) hold exactly. For the
> selected aligned R0.71K witness, equation (4.2) and the two-sided denominator
> comparison (5.2) also hold. The standard Leray energy inequality pays the
> positive weighted denominator mass (6.1).

The corresponding narrow no-free-gain statement is:

\[
 \boxed{
 \text{Taking the expanded viscous collar as an independent positive row}
 \text{ is not an exact coercive mechanism.}}
\]

It is a commutator component of (2.1), and taking its absolute value before
fusion discards an exact cancellation. A direct rowwise Cauchy--Young proof
still leaves (6.2) and, if normalization is split, (6.3).

This audit does **not** prove that no different Leray-level NSE estimate,
signed nonlinear cancellation, critical-space hypothesis, or continuation
argument can control those quantities. It proves no unconditional weighted
BV theorem, continuation criterion, global regularity result, singularity,
originality, or Millennium-problem result.

## 9. Reproduction and certificate boundary

Run

```bash
tmp/r068b-venv/bin/python research/r071l_exact_audit.py
```

The producer emits one JSON object. Its six top-level checks are:

1. fixed-cutoff viscous fusion;
2. finite-dimensional normalization/projective identities;
3. exact Fourier Helmholtz cancellation;
4. aligned cutoff--curl numerator cancellation;
5. denominator two-sided bounds and scale exponents;
6. Leray-paid denominator mass and the explicit unpaid tangent product.

The R0.71K producer declared the collar exponent but did not evaluate
\(N,M,E_t,\mathcal J\) row by row
(`research/r071k_exact_audit.py:102-124,184-188`), while its independent
quadrature evaluated \(B,d,Y\) rather than those time-source rows
(`research/r071k_independent_audit.py:232-370`). The present producer closes
the finite algebra gap only; a witness-specific independent time-row
reconstruction would be a separate numerical certificate.
