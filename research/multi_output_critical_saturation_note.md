# R0.59 — Tensor Rudin--Shapiro packets and multi-output critical saturation

## 1. Question and answer

R0.58 constructed one coherent low Fourier output from a flattened high
frequency shell.  It left open a possible escape route: perhaps a single
output is exceptional, while a growing family of low outputs must lose a
square-function factor.  This note gives an explicit negative answer to that
hope at the level of the first Navier--Stokes Picard iterate.

For every pair of dyadic integers \(L,M\), set \(H=4LM\).  We construct one
real, divergence-free trigonometric polynomial \(u_0\), supported in the
single shell

\[
 H\leq |\xi|<2H,
\tag{1.1}
\]

such that its first nonlinear Duhamel term at time
\(t_H=(\log2)/(2H^2)\) has coherent coefficients at all frequencies

\[
 K_M=\{(0,m,0):1\leq m\leq M\}.
\tag{1.2}
\]

The same sign array flattens both high-frequency inputs to size
\(O(\sqrt{LM})\), but it is squared on every matched output.  Consequently,
the normalized first-iterate quotient has a positive lower bound independent
of both \(L\) and \(M\) in the heat \(\dot B^{-1}_{\infty,\infty}\) norm and
in a periodic heat--Carleson \(BMO^{-1}\) norm.

This is a **multi-output critical-saturation theorem**.  It is not norm
inflation, an unboundedness result, or control of the full nonlinear solution.
It proves that merely replacing one output by a growing structured output set
does not force the missing shell-decay or square-function defect.

## 2. The packet

Let \(L=2^\ell\) and \(M=2^j\).  Let

\[
 P_L(z)=\sum_{n=0}^{L-1}a_nz^n,
 \qquad
 P_M(w)=\sum_{r=0}^{M-1}b_rw^r
\tag{2.1}
\]

be dyadic Rudin--Shapiro polynomials, so \(a_n,b_r\in\{-1,1\}\).
Use the tensor sign array

\[
 c_{r,n}=b_ra_n.
\tag{2.2}
\]

For \(0\leq r<M\), \(0\leq n<L\), write

\[
 R_{r,n}=H+rL+n,
 \qquad m_r=r+1,
\tag{2.3}
\]

and define

\[
 p_{r,n}=(R_{r,n},0,0),
 \qquad
 q_{r,n}=(-R_{r,n},m_r,0).
\tag{2.4}
\]

For an amplitude \(A>0\), prescribe the positive-side Fourier coefficients

\[
 \widehat U(p_{r,n})=Ac_{r,n}e_2,
 \qquad
 \widehat V(q_{r,n})=Ac_{r,n}e_3,
\tag{2.5}
\]

adjoin their conjugates at the negative frequencies, and set
\(u_0=U+V\).  The field is real and divergence free because
\(p_{r,n}\cdot e_2=q_{r,n}\cdot e_3=0\).

The whole packet lies in one shell.  Indeed,

\[
 H\leq R_{r,n}<H+LM=\frac54H,
 \qquad m_r\leq M\leq\frac14H,
\tag{2.6}
\]

and hence

\[
 |p_{r,n}|<\frac54H,
 \qquad
 |q_{r,n}|<\frac{\sqrt{26}}4H<2H.
\tag{2.7}
\]

The scale separation between the high shell and the largest target output is
\(H/M=4L\), so it can tend to infinity while \(|K_M|=M\) also tends to
infinity.

## 3. The full quadratic term reduces to one channel

The polarizations and variable dependence give the exact identities

\[
 U\cdot\nabla U=0,
 \qquad V\cdot\nabla V=0,
 \qquad V\cdot\nabla U=0.
\tag{3.1}
\]

They remain true after heat evolution.  Therefore the complete first Picard
term of \(u_0\), not merely a selected ordered bilinear block, is

\[
 \mathcal D_t(u_0,u_0)
 =-\int_0^t e^{(t-s)\Delta}\mathbb P
   \big((e^{s\Delta}U\cdot\nabla)e^{s\Delta}V\big)\,ds.
\tag{3.2}
\]

At the target frequency \(k_m=(0,m,0)\), equality
\(p_{r',n'}+q_{r,n}=k_m\) forces
\(R_{r',n'}=R_{r,n}\), hence \((r',n')=(r,n)\) and \(m=m_r\).
Thus the diagonal match is unique.  Moreover,

\[
 q_{r,n}\cdot e_2=m,
 \qquad \mathbb P_{k_m}e_3=e_3,
 \qquad c_{r,n}^2=1.
\tag{3.3}
\]

With the Fourier convention from R0.58, the positive coefficient is

\[
 \widehat{\mathcal D_t(u_0,u_0)}(k_m)
 =-iA^2d_m(t)e_3,
\tag{3.4}
\]

where the exact scalar is

\[
 \boxed{
 d_m(t)=m e^{-m^2t}
 \sum_{n=0}^{L-1}
 \frac{1-e^{-2R_{m-1,n}^2t}}{2R_{m-1,n}^2}.}
\tag{3.5}
\]

The heat denominator is again exactly \(2R_{m-1,n}^2\), because

\[
 |p_{m-1,n}|^2+|q_{m-1,n}|^2-|k_m|^2
 =2R_{m-1,n}^2.
\tag{3.6}
\]

At

\[
 t_H=\frac{\log2}{2H^2},
\tag{3.7}
\]

we have \(e^{-m^2t_H}>1/2\),
\(1-e^{-2R_{m-1,n}^2t_H}\geq1/2\), and
\((2R_{m-1,n}^2)^{-1}>8/(25H^2)\).  Therefore, for every
\(1\leq m\leq M\),

\[
 \boxed{
 \frac{2mL}{25H^2}<d_m(t_H)\leq\frac{mL}{2H^2}.}
\tag{3.8}
\]

All \(M\) target coefficients have the same physical phase.  If \(\Pi_0\)
denotes averaging in \(x_1\), the target part of the real output is exactly

\[
 \boxed{
 \Pi_0\mathcal D_{t_H}(u_0,u_0)(x)
 =2A^2\sum_{m=1}^M d_m(t_H)\sin(mx_2)e_3.}
\tag{3.9}
\]

## 4. One tensor sign array flattens both inputs

R0.58 proved the dyadic Rudin--Shapiro bounds

\[
 \|P_N\|_{L^\infty(\mathbb T)}\leq\sqrt{2N},
 \qquad
 \sup_{1\leq s\leq N}
 \left\|\sum_{n=0}^{s-1}a_nz^n\right\|_{L^\infty(\mathbb T)}
 \leq C_{\rm RS}\sqrt N,
\tag{4.1}
\]

where \(C_{\rm RS}=2+\sqrt2\).  The same holds for \(b_r\).

Order the tensor coefficients lexicographically by \((r,n)\), equivalently
by the consecutive integer \(R_{r,n}\).  Every prefix ending inside block
\(J\) has the form

\[
 z^Hw\left[
 P_L(z)\sum_{r=0}^{J-1}b_r(wz^L)^r
 +b_J(wz^L)^J\sum_{n=0}^{N-1}a_nz^n
 \right].
\tag{4.2}
\]

Consequently every two-variable tensor prefix is bounded by

\[
 \boxed{
 C_T\sqrt{LM},
 \qquad C_T=(1+\sqrt2)C_{\rm RS}.}
\tag{4.3}
\]

For \(U\), apply Abel summation to the decreasing weights
\(e^{-R_{r,n}^2s}\).  For \(V\), apply it to
\(e^{-(R_{r,n}^2+m_r^2)s}\), which are also decreasing in the same order.
After adjoining conjugates,

\[
 \|e^{s\Delta}U\|_\infty,
 \|e^{s\Delta}V\|_\infty
 \leq2C_TA\sqrt{LM}\,e^{-H^2s}.
\tag{4.4}
\]

Thus

\[
 \boxed{
 \|e^{s\Delta}u_0\|_\infty
 \leq4C_TA\sqrt{LM}\,e^{-H^2s}.}
\tag{4.5}
\]

The estimate is uniform in the number \(M\) of coherent target outputs.  The
same tensor signs appear in both inputs, so the matched nonlinear products in
(3.5) are \(c_{r,n}^2=1\).

## 5. The output projection cannot create the lower bound

The full output also contains frequencies with nonzero first coordinate.
They cannot invalidate the target lower bound.  For any periodic field, set

\[
 \Pi_0f(x)=\frac1{2\pi}\int_0^{2\pi}
 f(x_1+a,x_2,x_3)\,da.
\tag{5.1}
\]

This conditional expectation commutes with the heat flow and is an
\(L^\infty\) contraction.  Hence it is a contraction for

\[
 \|f\|_{\mathcal B^{-1}}
 :=\sup_{s>0}\sqrt{s}\,\|e^{s\Delta}f\|_\infty.
\tag{5.2}
\]

It is also a contraction for the periodic heat--Carleson norm

\[
 \|f\|_{BMO^{-1}_{\rm per}}
 :=\sup_{x,\,0<R\leq1}
 \left(\frac1{|B(x,R)|}\int_0^{R^2}\int_{B(x,R)}
 |e^{s\Delta}f(y)|^2\,dy\,ds\right)^{1/2}.
\tag{5.3}
\]

Indeed, Jensen's inequality bounds the squared conditional expectation by the
average of squared translates; every translated ball is another admissible
ball with the same radius.  Therefore

\[
 \|\Pi_0f\|_{\mathcal B^{-1}}\leq\|f\|_{\mathcal B^{-1}},
 \qquad
 \|\Pi_0f\|_{BMO^{-1}_{\rm per}}
 \leq\|f\|_{BMO^{-1}_{\rm per}}.
\tag{5.4}
\]

Thus a lower bound for (3.9) is automatically a lower bound for the complete
first Picard output.

## 6. Multi-output saturation in the heat Besov norm

From (4.5), \(LM=H/4\), and
\(\sup_{s>0}\sqrt{s}e^{-H^2s}=1/(H\sqrt{2e})\),

\[
 \boxed{
 \|u_0\|_{\mathcal B^{-1}}
 \leq\frac{\sqrt{2/e}\,C_TA}{\sqrt H}.}
\tag{6.1}
\]

For the projected output, apply an additional heat time

\[
 \sigma_M=\frac1{4M^2}
\tag{6.2}
\]

and evaluate at \(x_2=1/(2M)\).  For every \(m\leq M\),

\[
 e^{-m^2\sigma_M}\geq e^{-1/4},
 \qquad
 \sin\frac{m}{2M}\geq\frac{m}{4M}.
\tag{6.3}
\]

Using (3.8) and \(\sum_{m=1}^Mm^2\geq M^3/3\),

\[
 \left\|e^{\sigma_M\Delta}
 \Pi_0\mathcal D_{t_H}(u_0,u_0)\right\|_\infty
 \geq \frac{e^{-1/4}A^2LM^2}{75H^2}.
\tag{6.4}
\]

Multiplication by \(\sqrt{\sigma_M}=1/(2M)\) and \(LM=H/4\)
gives

\[
 \boxed{
 \|\mathcal D_{t_H}(u_0,u_0)\|_{\mathcal B^{-1}}
 \geq\frac{e^{-1/4}A^2}{600H}.}
\tag{6.5}
\]

Combining (6.1) and (6.5),

\[
 \boxed{
 \frac{\|\mathcal D_{t_H}(u_0,u_0)\|_{\mathcal B^{-1}}}
 {\|u_0\|_{\mathcal B^{-1}}^2}
 \geq\frac{e^{3/4}}{1200C_T^2}>0.}
\tag{6.6}
\]

The constant is independent of the shell \(H\), the separation parameter
\(L\), and the number \(M\) of target outputs.

## 7. Multi-output saturation in periodic \(BMO^{-1}\)

The \(L^\infty\) heat envelope (4.5), followed by integration to infinity,
gives

\[
 \boxed{
 \|u_0\|_{BMO^{-1}_{\rm per}}
 \leq\frac{\sqrt2C_TA}{\sqrt H}.}
\tag{7.1}
\]

For the output take

\[
 R_M=\frac1{8M},
 \qquad x_0=\left(0,\frac1{2M},0\right).
\tag{7.2}
\]

If \(y\in B(x_0,R_M)\), then
\(3/(8M)\leq y_2\leq5/(8M)\).  Hence, for all
\(m\leq M\) and \(0\leq s\leq R_M^2\),

\[
 \sin(my_2)\geq\frac{3m}{16M},
 \qquad e^{-m^2s}\geq e^{-1/64}.
\tag{7.3}
\]

Equations (3.8)--(3.9) imply the pointwise lower bound

\[
 \left|e^{s\Delta}\Pi_0
 \mathcal D_{t_H}(u_0,u_0)(y)\right|
 \geq\frac{e^{-1/64}A^2LM^2}{100H^2}.
\tag{7.4}
\]

Integrating this constant lower bound over the Carleson box, taking the
square root, and using \(LM=H/4\), we obtain

\[
 \boxed{
 \|\mathcal D_{t_H}(u_0,u_0)\|_{BMO^{-1}_{\rm per}}
 \geq\frac{e^{-1/64}A^2}{3200H}.}
\tag{7.5}
\]

Therefore

\[
 \boxed{
 \frac{\|\mathcal D_{t_H}(u_0,u_0)\|_{BMO^{-1}_{\rm per}}}
 {\|u_0\|_{BMO^{-1}_{\rm per}}^2}
 \geq\frac{e^{-1/64}}{6400C_T^2}>0.}
\tag{7.6}
\]

This disproves any uniform shell-decaying improvement based only on putting
many low outputs into an isotropic square-function or heat--Carleson norm.
An additional hypothesis would have to exclude the tensor phase structure or
use information beyond the first Picard iterate.

## 8. Energy bookkeeping

The target low modes do not violate the basic energy cancellation.  In fact,
the full quadratic output has first frequency coordinate either

\[
 |\xi_1|<LM=\frac14H
 \quad\hbox{or}\quad
 |\xi_1|\geq2H,
\tag{8.1}
\]

whereas the linear heat flow of \(u_0\) remains in
\(H\leq|\xi_1|<5H/4\).  Thus

\[
 \left\langle e^{t_H\Delta}u_0,
 \mathcal D_{t_H}(u_0,u_0)\right\rangle_{L^2}=0.
\tag{8.2}
\]

The instantaneous cancellation
\(\langle e^{s\Delta}u_0,
(e^{s\Delta}u_0\cdot\nabla)e^{s\Delta}u_0\rangle=0\)
also holds, here already by frequency support and by integration in \(x_2\).
Consequently, the positive \(L^2\) energy of the first nonlinear output is an
order-\(A^4\) term in a Picard expansion.  In the exact energy identity it
must be balanced by the interaction of the linear term with higher Picard
terms and by dissipation.  This is a precise reason why R0.59 cannot promote
the first-iterate theorem to a statement about the full solution without a
separate nonlinear-remainder analysis.

## 9. The theorem and its boundary

### Theorem — growing multi-output critical saturation

For every dyadic \(L,M\geq1\), let \(H=4LM\) and construct \(u_0\) by
(2.1)--(2.5).  Then:

1. \(u_0\) is a real smooth divergence-free field supported in the single
   shell \(H\leq|\xi|<2H\).
2. The complete first Navier--Stokes Picard output at
   \(t_H=(\log2)/(2H^2)\) has the exact projected form (3.9), with all
   \(M\) coefficients satisfying (3.8).
3. The number of coherent outputs is \(M\), while the high--low separation
   is \(H/M=4L\); both may tend to infinity.
4. The normalized quotients in heat \(\mathcal B^{-1}\) and periodic
   \(BMO^{-1}_{\rm per}\) satisfy the positive all-index lower bounds
   (6.6) and (7.6).
5. The linear and first nonlinear terms are exactly orthogonal in \(L^2\).

The theorem does **not** prove:

1. norm inflation or discontinuity of the solution map;
2. unboundedness of the Koch--Tataru bilinear map;
3. control or dominance of the first nonlinear output over higher iterates;
4. a compactly supported \(\mathbb R^3\) construction;
5. finite-time blow-up, large-data global regularity, or any resolution of
   the Clay Millennium problem.

If \(A\asymp\varepsilon\sqrt H\), then \(u_0\) has critical size
\(O(\varepsilon)\) and the first nonlinear output has size
\(\Omega(\varepsilon^2)\).  This is exactly compatible with a bounded
critical bilinear map.

## 10. Research value and next falsifiable test

R0.59 closes the smallest multi-output escape route left by R0.58.  A growing
set of low outputs, an isotropic heat square function, the complete quadratic
term of one divergence-free field, and exact energy orthogonality still do
not generate any extra shell factor.  Tensor phase flattening can preserve
coherence across all target modes at once.

The result is stronger than the R0.58 single-mode lemma, but its direct value
for the Clay problem remains low.  It is still an explicit first-iterate
obstruction, not a priori control for arbitrary smooth finite-energy data.
Its potential standalone publication value is moderate only if a broader
literature review confirms that this exact single-shell, growing-output,
periodic \(BMO^{-1}\) formulation is not already implicit in second-iterate
or norm-inflation constructions.  A targeted search is evidence about scope,
not proof of novelty.

R0.60 should no longer search for a shell gain inside the first quadratic
iterate under frequency separation alone.  The next falsifiable question is:

> After normalizing the R0.59 packet to fixed small critical size, can one
> prove a time-uniform bound for the sum of all Picard terms of order at least
> three on the window \(0\leq t\leq t_H\), with constants independent of both
> \(L\) and \(M\); or does an explicit third-order resonant family already
> destroy such dominance?

This question preserves the honest fork.  A uniform remainder bound would
turn the coherent first output into a genuine nonlinear statement.  A
third-order obstruction would identify exactly where the first-iterate
picture ceases to control the dynamics.

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
5. P. Balister, *Bounds on Rudin--Shapiro polynomials of arbitrary degree*,
   Journal of Fourier Analysis and Applications 26 (2020), Article 68,
   <https://arxiv.org/abs/1909.08777>.
