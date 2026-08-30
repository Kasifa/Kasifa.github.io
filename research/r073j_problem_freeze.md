# R0.73J problem freeze: a unique simple rightmost continuum branch

**Frozen:** 2026-08-30  
**Parent release:** R0.73I  
**Scope:** the exact periodic planar row
\((\beta,\xi,\gamma)=(0,0,1/2)\) and the slow interval
\(0\le d\le D_*=1/450\)  
**Evidence target:** a continuous-operator theorem, not a Fourier-cutoff
extrapolation  
**Public status:** source stage; R0.73J is not released

## 0. Direct decision

R0.73I left its branch contract open.  Finite matrices show a stable-looking
one-dimensional leading branch, but they do not prove that the continuum
root is unique, simple, or rightmost.  R0.73J will close that exact gap by a
validated periodic Rayleigh--Evans calculation.

The target is deliberately narrower than “only one unstable eigenvalue.”
Finite diagnostics consistently show a second unstable conjugate pair near
real part \(0.04\).  The statement to prove is instead:

> throughout \([0,1/450]\), exactly one discrete eigenvalue lies to the
> right of \(\operatorname{Re}\lambda=11/100\); it is real, algebraically
> simple, remains in a fixed local disk about \(17/100\), and is separated
> from every other spectral point by a uniform real-part gap.

The phrase *continuous branch* means continuous in the slow parameter
\(d\).  It is a branch of discrete eigenvalues.  It is not continuous or
essential spectrum.

## 1. Frozen operator and Rayleigh pencil

Let

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad
 L=-\partial_x^2+\frac14.
 \tag{1.1}
\]

The kinetic vorticity space is

\[
 X=\overline{L^2(\mathbb T)}^{\,\|q\|_X},
 \qquad
 \|q\|_X^2=4\langle L^{-1}q,q\rangle,
 \tag{1.2}
\]

and the inviscid generator is

\[
 A_X(d)=-\frac i2\left(M_{W_d}+M_{W_d''}L^{-1}\right).
 \tag{1.3}
\]

The unitary map \(U=2L^{-1/2}:X\to L^2\) conjugates \(A_X\) to a
compact perturbation of \(-iM_{W_d}/2\).  Indeed,
\(L^{-1/2}M_{W_d}L^{1/2}-M_{W_d}\) has negative pseudodifferential
order, and \(L^{-1/2}M_{W_d''}L^{-1/2}\) is compact.  Hence

\[
 \sigma_{\rm ess}(A_X(d))=-\frac i2\operatorname{Ran}W_d
 \subset i\mathbb R.
 \tag{1.4}
\]

Every spectral point in the open right half-plane is therefore an isolated
eigenvalue of finite algebraic multiplicity.

Writing \(q=L\phi\) and \(c=2i\lambda\), the eigenvalue equation is
equivalent in \(\operatorname{Re}\lambda>0\) to

\[
 (W_d-c)\left(\phi''-\frac14\phi\right)-W_d''\phi=0,
 \qquad
 (\phi,\phi')(2\pi)=(\phi,\phi')(0).
 \tag{1.5}
\]

Define

\[
 Q(x;d,\lambda)=\frac14+
 \frac{W_d''(x)}{W_d(x)-2i\lambda},
 \qquad
 Y'=\begin{pmatrix}0&1\\Q&0\end{pmatrix}Y,
 \quad Y(0)=I,
 \tag{1.6}
\]

\[
 M(d,\lambda)=Y(2\pi;d,\lambda),
 \qquad
 E(d,\lambda)=\det(M-I)=2-\operatorname{tr}M.
 \tag{1.7}
\]

The last identity uses \(\det M=1\).  Since

\[
 |W_d(x)-2i\lambda|\ge2\operatorname{Re}\lambda,
 \tag{1.8}
\]

the coefficient and Evans function are analytic in \(\lambda\) throughout
the open right half-plane and real-analytic in real \(d\).

For validated interpolation, this analyticity is extended to the specified
complex Bernstein ellipse in \(d\).  The certificate must record a strict
lower bound for \(|W_d-2i\lambda|\) on that full complex domain; real
analyticity on the physical interval alone is not an interpolation remainder.

## 2. Exact analytic enclosure

The periodic Howard identity is obtained by putting
\(\phi=(W_d-c)F\):

\[
 \int_{\mathbb T}(W_d-c)^2
 \left(|F'|^2+\frac14|F|^2\right)=0.
 \tag{2.1}
\]

It gives

\[
 |c|\le\|W_d\|_\infty.
 \tag{2.2}
\]

For \(a=e^{-d}\), \(b=e^{-4d}\), and \(t=\cos x\),

\[
 W_d=\frac12\sin x(-a+bt).
 \tag{2.3}
\]

When \(t\ge0\), \(|W_d|\le1/2\).  When \(t=-s\le0\),

\[
 |W_d|\le\frac12\sqrt{1-s^2}(1+s)
 \le\frac{3\sqrt3}{8}.
 \tag{2.4}
\]

Therefore every right-half-plane eigenvalue satisfies

\[
 \boxed{|\lambda|\le\frac{3\sqrt3}{16}<\frac{13}{40}.}
 \tag{2.5}
\]

This outer bound is independent of the numerical certificate.

## 3. Frozen contours and target constants

Set

\[
 D_*=\frac1{450},
 \qquad b_*=\frac{11}{100},
 \tag{3.1}
\]

\[
\Omega=
 \left\{\frac{11}{100}<\operatorname{Re}\lambda<\frac{19}{50},
 \quad |\operatorname{Im}\lambda|<\frac{19}{50}\right\},
 \tag{3.2}
\]

and

\[
 \Gamma_{\rm loc}:
 \left|\lambda-\frac{17}{100}\right|=\frac3{1000}.
 \tag{3.3}
\]

The formal interval certificate must prove:

1. \(E(0,\lambda)\ne0\) on the positively oriented
   \(\partial\Omega\), and its winding number is one;
2. \(E(d,\lambda)\ne0\) on the complete \(\partial\Omega\) for every
   \(d\in[0,D_*]\);
3. \(E(d,\lambda)\ne0\) on \(\Gamma_{\rm loc}\) for every
   \(d\in[0,D_*]\);
4. the local right and left kinetic eigenvectors have normalized overlap
   at least
   \[
   m_*=\frac12.
   \tag{3.4}
   \]

The Howard disk lies strictly inside the three outer sides of
\(\partial\Omega\).  R0.73C already supplies at least one root inside
\(\Gamma_{\rm loc}\) at \(d=0\).  Its convention was
\(F=\operatorname{tr}M-2=-E\), which reverses signs but does not change
zeros or winding numbers.

If the three contour statements pass, homotopy and the argument principle
give exactly one zero, counted with multiplicity, in both the global region
and the local disk for every \(d\).  The symmetry

\[
 E(d,\bar\lambda)=\overline{E(d,\lambda)}
 \tag{3.5}
\]

then forces that single zero to be real.  More explicitly, oddness gives
\(W_d(2\pi-x)=-W_d(x)\); with \(S=\operatorname{diag}(1,-1)\),

\[
 M(d,\bar\lambda)
 =S\,\overline{M(d,\lambda)^{-1}}\,S.
 \tag{3.6}
\]

Together with \(\det M=1\), this proves (3.5).  A nonreal zero in either
conjugation-symmetric region would therefore contribute with its distinct
conjugate and make the count at least two.  The count one also makes the
zero simple.  Joint analyticity and the analytic implicit-function theorem
give a local real-analytic function of \(d\); uniqueness glues the local
functions into one real-analytic branch on the whole interval.  It obeys

\[
 \frac{167}{1000}<\lambda_0(d)<\frac{173}{1000},
 \qquad
 \sup\operatorname{Re}\bigl(\sigma(A_X(d))\setminus
 \{\lambda_0(d)\}\bigr)\le\frac{11}{100}.
 \tag{3.7}
\]

Thus a conservative final real-part gap is

\[
 \boxed{g_*=\frac1{20}.}
 \tag{3.8}
\]

## 4. Multiplicity bridge that must accompany the certificate

Counting Evans zeros is not enough until their order is tied to the kinetic
operator.  The analytic proof must establish

\[
 \operatorname{ord}_{\lambda_0}E(d,\lambda)
 =\operatorname{algmult}_{A_X(d)}(\lambda_0).
 \tag{4.1}
\]

The intended proof has three explicit analytic equivalences:

1. right-half-plane Jordan chains in \(X\simeq H^{-1}\) bootstrap to smooth
   functions and coincide with the ordinary \(L^2\) chains;
2. for the ordinary realization
   \[
     A_2=-\frac i2(M_{W_d}+M_{W_d''}L^{-1}),\qquad
     D_\lambda=M_{\lambda+iW_d/2},
   \]
   the exact factorization is
   \[
     (\lambda-A_2)L=D_\lambda T(\lambda),\qquad
     T(\lambda)=-\partial_x^2+\frac14+
       \frac{W_d''}{W_d-2i\lambda};
   \]
   \(L:H^2_{\rm per}\to L^2\) and \(D_\lambda\) are invertible in the
   right half-plane;
3. the augmented periodic boundary-value pencil is analytically equivalent
   to \(M(d,\lambda)-I\) by the initial-value solution operator and a block
   elimination.

The zero order of the finite matrix determinant is then the sum of its
partial multiplicities.  An independent line-by-line audit is required
before (4.1) is marked closed.

For the overlap statement, the final note must define normalized vectors in
one Hilbert realization.  The intended convention is

\[
 \|h_d\|_X=\|\ell_d\|_X=1,\qquad
 A_Xh_d=\lambda_0h_d,\qquad
 A_X^*\ell_d=\lambda_0\ell_d,
 \qquad |\langle\ell_d,h_d\rangle_X|\ge\frac12.
 \tag{4.2}
\]

## 5. Evidence boundary

The present finite diagnostics are useful only for choosing contours and
precision:

\[
 \lambda_{0,N}(0)\approx0.17040798,
 \qquad
 \lambda_{0,N}(1/450)\approx0.16966723,
 \tag{5.1}
\]

with a finite real-part gap near \(0.1296\) and a finite kinetic overlap
near \(0.594\).  None of these decimals is a continuum theorem.

R0.73J does not prove a viscous branch, an adiabatic gain law, nonlinear
instability, a three-dimensional singularity, or the Clay problem.  It is
the missing continuum rank-one spectral input for those later questions.
