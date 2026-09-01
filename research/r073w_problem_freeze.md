# R0.73W problem freeze: signed production on the heat plane

**Frozen date:** 2026-09-01

**Status:** problem freeze complete; this file alone does not license a public
release

**Domain:** the normalized periodic torus \(\mathbb T^3=[0,2\pi]^3\),
viscosity \(\nu>0\), and a smooth real mean-zero divergence-free
Navier--Stokes solution on its smooth lifespan

**Dependency:** R0.73V, especially the exact trace equation and the unresolved
signed production term

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. Frozen object and sign convention

Let

\[
 P_s=e^{s\Delta},\qquad v_s=P_su,\qquad
 \tau_s=P_s(u\otimes u)-v_s\otimes v_s,
\tag{1.1}
\]

and put

\[
 S_s={1\over2}(\nabla v_s+\nabla v_s^T),\qquad
 \Pi_s=-\tau_s:\nabla v_s=-\tau_s:S_s.
\tag{1.2}
\]

With this sign, positive \(\Pi_s\) removes energy from the resolved field in
the local filtered-energy equation.  Every sign in the analytic and finite
gates must be checked against (1.2); a turbulence source using the opposite
stress convention is not interchangeable without conversion.

## 2. Questions fixed for this section

R0.73W has five narrow questions.

1. Does the Gaussian heat covariance give an exact scale representation of
   \(\Pi_s\), and which part of the positive covariance survives contraction
   with the incompressible strain?
2. Can physical viscosity pay for the signed production after space--time
   integration along a characteristic in the \((t,s)\) plane?
3. What absolute estimate for \(\Pi_s\) follows from the Leray--Hopf energy
   class alone, without assuming a Serrin norm or a higher derivative?
4. Is there a universal pointwise sign, mean sign, or amplitude-independent
   same-time absorption by the positive quadratic viscous covariance row?
5. After the third central flux is separated as a spatial divergence, what is
   the remaining signed increment functional, and what does the critical
   heat-scale weight \(s^{-1/2}\) recover?

The section is successful if it proves a useful exact identity or a rigorous
energy-class bound and closes false sign or absorption routes by an exact
finite witness.  It need not produce a regularity theorem.

## 3. Exact claims to audit

The analytic gate must establish the following claims.

1. The heat covariance solves
   \[
   (\partial_s-\Delta)\tau_{ij,s}
   =2\partial_\ell v_{s,i}\partial_\ell v_{s,j},\qquad \tau_{ij,0}=0,
   \tag{3.1}
   \]
   and therefore has the exact Duhamel representation
   \[
   \tau_{ij,s}=2\int_0^sP_{s-r}
   (\partial_\ell v_{r,i}\partial_\ell v_{r,j})\,dr.
   \tag{3.2}
   \]
2. Since \(\operatorname{tr}S_s=0\), only the deviatoric part of (3.2)
   contributes to \(\Pi_s\).  Positivity of \(\tau_s\) alone gives no sign.
3. For \(e_s=|v_s|^2/2\),
   \[
   \boxed{
   (\partial_t-\nu\partial_s)e_s+
   \nabla\!\cdot\!\left[((e_s+p_s)v_s)+\tau_sv_s\right]
   =-\Pi_s.}
   \tag{3.3}
   \]
   Hence the spatial mean of \(\Pi_s\) is an exact energy derivative along
   characteristics \(s'(t)=-\nu\).
4. For every finite time interval \(I\) and \(0<s\le1\), the energy class
   gives
   \[
   \|\Pi_s\|_{L^1(I\times\mathbb T^3)}
   \le C s^{-1/4}
   \|u\|_{L_t^\infty L_x^2(I)}
   \|\nabla u\|_{L^2(I\times\mathbb T^3)}^2.
   \tag{3.4}
   \]
   The bound is integrable in \(s\), but it is not uniform as \(s\downarrow0\).
5. The smooth finite Fourier field frozen in Section 4 gives both signs of
   the spatially averaged production and makes the ratio to the quadratic
   viscous covariance arbitrarily large under amplitude scaling.
6. With \(K_{j,s}=\kappa_{iij,s}/2\), production has the exact centered
   increment split
   \[
   \Pi_s=\partial_jK_{j,s}+\mathscr S_s,
   \qquad
   \mathscr S_s={1\over4s}\int_{\mathbb R^3}
   y\cdot a_s(x,y)|a_s(x,y)|^2g_s(y)\,dy,
   \tag{3.5}
   \]
   where \(a_s(x,y)=u(x-y)-v_s(x)\).  Substitution into the exact trace
   equation cancels \(K_s\), leaving the pressure flux, nonnegative gradient
   covariance, and the single signed remainder \(\mathscr S_s\).
7. For \(L=-\Delta\), \(h=(u\cdot\nabla)u\), and mean-zero \(u\),
   \[
   \int_0^\infty s^{-1/2}\langle\Pi_s\rangle\,ds
   =\sqrt{\pi/2}\,\langle L^{-1/2}u,h\rangle.
   \tag{3.6}
   \]
   This critical scale average reduces to a classical zero-order Riesz
   trilinear form and does not give arbitrary-energy coercivity.

## 4. Frozen exact finite witness

On the normalized torus define the rank-three Fourier-support field

\[
 \begin{aligned}
 R(x,y,z)={}&\big(\cos(y+z)-\sin(x+y+z)+\cos(2z),\\
 &\qquad \cos x+\sin(x+y+z),\ 0\big),
 \qquad u_A=A R.
 \end{aligned}
\tag{4.1}
\]

This field is real, mean-zero, and divergence-free.  Its nonzero Fourier
support spans rank three over \(\mathbb Q\).  With \(q=e^{-s}\), the two
independent finite producers must verify coefficient by coefficient that

\[
 \langle\Pi_s(u_A)\rangle={A^3\over4}q^2(1-q^2),
\tag{4.2}
\]

\[
 \langle|\nabla R|^2\rangle={13\over2},\qquad
 \langle|\nabla v_s|^2\rangle
 =A^2\left({q^2\over2}+q^4+3q^6+2q^8\right),
\tag{4.3}
\]

and

\[
 \langle D_{ii,s}(u_A)\rangle
 ={A^2\over2}(1-q^2)
 (13+12q^2+10q^4+4q^6).
\tag{4.4}
\]

The producer pair must also verify that \(u_A\mapsto-u_A\) leaves
\(\tau_s\) and \(D_{ii,s}\) unchanged while reversing \(S_s\) and \(\Pi_s\).
The finite result is a counterexample to the declared universal sign and
same-time quadratic absorption statements.  A rank-two three-coordinate
triad and a 2D3C field remain in the package as diagnostic cross-checks.  The
result is not a minimal-support claim, a genericity claim, a numerical
simulation, or a regularity result.

## 5. Literature and priority boundary

The Gaussian forced-diffusion equation for the subfilter stress, its exact
scale integral, and its strain--vorticity decomposition are established in
P. L. Johnson, *Physical Review Letters* **124** (2020), 104501.  The
deviatoric-stress interpretation and multiscale mechanism are developed
further in Johnson, *Journal of Fluid Mechanics* **922** (2021), A3.
These facts must be attributed rather than presented as new.

The filtered local-energy balance and sign-changing local transfer are also
standard parts of the LES/coarse-graining literature.  A bounded literature
search may fail to locate the precise heat-characteristic rewrite (3.3) or
the particular energy-class estimate (3.4); such a negative search is not a
novelty proof.  Public prose may call them the current section's synthesis or
estimate, not a first result.

## 6. Explicit non-claims

R0.73W does not claim any of the following:

- a proof or substantial partial solution of the Clay problem;
- pointwise positivity, mean positivity, or monotonicity of \(\Pi_s\);
- an \(s\)-uniform energy-class bound for \(|\Pi_s|\);
- a same-time coercive absorption of the cubic production by a quadratic
  viscous covariance with an amplitude-independent constant;
- novelty of the Gaussian stress representation;
- that the finite witness is a blow-up candidate or representative of generic
  turbulent data.

## 7. Release gate and next interface

Publication requires a parent proof, independent sign/index audit, two
independent exact finite producers, primary-source collision audit, formal
figure package, synchronized HTML/PDF, cumulative recap, local direct
translation, and the full GitHub Pages gate.

If these checks pass, R0.73X should ask whether a localized version of the
heat-characteristic identity yields a genuinely scale-critical tent-space or
Carleson-type control.  The next section must keep the divergence and cutoff
commutators visible; it may not replace the signed flux by its spatial mean.
