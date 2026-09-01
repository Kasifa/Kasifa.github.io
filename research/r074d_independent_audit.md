# R0.74D — independent analytic audit of the zero-mean local-transport obstruction

**Audit date:** 2026-09-01

**Status:** `PASS`

**Frozen theorem commit:**
`ff80370fe33094f1423d312b817dfec0bf42d664`

**Frozen theorem blob:**
`c987e8928d2167d146055750a7afdfd24b369bf1`

**Frozen theorem file:**
`research/r074d_zero_mean_local_transport_obstruction.md`

**Frozen theorem SHA-256:**
`bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124`

This audit independently recalculates the analytic proof in the frozen
theorem file.  The R0.74D gate and the earlier R0.74B definitions were used
only to recover the exact Version-A observables and pressure gauge.  No
finite certificate, numerical experiment, simulation, or literature search
was treated as proof of an analytic estimate.

The conclusion is that the frozen construction supports

\[
 \boxed{
 \sup_{\substack{0<R<\pi/16\\
        (u,p)\ {\rm smooth\ periodic\ NSE}\\
        \overline u=0}}
 \frac{\mathcal U_{\rm ext}^{\infty,A}+\mathcal D_{\rm ext}^A}
 {\left(\mathcal E^A(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}^A(z_0,2R;1)\right)^{2/3}}
 =\infty, }
\]

with \(z_0=(65R^2,0)\), \(\nu=\theta=1\), and the exact smooth
zero-total-mean family below.  No theorem-fatal gap was found.

---

## 1. Audit scope and independence boundary

The audit covers:

1. the exact periodic Navier--Stokes identity and zero-total-mean property;
2. the sign and size of \(B_R\), the reference characteristic, and the
   chart constants;
3. the nonautonomous Feynman--Kac representation, including reverse time
   ordering;
4. the target lower bound, positive-measure time slab, and annular geometry;
5. local Gaussian leakage for \(F,\partial_2F,\partial_3F\), including the
   periodic seam and every noncentral heat-kernel image;
6. the effective two-dimensional exterior weights after integrating the
   invariant direction and summing every periodic copy;
7. the one-sided Gaussian envelope, global \(L^2/L^3\) contraction, and the
   resulting packet moments;
8. the frozen local-pressure split and gauge even though the selected
   physical pressure is zero;
9. every \(R,A,M_m\) power in \(\mathcal E^A,\mathcal G_u^A,
   \mathcal G_p^A,\mathcal H_u^A,P_R^A\), and \((P_R^A)^{2/3}\);
10. the three limiting ratios, admissibility, finiteness, open boundary,
    and `NOT CLAY` boundary.

The audit does not cover primary-literature completeness, novelty, priority,
publication synchronization, HTML/PDF rendering, or any future finite
certificate.  Those are separate evidentiary layers.

---

## 2. Exact family, signs, and mean-zero property

The frozen parameters are

\[
 q_*=\frac12,\qquad M_m=3\,2^{m-1},\qquad q_m=M_mR,
\]

\[
 t_-=R^2,\qquad t_0=65R^2,\qquad T_R=66R^2,
\]

and

\[
 D_R=e^{-R^2}-e^{-65R^2}>0,\qquad
 B_R=\frac{q_m-q_*}{D_R}<0.
\]

Under \(M_m\ge64\) and \(q_m\le1/32\),

\[
 q_*-q_m\in[15/32,1/2],
\]

while the mean-value theorem gives

\[
 64R^2e^{-65R^2}\le D_R\le64R^2.
\]

Hence

\[
 cR^{-2}\le |B_R|\le CR^{-2}.
\]

With

\[
 q_{\rm pre}=q_*-B_R(1-e^{-R^2}),\qquad
 Q(t)=q_{\rm pre}+B_R(1-e^{-t}),
\]

direct substitution gives

\[
 Q(R^2)=q_*,\qquad Q(65R^2)=q_m,
\]

and

\[
 Q'(t)=B_Re^{-t}<0.
\]

Let \(F\) solve

\[
 \partial_tF+B_Re^{-t}\cos x_3\,\partial_2F
   =(\partial_2^2+\partial_3^2)F,
\]

with

\[
 F(0,x_2,x_3)
 =R^3\partial_2K_{R^2}^{\rm per}(x_2-q_{\rm pre})
       K_{R^2}^{\rm per}(x_3),
\]

and set

\[
 u=(AF,B_Re^{-t}\cos x_3,0),\qquad p=0.
\]

Because \(F\) is independent of \(x_1\) and the second component is
independent of \(x_2\),

\[
 \nabla\cdot u=\partial_1(AF)+\partial_2(B_Re^{-t}\cos x_3)=0.
\]

The nonlinear term is exactly

\[
 (u\cdot\nabla)u
 =(AB_Re^{-t}\cos x_3\,\partial_2F,0,0).
\]

The first component is therefore the scalar advection--diffusion equation,
and the second component obeys

\[
 \partial_t(B_Re^{-t}\cos x_3)
 =\partial_3^2(B_Re^{-t}\cos x_3).
\]

Thus the unforced periodic Navier--Stokes equation holds pointwise with
\(p=0\).  There is no hidden \(A^2\) nonlinear row.

The second component has zero spatial mean because \(\cos x_3\) does.
The initial first component has zero mean because it is an \(x_2\)
derivative.  Periodic integration of the scalar equation preserves that
mean.  Consequently

\[
 \overline u(t)=0
\]

for every time, so the Version-A subtraction and global-mean translation
are exactly the identity on this family.

**Result:** `PASS`.

---

## 3. Nonautonomous Feynman--Kac time ordering

Define

\[
 G(t,z,x)=F(t,z+Q(t),x).
\]

The chain rule and \(Q'(t)=B_Re^{-t}\) give

\[
 \partial_tG=\Delta_{z,3}G+d(t,x)\partial_zG,
 \qquad
 d(t,x)=B_Re^{-t}(1-\cos x)\le0.
\]

For a fixed terminal time \(t\), the stochastic generator at stochastic
time \(s\) must be

\[
 L_{t-s}=\Delta_{z,3}+d(t-s,x)\partial_z.
\]

Indeed, applying Itô's formula to \(G(t-s,Z_s,X_s)\) produces

\[
 -\partial_tG+\Delta G+d(t-s,X_s)\partial_zG=0.
\]

Using \(d(s,\cdot)\) instead would generally be wrong because the
nonautonomous generators need not commute.  The frozen source uses the
correct reverse ordering \(t-s\).

With

\[
 X_s^x=x+\sqrt2W_3(s)\pmod{2\pi},
\]

the accumulated displacement is

\[
 \mathfrak D_t^x
 =B_R\int_0^t e^{-(t-s)}(1-\cos X_s^x)\,ds\le0.
\]

Conditioning on the \(W_3\) path and convolving the independent
\(W_2\) endpoint yields

\[
 G(t,z,x)=R^3\mathbb E_x\!\left[
  \partial_zK_{R^2+t}^{\rm per}(z+\mathfrak D_t^x)
  K_{R^2}^{\rm per}(X_t^x)
 \right].
\]

The heat age \(R^2+t\), the sign of \(\mathfrak D\), and the argument
\(z+\mathfrak D\) are all consistent.

**Result:** `PASS`.

---

## 4. Accumulated displacement and target-weighted moment

Since \(1-\cos\le2\),

\[
 |\mathfrak D_t^x|
 \le2|B_R|(1-e^{-t}).
\]

For \(0\le t\le65R^2\), the frozen small-chart reduction gives

\[
 |B_R|(1-e^{-t})\le\frac35,
 \qquad
 -\frac65\le\mathfrak D_t^x\le0.
\]

For \(|x|\le2R\), torus Brownian motion satisfies the exact identity

\[
 \mathbb E_x(1-\cos X_s^x)=1-e^{-s}\cos x
 \le s+\frac{x^2}{2}\le CR^2.
\]

Together with \(\|K_{R^2}^{\rm per}\|_\infty\le CR^{-1}\), this gives

\[
 \begin{aligned}
 \mathbb E_x\!left[|\mathfrak D_t^x|
 K_{R^2}^{\rm per}(X_t^x)\right]
 &\le |B_R|\int_0^t
 \mathbb E_x\!\left[(1-\cos X_s^x)
 K_{R^2}^{\rm per}(X_t^x)\right]ds\\
 &\le CR^{-2}\cdot R^2\cdot(R^{-1}R^2)
 \le CR.
 \end{aligned}
\]

This estimate is weighted by the terminal heat kernel; it does not make
the false global claim that the coefficient \(d\) is uniformly small.

**Result:** `PASS`.

---

## 5. Target lower bound, essential supremum, and annular geometry

Let \(\tau=R^2+t\).  Removing the residual displacement from the
Feynman--Kac formula gives the comparison profile

\[
 R^3\partial K_\tau^{\rm per}(z)K_\tau^{\rm per}(x_3).
\]

The mean-value theorem, the bound

\[
 \|\partial^2K_\tau^{\rm per}\|_\infty\le CR^{-3}
 \quad(65R^2\le\tau\le66R^2),
\]

and the preceding weighted displacement moment imply

\[
 \left|G(t,z,x_3)
 -R^3\partial K_\tau^{\rm per}(z)K_\tau^{\rm per}(x_3)\right|
 \le CR.
\]

For fixed \(1<b_1<b_2<2\),

\[
 z/R\in[b_1,b_2],\qquad |x_3|/R\le1,
 \qquad \tau/R^2\in[65,66]
\]

is a compact dimensionless set on which the central real-Gaussian
derivative has one sign and a strictly positive absolute lower bound.
Noncentral images are \(O(e^{-c/R^2})\).  After reducing \(R_1\), one
therefore has \(|F|\ge c\) on a time slab

\[
 t_0-\varepsilon_0R^3<t<t_0
\]

and on the stated \((z,x_3)\) rectangle.

On that slab, \(|Q(t)-q_m|\le CR\).  The set

\[
 \Omega_t=\left\{
 |x_1|<\frac{q_m}{8},\quad
 b_1R<x_2-Q(t)<b_2R,\quad
 |x_3|<R
 \right\}
\]

has volume at least \(cM_mR^3\).  Since

\[
 2^mR=\frac23q_m,
 \qquad
 2^{m+1}R=\frac43q_m,
\]

and all non-\(x_1\) errors are \(O(R)=O(q_m/M_m)\), this set is contained
in \(A_m(R)\) for the frozen \(M_m\ge64\) regime.  The exact annular weight
is

\[
 \gamma_m=e^{-4^{m-1}/32}=e^{-M_m^2/288}.
\]

Consequently

\[
 \mathcal U_{\rm ext}^{\infty,A}
 \ge cA^2M_mR^2e^{-M_m^2/288}.
\]

The lower bound holds on an interval of positive measure contained in
\(I_R=(64R^2,65R^2)\), rather than only at the excluded endpoint.  Thus
the essential supremum is licensed.

**Result:** `PASS`.

---

## 6. One-sided local leakage, \(\partial_3\), and the periodic seam

On \(I_{8R}\times B_{8R}\),

\[
 z=x_2-Q(t)\le-(M_m-8)R<0.
\]

Because \(\mathfrak D\le0\),

\[
 |z+\mathfrak D_t^{x_3}|\ge|z|.
\]

The chart constants give

\[
 -\frac12-8R\le z<0,
 \qquad
 -\frac12-8R-\frac65<z+\mathfrak D_t^{x_3}<0.
\]

Since \(R\le1/2048\), both arguments remain in the central half-chart
\(( -\pi,0)\).  No Brownian path can wrap through the \(-\pi\) seam and
become spuriously closer to an adjacent periodic centre.

For \(2R^2\le\tau\le66R^2\), put

\[
 a=\frac{|z+\mathfrak D|}{R}\ge M_m-8\ge56.
\]

The first two real-line Gaussian derivative factors are a fixed polynomial
of degree at most two in \(a\), multiplied by \(e^{-a^2/264}\).  They are
decreasing in this range, and

\[
 \frac{(M_m-8)^2}{264}\ge\frac{M_m^2}{528}
 \qquad(M_m\ge64).
\]

Thus

\[
 R^2|\partial K_\tau^{\rm per}(z+\mathfrak D)|
 +R^3|\partial^2K_\tau^{\rm per}(z+\mathfrak D)|
 \le C(1+M_m)^6e^{-M_m^2/528}.
\]

Every noncentral periodic image is at an absolute positive distance.  Its
\(e^{-c/R^2}\) contribution is smaller than the displayed bound because
\(M_mR\le1/32\).  Hence the estimate does not discard periodic images.

For the transverse derivative, pathwise differentiation with respect to
the starting point is legitimate for periodic smooth functions and gives

\[
 \partial_x\mathfrak D_t^x
 =B_R\int_0^te^{-(t-s)}\sin X_s^x\,ds,
 \qquad
 |\partial_x\mathfrak D_t^x|\le C.
\]

Differentiating the representation gives the two terms

\[
 \begin{aligned}
 \partial_xG=R^3\mathbb E_x[&
 \partial^2K_\tau^{\rm per}(z+\mathfrak D)
 (\partial_x\mathfrak D)K_{R^2}^{\rm per}(X_t)\\
 &+\partial K_\tau^{\rm per}(z+\mathfrak D)
 \partial K_{R^2}^{\rm per}(X_t)].
 \end{aligned}
\]

Using \(\mathbb E K_{R^2}^{\rm per}(X_t)\le CR^{-1}\) and
\(\|\partial K_{R^2}^{\rm per}\|_\infty\le CR^{-2}\), both terms are
bounded at the required \(R^{-1}\) derivative scale.  Therefore, with

\[
 \Pi_m=(1+M_m)^{18},
\]

the frozen source correctly obtains

\[
 |F|+R|\partial_2F|+R|\partial_3F|
 \le C\Pi_m^{1/3}e^{-M_m^2/528},
\]

\[
 |F|^2+R^2|\nabla F|^2
 \le C\Pi_m^{2/3}e^{-M_m^2/264},
\]

and

\[
 |F|^3\le C\Pi_me^{-M_m^2/176}.
\]

The polynomial degrees are respectively six, twelve, and eighteen; no
power of \(\Pi_m\) is silently absorbed into itself.

**Result:** `PASS`.

---

## 7. All-copy weights and packet moments

At \(S=2R\), the lifted exterior weights satisfy

\[
 W_S(y)\le\frac{CS^4}{(|y|^2+S^2)^2},
 \qquad
 L_S(y)\le\frac{CS}{(|y|^2+S^2)^2}.
\]

Integrating the invariant \(y_1\) direction and summing all
\(n\in\mathbb Z^2\) periodic copies gives

\[
 \omega_S(x)\le
 \frac{CS^4}{(\rho(x)^2+S^2)^{3/2}},
 \qquad
 \ell_S(x)\le
 \frac{CS}{(\rho(x)^2+S^2)^{3/2}},
\]

where \(\rho(x)=\operatorname{dist}_{\mathbb T^2}(x,0)\).  The tail
lattice sum converges because \(\sum_{n\ne0}|n|^{-3}<\infty\).  Thus these
are all-annulus and all-copy estimates.

The scalar drift is divergence free in \((x_2,x_3)\), since its coefficient
is independent of \(x_2\).  Multiplication by \(|F|^{p-2}F\) gives, for
\(p=2,3\),

\[
 \|F(t)\|_{L^p(\mathbb T^2)}^p
 \le\|F(0)\|_{L^p(\mathbb T^2)}^p\le CR^2.
\]

On \(I_S=(61R^2,65R^2)\),

\[
 q_m=M_mR\le q=Q(t)\le\frac18.
\]

In the central box with \(x_2<q\), the one-sided sign and seam bounds give
the pathwise first-kernel estimate before taking expectation.  Only then is
the remaining positive endpoint factor averaged.  This yields

\[
 |F(t,x_2,x_3)|
 \le C\exp\!\left[-c\frac{(q-x_2)^2+x_3^2}{R^2}\right].
\]

This step does not incorrectly factor two correlated random quantities.

The torus is partitioned into:

1. the outside of the central box;
2. the central box with \(x_2\ge q\);
3. the one-sided central box with \(x_2<q\).

On the first two pieces, \(\rho(x)\ge cq\), so the effective weight bounds
and global \(L^2/L^3\) contraction suffice.  On the third, the one-sided
Gaussian envelope suffices.  The three pieces exhaust \(\mathbb T^2\).
The resulting moments are

\[
 \int_{\mathbb R^3}W_S(y)|\widetilde F(t,y_2,y_3)|^3\,dy
 \le\frac{CR^6}{q^3},
\]

\[
 \int_{\mathbb R^3}L_S(y)|\widetilde F(t,y_2,y_3)|^2\,dy
 \le\frac{CR^3}{q^3}.
\]

The powers agree with a packet of area \(R^2\) after the invariant
direction produces a \(q^{-3}\) marginal.

**Result:** `PASS`.

---

## 8. Frozen pressure gauge

Although the selected physical representative is \(p=0\), the frozen
local split at scale \(S=2R\) is

\[
 p_S^{\rm loc}=\mathcal R_i\mathcal R_j
 (\zeta_S\widetilde u_i\widetilde u_j),
 \qquad
 h_S=-p_S^{\rm loc},
 \qquad
 c_S=(h_S)_{B_{2S}}.
\]

Therefore \(p-c_S=-c_S\) on every pressure annulus; it would be wrong to
delete this row merely because \(p=0\).  Jensen and the whole-space
Calderón--Zygmund inequality yield

\[
 |c_S(t)|^{3/2}
 \le CS^{-3}\int_{B_{4S}}|u(t)|^3.
\]

Since \(\int_{\mathbb R^3}W_S\le CS^3\),

\[
 \mathcal G_p^A(z_0,S;1)
 \le CS^{-2}\int_{I_S}\int_{B_{4S}}|u|^3.
\]

The cutoff source includes the mixed \(AF\,b_R\) tensor entries.  They are
covered by the full \(|u|^3\) bound and

\[
 (A|F||b_R|)^{3/2}
 \le C(A^3|F|^3+|b_R|^3).
\]

Thus neither the local pressure nor its gauge is omitted.

**Result:** `PASS`.

---

## 9. Independent payment ledger

Write \(q=Q(t)\) on \(I_S\).  Since

\[
 dq=B_Re^{-t}dt<0,
\]

the positive time measure satisfies

\[
 dt=\frac{-dq}{|B_R|e^{-t}}\le CR^2(-dq).
\]

The complete recalculated ledger is:

| Quantity | background row | packet row |
|---|---:|---:|
| \(\mathcal E^A(z_0,8R)\) | \(R^{-2}\) | \(A^2R^2\Pi_m^{2/3}e^{-M_m^2/264}\) |
| \(\mathcal G_u^A(z_0,S;1)\) | \(R^{-3}\) | \(A^3R^4M_m^{-2}\) |
| \(\mathcal G_p^A(z_0,S;1)\) | \(R^{-3}\) | \(A^3R^3\Pi_me^{-M_m^2/176}\) |
| \(\mathcal H_u^A(z_0,S)\) | \(R^{-3}\) | \(A^3R^4M_m^{-7/2}\) |

The rows are obtained as follows.

### 9.1 Buffered energy

The background velocity contributes

\[
 |B_R|^2R^2\asymp R^{-2}
\]

to the normalized local \(L^2\) row.  Its \(\partial_3b_R\) dissipation
row is at most \(|B_R|^2R^6\), hence smaller.  The packet leakage, local
volume \(R^3\), time length \(R^2\), and the exterior normalization give

\[
 \mathcal E^A(z_0,8R)
 \le C\left[R^{-2}
 +A^2R^2\Pi_m^{2/3}e^{-M_m^2/264}\right].
\]

Both velocity components and all spatial derivatives are included.

### 9.2 Gaussian cubic velocity payment

The background uses

\[
 S^{-2}|I_S||B_R|^3\int W_S
 \lesssim |B_R|^3R^3\lesssim R^{-3}.
\]

For the packet,

\[
 \begin{aligned}
 S^{-2}A^3\int_{I_S}\frac{CR^6}{Q(t)^3}\,dt
 &\le CA^3R^6\int_{M_mR}^{1/8}q^{-3}\,dq\\
 &\le\frac{CA^3R^4}{M_m^2}.
 \end{aligned}
\]

### 9.3 Gauge-fixed pressure payment

The local pressure estimate is supported in \(B_{4S}=B_{8R}\).  The
background again gives \(R^{-3}\).  The cubic local leakage has volume
\(R^3\), time \(R^2\), and normalization \(R^{-2}\), giving

\[
 \mathcal G_p^A(z_0,S;1)
 \le C\left[R^{-3}
 +A^3R^3\Pi_me^{-M_m^2/176}\right].
\]

### 9.4 Algebraic harmonic payment

The all-copy algebraic moment satisfies

\[
 \Lambda_S(t)\le C\left[
 |B_R|^2+\frac{A^2R^3}{Q(t)^3}\right].
\]

After raising to \(3/2\), multiplying by \(S\), and using the positive
\(R^2(-dq)\) time measure,

\[
 \begin{aligned}
 \mathcal H_u^A(z_0,S)
 &\le CR^{-3}
 +CA^3R^{15/2}\int_{M_mR}^{1/8}q^{-9/2}\,dq\\
 &\le CR^{-3}+\frac{CA^3R^4}{M_m^{7/2}}.
 \end{aligned}
\]

The \(M_m^{-7/2}\) row is smaller than the cubic velocity
\(M_m^{-2}\) row.

**Result:** `PASS`.

---

## 10. The simultaneous denominator and its \(2/3\)-power

Raising the energy estimate to \(3/2\) converts the packet leakage into

\[
 A^3R^3\Pi_me^{-M_m^2/176}.
\]

Combining every row gives

\[
 P_R^A\le C\left[
 R^{-3}
 +A^3R^3\Pi_me^{-M_m^2/176}
 +\frac{A^3R^4}{M_m^2}
 \right].
\]

Using concavity/subadditivity for the \(2/3\)-power yields the slightly
relaxed but valid bound

\[
 (P_R^A)^{2/3}\le C\left[
 R^{-2}
 +A^2R^2\Pi_me^{-M_m^2/264}
 +A^2R^{8/3}M_m^{-4/3}
 \right].
\]

The direct \(2/3\)-power of \(\Pi_m\) is no larger than the displayed
\(\Pi_m\), and

\[
 \frac23\cdot\frac1{176}=\frac1{264}.
\]

No cubic payment row is compared with the quadratic target before taking
the required \(2/3\)-power.

**Result:** `PASS`.

---

## 11. Explicit sequence and three independent ratios

Take

\[
 R_m=e^{-M_m^2/96},\qquad
 \mathfrak a_m=R_m^{-2}e^{M_m^2/576},
 \qquad M_m=3\,2^{m-1}\to\infty.
\]

The target lower bound becomes

\[
 L_m=c\mathfrak a_m^2M_mR_m^2e^{-M_m^2/288}
 =cM_mR_m^{-2}.
\]

Against the background row,

\[
 \frac{L_m}{R_m^{-2}}=cM_m\to\infty.
\]

Against the local Gaussian leakage row,

\[
 \frac{L_m}
 {\mathfrak a_m^2R_m^2\Pi_me^{-M_m^2/264}}
 =\frac{cM_m}{\Pi_m}
 e^{M_m^2(1/264-1/288)}\to\infty,
\]

because

\[
 \frac1{264}-\frac1{288}=\frac1{3168}>0
\]

and \(\Pi_m=(1+M_m)^{18}\) is polynomial.

Against the exterior cubic row,

\[
 \begin{aligned}
 \frac{L_m}
 {\mathfrak a_m^2R_m^{8/3}M_m^{-4/3}}
 &=cM_m^{7/3}R_m^{-2/3}e^{-M_m^2/288}\\
 &=cM_m^{7/3}e^{M_m^2/288}\to\infty.
 \end{aligned}
\]

Thus every row in the simultaneous denominator is asymptotically smaller
than the target, and

\[
 \frac{X_{R_m}^A}{(P_{R_m}^A)^{2/3}}\to\infty.
\]

**Result:** `PASS`.

---

## 12. Quantifiers and finiteness

Along the explicit sequence,

\[
 R_m\to0,\qquad M_mR_m\to0.
\]

Therefore, for all sufficiently large \(m\),

\[
 R_m<\pi/16,\qquad M_m\ge64,
 \qquad M_mR_m\le1/32.
\]

All small-chart, seam, and large-\(M_m\) hypotheses hold simultaneously.
For every fixed \(m\), \(R_m>0\), \(\mathfrak a_m<\infty\), and the exact
parabolic solution is analytic on the required compact interval.  Every
positive-scale observable is finite.  No uniform global-energy bound across
the sequence is assumed by the rejected endpoint.

The construction is an analytic sequence of exact solutions, not a finite
sampling, DNS, Galerkin truncation, or numerical extrapolation.

**Result:** `PASS`.

---

## 13. Open boundary and `NOT CLAY`

The proved statement concerns only the frozen Version-A annular ledger,
which subtracts the constant global mean and translates by that constant
mean.  It does not decide:

1. a cylinder following a local or mollified velocity;
2. subtraction of a scale-dependent local spatial mean;
3. a fixed-centre estimate retaining a signed entrance-flux payment;
4. the optimal large-payment exponent of a transport-aware repair;
5. compact-cutoff absorption, epsilon regularity, continuation, or a
   zero-scale limit.

The witness lies in a classical globally smooth 2D3C invariant subspace.
The theorem proves no singularity, blow-up, epsilon-regularity criterion,
global regularity theorem, or breakdown result for general three-dimensional
Navier--Stokes solutions.  It is not a solution or partial solution of the
Clay Millennium problem.

**Result:** `PASS / OPEN boundary preserved / NOT CLAY`.

---

## 14. Final audit ledger

| Audit item | Status |
|---|---|
| Frozen commit, blob, and SHA-256 provenance | `PASS` |
| Exact smooth periodic NSE identity | `PASS` |
| Zero total spatial mean and Version-A identity | `PASS` |
| \(B_R<0\), \(|B_R|\asymp R^{-2}\), characteristic endpoints | `PASS` |
| Nonautonomous reverse time ordering \(t-s\) | `PASS` |
| Accumulated-displacement sign and weighted \(O(R)\) moment | `PASS` |
| Target heat-kernel lower bound | `PASS` |
| Positive-measure slab and essential supremum | `PASS` |
| Annular geometry and exponent \(-M_m^2/288\) | `PASS` |
| One-sided leakage exponent \(-M_m^2/528\) | `PASS` |
| \(\partial_2F\) and \(\partial_3F\) bounds | `PASS` |
| Central chart and periodic seam | `PASS` |
| Every noncentral heat-kernel image | `PASS` |
| Effective weights and every lifted periodic copy | `PASS` |
| Global \(L^2/L^3\) contraction | `PASS` |
| One-sided Gaussian plus contraction partition | `PASS` |
| Frozen local-pressure gauge with \(p=0\) | `PASS` |
| Background and packet energy rows | `PASS` |
| \(\mathcal G_u^A\) powers | `PASS` |
| \(\mathcal G_p^A\) powers | `PASS` |
| \(\mathcal H_u^A\) powers | `PASS` |
| Simultaneous \(P_R^A\) ledger | `PASS` |
| \((P_R^A)^{2/3}\) ledger | `PASS` |
| Background ratio | `PASS` |
| Local-leakage ratio | `PASS` |
| Exterior-cubic ratio | `PASS` |
| Admissibility and per-member finiteness | `PASS` |
| Open-claim boundary | `PASS` |
| `NOT CLAY` boundary | `PASS` |
| Separation from future finite-certificate layer | `PASS` |

**Overall independent analytic verdict:** `PASS`.
