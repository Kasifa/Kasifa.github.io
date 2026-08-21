# R0.69T — Exact physical-space annular increments and the affine-core boundary carrier

## 1. Result

R0.69S proves that sharp Fourier output shells alone cannot force a signed
depletion factor.  R0.69T returns to the full-space geometric Biot--Savart
kernel and keeps the sign before any absolute value is taken.

Let \(u\in C_c^\infty(\mathbb R^3;\mathbb R^3)\) be divergence free, put
\(\omega=\nabla\times u\), and write

\[
 \mathcal V(u)=\int_{\mathbb R^3}\omega\cdot S\omega\,dx,
 \qquad
 S=\frac{\nabla u+\nabla u^{\mathsf T}}2.
 \tag{1.1}
\]

For \(y\ne x\), set

\[
 e_{xy}=\frac{y-x}{|y-x|},
 \qquad
 J(x,y)
 =\bigl(e_{xy}\cdot\omega(x)\bigr)
  \bigl(e_{xy}\cdot(\omega(y)\times\omega(x))\bigr).
 \tag{1.2}
\]

The signed geometric representation from R0.69R becomes the direction-free
identity

\[
 \boxed{
 \mathcal V(u)
 =\frac{3}{4\pi}
 \iint_{\mathbb R^3\times\mathbb R^3}
 \frac{J(x,y)}{|x-y|^3}\,dy\,dx.}
 \tag{1.3}
\]

The double integral is absolutely convergent.  Averaging it with the same
integral after exchanging \(x\) and \(y\) gives a second exact identity.  If
\(\delta\omega(x,y)=\omega(y)-\omega(x)\), then

\[
 \boxed{
 \mathcal V(u)
 =\frac{3}{8\pi}
 \iint
 \frac{
  (e_{xy}\cdot\delta\omega(x,y))
  (e_{xy}\cdot(\omega(x)\times\delta\omega(x,y)))
 }{|x-y|^3}\,dy\,dx.}
 \tag{1.4}
\]

Thus global pair symmetrization supplies two vorticity increments, not one.
This is a genuine signed algebraic cancellation that was unavailable in the
pointwise near/far estimate of R0.69R.

Choose a smooth radial low-pass function \(\chi\) with
\(\chi(r)=1\) for \(0\le r\le1\), \(\chi(r)=0\) for \(r\ge2\), and
\(0\le\chi\le1\).  Define the nonnegative dyadic annuli

\[
 \psi_j(z)
 =\chi(2^{-j-1}|z|)-\chi(2^{-j}|z|),
 \qquad
 \sum_{j\in\mathbb Z}\psi_j(z)=1
 \quad(z\ne0).
 \tag{1.5}
\]

The signed physical-space annular production is

\[
 \boxed{
 \mathcal A_j(u)
 =\frac{3}{8\pi}
 \iint
 \psi_j(y-x)
 \frac{
  (e_{xy}\cdot\delta\omega)
  (e_{xy}\cdot(\omega(x)\times\delta\omega))
 }{|x-y|^3}\,dy\,dx.}
 \tag{1.6}
\]

Absolute convergence and the nonnegative partition imply

\[
 \boxed{
 \sum_{j\in\mathbb Z}\mathcal A_j(u)=\mathcal V(u),
 \qquad
 \sum_j|\mathcal A_j(u)|<\infty.}
 \tag{1.7}
\]

This closes the first R0.69T requirement: the annular observable reconstructs
total vortex stretching exactly, has no hidden remainder, and remains defined
at vorticity zeros without introducing the direction field
\(\xi=\omega/|\omega|\).

It does not yet prove a universal annular cancellation factor, a regularity
criterion, global regularity, or finite-time blow-up, and it does not solve the
Millennium Problem.

## 2. Removing the direction field exactly

On the set where both vorticities are nonzero, the geometric numerator is

\[
 \rho(x)^2\rho(y)
 (e_{xy}\cdot\xi(x))
 \bigl(e_{xy}\cdot(\xi(y)\times\xi(x))\bigr).
 \tag{2.1}
\]

Substituting \(\omega=\rho\xi\) cancels every denominator:

\[
 \boxed{
 \rho(x)^2\rho(y)
 (e_{xy}\cdot\xi(x))
 \bigl(e_{xy}\cdot(\xi(y)\times\xi(x))\bigr)
 =
 (e_{xy}\cdot\omega(x))
 \bigl(e_{xy}\cdot(\omega(y)\times\omega(x))\bigr).}
 \tag{2.2}
\]

The right side is polynomial in the two vorticities, so it extends through
their zero sets automatically.  Moreover,

\[
 \omega(y)\times\omega(x)
 =(\omega(y)-\omega(x))\times\omega(x),
 \tag{2.3}
\]

which already removes one near-diagonal singular order.

## 3. Pair exchange creates a second increment

Under \(x\leftrightarrow y\), the unit vector changes from \(e_{xy}\) to
\(-e_{xy}\).  Directly,

\[
 J(y,x)
 =-(e_{xy}\cdot\omega(y))
   (e_{xy}\cdot(\omega(y)\times\omega(x))).
 \tag{3.1}
\]

Consequently,

\[
 \begin{aligned}
 \frac{J(x,y)+J(y,x)}2
 &=\frac12
 (e_{xy}\cdot(\omega(x)-\omega(y)))
 (e_{xy}\cdot(\omega(y)\times\omega(x)))\\
 &=\frac12
 (e_{xy}\cdot\delta\omega)
 (e_{xy}\cdot(\omega(x)\times\delta\omega)).
 \end{aligned}
 \tag{3.2}
\]

Equation (1.4) follows because the radial kernel and Lebesgue measure are
invariant under pair exchange.

The pointwise size of the symmetrized numerator obeys

\[
 \left|
 (e_{xy}\cdot\delta\omega)
 (e_{xy}\cdot(\omega(x)\times\delta\omega))
 \right|
 \le |\omega(x)|\,|\delta\omega|^2.
 \tag{3.3}
\]

For a \(C^1\) field, \(|\delta\omega|=O(|x-y|)\).  The symmetrized kernel is
therefore \(O(|x-y|^{-1})\), which is locally integrable in three dimensions.
Since both vorticity factors vanish outside a common compact set, the
far-field part is also finite.

The improved local integrability is exact.  Turning (3.3) into a closed
Navier--Stokes estimate is a separate problem: the natural local quantity is
schematically \(\int|\omega||\nabla\omega|^2\), which is not controlled by
enstrophy and its first dissipation norm alone.

## 4. Finite annular windows expose both boundary tails

The definition (1.5) telescopes.  For integers \(L\le U\),

\[
 \boxed{
 \Psi_{L,U}(z):=\sum_{j=L}^{U}\psi_j(z)
 =\chi(2^{-U-1}|z|)-\chi(2^{-L}|z|).}
 \tag{4.1}
\]

Hence

\[
 1-\Psi_{L,U}(z)
 =\bigl[1-\chi(2^{-U-1}|z|)\bigr]
  +\chi(2^{-L}|z|).
 \tag{4.2}
\]

The first term is the far boundary and the second is the near boundary.
There is no unrecorded middle-scale commutator.  Inserting (4.2) into (1.4)
gives the exact remainder after retaining shells \(L,\ldots,U\).  Dominated
convergence sends both tails to zero as \(L\to-\infty\) and
\(U\to+\infty\).

If a cutoff scale is later allowed to move with time, differentiating the
two explicit \(\chi\)-terms in (4.2) will produce the complete boundary flux.
R0.69T does not silently discard that derivative.

## 5. Scaling and the correct physical-shell shift

Amplitude scaling is cubic:

\[
 \mathcal A_j(a u)=a^3\mathcal A_j(u).
 \tag{5.1}
\]

For the Navier--Stokes spatial scaling

\[
 u_\lambda(x)=\lambda u(\lambda x),
 \qquad
 \omega_\lambda(x)=\lambda^2\omega(\lambda x),
 \tag{5.2}
\]

and a dyadic factor \(\lambda=2^\ell\),

\[
 \boxed{
 \mathcal A_j(u_{2^\ell})
 =2^{3\ell}\mathcal A_{j+\ell}(u).}
 \tag{5.3}
\]

The production scales by the required factor \(2^{3\ell}\), while the
physical annulus moves from index \(j+\ell\) to the smaller length index
\(j\).  Therefore the annular cancellation ratio

\[
 \Gamma_{\rm ann}(u)
 =\frac{|\sum_j\mathcal A_j(u)|}{\sum_j|\mathcal A_j(u)|}
 \tag{5.4}
\]

is invariant under amplitude scaling and dyadic Navier--Stokes scaling
whenever its denominator is nonzero.

## 6. The affine core is carried entirely by boundary-crossing pairs

R0.69P constructs, for every trace-free matrix \(A\), a compactly supported
smooth divergence-free field

\[
 v_A=\nabla\times(\chi_0 B_A),
 \qquad
 B_A(x)=-\frac13x\times(Ax),
 \tag{6.1}
\]

such that \(v_A(x)=Ax\) on the unit ball \(B_1\).  On that ball,
\(\omega_A=\nabla\times(Ax)\) and \(S_A\) are constant.

If \(x,y\in B_1\), then

\[
 \delta\omega_A(x,y)=0,
 \qquad
 J(x,y)=0.
 \tag{6.2}
\]

Nevertheless one may choose \(A\) so that
\(\omega_A\cdot S_A\omega_A>0\) throughout \(B_1\).  Applying the original
signed kernel pointwise and integrating over the core gives the exact boundary
carrier identity

\[
 \boxed{
 |B_1|\,\omega_A\cdot S_A\omega_A
 =\frac{3}{4\pi}
 \int_{x\in B_1}\int_{y\notin B_1}
 \frac{J(x,y)}{|x-y|^3}\,dy\,dx.}
 \tag{6.3}
\]

Thus no pair lying wholly inside the affine core carries its positive
stretching.  The entire core production arrives through pairs crossing the
cutoff boundary.  This verifies the boundary-flux requirement stated in
R0.69R and explains why an internal direction-diffusion estimate could not
see the production in R0.69Q.

Equation (6.3) does not determine the signs of the individual annular pieces.
That sign distribution is the next computational and analytic target.

## 7. Decision for the route

R0.69T establishes the exact structural bridge

\[
 \boxed{
 \text{signed Biot--Savart kernel}
 \Longrightarrow
 \text{two-increment annular sum}
 +\text{explicit near/far boundaries}.}
 \tag{7.1}
\]

The remaining question is now precise: can the actual divergence-free
coupling force

\[
 \Gamma_{\rm ann}(u)\le\theta<1
 \tag{7.2}
\]

on a dynamically relevant class, or can a compactly supported saturating
family make \(\Gamma_{\rm ann}\to1\)?

The next audit will choose an explicit radial cutoff in (6.1), compute the
annular boundary-carrier distribution with monitored quadrature, and perform
two checks:

1. the annular sum must reproduce the exact core value in (6.3);
2. refinement and domain enlargement must stabilize every reported signed
   partial sum before any cancellation ratio is interpreted.

A numerical ratio will be treated only as exploratory evidence.  A route
closure requires either an analytic saturating family or a certified interval
bound uniform in the discretization parameters.

## 8. Prior work and claim boundary

The geometric vortex-stretching representation is classical, beginning with
Constantin and Fefferman.  Radial partitions of unity and increment
representations are standard harmonic-analysis devices.  R0.69T does not
claim those ingredients as new.

The project result is their exact combination at the integrated signed level:
the direction field is removed algebraically, pair exchange creates a second
vorticity increment, finite annular windows expose both boundary tails, and
the affine core is shown to be carried entirely by boundary-crossing pairs.

No annular depletion factor has yet been proved.  The note proves no new
regularity criterion, no global regularity theorem, and no finite-time
singularity result, and it does not solve the Millennium Problem.
