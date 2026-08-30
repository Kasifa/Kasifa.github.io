# R0.73G adversarial audit: nonlinear use of the exact-row growth theorem

**Date:** 2026-08-30  
**Input:** R0.73F, one exact moving linear Fourier row  
**Question:** what is required to convert that input into a nonlinear
Navier--Stokes perturbation theorem?  
**Verdict:** the direct upgrade from R0.73F alone is not closed; the current
R0.73G proof closes a deliberately weaker, over-small-seed planar theorem,
audited in Section 11

## 0. Direct verdict

R0.73F proves a genuine linear statement.  On the row

\[
 \beta=\xi=0,\qquad \gamma=\frac12,
 \qquad \varepsilon=|\Lambda|^{-1},
 \tag{0.1}
\]

there is a finite-dimensional moving unstable bundle and, for

\[
 T_{\varepsilon,D}=\frac{d_D}{\varepsilon},
 \qquad d_D=\min\{D,d_0\},
 \qquad T_D^{\rm phys}=\frac{d_D}{4},
 \tag{0.2}
\]

the exact row evolution has

\[
 \|U_\varepsilon(T_{\varepsilon,D},0)v_\varepsilon\|_{\mathcal K_{1/4}}
 \ge K_1^{-1}e^{\lambda T_{\varepsilon,D}},
 \qquad
 \lambda=\alpha+\eta>0,
 \tag{0.3}
\]

for every unit vector
\(v_\varepsilon\in P_\varepsilon H\).  The initial vector is allowed to
depend on \(\varepsilon\).  The theorem is in the row kinetic norm, which is
the physical velocity \(L^2\) norm after the exact OS--Squire embedding.

None of the following follows from (0.3) alone:

1. invariance of that row under the Navier--Stokes quadratic term;
2. a bilinear estimate in the kinetic \(L^2\) topology;
3. a uniform high-Sobolev realization of the unstable launch;
4. a nonlinear lifespan reaching \(T_D^{\rm phys}=d_D/4\);
5. nonlinear shadowing of the growing linear orbit;
6. finite-time blow-up.

Two exact no-go results below make the first two failures explicit.  A third
finite-dimensional example shows that even \(e^{c/\varepsilon}\) linear
growth is logically compatible with a global nonlinear flow.  For the actual
R0.73F OS launch there is a stronger fact: its full nonlinear orbit stays in
an embedded two-dimensional Navier--Stokes class and is globally smooth.

## 1. The nonlinear equation that would have to be frozen

Let \(\overline U^\Lambda(t)\) denote the exact heat-decaying shear on the
standard torus and let \(w\) be a divergence-free velocity perturbation.
Before choosing a topology, the full perturbation equation has to be written
in physical variables as

\[
 \partial_t w
 =\mathcal L_\Lambda(t)w
 -\mathbb P\nabla\!\cdot(w\otimes w),
 \qquad \nabla\cdot w=0,
 \tag{1.1}
\]

where \(\mathbb P\) is the full three-dimensional Leray projection.  In the
exact realization (3.5), the R0.73F profile time is \(d=4t\), and

\[
 \theta=|\Lambda|d=4|\Lambda|t.
 \tag{1.2}
\]

Thus a physical quadratic term with coefficient one becomes

\[
 \partial_\theta w
 =\mathscr L_\varepsilon(\theta)w
 -\frac{\varepsilon}{4}\mathbb P\nabla\!\cdot(w\otimes w).
 \tag{1.3}
\]

The factor \(\varepsilon/4\) must also be tracked through velocity recovery,
the OS--Squire variables, and the rowwise kinetic conjugation.  R0.73F is a
linear theorem and does not itself certify this nonlinear coordinate ledger.

The linearized equation preserves each homogeneous Fourier/Bloch row because
the background depends only on the shear variable.  The quadratic term obeys
the different selection rule

\[
 (\rho_1,\rho_2)\longmapsto \rho_1+\rho_2.
 \tag{1.4}
\]

Reality also forces the conjugate row.  Thus data in the real
\(\gamma=\pm1/2\) pair can generate rows
\(\gamma=0,\pm1\) at the first nonlinear interaction.  Later interactions
generate further integer and half-integer rows.  The rowwise kinetic
isometry is linear; it is not an algebra homomorphism that removes (1.3).
At the next interaction, the zero row times the half row, and the unit row
times the opposite half row, can feed back into \(\gamma=\pm1/2\).  Hence a
projected equation may show no same-row quadratic term and still acquire a
same-row cubic remainder.  The generated zero row can also change the shear
seen by the linearized half row.

## 2. Exact no-go I: the real one-row pair is not nonlinearly invariant

The following computation uses only the Fourier formula for the Leray
nonlinearity.  Work on a compatible periodic cover with shear variable
\(x\) of period \(2\pi\) and homogeneous variable \(y\) of period \(4\pi\).
Equivalently, this is the usual Bloch bookkeeping at
\(\gamma=1/2\).  The third coordinate is denoted by \(z\).

For an integer \(N\ge1\), set

\[
 k=\left(0,\frac12,0\right),
 \qquad
 \ell=\left(N,\frac12,0\right),
 \tag{2.1}
\]

and choose polarizations

\[
 a=(1,0,0),
 \qquad
 b_N=\left(-\frac1{2N},1,0\right).
 \tag{2.2}
\]

They are divergence-free:

\[
 a\cdot k=0,
 \qquad b_N\cdot\ell=0.
 \tag{2.3}
\]

Define the real smooth field

\[
 u_N(X)
 =a e^{ik\cdot X}+b_Ne^{i\ell\cdot X}
 +a e^{-ik\cdot X}+b_Ne^{-i\ell\cdot X}.
 \tag{2.4}
\]

Its Fourier support lies entirely in the real row pair
\(\gamma=\pm1/2\), with \(\xi=0\) and integer shear frequencies.  For

\[
 \mathcal B(u,v)=\mathbb P[(u\cdot\nabla)v],
 \tag{2.5}
\]

the coefficient at \(n=k+\ell=(N,1,0)\) is

\[
 \widehat{\mathcal B(u_N,u_N)}(n)
 =i\mathbb P_n
 \left[(a\cdot\ell)b_N+(b_N\cdot k)a\right].
 \tag{2.6}
\]

The vector before projection is exactly

\[
 (a\cdot\ell)b_N+(b_N\cdot k)a
 =Nb_N+\frac12a
 =(0,N,0).
 \tag{2.7}
\]

Since \(n=(N,1,0)\),

\[
 \mathbb P_n(0,N,0)
 =\left(
 -\frac{N^2}{N^2+1},
 \frac{N^3}{N^2+1},
 0
 \right),
 \tag{2.8}
\]

and hence

\[
 \left|\widehat{\mathcal B(u_N,u_N)}(n)\right|
 =\frac{N^2}{\sqrt{N^2+1}}>0.
 \tag{2.9}
\]

The output has homogeneous frequency \(\gamma=1\), not
\(\gamma=\pm1/2\).  Therefore the real one-row pair is not invariant under
the Navier--Stokes nonlinearity.

The same field also generates the homogeneous zero row.  At
\(m=k-\ell=(-N,0,0)\), the vector before projection is

\[
 -Nb_N+\frac12a=(1,-N,0),
 \qquad
 \mathbb P_m(1,-N,0)=(0,-N,0)\ne0.
 \tag{2.10}
\]

Thus both the mean row and a doubled row appear at the first quadratic
interaction.

This is an algebraic statement about the row, not a statement about the
particular R0.73F top eigenspace.  It proves that row membership alone cannot
close a nonlinear bootstrap.  A special cancellation for the actual top
vectors would have to be proved separately; it cannot be inferred from the
linear invariant-row theorem.

## 3. Exact no-go II: kinetic \(L^2\) cannot absorb the quadratic remainder

With normalized Fourier basis, (2.4) satisfies

\[
 \|u_N\|_2^2
 =2\bigl(|a|^2+|b_N|^2\bigr)
 =4+\frac1{2N^2}.
 \tag{3.1}
\]

Equations (2.8)--(2.9) give

\[
 \|\mathcal B(u_N,u_N)\|_2
 \ge \frac{N^2}{\sqrt{N^2+1}}.
 \tag{3.2}
\]

Consequently, there is no constant \(C\) such that

\[
 \|\mathbb P[(u\cdot\nabla)u]\|_2
 \le C\|u\|_2^2
 \tag{3.3}
\]

for all smooth periodic divergence-free fields.  The counterexample even
starts inside the real \(\gamma=\pm1/2\) row pair.

R0.73B supplies an all-row forced physical-\(L^2\) estimate when the
projected force belongs to \(L^1_dL^2_x\).  Equation (3.2) shows that an
energy-level perturbation does not place its Navier--Stokes forcing in that
class by a quadratic \(L^2\) bound.  R0.73F's one-row kinetic-\(L^2\) lower
law and R0.73B's forced \(L^2\) upper law therefore do not form a nonlinear
bootstrap by themselves.

For a standard Sobolev choice, one instead has, for suitable \(s\),

\[
 \|\mathcal B(u,v)\|_{H^{s-1}}
 \le C_s\|u\|_{H^s}\|v\|_{H^s}.
 \tag{3.4}
\]

Closing Duhamel in \(H^s\) then requires an all-row forced estimate from
\(H^{s-1}\) to \(H^s\), with its short-time singularity and all constants
uniformly quantified in \(\varepsilon\).  Alternatively, an
energy-commutator argument usually takes \(s>5/2\) in three dimensions so
that \(\nabla u\in L^\infty\).  Neither statement is contained in R0.73F.
There is also a possible mixed route: close the strong norm by a separate
\(H^s\) energy estimate, use
\(\mathcal B(w,w)\in L^1_dL^2_x\), and apply the R0.73B forced bound only to
the \(L^2\) shadowing error.  That route still needs the strong-norm lifespan
and its exponent budget; it is not an energy-level \(L^2\) closure.

### 3.1 Exact top-row leakage and the planar barrier

The physical realization of the R0.73F row gives a stronger model-specific
statement.  On the standard three-torus the background can be written

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr).
 \tag{3.5}
\]

The row \(K_1=0\), \(K_3=1\) has
\(\gamma=K_3/2=1/2\).  A positive-row OS velocity with zero Squire
component has, in the scaled shear coordinate, the form

\[
 u_v(y,z)
 =\left(0,v(y),\frac{i}{\gamma}v'(y)\right)e^{i\gamma z}.
 \tag{3.6}
\]

It is divergence-free.  Direct differentiation gives

\[
 (u_v\cdot\nabla)u_v
 =\left(
 0,0,
 \frac{i}{\gamma}\bigl(vv''-(v')^2\bigr)
 \right)e^{2i\gamma z}.
 \tag{3.7}
\]

Thus the self-interaction lies in the doubled row before projection.  It is
annihilated by the Leray projector exactly when

\[
 vv''-(v')^2\quad\hbox{is constant in }y.
 \tag{3.8}
\]

Indeed, the vector in (3.7) is a gradient exactly when its scalar coefficient
is independent of \(y\).

The exceptional profiles in (3.8) can be classified.  If
\(g=vv''-(v')^2\) is constant, then

\[
 g'=vv'''-v'v''=0.
 \tag{3.9}
\]

On every interval where \(v\ne0\), equation (3.9) says that
\(v''/v\) is constant.  If \(g\ne0\), every zero is simple and the constants
on adjacent intervals agree by matching \(v'''/v'\) at the zero.  If
\(g=0\), a nonzero exponential solution on a component cannot meet a finite
zero with both \(v\) and \(v'\) zero.  Hence, apart from \(v\equiv0\), one
has globally

\[
 v''=cv.
 \tag{3.10}
\]

Periodicity then gives

\[
 v(y)=Ae^{iny}+Be^{-iny}
 \tag{3.11}
\]

for an integer \(n\ge0\), with the constant case included at \(n=0\).

No nonzero frozen viscous top eigenvector has the form (3.11).  To see this,
write its physical OS vorticity as \(q=Lv\), where

\[
 L=-\partial_y^2+\frac14.
 \tag{3.12}
\]

The frozen eigenvalue equation is

\[
 \sigma Lv
 =-\frac i2\bigl(WLv+W_{yy}v\bigr)
 -\varepsilon L^2v.
 \tag{3.13}
\]

At \(d=0\), the coefficient \(W_2\) of \(e^{2iy}\) is nonzero.  For
\(n\ge1\), if the coefficient \(A\) in (3.11) is nonzero, the \(n+2\)
Fourier coefficient of the multiplication term in (3.13) is uniquely

\[
 W_2\left(n^2+\frac14-4\right)A
 =W_2\left(n^2-\frac{15}{4}\right)A\ne0.
 \tag{3.14}
\]

The left side and the viscous term have no \(n+2\) coefficient.  This is a
contradiction.  If \(A=0\), the symmetric \(-n-2\) coefficient generated by
the coefficient \(B\) gives the same contradiction.  The \(n=0\) constant
case is covered directly by its generated \(\pm2\) coefficients.  Therefore
the actual frozen top eigenvector has a nonzero projected doubled-row
self-interaction.  A real conjugate-pair launch is not a nonlinear one-row
solution.

There is, however, an exact barrier in the other direction.  Define

\[
 \mathcal S_{2D}
 =\left\{
 (0,w_2(y,z),w_3(y,z)):
 \partial_yw_2+\partial_zw_3=0
 \right\}.
 \tag{3.15}
\]

The background (3.5), the top OS row, its conjugate, the Laplacian, the
Leray projection, and the quadratic term all preserve
\(\mathcal S_{2D}\).  The restriction is exactly the two-dimensional
periodic Navier--Stokes equation in \((y,z)\), embedded in three dimensions.
Every smooth orbit in this class is global and smooth.

Consequently, row leakage does occur for the actual top launch, but all
generated rows remain inside a planar invariant class.  This exact fact rules
out finite-time singularity and three-dimensional vortex stretching for the
nonlinear continuation of the R0.73F launch.  A genuinely transverse
component is a necessary new ingredient for any later three-dimensional
gate.

## 4. Topology and derivative ledger

The exact linear theorem lives in

\[
 H=L^2(\mathbb T_{2\pi})
 \quad\hbox{or, equivalently on the row,}\quad
 \mathcal K_{1/4}.
 \tag{4.1}
\]

A nonlinear strong-solution theorem needs a declared full-space topology.
For example, if \(X_s=H^s_\sigma\) with \(s>5/2\), the following are new
requirements:

1. the row velocity reconstruction and the kinetic conjugation must map the
   selected launch into \(X_s\);
2. the norm
   \(M_s(\varepsilon)=\|v_\varepsilon\|_{X_s}\) must be quantified;
3. the full nonautonomous linear evolution must act on \(X_s\), not only on
   row kinetic \(L^2\);
4. the forced evolution must recover the derivative lost in (3.4), or an
   equivalent commutator energy estimate must close;
5. the constants must cover all rows created by (1.3).

The R0.73F fixed-contour theorem gives
\(P_\varepsilon^{\rm inst}(d)\in\mathcal B(L^2)\) and a bounded
\(d\)-derivative there.  It explicitly does not give uniform transport in
the unscaled \(H^2\) graph norm.  Thus no uniform \(M_s(\varepsilon)\), no
\(H^s\)-bounded moving projection, and no high-regularity adjoint observable
may be read from that contour result.

This is not a cosmetic loss of derivatives.  If
\(M_s(\varepsilon)\) were allowed to grow as fast as the certified linear
gain, an exponentially small coefficient in front of \(v_\varepsilon\)
need not be small in \(H^s\).

## 5. Dependence of the unstable bundle on \(\varepsilon\)

R0.73F proves the exact initial identity

\[
 E^u_{\varepsilon,d}(0)=P_\varepsilon H.
 \tag{5.1}
\]

It also proves an inverse conorm estimate for every vector in that finite
block.  This is stronger than selecting one simple eigenline.  It does not,
however, produce a single \(\varepsilon\)-independent smooth physical
perturbation.

There is a limited positive observation.  R0.73E gives operator-norm
convergence of the frozen top projections in \(L^2\).  If
\(v_0\in P_0H\setminus\{0\}\), then normalized
\(P_\varepsilon v_0\) is an \(L^2\)-convergent choice for small
\(\varepsilon\).  This only addresses the launch in \(L^2\).  It does not
give:

- a uniform \(H^s\) bound for that choice;
- a real three-dimensional launch satisfying the conjugate-row constraint;
- a common moving fiber at positive time;
- a projection of the nonlinear forcing onto the growing bundle;
- control of the rows generated by the forcing.

Once the quadratic term creates other rows, the nonlinear solution is not an
orbit of the row cocycle.  In particular, the inverse estimate on
\(E^u_{\varepsilon,d}(t)\) cannot be applied directly to the nonlinear
solution.  A lower-bound bootstrap needs either a uniformly controlled
adjoint observable or a Duhamel error estimate in a topology that dominates
the row kinetic norm.

## 6. Seed size and lifespan must be stated together

Let

\[
 T_\varepsilon=\frac{d_D}{\varepsilon},
 \qquad \lambda=\alpha+\eta,
 \tag{6.1}
\]

and launch the linear orbit with coefficient \(\delta_\varepsilon\):

\[
 z_\varepsilon(\theta)
 =\delta_\varepsilon
 U_\varepsilon(\theta,0)v_\varepsilon.
 \tag{6.2}
\]

The certified endpoint lower bound is

\[
 \|z_\varepsilon(T_\varepsilon)\|_{\mathcal K_{1/4}}
 \ge
 \delta_\varepsilon K_1^{-1}e^{\lambda T_\varepsilon}.
 \tag{6.3}
\]

To make the linear lower signal reach a fixed size \(a_*>0\), the natural
coefficient scale is exponential:

\[
 \delta_\varepsilon\asymp
 a_*e^{-\lambda d_D/\varepsilon}.
 \tag{6.4}
\]

More precisely, the lower bound alone makes
\(\delta_\varepsilon=K_1a_*e^{-\lambda d_D/\varepsilon}\) sufficient for a
linear endpoint of at least \(a_*\).  It does not give a matching upper size;
that requires the separate envelope used below.

The corresponding initial strong norm is

\[
 \|z_\varepsilon(0)\|_{X_s}
 =\delta_\varepsilon M_s(\varepsilon).
 \tag{6.5}
\]

Thus even the assertion that the launches tend to zero in \(X_s\) requires

\[
 M_s(\varepsilon)e^{-\lambda d_D/\varepsilon}\longrightarrow0.
 \tag{6.6}
\]

No estimate of the form (6.6) is contained in R0.73F.  The current R0.73G
proof supplies a new, selected-vector estimate
\(M_3(\varepsilon)\le C_{\rm top}\varepsilon^{-2}\); this is audited
separately in Section 11 and must not be back-attributed to the linear
moving-bundle theorem.

### 6.1 A quantitative Duhamel budget

The missing constants can be displayed without assuming they exist.  The
following is a one-norm version; a mixed \(H^s\)-upper/\(L^2\)-error argument
has the same structure with separate norms.  Suppose that, in fast time, the
full perturbation equation has nonlinear coefficient
\(\chi_\varepsilon\) and that spaces \(X,Y\) satisfy

\[
 \|\mathcal N(u,v)\|_Y
 \le C_N\|u\|_X\|v\|_X.
 \tag{6.7}
\]

Assume a full all-row forced propagator estimate

\[
 \|\mathcal S_\varepsilon(\theta,r)f\|_X
 \le A_\varepsilon k_\varepsilon(\theta-r)
 e^{\omega_\varepsilon(\theta-r)}\|f\|_Y,
 \tag{6.8}
\]

and an upper envelope for the selected linear orbit,

\[
 \|\mathcal S_\varepsilon(\theta,0)v_\varepsilon\|_X
 \le M_\varepsilon e^{\omega_\varepsilon\theta}.
 \tag{6.9}
\]

Put

\[
 J_\varepsilon(T)
 =\int_0^T k_\varepsilon(\tau)
 e^{-\omega_\varepsilon\tau}\,d\tau.
 \tag{6.10}
\]

If a bootstrap assumes

\[
 \|w(\theta)\|_X
 \le2\delta_\varepsilon M_\varepsilon
 e^{\omega_\varepsilon\theta},
 \tag{6.11}
\]

then Duhamel gives the explicit error

\[
 \begin{aligned}
 \|w(\theta)-z_\varepsilon(\theta)\|_X
 &\le
 4\chi_\varepsilon A_\varepsilon C_N
 \delta_\varepsilon^2M_\varepsilon^2
 e^{2\omega_\varepsilon\theta}
 J_\varepsilon(\theta).
 \end{aligned}
 \tag{6.12}
\]

Two different smallness conditions appear.  Closing the upper bootstrap
requires, up to fixed constants,

\[
 \chi_\varepsilon A_\varepsilon C_NM_\varepsilon
 J_\varepsilon(T_\varepsilon)
 \delta_\varepsilon e^{\omega_\varepsilon T_\varepsilon}\ll1.
 \tag{6.13}
\]

Preserving half of the certified endpoint lower signal requires the stronger
exponent comparison

\[
 8K_1\chi_\varepsilon A_\varepsilon C_NM_\varepsilon^2
 J_\varepsilon(T_\varepsilon)
 \delta_\varepsilon
 e^{(2\omega_\varepsilon-\lambda)T_\varepsilon}\le1.
 \tag{6.14}
\]

For the physical realization (3.5), equation (1.3) gives
\(\chi_\varepsilon=\varepsilon/4\).  That favorable factor does not replace
the missing topology, smoothing kernel, and exponent budget.  In particular,
a coarse full-space upper exponent strictly larger than the row lower
exponent can consume the entire gain in (6.14).

R0.73B provides an exact all-row physical-\(L^2\) forced bound with transient
\(e^{|\Lambda|K(s,d)/2}\).  It does not provide (6.8) for the
\(H^{s-1}\) nonlinear forcing in (3.4).  Substituting its coarse
\(L^2\) exponent into (6.14), while ignoring the derivative mismatch, would
therefore be invalid twice.

### 6.2 A conservative strong-lifespan check

A standard high-Sobolev perturbation estimate around a shear of size
\(|\Lambda|\) has the schematic form

\[
 Y'(t)\le C_s|\Lambda|Y(t)+C_sY(t)^2,
 \qquad Y(t)=\|w(t)\|_{H^s}.
 \tag{6.15}
\]

Comparison with the scalar Riccati equation gives

\[
 Y(t)
 \le
 \frac{Y(0)e^{C_s|\Lambda|t}}
 {1-|\Lambda|^{-1}Y(0)
  (e^{C_s|\Lambda|t}-1)},
 \tag{6.16}
\]

after harmless adjustment of constants.  A sufficient condition for this
particular estimate to reach the physical endpoint
\(T_D^{\rm phys}=d_D/4\) is therefore

\[
 Y(0)\ll |\Lambda|e^{-C_s|\Lambda|T_D^{\rm phys}}.
 \tag{6.17}
\]

This is only a conservative sufficient condition, not a necessary threshold.
It shows why a nonlinear theorem must state seed size, topology, and lifespan
in one quantifier block.  Local well-posedness with an unspecified time does
not guarantee that the solution reaches the fast interval of length
\(d_D/\varepsilon\) used by R0.73F.

The exit scale must also be frozen.  An \(O(1)\) absolute departure from the
background, an \(O(|\Lambda|)\) relative departure, and divergence of an
\(H^s\) norm are different conclusions and lead to different seed ledgers.

## 7. Exact no-go III: exponential linear growth does not imply blow-up

The logical failure can be seen in a quadratic system.  For \(\lambda>0\),
consider

\[
 \dot x=\lambda x-xy,
 \qquad
 \dot y=x^2.
 \tag{7.1}
\]

The linearization at the origin has the growing solution
\(x(t)=e^{\lambda t}x(0)\).  Nevertheless,

\[
 I(x,y)=x^2+(y-\lambda)^2
 \tag{7.2}
\]

is exactly conserved, because

\[
 \frac d{dt}I
 =2x(\lambda x-xy)+2(y-\lambda)x^2=0.
 \tag{7.3}
\]

Every trajectory is bounded and global.  Taking
\(\lambda=\varepsilon^{-1}\) gives fixed-time linear gain
\(e^{t/\varepsilon}\) while the nonlinear system still has no finite-time
blow-up.  This example is not evidence about Navier--Stokes dynamics.  It is
an exact counterexample to the inference from a linear growth law alone to a
nonlinear singularity.

The Navier--Stokes energy structure gives an additional warning.  For a
divergence-free perturbation on a periodic domain,

\[
 \langle\mathbb P[(w\cdot\nabla)w],w\rangle_{L^2}=0.
 \tag{7.4}
\]

Its perturbation energy identity has the form

\[
 \frac12\frac d{dt}\|w\|_2^2+\|\nabla w\|_2^2
 =-\int (w\cdot\nabla U^\Lambda)\cdot w.
 \tag{7.5}
\]

The linear growth extracts energy from the background.  It does not supply a
positive scalar quadratic feedback law for higher norms.  If a nonlinear
bootstrap reaches an \(O(1)\) exit, the justified conclusion is loss of
proximity to the chosen background.  The estimate normally stops there; it
does not turn the exit into an infinite norm.

There is also a quantifier barrier.  A statement of the form

\[
 \forall |\Lambda|\gg1\ \exists w_0^\Lambda
 \quad\hbox{with large finite amplification}
 \tag{7.6}
\]

does not produce one finite \(\Lambda\) and one smooth datum whose strong
solution becomes singular.  R0.73F is a family-level asymptotic theorem.

## 8. Minimal remediation interface

A defensible nonlinear gate should require all of the following before
claiming a bootstrap.

### N1. Exact physical normalization

Write the full perturbation equation, the real conjugate-row reconstruction,
the physical-to-fast time change, and the nonlinear term after every kinetic
coordinate map.  Record the exact coefficient
\(\chi_\varepsilon=\varepsilon/4\) in (6.12).

### N2. Declared strong topology

Choose a specific space, for example \(H^s_\sigma\) with a stated
\(s>5/2\), an anisotropic Sobolev space, or a Gevrey space.  Prove the exact
bilinear estimate and specify whether the constants depend on
\(\varepsilon\), \(\Lambda\), or the row.

### N3. Smooth real unstable launch

Construct real divergence-free data from the top row and its conjugate.
Quantify

\[
 M_s(\varepsilon)=\|v_\varepsilon\|_{X_s}
 \tag{8.1}
\]

and prove the lower signal survives the real reconstruction.  Operator-norm
convergence in row \(L^2\) is not a substitute for (8.1).
For the present route, the concrete sufficient target

\[
 M_3(\varepsilon)\le C_{\rm top}\varepsilon^{-2}
 =C_{\rm top}\Lambda^2
 \tag{8.2}
\]

is deliberately non-sharp but would keep the Sobolev cost polynomial relative
to the exponential gain.

### N4. Full convolution ledger

List the output rows of every quadratic interaction in the bootstrap class.
Prove a weighted convolution inequality that sums those rows without a hidden
row-count loss.  The zero row, the doubled row, and their feedback into the
half row must be included from the first two nonlinear generations.

### N5. All-row nonlinear forcing closure

Either prove an all-start estimate of the form (6.8) from the derivative-lost
forcing space \(Y\) into the solution space \(X\), or close a strong norm by
a commutator energy estimate and combine it with the R0.73B physical-\(L^2\)
forced theorem.  In the second route, prove explicitly that the nonlinear
forcing lies in \(L^1_dL^2_x\).  Record every kernel, heat weight, exponent,
and dependence on \(\varepsilon\).

### N6. Exponent and seed budget

Give explicit upper-envelope and lower-signal exponents, then check
(6.13)--(6.14) for a declared
\(\delta_\varepsilon\).  State the initial size in \(X_s\), not only the
coefficient of an \(L^2\)-normalized vector.

### N7. Lifespan and exit statement

Prove that a unique strong solution exists through the whole physical window
used by the lower bound.  Freeze the exit time, exit norm, and target size.
The first safe target is nonlinear relative amplification for the family of
background shears; the final perturbation may still tend to zero.  An
order-one exit requires a stronger seed/exponent compatibility.  Blow-up is
already excluded for the planar launch and cannot be restored by wording.

## 9. Claim ledger

| Claim | State | Evidence or obstruction |
|---|---|---|
| `exactRowFixedWindowLinearGain` | **CLOSED INPUT** | R0.73F, (0.3) |
| `realHalfRowPairNonlinearlyInvariant` | **FALSE IN GENERAL** | exact Fourier--Leray computation (2.1)--(2.9) |
| `kineticL2QuadraticRemainderBound` | **FALSE** | bounded input norm and \(O(N)\) output in (3.1)--(3.3) |
| `actualTopRowHasNoModeLeakage` | **FALSE** | exceptional-profile classification and frozen eigen-equation sideband (3.6)--(3.14) |
| `planarTopLaunchCanDevelop3DVortexStretching` | **FALSE** | exact invariant class \(\mathcal S_{2D}\) in (3.15) |
| `planarTopLaunchCanBlowUp` | **FALSE** | reduction to globally regular periodic 2D Navier--Stokes |
| `epsilonIndependentSmoothUnstableLaunch` | **OPEN** | only row-\(L^2\) projection convergence is available |
| `uniformHsMovingBundle` | **OPEN** | R0.73F explicitly excludes unscaled graph-norm transport |
| `selectedTopVectorPolynomialH3Cost` | **CLOSED IN R0.73G** | elliptic iteration gives \(H^4=O(\Lambda^2)\), followed by the exact row velocity map |
| `allModeOversmallSeedRemainder` | **CLOSED IN R0.73G** | full \(H^3\) energy bound and physical-\(L^2\) remainder estimate, without row projection |
| `fixedWindowOversmallSeedRelativeAmplification` | **CLOSED IN R0.73G** | current Theorem 1.1, subject to the explicit proof repairs in Section 11 |
| `naturalSeedOrderOneDeparture` | **OPEN** | the sufficient seed may be much smaller than \(e^{-\kappa_D\Lambda}\), so the endpoint may still tend to zero |
| `sharpNonlinearInstabilityThreshold` | **OPEN** | no necessary scale or natural-scale closure is proved |
| `linearExponentialGainImpliesNonlinearBlowup` | **FALSE IN GENERAL** | exact global quadratic system (7.1)--(7.3) |
| `finiteTimeNavierStokesSingularity` | **OPEN** | no post-exit continuation obstruction |
| `ClayMillenniumProblem` | **OPEN** | one-row family-level linear growth is insufficient |

## 10. Status of the nearest safe theorem

The nearest mathematically coherent target was conditional nonlinear relative
amplification, not singularity formation:

> For each sufficiently small \(\varepsilon\), construct a real smooth seed
> of explicitly stated \(X_s\) size, prove existence through a declared fixed
> physical window, control every convolution-generated row, and preserve a
> fixed fraction of the R0.73F relative amplification after subtracting the
> nonlinear Duhamel error.  State separately whether the final perturbation
> tends to zero or reaches an order-one size.

The current R0.73G proof closes this target with a conservative
\(H^3\)-energy argument and an exponentially over-small seed.  It does not
close the natural seed scale or order-one departure.  The next coherent gate
is therefore one of the following: sharpen the all-mode exponent budget to
the natural seed scale, or introduce a genuinely transverse component and
start a new three-dimensional operator analysis.  With the exact R0.73F
launch, the theorem remains embedded two-dimensional dynamics and cannot be
a Navier--Stokes blow-up theorem.

## 11. Independent audit of the current nonlinear shadowing proof

**Object audited:** `research/r073g_nonlinear_shadowing_proof.md` as read on
2026-08-30.  This audit checks the theorem actually stated there, not a
stronger order-one instability or blow-up claim.  No finite truncation or
numerical diagnostic is used as proof in this audit.

### 11.1 Two-dimensional invariance: PASS

The background and selected launch lie in

\[
 \mathcal S_{2D}
 =\{(0,u_2(y,z),u_3(y,z)):
   \partial_yu_2+\partial_zu_3=0\}.
 \tag{11.1}
\]

For a field in (11.1), the advective derivative is
\(u_2\partial_y+u_3\partial_z\), its first component stays zero, and the
remaining equations are exactly periodic two-dimensional Navier--Stokes in
\((y,z)\).  The Leray projection preserves this closed divergence-free
subspace.  Strong uniqueness gives invariance, and standard 2D vorticity
regularity gives global smoothness.  This part of Theorem 1.1 is valid.

The consequence must remain explicit: all rows generated by the quadratic
term are still planar rows.  Mode leakage is not three-dimensional vortex
stretching.

### 11.2 Row and time scaling: PASS, with one constant obligation

For the standard-torus realization,

\[
 R=2,\qquad K_3=1,\qquad \gamma=\frac{K_3}{R}=\frac12,
 \qquad x=2y,\qquad d=4t,\qquad
 \varepsilon=\Lambda^{-1}.
 \tag{11.2}
\]

The fast time is
\(\theta=\Lambda d=4\Lambda t\).  Thus the R0.73F endpoint
\(\theta=d_D/\varepsilon=d_D\Lambda\) is the physical endpoint
\(T_D=d_D/4\), and its exponent is exactly
\((\alpha+\eta)d_D\Lambda=\kappa_D\Lambda\).  There is no missing factor
of two or four.

The proof must, however, replace the statement that the reconstruction is
merely "bounded" by the exact map

\[
 \mathcal Eh
 =\left(0,\frac12L^{-1/2}h,
 i\partial_xL^{-1/2}h\right)(2y)e^{iz},
 \qquad L=-\partial_x^2+\frac14.
 \tag{11.3}
\]

On the normalized Fourier \(L^2\) convention,

\[
 \frac{1/4+n^2}{n^2+1/4}=1,
 \tag{11.4}
\]

so (11.3) is an isometry.  The real vector must be written as

\[
 \phi_\Lambda=2^{-1/2}
 (\mathcal Eh_\varepsilon+\overline{\mathcal Eh_\varepsilon}),
 \tag{11.5}
\]

because the \(K_3=1\) and \(K_3=-1\) rows are orthogonal.  Each row evolves
independently under the linearized operator.  Equations (11.3)--(11.5), not
bounded equivalence alone, preserve the same prefactor \(K_1^{-1}\) in the
physical lower bound.  Alternatively, the theorem must replace \(K_1\) by
a new physical comparability constant.  This is a mandatory constant-ledger
repair, although it does not change the exponential conclusion.

### 11.3 The selected top vector and its \(H^3\) cost: PASS

The selected vector may be chosen as an eigenvector in the nonzero
finite-dimensional top Riesz space.  The common contour bounds its
eigenvalue, while \(\widetilde A(0)\) is bounded on each fixed \(H^m\).
From

\[
 \varepsilon Lh_\varepsilon
 =(\widetilde A(0)-\lambda_\varepsilon)h_\varepsilon
 \tag{11.6}
\]

and ellipticity of \(L\), iteration at \(m=0,2\) gives

\[
 \|h_\varepsilon\|_{H^2}\le C\varepsilon^{-1},
 \qquad
 \|h_\varepsilon\|_{H^4}\le C\varepsilon^{-2}.
 \tag{11.7}
\]

The reconstruction (11.3) is order zero at its worst component, and the
fixed lift introduces no \(\Lambda\)-dependent norm factor.  Hence
\(\|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2\).  Repeating the
elliptic step also gives smoothness for each fixed \(\Lambda\).

The theorem should say explicitly that "unit vector" means an
\(L^2\)-unit vector and should state which normalized torus measure is used.

### 11.4 The \(H^3\) energy inequality: PASS

For derivatives of order at most three, the leading term
\(\overline U_\Lambda\cdot\nabla D^aw\) cancels in the energy identity.
The commutators and \(w\cdot\nabla\overline U_\Lambda\) cost at most

\[
 C\|\overline U_\Lambda\|_{W^{4,\infty}}
 \|w\|_{H^3}^2
 \le C\Lambda\|w\|_{H^3}^2.
 \tag{11.8}
\]

Since \(H^3(\mathbb T^3)\hookrightarrow W^{1,\infty}\), the nonlinear
transport contribution is at most \(C\|w\|_{H^3}^3\).  Therefore the
claimed inequality

\[
 Y'\le a\Lambda Y+bY^2
 \tag{11.9}
\]

is valid with \(a,b\) independent of \(\Lambda\) for fixed \(D\).  The
Riccati calculation is also correct: the first term of the seed ceiling and
\(\|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2\) give exactly

\[
 Y(0)\le\frac{a\Lambda}{4b}e^{-a\Lambda T_D}.
 \tag{11.10}
\]

Division by \(Y\) at a possible zero should be described by the usual
\((Y^2+\rho^2)^{1/2}\) regularization or an upper Dini derivative.  This is
a proof-writing obligation, not a change to (11.9).

### 11.5 All-mode remainder and exponent: PASS

For \(r=w-z\), integration by parts gives

\[
 |\langle\mathbb P\nabla\!\cdot(w\otimes w),r\rangle|
 \le \frac12\|\nabla r\|_2^2+C\|w\|_{H^3}^4.
 \tag{11.11}
\]

Together with the shear term,

\[
 \frac d{dt}\|r\|_2^2
 \le c\Lambda\|r\|_2^2+C Y^4.
 \tag{11.12}
\]

Using \(Y(s)\le2e^{a\Lambda s}Y(0)\) and \(r(0)=0\) yields

\[
 \|r(T_D)\|_2^2
 \le16CT_D e^{(c+4a)\Lambda T_D}Y(0)^4,
 \tag{11.13}
\]

and hence

\[
 \|r(T_D)\|_2
 \le C_De^{M_D\Lambda}Y(0)^2,
 \quad
 C_D=4(CT_D)^{1/2},
 \quad
 M_D=\left(\frac c2+2a\right)T_D.
 \tag{11.14}
\]

The exponent and square-root factors are correct.  This estimate never
projects onto the selected row and therefore includes the zero, doubled, and
all later convolution-generated modes.

The second term in the seed ceiling is also algebraically sufficient:

\[
 C_De^{M_D\Lambda}C_{\rm top}^2\Lambda^4\delta^2
 \le \frac1{2K_1}e^{\kappa_D\Lambda}\delta.
 \tag{11.15}
\]

When \(M_D<\kappa_D\), the positive part
\((M_D-\kappa_D)_+\) is conservative but valid.  The conclusion is a gain
ratio; the estimate does not imply a non-vanishing endpoint amplitude.

### 11.6 Doubled-row noncancellation: PASS, with a derivation obligation

For the positive physical row

\[
 u_f=(0,f(y),if'(y))e^{iz},
 \tag{11.16}
\]

direct calculation gives

\[
 (u_f\cdot\nabla)u_f
 =(0,0,i[ff''-(f')^2])e^{2iz}.
 \tag{11.17}
\]

The Leray projection of (11.17) vanishes exactly when
\(ff''-(f')^2\) is constant.  A nonzero periodic solution of that exceptional
identity satisfies \(f''=cf\) globally, including across its isolated zeros,
and hence

\[
 f=Ae^{iny}+Be^{-iny}
 \tag{11.18}
\]

for an integer \(n\ge0\).  Such a two-column profile cannot be a frozen top
eigenvector.  In the OS vorticity equation the shift by the nonzero second
harmonic of \(W(0)\) has coefficient proportional to

\[
 n^2+\frac14-4=n^2-\frac{15}{4},
 \tag{11.19}
\]

which never vanishes for integer \(n\).  The extreme shifted column lies
outside the support in (11.18) and has no other column with which to cancel;
the viscous term is diagonal.  Therefore the selected top vector has a
nonzero projected \(K_3=2\) self-interaction.  The conjugate vector similarly
generates \(K_3=-2\), and cross-interaction generates \(K_3=0\).

The proof's displayed coefficient (7.5) is consistent with the same zero
condition, but it should be derived from the exact OS generator and should
state that the diagonal kinetic conjugation preserves Fourier support.  The
phrase "analytic continuation" should be replaced by the explicit
continuation across zeros given in Section 3.1 of this audit.  These repairs
remove a presentation gap; the noncancellation conclusion itself is valid.

### 11.7 Mandatory repairs and final verdict

Before release, the proof document must make the following repairs:

1. Insert the exact scaling ledger (11.2) and the isometric reconstruction
   (11.3)--(11.5), or replace the unchanged \(K_1\) by a separately tracked
   physical norm-equivalence constant.
2. State explicitly that \(\phi_\Lambda\) is \(L^2\)-unit, declare the torus
   norm convention, and mention elliptic iteration to smoothness.
3. Derive the doubled-row extreme-column coefficient from the OS generator,
   including the passage between \(f\), vorticity, and the kinetic variable.
4. Repair the source-level mathematical markup throughout.  Concrete broken
   instances include `on (\mathbb T^3)` in Section 1,
   `-mathbb P` in (2.3), `H^{m+2}}le` in (3.5), and `(pm2)` in Section 7;
   inline formulas written as ordinary parentheses also need delimiters.
5. Preserve the theorem boundary: exponentially over-small-seed relative
   amplification inside a globally regular planar class; no order-one exit,
   three-dimensional cascade, singularity, or Clay conclusion.

**SUBSTANTIVE MATHEMATICAL VERDICT: PASS.**  No substantive error was found
in planar invariance, row scaling, the \(H^3\) energy estimate, the remainder
exponent, the seed algebra, or doubled-row noncancellation.

**AS-WRITTEN RELEASE VERDICT: FAIL UNTIL THE MANDATORY REPAIRS ABOVE ARE
MADE.**  The unchanged prefactor \(K_1\) is not justified by the proof's
present word "bounded"; it becomes justified once the exact isometry
(11.3)--(11.5) is inserted.  Without that insertion or an explicit
replacement constant, the stated constant-level proof is incomplete.  The
broken source markup independently prevents release.  Even after repair, the
theorem is neither an order-one nonlinear instability result nor evidence
for a finite-time singularity or the Clay problem.

## 12. Post-repair verdict on the rewritten proof

**Re-audited object:** the rewritten
`research/r073g_nonlinear_shadowing_proof.md`, read after the repairs on
2026-08-30.

The five requested mathematical checks now pass in the source itself:

1. **Planar invariance: PASS.**  Section 2 writes the full three-dimensional
   perturbation equation and then reduces the invariant class
   \(\mathcal S_{2D}\) to periodic two-dimensional vorticity dynamics.  No
   Fourier-row invariance is substituted for planar invariance.
2. **Physical row scaling and lower constant: PASS.**  Section 3 now fixes
   \(x=2y\), \(\varepsilon=\Lambda^{-1}\), the physical rows
   \(K_z=\pm1\), and \(d=4t\).  Equations (3.6)--(3.7) give the exact
   kinetic-to-velocity isometry and the normalized real conjugate pair.
   The distinct notation \(K_{\rm F}\) is carried consistently through
   (1.7), (1.9), (3.8), (6.1), and (6.2).
3. **\(H^3\) launch and energy estimate: PASS.**  Equations (3.3)--(3.5)
   give \(H^4=O(\Lambda^2)\) for the selected top eigenvector; the exact
   order-zero lift gives the claimed \(H^3\) cost.  Equations (4.2)--(4.7)
   have the correct background derivative count, Sobolev embedding, Riccati
   scale, and \(\Lambda\)-independent constants.
4. **All-mode remainder exponent and seed algebra: PASS.**  The square-energy
   estimate (5.5), its integration in (5.6), and the square root in
   (5.7)--(5.8) give
   \(M_D=(c/2+2a)T_D\).  The second seed ceiling then gives exactly the
   half-gain in (6.1)--(6.2), including the case
   \(M_D<\kappa_D\).
5. **Doubled-row noncancellation: PASS.**  Section 7 now uses standard-torus
   physical coordinates, obtains the correct factor four in (7.2), writes
   the frozen OS equation, and uses the extreme \(n+2\) column to exclude
   every exceptional two-column profile.  The \(K_z=0,\pm2\) first
   generation and the absence of quadratic feedback to \(K_z=\pm1\) are
   stated separately.

The repair status of the five obligations in the former Section 11.7 is:

| Former obligation | Post-repair state |
|---|---|
| exact scaling, reconstruction, and lower-bound prefactor | **ELIMINATED** by (3.6)--(3.8) and the notation \(K_{\rm F}\) |
| explicit unit norm and smooth top launch | **ELIMINATED** by (3.3), (3.7), and the elliptic iteration available on every fixed \(H^m\) |
| extreme-column derivation and variable bridge | **ELIMINATED IN SUBSTANCE** by (7.1)--(7.6) |
| broken mathematical markup | **ELIMINATED**; the previously identified malformed tokens are gone |
| theorem boundary | **SATISFIED** in Sections 1, 2, 6, and 8 |

One literal coefficient edit remains advisable in (7.6).  As written, the
coefficient of the bracket
\(WLv+W_{xx}v\) at frequency \(n+2\) is

\[
 W_2\left(n^2+\frac14-4\right)A,
 \tag{12.1}
\]

whereas the coefficient of the **entire right-hand side** of (7.5) is

\[
 -\frac i2W_2\left(n^2+\frac14-4\right)A.
 \tag{12.2}
\]

The missing nonzero factor \(-i/2\) does not affect the contradiction or any
theorem conclusion.  The prose should either say "the coefficient inside the
bracket" or display (12.2).  This is an exactness edit, not a substantive
obstruction.

**POST-REPAIR SUBSTANTIVE VERDICT: FINAL PASS.**  There is no remaining
mathematical obstruction to the stated over-small-seed, fixed-window,
nonlinear relative-amplification theorem.  The result remains entirely
inside a globally regular planar subsystem.  It does not prove a natural
seed threshold, order-one departure, a three-dimensional cascade, blow-up,
or the Clay problem.
