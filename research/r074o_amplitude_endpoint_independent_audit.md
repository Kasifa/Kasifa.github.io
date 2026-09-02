# R0.74O independent amplitude-endpoint audit

## 1. Binding, method, and verdict

This audit does not accept the conclusion of the R0.74O note as a premise.
It starts from the frozen general-amplitude inequalities, checks them against
the cited R0.74F/G/H/J/N source statements, and independently recomputes every
amplitude and exponent conversion used in the counterexample.

The verdict binds these exact current objects.

| Object | SHA-256 | Role |
|---|---|---|
| `research/r074o_problem_freeze.md` | `c461b85425e58ad0bb371bf7e1e6fe79301fd200912c67a15d4d8ebefb9ec54f` | frozen inputs and promotion gate |
| `research/r074o_amplitude_endpoint_counterexample.md` | `471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb` | proof under audit |
| `research/r074o_gap_matrix.md` | `11aaae9308056cb2afa5b8d3166fbeecf9713aeb77e05bd5128fc3835231cdcd` | final claim classification |

The inherited source statements were checked at the following exact hashes.

| Inherited object | SHA-256 | Fact used here |
|---|---|---|
| `research/r074f_two_packet_survival.md` | `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb` | exact family and every-amplitude terminal-lobe lower bound |
| `research/r074g_complete_payment_counterexample.md` | `95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be` | general-amplitude energy, pressure, cubic, and harmonic upper rows |
| `research/r074h_collar_flux_two_regime_closure.md` | `8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1` | signed-flux identity and energy closure |
| `research/r074j_matching_payment_law.md` | `d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad` | amplitude-independent fifth-shell payment lower bound |
| `research/r074n_all_shell_synthesis.md` | `ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e` | normalized-amplitude complete collar upper bound |

**Verdict: PASS.**  For all sufficiently large \(j\), the displayed
amplified fields are exact smooth periodic mean-zero unforced solutions and
the frozen premises rigorously imply

\[
 P_j^*\asymp B_j^3R_j^3,
 \qquad
 X_j^*\asymp\mathfrak C_j^*
 \asymp
 (P_j^*)^{8024/11907}
 (1+\log_+P_j^*)^{7/6}.
\]

Consequently the scalar square-root-log upper bound fails for both
\(X_R^\alpha\) and \(\mathfrak C_R^\alpha\).  This is a familywise no-go
result for a scalar-payment-only bound, not a regularity or singularity
result.

## 2. Independent exact-solution and frame check

Write

\[
 u=(\mathfrak aF,B\theta,0),\qquad p=0,
\]

where \(F=F(t,x_2,x_3)\), \(\theta=\theta(t,x_3)\),

\[
 F_t+B\theta\,\partial_2F=\Delta_{23}F,
 \qquad
 \theta_t=\partial_3^2\theta.
\]

For every finite spatially constant \(\mathfrak a>0\),

\[
 \nabla\cdot u
 =\partial_1(\mathfrak aF)+\partial_2(B\theta)=0.
\]

The first Navier--Stokes component is \(\mathfrak a\) times the displayed
linear equation for \(F\).  The second component is \(B\) times the heat
equation for \(\theta\), because \(u_3=0\) and \(\partial_2\theta=0\).
The third component is zero.  Thus \(p=0\) closes the equation exactly; this
is not a formal amplitude rescaling of a general Navier--Stokes solution.
Periodic parabolic evolution supplies smoothness for the required time
range, while the inherited derivative/odd construction gives mean zero.

The inherited full-inversion oddness makes the even-mollifier velocity at
the origin vanish.  The terminally anchored trajectory ODE therefore has
the identically zero solution, and uniqueness gives

\[
 X_R(t)=a_R(t)=a_R'(t)=0.
\]

Here \(X_R(t)\) is the trajectory, not the endpoint quantity
\(X_R^\alpha\).  Hence \(v_R=w_R=u\), Versions M and F coincide, and the
Version-F acceleration payment is exactly zero for every amplitude.

## 3. Exact arithmetic and the complete payment ledger

The independently reduced constants are

\[
 \rho=\frac1{320},\qquad
 c_\gamma=\frac8{3969},\qquad
 d_E=\frac{98}{29475},
\]

\[
 e_E=d_E-c_\gamma
 =\frac{17018}{12998475},
\]

and

\[
 m=\rho-\frac32c_\gamma
 =\frac{43}{423360}>0.
\]

Set

\[
 R=e^{-\rho L^2},\qquad
 \Gamma=e^{-c_\gamma L^2},\qquad
 \mathfrak a_0=B\Gamma^{-1/2},
\]

and choose

\[
 \varkappa=L^{2/3}e^{mL^2/3},
 \qquad
 \mathfrak a_*=\varkappa B\Gamma^{-1/2}.
\]

The notation \(\varkappa\) is distinct from the inherited fixed geometric
constant \(\kappa=16\).

### 3.1 Buffered energy and pressure

After division by the background energy \(B^2R^2\), the nonperiodic packet
majorant is

\[
\begin{aligned}
 \frac{\mathfrak a_*^2R^2e^{-d_EL^2}}{B^2R^2}
 &=\varkappa^2\Gamma^{-1}e^{-d_EL^2}\\
 &=L^{4/3}
 e^{-(e_E-2m/3)L^2}.
\end{aligned}
\]

Exact rational reduction gives

\[
 e_E-\frac{2m}{3}
 =\frac{1171}{943200}>0.
\]

The periodic-copy ratio is

\[
 L^{4/3}
 \exp\!\left[
 \left(\frac{2m}{3}+c_\gamma\right)L^2
 -c e^{2\rho L^2}
 \right]\longrightarrow0.
\]

Thus \(\mathcal E_*\le CB^2R^2\), and the inherited averaged local Riesz
estimate gives

\[
 \mathcal G_{p,*}\le C\mathcal E_*^{3/2}
 \le CB^3R^3.
\]

This retains the gauge-fixed pressure row even though the physical pressure
is zero.

### 3.2 Velocity-cubic and harmonic rows

For the velocity-cubic packet majorant, the exact algebraic ratio to the
background is

\[
\begin{aligned}
 \frac{\mathfrak a_*^3R^4L^{-2}}{B^3R^3}
 &=\varkappa^3R\Gamma^{-3/2}L^{-2}\\
 &=L^2e^{mL^2}e^{-\rho L^2}
   e^{(3/2)c_\gamma L^2}L^{-2}=1,
\end{aligned}
\]

because \(m=\rho-\frac32c_\gamma\).  Thus the packet upper majorant
saturates, but does not exceed, the background \(B^3R^3\) scale.

The corresponding harmonic ratio is

\[
 \frac{\mathfrak a_*^3R^4L^{-7/2}}{B^3R^3}
 =\varkappa^3R\Gamma^{-3/2}L^{-7/2}
 =L^{-3/2}.
\]

The full nonlinear \(3/2\) power has therefore been retained.  Combining
these two rows with the energy and pressure rows gives the complete upper
bound

\[
 P_*\le CB^3R^3.
\]

No payment row is removed: Version M contains
\(\mathcal E^{3/2}+\mathcal G_u+\mathcal G_p+\mathcal H_u\), and Version F
adds only an acceleration row which is zero on this family.

### 3.3 Matching payment lower bound

Pointwise orthogonality gives

\[
 |u|^3=(\mathfrak a_*^2F^2+B^2\theta^2)^{3/2}
 \ge B^3|\theta|^3.
\]

The inherited fifth-shell box is independent of the passive amplitude, so

\[
 P_*\ge\mathcal G_{u,*}
 \ge8e^{-8}B^3R^3.
\]

Consequently

\[
 P_*\asymp B^3R^3.
\]

With \(\beta_j=B_jR_j^2\to1/128\), hence bounded above and away from zero,

\[
 B_j^3R_j^3=\beta_j^3R_j^{-3}
 =\beta_j^3e^{3\rho L_j^2},
\]

and therefore

\[
 P_j^*\to\infty,
 \qquad
 \log P_j^*=3\rho L_j^2+O(1).
\]

This lower bound is essential: the conclusion uses the complete payment,
not merely an upper surrogate.

## 4. Exact collar-flux and endpoint scaling

For fixed \(B,\theta,F,R\), the inherited exact signed flux has the form

\[
 \mathfrak F_R^{(\mathfrak a)}(\tau)
 =\mathfrak a^2\,K_R(\tau),
\]

where \(K_R(\tau)\) is independent of \(\mathfrak a\).  Hence, pointwise in
\(\tau\),

\[
 \mathfrak F_*(\tau)=\varkappa^2\mathfrak F_0(\tau).
\]

Since \(\varkappa^2>0\), positive part and supremum commute with the
constant multiplier:

\[
 \mathfrak C_* =\varkappa^2\mathfrak C_0.
\]

The R0.74H normalized lower bound and the R0.74N normalized all-shell upper
bound concern the same complete signed collar integral and give

\[
 \mathfrak C_0\asymp B^2LR^2.
\]

Therefore

\[
 \mathfrak C_*\asymp\varkappa^2B^2LR^2.
\]

The every-amplitude R0.74F terminal-lobe theorem gives independently

\[
 X_*^\alpha
 \ge c\mathfrak a_*^2LR^2\Gamma
 =c\varkappa^2B^2LR^2.
\]

For the reverse bound, the R0.74H signed-flux closure gives

\[
 X_*^\alpha
 \le C\left(P_*^{2/3}+\mathfrak C_*\right).
\]

The already established payment upper bound implies

\[
 P_*^{2/3}\le CB^2R^2
 \le C\varkappa^2B^2LR^2
\]

for all sufficiently large \(L\), while the independent collar upper bound
has the same amplified scale.  Thus

\[
 X_*^\alpha\asymp\mathfrak C_*^\alpha
 \asymp\varkappa^2B^2LR^2,
 \qquad \alpha\in\{M,F\}.
\]

This dependency is non-circular: packet survival proves the \(X\) lower
bound; R0.74N proves the normalized collar upper; exact quadratic amplitude
scaling transports that upper; only then does the general R0.74H energy
closure prove the \(X\) upper.

## 5. Independent scalar-frontier conversion

Direct substitution gives

\[
 \varkappa^2B^2LR^2
 =B^2R^2L^{7/3}e^{(2m/3)L^2}.
\]

Define

\[
 \delta_*:=\frac{2m}{9\rho}.
\]

Exact rational reduction gives

\[
 \delta_*=\frac{86}{11907},
 \qquad
 3\rho\delta_*=\frac{2m}{3},
\]

and therefore

\[
 q_*:=\frac23+\delta_*
 =\frac{8024}{11907}.
\]

Because \(P_*\asymp B^3R^3\) and \(\beta=BR^2\asymp1\),

\[
 P_*^{2/3}\asymp B^2R^2,
 \qquad
 P_*^{\delta_*}\asymp e^{(2m/3)L^2},
 \qquad
 (1+\log_+P_*)^{7/6}\asymp L^{7/3}.
\]

Multiplication yields exactly

\[
 X_*^\alpha\asymp\mathfrak C_*^\alpha
 \asymp
 P_*^{8024/11907}(1+\log_+P_*)^{7/6}.
\]

Dividing by the proposed square-root-log scale leaves

\[
 \frac{X_*^\alpha}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 \frac{\mathfrak C_*^\alpha}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 P_*^{86/11907}(1+\log_+P_*)^{2/3}
 \longrightarrow\infty.
\]

Thus any nonnegative scalar majorant

\[
 \Phi(p)=o\!\left(
 p^{8024/11907}(1+\log_+p)^{7/6}
 \right)
\]

fails uniformly along this one fixed sequence.  The argument does not claim
that \(8024/11907\) is an optimal universal frontier.

## 6. Fixed-γ polynomial-amplitude audit

Fix \(\gamma\in\mathbb R\), select

\[
 M>\max\left\{0,\gamma-\frac12\right\},
 \qquad
 \varkappa_\gamma=L^M.
\]

The three nonperiodic packet-to-background upper ratios independently reduce
to

\[
 L^{2M}e^{-e_EL^2},\qquad
 L^{3M-2}e^{-mL^2},\qquad
 L^{3M-7/2}e^{-mL^2},
\]

for energy, velocity cubic, and harmonic payment respectively.  All tend to
zero for fixed finite \(M\); the periodic term is super-exponentially
smaller.  The same fifth-shell lower bound then gives

\[
 P_{\gamma,*}\asymp B^3R^3,
 \qquad
 \log P_{\gamma,*}=3\rho L^2+O(1).
\]

Exact flux scaling, the every-amplitude terminal lower bound, and the
signed-flux upper closure give

\[
 X_{\gamma,*}^\alpha
 \asymp\mathfrak C_{\gamma,*}^\alpha
 \asymp B^2R^2L^{2M+1}.
\]

Meanwhile

\[
 P_{\gamma,*}^{2/3}
 (1+\log_+P_{\gamma,*})^\gamma
 \asymp B^2R^2L^{2\gamma}.
\]

The quotient is \(L^{2M+1-2\gamma}\to\infty\) because
\(2M+1-2\gamma>0\).  Hence every fixed logarithmic correction at power
\(2/3\) fails.  The quantifier is correctly stated: the polynomial-amplitude
family may depend on the prescribed \(\gamma\); one polynomial choice is not
claimed to defeat all \(\gamma\) simultaneously.

## 7. Claim-boundary audit

The proof supports exactly the following conclusions.

1. A universal bound depending only on the frozen scalar payment cannot have
   the proposed square-root-log size, or any \(o\)-size below the displayed
   realized frontier.
2. The failure occurs on smooth global periodic unforced exact solutions, so
   it is not evidence of blow-up.
3. The sequence has \(P_*\to\infty\), so it does not contradict the inherited
   small-payment implication.
4. The argument does not refute an estimate containing an additional
   temporal, geometric, BV, Carleson, pressure, or flux observable.
5. The necessary additive repair scale
   \(Y_*\gtrsim\varkappa^2B^2LR^2\) follows along this family, but sufficiency
   of a new non-flux observable is not proved.
6. No optimal replacement, novelty, or priority conclusion follows.
7. No singularity, epsilon-regularity failure, global-regularity theorem, or
   Millennium-problem solution follows.

The 26 rows of `research/r074o_gap_matrix.md` are consistent with this
classification.  In particular, its O23--O26 rows remain explicitly open or
not claimed.

\[
 \boxed{\text{INDEPENDENT MATHEMATICAL AUDIT: PASS; NOT CLAY.}}
\]
