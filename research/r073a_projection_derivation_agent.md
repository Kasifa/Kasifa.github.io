# R0.73A internal derivation: the moving tangent projection

**Status:** independent analytic lane; internal working note only
**Date:** 2026-08-29
**Scope:** the abstract mean-zero Orr--Sommerfeld row at
\(\beta=\mu=0\), its exact tangent solution, and the obstruction to a
uniform continuation as \((\beta,\mu)\to(0,0)\).  This note does not assert a
physical \(\mu=0\) velocity theorem, a low-gap propagator theorem, or a
nonlinear Navier--Stokes estimate.

No literature claim is used below.  Every conclusion is obtained directly
from the R0.72Z equation and finite Fourier algebra.

---

## 0. Direct decision

There are three different meanings of “rank-one closure,” and they must not
be conflated.

1. The moving line \(E(d)=\operatorname{span}\{W_{xx}(d)\}\) is an exact
   trajectory bundle: its generator vector is an exact solution.  For every
   differentiable normalized dual, the quotient/complement variable obeys a
   closed triangular equation.  This part is an exact algebraic theorem.
2. The original OS equation splits into two invariant blocks only if the dual
   solves the transported adjoint equation \(\psi_d=-\mathscr A_0^*\psi\).
   That equation is forward anti-parabolic.  When \(c\ne0\), the pressure
   adjoint also generates new Fourier modes, so the transported dual is not a
   finite-dimensional construction and its uniform control is an analytic
   problem of essentially the same low-gap type as the desired propagator
   estimate.  At \(c=0\), finite Fourier support is preserved, although
   generic \(L^2\) forward anti-heat evolution is still ill-posed.
3. The instantaneous orthogonal projection is completely explicit and has
   \(\|P_d\|\le 3/2\), but its complement-to-tangent block contains a
   nonzero \(ic\mathscr B_0^*W_{xx}\) term.  The resulting complement equation
   is closed but is not a small or contractive perturbation when \(|c|\) is
   large.

For the coupled row \(c\ne0\), the fixed two-dimensional carrier

\[
 \mathcal S=\operatorname{span}\{\sin x,\sin2x\}
\]

is the minimal fixed Fourier space containing the tangent path and its time
derivative.  It is therefore more natural kinematically than the moving line.
It is not invariant under the full OS operator when \(c\ne0\): one independent
direction in \(\mathcal S\) leaks into \(\cos x-\cos3x\), and the next
application creates higher harmonics.  At \(c=0\), the generator is the heat
operator and \(\mathcal S\) is invariant.

Finally, on the full \(g=\beta^2+\mu>0\) row, normalization of any rank-one
dual forces a constant Fourier coefficient through
\(\mathcal L_{\beta,\mu}^{-1}M_{W_{xx}}\).  Either the projection norm or its
unscaled adjoint pressure block must diverge at least on the \(g^{-1}\) scale.
The full OS pressure block carries the additional factor \(|c|\).  The
mean-zero projection at exactly \(g=0\) removes this mode, but the endpoint
acts on a different space; no operator-norm continuity claim is made without
an explicit common-space identification.

---

## 1. Frozen notation and the exact tangent orbit

Use the normalized pairing

\[
 \langle f,g\rangle_0
 =\frac1{2\pi}\int_0^{2\pi}\overline{f(x)}g(x)\,dx,
 \tag{1.1}
\]

which is conjugate-linear in the first argument.  Let

\[
 H_0=L^2_0(\mathbb T;\mathbb C),\qquad
 \mathcal L_0=-\partial_x^2\quad\hbox{on }H_0,
 \tag{1.2}
\]

and write

\[
 a=e^{-d},\qquad b=e^{-4d},
 \tag{1.3}
\]

\[
 W=-\frac a2\sin x+\frac b4\sin2x,
 \qquad
 \phi:=W_{xx}=\frac a2\sin x-b\sin2x.
 \tag{1.4}
\]

The abstract gapless OS generator is

\[
 \mathscr A_0(d)q
 =-\mathcal L_0q-ic\mathscr B_0(d)q,
 \tag{1.5}
\]

\[
 \mathscr B_0q
 =Wq+\phi\mathcal L_0^{-1}q.
 \tag{1.6}
\]

For \(q\in H_0\), the two terms in (1.6) have cancelling means, so
\(\mathscr B_0:H_0\to H_0\).  Since

\[
 \mathcal L_0^{-1}\phi=-W,
 \tag{1.7}
\]

one has

\[
 \mathscr B_0\phi=W\phi-\phi W=0.
 \tag{1.8}
\]

Moreover,

\[
 \phi_d=-\frac a2\sin x+4b\sin2x
 =-\mathcal L_0\phi.
 \tag{1.9}
\]

Therefore

\[
 \boxed{\phi_d=\mathscr A_0(d)\phi.}
 \tag{1.10}
\]

Equation (1.10), not an instantaneous eigenvector identity, is the exact
tangent statement.  In particular, \(\phi_d\) is not proportional to
\(\phi\) while both Fourier modes are present.

The adjoint of (1.6) on \(H_0\) is

\[
 \boxed{
 \mathscr B_0^*
 =\Pi_0M_W+\mathcal L_0^{-1}\Pi_0M_\phi,}
 \tag{1.11}
\]

where \(\Pi_0\) removes the constant mode.  Indeed, for \(f,g\in H_0\),

\[
 \langle f,M_Wg\rangle_0
 =\langle\Pi_0(Wf),g\rangle_0,
 \tag{1.12}
\]

\[
 \langle f,M_\phi\mathcal L_0^{-1}g\rangle_0
 =\langle\mathcal L_0^{-1}\Pi_0(\phi f),g\rangle_0.
 \tag{1.13}
\]

Thus

\[
 \mathscr A_0^*=-\mathcal L_0+ic\mathscr B_0^*.
 \tag{1.14}
\]

---

## 2. General moving rank-one projection

For vectors \(u,v\in H_0\), use the tensor convention

\[
 (u\otimes v)f=u\langle v,f\rangle_0.
 \tag{2.1}
\]

Let \(\psi\in C^1(I;H_0)\) satisfy
\(\psi(d)\in D(\mathscr A_0(d)^*)\), with
\(d\mapsto\mathscr A_0(d)^*\psi(d)\) continuous, and suppose

\[
 \boxed{\langle\psi(d),\phi(d)\rangle_0=1.}
 \tag{2.2}
\]

Define

\[
 P=\phi\otimes\psi,
 \qquad Q=I-P.
 \tag{2.3}
\]

Then

\[
 P^2f
 =\phi\langle\psi,\phi\rangle_0\langle\psi,f\rangle_0
 =Pf,
 \tag{2.4}
\]

so \(P\) is a rank-one projection, not necessarily orthogonal.  Its exact
derivative is

\[
 \boxed{P_d=\phi_d\otimes\psi+\phi\otimes\psi_d.}
 \tag{2.5}
\]

Differentiating (2.2) gives the mandatory normalization ledger

\[
 \boxed{
 \langle\psi_d,\phi\rangle_0
 +\langle\psi,\phi_d\rangle_0=0.}
 \tag{2.6}
\]

### 2.1 The two off-diagonal OS blocks

Since \(\mathscr A_0\phi=\phi_d\),

\[
 \mathscr A_0P=\phi_d\otimes\psi.
 \tag{2.7}
\]

Consequently,

\[
 \boxed{
 Q\mathscr A_0P=(Q\phi_d)\otimes\psi.}
 \tag{2.8}
\]

On the other side,

\[
 P\mathscr A_0Qf
 =\phi\langle\psi,\mathscr A_0Qf\rangle_0
 =\phi\langle Q^*\mathscr A_0^*\psi,f\rangle_0,
 \tag{2.9}
\]

hence

\[
 \boxed{
 P\mathscr A_0Q
 =\phi\otimes(Q^*\mathscr A_0^*\psi).}
 \tag{2.10}
\]

The derivative blocks are just as explicit.  Equations (2.5)--(2.6) give

\[
 P_dP
 =\bigl(\phi_d-\phi\langle\psi,\phi_d\rangle_0\bigr)
   \otimes\psi
 =(Q\phi_d)\otimes\psi,
 \tag{2.11}
\]

and therefore

\[
 \boxed{P_dP=Q\mathscr A_0P.}
 \tag{2.12}
\]

Also,

\[
 \boxed{P_dQ=\phi\otimes(Q^*\psi_d).}
 \tag{2.13}
\]

Identity (2.12) is the precise cancellation that makes the quotient equation
triangular even though \(Q\mathscr A_0P\ne0\).

### 2.2 Amplitude and complement equations

Before specializing the rank-one coordinate, differentiation of
\(p=Pq\) and \(z=Qq\) gives the exact moving-block system

\[
 p_d=(P_dP+P\mathscr A_0P)p
 +(P_dQ+P\mathscr A_0Q)z,
 \tag{2.13a}
\]

\[
 z_d=(Q\mathscr A_0P-P_dP)p
 +(Q\mathscr A_0Q-P_dQ)z.
 \tag{2.13b}
\]

The first coefficient in (2.13b) vanishes exactly by (2.12).

Let \(q\in C^1(I;H_0)\) be a strong solution of
\(q_d=\mathscr A_0q\), with \(q(d)\in D(\mathscr A_0(d))\), and decompose

\[
 a_*(d)=\langle\psi,q\rangle_0,
 \qquad z=Qq,
 \qquad q=a_*\phi+z,
 \qquad\langle\psi,z\rangle_0=0.
 \tag{2.14}
\]

Put

\[
 h_\psi:=\psi_d+\mathscr A_0^*\psi.
 \tag{2.15}
\]

The exact tangent equation and the differentiated normalization imply

\[
\begin{aligned}
 \langle h_\psi,\phi\rangle_0
 &=\langle\psi_d,\phi\rangle_0
   +\langle\mathscr A_0^*\psi,\phi\rangle_0\\
 &=-\langle\psi,\phi_d\rangle_0
   +\langle\psi,\mathscr A_0\phi\rangle_0=0.
\end{aligned}
\tag{2.16}
\]

Therefore

\[
\begin{aligned}
 (a_*)_d
 &=\langle\psi_d,q\rangle_0
   +\langle\psi,\mathscr A_0q\rangle_0\\
 &=\langle h_\psi,z\rangle_0,
\end{aligned}
\tag{2.17}
\]

and

\[
\begin{aligned}
 z_d
 &=q_d-(a_*)_d\phi-a_*\phi_d\\
 &=\mathscr A_0z-\phi\langle h_\psi,z\rangle_0.
\end{aligned}
\tag{2.18}
\]

Equivalently,

\[
 \boxed{
 z_d=(Q\mathscr A_0Q-P_dQ)z
 =\mathscr A_0z-\phi\langle
 \psi_d+\mathscr A_0^*\psi,z\rangle_0.}
 \tag{2.19}
\]

This is a closed equation in \(z\).  There is no forcing from the tangent
amplitude \(a_*\).  The full system is triangular, however: the complement
can force \(a_*\) through (2.17).

Conversely, if (2.19) is solved with
\(\langle\psi(d_0),z(d_0)\rangle_0=0\), then

\[
 \frac d{dd}\langle\psi,z\rangle_0
 =\langle\psi_d+\mathscr A_0^*\psi,z\rangle_0
 -\langle\psi,\phi\rangle_0
  \langle\psi_d+\mathscr A_0^*\psi,z\rangle_0=0.
 \tag{2.19a}
\]

Thus the moving constraint is propagated by the standalone complement
equation; “closed” here is literal, not merely a formal substitution.

### 2.3 Exact invariant complement and the transported dual

The complement ceases to force the amplitude for every
\(z\in\ker\psi\) exactly when

\[
 \langle h_\psi,z\rangle_0=0
 \quad\hbox{for every }z\in\ker\psi.
 \tag{2.20}
\]

The annihilator of \(\ker\psi\) is \(\operatorname{span}\{\psi\}\).  But
(2.16) and \(\langle\psi,\phi\rangle_0=1\) force the coefficient of \(\psi\)
to vanish.  Thus (2.20) is equivalent to

\[
 \boxed{\psi_d=-\mathscr A_0^*\psi.}
 \tag{2.21}
\]

Under (2.21),

\[
 \boxed{P_d=\mathscr A_0P-P\mathscr A_0,}
 \tag{2.22}
\]

\[
 (a_*)_d=0,
 \qquad z_d=\mathscr A_0z.
 \tag{2.23}
\]

This is the exact two-sided invariant splitting under the stated domain and
regularity hypotheses.  Its uniform all-start realization is conditional.
Indeed, (1.14) turns (2.21) into

\[
 \psi_d=\mathcal L_0\psi-ic\mathscr B_0^*\psi.
 \tag{2.24}
\]

The leading term is forward anti-heat.  Its \(n\)-th Fourier component grows
like \(e^{n^2(d-d_0)}\).  Generic \(L^2\) initial data therefore do not define
a forward \(L^2\) dual.  For \(c\ne0\), the pressure term also creates new
Fourier modes; at \(c=0\), finite Fourier support is preserved.  A
terminal-value adjoint can be evolved backward in \(d\), but obtaining one
family for all start times with uniform projection norm is precisely an
additional analytic estimate.

---

## 3. The explicit orthogonal rank-one projection

The least-norm normalized dual is

\[
 \psi_\perp=\frac{\phi}{N},
 \qquad
 N=\|\phi\|_0^2=\frac{a^2}{8}+\frac{b^2}{2}.
 \tag{3.1}
\]

Then \(P_\perp=\phi\otimes\phi/N\) is orthogonal and
\(\|P_\perp\|=1\).

Set

\[
 A_1=\frac a2,
 \qquad
 \theta=b\sin x+A_1\sin2x.
 \tag{3.2}
\]

One checks directly that

\[
 \langle\theta,\phi\rangle_0=0,
 \qquad \|\theta\|_0^2=N.
 \tag{3.3}
\]

Write

\[
 \kappa=\frac{\langle\phi,\phi_d\rangle_0}{N}
 =-\frac{A_1^2+4b^2}{A_1^2+b^2},
 \tag{3.4}
\]

\[
 \omega=\frac{\langle\theta,\phi_d\rangle_0}{N}
 =\frac{3A_1b}{A_1^2+b^2}
 =\frac{3ab}{2(a^2/4+b^2)},
 \tag{3.5}
\]

\[
 \zeta:=Q_\perp\phi_d=\omega\theta.
 \tag{3.6}
\]

With \(r=b/A_1=2e^{-3d}\),

\[
 \omega=\frac{3r}{1+r^2},
 \qquad
 0<\omega\le\frac32.
 \tag{3.7}
\]

The maximum occurs at \(r=1\), or \(d=(\log2)/3\).  Hence the moving
orthogonal line itself has no singular rotation:

\[
 \boxed{
 (P_\perp)_d
 =\frac{\zeta\otimes\phi+\phi\otimes\zeta}{N},
 \qquad
 \|(P_\perp)_d\|=|\omega|\le\frac32.}
 \tag{3.8}
\]

### 3.1 Exact adjoint pressure vector

Define

\[
 G:=\mathscr B_0^*\phi
 =\Pi_0(W\phi)+\mathcal L_0^{-1}\Pi_0(\phi^2).
 \tag{3.9}
\]

The four Fourier coefficients can be audited term by term:

| term | \(\cos x\) | \(\cos2x\) | \(\cos3x\) | \(\cos4x\) |
|---|---:|---:|---:|---:|
| \(\Pi_0(W\phi)\) | \(5ab/16\) | \(a^2/8\) | \(-5ab/16\) | \(b^2/8\) |
| \(\mathcal L_0^{-1}\Pi_0(\phi^2)\) | \(-ab/2\) | \(-a^2/32\) | \(ab/18\) | \(-b^2/32\) |

Thus

\[
 \boxed{
 G=-\frac{3ab}{16}\cos x
 +\frac{3a^2}{32}\cos2x
 -\frac{37ab}{144}\cos3x
 +\frac{3b^2}{32}\cos4x.}
 \tag{3.10}
\]

In particular, \(G\ne0\) for every finite \(d\), and it is orthogonal to
both \(\phi\) and \(\theta\).  From (1.14),

\[
 \mathscr A_0^*\phi
 =\phi_d+icG
 =\kappa\phi+\zeta+icG.
 \tag{3.11}
\]

### 3.2 Fully expanded blocks

Equations (2.8), (2.10), and (3.8)--(3.11) give

\[
 \boxed{
 Q_\perp\mathscr A_0P_\perp
 =\frac{\zeta\otimes\phi}{N},}
 \tag{3.12}
\]

\[
 \boxed{
 P_\perp\mathscr A_0Q_\perp
 =\phi\otimes\frac{\zeta+icG}{N},}
 \tag{3.13}
\]

\[
 \boxed{
 (P_\perp)_dQ_\perp
 =\frac{\phi\otimes\zeta}{N}.}
 \tag{3.14}
\]

The orthogonal dual defect is therefore

\[
 \boxed{
 h_\perp
 =(\psi_\perp)_d+\mathscr A_0^*\psi_\perp
 =\frac{2\zeta+icG}{N}.}
 \tag{3.15}
\]

For

\[
 a_\perp=\frac{\langle\phi,q\rangle_0}{N},
 \qquad z=Q_\perp q,
 \tag{3.16}
\]

the exact triangular system is

\[
 \boxed{
 (a_\perp)_d
 =\left\langle\frac{2\zeta+icG}{N},z\right\rangle_0,}
 \tag{3.17}
\]

\[
 \boxed{
 z_d=\mathscr A_0z
 -\phi\left\langle\frac{2\zeta+icG}{N},z\right\rangle_0.}
 \tag{3.18}
\]

The kinematic quantities \(P_\perp\), \((P_\perp)_d\), and
\(Q_\perp\mathscr A_0P_\perp\) are uniformly bounded in \(d\).  Equation
(3.13), however, contains a nonzero term proportional to \(|c|G\).  Thus the
orthogonal rank-one quotient is an exact algebraic reduction but does not
produce a small low-gap generator.

---

## 4. Is the two-mode sine space more natural?

Let

\[
 \mathcal S=\operatorname{span}\{s_1,s_2\},
 \qquad s_1=\sin x,\quad s_2=\sin2x,
 \tag{4.1}
\]

and let \(\Pi_{\mathcal S}\) be the fixed orthogonal projection.  Both
\(\phi(d)\) and \(\phi_d(d)\) lie in \(\mathcal S\), and
\(-\mathcal L_0\mathcal S\subset\mathcal S\).  Thus \(\mathcal S\) removes
the rank-one rotation term \(P_d\).

It does not remove the pressure coupling.  For

\[
 q=x_1s_1+x_2s_2,
 \tag{4.2}
\]

direct multiplication gives

\[
\begin{aligned}
 \mathscr B_0q
 &=Wq+\phi\mathcal L_0^{-1}q\\
 &=-\frac3{16}(a x_2+2b x_1)
   (\cos x-\cos3x).
\end{aligned}
\tag{4.3}
\]

Therefore

\[
 \boxed{
 (I-\Pi_{\mathcal S})\mathscr A_0\Pi_{\mathcal S}q
 =\frac{3ic}{16}(a x_2+2b x_1)
 (\cos x-\cos3x).}
 \tag{4.4}
\]

For \(c\ne0\), the kernel of (4.4) inside \(\mathcal S\) is

\[
 a x_2+2b x_1=0,
 \tag{4.5}
\]

which is exactly the tangent line

\[
 (x_1,x_2)=\left(\frac a2,-b\right).
 \tag{4.6}
\]

There is also nonzero return coupling.  Since
\(\mathcal L_0^{-1}\cos x=\cos x\),

\[
 \mathscr B_0\cos x
 =(W+\phi)\cos x
 =-\frac{3b}{8}(\sin x+\sin3x),
 \tag{4.7}
\]

and hence

\[
 \boxed{
 \Pi_{\mathcal S}\mathscr A_0(I-\Pi_{\mathcal S})\cos x
 =\frac{3icb}{8}\sin x.}
 \tag{4.8}
\]

Adding \(\cos x\) and \(\cos3x\) does not close a finite system.  For
example,

\[
\begin{aligned}
 \mathscr B_0\cos3x
 &=-\frac{2a}{9}\sin4x
   +\frac{2a}{9}\sin2x\\
 &\quad+\frac{5b}{72}\sin5x
   -\frac{5b}{72}\sin x.
\end{aligned}
\tag{4.9}
\]

Thus higher harmonics appear immediately when \(c\ne0\).

The exact decision is:

\[
 \boxed{
 \mathcal S\text{ is the natural fixed heat/tangent carrier; it is not
 invariant for }c\ne0\text{, while it is invariant for }c=0.}
 \tag{4.10}
\]

---

## 5. The \((\beta,\mu)\to(0,0)\) constant-mode obstruction

Assume \(|\beta|\le1/2\) and put

\[
 \mathcal L_{\beta,\mu}=D_\beta^2+\mu,
 \qquad D_\beta=-i\partial_x+\beta,
 \qquad g=\beta^2+\mu>0.
 \tag{5.1}
\]

The \(n=0\) Fourier eigenvalue of \(\mathcal L_{\beta,\mu}\) is \(g\).
On the full periodic space,

\[
 \mathscr B_{\beta,\mu}
 =M_W+M_\phi\mathcal L_{\beta,\mu}^{-1},
 \qquad
 \mathscr B_{\beta,\mu}^*
 =M_W+\mathcal L_{\beta,\mu}^{-1}M_\phi.
 \tag{5.2}
\]

Let \(\psi_{\beta,\mu}\) be any dual normalized by

\[
 \langle\psi_{\beta,\mu},\phi\rangle_0=1.
 \tag{5.3}
\]

Recall that \(\widehat f(0)=\langle 1,f\rangle_0\) and that our inner
product is conjugate-linear in its first slot.  Because \(\phi\) is real,

\[
 \widehat{\phi\psi_{\beta,\mu}}(0)
 =\langle 1,\phi\psi_{\beta,\mu}\rangle_0
 =\langle\phi,\psi_{\beta,\mu}\rangle_0
 =\overline{\langle\psi_{\beta,\mu},\phi\rangle_0}=1.
 \tag{5.4}
\]

Consequently,

\[
 \boxed{
 \widehat{\mathcal L_{\beta,\mu}^{-1}
 (\phi\psi_{\beta,\mu})}(0)=\frac1g.}
 \tag{5.5}
\]

This singular coefficient is forced by normalization; it is not a poor
choice of orthogonal dual.  The constant coefficient of (5.2) gives the
exact identity

\[
 \frac1g
 =\left|
 \widehat{\mathscr B_{\beta,\mu}^*\psi_{\beta,\mu}}(0)
 -\widehat{W\psi_{\beta,\mu}}(0)
 \right|.
\]

Since \(\|1\|_0=1\), Cauchy--Schwarz and the multiplication bound now give

\[
 \frac1g
 \le
 \|\mathscr B_{\beta,\mu}^*\psi_{\beta,\mu}\|_0
 +\|W\|_\infty\|\psi_{\beta,\mu}\|_0.
 \tag{5.6}
\]

Therefore, at fixed \(d\), no normalized dual family can keep both its
projection norm and the raw adjoint pressure vector
\(\mathscr B_{\beta,\mu}^*\psi\) uniformly bounded as \(g\downarrow0\).
The pressure singularity also survives projection when the projection norm
is bounded.  Indeed, (5.12) below implies

\[
 \|\mathscr B_{\beta,\mu}\phi\|_0
 \le C_d(|\beta|+g),
 \tag{5.6a}
\]

For clarity, \(P^*=\psi\otimes\phi\) and
\(Q^*=I-\psi\otimes\phi\), so

\[
 Q^*\mathscr B^*\psi
 =\mathscr B^*\psi
  -\psi\langle\phi,\mathscr B^*\psi\rangle_0.
\]

Moreover, by the definition of the adjoint,
\(\langle\phi,\mathscr B^*\psi\rangle_0
=\langle\mathscr B\phi,\psi\rangle_0\).  Hence, if
\(\|\psi_{\beta,\mu}\|_0\le M\), the reverse triangle inequality,
(5.6), and (5.6a) yield

\[
\begin{aligned}
 \|Q^*\mathscr B_{\beta,\mu}^*\psi_{\beta,\mu}\|_0
 &\ge \frac1g-\|W\|_\infty M
 -C_d(|\beta|+g)M^2.
\end{aligned}
\tag{5.6b}
\]

Thus a uniformly bounded projection leaves a genuine \(g^{-1}\) divergence
in the unscaled pressure off-block.  In the full OS generator this block is
multiplied by \(|c|\), so the estimate forces a divergent OS contribution
only along paths with \(|c|/g\to\infty\), modulo the displayed lower-order
terms.

More precisely, on any compact \(d\)-interval where
\(\|\phi(d)\|_0\) is bounded below,

\[
 \|P_{\beta,\mu}\|
 =\|\phi\|_0\|\psi_{\beta,\mu}\|_0,
 \tag{5.7}
\]

so (5.6) gives a dichotomy between a singular projection and a singular
adjoint coupling.

For the orthogonal dual \(\psi_\perp=\phi/N\), the constant coefficient is
fully explicit:

\[
 \widehat{W\psi_\perp}(0)
 =-\frac{a^2+b^2}{a^2+4b^2},
 \tag{5.8}
\]

and hence

\[
 \boxed{
 \widehat{\mathscr B_{\beta,\mu}^*\psi_\perp}(0)
 =\frac1g-\frac{a^2+b^2}{a^2+4b^2}.}
 \tag{5.9}
\]

Because \(\phi\) has zero mean, the orthogonal \(Q_\perp^*\) does not remove
this constant component.  The pressure part of
\(P_\perp\mathscr A_{\beta,\mu}Q_\perp\) therefore has the scale
\(|c|/g\), not a uniform \(O(|c|)\) scale.

At exactly \(g=0\), the space was changed to \(H_0\), and \(\Pi_0\) in
(1.11) deletes this constant mode before \(\mathcal L_0^{-1}\) is applied.
This is why the finite vector \(G\) in (3.10) and the singular limit (5.9)
are consistent: they belong to different operator domains.

### 5.1 The tangent line itself is not exact for positive gap

The same \(\phi=W_{xx}\) ceases to solve the OS equation once
\((\beta,\mu)\ne(0,0)\).  Since

\[
 \mathcal L_{\beta,\mu}
 =\mathcal L_0-2i\beta\partial_x+g,
 \tag{5.10}
\]

and

\[
 \mathcal L_{\beta,\mu}W
 =-\phi-2i\beta W_x+gW,
 \tag{5.11}
\]

one obtains

\[
 \mathcal L_{\beta,\mu}^{-1}\phi
 =-W-2i\beta\mathcal L_{\beta,\mu}^{-1}W_x
 +g\mathcal L_{\beta,\mu}^{-1}W.
 \tag{5.12}
\]

Thus the exact residual is

\[
\boxed{
\begin{aligned}
 R_{\beta,\mu}
 &:=\mathscr A_{\beta,\mu}\phi-\phi_d\\
 &=2i\beta\phi_x-g\phi\\
 &\quad-ic\phi\left(
 -2i\beta\mathcal L_{\beta,\mu}^{-1}W_x
 +g\mathcal L_{\beta,\mu}^{-1}W\right).
\end{aligned}}
\tag{5.13}
\]

The inverses in (5.13) act only on the \(\pm1,\pm2\) modes of \(W\) and
\(W_x\), so they remain bounded near \((0,0)\).  Nevertheless the residual
has size

\[
 O(|\beta|+g)+O\bigl(|c|(|\beta|+g)\bigr),
 \tag{5.14}
\]

which is not small in the collision regime merely because \(g\) is small.
Hence the exact rank-one cancellation at the gapless row cannot simply be
continued to positive gap.

---

## 6. Proved candidate theorem and explicit obstruction

### Proposition R0.73A-P (exact moving-tangent quotient)

Let \(H\) be a Hilbert space and let \(\mathscr A(d)\) have a common dense
domain \(D\).  Let a nonzero
\(\phi\in C^1(I;H)\cap C(I;D)\) be a strong solution of
\(\phi_d=\mathscr A(d)\phi\).  Let \(\psi\in C^1(I;H)\) satisfy
\(\psi(d)\in D(\mathscr A(d)^*)\),
\(d\mapsto\mathscr A(d)^*\psi(d)\) continuous, and
\(\langle\psi,\phi\rangle=1\).  Set
\(P=\phi\otimes\psi\), \(Q=I-P\).  For every strong solution
\(q\in C^1(I;H)\cap C(I;D)\) of \(q_d=\mathscr A(d)q\), the variables

\[
 a=\langle\psi,q\rangle,
 \qquad z=Qq
\]

satisfy

\[
 a_d=\langle\psi_d+\mathscr A^*\psi,z\rangle,
 \tag{6.1}
\]

\[
 z_d=\mathscr A z
 -\phi\langle\psi_d+\mathscr A^*\psi,z\rangle
 =(Q\mathscr A Q-P_dQ)z.
 \tag{6.2}
\]

Moreover,

\[
 Q\mathscr AP=P_dP,
 \tag{6.3}
\]

so the complement equation has no tangent-amplitude forcing.  The two blocks
are invariant, equivalently \(P_d=[\mathscr A,P]\), if and only if

\[
 \psi_d=-\mathscr A^*\psi.
 \tag{6.4}
\]

**Proof.** Equations (2.4)--(2.23) are the proof; no spectral assumption is
used.  \(\square\)

### Application and obstruction

For the R0.72Z gapless tangent, the orthogonal instance of Proposition
R0.73A-P is explicit and uniformly kinematic, with (3.8), (3.12)--(3.18).
It does not give a uniform low-gap theorem because:

1. \(G\ne0\), so the orthogonal complement-to-tangent block carries
   \(|c|G\);
2. the exact transported dual solves the anti-parabolic equation (2.24) and,
   for \(c\ne0\), is not a finite Fourier construction (at \(c=0\), finite
   Fourier support is preserved but generic \(L^2\) forward evolution fails);
3. for \(c\ne0\), the fixed two-mode carrier leaks according to (4.4) and
   generates an infinite harmonic cascade (at \(c=0\) it is heat-invariant);
4. every normalized positive-gap dual obeys the \(g^{-1}\) dichotomy (5.6);
5. the gapless tangent residual becomes (5.13) for positive gap.

Thus the correct R0.73A conclusion is

\[
\boxed{
\begin{array}{ll}
\text{moving rank-one quotient algebra} & \texttt{CLOSED},\\
\text{explicit orthogonal }P_d,QAP,PAQ & \texttt{CLOSED},\\
\text{fixed two-mode OS invariance for }c\ne0 & \texttt{FALSE},\\
\text{uniform dual with bounded adjoint pressure block through }g=0
 & \texttt{FALSE as an unweighted claim},\\
\text{bounded transported dual / low-gap propagator} & \texttt{OPEN},\\
\text{physical Bloch-uniform velocity direct sum} & \texttt{OPEN}.
\end{array}}
\tag{6.5}
\]

The next viable analytic target is not “remove the tangent eigenvector.”  It
is a weighted modulation theorem that simultaneously tracks the tangent
carrier, the near-constant mode, and the adjoint pressure cost, with an
explicit transient prefactor.  Any such theorem must state its \(g\)- and
\(|c|\)-weights; rank one alone cannot make them uniform.

---

## 7. Audit checklist

- [x] \(\phi_d=\mathscr A_0\phi\) checked directly.
- [x] Dual normalization and \(P^2=P\) recorded.
- [x] \(P_d\), \(Q\mathscr A_0P\), and \(P\mathscr A_0Q\) expanded.
- [x] General amplitude/complement system derived without assuming
      orthogonality.
- [x] Transported-dual equivalence \(P_d=[\mathscr A_0,P]\) proved.
- [x] Orthogonal \(P_d\) and its sharp elementary bound computed.
- [x] The four coefficients of \(G=\mathscr B_0^*\phi\) tabulated.
- [x] Two-mode leakage and return coupling exhibited explicitly.
- [x] Higher-harmonic nonclosure exhibited explicitly.
- [x] Positive-gap constant-mode \(g^{-1}\) obstruction derived from
      normalization.
- [x] Positive-gap residual of the gapless tangent computed exactly.
- [x] No claim promoted to the physical \(\mu=0\) velocity row or to the
      nonlinear problem.
