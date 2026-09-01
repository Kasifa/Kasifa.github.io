# R0.74D — zero-mean local-transport obstruction to the global-mean frame

## Status and scope

This note continues the exact gate frozen in
`r074d_zero_mean_local_transport_gate.md`.  It proves that subtracting only
the **global** spatial mean and translating by that constant mean does not
restore the pure large-payment endpoint from R0.74B.  More precisely, for
the Version-A quantities frozen there,

\[
 X_R^A=\mathcal U_{\rm ext}^{\infty,A}+\mathcal D_{\rm ext}^A,
 \qquad
 P_R^A=\mathcal E^A(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}^A(z_0,2R;1),
\tag{0.1}
\]

take \(z_0=(65R^2,0)\) and regard each solution on
\([0,66R^2]\times\mathbb T^3\).  Then one has

\[
 \boxed{
 \sup_{\substack{0<R<\pi/16\\
        (u,p)\ {\rm smooth\ periodic\ NSE}\\
        \overline u=0}}
 \frac{X_R^A}{(P_R^A)^{2/3}}=\infty.}
\tag{0.2}
\]

The proof uses the zero-total-mean exact 2D3C family from the gate.  Its
new analytic ingredient is not a globally small drift.  In the moving
reference coordinates the residual drift has a fixed sign.  On the side
of the packet facing the observation centre this sign improves the
Gaussian separation; on the other side, global \(L^2\) and \(L^3\)
contraction suffices after the lifted weights are integrated in the
invariant direction.

Equation (0.2) does **not** test a cylinder following a local or mollified
flow.  It does not test a local-mean subtraction, and it does not rule out
an explicit entrance-flux payment.  Labels are literal: **PROVED**,
**FINITE**, **OPEN**, and **NOT CLAY**.

Throughout,

\[
 \nu=1,\qquad \theta=1,\qquad
 \mathbb T^3=(-\pi,\pi]^3.
\tag{0.3}
\]

---

## 1. The exact family and a smaller harmless chart constant

Retain

\[
 q_*=\frac12,\qquad M_m=3\,2^{m-1},\qquad q_m=M_mR,
\tag{1.1}
\]

\[
 t_-=R^2,\qquad t_0=65R^2,\qquad T_R=66R^2,
\tag{1.2}
\]

and

\[
 D_R=e^{-R^2}-e^{-65R^2},\qquad
 B_R=\frac{q_m-q_*}{D_R}<0.
\tag{1.3}
\]

Put

\[
 q_{\rm pre}=q_*-B_R(1-e^{-R^2}),\qquad
 Q(t)=q_{\rm pre}+B_R(1-e^{-t}),
\tag{1.4}
\]

so that

\[
 Q(R^2)=q_*,\qquad Q(65R^2)=q_m.
\tag{1.5}
\]

We reduce the unspecified constant in the gate once and for all and work
under

\[
 0<R<R_1,\qquad M_m\ge64,\qquad
 q_m=M_mR\le\frac1{32},
\tag{1.6}
\]

where \(R_1>0\) is an absolute constant chosen below.  This is harmless
for the final sequence, where \(R\) tends superexponentially to zero.
Elementary mean-value bounds give

\[
 cR^{-2}\le |B_R|\le CR^{-2}.
\tag{1.7}
\]

Indeed, \(q_*-q_m\in[15/32,1/2]\), while

\[
 64R^2e^{-65R^2}\le D_R\le64R^2.
\tag{1.8}
\]

Let \(F=F_{R,m}\) be the unit-amplitude solution

\[
 \partial_tF+B_Re^{-t}\cos x_3\,\partial_2F
   =(\partial_2^2+\partial_3^2)F,
\tag{1.9}
\]

\[
 F(0,x_2,x_3)
 =R^3\partial_2K_{R^2}^{\rm per}(x_2-q_{\rm pre})
       K_{R^2}^{\rm per}(x_3).
\tag{1.10}
\]

For \(A>0\), set

\[
 \boxed{u=(AF,B_Re^{-t}\cos x_3,0),\qquad p=0.}
\tag{1.11}
\]

Proposition 2.1 of the gate proves directly that (1.11) is smooth,
periodic, divergence free, unforced, and has zero total spatial mean for
every time.  Consequently the Version-A change of frame is the identity
for this family.

---

## 2. Correct time-reversed diffusion representation

Introduce the reference-centred profile

\[
 G(t,z,x_3)=F(t,z+Q(t),x_3).
\tag{2.1}
\]

Since \(Q'(t)=B_Re^{-t}\), (1.9) becomes

\[
 \partial_tG=\Delta_{z,3}G+d(t,x_3)\partial_zG,
 \qquad
 d(t,x_3)=B_Re^{-t}(1-\cos x_3)\le0.
\tag{2.2}
\]

The sign in (2.2) is decisive.

Fix \(t\le t_0\).  Let \(W_2,W_3\) be independent standard real
Brownian motions and put, on the one-dimensional torus,

\[
 X_s^x=x+\sqrt2W_3(s)\pmod{2\pi},
\tag{2.3}
\]

\[
 \mathfrak D_t^x
 =\int_0^t d(t-s,X_s^x)\,ds
 =B_R\int_0^t e^{-(t-s)}(1-\cos X_s^x)\,ds\le0.
\tag{2.4}
\]

### Lemma 2.1 — time ordering and the packet formula

With \(\tau=R^2+t\),

\[
 \boxed{
 G(t,z,x)=R^3\mathbb E_x\!\left[
  \partial_zK_\tau^{\rm per}(z+\mathfrak D_t^x)
  K_{R^2}^{\rm per}(X_t^x)
 \right].}
\tag{2.5}
\]

**Proof.**  For fixed terminal time \(t\), start a diffusion at
\((z,x)\) whose generator at stochastic time \(s\) is

\[
 \Delta_{z,3}+d(t-s,x_3)\partial_z.
\tag{2.6}
\]

Applying Ito's formula to \(G(t-s,Z_s,X_s)\), the drift is

\[
 -\partial_tG+\Delta G+d(t-s,X_s)\partial_zG=0.
\tag{2.7}
\]

Thus \(G(t,z,x)\) is the expectation of the initial datum evaluated at
the terminal diffusion.  Conditional on the \(W_3\) path, heat convolution
in the independent \(W_2\) variable gives

\[
 \mathbb E_{W_2}\partial K_{R^2}^{\rm per}
 (z+\mathfrak D_t^x+\sqrt2W_2(t))
 =\partial K_{R^2+t}^{\rm per}(z+\mathfrak D_t^x).
\tag{2.8}
\]

This is (2.5). \(\square\)

The coefficient must be read at \(t-s\), not at \(s\).  This is the
time-ordering point that is invisible in an autonomous equation.

### Lemma 2.2 — chart and accumulated-shift bounds

After decreasing \(R_1\), for every parameter in (1.6) and every
\(0\le t\le t_0\),

\[
 |B_R|(1-e^{-t})\le\frac35,
 \qquad
 -\frac65\le\mathfrak D_t^x\le0,
 \qquad
 q_{\rm pre}\le\frac35.
\tag{2.9}
\]

Also, for \(|x|\le2R\),

\[
 \boxed{
 \mathbb E_x\!\left[|\mathfrak D_t^x|
 K_{R^2}^{\rm per}(X_t^x)\right]\le CR.}
\tag{2.10}
\]

**Proof.**  The first estimate follows from (1.3), (1.8),
\(1-e^{-t}\le1-e^{-65R^2}\), and continuity at \(R=0\); its limiting
constant is at most \((q_*-q_m)65/64<33/64\).  Equation (2.4) and
\(1-\cos\le2\) then give the second estimate.  Finally,

\[
 q_{\rm pre}=q_*+|B_R|(1-e^{-R^2})
 \longrightarrow q_*+\frac{q_*-q_m}{64}<\frac{33}{64}
 \tag{2.9a}
\]

uniformly under \(0\le q_m\le1/32\); shrinking \(R_1\) gives the last
bound in (2.9).

For (2.10), use

\[
 \|K_{R^2}^{\rm per}\|_\infty\le CR^{-1}
\tag{2.11}
\]

and the exact torus Brownian identity

\[
 \mathbb E_x(1-\cos X_s^x)
 =1-e^{-s}\cos x
 \le s+\frac{x^2}{2}\le CR^2
\tag{2.12}
\]

for \(s\le t_0\) and \(|x|\le2R\).  Hence

\[
 \begin{aligned}
 \mathbb E_x[|\mathfrak D_t^x|K_{R^2}^{\rm per}(X_t^x)]
 &\le |B_R|\int_0^t
 \mathbb E_x[(1-\cos X_s^x)K_{R^2}^{\rm per}(X_t^x)]\,ds\\
 &\le CR^{-2}\,R^2\,(R^{-1}R^2)
 \le CR.
 \end{aligned}
\tag{2.13}
\]

No global smallness of \(d\) was used. \(\square\)

---

## 3. Uniform survival at the target annulus

### Lemma 3.1 — pointwise target lower bound

There are fixed

\[
 1<b_1<b_2<2,\qquad c_3>0,\qquad \varepsilon_0>0,
\tag{3.1}
\]

such that, after decreasing \(R_1\),

\[
 \boxed{|F(t,Q(t)+z,x_3)|\ge c_3}
\tag{3.2}
\]

whenever

\[
 t_0-\varepsilon_0R^3<t<t_0,\qquad
 b_1R\le z\le b_2R,\qquad |x_3|\le R.
\tag{3.3}
\]

**Proof.**  By the torus heat semigroup,

\[
 \mathbb E_xK_{R^2}^{\rm per}(X_t^x)
 =K_\tau^{\rm per}(x).
\tag{3.4}
\]

Subtract the zero-residual-drift value in (2.5).  The mean-value theorem,
the periodic heat-kernel bound

\[
 \|\partial^2K_\tau^{\rm per}\|_\infty\le CR^{-3}
 \quad(65R^2\le\tau\le66R^2),
\tag{3.5}
\]

and (2.10) give

\[
 \left|G(t,z,x)-R^3\partial K_\tau^{\rm per}(z)
 K_\tau^{\rm per}(x)\right|\le CR.
\tag{3.6}
\]

For \(z/R\in[b_1,b_2]\), \(|x|/R\le1\), and
\(\tau/R^2\in[65,66]\), the central real-Gaussian term in

\[
 R^3\partial K_\tau^{\rm per}(z)K_\tau^{\rm per}(x)
\tag{3.7}
\]

has one sign and absolute value bounded below by a fixed positive constant.
The noncentral periodic images are \(O(e^{-c/R^2})\).  Thus (3.7) is at
least \(2c_3\) in absolute value for small \(R\), whereas (3.6) is at most
\(c_3\).  The slightly shorter time interval in (3.3) stays inside the
same compact dimensionless heat-age range. \(\square\)

### Proposition 3.2 — the annular target

For the exact solution (1.11),

\[
 \boxed{
 X_R^A\ge\mathcal U_{\rm ext}^{\infty,A}
 \ge cA^2M_mR^2e^{-M_m^2/288}.}
\tag{3.8}
\]

**Proof.**  On the interval (3.3),

\[
 |Q(t)-q_m|\le C|B_R|R^3\le CR.
\tag{3.9}
\]

Choose \(\varepsilon_0\) and then \(R_1\) so that the set

\[
 \begin{aligned}
 \Omega_t=\{x:\;& |x_1|<q_m/8,\quad
 b_1R<x_2-Q(t)<b_2R,\\
 &|x_3|<R\}
 \end{aligned}
\tag{3.10}
\]

is contained in

\[
 A_m(R)=\{2^mR\le|x|<2^{m+1}R\}.
\tag{3.11}
\]

Indeed, \(2^mR=2q_m/3\), \(2^{m+1}R=4q_m/3\), and every error in
(3.10) other than the \(x_1\) width is \(O(R)=O(q_m/M_m)\).  Moreover,

\[
 |\Omega_t|\ge cM_mR^3.
\tag{3.12}
\]

Lemma 3.1 and the exact identity

\[
 \gamma_m=e^{-4^{m-1}/32}=e^{-M_m^2/288}
\tag{3.13}
\]

now give

\[
 R^{-1}\gamma_m\int_{\Omega_t}|AF|^2
 \ge cA^2M_mR^2e^{-M_m^2/288}.
\tag{3.14}
\]

The time interval has positive measure inside \(I_R\), so the essential
supremum is licensed. \(\square\)

---

## 4. One-sided Gaussian bounds and buffered leakage

The residual displacement in (2.4) is nonpositive.  Therefore, whenever
\(z<0\) and both \(z\) and \(z+\mathfrak D_t^x\) remain in the central
torus chart,

\[
 |z+\mathfrak D_t^x|\ge|z|.
\tag{4.1}
\]

This replaces the unavailable global estimate \(d=O(R)\).

### Lemma 4.1 — local packet and gradient leakage

Let

\[
 \Pi_m=(1+M_m)^{18}.
\tag{4.2}
\]

After decreasing \(R_1\), throughout

\[
 I_{8R}\times B_{8R}
 =(R^2,65R^2)\times B_{8R},
\tag{4.3}
\]

one has

\[
 \boxed{
 |F|+R|\partial_2F|+R|\partial_3F|
 \le C\Pi_m^{1/3}e^{-M_m^2/528}.}
\tag{4.4}
\]

Consequently,

\[
 |F|^2+R^2|\nabla F|^2
 \le C\Pi_m^{2/3}e^{-M_m^2/264},
\tag{4.5}
\]

and

\[
 |F|^3\le C\Pi_m e^{-M_m^2/176}.
\tag{4.6}
\]

**Proof.**  On \(I_{8R}\), \(Q(t)\ge q_m=M_mR\).  If
\((x_2,x_3)\in B_{8R}\) and \(z=x_2-Q(t)\), then

\[
 z\le-(M_m-8)R<0.
\tag{4.7}
\]

Equations (1.4), (1.6), and (2.9) place both \(z\) and
\(z+\mathfrak D_t^{x_3}\) in the central half-chart
\((-\pi,0)\).  More explicitly, (1.6) implies \(R\le1/2048\), while
\(q_m\le Q(t)\le q_*\); hence

\[
 -\frac12-8R\le z\le-(M_m-8)R<0,
 \qquad
 -\frac12-8R-\frac65<z+\mathfrak D_t^{x_3}<0.
 \tag{4.7a}
\]

The left endpoint in (4.7a) is strictly larger than \(-\pi\).  Thus no
path can wrap through the \(-\pi\) seam.  Hence (4.1) applies, and the
nearest periodic kernel centre is zero.  Since

\[
 2R^2\le\tau=R^2+t\le66R^2,
\tag{4.8}
\]

the first two heat-kernel derivatives obey

\[
 R^2|\partial K_\tau^{\rm per}(z+\mathfrak D)|
 +R^3|\partial^2K_\tau^{\rm per}(z+\mathfrak D)|
 \le C(1+M_m)^6e^{-M_m^2/528}.
\tag{4.9}
\]

Indeed, with \(a=|z+\mathfrak D|/R\ge M_m-8\ge56\), the real-line
Gaussian derivative factors are bounded by a fixed quadratic polynomial
in \(a\) times \(e^{-a^2/264}\).  This function is decreasing in the
present range, and

\[
 \frac{(M_m-8)^2}{264}\ge\frac{M_m^2}{528}
 \quad(M_m\ge64).
\tag{4.10}
\]

This proves the central-image contribution in (4.9), with ample room in
the displayed degree six.  By (4.7a), the distance to every noncentral
periodic image is bounded below by an absolute positive constant.  Since
\(M_mR\le1/32\), its \(e^{-c/R^2}\) contribution is smaller than the
right side of (4.9).  Thus all periodic copies are included.

Equation (2.5), together with

\[
 \mathbb E_xK_{R^2}^{\rm per}(X_t^x)\le CR^{-1},
\tag{4.11}
\]

gives the bounds for \(F\) and \(\partial_2F\).

For the remaining derivative, pathwise differentiation with respect to
the starting point gives

\[
 \partial_x\mathfrak D_t^x
 =B_R\int_0^te^{-(t-s)}\sin X_s^x\,ds,
 \qquad |\partial_x\mathfrak D_t^x|\le C,
\tag{4.12}
\]

and

\[
 \begin{aligned}
 \partial_xG=R^3\mathbb E_x[&
  \partial^2K_\tau^{\rm per}(z+\mathfrak D_t^x)
  (\partial_x\mathfrak D_t^x)K_{R^2}^{\rm per}(X_t^x)\\
 &+\partial K_\tau^{\rm per}(z+\mathfrak D_t^x)
  \partial K_{R^2}^{\rm per}(X_t^x)].
 \end{aligned}
\tag{4.13}
\]

Use (4.9), (4.11), and
\(\|\partial K_{R^2}^{\rm per}\|_\infty\le CR^{-2}\).
This proves (4.4).  The exponent and polynomial choices in (4.5)--(4.6)
are direct powers of (4.4): degree six becomes degree twelve in the
quadratic row and degree eighteen in the cubic row. \(\square\)

### Corollary 4.2 — buffered local energy

For the full solution (1.11),

\[
 \boxed{
 \mathcal E^A(z_0,8R)
 \le C\left[R^{-2}
 +A^2R^2\Pi_m^{2/3}e^{-M_m^2/264}\right].}
\tag{4.14}
\]

**Proof.**  The \(b_R\) component contributes at most

\[
 C|B_R|^2R^2+C|B_R|^2R^6\le CR^{-2}.
\tag{4.15}
\]

The two terms are respectively its local \(L^2\) row and its
\(\partial_3b_R\) dissipation row.  For \(AF\), use (4.5),
\(|B_{8R}|\asymp R^3\), and \(|I_{8R}|=64R^2\).  The velocity components
and their gradient entries are orthogonal, so no quadratic cross term is
missing. \(\square\)

---

## 5. Lifted weights after the invariant direction is integrated

At \(S=2R\), define

\[
 W_S(y)=\sum_{j\ge1}\gamma_j1_{A_j(S)}(y),
\qquad
 L_S(y)=S\sum_{j\ge1}(2^jS)^{-4}1_{A_j(S)}(y).
\tag{5.1}
\]

The R0.74C weight lemma gives

\[
 W_S(y)\le\frac{CS^4}{(|y|^2+S^2)^2},
 \qquad
 L_S(y)\le\frac{CS}{(|y|^2+S^2)^2}.
\tag{5.2}
\]

The right sides also cover the first annulus after changing the constant.
For \(x=(x_2,x_3)\in\mathbb T^2\), define the effective periodic weights

\[
 \omega_S(x)
 =\sum_{n\in\mathbb Z^2}\int_{\mathbb R}
 W_S(y_1,x+2\pi n)\,dy_1,
\tag{5.3}
\]

\[
 \ell_S(x)
 =\sum_{n\in\mathbb Z^2}\int_{\mathbb R}
 L_S(y_1,x+2\pi n)\,dy_1.
\tag{5.4}
\]

### Lemma 5.1 — all-copy two-dimensional weights

If \(\rho(x)={\rm dist}_{\mathbb T^2}(x,0)\), then

\[
 \boxed{
 \omega_S(x)\le\frac{CS^4}{(\rho(x)^2+S^2)^{3/2}},
 \qquad
 \ell_S(x)\le\frac{CS}{(\rho(x)^2+S^2)^{3/2}}.}
\tag{5.5}
\]

**Proof.**  Integrating (5.2) in \(y_1\) uses

\[
 \int_{\mathbb R}(y_1^2+a^2)^{-2}\,dy_1=Ca^{-3}.
\tag{5.6}
\]

The central lattice term gives (5.5).  The remaining two-dimensional
lattice sum is dominated by \(C\sum_{n\ne0}|n|^{-3}<\infty\), and is
absorbed by the displayed right side because the torus diameter is fixed.
Thus every lifted annulus and periodic copy is included. \(\square\)

### Lemma 5.2 — contraction and the one-sided packet envelope

For \(p=2,3\),

\[
 \boxed{\|F(t)\|_{L^p(\mathbb T^2)}^p\le CR^2.}
\tag{5.7}
\]

Moreover, if \(q=Q(t)\), \(|x_2|\le1\), \(|x_3|\le1\), and
\(x_2<q\), then

\[
 \boxed{
 |F(t,x_2,x_3)|
 \le C\exp\!\left[-c\frac{(q-x_2)^2+x_3^2}{R^2}\right]}
\tag{5.8}
\]

for \(t\in I_S=(61R^2,65R^2)\).

**Proof.**  Multiplication of (1.9) by
\(|F|^{p-2}F\), periodic integration, and the fact that
\(B_Re^{-t}\cos x_3\) is independent of \(x_2\) give \(L^p\)
contraction.  Direct periodic heat-kernel scaling of (1.10) gives
\(\|F(0)\|_p^p\le CR^2\).

For (5.8), put \(z=x_2-q<0\) in (2.5).  After shrinking \(R_1\), the
endpoint identities (1.5) give \(q_m\le q\le1/8\) on \(I_S\).  Explicitly,
for \(61R^2\le t\le65R^2\),

\[
 0\le Q(t)-q_m
 \le(q_*-q_m)
 \frac{e^{-61R^2}-e^{-65R^2}}
      {e^{-R^2}-e^{-65R^2}}
 \le\frac1{16}
 \tag{5.7a}
\]

for small \(R\), and \(q_m\le1/32\).  Equations (2.9) and the stated
central chart then give

\[
 -\frac98\le z<0,
 \qquad
 -\frac{93}{40}\le z+\mathfrak D_t^{x_3}<0,
 \tag{5.7b}
\]

where \(-93/40>-\pi\).  Thus every sampled point remains in the central
chart; no path can gain proximity by wrapping to the adjacent periodic
centre.  By (4.1), the first kernel factor is bounded by

\[
 CR^{-2}\exp[-cz^2/R^2].
\tag{5.9}
\]

After this pathwise bound has been taken outside the expectation, the
remaining endpoint factor averages exactly to

\[
 K_{R^2+t}^{\rm per}(x_3)
 \le CR^{-1}e^{-cx_3^2/R^2}
\tag{5.10}
\]

in this chart.  Multiplication by \(R^3\) proves (5.8). \(\square\)

### Lemma 5.3 — packet moments at distance \(q\)

For \(t\in I_S\),

\[
 q_m=M_mR\le q=Q(t)\le\frac18,
\tag{5.11}
\]

after decreasing \(R_1\), and

\[
 \boxed{
 \int_{\mathbb R^3}W_S(y)|\widetilde F(t,y_2,y_3)|^3\,dy
 \le\frac{CR^6}{q^3},}
\tag{5.12}
\]

\[
 \boxed{
 \int_{\mathbb R^3}L_S(y)|\widetilde F(t,y_2,y_3)|^2\,dy
 \le\frac{CR^3}{q^3}.}
\tag{5.13}
\]

**Proof.**  The short interval \(I_S\) traverses only a fixed small
fraction of the displacement in (1.5), proving (5.11).  By unfolding,
the left sides in (5.12)--(5.13) equal the corresponding integrals of
\(\omega_S|F|^3\) and \(\ell_S|F|^2\) over \(\mathbb T^2\).

Outside the central box \(|x_2|,|x_3|\le1\), or inside that box with
\(x_2\ge q\), the torus distance from zero is at least \(cq\).  Therefore
(5.5) and (5.7) give respectively

\[
 C\frac{S^4}{q^3}R^2\le C\frac{R^6}{q^3},
 \qquad
 C\frac{S}{q^3}R^2\le C\frac{R^3}{q^3}.
\tag{5.14}
\]

In the remaining one-sided box, use (5.8) and the elementary Gaussian
convolution bounds

\[
 \int_{\mathbb R^2}
 \frac{S^4e^{-c|x-(q,0)|^2/R^2}}
      {( |x|^2+S^2)^{3/2}}\,dx
 \le C\frac{S^4R^2}{(q^2+S^2)^{3/2}},
\tag{5.15}
\]

\[
 \int_{\mathbb R^2}
 \frac{Se^{-c|x-(q,0)|^2/R^2}}
      {( |x|^2+S^2)^{3/2}}\,dx
 \le C\frac{SR^2}{(q^2+S^2)^{3/2}}.
\tag{5.16}
\]

To prove either inequality, split at
\(|x-(q,0)|=q/2\).  On the near part the denominator is comparable to
\(q^3\) and the Gaussian mass is \(O(R^2)\).  On the far part, its
\(e^{-cq^2/R^2}\) factor beats every fixed negative power of
\(q/R\ge M_m\ge64\), while the two displayed weights have total masses
\(O(S^3)\) and \(O(1)\).  Since \(S=2R\) and \(q\ge64R\),
(5.15)--(5.16) are exactly the remaining parts of (5.12)--(5.13).
\(\square\)

---

## 6. Frozen gauge and the full payment ledger

### Lemma 6.1 — the physical zero pressure does not erase \(G_p\)

At scale \(S=2R\), let

\[
 p_S^{\rm loc}=\mathcal R_i\mathcal R_j
   (\zeta_S\widetilde u_i\widetilde u_j),
 \qquad h_S=-p_S^{\rm loc},
 \qquad c_S=(h_S)_{B_{2S}}.
\tag{6.1}
\]

Then

\[
 \boxed{
 \mathcal G_p^A(z_0,S;1)
 \le CS^{-2}\int_{I_S}\int_{B_{4S}}|u|^3.}
\tag{6.2}
\]

**Proof.**  Jensen and the whole-space Calderon--Zygmund inequality give

\[
 |c_S(t)|^{3/2}
 \le CS^{-3}\int_{B_{4S}}|u(t)|^3.
\tag{6.3}
\]

Although \(p=0\), the frozen quantity in the pressure annuli is
\(|p-c_S|^{3/2}=|c_S|^{3/2}\).  Since
\(\int_{\mathbb R^3}W_S\le CS^3\), (6.2) follows. \(\square\)

### Lemma 6.2 — Gaussian velocity and pressure rows

\[
 \boxed{
 \mathcal G_u^A(z_0,S;1)
 \le C\left[R^{-3}+\frac{A^3R^4}{M_m^2}\right],}
\tag{6.4}
\]

\[
 \boxed{
 \mathcal G_p^A(z_0,S;1)
 \le C\left[R^{-3}
 +A^3R^3\Pi_m e^{-M_m^2/176}\right].}
\tag{6.5}
\]

**Proof.**  Since

\[
 |u|^3\le C(A^3|F|^3+|B_R|^3),
\tag{6.6}
\]

the background part of \(\mathcal G_u\) is at most

\[
 CS^{-2}|I_S||B_R|^3\int W_S
 \le C|B_R|^3R^3\le CR^{-3}.
\tag{6.7}
\]

For the packet, (5.12) and

\[
 dt=\frac{-dq}{|B_R|e^{-t}}\le CR^2(-dq)
\tag{6.8}
\]

give

\[
 \begin{aligned}
 S^{-2}A^3\int_{I_S}\frac{CR^6}{Q(t)^3}\,dt
 &\le CA^3R^6\int_{M_mR}^{1/8}\frac{dq}{q^3}\\
 &\le\frac{CA^3R^4}{M_m^2}.
 \end{aligned}
\tag{6.9}
\]

This proves (6.4).  Apply (6.2), (6.6), and the local estimate (4.6)
on \(B_{4S}=B_{8R}\).  The background gives \(CR^{-3}\), while the
packet gives the second term of (6.5).  The apparent mixed local-pressure
source is already covered by
\((A|F||b_R|)^{3/2}\le C(A^3|F|^3+|b_R|^3)\). \(\square\)

### Lemma 6.3 — algebraic harmonic row

\[
 \boxed{
 \mathcal H_u^A(z_0,S)
 \le C\left[R^{-3}
 +\frac{A^3R^4}{M_m^{7/2}}\right].}
\tag{6.10}
\]

**Proof.**  Equations (5.1), (5.13), and the orthogonality of the two
velocity components give

\[
 \Lambda_S(t)
 \le C\left[|B_R|^2+\frac{A^2R^3}{Q(t)^3}\right].
\tag{6.11}
\]

Therefore, using (6.8),

\[
 \begin{aligned}
 \mathcal H_u^A
 &=S\int_{I_S}\Lambda_S(t)^{3/2}\,dt\\
 &\le CS|I_S||B_R|^3
 +CA^3R\,R^{9/2}R^2
   \int_{M_mR}^{1/8}q^{-9/2}\,dq\\
 &\le CR^{-3}+\frac{CA^3R^4}{M_m^{7/2}}.
 \end{aligned}
\tag{6.12}
\]

All algebraic annuli and periodic copies entered through (5.13). \(\square\)

### Proposition 6.4 — one simultaneous payment

\[
 \boxed{
 P_R^A\le C\left[
 R^{-3}
 +A^3R^3\Pi_m e^{-M_m^2/176}
 +\frac{A^3R^4}{M_m^2}
 \right].}
\tag{6.13}
\]

Consequently,

\[
 \boxed{
 (P_R^A)^{2/3}\le C\left[
 R^{-2}
 +A^2R^2\Pi_m e^{-M_m^2/264}
 +A^2R^{8/3}M_m^{-4/3}
 \right].}
\tag{6.14}
\]

**Proof.**  Raise (4.14) to the \(3/2\) power, then combine Lemmas
6.2--6.3.  The \(M_m^{-7/2}\) row is smaller than the
\(M_m^{-2}\) row.  The degree-eighteen definition (4.2) covers the
cubic leakage exactly, while the quadratic leakage in (4.14) carries only
\(\Pi_m^{2/3}\).  Finally use the subadditivity of \(x^{2/3}\) on the
nonnegative half-line. \(\square\)

---

## 7. Explicit divergence sequence

Let

\[
 M_m=3\,2^{m-1}\longrightarrow\infty,
 \qquad
 \boxed{
 R_m=e^{-M_m^2/96},\qquad
 \mathfrak a_m=R_m^{-2}e^{M_m^2/576}.}
\tag{7.1}
\]

For all sufficiently large \(m\), (1.6) holds.  Proposition 3.2 gives

\[
 L_m:=c\mathfrak a_m^2M_mR_m^2e^{-M_m^2/288}
 =cM_mR_m^{-2}.
\tag{7.2}
\]

Against the three rows of (6.14), respectively,

\[
 \frac{L_m}{R_m^{-2}}=cM_m\longrightarrow\infty,
\tag{7.3}
\]

\[
 \frac{L_m}{\mathfrak a_m^2R_m^2\Pi_m e^{-M_m^2/264}}
 =\frac{cM_m}{\Pi_m}
 e^{M_m^2(1/264-1/288)}\longrightarrow\infty,
\tag{7.4}
\]

and

\[
 \begin{aligned}
 \frac{L_m}{\mathfrak a_m^2R_m^{8/3}M_m^{-4/3}}
 &=cM_m^{7/3}R_m^{-2/3}e^{-M_m^2/288}\\
 &=cM_m^{7/3}e^{M_m^2/288}\longrightarrow\infty.
 \end{aligned}
\tag{7.5}
\]

Equations (6.14) and (7.3)--(7.5) prove

\[
 \boxed{
 \frac{X_{R_m}^A}{(P_{R_m}^A)^{2/3}}\longrightarrow\infty,}
\tag{7.6}
\]

which is (0.2).

The geometry differs from R0.74C.  The packet is localized at scale \(R\)
in both \(x_2\) and \(x_3\), but is invariant in \(x_1\).  Its target
volume is therefore \(M_mR^3\), and integrating the exterior weights in
the invariant direction produces a \(q^{-3}\) marginal.  This is why the
leading packet payment is \(A^3R^4/M_m^2\), rather than the
R0.74C strip row \(A^3R^4/M_m\).

---

## 8. Prior-art boundary and what remains open

The PDE subspace used here is a classical two-dimensional,
three-component (2D3C) invariant class: the planar velocity evolves by 2D
Navier--Stokes and the out-of-plane component is passively advected.  The
special planar velocity in (1.11) is itself a decaying shear.  Thus this
note makes no novelty claim for the exact family, for passive transport,
or for the 2D3C reduction.

Likewise, Galilean reductions, local or mollified mean subtraction,
flow-following trajectories, and skewed cylinders are established in the
Vasseur--Choi--Yang line of work.  The claim proved here is only the narrow
conjunction in (0.2): the particular frozen R0.74B Version-A annular
ledger is not controlled at arbitrary payment by removing the constant
global mean alone.

The following remain **OPEN**:

1. the same pure endpoint for a cylinder following a local or mollified
   flow;
2. a formulation subtracting a local spatial mean at each scale;
3. a fixed-centre formulation retaining a signed entrance-flux payment;
4. the optimal large-payment exponent after a transport-aware repair;
5. any absorption, epsilon-regularity, or continuation consequence.

---

## 9. Audit ledger

### PROVED

1. The family (1.11) is exact, smooth, periodic, unforced, divergence
   free, and has zero total spatial mean.
2. The nonautonomous stochastic representation (2.5) has the correct
   reverse time ordering.
3. The residual displacement has one sign and its target-weighted first
   moment is \(O(R)\), without a global coefficient-smallness claim.
4. The packet survives on a positive target time slab and gives (3.8).
5. The buffered packet and both spatial gradients have the strict leakage
   exponent (4.4)--(4.6).
6. The effective weights (5.5) include every lifted annulus and periodic
   copy.
7. One-sided Gaussian control plus global \(L^2/L^3\) contraction gives
   both packet moments (5.12)--(5.13).
8. The physical pressure is zero, but the frozen cutoff gauge is retained
   and paid in (6.2)--(6.5).
9. Every \(b_R\) background, packet, gradient, pressure, and harmonic row
   enters the simultaneous bound (6.13).
10. The three independent ratios (7.3)--(7.5) diverge.

### FINITE

For each fixed \(m\), \(R_m>0\), \(\mathfrak a_m<\infty\), and the corresponding
solution is analytic on the compact time interval.  Every positive-scale
quantity in (0.1) is finite.  The sequence has no uniform global energy
bound, and none is assumed by the endpoint under test.

### NOT CLAY

Equation (0.2) is a negative positive-scale estimate inside a classical
globally smooth invariant subspace.  It proves no singularity, no blow-up,
no epsilon-regularity theorem, and no global regularity or breakdown result
for general three-dimensional Navier--Stokes solutions.  It is not a
solution or partial solution of the Clay Millennium problem.
