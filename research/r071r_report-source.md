# R0.71R -- A scale-matched incidence theorem reduces temporal packing to two dynamical ledgers

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, localized Littlewood--Paley observables, parabolic
Carleson packing, local energy methods, and quantitative zero-set questions

**Status:** release source.  This report derives the exact forced heat equation
for the R0.71P observable, proves a finite conditional event-to-window packing
theorem, proves that its scale-matched source-square measure is paid by the
Leray energy inequality, and constructs exact forced-parabolic families showing
that the two remaining incidence hypotheses are not consequences of abstract
forced-parabolic regularity.  It proves no
uniform Navier--Stokes incidence law, temporal packing theorem, infinite-frame
estimate, continuation criterion, singularity, global regularity, novelty,
priority, or Millennium-problem result.

## 0. Direct decision

R0.71P reduced the componentwise positive-entry target to

\[
 \mathsf S_{\Lambda,+}(K)
 =\sum_{\beta=(\alpha,t_\beta)}
   \kappa_{j(\alpha)}^{-2}A_{\beta,+},
 \tag{0.1}
\]

and batched simultaneous shell--cell entries so their total is absorbed by a
single time-slice square-function estimate.  R0.71Q showed that quantitative
complex-time analyticity still leaves
an anchor, a component union, a window cover, and a pointwise event-weight
ledger.  R0.71R asks instead whether the equation forces every entry to leave
a scale-matched amount of source mass in a forward parabolic window.

The answer has a positive and a negative part.

1. The localized observable satisfies an exact forced heat equation
   \(C_{j,Q,t}-\nu\Delta C_{j,Q}=G_{j,Q}\).
2. A one-parameter incidence hypothesis

   \[
    A_{\beta,+}\le\Gamma_\rho\kappa_j^{-\rho}
    \frac{\|C_\alpha(t_\beta+h_\beta)\|_2^2}
    {\sup_{I_\beta}Y},
    \qquad h_\beta=\theta_\beta\kappa_j^{-2},
    \quad 0<\theta_-\le\theta_\beta\le\theta_*,
   \]

   together with bounded same-observable window overlap gives a rigorous
   event-to-window theorem.
3. The minimal energy-paid choice \(\rho=2\) produces the source measure

   \[
    \frac1{Y(t)}\sum_{j,Q}\kappa_j^{-6}\|G_{j,Q}(t)\|_2^2\,dt.
    \tag{0.2}
   \]

   The derivative powers are exact: after summing the cutoffs and annuli,
   (0.2) is bounded by

   \[
    C\left(
      \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}+\nu^2
    \right)dt,
    \tag{0.3}
   \]

   and this is integrable from the ordinary Leray energy budget.
4. However, \(\rho=2\) is not scale covariant.  Under a covariant NSE
   dilation, the optimal constant in (3.3) scales by the missing frequency
   square.  The scale-covariant choice is \(\rho=0\), but it leaves the strong
   source budget

   \[
    \int\left(
      \frac{\|L\|_2^2}{Y}
      +\nu^2\frac{\|\nabla\omega\|_2^2}{Y}
    \right)dt,
   \]

   not the Leray \(\dot H^{-1}\) budget.  This is an exact two-derivative
   mismatch inside the quadratic Duhamel route.
5. Exact scalar and multi-component forced-parabolic families further show that
   neither input follows from abstract analyticity, semigroup smoothing, a
   source-square upper bound, or a Carleson upper bound.  A positive-entry atom
   is degree zero in the leading observable coefficient, whereas every
   quadratic tent charge is degree two.

This is a finite conditional reduction and a narrowly scoped method verdict.  The source
square sum removes the arbitrary component-union tax on the upper-budget side
of the genuine matched frame, after one uniform componentwise
\(\Gamma_\rho\) has been assumed.  But no exponent \(\rho\) in the
one-parameter endpoint-square
certificate (3.3) is both NSE scale covariant and Leray paid.  R0.71R does not
prove temporal packing and does not exclude other Duhamel, signed, or bilinear
designs.

## 1. Interface inherited from R0.71P

On the normalized periodic torus let \(u\) be a nontrivial zero-mean classical
solution, let

\[
 \omega=\operatorname{curl}u,
 \qquad Y(t)=\|\omega(t)\|_2^2,
 \qquad L=\mathbb P(u\times\omega),
 \tag{1.1}
\]

and fix the smooth annular multipliers and cutoff frame

\[
 W_j=T_j\omega,
 \qquad F_j=T_jL,
 \qquad C_{j,Q}=\operatorname{curl}(\chi_QW_j).
 \tag{1.2}
\]

Write \(\alpha=(j,Q)\).  If \(t_\beta\) is a finite-order zero of
\(C_\alpha\),

\[
 C_\alpha(t_\beta+\tau)=c_\beta\tau^{m_\beta}
 +O(\tau^{m_\beta+1}),
 \qquad c_\beta\ne0,
 \tag{1.3}
\]

then its right positive-entry mass is

\[
 A_{\beta,+}
 =\frac{\langle F_j(t_\beta),c_\beta\rangle_+^2}
 {Y(t_\beta)\|c_\beta\|_2^2}.
 \tag{1.4}
\]

The target (0.1) sums all positive component entries in a fixed finite
truncation.  R0.71P also proved the time-slice estimate

\[
 \sum_{\beta:t_\beta=t}\kappa_{j(\beta)}^{-2}A_{\beta,+}
 \le C_{\chi,T}\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}.
 \tag{1.5}
\]

Formula (1.5) absorbs the total simultaneous batch into one time-slice
square-function bound.  It does not control how often distinct times occur.

## 2. The exact forced heat equation

The vorticity and annular vorticity equations are

\[
 \omega_t-\nu\Delta\omega=\operatorname{curl}L,
 \qquad
 W_{j,t}-\nu\Delta W_j=\operatorname{curl}F_j.
 \tag{2.1}
\]

Since curl commutes with \(\Delta\), a direct product calculation gives

\[
 \boxed{
 C_{j,Q,t}-\nu\Delta C_{j,Q}=G_{j,Q},}
 \tag{2.2}
\]

where

\[
 \boxed{
 \begin{aligned}
 G_{j,Q}
 &=\operatorname{curl}(\chi_Q\operatorname{curl}F_j)\\
 &\quad-\nu\operatorname{curl}\!\left(
   2\nabla\chi_Q\mathbin{\cdot}\nabla W_j
   +(\Delta\chi_Q)W_j
 \right).
 \end{aligned}}
 \tag{2.3}
\]

The second line is the exact localization--viscosity commutator.  No pressure
term is missing because it was removed in \(L=\mathbb P(u\times\omega)\)
before taking curl.

At an entry time \(C_\alpha(t_\beta)=0\), Duhamel's formula reads

\[
 C_\alpha(t_\beta+h)
 =\int_0^h e^{\nu(h-s)\Delta}
 G_\alpha(t_\beta+s)\,ds.
 \tag{2.4}
\]

The heat semigroup is an \(L^2\)-contraction.  Cauchy--Schwarz therefore gives

\[
 \boxed{
 \frac{\|C_\alpha(t_\beta+h)\|_2^2}{h}
 \le\int_{t_\beta}^{t_\beta+h}\|G_\alpha(s)\|_2^2\,ds.}
 \tag{2.5}
\]

This upper estimate becomes an event charge only if the entry weight has a
lower comparison with the left side.

## 3. A one-parameter incidence certificate

For every positive entry \(\beta=(\alpha,t_\beta)\), choose

\[
 h_\beta=\theta_\beta\kappa_{j(\alpha)}^{-2},
 \qquad 0<\theta_-\le\theta_\beta\le\theta_*,
 \qquad I_\beta=[t_\beta,t_\beta+h_\beta],
 \tag{3.1}
\]

with \(I_\beta\) contained in a classical neighborhood \(K^+\), and put

\[
 Y_\beta^*=\sup_{s\in I_\beta}Y(s).
 \tag{3.2}
\]

For \(\rho\ge0\), the **post-entry incidence certificate** with constant
\(\Gamma_\rho\) is

\[
 \boxed{
 A_{\beta,+}
 \le\Gamma_\rho\,
 \frac{\kappa_{j(\alpha)}^{-\rho}
 \|C_\alpha(t_\beta+h_\beta)\|_2^2}{Y_\beta^*}.}
 \tag{3.3}
\]

The exponent \(\rho\) records exactly where derivatives are paid.  The choice
\(\rho=2\) is energy matched after Duhamel and frame summation; the choice
\(\rho=0\) is NSE scale covariant.  Section 5.2 proves that these two choices do
not coincide.  The supremum in (3.2) is deliberate.  It removes a separate
local comparability assumption because

\[
 \frac1{Y_\beta^*}\le\frac1{Y(s)}
 \quad\text{for }s\in I_\beta.
 \tag{3.4}
\]

For each fixed observable define the forward-window multiplicity

\[
 \mathfrak m_\alpha(s)
 =\sum_{\beta:\alpha(\beta)=\alpha}\mathbf1_{I_\beta}(s),
 \qquad
 M=\sup_\alpha\operatorname*{ess\,sup}_{s}\mathfrak m_\alpha(s).
 \tag{3.5}
\]

The second required certificate is \(M<\infty\) with a bound independent of
the finite truncation.  The essential supremum makes the harmless double
counting of closed-window endpoints irrelevant.  The lower height
\(\theta_->0\) is essential: without it one could shrink each window before
the next isolated zero and trivialize \(M\), while transferring the entire
loss into \(\Gamma_\rho\).  This is not a same-time cell overlap: (3.5)
measures repeated temporal entries of one observable at a noncollapsing
parabolic height.

## 4. Conditional event-to-Carleson packing theorem

### Theorem 4.1 -- finite \(\rho\)-incidence packing

Let \(K\Subset K^+\Subset I_{\rm strong}\) and let \(\Lambda\) be finite.
Assume that every positive entry in \(K\) has a window satisfying (3.1)--(3.3)
for one fixed \(\rho\ge0\), and that (3.5) is bounded by \(M\).  Then

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 \le\Gamma_\rho\theta_*M
 \int_{K^+}\frac1{Y(s)}
 \sum_{\alpha\in\Lambda}
 \kappa_{j(\alpha)}^{-(4+\rho)}\|G_\alpha(s)\|_2^2\,ds.}
 \tag{4.1}
\]

#### Proof

Multiply (3.3) by \(\kappa_j^{-2}\), use (2.5), and then use
\(h_\beta\le\theta_*\kappa_j^{-2}\):

\[
 \begin{aligned}
 \kappa_j^{-2}A_{\beta,+}
 &\le\Gamma_\rho\frac{\kappa_j^{-(2+\rho)}}{Y_\beta^*}
 \|C_\alpha(t_\beta+h_\beta)\|_2^2\\
 &\le\Gamma_\rho\frac{\kappa_j^{-(2+\rho)}h_\beta}{Y_\beta^*}
 \int_{I_\beta}\|G_\alpha(s)\|_2^2\,ds\\
 &\le\Gamma_\rho\theta_*
 \int_{I_\beta}\frac{\kappa_j^{-(4+\rho)}
 \|G_\alpha(s)\|_2^2}{Y(s)}\,ds.
 \end{aligned}
 \tag{4.2}
\]

After summing \(\beta\), Tonelli's theorem turns the interval sum into
\(\mathfrak m_\alpha(s)\).  Formula (3.5) then gives (4.1). \(\square\)

For every subinterval \(J\subset K^+\), the same proof restricted to entries
whose owned windows satisfy \(I_\beta\subset J\) gives

\[
 \sum_{\beta:I_\beta\subset J}\kappa_j^{-2}A_{\beta,+}
 \le\Gamma_\rho\theta_*M\,\mu_{G,\rho}(J),
 \tag{4.3}
\]

where

\[
 d\mu_{G,\rho}(s)=\frac1{Y(s)}
 \sum_{\alpha\in\Lambda}\kappa_j^{-(4+\rho)}
 \|G_\alpha(s)\|_2^2\,ds.
 \tag{4.4}
\]

Thus (4.3) is a source-relative Carleson packing statement.  It is not a
classical \(|J|\)-Carleson bound unless a separate estimate for
\(\mu_{G,\rho}(J)\) is available.

## 5. Source powers and the two-derivative mismatch

Assume the adapted cutoffs have bounded overlap and, for \(0\le m\le3\),

\[
 \sup_x\sum_Q|\nabla^m\chi_Q(x)|^2
 \le C_\chi\kappa_j^{2m}.
 \tag{5.1}
\]

The fixed annular multiplier has the usual Bernstein bounds.  Expanding the
first term in (2.3) gives

\[
 \sum_Q\|\operatorname{curl}(\chi_Q\operatorname{curl}F_j)\|_2^2
 \le C_{\chi,T}\kappa_j^4\|F_j\|_2^2.
 \tag{5.2}
\]

Expanding the outer curl in the commutator gives only terms with total order
three at the cutoff scale: \(\nabla^2\chi_Q\nabla W_j\),
\(\nabla\chi_Q\nabla^2W_j\), \(\nabla\Delta\chi_QW_j\), and
\(\Delta\chi_Q\nabla W_j\).  Hence

\[
 \sum_Q\left\|
 \nu\operatorname{curl}\left(
 2\nabla\chi_Q\mathbin{\cdot}\nabla W_j
 +(\Delta\chi_Q)W_j
 \right)\right\|_2^2
 \le C_{\chi,T}\nu^2\kappa_j^6\|W_j\|_2^2.
 \tag{5.3}
\]

Combining (5.2)--(5.3), multiplying by
\(\kappa_j^{-(4+\rho)}\), and summing annuli gives the one-parameter ledger

\[
 \boxed{
 \sum_{j,Q}\kappa_j^{-(4+\rho)}\|G_{j,Q}\|_2^2
 \le C_{\chi,T}\left(
 \sum_j\kappa_j^{-\rho}\|F_j\|_2^2
 +\nu^2\sum_j\kappa_j^{2-\rho}\|W_j\|_2^2
 \right).}
 \tag{5.4}
\]

Equivalently, up to the fixed low-frequency convention on the zero-mean
torus, the two terms have Sobolev orders

\[
 \|L\|_{\dot H^{-\rho/2}}^2
 \quad\text{and}\quad
 \nu^2\|\omega\|_{\dot H^{1-\rho/2}}^2.
 \tag{5.4a}
\]

### 5.1 The minimal energy-matched choice \(\rho=2\)

For \(\rho=2\), (5.4) becomes

\[
 \boxed{
 \sum_{j,Q}\kappa_j^{-6}\|G_{j,Q}\|_2^2
 \le C_{\chi,T}\left(
 \|L\|_{\dot H^{-1}}^2+\nu^2Y
 \right).}
 \tag{5.5}
\]

Indeed, the nonlinear part uses

\[
 \sum_j\kappa_j^{-2}\|T_jL\|_2^2
 \le C_T\|L\|_{\dot H^{-1}}^2,
 \tag{5.6}
\]

and the commutator part uses

\[
 \sum_j\|T_j\omega\|_2^2\le C_TY.
 \tag{5.7}
\]

The Lamb term is integrable after division by \(Y\).  Sobolev interpolation
gives

\[
 \begin{aligned}
 \|L\|_{\dot H^{-1}}
 &\le C\|u\times\omega\|_{6/5}
 \le C\|u\|_3\|\omega\|_2\\
 &\le C\|u\|_2^{1/2}Y^{3/4},
 \end{aligned}
 \tag{5.8}
\]

Here \(L\) has zero mean by the periodic vector identity for
\(u\times\operatorname{curl}u\), and the Leray projector is bounded on
\(\dot H^{-1}\).

and therefore

\[
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}
 \le C\|u\|_2Y^{1/2}.
 \tag{5.9}
\]

On any finite interval \(J\), the energy inequality implies

\[
 \int_J\left(
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}+\nu^2
 \right)dt
 \le C\|u_0\|_2|J|^{1/2}
 \left(\int_JY\,dt\right)^{1/2}+\nu^2|J|<\infty.
 \tag{5.10}
\]

### Corollary 5.1 -- the \(\rho=2\) conditional target is energy-paid

Under Theorem 4.1's incidence and overlap hypotheses,

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 \le C_{\chi,T}\Gamma_2\theta_*M
 \int_{K^+}\left(
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}+\nu^2
 \right)dt.}
 \tag{5.11}
\]

Only the source integral and fixed frame constants in (5.11) are uniform in
the finite shell--cell truncation.  The complete right side is not yet uniform
because \(\Gamma_2\), \(M\), and forward-window availability may depend on
the truncation.  On the
zero-mean normalized torus, every \(\rho>2\) source ledger is also controlled
by the \(\rho=2\) ledger because \(\kappa_j\ge1\); thus \(\rho=2\) is the
minimal, or critical, Leray-paid exponent rather than the only paid exponent.
The constants
\(\Gamma_2\), \(M\), and the availability of the forward windows are not
known to be uniform.

### 5.2 Scale covariance forces \(\rho=0\)

For integer (and, for the dyadic annular family below, dyadic) \(\lambda\),
consider the three-dimensional NSE rescaling on the fixed periodic torus

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{5.12}
\]

and rescale the multiplier and cutoff families covariantly.  Corresponding
entries and windows obey \(t_\beta\mapsto\lambda^{-2}t_\beta\) and
\(h_\beta\mapsto\lambda^{-2}h_\beta\), so \(\theta_\beta\) is unchanged;
the matched quantities transform as

\[
 A_{\beta,+}\mapsto\lambda^2A_{\beta,+},
 \qquad
 \kappa_j\mapsto\lambda\kappa_j,
 \qquad
 \frac{\|C\|_2^2}{Y}\mapsto
 \lambda^2\frac{\|C\|_2^2}{Y}.
 \tag{5.13}
\]

Therefore the right side of (3.3), apart from \(\Gamma_\rho\), scales as
\(\lambda^{2-\rho}\).  A universal scale-independent incidence constant is
compatible only with

\[
 \boxed{\rho=0.}
 \tag{5.14}
\]

If \(\Gamma_\rho^{\rm opt}[u]\) denotes the least admissible constant for the
corresponding covariantly rescaled finite event/window family, covariance gives

\[
 \Gamma_\rho^{\rm opt}[u_\lambda]
 =\lambda^\rho\Gamma_\rho^{\rm opt}[u],
 \qquad
 \Gamma_2^{\rm opt}[u_\lambda]
 =\lambda^2\Gamma_2^{\rm opt}[u].
 \tag{5.15}
\]

Thus a dimensionless scale-uniform constant is impossible for this covariantly
rescaled \(\rho=2\) certificate: its optimal constant has the missing two
powers.

At the scale-covariant choice \(\rho=0\), (5.4) gives instead

\[
 \sum_{j,Q}\kappa_j^{-4}\|G_{j,Q}\|_2^2
 \le C_{\chi,T}\left(
 \|L\|_2^2+\nu^2\|\nabla\omega\|_2^2
 \right).
 \tag{5.16}
\]

After division by \(Y\), this requires the normalized \(L^2\)-Lamb term and
normalized palinstrophy.  These quantities are not controlled by the Leray
energy inequality; their integrability would be additional strong regularity
input.  Thus the one-parameter endpoint-square Duhamel design has an exact
mismatch:

\[
 \boxed{
 \text{NSE-critical incidence requires }\rho=0,
 \qquad
 \text{the minimal Leray-paid source exponent is }\rho=2.}
 \tag{5.17}
\]

No choice in this one-parameter interpolation supplies both properties:
scale covariance selects \(\rho=0\), while Leray payment begins at
\(\rho=2\).

### 5.3 Genuine NSE high-frequency initial-jet pressure test

On the periodic torus take a compatible integer, preferably dyadic,
frequency \(K\), put \(\kappa_j=K\), and set

\[
 u_{0,K}=a(0,\cos Kx_1,\cos Kx_2),
 \tag{5.18}
\]

and use one covariantly rescaled radial-multiplier family with value zero at
radius \(K\) and one at radius \(\sqrt2K\); set \(\chi=1\).  Scaling the exact R0.71O Fourier
calculation gives

\[
 \boxed{
 Y(0)=a^2K^2,
 \quad\|F(0)\|_2^2=\frac{a^4K^2}{4},
 \quad C_t(0)=2K^2F(0),
 \quad A_+=\frac{a^2}{4}.}
 \tag{5.19}
\]

At a formal parabolic height \(h=\theta K^{-2}\), the first-jet surrogate for
the \(\rho=2\) incidence right side is

\[
 K^{-2}\frac{\|hC_t(0)\|_2^2}{Y(0)}
 =\frac{a^2\theta^2}{K^2}.
 \tag{5.20}
\]

Define the corresponding Taylor-jet ratio by

\[
 \boxed{
 \Gamma_{2,{\rm jet}}
 :=\frac{A_+}{K^{-2}\|hC_t(0)\|_2^2/Y(0)}
 =\frac{K^2}{4\theta^2}.}
 \tag{5.21}
\]

The energy \(\|u_{0,K}\|_2^2=a^2\) is independent of \(K\).  The certificate
records only the exact Fourier jet and the first-jet coefficient.  It does not
control the Duhamel remainder at positive time and makes no positive-time
incidence claim.  In particular, \(\Gamma_{2,{\rm jet}}\) is not a proved
lower bound for the actual \(\Gamma_2\) in (3.3).  The choice \(\chi=1\) is a
global-cutoff annular pressure test; no claim is made that it realizes every
localized cell of the R0.71P frame.

## 6. Why a Carleson upper bound alone cannot create the charge

The positive-entry measure is atomic:

\[
 d\mu_{\rm entry}
 =\sum_\beta\kappa_j^{-2}A_{\beta,+}\,\delta_{t_\beta}.
 \tag{6.1}
\]

The source-square measure (4.4) is absolutely continuous on a classical
interval, so \(\mu_G(\{t_\beta\})=0\).  A direct measure domination
\(\mu_{\rm entry}\le C\mu_G\) is impossible.  Within the present
absolutely-continuous source-square route, comparison must therefore pass
through nonzero owned windows, as in (4.3), and that requires an event-wise
lower charge.  This does not exclude signed or nonlocal comparisons outside
that route.

This is the same logical feature that makes an epsilon-regularity covering
argument work for singular points: each bad cylinder must first carry a
quantitative amount of the relevant scale-normalized energy.  The CKN theorem
does not supply that implication for the present events.  A zero of one
localized filtered observable can occur in a completely smooth region.

## 7. Exact homogeneity obstruction

Take the scalar contraction generator \(A=1\) on \(H=\mathbb R\), set
\(F=1\), \(Y=1\), \(\kappa=1\), and define on \([0,1]\)

\[
 C_\varepsilon(t)=\varepsilon(t-1/2)^2,
 \qquad G_\varepsilon=C_\varepsilon'+C_\varepsilon.
 \tag{7.1}
\]

At \(t=1/2\), the leading coefficient is \(c=\varepsilon>0\), so

\[
 A_+=\frac{(Fc)^2}{Yc^2}=1
 \quad\text{for every }\varepsilon>0.
 \tag{7.2}
\]

For every fixed \(h\), however,

\[
 |C_\varepsilon(1/2+h)|^2=\varepsilon^2h^4,
 \qquad
 \int_0^1|G_\varepsilon|^2dt
 =\varepsilon^2E_1.
 \tag{7.3}
\]

Both quadratic charges tend to zero while the entry mass stays one.  Thus no
uniform \(\Gamma\) in (3.3) follows from smoothness, analyticity, or an upper
source norm for general forced parabolic paths.

Multiplying the squared Blaschke family from R0.71Q by \(\varepsilon\) gives
the same pressure test while preserving every relative Jensen datum
\(M/|C(t_*)|\).  Complex radius, relative growth, and relative anchor data do
not repair the missing absolute incidence charge.

This is a method obstruction, not an NSE counterexample.  In the NSE equation,
\(F\), \(Y\), \(C\), and \(G\) are dynamically coupled and cannot be scaled
independently in the manner of (7.1).

## 8. Sequential single-observable obstruction

For \(N\ge1\), let

\[
 q_N(t)=\prod_{k=1}^N\left(t-\frac{k}{N+1}\right)^2,
 \qquad
 C_N=\varepsilon_Nq_N,
 \qquad G_N=C_N'+C_N.
 \tag{8.1}
\]

Every root has a positive quadratic leading coefficient.  With \(F=Y=1\),
all \(N\) roots have \(A_+=1\).  Put

\[
 E_N=\int_0^1|q_N'+q_N|^2dt,
 \qquad \varepsilon_N=E_N^{-1/2}.
 \tag{8.2}
\]

Then

\[
 \int_0^1|G_N|^2dt=1,
 \qquad
 \sum_{k=1}^NA_{k,+}=N.
 \tag{8.3}
\]

Consequently, for any assignment of parabolic forward windows satisfying the
incidence theorem, the product \(\Gamma_\rho\theta_*M\) must grow at least linearly
along this abstract family.  A source-square total mass does not by itself
bound sequential entries.

## 9. All-observable union obstruction

Choose distinct \(b_q\in(1/4,3/4)\) and let

\[
 C_q(t)=2^{-q}(t-b_q)^2,
 \qquad G_q=C_q'+C_q,
 \qquad q=1,\ldots,Q.
 \tag{9.1}
\]

Each component has one positive entry of mass one.  On \([0,1]\),

\[
 |2(t-b_q)+(t-b_q)^2|\le3,
 \tag{9.2}
\]

and therefore

\[
 \sum_{q=1}^Q\int_0^1|G_q|^2dt
 \le9\sum_{q=1}^\infty4^{-q}=3,
 \qquad
 \sum_{q=1}^QA_{q,+}=Q.
 \tag{9.3}
\]

Here the temporal overlap of each fixed component is one.  The failure is the
absence of a uniform componentwise incidence constant as the amplitudes
decrease.  This shows why an all-observable square-sum upper budget does not
pay the union of degree-zero entry atoms without a lower charge.

Again, (9.1) is a forced scalar family and not an NSE frame realization.

## 10. Relation to the signed precursor

R0.71O proved, before taking componentwise positive parts, that the soft
signed source converges at a finite-order zero to a signed face measure, while
its positive part converges to \(A_+\delta_{t_\beta}\).  Bounding that complete
componentwise positive source would pay the target, but it is exactly the
missing positive-variation estimate; splitting its cancellation-sensitive
pieces separately creates divergent terms.

The source \(G_{j,Q}\) in (2.3) is different.  It is the ordinary forcing of
the localized parabolic equation and remains an \(L^2\)-time density on a
classical interval.  Theorem 4.1 uses it before positive parts and asks whether
the PDE converts each atomic face into a nonzero forward source packet.  The
homogeneity examples prove that such a conversion is not a generic parabolic
fact.

## 11. Primary-literature boundary

The bounded source audit is recorded separately in
`research/r071r_literature_audit.md`.  Its relevant conclusions are:

1. Caffarelli--Kohn--Nirenberg epsilon regularity and the quantitative
   refinement of Lei--Ren package singular cylinders or produce regular
   windows.  They do not assign a lower dissipation mass to every zero of a
   localized filtered observable.
2. Koch--Tataru's \(BMO^{-1}\) norm is a genuine parabolic square-Carleson
   budget, but it is an upper tent norm in a small-data solution class.  It
   supplies no entry-to-tent lower charge.
3. Dascaliuc--Grujić obtain signed physical-scale enstrophy-flux bounds under
   coherence, Kraichnan-scale, and modulation hypotheses.  Their quantity is
   a space--time cover average, not a count of temporal atoms.
4. Angenent's zero-number theorem gives actual cardinality monotonicity for a
   one-dimensional scalar homogeneous parabolic equation.  The three-
   dimensional Hilbert-valued, localized, forced observable lacks the Sturm
   order structure.
5. Higher-dimensional nodal-set estimates concern spatial zero sets at a
   fixed time; they do not count times at which an entire localized field is
   zero.  Known higher-dimensional examples also prevent a direct import of
   one-dimensional zero-number monotonicity.
6. Backward uniqueness requires a closed parabolic inequality and vanishing
   of the full field on a terminal spatial region.  The operator
   \(u\mapsto C_{j,Q}\) has a large kernel and equation (2.2) is forced.

No checked primary theorem directly provides (3.3) or (3.5) uniformly for the
R0.71P observables.  This is a bounded negative finding, not a claim of
nonexistence, novelty, or priority.

## 12. Exact result boundary

### Proved in R0.71R

1. the exact localized forced heat equation (2.2)--(2.3);
2. the Duhamel event-to-window inequality (2.5);
3. the finite conditional incidence packing theorem (4.1);
4. the one-parameter source-power estimate (5.4);
5. finite-time Leray payment at the minimal exponent \(\rho=2\),
   (5.5)--(5.11), with higher \(\rho\) controlled on the normalized torus;
6. the exact scaling verdict that scale covariance requires \(\rho=0\), while
   the minimal Leray-paid exponent is \(\rho=2\);
7. the genuine NSE high-frequency initial-jet pressure test (5.18)--(5.21);
8. exact abstract homogeneity, sequential, and component-union obstructions;
9. a bounded primary-source audit identifying the missing event lower charge.

### Not proved

1. a uniform NSE post-entry incidence constant \(\Gamma_\rho\);
2. a uniform NSE forward-window overlap constant \(M\);
3. noncollapsing forward parabolic windows near a possible maximal endpoint;
4. a uniform temporal packing theorem for the infinite frame;
5. a Leray-limit passage for the entry measure;
6. a continuation criterion, exclusion or construction of finite-time
   singularity, or global regularity.

At \(\rho=2\), every quantity after \(\Gamma_2\theta_*M\) is paid by energy,
but the optimal certificate constant has the missing two scale powers under a
covariant dilation.  At
\(\rho=0\), the incidence hypothesis is critical but the source budget is
strong.  It is not useful to hide either loss inside a new “Carleson norm”.

## 13. Next finite gate

R0.71S should no longer try to prove the one-parameter endpoint-square
\(\rho=2\) certificate with a
scale-independent constant.  It should test whether a signed directional
pairing can recover the missing two powers without upgrading the budget:

1. retain the entry direction \(e_\beta=c_\beta/\|c_\beta\|_2\) and the signed
   pairing \(\langle F_j,e_\beta\rangle\) before taking componentwise positive
   parts;
2. derive a scale-covariant packet functional whose frame sum is still paid by
   \(\dot H^{-1}\), rather than by \(L^2\) or palinstrophy;
3. pressure-test recurrence: if the observable returns toward zero, the packet
   must charge directional oscillation without paying the same interval many
   times.

The test must retain the exact coupling among \(F_j\), \(Y\), \(C_{j,Q}\),
and \(G_{j,Q}\), and it must pass the initial-jet and sequential-path pressure
tests without assuming a lower analytic anchor.  If every such pairing either
loses sign after localization or requires the strong \(\rho=0\) source budget,
the parabolic-incidence branch stops at the two-derivative mismatch proved
here.
