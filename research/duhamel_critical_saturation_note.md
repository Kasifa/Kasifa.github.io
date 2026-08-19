# R0.58 — Exact Duhamel denominators and critical-space saturation

## 1. Scope and literature boundary

R0.57 gave a real divergence-free Fourier packet whose instantaneous
fixed-output interaction has sharp \(\ell^2\times\ell^2\) norm one.  The open
question was whether the time integral in the mild formulation supplies a
genuine high-frequency gain.  This note computes that integral exactly and
then measures the same packet in four different norms.

There are two distinct conclusions.

1. The Duhamel integral contributes an exact \(N^{-2}\) denominator.  It gives
   polynomial shell decay in the fixed-output block norm,
   \(\mathcal X^{-1}\), and \(\dot H^{1/2}\).
2. After a deterministic Rudin--Shapiro phase choice flattens the high shell,
   the same denominator is exactly critical in the heat
   \(\dot B^{-1}_{\infty,\infty}\) scale and in a periodic
   Koch--Tataru-type \(BMO^{-1}\) data norm: the normalized bilinear quotient
   has a positive lower bound independent of the shell.

The second conclusion is a **saturation theorem**, not a norm-inflation or
ill-posedness theorem.  In particular, an input of critical size \(\varepsilon\)
produces an output of size comparable to \(\varepsilon^2\), exactly as a
bounded bilinear map should.  It says that shell separation alone cannot add a
small factor to the standard critical estimate.

This distinction is required by the literature:

- Koch and Tataru proved unique global solutions for sufficiently small
  \(BMO^{-1}\) data.
- Bourgain and Pavlović proved norm inflation in the larger
  \(\dot B^{-1}_{\infty,\infty}\) space using coherent high-to-low transfer.
- Germain analyzed boundedness of the second Picard iterate and its relation
  to the Koch--Tataru theory.
- Coiculescu and Palasek proved that uniqueness can fail for some large
  \(BMO^{-1}\) initial data.  Their result concerns data at the critical
  regularity and does not settle the Clay problem for smooth finite-energy
  initial data.

The Rudin--Shapiro polynomial estimate below is proved directly, so no
external flat-polynomial theorem is needed for the result.  A targeted
literature search did not identify this exact one-shell Rudin--Shapiro packet
in the Navier--Stokes setting, but such a search is not a novelty proof.  The
classical high-to-low mechanism substantially limits any standalone novelty
claim.

## 2. The exact Duhamel coefficient

Work on \(\mathbb T^3\), set the viscosity to one by parabolic scaling, and
use the Fourier convention

\[
 \widehat{\mathcal D_t(U,V)}(k)
 =-i\int_0^t e^{-|k|^2(t-s)}P_k
   \sum_{p+q=k}(q\cdot e^{-|p|^2s}\widehat U(p))
                  e^{-|q|^2s}\widehat V(q)\,ds.
\tag{2.1}
\]

Fix \(k=e_2\).  For an integer \(L\geq1\) and
\(N=L,\ldots,2L-1\), take

\[
 p_N=(N,0,0),\qquad q_N=(-N,1,0)=k-p_N,
\tag{2.2}
\]

and real coefficients \(c_N\), with

\[
 \widehat U(p_N)=c_Ne_2,\qquad
 \widehat V(q_N)=c_Ne_3.
\tag{2.3}
\]

As in R0.57, the fields are divergence free,
\(q_N\cdot e_2=1\), \(P_ke_3=e_3\), and the exchanged interaction
vanishes.  Since

\[
 |p_N|^2=N^2,\qquad |q_N|^2=N^2+1,\qquad |k|^2=1,
\tag{2.4}
\]

the coefficient at \(k\) is, up to the unit phase \(-i\),

\[
 \boxed{
 d_L(t;c)
 =e^{-t}\sum_{N=L}^{2L-1}
 c_N^2\frac{1-e^{-2N^2t}}{2N^2}.}
\tag{2.5}
\]

Thus the missing time integration contributes the exact denominator
\(2N^2\).  No inequality has been used in (2.5).

For equal magnitudes \(|c_N|=A\), write

\[
 d_L(t;c)=A^2d_L(t),\qquad
 d_L(t)=e^{-t}\sum_{N=L}^{2L-1}
 \frac{1-e^{-2N^2t}}{2N^2}.
\tag{2.6}
\]

Choose the parabolic observation time

\[
 t_L=\frac{\log2}{2L^2}.
\tag{2.7}
\]

For every \(N\in[L,2L)\),

\[
 1-e^{-2N^2t_L}\geq\frac12,
 \qquad e^{-t_L}\geq\frac12,
 \qquad \frac1{2N^2}>\frac1{8L^2}.
\tag{2.8}
\]

The opposite inequalities \(1-e^{-2N^2t_L}\leq1\),
\(e^{-t_L}\leq1\), and \((2N^2)^{-1}\leq(2L^2)^{-1}\)
give the upper bound.  Hence

\[
 \boxed{
 \frac1{32L}\leq d_L(t_L)\leq\frac1{2L}
 \qquad(L=1,2,\ldots).}
\tag{2.9}
\]

The precise scaled limit also exists:

\[
 \boxed{
 \lim_{L\to\infty}L d_L(t_L)
 =\frac12\int_1^2\frac{1-2^{-x^2}}{x^2}\,dx>0.}
\tag{2.10}
\]

This is a Riemann-sum limit, not a numerical conjecture.

## 3. Three norms where the heat denominator gives shell decay

First use the real fields obtained by adjoining the conjugate coefficients at
\(-p_N\) and \(-q_N\).  The output has Fourier coefficients of magnitude
\(A^2d_L(t_L)\) at \(\pm k\); in physical space it is a sine wave of
amplitude \(2A^2d_L(t_L)\), up to translation and sign.

### 3.1 Fixed-output block norm

For the one-sided blocks, each \(\ell^2\) norm is \(A\sqrt L\).  Therefore

\[
 \frac{A^2d_L(t_L)}{(A\sqrt L)(A\sqrt L)}
 =\frac{d_L(t_L)}L
 \in\left[\frac1{32L^2},\frac1{2L^2}\right].
\tag{3.1}
\]

The instantaneous equality from R0.57 has become an \(L^{-2}\) gain.

### 3.2 Fourier \(\mathcal X^{-1}\)

Define

\[
 \|f\|_{\mathcal X^{-1}}
 =\sum_{m\neq0}|m|^{-1}|\widehat f(m)|.
\tag{3.2}
\]

The two real inputs satisfy

\[
 A\leq\|U\|_{\mathcal X^{-1}},\|V\|_{\mathcal X^{-1}}
 \leq2A,
\tag{3.3}
\]

while \(\|\mathcal D_{t_L}(U,V)\|_{\mathcal X^{-1}}
=2A^2d_L(t_L)\).  Consequently

\[
 \boxed{
 \frac1{64L}
 \leq
 \frac{\|\mathcal D_{t_L}(U,V)\|_{\mathcal X^{-1}}}
      {\|U\|_{\mathcal X^{-1}}\|V\|_{\mathcal X^{-1}}}
 \leq\frac1L.}
\tag{3.4}
\]

Signs cannot improve the \(\ell^1\) Fourier input norm, so the exact
denominator survives as an \(L^{-1}\) gain.

### 3.3 Critical Sobolev \(\dot H^{1/2}\)

With

\[
 \|f\|_{\dot H^{1/2}}^2
 =\sum_{m\neq0}|m||\widehat f(m)|^2,
\tag{3.5}
\]

each input norm is between \(\sqrt2AL\) and \(2AL\), while the
output norm is \(\sqrt2A^2d_L(t_L)\).  It follows that

\[
 \boxed{
 \frac1{64\sqrt2\,L^3}
 \leq
 \frac{\|\mathcal D_{t_L}(U,V)\|_{\dot H^{1/2}}}
      {\|U\|_{\dot H^{1/2}}\|V\|_{\dot H^{1/2}}}
 \leq\frac1{2\sqrt2\,L^3}.}
\tag{3.6}
\]

Here the positive half derivative on both high-frequency inputs adds two more
powers of \(L^{-1}\).

## 4. Rudin--Shapiro flattening of the high shell

Let \(L=2^m\).  Define the Rudin--Shapiro polynomials recursively by

\[
 P_0(z)=Q_0(z)=1,
\tag{4.1}
\]

\[
 P_{m+1}(z)=P_m(z)+z^{2^m}Q_m(z),\qquad
 Q_{m+1}(z)=P_m(z)-z^{2^m}Q_m(z).
\tag{4.2}
\]

Write

\[
 P_m(z)=\sum_{n=0}^{L-1}a_nz^n,
 \qquad a_n\in\{-1,1\}.
\tag{4.3}
\]

On \(|z|=1\), the parallelogram identity gives

\[
 |P_m(z)|^2+|Q_m(z)|^2=2L.
\tag{4.4}
\]

We also need a bound for every prefix.  Let \(M_m\) be the largest supremum
norm of a prefix of either \(P_m\) or \(Q_m\).  Splitting a prefix at its
dyadic midpoint and using (4.4) gives

\[
 M_m\leq M_{m-1}+2^{m/2},\qquad M_0=1.
\tag{4.5}
\]

Therefore, with

\[
 C_{\rm RS}=2+\sqrt2,
\tag{4.6}
\]

we have the all-level bound

\[
 \boxed{M_m\leq C_{\rm RS}\sqrt L.}
\tag{4.7}
\]

If \(w_0\geq\cdots\geq w_{L-1}\geq0\), Abel summation and (4.7)
give

\[
 \left|\sum_{n=0}^{L-1}a_nw_nz^n\right|
 \leq C_{\rm RS}\sqrt L\,w_0
 \qquad(|z|=1).
\tag{4.8}
\]

Now choose the Duhamel coefficients

\[
 c_{L+n}=Aa_n,
 \qquad n=0,\ldots,L-1,
\tag{4.9}
\]

in **both** input blocks.  The spatial phases flatten each high-frequency
input, but the matched nonlinear products are
\(c_{L+n}^2=A^2\), so every low-output contribution retains the same sign.

For either real heat-evolved input, (4.8) with
\(w_n=e^{-(L+n)^2s}\) gives

\[
 \boxed{
 \|e^{s\Delta}U\|_{L^\infty},
 \|e^{s\Delta}V\|_{L^\infty}
 \leq2C_{\rm RS}A\sqrt L\,e^{-L^2s}.}
\tag{4.10}
\]

This is the phase-flattening step that is invisible to
\(\mathcal X^{-1}\) and \(\dot H^{1/2}\).

## 5. Saturation in the heat \(\dot B^{-1}_{\infty,\infty}\) norm

Use the heat definition

\[
 \|f\|_{\mathcal B^{-1}}
 :=\sup_{s>0}\sqrt s\,\|e^{s\Delta}f\|_{L^\infty}.
\tag{5.1}
\]

Since \(\sup_{s>0}\sqrt s\,e^{-L^2s}=1/\sqrt{2eL^2}\),
(4.10) implies

\[
 \|U\|_{\mathcal B^{-1}},\|V\|_{\mathcal B^{-1}}
 \leq\frac{2C_{\rm RS}A}{\sqrt{2eL}}.
\tag{5.2}
\]

The low output is a unit-frequency sine wave with amplitude
\(2A^2d_L(t_L)\), so its heat norm is exactly

\[
 \|\mathcal D_{t_L}(U,V)\|_{\mathcal B^{-1}}
 =\frac{2A^2d_L(t_L)}{\sqrt{2e}}.
\tag{5.3}
\]

Combining (2.9), (5.2), and (5.3) yields the uniform lower bound

\[
 \boxed{
 \frac{\|\mathcal D_{t_L}(U,V)\|_{\mathcal B^{-1}}}
      {\|U\|_{\mathcal B^{-1}}\|V\|_{\mathcal B^{-1}}}
 \geq
 \frac{\sqrt e}{32\sqrt2\,C_{\rm RS}^2}>0.}
\tag{5.4}
\]

Thus the \(N^{-2}\) denominator is real, but the negative derivative in the
critical input norm and the \(\sqrt L\) phase flattening exactly compensate
its shell decay.

## 6. Saturation in periodic \(BMO^{-1}\)

For a mean-zero periodic distribution, define the local heat-Carleson norm

\[
 \|f\|_{BMO^{-1}_{\rm per}}
 :=\sup_{x\in\mathbb T^3,\,0<r\leq1}
 \left(
 \frac1{|B(x,r)|}\int_0^{r^2}\int_{B(x,r)}
 |e^{s\Delta}f(y)|^2\,dy\,ds
 \right)^{1/2}.
\tag{6.1}
\]

It is the periodic local analogue of the heat-extension norm used by
Koch--Tataru on \(\mathbb R^3\).  From (4.10),

\[
 \boxed{
 \|U\|_{BMO^{-1}_{\rm per}},
 \|V\|_{BMO^{-1}_{\rm per}}
 \leq\frac{\sqrt2C_{\rm RS}A}{\sqrt L}.}
\tag{6.2}
\]

Indeed, the normalized spatial average is bounded by the squared
\(L^\infty\) norm, and extending the time integral to infinity gives
\(4C_{\rm RS}^2A^2L\int_0^\infty e^{-2L^2s}ds
=2C_{\rm RS}^2A^2/L\).

For the low sine wave, take \(r_0=1/4\) and center the ball at a maximum.
On that ball the sine is at least \(\cos r_0\).  Therefore

\[
 \|\mathcal D_{t_L}(U,V)\|_{BMO^{-1}_{\rm per}}
 \geq c_0A^2d_L(t_L),
\tag{6.3}
\]

where

\[
 c_0=\sqrt2\cos(1/4)\sqrt{1-e^{-1/8}}>0.
\tag{6.4}
\]

Equations (2.9), (6.2), and (6.3) imply

\[
 \boxed{
 \frac{\|\mathcal D_{t_L}(U,V)\|_{BMO^{-1}_{\rm per}}}
      {\|U\|_{BMO^{-1}_{\rm per}}
       \|V\|_{BMO^{-1}_{\rm per}}}
 \geq\frac{c_0}{64C_{\rm RS}^2}>0.}
\tag{6.5}
\]

No shell-decaying improvement can hold for this periodic critical data norm
without adding a hypothesis that excludes the packet.

## 7. The no-go statement and its precise boundary

### Theorem — exact Duhamel gain versus critical saturation

For every dyadic \(L=2^m\), the real divergence-free packet
(2.2)--(2.3), (4.9), observed at \(t_L=(\log2)/(2L^2)\), has an exact
low-frequency Duhamel coefficient (2.5) satisfying (2.9).  Its normalized
bilinear quotient has the following shell scalings:

\[
 \begin{array}{c|c}
 \text{normalization}&\text{bilinear quotient}\
 \hline
 \text{fixed-output }\ell^2\times\ell^2&\Theta(L^{-2})\\
 \mathcal X^{-1}&\Theta(L^{-1})\\
 \dot H^{1/2}&\Theta(L^{-3})\\
 \mathcal B^{-1}&\Omega(1)\\
 BMO^{-1}_{\rm per}&\Omega(1).
 \end{array}
\tag{7.1}
\]

Consequently, the Duhamel denominator does give a summable gain in the first
three single-shell tests, but shell separation alone cannot improve the
critical heat-Besov or periodic heat-Carleson bilinear estimates by a factor
tending to zero.

The theorem does **not** assert any of the following:

1. norm inflation in \(BMO^{-1}\) or \(\mathcal B^{-1}\);
2. unboundedness of the Koch--Tataru bilinear map;
3. a construction on \(\mathbb R^3\) with compactly supported smooth data;
4. control of higher Picard iterates or the nonlinear remainder;
5. a finite-time singularity, a large-data regularity theorem, or a solution
   of the Clay Millennium problem.

The result is fully consistent with small-data well-posedness: after setting
\(A\asymp\varepsilon\sqrt L\), both inputs have critical size
\(O(\varepsilon)\), and the first nonlinear output has size
\(O(\varepsilon^2)\).

## 8. Research value and next falsifiable test

R0.58 decisively separates two questions that were conflated after R0.57.
The time integral itself is not harmless: it changes a constant-one
instantaneous block estimate into an \(L^{-2}\) block estimate.  But the
critical negative derivative and deterministic phase flattening can consume
that gain.  Therefore a future proof cannot obtain an extra high-frequency
small factor from heat denominators and shell separation alone in a
Koch--Tataru-type organization.

This is a rigorous obstruction lemma with a self-contained construction.  Its
direct value for the Clay problem remains low: it rules out an overoptimistic
estimate but supplies no arbitrary-data a priori bound.  Its potential paper
value is as one component of a broader theorem that either:

1. identifies an additional dynamically propagated condition that excludes
   Rudin--Shapiro-type phase flattening while retaining large smooth data; or
2. couples many output modes and proves that global energy, helicity, or
   pressure geometry forces a summable defect not visible at one low mode.

R0.59 will test the smallest such extension: replace the single low output by
a structured family of low outputs and ask whether one Rudin--Shapiro sign
sequence can keep **all** of them coherent while the periodic
\(BMO^{-1}\) input remains \(O(L^{-1/2})\).  The acceptance criterion is an
all-index multi-output theorem or an all-index obstruction, with the nonlinear
remainder still kept outside the claim until it is separately bounded.

## References

1. H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*,
   Advances in Mathematics 157 (2001), 22--35,
   <https://math.berkeley.edu/~tataru/papers/nas.pdf>.
2. J. Bourgain and N. Pavlović, *Ill-posedness of the Navier--Stokes equations
   in a critical space in 3D*, Journal of Functional Analysis 255 (2008),
   2233--2247, <https://arxiv.org/abs/0807.0882>.
3. P. Germain, *The second iterate for the Navier--Stokes equation*, Journal
   of Functional Analysis 255 (2008), 2248--2264,
   <https://arxiv.org/abs/0806.4525>.
4. A. Cheskidov and M. Dai, *Norm inflation for generalized Navier--Stokes
   equations*, Indiana University Mathematics Journal 63 (2014), 869--884,
   <https://arxiv.org/abs/1212.3801>.
5. M. P. Coiculescu and S. Palasek, *Non-uniqueness of smooth solutions of the
   Navier--Stokes equations from critical data*, Inventiones Mathematicae 244
   (2026), 165--219, <https://arxiv.org/abs/2503.14699>.
6. P. Balister, *Bounds on Rudin--Shapiro polynomials of arbitrary degree*,
   Journal of Fourier Analysis and Applications 26 (2020), Article 68,
   <https://arxiv.org/abs/1909.08777>.
