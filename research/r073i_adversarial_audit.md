# R0.73I adversarial audit

**Date:** 2026-08-30  
**Scope:** attempts to invalidate the scoped R0.73I endpoint, upper-action,
zero-window tangent, and fixed-window non-implication claims  
**Evidence class:** independent adversarial source-stage audit  
**Public status:** final adversarial pass for the scoped claims only

## 0. Verdict

The adversarial tests below do not invalidate the scoped R0.73I results.
Several attacks do invalidate stronger statements, but those stronger
statements are explicitly left open in the corrected source:

- a fixed-\(D\) action limit;
- a joint limit with \(D=D(\varepsilon)\);
- a launch-independent action without a rank-one theorem;
- a bounded prefactor from a logarithmic action alone;
- a continuum conclusion from the finite Fourier package.

## 1. Attack: a hidden factor four in the time variables

The physical-to-profile change is \(d=4t_{\rm physical}\).  On the selected
row, the physical viscous multiplier is

\[
 4\partial_x^2-1=-4L,
 \qquad
 L=-\partial_x^2+\frac14.
 \tag{1.1}
\]

Dividing the physical equation by \(d_t=4\) gives \(-L\) in profile time.
The fast time is \(\theta=\Lambda d\), so the fast generator contains
\(-\varepsilon L\), where \(\varepsilon=\Lambda^{-1}\).  Therefore

\[
 \theta_{\rm end}=\Lambda D=\frac D\varepsilon.
 \tag{1.2}
\]

There is no remaining factor four to insert into the action or endpoint.
This attack fails.

## 2. Attack: a hidden factor two in the kinetic numerical form

For \(\gamma=1/2\),

\[
 E_{1/2}(v)=\|v'\|_2^2+\frac14\|v\|_2^2,
 \qquad
 F_d(v)=\frac12\operatorname{Im}\int W_x(d)v'\overline v.
 \tag{2.1}
\]

The kinetic variable \(h=2L^{1/2}v\) obeys

\[
 \|h\|_2^2=4E_{1/2}(v),
 \qquad
 \operatorname{Re}\langle\widetilde A(d)h,h\rangle=4F_d(v).
 \tag{2.2}
\]

The factor four cancels in the quotient.  Since the square completion is
performed for both signs, the sign convention of the complex inner product
does not affect the upper numerical abscissa.  This attack fails.

## 3. Attack: the square completion has the wrong potential

Expanding

\[
 c\left\|v'+\frac{i\sigma}{4c}W_xv\right\|_2^2
 \tag{3.1}
\]

produces

\[
 c\|v'\|_2^2
 +\sigma\frac12\operatorname{Im}\int W_xv'\overline v
 +\frac1{16c}\int W_x^2|v|^2.
 \tag{3.2}
\]

Adding

\[
 c\int\left(\frac14-\frac{W_x^2}{16c^2}\right)|v|^2
 \tag{3.3}
\]

cancels the last term in (3.2) and leaves
\(cE_{1/2}+\sigma F_d\).  Thus the potential coefficient
\(-1/(16c^2)\) is exact.

With \(\vartheta=1/(36c^2)\),

\[
 -\vartheta\frac94=-\frac1{16c^2},
 \tag{3.4}
\]

and the constant term in the convex combination is

\[
 \vartheta+\left(\frac14-\vartheta\right)=\frac14.
 \tag{3.5}
\]

No coefficient mismatch remains.  This attack fails.

## 4. Attack: the viscous factor should be \(-D/2\) or disappear

The energy inequality is

\[
 \frac12(\|u\|_2^2)'
 \le\left[c_H(\varepsilon\theta)-\frac{\varepsilon}{4}\right]
 \|u\|_2^2.
 \tag{4.1}
\]

Dividing by \(\|u\|_2^2\) gives the derivative of
\(\log\|u\|_2\), not only of the squared norm:

\[
 (\log\|u\|_2)'
 \le c_H(\varepsilon\theta)-\frac{\varepsilon}{4}.
 \tag{4.2}
\]

Integration over \(D/\varepsilon\) gives exactly \(-D/4\).  A factor
\(-D/2\) would result from forgetting the leading one-half in (4.1), while
omitting the factor would discard \(L\ge I/4\).  Both alternatives are
incorrect.  This attack fails.

## 5. Attack: loss of strictness in the endpoint bound

The potentially weak step is

\[
 2\nu\le c_F-b.
 \tag{5.1}
\]

The source has both

\[
 c_F<a
 \qquad\hbox{and}\qquad
 b>0,
 \tag{5.2}
\]

so

\[
 2\nu\le c_F-b<a.
 \tag{5.3}
\]

The R0.73F roughness inequality is also strict:

\[
 C_A d_0<\frac{\nu}{16K^2}.
 \tag{5.4}
\]

Consequently,

\[
 d_0<\frac a{392}
 \le\frac{\sqrt{19/180}}{392}
 <\frac1{450}.
 \tag{5.5}
\]

The final comparison is strict because

\[
 \frac{21375}{153664}<1.
 \tag{5.6}
\]

No equality case survives.  This attack fails.

## 6. Attack: the zero-window theorem silently exchanges limits

The lower proof has the quantifier order

\[
 \zeta
 \longmapsto
 (\alpha_\zeta,b_\zeta,c_\zeta)
 \longmapsto
 (\nu_\zeta,K_\zeta,r_\zeta)
 \longmapsto
 d_\zeta.
 \tag{6.1}
\]

For a fixed \(D\le d_\zeta\), it then sends
\(\varepsilon\downarrow0\).  Only afterward does it send
\(D\downarrow0\), and finally \(\zeta\downarrow0\).  The upper proof uses
an independent margin \(\rho>0\) and sends \(\rho\downarrow0\) last.

An attempted joint path such as \(D=\varepsilon\) does not remove

\[
 \frac{\varepsilon}{D}\log K_{1,\zeta}
 \quad\hbox{or}\quad
 \frac{\varepsilon}{D}\log C_\rho.
 \tag{6.2}
\]

Therefore the present argument does not prove a joint limit.  The source
states this exclusion explicitly.  The attack invalidates only a stronger
unstated theorem, not the nested result.

The possible collapse \(d_\zeta\downarrow0\) as
\(\zeta\downarrow0\) also causes no contradiction: for each fixed
\(\zeta>0\), every sufficiently small \(D\) lies below its positive
\(d_\zeta\).  This is exactly the definition of the outer
\(D\downarrow0\) limit.  This attack fails.

## 7. Attack: the four tangent rates are not all squeezed

For every \(\varepsilon,D\),

\[
 m_\varepsilon(D)\le M_\varepsilon(D).
 \tag{7.1}
\]

R0.73F supplies the lower estimate for every unit vector in the complete
top block, so it bounds both \(m_\varepsilon\) and \(M_\varepsilon\) from
below.  The Volterra estimate bounds the full evolution norm, so it bounds
both quantities from above.  Hence both inner liminf and inner limsup for
both \(m\) and \(M\) are caught between the same outer lower and upper
limits.  There is no missing combination.  This attack fails.

## 8. Attack: the diagonal counterexample lacks the inherited structure

The active two-dimensional example is

\[
 A_{\rm diag}(d)
 =
 \begin{pmatrix}
 a+\kappa d&0\\
 0&a-\kappa d
 \end{pmatrix},
 \qquad
 L=I.
 \tag{8.1}
\]

Its exact gains from \(e_1,e_2\) are

\[
 G_{\varepsilon,\pm}(D)
 =
 \exp\left[
 \frac{aD\pm\kappa D^2/2}{\varepsilon}-D
 \right].
 \tag{8.2}
\]

Thus the actions differ by \(\kappa D^2\), while both launches are
eigenvectors in the same degenerate frozen top block.  Alternating the
allowed launch destroys the selected action limit.

The bounded finite-dimensional \(L\) is not essential.  Define

\[
 \mathcal H=\mathbb C^2\oplus\ell^2(\mathbb N),
 \qquad
 \mathcal L=I_2\oplus
 \operatorname{diag}(n^2+1)_{n\ge1},
 \tag{8.3}
\]

and extend

\[
 \mathcal A_{\rm diag}(d)
 =A_{\rm diag}(d)\oplus(-I).
 \tag{8.4}
\]

Then

\[
 \mathcal B_\varepsilon(d)
 =\mathcal A_{\rm diag}(d)-\varepsilon\mathcal L
 \tag{8.5}
\]

has domain \(D(\mathcal L)\) for \(\varepsilon>0\), while
\(\mathcal B_0(d)\) is bounded on all of \(\mathcal H\).  The complement is
uniformly stable, the top projection is fixed and finite rank, and the
drift norm is \(\kappa d\).  The original two top gains are unchanged.

For a concrete consistency check, choose

\[
 a=0.18,\quad
 \kappa=1,\quad
 \alpha=0.174,\quad
 b=0.170,\quad
 c_F=0.178.
 \tag{8.6}
\]

Then

\[
 \nu=0.004,\qquad
 \eta=0.002,\qquad
 r=0.176>0.17035.
 \tag{8.7}
\]

With \(K=1\), \(C_A=49/4\), and \(D_*=10^{-5}\),

\[
 C_A D_*=1.225\times10^{-4}
 <\frac{\nu}{16}=2.5\times10^{-4}.
 \tag{8.8}
\]

The numerical abscissa on this window is below \(0.181\), hence below the
R0.73I upper coefficient \(c_H(d)>0.324\).  Thus the counterexample can be
embedded into the same common-domain and singular-domain-jump architecture
while retaining the relevant abstract estimates.  This attack fails.

## 9. Attack: the Jordan prefactor violates the moving dichotomy

For

\[
 A_J(d)=
 \begin{pmatrix}
 a&0\\
 d&a
 \end{pmatrix},
 \qquad L=I,
 \tag{9.1}
\]

the exact endpoint from \(e_1\) is

\[
 U_\varepsilon(D/\varepsilon,0)e_1
 =
 e^{aD/\varepsilon-D}
 \left(e_1+\frac{D^2}{2\varepsilon}e_2\right).
 \tag{9.2}
\]

Therefore

\[
 G_\varepsilon(D)
 \sim
 \frac{D^2}{2}\varepsilon^{-1}e^{-D}e^{aD/\varepsilon}.
 \tag{9.3}
\]

The action is \(aD\), but the compensated prefactor grows like
\(\varepsilon^{-1}\).

For \(0\le s\le t\le D/\varepsilon\), the top transition matrix is

\[
 e^{(a-\varepsilon)(t-s)}
 \begin{pmatrix}
 1&0\\
 \frac{\varepsilon}{2}(t^2-s^2)&1
 \end{pmatrix}.
 \tag{9.4}
\]

Writing \(\tau=t-s\),

\[
 \frac{\varepsilon}{2}(t^2-s^2)
 \le D\tau.
 \tag{9.5}
\]

For every \(r<a\) and sufficiently small \(\varepsilon\), the inverse norm
is bounded by

\[
 e^{-r\tau}
 (1+D\tau)e^{-(a-r)\tau/2}.
 \tag{9.6}
\]

The product
\((1+D\tau)e^{-(a-r)\tau/2}\) is uniformly bounded.  Thus the polynomial
endpoint prefactor coexists with an every-vector inverse dichotomy at every
strict lower rate.  The same unbounded direct-sum extension as in Section 8
preserves this conclusion.  This attack fails.

## 10. Attack: the counterexamples prove too much about the PDE

The finite examples have different coefficients from the exact periodic
operator.  They therefore cannot prove that the exact PDE gain lacks an
action or bounded prefactor.

The corrected source does not make that inference.  The no-go note states
that the examples test the abstract information already extracted from
R0.73F--H.  The report says that the negative line concerns what follows
from the inherited hypotheses and explicitly leaves the exact PDE matching
action open.  The gap matrix labels the claims FALSE AS INFERENCE.

Thus the valid conclusion is

\[
 \mathcal H_{\rm abs}
 \not\Longrightarrow
 \text{unique action or bounded prefactor},
 \tag{10.1}
\]

not

\[
 \text{the exact PDE gain has no such asymptotic}.
 \tag{10.2}
\]

The source preserves this distinction.  This attack fails.

## 11. Attack: an action limit is enough for the prescribed seed

If

\[
 \Lambda^{-1}\log G_\Lambda(D)\to\mathcal A(D),
 \tag{11.1}
\]

then only

\[
 G_\Lambda(D)=e^{\Lambda\mathcal A(D)+o(\Lambda)}
 \tag{11.2}
\]

follows.  For the pure seed
\(\delta e^{-\Lambda\mathcal A(D)}\), the effective linear endpoint is

\[
 \delta e^{o(\Lambda)},
 \tag{11.3}
\]

which need not stay small or bounded away from zero.  The Jordan example
makes it grow like \(\delta\Lambda\).  A two-sided bounded prefactor or an
explicit polynomial correction is genuinely additional.  The source keeps
the prescribed-seed claim open.  This attack fails.

## 12. Attack: finite convergence is being used as a PDE certificate

The archived finite validation reports

\[
 \text{continuumConclusion}=\text{none}.
 \tag{12.1}
\]

The report labels \(N=48\) actions, WKB corrections, and residuals as finite
diagnostics.  It distinguishes:

- the explicit pilot \(D=10^{-4}\);
- the analytic upper bound \(D_{\rm ub}\), which is not \(d_0\);
- the legacy \(1/450\) endpoint, which is outside the inherited theorem
  interval.

The independent RK4 check is on the same finite kinetic-coordinate
generator.  It is not presented as an independent physical PDE derivation
after the source correction.  No cutoff comparison is promoted to a
Fourier-tail enclosure.  This attack fails.

## 13. Attack: open contracts are presented as proved

The problem freeze lists rank-one branch selection, uniform viscous
continuation, non-selfadjoint adiabatic tracking, backward action
localization, and prescribed-seed departure as future contracts.  The gap
matrix keeps each corresponding item open.  The report's finite two-term
formula is labelled a candidate, not a continuum theorem.

No open contract is used in the proofs of the endpoint bound, continuum
upper action, zero-window tangent theorem, or scoped no-go.  This attack
fails.

## 14. Final boundary

The adversarial pass applies only to:

- \(D=d_0<\sqrt{19/180}/392<1/450\);
- the upper bound
  \(\|U_\varepsilon(D/\varepsilon,0)\|
    \le e^{\Omega_H(D)/\varepsilon-D/4}\);
- the four nested zero-window tangent rates;
- the two logical non-implications from the extracted abstract outputs.

It does not pass or reject the still-open exact-PDE fixed-window action,
rank-one branch, two-term adiabatic law, nonlinear prescribed seed,
fixed-background instability, three-dimensional closure, singularity, or
Clay alternatives.

No adversarial test above invalidates the scoped R0.73I claims.
