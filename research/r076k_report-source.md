# R0.76K source, sharpness, and collision report

## Report frame

- Date: 2026-09-05.
- Audience: analysts and PDE researchers auditing the exact-shear branch.
- Question: is the `exp(Cq sqrt(d))` edge scale reconstructed in R0.76J
  still necessary after imposing a real field, conjugate pairing, one
  dyadic band, integer spatial modes, and exact heat-shear evolution?
- Decision: distinguish fixed-slice class sharpness from complete-clock
  signed-flux sharpness.
- Scope: pointwise and integrated spatial transfer for real one-band
  trigonometric fibres, plus exact realization at one prescribed scaled
  time by a smooth unforced Navier--Stokes shear.
- Exclusions: an exhaustive priority search, persistence on a time
  interval, a full-plateau flux lower bound, arbitrary nonlinear fields,
  regularity, singularity, and the Clay problem.

## Direct answer

Yes for the spatial slice, not yet for the full spacetime quotient.
For `q` positive cosine modes in one dyadic band and `0<d<=1`, R0.76K
constructs a real conjugate-paired confluent sequence with

\[
 \sup_g\frac{|g(1+d)|}{\|g\|_{L^2[-1,1]}}
 \ge\frac1{2\sqrt2}
 e^{(q-1)\operatorname {arcosh}(1+d)},
\]

and one witness over the whole exterior interval with transfer at least

\[
 \frac d{128}e^{2(q-1)\sqrt{7d/8}}.
\]

At `d=0`, the Legendre endpoint kernel gives the lower order `q/sqrt(2)`.
The same witnesses can be realized exactly at any one prescribed time by
consecutive positive integer modes `n_0,...,n_0+q-1` of an exact real heat
shear.  A uniform confluent estimate proves this realization for every
`q(L)=o(L^2)` in the frozen geometry.  It does not cover all of the
R0.76J upper window `q=o(L^(5/2))`.

The two-cap sign can be closed at the selected slice: a phase-shifted real
Chebyshev carrier makes every paired collar contribution nonnegative and
retains the `exp(2 Gamma_m)` cap-to-full-plateau spatial contrast.  The
fixed-time theorem nevertheless does not imply sharpness of the complete
signed collar flux divided by full three-dimensional plateau mass.  Exact
semigroup conjugation produces `e^(tau A^(-2)D^2)T_m`, not a common modal
decay.  An explicit backward-heat calculation grows like
`exp(c T m^2/A^2)` and invalidates a cost-free terminal-to-full-clock
bridge in the overlap `A^(3/2)<<m=o(A^2)`.  Time persistence, the full-clock plateau mass,
and signed contribution outside a terminal slab must still be controlled
simultaneously.  R0.76K keeps that problem open.

## Primary-source ledger

| source | verified status | exact role in R0.76K |
|---|---|---|
| [R. Zhang, *Optimal Extrapolation Bounds for Sparse Fourier Sums*, arXiv:2607.10501v1](https://arxiv.org/abs/2607.10501v1) ([v1 PDF](https://arxiv.org/pdf/2607.10501v1)) | The official arXiv record dates v1 to 2026-07-11 and states the arbitrary-real-frequency, no-separation upper scale `exp(O(k arcosh x))`, with `exp(O(k sqrt(delta)))` at the edge.  Proposition 7.1 in the v1 source gives the complex Chebyshev confluent lower sequence. | Attribution for the polynomial-to-exponential lower architecture and the complex-class benchmark.  R0.76K locally proves the realification, positive-frequency dyadic placement, integer heat-shear embedding, and varying-degree bound. |
| [X. Chen and E. Price, *Estimating the Frequency of a Clustered Signal*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.36), ICALP 2019, DOI 10.4230/LIPIcs.ICALP.2019.36 ([arXiv](https://arxiv.org/abs/1904.13043)) | The publisher record gives the 2019-07-04 publication date, authors, venue, DOI, and clustered no-gap Fourier setting.  Zhang identifies its Remark 8.6 as the earlier Chebyshev-growth motivation. | Historical motivation for the confluent polynomial obstruction; no theorem from it is required by the local proof. |
| [NIST DLMF, Chapter 18, Section 18.3](https://dlmf.nist.gov/18.3) | The official reference table records the Legendre interval, weight, norm `2/(2n+1)`, and standard normalization, and identifies the Chebyshev family. | Standard-source support for the Legendre orthogonality ledger used in the endpoint kernel.  The finite kernel sum is evaluated locally. |
| [NIST DLMF, Chapter 18, Section 18.6](https://dlmf.nist.gov/18.6) | Official special-value table for the classical orthogonal polynomials, including `P_n(1)`. | Standard-source support for the endpoint normalization. |

## Reconstruction ledger

| step | evidence | status |
|---|---|---|
| Complex confluent Chebyshev lower sequence | Zhang v1 Proposition 7.1; Chen--Price is cited there for the motivating observation. | **LITERATURE ARCHITECTURE** |
| Coefficient formula and eventual nonvanishing | K.7--K.8, by finite binomial expansion and leading-degree isolation. | **PROVED LOCALLY** |
| Real conjugate pairing and one dyadic positive band | K.9 with `n epsilon<M`; every coefficient is nonzero after the stated limit. | **PROVED LOCALLY** |
| Pointwise and integrated real-dyadic lower bounds | K.12--K.20, with a fixed low carrier and uniform convergence. | **PROVED LOCALLY** |
| Linear endpoint factor | K.21--K.24, using the finite Legendre Christoffel kernel. | **PROVED LOCALLY FROM STANDARD FACTS** |
| Exact integer heat-shear slice | K.25--K.30, by exact amplitude and phase compensation. | **PROVED LOCALLY** |
| Growing-degree frozen range | K.31--K.39, using coefficient recurrences and `eta q^2 7^q ->0`. | **PROVED LOCALLY** |
| Signed two-cap slice | K.41--K.45, by Chebyshev parity and a fixed carrier phase. | **PROVED LOCALLY** |
| Exact clock evolution and backward warning | K.46--K.48, by heat-semigroup conjugation and the explicit even-Chebyshev coefficients. | **PROVED LOCALLY** |
| Complete signed flux relative to full plateau mass | Requires one spacetime packet, not supplied by the slice identity. | **OPEN** |

## Collision and prior-art boundary

The bounded search covered the official Zhang arXiv record and v1 source,
the Chen--Price arXiv and ICALP publisher records, NIST DLMF, and targeted
searches combining Chebyshev confluent lower bounds with real conjugate
pairing, dyadic bands, integer heat shears, and Navier--Stokes.  It found
the complex confluent construction and older clustered-Fourier motivation,
but no source stating the exact combined R0.76K theorem for real
conjugate-paired one-band integer heat-shear slices.

That bounded absence is not evidence of novelty or priority.  The core
polynomial-to-nearly-colliding-exponential mechanism is explicitly prior
art.  R0.76K is presented only as a local restriction-and-embedding audit
needed by this project.  Orthogonal-polynomial endpoint kernels and their
norm identities are classical.

The search also found general Fourier-sparse leverage, interpolation, and
trigonometric-sampling work.  Those sources do not state a complete signed
shrinking-collar Navier--Stokes flux lower bound with a full physical
plateau denominator, so they do not close the remaining spacetime gap.

## Claim-to-evidence boundary

| claim | status |
|---|---|
| The `exp(cq sqrt(d))` spatial edge scale is necessary even for real conjugate-paired one-dyadic-band fibres. | **PROVED LOCALLY** |
| The same class forces a linear `q` endpoint factor in `L2`. | **PROVED LOCALLY FROM STANDARD FACTS** |
| Consecutive positive integer modes of an exact smooth heat shear realize the witness at any one prescribed scaled time. | **PROVED LOCALLY** |
| The frozen geometry supports the growing slice construction for every `q=o(L^2)`. | **PROVED LOCALLY** |
| Reality and the paired collar sign erase the Chebyshev contrast at that slice. | **FALSE; K.45 GIVES A FAVOURABLE PAIRING** |
| A terminal Chebyshev profile remains unchanged up to common heat decay on the full clock. | **FALSE; K.46--K.48 GIVE THE PARABOLIC OBSTRUCTION** |
| The construction proves sharpness throughout the upper window `q=o(L^(5/2))`. | **OPEN; NOT CLAIMED** |
| It proves a matching complete-clock signed-flux lower bound against full plateau mass. | **OPEN; NOT CLAIMED** |
| It transfers to arbitrary nonlinear three-dimensional fields or proves regularity/singularity. | **OPEN; NOT CLAY** |

## Search limits and stop reason

The search was deliberately bounded to primary author/publisher records
and an official mathematical reference.  Search-result snippets were not
used as proof.  The proof-relevant Zhang proposition was checked against
the v1 TeX source; the classical identities were checked against DLMF and
then derived in the main note.  Search stopped when the known complex
ancestry, the nearest prior motivation, and the exact unclosed spacetime
claim were all identified.  Further broad searching was unlikely to alter
the proof dependency or the conservative no-priority boundary.

The Deep Research planning helper was unavailable in this environment, so
the scope, claim families, primary-source classes, collision queries,
follow-up verification, and stop rule were recorded directly here.  No
simulation or formal figure is needed for this analytic release.
**NOT CLAY.**
