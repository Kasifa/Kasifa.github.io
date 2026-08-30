# R0.73M proof: prescribed-action planar nonlinear departure

**Status:** continuum proof closed; independent analytic, adversarial, and
literature audits PASS; finite and publication gates remain separate

**Depends on:** the sealed R0.73H harmonic/remainder estimates and the sealed
R0.73L two-sided action and forward-orbit localization theorem

## 1. Statement

Use the exact background, selected launch, and notation in
`research/r073m_problem_freeze.md`.  In particular,

\[
 D_*={1\over450},\qquad T_*={1\over1800},\qquad
 \mathcal A_*:=\int_0^{D_*}\lambda_0(r)\,\mathrm dr,
 \qquad \mu_*:={167\over1000}.
 \tag{1.1}
\]

There exist \(\rho_0,c_*>0\) and \(\Lambda_0<\infty\) such that every
\(\Lambda\ge\Lambda_0\) and \(0<\rho\le\rho_0\) admit a global smooth
Navier--Stokes solution with initial datum

\[
U_\Lambda^\rho(0)=\overline U_\Lambda(0)
+\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda
\tag{1.2}
\]

Write the perturbation in profile time as

\[
 u_\Lambda^\rho(d)
 :=U_\Lambda^\rho(d/4)-\overline U_\Lambda(d/4).
 \tag{1.2a}
\]

whose perturbation satisfies

\[
 \|\Pi_{\{K_z=\pm1\}}
 (U_\Lambda^\rho(T_*)-\overline U_\Lambda(T_*))\|_2
 \ge c_*\rho.
 \tag{1.3}
\]

Moreover, the perturbation in (1.2) tends to zero in \(H^3\) as
\(\Lambda\to\infty\).

## 2. Exact kinetic-to-physical conjugacy

Put \(\varepsilon=\Lambda^{-1}\).  R0.73K--L use
\(H=L^2(\mathbb T_{2\pi})\) and

\[
 \varepsilon\partial_du=B_\varepsilon(d)u,
 \qquad B_\varepsilon(d)=\widetilde A(d)-\varepsilon L.
 \tag{2.1}
\]

The positive physical row \(K_z=1\), after the fixed change \(x=2y\), is
obtained by the map

\[
 \mathcal Eh(y,z)=
 \left(0,{1\over2}(L^{-1/2}h)(2y),
 i(\partial_xL^{-1/2}h)(2y)\right)e^{iz}.
 \tag{2.2}
\]

The normalization of the kinetic space was chosen so that \(\mathcal E\) is
an isometry into physical velocity \(L^2\).  It intertwines (2.1) with the
positive-row physical linear equation in profile time.  Complex conjugation
intertwines the positive and negative rows.  Since those rows are orthogonal,

\[
 \phi_\Lambda=2^{-1/2}
 (\mathcal Eh_\varepsilon(0)+\overline{\mathcal Eh_\varepsilon(0)})
 \tag{2.3}
\]

has unit norm and, for every \(0\le d\le D_*\),

\[
 \|S_{\pm1,\Lambda}(d,0)\phi_\Lambda\|_2
 =\|U_\varepsilon(d,0)h_\varepsilon(0)\|_H.
 \tag{2.4}
\]

Here \(S_{\pm1,\Lambda}(d,s)\) denotes the profile-time linear evolution on
the real conjugate pair.  Thus the scalar and real-pair gains are exactly
equal; no norm-equivalence or time-rescaling constant is hidden here.

## 3. The selected action and the normalized forward orbit

R0.73L and (2.4) give constants \(0<c_L\le C_L<\infty\) such that

\[
 c_Le^{\Lambda\mathcal A_*}
 \le G_\Lambda^*
 :=\|S_{\pm1,\Lambda}(D_*,0)\phi_\Lambda\|_2
 \le C_Le^{\Lambda\mathcal A_*}.
 \tag{3.1}
\]

For

\[
 a_\Lambda(s)
 =(G_\Lambda^*)^{-1}S_{\pm1,\Lambda}(s,0)\phi_\Lambda,
 \tag{3.2}
\]

one has \(\|a_\Lambda(D_*)\|_2=1\).  The R0.73L forward-orbit quotient
estimate gives

\[
 \begin{aligned}
 \|a_\Lambda(s)\|_2
 &\le C_L\exp\!\left[-\Lambda
       \int_s^{D_*}\lambda_0(r)\,dr\right]\\
 &\le C_Le^{-\mu_*\Lambda(D_*-s)}.
 \end{aligned}
 \tag{3.3}
\]

The last inequality uses the strict R0.73J floor
\(\lambda_0(r)>0.167=\mu_*\).  It is acceptable to retain the weak floor
\(\mu_*\) in (3.3), because the inequalities below remain strict at that
value.

## 4. Transfer lemma for the nonlinear Taylor hierarchy

The R0.73H proof can be isolated in the following form.

**Lemma 4.1 (localized planar nonlinear response).**  Fix
\(0<D\le1/450\), \(\mu>1/6\), and \(C_a<\infty\), all independent of
\(\Lambda\).  Let \(\mathcal L_\Lambda\) be the profile-time linearization
about the fixed two-harmonic background in
`research/r073m_problem_freeze.md`, equation (1.1):

\[
 \mathcal L_\Lambda(d)h={1\over4}\left\{
 \Delta h-\mathbb P\left[
 \overline U_\Lambda(d/4)\cdot\nabla h
 +h\cdot\nabla\overline U_\Lambda(d/4)\right]\right\}.
 \tag{4.0}
\]

Suppose one mean-zero, endpoint-normalized real \(K_z=\pm1\) linear orbit
satisfies

\[
 \|a(s)\|_2\le C_ae^{-\mu\Lambda(D-s)},
 \qquad \|a(D)\|_2=1.
 \tag{4.1}
\]

Assume the row estimates proved in R0.73H for this same background,
uniformly on \([0,D]\): the zero row is a mean-zero heat shear, every
nonzero row has inviscid numerical abscissa at most \(1/2\), and the doubled
rows \(K_z=\pm2\) have numerical abscissa at most \(1/3\).  For the exact
planar perturbation equation

\[
 \partial_du=\mathcal L_\Lambda(d)u+\mathcal B(u,u),
 \qquad
 \mathcal B(f,g)=-{1\over4}\mathbb P[(f\cdot\nabla)g],
 \tag{4.2}
\]

there are \(\delta_0,C_3,C_R>0\), independent of sufficiently large
\(\Lambda\), such that the solution with \(u(0)=\delta a(0)\),
\(0<\delta\le\delta_0\), is global and satisfies

\[
 \|\Pi_{\{K_z=\pm1\}}u(D)\|_2
 \ge\delta-C_3\delta^3-C_R\delta^4
 \ge{\delta\over2}.
 \tag{4.3}
\]

**Proof.**  Define the second and third Taylor coefficients by

\[
 \begin{aligned}
 \partial_db&=\mathcal L_\Lambda b+\mathcal B(a,a),&b(0)&=0,\\
 \partial_dc&=\mathcal L_\Lambda c
 +\mathcal B(a,b)+\mathcal B(b,a),&c(0)&=0.
 \end{aligned}
 \tag{4.4}
\]

The background is independent of \(z\), and Fourier labels add under
\(\mathcal B\).  More explicitly, if \(S_{q,\Lambda}(d,s)\) is the exact
non-autonomous linear evolution on row \(q\), then every row of the exact
solution obeys

\[
 u_q(d)=S_{q,\Lambda}(d,0)u_q(0)
 +\sum_{k+\ell=q}\int_0^d
 S_{q,\Lambda}(d,s)\mathcal B_q(u_k,u_\ell)(s)\,\mathrm ds.
 \tag{4.4a}
\]

This is an identity in the continuum equation, not a Fourier truncation.
It gives

\[
 a:\ \pm1,\qquad b:\ 0,\pm2,\qquad c:\ \pm1,\pm3,
 \qquad \Pi_{\{\pm1\}}b=0.
 \tag{4.5}
\]

Spatial mean zero propagates because the two linearized-background terms
and every bilinear forcing are divergences of periodic tensors.  Hence the
homogeneous two-dimensional Ladyzhenskaya inequality used below applies to
\(a,b,c\), the exact perturbation, the approximation, and the error.

For a nonzero row with \(\gamma=|K_z|/2\), the inviscid numerical form
obeys the universal upper bound \(1/2\).  On the doubled row
\(\gamma=1\), the exact periodic gauge and the R0.73H rational-tail
certificate give

\[
 \omega_1(d)\le{1\over3},
 \qquad0\le d\le{1\over450}.
 \tag{4.6}
\]

For a planar field \(h\), set

\[
 Y_h(s)=\|h(s)\|_2^2,
 \qquad
 M_h(s)={1\over4}\int_0^s\|\nabla h(\tau)\|_2^2\,d\tau.
 \tag{4.7}
\]

The linear energy identity, (4.1), and (4.6), followed by the Stieltjes
localization lemma from R0.73H, give

\[
 \begin{aligned}
 Y_a(s)+M_a(s)&\le C_1e^{-2\mu\Lambda(D-s)},\\
 Y_b(s)+M_b(s)&\le C_2e^{-4\mu\Lambda(D-s)},\\
 Y_c(s)+M_c(s)&\le C_3'e^{-6\mu\Lambda(D-s)}.
 \end{aligned}
 \tag{4.8}
\]

The strict conditions are

\[
 {1\over3}<2\mu,
 \qquad {1\over2}<3\mu,
 \tag{4.9}
\]

and follow from \(\mu>1/6\).  No pointwise high-Sobolev propagation is
used.

Put

\[
 u_{\rm app}=\delta a+\delta^2b+\delta^3c.
 \tag{4.10}
\]

Its residual begins at fourth order:

\[
 \begin{aligned}
 R_{\rm app}={}&\delta^4[
 \mathcal B(a,c)+\mathcal B(c,a)+\mathcal B(b,b)]\\
 &+\delta^5[\mathcal B(b,c)+\mathcal B(c,b)]
 +\delta^6\mathcal B(c,c).
 \end{aligned}
 \tag{4.11}
\]

For \(e=u-u_{\rm app}\), the exact transport cancellations remove
\(\langle\mathcal B(u_{\rm app},e),e\rangle\) and
\(\langle\mathcal B(e,e),e\rangle\).  Put

\[
 g=\|\nabla u_{\rm app}\|_2^2,
 \qquad
 \int_0^D g(s)\,\mathrm ds\le C\delta^2,
 \tag{4.11a}
\]

and define the nondecreasing product measures

\[
\begin{aligned}
 dN_4&=Y_a\,dM_c+Y_c\,dM_a+Y_b\,dM_b,\\
 dN_5&=Y_b\,dM_c+Y_c\,dM_b,\\
 dN_6&=Y_c\,dM_c.
\end{aligned}
 \tag{4.11b}
\]

Two-dimensional Ladyzhenskaya, (4.8), and the Stieltjes product-measure
argument give

\[
 N_j(s)\le C_j e^{-2j\mu\Lambda(D-s)},
 \qquad j=4,5,6.
 \tag{4.11c}
\]

The exact error energy inequality is

\[
 {1\over2}dY_e+{1\over2}dM_e
 \le\left({\Lambda\over2}+Cg\right)Y_e\,ds
 +C\left(\delta^8dN_4+\delta^{10}dN_5
 +\delta^{12}dN_6\right).
 \tag{4.11d}
\]

Its integrating factor from \(t\) to \(s\) is bounded by
\(e^{C_0\delta^2}e^{\Lambda(s-t)}\).  The leading strict condition is
\(1<8\mu\), equivalent to \(1/2<4\mu\).  A final Stieltjes estimate and
integration of the cumulative dissipation yield

\[
 Y_e(s)+M_e(s)
 \le C_e e^{C_0\delta^2}\delta^8
 e^{-8\mu\Lambda(D-s)}
 \tag{4.11e}
\]

and therefore

\[
 \|e(D)\|_2\le C_R\delta^4,
 \tag{4.12}
\]

provided

\[
 {1\over2}<4\mu.
 \tag{4.13}
\]

Again \(\mu>1/6\) is stronger than needed for (4.13).  At the endpoint,
the linear target has norm \(\delta\), the quadratic target vanishes by
(4.5), and (4.8), (4.12) give

\[
 \|\Pi_{\{\pm1\}}u(D)\|_2
 \ge\delta-C_3\delta^3-C_R\delta^4.
 \tag{4.14}
\]

Choose \(\delta_0\le1\) so that
\(C_3\delta_0^2+C_R\delta_0^3\le1/2\).  The full field remains in the
exact planar invariant subsystem, so standard two-dimensional vorticity
energy gives global smoothness independently of the quantitative remainder
estimate.  This proves the lemma. \(\square\)

For R0.73M, take \(D=D_*\) and \(\mu=\mu_*\).  The narrowest strict margin
is

\[
 2\mu_*-{1\over3}={1\over1500}>0,
 \tag{4.15}
\]

while

\[
 3\mu_*-{1\over2}={1\over1000}>0,
 \qquad
 4\mu_*-{1\over2}={21\over125}>0.
 \tag{4.16}
\]

Thus every constant in Lemma 4.1 is finite and independent of sufficiently
large \(\Lambda\), although no useful numerical size is asserted.
Fix \(\Lambda_0\) to be the maximum of the finitely many thresholds in the
R0.73J--L action theorem, the R0.73G elliptic estimate, and Lemma 4.1.

## 5. From the prescribed seed to a uniform Taylor amplitude

Define the action-normalized gain

\[
 g_\Lambda:=G_\Lambda^*e^{-\Lambda\mathcal A_*}.
 \tag{5.1}
\]

By (3.1),

\[
 c_L\le g_\Lambda\le C_L.
 \tag{5.2}
\]

For a prescribed seed coefficient \(\rho\), set

\[
 \delta_\Lambda:=\rho g_\Lambda.
 \tag{5.3}
\]

Then the physical initial perturbation is exactly

\[
 {\delta_\Lambda\over G_\Lambda^*}\phi_\Lambda
 =\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda.
 \tag{5.4}
\]

Choose

\[
 \rho_0:={\delta_0\over C_L}.
 \tag{5.5}
\]

For \(0<\rho\le\rho_0\), one has
\(0<\delta_\Lambda\le\delta_0\), so Lemma 4.1 applies.  Equations
(4.3) and (5.2) give

\[
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\rho(D_*)\|_2
 \ge{\delta_\Lambda\over2}
 \ge{c_L\over2}\rho.
 \tag{5.6}
\]

This proves (1.3) with \(c_*=c_L/2\).

## 6. Vanishing initial data and global existence

The launch has \(\|\phi_\Lambda\|_2=1\), hence

\[
 \|u_\Lambda^\rho(0)\|_2
 =\rho e^{-\Lambda\mathcal A_*}.
 \tag{6.1}
\]

The elliptic eigenvector bootstrap from R0.73G applies to the same
rank-one viscous branch and gives

\[
 \|\phi_\Lambda\|_{H^3}\le C\Lambda^2.
 \tag{6.2}
\]

Therefore

\[
 \|u_\Lambda^\rho(0)\|_{H^3}
 \le C\rho\Lambda^2e^{-\Lambda\mathcal A_*}\longrightarrow0.
 \tag{6.3}
\]

The action is strictly positive and explicitly bracketed:

\[
 {167\over450000}<\mathcal A_*<{173\over450000}.
 \tag{6.4}
\]

Both the background and the real launch lie in

\[
 \mathcal S_{2D}
 =\{(0,u_2(y,z),u_3(y,z)):
 \partial_yu_2+\partial_zu_3=0\}.
 \tag{6.5}
\]

This subspace is invariant, and its scalar vorticity obeys the periodic
two-dimensional Navier--Stokes enstrophy identity.  Every selected orbit is
therefore global and smooth.

## 7. Why the full action, not only its rate floor, fixes the seed scale

For comparison, prescribe a constant-slope seed
\(\rho e^{-\sigma\Lambda D_*}\phi_\Lambda\).  Its effective Taylor
amplitude obeys

\[
 \delta_\Lambda
 =\rho G_\Lambda^*e^{-\sigma\Lambda D_*}
 \asymp\rho\exp\{\Lambda(\mathcal A_*-\sigma D_*)\}.
 \tag{7.1}
\]

If \(\sigma D_*<\mathcal A_*\), this amplitude eventually leaves every
uniform Taylor radius, so the present fixed-endpoint bootstrap cannot
close.  The estimates (4.8) and (4.11e) also give the explicit upper bound

\[
 \|u(D)\|_2
 \le \delta+C\delta^2+C\delta^3+C\delta^4
 \le C'\delta,
 \qquad0<\delta\le\delta_0.
 \tag{7.2}
\]

If \(\sigma D_*>\mathcal A_*\), this bound makes the endpoint tend to zero
with \(\delta_\Lambda\).  Within this construction, a uniform-small
Taylor amplitude and a fixed-distance endpoint can coexist only at the
action-matching scale

\[
 \sigma D_* = \mathcal A_*+O(\Lambda^{-1}).
 \tag{7.3}
\]

In particular, the floor seed
\(\rho e^{-0.167\Lambda D_*}\phi_\Lambda\) is not licensed at \(D_*\):
the strict continuum inequality \(\mathcal A_*>0.167D_*\) makes its
effective Taylor amplitude grow exponentially.  The prescribed-action seed
used in (1.2) is the exact recoding justified by the bounded prefactor.

## 8. Result ledger and exact boundary

The continuum proof establishes

```text
physicalKineticSelectedGainConjugacy=CLOSED
fixedEndpointBackwardLocalization=CLOSED_UPSTREAM
prescribedActionSeedWindow=CLOSED
twoDimensionalNonlinearDeparture=CLOSED
fixedDistanceEndpoint=CLOSED
selectedPlanarOrbitGlobalSmoothness=CLOSED_UPSTREAM
prefactorLimit=OPEN
twoTermWKB=OPEN
singleFixedBackgroundLyapunovInstability=OPEN
transverseThreeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

The theorem is stronger than the R0.73H gain-normalized result because its
initial amplitude is specified by the inviscid action and no longer refers
to the unknown exact gain.  It remains a family-level result: the background
amplitude grows like \(\Lambda\), and all constructed trajectories stay in a
globally regular two-dimensional invariant subspace.  No three-dimensional
vortex-stretching or regularity conclusion follows.
