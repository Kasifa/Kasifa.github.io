# R0.74E local-frame independent audit: Sections 1--6

## Result and exact scope

This is an independent formula-by-formula audit of Sections 1--6 of the
R0.74E local mollified-frame gate.  The audited snapshot is **PASS** for the
claims that it labels as proved:

- the common mollifier, terminal trajectory, and periodic lift;
- the general moving/subtracting transformation;
- the Version-M and Version-F equations and local-energy signs;
- the filtered acceleration identity;
- the periodic-pressure versus affine-pressure boundary;
- the matching-mollifier cancellation and the absence of an automatic
  cancellation at other scales or for other cutoffs;
- the pointwise support comparison (4.12d), with a strict separation between
  auxiliary cubic support bookkeeping and acceleration moments; and
- the Version-M and Version-F familywise neutralization of the explicit
  R0.74D family.

This result is not an arbitrary-solution estimate.  In particular, it does
not prove either frozen endpoint (3.11) or (4.17), does not absorb the
Version-F acceleration for a general solution, and has no regularity or
global-smoothness consequence.

## Audited snapshot

The main authority was read at the following SHA-256 digest:

| File | SHA-256 |
|---|---|
| `research/r074e_local_mollified_frame_gate.md` | `3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7` |

For the inherited exact family and estimates invoked in Section 6, the
frozen R0.74D analytic source was also checked:

| File | SHA-256 |
|---|---|
| `research/r074d_zero_mean_local_transport_obstruction.md` | `bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124` |

The audited main snapshot includes two wording corrections that are
mathematically important for literal reading:

1. the closed support in (4.12c) is contained in
   \(\{\operatorname{dist}(y,A_j(R))\le R/8\}\), with a non-strict endpoint;
2. (4.10) supplies an automatic cancellation only at the matching radius;
   it does not assert that accidental cancellation is impossible for a
   special field at another radius.

Both corrected statements are used below.

## Audit method and reproduction

Every sign below was recomputed from the original periodic Navier--Stokes
equation

\[
 \partial_tu-\Delta u+(u\cdot\nabla)u+\nabla p=0,
 \qquad \nabla\cdot u=0.
\]

The local-energy identities were obtained by multiplying the transformed
equations by \(2W\chi\), integrating by parts, and keeping the force on its
original side.  The acceleration formula was recomputed by differentiating
\(u_R(t,X_R(t))\) and independently filtering the equation.  The shell
comparison was checked radially, including all padding endpoints.  The
Section 6 powers of \(R\), \(M_m\), and \(A\) were recomputed from the
displayed volumes and weights rather than inferred from the endpoint
statements.

The read-only inspection and final validation commands were:

```bash
shasum -a 256 \
  research/r074e_local_mollified_frame_gate.md \
  research/r074d_zero_mean_local_transport_obstruction.md

rg -n 'tag\{|3\.11|4\.17|PROVED|OPEN|NOT CLAY' \
  research/r074e_local_mollified_frame_gate.md

python3 - <<'PY'
from fractions import Fraction as F
from pathlib import Path

raw = Path('research/r074e_local_frame_independent_audit.md').read_bytes()
assert not [
    (offset, byte) for offset, byte in enumerate(raw)
    if byte < 32 and byte not in (9, 10)
]

# Section 6 shell coefficient and powers.
assert 2 * F(3, 2) ** 4 == F(81, 8)

# The fixed smallness used in the translated offset.
assert F(1, 4) * F(1, 2048) <= F(1, 8192)

# The elementary two-lobe inequality has coefficient 1/2.
x, y = F(7, 5), F(-11, 7)
alpha = F(13, 17)
assert (x-alpha)**2 + (y-alpha)**2 >= F(1, 2) * (x-y)**2
PY

git diff --check
git diff --no-index --check /dev/null \
  research/r074e_local_frame_independent_audit.md || test $? -eq 1
```

The inline rational checks are only sanity checks for displayed finite
coefficients.  The analytic estimates are audited by the derivations below,
not certified by that short program.  The ordinary diff check emitted no
diagnostics.  In no-index mode, exit status one records that the intentionally
new file differs from `/dev/null`; it emitted no whitespace-error diagnostic.

## 1. Mollifier, terminal trajectory, and matching mean

Let \(\varphi\in C_c^\infty(B_1)\) be nonnegative, even, radial, and of
unit integral.  Its periodic rescaling is

\[
 \varphi_\rho^{\rm per}(x)
 =\sum_{k\in\mathbb Z^3}\rho^{-3}
   \varphi\!\left(\frac{\widetilde x+2\pi k}{\rho}\right).
\]

The factor is \(\rho^{-3}\), so the normalization remains one at every
admissible radius.  For the principal scale \(R\), the terminal problem is

\[
 \dot X_R(t)=u_R(t,X_R(t)),\qquad X_R(t_0)=x_0,
 \qquad a_R(t)=\dot X_R(t).
\]

Solving this ODE backward from \(t_0\) does not reverse the sign of its
right-hand side.  Smoothness of \(u_R\) gives existence and uniqueness on
the frozen compact time interval.  The definitions

\[
 v_R(t,y)=u(t,y+X_R(t)),\qquad
 w_R(t,y)=v_R(t,y)-a_R(t),\qquad
 \pi_R(t,y)=p(t,y+X_R(t))
\]

use one and the same trajectory at radii \(R,2R,8R\).  A continuous
Euclidean lift changes by a lattice vector when another lift is chosen;
periodicity therefore makes the lifted fields independent of that choice.

Evenness of the kernel is needed in the following calculation:

\[
\begin{aligned}
 \int_{\mathbb T^3}\varphi_R^{\rm per}(y)v_R(t,y)\,dy
 &=\int_{\mathbb T^3}\varphi_R^{\rm per}(y)
     u(t,X_R(t)+y)\,dy \\
 &=u_R(t,X_R(t))=a_R(t).
\end{aligned}
\]

Since \(\int\varphi_R^{\rm per}=1\), this proves the exact weighted-mean
identity

\[
 \int_{\mathbb T^3}\varphi_R^{\rm per}(y)w_R(t,y)\,dy=0.
\]

The identity belongs to \(w_R\), not to \(v_R\), and it is tied to the
same kernel and the same radius that define the trajectory.

## 2. General moving/subtracting transformation

Let \(X'=a(t)\), let \(c(t)\) be spatially constant, and define

\[
 W(t,y)=u(t,y+X(t))-c(t),\qquad
 P(t,y)=p(t,y+X(t)).
\]

The chain rule gives

\[
 \partial_tW=u_t(t,y+X)+a\cdot\nabla u(t,y+X)-c'.
\]

Because \(u=W+c\), while \(a\) and \(c\) have no spatial derivatives,
substitution into Navier--Stokes yields

\[
 \boxed{
 \partial_tW-\Delta W+(W+c-a)\cdot\nabla W+\nabla P=-c',
 \qquad \nabla\cdot W=0.}
\]

All signs in (2.2) follow from this line.  In particular:

- moving coordinates contributes \(-a\) to the convecting velocity;
- subtracting \(c\) contributes \(+c\) to that velocity; and
- time-dependent subtraction contributes the body force \(-c'\).

Thus a general transformed field is canonical, periodic, and unforced only
when the residual convection and the subtraction match and the subtracted
constant has zero acceleration.  Special solutions may have additional
degenerate cancellations, but those are not structural consequences of the
change of variables.

## 3. Version M: equation and local-energy signs

Setting \(c=0\) gives

\[
 \boxed{
 \partial_tv_R-\Delta v_R+(v_R-a_R)\cdot\nabla v_R
 +\nabla\pi_R=0.}
\]

This equation has the physical periodic pressure and no body force.  Its
price is the residual transport \(-a_R\cdot\nabla v_R\).

Put \(b=v_R-a_R\).  Since both \(v_R\) and the spatially constant
\(a_R\) are divergence free, \(\nabla\cdot b=0\).  Multiplication by
\(2v_R\chi\) gives the four integration-by-parts identities

\[
\begin{aligned}
 2\int \partial_tv_R\cdot v_R\chi
 &=\frac d{dt}\int|v_R|^2\chi-\int|v_R|^2\partial_t\chi,\\
 -2\int \Delta v_R\cdot v_R\chi
 &=2\int|\nabla v_R|^2\chi-\int|v_R|^2\Delta\chi,\\
 2\int (b\cdot\nabla v_R)\cdot v_R\chi
 &=-\int|v_R|^2b\cdot\nabla\chi,\\
 2\int\nabla\pi_R\cdot v_R\chi
 &=-2\int\pi_Rv_R\cdot\nabla\chi.
\end{aligned}
\]

After time integration, these identities give precisely

\[
\begin{aligned}
 &\int|v_R(\tau)|^2\chi(\tau)
 +2\int_{t_a}^{\tau}\!\int|\nabla v_R|^2\chi \\
 &\le \int_{t_a}^{\tau}\!\int|v_R|^2
       (\partial_t\chi+\Delta\chi)
 +\int_{t_a}^{\tau}\!\int
   \bigl[|v_R|^2(v_R-a_R)+2\pi_Rv_R\bigr]\cdot\nabla\chi.
\end{aligned}
\]

The residual contribution is therefore

\[
 -\int |v_R|^2a_R\cdot\nabla\chi,
\]

with a minus sign inside the flux.  It is not an acceleration force.

The trajectory velocity is paid by the same cubic ledger.  Evenness and
Jensen give

\[
 |a_R(t)|^3
 \le\int\varphi_R^{\rm per}|v_R|^3
 \le CR^{-3}\int_{B_R}|v_R|^3.
\]

For the shell cutoffs, \(R|\nabla\psi_j^R|\le C1_{\operatorname{supp}
\psi_j^R}\).  Young's inequality and
\(\sum_j\gamma_j|\operatorname{supp}\psi_j^R|\le CR^3\) then give the
stated local-plus-supported-cubic estimate (3.5).  No term involving
\(a_R'\) is generated in Version M.

The endpoint inequality

\[
 X_R^M\stackrel{?}{\le}C(P_R^M)^{2/3}
\]

remains open for arbitrary solutions.  The definitions of \(X_R^M\) and
\(P_R^M\) use the same translated origin and the all-copy periodic lift;
changing the trajectory at \(2R\) or \(8R\) would change the statement.

## 4. Version F: acceleration, energy, and pressure

Setting \(c=a_R\) gives canonical convection but differentiates the
subtracted velocity:

\[
 \boxed{
 \partial_tw_R-\Delta w_R+(w_R\cdot\nabla)w_R+\nabla\pi_R=-a_R'.}
\]

### Filtered acceleration identity

Since \(a_R=u_R(t,X_R(t))\) and \(X_R'=u_R(t,X_R)\),

\[
 a_R'=\bigl[\partial_tu_R+(u_R\cdot\nabla)u_R\bigr](t,X_R(t)).
\]

Filtering Navier--Stokes gives

\[
 \partial_tu_R-\Delta u_R
 +\nabla\cdot(u\otimes u)_R+\nabla p_R=0.
\]

With

\[
 \tau_R=(u\otimes u)_R-u_R\otimes u_R
\]

and \(\nabla\cdot(u_R\otimes u_R)=(u_R\cdot\nabla)u_R\), the two formulas
combine to

\[
 \boxed{
 a_R'=\bigl[\Delta u_R-\nabla p_R-\nabla\cdot\tau_R\bigr](t,X_R(t)).}
\]

The stress sign is negative, as is the pressure-gradient sign.

### Version-F local energy sign

The unforced terms integrate exactly as in the canonical local-energy
identity.  The right-hand side contributes

\[
 2\int(-a_R')\cdot w_R\chi
 =-2a_R'(t)\cdot\int\chi(t,y)w_R(t,y)\,dy.
\]

Hence the force row in (4.3) has the audited sign

\[
 -2\int_{t_a}^{\tau}a_R'(t)\cdot
   \left(\int\chi(t,y)w_R(t,y)\,dy\right)dt.
\]

It must be retained unless the particular testing weight makes its moment
vanish.

### Periodic pressure and the affine rewrite

Taking divergence of the Version-F equation uses
\(\nabla\cdot a_R'=0\) and gives

\[
 \boxed{-\Delta\pi_R=\partial_i\partial_j(w_{R,i}w_{R,j}).}
\]

The spatially constant cross terms between \(w_R\) and \(a_R\) disappear
under double divergence.  Thus \(\pi_R\) remains the physical periodic
pressure and its source can be written using \(w_R\) alone.

On the Euclidean lift one may set

\[
 \Pi_R(t,y)=\pi_R(t,y)+a_R'(t)\cdot y.
\]

Then \(\nabla\Pi_R=\nabla\pi_R+a_R'\), so the displayed Version-F equation
looks unforced.  However,

\[
 \Pi_R(t,y+2\pi k)-\Pi_R(t,y)=2\pi a_R'(t)\cdot k.
\]

Unless \(a_R'=0\), \(\Pi_R\) is not a torus pressure.  The mean identity

\[
 \frac d{dt}\overline{w_R}=-a_R'
\]

gives the same obstruction, because an unforced canonical periodic solution
preserves its mean.

For the frozen super-Gaussian shell weights, the affine field has the finite
but nonzero row

\[
 \rho^{-2}\sum_{j\ge1}\gamma_j
 \int_{I_\rho}\!\int_{A_j(\rho)}|a_R'\cdot y|^{3/2}
 \,dy\,dt
 =C_\gamma\rho^{5/2}\int_{I_\rho}|a_R'|^{3/2}dt,
\]

where \(C_\gamma=C_*\sum_j\gamma_j2^{9j/2}<\infty\).  This finiteness does
not make the row a pressure gauge: it is a new scale-dependent payment, and
the \(L^{3/2}\) norm of the total pressure does not split linearly.

## 5. Matching cancellation versus all-scale noncancellation

Define the matching test weight

\[
 \chi_R(y)=R^3\varphi_R^{\rm per}(y).
\]

The weighted-mean identity from Section 1 implies, pointwise in time,

\[
 \int\chi_Rw_R=0,
 \qquad
 a_R'\cdot\int\chi_Rw_R=0.
\]

This is an exact automatic cancellation at the trajectory scale.  For
\(\chi_\rho=\rho^3\varphi_\rho^{\rm per}\), while keeping the same
\(R\)-trajectory,

\[
\begin{aligned}
 \int\chi_\rho w_R
 &=\rho^3\left[
   \int\varphi_\rho^{\rm per}(y)u(t,X_R+y)\,dy-a_R\right]\\
 &=\rho^3\bigl[u_\rho(t,X_R)-u_R(t,X_R)\bigr].
\end{aligned}
\]

The trajectory definition forces this expression to vanish at \(\rho=R\).
There is no corresponding identity at \(2R\) or \(8R\), or for a sharp
ball or shell cutoff.  This is a nonautomatic-cancellation statement, not a
claim of universal nonvanishing: a zero solution or another special field
may have accidental zeros.

## 6. The support estimate (4.12d) and functional ownership

Let

\[
 A_j(R)=\{2^jR\le|y|<2^{j+1}R\},
 \qquad \gamma_j=e^{-4^{j-1}/32},
\]

and let \(\psi_j^R\) equal one on \(A_j(R)\) with padding of width at most
\(R/8\).  With the standard closed-support convention, the corrected
statement is

\[
 \operatorname{supp}\psi_j^R
 \subset\{\operatorname{dist}(y,A_j(R))\le R/8\}.
\]

Also

\[
 W_{2R}(y)=\sum_{k\ge1}\gamma_k1_{A_k(2R)}(y),
 \qquad
 A_k(2R)=\{2^{k+1}R\le|y|<2^{k+2}R\}.
\]

For \(j\ge2\), the key identity is

\[
 A_j(R)=A_{j-1}(2R).
\]

For \(j\ge3\), the padding of \(A_j(R)\) can meet the central annulus
\(A_{j-1}(2R)\) and its two neighbours \(A_{j-2}(2R)\) and
\(A_j(2R)\).  The corresponding weights are respectively
\(\gamma_{j-1}\), \(\gamma_{j-2}\), and \(\gamma_j\), each at least
\(\gamma_j\).  The low-index pieces are handled by the \(8R\) core.  At a
fixed radius, only two padded shell supports can overlap.

For \(|y|<8R\), the total pointwise sum is bounded by an absolute constant
and is absorbed by \(1_{B_{8R}}\).  At \(|y|=8R\), the point belongs to
\(A_2(2R)\), which carries the needed weight, so there is no boundary gap.  For
\(|y|>8R\), the preceding annular comparison and monotonicity of
\(\gamma_j\) give, in fact with a harmless constant no larger than two,

\[
 \boxed{
 \sum_{j\ge1}\gamma_j1_{\operatorname{supp}\psi_j^R}
 \le C1_{B_{8R}}+CW_{2R}.}
\]

This proves (4.12d), including the closed padding endpoints.

Its use is limited to the auxiliary cubic term in (3.5):

\[
 \sum_j\gamma_j
 \int_{\operatorname{supp}\psi_j^R}|v_R|^3
 \le C\int_{B_{8R}}|v_R|^3
   +C\int W_{2R}|v_R|^3.
\]

It does not identify or dominate signed acceleration moments.  The shell
payment is

\[
 \mathcal J_{\rm acc,sh}^{F,R}
 =\frac2R\sum_{j\ge1}\gamma_j\int_{I_{2R}}|a_R'|
   \left|\int\psi_j^R\widetilde w_R\right|dt,
\]

and it retains every \(j\ge1\) term.  The independent core payment is

\[
 \mathcal J_{\rm acc,core}^{F,R}
 =\frac1{4R}\int_{I_{8R}}|a_R'|
   \left|\int\chi_{8R}^{\rm core}w_R\right|dt.
\]

Different test weights can have different cancellations.  Therefore the
core moment cannot replace any \(\psi_j^R\)-moment, even when part of the
support of that shell lies in the core.  The pointwise support estimate and
the acceleration functional have different mathematical ownership.

Consequently the frozen Version-F payment must retain

\[
 P_R^F
 =\mathcal E^{F,R}(z_0,8R)^{3/2}
  +\mathcal A_{\rm ext}^{F,R}(z_0,2R;1)
  +(\mathcal J_{\rm acc,sh}^{F,R}
    +\mathcal J_{\rm acc,core}^{F,R})^{3/2}.
\]

The arbitrary-solution inequality
\(X_R^F\stackrel?\le C(P_R^F)^{2/3}\) remains open.

## 7. Section 6 quantifiers and translated R0.74D geometry

Section 6 retains the exact R0.74D family

\[
 u=(AF,B_Re^{-t}\cos x_3,0),\qquad p=0,
\]

with

\[
 q_*=\frac12,\qquad M_m=3\,2^{m-1},\qquad q=q_m=M_mR,
 \qquad t_0=65R^2,
\]

and \(I_\rho=(t_0-\rho^2,t_0)\).  Define

\[
 D_R=e^{-R^2}-e^{-65R^2},\qquad
 B_R=\frac{q-q_*}{D_R}<0,
\]

and retain the reference path with

\[
 Q'(t)=B_Re^{-t},\qquad Q(R^2)=q_*,\qquad Q(t_0)=q.
\]

The mean-value bounds

\[
 64R^2e^{-65R^2}\le D_R\le64R^2,
 \qquad q_*-q\in[15/32,1/2]
\]

give the uniform estimate

\[
 cR^{-2}\le|B_R|\le CR^{-2}.
\]

The proved Section 6 statements have the uniform parameter range

\[
 A>0,\qquad M_m\ge64,
 \qquad M_mR\le\frac1{32},
 \qquad 0<R<R_E.
\]

Here \(R_E\) is fixed once for all as the minimum of the inherited chart
constant, \(2^{-11}\), and the two compact heat-kernel continuity
thresholds used for residence.  Constants \(c,C\) may depend on the frozen
mollifier and harmless chart data, but not on \(A,R,m\).

Since \(u_3=0\), \(X_{R,3}=0\).  Define

\[
 \mu_R=\int\varphi_R^{\rm per}(y)\cos y_3\,dy.
\]

The support of \(\varphi_R\) and \(1-\cos s\le s^2/2\) give

\[
 0\le1-\mu_R\le\frac{R^2}{2}.
\]

Because \(Q'=B_Re^{-t}\) and
\(\dot X_{R,2}=\mu_RB_Re^{-t}\), with terminal values
\(Q(t_0)=q\) and \(X_{R,2}(t_0)=0\),

\[
 X_{R,2}(t)=\mu_R[Q(t)-q].
\]

Thus the packet offset in translated coordinates is

\[
 q_R(t)=Q(t)-X_{R,2}(t)
 =\mu_Rq+(1-\mu_R)Q(t).
\]

On \(I_{8R}\), \(q\le Q(t)\le1/2\), and hence

\[
 0\le q_R(t)-q
 =(1-\mu_R)[Q(t)-q]
 \le\frac{R^2}{4}
 \le\frac{R}{8192}.
\]

The last inequality follows from the frozen choice \(R_E\le2^{-11}\).
This proves the uniform \(q_R=q+O(R^2)\) offset.  It does not by itself
prove mass residence.

## 8. Residence and the Version-M upper/lower pair

The reference-centred profile

\[
 G(t,z,x_3)=F(t,z+Q(t),x_3)
\]

has dimensionless heat age

\[
 62\le\frac{R^2+t}{R^2}\le66
 \qquad (t\in I_{2R}).
\]

On this compact interval, the two central real-Gaussian derivative lobes
have fixed opposite signs and a uniform positive magnitude on
\(z/R\in[b_1,b_2]\) and its negative reflection, with
\(1<b_1<b_2<2\).  The inherited weighted first-moment estimate makes the
nonautonomous displacement error \(O(R)\), uniformly on the whole interval,
and noncentral periodic images are \(O(e^{-c/R^2})\).  The fixed choice of
\(R_E\) absorbs both.  Therefore

\[
 |G(t,z,x_3)|\ge c_0
\]

for every admissible parameter triple, every \(t\in I_{2R}\),
\(|x_3|\le R\), and either signed lobe.  The quantifier is the full payment
interval, not only a terminal subinterval.

The translated lobe sets have volume

\[
 |\Omega_\pm(t)|\ge cqR^2=cM_mR^3.
\]

Since \(M_m=3\,2^{m-1}\),

\[
 A_m(R)=A_{m-1}(2R)
 =\left\{\frac{2q}{3}\le|y|<\frac{4q}{3}\right\}.
\]

The lower radial estimate follows from
\(q_R\ge q\) and \(q-2R\ge31q/32\).  The displayed upper Euclidean-norm
bound in (6.14), together with \(M_m\ge64\), puts both lobes below
\(4q/3\).  Thus the resident mass remains in the same physical shell when
the ledger is viewed at \(R\) or at \(2R\).

### Packet upper bound

After integrating the invariant \(y_1\)-direction and all periodic copies,
the effective weight satisfies

\[
 \omega_R(y_2,y_3)
 \le\frac{CR^4}{(\rho^2+R^2)^{3/2}},
 \qquad
 \rho=\operatorname{dist}_{\mathbb T^2}((y_2,y_3),0).
\]

On \(\rho\ge q/2\), this is at most \(CR^4/q^3\).  The inherited energy
bounds

\[
 \|F(t)\|_2^2\le CR^2,
 \qquad
 \int_{I_R}\|\nabla F(t)\|_2^2dt\le CR^2
\]

therefore give, after the outer \(R^{-1}\) normalization,

\[
 C R^{-1}\frac{R^4}{q^3}R^2
 =C\frac{R^2}{M_m^3}.
\]

On \(\rho<q/2\), the one-sided central-chart formula gives

\[
 |H|+R|\nabla H|
 \le C(1+M_m)^6e^{-M_m^2/1056}.
\]

Using \(\int\omega_R\le CR^3\), the time length \(|I_R|=R^2\), and
uniform absorption of the polynomial by the Gaussian for \(M_m\ge64\)
gives the same \(CR^2/M_m^3\) bound.  Multiplication by \(A^2\) proves

\[
 \boxed{X_{R,F}^M\le C\frac{A^2R^2}{M_m^3}.}
\]

### Compulsory harmonic lower bound

At scale \(2R\), the coefficient of \(A_{m-1}(2R)\) in \(L_{2R}\) is

\[
 2R(2^mR)^{-4}
 =2R\left(\frac{3}{2q}\right)^4
 =\frac{81}{8}Rq^{-4}.
\]

The packet has amplitude at least \(cA\) on a set of volume
\(cM_mR^3\) for every \(t\in I_{2R}\).  Hence

\[
 \Lambda_{2R,F}(t)
 \ge c(Rq^{-4})(A^2M_mR^3)
 =c\frac{A^2}{M_m^3}.
\]

Because \(|I_{2R}|=4R^2\), the harmonic functional satisfies

\[
\begin{aligned}
 \mathcal H_F^{M,R}
 &=2R\int_{I_{2R}}\Lambda_{2R,F}(t)^{3/2}dt\\
 &\ge c\frac{A^3R^3}{M_m^{9/2}},\\
 (\mathcal H_F^{M,R})^{2/3}
 &\ge c\frac{A^2R^2}{M_m^3}.
\end{aligned}
\]

This exactly pays the moved packet upper bound.  It also makes the old
exponentially weighted target negligible relative to this payment:

\[
 \frac{A^2M_mR^2e^{-M_m^2/288}}
      {(\mathcal H_F^{M,R})^{2/3}}
 \le CM_m^4e^{-M_m^2/288}\longrightarrow0.
\]

### Complete Version-M familywise conclusion

The shear part obeys

\[
 X_{R,b}^M\le CR^{-2},
 \qquad
 \mathcal H_b^{M,R}\ge cR^{-3},
 \qquad
 (\mathcal H_b^{M,R})^{2/3}\ge cR^{-2}.
\]

Indeed, the shear is of size \(|B_R|\asymp R^{-2}\) on a fixed fraction of
the first few shells.  Its kinematic supremum has size at most \(R^{-2}\),
while \(\Lambda_{2R,b}\gtrsim |B_R|^2\) and the factor
\(2R|I_{2R}|=8R^3\) give \(\mathcal H_b^{M,R}\gtrsim R^{-3}\).

The packet and shear occupy orthogonal velocity components, so their
quadratic contributions add at the \(\Lambda\) level.  For nonnegative
\(x,y\),

\[
 (x+y)^{3/2}\ge x^{3/2}+y^{3/2},
 \qquad
 x^{2/3}+y^{2/3}\le C(x+y)^{2/3}.
\]

Combining the two upper/lower pairs gives

\[
 X_R^M
 \le C\left(R^{-2}+\frac{A^2R^2}{M_m^3}\right)
 \le C(\mathcal H_{v_R}^{M,R})^{2/3}
 \le C(P_R^M)^{2/3}.
\]

The constant is uniform over every admissible \((A,R,m)\).  This proves
Proposition 6.4 for the explicit family only.

## 9. Version-F familywise neutralization

For \(w_R=v_R-a_R\), the first-component sampled mean is separated from
the packet by at least \((M_m-2)R\).  The inherited buffered Gaussian bound
gives

\[
 |a_{R,1}(t)|
 \le CA(1+M_m)^6e^{-M_m^2/528}
 \le C\frac{A}{M_m^{3/2}}.
\]

Its constant contribution to the kinematic exterior quantity is therefore

\[
 Ca_{R,1}^2R^2\le C\frac{A^2R^2}{M_m^3}.
\]

Subtraction cannot destroy both resident lobes.  At matched points with
\(g_+\ge c_0\) and \(g_-\le-c_0\), for every spatial constant \(\alpha\),

\[
 |g_+-\alpha|^2+|g_--\alpha|^2
 \ge\frac12|g_+-g_-|^2\ge2c_0^2.
\]

The first inequality follows by minimizing the left side at
\(\alpha=(g_++g_-)/2\).  Consequently the packet harmonic lower bound from
Section 8 remains valid for \(w_{R,1}\).

The residual shear is exactly

\[
 w_{R,2}=B_Re^{-t}(\cos y_3-\mu_R).
\]

Near the origin,

\[
 |\cos y_3-\mu_R|\le\frac{y_3^2+R^2}{2},
 \qquad
 |\partial_3w_{R,2}|\le |B_Ry_3|.
\]

Together with the exact weighted moments

\[
 \int W_R(y)|y_3|^{2k}dy\le C_kR^{3+2k},
 \qquad k=0,1,2,
\]

and \(|B_R|\asymp R^{-2}\), this gives the kinematic upper bound

\[
 X_{R,w_2}^F\le CR^2.
\]

The needed harmonic lower is deliberately taken away from the central
Gaussian region.  At \(S=2R\), integrating the all-copy weight in
\((y_1,y_2)\) and restricting to \(s=y_3\in[1,3/2]\) gives

\[
 \ell_S^{(1)}(s)\ge cS=cR.
\]

On this fixed interval \(|\cos s-\mu_R|\ge c\), and \(e^{-t}\) has a
uniform positive lower bound.  Therefore

\[
 \Lambda_{2R,w_2}(t)\ge cR|B_R|^2\ge cR^{-3},
\]

and

\[
 \mathcal H_{w_2}^{F,R}\ge cR^{-3/2},
 \qquad
 (\mathcal H_{w_2}^{F,R})^{2/3}\ge cR^{-1}.
\]

Since the packet and shear remain pointwise orthogonal velocity components,
their \(\Lambda\)-level lower bounds combine as in Version M.  Also
\(R^2\le CR^{-1}\) throughout the frozen small-scale range.  Thus

\[
 X_R^F
 \le C\left(R^2+\frac{A^2R^2}{M_m^3}\right)
 \le C(\mathcal H_{w_R}^{F,R})^{2/3}
 \le C(P_R^F)^{2/3}.
\]

This proves Proposition 6.5 uniformly over the same explicit parameter
family.  The proof uses the harmonic row to pay the kinematic quantity; it
does not cancel or estimate away the acceleration functional.  The
acceleration rows in \(P_R^F\) are finite and nonnegative for this smooth
family, so retaining them only enlarges the right-hand side.  This fact does
not license deleting them from the general Version-F gate.

## 10. Claim boundary

### Proved by the audited calculations

1. The transformation identity and both specialized transformed equations.
2. The Version-M residual-transport and Version-F acceleration signs in the
   local-energy inequalities.
3. The filtered-stress identity for \(a_R'\).
4. The impossibility of absorbing nonzero \(a_R'\) into a periodic torus
   pressure, together with the exact finite affine row for the frozen
   super-Gaussian exterior weight.
5. Automatic acceleration cancellation for the matching mollifier and only
   a nonautomatic formula at other radii or for other cutoffs.
6. The corrected closed-support statement and pointwise estimate (4.12d).
7. The distinction between cubic support bookkeeping and every retained
   shell/core acceleration moment.
8. The translated R0.74D offset and full-\(I_{2R}\) two-lobe residence.
9. Uniform Version-M and Version-F familywise neutralization for every
   admissible member of the explicit R0.74D family.

### Still open

1. The arbitrary-solution Version-M endpoint (3.11).
2. The arbitrary-solution Version-F endpoint (4.17), with all acceleration
   rows retained.
3. Any mechanism that converts the familywise calculations into a general
   absorption theorem or regularity criterion.

The audit makes no originality claim and no assertion about the later
packet-survival gates.  It proves neither global regularity nor singularity
formation.  **NOT CLAY.**

## Final verdict

For the audited SHA-256 snapshot and the literal PROVED/OPEN boundary above,
Sections 1--6 are **PASS**.  The general local-frame algebra is closed, the
latest support inequality has the correct scale and functional ownership,
and the R0.74D construction is neutralized only familywise, with no upgrade
to either open endpoint.
