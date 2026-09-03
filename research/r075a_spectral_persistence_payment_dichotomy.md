# R0.75A -- local persistence/payment dichotomy and its spectral ledger

## 0. Result and exact boundary

R0.74Z, \((Z.39)\), asked whether a finite common-shear passive correction
could preserve the outer packet's W-type remote endpoint, destroy that
remote field on an arbitrarily short backward time scale, and thereby
avoid the exterior cubic payment.  For the exact smooth common-shear
family, the answer is **no at the scale of that remote kinetic witness**.

The decisive estimate is local and does not require a spectral
observability theorem.  A cutoff moving with the packet satisfies an exact
energy identity.  On a backward interval of length \(cR^3\), either its
localized \(L^2\) energy remains at least half of its endpoint value, or
the increase back to the endpoint forces an \(R^3\)-normalized amount of
spacetime \(L^2\) mass in the enlarged remote strip.  In both cases,
spacetime Hölder and the scale-\(2R\) exterior weight give

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge c\,h_{\rm rem}
 R^{2/3}\omega^{-5/6}L^{-1/6}.}
 \tag{A.1}
\]

Here

\[
 \omega=\gamma_{k_2-1}=\Gamma^{1/4},
 \qquad
 h_{\rm rem}
 =\frac{\omega}{2R}
   \int_{\Omega_0(t_2)}|F(t_2,x)|^2\,dx
 \tag{A.2}
\]

is the kinetic mass of the **total passive first component** on a fixed
core of the W remote strip.  For the frozen R0.74Y parameters,

\[
 \liminf_{L\to\infty}\frac1{L^2}
 \log\frac{(P_R^M)^{2/3}}{h_{\rm rem}}
 \ge
 \frac5{24}c_\gamma-\frac\rho6
 =\frac{64279}{238140000}>0.
 \tag{A.3}
\]

Thus (A.1) includes persistent, critical, and arbitrarily shorter smooth
endpoint focusing.  It is uniform in the number and conditioning of a
finite correction family.  It uses the total field, so local cancellation,
inversion partners, and all periodic windings are already included.

The requested \(x_2\)-Fourier analysis remains useful as a separate exact
ledger.  Every horizontal mode obeys an exact energy identity and high
horizontal modes decay forward.  A horizontal band alone, however, gives
neither a vertical generator bound nor local observability.  In
particular, backward growth of one heat mode is not a short-persistence
example: an escape would require cancellation of the **total field** on
the earlier moving strip.  The local theorem above charges that
cancellation without converting global modal energy into local payment.

The precise status is

\[
\boxed{
\begin{gathered}
\textbf{W-REMOTE ENDPOINT PERSISTENCE/PAYMENT DICHOTOMY: PROVED}\\
\textbf{FOR THE EXACT SMOOTH COMMON-SHEAR FAMILY;}\\
\textbf{HORIZONTAL MODAL ENERGY AND FORWARD DECAY: EXACT;}\\
\textbf{NO FREQUENCY/GEOMETRY-UNIFORM LOCAL OBSERVABILITY CONSTANT;}\\
\textbf{COMPLETE }K\textbf{, FIXED DELETION, AND REGULARITY: OPEN.}
\end{gathered}}
\tag{A.4}
\]

No strip lower bound is used as a whole-shell upper bound.  No statement
is made about arbitrary suitable weak solutions.  This is not a
regularity or singularity theorem.  \(\mathbf{NOT\ CLAY}\).

<!-- R075A_LOCAL_MOVING_CUTOFF_IDENTITY -->
<!-- R075A_ENDPOINT_PAYMENT_DICHOTOMY -->
<!-- R075A_EXACT_HORIZONTAL_MODAL_ENERGY -->
<!-- R075A_GLOBAL_LOCAL_OBSERVABILITY_BOUNDARY -->
<!-- R075A_COMPLETE_CLOCK_OPEN -->
<!-- R075A_NOT_CLAY -->

## 1. Frozen sources, equation, and remote geometry

The note is bound to the following local snapshots.

| source | SHA-256 | use |
|---|---|---|
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` | Version-M payment and completed clock |
| `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` | exact finite same-shear superposition |
| `research/r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` | plateau and shear-size bounds |
| `research/r074w_remote_adjacent_inward_comparison.md` | `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10` | all-winding W remote comparator and strip geometry |
| `research/r074z_cancellation_cell_gate.md` | `bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a` | endpoint dichotomy and shell-tube payment |

Let the total first component of any finite exact correction family solve

\[
 (\partial_t+b(t,x_3)\partial_2-\Delta_{23})F=0,
 \qquad
 u=(F,b,0),
 \tag{A.5}
\]

where \(b=B\theta_R\), \(|\theta_R|\le1\), and all summands use this same
shear from time zero.  Then \(u\) is an exact smooth periodic unforced
Navier--Stokes solution with pressure zero.  No probabilistic statement is
used below.

Retain

\[
 \lambda=\frac{63}{32},\qquad
 p=\lambda^{-1}=\frac{32}{63},\qquad L=L_2,\qquad
 k=k_2-1,\qquad
 \Gamma=\gamma_{k_2},\qquad
 \omega=\gamma_k=\Gamma^{1/4}.
\tag{A.6}
\]

The reciprocal is essential: \(pL=2^{k_2}\).  The value
\(63/32\) is \(\lambda\), not the W radial coefficient \(p\).

At the re-centring time \(t_2=\tau_2\), \(Q_2(t_2)=0\), and

\[
 Q_2'(t)=b(t,h_2)=B\theta_R(t,h_2).
 \tag{A.7}
\]

The R0.74U bound \(1-\varepsilon_1>3/4\) gives

\[
 \frac1{128R^2}\le B
 \le\frac1{128(1-\varepsilon_1)R^2}
 \le\frac1{96R^2}.
 \tag{A.8}
\]

Put \(z=x_2-Q_2(t)\).  The W moving strip is

\[
\begin{aligned}
 \mathcal S_+(t):=\biggl\{x:\;&
 |x_1|<\frac14\sqrt{pL}\,R,\quad
 \frac54R<z<\frac32R,\\
 &pLR-R<x_3<pLR-\frac12R\biggr\}.
\end{aligned}
\tag{A.9}
\]

Choose the fixed inner core

\[
\begin{aligned}
 \Omega_0(t):=\biggl\{x:\;&
 |x_1|<\frac3{16}\sqrt{pL}\,R,\quad
 \frac{21}{16}R<z<\frac{23}{16}R,\\
 &pLR-\frac{15}{16}R<x_3
 <pLR-\frac9{16}R\biggr\}.
\end{aligned}
\tag{A.10}
\]

Thus \(\overline{\Omega_0(t)}\) has fixed normalized distance from the
boundary of \(\mathcal S_+(t)\).  R0.74Z, (Z.12a)--(Z.12b), gives an
absolute \(c_0>0\), independent of \(L,R\), such that

\[
 J=[t_2-c_0R^3,t_2]\subset I_{2R},
 \qquad
 \mathcal S_+(t)\subset A_k(R)=A_{k-1}(2R)
 \quad(t\in J),
 \tag{A.11}
\]

after decreasing \(c_0\) once.  Moreover,

\[
 |\mathcal S_+(t)|
 =\frac1{16}\sqrt{pL}\,R^3.
 \tag{A.12}
\]

For completeness, at \(t=t_2\) the worst outer corner obeys

\[
 \frac{|x|^2}{R^2}
 \le \frac{pL}{16}+\frac94+\left(pL-\frac12\right)^2
 =(pL)^2-\frac{15}{16}pL+\frac52
 <(pL)^2,
 \tag{A.12a}
\]

whereas \(x_3>pLR-R>pLR/2\).  These are respectively the outer
and inner radii of \(A_k(R)\).  For earlier \(t\in J\),
\(Q_2(t)\le0\) and \(|Q_2(t)|\le c_0R/96\); after fixing \(c_0\)
small, \(x_2=z+Q_2(t)\) stays positive and its square only decreases.
This verifies the shell margin directly with \(p=32/63\).  All face
gaps between (A.10) and (A.9) are strict; in particular,
\(-15/16>-1\) and \(-9/16<-1/2\) in the normalized \(x_3-pLR\)
coordinate.

On that physical shell the exact shifted scale-\(2R\) weight is

\[
 W_{2R}\ge\gamma_{k-1}
 =\omega^{1/4}=\Gamma^{1/16}.
 \tag{A.13}
\]

The nested core is only a convenient explicit choice.  Any pair of moving
sets with the same \(R\)-scale cutoff bounds, shell inclusion, and
\(O(L^{1/2}R^3)\) outer volume gives the same theorem.

## 2. Exact moving-cutoff local energy identity

Define the moving-frame total field

\[
 \widetilde F(t,z,x_3):=F(t,z+Q_2(t),x_3).
 \tag{A.14}
\]

It solves

\[
 \partial_t\widetilde F
 =\Delta_{z3}\widetilde F
 -c(t,x_3)\partial_z\widetilde F,
 \qquad
 c(t,x_3):=b(t,x_3)-Q_2'(t).
 \tag{A.15}
\]

Choose a smooth periodic \(0\le\phi\le1\), fixed in the
\((x_1,z,x_3)\) frame, which equals one on the set in (A.10) and is
supported in the set in (A.9).  It may be chosen so that

\[
 |\partial_z\phi|\le C_\phi R^{-1},
 \qquad
 |\Delta_{z3}\phi|\le C_\phi R^{-2}.
 \tag{A.16}
\]

The \(x_1\) cutoff causes no derivative error because \(F\) is independent
of \(x_1\) and (A.5) has only the \((x_2,x_3)\) passive operator.  Put

\[
 E(t):=\int_{\mathbb T^3}\phi(x_1,z,x_3)
             |\widetilde F(t,z,x_3)|^2\,dx_1\,dz\,dx_3.
 \tag{A.17}
\]

Multiplying (A.15) by \(\phi\widetilde F\), integrating on the torus, and
integrating by parts gives the exact identity

\[
 \boxed{
 \frac12E'(t)
 +\int_{\mathbb T^3}\phi|\nabla_{z3}\widetilde F|^2
 =\frac12\int_{\mathbb T^3}
 \bigl[c\,\partial_z\phi+\Delta_{z3}\phi\bigr]
 |\widetilde F|^2.}
 \tag{A.18}
\]

The sign of the transport term is plus on the right: indeed,

\[
 -\int\phi c\widetilde F\,\partial_z\widetilde F
 =\frac12\int c\,\partial_z\phi\,|\widetilde F|^2,
 \tag{A.19}
\]

because \(c\) is independent of \(z\).

The maximum principle, (A.7), and (A.8) imply the deliberately crude but
uniform bound

\[
 |c(t,x_3)|
 =B|\theta_R(t,x_3)-\theta_R(t,h_2)|
 \le2B\le\frac1{48R^2}.
 \tag{A.20}
\]

Consequently, for \(R\le1\), there is an absolute \(K_\phi<\infty\) such
that

\[
 \bigl|c\,\partial_z\phi+\Delta_{z3}\phi\bigr|
 \le K_\phi R^{-3}\mathbf 1_{\mathcal S_+},
 \tag{A.21}
\]

where \(\mathcal S_+\) is written in moving coordinates.  Dropping the
nonnegative gradient term in (A.18) therefore gives

\[
 E'(t)\le K_\phi R^{-3}M(t),
 \qquad
 M(t):=\int_{\mathcal S_+(t)}|F(t,x)|^2\,dx.
 \tag{A.22}
\]

No plateau-deficit estimate is needed: the crude \(R^{-3}\) error is
already exactly compatible with the \(R^3\) time window.

This is a moving-drift, anisotropic version of the standard nested-cutoff
local heat estimate; compare the inner-ball/outer-ball argument of
Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2.  The present
calculation is retained because the residual shear, moving periodic strip,
and subsequent Version-M weighted cubic payment are not covered by that
pure-heat result.

## 3. Endpoint persistence/payment dichotomy

Set

\[
 E_*:=E(t_2),
 \qquad
 X:=\int_JM(t)\,dt.
 \tag{A.23}
\]

There are two exhaustive cases.

* If \(E(t)\ge E_*/2\) for every \(t\in J\), then

  \[
   X\ge\int_JE(t)\,dt
   \ge\frac{c_0}{2}E_*R^3.
   \tag{A.24}
  \]

* Otherwise, there is \(t_0\in J\) with \(E(t_0)<E_*/2\).  Integrating
  (A.22) from \(t_0\) to \(t_2\) gives

  \[
   \frac12E_*
   <E(t_2)-E(t_0)
   \le K_\phi R^{-3}
       \int_{t_0}^{t_2}M(t)\,dt
   \le K_\phi R^{-3}X.
   \tag{A.25}
  \]

In either case,

\[
 \boxed{X\ge c_1E_*R^3,\qquad
 c_1:=\min\{c_0/2,(2K_\phi)^{-1}\}>0.}
 \tag{A.26}
\]

This is the exact persistence/focusing dichotomy.  The first case is a
literal local kinetic floor.  The second says that an arbitrarily sharp
rise to the endpoint cannot occur without a fixed amount of spacetime
\(L^2\) mass on the enlarged remote strip.  It applies to the total field,
not to a selected summand.

The spacetime support in (A.23) has volume at most

\[
 |J|\sup_{t\in J}|\mathcal S_+(t)|
 \le C L^{1/2}R^6.
 \tag{A.27}
\]

Spacetime Hölder, (A.26), and \(|u|\ge|F|\) yield

\[
\begin{aligned}
 \int_J\int_{\mathcal S_+(t)}|u|^3
 &\ge
 \frac{X^{3/2}}
 {\bigl(|J|\sup_t|\mathcal S_+(t)|\bigr)^{1/2}}\\
 &\ge cE_*^{3/2}R^{3/2}L^{-1/4}.
\end{aligned}
\tag{A.28}
\]

By (A.11)--(A.13), the nonnegative exterior velocity row of the Version-M
payment gives

\[
\begin{aligned}
 P_R^M
 &\ge (2R)^{-2}\omega^{1/4}
 \int_J\int_{\mathcal S_+(t)}|u|^3\\
 &\ge c\omega^{1/4}E_*^{3/2}R^{-1/2}L^{-1/4}.
\end{aligned}
\tag{A.29}
\]

Since \(\phi=1\) on the endpoint core,

\[
 E_*\ge\int_{\Omega_0(t_2)}|F(t_2,x)|^2\,dx
 =\frac{2R}{\omega}h_{\rm rem}.
 \tag{A.30}
\]

Because \(\Psi_k^R=1\) on the W strip, \(h_{\rm rem}\) is a genuine
nonnegative sub-witness of the original-scale shell endpoint kinetic row;
it is not a whole-shell upper bound.

Substitution in (A.29) proves

\[
 \boxed{
 P_R^M
 \ge c h_{\rm rem}^{3/2}
 R\,\omega^{-5/4}L^{-1/4},}
 \tag{A.31}
\]

and taking the two-thirds power proves (A.1).

### Theorem 3.1 -- arbitrary smooth endpoint focusing pays

Let a finite inversion-paired primary/corrector family be re-evolved from
time zero under one common shear and suppose that its total first
component has \(h_{\rm rem}>0\) on the endpoint core (A.10).  Then
(A.1) holds with constants independent of the family size, coefficients,
spectral bandwidth, and temporal condition number.

This theorem is deterministic.  It retains every periodic winding because
it is applied directly to the exact periodic total solution.  It needs no
separate survival estimate after the endpoint lower bound in (A.2) has
been supplied.

## 4. Exact frozen exponent and what it closes

For R0.74Y--Z,

\[
 c_\gamma=\frac8{3969},\qquad
 \frac{\log(1/R)}{L^2}=\frac\rho4=\frac9{40000},
 \qquad
 \omega=e^{-(c_\gamma/4)L^2}.
 \tag{A.32}
\]

Taking logarithms in (A.1) gives

\[
 \liminf_{L\to\infty}\frac1{L^2}
 \log\frac{(P_R^M)^{2/3}}{h_{\rm rem}}
 \ge\frac5{24}c_\gamma-\frac\rho6.
 \tag{A.33}
\]

The exact arithmetic is

\[
 \frac5{24}\frac8{3969}-\frac1{6}\frac9{10000}
 =\frac{64279}{238140000}>0.
 \tag{A.34}
\]

This is the same positive gap as Z.1.  Unlike Z.19a, no lower bound on a
persistence fraction \(\theta_L\) remains.  The drop alternative
(A.25)--(A.28) covers the equality layer
\(\theta_L=e^{-(\kappa_*+o(1))L^2}\) and all shorter smooth focusing.
Thus Z.39 is proved for the W remote kinetic witness in the exact family.

Two boundaries are essential.

1. The theorem lower-bounds payment in terms of the chosen local witness
   \(h_{\rm rem}\).  It does **not** upper-bound the full completed clock
   \(K_{k,R}(t_2)\) by that strip witness.
2. A larger accumulated-dissipation or other completed-clock row could
   have a different scale.  Therefore (A.1) alone neither proves a
   fixed-deletion bound nor refutes the frozen fixed-deletion theorem.

## 5. Exact \(x_2\)-Fourier ledger

Write

\[
 F(t,x_2,x_3)
 =\sum_{n\in\mathbb Z}f_n(t,x_3)e^{inx_2},
 \qquad
 f_n(t,x_3)=\frac1{2\pi}\int_{-\pi}^{\pi}
 F(t,x_2,x_3)e^{-inx_2}\,dx_2.
 \tag{A.35}
\]

Since \(b\) is independent of \(x_2\), the modes do not couple and

\[
 \partial_tf_n-\partial_3^2f_n
 +(n^2+inb(t,x_3))f_n=0.
 \tag{A.36}
\]

Taking the real part of the \(L^2(\mathbb T_{x_3})\) inner product with
\(f_n\) gives

\[
 \boxed{
 \frac12\frac d{dt}\|f_n(t)\|_2^2
 +\|\partial_3f_n(t)\|_2^2
 +n^2\|f_n(t)\|_2^2=0.}
 \tag{A.37}
\]

The shear term vanishes because

\[
 \operatorname {Re}\int_{\mathbb T}inb(t,x_3)|f_n|^2\,dx_3=0.
 \tag{A.38}
\]

For \(0\le s\le t\), integration yields

\[
\begin{aligned}
 \|f_n(t)\|_2^2
 &+2\int_s^t\|\partial_3f_n(r)\|_2^2\,dr
 +2n^2\int_s^t\|f_n(r)\|_2^2\,dr\\
 &=\|f_n(s)\|_2^2.
\end{aligned}
\tag{A.39}
\]

Hence

\[
 \|f_n(t)\|_2\le e^{-n^2(t-s)}\|f_n(s)\|_2.
 \tag{A.40}
\]

If \(\Pi_{\ge N}^{(2)}\) is the horizontal projection onto
\(\{|n|\ge N\}\), Parseval gives

\[
 \boxed{
 \|\Pi_{\ge N}^{(2)}F(t)\|_2
 \le e^{-N^2(t-s)}
 \|\Pi_{\ge N}^{(2)}F(s)\|_2.}
 \tag{A.41}
\]

Equivalently,

\[
 \|\Pi_{\ge N}^{(2)}F(s)\|_2
 \ge e^{N^2(t-s)}
 \|\Pi_{\ge N}^{(2)}F(t)\|_2.
 \tag{A.42}
\]

Equations (A.36)--(A.42) are global identities for the total periodic
field.  A single mode normalized at the endpoint is larger backward and
therefore does **not** refute backward kinetic-floor persistence.  To make
the earlier local remote field small, other pieces must cancel or
transport the total field on that strip.  Such pieces remain orthogonal to
the selected mode globally, so (A.42) by itself is not local payment.

## 6. What a band and a generator bound do -- and do not do

The invariant horizontal band

\[
 \mathcal H_N
 :=\{F:\widehat F(n,x_3)=0\text{ for }|n|>N\}
 \tag{A.43}
\]

does not control vertical frequency.  Indeed,

\[
 F_m(t,x_3)=e^{-m^2t}\sin(mx_3)
 \tag{A.44}
\]

lies in the horizontal zero mode and solves (A.5) for every shear, while

\[
 \frac{\|\partial_tF_m(t)\|_2}{\|F_m(t)\|_2}=m^2\to\infty.
 \tag{A.45}
\]

Thus no full generator bound follows from an \(x_2\) band alone.

For completeness, suppose on a backward interval that

\[
 \|\partial_t\widetilde F(t)\|_{L^2(\mathbb T^3)}
 \le\Lambda\|\widetilde F(t)\|_{L^2(\mathbb T^3)}.
 \tag{A.46}
\]

For any fixed positive-measure remote core \(\Omega\), set

\[
 A_*:=\|\widetilde F(t_*)\|_{L^2(\Omega)}>0,
 \qquad
 \mathcal O_*:=
 \frac{\|\widetilde F(t_*)\|_{L^2(\mathbb T^3)}}{A_*}\ge1.
 \tag{A.47}
\]

Then the endpoint local norm remains at least \(A_*/2\) for

\[
 0\le t_*-t\le
 \delta_{\rm sp}:=
 \Lambda^{-1}\log\left(1+\frac1{2\mathcal O_*}\right),
 \tag{A.48}
\]

with the usual \(+\infty\) convention when \(\Lambda=0\).  Indeed,

\[
\begin{aligned}
 \|\widetilde F(t)-\widetilde F(t_*)\|_2
 &\le\int_t^{t_*}\|\partial_s\widetilde F(s)\|_2\,ds\\
 &\le(e^{\Lambda(t_*-t)}-1)
       \|\widetilde F(t_*)\|_2.
\end{aligned}
\tag{A.49}
\]

The loss \(\mathcal O_*\) is indispensable: a global generator estimate is
not a local observability estimate.

One restrictive sufficient condition for (A.46) is

\[
 \Pi_{|n|>N}^{(2)}\widetilde F=0,
 \qquad
 \|\partial_3^2\widetilde F\|_2
 \le M^2\|\widetilde F\|_2.
 \tag{A.50}
\]

Writing

\[
 B_Q:=\sup_{t,x_3}|b(t,x_3)-Q_2'(t)|,
 \tag{A.51}
\]

equation (A.15) gives the admissible choice

\[
 \boxed{\Lambda_{\rm band}:=N^2+M^2+B_QN.}
 \tag{A.52}
\]

The horizontal band is invariant.  The vertical graph bound in (A.50) is
an additional hypothesis, not a consequence of initial vertical banding,
because multiplication by \(b(t,x_3)\) couples vertical modes.

If the endpoint belongs to the rectangular trigonometric space

\[
 \mathcal B_{N,M}
 =\operatorname {span}\{e^{i(nx_2+mx_3)}:
 |n|\le N,\ |m|\le M\},
 \tag{A.53}
\]

the exact observation constant is

\[
 \mathfrak B_\Omega(N,M)
 :=\sup_{0\ne f\in\mathcal B_{N,M}}
 \frac{\|f\|_{L^2(\mathbb T^3)}}
      {\|f\|_{L^2(\Omega)}}<\infty.
 \tag{A.54}
\]

Finiteness follows from analyticity and compactness in this
finite-dimensional space.  It need not be favorable.  On an \(R\)-width
\(x_2\) interval, the polynomial

\[
 p_N(x_2)=(e^{ix_2}-1)^N
 \tag{A.55}
\]

has degree \(N\), is at most \(R^N\) near zero, and is at least \(c^N\)
on a fixed separated interval.  Consequently, up to fixed and polynomial
factors,

\[
 \mathfrak B_\Omega(N,M)\gtrsim(c/R)^N.
 \tag{A.56}
\]

This explains why generic spectral observability cannot be silently
inserted into a local payment proof.  The moving-cutoff theorem avoids it.

## 7. Short-time focusing, global energy, and local payment

Suppose a high horizontal component satisfies

\[
 \|\Pi_{\ge N}^{(2)}F(t_*)\|_2\ge\eta_NA_*,
 \qquad \tau=t_*-s>0.
 \tag{A.57}
\]

Then (A.42) gives the exact early global-energy cost

\[
 \boxed{
 \|\Pi_{\ge N}^{(2)}F(s)\|_2^2
 \ge e^{2N^2\tau}\eta_N^2A_*^2.}
 \tag{A.58}
\]

If \(N^2\theta R^3\gtrsim1\), a backward interval of length \(cR^2\)
produces the amplification factor

\[
 \exp\!\left(\frac{c'}{\theta R}\right).
 \tag{A.59}
\]

At a critical exponential \(\theta\), this can be double exponential in
\(L^2\).  It still does not imply a central or exterior payment: (A.58) is
global, and a local observation constant could be equally bad.

What is exact without observability is the total-field statement.  If the
earlier moving-core norm is less than half the endpoint norm, then

\[
 \int_s^{t_*}\|\partial_t\widetilde F(t)\|_2\,dt
 \ge\frac12A_*.
 \tag{A.60}
\]

More strongly, when the endpoint core and enlarged strip are those of
Section 1, the local identity upgrades this mere global variation to

\[
 \int_J\int_{\mathcal S_+(t)}|F|^2
 \ge cE_*R^3,
 \tag{A.61}
\]

and therefore to the actual exterior Version-M payment (A.29).  This is
why total-field cancellation at the earlier moving strip, rather than
scalar decay or growth of one mode, is the relevant short-persistence
mechanism.

Pointwise endpoint data alone still require a spatial thickness estimate.
For example, if

\[
 |F(t_*,x_*)|=A_\infty,
 \qquad
 \|\nabla F(t_*)\|_\infty\le\mathcal B_\infty A_\infty,
 \tag{A.62}
\]

then \(|F|\ge A_\infty/2\) on a ball of radius
\((2\mathcal B_\infty)^{-1}\).  Without such a Bernstein/doubling input, a
point value cannot be relabeled as the positive-volume endpoint witness
in (A.2).

## 8. Status ledger and minimum next proposition

| statement | status |
|---|---|
| moving-frame identity (A.18) and crude cutoff bound (A.21) | **EXACT** |
| local spacetime dichotomy (A.26) | **EXACT THEOREM** |
| exterior payment bounds (A.29)--(A.31) | **EXACT THEOREM** for the frozen smooth family |
| critical and shorter endpoint focusing evade the W kinetic payment | **FALSE** in this exact family |
| horizontal mode equation, energy identity, and decay | **EXACT** |
| a single backward-growing mode is a short-persistence counterexample | **FALSE** |
| horizontal band alone controls the full generator | **FALSE** |
| global high-mode energy is automatically local payment | **FALSE** |
| arbitrary ill-conditioned finite families evade (A.31) | **FALSE** while they preserve the stated endpoint core |
| the full completed clock is bounded above by the W strip witness | **OPEN** |
| a fixed-deletion theorem follows from (A.31) | **NOT PROVED** |
| a statement for arbitrary suitable weak solutions follows | **NOT PROVED** |

The next proposition is no longer a spectral persistence estimate.  It is
a completed-clock extraction theorem at the remote coordinate:

\[
\boxed{
\begin{gathered}
\textbf{Remote complete-clock extraction.}\\
\text{Control every endpoint and accumulated row of }K_{k,R}(t_2)
\text{ by the local}\\
\text{W kinetic witness plus quantities already dominated by }
(P_R^M)^{2/3},\\
\text{without using a strip lower bound as a whole-shell upper bound.}
\end{gathered}}
\tag{A.63}
\]

Alternatively, a future counterexample route must abandon this W-type
endpoint kinetic coordinate and exhibit a genuinely different completed-
clock row.  Until (A.63) or such a new witness is proved, the complete
\(K\), simultaneous two-coordinate fixed-deletion claim, and all
regularity consequences remain open.  \(\mathbf{NOT\ CLAY}\).
