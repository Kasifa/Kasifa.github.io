# R0.73M problem freeze: prescribed-action planar nonlinear departure

**Status:** frozen contract; continuum proof, independent analytic,
adversarial and literature audits, and sealed finite diagnostic PASS; the
release remains incomplete until the figure and publication gates pass

**Slow endpoint:** \(D_*:=1/450\)

**Physical endpoint:** \(T_*:=D_*/4=1/1800\)

**Operator row:** \((\beta,\xi,\gamma)=(0,0,1/2)\), realized by the real
physical \(K_z=\pm1\) conjugate pair

## 0. Direct decision

R0.73H proves a fixed-distance nonlinear departure for the seed
\(\delta G_\Lambda^{-1}\phi_\Lambda\), where \(G_\Lambda\) is the actual
selected linear gain.  R0.73I proves that a logarithmic action alone cannot
replace this gain: an unbounded prefactor would move the effective Taylor
amplitude outside the uniform nonlinear radius.

R0.73L supplies exactly the missing input on the fixed interval
\([0,D_*]\): the selected gain has a two-sided bounded prefactor relative to
the inviscid action.  R0.73M asks whether this permits the exact prescribed
seed

\[
 \rho e^{-\Lambda\mathcal A_*}\phi_\Lambda,
 \qquad
 \mathcal A_*:=\int_0^{D_*}\lambda_0(r)\,\mathrm dr,
 \tag{0.1}
\]

with \(\rho>0\) independent of \(\Lambda\), and whether the nonlinear orbit
then reaches a fixed \(L^2\) distance by time \(T_*\).

The proof must not cite R0.73H as a black box at its old shrinkable endpoint.
It must recheck the nonlinear localization budgets on the new fixed endpoint
using the R0.73J rate floor together with the R0.73L forward-orbit quotient

\[
 \mu_*:=\frac{167}{1000}>\frac16.
 \tag{0.2}
\]

## 1. Exact background and selected launch

On the standard three-torus, let

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr),
 \qquad
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.1}
\]

Since \(W_d=W_{xx}\), this is an exact, smooth, unforced Navier--Stokes
solution with viscosity one.  Put \(\varepsilon=\Lambda^{-1}\).  Let
\(h_\varepsilon(0)\) be a unit vector in the R0.73K rank-one spectral line
\(P_\varepsilon(0)H\), with its phase fixed by

\[
 \alpha(h_\varepsilon(0))
 ={1\over2}(L^{-1/2}h_\varepsilon(0))(0)>0.
 \tag{1.2}
\]

R0.73K proves that this anchor never vanishes on the branch.  The exact
kinetic-to-velocity map on the positive row is

\[
 \mathcal Eh(y,z)=
 \left(0,\frac12(L^{-1/2}h)(2y),
 i(\partial_xL^{-1/2}h)(2y)\right)e^{iz},
 \qquad L=-\partial_x^2+\frac14.
 \tag{1.3}
\]

Define the real unit launch

\[
 \phi_\Lambda=2^{-1/2}
 \left(\mathcal Eh_\varepsilon(0)
 +\overline{\mathcal Eh_\varepsilon(0)}\right).
 \tag{1.4}
\]

The positive and negative rows are orthogonal and conjugate, so their real
pair has exactly the same gain as the scalar kinetic row.  Let
\(S_{\pm1,\Lambda}(d,s)\) denote the profile-time evolution on that real
conjugate pair, and write

\[
 G_\Lambda^*
 :=\|S_{\pm1,\Lambda}(D_*,0)\phi_\Lambda\|_2.
 \tag{1.5}
\]

## 2. Inherited action theorem

R0.73J--L give

\[
 \frac{167}{1000}<\lambda_0(d)<\frac{173}{1000},
 \qquad 0\le d\le D_*,
 \tag{2.1}
\]

and constants \(0<c_L\le C_L<\infty\), independent of sufficiently large
\(\Lambda\), such that

\[
 c_Le^{\Lambda\mathcal A_*}
 \le G_\Lambda^*
 \le C_Le^{\Lambda\mathcal A_*}.
 \tag{2.2}
\]

The endpoint-normalized forward orbit

\[
 a_\Lambda(s)
 :=(G_\Lambda^*)^{-1}S_{\pm1,\Lambda}(s,0)\phi_\Lambda
 \tag{2.3}
\]

satisfies

\[
 \|a_\Lambda(s)\|_2
 \le C_L\exp\!\left[-\Lambda\int_s^{D_*}\lambda_0(r)\,dr\right]
 \le C_Le^{-\mu_*\Lambda(D_*-s)}.
 \tag{2.4}
\]

No backward parabolic evolution is used in (2.4); it is a quotient along one
forward orbit.

## 3. Target theorem

The section succeeds only if there are \(\rho_0,c_*,C_H >0\) and
\(\Lambda_0<\infty\) such that, for every \(\Lambda\ge\Lambda_0\) and every
\(0<\rho\le\rho_0\), the exact Navier--Stokes solution with

\[
 U_\Lambda^\rho(0)
 =\overline U_\Lambda(0)
 +\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda
 \tag{3.1}
\]

is global and smooth.  Define the physical-time perturbation and its
profile-time representation by

\[
 w_\Lambda^\rho(t):=U_\Lambda^\rho(t)-\overline U_\Lambda(t),
 \qquad
 u_\Lambda^\rho(d):=w_\Lambda^\rho(d/4).
 \tag{3.2}
\]

The endpoint obligation is

\[
 \boxed{
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\rho(D_*)\|_2
 =\|\Pi_{\{K_z=\pm1\}}w_\Lambda^\rho(T_*)\|_2
 \ge c_*\rho.}
 \tag{3.3}
\]

Thus the endpoint is physical time \(T_*=1/1800\), not \(D_*\).  The
initial data must simultaneously satisfy

\[
 \|w_\Lambda^\rho(0)\|_2
 =\rho e^{-\Lambda\mathcal A_*}\longrightarrow0,
 \tag{3.4}
\]

\[
 \|w_\Lambda^\rho(0)\|_{H^3}
 \le C_H\rho\Lambda^2e^{-\Lambda\mathcal A_*}
 \longrightarrow0.
 \tag{3.5}
\]

The theorem is an \(H^3\)-small to \(L^2\)-fixed-distance statement for a
family of backgrounds.  It is not Lyapunov instability of one fixed
background.

## 4. Proof obligations

| ID | Obligation | Admissible mechanism |
|---|---|---|
| M1 | scalar kinetic gain equals the physical real-pair gain | exact unitary velocity recovery, row orthogonality, and conjugacy |
| M2 | prescribed action and actual gain differ only by fixed factors | R0.73L two-sided action theorem at \(D_*\) |
| M3 | endpoint-normalized orbit localizes at a rate above \(1/6\) | R0.73L forward-orbit quotient and \(\lambda_0>0.167\) |
| M4 | the R0.73H Taylor hierarchy closes on \([0,D_*]\) | repeat the row-energy/Stieltjes proof with \(r\) replaced by \(\mu_*=0.167\) |
| M5 | the nonlinear Taylor amplitude stays uniformly small | \(\delta_\Lambda=\rho G_\Lambda^*e^{-\Lambda\mathcal A_*}\in[c_L\rho,C_L\rho]\) |
| M6 | fixed-distance endpoint and vanishing initial norms | harmonic parity, cubic correction, fourth-order remainder, and elliptic \(H^3\) cost |
| M7 | global existence and exact dimensional boundary | invariance of the planar subsystem and two-dimensional vorticity energy |
| M8 | literature and claim boundary | bounded primary-source collision search and explicit open ledger |

The tight rate margin is

\[
 2\mu_*-\frac13
 =\frac1{1500}>0.
 \tag{4.1}
\]

The other two margins are

\[
 3\mu_*-\frac12=\frac1{1000}>0,
 \qquad
 4\mu_*-\frac12=\frac{21}{125}>0.
 \tag{4.2}
\]

## 5. Mandatory stop conditions and forbidden shortcuts

- If the physical/kinetic conjugacy changes the norm or the slow-time factor,
  stop; no action transfer is licensed.
- If only \(\Lambda^{-1}\log G_\Lambda^*\to\mathcal A_*\) were known, stop;
  this does not control the effective Taylor amplitude.
- If the localization rate were \(\mu\le1/6\), stop; the doubled-row and
  cubic energy budgets would not be strict.
- Do not use the old shrinkable R0.73F endpoint in place of \(D_*\).
- Do not use a full-space high-Sobolev semigroup bound or a backward
  parabolic solve.
- Do not use a Fourier truncation to close M1--M8.
- Do not infer a prefactor limit from the bounded-prefactor theorem.
- Do not call a sequence of changing, unbounded-amplitude backgrounds one
  fixed-background Lyapunov instability.
- Do not promote planar global smoothness to a three-dimensional regularity
  conclusion.

## 6. Exact claim boundary

If M1--M8 close, the section may state

```text
physicalKineticSelectedGainConjugacy=CLOSED
fixedEndpointBackwardLocalization=CLOSED
prescribedActionSeedWindow=CLOSED
twoDimensionalNonlinearDeparture=CLOSED
fixedDistanceEndpoint=CLOSED
selectedPlanarOrbitGlobalSmoothness=CLOSED
prefactorLimit=OPEN
twoTermWKB=OPEN
singleFixedBackgroundLyapunovInstability=OPEN
transverseThreeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

The admissible conclusion is a prescribed-action, family-level nonlinear
departure theorem inside a globally regular two-dimensional invariant
subsystem.  It neither produces vortex stretching nor addresses the Clay
alternative.
