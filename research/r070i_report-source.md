# R0.70I — Temporal Hardy reduction and the frozen-low paraproduct closure

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70I
**Date:** 2026-08-24
**Scope:** the exact temporal kernel behind the R0.70H core dual norm,
Littlewood--Paley separation of the source--core pairing, one energy-level
paraproduct closure, and initial-boundary sharpness

---

## 1. Result in one page

R0.70H identified the core quantity directly dual to the fixed-family source
square function. For a fixed center, a one-sided geometric scale chain, and
degrees $n=0,1$, its interior part is

\[
 \begin{aligned}
 \mathcal T_n
 :=\int\sum_k r_k^{-3}\bigg[&
 \mathbf1_{I_{k+1}}
 \left|m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}\right|^2\\
 &+\mathbf1_{I_k\setminus I_{k+1}}
 |m_k^{(n)}|^2\bigg]dt .
 \end{aligned}
 \tag{1.1}
\]

R0.70I obtains four precise conclusions.

First, the whole core norm has a one-dimensional temporal upper bound. Put

\[
 f(t)=\|\omega(t)\|_2^2,
 \qquad s=t_0-t.
 \tag{1.2}
\]

Then

\[
 \boxed{
 \mathcal T_n
 \lesssim
 \int_0^{r_0^2}s^{-1/2}f(t_0-s)^2\,ds,
 \qquad n=0,1.}
 \tag{1.3}
\]

For a finite chain ending at $r_K$, the sharper kernel is

\[
 \boxed{
 \min\{r_K^{-1},s^{-1/2}\}.}
 \tag{1.4}
\]

Thus the negative scale weight is exactly a temporal Hardy singularity. It
does not disappear merely because the discarded time slabs are disjoint.
Leray dissipation gives $f\in L_t^1$, while (1.3) asks for a weighted square
of $f$. The scalar profile $f(t_0-s)=s^{-\alpha}$ is in $L^1$ for
$\alpha<1$, whereas the right side of (1.3) diverges for
$\alpha\ge1/4$. This is a function-space obstruction, not a
Navier--Stokes trajectory.

Second, the complete quadratic core can be split into a part that really is
controlled at the Leray level and a smaller unresolved remainder. Freeze the
outer low-frequency vorticity

\[
 L_0=P_{\le c/r_0}\omega
 \tag{1.5}
\]

and let $B_k$ be an annular vorticity packet, with velocity block
$V_k$ satisfying $B_k=\nabla\times V_k$. If the cumulative source
coefficient obeys the R0.70H fixed-family estimate

\[
 \mathsf C^2
 =\int\sum_k r_k^{-1}|c_k(t)|^2dt<\infty,
 \tag{1.6}
\]

then, under the standard LP square-function assumptions stated in (5.0),
the full frozen-low/annular mixed triangular array, including its
physical-cutoff and nested-window pieces, satisfies

\[
 \boxed{
 |\mathscr W_{\rm frozen\text{-}low/mixed}|
 \lesssim r_0^{-3/2}
 \|u\|_{L_t^\infty L_x^2}\,
 \mathsf C\,
 \|\omega\|_{L_t^2L_x^2}.}
 \tag{1.7}
\]

This is an absolute termwise estimate. It survives taking positive parts.
The frozen low--low term also closes, and the isotropic high--high component
vanishes because the source jet is trace-free in the two vorticity indices.

Third, the representative unresolved mechanisms are now explicit for the
direct termwise-absolute route:

- the moving-low paraproduct requires a scale-dependent
  $B^{3/2}_{2,1}$-type or Carleson maximal quantity;
- the deviatoric high--high diagonal produces
  $\int\sum_k r_k^{-1}\|W_k\|_2^4dt$;
- the physical cutoff supplies no Fourier scale-gap factor;
- the fine Abel endpoint has the same saturated temporal kernel as (1.4).

None is controlled by
$L_t^\infty L_x^2\cap L_t^2\dot H_x^1$ through direct
Cauchy--Schwarz.

Fourth, the temporal and outer-scale losses are sharp at the initial
boundary. A small smooth Navier--Stokes solution $v^a$ with data $av_0$ can
be rescaled as

\[
 u^{a,r}(x,t)=r^{-1}v^a(x/r,t/r^2).
 \tag{1.8}
\]

On the initial-boundary window $r_0=r$, $t_0=r^2$, a suitable nonzero
profile gives

\[
 \boxed{
 \mathcal T_n[u^{a,r}]\gtrsim r^{-1}a^4,
 \qquad E[u^{a,r}]\asymp ra^2,
 \qquad D_{[0,r^2]}[u^{a,r}]\asymp ra^2.}
 \tag{1.9}
\]

Consequently $r_0^{-3}E^2$ has exactly the same size as the core norm. The
family rules out an outer-scale-free right side that remains locally bounded
as its energy and dissipation arguments tend to zero. This is an actual
smooth NSE initial-boundary family, but $t_0=r^2\downarrow0$; it is not one
solution trajectory concentrating at a fixed positive terminal time.

The R0.70I conclusion is therefore both positive and restrictive:

> **The frozen top-low/annular paraproduct is not the obstruction. It closes
> absolutely at the Leray level. The unresolved core is the moving-low plus
> deviatoric diagonal sector, whose direct norm is governed by the temporal
> Hardy weight $s^{-1/2}$.**

Nothing here proves global regularity, constructs a singularity, or solves
the Millennium problem.

## 2. Fixed conventions and the actual core norm

Let

\[
 r_{k+1}=\rho_kr_k,
 \qquad 0<\rho_-\le\rho_k\le\rho_+<1,
 \qquad I_k=(t_0-r_k^2,t_0).
 \tag{2.1}
\]

The chain is finite, $0\le k\le K$, or one-sided toward fine scales,
$k\in\mathbb N_0$. Let

\[
 \Omega_k=\varphi_{\sigma r_k}*\omega,
 \qquad
 \chi_k(x)=\chi((x-x_0)/r_k),
 \tag{2.2}
\]

where $\varphi\in L^1$ is a fixed smooth low-pass filter and $\chi$ is a
fixed compact cutoff. With $y=x-x_0$,

\[
 M_k^{(n)}
 =\int\chi_k y^{\otimes n}\otimes
       \Omega_k\otimes\Omega_k\,dx,
 \qquad
 m_k^{(n)}=r_k^{1-n}M_k^{(n)}.
 \tag{2.3}
\]

The spacetime work coordinate is

\[
 \mathcal N_k^{(n)}(t)
 =r_k^{-2}\mathbf1_{I_k}(t)m_k^{(n)}(t).
 \tag{2.4}
\]

The exact Abel increment from R0.70H is

\[
 \begin{aligned}
 \mathfrak D_k^{\rm st}\mathcal N^{(n)}
 ={}&r_k^{-2}\mathbf1_{I_{k+1}}
 \left(m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}\right)\\
 &+r_k^{-2}\mathbf1_{I_k\setminus I_{k+1}}
 m_k^{(n)}.
 \end{aligned}
 \tag{2.5}
\]

The two time regions are disjoint. Hence

\[
 \int\sum_k r_k
 |\mathfrak D_k^{\rm st}\mathcal N^{(n)}|^2dt
 =\mathcal T_n.
 \tag{2.6}
\]

For a finite chain containing the moments
$m_0^{(n)},\ldots,m_K^{(n)}$, the interior quantity is, explicitly,

\[
 \begin{aligned}
 \mathcal T_{n,K}
 :=\int\sum_{k=0}^{K-1} r_k^{-3}\bigg[&
 \mathbf1_{I_{k+1}}
 \left|m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}\right|^2\\
 &+\mathbf1_{I_k\setminus I_{k+1}}|m_k^{(n)}|^2\bigg]dt.
 \end{aligned}
 \tag{2.6a}
\]

Thus no undefined $m_{K+1}^{(n)}$ occurs.  For the one-sided infinite
chain, the sum in (1.1) and (2.6) is over every $k\ge0$.

If the finite Abel identity retains the fine endpoint, its core partner is

\[
 \mathcal E_{n,K}
 =\int r_K|\mathcal N_K^{(n)}|^2dt
 =\int_{I_K}r_K^{-3}|m_K^{(n)}|^2dt.
 \tag{2.7}
\]

It obeys the same finite-chain temporal bound derived below. A nonzero coarse
endpoint is analogous. R0.70I does not silently discard either endpoint.

## 3. Exact temporal Hardy reduction

The filter is $L^2$ bounded, and on the cutoff support
$|y|^n\lesssim r_k^n$. Therefore

\[
 \boxed{
 |m_k^{(n)}(t)|
 \lesssim r_k\|\omega(t)\|_2^2
 =r_kf(t),
 \qquad n=0,1.}
 \tag{3.1}
\]

Consequently

\[
 |m_k^{(n)}-\rho_k^nm_{k+1}^{(n)}|
 \lesssim r_kf(t),
 \tag{3.2}
\]

and each active summand in (1.1) is bounded by

\[
 r_k^{-1}f(t)^2.
 \tag{3.3}
\]

Fix $s=t_0-t$. The overlap indicator is active exactly when

\[
 s<r_{k+1}^2.
 \tag{3.4}
\]

If $K(s)$ is the finest active overlap index, then

\[
 \sum_{k=0}^{K(s)}r_k^{-1}
 \le\frac{1}{1-\rho_+}r_{K(s)}^{-1}
 \lesssim s^{-1/2}.
 \tag{3.5}
\]

The slab indicator

\[
 r_{k+1}^2\le s<r_k^2
 \tag{3.6}
\]

selects at most one index and its $r_k^{-1}$ is also at most a fixed
multiple of $s^{-1/2}$. Integrating (3.3) proves (1.3).

For a finite chain, the complete scalar kernel for the $K$ interior
increments and the fine endpoint is

\[
 \begin{aligned}
 G_K(s):={}&
 \sum_{k=0}^{K-1}r_k^{-1}\mathbf1_{s<r_{k+1}^2}
 +\sum_{k=0}^{K-1}r_k^{-1}
   \mathbf1_{r_{k+1}^2\le s<r_k^2}\\
 &+r_K^{-1}\mathbf1_{s<r_K^2}.
 \end{aligned}
 \tag{3.6a}
\]

If $s<r_K^2$, all available overlap scales are active and the sum can grow
no further.  The geometric-chain assumptions therefore give

\[
 G_K(s)\lesssim
 \mathbf1_{0<s<r_0^2}\min\{r_K^{-1},s^{-1/2}\}.
 \tag{3.6b}
\]

Consequently

\[
 \boxed{
 \mathcal T_{n,K}+\mathcal E_{n,K}
 \lesssim
 \int_0^{r_0^2}
 \min\{r_K^{-1},s^{-1/2}\}
 f(t_0-s)^2\,ds.}
 \tag{3.7}
\]

Changing $r_K$ to $r_{K-1}$ when the interior increment stops at $K-1$
only changes the geometric constant. Equation (3.7) is uniform in the chain
length but records the exact finest-scale saturation.

The exponent $1/2$ comes from parabolic time $s\simeq r^2$ together with the
spatial dual weight $r^{-1}$ after using (3.1). It is not an artifact of a
loose count of the time slabs.

## 4. Temporal integrability threshold

The Leray inequality gives only

\[
 \int f(t)dt
 =\int\|\omega(t)\|_2^2dt<\infty.
 \tag{4.1}
\]

No embedding sends this $L^1$ quantity to the right side of (1.3). For the
scalar comparator

\[
 f(t_0-s)=c s^{-\alpha},
 \tag{4.2}
\]

one has

\[
 \int_0^1f(t_0-s)ds<\infty
 \quad\Longleftrightarrow\quad \alpha<1,
 \tag{4.3}
\]

whereas

\[
 \int_0^1s^{-1/2}f(t_0-s)^2ds<\infty
 \quad\Longleftrightarrow\quad \alpha<\frac14.
 \tag{4.4}
\]

For $1/4\le\alpha<1$, (4.1) holds and (4.4) fails. This proves a norm
non-implication only. The comparator has not been realized as the enstrophy
history of a common-top NSE solution.

The temporal exponent is attained by an abstract moment-size comparator.
For a fixed nonzero tensor $T$, put

\[
 m_k^{(n)}(t)=r_k f(t)T.
 \tag{4.4a}
\]

Then on the overlap window

\[
 m_k^{(n)}-\rho_k^nm_{k+1}^{(n)}
 =(1-\rho_k^{n+1})r_kf(t)T.
 \tag{4.4b}
\]

Because $\rho_k\le\rho_+<1$, the resulting finite-chain kernel is comparable
from above and below to (1.4). This verifies that the power $s^{-1/2}$ cannot
be improved from the moment-size inequality (3.1) alone. Sequence (4.4a) is
not asserted to be the filtered moment sequence of one NSE solution.

A direct sufficient condition is

\[
 \int_0^{r_0^2}s^{-1/2}
 \|\omega(t_0-s)\|_2^4ds<\infty.
 \tag{4.5}
\]

For example, if

\[
 f(t_0-s)\le A s^{-\alpha},
 \qquad \alpha<\frac14,
 \tag{4.6}
\]

then

\[
 \mathcal T_n
 \lesssim
 \frac{A^2r_0^{1-4\alpha}}{1-4\alpha}.
 \tag{4.7}
\]

More generally, if

\[
 \omega\in L_t^pL_x^2(I_0),
 \qquad p>8,
 \tag{4.8}
\]

Hölder gives

\[
 \mathcal T_n
 \lesssim
 r_0^{1-8/p}
 \|\omega\|_{L_t^pL_x^2(I_0)}^4.
 \tag{4.9}
\]

This is a strong additional regularity condition, not a consequence of the
Leray class. R0.70I makes no endpoint $p=8$ claim.

## 5. Physical-cutoff and filter decomposition

Sections 5--8 now specialize the general smooth filter in Section 2 to a
standard Littlewood--Paley resolution, or to a finite-overlap multiplier
family with the same estimates.  We use chain-adapted annular vorticity
packets $B_j=\nabla\times V_j$ satisfying

\[
 \|B_j\|_2\lesssim r_j^{-1}\|V_j\|_2,
 \qquad
 \sum_j\|V_j(t)\|_2^2\lesssim\|u(t)\|_2^2,
 \tag{5.0}
\]

and the low-pass expansion
$\Omega_k=L_0+\sum_{1\le j\le k}B_j$, up to a uniformly finite overlap.
For Schwartz multipliers the corresponding rapidly decaying tails are
included only when their standard almost-orthogonality estimates imply
(5.0).  The closure claims below are not asserted for an arbitrary
$L^1$-bounded filter lacking this LP structure.

Write

\[
 Q_k=\Omega_k\otimes\Omega_k.
 \tag{5.1}
\]

On the overlap window, direct substitution in (2.5) gives

\[
 \begin{aligned}
 &r_k^{-2}
 \left(m_k^{(n)}-\rho_k^nm_{k+1}^{(n)}\right)\\
 &\quad=r_k^{-n-1}\bigg[
 \int(\chi_k-\rho_k\chi_{k+1})
 y^{\otimes n}\otimes Q_k\,dx\\
 &\qquad\qquad
 -\rho_k\int\chi_{k+1}y^{\otimes n}\otimes
 (Q_{k+1}-Q_k)\,dx\bigg].
 \end{aligned}
 \tag{5.2}
\]

Thus the full spacetime increment is the sum

\[
 \mathfrak D_k^{\rm st}\mathcal N
 =\mathcal C_{k,n}+\mathcal F_{k,n}+\mathcal S_{k,n},
 \tag{5.3}
\]

where

\[
 \mathcal C_{k,n}
 =r_k^{-n-1}\mathbf1_{I_{k+1}}
 \int(\chi_k-\rho_k\chi_{k+1})
 y^{\otimes n}\otimes Q_k\,dx,
 \tag{5.4}
\]

\[
 \mathcal F_{k,n}
 =-\rho_kr_k^{-n-1}\mathbf1_{I_{k+1}}
 \int\chi_{k+1}y^{\otimes n}\otimes
 (Q_{k+1}-Q_k)\,dx,
 \tag{5.5}
\]

and

\[
 \mathcal S_{k,n}
 =r_k^{-n-1}\mathbf1_{I_k\setminus I_{k+1}}
 \int\chi_ky^{\otimes n}\otimes Q_k\,dx.
 \tag{5.6}
\]

The cutoff coefficient contains both the physical shell and the pairing
baseline:

\[
 \chi_k-\rho_k\chi_{k+1}
 =(\chi_k-\chi_{k+1})+(1-\rho_k)\chi_{k+1}.
 \tag{5.7}
\]

All three terms have the same elementary physical weight. If $a_{k,n}$ is
the scalar size of the cutoff and tensor factor, then

\[
 \|a_{k,n}\|_\infty\lesssim r_k^{-1},
 \qquad
 |\operatorname{supp}a_{k,n}|\lesssim r_k^3.
 \tag{5.8}
\]

This common weight is why the physical shell and the time slab cannot be
treated as lower-order bookkeeping errors.

Let

\[
 \delta\Omega_k=\Omega_{k+1}-\Omega_k.
 \tag{5.9}
\]

The exact polarization is

\[
 Q_{k+1}-Q_k
 =\delta\Omega_k\otimes\Omega_k
 +\Omega_k\otimes\delta\Omega_k
 +\delta\Omega_k\otimes\delta\Omega_k.
 \tag{5.10}
\]

For a standard annular LP filter, $\delta\Omega_k$ is a uniformly finite
sum of packets concentrated at frequency
$2^{J_k}\simeq r_k^{-1}$. Bony's decomposition separates (5.10) into
low--high, high--low, and high--high/diagonal pieces. With an ideal compact
Fourier low-pass, the far high--low term is empty; for a Schwartz low-pass it
is a rapidly decaying tail requiring the usual multiplier regularity. The
square-function assumption alone does not certify every such tail estimate.

The physical cutoff does not restore Fourier orthogonality. Indeed,

\[
 \int\chi_k f_p g_q
 =\iint\widehat\chi_k(-\xi-\eta)
 \widehat f_p(\xi)\widehat g_q(\eta)\,d\xi d\eta.
 \tag{5.11}
\]

Since
$\widehat\chi_k(\zeta)=r_k^3e^{-ix_0\cdot\zeta}
\widehat\chi(r_k\zeta)$, the multiplier itself carries the expected volume
factor $r_k^3$.  When $p\simeq J_k$ and $q\ll p$,
$r_k|\xi+\eta|\simeq1$, so after this spatial-volume normalization its
profile is generally order one.  There is no automatic small factor from
the scale gap.

## 6. Frozen-low/annular closure

Freeze the top low frequency

\[
 L_0=P_{\le c/r_0}\omega
 \tag{6.1}
\]

and use the annular packets from (5.0):

\[
 B_j=\nabla\times V_j,
 \qquad
 \|B_j\|_2\lesssim r_j^{-1}\|V_j\|_2,
 \qquad
 \sum_j\|V_j(t)\|_2^2\lesssim\|u(t)\|_2^2.
 \tag{6.2}
\]

The filter-difference term contains only $j=k+O(1)$, but the cutoff and slab
terms contain the entire triangular array $j\le k$.  For any occurrence of
$B_j\otimes L_0$ or its tensor reverse in (5.4)--(5.6), (5.8), spatial
Cauchy--Schwarz, and annular Bernstein give

\[
 \begin{aligned}
 \left|\int a_{k,n}B_j\otimes L_0\,dx\right|
 &\lesssim r_k^{-1}r_k^{3/2}
 \|B_j\|_2\|L_0\|_\infty\\
 &\lesssim r_k^{-1/2}\frac{r_k}{r_j}
 \|V_j\|_2\|L_0\|_\infty,
 \qquad j\le k.
 \end{aligned}
 \tag{6.3}
\]

The first factor matches the source coordinate:

\[
 |c_k|r_k^{-1/2}.
 \tag{6.4}
\]

Set $H_k=\sum_{j\le k}(r_k/r_j)\|V_j\|_2$. Since

\[
 \frac{r_k}{r_j}
 =\prod_{q=j}^{k-1}\rho_q
 \le\rho_+^{k-j},
 \qquad
 \sum_kH_k^2\lesssim_{\rho_+}\sum_j\|V_j\|_2^2,
 \tag{6.4a}
\]

where the second inequality is Young's inequality for the discrete
$\ell^1*\ell^2$ convolution. Hence, at each time, the complete triangular
array satisfies

\[
 \begin{aligned}
 \sum_k|c_k|r_k^{-1/2}H_k\|L_0\|_\infty
 \lesssim{}&
 \left(\sum_kr_k^{-1}|c_k|^2\right)^{1/2}\\
 &\times\left(\sum_j\|V_j\|_2^2\right)^{1/2}
 \|L_0\|_\infty.
 \end{aligned}
 \tag{6.5}
\]

The fixed low-pass Bernstein estimate is

\[
 \|L_0(t)\|_\infty
 \lesssim r_0^{-3/2}\|\omega(t)\|_2.
 \tag{6.6}
\]

Using $L_t^2\times L_t^\infty\times L_t^2$ in (6.5) proves (1.7).
Rowwise window indicators only decrease the $\ell^2$ norm in (6.4a), so the
same argument covers the physical-cutoff and discarded-slab mixed arrays,
not just the same-index filter difference. No coefficient $c_k(t)$ has been
factored out of time, and the physical cutoff has not been discarded.

The frozen low--low contribution also closes. Here

\[
 \|L_0\|_\infty
 \lesssim r_0^{-5/2}\|u\|_2,
 \tag{6.7}
\]

and

\[
 \sum_k|c_k|r_k^2
 \le
 \left(\sum_kr_k^{-1}|c_k|^2\right)^{1/2}
 \left(\sum_kr_k^5\right)^{1/2}.
 \tag{6.8}
\]

Since the outer time interval has length $r_0^2$, (6.7)--(6.8) yield

\[
 \boxed{
 |\mathscr W_{\rm frozen\text{-}low/low}|
 \lesssim
 r_0^{-3/2}
 \|u\|_{L_t^\infty L_x^2}^2\mathsf C.}
 \tag{6.9}
\]

Both (1.7) and (6.9) are absolute estimates, so these components remain
controlled when a positive part is applied before summing scales.

## 7. The exact isotropic cancellation

Let $c_{ij}$ denote the two vorticity indices of a degree-zero source jet, or
the corresponding pair inside a degree-one coefficient. The strain and all
of its spatial derivatives are trace-free in those indices:

\[
 c_{ii}=0.
 \tag{7.1}
\]

Therefore the isotropic part of a diagonal high--high tensor vanishes
identically:

\[
 c_{ij}\left(\frac{|W_k|^2}{3}\delta_{ij}\right)=0.
 \tag{7.2}
\]

This cancellation is pointwise in the tensor contraction. It survives
cutoffs, time windows, and positive parts because the contracted component is
exactly zero. It does not cancel the deviatoric tensor

\[
 W_k\otimes W_k-\frac{|W_k|^2}{3}I.
 \tag{7.3}
\]

## 8. Representative unresolved Bony sectors

This section identifies the norms forced by the direct, termwise-absolute
triangle route.  It is not an exhaustive signed Bony identity for every
cutoff and slab array.  In particular, the physical-cutoff pieces contain
additional lower-triangular indices; unlike the frozen $L_0$ array in
Section 6, their moving-low and diagonal factors have no summable geometric
gain under Leray control.

Split the low factor at the fixed outer scale:

\[
 S_{J_k-L}\omega
 =L_0+L_k^{\rm mov},
 \qquad
 L_k^{\rm mov}
 =\sum_{J_0<j\le J_k-L}\Delta_j\omega.
 \tag{8.1}
\]

### 8.1 Moving low

The same physical estimate used in (6.3) now produces

\[
 |c_k\mathcal F_{k,j}^{LH}|
 \lesssim
 \underbrace{|c_k|r_k^{-1/2}}_{\text{source square coordinate}}
 \|V_k\|_2
 2^{3j/2}\|\Delta_j\omega\|_2.
 \tag{8.2}
\]

Summing the moving range $J_0<j\le J_k-L$ by this absolute route requires
control of

\[
 \sum_{J_0<j\le J_k-L}
 2^{3j/2}\|\Delta_j\omega\|_2.
 \tag{8.3}
\]

This is a moving $B^{3/2}_{2,1}$-type or Carleson maximal quantity. Leray
dissipation controls the unweighted square sum of the vorticity blocks, not
the weighted $\ell^1$ accumulation in (8.3).  This states a requirement of
the present direct absolute-value route, not a theorem that every possible
signed or equation-correlated argument must control (8.3).

### 8.2 Deviatoric high--high

For a current diagonal block $W_k$, the direct physical estimate is only

\[
 |\mathcal F_{k,HH}|
 \lesssim r_k^{-1}\|W_k\|_2^2.
 \tag{8.4}
\]

After source Cauchy--Schwarz, the core partner contains

\[
 \boxed{
 \int\sum_k r_k^{-1}\|W_k(t)\|_2^4dt.}
 \tag{8.5}
\]

The Leray inequality provides only

\[
 \int\sum_k\|W_k(t)\|_2^2dt<\infty.
 \tag{8.6}
\]

The missing spatial weight and time square occur together. The physical
cutoff shell and discarded time slab have the same $r_k^{-1}$ multiplier and
do not repair (8.5).

### 8.3 Fine endpoint

The endpoint (2.7) is controlled by the finite kernel in (3.7). It therefore
saturates at $r_K^{-1}f(t)^2$ during the final time layer. It is not a
separate source of a better exponent.

These facts reduce the open direct-Cauchy gate to moving-low, deviatoric
diagonal, and the associated endpoint. A proof using a correlation special
to the NSE equation or a signed cancellation across these sectors is not
excluded.

## 9. An abstract source-coordinate comparator (degree zero)

The failure of the remaining direct Hilbert-space norm is scale-sharp before
one asks whether the source coordinate is realized by an exterior pressure
field.  Choose

\[
 U\in C_c^\infty(\mathbb R^3;\mathbb R^3),
 \qquad \nabla\!\cdot U=0,
 \qquad
 0\le\theta\in C_c^\infty((-1,0)),
 \quad\theta\not\equiv0.
 \tag{9.1}
\]

Fix a nonnegative cutoff $\chi$ and filter scale $\sigma$ so that

\[
 Q_0:=\int\chi(z)
 [\varphi_\sigma*\operatorname{curl}U](z)
 \otimes[\varphi_\sigma*\operatorname{curl}U](z)\,dz,
 \qquad \operatorname{dev}Q_0\ne0.
 \tag{9.2}
\]

An anisotropic compact divergence-free profile can be chosen with this
property. Put

\[
 \theta_r(t)=\theta((t-t_0)/r^2),
 \qquad
 u_r(x,t)=r^{-3/2}U((x-x_0)/r)\theta_r(t).
 \tag{9.3}
\]

Direct change of variables gives

\[
 \|u_r\|_{L_t^\infty L_x^2}\simeq1,
 \qquad
 \|\nabla u_r\|_{L_{t,x}^2}\simeq1,
 \qquad
 m_r^{(0)}(t)=r^{-1}\theta_r(t)^2Q_0,
 \tag{9.4}
\]

and hence

\[
 \mathcal N_r^{(0)}(t)=r^{-3}\theta_r(t)^2Q_0.
 \tag{9.5}
\]

Let

\[
 C_0=\frac{\operatorname{dev}Q_0}{|\operatorname{dev}Q_0|},
 \qquad
 c_r(t)=r^{-1/2}\theta_r(t)C_0.
 \tag{9.6}
\]

The coefficient is trace-free and obeys the critical source norm

\[
 \int r^{-1}|c_r(t)|^2dt
 =\int_{-1}^{0}\theta(\tau)^2d\tau,
 \tag{9.7}
\]

whereas the contraction is strictly positive:

\[
 \int c_r:\mathcal N_r^{(0)}dt
 =r^{-3/2}|\operatorname{dev}Q_0|
 \int_{-1}^{0}\theta(\tau)^3d\tau>0.
 \tag{9.8}
\]

This is an abstract source-coordinate/core comparator for $n=0$.  It proves
that the three displayed norms alone do not imply a scale-uniform direct
trilinear embedding.  It does **not** construct $c_r$ from a compact exterior
divergence-free source, verify the complete harmonic-jet realization
constraints, treat the degree-one coefficient, or place the source and core
on one NSE trajectory.  Equation (9.8) therefore leaves open an
equation-specific correlation or signed cancellation.

## 10. Initial-boundary sharpness

In this section

\[
 E[u]:=\|u(0)\|_2^2,
 \qquad
 D_{[0,T]}[u]:=\nu\int_0^T\|\nabla u(t)\|_2^2dt.
 \tag{10.0}
\]

Every scaling statement below rescales one fixed cutoff, filter, complete
base chain, center, and terminal time together with the field.

### 10.1 Linear heat scaling

Fix a nonzero divergence-free Schwartz solution $v$ of the linear heat
equation, a base chain $\{R_k\}$, a top time $\tau_0$, and a fixed
filter/cutoff family for which

\[
 \mathcal T_n[v;\{R_k\},\tau_0]>0.
 \tag{10.0a}
\]

For $n=0$ this can be arranged by placing a cutoff and discarded slab where
the filtered vorticity is nonzero; for $n=1$ the base profile must
additionally have a nonzero asymmetric first moment. Define

\[
 u^{A,r}(x,t)=A v((x-x_0)/r,t/r^2),
 \quad
 r_k^{(r)}=rR_k,
 \quad
 t_0^{(r)}=r^2\tau_0,
 \quad
 \ell_k^{(r)}=r\ell_k.
 \tag{10.1}
\]

Direct change of variables gives

\[
 E,D_{[0,\tau_0]}\mapsto A^2r^3
 (E,D_{[0,\tau_0]}),
 \tag{10.2}
\]

\[
 M^{(n)}\mapsto A^2r^{n+1}M^{(n)},
 \qquad
 m^{(n)}\mapsto A^2r^2m^{(n)},
 \tag{10.3}
\]

and

\[
 \mathcal T_n[u^{A,r};\{rR_k\},r^2\tau_0]
 =A^4r^3\mathcal T_n[v;\{R_k\},\tau_0].
 \tag{10.4}
\]

Taking $A=r^{-3/2}$ keeps the two base-window quantities fixed and, by the
strict positivity in (10.0a), gives
$\mathcal T_n=r^{-3}\mathcal T_n[v]$. This is a linear initial-layer
counterexample to any outer-scale-free right side that is locally bounded on
bounded energy/dissipation sets. A linear heat field is not generally a
Navier--Stokes solution.

### 10.2 Small smooth NSE scaling

Choose a nonzero smooth divergence-free rapidly decaying datum $v_0$, and
fix one base cutoff/filter/chain/top family whose filtered linear vorticity
has a nonzero zeroth-moment contribution on the discarded slab. For small
$a>0$, [Koch--Tataru, Theorem
2](https://math.berkeley.edu/~tataru/papers/nas.pdf) supplies the global small
solution in its $X$ class. For this smooth datum, persistence of regularity
and the same fixed-point equation give, for any fixed sufficiently large
Sobolev index $m$,

\[
 v^a(t)=a e^{\nu t\Delta}v_0+O(a^2)
 \tag{10.5}
\]

in $C([0,1];H^m)$; the $O(a^2)$ expansion is a consequence of the contraction
equation, not a verbatim assertion of Theorem 2. Continuity and (10.5) give

\[
 \mathcal T_0[v^a]\ge c a^4.
 \tag{10.6}
\]

On the same fixed base time window, the expansion also gives

\[
 E[v^a]\asymp a^2,
 \qquad
 D_{[0,\tau_0]}[v^a]
 =a^2D_{\rm lin}+O(a^3)\asymp a^2,
 \tag{10.6a}
\]

after choosing $v_0$ with $D_{\rm lin}>0$.

For $n=1$, one may choose an asymmetric translated profile with a nonzero
first tensor moment; the same perturbative argument applies.

Apply the exact NSE scaling (1.8) while scaling the fixed base geometry as
in (10.1); normalize $R_0=\tau_0=1$, so $r_0=r$ and $t_0=r^2$. Then

\[
 \mathcal T_n[u^{a,r}]\gtrsim a^4/r,
 \qquad
 E[u^{a,r}]\asymp ra^2,
 \qquad
 D_{[0,r^2]}[u^{a,r}]\asymp ra^2.
 \tag{10.6b}
\]

Thus (1.9) follows. In particular, for fixed small $a$,

\[
 E[u^{a,r}]+D_{[0,r^2]}[u^{a,r}]\longrightarrow0,
 \qquad
 \mathcal T_n[u^{a,r}]\longrightarrow\infty
 \quad(r\downarrow0).
 \tag{10.7}
\]

Thus no outer-scale-free bound $\mathcal T_n\le F(E,D)$ with $F$ locally
bounded near $(0,0)$ can control all such initial layers. This includes the
usual monotone polynomial energy/dissipation bounds; no claim is made about a
pathological right side singular at $(0,0)$. The scale-correct quadratic
quantity is

\[
 r_0^{-3}E^2\asymp r^{-1}a^4,
 \tag{10.8}
\]

which is saturated by this family. Equation (10.8) does not prove the upper
bound $\mathcal T_n\lesssim r_0^{-3}E^2$.

More generally, dimensional scaling of a candidate monomial

\[
 r_0^{-\gamma}E^pD^q
 \tag{10.9}
\]

forces

\[
 \gamma=p+q+1.
 \tag{10.10}
\]

### 10.3 The common-positive-top boundary

Every member of (10.7) starts at $t=0$, but the members have different
rescaled initial data and are different solutions, while their terminal
times satisfy $t_0=r^2\downarrow0$. The construction does not exhibit one
solution history concentrating at a fixed $t_0=T>0$.

For comparison, if a linear heat solution is observed on a complete window
separated from its initial face by $\tau>0$, semigroup smoothing and (1.3)
give

\[
 \mathcal T_n
 \lesssim r_0(\nu\tau)^{-2}E_0^2.
 \tag{10.11}
\]

Thus linear diffusion controls rather than creates the fixed-positive-time
defect. Constructing the same concentration along one NSE solution at a
fixed positive top, or excluding it from Leray information, remains open.

## 11. Bounded primary-literature audit

R0.70H already audited local energy, physical-scale flux, BMO/Carleson,
linear variation, and bilinear LP variation. R0.70I stopped after eight new
high-signal primary sources covering maximal regularity on tent spaces, NSE
tent bilinear maps, local initial-time estimates, LP flux, and martingale
paraproduct variation.

| primary source | exact object | boundary relative to R0.70I |
|---|---|---|
| [Auscher--Monniaux--Portal, Definition 2.3 and Theorems 3.1--3.2](https://arxiv.org/pdf/1011.1748) | maximal regularity for analytic semigroups on weighted $T^{p,2,m}$ in the stated $p,\beta,m$ range, and the $T^{\infty,2,m}$ endpoint for $\beta<1$, under the stated off-diagonal orders | transfers a tent norm already present in the input; it does not square a changing-cutoff quadratic moment after spatial integration |
| [Auscher--Frey, Definition 2.2, Theorem 2.4, and Proposition 4.1](https://arxiv.org/pdf/1412.8407v3) | Theorem 2.4 proves $B:(E_T)^n\times(E_T)^n\to(E_T)^n$; in its proof the source $\alpha=u\otimes v$ has $T^{\infty,1}$, weighted $T^{\infty,2}$, and $L^\infty$ control, while Proposition 4.1 isolates the $A_2$ failure from weighted $T^{\infty,2}$ alone | those source controls encode local concentration stronger than Leray dissipation and do not give the discrete moment variation |
| [Germain--Pavlović--Staffilani, Theorem 2.2, Corollary 2.3, and Lemma 3.1](https://arxiv.org/pdf/math/0609781v2) | small-$BMO^{-1}$ smoothing; a heat source estimate using both a Carleson quantity and total $L^1$ mass | with source $\omega\otimes\omega$, Leray gives total mass but not the required Carleson factor |
| [Jia--Šverák, Lemma 3.1 and Theorem 3.1](https://arxiv.org/pdf/1204.0529) | Lemma 3.1 gives local velocity energy/dissipation from uniformly local $L^2$ data; Theorem 3.1 adds local $L^m$, $m>3$, for near-initial-time Hölder control | the regularity theorem has an extra subcritical good-region assumption, and neither statement gives a nested quadratic vorticity-moment square sum |
| [Bradshaw--Tsai, Definition 1.1 and Theorem 1.4](https://arxiv.org/pdf/2008.09204) | for $u_0\in E_q^2$, $2\le q<\infty$, and a solution in the corresponding $LE_q$ class, fixed-radius $R\ge1$ velocity energy/dissipation is summed over lattice centers | the discrete index labels different centers at one radius, not different fine scales at one center, and the controlled energy appears only to the first power |
| [Eyink--Aluie, equations (1)--(11) and (20)--(24)](https://arxiv.org/pdf/0909.2386) | smooth coarse-grained energy flux and a positive global band-energy decomposition for the specified nonnegative S-type filter; scale locality uses $0<\sigma_p<1$ structure-function/Besov scaling, and relative-flux comparison uses nonzero mean flux | useful first-power band orthogonality, but no fixed cutoff, nested time window, or negative-weight moment square |
| [Cheskidov--Constantin--Friedlander--Shvydkoy, Proposition 3.2 and Theorem 3.3](https://arxiv.org/pdf/0704.0759) | global Fourier-LP Euler velocity-energy flux controlled using $L^3$-Besov data at the Onsager scale; the paper's enstrophy statement is two-dimensional | stronger spatial integrability and a global velocity-flux object, not the three-dimensional fixed-center vorticity moment |
| [Kovač--Zorin-Kranich, Theorem 1.1](https://arxiv.org/pdf/1812.09763) | for $p,q\in(1,\infty)$, $r>1/2$, $1/r=1/p+1/q$, and variation exponent $>1$, variation and jump estimates for truncated off-diagonal martingale paraproducts built from one filtration | smooth cutoffs are not conditional expectations, while diagonal, cutoff, time-slab, and scale-weight terms remain |

The appearance of $r^{-3}$ in a three-dimensional tent norm is not itself a
match. A tent norm has the order

\[
 r^{-3}\int_{Q_r}|F(x,t)|^2\,dxdt,
 \tag{11.1}
\]

where the spatial field is squared before integration. The core target has
the order

\[
 r^{-3}|m_k(t)|^2
 \lesssim
 r^{-1}\left(\int_{B_{Cr}}|\Omega_k(x,t)|^2dx\right)^2,
 \tag{11.2}
\]

where local enstrophy is integrated first and then squared. Passing from
(11.1) to (11.2) introduces an $L^4$ or local-enstrophy-square requirement.

No audited theorem supplies every target feature from Leray energy and
dissipation alone. This is a bounded search finding, not a proof that no such
theorem exists. The theorem-by-theorem scope record is archived in
`research/r070i_literature_audit.md`.

## 12. Claim-to-evidence ledger

| claim | support | status |
|---|---|---|
| finite and infinite temporal kernels (1.3)--(1.4) | moment size (3.1), exact window indicators, geometric summation | proved; finite exact cases are machine-regressed |
| $\alpha=1/4$ scalar threshold | elementary power integral | proved as a norm comparator, not an NSE trajectory |
| frozen-low/annular estimate (1.7) | physical support size, band Bernstein, triangular convolution, source square function, and Leray norms | proved for a standard annular LP decomposition and fixed source family |
| frozen low--low estimate (6.9) | outer low-pass Bernstein and geometric scale sum | proved under the same fixed-family boundary |
| isotropic high--high cancellation | trace-free source tensor | exact algebraic identity |
| moving-low and deviatoric diagonal remain open | direct-route required norms (8.3) and (8.5) | direct-Cauchy gap; no exhaustive Bony or universal impossibility claim |
| abstract degree-zero coordinate comparator | explicit identities (9.1)--(9.8) | norm counterexample only; no exterior harmonic realization and no NSE trajectory |
| heat initial-layer scaling | direct change of variables | exact |
| small NSE initial-boundary saturation | small-data perturbation and exact NSE scaling | analytic initial-boundary family; no fixed-positive-top claim |
| no matching theorem found | eight-source new primary audit plus R0.70H baseline | bounded literature finding only |

## 13. Closed question, open question, and R0.70J

### Closed in R0.70I

- The full direct core square norm reduces to the temporal kernel
  $s^{-1/2}\|\omega\|_2^4$, with exact finite-chain saturation.
- Disjoint time slabs remove scale multiplicity but do not reduce the time
  square to Leray's time integral.
- Under the stated LP hypotheses, the frozen outer low/annular triangular
  paraproduct, its cutoff-shell terms, and its time slabs close absolutely
  using energy, dissipation, and the source square function.
- The frozen low--low term closes, and the isotropic high--high tensor is
  exactly invisible to the trace-free source jet.
- Any outer-scale-free core estimate whose energy/dissipation right side is
  locally bounded near zero is ruled out by a smooth NSE initial-boundary
  scaling family.

### Still open in this route

- The moving-low paraproduct without a $B^{3/2}_{2,1}$ or Carleson input.
- The deviatoric high--high diagonal without the weighted fourth-power norm.
- A direct source--core correlation that avoids separate Hölder norms.
- A cancellation surviving scale-by-scale positive parts.
- A realization or exclusion of the concentration mechanism along one
  solution history at a fixed positive terminal time.

### R0.70J success criterion

The next smallest gate is the **deviatoric diagonal correlation problem**.
Let

\[
 \mathring Q_k
 =W_k\otimes W_k-\frac{|W_k|^2}{3}I.
 \tag{13.1}
\]

R0.70J should compute the exact tensor symbol coupling the exterior harmonic
source coefficient to $\mathring Q_k$, then test whether incompressibility,
angular averaging, or helical polarization produces a signed null structure.
It succeeds if it proves one scale-uniform angular cancellation with the
physical cutoff retained, or constructs a compact smooth source/core family
showing the deviatoric contraction stays positive at the exact critical
weights. A function-space pressure family must not be reported as a dynamic
NSE singularity.

## 14. Reproduction and claim boundary

The exact finite producer is
`research/r070i_temporal_hardy_audit.py`. It checks finite temporal kernels,
the $\alpha=1/4$ exponent, heat and NSE scale maps, dimensional monomials,
the frozen-low scale ledger, and the isotropic trace cancellation.

The journal-style explanatory figure is archived at
`figures/r070i-temporal-hardy/fig-r070i-temporal-hardy/`. It plots closed
formulas only. It is not a numerical PDE simulation, a sampled NSE
trajectory, or a fixed-positive-top counterexample.

The certificate does not computer-prove arbitrary-length geometric sums,
small-data existence, the perturbative lower bound, concentration along one
NSE solution at a fixed positive terminal time, an NSE-specific source--core
no-go theorem, singularity formation, large-data regularity, or the
Millennium problem.
