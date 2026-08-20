# R0.67C-1: an exact first-cycle sign for the complete sixth-order heat observable

## 1. Scope

R0.67B lifted the sixth-order mass and four first moments and proved the
strict separation

\[
 26<256<300<\mu.
\]

The remaining question is whether the complete heat observable pairs
nontrivially with the dominant \(\mu\)-eigenspace.  Before constructing that
asymptotic projection, this note performs a finite but exact diagnostic at the
first stationary four-bit cycle.  The result is a sign certificate at
\(M=16\), not an asymptotic theorem.

## 2. Complete path sum

Put

\[
 M=16,\qquad H=4M=64,\qquad q=2,\qquad Q=H+q=66.
\]

For offsets \(a,b,c,d,e\in\{0,\ldots,M-1\}\), write

\[
 A=H+a,\ B=H+b,\ C=H+c,\ D=H+d,\ E=H+e.
\]

The constraint \(A+B+C-D-E=Q\) is equivalent to

\[
 e=a+b+c-d-q.
\]

There are exactly 34,690 valid quadruples \((a,b,c,d)\), and hence 346,900
signed ordered paths after including all ten \((3,2)\)-shuffle words.  For
each word \(\omega\), define \(p_1,\ldots,p_5\), \(k_j\), and the five
nonzero integer rates

\[
 \beta_j=H^2\alpha_j
 =k_j^2+\sum_{\ell=j+1}^{5}p_\ell^2,
 \qquad 0\le j\le4.
\]

Every enumerated path ends at \(k_5=0\).  The largest rate in the complete
finite enumeration is

\[
 \max\beta_j=67014,
 \qquad
 \max\alpha_j=\frac{67014}{4096}=16.36083984375.
\]

## 3. Exact Taylor representation

For five nonzero rates, the positive five-simplex kernel has the expansion

\[
 K_T^{(5)}
 =\sum_{n=0}^{\infty}
 \frac{(-1)^n h_n(\alpha_0,\ldots,\alpha_4)T^{n+5}}
 {(n+5)!},
 \qquad T=\frac{\log2}{2},
\]

where \(h_n\) is the complete homogeneous polynomial.  The audit sums the
integer quantities \(h_n(\beta_0,\ldots,\beta_4)\) through \(n=32\), including
the Rudin--Shapiro sign of the target and all five carriers.  At \(n=0\),

\[
 J_0=5000=10\times500,
\]

which independently matches the R0.67A zero-time mass for the first cycle.

The time \(T=\operatorname{atanh}(1/3)\) is enclosed by 120 positive rational
terms.  If \(A=\max\alpha_j\), then

\[
 h_n(\alpha_0,\ldots,\alpha_4)
 \le {n+4\choose4}A^n.
\]

This converts all terms after degree 32 into a rational geometric majorant.

## 4. Certified finite-scale conclusion

The exact outward interval is recorded in the JSON certificate.  In decimal
form it is centred at

\[
 S_{6,q}^{(M=16)}\approx0.0516697551563920,
\]

while the absolute omitted-series bound is below

\[
 2\times10^{-12}.
\]

Therefore

\[
 \boxed{S_{6,q}^{(M=16)}>0.}
\]

This is useful because it validates, in one exact computation, the ten time
orders, the endpoint constraint, the heat normalization, the Rudin--Shapiro
signs, and the five-simplex Taylor convention.  It does **not** determine the
sign of the dominant asymptotic coefficient.  The zero-time sequence itself
changes sign only at later cycles, so extrapolating the first-cycle sign would
be mathematically invalid.

## 5. Next step

R0.67C-2 will evaluate the canonical finite-lift contribution

\[
 (Jv)(F_{2/15})
\]

for the dominant finite spectral projector, then compare it with an explicit
resolvent error bound for

\[
 \eta_v=(\mu-\mathcal P|_{\mathcal B_0})^{-1}Rv.
\]

If the canonical term dominates that error, the heat projection sign follows
immediately.  If it does not, successive Neumann corrections will be computed
until the remaining \((256/\mu)^n\) tail is smaller than the observed signal.

No result in this note proves control of all Picard orders, singularity, norm
inflation, or global regularity for the three-dimensional Navier--Stokes
equations.
