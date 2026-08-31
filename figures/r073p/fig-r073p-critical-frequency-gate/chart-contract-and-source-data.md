# R0.73P chart contract and source-data note

## Analytical question

How sharply does a high-frequency perturbation separate a direct \(H^3\)
entry condition from a critical \(\dot H^{1/2}\) entry condition, and what can
the linear heat semigroup show without importing an unjustified nonlinear
smoothing step?

## One-sentence takeaway

The frequency penalty improves from normalized order \(N^{-3}\) to
\(N^{-1/2}\) at the critical interface, leaving a wide pure-mode regime where
\(L^2\) and \(\dot H^{1/2}\) vanish while \(\dot H^3\) diverges; the heat plot
is only a linear scale benchmark.

## Chart map

| Panel | Chart family | Source grain | Evidentiary role |
|---|---|---|---|
| A | log--log threshold comparison | deterministic integer cutoffs \(N\) | displays the two normalized sufficient frequency penalties |
| B | exponent phase diagram | deterministic \(\gamma\)-grid plus exact boundary lines | identifies the open strip \(1/2<\gamma<3\) and the endpoint-prefactor caveat |
| C | log--log discrete maximum and continuous envelope | deterministic \(\tau\)-grid; exhaustive three-square radii | checks the exact sampled linear lattice maximum and its continuous upper bound |

## Formula source

No empirical data, fitted parameter, Navier--Stokes trajectory, or stochastic
sample enters this figure. `source-data.csv` is generated from the following
closed formulas.

For a Fourier cutoff \(N\), normalized unit radii give

\[
 \varepsilon_{H^3}(N)=N^{-3},\qquad
 \varepsilon_{\dot H^{1/2}}(N)=N^{-1/2}.
\]

For a mean-zero normalized Fourier mode \(e_N\) with \(|k|=N\) and
\(a_N=cN^{-\gamma}\),

\[
 \|a_Ne_N\|_{\dot H^s}=cN^{s-\gamma}.
\]

The plotted exponents are therefore \(-\gamma\),
\(1/2-\gamma\), and \(3-\gamma\). The open strip
\(1/2<\gamma<3\) has negative \(L^2\) and
\(\dot H^{1/2}\) powers but a positive \(\dot H^3\) power. If
\(\gamma>1/2\), then for every fixed \(c>0\) and every fixed critical radius
\(R_{1/2}>0\), there exists

\[
 N_0>N_0(c,R_{1/2},\gamma)
 \quad\text{such that}\quad
 cN^{1/2-\gamma}<R_{1/2}\quad(N\geq N_0).
\]

At \(\gamma=1/2\), the left side is the constant \(c\), so the strict
prefactor condition cannot be suppressed.

For \(\tau>0\), set

\[
 f_\tau(n)=n^{3/2}e^{-\tau n},\qquad n=|k|^2.
\]

The discrete curve is the maximum of \(f_\tau(n)\) over positive integers
representable as three squares. The continuous maximizer satisfies
\(n_*=3/(2\tau)\), giving

\[
 \sup_{r>0}r^3e^{-\tau r^2}
 =\left(\frac{3}{2e\tau}\right)^{3/2}.
\]

The configuration uses \(\tau\geq10^{-3}\) and lattice half-width
\(K=64\). Since \(K^2=4096>3/(2\tau_{\min})=1500\),
\(f_\tau(n)\) is strictly decreasing for every \(n\geq K^2\) and every
plotted \(\tau\). The included radius \(n=K^2\) therefore dominates every
omitted radius, while all representable \(n\leq K^2\) are exhaustively
enumerated.

## Visual encoding

The palette has two chromatic roots: blue and ochre. Line style, marker shape,
direct boundary labels, a zero reference line, and hatching preserve the
meaning in grayscale. All axes state either a dimensionless frequency,
Sobolev power, or nondimensional heat time.

## Claim boundary

Panels A and B are formula diagnostics for sufficient norm interfaces. They do
not establish that a general \(L^2\) perturbation is frequency truncated. Panel
C is a linear semigroup calculation. It does not control the Duhamel term, does
not prove delayed nonlinear smoothing, and cannot by itself certify entry into
a nonlinear stability tube.
