# R0.72S claim-to-evidence matrix

**Date:** 2026-08-28

| Candidate claim | Analytic route | Finite certificate role | Publication boundary |
|---|---|---|---|
| Every incidence preimage has type \(A_2\), \(A_3\), \(A_4\), or \(A_5\) | Substitute the R0.72R incidence formulas into derivatives three through six | Reconstructs all four jets exactly | This classifies incidence preimages, not self-intersections or complement chambers |
| The four-real-dimensional coefficient family is restricted miniversal through \(A_5\), modulo additive constants | The coefficient-derivative jet matrix of orders one through four has determinant \(5400\) | Independent determinant evaluation in two implementations | Full miniversality including the function-value direction needs one additional constant parameter; codimension statements are local to one incidence branch |
| A generic heat-law \(A_2\) crossing occurs at \(y=\log 2\) | Use \(z_{20}=4i,z_{30}=0\), reduce \(F'=0\) to a quadratic in \(\sin\phi\), and solve exactly | Checks the root formulas, unique degeneracy, jets, and root counts | The third carrier is inactive in this representative; the local stratum statement is nevertheless in the full four-dimensional family |
| The \(A_2\) path has \(4/3/2\) distinct critical points before/at/after the wall | Classify the two quadratic roots \(s_\pm(k)\) for \(k=8e^{-3y}\) | Checks the polynomial identities and exact sign guards | Counting multiplicity gives four at the crossing; one distinct point is \(A_2\) and two are simple |
| A real-even heat-law \(A_3\) crossing occurs at \(y=\log2\) | Factor \(F'=-\sin\phi\,q_\tau(\cos\phi)\) and prove \(q_\tau\) strictly decreases on \([-1,1]\) | Checks exact coefficient, derivative, and endpoint ledgers | A one-dimensional path is not transverse to the codimension-two \(A_3\) stratum in full coefficient space |
| The real-even \(A_3\) path has \(4/2/2\) distinct critical points before/at/after the wall | Prove \(q(-1)>0\), determine the sign of \(q(1)\), and use strict monotonicity | Independently reconstructs the factorization and all signs | Counting multiplicity gives four at the crossing; transversality is asserted only inside the two-dimensional real-even slice |
| Local branch laws are square-root laws | Taylor expansion of \(F'\) for \(A_2\), and of \(q(\cos\phi)\) for \(A_3\) | Checks leading coefficients \(-2\) and \(-6\) | No uniform remainder constant or nonautonomous PDE estimate is inferred from the plotted asymptotics |
| Stationary finite-type rates provide benchmarks | Apply the order convention in Albritton--Beekie--Novack to frozen \(A_2\) and \(A_3\) profiles | No computational theorem transfer | The stationary \(\nu^{3/5}\) and \(\nu^{2/3}\) rates do not prove decay through a time-dependent collision |
| Research value is a geometric input for the next PDE gate | Exact local strata plus two fully counted heat paths | No novelty certificate | No enhanced dissipation through the wall and no general three-dimensional Navier--Stokes regularity result |

## Rejected exploratory candidate

The active-third candidate

\[
 z_{20}=-2-\frac65i,
 \qquad z_{30}=\frac{128}{5}i
\]

was abandoned after an exploratory numerical scan indicated an additional
earlier fold.  No resultant, Sturm chain, isolating interval, or reproducible
certificate for that scan is retained in R0.72S, so neither the location nor
the resulting global count sequence is asserted here.  The candidate is not
used in the theorem or either formal figure.  Its only audit lesson is that a
single-time-slice gcd cannot certify an entire heat path.
