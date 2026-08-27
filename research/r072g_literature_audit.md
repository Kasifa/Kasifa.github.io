# R0.72G primary-source literature audit

**Date:** 2026-08-27

**Question:** Is there an existing theorem that controls the complete
temporal zero-slope mass of the distinguished Fourier coordinate in the
R0.72E one-carrier parabolic lattice?

**Decision:** I found sources for time analyticity, spatial zero-number
theory, fixed-node sampling, Bessel asymptotics, and counterexamples to
naive global temporal-zero finiteness.  I did not find a source that gives the
complete, root-count-free temporal slope-sum estimate needed here.  R0.72G
therefore uses an internal real-phase Rolle--BV argument rather than citing
analyticity or Sturm theory as a substitute.

## 1. Claim--source ledger

| Source | What the source supports | What it does not support here |
|---|---|---|
| NIST DLMF, [Jacobi--Anger expansions](https://dlmf.nist.gov/10.12), [large-argument Bessel asymptotics](https://dlmf.nist.gov/10.17), and [Bessel zeros](https://dlmf.nist.gov/10.21) | Fixed-order Bessel expansions, simple positive roots, root locations, and derivative asymptotics.  These imply the selected-root law \(|J_1'(j_{1,k})|^2\asymp k^{-1}\) and hence logarithmic accumulated mass. | It does not show that the nonautonomous lattice has no additional roots or bound their total slope mass. |
| S. Kusuoka and D. Stroock, *Applications of the Malliavin calculus, Part II* (1985), [DOI](https://doi.org/10.15083/00039520) | Corollary (3.25) and inequality (3.27) provide the quantitative density input inherited by the R0.72E negative-moment and action estimate. | It is not a temporal-root theorem and does not contain the target-row Rolle identity or the critical-log physical ledger. |
| P. Polacik and V. Sverak, *Zeros of complex caloric functions and singularities of complex viscous Burgers equation* (2008), [arXiv](https://arxiv.org/abs/math/0612506), [DOI](https://doi.org/10.1515/CRELLE.2008.022) | Theorem 3.3 treats isolated interior zeros of certain complex caloric solutions.  Proposition 5.1 constructs a fixed-point temporal trace with zeros \(\tau_k\to\infty\) on an unbounded half-line despite nonvanishing initial data. | Parabolic smoothing and analyticity alone therefore do not give a uniform global temporal root count.  The paper does not estimate the squared time slopes at those roots or contradict finite root counts on compact positive-time intervals. |
| H. Dong and Q. S. Zhang, *Time analyticity for the heat equation and Navier--Stokes equations* (2020), [arXiv](https://arxiv.org/abs/1907.01687) | Quantitative time-analyticity and time-derivative estimates for heat solutions and bounded mild NSE solutions at positive times. | The estimates degenerate toward launch and do not imply a root count, root separation, or a sum of root slopes. |
| Y. Giga, H. Jo, A. Mahalov, and T. Yoneda, *On time analyticity of the Navier--Stokes equations in a class of spatially almost periodic functions* (2008), [author manuscript](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/69669/re860.pdf) | Individual Fourier/Bohr amplitudes are analytic for positive time in the stated mild almost-periodic setting. | Analyticity only makes nontrivial interior roots isolated.  It gives no complete root-slope sum and no launch-uniform constant. |
| S. Angenent, *The zero set of a solution of a parabolic equation* (1988), [DOI](https://doi.org/10.1515/crll.1988.390.79) | Structure and zero-number tools for spatial zeros of one-dimensional real scalar parabolic equations. | The variable and object differ: R0.72G samples a fixed Fourier coordinate in time.  The theorem is not a temporal trace estimate. |
| H. Matano, *Nonincrease of the lap-number of a solution for a one-dimensional semilinear parabolic equation* (1982), [official repository](https://repository.dl.itc.u-tokyo.ac.jp/records/39589) | Monotonicity of a spatial lap number in a real one-dimensional parabolic problem. | It does not transfer to a complex Fourier temporal trace or a squared-slope ledger. |
| K. Masuda, *On the analyticity and the unique continuation theorem for solutions of the Navier--Stokes equation* (1967), [J-STAGE](https://www.jstage.jst.go.jp/article/pjab1945/43/9/43_9_827/_article/-char/en) | Analyticity and whole-field unique continuation for sufficiently regular NSE solutions. | Vanishing of one annular/Fourier observable at isolated times is far weaker than vanishing of the full field on a spatial open set. |
| L. de Branges, *Hilbert Spaces of Entire Functions* (1968), [author-hosted book](https://www.math.purdue.edu/~branges/Hilbert%20Spaces%20of%20Entire%20Functions.pdf), and J. Ortega-Cerda--K. Seip, *Fourier frames* (2002), [Annals](https://annals.math.princeton.edu/2002/155-3/p03) | Stable sampling in de Branges or Paley--Wiener spaces at prescribed sequences satisfying the relevant structural conditions. | The nodes here are the moving zeros of the sampled function itself.  Separation, density, and a uniform entire-function type have not been established. |
| B. Ya. Levin, *Distribution of Zeros of Entire Functions* (1964), [AMS](https://bookstore.ams.org/mmono-5/) | Growth, type, and zero-density theory for Cartwright and related entire functions. | Root counts depend on growth and an anchor; they do not directly control the derivative mass, and the launch trace lacks a uniform entire type. |

## 2. Why analyticity is not the missing estimate

Positive-time analyticity can show that a nontrivial scalar trace has
isolated roots on compact subintervals away from launch.  It cannot by
itself control

\[
 \sum_{f(x_j)=0}|f'(x_j)|^2,
 \tag{2.1}
\]

uniformly as roots approach the launch endpoint.  The Polacik--Sverak
example makes the more basic point that a complex caloric time trace can
have infinitely many roots on an unbounded time half-line.  A proof based only
on smoothing or analyticity would therefore have a genuine logical gap.

R0.72G instead uses the special real phase gauge of the exact one-carrier
lattice.  Rolle's theorem then inserts a zero of the coupling slope between
two target roots, and the exact target-row equation converts the full root
sum into a continuous negative-Sobolev action.  This mechanism neither
counts roots nor assumes they are separated.

## 3. Why spatial Sturm theory and fixed sampling do not transfer

Angenent and Matano control spatial sign changes of real one-dimensional
parabolic solutions at a fixed time.  The target here is one Fourier
coordinate as a function of time; it is not itself governed by a closed
scalar parabolic equation.  De Branges and Paley--Wiener sampling theory
also has the wrong input geometry: the sampling nodes are normally fixed by
the ambient space, whereas the nodes here are the solution-dependent zeros
of the function being sampled.

These theories remain useful comparisons.  They do not prove the
root-count-free estimate in R0.72G.

## 4. Allowed literature statement

The following wording is supported by this audit:

> Standard Bessel theory supplies the selected logarithmic lower mass, and
> quantitative Malliavin density estimates supply the inherited
> negative-Sobolev action upper bound.  Time analyticity and spatial
> zero-number results do not control this complete temporal slope sum.  In
> the exact real one-carrier lattice, the missing estimate is instead
> obtained from an explicit phase gauge, Rolle's theorem, and the target-row
> evolution identities.

The statement “no existing theorem does this” is not supported without a
qualification.  The correct claim is that no such theorem was found in the
bounded primary-source search above.  This audit is not an originality,
priority, or exhaustive-search certificate.
