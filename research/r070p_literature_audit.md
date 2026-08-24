# R0.70P primary-literature audit

**Audit date:** 2026-08-25

**Audit decision:** CONDITIONAL PASS for the cited analytic inputs; no
priority or novelty claim

## 1. Question and bounded method

R0.70P uses two external analytic mechanisms:

1. an order-one commutator estimate with a Lipschitz coefficient, uniform
   over finite randomized Littlewood--Paley symbols;
2. a critical transverse-vorticity continuation mechanism, rewritten for a
   rank-one projector on the periodic box.

The audit checked the primary journal text or author manuscript for the
closest sources, not only abstracts or secondary descriptions.  It stopped
after the exact Coifman--Meyer theorem and endpoint section, Miller's exact
variable-direction theorem and proof mechanism, the middle-strain theorem's
torus statement, and the classical Betchov identity source were identified.

This is a bounded theorem-support audit.  It is not an exhaustive
MathSciNet, zbMATH, or all-language priority search.  Accordingly, the report
does not call the square commutator or the projector packaging new.

## 2. Coifman--Meyer: the order-one commutator dependency

- Primary source: R. R. Coifman and Y. Meyer, “Commutateurs d'intégrales
  singulières et opérateurs multilinéaires,” *Annales de l'Institut Fourier*
  28 (1978), no. 3, 177--202,
  [journal record](https://numdam.org/articles/10.5802/aif.708/),
  [primary PDF](https://www.numdam.org/item/AIF_1978__28_3_177_0.pdf),
  [DOI](https://doi.org/10.5802/aif.708).

The introduction, pp. 177--178, starts with a compact smooth manifold \(V\)
and states that if \(S\) is a classical order-one pseudodifferential
operator and \(A\) is Lipschitz, then

\[
 [S,A]:L^2(V)\longrightarrow L^2(V)
 \tag{2.1}
\]

is bounded.  It explicitly says that the problems are local and reduce to
the corresponding Euclidean statements.

Theorem 2, pp. 179--180, is the multilinear order-\(n\) statement.  With
\(n=1\), \(p_1=\infty\), and \(p=r=2\), it yields

\[
 \|[S,A]g\|_2
 \leq C_S\|\nabla A\|_\infty\|g\|_2.
 \tag{2.2}
\]

The displayed constant in that theorem is stated to depend on the symbol
bounds defining \(S\).  Section 5, beginning on p. 197, is the real-variable
endpoint argument that passes to \(p_1=\infty\).  These locations, rather
than the article abstract alone, are the relevant support for R0.70P.

For a finite randomized annular family

\[
 M_{\varepsilon,F}
 =\sum_{j\in F}\varepsilon_j\varphi(2^{-j}D),
 \qquad
 S_{\varepsilon,F}=M_{\varepsilon,F}|D|,
 \tag{2.3}
\]

finite overlap gives homogeneous order-one bounds for
\(S_{\varepsilon,F}\), uniform in \(F\) and the signs.  On
\(\mathbb R^3\), a finite family whose lowest active scale is below one is
first dilated so that its lowest scale is one.  Both (2.2) and the Lipschitz
seminorm scale invariantly, so the resulting constant is independent of the
truncation endpoints.  This dilation step avoids silently replacing a
homogeneous symbol class by a nonhomogeneous one with nonuniform low-scale
seminorms.

On \(\mathbb T^3\), the nonzero lattice has a fixed minimum frequency.
The compact-manifold formulation therefore applies to the periodized finite
symbols with uniform order-one bounds.  This supports the annular part of
the periodic estimate without treating ordinary linear multiplier
transference as though it automatically transferred a bilinear commutator.

The isolated constant block

\[
 T_\star=\Pi_0
 \tag{2.4}
\]

is not supplied by Coifman--Meyer and does not need to be.  For zero-mean
\(f\), R0.70P proves directly

\[
 \|[\Pi_0,A]f\|_2
 \lesssim_{\mathbb T^3}
 \|\nabla A\|_\infty\|f\|_{\dot H^{-1}_\#}
 \tag{2.5}
\]

by homogeneous \(H^{-1}\)--\(H^1\) duality.  The block is required because
\(P f\) can have a nonzero mean even when \(f\) does not.

### Support boundary

The source supports the first-order commutator estimate used after finite
randomization.  It does not state the R0.70P square-function estimate
verbatim.  The square estimate is the report's exact consequence of:

\[
 \mathbb E_\varepsilon
 \|[M_{\varepsilon,F},A]f\|_2^2
 =\sum_{j\in F}\|[T_j,A]f\|_2^2,
 \tag{2.6}
\]

the operator identity

\[
 [M,A]|D|=[M|D|,A]+M[A,|D|],
 \tag{2.7}
\]

and monotone convergence.  No infinite random multiplier is invoked before
the uniform finite estimate is proved.

## 3. Calderón: historical first commutator

- Primary source: A. P. Calderón, “Commutators of Singular Integral
  Operators,” *Proceedings of the National Academy of Sciences* 53 (1965),
  1092--1099,
  [full record](https://pmc.ncbi.nlm.nih.gov/articles/PMC301378/),
  [DOI](https://doi.org/10.1073/pnas.53.5.1092).

This is the classical first-commutator source behind the special multiplier
\(|D|\).  R0.70P cites it for the historical Calderón mechanism.  The
uniform randomized symbol-family statement is discharged by the more
general Coifman--Meyer theorem and the explicit symbol audit in Section 2,
not attributed verbatim to Calderón's paper.

## 4. Miller: the critical transverse-vorticity consumer

- Primary source: Evan Miller, “A Locally Anisotropic Regularity Criterion
  for the Navier--Stokes Equation in Terms of Vorticity,” *Proceedings of
  the American Mathematical Society, Series B* 8 (2021), 60--74,
  [DOI](https://doi.org/10.1090/bproc/74),
  [author manuscript](https://arxiv.org/abs/2002.02152).

Miller's Theorem 1.6 is stated for an \(H^1(\mathbb R^3)\) mild solution and
a global unit vector field \(v(x,t)\).  It assumes spatial Lipschitz control

\[
 \nabla_xv\in
 L^\infty_{\mathrm{loc}}([0,\infty);L^\infty_x)
 \tag{4.1}
\]

and uses the critical quantity

\[
 v\times\omega\in L_t^4L_x^2.
 \tag{4.2}
\]

No time derivative of \(v\) is assumed.  The proof's integration by parts
controls the component of the strain along \(v\) by (4.2), the velocity
energy, and \(\|\nabla v\|_\infty\).

The paper supports the exponent and mechanism used by R0.70P.  It does not
state the periodic, orientation-free projector theorem verbatim.  R0.70P
therefore reconstructs that theorem from periodic identities rather than
citing the whole-space statement as if the domain and topology were
unchanged.

The endpoint wording matters.  Miller defines the field on
\([0,\infty)\); hence local boundedness there is uniform on any finite
candidate interval.  Merely assuming

\[
 \nabla L\in
 L^\infty_{\mathrm{loc}}([0,T_{\max});L^\infty_x)
 \tag{4.3}
\]

does not prevent blow-up of the Lipschitz norm at \(T_{\max}\) and is not
enough for the periodic continuation proof.

## 5. Middle strain and the torus

- Primary source: Evan Miller, “A Regularity Criterion for the
  Navier--Stokes Equation Involving Only the Middle Eigenvalue of the Strain
  Tensor,” *Archive for Rational Mechanics and Analysis* 235 (2020),
  99--139,
  [DOI](https://doi.org/10.1007/s00205-019-01419-z),
  [author manuscript](https://arxiv.org/abs/1710.05569).

The paper proves the middle-eigenvalue strain criterion and explicitly notes
that the results apply equally on the torus, with the corresponding
domain-dependent Sobolev constants.  R0.70P uses the endpoint

\[
 \lambda_2^+\in L_t^4L_x^2
 \tag{5.1}
\]

but also writes the periodic strain identity, determinant estimate,
zero-mean Gagliardo--Nirenberg interpolation, Young inequality, and Gronwall
argument explicitly.  Thus the torus conclusion is not resting on an
uncited domain transfer.

## 6. Betchov identity

- Primary source: R. Betchov, “An Inequality Concerning the Production of
  Vorticity in Isotropic Turbulence,” *Journal of Fluid Mechanics* 1 (1956),
  497--504, [DOI](https://doi.org/10.1017/S0022112056000317).

The kinematic relation now called the Betchov identity underlies the strain
growth formula.  In R0.70P it is used as an exact periodic integration
identity for an incompressible field.  No statistical isotropy assumption is
imported into the continuation theorem.

## 7. Exact collision and novelty boundary

The literature supports the following dependency chain:

\[
 \text{order-one commutator}
 \Longrightarrow
 \text{finite-randomized LP square estimate}
 \Longrightarrow
 \text{energy-level frame bridge},
 \tag{7.1}
\]

and

\[
 \text{projected critical vorticity}
 \Longrightarrow
 \text{middle-strain control}
 \Longrightarrow
 \text{periodic continuation}.
 \tag{7.2}
\]

No audited source was used to claim that Navier--Stokes propagates the
solution-selected covariance residual, its spectral gap, or
\(|\nabla Q|/\operatorname{tr}Q\).  No audited source turns a normalized
covariance ratio into the absolute critical norm.  Those are the remaining
PDE gates.

The finite-randomized square form and orientation-free periodic packaging
may be useful formulations, but this bounded audit does not establish
priority.  A formal article must describe them as deductions or
reformulations unless a broader priority search supports a stronger claim.

## 8. Audit conclusion

The primary-source chain is sufficient for the conditional R0.70P report
provided all of the following remain explicit:

1. Coifman--Meyer Theorem 2 and its Lipschitz endpoint are the external
   order-one input;
2. uniformity over finite random symbols is verified from symbol seminorms
   and scaling, not assumed;
3. the periodic constant mode is added and estimated separately;
4. Miller's whole-space theorem is not quoted as a ready-made periodic
   projector theorem;
5. endpoint-uniform spatial Lipschitz control is retained;
6. no propagation, regularity, novelty, or Millennium claim is inferred
   from this literature audit.
