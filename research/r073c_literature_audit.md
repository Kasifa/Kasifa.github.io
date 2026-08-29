# R0.73C literature audit: cubic Rayleigh levels, instability, and viscous transfer

**Audit date:** 2026-08-30  
**Question:** which published theorem, if any, already proves the collision
profile claims C3--C5?  
**Source policy:** primary papers and official project documentation only

## 1. Decision

No located source directly proves the exact R0.73C chain

\[
 \text{cubic periodic neutral level}
 \Longrightarrow \text{purely growing inviscid mode}
 \Longrightarrow \text{uniform vanishing-viscosity transfer}.
\]

The first arrow lies near classical Tollmien--Lin theory but the present
profile violates its regular potential hypotheses at the cubic zero.  The
second arrow is a singular operator problem because the small viscous term is
unbounded in the kinetic space.  R0.73C therefore proves C3 directly, proves
C4 by a validated periodic-ODE sign change away from the singular phase
speed, and leaves C5 OPEN under an explicit spectral-persistence package.

## 2. Source matrix

| source | verified contribution | why it does not close the present gate |
|---|---|---|
| Z. Lin, *Instability of Some Ideal Plane Flows*, SIAM J. Math. Anal. 35 (2003), 318--356, [DOI](https://doi.org/10.1137/S0036141002406266) | Establishes purely growing modes for broad classes of ideal plane flows through neutral-mode and continuation methods. | For the present profile, \(-W_0''/W_0\sim-6/x^2\) is unbounded and not locally integrable. The regular odd-shear criterion cannot be invoked without a new singular continuation proof. |
| D. Bian and E. Grenier, *Singularities of Rayleigh equation*, [arXiv:2408.00977](https://arxiv.org/abs/2408.00977) | Analyses Rayleigh singularities and degenerate critical-layer behavior. | It provides relevant local structure, not the specific periodic monodromy sign or the global branch existence statement used here. |
| Z. Lin and C. Zeng, *Instability, index theorem, and exponential trichotomy for Linear Hamiltonian PDEs*, [arXiv:1703.04016](https://arxiv.org/abs/1703.04016) | Supplies abstract instability index and trichotomy machinery for Hamiltonian PDEs. | R0.73C still has to verify the singular profile's operator/domain hypotheses and later the viscous, non-Hamiltonian persistence package. |
| Z. Lin and M. Xu, *Metastability of Kolmogorov flows and inviscid damping of shear flows*, [arXiv:1707.00278](https://arxiv.org/abs/1707.00278) | Gives rigorous spectral/dynamical information for periodic shear flows and Kolmogorov-type settings. | The exact two-harmonic cubic collision profile and its logarithmic vanishing-viscosity transfer are not the theorem proved there. |
| mpmath 1.3.0 [interval documentation](https://mpmath.org/doc/current/contexts.html) and [pinned interval source](https://github.com/mpmath/mpmath/blob/1.3.0/mpmath/libmp/libmpi.py) | Documents closed interval arithmetic and implements basic endpoints with floor/ceiling directed rounding. | The library is an arithmetic engine, not an ODE theorem. R0.73C separately proves the Picard and Taylor enclosure logic and restricts use to basic algebra plus `iv.pi`. |

## 3. Hypothesis audit for the neutral criterion

The collision profile satisfies

\[
 W_0(x)=-\frac14x^3+O(x^5),
 \qquad
 -\frac{W_0''(x)}{W_0(x)}=-\frac6{x^2}+O(1).
\]

Consequences:

- the effective potential is not bounded;
- it is not in \(L^1_{\rm loc}\) at the joined cubic zero;
- the neutral phase speed lies in the essential spectrum;
- the admissible local branch is selected by an inverse-square limit-point
  condition rather than a regular endpoint condition;
- ordinary Kato continuation of an isolated neutral eigenvalue does not
  apply.

The exact Pöschl--Teller calculation is therefore an independent theorem for
C3, not a line-by-line application of the classical regular criterion.

## 4. Why the monodromy route is legitimate

For every fixed \(\eta>0\), the phase speed \(c=i\eta\) stays a distance at
least \(\eta\) from the real range of \(W_0\).  The periodic Rayleigh ODE is
then smooth.  A certified sign change of
\(\operatorname{tr}M(\eta)-2\) on a positive interval proves a periodic mode
by elementary ODE continuity; it does not cross the singular neutral phase
speed and does not need the missing singular continuation theorem.

## 5. Viscous-transfer literature boundary

Even after a positive inviscid eigenvalue is known, the fast-time generator

\[
 sA_{1/2}(d)-\varepsilon L_{1/4}
\]

contains an unbounded sectorial term.  The publication search did not locate
a theorem whose hypotheses have already been verified for this precise
kinetic-space family and which simultaneously supplies:

- eigenvalue persistence as \(\varepsilon\downarrow0\);
- uniform Riesz projections;
- a complement resolvent/dichotomy;
- graph-domain-compatible Kato transport along \(d=\varepsilon\theta\).

The R0.73C conditional transfer lemma is therefore a problem specification,
not a literature corollary.

## 6. Claim boundary

The literature supports the relevance of neutral modes, Rayleigh
singularities, and spectral trichotomy.  It does not authorize any of the
following shortcuts:

- treating the exact neutral mode alone as proof of an unstable branch;
- treating Fourier cutoff convergence as an infinite-dimensional spectrum
  theorem;
- treating \(-\varepsilon L\) as a small bounded perturbation;
- promoting one frozen linear row to nonlinear three-dimensional regularity
  or the Clay problem.

