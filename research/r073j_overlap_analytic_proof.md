# R0.73J overlap analytic proof and audit contract

**Status:** source-stage proof candidate; numerical and independent audits are
still required
**Scope:** the real rectangle
\(0\le d\le D_*=1/450\),
\(167/1000\le\lambda\le173/1000\)
**Claims addressed:** the analytic basis of J10 and J11
**Dependency:** the J8 theorem that the unique local Evans zero is real,
algebraically simple, and lies in this rectangle

## 0. Evidence boundary

I use this note to justify the analytic interpolation performed by
`research/r073j_overlap_core.py` and
`experiments/r073j/certify_overlap.py`.  The code evaluates conjugates at real
Chebyshev nodes.  A conjugate is not a holomorphic operation in a complexified
parameter.  The proof below replaces every such quantity by an explicit
plus/minus holomorphic pair, proves that its real-rectangle restriction is the
quantity evaluated by the code, and derives the majorants used for the two
one-variable Bernstein ellipses.

This note does not prove the numerical lower bounds produced by the interval
program.  It also does not prove J8.  The conclusion about kinetic
eigenvectors is conditional on both inputs.  J10 and J11 remain open until
the interval run, source sealing, independent recomputation, and independent
analytic audit have passed.

## 1. Operators, conventions, and the selected right solution

Let

\[
 \mathbb T=\mathbb R/(2\pi\mathbb Z),\qquad
 L=-\partial_x^2+\frac14,
 \tag{1.1}
\]

and

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.2}
\]

The kinetic vorticity space is

\[
 X=H^{-1}_{\rm per},\qquad
 \langle q_1,q_2\rangle_X
 =4\langle L^{-1}q_1,q_2\rangle_{L^2},
 \tag{1.3}
\]

where

\[
 \langle f,g\rangle_{L^2}
 =\int_{\mathbb T}\overline f\,g\,dx.
 \tag{1.4}
\]

The kinetic and ordinary realizations are

\[
 A_X(d)=-\frac i2(M_{W_d}+M_{W_d''}L^{-1}),
 \qquad
 A_2(d)=-\frac i2(M_{W_d}+M_{W_d''}L^{-1}).
 \tag{1.5}
\]

They act on \(X\) and \(L^2\), respectively.

For now let \(d\) and \(\lambda\) be real and in the frozen rectangle.  Put

\[
 D_+(x;d,\lambda)=W_d(x)-2i\lambda,
 \qquad
 Q_+(x;d,\lambda)=\frac14+\frac{W_d''(x)}{D_+(x;d,\lambda)}.
 \tag{1.6}
\]

Let \(Y_+\) solve

\[
 Y_+'=\begin{pmatrix}0&1\\Q_+&0\end{pmatrix}Y_+,
 \qquad Y_+(0)=I,
 \tag{1.7}
\]

and set \(M_+=Y_+(2\pi)\).  The selected initial vector is

\[
 v_+(d,\lambda)=
 \binom{M_{+,12}}{1-M_{+,11}}.
 \tag{1.8}
\]

The function \(\phi_+\) is the solution of

\[
 \phi_+''=Q_+\phi_+,
 \qquad
 \binom{\phi_+(0)}{\phi_+'(0)}=v_+.
 \tag{1.9}
\]

This defines \(\phi_+\) at every point of the rectangle, not only on the
Evans zero set.  If

\[
 E(d,\lambda)=\det(M_+-I)=0
 \tag{1.10}
\]

and \(M_{+,12}\ne0\), then \(v_+\ne0\) and

\[
 (M_+-I)v_+=0.
 \tag{1.11}
\]

Indeed, the first component in (1.11) vanishes identically.  Liouville's
formula gives \(\det M_+=1\), while (1.10) gives
\(\operatorname{tr}M_+=2\); these identities make the second component
vanish.  Thus \(\phi_+\) is a nonzero periodic Rayleigh eigenfunction at an
Evans zero covered by the anchor certificate.

## 2. The kinetic adjoint potential and the exact pairing

At a real \(\lambda\), define

\[
 D_-=W_d+2i\lambda.
 \tag{2.1}
\]

The exact factorization from the J0--J2 proof is

\[
 \lambda-A_2
 =\mathcal D_+T_+L^{-1},
 \qquad
 \mathcal D_+=\lambda+\frac i2W_d=\frac i2D_+,
 \tag{2.2}
\]

where

\[
 T_+=L+\frac{W_d''}{D_+}.
 \tag{2.3}
\]

Since \(d,\lambda\) and \(W_d\) are real,

\[
 T_+^*=L+\frac{W_d''}{D_-},
 \qquad
 \mathcal D_+^*=\lambda-\frac i2W_d=-\frac i2D_-.
 \tag{2.4}
\]

At an Evans zero, conjugation of \(T_+\phi_+=0\) gives

\[
 T_+^*\overline{\phi_+}=0.
 \tag{2.5}
\]

Define the left potential

\[
 \boxed{
 p=\frac{\overline{\phi_+}}{W_d+2i\lambda}.}
 \tag{2.6}
\]

Then

\[
 \mathcal D_+^*p=-\frac i2\overline{\phi_+},
 \tag{2.7}
\]

and (2.2)--(2.5) imply

\[
 (\lambda-A_2)^*p=0.
 \tag{2.8}
\]

The corresponding kinetic left vector is

\[
 \ell=Lp,
 \tag{2.9}
\]

while the right kinetic vector is

\[
 h=L\phi_+.
 \tag{2.10}
\]

For every smooth \(q\),

\[
 \langle Lp,q\rangle_X=4\langle p,q\rangle_{L^2}.
 \tag{2.11}
\]

Equations (2.8) and (2.11) show that

\[
 A_X^*\ell=\lambda\ell.
 \tag{2.12}
\]

The right Rayleigh equation is

\[
 L\phi_+=-\frac{W_d''}{D_+}\phi_+.
 \tag{2.13}
\]

At real parameters,

\[
 \overline p=\frac{\phi_+}{D_+}.
 \tag{2.14}
\]

Therefore

\[
 \begin{aligned}
 N
 &:=\langle p,L\phi_+\rangle_{L^2}\\
 &=-\int_{\mathbb T}
 \frac{W_d''\phi_+^2}{D_+^2}\,dx.
 \end{aligned}
 \tag{2.15}
\]

Because \(p\) and \(\phi_+\) are periodic at the eigenvalue,

\[
 E_r:=\langle\phi_+,L\phi_+\rangle_{L^2}
 =\int_{\mathbb T}
 \left(|\phi_+'|^2+\frac14|\phi_+|^2\right)dx,
 \tag{2.16}
\]

and

\[
 E_p:=\langle p,Lp\rangle_{L^2}
 =\int_{\mathbb T}
 \left(|p'|^2+\frac14|p|^2\right)dx.
 \tag{2.17}
\]

The kinetic factors of four cancel:

\[
 \boxed{
 \frac{|\langle\ell,h\rangle_X|}
 {\|\ell\|_X\|h\|_X}
 =\frac{|N|}{\sqrt{E_rE_p}}.}
 \tag{2.18}
\]

Equations (2.6), (2.15), (2.16), and (2.17) are exactly the formulas
integrated by `research/r073j_overlap_core.py`.  Away from an Evans zero they
are auxiliary functions.  They become adjoint-vector norms and a kinetic
pairing only after periodicity is supplied by (1.10)--(1.11).

## 3. Plus/minus holomorphic substitutes

The Chebyshev remainder needs holomorphic functions on complex parameter
ellipses.  I now define those functions without conjugating a complexified
parameter.

For complex \(d\) and \(\lambda\), set

\[
 D_\pm=W_d\mp2i\lambda,
 \qquad
 Q_\pm=\frac14+\frac{W_d''}{D_\pm}.
 \tag{3.1}
\]

Whenever both denominators are nonzero, let \(Y_\pm\), \(M_\pm\), and
\(\phi_\pm\) be defined by

\[
 Y_\pm'=
 \begin{pmatrix}0&1\\Q_\pm&0\end{pmatrix}Y_\pm,
 \qquad Y_\pm(0)=I,
 \qquad M_\pm=Y_\pm(2\pi),
 \tag{3.2}
\]

\[
 \binom{\phi_\pm(0)}{\phi_\pm'(0)}
 =\binom{M_{\pm,12}}{1-M_{\pm,11}}.
 \tag{3.3}
\]

The profile is entire in \(d\), and parameter-dependent ODE theory makes all
these quantities holomorphic in \(d\) and \(\lambda\) on every domain where
\(D_+D_-\ne0\).

For real \(d\) and real \(\lambda\),

\[
 Q_-=\overline{Q_+},\qquad
 M_-=\overline{M_+},\qquad
 \phi_-=\overline{\phi_+}.
 \tag{3.4}
\]

Define the two analytic potential substitutes by

\[
 p_+=\frac{\phi_-}{D_-},
 \qquad
 p_-=\frac{\phi_+}{D_+}.
 \tag{3.5}
\]

Their derivatives are

\[
 p_+'=\frac{\phi_-'}{D_-}
 -\frac{W_d'\phi_-}{D_-^2},
 \qquad
 p_-'=\frac{\phi_+'}{D_+}
 -\frac{W_d'\phi_+}{D_+^2}.
 \tag{3.6}
\]

The four functions interpolated by the overlap certificate are represented
holomorphically as

\[
 \mathcal A(d,\lambda)=M_{+,12},
 \tag{3.7}
\]

\[
 \mathcal N(d,\lambda)
 =-\int_{\mathbb T}
 \frac{W_d''\phi_+^2}{D_+^2}\,dx,
 \tag{3.8}
\]

\[
 \mathcal E_r(d,\lambda)
 =\int_{\mathbb T}
 \left(\phi_+'\phi_-'+\frac14\phi_+\phi_-\right)dx,
 \tag{3.9}
\]

and

\[
 \mathcal E_p(d,\lambda)
 =\int_{\mathbb T}
 \left(p_+'p_-'+\frac14p_+p_-\right)dx.
 \tag{3.10}
\]

On the real rectangle, (3.4)--(3.6) give

\[
 (\mathcal A,\mathcal N,\mathcal E_r,\mathcal E_p)
 =(\texttt{anchor},\texttt{numerator},
   \texttt{rightEnergy},\texttt{leftEnergy}).
 \tag{3.11}
\]

In particular, \(\mathcal E_r\) and \(\mathcal E_p\) are real and positive
there whenever the selected solution is nonzero.  The interval ODE may use
ordinary conjugation at real nodes because (3.11) identifies those node
values with restrictions of the holomorphic functions (3.7)--(3.10).

## 4. Domains and denominator lower bounds

Let

\[
 \lambda_c=\frac{17}{100},\qquad
 r_\lambda=\frac3{1000},\qquad
 D_*=\frac1{450}.
 \tag{4.1}
\]

For a Bernstein-ellipse parameter \(\rho>1\), write

\[
 a_\rho=\frac{\rho+\rho^{-1}}2,
 \qquad
 b_\rho=\frac{\rho-\rho^{-1}}2.
 \tag{4.2}
\]

### 4.1 Complex \(d\), real \(\lambda\)

Map the \(d\)-ellipse by

\[
 d=\frac{D_*}{2}(1+z),
 \qquad z\in\mathcal E_{\rho_d}.
 \tag{4.3}
\]

Then

\[
 \operatorname{Re}d\ge u_*:=\frac{D_*}{2}(1-a_{\rho_d}),
 \qquad
 |\operatorname{Im}d|\le v_*:=\frac{D_*}{2}b_{\rho_d}.
 \tag{4.4}
\]

Put

\[
 A_1=e^{-u_*},\qquad A_4=e^{-4u_*}.
 \tag{4.5}
\]

For \(d=u+iv\), the elementary inequalities
\(|\sin v|\le|v|\) and \(|\sin4v|\le4|v|\) give

\[
 |\operatorname{Im}W_d(x)|
 \le\left(\frac{A_1}{2}+A_4\right)v_*
 =:B_{\rm im}.
 \tag{4.6}
\]

For every real \(\lambda\in[167/1000,173/1000]\), both signs obey

\[
 |D_\pm|
 \ge \frac{334}{1000}-B_{\rm im}
 =:\delta_d.
 \tag{4.7}
\]

The derivative bounds are

\[
 |W_d''|\le\frac{A_1}{2}+A_4=:B_{xx,d},
 \qquad
 |W_d'|\le\frac{A_1}{2}+\frac{A_4}{2}=:B_{x,d}.
 \tag{4.8}
\]

The complex-\(d\) majorant is valid whenever \(\delta_d>0\).  The configured
choice \(\rho_d=16\) is checked by outward-rounded arithmetic in the driver;
the check is part of the numerical certificate, not an assumption hidden in
this proof.

### 4.2 Real \(d\), complex \(\lambda\)

Map the \(\lambda\)-ellipse by

\[
 \lambda=\lambda_c+r_\lambda z,
 \qquad z\in\mathcal E_{\rho_\lambda}.
 \tag{4.9}
\]

Then

\[
 \operatorname{Re}\lambda
 \ge\lambda_*:=\lambda_c-r_\lambda a_{\rho_\lambda}.
 \tag{4.10}
\]

For real \(d\), \(W_d\) is real.  Hence

\[
 |D_\pm|\ge2\lambda_*=:\delta_\lambda.
 \tag{4.11}
\]

Uniformly for \(0\le d\le D_*\),

\[
 |W_d''|\le\frac32=:B_{xx,\lambda},
 \qquad
 |W_d'|\le1=:B_{x,\lambda}.
 \tag{4.12}
\]

The complex-\(\lambda\) majorant is valid whenever
\(\lambda_*>0\).  The driver verifies this condition with ball arithmetic.

## 5. Scaled fundamental and output majorants

This section applies to either ellipse.  Let \(\delta\) be the corresponding
lower bound in (4.7) or (4.11), and let \(B_{xx}\), \(B_x\) be the
corresponding bounds in (4.8) or (4.12).  Define

\[
 Q_*:=\frac14+\frac{B_{xx}}{\delta},
 \qquad s:=\sqrt{Q_*},
 \qquad F:=e^{2\pi s}.
 \tag{5.1}
\]

The denominator and derivative bounds give
\(|Q_\pm(x)|\le Q_*=s^2\) on the corresponding ellipse.

For either sign, let \(\psi''=Q_\pm\psi\), and introduce

\[
 z=\binom{s\psi}{\psi'}.
 \tag{5.2}
\]

Then

\[
 z'=\begin{pmatrix}0&s\\Q_\pm/s&0\end{pmatrix}z,
 \qquad
 \|z'\|_\infty\le s\|z\|_\infty.
 \tag{5.3}
\]

Gronwall's inequality gives

\[
 \|z(x)\|_\infty\le e^{sx}\|z(0)\|_\infty.
 \tag{5.4}
\]

Applying (5.4) to the two fundamental columns yields

\[
 |M_{\pm,11}|\le F,
 \qquad
 |M_{\pm,12}|\le\frac Fs.
 \tag{5.5}
\]

For the selected initial vector (3.3),

\[
 \max(s|\phi_\pm(0)|,|\phi_\pm'(0)|)
 \le1+F.
 \tag{5.6}
\]

Therefore, with

\[
 S:=F(1+F),
 \tag{5.7}
\]

the complete period satisfies

\[
 |\phi_\pm|\le\frac Ss,
 \qquad
 |\phi_\pm'|\le S.
 \tag{5.8}
\]

Equations (3.5)--(3.6) give

\[
 |p_\pm|\le P_0:=\frac{S}{s\delta},
 \tag{5.9}
\]

and

\[
 |p_\pm'|
 \le P_1:=\frac S\delta+\frac{SB_x}{s\delta^2}.
 \tag{5.10}
\]

With \(P=2\pi\), the four holomorphic outputs obey

\[
 |\mathcal A|\le M_{\mathcal A}:=\frac Fs,
 \tag{5.11}
\]

\[
 |\mathcal N|
 \le M_{\mathcal N}
 :=P B_{xx}\frac{(S/s)^2}{\delta^2},
 \tag{5.12}
\]

\[
 |\mathcal E_r|
 \le M_{\mathcal E_r}
 :=P\left(S^2+\frac{(S/s)^2}{4}\right),
 \tag{5.13}
\]

and

\[
 |\mathcal E_p|
 \le M_{\mathcal E_p}
 :=P\left(P_1^2+\frac{P_0^2}{4}\right).
 \tag{5.14}
\]

These are the quantities named `anchor`, `numerator`, `rightEnergy`, and
`leftEnergy` in `overlap_majorant`.  In particular, the factor
`scaledSolution = fundamental * (1 + fundamental)` is (5.7), and no
unrecorded Euclidean-norm constant is needed because (5.3) uses the scaled
maximum norm.

## 6. Tensor interpolation error

Let \(I_d\) be degree \(n_d\) interpolation at the \(n_d+1\) first-kind
Chebyshev roots in the real \(d\)-coordinate.  Define \(I_\lambda\)
similarly.  If a scalar holomorphic function is bounded by \(M\) on the
Bernstein ellipse \(\mathcal E_\rho\), the standard root-interpolation bound
is

\[
 \|f-I_nf\|_{[-1,1]}
 \le\frac{4M\rho^{-n}}{\rho-1}.
 \tag{6.1}
\]

For each of the four functions in Section 3, let

\[
 \epsilon_d=\frac{4M_d\rho_d^{-n_d}}{\rho_d-1},
 \qquad
 \epsilon_\lambda
 =\frac{4M_\lambda\rho_\lambda^{-n_\lambda}}
 {\rho_\lambda-1},
 \tag{6.2}
\]

where \(M_d\) and \(M_\lambda\) are obtained from Section 5 with the two
sets of bounds in Section 4.

The tensor interpolant used by the code is \(I_\lambda I_df\).  The exact
identity

\[
 f-I_\lambda I_df
 =(f-I_\lambda f)+I_\lambda(f-I_df)
 \tag{6.3}
\]

gives

\[
 \boxed{
 \|f-I_\lambda I_df\|_\infty
 \le\epsilon_\lambda+\Lambda_\lambda\epsilon_d,}
 \tag{6.4}
\]

where \(\Lambda_\lambda\) is the Lebesgue constant of the
\(\lambda\)-interpolant.  Thus no joint complex \((d,\lambda)\) majorant is
needed.  It is enough to control complex \(d\) with real \(\lambda\), and
complex \(\lambda\) with real \(d\), as Sections 4.1 and 4.2 do.

For first-kind roots,

\[
 \Lambda_\lambda
 \le1+\frac2\pi\log(n_\lambda+1).
 \tag{6.5}
\]

The formal configuration uses \(n_d=n_\lambda=28\), hence 29 nodes in each
variable.  The calls with `degree + 1` nodes and the degree-28 remainder in
the driver are consistent with (6.1).  There is no degree/node shift.

The Arb node enclosures propagate through the discrete Chebyshev transform
and the Chebyshev-to-Bernstein conversion.  On a real cell, tensor Bernstein
basis functions are nonnegative and sum to one.  The componentwise hull of
the ball coefficients therefore encloses the interpolating polynomial.  An
additional real and imaginary radius equal to the right side of (6.4)
encloses the exact holomorphic function on that cell.

The Taylor ODE setting is separate from the Chebyshev degree.  With Taylor
order 12, the core evaluates coefficients through order 11 and adds the
order-12 Lagrange remainder.  The accumulated integral states use
integrand coefficients through order 11, which is exactly what their
order-12 state coefficient requires.

## 7. Conditional extraction at the true root

The overlap rectangle alone does not prove that an eigenvalue exists in it.
The following implication is the exact contract needed for J10 and J11.

Assume first that J8 has established, for every \(d\in[0,D_*]\), a unique
real algebraically simple Evans zero satisfying

\[
 |\lambda_0(d)-17/100|<3/1000.
 \tag{7.1}
\]

Then

\[
 \lambda_0(d)\in(167/1000,173/1000),
 \tag{7.2}
\]

so the closed overlap rectangle covers the complete branch.

Assume next that the validated tensor-Bernstein certificate proves throughout
the closed rectangle that

\[
 |\mathcal A|>0,
 \qquad
 \mathcal E_r>0,
 \qquad
 \mathcal E_p>0,
 \tag{7.3}
\]

and

\[
 \frac{|\mathcal N|}
 {\sqrt{\mathcal E_r\mathcal E_p}}>\frac12.
 \tag{7.4}
\]

At \(\lambda=\lambda_0(d)\), equations (1.10)--(1.11) make \(\phi_+\)
periodic and nonzero.  Sections 2 and 3 then identify

\[
 h_d=L\phi_+,
 \qquad
 \ell_d=Lp
 \tag{7.5}
\]

as kinetic right and left eigenvectors.  After normalization, (2.18) and
(7.4) give

\[
 |\langle\ell_d,h_d\rangle_X|>\frac12.
 \tag{7.6}
\]

This is the conditional J10 conclusion.

For J11, define the fixed linear functional

\[
 \mathfrak a:X\longrightarrow\mathbb C,
 \qquad
 \mathfrak a(h)=(L^{-1}h)(0).
 \tag{7.7}
\]

It is bounded: \(L^{-1}:H^{-1}_{\rm per}\to H^1_{\rm per}\) is bounded,
and the one-dimensional embedding \(H^1_{\rm per}\hookrightarrow C^0\)
makes point evaluation continuous.  For (7.5),

\[
 \mathfrak a(h_d)=\phi_+(0)=M_{+,12}=\mathcal A(d,\lambda_0(d)).
 \tag{7.8}
\]

The first inequality in (7.3) therefore supplies a fixed nonzero kinetic
phase anchor along the branch.  A normalized eigenvector can be phased
uniquely by requiring \(\mathfrak a(h_d)>0\) real.

Neither (7.6) nor (7.8) is an unconditional conclusion of this note.  They
require the J8 root theorem and the completed interval certificate stated in
(7.3)--(7.4).

## 8. Audit and release contract

The formal overlap certificate must retain the following dependencies in its
source ledger and decision record.

1. This analytic note, the real-node ODE core, the Chebyshev/Bernstein core,
   the certificate driver, the exact configuration, and the pinned Arb/Acb
   dependency must all be hashed.
2. The certificate must state that its eigenvector conclusion is conditional
   on J8.  A standalone rectangle computation proves bounds for the auxiliary
   functions in Section 3; it does not prove the existence of an eigenvector.
3. The numerical record must expose \(\delta_d\), \(\delta_\lambda\), all
   four majorants, both interpolation errors, the Lebesgue bound, every final
   Bernstein cell, and the minimum strict margins in (7.3)--(7.4).
4. An independent implementation must recompute the decisive anchor and
   normalized-overlap lower bounds without reading the primary result cells.

The status after this draft is therefore:

| Item | Present status |
|---|---|
| plus/minus holomorphic replacement | proof candidate; independent audit pending |
| kinetic adjoint and pairing formulas | proof candidate; independent audit pending |
| complex-parameter majorants | proof candidate; interval evaluation pending |
| tensor error \(\epsilon_\lambda+\Lambda_\lambda\epsilon_d\) | proof candidate; independent audit pending |
| J10 kinetic overlap | conditional and open |
| J11 fixed phase anchor | conditional and open |
