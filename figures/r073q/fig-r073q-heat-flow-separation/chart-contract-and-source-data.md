# R0.73Q chart contract and source-data note

## Analytical question

Does the exact shear sequence enter arbitrarily small critical heat-flow
neighbourhoods while escaping every fixed \(H^{1/2}\) ball, and what exact
time-endpoint calculation prevents replacing the required HLS estimate by a
bare Kato-sup argument?

## One-sentence takeaway

Along one smooth shear sequence, \(L^2\) and the heat-flow trace vanish while
\(H^{1/2}\) diverges; independently, the endpoint input stays bounded in
\(L^4\) while its fractional output diverges.

## Chart map

| Panel | Chart family | Source grain | Evidentiary role |
|---|---|---|---|
| A | log--log highlighted multi-series line | \(N=2^j\), \(0\le j\le32\) | checks all three exact shear-norm powers and constants |
| B | log--log parametric trace | the same 33 shear observations | displays simultaneous \(\mathfrak X\to0\) and \(H^{1/2}\to\infty\) without drawing either proof radius |
| C | log--log two-series line | \(n=2^j\), \(1\le j\le20\) | checks bounded endpoint input and divergent fractional output |

The requested data are sufficient because every panel shows a deterministic
ordered family with at least 20 observations. There is no empirical sample,
fit, random seed, PDE trajectory, or hidden interpolation.

## Exact formula source

On \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar measure, set

\[
 w_N=N^{-1/4}e_2\sin(Nx_1),\qquad
 c_6=\left(\frac5{16}\right)^{1/6}.
\]

Since \(e^{t\Delta}w_N=e^{-N^2t}w_N\), direct integration gives

\[
 \|w_N\|_2=2^{-1/2}N^{-1/4},\qquad
 |w_N|_{1/2}=2^{-1/2}N^{1/4},
\]

and

\[
 \|w_N\|_{\mathfrak X}
 =\left(\int_0^\infty\|e^{t\Delta}w_N\|_6^4dt\right)^{1/4}
 =\frac{c_6}{4^{1/4}}N^{-3/4}.
\]

Consequently, for every \(\rho>0\) and \(R>0\), some sufficiently large
\(N=2^j\) satisfies

\[
 \|w_N\|_{\mathfrak X}<\rho,
 \qquad |w_N|_{1/2}>R.
\]

This is the exact strictness quantifier. It does not compare
\(\rho_{\mathfrak X}[u]\) with the separately derived
\(R_{1/2}[u]\); the safe released domain is the union of the two tubes.

For integer \(n\ge2\), let

\[
 g_n(s)=n^{-1/4}(1-s)^{-1/4}
 \mathbf1_{\{e^{-n}<1-s<1/2\}}.
\]

Then

\[
 \|g_n\|_4^4=1-\frac{\log2}{n},\qquad
 \|g_n\|_4=\left(1-\frac{\log2}{n}\right)^{1/4},
\]

while

\[
 \int_0^1(1-s)^{-3/4}g_n(s)\,ds
 =n^{3/4}-n^{-1/4}\log2.
\]

The source CSV records both the fourth power and the norm so that the
validator can independently check the integration identity and the plotted
quantity.

## Visual encoding

The final surface is a 178 mm double-column archival figure. The palette uses
two chromatic roots, blue and ochre, plus neutrals. Solid, dashed, and dotted
lines; filled, open, and triangular markers; direct endpoint labels; arrows;
and boxed warnings carry meaning independently of colour. Axes are honest
logarithmic scales with dimensionless variables. No radius line is drawn.

## Claim boundary

Panels A and B certify exact norm geometry for one smooth structured family.
They do not certify arbitrary \(L^2\)-small data and do not rely on the
special cancellation \((w_N\cdot\nabla)w_N=0\) in the continuum theorem.
Panel C is a counterexample to one scalar endpoint mapping used by a failed
proof route. It is not a counterexample to the full Koch--Tataru space. No
panel is an NSE simulation, a nonlinear regularity computation, or a Clay
claim.
