# R0.71E — Projected Lamb compression, unconditional heat bulk, and the critical bottom-trace gap

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, vorticity stretching, Littlewood--Paley
localization, and heat-extension square functions

**Status:** exact global and localized identities, an unconditional
energy-level heat-bulk estimate, a minimal exact Fourier trace obstruction,
and two independent finite certificates; no unconditional regularity theorem,
no singularity construction, and no Millennium-problem claim

## 1. Direct decision

R0.71D left one narrow possibility open.  The material heat-tent geometry
alone did not improve the critical scale, but perhaps the three apparently
different nonlinear sectors--stretching, transport--filter commutation, and
pressure--had a special Navier--Stokes cancellation.

R0.71E gives a positive intermediate result and identifies the remaining
gap exactly.

1. The three sectors are not independent in the vorticity equation.  After
   the Hodge projection, stretching and transport compress into the curl of
   the solenoidal Lamb vector

   \[
     L=\mathbb P(u\times\omega).
   \]

   Pressure is the complementary Bernoulli gradient.  It cannot be added as
   a third freely signed vorticity term.
2. For every tight real-even scalar frame, the complete positive shell
   injection at heat height \(s\) is bounded by

   \[
     \Theta_s^2\le \|e^{s\Delta}L\|_2^2.
   \]

3. Its full vertical integral satisfies the exact energy-level estimate

   \[
     \int_0^\infty\Theta_s^2\,ds
     \le \frac12\|(-\Delta)^{-1/2}L\|_2^2
     \le \frac12\|u\|_4^4.
   \]

   After division by enstrophy, this heat-bulk coefficient is
   unconditionally integrable in time for every Leray--Hopf solution on a
   finite interval.
4. This does not control the bottom value \(\Theta_0^2\).  For the fixed
   radial frame constructed in Section 10, a support-minimal six-mode smooth
   NSE datum gives at the initial heat trace

   \[
     A_{\rm sb,+}(0)=2K^2\,\mathcal V(0).
   \]

   The missing bottom trace costs exactly two frequency powers.  Across a
   heat-height window of size \(K^{-2}\), the normalized vertical mass is
   strictly positive and independent of \(K\).
5. Localizing the projected Lamb identity creates a cutoff--curl boundary
   term.  Reintroducing the Bernoulli gradient only splits this term into two
   pieces that cancel exactly.  A separate pressure sign is therefore not
   available in the vorticity ledger.  Pressure remains nonlocal in a strain
   ledger, where the R0.70L sign obstruction still applies.

The result is not a regularity proof.  It closes the heat *bulk* from the
standard energy budget and shows that the unresolved object is a signed
bottom-trace concentration, not another omitted pressure term.

## 2. Normalization and frame

Work on

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3
\]

with normalized spatial average.  Let \(u\) have zero spatial mean and solve

\[
 \partial_tu+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u.
 \tag{2.1}
\]

Let \((T_j)_j\) be a real-even scalar tight frame with multipliers
\(m_j(k)\):

\[
 \sum_j|m_j(k)|^2=1\qquad(k\ne0).
 \tag{2.2}
\]

Set

\[
 A_{j,s}=e^{s\Delta}T_j,
 \qquad W_{j,s}=A_{j,s}\omega,
 \qquad D_{j,s}=\|\nabla W_{j,s}\|_2^2.
 \tag{2.3}
\]

Because \(W_{j,s}\) is divergence free,

\[
 D_{j,s}=\|\nabla\times W_{j,s}\|_2^2.
 \tag{2.4}
\]

The operator \((-\Delta)^{-1/2}\) is set to zero on the zero Fourier mode.

## 3. Exact projected-Lamb compression

Put

\[
 B=p+\frac12|u|^2,
 \qquad
 L=\mathbb P(u\times\omega).
 \tag{3.1}
\]

The rotational form of the momentum equation gives

\[
 \boxed{
 u\times\omega=L+\nabla B,
 \qquad
 L=\partial_tu-\nu\Delta u
   =-\mathbb P\nabla\cdot(u\otimes u).}
 \tag{3.2}
\]

Taking curl removes the Bernoulli gradient:

\[
 \partial_t\omega-\nu\Delta\omega
 =\nabla\times L
 =S\omega-u\cdot\nabla\omega,
 \tag{3.3}
\]

where \(S=(\nabla u+\nabla u^T)/2\).  Hence the heat extension obeys

\[
 \boxed{
 (\partial_t-\nu\partial_s)W_{j,s}
 =\nabla\times(A_{j,s}L).}
 \tag{3.4}
\]

The R0.71D material form is equivalent.  Indeed,

\[
 A_{j,s}(S\omega)+[u\cdot\nabla,A_{j,s}]\omega
 =u\cdot\nabla W_{j,s}+\nabla\times(A_{j,s}L).
 \tag{3.5}
\]

After global pairing with \(W_{j,s}\), the advection term vanishes.  Thus the
complete shell injection is

\[
 \boxed{
 \begin{aligned}
 b_{j,s}
 &:=\langle W_{j,s},A_{j,s}(S\omega-u\cdot\nabla\omega)\rangle\\
 &=\langle W_{j,s},
 A_{j,s}(S\omega)+[u\cdot\nabla,A_{j,s}]\omega\rangle\\
 &=\langle\nabla\times W_{j,s},A_{j,s}L\rangle .
 \end{aligned}}
 \tag{3.6}
\]

This is the first main correction to the proposed three-sector ledger:
pressure is already the gradient complement in (3.2).  Adding a separate
pressure work to (3.6) would double count the momentum decomposition.

The projection idea itself is not new.  Solenoidal Lamb-vector decompositions
appear in [Speziale 1987](https://ntrs.nasa.gov/citations/19880002646),
[Shtilman 1992](https://doi.org/10.1063/1.858488), and
[Iyer--Sreenivasan--Yeung 2022](https://doi.org/10.1017/jfm.2021.914).
[Lerner--Vigneron 2022](https://arxiv.org/abs/2203.07950) explicitly writes
the Navier--Stokes nonlinearity modulo gradients using the Leray projection.
R0.71E uses that established structure to audit the specific signed heat
coefficient left by R0.71C.

## 4. The localized projected-Lamb heat ledger

Let \(I=[t_0,t_1]\), \(0<s<h\), and let \(\phi(t,x,s)\) be smooth.  Write

\[
 e_{j,s}=\frac12|W_{j,s}|^2,
 \qquad E_\phi(t,s)=\int\phi e_{j,s}\,dx.
 \tag{4.1}
\]

Multiplying (3.4) by \(\phi W_{j,s}\) and integrating by parts in \(t,s,x\)
gives

\[
 \boxed{
 \begin{aligned}
 &\int_0^h[E_\phi(t_1,s)-E_\phi(t_0,s)]\,ds
 +\nu\int_I[E_\phi(t,0)-E_\phi(t,h)]\,dt\\
 &=\iiint
 \left\{
 \phi(\nabla\times W_{j,s})\cdot A_{j,s}L
 +A_{j,s}L\cdot(\nabla\phi\times W_{j,s})
 +e_{j,s}(\partial_t-\nu\partial_s)\phi
 \right\}.
 \end{aligned}}
 \tag{4.2}
\]

The second term on the right is the cutoff--curl boundary ledger.  It does
not have a universal sign.  If

\[
 (\partial_t+V_j\cdot\nabla-\nu\partial_s)\phi=R_{\rm shape},
 \tag{4.3}
\]

then the last term in (4.2) is exactly

\[
 e_{j,s}(R_{\rm shape}-V_j\cdot\nabla\phi).
 \tag{4.4}
\]

Flow adaptation moves the cutoff cost; it does not erase the nonlocal Lamb
boundary term.

There is nevertheless a local packing estimate at each fixed \((t,s,j)\).
For a nonnegative smooth partition \((\phi_Q)_Q\), define the complete local
Lamb work and its stabilized denominator by

\[
 B_Q^L
 =\langle A_{j,s}L,\nabla\times(\phi_QW_{j,s})\rangle,
 \qquad
 d_Q^{\rm loc}
 =\|\nabla\times(\phi_QW_{j,s})\|_2^2.
 \tag{4.5}
\]

Then

\[
 \frac{((B_Q^L)^+)^2}{d_Q^{\rm loc}}
 \le\|1_{\operatorname{supp}\phi_Q}A_{j,s}L\|_2^2.
 \tag{4.6}
\]

Here the quotient is taken only when \(d_Q^{\rm loc}>0\), and is set to zero
otherwise.  Assume the supports and collars overlap at most \(N\) times and
that \(|\nabla\phi_Q|\le C/r\) on the collars.  Summing (4.6) then costs only
the overlap constant.  Also

\[
 \sum_Qd_Q^{\rm loc}
 \lesssim
 \int|\nabla\times W_{j,s}|^2
 +r^{-2}\int_{\rm collars}|W_{j,s}|^2.
 \tag{4.7}
\]

Thus the projected-Lamb part admits a genuine local packing bound, but the
denominator is stabilized palinstrophy and the moving-geometry term in
(4.4) remains separate.  Comparing (4.7) back to the original R0.71C
denominator requires a valid Bernstein/collar estimate; it cannot be assumed.

There is a useful consistency check.  If one replaces \(A_{j,s}L\) in
(4.2) by \(A_{j,s}(u\times\omega)-\nabla A_{j,s}B\), the two apparent
Bernoulli contributions satisfy

\[
 \int\phi\nabla A_{j,s}B\cdot\nabla\times W_{j,s}
 +\int\nabla A_{j,s}B\cdot(\nabla\phi\times W_{j,s})=0.
 \tag{4.8}
\]

Thus pressure does not furnish an additional local vorticity sign.  It is
part of the Hodge representation of the same boundary ledger.

## 5. An unconditional heat-bulk estimate

Define

\[
 \Theta_s^2
 =\sum_{D_{j,s}>0}\frac{(b_{j,s}^+)^2}{D_{j,s}}.
 \tag{5.1}
\]

Shellwise Cauchy and (2.4) give

\[
 \frac{(b_{j,s}^+)^2}{D_{j,s}}
 \le \|A_{j,s}L\|_2^2.
 \tag{5.2}
\]

The tight-frame identity then yields

\[
 \boxed{
 \Theta_s^2\le\sum_j\|A_{j,s}L\|_2^2
 =\|e^{s\Delta}L\|_2^2.}
 \tag{5.3}
\]

Since \(L\) has zero mean,

\[
 \int_0^\infty\|e^{s\Delta}L\|_2^2\,ds
 =\frac12\|(-\Delta)^{-1/2}L\|_2^2.
 \tag{5.4}
\]

Moreover, the Fourier multiplier

\[
 (-\Delta)^{-1/2}\mathbb P\nabla\cdot
 \tag{5.5}
\]

has \(L^2\) operator norm at most one from matrix fields with Frobenius norm
to vector fields.  From (3.2),

\[
 \|(-\Delta)^{-1/2}L\|_2
 \le\|u\otimes u\|_2=\|u\|_4^2.
 \tag{5.6}
\]

Combining (5.3)--(5.6) proves

\[
 \boxed{
 \int_0^\infty\Theta_s^2\,ds
 \le\frac12\|(-\Delta)^{-1/2}L\|_2^2
 \le\frac12\|u\|_4^4.}
 \tag{5.7}
\]

The factor \(1/2\) in the first inequality is exact because

\[
 \int_0^\infty e^{-2s|k|^2}\,ds=\frac1{2|k|^2}.
 \tag{5.8}
\]

## 6. The normalized bulk is forced by Leray energy

Put

\[
 Y(t)=\|\omega(t)\|_2^2=\|\nabla u(t)\|_2^2
 \tag{6.1}
\]

and, when \(Y(t)>0\), define

\[
 \boxed{
 \mathcal V(t)
 =\frac1{Y(t)}\int_0^\infty\Theta_s(t)^2\,ds.}
 \tag{6.2}
\]

Set \(\mathcal V=0\) when \(Y=0\).  Interpolation and Sobolev give

\[
 \|u\|_4^4\le\|u\|_2\|u\|_6^3
 \le C_S^3\|u\|_2Y^{3/2}.
 \tag{6.3}
\]

Consequently,

\[
 \boxed{
 \mathcal V(t)
 \le\frac{C_S^3}{2}\|u(t)\|_2Y(t)^{1/2}.}
 \tag{6.4}
\]

For a Leray--Hopf solution,

\[
 \|u(t)\|_2\le\|u_0\|_2,
 \qquad
 \nu\int_0^TY(t)\,dt\le\frac12\|u_0\|_2^2.
 \tag{6.5}
\]

Therefore, for every finite \(T\),

\[
 \boxed{
 \int_0^T\mathcal V(t)\,dt
 \le
 \frac{C_S^3}{2\sqrt{2\nu}}
 \|u_0\|_2^2\sqrt T<\infty.}
 \tag{6.6}
\]

This is the positive theorem of R0.71E.  It is unconditional at the standard
energy level and is not a disguised enstrophy-supremum assumption.

For a Leray--Hopf solution the assertion is understood at almost every time.
At such a time \(u(t)\in H^1\), hence \(u\otimes u\in L^2\) and
\(L=-\mathbb P\nabla\cdot(u\otimes u)\in\dot H^{-1}\).  For \(s>0\) the
heat-filtered terms are legitimate in \(L^2\); pointwise Cauchy followed by
Tonelli, or equivalently finite truncation followed by Fatou, gives (5.7).
The fully localized identity (4.2) is
stated only on smooth or strong intervals; no unsuitable test function is
inserted into a weak formulation.

## 7. Why this does not yet continue the solution

On a smooth or strong-solution interval, at times with \(Y(t)>0\), the
bottom value \(s=0\) in (5.1) defines exactly the R0.71C shell coefficient:

\[
 A_{\rm sb,+}(t)=\frac{\Theta_0(t)^2}{Y(t)}.
 \tag{7.1}
\]

Set \(A_{\rm sb,+}=0\) when \(Y=0\).  Under the zero-mean normalization,
\(Y=0\) forces \(u=0\), hence \(L=0\) and \(\Theta_s=0\).

R0.71C proves continuation if

\[
 \int_0^{T_*}A_{\rm sb,+}(t)\,dt<\infty.
 \tag{7.2}
\]

The energy theorem (6.6) controls a vertical integral, not its bottom trace.
To display the missing quantity, define, on the same smooth or strong interval,

\[
 \Lambda_L^2(t)
 =\frac{\Theta_0(t)^2}
 {\displaystyle\int_0^\infty\Theta_s(t)^2\,ds}
 \tag{7.3}
\]

when the denominator is positive, and set it to zero otherwise.  Then

\[
 \boxed{A_{\rm sb,+}=\Lambda_L^2\mathcal V.}
 \tag{7.4}
\]

The quantity \(\Lambda_L\) is an effective signed Lamb trace wavenumber.  It
has the correct frequency scaling.  Equation (6.6) controls \(\mathcal V\)
but gives no bound, integrability, or negative correlation for
\(\Lambda_L^2\).  Formula (7.4) is a diagnosis of the gap, not a new
criterion: assuming its right side integrable simply restates (7.2).

## 8. A support-minimal exact NSE witness

For \(\sigma\in\{-1,1\}\), \(a>0\), and integer \(K\ge1\), set

\[
 \boxed{
 u_{\sigma,a,K}(x)
 =aK\left(
 0,
 -2\cos(Kx_1),
 2\sigma\sin(Kx_1+Kx_2)-2\cos(Kx_2)
 \right).}
 \tag{8.1}
\]

It is real, zero mean, divergence free, and independent of \(x_3\).  Its
vorticity is

\[
 \omega_{\sigma,a,K}
 =2aK^2\left(
 \sigma\cos(Kx_1+Kx_2)+\sin(Kx_2),
 -\sigma\cos(Kx_1+Kx_2),
 \sin(Kx_1)
 \right).
 \tag{8.2}
\]

The positive-frequency representatives and velocity coefficients at
\(a=K=1\) are

\[
 \begin{array}{c|c}
 k=(1,0,0)&(0,-1,0)\\
 p=(0,1,0)&(0,0,-1)\\
 q=(-1,-1,0)&(0,0,\sigma i).
 \end{array}
 \tag{8.3}
\]

They satisfy \(k+p+q=0\), and the negative coefficients are their complex
conjugates.  Exact normalized averages give

\[
 \|u\|_2^2=6a^2K^2,
 \qquad
 Y=8a^2K^4,
 \qquad
 D=12a^2K^6.
 \tag{8.4}
\]

The complete nonlinear enstrophy work, resolved by output radius, is

\[
 \begin{array}{c|ccc}
 \text{output radius}
 &\text{stretching}&\text{transport}&\text{combined}\\ \hline
 K&0&2\sigma a^3K^6&-2\sigma a^3K^6\\
 \sqrt2K&2\sigma a^3K^6&-2\sigma a^3K^6&4\sigma a^3K^6.
 \end{array}
 \tag{8.5}
\]

Thus the total transport vanishes, while

\[
 \langle\omega,S\omega-u\cdot\nabla\omega\rangle
 =2\sigma a^3K^6.
 \tag{8.6}
\]

The two phases have identical quadratic norms and opposite cubic work.

This six-mode support is minimal in a simple resonance sense.  A real
zero-mean field with fewer than three conjugate Fourier pairs has at most two
frequency directions.  A cubic zero-frequency resonance among two pairs
forces the wavevectors to be collinear, and incompressibility then makes the
corresponding transport nonlinearity vanish.  The certificate checks the
minimal six-mode construction; it does not claim uniqueness.

The datum is not merely kinematic.  It is a 2D3C field.  Its horizontal
velocity is an exact decaying two-dimensional shear, while its third
component solves a linear advection--diffusion equation driven by that
shear.  It therefore generates a global smooth three-dimensional periodic
NSE solution.  This regularity is precisely why the datum is only a trace
and criticality obstruction, not evidence for blow-up.

## 9. Stretching and commutator must be combined

Let a real-even radial block have multiplier value \(\alpha\) at radius
\(K\) and \(\beta\) at radius \(\sqrt2K\).  The producer obtains

\[
 \begin{aligned}
 Y_T&=4a^2K^4(\alpha^2+\beta^2),\\
 D_T&=4a^2K^6(\alpha^2+2\beta^2),\\
 b_T^{\rm stretch}&=2\sigma a^3K^6\beta^2,\\
 b_T^{\rm comm}&=2\sigma a^3K^6(\beta^2-\alpha^2),\\
 \boxed{b_T=2\sigma a^3K^6(2\beta^2-\alpha^2).}
 \end{aligned}
 \tag{9.1}
\]

At heat height \(s\), with \(\tau=K^2s\),

\[
 \begin{aligned}
 b_T(s)
 &=2\sigma a^3K^6
 \left(2\beta^2e^{-4\tau}-\alpha^2e^{-2\tau}\right),\\
 D_T(s)
 &=4a^2K^6
 \left(\alpha^2e^{-2\tau}+2\beta^2e^{-4\tau}\right).
 \end{aligned}
 \tag{9.2}
\]

Neither the stretching term nor the commutator alone gives the correct
shell injection.  Formula (9.1) is an exact finite demonstration of the
compression in Section 3.

## 10. The exact two-derivative trace cost

A fixed smooth radial tight frame with the needed values can be constructed
in the logarithmic radius \(\rho=\log_2|\xi|\).  Start with a smooth square
partition

\[
 \sum_{j\in\mathbb Z}m(\rho-j)^2=1
 \tag{10.1}
\]

whose base function has a flat top \(m=1\) on \([0,1/2]\).  One standard
construction joins adjacent translates by a flat smooth sine--cosine
transition.  Explicitly, choose a smooth \(\eta:[0,1]\to[0,\pi/2]\) with
\(\eta(0)=0\), \(\eta(1)=\pi/2\), and all one-sided derivatives zero at both
endpoints; put
\(m(\rho)=\sin\eta(2\rho+1)\) on \([-1/2,0]\), set \(m=1\) on
\([0,1/2]\), put \(m(\rho)=\cos\eta(2\rho-1)\) on \([1/2,1]\), and set it
to zero outside.  Adjacent transition squares add to one.  Set
\(m_j(|\xi|)=m(\log_2|\xi|-j)\).  For every \(K=2^j\), \(j\ge0\), the
same parent is one at both \(K\) and \(\sqrt2K\), while all other parents
vanish at those two radii.

Now split every parent by the same smooth function \(\vartheta\):

\[
 m_{j,{\rm lo}}=m_j\cos\vartheta(\rho-j),
 \qquad
 m_{j,{\rm hi}}=m_j\sin\vartheta(\rho-j),
 \tag{10.2}
\]

where \(\vartheta(0)=0\) and \(\vartheta(1/2)=\pi/2\).  This preserves
\(m_{j,{\rm lo}}^2+m_{j,{\rm hi}}^2=m_j^2\) and separates the two radii
exactly.  It is one dyadically covariant frame fixed before the data, not a
frame retuned for each \(K\).

Choose \(\sigma=-1\).  The low-radius subblock has positive injection, while
the high-radius subblock has negative injection.  Thus the positive-square
ledger consists of the low block alone:

\[
 \begin{aligned}
 b_{\rm lo}(s)&=2a^3K^6e^{-2K^2s},\\
 D_{\rm lo}(s)&=4a^2K^6e^{-2K^2s},\\
 q_{\rm lo}(s)
 :=\frac{(b_{\rm lo}(s)^+)^2}{D_{\rm lo}(s)}
 &=a^4K^6e^{-2K^2s}.
 \end{aligned}
 \tag{10.3}
\]

Consequently,

\[
 \boxed{
 q_{\rm lo}(0)
 =2K^2\int_0^\infty q_{\rm lo}(s)\,ds.}
 \tag{10.4}
\]

Using the physical bottom enstrophy \(Y=8a^2K^4\),

\[
 \boxed{
 A_{\rm sb,+}(0)=\frac{a^2K^2}{8},
 \qquad
 \mathcal V(0)=\frac{a^2}{16},
 \qquad
 A_{\rm sb,+}(0)=2K^2\mathcal V(0).}
 \tag{10.5}
\]

On a finite heat box \(0<s<\theta/K^2\),

\[
 \boxed{
 \frac1Y\int_0^{\theta/K^2}q_{\rm lo}(s)\,ds
 =\frac{a^2}{16}(1-e^{-2\theta}),}
 \tag{10.6}
\]

which is independent of \(K\).  The bottom value grows like \(K^2\), while
the entire normalized heat bulk stays at order one.

### Theorem 10.1 — unconditional bulk closure with critical trace loss

For every mean-zero periodic Leray--Hopf solution and every tight real-even
scalar frame, (5.7) holds at almost every time in the heat-regularized
finite-truncation/Fatou sense, and (6.6) holds on every finite time interval.
There is also a smooth global 2D3C NSE family and one fixed admissible radial
tight-frame refinement for which (10.4)--(10.6) hold at the initial trace for
every dyadic integer \(K=2^j\), \(j\ge0\).

Therefore Leray energy closes the normalized vertical bulk, but no estimate
that recovers the R0.71C bottom coefficient from that bulk without paying a
full frequency-square trace cost can hold uniformly on this family.

**Proof.**  For smooth finite truncations, the first statement is (3.6),
shellwise Cauchy, the tight-frame identity, the heat spectral integral, and
the order-zero estimate (5.6), followed by (6.3)--(6.6).  At almost every
Leray--Hopf time, finite shell and heat-height truncation followed by Tonelli
and Fatou gives the stated interpretation; the energy inequality supplies
(6.6).  For the second statement, the exact Fourier convolution table gives
(8.5) and (9.1).  The radial split and \(\sigma=-1\) leave only the positive
low block.  Direct substitution gives (10.3), and integrating the exponential
gives (10.4)--(10.6).  The independent checker reconstructs the same values
from the trigonometric field without importing the Fourier producer.
\(\square\)

The theorem does **not** rule out a nonlinear depletion estimate that
controls \(\Lambda_L\), a solution-dependent signed trace theorem, or a
local Carleson mechanism with additional NSE structure.  It rules out only
the free bottom-trace upgrade from the energy-controlled heat bulk.

## 11. Pressure and the strain ledger

Pressure is absent from (3.4), but it is present if one separately evolves
the filtered strain.  With

\[
 U=A_{j,s}u,
 \qquad \Sigma=A_{j,s}S,
 \qquad P=A_{j,s}p,
 \tag{11.1}
\]

the localized pressure-Hessian pairing has the exact boundary form

\[
 \boxed{
 -\int\phi\,\Sigma:\nabla^2P
 =-\int\left[(\Delta P)U\cdot\nabla\phi
 +U_i(\partial_kP)(\partial_{ik}\phi)\right].}
 \tag{11.2}
\]

Filtering also creates the subgrid tensor

\[
 \tau=A_{j,s}(u\otimes u)-U\otimes U.
 \tag{11.3}
\]

The compatible Hodge identity is

\[
 |\Sigma|^2-\frac12|\nabla\times U|^2
 =-\Delta P-\partial_i\partial_a\tau_{ia}.
 \tag{11.4}
\]

Thus filtered pressure alone is representation dependent; pressure and SGS
must be kept together.  R0.70L already gives local states with identical
vorticity/strain data and opposite pressure-driven strain production.  No
universal local pressure compensation can be inserted into (10.4).

## 12. An independent whole-space scaling check

The trace gap is also consistent with the whole-space NSE scaling.  Choose a
smooth compact cutoff \(\chi\) that equals one near the origin and set

\[
 \psi=\chi(x)(x_1x_2+x_1x_3),
 \qquad
 u_0=\nabla\times(0,0,\psi).
 \tag{12.1}
\]

Near the origin,

\[
 u_0=(x_1,-x_2-x_3,0),
 \qquad \omega_0=(1,0,0),
 \tag{12.2}
\]

and

\[
 (\omega_0\cdot\nabla)u_0-(u_0\cdot\nabla)\omega_0=(1,0,0).
 \tag{12.3}
\]

Hence \(\mathbb P(u_0\times\omega_0)\ne0\); otherwise its curl would vanish.
For

\[
 u_{0,\lambda}(x)=\lambda u_0(\lambda x)
 \tag{12.4}
\]

on \(\mathbb R^3\),

\[
 \|u_{0,\lambda}\|_2^2=\lambda^{-1}\|u_0\|_2^2,
 \quad
 \|\omega_{0,\lambda}\|_2^2=\lambda\|\omega_0\|_2^2,
 \quad
 \|L_{0,\lambda}\|_2^2=\lambda^3\|L_0\|_2^2.
 \tag{12.5}
\]

Thus \(\|L\|_2^2/Y\) scales like \(\lambda^2\), while the kinetic energy
can tend to zero.  This is a family of different smooth initial data, not a
blow-up sequence for one solution.  It rules out an energy-only upper bound
for this quotient whose right side remains bounded as the kinetic energy
tends to zero.  It does not rule out an arbitrary energy function that is
allowed to diverge at zero.

## 13. Literature boundary

A bounded primary-source audit found no theorem deriving the missing signed
bottom trace, its flow-adapted Carleson vanishing, or the required
stretching--commutator--localization summability from standard NSE budgets.
This is a search result, not a proof of nonexistence or a priority claim.

The nearest 2026 preprint located was [Yu, *Filtered Vortex Stretching and
Subgrid Defects*](https://arxiv.org/html/2606.27560).  Its near-field
stretching estimate is substantial, but the final unweighted summation and
defect vanishing assume summability of the far field, commutator surrogate,
and remaining shell/localization budgets.  It uses fixed parabolic cylinders,
and curl removes pressure from its vorticity equation.

Other adjacent results divide into separate modules:

- [Yang 2020](https://arxiv.org/abs/2008.05588) and
  [Vasseur--Yang 2020](https://arxiv.org/abs/2009.14291) provide rigorous
  skewed-cylinder geometry, but not the signed filtered Lamb trace.
- [Constantin--Fefferman 1993](https://doi.org/10.1512/iumj.1993.42.42034)
  and later vorticity-direction criteria obtain depletion under additional
  geometric assumptions, not from Leray energy alone.
- [Koch--Tataru 2001](https://doi.org/10.1006/aima.2000.1937) gives a genuine
  heat-extension Carleson norm for small \(BMO^{-1}\) data, but it is a
  fixed-tent small-data theorem and its square function is sign blind.
- [Cheskidov--Shvydkoy 2011](https://arxiv.org/abs/1102.1944) proves that the
  dissipation wavenumber is unconditionally in \(L^1_t\), while regularity
  follows from \(L^{5/2}_t\).  This is a useful comparison for the unresolved
  frequency-square concentration in (7.3).
- [Duchon--Robert 2000](https://doi.org/10.1088/0951-7715/13/1/312) shows how
  an exact commutator defect enters a local energy equation, but an identity
  and a sign do not by themselves imply defect vanishing.

The literature therefore supports the separation made here: projected Lamb
compression is established structure; the exact R0.71C heat-bulk quotient
has no isomorphic theorem in the bounded search, but no novelty claim is
made; and no existing theorem found in that search closes its bottom trace.

## 14. Claim ledger and next gate

| Item | R0.71E status |
|---|---|
| Projected-Lamb/Hodge representation | Established structure, rederived exactly |
| Complete global shell injection (3.6) | Exact identity |
| Localized heat ledger (4.2) | Exact identity |
| Heat-bulk estimate (5.7) | Exact theorem |
| Normalized bulk \(\mathcal V\in L^1_t\) from Leray energy | Unconditional positive result |
| Bottom coefficient \(A_{\rm sb,+}\in L^1_t\) | Not proved |
| Two-frequency trace factor \(2K^2\) | Exact smooth NSE obstruction |
| Universal beneficial pressure sign | Rejected as an independent vorticity sector |
| Global regularity or singularity | Not obtained |

### Next justified gate: R0.71F

The next question is no longer whether the omitted heat bulk or pressure term
closes the estimate.  It is whether NSE dynamics independently constrain the
vertical concentration \(\Lambda_L\), or a localized analogue, below the
known BMO/Besov/BKM side of the problem.

The first admissible test should be a **localized projected-Lamb trace
criterion** on mollified-flow skewed cylinders.  It must:

1. retain the cutoff--curl boundary term in (4.2);
2. keep pressure and SGS representation consistent if a strain ledger is
   added;
3. prove, rather than assume, the required Carleson or shell summability;
4. compare logically with Serrin, \(BMO^{-1}\), Besov, and dissipation-
   wavenumber criteria;
5. reject the branch if the trace estimate merely restates
   \(A_{\rm sb,+}\in L^1_t\).

That is a smaller and more precise target than the original three-sector
proposal.  R0.71E has supplied one unconditional half of the factorization
(7.4); R0.71F must decide whether the other half contains genuine NSE
depletion or only another form of the regularity problem.
