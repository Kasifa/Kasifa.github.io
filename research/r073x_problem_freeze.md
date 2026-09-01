# R0.73X problem freeze: localized heat characteristics and the defect ledger

**Frozen date:** 2026-09-01

**Status:** problem freeze and finite-diagnostic scope only; no analytic
theorem, certificate, or public release is asserted by this file

**Domain:** the normalized periodic torus
\(\mathbb T^3=[0,2\pi]^3\), with local balls of radius
\(0<R<\pi/8\), viscosity \(\nu>0\), and either a smooth solution on its
smooth lifespan or a suitable weak solution with its defect measure stated
explicitly

**Dependency:** R0.73W, especially the signed heat-plane energy identity,
the centered-increment split, and the positive gradient covariance

**Ordinary translation path:** LOCAL_DIRECT_NO_DGX

**DGX used:** false

**Kernel convention:** whenever an increment integral is written over
\(\mathbb R^3\), the periodic field is lifted to \(\mathbb R^3\) and
\(g_s\) is the Euclidean Gaussian.  This is equivalent to integration over
one period against the periodic heat kernel used in the localized note.

## 1. Frozen objects and conventions

Let

\[
 P_s=e^{s\Delta},\qquad v_s=P_su,\qquad
 \tau_s=P_s(u\otimes u)-v_s\otimes v_s,
\tag{1.1}
\]

\[
 e_s={1\over2}|v_s|^2,\qquad
 \Pi_s=-\tau_s:\nabla v_s,
\tag{1.2}
\]

and

\[
 F_s=(e_s+p_s)v_s+\tau_sv_s,\qquad
 {\cal D}_\nu=\partial_t-\nu\partial_s.
\tag{1.3}
\]

Positive \(\Pi_s\) is a sink of resolved energy.  R0.73W proved, at every
positive heat scale,

\[
 \boxed{{\cal D}_\nu e_s+\nabla\cdot F_s=-\Pi_s.}
\tag{1.4}
\]

Every localized formula in R0.73X must retain the pressure transport
\(p_sv_s\), the stress transport \(\tau_sv_s\), the cutoff derivatives, and
the positive-scale endpoint.  Replacing (1.4) by its spatial mean is not an
admissible localization argument.

## 2. Exact cutoff heat-characteristic ledger

Let \(\phi=\phi(t,x,s)\ge0\) be smooth and periodic in \(x\).  The product
rule applied to (1.4) gives the pointwise identity

\[
 \boxed{
 {\cal D}_\nu(\phi e_s)+\nabla\cdot(\phi F_s)
 =-\phi\Pi_s+e_s{\cal D}_\nu\phi+F_s\cdot\nabla\phi.}
\tag{2.1}
\]

Suppose

\[
 s(t)=s_- -\nu(t-t_-)>0,\qquad t\in[t_-,t_+],
\tag{2.2}
\]

and write

\[
 E_{\phi,s}(t)=\int_{\mathbb T^3}\phi(t,x,s)e_s(t,x)\,dx.
\tag{2.3}
\]

Spatial integration of (2.1) and the chain rule along (2.2) yield

\[
 \boxed{
 \begin{aligned}
 \int_{t_-}^{t_+}\!\!\int_{\mathbb T^3}
 \phi\,\Pi_{s(t)}\,dx\,dt
 ={}&E_{\phi,s_-}(t_-)-E_{\phi,s(t_+)}(t_+)\\
 &+\int_{t_-}^{t_+}\!\!\int_{\mathbb T^3}
 \left(e_s{\cal D}_\nu\phi+F_s\cdot\nabla\phi\right)\,dx\,dt .
 \end{aligned}}
\tag{2.4}
\]

Every unlabelled \(s\)-dependent integrand in (2.4) is evaluated at
\(s=s(t)\).
Thus localization replaces the vanished global divergence by two signed
commutators.  Neither term on the second line has a fixed sign.  If
\(\phi\) is independent of \(s\), then
\({\cal D}_\nu\phi=\partial_t\phi\), but the spatial-flux term remains.
If the characteristic reaches \(s=0\), (2.4) is not to be asserted for a
weak solution without a separate endpoint argument.

The first mandatory R0.73X result is a proof of (2.1)--(2.4) at the strongest
solution regularity for which every product and endpoint is justified.  The
smooth theorem, the positive-scale weak theorem, and any zero-scale
inequality must be stated separately.

## 3. Centered increment, cutoff commutator, and defect

Write

\[
 \kappa_{ijk,s}(x)=\int_{\mathbb R^3}
 \big(u_i(x-y)-v_{s,i}(x)\big)
 \big(u_j(x-y)-v_{s,j}(x)\big)
 \big(u_k(x-y)-v_{s,k}(x)\big)g_s(y)\,dy.
\]

Set

\[
 k_s={1\over2}\operatorname{tr}\tau_s,\qquad
 K_{j,s}={1\over2}\kappa_{iij,s},
\tag{3.1}
\]

\[
 Q_{j,s}=P_s(pu_j)-p_sv_{s,j},\qquad
 D_{ii,s}=P_s(|\nabla u|^2)-|\nabla v_s|^2\ge0.
\tag{3.2}
\]

The exact positive-scale carré-du-champ identity is

\[
 \boxed{
 D_{ii,s}=2\int_0^sP_{s-r}\!\left(|\nabla^2v_r|^2\right)\,dr,}
 \qquad
 |\nabla^2v_r|^2
 =\partial_\ell\partial_m v_{r,i}\,
  \partial_\ell\partial_m v_{r,i}.
\tag{3.2a}
\]

With

\[
 a_s(x,y)=u(x-y)-v_s(x),
\tag{3.3}
\]

the signed centered remainder is

\[
 {\mathscr S}_s={1\over4s}\int_{\mathbb R^3}
 y\cdot a_s(x,y)|a_s(x,y)|^2g_s(y)\,dy,
\tag{3.4}
\]

and R0.73W proved

\[
 \Pi_s=\partial_jK_{j,s}+{\mathscr S}_s.
\tag{3.5}
\]

Consequently, for every spatial cutoff \(\eta\),

\[
 \boxed{
 \int\eta\Pi_s\,dx
 =-\int\nabla\eta\cdot K_s\,dx+\int\eta{\mathscr S}_s\,dx.}
\tag{3.6}
\]

The sign in front of \(\nabla\eta\cdot K_s\) is part of the frozen contract.
The global cancellation of \(K_s\) does not survive localization.

For a suitable weak solution, let \(\mu\ge0\) denote the local
energy-defect measure, with the convention that the local total-energy
equation contains \(-\mu\).  The positive-scale trace ledger to be proved,
not assumed, is

\[
 \boxed{
 \partial_tk_s+\nabla\cdot G_s
 =-\nu D_{ii,s}+{\mathscr S}_s-P_s\mu,}
\qquad
 G_s=v_sk_s+Q_s-\nu\nabla k_s.
\tag{3.7}
\]

For smooth solutions \(\mu=0\).  At each fixed \(s>0\), multiplication by a
nonnegative \(\phi=\phi(t,x)\), spatial integration, and time integration
give the following identity.  For a suitable weak solution, the display is
licensed only after choosing a precise trace representative and admissible
endpoint times; without that extra trace statement, its rigorous meaning is
the distributional time-test formulation in
[`r073x_localized_heat_characteristic.md`](r073x_localized_heat_characteristic.md),
not an equality at arbitrary pointwise times:

\[
 \boxed{
 \begin{aligned}
 \int_{t_-}^{t_+}\!\!\int\phi{\mathscr S}_s\,dx\,dt
 ={}&
 \left[\int\phi k_s\,dx\right]_{t_-}^{t_+}
 +\nu\int_{t_-}^{t_+}\!\!\int\phi D_{ii,s}\,dx\,dt\\
 &+\int_{t_-}^{t_+}\!\!\int\phi\,d(P_s\mu)
 -\int_{t_-}^{t_+}\!\!\int
 \left(k_s\partial_t\phi+G_s\cdot\nabla\phi\right)\,dx\,dt .
 \end{aligned}}
\tag{3.8}
\]

The \(D_{ii,s}\) and \(P_s\mu\) rows are nonnegative payments in (3.8).
The \(Q_s\) pressure covariance and all cutoff errors remain signed.  A
finite smooth Fourier calculation necessarily has \(\mu=0\); it can check
the algebra and signs in (3.7)--(3.8), but cannot construct or certify a
nonzero PDE defect measure.

## 4. Frozen cylinder and scale normalization

This section uses the standard Navier--Stokes scaling cylinder \(Q_R\) with
time depth \(R^2\).  The descending heat-characteristic theorem instead uses
the viscosity-adapted cylinder
\(Q_R^\nu=(t_0-R^2/\nu,t_0)\times B_R(x_0)\), so that a characteristic with
\(s'=-\nu\) traverses a heat-scale interval of order \(R^2\).  The two
conventions coincide when \(\nu=1\); they must not be interchanged silently.

For \(z_0=(t_0,x_0)\), define

\[
 Q_R(z_0)=(t_0-R^2,t_0)\times B_R(x_0),\qquad
 {\cal T}_R(z_0)=Q_R(z_0)\times(0,R^2).
\tag{4.1}
\]

Choose cutoffs \(\chi_R(t)\eta_R(x)\) that equal one on \(Q_R\), are
supported in \(Q_{2R}\), and satisfy

\[
 |\partial_t\chi_R|\le C R^{-2},\qquad
 |\nabla\eta_R|\le C R^{-1},\qquad
 |\nabla^2\eta_R|\le C R^{-2}.
\tag{4.2}
\]

Under the Navier--Stokes scaling

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),\quad
 p_\lambda(t,x)=\lambda^2p(\lambda^2t,\lambda x),
\tag{4.3}
\]

the heat coordinate obeys
\[
 v_s[u_\lambda](t,x)
 =\lambda v_{\lambda^2s}[u](\lambda^2t,\lambda x).
\]
Equivalently, a physical heat scale is divided by \(\lambda^2\) under
zooming.  Hence \(k_s,e_s\) have degree two,
\(K_s,Q_s,F_s\) have degree three, and
\(\Pi_s,{\mathscr S}_s,D_{ii,s}\) have degree four.  The following
dimensionless quantities are therefore frozen for comparison:

\[
 {\cal C}^{\rm abs}_{\Pi,0}(z_0,R)
 ={1\over R^3}\int_{{\cal T}_R(z_0)}|\Pi_s|\,ds\,dx\,dt,
\tag{4.4}
\]

\[
 {\cal C}^{\rm sgn}_{\Pi,0}(z_0,R)
 ={1\over R^3}\left|
 \int_{{\cal T}_R(z_0)}\Pi_s\,ds\,dx\,dt\right|,
\tag{4.5}
\]

\[
 {\cal C}^{\rm abs}_{\Pi,1/2}(z_0,R)
 ={1\over R^2}\int_{{\cal T}_R(z_0)}
 s^{-1/2}|\Pi_s|\,ds\,dx\,dt.
\tag{4.6}
\]

The same definitions apply to \({\mathscr S}_s\) and
\(\nabla\eta_R\cdot K_s\).  The signed quantities in (4.5) are weaker than
their absolute counterparts; cancellation in (4.5) cannot be advertised as
Carleson control of (4.4).

The local energy, pressure, and defect controls used to test candidate
right-hand sides are

\[
 \begin{aligned}
 {\cal E}(z_0,R)
 ={}&{1\over R}\operatorname*{ess\,sup}_{t_0-R^2<t<t_0}
 \int_{B_R}|u|^2\,dx
 +{\nu\over R}\int_{Q_R}|\nabla u|^2\,dx\,dt,\\
 {\cal P}(z_0,R)
 ={}&{1\over R^2}\int_{Q_R}
 |p-(p)_{B_R}(t)|^{3/2}\,dx\,dt,\\
 {\cal M}(z_0,R)
 ={}&{1\over R}\mu(Q_R).
 \end{aligned}
\tag{4.7}
\]

These normalizations do not assert an estimate.  They prevent a
dimensionally false candidate from entering the finite search.

## 5. Decidable questions

R0.73X is restricted to the following questions.

1. **Exact localized identity.**  Do (2.1)--(2.4), (3.6), and the
   appropriately qualified version of (3.7)--(3.8) hold with the displayed
   signs and coefficients?
2. **Cutoff ledger.**  For a sparse exact witness, are
   \(\int\eta\Pi_s\), \(-\int\nabla\eta\cdot K_s\), and
   \(\int\eta{\mathscr S}_s\) separately nonzero, and do they add exactly as
   in (3.6)?
3. **Quadratic absorption rejection target.**  Can either of the universal
   same-time inequalities
   \[
   \left|\int\eta_R\Pi_{\theta R^2}\,dx\right|
   \le C\left[
   \nu\int\eta_RD_{ii,\theta R^2}\,dx
   +R^{-2}\int\eta_Rk_{\theta R^2}\,dx\right],
   \tag{5.1}
   \]
   \[
   \left|\int\eta_R{\mathscr S}_{\theta R^2}\,dx\right|
   \le C\left[
   \nu\int\eta_RD_{ii,\theta R^2}\,dx
   +R^{-2}\int\eta_Rk_{\theta R^2}\,dx\right]
   \tag{5.2}
   \]
   hold for all smooth divergence-free data with an amplitude-independent
   \(C\), with the cutoff fixed independently of the amplitude?  A single
   nonzero cubic numerator and amplitude scaling can decide these
   deliberately strong statements.
4. **Local-core candidate; exterior ledger still required.**  Does a
   scaling-compatible estimate of the schematic form
   \[
   {\cal C}^{\rm abs}_{{\mathscr S},0}(z_0,R)
   \le C\left[
   {\cal E}(z_0,2R)^{3/2}
   +{\cal P}(z_0,2R)+{\cal M}(z_0,2R)
   +{\cal A}_{\rm ext}(z_0,R)\right]
   \tag{5.3}
   \]
   hold under a precisely stated solution class?  Here
   \({\cal A}_{\rm ext}\) must be a separately frozen, dimensionless Gaussian
   annular velocity/pressure-tail functional, unless a global hypothesis is
   proved to control it.  Until that term is defined, (5.3) is schematic and
   is not a ledger-complete theorem statement.  Amplitude parity alone cannot
   decide (5.3), because the energy term has the matching cubic degree.
5. **Carleson/tent candidate.**  Is either absolute tent quantity (4.4) or
   (4.6) controlled in a way that becomes small from a non-circular local
   hypothesis?  The spatially and scale-signed quantity (4.5) is to be
   recorded separately.
6. **Defect compatibility.**  Can the positive defect payment be passed to
   the required weak limit without losing the pressure and cutoff rows?
   Smooth finite data cannot answer this question; they only test the
   zero-defect algebra.

Questions (5.1)--(5.2) are finite falsification targets.  Questions
(5.3)--(5.6) require analysis beyond a bounded certificate unless an exact
family produces an unbounded ratio for the fully declared right-hand side.

## 6. Finite evidence gate

The companion finite design must contain two independent tracks.

- A smallest-available sparse resonant Fourier track probes every term in
  (3.6) and the smooth \(\mu=0\) version of (3.7).
- A finite Fourier concentration track uses a nonnegative Fejér cutoff and a
  Leray-projected carrier to test the \(R\), \(s\), frequency, and amplitude
  powers in (4.4)--(5.3).

Every exact output must distinguish:

1. an identity check;
2. a counterexample to one explicitly quantified universal inequality;
3. a bounded search result;
4. a scaling diagnostic;
5. a statement requiring a genuine Navier--Stokes trajectory or weak limit.

A bounded ratio on the test family is not evidence that an inequality holds.
An unbounded ratio refutes an inequality only if the computed family lies in
its declared quantifiers and every denominator term has been included.

## 7. Explicit non-claims

R0.73X does not claim any of the following at problem-freeze stage:

- a local energy equality at \(s=0\) for arbitrary weak solutions;
- construction of a nonzero suitable-weak-solution defect measure;
- a Carleson estimate, epsilon-regularity criterion, or continuation
  criterion;
- absorption of the signed remainder after omitting pressure, endpoint, or
  cutoff terms;
- that a trigonometric polynomial or a static concentrated profile is a
  singularity, blow-up candidate, DNS, or generic turbulent flow;
- that a finite enumeration proves global minimal Fourier support outside
  its explicit search box;
- arbitrary-data three-dimensional global regularity or a Clay conclusion.

NOT CLAY.

## 8. Exit condition

The section may advance beyond the freeze only after:

1. the two localized ledgers are independently rederived with matching
   signs;
2. a source-level regularity statement is attached to every use of
   \(\mu\), \(P_s\mu\), and the \(s=0\) endpoint;
3. the sparse and concentrated finite tracks agree on all shared exact
   rows;
4. every failed candidate is named with its exact quantifiers;
5. every surviving Carleson or epsilon-regularity candidate is marked
   OPEN rather than inferred from finite data.

## 9. Frozen claim-state ledger

This is the entry-state ledger frozen before the companion derivation and
finite audit.  It records the questions that had to be discharged, not the
current cross-file result status.

\[
\begin{array}{ll}
\texttt{localizedHeatCharacteristicLedger}
  &=\texttt{TARGET\_EXACT\_REDERIVATION},\\
\texttt{centeredIncrementCutoffSplit}
  &=\texttt{TARGET\_EXACT\_TWO\_PATH},\\
\texttt{suitableWeakDefectLedger}
  &=\texttt{TARGET\_CONDITIONAL\_WITH\_MEASURE},\\
\texttt{compactCutoffQuadraticAbsorption}
  &=\texttt{FINITE\_FALSIFICATION\_TARGET},\\
\texttt{absoluteCarlesonControl}
  &=\texttt{OPEN},\\
\texttt{epsilonRegularityCriterion}
  &=\texttt{OPEN},\\
\texttt{finiteComputationCertifiesPDE}
  &=\texttt{FALSE},\\
\texttt{arbitraryThreeDimensionalGlobalRegularity}
  &=\texttt{OPEN},\\
\texttt{clayConclusion}
  &=\texttt{OPEN}.
\end{array}
\]
