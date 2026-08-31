# R0.73O gap matrix

**Status:** final after independent analytic audit and finite diagnostic

| Cell | Equation / background | Input topology | Output / event | Current state | Why |
|---|---|---|---|---|---|
| G1 | unforced, one a priori global mean-zero \(H^3\) orbit | \(H^3\)-small | uniform \(H^3\) closeness and exponential synchronization | **CLOSED CONDITIONALLY** | finite \(H^4\) action closes the bootstrap; the reference orbit is assumed global |
| G2 | same as G1 | \(H^3\)-small | fixed \(L^2\) closeness | **CLOSED AS COROLLARY** | \(H^3\hookrightarrow L^2\); input is not \(L^2\)-only |
| G3 | same as G1 | small only in \(L^2\), arbitrarily large \(H^3\) | global \(H^3\) continuation and \(L^2\) closeness | **OPEN / COLLISION-SENSITIVE** | G1 radius depends on \(H^3\); Mucha 2001 must be cited and its exact dependence not guessed |
| G4 | all unforced \(H^3\) data | none | global smooth solution | **OPEN** | this is the global-regularity problem |
| G5 | unforced global-data set \(\mathcal G_3\) | \(H^3\) neighborhood | neighboring global data | **CLOSED; CLASSICAL PHENOMENON** | follows from G1; Pizzocchero is a direct periodic smooth-data collision |
| G6 | unforced reference not known a priori global | \(H^3\)-small | use G1 to prove the reference is global | **LOGICALLY UNAVAILABLE** | the entry time and finite initial \(L^2H^4\) interval already assume global survival |
| F1 | forced \(U_*=(30.12\sin10y,0,0)\) | smooth/\(H^3\)-small planar sequence | fixed \(L^2\) escape | **CLOSED BY COMPOSITE CHAIN** | exact scaling + primary-source positive spectrum + 2D FPS |
| F2 | same forced equilibrium | planar smooth data | global smooth witness solution | **CLOSED CLASSICALLY** | planar invariance and 2D global regularity |
| F3 | same forced equilibrium | general nonplanar \(H^3\)-small data | global solution and escape | **NOT CLAIMED** | 3D globality is not supplied by FPS |
| F4 | same forced equilibrium | \(H^3\)-small | essentially 3D unstable mode | **OPEN / NOT NEEDED** | current eigenfunction is \(z\)-independent |
| C1 | compare G1 with F1 | topology-matched inputs | decay/stability versus nondecay/escape | **CLOSED AS A CONTRAST** | forcing changes accumulated action and the equation; no Clay transfer |
| C2 | infer Clay blow-up from F1 | any | singularity or nonuniqueness | **INVALID** | different forced equation; every witness solution is smooth |

## Quantifier diagram

The closed candidate on the unforced side is

\[
 \forall u_0\in\mathcal G_3\;\exists R[u]>0\;\forall t_0\ge0\;
 \forall v(t_0):
 \|v(t_0)-u(t_0)\|_{H^3}<R[u]
 \Longrightarrow v\hbox{ is global and synchronizes}.
\]

The still-open \(L^2\)-only cell would require

\[
 \forall u_0\in\mathcal G_3\;\forall\varepsilon>0\;\exists\delta>0\;
 \|v(t_0)-u(t_0)\|_{L^2}<\delta
\]

with no high-norm restriction capable of excluding arbitrarily oscillatory
regular data. The first statement does not imply the second.

The forced instability cell has the opposite existential pattern:

\[
 \exists U_*,\rho_*>0\;\forall\delta>0\;\exists w_0,t_*>0:
 \|w_0\|_{H^3}<\delta,
 \qquad
 \|u(t_*)-U_*\|_{L^2}\ge\rho_*.
\]

The witnesses are planar and globally smooth. This establishes nonlinear
instability without creating any singularity mechanism.

## Route decision after R0.73O

Because G1--G2 and F1--F2 pass, another fixed unforced global background is
not the next bottleneck: every such orbit is already inside the same
finite-action stability class. A meaningful next step must attack one of the
surviving interfaces explicitly:

1. the \(L^2\)-only/high-frequency perturbation gap G3;
2. a continuation criterion that does not assume the reference orbit global;
3. a nonautonomous or renormalized mechanism not reduced to a fixed global
   background;
4. a forced calculation only as a laboratory, with no transfer to Clay unless
   the forcing can be removed by a proved argument.
