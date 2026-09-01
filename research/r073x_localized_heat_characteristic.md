# R0.73X — Localized heat-characteristic identities on a fixed parabolic cylinder

Status: **INTERNAL DERIVATION / OPEN ESTIMATE**

Claim class: **SMOOTH EXACT + SUITABLE-WEAK DISTRIBUTIONAL + OPEN**

Ordinary translation path: `LOCAL_DIRECT_NO_DGX`

DGX used: `false`

This note localizes the exact R0.73W heat-plane identities by a cutoff on a
fixed parabolic cylinder.  Its purpose is bookkeeping: every boundary flux,
pressure covariance, centered cubic increment, viscous carré-du-champ, and
suitable-weak energy defect is kept visible.

The identities below are not a regularity theorem, not a singularity
construction, and not progress on the Clay Navier–Stokes problem.  The new
mathematical obstruction is an estimate, stated explicitly in Section 8.

---

## 1. Setting and notation

Work on the normalized three-torus, with viscosity \(\nu>0\), and write

\[
 \partial_tu+\nabla\!\cdot(u\otimes u)+\nabla p=\nu\Delta u,
 \qquad \nabla\!\cdot u=0.
\tag{X1.1}
\]

For heat scale \(s>0\), let

\[
 P_s=e^{s\Delta},\qquad v_s=P_su,\qquad p_s=P_sp,
 \qquad \tau_s=P_s(u\otimes u)-v_s\otimes v_s.
\tag{X1.2}
\]

The resolved and subfilter energies are

\[
 e_s=\frac12|v_s|^2,
 \qquad
 k_s=\frac12\operatorname{tr}\tau_s
     =P_s\!\left(\frac12|u|^2\right)-e_s.
\tag{X1.3}
\]

Use the R0.73W sign convention

\[
 \Pi_s=-\tau_s:\nabla v_s,
\tag{X1.4}
\]

so positive \(\Pi_s\) is a sink of resolved energy.  Define

\[
 F_s=(e_s+p_s)v_s+\tau_sv_s.
\tag{X1.5}
\]

Let \(g_s\) be the periodic heat kernel and set

\[
 a_s(x,y)=u(x-y)-v_s(x),
 \qquad
 K_{j,s}(x)=\frac12\int_{\mathbb T^3}g_s(y)
       a_{s,j}(x,y)|a_s(x,y)|^2\,dy,
\tag{X1.6}
\]

\[
 \mathscr S_s(x)
 =-\frac12\int_{\mathbb T^3}\nabla g_s(y)\!\cdot a_s(x,y)
          |a_s(x,y)|^2\,dy.
\tag{X1.7}
\]

Then the exact centered-increment split is

\[
 \Pi_s=\nabla\!\cdot K_s+\mathscr S_s.
\tag{X1.8}
\]

The pressure covariance and viscous carré-du-champ are

\[
 Q_{j,s}=P_s(pu_j)-p_sv_{s,j},
\tag{X1.9}
\]

\[
 D_{ii,s}=P_s(|\nabla u|^2)-|\nabla v_s|^2
 =2\int_0^sP_{s-r}|\nabla^2v_r|_F^2\,dr\ge0.
\tag{X1.10}
\]

The covariance \(Q_s\) is invariant under the pressure gauge change
\(p\mapsto p+c(t)\).

---

## 2. Fixed cylinder, fixed cutoff, descending heat characteristic

For \(0<r<R\), use the viscosity-adapted backward cylinder

\[
 Q_R^\nu(z_0)
 =\left(t_0-\frac{R^2}{\nu},t_0\right)\times B_R(x_0).
\tag{X2.1}
\]

Take a nonnegative product cutoff

\[
 \chi(t,x)=\eta(t)\phi(x)\in C_c^\infty(Q_R^\nu),
 \qquad 0\le\chi\le1,
\tag{X2.2}
\]

equal to one on a smaller cylinder.  It may be chosen so that

\[
 |\partial_t\chi|\lesssim\frac{\nu}{(R-r)^2},\qquad
 |\nabla\chi|\lesssim\frac1{R-r},\qquad
 |\Delta\chi|\lesssim\frac1{(R-r)^2}.
\tag{X2.3}
\]

The word *fixed* is essential: \(\chi\) is independent of \(s\), and its
spatial support does not move with the heat characteristic.  Let

\[
 s(t)=s_a-\nu(t-a),\qquad s'(t)=-\nu,
\tag{X2.4}
\]

on \([a,b]\), with

\[
 0<\sigma\le s(t)\le s_*\lesssim(R-r)^2.
\tag{X2.5}
\]

The lower bound \(\sigma>0\) is retained for the weak formulation.  It is not
legitimate to set \(s=0\) in the weak identities without a separate limiting
argument.

---

## 3. Smooth exact resolved-energy identity

For a smooth solution, R0.73W gives the pointwise heat-plane identity

\[
 (\partial_t-\nu\partial_s)e_s+\nabla\!\cdot F_s=-\Pi_s.
\tag{X3.1}
\]

Define

\[
 E_\chi(t)=\int_{\mathbb T^3}\chi(t,x)e_{s(t)}(t,x)\,dx.
\tag{X3.2}
\]

Multiplication by \(\chi\), spatial integration, and the chain rule along
\(s'(t)=-\nu\) give

\[
 \boxed{
 \frac{d}{dt}E_\chi(t)
 =-\int\chi\Pi_s\,dx
  +\int F_s\!\cdot\nabla\chi\,dx
  +\int e_s\partial_t\chi\,dx .}
\tag{X3.3}
\]

Thus

\[
 \boxed{
 \begin{aligned}
 \int_a^b\!\!\int\chi\Pi_{s(t)}\,dx\,dt
 ={}&E_\chi(a)-E_\chi(b)\\
 &+\int_a^b\!\!\int F_{s(t)}\!\cdot\nabla\chi\,dx\,dt
 +\int_a^b\!\!\int e_{s(t)}\partial_t\chi\,dx\,dt .
 \end{aligned}}
\tag{X3.4}
\]

Unlike the torus mean identity, (X3.4) contains a genuine spatial cutoff
flux.  It has no sign.

Using (X1.8),

\[
 \int\chi\Pi_s\,dx
 =-\int K_s\!\cdot\nabla\chi\,dx+
   \int\chi\mathscr S_s\,dx.
\tag{X3.5}
\]

Consequently, the centered-increment form is

\[
 \boxed{
 \begin{aligned}
 \int_a^b\!\!\int\chi\mathscr S_{s(t)}\,dx\,dt
 ={}&E_\chi(a)-E_\chi(b)\\
 &+\int_a^b\!\!\int(F_{s(t)}+K_{s(t)})\!\cdot\nabla\chi\,dx\,dt\\
 &+\int_a^b\!\!\int e_{s(t)}\partial_t\chi\,dx\,dt .
 \end{aligned}}
\tag{X3.6}
\]

Equation (X3.6), not the unlocalized torus mean, is the relevant signed cubic
ledger on a fixed cylinder.

---

## 4. Smooth exact subfilter trace balance at fixed heat scale

At a fixed \(s>0\), the exact R0.73W trace equation is

\[
 \partial_tk_s+
 \nabla\!\cdot\bigl(v_sk_s+Q_s-\nu\nabla k_s\bigr)
 =-\nu D_{ii,s}+\mathscr S_s.
\tag{X4.1}
\]

Put

\[
 G_s=v_sk_s+Q_s-\nu\nabla k_s.
\tag{X4.2}
\]

Localization by the fixed cutoff yields

\[
 \boxed{
 \frac{d}{dt}\int\chi k_s\,dx
 +\nu\int\chi D_{ii,s}\,dx
 =\int\chi\mathscr S_s\,dx
  +\int G_s\!\cdot\nabla\chi\,dx
  +\int k_s\partial_t\chi\,dx .}
\tag{X4.3}
\]

All three non-periodic terms are now explicit:

* transport of subfilter energy, \(v_sk_s\cdot\nabla\chi\);
* pressure covariance flux, \(Q_s\cdot\nabla\chi\);
* viscous boundary flux, \(-\nu\nabla k_s\cdot\nabla\chi\).

The nonnegative bulk term is \(D_{ii,s}\).  Neither
\(\mathscr S_s\) nor any of the cutoff fluxes has a prescribed sign.

---

## 5. Smooth exact subfilter balance along the heat characteristic

Because \(s=s(t)\), (X4.3) acquires the chain-rule term
\(-\nu\partial_sk_s\).  With

\[
 K_\chi(t)=\int\chi(t,x)k_{s(t)}(t,x)\,dx,
\tag{X5.1}
\]

the exact identity with the carré-du-champ left visible is

\[
 \boxed{
 \begin{aligned}
 \frac{d}{dt}K_\chi(t)
 &+\nu\int\chi\bigl(\partial_sk_s+D_{ii,s}\bigr)\,dx\\
 &=\int\chi\mathscr S_s\,dx
  +\int\bigl(v_sk_s+Q_s-\nu\nabla k_s\bigr)
       \!\cdot\nabla\chi\,dx
  +\int k_s\partial_t\chi\,dx .
 \end{aligned}}
\tag{X5.2}
\]

Here and below every field on the right side is evaluated at \(s=s(t)\).
The term \(\partial_sk_s\) has no sign and must not be merged silently with
the nonnegative \(D_{ii,s}\).

There is, however, an exact heat-scale identity

\[
 (\partial_s-\Delta)k_s=|\nabla v_s|^2.
\tag{X5.3}
\]

Using (X5.3), integrating \(\Delta k_s\) against \(\chi\), and cancelling
the resulting term with the viscous cutoff flux in (X5.2) gives the equivalent
form

\[
 \boxed{
 \begin{aligned}
 \frac{d}{dt}K_\chi(t)
 +\nu\int\chi\,P_s(|\nabla u|^2)\,dx
 ={}&\int\chi\mathscr S_s\,dx\\
 &+\int(v_sk_s+Q_s)\!\cdot\nabla\chi\,dx
 +\int k_s\partial_t\chi\,dx .
 \end{aligned}}
\tag{X5.4}
\]

The equality

\[
 |\nabla v_s|^2+D_{ii,s}=P_s(|\nabla u|^2)
\tag{X5.5}
\]

is the precise reason the collapsed dissipation in (X5.4) is nonnegative.
Equations (X5.2) and (X5.4) are the same identity; (X5.2) is the audit form
that keeps \(D_{ii,s}\) explicit.

Adding (X3.3), in its centered form, to (X5.4) cancels
\(\mathscr S_s\) and gives the consistency check

\[
 \boxed{
 \begin{aligned}
 \frac{d}{dt}\int\chi(e_s+k_s)\,dx
 +\nu\int\chi P_s(|\nabla u|^2)\,dx
 ={}&\int\bigl(F_s+K_s+v_sk_s+Q_s\bigr)
            \!\cdot\nabla\chi\,dx\\
 &+\int(e_s+k_s)\partial_t\chi\,dx .
 \end{aligned}}
\tag{X5.6}
\]

This cancellation is an algebraic check, not an estimate for either signed
cubic term separately.

---

## 6. Suitable weak solutions: distributional identity with defect measure

Let \((u,p)\) be a suitable weak solution on the full torus throughout an
open time interval containing the time projection of \(Q_R^\nu\).  This
global-in-space hypothesis is needed because \(P_su\), \(P_sp\), and
\(P_s\mu\) sample points outside \(B_R(x_0)\).  Write its local energy
relation as

\[
 \partial_t\frac{|u|^2}{2}
 +\nabla\!\cdot\left[\left(\frac{|u|^2}{2}+p\right)u
                    -\nu\nabla\frac{|u|^2}{2}\right]
 =-\nu|\nabla u|^2-\mu
\tag{X6.1}
\]

in distributions, where \(\mu\ge0\) is the local energy-defect measure.
For a smooth solution, \(\mu=0\).

For each fixed \(s>0\), spatial heat convolution and subtraction of the
resolved equation give

\[
 \boxed{
 \partial_tk_s+
 \nabla\!\cdot(v_sk_s+Q_s-\nu\nabla k_s)
 =-\nu D_{ii,s}+\mathscr S_s-P_s\mu }
\tag{X6.2}
\]

in distributions.  Spatial convolution of the measure is defined by duality:

\[
 \langle P_s\mu,\psi\rangle
 =\int P_s\psi(t,\cdot)(y)\,d\mu(t,y).
\tag{X6.3}
\]

For the descending characteristic with \(s(t)\ge\sigma>0\), define the
nonnegative measure \(\mathcal M_{\chi,s}\) on time by

\[
 \int_a^b\rho(t)\,d\mathcal M_{\chi,s}(t)
 :=\int_{(a,b)\times\mathbb T^3}
       \rho(t)P_{s(t)}\chi(t,\cdot)(y)\,d\mu(t,y)
\tag{X6.4}
\]

for bounded Borel \(\rho\).  This definition does not assume that \(\mu\)
has a time density.

Because \(s(t)\ge\sigma>0\), heat smoothing makes
\(s\mapsto k_s(t,\cdot)\) continuously differentiable in the spatially
smoothed \(L^1\) class for almost every \(t\), with locally integrable
\(\partial_sk_s\).  Testing (X6.2) by smooth approximations to the graph
\(s=s(t)\), and using (X6.4) for its measure term, therefore justifies the
distributional pullback below.  For every
\(\rho\in C_c^\infty((a,b))\), the explicit carré-du-champ form is

\[
 \boxed{
 \begin{aligned}
 -\int_a^b\rho'(t)K_\chi(t)\,dt
 &+\nu\int_a^b\rho(t)\!\int\chi
       (\partial_sk_s+D_{ii,s})\,dx\,dt\\
 ={}&\int_a^b\rho(t)\!\int\chi\mathscr S_s\,dx\,dt\\
 &+\int_a^b\rho(t)\!\int
       (v_sk_s+Q_s-\nu\nabla k_s)\!\cdot\nabla\chi\,dx\,dt\\
 &+\int_a^b\rho(t)\!\int k_s\partial_t\chi\,dx\,dt
 -\int_a^b\rho(t)\,d\mathcal M_{\chi,s}(t).
 \end{aligned}}
\tag{X6.5}
\]

Equivalently, after the same exact cancellation used in Section 5,

\[
 \boxed{
 \begin{aligned}
 -\int_a^b\rho'(t)K_\chi(t)\,dt
 &+\nu\int_a^b\rho(t)\!\int
       \chi P_s(|\nabla u|^2)\,dx\,dt\\
 ={}&\int_a^b\rho(t)\!\int\chi\mathscr S_s\,dx\,dt\\
 &+\int_a^b\rho(t)\!\int(v_sk_s+Q_s)
       \!\cdot\nabla\chi\,dx\,dt\\
 &+\int_a^b\rho(t)\!\int k_s\partial_t\chi\,dx\,dt
 -\int_a^b\rho(t)\,d\mathcal M_{\chi,s}(t).
 \end{aligned}}
\tag{X6.6}
\]

For \(\chi,\rho\ge0\), the last term is favorable.  It does not supply a
bound on \(\mathscr S_s\), \(Q_s\cdot\nabla\chi\), or the transport flux.

The resolved identity (X3.3) also holds distributionally for \(s\ge\sigma\):
spatial smoothing makes every resolved factor meaningful, and no defect
measure enters that resolved equation.  The defect appears only when the
filtered full-energy relation is compared with the resolved relation.

The weak claim made here is exactly (X6.2), (X6.5), and (X6.6) in the sense of
distributions.  No pointwise-in-time endpoint equality and no \(s\downarrow0\)
limit is asserted.

---

## 7. What localization changes

The periodic mean identity suppresses all divergences.  A fixed cylinder does
not.  The exact local ledger contains:

1. the resolved cutoff flux \(F_s\cdot\nabla\chi\);
2. the centered third-order cutoff flux \(K_s\cdot\nabla\chi\);
3. the subfilter transport flux \(v_sk_s\cdot\nabla\chi\);
4. the pressure covariance flux \(Q_s\cdot\nabla\chi\);
5. the viscous cutoff flux \(-\nu\nabla k_s\cdot\nabla\chi\), before the exact
   heat-scale cancellation;
6. the signed centered production \(\chi\mathscr S_s\);
7. the nonnegative carré-du-champ \(\chi D_{ii,s}\);
8. the nonnegative suitable-weak defect \(P_s\mu\), with a favorable sign;
9. the time-cutoff payment \(e_s\partial_t\chi\) or
   \(k_s\partial_t\chi\).

There is also a nonlocality that a compactly supported cutoff does not remove.
The heat kernel samples \(u\), \(p\), and \(\mu\) outside \(B_R\).  The
restriction \(s_*\lesssim(R-r)^2\) makes Gaussian tails small only after an
actual tail estimate; it does not make them vanish.  Therefore these are
spatially localized identities, not identities determined solely by data in
the cylinder.

If an \(s\)-dependent cutoff is used instead, every characteristic identity
acquires an additional term \(-\nu\int(\partial_s\chi)e_s\) or
\(-\nu\int(\partial_s\chi)k_s\).  Those terms are absent here precisely
because the cutoff is fixed.

---

## 8. Open estimate and present blocking points

The exact algebra is closed.  The estimate needed for a useful local theorem
is not.

A representative non-circular target would control the two unsigned cubic and
pressure terms by local scale-invariant data, for \(s(t)\simeq R^2\), in a form
such as

\[
 \begin{aligned}
 &\left|\int_a^b\!\!\int\chi\mathscr S_{s(t)}\,dx\,dt\right|
 +\left|\int_a^b\!\!\int Q_{s(t)}\!\cdot\nabla\chi\,dx\,dt\right|\\
 &\qquad\le
 \varepsilon\nu\int_a^b\!\!\int
       \chi P_{s(t)}(|\nabla u|^2)\,dx\,dt
 +C_\varepsilon\,\mathcal E(Q_R^\nu),
\end{aligned}
\tag{X8.1}
\]

where \(\mathcal E(Q_R^\nu)\) must itself be controlled at the suitable-weak
energy level and must not assume a Serrin, Hölder, or regularity norm that
already resolves the problem.  Its normalization is part of the target:
\(\mathcal E(Q_R^\nu)=R\,\mathfrak R(z_0,R)\), where \(\mathfrak R\) is
dimensionless and has at least the cubic amplitude degree of the left side
(for example, a declared combination beginning with a local energy quantity
to the \(3/2\) power, together with pressure, defect, and annular-tail
payments).  A merely quadratic local-energy remainder is already excluded by
amplitude scaling and is not being left open here.  Equation (X8.1) is a
schematic target, not a proved inequality; a theorem must replace
\(\mathfrak R\) by one fully specified functional.

The blocking points are:

* **Centered cubic term.**  \(\mathscr S_s\) is signed and cubic.  The global
  absolute R0.73W bound loses a negative power of \(s\); localization alone
  does not repair that loss.
* **Pressure covariance.**  \(Q_s\cdot\nabla\chi\) has no sign.  Calderón–Zygmund
  control is spatially nonlocal and brings both cutoff commutators and exterior
  pressure tails.
* **Heat-kernel tails.**  A compactly supported \(\chi\) does not localize
  \(P_s\).  Quantitative annular tail payments are required before a genuinely
  local iteration can be attempted.
* **Characteristic scale derivative.**  In the audit form (X5.2),
  \(\partial_sk_s\) is not nonnegative.  It becomes harmless only through the
  exact cancellation leading to (X5.4); it cannot be discarded in an
  inequality derived directly from (X5.2).
* **Endpoint \(s=0\).**  The weak identities are secure for \(s\ge\sigma>0\).
  Passing to \(s=0\) requires uniform integrability or compactness not supplied
  by the identities.
* **Defect measure.**  The sign of \(\mu\) helps, but it controls neither the
  signed cubic term nor the pressure/cutoff fluxes.  Treating it as if it did
  would reverse the logic of suitability.

Until at least the cubic, pressure, and tail payments are controlled in a
scale-compatible and non-circular way, no epsilon-regularity improvement,
singular-set reduction, or Clay-level conclusion follows.

---

## 9. Claim boundary

### Smooth exact

Equations (X3.3)–(X3.6), (X4.3), and (X5.2)–(X5.6) follow by exact algebra,
integration by parts, and the chain rule for \(s'(t)=-\nu\).

### Suitable weak, distributional

Equations (X6.2), (X6.5), and (X6.6) follow from the suitable local energy
relation with defect measure, spatial heat convolution, and testing away from
\(s=0\).  They are distributional statements; no smooth endpoint identity is
claimed for an arbitrary weak solution.

### Open

An estimate of the type (X8.1), with all pressure and heat-tail payments and
with no hidden regularity hypothesis, remains open in this research line.

### Explicit non-claim

This note does not prove regularity, exclude blow-up, construct a singularity,
or advance the Clay Millennium problem.  It identifies the exact localized
ledger that any later estimate must pay.
