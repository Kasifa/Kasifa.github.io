# R0.70Z — Principal-eigengap sign no-go and the two-channel response lift

**Date:** 2026-08-25
**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity and harmonic-analysis formulations of vortex
stretching
**Status:** exact finite construction plus analytic lemmas; no enstrophy
closure and no regularity claim

## 1. Direct decision

R0.70Z closes the principal-eigengap sign/amplitude branch in one precise
sense and keeps one narrower branch open.

The negative result is definitive:

> A uniform absolute or relative gap between the first two eigenvalues of
> the complete-frame covariance \(Q\) does not determine the sign of the
> principal work
>
> \[
>  \mathfrak P_Q(\omega):=\int_{\mathbb T^3}S(\omega):Q(\omega)\,dx.
> \]

More strongly, there are two smooth real mean-zero divergence-free finite
Fourier fields

\[
 \omega_{\Lambda,+},\qquad \omega_{\Lambda,-}
 \tag{1.1}
\]

such that their pointwise frame covariances are identical,

\[
 Q(\omega_{\Lambda,+})(x)
 =Q(\omega_{\Lambda,-})(x),
 \tag{1.2}
\]

and satisfy

\[
 \lambda _1-\lambda _2\ge8\Lambda^2,
 \qquad
 \frac{\lambda _1-\lambda _2}{\lambda _1}\ge\frac23,
 \qquad
 \frac{\lambda _1-\lambda _2}{\operatorname{tr}Q}\ge\frac12,
 \tag{1.3}
\]

but

\[
 \boxed{
 \mathfrak P_Q(\omega_{\Lambda,\pm})
 =\pm\frac{9\sqrt{41}}{164}\Lambda^3.}
 \tag{1.4}
\]

Consequently no functional of \(Q\), its eigenvalues, its principal
projector, or its eigengap alone can supply a universal one-sided sign law
for the principal work. Scaling \(\Lambda\) also shows that the gap does not
turn this cubic work into a lower-order amplitude contribution.

The positive result is narrower but useful. If

\[
 Q=\sum_{j=1}^3\lambda_jP_j,
 \qquad \lambda_1>\lambda_2\ge\lambda_3,
 \tag{1.5}
\]

then the principal projector \(P_1\) has the exact derivative

\[
 D P_1[H]
 =\sum_{j=2}^3
 \frac{P_jHP_1+P_1HP_j}{\lambda_1-\lambda_j},
 \qquad
 |DP_1[H]|_F\le
 \frac{|H|_F}{\lambda_1-\lambda_2}.
 \tag{1.6}
\]

Thus the gap makes a covariance direction quantitatively stable. A natural
scale-correct upper majorant exposed by the gap is

\[
 \boxed{
 \chi_Q:=
 \frac{|\nabla Q|_F}{\lambda_1-\lambda_2}.}
 \tag{1.7}
\]

The quantity \(\chi_Q\) is a sharp, scale-correct upper majorant for
\(|\nabla P_1|\), not its exact or necessary value. Its spatial exponent
\(L^3\) is dimensionally critical and is invariant under the usual
whole-space (or rescaled-domain) Navier--Stokes scaling. On the fixed
normalized torus, dyadic scaling is exactly frame-covariant but replicates
the field, so the fixed-domain \(L^3\) norm is not invariant. The gap does
not bound either \(|\nabla P_1|\) or \(\chi_Q\); directional coherence,
strain alignment, or some other compensating structure would be required.

The pre-convolution branch also becomes exact. There is a two-channel
response lift whose traces recover full stretching, principal covariance,
and defect before convolution. It survives the R0.70X rank-one field.
However, its common-response channel remains order one in high--high--low
interactions. The summable \(2^{k-J}\) chord gain proved in R0.70Y therefore
cannot extend to the full stretching term by the same absolute shell
argument.

This is a gate result, not a solution of the three-dimensional regularity
problem.

## 2. Fixed setting

Work on the normalized torus \(\mathbb T^3\). Let \(\omega\) be smooth, real,
mean-zero, and divergence-free. Its mean-zero Biot--Savart velocity and
strain are

\[
 \widehat u(k)=\frac{i\,k\times\widehat\omega(k)}{|k|^2},
 \qquad
 S=\frac12(\nabla u+\nabla u^{\mathsf T}),
 \qquad \operatorname{tr}S=0.
 \tag{2.1}
\]

Use the same pinned real-even radial smooth Parseval frame as R0.70X--Y:

\[
 \sum_\alpha T_\alpha^2=I,
 \qquad
 \operatorname{supp}m_j
 \subset\{2^{j-1}<|k|<2^{j+1}\}.
 \tag{2.2}
\]

Write

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \mathcal D_\times=\omega\otimes\omega-Q.
 \tag{2.3}
\]

For nonzero frequencies,

\[
 V(k)=(m_\alpha(k))_\alpha,
 \quad
 \Gamma(p,q)=\langle V(p),V(q)\rangle,
 \quad
 K(p,q)=1-\Gamma(p,q)
 =\frac12\|V(p)-V(q)\|_{\ell^2}^2.
 \tag{2.4}
\]

The three cubic quantities are

\[
 \mathfrak I=\int S:(\omega\otimes\omega),
 \qquad
 \mathfrak P_Q=\int S:Q,
 \qquad
 \mathfrak E_S=\int S:\mathcal D_\times,
 \tag{2.5}
\]

with the exact split

\[
 \mathfrak I=\mathfrak P_Q+\mathfrak E_S.
 \tag{2.6}
\]

R0.70Y controls \(\mathfrak E_S\). The present question is whether a true
principal eigengap adds enough structure to control \(\mathfrak P_Q\).

## 3. Exact spectral algebra

Let

\[
 Q=\lambda_1P_1+\lambda_2P_2+\lambda_3P_3,
 \qquad
 \lambda_1>\lambda_2\ge\lambda_3\ge0.
 \tag{3.1}
\]

Put

\[
 g=\lambda_1-\lambda_2,
 \qquad
 d=\lambda_2-\lambda_3,
 \qquad
 s_j=P_j:S.
 \tag{3.2}
\]

Since \(s_1+s_2+s_3=0\),

\[
 \boxed{S:Q=g\,s_1-d\,s_3.}
 \tag{3.3}
\]

This identity already locates the obstruction. The principal gap \(g>0\)
multiplies the strain in the top covariance direction, but gives no sign for
\(s_1\). The lower spectral gap contributes a second independent signed
term.

An invariant decomposition makes the same point more sharply. Let

\[
 L=P_1,
 \qquad P=I-L,
 \qquad r=\lambda_2+\lambda_3,
 \qquad a=\lambda_1-\frac r2=g+\frac d2,
 \tag{3.4}
\]

and

\[
 D=PQP-\frac r2P=\frac d2(P_2-P_3).
 \tag{3.5}
\]

Then

\[
 Q-\frac{\operatorname{tr}Q}{3}I
 =a\left(L-\frac I3\right)+D,
 \qquad
 D:L=D:I=0,
 \tag{3.6}
\]

and the two pieces are Frobenius-orthogonal. Hence

\[
 \boxed{
 \left|Q-\frac{\operatorname{tr}Q}{3}I\right|_F^2
 =\frac23a^2+\frac12d^2.}
 \tag{3.7}
\]

Because \(S:I=0\), only this anisotropy is visible:

\[
 S:Q=a\,L:S+S:D.
 \tag{3.8}
\]

A positive gap therefore forces covariance anisotropy away from zero; it
does not make the pairing of that anisotropy with \(S\) small or sign
definite. The elementary pointwise pair

\[
 S_\pm=\pm\left(P_1-\frac I3\right)
 \tag{3.9}
\]

gives

\[
 S_\pm:Q
 =\pm\frac{2\lambda_1-\lambda_2-\lambda_3}{3},
 \tag{3.10}
\]

which is strictly positive for \(S_+\) and strictly negative for \(S_-\).

### 3.1 What a relative gap does give

Let \(E=\operatorname{tr}Q\), and suppose

\[
 g\ge\gamma E,
 \qquad 0<\gamma\le1.
 \tag{3.11}
\]

Then

\[
 \lambda_1\ge\frac{1+2\gamma}{3}E,
 \qquad
 \lambda_2+\lambda_3\le\frac{2(1-\gamma)}3E,
 \tag{3.12}
\]

\[
 d\le\frac{1-\gamma}{2}E,
 \qquad
 a\ge\gamma E.
 \tag{3.13}
\]

Thus a large relative gap makes the top axisymmetric component dominant in
size. It still does not choose the sign of \(L:S\). A sufficient sign
condition must explicitly include strain alignment. Put

\[
 s=L:S,
 \qquad
 T=PSP+\frac{s}{2}P,
\]

so that \(T\) is the trace-free part of the strain restricted to the lower
two-dimensional spectral plane. Then

\[
 S:Q=a\,s+T:D,
 \qquad s=L:S,
 \tag{3.14}
\]

and

\[
 |T:D|\le a\,c_\gamma|T|,
 \qquad
 c_\gamma=\frac{\sqrt2(1-\gamma)}{1+3\gamma}.
 \tag{3.15}
\]

Therefore \(s\ge c_\gamma|T|\) implies \(S:Q\ge0\). The alignment
condition, not the gap, supplies the sign.

## 4. The exact projector differential

At a simple top eigenvalue, define \(P=I-L\) and the reduced resolvent

\[
 \mathcal R_Q
 =P\Bigl((\lambda_1I-Q)|_{\operatorname{Ran}P}\Bigr)^{-1}P
 =\sum_{j=2}^3\frac{P_j}{\lambda_1-\lambda_j}.
 \tag{4.1}
\]

Here the inverse is taken only on \(\operatorname{Ran}P\); the full operator
\(\lambda_1I-Q\) is singular on \(\operatorname{Ran}L\). Differentiating
\(QL=\lambda_1L\) and \(L^2=L\) in a symmetric matrix direction \(H\) gives

\[
 \boxed{DL[H]=\mathcal R_QHL+LH\mathcal R_Q.}
 \tag{4.2}
\]

In an eigenbasis,

\[
 |DL[H]|_F^2
 =2\sum_{j=2}^3
 \frac{|e_j^{\mathsf T}He_1|^2}
 {(\lambda_1-\lambda_j)^2}
 \le\frac{|H|_F^2}{g^2}.
 \tag{4.3}
\]

The constant one is optimal. For a \(C^1\) covariance field,

\[
 |\nabla L|_F^2
 =2\sum_{\ell=1}^3\sum_{j=2}^3
 \frac{|e_j^{\mathsf T}(\partial_\ell Q)e_1|^2}
 {(\lambda_1-\lambda_j)^2},
\]

and therefore

\[
 \boxed{|\nabla L|_F\le\frac{|\nabla Q|_F}{g}.}
 \tag{4.4}
\]

Under a dyadic Navier--Stokes scaling \(\mu=2^m\), for which the fixed frame
changes only by an index shift,

\[
 \omega_\mu(x,t)=\mu^2\omega(\mu x,\mu^2t),
 \tag{4.5}
\]

one has

\[
 Q_\mu=\mu^4Q(\mu x,\mu^2t),
 \quad
 g_\mu=\mu^4g(\mu x,\mu^2t),
 \quad
 \chi_{Q_\mu}=\mu\chi_Q(\mu x,\mu^2t).
 \tag{4.6}
\]

Formula (4.6) is exactly frame-covariant under dyadic index shifts. On
\(\mathbb R^3\), or when the spatial domain is rescaled with the solution,
it makes \(\|\chi_Q\|_{L^3_x}\) invariant. On the fixed normalized torus,
integer dilation replicates the periodic field and instead gives
\(\|\chi_{Q_\mu}\|_{L^3}=\mu\|\chi_Q\|_{L^3}\). Thus \(L^3\) is the critical
dimensional exponent, but not a fixed-torus invariant norm.

The exact geometric coefficient is \(|\nabla L|\); \(\chi_Q\) is the sharp
upper majorant exposed by the spectral gap. It is not necessary: a diagonal
covariance with rapidly varying eigenvalues can have \(\nabla L=0\) while
\(\chi_Q\) is large. Conversely, a fixed relative gap alone does not control
\(|\nabla L|\): rotating rank-one projectors can have relative gap one and
arbitrarily large eigendirection variation.

There is also an exact integral identity. Assume that \(Q\) is \(C^1\), that
its top eigenvalue is globally simple (so \(L,a,D\) are \(C^1\)), and that
\(u\) is smooth, periodic, and divergence-free. Then

\[
 \boxed{
 \int_{\mathbb T^3}S:Q
 =-\int_{\mathbb T^3}u\cdot
 \left(L\nabla a+a\,\operatorname{div}L+\operatorname{div}D\right).}
 \tag{4.7}
\]

The gap therefore makes \(\operatorname{div}L\) estimable through (4.4), but
does not remove \(\nabla a\), \(\nabla Q/g\), or \(\operatorname{div}D\).

## 5. A six-mode field with nonzero principal work

Set

\[
 n=(1,1,0),
 \qquad p=(4,-5,0),
 \qquad q=(-5,4,0),
 \tag{5.1}
\]

and

\[
 c=(1,-1,0),
 \qquad a=e_3,
 \qquad b=\frac{(4,5,0)}{\sqrt{41}}.
 \tag{5.2}
\]

Then

\[
 n+p+q=0,
 \qquad n\cdot c=p\cdot a=q\cdot b=0,
 \tag{5.3}
\]

and

\[
 |n|^2=2,
 \qquad |p|^2=|q|^2=41,
 \qquad 41-16\cdot2=9>0.
 \tag{5.4}
\]

Define the real field

\[
 \xi(x)
 =c\cos(n\cdot x)
 +a\cos(p\cdot x)
 +b\cos(q\cdot x).
 \tag{5.5}
\]

The strict factor-four separation makes the radius-\(\sqrt2\) response
orthogonal to the radius-\(\sqrt{41}\) response, while \(p\) and \(q\) have
the same response. Writing \(\xi=\xi_L+\xi_H\),

\[
 Q(\xi)=\xi_L\otimes\xi_L+\xi_H\otimes\xi_H.
 \tag{5.6}
\]

Because \(|\xi_L|^2\le2\), while \(a\perp b\) gives
\(|\xi_H|^2=\cos^2(p\cdot x)+\cos^2(q\cdot x)\le2\),

\[
 \|Q(\xi)(x)\|_{op}
 \le\operatorname{tr}Q(\xi)(x)\le4.
 \tag{5.7}
\]

The six-mode Fourier/Parseval calculation gives

\[
 \boxed{
 \mathfrak P_Q(\xi)=\frac{9\sqrt{41}}{164}.}
 \tag{5.8}
\]

For comparison,

\[
 \mathfrak E_S(\xi)=-\frac{9\sqrt{41}}{3362},
 \qquad
 \mathfrak I(\xi)=\frac{351\sqrt{41}}{6724},
 \tag{5.9}
\]

and these satisfy (2.6) exactly.

## 6. The identical-\(Q\) eigengap sign pair

Use the separated shear filler

\[
 \eta(x)=e_2\left[\cos(49x_1)+\sin(197x_1)\right].
 \tag{6.1}
\]

Its two radii and the base radii obey

\[
 49^2-16\cdot41=1745,
 \qquad
 197^2-16\cdot49^2=393.
 \tag{6.2}
\]

Thus all four distinct radii \(2,41,49^2,197^2\) are separated by the
strict factor-four support rule. The two filler shells also have orthogonal
frame responses.

Let

\[
 h(x_1)=\cos^2(49x_1)+\sin^2(197x_1).
 \tag{6.3}
\]

The zero-set parity lemma from R0.70Y gives

\[
 \boxed{h(x_1)\ge\frac1{49^2+197^2}=\frac1{41210}.}
 \tag{6.4}
\]

Choose

\[
 C^2=12\cdot41210=494520
 \tag{6.5}
\]

and define, for \(\sigma\in\{-1,1\}\),

\[
 \omega_{\Lambda,\sigma}
 =\Lambda(\sigma\xi+C\eta).
 \tag{6.6}
\]

All cross-frame covariance terms vanish. Hence

\[
 \boxed{
 Q(\omega_{\Lambda,\sigma})
 =\Lambda^2\left[Q(\xi)+C^2h\,e_2\otimes e_2\right],}
 \tag{6.7}
\]

which is independent of \(\sigma\). In particular the two sign choices have
the same covariance at every point, not merely the same spectrum.

Put \(\alpha=C^2h\), \(A=\alpha e_2\otimes e_2\), and
\(B=Q(\xi)\). From (5.7) and (6.4),

\[
 \alpha\ge12,
 \qquad
 \lambda_1(B)\le\operatorname{tr}B\le4.
 \tag{6.8}
\]

Weyl monotonicity gives

\[
 \lambda_1(A+B)\ge\alpha,
 \qquad
 \lambda_2(A+B)\le4.
 \tag{6.9}
\]

After restoring \(\Lambda\),

\[
 \boxed{
 \lambda_1-\lambda_2\ge8\Lambda^2,
 \qquad
 \frac{\lambda_1-\lambda_2}{\lambda_1}\ge\frac23,
 \qquad
 \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}\ge\frac12.}
 \tag{6.10}
\]

The first ratio in (6.10) is top-normalized. The second is the
trace-relative gap used in Section 3: indeed
\(\operatorname{tr}(A+B)\le\alpha+4\) and
\(\lambda_1-\lambda_2\ge\alpha-4\), so its ratio is at least
\((\alpha-4)/(\alpha+4)\ge1/2\).

An exhaustive ten-mode check finds no zero-sum Fourier triple containing a
filler mode. The filler self-work is zero. Therefore the sign of the base
strain is the only surviving change in principal work, which proves (1.4).

### Theorem 6.1 — uniform eigengap does not determine principal-work sign

For the fixed real-even radial scalar Parseval frame described in Section 2
and every \(\Lambda>0\), the fields
\(\omega_{\Lambda,+}\) and \(\omega_{\Lambda,-}\) are smooth, real,
mean-zero, and divergence-free. They have identical pointwise covariance,
satisfy (6.10), and have opposite nonzero principal work (1.4).

This rules out:

1. a universal sign law for \(\mathfrak P_Q\) based only on \(Q\);
2. a claim that a true principal eigengap forces \(\mathfrak P_Q=0\);
3. any depletion statement in which increasing amplitude while preserving a
   relative gap makes the cubic principal work lower order.

It does **not** rule out a scale-homogeneous absolute estimate containing an
additional strain, derivative, alignment, or coherence factor.

## 7. The two-channel pre-convolution response lift

For each input pair \(p,q\), define in the response Hilbert space

\[
 U_{pq}=\frac{V(p)+V(q)}2,
 \qquad
 C_{pq}=\frac{V(p)-V(q)}2.
 \tag{7.1}
\]

Set

\[
 H^+_{pq}=U_{pq}\otimes U_{pq}+C_{pq}\otimes C_{pq},
 \tag{7.2}
\]

\[
 H^-_{pq}=U_{pq}\otimes U_{pq}-C_{pq}\otimes C_{pq},
 \qquad
 H^\Delta_{pq}=2C_{pq}\otimes C_{pq}.
 \tag{7.3}
\]

These obey the exact operator identity

\[
 H^+=H^-+H^\Delta
 \tag{7.4}
\]

and, because \(\|V(k)\|_{\ell^2}=1\),

\[
 \operatorname{tr}_{\mathcal R}H^+=1,
 \qquad
 \operatorname{tr}_{\mathcal R}H^-=\Gamma(p,q),
 \qquad
 \operatorname{tr}_{\mathcal R}H^\Delta=K(p,q).
 \tag{7.5}
\]

If \(a_p=\widehat\omega(p)\) and
\(a_p\odot a_q=(a_p\otimes a_q+a_q\otimes a_p)/2\), retain the response
indices before the \(p+q=r\) convolution:

\[
 \widehat{\mathbb M^\bullet}(r)
 =\sum_{p+q=r}H^\bullet_{pq}\otimes(a_p\odot a_q).
 \tag{7.6}
\]

Then

\[
 \boxed{
 \operatorname{tr}_{\mathcal R}\mathbb M^+
 =\omega\otimes\omega,
 \quad
 \operatorname{tr}_{\mathcal R}\mathbb M^-=Q,
 \quad
 \operatorname{tr}_{\mathcal R}\mathbb M^\Delta
 =\mathcal D_\times.}
 \tag{7.7}
\]

This is the cleanest response-index object found so far. It preserves the
common response and the response chord separately and does not vanish on the
R0.70X field merely because its physical covariance has rank at most one.

Indeed, the exact thirty-six-mode reconstruction gives

\[
 \mathfrak I=-\frac{137781}{32780},
 \qquad
 \mathfrak P_Q=\frac{81(\kappa-1)}{20},
 \qquad
 \mathfrak E_S
 =-\frac{81(1639\kappa+62)}{32780}.
 \tag{7.8}
\]

All three response traces are therefore visible before convolution.

## 8. Why the chord gain cannot control full stretching

For a resonant triad \(n+p+q=0\), write the three strain legs as
\(A_n,A_p,A_q\), and put \(B_n=|n|^2A_n\), cyclically. The exact identity is

\[
 B_n+B_p+B_q=0.
 \tag{8.1}
\]

The cyclic full, principal, and defect symbols are

\[
 \mathcal F=A_n+A_p+A_q,
 \tag{8.2}
\]

\[
 \mathcal P
 =\Gamma_{pq}A_n+\Gamma_{qn}A_p+\Gamma_{np}A_q,
 \tag{8.3}
\]

\[
 \mathcal G
 =K_{pq}A_n+K_{qn}A_p+K_{np}A_q,
 \qquad
 \mathcal F=\mathcal P+\mathcal G.
 \tag{8.4}
\]

On the sharp R0.70X high--high--low family,

\[
 (A_n,A_p,A_q)
 =\frac1{\sqrt{2M^2+2M+1}}
 (-M,-M-1,M),
 \tag{8.5}
\]

and \(\kappa_M=K(p,q)=O_{\mathscr T}(M^{-2})\). Consequently

\[
 \boxed{
 \mathcal F_M
 =-\frac{M+1}{\sqrt{2M^2+2M+1}},}
 \tag{8.6}
\]

\[
 \boxed{
 \mathcal P_M
 =-\frac{M(1-\kappa_M)}
 {\sqrt{2M^2+2M+1}},}
 \tag{8.7}
\]

\[
 \boxed{
 \mathcal G_M
 =-\frac{1+M\kappa_M}
 {\sqrt{2M^2+2M+1}}.}
 \tag{8.8}
\]

Thus \(\mathcal F_M\) and \(\mathcal P_M\) approach a nonzero constant, while
\(\mathcal G_M=O(M^{-1})\). The complete and principal terms retain the
common-response channel; only the defect loses its order-one high--high
interaction.

At the shell level, the defect has the summable uniform absolute majorant

\[
 h_m\simeq2^{-m},
 \tag{8.9}
\]

whereas the sharp family shows that any uniform absolute majorant for the
common-response part must stay bounded below along high--high--low
separations. Schematically, its worst-case kernel has

\[
 h_m\simeq1.
 \tag{8.10}
\]

Therefore the R0.70Y absolute proof in \(B^0_{3,3}\) and the mixed
\(B^0_{\infty,\infty}\)-\(L^2\) estimate cannot be copied to full stretching.
Safe absolute bounds revert to stronger shell summability such as
\(B^0_{3,1}\), or to established critical coefficients.

One such coefficient is BMO. For each component, set

\[
 h_j=\omega\cdot\nabla u_j.
 \tag{8.11}
\]

The divergence-free/curl-free Hardy-space estimate gives

\[
 \|h_j\|_{\mathcal H^1}
 \lesssim\|\omega\|_2\|\nabla u_j\|_2.
 \tag{8.12}
\]

By \(\mathcal H^1\)-BMO duality and
\(\|\nabla u\|_2\simeq\|\omega\|_2\),

\[
 \boxed{
 |\mathfrak I|
 \lesssim\|\omega\|_{\mathrm{BMO}}\|\omega\|_2^2.}
 \tag{8.13}
\]

This is a classical compensated-compactness mechanism, not a new frame
estimate. It supplies one classical endpoint control of the common channel;
the sharp family only rules out inheriting the R0.70Y chord decay and does
not exclude another signed or Carleson-type compensation. Leray energy
bounds alone do not provide the displayed BMO coefficient's time
integrability.

## 9. Literature boundary

The classical geometric criteria of Constantin--Fefferman and later work
control vortex stretching through regularity or coherence of a direction
field, not through a covariance eigengap alone
([Constantin--Fefferman 1993](https://iumj.org/article/3627/)). A more recent
locally varying-plane criterion likewise requires a bound on the gradient of
the plane normal, which is consistent with the appearance of
\(|\nabla Q|/g\) in (4.4)
([Miller 2020](https://arxiv.org/abs/2002.02152)).

Strain-spectrum criteria use eigenvalues of the physical strain tensor \(S\),
especially the positive part of its middle eigenvalue; they do not imply a
sign law for \(S:Q\) from the spectrum of the frame covariance \(Q\)
([Miller 2017/2020](https://arxiv.org/abs/1710.05569)).

The endpoint in (8.13) is based on the div--curl Hardy-space theorem of
Coifman, Lions, Meyer and Semmes, its periodic version or standard
transference, and Hardy--BMO duality
([CLMS 1993 zbMATH record](https://zbmath.org/0864.42009)).
The direct vorticity-BMO criterion appears in
[Kozono--Taniuchi 2000](https://doi.org/10.1007/s002090000130), while nearby
Besov continuation criteria are given by
[Kozono--Ogawa--Taniuchi 2003](https://doi.org/10.2206/kyushujm.57.303).

A bounded collision search using the exact phrases “frame covariance”,
“principal eigenvalue gap”, “Littlewood--Paley covariance tensor”, and
“spectral projector vorticity direction” did not locate the identical-\(Q\)
sign pair or the response operators (7.2)--(7.7). This is a literature
boundary only. It is not evidence of priority, and a publication-level
novelty statement would require a broader specialist search and external
review.

## 10. Research value

The principal-eigengap sign/amplitude branch is now sharply classified.

1. **Gap as geometry:** it forces anisotropy and makes the top projector
   stable under perturbation.
2. **Gap as sign:** it fails completely, even for two fields with the same
   pointwise \(Q\), top-normalized gap at least \(2/3\), and trace-relative
   gap at least \(1/2\).
3. **Gap as regularity input:** the gap alone is insufficient. The exact
   direction variable \(|\nabla L|\), its sufficient majorant \(\chi_Q\),
   and signed alignment such as \(L:S\) are candidate additions, not an
   exhaustive list of possible compensations.
4. **Response lift:** the two-channel tensor is an exact bookkeeping device,
   but the full term keeps a non-summable common-response channel.

The strongest R0.70Z component is Theorem 6.1. It is a clean no-go lemma that
prevents a large class of future arguments from confusing spectral
separation with nonlinear depletion. The response lift is useful
infrastructure, but its first audit points back to classical BMO/div--curl
control rather than a new closure.

This stage does not improve a known Navier--Stokes continuation criterion and
does not solve any part of the Clay problem in the theorem-reduction sense.
Its value is to remove a plausible but false route and isolate the additional
quantity that a viable geometric argument must control.

## 11. Next justified gate

The next stage should not enlarge the eigengap hypothesis by itself. It
should test one of two genuinely additional structures:

1. **projector coherence:** whether scale-critical control of the exact
   quantity \(|\nabla P_1|\), for example an admissible
   \(L_t^qL_x^p\) class with \(2/q+3/p=1\) such as
   \(L_t^\infty L_x^3\), combined with a quantitative relation between
   \(P_1\) and the physical vorticity direction, yields a non-tautological
   bound for \(\mathfrak P_Q\). The coefficient
   \(\chi_Q=|\nabla Q|/(\lambda_1-\lambda_2)\) may be tested as a sufficient
   upper bound, not treated as a necessary one; or
2. **response-trace compensation:** whether the common channel of
   \(\mathbb M^+\) has a Carleson/div--curl cancellation stronger than its
   Schatten-\(S_1\) trace bound, without merely restating the classical BMO
   criterion.

The stopping rule is strict: if either route reduces exactly to an existing
conditional criterion, it should be recorded as an equivalence and closed,
not promoted as progress toward unconditional regularity.

No large DNS, stochastic search, GPU, or DGX computation is justified before
this analytic gate is decided.

## 12. Reproduction boundary

Run

~~~bash
tmp/r068b-venv/bin/python research/r070z_exact_audit.py
~~~

The producer checks six finite groups:

1. trace-free spectral and anisotropy identities;
2. the principal-projector derivative residuals;
3. the six-mode principal/full/defect work split;
4. equality of every covariance Fourier coefficient for the sign pair;
5. the ten-mode resonance ledger and the eigengap constants \(8\),
   \(2/3\), and \(1/2\); and
6. the response-lift traces, the R0.70X full/principal/defect reconstruction,
   and the sharp common/chord HHL formulas.

The finite certificate does not prove the zero-set lemma, Weyl inequalities,
the analytic projector estimates, the shell summation boundary, the
div--curl theorem, a new continuation criterion, global regularity, or a
solution of the Millennium problem. Those dependencies and limits are
stated explicitly above.

No public-page update or GitHub publication is part of R0.70Z.
