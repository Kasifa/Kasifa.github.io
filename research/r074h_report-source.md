# R0.74H primary-source report

## Research question

For the two terminally anchored local frames frozen in R0.74E, does the
standard weighted local-energy identity support either of the following
claims?

1. the positive velocity--pressure flux across a smooth annular collar is
   the identity-level term missing from the disproved pure
   \(X_R\lesssim P_R^{2/3}\) estimate; and
2. the coarser two-regime bound
   \(X_R\lesssim P_R^{2/3}+P_R\) is consistent with established weighted
   and local-energy methods.

This is a bounded boundary check, not an exhaustive novelty or priority
search.  Sources were restricted to primary research papers.  Search and
source review were completed on 2026-09-01.

## Direct answer

The primary literature supports the *methodological form* of the R0.74H
derivation: a spatial weight in the Navier--Stokes energy balance produces
terms involving the derivative of that weight, including velocity transport
and pressure flux, and local-energy theories control energy on spatially
distributed families of regions.  None of the four sources below was found
to state the R0.74H theorem for the particular periodic dyadic collar weight,
the terminally anchored mollified trajectory, both R0.74E frames, or the
R0.74G two-packet diagnostic.

That absence is only a bounded-search observation.  It is not evidence of
novelty.

## Claim--source ledger

| Claim checked | Primary source | What the source directly supports | Boundary for R0.74H |
|---|---|---|---|
| Weighted energy methods for 3D NSE with polynomial spatial weights | Pedro Gabriel Fernández-Dalgo and Pierre Gilles Lemarié-Rieusset, [*Weak solutions for Navier--Stokes equations with initial data in weighted \(L^2\) spaces*](https://arxiv.org/abs/1906.11038), arXiv:1906.11038; published in *Archive for Rational Mechanics and Analysis*, DOI [10.1007/s00205-020-01510-w](https://doi.org/10.1007/s00205-020-01510-w) | Global weak solutions for data in \(L^2((1+|x|)^{-\gamma}dx)\), \(0<\gamma\le2\), using weighted energy controls; the weighted balance couples transport and pressure to derivatives of the weight | Polynomial Muckenhoupt weights on \(\mathbb R^3\), not periodic super-Gaussian dyadic collars or moving frames |
| Local-energy control through truncated Morrey-type quantities | Zachary Bradshaw and Tai-Peng Tsai, [*Global existence, regularity, and uniqueness of infinite energy solutions to the Navier--Stokes equations*](https://arxiv.org/abs/1907.00256), arXiv:1907.00256 | Global existence, initial/eventual regularity, and uniqueness results for local-energy solutions under scale-dependent Morrey-type hypotheses | Different observables, pressure expansion, geometry, and theorem objective; no R0.74E collar identity |
| Spatially distributed local-energy bounds in Wiener amalgam classes | Zachary Bradshaw and Tai-Peng Tsai, [*Local energy solutions to the Navier--Stokes equations in Wiener amalgam spaces*](https://arxiv.org/abs/2008.09204), arXiv:2008.09204 | A priori local-energy bounds, local/global existence, and growth results in \(L^2\)-based Wiener amalgam classes | Cube/amalgam aggregation rather than the frozen dyadic shell payment and terminal local frame |
| A broader family of weighted NSE estimates and suitable solutions | Pedro Gabriel Fernández-Dalgo and Pierre Gilles Lemarié-Rieusset, [*Weighted energy estimates for the incompressible Navier--Stokes equations and applications to axisymmetric solutions without swirl*](https://arxiv.org/abs/2010.00868), arXiv:2010.00868 | Weighted Leray procedure and suitable weak solutions; application to axisymmetric no-swirl data in weighted spaces | Axisymmetric/global application and different weights; no two-frame acceleration ledger or two-packet flux lower bound |

## Collision screen

The exact strings and concepts screened were:

- weighted Navier--Stokes energy identity with pressure and transport flux;
- local-energy solutions with weighted \(L^2\), Morrey, uniformly local, and
  Wiener-amalgam control;
- annular/collar leakage in local-energy arguments;
- moving, mollified, or Lagrangian local frames; and
- a two-regime \(P^{2/3}+P\) bound or a positive cumulative collar-flux
  correction.

The first three concepts have close methodological precedents in the sources
above.  The last two, in the exact R0.74E notation and geometry, were not
located in this bounded screen.

## What the sources do not certify

The literature review does not certify any of the following:

1. the signs, constants, shell limits, or acceleration power in the R0.74H
   derivation;
2. the R0.74G collar-flux lower bound;
3. weak-solution stability of the moving-frame flux;
4. novelty or publication priority;
5. an epsilon-regularity, continuation, blow-up, or global-regularity result.

Those items require separate mathematical audits.  In particular, the
R0.74H result remains a positive-scale size estimate and **NOT CLAY**.

## Reproducibility note

The stable identifiers used in this report are the four arXiv records
1906.11038, 1907.00256, 2008.09204, and 2010.00868.  The first source's DOI
was cross-checked through its arXiv journal reference.  No conclusion here
depends on search-result ranking or a secondary summary.
