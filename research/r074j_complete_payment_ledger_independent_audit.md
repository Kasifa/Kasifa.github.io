# R0.74J independent complete-payment ledger audit

**Verdict:** `INDEPENDENT_COMPLETE_PAYMENT_LEDGER_AUDIT_PASS`
**Source-rebind verdict:** `R074J_LEDGER_SOURCE_REBIND_PASS`
**Bound analytic source:** `research/r074j_matching_payment_law.md`
**Bound analytic source SHA-256:**
`d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad`

This is a byte-exact source binding.  The verdict does not transfer to a
later byte sequence without a new source rebind.

## 1. Independent geometric and row reconstruction

At payment radius \(2R\), the source definitions give

\[
 I_{2R}=(61R^2,65R^2),
 \qquad |I_{2R}|=4R^2,
\]

and

\[
 A_5(2R)=\{64R\le |x|<128R\},
 \qquad
 \Gamma_5=e^{-4^4/32}=e^{-8}.
\]

For

\[
 Q_R=\{|x_1|<R,\ |x_2|<R,\ 80R<x_3<96R\},
\]

the lower radial inequality is \(|x|>80R>64R\), while the upper one is

\[
 |x|^2<(96^2+1+1)R^2=9218R^2<128^2R^2.
\]

Hence \(Q_R\subset A_5(2R)\).  Its three side lengths are
\(2R,2R,16R\), so

\[
 |Q_R|=64R^3.
\]

The shear-platform lemma supplies \(\theta_j\ge1/2\) throughout
\(I_{2R}\times Q_R\) for all sufficiently large \(j\).  The canonical
asymptotic scalar is

\[
 \boxed{\beta_j:=B_jR_j^2\longrightarrow\frac1{128}}.
\]

It follows that \(B_j>0\) eventually.  The inherited lower-case shear-field
symbol remains reserved and is not repurposed for this scalar; doing so would
create a symbol collision.  Orthogonality of the two velocity components gives

\[
 |u_j|^3
 =\bigl(\mathfrak a_j^2F_j^2+B_j^2\theta_j^2\bigr)^{3/2}
 \ge B_j^3|\theta_j|^3.
\]

The normalization, time length, box volume, and shear floor therefore produce
the exact coefficient

\[
 (2R)^{-2}(4R^2)(64R^3)\left(\frac12\right)^3
 =8R^3.
\]

Since \(\mathcal G_u\) is a nonnegative row of the complete payment, the full
lower-bound chain is

\[
 \boxed{
 P_j:=P_{R_j}^M=P_{R_j}^F
 \ge \mathcal G_u(z_{0,j},2R_j;1)
 \ge 8e^{-8}B_j^3R_j^3.}
\]

The common-quantity identity uses the exact symmetry cancellation
\(X_{R_j}=a_{R_j}=a'_{R_j}=0\).  The inherited R0.74G Theorem 1.1 supplies,
for the same family and amplitude,

\[
 P_j\le CB_j^3R_j^3.
\]

Thus the independently reconstructed ledger is

\[
 8e^{-8}B_j^3R_j^3
 \le P_j=P_{R_j}^M=P_{R_j}^F
 \le CB_j^3R_j^3.
\]

## 2. Independent asymptotic reconstruction

From \(\beta_j=B_jR_j^2\to1/128\) and
\(R_j=e^{-\rho L_j^2}\), with \(\rho=1/320\),

\[
 B_j^3R_j^3
 =\beta_j^3R_j^{-3}
 =\beta_j^3e^{3\rho L_j^2}.
\]

The two-sided ledger therefore gives

\[
 \log P_j=3\rho L_j^2+O(1),
 \qquad
 \boxed{\frac{\log P_j}{L_j^2}\longrightarrow\frac3{320}}.
\]

Because \(L_{j+1}=2L_j\), subtraction at consecutive indices gives

\[
 \boxed{
 \log\frac{P_{j+1}}{P_j}
 =3\rho(4-1)L_j^2+O(1)
 =\frac9{320}L_j^2+O(1).}
\]

This confirms both the payment rate \(3/320\) and the lacunarity rate
\(9/320\).

## 3. Endpoint meaning and open upper analyses

The same ledger first gives

\[
 \frac{P_j}{B_j^2L_jR_j^2}
 \asymp\frac{B_jR_j}{L_j}
 =\frac{\beta_j}{L_jR_j}\longrightarrow\infty.
\]

It also implies \(P_j>1\) eventually.  Thus on the asymptotic tail
\(\log_+P_j=\log P_j\), and

\[
 \boxed{
 P_j^{2/3}\sqrt{1+\log_+P_j}
 \asymp B_j^2L_jR_j^2.}
\]

This is a scale identity for the endpoint monomial.  Combined with the
inherited lower bounds for \(X_j\) and \(\mathfrak C_j\), it explains why
scale counting does not reject the square-root-log exponent.  It is not an
endpoint upper estimate for either observable.

- `X_j_UPPER_OPEN`: a matching upper bound for \(X_j\) remains **OPEN** and
  requires the separate inward-tail audit identified by the source.
- `MATHFRAK_C_j_UPPER_OPEN`: a matching upper bound for \(\mathfrak C_j\)
  remains **OPEN** and separately requires collar-flux and energy upper
  audits.

The two open upper analyses must not be merged into, or inferred from, the
complete-payment ledger.  No missing premise or mathematical overclaim was
found in the bound source at the SHA-256 recorded above.

**NOT CLAY.**
