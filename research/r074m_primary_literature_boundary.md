# R0.74M bounded primary-source collision audit

## Scope and stop rule

Search date: 2026-09-02.

The bounded search asked one narrow question:

> Is there a primary theorem which directly supplies the endpoint-correlated,
> \(j\)-uniform estimate at the exponentially flat nearest inward collar
> frozen in R0.74M (F.10) or (F.19)?

Three search waves were used:

1. Brownian-bridge additive functionals and occupation laws;
2. Malliavin/Hörmander density and covariance estimates; and
3. stochastic finite-window estimates for passive scalars in shear flows.

The search stopped when new hits repeated the same mismatch: they gave
smooth densities, bridge representations, or global mixing for a fixed
shear, but not the signed collar observable with constants uniform in the
\(j\)-dependent exponentially flat family.  A bounded non-hit is not a
novelty, priority, or exhaustive-search claim.

## Primary-source ledger

### Kohatsu-Higa and Tanaka — additive-functional densities

Primary source:
[A Malliavin Calculus method to study densities of additive functionals of
SDEs with irregular drifts](https://www.numdam.org/item/10.1214/11-AIHP418.pdf).

Theorem 6 assumes a uniform Hörmander condition with a fixed positive
constant and proves inverse moments for the Malliavin covariance; Theorem 7
then obtains rapid characteristic-function decay and smooth densities for
the additive functional.  This supports the general idea that a shear
clock can be studied as an augmented diffusion.

It does not give the R0.74M estimate.  The source does not condition on the
bridge endpoint or preserve a correlated radial collar weight, and its
constants are tied to the uniform Hörmander data.  Establishing those data
uniformly for the exponentially flat \(R_j\)-family would itself contain
the missing estimate.

### Hairer — Hörmander via Malliavin calculus

Primary source:
[On Malliavin's proof of Hörmander's theorem](https://arxiv.org/abs/1103.1998).

Theorem 4.5 gives smooth transition densities under the parabolic Hörmander
condition.  Theorem 4.8 gives polynomial small-probability bounds for a
small Malliavin covariance eigenvalue, with constants attached to the
fixed vector fields.

Neither theorem gives a bridge-endpoint conditional density bound, an
\(L^\infty\) anti-concentration constant at the R0.74M scale, or constants
uniform in the frozen \(j\)-dependent shear.  Quoting Hörmander smoothness
would therefore move, not solve, the quantitative nondegeneracy problem.

### Nourdin and Viens — density bounds from a Malliavin sandwich

Primary source:
[Density estimates and concentration inequalities with Malliavin
calculus](https://arxiv.org/abs/0808.2088).

Theorem 3.1 and Corollary 3.4 provide explicit Gaussian density bounds when
the conditional Malliavin quantity \(g(Z)\) has a two-sided positive
sandwich.  Proposition 3.10 treats an integral of a monotone function of a
Gaussian process under corresponding derivative and covariance bounds.

These results can convert a previously proved uniform nondegeneracy
sandwich into a density estimate.  They do not prove that sandwich for the
R0.74M functional.  The present shear is exponentially flat on most of the
relevant plateau, the bridge has winding components, and the observable
keeps its endpoint collar correlation.  The required \(g(Z)\) lower bound
would be at least as difficult as the local lemma under review.

### Çetin and Danilova — Markov bridge SDEs

Primary source:
[Markov bridges: SDE representation](https://arxiv.org/abs/1402.0822).

Theorems 2.1--2.2 construct weak bridge solutions through an
\(h\)-transform, and later results give strong solutions under additional
conditions.  They justify bridge SDE representations when those
representations are needed.

They provide no tail estimate for the shear additive functional, no
uniform anti-concentration bound, and no signed collar estimate.  R0.74M in
fact avoids importing a new bridge SDE by using the already proved exact
common-forward-law disintegration.

### Villringer — Malliavin enhanced dissipation for a fixed shear

Primary source:
[Enhanced Dissipation via the Malliavin
Calculus](https://arxiv.org/abs/2405.12787).

Theorem 1.1 proves a global semigroup enhanced-dissipation rate for a fixed
autonomous shear with finitely many critical points of bounded order.  The
proof estimates inverse moments of a Malliavin determinant, and the
constants explicitly depend on the fixed profile \(u\).

This is methodologically close to a shear additive functional, but it has
no endpoint bridge condition, no \(j\)-dependent time-varying heat shear,
no local signed radial collar, and no supremum over the calibrated terminal
window.  It cannot be cited for the R0.74M constant.

### Liss and Luan — finite-window stochastic good/bad decomposition

Primary source:
[Uniform-in-diffusivity mixing by shear flows: stochastic and dynamical
perspectives](https://arxiv.org/abs/2603.09238).

Theorems 1.1--1.2 prove uniform-in-diffusivity mixing for a fixed smooth
autonomous shear with finitely many finite-order critical points.  Its key
stochastic lemma separates rare Brownian events from regions where the
random phase derivative is quantitatively large.

This is the closest recent structural analogue to R0.74M's good/bad path
split.  The theorem nevertheless controls global negative-Sobolev mixing
under an unconditioned stochastic flow.  Its constant depends on the fixed
profile \(b\); it does not cover a time-dependent exponentially flat
\(\theta_j\), the endpoint-correlated \(j-1\) collar, or the target annular
weight ratio.

### Fitzsimmons and Getoor — occupation times for Lévy bridges

Primary source:
[Occupation time distributions for Lévy bridges and
excursions](https://doi.org/10.1016/0304-4149(95)00013-W).

This source confirms that exact bridge occupation-time theory exists in
special Lévy settings.  Its special occupation structure does not contain
the time-varying smooth shear, winding mixture, derivative heat kernel, and
correlated radial window of R0.74M.  No theorem from it is imported.

## Decisive logical boundary

Positivity or monotonicity of an additive clock does not imply the required
anti-concentration.  If the integrand is a constant \(c\), then under every
endpoint-conditioned bridge

\[
 \int_0^T c\,ds=cT
\]

is an atom.  If the integrand is \(c+\varepsilon g\), a density constant
generally degenerates as \(\varepsilon\to0\).  Thus a global
Hörmander/Malliavin citation cannot replace a quantitative argument showing
that relevant paths actually sample a nonflat shear region.

The proof selected in R0.74M uses a different local fact.  Conditional on
the *collar support inside the common forward expectation*, a typical final
Brownian segment remains near the inward endpoint.  A direct positive heat
defect then produces a displacement much larger than \(LR\); exceptional
fast-return paths are paid by an explicit reflection estimate.  No density
or Malliavin theorem from the ledger is used as a black box.

## Collision verdict

No primary theorem found in the bounded search directly implies or refutes
the R0.74M estimate.  The closest papers support the general stochastic
mechanisms but miss endpoint correlation, the exponentially flat
\(j\)-family, or the signed local observable.  The final-segment caloric
defect lemma and its exact exponent ledger are therefore local contributions
of this research record.  Their analytic argument has passed the separate
independent reconstruction recorded in
r074m_nearest_inward_independent_audit.md.

This verdict is only a finite literature boundary.  It is not evidence of
novelty or priority.  **NOT CLAY.**
