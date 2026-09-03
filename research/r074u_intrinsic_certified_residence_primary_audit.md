# R0.74U Step 20 — independent primary analytic audit

## 0. Verdict and audit boundary

**Verdict: PASS.**

This audit independently checks the deductions in
r074u_intrinsic_certified_residence.md, with particular attention to the
exact annular margin, slab-truncated residence constants, extension of the
inherited packet estimates to the full terminal slab, separation of the
certified geometric corridor from a completed-clock superlevel set, and the
direction in which R0.74T (T.28) may be used.  The audited main source has
SHA-256

    e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99

This is a human-readable analytic audit.  It does not formally verify the
Navier--Stokes equations, independently reprove every inherited heat-kernel
estimate, or turn a finite computation into a PDE proof.  It proves no
regularity theorem, no singularity theorem, and no solution of the
Navier--Stokes Millennium problem.  **NOT CLAY.**

## 1. Frozen source ledger

The following SHA-256 hashes were recomputed directly from the files used by
Step 20.

| Role | Path | SHA-256 |
|---|---|---|
| audited Step 20 source | research/r074u_intrinsic_certified_residence.md | e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99 |
| completed-clock definitions and positivity | research/r074p_temporal_observable_triage.md | a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867 |
| schedule-invariant lobe coercivity and dwell threshold | research/r074t_schedule_invariant_dwell_coercivity.md | 8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd |
| exact common-shear Navier--Stokes family and platform lemma | research/r074q_common_shear_multipacket_gate.md | 60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695 |
| multipacket dominance and periodic remainder | research/r074q_relaxed_multipacket_cubic_obstruction.md | ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d |
| full-time bridge comparison and inverted-packet suppression | research/r074f_two_packet_survival.md | 0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb |
| Step 16 comparison boundary only | research/r074s_moving_frame_taylor_vortex_obstruction.md | de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0 |

The main source contains exactly 45 displayed U-labels in the strict order
U.1 through U.45.  No label is duplicated or missing.  This audit is bound
to the hashes above rather than to an unfrozen working-tree path alone.

## 2. Platform interval, calibration, and speed

For $i=1,2$, Step 20 sets

\[
 \varepsilon_i=4e^{-a_DL_i^2},
 \qquad
 a_D=\frac{49}{14625},
 \qquad
 L_i\ge L_1\ge9216.
\]

The exact endpoint calculation is

\[
 a_D(9216)^2=\frac{462422016}{1625}>4.
\]

Since $e^4>16$, this implies

\[
 \varepsilon_i<\frac14,
 \qquad
 1-\varepsilon_i>\frac34.
\]

The two-parameter platform lemma applies on the complete calibration
interval

\[
 R^2\le t\le65R^2,
\]

not merely on the terminal slab.  Integration over its length $64R^2$
therefore legitimately gives

\[
 64R^2(1-\varepsilon_1)\le D_1\le64R^2.
\]

Taking reciprocals in $B=(2D_1)^{-1}$ gives

\[
 \frac1{128R^2}
 \le B
 \le\frac1{128(1-\varepsilon_1)R^2}.
\]

On $I_R=(64R^2,65R^2)$,

\[
 Q_i'(t)=B\theta_R(t,h_i),
\]

so the packetwise platform bounds imply exactly

\[
 \frac{1-\varepsilon_i}{128R^2}
 \le Q_i'(t)
 \le\frac1{128(1-\varepsilon_1)R^2}.
\]

Every $Q_i$ is therefore strictly increasing on the slab.  The appearance
of $\varepsilon_i$ in the lower bound and $\varepsilon_1$ in the upper bound
is correct: the former comes from the $i$-th platform height, while the
common coefficient $B$ is calibrated using $D_1$.

The chart restriction also gives

\[
 R^{-1}\ge\frac{144}{5}L_2.
\]

Together with $R^{-1}e^{-a_SL_1^2}\to0$, this forces $L_1\to\infty$ and
then $R\to0$.  Thus later periodic-copy limits do not silently assume the
special relation $R=e^{-\rho L^2}$.

## 3. Exact annular geometry

The lobe $\Omega_i(t)$ has side lengths

\[
 \frac{r_i}{8},\qquad \frac R4,\qquad 2R.
\]

Its volume is exactly

\[
 |\Omega_i(t)|=\frac{r_iR^2}{16}
 =\frac1{16}L_iR^3.
\]

The sufficient symmetric centre margin is

\[
 A(L)=
 \sqrt{\left(\frac2\lambda\right)^2-\frac1{256}
       -\left(c_h+\frac1L\right)^2}
 -\frac{b_2}{L}.
\]

At the conservative endpoint $L=9216$, the exact lower-margin calculation is

\[
 \left(\frac2\lambda\right)^2-\frac1{256}
 -\left(c_h+\frac1L\right)^2
 -\left(\frac38+\frac{b_2}{L}\right)^2
 =\frac{15232043}{1849688064}>0.
\]

All $L^{-1}$ corrections decrease as $L$ increases.  Hence

\[
 A(L)>\frac38
 \qquad(L\ge9216).
\]

The upper estimate $A(L)<1$ is uniform as well, since the radicand is
strictly less than its limiting upper value

\[
 \left(\frac{64}{63}\right)^2-\frac1{256}
 -\left(\frac{15}{16}\right)^2
 =\frac{75791}{508032}<1.
\]

For the inner shell boundary, the exact reserve is

\[
 c_h-\frac1{9216}-\frac1\lambda
 =\frac{9235}{21504}>0.
\]

Thus $|x|>r_i/\lambda=2^{k_i}R$ follows from the vertical coordinate
alone.  If $|Q_i(t)|<A(L_i)r_i$, the box bounds give

\[
 \frac{|x|^2}{r_i^2}
 <\frac1{256}
  +\left(A(L_i)+\frac{b_2}{L_i}\right)^2
  +\left(c_h+\frac1{L_i}\right)^2
 =\left(\frac2\lambda\right)^2.
\]

This is precisely $|x|<2r_i/\lambda=2^{k_i+1}R$.  The chart condition keeps
the full box in the central lift, so there is no hidden torus-distance
substitution.  It follows that

\[
 \Omega_i(t)\subset A_{k_i}(R),
 \qquad
 \Psi_{k_i}^R=1\quad\hbox{on }\Omega_i(t).
\]

The function $A(L)$ is an exact sufficient symmetric centre margin for this
chosen box.  It is not asserted to describe every centre for which some
portion of a packet lies in the shell, and it is not a completed-clock
statement.

## 4. Residence constants and slab truncation

For clarity in this audit, write

\[
 \Theta_i^{\rm geom}:=\mathscr R_i^{\rm cert}
 =\{t\in I_R:|Q_i(t)|<A(L_i)r_i\}.
\]

This is a geometric time corridor.  Since $Q_i(\tau_i)=0$, the speed upper
bound guarantees that every available one-sided segment of length less than

\[
 \frac{A(L_i)L_iR}
 {1/[128(1-\varepsilon_1)R^2]}
 =128A(L_i)(1-\varepsilon_1)L_iR^3
\]

stays within the sufficient centre interval.  The lower bounds on $A$ and
$1-\varepsilon_1$ make this quantity strictly larger than

\[
 128\cdot\frac38\cdot\frac34L_iR^3
 =36L_iR^3.
\]

At least one side of every $\tau_i\in\overline I_R$ has slab room at least
$R^2/2$.  Moreover,

\[
 L_iR\le\frac5{144}
 \quad\Longrightarrow\quad
 \frac{72}{5}L_iR^3\le\frac{R^2}{2}.
\]

Taking the smaller of the travel allowance and slab room proves

\[
 |\Theta_i^{\rm geom}|\ge\frac{72}{5}L_iR^3.
\]

For the upper estimate, strict monotonicity of $Q_i$ and its derivative
lower bound show that the preimage of the centre interval of width
$2A(L_i)r_i$ has measure at most

\[
 \frac{2A(L_i)L_iR}
 {(1-\varepsilon_i)/(128R^2)}
 =\frac{256A(L_i)}{1-\varepsilon_i}L_iR^3.
\]

Intersection with the slab gives the independent upper bound $R^2$.
Because $A(L_i)<1$ and $1-\varepsilon_i>3/4$,

\[
 |\Theta_i^{\rm geom}|
 \le\min\left\{R^2,
 \frac{256A(L_i)}{1-\varepsilon_i}L_iR^3\right\}
 <\frac{1024}{3}L_iR^3.
\]

Thus the constants $72/5$, $256$, and $1024/3$, and every inequality
direction in (U.21)--(U.24), are correct.

This upper bound belongs only to the full preimage of the chosen symmetric
sufficient centre condition.  It is not a maximal physical-shell residence
bound and cannot be transferred to a completed-clock superlevel set.

## 5. Full-slab packet survival

The extension from the previously selected $R^3$ window to the full slab
$I_R$ uses compatible inherited quantifiers.

1. R0.74F Lemma 4.1 is uniform for
   $0\le t\le65R^2$, $|y|\le R$, and every horizontal offset $z$.
   Its proof needs the saturation platform, an $O(R^{-2})$ bound on $B$,
   the chart separation, and the all-winding bridge estimate.  Step 20 has
   the stronger explicit coefficient bound

   \[
    B<\frac1{96R^2}<\frac1{32R^2},
   \]

   while $R^{-1}\ge(144/5)L_2\ge L_i$ supplies the inherited winding
   comparison.  Horizontal translation does not enter these constants
   because it commutes with the common scalar equation.
2. Both bridge exponentials vanish uniformly in $i$.  The exact comparison

   \[
    a_D-a_S=\frac{6997}{329472000}>0
   \]

   makes the $a_D$ term subordinate to the assumed $a_S$ reserve
   $R^{-1}e^{-a_SL_1^2}\to0$.  The remaining $e^{-c/R^2}$ term vanishes
   because $R\to0$.
3. On $I_R$, the normalized heat age lies in $(65,66)$, the normalized
   horizontal offset lies in $(5/4,3/2)$, and the normalized vertical offset
   lies in $(-1,1)$.  The central real-Gaussian derivative has one sign and
   a positive minimum on this compact box.  Its noncentral periodic copies
   vanish exponentially.  Repeating this compact-minimum step gives (U.28)
   on the whole slab.  R0.74Q Step 2 (Q.130) itself was stated only on the
   shorter window; Step 20 correctly does not silently enlarge that
   conclusion.
4. R0.74F Lemma 5.1 is already uniform for the same full time interval and
   for every $x_2$.  Arbitrary horizontal re-centring therefore does not
   weaken the inverted-packet estimate.
5. R0.74Q Step 2 (Q.138)--(Q.153) estimates the other packet through the
   vertical heat kernel after taking the supremum of the horizontal
   derivative kernel.  Its relevant quantifier is again
   $0\le t\le65R^2$.  Neither $q_{{\rm pre},i}$ nor the size of $Q_i(t)$ in
   the certified corridor changes those constants.

The exact cross-tail margins are

\[
 a_\times-\frac32c_\gamma
 =\frac{67}{242550}>0,
 \qquad
 \mu_{\rm in}=\frac{4601}{2910600}>0.
\]

For the periodic term, set $q=c_\gamma/2=4/3969$.  The chart condition gives

\[
 qL_2^2-\frac3{22R^2}
 \le-\left[\frac3{22}\left(\frac{144}{5}\right)^2-q\right]L_2^2.
\]

The bracket is exactly

\[
 c_*=\frac{123450676}{1091475}>0.
\]

Thus the periodic remainder tends to zero without the special R0.74Q scale
law.

There are two distinct dominance steps.  First, (U.28) and (U.29) give
$|G_i|\ge c_0$ for the full inversion-paired $i$-th packet.  Second, the
amplitude-weighted cross-tail estimates give

\[
 \frac{\mathfrak a_{3-i}|G_{3-i}|}
 {\mathfrak a_i|G_i|}=o(1)
\]

uniformly on the moving $i$-th box.  Hence the first velocity component, and
therefore the full velocity norm, satisfies

\[
 |u(t,x)|\ge c\mathfrak a_i
\]

on the certified corridor.  No isolated packet summand is substituted for
the total field.

Both packets are evolved under the same coefficient $b$.  Their independent
horizontal translations commute with that equation, their inversion
partners preserve full oddness, and the even frozen mollifier gives

\[
 X_R=a_R=a_R'=0.
\]

Thus the physical boxes are the Version-M moving-frame boxes.  The
construction remains one exact smooth periodic mean-zero unforced
Navier--Stokes solution with $p=0$.

## 6. Geometric corridor versus clock superlevel

To make the one-way relation explicit, define for this audit

\[
 \Omega_i^K
 :=\{t\in I_R:K_{k_i,R}(t)\ge c_KT\}.
\]

This time set is distinct from the main source's spatial lobe
$\Omega_i(t)$.  The geometric-corridor-versus-clock-superlevel relation is

\[
 \boxed{\Theta_i^{\rm geom}\subset\Omega_i^K.}
\]

The time cutoff and shell cutoff equal one on the lobe, and every other
piece of the defect-completed clock is nonnegative.  Hence

\[
\begin{aligned}
 K_{k_i,R}(t)
 &\ge\frac{\Gamma_i}{2R}
       \int_{\Omega_i(t)}|u(t,x)|^2\,dx\\
 &\ge c\Gamma_i\mathfrak a_i^2L_iR^2\\
 &=cA_*^2R^2=cT.
\end{aligned}
\]

Consequently

\[
 |\Omega_i^K|\ge|\Theta_i^{\rm geom}|
 \ge\frac{72}{5}L_iR^3.
\]

Only this inclusion and lower measure bound are proved.  Accumulated
dissipation, another packet, off-target endpoint mass, or the common shear
may keep $K_{k_i,R}$ large after the chosen lobe exits its geometric
corridor.  Neither the reverse inclusion nor an upper bound for
$|\Omega_i^K|$ follows from (U.24).

## 7. Certified dwell and the direction of (T.28)

Set

\[
 \theta_{{\rm cert},2}
 =\frac{|\Theta_2^{\rm geom}|}{R^3}
 \ge\frac{72}{5}L_2.
\]

The moving spacetime lobe is measurable because $Q_2$ is smooth and the box
is specified by strict continuous inequalities.  R0.74T Lemma 2.1 therefore
applies to the full corridor.  The endpoint calculation gives a persistent
lobe floor $h_2\ge cT$, so

\[
 P_R^M\ge2\sqrt2\,
 \theta_{{\rm cert},2}h_2^{3/2}R
 \Gamma_2^{-5/4}L_2^{-1/2}.
\]

After taking the $2/3$ power and inserting the certified dwell lower bound,

\[
 \frac{(P_R^M)^{2/3}}{T}
 \ge cR^{2/3}\Gamma_2^{-5/6}L_2^{1/3}.
\]

The power $L_2^{1/3}$ is correct: $\theta^{2/3}$ contributes
$L_2^{2/3}$, while the Hölder expression contributes $L_2^{-1/3}$.

Now put

\[
 S=\log\frac1R,
 \qquad
 d_L=a_SL_1^2-S\to+\infty,
 \qquad
 L_2=2L_1.
\]

The exact logarithmic identity inherited from R0.74T is

\[
 \log\Lambda_2
 =\frac23\left[
 \log\theta+(5c_\gamma-a_S)L_1^2+d_L
 -\frac12\log L_2\right].
\]

Since

\[
 \log\theta_{{\rm cert},2}
 \ge\log\frac{72}{5}+\log L_2,
\]

one gets

\[
 \log\Lambda_2
 \ge\frac23\left[
 \log\frac{72}{5}
 +(5c_\gamma-a_S)L_1^2+d_L
 +\frac12\log L_2\right].
\]

The exact exponent reserve is

\[
 5c_\gamma-a_S
 =\frac{603445}{89413632}>0.
\]

It follows that $(P_R^M)^{2/3}/T\to\infty$.

The use of R0.74T (T.28) has the correct conditional direction.  If one
instead assumes that $(P_R^M)^{2/3}/T$ remains bounded, then
$h_2\ge cT$ and the coercive lower bound force $\Lambda_2=O(1)$.  Solving
this necessary condition for the dwell gives

\[
 \theta_{{\rm cert},2}
 \le CR^{-1}\Gamma_2^{5/4}L_2^{1/2}
 =CL_2^{1/2}
 e^{-(5c_\gamma-a_S)L_1^2-d_L}.
\]

This is a necessary consequence of the hypothetical bounded-payment
assumption, not an unconditional upper bound on the actual corridor.  It is
incompatible with

\[
 \theta_{{\rm cert},2}\ge\frac{72}{5}L_2.
\]

The ratio between the proved lower dwell and the conditionally permitted
dwell is bounded below by

\[
 cL_2^{1/2}
 e^{(5c_\gamma-a_S)L_1^2+d_L}\to\infty.
\]

Thus neither the implication nor the inequality in (U.40)--(U.41) is
reversed.

## 8. Explicit phase constants

For

\[
 \tau_1=64R^2+2R^3,
 \qquad
 \tau_2=65R^2,
 \qquad
 R<\frac13,
\]

the inner forward slab room is

\[
 65R^2-\tau_1=R^2(1-2R)>\frac13R^2.
\]

Since $L_1R\le5/288$,

\[
 \frac{96}{5}L_1R^3\le\frac13R^2.
\]

For the outer packet, $L_2R\le5/144$ gives

\[
 \frac{144}{5}L_2R^3\le R^2.
\]

Both constants are smaller than the geometric travel constant $36$.
Therefore the one-sided bounds $96/5$ and $144/5$ in (U.45) are correct.
The first concerns the forward portion after $\tau_1$, not the earlier
$R^3$ window in R0.74T; the source states this distinction.

## 9. Claim-boundary audit

The source correctly distinguishes the following statements.

- $\mathscr R_i^{\rm cert}$ is the full time preimage of one explicit
  sufficient symmetric centre margin.  Its two-sided
  $\Theta(L_iR^3)$ estimate is proved.
- The completed-clock superlevel set is only known to contain that corridor.
  Its maximal extent and every upper measure bound remain open.
- The theorem closes the exponentially short-dwell escape only for the
  frozen saturation-shear, derivative-heat-packet architecture.
- It does not rule out a different shear, packet shape, shell placement, or
  a clock produced mainly by accumulated dissipation.
- It supplies no upper bound for the fixed-deletion completed-clock
  functional, no arbitrary-clock lobe extraction theorem, and no transfer
  to the stopped-flux functional.
- The high-Rayleigh branch, anomalous-defect branch, fixed-deletion gate,
  direct hybrid gate, Q.12, Q.1, scale contraction, regularity, and
  singularity formation all remain open.

Within these boundaries, (U.1)--(U.45) are mathematically consistent and
the audited Step 20 source passes this independent primary analytic review.
**NOT CLAY.**

<!-- R074U_STEP20_PRIMARY_AUDIT_PASS -->
