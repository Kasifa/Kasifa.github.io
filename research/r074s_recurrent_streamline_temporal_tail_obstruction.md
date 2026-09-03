# R0.74S Step 17 — recurrent streamlines destroy every sublinear absolute temporal tail

## 0. Result, correction, and scope

Step 16 used Taylor's exact decaying vortex with terminal centre
\(x_*=(\pi/4,0,0)\).  That centre lies on a nonrecurrent invariant line:
the trajectory crosses the relevant phase only once, and its absolute flux
variation is of order \(A^2\).  The calculation is correct for that terminal
setting, but it cannot decide a statement quantified over every terminal
setting.

This step moves the terminal centre to a regular closed streamline of the
same smooth exact solution.  The change has a decisive effect.  In a fixed
physical time window the moving centre makes \(O_R(A)\) circuits, while the
flux density has size \(A^3\).  Signed increments cancel from circuit to
circuit, but absolute temporal variation counts every circuit.

The conclusions are:

1. For every \(p\in[1,\infty]\), every finite deletion budget \(N\), and
   fixed admissible \(R\) chosen after \(N\), as \(A\to\infty\),
   \[
    \mathfrak H^F_{p,N,R}\asymp_{p,N,R}A^3,
    \qquad P_R^M\asymp_RA^3.
   \]
2. Consequently, every universal power-only estimate
   \(\mathfrak H^F_{p,N,R}\le C(P_R^M)^\beta\) with \(\beta<1\) is false.
   This includes both the already-refuted \(p>1\) proposal (S.342) and the
   Step 16 endpoint proposal (S.444).  Thus **(S.444 is false)**.
3. The obstruction is exactly recurrence plus absolute value.  On the same
   family, every signed flux range is only \(O_R(A^2)\).  The fixed-deletion
   positive-excursion tail introduced below is compatible with the quadratic
   scale and still implies the Step 15 hybrid terminal gate.
4. Equations (S.439)--(S.443) remain valid for the special separatrix
   terminal centre used in Step 16.  What is superseded is the extrapolation
   from that special centre to the universal status of (S.444), and the
   claim that \(1-1/(3p)\) is the final necessary payment exponent.

This is a route correction for one overstrong absolute-variation ansatz.  It
does **not** refute the signed hybrid terminal-flux gate, the terminal-crown
coercivity estimate (S.407), Q.12, Q.1, scale contraction, or regularity.
The example is globally smooth.  **NOT CLAY.**

## 1. The exact Taylor family and a regular closed streamline

On \(\mathbb T^3=(-\pi,\pi]^3\), define

\[
 \boxed{
 \psi(x_1,x_2)=\sin x_1\sin x_2,
 \qquad
 W=(\partial_2\psi,-\partial_1\psi,0)
   =(\sin x_1\cos x_2,-\cos x_1\sin x_2,0).}
 \tag{S.445}
\]

With

\[
 p_W={\cos2x_1+\cos2x_2\over4},
 \qquad b_A(t)=Ae^{-2(t-t_0)},
 \qquad u_A=b_AW,
 \qquad p_A=b_A^2p_W,
\]

the identities
\(\nabla\!\cdot W=0\), \(\Delta W=-2W\), and
\((W\!\cdot\!\nabla)W=-\nabla p_W\) show directly that \((u_A,p_A)\)
is a smooth periodic mean-zero unforced Navier--Stokes solution for every
\(A>0\).

Let \(\Gamma\) be the component in \((0,\pi)^2\) of

\[
 \boxed{
 \{\psi=1/2\}
 =\{(x_1,x_2):\sin x_1\sin x_2=1/2\}.}
 \tag{S.446}
\]

The level is regular.  Indeed, on \(\{\psi=1/2\}\) both sine factors are
nonzero.  If \(\nabla\psi=0\), then
\(\cos x_1=\cos x_2=0\), which would give \(\psi=1\), not \(1/2\).
Compactness and connectedness can also be seen explicitly, rather than
being inferred from regularity alone.  The level equation implies
\(\sin x_i\ge1/2\), so \(x_i\in[\pi/6,5\pi/6]\).  For
\(x_1\in[\pi/6,5\pi/6]\), its two branches are

\[
 x_2=\arcsin {1\over2\sin x_1}
 \quad\hbox{and}\quad
 x_2=\pi-\arcsin {1\over2\sin x_1}.
\]

They join at \(x_1=\pi/6,5\pi/6\), where \(x_2=\pi/2\), and form one
compact connected oval surrounding \((\pi/2,\pi/2)\).  Thus \(\Gamma\)
is a smooth circle, and both \((\pi/4,\pi/4)\) and
\((\pi/2,\pi/6)\) lie on this same component.  Since
\(W=(\partial_2\psi,-\partial_1\psi)\), the field is nonzero and tangent
to \(\Gamma\).

Choose

\[
 x_*=(\pi/4,\pi/4,0)
\]

and let \(\chi\) solve \(\chi'=W(\chi)\), \(\chi(0)=x_*\), on
\(\Gamma\times\{0\}\).  The preceding explicit compact regular-level
argument gives a finite period

\[
 \boxed{
 \chi(s+T_*)=\chi(s),
 \qquad
 0<T_*:=\int_\Gamma{d\ell\over|W|}<\infty.}
 \tag{S.447}
\]

Put

\[
 \boxed{
 g(s):=|W(\chi(s))|^2,
 \qquad q(s):=g'(s)
  =W(\chi(s))\cdot\nabla|W|^2(\chi(s)).}
 \tag{S.448}
\]

Both are smooth and \(T_*\)-periodic.  The function \(g\) is not constant:
the points \((\pi/4,\pi/4)\) and \((\pi/2,\pi/6)\) belong to the same
component \(\Gamma\), while \(|W|^2\) takes the respective values \(1/2\)
and \(3/4\).  Therefore

\[
 V_p:=\int_0^{T_*}|q(s)|^p\,ds>0
 \quad(1\le p<\infty),
 \qquad
 q_\infty:=\max_{[0,T_*]}|q|>0.
\]

In particular, periodic return forces \(V_1\ge1/2\).  We will repeatedly
use the elementary periodic averaging bound

\[
 \boxed{
 L\ge2T_*
 \quad\Longrightarrow\quad
 \int_a^{a+L}|q(s)|^p\,ds
 \ge {V_p\over2T_*}L.}
 \tag{S.449}
\]

It follows by retaining \(\lfloor L/T_*\rfloor\) complete periods.

## 2. Simultaneous shell activation and the recurrent Version-M path

Fix an arbitrary \(N\in\mathbb N_0\), and set \(M=N+1\).  Retain the
unperiodized physical shell cutoffs \(\psi_k^R\), their periodizations
\(\Psi_k^R\), and the super-Gaussian weights \(\gamma_k\).  As in Step 16,

\[
 \begin{aligned}
 m_{k,R}&:=\int_{\mathbb R^3}\psi_k^R(y)\,dy,\\
 c_{k,R}&:=\int_{\mathbb R^3}\psi_k^R(y)
                  \cos((2,2,0)\cdot y)\,dy,\\
 J_{k,R}(\xi)&:={m_{k,R}\over2}
  +c_{k,R}\left(|W(\xi)|^2-{1\over2}\right).
 \end{aligned}
 \tag{S.450}
\]

Choose \(R\) after \(N\) so that

\[
 \boxed{
 0<R<\min\left\{{\pi\over16},
 {\pi\over6\sqrt2(2^{M+1}+1/8)}\right\},
 \qquad
 \mu_R\ge{1\over2},
 \qquad
 \overline I_{8R}\Subset(0,T).}
 \tag{S.451}
\]

Here \(\varphi_R^{\rm per}*W=\mu_RW\).  The support/cosine argument from
Step 16 then gives

\[
 c_{k,R}\ge{1\over2}m_{k,R}>0,
 \qquad 1\le k\le M.
\]

Define the recurrent phase and terminally anchored path by

\[
 \boxed{
 \theta_A(t):=\mu_R\int_{t_0}^{t}b_A(r)\,dr,
 \qquad
 \xi_A(t):=\chi(\theta_A(t)),
 \qquad
 \theta_A'(t)=\mu_Rb_A(t).}
 \tag{S.452}
\]

Then \(\xi_A(t_0)=x_*\) and
\(\dot\xi_A=\mu_Rb_AW(\xi_A)\), so \(\xi_A=X_R\) is exactly the frozen
Version-M trajectory.  On \(I_R=(t_0-R^2,t_0)\),

\[
 \boxed{
 \theta_A(t_0-R^2)=-L_A,
 \qquad
 L_A={\mu_RA\over2}(e^{2R^2}-1).}
 \tag{S.453}
\]

Thus \(L_A/T_*\to\infty\): the moving centre completes linearly many
circuits as \(A\to\infty\).  There is no lift ambiguity because \(\chi\)
itself is the chosen periodic parametrization of the orbit.

## 3. Exact recurrent flux and all \(L_t^p\) lower bounds

The fixed-frame kinetic and physical-pressure fluxes cancel exactly, as in
Step 16, because \(\nabla\cdot[(|W|^2/2+p_W)W]=0\).  The pressure gauge
also cancels shellwise.  Using \(\nabla J_{k,R}=c_{k,R}\nabla|W|^2\), the
moving-cutoff drift is

\[
 \boxed{
 \dot F_{k,R}(t)
 ={\gamma_k\mu_Rc_{k,R}\over2R}
   \eta_R(t)b_A(t)^3q(\theta_A(t)).}
 \tag{S.454}
\]

The terminal target interval \(I_R\) lies where \(\eta_R=1\).  For
\(1\le p<\infty\), the dimensionless normalization gives

\[
 \boxed{
 \|h_{k,R}\|_{L^p(0,4)}^p
 =R^{2p-2}\int_{s_R}^{t_0}|\dot F_{k,R}(t)|^p\,dt.}
 \tag{S.455}
\]

Restrict (S.455) to \(I_R\), substitute
\(d\theta=\mu_Rb_A\,dt\), use \(b_A\ge A\), and then apply (S.449).
Once \(L_A\ge2T_*\), for every \(1\le k\le M\),

\[
 \boxed{
 \begin{aligned}
 \|h_{k,R}\|_p^p
 &\ge { (\gamma_kc_{k,R})^p\mu_R^{p-1}R^{p-2}
          \over2^p}
       A^{3p-1}\int_{-L_A}^{0}|q(\theta)|^p\,d\theta\\
 &\ge { (\gamma_kc_{k,R})^p\mu_R^pR^{p-2}V_p
          (e^{2R^2}-1)\over 2^{p+2}T_*}\,A^{3p}.
 \end{aligned}}
 \tag{S.456}
\]

For \(p=\infty\), once \(L_A\ge T_*\), the orbit contains a phase where
\(|q|=q_\infty\), and hence

\[
 \boxed{
 \|h_{k,R}\|_\infty
 \ge {\gamma_k\mu_Rc_{k,R}R\over2}
       q_\infty A^3,
 \qquad 1\le k\le M.}
 \tag{S.457}
\]

Every set of at most \(N=M-1\) shell indices leaves at least one of the
first \(M\) shells.  Therefore, for every \(p\in[1,\infty]\) and
\(A\ge A_0(R)\) large enough that \(L_A\ge2T_*\),

\[
 \boxed{
 \mathfrak H^F_{p,N,R}\ge d_{p,N,R}A^3,
 \qquad d_{p,N,R}>0.}
 \tag{S.458}
\]

There is also a matching upper bound.  Formula (S.454),
\(|c_{k,R}|\le m_{k,R}\), boundedness of \(q\), and
\(\sum_k\gamma_km_{k,R}<\infty\) give, with \(N,R,p\) fixed,

\[
 \boxed{
 d_{p,N,R}A^3
 \le\mathfrak H^F_{p,N,R}
 \le D_{p,R}A^3.}
 \tag{S.459}
\]

Here and below the two-sided lower laws for this family are asserted for
\(A\ge A_0(R)\); all asymptotic comparisons are as \(A\to\infty\).

The lower bound is a continuum analytic statement.  Finite calculations
below only check its exact identities and exponent bookkeeping.

## 4. The complete payment remains cubic

Translations around a closed orbit do not change the amplitude of the
fixed smooth profiles.  On \(\overline I_{8R}\),
\(A\le b_A\le Ae^{128R^2}\).  The same row-by-row calculation as Step 16
therefore gives

\[
 \boxed{
 \begin{aligned}
 \mathcal E^{M,R}(z_0,8R)&\le C_RA^2,\\
 \mathcal G_{v_R,\pi_R}^{M,R}(z_0,2R;1)&\le C_RA^3,\\
 \Lambda_{2R}^{M,R}(t)&\le C_RA^2,\\
 \mathcal H_{v_R}^{M,R}(z_0,2R)&\le C_RA^3.
 \end{aligned}}
 \tag{S.460}
\]

The exterior \(\mathcal G\) sum uses the frozen super-Gaussian weights;
the harmonic \(\mathcal H\) row uses its algebraic order-\(-4\) kernel.
The fixed pressure gauge and every nonnegative row of the Version-M payment
are included.

At good times tending to \(t_0\), the local energy on \(B_{8R}\) tends to

\[
 {A^2\over8R}\int_{B_{8R}}|W(y+x_*)|^2\,dy>0.
\]

Consequently,

\[
 \boxed{
 c_RA^3\le P_R^M\le C_RA^3.}
 \tag{S.461}
\]

This is the complete \(P_R^M\), not one selected payment row.

## 5. Failure of every sublinear absolute temporal-tail power

Let \(p\in[1,\infty]\), \(N\in\mathbb N_0\), and
\(\beta<1\) be fixed.  After choosing \(R\) by (S.451), (S.458) and
(S.461) give the following bound: use the upper half of (S.461) when
\(\beta\ge0\), and its lower half when \(\beta<0\), because raising a
positive quantity to a negative power reverses the comparison.

\[
 \boxed{
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^\beta}
 \ge c_{p,N,R,\beta}A^{3(1-\beta)}
 \longrightarrow\infty.}
 \tag{S.462}
\]

Equivalently, the exact quantifier statement is

\[
 \boxed{
 \begin{gathered}
 \forall p\in[1,\infty],\quad
 \forall N\in\mathbb N_0,\quad
 \forall\beta<1,\quad
 \forall C>0,\\
 \exists\text{ admissible }R,z_0\text{ and a smooth periodic unforced
 Version-M solution such that}\\
 \mathfrak H^F_{p,N,R}>C(P_R^M)^\beta.
 \end{gathered}}
 \tag{S.463}
\]

Taking \(\beta=2/3\) and \(p=1\) is the exact negation of (S.444).  For
all \(p\ge1\), any power-only estimate of this absolute temporal-tail form
requires \(\beta\ge1\).  The separatrix lower law
\(A^{3-1/p}\) in Step 16 remains correct for that path but is not the
worst terminal setting.

## 6. Signed range stays at the quadratic amplitude scale

The same formula exposes what the absolute value destroyed.  Since
\(d[g(\theta_A(t))]/dt=\mu_Rb_Aq(\theta_A(t))\), (S.454) factors as

\[
 \boxed{
 \dot F_{k,R}(t)
 ={\gamma_kc_{k,R}\over2R}\,
   \eta_R(t)b_A(t)^2{d\over dt}g(\theta_A(t)).}
 \tag{S.464}
\]

For \(s_R\le a<b<t_0\), integration by parts gives

\[
 \boxed{
 \begin{aligned}
 F_{k,R}(b)-F_{k,R}(a)
 ={\gamma_kc_{k,R}\over2R}\Bigg(&
   [\eta_Rb_A^2g(\theta_A)]_a^b\\
 &-\int_a^b(\eta_R'b_A^2-4\eta_Rb_A^2)
       g(\theta_A)\,dt\Bigg).
 \end{aligned}}
 \tag{S.465}
\]

Here \(b_A'=-2b_A\), \(0\le\eta_R\le1\), and the frozen nondecreasing
cutoff satisfies \(\int|\eta_R'|=1\).  Since \(g\) is bounded and the
full time interval has length \(4R^2\),

\[
 \boxed{
 \sum_{k\ge1}\operatorname {osc}_{[s_R,t_0)}F_{k,R}
 \le C_RA^2,
 \qquad
 \operatorname {osc}_I F:=\sup_{a,b\in I}|F(b)-F(a)|.}
 \tag{S.466}
\]

Conversely, orient the comparison so that it is a positive forward
increment.  There is an \(s_*\in(0,T_*)\) with
\(\chi(s_*)=(\pi/2,\pi/6,0)\): at \(s=0\), both the sign of \(W\) and the
explicit lower branch above point from \((\pi/4,\pi/4)\) toward that
point.  Hence \(g(s_*)-g(0)=1/4\).  For all large \(A\), choose
\(a<b\) in \(I_R\) by
\(\theta_A(a)=-T_*\) and \(\theta_A(b)=-T_*+s_*\).  Then
\(t_0-a,t_0-b=O_R(A^{-1})\), so
\(b_A(a)^2,b_A(b)^2=A^2+O_R(A)\).  Since \(\eta_R=1\) there, (S.465)
becomes

\[
 F_{k,R}(b)-F_{k,R}(a)
 ={\gamma_kc_{k,R}\over2R}
 \left({A^2\over4}+O_R(A)
       +4\int_a^b b_A(t)^2g(\theta_A(t))\,dt\right)>0.
\]

The integral is nonnegative.  Thus, for sufficiently large \(A\), every
\(1\le k\le M\) has both two-sided oscillation and positive excursion at
least \(c_{k,R}'A^2\).  This proves a signed range of order \(A^2\), even
though the absolute variation is of order \(A^3\), and supplies the
forward-oriented lower bound needed in (S.471).

## 7. Exact BV decomposition and the correct successor target

At \(p=1\), the dimensionless normalization cancels exactly:

\[
 \boxed{
 \mathfrak H^F_{1,N,R}
 =\inf_{\#S\le N}\sum_{k\notin S}
   \operatorname {TV}_{[s_R,t_0)}F_{k,R}.}
 \tag{S.467}
\]

Let

\[
 V_{k,R}^\pm:=\int_{s_R}^{t_0}[\pm\dot F_{k,R}(t)]_+\,dt,
 \qquad
 B_{k,R}:=\min\{V_{k,R}^+,V_{k,R}^-\}.
\]

Since \(F_{k,R}(s_R)=0\) and the inherited variation ledger is summable,
the terminal limit exists and Jordan decomposition gives the exact identity

\[
 \boxed{
 \operatorname {TV}F_{k,R}
 =|F_{k,R}(t_0^-)|+2B_{k,R}.}
 \tag{S.468}
\]

The quantity \(B_{k,R}\) is the temporal backtracking debt.  On the closed
orbit, the coordinatewise \(p=1\) lower bound (S.456), the coordinatewise
upper bound from (S.454), and (S.466)--(S.468) imply that this debt is
\(\asymp_{k,R}A^3\) on each activated shell, for large \(A\).  Signed
local-energy balance can control an endpoint or a range; it cannot control
(S.468) after the absolute value without paying for every recurrent
circuit.

For the forward orientation relevant to the hybrid increments, define

\[
 \operatorname {osc}_I^+F
 :=\sup_{a<b,\ a,b\in I}[F(b)-F(a)]_+,
\]

and the fixed-deletion positive-excursion tail

\[
 \boxed{
 \mathfrak O^{F,+}_{N,R}
 :=\inf_{\#S\le N}\sum_{k\notin S}
   \operatorname {osc}^+_{[s_R,t_0)}F_{k,R}.}
 \tag{S.469}
\]

Every Step 15 hybrid coordinate \(z_k(\tau)\) is an increment of
\(F_{k,R}\) between two times in \([s_R,t_0)\).  Hence, with
\(\mathfrak Z_{N,R}^{\boldsymbol\lambda}\) as defined there,

\[
 \boxed{
 \mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal T_R)
 \le\mathfrak O^{F,+}_{N,R}
 \le\mathfrak H^F_{1,N,R}.}
 \tag{S.470}
\]

The first inequality keeps one deletion set across all terminal times,
whereas the direct Step 15 deletion may depend on \(\tau\); it is therefore
stronger in quantifiers than the direct Step 15 gate.  The
second is the elementary range-versus-variation inequality.  On the present
exact family, as \(A\to\infty\),

\[
 \boxed{
 \mathfrak O^{F,+}_{N,R}\asymp_{N,R}A^2
 \asymp_{N,R}(P_R^M)^{2/3},
 \qquad
 \mathfrak H^F_{1,N,R}\asymp_{N,R}A^3.}
 \tag{S.471}
\]

Thus a clean surviving sufficient input is

\[
 \boxed{
 \begin{gathered}
 \exists N_O\in\mathbb N_0,\ C>0\text{ universal such that}\\
 \forall\text{ admissible Version-M solutions, }R,z_0
 \text{ and terminal settings},\qquad
 \mathfrak O^{F,+}_{N_O,R}\le C(P_R^M)^{2/3}.
 \end{gathered}}
 \tag{S.472}
\]

Equation (S.472) is **OPEN**.  By (S.470) and Step 15
(S.385)--(S.391), it would close the complete hybrid residual with a
single fixed-across-time deletion set.  It is strictly better aligned with
the signed terminal problem than (S.444), because it does not charge
repeated backtracking that cancels in every relevant increment.

The even weaker direct hybrid terminal gate from Step 15 also remains
**OPEN**.  A future proof need not establish the fixed-deletion strengthening
(S.472).

There is also an exact clock-level reformulation.  Put

\[
 \boxed{
 A_R=(P_R^M)^{2/3},
 \qquad
 B_{Q,R}:=\sum_k\operatorname {TV}Q_{k,R}\le C_QA_R.}
 \tag{S.473}
\]

For the completed nonnegative clocks \(K_{k,R}=F_{k,R}+Q_{k,R}\), define

\[
 \boxed{
 \begin{aligned}
 \mathfrak M^K_{N,R}
 &:=\inf_{\#S\le N}\sum_{k\notin S}
       \sup_{t\in[s_R,t_0)}K_{k,R}(t),\\
 \mathfrak V^K_{N,R}
 &:=\inf_{\#S\le N}\sum_{k\notin S}
       \operatorname {Var}^{+}_{[s_R,t_0)}K_{k,R}.
 \end{aligned}}
 \tag{S.474}
\]

For each fixed deletion set, use \(K\ge0\), \(F=K-Q\), and the common
zero start, and only then optimize.  This gives

\[
 \boxed{
 \begin{aligned}
 \mathfrak O^{F,+}_{N,R}
 &\le\mathfrak M^K_{N,R}+B_{Q,R},
 &\mathfrak M^K_{N,R}
 &\le\mathfrak O^{F,+}_{N,R}+B_{Q,R},\\
 \mathfrak V^K_{N,R}
 &\le\mathfrak H^F_{1,N,R}+B_{Q,R},
 &\mathfrak H^F_{1,N,R}
 &\le2\mathfrak V^K_{N,R}+B_{Q,R},\\
 \mathfrak M^K_{N,R}&\le\mathfrak V^K_{N,R}.
 \end{aligned}}
 \tag{S.475}
\]

For the fourth inequality, a nonnegative clock starting at zero has
\(\operatorname {TV}K\le2\operatorname {Var}^{+}K\).  Equations
(S.473)--(S.475) show that (S.444) is essentially a positive-variation
packing theorem for the completed clocks, whereas the surviving target is
only a maximal-height or positive-excursion packing theorem.  The latter
forgets repeated up-and-down traversal, exactly as the terminal problem
requires.

## 8. Primary-source and collision boundary

The exact field is the classical bi-periodic decaying vortex from G. I.
Taylor, [*On the decay of vortices in a viscous fluid*](https://doi.org/10.1080/14786442308634295)
(1923).  The closed-streamline recurrence, the Version-M trajectory, the
physical-shell deletion, and the payment comparison above are proved by
direct substitution; they are not attributed to the historical source.

A bounded primary-source search checked nearby architectures:

- J. Yang,
  [*Construction of Maximal Functions associated with Skewed Cylinders
  Generated by Incompressible Flows and Applications*](https://arxiv.org/abs/2008.05588),
  proves, under the paper's divergence-free generator and
  \(M(\nabla u)\in L^p\) hypotheses, weak-\((1,1)\) and
  strong-\((q,q)\), \(q>1\), maximal estimates for \(\eta\)-admissible
  cylinders generated by mollified trajectories.  It does not give strong
  \(L^1\) variation of the present flux or one fixed shell deletion.
- R. Dascaliuc and Z. Grujić,
  [*Energy cascades and flux locality in physical scales of the 3D
  Navier--Stokes equations*](https://arxiv.org/abs/1101.2193), control signed,
  time/ensemble-averaged physical-space flux under inertial-range
  hypotheses, not absolute temporal variation along one moving centre.
- J. Wolf,
  [*On the local pressure of the Navier--Stokes equations and related
  systems*](https://arxiv.org/abs/1611.01482), supplies a local pressure
  representation but no temporal BV estimate.
- J. Duchon and R. Robert,
  [*Dissipation d'énergie pour des solutions faibles des équations d'Euler
  et Navier--Stokes incompressibles*](https://www.numdam.org/item/SEDP_1999-2000____A13_0/),
  identify a local energy-defect distribution in a signed local balance;
  their result does not bound the absolute backtracking debt in (S.468).

These sources support geometric, pressure, or signed-energy ingredients.
They do not rescue the now-explicitly-false estimate (S.444).  The search
was bounded and is not a novelty or priority claim.

## 9. Claim ledger and route decision

The following are **PROVED** in the frozen Version-M setting:

- the regular closed-streamline construction and recurrence lemma,
  (S.445)--(S.449);
- simultaneous activation of arbitrary \(N+1\) physical shells and the
  exact recurrent path, (S.450)--(S.453);
- the exact flux identity and \(A^3\) lower and upper temporal-tail laws for
  every \(p\ge1\), (S.454)--(S.459);
- the complete-payment comparison \(P_R^M\asymp_RA^3\),
  (S.460)--(S.461);
- the quantifier-level failure of every sublinear power-only absolute tail,
  (S.462)--(S.463), including **(S.444 is false)**;
- the signed \(A^2\) range bound and the exact BV/backtracking decomposition,
  (S.464)--(S.468); and
- the implication from fixed-deletion positive excursion to the Step 15
  hybrid gate, (S.469)--(S.470), together with exact-family separation
  (S.471); and
- the exact completed-clock comparison (S.473)--(S.475).

The following is **OPEN**:

- the fixed-deletion positive-excursion estimate (S.472), equivalently up
  to the already-paid \(Q\)-variation, the maximal-height clock estimate.

The following remain **OPEN AND UNCHANGED**:

- the weaker direct hybrid terminal-flux gate, terminal-crown coercivity
  (S.407), (S.375), (S.288), (S.303), (S.272), Step 10 (S.243), Q.12,
  Q.1, scale contraction, and regularity.

The route decision is strict.  No later proof may use (S.342) or (S.444),
or any \(\mathfrak H^F_{p,N,R}\lesssim(P_R^M)^\beta\) with \(\beta<1\):
all are false on a globally smooth exact solution.  The next temporal task
is to analyze the signed positive-excursion tail (S.469), or to work
directly with the hybrid last-exit increments, without replacing range by
total variation.  The terminal-crown route remains independently available.
