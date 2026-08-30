# R0.73K proof candidate: uniform viscous branch and complement control

**Status:** analytic proof; independent analytic and adversarial audits pass

**Depends on:** the sealed R0.73J continuum branch and overlap theorem

**Does not depend on:** finite Fourier diagnostics

## 1. Statement

Use the notation and constants of `research/r073k_problem_freeze.md`.  Thus

\[
 B_\varepsilon(d)=M_d+K_d-\varepsilon L,
 \qquad D(B_\varepsilon(d))=H^2_{\rm per},
 \tag{1.1}
\]

for \(\varepsilon>0\), while \(B_0(d)=M_d+K_d\) is bounded on \(H=L^2\).
The aim is the complete K1--K7 contract, with

\[
 D_*={1\over450},\qquad
 \Gamma_*=\{|z-0.17|=0.003\},\qquad
 b_K=0.12,\qquad c_K=0.16.
 \tag{1.2}
\]

The viscosity threshold obtained below is existential.  No explicit numerical
value of \(\varepsilon_K\) is claimed.

## 2. Uniform compact structure

The maps \(d\mapsto M_d\) and \(d\mapsto K_d\) are real analytic in operator
norm.  Indeed, the two Fourier coefficients of \(W_d\) are entire functions
of \(d\), multiplication is bounded on \(L^2\), and formula (1.6) in the
problem freeze contains only fixed powers of \(L\), multiplication, and a
commutator.  Each \(K_d\) is compact by the R0.73D commutator argument.

Consequently

\[
 \mathcal K:=\{K_d:0\le d\le D_*\}
 \tag{2.1}
\]

is compact in the operator norm.  It is also collectively compact: for any
\(\eta>0\), finitely many operators \(K_{d_j}\) form an \(\eta\)-net for
\(\mathcal K\); the image of the unit ball under each \(K_{d_j}\) has a
finite \(\eta\)-net, and the union of these finite nets covers
\(\{K_du:\|u\|\le1,0\le d\le D_*\}\) up to \(2\eta\).  The same statement
holds for \(\{K_d^*\}\).

## 3. Joint strong convergence of the base resolvents

Put

\[
 H_{\varepsilon,d}=M_d-\varepsilon L,
 \qquad
 R_{\varepsilon,d}(z)=(z-H_{\varepsilon,d})^{-1}.
 \tag{3.1}
\]

For \(\operatorname{Re}z>0\), maximal dissipativity gives

\[
 \|R_{\varepsilon,d}(z)\|\le {1\over\operatorname{Re}z}
 \tag{3.2}
\]

uniformly in \(\varepsilon\ge0\) and \(d\in[0,D_*]\).  Let
\(\mathcal Z\Subset\{\operatorname{Re}z>0\}\).  If \(f\in H^2_{\rm per}\),
then

\[
 u_{d,z}:=R_{0,d}(z)f=(z-M_d)^{-1}f
 \tag{3.3}
\]

belongs to \(H^2_{\rm per}\).  The multiplier \((z+iW_d/2)^{-1}\) and its
first two derivatives are uniformly bounded for
\((d,z)\in[0,D_*]\times\mathcal Z\).  Hence

\[
 \sup_{d\in[0,D_*],\,z\in\mathcal Z}\|Lu_{d,z}\|<\infty.
 \tag{3.4}
\]

The exact resolvent identity on this common core is

\[
 R_{\varepsilon,d}(z)f-R_{0,d}(z)f
 =-\varepsilon R_{\varepsilon,d}(z)L R_{0,d}(z)f.
 \tag{3.5}
\]

Equations (3.2)--(3.5), density of \(H^2_{\rm per}\) in \(H\), and a
uniform finite-net argument give

\[
 \sup_{d\in[0,D_*],\,z\in\mathcal Z}
 \|(R_{\varepsilon,d}(z)-R_{0,d}(z))f\|
 \longrightarrow0
 \quad(f\in H).
 \tag{3.6}
\]

The identical argument for
\(H_{\varepsilon,d}^*=-M_d-\varepsilon L\), with spectral parameter in
\(\overline{\mathcal Z}\), gives (3.6) for the adjoint resolvents.

Collective compactness now upgrades joint strong convergence to the two
operator-norm sandwiches

\[
 \sup_{d\in[0,D_*],\,z\in\mathcal Z}
 \|(R_{\varepsilon,d}(z)-R_{0,d}(z))K_d\|\longrightarrow0,
 \tag{3.7}
\]

\[
 \sup_{d\in[0,D_*],\,z\in\mathcal Z}
 \|K_d(R_{\varepsilon,d}(z)-R_{0,d}(z))\|\longrightarrow0.
 \tag{3.8}
\]

For (3.7), cover the collectively compact image of the unit ball by a finite
net and apply (3.6).  For (3.8), take adjoints and use the corresponding
argument for \(R_{\varepsilon,d}(z)^*\) and \(K_d^*\).  This proves K1 and
K2 without asserting norm convergence of the full base resolvents.

## 4. A common contour and norm convergence of its projection

For \(\operatorname{Re}z>0\), factor

\[
 z-B_\varepsilon(d)
 =(z-H_{\varepsilon,d})F_{\varepsilon,d}(z),
 \qquad
 F_{\varepsilon,d}(z)=I-R_{\varepsilon,d}(z)K_d.
 \tag{4.1}
\]

R0.73J puts \(\Gamma_*\) in \(\rho(B_0(d))\) for every \(d\).  Thus
\(F_{0,d}(z)\) is invertible on the compact set
\([0,D_*]\times\Gamma_*\), with a uniform inverse bound.  Equation (3.7)
gives

\[
 \sup_{d,z\in\Gamma_*}
 \|F_{\varepsilon,d}(z)-F_{0,d}(z)\|\longrightarrow0.
 \tag{4.2}
\]

For all sufficiently small \(\varepsilon\), the inverse therefore persists
uniformly, and

\[
 G_{\varepsilon,d}(z):=(z-B_\varepsilon(d))^{-1}
 =F_{\varepsilon,d}(z)^{-1}R_{\varepsilon,d}(z)
 \tag{4.3}
\]

is uniformly bounded on the common contour.

The identity

\[
 G_{\varepsilon,d}-R_{\varepsilon,d}
 =G_{\varepsilon,d}K_dR_{\varepsilon,d}
 \tag{4.4}
\]

contains the needed compact part.  First, (3.7), (4.2), and the uniform
inverse bound give

\[
 \begin{aligned}
 G_{\varepsilon,d}(z)K_d
 &=F_{\varepsilon,d}(z)^{-1}R_{\varepsilon,d}(z)K_d\\
 &\longrightarrow
 F_{0,d}(z)^{-1}R_{0,d}(z)K_d
 =G_{0,d}(z)K_d
 \end{aligned}
 \tag{4.5a}
\]

in operator norm, uniformly on
\([0,D_*]\times\Gamma_*\).  Next split

\[
 \begin{aligned}
 &G_{\varepsilon,d}K_dR_{\varepsilon,d}
   -G_{0,d}K_dR_{0,d}\\
 &\quad=(G_{\varepsilon,d}K_d-G_{0,d}K_d)R_{\varepsilon,d}
   +G_{0,d}K_d(R_{\varepsilon,d}-R_{0,d}).
 \end{aligned}
 \tag{4.5b}
\]

The first term tends to zero by (4.5a) and (3.2).  For the second,
\((d,z)\mapsto G_{0,d}(z)K_d\) is an operator-norm-continuous family of
compact operators on a compact parameter set.  Its adjoint family is
collectively compact.  Applying the adjoint version of (3.6) to that family
shows that the second term also tends to zero in norm, uniformly.  Therefore

\[
 \sup_{d,z\in\Gamma_*}
 \|G_{\varepsilon,d}K_dR_{\varepsilon,d}
   -G_{0,d}K_dR_{0,d}\|\longrightarrow0.
 \tag{4.5}
\]

Every base operator \(H_{\varepsilon,d}\) has spectrum in the closed left
half-plane, whereas the closed disk bounded by \(\Gamma_*\) lies in
\(\{\operatorname{Re}z>0\}\).  Hence

\[
 \int_{\Gamma_*}R_{\varepsilon,d}(z)\,dz=0.
 \tag{4.6}
\]

Subtracting (4.4), integrating, and using (4.5) gives

\[
 \boxed{
 \sup_{0\le d\le D_*}
 \|P_\varepsilon(d)-P_0(d)\|\longrightarrow0.}
 \tag{4.7}
\]

For small \(\varepsilon\), the norm difference is below one, so the two
projections have the same rank.  R0.73J gives \(\operatorname{rank}P_0(d)=1\);
therefore \(P_\varepsilon(d)\) has rank one uniformly in \(d\).  The same
cancellation with \(zR_{\varepsilon,d}(z)\) gives

\[
 \sup_d\|B_\varepsilon(d)P_\varepsilon(d)
       -B_0(d)P_0(d)\|\longrightarrow0.
 \tag{4.8}
\]

This proves K3 and also gives uniform \(o(1)\) convergence of the selected
eigenvalue.

## 5. The uniform \(O(\varepsilon)\) eigenvalue rate

The stronger rate does not follow from (4.8).  It uses the smooth inviscid
left eigenvector and never applies \(L\) to an uncontrolled difference of
eigenvectors.

Let \(h_0(d),\ell_0(d)\in H\) be unit right and left inviscid eigenvectors.
Under the unitary map from the kinetic space, the explicit R0.73J potentials
give

\[
 h_0\ \parallel\ 2L^{1/2}\phi_d,
 \qquad
 \ell_0\ \parallel\ 2L^{1/2}p_d,
 \qquad
 p_d={\overline{\phi_d}\over W_d+2i\lambda_0(d)}.
 \tag{5.1}
\]

The R0.73J selected solution is obtained from a first-order periodic ODE whose
coefficients and certified monodromy data are real analytic in \(d\).  Along
the real branch,

\[
 |W_d(x)+2i\lambda_0(d)|\ge2\lambda_0(d)>0.334.
 \tag{5.2a}
\]

Parameter-dependent ODE theory, differentiation of the equation in \(x\),
and (5.2a) show that \(d\mapsto\phi_d\) and \(d\mapsto p_d\) are continuous
into \(H^m_{\rm per}\) for every fixed \(m\).  The vector \(p_d\) is nonzero;
therefore the normalizing factor
\(\|2L^{1/2}p_d\|^{-1}\) is continuous and bounded on the compact interval.
In particular,

\[
 \ell_0(d)\in H^2_{\rm per}=D(L)
 \quad\hbox{and}\quad
 C_L:=\sup_{0\le d\le D_*}\|L\ell_0(d)\|<\infty.
 \tag{5.2}
\]

Choose phases so that

\[
 |\langle\ell_0(d),h_0(d)\rangle|>0.5853.
 \tag{5.3}
\]

Put \(h_\varepsilon(d)=P_\varepsilon(d)h_0(d)\).  Riesz functional calculus
also gives the bounded operator

\[
 B_\varepsilon(d)P_\varepsilon(d)
 ={1\over2\pi i}\int_{\Gamma_*}
 z(z-B_\varepsilon(d))^{-1}\,dz.
 \tag{5.3a}
\]

Consequently
\(P_\varepsilon(d)H\subset D(B_\varepsilon(d))=H^2_{\rm per}=D(L)\).
The rank-one result makes \(h_\varepsilon\) a viscous eigenvector, and both
sides of the later integration by parts with \(L\) are now in its domain.
Decrease \(\varepsilon_K\) until the left side of (4.7) is below \(2/25\).
Then

\[
 \|h_\varepsilon-h_0\|<\frac2{25},
 \qquad
 |\langle\ell_0,h_\varepsilon\rangle|
 >0.5853-0.08>\frac12,
 \qquad
 \|h_\varepsilon\|<\frac{27}{25}.
 \tag{5.4}
\]

Let \(\psi_{0,d}\) be the bounded left functional represented by
\(\ell_0(d)\), so that
\(\psi_{0,d}B_0(d)=\lambda_0(d)\psi_{0,d}\).  Pair the viscous eigen-equation
with \(\psi_{0,d}\).  Since \(h_\varepsilon\in H^2_{\rm per}\), self-adjointness
of \(L\) and (5.2) give the exact identity

\[
 (\lambda_\varepsilon-\lambda_0)
 \langle\ell_0,h_\varepsilon\rangle
 =-\varepsilon\langle L\ell_0,h_\varepsilon\rangle.
 \tag{5.5}
\]

Therefore

\[
 \boxed{
 \sup_d|\lambda_\varepsilon(d)-\lambda_0(d)|
 \le {11\over5}C_L\varepsilon.}
 \tag{5.6}
\]

This proves K4.  It is an existential quantitative rate because \(C_L\) is
not evaluated numerically in this section.

## 6. Reality, analyticity, anchor, and conditioning

Let \(\mathcal Rf(x)=f(-x)\), let \(\mathcal C\) be complex conjugation,
and put \(\Theta=\mathcal R\mathcal C\).  The profile and its second
derivative are odd, while \(L\) commutes with both \(\mathcal R\) and
\(\mathcal C\).  Moreover \(\Theta H^2_{\rm per}=H^2_{\rm per}\).
Directly from (1.5)--(1.7),

\[
 B_\varepsilon(d)\Theta=\Theta B_\varepsilon(d).
 \tag{6.1}
\]

The antiunitary symmetry sends an eigenvalue to its complex conjugate.  The
disk bounded by \(\Gamma_*\) is conjugation invariant and contains only one
algebraically simple eigenvalue, so \(\lambda_\varepsilon(d)\) is real.

For fixed \(\varepsilon>0\), \(d\mapsto B_\varepsilon(d)\) is a type-A
analytic family with common domain \(H^2_{\rm per}\).  The common contour and
simplicity make \(P_\varepsilon(d)\) and \(\lambda_\varepsilon(d)\) locally
real analytic; uniqueness in the disk glues the local branches across the
whole interval.

Riesz differentiation gives

\[
 \partial_dP_\varepsilon(d)
 ={1\over2\pi i}\int_{\Gamma_*}
 G_{\varepsilon,d}(z)\,\partial_d\widetilde A(d)\,
 G_{\varepsilon,d}(z)\,dz.
 \tag{6.2}
\]

The contour-resolvent bound and
\(\sup_d\|\partial_d\widetilde A(d)\|<\infty\) yield

\[
 \sup_{0<\varepsilon\le\varepsilon_K,\,0\le d\le D_*}
 \|\partial_dP_\varepsilon(d)\|<\infty.
 \tag{6.3}
\]

For a rank-one spectral projection, its norm is the reciprocal of the
normalized left--right overlap.  R0.73J gives

\[
 \|P_0(d)\|<{1\over0.5853}<1.709.
 \tag{6.4}
\]

Together with the \(2/25\) choice in (5.4),

\[
 \|P_\varepsilon(d)\|<1.789<{9\over5},
 \tag{6.5}
\]

so every pair of unit viscous right and left eigenvectors has overlap greater
than \(5/9\).

Finally choose the inviscid right vector \(\widehat h_0(d)\) real analytically
with \(\alpha(\widehat h_0)=1\).  The R0.73J anchor and compactness of the
parameter interval make this normalization regular.  Uniform projection
convergence gives

\[
 \alpha(P_\varepsilon(d)\widehat h_0(d))\ne0
 \tag{6.6}
\]

for small \(\varepsilon\), uniformly in \(d\).  Explicitly,

\[
 \sup_d|\alpha(P_\varepsilon\widehat h_0)-1|
 \le \|\alpha\|\sup_d\|\widehat h_0(d)\|
       \sup_d\|P_\varepsilon(d)-P_0(d)\|\longrightarrow0.
 \tag{6.6a}
\]

Thus

\[
 \widehat h_\varepsilon(d)=
 {P_\varepsilon(d)\widehat h_0(d)
  \over\alpha(P_\varepsilon(d)\widehat h_0(d))}
 \tag{6.7}
\]

is a fixed-anchor real-analytic viscous eigenvector.  This proves K5.

## 7. No pollution in the fixed half-plane

Write \(z=x+i\tau\), \(x\ge b_K\).  Since \(L\) is positive self-adjoint,

\[
 \|(z+\varepsilon L)^{-1}\|\le {1\over|\tau|}
 \qquad(\tau\ne0).
 \tag{7.1}
\]

The two Neumann factorizations are

\[
 z-H_{\varepsilon,d}
 =(z+\varepsilon L)
  [I-(z+\varepsilon L)^{-1}M_d],
 \qquad
 z-B_\varepsilon(d)
 =(z-H_{\varepsilon,d})[I-R_{\varepsilon,d}(z)K_d].
 \tag{7.1a}
\]

They yield, uniformly in \(d\) and \(\varepsilon\ge0\),

\[
 \|G_{\varepsilon,d}(z)\|
 \le {2\over|\tau|-M_*}
 \quad\text{if }|\tau|>M_*+2K_*,
 \tag{7.2}
\]

where \(M_*:=\sup_d\|M_d\|\) and \(K_*:=\sup_d\|K_d\|\).  Similarly, the
dissipative estimate \(\|R_{\varepsilon,d}(z)\|\le1/x\) excludes spectrum
for \(x>2K_*\).

Choose

\[
 T_*=M_*+2K_*+1,
 \qquad X_*=\max\{2K_*+1,b_K+1\}.
 \tag{7.2a}
\]

Only the compact set

\[
 \mathscr R=
 \{b_K\le\operatorname{Re}z\le X_*,\ |\operatorname{Im}z|\le T_*\}
 \setminus\{|z-0.17|<0.003\}
 \tag{7.2b}
\]

remains.  R0.73J says that \(\mathscr R\subset\rho(B_0(d))\) for every
\(d\).  The parameter-uniform Fredholm convergence of Sections 3--4, now
applied to the compact set \([0,D_*]\times\mathscr R\), gives a common
viscous resolvent bound there.  Hence, after decreasing \(\varepsilon_K\),

\[
 \boxed{
 \sigma(B_\varepsilon(d))\cap\{\operatorname{Re}z\ge0.12\}
 =\{\lambda_\varepsilon(d)\}.}
 \tag{7.3}
\]

The selected eigenvalue lies inside the real interval \((0.167,0.173)\),
while every complement spectral point has real part strictly below \(0.12\).
Each pointwise separation is therefore greater than \(0.047\); the uniform
safe constant asserted here is the smaller value \(1/25=0.04\).  This proves
the no-pollution part of K6.

## 8. The extended reduced resolvent

Let \(Q_\varepsilon(d)=I-P_\varepsilon(d)\).  Riesz functional calculus
gives

\[
 P_\varepsilon D(B_\varepsilon)\subset D(B_\varepsilon),
 \qquad
 Q_\varepsilon D(B_\varepsilon)\subset D(B_\varepsilon),
 \tag{8.1a}
\]

and both projections commute with \(B_\varepsilon\) on its domain.  Define
the part in the complementary space by

\[
 D(C_{\varepsilon,d})
 =D(B_\varepsilon(d))\cap Q_\varepsilon(d)H,
 \qquad
 C_{\varepsilon,d}=B_\varepsilon(d)|_{D(C_{\varepsilon,d})}.
 \tag{8.1b}
\]

Then define

\[
 \widehat G_{\varepsilon,d}(z)
 =(z-C_{\varepsilon,d})^{-1}Q_\varepsilon(d).
 \tag{8.1}
\]

The Riesz decomposition assigns all spectrum in the selected disk to the
rank-one \(P_\varepsilon\) block.  Hence the whole disk belongs to
\(\rho(C_{\varepsilon,d})\), including \(\lambda_\varepsilon(d)\).  Wherever
the full resolvent exists, (8.1) equals
\(G_{\varepsilon,d}(z)Q_\varepsilon(d)\); Sections 4 and 7 give a uniform
bound outside the disk and on \(\Gamma_*\).  Applying the scalar maximum
principle to
\(\langle f,\widehat G_{\varepsilon,d}(z)g\rangle\), with unit \(f,g\),
inside the disk gives

\[
 \boxed{
 \sup_{0<\varepsilon\le\varepsilon_K}
 \sup_{0\le d\le D_*}
 \sup_{\operatorname{Re}z\ge b_K}
 \|\widehat G_{\varepsilon,d}(z)\|<\infty.}
 \tag{8.2}
\]

This completes K6.  The proof uses resolvent control, not the spectral gap
alone.

## 9. Uniform complementary semigroup bounds

For \(\varepsilon>0\), \(-\varepsilon L+M_d+K_d\) generates an analytic
semigroup.  Riesz invariance in (8.1a) implies that
\(C_{\varepsilon,d}\) generates its restriction to
\(Q_\varepsilon(d)H\).  The base \(-\varepsilon L+M_d\) is maximally
dissipative, so

\[
 \|e^{tB_\varepsilon(d)}\|\le e^{K_*t}.
 \tag{9.1}
\]

Equations (7.2), (8.2), and the uniform projection bound imply on the line
\(b_K+i\mathbb R\)

\[
 \|(b_K+i\tau-C_{\varepsilon,d})^{-1}\|
 \le {C\over1+|\tau|}.
 \tag{9.2}
\]

Choose a fixed \(\omega>K_*\).  The short-time bound (9.1), together with
\(\sup\|Q_\varepsilon\|<\infty\), puts \(\omega\) to the right of a common
growth bound for every complementary semigroup.  Start the truncated
Bromwich formula on \(\omega+i\mathbb R\).  Integration by parts uses

\[
 {d\over d\tau}(x+i\tau-C_{\varepsilon,d})^{-1}
 =-i(x+i\tau-C_{\varepsilon,d})^{-2},
 \qquad b_K\le x\le\omega.
 \tag{9.3}
\]

On the line \(\operatorname{Re}z=\omega\), the boundary term vanishes by
(7.2), and the resulting square-resolvent integral is absolutely convergent.
Move that integral through the pole-free reduced strip
\(b_K\le\operatorname{Re}z\le\omega\).  Equation (7.2) holds throughout the
strip, so the horizontal integrals of the square resolvent are
\(O(|\tau|^{-2})\) and vanish uniformly.  It follows that, as an operator on
the full space after extension by \(Q_\varepsilon(d)\),

\[
 e^{tB_\varepsilon(d)}Q_\varepsilon(d)
 ={e^{b_Kt}\over2\pi t}
 \int_{\mathbb R}e^{i\tau t}
 (b_K+i\tau-C_{\varepsilon,d})^{-2}Q_\varepsilon(d)\,d\tau.
 \tag{9.3a}
\]

The integral is uniformly absolutely convergent: its integrand is bounded on
compact \(\tau\)-intervals by (8.2) and is \(O(|\tau|^{-2})\) at infinity by
(9.2).  For \(t\ge1\),

\[
 \|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|
 \le C e^{b_Kt}.
 \tag{9.4}
\]

For \(0\le t\le1\), use (9.1) and the uniform projection bound.  Enlarging
the constant gives (9.4) for all \(t\ge0\).

On the rank-one block,

\[
 e^{-tB_\varepsilon(d)}P_\varepsilon(d)
 =e^{-t\lambda_\varepsilon(d)}P_\varepsilon(d).
 \tag{9.5}
\]

Since \(\lambda_\varepsilon(d)>0.167>c_K\) and
\(\|P_\varepsilon(d)\|<9/5\),

\[
 \|e^{-tB_\varepsilon(d)}P_\varepsilon(d)\|
 \le {9\over5}e^{-c_Kt}.
 \tag{9.6}
\]

This proves K7.

## 10. Result ledger and boundary

The independent analytic and adversarial audits both pass.  Sections 2--9
therefore close

```text
uniformBaseStrongResolvent=CLOSED
collectiveCompactSandwich=CLOSED
uniformViscousContour=CLOSED
uniformRankOneViscousBranch=CLOSED
uniformProjectionNormConvergence=CLOSED
uniformEigenvalueOepsilon=CLOSED
uniformViscousConditioning=CLOSED
uniformProjectionDerivative=CLOSED
fixedHalfPlaneNoPollution=CLOSED
uniformReducedResolvent=CLOSED
uniformComplementSemigroup=CLOSED
explicitViscosityThreshold=OPEN
adiabaticTracking=OPEN
matchingAction=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The finite diagnostic planned for this section checks branch identity,
cutoff stability, and nonnormal conditioning.  It contributes no proof weight
to the continuum statements above.
