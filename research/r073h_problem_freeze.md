# R0.73H problem freeze: gain-normalized planar departure

**Frozen:** 2026-08-30  
**Parent release:** R0.73G  
**Physical realization:** viscosity one, shear frequency \(R=2\),
\(K_x=0\), real \(K_z=\pm1\) launch  
**Evidence target:** a fixed-distance nonlinear departure for a seed
normalized by the exact selected linear gain

## 1. Background and inherited input

The exact unforced background is

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr),
 \qquad
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.1}
\]

R0.73F supplies \(d_0,K_{\rm F},\alpha,\eta>0\) and a moving unstable
bundle on the real \(K_z=\pm1\) pair.  Fix

\[
 r=\alpha+\eta>0.17035,
 \qquad
 D=\min\{d_0,1/450\},
 \qquad
 T=D/4.
 \tag{1.2}
\]

For sufficiently large \(\Lambda\), use the real unit conjugate launch
\(\phi_\Lambda\) constructed in R0.73G from a normalized frozen top
eigenvector.  Define the actual selected gain

\[
 G_\Lambda
 =\|S_{1,\Lambda}(D,0)\phi_\Lambda\|_2.
 \tag{1.3}
\]

The inherited requirements are

\[
 G_\Lambda\ge K_{\rm F}^{-1}e^{r\Lambda D},
 \tag{1.4}
\]

and the interval backward estimate

\[
 \left\|
 \frac{S_{1,\Lambda}(s,0)\phi_\Lambda}{G_\Lambda}
 \right\|_2
 \le K_{\rm F}e^{-r\Lambda(D-s)},
 \qquad0\le s\le D.
 \tag{1.5}
\]

Equation (1.5), not a coarse forward Sobolev estimate, is the localization
input.

## 2. Exact slow-time equation

In profile time \(d=4t\), keep physical velocity amplitude and define

\[
 \mathcal B(f,g)=-\frac14\mathbb P[(f\cdot\nabla)g].
 \tag{2.1}
\]

Then

\[
 \partial_du=\mathcal L_\Lambda(d)u+\mathcal B(u,u),
 \qquad\nabla\cdot u=0.
 \tag{2.2}
\]

The exact planar subspace

\[
 \mathcal S_{2D}
 =\{(0,u_2(y,z),u_3(y,z)):
 \partial_yu_2+\partial_zu_3=0\}
 \tag{2.3}
\]

is invariant and globally regular.

## 3. Contract H1: harmonic Taylor hierarchy

Set

\[
 a(d)=G_\Lambda^{-1}S_{1,\Lambda}(d,0)\phi_\Lambda,
 \tag{3.1}
\]

and define

\[
 \begin{aligned}
 \partial_db&=\mathcal L_\Lambda b+\mathcal B(a,a),
 &b(0)&=0,\\
 \partial_dc&=\mathcal L_\Lambda c
 +\mathcal B(a,b)+\mathcal B(b,a),
 &c(0)&=0.
 \end{aligned}
 \tag{3.2}
\]

The section must prove

\[
 a:\ \pm1,
 \qquad
 b:\ 0,\pm2,
 \qquad
 c:\ \pm1,\pm3.
 \tag{3.3}
\]

The positive cubic target must include the four ordered paths

\[
 (1,0),\quad(0,1),\quad(-1,2),\quad(2,-1).
 \tag{3.4}
\]

The exact one-dimensional Leray profiles must be compared against a generic
physical Fourier convolution.  Finite agreement may validate the formulas
and code path, but may not carry a continuum theorem.

## 4. Contract H2: doubled-row continuum energy

For a nonzero row \(K_z=q\), put \(\gamma=|q|/2\) and

\[
 E_\gamma(v)=\|v'\|_2^2+\gamma^2\|v\|_2^2.
 \tag{4.1}
\]

The inviscid numerical form is

\[
 \operatorname{Re}\langle A_\gamma(d)v,v\rangle_{E_\gamma}
 =\gamma\operatorname{Im}\int W_x(d,x)v'\bar v.
 \tag{4.2}
\]

The universal estimate is \(\omega_\gamma(d)\le1/2\).  The doubled row
must satisfy the sharper continuum bound

\[
 \boxed{
 \omega_1(d)\le\frac13,
 \qquad0\le d\le D.}
 \tag{4.3}
\]

The permitted proof route is the two-sign periodic gauge reduction to

\[
 H_d=-\partial_x^2+1-\frac94W_x(d,x)^2.
 \tag{4.4}
\]

At \(d=0\), an exact rational \(|m|\le4\) block, an analytic tail and
cross-block estimate, and a two-by-two Schur bound must prove

\[
 H_0\ge\frac1{20}I.
 \tag{4.5}
\]

The explicit profile perturbation for \(d\le1/450\) must then give
\(H_d\ge1/40\).  A floating-point eigenvalue plot is not an acceptable
replacement.

## 5. Contract H3: localized coefficient energy

For each field \(h\), write

\[
 Y_h(s)=\|h(s)\|_2^2,
 \qquad
 M_h(s)=\frac14\int_0^s\|\nabla h(\tau)\|_2^2\,d\tau.
 \tag{5.1}
\]

Backward localization, two-dimensional Ladyzhenskaya, and a Stieltjes
product-measure lemma must prove constants independent of large
\(\Lambda\) such that

\[
 \begin{aligned}
 Y_a(s)+M_a(s)&\le C_ae^{-2r\Lambda(D-s)},\\
 Y_b(s)+M_b(s)&\le C_be^{-4r\Lambda(D-s)},\\
 Y_c(s)+M_c(s)&\le C_ce^{-6r\Lambda(D-s)}.
 \end{aligned}
 \tag{5.2}
\]

The strict rate gates are

\[
 \frac13<2r,
 \qquad
 \frac12<3r,
 \qquad
 \frac12<4r.
 \tag{5.3}
\]

No uniform high-Sobolev propagation may be assumed.

## 6. Contract H4: fourth-order remainder and endpoint

For fixed \(0<\delta\le1\), define

\[
 u_{\rm app}=\delta a+\delta^2b+\delta^3c.
 \tag{6.1}
\]

Its residual must begin at fourth order:

\[
 \begin{aligned}
 R_{\rm app}={}&\delta^4[
 \mathcal B(a,c)+\mathcal B(c,a)+\mathcal B(b,b)]\\
 &+\delta^5[
 \mathcal B(b,c)+\mathcal B(c,b)]
 +\delta^6\mathcal B(c,c).
 \end{aligned}
 \tag{6.2}
\]

The exact solution has initial perturbation

\[
 u_\Lambda^\delta(0)=\frac\delta{G_\Lambda}\phi_\Lambda.
 \tag{6.3}
\]

The error \(e=u_\Lambda^\delta-u_{\rm app}\) must use the exact transport
cancellations, retain the single
\(\|\nabla u_{\rm app}\|_2^2\|e\|_2^2\) term, and prove

\[
 \|e(D)\|_2\le C\delta^4.
 \tag{6.4}
\]

Since \(b\) has no target row, the required endpoint is

\[
 \boxed{
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\delta(D)\|_2
 \ge\delta-C_3\delta^3-C_4\delta^4
 \ge\frac\delta2.}
 \tag{6.5}
\]

The seed must simultaneously satisfy

\[
 \|u_\Lambda^\delta(0)\|_{H^3}
 \le C\delta\Lambda^2e^{-r\Lambda D}\longrightarrow0.
 \tag{6.6}
\]

## 7. Finite diagnostic contract

The finite computation must use \(\rho\) for launch amplitude and
\(\varepsilon_\nu=\Lambda^{-1}\) for the singular parameter.  It must
archive complex coefficient snapshots, mean and doubled cubic paths,
cutoff and time-step comparisons, an independent alias-free FFT
implementation, progress logs, environment, and hashes.

All finite sizes, slopes, plateaus, and signs remain binary64 Galerkin
evidence.  They do not prove a continuum Taylor radius, Fourier-tail
enclosure, natural-seed theorem, or saturation law.

## 8. Claim boundary

If H1--H4 pass, the following may be marked CLOSED:

- exact harmonic hierarchy through cubic order;
- continuum doubled-row \(1/3\) bound;
- localized quadratic and cubic coefficient energy;
- fourth-order exact remainder;
- gain-normalized fixed-distance nonlinear departure;
- global smoothness of every selected orbit.

The following remain OPEN:

- matching upper and lower action for \(G_\Lambda\);
- fixed-distance departure for the prescribed seed
  \(\delta e^{-r\Lambda D}\);
- one fixed background with a Lyapunov-instability sequence;
- any transverse \(K_x\ne0\) or nonzero first velocity component;
- three-dimensional vortex stretching, finite-time singularity, or the
  Clay alternative.

The theorem is stronger than R0.73G's vanishing endpoint, but remains
inside a globally regular two-dimensional invariant subsystem.
