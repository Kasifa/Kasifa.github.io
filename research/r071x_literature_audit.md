# R0.71X primary-literature audit — data-dependent payments, one-third exponents, zero/level traces, enstrophy growth, and projected Lamb terms

**Status:** bounded primary-source audit for the R0.71X release

**Audit date:** 2026-08-26

**Audit decision:** no direct collision was found in the bounded
primary-source search.  This supports the claim boundary; it is not a novelty
or priority claim.

## 1. Scope and normalization

This audit asks whether the primary literature already proves a
three-dimensional incompressible Navier--Stokes estimate that pays a fixed
temporal level/zero ledger from the initial energy--enstrophy size

\[
 D=\|u_0\|_2^2+\|\omega_0\|_2^2,
 \qquad \omega_0=\operatorname{curl}u_0,
 \tag{1.1}
\]

and, in particular, whether it supplies a universal estimate with a
one-third initial-data exponent such as

\[
 J\lesssim D^{1/3}.
 \tag{1.2}
\]

Here \(J\) denotes the R0.71X type of quantity: a fixed observable is followed
in time, selected level or zero events are isolated, and the ledger records a
weighted contribution involving the derivative at those events.  The exact
R0.71X definition is internal to the project.  The literature comparison below
uses only the structural features just listed and does not attribute that
definition to an external paper.

The bounded search covered:

1. estimates depending on initial kinetic energy and enstrophy;
2. cubic enstrophy-growth inequalities and finite-time amplification;
3. the Leray-projected Lamb nonlinearity;
4. classical occurrences of a one-third exponent;
5. spatial level-set and vorticity trace estimates; and
6. time analyticity and what it does, and does not, imply about zeros.

Normalization is a material issue.  The sources use at least three different
conventions:

\[
 K=\frac12\|u\|_2^2,
 \qquad E=\frac12\|\omega\|_2^2,
 \tag{1.3}
\]

\[
 \mathcal E=\frac12\|\omega\|_2^2,
 \tag{1.4}
\]

or

\[
 E=\|\omega\|_2^2=\|\nabla u\|_2^2.
 \tag{1.5}
\]

Constants are quoted only with the source's stated convention.  Whole-space
constants are not silently transferred to the torus.

All principal sources below are published journal articles.  Where an arXiv
link is included, it is identified as an author preprint for access to the
paper's text; no result is classified as published merely because an arXiv
version exists.  No preprint-only global-regularity claim is used.

## 2. Claim-to-source ledger

| Candidate claim or dependency | Primary source checked | What the source directly supports | Collision decision for R0.71X |
|---|---|---|---|
| Initial kinetic energy plus enstrophy gives an explicit data-dependent estimate | [Miller 2020](https://doi.org/10.1088/1361-6544/ab9246) | On \(\mathbb R^3\), a cubic enstrophy ODE, an explicit local lifespan, and a small \(K_0E_0\) global-smoothness threshold | Supports \(D^{-2}\) lifespan and small-data baselines; does not support \(D^{1/3}\) zero payment |
| Incompressibility lowers the instantaneous cubic enstrophy exponent | [Lu--Doering 2008](https://doi.org/10.1512/iumj.2008.57.3716), [journal record](https://iumj.org/article/4718/) | Numerical variational maximizers among divergence-free periodic fields saturate the \(E^3\) instantaneous exponent up to a prefactor | Negative for exponent reduction; no temporal zero ledger |
| Finite-time Navier--Stokes trajectories realize the cubic ODE growth | [Ayala--Protas 2017](https://doi.org/10.1017/jfm.2017.136), [Kang--Yun--Protas 2020](https://doi.org/10.1017/jfm.2020.204) | Instantaneous extreme growth is rapidly depleted; computed finite-time local maximizers exhibit approximately \(\mathcal E_0^{3/2}\) amplification | Computational evidence only, not a theorem paying \(J\) from \(D\) |
| The projected Lamb term has an exact determinant/Sobolev balance | [Lerner--Vigneron 2022](https://doi.org/10.4208/cmr.2021-0106), [publisher full text](https://global-sci.com/article/81500/download) | Exact curl form, projected cross-product identity, determinant weak form, enstrophy balance, and \(\dot H^\theta\) balances | Directly supports the algebraic dependency; contains no \(D^{1/3}\) level/zero estimate |
| A classical Navier--Stokes theorem already has the exponent \(1/3\) | [Foias--Guillopé--Temam 1981](https://doi.org/10.1080/03605308108820180) | For periodic 3D Leray weak solutions, the higher-derivative hierarchy includes \(H_2^{1/3}\in L_t^1\) | Non-collision: this is a time-integrability exponent of \(H_2\), not an initial-data exponent of \(D\) |
| Level-set geometry controls the relevant temporal zero ledger | [Constantin 1990](https://doi.org/10.1007/BF02096982) | Bounds an average spatial Hausdorff measure of vorticity-magnitude level sets using coarea/geometric measure arguments | Spatial level average, not fixed temporal zeros or squared slopes |
| Energy pays a vorticity trace estimate | [Yang 2025](https://doi.org/10.1016/j.jde.2025.113486), [author preprint](https://arxiv.org/abs/2308.09350) | Weak-Lorentz spacetime and lower-dimensional spatial traces paid by \(\|\nabla u\|_{L^2_{t,x}}^2\), hence by initial kinetic energy | Strong spatial trace theorem, but no temporal zero count or zero-slope ledger |
| Time analyticity quantitatively controls all zeros from \(D\) | [Wang--Gao--Xue 2022](https://doi.org/10.1016/j.jmaa.2022.126428), [author preprint](https://arxiv.org/abs/2112.03079) | Joint space--time analyticity and explicit derivative smoothing for mild solutions from \(L^3\) data on \(\mathbb R^3\) | Gives isolated zeros unless the observable is identically zero; gives no \(D\)-only zero count or slope sum |

## 3. Initial-data payments actually proved

### 3.1 Miller: explicit whole-space energy--enstrophy estimates

Published source: Evan Miller, “Global regularity for solutions of the three
dimensional Navier--Stokes equation with almost two dimensional initial
data,” *Nonlinearity* 33 (2020), 5272--5323,
[DOI](https://doi.org/10.1088/1361-6544/ab9246),
[author preprint](https://arxiv.org/abs/1909.09125).

The paper works on \(\mathbb R^3\) and defines

\[
 K(t)=\frac12\|u(t)\|_2^2,
 \qquad
 E(t)=\frac12\|\omega(t)\|_2^2=\|S(t)\|_2^2,
 \tag{3.1}
\]

where \(S=\nabla_{\rm sym}u\).  Proposition 2.1 states

\[
 \partial_t\|S\|_2^2
 =-2\nu\|S\|_{\dot H^1}^2
 -4\int_{\mathbb R^3}\det S\,dx.
 \tag{3.2}
\]

Proposition 2.4 gives

\[
 E'(t)\le \frac{1}{3456\pi^4\nu^3}E(t)^3,
 \qquad
 K'(t)=-2\nu E(t).
 \tag{3.3}
\]

Proposition 2.6 gives the explicit sufficient condition

\[
 K_0E_0<6912\pi^4\nu^4
 \quad\Longrightarrow\quad
 T_{\max}=+\infty,
 \tag{3.4}
\]

and the global bound

\[
 E(t)\le
 \frac{E_0}{1-K_0E_0/(6912\pi^4\nu^4)}.
 \tag{3.5}
\]

Proposition 2.9 gives

\[
 E(t)\le
 \frac{E_0}
 {\sqrt{1-E_0^2t/(1728\pi^4\nu^3)}}
 \tag{3.6}
\]

for

\[
 0<t<\frac{1728\pi^4\nu^3}{E_0^2},
 \qquad
 T_{\max}\ge\frac{1728\pi^4\nu^3}{E_0^2}.
 \tag{3.7}
\]

For the R0.71X normalization

\[
 D=\|u_0\|_2^2+\|\omega_0\|_2^2=2(K_0+E_0),
 \tag{3.8}
\]

the elementary consequences are

\[
 E_0\le\frac D2,
 \qquad
 K_0E_0\le\left(\frac D4\right)^2,
 \tag{3.9}
\]

and therefore

\[
 T_{\max}\ge\frac{6912\pi^4\nu^3}{D^2},
 \tag{3.10}
\]

while

\[
 D<192\sqrt3\,\pi^2\nu^2
 \tag{3.11}
\]

is a sufficient \(D\)-only condition for (3.4).

#### Direct-support boundary

The source directly supports (3.2)--(3.7) on \(\mathbb R^3\).  Equations
(3.8)--(3.11) are explicit algebraic consequences recorded for comparison
with R0.71X.  The source does not define the R0.71X ledger, select temporal
zeros, or state a \(D^{1/3}\) estimate.  The constants depend on sharp
whole-space Sobolev inequalities and must not be quoted as periodic constants.

### 3.2 Lu--Doering: cubic instantaneous growth remains attainable under incompressibility

Published source: Lu Lu and Charles R. Doering, “Limits on Enstrophy Growth
for Solutions of the Three-dimensional Navier--Stokes Equations,” *Indiana
University Mathematics Journal* 57 (2008), 2693--2728,
[DOI](https://doi.org/10.1512/iumj.2008.57.3716),
[journal record](https://iumj.org/article/4718/).

The paper works on the periodic box \(\Omega=[0,L]^3\) and uses

\[
 E=\|\omega\|_2^2=\|\nabla u\|_2^2
 \tag{3.12}
\]

without a factor \(1/2\).  Equations (1.14)--(1.17) give

\[
 \left|\int_\Omega u\cdot\nabla u\cdot\Delta u\,dx\right|
 \le c\|\Delta u\|_2^{3/2}\|\nabla u\|_2^{3/2},
 \qquad c=\frac{2.2}{\pi},
 \tag{3.13}
\]

and

\[
 \frac{dE}{dt}
 \le \frac{27c^3}{128\nu^3}E^3.
 \tag{3.14}
\]

They formulate a constrained variational problem for the largest instantaneous
enstrophy-production rate at prescribed \(E\).  Their computed divergence-free
maximizers scale cubically in \(E\), up to a much smaller numerical prefactor.

#### Direct-support boundary

The analytic inequality (3.14) is rigorous.  Saturation of its exponent is a
numerical variational conclusion about instantaneous divergence-free fields.
Neither statement proves that a single Navier--Stokes trajectory sustains cubic
growth on a finite time interval.  Neither involves temporal zeros or a
\(D^{1/3}\) payment.

### 3.3 Ayala--Protas and Kang--Yun--Protas: finite-time computational evidence

Published sources:

- Diego Ayala and Bartosz Protas, “Extreme Vortex States and the Growth of
  Enstrophy in Three-dimensional Incompressible Flows,” *Journal of Fluid
  Mechanics* 818 (2017), 772--806,
  [DOI](https://doi.org/10.1017/jfm.2017.136),
  [author preprint](https://arxiv.org/abs/1605.05742);
- Di Kang, Dongfang Yun, and Bartosz Protas, “Maximum amplification of
  enstrophy in three-dimensional Navier--Stokes flows,” *Journal of Fluid
  Mechanics* 893 (2020), A22,
  [DOI](https://doi.org/10.1017/jfm.2020.204),
  [author preprint](https://arxiv.org/abs/1909.00041).

Kang--Yun--Protas work on the unit periodic cube, take \(\nu=0.01\), and use

\[
 \mathcal E(u)=\frac12\|\omega\|_2^2.
 \tag{3.15}
\]

Their equation (10) records the standard cubic estimate

\[
 \frac{d\mathcal E}{dt}
 \le\frac{27}{8\pi^4\nu^3}\mathcal E^3,
 \tag{3.16}
\]

whose integrated form, equation (11), is

\[
 \mathcal E(t)\le
 \frac{\mathcal E_0}
 {\sqrt{1-\frac{27}{4\pi^4\nu^3}\mathcal E_0^2t}}.
 \tag{3.17}
\]

Problem 3.1 maximizes \(\mathcal E(u(T))\) over divergence-free \(H^1\) initial
data with prescribed \(\mathcal E_0\), conditional on smooth existence over the
optimization window.  For the computed asymmetric branch and
\(100\le\mathcal E_0\le1000\), equation (29) gives the numerical fit

\[
 \max_{T>0}\mathcal E(T)
 \sim(0.224\pm0.006)\mathcal E_0^{1.490\pm0.004},
 \tag{3.18}
\]

and equation (30) gives, for sufficiently large \(\mathcal E_0\),

\[
 \widetilde T
 \sim(4.0\pm1.1)\mathcal E_0^{-0.51\pm0.04}.
 \tag{3.19}
\]

The authors explicitly state that the gradient optimization locates local
maximizers and cannot guarantee global maximizers.  Ayala--Protas likewise show
that fields saturating the instantaneous cubic power undergo immediate
depletion rather than sustained ODE saturation.

#### Direct-support boundary

Equations (3.18)--(3.19) are computational fits, not a priori theorems.  The
approximately \(3/2\) amplification exponent is distinct both from the FGT
time-integrability exponent below and from the R0.71X initial-data exponent
\(1/3\).

## 4. The projected Lamb term

### 4.1 Exact curl and determinant identities

Published source: Nicolas Lerner and François Vigneron, “On Some Properties
of the Curl Operator and Their Consequences for the Navier--Stokes System,”
*Communications in Mathematical Research* 38 (2022), 449--497,
[DOI](https://doi.org/10.4208/cmr.2021-0106),
[publisher full text](https://global-sci.com/article/81500/download),
[author preprint](https://arxiv.org/abs/2203.07950).

On \(\mathbb R^3\), let \(C=\operatorname{curl}\).  Equations (26), (28)--(31)
state

\[
 \mathbb P=|D|^{-2}C^2
 =I+\nabla(-\Delta)^{-1}\operatorname{div},
 \tag{4.1}
\]

\[
 (Cu)\times u
 =(u\cdot\nabla)u-\frac12\nabla|u|^2,
 \tag{4.2}
\]

\[
 \mathbb P((u\cdot\nabla)u)
 =\mathbb P((Cu)\times u),
 \tag{4.3}
\]

\[
 \partial_tu+\mathbb P((Cu)\times u)+\nu C^2u=0,
 \tag{4.4}
\]

and, for divergence-free \(w\),

\[
 \langle (u\cdot\nabla)u,w\rangle
 =\int_{\mathbb R^3}\det(Cu,u,w)\,dx.
 \tag{4.5}
\]

Equation (69) is the exact enstrophy balance

\[
 \begin{aligned}
 \|\omega(t)\|_2^2
 &+2\nu\int_0^t\|C\omega(s)\|_2^2\,ds\\
 &+2\int_0^t\int_{\mathbb R^3}
 \det(u,Cu,\Delta u)\,dx\,ds
 =\|\omega_0\|_2^2.
 \end{aligned}
 \tag{4.6}
\]

Proposition 27, equation (80), gives for every \(\theta>0\)

\[
 \begin{aligned}
 \|u(t)\|_{\dot H^\theta}^2
 &+2\nu\int_0^t\|u(s)\|_{\dot H^{\theta+1}}^2\,ds\\
 &+2\int_0^t\int_{\mathbb R^3}
 \det(Cu,u,|D|^{2\theta}u)\,dx\,ds
 =\|u_0\|_{\dot H^\theta}^2.
 \end{aligned}
 \tag{4.7}
\]

The sign convention matters.  Lerner--Vigneron use

\[
 (Cu)\times u=\omega\times u,
 \tag{4.8}
\]

whereas the R0.71X convention is \(u\times\omega\); the two cross-products
differ by a minus sign.

### 4.2 Generic energy-level consequence

For the R0.71X convention

\[
 L=\mathbb P(u\times\omega),
 \tag{4.9}
\]

Sobolev duality, Hölder, and interpolation give on a fixed periodic domain

\[
 \begin{aligned}
 \|L\|_{\dot H^{-1}}
 &\lesssim\|u\times\omega\|_{6/5}\\
 &\le\|u\|_3\|\omega\|_2\\
 &\lesssim\|u\|_2^{1/2}\|\omega\|_2^{3/2}.
 \end{aligned}
 \tag{4.10}
\]

Consequently, at the initial time,

\[
 \frac{\|L_0\|_{\dot H^{-1}}^2}{\|\omega_0\|_2^2}
 \lesssim
 \|u_0\|_2\|\omega_0\|_2
 \le\frac D2.
 \tag{4.11}
\]

Equations (4.10)--(4.11) are direct standard consequences of the exact
projected identity, not a theorem quoted verbatim from Lerner--Vigneron.
They show the generic energy-level scale available without exploiting the
special R0.71X temporal-zero geometry: it is \(O(D)\), not
\(O(D^{1/3})\).

#### Direct-support boundary

The source supplies the exact projection, cross-product, determinant, and
Sobolev-balance identities.  It does not supply a count of temporal zeros, a
trace at those zeros, or a \(D^{1/3}\) estimate for the projected Lamb term.

## 5. The genuine Foias--Guillopé--Temam one-third exponent

Published source: Ciprian Foias, Colette Guillopé, and Roger Temam, “New a
priori estimates for Navier--Stokes equations in dimension 3,”
*Communications in Partial Differential Equations* 6 (1981), 329--359,
[publisher record and DOI](https://doi.org/10.1080/03605308108820180).

For three-dimensional periodic Leray weak solutions, define the squared
higher-derivative quantities

\[
 H_n(t)=\int_\Omega|\nabla^n u(t,x)|^2\,dx.
 \tag{5.1}
\]

The paper's a priori hierarchy gives, on finite time intervals and under its
stated data/forcing assumptions,

\[
 \int_0^T H_n(t)^{1/(2n-1)}\,dt<\infty.
 \tag{5.2}
\]

For \(n=2\), this is

\[
 \int_0^T H_2(t)^{1/3}\,dt<\infty,
 \qquad
 H_2(t)=\|\nabla^2u(t)\|_2^2.
 \tag{5.3}
\]

The objects and exponents in (5.3) must be read literally:

| Feature | FGT statement | R0.71X candidate |
|---|---|---|
| Quantity raised to \(1/3\) | The time-dependent squared higher-derivative norm \(H_2(t)\) | The initial data size \(D\) |
| Operation | Integration over all regular times, \(\int_0^T\cdot\,dt\) | Payment of a selected level/zero-event ledger |
| Information about zeros | None | Zero location and derivative enter the definition of \(J\) |
| Domain of conclusion | Periodic Leray weak solutions, with the paper's data/forcing hypotheses | The specific R0.71X triangular mechanism, and any later proposed PDE theorem |

Thus

\[
 H_2^{1/3}\in L_t^1
 \tag{5.4}
\]

is not a result of the form

\[
 J\lesssim
 \bigl(\|u_0\|_2^2+\|\omega_0\|_2^2\bigr)^{1/3}.
 \tag{5.5}
\]

No algebraic relabelling converts (5.3) into (5.5).  Any use of FGT in an
R0.71X proof would require a new bridge from the global-in-time integral of a
higher spatial derivative to the particular temporal level/zero ledger.

#### Direct-support boundary

The primary paper supports the hierarchy (5.2), including (5.3).  It does not
state the R0.71X zero functional and does not establish a one-third power of
the initial energy--enstrophy size.

## 6. Spatial level and trace results

### 6.1 Constantin: averaged spatial level-set area

Published source: Peter Constantin, “Navier--Stokes equations and area of
interfaces,” *Communications in Mathematical Physics* 129 (1990), 241--266,
[DOI](https://doi.org/10.1007/BF02096982).

The paper proves new vorticity estimates, constructs global Leray weak
solutions satisfying them, and combines the estimates with geometric measure
theory to control an average two-dimensional Hausdorff measure of spatial level
sets of \(|\omega|\).  In the paper's turbulence variables, the advertised
average-area estimate has the form

\[
 \langle\mu\rangle
 \le \frac{L^3}{\eta}
 \left(1+\operatorname{Re}^{-1/2}\right)^{1/2}.
 \tag{6.1}
\]

It also establishes an a priori \(L^1\) vorticity bound and time-averaged
integrability of \(\nabla\omega\) with exponent \(4/(3+\varepsilon)\).

#### Direct-support boundary

The level parameter in this source is a spatial value of vorticity magnitude,
and the estimate averages the spatial level-set area using coarea/geometric
measure arguments.  It is not a theorem about the zeros of one scalar temporal
observable.  In particular it does not bound the number of such zeros or a sum
of their squared slopes.

### 6.2 Yang: energy-paid spatial traces

Published source: Jincheng Yang, “Vorticity interior trace estimates and
higher derivative estimates via blow-up method,” *Journal of Differential
Equations* 442 (2025), article 113486,
[DOI](https://doi.org/10.1016/j.jde.2025.113486),
[author preprint](https://arxiv.org/abs/2308.09350).

The viscosity is normalized to one.  Theorem 1.1 permits a uniformly
Lipschitz domain, including the periodic cube alternative, and a time-dependent
\(d\)-dimensional Lipschitz graph \(\Gamma_t\).  It produces a measurable scale
\(s_1\) such that

\[
 |\nabla^n\omega(t,x)|\le C_ns_1(t,x)^{-n-2}
 \tag{6.2}
\]

and

\[
 \left\|s_1^{-1}\mathbf1_{\{s_1<r_*\}}\right\|_
 {L^{d+1,\infty}(\Gamma_T)}^{d+1}
 \le C_L\|\nabla u\|_{L^2(\Omega_T)}^2.
 \tag{6.3}
\]

Corollary 1.2 gives for suitable weak solutions on a bounded domain

\[
 \left\|
 \nabla\omega\,
 \mathbf1_{\{|\nabla\omega|>Cr_*^{-3}\}}
 \right\|_{L^{4/3,\infty}(\Omega_T)}^{4/3}
 \le C_L\|\nabla u\|_{L^2(\Omega_T)}^2,
 \tag{6.4}
\]

and, for a two-dimensional graph,

\[
 \left\|
 \omega\,
 \mathbf1_{\{|\omega|>Cr_*^{-2}\}}
 \right\|_{L^{3/2,\infty}(\Gamma_T)}^{3/2}
 \le C_L\|\nabla u\|_{L^2(\Omega_T)}^2.
 \tag{6.5}
\]

The energy inequality pays the right-hand side from initial kinetic energy:

\[
 \frac12\|u(T)\|_2^2
 +\|\nabla u\|_{L^2(\Omega_T)}^2
 \le\frac12\|u(0)\|_2^2.
 \tag{6.6}
\]

#### Direct-support boundary

Equations (6.3)--(6.5) are spatial or spacetime Lorentz trace estimates on
Lipschitz graphs and high-value sets.  The exponents \(4/3\) and \(3/2\) are
Lebesgue/Lorentz exponents; they are not powers of \(D\).  The theorem does not
sample a temporal observable at its zero set and does not estimate zero slopes.

## 7. Time analyticity and the zero-set boundary

Published source: Zhuo Wang, Wei Gao, and Jiao Xue, “Joint space-time
analyticity of mild solutions to the Navier--Stokes equations,” *Journal of
Mathematical Analysis and Applications* 515 (2022), article 126428,
[DOI](https://doi.org/10.1016/j.jmaa.2022.126428),
[author preprint](https://arxiv.org/abs/2112.03079).

Theorem 1.1 considers divergence-free \(u_0\in L^3(\mathbb R^3)\) and the
corresponding mild solution.  For \(3\le q\le\infty\), \(t\in(0,T]\), and
\(|\beta|+k>0\), it proves an estimate of the form

\[
 \|D_x^\beta\partial_t^ku(t)\|_{L^q}
 \le
 M^{|\beta|+k}(|\beta|+k)^{|\beta|+k}
 t^{-\frac{|\beta|}{2}-k-\frac32(\frac13-\frac1q)}.
 \tag{7.1}
\]

The solution is jointly analytic in space and time for positive times.  Hence,
when a continuous linear observable of the solution is analytic in time, its
zeros are isolated on an interior interval unless the observable vanishes
identically.  This last zero-set statement is the elementary identity theorem
for analytic functions, not an additional Navier--Stokes theorem quoted from
the paper.

Analyticity alone does not provide:

1. a \(D\)-only bound for the number of zeros;
2. a lower bound preventing the observable from being uniformly tiny;
3. a \(D\)-only complex-disc growth ratio suitable for Jensen's formula; or
4. a bound for a weighted sum of \(|f'(t_j)|^2\) at the zeros.

The domain is \(\mathbb R^3\), not the periodic box.  R0.71X's explicit
finite-mode family is already analytic, so this source supports only the
qualitative isolated-zero boundary, not the desired quantitative payment.

## 8. Non-collision boundary for R0.71X

The primary sources separate into four established mechanisms:

\[
 \text{cubic enstrophy ODE}
 \Longrightarrow
 \text{local lifespan of order }D^{-2}
 \text{ and small-data thresholds},
 \tag{8.1}
\]

\[
 H_2^{1/3}\in L_t^1
 \Longrightarrow
 \text{time integrability of a higher spatial derivative},
 \tag{8.2}
\]

\[
 \text{spatial coarea/Lorentz trace}
 \Longrightarrow
 \text{averaged spatial level or graph control},
 \tag{8.3}
\]

and

\[
 \text{time analyticity}
 \Longrightarrow
 \text{qualitative isolation of nontrivial zeros}.
 \tag{8.4}
\]

None of (8.1)--(8.4) gives the missing composite implication

\[
 \text{initial }D
 \Longrightarrow
 \text{quantitative fixed temporal zero trace}
 \Longrightarrow
 J\lesssim D^{1/3}.
 \tag{8.5}
\]

For the current R0.71X triangular family, the internal scaling under audit is

\[
 D_q\asymp A_q^2q^2,
 \qquad
 J_q\asymp\frac{A_q^2}{q^2}.
 \tag{8.6}
\]

Therefore

\[
 \frac{J_q^3}{D_q}
 \asymp\left(\frac{A_q}{q^2}\right)^4.
 \tag{8.7}
\]

If the uniform implicit-function regime imposes \(A_q\lesssim q^2\), then
(8.7) yields the mechanism-specific estimate

\[
 J_q\lesssim D_q^{1/3}.
 \tag{8.8}
\]

This algebra is internal to R0.71X.  Its present safe interpretation is:

> one third is an endpoint of the uniform triangular/IFT construction,
> rather than a universal Navier--Stokes exponent supplied by the checked
> literature.

An eventual article may describe a rigorously certified version of (8.8) as
an internal endpoint barrier or saturation law for that construction.  It must
not describe it as a general three-dimensional Navier--Stokes theorem unless a
new argument proves (8.5) for the stated PDE solution class.

## 9. Safe claims and prohibited upgrades

### Directly supported or elementary consequences

- the exact Miller cubic enstrophy inequality, lifespan, and
  energy--enstrophy smallness condition on \(\mathbb R^3\);
- the algebraic \(D\)-only consequences (3.10)--(3.11), with their domain
  and normalization stated;
- the Lu--Doering cubic instantaneous exponent and its computational
  divergence-free saturation;
- the Kang--Yun--Protas finite-time computational fits, explicitly labelled
  local-maximizer evidence;
- the Lerner--Vigneron projected Lamb and determinant identities;
- the standard \(H^{-1}\) consequence (4.10)--(4.11), labelled as a
  derivation rather than a quoted theorem;
- the FGT hierarchy \(H_n^{1/(2n-1)}\in L_t^1\), in particular
  \(H_2^{1/3}\in L_t^1\);
- the Constantin spatial level-average result;
- the Yang energy-paid spatial trace estimates; and
- qualitative isolation of nontrivial temporal zeros under analyticity.

### Not supported by the checked sources

- a universal deterministic estimate \(J\lesssim D^{1/3}\);
- a \(D\)-only bound on the number of temporal zeros of a fixed Fourier
  observable;
- a \(D\)-only bound on a sum of squared slopes at those zeros;
- identification of the FGT exponent with the R0.71X initial-data exponent;
- treating the Lorentz exponents \(4/3\) or \(3/2\) as powers of \(D\);
- upgrading numerical enstrophy optimization to a theorem about global
  maximizers or global regularity; or
- transferring whole-space sharp constants unchanged to \(\mathbb T^3\).

## 10. Search boundary and nonexistence disclaimer

This was a bounded primary-source audit, not a systematic all-language
bibliographic or priority search.  It checked the named journal articles,
their DOI/publisher records, and author preprints where listed.  Search terms
and source trails included combinations of:

- Navier--Stokes initial energy and enstrophy estimates;
- enstrophy growth and maximum amplification;
- one-third exponent and higher-derivative a priori estimates;
- vorticity level sets, interior trace, and Lipschitz-graph trace;
- time analyticity and zero sets;
- Lamb vector, curl form, Leray projection, determinant balances; and
- \(H^{-1}\) control of the projected quadratic nonlinearity.

The search did not locate a published primary theorem matching (8.5).  The
correct conclusion is

> **no direct collision was identified in the bounded checked corpus.**

It is not correct to conclude that no such theorem exists anywhere.  In
particular, this file does not establish novelty, priority, or exhaustive
coverage of MathSciNet, zbMATH, dissertations, non-English literature,
conference proceedings, or papers using different terminology.  Before any
submission-level novelty claim, the search should be expanded around the final
exact definition of \(J\), its temporal trace measure, its Fourier observable,
and its normalization.  Until then, R0.71X must use “not found in the bounded
primary-source audit,” not “absent from the literature.”
