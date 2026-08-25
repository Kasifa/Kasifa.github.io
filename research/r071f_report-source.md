# R0.71F — Skewed-cylinder localization preserves heat packing but not the bottom trace

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, vorticity stretching, localized Littlewood--Paley
estimates, skewed cylinders, and heat-extension trace methods

**Status:** exact moving-cutoff identities, a localized conditional
continuation criterion, exact bounded-overlap heat-moment packing with
Leray-level finiteness at \(\alpha=1\), an exact local cutoff witness from a
true global-smooth 2D3C solution, a
scale-covariant interior-cylinder no-go, and two independent finite
certificates; no unconditional regularity theorem, no singularity
construction, no novelty theorem, and no Millennium-problem claim

## 1. Direct decision

R0.71E proved that Leray energy controls the vertical heat bulk of the
projected-Lamb quotient but not its value at heat height \(s=0\).  R0.71F
tests whether localization along mollified-flow skewed cylinders supplies the
missing trace gain.

It does not.  The result has a positive half and a sharp negative half.

1. For every smooth moving cutoff, the projected-Lamb heat equation has a
   complete local ledger.  It contains the time faces, both heat-height
   faces, the cutoff--curl term, the transport/shape term, and the viscous
   collar.  The projected and material representations are exactly
   equivalent; their apparent boundary errors cannot be counted twice.
2. For a matched dyadic spatial partition, the stabilized local positive
   quotient gives a valid continuation criterion.  Bounded overlap also
   gives the unconditional heat packing

   \[
     \sum_{j,Q}q_{j,Q}(t,s)
     \le N\|e^{s\Delta}L(t)\|_2^2.
     \tag{1.1}
   \]

   Its normalized \(s\)-integral is forced into \(L_t^1\) by the Leray
   energy inequality.
3. More generally, for every \(\alpha>0\),

   \[
    \int_0^\infty s^{\alpha-1}
    \sum_{j,Q}q_{j,Q}(t,s)\,ds
    \le
    \frac{N\Gamma(\alpha)}{2^\alpha}
    \|(-\Delta)^{-\alpha/2}L(t)\|_2^2.
    \tag{1.2}
   \]

   The energy endpoint is \(\alpha=1\).  Reaching the bottom trace costs the
   missing frequency square.
4. The loss persists after genuine localization.  For the fixed dyadic
   frame and the true global-smooth 2D3C family from R0.71E, every nonzero
   smooth cutoff \(\phi\ge0\) gives

   \[
    B_\phi(s)
    =4a^3K^6e^{-2K^2s}
      \int\phi(x)\sin^2(Kx_2)\,dx>0,
    \tag{1.3}
   \]

   with the complete cutoff--curl term included.  Hence

   \[
    q_\phi(0)
    =\frac{2K^2}{1-e^{-2K^2h}}
      \int_0^h q_\phi(s)\,ds.
    \tag{1.4}
   \]

5. At the matched parabolic height \(h=\theta K^{-2}\), (1.4) is a
   critical \(K^2\simeq h^{-1}\) estimate.  It does not disprove such an
   estimate; it proves that the factor cannot be removed or replaced by a
   subcritical one.  The resulting scale-normalized average is a fixed
   fraction of the bottom value, not a vanishing gain.
6. A bounded-overlap partition at radius \(r\simeq K^{-1}\) cannot hide the
   low-block obstruction.  Its low-block aggregate bottom quotient is
   comparable to \(a^4K^6\), with constants fixed by the partition geometry.
   With \(a=K^{-1}\), the kinetic energy stays fixed, the
   normalized low-block bottom coefficient stays bounded away from zero, and
   its corresponding heat bulk tends to zero like \(K^{-2}\).
7. Skewed-cylinder geometry remains useful for covering and local-to-global
   arguments.  It does not regularize the independent heat-height variable.
   For the covariant one-block frame, a scale-covariant interior-cylinder
   construction rules out every pure multiplicative bottom-from-bulk factor
   \(o(r^{-2})\) whose constant depends only on the uniform geometry and
   admissibility parameters.  The critical \(Cr^{-2}\) factor is saturated,
   not disproved.

The route decision is therefore negative but precise: bounded overlap closes
the local *bulk*, while the bottom trace remains a critical analytic input.
R0.71F does not infer that every possible nonlinear depletion mechanism
fails.  It rejects only the proposed free trace upgrade from flow-adapted
geometry and standard energy budgets.

## 2. Setup

Work first on

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3
\]

with normalized spatial average.  Let \(u\) be a zero-mean smooth solution on
an interval \(I=[t_-,t_+]\):

\[
 \partial_tu+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u.
 \tag{2.1}
\]

Set

\[
 L=\mathbb P(u\times\omega)
   =\partial_tu-\nu\Delta u
   =-\mathbb P\nabla\cdot(u\otimes u).
 \tag{2.2}
\]

Let \((T_j)_j\) be a real-even scalar tight frame, with the dyadic annular
support specified when a matched partition is used.  Define

\[
 A_{j,s}=e^{s\Delta}T_j,
 \qquad
 W_{j,s}=A_{j,s}\omega,
 \qquad
 F_{j,s}=A_{j,s}L.
 \tag{2.3}
\]

Then

\[
 \boxed{(\partial_t-\nu\partial_s)W_{j,s}
 =\nabla\times F_{j,s}.}
 \tag{2.4}
\]

Write \(e_{j,s}=|W_{j,s}|^2/2\).  Quotients with zero denominator are set to
zero.  I also use

\[
 Y(t)=\|\omega(t)\|_2^2,
 \qquad
 Y_{j,s}(t)=\|W_{j,s}(t)\|_2^2,
 \qquad
 D_{j,s}(t)=\|\nabla W_{j,s}(t)\|_2^2
            =\|\nabla\times W_{j,s}(t)\|_2^2.
 \tag{2.5}
\]

## 3. Complete ledger on a moving cutoff

Let \(0\le\chi_Q(t,x)\le1\) be a smooth spatial--temporal cutoff and let
\(0\le\zeta(s)\le1\) on \(0\le s\le h\).  Let \(V_r\) be a smooth
divergence-free mollified velocity and put

\[
 R_Q=(\partial_t+V_r\cdot\nabla)\chi_Q.
 \tag{3.1}
\]

Define the time faces

\[
 \mathcal T_Q
 =\int_0^h\zeta(s)
 \left[
  \int\chi_Q(t_+)e_{j,s}(t_+)
  -\int\chi_Q(t_-)e_{j,s}(t_-)
 \right]ds
 \tag{3.2}
\]

and the heat-height faces

\[
 \mathcal S_Q
 =\int_I
 \left[
  \zeta(0)\int\chi_Qe_{j,0}
  -\zeta(h)\int\chi_Qe_{j,h}
 \right]dt.
 \tag{3.3}
\]

Multiplying (2.4) by \(\chi_Q\zeta W_{j,s}\) and integrating in \(t,s,x\)
gives the exact identity

\[
 \boxed{
 \begin{aligned}
 \mathcal T_Q+\nu\mathcal S_Q
 ={}&\int_I\int_0^h\zeta(s)B_Q^L(t,s)\,dsdt\\
 &+\iiint\zeta e_{j,s}
       (R_Q-V_r\cdot\nabla\chi_Q)\\
 &-\nu\iiint e_{j,s}\chi_Q\zeta'(s),
 \end{aligned}}
 \tag{3.4}
\]

where the complete local Lamb work is

\[
 \boxed{
 B_Q^L
 =\langle F_{j,s},\nabla\times(\chi_QW_{j,s})\rangle.}
 \tag{3.5}
\]

Expanding (3.5) shows the two pieces that must remain together:

\[
 B_Q^L
 =\int\chi_QF_{j,s}\cdot\nabla\times W_{j,s}
  +\int F_{j,s}\cdot(\nabla\chi_Q\times W_{j,s}).
 \tag{3.6}
\]

The second term is the cutoff--curl collar.  It has no universal sign.

There is an equivalent dissipative form.  Since

\[
 \partial_se_{j,s}=\Delta e_{j,s}-|\nabla W_{j,s}|^2,
 \tag{3.7}
\]

the heat-height faces satisfy

\[
 \mathcal S_Q
 =\iiint
 \left[
  \zeta\chi_Q|\nabla W_{j,s}|^2
  -\zeta e_{j,s}\Delta\chi_Q
  -e_{j,s}\chi_Q\zeta'
 \right].
 \tag{3.8}
\]

Substitution into (3.4) cancels the two \(\zeta'\) terms exactly:

\[
 \boxed{
 \begin{aligned}
 \mathcal T_Q
 +\nu\iiint\zeta\chi_Q|\nabla W_{j,s}|^2
 ={}&\int_I\int_0^h\zeta B_Q^L\,dsdt\\
 &+\iiint\zeta e_{j,s}
       (R_Q-V_r\cdot\nabla\chi_Q)\\
 &+\nu\iiint\zeta e_{j,s}\Delta\chi_Q.
 \end{aligned}}
 \tag{3.9}
\]

Thus a heat taper does not create a new positive term.  It only moves the
same quantity between the \(s\)-faces and the bulk.

## 4. Projected and material ledgers are the same ledger

Define

\[
 G_{j,s}
 =A_{j,s}(S\omega)+[u\cdot\nabla,A_{j,s}]\omega.
 \tag{4.1}
\]

The material heat equation is

\[
 (\partial_t+u\cdot\nabla-\nu\partial_s)W_{j,s}=G_{j,s},
 \tag{4.2}
\]

and the projected-Lamb compression gives

\[
 G_{j,s}=u\cdot\nabla W_{j,s}+\nabla\times F_{j,s}.
 \tag{4.3}
\]

The material form of (3.4) is

\[
 \begin{aligned}
 \mathcal T_Q+\nu\mathcal S_Q
 ={}&\iiint\zeta\chi_QW_{j,s}\cdot G_{j,s}\\
 &+\iiint\zeta e_{j,s}
 \left[(u-V_r)\cdot\nabla\chi_Q+R_Q\right]\\
 &-\nu\iiint e_{j,s}\chi_Q\zeta'.
 \end{aligned}
 \tag{4.4}
\]

Indeed,

\[
 \int\chi_QW_{j,s}\cdot G_{j,s}
 =B_Q^L-\int e_{j,s}u\cdot\nabla\chi_Q.
 \tag{4.5}
\]

Equations (3.4) and (4.4) are therefore identical.  One may use the
projected cutoff--curl term or the material relative-transport term, but not
charge both as independent defects.

For a center-transported cutoff

\[
 \chi_Q(t,x)=\chi\!\left(\frac{x-X_Q(t)}r\right),
 \qquad X_Q'(t)=V_r(t,X_Q(t)),
 \tag{4.6}
\]

the shape residual is

\[
 R_Q
 =[V_r(t,x)-V_r(t,X_Q(t))]\cdot\nabla\chi_Q.
 \tag{4.7}
\]

It lives in the collar and costs the local variation of the mollified flow.
If the entire cutoff is transported by the \(V_r\)-flow, then \(R_Q=0\), but
the cutoff derivatives pay the flow-map distortion.  Neither construction
regularizes the independent heat-height variable.

## 5. Stabilized local quotient and continuation

At fixed \((t,s,j)\), define

\[
 d_{j,Q}(t,s)
 =\|\nabla\times(\chi_QW_{j,s})\|_2^2,
 \qquad
 q_{j,Q}(t,s)
 =\frac{((B_Q^L(t,s))^+)^2}{d_{j,Q}(t,s)}.
 \tag{5.1}
\]

The denominator must be stabilized.  If

\[
 P_{j,Q}^{\chi^2}=\|\chi_Q\nabla W_{j,s}\|_2^2,
 \qquad
 M_{j,Q}=\|1_{\operatorname{collar}Q}W_{j,s}\|_2^2,
 \tag{5.2}
\]

then

\[
 d_{j,Q}\le2P_{j,Q}^{\chi^2}+C r^{-2}M_{j,Q},
 \qquad
 P_{j,Q}^{\chi^2}\le2d_{j,Q}+C r^{-2}M_{j,Q}.
 \tag{5.3}
\]

Thus only

\[
 d_{j,Q}+r^{-2}M_{j,Q}
 \asymp
 P_{j,Q}^{\chi^2}+r^{-2}M_{j,Q}
 \tag{5.4}
\]

Here \(P_{j,Q}^{\chi^2}=\int\chi_Q^2|\nabla W|^2\); it is a cutoff-square
comparison quantity, not the ledger dissipation
\(\int\chi_Q|\nabla W|^2\) in (3.9).  Formula (5.4), rather than either
uncollared term alone, is structurally stable.  The collar cannot be
discarded.  For example, in an affine core with constant vorticity,
\(P_{j,Q}^{\chi^2}=0\) while \(d_{j,Q}>0\) comes entirely from
\(\nabla\chi_Q\times W\).

Now assume a nonnegative partition of unity \((\chi_{j,Q})_Q\) at the
matched radius

\[
 r_j=\rho K_j^{-1},
 \tag{5.5}
\]

where \(T_j\) is supported in
\(cK_j\le|k|\le CK_j\).  Suppose the overlap and normalized derivative
constants are uniform.  Then

\[
 \sum_Qd_{j,Q}
 \lesssim D_{j,s}+r_j^{-2}Y_{j,s}
 \lesssim D_{j,s},
 \tag{5.6}
\]

where the last step is the valid annular Bernstein estimate.  Since
\(\sum_QB_Q^L=b_{j,s}\),

\[
 \frac{(b_{j,s}^+)^2}{D_{j,s}}
 \lesssim\sum_Qq_{j,Q}(t,s).
 \tag{5.7}
\]

At \(s=0\), set

\[
 A_{\rm loc,+}(t)
 =\frac1{Y(t)}\sum_{j,Q}q_{j,Q}(t,0).
 \tag{5.8}
\]

Set \(A_{\rm loc,+}=0\) when \(Y=0\).  The bridge to the global shell
consumer is explicit:

\[
 \begin{aligned}
 (b_{j,s}^+)^2
 &\le\left(\sum_Q(B_{j,Q}^L)^+\right)^2\\
 &\le\left(\sum_Qq_{j,Q}\right)\left(\sum_Qd_{j,Q}\right)
 \lesssim D_{j,s}\sum_Qq_{j,Q}.
 \end{aligned}
 \tag{5.8a}
\]

R0.71C and (5.7) give the following conditional statement.

### Theorem 5.1 — matched local projected-Lamb continuation criterion

Let a strong solution use a fixed dyadic annular tight frame and matched
partitions satisfying the uniform constants above.  If

\[
 \int_0^{T_*}A_{\rm loc,+}(t)\,dt<\infty,
 \tag{5.9}
\]

then the strong solution continues beyond \(T_*\).

This is a valid localization of the R0.71C consumer.  By (5.7), it is more
restrictive than the global shell condition.  No implication showing it to be
weaker than a standard published criterion is proved here.  In fact, local
Cauchy and bounded overlap give

\[
 A_{\rm loc,+}(t)
 \le N\frac{\|L(t)\|_2^2}{Y(t)}
 \le N\|u(t)\|_\infty^2.
 \tag{5.10}
\]

Therefore the Serrin endpoint \(u\in L_t^2L_x^\infty\) implies (5.9).  No
converse or strict separation is proved.

## 6. Unconditional local heat packing

The positive bulk estimate is stronger than the signed reconstruction in
(5.7).  Cauchy gives, for every cutoff separately,

\[
 q_{j,Q}(t,s)
 \le\|1_{\operatorname{supp}\chi_{j,Q}}F_{j,s}(t)\|_2^2.
 \tag{6.1}
\]

If the supports overlap at most \(N\) times, then

\[
 \sum_Qq_{j,Q}(t,s)\le N\|F_{j,s}(t)\|_2^2.
 \tag{6.2}
\]

Summing the tight frame proves (1.1).  Spectral integration gives, for every
\(\alpha>0\), the exact extended-valued inequality

\[
 \boxed{
 \int_0^\infty s^{\alpha-1}
 \sum_{j,Q}q_{j,Q}(t,s)\,ds
 \le
 \frac{N\Gamma(\alpha)}{2^\alpha}
 \|(-\Delta)^{-\alpha/2}L(t)\|_2^2.}
 \tag{6.3}
\]

The right side is not asserted finite from Leray energy for every
\(\alpha>0\).  Standard energy closes the critical endpoint \(\alpha=1\);
the torus spectral gap then also gives finiteness for \(\alpha\ge1\).
For \(0<\alpha<1\), (6.3) is a precise spectral inequality but requires
additional negative-Sobolev information to be finite.

At \(\alpha=1\),

\[
 \int_0^\infty\sum_{j,Q}q_{j,Q}(t,s)\,ds
 \le\frac N2\|(-\Delta)^{-1/2}L(t)\|_2^2
 \le\frac N2\|u(t)\|_4^4.
 \tag{6.4}
\]

Define the normalized local bulk

\[
 \mathcal V_{\rm loc}(t)
 =\frac1{Y(t)}
 \int_0^\infty\sum_{j,Q}q_{j,Q}(t,s)\,ds.
 \tag{6.5}
\]

Set \(\mathcal V_{\rm loc}=0\) when \(Y=0\).
The same interpolation and energy argument as R0.71E gives

\[
 \boxed{
 \int_0^T\mathcal V_{\rm loc}(t)\,dt
 \le
 \frac{NC_S^3}{2\sqrt{2\nu}}
 \|u_0\|_2^2\sqrt T.}
 \tag{6.6}
\]

This is unconditional for periodic Leray--Hopf solutions in the same
finite-truncation/Fatou sense as R0.71E.  The moving-cutoff identity itself is
used only on smooth or strong intervals.

There is a second packing boundary.  If independent covers are taken at
every spatial radius \(r_k=R2^{-k}\), bounded overlap controls each scale but
does not sum the infinitely many scales.  For every \(\beta>0\),

\[
 \sum_{k,Q}r_k^\beta q_{j,k,Q}
 \le\frac{NR^\beta}{1-2^{-\beta}}\|F_{j,s}\|_2^2,
 \tag{6.7}
\]

whereas \(\beta=0\) pays the number of retained scales.  Thus a covering
lemma does not by itself prove unweighted Carleson packing across an infinite
scale chain.

## 7. Exact local cutoff witness

For \(\sigma=-1\), \(a>0\), and dyadic \(K=2^j\), recall the true NSE datum

\[
 u_{-,a,K}(x)
 =aK\left(
 0,
 -2\cos(Kx_1),
 -2\sin(Kx_1+Kx_2)-2\cos(Kx_2)
 \right).
 \tag{7.1}
\]

It is 2D3C and generates a global smooth three-dimensional periodic NSE
solution.  Use the one fixed radial frame refinement constructed in R0.71E.
Its positive low-radius block at the initial trace is

\[
 W_s
 =2aK^2e^{-K^2s}
 \left(\sin(Kx_2),0,\sin(Kx_1)\right),
 \tag{7.2}
\]

\[
 F_s
 =-2a^2K^3e^{-K^2s}
 \left(0,0,\cos(Kx_2)\right).
 \tag{7.3}
\]

Let \(\phi\ge0\) be any nonzero smooth spatial cutoff, fixed before the data.
The complete local work is

\[
 B_\phi(s)
 =\langle F_s,\nabla\times(\phi W_s)\rangle.
 \tag{7.4}
\]

No collar term is removed.  Integration by parts gives

\[
 \begin{aligned}
 B_\phi(s)
 &=\langle\phi W_s,\nabla\times F_s\rangle\\
 &=4a^3K^6e^{-2K^2s}
   \int\phi(x)\sin^2(Kx_2)\,dx>0.
 \end{aligned}
 \tag{7.5}
\]

Both \(F_s\) and \(W_s\) lie on the sphere \(|k|=K\).  Therefore

\[
 d_\phi(s)=e^{-2K^2s}d_\phi(0),
 \qquad
 q_\phi(s)=e^{-2K^2s}q_\phi(0).
 \tag{7.6}
\]

For every \(h>0\),

\[
 \boxed{
 q_\phi(0)
 =\frac{2K^2}{1-e^{-2K^2h}}
 \int_0^h q_\phi(s)\,ds.}
 \tag{7.7}
\]

The exact coefficient satisfies

\[
 \max\{2K^2,h^{-1}\}
 \le
 \frac{2K^2}{1-e^{-2K^2h}}
 \le
 \frac1{1-e^{-1}}\max\{2K^2,h^{-1}\}.
 \tag{7.8}
\]

Thus the trace costs \(K^2+h^{-1}\) in scale equivalence.  At
\(h=\theta K^{-2}\), the height average obeys

\[
 \frac{h^{-1}\int_0^h q_\phi(s)\,ds}{q_\phi(0)}
 =\frac{1-e^{-2\theta}}{2\theta}.
 \tag{7.9}
\]

It is a fixed positive fraction.  Calling this average a Carleson quantity
does not make it smaller than the bottom trace.

## 8. A matched partition cannot hide the trace cost

Take a standard nonnegative partition \((\phi_Q)_Q\) at radius
\(r=\rho/K\), with

\[
 \sum_Q\phi_Q=1,
 \quad
 \sum_Q1_{\operatorname{supp}\phi_Q}\le N,
 \quad
 \sum_Q\phi_Q^2\le C_0,
 \quad
 \sum_Q|\nabla\phi_Q|^2\le C_1r^{-2}.
 \tag{8.1}
\]

The last two bounds in (8.1) are pointwise in space.  All quantities in this
section refer to the positive low-radius subblock from Section 7.
Every \(B_Q(s)\) is nonnegative by (7.5), and it is strictly positive for
every nonzero partition element.  Moreover,

\[
 \sum_QB_Q(s)=2a^3K^6e^{-2K^2s}.
 \tag{8.2}
\]

The stabilized denominators satisfy

\[
 \sum_Qd_Q(s)
 \le8a^2K^6e^{-2K^2s}
 \left(C_0+\frac{C_1}{\rho^2}\right).
 \tag{8.3}
\]

Cauchy in the reverse direction and the local upper packing give

\[
 \boxed{
 \frac{a^4K^6e^{-2K^2s}}
 {2(C_0+C_1/\rho^2)}
 \le\sum_Qq_Q(s)
 \le2Na^4K^6e^{-2K^2s}.}
 \tag{8.4}
\]

Using the total physical enstrophy

\[
 Y=8a^2K^4,
 \tag{8.5}
\]

the normalized bottom coefficient is comparable to \(a^2K^2\), while its
infinite heat bulk is exactly smaller by \(2K^2\).  In particular, choose

\[
 a=K^{-1}.
 \tag{8.6}
\]

Then

\[
 \|u_{-,K^{-1},K}\|_2^2=6,
 \tag{8.7}
\]

the normalized low-block aggregate bottom stays between positive
\(K\)-independent constants, and the corresponding low-block heat bulk is
\(O(K^{-2})\).  This is a
fixed-energy sequence of true global-smooth NSE initial traces.  It rules out
any energy-uniform, frequency-free recovery of this local low-block bottom
from its heat bulk.  No two-sided estimate for the full-frame
\(A_{\rm loc,+}\) is asserted here.

## 9. Interior skewed-cylinder scaling boundary

The exact formula above is an initial-trace theorem.  A separate scaling
argument puts the same critical obstruction on strictly interior skewed
cylinders, with a narrower claim.

Let \(u_{\rm aff}=(x_1,-x_2-x_3,0)\), put
\(A_0=-\frac13x\times u_{\rm aff}\), and choose a compactly supported smooth
cutoff \(\eta\) that equals one on a fixed affine core.  Then
\(u_0=\nabla\times(\eta A_0)\) is a smooth compactly supported
divergence-free datum on \(\mathbb R^3\), because
\(\nabla\times A_0=u_{\rm aff}\) in that core.  There,

\[
 u_0=u_{\rm aff}=(x_1,-x_2-x_3,0),
 \qquad \omega_0=(1,0,0),
 \qquad \nabla\times L_0=(1,0,0).
 \tag{9.1}
\]

The last equality follows from
\(\nabla\times L=\nabla\times(u\times\omega)
=(\omega\cdot\nabla)u-(u\cdot\nabla)\omega\).
Choose a nonnegative cutoff inside that core with
\(\nabla\chi\times\omega_0\not\equiv0\).  At the initial trace,

\[
 B_\chi^L=\int\chi\,\omega_0\cdot\nabla\times L_0>0,
 \qquad
 d_\chi>0.
 \tag{9.2}
\]

For this scaling test, take the covariant one-block tight frame \(T_0=I\), so
\(W_s=e^{s\Delta}\omega\) and \(F_s=e^{s\Delta}L\).  Multiplying the datum by
a sufficiently small fixed amplitude preserves (9.2).  Smooth local existence
and continuity keep (9.2) positive at a sufficiently small strictly interior
center time.  A sufficiently small symmetric skewed cylinder in Yang's sense,
centered at that time and contained strictly inside the smooth interval, is
admissible because

\[
 r^2\fint_{Q_r}\mathcal M(|\nabla u|)
 \le r^2\sup_{t\in I_r}\|\nabla u(t)\|_{L^\infty(\mathbb R^3)}
 \tag{9.3}
\]

and the right side tends to zero.  Fix one such base radius \(r_0\).
Continuity in the heat height gives \(q_Q(s)>0\) on some interval
\([0,h_0]\).  Shrink \(h_0\) if necessary and set
\(\theta=h_0/r_0^2>0\), so \(\mathcal V_{Q,h_0}>0\).

Now apply the exact NSE scaling, with \(r=r_0\) and \(h=h_0\),

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \quad
 r_\lambda=\lambda^{-1}r,
 \quad
 h_\lambda=\lambda^{-2}h,
 \tag{9.4}
\]

and scale the cutoff, mollifier, trajectory, and heat height covariantly.
The admissibility condition is scale invariant.  Moreover,

\[
 B_{Q_\lambda}=\lambda^3B_Q,
 \quad
 d_{Q_\lambda}=\lambda^3d_Q,
 \quad
 q_{Q_\lambda}=\lambda^3q_Q,
 \quad
 Y_\lambda=\lambda Y.
 \tag{9.5}
\]

At the strictly interior center time, define

\[
 A_Q=\frac{q_Q(s=0)}{Y},
 \qquad
 \mathcal V_{Q,h}=\frac1Y\int_0^h q_Q(s)\,ds.
 \tag{9.6}
\]

Thus the normalized bottom and heat bulk scale as

\[
 A_{Q_\lambda}=\lambda^2A_Q,
 \qquad
 \mathcal V_{Q_\lambda,h_\lambda}=\mathcal V_{Q,h}.
 \tag{9.7}
\]

### Theorem 9.1 — geometry-only subcritical trace no-go

There is a scale-covariant family of smooth NSE solutions and strictly
interior admissible skewed cylinders for which

\[
 \frac{A_{Q_r}}{\mathcal V_{Q_r,\theta r^2}}
 =c_*r^{-2}
 \tag{9.8}
\]

with \(c_*>0\) fixed by the base cylinder.  Consequently, consider a proposed
pure multiplicative estimate

\[
 A_Q\le c(r)\mathcal V_{Q,\theta r^2}
 \tag{9.9}
\]

for all smooth NSE solutions and all cylinders in this covariant one-block
class, with \(c(r)\) depending only on \(r\) and fixed uniform
geometry/admissibility constants.  Such an estimate cannot have
\(c(r)=o(r^{-2})\).

Explicitly, for the chosen base cylinder
\(c_*=r_0^2A_Q/\mathcal V_{Q,h_0}>0\); (9.8) is then the exact scaling
identity along \(r_\lambda=r_0/\lambda\).

The theorem has five boundaries.

1. It is a family of different smooth solutions, not a blow-up sequence for
   one solution.
2. It does not disprove a critical \(Cr^{-2}\) trace inequality; that scale is
   saturated.
3. The interior cylinders approach the initial face at the parabolic rate
   \(O(r^2)\).  The theorem does not address cylinders that remain a fixed
   positive time from the initial face while \(r\to0\).
4. The scaling theorem uses the covariant one-block frame.  It does not by
   itself reject an estimate restricted to another prescribed frame.  The
   fixed R0.71E dyadic frame is covered separately by Sections 7--8 at the
   exact initial trace.
5. An estimate with additional shape, collar, pressure, subgrid, or
   solution-dependent terms is not of the pure form (9.9) and is not rejected
   by this theorem.

The fixed-energy statement is the exact initial-trace family in Section 8.
The whole-space interior scaling family has
\(\|u_\lambda\|_2^2=\lambda^{-1}\|u\|_2^2\).  It therefore also rejects a
factor that is uniform under a bounded kinetic-energy upper bound.  It does
not reject an arbitrary solution-dependent factor, including one allowed to
become singular as the kinetic energy tends to zero.

## 10. Why standard trace and Carleson arguments stop here

For every absolutely continuous nonnegative function \(q\),

\[
 q(0)
 \le\frac1h\int_0^hq(s)\,ds+\int_0^h|q'(s)|\,ds.
 \tag{10.1}
\]

For the local quotient, \(q'\) contains

\[
 \Delta F_{j,s},
 \qquad
 \Delta W_{j,s},
 \tag{10.2}
\]

through the derivatives of \(B_Q^L\) and \(d_Q\).  Annular Bernstein replaces
these derivatives by \(K_j^2\), exactly the factor in (7.7).  Across shells,
controlling them would require an additional derivative or frequency
hypothesis.  This report proves no particular Besov or dissipation-wavenumber
criterion implies the desired trace bound.

The energy theorem controls only

\[
 \mathcal V_{\rm loc}\in L_t^1.
 \tag{10.3}
\]

On a time interval \(I_r\) of length \(r^2\), absolute continuity gives

\[
 \int_{I_r}\mathcal V_{\rm loc}(t)\,dt\to0,
 \tag{10.4}
\]

but a critical trace estimate would require the stronger rate

\[
 \int_{I_r}\mathcal V_{\rm loc}(t)\,dt=o(r^2)
 \tag{10.5}
\]

to force vanishing after multiplication by \(r^{-2}\).  Standard energy does
not provide that rate.  At an ordinary Lebesgue point the integral is
typically \(r^2\mathcal V_{\rm loc}(t_0)+o(r^2)\), which yields only an
\(O(1)\) critical density.

This is also why the flow-adapted maximal theorem does not close the gap.  It
is weak \((1,1)\) at the energy endpoint and acts in physical space--time.  It
does not add regularity in \(s\), and it does not turn \(L_t^1\) absolute
continuity into the rate (10.5).

## 11. Literature and known-criterion boundary

The theorem-level source audit is recorded in
[research/r071f_literature_audit.md](r071f_literature_audit.md).  Its narrow
conclusions are as follows.

- [Yang, arXiv:2008.05588v2](https://arxiv.org/abs/2008.05588v2) constructs the skewed-cylinder
  maximal function, proves weak \((1,1)\) and strong \((p,p)\), and supplies the
  admissibility/covering geometry.  It proves no projected-Lamb heat trace.
- [Vasseur--Yang, arXiv:2009.14291v1](https://arxiv.org/html/2009.14291v1) uses that geometry to
  globalize local vorticity estimates.  Its local regularity theorem assumes
  mixed-norm smallness; the geometry does not manufacture that smallness.
- [Chen--Liang--Tsai, arXiv:2606.16438v1](https://arxiv.org/html/2606.16438v1)
  proves, for the exact parabolic Poisson extension defined in that paper,
  reverse caloric trace estimates from interior normal derivatives to boundary
  Besov/Triebel--Lizorkin regularity.  It does not recover a boundary trace from
  zero-order heat bulk.
- [Yu, arXiv:2606.27560v1](https://arxiv.org/html/2606.27560v1) proves
  conditional unweighted filtered-vortex-stretching closure in its exact
  whole-space setting.  The principal cutoff residual must be eliminated by an
  adjoint cutoff or included in a summable nonnegative shell budget, and the
  full far field, including a separately controlled exterior tail, commutator
  increments, and remaining shell budgets are assumed summable.  Those
  hypotheses are not consequences of Leray energy in that paper.

The comparison with standard regularity criteria is logical, not rhetorical.

| Criterion | Safe relation established here |
|---|---|
| Serrin endpoint \(u\in L_t^2L_x^\infty\) | Equation (5.10) implies (5.9); no converse or strict separation is proved |
| Koch--Tataru small \(BMO^{-1}\) initial data | No implication in either direction is proved between that initial-data theory or solution-space norm and the posterior quantity \(A_{\rm loc,+}\) |
| Critical Besov criteria | No particular Besov space, exponent, or published criterion is fixed here; no implication in either direction with (5.9) is claimed |
| BKM-type vorticity continuation condition | No implication in either direction with (5.9) is established here |
| Dissipation-wavenumber criteria | These are distinct from BKM-type criteria; no implication in either direction with (5.9) is established here |
| R0.71F heat bulk | Unconditional for periodic Leray--Hopf solutions only in the stated setup and finite-truncation/Fatou sense; it is not itself a regularity criterion |

The phrase “localized criterion” therefore does not mean “weaker criterion.”
R0.71F has proved a correct consumer and a sharp obstruction to deriving its
hypothesis from geometry plus energy.

Pressure supplies no missing sign.  If

\[
 F_{j,s}=A_{j,s}(u\times\omega)-\nabla A_{j,s}B,
 \tag{11.1}
\]

then the two apparent Bernoulli contributions inside (3.6) cancel because

\[
 \langle\nabla A_{j,s}B,
 \nabla\times(\chi_QW_{j,s})\rangle=0.
 \tag{11.2}
\]

Pressure remains nonlocal in a strain or local-energy ledger, where it must
be retained with the compatible subgrid terms.

## 12. Claim ledger and next gate

| Item | R0.71F status |
|---|---|
| Complete moving projected-Lamb ledger (3.4), (3.9) | Exact identity |
| Projected/material equivalence (4.5) | Exact identity |
| Stabilized matched local continuation criterion | Conditional theorem |
| Bounded-overlap local heat packing (6.3) | Exact theorem |
| Normalized local heat bulk in \(L_t^1\) | Unconditional Leray-level result |
| Unweighted packing over infinitely many independent spatial scales | Not proved; the overlap upper bound grows with the retained scale count and gives no uniform infinite-scale sum |
| Exact local cutoff trace (7.5)--(7.7) | True global-smooth 2D3C initial-trace theorem |
| Fixed-energy matched-partition low-block separation | Exact obstruction; no full-frame two-sided estimate is claimed |
| Pure geometry-only \(o(r^{-2})\) interior trace for covariant one-block frame | Rejected by scale-covariant smooth family |
| Critical \(Cr^{-2}\) trace | Not rejected; saturated by the witness |
| Bottom coefficient in \(L_t^1\) from standard energy | Not proved |
| Universal beneficial pressure sign | Not available in the vorticity ledger |
| Global regularity or singularity | Not obtained |

### Next justified gate: R0.71G

The instantaneous bottom trace can be large even for global-smooth data, but
the continuation theorem integrates it in physical time.  The next
admissible question is therefore temporal, not another spatial covering:

> Can NSE dynamics bound the residence time of a high signed Lamb trace at
> frequency \(K\) by its viscous time \(K^{-2}\), with all inter-shell transfer
> and time-boundary terms retained?

R0.71G should construct a signed Lamb trace residence-time ledger.  It must:

1. distinguish a large instantaneous trace from a persistent trace;
2. retain \(\partial_tL\), inter-shell transfer, and moving-partition terms;
3. prove any occupation-time or frequency-envelope summability from NSE
   budgets rather than assume it;
4. test the estimate on the exact 2D3C family and on scale-covariant interior
   cylinders;
5. compare the resulting time-frequency condition with Serrin, BKM, critical
   Besov, and dissipation-wavenumber criteria.

If the occupation estimate merely rewrites
\(\int A_{\rm sb,+}(t)dt<\infty\), the branch must stop.  The valid advance in
R0.71F is narrower: it identifies persistence, rather than geometry or heat
bulk, as the next unresolved mechanism.

## 13. Reproduction

The exact producer is research/r071f_exact_audit.py.  It reconstructs the low
block from the six Fourier modes, verifies the cutoff--curl
integration-by-parts identity, proves the exact heat trace and Gamma moment
constants, and checks the matched-partition bounds.

The independent checker is research/r071f_independent_audit.py.  It does not
import the producer.  It starts from the full trigonometric velocity, uses
independent FFT differentiation and Leray projection, inserts a nonconstant
positive cutoff in physical space, and checks \(K=1,2,4,8\) plus finite-height
quadrature.

The archived certificate bundle, formal figure package, public HTML, and PDF
were locked only after both checkers and the independent mathematical audit
passed.  Numerical certificates support the finite identities; the general
theorems are proved in this report.
