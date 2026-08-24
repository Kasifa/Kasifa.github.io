# R0.70B — Matching-scale bridge, reverse obstruction, and normal-form gate

**Audit date:** 2026-08-24
**Status:** internal research report; not a public theorem chapter
**Canonical source:** this file is the source of record for the R0.70B gate

## 0. Claim protocol

The report uses four labels.

- **[P] Proved here:** a proof is included below from the displayed
  definitions.
- **[F] Source fact:** a definition or result is read from a locked primary
  source; this project has not independently re-proved the whole source.
- **[O] Obstruction:** a rigorous counterexample or no-go statement for the
  explicitly stated class only.
- **[U] Unresolved:** a step that is still unavailable and must not be used as
  a hypothesis under a new name.

Nothing in this report proves regularity or finite-time blow-up for the
three-dimensional Navier--Stokes equations.  In particular, a failure of the
bridge studied here is a route-selection result, not evidence for singularity.

## 1. Research question and outcome

R0.69T introduced signed physical-space annular production
\(\mathcal A_j\), and R0.69W gave a strict computer-assisted sign obstruction
for a declared static two-scale family.  R0.70A identified Runlong Yu's
filtered far-field reservoirs as the closest current comparison object.  The
R0.70B question is deliberately narrow:

> At matching physical scales, can the signed annular production replace one
> of the positive far-field, subgrid, or localization inputs in Yu's filtered
> vorticity budget?

The answer obtained at this gate is:

1. **[P] A forward estimate closes with exactly Yu's scale factor.**  The
   localized unsymmetrized shell work is bounded by
   \((r_k/r_j)\mathfrak A_{j,k}\mathcal Q_k\).  This recovers the scaling of
   Yu's Proposition 8.6 and gives no new small factor.
2. **[P] Localization changes the object.**  Exact pair exchange splits the
   shell work into a two-increment signed main term and a cutoff commutator of
   the same scaling degree.  The commutator cannot be discarded.
3. **[O] The forward estimate has no kinematic inverse.**  A smooth compactly
   supported divergence-free field with an affine shear core has nonzero
   filtered vorticity reservoirs and nonzero velocity-increment defect, while
   every internal matching-shell production is zero.
4. **[O] Signed integration cannot control a positive far-field budget
   without a sign defect.**  The missing quantity is exactly the difference
   between the integral of the absolute local shell density and the absolute
   value of its integral.
5. **[O] Filtered signed annuli cannot kinematically control the subgrid
   commutator.**  A high-frequency packet with a low-frequency carrier makes
   the entire filtered annular absolute sum tend to zero while the actual
   commutator forcing diverges.
6. **[O] No continuous, polynomially bounded, translation-invariant
   self-adjoint quadratic multiplier exactly generates one physical annulus
   with zero cubic remainder.**  A \(3:4:5\) helical triad gives an explicit
   symbol inconsistency, first visible at fourth order in the low-frequency
   expansion.
7. **[U] No control of the sign defect, the exterior tail, or the subgrid and
   localization budgets follows from the standard energy inequality or from
   R0.69T--W.**  Adding their summability as assumptions would restate the
   known conditional closure rather than advance it.

The direct R0.69T-to-Yu replacement route therefore stops at R0.70B.  A more
special dynamic sign-coherence mechanism would be a different theorem and
remains open.

## 2. Locked objects and index direction

### 2.1 The signed R0.69T annulus

For a smooth divergence-free velocity \(u\), write
\(\omega=\nabla\times u\), \(e_{xy}=(y-x)/|y-x|\), and

\[
 J_u(x,y)
 =\bigl(e_{xy}\cdot\omega(x)\bigr)
  \bigl(e_{xy}\cdot(\omega(y)\times\omega(x))\bigr).
 \tag{2.1}
\]

R0.69T proved the exact signed representation

\[
 \int\omega\cdot S\omega\,dx
 =\frac{3}{4\pi}\iint\frac{J_u(x,y)}{|x-y|^3}\,dy\,dx
 \tag{2.2}
\]

and its pair-symmetrized two-increment form.  A nonnegative dyadic partition
\(\psi_n\), supported at physical length \(|x-y|\simeq2^n\), defines the
signed cubic scalar \(\mathcal A_n(u)\).  For every
\(u\in C_c^\infty\),

\[
 \sum_{n\in\mathbb Z}\mathcal A_n(u)
 =\int\omega\cdot S\omega\,dx,
 \qquad
 \sum_n|\mathcal A_n(u)|<\infty.
 \tag{2.3}
\]

This is a fixed-time full-space identity.  It is not a cross-cylinder
Carleson estimate.

### 2.2 Yu's filtered reservoirs

Fix \(r_k=2^{-k}\), a relative filter length
\(\ell_k=\sigma r_k\), a parabolic time interval \(I_k\), a core cutoff
\(\chi_k\), and

\[
 U_k=\varphi_{\ell_k}*u,
 \qquad
 \Omega_k=\nabla\times U_k.
 \tag{2.4}
\]

For a fixed enlarged physical annulus \(\widetilde A_j\), the two quantities
from Definition 8.5 and the subsequent time profile in Yu v1 are

\[
 \mathfrak A_{j,k}
 =\left(
 r_j^{-1}\iint_{I_k\times\widetilde A_j}
 |\Omega_k(y,t)|^2\,dy\,dt
 \right)^{1/2},
 \qquad
 \mathfrak A_j=\sup_{k\ge j}\mathfrak A_{j,k},
 \tag{2.5}
\]

and

\[
 \mathcal Q_k
 =\left\{
 \int_{I_k}
 \left(\int\chi_k(x)|\Omega_k(x,t)|^2\,dx\right)^2dt
 \right\}^{1/2}.
 \tag{2.6}
\]

Both are nonnegative.  The first is linear and the second quadratic under
amplitude scaling, so only their product has the cubic homogeneity of an
annular production.  **[F]** Yu's Proposition 8.6 bounds the redistributed
annular far field by

\[
 \mu_k^{\mathrm{far,ann}}
 \le C\sum_{j=0}^k
 2^{-(k-j)}\mathfrak A_{j,k}\mathcal Q_k.
 \tag{2.7}
\]

The comparison below reads the preprint's definitions and statement but does
not independently certify every step of that preprint.

### 2.3 The scale labels run in opposite directions

The R0.69T index increases with physical length \(2^n\), whereas Yu's index
increases while \(r_j=2^{-j}\) decreases.  Comparable shells satisfy

\[
 n(j)=-j+O(1),
 \tag{2.8}
\]

where the bounded offset depends only on the two fixed window conventions.
Writing \(\mathcal A_j(U_k)\) with the same literal index on both sides would
therefore compare opposite scales.

## 3. The localized matching-shell decomposition

Fix one smooth, even, nonnegative profile \(\eta\), and set

\[
 \eta_j(z)=\eta(z/r_j),
 \qquad
 \sup_j\|\eta_j\|_\infty=\|\eta\|_\infty<\infty.
 \tag{3.1}
\]

Assume that it is supported where

\[
 c_0r_j\le |z|\le c_1r_j.
 \tag{3.2}
\]

After a fixed enlargement of \(\widetilde A_j\), assume that
\(x\in\operatorname{supp}\chi_k\) and
\(z\in\operatorname{supp}\eta_j\) imply
\(x+z\in\widetilde A_j\).  This is the geometric containment used below; its
constants are uniform for the separated range \(j\le k\).

Define the normalized unsymmetrized local shell work

\[
 W_{j,k}
 =r_k\frac{3}{4\pi}
 \int_{I_k}\iint
 \chi_k(x)\eta_j(y-x)
 \frac{J_{U_k}(x,y)}{|x-y|^3}\,dy\,dx\,dt.
 \tag{3.3}
\]

Put

\[
 \overline\chi_k(x,y)=\frac{\chi_k(x)+\chi_k(y)}2,
 \qquad
 \delta\chi_k(x,y)=\chi_k(y)-\chi_k(x),
 \qquad
 \delta\Omega_k=\Omega_k(y)-\Omega_k(x).
 \tag{3.4}
\]

Exact exchange of \(x\) and \(y\), as in R0.70A equation (6.7), gives

\[
 \boxed{W_{j,k}=T_{j,k}+C^\chi_{j,k},}
 \tag{3.5}
\]

where

\[
\begin{aligned}
 T_{j,k}
 ={}&r_k\frac{3}{8\pi}
 \int_{I_k}\iint\frac{\eta_j(y-x)}{|x-y|^3}
 \overline\chi_k(x,y)
 \bigl(e_{xy}\cdot\delta\Omega_k\bigr)\\
 &\hspace{38mm}\times
 \bigl(e_{xy}\cdot(\Omega_k(x)\times\delta\Omega_k)\bigr)
 \,dy\,dx\,dt,
 \tag{3.6}
\end{aligned}
\]

and

\[
\begin{aligned}
 C^\chi_{j,k}
 ={}&r_k\frac{3}{8\pi}
 \int_{I_k}\iint\frac{\eta_j(y-x)}{|x-y|^3}
 \frac{\delta\chi_k(x,y)}2
 \bigl(e_{xy}\cdot(\Omega_k(x)+\Omega_k(y))\bigr)\\
 &\hspace{38mm}\times
 \bigl(e_{xy}\cdot(\Omega_k(x)\times\delta\Omega_k)\bigr)
 \,dy\,dx\,dt.
 \tag{3.7}
\end{aligned}
\]

Thus the localized object matching the positive far-field calculation is
\(W_{j,k}\), not the full-space signed scalar.  The two-increment main term
\(T_{j,k}\) differs from it by a boundary-crossing commutator with the same
Navier--Stokes scaling.  Let \(w_{j,k}^{\eta}(x,t)\) be the local density in
(3.3), after the \(y\) integration, and let
\(w_{j,k}^{\mathrm{Yu}}(x,t)\) be the density with Yu's exact matching-shell
window and the same normalization.  Define the nonnegative window mismatch

\[
 C^{\mathrm{win}}_{j,k}
 :=\iint_{I_k\times\mathbb R^3}
 |w_{j,k}^{\mathrm{Yu}}(x,t)-w_{j,k}^{\eta}(x,t)|\,dx\,dt.
 \tag{3.8}
\]

This density-level \(L^1\) difference, rather than only the difference of two
signed scalars, is what survives after taking a positive part or absolute
value.

## 4. The forward matching-scale bridge

### Proposition 4.1 [P]

Under the containment in Section 3, there is a constant depending only on the
fixed windows such that

\[
 \boxed{
 |W_{j,k}|
 \le C\frac{r_k}{r_j}
 \mathfrak A_{j,k}\mathcal Q_k
 =C2^{-(k-j)}\mathfrak A_{j,k}\mathcal Q_k.}
 \tag{4.1}
\]

Consequently,

\[
 |T_{j,k}|
 \le C2^{-(k-j)}\mathfrak A_{j,k}\mathcal Q_k
 +|C^\chi_{j,k}|.
 \tag{4.2}
\]

For a different shell convention, add
\(C^{\mathrm{win}}_{j,k}\) to the right-hand side.

### Proof

The unsymmetrized numerator obeys

\[
 |J_{U_k}(x,y)|
 \le |\Omega_k(x)|^2|\Omega_k(y)|.
 \tag{4.3}
\]

On the support of \(\eta_j\), the kernel is bounded by
\(Cr_j^{-3}\), while the shell volume is bounded by \(Cr_j^3\).  Define

\[
 E_k(t)=\int\chi_k(x)|\Omega_k(x,t)|^2\,dx,
 \qquad
 B_{j,k}(t)
 =\left(\int_{\widetilde A_j}|\Omega_k(y,t)|^2\,dy\right)^{1/2}.
 \tag{4.4}
\]

Spatial Cauchy--Schwarz in the shell gives

\[
 |W_{j,k}|
 \le Cr_kr_j^{-3/2}
 \int_{I_k}E_k(t)B_{j,k}(t)\,dt.
 \tag{4.5}
\]

Time Cauchy--Schwarz and (2.5)--(2.6) yield

\[
 \left(\int_{I_k}E_k(t)^2dt\right)^{1/2}=\mathcal Q_k,
 \qquad
 \left(\int_{I_k}B_{j,k}(t)^2dt\right)^{1/2}
 =r_j^{1/2}\mathfrak A_{j,k}.
 \tag{4.6}
\]

Substitution gives (4.1).  Equation (4.2) follows from the exact identity
(3.5).  \(\square\)

### Interpretation

The estimate is scale-critical and rigorous, but it is not a new closure.  It
reproduces the factor in Yu's Proposition 8.6 after the objects are placed at
the same physical scale.  In particular, it points from the positive
reservoir product to signed production:

\[
 \mathfrak A_{j,k}\mathcal Q_k
 \quad\Longrightarrow\quad |W_{j,k}|,
 \tag{4.7}
\]

not in the direction needed to replace Yu's assumption by R0.69T.

## 5. A smooth affine-shear obstruction to the reverse bridge

### Construction

Let \(\Theta\in C_c^\infty(\mathbb R^3)\) equal one on a large ball and put

\[
 \Psi(x)=\frac{x_2^2}{2}\Theta(x),
 \qquad
 u=\nabla\times(0,0,\Psi).
 \tag{5.1}
\]

Then \(u\in C_c^\infty\) and \(\nabla\cdot u=0\).  In the region where
\(\Theta=1\),

\[
 u(x)=(x_2,0,0),
 \qquad
 \omega(x)=(0,0,-1).
 \tag{5.2}
\]

Choose the core, filter support, and relative shell strictly inside that
region.  A normalized even filter preserves affine functions there, so
\(U_k=u\) and \(\Omega_k=(0,0,-1)\) on every point used by the shell
integral.  Hence

\[
 \Omega_k(y)\times\Omega_k(x)=0,
 \qquad
 \delta\Omega_k=0,
 \tag{5.3}
\]

and therefore

\[
 W_{j,k}=T_{j,k}=C^\chi_{j,k}=0.
 \tag{5.4}
\]

On the other hand,

\[
 \mathfrak A_{j,k}>0,
 \qquad
 \mathcal Q_k>0,
 \tag{5.5}
\]

for every nontrivial time interval and nonzero core and shell.  The velocity
increments are also nonzero:

\[
 \delta_z u(x)=(-z_2,0,0)
 \tag{5.6}
\]

for Yu's convention \(\delta_z u(x)=u(x-z)-u(x)\).

Thus every nondegenerate smooth radial filter has a strictly positive moment
of these increments.  In particular, the derivative-compatible increment
envelope entering Yu's \(\widetilde{\mathcal S}^{(p)}\) is not forced to
vanish when the annular vorticity production vanishes.

### Corollary 5.1 [O]

There is no universal constant \(c>0\) for which

\[
 c\,2^{-(k-j)}\mathfrak A_{j,k}\mathcal Q_k
 \le |T_{j,k}|+|C^\chi_{j,k}|
 \tag{5.7}
\]

holds for all smooth compactly supported divergence-free fields at matching
internal scales.  The same construction also shows that
\(T_{j,k}=0\) does not force the derivative-compatible velocity-increment
defect to vanish.

The construction can be dilated so that the same dimensionless obstruction
occurs at any selected physical scale.  It is a kinematic family, not a
single Navier--Stokes trajectory.  Therefore it rules out a purely
kinematic reverse inequality, but it does not exclude a future estimate that
uses an additional dynamical property of Navier--Stokes solutions.

## 6. The sign defect is unavoidable

Let \(w_{j,k}(x,t):=w_{j,k}^{\eta}(x,t)\) denote the signed local density
obtained from (3.3), including its fixed normalization.  Define

\[
 D^{\mathrm{sign}}_{j,k}
 =\iint_{I_k\times\mathbb R^3}|w_{j,k}(x,t)|\,dx\,dt
  -|W_{j,k}|\ge0.
 \tag{6.1}
\]

This gives the exact bookkeeping identity

\[
 \iint|w_{j,k}|=|W_{j,k}|+D^{\mathrm{sign}}_{j,k}.
 \tag{6.2}
\]

Yu's far-field budget is nonnegative because absolute values or positive
parts are taken before the final space-time integration.  Here
\(\mu_k^{\mathrm{far,ann}}\) denotes the actual positive annular shell-work
contribution, not the reservoir majorant on the right of Yu's Proposition
8.6.  With the fixed geometric normalization absorbed into
\(C_{\mathrm{geom}}\), its definition first gives

\[
 \mu_k^{\mathrm{far,ann}}
 \le C_{\mathrm{geom}}
 \sum_{j\le k}\iint
 |w^{\mathrm{Yu}}_{j,k}(x,t)|\,dx\,dt.
 \tag{6.3}
\]

The signed scalar \(W_{j,k}\) has already discarded the local cancellation
measured by \(D^{\mathrm{sign}}_{j,k}\).  The density comparison (3.8), the
identity (6.2), and the exact decomposition (3.5) therefore imply that the
most exact bookkeeping can give is

\[
 \mu_k^{\mathrm{far,ann}}
 \lesssim
 \sum_{j\le k}\left(
 |T_{j,k}|+D^{\mathrm{sign}}_{j,k}
 +|C^\chi_{j,k}|+C^{\mathrm{win}}_{j,k}
 \right).
 \tag{6.4}
\]

Equation (6.4) is not a closure estimate until the sign and window defects on
its right are independently controlled.  Assuming their cross-scale
summability would simply rename the missing positive far-field hypothesis.

## 7. Why the subgrid and localization modules do not follow

**[F]** Yu's filtered equation contains the unresolved stress

\[
 R_k=\varphi_{\ell_k}*(u\otimes u)-U_k\otimes U_k
 \tag{7.1}
\]

and a corresponding vorticity forcing.  Theorem 9.3 in Yu v1 has the form

\[
 F_k^{\mathrm{com}}
 \le \eta P_k+C_\eta\widetilde{\mathcal S}^{(p)}_k
     +L^{\mathrm{com}}_{k,\mathrm{inc}}.
 \tag{7.2}
\]

The signed quantity \(T_{j,k}\) sees only \(U_k\) and \(\Omega_k\); it does
not determine \(R_k\), the derivative of the filter, or the localization
shell.  Its cubic homogeneity also cannot by itself control the quartic
increment defect without another amplitude-one, scale-invariant factor.

Likewise, a full-space translation-invariant annular scalar cannot see
\(\partial_t\chi_k\), \(\nabla\chi_k\), filter-transition shells, or the
exterior part not covered by \(j\le k\).  A solution-adapted adjoint cutoff
may remove a principal localization term, but it does not remove every
commutator shell budget.

Conditionally combining (6.4) with Yu's displayed budget yields at most

\[
\begin{aligned}
 \mathfrak S_k\lesssim{}&
 \sum_{j\le k}\left(
 |T_{j,k}|+D^{\mathrm{sign}}_{j,k}
 +|C^\chi_{j,k}|+C^{\mathrm{win}}_{j,k}
 \right)\\
 &+E_k^{\mathrm{ext}}
 +C\widetilde{\mathcal S}^{(p)}_k
 +L_k+L^{\mathrm{com}}_{k,\mathrm{inc}}.
 \tag{7.3}
\end{aligned}
\]

Here \(E_k^{\mathrm{ext}}\) is the outer tail not present in the finite
redistribution.  Formula (7.3) is the maximal honest ledger under the current
definitions.  It is not a new theorem if the last line and the sign defect are
assumed summable.

### 7.1 A kinematic one-scale commutator obstruction [O]

The absence of subgrid information is not only a matter of notation.  Fix a
standard cylinder \(Q_r\), a filter length
\(0<\ell=\sigma r\) with \(0<\sigma\le\rho\le1/4\), and a core cutoff with an
interior platform.  Let \(S_\ell\) denote convolution with the fixed smooth
compactly supported filter.

Choose a smooth compactly supported scalar \(\zeta\), equal to one on a
positive-measure subregion with a full \(\ell\)-buffer inside the cylinder,
such that elsewhere
\(\partial_1\partial_2(\zeta^2)\not\equiv0\), and define

\[
 w_N
 =\nabla\times\left(N^{-1}\zeta(x)e_3\sin(Nx_1)\right)
 =-\zeta e_2\cos(Nx_1)
  +N^{-1}(\partial_2\zeta,-\partial_1\zeta,0)\sin(Nx_1).
 \tag{7.4}
\]

Every \(w_N\) is smooth, compactly supported, and divergence free.  At fixed
filter length, integration by parts in the oscillatory variable gives, for
all \(M,s\),

\[
 \|S_\ell w_N\|_{C^s}=O_{M,s}(N^{-M}),
 \tag{7.5}
\]

whereas the high--high center stress has the nonzero low-frequency limit

\[
 R_\ell(w_N)
 \longrightarrow
 R^0:=\frac12S_\ell(\zeta^2e_2\otimes e_2)
 \quad\text{in }C^\infty.
 \tag{7.6}
\]

Indeed, the central term \(S_\ell w_N\otimes S_\ell w_N\) vanishes rapidly,
while \(\cos^2(Nx_1)=(1+\cos(2Nx_1))/2\).  Put

\[
 G=\nabla\times\nabla\cdot R^0
 =\frac12S_\ell
 \begin{pmatrix}
 -\partial_3\partial_2(\zeta^2)\\
 0\\
 \partial_1\partial_2(\zeta^2)
 \end{pmatrix}.
 \tag{7.7}
\]

The field \(G\) is nonzero.  Its Fourier transform is entire and the filter
transform is nonzero near the origin, so convolution cannot annihilate the
nonzero compactly supported input on an open frequency set.

Let

\[
 H=S_\ell^*G,
 \qquad K=\nabla\times H,
 \qquad v=K.
 \tag{7.8}
\]

The same Fourier-analytic argument used for \(G\) shows that
\(H=S_\ell^*G\ne0\).  Both \(G\) and \(H\) are divergence free.  Then \(v\)
is smooth, compactly supported, and divergence free.  Moreover
\(K\ne0\): otherwise the divergence-free field \(H\) would be both curl free
and compactly supported, hence harmonic and zero, contradicting \(H\ne0\).
With the core cutoff equal to one on the interaction support,

\[
 \int (S_\ell\nabla\times v)\cdot G\,dx
 =\int(\nabla\times K)\cdot H\,dx
 =\int K\cdot\nabla\times H\,dx
 =\|K\|_2^2>0.
 \tag{7.9}
\]

Now take the time-independent smooth fields

\[
 u_N=N^{-1/3}v+N^{2/3}w_N.
 \tag{7.10}
\]

The filtered velocity has only the small carrier at leading order,

\[
 S_\ell u_N=N^{-1/3}S_\ell v+O(N^{-M})
 \quad\text{in every fixed }C^s,
 \tag{7.11}
\]

so cubic homogeneity and the absolute annular estimate from R0.69T give

\[
 r\int_{I_r}\sum_q
 |\mathcal A_q(S_\ell u_N(t))|\,dt
 =O(N^{-1})\longrightarrow0.
 \tag{7.12}
\]

For the polarized center stress

\[
 C_\ell(v,w)
 =S_\ell(v\otimes w+w\otimes v)
  -S_\ell v\otimes S_\ell w-S_\ell w\otimes S_\ell v,
 \tag{7.13}
\]

the exact expansion is

\[
 R_\ell(u_N)
 =N^{-2/3}R_\ell(v)
  +N^{1/3}C_\ell(v,w_N)
  +N^{4/3}R_\ell(w_N).
 \tag{7.14}
\]

At fixed filter length, every derivative of
\(C_\ell(v,w_N)\) is in fact rapidly decaying by nonstationary integration;
uniform boundedness would already make its normalized contribution
\(N^{-1}C_\ell(v,w_N)\) vanish.

In contrast,

\[
 N^{-4/3}R_\ell(u_N)\longrightarrow R^0,
 \qquad
 \Omega_{\ell,N}
 =N^{-1/3}S_\ell(\nabla\times v)+O(N^{-M}),
 \tag{7.15}
\]

Use a product cutoff
\(\chi(x,t)=\chi_x(x)\chi_t(t)\), with \(\chi_t\ge0\) nonzero and
\(\chi_x=1\) on the supports needed in (7.9).  Yu's absolute value is outside
the whole space-time integral:

\[
 F^{\mathrm{com}}_{r,\ell}(u)
 =r\left|
 \iint_{Q_r}\chi\,\Omega_\ell\cdot
 (\nabla\times\nabla\cdot R_\ell)\,dx\,dt
 \right|.
 \tag{7.16}
\]

Equations (7.9), (7.14), and (7.15) yield

\[
 \boxed{
 F^{\mathrm{com}}_{r,\ell}(u_N)
 =cN+o(N)\longrightarrow\infty,
 \qquad
 c=r\left(\int_{I_r}\chi_t(t)\,dt\right)\|K\|_2^2>0.}
 \tag{7.17}
\]

The same sequence has the compatible magnitudes

\[
 P_{r,\ell}(u_N)\asymp N^{-2/3},
 \qquad
 \widetilde{\mathcal S}^{(2)}_{r,\ell}(u_N)\asymp N^{8/3},
 \qquad
 \bigl(P_{r,\ell}\widetilde{\mathcal S}^{(2)}_{r,\ell}\bigr)^{1/2}
 \asymp N.
 \tag{7.18}
\]

For completeness, choose the cutoff positive on the buffered
\(\zeta\equiv1\) subcylinder and on the regions where \(G\) and
\(\Omega_{\ell,v}=S_\ell(\nabla\times v)\) are used.  The
Riemann--Lebesgue lemma gives a uniform positive lower bound for the
\(\varphi_\ell\)-weighted \(L^2\) velocity increment of \(w_N\) on that
subcylinder.  Hence
\(\mathfrak M_{\ell,2}(u_N)\asymp N^{2/3}\) there and globally has the same
upper order, proving
\(\widetilde{\mathcal S}^{(2)}_{r,\ell}(u_N)\asymp N^{8/3}\).
Equation (7.15) gives the matching upper bound for \(P\).  Its lower bound is
positive because (7.9) makes \(\Omega_{\ell,v}\) nonzero, and a nonzero
compactly supported smooth field cannot have identically zero gradient.
Thus \(P_{r,\ell}(u_N)\asymp N^{-2/3}\).

Therefore no universal **kinematic** bound based only on filtered signed
annuli, even their complete absolute shell sum, can control the subfilter
commutator.  The sequence consists of admissible smooth initial states but is
not a Navier--Stokes trajectory on the whole parabolic interval.  It does not
exclude a genuinely dynamical estimate in which viscosity suppresses the
high frequencies on their \(N^{-2}\) time scale.

## 8. Translation-invariant quadratic normal form: a 3:4:5 no-go

R0.70A proposed a separate candidate

\[
 Q_m(\omega)=\frac12\langle\omega,m(D)\omega\rangle
 \tag{8.1}
\]

whose nonlinear Euler derivative would equal a single prescribed annular
production.  This section closes exact generation for a broad but still
specific class.

### Theorem 8.1 [O]

Fix \(r>0\), \(\Lambda>1\), and the nontrivial nonnegative smooth annular
window \(\eta_{r,\Lambda}\) induced by the nonincreasing profile \(\chi\) in
R0.70A.  There is no continuous,
polynomially bounded, translation-invariant, self-adjoint matrix Fourier
multiplier \(M_r(D)\), satisfying

\[
 M_r(k)^*=M_r(k),
 \qquad M_r(-k)=\overline{M_r(k)},
 \tag{8.2}
\]

such that

\[
 \left.\frac d{dt}\right|_{\mathrm{Euler\ nonlinear}}
 \frac12\langle\omega,M_r(D)\omega\rangle
 =\mathcal A_{r,\Lambda}(u)
 \tag{8.3}
\]

for every real Schwartz divergence-free datum whose Fourier support is a
compact subset of \(\mathbb R^3\setminus\{0\}\).

The theorem concerns exact generation with zero cubic remainder.  It does
not cover a spatially localized or solution-dependent operator, a
nonquadratic or time-nonlocal functional, or an identity
\(\mathcal A_{r,\Lambda}+\mathcal R_r\) with a same-order remainder.  It is a
full-space \(\mathbb R^3\) theorem, not a fixed-torus statement.  Merely
measurable or distributional multiplier symbols are also outside its scope;
they would require a separate almost-everywhere symbol argument.

### 8.1 The annular cubic symbol

Use the Fourier convention

\[
 \widehat f(k)=\int_{\mathbb R^3}e^{-ik\cdot x}f(x)\,dx,
 \qquad
 f(x)=\frac1{(2\pi)^3}\int_{\mathbb R^3}e^{ik\cdot x}\widehat f(k)\,dk.
 \tag{8.4}
\]

For a Fourier vorticity amplitude \(a\perp k\), define

\[
 U_k a=\frac{i\,k\times a}{|k|^2},
 \qquad
 S_k(a)=\frac i2\left(k\otimes U_ka+U_ka\otimes k\right).
 \tag{8.5}
\]

The unsymmetrized annular kernel is

\[
 K_{ij}^{r,\Lambda}(z)
 =\frac{3}{4\pi}\eta_{r,\Lambda}(z)
  \frac{z_i z_j}{|z|^5}.
 \tag{8.6}
\]

Radial Fourier transformation gives

\[
 \widehat K_{ij}^{r,\Lambda}(\xi)
 =\alpha_{r,\Lambda}(|\xi|)\delta_{ij}
 -G_{r,\Lambda}(|\xi|)\frac{\xi_i\xi_j}{|\xi|^2},
 \qquad
 G_{r,\Lambda}(\rho)
 =3\int_0^\infty
 \eta_{r,\Lambda}(s)j_2(\rho s)\frac{ds}{s}.
 \tag{8.7}
\]

The scalar \(\alpha\delta_{ij}\) part contracts to zero because a vector is
orthogonal to its cross product.  If \(k+p+q=0\), the completely polarized
target symbol is consequently

\[
\begin{aligned}
 \mathfrak A_G(k,p,q;a,b,c)
 ={}&2G_{r,\Lambda}(|k|)\,b\cdot S_k(a)c\\
 &+2G_{r,\Lambda}(|p|)\,c\cdot S_p(b)a\\
 &+2G_{r,\Lambda}(|q|)\,a\cdot S_q(c)b.
 \tag{8.8}
\end{aligned}
\]

Here "completely polarized" means the coefficient of the ordered amplitude
product \(abc\) in the cubic polarization, without division by \(3!\).  This
fixes the factor two in (8.8) and the normalization used below.

### 8.2 Exact scalar-multiplier inconsistency

For \(\varepsilon>0\), take the planar \(3:4:5\) interaction triad

\[
 k=\varepsilon(3,0,0),
 \qquad p=\varepsilon(0,4,0),
 \qquad q=\varepsilon(-3,-4,0).
 \tag{8.9}
\]

Use the helical polarizations

\[
\begin{aligned}
 h_\sigma(k)&=2^{-1/2}(0,1,i\sigma),\\
 h_\sigma(p)&=2^{-1/2}(-1,0,i\sigma),\\
 h_\sigma(q)&=2^{-1/2}(4/5,-3/5,i\sigma),
\end{aligned}
 \tag{8.10}
\]

and amplitudes
\(a=h_{\sigma_k}(k)\),
\(b=h_{\sigma_p}(p)\),
\(c=i h_{\sigma_q}(q)\).  Write

\[
 m_3=m_r(k),\qquad m_4=m_r(p),\qquad m_5=m_r(q),
 \qquad
 g_j=G_{r,\Lambda}(j\varepsilon),\quad j\in\{3,4,5\}.
 \tag{8.11}
\]

After removing the common nonzero factor \(\sqrt2/50\) from one oriented
complex triad, the four choices
\((---),(--+),(-+-),(-++)\) give the derivative and target coefficient
matrices

\[
 D=
 \begin{pmatrix}
 9/2&-16&25/2\\
 27/4&-32/3&-25/12\\
 -27/2&16/3&175/6\\
 9/4&-32&175/4
 \end{pmatrix},
 \qquad
 A=
 \begin{pmatrix}
 10&-15&6\\
 -15&10&-1\\
 30&5&-14\\
 5&30&-21
 \end{pmatrix}.
 \tag{8.12}
\]

Adding the conjugate orientation to make a real six-mode field doubles both
sides, so it changes no compatibility condition.  Two exact left-null vectors
of \(D\) are

\[
 v_1=(-9/5,16/5,1,0),
 \qquad
 v_2=(-16/5,9/5,0,1).
 \tag{8.13}
\]

They satisfy

\[
 v_1^TA=4(-9,16,-7),
 \qquad
 v_2^TA=6(-9,16,-7).
 \tag{8.14}
\]

Thus every scalar multiplier, even a nonradial one, would have to satisfy

\[
 \boxed{16g_4-9g_3-7g_5=0.}
 \tag{8.15}
\]

The finite-dimensional matrices in (8.12) are independently generated by
`r070b_triad_audit.py`; they are not inserted as that script's computational
input.

### 8.3 The physical annulus violates the condition

Put

\[
 w_\Lambda(x)=\chi(x/\Lambda)-\chi(x)\ge0,
 \qquad
 I_j=\int_0^\infty w_\Lambda(x)x^{j-1}\,dx.
 \tag{8.16}
\]

The window is nontrivial, so

\[
 I_4=(\Lambda^4-1)\int_0^\infty\chi(x)x^3\,dx>0.
 \tag{8.17}
\]

Since

\[
 j_2(s)=\frac{s^2}{15}-\frac{s^4}{210}+O(s^6),
 \tag{8.18}
\]

equation (8.7) gives

\[
 G_{r,\Lambda}(\rho)
 =\frac{I_2}{5}(r\rho)^2
  -\frac{I_4}{70}(r\rho)^4
  +O((r\rho)^6).
 \tag{8.19}
\]

The quadratic coefficient cancels in (8.15), but the quartic coefficient does
not:

\[
\begin{aligned}
 &16G_{r,\Lambda}(4\varepsilon)
 -9G_{r,\Lambda}(3\varepsilon)
 -7G_{r,\Lambda}(5\varepsilon)\\
 &\qquad
 =\frac{72}{5}I_4(\varepsilon r)^4
  +O((\varepsilon r)^6)>0
 \tag{8.20}
\end{aligned}
\]

for all sufficiently small \(\varepsilon r>0\).  This contradicts (8.15)
for every fixed \(r>0\).

The plane waves expose only the symbol.  Place smooth Fourier packets in
disjoint neighborhoods of \(\{\pm k,\pm p,\pm q\}\), take conjugate
amplitudes on the negative-frequency balls, and project smoothly onto the
divergence-free planes.  For sufficiently small balls the selected triad and
its conjugate are the only zero-sum combinations.  Continuity of the symbols
and a shrinking-packet limit then recover the nonzero center defect.  Hence
an identity for all real Schwartz data would imply the contradicted pointwise
symbol identity.

### 8.4 From scalar to matrix multipliers

Suppose a matrix multiplier \(M_r\) solved (8.3).  Vorticity transforms as an
axial vector under \(R\in O(3)\), and the Euler nonlinearity and radial
annular target are covariant under the full orthogonal group.  Average the
symbols

\[
 M_r^R(k)=R^TM_r(Rk)R
 \tag{8.21}
\]

against Haar measure on \(O(3)\).  Continuity and polynomial bounds justify
the average, and linearity in \(M_r\) implies that it still solves (8.3).
Full orthogonal invariance forces

\[
 \overline M_r(k)
 =a_r(|k|)P_k+b_r(|k|)\frac{k\otimes k}{|k|^2}.
 \tag{8.22}
\]

Using all of \(O(3)\), rather than only \(SO(3)\), is essential: reflections
remove the possible transverse helical term
\(ic_r(|k|)\widehat k\times\).  Only the scalar
\(a_r(|k|)P_k\) acts on divergence-free vorticity, contradicting (8.15).
This proves Theorem 8.1.

For a prescribed scale law \(r(t)\) independent of the solution amplitude,
viscosity and the moving label add quadratic terms to \(dQ_{r(t)}/dt\); they
cannot repair the cubic Euler-symbol inconsistency.
If a scalar-multiplier remainder is permitted, its projection onto the two
left-null combinations in (8.13) must carry the nonzero
\(O((\varepsilon r)^4)\) defect in (8.20).  For a general matrix multiplier,
the same statement applies to the \(O(3)\)-averaged remainder.  In particular,
an averaged remainder that is little-o of this obstruction on the tested
low-frequency triads is impossible.

## 9. Claim--source ledger

| Claim used in this report | Primary evidence | Confidence and boundary |
|---|---|---|
| Exact signed Biot--Savart and two-increment annular identities | Local R0.69T proof in `physical_space_annular_increment_note.md` | High; independently derived in this project for smooth compactly supported data |
| Weighted pair exchange produces a same-scale cutoff commutator | Local R0.70A equation (6.7) in `r070a_moving_annular_balance_note.md` | High; direct algebra |
| Forward matching-scale bridge and affine-shear inverse obstruction | Sections 4--5 of this report | High; direct Cauchy--Schwarz proof and explicit smooth construction |
| Filtered annular sum cannot kinematically control the subgrid commutator | Section 7.1 of this report | High for fixed-filter smooth test fields; it is not a parabolic-time NSE counterexample |
| No continuous, polynomially bounded, translation-invariant self-adjoint quadratic multiplier exactly generates one annulus with zero cubic remainder | Section 8 and `certificates/r070b/` | High after two independent coefficient recalculations; analytic wave-packet and group-averaging arguments remain human proofs |
| Definitions of \(\mathfrak A_{j,k}\), \(\mathcal Q_k\), Proposition 8.6, and the conditional defect budget | [Yu, arXiv:2606.27560v1](https://arxiv.org/html/2606.27560v1) | High for textual attribution; the preprint's full proof is not independently re-certified here |
| Smooth coarse-graining separates resolved quantities from subgrid stress and uses exact increment identities | [Eyink--Aluie, arXiv:0909.2386v1](https://arxiv.org/html/0909.2386v1) | High for the general coarse-graining framework; not used as proof of Proposition 4.1 |
| Exact two-point equations depend on the chosen averaging/localization operation | [Hill, JFM 468 (2002)](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/exact-secondorder-structurefunction-relationships/C48D3847FDAE125F92032A412AB674A7) | Medium-high; used only as historical/methodological boundary |
| A neighboring 2026 route requires a critical concentration profile and logarithmic BMO direction control | [Grujić, arXiv:2607.08866v2](https://arxiv.org/html/2607.08866v2) | High for attribution; not independently re-proved and not used in the bridge proof |

## 10. Proof-gap matrix and route decision

| Desired arrow | Status | Exact missing item | Decision |
|---|---|---|---|
| \(\mathfrak A_{j,k}\mathcal Q_k\to W_{j,k}\) | **[P] closed** | none beyond fixed window containment | Keep as a comparison lemma; it reproduces known scaling |
| \(T_{j,k}\to\mathfrak A_{j,k}\mathcal Q_k\) | **[O] false kinematically** | correlation/nondegeneracy | Stop the unconditional inverse route |
| signed \(T\to\) positive far-field budget | **[U]** | \(D^{\mathrm{sign}}\), cutoff/window defects, outer tail | Continue only if NSE dynamics controls one defect without assuming it |
| filtered signed annuli \(\to F^{\mathrm{com}}\) or \(\widetilde{\mathcal S}^{(p)}\) | **[O] false kinematically** | unresolved high--high stress invisible after filtering | Stop every purely kinematic single-observable arrow; an NSE-time estimate remains a different open question |
| \(T\to\) localization budget | **[U]** | cutoff derivatives, transition shells, exterior tail | Do not rename these terms as a remainder assumption |
| continuous, polynomially bounded, translation-invariant self-adjoint quadratic normal form \(Q_M\) | **[O] exact generation impossible with zero cubic remainder** | explicit 3:4:5 fourth-order symbol defect | Stop this zero-remainder class; any continuation must expose and control a same-order remainder |

The meaningful R0.70B contribution is therefore a **falsifiable route
elimination**: after exact scale matching, the signed observable is downstream
of the positive reservoir estimate, not a replacement for it.  The result
does not reduce the hypotheses of a regularity theorem and does not advance a
Millennium-problem claim.  It does prevent future work from spending large
compute on a bridge that fails before numerical resolution becomes relevant.

## 11. Compute and publication decision

- **DGX:** not justified.  The active gates are exact algebra and small
  rational-symbol checks; additional GPU sampling cannot control the missing
  sign or subgrid defects.
- **Public site:** do not publish this revision.  Publication requires the
  historical novelty search for the exact multiplier no-go and a separate
  manuscript-style proof pass; the present result remains an internal route
  gate even though its arithmetic is archived.
- **Next admissible step:** test whether the two surviving genuinely dynamic
  possibilities have content: an NSE estimate for the sign defect, or an
  explicit same-order normal-form remainder whose 3:4:5 obstruction can be
  controlled.  If both reduce to known conditional inputs, leave the annular
  route and return to the broader route tree.
