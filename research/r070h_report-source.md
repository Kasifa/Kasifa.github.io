# R0.70H — Core-moment variation: the fixed-time gain and the parabolic duality gap

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70H
**Date:** 2026-08-24
**Scope:** fixed-center filtered zeroth and first vorticity moments, critical
normalization, scale and cylinder variation, and the exact point at which the
R0.70G source square function still fails to close the nonlinear pairing

---

## 1. Result in one page

R0.70G left one precise question. The adjacent physical-source jets have a
dissipation-level square function, but their nonlinear work needs a dual
estimate for the changing core moments. R0.70H derives the exact core-side
identities and finds a mixed answer.

There is a genuine positive estimate. At one time, on one fixed-center
geometric chain, let

\[
 M_k^{(0)}=\int\chi_k\Omega_k\otimes\Omega_k\,dx,
 \qquad
 M_k^{(1)}=\int\chi_k(x-x_0)\otimes
                    \Omega_k\otimes\Omega_k\,dx .
 \tag{1.1}
\]

The work-critical instantaneous moments are

\[
 \boxed{
 m_k^{(0)}=r_kM_k^{(0)},\qquad
 m_k^{(1)}=M_k^{(1)}.}
 \tag{1.2}
\]

Under the explicit filter square-function assumption in Section 5,

\[
 \boxed{
 \sum_k|m_{k+1}^{(n)}-m_k^{(n)}|
 \lesssim r_0\|\omega\|_2^2,
 \qquad n=0,1.}
 \tag{1.3}
\]

The same estimate holds, up to a constant, for the **instantaneous**
pairing-covariant moment increment. For Leray solutions, integration over one
common time interval gives the diagnostic bound

\[
 \int_I\sum_k|\mathfrak D_k^{\rm pair}m^{(n)}(t)|\,dt
 \lesssim \frac{r_0E_0}{\nu}.
 \tag{1.4}
\]

Equation (1.4) is an $L_t^1(\ell_k^1)$ estimate for an unweighted
instantaneous coordinate. It is not the coordinate in the R0.70F spacetime
work. The latter contains the additional factor $r_k^{-2}$:

\[
 \mathcal N_k^{(n)}(t)=r_k^{-2}\mathbf1_{I_k}(t)m_k^{(n)}(t).
 \tag{1.4a}
\]

After critical Abel summation, the source square function would require a
bound of the form

\[
 \int\sum_k r_k
 \left|\mathcal N_k^{(n)}-\rho^{n+2}\mathcal N_{k+1}^{(n)}\right|^2dt.
 \tag{1.4b}
\]

Thus the gap is stronger than one missing time exponent: it also contains a
critical $r_k^{-2}$ amplification, which becomes an $r_k^{-3}$ weight after
the direct source--core Cauchy--Schwarz pairing. R0.70H obtains neither
(1.4b) nor an equivalent direct trilinear embedding from Leray energy and
dissipation; no universal impossibility statement is asserted.

There is also an exact algebraic correction. If

\[
 h_k^{(n)}=c_k^{(n)}-
 \left(\frac{r_k}{r_{k-1}}\right)^{n+2}c_{k-1}^{(n)},
 \tag{1.5}
\]

then the dual increment in the Abel identity is not the ordinary core
difference. On a constant-ratio grid it is

\[
 \boxed{
 \mathfrak D_k^{\rm pair}m^{(n)}
 =m_k^{(n)}-\rho^{n+2}m_{k+1}^{(n)}.}
 \tag{1.6}
\]

Thus, for the instantaneous normalized work, a constant core baseline has
zero ordinary variation but contributes
$(1-\rho^{n+2})m$ at every scale. The R0.70F compact initial-face family
realizes this mechanism with uniformly bounded velocity energy: its ordinary
critical-moment variation is bounded, while the pairing-covariant $\ell^1$
and square masses grow linearly in the number of active scales. This is an
initial-face statement, not a claim about the spacetime coordinate (1.4a).
The family has no uniform instantaneous enstrophy bound, and no
common-positive-terminal-time persistence statement has been proved.

Finally, differentiating the filtered core moment in time exactly reproduces
the resolved vortex-stretching work:

\[
 \frac12\frac d{dt}\int\phi|\Omega|^2
 =\cdots+\int\phi\,S(U):\Omega\otimes\Omega+\cdots .
 \tag{1.7}
\]

Consequently, a total-time-variation estimate obtained by taking absolute
values in the moment evolution equation is circular unless the stretching
term is controlled by an independent mechanism.

The R0.70H conclusion is therefore narrow but useful:

> **Unweighted fixed-time scale variation is not the missing bridge. It has a
> valid $\ell_k^1$ estimate, and its common-time integral has an
> $L_t^1\ell_k^1$ estimate. The actual spacetime work carries an additional
> $r_k^{-2}$ factor. The surviving problem is a weighted parabolic
> source--core embedding, not ordinary moment variation.**

Nothing in this report proves global regularity, produces a singularity, or
solves the Millennium problem.

## 2. Fixed conventions and the work-critical moment

Fix a center $x_0$ and a finite chain $0\le k\le N$, or a one-sided
fine-scale chain $k=0,1,2,\ldots$, with

\[
 r_{k+1}=\rho_kr_k,
 \qquad 0<\rho_-\le\rho_k\le\rho_+<1,
 \tag{2.1}
\]

and filter scales $\ell_k=\sigma r_k$. Let

\[
 U_k=\varphi_{\ell_k}*u,
 \qquad
 \Omega_k=\varphi_{\ell_k}*\omega,
 \qquad
 \chi_k(x)=\chi\!\left(\frac{x-x_0}{r_k}\right),
 \tag{2.2}
\]

where $\varphi$ is a smooth unit-mass filter and $\chi$ is a fixed smooth
compact cutoff. The tensor $(x-x_0)^{\otimes n}$ is placed before the two
vorticity indices; only $n=0,1$ is used below:

\[
 M_k^{(n)}(t)
 =\int\chi_k(x)(x-x_0)^{\otimes n}\otimes
       \Omega_k(x,t)\otimes\Omega_k(x,t)\,dx .
 \tag{2.3}
\]

This is a single reindexed source--core scale chain, the smallest setting in
which the R0.70G adjacent-source proposal can be tested. It is not an
identification with the complete two-index moving-shell positive packing.

Under the Navier--Stokes scaling, $M_k^{(n)}$ has length dimension
$n-1$. A degree-$n$ strain jet has dimension $-(n+2)$. Therefore

\[
 c_k^{(n)}=r_k^{n+2}P_k^{(n)},
 \qquad
 m_k^{(n)}=r_k^{1-n}M_k^{(n)}
 \tag{2.4}
\]

are the two scale-invariant coordinates satisfying

\[
 r_k^3P_k^{(n)}:M_k^{(n)}
 =c_k^{(n)}:m_k^{(n)}.
 \tag{2.5}
\]

For the spacetime work used in R0.70F, the exact identity is

\[
 r_k\int_{I_k}P_k^{(n)}:M_k^{(n)}\,dt
 =r_k^{-2}\int_{I_k}c_k^{(n)}(t):m_k^{(n)}(t)\,dt.
 \tag{2.6}
\]

The auxiliary parabolic moment average is

\[
 \boxed{
 \bar m_k^{(n)}
 =r_k^{-(n+1)}\int_{I_k}M_k^{(n)}(t)\,dt
 =r_k^{-2}\int_{I_k}m_k^{(n)}(t)\,dt.}
 \tag{2.7}
\]

Only when $c_k^{(n)}(t)$ is constant on $I_k$ may (2.6) be factored as
$c_k^{(n)}:\bar m_k^{(n)}$. No such time constancy is assumed in the
Navier--Stokes problem. This distinction is the source of the $r_k^{-2}$
weight in Sections 6--7.

Two other normalizations must not be confused with (2.4):

- $r_k^{-3/2}M_k^{(0)}$ and $r_k^{-5/2}M_k^{(1)}$ are the
  unweighted coordinates dual to the particular source square function in
  R0.70G, Section 7;
- $m_k^{(0)}=r_kM_k^{(0)}$ and $m_k^{(1)}=M_k^{(1)}$ are the
  scale-invariant moments paired by the normalized physical work.

The distinction is essential. Neither coordinate may be substituted for the
other without carrying its scale weight.

## 3. Critical Abel identity and two different covariances

Let

\[
 h_k^{(n)}
 =c_k^{(n)}-\lambda_k^{(n)}c_{k-1}^{(n)},
 \qquad
 \lambda_k^{(n)}=\rho_{k-1}^{n+2}
 =\left(\frac{r_k}{r_{k-1}}\right)^{n+2}.
 \tag{3.1}
\]

For arbitrary finite tensor sequences, componentwise summation gives

\[
 \boxed{
 \begin{aligned}
 \sum_{k=a}^b h_k^{(n)}:m_k^{(n)}
 ={}&c_b^{(n)}:m_b^{(n)}
 -\lambda_a^{(n)}c_{a-1}^{(n)}:m_a^{(n)}\\
 &+\sum_{k=a}^{b-1}c_k^{(n)}:
 \left(m_k^{(n)}-\lambda_{k+1}^{(n)}m_{k+1}^{(n)}\right).
 \end{aligned}}
 \tag{3.2}
\]

The interior term defines the **pairing-covariant increment**

\[
 \mathfrak D_k^{\rm pair}m^{(n)}
 :=m_k^{(n)}-\rho_k^{n+2}m_{k+1}^{(n)}.
 \tag{3.3}
\]

The scale-difference ledger in Section 4 has another natural covariance:

\[
 \mathfrak D_k^{\rm geom}m^{(n)}
 :=m_{k+1}^{(n)}-\rho_k^{1-n}m_k^{(n)}.
 \tag{3.4}
\]

Equation (3.4) removes the change in the moment normalization itself. Equation
(3.3) is dual to the source-jet transport. Their factors are different:

\[
 \begin{array}{c|c|c}
 n&\text{geometric factor}&\text{pairing factor}\\ \hline
 0&\rho&\rho^2\\
 1&1&\rho^3.
 \end{array}
 \tag{3.5}
\]

Calling both objects a covariant difference without the factor would conceal
the main defect. In particular,

\[
 \mathfrak D_k^{\rm pair}m
 =(m_k-m_{k+1})+(1-\rho_k^{n+2})m_{k+1}.
 \tag{3.6}
\]

Ordinary variation controls the first term but not the mean mode in the
second. This is the core-side version of the critical dilation defect found
on the source side in R0.70G. Equations (3.2)--(3.6) concern the
instantaneous $r_k^3P_k:M_k$ normalization. Section 6 applies the same Abel
identity to the differently weighted spacetime coordinate.

## 4. Exact adjacent-scale moment ledger

Put

\[
 D_k=\Omega_{k+1}-\Omega_k,
 \qquad
 Q_k=\Omega_k\otimes\Omega_k,
 \qquad
 y=x-x_0.
 \tag{4.1}
\]

The exact polarization identities

\[
 Q_{k+1}-Q_k
 =D_k\otimes\Omega_{k+1}+\Omega_k\otimes D_k
 \tag{4.2}
\]

and

\[
 Q_{k+1}-Q_k
 =D_k\otimes\Omega_k+\Omega_k\otimes D_k+D_k\otimes D_k
 \tag{4.3}
\]

are interchangeable. Direct substitution into (2.4) gives

\[
 \boxed{
 \begin{aligned}
 m_{k+1}^{(n)}-m_k^{(n)}
 ={}&(\rho_k^{1-n}-1)m_k^{(n)}\\
 &+\rho_k^{1-n}r_k^{1-n}
   \int(\chi_{k+1}-\chi_k)y^{\otimes n}\otimes Q_k\,dx\\
 &+\rho_k^{1-n}r_k^{1-n}
   \int\chi_{k+1}y^{\otimes n}\otimes
        (Q_{k+1}-Q_k)\,dx .
 \end{aligned}}
 \tag{4.4}
\]

The three lines are respectively:

1. normalization dilation;
2. physical cutoff-shell variation;
3. filter-field variation.

For $n=0$, the first line is $(\rho_k-1)m_k^{(0)}$. For $n=1$
it vanishes. A moving center would add a cutoff-translation term and, for the
first moment, a center-displacement tensor. R0.70H fixes $x_0$ and makes no
claim for a moving chain.

## 5. A positive fixed-time variation estimate

Assume the filter family satisfies

\[
 C_\varphi
 :=\sup_{\xi\ne0}\sum_k
 \left|\widehat\varphi(\ell_{k+1}\xi)
       -\widehat\varphi(\ell_k\xi)\right|^2<\infty.
 \tag{5.1}
\]

This is the precise input needed below. Standard smooth low-pass filters on a
fixed geometric grid have this multiplier square-function property. By
Plancherel,

\[
 \sum_k\|D_k\|_2^2\le C_\varphi\|\omega\|_2^2,
 \qquad
 \sup_k\|\Omega_k\|_2\lesssim\|\omega\|_2.
 \tag{5.2}
\]

On the cutoff support,

\[
 r_k^{1-n}|y|^n\lesssim r_k,
 \qquad n=0,1.
 \tag{5.3}
\]

The normalization and cutoff terms in (4.4) therefore have total size

\[
 \sum_k r_k\|\omega\|_2^2
 \lesssim r_0\|\omega\|_2^2.
 \tag{5.4}
\]

For the filter term, (4.2), Cauchy--Schwarz, and (5.2) give

\[
 \begin{aligned}
 \sum_kr_k\|D_k\|_2
       (\|\Omega_{k+1}\|_2+\|\Omega_k\|_2)
 &\lesssim
 \|\omega\|_2
 \left(\sum_kr_k^2\right)^{1/2}
 \left(\sum_k\|D_k\|_2^2\right)^{1/2}\\
 &\lesssim r_0\|\omega\|_2^2.
 \end{aligned}
 \tag{5.5}
\]

Combining (4.4)--(5.5) proves

\[
 \boxed{
 \sum_k|m_{k+1}^{(n)}-m_k^{(n)}|
 +\sum_k|m_k^{(n)}|
 \lesssim r_0\|\omega\|_2^2,
 \quad n=0,1.}
 \tag{5.6}
\]

The second sum uses the elementary bound
$|m_k^{(n)}|\lesssim r_k\|\omega\|_2^2$. Equation (3.6) then yields

\[
 \boxed{
 \sum_k|\mathfrak D_k^{\rm pair}m^{(n)}|
 \lesssim r_0\|\omega\|_2^2.}
 \tag{5.7}
\]

For Leray solutions, $\omega\in L_t^2L_x^2$ and

\[
 \int_I\|\omega(t)\|_2^2dt\lesssim E_0/\nu.
 \tag{5.8}
\]

Thus (1.4) follows for almost every time slice and then by integration. This
is a real positive result, but its norm must be recorded exactly:

\[
 \mathfrak D^{\rm pair}m
 \in L_t^1(\ell_k^1),
 \tag{5.9}
\]

not $L_t^2(\ell_k^2)$.

## 6. Nested time windows and the missing $r_k^{-2}$ coordinate

Let

\[
 I_k=(t_0-r_k^2,t_0),
 \qquad I_{k+1}\subset I_k,
 \tag{6.1}
\]

and define the parabolically averaged critical moment by (2.7). Its ordinary
difference has the exact ledger

\[
 \boxed{
 \begin{aligned}
 \bar m_{k+1}-\bar m_k
 ={}&r_{k+1}^{-2}\int_{I_{k+1}}
       (m_{k+1}-m_k)\,dt\\
 &+(r_{k+1}^{-2}-r_k^{-2})
       \int_{I_{k+1}}m_k\,dt\\
 &-r_k^{-2}\int_{I_k\setminus I_{k+1}}m_k\,dt .
 \end{aligned}}
 \tag{6.2}
\]

The lines are the filter/cutoff change on the fine window, the averaging
dilation, and the discarded coarse time slab. A time-constant, scale-constant
moment makes the last two lines cancel, as they must.

For the actual work it is essential not to factor the time-dependent source
coefficient out of the integral. Put

\[
 \mathcal N_k^{(n)}(t)
 =r_k^{-2}\mathbf 1_{I_k}(t)m_k^{(n)}(t).
 \tag{6.3}
\]

The exact spacetime pairing increment becomes

\[
 \boxed{
 \begin{aligned}
 \mathfrak D_k^{\rm st}\mathcal N^{(n)}
 :={}&\mathcal N_k^{(n)}
       -\lambda_{k+1}^{(n)}\mathcal N_{k+1}^{(n)}\\
 ={}&r_k^{-2}\mathbf1_{I_{k+1}}
       \left(m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}\right)\\
 &+r_k^{-2}\mathbf1_{I_k\setminus I_{k+1}}m_k^{(n)}.
 \end{aligned}
 }
 \tag{6.4}
\]

The overlap factor is $1$ for $n=0$ and $\rho_k$ for $n=1$. These are not
the instantaneous pairing factors $\rho_k^2$ and $\rho_k^3$ from Section 3;
the difference is exactly the $r_{k+1}^{-2}/r_k^{-2}$ time-normalization
ratio. Equations (5.6)--(5.8) control only the unweighted moments. They do not
control (6.4), even in $L_t^1\ell_k^1$, because every term now carries
$r_k^{-2}$.

The normalized average itself satisfies

\[
 |\bar m_k^{(n)}|
 \lesssim r_k^{-1}
 \int_{I_k}\int_{B_{Cr_k}(x_0)}|\omega|^2\,dx\,dt,
 \qquad n=0,1,
 \tag{6.5}
\]

up to a fixed enlargement caused by a compact filter. The right side is a
local enstrophy density. Its uniform control is a parabolic Carleson or
critical Morrey condition. Global dissipation controls the numerator summed
over all space and time; it does not imply the normalized fixed-center
supremum in (6.5).

This last statement is a norm comparison, not an NSE counterexample. A
nonnegative $L^1$ density of fixed total mass can be concentrated in an
arbitrarily small parabolic cylinder, making $r^{-1}\mu(Q_r)$ arbitrarily
large. R0.70H does not realize that abstract concentration as one common-top
Navier--Stokes solution.

## 7. Why the source square function still does not pair

R0.70G gives a weighted estimate for the adjacent source coordinate $h$.
On a constant-ratio grid, with the same zero coarse extension or an explicit
coarse endpoint term, the backward shift has norm $\rho^{-1/2}$ in
$\ell^2(r_k^{-1})$, while the transport factor is $\rho^{n+2}$. Since
$\rho^{n+3/2}<1$, a Neumann series gives the same weighted estimate for the
cumulative coordinate $c$. Thus, for one fixed source/filter family,

\[
 \int_I\sum_k r_k^{-1}|c_k^{(n)}(t)|^2dt
 \lesssim\int_I\|\omega(t)\|_2^2dt,
 \tag{7.1}
\]

with the fixed-source/filter boundary stated there. With $h_k$ denoting the
normalized adjacent source coefficient, the spacetime work is

\[
 \sum_k r_k\int_{I_k}J_k^{(n)}:M_k^{(n)}dt
 =\int_I\sum_k h_k^{(n)}:\mathcal N_k^{(n)}dt.
 \tag{7.1a}
\]

Critical Abel summation reduces its signed interior part to

\[
 \int_I\sum_k c_k^{(n)}:
      \mathfrak D_k^{\rm st}\mathcal N^{(n)}\,dt.
 \tag{7.2}
\]

The direct Cauchy--Schwarz partner of (7.1) is

\[
 \int_I\sum_k r_k
 \left|\mathfrak D_k^{\rm st}\mathcal N^{(n)}\right|^2dt.
 \tag{7.3}
\]

Because the two indicator regions in (6.4) are disjoint, (7.3) is exactly

\[
 \begin{aligned}
 \int_I\sum_k r_k^{-3}\bigg[
 &\mathbf1_{I_{k+1}}
  \left|m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}\right|^2\\
 &+\mathbf1_{I_k\setminus I_{k+1}}|m_k^{(n)}|^2
 \bigg]dt.
 \end{aligned}
 \tag{7.3a}
\]

No bound for (7.3a) has been proved. The unweighted fixed-time estimate
(5.7) does not address the negative weight $r_k^{-3}$. Even after suppressing
that weight, squaring the fixed-time quadratic estimate leads naturally to
$\|\omega\|_2^4$, hence to an $L_t^4L_x^2$ requirement.

The alternative $\ell^1$ pairing uses

\[
 \sup_k|c_k(t)|
 \lesssim r_0^{1/2}
 \left(\sum_kr_k^{-1}|c_k(t)|^2\right)^{1/2}.
 \tag{7.4}
\]

It would still require
$\int\sum_k|\mathfrak D_k^{\rm st}\mathcal N|dt$. The available estimate
(5.7) omits $r_k^{-2}$, so this route is not closed. If that scale weight is
formally discarded, the remaining product already produces a cubic time
integrand comparable to $\|\omega(t)\|_2^3$; Leray dissipation supplies only
its square.

Thus the failure is not that no moment variation exists. It is a precise
duality mismatch:

\[
 \boxed{
 \text{source: }L_t^2\ell_k^2(r_k^{-1}),
 \qquad
 \text{required core: }L_t^2\ell_k^2(r_k),
 \quad \mathcal N_k=r_k^{-2}\mathbf1_{I_k}m_k.}
 \tag{7.5}
\]

Taking a positive part or absolute values also removes the signed cancellation
that produced (3.2). Moreover, if the source filter itself changes with the
core index, (7.1) cannot simply be reused; the fixed-family boundary from
R0.70G remains in force. The mismatch above is present even after granting the
more favorable fixed-family source estimate.

## 8. Filtered moment evolution and temporal circularity

For a smooth solution and a smooth spatial filter, set

\[
 \tau_{ai}^{u\omega}
 =(u_a\omega_i)_\ell-U_a\Omega_i,
 \qquad
 \tau_{ai}^{\omega u}
 =(\omega_a u_i)_\ell-\Omega_aU_i,
 \tag{8.1}
\]

and

\[
 C_{ai}=\tau_{ai}^{\omega u}-\tau_{ai}^{u\omega}.
 \tag{8.2}
\]

The exact filtered vorticity equation is

\[
 \partial_t\Omega_i+U_a\partial_a\Omega_i
 =\Omega_a\partial_aU_i+\nu\Delta\Omega_i
  +\partial_aC_{ai}.
 \tag{8.3}
\]

For a smooth scalar weight $\phi(x,t)$, integration by parts gives the tensor
moment identity

\[
 \boxed{
 \begin{aligned}
 \frac d{dt}\int\phi\Omega_i\Omega_j
 ={}&\int(\partial_t\phi+U\cdot\nabla\phi+\nu\Delta\phi)
       \Omega_i\Omega_j\\
 &+\int\phi\left[(\Omega\cdot\nabla U)_i\Omega_j
                  +\Omega_i(\Omega\cdot\nabla U)_j\right]\\
 &-2\nu\int\phi\,\partial_a\Omega_i\partial_a\Omega_j\\
 &-\int\left[C_{ai}\partial_a(\phi\Omega_j)
       +C_{aj}\partial_a(\phi\Omega_i)\right].
 \end{aligned}}
 \tag{8.4}
\]

Taking the trace yields

\[
 \boxed{
 \begin{aligned}
 \frac12\frac d{dt}\int\phi|\Omega|^2
 ={}&\frac12\int
   (\partial_t\phi+U\cdot\nabla\phi+\nu\Delta\phi)|\Omega|^2\\
 &+\int\phi\,S(U):\Omega\otimes\Omega
 -\nu\int\phi|\nabla\Omega|^2\\
 &-\int C_{ai}\partial_a(\phi\Omega_i).
 \end{aligned}}
 \tag{8.5}
\]

The far-annular strain under study is a component of $S(U)$. Therefore an
absolute time-variation estimate obtained from (8.5) already contains the
target vortex-stretching term, together with local strain, diffusion, cutoff
flux, and the subfilter commutator. Without a separate sign or cancellation
mechanism, this is a circular estimate rather than a new input.

For a first moment, take $\phi=y_\ell\chi$. Then

\[
 (\partial_t+U\cdot\nabla+\nu\Delta)(y_\ell\chi)
 =y_\ell(\partial_t+U\cdot\nabla+\nu\Delta)\chi
  +\chi U_\ell+2\nu\partial_\ell\chi,
 \tag{8.6}
\]

while the stretching line in (8.4) remains. The first moment has no hidden
temporal cancellation.

Equations (8.3)--(8.6) are asserted for smooth filtered solutions. Extending
every tensor identity to a minimal Leray formulation requires the usual
mollification and limiting justification and is not needed for the negative
integrability diagnosis here.

## 9. Exact R0.70F pressure test in the corrected coordinates

Return to the compact interlaced initial-face family from R0.70F, with fixed
center $x_0=0$. Its active target scales satisfy

\[
 \rho=\frac{r_{n+1}}{r_n}=\Lambda^{-2},
 \qquad
 q=\rho^2=\Lambda^{-4},
 \qquad
 b_n=\frac{1-q^n}{1-q}.
 \tag{9.1}
\]

With

\[
 C_0=c_\chi\eta^3,
 \qquad
 C_1=c\,c_\chi\eta^3,
 \qquad
 E=e_1^{\otimes2},
 \qquad
 T=e_1^{\otimes3},
 \tag{9.2}
\]

the raw moments are

\[
 M_n^{(0)}=C_0r_n^{-1}b_n^2E,
 \qquad
 M_n^{(1)}=C_1b_n^2T.
 \tag{9.3}
\]

Hence the corrected work-critical moments are

\[
 \boxed{
 m_n^{(0)}=C_0b_n^2E,
 \qquad
 m_n^{(1)}=C_1b_n^2T.}
 \tag{9.4}
\]

Their ordinary total variation telescopes:

\[
 \sum_{n=1}^{N-1}|m_{n+1}^{(s)}-m_n^{(s)}|
 =C_s(b_N^2-1)
 \le C_s\left((1-q)^{-2}-1\right),
 \quad s=0,1.
 \tag{9.5}
\]

The ordinary square variation is also uniformly bounded. Indeed,

\[
 b_{n+1}^2-b_n^2
 =\frac{2q^n-(1+q)q^{2n}}{1-q},
 \tag{9.6}
\]

so its squared sum is a finite combination of geometric series in
$q^2,q^3,q^4$.

For the instantaneous normalized pairing $r_n^3P_n:M_n=c_n:m_n$, the
pairing factors are

\[
 \lambda_0=\rho^2=q,
 \qquad
 \lambda_1=\rho^3=\Lambda^{-6}.
 \tag{9.7}
\]

For either degree,

\[
 b_n^2-\lambda_sb_{n+1}^2
 \ge1-\frac{\lambda_s}{(1-q)^2}>0
 \qquad(\Lambda\ge2).
 \tag{9.8}
\]

Therefore

\[
 \sum_{n=1}^{N-1}
 |\mathfrak D_n^{\rm pair}m^{(s)}|
 \ge C_s(N-1)
 \left(1-\frac{\lambda_s}{(1-q)^2}\right),
 \tag{9.9}
\]

and

\[
 \sum_{n=1}^{N-1}
 |\mathfrak D_n^{\rm pair}m^{(s)}|^2
 \ge C_s^2(N-1)
 \left(1-\frac{\lambda_s}{(1-q)^2}\right)^2.
 \tag{9.10}
\]

Thus ordinary variation is bounded while the pairing-covariant variation and
square mass are linear. This is exactly the baseline term in (3.6).

The velocity energy of the compact family remains uniformly bounded because
its profile energies carry the geometric weights $R_n+r_n$. However, the
instantaneous vorticity $L^2$ norm at the initial face is not uniformly
bounded. Equations (9.9)--(9.10) therefore exclude an estimate based only on
uniform initial velocity energy at that face; they do not contradict the
dissipation-integrated bound (1.4).

The original positive works remain

\[
 w_n^{(0)}=c_\chi\eta^3\Lambda^{-2}b_n^2,
 \qquad
 w_n^{(1)}=6c\,c_\chi\eta^3\Lambda^{-3}b_n^2,
 \tag{9.11}
\]

and sum linearly. The critical Abel identity explains rather than cancels
that recurrence: the missing ordinary baseline reappears in
$\mathfrak D^{\rm pair}m$. These factors are not the fine-window factors in
the spacetime coordinate (6.4).

This remains an initial-face result. It is not a counterexample on nested
backward cylinders with one common positive terminal time.

## 10. Conditional stronger estimates

The field-difference part of (4.4) is quadratic. A transparent local
concentration parameter is

\[
 \mathcal A(t)
 =\sup_k r_k
 \|\Omega_k(t)\|_{L^2(B_{Cr_k}(x_0))}^2.
 \tag{10.1}
\]

An essential bound on $\mathcal A(t)$, or the weaker integrability

\[
 \int_I\mathcal A(t)\|\omega(t)\|_2^2dt<\infty,
 \tag{10.2}
\]

would permit square estimates for unweighted parts of the core difference.
Such a bound is an additional fixed-center critical Morrey-type input, not a
consequence recorded by the Leray energy inequality. A corresponding uniform
spacetime version would be Carleson-type. Neither formulation automatically
absorbs the $r_k^{-3}$ weight in (7.3a).

There is also a frequency-localized positive route. Bilinear
Littlewood--Paley variational estimates control paraproduct block increments
in an $L_x^1(\ell^2)$ norm. For a fixed cutoff, an explicit Bony/LP
decomposition can use this to control a signed
frequency-paraproduct component of the quadratic filter difference. It does
not by itself control:

- the physical cutoff-shell term in (4.4);
- the normalization baseline in (3.6);
- the nested time-window term in (6.4);
- the negative scale weight in (7.3a);
- the low--low or diagonal quadratic pieces unless separately decomposed;
- the positive part of the nonlinear work;
- the missing $L_t^2$ integrability.

These are possible inputs for a refined route, not conclusions of R0.70H.

## 11. Bounded primary-literature audit

The search stopped after eight primary sources covering the five closest
frameworks: local energy, physical-scale flux, tent/Carleson control, linear
variation, and bilinear paraproduct variation.

| primary source | exact object | why it does not supply the target |
|---|---|---|
| [Caffarelli--Kohn--Nirenberg, 1982, Section 2](https://doi.org/10.1002/cpa.3160350604) | suitable weak solutions and the localized velocity-energy inequality | controls velocity energy and dissipation with pressure/cutoff flux; no filtered vorticity tensor-moment scale variation |
| [Duchon--Robert, 2000, Propositions 1 and 3](https://doi.org/10.1088/0951-7715/13/1/312) | distributional local energy balance and a cubic velocity-increment defect | no $V^q$ or square-variation estimate for fixed-center nested core moments |
| [Dascaliuc--Grujić, 2011, Theorems 4.1 and 5.1](https://arxiv.org/html/1101.2193v2) | Taylor-scale- and time-length-conditional optimal-cover averaged modified energy flux; separately, a local-Taylor-scale-conditional fixed-center shell modified flux | neither result gives energy-only variation for a complete fixed-center nested chain; ordinary-flux upper comparability additionally needs local energy equality |
| [Dascaliuc--Grujić, 2013, Theorems 4.1--4.2](https://arxiv.org/pdf/1107.0058) | enstrophy-flux positivity and scale locality under vorticity coherence, a modified Kraichnan-scale condition, terminal modulation/localization, and solution/data hypotheses | the hypotheses add geometric, scale, and time information absent from energy alone |
| [Fefferman--Stein, 1972, Theorem 3](https://doi.org/10.1007/BF02392215) | BMO characterized by a Carleson measure of a Poisson extension | the Carleson density is extra local concentration control, not a consequence of global $L^2$ mass |
| [Koch--Tataru, 2001, Definition 1.1 and Theorems 2--3](https://math.berkeley.edu/~tataru/papers/nas.pdf) | $BMO^{-1}$ and solution-space parabolic tent norms | small critical tent control is an additional hypothesis and the object is not the core vorticity tensor moment |
| [Jones--Seeger--Wright, 2008, Theorems 1.1--1.2](https://people.math.wisc.edu/~seeger/papers/jsw.pdf) | for $1<p<\infty$, strong $V^q$, $q>2$, for dyadic convolution averages and truncated singular integrals generated by compactly supported finite Borel measures under Fourier decay (10); the truncated family also has mean-zero condition (12), while (11) supplies the endpoint regularity used for weak type $(1,1)$ | controls linear families, not the changing-cutoff quadratic moment or its positive work |
| [Do--Muscalu--Thiele, 2012, Theorems 1.2--1.3](https://ems.press/content/serial-article-files/38391?nt=1) | bilinear variation estimates for Littlewood--Paley paraproduct block increments; $p=q=r=s=t=2$ gives strong $L_x^1(\ell^2)$ | closest positive tool, but frequency-localized, signed, and missing the physical cutoff, time window, and full quadratic diagonal |

No theorem matching the complete target was found in this bounded audit. This
is a documented search result, not a proof that no such theorem exists.

## 12. Claim-to-evidence ledger

| claim | support | status |
|---|---|---|
| $m^{(0)}=rM^{(0)}$, $m^{(1)}=M^{(1)}$, (2.6), and (2.7) | scaling and direct work factorization | proved algebraically; $c(t)$ cannot be extracted from the time integral without time constancy |
| critical Abel identity (3.2) | finite summation by parts | proved algebraically and checked on exact finite sequences |
| ordinary scale ledger (4.4) | polarization and cutoff decomposition | proved algebraically |
| fixed-time $\ell_k^1$ variation, and its common-time $L_t^1\ell_k^1$ integral | filter square function, one-sided geometric scale weights, and Plancherel | proved under (5.1); not a bound for the weighted spacetime coordinate $\mathcal N$ |
| nested-window ledgers (6.2) and (6.4) | exact interval and scale-weight decomposition | proved algebraically |
| weighted parabolic duality gap | comparison of (5.9) with (7.1)--(7.3a) | proved for the direct Hölder/Cauchy route; no universal impossibility claim |
| filtered moment identity contains vortex stretching | filtered vorticity equation and integration by parts | proved for smooth filtered solutions |
| R0.70F ordinary variation is bounded but pairing variation is linear | exact $b_n$ recurrence | proved for the initial-face family and exact certificate |
| energy does not supply the normalized parabolic Carleson density | global-mass versus local-density norm comparison | functional mismatch; not an actual NSE counterexample |
| no matching theorem was found | eight-source primary audit | bounded search finding only |

## 13. Closed question, open question, and R0.70I

### Closed in R0.70H

- The work-critical moments and the source-square-function dual coordinates
  are different normalizations.
- Critical Abel summation uses the pairing factor $\rho^{n+2}$, not the
  geometric moment factor $\rho^{1-n}$.
- At each fixed time, ordinary and instantaneous pairing-covariant scale
  variation admit a genuine $\ell_k^1$ bound under the explicit filter
  condition; common-time integration gives $L_t^1\ell_k^1$.
- The actual spacetime work uses $\mathcal N_k=r_k^{-2}\mathbf1_{I_k}m_k$;
  the unweighted estimate does not control it.
- Direct source--core Cauchy--Schwarz requires the negative-weight expression
  (7.3a), not merely a better time exponent.
- Moment time evolution contains the same resolved vortex stretching and is
  circular after absolute values unless supplemented by another mechanism.
- The R0.70F pressure family exactly realizes the ordinary-versus-pairing
  baseline defect at the initial face.

### Still open in this route

- A bound of the form (7.3a), or another paired norm strong enough to control
  (7.2).
- A local/parabolic Carleson estimate for the fixed-center filtered core
  moment derived from information genuinely available for Leray solutions.
- A coupled source--core bilinear estimate that avoids separating the cubic
  term into incompatible norms.
- A signed mechanism that survives the positive part.
- Any common-positive-terminal-time realization or exclusion of the
  initial-face recurrence.

### R0.70I success criterion

The next smallest gate is the **parabolic source--core coupling problem**.
It should not ask again for ordinary scale variation. It should decompose the
filter-difference core term into Littlewood--Paley paraproduct, diagonal, and
physical-cutoff pieces, then test whether the actual time-window geometry
supplies either

\[
 \int\sum_k r_k
 |\mathfrak D_k^{\rm st}\mathcal N_k|^2dt<\infty
 \tag{13.1}
\]

or a direct trilinear embedding for (7.2), using only energy, dissipation, and
the fixed source--target separation.

R0.70I succeeds if it proves one nontrivial component of that embedding with
correct weights and isolates the remaining component, or constructs a
scale-correct caloric/initial-boundary family showing why the proposed
component cannot be energy-only. An initial-boundary result must not be
reported as a common-top-time NSE counterexample.

## 14. Reproduction

The exact finite symbolic-regression producer is
`research/r070h_core_moment_audit.py`. It checks:

- instantaneous and spacetime dimensional work normalization;
- constant- and variable-coefficient finite Abel regressions;
- scalar-contraction adjacent-scale ledgers;
- the conditional nested-window ledger and spacetime overlap factors;
- the nonconstant-radius $\rho$-to-$\lambda$ index map and the exact
  $r_k(r_k^{-2})^2=r_k^{-3}$ dual weight;
- one polynomial pointwise-divergence regression of the local-enstrophy
  identity, with $\Omega=\nabla\times U$;
- corrected finite-$N$ R0.70F recurrence samples;
- component scale-weight geometric sums.

The general identities and lower bounds are proved in the report, not by
extrapolating finite regression loops. The certificate does not
computer-prove the filter hypothesis, compact geometry inherited from
R0.70F, a Leray-class Carleson estimate, nonlinear time persistence, a
singular solution, large-data regularity, or a Millennium solution.

The journal-style explanatory figure is archived at
`figures/r070h-core-moment-gap/fig-r070h-core-moment-gap/`. It plots closed
algebraic sequences and the exact scale weight only. It is not a numerical
Navier--Stokes trajectory, a PDE simulation, or evidence for a singularity;
the displayed $\Lambda=2$ case is an algebraic diagnostic and does not certify
the compact-field geometry assumed in R0.70F.
