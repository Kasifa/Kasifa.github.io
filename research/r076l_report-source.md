# R0.76L source, collision, and evidence report

## Report frame

- Date: 2026-09-05.
- Audience: analysts and PDE researchers auditing the exact-shear branch.
- Question: what becomes of the R0.76K Chebyshev edge gain when the same
  start-prepaid exact integer shear is charged over the complete clock and
  against the full physical plateau mass?
- Decision: separate classical polynomial heat-flow identities from the
  simultaneous growing-degree edge limit and its local signed-flux use.
- Scope: the explicit first-kind Chebyshev family with
  `sqrt(A)<<m=o(A^2)`, its exact integer one-band shear realization, the
  complete signed collar clock, and the full-plateau denominator.
- Exclusions: an exhaustive priority search, arbitrary Fourier packets,
  Version-M, the formal `m` comparable with `A^4` route, regularity,
  singularity, and the Clay problem.

## Direct answer

For this explicit family, the complete clock suppresses but does not erase
the spatial Chebyshev obstruction.  If

\[
 \mu=(m^2/A)^{1/3},
 \qquad \sqrt A\ll m=o(A^2),
\]

then the fixed-slice exponent `m/sqrt(A)=mu^(3/2)` is replaced by a
complete-clock residual of order `exp(Theta(mu))`, up to polynomial factors
and frozen geometric constants.  The signed collar flux is eventually
positive, but after the frozen `omega^(1/3)` normalization its exact
quadratic logarithmic rate is still

\[
 -\frac{2}{11907}<0.
\]

Thus R0.76L is a route-specific negative result for the start-prepaid
family in `m=o(A^2)`: it rules out this family as a counterexample to the
R0.76E-type normalized estimate, while isolating a smaller complete-clock
edge scale that was invisible in R0.76K.  It neither proves a uniform
no-go theorem nor advances a regularity/singularity claim by itself.

## Primary-source ledger

| source | verified scope | role in R0.76L |
|---|---|---|
| [NIST DLMF, Chapter 18, Section 18.5](https://dlmf.nist.gov/18.5) | Official formulas for the classical Chebyshev representations, including the trigonometric and exterior hyperbolic forms. | Classical input for `T_m(cos theta)` and the `cosh(m arcosh x)` exterior formula. |
| [NIST DLMF, Chapter 18, Section 18.9](https://dlmf.nist.gov/18.9) and [Section 18.14, Eq. 18.14.4](https://dlmf.nist.gov/18.14) | Official derivative identities and interval inequalities for classical orthogonal polynomials. | Standard support for the endpoint derivative recurrence and the Gegenbauer-based majorant. |
| [B. C. Hall and C.-W. Ho, *The heat flow conjecture for polynomials and random matrices* (2025)](https://link.springer.com/article/10.1007/s11005-025-01946-9) | Publisher record for polynomial heat flow and its Gaussian/Hermite representations. | Confirms that the terminating heat series and Gaussian expectation are standard heat-polynomial identities, not a local novelty claim. |
| [Z. Kabluchko, *Lee--Yang zeroes of the Curie--Weiss ferromagnet, unitary Hermite polynomials, and the backward heat flow* (2025)](https://ahl.centre-mersenne.org/item/AHL_2025__8__1_0/) ([journal PDF](https://ahl.centre-mersenne.org/item/10.5802/ahl.227.pdf)) | Journal article on polynomial heat flow, Hermite representations, and high-degree zero dynamics. | Directly adjacent framework; its asymptotics concern zero distributions rather than the Chebyshev edge value, fixed-coordinate ratio, or the complete-clock flux used here. |
| [D. Dominici, *Asymptotic analysis of the Hermite polynomials from their differential-difference equation* (2006)](https://arxiv.org/abs/math/0601078) | Author manuscript deriving Hermite asymptotics in several regions. | Adjacent asymptotic input candidate; it does not by itself control the growing number of terms and cancellations in the present heat expansion. |
| [S. R. Batahan and A. Shehata, *Hermite-Chebyshev Polynomials with Their Generalized Form* (2014)](https://scientificadvances.co.in/admin/img_data/849/images/%5B4%5D%20JMSAA%207100121348%20S.%20Raed%20Batahan%20and%20A%20Shehata%20%5B47-59%5D.pdf) | Publisher PDF containing a fixed-scale operational relation between a Hermite--Chebyshev family and a heat-operator action on second-kind Chebyshev polynomials. | Direct algebraic collision for the operational viewpoint, but not for the first-kind forward double limit or the signed complete-clock theorem. |
| [W. A. Khan, *Certain Results for the Hermite and Chebyshev Polynomials of 2-Variables* (2019)](https://www.technoskypub.com/wp-content/uploads/2023/09/3-V2N2-P3-W-Certain-results-for-the-Hermite.pdf) | Publisher PDF giving higher-order exponential differential-operator formulas for two-variable Hermite--Chebyshev families. | Further evidence that fixed-scale operational identities are prior art; no matching edge-ratio or Navier--Stokes clock result was located. |

The Rosenbloom--Widder heat-polynomial paper
[DOI 10.1090/S0002-9947-1959-0107118-2](https://doi.org/10.1090/S0002-9947-1959-0107118-2)
and Ditzian's Chebyshev-transform paper
[DOI 10.1017/S144678870000968X](https://doi.org/10.1017/S144678870000968X)
were also retained as historical leads.  They support the conservative
classification of heat-polynomial algebra as established background; no
claim in R0.76L depends on importing an unverified theorem from them.

## Claim-to-evidence ledger

| claim | evidence | status |
|---|---|---|
| The terminating heat series, Gaussian convolution, Chebyshev exterior formula, and endpoint derivative identities are available inputs. | DLMF; Hall--Ho; the main note also derives the finite formulas used. | **CLASSICAL INPUT** |
| The operational idea of producing Hermite--Chebyshev families through exponential differential operators is new here. | Batahan--Shehata and Khan give direct fixed-scale precedents. | **FALSE; NOT CLAIMED** |
| In the simultaneous limit `m,A->infinity`, `x=1+c/A`, `mu=(m^2/A)^(1/3)`, the positive exterior integral has the stated saddle and fixed-edge tilt. | R0.76L L.17--L.29, including a uniform tilted-tail estimate. | **PROVED LOCALLY** |
| The signed polynomial heat flow has the same leading edge law as its positive exterior integral. | R0.76L L.27--L.29, with bounded middle interval and uniform negative-exterior suppression. | **PROVED LOCALLY** |
| The finite-`eta` consecutive integer shear follows from the ideal polynomial heat flow uniformly over the complete clock. | R0.76L L.38--L.47, by an exact conjugated operator and finite-dimensional Duhamel estimate. | **PROVED LOCALLY** |
| The full signed collar clock is eventually positive for the specified fixed negative drift. | R0.76L L.48--L.54, including quantitative terminal pairing and early-time absorption. | **PROVED LOCALLY FOR THIS FAMILY** |
| Full-plateau payment reduces the fixed-slice `mu^(3/2)` edge exponent to a complete-clock `mu` exponent. | R0.76L L.55--L.62. | **PROVED LOCALLY FOR THIS QUOTIENT** |
| The normalized quadratic logarithmic rate is `-2/11907`. | Exact physical conversion and frozen normalization, R0.76L L.63--L.66. | **PROVED LOCALLY** |
| At `m=kappa A^4`, the formal bulk-exterior saddle can cross the frozen penalty at the displayed threshold. | Formal balance R0.76L L.70--L.72 only. | **OPEN DIRECTION; NOT A THEOREM** |
| The result proves or disproves Navier--Stokes global regularity. | No such transfer is supplied. | **NOT CLAIMED; NOT CLAY** |

## Collision and priority boundary

Exact polynomial heat-flow formulas, Gaussian convolution, Chebyshev
derivative identities, and fixed-scale Hermite--Chebyshev operational
relations are classical inputs.  The local contribution claimed here begins
only with the simultaneous first-kind Chebyshev limit

\[
 m,A\to\infty,
 \qquad x=1+c/A,
 \qquad \mu=(m^2/A)^{1/3},
\]

and continues through its explicit complete-clock exact-shear application.
A bounded primary-source search found no theorem with this combined scope.
That absence is not evidence of novelty, priority, or nonexistence.

The reverse search combined `exp(tD^2)T_n`, Gaussian/Weierstrass
transforms, Chebyshev heat flow, Hermite--Chebyshev operational formulas,
edge scaling, and polynomial zero dynamics.  Results converged to the
fixed-scale operational identities or to zero-distribution asymptotics;
none stated the R0.76L fixed-edge logarithmic ratio or its complete-clock
collar/plateau application.  Search stopped once the direct algebraic
ancestry, the nearest modern heat-flow context, and the exact local claim
boundary were all identified.

## Finite diagnostic boundary

The archived deterministic binary64 computation checks the three terminal
constants

\[
 2^{5/3},\qquad 3\,2^{-2/3},\qquad 2^{-4/3}
\]

over sixteen finite `(A,m)` cases.  It saves data, progress/resource logs,
SVG, one-page PDF, and 600 dpi PNG.  It is finite evidence for scaling,
sign, constants, deterministic regeneration, and presentation quality.  It
does not prove the Laplace principle, the exact integer transfer, the
signed-flux estimate, or a Navier--Stokes regularity statement.

## Research-process note

Deep Research was used for the bounded primary-source and collision audit.
Its planning helper was unavailable in this environment, so the source
classes, claim matrix, collision queries, follow-up verification, and stop
rule were maintained directly in this report.  **NOT CLAY.**
