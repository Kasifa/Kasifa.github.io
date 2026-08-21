# R0.69S — A single dyadic shell can carry strictly positive signed stretching

## 1. Result

R0.69R showed that taking absolute values in a physical-space near/far split
returns exactly to the classical sextic enstrophy cost.  The next possibility
is to postpone absolute values and look for cancellation between scales.
R0.69S tests the most direct version of that idea: the exact signed
output-shell decomposition of vortex stretching.

On the normalized torus \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), let
\(P_m\) be the mutually orthogonal sharp Fourier projectors

\[
 \widehat{P_m f}(k)
 =\mathbf 1_{\{2^m\le |k|<2^{m+1}\}}\widehat f(k),
 \qquad k\ne0.                                               \tag{1.1}
\]

For a smooth, real, mean-zero, divergence-free velocity field, define the
signed output-shell stretching production

\[
 \mathcal F_m(u)
 =\int_{\mathbb T^3}
 P_m\omega\cdot P_m(S\omega)\,dx,
 \qquad
 S=\frac{\nabla u+\nabla u^{\mathsf T}}2.                    \tag{1.2}
\]

Orthogonality gives the exact identity

\[
 \sum_{m\in\mathbb Z}\mathcal F_m(u)
 =\int_{\mathbb T^3}\omega\cdot S\omega\,dx.                 \tag{1.3}
\]

The cancellation ratio is

\[
 \Gamma(u)
 =\frac{\left|\sum_m\mathcal F_m(u)\right|}
        {\sum_m|\mathcal F_m(u)|},
 \qquad
 \sum_m|\mathcal F_m(u)|>0.                                 \tag{1.4}
\]

Trivially \(0\le\Gamma\le1\).  R0.69S constructs an exact six-mode field
for which

\[
 \boxed{
 \mathcal F_0(u)=2,\qquad
 \mathcal F_m(u)=0\ (m\ne0),\qquad
 \Gamma(u)=1.}                                               \tag{1.5}
\]

Consequently, there is no universal \(\theta<1\) such that

\[
 \left|\sum_m\mathcal F_m(u)\right|
 \le\theta\sum_m|\mathcal F_m(u)|                            \tag{1.6}
\]

for all smooth divergence-free data.  Dyadic shell grouping by itself does
not force any signed depletion.

The conclusion is deliberately narrow.  It does not rule out:

- cancellation within one shell;
- smooth overlapping Littlewood--Paley decompositions with an additional
  commutator structure;
- physical-space annular cancellation in the Biot--Savart kernel;
- dynamical cancellation accumulated along a Navier--Stokes solution;
- a critical regularity criterion containing an independently controlled
  third quantity.

It proves neither global regularity nor finite-time blow-up and does not solve
the Millennium Problem.

## 2. The exact six-mode witness

Take the positive wavevectors

\[
 k=(1,0,0),\qquad
 p=(0,1,0),\qquad
 q=(-1,-1,0),\qquad k+p+q=0,                                \tag{2.1}
\]

and complex Fourier coefficients

\[
 \begin{aligned}
 a_k&=(0,\,1,\,-1-i),\\
 a_p&=(-1,\,0,\,-1),\\
 a_q&=(-1-i,\,1+i,\,1).                                     \tag{2.2}
 \end{aligned}
\]

They are exactly transverse:

\[
 k\cdot a_k=p\cdot a_p=q\cdot a_q=0.                        \tag{2.3}
\]

Adjoin

\[
 a_{-r}=\overline{a_r},\qquad r\in\{k,p,q\},                 \tag{2.4}
\]

and set all other coefficients to zero.  Then

\[
 u(x)=\sum_{r\in\{\pm k,\pm p,\pm q\}}a_r e^{ir\cdot x}      \tag{2.5}
\]

is a real, smooth, mean-zero, divergence-free trigonometric polynomial.
All six frequencies satisfy

\[
 1\le|r|<2,                                                  \tag{2.6}
\]

because their squared lengths are \(1,1,2\).  Thus

\[
 P_0u=u,\qquad P_mu=0\quad(m\ne0),                           \tag{2.7}
\]

and the same support statement holds for \(\omega=\nabla\times u\).

## 3. Direct Fourier evaluation of the signed stretching

For a Fourier mode \(r\), the vorticity and strain coefficients are

\[
 \omega_r=i\,r\times a_r,\qquad
 S_r=\frac i2(r\otimes a_r+a_r\otimes r).                   \tag{3.1}
\]

With normalized torus integration, the zero Fourier coefficient of
\(\omega\cdot S\omega\) is

\[
 \mathcal V(u)
 =\sum_{r+s+t=0}\omega_r\cdot S_s\omega_t.                  \tag{3.2}
\]

There are twelve nonzero ordered contributions.  For the positive triad they
are

\[
 \frac52,\quad-\frac12,\quad-\frac32,\quad-\frac12,\quad
 -\frac32,\quad\frac52,                                     \tag{3.3}
\]

and the conjugate triad contributes the same list.  Hence

\[
 \boxed{\mathcal V(u)
 =\int_{\mathbb T^3}\omega\cdot S\omega\,dx=2>0.}            \tag{3.4}
\]

This is a direct evaluation of vortex stretching, not an inference from a
floating-point simulation.

For comparison with the usual triad transfer bookkeeping, the three positive
modal transfers are

\[
 (T_k,T_p,T_q)=(2,-3,1).                                    \tag{3.5}
\]

They conserve kinetic energy,

\[
 T_k+T_p+T_q=0,                                              \tag{3.6}
\]

but their enstrophy-weighted sum is nonzero:

\[
 |k|^2T_k+|p|^2T_p+|q|^2T_q
 =2-3+2=1.                                                   \tag{3.7}
\]

The negative frequencies double this value, agreeing with (3.4).

## 4. Why only one output shell is active

Since \(P_0\omega=\omega\) and \(P_m\omega=0\) for \(m\ne0\),

\[
 \begin{aligned}
 \mathcal F_0(u)
 &=\langle\omega,P_0(S\omega)\rangle\\
 &=\langle P_0\omega,S\omega\rangle
 =\langle\omega,S\omega\rangle=2,                            \tag{4.1}\\
 \mathcal F_m(u)&=0,\qquad m\ne0.                            \tag{4.2}
 \end{aligned}
\]

The nonlinear product \(S\omega\) may contain frequencies outside the
original annulus.  This does not change (4.1): orthogonality moves \(P_0\)
onto the first factor, which already equals \(\omega\).  Thus the
single-shell conclusion does not silently assume that the nonlinear product
is shell preserving.

Equations (4.1)--(4.2) imply \(\Gamma(u)=1\), so the trivial upper bound on
the cancellation ratio is sharp.

## 5. Sign and scale robustness

The functional is cubic:

\[
 \mathcal F_m(a u)=a^3\mathcal F_m(u).                       \tag{5.1}
\]

In particular, \(u\mapsto-u\) reverses every signed shell production and
\(\mathcal V(-u)=-2\), while the cancellation ratio remains one.  Shell
localization cannot create a preferred sign.

The family

\[
 u^{(\ell)}(x)=u(2^\ell x),\qquad \ell\in\mathbb Z_{\ge0},   \tag{5.2}
\]

is again smooth and periodic.  Its support lies entirely in shell \(m=\ell\)
and

\[
 \mathcal F_\ell(u^{(\ell)})=2^{3\ell}\mathcal F_0(u),
 \qquad
 \Gamma(u^{(\ell)})=1.                                      \tag{5.3}
\]

Hence the obstruction can be moved to arbitrarily high dyadic frequency; it
is not a low-mode accident.

## 6. Decision for the route

R0.69S proves

\[
 \boxed{
 \text{signed output-shell decomposition}
 \not\Longrightarrow
 \text{universal cross-shell depletion}.}                   \tag{6.1}
\]

A successful signed argument must use more than the identity
\(\mathcal V=\sum_m\mathcal F_m\).  It must exploit at least one of:

1. cancellation inside the active shell;
2. an angular or helical sub-decomposition;
3. time coherence or decorrelation across successive nonlinear interactions;
4. a physical-space flux term that is not determined by shell support alone.

R0.69T will test the fourth option: physical-space annuli in the geometric
Biot--Savart kernel.  The affine-core witness from R0.69P will be used to
check whether signed annular contributions can be forced to one sign, while
all truncation boundary terms are kept explicit.

## 7. Prior work and claim boundary

Fourier-shell energy and enstrophy transfers, Littlewood--Paley
decompositions, and helical triad analysis are classical tools in turbulence
and Navier--Stokes analysis.  This note does not claim those tools or the
general possibility of one-shell interactions as new.

The project result is the exact route audit: an explicit six-mode
divergence-free field is evaluated directly in the vorticity--strain
functional and shown to saturate the signed cross-shell cancellation ratio.
It rules out an unconditional depletion factor derived solely from sharp
output-shell grouping.  It does not rule out smooth-projector commutators,
physical-space annular geometry, conditional criteria, global regularity, or
finite-time singularity.
