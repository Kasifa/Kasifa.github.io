# Figure contract — fig-r070o-rank-bridge

## Question

What exact information is lost when a decaying scalar filter is used to infer
unfiltered critical vorticity control, and how should the normalized
covariance spectrum be stratified before a continuation argument is attempted?

## Claim encoded

For the scalar Bessel filter
\[
m(k)=\frac{1}{1+|k|^2},
\qquad
A(N)=|m(Ne_2)|^2=\frac{1}{(1+N^2)^2},
\]
the exact filtered near-line residual of the periodic shear witness satisfies
\[
\|r_N\|_{L_t^2}=\frac{A(N)}{4\sqrt\nu}.
\]
It therefore tends to zero like \(N^{-4}\), while reconstruction through the
same observation costs
\[
A(N)^{-1}=(1+N^2)^2\sim N^4.
\]
This is a lower-frame obstruction for that observation, not a regularity
theorem.

For ordered covariance eigenvalues
\(\lambda_1\ge\lambda_2\ge\lambda_3\ge0\), set
\[
x=\frac{\lambda_3}{E},
\qquad
y=\frac{\lambda_2+\lambda_3}{E},
\qquad
E=\lambda_1+\lambda_2+\lambda_3>0.
\]
The exact feasible region is
\[
0\le x\le\frac13,
\qquad
2x\le y\le\frac{1+x}{2}.
\]

## Panel contract

- **A — Bessel response and residual.** Plot \(A(N)\), the exact
  \(L_t^2\) residual \(A(N)/4\) at displayed normalization \(\nu=1\), and
  the neutral asymptotic reference \(N^{-4}\), for \(2\le N\le128\).
- **B — Exact reconstruction factor.** Plot \(A(N)^{-1}=(1+N^2)^2\) and the
  neutral reference \(N^4\) on the same frequency interval.
- **C — Feasible spectral strata.** Draw the complete ordered-eigenvalue
  domain and use the mutually exclusive partition
  \[
  \begin{aligned}
  \text{coercive}:&\quad x\ge\delta,\\
  \text{near-line}:&\quad x<\delta,\ y\le\eta,\\
  \text{near-plane}:&\quad x<\delta,\ y>\eta,
  \end{aligned}
  \qquad
  \delta=\frac1{20},\quad \eta=\frac25.
  \]
  The near-line region yields
  \(\lambda_1-\lambda_2\ge(1-2\eta)E=E/5\).
  In the near-plane region, strict \(y>\eta\) and \(x<\delta\) give
  \(\lambda_2-\lambda_3>(\eta-2\delta)E=3E/10\).

The displayed conditions make the three regions disjoint and exhaustive
inside the feasible domain.

## Data and transformations

Every curve and boundary is a closed exact formula certified by
`research/certificates/r070o/result.json`. Integer-frequency values and
rational boundary samples are written to `data.csv`; IEEE binary64 values are
used only for rendering. No random seed, fitted curve, DNS, or PDE time
integration is used. The plot script validates the response identities,
limits, feasible-domain inequalities, exact region areas, gap constants,
row count, output dimensions, embedded DPI, and visible claim boundary.

## Visual rules

- Double-column width, vector PDF/SVG, and 600 dpi PNG.
- At most two non-neutral color roots.
- Line style, marker shape and fill, hatching, and direct labels must preserve
  every distinction in grayscale.
- Both logarithmic axes and the displayed normalization \(\nu=1\) must be
  explicit.
- The complete feasible-domain boundary and all threshold lines must be
  visible.
- Original-resolution and grayscale QA renderings must be archived.

## Claim boundary

The figure proves neither that all filtered observables fail nor that a
low-rank covariance controls Navier--Stokes dynamics. It does not control a
space-time dependent principal direction, filter commutators, or the source
matrix in the covariance evolution. It is not a continuation theorem,
blow-up result, global-regularity result, or Millennium-problem solution.
