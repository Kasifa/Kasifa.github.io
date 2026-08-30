# R0.73J analytic proof: the kinetic Rayleigh--Evans bridge

**Status:** source stage; proof candidate awaiting an independent audit
**Scope:** \((\beta,\xi,\gamma)=(0,0,1/2)\),
\(0\le d\le1/450\), and \(\operatorname{Re}\lambda>0\)
**Claims covered:** J0--J3 only
**Claims not covered:** J5--J11, including the interval winding,
parameter-uniform boundary nonvanishing, overlap, and phase anchor

## 0. What this note proves

I record the analytic part of the R0.73J certificate here.  For each fixed
real \(d\in[0,1/450]\), the note proves the following statements.

1. The essential spectrum of the kinetic vorticity operator lies on the
   imaginary axis.  Every spectral point in the open right half-plane is an
   isolated eigenvalue of finite algebraic multiplicity.
2. The generalized eigenspaces in the kinetic space and in the ordinary
   \(L^2\) realization coincide in the open right half-plane.
3. The order of a periodic monodromy Evans zero equals the algebraic
   multiplicity of the corresponding kinetic eigenvalue.
4. Every right-half-plane eigenvalue obeys
   \(|\lambda|\le3\sqrt3/16<13/40\).
5. Reflection followed by complex conjugation gives the exact symmetry
   \(E(d,\bar\lambda)=\overline{E(d,\lambda)}\).

These statements do not count any zero.  In particular, this note does not
prove that the proposed global or local contour is nonzero for the complete
\(d\)-interval.  It does not release R0.73J.

## 1. Spaces and the two operator realizations

Let \(\mathbb T=\mathbb R/(2\pi\mathbb Z)\), and use complex periodic
Sobolev spaces.  Put

\[
 \mu=\frac14,\qquad \gamma=\frac12,\qquad
 L=-\partial_x^2+\mu,
 \tag{1.1}
\]

and

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.2}
\]

The operator \(L:H^{s+2}_{\rm per}\to H^s_{\rm per}\) is an isomorphism
for every real \(s\).  Define the kinetic vorticity space by completing
\(L^2(\mathbb T)\) in the norm

\[
 \|q\|_X^2=4\langle L^{-1}q,q\rangle_{L^2}.
 \tag{1.3}
\]

Thus \(X\) is \(H^{-1}_{\rm per}\) with an equivalent, fixed Hilbert norm.
The map

\[
 U=2L^{-1/2}:X\longrightarrow L^2(\mathbb T)
 \tag{1.4}
\]

is unitary.  Multiplication by a smooth periodic function is bounded on
\(X\).  Hence

\[
 A_X(d)=-\frac i2
 \left(M_{W_d}+M_{W_d''}L^{-1}\right)\in\mathcal B(X)
 \tag{1.5}
\]

is well defined.  I also use the ordinary \(L^2\) realization

\[
 A_2(d)=-\frac i2
 \left(M_{W_d}+M_{W_d''}L^{-1}\right)\in\mathcal B(L^2).
 \tag{1.6}
\]

The formulas agree on \(L^2\subset X\), but the two bounded operators are
not being declared similar.  Their right-half-plane generalized eigenspaces
will instead be identified by regularity in Section 3.

## 2. Essential spectrum and discreteness off the imaginary axis

Conjugating (1.5) by (1.4) gives

\[
 UA_X(d)U^{-1}=-\frac i2M_{W_d}+K_d,
 \tag{2.1}
\]

where

\[
 K_d=-\frac i2\left(
 L^{-1/2}[M_{W_d},L^{1/2}]
 +L^{-1/2}M_{W_d''}L^{-1/2}
 \right).
 \tag{2.2}
\]

For the finite Fourier profile (1.2), the commutator
\([M_{W_d},L^{1/2}]\) is bounded on \(L^2\).  This follows directly from its
Fourier matrix

\[
 (W_d)_{n-m}
 \left(\sqrt{m^2+\mu}-\sqrt{n^2+\mu}\right)
 \tag{2.3}
\]

and

\[
 \left|\sqrt{m^2+\mu}-\sqrt{n^2+\mu}\right|
 \le |m-n|.
 \tag{2.4}
\]

The diagonal multiplier \(L^{-1/2}\) is compact on periodic \(L^2\).
Both terms in (2.2) are therefore compact.  For the Fredholm essential
spectrum, compact-perturbation invariance and the spectrum of a multiplication
operator yield

\[
 \boxed{
 \sigma_{\rm ess}(A_X(d))
 =-\frac i2\operatorname{essran}W_d
 =-\frac i2\operatorname{Ran}W_d
 \subset i\mathbb R.}
 \tag{2.5}
\]

The same conclusion holds for \(A_2(d)\), since
\(M_{W_d''}L^{-1}\) is compact on \(L^2\).

For \(\lambda\notin-i\operatorname{Ran}(W_d)/2\), both
\(\lambda-A_X(d)\) and \(\lambda-A_2(d)\) are Fredholm of index zero.
The complement of this compact imaginary segment is connected and contains
points with \(|\lambda|\) larger than both operator norms.  The analytic
Fredholm theorem therefore applies on the whole complement.  Consequently
every spectral point with
\(\operatorname{Re}\lambda>0\) is isolated and has finite algebraic
multiplicity.  There is no non-discrete right-half-plane spectrum left
unaccounted for by an Evans count.

## 3. Kinetic and ordinary \(L^2\) Jordan chains

Fix \(d\) and \(\lambda_0\) with \(\operatorname{Re}\lambda_0>0\).  Define

\[
 D_{\lambda}=M_{\lambda+iW_d/2}.
 \tag{3.1}
\]

For real \(W_d\),

\[
 |\lambda+iW_d(x)/2|\ge\operatorname{Re}\lambda.
 \tag{3.2}
\]

Thus \(D_\lambda\) is invertible on every \(H^s_{\rm per}\) in the open
right half-plane.  Its inverse is multiplication by a smooth function and is
holomorphic in \(\lambda\).

I first prove a regularity lemma.  If

\[
 q\in\ker(\lambda_0-A_X(d))^m
 \tag{3.3}
\]

for some \(m\ge1\), then \(q\in C^\infty(\mathbb T)\).

For \(m=1\), put \(\phi=L^{-1}q\).  Initially
\(q\in X=H^{-1}\) and \(\phi\in H^1\).  The eigenvalue equation is

\[
 D_{\lambda_0}q+\frac i2W_d''\phi=0,
 \tag{3.4}
\]

so (3.2) gives \(q\in H^1\).  Then \(\phi\in H^3\), and another use of
(3.4) gives \(q\in H^3\).  Repetition proves smoothness.

For the induction step, let

\[
 r=(\lambda_0-A_X(d))q.
 \tag{3.5}
\]

Then \(r\in\ker(\lambda_0-A_X(d))^{m-1}\), so the induction hypothesis
gives \(r\in C^\infty\).  The equation

\[
 D_{\lambda_0}q+\frac i2W_d''L^{-1}q=r
 \tag{3.6}
\]

starts with \(L^{-1}q\in H^1\).  The same two-derivative bootstrap proves
that \(q\) is smooth.

Every generalized root vector of \(A_X(d)\) in the open right half-plane
therefore belongs to \(L^2\), where (1.5) and (1.6) agree.  Conversely, an
\(L^2\) generalized root vector of \(A_2(d)\) belongs to \(X\) and satisfies
the same chain equations for \(A_X(d)\).  Hence, for every \(m\ge1\),

\[
 \ker(\lambda_0-A_X(d))^m
 =\ker(\lambda_0-A_2(d))^m.
 \tag{3.7}
\]

Since the eigenvalues are isolated and of finite algebraic multiplicity,
the increasing kernels stabilize.  Therefore

\[
 \operatorname{algmult}_{A_X(d)}(\lambda_0)
 =\operatorname{algmult}_{A_2(d)}(\lambda_0).
 \tag{3.8}
\]

This argument identifies the whole generalized eigenspace.  Equality of
ordinary eigenfunctions alone would not be sufficient for (3.8).

## 4. Exact Rayleigh-pencil factorization

On \(H^2_{\rm per}\), define

\[
 T(d,\lambda)
 =L+\frac i2D_\lambda^{-1}M_{W_d''}
 =-\partial_x^2+\frac14+
 \frac{W_d''}{W_d-2i\lambda}.
 \tag{4.1}
\]

The second equality uses

\[
 \lambda+\frac i2W_d=\frac i2(W_d-2i\lambda).
 \tag{4.2}
\]

A direct multiplication gives the operator identity

\[
 \boxed{
 (\lambda-A_2(d))L=D_\lambda T(d,\lambda),
 \qquad L:H^2_{\rm per}\longrightarrow L^2.}
 \tag{4.3}
\]

Indeed, both sides equal

\[
 \left(\lambda+\frac i2W_d\right)L+\frac i2W_d''.
 \tag{4.4}
\]

The outer factors \(L\) and \(D_\lambda\) are invertible, and the latter is
holomorphic in the open right half-plane.  Thus the linear operator pencil
\(\lambda-A_2(d)\) and the Rayleigh pencil

\[
 T(d,\lambda):H^2_{\rm per}\longrightarrow L^2
 \tag{4.5}
\]

are analytically equivalent.  The pencil in (4.5) is Fredholm of index zero:
after composition with \(L^{-1}\), it is the identity plus a compact
operator on \(L^2\).  Analytic equivalence preserves its characteristic
values and all partial multiplicities.

The equation \(T(d,\lambda)\phi=0\) is

\[
 (W_d-c)\left(\phi''-\frac14\phi\right)-W_d''\phi=0,
 \qquad c=2i\lambda.
 \tag{4.6}
\]

This also checks the sign of the phase-speed convention.  Since
\(\lambda=-ic/2\), a phase speed \(c=i\eta\), \(\eta>0\), corresponds to
the growing real eigenvalue \(\lambda=\eta/2\).

## 5. From the periodic boundary-value pencil to monodromy

This section records the stabilization and block elimination needed for
algebraic multiplicity.  It avoids inferring an operator multiplicity from a
finite determinant without an analytic equivalence.

Let \(P=2\pi\), let \(H^2=H^2(0,P)\) have no boundary condition, and let
\(T^\sharp(d,\lambda):H^2\to L^2(0,P)\) be the differential expression in
(4.1).  Define the boundary mismatch and initial trace by

\[
 \mathcal Bu=
 \binom{u(P)-u(0)}{u'(P)-u'(0)},
 \qquad
 \mathcal Cu=\binom{u(0)}{u'(0)}.
 \tag{5.1}
\]

The augmented periodic pencil is

\[
 \mathcal F(d,\lambda)=
 \binom{T^\sharp(d,\lambda)}{\mathcal B}:
 H^2\longrightarrow L^2(0,P)\times\mathbb C^2.
 \tag{5.2}
\]

First compare (5.2) with the periodic-domain pencil.  The map
\(\mathcal B:H^2\to\mathbb C^2\) is onto.  Choose a fixed bounded right
inverse \(R_B:\mathbb C^2\to H^2\).  Then

\[
 J:H^2_{\rm per}\times\mathbb C^2\longrightarrow H^2,
 \qquad J(v,b)=v+R_Bb,
 \tag{5.3}
\]

is an isomorphism, with inverse

\[
 J^{-1}u=(u-R_B\mathcal Bu,\mathcal Bu).
 \tag{5.4}
\]

In these coordinates,

\[
 \mathcal F(d,\lambda)J
 =\begin{pmatrix}
 T_{\rm per}(d,\lambda)&T^\sharp(d,\lambda)R_B\\
 0&I
 \end{pmatrix}.
 \tag{5.5}
\]

Multiplication on the left by the analytic invertible triangular operator

\[
 \begin{pmatrix}
 I&-T^\sharp(d,\lambda)R_B\\0&I
 \end{pmatrix}
 \tag{5.6}
\]

reduces (5.5) to

\[
 \operatorname{diag}(T_{\rm per}(d,\lambda),I).
 \tag{5.7}
\]

Thus \(\mathcal F\) and \(T_{\rm per}\), after adding an identity block,
have the same partial multiplicities.

Next use the initial-value problem.  The operator

\[
 \mathcal G(d,\lambda)=
 \binom{T^\sharp(d,\lambda)}{\mathcal C}:
 H^2\longrightarrow L^2(0,P)\times\mathbb C^2
 \tag{5.8}
\]

is an isomorphism.  Existence and uniqueness for the second-order initial-
value problem give bijectivity, and the standard energy estimate gives a
bounded inverse.  Parameter-dependent ODE theory makes
\(\mathcal G(d,\lambda)^{-1}\) holomorphic in \(\lambda\).

Let \(Y(x;d,\lambda)\) be the fundamental matrix of

\[
 Y'=\begin{pmatrix}0&1\\Q&0\end{pmatrix}Y,
 \qquad
 Q=\frac14+\frac{W_d''}{W_d-2i\lambda},
 \qquad Y(0)=I,
 \tag{5.9}
\]

and set \(M(d,\lambda)=Y(P;d,\lambda)\).  If
\(u=\mathcal G(d,\lambda)^{-1}(f,a)\), variation of constants gives

\[
 \mathcal Bu=R(d,\lambda)f+(M(d,\lambda)-I)a
 \tag{5.10}
\]

for an analytic bounded operator
\(R(d,\lambda):L^2(0,P)\to\mathbb C^2\).  Consequently

\[
 \mathcal F(d,\lambda)\mathcal G(d,\lambda)^{-1}
 =\begin{pmatrix}
 I&0\\R(d,\lambda)&M(d,\lambda)-I
 \end{pmatrix}.
 \tag{5.11}
\]

The analytic invertible left multiplier

\[
 \begin{pmatrix}I&0\\-R(d,\lambda)&I\end{pmatrix}
 \tag{5.12}
\]

reduces (5.11) to

\[
 \operatorname{diag}(I,M(d,\lambda)-I).
 \tag{5.13}
\]

Equations (5.5)--(5.13) are the required analytic BVP/IVP block
equivalence.  Therefore the periodic Rayleigh pencil and the analytic
two-by-two matrix \(M-I\) have the same nonzero partial multiplicities at
every characteristic value in the open right half-plane.

The first-order coefficient matrix in (5.9) has trace zero.  Liouville's
formula gives

\[
 \det M(d,\lambda)=1.
 \tag{5.14}
\]

Define

\[
 E(d,\lambda)=\det(M(d,\lambda)-I)
 =2-\operatorname{tr}M(d,\lambda).
 \tag{5.15}
\]

R0.73C used the real-line convention
\(F=\operatorname{tr}M-2\).  Thus the present convention is exactly
\(E=-F\).  The zero set and contour winding are unchanged by this constant
factor, while any quoted endpoint sign must be reversed.

For a finite analytic matrix, the order of its determinant is the sum of its
partial multiplicities.  Combining Sections 3--5 yields

\[
 \boxed{
 \operatorname{ord}_{\lambda_0}E(d,\lambda)
 =\operatorname{algmult}_{A_2(d)}(\lambda_0)
 =\operatorname{algmult}_{A_X(d)}(\lambda_0)}
 \tag{5.16}
\]

for every right-half-plane eigenvalue \(\lambda_0\).

In particular, an Evans zero of order one is an algebraically simple kinetic
eigenvalue.  This conclusion uses the analytic equivalences above; it does
not come merely from observing that \(\det(M-I)=0\).

## 6. Evans analyticity and reflection--conjugation symmetry

For real \(d\) and \(\operatorname{Re}\lambda>0\),

\[
 |W_d(x)-2i\lambda|\ge2\operatorname{Re}\lambda.
 \tag{6.1}
\]

The coefficient in (5.9), its fundamental solution, \(M\), and \(E\) are
therefore holomorphic in \(\lambda\).  They are real-analytic in real \(d\).
They also extend holomorphically to every sufficiently small complex
\(d\)-neighborhood on which the denominator remains uniformly nonzero.  A
future Bernstein-ellipse certificate must specify and validate such a
neighborhood; real analyticity alone is not an interval remainder bound.

The profile has the exact parity

\[
 W_d(P-x)=-W_d(x),\qquad W_d''(P-x)=-W_d''(x).
 \tag{6.2}
\]

Let \(S=\operatorname{diag}(1,-1)\).  If
\(z=(\phi,\phi')^T\) solves the homogeneous first-order system at
\(\lambda\), then

\[
 \widetilde z(x)=S\overline{z(P-x)}
 \tag{6.3}
\]

solves it at \(\bar\lambda\).  Comparing its values at \(0\) and \(P\)
gives

\[
 M(d,\bar\lambda)
 =S\,\overline{M(d,\lambda)^{-1}}\,S.
 \tag{6.4}
\]

Since a determinant-one two-by-two matrix satisfies
\(\operatorname{tr}M^{-1}=\operatorname{tr}M\), equations (5.15) and (6.4)
give

\[
 \boxed{E(d,\bar\lambda)=\overline{E(d,\lambda)}.}
 \tag{6.5}
\]

The same symmetry is visible directly on the kinetic operator.  If
\((\mathcal Rf)(x)=f(P-x)\) and \(\mathcal C f=\bar f\), then

\[
 \mathcal R A_X(d)\mathcal R=-A_X(d),
 \qquad
 \mathcal C A_X(d)\mathcal C=-A_X(d).
 \tag{6.6}
\]

The antiunitary map \(\mathcal R\mathcal C\) therefore commutes with
\(A_X(d)\) in the antilinear sense and maps every Jordan chain at
\(\lambda\) to a chain of the same length at \(\bar\lambda\).

## 7. The profile-specific Howard disk

Let \(\lambda\) be a right-half-plane eigenvalue, let \(c=2i\lambda\), and
let \(\phi\ne0\) be its smooth periodic Rayleigh eigenfunction.  Then
\(\operatorname{Im}c=2\operatorname{Re}\lambda>0\), so \(W_d-c\) never
vanishes.  Put

\[
 \phi=(W_d-c)F.
 \tag{7.1}
\]

Substitution in (4.6) gives

\[
 \left((W_d-c)^2F'\right)'
 -\frac14(W_d-c)^2F=0.
 \tag{7.2}
\]

The function \(F\) is periodic.  Multiplication by \(\bar F\), integration
over \(\mathbb T\), and periodic integration by parts give

\[
 \int_{\mathbb T}(W_d-c)^2
 \left(|F'|^2+\frac14|F|^2\right)\,dx=0.
 \tag{7.3}
\]

Set

\[
 G=|F'|^2+\frac14|F|^2,\qquad
 N=\int_{\mathbb T}G\,dx>0,
 \tag{7.4}
\]

and let brackets denote the probability average
\(\langle h\rangle_G=N^{-1}\int hG\).  Equation (7.3) becomes

\[
 c^2-2\langle W_d\rangle_Gc+\langle W_d^2\rangle_G=0.
 \tag{7.5}
\]

Because \(W_d\) is real and \(\operatorname{Im}c>0\),

\[
 c=\langle W_d\rangle_G
 +i\sqrt{\langle W_d^2\rangle_G-
 \langle W_d\rangle_G^2}.
 \tag{7.6}
\]

It follows that

\[
 |c|^2=\langle W_d^2\rangle_G
 \le\|W_d\|_\infty^2.
 \tag{7.7}
\]

It remains to bound the profile uniformly.  Write

\[
 a=e^{-d},\qquad b=e^{-4d},\qquad t=\cos x.
 \tag{7.8}
\]

For \(d\ge0\), \(0<b\le a\le1\), and

\[
 W_d(x)=\frac12\sin x(-a+bt).
 \tag{7.9}
\]

If \(t\ge0\), then \(|-a+bt|=a-bt\le1\), so
\(|W_d|\le1/2\).  If \(t=-s\le0\), where \(0\le s\le1\), then

\[
 |W_d|
 \le\frac12\sqrt{1-s^2}(1+s).
 \tag{7.10}
\]

The square of the last expression, apart from the factor \(1/4\), is
\((1-s)(1+s)^3\).  Its maximum on \([0,1]\) occurs at \(s=1/2\).  Hence

\[
 \|W_d\|_\infty\le\frac{3\sqrt3}{8}.
 \tag{7.11}
\]

Since \(|c|=2|\lambda|\), every right-half-plane eigenvalue satisfies

\[
 \boxed{|\lambda|\le\frac{3\sqrt3}{16}<\frac{13}{40}.}
 \tag{7.12}
\]

The strict comparison is exact:

\[
 \left(\frac{13}{40}\right)^2
 -\left(\frac{3\sqrt3}{16}\right)^2
 =\frac1{6400}>0.
 \tag{7.13}
\]

Together with (2.5), this controls every right-half-plane spectral point,
not only eigenvalues found by a finite Fourier compression.

## 8. Conditional analytic branch consequence

The following consequence records what a future contour certificate may use.
It is conditional; the required contour hypotheses have not been validated
in this note.

Suppose \(E(d_0,\lambda_0)=0\),
\(\operatorname{Re}\lambda_0>0\), and

\[
 \partial_\lambda E(d_0,\lambda_0)\ne0.
 \tag{8.1}
\]

The local complexification in \(d\) and the holomorphic implicit-function
theorem give a unique local holomorphic function \(d\mapsto\lambda_0(d)\).
For real \(d\), the symmetry (6.5) implies that this branch is real whenever
it is the unique zero in a conjugation-invariant neighborhood.

More generally, suppose a future validated calculation proves that a fixed
conjugation-invariant contour in \(\operatorname{Re}\lambda>0\) is zero-free
for every \(d\in[0,1/450]\), and that its positively oriented winding number
is one at one parameter value.  Homotopy invariance and the argument
principle then give one Evans zero counted with order throughout the
interval.  That zero has order one;
(5.16) makes the kinetic eigenvalue algebraically simple.  Symmetry makes it
real, and the local implicit branches patch uniquely to a real-analytic
branch on the whole interval.

No premise in the preceding paragraph is asserted to have passed interval
validation here.

## 9. Standard analytic-pencil facts used

I use the following standard results in their usual Banach-space forms.

1. The Fredholm essential spectrum is invariant under compact perturbations,
   and the spectrum of a continuous multiplication operator is its essential
   range.
2. The analytic Fredholm theorem makes noninvertible points discrete, with
   finite algebraic multiplicity, when an analytic Fredholm family of index
   zero is invertible at one point.
3. Parameter-dependent linear ODE solution operators are holomorphic when
   their coefficients are holomorphic; Liouville's formula gives the
   determinant of a fundamental matrix.
4. Left and right multiplication by analytic invertible operator families,
   and stabilization by identity blocks, preserve characteristic values and
   partial multiplicities of analytic Fredholm pencils.  This is the standard
   analytic-equivalence principle for operator pencils, often formulated in
   Gohberg--Sigal theory.
5. For the linear pencil \(\lambda-A\) at an isolated eigenvalue, the sum of
   its partial multiplicities equals the rank of the Riesz projection, hence
   the operator's algebraic multiplicity.
6. For a finite analytic matrix, the zero order of its determinant is the sum
   of its partial multiplicities.
7. A simple zero of a jointly holomorphic scalar function defines a unique
   local holomorphic branch by the implicit-function theorem.

Items 4--6 are used only after the explicit factorizations and block
equivalences in Sections 4 and 5.  No finite-section convergence statement is
used in this proof.

## 10. Source-stage ledger

| ID | Analytic conclusion in this note | Status after this draft |
|---|---|---|
| J0 | kinetic/Rayleigh equivalence, generalized-root equality, and right-half-plane discreteness | proof candidate; independent audit pending |
| J1 | Evans analyticity in the right half-plane and local complexification in \(d\) | proof candidate; explicit Bernstein ellipse remains part of the interval certificate |
| J2 | Evans zero order equals kinetic algebraic multiplicity | proof candidate; independent line-by-line audit pending |
| J3 | uniform Howard disk \(|\lambda|\le3\sqrt3/16\) | proof candidate; independent audit pending |
| J5--J7 | global winding and parameter-uniform contour nonvanishing | open; not addressed here |
| J10--J11 | kinetic overlap and fixed phase anchor | open; not addressed here |
