# R0.74Q, Step 1 — the common-shear multipacket gate

## 0. Status and claim boundary

R0.74Q asks whether many physical-shell clocks can be large at one terminal
time while the square-function clock and the complete local payment remain
sublinear in the number of active shells.  This note performs the first exact
test on the R0.74F--O passive-packet family.

Five statements are proved here.

1. Any finite number of inversion-paired passive packets can be re-evolved
   under one common heat shear to give an exact smooth periodic
   Navier--Stokes solution with zero physical pressure.
2. Previously constructed packets with different shears cannot simply be
   added; the common-shear re-evolution is essential.
3. The frozen R0.74F terminal-angle geometry cannot be transplanted to two
   distinct dyadic physical shells with one common shear calibration along
   an asymptotic sequence that retains the inner-packet survival reserve.
4. For two common-shear packets, every quadratic shell-flux and clock cross
   term can be written exactly.  Their vanishing would still not make the
   complete payment additive because the central and harmonic rows contain
   an outer \(3/2\) power.
5. The inherited inner survival closure and outer amplified cubic-majorant
   closure have disjoint exponent windows at adjacent dyadic shells.  A
   genuine cubic no-go follows only under an explicit outer-lobe
   no-cancellation hypothesis.

The third statement is an asymptotic obstruction for a specified frozen
geometry.  It is not an impossibility theorem for every common-shear packet
family.  In particular, terminal angle, entrance point, reference path, or
shear profile may be changed, but all survival, annular, and payment estimates
would then have to be proved again.  This note does not decide the fixed-scale
inequality (Q.1), regularity, blow-up, or the Millennium problem.
**NOT CLAY.**

No simulation or numerical fit is used.

## 1. Exact finite-\(N\) common-shear family

Work on \(\mathbb T^3=(-\pi,\pi]^3\).  Let \(\theta_0\) be a smooth odd
periodic function of \(x_3\), and set

\[
 \theta(t,x_3)=e^{t\partial_3^2}\theta_0(x_3),
 \qquad b(t,x_3)=B\theta(t,x_3),
 \qquad B\in\mathbb R.
\tag{Q.28}
\]

Fix a finite integer \(N\).  For each \(1\le\ell\le N\), choose a packet
width \(\varepsilon_\ell>0\), a height \(h_\ell\), and a horizontal entrance
point \(q_{{\rm pre},\ell}\).  With \(K_t=K_t^{\rm per}\), define

\[
\begin{aligned}
 G_{\ell,0}^+(x_2,x_3)
 &=\varepsilon_\ell^3
   \partial_2K_{\varepsilon_\ell^2}
       (x_2-q_{{\rm pre},\ell})
   K_{\varepsilon_\ell^2}(x_3-h_\ell),\\
 G_{\ell,0}^-(x_2,x_3)
 &=\varepsilon_\ell^3
   \partial_2K_{\varepsilon_\ell^2}
       (x_2+q_{{\rm pre},\ell})
   K_{\varepsilon_\ell^2}(x_3+h_\ell).
\end{aligned}
\tag{Q.29}
\]

Then

\[
 G_{\ell,0}^-(x_2,x_3)
 =-G_{\ell,0}^+(-x_2,-x_3).
\tag{Q.30}
\]

Let \(G_\ell^\pm\) solve the same common-shear equation

\[
 (\partial_t+b\partial_2-\Delta_{23})G_\ell^\pm=0,
 \qquad G_\ell^\pm(0)=G_{\ell,0}^\pm,
\tag{Q.31}
\]

and put \(G_\ell=G_\ell^++G_\ell^-\).  For arbitrary constant amplitudes
\(\mathfrak a_\ell\in\mathbb R\), define

\[
 U_N=\sum_{\ell=1}^N\mathfrak a_\ell G_\ell,
 \qquad
 u^{(N)}=(U_N,b,0),
 \qquad p^{(N)}=0.
\tag{Q.32}
\]

### Proposition 1.1 — exact common-shear superposition

For every finite \(N\), (Q.32) is a smooth periodic mean-zero solution of
the unforced incompressible Navier--Stokes equations on the time interval on
which (Q.28)--(Q.31) are considered.

**Proof.**  The fields are independent of \(x_1\), while \(b\) is independent
of \(x_2\).  Hence

\[
 \nabla\cdot u^{(N)}=\partial_1U_N+\partial_2b=0
\tag{Q.33}
\]

and

\[
 u^{(N)}\cdot\nabla=b\partial_2.
\tag{Q.34}
\]

Linearity of (Q.31) gives

\[
 \partial_tU_N+b\partial_2U_N-\Delta U_N=0.
\tag{Q.35}
\]

The second component satisfies

\[
 \partial_tb-\Delta b=0,
 \qquad b\partial_2b=0,
\tag{Q.36}
\]

and the third component is zero.  Thus every component of

\[
 \partial_tu^{(N)}-\Delta u^{(N)}
 +(u^{(N)}\cdot\nabla)u^{(N)}+\nabla p^{(N)}
\tag{Q.37}
\]

vanishes.  Oddness of \(\theta_0\), (Q.30), and uniqueness for the linear
parabolic equations imply

\[
 u^{(N)}(t,-x)=-u^{(N)}(t,x).
\tag{Q.38}
\]

The shear has zero mean by oddness.  Each passive datum has zero mean because
it is an \(x_2\)-derivative, and the common-shear equation preserves its
spatial integral.  This proves the mean-zero statement. \(\square\)

### Corollary 1.2 — exact zero mollified path

Let the frozen mollifier be even and anchor the terminal trajectory at the
origin.  Equation (Q.38) gives

\[
 u_R^{(N)}(t,0)=0.
\tag{Q.39}
\]

The smooth terminal-value ODE therefore has the unique solution

\[
 X_R(t)\equiv0,
 \qquad a_R(t)=a_R'(t)\equiv0.
\tag{Q.40}
\]

Versions M and F coincide for this family.  Periodic copies are already
contained in the periodic heat kernels and do not alter (Q.33)--(Q.40).

## 2. Why the old shears cannot be superposed

Suppose an old packet \(F_\ell\) was evolved under its own shear
\(b_\ell\):

\[
 (\partial_t+b_\ell\partial_2-\Delta_{23})F_\ell=0.
\tag{Q.41}
\]

Placing it under a new common shear \(b\) leaves the exact residual

\[
 (\partial_t+b\partial_2-\Delta_{23})F_\ell
 =(b-b_\ell)\partial_2F_\ell.
\tag{Q.42}
\]

Alternatively, summing the old full velocities gives

\[
 \widehat u
 =\left(\sum_\ell\mathfrak a_\ell F_\ell,
         \sum_m b_m,0\right).
\tag{Q.43}
\]

Its first equation contains the cross residual

\[
 \sum_\ell\sum_{m\ne\ell}
 b_m\mathfrak a_\ell\partial_2F_\ell.
\tag{Q.44}
\]

No linear superposition principle removes (Q.42) or (Q.44).  The valid
construction is (Q.31): freeze one shear first, then re-evolve every packet
under that same coefficient.

Translations in \(x_2\) commute with (Q.31).  Translations in \(x_3\)
generally do not, because the coefficient \(b(t,x_3)\) is not translation
invariant.  Different target heights must therefore be analysed rather than
inserted by symmetry.

## 3. Frozen-angle common-calibration obstruction

The literal R0.74F sequence fixes both

\[
 L_j=\lambda2^j,
 \qquad R_j=e^{-\rho L_j^2}.
\tag{Q.45}
\]

Since the second map is strictly decreasing in \(L_j\), one literal frozen
scale \(R_j\) already determines one index \(j\).  That parameterization
fact is not the obstruction below.  I instead test a common-\(R\) transplant
of the frozen terminal geometry.

Retain

\[
 \lambda=\frac{63}{32},
 \quad c_h=\frac{15}{16},
 \quad \alpha=\frac{14}{15},
 \quad \beta=\frac{\sqrt{31}}{16},
 \quad q_*=\frac12,
\tag{Q.46}
\]

and define

\[
 a_D=\frac{\alpha^2}{260},
 \qquad
 a_S=\min\left\{\frac{\alpha^2}{260},
                  \frac{c_h^2}{264}\right\}
     =\frac{c_h^2}{264}.
\tag{Q.47}
\]

For this section, specialize the arbitrary odd seed in Section 1 to the
R0.74F saturation shear

\[
 g_R(x_3)=\sigma\!\left(\frac{\sin x_3}{16R}\right),
 \qquad
 \theta_R(t,x_3)=e^{t\partial_3^2}g_R(x_3),
\tag{Q.47a}
\]

where \(\sigma\in C^\infty(\mathbb R;[-1,1])\) is odd and equals
\(\operatorname{sgn}s\) for \(|s|\ge1\).  For a common packet scale \(R\),
write

\[
 D_R(h)=\int_{R^2}^{65R^2}\theta_R(t,h)\,dt.
\tag{Q.48}
\]

### Lemma 3.1 — two-parameter positive platform

Let

\[
 L\ge9216,
 \qquad 0<R\le\frac1{32},
 \qquad LR\le\frac5{144},
 \qquad h=c_hLR.
\tag{Q.48a}
\]

Then, uniformly for \(R^2\le t\le65R^2\),

\[
 0\le1-\theta_R(t,h)
 \le4e^{-a_DL^2}.
\tag{Q.48b}
\]

Consequently,

\[
 0\le64R^2-D_R(c_hLR)
 \le256R^2e^{-a_DL^2}.
\tag{Q.49}
\]

**Proof.**  Put

\[
 \delta_R=\arcsin(16R),
 \qquad
 P_R=[\delta_R,\pi-\delta_R]\pmod{2\pi}.
\tag{Q.49a}
\]

Since \(R\le1/32\), \(\delta_R\le32R\).  The datum \(g_R\) equals one on
\(P_R\).  The central-chart condition in (Q.48a) and \(L\ge9216\) give

\[
\begin{aligned}
 \operatorname{dist}_{\mathbb T}(h,P_R^c)
 &\ge(c_hL-32)R\\
 &\ge\alpha LR.
\end{aligned}
\tag{Q.49b}
\]

The last inequality uses
\((c_h-\alpha)L=L/240\ge32\).  If
\(A(t,h)=1-\theta_R(t,h)\), then \(0\le1-g_R\le2\), and every lifted copy
of its support lies outside the real interval of radius \(\alpha LR\)
centred at \(h\).  The periodic heat-kernel expansion and the real Gaussian
two-tail bound therefore give

\[
 0\le A(t,h)
 \le4\exp\!\left[-\frac{\alpha^2L^2R^2}{4t}\right]
 \le4e^{-\alpha^2L^2/260}.
\tag{Q.49c}
\]

This proves (Q.48b).  Integrating it over an interval of length \(64R^2\)
proves (Q.49). \(\square\)

Unlike the original one-parameter presentation, Lemma 3.1 treats \(R\) and
\(L\) independently.  Its proof uses only the explicit saturation plateau,
the central chart, and the periodic Gaussian tail.

### Lemma 3.2 — frozen-angle calibration obstruction

Let \(R_n\downarrow0\).  For \(i=1,2\), let

\[
 L_{i,n}=\lambda2^{k_{i,n}},
 \qquad k_{1,n}<k_{2,n},
 \qquad L_{1,n}\longrightarrow\infty,
\tag{Q.50}
\]

and set

\[
 h_{i,n}=c_hL_{i,n}R_n,
 \qquad q_{i,n}=\beta L_{i,n}R_n.
\tag{Q.51}
\]

Assume that \(L_{2,n}R_n\le5/144\), so Lemma 3.1 applies at both terminal
heights, and that

\[
 \frac{e^{-a_DL_{1,n}^2}}
 {R_n(L_{2,n}-L_{1,n})}\longrightarrow0.
\tag{Q.52}
\]

Then no sequence \(B_n>0\) can satisfy both frozen calibrations

\[
 B_nD_{R_n}(h_{i,n})=q_*+q_{i,n},
 \qquad i=1,2,
\tag{Q.53}
\]

for all sufficiently large \(n\).

**Proof.**  Put

\[
 D_{i,n}=64R_n^2-\delta_{i,n}.
\tag{Q.54}
\]

By (Q.49),

\[
 0\le\delta_{i,n}
 \le CR_n^2e^{-a_DL_{i,n}^2}
 \le CR_n^2e^{-a_DL_{1,n}^2}.
\tag{Q.55}
\]

In particular, \(D_{i,n}>0\) for all sufficiently large \(n\).  If (Q.53)
holds for one \(B_n\), then

\[
 \frac{q_*+\beta L_{1,n}R_n}{D_{1,n}}
 =\frac{q_*+\beta L_{2,n}R_n}{D_{2,n}}.
\tag{Q.56}
\]

Cross multiplication gives the exact identity

\[
\begin{aligned}
 64\beta R_n^3(L_{2,n}-L_{1,n})
 ={}&(q_*+\beta L_{2,n}R_n)\delta_{1,n}\\
    &-(q_*+\beta L_{1,n}R_n)\delta_{2,n}.
\end{aligned}
\tag{Q.57}
\]

The chart assumption bounds both coefficients on the right uniformly.
Equations (Q.55)--(Q.57) imply

\[
 R_n(L_{2,n}-L_{1,n})
 \le Ce^{-a_DL_{1,n}^2},
\tag{Q.58}
\]

contradicting (Q.52). \(\square\)

### Corollary 3.3 — survival-compatible dyadic two-shell no-go

Let \(R_n,L_{i,n},h_{i,n},q_{i,n}\) satisfy (Q.50)--(Q.51), let
\(L_{2,n}R_n\le5/144\), and use the common shear (Q.47a).  Do not assume
(Q.52).  Suppose instead that the inherited R0.74F bridge argument is closed
under its sufficient reserve condition

\[
 R_n^{-1}e^{-a_SL_{1,n}^2}\longrightarrow0.
\tag{Q.59}
\]

Since \(a_D>a_S\), (Q.59) implies

\[
 R_n^{-1}e^{-a_DL_{1,n}^2}\longrightarrow0.
\tag{Q.60}
\]

Distinct dyadic indices give

\[
 L_{2,n}\ge2L_{1,n},
 \qquad L_{2,n}-L_{1,n}\ge L_{1,n}\longrightarrow\infty.
\tag{Q.61}
\]

Thus (Q.52) follows, and Lemma 3.2 applies.  Any such survival-compatible
asymptotic \(N\ge2\) frozen-angle common-shear family fails pairwise by
selecting its two innermost distinct shells.

This conclusion depends on the terminal angle
\((h_i,q_i)=(c_hL_iR,\beta L_iR)\), the common entrance \(q_*=1/2\), one
positive-platform shear, the common \(R^2\)-to-\(65R^2\) time window, and
the survival-compatible asymptotics.  It is an asymptotic frozen-geometry
no-go, not an exact PDE no-go.

## 4. The relaxed terminal geometry remains open

One can remove the algebraic calibration conflict by defining the horizontal
terminal coordinate from the common shear:

\[
 q_\ell=BD_R(h_\ell)-q_*,
\tag{Q.62}
\]

with the corresponding entrance point

\[
 q_{{\rm pre},\ell}
 =-q_*-B\int_0^{R^2}\theta_R(t,h_\ell)\,dt,
\tag{Q.62a}
\]

and asking only that

\[
 h_\ell^2+q_\ell^2
 \in[2^{2k_\ell}R^2,2^{2k_\ell+2}R^2).
\tag{Q.63}
\]

Equations (Q.62)--(Q.63) do not contradict one another formally.  They do
not inherit the old proof.  At minimum, a new construction must re-establish

1. positive-packet bridge survival at every \(h_\ell\);
2. suppression of every inversion partner and every periodic copy;
3. terminal-lobe inclusion with quantitative inner and outer margins;
4. one common terminal interval and one common mollified path;
5. all local-energy and exterior-payment bounds with constants uniform in
   the number and range of target shells.

The remainder of this note records the exact nonlinear ledger that such a
relaxed construction would face.

## 5. Exact two-packet shell ledger

Let

\[
 g_\ell=\mathfrak a_\ell G_\ell,
 \qquad G=g_1+g_2,
 \qquad u^{(2)}=(G,b,0),
\tag{Q.64}
\]

with both packets satisfying

\[
 (\partial_t+b\partial_2-\Delta_{23})g_\ell=0.
\tag{Q.65}
\]

The common inversion parity gives \(X_R=a_R=a_R'=0\).  The physical
pressure is zero.  Let \(\Psi_k^R\), \(\gamma_k\), and \(\eta_R\) be the
frozen shell cutoff, shell weight, and time cutoff.

Every \(\partial_1\Psi_k^R\) row integrates to zero because the solution is
independent of \(x_1\).  The pure \(b^3\partial_2\Psi_k^R\) row integrates
to zero because \(b\) is independent of \(x_2\).  The pressure gauge constant
also integrates to zero by incompressibility.  Therefore

\[
\begin{aligned}
 F_{k,R}^{(2)}(\tau)
 ={}&\frac{\gamma_k}{2R}
 \sum_{\ell=1}^2
 \int_{s_R}^{\tau}\!\!\int
 \eta_R b g_\ell^2\partial_2\Psi_k^R\\
 &+\frac{\gamma_k}{R}
 \int_{s_R}^{\tau}\!\!\int
 \eta_R b g_1g_2\partial_2\Psi_k^R.
\end{aligned}
\tag{Q.66}
\]

The factor \(2\) in \(G^2\) cancels the kinetic-flux factor \(1/2\).  Define
the cross terms

\[
 F_{k,R}^{12}(\tau)
 =\frac{\gamma_k}{R}
 \int_{s_R}^{\tau}\!\!\int
 \eta_R b g_1g_2\partial_2\Psi_k^R,
\tag{Q.67}
\]

\[
 Q_{k,R}^{12}(\tau)
 =\frac{\gamma_k}{R}
 \int_{s_R}^{\tau}\!\!\int
 (\eta_R'\Psi_k^R+\eta_R\Delta\Psi_k^R)g_1g_2.
\tag{Q.68}
\]

For the smooth solution, the defect-completed clock is

\[
\begin{aligned}
 K_{k,R}^{(2)}(\tau)
 ={}&\frac{\gamma_k\eta_R(\tau)}{2R}
 \int\Psi_k^R[b^2+(g_1+g_2)^2]\\
 &+\frac{\gamma_k}{R}
 \int_{s_R}^{\tau}\!\!\int
 \eta_R\Psi_k^R
 [|\partial_3b|^2+|\nabla(g_1+g_2)|^2].
\end{aligned}
\tag{Q.69}
\]

Here and below \(\nabla\) on a packet denotes the \((x_2,x_3)\) gradient.
The clock cross term is exactly

\[
\begin{aligned}
 K_{k,R}^{12}(\tau)
 ={}&\frac{\gamma_k\eta_R(\tau)}{R}
 \int\Psi_k^R g_1g_2\\
 &+\frac{2\gamma_k}{R}
 \int_{s_R}^{\tau}\!\!\int
 \eta_R\Psi_k^R\nabla g_1\cdot\nabla g_2.
\end{aligned}
\tag{Q.70}
\]

The product equation

\[
 (\partial_t+b\partial_2-\Delta)(g_1g_2)
 =-2\nabla g_1\cdot\nabla g_2
\tag{Q.71}
\]

gives the exact cross balance

\[
 \boxed{K_{k,R}^{12}=Q_{k,R}^{12}+F_{k,R}^{12}.}
\tag{Q.72}
\]

Positive variation is not linear.  The safe estimate is

\[
 v_{k,R}^{(2)}
 \le v_{k,R}^{b}+v_{k,R}^{1}+v_{k,R}^{2}
    +\operatorname{TV}K_{k,R}^{12}.
\tag{Q.73}
\]

Here \(v_{k,R}^{b}\) and \(v_{k,R}^{\ell}\) denote the positive variations
of the nonnegative shear and diagonal packet clock components obtained by
expanding (Q.69).

For general \(N\), (Q.67)--(Q.70) produce
\(\binom N2\) packet-pair terms.  Ordinary unweighted Fourier orthogonality
does not remove them because the clock uses the weights
\(\Psi_k^R\), \(\nabla\Psi_k^R\), and \(\eta_R\), and because positive
variation retains earlier increments.

## 6. Nonlinear payment aggregation

The exact Version-M payment has the form

\[
 P_R^{M,(N)}
 =\bigl(\mathcal E_{8R}^{(N)}\bigr)^{3/2}
  +\mathcal G_u^{(N)}+\mathcal G_p^{(N)}+\mathcal H^{(N)}.
\tag{Q.74}
\]

For two packets, the central quadratic row expands as

\[
\begin{aligned}
 \mathcal E_{8R}^{(2)}
 ={}&\operatorname*{ess\,sup}_{t\in I_{8R}}
 \frac1{8R}\int_{B_{8R}}
 [b^2+g_1^2+g_2^2+2g_1g_2]\\
 &+\frac1{8R}\int_{I_{8R}}\!\!\int_{B_{8R}}
 [|\partial_3b|^2+|\nabla g_1|^2+|\nabla g_2|^2
  +2\nabla g_1\cdot\nabla g_2].
\end{aligned}
\tag{Q.75}
\]

Even if every quadratic cross term vanished, suppose that at one common
endpoint the diagonal endpoint energies, together with their accumulated
diagonal dissipations, have total size comparable to \(NT\).  Then

\[
 \mathcal E_{8R}^{(N)}\gtrsim NT,
 \qquad
 \bigl(\mathcal E_{8R}^{(N)}\bigr)^{3/2}
 \gtrsim N^{3/2}T^{3/2}.
\tag{Q.76}
\]

This already reaches the critical lower size whose \(2/3\) power is \(NT\).
Since
\(P_R^{M,(N)}\ge(\mathcal E_{8R}^{(N)})^{3/2}\), one always has

\[
 (P_R^{M,(N)})^{2/3}\ge\mathcal E_{8R}^{(N)}.
\tag{Q.76a}
\]

Within the target stress-test scaling
\(\mathfrak C_R^{M,(N)}\asymp NT\), making the payment term
\(o(\mathfrak C_R^{M,(N)})\) therefore requires

\[
 \mathcal E_{8R}^{(N)}=o(NT).
\tag{Q.77}
\]

The stronger ideal payment
\(P_R^{M,(N)}=O(NT^{3/2})\) would require

\[
 \mathcal E_{8R}^{(N)}=O(N^{2/3}T).
\tag{Q.78}
\]

The exterior velocity row contains

\[
 \mathcal G_u^{(2)}
 =\rho^{-2}\int_{I_\rho}\!\!\int
 W_\rho[b^2+(g_1+g_2)^2]^{3/2},
 \qquad \rho=2R.
\tag{Q.79}
\]

If \(g_1g_2=0\) pointwise throughout the whole payment window, then the
packet increment above the common background is exactly additive:

\[
\begin{aligned}
 &[b^2+(g_1+g_2)^2]^{3/2}-|b|^3\\
 &\quad=[b^2+g_1^2]^{3/2}-|b|^3
       +[b^2+g_2^2]^{3/2}-|b|^3.
\end{aligned}
\tag{Q.80}
\]

Heat flow creates immediate tails, so a strict disjoint-support statement
is unavailable for the present packets.  The general pointwise bound

\[
 \left|\sum_{\ell=1}^Ng_\ell\right|^3
 \le N^2\sum_{\ell=1}^N|g_\ell|^3
\tag{Q.81}
\]

allows an \(N^2\) loss relative to the diagonal cubic sum.  Weighted
quadratic orthogonality alone does not control this convex interaction.

For the harmonic row, let

\[
 \Lambda_\rho^{(N)}(t)
 =\int L_\rho[b^2+(\sum_\ell g_\ell)^2],
 \qquad
 \mathcal H^{(N)}
 =\rho\int_{I_\rho}[\Lambda_\rho^{(N)}(t)]^{3/2}\,dt.
\tag{Q.82}
\]

Even when all weighted quadratic cross terms vanish, simultaneous diagonal
masses are summed before the \(3/2\) power.  Spatial separation therefore
does not by itself make (Q.82) additive.  Time separation can reduce this
row, but it must be reconciled with terminal clock accumulation.

Finally, \(p^{(N)}=0\) removes the physical pressure flux, not the frozen
local-pressure payment.  Its local Riesz input contains

\[
 u^{(N)}\otimes u^{(N)}
 =\begin{pmatrix}
  (\sum_\ell g_\ell)^2 & b\sum_\ell g_\ell &0\\
  b\sum_\ell g_\ell & b^2&0\\
  0&0&0
 \end{pmatrix}.
\tag{Q.83}
\]

The localized split consequently retains packet-pair terms and a
\(3/2\)-integrability payment.  The correct boundary is

\[
\boxed{\text{physical pressure flux }=0}
\tag{Q.84}
\]

while

\[
\boxed{\text{frozen local-pressure payment need not vanish}.}
\tag{Q.85}
\]

## 7. A second obstruction: the inherited exponent windows

The calibration obstruction in Section 3 depends on the frozen terminal
angle.  There is a separate obstruction that remains relevant if the angle is
relaxed while the old survival estimate, dyadic weight, normalized or
amplified packet amplitude, and background-scale payment target are retained.

Let

\[
 S=\log\frac1R,
 \qquad L_2=2L_1,
 \qquad L_i=\lambda2^{j_i},
 \qquad j_2=j_1+1,
 \qquad L_1\longrightarrow\infty.
\tag{Q.86}
\]

If the R0.74F bound is transplanted to an independent common \(R\) and inner
height \(L_1R\), its shift-error majorant is

\[
 CR^{-1}\left(e^{-a_DL_1^2}+e^{-a_SL_1^2}\right).
\tag{Q.87}
\]

Since \(a_S<a_D\), the inherited proof makes this error vanish under

\[
 S-a_SL_1^2\longrightarrow-\infty,
 \qquad
 a_S=\frac{75}{22528}.
\tag{Q.88}
\]

This is a sufficient condition for the existing proof.  It is not claimed to
be necessary for the actual packet to survive.

For the outer packet, retain

\[
 c_\gamma=\frac8{3969},
 \qquad
 \Gamma_2=e^{-c_\gamma L_2^2},
 \qquad
 \mathfrak a_2=\varkappa_2B\Gamma_2^{-1/2}.
\tag{Q.89}
\]

The R0.74O velocity-cubic majorant, divided by the background scale
\(B^3R^3\), is

\[
 \mathcal R_2
 =\varkappa_2^3R\Gamma_2^{-3/2}L_2^{-2}.
\tag{Q.90}
\]

For the exact R0.74O amplification,

\[
 \rho=\frac1{320},
 \qquad
 m=\rho-\frac32c_\gamma=\frac{43}{423360},
 \qquad
 \varkappa_2=L_2^{2/3}e^{mL_2^2/3},
\tag{Q.91}
\]

equation (Q.90) reduces exactly to

\[
 \mathcal R_2=e^{-S+\rho L_2^2}.
\tag{Q.92}
\]

### Proposition 7.1 — inherited proof-window incompatibility

There is no sequence satisfying both the inherited inner shift closure
(Q.88) and boundedness of the inherited outer cubic majorant (Q.92).

**Proof.**  Boundedness of (Q.92) requires

\[
 S\ge\rho L_2^2-O(1)
   =\frac1{80}L_1^2-O(1).
\tag{Q.93}
\]

But

\[
 \frac1{80}-a_S
 =\frac1{80}-\frac{75}{22528}
 =\frac{1033}{112640}>0.
\tag{Q.94}
\]

Equations (Q.88) and (Q.93) are therefore incompatible for large
\(L_1\). \(\square\)

The same conclusion holds for every \(\varkappa_2\ge1\) if the same cubic
majorant is required to stay at background scale.  Indeed, (Q.90) then
requires

\[
 S\ge
 \frac32c_\gamma L_2^2-2\log L_2-O(1)
 =\frac{16}{1323}L_1^2-2\log(2L_1)-O(1),
\tag{Q.95}
\]

and

\[
 \frac{16}{1323}-\frac{75}{22528}
 =\frac{261223}{29804544}>0.
\tag{Q.96}
\]

Proposition 7.1 is a theorem about the simultaneous use of two inherited
proof closures.  Divergence of an upper majorant does not prove that the
actual cubic payment diverges.

### Proposition 7.2 — conditional genuine cubic obstruction

Assume in addition that the outer packet has the R0.74F terminal lobe on a
time interval of length \(R^3\), with lobe volume comparable to
\(L_2R^3\), and that throughout that lobe

\[
 \left|\sum_{\ell\ne2}\mathfrak a_\ell G_\ell\right|
 \le\frac12|\mathfrak a_2G_2|.
\tag{Q.96a}
\]

Then

\[
 \mathcal G_u^{(N)}
 \ge c\mathfrak a_2^3
       e^{-(c_\gamma/4)L_2^2}L_2R^4.
\tag{Q.97}
\]

Consequently, if \(\varkappa_2\ge1\) and the complete payment is bounded by
\(CB^3R^3\), then necessarily

\[
 S\ge
 \frac54c_\gamma L_2^2+\log L_2-O(1)
 =\frac{40}{3969}L_1^2+\log(2L_1)-O(1).
\tag{Q.98}
\]

This is incompatible with (Q.88), since

\[
 \frac{40}{3969}-\frac{75}{22528}
 =\frac{603445}{89413632}>0.
\tag{Q.99}
\]

**Proof.**  The outer lobe lies in \(A_{j_2}(R)=A_{j_2-1}(2R)\).
The exterior weight there is
\(\gamma_{j_2-1}=e^{-(c_\gamma/4)L_2^2}\).  The no-cancellation assumption
gives a fixed lower fraction of \(|\mathfrak a_2G_2|^3\).  Multiplying the
lobe lower bound by its spatial volume and time length, then by the
\((2R)^{-2}\) normalization, gives (Q.97).  Substitute (Q.89), divide by
\(B^3R^3\), and take logarithms to obtain (Q.98). \(\square\)

The no-cancellation premise in Proposition 7.2 has not been proved for the
relaxed multipacket family.  Without it, packet tails may cancel pointwise
inside \(|\sum_\ell g_\ell|^3\).  Thus Proposition 7.2 is a conditional
route-closing statement, not a completed no-go for common-shear packets.

## 8. Decision after Step 1

The common-shear idea passes the exact NSE, divergence, pressure, parity,
periodicity, and mollified-path gates.  The direct frozen-angle transplant
fails before the all-shell payment estimate: one common \(B\) cannot satisfy
the two frozen terminal calibrations while retaining the inner survival
reserve.

The only live continuation from this packet architecture is a relaxed
terminal geometry such as (Q.62)--(Q.63).  It must also change or defeat at
least one hypothesis of the exponent obstruction in Section 7.  Before any
full \(N\)-packet construction, it must pass four calculations in this order:

1. simultaneous shell placement and bridge survival with one \(B\);
2. outer-lobe dominance or a different amplitude/payment scaling;
3. central, harmonic, and exterior-cubic packet-tail estimates;
4. the \(\binom N2\) weighted cross-clock ledger and the full all-shell
   positive-variation bound.

Failure of one of these gates for a uniform quantitative reason would be a
valid obstruction.  Failure of the old parameterization alone would not
prove the effective-shell estimate (Q.12).

## 9. Internal source ledger

The inherited definitions and estimates used above are located as follows.

- R0.74F, Sections 1 and 3--6: the saturation shear, calibrated single
  packet, periodic Gaussian leakage, bridge survival, inversion suppression,
  terminal lobe, and dyadic shell weight.
- R0.74H, equations (3.2) and (7.2): the exact kinetic-pressure collar flux
  and its pressure-free passive-shear reduction.
- R0.74P, equations (2.6)--(2.10): the shell clock, cutoff primitive, flux,
  and defect-completed balance.
- R0.74E, equations (3.6)--(3.10): the central energy, exterior velocity and
  pressure rows, harmonic row, and Version-M payment.
- R0.74O, equations (1.1)--(1.12) and (2.9)--(2.15): the normalized and
  amplified amplitudes and the inherited cubic majorant.

The finite-\(N\) common-shear substitution, the two-parameter platform lemma,
the common-calibration obstruction, and the proof-window comparison are
proved in this note.  The finite certificate checks their rational constants
and source-text bindings only; it does not replace the analytic proofs.
