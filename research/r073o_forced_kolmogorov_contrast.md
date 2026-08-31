# R0.73O forced contrast: a nondecaying Kolmogorov equilibrium with smooth \(H^3\)-small/\(L^2\)-escaping perturbations

**Status:** **FORMAL PASS after final independent analytic readback.**  The
audit passed the equilibrium, vorticity sign, cube embedding, scaling,
common-domain compact-resolvent continuation, complete Fourier-sector
exclusion, Riesz-rank argument, and the repaired two-dimensional FPS
transfer. No single checked source supplies both the twelve-digit critical
enclosure and the supercritical spectral direction; Section 4 records the
exact combination rather than attributing both claims to Nagatou alone.

**Role:** contrast theorem only. The equation contains a fixed nonzero body
force and therefore is not the unforced equation in the Clay problem.

## 1. Statement

On the standard torus

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3
\]

with viscosity one, consider

\[
 \partial_tu-\Delta u+P(u\cdot\nabla u)=Pf_*,
 \qquad \nabla\cdot u=0,
 \tag{1.1}
\]

where

\[
 U_*(x,y,z)=(30.12\sin 10y,0,0),
 \qquad
 f_*(x,y,z)=(3012\sin 10y,0,0).
 \tag{1.2}
\]

Then \(U_*\) is a smooth nondecaying equilibrium and has infinite accumulated
strain. Moreover, there are a number \(\rho_*>0\), smooth planar perturbations
\(w_{0,j}\), and times \(t_j>0\) such that

\[
 \|w_{0,j}\|_{H^3(\mathbb T^3)}\longrightarrow0,
 \tag{1.3}
\]

the solutions \(u_j\) of (1.1) with
\(u_j(0)=U_*+w_{0,j}\) are global and smooth, and

\[
 \|u_j(t_j)-U_*\|_{L^2(\mathbb T^3)}\ge\rho_*.
 \tag{1.4}
\]

Thus \(U_*\) is unstable in the full three-dimensional phase space, with
arbitrarily \(H^3\)-small input and a fixed \(L^2\) escape. The witnessing
directions lie in a two-dimensional invariant subspace; the theorem does not
claim an essentially three-dimensional unstable eigenmode.

## 2. Exact equilibrium and nondecay

Because \(U_*\) has only an \(x\)-component and depends only on \(y\),

\[
 (U_*\cdot\nabla)U_*=0.
 \tag{2.1}
\]

Also

\[
 -\Delta U_*=100U_*=f_*.
 \tag{2.2}
\]

Equations (2.1)--(2.2) prove the steady equation with constant pressure.
Furthermore,

\[
 \|\nabla U_*\|_{L^\infty}=30.12\times10=301.2,
\]

and hence

\[
 \int_0^\infty\|\nabla U_*\|_{L^\infty}\,dt=\infty.
 \tag{2.3}
\]

The divergence in (2.3) is automatic for this nonconstant equilibrium. It is
not, by itself, evidence of singularity or turbulence.

## 3. Exact reduction to the Kolmogorov eigenvalue problem

Keep only \(z\)-independent velocities with zero third component. This planar
subspace is invariant under (1.1). Write a perturbation using the stream
function convention

\[
 w=(\partial_y\psi,-\partial_x\psi,0).
 \tag{3.1}
\]

More generally, let the base velocity be

\[
 U=(A\sin Ny,0,0).
\]

Linearizing the vorticity equation and seeking
\(\psi=e^{\lambda t}\phi\) gives

\[
 \lambda\Delta\phi-\nu\Delta^2\phi
 +A\sin(Ny)(\Delta+N^2)\partial_x\phi=0.
 \tag{3.2}
\]

Introduce

\[
 X=Nx,\qquad Y=Ny,\qquad
 \sigma={\lambda\over AN},\qquad
 R={A\over\nu N}.
 \tag{3.3}
\]

After division by \(AN^3\), (3.2) becomes

\[
 \sigma\Delta_{X,Y}\phi-{1\over R}\Delta_{X,Y}^2\phi
 +\sin Y(\Delta_{X,Y}+I)\partial_X\phi=0.
 \tag{3.4}
\]

Take the physical \(x\)-wave number \(m=7\), the forcing wave number \(N=10\),
and \(A=30.12\). Functions of the form

\[
 e^{i7x}\sum_{k\in\mathbb Z}c_ke^{i10ky}
\]

become functions on

\[
 \mathbb T^2_\alpha
 =(-\pi/\alpha,\pi/\alpha)\times(-\pi,\pi),
 \qquad
 \alpha={m\over N}=0.7,
 \tag{3.5}
\]

and

\[
 R={30.12\over10}=3.012.
 \tag{3.6}
\]

This verifies the geometry and normalization rather than importing a critical
Reynolds number from a differently scaled torus.

## 4. Right-half-plane spectrum: the closed one-sided chain

Nagatou studies exactly (3.4) on \(\mathbb T^2_\alpha\). For
\(\alpha=0.7\), the computer-assisted proof encloses the critical Reynolds
number by

\[
 R_c\in
 [3.011528364444,\;3.011528364446].
 \tag{4.1}
\]

The numerical enclosure alone is not enough to choose the side of the
crossing.  All spectral continuation below is made on the invariant complex
Hilbert space

\[
 H=\left\{v\in L^2(\mathbb T^2_\alpha;\mathbb C^2):
 \nabla\cdot v=0,\ \int_{\mathbb T^2_\alpha}v=0\right\}.
\]

This restriction removes the constant harmonic velocities and is sufficient
for instability of the full phase space: an eigenvalue on an invariant
subspace is also an eigenvalue of the full linearization.  With
\(U=(\sin y,0)\), Leray projection \(P\), and common domain
\(D=H^2(\mathbb T^2_\alpha;\mathbb C^2)\cap H\), write the velocity
linearization as

\[
 \mathcal A_Rv={1\over R}P\Delta v
 -P\bigl(U\cdot\nabla v+v\cdot\nabla U\bigr).
\]

Every \(v\in H\) has a unique mean-zero periodic stream function
\(v=(\partial_y\phi,-\partial_x\phi)\).  Taking curl of
\(\mathcal A_Rv=\zeta v\) gives exactly (3.4) with
\(\sigma=\zeta\); conversely, a nonconstant solution of (3.4) gives an
eigenvector in \(H\).  Thus the source statements about (3.4) apply to the
velocity operator used in the continuation.

The required direction is supplied by the following source-level links and
the standard operator argument given immediately afterward.

1. Nagatou's equation (2.4) is exactly (3.4), and Proposition 2.1 says every
   eigenvalue with nonnegative real part is real.  In particular, an
   eigenvalue on the imaginary axis can only be zero.
2. In Matsuda--Miyatake's notation, the Reynolds parameter
   \(\lambda=\gamma/\nu^2\) equals base-flow amplitude divided by viscosity
   because their forcing wave number is one.  Their equations (4')--(6') are
   exactly the \(\sigma=0\) recurrence for (3.4), with
   \(\beta=m\alpha\) and \(\lambda=R\):

   \[
    a_{m,n}b_{m,n}+b_{m,n-1}-b_{m,n+1}=0,
    \qquad
    a_{m,n}=
    {2(m^2\alpha^2+n^2)^2\over
    Rm\alpha(m^2\alpha^2+n^2-1)}.
   \]

   Proposition 1 states that, for \(0<\beta<1\), this recurrence has a
   nonzero \(\ell^2\) solution if and only if
   \(\lambda=\lambda(\beta)\), while for \(\beta\ge1\) it has only the zero
   solution.

   Matsuda--Miyatake formulate this recurrence in the central-inversion-even
   sector spanned, for fixed \(m>0\), by
   \(\cos(m\alpha x+ny)\).  The zero operator in (3.4) commutes with
   \(x\)-translations and central inversion.  Translation by
   \(\pi/(2m\alpha)\) maps that whole fixed-\(m\) cosine block to its
   negative sine block, so the inversion-odd sector has the identical kernel
   condition.  Negative \(m\) are conjugate copies (equivalently, relabel
   \(n\)); hence these two blocks cover all \(m\ne0\) Fourier modes.  For
   \(m=0\) and \(\sigma=0\), (3.4) reduces to
   \(-R^{-1}\Delta^2\phi=0\).  Its periodic solutions are constants, whose
   velocity is zero and whose stream-function gauge is removed by the
   normalization.  Thus Proposition 1 excludes zero spectrum in the complete
   mean-zero planar phase space except at the listed characteristic values;
   in particular, the value enclosed in (4.1) is
   \(R_c=\lambda(0.7)\).
3. Watanabe's primary-source account independently uses the same
   nondimensionalization and identifies the \(\alpha=0.7\) number enclosed by
   Nagatou as the critical Reynolds number at which the basic flow loses
   stability.  This is corroboration of the identification
   \(R_c=\lambda(0.7)\), not a substitute for the continuation argument below.
4. Ilyin's Theorem 5.1 supplies a nonempty positive spectrum at a finite
   high-parameter anchor.  We specialize the theorem before comparing
   parameters: set \(L=2\pi\), so Ilyin's torus is
   \((0,2\pi/\alpha)\times(0,2\pi)\), his force and equilibrium are
   respectively
   \(f=(\Lambda\nu^2\sin x_2,0)\) and
   \(\bar U=(\Lambda\nu\sin x_2,0)\), and therefore
   \(R=A/(\nu N)=\Lambda\).  For every
   \(\Lambda>\Lambda_0(\alpha)\), Theorem 5.1 gives
   \(\lfloor1/\alpha\rfloor_*\) distinct positive real eigenvalues, where
   \(\lfloor x\rfloor_*\) counts positive integers strictly below \(x\).
   Only their existence, not the number of distinct eigenvalues, is used
   below.  No general-\(L\) normalization is asserted here.

Here is the operator-theoretic part of the proof.  The first-order operator

\[
 Bv=-P\bigl(U\cdot\nabla v+v\cdot\nabla U\bigr)
\]

is \(P\Delta\)-bounded with relative bound zero, since for every
\(\varepsilon>0\)

\[
 \|Bv\|_2\le C(\|\nabla v\|_2+\|v\|_2)
 \le\varepsilon\|\Delta v\|_2+C_\varepsilon\|v\|_2,
 \qquad v\in D.
\]

Consequently \(\{\mathcal A_R:R>0\}\) is a common-domain analytic family of
type (A).  More explicitly, on any compact \(K\Subset(0,\infty)\), the Stokes
resolvent estimates and the preceding relative-bound inequality give

\[
 \sup_{R\in K}\left\|B
 (\mu-R^{-1}P\Delta)^{-1}\right\|_{H\to H}<1
\]

for all sufficiently large real \(\mu\).  Hence

\[
 (\mu-\mathcal A_R)^{-1}
 =(\mu-R^{-1}P\Delta)^{-1}
 \left[I-B(\mu-R^{-1}P\Delta)^{-1}\right]^{-1}.
\]

The first factor maps \(H\) into \(D\), and \(D\hookrightarrow H\) is
compact.  Thus every \(\mathcal A_R\) has compact resolvent and only isolated
eigenvalues of finite algebraic multiplicity; the same estimates give uniform
sectoriality on \(K\).  These statements are the standard elliptic-operator
derivation, rather than an additional claim quoted from Nagatou,
Matsuda--Miyatake, or Ilyin.

The high-frequency control needed for continuation is explicit.  Let
\(M=\|\nabla U\|_\infty\) and \(M_0=\|U\|_\infty\).  If
\(\mathcal A_Rv=\zeta v\), then incompressibility and periodic integration by
parts give

\[
 \operatorname{Re}\zeta\,\|v\|_2^2
 =-{1\over R}\|\nabla v\|_2^2
 -\operatorname{Re}\langle v\cdot\nabla U,v\rangle.
\]

Thus, whenever \(\operatorname{Re}\zeta\ge0\) and
\(R\in[3.012,R_H]\),

\[
 \|\nabla v\|_2\le\sqrt{R_HM}\,\|v\|_2,
 \qquad 0\le\operatorname{Re}\zeta\le M.
\]

Taking imaginary parts of the same eigenvalue equation gives

\[
 |\operatorname{Im}\zeta|
 \le M_0{\|\nabla v\|_2\over\|v\|_2}+M
 \le M_0\sqrt{R_HM}+M.
\]

For the present \(U=(\sin y,0)\), \(M=M_0=1\).  Hence, uniformly for
\(R\in[3.012,R_H]\), all closed-right-half-plane spectrum lies in the fixed
compact rectangle

\[
 [0,1]+i[-(\sqrt{R_H}+1),\sqrt{R_H}+1].
\]

This prevents a right-half-plane eigenvalue from entering or leaving through
spectral infinity.

Choose a finite \(R_H>\max\{\Lambda_0(0.7),3.012\}\).  Ilyin makes the
right-half-plane Riesz projection nonzero at \(R_H\).  On the whole compact
interval \([3.012,R_H]\), Nagatou excludes every nonzero imaginary-axis
eigenvalue.  The full-sector argument in item 2 excludes zero: the
\(|m|=1\) block is neutral only at \(R=\lambda(0.7)=R_c<3.012\), and
\(|m|\ge2\) has \(\beta=|m|\alpha\ge1\).

For completeness, suppose the positive-real-part spectrum on this interval
were not uniformly separated from the imaginary axis.  The fixed rectangle
would give
\(R_j\to R_*\) and eigenvalues \(\zeta_j\to\zeta_*\in i\mathbb R\).
Norm-resolvent continuity of the common-domain analytic family then implies
\(\zeta_*\in\operatorname{spec}(\mathcal A_{R_*})\), contradicting the
preceding exclusion.  Consequently there is a uniform \(\delta>0\) such that
every eigenvalue with positive real part satisfies
\(\operatorname{Re}\zeta\ge\delta\).  One may therefore take \(\Gamma\) to
be the boundary of the rectangle with left edge
\(\operatorname{Re}z=\delta/2\), right edge
\(\operatorname{Re}z=2\), and horizontal edges
\(|\operatorname{Im}z|=\sqrt{R_H}+2\).  This single contour lies in the
resolvent set and separates the complete right-half-plane spectrum for every
\(R\in[3.012,R_H]\).  Its Riesz projection

\[
 \Pi_R={1\over2\pi i}\int_\Gamma
 (z-\mathcal A_R)^{-1}\,dz
\]

depends continuously on \(R\).  The integer \(\operatorname{rank}\Pi_R\),
which is the total algebraic multiplicity of all eigenvalues with positive
real part, is therefore constant.  This is the continued quantity; the
number of distinct eigenvalues is not used and need not be invariant under
collisions inside the open right half-plane.  Since
\(\operatorname{rank}\Pi_{R_H}>0\), also
\(\operatorname{rank}\Pi_{3.012}>0\).

For \(\alpha=0.7\), \(\lfloor1/\alpha\rfloor_*=1\), and

\[
 3.012>3.011528364446,
 \tag{4.2}
\]

with margin \(4.71635554\times10^{-4}\).  Therefore the planar linearized
operator at \(U_*\) has at least one positive real eigenvalue and a smooth
eigenfunction.  Constant extension in \(z\) places the same eigenvalue in the
full three-dimensional linearized operator.

The finite Fourier truncation gives

\[
 \sigma_{\max}^{(120)}(3.012)
 \approx3.7327236416\times10^{-5},
 \qquad
 \lambda^{(120)}=301.2\sigma_{\max}^{(120)}
 \approx1.1242963608\times10^{-2}.
 \tag{4.3}
\]

This independently checks the sign and all scaling factors but has no
infinite-tail interval bound.  It is diagnostic evidence only and does not
replace the one-sided theorem chain above.

The source boundary is important. The often quoted value
\(R_c=\sqrt2\) is a long-wave limit as \(\alpha\to0\), not the critical value
at fixed \(\alpha=0.7\). The use of \(N=10,m=7\) embeds the verified
rectangular geometry in the standard cubic torus exactly.

## 5. From spectrum to nonlinear escape

Apply Friedlander--Pavlović--Shvydkoy Theorem 2.2 first on the invariant
two-dimensional mean-zero phase space (H), with

\[
 n=2,\qquad p=2,\qquad q=4.
\]

Their theorem turns right-half-plane \(L^2\) spectrum of a smooth forced
equilibrium into nonlinear \((L^4,L^2)\) instability. On a finite domain the
unstable eigenfunction is \(C^\infty\), and the proof explicitly permits the
size of the initial perturbation to be measured in any stronger smooth norm
while retaining fixed escape in the weak \(L^2\) metric.  Thus there are
smooth two-dimensional data tending to zero in every fixed Sobolev norm and a
fixed two-dimensional \(L^2\) escape.

Let \(E\) extend a planar vector field constantly in \(z\).  For a fixed
normalization of Lebesgue measure there is a fixed \(c_z>0\) such that

\[
 \|Eg\|_{H^3(\mathbb T^3)}=c_z\|g\|_{H^3(\mathbb T^2)},
 \qquad
 \|Eg\|_{L^2(\mathbb T^3)}=c_z\|g\|_{L^2(\mathbb T^2)}.
 \tag{5.1}
\]

For unnormalized measure, \(c_z=(2\pi)^{1/2}\).  Constant extension therefore
gives (1.3) and (1.4), with the escape radius multiplied by \(c_z\).  This
two-dimensional-first application is essential: applying FPS directly in
three dimensions would not let one prescribe that its selected rightmost
eigenfunction is planar.

There is one extra global-existence issue in the general three-dimensional
definition of instability: loss of the global strong solution is itself an
instability alternative. It does not occur here. Both \(U_*\) and the chosen
perturbations are planar, the planar subspace is invariant, and
two-dimensional periodic Navier--Stokes solutions from smooth data are global
and smooth. Thus the fixed \(L^2\) escape in (1.4) is the actual conclusion.

## 6. What this theorem establishes and excludes

The closed chain establishes the clean logical contrast

\[
\begin{array}{c|c}
\text{unforced a priori global orbit}&
\int_0^\infty\|u(t)\|_{H^4}\,dt<\infty
\ \Longrightarrow\ \text{positive }H^3\text{ tube},\\[2mm]
\text{forced nondecaying equilibrium}&
\text{positive autonomous spectrum}
\ \Longrightarrow\ H^3\text{-small}/L^2\text{-fixed escape}.
\end{array}
\]

It does not establish finite-time blow-up, loss of uniqueness, an anomalous
energy law, turbulence, or any implication for the unforced Clay equation.
Indeed, every escaping solution in this construction is globally smooth.

## 7. Primary theorem chain

1. L. D. Meshalkin and Ya. G. Sinai, *Investigation of the stability of a
   stationary solution of a system of equations for the plane movement of an
   incompressible viscous liquid*, J. Appl. Math. Mech. 25 (1961/62),
   1700--1705, DOI
   [10.1016/0021-8928(62)90149-1](https://doi.org/10.1016/0021-8928(62)90149-1).
2. K. Nagatou, *A computer-assisted proof on the stability of the Kolmogorov
   flows of incompressible viscous fluid*, J. Comput. Appl. Math. 169 (2004),
   33--44, DOI
   [10.1016/j.cam.2003.10.016](https://doi.org/10.1016/j.cam.2003.10.016).
3. M. Matsuda and S. Miyatake, *Bifurcation analysis of Kolmogorov flows*,
   Tohoku Math. J. 54 (2002), 329--365, Proposition 1, DOI
   [10.2748/tmj/1113247600](https://doi.org/10.2748/tmj/1113247600).
4. A. A. Ilyin, *Lieb--Thirring integral inequalities and their applications
   to attractors of the Navier--Stokes equations*, Sbornik Math. 196 (2005),
   29--61, Theorem 5.1, DOI
   [10.1070/SM2005v196n01ABEH000871](https://doi.org/10.1070/SM2005v196n01ABEH000871).
5. Y. Watanabe, *A computer assisted proof of the Kolmogorov problem of
   incompressible viscous fluid*, RIMS Kôkyûroku 1905 (2014), 132--143,
   [first-party PDF](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1905-11.pdf),
   Section 7.
6. S. Friedlander, N. Pavlović, and R. Shvydkoy, *Nonlinear instability for
   the Navier--Stokes equations*, Comm. Math. Phys. 264 (2006), 335--347,
   [arXiv:math/0508173](https://arxiv.org/abs/math/0508173), DOI
   [10.1007/s00220-006-1526-7](https://doi.org/10.1007/s00220-006-1526-7).
7. T. Kato, *Perturbation Theory for Linear Operators*, second edition,
   Springer, Chapters III.6 and VII.1--2, DOI
   [10.1007/978-3-642-66282-9](https://doi.org/10.1007/978-3-642-66282-9).

The spectral interval in (4.1), the scaling (3.3)--(3.6), and the exact FPS
topology are each reproduced independently in the R0.73O source ledger and
audit rather than being treated as an unexamined citation chain.
