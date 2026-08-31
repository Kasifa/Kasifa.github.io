# R0.73T independent no-go and scaling audit

**Question audited:** can the instantaneous evolution of
\(Q=\|u\|_4^4\), or its pressure contribution, be controlled from only
the scalar autocorrelation data

\[
 \mathcal E=\|u\|_2^2=C(0),\qquad
 C(h)=\widehat{|u|^2}(h),\qquad
 Q=\sum_h|C(h)|^2,\qquad
 A=\sum_h|C(h)|,
\]

the support count \(D_C=|\operatorname {supp}C|\), or finitely many
preselected \(C(h)\)?

**Verdict:** there are two different answers which must not be conflated.

1. `EXACT_POSITIVE`: viscosity permits a **one-sided** differential
   inequality
   \[
    {dQ\over dt}\lesssim_\nu A Q
    \le Q\min\{M\mathcal E,\sqrt{D_CQ}\}
   \]
   for finite Fourier/Wiener data.  A weaker standard bound uses \(Q\)
   alone.  Thus there is no valid no-go against every upper estimate for the
   full derivative.
2. `EXACT_NO_GO`: the isolated pressure contribution, the exact value of
   \(dQ/dt\), and any two-sided or absolute-value bound are not determined
   by these zero-order summaries.  A six-mode, real, divergence-free
   fixed-ratio-annular family below has fixed
   \((\mathcal E,Q,A,D_C)\) but pressure contribution of size \(384L\).
   A shear family has the same four summaries for every \(L\), while
   \(|dQ/dt|=(3/2)\nu L^2\).

These are finite Fourier statements at one time.  They are not a blow-up
construction and do not settle a Navier--Stokes regularity question.

## 1. Exact evolution identity

Use normalized Haar measure on \(\mathbb T^3\), viscosity \(\nu>0\), and

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0.
 \tag{1.1}
\]

Put

\[
 w=|u|^2,\qquad
 X^2=\|\nabla w\|_2^2,\qquad
 Y=\int_{\mathbb T^3}w|\nabla u|^2.
 \tag{1.2}
\]

The scalar equation is

\[
 \partial_tw+u\cdot\nabla w+2u\cdot\nabla p
 =\nu\Delta w-2\nu|\nabla u|^2.
 \tag{1.3}
\]

Multiplication by \(2w\), periodic integration, and
\(\nabla\cdot u=0\) give the exact identity

\[
 \boxed{
 {dQ\over dt}
 =-4\nu Y-2\nu X^2+\mathcal N_4(u),
 \qquad
 \mathcal N_4(u):=-4\int w\,u\cdot\nabla p
 =4\int p\,u\cdot\nabla w.}
 \tag{1.4}
\]

The apparent quartic transport term cancels exactly.  The only sign-odd
nonlinear contribution in (1.4) is the pressure term \(\mathcal N_4\).
It is quintic under amplitude scaling and contains one spatial derivative.

## 2. The positive result that survives the audit

Let \(C_R\) be the \(L^3(\mathbb T^3)\) norm of the periodic double-Riesz
pressure operator, with the harmless component sum absorbed into the
constant.  Since

\[
 p=R_iR_j(u_i u_j),
 \qquad
 \|p\|_3\le C_R\|u\|_6^2,
 \tag{2.1}
\]

Hölder and Young give

\[
\begin{aligned}
 |\mathcal N_4(u)|
 &\le4C_R\|u\|_6^3X\\
 &\le\nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
\end{aligned}
 \tag{2.2}
\]

The second line uses \(2ab\le a^2+b^2\) with
\(a=\sqrt\nu X\) and
\(b=2C_R\nu^{-1/2}\|u\|_6^3\).  Thus the coefficient
\(4C_R^2/\nu\) and the one remaining copy of \(\nu X^2\) below have no
hidden normalization loss.

Consequently

\[
 \boxed{
 {dQ\over dt}+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}\|u\|_6^6
 \le {4C_R^2\over\nu}AQ.}
 \tag{2.3}
\]

The last inequality is exactly the classical R0.73S autocorrelation
certificate \(\|u\|_6^6\le AQ\).  If \(u\) has \(M\) Fourier sites and
\(C\) has finite support, then

\[
 A\le M\mathcal E,
 \qquad
 A\le\sqrt{D_CQ},
 \tag{2.4}
\]

so

\[
 {dQ\over dt}
 \le {4C_R^2\over\nu}
 Q\min\{M\mathcal E,\sqrt{D_CQ}\}.
 \tag{2.5}
\]

For a general field, (2.3) has content only under the explicit Wiener
condition

\[
 |u|^2\in\mathcal A(\mathbb T^3),
 \qquad
 \||u|^2\|_{\mathcal A}
 :=\sum_h|\widehat{|u|^2}(h)|=A<\infty.
 \tag{2.6}
\]

Trigonometric polynomials satisfy (2.6), and
\(|u|^2\in H^s(\mathbb T^3)\) with \(s>3/2\) is a sufficient condition.
In particular, the smooth/H3 regime under study has pointwise finite
\(A(t)\), but no uniform or time-integrated bound follows from smoothness
up to a possibly finite maximal time.  If \(A=\infty\), (2.3) is only a
formal inequality with a vacuous right side.

This is a genuine dynamic use of the R0.73S static certificate, but it is
not a global closure.  For the full PDE, \(M\) and \(D_C\) need not stay
finite or bounded, and (2.3) still needs time control of \(A(t)\).  In
particular, (2.3) would yield a Gronwall bound if
\(\int_0^T A(t)\,dt<\infty\); the audit does not prove that hypothesis.

That missing hypothesis is scaling-critical, not a lower-order bonus.  For
the Navier--Stokes rescaling

\[
 u^{[\lambda]}(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{2.7}
\]

with integer \(\lambda\) on the fixed torus (or the usual rescaling on
\(\mathbb R^3\)),

\[
 A^{[\lambda]}(t)=\lambda^2A(\lambda^2t),
 \qquad
 \int_0^{T/\lambda^2}A^{[\lambda]}(t)\,dt
 =\int_0^TA(s)\,ds.
 \tag{2.8}
\]

Moreover Fourier inversion gives

\[
 \|u(t)\|_\infty^2=\||u(t)|^2\|_\infty\le A(t).
 \tag{2.9}
\]

Thus \(A\in L_t^1\) implies the critical
\(u\in L_t^2L_x^\infty\) condition.  Controlling \(\int A\) for arbitrary
energy data would be at least as demanding as producing this classical
critical spacetime control; (2.3) does not supply it.

There is also a weaker classical one-sided estimate from \(Q\) alone.  The
torus Gagliardo--Nirenberg inequality applied to \(w\) gives

\[
 \|u\|_6^6=\|w\|_3^3
 \le C\bigl(Q^{3/4}X^{3/2}+Q^{3/2}\bigr).
 \tag{2.10}
\]

Substituting (2.10) into the first line of (2.2), then using Young with
exponents \((8/7,8)\) and \((2,2)\), yields constants
\(c_\nu,C_\nu>0\) such that

\[
 {dQ\over dt}+4\nu Y+c_\nu X^2
 \le C_\nu\bigl(Q^3+Q^{3/2}\bigr).
 \tag{2.11}
\]

Thus “\(Q\) cannot upper-control \(dQ/dt\) at all” would be false.  The
comparison ODE in (2.11) can itself blow up, so this standard local estimate
does not imply global regularity.

## 3. Exact six-mode pressure obstruction

Let \(x=x_1\), \(y=x_2\), and define

\[
 u(x,y)=
 \bigl(6\sin y-4\sin(x+y),\;
       4\sin x+4\sin(x+y),\;0\bigr).
 \tag{3.1}
\]

This field is real, mean zero, divergence free, and has the six Fourier
sites

\[
 \pm(1,0,0),\qquad \pm(0,1,0),\qquad \pm(1,1,0).
\]

It is a planar two-dimensional solution class embedded in three dimensions.
That is enough for an information/scaling obstruction, but it deliberately
does not probe three-dimensional vortex stretching.

For the normalization used throughout this repository,

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu(x),
 \qquad \int_{\mathbb T^3}1\,d\mu=1.
 \tag{3.2}
\]

Taking divergence of (1.1) gives
\(\Delta p=-\partial_i\partial_j(u_i u_j)\); hence, for \(n\ne0\),

\[
 \widehat p(n)
 =-{n_i n_j\over|n|^2}
   \sum_k\widehat u_i(k)\widehat u_j(n-k).
 \tag{3.3}
\]

Equations (3.2)--(3.3) fix both the Fourier sign and the absence of any
\((2\pi)^3\) volume factor in the calculations below.

Its nonzero scalar autocorrelation coefficients are the following exact
integers.

| shifts \(h\) | \(C(h)\) |
| --- | ---: |
| \(0\) | \(42\) |
| \(\pm(1,0,0)\) | \(-12\) |
| \(\pm(0,1,0)\) | \(8\) |
| \(\pm(2,0,0)\) | \(-4\) |
| \(\pm(0,2,0)\) | \(-9\) |
| \(\pm(2,1,0)\) | \(-8\) |
| \(\pm(1,2,0)\) | \(12\) |
| \(\pm(2,2,0)\) | \(-8\) |

Therefore

\[
 \boxed{
 \mathcal E=42,\qquad Q=2918,\qquad A=164,\qquad D_C=15.}
 \tag{3.4}
\]

The mean-zero pressure solving
\(-\Delta p=\partial_i\partial_j(u_i u_j)\) is

\[
\begin{aligned}
 p={}&24\cos x-16\cos y
 +12\cos(x+y)+12\cos(x-y)\\
 &-{16\over5}\cos(2x+y)
 +{24\over5}\cos(x+2y).
\end{aligned}
 \tag{3.5}
\]

Direct finite Fourier convolution gives

\[
 \int |u|^2u\cdot\nabla p=96,
 \qquad
 \boxed{\mathcal N_4(u)=-384.}
 \tag{3.6}
\]

This value can be checked using only the eight rows of \(C\) above and the
six conjugate pairs of pressure coefficients in (3.5).  No numerical
quadrature or limiting argument is involved.

For any integer \(L\ge1\), put

\[
 u_L(x)=u(Lx).
 \tag{3.7}
\]

Then \(u_L\) remains real, mean zero, and divergence free, and all its
Fourier sites lie in the fixed-ratio annulus

\[
 L\le|k|\le\sqrt2L.
 \tag{3.8}
\]

The map \(x\mapsto Lx\) preserves normalized Haar measure and

\[
 C_{u_L}(Lh)=C_u(h),\qquad C_{u_L}(n)=0\quad(n\notin L\mathbb Z^3).
 \tag{3.9}
\]

Hence the four numbers in (3.4) are independent of \(L\), whereas
\(p_L(x)=p(Lx)\) and

\[
 \boxed{\mathcal N_4(u_L)=-384L.}
 \tag{3.10}
\]

This is an unchanged-amplitude dilation used to compare instantaneous
data; it is not the amplitude-rescaled Navier--Stokes symmetry (2.7).

This disproves any finite-valued bound for
\(|\mathcal N_4|\) depending only on
\((\mathcal E,Q,A,D_C)\).  If \(H\subset\mathbb Z^3\) is any predeclared
finite shift set, then every large enough \(L\) also obeys

\[
 C_{u_L}(h)=0\quad(h\in H\setminus\{0\}),
 \tag{3.11}
\]

so finitely many selected shifts do not repair the obstruction.

There is an independent sign/non-identifiability boundary.  The fields
\(u_L\) and \(-u_L\) have **the same complete scalar autocorrelation**,
not merely the same four summaries, while pressure is unchanged and

\[
 \mathcal N_4(-u_L)=+384L.
 \tag{3.12}
\]

Thus even complete knowledge of \(|u|^2\) does not determine the pressure
contribution: pressure depends on the tensor coefficients
\(\widehat{u_i u_j}\), not only on their trace \(C=\widehat{|u|^2}\).
Complete \(C\) may still support a scale-dependent upper bound; (3.12)
proves non-identifiability of the signed value, not impossibility of every
bound.

For additional exact bookkeeping, the field (3.1) has

\[
 X^2=4296,\qquad Y=1986.
 \tag{3.13}
\]

Therefore

\[
 \left.{dQ(u_L)\over dt}\right|_{t=0}
 =-16536\nu L^2-384L,
 \qquad
 \left.{dQ(-u_L)\over dt}\right|_{t=0}
 =-16536\nu L^2+384L.
 \tag{3.14}
\]

In particular,

\[
 \boxed{
 \left.{dQ(u_L)\over dt}\right|_{t=0}
 -\left.{dQ(-u_L)\over dt}\right|_{t=0}
 =-768L.}
 \tag{3.15}
\]

Both members of the sign pair are real, mean zero, divergence free, and
supported in the same annulus (3.8).  Equation (3.14) is compatible with
the one-sided estimate (2.3): the
unresolved derivative scale also creates the stronger negative viscous
term.

## 4. Exact no-go for a two-sided bound on the full derivative

The simpler shear

\[
 s_L(x)=(0,\sin(Lx_1),0)
 \tag{4.1}
\]

has zero advection and zero pressure.  For every integer \(L\ge1\),

\[
 \mathcal E={1\over2},\qquad
 Q={3\over8},\qquad
 A=1,\qquad
 D_C=3,
 \tag{4.2}
\]

because \(C(0)=1/2\) and \(C(\pm2Le_1)=-1/4\).  Its exact heat evolution
gives

\[
 \boxed{
 \left.{dQ(s_L)\over dt}\right|_{t=0}
 =-{3\over2}\nu L^2.}
 \tag{4.3}
\]

Thus no finite function of \((\mathcal E,Q,A,D_C)\), or of those numbers
plus a fixed finite shift sample, can bound \(|dQ/dt|\).  This does not
contradict (2.3), which is a one-sided upper bound and allows arbitrarily
negative derivatives.

## 5. Heat-weighted autocorrelation does not erase the scale cost

Adopt the conventions

\[
 Q_\tau=\sum_h e^{-2\tau|h|^2}|C(h)|^2,
 \qquad
 A_\tau=\sum_h e^{-\tau|h|^2}|C(h)|.
 \tag{5.1}
\]

For the six-mode field (3.1), direct grouping by \(|h|^2\) gives

\[
\begin{aligned}
 Q_\tau={}&1764+416e^{-2\tau}+194e^{-8\tau}
             +416e^{-10\tau}+128e^{-16\tau},\\
 A_\tau={}&42+40e^{-\tau}+26e^{-4\tau}
             +40e^{-5\tau}+16e^{-8\tau}.
\end{aligned}
 \tag{5.2}
\]

Scaling is exact:

\[
 Q_\tau(u_L)=Q_{\tau L^2}(u),
 \qquad
 A_\tau(u_L)=A_{\tau L^2}(u).
 \tag{5.3}
\]

Hence at the parabolic choice \(\tau_L=\theta/L^2\), both weighted
statistics are independent of \(L\), while the unfiltered pressure term is
still \(384L\).  Any robust bound for the unfiltered term must therefore
pay at least one inverse length, represented by \(\tau^{-1/2}\), a Fourier
radius, or a derivative norm.

At one fixed \(\tau>0\), (5.2)--(5.3) approach
\(Q_\tau\to\mathcal E^2=1764\) and
\(A_\tau\to\mathcal E=42\), although
\(|\mathcal N_4(u_L)|\to\infty\).  Thus no control function which stays
locally bounded at this limiting tuple can work.  This is a **stability
no-go**, not an information-theoretic one: exact exponentially small tails
could be fed into a deliberately singular function to recover a frequency
scale.

Heat weighting does improve the derivative of the smoothed statistic
itself, but it does not make that derivative scalar-autocorrelation
determined.  Since

\[
 Q_\tau=\|e^{\tau\Delta}w\|_2^2,
 \qquad
 {dQ_\tau\over dt}
 =2\langle e^{2\tau\Delta}w,\partial_tw\rangle,
 \tag{5.4}
\]

the odd-in-\(u\) part of \(\partial_tw\) is
\(-u\cdot\nabla w-2u\cdot\nabla p\).  Exact convolution for (3.1) gives

\[
 \boxed{
 \left.{dQ_\tau(u)\over dt}\right|_{t=0}
 -\left.{dQ_\tau(-u)\over dt}\right|_{t=0}
 =-768e^{-8\tau}.}
 \tag{5.5}
\]

For the dilated pair this becomes

\[
 -768L e^{-8\tau L^2}.
 \tag{5.6}
\]

The two fields in each pair have identical complete \(C\), hence identical
\(Q_\tau\) and \(A_\tau\), but their instantaneous derivatives differ.
At fixed \(\tau\) the difference is exponentially suppressed; at
\(\tau=\theta/L^2\) it is of order \(L\).  This identifies, rather than
removes, the missing parabolic scale.

There is a valid band-limited recovery.  If
\(\operatorname {supp}C\subset\{|h|\le K\}\), then

\[
 A\le e^{\tau K^2}A_\tau,
 \qquad
 Q\le e^{2\tau K^2}Q_\tau,
 \tag{5.7}
\]

and (2.3) yields

\[
 {dQ\over dt}+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}e^{3\tau K^2}A_\tau Q_\tau.
 \tag{5.8}
\]

Choosing \(\tau\asymp K^{-2}\) keeps the exponential cost bounded.  Without
\(K\), an equivalent derivative scale, or a rigorous tail contract,
\(A_\tau Q_\tau\) is smaller than \(AQ\) and cannot simply replace it.

## 6. Evidence classification

### Exact analytic results

1. The evolution identity (1.4).
2. The one-sided autocorrelation inequality (2.3)--(2.5).
3. The standard \(Q\)-only one-sided inequality (2.11).
4. The six-mode pressure value, scaling obstruction, and sign pair
   (3.1)--(3.15).
5. The shear obstruction to an absolute/two-sided derivative bound
   (4.1)--(4.3).
6. The weighted formulas, signed derivative separation, and band-limited
   deweighting (5.1)--(5.8).

### Finite evidence

The coefficient tables in Sections 3 and 5 are exact finite convolutions:
six velocity sites, fifteen nonzero scalar autocorrelation sites, and twelve
nonzero pressure sites.  They are reproducible by rational arithmetic.  No
claim in this audit relies on floating-point simulation, asymptotic fitting,
DGX computation, or an unverified PDE time integration.

### Conjectures / next tests

1. `OPEN_DYNAMIC_A`: whether a scale-aware quantity comparable to
   \(\int_0^T A(t)\,dt\) can be controlled from the energy inequality and
   shellwise flux without reintroducing a critical or supercritical norm.
2. `OPEN_TENSOR_PROXY`: whether a tractable tensor statistic built from
   \(\widehat{u_i u_j}\), rather than only its trace \(C\), can control the
   pressure pairing with a rigorously priced tail.  Any finite-shift version
   must defeat the dilation obstruction (3.11).
3. `OPEN_HEAT_HIERARCHY`: whether \(Q_{\tau(t)}\), together with a decreasing
   analytic radius \(\tau(t)\) and tensor pressure data, admits a closed
   differential inequality.  Equations (5.5)--(5.6) show that a scalar-only
   hierarchy cannot ignore the factor \(\tau^{-1/2}\).

## 7. Claim boundary

The publishable mathematical gain from this audit is narrow but useful:
R0.73S's \(AQ\) certificate does feed into a correct one-sided \(L^4\)
evolution inequality.  The general coefficient law exposes the missing
pressure-tensor input, while the exact finite annular sign pair separately
isolates signed velocity phase in the pressure pairing; the carrier witness
exposes the missing derivative scale.

It is forbidden to describe the six-mode or shear families as singular,
near-singular, or evidence for blow-up.  They are planar smooth
trigonometric polynomials used only to audit identifiability and scaling;
in particular, they omit the genuinely three-dimensional vortex-stretching
mechanism.  The existence of a global-in-time bound for arbitrary
three-dimensional smooth data and the Clay problem remain open.
