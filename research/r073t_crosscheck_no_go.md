# R0.73T cross-check of the six-mode pressure no-go

**Cross-checked file:** `research/r073t_no_go_audit.md`

**Method:** independent exact sparse-Fourier reconstruction over rational
numbers, starting from the sine coefficients rather than from the displayed
autocorrelation or pressure tables

**Verdict:** `PASS_EXACT__NO_CORRECTION_REQUIRED`

All requested quantities were reproduced exactly:

\[
 \mathcal E=42,\qquad Q=2918,\qquad A=164,\qquad D_C=15,
 \tag{0.1}
\]

\[
 \mathcal N_4=-384,\qquad X^2=4296,\qquad Y=1986.
 \tag{0.2}
\]

The pressure sign, the dilation factors, the sign change under
\(u\mapsto-u\), and the constant \(4C_R^2/\nu\) in the one-sided estimate
(2.3) of the audited file are correct.  No floating-point quadrature, PDE
time integration, or DGX computation was used.

## 1. Normalization reconstructed from first principles

The audit uses Haar probability measure,

\[
 d\mu=(2\pi)^{-3}dx,
 \qquad
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu,
 \tag{1.1}
\]

so

\[
 \int e^{i(k-\ell)\cdot x}\,d\mu=\mathbf 1_{k=\ell},
 \qquad
 \widehat{\partial_jf}(k)=ik_j\widehat f(k).
 \tag{1.2}
\]

Thus no \((2\pi)^3\) factor occurs in Parseval or any convolution below.
Also,

\[
 \sin\theta={e^{i\theta}-e^{-i\theta}\over2i},
 \qquad
 \cos\theta={e^{i\theta}+e^{-i\theta}\over2}.
 \tag{1.3}
\]

For

\[
 u=(6\sin y-4\sin(x+y),\;4\sin x+4\sin(x+y),\;0),
 \tag{1.4}
\]

write \(\widehat u(k)=i b_k\), with real integer vectors \(b_k\).  Directly
from (1.3), the six nonzero entries are

| \(k\) | \(b_k\) |
| --- | --- |
| \((1,0,0)\) | \((0,-2,0)\) |
| \((-1,0,0)\) | \((0,2,0)\) |
| \((0,1,0)\) | \((-3,0,0)\) |
| \((0,-1,0)\) | \((3,0,0)\) |
| \((1,1,0)\) | \((2,-2,0)\) |
| \((-1,-1,0)\) | \((-2,2,0)\) |

They obey

\[
 b_{-k}=-b_k,\qquad k\cdot b_k=0.
 \tag{1.5}
\]

Hence \(\widehat u(-k)=\overline{\widehat u(k)}\), and the field is exactly
real and divergence free.  This coefficient list, rather than any table in
the audited file, was the input to all calculations below.

## 2. Independent autocorrelation reconstruction

Because \(\widehat u(k)=ib_k\),

\[
 C(h)=\sum_{p-q=h}\widehat u(p)\cdot
                    \overline{\widehat u(q)}
     =\sum_{p-q=h}b_p\cdot b_q.
 \tag{2.1}
\]

Exact integer convolution gives

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

All other shifts vanish.  Consequently

\[
 \mathcal E=C(0)=42,
 \tag{2.2}
\]

\[
\begin{aligned}
 Q
 &=42^2+2(12^2+8^2+4^2+9^2+8^2+12^2+8^2)\\
 &=2918,
\end{aligned}
 \tag{2.3}
\]

and

\[
 A=42+2(12+8+4+9+8+12+8)=164,
 \qquad D_C=1+2\cdot7=15.
 \tag{2.4}
\]

As an additional static check, direct cubic convolution of \(C\) gives

\[
 \|u\|_6^6=247716,
 \qquad
 A Q=478552,
 \tag{2.5}
\]

so the unit-constant R0.73S inequality \(\|u\|_6^6\le A Q\) holds with the
same normalization.  With \(M=6\), the two auxiliary estimates also read

\[
 A=164\le M\mathcal E=252,
 \qquad
 A^2=26896\le D_CQ=43770.
 \tag{2.6}
\]

## 3. Pressure reconstructed from the tensor, not from \(C\)

Define the tensor coefficient

\[
 U_{ij}(n)=\widehat{u_i u_j}(n)
 =-\sum_{k+\ell=n}b_{k,i}b_{\ell,j}.
 \tag{3.1}
\]

Taking divergence of Navier--Stokes gives

\[
 -\Delta p=\partial_i\partial_j(u_i u_j).
 \tag{3.2}
\]

Therefore, for \(n\ne0\),

\[
 \boxed{
 \widehat p(n)=-{n_i n_j\over |n|^2}U_{ij}(n).}
 \tag{3.3}
\]

Indeed, (3.2) becomes
\(|n|^2\widehat p(n)=-n_in_jU_{ij}(n)\), which fixes the minus sign and
agrees with the double-Riesz representation.  Exact tensor convolution gives

| pressure sites | \(\widehat p(n)\) |
| --- | ---: |
| \(\pm(1,0,0)\) | \(12\) |
| \(\pm(0,1,0)\) | \(-8\) |
| \(\pm(1,1,0)\) | \(6\) |
| \(\pm(1,-1,0)\) | \(6\) |
| \(\pm(2,1,0)\) | \(-8/5\) |
| \(\pm(1,2,0)\) | \(12/5\) |

Using (1.3), this is precisely

\[
\begin{aligned}
 p={}&24\cos x-16\cos y+12\cos(x+y)+12\cos(x-y)\\
 &-{16\over5}\cos(2x+y)+{24\over5}\cos(x+2y),
\end{aligned}
 \tag{3.4}
\]

with zero mean.  This independently confirms both the sign and every
coefficient of the displayed pressure in the audited file.

## 4. Exact pressure work and \(\mathcal N_4\)

Let

\[
 I=\int |u|^2u\cdot\nabla p\,d\mu.
 \tag{4.1}
\]

Since \(\widehat u(k)=ib_k\) and
\(\widehat{\nabla p}(n)=in\widehat p(n)\), an independent scalar convolution
is

\[
 I=\sum_{h+k+n=0}
 C(h)\bigl[-b_k\cdot n\bigr]\widehat p(n).
 \tag{4.2}
\]

Grouping this exact rational sum by the squared length of the
autocorrelation shift gives

| \(|h|^2\) | contribution to \(I\) |
| ---: | ---: |
| \(0\) | \(0\) |
| \(1\) | \(0\) |
| \(4\) | \(-144\) |
| \(5\) | \(240\) |
| \(8\) | \(0\) |

Thus

\[
 I=-144+240=96,
 \qquad
 \boxed{\mathcal N_4=-4I=-384.}
 \tag{4.3}
\]

No value from the original pressure-work calculation was used in obtaining
(4.2)--(4.3).

## 5. Independent reconstruction of \(X^2\) and \(Y\)

Parseval applied to \(w=|u|^2\) gives

\[
\begin{aligned}
 X^2
 &=\|\nabla w\|_2^2
 =\sum_h|h|^2|C(h)|^2\\
 &=2\bigl(12^2+8^2+4\cdot4^2+4\cdot9^2
          +5\cdot8^2+5\cdot12^2+8\cdot8^2\bigr)\\
 &=4296.
\end{aligned}
 \tag{5.1}
\]

For the other viscous term, define independently

\[
 G(h)=\widehat{|\nabla u|^2}(h)
 =\sum_{p-q=h}(p\cdot q)(b_p\cdot b_q).
 \tag{5.2}
\]

The nonzero values align with the support of \(C\):

| shifts \(h\) | \(G(h)\) |
| --- | ---: |
| \(0\) | \(58\) |
| \(\pm(1,0,0)\) | \(-12\) |
| \(\pm(0,1,0)\) | \(8\) |
| \(\pm(2,0,0)\) | \(4\) |
| \(\pm(0,2,0)\) | \(9\) |
| \(\pm(2,1,0)\) | \(8\) |
| \(\pm(1,2,0)\) | \(-12\) |
| \(\pm(2,2,0)\) | \(16\) |

Therefore

\[
\begin{aligned}
 Y
 &=\int |u|^2|\nabla u|^2\,d\mu
 =\sum_h C(h)G(-h)\\
 &=42\cdot58
 +2\bigl(144+64-16-81-64-144-128\bigr)\\
 &=1986.
\end{aligned}
 \tag{5.3}
\]

The full viscous coefficient is consequently

\[
 4Y+2X^2=4\cdot1986+2\cdot4296=16536.
 \tag{5.4}
\]

## 6. Dilation and sign checks

For integer \(L\ge1\), the field \(u_L(x)=u(Lx)\) has coefficients

\[
 \widehat{u_L}(Lk)=\widehat u(k),
 \tag{6.1}
\]

and no others.  Haar invariance under the torus covering map gives

\[
 C_{u_L}(Lh)=C_u(h).
 \tag{6.2}
\]

Hence \((\mathcal E,Q,A,D_C)\) is unchanged.  Formula (3.3) is homogeneous
of degree zero in the frequency, so

\[
 \widehat{p_L}(Ln)=\widehat p(n),
 \qquad p_L(x)=p(Lx).
 \tag{6.3}
\]

One derivative then gives

\[
 I(u_L)=96L,\qquad
 \mathcal N_4(u_L)=-384L,\qquad
 X_L^2=4296L^2,\qquad Y_L=1986L^2.
 \tag{6.4}
\]

Substitution into the exact \(L^4\) balance yields

\[
 \left.{dQ(u_L)\over dt}\right|_{t=0}
 =-16536\nu L^2-384L.
 \tag{6.5}
\]

Under \(u\mapsto-u\), the tensors \(u_i u_j\), \(w\), \(C\), \(G\), and
the pressure are unchanged, while the single velocity factor in \(I\)
changes sign.  Thus

\[
 \mathcal N_4(-u_L)=384L,
 \tag{6.6}
\]

\[
 \left.{dQ(-u_L)\over dt}\right|_{t=0}
 =-16536\nu L^2+384L,
 \tag{6.7}
\]

and the signed derivative difference is exactly

\[
 -768L.
 \tag{6.8}
\]

All six original velocity frequencies have magnitude \(1\) or \(\sqrt2\);
after dilation they lie in \(L\le|k|\le\sqrt2L\), confirming the fixed-ratio
annulus statement.

## 7. Constant audit for equation (2.3)

Let \(C_R\) include the finite component sum and satisfy

\[
 \|p\|_3\le C_R\|u\|_6^2.
 \tag{7.1}
\]

With \(X=\|\nabla|u|^2\|_2\), Hölder with exponents \((3,6,2)\) gives

\[
 |\mathcal N_4|
 \le4\|p\|_3\|u\|_6X
 \le4C_R\|u\|_6^3X.
 \tag{7.2}
\]

The precise Young constant follows by completing a square:

\[
 0\le
 \left(\sqrt\nu X-{2C_R\over\sqrt\nu}\|u\|_6^3\right)^2.
 \tag{7.3}
\]

Equivalently,

\[
 4C_R\|u\|_6^3X
 \le\nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
 \tag{7.4}
\]

Combining (7.4) with

\[
 Q'=-4\nu Y-2\nu X^2+\mathcal N_4
 \tag{7.5}
\]

leaves exactly

\[
 \boxed{
 Q'+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}\|u\|_6^6
 \le {4C_R^2\over\nu}A Q.}
 \tag{7.6}
\]

Thus the coefficient \(4C_R^2/\nu\), the surviving coefficient \(\nu\) of
\(X^2\), and the coefficient \(4\nu\) of \(Y\) in the audited equation
(2.3) are all correct.  The value \(4C_R^2/\nu\) is the exact output of
this chosen scalar Young split; no claim that the Riesz norm \(C_R\) itself
is sharp is required.

## 8. Additional normalization checks

Grouping the exact \(C\) table by \(|h|^2\) reproduces

\[
\begin{aligned}
 Q_\tau={}&1764+416e^{-2\tau}+194e^{-8\tau}
 +416e^{-10\tau}+128e^{-16\tau},\\
 A_\tau={}&42+40e^{-\tau}+26e^{-4\tau}
 +40e^{-5\tau}+16e^{-8\tau}.
\end{aligned}
 \tag{8.1}
\]

An independent convolution of the odd part of \(\partial_t|u|^2\) shows
that every weighted sign-pair contribution cancels except the
\(|h|^2=4\) group.  It gives

\[
 Q_\tau'(u)-Q_\tau'(-u)=-768e^{-8\tau},
 \tag{8.2}
\]

and dilation gives \(-768Le^{-8\tau L^2}\), as in the audited file.

For the auxiliary shear \(s_L=(0,\sin Lx_1,0)\), direct Fourier expansion
gives

\[
 C(0)={1\over2},\qquad C(\pm2Le_1)=-{1\over4},
 \tag{8.3}
\]

so

\[
 \mathcal E={1\over2},\quad Q={3\over8},\quad A=1,\quad D_C=3.
 \tag{8.4}
\]

Since \(s_L(t)=e^{-\nu L^2t}s_L(0)\),

\[
 Q(t)={3\over8}e^{-4\nu L^2t},
 \qquad Q'(0)=-{3\over2}\nu L^2.
 \tag{8.5}
\]

This confirms the remaining normalization used by the two-sided derivative
obstruction.

## 9. Final authorization matrix

```text
velocityRealityAndDivergence=PASS_EXACT
autocorrelationTable=PASS_EXACT
energyE=42=PASS_EXACT
quarticQ=2918=PASS_EXACT
wienerA=164=PASS_EXACT
autocorrelationSupportDC=15=PASS_EXACT
pressureFourierSign=PASS_EXACT
pressureFormula=PASS_EXACT
pressureWorkIntegral=96=PASS_EXACT
N4=-384=PASS_EXACT
XSquared=4296=PASS_EXACT
Y=1986=PASS_EXACT
dilationScaling=PASS_EXACT
signPair=PASS_EXACT
equation2.3Constant=PASS_EXACT
haarAndFourierNormalization=PASS_EXACT
weightedFormula=PASS_EXACT
shearNormalization=PASS_EXACT
correctionRequired=NO
```

The cross-check validates a finite identifiability and scaling obstruction,
not a singularity mechanism or a global Navier--Stokes theorem.
