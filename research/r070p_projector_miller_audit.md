# R0.70P periodic projector-form Miller audit

**Audit date:** 2026-08-25

**Audit decision:** CONDITIONAL PASS

The projector-form continuation argument is valid on \(\mathbb T^3\) for a
maximal \(H^1\) mild solution, provided the spatial Lipschitz norm of the
rank-one projector stays uniformly bounded all the way to a putative finite
maximal time.  No orientation of the line field and no time derivative of
the projector are needed.

The statement is not valid as an audited continuation theorem if “locally
bounded” means only bounded on every compact subinterval of
\([0,T_{\max})\).  That weaker condition permits
\(\|\nabla L(t)\|_\infty\) to diverge as \(t\uparrow T_{\max}\), precisely
where the proof needs an endpoint bound.  Section 2 records the exact
hypothesis.

## 1. Equation, solution class, and conventions

Let

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3
\]

and let \(\nu>0\).  Consider the unforced periodic Navier--Stokes equation

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0.
 \tag{1.1}
\]

The gradient convention in this note is

\[
 B_{ij}=(\nabla u)_{ij}=\partial_i u_j.
 \tag{1.2}
\]

Set

\[
 S=\frac12(B+B^{\mathsf T}),
 \qquad
 A=\frac12(B-B^{\mathsf T}),
 \qquad
 \omega=\nabla\times u.
 \tag{1.3}
\]

Let \(u_0\in H^1_\sigma(\mathbb T^3)\), and let

\[
 u\in C([0,T_{\max});H^1_\sigma(\mathbb T^3))
 \cap L^2_{\mathrm{loc}}([0,T_{\max});H^2(\mathbb T^3))
 \tag{1.4}
\]

be its maximal mild solution.  This is the strong/mild class used below.
Such a solution is smooth for every positive time strictly below
\(T_{\max}\).  The standard periodic \(H^1\) blow-up alternative says that
if \(T_{\max}<\infty\), then

\[
 \limsup_{t\uparrow T_{\max}}\|u(t)\|_{H^1}=+\infty.
 \tag{1.5}
\]

The argument below does not claim a new criterion for an arbitrary
Leray--Hopf solution.  Passing from that class to (1.4) would require a
separate weak--strong regularity argument.

## 2. Exact theorem and the endpoint condition

### Theorem 2.1 — Periodic projector-form continuation criterion

Let \(u\) satisfy Section 1.  Let

\[
 L:\mathbb T^3\times(0,T_{\max})\longrightarrow
 \mathbb R^{3\times3}
 \tag{2.1}
\]

be jointly measurable and satisfy, almost everywhere,

\[
 L=L^{\mathsf T},
 \qquad L^2=L,
 \qquad \operatorname{tr}L=1.
 \tag{2.2}
\]

Thus \(L\) is a rank-one orthogonal projector.  Set

\[
 P=I-L.
 \tag{2.3}
\]

Suppose, if \(T_{\max}<\infty\), that

\[
 M:=\operatorname*{ess\,sup}_{0<t<T_{\max}}
 \|\nabla_xL(t)\|_{L^\infty(\mathbb T^3)}<\infty
 \tag{2.4}
\]

and

\[
 \int_0^{T_{\max}}\|P(t)\omega(t)\|_2^4\,dt<\infty.
 \tag{2.5}
\]

Then the solution extends as an \(H^1\) mild solution beyond
\(T_{\max}\).  Consequently a finite maximal time is impossible under
(2.4)--(2.5).

An equivalent Miller-style formulation is to define \(L\) for all
nonnegative times and require

\[
 \nabla_xL\in
 L^\infty_{\mathrm{loc}}
 ([0,\infty);L^\infty(\mathbb T^3)).
 \tag{2.6}
\]

For a finite \(T_{\max}\), (2.6) supplies (2.4).  In contrast,

\[
 \nabla_xL\in
 L^\infty_{\mathrm{loc}}
 ([0,T_{\max});L^\infty(\mathbb T^3))
 \tag{2.7}
\]

does not supply (2.4).  It allows, for example, an unbounded Lipschitz norm
as \(t\uparrow T_{\max}\).  Condition (2.7) alone therefore fails the
acceptance gate for a continuation theorem.

The proof actually needs only the weaker weighted condition

\[
 \int_0^{T_{\max}}
 \|u(t)-\overline u_0\|_2^2
 \|\nabla u(t)\|_2^2
 \|\nabla L(t)\|_\infty^2\,dt<\infty.
 \tag{2.8}
\]

The endpoint-uniform condition (2.4), together with the energy equality,
is a simple solution-independent way to guarantee (2.8).

## 3. The conserved mean and the energy bound

Integrating (1.1) over the torus gives

\[
 \overline u(t):=\frac1{|\mathbb T^3|}
 \int_{\mathbb T^3}u(x,t)\,dx=\overline u_0.
 \tag{3.1}
\]

Define the mean-zero velocity

\[
 \widetilde u=u-\overline u_0.
 \tag{3.2}
\]

The strain, vorticity, and all spatial derivatives of \(u\) and
\(\widetilde u\) coincide.  Subtracting the constant mean from the usual
energy equality gives

\[
 \frac12\|\widetilde u(t)\|_2^2
 +\nu\int_0^t\|\nabla u(s)\|_2^2\,ds
 =\frac12\|\widetilde u_0\|_2^2.
 \tag{3.3}
\]

In particular,

\[
 \sup_{0<t<T_{\max}}\|\widetilde u(t)\|_2
 \leq\|\widetilde u_0\|_2,
 \qquad
 \int_0^{T_{\max}}\|\nabla u(t)\|_2^2\,dt
 \leq\frac{\|\widetilde u_0\|_2^2}{2\nu}.
 \tag{3.4}
\]

The use of \(\widetilde u\), rather than \(u\), in the integration by parts
below removes the harmless constant Fourier mode and gives the sharp
energy-level quantity.

## 4. Orientation-free projector algebra

Define

\[
 Z_L(t)=\int_{\mathbb T^3}\operatorname{tr}(L S^2)\,dx.
 \tag{4.1}
\]

At a fixed point, choose either of the two unit vectors spanning the range
of \(L\), solely for the pointwise calculation, and call it \(v\).  Then
\(L=v\otimes v\), but every expression below is invariant under
\(v\mapsto-v\).  One has

\[
 \operatorname{tr}(LS^2)=|Sv|^2
 \tag{4.2}
\]

and, since \(Av=\frac12v\times\omega\) up to the immaterial sign set by the
curl convention,

\[
 \operatorname{tr}(LA^{\mathsf T}A)
 =|Av|^2
 =\frac14|P\omega|^2.
 \tag{4.3}
\]

Expanding \(S=(B+B^{\mathsf T})/2\) and
\(A=(B-B^{\mathsf T})/2\) gives the exact identity

\[
 \operatorname{tr}(LS^2)-\frac14|P\omega|^2
 =B_{ij}B_{ki}L_{jk}
 =\partial_i u_j\,\partial_k u_i\,L_{jk}.
 \tag{4.4}
\]

Equation (4.4) is already expressed only in \(L\).  It therefore remains
globally meaningful when the line bundle has no global orientation.

## 5. The integration-by-parts estimate

Integrate the last term in (4.4) over \(\mathbb T^3\).  Periodicity and
incompressibility give

\[
\begin{aligned}
 I_L
 &:=\int_{\mathbb T^3}
 \partial_i u_j\,\partial_k u_i\,L_{jk}\,dx\\
 &=-\int_{\mathbb T^3}
 \widetilde u_j\,
 \partial_i(\partial_k u_i\,L_{jk})\,dx\\
 &=-\int_{\mathbb T^3}
 \widetilde u_j\,\partial_k u_i\,\partial_iL_{jk}\,dx.
\end{aligned}
 \tag{5.1}
\]

The term containing \(\partial_i\partial_k u_i\) vanishes because
\(\partial_i u_i=0\).  Hence

\[
 |I_L|
 \leq
 \|\widetilde u\|_2
 \|\nabla u\|_2
 \|\nabla L\|_\infty,
 \tag{5.2}
\]

where any fixed equivalent Euclidean tensor norm may be used.  Combining
(4.4) and (5.2) yields

\[
 Z_L(t)
 \leq\frac14\|P\omega(t)\|_2^2
 +\|\widetilde u(t)\|_2
  \|\nabla u(t)\|_2
  \|\nabla L(t)\|_\infty.
 \tag{5.3}
\]

After squaring,

\[
 Z_L(t)^2
 \leq\frac18\|P\omega(t)\|_2^4
 +2\|\widetilde u(t)\|_2^2
   \|\nabla u(t)\|_2^2
   \|\nabla L(t)\|_\infty^2.
 \tag{5.4}
\]

Equations (2.4), (3.4), and (5.4) give

\[
 \boxed{
 \int_0^{T_{\max}}Z_L(t)^2\,dt
 \leq
 \frac18\int_0^{T_{\max}}\|P\omega(t)\|_2^4\,dt
 +\frac1\nu\|\widetilde u_0\|_2^4M^2.}
 \tag{5.5}
\]

This is the only step in the projector-to-strain bridge that uses spatial
regularity of \(L\).  It explains why endpoint control in (2.4), rather
than (2.7), is needed.  No derivative in time appears.

For the solution class (1.4), (5.1) can first be applied on
\([\tau,T]\), where \(0<\tau<T<T_{\max}\) and the solution is smooth.
The estimates are uniform as \(\tau\downarrow0\), so the displayed bounds
extend to the initial endpoint.  Alternatively, (5.1) follows by standard
spatial approximation with the \(W^{1,\infty}\) coefficient \(L\).

## 6. The middle-eigenvalue reduction

Let

\[
 \lambda_1(x,t)\leq\lambda_2(x,t)\leq\lambda_3(x,t)
 \tag{6.1}
\]

be the eigenvalues of the symmetric, trace-free strain matrix.  For any
three ordered real numbers with zero sum,

\[
 |\lambda_2|=\min_{a=1,2,3}|\lambda_a|.
 \tag{6.2}
\]

Indeed, if \(\lambda_2\geq0\), then
\(|\lambda_1|=\lambda_2+\lambda_3\geq\lambda_2\); if
\(\lambda_2\leq0\), then
\(\lambda_3=|\lambda_1|+|\lambda_2|\geq|\lambda_2|\).

For any unit vector \(v\), the spectral theorem therefore gives

\[
 |Sv|^2\geq\lambda_2^2.
 \tag{6.3}
\]

Since \(\operatorname{tr}(LS^2)=|Sv|^2\) for either local lift,

\[
 (\lambda_2^+)^2
 \leq\operatorname{tr}(LS^2)
 \qquad\hbox{pointwise},
 \tag{6.4}
\]

where \(\lambda_2^+=\max\{\lambda_2,0\}\).  Consequently,

\[
 \|\lambda_2^+(t)\|_2^2\leq Z_L(t),
 \qquad
 \|\lambda_2^+(t)\|_2^4\leq Z_L(t)^2.
 \tag{6.5}
\]

By (5.5), assumptions (2.4)--(2.5) imply

\[
 \lambda_2^+\in L^4(0,T_{\max};L^2(\mathbb T^3)).
 \tag{6.6}
\]

## 7. Periodic strain growth identity

For a smooth periodic incompressible velocity field, the Betchov identity
and the vorticity energy equality give

\[
 \frac{d}{dt}\|S\|_2^2
 +2\nu\|\nabla S\|_2^2
 =-4\int_{\mathbb T^3}\det S\,dx.
 \tag{7.1}
\]

Equivalently, the underlying kinematic identity is

\[
 4\int_{\mathbb T^3}\operatorname{tr}(S^3)\,dx
 =-3\int_{\mathbb T^3}\omega\cdot S\omega\,dx,
 \tag{7.2}
\]

together with

\[
 \operatorname{tr}(S^3)=3\det S
 \tag{7.3}
\]

for a trace-free \(3\times3\) matrix.  These identities use only
periodicity, integration by parts, and incompressibility.  They do not
require decay at spatial infinity.

The elementary eigenvalue estimate

\[
 -\det S\leq\frac12\lambda_2^+|S|^2
 \tag{7.4}
\]

follows from

\[
 -\det S=(-\lambda_1\lambda_3)\lambda_2
 \leq(-\lambda_1\lambda_3)\lambda_2^+
 \leq\frac12|S|^2\lambda_2^+.
 \tag{7.5}
\]

Thus (7.1) implies

\[
 \frac{d}{dt}\|S\|_2^2
 +2\nu\|\nabla S\|_2^2
 \leq2\int_{\mathbb T^3}\lambda_2^+|S|^2\,dx.
 \tag{7.6}
\]

## 8. Gagliardo--Nirenberg, Young, and Gronwall

Each entry of \(S\) is a derivative of a periodic function, hence

\[
 \int_{\mathbb T^3}S\,dx=0.
 \tag{8.1}
\]

The zero-mean periodic Sobolev inequality and interpolation yield

\[
 \|S\|_4^2
 \leq C_{\mathbb T^3}
 \|S\|_2^{1/2}\|\nabla S\|_2^{3/2}.
 \tag{8.2}
\]

Set

\[
 Y(t)=\|S(t)\|_2^2,
 \qquad D(t)=\|\nabla S(t)\|_2^2,
 \qquad F(t)=\|\lambda_2^+(t)\|_2.
 \tag{8.3}
\]

Hölder, (8.2), and Young's inequality with exponents \(4/3\) and \(4\)
give

\[
\begin{aligned}
 2\int\lambda_2^+|S|^2
 &\leq2F\|S\|_4^2\\
 &\leq C_{\mathbb T^3}F Y^{1/4}D^{3/4}\\
 &\leq\nu D+C_{\mathbb T^3}\nu^{-3}F^4Y.
\end{aligned}
 \tag{8.4}
\]

Consequently,

\[
 Y'(t)+\nu D(t)
 \leq C_{\mathbb T^3}\nu^{-3}F(t)^4Y(t).
 \tag{8.5}
\]

Gronwall and (6.5) give, for every \(t<T_{\max}\),

\[
 Y(t)
 \leq Y(0)
 \exp\!\left(
 C_{\mathbb T^3}\nu^{-3}
 \int_0^t Z_L(s)^2\,ds
 \right).
 \tag{8.6}
\]

Inserting (5.5) proves the finite bound

\[
\begin{aligned}
 \sup_{0<t<T_{\max}}\|S(t)\|_2^2
 \leq \|S(0)\|_2^2
 \exp\!\Bigg[
 C_{\mathbb T^3}\nu^{-3}
 \Bigg(&\frac18
 \|P\omega\|_{L_t^4L_x^2(0,T_{\max})}^4\\
 &+\frac1\nu
 \|\widetilde u_0\|_2^4M^2\Bigg)
 \Bigg].
\end{aligned}
 \tag{8.7}
\]

No low-frequency correction appears in (8.2), because \(S\) has zero
spatial mean.

## 9. Closing the continuation argument

For a periodic divergence-free velocity,

\[
 \|\nabla u\|_2^2=2\|S\|_2^2=\|\omega\|_2^2.
 \tag{9.1}
\]

The conserved mean, (3.3), and (8.7) therefore imply

\[
 \sup_{0<t<T_{\max}}\|u(t)\|_{H^1}<\infty.
 \tag{9.2}
\]

This contradicts the blow-up alternative (1.5).  Equivalently, choose a
sequence \(t_n\uparrow T_{\max}\).  The uniform \(H^1\) bound gives a local
existence time from each \(u(t_n)\) bounded below independently of \(n\),
so one of the restarted mild solutions extends beyond \(T_{\max}\).
Uniqueness in the \(H^1\) mild class identifies it with the original
solution on the overlap.  This completes the proof of Theorem 2.1.

## 10. Orientation and time regularity

The theorem is genuinely projector-valued:

- A global unit lift \(v\) is not assumed.
- A nonorientable rank-one line bundle on \(\mathbb T^3\) causes no
  difficulty.
- The quantities \(\operatorname{tr}(LS^2)\), \(|P\omega|\), and
  \(\partial_iL_{jk}\) are invariant under local sign changes of a lift.
- Only joint measurability in \(t\) is needed.  Neither continuity in time
  nor \(\partial_tL\) occurs in the proof.
- Spatially, \(L(t)\in W^{1,\infty}\) almost everywhere in time is enough.

If an oriented lift happens to exist, then locally

\[
 L=v\otimes v,
 \qquad
 \|\partial_iL\|_F=\sqrt2\,|\partial_iv|.
 \tag{10.1}
\]

Thus the projector condition is quantitatively equivalent to Miller's
spatial Lipschitz condition on a lift, while avoiding a global topology
assumption.

## 11. Forcing and weak-solution caveats

This audit proves Theorem 2.1 only for the unforced equation.  With an
external force, both the mean equation and the strain growth identity gain
terms.  A forced extension requires explicit assumptions sufficient to
control those terms, for example the force class used in the cited strain
criterion.  The unforced theorem must not be quoted unchanged for an
arbitrary force.

Likewise, the calculation does not by itself prove regularity of every
Leray--Hopf solution satisfying formal versions of (2.4)--(2.5).  In that
setting the Betchov/strain identity, the meaning of the projector
integration by parts, and the transition to the strong class all require
additional justification.

## 12. Non-skippable lemmas and acceptance boundary

A canonical use of Theorem 2.1 must retain all of the following points:

1. conservation of the periodic mean and the mean-zero energy equality;
2. the exact projector identity (4.4);
3. the periodic integration by parts (5.1);
4. endpoint-uniform control (2.4), or the weighted replacement (2.8);
5. the spectral inequality (6.4);
6. the periodic Betchov/strain identity (7.1);
7. the determinant inequality (7.4);
8. zero-mean periodic Sobolev interpolation (8.2);
9. Young's inequality at the \((4/3,4)\) exponents and Gronwall;
10. the periodic \(H^1\) blow-up alternative.

The continuation route passes if these statements are present with the
solution class and endpoint condition above.  It fails the acceptance gate
if (2.4) is replaced only by (2.7), if a global orientation is silently
assumed, if the whole-space Miller theorem is cited as though it were
already a periodic theorem, or if the conclusion is enlarged to arbitrary
Leray--Hopf solutions without a separate argument.

## 13. Primary-source boundary

1. Evan Miller, “A Locally Anisotropic Regularity Criterion for the
   Navier--Stokes Equation in Terms of Vorticity,” *Proceedings of the
   American Mathematical Society, Series B* 8 (2021), 60--74,
   [DOI](https://doi.org/10.1090/bproc/74),
   [author manuscript](https://arxiv.org/abs/2002.02152).

   Miller's theorem is stated on \(\mathbb R^3\) for a unit vector field
   \(v\), with
   \(\nabla_xv\in L^\infty_{\mathrm{loc}}([0,\infty);L^\infty_x)\), and
   assumes no time derivative of \(v\).  Its key integration by parts is
   exactly the oriented version of (5.1).

2. Evan Miller, “A Regularity Criterion for the Navier--Stokes Equation
   Involving Only the Middle Eigenvalue of the Strain Tensor,” *Archive for
   Rational Mechanics and Analysis* 235 (2020), 99--139,
   [DOI](https://doi.org/10.1007/s00205-019-01419-z),
   [author manuscript](https://arxiv.org/abs/1710.05569).

   This paper proves the middle-eigenvalue strain criterion on
   \(\mathbb R^3\) and explicitly notes that the results apply on the torus
   with the corresponding periodic Sobolev constants.  Sections 7--9 above
   reconstruct the periodic \(q=2,p=4\) case instead of relying only on
   that remark.

3. R. Betchov, “An Inequality Concerning the Production of Vorticity in
   Isotropic Turbulence,” *Journal of Fluid Mechanics* 1 (1956), 497--504,
   [DOI](https://doi.org/10.1017/S0022112056000317).

   The classical kinematic relation behind (7.2) is the Betchov identity.
   For the present theorem it is used as an exact periodic integration
   identity, not as a statistical or isotropy assumption.

## 14. Audit conclusion

The periodic projector-form route is mathematically closed at the
conditional level stated in Theorem 2.1.  Its gain over a vector-field
formulation is topological, not a stronger exponent: the proof uses only
the rank-one projector and therefore does not require an oriented principal
line.  The two substantive hypotheses remain the endpoint-uniform spatial
Lipschitz bound and the critical unfiltered transverse-vorticity condition.
The next covariance bridge may supply the second condition only after its
all-frequency and commutator estimates are proved; this note does not claim
that either hypothesis follows from covariance eigenvalue ratios alone.
