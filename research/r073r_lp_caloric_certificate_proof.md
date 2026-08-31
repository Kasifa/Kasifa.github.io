# R0.73R analytic proof: an LP--caloric concentration certificate

**Status:** complete analytic draft; two independent derivations and the
primary-literature collision audit agree; formal certificate and public seal
are still pending

**Dependencies:** R0.73Q uniform heat-flow stability tube; periodic
Littlewood--Paley theory; Hausdorff--Young; Parseval; the classical
Rudin--Shapiro recursion

## 1. Setting and exact statement

Work on \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar measure and
viscosity one.  All fields are real, mean zero, and divergence free unless a
lemma explicitly treats a scalar component.

Fix once and for all a smooth inhomogeneous periodic Littlewood--Paley
decomposition

\[
 f=\sum_{j\ge0}P_jf.
 \tag{1.1}
\]

The block \(P_0\) contains finitely many nonzero low modes.  For \(j\ge1\),
the symbol of \(P_j\) is supported in

\[
 c_0 2^j\le |k|\le C_0 2^j,
 \tag{1.2}
\]

and the enlarged supports have a fixed finite overlap.  Put

\[
 f_j=P_jf,\qquad E_j=\|f_j\|_2,\qquad b_j=\|f_j\|_6.
 \tag{1.3}
\]

When \(E_j>0\), define

\[
 c_j(f):={b_j\over2^jE_j},
 \qquad
 \Theta_j(f):={b_j^6\over E_j^6};
 \tag{1.4}
\]

both are set equal to zero when \(E_j=0\).  Thus

\[
 c_j2^{j/2}E_j=2^{-j/2}b_j,
 \qquad
 \Theta_j^{2/3}E_j^4=b_j^4.
 \tag{1.5}
\]

The numbers \(c_j\) depend on the fixed LP decomposition.  The norm class
below does not.  In particular, Bernstein gives only \(c_j\le C_B\), not a
cutoff-independent bound by one.

### Theorem 1.1: two-sided LP--caloric certificate

There are constants \(0<C_-\le C_+<\infty\), depending only on the fixed
LP cutoffs and the torus, such that every mean-zero trigonometric polynomial
satisfies

\[
 \boxed{
 C_-\left(\sum_{j\ge0}
       [c_j(f)2^{j/2}E_j]^4\right)^{1/4}
 \le
 \|e^{t\Delta}f\|_{L^4((0,\infty);L^6)}
 \le
 C_+\left(\sum_{j\ge0}
       [c_j(f)2^{j/2}E_j]^4\right)^{1/4}.}
 \tag{1.6}
\]

Equivalently,

\[
 \|e^{t\Delta}f\|_{L_t^4L_x^6}
 \asymp
 \left(\sum_{j\ge0}2^{-2j}\|P_jf\|_6^4\right)^{1/4}
 =\left(\sum_{j\ge0}
 2^{-2j}\Theta_j(f)^{2/3}E_j^4\right)^{1/4}.
 \tag{1.7}
\]

The completion of the right side is the mean-zero periodic
\(B^{-1/2}_{6,4}\) heat-flow space.  This heat-semigroup/LP
characterization is classical; in particular, Chemin--Gallagher (2006,
Definitions 1.1 and 2.2) state the periodic thermic and dyadic versions.
Theorem 1.1 records the exact normalization and shell interface needed here;
it is not a new function-space theorem.

### Corollary 1.2: entrance to the R0.73Q tube

Let \(u\) be the fixed a priori global \(H^3\) reference orbit in R0.73Q,
with heat-flow stability radius \(\rho_{\mathfrak X}[u]>0\).  If an
\(H^3\) perturbation \(f\) satisfies

\[
 C_+\left(\sum_j
 2^{-2j}\Theta_j(f)^{2/3}E_j^4\right)^{1/4}
 <\rho_{\mathfrak X}[u],
 \tag{1.8}
\]

then \(u(t_0)+f\) starts a unique global strong solution for every restart
time \(t_0\ge0\).  The same conclusion holds when the exact \(\Theta_j\)
in (1.8) is replaced by any certified upper bound in Section 4.

This corollary still fixes a known global reference orbit.  It does not make
(1.8) follow from \(\|f\|_2\) alone.

## 2. Uniform annular heat multipliers

The proof uses the following standard periodic multiplier facts.

### Lemma 2.1

There are \(C_H,c_H>0\) such that

\[
 \|e^{t\Delta}P_jg\|_6
 \le C_He^{-c_H4^jt}\|P_jg\|_6,
 \qquad j\ge0,\ t\ge0.
 \tag{2.1}
\]

There are fixed \(0<A<B<\infty\) and \(C_I<\infty\) such that

\[
 \|P_jg\|_6\le C_I\|e^{t\Delta}g\|_6,
 \qquad t\in I_j:=[A4^{-j},B4^{-j}].
 \tag{2.2}
\]

The intervals may be chosen with uniformly bounded overlap.

### Proof

For \(j\ge1\), rescale the smooth annular symbol.  On its support,
\(|k|^2\asymp4^j\).  After extracting \(e^{-c_H4^jt}\), the rescaled
symbol and finitely many derivatives have bounds uniform in \(j\) and
\(t\).  Periodization of the corresponding Schwartz kernel gives a uniform
\(L^1\) kernel bound and hence (2.1).

For (2.2), the multiplier with symbol

\[
 \varphi_j(k)e^{t|k|^2}
 \tag{2.3}
\]

has the same uniform kernel property when \(t4^j\in[A,B]\).  Applied to
\(e^{t\Delta}g\), it returns \(P_jg\).  The low block contains only a fixed
set of nonzero frequencies and is absorbed into the constants.  Taking, for
example, intervals separated by a fixed factor of four gives bounded
overlap.  \(\square\)

## 3. Proof of Theorem 1.1

The LP synthesis inequality and Minkowski in \(L^3_x\) give

\[
 \|e^{t\Delta}f\|_6
 \le C\left\|\left(\sum_j
       |e^{t\Delta}f_j|^2\right)^{1/2}\right\|_6
 \le C\left(\sum_j\|e^{t\Delta}f_j\|_6^2\right)^{1/2}.
 \tag{3.1}
\]

Using (2.1), raising to the fourth power, and integrating,

\[
\begin{aligned}
 \|e^{t\Delta}f\|_{L_t^4L_x^6}^4
 &\le C\int_0^\infty
 \left(\sum_j e^{-2c_H4^jt}b_j^2\right)^2dt\\
 &\le C\sum_{j,k}{b_j^2b_k^2\over4^j+4^k}.
\end{aligned}
 \tag{3.2}
\]

Set \(a_j=2^{-j/2}b_j\).  Then

\[
 {b_j^2b_k^2\over4^j+4^k}
 =a_j^2a_k^2{2^{j+k}\over4^j+4^k}
 \le2^{-|j-k|}a_j^2a_k^2.
 \tag{3.3}
\]

The kernel \(K_n=2^{-|n|}\) belongs to \(\ell^1(\mathbb Z)\).  Young's
inequality on \(\ell^2\), applied to \(x_j=a_j^2\), yields

\[
 \sum_{j,k}K_{j-k}a_j^2a_k^2
 \le\|K\|_{\ell^1}\sum_ja_j^4.
 \tag{3.4}
\]

This proves the upper bound in (1.6).

For the lower bound, (2.2) gives for every \(t\in I_j\)

\[
 b_j^4\le C_I^4\|e^{t\Delta}f\|_6^4.
 \tag{3.5}
\]

Since \(|I_j|\asymp4^{-j}\),

\[
 2^{-2j}b_j^4
 \le C\int_{I_j}\|e^{t\Delta}f\|_6^4dt.
 \tag{3.6}
\]

Summation and bounded overlap prove

\[
 \sum_j2^{-2j}b_j^4
 \le C\|e^{t\Delta}f\|_{L_t^4L_x^6}^4.
 \tag{3.7}
\]

The theorem follows.  Finite LP truncations and Fatou give the corresponding
completion statement.  \(\square\)

### Why \(\ell^4\) is the exact shell exponent

Direct blockwise Minkowski gives the stronger assumption \(a\in\ell^1\).
Taking a triangle inequality after the square function gives the stronger
assumption \(a\in\ell^2\).  The proof above retains the heat-time kernel
before summing and reaches \(a\in\ell^4\).  The lower bound (3.7) proves
that neither an \(\ell^\infty\) condition nor cross-shell phase cancellation
can replace \(\ell^4\).

For example, if \(n\) disjoint smooth shells have \(a_j=1\), then
\(\sup_ja_j=1\) while the heat trace is bounded below by a constant times
\(n^{1/4}\).

## 4. Three levels of computable shell information

Write

\[
 f_j(x)=\sum_{k\in\mathbb Z^3}A_j(k)e^{ik\cdot x},
 \qquad A_j(k)\in\mathbb C^3,
 \tag{4.1}
\]

and let

\[
 S_j=\{k:A_j(k)\ne0\},
 \qquad M_j=|S_j|.
 \tag{4.2}
\]

### 4.1 Exact phase-sensitive convolution

For components \(r,m\in\{1,2,3\}\), define

\[
 \widetilde A_{j,r}(k)=\overline{A_{j,r}(-k)},
 \qquad
 T_{j,m}=\sum_{r=1}^3
 A_{j,r}*\widetilde A_{j,r}*A_{j,m}.
 \tag{4.3}
\]

The sequence \(T_{j,m}\) is the Fourier transform of
\(|f_j|^2f_{j,m}\).  Parseval gives the exact identity

\[
 \boxed{
 b_j^6=\sum_{m=1}^3\|T_{j,m}\|_{\ell^2}^2.}
 \tag{4.4}
\]

Thus (4.4) computes \(\Theta_j\) from finite Fourier data without spatial
quadrature.  Linear convolution is essential: an FFT certificate must pad
each frequency axis enough to contain the triple support.  Thresholding a
Fourier tail changes the certified field and is valid only when the removed
tail is bounded separately.

### 4.2 Additive multiplicity

Define

\[
 R_j=\max_n\#\{(k_1,k_2,k_3)\in S_j^3:
                    k_1+k_2+k_3=n\}.
 \tag{4.5}
\]

For a scalar component with Fourier sequence \(a\), Cauchy--Schwarz on each
triple sum gives

\[
 |(a*a*a)(n)|^2
 \le R_j\sum_{k_1+k_2+k_3=n}
 |a(k_1)a(k_2)a(k_3)|^2.
 \tag{4.6}
\]

After summing \(n\) and using Parseval,

\[
 \|f_{j,m}\|_6\le R_j^{1/6}\|A_{j,m}\|_{\ell^2}.
 \tag{4.7}
\]

Minkowski for the three components yields

\[
 b_j\le R_j^{1/6}E_j.
 \tag{4.8}
\]

Consequently,

\[
 \|f\|_{\mathfrak X}
 \le C\left(\sum_j2^{-2j}R_j^{2/3}E_j^4\right)^{1/4}.
 \tag{4.9}
\]

### 4.3 Support cardinality and effective support

Hausdorff--Young and Minkowski give

\[
 b_j
 \le\left(\sum_{m=1}^3
   \|A_{j,m}\|_{\ell^{6/5}}^2\right)^{1/2}
 \le M_j^{1/3}E_j.
 \tag{4.10}
\]

Hence

\[
 \|f\|_{\mathfrak X}
 \le C\left(\sum_j2^{-2j}M_j^{4/3}E_j^4\right)^{1/4}.
 \tag{4.11}
\]

One may replace \(M_j\) by the coefficient-sensitive effective support

\[
 M_{{\rm eff},j}
 :=\left(
 {\big(\sum_m\|A_{j,m}\|_{\ell^{6/5}}^2\big)^{1/2}
  \over E_j}
 \right)^3,
 \qquad 1\le M_{{\rm eff},j}\le M_j.
 \tag{4.12}
\]

The three levels have distinct meanings.  Equation (4.4) retains exact
phase and polarization.  The number \(R_j\) retains additive geometry but
forgets signs.  The number \(M_j\) retains only raw support size.  None of
these dimensionless numbers controls the heat trace without the weighted
energy sequence in (1.6).

## 5. A matched phase-coherence pair

The next construction shows that support, coefficient magnitudes, every
quadratic Sobolev norm, and \(L^2\) can all agree while the heat-flow trace
has a growing ratio.

Let \(m=2^r\), \(N=8m\), and

\[
 D_m(z)=\sum_{q=0}^{m-1}z^q.
 \tag{5.1}
\]

Define Rudin--Shapiro polynomials recursively by

\[
 P_1=Q_1=1,
 \qquad
 P_{2m}=P_m+z^mQ_m,
 \qquad
 Q_{2m}=P_m-z^mQ_m.
 \tag{5.2}
\]

Their coefficients are \(\pm1\), and induction gives

\[
 |P_m(e^{ix})|^2+|Q_m(e^{ix})|^2=2m,
 \qquad
 \|P_m\|_\infty\le\sqrt{2m}.
 \tag{5.3}
\]

For \(R_m=D_m\) or \(P_m\), put

\[
 W_{R,m}(x)
 ={\sqrt2\over m}e_3\operatorname{Re}\!\left[
 e^{iNx_1}R_m(e^{ix_1})R_m(e^{ix_2})
 \right].
 \tag{5.4}
\]

### Lemma 5.1: exact common quadratic data

The field \(W_{R,m}\) is real, smooth, mean zero, and divergence free.  Its
support consists of the \(2m^2\) sites

\[
 \{(N+q,s,0):0\le q,s<m\}
 \cup
 \{(-N-q,-s,0):0\le q,s<m\}.
 \tag{5.5}
\]

Every nonzero Fourier coefficient has magnitude \(1/(\sqrt2m)\).  Thus the
Dirichlet and Rudin--Shapiro fields have the same support, the same
coefficient magnitudes, \(L^2\) norm one, and the same value of every
quadratic Fourier-weighted Sobolev norm.

### Proof

The field has only an \(e_3\) component and is independent of \(x_3\), so it
is divergence free.  Expanding the real part gives (5.5) and the stated
coefficient magnitude.  Parseval then gives

\[
 \|W_{R,m}\|_2^2
 =2m^2{1\over2m^2}=1.
 \tag{5.6}
\]

Every quadratic Fourier-weighted norm depends only on the common sites and
coefficient magnitudes.  \(\square\)

### Lemma 5.2: exact sixth moments

If \(N>6(m-1)\), then

\[
 \|W_{R,m}\|_6^6
 ={5\over2m^6}\|R_m\|_6^{12}.
 \tag{5.7}
\]

Moreover,

\[
 \|D_m\|_6^6
 ={11m^5+5m^3+4m\over20}.
 \tag{5.8}
\]

Consequently,

\[
 \|W_{D,m}\|_6\asymp m^{2/3},
 \qquad
 (5/2)^{1/6}\le\|W_{P,m}\|_6\le40^{1/6}.
 \tag{5.9}
\]

### Proof

Write \(Z=e^{iNx_1}R_m(e^{ix_1})R_m(e^{ix_2})\).  In the expansion of
\((\operatorname{Re}Z)^6\), every term except \(Z^3\overline Z^3\) has a
nonzero carrier frequency.  The envelope width is at most \(6(m-1)\), so
those terms integrate to zero.  The neutral coefficient is

\[
 {1\over2^6}{6\choose3}={5\over16}.
 \tag{5.10}
\]

Multiplying by \((\sqrt2/m)^6\) and separating the two variables gives
(5.7).

For (5.8), let \(r_m(s)\) count triples from
\(\{0,\ldots,m-1\}\) with sum \(s\).  Then

\[
 \|D_m\|_6^6=\sum_{s=0}^{3m-3}r_m(s)^2,
 \tag{5.11}
\]

where

\[
 r_m(s)=\sum_{q=0}^3(-1)^q{3\choose q}
 {s-qm+2\choose2}_+.
 \tag{5.12}
\]

Splitting at \(m-1\) and \(2m-2\), using
\(r_m(s)=r_m(3m-3-s)\), and summing the resulting quartic polynomials gives
(5.8).

For Rudin--Shapiro, (5.3) and \(\|P_m\|_2^2=m\) imply

\[
 \|P_m\|_6^6
 \le\|P_m\|_\infty^4\|P_m\|_2^2
 \le4m^3.
 \tag{5.13}
\]

Equations (5.7)--(5.8) give (5.9).  For the sharper Rudin--Shapiro lower
bound, \(\|P_m\|_6\ge\|P_m\|_2=m^{1/2}\) in normalized measure, so (5.7)
gives \(\|W_{P,m}\|_6^6\ge5/2\).  \(\square\)

### Lemma 5.3: heat-flow separation

There are constants independent of \(m\) and \(R\) such that

\[
 \|W_{R,m}\|_{\mathfrak X}
 \asymp N^{-1/2}\|W_{R,m}\|_6.
 \tag{5.14}
\]

Therefore

\[
 \|W_{D,m}\|_{\mathfrak X}\asymp N^{-1/2}m^{2/3},
 \qquad
 \|W_{P,m}\|_{\mathfrak X}\asymp N^{-1/2}.
 \tag{5.15}
\]

### Proof

The common support lies in

\[
 N\le |k|\le
 \sqrt{(N+m-1)^2+(m-1)^2}
 <1.14N.
 \tag{5.16}
\]

Choose one smooth annular cutoff equal to one on this fixed-ratio annulus.
The upper annular heat multiplier gives

\[
 \|e^{t\Delta}W_{R,m}\|_6
 \le Ce^{-cN^2t}\|W_{R,m}\|_6.
 \tag{5.17}
\]

Integration gives the upper half of (5.14).  For
\(t\in[aN^{-2},bN^{-2}]\), the corresponding inverse heat multiplier is
uniformly bounded on \(L^6\); hence

\[
 \|W_{R,m}\|_6
 \le C\|e^{t\Delta}W_{R,m}\|_6.
 \tag{5.18}
\]

Integrating over that interval proves the lower half.  \(\square\)

### Theorem 5.4: same vanishing \(L^2\), different heat entry

Set

\[
 \alpha_m=N^{1/2}m^{-2/3}=\sqrt8\,m^{-1/6}.
 \tag{5.19}
\]

Then the two matched fields obey

\[
 \|\alpha_mW_{D,m}\|_2
 =\|\alpha_mW_{P,m}\|_2
 =\alpha_m\longrightarrow0,
 \tag{5.20}
\]

but

\[
 \|\alpha_mW_{D,m}\|_{\mathfrak X}\asymp1,
 \qquad
 \|\alpha_mW_{P,m}\|_{\mathfrak X}\asymp m^{-2/3}\longrightarrow0.
 \tag{5.21}
\]

Their complete quadratic Fourier data still agree.  Thus \(L^2\), maximum
frequency, shell scale, modal count, additive support geometry, Fourier
support, coefficient magnitudes, and all quadratic Sobolev norms do not
determine heat-flow entry.  The exact phase-sensitive convolution (4.4)
distinguishes the pair.

For any prescribed positive heat-ball threshold, multiplying both sequences
by one suitable fixed constant makes the Rudin--Shapiro sequence enter the
ball eventually while the Dirichlet sequence remains outside it.  This
comparison is about a sufficient norm threshold, not about safe versus
singular dynamics.

The common homogeneous half-derivative norm also has a fixed scale:

\[
 N\le \|W_{R,m}\|_{\dot H^{1/2}}^2
 \le {\sqrt{82}\over8}N,
 \qquad
 \|\alpha_mW_{R,m}\|_{\dot H^{1/2}}\asymp m^{1/3}.
 \tag{5.22}
\]

Thus the scaled pair has the same vanishing \(L^2\) norm and the same
diverging \(\dot H^{1/2}\) norm, while its critical heat traces separate.

## 6. Exact Navier--Stokes boundary of the example

Every field in (5.4) has the form \(e_3g(x_1,x_2)\).  Hence

\[
 (W_{R,m}\cdot\nabla)W_{R,m}
 =g\,\partial_3(e_3g)=0.
 \tag{6.1}
\]

Its unforced Navier--Stokes evolution is exactly the linear heat flow and is
globally smooth.  In particular, the coherent Dirichlet sequence in
(5.21) is not unsafe.  It only proves that failure of a small
\(\mathfrak X\) entrance is compatible with global regularity and that no
necessity claim is available.

The construction also shows why the support exponent cannot be improved
from cardinality alone.  A two-dimensional Dirichlet patch has
\(M\asymp m^2\) and

\[
 {\|W_{D,m}\|_6\over\|W_{D,m}\|_2}
 \asymp m^{2/3}=M^{1/3}.
 \tag{6.2}
\]

The divergence-free constraint does not by itself reduce the
Hausdorff--Young exponent.

## 7. Strict boundaries and value

The local synthesis does three precise things:

1. it turns the abstract R0.73Q heat-flow threshold into an auditable
   shellwise budget;
2. it separates exact phase coherence, additive support geometry, and raw
   modal count;
3. it gives an exact matched family showing which pieces of spectral data
   are insufficient.

Its analytic core is the classical heat-semigroup characterization of a
critical Besov space.  Finite-support Bernstein/Nikolskii bounds,
Rudin--Shapiro flatness, random-sign improvement, and general spectral-cluster
\(L^p\) improvements also have substantial prior literature.  The exact
Fourier certificate and the matched divergence-free Dirichlet/Rudin--Shapiro
pair are therefore presented as a local quantitative synthesis and an
auditable diagnostic, not as a new regularity theorem or a priority claim.

The exact convolution (4.4) is phase-sensitive but is an exact evaluation of
the shell \(L^6\) norm; it is not a lower-cost a priori proxy.  The quantities
\(R_j\) and \(M_j\) are lower-cost deterministic proxies, but they discard
phase.  A stronger future result would need a genuinely cheap phase-sensitive
upper certificate, a sharp extremal theorem, or a new Navier--Stokes
consequence beyond the existing oscillatory-data theory.

The following statements are not proved:

- smallness from \(L^2\) alone;
- necessity of \(\mathfrak X\) smallness;
- instability, blow-up, or singularity when the certificate fails;
- a fixed-background result without the R0.73Q a priori global orbit;
- nonperturbative \(BMO^{-1}\) uniqueness;
- arbitrary three-dimensional global regularity or the Clay conclusion.
