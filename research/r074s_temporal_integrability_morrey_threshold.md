# R0.74S Step 13 — temporal-integrability ceiling and the combined Morrey threshold

## 0. Result and scope

Step 12 replaced the short last-exit residual by an absolute physical-flux
variation in one common terminal window.  It also proved an excess estimate
under uniform moving-tube Morrey and path-length bounds.  This note asks how
far ordinary time integrability and a nonuniform Morrey coefficient can move
those two gates.

There are five conclusions.

1. For every fixed periodic suitable weak solution and fixed scale, the
   shellwise physical-flux densities have a summable
   \(\ell^1(L_t^{4/3})\) envelope.  This follows from the energy-class
   interpolation \(u\in L_t^4L_x^3\), the periodic Calderón--Zygmund pressure
   estimate, and the fixed-scale mollified drift bound.
2. A common terminal window of dimensionless length \(\delta\) therefore
   gains \(\delta^{1/4}\).  More generally an \(L_t^p\) shell-tail estimate
   gains \(\delta^{1-1/p}\), with one deletion set for the whole window.
3. That time gain does not repair the payment exponent.  Even granting the
   stronger, presently unproved estimate that the relevant
   \(\ell^1(L_t^p)\) tail is linear in \(P_R^M\), optimization against the
   inherited positive-depth term gives
   \(P^{2(2p-1)/(5p-3)}\).  The energy-class value is \(P^{10/11}\), and even
   \(p=\infty\) reaches only \(P^{4/5}\), never \(P^{2/3}\).
4. A smooth \((N+1)\)-coordinate witness proves that scalar temporal
   regularity of any order, with amplitude linear in the payment, cannot by
   itself imply the fixed-window best-\(N\) gate.  This is an abstract
   vector-valued witness, not a Navier--Stokes solution.
5. The Step 12 moving-tube hypothesis can be weakened.  Uniform bounds on
   its Morrey and path factors separately are unnecessary; it is enough that
   their combined cover coefficient grow no faster than
   \(1+(P_R^M)^{2/3}\).  The exponent \(2/3\) is sharp for this two-scalar-cap
   argument.  It is not asserted to be necessary for a different PDE proof.

The universal terminal-window gate (S.280), the universal ancestor gate
(S.288), and the combined target (S.303) remain **OPEN**.  No claim below
proves Q.12, Q.1, scale contraction, regularity, singularity formation, or
the Millennium problem.  No DNS or DGX computation is used.  **NOT CLAY.**

## 1. Dimensionless flux densities

Retain the full R0.74S Step 12 setting.  Write

\[
 \vartheta={\tau-s_R\over R^2}\in(0,4),\qquad
 t(\sigma)=s_R+R^2\sigma,
\]

and extend every derivative by zero outside \(\mathcal T_R\).  Define

\[
 \boxed{
 h_{k,R}(\sigma):=R^2|\dot F_{k,R}(t(\sigma))|,
 \qquad 0<\sigma<4.}
\tag{S.307}
\]

Then the common-window coordinate from (S.273) is exactly

\[
 \boxed{
 f_{k,R}(\tau,\delta)
 =\int_{(\vartheta-\delta,\vartheta)\cap(0,4)}
       h_{k,R}(\sigma)\,d\sigma.}
\tag{S.308}
\]

For \(1\le p\le\infty\) and an integer \(N\ge0\), introduce the
common-deletion temporal tail

\[
 \boxed{
 \mathfrak H^F_{p,N,R}
 :=\inf_{\#S\le N}\sum_{k\notin S}
       \|h_{k,R}\|_{L^p(0,4)}.}
\tag{S.309}
\]

The order in (S.309) matters: one shell set is removed before the time norm is used.
A pointwise-in-time minimizing shell set would be allowed to move
with time and would not control the common-window functional.

## 2. The fixed-solution \(L_t^{4/3}\) fact

### Proposition 2.1 — energy-class temporal envelope

For every fixed periodic suitable weak solution in the frozen class and
every fixed \(R>0\), put

\[
 E_I:=\mathop{\rm ess\,sup}_{t\in\mathcal T_R}\|v_R(t)\|_2^2,
 \qquad
 D_I:=\int_{\mathcal T_R}\|\nabla v_R(t)\|_2^2\,dt,
 \qquad
 e_R:={E_I\over R},\quad d_R:={D_I\over R}.
\]

Then

\[
 \boxed{
 \mathfrak H^F_{4/3,0,R}
 \le C\left([e_R(e_R+d_R)]^{3/4}+e_R^{3/2}\right)
 \le C(e_R+d_R)^{3/2}<\infty.}
\tag{S.310}
\]

Consequently, for every terminal and \(0<\delta<4\),

\[
\boxed{
 \mathcal V^F_{N,R}(\tau,\delta)
 \le C\delta^{1/4}[e_R(e_R+d_R)]^{3/4}
      +C\delta e_R^{3/2}.}
\tag{S.311}
\]

The finite coefficient in (S.310) may depend on the solution and on \(R\).
No uniform estimate for it in terms of \(P_R^M\) is claimed.

**Proof.**  Use the mean-zero periodic pressure gauge.  Shellwise gauge
cancellation permits this gauge in the signed derivative defining
\(F_{k,R}\).  The energy class and spatial interpolation give

\[
 \boxed{
 v_R\in L_t^4L_x^3,\qquad
 \pi_R-\overline\pi_R(t)\in L_t^2L_x^{3/2},\qquad
 a_R\in L_t^\infty.}
\tag{S.312}
\]

Indeed,
\(L_t^\infty L_x^2\cap L_t^2H_x^1\subset L_t^4L_x^3\).
Periodic Calderón--Zygmund gives

\[
 \|\pi_R-\overline\pi_R(t)\|_{L^{3/2}}
 \le C\|v_R(t)\|_{L^3}^2,
\]

and fixed-scale convolution maps \(L_x^2\) to \(L_x^\infty\), so
\(|a_R(t)|\le C_R\|v_R(t)\|_2\).

The inherited cutoff bound and the super-Gaussian shell weights imply

\[
 \sum_{k\ge1}\gamma_k(1+2^{3k}R^3)<\infty.
\]

Taking the absolute value only after the pressure gauge has been changed,
(2.9) of R0.74P therefore gives, with \(t=t(\sigma)\),

\[
 \boxed{
 h_{k,R}(\sigma)
 \le C\gamma_k(1+2^{3k}R^3)
 \left[
  \|v_R(t)\|_3^3
  +\|\pi_R(t)-\overline\pi_R(t)\|_{3/2}\|v_R(t)\|_3
  +|a_R(t)|\|v_R(t)\|_2^2
 \right].}
\tag{S.313}
\]

For completeness, the scale factors can be retained.  The cutoff sum gives

\[
 \sum_k\gamma_k|\nabla\Psi_k^R|
 \le CR^{-1},
\]

where the restriction \(R<\pi/16<1\) absorbs the harmless
\(R^2\sum_k2^{3k}\gamma_k\) term.  The periodic interpolation inequality

\[
 \|v_R(t)\|_3^4
 \le C\|v_R(t)\|_2^2
 \left(\|\nabla v_R(t)\|_2^2
       +R^{-2}\|v_R(t)\|_2^2\right)
\]

and \(|\mathcal T_R|=4R^2\) imply

\[
 \left\|\sum_k|\dot F_{k,R}^{\rm cub}|
       +\sum_k|\dot F_{k,R}^{\rm pr}|\right\|_{L_t^{4/3}}
 \le CR^{-1/2}[e_R(e_R+d_R)]^{3/4}.
\]

Moreover,
\(\|\varphi_R^{\rm per}\|_2\le CR^{-3/2}\) gives

\[
 \left\|\sum_k|\dot F_{k,R}^{\rm dr}|\right\|_{L_t^\infty}
 \le CR^{-2}e_R^{3/2}.
\]

The individual estimate (S.313), followed by summation of its
super-Gaussian coefficients, proves the corresponding
\(\ell^1(L_t^{4/3})\) statement rather than only an
\(L_t^{4/3}(\ell^1)\) statement.  Under the change of variables (S.307),
an \(L_t^{4/3}\) norm gains \(R^{1/2}\), while an \(L_t^\infty\) norm
gains \(R^2\).  This proves (S.310).

For a fixed deletion set \(S\), Hölder on the interval in (S.308) gives

\[
 \sum_{k\notin S}f_{k,R}(\tau,\delta)
 \le\delta^{1/4}\sum_{k\notin S}
       \|h_{k,R}\|_{4/3}.
\]

Take the infimum over \(S\).  Keeping the cubic/pressure and drift time
exponents separate gives (S.311); replacing \(\delta\) by
\(C\delta^{1/4}\) on \(0<\delta\le1\) gives the coarser bound with the
coefficient displayed in (S.310). \(\square\)

The norm order is explicit.  Writing the bracket in (S.313), evaluated at
\(t=t(\sigma)\), as \(\mathcal B_R(\sigma)\), the pointwise shell
envelope used above gives

\[
 \sum_k\|h_{k,R}\|_{4/3}
 \le C\!\left[\sum_k\gamma_k(1+2^{3k}R^3)\right]
       \|\mathcal B_R\|_{4/3}.
\]

No interchange of \(\ell^1(L^{4/3})\) with
\(L^{4/3}(\ell^1)\) is being used.

This improves the qualitative fixed-solution modulus (S.277) to an
algebraic \(\delta^{1/4}\) modulus.  It does not improve its uniformity.
The exponent \(4/3\) is the endpoint of the direct energy-class interpolation
for a spatial cubic integral.  The statement does not exclude
higher time integrability derived from additional PDE hypotheses.

The endpoint assertion has an exact interpolation check.  Energy-admissible
pairs satisfy

\[
 {2\over q}+{3\over r}={3\over2},
 \qquad 2<r\le6,
 \qquad q(r)={4r\over3(r-2)}.
\]

The endpoint \(r=2\) is understood separately as \(q(2)=\infty\).

At the symmetric cubic point \((q,r)=(4,3)\), taking three factors gives
time exponent \(q/3=4/3\).  More generally, if three energy-admissible
pairs close spatial Hölder exactly,
\(\sum_i1/r_i=1\), then

\[
 \sum_{i=1}^3{1\over q_i}
 ={9\over4}-{3\over2}\sum_{i=1}^3{1\over r_i}
 ={3\over4}.
\]

Hence the same \(4/3\) time exponent results.  If the spatial reciprocal
sum is smaller than one, the direct time exponent is worse.  For pressure,
the symmetric choice first places \(v_R\otimes v_R\) in \(L_x^{3/2}\),
inside the strong Calderón--Zygmund range.  The \(L^1\) endpoint is only
weak type and the \(L^\infty\) endpoint is BMO; neither is supplied by this
argument.

## 3. General temporal exponent and exact optimization

Set

\[
 a_p:=1-{1\over p}\quad(1\le p<\infty),
 \qquad a_\infty:=1.
\tag{S.314}
\]

For any nonnegative shell densities in \(\ell^1(L^p(0,4))\), the same proof
as (S.311) gives

\[
 \boxed{
 \mathcal V^F_{N,R}(\tau,\delta)
 \le\delta^{a_p}\mathfrak H^F_{p,N,R}.}
\tag{S.315}
\]

Suppose, only for this method test, that some fixed
\(p\in(1,\infty]\), \(N\),
\(\beta>0\), and \(C_H\) obey

\[
 \mathfrak H^F_{p,N,R}\le C_H(P_R^M)^\beta
\tag{S.316}
\]

uniformly in the solution, scale, and terminal setting.  Combining (S.315)
with (S.275) yields

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le C_H\delta^{a_p}P^\beta
     +C_{\rm deep}\delta^{-2/3}P^{2/3},
 \qquad P:=P_R^M.}
\tag{S.317}
\]

Assume \(P\ge1\) and \(\beta>2/3\).  Up to a constant depending only on
\(p,C_H,C_{\rm deep}\), the balancing scale is

\[
 \boxed{
 \delta_{p,\beta}
 \asymp P^{-(\beta-2/3)/(a_p+2/3)}.}
\tag{S.318}
\]

Once this scale lies in \((0,4)\), both terms in (S.317) have the power

\[
 \boxed{
 E_{p,\beta}
 ={2\over3}{a_p+\beta\over a_p+2/3},
 \qquad
 E_{p,\beta}-{2\over3}
 ={2\over3}{\beta-2/3\over a_p+2/3}>0.}
\tag{S.319}
\]

Thus no \(p\), including \(p=\infty\), removes the exponent loss when the
temporal coefficient grows faster than \(P^{2/3}\).  Conversely, within
this particular two-term argument, \(\beta\le2/3\) is sufficient in the
large-payment regime by taking any fixed admissible window.  The small-
payment regime is already controlled by the inherited linear ledger because
\(P\le P^{2/3}\) for \(0\le P\le1\).

The optimistic linear case \(\beta=1\) has

\[
 \boxed{
 \delta_p\asymp P^{-p/(5p-3)},
 \qquad
 E_p={2(2p-1)\over5p-3}.}
\tag{S.320}
\]

In particular,

\[
 \boxed{
 p={4\over3}:\quad \delta\asymp P^{-4/11},
 \quad E_p={10\over11};
 \qquad
 p=\infty:\quad \delta\asymp P^{-1/5},
 \quad E_p={4\over5}.}
\tag{S.321}
\]

For \(p=1\), there is no positive window power and the linear term remains
\(P\).  Formula (S.320) approaches \(4/5\) monotonically as
\(p\to\infty\).  Hence even a hypothetical \(L_t^\infty\) flux-density
bound with linear payment scale cannot make this direct window/depth balance
reach \(2/3\).

For the actually proved coefficient in Proposition 2.1, direct optimization
gives the fixed-solution estimate

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le C\left[
 A_R+(\mathfrak H^F_{4/3,N,R})^{8/11}A_R^{3/11}
 \right].}
\tag{S.322}
\]

The \(A_R\) term covers the case in which the formal optimizer exceeds the
allowed window length.  If one additionally had
\(\mathfrak H^F_{4/3,N,R}\lesssim P\), the mixed term in (S.322) would be
\(P^{10/11}\), exactly as in (S.321).  No such uniform estimate is proved
here.

## 4. Smooth all-\(p\) saturation witness

Fix \(N\ge0\), set \(M=N+1\), choose
\(0<\delta_0<4\), and take a nonnegative
\(\phi\in C_c^\infty((-\delta_0,0))\) with \(\int\phi=1\).  Choose a
terminal \(\vartheta_0\) for which the translated support lies in \((0,4)\).
For \(H>0\), define

\[
 \boxed{
 h_{k,H}(\sigma)={H\over M}\phi(\sigma-\vartheta_0)
 \quad(1\le k\le M),
 \qquad h_{k,H}=0\quad(k>M).}
\tag{S.323}
\]

Every primitive is smooth and increasing.  For every
\(1\le p\le\infty\),

\[
 \boxed{
 \sum_k\|h_{k,H}\|_{L^p}=H\|\phi\|_{L^p},
 \qquad
 \mathcal V^F_{N}(\vartheta_0,\delta_0)={H\over M}.}
\tag{S.324}
\]

If the abstract payment is normalized so that \(P_H\asymp H\), then

\[
 \boxed{
 {\mathcal V^F_N(\vartheta_0,\delta_0)\over P_H^{2/3}}
 \asymp {H^{1/3}\over N+1}\longrightarrow\infty.}
\tag{S.325}
\]

The witness has a fixed smooth time profile; it is not a concentration
artifact and it belongs to every temporal \(L^p\) space.  It proves only a
logical boundary: temporal regularity plus a scalar linear-amplitude bound
does not contain the fixed-window, fixed-\(N\) estimate (S.280).  It is not a
velocity field, pressure, suitable weak solution, or Navier--Stokes
counterexample.

There is also a smooth abstract witness that saturates the adaptive
\(p=4/3\) balance.  Take \(P\ge1\), choose
\(0\le\rho\in C_c^\infty((-1,0))\) with
\(\|\rho\|_{4/3}=1\), and put

\[
 c_\rho:=\int_{-1}^0\rho(s)\,ds>0,
 \qquad d:=P^{-4/11}\le1.
\]

Choose \(\vartheta_0\) so that
\(\vartheta_0+d\,\operatorname{supp}\rho\subset(0,4)\), and replace
(S.323) by

\[
 h_{k,P}(\sigma)
 ={P\over Md^{3/4}}
 \rho\!\left({\sigma-\vartheta_0\over d}\right),
 \qquad 1\le k\le M.
\]

Then

\[
 \sum_k\|h_{k,P}\|_{4/3}=P,
 \qquad
 \sum_k\|h_{k,P}\|_1=c_\rho P^{10/11}\le c_\rho P,
\]

and deletion of \(N=M-1\) coordinates leaves exactly
\(c_\rho P^{10/11}/M\).  Assign each coordinate the abstract depth
\(d_{k,P}=d\) and residual

\[
 r_{k,P}:={c_\rho P^{10/11}\over M}.
\]

If \(\delta\ge d\), the common terminal window contains the entire
support and hence pays this residual exactly.  If \(0<\delta<d\), the
coordinate is in the deep class and

\[
 \sum_kr_{k,P}=c_\rho P^{10/11}
 \le c_\rho P^{2/3}\delta^{-2/3},
\]

because the right-hand side is smallest as \(\delta\uparrow d\).  At the
balancing depth,

\[
 P^{2/3}d^{-2/3}=P^{10/11},
 \qquad
 {10\over11}-{2\over3}={8\over33}.
\]

Thus, up to the fixed constant \(c_\rho\), the \(10/11\) power is sharp
for the abstract combination of a linear
\(\ell^1(L^{4/3})\) rate bound, the inherited linear \(L^1\) ledger, the
depth allowance, and a fixed deletion budget.  This remains a method-level
countermodel, not an NSE realization.

## 5. The exact scalar threshold in the moving-tube route

Allow the Step 12 quantities to depend on the solution, scale, and terminal:

\[
 \begin{aligned}
 M_R(\tau)&:=\sup_{Q_R^-\ {\rm in\ the\ buffer}}
       {\widetilde{\boldsymbol\mu}(Q_R^-)\over R},\\
 L_R(\tau)&:={1\over R}\int_{s_R}^{\tau}
       |\dot{\widetilde X}_R(t)|\,dt.
 \end{aligned}
\]

Define their one combined cover coefficient

\[
 \boxed{
 B_R(\tau):=C_\psi M_R(\tau)
       \bigl(\mathscr A_3+L_R(\tau)\mathscr A_2\bigr).}
\tag{S.326}
\]

Whenever these quantities are finite, the proof of Step 12 (S.291)--(S.293)
is pointwise in \((u,R,\tau)\) and gives

\[
 \boxed{
 \sum_kx_k^{\rm sel}(\tau)
 \le\min\{C_0P_R^M,B_R(\tau)\}.}
\tag{S.327}
\]

The separate uniform hypotheses \(M_R\le M\), \(L_R\le L\) used in Step 12
are therefore stronger than necessary for this algebraic closure.

### Proposition 5.1 — payment-dependent Morrey envelope

Suppose one universal \(C_B\) satisfies

\[
 \boxed{
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}B_R(\tau)
 \le C_B\bigl[1+(P_R^M)^{2/3}\bigr]}
\tag{S.328}
\]

for every solution and scale.  Then

\[
 \boxed{
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}
 \mathcal S_0(x^{\rm sel}(\tau))
 \le C(C_0,C_B)(P_R^M)^{2/3}.}
\tag{S.329}
\]

**Proof.**  If \(P_R^M\le1\), use the linear side of (S.327) and
\(P_R^M\le(P_R^M)^{2/3}\).  If \(P_R^M\ge1\), use the second side,
(S.328), and \(1\le(P_R^M)^{2/3}\). \(\square\)

In particular, a power envelope

\[
 \boxed{
 B_R(\tau)\le C_B[1+(P_R^M)^\theta],
 \qquad 0\le\theta\le{2\over3},}
\tag{S.330}
\]

closes the selected-excess gate.  This permits \(M_R\) and \(L_R\) to be
nonuniform individually, provided their combined weighted cover cost has
the required payment growth.

The exponent threshold is sharp for an argument that knows only the two
scalar caps in (S.327).  If \(\theta>2/3\), fix \(N\), put \(M=N+1\), and
for large \(P\) take \(M\) equal coordinates with total mass
\(T_P=\min\{C_0P,C_BP^\theta\}\), and set
\(x_k^{\rm sel}=b_k=T_P/M\).  Then

\[
 \boxed{
 \sum_kb_k=T_P,
 \qquad
 \mathcal S_N(b)={T_P\over N+1},
 \qquad
 {\mathcal S_N(b)\over P^{2/3}}\longrightarrow\infty.}
\tag{S.331}
\]

This is an abstract sequence countermodel to the two-cap inference.  It is
not asserted to arise from a dissipation measure or an NSE solution.  A PDE
argument using more than the two scalar caps could still succeed above this
threshold.

## 6. Dynamic high frequency does not by itself attack the flux gate

There is a useful exact-solution screen.  On the \(2\pi\)-periodic torus,
take \(A>0\), \(T>0\), and an integer \(n\ge1\):

\[
 \boxed{
 u^{(n)}(t,x)=Ae^{-n^2t}\sin(nx_2)e_1,
 \qquad p^{(n)}=0.}
\tag{S.332}
\]

This is an unforced smooth Navier--Stokes solution: it is divergence free,
\((u^{(n)}\!\cdot\nabla)u^{(n)}=0\), and it solves the heat equation.  The
mollified path velocity is parallel to \(e_1\), while the moving velocity is
independent of \(y_1\).  Therefore, for every periodic shell cutoff,

\[
 \boxed{
 \dot F_{k,R}^{(n)}(t)
 ={\gamma_k\eta_R(t)\over2R}
 \int_{\mathbb T^3}|v_R^{(n)}|^2
       (v_{R,1}^{(n)}-a_{R,1})\,\partial_{y_1}\Psi_k^R\,dy
 =0.}
\tag{S.333}
\]

The last equality is periodic integration in \(y_1\).  Hence every
\(f_{k,R}\) and every \(\mathcal V^F_{N,R}\) vanishes for this exact family.

At the same time, on \([0,T]\),

\[
 \boxed{
 \begin{aligned}
 \int_0^T\!\int_{\mathbb T^3}|\nabla u^{(n)}|^2
 &=2\pi^3A^2(1-e^{-2n^2T}),\\
 \int_0^T\!\int_{\mathbb T^3}|u^{(n)}|^3
 &={32\pi^2A^3\over9n^2}(1-e^{-3n^2T}).
 \end{aligned}}
\tag{S.334}
\]

Thus its dissipation-to-cubic ratio grows like \(n^2/A\), but its canonical
physical-flux primitive is zero and its completed clock satisfies \(K=Q\).
The example confirms that high Fourier frequency and high Rayleigh ratio do
not automatically create a short physical-shell flux tail.  The index \(k\)
labels physical moving annuli, not Fourier shells.  A relevant exact-family
test would need a PDE-compatible mechanism converting sub-\(R\) frequency
into many spatially separated annular residuals while keeping every existing
payment channel small.  No such mechanism is proved here.

## 7. Bounded primary-source audit

A bounded search was made for results that could supply a uniform temporal
tail or the payment-dependent Morrey envelope (S.328).  No theorem with
those quantifiers was found.

| Primary result | Established scope | Boundary for Step 13 |
|---|---|---|
| Z. Lei, X. Ren, [*Quantitative partial regularity of the Navier--Stokes equations and applications*](https://doi.org/10.1016/j.aim.2024.109654), *Adv. Math.* **445** (2024), 109654 | Gives a quantitative replacement for dissipation-energy absolute continuity through pigeonholing and proves logarithmically improved partial regularity. | The pigeonholed annular levels and constants depend on natural local energies; the result is not a common-terminal, fixed-physical-shell best-\(N\) flux estimate. |
| H. J. Choe, M. Yang, [*Local kinetic energy and singularities of the incompressible Navier--Stokes equations*](https://doi.org/10.1016/j.jde.2017.09.036), *JDE* **264** (2018), 1171--1191 | Proves a reverse Holder inequality for the velocity gradient under a uniformly bounded scaled local-kinetic-energy functional. | The extra uniform scaled-energy hypothesis is precisely additional information absent from the bare payment ledger. |
| C. Guevara, N. C. Phuc, [*Local energy bounds and epsilon-regularity criteria for the 3D Navier--Stokes system*](https://doi.org/10.1007/s00526-017-1151-7), *Calc. Var. PDE* **56** (2017), 68 | Develops pressure-sensitive local-energy estimates and improved epsilon-regularity criteria. | It converts small scale-integrated inputs into regularity; it does not produce the shell-tail coefficient in (S.316) or the ancestor envelope (S.328). |
| H. Koch, D. Tataru, [*Well-posedness for the Navier--Stokes equations*](https://doi.org/10.1006/aima.2000.1937), *Adv. Math.* **157** (2001), 22--35 | Establishes well-posedness in the critical \(BMO^{-1}\) framework using a Carleson-type spacetime norm. | This is a critical small-data solution class, not a Carleson estimate derived for every bare suitable weak solution from \(P_R^M\). |

This search is a collision check, not a priority claim.  The papers support
the stated boundary: quantitative time or Morrey gains in the literature
come with extra scale information, smallness, or energy-dependent constants.

## 8. A critical eight-ary tree countermodel

The preceding Morrey threshold is scalar.  A separate question is whether a
bounded-branching ancestor tree, together with the existing linear and
square ledgers, forces additional packing.  The answer is no at the critical
tree exponent.

Fix an integer \(m\ge1\), put \(L=m^3\), and take the complete eight-ary
tree with depths \(0\le d\le L-1\).  For every node \(v\) at depth \(d\),
define

\[
 \boxed{
 b_v={1\over m^2 8^d},\qquad
 s_v={5\over3m^2 8^d},\qquad
 c_v=2^{-d},\qquad
 p_v={1\over m^3 8^d}.}
\tag{S.335}
\]

Scale the pure high-Rayleigh scalar row of Step 11 (S.267) by \(s_v\):

\[
 \boxed{
 T_v=s_v,\quad d_v^{\rm def}=0,\quad
 \int_{H_v}g_v=b_v={3\over5}s_v,
 \quad\beta_v=0,\quad
 \sigma_v={983\over12000}s_v<{T_v\over12},\quad
 x_v={2617\over6000}s_v>{T_v\over6},\quad
 r_v^x={s_v\over3}.}
\tag{S.336}
\]

Thus every node lies strictly in the abstract \(\mathcal I_x\) branch and
its ancestor is purely high-Rayleigh.  Direct level summation gives

\[
 \boxed{
 b_v=c_vp_v^{2/3},\qquad
 \sum_vp_v=1,\qquad
 \sum_vb_v=m,\qquad
 \sum_vs_v={5m\over3}=:P_m.}
\tag{S.337}
\]

The scaled scalar rows are therefore compatible, up to absolute constants,
with the inherited linear clock and variation ledgers and with zero
\(Q\)-variation.  They even satisfy

\[
 \boxed{
 \sum_vs_v^2
 <{200\over63m^4},\qquad
 \sum_{w\succeq v}b_w^2\le{8\over7}b_v^2,
 \qquad
 \sum_{w\in{\rm child}(v)}c_w^3=c_v^3
 \quad(0\le d(v)\le L-2).}
\tag{S.338}
\]

Here \(w\succeq v\) denotes a descendant of \(v\), including \(v\).  The
second relation is a strong square-Carleson bound.  The last relation is
exactly critical: eight children, each with half the parent coefficient,
conserve the total coefficient cube.

Every coordinate is at most \(m^{-2}\).  Deleting any fixed \(N\)
coordinates consequently leaves

\[
 \boxed{
 \mathcal S_N(b)\ge m-{N\over m^2},\qquad
 A_m=P_m^{2/3}=\left({5m\over3}\right)^{2/3},
 \qquad
 {\mathcal S_N(b)\over A_m}\longrightarrow\infty.}
\tag{S.339}
\]

This proves that a linear total ledger, a vanishing global square ledger,
bounded branching, a square-Carleson subtree estimate, and critical child
decay still do not imply (S.288).  Stopping one ancestor cannot be counted
as one shell exception while all of its descendants are silently deleted:
the best-\(N\) functional removes individual shell coordinates.  A separate
PDE theorem would have to pay the descendants.

The tree is a strict abstract ledger model.  Its nodes have not been
realized simultaneously as physical moving annuli of one solution.  In
particular, it does not solve the coupled Navier--Stokes dynamics, pressure,
diffusion, cross-cubic payment, periodic incidence, or the identity
\(K=Q+F\) for one common velocity field.  It is not an NSE counterexample.

There is an exact sufficient replacement.  Suppose that for every terminal
there are a shell set \(E_\tau\), \(\#E_\tau\le N_b\), nonnegative
\(q_k\), tree payments \(p_\nu\), coefficients \(c_\nu\), and incidences
\(\nu\rightsquigarrow k\), such that, outside \(E_\tau\),

\[
 b_k\le q_k+\sum_{\nu\rightsquigarrow k}c_\nu p_\nu^{2/3},
 \qquad
 \sum_kq_k\le C_qA_R,
\]

and

\[
 \sum_{\rm incidences}p_\nu\le B_{\rm inc}C_pP_R^M,
 \qquad
 \sum_{\substack{\rm incidences\\k\notin E_\tau}}c_\nu^3\le C_c.
\]

Then Hölder over the incidence set gives

\[
 \boxed{
 \mathcal S_{N_b}(b)
 \le\left[C_q+C_c^{1/3}(B_{\rm inc}C_p)^{2/3}\right]A_R.}
\tag{S.340}
\]

The cube is the exact dual exponent, not a convenient choice.  For every
finite nonnegative coefficient vector,

\[
 \boxed{
 \sup_{p_\nu\ge0,\ \sum p_\nu\le1}
       \sum_\nu c_\nu p_\nu^{2/3}
 =\left(\sum_\nu c_\nu^3\right)^{1/3}.}
\tag{S.341}
\]

Equality holds for
\(p_\nu=c_\nu^3/\sum_\omega c_\omega^3\) when the denominator is
nonzero.  To pass from a node tree to the incidence sum in (S.340), assume
that the root family and incidence map obey the uniform bounds

\[
 \sum_{v\in{\rm roots}}c_v^3\le C_{\rm root},
 \qquad
 \#\{\hbox{incidences carrying a fixed node }v\}\le M_{\rm inc}.
\]

A sufficient uniform Dini-Carleson condition is then

\[
 0\le\theta_d,\qquad
 \sum_{w\in{\rm child}(v)}c_w^3\le\theta_d c_v^3,
 \qquad
 \sup_{d_0\ge0}\sum_{n\ge0}
       \prod_{j=0}^{n-1}\theta_{d_0+j}
 \le C_D<\infty.
\]

Indeed these three hypotheses give
\(\sum_{\rm incidences}c_\nu^3
 \le M_{\rm inc}C_{\rm root}C_D\), so they supply the constant \(C_c\)
required in (S.340).  The uniform condition
\(\theta_d\le\theta<1\) is a simple special case.  The model (S.335) has
\(\theta_d=1\); its finite-depth Dini constant grows like
\(L=m^3\), explaining exactly why critical branching does not close a
uniform cubic coefficient sum.

## 9. Route decision

Step 13 removes two unproductive directions.

1. Increasing scalar time regularity of the whole flux density is not enough.
   The next short-branch target must be genuinely shell selective.  One clean
   sufficient input is

   \[
    \boxed{
    \exists p\in(1,\infty],N_F,C:\quad
    \mathfrak H^F_{p,N_F,R}\le C(P_R^M)^{2/3}.}
   \tag{S.342}
   \]

   The deletion set in (S.342) is fixed across time.  A pointwise moving
   exceptional set is insufficient.
2. For the excess branch, the next target is the weaker combined envelope
   (S.328), not separate universal bounds on \(M_R\) and \(L_R\).  A proof
   may trade a larger path length against a smaller cylinder-density
   coefficient, provided the product stays at the quadratic payment scale.
3. Pure high-frequency heat shears are not candidate counterexamples to the
   physical-window gate.  Any further exact-family search must create
   physical annular separation and survive the \(Q\), cubic, pressure, and
   drift ledgers simultaneously.

The first task in the next step is to decompose
\(\mathfrak H^F_{p,N,R}\) into local cubic, local pressure, harmonic pressure,
and drift tails after finitely many inner shells, and test whether the
super-Gaussian weights plus the local-energy equation give a sublinear
\(\ell^1(L^p)\) tail.  In parallel, (S.328) should be tested against a
dyadic stopping-tree construction for the total dissipation measure.

## 10. Claim ledger

The following are **PROVED** in the frozen setting:

- the dimensionless representation (S.307)--(S.309);
- fixed-solution \(\ell^1(L_t^{4/3})\) finiteness and the
  \(\delta^{1/4}\) common-window bound (S.310)--(S.313);
- the general common-deletion Hölder bound (S.314)--(S.315);
- the exact optimization algebra (S.317)--(S.322), conditional on the
  explicitly stated temporal-tail hypothesis (S.316);
- the smooth all-\(p\) abstract saturation witness (S.323)--(S.325);
- the payment-dependent Morrey implication (S.326)--(S.330), conditional on
  the explicit geometric envelope (S.328);
- sharpness of the exponent threshold for the two-scalar-cap inference,
  through the abstract sequence witness (S.331);
- the exact heat-shear identities and zero physical-flux conclusion
  (S.332)--(S.334);
- the critical eight-ary abstract countermodel (S.335)--(S.339); and
- the conditional incidence-charging theorem, exact cubic duality, and
  Dini-subcritical tree criterion (S.340)--(S.341).

The following are **ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES**:

- the smooth synchronized temporal family (S.323)--(S.325);
- the adaptive smooth rate/depth family following (S.325);
- the equal-coordinate two-cap family (S.331); and
- the eight-ary critical ancestor tree (S.335)--(S.339).

The following remain **OPEN**:

- a uniform payment bound for
  \(\mathfrak H^F_{4/3,N,R}\), including the optimistic linear bound used
  only as a method test;
- the quadratic shell-selective estimate (S.342);
- a PDE construction of the incidence data in (S.340), including a strict
  cubic Dini-Carleson gain;
- the payment-dependent moving-tube estimate (S.328) for the bare suitable-
  weak class;
- the universal gates (S.280), (S.288), and (S.303), Step 11 (S.272), Q.12,
  and Q.1; and
- scale contraction, regularity, singularity formation, and the
  Navier--Stokes Millennium problem.

The advance is a proved fixed-solution algebraic terminal modulus, an exact
time-integrability exponent ceiling for the present two-term method, a
strictly weaker combined Morrey interface for the excess branch, and a
critical-tree obstruction that identifies strict cubic Dini decay as the
next conditional packing interface.  **NOT CLAY.**
