# R0.73O problem freeze: finite-action global-orbit stability and a forced Kolmogorov contrast

**Status:** theorem contract met; continuum proof, primary-source audit,
independent analytic readback, finite diagnostic, and formal figure pass;
public HTML/PDF publication remains a separate gate

**Parent result:** R0.73N fixed-member finite-strain stability and the
family-transfer obstruction

**Equation:** unforced incompressible Navier--Stokes on the normalized
standard three-torus, viscosity one, in the mean-zero divergence-free phase
space

**Topology:** full three-dimensional forward synchronized stability in

\[
 H^3_{\sigma,0}(\mathbb T^3).
\]

Smallness and observed distance are both measured in \(H^3\).  The resulting
\(H^3\)-input/\(L^2\)-output statement is only a corollary.  Full
three-dimensional FPS \((H^3,L^2)\), whose datum is small only in \(L^2\),
remains outside the theorem.

## 0. Direct decisions to be proved

R0.73N established a positive \(H^3\) tube around one explicit decaying
two-harmonic trajectory because its integrated \(H^4\) size is finite.
R0.73O asks whether that mechanism is special to the explicit formula or is
forced by the unforced periodic dynamics itself.

Let \(u\) be any a priori global strong solution satisfying

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0}).
 \tag{0.1}
\]

The unforced target answer is:

1. every such orbit has finite accumulated \(H^4\) action,

   \[
   \mathcal A_4[u]
   :=\int_0^\infty\|u(t)\|_{H^4}\,dt<\infty;
   \tag{0.2}
   \]

2. every such orbit has a positive, full-three-dimensional \(H^3\)
   stability radius;
3. the radius can be chosen uniformly over the starting time along that
   fixed orbit;
4. synchronized perturbations inside the tube converge exponentially to the
   reference orbit;
5. therefore no known a priori global unforced periodic orbit can be the
   base of an \(H^3\)-small fixed-background Lyapunov-instability mechanism.

The theorem is conditional on the reference datum already generating a
global strong solution.  It is an openness and route-exclusion result, not a
proof that every smooth datum is global.

The forced contrast target is deliberately separate.  On the same standard
three-torus, construct one explicit, nondecaying forced Kolmogorov equilibrium
with infinite accumulated strain and prove that it has smooth

\[
 H^3\hbox{-small initial perturbations that escape a fixed }L^2\hbox{ ball}.
 \tag{0.3}
\]

The escaping solutions must remain global and smooth, so that the conclusion
cannot be caused merely by failure of three-dimensional continuation.  The
example is allowed to use a two-dimensional invariant subspace, but it must be
described exactly that way: it is instability in the full three-dimensional
phase space witnessed by planar directions, not an essentially
three-dimensional unstable mode.

## 1. Exact phase space and norm convention

Let \(P\) be the Leray projector and let

\[
 A=-P\Delta
\]

on mean-zero divergence-free vector fields.  For integer \(m\ge0\), write

\[
 |z|_m:=\|A^{m/2}z\|_2.
 \tag{1.1}
\]

These homogeneous Stokes norms are equivalent to the usual periodic
\(H^m\) norms on the mean-zero phase space.  They obey

\[
 |z|_{m+1}\ge |z|_m,
 \qquad
 |z|_m^2\le |z|_{m-1}|z|_{m+1}.
 \tag{1.2}
\]

The proof may be written in the Stokes norms.  All public \(H^3\) statements
are obtained through fixed norm-equivalence constants; no topology is
changed.

## 2. Target O1: eventual smallness and the regularity ladder

The energy equality gives

\[
 {1\over2}\|u(t)\|_2^2
 +\int_0^t|u(s)|_1^2\,ds
 ={1\over2}\|u(0)\|_2^2.
 \tag{2.1}
\]

Hence there is a time \(T_1\) at which \(|u(T_1)|_1\) is below the universal
small-data threshold.  The target ladder is then

\[
 |u|_1\hbox{ small and decaying}
 \Longrightarrow |u|_2\hbox{ decays}
 \Longrightarrow |u|_3\hbox{ decays},
 \tag{2.2}
\]

using the three estimates

\[
\begin{aligned}
 {1\over2}{d\over dt}|u|_1^2+|u|_2^2
 &\le C_1|u|_1^{3/2}|u|_2^{3/2},\\
 {1\over2}{d\over dt}|u|_2^2+|u|_3^2
 &\le C_2|u|_1|u|_3^2,\\
 {1\over2}{d\over dt}|u|_3^2+|u|_4^2
 &\le C_3|u|_2|u|_4^2.
\end{aligned}
\tag{2.3}
\]

The first line preserves a sufficiently small \(H^1\) ball.  The second
line then damps \(H^2\), and after \(H^2\) is small the third line damps
\(H^3\).

## 3. Target O2: finite accumulated \(H^4\) action

After a finite time \(T_2\), the last line of (2.3) must yield constants
\(c,\alpha>0\) such that

\[
 {d\over dt}|u|_3^2+c|u|_4^2\le0,
 \qquad
 \int_{T_2}^\infty e^{\alpha(t-T_2)}|u(t)|_4^2\,dt<\infty.
 \tag{3.1}
\]

Weighted Cauchy--Schwarz then gives

\[
 \int_{T_2}^\infty|u(t)|_4\,dt<\infty.
 \tag{3.2}
\]

On \([0,T_2]\), (0.1) gives \(u\in L^2H^4\), hence \(u\in L^1H^4\).
Combining the two intervals closes (0.2).

## 4. Target O3: an all-starting-time positive tube

Fix a starting time \(t_0\ge0\), let \(v\) be a second local \(H^3\) strong
solution, and put

\[
 w=v-u,
 \qquad
 X=|w|_3^2,
 \qquad
 Y=|w|_4^2.
 \tag{4.1}
\]

The target perturbation estimate is

\[
 {1\over2}X'+Y
 \le C_*|u|_4X+C_*X^{1/2}Y.
 \tag{4.2}
\]

Define

\[
 r_*={1\over4C_*},
 \qquad
 R[u]=r_*e^{-C_*\mathcal A_4[u]}.
 \tag{4.3}
\]

The theorem to be proved is

\[
 |v(t_0)-u(t_0)|_3<R[u]
 \tag{4.4}
\]

implies a unique global forward strong solution and

\[
 \boxed{
 |v(t)-u(t)|_3
 \le e^{C_*\mathcal A_4[u]}
 e^{-(t-t_0)/2}|v(t_0)-u(t_0)|_3,
 \quad t\ge t_0.}
 \tag{4.5}
\]

The same \(R[u]\) works for every \(t_0\), because

\[
 \int_{t_0}^\infty|u(t)|_4\,dt\le\mathcal A_4[u].
 \tag{4.6}
\]

In the usual \(H^3\) norm, fixed equivalence constants modify only the
universal prefactor, radius, and exponential rate.

## 5. Exact quantifier consequences

Let \(\mathcal G_3\) be the set of mean-zero divergence-free \(H^3\) data
that generate a global strong solution.  The targets imply:

1. \(\mathcal G_3\) is open in \(H^3_{\sigma,0}\);
2. every trajectory through \(\mathcal G_3\) is uniformly forward
   synchronized and asymptotically stable in \(H^3\);
3. for each such trajectory and each \(\epsilon>0\), a positive
   \(H^3\)-smallness radius gives

   \[
   \sup_{t\ge t_0}\|v(t)-u(t)\|_{H^3}<\epsilon;
   \tag{5.1}
   \]

4. the same hypothesis gives a custom \(H^3\)-input/\(L^2\)-output
   corollary;
5. none of these claims closes full-three-dimensional FPS
   \((H^3,L^2)\), because the latter assumes only \(L^2\) smallness.

The complement \(H^3_{\sigma,0}\setminus\mathcal G_3\), if nonempty, is
closed.  This is a topological consequence of openness, not evidence that
the complement is nonempty.

## 6. Target O4: forced nondecaying contrast

With viscosity one, set

\[
 U_*(x,y,z)=(30.12\sin 10y,0,0),
 \qquad
 f_*(x,y,z)=(3012\sin 10y,0,0).
 \tag{6.1}
\]

The target proof must verify directly that (U_*) is a steady solution of the
forced equation and that

\[
 \int_0^\infty\|\nabla U_*\|_\infty\,dt=\infty.
 \tag{6.2}
\]

It must then audit the exact scaling from physical variables to the
Kolmogorov eigenvalue problem with

\[
 \alpha={7\over10},\qquad R={30.12\over10}=3.012,
 \tag{6.3}
\]

combine a rigorous right-half-plane spectral certificate with the
Friedlander--Pavlovi\'c--Shvydkoy nonlinear instability theorem, and retain
the planar invariant subspace so every escaping solution is globally smooth.
The spectral threshold, scaling, topology, and global-existence quantifiers
are independent release gates.

## 7. Literature and novelty boundary

The source audit must distinguish three levels.

1. Strong stability and openness of the global-data set are classical in
   whole-space critical topologies and under integrability criteria for
   large strong solutions.
2. R0.73O supplies a direct, topology-matched periodic \(H^3\) derivation
   and connects it to the R0.73M--N fixed-background route.
3. Unless an exact prior theorem is excluded by a bounded primary-source
   audit, the result must be described as a rigorous scoped corollary and
   route closure, not as a first or priority theorem.

Forced steady equilibria may be nonlinearly unstable under autonomous
spectral hypotheses.  They are admissible only as a contrast: forcing
removes the decay mechanism and changes the equation in the Clay problem.
The Kolmogorov spectral and nonlinear-instability ingredients are classical;
their role here is a topology-matched, globally smooth comparison, not a
novelty or priority claim.

## 8. Explicit exclusions

R0.73O does **not** prove any of the following:

1. that every \(H^3\) datum belongs to \(\mathcal G_3\);
2. an a priori bound for a trajectory not already known to be global;
3. stability under perturbations small only in \(L^2\);
4. stability for forced, bounded-domain, moving-wall, or nonperiodic flows;
5. optimality of \(R[u]\) or of the exponential rate;
6. absence of transient growth outside the certified tube;
7. finite-time singularity, global regularity for arbitrary data, or the
   Clay conclusion.

## 9. Release stop rule and final gate state

R0.73O can be formal-sealed only if all of the following pass independently:

1. the continuum proof of (2.3), (3.1), and (4.2)--(4.5);
2. a primary-source collision audit with exact norm/domain boundaries;
3. an adversarial audit of the mean-zero, start-time, continuation, and
   FPS-topology quantifiers;
4. a finite diagnostic and formal figure explicitly labeled illustrative;
5. synchronized bilingual HTML/PDF, cumulative recap, manifest, and
   publication tests.

The first four obligations now pass. The fifth remains the transactional
publication step and must bind the exact frozen sources, sealed finite
package, sealed figure, local bilingual copy, synchronized PDFs, cumulative
recap, manifest counts, and deployment tests before the release is called
public.

The next theorem interface after a PASS is not another unforced global
background.  It must cross one of the surviving boundaries deliberately:
weaker input topology, a trajectory not known a priori to be global, or a
forced/nondecaying comparison problem kept separate from the Clay equation.
